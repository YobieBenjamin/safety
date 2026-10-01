#!/usr/bin/env bash
# COMMITTED AFTER THE FACT (audit B20): this is the exact wrapper that launched agr/seed7_chain.sh on 2026-09-30.
# It waited until GitHub reported commit b6c795b (the YB-0035 protocol) as main, logged that, then ran the chain.
# The run-alone guard (agr/runguard.py) did not exist yet; no contention was logged in data/agr/contention_windows.txt.
cd ~/Desktop/SAFETY; export PATH=/opt/homebrew/bin:/usr/local/bin:$PATH
while [ "$(git ls-remote origin -h refs/heads/main | cut -c1-7)" != "b6c795b" ]; do sleep 30; done
echo "$(date +%H:%M) protocol b6c795b confirmed on GitHub; starting seed 7" >> /tmp/seed7_chain.log
exec agr/seed7_chain.sh
