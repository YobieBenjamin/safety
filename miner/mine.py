#!/usr/bin/env python3
"""Algorithm miner: parallel agents turn open hypotheses into tested, documented algorithms.

  python3 miner/mine.py                 # run until backlog empty or daily budget spent
  MINER_DRY_RUN=1 python3 miner/mine.py # parse backlog, no API calls

Env: ANTHROPIC_API_KEY (required), MINER_MODEL (default claude-sonnet-5),
     MINER_DAILY_TOKENS (default 2_000_000), MINER_WORKERS (default 3),
     MINER_REPAIRS (default 2), MINER_PUBLISH=1 to run ../publish.sh after each success.

Each agent: claim hypothesis -> generate code+tests+docs -> `make test` in a sandbox
(timeout) -> on failure feed errors back up to MINER_REPAIRS times -> promote to
algorithms/ on pass, or record the failure in LEDGER.md. Negative results are kept.

SECURITY: this executes model-written code. Run it inside a container or VM.
"""
import json, os, re, shutil, subprocess, sys, threading, datetime, urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HYP, LEDGER = os.path.join(ROOT, "HYPOTHESES.md"), os.path.join(ROOT, "LEDGER.md")
STATE, SANDBOX = os.path.join(ROOT, "miner", "state.json"), os.path.join(ROOT, "miner", "sandbox")
MODEL = os.environ.get("MINER_MODEL", "claude-sonnet-5")
BUDGET = int(os.environ.get("MINER_DAILY_TOKENS", 2_000_000))
WORKERS = int(os.environ.get("MINER_WORKERS", 3))
REPAIRS = int(os.environ.get("MINER_REPAIRS", 2))
DRY = os.environ.get("MINER_DRY_RUN") == "1"
LOCK = threading.Lock()

SPEC = """You are a research agent mining NEW AI-safety algorithms grounded in graph theory,
neuroscience and biological behavior. Implement the hypothesis below as a self-contained
algorithm directory. Requirements (all mandatory):
- A compiled core in C (src/*.c, must build with gcc -O2 -Wall -Wextra -Werror) called from Python via ctypes.
- Makefile with targets build, test, experiment, all (all = test + experiment). Dependencies: numpy, scikit-learn only.
- tests/test_core.py: correctness tests of the math against independent references/closed forms.
- tests/experiment.py: deterministic evaluation against at least two standard baselines, writes docs/results.json.
- README.md with sections: 1 Plain English, 2 Technical summary, 3 Mathematics (definitions, and any claim
  either proved or labelled conjecture), 4 Code map, 5 Results (tables filled from actual output),
  6 Honest limitations and prior art. Never claim a win the numbers do not show; negative results are valuable.
Existing reference implementation style: see YB-0001 (effective-connectivity graphs, numpy MLP on sklearn digits).
Reply with ONLY a JSON object: {"files": {"relative/path": "content", ...}, "summary": "one-line headline result"}."""


def load_state():
    today = datetime.date.today().isoformat()
    try:
        s = json.load(open(STATE))
        return s if s.get("date") == today else {"date": today, "used": 0}
    except (FileNotFoundError, json.JSONDecodeError):
        return {"date": today, "used": 0}


def spend(n):
    with LOCK:
        s = load_state(); s["used"] += n; json.dump(s, open(STATE, "w")); return s["used"]


def budget_left():
    return BUDGET - load_state()["used"]


def claim():
    """Atomically take the first open hypothesis. Returns (id, block) or None."""
    with LOCK:
        text = open(HYP).read()
        for block in re.split(r"(?m)^(?=## )", text):
            if block.startswith("## ") and "status: open" in block:
                hid = block.split()[1]
                open(HYP, "w").write(text.replace(block, block.replace("status: open", "status: in-progress", 1)))
                return hid, block
    return None


