#!/usr/bin/env bash
# YB-0031 data collection, unattended and sequential (timed stages run alone):
# seed-2 derivation recording (already running) -> seed-3 test recording -> judge (prefix, full) -> self-consistency (prefix, full).
cd "$(dirname "$0")/.."; export PATH=$HOME/.lmstudio/bin:/opt/homebrew/bin:/usr/local/bin:$PATH
log() { echo "$(date +%H:%M) $1" >> /tmp/overnight_chain.log; }
while pgrep -f 'agr/recorder.py' >/dev/null; do sleep 60; done; log 'seed 2 done'
.venv/bin/python agr/recorder.py 100 800 --layers --seed=3 > /tmp/rec_L3.log 2>&1; log 'seed 3 recorded'
lms server status 2>&1 | grep -q 'is running' || lms server start --port 1234 >/dev/null 2>&1
lms load openai/gpt-oss-120b --context-length 65536 --gpu max -y --identifier local-strong >/dev/null 2>&1
SEED=3 .venv/bin/python agr/prefix_monitors.py judge > /tmp/prefix_judge3.log 2>&1; log 'prefix judge done'
SEED=3 .venv/bin/python agr/monitors.py judge > /tmp/mon_judge3.log 2>&1; log 'full judge done'
lms unload local-strong >/dev/null 2>&1
SEED=3 .venv/bin/python agr/prefix_monitors.py selfcons > /tmp/prefix_selfcons3.log 2>&1; log 'prefix selfcons done'
SEED=3 .venv/bin/python agr/monitors.py selfcons > /tmp/mon_selfcons3.log 2>&1; log 'full selfcons done'
log OVERNIGHT_DONE
