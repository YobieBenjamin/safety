# YB-0048: multi-level, hospital-style fusion of non-LLM monitors

Pre-registered secondary analysis of the YB-0045 recordings. Does combining question difficulty, a trained text monitor, a hidden-state probe and the telemetry regulator beat the best of them, as a learned stack and as a transparent NEWS2-style banded score? Plan: docs/PREREGISTRATION.md. Code: src/fusion.py, tests/experiment.py.

## Data
This analysis reads the YB-0045 recordings through a local hard-linked copy in data/ (not tracked in git). The record is algorithms/YB-0045-powered-replication/data; every file is SHA-256 identical (checked 2026-10-04).
