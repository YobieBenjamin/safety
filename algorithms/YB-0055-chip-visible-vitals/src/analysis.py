# Copyright (c) 2026 Yobie Benjamin. Autonomic Graph Regulation (AGR). All rights reserved except as licensed.
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (see LICENSE.md, NOTICE)
# Provenance canary: AGR-CANARY-7f3c2a9e-5b14-4d6e-9a1f-2c8e0b6d4a71
'''YB-0055 pre-registered analysis (see docs/PREREGISTRATION.md). analyse() is shared by the real run, the dry run and the smoke test.'''
import time
from vitals_tier0 import (T, COST, GROUPS, Vitals, make_jobs, features, checkpoints, in_time, evaluate, boot_diff, cap_threshold,
                          auroc, boot_auc)

LAMS = (1.0, 10.0, 100.0)
FOLDS = 5

def wrong_of(r): return 0 if r['correct'] else 1

def cv_oof(R, lam, group='full'):
    '''Out-of-fold scores on derivation rows, folds grouped by episode (idx mod FOLDS), returned as {(idx, t): score} and mean AUROC.'''
    jobs = make_jobs(R); oof = {}
    for k in range(FOLDS):
        tr = [j for j in jobs if j[0]['idx'] % FOLDS != k]; te = [j for j in jobs if j[0]['idx'] % FOLDS == k]
        m = Vitals(group, lam).fit(tr)
        for r, t, f, _ in te: oof[(r['idx'], t)] = m.score(f, t)
    y = [j[3] for j in jobs]; return oof, auroc(y, [oof[(j[0]['idx'], j[1])] for j in jobs])

def analyse(deriv, tests, boots=1000, log=print):
    '''deriv: list of episodes. tests: {name: list of episodes}; the first is the primary test set. Returns the results dict.'''
    t0 = time.time(); Rd = [r for r in deriv if r['answered']]
    cvs = {lam: cv_oof(Rd, lam) for lam in LAMS}; lam = max(LAMS, key=lambda l: (cvs[l][1], -l)); oof = cvs[lam][0]
    log('lambda %s cv auroc %s (%.0fs)' % (lam, {l: round(v[1], 4) for l, v in cvs.items()}, time.time() - t0))
    jobs = make_jobs(Rd); models = {g: Vitals(g, lam).fit(jobs) for g in GROUPS}
    rate = {}
    for r in Rd: rate.setdefault(r['cat'], []).append(wrong_of(r))
    rate = {c: sum(v) / len(v) for c, v in rate.items()}
    # frozen deployment threshold: the 10 percent cap on derivation correct episodes, scored out of fold
    Vd = in_time(Rd, lambda r, t: oof[(r['idx'], t)], lambda r, t: COST)
    frozen = cap_threshold([v for v, r in zip(Vd, Rd) if r['correct']])
    res = dict(lam=lam, lam_cv_auroc={str(l): round(v[1], 4) for l, v in cvs.items()}, derivation_answered=len(Rd), derivation_rows=len(jobs),
               derivation_wrong=sum(wrong_of(r) for r in Rd), weights_full=dict(zip(list(GROUPS['full']) + ['int%d' % t for t in T], [round(w, 4) for w in models['full'].w])),
               power='null in every recording (not testable here)', tests={})
    for name, R in tests.items():
        A = [r for r in R if r['answered']]; y = [wrong_of(r) for r in A]; mon = [len(checkpoints(r)) > 0 for r in A]
        V = {g: in_time(A, lambda r, t, m=models[g]: m.score(features(r['latency'], t), t), lambda r, t: COST) for g in GROUPS}
        V['length'] = in_time(A, lambda r, t: float(t), lambda r, t: 0.0); V['type'] = in_time(A, lambda r, t: rate.get(r['cat'], 0.0), lambda r, t: 0.0)
        per = {m: {k: (round(v, 4) if isinstance(v, float) else v) for k, v in evaluate(vv, y, mon).items()} for m, vv in V.items()}
        out = dict(answered=len(A), wrong=sum(y), monitorable=sum(mon), short_correct_included=sum(1 for m, yy in zip(mon, y) if not m and yy == 0), monitors=per)
        out['H_vitals_minus_length'] = boot_diff(V['full'], V['length'], y, boots); out['H_vitals_minus_type'] = boot_diff(V['full'], V['type'], y, boots)
        out['H_supported'] = bool(out['H_vitals_minus_length'][1] > 0 and out['H_vitals_minus_type'][1] > 0)
        out['S_full_minus_level'] = boot_diff(V['full'], V['level'], y, boots); out['S_full_minus_shape'] = boot_diff(V['full'], V['shape'], y, boots)
        ym = [yy for yy, m in zip(y, mon) if m]
        out['S_equal_fpr_monitorable_caught'] = {m: sum(1 for v, yy in zip([v for v, mm in zip(vv, mon) if mm], ym)
                                                       if yy == 1 and v > cap_threshold([a for a, b in zip([v for v, mm in zip(vv, mon) if mm], ym) if b == 0])) for m, vv in V.items()}
        f = [v > frozen for v in V['full']]
        out['S_frozen_derivation_threshold'] = dict(threshold=frozen, caught=sum(1 for a, yy in zip(f, y) if a and yy), fpr=round(sum(1 for a, yy in zip(f, y) if a and not yy) / max(1, y.count(0)), 4))
        pc = {}
        for t in T:
            idx = [i for i, r in enumerate(A) if t in checkpoints(r)]; yt = [y[i] for i in idx]
            if len(idx) < 20 or sum(yt) < 3: continue
            pc[str(t)] = dict(episodes=len(idx), wrong=sum(yt), auroc_with_ci=dict(
                vitals=boot_auc(yt, [models['full'].score(features(A[i]['latency'], t), t) for i in idx]), type=boot_auc(yt, [rate.get(A[i]['cat'], 0.0) for i in idx])))
        out['S_per_checkpoint_auroc'] = pc; res['tests'][name] = out
        log('%s: wrong %d, vitals caught %d, length %d, type %d, H_supported %s (%.0fs)' % (name, sum(y), per['full']['caught'], per['length']['caught'], per['type']['caught'], out['H_supported'], time.time() - t0))
    return res
