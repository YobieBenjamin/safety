import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bench"))
import independence as ind  # noqa: E402


def test_phi_identical_opposite_and_constant():
    assert ind.phi([1, 0, 1, 0], [1, 0, 1, 0]) == pytest.approx(1.0)
    assert ind.phi([1, 0, 1, 0], [0, 1, 0, 1]) == pytest.approx(-1.0)
    assert ind.phi([1, 1, 1], [1, 0, 1]) is None


def test_subsets_count():
    assert len(ind.subsets(4)) == 4 + 6 * 2 + 4 * 3 + 4


def test_incomplete_rows_are_dropped_and_counted():
    rows = [
        {"id": "a", "source": "x", "label": 1, "scores": {m: 1.0 for m in ind.MONITORS}},
        {"id": "b", "source": "x", "label": 0, "scores": dict({m: 0.0 for m in ind.MONITORS}, sentry=None)},
    ]
    pos, ben, cov = ind.split_complete(rows)
    assert len(pos) == 1 and ben == []
    assert cov["x"]["rows"] == 2 and cov["x"]["complete"] == 1 and cov["x"]["sentry"] == 1


def test_any_of_four_at_per_monitor_budget_inflates_false_alarms():
    pos, ben, _ = ind.split_complete(ind.synthetic_table(0.0, seed=3))
    out = ind.evaluate(pos, ben, 0.10)
    assert out["mmfar|0.1.2.3|1"] > 0.2
    assert out["mq|0.1.2.3|1"] >= out["mm|0.1.2.3|1"] - 1e-9


def test_single_monitor_modes_agree():
    pos, ben, _ = ind.split_complete(ind.synthetic_table(0.0, seed=4))
    out = ind.evaluate(pos, ben, 0.10)
    assert out["mq|2|1"] == pytest.approx(out["single|2"], abs=0.02)


def test_too_few_inputs_refused():
    pos, ben, _ = ind.split_complete(ind.synthetic_table(0.0, n_pos=5, n_ben=20))
    with pytest.raises(SystemExit):
        ind.analyse(pos, ben)


def test_regimes_are_told_apart():
    prereg = dict(ind.PREREG, bootstrap_resamples=40)
    a = ind.analyse(*ind.split_complete(ind.synthetic_table(0.0))[:2], prereg)
    b = ind.analyse(*ind.split_complete(ind.synthetic_table(3.0))[:2], prereg)
    assert a["quorum_helps"] and not b["quorum_helps"]
    assert a["mean_pairwise_phi"] < b["mean_pairwise_phi"]


def test_layer3_score_runs():
    assert ind.layer3_score("files.read", {"path": "reports/q3.md"}) < 0.05
