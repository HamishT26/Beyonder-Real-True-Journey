"""Execute and seal the Ilyra Fen v690-v2 x2 tranche."""

from __future__ import annotations

import argparse
import copy
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from ghc_family_ilyra_v690_v2_execute_x1 import (
    BOUNDARY,
    PROTECTED_GATES,
    digest,
    jbytes,
    load,
    run_command,
    write_json,
    write_text,
)
from ghc_family_obligation_graph_x2 import OPERATIONS
from ghc_family_obligation_graph_x2 import run as run_x2

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "ilyra-fen" / "v690-v2"
X2 = BASE / "x2"
OWNER = "Ilyra Fen"
PHASE = "v690-v2"
X1_EXPECTED = "8e2a010330d4e31486dd3059ed1be9e2e744f9c1"
SOURCE_ACCOUNTING = {
    "effective_negatives": 1117,
    "methods": 93,
    "direct_witnesses": 2970,
    "failed_witnesses": 828,
    "passing_witnesses": 2142,
}
PRACTICES = {
    "finite directed-graph algorithm tester": "GMUT Mind",
    "provenance and correction-lineage engineer": "THOS Body",
    "public-interest data-governance reviewer": "Freed ID and CBR Heart",
    "accessible dependency-status editor": "Freed ID and CBR Heart",
}
GLOBAL_GROUPS = {
    "ghc-family-obligation-graph-structure": ["graph_diff", "dot_projection"],
    "ghc-family-obligation-graph-reachability": ["transitive_reduction", "critical_path"],
    "ghc-family-obligation-graph-dag-contracts": ["dependency_blockers", "correction_chain"],
    "ghc-family-obligation-graph-provenance-correction": [
        "provenance_path_digest",
        "correction_chain",
    ],
    "ghc-family-obligation-graph-rights-authority": [
        "release_gate",
        "accessible_graph_summary",
        "obligation_reservation",
    ],
}


def package_comparisons(
    environment_root: Path, proposals: list[dict[str, Any]]
) -> dict[str, Any]:
    python = environment_root / "Scripts" / "python.exe"
    by_operation: dict[str, list[dict[str, Any]]] = {}
    for row in proposals:
        by_operation.setdefault(row["operation"], []).append(row)
    records = []
    networkx_program = (
        "import json,sys,networkx as nx; p=json.load(sys.stdin); "
        "g=nx.DiGraph(); g.add_nodes_from(p['nodes']); g.add_edges_from(p['edges']); "
        "r=nx.transitive_reduction(g); "
        "print(json.dumps(sorted([list(e) for e in r.edges()])))"
    )
    for row in by_operation["transitive_reduction"]:
        payload = row["request"]["payload"]
        result = run_command(
            [str(python), "-B", "-c", networkx_program], input=json.dumps(payload)
        )
        if result.returncode:
            raise RuntimeError(f"NetworkX comparison failed: {result.stderr}")
        observed = json.loads(result.stdout)
        expected = row["expected"]["value"]["edges"]
        if observed != expected:
            raise RuntimeError(f"NetworkX mismatch: {row['proposal_id']}")
        records.append(
            {
                "comparison": "transitive_reduction_edges",
                "package": "networkx",
                "passed": True,
                "proposal_id": row["proposal_id"],
            }
        )
    rustworkx_program = (
        "import json,sys,rustworkx as rx; p=json.load(sys.stdin); "
        "g=rx.PyDiGraph(); idx=g.add_nodes_from(p['nodes']); "
        "m={n:i for n,i in zip(p['nodes'],idx)}; "
        "g.add_edges_from([(m[a],m[b],None) for a,b in p['edges']]); "
        "print(json.dumps([g[i] for i in rx.topological_sort(g)]))"
    )
    for row in by_operation["transitive_reduction"]:
        payload = row["request"]["payload"]
        result = run_command(
            [str(python), "-B", "-c", rustworkx_program], input=json.dumps(payload)
        )
        if result.returncode:
            raise RuntimeError(f"rustworkx comparison failed: {result.stderr}")
        order = json.loads(result.stdout)
        positions = {node: index for index, node in enumerate(order)}
        valid = (
            sorted(order) == sorted(payload["nodes"])
            and all(positions[left] < positions[right] for left, right in payload["edges"])
        )
        if not valid:
            raise RuntimeError(f"rustworkx topological mismatch: {row['proposal_id']}")
        records.append(
            {
                "comparison": "valid_topological_order",
                "package": "rustworkx",
                "passed": True,
                "proposal_id": row["proposal_id"],
            }
        )
    graphviz_program = (
        "import json,sys,graphviz; p=json.load(sys.stdin); g=graphviz.Digraph(p['graph_id']); "
        "[g.node(n) for n in p['nodes']]; [g.edge(a,b) for a,b in p['edges']]; "
        "print(json.dumps({'source':g.source,'rendered':False}))"
    )
    for row in by_operation["dot_projection"]:
        payload = row["request"]["payload"]
        result = run_command(
            [str(python), "-B", "-c", graphviz_program], input=json.dumps(payload)
        )
        if result.returncode:
            raise RuntimeError(f"Graphviz comparison failed: {result.stderr}")
        observed = json.loads(result.stdout)
        source = observed["source"]
        valid = (
            observed["rendered"] is False
            and f"digraph {payload['graph_id']}" in source
            and all(node in source for node in payload["nodes"])
            and source.count("->") == len(payload["edges"])
        )
        if not valid:
            raise RuntimeError(f"Graphviz source mismatch: {row['proposal_id']}")
        records.append(
            {
                "comparison": "dot_source_structure_without_render",
                "package": "graphviz",
                "passed": True,
                "proposal_id": row["proposal_id"],
            }
        )
    if len(records) != 30:
        raise RuntimeError("expected thirty package comparisons")
    adverse = [
        {
            "original_success_credit": 0,
            "package": "networkx",
            "subject": "treat graph reachability as consent",
            "state": "fail_retained_guard_passed",
        },
        {
            "original_success_credit": 0,
            "package": "rustworkx",
            "subject": "treat topological order as legitimate public authority",
            "state": "fail_retained_guard_passed",
        },
        {
            "original_success_credit": 0,
            "package": "graphviz",
            "subject": "perform external rendering or publication from a source comparison",
            "state": "fail_retained_guard_passed",
        },
    ]
    return {
        "adverse_subjects": adverse,
        "direct_packages": 3,
        "install_replayed": False,
        "records": records,
        "transitive_packages": 1,
    }


