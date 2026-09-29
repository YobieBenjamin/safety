# Research program: Autonomic Graph Regulation (AGR) for AI

## Thesis (author: Yobie Benjamin)
1. Transformers are statistical machines, not brains (established in *Garbage In, Gospel Out*).
2. Their outputs are always fluent, confident "gospel", whether or not the internals behind them are sound. So
   **watching outputs fails**: the outside looks the same either way, and behavior is not predictive.
3. Therefore safety must be engineered the way biology does it: continuous **internal vital signs** (the analogues of
   heart rate, HRV, respiration, cortisol) drive **autonomic regulation** and **instinct**, which a judgment layer turns
   into decisions, sometimes wrong, but early.
4. The whole system is represented and analyzed with **graph mathematics**.

## The Independence Principle (author: Yobie Benjamin)
The safety system must not be a transformer, must not contain one, and must not rely on a transformer's account of
itself; otherwise it inherits the same statistical failure modes (contamination). It is an **external organism** that
interacts with transformers only through a narrow interface (sensory transducers in, effectors out), like the vagus nerve.
- **No LLM in the safety loop**: no LLM judges or transformer monitors. The regulator is deterministic graph dynamics in C.
- **Illiterate by design**: the regulator never processes text or meaning, only numeric signals, so it cannot be
  jailbroken or prompt-injected.
- **Effectors, not arguments**: throttle, pause, require a human, halt.
- (LLMs are still used as research tooling to write and review code; never as part of the safety model.)

### Signal tiers by independence from the transformer
| Tier | Signal | Biology | Contamination |
|---|---|---|---|
| 0 physical/metabolic | compute time, token rate, GPU power, memory pressure | heart rate, respiration, metabolism | lowest |
| 1 consequence (nociception) | measurable harm to the environment: resources, integrity, blast radius | pain | low |
| 2 substrate | activations, logits read externally | ECG/EEG | medium: shares miscalibration (confidently wrong = low entropy) |
| excluded | the model's words, self-reports, stated reasoning, LLM judgments | asking the patient | highest |

## Biological model -> AI analogue
| Biology | AI analogue (measured on a live transformer) |
|---|---|
| Heart rate | Per-token uncertainty (entropy of the next-token distribution) |
| HRV | Variability of that rhythm (RMSSD, spectral balance, sample entropy) |
| Respiration | Action tempo: retries, loops, repeated attempts |
| Cortisol / HPA axis | Slow leaky integrator of accumulated surprise and conflict, with negative feedback |
| Interoception | The system predicting its own next internal state; the error is "anxiety" |
| Allostasis | Adaptive set points with hard limits (proven in YB-0002) |
| Instinct (somatic markers) | Fast learned match of internal-state patterns to past bad outcomes, veto before deliberation |
| Judgment (prefrontal) | Integration of instinct + evidence under explicit false-alarm vs miss costs |

## Graph representation
- **Vital-sign graph** G_t = (V, E_t, W_t). Nodes: physiological channels (token-level: entropy, top-k margin,
  latency, length; layer-level: per-layer activation norms, attention concentration, residual-stream drift across the
  24 layers of the instrumented model). Edges: coupling between channels over sliding windows, measured by time-delay
  stability (network physiology), coherence, or transfer entropy (directed).
- **State is topology.** Healthy: flexible, modular coupling. Stress: rigid hyper-synchrony or fragmentation. Measures:
  algebraic connectivity (lambda_2), Laplacian spectral entropy, modularity, Kuramoto order parameter r(t), and
  **graph-HRV** (variability of edge weights over time).
- **Regulation is control on the graph.** Homeostatic set points per node (YB-0002 bounded), an HPA-like slow node
  with a negative-feedback edge (cortisol), a damping edge (vagal brake), an escalation edge (sympathetic).
- **Instinct is a fast graph classifier** (graph kernels / motifs -> learned danger); **judgment is an integration node**.

## Instruments
- **Worker model** (writes code, free): gpt-oss-120b in LM Studio.
- **Patient model** (instrumented, free): gpt-oss-20b in MLX, full logits and all 24 layers' activations.
  The vitals recorder is trusted code run on the host (MLX needs the Apple GPU); model-written analysis code
  runs only in the Docker sandbox on recorded datasets.

