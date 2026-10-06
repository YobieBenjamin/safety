# YB-0050: a powered decider, and whether the regulator can scale

Pre-registered test (docs/PREREGISTRATION.md) on NEW test seeds 15 to 26, recorded after the plan is timestamped. It settles two close
calls from YB-0047 and YB-0049 with about four times the data, tests whether a stack with no language-model signal comes within 10 points
of the model's own self-consistency, and measures the two numbers that decide whether the regulator scales: cost per check as a share of
inference, and the false-alarm burden at realistic error base rates.

Position held by the author (design principle, not a tested claim): no AI is the judge, jury or arbiter of AI safety. The model's
disagreement with itself is used only as a signal measured by outside code; the decision to alarm, hold or block is made by non-LLM code
and, for irreversible acts, a human.

## Run
One command on the Mac: `agr/yb0050_start.sh` (waits for AC power; `--now` to skip). Progress: /tmp/chain50.log, copied to
agr/yb0050_chain_progress.log. Analysis targets: `make smoke`, `make dryrun`, `make confirmatory` (only after the public timestamp).

## Code
src/decider.py (alarm rules, one paired bootstrap for every comparison, burden arithmetic, operation counts; new), tests/experiment.py
(new), tests/test_decider.py (new). Every other file in src/ is a byte-identical copy of YB-0048 (layered.py of YB-0049); see
docs/src_hashes.txt. Recorders: agr/recorder.py (unchanged), agr/selfcons_yb0050.py (agr/selfcons_yb0049.py with only seeds and file
names changed).

## Data
Derivation: YB-0045 recordings, seeds 2 to 14, through hash-verified local hard links (not tracked; the record is
algorithms/YB-0045-powered-replication/data). Test: seeds 15 to 26 and their self-consistency reviews, packed into data/ by the chain
(tracked).

## Results
Pending (not yet recorded).
