**Revision 2** (2026-10-22 20:19) on sonnet: 7 turns, estimated $1.2939, acceptance `python3 -m pytest -q observer/tests && python3 agr/bench/tier0_vitals.py --smoke`: **pass**. The gate reviews the branch again.

Agent summary:

Revision 2 is committed (f1654cb) and the acceptance command now passes. I ran it once after the changes: 33 observer tests, 10 experiment tests (run from inside the smoke), then smoke `ok`.

When I picked this up, `project`, `cap_alarm` and the updated tests and docs were already sitting uncommitted in the worktree. I reviewed and kept them, and committed them along with my own changes.

**What changed**
- **Blocking: acceptance failure.** Smoke called `V.project`, which didn't exist. `project()` now exists in `vitals_tier0.py` and is applied in `recordings.load_seed`, so text, entropy, p_top1, margin, toks, final and truth are dropped at load. The tier-0 restriction is therefore enforced in the pipeline, and smoke and `test_project_drops_content` check it.
- **Blocking: the unit tests were never run by acceptance.** Smoke now runs `tests/test_core.py` through pytest, so the acceptance command covers them.
- **Tied baselines.** `cap_alarm` splits ties at the threshold, so the length and type controls can reach the 10% cap. In the regenerated dry run they catch 8 and 11, where before both caught 0. It is used in `evaluate`, `boot_diff` and the equal-false-alarm count. The baselines are no longer handicapped to zero.
- **Seed 38.** `PREREGISTRATION.md` and `recordings.py` now say that no seed is fresh across the program: 27–38 were YB-0051 test seeds. "Fresh" means held out from this experiment's model selection, and the run is corroboration.
- **Wrong-answer counts.** The pre-registration no longer states "about 43 / 500 / 0.2" as numbers. It records that `inspect_seeds.py` was run once as a descriptive look at labels, with no model fitted or score computed.
- **Power wording.** The power claim now reads "not recorded in the analysed fields", not "null in every recording". Only the seeds I inspected showed null.
- **README.** It no longer says "pre-registered"; it says not yet timestamped.
- **Dry run.** `docs/dryrun.json` is regenerated. It shows the pipeline runs, not that the regulator works.

**Not changed**
- **Timestamp proofs.** `scripts/timestamp_prereg.sh` needs network, which I don't have. That step stays local, before `--run`.
- **"Follows YB-0035 corrected.py".** I haven't added a comparison test, because that file is skip-worktree and outside what I may touch. The tie-aware cap is a documented departure from it.
- **The "acceptance.log shows a pass" claim.** That was the launcher's log of the earlier tree, which called an undefined `project`. It was stale, and I can't explain it further.

## Commit messages
- YB-0055: Makefile with test and experiment targets so CI's make verify reaches it; plain-python test runner (CI has no pytest)

- YB-0055 (#4): project() at the load boundary, tie-aware 10 percent cap, unit tests inside the smoke, honest status
Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Agent: wave 2, issue #4 (revision 2)

- Revision 1: work left uncommitted by the agent, committed by the launcher (#4)
Agent: wave 2, issue #4 (revision 1, launcher commit)

- YB-0055 (#4): tier-0 vitals regulator, pre-registration, dry run and smoke test
Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Agent: wave 2, issue #4

