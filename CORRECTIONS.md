# Corrections log

**Outcome of the deep debug (2026-09-30).** All critical findings were independently verified. The real-time result
was re-run end to end under a corrected protocol (YB-0035, committed before its test data existed): the regulator beats
both the LLM judge and the length control on the fresh seed-7 test set and on seeds 5 and 6 (pooled 1,610 episodes:
+32 points vs each, 95% CI lower bounds +19 and +20), at <= 10% false alarms. Boundary: when never-answered episodes
count as failures, the regulator is no better than length alone. Pre-YB-0033 accuracy claims did not beat
question-type or length baselines (F16). Terminology from here on follows docs/GLOSSARY.md (e.g. regulator = organism).

Every error found in this repository, who found it, how it was verified, and how it was resolved. Nothing is silently
edited: a correction changes the affected document **and** is recorded here. Sources: the independent audit
(`archive/audit/independent_audit_2026-09-30.md`, a separate read-only Claude Code session at commit fc575cf), our
own verification (Phase A of the deep debug), and our own findings (marked *self*).
Resolution codes: **FIXED-YB-0035** (corrected in the re-run experiment), **RETRACT** (claim withdrawn), **REWORD**
(claim qualified), **ARTIFACT** (missing script or data added), **DOC** (documentation fix), **PROCESS**, **OPEN (backlog)**.

## Critical
| ID | Finding | Verified | Resolution |
|---|---|---|---|
| F1 | YB-0012 'alarms 4.5 s before the answer, 100% of detections': the online alarm fires on 89.3% of correct answers at the first check (93.9% at any check); the lead is reasoning length | Phase A rerun (exact) | RETRACT the earliness claim; superseded by matched-false-alarm races (YB-0033/34/35) |
| F2 | YB-0019 'warned 4.65 s before answering, every time': same mechanism, 56.1% false alarms | auditor rerun | RETRACT, as F1 |
| F3 | YB-0015 'reasoning phase detects errors; the reasoning trace is not contaminated': features were whole generation + answer segment; no reasoning-only feature existed | Phase A (code) | RETRACT the claim; OPEN: re-test on the reasoning segment only (backlog) |

## Major
| ID | Finding | Verified | Resolution |
|---|---|---|---|
| F4 | Layer tap stored each token's reading one step late (prompt pass first); stale, not future | Phase A: fresh forward pass (lag-1 error 0.01, aligned error 0.4-3.6) | FIXED-YB-0035: tap fixed + permanent test (agr/test_layertap_alignment.py); seeds 2-6 resynchronized (shift verified, 0.013 vs 0.5-0.9 SD); result confirmed on corrected data |
| F5 | YB-0033/34 excluded never-answered episodes (62/600, 63/600) without disclosure | auditor | FIXED-YB-0035: pre-declared sensitivity analysis; DOC disclosure in YB-0033/34 |
| F6 | YB-0034 undocumented; pre-registered pooled estimate R3 never computed | auditor, self | FIXED-YB-0035 (pooled 5+6+7); DOC: YB-0034 README and LEDGER row |
| F7 | 'EUREKA (confirmed robust)', 'first leak-free' overstated | auditor | REWORD: 'primary criterion met (YB-0033), replicated (YB-0034), confirmed under the corrected protocol (YB-0035); first such result in this program' |
| F8 | Organism false-alarm rate 10.12% > 10% cap | auditor | FIXED-YB-0035 (tightest threshold with <= 10%) |
| F9 | False alarms among monitorable episodes unreported (16.6%) | auditor | FIXED-YB-0035 (reported) |
| F10 | Bootstrap CIs ignored threshold uncertainty | auditor | FIXED-YB-0035 (all episodes resampled, thresholds re-set) |
| F11 | Analysis code committed with results, not before | auditor | PROCESS: YB-0035 code + dry run committed before seed 7 (b6c795b); DOC disclosure for earlier experiments |
| F12 | YB-0019 '≈302 features' (actual 314); unregistered metric and extrapolation change | auditor, self | DOC: count corrected; deviations listed |
| F13 | YB-0030 called pre-registered (4 minutes before results, on thrice-used data); V6 changed | auditor | REWORD: retrospective; DOC the V6 change |
| F15 | YB-0031 H5 'failure to settle confirmed' driven by one question type | auditor rerun | REWORD: weekday-specific; within-type tests reported |
| F16 | Length and question-type baselines match or beat pre-YB-0033 organisms | auditor rerun | DOC + ARTIFACT (archive/audit/artifacts/): seed 1 type 0.764 and length 0.796 exceed YB-0012 (0.72), YB-0019 (0.765), YB-0030 (0.725); YB-0031 0.89 exceeds type 0.80 and length 0.73 |
| F17 | YB-0009 topology features include n_windows (a length proxy) | auditor rerun | OPEN (backlog) rerun without it; DOC |
| F18 | YB-0018 'substrate' entropy includes answer tokens; Proposition 2 false | auditor | RETRACT Proposition 2; OPEN (backlog) re-window |
| F19 | YB-0017 'variance 9-10x lower' is a CV ratio (≈3.7x above rest); drive correlates with length | auditor rerun | REWORD; DOC |
| F20 | '290 ns/token' attributed to competing organisms (they cost 2-4 ms) | auditor | REWORD + ARTIFACT (timing script) |
| F21 | YB-0032 length control not reproducible (0.578 does not reproduce) | auditor, self | ARTIFACT: archive/audit/artifacts/baselines_and_breakdowns.py reproduces 0.773, 15/46 and 0.578, 11/46 (our definition: derivation-correct percentile by type) |
| F22 | YB-0002 detection claims at unmatched false-positive rates | auditor rerun | REWORD; OPEN (backlog) matched comparison |
| F23 | RESEARCH_PROGRAM: 'behavior is not predictive', 'unjailbreakable by construction' | auditor | REWORD: update through YB-0035; 'text-blind' kept, 'unjailbreakable' dropped (untested) |
| F24 | Novelty claims without related work (hidden-state error prediction literature) | auditor | DOC: related-work section |

