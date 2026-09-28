# Project history and decisions

A one-person AI-safety research program run like mining: many hypotheses tried, each one coded in C + Python,
compiled, tested against baselines, and documented four ways (plain English, technical, mathematical, code).
Foundations: the book *Garbage In, Gospel Out*, graph theory, brain science and biological behavior.
Every attempt is kept, including failures (see LEDGER.md and archive/).

## 2026-09-28

1. **Charter and first block (YB-0001).** Built in a cloud container: per-input effective-connectivity graph +
   normalized-Laplacian heat trace as an OOD/adversarial monitor, plus a homeostatic baseline with a drift budget.
   Spectral detector: negative result (AUROC 0.64-0.78, below MSP/energy/Mahalanobis). Drift budget: positive
   (5/5 slow poisoning caught, 0/5 false alarms).
2. **Repository.** Private permanent repo YobieBenjamin/safety. First upload through the browser with SHA-256
   verification of every file; GitHub rejects dotfiles and `.github/` via the uploader, so those used the editor.
3. **YB-0002 Bounded Homeostatic Wrapper.** Proved confinement theorems T1-T3; worst-case attacker drags an
   unbounded monitor 768-5954 Mahalanobis units with zero flags, BHW caps it at B + eta*tau. Energy + BHW:
   detection 1.1% -> 43% with 0/10 false alarms. Closed-form budget calibration (C1/C2) fails in 64-D -> YB-0007.
4. **Moved to the Mac.** gh CLI logged in as YobieBenjamin alongside an existing account; clone at ~/safety with
   .venv; macOS 27 SDK linker quirk found and auto-handled; results reproduce bit-for-bit across the cloud
   container, macOS, and the Linux sandbox.
5. **Security sandbox.** All model-written code runs only in a locked-down Docker container (no network, no
   capabilities, non-root, read-only root, CPU/memory/process caps, timeout). Adversarial probe: every escape
   blocked, planted fake secrets never reached it. Miner and publish.sh fail closed. Found and fixed: an
   `a && b` under `set -e` that could have skipped verification; Mac-built .so files leaking into Linux builds.
6. **Parallel session.** Another Claude session in the same working tree added Miner v2 (prompt caching,
   cheap-model triage), a GitHub-hosted scheduled miner (`.github/workflows/mine.yml`, inert until an
   ANTHROPIC_API_KEY repo secret exists), and CI fixes for Linux runners (caller uid, CPU clamp). History stayed
   linear; nothing was overwritten.
7. **Local-first hybrid orchestrator (`./mine`).** Docker raised to 32 GB / 12 CPUs; LM Studio gpt-oss-120b as the
   local model. First fully local attempt at YB-0003 (0 cloud tokens) failed verification: the local model
   wrote a good design and all files but hallucinated an API, left a placeholder stub overriding a real function,
   and mis-derived its own closed form (Gini of one active unit among n is (n-1)/n, not (n-1)/(2n-1)).
   Fixes: one file per call, fixed Makefile template, README written after real results, real mlp.py source in
   every prompt, broader repair scope, resume mode, a free static quality gate, and cloud routing for the
   math-heavy C core and algorithm module. Also fixed an orchestrator bug that truncated HYPOTHESES.md.
8. **Complete archive for migration.** archive/2026-09-28 (run logs, raw model outputs, failed attempts,
   benchmarks), requirements.txt, bootstrap.sh, docs/MACHINE_SETUP.md, this file. Full clone at ~/Desktop/SAFETY.

## Open items
- Anthropic API key in Keychain, then a supervised pilot (`./mine --max 1`) to measure real cloud-token cost per algorithm.
- Decide the single miner of record: local orchestrator (`./mine`) vs GitHub `mine.yml`; running both would compete for hypotheses.
- Ingest the book so hypotheses derive from its chapters (not yet provided).
- Open hypotheses: YB-0003 to YB-0007. Novelty claims still need a systematic literature search.

## Lessons
- Keep negative results; they redirect the search (YB-0001 -> YB-0002 -> YB-0007).
- Local models: strong at design prose and mechanical fixes, unreliable at novel math code; never let a model verify its own theorems.
- Deterministic scaffolding (templates, static gates, sandbox) beats more model calls.
- Fail closed everywhere; test the failure path, not just the success path.
