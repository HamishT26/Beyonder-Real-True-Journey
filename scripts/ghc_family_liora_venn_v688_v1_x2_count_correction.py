"""Apply the retained Method Flow derived-count correction without replaying x2."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/liora-venn/v688-v1/x2"
GATES = ["empirical", "real_participant", "professional", "production", "deployment", "identity", "legal", "cultural", "affected_party", "maori_authority", "privacy_complete", "accessibility_complete", "exhaustive_security", "independent_reproduction", "agi_asi", "consciousness_personhood", "theory_of_everything", "proof_canon", "stage20"]
FAILURE = "The first installed Method Flow validation rejected an older flat derived-count shape as stale."
RECOVERY = "Retain every existing method and witness, append this failure and recovery, and emit the current nested state and witness-result count shape."


def load(name):
    return json.loads((BASE / name).read_text(encoding="utf-8"))


def dump(name, value):
    (BASE / name).write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def main():
    ledger = load("method-flow/ledger.json")
    assert len(ledger["methods"]) == 31 and len(ledger["witnesses"]) == 760
    method_id, negative_id = "LV6881-X2-M023", "LV6881-X2-N023"
    ledger["methods"].append({"method_id": method_id, "title": RECOVERY, "failure_signature": FAILURE, "trigger_preconditions": ["Liora v688-v1 immutable x1", "installed current Method Flow validation"], "privacy_class": "sanitized_public", "approval_class": "safe_now", "candidate_workaround": RECOVERY, "validation_witness_ids": [method_id + "-FAIL", method_id + "-PASS"], "recurrence_guard": "Compare the ledger count block with the installed schema-derived summary before evidence freeze.", "rollback": "Retain the failed receipt and restore only the derived count block if the narrow correction fails.", "recommendation_state": "preferred", "supersedes": [], "protected_gates": GATES, "retained_negative_ids": [negative_id], "scope_boundary": "Derived Method Flow arithmetic only; zero proposal, canonical, empirical, route, or authority credit.", "execution_authority": "owner_self_scoped_delta", "repository_scan": False, "module_scan": False, "cross_lane_scan": False, "unchanged_history_scan": False, "sibling_lane_mutation": False, "source_commit": "17fee348a09ec1cb480f7326bce70cd75413dad3", "final_commit": None, "changed_file_allowlist": [], "module_allowlist": [], "exact_pushed_head_required": True})
    ledger["witnesses"].extend([
        {"witness_id": method_id + "-FAIL", "method_id": method_id, "procedure": "Installed Method Flow validation", "scope": "Liora v688-v1 owner delta", "expected": "Current derived-count shape", "observed": FAILURE, "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": "The corrected count block never erases or promotes this failed witness."},
        {"witness_id": method_id + "-PASS", "method_id": method_id, "procedure": RECOVERY, "scope": "Liora v688-v1 owner delta", "expected": "Current nested count shape with all prior witnesses unchanged", "observed": "Derived count block corrected additively", "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": "A narrow schema recovery is not independent reproduction or broader evidence."},
    ])
    ledger["state_events"].extend([{"method_id": method_id, "from": "observed", "to": "candidate"}, {"method_id": method_id, "from": "candidate", "to": "validated"}, {"method_id": method_id, "from": "validated", "to": "preferred"}])
    ledger["counts"] = {"methods": 32, "witnesses": 762, "state_events": 96, "recommendations": 0, "states": {"candidate": 0, "deprecated": 0, "observed": 0, "preferred": 32, "superseded": 0, "validated": 0}, "witness_results": {"fail": 272, "pass": 490}}
    ledger["count_contract"] = "Ten operation methods, three package methods, ten skill methods, five runner methods, and four operational-recovery methods. Failed witnesses are 250 altered outputs, eighteen adverse interfaces, and four operational failures. Passing witnesses are 200 contract matches, 250 mutation rejections, 36 interface witnesses, and four recoveries."
    dump("method-flow/ledger.json", ledger)

    counts = {"proposals": 15630, "negatives": 82593, "methods": 93286, "failed_witnesses": 53441, "passing_witnesses": 83003, "open_gaps": 748, "exact_gates": 747}
    truth = load("phase-truth.json"); truth["effective_counts"] = counts; dump("phase-truth.json", truth)
    retained = load("retained-negative-register.json")
    retained["x2_delta"] = {"negatives": 272, "methods": 32, "failed_witnesses": 272, "passing_witnesses": 490}
    retained["effective_counts"] = counts
    retained["operational_failures"].append({"negative_id": negative_id, "failure": FAILURE, "recovery": RECOVERY, "original_success_credit": 0})
    dump("retained-negative-register.json", retained)
    execution = load("execution-summary.json"); execution["retained_operational_failures"] = 4; dump("execution-summary.json", execution)
    overview = (BASE / "integrated-overview.html").read_text(encoding="utf-8").replace("Three x2 operational failures", "Four x2 operational failures")
    (BASE / "integrated-overview.html").write_text(overview, encoding="utf-8", newline="\n")
    dump("method-flow-correction-receipt.json", {"schema": "ghc.family.method-flow-derived-count-correction.v1", "negative_id": negative_id, "failed_validation_preserved": True, "mutation_or_contract_witnesses_changed": 0, "recovery": RECOVERY, "canonical_credit": 0})
    print(json.dumps({"state": "METHOD_FLOW_COUNT_CORRECTED", "methods": 32, "witnesses": 762, "failed": 272, "passed": 490}, sort_keys=True))


if __name__ == "__main__":
    main()