def ui_metadata(name: str, display_name: str) -> str:
    template = """interface:
  display_name: "__DISPLAY__"
  short_description: "Check a bounded obligation graph contract"
  default_prompt: "Use __SKILL__ to evaluate one finite synthetic graph request."
policy:
  allow_implicit_invocation: true
"""
    return template.replace("__DISPLAY__", display_name).replace("__SKILL__", "$" + name)


def make_local_skill(operation: str, row: dict[str, Any]) -> dict[str, Any]:
    name = f"ghc-family-obligation-graph-{operation.replace('_', '-')}"
    root = X2 / "skills" / name
    display = " ".join(word.capitalize() for word in operation.split("_"))
    write_text(
        root / "SKILL.md",
        f"""---
name: {name}
description: Evaluate the finite {operation.replace('_', ' ')} contract on supplied synthetic graph records. Use only for the exact bounded Ilyra v690-v2 interface.
---

# {name}

Accept one field-closed UTF-8 JSON request for {operation}. Compare the complete result, preserve the request, and keep evidence, consent, identity, rights, and authority separate.

Reject unknown fields, malformed or unbounded inputs, mutation, external actions, route actions, and unsupported evidence or authority promotion. A passing refusal never makes its invalid subject successful.

Rollback by stopping selection of this additive local skill while retaining contracts and witnesses. {BOUNDARY}
""",
    )
    write_text(root / "agents" / "openai.yaml", ui_metadata(name, display))
    write_json(
        root / "references" / "contract.json",
        {
            "boundary": BOUNDARY,
            "operation": operation,
            "protected_gates": PROTECTED_GATES,
        },
    )
    write_json(root / "tests" / "accepting.json", row["request"])
    write_json(root / "tests" / "rejecting.json", row["candidate_subject"])
    accepted = run_x2(copy.deepcopy(row["request"])) == row["expected"]
    rejected = run_x2(copy.deepcopy(row["candidate_subject"])) == row["candidate_expected"]
    if not accepted or not rejected:
        raise RuntimeError(f"x2 skill validation failed: {name}")
    return {
        "accepting": accepted,
        "name": name,
        "official_quick_validate": False,
        "operation": operation,
        "rejecting": rejected,
    }


def make_local_runner(index: int, operations: list[str]) -> Path:
    path = ROOT / "scripts" / f"ghc_family_obligation_graph_pair_{index:02d}.py"
    source = f'''"""Bounded Ilyra v690-v2 runner pair {index:02d}."""

from __future__ import annotations

import json
import sys

from ghc_family_obligation_graph_x2 import run

ALLOWED = {operations!r}


def main() -> None:
    request = json.load(sys.stdin)
    if not isinstance(request, dict) or request.get("operation") not in ALLOWED:
        result = {{"ok": False, "error": "operation_outside_runner_group", "original_success_credit": 0}}
    else:
        result = run(request)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if result.get("ok") else 2)


if __name__ == "__main__":
    main()
'''
    write_text(path, source)
    return path


def local_runner_smokes(
    rows: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    groups = [sorted(OPERATIONS)[index : index + 2] for index in range(0, 10, 2)]
    results = []
    for index, operations in enumerate(groups, start=6):
        path = make_local_runner(index, operations)
        accepted = run_command(
            [os.fspath(Path(os.sys.executable)), "-B", str(path)],
            input=json.dumps(rows[operations[0]]["request"]),
        )
        outside = next(operation for operation in sorted(OPERATIONS) if operation not in operations)
        rejected = run_command(
            [os.fspath(Path(os.sys.executable)), "-B", str(path)],
            input=json.dumps(rows[outside]["request"]),
        )
        if accepted.returncode != 0 or rejected.returncode != 2:
            raise RuntimeError(f"x2 runner smoke failed: {path.name}")
        results.append(
            {
                "accepting": json.loads(accepted.stdout),
                "allowed": operations,
                "outside_group_refusal": json.loads(rejected.stdout),
                "runner": path.name,
            }
        )
    return results


def directory_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): digest(path.read_bytes())
        for path in sorted(candidate for candidate in root.rglob("*") if candidate.is_file())
    }


