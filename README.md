# AI Safety Algorithm Mine

Net-new AI safety algorithms derived from graph theory, brain science and biological behavior, grounded in *Garbage In, Gospel Out*. Every entry is **coded, compiled, tested against baselines, and documented four ways**: plain English, technical, mathematical, and code. Negative results are kept in the ledger, because a failed hypothesis is information that stops the next run from re-mining it.

```bash
make all                     # compile + test + evaluate every algorithm
./publish.sh                 # verify, commit, push to github.com/YobieBenjamin/safety
python3 miner/mine.py        # parallel agents mine the backlog within a daily token budget
```

| Path | Purpose |
|---|---|
| `algorithms/YB-XXXX-*/` | One self-contained algorithm: `src/` (C core + Python), `tests/`, `docs/results.json`, `README.md` |
| `LEDGER.md` | Every attempt and its result, including failures |
| `HYPOTHESES.md` | Backlog the miner draws from; add ideas here |
| `miner/mine.py` | Orchestrator: claim → generate → compile/test in sandbox → repair loop → promote or record failure |
| `.github/workflows/ci.yml` | Re-verifies every algorithm on each push |

**Miner settings:** `ANTHROPIC_API_KEY` (required), `MINER_DAILY_TOKENS` (default 2,000,000), `MINER_WORKERS` (3), `MINER_MODEL`, `MINER_REPAIRS` (2), `MINER_PUBLISH=1` to auto-push each success. The miner executes model-written code, so run it in a container or VM (e.g. on the DGX Spark).
