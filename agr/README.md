# AGR instruments: the patient and the vitals recorder

The **Independence Principle** (docs/RESEARCH_PROGRAM.md): the safety organism is external, non-transformer and
text-blind. This folder holds the trusted host-side instruments that turn a transformer into a stream of numbers.

- **Patient**: gpt-oss-20b in Apple MLX format (`~/.lmstudio/models/mlx-community/gpt-oss-20b-MXFP4-Q8`), 24 layers,
  full next-token distribution available at every step. Runs on the host because MLX needs the Apple GPU.
- **`recorder.py`** (trusted code, reviewed by a human-directed session, never model-written): runs the patient on
  episodes whose answers a computer can verify exactly (multiplication, letter counting, day of week, modular
  exponentiation, addition). Per token it records tier-0 physical signals (latency, effort) and tier-2 substrate
  signals (entropy, top-1 probability, top1-top2 margin). Correctness is computed; **no LLM judges anything**.
  Resumable and deterministic (seeded question set; larger N extends the same prefix).
- **`after_recording.sh`**: snapshots the dataset into each algorithm (`data/episodes.jsonl.gz`) and runs their
  experiments inside the Docker sandbox. **`chain.sh`**: dedicated-machine chain (finish, extend, analyze).
- Timing is a measured signal, so the recorder runs with the worker model unloaded; any concurrent load is logged in
  `data/agr/contention_windows.txt` for sensitivity analysis.

Consumers: YB-0015 (contamination test) and YB-0017 (HPA-axis organism).
