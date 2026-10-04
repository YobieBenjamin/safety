# YB-0047: internal state vs a trained text monitor, and cross-task transfer

Pre-registered secondary analysis of the YB-0045 recordings. Part A compares the regulator and probe with a text monitor trained on the same
reasoning prefixes and labels. Part B refits each monitor without one task type and tests it on that type (leave-one-task-out).
Plan: docs/PREREGISTRATION.md. Dry run: docs/dryrun.json. Results: docs/results.json. Code: src/textmon.py, tests/experiment.py; src/ otherwise
a byte-identical copy of YB-0045 (docs/src_hashes.txt).
