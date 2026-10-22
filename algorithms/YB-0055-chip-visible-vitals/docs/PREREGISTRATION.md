# YB-0055 pre-registration: chip-visible vitals

**Status:** code and dry run written before any test seed is scored. Timestamp with `scripts/timestamp_prereg.sh
algorithms/YB-0055-chip-visible-vitals/docs/PREREGISTRATION.md` and commit the proofs before running `python3 agr/bench/tier0_vitals.py --run`.

## Question
Can a regulator restricted to signals a rack-tier governor reads with no host cooperation catch wrong answers before commitment, at a
matched 10 percent false-alarm rate, better than the length and question-type baselines?

## Tier-0 view
Allowed: the per-token arrival latencies of the stream (token rate, per-token latency, elapsed time) and the token count (bytes are a
function of it at this tier). Board power is in the tier but is null in every existing recording, so it cannot be tested here and is
reported as such; the YB-0018 prior (power carries nothing) is therefore neither confirmed nor contradicted by this run.
Cycles are not recorded; wall time stands in for them. Dropped before any feature: text, entropy, p_top1, margin, toks, final, truth,
correct. `final_start`, `correct`, `answered` and `cat` are used only to score and to build the controls, never as features.

## Features (at checkpoint t in 48, 96, 192, 384, t before the final answer starts; each uses latency[:t] only)
log time to first token; mean and sd of log decode latency; log of recent (last 16 tokens) over prefix mean latency; slope of log
latency; fraction of tokens slower than 1.5 times the median; log of max over median latency; log elapsed time.
Model: pooled ridge logistic regression, features standardised per checkpoint on derivation rows, one intercept per checkpoint.
Ridge strength chosen from 1, 10, 100 by 5-fold episode-grouped cross-validated AUROC on derivation only.
Ablations: `level` (TTFT, mean, sd, elapsed) and `shape` (recent, slope, stall, max).

## Data
Derivation: seeds 2 to 14 (the recordings of YB-0033 to YB-0045). **Primary test: seed 38**, scored once. **Secondary (powered
check, same frozen model, reported separately, never changes the primary verdict): seeds 27 to 37.** Seeds 15 to 26 are unused.

## Real-time protocol (YB-0035 definitions, unchanged)
A check at t is in time if elapsed(t) + 0.005 s is at most the time the final answer starts; an episode's score is the maximum over its in-time
checks (-inf if none). Population: all answered test episodes; episodes finishing before t = 48 stay in and can never be alarmed. The
threshold per monitor is the tightest with at most 10 percent of all correct answered test episodes alarmed. Baselines: length (score t,
cost 0) and question type (derivation wrong-rate of the category, cost 0).

## Hypothesis and decision
H: vitals minus length and vitals minus type, in-time recall at the matched 10 percent rate (threshold-resampling bootstrap, 1,000
resamples, 95 percent CI). **Supported iff both lower bounds exceed 0 on the primary seed.** Otherwise not supported.
Secondary: same contrasts on seeds 27 to 37 pooled; vitals minus level and shape ablations; caught counts at equal false alarms among
monitorable episodes; frozen derivation threshold (out-of-fold, 10 percent cap); per-checkpoint AUROC of vitals and type with CIs.

## Power
Primary seed has about 43 wrong answers, so a 95 percent half-width of roughly 0.2 on recall differences; a modest advantage
will not be resolved on one seed. The pooled secondary has about 500 wrong answers and is the informative check; if it is clearly positive
while the primary is not, that is reported as underpowered primary, not as support.

## Pre-declared consequences
- Supported: tier-0 token rate and latency carry an in-time early warning beyond length and type; the chip may use them as a coarse alarm.
- Not supported: the chip's own sensing serves enforcement and accountability only; every early warning arrives as a signed verdict from
  an observer with substrate access, and the chip design says so.
- No re-run of the test analysis except after a crash with no output seen (logged as a deviation).
