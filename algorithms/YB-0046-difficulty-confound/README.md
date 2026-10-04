# YB-0046: is the internal-state signal more than a difficulty detector?

Pre-registered secondary analysis of the YB-0045 recordings. Adds a difficulty baseline built only from the question text (digits, carries,
string length, exponent size and so on) and asks whether the regulator and probe beat it, and whether internal state adds to it.
Plan: docs/PREREGISTRATION.md. Dry run (seeds 2-8 vs 10-12, test seeds untouched): docs/dryrun.json. Results: docs/results.json.
Code: src/difficulty.py (features and baseline), tests/experiment.py; src/ otherwise a byte-identical copy of YB-0045 (docs/src_hashes.txt).
