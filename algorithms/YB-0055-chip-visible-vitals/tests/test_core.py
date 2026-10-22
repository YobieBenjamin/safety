import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
import vitals_tier0 as V

def test_cap_threshold_respects_cap():
    for n in (7, 20, 55, 100):
        v = [math.sin(i) for i in range(n)]; thr = V.cap_threshold(v)
        assert sum(x > thr for x in v) <= 0.10 * n + 1e-9

def test_cap_threshold_ties():
    v = [1.0] * 10 + [0.0] * 10; assert sum(x > V.cap_threshold(v) for x in v) <= 2

def test_features_use_prefix_only():
    r = V.synth(5, 3)[0]; a = V.features(r['latency'], 48); b = V.features(r['latency'][:48] + [5.0] * 100, 48)
    assert a == b

def test_chip_view_drops_content():
    r = dict(V.synth(1, 1)[0], text='secret', entropy=[0.1], final='x', truth='y')
    assert set(V.chip_view(r)) == set(V.CHIP_FIELDS)

def test_auroc_known():
    assert V.auroc([0, 0, 1, 1], [0.1, 0.2, 0.3, 0.4]) == 1.0 and V.auroc([0, 1], [0.5, 0.5]) == 0.5

def test_logistic_learns_signal():
    R = V.synth(600, 7, 0.2); m = V.Vitals('full', 10.0).fit(V.make_jobs(R))
    jobs = V.make_jobs(V.synth(400, 8, 0.2)); a = V.auroc([j[3] for j in jobs], [m.score(j[2], j[1]) for j in jobs])
    assert a > 0.7

def test_in_time_excludes_late_checks():
    assert V.in_time_max([(5.0, 10.0, 1.0, 10.5)]) == -math.inf and V.in_time_max([(5.0, 1.0, 1.0, 10.5)]) == 5.0
