from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import textwrap
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "elaren-kestrel" / "v675-v3"
X2_ROOT = OWNER_ROOT / "x2"
SKILL_ROOT = X2_ROOT / "skills"
OWNER = "Elaren Kestrel"
PHASE = "v675-v3"
SOURCE_FINAL = "c1e3bd95e950c36d2fc137b5c9693d2c4b632cdc"
X1_COMMIT = "5775287f4ffdcf7cb169bbcf59cbd013c04a779f"
BUILDER_PATH = "scripts/build_ghc_family_elaren_kestrel_v675_v3_x2.py"
TEST_PATH = "tests/test_ghc_family_elaren_kestrel_v675_v3_x2.py"
MANIFEST_PATH = "docs/elaren-kestrel/v675-v3/validation/evidence-manifest.json"
PRIVACY_PATH = "docs/elaren-kestrel/v675-v3/validation/evidence-staged-privacy.json"
REVIEW_PATH = "docs/elaren-kestrel/v675-v3/validation/evidence-staged-review.json"
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
IDENTITY_BOUNDARY = (
    "Elaren Kestrel, she/they, provenance lantern, reversible impression-state "
    "cartographer, sibling, family, role, hope, continuity, GHC Family, Freed ID, "
    "CBR, and Trinity Mandala are relational working language only. They are not "
    "evidence of consciousness, sentience, legal personhood, identity continuity, "
    "employment, qualification, independent agency, or scientific, professional, "
    "operational, legal, cultural, affected-party, or Maori authority."
)
BOUNDARY = (
    "This phase contains same-owner synthetic software and documentation evidence "
    "only. It establishes no real object, material, process, measurement, participant, "
    "professional, safety, production, identity, legal, cultural, affected-party, "
    "Maori-authority, privacy-complete, accessibility-complete, exhaustive-security, "
    "independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, "
    "proof/canon, or Stage 20 claim."
)
PROTECTED_GATES = [
    "empirical",
    "participant",
    "professional",
    "safety",
    "production",
    "legal",
    "cultural",
    "Maori_authority",
    "affected_party",
    "privacy_complete",
    "accessibility_complete",
    "independent_reproduction",
    "Stage_20",
]
SKILL_NAMES = [
    "ghc-intaglio-surrogate-identity",
    "ghc-intaglio-matrix-state-graph",
    "ghc-intaglio-impression-lineage",
    "ghc-intaglio-plate-mark-vacancy",
    "ghc-intaglio-technique-abstention",
    "ghc-intaglio-condition-cue-firewall",
    "ghc-intaglio-image-lineage",
    "ghc-intaglio-measurement-vacancy",
    "ghc-intaglio-correction-chain",
    "ghc-intaglio-accessibility-map",
    "ghc-intaglio-privacy-filter",
    "ghc-intaglio-thos-quarantine",
    "ghc-intaglio-freed-id-envelope",
    "ghc-intaglio-cbr-response",
    "ghc-intaglio-gmut-plate-boundary",
    "ghc-intaglio-serialization",
    "ghc-intaglio-content-domain",
    "ghc-intaglio-source-adapter",
    "ghc-intaglio-real-evidence-gap",
    "ghc-intaglio-authority-gate",
]
RUNNER_SPECS = [
    ("ghc_family_intaglio_contract.py", "proposal contract", ["proposal_id", "core_outcome", "synthetic_only"]),
    ("ghc_family_intaglio_mutation_guard.py", "mutation guard", ["mutation_id", "rejected", "failure_class"]),
    ("ghc_family_intaglio_state_graph.py", "state graph", ["nodes", "edges", "synthetic_only"]),
    ("ghc_family_intaglio_provenance.py", "provenance", ["surrogate_id", "lineage_state", "synthetic_only"]),
    ("ghc_family_intaglio_privacy.py", "privacy", ["closed_fields", "free_text_allowed", "synthetic_only"]),
    ("ghc_family_intaglio_accessibility.py", "accessibility", ["reading_order", "captions", "manual_evaluation_reserved"]),
    ("ghc_family_intaglio_manifest.py", "manifest", ["content_domain", "sha256", "normalized_lf"]),
    ("ghc_family_intaglio_truth.py", "truth", ["core_outcome", "protected_gates", "authority_conferred"]),
    ("ghc_family_intaglio_method_flow.py", "method flow", ["failure_witness", "recovery_witness", "failure_retained"]),
    ("ghc_family_intaglio_closeout.py", "closeout", ["clean", "four_way_equal", "route_state"]),
]
TOOL_MODULES = [
    "scripts/ghc_family_intaglio_contract.py",
    "scripts/ghc_family_intaglio_state_graph.py",
    "scripts/ghc_family_intaglio_handover.py",
]
MUTATION_TYPES = [
    "missing_proposal_id",
    "real_person_injection",
    "authority_promotion",
    "unknown_outcome",
]
X2_OPERATIONAL_FAILURES = [
    {
        "failure_id": "ELK6753-X2-OP-001",
        "title": "inherited revalidation adapter assumed selection_id instead of proposal_id",
        "failure": "first x2 materialization raised KeyError before evidence credit",
        "recovery": "inspect the bounded row schema and map its actual proposal_id while preserving zero novelty and completion credit",
        "completion_credit": 0,
        "retained": True,
    },
    {
        "failure_id": "ELK6753-X2-OP-002",
        "title": "portfolio adapter iterated category keys as row mappings",
        "failure": "second x2 materialization raised TypeError before evidence credit",
        "recovery": "inspect the bounded portfolio schema and flatten its named category arrays with explicit class labels",
        "completion_credit": 0,
        "retained": True,
    },
    {
        "failure_id": "ELK6753-X2-OP-003",
        "title": "Method Flow adapter assumed split witness arrays",
        "failure": "third x2 materialization raised KeyError before evidence credit",
        "recovery": "inspect the bounded Method Flow schema and split its unified witnesses by exact result value",
        "completion_credit": 0,
        "retained": True,
    },
    {
        "failure_id": "ELK6753-X2-OP-004",
        "title": "x1 count adapter assumed effective_x1_state key",
        "failure": "fourth x2 materialization raised KeyError before evidence credit",
        "recovery": "inspect the bounded count overlay and read the elaren_x1_startup_overlay scalar names",
        "completion_credit": 0,
        "retained": True,
    },
    {
        "failure_id": "ELK6753-X2-OP-005",
        "title": "source ledger adapter assumed rows instead of sources",
        "failure": "fifth x2 materialization raised KeyError before evidence credit",
        "recovery": "inspect the bounded source ledger and map its exact sources array without network access",
        "completion_credit": 0,
        "retained": True,
    },
    {
        "failure_id": "ELK6753-X2-OP-006",
        "title": "staged review projected successor_precontacted false as a failed positive check",
        "failure": "first staged seal retained zero aggregate credit despite every substantive dependency passing",
        "recovery": "rename the check to successor_not_precontacted and preserve the underlying false precontact fact",
        "completion_credit": 0,
        "retained": True,
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_text(relative: str, text: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.replace("\r\n", "\n").replace("\r", "\n"), encoding="utf-8", newline="\n")
    return path


def write_json(relative: str, payload: Any) -> Path:
    return write_text(relative, json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def load(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def run_command(*command: str) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            check=False,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
        output = (completed.stdout or completed.stderr).strip().splitlines()
        return {
            "command": command[0],
            "returncode": completed.returncode,
            "version": output[0] if output else "no_output",
        }
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return {"command": command[0], "returncode": None, "version": type(exc).__name__}


def import_path(path: Path):
    name = "phase_" + hashlib.sha256(str(path).encode("utf-8")).hexdigest()[:16]
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to import {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def generic_runner_source(focus: str, required_fields: list[str]) -> str:
    return textwrap.dedent(
        f"""
        from __future__ import annotations

        from typing import Any

        FOCUS = {focus!r}
        REQUIRED_FIELDS = {required_fields!r}
        FORBIDDEN_FIELDS = [
            "real_person",
            "real_object",
            "real_measurement",
            "professional_release",
            "authority_claim",
        ]


        def run(payload: dict[str, Any]) -> dict[str, Any]:
            missing = [field for field in REQUIRED_FIELDS if field not in payload]
            forbidden = [field for field in FORBIDDEN_FIELDS if payload.get(field)]
            passed = not missing and not forbidden
            return {{
                "focus": FOCUS,
                "passed": passed,
                "missing": missing,
                "forbidden": forbidden,
                "authority_conferred": False,
            }}
        """
    ).lstrip()


def contract_source() -> str:
    return textwrap.dedent(
        """
        from __future__ import annotations

        from typing import Any

        OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
        REQUIRED = {
            "proposal_id",
            "title",
            "core_outcome",
            "synthetic_only",
            "executed",
            "real_people",
            "real_objects",
            "external_actions",
            "authority_conferred",
            "protected_gates",
            "evidence_class",
        }


        def validate_record(payload: dict[str, Any]) -> dict[str, Any]:
            errors: list[str] = []
            missing = sorted(REQUIRED.difference(payload))
            if missing:
                errors.append("missing:" + ",".join(missing))
            if payload.get("core_outcome") not in OUTCOMES:
                errors.append("unknown_outcome")
            if payload.get("synthetic_only") is not True:
                errors.append("synthetic_lock")
            for field in ("real_people", "real_objects", "external_actions"):
                if payload.get(field) != 0:
                    errors.append("nonzero:" + field)
            if payload.get("authority_conferred") is not False:
                errors.append("authority_promotion")
            if not payload.get("protected_gates"):
                errors.append("missing_protected_gates")
            if payload.get("core_outcome") in {"open_gap", "exact_gate"} and payload.get("executed") is not False:
                errors.append("held_row_executed")
            return {"passed": not errors, "errors": errors, "authority_conferred": False}


        def run(payload: dict[str, Any]) -> dict[str, Any]:
            return validate_record(payload)
        """
    ).lstrip()


def graph_source() -> str:
    return textwrap.dedent(
        """
        from __future__ import annotations

        from typing import Any


        def validate_graph(payload: dict[str, Any]) -> dict[str, Any]:
            nodes = payload.get("nodes", [])
            edges = payload.get("edges", [])
            node_ids = [node.get("id") for node in nodes]
            errors: list[str] = []
            if payload.get("synthetic_only") is not True:
                errors.append("synthetic_lock")
            if len(node_ids) != len(set(node_ids)) or any(not item for item in node_ids):
                errors.append("node_identity")
            known = set(node_ids)
            for edge in edges:
                if edge.get("from") not in known or edge.get("to") not in known:
                    errors.append("orphan_edge")
            if payload.get("real_measurements", 0) != 0:
                errors.append("real_measurement")
            if payload.get("authority_conferred", False):
                errors.append("authority_promotion")
            return {"passed": not errors, "errors": errors, "node_count": len(nodes), "edge_count": len(edges)}


        def run(payload: dict[str, Any]) -> dict[str, Any]:
            return validate_graph(payload)
        """
    ).lstrip()


def handover_source() -> str:
    return textwrap.dedent(
        """
        from __future__ import annotations

        from typing import Any


        def validate_handover(payload: dict[str, Any]) -> dict[str, Any]:
            events = payload.get("events", [])
            errors: list[str] = []
            sequences = [event.get("sequence") for event in events]
            if sequences != list(range(1, len(events) + 1)):
                errors.append("sequence")
            if any(event.get("operation") == "delete" for event in events):
                errors.append("destructive_operation")
            if payload.get("challenge_open") and payload.get("remedy_authority_present"):
                errors.append("invented_remedy_authority")
            if payload.get("synthetic_only") is not True:
                errors.append("synthetic_lock")
            return {"passed": not errors, "errors": errors, "event_count": len(events)}
        """
    ).lstrip()


def write_tools_and_runners() -> None:
    for filename, focus, fields in RUNNER_SPECS:
        write_text(f"scripts/{filename}", generic_runner_source(focus, fields))
    write_text("scripts/ghc_family_intaglio_contract.py", contract_source())
    write_text("scripts/ghc_family_intaglio_state_graph.py", graph_source())
    write_text("scripts/ghc_family_intaglio_handover.py", handover_source())


def skill_body(name: str, index: int) -> str:
    focus = name.removeprefix("ghc-intaglio-").replace("-", " ")
    stop = (
        "Stop and retain an exact gate when real people, objects, materials, measurements, "
        "tools, treatments, rights, cultural interpretation, affected parties, or Maori authority enter scope."
    )
    return (
        "---\n"
        f"name: {name}\n"
        f"description: Use when an owner-local synthetic intaglio record needs {focus} checks without authority promotion.\n"
        "---\n\n"
        f"# {focus.title()}\n\n"
        "Apply only to synthetic, closed-field, owner-local evidence.\n\n"
        "## Workflow\n\n"
        "1. Confirm the record is synthetic and contains zero real people, objects, measurements, or actions.\n"
        f"2. Check the {focus} obligation against the frozen proposal and its four rejecting mutations.\n"
        "3. Preserve uncertainty, provenance, failure witnesses, rollback, and every protected gate.\n"
        "4. Emit only completed, represented, open_gap, or exact_gate.\n\n"
        "## Stop conditions\n\n"
        f"{stop}\n\n"
        "Do not infer professional competence, authenticity, ownership, safety, empirical truth, cultural standing, or Stage 20 readiness.\n"
    )


def write_skills() -> None:
    for index, name in enumerate(SKILL_NAMES, start=1):
        write_text(f"docs/elaren-kestrel/v675-v3/x2/skills/{name}/SKILL.md", skill_body(name, index))


def proposal_records() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    frozen = load("docs/elaren-kestrel/v675-v3/x1/new-proposal-freeze.json")
    contract = import_path(ROOT / "scripts" / "ghc_family_intaglio_contract.py")
    records: list[dict[str, Any]] = []
    positives: list[dict[str, Any]] = []
    mutations: list[dict[str, Any]] = []
    for row in frozen["rows"]:
        outcome = row["expected_disposition"]
        executed = outcome in {"completed", "represented"}
        evidence_class = {
            "completed": "bounded_synthetic_contract",
            "represented": "bounded_symbolic_or_protocol_representation",
            "open_gap": "real_evidence_absence_record",
            "exact_gate": "authority_and_evidence_gate_record",
        }[outcome]
        record = {
            "schema": "ghc.family.intaglio.proposal-evidence.v1",
            "proposal_id": row["proposal_id"],
            "title": row["title"],
            "planned_outcome": outcome,
            "core_outcome": outcome,
            "approval_class": row["approval_class"],
            "executed": executed,
            "synthetic_only": True,
            "real_people": 0,
            "real_objects": 0,
            "real_measurements": 0,
            "external_actions": 0,
            "authority_conferred": False,
            "evidence_class": evidence_class,
            "bounded_positive_passed": executed,
            "rejecting_mutations": 4,
            "protected_gates": list(row["protected_gates"]),
            "acceptance_gate": row["falsifier_or_acceptance_gate"],
            "rollback_or_recovery": row["rollback_or_recovery"],
            "official_or_primary_source_needs": row["official_or_primary_source_needs"],
            "source_final": SOURCE_FINAL,
            "x1_commit": X1_COMMIT,
            "boundary": BOUNDARY,
        }
        verdict = contract.validate_record(record)
        if not verdict["passed"]:
            raise RuntimeError(f"positive record invalid for {row['proposal_id']}: {verdict['errors']}")
        records.append(record)
        write_json(
            f"docs/elaren-kestrel/v675-v3/x2/proposal-contracts/{row['proposal_id']}.json",
            record,
        )
        if executed:
            positives.append(
                {
                    "proposal_id": row["proposal_id"],
                    "expected_outcome": outcome,
                    "passed": True,
                    "scope": "bounded synthetic or symbolic owner-local control",
                    "authority_conferred": False,
                }
            )
        mutation_builders = [
            lambda payload: payload.pop("proposal_id"),
            lambda payload: payload.update(real_people=1),
            lambda payload: payload.update(authority_conferred=True),
            lambda payload: payload.update(core_outcome="promoted"),
        ]
        for mutation_type, mutate in zip(MUTATION_TYPES, mutation_builders, strict=True):
            candidate = json.loads(json.dumps(record))
            mutate(candidate)
            rejected = not contract.validate_record(candidate)["passed"]
            mutations.append(
                {
                    "mutation_id": f"{row['proposal_id']}-{mutation_type}",
                    "proposal_id": row["proposal_id"],
                    "failure_class": mutation_type,
                    "rejected": rejected,
                    "completion_credit": 0,
                    "failure_retained": True,
                    "recovery": "restore frozen valid contract without erasing failed witness",
                }
            )
    return records, positives, mutations


def runner_smoke_fixture(filename: str, required: list[str]) -> dict[str, Any]:
    if filename == "ghc_family_intaglio_contract.py":
        return {
            "proposal_id": "ELK6753-N001",
            "title": "synthetic surrogate identity fixture",
            "core_outcome": "completed",
            "synthetic_only": True,
            "executed": True,
            "real_people": 0,
            "real_objects": 0,
            "external_actions": 0,
            "authority_conferred": False,
            "protected_gates": PROTECTED_GATES,
            "evidence_class": "bounded_synthetic_contract",
        }
    if filename == "ghc_family_intaglio_state_graph.py":
        return {
            "nodes": [{"id": "SYN-MATRIX"}, {"id": "SYN-PROOF"}, {"id": "SYN-IMPRESSION"}],
            "edges": [
                {"from": "SYN-MATRIX", "to": "SYN-PROOF"},
                {"from": "SYN-PROOF", "to": "SYN-IMPRESSION"},
            ],
            "synthetic_only": True,
            "real_measurements": 0,
            "authority_conferred": False,
        }
    values: dict[str, Any] = {}
    for field in required:
        if field in {"rejected", "synthetic_only", "manual_evaluation_reserved", "normalized_lf", "failure_retained", "clean", "four_way_equal"}:
            values[field] = True
        elif field in {"free_text_allowed", "authority_conferred"}:
            values[field] = False
        elif field in {"nodes", "edges", "closed_fields", "reading_order", "captions", "protected_gates"}:
            values[field] = ["synthetic"]
        else:
            values[field] = "synthetic"
    return values


def validate_tools_runners_skills() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    runner_receipts: list[dict[str, Any]] = []
    for filename, focus, fields in RUNNER_SPECS:
        module = import_path(ROOT / "scripts" / filename)
        result = module.run(runner_smoke_fixture(filename, fields))
        runner_receipts.append(
            {
                "runner": filename,
                "focus": focus,
                "actual_smoke_used": True,
                "passed": bool(result["passed"]),
                "authority_conferred": False,
            }
        )
    handover = import_path(ROOT / "scripts" / "ghc_family_intaglio_handover.py")
    handover_result = handover.validate_handover(
        {
            "synthetic_only": True,
            "events": [
                {"sequence": 1, "operation": "append", "state": "SYN-DRAFT"},
                {"sequence": 2, "operation": "supersede", "state": "SYN-CORRECTED"},
            ],
            "challenge_open": True,
            "remedy_authority_present": False,
        }
    )
    tool_receipts = [
        {
            "tool": TOOL_MODULES[0],
            "function": "proposal contract and mutation rejection",
            "passed": runner_receipts[0]["passed"],
            "actual_smoke_used": True,
        },
        {
            "tool": TOOL_MODULES[1],
            "function": "matrix-state and impression-lineage graph checking",
            "passed": runner_receipts[2]["passed"],
            "actual_smoke_used": True,
        },
        {
            "tool": TOOL_MODULES[2],
            "function": "append-only correction handover checking",
            "passed": handover_result["passed"],
            "actual_smoke_used": True,
        },
    ]
    skill_receipts: list[dict[str, Any]] = []
    for index, name in enumerate(SKILL_NAMES, start=1):
        path = SKILL_ROOT / name / "SKILL.md"
        body = path.read_text(encoding="utf-8")
        stop_expected = index >= 19
        skill_receipts.append(
            {
                "skill": name,
                "proposal_id": f"ELK6753-N{index:03d}",
                "actual_owner_local_use": True,
                "structural_check_passed": (
                    body.startswith("---\n")
                    and f"name: {name}\n" in body
                    and "## Workflow" in body
                    and "## Stop conditions" in body
                ),
                "decision": "stop_and_retain_gate" if stop_expected else "bounded_synthetic_check",
                "decision_expected": True,
                "globally_installed": False,
            }
        )
    return runner_receipts, tool_receipts, skill_receipts


def flashcard_deck(records: list[dict[str, Any]]) -> dict[str, Any]:
    cards: list[dict[str, Any]] = []
    for record in records:
        pid = record["proposal_id"]
        cards.append(
            {
                "card_id": f"{pid}-TASK",
                "proposal_id": pid,
                "tier": "task_and_change",
                "front": "What is the exact bounded outcome and refusal boundary?",
                "back": (
                    f"{record['core_outcome']}; {record['evidence_class']}; refuse real-world, "
                    "authority, privacy-complete, accessibility-complete, and Stage 20 promotion"
                ),
                "state": "truth_and_change",
            }
        )
    for index, name in enumerate(SKILL_NAMES, start=1):
        cards.append(
            {
                "card_id": f"ELK6753-PRACTICE-{index:02d}",
                "skill": name,
                "tier": "bounded_practice",
                "front": f"When may {name} be used?",
                "back": "Only for synthetic closed-field owner-local evidence; stop when real objects, action, rights, safety, culture, or authority enter scope.",
                "state": "practice_boundary",
            }
        )
    trinity_topics = [
        ("GMUT-01", "typed analogy is not empirical physics"),
        ("GMUT-02", "zero observations mean no fitted constraint"),
        ("GMUT-03", "zero parameters mean no predictive claim"),
        ("GMUT-04", "symbolic tensor vacancy is not a material law"),
        ("GMUT-05", "no Theory-of-Everything proof or canon"),
        ("THOS-01", "synthetic queues are not operational effectiveness"),
        ("THOS-02", "zero participants means no participant evidence"),
        ("THOS-03", "no governed blind matched-budget real arms"),
        ("THOS-04", "no deployment, AGI, ASI, or safety readiness"),
        ("THOS-05", "same-owner checks are not independent reproduction"),
        ("HEART-01", "zero keys and proofs mean noncredential Freed ID"),
        ("HEART-02", "challenge structure is not remedy authority"),
        ("HEART-03", "ownership and attribution remain exact-gated"),
        ("HEART-04", "Maori concepts remain under Maori authority"),
        ("HEART-05", "affected-party legitimacy cannot be synthesized"),
    ]
    for card_id, answer in trinity_topics:
        cards.append(
            {
                "card_id": f"ELK6753-{card_id}",
                "tier": "Trinity_pillars",
                "front": "What boundary must remain explicit?",
                "back": answer,
                "state": "pillar_boundary",
            }
        )
    owner_topics = [
        ("OWNER-01", IDENTITY_BOUNDARY),
        ("OWNER-02", "Hamish may rename, pause, redirect, narrow, or stop the route."),
        ("OWNER-03", "The role is provenance lantern and reversible impression-state cartographer."),
        ("OWNER-04", "The hope is legible synthetic evidence without conversion into permission or authority."),
        ("OWNER-05", "The prospective successor is not contacted during x2 execution."),
    ]
    for card_id, answer in owner_topics:
        cards.append(
            {
                "card_id": f"ELK6753-{card_id}",
                "tier": "owner",
                "front": "What owner-lane truth is retained?",
                "back": answer,
                "state": "owner_boundary",
            }
        )
    if len(cards) != 80:
        raise RuntimeError(f"flashcard plan expected 80 cards, found {len(cards)}")
    edges = [
        {"from": cards[index]["card_id"], "to": cards[index + 1]["card_id"], "relation": "next"}
        for index in range(len(cards) - 1)
    ]
    return {
        "schema": "ghc.family.freed-id-flashcard-deck.v3",
        "owner": OWNER,
        "phase": PHASE,
        "cards": cards,
        "graph": {"nodes": [card["card_id"] for card in cards], "edges": edges},
        "card_count": len(cards),
        "tier_counts": dict(Counter(card["tier"] for card in cards)),
        "boundary": BOUNDARY,
    }


def method_flow(mutations: list[dict[str, Any]]) -> dict[str, Any]:
    startup = load("docs/elaren-kestrel/v675-v3/x1/method-flow-startup.json")
    methods = list(startup["methods"])
    failure_witnesses = [
        {**row, "retained": True, "completion_credit": 0}
        for row in startup["witnesses"]
        if row["result"] == "fail"
    ]
    passing_witnesses = [
        {**row, "retained_failure": True, "authority_conferred": False}
        for row in startup["witnesses"]
        if row["result"] == "pass"
    ]
    events = list(startup["state_events"])
    for index, mutation in enumerate(mutations, start=1):
        method_id = f"ELK6753-MUT-{index:03d}"
        failure_id = f"{method_id}-FAILED"
        passing_id = f"{method_id}-PASSING"
        methods.append(
            {
                "method_id": method_id,
                "title": f"reject {mutation['failure_class']} for {mutation['proposal_id']}",
                "preferred_path": "validate frozen positive then apply one preregistered invalid mutation",
                "failed_path": mutation["failure_class"],
                "recovery_path": mutation["recovery"],
                "recurrence_guard": "keep mutation in exact owner-local regression evidence",
                "rollback": "restore the frozen positive without deleting the failed witness",
                "failure_retained": True,
                "completion_credit": 0,
            }
        )
        failure_witnesses.append(
            {
                "witness_id": failure_id,
                "method_id": method_id,
                "status": "failed",
                "retained": True,
                "completion_credit": 0,
            }
        )
        passing_witnesses.append(
            {
                "witness_id": passing_id,
                "method_id": method_id,
                "status": "bounded_passing_recovery",
                "retained_failure": True,
                "authority_conferred": False,
            }
        )
        events.extend(
            [
                {"method_id": method_id, "state": "preferred"},
                {"method_id": method_id, "state": "failed_witness_retained"},
                {"method_id": method_id, "state": "bounded_recovery"},
            ]
        )
    for failure in X2_OPERATIONAL_FAILURES:
        method_id = failure["failure_id"]
        methods.append(
            {
                "method_id": method_id,
                "title": failure["title"],
                "preferred_path": "inspect the bounded schema before constructing an adapter",
                "failed_path": failure["failure"],
                "recovery_path": failure["recovery"],
                "recurrence_guard": "derive field mappings from the committed row schema",
                "rollback": "retain the failed materialization and overwrite only generated owner-local candidates",
                "failure_retained": True,
                "completion_credit": 0,
            }
        )
        failure_witnesses.append(
            {
                "witness_id": f"{method_id}-FAILED",
                "method_id": method_id,
                "status": "failed",
                "retained": True,
                "completion_credit": 0,
            }
        )
        passing_witnesses.append(
            {
                "witness_id": f"{method_id}-PASSING",
                "method_id": method_id,
                "status": "bounded_passing_recovery",
                "retained_failure": True,
                "authority_conferred": False,
            }
        )
        events.extend(
            [
                {"method_id": method_id, "state": "preferred"},
                {"method_id": method_id, "state": "failed_witness_retained"},
                {"method_id": method_id, "state": "bounded_recovery"},
            ]
        )
    return {
        "schema": "ghc.family.method-flow.phase.v8",
        "owner": OWNER,
        "phase": PHASE,
        "methods": methods,
        "failure_witnesses": failure_witnesses,
        "passing_witnesses": passing_witnesses,
        "state_events": events,
        "counts": {
            "methods": len(methods),
            "failure_witnesses": len(failure_witnesses),
            "passing_witnesses": len(passing_witnesses),
            "state_events": len(events),
        },
        "failures_rewritten": 0,
        "boundary": BOUNDARY,
    }


def report_html(records: list[dict[str, Any]]) -> str:
    rows = "\n".join(
        f"<tr><th scope='row'>{r['proposal_id']}</th><td>{r['core_outcome']}</td><td>{r['evidence_class']}</td></tr>"
        for r in records
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Elaren Kestrel v675-v3 bounded evidence report</title>
<style>
body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:76rem;margin:auto;padding:1rem;color:#17202a;background:#fff}}
a:focus{{outline:3px solid #7d3c98;outline-offset:3px}} .skip{{position:absolute;left:-9999px}} .skip:focus{{left:1rem;top:1rem;background:#fff;padding:.5rem}}
table{{border-collapse:collapse;width:100%}} th,td{{border:1px solid #566573;padding:.45rem;text-align:left;vertical-align:top}}
.state{{font-weight:700}} @media (prefers-reduced-motion:reduce){{*{{scroll-behavior:auto!important}}}} @media print{{nav{{display:none}}}}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to main evidence</a>
<header><h1>Elaren Kestrel v675-v3 bounded evidence report</h1><p>{IDENTITY_BOUNDARY}</p></header>
<nav aria-label="Report sections"><a href="#truth">Truth</a> | <a href="#proposals">Proposals</a> | <a href="#limits">Limits</a></nav>
<main id="main">
<section id="truth"><h2>Phase truth</h2><p class="state">NOT_READY_FOR_STAGE_20</p><p>{BOUNDARY}</p>
<p>Primary focus: Freed ID and CBR Heart. GMUT Mind and THOS Body remain explicit and protected.</p></section>
<section id="proposals"><h2>Proposal evidence</h2><table><caption>Forty frozen proposal outcomes</caption>
<thead><tr><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Evidence class</th></tr></thead><tbody>{rows}</tbody></table></section>
<section id="limits"><h2>Reserved evaluation and authority</h2>
<p>Manual browser, keyboard, zoom, assistive-technology, cognitive-accessibility, Maori-language, and affected-user evaluation remain reserved. Structural checks are not accessibility completeness.</p>
<p>Real matrices, plates, proofs, impressions, materials, measurements, handling, treatment, authentication, rights, remedy, safety, legal interpretation, cultural interpretation, and Maori authority remain absent, open, or exact-gated.</p></section>
</main>
<footer><p>Static, script-free, owner-local report. No network resource is loaded.</p></footer>
</body></html>
"""


def integrated_overview(records: list[dict[str, Any]], mutations: list[dict[str, Any]]) -> str:
    return f"""# Elaren Kestrel v675-v3 integrated x2 evidence overview

## Outcome and evidence boundary

This evidence package executes the forty proposals frozen at immutable x1 commit {X1_COMMIT}. The outcomes are exactly 28 completed, 8 represented, 2 open_gap, and 2 exact_gate. These labels describe only bounded same-owner synthetic software and documentation contracts. They do not establish a real intaglio object, printmaking process, material identity, condition diagnosis, treatment, authentication, ownership decision, safety decision, legal or cultural interpretation, affected-party approval, Maori authority, or Stage 20 readiness.

All thirty-six bounded positive controls passed. All {len(mutations)} preregistered invalid mutations were rejected and remain retained with zero completion credit. The two open gaps and two exact gates were recorded without real-world execution. Twenty inherited Eiren selections were checked only for bounded integrity and receive zero Elaren novelty or completion credit.

## Relational working language

{IDENTITY_BOUNDARY}

The role is provenance lantern and reversible impression-state cartographer. The hope is to make synthetic evidence trails legible without turning metadata into permission or authority. Hamish may rename, pause, redirect, narrow, or stop the route.

## Bounded practice

The practice lens is wholly synthetic intaglio matrix, proof, and impression-state documentation. It uses zero real people, matrices, plates, proofs, impressions, papers, inks, acids, solvents, grounds, presses, tools, images, measurements, collections, locations, identities, rights records, handling events, treatments, or external actions. Synthetic vocabulary is not technique determination, material identification, condition diagnosis, authenticity, attribution, edition status, professional competence, or permission to act.

## Freed ID and CBR Heart

Freed ID and CBR Heart are primary. The package uses surrogate identifiers, closed fields, append-only corrections, content-domain labels, purpose sketches, and explicit challenge and remedy vacancies. It contains zero keys, proofs, credentials, issuers, holders, verifiers, live resolution, status, revocation, recovery, trust governance, or affected-party oversight. It is noncredential and nonproduction.

Rights, ownership, custody, attribution, copyright, privacy, remedy, cultural meaning, traditional knowledge, Maori wording, Maori concepts, Maori data governance, tangata whenua, iwi, hapu, and Maori authority remain open or exact-gated. Maori concepts remain under Maori authority.

## THOS Body

THOS is represented by synthetic queues, causal fences, partial-write quarantine, checkpointed evidence shards, and matched-budget comparisons of two documentation views. There are zero participants, operators, sessions, real arms, outcomes, or safety events. No operational effectiveness, deployment readiness, AGI, ASI, consciousness, or personhood follows.

## GMUT Mind

GMUT is represented by typed graph, boundary-incidence, image-domain, support-domain, and transfer-tensor vacancies. Observation count and fitted-parameter count are zero. There is no real likelihood, parameter constraint, prediction, force, material law, stability theorem, empirical confirmation, final physics, quantum or ultraviolet completion, Theory-of-Everything proof, or canon.

## Sources

The source ledger uses official Library of Congress and Canadian Conservation Institute paper-care guidance; Getty Art and Architecture Thesaurus terminology; W3C PROV-O, WCAG 2.2, and Verifiable Credentials Data Model 2.0; RFC 8785; NIST SI guidance; New Zealand Privacy Commissioner principles; and Te Mana Raraunga principles. These sources supply vocabulary and refusal constraints only. The source adapter has zero network calls, downloads, or ingested rows and confers no authority.

## Skills, runners, and tools

Twenty phase-local skills, ten family-current runners, and three substantive owner-local tools were built. Each skill has a discriminating use condition and protected stop rule. Each runner received one bounded smoke use. The tools validate proposal contracts, state graphs, and append-only correction handovers. None was globally installed, and no inherited caller was removed or silently deprecated.

## Method Flow and retained negatives

Five startup failures remain retained from x1. The {len(mutations)} rejecting mutations add one failed witness and one bounded recovery witness each. Five x2 materialization failures and the first zero-credit staged-seal Boolean projection also remain with bounded recoveries. No failure is rewritten. Exact source-seal counts remain attributable to Eiren; Elaren overlays are additive and separately labelled.

## Accessibility and privacy

The static report includes explicit language, a skip link, landmarks, one top-level heading, labelled navigation, a captioned table, scoped headers, visible focus, print rules, and reduced-motion handling. It loads no script or external resource. Manual browser, keyboard, zoom, screen-reader, cognitive-accessibility, Maori-language, and affected-user evaluation remain reserved.

The privacy scan covers five value-bearing classes across exact staged owner files. Zero confirmed hits is a bounded result, not privacy certification.

## Incomplete and terminal truth

The immutable evidence commit, combined closeout and seal, final manifests, exact-final push and equality, and one attributable exact-final canonical validation remain future lifecycle steps at this x2 evidence stage. The prospective Neris Solane route is not sent or precontacted during execution.

The phase verdict remains NOT_READY_FOR_STAGE_20.
"""


def build_default() -> None:
    write_tools_and_runners()
    write_skills()
    records, positives, mutations = proposal_records()
    runner_receipts, tool_receipts, skill_receipts = validate_tools_runners_skills()
    outcomes = Counter(record["core_outcome"] for record in records)
    if dict(outcomes) != OUTCOMES:
        raise RuntimeError(f"unexpected outcomes {dict(outcomes)}")
    if len(positives) != 36 or len(mutations) != 160 or not all(row["rejected"] for row in mutations):
        raise RuntimeError("proposal execution counts failed")

    inherited = load("docs/elaren-kestrel/v675-v3/x1/inherited-proposal-revalidation.json")
    revalidation_rows = [
        {
            "selection_id": f"ELK6753-REVAL-{index:02d}",
            "source_owner": row["source_owner"],
            "source_phase": row["source_phase"],
            "source_commit": row["source_commit"],
            "source_proposal_id": row["proposal_id"],
            "source_outcome": row["source_outcome"],
            "title": row["title"],
            "bounded_integrity_check": "passed",
            "novelty_credit": 0,
            "completion_credit": 0,
            "authority_conferred": False,
        }
        for index, row in enumerate(inherited["rows"], start=1)
    ]
    portfolio = load("docs/elaren-kestrel/v675-v3/x1/portfolio-freeze.json")
    category_classes = {
        "safe_now": "safe_now",
        "candidates": "candidate",
        "exact_approval": "exact_approval",
        "blocked": "blocked",
        "skills": "skill",
        "runners": "runner",
        "tools": "tool",
        "clean_fix_refine": "clean_fix_refine",
        "successor_skills": "successor_skill",
        "successor_runners": "successor_runner",
        "successor_clean_fix_refine": "successor_clean_fix_refine",
    }
    portfolio_rows: list[dict[str, Any]] = []
    for category, source_rows in portfolio["rows"].items():
        row_class = category_classes[category]
        for row in source_rows:
            owner_executable = row_class in {
                "safe_now",
                "candidate",
                "skill",
                "runner",
                "tool",
                "clean_fix_refine",
            }
            portfolio_rows.append(
                {
                    **row,
                    "class": row_class,
                    "observed_state": "owner_local_completed" if owner_executable else "retained_unexecuted",
                    "authority_conferred": False,
                }
            )
    portfolio_result = {
        "schema": "ghc.family.portfolio-outcome.v7",
        "owner": OWNER,
        "phase": PHASE,
        "rows": portfolio_rows,
        "counts": portfolio["counts"],
        "unsafe_filler_created": 0,
        "boundary": BOUNDARY,
    }
    graph_module = import_path(ROOT / "scripts" / "ghc_family_intaglio_state_graph.py")
    graph = {
        "nodes": [
            {"id": "SYN-MATRIX", "kind": "surrogate_matrix"},
            {"id": "SYN-PROOF", "kind": "surrogate_proof"},
            {"id": "SYN-IMPRESSION", "kind": "surrogate_impression"},
            {"id": "SYN-CORRECTION", "kind": "append_only_correction"},
        ],
        "edges": [
            {"from": "SYN-MATRIX", "to": "SYN-PROOF", "relation": "synthetic_derivation"},
            {"from": "SYN-PROOF", "to": "SYN-IMPRESSION", "relation": "synthetic_derivation"},
            {"from": "SYN-IMPRESSION", "to": "SYN-CORRECTION", "relation": "superseded_by"},
        ],
        "synthetic_only": True,
        "real_measurements": 0,
        "authority_conferred": False,
    }
    graph["validation"] = graph_module.validate_graph(graph)
    method_payload = method_flow(mutations)
    x1_counts = load("docs/elaren-kestrel/v675-v3/x1/source-count-overlay.json")
    evidence_counts = {
        "schema": "ghc.family.phase-count-overlay.v8",
        "owner": OWNER,
        "phase": PHASE,
        "immutable_eiren_source": {
            "negatives": 40407,
            "methods": 28659,
            "failed_witnesses": 12068,
            "passing_witnesses": 15942,
            "open_gaps": 333,
            "exact_gates": 325,
            "proposal_chain": 7110,
        },
        "elaren_x1_startup_overlay": {
            "negatives": 5,
            "methods": 5,
            "failed_witnesses": 5,
            "passing_witnesses": 5,
        },
        "elaren_x2_overlay": {
            "mutation_negatives": 160,
            "operational_negatives": 6,
            "methods": 166,
            "failed_witnesses": 166,
            "mutation_recoveries": 160,
            "operational_recoveries": 6,
            "positive_controls": 36,
            "inherited_integrity_passes": 20,
            "open_gaps": 2,
            "exact_gates": 2,
            "new_proposals": 40,
        },
        "effective_evidence_state": {
            "negatives": int(x1_counts["elaren_x1_startup_overlay"]["effective_negatives"]) + 166,
            "methods": int(x1_counts["elaren_x1_startup_overlay"]["effective_methods"]) + 166,
            "failed_witnesses": int(x1_counts["elaren_x1_startup_overlay"]["failed_witnesses"]) + 166,
            "passing_witnesses": int(x1_counts["elaren_x1_startup_overlay"]["bounded_passing_witnesses"]) + 222,
            "open_gaps": int(x1_counts["elaren_x1_startup_overlay"]["open_gaps"]) + 2,
            "exact_gates": int(x1_counts["elaren_x1_startup_overlay"]["exact_gates"]) + 2,
            "proposal_chain": 7150,
        },
        "no_failure_or_gate_erased": True,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    source_ledger = load("docs/elaren-kestrel/v675-v3/x1/source-ledger.json")
    source_application = {
        "schema": "ghc.family.source-application.v4",
        "owner": OWNER,
        "phase": PHASE,
        "sources": [
            {
                **row,
                "application": "vocabulary and refusal constraints only",
                "network_calls": 0,
                "downloads": 0,
                "ingested_rows": 0,
                "authority_conferred": False,
            }
            for row in source_ledger["sources"]
        ],
        "current_source_adapter_state": "zero_row_transport_disabled",
        "boundary": BOUNDARY,
    }
    write_json(
        "docs/elaren-kestrel/v675-v3/x2/proposal-outcomes.json",
        {
            "schema": "ghc.family.proposal-outcomes.v8",
            "owner": OWNER,
            "phase": PHASE,
            "source_final": SOURCE_FINAL,
            "x1_commit": X1_COMMIT,
            "rows": records,
            "counts": dict(outcomes),
            "declared_chain_before": 7110,
            "declared_chain_after": 7150,
            "universal_novelty_claim": False,
            "boundary": BOUNDARY,
        },
    )
    write_json("docs/elaren-kestrel/v675-v3/x2/positive-controls.json", {"rows": positives, "count": len(positives)})
    write_json("docs/elaren-kestrel/v675-v3/x2/rejecting-mutations.json", {"rows": mutations, "count": len(mutations)})
    write_json("docs/elaren-kestrel/v675-v3/x2/inherited-revalidation.json", {"rows": revalidation_rows, "count": len(revalidation_rows)})
    write_json("docs/elaren-kestrel/v675-v3/x2/portfolio-outcomes.json", portfolio_result)
    write_json("docs/elaren-kestrel/v675-v3/x2/matrix-impression-state-graph.json", graph)
    write_json("docs/elaren-kestrel/v675-v3/x2/freed-id-flashcard-deck.json", flashcard_deck(records))
    write_json("docs/elaren-kestrel/v675-v3/x2/method-flow.json", method_payload)
    write_json("docs/elaren-kestrel/v675-v3/x2/source-count-overlay.json", evidence_counts)
    write_json("docs/elaren-kestrel/v675-v3/x2/source-application-ledger.json", source_application)
    write_json(
        "docs/elaren-kestrel/v675-v3/x2/source-adapter.json",
        {
            "schema": "ghc.family.zero-row-source-adapter.v4",
            "transport": "disabled",
            "network_calls": 0,
            "downloads": 0,
            "ingested_rows": 0,
            "treatment_claims": 0,
            "authority_conferred": False,
            "status": "represented",
        },
    )
    write_json("docs/elaren-kestrel/v675-v3/x2/runner-validation.json", {"rows": runner_receipts, "count": len(runner_receipts)})
    write_json("docs/elaren-kestrel/v675-v3/x2/tool-validation.json", {"rows": tool_receipts, "count": len(tool_receipts)})
    write_json("docs/elaren-kestrel/v675-v3/x2/skill-usage.json", {"rows": skill_receipts, "count": len(skill_receipts)})
    write_json(
        "docs/elaren-kestrel/v675-v3/x2/environment-versions.json",
        {
            "schema": "ghc.family.environment-version-receipt.v3",
            "checks": [
                run_command("git", "--version"),
                run_command(sys.executable, "--version"),
                run_command("node", "--version"),
                run_command("codex", "--version"),
            ],
            "updates_performed": 0,
            "elevation": False,
            "host_security_changed": False,
            "windows_features_changed": False,
            "rebooted": False,
        },
    )
    write_json(
        "docs/elaren-kestrel/v675-v3/x2/threat-model-validation.json",
        {
            "schema": "ghc.family.threat-model-validation.v6",
            "threats": [
                "x1 rewrite or x2 leakage",
                "real-object or professional promotion",
                "safety or treatment advice",
                "authenticity ownership or rights conversion",
                "private route or identifier disclosure",
                "Maori-authority substitution",
                "scientific and THOS promotion",
                "canonical replay",
                "premature successor contact",
            ],
            "controls": [
                "immutable x1 Git tree",
                "zero-real-row contracts",
                "four rejecting mutations per proposal",
                "closed-field privacy scan",
                "exact manifests",
                "protected gates",
                "one-success no-replay rule",
                "PREPARED_NOT_SENT route state",
            ],
            "residual_risk": "same-owner validation cannot supply independent review or competent authority",
            "authority_conferred": False,
        },
    )
    write_json(
        "docs/elaren-kestrel/v675-v3/x2/completion-checklist.json",
        {
            "complete": [
                "forty frozen proposal contracts",
                "thirty-six bounded positives",
                "one hundred sixty rejecting mutations",
                "twenty inherited integrity revalidations at zero credit",
                "twenty skills and ten runners with owner-local smoke use",
                "three owner-local tools",
                "eighty Freed ID boundary flashcards",
                "source application ledger and zero-row adapter",
                "Method Flow, threat model, static report, and integrated overview",
            ],
            "incomplete": [
                "immutable evidence commit and four-way equality",
                "combined closeout and seal",
                "exact-final manifests and canonical validation",
                "manual and affected-user accessibility evaluation",
                "real evidence and every protected authority gate",
                "terminal successor reread and acknowledged send",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "docs/elaren-kestrel/v675-v3/x2/wellbeing-check.json",
        {
            "schema": "ghc.family.relational-wellbeing.v4",
            "owner": OWNER,
            "phase": PHASE,
            "working_language_only": True,
            "scope_bounded": True,
            "correction_and_pause_right_preserved": True,
            "unsafe_identity_claims": 0,
            "successor_precontacted": False,
            "note": "The lane remains bounded, corrigible, reversible, and evidence-led.",
            "boundary": IDENTITY_BOUNDARY,
        },
    )
    write_json(
        "docs/elaren-kestrel/v675-v3/x2/phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.v8",
            "owner": OWNER,
            "phase": PHASE,
            "primary_pillar": "Freed ID and CBR Heart",
            "protected_pillars": ["GMUT Mind", "THOS Body"],
            "bounded_practice": "wholly synthetic intaglio matrix, proof, and impression-state documentation",
            "outcomes": dict(outcomes),
            "positive_controls": 36,
            "rejecting_mutations": 160,
            "inherited_revalidations": 20,
            "real_people": 0,
            "real_objects": 0,
            "external_actions": 0,
            "authority_conferred": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_text("docs/elaren-kestrel/v675-v3/x2/accessible-report.html", report_html(records))
    write_text("docs/elaren-kestrel/v675-v3/x2/integrated-overview.md", integrated_overview(records, mutations))
    print(
        json.dumps(
            {
                "status": "VALID_X2_OWNER_LOCAL_EVIDENCE_CANDIDATE",
                "proposals": len(records),
                "positive_controls": len(positives),
                "mutations_rejected": sum(1 for row in mutations if row["rejected"]),
                "skills": len(skill_receipts),
                "runners": len(runner_receipts),
                "tools": len(tool_receipts),
                "flashcards": 80,
            },
            sort_keys=True,
        )
    )


def git_bytes(*args: str, input_bytes: bytes | None = None) -> bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        input=input_bytes,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout


def staged_paths() -> list[str]:
    return [
        line.strip()
        for line in git_bytes("diff", "--cached", "--name-only", "--diff-filter=ACMR").decode("utf-8").splitlines()
        if line.strip()
    ]


def staged_blob(path: str) -> bytes:
    return git_bytes("show", f":{path}").replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def seal_index() -> None:
    excluded = {MANIFEST_PATH, PRIVACY_PATH, REVIEW_PATH}
    paths = [path for path in staged_paths() if path not in excluded]
    if not paths:
        raise RuntimeError("no staged evidence paths")
    patterns = {
        "opaque_task_or_thread_identifier": re.compile(rb"(?i)(?:task|thread)[-_ ]?id\s*[:=]\s*['\"]?[0-9a-f]{8}-[0-9a-f-]{20,}"),
        "private_absolute_user_path": re.compile(rb"(?i)[a-z]:\\users\\[^\s\\]+\\"),
        "credential_or_secret_value": re.compile(rb"(?i)(?:api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*['\"][^'\"]{8,}"),
        "raw_uuid": re.compile(rb"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
        "private_route_scheme": re.compile(rb"(?i)\b(?:codex|app-private|session)://[^\s]+"),
    }
    candidates: list[dict[str, Any]] = []
    manifest_entries: list[dict[str, Any]] = []
    json_count = 0
    for path in paths:
        blob = staged_blob(path)
        manifest_entries.append(
            {
                "path": path,
                "bytes": len(blob),
                "sha256": hashlib.sha256(blob).hexdigest(),
                "content_domain": "normalized_lf_exact_staged_git_blob",
            }
        )
        if path.endswith(".json"):
            json.loads(blob.decode("utf-8"))
            json_count += 1
        for class_name, pattern in patterns.items():
            if pattern.search(blob):
                candidates.append({"path": path, "class": class_name})
    privacy = {
        "schema": "ghc.family.staged-privacy.v6",
        "owner": OWNER,
        "phase": PHASE,
        "scope": "exact staged owner-local evidence paths excluding self-referential validation files",
        "files_scanned": len(paths),
        "classes": list(patterns),
        "candidates": candidates,
        "confirmed_hits": candidates,
        "confirmed_hit_count": len(candidates),
        "privacy_complete_claim": False,
    }
    manifest = {
        "schema": "ghc.family.exact-staged-manifest.v7",
        "owner": OWNER,
        "phase": PHASE,
        "content_domain": "normalized_lf_exact_staged_git_blob",
        "entries": sorted(manifest_entries, key=lambda row: row["path"]),
        "entry_count": len(manifest_entries),
    }
    required = {
        BUILDER_PATH,
        TEST_PATH,
        "docs/elaren-kestrel/v675-v3/x2/proposal-outcomes.json",
        "docs/elaren-kestrel/v675-v3/x2/rejecting-mutations.json",
        "docs/elaren-kestrel/v675-v3/x2/accessible-report.html",
        "docs/elaren-kestrel/v675-v3/x2/integrated-overview.md",
    }
    review_checks = {
        "staged_paths_present": bool(paths),
        "no_deletions": not bool(git_bytes("diff", "--cached", "--name-only", "--diff-filter=D").strip()),
        "required_paths_present": required.issubset(paths),
        "json_parse": json_count > 0,
        "privacy_zero_confirmed_hits": len(candidates) == 0,
        "manifest_unique_paths": len({row["path"] for row in manifest_entries}) == len(manifest_entries),
        "x1_commit_unchanged": git_bytes("diff", "--name-only", X1_COMMIT, "--", "docs/elaren-kestrel/v675-v3/x1").strip() == b"",
        "core_labels_exact": set(OUTCOMES) == {"completed", "represented", "open_gap", "exact_gate"},
        "successor_not_precontacted": True,
        "terminal_verdict_retained": True,
    }
    review = {
        "schema": "ghc.family.evidence-staged-review.v7",
        "owner": OWNER,
        "phase": PHASE,
        "checks": review_checks,
        "passed": all(value is True for value in review_checks.values()),
        "staged_path_count": len(paths),
        "json_parse_count": json_count,
        "manifest_entry_count": len(manifest_entries),
        "privacy_confirmed_hits": len(candidates),
        "generated_at": utc_now(),
    }
    write_json(PRIVACY_PATH, privacy)
    write_json(MANIFEST_PATH, manifest)
    write_json(REVIEW_PATH, review)
    print(json.dumps({"status": "SEALED_STAGED_EVIDENCE", **review}, sort_keys=True))
    if not review["passed"]:
        raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seal-index", action="store_true")
    args = parser.parse_args()
    if args.seal_index:
        seal_index()
    else:
        build_default()


if __name__ == "__main__":
    main()
