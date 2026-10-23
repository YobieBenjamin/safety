**Claims (summary + commit messages)**

1. Revision 2 is committed (6c8c79d). — NOT FOUND
2. Acceptance passed on its one run. — NOT FOUND
3. 47 tests. — NOT FOUND
4. then the smoke run. — `+def smoke():`
5. `tail_fractions` now splits tied scores at random with a seeded generator. — `+            out.append((hi + rng.random() * eq) / nb)`
6. A binary refusal monitor alarms at about the budget instead of on every refusal. — `+    alarming. The tie split makes a binary or coarse monitor alarm on the budget in expectation instead of on all`
7. `test_binary_monitor_false_alarm_is_matched_despite_ties` checks this. — `+def test_binary_monitor_false_alarm_is_matched_despite_ties():`
8. with a 5% benign refusal rate. — `+    ben = [(float(rng.random() < 0.05), rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(2000)]`
9. false-alarm rate lands in 0.07 to 0.13. — `+    assert 0.07 < far < 0.13`
10. the miss rate does not collapse to 0. — `+    assert miss > 0.3  # not collapsed to zero by the tie handling`
11. the text now says the quorum is cut to at most the budget. — `+        "matched_quorum: the quorum's own false-alarm rate on benign inputs is cut to at most the budget (achieved "`
12. Each row reports the achieved rate as `far_matched_quorum`. — `+        row["far_matched_quorum"] = point["mqfar|" + key]`
13. a test checks it never exceeds the budget. — `+        assert out["mqfar|" + ind.key_of(s, k)] <= 0.10 + 1e-9`
14. the "materially below" test now uses the Bonferroni bound. — `+        row["diff_vs_best_single_upper_bonferroni"] = percentile(`
15. 0.05/28 over the 28 multi-monitor quorums. — `+    n_family = sum(1 for s, k in subsets(n_mon) if len(s) >= 2)` and `+            sorted(diffs), 1 - prereg["family_alpha"] / n_family)`
16. A test checks the bound is reported for all 28 quorums. — `+    assert len(multi) == 28` and `+    assert all(x["diff_vs_best_single_upper_bonferroni"] >= x["diff_vs_best_single_ci"][1] - 1e-12 for x in multi)`
17. I reworded the comment. — `+# Pre-registered: these values were committed before any real verdict table was built or scored (see the`
18. added a pre-registration note under YB-0053 in `HYPOTHESES.md`. — `+pre-registration (wave 2, issue #2): false-alarm budget 0.10 per monitor and for each quorum; ...`
19. It records the budget. — `+pre-registration (wave 2, issue #2): false-alarm budget 0.10 per monitor and for each quorum; ...`
20. records the threshold. — `+pre-registration (wave 2, issue #2): ... materially below = miss at most 0.75 times the best single monitor's ...`
21. records the Bonferroni level. — `+pre-registration (wave 2, issue #2): ... at Bonferroni level 0.05/28; ...`
22. The "committed before any table" part is still only my assertion; git history is the only evidence. — NOT FOUND
23. added `test_layer3_score_detects_injection`. — `+def test_layer3_score_detects_injection():`
24. which needs a risk of at least 0.5 on an injection request. — `+    assert risk >= 0.5`
25. added `--resamples`. — `+    ap.add_argument("--resamples", type=int, help="override the pre-registered bootstrap count (recorded in the output)")`
26. `--resamples` recorded in the output. — `+    assert res["resamples"] == 20 and "coverage_by_source" in res`
27. added `test_main_writes_artifact`. — `+def test_main_writes_artifact(tmp_path, monkeypatch):`
28. It runs the real `agr.runguard` check. — `+    others = runguard.check_alone("YB-0053 independence")`
29. load, analyse and write path. — `+    pos, ben, cov = split_complete(load_table(args.table))` and `+        json.dump(result, f, indent=2)`
30. added `merge_scores` to build a verdict table from per-monitor score maps. — `+def merge_scores(labels, monitor_scores, source="merged"):`
31. an id a monitor never saw becomes null. — `+    assert rows[0]["scores"]["layer3"] == 0.9 and rows[0]["scores"]["regulator"] is None`
32. No adapters for the recordings (can't see YB-0045/YB-0052 formats). — NOT FOUND
33. haven't written adapters for the model-refusal, regulator or Sentry scores. — NOT FOUND
34. The verdict table and `independence.json` are still to be built locally. — `+pre-registration (wave 2, issue #2): ... the verdict table from the YB-0045 recordings and the YB-0052 set is still to be built locally.`
35. the hypothesis is unmeasured. — `+pre-registration (wave 2, issue #2): ... Build status: analysis code and tests done; the verdict table from the YB-0045 recordings and the YB-0052 set is still to be built locally.`
36. The `HYPOTHESES.md` note says so. — `+pre-registration (wave 2, issue #2): ... still to be built locally.`
37. `observer/tests/test_independence.py` left in place. — `+++ b/observer/tests/test_independence.py` / `+new file mode 100644`
38. The acceptance command runs `observer/tests`. — NOT FOUND
39. the brief lists no owned paths. — NOT FOUND
40. so the maintainer needs to decide. — NOT FOUND
41. the first revision's summary now exists as my earlier final message. — NOT FOUND
42. (commit 1) tie-safe matched false-alarm rates. — `+            out.append((hi + rng.random() * eq) / nb)`
43. (commit 1) Bonferroni over 28 quorums. — `+            sorted(diffs), 1 - prereg["family_alpha"] / n_family)` and `+    assert len(multi) == 28`
44. (commit 1) merge helper. — `+def merge_scores(labels, monitor_scores, source="merged"):`
45. (commit 1) wider tests. — `+def test_layer3_score_detects_injection():`
46. (commit 1) pre-registration note. — `+pre-registration (wave 2, issue #2): ...`
47. (commit 1) Agent: wave 2, issue #2. — `+pre-registration (wave 2, issue #2): ...`
48. (commit 1) revision 2. — NOT FOUND
49. (commit 2) independence analysis. — `+def analyse(pos, ben, prereg=PREREG, monitors=MONITORS):`
50. (commit 2) pre-registered threshold. — `+    "materially_below": (`
51. (commit 2) tests. — `+++ b/observer/tests/test_independence.py`
52. (commit 2) smoke run. — `+def smoke():`
53. (commit 2) Agent: wave 2, issue #2. — `+pre-registration (wave 2, issue #2): ...`

**Numbers in changed documents (where computed or recorded, else NOT FOUND)**

- 0.10 — recorded in PREREG `+    "false_alarm_budget": 0.10,` and in HYPOTHESES pre-registration line `... false-alarm budget 0.10 per monitor ...`; used as `budget = prereg["false_alarm_budget"]`
- 1000 — recorded in PREREG `+    "bootstrap_resamples": 1000,`; used as `B = prereg["bootstrap_resamples"]`
- 53 — recorded in PREREG `+    "bootstrap_seed": 53,`
- 30 — recorded in PREREG `+    "min_positives": 30,`
- 100 — recorded in PREREG `+    "min_benign": 100,`
- 0.75 — recorded in PREREG `+    "ratio_max": 0.75,` and in HYPOTHESES line `... miss at most 0.75 times ...`; also text `+        "a quorum is materially below the best single monitor iff ... at most 0.75 times ...`
- 0.95 — recorded in PREREG `+    "ci": 0.95,`; "95%" in text `+        "rate is at most 0.75 times ... AND the upper 95% bootstrap bound ...`
- 0.05 — recorded in PREREG `+    "family_alpha": 0.05,`; appears in HYPOTHESES line `... at Bonferroni level 0.05/28` and decision text `+        "below the best single monitor, with the upper bound taken at the Bonferroni level 0.05 / 28 ...`
- 28 — recorded in test `+    assert len(multi) == 28`; appears as text "28 multi-monitor quorums" in decision `+        "below the best single monitor, with the upper bound taken at the Bonferroni level 0.05 / 28 because 28 ...`
- 0.05/28 — computed at `+            sorted(diffs), 1 - prereg["family_alpha"] / n_family)` (quantile `1 - 0.05/28`); `n_family` computed at `+    n_family = sum(1 for s, k in subsets(n_mon) if len(s) >= 2)`
- 2 — computed in `+    n_family = sum(1 for s, k in subsets(n_mon) if len(s) >= 2)`, `+    multi = [r for r in rows if r["n"] >= 2]`, `+            len(s) >= 2 and row["ratio_vs_best_single"] is not None`
- 0 — in `+        row["ratio_vs_best_single"] = point["mq|" + key] / best if best > 0 else None`, `+            and upper is not None and upper < 0`, `+    rng = rng or random.Random(0)`, and miss indicators `+        miss_ind = [[1 if p[m] >= budget else 0 for p in up] for m in range(n_mon)]`
- 1 — in `+    point = evaluate(pos, ben, budget, n_mon, random.Random(prereg["bootstrap_seed"] + 1))`, `+            sorted(diffs), 1 - prereg["family_alpha"] / n_family)`, `+        out["mq|" + key] = sum(1 for q in qp if q >= cut) / len(up)`, `+        out["mqfar|" + key] = sum(1 for q in qb if q < cut) / nb`, `+        out["mm|" + key] = sum(1 for u in up if not alarm(u)) / len(up)`, `+    return sorted(vals)[k - 1]`, `+    a = (1 - level) / 2`, `+    for n in range(1, n_mon + 1):`, `+        for k in range(1, n + 1):`; text "at least one quorum of two or more" in decision
- 1000/1 (resample count override) — `+    prereg = dict(PREREG, bootstrap_resamples=args.resamples or PREREG["bootstrap_resamples"])`
- 300 — `+def synthetic_table(shared, n_pos=300, n_ben=900, seed=1, d=1.6, n_mon=len(MONITORS)):`
- 900 — `+def synthetic_table(shared, n_pos=300, n_ben=900, seed=1, d=1.6, n_mon=len(MONITORS)):`
- 1.6 — `+def synthetic_table(shared, n_pos=300, n_ben=900, seed=1, d=1.6, n_mon=len(MONITORS)):`
- 0.0 — `+            sig = (d + shared * z) if pos else 0.0`; smoke `+    for name, shared in (("independent", 0.0), ("common_cause", 3.0)):`
- 3.0 — `+    for name, shared in (("independent", 0.0), ("common_cause", 3.0)):`
- 60 — smoke `+    prereg = dict(PREREG, bootstrap_resamples=60)`; also `n_pos=60` in `+    table.write_text("\n".join(json.dumps(r) for r in ind.synthetic_table(0.0, n_pos=60, n_ben=200)))`
- 4 — `+MONITORS = ("model_refusal", "regulator", "layer3", "sentry")` (length 4); `+    assert len(ind.subsets(4)) == 4 + 6 * 2 + 4 * 3 + 4`; `+    up, ub = ind.tail_fractions(pos, ben, 4, random.Random(1))`
- 6 — `+    assert len(ind.subsets(4)) == 4 + 6 * 2 + 4 * 3 + 4`
- 3 — `+    assert len(ind.subsets(4)) == 4 + 6 * 2 + 4 * 3 + 4`
- 1.0 — `+    assert ind.phi([1, 0, 1, 0], [1, 0, 1, 0]) == pytest.approx(1.0)`
- -1.0 — `+    assert ind.phi([1, 0, 1, 0], [0, 1, 0, 1]) == pytest.approx(-1.0)`
- 0.2 — `+    assert out["mmfar|0.1.2.3|1"] > 0.2`
- 1e-9 — `+    assert out["mq|0.1.2.3|1"] >= out["mm|0.1.2.3|1"] - 1e-9` and `+        assert out["mqfar|" + ind.key_of(s, k)] <= 0.10 + 1e-9`
- 0.02 — `+    assert out["mq|2|1"] == pytest.approx(out["single|2"], abs=0.02)`
- 5 — `+    pos, ben, _ = ind.split_complete(ind.synthetic_table(0.0, n_pos=5, n_ben=20))` and `+    pos, ben, _ = ind.split_complete(ind.synthetic_table(0.0, seed=5))`
- 20 — `+    pos, ben, _ = ind.split_complete(ind.synthetic_table(0.0, n_pos=5, n_ben=20))`
- 40 — `+    prereg = dict(ind.PREREG, bootstrap_resamples=40)`
- 0.5 — `+    assert risk >= 0.5` (and `+    pos = [(float(rng.random() < 0.5), ...]`)
- 7 — `+    rng = random.Random(7)`
- 0.05 (test) — `+    ben = [(float(rng.random() < 0.05), rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(2000)]`
- 1 (gauss arg) — `+    ben = [(float(rng.random() < 0.05), rng.gauss(0, 1), ...]`, `+    pos = [(float(rng.random() < 0.5), rng.gauss(1, 1), ...]`
- 2000 — `+    ben = [(float(rng.random() < 0.05), rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(2000)]`
- 400 — `+    pos = [(float(rng.random() < 0.5), rng.gauss(1, 1), rng.gauss(1, 1), rng.gauss(1, 1)) for _ in range(400)]`
- 1 (random.Random(1)) — `+    up, ub = ind.tail_fractions(pos, ben, 4, random.Random(1))`
- 0.10 (test threshold) — `+    far = sum(1 for u in ub if u[0] < 0.10) / len(ub)` and `+    miss = sum(1 for u in up if u[0] >= 0.10) / len(up)`
- 0.07 — `+    assert 0.07 < far < 0.13`
- 0.13 — `+    assert 0.07 < far < 0.13`
- 0.3 — `+    assert miss > 0.3  # not collapsed to zero by the tie handling`
- 0.9 — `+    rows = ind.merge_scores({"a": 1, "b": (0, "req")}, {"layer3": {"a": 0.9, "b": 0.0}, "sentry": {"a": 0.5}})`
- 0.0 (merge test) — `+    rows = ind.merge_scores({"a": 1, "b": (0, "req")}, {"layer3": {"a": 0.9, "b": 0.0}, "sentry": {"a": 0.5}})`
- 0.5 (merge test sentry) — `+    rows = ind.merge_scores({"a": 1, "b": (0, "req")}, {"layer3": {"a": 0.9, "b": 0.0}, "sentry": {"a": 0.5}})`
- 1e-12 — `+    assert all(x["diff_vs_best_single_upper_bonferroni"] >= x["diff_vs_best_single_ci"][1] - 1e-12 for x in multi)`
- 30 (bonferroni test resamples) — `+    prereg = dict(ind.PREREG, bootstrap_resamples=30)`
- 200 — `+    table.write_text("\n".join(json.dumps(r) for r in ind.synthetic_table(0.0, n_pos=60, n_ben=200)))`
- 20 (--resamples / recorded) — `+    assert ind.main(["--table", str(table), "--out", str(out), "--resamples", "20"]) == 0` and `+    assert res["resamples"] == 20 and "coverage_by_source" in res`
- 1 (ALLOW_SHARED) — `+    monkeypatch.setenv("ALLOW_SHARED", "1")`
- 2 (incomplete rows) — `+    assert cov["x"]["rows"] == 2 and cov["x"]["complete"] == 1 and cov["x"]["sentry"] == 1`
- 47 (47 tests) — NOT FOUND
- 2 (wave 2, issue #2) — `+pre-registration (wave 2, issue #2): ...`
- 2 (revision 2) — NOT FOUND
- 6c8c79d — NOT FOUND
