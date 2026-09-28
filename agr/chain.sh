#!/usr/bin/env bash
# Dedicated-machine chain: finish batch 1, extend to 480 episodes (same deterministic prefix), then analyze.
cd "$(dirname "$0")/.."
while pgrep -f 'agr/recorder.py' >/dev/null; do sleep 20; done
.venv/bin/python agr/recorder.py 80 800 >> /tmp/rec_full.log 2>&1
agr/after_recording.sh
