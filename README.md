# AI Safety Algorithm Mine

Net-new AI safety algorithms derived from graph theory, brain science and biological behavior, grounded in *Garbage In, Gospel Out*. Every entry is **coded, compiled, tested against baselines, and documented four ways**: plain English, technical, mathematical, and code. Negative results are kept in the ledger, because a failed hypothesis is information that stops the next run from re-mining it.

```bash
make all                     # compile + test + evaluate every algorithm
./publish.sh                 # verify, commit, push to github.com/YobieBenjamin/safety
python3 miner/mine.py        # agents mine the backlog, then propose new hypotheses, within a token budget
python3 miner/test_miner.py  # offline end-to-end miner test against a mock API (no tokens)
```

| Path | Purpose |
|---|---|
| `algorithms/YB-XXXX-*/` | One self-contained algorithm: `src/` (C core + Python), `tests/`, `docs/results.json`, `README.md` |
| `LEDGER.md` | Every attempt and its result, including failures |
| `HYPOTHESES.md` | Backlog the miner draws from; add ideas here |
| `miner/mine.py` | Orchestrator: claim → generate → compile/test in sandbox → repair loop → promote or record failure |
| `.github/workflows/ci.yml` | Re-verifies every algorithm on each push |

**Miner settings:** `ANTHROPIC_API_KEY` (required), `MINER_DAILY_TOKENS` (default 2,000,000), `MINER_WORKERS` (3), `MINER_MODEL`, `MINER_REPAIRS` (2), `MINER_PUBLISH=1` to auto-push each success. Requires Docker (auto-started on macOS).

## Security model

Model-written code is untrusted. It is compiled and executed **only** inside `sandbox/run.sh`: a Docker container with no network, no Linux capabilities, no privilege escalation, a non-root user, a read-only root filesystem, 3 GB memory / 4 CPU / 256-process caps, and a wall-clock timeout. It sees only the one directory under test. The orchestrator (which holds `ANTHROPIC_API_KEY` and GitHub credentials) runs on the host and never executes generated code; secrets never enter the container. `publish.sh` also verifies inside the sandbox, from a read-only copy, before anything is pushed, and aborts if Docker is unavailable or any test fails. Both fail closed: running on the host requires an explicit `MINER_SANDBOX=host` / `PUBLISH_SANDBOX=host`.

Validated by an adversarial probe (network egress, DNS, writes outside scope, host file access, Docker socket, root escalation, secret leakage, runaway process): all blocked. Results reproduce bit-for-bit between macOS and the Linux sandbox.

## Recursive mining on GitHub

`.github/workflows/mine.yml` runs the miner daily (and on demand from the Actions tab) using the repo secret `ANTHROPIC_API_KEY`. When the backlog is empty it proposes new hypotheses from the ledger, capped per run (`MINER_MAX_NEW`). Token efficiency: 1-hour prompt caching of the spec + reference implementation, a cheap-model triage gate before any expensive build, patch-only repairs, trimmed error logs, and price-weighted budget accounting with a hard daily stop.
