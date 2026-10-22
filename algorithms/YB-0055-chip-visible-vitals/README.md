# YB-0055 · Chip-visible vitals

**Status:** pre-registered code, not yet run on the test seeds. Design in docs/PREREGISTRATION.md; synthetic dry run in docs/dryrun.json.
**Run (local, once):** `python3 agr/bench/tier0_vitals.py --run` writes docs/results.json and refuses to run twice.
**Smoke:** `python3 agr/bench/tier0_vitals.py --smoke`. Unit tests: `python3 -m pytest -q algorithms/YB-0055-chip-visible-vitals/tests`.

Standard library only (the project venv has no numpy). Recordings are read from the checkout or, when hidden by skip-worktree, from
`git show HEAD:<path>` (src/recordings.py). Layout: src/vitals_tier0.py (features, model, statistics), src/analysis.py (pipeline),
agr/bench/tier0_vitals.py (entry point).
