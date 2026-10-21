"""pytest entry for the YB-0052 self-checks: python3 -m pytest -q observer/bench"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import checks  # noqa: E402
import score  # noqa: E402


def test_set_checks():
    checks.check_set(score.load_rows())


def test_scorer_checks():
    checks.check_scorer()
