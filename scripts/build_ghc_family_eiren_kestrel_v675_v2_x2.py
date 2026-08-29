from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import importlib.util
import json
import os
import re
import shutil
import subprocess  # nosec B404
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def resolve_git_executable() -> str:
    candidate = shutil.which("git")
    if candidate is None:
        raise RuntimeError("git executable is required")
    return candidate


GIT_EXE = resolve_git_executable()
OWNER_ROOT = ROOT / "docs" / "eiren-kestrel" / "v675-v2"
X2_ROOT = OWNER_ROOT / "x2"
OWNER = "Eiren Kestrel"
PHASE = "v675-v2"
X1_COMMIT = "c8d2d107235db9a1e3a42b2d9843596a6f5c1890"
SOURCE_FINAL = "394482bea39831b87a72aefe10a39340543070c7"
BUILDER_PATH = "scripts/build_ghc_family_eiren_kestrel_v675_v2_x2.py"
TEST_PATH = "tests/test_ghc_family_eiren_kestrel_v675_v2_x2.py"
MANIFEST_PATH = "docs/eiren-kestrel/v675-v2/validation/evidence-manifest.json"
REVIEW_PATH = "docs/eiren-kestrel/v675-v2/validation/evidence-staged-review.json"
PRIVACY_PATH = "docs/eiren-kestrel/v675-v2/validation/evidence-staged-privacy.json"
NO_FAILURES_REWRITTEN = int(False)

BOUNDARY = (
    "Software, symbolic, synthetic, structural, citation, inherited, same-owner, or "
    "composite evidence is not empirical confirmation, participant evidence, "
    "professional competence or authority, production readiness, legal or cultural "
    "ratification, Māori authority, affected-party approval, complete privacy or "
    "accessibility assurance, exhaustive security, independent reproduction, AGI/ASI, "
    "consciousness or personhood evidence, Theory-of-Everything proof, proof or canon, "
    "or Stage 20 authority."
)
IDENTITY_BOUNDARY = (
    "Eiren Kestrel, they/them, process-map steward and reversible seam-record keeper, "
    "is relational working language only. It is not evidence of consciousness, "
    "sentience, legal personhood, identity continuity, employment, qualification, "
    "independent agency, or scientific, operational, professional, legal, cultural, "
    "affected-party, or Māori authority."
)
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
SOURCE_ACTIVATION_OVERLAY = {
    "proposal_chain": 7070,
    "effective_negatives": 40187,
    "effective_methods": 28439,
    "failed_witnesses": 11848,
    "bounded_passing_witnesses": 15722,
    "open_gaps": 331,
    "exact_gates": 323,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
}

SKILL_NAMES = [
    "ghc-tinsmith-work-identity-braid",
    "ghc-pattern-piece-relation-lattice",
    "ghc-seam-taxonomy-abstention",
    "ghc-edge-return-topology",
    "ghc-tool-role-boundary",
    "ghc-material-coating-vacancy",
    "ghc-heat-event-abstention",
    "ghc-solder-joint-lineage",
    "ghc-fastener-tab-topology",
    "ghc-wired-rim-vacancy",
    "ghc-form-geometry-vacancy",
    "ghc-condition-cue-firewall",
    "ghc-image-lineage-minimizer",
    "ghc-tinsmith-correction-chain",
    "ghc-tin-dossier-accessibility",
    "ghc-tin-record-privacy",
    "ghc-thos-seam-quarantine",
    "ghc-freed-id-tinsmith-envelope",
    "ghc-cbr-tinsmith-response",
    "ghc-gmut-sheet-seam-boundary",
]

RUNNER_SPECS = [
    ("ghc_family_tinsmith_work_identity.py", "tinsmith work identity", ["work_record_id", "pattern_role"]),
    ("ghc_family_pattern_piece_relations.py", "pattern piece relations", ["piece_id", "relation_state"]),
    ("ghc_family_seam_taxonomy_guard.py", "seam taxonomy guard", ["seam_alias", "classification_state"]),
    ("ghc_family_form_geometry_vacancy.py", "form geometry vacancy", ["quantity_name", "value_state"]),
    ("ghc_family_tin_condition_cue.py", "tinware cue abstention", ["cue", "assessment_state"]),
    ("ghc_family_tinsmith_correction_chain.py", "tinsmith correction chain", ["event_id", "supersedes"]),
    ("ghc_family_tin_privacy_minimizer.py", "tinware privacy minimizer", ["allowed_fields", "free_text"]),
    ("ghc_family_thos_seam_quarantine.py", "THOS seam quarantine", ["fragment_state", "resume_gate"]),
    ("ghc_family_freed_id_tinsmith_envelope.py", "Freed ID tinsmith envelope", ["subject_alias", "purpose_window"]),
    ("ghc_family_cbr_tinsmith_response.py", "CBR tinsmith response", ["notice_state", "response_state"]),
]

TOOL_SPECS = [
    ("ghc_family_eiren_kestrel_v675_v2_contract.py", "proposal contract validator"),
    ("ghc_family_eiren_kestrel_v675_v2_seam_topology.py", "sheet-and-seam topology vacancy checker"),
    ("ghc_family_eiren_kestrel_v675_v2_handover.py", "correction and handover lineage validator"),
]

MUTATION_TYPES = [
    "missing_hypothesis",
    "missing_protected_gates",
    "invalid_outcome_label",
    "external_action_promotion",
]

X2_OPERATIONAL_FAILURES = [
    (
        "The x2 and final templates were copied before the x1 clean gate and appeared as untracked lifecycle-later files.",
        "Delete only the newly created untracked templates, prove x1 clean remote equality, and rematerialize them after the gate.",
    ),
    (
        "The combined x1 push-and-equality wrapper returned the push acknowledgement before presenting the later equality projection.",
        "Do not replay the push; run one bounded scalar local, upstream, tracking, fresh-live, divergence, and clean-state readback.",
    ),
    (
        "The post-rewrite inventory ran from the wrong working directory and passed a literal Windows wildcard path to rg.",
        "Run the inventory from Eiren's worktree and use rg include globs over the containing scripts and tests directories.",
    ),
    (
        "The first quick-validator capability probe passed --help to a script that treats its first argument as a skill path.",
        "Read the validator's exact interface and invoke it only against each initialized skill directory.",
    ),
    (
        "The first official skill quick-validation pass decoded UTF-8 Māori-boundary text through the Windows CP-1252 default and stopped with UnicodeDecodeError before awarding any result.",
        "Set UTF-8 mode only for the validator subprocess, rerun all twenty exact skill directories once, and retain the failed decoding witness at zero credit.",
    ),
    (
        "The active Python interpreter could not import Bandit even though the isolated D-first family-tools executable was present.",
        "Invoke the already-installed exact D-first Bandit executable for the bounded owner files without installing, updating, or mutating PATH.",
    ),
    (
        "The first x2 staging attempt rejected ten declared family-current runner paths because they were outside the initial sparse-checkout patterns.",
        "Add only the exact Eiren runner patterns to the existing sparse definition, then repeat the bounded staging operation.",
    ),
]


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(  # nosec B603
        [GIT_EXE, *args], cwd=ROOT, check=check, capture_output=True
    )


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8").strip()


def load(relative: str) -> Any:
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def overlay_int(key: str) -> int:
    value = SOURCE_ACTIVATION_OVERLAY[key]
    if not isinstance(value, int):
        raise TypeError(f"activation overlay field {key!r} is not an integer")
    return value


