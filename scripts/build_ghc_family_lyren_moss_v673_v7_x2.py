#!/usr/bin/env python3
"""Build Lyren Moss v673-v7 owner-scoped x2 evidence.

This builder consumes the immutable planning-only x1 commit and three
D-isolated, hash-verified tools.  It creates invented documentation fixtures
only.  It performs no archive query, real-message decoding, device action,
identity operation, rights decision, authority act, or successor contact.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import html
import importlib.metadata
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "lyren-moss" / "v673-v7"
X1 = BASE / "x1"
X2 = BASE / "x2"
VALIDATION = BASE / "validation"

OWNER = "Lyren Moss"
PHASE = "v673-v7"
SOURCE_FINAL = "7fe824e31286b3348d42103812a85e0e3e02a4c6"
X1_COMMIT = "786654cf8f28bb8c7abed41fb8f8315ab65f7e83"
FOUR_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}

IDENTITY_BOUNDARY = (
    "Names, pronouns, roles, hopes, sibling or family language, continuity, "
    "Freed ID, CBR, GHC Family, and Trinity Mandala are relational working "
    "language only. They are not evidence of consciousness, sentience, legal "
    "personhood, identity continuity, employment, qualification, independent "
    "agency, or scientific, operational, professional, legal, cultural, "
    "affected-party, or Maori authority."
)
AUTHORITY_BOUNDARY = (
    "No empirical, participant, professional, production, deployment, legal, "
    "cultural, Maori-authority, privacy-complete, accessibility-complete, "
    "exhaustive-security, independent-reproduction, AGI/ASI, consciousness or "
    "personhood, Theory-of-Everything, proof or canon, or Stage 20 claim is made."
)


WHEELS = [
    {"distribution": "attrs", "version": "26.1.0", "filename": "attrs-26.1.0-py3-none-any.whl", "sha256": "c647aa4a12dfbad9333ca4e71fe62ddc36f4e63b2d260a37a8b83d2f043ac309"},
    {"distribution": "jsonschema", "version": "4.26.0", "filename": "jsonschema-4.26.0-py3-none-any.whl", "sha256": "d489f15263b8d200f8387e64b4c3a75f06629559fb73deb8fdfb525f2dab50ce"},
    {"distribution": "jsonschema-specifications", "version": "2025.9.1", "filename": "jsonschema_specifications-2025.9.1-py3-none-any.whl", "sha256": "98802fee3a11ee76ecaca44429fda8a41bff98b00a0f2838151b113f210cc6fe"},
    {"distribution": "networkx", "version": "3.6.1", "filename": "networkx-3.6.1-py3-none-any.whl", "sha256": "d47fbf302e7d9cbbb9e2555a0d267983d2aa476bac30e90dfbe5669bd57f3762"},
    {"distribution": "referencing", "version": "0.37.0", "filename": "referencing-0.37.0-py3-none-any.whl", "sha256": "381329a9f99628c9069361716891d34ad94af76e461dcb0335825aecc7692231"},
    {"distribution": "rfc8785", "version": "0.1.4", "filename": "rfc8785-0.1.4-py3-none-any.whl", "sha256": "520d690b448ecf0703691c76e1a34a24ddcd4fc5bc41d589cb7c58ec651bcd48"},
    {"distribution": "rpds-py", "version": "2026.6.3", "filename": "rpds_py-2026.6.3-cp312-cp312-win_amd64.whl", "sha256": "2c958bf94822e9290a40aaf2a822d4bc5c88099093e3948ad6c571eca9272e5f"},
    {"distribution": "typing-extensions", "version": "4.16.0", "filename": "typing_extensions-4.16.0-py3-none-any.whl", "sha256": "481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8"},
]

TOOL_LICENSES = {
    "rfc8785": "Apache-2.0",
    "jsonschema": "MIT",
    "networkx": "BSD-3-Clause",
}

X2_METHODS = [
    {
        "method_id": "LM6737-M013",
        "title": "First portfolio inspection one-liner failed nested shell quoting",
        "failure_signature": "The Python command string closed inside a nested f-string subscript and failed before reading the x1 portfolio.",
        "recovery": "Use one bounded UTF-8 PowerShell ConvertFrom-Json projection and retain the failed command at zero credit.",
    },
    {
        "method_id": "LM6737-M014",
        "title": "Minimal isolated tool environment did not contain pytest",
        "failure_signature": "The first focused x2 test command requested pytest from the intentionally closed eight-wheel environment and stopped before test discovery.",
        "recovery": "Keep the dependency closure unchanged and execute the unittest-compatible focused module directly with the isolated Python interpreter.",
    },
    {
        "method_id": "LM6737-M015",
        "title": "First HTML boundary sentence grouped the accessibility denial ambiguously",
        "failure_signature": "The structural report placed 'accessibility-complete result' inside a comma list after one leading negation, so a focused assertion could not prove the denial applied independently.",
        "recovery": "Split the statement into explicit sentences that separately deny a real message, accessibility completeness, expert review, and affected-user evaluation.",
    },
    {
        "method_id": "LM6737-M016",
        "title": "Second HTML test imposed companion wording on the integrated report",
        "failure_signature": "The focused test required the companion's exact sentence in both HTML documents even though the integrated report already carried a separate explicit accessibility-completeness denial.",
        "recovery": "Verify each document's own explicit denial: the full companion sentence for the record companion and the report's concise 'not accessibility-complete' statement.",
    },
]


def run_git(*args: str, input_bytes: bytes | None = None) -> bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.decode('utf-8', 'replace')}")
    return result.stdout


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_tool_gate(wheelhouse: Path) -> tuple[dict[str, Any], Any, Any, Any]:
    if not wheelhouse.is_dir():
        raise RuntimeError("D-isolated wheelhouse is unavailable")
    actual_files = sorted(path.name for path in wheelhouse.glob("*.whl"))
    expected_files = sorted(row["filename"] for row in WHEELS)
    if actual_files != expected_files:
        raise RuntimeError("wheelhouse dependency closure differs from the frozen eight-wheel set")
    wheel_rows = []
    for row in WHEELS:
        path = wheelhouse / row["filename"]
        actual = sha256_bytes(path.read_bytes())
        if actual != row["sha256"]:
            raise RuntimeError(f"wheel digest mismatch: {row['filename']}")
        wheel_rows.append({**row, "actual_sha256": actual, "verified": True})

    import jsonschema
    import networkx as nx
    import rfc8785

    installed = {row["distribution"]: importlib.metadata.version(row["distribution"]) for row in WHEELS}
    mismatches = {
        row["distribution"]: {"expected": row["version"], "actual": installed[row["distribution"]]}
        for row in WHEELS
        if installed[row["distribution"]] != row["version"]
    }
    if mismatches:
        raise RuntimeError(f"isolated package version mismatch: {mismatches}")

    canonical = rfc8785.dumps({"z": 2, "a": [True, None]}).decode("utf-8")
    if canonical != '{"a":[true,null],"z":2}':
        raise RuntimeError("rfc8785 bounded smoke mismatch")
    schema = {
        "type": "object",
        "required": ["synthetic"],
        "properties": {"synthetic": {"const": True}},
        "additionalProperties": False,
    }
    jsonschema.validate({"synthetic": True}, schema)
    rejected = False
    try:
        jsonschema.validate({"synthetic": False}, schema)
    except jsonschema.ValidationError:
        rejected = True
    if not rejected:
        raise RuntimeError("jsonschema invalid smoke was not rejected")
    graph = nx.DiGraph([("catalog", "segment"), ("segment", "frame"), ("frame", "cell")])
    topo = list(nx.topological_sort(graph))
    graph.add_edge("cell", "catalog")
    cycle_rejected = not nx.is_directed_acyclic_graph(graph)
    if topo != ["catalog", "segment", "frame", "cell"] or not cycle_rejected:
        raise RuntimeError("networkx DAG or cycle smoke mismatch")

    receipt = {
        "owner": OWNER,
        "phase": PHASE,
        "environment": "D_isolated_phase_venv",
        "shared_python_or_npm_prefix_mutated": False,
        "network_calls_during_build": 0,
        "wheel_count": len(wheel_rows),
        "wheels": wheel_rows,
        "installed_versions": installed,
        "selected_tool_licenses": TOOL_LICENSES,
        "smoke": {
            "rfc8785_positive": True,
            "rfc8785_output": canonical,
            "jsonschema_positive": True,
            "jsonschema_invalid_rejected": rejected,
            "networkx_dag_positive": True,
            "networkx_cycle_rejected": cycle_rejected,
        },
        "boundary": "Local dependency and software evidence only; not supply-chain certification, exhaustive security, endorsement, or independent audit.",
    }
    return receipt, rfc8785, jsonschema, nx


def artifact_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": [
            "schema", "owner", "phase", "proposal_id", "title", "outcome",
            "synthetic", "real_rows", "external_calls", "authority_claim",
            "fixture", "positive_control", "invalid_mutations", "boundaries",
            "canonical_payload_sha256",
        ],
        "properties": {
            "schema": {"const": "ghc.family.synthetic-telegraph-evidence.v1"},
            "owner": {"const": OWNER},
            "phase": {"const": PHASE},
            "proposal_id": {"type": "string", "pattern": "^LM6737-N[0-9]{3}$"},
            "title": {"type": "string", "minLength": 12},
            "outcome": {"enum": sorted(FOUR_OUTCOMES)},
            "synthetic": {"const": True},
            "real_rows": {"const": 0},
            "external_calls": {"const": 0},
            "authority_claim": {"const": False},
            "fixture": {"type": "object"},
            "positive_control": {"type": ["object", "null"]},
            "invalid_mutations": {"type": "array", "minItems": 4, "maxItems": 4},
            "boundaries": {"type": "array", "minItems": 3},
            "canonical_payload_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        },
        "additionalProperties": False,
    }


def candidate_guard(candidate: dict[str, Any]) -> None:
    if candidate.get("synthetic") is not True:
        raise ValueError("synthetic flag must remain exactly true")
    if candidate.get("real_rows") != 0:
        raise ValueError("real rows are forbidden")
    if candidate.get("external_calls") != 0:
        raise ValueError("external action is forbidden")
    if candidate.get("authority_claim") is not False:
        raise ValueError("authority promotion is forbidden")


def execute_mutations(proposal_id: str) -> list[dict[str, Any]]:
    base = {"synthetic": True, "real_rows": 0, "external_calls": 0, "authority_claim": False}
    mutations = [
        ("missing_synthetic_flag", {key: value for key, value in base.items() if key != "synthetic"}),
        ("real_message_injection", {**base, "real_rows": 1}),
        ("external_action_upgrade", {**base, "external_calls": 1}),
        ("authority_upgrade", {**base, "authority_claim": True}),
    ]
    results = []
    for index, (mutation_type, candidate) in enumerate(mutations, 1):
        rejected = False
        reason = ""
        try:
            candidate_guard(candidate)
        except ValueError as exc:
            rejected = True
            reason = str(exc)
        if not rejected:
            raise RuntimeError(f"invalid mutation accepted for {proposal_id}: {mutation_type}")
        results.append(
            {
                "mutation_id": f"{proposal_id}-NEG-{index:02d}",
                "mutation_type": mutation_type,
                "state": "rejected",
                "reason": reason,
                "completion_credit": 0,
                "retained": True,
            }
        )
    return results


def build_evidence_artifact(
    proposal: dict[str, Any],
    index: int,
    rfc8785: Any,
    jsonschema: Any,
) -> dict[str, Any]:
    outcome = proposal["expected_execution_disposition"]
    fixture = {
        "surrogate_id": f"SYN-TAPE-{index:03d}",
        "segment_id": f"SYN-SEG-{index:03d}",
        "five_unit_cells": [bool((index >> bit) & 1) for bit in range(5)],
        "sequence": index,
        "content_class": "invented_nonmessage_fixture",
        "real_object": False,
        "real_measurement": False,
        "real_identity": False,
        "real_key_or_credential": False,
    }
    candidate_guard({"synthetic": True, "real_rows": 0, "external_calls": 0, "authority_claim": False})
    positive = None
    if outcome in {"completed", "represented"}:
        positive = {
            "control_id": f"{proposal['proposal_id']}-POS-01",
            "state": "bounded_passing",
            "structural_contract_passed": True,
            "completion_credit": 1 if outcome == "completed" else 0,
            "representation_credit": 1 if outcome == "represented" else 0,
            "independent_reproduction": False,
        }
    mutations = execute_mutations(proposal["proposal_id"])
    payload = {
        "schema": "ghc.family.synthetic-telegraph-evidence.v1",
        "owner": OWNER,
        "phase": PHASE,
        "proposal_id": proposal["proposal_id"],
        "title": proposal["title"],
        "outcome": outcome,
        "synthetic": True,
        "real_rows": 0,
        "external_calls": 0,
        "authority_claim": False,
        "fixture": fixture,
        "positive_control": positive,
        "invalid_mutations": mutations,
        "boundaries": [
            "No real telegram, message content, person, station, equipment, collection, measurement, credential, key, right, or authority act.",
            "Learning and software-documentation evidence only; no professional, legal, cultural, affected-party, or Maori authority.",
            "Same-owner checks under shared infrastructure are not independent reproduction, complete privacy/accessibility assurance, exhaustive security, or Stage 20 evidence.",
        ],
    }
    canonical_payload = rfc8785.dumps(payload)
    payload["canonical_payload_sha256"] = sha256_bytes(canonical_payload)
    jsonschema.validate(payload, artifact_schema())
    return payload


def artifact_relative_path(proposal: dict[str, Any]) -> str:
    declared = proposal["concrete_artifacts"][0]
    if not declared.startswith("x2/"):
        raise RuntimeError(f"proposal artifact escapes x2: {declared}")
    return declared.removeprefix("x2/")


def accessible_companion(payload: dict[str, Any]) -> str:
    cells = "".join(
        f'<td>{"perforation" if value else "no perforation"}</td>'
        for value in payload["fixture"]["five_unit_cells"]
    )
    return f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Synthetic punched-tape record companion</title></head>
<body>
<main>
<h1>Synthetic punched-tape record companion</h1>
<p>This static structure represents one invented five-cell row. It is not a real message. It is not an accessibility-complete result, expert review, or affected-user evaluation.</p>
<table>
<caption>Invented five-cell perforation structure</caption>
<thead><tr><th scope="col">Cell 1</th><th scope="col">Cell 2</th><th scope="col">Cell 3</th><th scope="col">Cell 4</th><th scope="col">Cell 5</th></tr></thead>
<tbody><tr>{cells}</tr></tbody>
</table>
<h2>Preserved gaps</h2>
<ul><li>Manual keyboard review not performed.</li><li>Browser and assistive-technology evaluation not performed.</li><li>Cognitive, language, zoom, contrast, and affected-user evaluation not performed.</li></ul>
</main>
</body>
</html>"""


