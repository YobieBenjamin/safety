## Review of `exp/yb-0055`: **revise**

Verifier: clean; model review on ?: 1 blocking, 9 warnings, 5 unsupported claim(s) of 11; estimated $0.42, 10 turns.

### Reviewer's summary

The code is sound as far as I could read it, and nothing was deleted or weakened. Three things need fixing or showing before it merges.
1. The pre-registration says the protocol is "YB-0035 definitions, unchanged", but the tie-splitting 10 percent cap is a new departure. The pre-registration does not describe it. The comparison file `corrected.py` is not in the checkout, so "follows corrected.py" cannot be checked.
2. The acceptance command never touches a real recording. It runs 33 observer tests unrelated to this diff, then a smoke on synthetic data with a planted signal, which cannot fail on the hypothesis. `results.json` does not exist; the brief says that run is local. The pre-registration is not timestamped.
3. Some claims are asserted without an artifact: board power "not recorded", "order 0.2", "tens of wrong answers", and bytes as "a function of token count". Seed 38 is not fresh (YB-0051 test seed); the text discloses this, but the brief's "fresh seed" is not met.
Question: was `inspect_seeds.py` run on seed 38? The pre-registration only says "may include".
I could not run anything in the checkout (shell access was denied), so I did not re-run `--dry` or open the recordings.

### Reviewer findings

- [block] unsupported_claim at `algorithms/YB-0055-chip-visible-vitals/docs/PREREGISTRATION.md:41`: The heading says 'Real-time protocol (YB-0035 definitions, unchanged)'. The code adds a tie-splitting 10 percent cap (`cap_alarm`, randomised per episode) that the pre-registration never describes, and the summary calls it a 'documented departure'. `vitals_tier0.py` line 5 says it follows YB-0035 `corrected.py`, but that file is not in the checkout (no `corrected.py` under algorithms/YB-0035*), so the claim cannot be checked. Fix: describe the tie rule in the pre-registration and drop 'unchanged'. Do this before timestamping, because the tie rule decides the baselines' recall.
- [warn] test_integrity at `agr/bench/tier0_vitals.py:58`: The brief's acceptance is `pytest observer/tests` plus the smoke. The 33 observer tests are not touched by this diff. The smoke runs only on `V.synth` data, where wrong answers are made 15 percent slower and noisier by construction. It never calls `load_seed` or the `git show` fallback on a real recording, and it does not check the hypothesis. Line 58 asserts `caught >= 0`, which cannot fail. Line 61 skips the unit tests silently if `tests/test_core.py` is missing. The summary's 'acceptance passes' therefore shows that the pipeline runs on synthetic data, not that the stated acceptance holds on recordings.
- [warn] test_integrity at `agr/bench/tier0_vitals.py:43`: Smoke check 1, `set(chip_view(R[0])) == set(CHIP_FIELDS)`, is true by construction, because `chip_view` builds its dict from `CHIP_FIELDS`. `analyse` never calls `chip_view`, so the check says nothing about the pipeline. The same holds for `tests/test_core.py` line 17. Check 3 (`project`) does test something, but only on a hand-made dict, not on the output of `load_seed`.
- [warn] unsupported_claim at `algorithms/YB-0055-chip-visible-vitals/docs/PREREGISTRATION.md:17`: The text says board power 'is not recorded in the analysed fields' and so 'cannot be tested here'. No artifact is committed that shows this: the `inspect_seeds.py` output is not saved, and `project` still carries `power` in `CHIP_FIELDS`. The brief says power is part of what is tested (the YB-0018 prior). If any recording has non-null power, a named signal was dropped without a test. The same claim appears in `docs/dryrun.json` line 25 and in `vitals_tier0.py` lines 9-10. Evidence: not found.
- [warn] unsupported_claim at `algorithms/YB-0055-chip-visible-vitals/docs/PREREGISTRATION.md:57`: The Power section keeps numbers with no artifact behind them: 'tens of wrong answers', a half-width 'of order 0.2', and 'an order of magnitude more wrong answers' for seeds 27-37. The summary says the numbers were removed. The agent saw the label counts through `inspect_seeds.py` but did not commit its output, so the statement cannot be checked. Either commit the counts as a descriptive artifact or delete the figures.
- [warn] unsupported_claim at `algorithms/YB-0055-chip-visible-vitals/src/vitals_tier0.py:9`: The brief's tier-0 set is token rate, latency, cycles, bytes and power. The code says bytes 'are a function of the token count at this tier' and that wall time stands in for cycles. Neither is shown. Bytes are not a function of token count in general. The result is a latency-only regulator under a broader label. State this narrowing in the verdict text.
- [warn] scope at `algorithms/YB-0055-chip-visible-vitals/docs/PREREGISTRATION.md:36`: The brief asks for a test 'once on a fresh seed'. Seed 38 is a YB-0051 test seed, so the result is already known to the program, and the pre-registration says the run is corroboration only. That is disclosed honestly, but the brief's condition is not met and the owner has to accept the substitution. Also, `inspect_seeds.py` (lines 12-13) prints wrong-answer counts for any seed passed, and the pre-registration (line 4) says only that this 'may include the test seeds', not whether it did.
- [warn] protocol at `algorithms/YB-0055-chip-visible-vitals/README.md:3`: The brief requires pre-registering with the timestamp script before the run. The proofs are not committed, and the README and `PREREGISTRATION.md` line 6 say so. `--run` will execute without proof of order. Timestamp the final pre-registration, after fixing the tie-rule wording, and commit the proofs before `--run`.
- [warn] correctness at `algorithms/YB-0055-chip-visible-vitals/docs/dryrun.json:89`: The committed dry run reports `H_supported: true`, per-checkpoint AUROC of 1.0 (lines 117-121) and identical recall for full, level and shape. That comes from the planted synthetic signal, and it sits in docs/ beside the future `results.json`. The only label is `dry_run: true`. The summary's note that it 'shows the pipeline runs, not that the regulator works' is fair but is not written in the file. The summary also says the length and type baselines caught 0 before the fix and 8 and 11 after. The baselines' catches of 8 and 11 match lines 247-262 of this file, but the earlier file is not in the diff, so the 'before' figure is not found.
- [warn] correctness at `algorithms/YB-0055-chip-visible-vitals/src/analysis.py:48`: The 'equal false alarm' counts re-run `cap_alarm` on the monitorable subset with a fixed seed 0. This is a different population and tie draw from the primary `evaluate` (line 45 uses all answered episodes). The two sets of figures are not directly comparable, and the pre-registration (lines 49-50) does not say so. Low risk, but it should be stated.

