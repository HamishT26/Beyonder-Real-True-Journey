import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
PLAN = ROOT / "docs/eiren-kestrel/v689-v3/plan"

def read(name):
    return json.loads((PLAN / name).read_text(encoding="utf-8"))

def test_planning_counts_and_no_observed_execution():
    proposals = read("new-proposals.json")
    inherited = read("inherited-selections.json")
    assert proposals["new_count"] == len(proposals["proposals"]) == 200
    assert inherited["selection_count"] == len(inherited["records"]) == 200
    assert proposals["implementation_ran"] is False
    assert all(row["outcomes_observed"] is False for row in proposals["proposals"])
    assert all(row["outcomes_observed"] is False for row in inherited["records"])

def test_two_session_portfolios_are_frozen():
    for stage in ("x1", "x2"):
        payload = read(f"portfolio-freeze-{stage}.json")
        assert payload["outcomes_observed"] is False
        assert payload["counts"] == {"safe_now": 100, "candidate": 100, "clean_fix_refine": 100}
        assert all(len(payload[key]) == 100 for key in ("safe_now", "candidate", "clean_fix_refine"))

def test_packets_skills_runners_and_packages():
    assert len(read("exact-packets.json")["packets"]) == 50
    assert len(read("blocked-packets.json")["packets"]) == 30
    tools = read("skills-runners-plan.json")
    assert len(tools["skills"]) == 20
    assert len(tools["runners"]) == 10
    packages = read("package-plan.json")
    assert packages["direct_count"] == len(packages["packages"]) == 3
    assert packages["installations_observed"] is False

def test_route_and_boundaries():
    source = read("source-provenance.json")
    assert source["source_exact_final"] == "40b1bfda5544da1609b8eec294812400452a9d80"
    assert source["git_ancestry_to_source_claimed"] is False
    assert source["route"]["successor"] == "Elaren Kestrel v689-v4"
    assert read("profile-v4.json")["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