## Minor
| ID | Finding | Resolution |
|---|---|---|
| F14 | YB-0031 H4 used a test-set threshold; 'silent slip' defined by question type only | DOC deviation; per-category false alarms reported |
| F25 | 'Below chance' confidence claim cited with a CI that includes 0.5 | REWORD: cite YB-0031 0.366 [0.304, 0.433] |
| F26 | 'Perfectly ordered' levels rest on groups of 17, 8, 2 | REWORD |
| F27 | 'Better than the judge at every checkpoint' (no CIs; reverses at t=384 in YB-0034) | REWORD; CIs OPEN (backlog) |
| F28 | Lead time at best, not first, crossing | FIXED-YB-0035 |
| F29 | Live compute timing made in-time status non-deterministic | FIXED-YB-0035 (fixed 5 ms cost) |
| F30 | Judge prefixes re-tokenized from text | FIXED-YB-0035 (exact token ids, seed 7) |
| F31 | Compute ratios exclude tap cost; wall-clock not compute | REWORD |
| F32-F34 | YB-0001/0002/0017 theorem wording and test coverage | REWORD; tests OPEN (backlog) |
| F35 | YB-0019 Proposition 3 test does not check the exact statement; features numerically fragile | DOC; OPEN (backlog) exact-case test and sensitivity |
| F36 | Missing LEDGER rows (YB-0003, 0022, 0034); YB-0022 test only greps a file; wrong checkpoints in HYPOTHESES | DOC + PROCESS |
| F37 | '9x more data' (10x); V8 points dropped from explanations; methodology 0-21 vs 0-24 | DOC; code fix OPEN (backlog) |
| F38 | '6x larger judge' (5.6x total, 1.4x active parameters) | REWORD |

## Found by us (self)
| ID | Finding | Resolution |
|---|---|---|
| S1 (F39) | Greedy generation is deterministic within a session but diverged across sessions for ~40% of episodes (likely GPU sharing during the seed-2 recording) | REWORD 'token-reproducible' claims; PROCESS: record alone; log environment |
| S2 | '720/720 token-identical' was asserted before being checked (true when later checked: 480/480 + 240/240) | PROCESS: no verification claim before the check |
| S3 | Per-type 'struggle 10/12 vs slips 0/9' (YB-0012) computed ad hoc, never saved | ARTIFACT: same script reproduces 10/12 struggle and 0/9 slips |
| S4 | Pre-registration folders copied with full Makefiles broke CI (YB-0034); local checks did not mirror CI | PROCESS: YB-0035 experiment exits cleanly when data is absent (done); local check to mirror CI (Phase D) |
| S5 | Blog draft repeats F1, F3, F23, F38 and 'every experiment is public' | Phase E: rewrite from the corrected record |