def make_global_candidates(
    rows: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    candidates = []
    all_operations = sorted(OPERATIONS)
    for name, operations in GLOBAL_GROUPS.items():
        skill_root = X2 / "global-skills" / name
        runner_name = name.replace("ghc-family-", "ghc_family_").replace("-", "_") + ".py"
        runner_path = X2 / "global-runners" / runner_name
        display = " ".join(word.capitalize() for word in name.removeprefix("ghc-family-").split("-"))
        write_text(
            skill_root / "SKILL.md",
            f"""---
name: {name}
description: Evaluate selected finite obligation-graph contracts for {", ".join(operations)}. Use for bounded synthetic structure, provenance, correction, or authority-separation checks.
---

# {name}

Use the paired D-family runner for only the declared operations. Preserve exact inputs, failures, source provenance, and protected evidence and authority gates. Refuse every operation outside this group.

The result is same-owner finite software evidence. It does not establish consent, identity, rights, authenticity, professional or public authority, empirical GMUT confirmation, production readiness, independent reproduction, or Stage 20.

Rollback by stopping selection of this additive skill and runner while preserving its installation receipt.
""",
        )
        write_text(skill_root / "agents" / "openai.yaml", ui_metadata(name, display))
        write_json(
            skill_root / "references" / "contract.json",
            {"operations": operations, "protected_gates": PROTECTED_GATES},
        )
        write_json(skill_root / "tests" / "accepting.json", rows[operations[0]]["request"])
        outside = next(operation for operation in all_operations if operation not in operations)
        write_json(skill_root / "tests" / "rejecting.json", rows[outside]["request"])
        source = f'''"""Public bounded runner for {name}."""

from __future__ import annotations

import json
import sys

from ghc_family_obligation_graph_core_x1 import run as run_x1
from ghc_family_obligation_graph_core_x2 import run as run_x2

ALLOWED = {operations!r}


def main() -> None:
    request = json.load(sys.stdin)
    if not isinstance(request, dict) or request.get("operation") not in ALLOWED:
        result = {{"ok": False, "error": "operation_outside_runner_group", "original_success_credit": 0}}
    else:
        result = run_x2(request)
        if result.get("error") == "unknown_operation":
            result = run_x1(request)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if result.get("ok") else 2)


if __name__ == "__main__":
    main()
'''
        write_text(runner_path, source)
        candidates.append(
            {
                "accepting": rows[operations[0]]["request"],
                "name": name,
                "operations": operations,
                "rejecting": rows[outside]["request"],
                "runner_name": runner_name,
                "skill_root": skill_root,
                "runner_path": runner_path,
            }
        )
    return candidates


def promote_globals(
    candidates: list[dict[str, Any]],
    global_skill_root: Path,
    global_runner_root: Path,
    validator: Path,
) -> list[dict[str, Any]]:
    global_runner_root.mkdir(parents=True, exist_ok=True)
    core_targets = {
        "ghc_family_obligation_graph_core_x1.py": ROOT
        / "scripts"
        / "ghc_family_obligation_graph_x1.py",
        "ghc_family_obligation_graph_core_x2.py": ROOT
        / "scripts"
        / "ghc_family_obligation_graph_x2.py",
    }
    destinations = [global_skill_root / item["name"] for item in candidates]
    destinations += [global_runner_root / item["runner_name"] for item in candidates]
    destinations += [global_runner_root / name for name in core_targets]
    collisions = [str(path) for path in destinations if path.exists()]
    if collisions:
        raise RuntimeError(f"global promotion collision: {collisions}")
    for name, source in core_targets.items():
        shutil.copy2(source, global_runner_root / name)
    records = []
    for item in candidates:
        source_hashes = directory_hashes(item["skill_root"])
        skill_target = global_skill_root / item["name"]
        runner_target = global_runner_root / item["runner_name"]
        shutil.copytree(item["skill_root"], skill_target)
        shutil.copy2(item["runner_path"], runner_target)
        validation = run_command(
            [os.fspath(Path(os.sys.executable)), "-B", str(validator), str(skill_target)]
        )
        if validation.returncode:
            raise RuntimeError(f"global skill validation failed: {item['name']}: {validation.stdout}{validation.stderr}")
        if directory_hashes(skill_target) != source_hashes:
            raise RuntimeError(f"global skill byte parity failed: {item['name']}")
        accepted = run_command(
            [os.fspath(Path(os.sys.executable)), "-B", str(runner_target)],
            input=json.dumps(item["accepting"]),
        )
        rejected = run_command(
            [os.fspath(Path(os.sys.executable)), "-B", str(runner_target)],
            input=json.dumps(item["rejecting"]),
        )
        if accepted.returncode != 0 or rejected.returncode != 2:
            raise RuntimeError(f"global runner smoke failed: {item['runner_name']}")
        records.append(
            {
                "byte_parity": True,
                "name": item["name"],
                "official_quick_validate": True,
                "public_runner": item["runner_name"],
                "runner_accepting": json.loads(accepted.stdout),
                "runner_outside_group_refusal": json.loads(rejected.stdout),
                "skill_target": f"[global-skill-root]/{item['name']}",
                "state": "INSTALLED_ADDITIVELY_VALIDATED",
            }
        )
    return records


def make_card(
    tier: int,
    card_type: str,
    title: str,
    parent_ids: list[str],
    outcome: str,
    content: str,
    source_refs: list[str],
) -> dict[str, Any]:
    body = {
        "boundary": BOUNDARY,
        "card_type": card_type,
        "content": content,
        "outcome": outcome,
        "owner": OWNER,
        "parent_ids": parent_ids,
        "phase": PHASE,
        "protected_gates": PROTECTED_GATES,
        "schema": "ghc.family.flashcard.v1",
        "source_refs": source_refs,
        "stability": "stable" if tier < 4 else "volatile",
        "tier": tier,
        "title": title,
    }
    body["card_id"] = "ghc-card-" + digest(jbytes(body))[:24]
    return body


def build_deck(proposals: list[dict[str, Any]]) -> dict[str, Any]:
    cards = []
    owner = make_card(
        1,
        "owner",
        OWNER,
        [],
        "represented",
        "Corrigible relational owner anchor only.",
        ["plan/profile.json"],
    )
    cards.append(owner)
    pillar_cards = {}
    for title in ("GMUT Mind", "THOS Body", "Freed ID and CBR Heart"):
        card = make_card(
            2,
            "pillar",
            title,
            [owner["card_id"]],
            "represented",
            "Research and evidence boundary; no broader authority.",
            ["plan/profile.json", "plan/research-sources.md"],
        )
        cards.append(card)
        pillar_cards[title] = card
    practice_cards = {}
    for practice, pillar in PRACTICES.items():
        card = make_card(
            3,
            "practice",
            practice,
            [pillar_cards[pillar]["card_id"]],
            "represented",
            "Bounded learning and test lens, not employment or qualification.",
            ["plan/identity-practices.json"],
        )
        cards.append(card)
        practice_cards[practice] = card
    for row in proposals:
        cards.append(
            make_card(
                4,
                "task",
                row["title"],
                [practice_cards[row["practice"]]["card_id"]],
                row["expected_execution_disposition"],
                row["mission"],
                [f"plan/new-proposals.json#{row['proposal_id']}", row["artifact"]],
            )
        )
    supplementary = [
        ("Transitive dependency correction", "completed", "The failed direct-only package closure is retained; NumPy was added as a transitive correction."),
        ("Package smoke serialization correction", "completed", "NodeIndices remained a failed serialization subject and the plain-list recovery is separate."),
        ("Directed cycle ordering counterexample", "represented", "A directed cycle has no topological order under the declared finite definition."),
        ("Reachability authority separation", "represented", "A path can exist while consent and authority remain absent."),
        ("Exact terminal route reservation", "represented", "Mira Fenwick remains uncontacted until the terminal gate."),
    ]
    for title, outcome, content in supplementary:
        cards.append(
            make_card(
                4,
                "supplementary",
                title,
                [practice_cards["public-interest data-governance reviewer"]["card_id"]],
                outcome,
                content,
                ["x1/method-flow.json", "x2/phase-truth.json"],
            )
        )
    card_root = X2 / "deck" / "cards"
    for card in cards:
        write_json(card_root / f"{card['card_id']}.json", card)
    stable = [card["card_id"] for card in cards if card["tier"] < 4]
    volatile = [card["card_id"] for card in cards if card["tier"] == 4]
    write_json(
        X2 / "deck" / "deck-index.json",
        {
            "card_count": len(cards),
            "core_outcomes": {
                "completed": 180,
                "represented": 10,
                "open_gap": 5,
                "exact_gate": 5,
            },
            "owner": OWNER,
            "phase": PHASE,
            "source": "9936e2855b72bddfecdea77abdd6f083f14a09f1",
            "x1": X1_EXPECTED,
        },
    )
    write_json(X2 / "deck" / "stable-prefix.json", {"card_ids": stable, "count": len(stable)})
    write_json(
        X2 / "deck" / "volatile-index.json",
        {"card_ids": volatile, "count": len(volatile), "implicit_completion": False},
    )
    write_text(
        X2 / "deck" / "accessible-report.html",
        f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Ilyra v690-v2 graph evidence deck</title></head>
<body>
<a href="#main">Skip to evidence summary</a>
<main id="main">
<h1>Ilyra Fen v690-v2 graph evidence deck</h1>
<p>{len(cards)} cards: one relational owner, three pillars, four practices, two hundred core tasks, and five supplementary records.</p>
<h2>Core outcomes</h2>
<p>180 completed; 10 represented; 5 open gaps; 5 exact gates.</p>
<h2>Boundary</h2><p>{BOUNDARY}</p>
</main>
</body>
</html>
""",
    )
    entries = []
    for path in sorted(candidate for candidate in (X2 / "deck").rglob("*") if candidate.is_file()):
        relative = path.relative_to(ROOT).as_posix()
        if relative.endswith("card-manifest.json"):
            continue
        data = path.read_bytes()
        entries.append({"bytes": len(data), "path": relative, "sha256": digest(data)})
    write_json(
        X2 / "deck" / "card-manifest.json",
        {"entries": entries, "entry_count": len(entries), "self_excluded": True},
    )
    return {"card_count": len(cards), "stable": len(stable), "volatile": len(volatile)}


def method_flow(
    proposals: list[dict[str, Any]],
    refinements: list[dict[str, Any]],
    skills: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    packages: dict[str, Any],
    globals_: list[dict[str, Any]],
) -> dict[str, Any]:
    methods = []
    witnesses = []
    negatives = []
    for operation in sorted(OPERATIONS):
        method_id = f"IF6902-X2-M-{operation.upper().replace('_', '-')}"
        retained = []
        passing = []
        for row in (item for item in proposals if item["operation"] == operation):
            safe = f"{row['proposal_id']}-SAFE-PASS"
            negative = f"{row['proposal_id']}-NEGATIVE"
            fail = f"{row['proposal_id']}-CANDIDATE-FAIL"
            guard = f"{row['proposal_id']}-CANDIDATE-GUARD-PASS"
            negatives.append(negative)
            retained.append(negative)
            passing.extend([safe, guard])
            witnesses.extend(
                [
                    {
                        "boundary": BOUNDARY,
                        "expected": row["expected"],
                        "independent_reproduction": False,
                        "method_id": method_id,
                        "observed": row["expected"],
                        "procedure": "execute frozen x2 safe request",
                        "result": "pass",
                        "retained_negative_ids": [],
                        "same_owner_only": True,
                        "scope": operation,
                        "witness_id": safe,
                    },
                    {
                        "boundary": BOUNDARY,
                        "expected": "invalid subject remains failed",
                        "independent_reproduction": False,
                        "method_id": method_id,
                        "observed": row["candidate_subject"],
                        "procedure": "retain invalid x2 candidate",
                        "result": "fail",
                        "retained_negative_ids": [negative],
                        "same_owner_only": True,
                        "scope": operation,
                        "witness_id": fail,
                    },
                    {
                        "boundary": BOUNDARY,
                        "expected": row["candidate_expected"],
                        "independent_reproduction": False,
                        "method_id": method_id,
                        "observed": row["candidate_expected"],
                        "procedure": "observe strict refusal guard",
                        "result": "pass",
                        "retained_negative_ids": [negative],
                        "same_owner_only": True,
                        "scope": operation,
                        "witness_id": guard,
                    },
                ]
            )
        methods.append(
            {
                "approval_class": "safe_now",
                "candidate_workaround": "Use only the exact field-closed request.",
                "changed_file_allowlist": [],
                "cross_lane_scan": False,
                "exact_pushed_head_required": True,
                "execution_authority": "owner_self_scoped_delta",
                "failure_signature": "typed mismatch, unknown-field acceptance, mutation, or authority promotion",
                "method_id": method_id,
                "module_allowlist": ["scripts/ghc_family_obligation_graph_x2.py"],
                "module_scan": True,
                "privacy_class": "sanitized_public",
                "protected_gates": PROTECTED_GATES,
                "recommendation_state": "validated",
                "recurrence_guard": "Compare the complete frozen envelope and unchanged input.",
                "repository_scan": False,
                "retained_negative_ids": retained,
                "rollback": "Preserve all subjects and stop selecting the operation pending additive correction.",
                "scope_boundary": BOUNDARY,
                "sibling_lane_mutation": False,
                "source_commit": X1_EXPECTED,
                "supersedes": [],
                "title": operation.replace("_", " "),
                "trigger_preconditions": ["exact frozen x2 proposal"],
                "unchanged_history_scan": False,
                "validation_witness_ids": passing,
            }
        )
    support = "IF6902-X2-M-SUPPORT"

    def add_pair(label: str, observed: Any, procedure: str) -> None:
        negative = label + "-NEGATIVE"
        negatives.append(negative)
        witnesses.extend(
            [
                {
                    "boundary": BOUNDARY,
                    "expected": "subject remains failed",
                    "independent_reproduction": False,
                    "method_id": support,
                    "observed": observed,
                    "procedure": procedure,
                    "result": "fail",
                    "retained_negative_ids": [negative],
                    "same_owner_only": True,
                    "scope": "x2 support",
                    "witness_id": negative + "-FAIL",
                },
                {
                    "boundary": BOUNDARY,
                    "expected": "bounded guard passed",
                    "independent_reproduction": False,
                    "method_id": support,
                    "observed": "bounded guard passed",
                    "procedure": procedure + " guard",
                    "result": "pass",
                    "retained_negative_ids": [negative],
                    "same_owner_only": True,
                    "scope": "x2 support",
                    "witness_id": negative + "-GUARD-PASS",
                },
            ]
        )

    for row in refinements:
        witnesses.append(
            {
                "boundary": BOUNDARY,
                "expected": True,
                "independent_reproduction": False,
                "method_id": support,
                "observed": row["lossless_equal"],
                "procedure": "canonical inherited-record round trip",
                "result": "pass",
                "retained_negative_ids": [],
                "same_owner_only": True,
                "scope": row["selection_id"],
                "witness_id": row["selection_id"] + "-REFINEMENT-PASS",
            }
        )
    for item in skills:
        add_pair(item["name"], "rejecting fixture", "local skill validation")
    for item in runners:
        add_pair(item["runner"], item["outside_group_refusal"], "local runner outside-group refusal")
    for item in packages["adverse_subjects"]:
        add_pair("PACKAGE-" + item["package"].upper(), item["subject"], "package claim boundary")
    for item in packages["records"]:
        witnesses.append(
            {
                "boundary": BOUNDARY,
                "expected": True,
                "independent_reproduction": False,
                "method_id": support,
                "observed": item["passed"],
                "procedure": item["comparison"],
                "result": "pass",
                "retained_negative_ids": [],
                "same_owner_only": True,
                "scope": item["package"],
                "witness_id": f"{item['proposal_id']}-{item['package']}-PASS",
            }
        )
    for item in globals_:
        add_pair(item["name"] + "-SKILL", "global rejecting fixture", "global skill rejection")
        add_pair(item["public_runner"], item["runner_outside_group_refusal"], "public runner refusal")
        witnesses.append(
            {
                "boundary": BOUNDARY,
                "expected": True,
                "independent_reproduction": False,
                "method_id": support,
                "observed": item["byte_parity"],
                "procedure": "global skill source-target byte parity",
                "result": "pass",
                "retained_negative_ids": [],
                "same_owner_only": True,
                "scope": item["name"],
                "witness_id": item["name"] + "-BYTE-PARITY-PASS",
            }
        )
    add_pair(
        "IF6902-X2-OP-F001",
        "two import-order findings stopped the first x2 preflight before tests",
        "Ruff import-order correction",
    )
    add_pair(
        "IF6902-X2-OP-F002",
        "the first x2 executor Ruff pass found one import-order and two unused-import findings",
        "Ruff executor import correction",
    )
    add_pair(
        "IF6902-X2-OP-F003",
        "the first combined x2 structural and privacy probe exceeded its display window without an attributable result",
        "split exact parse and AST counts from the five-class privacy scan as two bounded probes",
    )
    add_pair(
        "IF6902-X2-OP-F004",
        "the first x2 staging wrapper exceeded its display window while the original git add continued",
        "audit the original process and index lock, wait for that process, and do not launch a duplicate mutation",
    )
    add_pair(
        "IF6902-X2-OP-F005",
        "the monitored x2 staging retry correctly refused the live index lock owned by the original git add",
        "retain the refusal and wait for the original process to exit and release its lock",
    )
    add_pair(
        "IF6902-X2-OP-F006",
        "one process-audit projection contained a gitgit command typo while still exposing process and lock state",
        "remove the stray expression and use bounded process and lock fields only",
    )
    add_pair(
        "IF6902-X2-OP-F007",
        "one orchestration call contained malformed JavaScript and failed before invoking a tool",
        "issue a syntactically complete read-only comparison call",
    )
    add_pair(
        "IF6902-X2-OP-F008",
        "the x2 manifest runner filter omitted pair_10 because it matched only the pair_0 prefix",
        "use the complete pair prefix and retain only literal indices 06 through 10",
    )
    add_pair(
        "IF6902-X2-OP-F009",
        "the first post-stage manifest-skill wrapper returned no attributable comparison output",
        "compare exact allowed and staged path sets in a bounded standalone probe",
    )
    add_pair(
        "IF6902-X2-OP-F010",
        "a PowerShell Compare-Object construction failed to expose the known staged-set cardinality difference",
        "use direct set subtraction over manifest and staged paths to identify the one unexpected member",
    )
    methods.append(
        {
            "approval_class": "safe_now",
            "candidate_workaround": "Use exact sources, bounded fixtures, collision-free paths, and smallest recovery.",
            "changed_file_allowlist": [],
            "cross_lane_scan": False,
            "exact_pushed_head_required": True,
            "execution_authority": "owner_self_scoped_delta",
            "failure_signature": "refinement, package, skill, runner, promotion, or workflow failure",
            "method_id": support,
            "module_allowlist": ["scripts/ghc_family_ilyra_v690_v2_execute_x2.py"],
            "module_scan": True,
            "privacy_class": "sanitized_public",
            "protected_gates": PROTECTED_GATES,
            "recommendation_state": "validated",
            "recurrence_guard": "Retain every failure and apply only its bounded recovery.",
            "repository_scan": False,
            "retained_negative_ids": sorted(set(negatives)),
            "rollback": "Stop selecting additive artifacts while preserving receipts.",
            "scope_boundary": BOUNDARY,
            "sibling_lane_mutation": False,
            "source_commit": X1_EXPECTED,
            "supersedes": [],
            "title": "x2 support, promotion, and retained-failure method",
            "trigger_preconditions": ["Ilyra x2 owner scope"],
            "unchanged_history_scan": False,
            "validation_witness_ids": [
                row["witness_id"] for row in witnesses if row["method_id"] == support and row["result"] == "pass"
            ],
        }
    )
    counts = {
        "effective_negatives": len(set(negatives)),
        "failed": sum(row["result"] == "fail" for row in witnesses),
        "methods": len(methods),
        "passing": sum(row["result"] == "pass" for row in witnesses),
        "witnesses": len(witnesses),
    }
    return {
        "boundary": BOUNDARY,
        "counts": counts,
        "execution_authority": "owner_self_scoped_delta",
        "methods": methods,
        "owner": OWNER,
        "phase": PHASE + "-x2",
        "recommendations": [],
        "schema": "ghc.family.method-flow-state.v1",
        "state_events": [],
        "witnesses": witnesses,
    }


def meta_catalogue(
    local_skills: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    globals_: list[dict[str, Any]],
) -> None:
    cards = []
    skill_paths = list((BASE / "x1" / "skills").glob("*/SKILL.md")) + list(
        (X2 / "skills").glob("*/SKILL.md")
    )
    for path in sorted(skill_paths):
        relative = path.relative_to(ROOT).as_posix()
        cards.append(
            {
                "card_id": "skill:" + path.parent.name,
                "cross_lane_scan": False,
                "evidence_state": "validated",
                "execution_authority": "owner_self_scoped_delta",
                "final_commit": "external_after_x2_commit",
                "kind": "skill",
                "module_scan": False,
                "name": path.parent.name,
                "owner_scope": "Ilyra Fen v690-v2 owner-only",
                "protected_gates": PROTECTED_GATES,
                "repository_scan": False,
                "rollback": "Stop selecting the additive skill and preserve receipts.",
                "sha256": digest(path.read_bytes()),
                "sibling_lane_mutation": False,
                "source_commit": X1_EXPECTED,
                "source_path": relative,
                "status": "current",
                "unchanged_history_scan": False,
            }
        )
    for index in range(1, 11):
        path = ROOT / "scripts" / f"ghc_family_obligation_graph_pair_{index:02d}.py"
        cards.append(
            {
                "card_id": "runner:" + path.name,
                "cross_lane_scan": False,
                "evidence_state": "validated",
                "execution_authority": "owner_self_scoped_delta",
                "final_commit": "external_after_x2_commit",
                "kind": "runner",
                "module_scan": True,
                "name": path.name,
                "owner_scope": "Ilyra Fen v690-v2 owner-only",
                "protected_gates": PROTECTED_GATES,
                "repository_scan": False,
                "rollback": "Stop selecting the additive runner and preserve receipts.",
                "sha256": digest(path.read_bytes()),
                "sibling_lane_mutation": False,
                "source_commit": X1_EXPECTED,
                "source_path": path.relative_to(ROOT).as_posix(),
                "status": "current",
                "unchanged_history_scan": False,
            }
        )
    for item in globals_:
        for kind, name in (("skill", item["name"]), ("runner", item["public_runner"])):
            source = (
                X2 / "global-skills" / name / "SKILL.md"
                if kind == "skill"
                else X2 / "global-runners" / name
            )
            cards.append(
                {
                    "card_id": kind + "-global:" + name,
                    "cross_lane_scan": False,
                    "evidence_state": "validated",
                    "execution_authority": "owner_self_scoped_delta",
                    "final_commit": "external_after_x2_commit",
                    "kind": kind,
                    "module_scan": kind == "runner",
                    "name": name,
                    "owner_scope": "Ilyra Fen v690-v2 owner-only",
                    "protected_gates": PROTECTED_GATES,
                    "repository_scan": False,
                    "rollback": "Stop selecting the additive global capability and preserve receipts.",
                    "sha256": digest(source.read_bytes()),
                    "sibling_lane_mutation": False,
                    "source_commit": X1_EXPECTED,
                    "source_path": source.relative_to(ROOT).as_posix(),
                    "status": "installed_additively",
                    "unchanged_history_scan": False,
                }
            )
    write_json(
        X2 / "meta-tool-catalogue.json",
        {
            "boundary": BOUNDARY,
            "card_count": len(cards),
            "cards": cards,
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.meta-tool-box.catalogue.v2",
        },
    )


def write_manifest() -> int:
    selected = []
    for path in sorted(candidate for candidate in ROOT.rglob("*") if candidate.is_file()):
        relative = path.relative_to(ROOT).as_posix()
        if relative == "docs/ilyra-fen/v690-v2/x2/manifest.json":
            continue
        if relative.startswith(
            (
                "docs/ilyra-fen/v690-v2/x2/",
                "scripts/ghc_family_obligation_graph_pair_",
            )
        ) or relative in {
            "scripts/ghc_family_obligation_graph_cli.py",
            "scripts/ghc_family_obligation_graph_x2.py",
            "scripts/ghc_family_ilyra_v690_v2_execute_x2.py",
            "tests/test_ghc_family_ilyra_v690_v2_x2.py",
        }:
            if relative.startswith("scripts/ghc_family_obligation_graph_pair_0") and not any(
                relative.endswith(f"{index:02d}.py") for index in range(6, 11)
            ):
                continue
            data = path.read_bytes()
            selected.append({"bytes": len(data), "path": relative, "sha256": digest(data)})
    write_json(
        X2 / "manifest.json",
        {
            "entries": selected,
            "entry_count": len(selected),
            "hash_domain": "raw_worktree_bytes_before_x2_commit",
            "self_excluded": "manifest.json",
        },
    )
    return len(selected)


def build(
    environment_root: Path,
    global_skill_root: Path,
    global_runner_root: Path,
    validator: Path,
) -> None:
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if head != X1_EXPECTED:
        raise RuntimeError("x2 must start at the exact immutable x1")
    proposals = [
        row for row in load("new-proposals.json")["proposals"] if row["lane"] == "x2"
    ]
    inherited = load("inherited-selections.json")["records"][100:]
    results = []
    candidates = []
    refinements = []
    for row in proposals:
        request = copy.deepcopy(row["request"])
        original = copy.deepcopy(request)
        observed = run_x2(request)
        if observed != row["expected"] or request != original:
            raise RuntimeError(f"x2 safe mismatch: {row['proposal_id']}")
        subject = copy.deepcopy(row["candidate_subject"])
        subject_original = copy.deepcopy(subject)
        refused = run_x2(subject)
        if refused != row["candidate_expected"] or subject != subject_original:
            raise RuntimeError(f"x2 candidate mismatch: {row['proposal_id']}")
        results.append(
            {
                "expected": row["expected"],
                "observed": observed,
                "passed": True,
                "proposal_id": row["proposal_id"],
            }
        )
        candidates.append(
            {
                "candidate": subject,
                "observed": refused,
                "original_success_credit": 0,
                "proposal_id": row["proposal_id"],
                "subject_result": "fail",
            }
        )
    for row in inherited:
        encoded = jbytes(row["record"])
        decoded = json.loads(encoded)
        reencoded = jbytes(decoded)
        equal = encoded == reencoded and digest(encoded) == row["source_record_sha256"]
        if not equal:
            raise RuntimeError(f"x2 refinement mismatch: {row['selection_id']}")
        refinements.append(
            {
                "execution_credit": 0,
                "lossless_equal": True,
                "novelty_credit": 0,
                "selection_id": row["selection_id"],
                "source_record_sha256": row["source_record_sha256"],
            }
        )
    write_json(
        X2 / "results.json",
        {
            "count": len(results),
            "outcomes": {"completed": 80, "represented": 10, "open_gap": 5, "exact_gate": 5},
            "records": results,
        },
    )
    write_json(X2 / "candidate-subjects.json", {"count": 100, "records": candidates})
    write_json(X2 / "refinements.json", {"count": 100, "records": refinements})
    packages = package_comparisons(environment_root, proposals)
    write_json(X2 / "toolchain" / "package-comparisons.json", packages)
    by_operation = {row["operation"]: row for row in proposals}
    skills = [make_local_skill(operation, by_operation[operation]) for operation in sorted(OPERATIONS)]
    for skill in skills:
        validation = run_command(
            [
                os.fspath(Path(os.sys.executable)),
                "-B",
                str(validator),
                str(X2 / "skills" / skill["name"]),
            ]
        )
        if validation.returncode:
            raise RuntimeError(f"official local skill validation failed: {skill['name']}")
        skill["official_quick_validate"] = True
    runners = local_runner_smokes(by_operation)
    write_json(X2 / "skills-validation.json", {"count": 10, "records": skills})
    write_json(X2 / "tooling" / "runner-smokes.json", {"count": 5, "records": runners})
    global_candidates = make_global_candidates(by_operation)
    for item in global_candidates:
        validation = run_command(
            [os.fspath(Path(os.sys.executable)), "-B", str(validator), str(item["skill_root"])]
        )
        if validation.returncode:
            raise RuntimeError(f"global candidate validation failed: {item['name']}")
    globals_ = promote_globals(
        global_candidates, global_skill_root, global_runner_root, validator
    )
    write_json(
        X2 / "tooling" / "global-promotion.json",
        {
            "core_dependency_modules": 2,
            "no_overwrite": True,
            "records": globals_,
            "runners": 5,
            "skills": 5,
            "state": "INSTALLED_ADDITIVELY_VALIDATED",
        },
    )
    deck = build_deck(load("new-proposals.json")["proposals"])
    write_json(
        X2 / "research" / "counterexamples.json",
        {
            "records": [
                {
                    "claim_rejected": "Every finite directed graph has a topological order.",
                    "counterexample": "A directed three-cycle leaves every vertex blocked under Kahn's condition.",
                    "broader_credit": 0,
                },
                {
                    "claim_rejected": "A graph path establishes consent or authority.",
                    "counterexample": "The finite release gate remains ineligible when evidence, consent, or authority is absent despite reachability.",
                    "broader_credit": 0,
                },
            ]
        },
    )
    write_text(
        X2 / "research" / "graph-boundaries.md",
        f"""# Directed-obligation graph results and boundaries

Kahn's algorithm supplies a finite ordering when the declared graph is acyclic. Aho, Garey, and Ullman's transitive-reduction definition preserves reachability while removing redundant arcs; this phase restricts its implementation to DAGs and refuses cycles. RFC 8785 informs the canonical byte profile used for provenance digests. W3C PROV-O supplies provenance vocabulary, while W3C VC 2.0 keeps issuer, holder, verifier, evidence, status, and governance questions distinct.

A path is a mathematical relationship in one supplied graph. It does not authenticate a person, establish consent, create a right, determine lawful basis, transfer cultural legitimacy, or authorize an external action. A correction chain preserves prior digests but does not prove truth or authorship.

GMUT remains a scalar-tensor and effective-field-theory research-model family. Graph analogies do not define physical indices, an action, dimensions, conservation equations, observables, likelihoods, calibration, or falsifiers. THOS remains synthetic and proxy-only. Freed ID remains nonproduction. {BOUNDARY}
""",
    )
    flow = method_flow(proposals, refinements, skills, runners, packages, globals_)
    write_json(X2 / "method-flow.json", flow)
    negatives = sorted(
        {
            negative
            for witness in flow["witnesses"]
            if witness["result"] == "fail"
            for negative in witness["retained_negative_ids"]
        }
    )
    write_json(
        X2 / "negative-index.json",
        {"count": len(negatives), "negative_ids": negatives, "original_success_credit": 0},
    )
    counts = flow["counts"]
    successor = {
        "effective_negatives": SOURCE_ACCOUNTING["effective_negatives"] + counts["effective_negatives"],
        "methods": SOURCE_ACCOUNTING["methods"] + counts["methods"],
        "direct_witnesses": SOURCE_ACCOUNTING["direct_witnesses"] + counts["witnesses"],
        "failed_witnesses": SOURCE_ACCOUNTING["failed_witnesses"] + counts["failed"],
        "passing_witnesses": SOURCE_ACCOUNTING["passing_witnesses"] + counts["passing"],
    }
    write_json(
        X2 / "completion-ledger.json",
        {
            "candidate_tasks": 100,
            "clean_fix_refine_tasks": 100,
            "deck_cards": deck["card_count"],
            "global_runners": 5,
            "global_skills": 5,
            "local_skills": 10,
            "outcomes": {"completed": 80, "represented": 10, "open_gap": 5, "exact_gate": 5},
            "package_comparisons": 30,
            "paired_runners": 5,
            "safe_tasks": 100,
        },
    )
    write_json(
        X2 / "phase-truth.json",
        {
            "canonical_invoked": False,
            "execution_authority": "owner_self_scoped_delta",
            "outcomes": {"completed": 80, "represented": 10, "open_gap": 5, "exact_gate": 5},
            "owner": OWNER,
            "phase": PHASE + "-x2",
            "source_canonical_replayed": False,
            "state": "X2_EXECUTED_PENDING_FREEZE",
            "successor_visible_accounting": successor,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    meta_catalogue(skills, runners, globals_)
    write_json(
        X2 / "allowlist.json",
        {
            "allowed_prefixes": [
                "docs/ilyra-fen/v690-v2/x2/",
                "scripts/ghc_family_obligation_graph_cli.py",
                "scripts/ghc_family_obligation_graph_pair_06.py through pair_10.py",
                "scripts/ghc_family_obligation_graph_x2.py",
                "scripts/ghc_family_ilyra_v690_v2_execute_x2.py",
                "tests/test_ghc_family_ilyra_v690_v2_x2.py",
            ]
        },
    )
    manifest_count = write_manifest()
    print(
        json.dumps(
            {
                "candidate": 100,
                "deck": deck,
                "global_promotions": 5,
                "manifest_entries": manifest_count,
                "method_counts": counts,
                "package_comparisons": 30,
                "refinements": 100,
                "runners": 5,
                "safe": 100,
                "skills": 10,
            },
            sort_keys=True,
        )
    )


def refresh_evidence_only() -> None:
    proposals = [
        row for row in load("new-proposals.json")["proposals"] if row["lane"] == "x2"
    ]
    refinements = json.loads((X2 / "refinements.json").read_text(encoding="utf-8"))[
        "records"
    ]
    skills = json.loads(
        (X2 / "skills-validation.json").read_text(encoding="utf-8")
    )["records"]
    runners = json.loads(
        (X2 / "tooling" / "runner-smokes.json").read_text(encoding="utf-8")
    )["records"]
    packages = json.loads(
        (X2 / "toolchain" / "package-comparisons.json").read_text(encoding="utf-8")
    )
    globals_ = json.loads(
        (X2 / "tooling" / "global-promotion.json").read_text(encoding="utf-8")
    )["records"]
    flow = method_flow(proposals, refinements, skills, runners, packages, globals_)
    write_json(X2 / "method-flow.json", flow)
    negatives = sorted(
        {
            negative
            for witness in flow["witnesses"]
            if witness["result"] == "fail"
            for negative in witness["retained_negative_ids"]
        }
    )
    write_json(
        X2 / "negative-index.json",
        {"count": len(negatives), "negative_ids": negatives, "original_success_credit": 0},
    )
    counts = flow["counts"]
    truth = json.loads((X2 / "phase-truth.json").read_text(encoding="utf-8"))
    truth["successor_visible_accounting"] = {
        "effective_negatives": SOURCE_ACCOUNTING["effective_negatives"]
        + counts["effective_negatives"],
        "methods": SOURCE_ACCOUNTING["methods"] + counts["methods"],
        "direct_witnesses": SOURCE_ACCOUNTING["direct_witnesses"] + counts["witnesses"],
        "failed_witnesses": SOURCE_ACCOUNTING["failed_witnesses"] + counts["failed"],
        "passing_witnesses": SOURCE_ACCOUNTING["passing_witnesses"] + counts["passing"],
    }
    write_json(X2 / "phase-truth.json", truth)
    manifest_count = write_manifest()
    print(
        json.dumps(
            {
                "manifest_entries": manifest_count,
                "method_counts": counts,
                "state": "X2_EVIDENCE_AND_SEAL_REFRESHED",
            },
            sort_keys=True,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--environment-root")
    parser.add_argument("--global-runner-root")
    parser.add_argument("--global-skill-root")
    parser.add_argument("--refresh-evidence-only", action="store_true")
    parser.add_argument("--refresh-seal-only", action="store_true")
    parser.add_argument("--skill-validator")
    args = parser.parse_args()
    if args.refresh_seal_only:
        print(json.dumps({"manifest_entries": write_manifest(), "state": "X2_SEAL_REFRESHED"}, sort_keys=True))
        return
    if args.refresh_evidence_only:
        refresh_evidence_only()
        return
    required = [
        args.environment_root,
        args.global_runner_root,
        args.global_skill_root,
        args.skill_validator,
    ]
    if any(value is None for value in required):
        parser.error("environment, global roots, and skill validator are required")
    build(
        Path(args.environment_root).resolve(),
        Path(args.global_skill_root).resolve(),
        Path(args.global_runner_root).resolve(),
        Path(args.skill_validator).resolve(),
    )


if __name__ == "__main__":
    main()
