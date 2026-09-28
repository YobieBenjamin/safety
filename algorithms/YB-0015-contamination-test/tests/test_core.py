import sys, numpy as np
sys.path.insert(0, 'src')
from agr import features, features_ref
def t_random():
    r = np.random.default_rng(0)
    for n in (2, 3, 17, 400):
        x = r.normal(size=n); assert np.allclose(features(x), features_ref(x), atol=1e-12)
def t_constant():
    f = features(np.full(50, 3.0)); assert f[0] == 3 and f[1] == 0 and f[2] == 0 and f[5] == 0 and f[6] == 0
def t_ramp():
    f = features(np.arange(10.0)); assert abs(f[5] - 1) < 1e-12 and abs(f[2] - 1) < 1e-12 and f[3] == 9 and f[4] == 0
def t_spike():
    x = np.zeros(100); x[7] = 100; assert abs(features(x)[6] - 0.01) < 1e-12
def t_short():
    assert np.isnan(features(np.array([1.0]))).all()
T = [t_random, t_constant, t_ramp, t_spike, t_short]
for t in T: t(); print('PASS', t.__name__)
print(f'{len(T)}/{len(T)} tests passed')
