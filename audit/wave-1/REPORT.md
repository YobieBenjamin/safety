# Wave report

Generated 2026-10-20 17:59 from `/Users/yb/safety/.agents/wave-1`.

| issue | backend | outcome | acceptance | pull request | turns | est. cost | wall time | attempts |
|---|---|---|---|---|---|---|---|---|
| YB-0052 | cloud | done: 1 commit(s), 15 turns | pass | https://github.com/YobieBenjamin/safety/pull/7 | 15 | $0.58 | 3 min | 1 |

Estimated API-equivalent spend for the wave: $0.58 (Claude Code's client-side estimate; a subscription is billed by its windows, not by this figure).

## YB-0052: the agent's last words

YB-0052 is built and committed (42f597f), and the acceptance command passes: 36 tests pass and `score.py --smoke` finishes. It ran twice, so one run is left. I did not run the full scoring, because the protocol says to pre-register first and score the test split once.

- **Set:** `observer/bench/set.jsonl` has 134 gate-typed rows, built by `build_set.py`. Six families have overt and disguised positives: exfiltration, weight_exfiltration, oversight_evasion, financial, hazard_content and credential_access. Negatives are 30 benign and 30 benign-but-alarming rows, plus the two README calibration rows (bare keyword under 0.25, benign transfer under 0.05). Hazard classes are abstract `<<HAZ:..>>` tokens. Rows are split into dev and test.
- **Scorer:** `score.py` runs `python -m safety_observer assess` on every row. It reports miss and false alarm per family, with 95% bootstrap intervals and thresholds re-set in each resample, for four signals: the observer's per-family strength, its overall risk, a length-only baseline and a keyword-count baseline. A second full run needs `--deviation REASON`.
- **Pre-registration:** `PREREG.md` fixes the decision rules, and `test_bench.py` adds shape checks on the set.
- **Smoke artifact:** `results.smoke.json` comes from 42 dev rows and 50 resamples. On those few rows the disguised miss rate is 0.67 to 1.0 in every family, but that is not evidence for or against the hypothesis. I have not generated `results.json`.

Open questions:
- The governor's `hazard_budget` is a count per session (`max: 1`), not a rate. I registered 0.10 per request as a stand-in; you should confirm or change it before the full run.
- Positives per family are small (about 12), so intervals will be wide. A family can only reach "below budget" with near-zero misses.
- I wrote the disguised rows after reading the observer's patterns. That biases the set toward easy evasion, and `PREREG.md` states it.
- I did not sweep family weights. Only the shipped weights (the risk signal) and the weight-independent family strength are scored.
- No patches are needed in the other repositories.
- The next step is for the launcher to timestamp the pre-registration, then run `python3 observer/bench/score.py` once.

