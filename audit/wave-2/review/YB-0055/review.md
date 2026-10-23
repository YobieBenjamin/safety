## Review of `exp/yb-0055`: **revise**

Verifier: clean; model review on ?: 2 blocking, 8 warnings, 6 unsupported claim(s) of 18; estimated $0.82, 5 turns.

### Reviewer's summary

The work is sound as code and the status text is mostly honest, but the pre-registration is not ready to timestamp.
- The tie-aware random cap (cap_alarm) changes the decision rule. PREREGISTRATION.md says "YB-0035 definitions, unchanged" and never mentions it.
- The power claim ("not recorded in the analysed fields") is not shown anywhere. project() keeps `power`, and no artifact shows it is null.
- The Power paragraph's figures ("tens", "order 0.2", "order of magnitude") are not computed. They come from a peek at test-seed labels.
- Acceptance runs only synthetic data. The real-recordings path (load_seed, --run) is never executed. The smoke silently skips the unit tests if the file is missing.
- Timestamping and results.json are not done. The README says so, and the brief makes them local steps.
- Question: the "CI make verify" claim has no `verify` target or CI file in the diff to support it.

### Reviewer findings

- [block] protocol at `algorithms/YB-0055-chip-visible-vitals/docs/PREREGISTRATION.md:41`: Header says "YB-0035 definitions, unchanged", and the section describes a strict 10 percent threshold. The code instead splits the tie at the threshold with a per-episode random draw (vitals_tier0.py:108-133, used by evaluate, boot_diff and the equal-FPR count). That is a change to the decision rule. It sets the controls' recall (dryrun: length 8, type 11 against 0 under the strict rule) and so the primary verdict. It is documented only in the code docstring and the agent summary, not in the document that is about to be timestamped. Pre-register the tie rule, the seeds used and its effect on the baselines before the timestamp.
- [block] unsupported_claim at `algorithms/YB-0055-chip-visible-vitals/docs/PREREGISTRATION.md:17`: Claims board power is "not recorded in the analysed fields, so it cannot be tested here". The same text appears in the vitals_tier0.py:10 docstring, analysis.py:37 (a hard-coded string literal, not computed) and dryrun.json:25. But CHIP_FIELDS includes 'power' (vitals_tier0.py:19) and project() passes it through, so it is in the analysed fields. No committed artifact shows it is null: inspect_seeds.py output is not committed, and the agent says it saw null only on the seeds it inspected. Not found. Either show the evidence or reword to "not used as a feature". The brief calls the power prior part of the hypothesis, so this must not be asserted without evidence.
- [warn] unsupported_claim at `algorithms/YB-0055-chip-visible-vitals/docs/PREREGISTRATION.md:56`: The Power section says the primary seed has "on the order of tens of wrong answers", the half-width is "order 0.2" and the secondary has "an order of magnitude more". No test or artifact computes any of these. They can only come from the descriptive peek at test-seed labels (inspect_seeds.py), yet the Status (lines 5-8) says the design does not depend on those counts. Line 54 also says the counts "are measured ... at registration" (future), while the Status says they were already looked at. Remove the figures or compute them from derivation seeds only.
- [warn] test_integrity at `agr/bench/tier0_vitals.py:61`: The unit tests run inside the smoke only `if os.path.exists(tp)`. If the file is missing (the sparse-checkout case _load exists for), the smoke prints ok without running them. Line 58 (`caught >= 0`) is always true. Nothing in the acceptance command exercises recordings.load_seed, the HOME map, raw_bytes or run(). Only synthetic episodes are used, and the dry-run AUROC of 1.0 comes from signal built into synth(). The 'project at the load boundary' claim therefore rests on code reading plus a test of project() on a hand-built dict.
- [warn] correctness at `algorithms/YB-0055-chip-visible-vitals/src/recordings.py:29`: project() uses r.get over ALLOWED, so a recording that lacks latency, final_start, answered, correct or cat becomes None silently and fails later, or wrongly. No artifact shows the real recordings carry these field names. The inspect_seeds output is not committed. The one-shot --run path is untested and would spend the single permitted run if it crashes after the load.
- [warn] unsupported_claim at `algorithms/YB-0055-chip-visible-vitals/docs/PREREGISTRATION.md:33`: "seeds 2 to 14 (the recordings of YB-0033 to YB-0045)" (same in tier0_vitals.py:36). The seed-to-directory map (recordings.py:16-17) assigns seeds 2-14 only to YB-0042 and YB-0045. YB-0033 does not appear. Not found.
- [warn] unsupported_claim at `algorithms/YB-0055-chip-visible-vitals/docs/PREREGISTRATION.md:16`: "the token count (bytes are a function of it at this tier)" and "cycles are not recorded": there is no source or artifact for either. Token count is not in CHIP_FIELDS (it is len(latency)), and nothing shows which fields the recordings hold.
- [warn] protocol at `agr/bench/tier0_vitals.py:37`: The brief asks for a test on a fresh seed. PRIMARY=38 is a YB-0051 test seed, and 27-37 likewise. This is disclosed and redefined as "held out from this experiment's selection". The run is corroboration, not a fresh test. The brief also requires pre-registration with the timestamp script. That step is not done (README.md:3, PREREGISTRATION.md:8), and docs/results.json is absent. Both are honestly flagged. The verdict text must carry the corroboration caveat.
- [warn] unsupported_claim at `algorithms/YB-0055-chip-visible-vitals/docs/dryrun.json:89`: The committed artifact reports H_supported true, AUROC 1.0 and 86/93 caught. These come from synthetic data whose signal is built into synth() (vitals_tier0.py:185-194). It carries dry_run:true, but no field or note says the numbers are not evidence. Nothing checks the file matches the code's output, so it can drift.
- [warn] unsupported_claim at `algorithms/YB-0055-chip-visible-vitals/Makefile:10`: The commit message says the Makefile lets "CI's make verify reach it", but the Makefile has no `verify` target (targets: all, test, experiment, smoke, clean) and no CI configuration is in the diff. The comment on line 5 gives "about 10 s" for the dry run with no measurement. Not found.

