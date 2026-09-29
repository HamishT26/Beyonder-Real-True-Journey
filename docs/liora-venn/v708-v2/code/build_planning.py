#!/usr/bin/env python3
"""Build only the frozen planning layer for Liora Venn v708-v2.

This builder deliberately creates no X1 or X2 implementation, observation, or
completion record. External inputs are read-only and are represented in output
through sanitized labels and digests rather than host-private absolute paths.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


PHASE = "v708-v2"
OWNER = "Liora Venn"
SOURCE_FINAL = "431f2774ca49373093809138811909755fcadbe7"
OWNER_BASE = "2f86f76169acfe9d9376b4400720434fa246ee7a"
BOUNDARY = (
    "Finite synthetic same-owner rough-set mathematical, software, and documentary "
    "evidence only. No real participant, dataset, measurement, classification, identity "
    "decision, professional act, legal or cultural interpretation, affected-party or "
    "Maori authority, empirical GMUT confirmation, production THOS or Freed ID, complete "
    "privacy or accessibility, exhaustive security, independent reproduction, AGI/ASI, "
    "consciousness/personhood, Theory-of-Everything, canon, or Stage 20 credit. "
    "NOT_READY_FOR_STAGE_20."
)


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def jaccard(a: str, b: str) -> float:
    left, right = tokens(a), tokens(b)
    if not left and not right:
        return 1.0
    return len(left & right) / len(left | right)


def project(
    number: int,
    title: str,
    stage: str,
    expected: str,
    hypothesis: str,
    failure: str,
    acceptance: str,
    artifacts: list[str],
    sources: list[str],
    gates: list[str],
) -> dict:
    return {
        "project_id": f"LI7082-P{number:02d}",
        "title": title,
        "stage": stage,
        "hypothesis": hypothesis,
        "null_or_failure_condition": failure,
        "approval_class": "safe_now_owner_scoped" if expected in {"completed", "represented"} else expected,
        "execution_lane": "owner_self_scoped_delta",
        "official_or_primary_source_needs": sources,
        "concrete_artifacts": artifacts,
        "acceptance_or_falsifier_gate": acceptance,
        "rollback_or_recovery": "Retain the failed subject at zero credit, correct only the smallest named dependency, and rerun only the unsatisfied check.",
        "protected_gates": gates,
        "expected_disposition": expected,
    }


PROJECTS = [
    project(1, "Decision-table shape and digest", "x1", "completed", "A bounded decision table can be normalized without changing row order or declared values.", "Duplicate object labels, unknown attributes, Boolean-as-integer values, or a changed digest are rejected.", "Independent shape and digest checks agree for all fifteen fixtures.", ["x1/code/rough_set.py", "x1/results/contracts.json"], ["pawlak-1991", "rfc8785"], ["no_real_data", "no_identity_decision"]),
    project(2, "Indiscernibility partition", "x1", "completed", "Equality on a declared attribute subset induces a deterministic partition of the finite universe.", "A block overlaps another block, omits an object, or changes under row permutation.", "Direct grouping and pairwise-equivalence closure return identical sorted blocks.", ["x1/results/contracts.json"], ["pawlak-1991"], ["no_empirical_promotion"]),
    project(3, "Target lower approximation", "x1", "completed", "The lower approximation is exactly the union of indiscernibility blocks contained in the target.", "Any included block crosses the target or any contained block is omitted.", "Block-union and object-neighborhood formulations agree.", ["x1/results/contracts.json"], ["pawlak-1991"], ["no_classification_authority"]),
    project(4, "Target upper approximation", "x1", "completed", "The upper approximation is exactly the union of blocks intersecting the target.", "An intersecting block is omitted or a disjoint block is included.", "Block-union and object-neighborhood formulations agree.", ["x1/results/contracts.json"], ["pawlak-1991"], ["no_classification_authority"]),
    project(5, "Boundary and negative regions", "x1", "completed", "Boundary and negative regions form the declared upper-minus-lower and universe-minus-upper sets.", "The three regions overlap incorrectly or fail their declared set identities.", "Exact set identities pass for all fixtures.", ["x1/results/contracts.json"], ["pawlak-1991"], ["no_empirical_promotion"]),
    project(6, "Approximation accuracy and rough membership", "x1", "completed", "Exact rational accuracy and neighborhood membership stay within their declared bounds.", "A denominator is zero without an explicit convention or a value falls outside zero through one.", "Fraction arithmetic and counted-set definitions agree.", ["x1/results/contracts.json", "x1/models"], ["pawlak-1991"], ["no_probability_claim"]),
    project(7, "Positive region and dependency degree", "x1", "completed", "The positive region is the union of lower approximations of decision classes and yields an exact rational dependency degree.", "Decision classes fail to partition known decisions or dependency leaves zero through one.", "Class-by-class and object-certainty formulations agree.", ["x1/results/contracts.json"], ["pawlak-1991"], ["no_causal_claim"]),
    project(8, "Discernibility matrix", "x1", "completed", "Pairs with different decisions expose the exact condition attributes that discern them.", "A same-decision pair contributes or a differing attribute is lost.", "Symmetry and direct attribute-difference checks pass.", ["x1/results/contracts.json"], ["pawlak-1991"], ["no_feature_selection_authority"]),
    project(9, "Minimal reduct enumeration", "x1", "completed", "For at most four condition attributes, exhaustive subsets can identify inclusion-minimal dependency-preserving reducts.", "A reported reduct does not preserve dependency or has a preserving proper subset.", "Exhaustive minimality witnesses pass under the declared cap.", ["x1/results/contracts.json"], ["pawlak-1991"], ["bounded_search_only"]),
    project(10, "Core attribute intersection", "x1", "completed", "The rough-set core is the exact intersection of all enumerated reducts.", "A core attribute is absent from a reduct or a universally present reduct attribute is omitted.", "Direct intersection and per-attribute necessity checks agree.", ["x1/results/contracts.json"], ["pawlak-1991"], ["bounded_search_only"]),
    project(11, "Decision consistency census", "x2", "completed", "Condition blocks can be labelled consistently, inconsistently, or partly unknown without erasing conflicts.", "A conflicting known decision is collapsed into a single label.", "Block decision sets and conflict witnesses match.", ["x2/results/contracts.json"], ["pawlak-1991", "prov-o"], ["conflict_nonerasure"]),
    project(12, "Pessimistic missing-value neighborhoods", "x2", "completed", "A declared conservative neighborhood can require known equality except for self-membership.", "Unknown values silently match nonself objects or symmetry fails.", "Pairwise neighborhood checks and declared relation properties pass.", ["x2/results/contracts.json"], ["pawlak-1991"], ["semantics_declared_not_standard_claim"]),
    project(13, "Optimistic missing-value neighborhoods", "x2", "completed", "A declared permissive neighborhood can match when either compared value is missing.", "Known unequal values match or symmetry fails.", "Pairwise checks pass and nontransitivity is reported rather than hidden.", ["x2/results/contracts.json"], ["pawlak-1991"], ["semantics_declared_not_standard_claim"]),
    project(14, "Finite dominance cones", "x2", "completed", "Known ordinal condition values induce bounded upward and downward dominance cones.", "Missing values are silently ordered or reflexivity fails on known rows.", "Direct pairwise and cone membership checks agree.", ["x2/results/contracts.json"], ["drsa-primary"], ["no_preference_authority"]),
    project(15, "Dominance approximation checks", "x2", "completed", "Declared upward and downward class unions admit exact finite lower and upper dominance approximations.", "The approximation uses the wrong cone orientation or violates lower-subset-upper.", "Dual orientation checks pass on all applicable fixtures.", ["x2/results/contracts.json"], ["drsa-primary"], ["no_decision_authority"]),
    project(16, "Refinement and correction lineage", "x2", "completed", "Adding condition attributes refines indiscernibility and corrections can preserve both original and replacement digests.", "A refined block crosses a coarse block or original evidence disappears.", "Refinement witnesses and PROV-style correction links validate.", ["x2/results/contracts.json"], ["prov-o", "rfc8785"], ["correction_nonerasure"]),
    project(17, "Accessible three-coordinate projections", "x2", "represented", "Lower size, boundary size, and upper size can be presented as a compact inspection aid.", "A coordinate is described as physical, empirical, or complete accessibility evidence.", "Fifteen X2 projections bind exact source results and carry an analogy firewall.", ["x2/models", "x2/accessible-overview.md"], ["wcag22"], ["no_physical_simulation_claim", "no_accessibility_complete_claim"]),
    project(18, "Empirical calibration vacancy", "x2", "open_gap", "Real measurement quality and decision utility require governed data and a preregistered evaluation.", "Synthetic fixtures are promoted into empirical calibration or professional validity.", "Remain open until governed real evidence, appropriate statistics, and independent review exist.", ["final/gate-register.json"], [], ["real_data_required", "independent_review_required"]),
    project(19, "Independent reproduction and affected-user evaluation vacancy", "x2", "open_gap", "Independent implementation and affected-user evaluation are needed for broader confidence.", "Same-owner tests or static structure are described as independent reproduction or complete accessibility.", "Remain open pending an independent team and affected-user accessibility review.", ["final/gate-register.json"], ["wcag22"], ["independent_team_required", "affected_user_review_required"]),
    project(20, "Classification, remedy, and cultural authority hold", "x2", "exact_gate", "Real classification, remedy, cultural interpretation, and Maori data decisions require competent and affected authority.", "Repository software is allowed to confer a right, identity, remedy, cultural legitimacy, or Maori authority.", "Remain unexecuted unless action-specific evidence and competent affected authority are present.", ["final/gate-register.json"], [], ["legal_authority", "affected_party_authority", "maori_authority"]),
]


FIXTURE_ROWS = [
    [(0, 0, 0, 0), (0, 0, 1, 0), (0, 1, 1, 1), (1, 1, 1, 1), (1, 2, 2, 2), (2, 2, 2, 2)],
    [(0, 1, 0, 0), (0, 1, 1, 0), (1, 1, 1, 1), (1, 2, 1, 1), (2, 2, 2, 2), (2, 1, 2, 2)],
    [(0, 0, 2, 0), (0, 1, 2, 1), (1, 1, 2, 1), (1, 2, 2, 2), (2, 2, 1, 2), (2, 0, 1, 1)],
    [(0, 0, 0, 0), (0, 0, 0, 1), (1, 0, 1, 1), (1, 1, 1, 1), (2, 1, 2, 2), (2, 2, 2, 2)],
    [(0, 2, 0, 0), (0, 2, 1, 0), (1, 2, 1, 1), (1, 1, 1, 1), (2, 1, 2, 2), (2, 0, 2, 2)],
    [(0, 0, 1, 0), (0, 1, 1, 1), (1, 1, 0, 1), (1, 2, 0, 2), (2, 2, 1, 2), (2, 2, 2, 2)],
    [(0, 1, 2, 0), (0, 1, 2, 0), (1, 1, 1, 1), (1, 1, 2, 2), (2, 2, 2, 2), (2, 0, 0, 1)],
    [(0, 0, 0, 0), (0, 1, 0, 0), (1, 1, 0, 1), (1, 1, 1, 1), (2, 1, 1, 2), (2, 2, 1, 2)],
    [(0, 2, 2, 0), (0, 2, 1, 1), (1, 2, 1, 1), (1, 1, 1, 2), (2, 1, 0, 2), (2, 0, 0, 2)],
    [(0, 0, 2, 0), (0, 0, 1, 0), (1, 0, 1, 1), (1, 1, 2, 1), (2, 1, 2, 2), (2, 2, 2, 2)],
    [(0, 1, 0, 0), (0, 1, 0, 1), (1, 1, 1, 1), (1, 2, 1, 2), (2, 2, 1, 2), (2, 2, 2, 2)],
    [(0, 0, 0, 0), (0, 1, 1, 0), (1, 0, 1, 1), (1, 2, 1, 1), (2, 2, 2, 2), (2, 1, 2, 2)],
    [(0, 2, 0, 0), (0, 1, 0, 0), (1, 1, 1, 1), (1, 0, 2, 1), (2, 1, 2, 2), (2, 2, 2, 2)],
    [(0, 0, 1, 0), (0, 1, 2, 1), (1, 1, 2, 1), (1, 2, 2, 2), (2, 2, 2, 2), (2, 0, 0, 1)],
    [(0, 1, 1, 0), (0, 1, 2, 0), (1, 1, 2, 1), (1, 2, 2, 2), (2, 2, 2, 2), (2, 0, 1, 1)],
]


def build_fixtures() -> list[dict]:
    fixtures = []
    for index, source_rows in enumerate(FIXTURE_ROWS, start=1):
        rows = []
        for row_index, (a, b, c, decision) in enumerate(source_rows, start=1):
            values: dict[str, object] = {"a": a, "b": b, "c": c}
            if index >= 6 and (row_index + index) % 5 == 0:
                values["c"] = "?"
            if index >= 11 and (row_index * index) % 7 == 0:
                values["b"] = "?"
            rows.append({"object": f"O{row_index}", "conditions": values, "decision": decision})
        target = [row["object"] for row in rows if row["decision"] >= (2 if index % 3 == 0 else 1)]
        fixtures.append({
            "fixture_id": f"RS{index:02d}",
            "condition_attributes": ["a", "b", "c"],
            "decision_attribute": "d",
            "rows": rows,
            "target": target,
            "target_rule": "declared decision threshold used only to build this synthetic target",
            "synthetic": True,
            "real_data_rows": 0,
        })
    return fixtures


SOURCES = [
    {"source_id": "pawlak-1991", "title": "Rough Sets: Theoretical Aspects of Reasoning about Data", "url": "https://doi.org/10.1007/978-94-011-3534-4", "kind": "primary monograph", "used_for": ["approximation spaces", "decision tables", "reduct and dependency vocabulary"], "not_used_as": ["observation", "endorsement", "authority grant"]},
    {"source_id": "drsa-primary", "title": "Dominance-based rough set approach as a proper way of handling graduality in rough set theory", "url": "https://doi.org/10.1007/978-3-540-73451-2_3", "kind": "primary research chapter", "used_for": ["dominance cone and class-union vocabulary"], "not_used_as": ["real preference", "decision authority", "measurement"]},
    {"source_id": "prov-o", "title": "PROV-O: The PROV Ontology", "url": "https://www.w3.org/TR/prov-o/", "kind": "W3C Recommendation", "used_for": ["entity", "activity", "derivation", "revision", "bundle vocabulary"], "not_used_as": ["proof that repository records are externally governed provenance"]},
    {"source_id": "rfc8785", "title": "RFC 8785: JSON Canonicalization Scheme", "url": "https://www.rfc-editor.org/rfc/rfc8785.html", "kind": "RFC Independent Stream", "used_for": ["canonical JSON digest discipline"], "not_used_as": ["signature", "identity", "security certification"]},
    {"source_id": "wcag22", "title": "Web Content Accessibility Guidelines 2.2", "url": "https://www.w3.org/TR/WCAG22/", "kind": "W3C Recommendation", "used_for": ["static accessibility structure and reservation vocabulary"], "not_used_as": ["complete accessibility conformance", "affected-user evaluation"]},
]


RECENT = [
    ("Ceryn Alder", "v708-v1", "431f2774ca49373093809138811909755fcadbe7", "bounded THOS evidence-admission tickets, atomic nonce schedules, cold replay, and retained route overlays"),
    ("Orin Thale", "v707-v8", "9d3a13198622436743ef7dae418ec2fdca4c08be", "interval and affine-form abstraction with a lifecycle-correct additive terminal correction"),
    ("Caelen Ash", "v707-v7", "9507b8dd848901d2be997797d90a52525c0b2c32", "finite event-ledger publication-time permission, conflict retention, and two bounded consultations"),
    ("Avelin Reed", "v707-v6-r2", "0c6481a043fe896271c80732aeaacb4f40a3fa7b", "shared D-first laboratory, persistent source intake, and advisory workflow"),
    ("Avelin Reed", "v707-v6", "06f54492a7da636205b0e85184d2d2fa33286134", "finite transformation monoids and a held remaster transition"),
    ("Sable Rook", "v707-v5", "0cbf2e1ebfe2e6dd4b040ce62b12ebb8e3ac0297", "finite chordal-graph certificates and compacted commit-local result aggregates"),
    ("Neris Solane", "v706-v6", "b31f70e1f824d3ba45d329af96c03db7c7c5b220", "directed arborescence enumeration and outgoing-Laplacian cofactors"),
    ("Rowan Ash", "v706-v5", "40b1f340fc1acdbc47934107748004c63427811a", "finite rook and hit-number certificates with independent same-owner formulations"),
    ("Elaren Kestrel", "v706-v4", "68747f691fb037d42bf5845e5e6bb1a47f1f346b", "exact integer partitions, conjugation, hooks, and bounded ranking"),
    ("Eiren Kestrel", "v706-v3", "6b7189a71c0f2c8616d6a3f713ac31de25128df8", "continued fractions, exact rational recurrences, and bounded denominator search"),
]


STARTUP_FAILURES = [
    ("LI7082-START-N001", "PowerShell rejected a pipeline immediately after foreach before the skill line-count projection ran.", "Materialize the foreach result array before ConvertTo-Json."),
    ("LI7082-START-N002", "PowerShell rejected an embedded Git command and LASTEXITCODE expression in the source verification probe.", "Run the Git command, then read LASTEXITCODE as a separate scalar step."),
    ("LI7082-START-N003", "The first per-file raw Git-blob parity wrapper completed without returning its projection.", "Use one persistent git cat-file batch stream."),
    ("LI7082-START-N004", "The first Python recovery command had an unterminated quoted string and executed no validation.", "Pass literal Python through a PowerShell here-string."),
    ("LI7082-START-N005", "The corrected per-file process wrapper again completed without a visible projection.", "Replace hundreds of process launches with a single streamed batch process."),
    ("LI7082-START-N006", "A worktree inventory variable collided with PowerShell's automatic Matches hashtable.", "Use a non-reserved variable name and materialize strings explicitly."),
    ("LI7082-START-N007", "A capability-search orchestration cell mixed PowerShell syntax into JavaScript and failed before launch.", "Keep JavaScript orchestration and PowerShell command text in their correct language boundaries."),
]


LAW_HYPOTHESES = [
    "Lower approximation is a subset of target, which is a subset of upper approximation for every declared equivalence fixture.",
    "Boundary emptiness coincides with exact definability for the declared target and partition.",
    "Approximation accuracy is an exact rational in the closed interval from zero to one.",
    "Rough membership equals the exact target fraction of an object's declared neighborhood.",
    "Positive-region size never exceeds universe size.",
    "Adding known condition attributes cannot merge previously distinct indiscernibility blocks.",
    "Dependency degree under a superset of known condition attributes does not decrease on a fixed complete table.",
    "Every enumerated reduct preserves the full-condition dependency degree.",
    "No proper subset of an enumerated reduct preserves that dependency degree.",
    "The core is the intersection of all bounded enumerated reducts.",
    "The optimistic missing-value upper neighborhood contains the pessimistic counterpart under the declared semantics.",
    "Pessimistic and optimistic compatibility are symmetric under the declared finite definitions.",
    "Known-value dominance is reflexive and transitive on its admitted rows.",
    "Dominance lower approximation remains a subset of its corresponding upper approximation.",
    "A correction bundle can preserve the original digest while binding a replacement digest and stated reason.",
]


OPEN_PROBES = [
    "How do reduct enumeration costs scale beyond the four-attribute cap without losing exact minimality witnesses?",
    "Which missing-value semantics are appropriate for a specific governed domain and why?",
    "Can an independently authored implementation reproduce every finite result and counterexample?",
    "How should dynamic object insertion preserve correction lineage and invalidate cached approximations?",
    "What privacy model is required before any real decision table can be admitted?",
    "How should affected people contest a reduct-backed explanation or classification?",
    "Which accessibility checks require keyboard, zoom, screen-reader, cognitive, and affected-user evaluation?",
    "How can multilingual technical terms be reviewed without flattening cultural meaning?",
    "What Māori data-governance authority and tikanga processes would be required for any relevant real data?",
    "How should fairness and disparate impact be evaluated without treating rough membership as a probability?",
    "What independent security review is necessary for production identity or remedy workflows?",
    "Can provenance constraints expose contradictory correction branches without choosing an authority winner?",
    "What observations would be needed before any GMUT analogy could become a physical model claim?",
    "What governed participant study would be needed before THOS workflow-effectiveness claims?",
    "What trust, appeal, recovery, and competent-authority structure would be needed for Freed ID or CBR use?",
]


PRACTICES = [
    {"practice": "knowledge-representation analysis", "learning_only": True},
    {"practice": "archival description and correction lineage", "learning_only": True},
    {"practice": "measurement-provenance review", "learning_only": True},
    {"practice": "software verification", "learning_only": True},
    {"practice": "accessible technical communication", "learning_only": True},
    {"practice": "public-policy evidence review", "learning_only": True},
    {"practice": "data-governance boundary analysis", "learning_only": True},
    {"practice": "philosophy of science and classification", "learning_only": True},
]


SUCCESSOR_PRACTICES = [
    "formal-methods specification review",
    "measurement-system provenance analysis",
    "participatory human-factors evaluation planning",
    "Māori data-governance study under Māori authority",
]


def method_flow() -> dict:
    methods, witnesses = [], []
    for index, (negative_id, failure, recovery) in enumerate(STARTUP_FAILURES, start=1):
        method_id = f"LI7082-START-M{index:03d}"
        fail_id, pass_id = f"{method_id}-W001", f"{method_id}-W002"
        methods.append({
            "method_id": method_id,
            "title": f"Startup recovery for {negative_id}",
            "failure_signature": failure,
            "trigger_preconditions": ["Liora v708-v2 startup", "read-only pre-mutation probe"],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped",
            "candidate_workaround": recovery,
            "validation_witness_ids": [fail_id, pass_id],
            "recurrence_guard": recovery,
            "rollback": "Return to the last clean owner head and preserve the failed probe.",
            "recommendation_state": "validated",
            "supersedes": [],
            "protected_gates": ["no_failure_erasure", "no_source_mutation", "no_stage20"],
            "retained_negative_ids": [negative_id],
            "scope_boundary": BOUNDARY,
        })
        witnesses.extend([
            {"witness_id": fail_id, "method_id": method_id, "procedure": "original startup observation", "scope": "read-only startup", "expected": "bounded observable result", "observed": failure, "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": BOUNDARY},
            {"witness_id": pass_id, "method_id": method_id, "procedure": "smallest isolated recovery", "scope": "read-only startup", "expected": "bounded observable result without repository mutation", "observed": recovery, "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": BOUNDARY},
        ])
    return {
        "schema": "ghc.family.method-flow-state.v1",
        "phase": PHASE + "-planning",
        "owner": OWNER,
        "identity_boundary": "Relational working name only; no consciousness, personhood, continuity, employment, qualification, agency, or authority evidence.",
        "execution_authority": "owner_self_scoped_delta",
        "methods": methods,
        "witnesses": witnesses,
        "state_events": [],
        "recommendations": [],
        "counts": {"methods": len(methods), "witnesses": len(witnesses), "state_events": 0, "recommendations": 0, "states": {"observed": 0, "candidate": 0, "validated": len(methods), "preferred": 0, "superseded": 0, "deprecated": 0}, "witness_results": {"pass": len(methods), "fail": len(methods)}},
        "boundary": BOUNDARY,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--labs", required=True)
    parser.add_argument("--workflow", required=True)
    parser.add_argument("--roster", required=True)
    parser.add_argument("--authorization", required=True)
    parser.add_argument("--consultation", required=True)
    args = parser.parse_args()

    root = Path(args.root)
    planning = root / "planning"
    labs_raw = Path(args.labs).read_bytes()
    labs = json.loads(labs_raw)
    controls = {}
    for label, value in (("workflow", args.workflow), ("roster", args.roster), ("authorization", args.authorization), ("consultation", args.consultation)):
        raw = Path(value).read_bytes()
        parsed = json.loads(raw)
        controls[label] = {"schema": parsed.get("schema"), "sha256": sha256_bytes(raw), "source_label": f"current-{label}-v20"}

    fixtures = build_fixtures()
    lab_records = [{"id": item["id"], "owner": item["owner"], "phase": item["phase"], "topic": item["topic"], "source_head": item["source_head"], "inherited_execution_credit": 0} for item in labs]
    similarities = []
    for proposal in PROJECTS:
        best = max(lab_records, key=lambda item: jaccard(proposal["title"], item["topic"]))
        similarities.append({"project_id": proposal["project_id"], "nearest_lab_id": best["id"], "token_jaccard": round(jaccard(proposal["title"], best["topic"]), 6)})

    write_text(root / "README.md", f"""# Liora Venn {PHASE}

