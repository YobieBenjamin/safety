# Research program: Autonomic Graph Regulation (AGR) for AI

## Thesis (author: Yobie Benjamin)
1. Transformers are statistical machines, not brains (established in *Garbage In, Gospel Out*).
2. Their outputs are always fluent, confident "gospel", whether or not the internals behind them are sound. So
   **watching outputs fails**: the outside looks the same either way, and behavior is not predictive.
3. Therefore safety must be engineered the way biology does it: continuous **internal vital signs** (the analogues of
   heart rate, HRV, respiration, cortisol) drive **autonomic regulation** and **instinct**, which a judgment layer turns
   into decisions, sometimes wrong, but early.
4. The whole system is represented and analyzed with **graph mathematics**.

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
