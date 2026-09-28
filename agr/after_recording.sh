#!/usr/bin/env bash
# Waits for the recorder to finish, snapshots the dataset into each algorithm, runs both experiments in the sandbox.
cd "$(dirname "$0")/.."
while pgrep -f 'agr/recorder.py' >/dev/null; do sleep 20; done
gzip -9 -c data/agr/episodes.jsonl > /tmp/episodes.jsonl.gz
for a in YB-0015-contamination-test YB-0017-hpa-axis-organism; do
  cp /tmp/episodes.jsonl.gz algorithms/$a/data/episodes.jsonl.gz
  sandbox/run.sh algorithms/$a all > /tmp/$a.log 2>&1; echo "$a EXIT=$?" >> /tmp/agr_pipeline.log
done
echo PIPELINE_DONE >> /tmp/agr_pipeline.log
