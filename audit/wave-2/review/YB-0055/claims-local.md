**Claims**

1. Revision 2 is committed as `f1654cb` — NOT FOUND (no commit hash appears in the diff).
2. The acceptance command (`python3 -m pytest -q observer/tests && python3 agr/bench/tier0_vitals.py --smoke`) now passes — NOT FOUND (a runtime result; the diff contains no pass/fail output, and `observer/tests` is not in the diff).
3. 33 observer tests run — NOT FOUND.
4. 10 experiment tests run — NOT FOUND.
5. The experiment tests run from inside the smoke — `+        assert pytest.main(['-q', '-p', 'no:cacheprovider', tp]) == 0, 'tests/test_core.py failed'` (`tp = os.path.join(EXP, 'tests', 'test_core.py')`).
6. Smoke prints `ok` — `+    print(json.dumps(dict(smoke='ok', vitals_caught=s['monitors']['full']['caught'], ...`.
7. `project`, `cap_alarm`, the updated tests and docs were already uncommitted in the worktree and were kept — NOT FOUND (worktree/process state not in the diff).
8. Smoke called `V.project`, which didn't exist (blocking) — `+        assert k not in V.project(full), 'secret field %s survived the projection' % k` and `+    assert set(V.project(full)) <= set(V.CHIP_FIELDS + V.SCORING_FIELDS)` show the call; "didn't exist" NOT FOUND.
9. `project()` now exists in `vitals_tier0.py` — `+def project(r):` (in `src/vitals_tier0.py`).
10. `project` is applied in `recordings.load_seed` — `+    return [project(dict(r, idx=off + r['idx'], seed=seed)) for r in rows]` with `+from vitals_tier0 import project`.
11. text, entropy, p_top1, margin, toks, final, truth are dropped at load — `+    return {k: r.get(k) for k in ALLOWED}` (ALLOWED = CHIP_FIELDS + SCORING_FIELDS) and `+    for k in ('text', 'entropy', 'p_top1', 'margin', 'toks', 'final', 'truth'): ... assert k not in V.project(full)`.
12. The tier-0 restriction is enforced in the pipeline, and smoke and `test_project_drops_content` check it — `+def test_project_drops_content():` plus the smoke assertions above.
13. The unit tests were never run by acceptance before — NOT FOUND (a prior-state claim; not in the diff).
14. Smoke now runs `tests/test_core.py` through pytest so acceptance covers them — `+        import pytest` / `+        assert pytest.main(['-q', '-p', 'no:cacheprovider', tp]) == 0, 'tests/test_core.py failed'`.
15. `cap_alarm` splits ties at the threshold — `+        cut = max(sorted((keys[i] for i in tied))[:budget])` and `+            if V[i] > thr or (V[i] == thr and keys[i] <= cut): f[i] = True`.
16. The length and type controls can reach the 10% cap — `+CAP, COST = 0.10, 0.005` and `+    # the length and question-type baselines take few distinct values; ... cap_alarm splits` `+    # that tie, so the control reaches the cap (FPR exactly the cap) instead of being handicapped to 0.`
17. In the regenerated dry run they catch 8 (length) and 11 (type) — `+     "caught": 8,` (length block) and `+     "caught": 11,` (type block) in `docs/dryrun.json`.
18. Where before both caught 0 — NOT FOUND (old state; not in the diff).
19. `cap_alarm` is used in `evaluate` — `+    thr = cap_threshold([v for v, yy in zip(V, y) if yy == 0]); f = cap_alarm(V, y, CAP, seed=0)`.
20. `cap_alarm` is used in `boot_diff` — via `recall_at_cap`: `+    f = cap_alarm(V, y, CAP, seed=seed)` and `+        d.append(recall_at_cap([Va[k] for k in i], yy, seed=s) - recall_at_cap([Vb[k] for k in i], yy, seed=s))`.
21. `cap_alarm` is used in the equal-false-alarm count — `+        out['S_equal_fpr_monitorable_caught'] = {m: sum(1 for f, yy in zip(cap_alarm([vv[i] for i in mon_idx], mony, CAP, seed=0), mony)``.
22. The baselines are no longer handicapped to zero — `+    # that tie, so the control reaches the cap (FPR exactly the cap) instead of being handicapped to 0.`
23. `PREREGISTRATION.md` says no seed is fresh across the program — `+None is fresh across the chip program, so "fresh" here means *held`.
24. `recordings.py` says the same — `+# recordings: none is fresh across the chip program; "fresh" here means held out from YB-0055's model selection.`
25. 27–38 were YB-0051 test seeds — `+HOME.update({s: 'YB-0051-low-false-alarm-precision' for s in range(27, 39)})`.
26. "Fresh" means held out from this experiment's model selection — `+out from YB-0055's own model selection* (only the derivation seeds 2-14 select the model and threshold; 15-38 are untouched by it).`
27. The run is corroboration (of YB-0051), not a fresh confirmation — `+this run is *corroboration* of the YB-0051 result on the same held-out` / `+seeds, not a fresh confirmation; that is stated in the verdict, not hidden.`
28. The pre-registration no longer states "about 43 / 500 / 0.2" — NOT FOUND (all files are new in this diff; no deletion of those numbers is shown, so the removal cannot be verified from the diff).
29. It records that `inspect_seeds.py` was run once as a descriptive look at labels — `+Before this record, `tests/inspect_seeds.py` was run once for a *descriptive*`.
30. No model was fitted or score computed on those counts — `+That is a peek at the labels only; it fits no model, computes no score, and the design does not depend on those counts (see`.
31. The power claim now reads "not recorded in the analysed fields" — `+ "power": "not recorded in the analysed fields; not testable here (a descriptive check, not this result)",` (dryrun.json) and `+               power='not recorded in the analysed fields; not testable here (a descriptive check, not this result)',` (analysis.py).
32. It no longer reads "null in every recording" — NOT FOUND (old wording; not in the diff).
33. Only the seeds the agent inspected showed null — NOT FOUND.
34. The README no longer says "pre-registered" — NOT FOUND (the diff only adds `+**Status:** code and pre-registration written, NOT yet timestamped ...`, which still contains "pre-registration"; the removal is not shown).
35. The README says "not yet timestamped" — `+**Status:** code and pre-registration written, NOT yet timestamped and not run on the test seeds (timestamping needs network and is a local step).`
36. `docs/dryrun.json` is regenerated — `+++ b/algorithms/YB-0055-chip-visible-vitals/docs/dryrun.json` ... `+ "dry_run": true`.
37. The dry run shows the pipeline runs, not that the regulator works — NOT FOUND as a direct statement (a characterization; the diff records `+ "H_supported": true` for the synthetic primary, which the claim says not to read as such).
38. `scripts/timestamp_prereg.sh` needs network — `+Timestamp with `scripts/timestamp_prereg.sh`` and `+(needs network + a `.venv/ots`; not run from this agent).`.
39. That step stays local, before `--run` — `+algorithms/YB-0055-chip-visible-vitals/docs/PREREGISTRATION.md` and commit the proofs before running` / `+`python3 agr/bench/tier0_vitals.py --run` (needs network + a `.venv/ots`; not run from this agent).`
40. "Follows YB-0035 corrected.py" — `+Statistics follow YB-0035 corrected.py (in-time max, 10 percent cap, threshold-resampling bootstrap);`.
41. No comparison test was added (negative claim) — NOT FOUND.
42. `corrected.py` is skip-worktree / outside what may be touched — `+    skip-worktree has hidden it (as src/recordings.py does for the data). The module is registered in` (refers to `recordings.py`/data, not to `corrected.py` specifically; the "may not touch" scope is NOT FOUND).
43. The tie-aware cap is a documented departure from YB-0035 — `+the 10 percent cap is tie-aware: cap_alarm splits the tie at the threshold by a per-episode draw so a control whose score`.
44. The "acceptance.log shows a pass" claim was the launcher's stale log of an earlier tree calling an undefined `project` — NOT FOUND.
45. Commit "YB-0055 (#4): project() at the load boundary, tie-aware 10 percent cap, unit tests inside the smoke, honest status" — project at load boundary: `+def project(r):` / `+    return [project(dict(r, idx=off + r['idx'], seed=seed)) for r in rows]`; tie-aware cap: `+    thr = cap_threshold([V[i] for i in neg], cap)` ... `+        cut = max(sorted((keys[i] for i in tied))[:budget])`; unit tests inside smoke: `+        assert pytest.main(['-q', '-p', 'no:cacheprovider', tp]) == 0`; "honest status" NOT FOUND.
46. Commit "Revision 1: work left uncommitted by the agent, committed by the launcher (#4)" — NOT FOUND.
47. Commit "YB-0055 (#4): tier-0 vitals regulator, pre-registration, dry run and smoke test" — regulator: `+CHIP_FIELDS = ('idx', 'seed', 'latency', 'power')`; pre-registration: `+++ b/.../docs/PREREGISTRATION.md`; dry run: `+ "dry_run": true`; smoke test: `+def smoke():`.

**Numbers in the changed documents**

1. `2026` (tier0_vitals.py, README, all files) — recorded in `+# Copyright (c) 2026 Yobie Benjamin. ...`.
2. `7f3c2a9e-5b14-4d6e-9a1f-2c8e0b6d4a71` (canary, all files) — recorded in `+ Provenance canary: AGR-CANARY-7f3c2a9e-5b14-4d6e-9a1f-2c8e0b6d4a71`.
3. `YB-0055` (all files) — reference id, recorded in headers/docstrings.
4. `160` (tier0_vitals.py) — recorded/computed in `+    R = V.synth(160, 1)` and `+    res = analyse(R, {'smoke_test': V.synth(160, 2)}, boots=40, ...)`.
5. `9.9` (tier0_vitals.py) — recorded in `+    r2 = dict(r, latency=r['latency'][:t] + [9.9] * (len(r['latency']) - t))`.
6. `0.1 / 0.9 / 0.2 / 1` (tier0_vitals.py smoke `full` dict) — recorded in `+    full = dict(R[0], text='secret', entropy=[0.1], p_top1=0.9, margin=0.2, toks=[1], final='x', truth='y')`.
7. `40` boots (tier0_vitals.py smoke) — recorded in `+    res = analyse(R, {'smoke_test': V.synth(160, 2)}, boots=40, log=lambda *a: None)`.
8. `1e-9` (tier0_vitals.py smoke) — recorded in `+        assert m['fpr'] <= V.CAP + 1e-9, m`.
9. `1500 / 3 / 200 / 600 / 2` (tier0_vitals.py dry) — recorded in `+    res = analyse(V.synth(1500, 1) + V.synth(1500, 3), {'primary': V.synth(600, 2)}, boots=200)`.
10. `1000` boots (tier0_vitals.py run) — recorded in `+    res = analyse(deriv, tests, boots=1000)`.
11. `2..14` (DERIV) — recorded in `+DERIV = tuple(range(2, 15))`.
12. `38` (PRIMARY) — recorded in `+PRIMARY = 38`.
13. `27..37` (SECONDARY) — recorded in `+SECONDARY = tuple(range(27, 38))`.
14. `YB-0055` / status (README) — recorded in `+**Status:** code and pre-registration written, NOT yet timestamped ...`; README contains no other numeric literal.
15. `10 percent` (PREREGISTRATION, two places) — recorded in `+matched 10 percent false-alarm rate, better than the length and question-type baselines?` and `+threshold per monitor is the tightest with at most 10 percent of all correct answered test episodes alarmed.`
16. `0.005 s` (PREREGISTRATION) — recorded in `+A check at t is in time if elapsed(t) + 0.005 s is at most the time the final answer starts;`.
17. `48, 96, 192, 384` (PREREGISTRATION) — recorded in `+## Features (at checkpoint t in 48, 96, 192, 384, t before the final answer starts`.
18. `16` (PREREGISTRATION) — recorded in `+log of recent (last 16 tokens) over prefix mean latency;`.
19. `1.5` (PREREGISTRATION) — recorded in `+fraction of tokens slower than 1.5 times the median;`.
20. `1, 10, 100` and `5` (PREREGISTRATION) — recorded in `+Ridge strength chosen from 1, 10, 100 by 5-fold episode-grouped cross-validated AUROC on derivation only.`
21. `2 to 14` (PREREGISTRATION) — recorded in `+Derivation: seeds 2 to 14 (the recordings of YB-0033 to YB-0045).`.
22. `38` (PREREGISTRATION) — recorded in `+**Primary test: seed 38**, scored once.`.
23. `27 to 37` (PREREGISTRATION) — recorded in `+check, same frozen model, reported separately, never changes the primary verdict): seeds 27 to 37.**`.
24. `2 to 38` (PREREGISTRATION) — recorded in `+The recorded corpus is seeds 2 to 38;`.
25. `2,3,4,8 / 5-14 / 15-26 / 27-38` (PREREGISTRATION) — recorded in `+(2,3,4,8), YB-0045 (5-14), YB-0050 (15-26) and YB-0051 (27-38).`.
26. `1,000` resamples (PREREGISTRATION) — recorded in `+(threshold-resampling bootstrap, 1,000` / `+resamples, 95 percent CI).`
27. `95 percent` (PREREGISTRATION) — recorded in `+resamples, 95 percent CI).`
28. `0` (PREREGISTRATION decision) — recorded in `+**Supported iff both lower bounds exceed 0 on the primary seed.**`.
29. `0.2` (PREREGISTRATION power) — recorded in `+and a modest advantage is unlikely to resolve on one seed. The informative check is the pooled secondary (seeds 27 to 37, an order of` (i.e. "large (order 0.2)").
30. `48` (PREREGISTRATION, episodes finishing before t=48) — recorded in `+episodes finishing before t = 48 stay in and can never be alarmed.`
31. `1.0` lam, `1.0 / 1.0 / 0.9998` lam_cv_auroc (dryrun.json) — computed in `+    cvs = {lam: cv_oof(Rd, lam) for lam in LAMS}; lam = max(LAMS, key=lambda l: (cvs[l][1], -l))` via `auroc`, recorded in `+ "lam": 1.0,` and `+  "1.0": 1.0, "10.0": 1.0, "100.0": 0.9998`.
32. `3000` derivation_answered (dryrun.json) — computed in `+               derivation_answered=len(Rd),`, recorded in `+ "derivation_answered": 3000,`.
33. `8203` derivation_rows (dryrun.json) — computed in `+derivation_rows=len(jobs),`, recorded in `+ "derivation_rows": 8203,`.
34. `346` derivation_wrong (dryrun.json) — computed in `+derivation_wrong=sum(wrong_of(r) for r in Rd),`, recorded in `+ "derivation_wrong": 346,`.
35. `weights_full` values `4.818, -0.1369, -0.0833, -0.0069, -2.3155, 1.0329, 3.1459, -6.7028, -6.7637, -7.4972, -8.6572` (dryrun.json) — computed in `+weights_full=dict(zip(list(GROUPS['full']) + ['int%d' % t for t in T], [round(w, 4) for w in models['full'].w])),`, recorded in the `+ "weights_full": { ... }` block.
36. power string (dryrun.json) — computed in `+               power='not recorded in the analysed fields; not testable here (a descriptive check, not this result)',`, recorded in `+ "power": "not recorded in the analysed fields; not testable here (a descriptive check, not this result)",`.
37. primary `answered 600 / wrong 93 / monitorable 561 / short_correct_included 32` (dryrun.json) — computed in `+        out = dict(answered=len(A), wrong=sum(y), monitorable=sum(mon), short_correct_included=sum(1 for m, yy in zip(mon, y) if not m and yy == 0), monitors=per)`, recorded in `+   "answered": 600,` / `+   "wrong": 93,` / `+   "monitorable": 561,` / `+   "short_correct_included": 32,`.
38. full monitor `threshold -5.6122 / caught 86 / wrong 93 / recall 0.9247 / fpr 0.0986 / fpr_monitorable 0.1053 / recall_monitorable 1.0` (dryrun.json) — computed in `+    return dict(threshold=thr, caught=sum(f[i] for i in w), wrong=len(w), recall=..., fpr=..., fpr_monitorable=..., recall_monitorable=...)` (`evaluate`), recorded in the `+    "full": { ... }` block.
39. length monitor `threshold 384.0 / caught 8 / recall 0.086 / fpr 0.0986 / fpr_monitorable 0.1053 / recall_monitorable 0.093` (dryrun.json) — computed via `evaluate` from `+V['length'] = in_time(A, lambda r, t: float(t), lambda r, t: 0.0)`, recorded in the `+    "length": { ... }` block.
40. type monitor `threshold 0.119 / caught 11 / recall 0.1183 / fpr 0.0986 / fpr_monitorable 0.1053 / recall_monitorable 0.1279` (dryrun.json) — computed via `evaluate` from `+V['type'] = in_time(A, lambda r, t: rate.get(r['cat'], 0.0), lambda r, t: 0.0)`, recorded in the `+    "type": { ... }` block.
41. level/shape monitors `threshold -5.6357 / -2.1595`, `caught 86` (dryrun.json) — computed via `evaluate` on `GROUPS['level']`/`GROUPS['shape']`, recorded in the `+    "level": { ... }` / `+    "shape": { ... }` blocks.
42. `H_vitals_minus_length [0.8387, 0.7632, 0.9135]` (dryrun.json) — computed in `+out['H_vitals_minus_length'] = boot_diff(V['full'], V['length'], y, boots)`, recorded in `+    0.8387, 0.7632, 0.9135`.
43. `H_vitals_minus_type [0.8065, 0.75, 0.9]` (dryrun.json) — computed in `+out['H_vitals_minus_type'] = boot_diff(V['full'], V['type'], y, boots)`, recorded in `+    0.8065, 0.75, 0.9`.
44. `H_supported true` (dryrun.json) — computed in `+        out['H_supported'] = bool(out['H_vitals_minus_length'][1] > 0 and out['H_vitals_minus_type'][1] > 0)`, recorded in `+   "H_supported": true,`.
45. `S_full_minus_level [0,0,0]`, `S_full_minus_shape [0,0,0]` (dryrun.json) — computed in `+out['S_full_minus_level'] = boot_diff(V['full'], V['level'], y, boots); out['S_full_minus_shape'] = boot_diff(V['full'], V['shape'], y, boots)`, recorded in the `+ "S_full_minus_level": [...]` / `+ "S_full_minus_shape": [...]` blocks.
46. `S_equal_fpr_monitorable_caught {full 86, level 86, shape 86, length 9, type 12}` (dryrun.json) — computed in `+        out['S_equal_fpr_monitorable_caught'] = {m: sum(1 for f, yy in zip(cap_alarm([vv[i] for i in mon_idx], mony, CAP, seed=0), mony) ...}`, recorded in `+ "S_equal_fpr_monitorable_caught": { ... }`.
47. `S_frozen_derivation_threshold threshold -5.607557229734349 / caught 86 / fpr 0.0986` (dryrun.json) — computed in `+        out['S_frozen_derivation_threshold'] = dict(threshold=frozen, caught=sum(1 for a, yy in zip(f, y) if a and yy), fpr=round(sum(1 for a, yy in zip(f, y) if a and not yy) / max(1, y.count(0)), 4))`, recorded in `+ "S_frozen_derivation_threshold": { ... }`.
48. per-checkpoint `48/96/192/384 → episodes 561/509/395/176, wrong 86/81/59/24, vitals auroc [1,1,1], type auroc 0.489/0.4948/0.5295/0.5496 (CIs ...)` (dryrun.json) — computed in `+            pc[str(t)] = dict(episodes=len(idx), wrong=sum(yt), auroc_with_ci=dict(vitals=boot_auc(...), type=boot_auc(...)))`, recorded in the `+ "S_per_checkpoint_auroc": { ... }` block.
49. `dry_run true` (dryrun.json) — recorded in `+ "dry_run": true`.
50. `1.0, 10.0, 100.0` LAMS (analysis.py) — recorded in `+LAMS = (1.0, 10.0, 100.0)`.
51. `5` FOLDS (analysis.py) — recorded in `+FOLDS = 5`.
52. `1000` default boots (analysis.py) — recorded in `+def analyse(deriv, tests, boots=1000, log=print):`.
53. `0` wrong_of (analysis.py) — recorded in `+def wrong_of(r): return 0 if r['correct'] else 1`.
54. `0.0` length/type cost (analysis.py) — recorded in `+V['length'] = in_time(A, lambda r, t: float(t), lambda r, t: 0.0); V['type'] = in_time(A, lambda r, t: rate.get(r['cat'], 0.0), lambda r, t: 0.0)`.
55. `20` / `3` per-checkpoint gates (analysis.py) — recorded in `+            if len(idx) < 20 or sum(yt) < 3: continue`.
56. `100000` seed offset (recordings.py) — recorded in `+    off = 100000 * seed if off is None else off`.
57. `2, 3, 4, 8` (recordings.py) — recorded in `+HOME = {s: 'YB-0042-probe-baseline' for s in (2, 3, 4, 8)}`.
58. `5, 6, 7, 9, 10, 11, 12, 13, 14` (recordings.py) — recorded in `+HOME.update({s: 'YB-0045-powered-replication' for s in (5, 6, 7, 9, 10, 11, 12, 13, 14)})`.
59. `range(15, 27)` (recordings.py) — recorded in `+HOME.update({s: 'YB-0050-powered-decider' for s in range(15, 27)})`.
60. `range(27, 39)` (recordings.py) — recorded in `+HOME.update({s: 'YB-0051-low-false-alarm-precision' for s in range(27, 39)})`.
61. `48, 96, 192, 384` T (vitals_tier0.py) — recorded in `+T = (48, 96, 192, 384)`.
62. `0.10, 0.005` CAP, COST (vitals_tier0.py) — recorded in `+CAP, COST = 0.10, 0.005`.
63. `1e-4` (vitals_tier0.py, several) — recorded in `+    mean = sum(lg) / n; ... math.log(max(v, 1e-4))` and related lines.
64. `1e-6` (vitals_tier0.py) — recorded in `+            z = ...; s = p * (1 - p) + 1e-6` and `+        if max(abs(v) for v in step) < 1e-6: break`.
65. `1e-9` (vitals_tier0.py) — recorded in `+                self.mu[t][n], self.sd[t][n] = m, s if s > 1e-9 else 1.0`.
66. `1e-12` (vitals_tier0.py) — recorded in `+    k = int(math.floor(cap * n + 1e-12))` and `+    budget = int(math.floor(cap * len(neg) + 1e-12)) - len(over)`.
67. `16` recent window (vitals_tier0.py) — recorded in `+    med = sorted(dec)[n // 2]; rec = dec[-16:]`.
68. `1.5` stall fraction (vitals_tier0.py) — recorded in `+                stall_frac=sum(1 for v in dec if v > 1.5 * med) / n,`.
69. `12` iters (vitals_tier0.py) — recorded in `+def fit_logistic(X, y, lam, iters=12):`.
70. `30.0` clamp (vitals_tier0.py) — recorded in `+            z = sum(a * b for a, b in zip(w, xi)); p = 1 / (1 + math.exp(-max(-30.0, min(30.0, z))))`.
71. `0.12` default wrong_rate (vitals_tier0.py) — recorded in `+def synth(n, seed, wrong_rate=0.12):`.
72. `20 / 520` final_start range (vitals_tier0.py) — recorded in `+        wrong = g.random() < wrong_rate; fs = g.randrange(20, 520); nt = fs + 20`.
73. `0.011 / 1.15` base latency (vitals_tier0.py) — recorded in `+        base = 0.011 * (1.15 if wrong else 1.0)`.
74. `0.15 / 0.05 / 0.15 / 3 / 0.12 / 0.04` synth latencies (vitals_tier0.py) — recorded in `+        lat = [0.15] + [base * math.exp(g.gauss(0, 0.05 + (0.15 if wrong else 0.0))) * (3 if g.random() < (0.12 if wrong else 0.04) else 1) for _ in range(nt - 1)]`.
75. `100000` idx offset (vitals_tier0.py synth) — recorded in `+        R.append(dict(idx=seed * 100000 + i, ...)`.
76. `500` boot_auc n (vitals_tier0.py) — recorded in `+def boot_auc(y, s, n=500, seed=0):`.
77. `0.025 / 0.975` quantiles (vitals_tier0.py) — recorded in `+    a.sort(); return [round(auroc(y, s), 4), round(a[int(0.025 * len(a))], 4), round(a[min(len(a) - 1, int(0.975 * len(a)))], 4)]` and `+    return [round(recall_at_cap(Va, y) - recall_at_cap(Vb, y), 4), round(q(0.025), 4), round(q(0.975), 4)]`.
78. `0` neg filter (vitals_tier0.py) — recorded in `+    neg = [i for i, yy in enumerate(y) if yy == 0]`.
79. `YB-0035` ref (vitals_tier0.py) — recorded in `+Statistics follow YB-0035 corrected.py (...)`.
80. `48` final_start gate (inspect_seeds.py) — recorded in `+          'final_start>48', sum(r['final_start'] > 48 for r in a),`.
81. `200` sample slice (inspect_seeds.py) — recorded in `+    if p: print(' power sample', str(p[0])[:200])`.
82. `7, 20, 55, 100` (test_core.py) — recorded in `+    for n in (7, 20, 55, 100):`.
83. `0.10` / `1e-9` (test_core.py cap test) — recorded in `+        assert sum(x > thr for x in v) <= 0.10 * n + 1e-9`.
84. `1.0, 0.0, 10, 2` ties (test_core.py) — recorded in `+    v = [1.0] * 10 + [0.0] * 10; assert sum(x > V.cap_threshold(v) for x in v) <= 2`.
85. `5, 3, 48, 100, 5.0` (test_core.py features) — recorded in `+    r = V.synth(5, 3)[0]; a = V.features(r['latency'], 48); b = V.features(r['latency'][:48] + [5.0] * 100, 48)`.
86. `1, 1, 0.1` chip_view (test_core.py) — recorded in `+    r = dict(V.synth(1, 1)[0], text='secret', entropy=[0.1], final='x', truth='y')`.
87. `0.1, 0.2, 0.3, 0.4, 1.0, 0.5` auroc known (test_core.py) — recorded in `+    assert V.auroc([0, 0, 1, 1], [0.1, 0.2, 0.3, 0.4]) == 1.0 and V.auroc([0, 1], [0.5, 0.5]) == 0.5`.
88. `600, 7, 0.2, 10.0, 400, 8, 0.2, 0.7` logistic learns (test_core.py) — recorded in `+    R = V.synth(600, 7, 0.2); m = V.Vitals('full', 10.0).fit(V.make_jobs(R))` / `+    jobs = V.make_jobs(V.synth(400, 8, 0.2)); a = V.auroc(...)` / `+    assert a > 0.7`.
89. `5.0, 10.0, 1.0, 10.5` in_time_max (test_core.py) — recorded in `+    assert V.in_time_max([(5.0, 10.0, 1.0, 10.5)]) == -math.inf and V.in_time_max([(5.0, 1.0, 1.0, 10.5)]) == 5.0`.
90. `7, 20, 55, 100, 123` / `0.10` / `1e-9` / `0, 1, 2, 17` / `37, 7` cap_alarm test (test_core.py) — recorded in `+        for n in (7, 20, 55, 100, 123):` ... `+            for seed in (0, 1, 2, 17):` ... `+            f = V.cap_alarm([float((i * 37) % 7) for i in range(n)], y, seed=seed)` ... `+            assert sum(f[i] for i in range(nc)) <= 0.10 * nc + 1e-9`.
91. `90, 10, 100, 3, 8, 9` tied control (test_core.py) — recorded in `+    y = [0] * 90 + [1] * 10` / `+    scores = [3] * 100` / `+    for seed in range(8):` / `+        assert sum(V.cap_alarm(scores, y, seed=seed)[i] for i in range(90)) == 9` / `+    assert sum(sum(V.cap_alarm(scores, y, seed=s)[i] for i in range(90, 100)) for s in range(8)) > 0`.
92. `1, 1, 0.1, 0.9, 0.2, 1` project test (test_core.py) — recorded in `+    r = dict(V.synth(1, 1)[0], text='secret', entropy=[0.1], p_top1=0.9, margin=0.2, toks=[1], final='x', truth='y')`.

Note on the bulk of `docs/dryrun.json`: every floating-point value in that file (the `weights_full` coefficients, the per-monitor thresholds/recalls/fprs, the `H_vitals_minus_*` CIs, the per-checkpoint AUROCs and their CIs, etc.) is a computed output, not an independently stated figure — they are produced by `analyse()` in `src/analysis.py` (which calls the statistics in `src/vitals_tier0.py`: `cap_threshold`, `cap_alarm`, `boot_diff`, `auroc`, `boot_auc`) and written out by `+    json.dump(dict(res, dry_run=True), open(os.path.join(EXP, 'docs', 'dryrun.json'), 'w'), indent=1)`; no such number appears in the agent summary or commit messages except the two cited as `caught` 8 (length) and 11 (type), which are items 39–40 above.
