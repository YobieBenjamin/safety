# YB-0055 · Chip-visible vitals: can a regulator restricted to tier-0 signals the governor reads out of band (token rate, latency, cycles, bytes, board power) catch wrong answers in time?

**Hypothesis.** A regulator restricted to the signals a rack-tier governor can read with no host cooperation catches wrong answers before commitment at a matched 10 percent false-alarm rate better than the length and question-type baselines. The prior from YB-0018 is that power contributes nothing, so this is really a test of token rate and per-token latency. If it fails, the chip's own sensing serves enforcement and accountability only, and every early warning must arrive as a signed verdict from an observer with substrate access; the chip design will say so.

**Build.** `algorithms/YB-0055-chip-visible-vitals/`: features restricted to the chip-visible set on the existing recordings (YB-0033 to YB-0045); train on derivation seeds; test once on a fresh seed under the real-time protocol (no future information; matched false-alarm rate; length and question-type controls); pre-register with the timestamp script.

**Runs on the M4 Max.** A cloud agent may write the pre-registered code; the run is local and happens once.

**Artifact.** `algorithms/YB-0055-chip-visible-vitals/docs/results.json`.

**Budget.** About 100k cloud tokens for the code.

**Acceptance command (the launcher runs it after the agent).** `python3 -m pytest -q observer/tests && python3 agr/bench/tier0_vitals.py --smoke`

## Rules for this run
- You are in a git worktree on branch `exp/yb-0055`; it is the only place you write. Run commands from this directory with relative paths; do not cd elsewhere.
- The other repositories of the program are readable at: /Volumes/External_4TB/Safety Experiments/safety-governor /Volumes/External_4TB/Safety Experiments/hardware-and-silicon. Never edit them: a change they need goes into `patches/<repo>/<file>.patch` here, with a note in your final summary.
- Acceptance: `python3 -m pytest -q observer/tests && python3 agr/bench/tier0_vitals.py --smoke`. Run it at most three times. Stop when it passes, or after the third failure; then record exactly what fails in EXPERIMENTS.md (safety-governor) or in the hypothesis's section (safety), with the failing output.
- Read only the files the brief names under Read first and the files you create. Do not read whole directories, do not run the full test suite (the acceptance command is enough), do not search the web, do not start sub-agents.
- Shell commands run without anyone to approve them: a command passes only when every program in it is one of python3, python, pytest, make, pip, git (add, commit, status, diff, log, show, rev-parse, ls-files), ls, cat, head, tail, wc, grep, find, diff, sed, awk, sort, uniq, tr, cut, xargs, printf, mkdir, cp, mv, touch, echo, shasum. Write plain commands: no environment-variable prefix (put a path on sys.path inside the script instead), no sudo, no network, nothing outside this directory. A denied command is denied for good; do not retry it, rewrite it.
- Never weaken, skip or delete an existing test. Do not refactor beyond the brief. No em dashes in anything you write.
- Commit as you go with messages that name the issue (#4) and end with the line: Agent: wave 2, issue #4. Do not push, do not open a pull request; the launcher does both.
- This run is capped at 40 turns and an estimated spend of $10. Keep the tree in a working, committed state at all times, so a cap mid-way still leaves usable work.
- Finish with a summary of at most fifteen lines: what was built, what passes, what does not and why, open questions. It is posted on the issue as is.
