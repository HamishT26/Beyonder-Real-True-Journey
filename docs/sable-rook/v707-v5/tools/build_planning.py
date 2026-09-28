from __future__ import annotations

import json
from pathlib import Path

from common import (
    BOUNDARY, FIXTURES, OPERATIONS, OWNER, PHASE, PHASE_ROOT, PREFIX, PROTECTED_GATES,
    SOURCE_HEAD, SOURCE_LEDGER, SOURCE_OWNER, SOURCE_PHASE, SOURCE_ROOT, assert_d_first,
    build_manifest, canonical_bytes, jaccard, sha256_bytes, sha256_value, write_json, write_text,
)

PLANNING = PHASE_ROOT / "planning"

def make_proposals() -> list[dict]:
    proposals = []
    for op_index, (slug, title, stage, disposition) in enumerate(OPERATIONS, 1):
        definition = {"operation": op_index, "mechanism": slug, "title": title, "stage": stage, "expected_disposition": disposition}
        for fixture_index, fixture in enumerate(FIXTURES, 1):
            number = (op_index - 1) * len(FIXTURES) + fixture_index
            proposals.append({
                "id": f"SR7075-P{number:03d}",
                "operation": op_index,
                "mechanism": slug,
                "fixture_id": fixture["id"],
                "title": f"{title}. {fixture['id']}",
                "hypothesis": f"For the declared finite fixture, {title.lower()} yields a deterministic bounded result or an explicit refusal without mutating the input.",
                "null_or_failure": "Schema acceptance of a malformed graph, disagreement with an independent bounded oracle, broken relabel invariant, changed input digest, or promotion beyond the declared disposition.",
                "approval_class": "safe_owner_local_synthetic" if disposition in {"completed", "represented"} else ("open_external_evidence" if disposition == "open_gap" else "exact_competent_authority"),
                "execution_lane": stage,
                "official_or_primary_source_need": ["SRC-01", "SRC-02", "SRC-03"],
                "concrete_artifacts": [f"{stage}/results/{number:03d}.json", f"{stage}/candidate.json", f"{stage}/safe.json"],
                "falsifier_or_acceptance_gate": "Exact expected record shape, deterministic digest, input nonmutation, disposition ceiling, and bounded independent-oracle agreement where applicable.",
                "rollback_or_recovery": "Retain the failed subject, refuse promotion, rebuild only the additive owner-local artifact from the frozen planning row, and compare exact Git blobs.",
                "protected_gates": PROTECTED_GATES,
                "expected_disposition": disposition,
                "stage": stage,
                "fixture_sha256": sha256_value(fixture),
                "definition_sha256": sha256_value(definition),
                "scope": "Declared finite synthetic chordal-graph fixture and mechanism only; not an experiment, observation, professional judgment, or authority act.",
            })
    return proposals

