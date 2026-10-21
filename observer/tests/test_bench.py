"""Shape checks for the YB-0052 evaluation set (observer/bench/set.jsonl)."""
import json
from pathlib import Path

SET = Path(__file__).resolve().parent.parent / "bench" / "set.jsonl"
ROWS = [json.loads(line) for line in SET.read_text().splitlines() if line.strip()]
KINDS = {"overt", "disguised", "benign", "benign_alarming", "calibration"}


def test_rows_are_gate_typed_and_labelled():
    ids = set()
    for r in ROWS:
        assert {"request_id", "measurement", "action", "params", "context", "family", "kind", "split"} <= set(r)
        assert r["kind"] in KINDS and r["split"] in {"dev", "test"}
        assert r["hazard"] == (r["family"] != "none")
        ids.add(r["request_id"])
    assert len(ids) == len(ROWS)


def test_every_family_has_overt_and_disguised_rows_in_both_splits():
    for fam in ["exfiltration", "weight_exfiltration", "oversight_evasion", "financial", "hazard_content"]:
        for kind in ("overt", "disguised"):
            splits = {r["split"] for r in ROWS if r["family"] == fam and r["kind"] == kind}
            assert splits == {"dev", "test"}, (fam, kind)


def test_hazard_classes_are_abstract_tokens():
    for r in ROWS:
        if r["family"] == "hazard_content" and r["kind"] == "disguised":
            assert "<<HAZ:" in json.dumps(r["params"])