### Claims

- supported (summary): The acceptance command passes (33 observer tests, 10 experiment tests, smoke ok) (evidence: verify.json acceptance exit 0 with 33 passed; acceptance.log shows 10 passed and the smoke ok line)
- supported (summary): project() exists and is applied in recordings.load_seed, so text, entropy, p_top1, margin, toks, final and truth are dropped at load (evidence: vitals_tier0.py:30 (def project, ALLOWED); recordings.py:29-31 calls project; test_project_drops_content. The load_seed path itself is never run by any test.)
- supported (summary): The tier-0 restriction is enforced in the pipeline and smoke and test_project_drops_content check it (evidence: Smoke step 3 and test_core.py:test_project_drops_content test project() on a constructed dict; load_seed is not exercised on real data.)
- supported (summary): Smoke now runs tests/test_core.py through pytest so acceptance covers them (evidence: tier0_vitals.py:61-63; acceptance.log '10 passed'. Guarded by os.path.exists, so it can be skipped silently.)
- supported (summary): cap_alarm splits ties so length and type controls reach the cap; they now catch 8 and 11 (evidence: vitals_tier0.py:108-133; test_tied_control_reaches_cap; dryrun.json:wh lengths 8 and 11 (length caught 8, type caught 11). The 'before: 0' figure is not in the diff.)
- NOT SUPPORTED (document): PREREGISTRATION: real-time protocol is YB-0035 definitions, unchanged (evidence: Contradicted by the tie-aware random cap in vitals_tier0.py:108-133, which is not described in the document.)
- NOT SUPPORTED (document): Board power is not recorded in the analysed fields so cannot be tested (evidence: No artifact shows null power. CHIP_FIELDS includes 'power' and project() keeps it.)
- NOT SUPPORTED (document): Seeds 2-14 are the recordings of YB-0033 to YB-0045 (evidence: recordings.py HOME maps 2-14 only to YB-0042 and YB-0045; YB-0033 not found.)
- NOT SUPPORTED (document): Primary seed carries tens of wrong answers; half-width order 0.2; secondary an order of magnitude more (evidence: No computation or committed artifact. Derives from the label peek.)
- supported (document): No seed is fresh across the program; 27-38 were YB-0051 test seeds; the run is corroboration (evidence: recordings.py:14-17 HOME map and PREREGISTRATION.md lines 35-39)
- supported (document): inspect_seeds.py was run once as a descriptive look only, fitting no model and computing no score (evidence: inspect_seeds.py body only loads and prints. 'Run once' is a process statement and cannot be checked from the diff.)
- supported (code): Features use only latency[:t] (no future information) (evidence: features() slices lat[:t]; test_features_use_prefix_only and smoke step 2)
- NOT SUPPORTED (document): Bytes are a function of token count at this tier; cycles are not recorded (evidence: No source or artifact)
- supported (code): cap_alarm's false-alarm rate is floor(cap*n)/n, at most the cap, for every seed (evidence: test_cap_alarm_respects_cap over n in (7,20,55,100,123) and four seeds; smoke asserts fpr <= CAP)
- supported (summary): docs/dryrun.json is regenerated and shows the pipeline runs, not that the regulator works (evidence: dry() in tier0_vitals.py:67 writes it from synthetic data; dry_run:true)
- supported (summary): PREREGISTRATION no longer states the 43/500/0.2 counts and the README no longer says pre-registered (evidence: Absent from the current files, but the removal itself is not in the diff (all files are new). The Power section still gives vague count claims.)
- NOT SUPPORTED (commit): Makefile lets CI's make verify reach the experiment (evidence: No verify target in Makefile:10; no CI file in the diff)
- NOT SUPPORTED (code): Statistics follow YB-0035 corrected.py (evidence: vitals_tier0.py docstring; the source file is not readable or compared by any test, and the tie rule is a stated departure)

### suite in a clean checkout: exit 0

```
============================= test session starts ==============================
platform darwin -- Python 3.12.15, pytest-9.1.1, pluggy-1.7.0
rootdir: /private/var/folders/30/33qb062d34q5p1j5tycqcyww0000gn/T/verify-cw27889v/observer
configfile: pyproject.toml
collected 33 items

observer/tests/test_contract.py .......                                  [ 21%]
observer/tests/test_signals.py ..........................                [100%]

============================== 33 passed in 0.08s ==============================

```

### acceptance in a clean checkout: exit 0

```
.................................                                        [100%]
33 passed in 0.03s
{"smoke": "ok", "vitals_caught": 20, "length_caught": 3, "wrong": 20, "fpr_full": 0.1}

```