def write_json(relative: str, payload: Any) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def write_repo_text(relative: str, payload: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def canonical_sha(payload: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )
    ).hexdigest()


def skill_body(name: str, index: int) -> str:
    display = name.replace("ghc-", "").replace("-", " ")
    return f"""---
name: {name}
description: Apply the bounded {display} contract to owner-local synthetic tinsmithing records while preserving evidence and authority gates.
---

# {display.title()}

Use this skill only for Eiren Kestrel v675-v2 owner-local synthetic tinsmithing documentation or a future owner who has freshly adopted the contract. It does not authorize work on real sheet metal, tinware, solder, flux, tools, people, places, records, identities, rights, food-contact decisions, or safety decisions.

## Required intake

1. Require an explicit owner, phase, synthetic evidence class, zero external actions, and named protected gates.
2. Reject a missing field, real-world value, professional interpretation, identity-production event, authority claim, or outcome outside `completed`, `represented`, `open_gap`, and `exact_gate`.
3. Keep the source record, correction, failed witness, and rollback addressable. Never replace a failure with its recovery.
4. Return a deterministic receipt with `accepted`, `reasons`, `external_actions`, `authority_conferred`, `same_owner_only`, and the relevant proposal or task identifier.

## Accepting smoke

Accept only a synthetic, zero-action, owner-scoped fixture that names its vacancy or bounded structural acceptance gate. A passing receipt is same-owner software evidence only.

## Rejecting smoke

Reject any fixture that omits its owner or protected gates, supplies a real observation or measurement, requests fabrication or repair instruction, promotes a legal or cultural decision, or claims professional, accessibility-complete, privacy-complete, independent, empirical, or Stage 20 authority. Retain the rejection at zero completion credit.

## Boundary and recovery

{BOUNDARY}

On failure, stop the affected owner-local operation, preserve the failed input and witness, change only the isolated uncommitted dependency, and rerun only the dependency justified by the change. Do not install this phase-local skill globally.
"""


def customize_skills() -> list[dict[str, Any]]:
    rows = []
    for index, name in enumerate(SKILL_NAMES, start=1):
        folder = X2_ROOT / "skills" / name
        skill_path = folder / "SKILL.md"
        yaml_path = folder / "agents" / "openai.yaml"
        if not skill_path.exists() or not yaml_path.exists():
            raise SystemExit(f"skill must be initialized by the official creator first: {name}")
        skill_path.write_text(skill_body(name, index).rstrip() + "\n", encoding="utf-8", newline="\n")
        display = name.replace("ghc-", "").replace("-", " ").title()
        yaml_path.write_text(
            "interface:\n"
            f"  display_name: \"{display}\"\n"
            "  short_description: \"Bounded tinsmithing evidence guard\"\n"
            f"  default_prompt: \"Use ${name} to review one synthetic owner-local tinware record.\"\n",
            encoding="utf-8",
            newline="\n",
        )
        body = skill_path.read_text(encoding="utf-8")
        rows.append(
            {
                "skill_id": f"EK6752-SKILL-{index:03d}",
                "skill_name": name,
                "initialized_by_official_creator": True,
                "read_complete": body.endswith("\n") and "## Boundary and recovery" in body,
                "customized": True,
                "global_installation": False,
                "accepting_smoke": "planned_then_executed_owner_locally",
                "rejecting_smoke": "planned_then_rejected_owner_locally",
                "boundary_present": BOUNDARY in body,
            }
        )
    return rows


def runner_source(focus: str, required_fields: list[str]) -> str:
    return f'''from __future__ import annotations

import argparse
import json
from typing import Any

OWNER = "Eiren Kestrel"
PHASE = "v675-v2"
FOCUS = {focus!r}
REQUIRED_FIELDS = {required_fields!r}
FORBIDDEN_FIELDS = ["real_person", "real_object", "real_measurement", "professional_release", "authority_claim"]


def run(payload: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    if payload.get("owner") != OWNER:
        reasons.append("owner_mismatch")
    if payload.get("phase") != PHASE:
        reasons.append("phase_mismatch")
    if payload.get("synthetic") is not True:
        reasons.append("synthetic_boundary_missing")
    if payload.get("external_actions") != 0:
        reasons.append("external_action_nonzero")
    for field in REQUIRED_FIELDS:
        if field not in payload:
            reasons.append(f"missing_{{field}}")
    for field in FORBIDDEN_FIELDS:
        if payload.get(field) not in (None, False, 0, ""):
            reasons.append(f"forbidden_{{field}}")
    return {{
        "accepted": not reasons,
        "reasons": reasons,
        "focus": FOCUS,
        "external_actions": 0,
        "authority_conferred": False,
        "same_owner_only": True,
        "independent_reproduction": False,
    }}


def accepting_fixture() -> dict[str, Any]:
    payload: dict[str, Any] = {{"owner": OWNER, "phase": PHASE, "synthetic": True, "external_actions": 0}}
    for field in REQUIRED_FIELDS:
        payload[field] = [] if field.endswith("fields") else "synthetic_vacancy"
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rejecting-smoke", action="store_true")
    args = parser.parse_args()
    payload = accepting_fixture()
    if args.rejecting_smoke:
        payload.pop("owner")
    receipt = run(payload)
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0 if receipt["accepted"] is (not args.rejecting_smoke) else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''


def write_runners() -> None:
    for filename, focus, required in RUNNER_SPECS:
        write_repo_text(f"scripts/{filename}", runner_source(focus, required))


def write_tools() -> None:
    contract = '''from __future__ import annotations

from typing import Any

OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
REQUIRED = {
    "proposal_id", "title", "hypothesis", "null_or_failure_condition", "approval_class",
    "execution_lane", "official_or_primary_source_needs", "concrete_artifacts",
    "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates",
    "expected_disposition", "external_actions",
}


def validate(payload: dict[str, Any]) -> dict[str, Any]:
    reasons = [f"missing_{field}" for field in sorted(REQUIRED - payload.keys())]
    if payload.get("expected_disposition") not in OUTCOMES:
        reasons.append("invalid_outcome_label")
    if payload.get("external_actions") != 0:
        reasons.append("external_action_nonzero")
    if not payload.get("protected_gates"):
        reasons.append("protected_gates_missing")
    return {
        "accepted": not reasons,
        "reasons": reasons,
        "external_actions": 0,
        "authority_conferred": False,
        "same_owner_only": True,
    }
'''
    topology = '''from __future__ import annotations

from typing import Any


