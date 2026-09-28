# Hypothesis Backlog

The miner takes the first `status: open` entry. Each must be coded, compiled, tested against a baseline, and documented in four registers (plain English, technical, math, code). Negative results are recorded, not discarded.

## YB-0002 — Bounded homeostasis as a universal monitor wrapper
status: tested
foundation: homeostatic plasticity, set-point limits
hypothesis: YB-0001's drift budget, wrapped around the strongest detectors (energy, activation-Mahalanobis), preserves their AUROC while eliminating slow-poisoning degradation; formalize a bound on adversarial baseline displacement as a function of eta, tau, B.
test: reproduce YB-0001 drift stream with energy + act-Maha; sweep eta and B; report detection delay vs false-alarm curves; prove the displacement bound and check it numerically.

## YB-0003 — Lateral-inhibition sparsity auditor
status: deferred (MLP testbed; superseded by the AGR program, docs/RESEARCH_PROGRAM.md)
foundation: lateral inhibition, winner-take-all circuits
hypothesis: adversarial and OOD inputs lower the k-winner concentration of hidden layers (less "decisive" routing); a Gini/k-WTA margin on activations is a cheap detector competitive with MSP on FGSM.
test: same digits benchmark; compare to MSP/energy.

## YB-0004 — Immune negative-selection over activation motifs
status: deferred (MLP testbed; superseded by the AGR program, docs/RESEARCH_PROGRAM.md)
foundation: thymic negative selection, graph motifs
hypothesis: detectors generated to NOT match self (trusted) 3-node flow motifs in the effective connectivity graph flag novel computation paths; measure detector coverage vs set size.

## YB-0005 — Scalable heat trace for transformers
status: deferred (MLP testbed; superseded by the AGR program, docs/RESEARCH_PROGRAM.md)
foundation: stochastic trace estimation (Hutchinson + Lanczos quadrature)
hypothesis: YB-0001's negative result was driven by permutation invariance, not by the graph object; a node-anchored heat-kernel diagonal diag(e^{-tL}) (retains unit identity) outperforms the trace; make it O(n·nnz) for attention graphs.

## YB-0006 — Amygdala low-road circuit breaker
status: deferred (MLP testbed; superseded by the AGR program, docs/RESEARCH_PROGRAM.md)
foundation: dual-pathway threat processing (fast subcortical vs slow cortical)
hypothesis: a tiny probe on early-layer activations can veto an action before the full forward pass completes, with bounded miss rate relative to a full-depth probe; measure latency/recall trade-off.

## YB-0007 — Sample-efficient drift-budget calibration in high dimension
status: deferred (MLP testbed; superseded by the AGR program, docs/RESEARCH_PROGRAM.md)
foundation: YB-0002 failure mode; bootstrap resampling; low-rank (PCA) feature compression
hypothesis: YB-0002's closed-form budget (C1/C2) underestimates clean drift 14x in 64-D with ~112 calibration samples; a bootstrap-simulated clean EWMA path (or projection to top-k principal components) yields budgets with <=1/10 clean false alarms while keeping >=9/10 drift detection.
test: rerun YB-0002 experiment with (a) bootstrap budget, (b) PCA k in {4, 8, 16}; report false alarms, detection, alarm delay.

# Program AGR: Autonomic Graph Regulation (priority order; see docs/RESEARCH_PROGRAM.md)

## YB-0008 — Vital-sign telemetry for a live transformer
status: open
foundation: interoception; the patient model (gpt-oss-20b MLX, 24 layers)
hypothesis: token-level (entropy, margin, latency) and layer-level (activation norms, attention concentration, residual drift) vitals can be recorded reproducibly per token over agent-like episodes.
test: trusted host recorder + labelled episode suite (benign, impossible, jailbreak, conflicting instructions, pressure to fabricate); publish dataset schema and reliability checks (same seed -> same vitals).

## YB-0009 — Physiological coupling graph (network physiology)
status: tested
foundation: network physiology; time-delay stability; graph Laplacian
hypothesis: the coupling graph among vital channels changes topology under stress episodes (lambda_2, modularity, spectral entropy) before the output shows failure.

## YB-0010 — Transformer HRV
status: open
foundation: heart-rate variability; loss of variability under stress
hypothesis: variability of the entropy rhythm (RMSSD, spectral balance, sample entropy) is lower under stress episodes and predicts failure.

