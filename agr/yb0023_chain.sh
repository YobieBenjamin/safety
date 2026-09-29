#!/usr/bin/env bash
# YB-0023 monitors on a quiet machine: wait for YB-0019 to finish, then judge alone, then self-consistency alone.
cd "$(dirname "$0")/.."; export PATH=$HOME/.lmstudio/bin:/opt/homebrew/bin:/usr/local/bin:$PATH
while ! grep -q ALL_DONE /tmp/yb0019_chain.log 2>/dev/null; do sleep 60; done
lms server status 2>&1 | grep -q 'is running' || lms server start --port 1234 >/dev/null 2>&1
lms load openai/gpt-oss-120b --context-length 65536 --gpu max -y --identifier local-strong >/dev/null 2>&1
.venv/bin/python agr/prefix_monitors.py judge > /tmp/prefix_judge.log 2>&1
lms unload local-strong >/dev/null 2>&1
.venv/bin/python agr/prefix_monitors.py selfcons > /tmp/prefix_selfcons.log 2>&1
echo YB0023_MONITORS_DONE > /tmp/yb0023_chain.log