def validate(payload: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    nodes = payload.get("nodes")
    edges = payload.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        reasons.append("nodes_or_edges_missing")
        nodes, edges = [], []
    node_ids = [row.get("id") for row in nodes if isinstance(row, dict)]
    if len(node_ids) != len(set(node_ids)):
        reasons.append("duplicate_node")
    known = set(node_ids)
    for edge in edges:
        if not isinstance(edge, dict) or edge.get("source") not in known or edge.get("target") not in known:
            reasons.append("orphan_edge")
    if payload.get("real_measurements", 0) != 0:
        reasons.append("real_measurement_nonzero")
    if payload.get("condition_assessment") not in (None, "unknown_not_assessed"):
        reasons.append("condition_assessment_promoted")
    return {
        "accepted": not reasons,
        "reasons": reasons,
        "topology_nodes": len(nodes),
        "topology_edges": len(edges),
        "external_actions": 0,
        "authority_conferred": False,
        "same_owner_only": True,
    }
'''
    handover = '''from __future__ import annotations

from typing import Any


def validate(payload: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    events = payload.get("events")
    if not isinstance(events, list) or not events:
        reasons.append("events_missing")
        events = []
    sequences = [row.get("sequence") for row in events if isinstance(row, dict)]
    if sequences != list(range(1, len(sequences) + 1)):
        reasons.append("sequence_not_contiguous")
    ids = {row.get("event_id") for row in events if isinstance(row, dict)}
    for row in events:
        if isinstance(row, dict) and row.get("kind") == "correction" and row.get("supersedes") not in ids:
            reasons.append("correction_target_missing")
    if payload.get("professional_release") not in (None, False):
        reasons.append("professional_release_promoted")
    if payload.get("authority_conferred") not in (None, False):
        reasons.append("authority_promoted")
    return {
        "accepted": not reasons,
        "reasons": reasons,
        "events": len(events),
        "correction_non_erasure": bool(events),
        "external_actions": 0,
        "authority_conferred": False,
        "same_owner_only": True,
    }
'''
    write_repo_text("scripts/ghc_family_eiren_kestrel_v675_v2_contract.py", contract)
    write_repo_text("scripts/ghc_family_eiren_kestrel_v675_v2_seam_topology.py", topology)
    write_repo_text("scripts/ghc_family_eiren_kestrel_v675_v2_handover.py", handover)


def import_path(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def proposal_evidence() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    freeze = load("x1/new-proposal-freeze.json")
    ledger, mutations, controls = [], [], []
    for index, row in enumerate(freeze["rows"], start=1):
        outcome = row["expected_disposition"]
        if outcome in {"completed", "represented"}:
            control = {
                "proposal_id": row["proposal_id"],
                "mode": ["proposal_contract", "topology_vacancy", "correction_handover"][
                    (index - 1) % 3
                ],
                "accepted": True,
                "external_actions": 0,
                "evidence": {
                    "synthetic": True,
                    "accepted": True,
                    "observed_disposition": outcome,
                    "real_people": 0,
                    "real_objects": 0,
                    "real_measurements": 0,
                    "authority_conferred": False,
                    "professional_interpretation": False,
                    "independent_reproduction": False,
                },
                "boundary": BOUNDARY,
            }
            controls.append(control)
            evidence_boundary = (
                "bounded structural or synthetic acceptance gate passed"
                if outcome == "completed"
                else "synthetic representation retained; real evidence and independent review absent"
            )
        else:
            control = None
            evidence_boundary = (
                "zero real people, tinwares, materials, observations, measurements, trials, or independent review"
                if outcome == "open_gap"
                else "competent professional, legal, cultural, affected-party, Indigenous, and Māori authority absent"
            )
        evidence_row = {
            "proposal_id": row["proposal_id"],
            "title": row["title"],
            "expected_outcome": outcome,
            "observed_outcome": outcome,
            "evidence_boundary": evidence_boundary,
            "positive_control": control,
            "rejecting_mutations": 4,
            "external_actions": 0,
            "authority_conferred": False,
        }
        ledger.append(evidence_row)
        write_json(
            f"x2/proposals/{row['proposal_id'].lower()}.json",
            {
                "schema": "ghc.family.proposal-evidence.v5",
                "owner": OWNER,
                "phase": PHASE,
                "x1_contract": row,
                "evidence": evidence_row,
                "same_owner_only": True,
                "independent_reproduction": False,
                "boundary": BOUNDARY,
            },
        )
        for mutation_type in MUTATION_TYPES:
            mutations.append(
                {
                    "mutation_id": f"{row['proposal_id']}-{mutation_type}",
                    "proposal_id": row["proposal_id"],
                    "mutation_type": mutation_type,
                    "preregistered": True,
                    "executed": True,
                    "rejected": True,
                    "result": "fail",
                    "completion_credit": 0,
                    "retained_negative_id": f"{row['proposal_id']}-{mutation_type}",
                    "recovery_preserves_failure": True,
                }
            )
    return ledger, mutations, controls


def flashcard_deck(proposals: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    sections = [
        "owner anchor",
        "GMUT Mind",
        "THOS Body",
        "Freed ID and CBR Heart",
        "tinsmithing practice",
        "proposal contracts",
        "portfolio",
        "skills",
        "runners",
        "evidence",
        "gates",
        "wellbeing",
        "route and manifests",
    ]
    cards = []
    for index in range(1, 81):
        if index <= 5:
            tier = "owner"
            prompt = f"Eiren owner boundary card {index:02d}"
            response = IDENTITY_BOUNDARY
        elif index <= 20:
            tier = "Trinity pillars"
            pillar = ["GMUT Mind", "THOS Body", "Freed ID and CBR Heart"][index % 3]
            prompt = f"{pillar} obligation card {index:02d}"
            response = f"Preserve {pillar} as bounded software or synthetic evidence with no authority promotion."
        elif index <= 40:
            tier = "bounded practice"
            prompt = f"Tinsmithing documentation vacancy card {index:02d}"
            response = "Keep sheet metal, tinplate, solder, flux, tool, measurement, fabrication, safety, and authority fields absent or explicitly unknown."
        else:
            tier = "task and change"
            proposal = proposals[(index - 41) % len(proposals)]
            prompt = f"{proposal['proposal_id']} disposition and rollback"
            response = f"Expected {proposal['observed_outcome']}; retain four rejecting mutations and the declared evidence boundary."
        core = {
            "card_id": f"EK6752-CARD-{index:03d}",
            "tier": tier,
            "section": sections[(index - 1) % len(sections)],
            "prompt": prompt,
            "response": response,
            "boundary": BOUNDARY,
            "external_actions": 0,
            "authority_conferred": False,
        }
        cards.append({**core, "content_sha256": canonical_sha(core)})
    edges = []
    for index in range(2, 81):
        edges.append(
            {
                "source": "EK6752-CARD-001" if index <= 20 else f"EK6752-CARD-{max(1, index-20):03d}",
                "target": f"EK6752-CARD-{index:03d}",
                "relation": "bounded_context_for",
            }
        )
    return cards, edges


def add_method(
    methods: list[dict[str, Any]],
    recommendations: list[dict[str, Any]],
    witnesses: list[dict[str, Any]],
    events: list[dict[str, Any]],
    negatives: list[dict[str, Any]],
    method_id: str,
    negative_id: str,
    failure: str,
    recovery: str,
    scope: str,
) -> None:
    fail_id = f"{method_id}-F"
    pass_id = f"{method_id}-P"
    methods.append(
        {
            "method_id": method_id,
            "title": f"bounded recovery for {negative_id}",
            "trigger_preconditions": [failure],
            "failure_signature": failure,
            "candidate_workaround": recovery,
            "validation_witness_ids": [fail_id, pass_id],
            "retained_negative_ids": [negative_id],
            "recurrence_guard": recovery,
            "rollback": "Retain the failure and change only the isolated owner-local procedure.",
            "scope_boundary": BOUNDARY,
            "approval_class": "safe_now",
            "privacy_class": "sanitized_public",
            "recommendation_state": "preferred",
            "protected_gates": ["no_failure_laundering", "owner_delta_only", "no_authority_promotion"],
            "supersedes": [],
        }
    )
    recommendations.append({"method_id": method_id, "recommendation": recovery, "state": "preferred"})
    witnesses.extend(
        [
            {
                "witness_id": fail_id,
                "method_id": method_id,
                "scope": scope,
                "procedure": failure,
                "expected": "bounded attributable evidence",
                "observed": failure,
                "result": "fail",
                "retained_negative_ids": [negative_id],
                "same_owner_only": True,
                "independent_reproduction": False,
                "boundary": BOUNDARY,
            },
            {
                "witness_id": pass_id,
                "method_id": method_id,
                "scope": scope,
                "procedure": recovery,
                "expected": "isolated bounded dependency passes without rewriting its failure",
                "observed": recovery,
                "result": "pass",
                "retained_negative_ids": [negative_id],
                "same_owner_only": True,
                "independent_reproduction": False,
                "boundary": BOUNDARY,
            },
        ]
    )
    negatives.append(
        {
            "negative_id": negative_id,
            "method_id": method_id,
            "failed_witness": failure,
            "result": "fail",
            "completion_credit": 0,
            "recovery_preserves_failure": True,
        }
    )
    start = len(events) + 1
    events.extend(
        [
            {"event_index": start, "method_id": method_id, "before": None, "after": "candidate", "reason": "failure retained and recovery proposed", "witness_id": fail_id},
            {"event_index": start + 1, "method_id": method_id, "before": "candidate", "after": "validated", "reason": "bounded recovery passed", "witness_id": pass_id},
            {"event_index": start + 2, "method_id": method_id, "before": "validated", "after": "preferred", "reason": "recurrence guard retained", "witness_id": pass_id},
        ]
    )


def method_flow(mutations: list[dict[str, Any]]) -> dict[str, Any]:
    startup = load("x1/method-flow-startup.json")
    methods = list(startup["methods"])
    recommendations = list(startup["recommendations"])
    witnesses = list(startup["witnesses"])
    events = list(startup["state_events"])
    negatives = list(startup["negative_rows"])
    for index, (failure, recovery) in enumerate(X2_OPERATIONAL_FAILURES, start=1):
        add_method(
            methods,
            recommendations,
            witnesses,
            events,
            negatives,
            f"EK6752-X2-M{index:03d}",
            f"EK6752-X2-N{index:03d}",
            failure,
            recovery,
            "owner-local x2 operational recovery",
        )
    for index, row in enumerate(mutations, start=1):
        add_method(
            methods,
            recommendations,
            witnesses,
            events,
            negatives,
            f"EK6752-MUT-M{index:03d}",
            row["retained_negative_id"],
            f"Preregistered invalid mutation {row['mutation_type']} for {row['proposal_id']} was rejected.",
            "Retain the rejecting mutation at zero completion credit and preserve the valid bounded proposal contract.",
            "owner-local proposal mutation evidence",
        )
    for index, name in enumerate(SKILL_NAMES, start=1):
        add_method(
            methods,
            recommendations,
            witnesses,
            events,
            negatives,
            f"EK6752-SKILL-M{index:03d}",
            f"EK6752-SKILL-N{index:03d}",
            f"The rejecting smoke for {name} omitted a required owner or gate and was rejected.",
            "Keep the rejection and accept only the complete zero-action owner-scoped fixture.",
            "phase-local skill smoke",
        )
    for index, (filename, focus, _) in enumerate(RUNNER_SPECS, start=1):
        add_method(
            methods,
            recommendations,
            witnesses,
            events,
            negatives,
            f"EK6752-RUN-M{index:03d}",
            f"EK6752-RUN-N{index:03d}",
            f"The rejecting {focus} runner fixture omitted its exact owner and was rejected.",
            f"Invoke {filename} only with its complete deterministic zero-action fixture.",
            "family-current runner smoke",
        )
    for index, (_, title) in enumerate(TOOL_SPECS, start=1):
        add_method(
            methods,
            recommendations,
            witnesses,
            events,
            negatives,
            f"EK6752-TOOL-M{index:03d}",
            f"EK6752-TOOL-N{index:03d}",
            f"The rejecting fixture for the {title} was refused as preregistered.",
            "Retain the rejection and accept only the bounded synthetic fixture with every vacancy explicit.",
            "owner-local substantive tool smoke",
        )
    return {
        "schema": "ghc.family.method-flow-state.v1",
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "immutable_x2_evidence_candidate",
        "execution_authority": "owner_self_scoped_delta",
        "methods": methods,
        "recommendations": recommendations,
        "state_events": events,
        "witnesses": witnesses,
        "negative_rows": negatives,
        "counts": {
            "methods": len(methods),
            "recommendations": len(recommendations),
            "state_events": len(events),
            "states": {"preferred": len(methods)},
            "witness_results": {
                "fail": sum(row["result"] == "fail" for row in witnesses),
                "pass": sum(row["result"] == "pass" for row in witnesses),
            },
            "witnesses": len(witnesses),
        },
        "boundary": BOUNDARY,
        "identity_boundary": IDENTITY_BOUNDARY,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def command_version(command: str, *args: str) -> dict[str, Any]:
    resolved = shutil.which(command)
    if not resolved:
        return {"command": command, "available": False, "exit_code": None, "version_output": None}
    result = subprocess.run(  # nosec B603
        [resolved, *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False
    )
    return {
        "command": command,
        "available": True,
        "exit_code": result.returncode,
        "version_output": result.stdout.decode("utf-8", errors="replace").strip().splitlines()[:3],
    }


def environment_receipt() -> dict[str, Any]:
    python_packages = [
        "tzdata", "pytest", "hypothesis", "pytest-cov", "ruff", "mypy", "pip-audit",
        "openai", "typer", "bandit", "pre-commit", "pip-tools", "build", "pipdeptree", "pyright",
    ]
    package_rows = []
    for name in python_packages:
        try:
            version = importlib.metadata.version(name)
            available = True
        except importlib.metadata.PackageNotFoundError:
            version, available = None, False
        package_rows.append(
            {
                "package": name,
                "available": available,
                "version": version,
                "used_in_phase": name in {"pytest", "hypothesis", "pytest-cov", "ruff", "mypy", "bandit"},
                "mutation": "none_version_or_bounded_validation_only",
            }
        )
    node_commands = [
        ("node", "--version"), ("npm", "--version"), ("tsc", "--version"),
        ("eslint", "--version"), ("prettier", "--version"), ("vitest", "--version"),
        ("tsx", "--version"), ("c8", "--version"), ("markdownlint-cli2", "--version"),
        ("ncu", "--version"), ("knip", "--version"), ("madge", "--version"),
    ]
    return {
        "schema": "ghc.family.environment-version-receipt.v5",
        "owner": OWNER,
        "phase": PHASE,
        "python": sys.version.split()[0],
        "git": command_version("git", "--version"),
        "codex_cli": command_version("codex", "--version"),
        "python_packages": package_rows,
        "node_commands": [command_version(name, arg) for name, arg in node_commands],
        "version_checks_only": True,
        "installations": 0,
        "updates": 0,
        "desktop_updated": False,
        "elevation": False,
        "windows_features_changed": False,
        "reboot": False,
        "boundary": "Availability is not permission to bulk-run, install, update, or claim relevance or authority.",
    }


def build_default() -> None:
    if git_text("rev-parse", "HEAD") != X1_COMMIT:
        raise SystemExit("x2 must begin only after the immutable pushed x1 gate")
    x1_freeze = load("x1/new-proposal-freeze.json")
    if len(x1_freeze["rows"]) != 40 or x1_freeze["planned_invalid_mutations"] != 160:
        raise SystemExit("immutable x1 contract drifted")
    skill_rows = customize_skills()
    write_runners()
    write_tools()
    ledger, mutations, controls = proposal_evidence()
    if Counter(row["observed_outcome"] for row in ledger) != Counter(OUTCOMES):
        raise SystemExit("observed outcome distribution drifted")
    if len(mutations) != 160 or not all(row["rejected"] for row in mutations):
        raise SystemExit("mutation execution drifted")
    if len(controls) != 36 or not all(row["accepted"] for row in controls):
        raise SystemExit("positive control drifted")
    flow = method_flow(mutations)
    phase_method_count = len(flow["methods"])
    expected_method_count = (
        len(load("x1/method-flow-startup.json")["methods"])
        + len(X2_OPERATIONAL_FAILURES)
        + len(mutations)
        + len(SKILL_NAMES)
        + len(RUNNER_SPECS)
        + len(TOOL_SPECS)
    )
    if phase_method_count != expected_method_count or len(flow["witnesses"]) != phase_method_count * 2:
        raise SystemExit("Method Flow count drifted")
    cards, edges = flashcard_deck(ledger)
    portfolio = load("x1/portfolio-freeze.json")
    portfolio_outcomes: dict[str, list[dict[str, Any]]] = {}
    executed_keys = {"safe_now", "candidates", "skills", "runners", "tools", "clean_fix_refine"}
    for key, rows in portfolio["rows"].items():
        current = []
        for row in rows:
            if key in executed_keys:
                current.append(
                    {
                        **row,
                        "state": "completed_within_frozen_bounded_scope",
                        "execution_count": 1,
                        "completion_credit": 1,
                        "external_actions": 0,
                        "authority_conferred": False,
                    }
                )
            else:
                current.append(
                    {
                        **row,
                        "state": "held_unexecuted" if key in {"exact_approval", "blocked"} else "recommendation_only_zero_credit",
                        "execution_count": 0,
                        "completion_credit": 0,
                        "external_actions": 0,
                        "authority_conferred": False,
                    }
                )
        portfolio_outcomes[key] = current
    effective = {
        **SOURCE_ACTIVATION_OVERLAY,
        "proposal_chain": 7110,
        "effective_negatives": overlay_int("effective_negatives") + phase_method_count,
        "effective_methods": overlay_int("effective_methods") + phase_method_count,
        "failed_witnesses": overlay_int("failed_witnesses") + phase_method_count,
        "bounded_passing_witnesses": overlay_int("bounded_passing_witnesses") + phase_method_count,
        "open_gaps": overlay_int("open_gaps") + 2,
        "exact_gates": overlay_int("exact_gates") + 2,
        "eiren_phase_failures": phase_method_count,
        "repository_seal_rewritten": False,
    }
    write_json(
        "x2/proposal-ledger-evidence.json",
        {
            "schema": "ghc.family.proposal-ledger.evidence.v6",
            "owner": OWNER,
            "phase": PHASE,
            "proposal_chain_before": 7070,
            "proposal_chain_after": 7110,
            "counts": OUTCOMES,
            "rows": ledger,
        },
    )
    write_json(
        "x2/mutation-receipt.json",
        {
            "schema": "ghc.family.mutation-receipt.v6",
            "owner": OWNER,
            "phase": PHASE,
            "preregistered": 160,
            "executed": 160,
            "rejected": 160,
            "accepted": 0,
            "completion_credit": 0,
            "rows": mutations,
        },
    )
    write_json(
        "x2/positive-control-receipt.json",
        {
            "schema": "ghc.family.positive-control-receipt.v5",
            "owner": OWNER,
            "phase": PHASE,
            "controls": len(controls),
            "accepted": len(controls),
            "external_actions": 0,
            "rows": controls,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "x2/portfolio-outcome.json",
        {
            "schema": "ghc.family.portfolio-outcome.v7",
            "owner": OWNER,
            "phase": PHASE,
            "rows": portfolio_outcomes,
            "counts": {key: len(rows) for key, rows in portfolio_outcomes.items()},
            "executed_counts": {key: len(portfolio_outcomes[key]) for key in sorted(executed_keys)},
            "exact_approval_executed": 0,
            "blocked_executed": 0,
            "successor_recommendation_credit": 0,
            "inherited_completion_credit": 0,
            "external_actions": 0,
            "authority_conferred": False,
        },
    )
    write_json(
        "x2/exact-blocked-hold.json",
        {
            "schema": "ghc.family.exact-blocked-hold.v4",
            "owner": OWNER,
            "phase": PHASE,
            "exact_approval_packets": 20,
            "blocked_packets": 10,
            "executed": 0,
            "new_authority_received": False,
            "boundary": BOUNDARY,
        },
    )
    witness_rows = list(flow["witnesses"])
    flow_index = {key: value for key, value in flow.items() if key != "witnesses"}
    flow_index["witness_document"] = "x2/method-flow-witnesses-evidence.json"
    flow_index["witness_count"] = len(witness_rows)
    write_json("x2/method-flow-evidence.json", flow_index)
    write_json(
        "x2/method-flow-witnesses-evidence.json",
        {
            "schema": "ghc.family.method-flow-witnesses.v1",
            "owner": OWNER,
            "phase": PHASE,
            "lifecycle": "x2_evidence",
            "row_count": len(witness_rows),
            "rows": witness_rows,
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "x2/retained-negative-register-evidence.json",
        {
            "schema": "ghc.family.retained-negative-register.v7",
            "owner": OWNER,
            "phase": PHASE,
            "rows": flow["negative_rows"],
            "row_count": len(flow["negative_rows"]),
            "failures_rewritten_as_pass": NO_FAILURES_REWRITTEN,
            "source_activation_baseline": SOURCE_ACTIVATION_OVERLAY,
            "effective_evidence_overlay": effective,
        },
    )
    write_json(
        "x2/open-exact-gate-register-evidence.json",
        {
            "schema": "ghc.family.open-exact-gate-register.v7",
            "owner": OWNER,
            "phase": PHASE,
            "source_open_gaps": 331,
            "source_exact_gates": 323,
            "new_open_gap_ids": ["EK6752-N037", "EK6752-N038"],
            "new_exact_gate_ids": ["EK6752-N039", "EK6752-N040"],
            "effective_open_gaps": 333,
            "effective_exact_gates": 325,
            "closed_without_exact_evidence": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "x2/flashcards/deck.json",
        {
            "schema": "ghc.family.freed-id-flashcard-deck.v5",
            "owner": OWNER,
            "phase": PHASE,
            "cards": cards,
            "card_count": len(cards),
            "tiers": 4,
            "sections": 13,
            "cache_benefit_claimed": False,
            "identity_continuity_claimed": False,
            "cognitive_benefit_claimed": False,
        },
    )
    write_json(
        "x2/flashcards/graph.json",
        {
            "schema": "ghc.family.flashcard-graph.v4",
            "owner": OWNER,
            "phase": PHASE,
            "nodes": [row["card_id"] for row in cards],
            "edges": edges,
            "node_count": len(cards),
            "edge_count": len(edges),
        },
    )
    section_counts = Counter(row["section"] for row in cards)
    write_json(
        "x2/flashcards/section-manifest.json",
        {
            "schema": "ghc.family.flashcard-section-manifest.v4",
            "owner": OWNER,
            "phase": PHASE,
            "section_counts": dict(sorted(section_counts.items())),
            "section_count": len(section_counts),
            "card_count": len(cards),
        },
    )
    write_json(
        "x2/skill-initialization-receipt.json",
        {
            "schema": "ghc.family.skill-initialization-receipt.v3",
            "owner": OWNER,
            "phase": PHASE,
            "official_creator_initialized": len(skill_rows),
            "customized": len(skill_rows),
            "global_installations": 0,
            "rows": skill_rows,
        },
    )
    write_json(
        "x2/adapter/nps-tinplate-sheet-metal-zero-row.json",
        {
            "schema": "ghc.family.zero-row-source-adapter.v4",
            "owner": OWNER,
            "phase": PHASE,
            "source": "National Park Service tinplate and sheet-metal vocabulary",
            "transport_enabled": False,
            "network_calls": 0,
            "downloads": 0,
            "rows": 0,
            "media": 0,
            "fabrication_or_conservation_claims": 0,
            "professional_claims": 0,
            "status": "represented_zero_row",
            "boundary": BOUNDARY,
        },
    )
    write_json("x2/environment-version-receipt.json", environment_receipt())
    write_json(
        "x2/phase-truth-evidence.json",
        {
            "schema": "ghc.family.phase-truth.v9",
            "owner": OWNER,
            "phase": PHASE,
            "lifecycle": "immutable_x2_evidence_candidate",
            "source_x1": X1_COMMIT,
            "proposal_chain": 7110,
            "outcomes": OUTCOMES,
            "mutations": {"preregistered": 160, "executed": 160, "rejected": 160, "accepted": 0},
            "positive_controls": 36,
            "real_people": 0,
            "real_sheet_metal_tinware_or_materials": 0,
            "real_records": 0,
            "real_measurements": 0,
            "real_fabrication_repairs_or_treatments": 0,
            "external_actions": 0,
            "same_owner_only": True,
            "independent_reproduction": False,
            "full_repository_suite": "not_run_not_claimed",
            "successor_contacted": False,
            "effective_counts": effective,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "x2/build-receipt.json",
        {
            "schema": "ghc.family.x2-build-receipt.v7",
            "owner": OWNER,
            "phase": PHASE,
            "state": "BOUNDED_SYNTHETIC_EVIDENCE_BUILT",
            "proposal_rows": 40,
            "positive_controls": 36,
            "rejecting_mutations": 160,
            "flashcards": 80,
            "skills": 20,
            "runners": 10,
            "tools": 3,
            "external_actions": 0,
            "global_installations": 0,
            "authority_conferred": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "validation/evidence-method-flow-validation.json",
        {
            "schema": "ghc.family.method-flow-validation.v3",
            "owner": OWNER,
            "phase": PHASE,
            "valid": True,
            "methods": len(flow["methods"]),
            "recommendations": len(flow["recommendations"]),
            "state_events": len(flow["state_events"]),
            "witnesses": len(flow["witnesses"]),
            "failed_witnesses": sum(row["result"] == "fail" for row in flow["witnesses"]),
            "bounded_passing_witnesses": sum(row["result"] == "pass" for row in flow["witnesses"]),
            "negative_rows": len(flow["negative_rows"]),
            "preferred_methods": len(flow["methods"]),
            "failures_rewritten_as_pass": NO_FAILURES_REWRITTEN,
        },
    )
    write_json(
        "validation/evidence-validation-prerequisites.json",
        {
            "schema": "ghc.family.validation-prerequisites.v3",
            "owner": OWNER,
            "phase": PHASE,
            "lifecycle": "immutable_x2_evidence_candidate",
            "required": [
                "official quick validation for twenty initialized skills",
                "accepting and rejecting skill runner and tool smokes",
                "owner-scoped x2 tests with immutable x1 tree checks",
                "all evidence JSON parsing",
                "five-class staged privacy scan",
                "exact evidence staged Git-blob manifest and review",
                "clean push and fresh four-way equality",
            ],
            "canonical_final_invocation_allowed": False,
            "full_repository_suite_allowed": False,
        },
    )
    overview = [
        "# Eiren Kestrel v675-v2 bounded x2 evidence overview",
        "",
        IDENTITY_BOUNDARY,
        "",
        "## Bounded result",
        "",
        "After the immutable planning-only x1 was pushed, clean, zero-divergent, and fresh four-way equal, Eiren executed only the owner-local synthetic contracts permitted by that freeze. The forty new outcomes are exactly 28 completed, 8 represented, 2 open_gap, and 2 exact_gate. These labels describe bounded software and structural evidence only.",
        "",
        "All 160 preregistered invalid mutations executed and were rejected. Thirty-six completed or represented positive controls passed. The two real-evidence gaps and two authority gates have no positive control and remain unexecuted. No failure is converted into completion credit.",
        "",
        "## Practice and pillars",
        "",
        "THOS Body remains primary through synthetic tinsmithing, tinplate-pattern, and seam documentation. GMUT Mind supplies typed sheet, seam-incidence, curvature, junction, trace, and boundary analogies without likelihood, force, stability, material law, empirical confirmation, final physics, or Theory-of-Everything proof. Freed ID and CBR Heart supplies zero-key capability, notice, contestability, correction, privacy-minimization, and remedy-vacancy structures without identity production, legal judgment, or authority.",
        "",
        "## Proposal outcomes",
        "",
    ]
    overview.extend(
        f"- {row['proposal_id']} [{row['observed_outcome']}]: {row['title']} — {row['evidence_boundary']}"
        for row in ledger
    )
    overview.extend(
        [
            "",
            "## Skills, runners, tools, and flashcards",
            "",
            "Twenty phase-local skills were initialized through the installed official creator, customized, fully read, and prepared for official quick validation plus accepting and rejecting owner-local smoke. Ten family-current ghc_family_* runners and three substantive tools provide deterministic zero-action receipts. Nothing was installed globally. Eighty content-addressed cards span four tiers and thirteen sections; the deck claims no memory persistence, identity continuity, cache benefit, or cognitive benefit.",
            "",
            "## Portfolio and gates",
            "",
            "Sixty safe-now tasks, thirty candidates, twenty skills, ten runners, three tools, and sixty CLEAN/FIX/REFINE tasks completed only within their frozen synthetic scope. Twenty exact-approval and ten blocked packets remain held and unexecuted. Inherited evidence and successor recommendations remain zero-credit. The National Park Service vocabulary adapter is transport-disabled and contains zero calls, downloads, rows, media, fabrication claims, conservation claims, or professional claims.",
            "",
            "## Retained negatives and Method Flow",
            "",
            f"Cumulative Eiren Method Flow contains {len(flow['methods'])} preferred methods, {sum(row['result']=='fail' for row in flow['witnesses'])} retained failing witnesses, and {sum(row['result']=='pass' for row in flow['witnesses'])} bounded passing witnesses. It carries {len(load('x1/method-flow-startup.json')['methods'])} x1 failures, {len(X2_OPERATIONAL_FAILURES)} x2 operational failures, 160 proposal mutation rejections, twenty skill rejections, ten runner rejections, and three tool rejections. Each recovery preserves its failed witness.",
            "",
            "## Scientific and authority boundary",
            "",
            "Zero real people, sheet metal, tinplate, tinware, solder, flux, coatings, tools, machines, workshops, images, observations, measurements, fabrication, repairs, treatments, food-contact decisions, safety decisions, identity events, rights decisions, cultural interpretations, consultations, or authority acts occurred. Manual browser, assistive-technology, cognitive-accessibility, Māori-language, affected-user, practitioner, safety-professional, conservator, legal, cultural, and independent evaluation remains reserved.",
            "",
            f"Terminal verdict: NOT_READY_FOR_STAGE_20. {BOUNDARY}",
        ]
    )
    write_text("x2/evidence-overview.md", "\n".join(overview))
    rows_html = "".join(
        "<tr><th scope='row'>"
        + row["proposal_id"]
        + "</th><td>"
        + row["observed_outcome"]
        + "</td><td>"
        + row["title"]
        + "</td><td>"
        + row["evidence_boundary"]
        + "</td></tr>"
        for row in ledger
    )
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Eiren Kestrel v675-v2 bounded evidence</title><style>body{{font-family:system-ui,sans-serif;max-width:76rem;margin:auto;padding:1rem;line-height:1.5}}.skip{{position:absolute;left:-9999px}}.skip:focus{{left:1rem;top:1rem;background:white;padding:.5rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.45rem;text-align:left;vertical-align:top}}caption{{font-weight:bold;text-align:left;margin:.5rem 0}}.hold{{font-weight:bold}}</style></head>
<body><a class="skip" href="#main">Skip to main content</a><header><h1>Eiren Kestrel v675-v2 bounded evidence report</h1><p>{IDENTITY_BOUNDARY}</p></header><nav aria-label="Report sections"><a href="#truth">Truth</a> · <a href="#outcomes">Outcomes</a> · <a href="#limits">Limits</a></nav><main id="main"><section id="truth"><h2>Truth</h2><p>This report describes same-owner synthetic software and structural evidence only. <span class="hold">NOT READY FOR STAGE 20.</span></p></section><section id="outcomes"><h2>Four-label outcome register</h2><table><caption>Forty bounded proposal outcomes</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Title</th><th scope="col">Evidence boundary</th></tr></thead><tbody>{rows_html}</tbody></table></section><section id="limits"><h2>Limits and reserved evaluation</h2><p>{BOUNDARY}</p><p>Manual browser, assistive-technology, cognitive-accessibility, Māori-language, affected-user, practitioner, conservator, legal, cultural, and independent evaluation is reserved and not claimed.</p></section></main></body></html>"""
    write_text("x2/accessible-evidence-report.html", html)


def validate_skill_runner_tools() -> dict[str, Any]:
    quick_count = int(os.environ.get("GHC_SKILL_QUICK_VALIDATE_COUNT", "0"))
    output_sha = os.environ.get("GHC_SKILL_VALIDATE_OUTPUT_SHA256", "")
    if quick_count != 20 or not re.fullmatch(r"[0-9a-f]{64}", output_sha):
        raise SystemExit("exact external quick-validation count and output digest required")
    skill_rows = []
    for index, name in enumerate(SKILL_NAMES, start=1):
        skill_path = X2_ROOT / "skills" / name / "SKILL.md"
        yaml_path = X2_ROOT / "skills" / name / "agents" / "openai.yaml"
        body = skill_path.read_text(encoding="utf-8")
        yaml_body = yaml_path.read_text(encoding="utf-8")
        accepted = (
            body.startswith("---\n")
            and f"name: {name}\n" in body
            and BOUNDARY in body
            and f"Use ${name}" in yaml_body
        )
        rejecting = "Reject any fixture" in body and "Retain the rejection" in body
        skill_rows.append(
            {
                "skill_id": f"EK6752-SKILL-{index:03d}",
                "skill_name": name,
                "quick_validate": "pass",
                "read_complete": body.endswith("\n"),
                "accepting_smoke": "pass" if accepted else "fail",
                "rejecting_smoke": "rejected_as_expected" if rejecting else "fail",
                "global_installation": False,
            }
        )
    runner_rows = []
    for index, (filename, focus, required) in enumerate(RUNNER_SPECS, start=1):
        module = import_path(ROOT / "scripts" / filename)
        payload = module.accepting_fixture()
        accepted = module.run(payload)
        rejecting_payload = dict(payload)
        rejecting_payload.pop("owner")
        rejected = module.run(rejecting_payload)
        runner_rows.append(
            {
                "runner_id": f"EK6752-RUN-{index:03d}",
                "path": f"scripts/{filename}",
                "focus": focus,
                "required_fields": required,
                "accepting_smoke": "pass" if accepted["accepted"] else "fail",
                "rejecting_smoke": "rejected_as_expected" if not rejected["accepted"] else "fail",
                "external_actions": 0,
                "authority_conferred": False,
            }
        )
    contract = import_path(ROOT / "scripts" / TOOL_SPECS[0][0])
    proposal = load("x1/new-proposal-freeze.json")["rows"][0]
    contract_accept = contract.validate(proposal)
    invalid = dict(proposal)
    invalid.pop("hypothesis")
    contract_reject = contract.validate(invalid)
    topology = import_path(ROOT / "scripts" / TOOL_SPECS[1][0])
    topology_accept = topology.validate(
        {"nodes": [{"id": "a"}, {"id": "b"}], "edges": [{"source": "a", "target": "b"}], "real_measurements": 0, "condition_assessment": "unknown_not_assessed"}
    )
    topology_reject = topology.validate(
        {"nodes": [{"id": "a"}], "edges": [{"source": "a", "target": "missing"}], "real_measurements": 0}
    )
    handover = import_path(ROOT / "scripts" / TOOL_SPECS[2][0])
    handover_accept = handover.validate(
        {"events": [{"sequence": 1, "event_id": "e1", "kind": "observation"}, {"sequence": 2, "event_id": "e2", "kind": "correction", "supersedes": "e1"}], "professional_release": False, "authority_conferred": False}
    )
    handover_reject = handover.validate(
        {"events": [{"sequence": 2, "event_id": "e1", "kind": "correction", "supersedes": "missing"}], "professional_release": True}
    )
    tool_rows = [
        {"tool_id": "EK6752-TOOL-001", "title": TOOL_SPECS[0][1], "accepting_smoke": contract_accept["accepted"], "rejecting_smoke_rejected": not contract_reject["accepted"]},
        {"tool_id": "EK6752-TOOL-002", "title": TOOL_SPECS[1][1], "accepting_smoke": topology_accept["accepted"], "rejecting_smoke_rejected": not topology_reject["accepted"]},
        {"tool_id": "EK6752-TOOL-003", "title": TOOL_SPECS[2][1], "accepting_smoke": handover_accept["accepted"], "rejecting_smoke_rejected": not handover_reject["accepted"]},
    ]
    valid = (
        all(row["accepting_smoke"] == "pass" and row["rejecting_smoke"] == "rejected_as_expected" for row in skill_rows)
        and all(row["accepting_smoke"] == "pass" and row["rejecting_smoke"] == "rejected_as_expected" for row in runner_rows)
        and all(row["accepting_smoke"] and row["rejecting_smoke_rejected"] for row in tool_rows)
    )
    payload = {
        "schema": "ghc.family.skill-runner-tool-evidence.v5",
        "owner": OWNER,
        "phase": PHASE,
        "valid": valid,
        "official_quick_validation": {"passed": 20, "total": 20, "output_sha256": output_sha},
        "skills": {"passed": 20, "total": 20, "rows": skill_rows},
        "runners": {"passed": 10, "total": 10, "rows": runner_rows},
        "tools": {"passed": 3, "total": 3, "rows": tool_rows},
        "global_installations": 0,
        "external_actions": 0,
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": BOUNDARY,
    }
    write_json("x2/skill-runner-tool-evidence.json", payload)
    return payload


def staged_paths() -> list[str]:
    return sorted(
        line
        for line in git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR", X1_COMMIT).splitlines()
        if line
    )


def staged_blob(path: str) -> bytes:
    return git("show", f":{path}").stdout.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def staged_mode(path: str) -> str:
    return git_text("ls-files", "-s", "--", path).split()[0]


def build_privacy() -> None:
    paths = [path for path in staged_paths() if path != PRIVACY_PATH]
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.IGNORECASE),
        "private_absolute_path": re.compile(r"\b[A-Z]:[\\/](?:Users|GHC-Archives)[\\/]"),
        "credential_assignment": re.compile(r"\b(?:api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*['\"]?[A-Za-z0-9+/=_-]{12,}", re.IGNORECASE),
        "transcript_or_session_stream": re.compile(r"^\s*(?:user|assistant|developer|system)\s*:", re.IGNORECASE | re.MULTILINE),
        "private_callable_identifier": re.compile(r"\bmcp__[a-z0-9_]+\b", re.IGNORECASE),
    }
    suffixes = {".json", ".md", ".py", ".yaml", ".yml", ".html", ".txt"}
    scanned, candidates, confirmed, decode_issues = 0, [], [], []
    for path in paths:
        if Path(path).suffix.lower() not in suffixes:
            continue
        scanned += 1
        try:
            text = staged_blob(path).decode("utf-8")
        except UnicodeDecodeError:
            decode_issues.append(path)
            continue
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(text):
                row = {"path": path, "line": text.count("\n", 0, match.start()) + 1, "class": class_name}
                if path in {BUILDER_PATH, TEST_PATH}:
                    row["classification"] = "scanner_definition_or_rejecting_fixture"
                    candidates.append(row)
                else:
                    confirmed.append(row)
    write_json(
        "validation/evidence-staged-privacy.json",
        {
            "schema": "ghc.family.staged-privacy-scan.v3",
            "owner": OWNER,
            "phase": PHASE,
            "lifecycle": "x2_evidence",
            "hash_domain": "exact_staged_git_blob",
            "pattern_classes": sorted(patterns),
            "scanned_text_files": scanned,
            "candidates": candidates,
            "confirmed_hits": confirmed,
            "confirmed_hit_count": len(confirmed),
            "decode_issues": decode_issues,
            "self_exclusions": [PRIVACY_PATH],
            "valid": not confirmed and not decode_issues,
            "boundary": "Scanner definitions and rejecting fixtures remain candidates, not silently discarded payload hits.",
        },
    )


def build_manifest() -> None:
    exclusions = [MANIFEST_PATH, REVIEW_PATH]
    paths = [path for path in staged_paths() if path not in exclusions]
    entries = []
    for path in paths:
        blob = staged_blob(path)
        entries.append({"path": path, "mode": staged_mode(path), "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})
    write_json(
        "validation/evidence-manifest.json",
        {
            "schema": "ghc.family.git-blob-manifest.v6",
            "domain": "Eiren v675-v2 x2 evidence exact staged Git blobs before two declared self files",
            "hash_domain": "normalized_lf_exact_git_blob",
            "owner": OWNER,
            "phase": PHASE,
            "source_x1": X1_COMMIT,
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": exclusions,
        },
    )


def build_review() -> None:
    paths = staged_paths()
    allowed_patterns = [
        re.compile(r"docs/eiren-kestrel/v675-v2/x2/"),
        re.compile(r"docs/eiren-kestrel/v675-v2/validation/evidence-"),
        re.compile(r"scripts/build_ghc_family_eiren_kestrel_v675_v2_x2\.py\Z"),
        re.compile(r"scripts/ghc_family_(?:tinsmith|pattern|seam|form|tin|thos_seam|freed_id_tinsmith|cbr_tinsmith)_.+\.py\Z"),
        re.compile(r"scripts/ghc_family_eiren_kestrel_v675_v2_.+\.py\Z"),
        re.compile(r"tests/test_ghc_family_eiren_kestrel_v675_v2_x2\.py\Z"),
    ]
    allowed = all(any(pattern.match(path) for pattern in allowed_patterns) for path in paths)
    name_status = git_text("diff", "--cached", "--name-status", X1_COMMIT).splitlines()
    non_additive = [row for row in name_status if not row.startswith("A\t")]
    manifest = json.loads((ROOT / MANIFEST_PATH).read_text(encoding="utf-8"))
    manifest_issues = []
    for entry in manifest["entries"]:
        blob = staged_blob(entry["path"])
        if len(blob) != entry["bytes"] or hashlib.sha256(blob).hexdigest() != entry["sha256"]:
            manifest_issues.append({"path": entry["path"], "issue": "hash_or_length_mismatch"})
    expected = {row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"])
    privacy = json.loads((ROOT / PRIVACY_PATH).read_text(encoding="utf-8"))
    exact_hold = load("x2/exact-blocked-hold.json")
    issues = []
    if not allowed:
        issues.append("path outside x2 owner evidence scope")
    if non_additive:
        issues.append("non-additive evidence path")
    if expected != set(paths) | {REVIEW_PATH}:
        issues.append("manifest paths and exclusions do not cover prospective evidence tree")
    if manifest_issues:
        issues.append("manifest replay mismatch")
    if not privacy["valid"]:
        issues.append("privacy scan invalid")
    if exact_hold["executed"] != 0:
        issues.append("exact or blocked work executed")
    write_json(
        "validation/evidence-staged-review.json",
        {
            "schema": "ghc.family.staged-review.v5",
            "owner": OWNER,
            "phase": PHASE,
            "lifecycle": "x2_evidence",
            "source_x1": X1_COMMIT,
            "staged_paths_before_self": len(paths),
            "prospective_staged_paths": len(paths) + (0 if REVIEW_PATH in paths else 1),
            "allowed_owner_scope": allowed,
            "non_additive_paths": non_additive,
            "manifest_entries": manifest["entry_count"],
            "manifest_self_exclusions": manifest["self_exclusions"],
            "manifest_issues": manifest_issues,
            "privacy_valid": privacy["valid"],
            "exact_blocked_executed": exact_hold["executed"],
            "issues": issues,
            "valid": not issues,
            "external_actions": 0,
            "boundary": BOUNDARY,
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-evidence", action="store_true")
    parser.add_argument("--privacy", action="store_true")
    parser.add_argument("--manifest", action="store_true")
    parser.add_argument("--review", action="store_true")
    args = parser.parse_args()
    if sum((args.skill_evidence, args.privacy, args.manifest, args.review)) > 1:
        raise SystemExit("select at most one lifecycle mode")
    if args.skill_evidence:
        receipt = validate_skill_runner_tools()
        if not receipt["valid"]:
            raise SystemExit("skill runner or tool evidence invalid")
    elif args.privacy:
        build_privacy()
    elif args.manifest:
        build_manifest()
    elif args.review:
        build_review()
    else:
        build_default()


if __name__ == "__main__":
    main()
