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

def test_cap_alarm_respects_cap():
    # the tie-aware alarm's false-alarm rate is floor(cap*n)/n, which is at most the cap, for every seed
    for n in (7, 20, 55, 100, 123):
        nc = n - n // 10
        y = [0] * nc + [1] * (n - nc)
        for seed in (0, 1, 2, 17):
            f = V.cap_alarm([float((i * 37) % 7) for i in range(n)], y, seed=seed)
            assert sum(f[i] for i in range(nc)) <= 0.10 * nc + 1e-9

def test_tied_control_reaches_cap():
    # the length and question-type baselines take few distinct values; under a strict '> cap_threshold'
    # they catch 0 when more than the cap fraction of the correct tie at the top value. cap_alarm splits
    # that tie, so the control reaches the cap (FPR exactly the cap) instead of being handicapped to 0.
    y = [0] * 90 + [1] * 10
    scores = [3] * 100                          # every episode reaches the top checkpoint
    assert sum(1 for s in scores[90:] if s > V.cap_threshold(scores[:90])) == 0      # strict control: handicapped
    for seed in range(8):
        assert sum(V.cap_alarm(scores, y, seed=seed)[i] for i in range(90)) == 9     # FPR reaches the cap
    assert sum(sum(V.cap_alarm(scores, y, seed=s)[i] for i in range(90, 100)) for s in range(8)) > 0

def test_project_drops_content():
    # the load boundary projects to the tier-0 fields; the content fields never reach a feature
    r = dict(V.synth(1, 1)[0], text='secret', entropy=[0.1], p_top1=0.9, margin=0.2, toks=[1], final='x', truth='y')
    p = V.project(r)
    for k in ('text', 'entropy', 'p_top1', 'margin', 'toks', 'final', 'truth'):
        assert k not in p
    assert set(p) <= set(V.CHIP_FIELDS + V.SCORING_FIELDS)
    assert p['latency'] is not None and p['correct'] is not None
