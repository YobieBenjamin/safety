#!/usr/bin/env bash
# Publish only after the timing/power-sensitive recording has finished (never load the machine mid-recording).
cd "$(dirname "$0")/.."; export PATH=/opt/homebrew/bin:/usr/local/bin:$PATH
while pgrep -f 'agr/recorder.py' >/dev/null; do sleep 20; done
./publish.sh 'AGR results written up: YB-0015 (contamination), YB-0017 (HPA organism), YB-0009 (coupling graph) with theory, math, proofs, repeatable proof, plain English; ledger + backlog (YB-0019, YB-0020); YB-0018 power instrument' > /tmp/publish11.log 2>&1
echo "EXIT=$?" >> /tmp/publish11.log; git -C ~/safety pull -q >> /tmp/publish11.log 2>&1; echo DONE >> /tmp/publish11.log
