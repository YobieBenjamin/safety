# Copyright (c) 2026 Yobie Benjamin. Autonomic Graph Regulation (AGR). All rights reserved except as licensed.
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (see LICENSE.md, NOTICE)
# Provenance canary: AGR-CANARY-7f3c2a9e-5b14-4d6e-9a1f-2c8e0b6d4a71
'''Loads the existing recordings (seed<N>_LH.jsonl.gz). Reads the file from the checkout when it is materialised, otherwise
from the committed tree with `git show HEAD:<path>` (the checkout may hide large data with skip-worktree). Only the fields a
tier-0 observer could see are ever passed on: see vitals_tier0.chip_view.'''
import gzip, io, json, os, subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
HOME = {s: 'YB-0042-probe-baseline' for s in (2, 3, 4, 8)}
HOME.update({s: 'YB-0045-powered-replication' for s in (5, 6, 7, 9, 10, 11, 12, 13, 14)})
HOME.update({s: 'YB-0050-powered-decider' for s in range(15, 27)})
HOME.update({s: 'YB-0051-low-false-alarm-precision' for s in range(27, 39)})

def rel(seed): return 'algorithms/%s/data/seed%d_LH.jsonl.gz' % (HOME[seed], seed)

def raw_bytes(seed):
    p = os.path.join(ROOT, rel(seed))
    if os.path.exists(p):
        return open(p, 'rb').read()
    return subprocess.run(['git', '-C', ROOT, 'show', 'HEAD:' + rel(seed)], check=True, capture_output=True).stdout

def load_seed(seed, off=None):
    off = 100000 * seed if off is None else off
    return [dict(r, idx=off + r['idx'], seed=seed) for r in map(json.loads, io.TextIOWrapper(gzip.GzipFile(fileobj=io.BytesIO(raw_bytes(seed)))))]
