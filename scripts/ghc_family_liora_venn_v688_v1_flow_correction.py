"""Append the two sparse-stage failures and recoveries without replaying x2."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/liora-venn/v688-v1/x2"
GATES = ["empirical", "real_participant", "professional", "production", "deployment", "identity", "legal", "cultural", "affected_party", "maori_authority", "privacy_complete", "accessibility_complete", "exhaustive_security", "independent_reproduction", "agi_asi", "consciousness_personhood", "theory_of_everything", "proof_canon", "stage20"]
FAILURES = [
    ("024", "The first exact x2 staging request partially staged eligible files but refused two owner scripts outside the sparse definition.", "Retain the failed stage attempt, add only the two exact owner-script patterns, regenerate manifests, and require zero unstaged paths before commit."),
    ("025", "The first sparse-pattern update used an unsupported sparse-checkout add --no-cone option.", "Keep the established non-cone mode and add the same two literal patterns with the supported --skip-checks option."),
]
STAGED_AUDIT_FAILURE = ("026", "The second combined stage-and-manifest audit exceeded its output window while sequential Git blob reads continued without an attributable result.", "Confirm the original read-only process exits, retain the no-result attempt, and use one batched Git object stream for the exact staged manifest.")


def load(name):
    return json.loads((BASE / name).read_text(encoding="utf-8"))


def dump(name, value):
    (BASE / name).write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def main():
    ledger = load("method-flow/ledger.json")
    if len(ledger["methods"]) == 32:
        pending = FAILURES
        target_methods, target_witnesses, target_events, target_fail, target_pass = 34, 766, 102, 274, 492
    elif len(ledger["methods"]) == 34:
        pending = [STAGED_AUDIT_FAILURE]
        target_methods, target_witnesses, target_events, target_fail, target_pass = 35, 768, 105, 275, 493
    else:
        raise AssertionError((len(ledger["methods"]), len(ledger["witnesses"])))
    for suffix, failure, recovery in pending:
        method_id, negative_id = "LV6881-X2-M" + suffix, "LV6881-X2-N" + suffix
        ledger["methods"].append({"method_id": method_id, "title": recovery, "failure_signature": failure, "trigger_preconditions": ["Liora v688-v1 immutable x1", "exact sparse staging"], "privacy_class": "sanitized_public", "approval_class": "safe_now", "candidate_workaround": recovery, "validation_witness_ids": [method_id + "-FAIL", method_id + "-PASS"], "recurrence_guard": recovery, "rollback": "Stop staging, preserve all owner files and the index, then use only exact owner path patterns.", "recommendation_state": "preferred", "supersedes": [], "protected_gates": GATES, "retained_negative_ids": [negative_id], "scope_boundary": "Owner sparse-index mechanics only; zero proposal, canonical, empirical, route, or authority credit.", "execution_authority": "owner_self_scoped_delta", "repository_scan": False, "module_scan": False, "cross_lane_scan": False, "unchanged_history_scan": False, "sibling_lane_mutation": False, "source_commit": "17fee348a09ec1cb480f7326bce70cd75413dad3", "final_commit": None, "changed_file_allowlist": [], "module_allowlist": [], "exact_pushed_head_required": True})
        ledger["witnesses"].extend([
            {"witness_id": method_id + "-FAIL", "method_id": method_id, "procedure": "Exact sparse staging", "scope": "Liora v688-v1 owner delta", "expected": "All allowlisted paths become index-eligible", "observed": failure, "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": "The corrected stage never erases or promotes this failed witness."},
            {"witness_id": method_id + "-PASS", "method_id": method_id, "procedure": recovery, "scope": "Liora v688-v1 owner delta", "expected": "Literal sparse recovery", "observed": recovery, "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": "The narrow recovery is not independent reproduction or broader evidence."},
        ])
        ledger["state_events"].extend([{"method_id": method_id, "from": "observed", "to": "candidate"}, {"method_id": method_id, "from": "candidate", "to": "validated"}, {"method_id": method_id, "from": "validated", "to": "preferred"}])
    ledger["counts"] = {"methods": target_methods, "witnesses": target_witnesses, "state_events": target_events, "recommendations": 0, "states": {"candidate": 0, "deprecated": 0, "observed": 0, "preferred": target_methods, "superseded": 0, "validated": 0}, "witness_results": {"fail": target_fail, "pass": target_pass}}
    ledger["count_contract"] = f"Ten operation methods, three package methods, ten skill methods, five runner methods, and {target_methods - 28} operational-recovery methods. Failed witnesses are 250 altered outputs, eighteen adverse interfaces, and {target_methods - 28} operational failures. Passing witnesses are 200 contract matches, 250 mutation rejections, 36 interface witnesses, and {target_methods - 28} recoveries."
    dump("method-flow/ledger.json", ledger)
    counts = {"proposals": 15630, "negatives": 82561 + target_methods, "methods": 93254 + target_methods, "failed_witnesses": 53409 + target_methods, "passing_witnesses": 82971 + target_methods, "open_gaps": 748, "exact_gates": 747}
    truth = load("phase-truth.json"); truth["effective_counts"] = counts; dump("phase-truth.json", truth)
    retained = load("retained-negative-register.json")
    retained["x2_delta"] = {"negatives": 240 + target_methods, "methods": target_methods, "failed_witnesses": 240 + target_methods, "passing_witnesses": 458 + target_methods}
    retained["effective_counts"] = counts
    retained["operational_failures"].extend([{"negative_id": "LV6881-X2-N" + suffix, "failure": failure, "recovery": recovery, "original_success_credit": 0} for suffix, failure, recovery in pending])
    dump("retained-negative-register.json", retained)
    execution = load("execution-summary.json"); execution["retained_operational_failures"] = target_methods - 28; dump("execution-summary.json", execution)
    overview = (BASE / "integrated-overview.html").read_text(encoding="utf-8").replace("Four x2 operational failures", "Six x2 operational failures").replace("Six x2 operational failures", "Seven x2 operational failures" if target_methods == 35 else "Six x2 operational failures")
    (BASE / "integrated-overview.html").write_text(overview, encoding="utf-8", newline="\n")
    if target_methods == 34:
        dump("sparse-stage-correction-receipt.json", {"schema": "ghc.family.sparse-stage-correction.v1", "negative_ids": ["LV6881-X2-N024", "LV6881-X2-N025"], "failed_stage_credit": 0, "broad_patterns_added": 0, "literal_patterns_added": 2, "manifest_regeneration_required": True})
    else:
        dump("staged-audit-recovery-receipt.json", {"schema": "ghc.family.staged-audit-recovery.v1", "negative_id": "LV6881-X2-N026", "first_result_attributable": False, "sequential_reader_reused": False, "batched_object_stream_required": True, "canonical_credit": 0})
    print(json.dumps({"state": "X2_FLOW_CORRECTION_RETAINED", "methods": target_methods, "witnesses": target_witnesses, "failed": target_fail, "passed": target_pass}, sort_keys=True))


if __name__ == "__main__":
    main()
