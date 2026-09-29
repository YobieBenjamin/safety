#!/usr/bin/env bash
# Re-record training (seed 0, 480) and held-out (seed 1, 240) episodes with 24-layer telemetry. Same questions and,
# with greedy decoding, the same tokens and answers as before (verified on a smoke test).
cd "$(dirname "$0")/.."
.venv/bin/python agr/recorder.py 80 800 --layers > /tmp/rec_L0.log 2>&1
.venv/bin/python agr/recorder.py 40 800 --layers --seed=1 > /tmp/rec_L1.log 2>&1
echo DEEP_RECORDING_DONE > /tmp/deep_chain.log