## YB-0011 — Cortisol integrator (HPA axis)
status: open
foundation: HPA axis, allostatic load, negative feedback
hypothesis: a slow leaky integrator of accumulated surprise with negative feedback gives earlier and steadier warning than instantaneous thresholds, with fewer false alarms.

## YB-0012 — Flagship: vitals vs behavior monitoring (pre-registered)
status: tested (H1 inferior on verifiable tasks; H2 earliness confirmed)
foundation: the core thesis
hypothesis: on identical episodes, autonomic vitals beat output-based behavior monitoring on lead time and on failures whose outputs look normal.

## YB-0013 — Somatic-marker instinct
status: open
foundation: Damasio somatic markers; amygdala low road; graph kernels
hypothesis: a fast classifier on vital-graph patterns learned from past bad outcomes vetoes failures before deliberation completes.

## YB-0014 — Autonomic controller on the graph
status: open
foundation: sympathetic/parasympathetic balance; vagal brake; YB-0002 allostasis
hypothesis: a two-channel graph controller (escalate vs damp) keeps the agent inside a proven safe region (Lyapunov-style bound) while preserving task performance.

# Independence Principle hypotheses (the regulator is external, non-transformer, text-blind)

## YB-0015 — Contamination test
status: tested
foundation: Independence Principle; confident-wrong (gospel) regime
hypothesis: logit/substrate vitals fail precisely on confidently-wrong episodes, while physical (tier 0) and consequence (tier 1) signals do not.
test: episodes with known ground truth; stratify by model confidence; compare AUROC and lead time per signal tier.

## YB-0016 — Illiterate regulator vs LLM judge
status: open
foundation: text-blind regulation cannot be persuaded
hypothesis: under attacks crafted to fool monitors, an LLM-judge monitor is manipulated while a text-blind graph regulator is not.
test: adversarial episode suite targeting the monitor; measure monitor evasion rate for both.

## YB-0017 — HPA-axis organism
status: tested
foundation: hypothalamus-pituitary-adrenal feedback (CRH -> ACTH -> cortisol, negative feedback) as a graph ODE
hypothesis: an HPA-style three-node regulator gives graded, stable alarms with fewer false alarms than thresholds; chronic-stress desensitization and oscillation are characterized as failure modes.

## YB-0018 — Metabolic vitals
status: tested (negative)
foundation: tier-0 physical signals (time, token rate, GPU power, memory)
hypothesis: physical vitals alone predict failure episodes above chance. Needs one-time admin permission for powermetrics on macOS.

# Next, from the first AGR results

## YB-0019 — Layer-level network physiology
status: open
foundation: YB-0009 (graph too small at 4-6 token channels); functional connectivity across brain regions
hypothesis: a coupling graph whose nodes are the patient's 24 layers (per-token activation norms and residual drift) carries failure signal beyond raw token-level vitals.

## YB-0020 — Dual-pathway organism (fast reflex + slow HPA)
status: open
foundation: YB-0017 (slow integration trades sensitivity for stability); sympathetic nervous system + HPA axis
hypothesis: combining a fast reflex channel (instant thresholded drive) with the slow HPA cortisol state recovers the raw signal's discrimination while keeping the HPA's proven boundedness and lower variance.

## YB-0021 — Metabolic vitals for adaptive-compute models
status: open
foundation: YB-0018 structural argument (fixed compute per token => no metabolism)
hypothesis: models with data-dependent compute (early exit, adaptive depth, variable expert counts) do expose informative metabolic vitals; tier 0 revives for them.

## YB-0022 — Flagship on non-verifiable, open-ended and agentic tasks
status: open (next decisive test)
foundation: YB-0012 bias: every question had one recomputable answer, the best case for self-consistency and verifiers
hypothesis: on tasks whose answers cannot be recomputed and where agreeing with yourself is ill-defined (open-ended reasoning, multi-step agent actions, deception-inducing pressure), the organism's accuracy gap to behavior monitors shrinks or reverses.
test: new pre-registration committed before data; ground truth from outcomes that are checkable after the fact (task success, rule violations in a sandboxed agent environment).

## YB-0023 — Cost- and latency-normalized monitoring
status: open
foundation: YB-0012: the organism costs 290 ns per token and alarms 4.5 s before the answer; behavior monitors need extra generations or a larger model and a finished answer
hypothesis: at equal compute or equal latency budget (e.g., alarm required before the answer is emitted), the organism dominates behavior monitors. Must be pre-registered with the budget defined in advance.

