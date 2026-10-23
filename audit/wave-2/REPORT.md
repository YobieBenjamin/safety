# Wave report

Generated 2026-10-22 16:26 from `/Volumes/External_4TB/Safety Experiments/safety/.agents/wave-2`.

| issue | backend | outcome | acceptance | pull request | turns | est. cost | wall time | attempts |
|---|---|---|---|---|---|---|---|---|
| YB-0053 | cloud+local | done: 1 commit(s), 13 turns | pass | https://github.com/YobieBenjamin/safety/pull/8 | 13 | $0.50 | 2 min | 1 |
| YB-0055 | cloud+local | done: 1 commit(s), 41 turns | pass | https://github.com/YobieBenjamin/safety/pull/9 | 41 | $0.79 | 3 min | 1 |

Estimated API-equivalent spend for the wave: $1.29 (Claude Code's client-side estimate; a subscription is billed by its windows, not by this figure).

## YB-0053: the agent's last words

The analysis code is built and the acceptance command passes on the first run (41 tests, then the smoke run). `observer/bench/independence.json` does not exist yet. Nothing has been run on real recordings, so there is no result for the hypothesis.

- **What exists:** `observer/bench/independence.py` and `observer/tests/test_independence.py`, in commit 22e26c5 (Agent: wave 2, issue #2).
- **How it works:**
  - It reads a verdict table with one JSON line per input: `id`, `source`, `label`, and `scores` for `model_refusal`, `regulator`, `layer3` and `sentry`.
  - Only inputs scored by all four monitors enter the joint analysis, and it reports coverage per source.
  - It computes each monitor's miss rate and the pairwise failure correlation, with bootstrap intervals and thresholds re-set in every resample.
  - It computes the joint miss rate for every k-of-n over the four monitors (32 rows).
  - The comparison is at a matched false-alarm rate, so a quorum is not credited for the extra alarms of an any-of-n rule.
  - It is pure standard library; a real run goes through `agr/runguard.py`.
- **Pre-registered threshold:** it is in `PREREG` in the script. A quorum counts as materially below the best single monitor if its miss rate is at most 0.75 times that monitor's, and the upper 95% bound of the difference is below zero. The false-alarm budget is 10%.
- **Smoke check:** on synthetic data it separates independent failures (best quorum miss 0.083 against a best single of 0.350) from common-cause failures (0.350 against 0.413). This shows the machinery works, not what the monitors do.
- **Not done:** the verdict table has to be built on the M4 Max, then `python3 observer/bench/independence.py --table <file>` run to write `independence.json`.
- **Why no table:** I could not see the YB-0045 episode format. This worktree has no `algorithms/` directory on disk, though git tracks it, and a command to check why was denied. `observer/bench/` did not exist either, so no YB-0052 set was available.
- **Open question:** the YB-0045 episodes are model answers scored by vitals, while the YB-0052 inputs are typed requests scored by Layer 3. Few inputs may be scored by all four monitors, so check the coverage figures before reading the verdict. If overlap is thin, the table needs adapters that score one population with the other monitors.
- **No patches** are needed for the other repositories.

## YB-0055: the agent's last words

The code for YB-0055 is built and committed (3951ee0), and the acceptance command passes: 33 observer tests, then the smoke test. The pre-registered run has not happened, so there is no result and `docs/results.json` does not exist.

- **What I built:**
  - A regulator that sees only the per-token arrival latencies and the token count. It uses ridge logistic regression on 8 latency features at checkpoints 48/96/192/384, using only the prefix up to each checkpoint.
  - The real-time protocol and statistics follow YB-0035: in-time maximum score, a threshold giving 10 percent false alarms among correct answers, and a threshold-resampling bootstrap.
  - The length and question-type controls, plus `level` and `shape` ablations.
  - Everything is standard library, because the project venv has no numpy or sklearn.
- **Design:** derivation uses seeds 2–14, the YB-0033 to YB-0045 recordings. The primary test is seed 38, scored once; the hypothesis is supported only if vitals beat both length and question type with a 95% lower bound above 0 (`docs/PREREGISTRATION.md`). Seeds 27–37 pooled are a secondary powered check with the frozen model, and they cannot change the primary verdict.
- **Verification:** 7 unit tests of mine pass, and a synthetic dry run ran end to end (`docs/dryrun.json`). The smoke test checks that no feature reads past its checkpoint, that only the tier-0 fields are exposed, and that the 10 percent false-alarm cap holds.
- **Power is untestable:** board power is null in all recordings, so the YB-0018 prior (power contributes nothing) is neither confirmed nor contradicted. Cycles are not recorded, so wall time stands in for them, and bytes are treated as a function of token count.
- **Checkout quirk:** `algorithms/` is hidden by skip-worktree and sparse checkout. `src/recordings.py` reads recordings with `git show HEAD:<path>`, and I committed with `git add --sparse`. No config was changed.
- **Open questions:**
  - Seed 38 has about 43 wrong answers, so the primary CI half-width is roughly 0.2 and a small advantage may not resolve. The pooled secondary is the informative check.
  - Is "fresh seed" meant to be seed 38? Seeds 27–38 were tests for other monitors, but never for vitals-only.
- **Still to do locally:** run `scripts/timestamp_prereg.sh algorithms/YB-0055-chip-visible-vitals/docs/PREREGISTRATION.md` (it needs network), commit the proofs, then run `python3 agr/bench/tier0_vitals.py --run`. That writes `docs/results.json` and refuses to run twice.
- **Patches for other repos:** none.

