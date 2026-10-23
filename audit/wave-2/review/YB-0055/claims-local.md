## Claims

1. **Revision 2 is committed (f1654cb)** — NOT FOUND (no `f1654cb` anywhere in the diff; it is git history, not diff content).
2. **The acceptance command now passes** — NOT FOUND in the diff (it is the gate's observation, not a line in the diff).
3. **I ran it once after the changes: 33 observer tests** — NOT FOUND (`observer/tests` is not in this diff, which contains only YB-0055 files).
4. **10 experiment tests (run from inside the smoke)** — FOUND: `test_core.py` defines exactly 10 `def test_` functions (`test_cap_threshold_respects_cap`, `test_cap_threshold_ties`, `test_features_use_prefix_only`, `test_chip_view_drops_content`, `test_auroc_known`, `test_logistic_learns_signal`, `test_in_time_excludes_late_checks`, `test_cap_alarm_respects_cap`, `test_tied_control_reaches_cap`, `test_project_drops_content`); smoke runs them: `assert pytest.main(['-q', '-p', 'no:cacheprovider', tp]) == 0, 'tests/test_core.py failed'`. (The number 10 is derived by counting, not written as a literal.)
5. **then smoke `ok`** — FOUND: `print(json.dumps(dict(smoke='ok', vitals_caught=...)))`.
6. **When I picked this up, `project`, `cap_alarm` and the updated tests and docs were already sitting uncommitted in the worktree** — NOT FOUND as a process claim; the artifacts' *presence* is confirmed (`def project(r):`, `def cap_alarm(V, y, cap=CAP, seed=None):`, `tests/test_core.py`, `docs/PREREGISTRATION.md`), but "uncommitted in the worktree" is not in the diff.
7. **I reviewed and kept them, and committed them along with my own changes** — NOT FOUND in the diff (process/commit-history claim; supported only by the "Revision 1: work left uncommitted by the agent, committed by the launcher" commit message, which is itself one of the claims under audit).
8. **Smoke called `V.project`, which didn't exist** — NOT FOUND for the "didn't exist" (before) half; the *current* call is FOUND: `assert k not in V.project(full), 'secret field %s survived the projection' % k`.
9. **`project()` now exists in `vitals_tier0.py`** — FOUND: `def project(r):` … `return {k: r.get(k) for k in ALLOWED}`.
10. **and is applied in `recordings.load_seed`** — FOUND: `return [project(dict(r, idx=off + r['idx'], seed=seed)) for r in rows]`.
11. **so text, entropy, p_top1, margin, toks, final and truth are dropped at load** — FOUND: `ALLOWED = CHIP_FIELDS + SCORING_FIELDS` (neither tuple contains those keys); recordings.py: "Everything else (text, entropy, p_top1, margin, toks, final, truth) is dropped here, at the load boundary".
12. **The tier-0 restriction is therefore enforced in the pipeline** — FOUND: `from vitals_tier0 import project` then `project(...)` in `load_seed`, used by `run()` via `load_seed`.
13. **and smoke and `test_project_drops_content` check it** — FOUND: smoke loop `assert k not in V.project(full)`; test `def test_project_drops_content():` … `assert k not in p`.
14. **Smoke now runs `tests/test_core.py` through pytest, so the acceptance command covers them** — FOUND: `tp = os.path.join(EXP, 'tests', 'test_core.py')` … `assert pytest.main(['-q', '-p', 'no:cacheprovider', tp]) == 0`.
15. **`cap_alarm` splits ties at the threshold** — FOUND: `tied = [i for i in neg if V[i] == thr]` … `cut = max(sorted((keys[i] for i in tied))[:budget])` … `if V[i] > thr or (V[i] == thr and keys[i] <= cut): f[i] = True`.
16. **so the length and type controls can reach the 10% cap** — FOUND: `def cap_alarm` docstring "lets the control reach the cap without exceeding it"; test `test_tied_control_reaches_cap`.
17. **In the regenerated dry run they catch 8 and 11** — FOUND in `docs/dryrun.json`: `"length": { "threshold": 384.0, "caught": 8, ... }` and `"type": { "threshold": 0.119, "caught": 11, ... }`.
18. **where before both caught 0** — NOT FOUND (no pre-change state in the diff; all files are `new file mode` additions).
19. **It is used in `evaluate`** — FOUND: `f = cap_alarm(V, y, CAP, seed=0)` in `def evaluate`.
20. **`boot_diff`** — FOUND transitively: `boot_diff` calls `recall_at_cap(...)`, which calls `f = cap_alarm(V, y, CAP, seed=seed)`; `cap_alarm` is not called directly in `boot_diff`.
21. **and the equal-false-alarm count** — FOUND: `out['S_equal_fpr_monitorable_caught'] = {m: sum(1 for f, yy in zip(cap_alarm([vv[i] for i in mon_idx], mony, CAP, seed=0), mony) if f and yy == 1) ...}`.
22. **The baselines are no longer handicapped to zero** — FOUND: `test_tied_control_reaches_cap` comment "they catch 0 when more than the cap fraction of the correct tie … cap_alarm splits that tie, so the control reaches the cap"; dryrun.json length/type caught 8/11.
23. **`PREREGISTRATION.md` and `recordings.py` now say that no seed is fresh across the program** — FOUND: PREREGISTRATION "None is fresh across the chip program"; recordings.py "none is fresh across the chip program".
24. **27–38 were YB-0051 test seeds** — FOUND: PREREGISTRATION "YB-0051 (27-38)"; recordings.py `HOME.update({s: 'YB-0051-low-false-alarm-precision' for s in range(27, 39)})`.
25. **"Fresh" means held out from this experiment's model selection** — FOUND: PREREGISTRATION "so "fresh" here means *held out from YB-0055's own model selection*"; recordings.py ""fresh" here means held out from YB-0055's model selection".
26. **and the run is corroboration** — FOUND: PREREGISTRATION "this run is *corroboration* of the YB-0051 result on the same held-out seeds, not a fresh confirmation".
27. **The pre-registration no longer states "about 43 / 500 / 0.2" as numbers** — NOT FOUND as a removal (diff shows only additions); confirmed *absent* in current PREREGISTRATION.md (no `43`, no `500`; `0.2` appears only as "order 0.2" in Power, a different quantity).
28. **It records that `inspect_seeds.py` was run once as a descriptive look at labels, with no model fitted or score computed** — FOUND: PREREGISTRATION "Before this record, `tests/inspect_seeds.py` was run once for a *descriptive* look … it fits no model, computes no score"; `inspect_seeds.py` "no model, no score, no threshold" and its body calls only `load_seed` + `print`.
29. **The power claim now reads "not recorded in the analysed fields"** — FOUND: analysis.py `power='not recorded in the analysed fields; not testable here (a descriptive check, not this result)'`; dryrun.json `"power": "not recorded in the analysed fields; not testable here (a descriptive check, not this result)"`.
30. **not "null in every recording"** — NOT FOUND (before-state; the old wording is not in the diff).
31. **Only the seeds I inspected showed null** — NOT FOUND (process claim, not in the diff).
32. **README no longer says "pre-registered"; it says not yet timestamped** — FOUND for the "not yet timestamped" half: "code and pre-registration written, NOT yet timestamped and not run on the test seeds"; the "no longer says pre-registered" half is NOT FOUND as a removal, but the current README uses "pre-registration written" / "pre-registration", not "pre-registered".
33. **`docs/dryrun.json` is regenerated** — FOUND: `dry()` does `json.dump(dict(res, dry_run=True), open(..., 'docs/dryrun.json'), 'w')`; dryrun.json `"dry_run": true`.
34. **It shows the pipeline runs, not that the regulator works** — FOUND (judgment): dryrun.json is computed from synthetic data (`res = analyse(V.synth(1500, 1) + V.synth(1500, 3), {'primary': V.synth(600, 2)}, boots=200)`).
35. **`scripts/timestamp_prereg.sh` needs network, which I don't have** — FOUND: PREREGISTRATION "Timestamp with `scripts/timestamp_prereg.sh …` (needs network + a `.venv/ots`; not run from this agent)." (The script file itself is not in the diff.)
36. **That step stays local, before `--run`** — FOUND: PREREGISTRATION "commit the proofs before running `python3 agr/bench/tier0_vitals.py --run`".
37. **"Follows YB-0035 corrected.py."** — FOUND: vitals_tier0.py docstring "Statistics follow YB-0035 corrected.py (in-time max, 10 percent cap, threshold-resampling bootstrap)".
38. **I haven't added a comparison test, because that file is skip-worktree** — NOT FOUND as positive evidence; confirmed by absence (test_core.py contains no YB-0035 comparison test); "skip-worktree" is not in the diff.
39. **The tie-aware cap is a documented departure from it** — FOUND: vitals_tier0.py docstring "the 10 percent cap is tie-aware: cap_alarm splits the tie at the threshold by a per-episode draw so a control whose score takes few distinct values (length, question type) is not forced to zero catches".
40. **The 'acceptance.log shows a pass' claim. That was the launcher's log of the earlier tree, which called an undefined `project`. It was stale** — NOT FOUND (acceptance.log is not in the diff).
41. **Commit 1: Makefile with test and experiment targets** — FOUND: Makefile `test:` and `experiment:` targets.
42. **so CI's make verify reaches it** — NOT FOUND: the Makefile defines `.PHONY: all test experiment smoke clean` and `all: test experiment`, but no `verify` target appears in the diff.
43. **plain-python test runner (CI has no pytest)** — FOUND: Makefile "run the unit tests with plain python3 (CI installs no pytest)" and "smoke: … needs pytest … not run in CI"; `tests/run_plain.py` "so CI needs no pytest".
44. **Commit 2: project() at the load boundary** — FOUND: `def project(r)` + recordings.py `project(...)` in `load_seed`.
45. **tie-aware 10 percent cap** — FOUND: `def cap_alarm` tie-splitting (line 15 evidence).
46. **unit tests inside the smoke** — FOUND: smoke `assert pytest.main([... tp]) == 0`.
47. **honest status** — FOUND (judgment): README "**Status:** … NOT yet timestamped and not run on the test seeds"; PREREGISTRATION "**Status:** … no test seed has been *scored*".
48. **Commit 3: work left uncommitted by the agent, committed by the launcher** — NOT FOUND in the diff (it is a commit message, self-referential).
49. **Commit 4: tier-0 vitals regulator** — FOUND: `agr/bench/tier0_vitals.py`, `src/vitals_tier0.py`.
50. **pre-registration** — FOUND: `docs/PREREGISTRATION.md`.
51. **dry run** — FOUND: `docs/dryrun.json` + `def dry()`.
52. **smoke test** — FOUND: `def smoke()`.

## Numbers

1. **33** (observer tests) — NOT FOUND (observer/tests not in this diff).
2. **10** (experiment tests) — recorded by counting the 10 `def test_` functions in `tests/test_core.py`; not a literal in the diff.
3. **f1654cb** — NOT FOUND.
4. **160** (`synth(160, 1)`, `synth(160, 2)`) — recorded as the smoke episode count: `R = V.synth(160, 1)` and `analyse(R, {'smoke_test': V.synth(160, 2)}, ...)`.
5. **40** (`boots=40`) — recorded: `res = analyse(R, {'smoke_test': V.synth(160, 2)}, boots=40, ...)`.
6. **1500 / 1500** (`synth(1500, 1) + V.synth(1500, 3)`) — recorded in `def dry()`: `res = analyse(V.synth(1500, 1) + V.synth(1500, 3), ...)`.
7. **600** (`synth(600, 2)`; dryrun.json `tests.primary.answered: 600`) — computed by `answered=len(A)` from `synth(600, 2)`, recorded in dryrun.json.
8. **200** (`boots=200` in `dry()`) — recorded: `..., boots=200)`.
9. **1000 / 1,000** (resamples; `run()` `boots=1000`; PREREGISTRATION "1,000 resamples") — recorded: `def analyse(deriv, tests, boots=1000, ...)` and `res = analyse(deriv, tests, boots=1000)`.
10. **0.005 / 0.005 s** (cost) — recorded: `CAP, COST = 0.10, 0.005`; used as `cost(r, t)` / `lambda r, t: COST`; PREREGISTRATION "elapsed(t) + 0.005 s".
11. **0.10 / 10 percent** (cap) — recorded: `CAP, COST = 0.10, 0.005`; tests `0.10 * n`, `0.10 * nc`; PREREGISTRATION "10 percent".
12. **48, 96, 192, 384** (checkpoints `T`) — recorded: `T = (48, 96, 192, 384)`; PREREGISTRATION "at checkpoint t in 48, 96, 192, 384".
13. **16** ("last 16 tokens") — recorded: `rec = dec[-16:]`; PREREGISTRATION "recent (last 16 tokens)".
14. **1.5** (stall threshold) — recorded: `stall_frac=sum(1 for v in dec if v > 1.5 * med) / n`; PREREGISTRATION "slower than 1.5 times the median".
15. **5 / 5-fold** (FOLDS) — recorded: `FOLDS = 5`; PREREGISTRATION "5-fold episode-grouped".
16. **1, 10, 100** (ridge strengths) — recorded: `LAMS = (1.0, 10.0, 100.0)`; PREREGISTRATION "Ridge strength chosen from 1, 10, 100".
17. **2 to 14 / 2-14** (derivation seeds) — recorded: `DERIV = tuple(range(2, 15))`; `HOME` entries for 2,3,4,8,5-14; PREREGISTRATION "seeds 2 to 14".
18. **38** (primary seed) — recorded: `PRIMARY = 38`; `HOME.update({s: 'YB-0051-low-false-alarm-precision' for s in range(27, 39)})` (38 ∈ range(27,39)); PREREGISTRATION "Primary test: seed 38".
19. **27 to 37 / 27-37** (secondary) — recorded: `SECONDARY = tuple(range(27, 38))` (27..37); PREREGISTRATION "seeds 27 to 37".
20. **2 to 38 / 27-38** (corpus / YB-0051) — recorded: `HOME` covers 2..38; PREREGISTRATION "YB-0051 (27-38)", "seeds 2 to 38".
21. **YB-0033** (PREREGISTRATION "recordings of YB-0033 to YB-0045") — NOT FOUND in the seed-to-directory map: `recordings.HOME` maps 2,3,4,8 → `YB-0042` and 5-14 → `YB-0045`; no `YB-0033` entry appears.
22. **YB-0042 / YB-0045 / YB-0050 / YB-0051** (directories) — recorded: `HOME = {s: 'YB-0042-probe-baseline' for s in (2,3,4,8)}`, `YB-0045-powered-replication` for 5,6,7,9,10,11,12,13,14, `YB-0050-powered-decider` for `range(15, 27)`, `YB-0051-low-false-alarm-precision` for `range(27, 39)`.
23. **10.0 / 0.9998 / 1.0** (`lam_cv_auroc`) — recorded in dryrun.json `"lam_cv_auroc": {"1.0": 1.0, "10.0": 1.0, "100.0": 0.9998}`, computed by `lam_cv_auroc={str(l): round(v[1], 4) ...}` from `cv_oof` auroc.
24. **1.0** (chosen `lam`) — recorded dryrun.json `"lam": 1.0`, computed `lam = max(LAMS, key=lambda l: (cvs[l][1], -l))`.
25. **3000** (`derivation_answered`) — recorded dryrun.json, computed `derivation_answered=len(Rd)`.
26. **8203** (`derivation_rows`) — recorded dryrun.json, computed `derivation_rows=len(jobs)`.
27. **346** (`derivation_wrong`) — recorded dryrun.json, computed `derivation_wrong=sum(wrong_of(r) for r in Rd)`.
28. **weights_full** (0.0, 4.818, -0.1369, -0.0833, -0.0069, -2.3155, 1.0329, 3.1459, -6.7028, -6.7637, -7.4972, -8.6572) — recorded dryrun.json, computed `weights_full=dict(zip(list(GROUPS['full']) + ['int%d' % t for t in T], [round(w, 4) for w in models['full'].w]))`.
29. **93** (`tests.primary.wrong`) — recorded dryrun.json, computed `wrong=sum(y)`; also `monitors.*.wrong: 93`.
30. **561** (`monitorable`) — recorded dryrun.json, computed `monitorable=sum(mon)`.
31. **32** (`short_correct_included`) — recorded dryrun.json, computed `short_correct_included=sum(1 for m, yy in zip(mon, y) if not m and yy == 0)`.
32. **86** (`monitors.full/level/shape.caught`, `S_full_minus_*`, `S_equal_fpr … full/level/shape`, `S_frozen … caught`) — recorded dryrun.json, computed via `evaluate`/`boot_diff`/`cap_alarm`.
33. **-5.6122 / -5.6357 / -2.1595** (monitors thresholds) — recorded dryrun.json, computed `thr = cap_threshold(...)` in `evaluate`.
34. **0.9247 / 0.0986 / 0.1053 / 1.0** (full monitor recall/fpr/fpr_monitorable/recall_monitorable) — recorded dryrun.json, computed in `evaluate`.
35. **384.0, 8, 0.086, 0.093** (length monitor threshold/caught/recall/recall_monitorable) — recorded dryrun.json, computed in `evaluate` (length baseline `in_time(A, lambda r, t: float(t), ...)`); the **8** is the "8" in claim 17.
36. **0.119, 11, 0.1183, 0.1279** (type monitor threshold/caught/recall/recall_monitorable) — recorded dryrun.json, computed in `evaluate` (type baseline `in_time(A, lambda r, t: rate.get(r['cat'], 0.0), ...)`); the **11** is the "11" in claim 17.
37. **0.8387, 0.7632, 0.9135** (`H_vitals_minus_length`) — recorded dryrun.json, computed `boot_diff(V['full'], V['length'], y, boots)`.
38. **0.8065, 0.75, 0.9** (`H_vitals_minus_type`) — recorded dryrun.json, computed `boot_diff(V['full'], V['type'], y, boots)`.
39. **true** (`H_supported`) — recorded dryrun.json, computed `out['H_supported'] = bool(out['H_vitals_minus_length'][1] > 0 and out['H_vitals_minus_type'][1] > 0)`.
40. **0.0, 0.0, 0.0** (`S_full_minus_level`, `S_full_minus_shape`) — recorded dryrun.json, computed `boot_diff(V['full'], V['level'/'shape'], y, boots)`.
41. **9, 12** (`S_equal_fpr_monitorable_caught` length/type) — recorded dryrun.json, computed `out['S_equal_fpr_monitorable_caught'] = {... cap_alarm([vv[i] for i in mon_idx], mony, CAP, seed=0) ...}`.
42. **-5.607557229734349, 86, 0.0986** (`S_frozen_derivation_threshold`) — recorded dryrun.json, computed `out['S_frozen_derivation_threshold'] = dict(threshold=frozen, caught=..., fpr=...)`.
43. **561, 86 / 509, 81 / 395, 59 / 176, 24** (per-checkpoint episodes/wrong) — recorded dryrun.json `S_per_checkpoint_auroc`, computed in the `for t in T:` loop `pc[str(t)] = dict(episodes=len(idx), wrong=sum(yt), ...)`.
44. **vitals [1.0,1.0,1.0]** and **type [0.489,0.42,0.5493] / [0.4948,0.4309,0.561] / [0.5295,0.4515,0.6058] / [0.5496,0.4271,0.6579]** (per-checkpoint AUROCs) — recorded dryrun.json, computed `auroc_with_ci=dict(vitals=boot_auc(...), type=boot_auc(...))`.
45. **true** (`dry_run`) — recorded dryrun.json, computed `json.dump(dict(res, dry_run=True), ...)`.
46. **"not recorded in the analysed fields; not testable here (a descriptive check, not this result)"** (`power` string) — recorded dryrun.json, computed `power='not recorded in the analysed fields; not testable here (a descriptive check, not this result)'`.
47. **43 / 500 / 0.2** (the old "about 43 / 500 / 0.2") — NOT FOUND in the diff; `0.2` appears only as "order 0.2" (PREREGISTRATION Power), a different quantity.
48. **1e-9 / 1e-6 / 1e-4 / 1e-12** (tolerances) — recorded: `assert m['fpr'] <= V.CAP + 1e-9`, `+ 1e-6` in `fit_logistic`, `1e-4` floor in `features`, `+ 1e-12` in `cap_threshold`/`cap_alarm`.
49. **12 / 30 / 100 / 32** (numeric literals in `fit_logistic`/`boot_diff`: `iters=12`, `max(-30.0, min(30.0, z))`, `g.getrandbits(32)`, `randrange(N)`) — recorded as code constants: `def fit_logistic(X, y, lam, iters=12)`, `math.exp(-max(-30.0, min(30.0, z)))`, `s = g.getrandbits(32)`.
50. **0.0 / 1.0 / 5.0** (synth/test literals: `nt = fs + 20`, `[0.15] + ...`, `[5.0] * 100`, `0.5` in `test_auroc_known`, `0.7` threshold in `test_logistic_learns_signal`) — recorded as literals: `V.auroc([0, 1], [0.5, 0.5]) == 0.5`, `assert a > 0.7`, `b = V.features(r['latency'][:48] + [5.0] * 100, 48)`, `lat = [0.15] + [base * math.exp(...)]`.
51. **0.025 / 0.975 / 0.025 / 0.975** (CI quantiles) — recorded: `q(0.025)`, `q(0.975)` in `boot_diff`; `a[int(0.025 * len(a))]`, `a[min(len(a) - 1, int(0.975 * len(a)))]` in `boot_auc`.
52. **20 / 3 / 2 / 0.12 / 0.15 / 0.04 / 1.15 / 0.05 / 20, 520** (synth parameters: `if len(idx) < 20`, `sum(yt) < 3`, `wrong_rate=0.12`, `g.random() < (0.12 ... else 0.04)`, `base = 0.011 * 1.15`, `g.gauss(0, 0.05 + 0.15)`, `fs = g.randrange(20, 520)`) — recorded as code literals in `synth`/`analyse`: `def synth(n, seed, wrong_rate=0.12)`, `if len(idx) < 20 or sum(yt) < 3: continue`.
53. **7, 20, 55, 100, 123 / 0, 1, 2, 17 / 8 / 90, 10 / 9** (`test_cap_alarm_respects_cap`, `test_tied_control_reaches_cap` counts) — recorded as test literals: `for n in (7, 20, 55, 100, 123)`, `for seed in (0, 1, 2, 17)`, `for seed in range(8)`, `y = [0] * 90 + [1] * 10`, `== 9`.
54. **0.1, 0.2, 0.3, 0.4, 0.5** (`test_auroc_known`) — recorded: `V.auroc([0, 0, 1, 1], [0.1, 0.2, 0.3, 0.4]) == 1.0 and V.auroc([0, 1], [0.5, 0.5]) == 0.5`.
55. **48** (the "episodes finishing before t = 48 stay in" / `final_start>48`) — recorded: PREREGISTRATION "episodes finishing before t = 48 stay in"; inspect_seeds.py `sum(r['final_start'] > 48 for r in a)`.
56. **0.005 / 0.005 s** in PREREGISTRATION — recorded (same as 10).
57. **"order 0.2"** (Power half-width estimate) — NOT FOUND as a computed value; it is a hand estimate in PREREGISTRATION prose ("a 95 percent half-width of a recall difference is large (order 0.2)").
58. **YB-0018 / YB-0035 / YB-0055 / YB-0033 / YB-0042 / YB-0045 / YB-0050 / YB-0051 / issue #4** — recorded as cross-reference labels (PREREGISTRATION "the YB-0018 prior", "YB-0035 definitions", commit "(#4)"); YB-0033 specifically NOT FOUND in `recordings.HOME` (see 21).
59. **5.0 / 10.5 / 1.0 / 10.0** (`test_in_time_excludes_late_checks` check tuples) — recorded: `V.in_time_max([(5.0, 10.0, 1.0, 10.5)]) == -math.inf and V.in_time_max([(5.0, 1.0, 1.0, 10.5)]) == 5.0`.
60. **100000** (`off` seed offset) — recorded: `off = 100000 * seed` in `load_seed`; `idx=seed * 100000 + i` in `synth`.
