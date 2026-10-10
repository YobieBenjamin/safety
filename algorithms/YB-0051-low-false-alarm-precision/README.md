# YB-0051: precision at low false-alarm rates

Stage: PRE-REGISTERED (docs/PREREGISTRATION.md, timestamped before any test data exist). Results will appear here after the run.

Plain English: when real mistakes are rare (1 in 100 answers), even a good alarm cries wolf many times for every real catch. YB-0050
showed that is the real limit, not compute. YB-0051 tests a fix found in exploration: let the model answer the same question again
8 times, count how often it disagrees with itself, and break ties inside each disagreement level with the non-LLM internal-state
scores. Outside code, not a language model, makes the call. New test seeds 27-38 are recorded only after the plan is timestamped.

- tests/candidates.py: the frozen candidate scores (C1 tie-break, C2 combination, C3 conjunction, C4 per-task calibration).
- tests/score_test.py: scores the test seeds with the non-LLM monitors fitted on seeds 2-14 (same as the reference).
- tests/experiment.py: H1-H3 and the descriptive tables (make confirmatory only after the timestamp).
- tests/test_candidates.py, tests/c4_check.py: unit tests and the pre-freeze C4 check (docs/c4_derivation_check.json).
- explore/: the exploratory analysis that generated the hypotheses (selection only, not evidence).
- Recorder and chain: agr/selfcons_yb0051.py, agr/yb0051_chain.sh, agr/yb0051_start.sh.