This owner-main contribution is a finite rough-set approximation and evidence-boundary laboratory. Planning is frozen before X1, and X1 must be pushed and fresh-four-way equal before X2 begins. Ceryn Alder `{SOURCE_FINAL}` is content provenance; the existing Liora owner head `{OWNER_BASE}` is the Git parent. No false ancestry, inherited completion credit, or source replay is permitted.

Liora's relational phase role is **granularity-and-falsifier cartographer**, with the hope that uncertainty boundaries remain inspectable without being converted into scientific, professional, identity, legal, cultural, affected-party, or Māori authority. This is working language only.

{BOUNDARY}
""")
    write_json(planning / "activation.json", {
        "schema": "liora.activation.v708-v2.v1", "owner": OWNER, "phase": PHASE,
        "relational_role": "granularity-and-falsifier cartographer",
        "relational_hope": "Make uncertainty boundaries inspectable without converting them into authority.",
        "identity_boundary": "Relational working language only; no consciousness, personhood, continuity, employment, qualification, agency, or authority evidence.",
        "source_content_provenance": SOURCE_FINAL, "owner_git_parent": OWNER_BASE,
        "source_is_git_parent": False, "selected_baseline_fold_count": 1,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": BOUNDARY,
    })
    write_json(planning / "controls.json", {"schema": "liora.controls.v708-v2.v1", "controls": controls, "workflow_interpretation": {"initial_projects": 20, "project_cap": 80, "minimum_models_each_session": 15, "adviser_messages": {"x1": 1, "x2": 1}, "full_repository_suite": False, "new_tasks_or_subagents": False}, "boundary": BOUNDARY})
    write_json(planning / "source-provenance.json", {
        "schema": "liora.source-provenance.v708-v2.v1", "source_owner": "Ceryn Alder", "source_phase": "v708-v1", "source_final": SOURCE_FINAL,
        "source_branch": "codex/GHC-Family/ceryn-alder-main", "source_as_content_provenance": True, "source_as_git_parent": False,
        "repository_sealed_baseline": {"methods": 6933, "witnesses": 314781, "passing": 242285, "failed": 72496, "effective_negatives": 81329, "open_gaps": 2511, "exact_gate_obligations": 2871},
        "external_terminal_overlay": {"methods": 1, "witnesses": 4, "passing": 2, "failed": 2, "effective_negatives": 2, "open_gaps": 0, "exact_gate_obligations": 0},
        "selected_terminal_effective_baseline": {"methods": 6934, "witnesses": 314785, "passing": 242287, "failed": 72498, "effective_negatives": 81331, "open_gaps": 2511, "exact_gate_obligations": 2871},
        "fold_overlay_once": True, "rewrite_source_seal": False, "source_executions": 0, "source_canonical_replays": 0,
        "source_manifest_reverification": {"planning": 36, "x1": 93, "x2": 155, "final": 171, "mismatches": 0},
        "boundary": BOUNDARY,
    })
    write_json(planning / "projects.json", {"schema": "liora.projects.v708-v2.v1", "count": len(PROJECTS), "cap": 80, "projects": PROJECTS, "outcomes_expected": {"completed": 16, "represented": 1, "open_gap": 2, "exact_gate": 1}, "boundary": BOUNDARY})
    write_json(planning / "fixtures.json", {"schema": "liora.rough-set-fixtures.v1", "count": len(fixtures), "fixtures": fixtures, "boundary": BOUNDARY})
    write_json(planning / "sources.json", {"schema": "liora.sources.v708-v2.v1", "sources": SOURCES, "source_ceiling": "Vocabulary, definitions, and refusal conditions only; citations are not observations, endorsements, qualifications, or authority grants.", "boundary": BOUNDARY})
    write_json(planning / "recent-overviews.json", {"schema": "liora.recent-overviews.v708-v2.v1", "count": len(RECENT), "records": [{"owner": o, "phase": p, "source_head": h, "bounded_learning": s, "execution_credit": 0} for o, p, h, s in RECENT], "boundary": BOUNDARY})
    write_json(planning / "prior-laboratories.json", {"schema": "liora.prior-laboratories.v708-v2.v1", "release_label": "avelin-v707-v6-r2-review-1", "source_sha256": sha256_bytes(labs_raw), "count": len(lab_records), "records": lab_records, "inherited_execution_credit": 0, "boundary": BOUNDARY})
    write_json(planning / "semantic-neighbor-audit.json", {"schema": "liora.semantic-neighbor-audit.v708-v2.v1", "scope": {"laboratory_cards": len(lab_records), "recent_overviews": len(RECENT), "installed_skill_exact_query": {"rough-set": 0, "oriented-matroid": 0, "measurement provenance": 0}}, "project_neighbors": similarities, "maximum_token_jaccard": max(item["token_jaccard"] for item in similarities), "exact_title_collisions": 0, "universal_novelty_claim": False, "reason": "The bounded accessible corpus cannot prove absence from all historic branches, repositories, paraphrases, or literature.", "boundary": BOUNDARY})
    write_json(planning / "portfolio-freeze.json", {
        "schema": "liora.portfolio.v708-v2.v1", "projects": 20,
        "x1": {"contracts": 150, "safe": 150, "candidate_failed_subjects": 150, "refusal_witnesses": 150, "clean_fix_refine": 150, "skills": 5, "runners": 3, "tests_planned": 25, "models": 15, "adviser_messages": 1},
        "x2": {"contracts": 150, "safe": 150, "candidate_failed_subjects": 150, "refusal_witnesses": 150, "clean_fix_refine": 150, "skills": 5, "runners": 3, "tests_planned": 35, "models": 15, "adviser_messages": 1},
        "held_exact_packets": 10, "held_blocked_packets": 5, "hooks_reused": ["source", "budget", "consultation", "roster", "evidence"],
        "caps_are_ceilings_not_quotas": True, "no_x1_or_x2_execution_in_planning": True, "boundary": BOUNDARY,
    })
    write_json(planning / "law-hypotheses.json", {"schema": "liora.law-hypotheses.v708-v2.v1", "label": "finite engineering hypotheses, not fundamental laws", "count": 15, "hypotheses": [{"id": f"LI7082-H{i:02d}", "statement": text, "status": "to_test_bounded"} for i, text in enumerate(LAW_HYPOTHESES, 1)], "boundary": BOUNDARY})
    write_json(planning / "open-problem-probes.json", {"schema": "liora.open-problem-probes.v708-v2.v1", "count": 15, "solution_claims": 0, "probes": [{"id": f"LI7082-Q{i:02d}", "question": text, "status": "open"} for i, text in enumerate(OPEN_PROBES, 1)], "boundary": BOUNDARY})
    write_json(planning / "practices.json", {"schema": "liora.practices.v708-v2.v1", "owner_practices": PRACTICES, "successor_recommendations": SUCCESSOR_PRACTICES, "qualification_claims": 0, "boundary": BOUNDARY})
    write_json(planning / "skill-runner-ideas.json", {"schema": "liora.skill-runner-ideas.v708-v2.v1", "x1_skills": ["table envelope", "indiscernibility partition", "approximations", "accuracy and membership", "dependency and reducts"], "x2_skills": ["consistency", "missingness", "dominance", "correction lineage", "evidence reservations"], "x1_runners": ["structure", "approximation", "portfolio"], "x2_runners": ["missingness", "dominance", "evidence"], "successor_skill_ideas": ["granular provenance", "rough-set counterexample pack", "participatory explanation reservation", "dynamic approximation diff", "authority-vacancy audit"], "successor_runner_ideas": ["independent formulation comparer", "source-bound model loader", "affected-user evaluation planner", "correction-lineage checker", "terminal evidence reducer"], "boundary": BOUNDARY})
    write_json(planning / "held-exact.json", {"schema": "liora.held-exact.v708-v2.v1", "count": 10, "executed": 0, "packets": [{"id": f"LI7082-EXACT-{i:02d}", "topic": topic, "state": "exact_gate"} for i, topic in enumerate(["real classification", "identity lifecycle", "production deployment", "professional decision", "legal interpretation", "cultural interpretation", "affected-party remedy", "Maori wording", "Maori data governance", "Stage 20 claim"], 1)], "boundary": BOUNDARY})
    write_json(planning / "held-blocked.json", {"schema": "liora.held-blocked.v708-v2.v1", "count": 5, "executed": 0, "packets": [{"id": f"LI7082-BLOCK-{i:02d}", "topic": topic, "state": "blocked"} for i, topic in enumerate(["destructive cross-lane cleanup", "credential or account mutation", "administrator elevation", "unbounded real-person data intake", "wholesale skill-bank merge without caller proof"], 1)], "boundary": BOUNDARY})
    write_json(planning / "hook-plan.json", {"schema": "liora.hook-plan.v708-v2.v1", "hooks": ["source", "budget", "consultation", "roster", "evidence"], "reuse_current_v20_hooks": True, "duplicate_hooks_created": 0, "manual_smokes_planned_each_session": 10, "live_host_claim": False, "boundary": BOUNDARY})
    write_json(planning / "consultation-plan.json", {"schema": "liora.consultation-plan.v708-v2.v1", "reviewer_title": "Review and refine GHC Lab", "private_target_exported": False, "x1_messages": 1, "x2_messages": 1, "no_resend_after_accepted_pending_opaque_or_unresolved": True, "x1_question": "Review the proposed finite rough-set laboratory and identify the strongest discriminating counterexample for reduct preservation, missing-value semantics, or authority nonpromotion.", "x2_question": "Review the saved bounded results and recommend one correction or additional falsifier without promoting same-owner evidence into empirical, professional, or authority credit.", "boundary": BOUNDARY})
    flow = method_flow()
    write_json(planning / "method-flow.json", flow)
    write_json(planning / "failure-ledger.json", {"schema": "liora.failures.v708-v2.v1", "count": len(STARTUP_FAILURES), "failures": [{"id": i, "stage": "startup", "failure": f, "recovery": r, "original_success_credit": 0, "retained": True} for i, f, r in STARTUP_FAILURES], "boundary": BOUNDARY})
    write_json(planning / "plan.json", {"schema": "liora.plan.v708-v2.v1", "owner": OWNER, "phase": PHASE, "primary_pillar": "GMUT Mind", "secondary_pillars": ["THOS Body", "Freed ID and CBR Heart"], "domain": "finite rough-set approximation and evidence-boundary laboratory", "planning_only": True, "x1_execution_present": False, "x2_execution_present": False, "projects": 20, "fixtures": 15, "models_each_session": 15, "source_content": SOURCE_FINAL, "git_parent": OWNER_BASE, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": BOUNDARY})
    write_text(planning / "freeze.md", f"""# Liora Venn {PHASE} planning freeze