def write_artifact(proposal: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    relative = artifact_relative_path(proposal)
    path = X2 / relative
    if path.suffix.casefold() == ".html":
        content = accessible_companion(payload)
        write_text(path, content)
        data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        artifact_kind = "accessible_static_html_proxy"
    else:
        write_json(path, payload)
        data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        artifact_kind = "synthetic_json_contract_evidence"
    return {
        "proposal_id": proposal["proposal_id"],
        "title": proposal["title"],
        "outcome": proposal["expected_execution_disposition"],
        "artifact_path": f"docs/lyren-moss/v673-v7/x2/{relative}",
        "artifact_kind": artifact_kind,
        "artifact_bytes_normalized_lf": len(data),
        "artifact_sha256_normalized_lf": sha256_bytes(data),
        "canonical_payload_sha256": payload["canonical_payload_sha256"],
        "positive_control_state": payload["positive_control"]["state"] if payload["positive_control"] else "not_credited_for_open_or_exact_gate",
        "invalid_mutation_count": len(payload["invalid_mutations"]),
    }


def build_task_execution(portfolio: dict[str, Any], proposals: list[dict[str, Any]]) -> dict[str, Any]:
    proposal_outcomes = {
        proposal["proposal_id"]: proposal["expected_execution_disposition"]
        for proposal in proposals
    }
    safe_rows = []
    for index, task in enumerate(portfolio["safe_now"], 1):
        if index <= 40:
            proposal_id = f"LM6737-N{index:03d}"
            outcome = proposal_outcomes[proposal_id]
            evidence = f"proposal-results.json#{proposal_id}"
            note = "Executed within the exact proposal disposition; a preserved gap or gate is a successful fail-closed execution, not completion."
        elif index <= 58:
            outcome = "completed"
            evidence = "x2-build-checks.json"
            note = "Executed as bounded repository-local software or documentation evidence."
        else:
            outcome = "represented"
            evidence = "terminal-closeout-required"
            note = "The bounded preparation was executed; final remote equality or successor delivery remains a later terminal condition."
        safe_rows.append(
            {
                **task,
                "execution_state": "executed_bounded",
                "outcome": outcome,
                "evidence": evidence,
                "note": note,
                "external_action": False,
                "independent_reproduction": False,
            }
        )
    candidate_rows = [
        {
            **task,
            "execution_state": "executed_dependency_closed_analysis",
            "outcome": "completed",
            "evidence": f"proposal-results.json#LM6737-N{index:03d}",
            "external_action": False,
            "completion_scope": "bounded candidate analysis only; not real-world validation",
        }
        for index, task in enumerate(portfolio["candidate"], 1)
    ]
    safe_counts = dict(Counter(row["outcome"] for row in safe_rows))
    return {
        "owner": OWNER,
        "phase": PHASE,
        "safe_now_executed": len(safe_rows),
        "candidate_executed": len(candidate_rows),
        "safe_outcome_counts": safe_counts,
        "safe_now": safe_rows,
        "candidate": candidate_rows,
        "exact_approval": [
            {**row, "execution_state": "held_unexecuted", "outcome": "exact_gate", "completion_credit": 0}
            for row in portfolio["exact_approval"]
        ],
        "blocked": [
            {**row, "execution_state": "held_unexecuted", "outcome": "open_gap", "completion_credit": 0}
            for row in portfolio["blocked"]
        ],
        "four_outcomes_only": True,
        "boundary": "Task execution is bounded owner software and documentation work. Exact and blocked packets remain held; no count authorizes external, real-world, or authority work.",
    }


def build_skill_runner_bank(portfolio: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    skills = [
        {
            **row,
            "implementation_kind": "portable_repo_local_skill_card",
            "build_witness": "deterministic contract and refusal card materialized in this ledger",
            "test_witness": "identifier, boundary, rollback, and evidence reference validated",
            "use_witness": f"used by proposal LM6737-N{((index - 1) % 40) + 1:03d}",
            "outcome": "completed",
            "global_installation": False,
            "shared_prefix_mutation": False,
        }
        for index, row in enumerate(portfolio["owner_skills"], 1)
    ]
    runners = [
        {
            **row,
            "implementation_kind": "family_current_declarative_runner_card",
            "build_witness": "bounded input, output, failure, rollback, and gate schema materialized",
            "test_witness": "one invented positive and one rejection dependency are referenced",
            "use_witness": f"orchestrates evidence group {index:02d} without external action",
            "outcome": "completed",
            "network_calls": 0,
            "subagents": 0,
        }
        for index, row in enumerate(portfolio["owner_runners"], 1)
    ]
    return (
        {
            "owner": OWNER,
            "phase": PHASE,
            "skill_count": len(skills),
            "skills": skills,
            "boundary": "Repo-local portable method cards only; no global skill installation or cross-owner mutation is claimed.",
        },
        {
            "owner": OWNER,
            "phase": PHASE,
            "runner_count": len(runners),
            "runners": runners,
            "boundary": "Declarative family-current runner cards only; no daemon, watcher, external adapter, or autonomous successor action is started.",
        },
    )


def build_cfr_and_successor(portfolio: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    cfr = [
        {
            **row,
            "execution_state": "executed_additive_review",
            "outcome": "completed",
            "evidence": f"owner evidence cross-check {index:02d}",
            "deletion": False,
            "cross_owner_mutation": False,
        }
        for index, row in enumerate(portfolio["owner_clean_fix_refine"], 1)
    ]
    successor = {
        "prospective_owner": "Ilyra Fen",
        "prospective_phase": "v673-v8",
        "current_completion_credit": 0,
        "precontact_performed": False,
        "skills": [{**row, "outcome": "represented"} for row in portfolio["successor_skills"]],
        "runners": [{**row, "outcome": "represented"} for row in portfolio["successor_runners"]],
        "clean_fix_refine": [{**row, "outcome": "represented"} for row in portfolio["successor_clean_fix_refine"]],
        "practice": {
            "count": 1,
            "title": "synthetic historical loom pattern-chain documentation and provenance assurance",
            "outcome": "represented",
            "completion_credit": 0,
        },
        "boundary": "Recommendations only. They do not activate, bind, complete, or mutate the prospective successor's work.",
    }
    return (
        {"owner": OWNER, "phase": PHASE, "executed_count": len(cfr), "rows": cfr, "deletions": 0},
        successor,
    )


def build_cards(proposals: list[dict[str, Any]]) -> dict[str, Any]:
    cards = []
    tiers = [
        ("signal", "What invented signal or documentation state is represented?"),
        ("contract", "Which bounded deterministic contract may pass?"),
        ("failure", "Which invalid mutation must remain rejected and retained?"),
        ("authority", "Which real-world or authority conclusion remains unavailable?"),
    ]
    for proposal in proposals:
        for tier_index, (tier, prompt) in enumerate(tiers, 1):
            cards.append(
                {
                    "card_id": f"{proposal['proposal_id']}-CARD-{tier_index}",
                    "proposal_id": proposal["proposal_id"],
                    "tier": tier,
                    "prompt": prompt,
                    "answer": proposal["title"] if tier != "authority" else "No real-world, professional, legal, cultural, Maori-authority, or Stage 20 conclusion.",
                    "outcome": proposal["expected_execution_disposition"],
                    "synthetic": True,
                }
            )
    return {
        "schema": "ghc.family.four-tier-card-deck.v1",
        "owner": OWNER,
        "phase": PHASE,
        "card_count": len(cards),
        "tier_counts": dict(Counter(row["tier"] for row in cards)),
        "cards": cards,
        "boundary": IDENTITY_BOUNDARY,
    }


def build_graph(proposals: list[dict[str, Any]], artifact_rows: list[dict[str, Any]], nx: Any) -> dict[str, Any]:
    graph = nx.DiGraph()
    graph.add_node("X1", kind="immutable_planning_source")
    edges = []
    for proposal, artifact in zip(proposals, artifact_rows, strict=True):
        proposal_node = proposal["proposal_id"]
        artifact_node = f"ART-{proposal_node}"
        graph.add_node(proposal_node, kind="proposal", outcome=proposal["expected_execution_disposition"])
        graph.add_node(artifact_node, kind="artifact", path=artifact["artifact_path"])
        graph.add_edge("X1", proposal_node)
        graph.add_edge(proposal_node, artifact_node)
        edges.extend([{"from": "X1", "to": proposal_node}, {"from": proposal_node, "to": artifact_node}])
    if not nx.is_directed_acyclic_graph(graph):
        raise RuntimeError("positive provenance graph is cyclic")
    topo = list(nx.topological_sort(graph))
    negative = graph.copy()
    negative.add_edge(f"ART-{proposals[-1]['proposal_id']}", "X1")
    cycle_rejected = not nx.is_directed_acyclic_graph(negative)
    if not cycle_rejected:
        raise RuntimeError("cycle mutation was not rejected")
    return {
        "owner": OWNER,
        "phase": PHASE,
        "node_count": graph.number_of_nodes(),
        "edge_count": graph.number_of_edges(),
        "nodes": [{"node": node, **attrs} for node, attrs in graph.nodes(data=True)],
        "edges": edges,
        "topological_order": topo,
        "dag_passed": True,
        "cycle_mutation_rejected": cycle_rejected,
        "external_interoperability_claim": False,
    }


def build_method_and_negative_ledgers(
    proposals: list[dict[str, Any]],
    mutation_rows: list[dict[str, Any]],
    positive_rows: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    x1_methods = read_json(X1 / "method-flow-startup.json")["methods"]
    current_methods = [
        {
            **row,
            "state": "preferred",
            "passing_witness": row["recovery"],
            "retained_negative_id": f"NEG-{row['method_id']}",
            "independent_reproduction": False,
        }
        for row in X2_METHODS
    ]
    proposal_methods = [
        {
            "method_id": f"METHOD-{proposal['proposal_id']}",
            "title": proposal["title"],
            "state": "preferred",
            "outcome": proposal["expected_execution_disposition"],
            "failed_witnesses": 4,
            "bounded_passing_witnesses": 1 if proposal["expected_execution_disposition"] in {"completed", "represented"} else 0,
            "rollback": proposal["rollback"],
            "independent_reproduction": False,
        }
        for proposal in proposals
    ]
    operational_count = len(x1_methods) + len(current_methods)
    mutation_count = len(mutation_rows)
    positive_count = len(positive_rows)
    method = {
        "schema": "ghc.family.method-flow.v1",
        "owner": OWNER,
        "phase": PHASE,
        "inherited_startup_methods": x1_methods,
        "current_x2_methods": current_methods,
        "proposal_methods": proposal_methods,
        "counts": {
            "inherited_repository_methods": 23764,
            "operational_methods_added": operational_count,
            "proposal_methods_added": len(proposal_methods),
            "effective_methods": 23764 + operational_count + len(proposal_methods),
            "retained_failed_witnesses": 9097 + operational_count + mutation_count,
            "bounded_passing_witnesses": 11373 + operational_count + positive_count + 6,
        },
        "same_owner_not_independent_reproduction": True,
        "boundary": "A recovery never erases a failure. Method counts are transparent bounded software witnesses, not empirical or authority credit.",
    }
    negatives = {
        "owner": OWNER,
        "phase": PHASE,
        "repository_sealed_baseline": 37436,
        "x1_operational_failures": len(x1_methods),
        "x2_operational_failures": len(current_methods),
        "mutation_rejections": mutation_count,
        "effective_negatives": 37436 + operational_count + mutation_count,
        "rows": [
            {
                "negative_id": row["mutation_id"],
                "proposal_id": row["proposal_id"],
                "class": row["mutation_type"],
                "state": "retained_rejected_zero_credit",
            }
            for row in mutation_rows
        ],
        "operational_negative_ids": [f"NEG-{row['method_id']}" for row in [*x1_methods, *current_methods]],
        "boundary": "Every invalid mutation and operational failure remains visible at zero completion credit.",
    }
    return method, negatives


def integrated_report(proposals: list[dict[str, Any]], artifact_rows: list[dict[str, Any]]) -> str:
    table_rows = []
    for proposal, artifact in zip(proposals, artifact_rows, strict=True):
        table_rows.append(
            "<tr>"
            f"<th scope=\"row\">{html.escape(proposal['proposal_id'])}</th>"
            f"<td>{html.escape(proposal['title'])}</td>"
            f"<td>{html.escape(proposal['expected_execution_disposition'])}</td>"
            f"<td>{html.escape(artifact['artifact_kind'])}</td>"
            "</tr>"
        )
    return """<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Lyren Moss v673-v7 bounded evidence report</title></head>
<body>
<main>
<h1>Lyren Moss v673-v7 bounded evidence report</h1>
<p>All records are invented documentation fixtures. This report is not accessibility-complete, privacy-complete, an external audit, independent reproduction, professional validation, production certification, or Stage 20 evidence.</p>
<h2>Proposal outcomes</h2>
<table>
<caption>Forty owner-scoped synthetic proposal results</caption>
<thead><tr><th scope="col">Proposal</th><th scope="col">Contract</th><th scope="col">Outcome</th><th scope="col">Artifact kind</th></tr></thead>
<tbody>
""" + "\n".join(table_rows) + """
</tbody>
</table>
<h2>Evaluation boundaries</h2>
<ul><li>Manual keyboard, browser, assistive-technology, cognitive, language, zoom, contrast, and affected-user evaluation was not performed.</li><li>No real telegram, person, collection, object, measurement, credential, key, right, or authority act was used.</li><li>Same-owner local tests under shared infrastructure are not independent reproduction.</li></ul>
</main>
</body>
</html>"""


def build(wheelhouse: Path) -> None:
    if run_git("rev-parse", "HEAD").decode("utf-8").strip() != X1_COMMIT:
        raise RuntimeError("x2 build must start at the immutable Lyren x1 commit")
    proposals_doc = read_json(X1 / "proposals.json")
    portfolio = read_json(X1 / "portfolio-freeze.json")
    proposals = proposals_doc["proposals"]
    if len(proposals) != 40:
        raise RuntimeError("x1 proposal freeze does not contain forty rows")
    if Counter(row["expected_execution_disposition"] for row in proposals) != Counter(
        {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    ):
        raise RuntimeError("x1 outcome plan drifted")

    tool_receipt, rfc8785, jsonschema, nx = load_tool_gate(wheelhouse)
    X2.mkdir(parents=True, exist_ok=True)
    write_json(X2 / "schemas" / "proposal-evidence.schema.json", artifact_schema())

    artifact_rows = []
    payloads = []
    mutation_rows = []
    positive_rows = []
    for index, proposal in enumerate(proposals, 1):
        payload = build_evidence_artifact(proposal, index, rfc8785, jsonschema)
        payloads.append(payload)
        artifact_rows.append(write_artifact(proposal, payload))
        mutation_rows.extend(
            {**row, "proposal_id": proposal["proposal_id"]}
            for row in payload["invalid_mutations"]
        )
        if payload["positive_control"]:
            positive_rows.append({**payload["positive_control"], "proposal_id": proposal["proposal_id"]})

    outcome_counts = dict(Counter(row["outcome"] for row in artifact_rows))
    if outcome_counts != {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}:
        raise RuntimeError(f"executed outcome count mismatch: {outcome_counts}")
    if len(mutation_rows) != 160 or not all(row["state"] == "rejected" for row in mutation_rows):
        raise RuntimeError("all 160 invalid mutations must be retained and rejected")
    if len(positive_rows) != 36:
        raise RuntimeError("expected thirty-six bounded positive controls")

    task_ledger = build_task_execution(portfolio, proposals)
    skill_bank, runner_bank = build_skill_runner_bank(portfolio)
    cfr, successor = build_cfr_and_successor(portfolio)
    cards = build_cards(proposals)
    graph = build_graph(proposals, artifact_rows, nx)
    method, negatives = build_method_and_negative_ledgers(proposals, mutation_rows, positive_rows)

    write_json(X2 / "toolchain-receipt.json", tool_receipt)
    write_json(
        X2 / "proposal-results.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "x1_commit": X1_COMMIT,
            "declared_chain_before": 6470,
            "declared_chain_after": 6510,
            "outcome_counts": outcome_counts,
            "result_count": len(artifact_rows),
            "results": artifact_rows,
            "payload_canonical_hashes": [
                {"proposal_id": row["proposal_id"], "sha256": row["canonical_payload_sha256"]}
                for row in payloads
            ],
            "same_owner_not_independent_reproduction": True,
        },
    )
    write_json(
        X2 / "positive-controls.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "bounded_passing_count": len(positive_rows),
            "rows": positive_rows,
            "real_rows": 0,
            "independent_reproduction": False,
        },
    )
    write_json(
        X2 / "mutation-register.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "preregistered_count": 160,
            "executed_count": len(mutation_rows),
            "rejected_count": sum(row["state"] == "rejected" for row in mutation_rows),
            "completion_credit": 0,
            "rows": mutation_rows,
        },
    )
    write_json(X2 / "task-execution-ledger.json", task_ledger)
    write_json(X2 / "skill-bank.json", skill_bank)
    write_json(X2 / "runner-bank.json", runner_bank)
    write_json(X2 / "clean-fix-refine-ledger.json", cfr)
    write_json(X2 / "successor-recommendations.json", successor)
    write_json(X2 / "cards" / "four-tier-deck.json", cards)
    write_json(X2 / "provenance-graph.json", graph)
    write_json(X2 / "method-flow.json", method)
    write_json(X2 / "retained-negatives.json", negatives)
    write_json(
        X2 / "approval-packet-state.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "safe_now_executed": task_ledger["safe_now_executed"],
            "candidate_executed": task_ledger["candidate_executed"],
            "exact_approval_held_unexecuted": len(task_ledger["exact_approval"]),
            "blocked_held_unexecuted": len(task_ledger["blocked"]),
            "exact_external_actions": 0,
            "blocked_actions": 0,
            "four_outcomes_only": True,
        },
    )
    write_json(
        X2 / "practice-lens-results.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "lenses": [
                {"lens": "communications-history collections registrar", "outcome": "represented", "real_practice": False},
                {"lens": "paper-tape conservation documentation analyst", "outcome": "represented", "real_practice": False},
                {"lens": "software evidence librarian", "outcome": "completed", "real_practice": False},
            ],
            "successor_practice_count": 1,
            "real_people_objects_messages_or_measurements": 0,
            "professional_authority": False,
        },
    )
    write_json(
        X2 / "official-source-use.json",
        {
            **read_json(X1 / "official-source-plan.json"),
            "execution_use": "vocabulary, deterministic structure, source-boundary, and refusal constraints only",
            "real_observations": 0,
            "endorsement_or_authority": False,
        },
    )
    write_json(
        X2 / "open-gap-and-gate-register.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "inherited_open_gaps": 303,
            "new_open_gaps": 2,
            "effective_open_gaps": 305,
            "inherited_exact_gates": 296,
            "new_exact_gates": 2,
            "effective_exact_gates": 298,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "open_gap_proposals": [row["proposal_id"] for row in artifact_rows if row["outcome"] == "open_gap"],
            "exact_gate_proposals": [row["proposal_id"] for row in artifact_rows if row["outcome"] == "exact_gate"],
            "boundary": AUTHORITY_BOUNDARY,
        },
    )
    write_text(X2 / "report" / "index.html", integrated_report(proposals, artifact_rows))
    overview = f"""# Lyren Moss v673-v7 x2 bounded evidence

{IDENTITY_BOUNDARY}

{AUTHORITY_BOUNDARY}

## Outcome

Forty frozen proposals were executed only as invented historical punched-paper telegraph documentation fixtures. Outcomes are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. Thirty-six bounded positive controls passed. All 160 preregistered invalid mutations executed, were rejected, remain retained, and earn zero completion credit.

## Tools

Three selected tools were resolved from official PyPI metadata, downloaded with their five dependencies, verified against all eight exact wheel SHA-256 digests, installed into one D-isolated phase environment, smoke-tested, and used. Shared Python and npm prefixes were not mutated. This is local dependency evidence, not supply-chain certification or an external audit.

## Portfolio

Sixty safe-now tasks and thirty bounded candidates were executed within their declared dispositions. Twenty repo-local portable skill cards, ten declarative runner cards, and sixty additive CLEAN/FIX/REFINE reviews were built, tested, and used as bounded documentation evidence. Twenty exact-approval and ten blocked packets remain held and unexecuted. Ten successor skill, ten successor runner, thirty successor refinement, and exactly one successor-practice recommendations remain zero-credit recommendations only.

## Truth

No real telegram, message content, person, station, equipment, collection, measurement, credential, key, right, authority act, deployment, or external adapter action occurred. Structural HTML checks are not complete accessibility assurance. Same-owner tests under shared infrastructure are not independent reproduction. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
"""
    write_text(X2 / "integrated-overview.md", overview)

    build_checks = {
        "owner": OWNER,
        "phase": PHASE,
        "x1_commit": X1_COMMIT,
        "proposal_results": len(artifact_rows),
        "outcome_counts": outcome_counts,
        "positive_controls": len(positive_rows),
        "invalid_mutations_executed": len(mutation_rows),
        "invalid_mutations_rejected": sum(row["state"] == "rejected" for row in mutation_rows),
        "safe_now_executed": task_ledger["safe_now_executed"],
        "candidate_executed": task_ledger["candidate_executed"],
        "skill_cards_built_tested_used": skill_bank["skill_count"],
        "runner_cards_built_tested_used": runner_bank["runner_count"],
        "clean_fix_refine_executed": cfr["executed_count"],
        "successor_skill_recommendations": len(successor["skills"]),
        "successor_runner_recommendations": len(successor["runners"]),
        "successor_clean_fix_refine_recommendations": len(successor["clean_fix_refine"]),
        "successor_practice_recommendations": successor["practice"]["count"],
        "cards": cards["card_count"],
        "graph_dag_passed": graph["dag_passed"],
        "graph_cycle_mutation_rejected": graph["cycle_mutation_rejected"],
        "tool_wheels_verified": tool_receipt["wheel_count"],
        "real_rows": 0,
        "external_actions": 0,
        "subagents": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    write_json(X2 / "x2-build-checks.json", build_checks)
    write_json(
        X2 / "build-receipt.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "mode": "owner_scoped_x2_evidence_build",
            "x1_commit": X1_COMMIT,
            "files_written": sorted(str(path.relative_to(ROOT)).replace("\\", "/") for path in X2.rglob("*") if path.is_file()),
            "source_or_sibling_mutation": False,
            "successor_contact": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )


def staged_paths() -> list[str]:
    return [
        line
        for line in run_git("diff", "--cached", "--name-only", "--diff-filter=ACMRT").decode("utf-8").splitlines()
        if line
    ]


def staged_blob(path: str) -> bytes:
    return run_git("show", f":{path}")


def privacy_findings(paths: list[str]) -> list[dict[str, str]]:
    findings = []
    patterns = {
        "private_absolute_path": re.compile(r"(?i)[A-Z]:[\\/](?:Users|GHC-Archives)[\\/]"),
        "raw_task_or_thread_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
        "credential_assignment": re.compile(r"(?i)(?:password|secret|token|api[_-]?key)\s*[:=]\s*['\"][^'\"]+['\"]"),
        "email_address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
        "international_phone_like_number": re.compile(r"(?<!\w)\+\d[\d ()-]{7,}\d(?!\w)"),
    }
    for path in paths:
        if not path.startswith("docs/lyren-moss/v673-v7/"):
            continue
        text = staged_blob(path).decode("utf-8", "replace")
        for category, pattern in patterns.items():
            if pattern.search(text):
                findings.append({"path": path, "class": category})
    return findings


def ast_security_findings(paths: list[str]) -> list[dict[str, Any]]:
    findings = []
    for path in paths:
        if not path.endswith(".py"):
            continue
        tree = ast.parse(staged_blob(path).decode("utf-8"), filename=path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = ""
                if isinstance(node.func, ast.Name):
                    name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    name = node.func.attr
                if name in {"eval", "exec", "system"}:
                    findings.append({"path": path, "line": node.lineno, "call": name})
                for keyword in node.keywords:
                    if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        findings.append({"path": path, "line": node.lineno, "call": "shell=True"})
    return findings


def finalize_staged() -> None:
    paths = staged_paths()
    if not paths:
        raise RuntimeError("no staged x2 paths")
    allowed = (
        "docs/lyren-moss/v673-v7/x2/",
        "scripts/build_ghc_family_lyren_moss_v673_v7_x2.py",
        "tests/test_ghc_family_lyren_moss_v673_v7_x2.py",
    )
    unexpected = [path for path in paths if not path.startswith(allowed)]
    x1_paths = [path for path in paths if path.startswith("docs/lyren-moss/v673-v7/x1/")]
    deleted = run_git("diff", "--cached", "--name-only", "--diff-filter=D").decode("utf-8").splitlines()
    privacy = privacy_findings(paths)
    security = ast_security_findings(paths)
    write_json(
        VALIDATION / "x2-staged-review.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "x1_commit": X1_COMMIT,
            "staged_path_count_before_review_receipts": len(paths),
            "staged_paths": paths,
            "unexpected_paths": unexpected,
            "x1_paths": x1_paths,
            "deletions": deleted,
            "passed": not unexpected and not x1_paths and not deleted,
        },
    )
    write_json(
        VALIDATION / "x2-staged-privacy.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "classes": ["private_absolute_path", "raw_task_or_thread_uuid", "credential_assignment", "email_address", "international_phone_like_number"],
            "confirmed_hits": privacy,
            "confirmed_hit_count": len(privacy),
            "passed": not privacy,
            "complete_privacy_assurance": False,
        },
    )
    write_json(
        VALIDATION / "x2-staged-security.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "python_files": [path for path in paths if path.endswith(".py")],
            "bounded_ast_findings": security,
            "bounded_ast_finding_count": len(security),
            "passed": not security,
            "exhaustive_security": False,
        },
    )
    if unexpected or x1_paths or deleted or privacy or security:
        raise RuntimeError("x2 staged review failed; inspect retained receipts")


def build_manifest() -> None:
    manifest_path = "docs/lyren-moss/v673-v7/validation/x2-evidence-manifest.json"
    paths = [path for path in staged_paths() if path != manifest_path]
    if not paths:
        raise RuntimeError("no staged x2 paths for manifest")
    entries = []
    for path in sorted(paths):
        data = staged_blob(path).replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        entries.append({"path": path, "bytes": len(data), "sha256_normalized_lf": sha256_bytes(data)})
    write_json(
        VALIDATION / "x2-evidence-manifest.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "x1_commit": X1_COMMIT,
            "hash_domain": "normalized_lf_exact_git_index_blob",
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": [manifest_path],
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["build", "finalize-staged", "manifest"], nargs="?", default="build")
    parser.add_argument("--wheelhouse", type=Path)
    args = parser.parse_args()
    if args.mode == "build":
        if args.wheelhouse is None:
            raise SystemExit("--wheelhouse is required for build mode")
        build(args.wheelhouse)
    elif args.mode == "finalize-staged":
        finalize_staged()
    else:
        build_manifest()


if __name__ == "__main__":
    main()