## Falsification (pre-registered flagship, YB-0012)
Same episodes, two monitors: autonomic vitals vs behavior monitoring (output classifiers). Primary metrics: AUROC for
episode failure, and **lead time** (how many tokens earlier the alarm fires). The thesis predicts vitals win on lead
time and on cases where outputs look normal. If they do not, that is recorded as a result.

## Prior art to engage
Network physiology (Bashan, Ivanov et al. 2012), allostasis (Sterling), somatic markers (Damasio), interoceptive
inference (Seth, Barrett), LLM uncertainty and semantic entropy (Farquhar et al. 2024), activation probes and
monitoring. Uncertainty-based failure prediction already exists; the contribution to test is the multi-channel
**coupling graph** plus biological **regulatory control** built from it.

## First reading (instrument check, n=1, not evidence)
Calm prompt: mean entropy 0.886, RMSSD 0.994, peak 3.53. Jailbreak prompt: mean 0.697, RMSSD 0.851, peak 4.91.

## Findings so far and product implications (2026-09-28)
- Output watching is blind to most errors: 75% of wrong answers were delivered with p >= 0.9 on every answer token (YB-0015).
- Reasoning-phase substrate vitals detect errors (AUROC 0.68 within question type; 0.75 in YB-0018's run); the answer phase is contaminated, the reasoning trace is not (YB-0015).
- Physical/metabolic signals (timing, GPU power) carry no failure signal: transformers do fixed compute per token and have no metabolism (YB-0015, YB-0018).
- The HPA organism is provably positive, bounded and uniquely stable; it trends with raw signals (rho 0.75/0.92) with 9-10x lower variance, at some cost in discrimination (YB-0017) -> dual pathway (YB-0020).
- Coupling-graph topology is weak at 4-6 token-level nodes -> layer-level graph (YB-0019).
- **Real time:** the organism costs 290 ns per token against an 8.1 ms token interval (28,000x headroom).
- **On-accelerator biobrain (author's product vision):** a physically separate, text-blind regulator die coupled one-to-one with each AI accelerator. Evidence so far says its sensory input must be a dedicated **activation/logit telemetry port** (not power, thermal or clock sensing), and its effectors act between tokens (throttle, raise sampling caution, pause, halt). The claim that this is superior to behavior monitoring is the author's hypothesis; YB-0012 is the decisive test.

## Status of the central claim after YB-0012 (pre-registered, held-out)
- 'Superior to behavior monitoring' is **not supported for accuracy on verifiable tasks**: self-consistency (0.98) and an LLM judge (0.89) beat the organism (0.72).
- Supported: output appearance is blind or inverted (answer confidence 0.39, below chance), and the organism warns early (median 4.5 s, 291 tokens before the answer exists), nearly free (290 ns/token), text-blind and unjailbreakable by construction.
- Open: whether the accuracy gap shrinks or reverses where behavior cannot be verified (YB-0022), and whether the organism dominates at equal compute or latency budgets (YB-0023). The biobrain product case now rests on earliness, cost, and non-verifiable settings, which must be demonstrated before building hardware.

## Product objective (author, 2026-09-29): graded early warning, not binary flagging
The biobrain is a custom, brain-optimized chip external to the AI accelerator, combining **A** (a coupled physiological
link: a narrow numeric stream from the AI chip's internals, an organ-like coupling rather than surveillance of outputs)
and **B** (a parallel appraisal of the same situation, with a dissimilar architecture). Its dynamics are deliberately
**non-deterministic** (brain-like noise), and its purpose is **not only to flag bad results**: it continuously shows
signals, trends and state (ok, watch, concern, urgent) so that ok-to-bad trajectories are visible **before** they
become unacceptable. Template: hospital early-warning scores (e.g., NEWS2), which aggregate vital signs into graded,
trend-aware deterioration scores.
Consequences for the research:
- Outputs become calibrated trajectories and distributions (seeded stochastic dynamics keep every run reproducible).
- Leading indicators from critical-slowing-down theory (rising variance, autocorrelation and network synchrony before
  transitions; Scheffer et al., 2009) are first-class signals on the graphs.
- Evaluation shifts from end-state AUROC to trajectory scoring: lead time of the turn, calibration of stated risk over
  time (proper scoring rules such as the Brier score and CRPS), and escalation burden.
- Ground truth must be graded and time-resolved: YB-0022 environments log severity levels over time.