### Claims

- supported (summary): The tier-0 restriction is enforced in the pipeline: project() at load drops text, entropy, p_top1, margin, toks, final and truth. (evidence: vitals_tier0.py lines 30-36 and recordings.py line 33 apply project. The smoke (lines 54-56) and test_core.py::test_project_drops_content test it on hand-made dicts. The check on real data is not run in acceptance.)
- supported (summary): The acceptance command now passes: 33 observer tests, 10 experiment tests run from inside the smoke, smoke ok. (evidence: acceptance.log and verify.json (exit 0, '33 passed', '10 passed', smoke ok). test_core.py has 10 tests. It shows the pipeline runs on synthetic data only.)
- supported (summary): The tie-aware cap_alarm lets the length and type controls reach the 10 percent cap; the dry run catches 8 and 11 where before it caught 0. (evidence: test_tied_control (test_core.py line 41) shows the mechanism. dryrun.json lines 247 and 262 show 8 and 11. The earlier 'caught 0' file is not in the diff, so 'before' is not found.)
- NOT SUPPORTED (document): The protocol uses YB-0035 definitions, unchanged, and follows YB-0035 corrected.py. (evidence: The tie-splitting cap is a departure that the pre-registration does not describe. corrected.py is not in the checkout, so no comparison test or source is available.)
- NOT SUPPORTED (document): Board power is not recorded in the analysed fields, so it cannot be tested here. (evidence: Not found. No committed output from inspect_seeds.py or other artifact shows it. The agent says it saw null only in the seeds it inspected.)
- NOT SUPPORTED (document): Bytes are a function of the token count at this tier; wall time stands in for cycles. (evidence: Asserted in PREREGISTRATION.md line 16 and vitals_tier0.py lines 9-10 with no source or test.)
- NOT SUPPORTED (document): A single primary seed carries on the order of tens of wrong answers; the half-width is of order 0.2; the pooled seeds have an order of magnitude more. (evidence: Not found. No committed count. The dry-run bootstrap (synthetic, 93 wrong) gives intervals about 0.15 wide, which does not bear on seed 38.)
- supported (document): No seed is fresh across the program; seeds 27-38 are YB-0051 test seeds; seed 38 is held out from this experiment's model selection. (evidence: The map in recordings.py lines 17-20 and the derivation seeds 2-14 in tier0_vitals.py line 36 agree with it. The deviation from the brief's 'fresh seed' is disclosed.)
- NOT SUPPORTED (document): No test seed has been scored; inspect_seeds.py was a descriptive look at labels only. (evidence: No scoring path touches seeds above 14 outside --run, and no results.json exists. Whether inspect_seeds was run on seed 38 is not stated and its output is not committed.)
- supported (summary): docs/dryrun.json shows the pipeline runs, not that the regulator works. (evidence: Consistent with the synthetic planted signal in synth() (vitals_tier0.py lines 123-133, per its diff location) and AUROC 1.0 in the file. The caveat appears only in the summary and the README.)
- supported (code): The statistics (in-time max, 10 percent cap, threshold-resampling bootstrap) implement the pre-registered decision rule: H is supported iff both lower bounds exceed 0 on the primary seed. (evidence: analysis.py line 45 uses index [1], the lower bound, of both boot_diff outputs. boot_diff (vitals_tier0.py lines 120-126 of the new file) resamples and resets thresholds. There is no test of the bootstrap itself, only of the cap and AUROC functions.)

### suite in a clean checkout: exit 0

```
============================= test session starts ==============================
platform darwin -- Python 3.12.15, pytest-9.1.1, pluggy-1.7.0
rootdir: /private/var/folders/30/33qb062d34q5p1j5tycqcyww0000gn/T/verify-g9nhoqiw/observer
configfile: pyproject.toml
collected 33 items

observer/tests/test_contract.py .......                                  [ 21%]
observer/tests/test_signals.py ..........................                [100%]

============================== 33 passed in 0.04s ==============================

```

### acceptance in a clean checkout: exit 0

```
.................................                                        [100%]
33 passed in 0.03s
{"smoke": "ok", "vitals_caught": 20, "length_caught": 3, "wrong": 20, "fpr_full": 0.1}

```
