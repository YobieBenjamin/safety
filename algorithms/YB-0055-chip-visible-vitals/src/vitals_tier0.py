# Copyright (c) 2026 Yobie Benjamin. Autonomic Graph Regulation (AGR). All rights reserved except as licensed.
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (see LICENSE.md, NOTICE)
# Provenance canary: AGR-CANARY-7f3c2a9e-5b14-4d6e-9a1f-2c8e0b6d4a71
'''YB-0055: a regulator restricted to tier-0 signals (what a rack-tier governor reads with no host cooperation).
Standard library only. Statistics follow YB-0035 corrected.py (in-time max, 10 percent cap, threshold-resampling bootstrap).

Tier-0 view of an episode: the per-token arrival latencies (token rate, per-token latency, elapsed time) and the token count
(bytes are a function of the token count at this tier). Board power is part of the tier but is null in every existing
recording, so it is reported as not testable. Cycles are not recorded; wall time is the proxy. Everything else in a recording
(text, entropy, p_top1, margin, toks, final, truth, correct) is dropped by chip_view and never reaches a feature.'''
import math, random

T = (48, 96, 192, 384)
CAP, COST = 0.10, 0.005
CHIP_FIELDS = ('idx', 'seed', 'latency', 'power')            # the observable stream
SCORING_FIELDS = ('answered', 'correct', 'final_start', 'cat')  # used only to score and to build the controls, never as features
FEATURES = ('log_ttft', 'mean_log_lat', 'sd_log_lat', 'recent_vs_mean', 'slope', 'stall_frac', 'max_vs_median', 'log_elapsed')
GROUPS = {'full': FEATURES, 'level': ('log_ttft', 'mean_log_lat', 'sd_log_lat', 'log_elapsed'),
          'shape': ('recent_vs_mean', 'slope', 'stall_frac', 'max_vs_median')}

def chip_view(r):
    '''The tier-0 observable of an episode: only the keys in CHIP_FIELDS.'''
    return {k: r.get(k) for k in CHIP_FIELDS}

def checkpoints(r): return [t for t in T if t < r['final_start']]

def features(lat, t):
    '''Features at checkpoint t from lat[:t] only (no future information).'''
    x = lat[:t]; dec = x[1:]; lg = [math.log(max(v, 1e-4)) for v in dec]; n = len(lg)
    mean = sum(lg) / n; sd = math.sqrt(sum((v - mean) ** 2 for v in lg) / n)
    med = sorted(dec)[n // 2]; rec = dec[-16:]
    mi = (n - 1) / 2; den = sum((i - mi) ** 2 for i in range(n)) or 1.0
    slope = sum((i - mi) * (v - mean) for i, v in enumerate(lg)) / den * t          # change in log latency over the prefix
    return dict(log_ttft=math.log(max(x[0], 1e-4)), mean_log_lat=mean, sd_log_lat=sd,
                recent_vs_mean=math.log(max(sum(rec) / len(rec), 1e-4)) - math.log(max(sum(dec) / n, 1e-4)), slope=slope,
                stall_frac=sum(1 for v in dec if v > 1.5 * med) / n, max_vs_median=math.log(max(max(dec), 1e-4) / max(med, 1e-4)),
                log_elapsed=math.log(max(sum(x), 1e-4)))

# ---- logistic regression (ridge, Newton) ----
def solve(A, b):
    n = len(b); M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda i: abs(M[i][c])); M[c], M[p] = M[p], M[c]
        for i in range(c + 1, n):
            f = M[i][c] / M[c][c]
            for j in range(c, n + 1): M[i][j] -= f * M[c][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1): x[i] = (M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))) / M[i][i]
    return x

def fit_logistic(X, y, lam, iters=12):
    d = len(X[0]); w = [0.0] * d
    for _ in range(iters):
        g = [lam * w[j] if j < d - len(T) else 0.0 for j in range(d)]; H = [[0.0] * d for _ in range(d)]
        for j in range(d - len(T)): H[j][j] += lam
        for xi, yi in zip(X, y):
            z = sum(a * b for a, b in zip(w, xi)); p = 1 / (1 + math.exp(-max(-30.0, min(30.0, z)))); s = p * (1 - p) + 1e-6
            for j in range(d):
                if xi[j] == 0.0: continue
                g[j] += (p - yi) * xi[j]; sj = s * xi[j]; Hj = H[j]
                for k in range(j, d): Hj[k] += sj * xi[k]
        for j in range(d):
            for k in range(j): H[j][k] = H[k][j]
        step = solve(H, g); w = [a - b for a, b in zip(w, step)]
        if max(abs(v) for v in step) < 1e-6: break
    return w

