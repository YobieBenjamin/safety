# YB-0045 · Powered replication of the in-time comparison with the LLM judge

**Status:** pre-registered (docs/PREREGISTRATION.md, analysis code, dry run docs/dryrun.json) before any test recording. Results pending.
**Reproduce:** SANDBOX_MEM=16g SANDBOX_TIMEOUT=21600 sandbox/run.sh algorithms/YB-0045-powered-replication all (dry run: DRY_RUN=1).

Training data matched to YB-0035 (10 seeds, about 5,350 answered); three fresh test seeds (9, 13, 14; about 120 wrong answers); false-alarm population identical in prose and code (all answered test episodes; verified in the dry run). Primary: regulator minus LLM judge, in-time recall, lower 95% bound > 0. Chain: agr/yb0045_chain.sh.
