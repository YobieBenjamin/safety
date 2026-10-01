# YB-0042 · The regulator versus a hidden-state probe (and a second fresh replication against the LLM judge)

**Status:** pre-registered (docs/PREREGISTRATION.md, with the full analysis code and a dry run, docs/dryrun.json), before
any YB-0042 recording exists. Results pending.
**Reproduce:** `SANDBOX_MEM=12g SANDBOX_TIMEOUT=14400 sandbox/run.sh algorithms/YB-0042-probe-baseline all` (dry run: `DRY_RUN=1`).

## Plain English
Our regulator reads 120 summary vital signs per token. The obvious competitor from published work is a probe: a simple
statistical model trained on the AI's full internal state (thousands of numbers per layer). If a probe does as well as
or better than the regulator in the same race, the honest conclusion is that reading the AI's internals beats the AI
judge, but our particular vital signs add nothing. This experiment finds out, and also repeats the race against the
judge on a second, brand-new test set.

## Instruments
agr/hstap.py captures hidden states in the same pass as the telemetry (agr/layertap.py, unchanged);
agr/test_hstap_alignment.py verifies alignment and that the telemetry is unchanged (passed 2026-10-01: aligned error
0.010-0.114 vs neighbour 0.735-1.949; telemetry errors identical to the YB-0035 baseline). Chain: agr/yb0042_chain.sh.
