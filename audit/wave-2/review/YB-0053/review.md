## Review of `exp/yb-0053`: **revise**

Verifier: 1 blocking finding(s); model review on ?: 0 blocking, 8 warnings, 2 unsupported claim(s) of 15; estimated $0.29, 7 turns.

### Reviewer's summary

The analysis code is sound and its tests are real. The measurement the brief asks for does not exist yet.
- No adapters for the YB-0045 recordings or the YB-0052 set, and no independence.json. The acceptance command runs only synthetic data, so the hypothesis is unmeasured. The agent says so, and that is honest.
- The pre-registered rule contradicts itself: PREREG says "upper 95% bootstrap bound", while the code and the decision text use Bonferroni 0.05/28.
- "Committed before any table was built" rests on git history alone. Both revisions of PREREG changed after the first draft, though only synthetic data had been seen.
- test_main_writes_artifact sets ALLOW_SHARED=1, so it does not exercise the run-alone guard.
- verify.json blocks on observer/tests/test_independence.py as outside the owned paths. The acceptance command itself runs observer/tests, so I rate this a warn. The maintainer should confirm the owned paths.
- Question: does the Bonferroni quantile 1-0.05/28 give a stable bound at B=1000? It rests on about two resamples in the tail.

### Verifier findings

- [block] a file outside the issue's owned paths changed: `observer/tests/test_independence.py`

### Reviewer findings

- [warn] correctness at `observer/bench/independence.py:41`: The pre-registered rule text in PREREG['materially_below'] says the test uses 'the upper 95% bootstrap bound' (ci=0.95). The code (line ~252) and the 'decision' text (line ~55) use the Bonferroni bound at 1-0.05/28. The rule that was supposedly registered is therefore stated two ways. Make PREREG say only what the code does.
- [warn] correctness at `observer/bench/independence.py:252`: The Bonferroni upper bound is the 1-0.05/28 (about 0.998) quantile of the bootstrap differences. With bootstrap_resamples=1000 that is set by about two resamples in the tail, and by the single maximum at the smoke count of 60. The bound is very noisy, and no test or pre-registered justification covers its resolution. The best single monitor is also fixed on the same point estimate (line ~228), and the best quorum is picked by min over 28 on the same data (line ~261), with no correction on the reported 'best_quorum' miss.
- [warn] unsupported_claim at `observer/bench/independence.py:30`: The comment 'these values were committed before any real verdict table was built or scored' is not shown by any artifact. It is vacuously true (no table exists), and the only evidence is git history. The HYPOTHESES.md note is itself in the same pull request as the code and was added in the revision commit, after PREREG had already changed once. Reword it as 'fixed before any real table exists' or remove it.
- [warn] unsupported_claim at `HYPOTHESES.md:287`: The note says the full rule is PREREG 'committed before any verdict table was built'. The same applies as above: not shown beyond the commit order. 'Analysis code and tests done' is supported by acceptance.log lines 1-2. 'Still to be built locally' is consistent with the diff (no table, no adapters, no independence.json).
- [warn] test_integrity at `observer/tests/test_independence.py:101`: test_main_writes_artifact sets ALLOW_SHARED=1, which makes runguard.check_alone skip its refusal (agr/runguard.py:23). The summary's claim that it 'runs the real agr.runguard check' is overstated: the guard's refusal path is bypassed and untested. The load, analyse and write path is exercised.
- [warn] test_integrity at `observer/bench/independence.py:299`: The acceptance command (pytest observer/tests, then --smoke) exercises only the synthetic one-factor generator. It shows the pipeline separates a shared-factor regime from an independent one. It does not touch YB-0045's episodes or the YB-0052 set, and it writes no observer/bench/independence.json, which the brief names as the artifact. The command passes by testing less than the hypothesis needs, though the brief says the run itself is local.
- [warn] correctness at `observer/bench/independence.py:3`: Nothing builds a verdict table from real monitors. There is no adapter for model refusal, regulator or Sentry scores, and layer3_score is the only per-monitor producer. The tie handling for a binary refusal monitor (line ~133, random split) credits random alarms on non-refusals to match the budget. That is sound as randomisation, but it is only tested on synthetic binary data.
- [warn] scope at `observer/tests/test_independence.py:1`: verify.json flags this new file as outside the issue's owned paths. The acceptance command runs observer/tests and the file is new, so no existing test was weakened. The maintainer must decide whether tests there are in scope.