This commit freezes twenty initial projects and fifteen wholly synthetic decision-table fixtures before X1. It includes no X1 or X2 implementation, saved domain result, observed outcome, completion claim, skill package, runner package, canonical receipt, or successor activation.

The primary pillar is GMUT Mind through finite exact approximation structures and explicit falsifiers. THOS Body is limited to bounded executable envelopes and recovery discipline. Freed ID and CBR Heart preserve provenance, correction, disclosure restraint, remedy vacancy, and authority holds. None of these structures establishes a real physical theory, operating system, identity system, right, remedy, cultural legitimacy, or authority.

Ceryn Alder `{SOURCE_FINAL}` is read-only content provenance and supplies the selected terminal-effective baseline exactly once. The Liora Git parent is `{OWNER_BASE}`. Source validation and Ceryn's successful canonical are inherited evidence only and are not replayed or counted as Liora work.

The X1 adviser request and all X1 execution remain prospective. After this planning commit is pushed, clean, zero-divergent, and fresh-four-way equal, X1 may begin. X2 may begin only after the same gate closes for X1.

{BOUNDARY}

LITERAL_EOF_LIORA_V708_V2_PLANNING
""")

    generated = sorted(p for p in root.rglob("*") if p.is_file())
    write_json(planning / "build-receipt.json", {"schema": "liora.planning-build.v708-v2.v1", "files_before_manifest": len(generated), "projects": len(PROJECTS), "fixtures": len(fixtures), "laboratory_cards": len(lab_records), "recent_overviews": len(RECENT), "startup_failures": len(STARTUP_FAILURES), "x1_execution": 0, "x2_execution": 0, "boundary": BOUNDARY})


if __name__ == "__main__":
    main()
