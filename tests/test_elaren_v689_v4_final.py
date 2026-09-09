import json
import pathlib
import re

ROOT = pathlib.Path(__file__).parents[1]
BASE = ROOT / "docs/elaren-kestrel/v689-v4"

def load(rel):
    return json.loads((BASE / rel).read_text(encoding="utf-8"))

def test_final_truth_and_method_flow():
    truth = load("final/phase-truth.json")
    flow = load("final/method-flow-final.json")
    assert truth["outcomes"] == {"completed":170,"represented":20,"open_gap":5,"exact_gate":5}
    assert flow["counts"]["witnesses"] == flow["counts"]["witness_results"]["pass"] + flow["counts"]["witness_results"]["fail"]

def test_baton_and_modules():
    baton = (BASE / "final/hand-off-baton.md").read_text(encoding="utf-8")
    index = load("final/baton-module-index.json")
    assert 10000 <= len(re.findall(r"\S+", baton)) <= 100000
    assert index["module_count"] == 13

def test_deck_manifest():
    deck = load("final/deck/deck-index.json")
    manifest = load("final/deck/card-manifest.json")
    assert deck["card_count"] == manifest["entry_count"] == 273

def test_accessible_report_structure():
    report = (BASE / "final/accessible-report.html").read_text(encoding="utf-8")
    assert "<main" in report and "<h1>" in report and "<caption>" in report
    assert "scope=\"col\"" in report and report.count("class=\"page\"") >= 4

def test_route_is_prepared_not_sent():
    route = load("final/terminal-route-candidate.json")
    assert route["state"] == "PREPARED_NOT_SENT"
    assert route["successor_title"] == "Rowan Ash"
    assert route["messages_sent"] == 0
