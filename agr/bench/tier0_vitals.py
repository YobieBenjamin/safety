#!/usr/bin/env python3
# Copyright (c) 2026 Yobie Benjamin. Autonomic Graph Regulation (AGR). All rights reserved except as licensed.
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (see LICENSE.md, NOTICE)
# Provenance canary: AGR-CANARY-7f3c2a9e-5b14-4d6e-9a1f-2c8e0b6d4a71
'''YB-0055 entry point. --smoke: synthetic episodes, checks the invariants (no future information, tier-0 view only, 10 percent cap),
seconds. --dry: the full pipeline on synthetic data, writes docs/dryrun.json. --run: the pre-registered single run on the recordings,
writes docs/results.json and refuses to run twice. See algorithms/YB-0055-chip-visible-vitals/docs/PREREGISTRATION.md.'''
import json, os, sys, subprocess, types

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
EXP = os.path.join(ROOT, 'algorithms', 'YB-0055-chip-visible-vitals')
PKG = 'algorithms/YB-0055-chip-visible-vitals'

def _load(name, rel):
    '''Load an experiment module from the checkout, or from the committed tree when sparse-checkout or
    skip-worktree has hidden it (as src/recordings.py does for the data). The module is registered in
    sys.modules before its source runs, so its cross-imports (analysis imports vitals_tier0) resolve.
    This is what makes the acceptance command reproduce in a clean checkout of the branch.'''
    if name in sys.modules:
        return sys.modules[name]
    p = os.path.join(EXP, rel)
    if os.path.exists(p):
        src = open(p).read()
    else:
        src = subprocess.run(['git', '-C', ROOT, 'show', 'HEAD:' + PKG + '/' + rel],
                             check=True, capture_output=True).stdout.decode('utf-8')
    mod = types.ModuleType(name); mod.__file__ = p
    sys.modules[name] = mod
    exec(compile(src, p, 'exec'), mod.__dict__)
    return mod

sys.path.insert(0, os.path.join(EXP, 'src'))   # the disk case; _load still works when the dir is absent
V = _load('vitals_tier0', 'src/vitals_tier0.py')
analyse = _load('analysis', 'src/analysis.py').analyse

DERIV = tuple(range(2, 15))                 # seeds recorded for YB-0033 to YB-0045
PRIMARY = 38                                # fresh seed, tested once
SECONDARY = tuple(range(27, 38))            # powered check with the frozen model, reported separately

def smoke():
    R = V.synth(160, 1)
    # 1. the tier-0 view carries nothing but the observable stream
    assert set(V.chip_view(R[0])) == set(V.CHIP_FIELDS), V.chip_view(R[0]).keys()
    # 2. no future information: a score at checkpoint t must not change when latencies after t change
    r = next(r for r in R if V.checkpoints(r)); t = V.checkpoints(r)[0]
    r2 = dict(r, latency=r['latency'][:t] + [9.9] * (len(r['latency']) - t))
    assert V.features(r['latency'], t) == V.features(r2['latency'], t), 'features read past the checkpoint'
    # 3. the load boundary projects to the tier-0 fields: secret fields never reach the analysis
    full = dict(R[0], text='secret', entropy=[0.1], p_top1=0.9, margin=0.2, toks=[1], final='x', truth='y')
    for k in ('text', 'entropy', 'p_top1', 'margin', 'toks', 'final', 'truth'):
        assert k not in V.project(full), 'secret field %s survived the projection' % k
    assert set(V.project(full)) <= set(V.CHIP_FIELDS + V.SCORING_FIELDS), V.project(full).keys()
    # 4. the matched false-alarm cap holds and the pipeline runs end to end
    res = analyse(R, {'smoke_test': V.synth(160, 2)}, boots=40, log=lambda *a: None)
    s = res['tests']['smoke_test']
    for m in s['monitors'].values():
        assert m['fpr'] <= V.CAP + 1e-9, m
    assert s['monitors']['full']['caught'] >= 0 and 'H_vitals_minus_length' in s
    print(json.dumps(dict(smoke='ok', vitals_caught=s['monitors']['full']['caught'], length_caught=s['monitors']['length']['caught'],
                          wrong=s['wrong'], fpr_full=s['monitors']['full']['fpr'])))

def dry():
    res = analyse(V.synth(1500, 1) + V.synth(1500, 3), {'primary': V.synth(600, 2)}, boots=200)
    json.dump(dict(res, dry_run=True), open(os.path.join(EXP, 'docs', 'dryrun.json'), 'w'), indent=1)

def run():
    load_seed = _load('recordings', 'src/recordings.py').load_seed
    out = os.path.join(EXP, 'docs', 'results.json')
    if os.path.exists(out): sys.exit('docs/results.json exists: the pre-registered test is run once')
    deriv = [r for s in DERIV for r in load_seed(s)]
    tests = {'primary_seed%d' % PRIMARY: load_seed(PRIMARY), 'secondary_seeds_%d_%d' % (SECONDARY[0], SECONDARY[-1]): [r for s in SECONDARY for r in load_seed(s)]}
    res = analyse(deriv, tests, boots=1000)
    res.update(dry_run=False, derivation_seeds=list(DERIV), primary_seed=PRIMARY, secondary_seeds=list(SECONDARY))
    json.dump(res, open(out, 'w'), indent=1)
    print(json.dumps({k: v['H_supported'] for k, v in res['tests'].items()}))

if __name__ == '__main__':
    a = sys.argv[1:]
    if '--smoke' in a: smoke()
    elif '--dry' in a: dry()
    elif '--run' in a: run()
    else: sys.exit(__doc__)