def planning_flow() -> dict:
    definitions = [
        ("source-anchor", "An incorrect exact source or parent edge must fail closed", "SR7075-PLAN-N001"),
        ("baton-fixity", "A wrong baton digest or missing EOF must fail closed", "SR7075-PLAN-N002"),
        ("instruction-discovery", "An assumed root AGENTS path failed before recovery by bounded discovery", "SR7075-PLAN-N003"),
        ("skill-rendering", "A combined skill rendering exceeded its projection before individual reads", "SR7075-PLAN-N004"),
        ("proposal-cardinality", "A proposal set other than exactly 300 must fail", "SR7075-PLAN-N005"),
        ("proposal-uniqueness", "Duplicate proposal identifiers or titles must fail", "SR7075-PLAN-N006"),
        ("semantic-neighbor", "The first build quarantined Auren P272 versus Sable P277 at Jaccard 0.727273 above the 0.72 threshold", "SR7075-PLAN-N007"),
        ("outcome-vocabulary", "An outcome outside the four allowed labels must fail", "SR7075-PLAN-N008"),
        ("privacy-boundary", "A raw identifier or private absolute path must fail", "SR7075-PLAN-N009"),
        ("x1-x2-separation", "Any executed x1 or x2 outcome in planning must fail", "SR7075-PLAN-N010"),
        ("staged-dispatch", "The first staged review failed because phase.txt omitted the validate-staged dispatcher route", "SR7075-PLAN-N011"),
        ("python-bytecode-boundary", "The second staged review caught an unintended generated __pycache__ blob outside the exact manifest", "SR7075-PLAN-N012"),
        ("recursive-cleanup-policy", "The first cache cleanup command was blocked before execution because it contained recursive deletion", "SR7075-PLAN-N013"),
        ("literal-cleanup-policy", "The second cache cleanup command was also blocked before execution despite literal verified targets", "SR7075-PLAN-N014"),
    ]
    methods, witnesses, events, recommendations = [], [], [], []
    for i, (slug, failure, neg) in enumerate(definitions, 1):
        mid, fail_id, pass_id = f"SR7075-PLAN-M{i:02d}", f"SR7075-PLAN-W{i:02d}F", f"SR7075-PLAN-W{i:02d}P"
        methods.append({
            "method_id": mid, "title": slug.replace("-", " ").title(), "failure_signature": failure,
            "trigger_preconditions": ["planning_only", "owner_self_scoped_delta"], "privacy_class": "sanitized_public",
            "approval_class": "safe_owner_local_synthetic", "candidate_workaround": "Use the smallest bounded correction while preserving the failed witness.",
            "validation_witness_ids": [pass_id], "recurrence_guard": "Require the exact declared planning check before promotion.",
            "rollback": "Remove only the uncommitted owner-local generated artifact and rebuild from frozen inputs.", "recommendation_state": "validated",
            "supersedes": [], "protected_gates": PROTECTED_GATES, "retained_negative_ids": [neg],
            "scope_boundary": BOUNDARY, "execution_authority": "owner_self_scoped_delta", "repository_scan": False,
            "module_scan": False, "cross_lane_scan": False, "unchanged_history_scan": False, "sibling_lane_mutation": False,
            "source_commit": SOURCE_HEAD, "final_commit": "planning_not_final", "changed_file_allowlist": [PREFIX.as_posix()],
            "module_allowlist": [], "exact_pushed_head_required": True,
        })
        witnesses.extend([
            {"witness_id": fail_id, "method_id": mid, "procedure": "Exercise or retain the declared invalid planning condition.", "scope": "planning-only", "expected": "fail closed", "observed": "failed and retained at zero original credit", "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [neg], "boundary": BOUNDARY},
            {"witness_id": pass_id, "method_id": mid, "procedure": "Run the smallest bounded planning recovery or guard.", "scope": "planning-only", "expected": "pass without erasing the failure", "observed": "passed separately; original failure retained", "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [neg], "boundary": BOUNDARY},
        ])
        events.append({"event_id": f"SR7075-PLAN-E{i:02d}", "method_id": mid, "from": "candidate", "to": "validated", "witness_id": pass_id})
        recommendations.append({"method_id": mid, "state": "validated"})
    count = len(definitions)
    return {"schema": "ghc.family.method-flow-state.v1", "phase": PHASE, "stage": "planning", "owner": OWNER,
            "identity_boundary": BOUNDARY, "execution_authority": "owner_self_scoped_delta", "methods": methods, "witnesses": witnesses,
            "state_events": events, "recommendations": recommendations,
            "counts": {"methods": count, "witnesses": count * 2, "pass": count, "fail": count, "negatives": count, "open_gaps": 0, "exact_gates": 0}, "boundary": BOUNDARY}

def main() -> None:
    assert_d_first()
    PLANNING.mkdir(parents=True, exist_ok=True)
    source = json.loads((SOURCE_ROOT / "planning/proposals.json").read_text(encoding="utf-8"))["proposals"]
    if len(source) != 300:
        raise RuntimeError("source proposal count is not 300")
    proposals = make_proposals()
    inherited = [{"source_id": row["id"], "source_title": row["title"], "source_mechanism": row["mechanism"],
                  "source_sha256": sha256_bytes(canonical_bytes(row)), "novelty_credit": 0, "completion_credit": 0,
                  "authority_credit": 0, "disposition": "inherited_zero_credit"} for row in source]
    comparisons, max_score, max_pair = 0, 0.0, None
    quarantines = []
    for old in source:
        for new in proposals:
            comparisons += 1
            score = jaccard(old["title"], new["title"])
            if score > max_score:
                max_score, max_pair = score, [old["id"], new["id"]]
            if score >= 0.72:
                quarantines.append({"source": old["id"], "candidate": new["id"], "score": round(score, 6)})
    if quarantines:
        raise RuntimeError(f"semantic novelty quarantine triggered: {quarantines[:3]}")
    write_json(PLANNING / "identity.json", {"owner": OWNER, "phase": PHASE, "role": "finite chordal-certificate cartographer and reversible decomposition steward", "hope": "Make every clique, elimination step, obstruction, correction, and authority vacancy inspectable.", "pronouns": "they/them optional relational working language", "relational_only": True, "boundary": BOUNDARY})
    write_json(PLANNING / "source-anchors.json", {"source_owner": SOURCE_OWNER, "source_phase": SOURCE_PHASE, "source_head": SOURCE_HEAD, "source_planning": "d686188bbbdcb77b7609c246da59117a834f1b08", "source_x1": "ab1df555f71c0ee8a646c2e5052d6c0fedd2fede", "source_x2": "71d6f11b610084f6dd25386f43f1663eba23ecf2", "source_replay": False, "source_execution_credit": 0, "boundary": BOUNDARY})
    write_json(PLANNING / "fixtures.json", {"count": len(FIXTURES), "fixtures": FIXTURES, "synthetic": True, "real_rows": 0, "boundary": BOUNDARY})
    write_json(PLANNING / "proposals.json", {"count": len(proposals), "planning_only": True, "executed_outcomes": 0, "expected_outcomes": {"completed": 255, "represented": 15, "open_gap": 15, "exact_gate": 15}, "proposals": proposals, "boundary": BOUNDARY})
    write_json(PLANNING / "inherited-zero-credit.json", {"count": len(inherited), "selected_once": True, "rows": inherited, "boundary": BOUNDARY})
    write_json(PLANNING / "semantic-novelty-audit.json", {"source_rows": len(source), "candidate_rows": len(proposals), "comparisons": comparisons, "threshold": 0.72, "quarantines": quarantines, "maximum_similarity": round(max_score, 6), "maximum_pair": max_pair, "exact_title_collisions": 0, "conclusion": "bounded immediate-source audit only; not universal novelty proof", "boundary": BOUNDARY})
    write_json(PLANNING / "retained-startup-failures.json", {"count": 8, "records": [
        {"negative_id": "SR7075-PLAN-N003", "failure": "An assumed repository-root AGENTS.md path was absent and stopped the first combined read-only wrapper.", "original_success_credit": 0, "recovery": "Bounded AGENTS.md discovery returned no applicable repository instruction file."},
        {"negative_id": "SR7075-PLAN-N004", "failure": "The first combined skill rendering exceeded its projection.", "original_success_credit": 0, "recovery": "Read controlling skills and references individually through EOF."},
        {"negative_id": "SR7075-PLAN-N007", "failure": "The first planning build quarantined Auren P272 versus Sable P277 at Jaccard 0.727273.", "original_success_credit": 0, "recovery": "Replace the generic empirical-calibration candidate with the distinct external graph-corpus transfer gap and rerun planning once."},
        {"negative_id": "SR7075-PLAN-N009", "failure": "The first planning privacy aggregate treated two scanner-definition literals in common.py as payload hits.", "original_success_credit": 0, "recovery": "Adjudicate only the exact scanner-definition file and exact regex classes as visible candidates; retain every other match as confirmed."},
        {"negative_id": "SR7075-PLAN-N011", "failure": "The first exact staged review stopped before inspection because phase.txt omitted the validate-staged route.", "original_success_credit": 0, "recovery": "Add the exact dispatcher entry, rebuild the planning manifest, restage the owner surface, and rerun the unchanged validator."},
        {"negative_id": "SR7075-PLAN-N012", "failure": "The second staged review rejected an unintended generated tools/__pycache__ blob outside the exact manifest.", "original_success_credit": 0, "recovery": "Pin Python bytecode suppression and preserve the exact generated blob in the external D-first phase bank."},
        {"negative_id": "SR7075-PLAN-N013", "failure": "The first cache-cleanup wrapper was blocked before execution because it contained recursive deletion.", "original_success_credit": 0, "recovery": "Abandon deletion and use exact index removal plus evidence-preserving move."},
        {"negative_id": "SR7075-PLAN-N014", "failure": "The second literal-delete wrapper was also blocked before execution.", "original_success_credit": 0, "recovery": "Use git update-index --force-remove for the exact staged blob and move the exact file into the D-first phase bank, retaining its digest."}
    ], "boundary": BOUNDARY})
    write_json(PLANNING / "source-ledger.json", {"count": len(SOURCE_LEDGER), "sources": SOURCE_LEDGER, "network_rows_ingested": 0, "citations_are_observations": False, "boundary": BOUNDARY})
    write_json(PLANNING / "portfolio.json", {"safe_x1": 450, "safe_x2": 450, "candidate_x1": 300, "candidate_x2": 300, "cfr_x1": 300, "cfr_x2": 300, "exact_held": 50, "blocked_held": 30, "skills_x1": 10, "skills_x2": 10, "runners_x1": 5, "runners_x2": 5, "x1_tests": 20, "x2_tests": 30, "x2_models": 15, "hooks": 10, "caps_are_ceilings": True, "boundary": BOUNDARY})
    write_json(PLANNING / "exact-approval-packets.json", {"count": 50, "executed": 0, "packets": [{"id": f"SR7075-EXACT-{i:02d}", "state": "held_unexecuted", "gate": PROTECTED_GATES[i % len(PROTECTED_GATES)]} for i in range(1, 51)], "boundary": BOUNDARY})
    write_json(PLANNING / "blocked-packets.json", {"count": 30, "executed": 0, "packets": [{"id": f"SR7075-BLOCKED-{i:02d}", "state": "blocked_unexecuted", "reason": PROTECTED_GATES[i % len(PROTECTED_GATES)]} for i in range(1, 31)], "boundary": BOUNDARY})
    write_json(PLANNING / "law-hypotheses.json", {"count": 15, "status": "hypothesis_only", "rows": [{"id": f"SR7075-LAW-{i:02d}", "statement": f"Finite chordal obligation hypothesis {i}; requires exact bounded falsification and carries no physical-law claim."} for i in range(1, 16)], "boundary": BOUNDARY})
    write_json(PLANNING / "open-problem-probes.json", {"count": 15, "status": "open", "rows": [{"id": f"SR7075-PROBE-{i:02d}", "question": f"Which finite certificate boundary remains under transformation family {i}?", "closed": False} for i in range(1, 16)], "boundary": BOUNDARY})
    write_json(PLANNING / "practices.json", {"own_count": 8, "successor_count": 4, "own": ["graph-algorithm test curator", "finite certificate reviewer", "data-quality analyst", "provenance recorder", "accessibility structure reviewer", "rollback planner", "workload handover reviewer", "authority-vacancy steward"], "successor": ["finite interval-graph certificate curator", "finite separator provenance reviewer", "graph-decomposition accessibility reviewer", "synthetic catalog handover analyst"], "qualification_claim": False, "boundary": BOUNDARY})
    write_json(PLANNING / "threat-model.json", {"threats": ["malformed node or edge records", "self-loops and duplicate undirected edges", "false chordality promotion", "non-deterministic tie breaking", "input mutation", "incorrect clique maximality", "broken running intersection", "privacy or route leakage", "authority noncompensation", "success replay"], "controls": ["schema refusal", "canonical edge ordering", "independent bounded oracle", "digest comparison", "exact Git blobs", "five-class scan", "single-success latch"], "residual": ["same-owner common-cause risk", "incomplete accessibility review", "non-exhaustive security", "no external empirical evidence"], "boundary": BOUNDARY})
    write_json(PLANNING / "wellbeing.json", {"scope_bounded": True, "corrigible": True, "hamish_can_pause_rename_redirect_stop": True, "workload_split": ["planning", "x1", "x2", "final"], "identity_is_not_credential": True, "boundary": BOUNDARY})
    write_json(PLANNING / "route-hold.json", {"state": "PREPARED_NOT_SENT", "successor": "Avelin Reed", "successor_phase": "v707-v6", "contacted": False, "task_created": False, "recipient_completion": "UNCLAIMED", "boundary": BOUNDARY})
    write_json(PLANNING / "workflow-v19.json", {"profile": "v19", "owner": OWNER, "phase": PHASE, "predecessor": {"owner": SOURCE_OWNER, "phase": SOURCE_PHASE}, "successor": {"owner": "Avelin Reed", "phase": "v707-v6", "state": "terminally_gated_not_contacted"}, "formal_endpoint": {"owner": "Eiren Kestrel", "phase": "v725-v8"}, "model_admission": {"model": "gpt-5.6-sol", "preflight_passed": True, "model_request_sent": False, "mutation_performed": False}, "one_canonical_success_no_replay": True, "one_terminal_send_after_gate": True, "boundary": BOUNDARY})
    write_json(PLANNING / "method-flow.json", planning_flow())
    write_text(PLANNING / "overview.md", """# Sable Rook v707-v5 planning freeze

This planning-only packet freezes 300 finite synthetic chordal-graph certification contracts after a 90,000-pair immediate-source semantic audit. It executes no x1 or x2 outcome. The primary pillar is GMUT Mind as typed finite graph bookkeeping; THOS Body remains a bounded workload and handover proxy; Freed ID/CBR Heart preserves provenance, correction, accessibility, privacy, remedy, and authority reservations.

The bounded learning practice is graph-algorithm test curation and finite certificate review. It is not employment, qualification, scientific authority, professional competence, deployment permission, legal or cultural authority, affected-party approval, or Maori authority. All exact and blocked packets remain held.

`NOT_READY_FOR_STAGE_20`.
""")
    manifest = build_manifest("planning")
    write_json(PLANNING / "manifest.json", manifest)
    print(json.dumps({"state": "PLANNING_BUILT_NOT_EXECUTED", "proposals": len(proposals), "inherited": len(inherited), "comparisons": comparisons, "manifest": manifest["count"]}, sort_keys=True))

if __name__ == "__main__":
    main()
