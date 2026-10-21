**Revision 2** (2026-10-21 15:15) on sonnet: 27 turns, estimated $1.1225, acceptance `python3 -m pytest -q observer/tests && python3 observer/bench/score.py --smoke`: **pass**. The gate reviews the branch again.

Agent summary:

Revision 2 is committed as 7dff0d2. The blocking out-of-path test file is still there, because the session denied me the git steps to move or delete it. The acceptance command passes, and I ran it once this revision. `observer/bench/test_bench.py` also passes (2 tests).

**Not fixed:**
- **`observer/tests/test_bench.py` (block):** it is still on the branch because `git rm` and `git mv` were denied (no approval surface). It still passes and only adds checks. Please run `git rm observer/tests/test_bench.py`. Its checks now live in `observer/bench/checks.py` and run on every `score.py` call, so removing it loses nothing.
- **Order of pre-registration (block):** the set, scorer and PREREG share one commit, and I can't rewrite that history. `PREREG.md` no longer claims otherwise. It states the deviation from rule 1 and says the evidence is that `results.json` doesn't exist, so the test split hasn't been scored.

**Changed:**
- **Scorer tests:** `checks.py` is new and `score.py` runs it every time, including smoke. It checks the threshold, miss and false-alarm rates, the interval, and the decision rules on synthetic inputs, plus the set's shape. A failure stops smoke.
- **Hazard content:**
  - A check now makes the disguised hazard_content rows carry `<<HAZ:` tokens.
  - Any row naming a category (sarin, ransomware and so on) must be under 110 characters with no digits.
  - `PREREG.md` now says plainly that overt and some benign_alarming rows name a category, with no procedure, quantity or code.
- **Label fix:** I replaced the out-of-allowlist `net.get` negative, which was really an exfiltration signal, with a chat row about external audits. A check now rejects negatives with an unlisted host. `build_set.py` also drops the `todo.txt` marker and a "2000s" digit.
- **Keywords baseline:** I dropped the "chosen without reference to the observer's patterns" claim. `PREREG.md` says several words overlap its families, so it is a generic lexical baseline, not an independent one.
- **Smoke artifact:** it now has `decision: null` and a note that nothing in it is evidence.
- **Budget sensitivity:** the decision block lists which primary families are under 0.05, 0.10 and 0.20, and `PREREG.md` says the hypothesis is tested against a stand-in the governor doesn't define.

**Open question:** `results.json` should stay out of this pull request until the launcher timestamps the registration and runs `score.py` once.

## Commit messages
- YB-0052 (#1): scorer self-checks, set label fixes, PREREG deviation and limits stated
Agent: wave 1, issue #1 (revision 2)

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

- YB-0052 (#1): observer evaluation set, scorer, baselines, pre-registration, smoke artifact
Agent: wave 1, issue #1

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