class Vitals:
    '''Pooled ridge logistic over checkpoints; features standardised per checkpoint on the training rows; one intercept per checkpoint.'''
    def __init__(self, group='full', lam=10.0): self.names, self.lam = GROUPS[group], lam
    def row(self, f, t): return [(f[n] - self.mu[t][n]) / self.sd[t][n] for n in self.names] + [1.0 if t == u else 0.0 for u in T]
    def fit(self, jobs):
        '''jobs: list of (episode, t, feature-dict, wrong).'''
        self.mu, self.sd = {}, {}
        for t in T:
            F = [f for _, tt, f, _ in jobs if tt == t]; self.mu[t], self.sd[t] = {}, {}
            for n in self.names:
                v = [f[n] for f in F] or [0.0]; m = sum(v) / len(v); s = math.sqrt(sum((a - m) ** 2 for a in v) / len(v))
                self.mu[t][n], self.sd[t][n] = m, s if s > 1e-9 else 1.0
        self.w = fit_logistic([self.row(f, t) for _, t, f, _ in jobs], [yy for *_, yy in jobs], self.lam); return self
    def score(self, f, t): return sum(a * b for a, b in zip(self.w, self.row(f, t)))

def make_jobs(R):
    return [(r, t, features(r['latency'], t), 0 if r['correct'] else 1) for r in R if r['answered'] for t in checkpoints(r)]

# ---- statistics (YB-0035 corrected.py, stdlib) ----
def in_time_max(checks):
    v = [s for s, t, c, d in checks if t + c <= d]; return max(v) if v else -math.inf

def cap_threshold(v_correct, cap=CAP):
    '''Smallest threshold with at most cap of correct episodes scoring above it.'''
    s = sorted(v_correct, reverse=True); n = len(s); k = int(math.floor(cap * n + 1e-12))
    return s[k] if k < n else -math.inf

def in_time(R, fn, cost):
    V = []
    for r in R:
        lat = r['latency']; D = sum(lat[:r['final_start']]); acc = 0.0; checks = []; last = 0
        for t in checkpoints(r):
            acc += sum(lat[last:t]); last = t; checks.append((fn(r, t), acc, cost(r, t), D))
        V.append(in_time_max(checks))
    return V

def evaluate(V, y, mon):
    thr = cap_threshold([v for v, yy in zip(V, y) if yy == 0]); f = [v > thr for v in V]
    w = [i for i, yy in enumerate(y) if yy == 1]; c = [i for i, yy in enumerate(y) if yy == 0]
    mc = [i for i in c if mon[i]]
    return dict(threshold=thr, caught=sum(f[i] for i in w), wrong=len(w), recall=sum(f[i] for i in w) / len(w) if w else None,
                fpr=sum(f[i] for i in c) / len(c), fpr_monitorable=sum(f[i] for i in mc) / len(mc) if mc else None,
                recall_monitorable=(lambda mw: sum(f[i] for i in mw) / len(mw) if mw else None)([i for i in w if mon[i]]))

def recall_at_cap(V, y):
    thr = cap_threshold([v for v, yy in zip(V, y) if yy == 0]); w = [v for v, yy in zip(V, y) if yy == 1]
    return sum(v > thr for v in w) / len(w)

def boot_diff(Va, Vb, y, n=1000, seed=0):
    '''Resample all episodes, reset both thresholds on each resample's correct episodes, recall difference on its wrong ones.'''
    g = random.Random(seed); N = len(y); d = []
    for _ in range(n):
        i = [g.randrange(N) for _ in range(N)]; yy = [y[k] for k in i]
        if sum(yy) == 0 or sum(yy) == N: continue
        d.append(recall_at_cap([Va[k] for k in i], yy) - recall_at_cap([Vb[k] for k in i], yy))
    d.sort(); q = lambda p: d[min(len(d) - 1, max(0, int(p * len(d))))]
    return [round(recall_at_cap(Va, y) - recall_at_cap(Vb, y), 4), round(q(0.025), 4), round(q(0.975), 4)]

def auroc(y, s):
    pos = [v for v, yy in zip(s, y) if yy == 1]; neg = [v for v, yy in zip(s, y) if yy == 0]
    if not pos or not neg: return None
    order = sorted(range(len(s)), key=lambda i: s[i]); rk = [0.0] * len(s); i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and s[order[j + 1]] == s[order[i]]: j += 1
        for k in range(i, j + 1): rk[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return (sum(rk[k] for k in range(len(s)) if y[k] == 1) - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))

def boot_auc(y, s, n=500, seed=0):
    g = random.Random(seed); N = len(y); a = []
    for _ in range(n):
        i = [g.randrange(N) for _ in range(N)]; v = auroc([y[k] for k in i], [s[k] for k in i])
        if v is not None: a.append(v)
    a.sort(); return [round(auroc(y, s), 4), round(a[int(0.025 * len(a))], 4), round(a[min(len(a) - 1, int(0.975 * len(a)))], 4)]

def synth(n, seed, wrong_rate=0.12):
    '''Synthetic recordings for the smoke test and the dry run: wrong answers drift slower and stall more.'''
    g = random.Random(seed); R = []
    for i in range(n):
        wrong = g.random() < wrong_rate; fs = g.randrange(20, 520); nt = fs + 20; base = 0.011 * (1.15 if wrong else 1.0)
        lat = [0.15] + [base * math.exp(g.gauss(0, 0.05 + (0.15 if wrong else 0.0))) * (3 if g.random() < (0.12 if wrong else 0.04) else 1) for _ in range(nt - 1)]
        R.append(dict(idx=seed * 100000 + i, seed=seed, cat=['mul_hard', 'weekday', 'modpow'][i % 3], answered=True, correct=not wrong,
                      final_start=fs, n_tokens=nt, latency=lat, power=None))
    return R