def set_status(hid, status):
    with LOCK:
        text = open(HYP).read()
        text = re.sub(rf"(## {re.escape(hid)}\b[^\n]*\n)status: \S+", rf"\1status: {status}", text)
        open(HYP, "w").write(text)


def ledger(hid, name, status, headline):
    with LOCK:
        open(LEDGER, "a").write(f"| {hid} | {name} | see HYPOTHESES.md | {status} | {headline} |\n")


def call(messages):
    body = json.dumps({"model": MODEL, "max_tokens": 32000, "system": SPEC, "messages": messages}).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", body, {
        "x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01",
        "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        d = json.load(r)
    spend(d["usage"]["input_tokens"] + d["usage"]["output_tokens"])
    text = "".join(b.get("text", "") for b in d["content"] if b["type"] == "text")
    return text, json.loads(re.sub(r"^```(json)?|```$", "", text.strip(), flags=re.M))


def write(dirpath, files):
    for rel, content in files.items():
        p = os.path.normpath(os.path.join(dirpath, rel))
        if not p.startswith(dirpath + os.sep):
            raise ValueError(f"path escapes sandbox: {rel}")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w").write(content)


def run_tests(d):
    try:
        r = subprocess.run(["make", "-C", d, "all"], capture_output=True, text=True, timeout=1800)
        return r.returncode == 0, (r.stdout + r.stderr)[-6000:]
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT after 1800s"


def mine_one(hid, block):
    name = block.splitlines()[0].split("—", 1)[-1].strip()
    slug = hid + "-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:50]
    box = os.path.join(SANDBOX, slug); shutil.rmtree(box, ignore_errors=True); os.makedirs(box)
    msgs = [{"role": "user", "content": f"Algorithm ID {hid}.\n{block}"}]
    log = ""
    for attempt in range(REPAIRS + 1):
        if budget_left() <= 0:
            set_status(hid, "open"); return f"{hid}: budget exhausted, returned to backlog"
        try:
            raw, out = call(msgs)
            write(box, out["files"])
        except Exception as e:  # malformed JSON, network, bad path
            log = f"generation error: {e}"; msgs += [{"role": "user", "content": log}]; continue
        ok, log = run_tests(box)
        if ok:
            dest = os.path.join(ROOT, "algorithms", slug); shutil.rmtree(dest, ignore_errors=True)
            shutil.move(box, dest); set_status(hid, "tested")
            ledger(hid, name, "tested", out.get("summary", "")[:200])
            if os.environ.get("MINER_PUBLISH") == "1":
                subprocess.run([os.path.join(ROOT, "publish.sh"), f"Mined {hid}"], cwd=ROOT)
            return f"{hid}: PASS — {out.get('summary', '')}"
        msgs += [{"role": "assistant", "content": raw},
                 {"role": "user", "content": f"`make all` failed. Fix and resend the full JSON.\n{log}"}]
    set_status(hid, "failed"); ledger(hid, name, "failed build/test", log.splitlines()[-1][:200] if log else "")
    return f"{hid}: FAILED after {REPAIRS + 1} attempts"


def worker(_):
    results = []
    while budget_left() > 0:
        job = claim()
        if not job:
            break
        results.append(mine_one(*job))
        print(results[-1], f"| tokens used today: {load_state()['used']:,}/{BUDGET:,}", flush=True)
    return results


if __name__ == "__main__":
    os.makedirs(SANDBOX, exist_ok=True)
    if DRY:
        text = open(HYP).read()
        opened = [b.split()[1] for b in re.split(r"(?m)^(?=## )", text) if b.startswith("## ") and "status: open" in b]
        print(f"DRY RUN: {len(opened)} open hypotheses: {opened}; budget left {budget_left():,}"); sys.exit(0)
    if "ANTHROPIC_API_KEY" not in os.environ:
        sys.exit("export ANTHROPIC_API_KEY first")
    with ThreadPoolExecutor(WORKERS) as ex:
        list(ex.map(worker, range(WORKERS)))
    print("Mining run complete.")
