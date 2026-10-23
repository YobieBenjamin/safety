# Copyright (c) 2026 Yobie Benjamin. Autonomic Graph Regulation (AGR). All rights reserved except as licensed.
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (see LICENSE.md, NOTICE)
# Provenance canary: AGR-CANARY-7f3c2a9e-5b14-4d6e-9a1f-2c8e0b6d4a71
# YB-0055 is standard library only (no C core, no numpy), so there is no build step.
# test:       compile everything, run the unit tests with plain python3 (CI installs no pytest).
# experiment: what CI runs when this folder changes: the full pipeline on SYNTHETIC data (--dry, about 10 s),
#             with docs/dryrun.json put back afterwards so the committed record is never rewritten by a check.
#             The real pre-registered run (--run) touches the recordings, refuses to run twice and is a local step;
#             it is deliberately not a target here, so no check can spend it by accident.
.PHONY: all test experiment smoke clean
ROOT := ../..
all: test experiment
test:
	python3 -m py_compile src/*.py tests/*.py $(ROOT)/agr/bench/tier0_vitals.py
	python3 tests/run_plain.py
experiment: test
	@cp docs/dryrun.json docs/.dryrun.keep
	@cd $(ROOT) && python3 agr/bench/tier0_vitals.py --dry; s=$$?; mv algorithms/YB-0055-chip-visible-vitals/docs/.dryrun.keep algorithms/YB-0055-chip-visible-vitals/docs/dryrun.json; exit $$s
smoke:
	cd $(ROOT) && python3 agr/bench/tier0_vitals.py --smoke   # needs pytest (local venv), not run in CI
clean:
	rm -rf src/__pycache__ tests/__pycache__ docs/.dryrun.keep
