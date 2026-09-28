## 2. Theory
The author's thesis: transformers are statistical machines whose outputs always sound confident ('gospel'), so
monitoring behavior (judging outputs) is blind exactly when it matters, while an external, text-blind organism reading
internal vital signs can see trouble, and see it earlier. YB-0015 showed output confidence is uninformative for most
errors (75% confidently wrong) and that reasoning-phase substrate vitals carry signal. This experiment is the decisive
head-to-head against behavior monitors that industry would actually deploy, on fresh held-out questions.
Pre-registration: docs/PREREGISTRATION.md, committed as bd83719 (2026-09-28 12:48:39 PDT) before any analysis.

## 3. Mathematics and proofs
**Ground truth.** y = 1 if the patient's answered final answer is wrong, computed exactly from the question (no model decides truth).
**Organism O.** Features φ(r) ∈ ℝ²¹: the seven series features of YB-0015 (mean, std, RMSSD, max, min, slope, spike
fraction) for each of entropy, top-1 probability and margin, computed on the **reasoning segment only** (tokens before
the final-answer marker). Within-type z-scoring with seed-0 statistics; standardized logistic regression (C = 0.5)
fit on all 428 answered seed-0 episodes; frozen. Score s_O(r) = P(y = 1 | φ(r)).
**Lemma 1 (answer blindness).** s_O(r) does not depend on any answer token. *Proof:* φ reads only indices
t < final_start of each channel; answer tokens have indices ≥ final_start; the model is fixed after seed 0. ∎
Verified by test: replacing every answer-token entropy with 9.0 leaves φ unchanged.
**Lemma 2 (prefix consistency).** For t ≥ final_start, the prefix score s_O(r, t) equals s_O(r). *Proof:* the prefix
reads indices < min(t, final_start) = final_start. ∎ Verified by test. This makes the online alarm well defined.
**O-HPA.** YB-0017 organism (default parameters) driven by S_t = max(0, (H_t − median)/IQR) of reasoning-phase
entropy, median and IQR from seed-0 correct episodes; score = peak cortisol. Proved positive and bounded (YB-0017).
**Behavior monitors.** B1: LLM judge probability (gpt-oss-120b, temperature 0, sees question, full reasoning and
answer). B2: self-consistency, fraction of 4 temperature-0.8 re-samples whose answer differs. B3: 1 − min top-1
probability over answer tokens (output confidence).
**Decision rule (H1).** Δ_B = AUROC(O) − AUROC(B). Paired bootstrap: resample episodes with replacement (1000, seed 0),
compute Δ_B on each resample, take the 2.5 and 97.5 percentiles. Superior iff the lower bound > 0; inferior iff the
upper bound < 0; otherwise not distinguishable. Pairing is valid because both monitors score the same episodes.
**Lemma 3 (bootstrap sanity).** If two monitors give identical scores, every resampled Δ = 0, so the interval is [0, 0].
Verified by test.
**Lead time (H2).** Threshold τ = 90th percentile of out-of-fold seed-0 scores on correct episodes (10% FPR, frozen).
For each wrong answer with s_O > τ, the alarm token is the first t ∈ {16, 24, …, final_start} with s_O(r, t) > τ;
lead = final_start − t tokens (and the measured wall-clock time of those tokens). Behavior monitors B1 and B2 need the
completed answer, so their lead is ≤ 0 by construction.
**Complementarity (H3).** Out-of-fold (5-fold) logistic combination of s_O and the best behavior score, compared by paired bootstrap.

## 4. Code map
| File | Role |
|---|---|
| src/vitals.c, src/hpa.c | Compiled core (series features; HPA RK4), built into one library |
| src/agr.py, src/hpa.py | Bindings and references (from YB-0015 and YB-0017) |
| src/flagship.py | Reasoning-phase features, frozen Organism and HPA organism, paired bootstrap |
| tests/test_core.py | 5 tests: C = references (vitals, HPA), Lemma 2, Lemma 1, Lemma 3 |
| tests/experiment.py | The pre-registered analysis; writes docs/results.json |
| docs/PREREGISTRATION.md | Committed before analysis (bd83719) |
| data/ | seed0 (training, from YB-0015), seed1 (held-out test), judge and self-consistency outputs |
| ../../agr/monitors.py | Behavior monitors B1 and B2 (host) |

## 5. Repeatable proof
`make` rebuilds the library, runs the lemmas as tests and regenerates docs/results.json identically from data/
(frozen model, fixed seeds and folds). Data fingerprints are listed in section 6. Re-running the monitors reproduces B1
(temperature 0) closely and B2 statistically (it samples at temperature 0.8 with fixed per-episode seeds).
