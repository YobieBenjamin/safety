#!/usr/bin/env bash
# YB-0033 test-set collection (seed 5): record -> judge at absolute checkpoints (alone) -> self-consistency (alone).
cd "$(dirname "$0")/.."; export PATH=$HOME/.lmstudio/bin:/opt/homebrew/bin:/usr/local/bin:$PATH
log() { echo "$(date +%H:%M) $1" >> /tmp/seed5_chain.log; }
.venv/bin/python agr/recorder.py 100 800 --layers --seed=5 > /tmp/rec_L5.log 2>&1; log 'seed 5 recorded'
lms server status 2>&1 | grep -q 'is running' || lms server start --port 1234 >/dev/null 2>&1
lms load openai/gpt-oss-120b --context-length 65536 --gpu max -y --identifier local-strong >/dev/null 2>&1
CKPT=abs SEED=5 .venv/bin/python agr/prefix_monitors.py judge > /tmp/prefix_judge5.log 2>&1; log 'abs judge done'
lms unload local-strong >/dev/null 2>&1
CKPT=abs SEED=5 .venv/bin/python agr/prefix_monitors.py selfcons > /tmp/prefix_selfcons5.log 2>&1; log 'abs selfcons done'
log SEED5_DONE
