# Hypothesis Backlog

The miner takes the first `status: open` entry. Each must be coded, compiled, tested against a baseline, and documented in four registers (plain English, technical, math, code). Negative results are recorded, not discarded.

## YB-0002 — Bounded homeostasis as a universal monitor wrapper
status: tested
foundation: homeostatic plasticity, set-point limits
hypothesis: YB-0001's drift budget, wrapped around the strongest detectors (energy, activation-Mahalanobis), preserves their AUROC while eliminating slow-poisoning degradation; formalize a bound on adversarial baseline displacement as a function of eta, tau, B.
test: reproduce YB-0001 drift stream with energy + act-Maha; sweep eta and B; report detection delay vs false-alarm curves; prove the displacement bound and check it numerically.

## YB-0003 — Lateral-inhibition sparsity auditor
status: open
foundation: lateral inhibition, winner-take-all circuits
hypothesis: adversarial and OOD inputs lower the k-winner concentration of hidden layers (less "decisive" routing); a Gini/k-WTA margin on activations is a cheap detector competitive with MSP on FGSM.
test: same digits benchmark; compare to MSP/energy.

## YB-0004 — Immune negative-selection over activation motifs
status: open
foundation: thymic negative selection, graph motifs
hypothesis: detectors generated to NOT match self (trusted) 3-node flow motifs in the effective connectivity graph flag novel computation paths; measure detector coverage vs set size.

## YB-0005 — Scalable heat trace for transformers
status: open
foundation: stochastic trace estimation (Hutchinson + Lanczos quadrature)
hypothesis: YB-0001's negative result was driven by permutation invariance, not by the graph object; a node-anchored heat-kernel diagonal diag(e^{-tL}) (retains unit identity) outperforms the trace; make it O(n·nnz) for attention graphs.

## YB-0006 — Amygdala low-road circuit breaker
status: open
foundation: dual-pathway threat processing (fast subcortical vs slow cortical)
hypothesis: a tiny probe on early-layer activations can veto an action before the full forward pass completes, with bounded miss rate relative to a full-depth probe; measure latency/recall trade-off.

## YB-0007 — Sample-efficient drift-budget calibration in high dimension
status: open
foundation: YB-0002 failure mode; bootstrap resampling; low-rank (PCA) feature compression
hypothesis: YB-0002's closed-form budget (C1/C2) underestimates clean drift 14x in 64-D with ~112 calibration samples; a bootstrap-simulated clean EWMA path (or projection to top-k principal components) yields budgets with <=1/10 clean false alarms while keeping >=9/10 drift detection.
test: rerun YB-0002 experiment with (a) bootstrap budget, (b) PCA k in {4, 8, 16}; report false alarms, detection, alarm delay.
