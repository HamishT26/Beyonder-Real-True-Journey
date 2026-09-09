import hashlib
import json
import re
from pathlib import Path

ROOT=Path(__file__).parents[1]
FINAL=ROOT/"docs/eiren-kestrel/v689-v3/final"
def read(path): return json.loads((FINAL/path).read_text(encoding="utf-8"))

def test_final_outcomes_and_portfolios():
    truth=read("phase-truth.json")
    assert truth["outcomes"]=={"completed":170,"represented":20,"open_gap":5,"exact_gate":5}
    assert truth["new_proposals"]==truth["inherited_refinements"]==200
def test_source_window_and_blank_root_provenance():
    source=json.loads((ROOT/"docs/eiren-kestrel/v689-v3/plan/source-provenance.json").read_text(encoding="utf-8"))
    window=json.loads((ROOT/"docs/eiren-kestrel/v689-v3/plan/source-window.json").read_text(encoding="utf-8"))
    assert source["git_ancestry_to_source_claimed"] is False and len(window["records"])==10
def test_package_receipt():
    package=json.loads((ROOT/"docs/eiren-kestrel/v689-v3/x1/package-receipt.json").read_text(encoding="utf-8"))
    assert package["valid"] and package["direct_count"]==3 and package["closure_count"]==9
def test_method_flow_truth():
    summary=read("method-flow-summary.json")
    counts=summary["counts"]
    assert counts["methods"]==33 and counts["witnesses"]==counts["witness_results"]["pass"]+counts["witness_results"]["fail"]
def test_tool_counts_and_collision_resolution():
    assert read("wellbeing-workload.json")["local_skills"]==21
    resolution=json.loads((ROOT/"docs/eiren-kestrel/v689-v3/tooling/meta-tool-collision-resolution.json").read_text(encoding="utf-8"))
    assert resolution["global_overwrites"]==0
def test_card_manifest_and_parent_rules():
    manifest=read("deck/card-manifest.json"); cards={}
    for row in manifest["entries"]:
        path=ROOT/row["path"]; raw=path.read_bytes(); assert len(raw)==row["bytes"] and hashlib.sha256(raw).hexdigest()==row["sha256"]
        payload=json.loads(raw); cards[payload["card_id"]]=payload
    assert len(cards)==8+200+read("method-flow-summary.json")["counts"]["methods"]
    for item in cards.values():
        for parent in item["parent_ids"]: assert parent in cards and cards[parent]["tier"]==item["tier"]-1
def test_baton_modules_and_word_budget():
    baton=(FINAL/"hand-off-baton.md").read_text(encoding="utf-8"); index=read("baton-module-index.json")
    assert index["module_count"]==13 and 10000<=len(re.findall(r"\S+",baton))<=100000
def test_overview_and_accessible_report_structure():
    assert len(re.findall(r"\S+",(FINAL/"overview.md").read_text(encoding="utf-8")))>=1800
    report=(FINAL/"accessible-report.html").read_text(encoding="utf-8"); assert report.count('class="page"')>=4 and "<main" in report and "<table" in report
def test_route_is_prepared_and_single_valued():
    route=read("terminal-route-candidate.json")
    assert route["state"]=="PREPARED_NOT_SENT" and route["successor_title"]=="Elaren Kestrel" and route["following_title"]=="Rowan Ash" and route["messages_sent"]==0
def test_retained_negative_and_gate_counts():
    assert read("retained-negative-register.json")["count"]==read("method-flow-summary.json")["counts"]["witness_results"]["fail"]
    gates=read("open-exact-gate-register.json"); assert gates["proposal_open_gaps"]==5 and gates["proposal_exact_gates"]==5 and gates["blocked_subjects"]==30
def test_exact_packets_and_terminal_boundary():
    closeout=read("closeout-candidate.json"); assert closeout["exact_packets"]==50 and closeout["exact_actions_completed_at_repository_seal"]==47 and closeout["canonical_invocations"]==0
def test_final_manifests_and_seal_exist():
    for name in ("final-delta-manifest.json","final-owner-manifest.json","content-seal.json"):
        payload=read(name); assert payload["entry_count"]==len(payload["entries"])