### Claims

- supported (summary): Revision 2 is committed (6c8c79d); acceptance passed, 47 tests then the smoke run (evidence: acceptance.log lines 1-5 show '47 passed' and 'smoke ok'; verify.json head 6c8c79d, acceptance exit 0)
- supported (summary): tail_fractions splits tied scores at random with a seeded generator, so a binary refusal monitor alarms at about the budget (evidence: independence.py tail_fractions (rng.random()*eq); test_binary_monitor_false_alarm_is_matched_despite_ties asserts far in (0.07,0.13) and miss>0.3)
- supported (code): The quorum is cut to at most the budget; far_matched_quorum is reported; a test checks it never exceeds the budget (evidence: evaluate(): cut=qb[m_budget], mqfar; test_matched_quorum_far_is_reported_and_within_budget asserts <=0.10+1e-9 for all subsets)
- supported (summary): The 'materially below' test uses the Bonferroni bound 0.05/28 over 28 multi-monitor quorums; a test checks it is reported for all 28 (evidence: analyse(): n_family and percentile(sorted(diffs),1-family_alpha/n_family); test_bonferroni_bound_is_reported asserts len(multi)==28)
- NOT SUPPORTED (code): PREREG states the rule as 'upper 95% bootstrap bound' for materially below (evidence: PREREG['materially_below'] says 95% while the code uses the Bonferroni quantile; the two disagree)
- NOT SUPPORTED (code): These values were committed before any real verdict table was built or scored (evidence: Only git history; the note was added in the revision commit. No real table exists, so the statement is vacuous)
- supported (document): Pre-registration note added under YB-0053 in HYPOTHESES.md, recording budget 0.10, threshold 0.75 and Bonferroni 0.05/28 (evidence: HYPOTHESES.md:287 and PREREG values false_alarm_budget=0.10, ratio_max=0.75, family_alpha=0.05)
- supported (document): The verdict table and independence.json are still to be built locally; the hypothesis is unmeasured (evidence: No independence.json or adapters in the diff; HYPOTHESES.md:287 says so)
- supported (code): Thresholds are re-set inside every bootstrap resample (evidence: evaluate() calls tail_fractions on each resample (analyse loop))
- supported (summary): Added test_layer3_score_detects_injection requiring risk >= 0.5 (evidence: test file defines it with 'assert risk >= 0.5'; it passes in the 47-test run)
- NOT SUPPORTED (summary): test_main_writes_artifact runs the real agr.runguard check, load, analyse and write path (evidence: The test sets ALLOW_SHARED=1, so check_alone returns without refusing; the refusal path is untested)
- supported (summary): --resamples added and recorded in the output (evidence: argparse option; prereg override stored in preregistration; the test asserts res['resamples']==20)
- supported (summary): merge_scores builds a verdict table from per-monitor score maps; an id a monitor never saw becomes null (evidence: merge_scores and test_merge_scores_builds_table_with_nulls)
- supported (code): The smoke run tells the independent and common-cause regimes apart (evidence: smoke() asserts and acceptance.log lines 3-4 (quorum_helps True vs False, phi -0.009 vs 0.738), on synthetic data only)
- NOT SUPPORTED (summary): The agent cannot see the YB-0045 or YB-0052 data formats, so no adapters were written (evidence: Not found in the diff or packet; the agent's own statement. The other repositories are readable per the brief)

### suite in a clean checkout: exit 0

```
============================= test session starts ==============================
platform darwin -- Python 3.12.15, pytest-9.1.1, pluggy-1.7.0
rootdir: /private/var/folders/30/33qb062d34q5p1j5tycqcyww0000gn/T/verify-0nor7gh7/observer
configfile: pyproject.toml
collected 47 items

observer/tests/test_contract.py .......                                  [ 14%]
observer/tests/test_independence.py ..............                       [ 44%]
observer/tests/test_signals.py ..........................                [100%]

============================== 47 passed in 1.93s ==============================

```

### acceptance in a clean checkout: exit 0

```
...............................................                          [100%]
47 passed in 1.92s
independent: best single model_refusal miss 0.350, best quorum 3-of-4 miss 0.083, mean phi -0.009, quorum_helps=True
common_cause: best single model_refusal miss 0.413, best quorum 2-of-4 miss 0.350, mean phi 0.738, quorum_helps=False
smoke ok

```
