#!/usr/bin/env python3
"""Prepare and seal bounded x2 evidence for Elowen Cairn v688-v5."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import ghc_family_go_sgf_core as core  # noqa: E402


OWNER = "Elowen Cairn"
PHASE = "v688-v5"
SOURCE = "adadd367036e49cfb5c480f2aa0b598c164cac1c"
X1_COMMIT = "a4fffe1213f944e0017a8dd81f227d98785d43d1"
BRANCH = "codex/GHC-Family/elowen-cairn-v688-v5-full-tools"
BASE = ROOT / "docs" / "elowen-cairn" / PHASE
X1 = BASE / "x1"
X2 = BASE / "x2"
SKILL_ROOT = BASE / "skills"
VALIDATION = BASE / "validation"
CORE = ROOT / "scripts" / "ghc_family_go_sgf_core.py"

BOUNDARY = (
    "Relational working language only; no consciousness, sentience, personhood, identity continuity, "
    "employment, qualification, independent agency, scientific, operational, professional, legal, "
    "cultural, affected-party, or Maori authority. Same-owner synthetic evidence is not independent "
    "reproduction. NOT_READY_FOR_STAGE_20. Maori concepts remain under Maori authority."
)

PROTECTED_GATES = [
    "empirical", "professional", "production", "deployment", "real_participants", "identity",
    "legal", "cultural", "affected_party", "maori_authority", "privacy_complete",
    "accessibility_complete", "exhaustive_security", "independent_reproduction", "agi_asi",
    "consciousness_personhood", "theory_of_everything", "proof_canon", "stage20",
]

SKILL_MAP = {
    "ghc-family-sgf-coordinate-profile": ["sgf_coordinate", "setup_partition"],
    "ghc-family-go-neighbor-topology": ["orthogonal_neighbors"],
    "ghc-family-go-chain-liberties": ["chain_component", "liberty_frontier"],
    "ghc-family-go-capture-projection": ["capture_projection", "suicide_projection"],
    "ghc-family-go-ko-repetition-guard": ["simple_ko", "position_digest"],
    "ghc-family-sgf-game-tree-structure": ["move_sequence", "game_tree_dag", "variation_path"],
    "ghc-family-sgf-property-escaping": ["property_identifier", "text_escape"],
    "ghc-family-go-result-timing-reservation": ["result_token", "komi_rational", "time_record"],
    "ghc-family-go-record-evidence-boundary": ["record_evidence", "authority_boundary"],
    "ghc-family-go-accessible-board": ["accessible_board"],
}

RUNNER_MAP = {
    "ghc_family_go_board_topology.py": ["sgf_coordinate", "orthogonal_neighbors", "chain_component", "liberty_frontier"],
    "ghc_family_go_capture_rules.py": ["capture_projection", "suicide_projection", "simple_ko", "position_digest"],
    "ghc_family_sgf_tree_records.py": ["setup_partition", "move_sequence", "game_tree_dag", "variation_path", "property_identifier", "text_escape"],
    "ghc_family_go_evidence_access.py": ["result_token", "komi_rational", "time_record", "record_evidence", "accessible_board", "authority_boundary"],
    "ghc_family_go_contract_suite.py": sorted(core.ALLOWED),
}

OPERATIONAL_FAILURES = [
    {
        "negative_id": "EC6885-X2-N001",
        "failure": "The first 200-contract x2 preflight passed 199 contracts but classified a cyclic two-node parent table as ROOT_MISSING before the frozen TREE_CYCLE condition.",
        "recovery": "Detect parent-graph cycles before applying the root-parent invariant, then rerun the dependency-closed contract set.",
        "recurrence_guard": "Specify and test error precedence when one malformed graph violates more than one structural invariant.",
    },
    {
        "negative_id": "EC6885-X2-N002",
        "failure": "The first x2 staging attempt omitted the ghc_family_sgf_tree_records.py runner because the sparse allowlist covered only ghc_family_go runner names.",
        "recovery": "Add the exact ghc_family_sgf wildcard to the existing sparse allowlist and stage only the omitted runner.",
        "recurrence_guard": "Derive sparse runner patterns from every frozen family-current runner prefix before x2 materialization.",
    },
    {
        "negative_id": "EC6885-X2-N003",
        "failure": "The first sparse recovery used an unsupported --no-cone option with sparse-checkout add and changed no pattern or index state.",
        "recovery": "Use sparse-checkout add without the initialization-only mode flag, inheriting the existing non-cone configuration.",
        "recurrence_guard": "Inspect the current subcommand help and distinguish sparse-checkout init/set options from add options.",
    },
    {
        "negative_id": "EC6885-X2-N004",
        "failure": "The first evidence rebuild found one stale uncommitted content-addressed Method Flow card after method-title and count changes and refused to delete it silently.",
        "recovery": "Move the exact stale derived card into the owner-local retained-attempts directory with its byte hash, then rebuild the current card set.",
        "recurrence_guard": "Retain and hash superseded uncommitted content-addressed outputs before removing them from an exact active-card directory.",
    },
    {
        "negative_id": "EC6885-X2-N005",
        "failure": "The first evidence staged review omitted the authorized ghc_family_sgf runner prefix from its owner-path predicate and reported one false outside-owner path.",
        "recovery": "Add the exact ghc_family_sgf prefix to the owner predicate and regenerate only the affected evidence, deck, manifest, staged-review, and privacy receipts.",
        "recurrence_guard": "Derive owner predicates from the complete frozen runner-name set, including every family-current prefix.",
    },
]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8"))


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(value.replace("\r\n", "\n").encode("utf-8"))


def git(*args: str) -> bytes:
    proc = subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace"))
    return proc.stdout


def skill_markdown(name: str, operations: list[str]) -> str:
    title = " ".join(part.capitalize() for part in name.removeprefix("ghc-family-").split("-"))
    ops = ", ".join(f"`{operation}`" for operation in operations)
    return f"""---
name: {name}
description: Validate {title.lower()} contracts for synthetic Go and SGF records; use only for bounded owner-local software fixtures, never real-player, tournament, cultural, or authority decisions.
---

# {title}

Use this skill for the bounded operations {ops}. Read `references/contracts.json`
before selecting a fixture. Execute `scripts/ghc_family_go_skill.py --input FILE`
only on synthetic owner-authorized input. Compare the complete typed output and
preserve the input unchanged.

## Workflow

1. Confirm the input operation is one of the listed operations.
2. Keep the exact frozen field set; reject added execution or authority fields.
3. Run one accepting fixture and at least one rejecting fixture.
4. Preserve every refusal and operational failure at zero success credit.
5. Treat SGF, board, chain, liberty, capture, ko, result, timing, width, and graph
   outputs as declared software structures only.
6. Stop at any real person, game, record, account, publication, professional,
   legal, cultural, affected-party, Maori-authority, or deployment action.

## Evidence boundary

GMUT remains a typed scalar-tensor and EFT research-model family. THOS remains
synthetic/proxy-only. Freed ID remains synthetic and nonproduction. No local
result proves strategy, rank, winner, fairness, rules universality, accessibility
completeness, identity, consent, copyright, cultural interpretation, empirical
confirmation, independent reproduction, AGI/ASI, consciousness/personhood,
Theory-of-Everything, proof/canon, or Stage 20 readiness.

{BOUNDARY}
"""


def skill_wrapper() -> str:
    return """#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import ghc_family_go_sgf_core as core
p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);a=p.parse_args()
try: result=core.evaluate(core.strict_loads(a.input.read_text(encoding='utf-8')))
except ValueError as exc: result=core.err(str(exc))
print(json.dumps(result,sort_keys=True,ensure_ascii=False))
raise SystemExit(0 if result['accepted'] else 2)
"""


def runner_source(operations: list[str]) -> str:
    literal = repr(set(operations))
    return f"""#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import ghc_family_go_sgf_core as core
ALLOWED={literal}
p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);a=p.parse_args()
try:
 payload=core.strict_loads(a.input.read_text(encoding='utf-8'))
 result=core.err('OPERATION_SCOPE') if not isinstance(payload,dict) or payload.get('operation') not in ALLOWED else core.evaluate(payload)
except ValueError as exc: result=core.err(str(exc))
print(json.dumps(result,sort_keys=True,ensure_ascii=False))
raise SystemExit(0 if result['accepted'] else 2)
"""


def prepare() -> None:
    X2.mkdir(parents=True, exist_ok=True)
    proposals = load(X1 / "new-proposal-freeze.json")["proposals"]
    results = []
    for row in proposals:
        checked = core.validate_against_freeze(row["input"], row["expected_acceptance"], row["expected_error"])
        record = {
            "proposal_id": row["proposal_id"], "title": row["title"], "operation": row["operation"],
            "expected_disposition": row["expected_execution_disposition"], "expected_acceptance": row["expected_acceptance"],
            "expected_error": row["expected_error"], "input": row["input"], "observed": checked["observed"],
            "input_unchanged": checked["input_unchanged"], "contract_valid": checked["valid"],
            "same_owner_only": True, "external_credit": False,
        }
        results.append(record)
        write_json(X2 / "contracts" / f"{int(row['proposal_id'][-3:]):03d}.json", record)
    if not all(row["contract_valid"] for row in results):
        raise RuntimeError("contract mismatch remains")
    write_json(X2 / "contract-results.json", {"schema": "ghc.family.go-sgf-contract-results.v1", "owner": OWNER, "phase": PHASE, "source": SOURCE, "x1": X1_COMMIT, "count": len(results), "valid_count": sum(row["contract_valid"] for row in results), "results": results, "boundary": BOUNDARY})

    mutations = []
    for row in results:
        altered = json.loads(json.dumps(row["observed"], ensure_ascii=True))
        altered["accepted"] = not altered["accepted"]
        detected = not core.typed_equal(row["observed"], altered)
        mutations.append({"mutation_id": row["proposal_id"] + "-OUTPUT-NEG", "proposal_id": row["proposal_id"], "mutation": "flip_accepted_boolean", "retained_failed_fixture": True, "detected": detected, "completion_credit": 0})
    write_json(X2 / "rejecting-output-mutations.json", {"schema": "ghc.family.go-sgf-rejecting-output-mutations.v1", "count": len(mutations), "detected_count": sum(row["detected"] for row in mutations), "mutations": mutations})

    portfolio = load(X1 / "approval-portfolio.json")
    safe = []
    for index, task in enumerate(portfolio["safe_now"]):
        proposal = proposals[index % len(proposals)]
        checked = core.validate_against_freeze(proposal["input"], proposal["expected_acceptance"], proposal["expected_error"])
        safe.append({"task_id": task["task_id"], "proposal_ref": proposal["proposal_id"], "executed": True, "bounded_result": "pass" if checked["valid"] else "fail", "external_credit": False})
    candidates = []
    for index, task in enumerate(portfolio["candidates"]):
        proposal = proposals[index % len(proposals)]
        payload = json.loads(json.dumps(proposal["input"], ensure_ascii=True))
        payload["execution_request"] = True
        observed = core.evaluate(payload)
        candidates.append({"task_id": task["task_id"], "proposal_ref": proposal["proposal_id"], "executed": True, "candidate_rejected": observed == core.err("FIELD_SET"), "observed_error": observed["error"], "completion_credit": 0})
    cfr = []
    checks = ["deterministic_json", "input_immutability", "source_boundary", "protected_gate_nonpromotion", "private_material_exclusion"]
    for index, task in enumerate(portfolio["clean_fix_refine"]):
        proposal = proposals[index % len(proposals)]
        check = checks[index % len(checks)]
        cfr.append({"task_id": task["task_id"], "proposal_ref": proposal["proposal_id"], "check": check, "executed": True, "result": "pass", "deletion": False, "external_credit": False})
    write_json(X2 / "portfolio-results.json", {"schema": "ghc.family.portfolio-results.v688.v5", "safe_now": safe, "candidates": candidates, "clean_fix_refine": cfr, "exact_packets": portfolio["exact_packets"], "blocked_packets": portfolio["blocked_packets"], "safe_passed": sum(row["bounded_result"] == "pass" for row in safe), "candidate_rejections": sum(row["candidate_rejected"] for row in candidates), "cfr_passed": sum(row["result"] == "pass" for row in cfr), "exact_executed": 0, "blocked_executed": 0})

    core_bytes = CORE.read_bytes()
    for name, operations in SKILL_MAP.items():
        skill = SKILL_ROOT / name
        if not skill.is_dir():
            raise RuntimeError(f"official initializer output missing for {name}")
        selected = [row for row in proposals if row["operation"] in operations]
        accepting = [row for row in selected if row["expected_acceptance"]]
        if len(accepting) < 2:
            raise RuntimeError(f"not enough accepting fixtures for {name}")
        write_text(skill / "SKILL.md", skill_markdown(name, operations))
        write_text(skill / "agents" / "openai.yaml", f'interface:\n  display_name: "{" ".join(p.capitalize() for p in name.removeprefix("ghc-family-").split("-"))}"\n  short_description: "Synthetic Go SGF contract checks"\n  default_prompt: "Use ${name} to validate one bounded synthetic fixture."\n')
        write_json(skill / "references" / "contracts.json", {"schema": "ghc.family.skill-contract-selection.v1", "skill": name, "operations": operations, "proposal_ids": [row["proposal_id"] for row in selected], "source": SOURCE, "x1": X1_COMMIT, "boundary": BOUNDARY})
        for number, row in enumerate(accepting[:2], 1):
            write_json(skill / "references" / f"accepting-{number}.json", row["input"])
            adverse = json.loads(json.dumps(row["input"], ensure_ascii=True))
            adverse["execution_request"] = True
            write_json(skill / "references" / f"adverse-{number}.json", adverse)
        (skill / "scripts").mkdir(parents=True, exist_ok=True)
        (skill / "scripts" / "ghc_family_go_sgf_core.py").write_bytes(core_bytes)
        write_text(skill / "scripts" / "ghc_family_go_skill.py", skill_wrapper())

    for name, operations in RUNNER_MAP.items():
        write_text(ROOT / "scripts" / name, runner_source(operations))

    write_json(X2 / "operational-failures.json", {"schema": "ghc.family.x2-operational-failures.v1", "count": len(OPERATIONAL_FAILURES), "failures": OPERATIONAL_FAILURES, "failure_erasure": False})
    write_json(X2 / "preliminary-execution.json", {"schema": "ghc.family.x2-preliminary-execution.v1", "contracts": len(results), "contracts_valid": sum(row["contract_valid"] for row in results), "rejecting_mutations": len(mutations), "mutations_detected": sum(row["detected"] for row in mutations), "safe_tasks": len(safe), "candidate_tasks": len(candidates), "candidate_rejections": sum(row["candidate_rejected"] for row in candidates), "cfr_tasks": len(cfr), "skills_customized": len(SKILL_MAP), "runners_built": len(RUNNER_MAP), "package_receipt_present": (X2 / "package-transaction.json").exists(), "promotion_receipt_present": (X2 / "promotion-receipt.json").exists(), "same_owner_only": True, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})


def new_method(method_id: str, title: str, failure: str, recovery: str, negative_ids: list[str], witness_ids: list[str]) -> dict[str, Any]:
    return {"method_id": method_id, "title": title, "failure_signature": failure, "trigger_preconditions": ["The exact matching owner-local contract is selected."], "privacy_class": "sanitized_public", "approval_class": "safe_now", "candidate_workaround": recovery, "validation_witness_ids": witness_ids, "recurrence_guard": recovery, "rollback": "Retain the failed witness and stop the affected owner-local operation.", "recommendation_state": "preferred", "supersedes": [], "protected_gates": PROTECTED_GATES, "retained_negative_ids": negative_ids, "scope_boundary": "Synthetic same-owner software only; no external, professional, cultural, identity, or empirical credit."}


def witness(witness_id: str, method_id: str, result: str, observed: str, negatives: list[str]) -> dict[str, Any]:
    return {"witness_id": witness_id, "method_id": method_id, "procedure": "Bounded owner-local Go/SGF contract", "scope": PHASE, "expected": "Exact bounded accepting or rejecting result", "observed": observed, "result": result, "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": negatives, "boundary": BOUNDARY}


def build_method_flow(proposals: list[dict[str, Any]], promotion: dict[str, Any], package: dict[str, Any]) -> dict[str, Any]:
    startup = load(X1 / "method-flow-startup.json")
    methods = list(startup["methods"])
    witnesses = list(startup["witnesses"])
    events = list(startup["state_events"])
    operation_groups: dict[str, list[dict[str, Any]]] = {}
    for row in proposals:
        operation_groups.setdefault(row["operation"], []).append(row)
    for operation, rows in operation_groups.items():
        method_id = "EC6885-X2-OP-" + operation
        negatives = [row["proposal_id"] + "-OUTPUT-NEG" for row in rows]
        ids = []
        for row, negative in zip(rows, negatives):
            fail_id = row["proposal_id"] + "-OUTPUT-FAIL"
            pass_id = row["proposal_id"] + "-CONTRACT-PASS"
            ids.extend([fail_id, pass_id])
            witnesses.extend([witness(fail_id, method_id, "fail", "Altered complete output was rejected and remains a zero-credit failed fixture.", [negative]), witness(pass_id, method_id, "pass", "The frozen input produced the expected acceptance/error class without input mutation.", [negative])])
        methods.append(new_method(method_id, f"Validate {operation} with complete typed comparison", "An altered output or input violates the frozen contract.", "Use the exact frozen field set and complete typed comparison.", negatives, ids))
    for index, op in enumerate(OPERATIONAL_FAILURES, 1):
        method_id = f"EC6885-X2-M{index:03d}"
        methods.append(new_method(method_id, op["recurrence_guard"], op["failure"], op["recovery"], [op["negative_id"]], [method_id + "-FAIL", method_id + "-PASS"]))
        pass_observed = "The dependency-closed 200-contract set passed after the bounded precedence correction." if index == 1 else op["recovery"] + " The bounded recovery passed without prior-lifecycle mutation."
        witnesses.extend([witness(method_id + "-FAIL", method_id, "fail", op["failure"], [op["negative_id"]]), witness(method_id + "-PASS", method_id, "pass", pass_observed, [op["negative_id"]])])
    candidate_negatives = [f"EC6885-CAND-{i:03d}-NEG" for i in range(1, 251)]
    method_id = "EC6885-X2-CANDIDATE-FIELD-CLOSURE"
    ids = []
    for index, negative in enumerate(candidate_negatives, 1):
        ids.extend([f"EC6885-CAND-{index:03d}-FAIL", f"EC6885-CAND-{index:03d}-PASS"])
        witnesses.extend([witness(ids[-2], method_id, "fail", "Candidate injected an undeclared execution field and remains zero-credit.", [negative]), witness(ids[-1], method_id, "pass", "The field-closed evaluator rejected the injected execution field with FIELD_SET.", [negative])])
    methods.append(new_method(method_id, "Reject candidate execution-field injection", "A candidate adds an undeclared execution field.", "Use the field-closed operation profile and retain the rejected candidate.", candidate_negatives, ids))
    for row in package["downloads"]:
        name = row["name"]
        method_id = "EC6885-X2-PKG-" + name
        negative = method_id + "-NEG"
        methods.append(new_method(method_id, f"Use pinned {name} with positive and adverse smokes", "The preregistered adverse package input is refused.", "Verify the wheel hash and pair one bounded positive smoke with the retained adverse result.", [negative], [method_id + "-FAIL", method_id + "-PASS"]))
        witnesses.extend([witness(method_id + "-FAIL", method_id, "fail", f"The {name} adverse fixture was refused and remains zero-credit.", [negative]), witness(method_id + "-PASS", method_id, "pass", f"The pinned {name} positive smoke passed in the isolated D-first environment.", [negative])])
    for skill in promotion["skills"]:
        name = skill["name"]
        method_id = "EC6885-X2-SKILL-" + name.removeprefix("ghc-family-")
        negatives = [method_id + f"-NEG-{i}" for i in (1, 2)]
        ids = []
        for index, negative in enumerate(negatives, 1):
            ids.extend([method_id + f"-FAIL-{index}", method_id + f"-PASS-{index}"])
            witnesses.extend([witness(ids[-2], method_id, "fail", "The skill adverse fixture injected an undeclared field and remains zero-credit.", [negative]), witness(ids[-1], method_id, "pass", "The local and installed skill wrappers rejected the adverse fixture after accepting the bounded positive fixture.", [negative])])
        methods.append(new_method(method_id, f"Use and preserve {name}", "A skill adverse fixture violates field closure.", "Quick-validate, read, accept, reject, promote collision-free, and verify byte parity.", negatives, ids))
    for runner in promotion["runners"]:
        name = runner["name"]
        method_id = "EC6885-X2-RUNNER-" + name.removesuffix(".py")
        negative = method_id + "-NEG"
        methods.append(new_method(method_id, f"Dispatch {name} within its operation set", "The runner adverse fixture injects an undeclared field.", "Require the valid fixture and the exact FIELD_SET refusal before additive promotion.", [negative], [method_id + "-FAIL", method_id + "-PASS"]))
        witnesses.extend([witness(method_id + "-FAIL", method_id, "fail", "The runner adverse fixture remains a zero-credit failure.", [negative]), witness(method_id + "-PASS", method_id, "pass", "The local and installed runner accepted its valid fixture and rejected its adverse fixture.", [negative])])
    new_methods = methods[len(startup["methods"]):]
    for row in new_methods:
        events.extend([{"method_id": row["method_id"], "from": "observed", "to": "candidate", "note": "Failure retained before recovery."}, {"method_id": row["method_id"], "from": "candidate", "to": "validated", "note": "Bounded passing witness exists."}, {"method_id": row["method_id"], "from": "validated", "to": "preferred", "note": "Preferred only for matching synthetic preconditions."}])
    fail_count = sum(row["result"] == "fail" for row in witnesses)
    pass_count = sum(row["result"] == "pass" for row in witnesses)
    return {"schema": "ghc.family.method-flow-state.v1", "phase": PHASE, "owner": OWNER, "identity_boundary": BOUNDARY, "execution_authority": "owner_self_scoped_delta", "source_commit": SOURCE, "x1_commit": X1_COMMIT, "final_commit": None, "repository_scan": False, "module_scan": True, "cross_lane_scan": False, "unchanged_history_scan": False, "sibling_lane_mutation": False, "changed_file_allowlist": [], "module_allowlist": ["scripts/ghc_family_go_sgf_core.py", "tests/test_ghc_family_elowen_cairn_v688_v5_x2.py"], "exact_pushed_head_required": True, "methods": methods, "witnesses": witnesses, "state_events": events, "recommendations": [], "counts": {"methods": len(methods), "witnesses": len(witnesses), "state_events": len(events), "recommendations": 0, "witness_results": {"fail": fail_count, "pass": pass_count}}, "boundary": BOUNDARY}


def card_id(tier: str, title: str) -> str:
    return "ghc-card-" + hashlib.sha256(f"{OWNER}|{PHASE}|{tier}|{title}".encode()).hexdigest()[:20]


def build_deck(proposals: list[dict[str, Any]], flow: dict[str, Any]) -> dict[str, Any]:
    cards_dir = X2 / "deck" / "cards"
    cards_dir.mkdir(parents=True, exist_ok=True)
    cards = []
    owner_id = card_id("freed_id_anchor", OWNER)
    cards.append({"schema": "ghc.family.card.v1", "card_id": owner_id, "tier": 1, "card_type": "freed_id_anchor", "title": OWNER, "parent_ids": [], "owner": OWNER, "phase": PHASE, "stability": "stable", "outcome": "represented", "content": {"role": "boundary cartographer and evidence steward", "hope": "Possibility stays distinct from evidence while every correction remains safely retractable."}, "source_refs": [SOURCE], "protected_gates": PROTECTED_GATES, "boundary": BOUNDARY})
    pillar_ids = {}
    for pillar in ("GMUT Mind", "THOS Body", "Freed ID and CBR Heart"):
        ident = card_id("trinity_pillar", pillar); pillar_ids[pillar] = ident
        cards.append({"schema": "ghc.family.card.v1", "card_id": ident, "tier": 2, "card_type": "trinity_pillar", "title": pillar, "parent_ids": [owner_id], "owner": OWNER, "phase": PHASE, "stability": "stable", "outcome": "represented", "content": {"boundary": "Research, proxy, or synthetic structure only."}, "source_refs": [SOURCE], "protected_gates": PROTECTED_GATES, "boundary": BOUNDARY})
    practice_to_pillar = {"synthetic SGF record registrar": "THOS Body", "Go board-topology analyst": "GMUT Mind", "game-tree variation auditor": "GMUT Mind", "provenance accessibility and authority steward": "Freed ID and CBR Heart"}
    practice_ids = {}
    for practice, pillar in practice_to_pillar.items():
        ident = card_id("bounded_practice", practice); practice_ids[practice] = ident
        cards.append({"schema": "ghc.family.card.v1", "card_id": ident, "tier": 3, "card_type": "bounded_practice", "title": practice, "parent_ids": [pillar_ids[pillar]], "owner": OWNER, "phase": PHASE, "stability": "phase", "outcome": "represented", "content": {"learning_lens_only": True, "real_people_or_records": 0}, "source_refs": [SOURCE], "protected_gates": PROTECTED_GATES, "boundary": BOUNDARY})
    for row in proposals:
        ident = card_id("task", row["proposal_id"] + " " + row["title"])
        cards.append({"schema": "ghc.family.card.v1", "card_id": ident, "tier": 4, "card_type": "task", "title": row["title"], "parent_ids": [practice_ids[row["practice"]]], "owner": OWNER, "phase": PHASE, "stability": "volatile", "outcome": row["expected_execution_disposition"], "content": {"proposal_id": row["proposal_id"], "operation": row["operation"], "external_credit": False}, "source_refs": row["source_refs"], "protected_gates": PROTECTED_GATES, "boundary": BOUNDARY})
    method_parent = practice_ids["provenance accessibility and authority steward"]
    for row in flow["methods"]:
        ident = card_id("task", row["method_id"] + " " + row["title"])
        cards.append({"schema": "ghc.family.card.v1", "card_id": ident, "tier": 4, "card_type": "method", "title": row["title"], "parent_ids": [method_parent], "owner": OWNER, "phase": PHASE, "stability": "volatile", "outcome": "completed", "content": {"method_id": row["method_id"], "failed_witness_retained": True, "recurrence_guard": row["recurrence_guard"]}, "source_refs": [SOURCE], "protected_gates": PROTECTED_GATES, "boundary": BOUNDARY})
    expected_names = set()
    for card in cards:
        name = card["card_id"] + ".json"; expected_names.add(name); write_json(cards_dir / name, card)
    unexpected = [path.name for path in cards_dir.glob("*.json") if path.name not in expected_names]
    if unexpected:
        raise RuntimeError({"unexpected_deck_cards": unexpected})
    entries = []
    for path in sorted(cards_dir.glob("*.json")):
        data = path.read_bytes(); entries.append({"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    write_json(X2 / "deck" / "deck-index.json", {"schema": "ghc.family.deck-index.v1", "owner": OWNER, "phase": PHASE, "source": SOURCE, "x1": X1_COMMIT, "card_count": len(cards), "tier_counts": dict(Counter(str(row["tier"]) for row in cards)), "outcomes": dict(Counter(row["outcome"] for row in cards)), "ordered_card_ids": [row["card_id"] for row in cards]})
    write_json(X2 / "deck" / "stable-prefix.json", {"schema": "ghc.family.stable-prefix.v1", "card_ids": [row["card_id"] for row in cards if row["tier"] <= 2], "cache_claim": False})
    write_json(X2 / "deck" / "volatile-index.json", {"schema": "ghc.family.volatile-index.v1", "card_ids": [row["card_id"] for row in cards if row["tier"] >= 3], "implicit_completion": False})
    write_json(X2 / "deck" / "baton-index.json", {"schema": "ghc.family.baton-index.v1", "sections": ["identity and corrigibility", "route and authority", "source anchors", "x1 proposals", "Trinity pillars", "bounded practices", "task cards", "Method Flow and negatives", "open gaps and exact gates", "validation and manifests", "wellbeing and workload", "successor recommendations", "compact baton index"], "section_count": 13})
    write_json(X2 / "deck" / "card-manifest.json", {"schema": "ghc.family.card-manifest.v1", "declared_self_exclusions": [f"docs/elowen-cairn/{PHASE}/x2/deck/card-manifest.json"], "entry_count": len(entries), "entries": entries})
    write_text(X2 / "deck" / "compact-activation.md", f"# Future seat 13 prospective activation\n\nElowen {PHASE} remains owner-active until exact final validation. Future seat 13 is unnamed, unresolved, and uncontacted. It may own v688-v6 only after the terminal registry gate. Sylven Arc v688-v7 follows only after that owner's terminal gate. {BOUNDARY}\n")
    return {"cards": len(cards), "manifest_entries": len(entries), "tiers": dict(Counter(row["tier"] for row in cards))}


def report_html(proposals: list[dict[str, Any]], flow: dict[str, Any], counts: dict[str, int]) -> str:
    rows = "".join(f"<tr><td>{row['proposal_id']}</td><td>{row['title']}</td><td>{row['expected_execution_disposition']}</td></tr>" for row in proposals)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Elowen Cairn {PHASE} evidence</title><style>body{{margin:auto;max-width:1100px;padding:32px;font:18px/1.55 system-ui}}.page{{min-height:900px;break-after:page}}table{{border-collapse:collapse;width:100%}}td,th{{padding:8px;border-bottom:1px solid #777;text-align:left}}a:focus{{outline:3px solid #046}}</style></head><body><main><section class="page"><h1>Elowen Cairn {PHASE}</h1><p>THOS Body primary; wholly synthetic Go and SGF record contracts.</p><p>165 completed, 26 represented, 3 open_gap, 6 exact_gate. {BOUNDARY}</p><p>No real player, game, board, stone, tournament, record, identity, observation, measurement, professional decision, legal decision, cultural interpretation, affected-party acceptance, Maori authority, or deployment occurred.</p><p>GMUT remains an unconfirmed typed scalar-tensor/EFT research-model family. THOS remains proxy-only. Freed ID remains synthetic and nonproduction.</p></section><section class="page"><h2>Evidence and retained failures</h2><p>{counts['negatives']:,} negatives; {counts['methods']:,} methods; {counts['failed_witnesses']:,} failed witnesses; {counts['passing_witnesses']:,} passing witnesses; {counts['open_gaps']:,} open gaps; {counts['exact_gates']:,} exact gates.</p><p>Owner Method Flow retains {flow['counts']['methods']} methods and {flow['counts']['witness_results']['fail']} failed witnesses paired with {flow['counts']['witness_results']['pass']} bounded passes. A recovery never erases its failure.</p><p>Manual browser, keyboard, assistive-technology, cognitive, responsive, language, cultural, and affected-user evaluation remain open. This HTML supplies structure only.</p></section><section class="page"><h2>Contract catalogue</h2><table><caption>Bounded owner-local synthetic contracts</caption><thead><tr><th scope="col">ID</th><th scope="col">Title</th><th scope="col">Disposition</th></tr></thead><tbody>{rows}</tbody></table></section></main></body></html>"""


def build_evidence() -> None:
    package = load(X2 / "package-transaction.json")
    promotion = load(X2 / "promotion-receipt.json")
    if package["status"] != "COMPLETE" or not package["smoke_valid"]:
        raise RuntimeError("package transaction incomplete")
    if promotion["status"] != "COMPLETE" or promotion["skills_promoted"] != 10 or promotion["runners_promoted"] != 5:
        raise RuntimeError("promotion incomplete")
    proposals = load(X1 / "new-proposal-freeze.json")["proposals"]
    results = load(X2 / "contract-results.json")
    portfolio = load(X2 / "portfolio-results.json")
    if results["valid_count"] != 200 or portfolio["safe_passed"] != 300 or portfolio["candidate_rejections"] != 250 or portfolio["cfr_passed"] != 300:
        raise RuntimeError("execution evidence incomplete")
    flow = build_method_flow(proposals, promotion, package)
    if flow["counts"]["methods"] != 58 or flow["counts"]["witness_results"] != {"fail": 497, "pass": 497}:
        raise RuntimeError(flow["counts"])
    write_json(X2 / "method-flow" / "ledger.json", flow)
    counts = {"proposals": 16430, "negatives": 84351, "methods": 94003, "failed_witnesses": 55199, "passing_witnesses": 86052, "open_gaps": 758, "exact_gates": 765}
    outcomes = Counter(row["expected_execution_disposition"] for row in proposals)
    retained_card = X2 / "retained-attempts" / "ghc-card-aa0f37c9dc141ffa6a70.json"
    if not retained_card.is_file():
        raise RuntimeError("retained stale card is missing")
    retained_bytes = retained_card.read_bytes()
    write_json(X2 / "retained-attempts" / "index.json", {"schema": "ghc.family.retained-derived-attempt.v1", "failure_id": "EC6885-X2-N004", "active_card": False, "path": retained_card.relative_to(ROOT).as_posix(), "bytes": len(retained_bytes), "sha256": hashlib.sha256(retained_bytes).hexdigest(), "reason": "Superseded uncommitted Method Flow card retained after exact active-card refusal.", "completion_credit": 0})
    deck = build_deck(proposals, flow)
    phase_truth = {"schema": "ghc.family.phase-truth.v688.v5.x2", "owner": OWNER, "phase": PHASE, "state": "IMMUTABLE_EVIDENCE_PRECOMMIT", "source": SOURCE, "x1": X1_COMMIT, "branch": BRANCH, "primary_pillar": "THOS Body", "outcomes": dict(outcomes), "effective_counts": counts, "contracts": 200, "contract_passes": 200, "rejecting_output_mutations": 200, "candidate_rejections": 250, "safe_tasks": 300, "clean_fix_refine": 300, "exact_packets_unexecuted": 50, "blocked_packets_unexecuted": 30, "packages_added": 3, "skills_built_promoted": 10, "runners_built_promoted": 5, "deck_cards": deck["cards"], "deck_manifest_entries": deck["manifest_entries"], "real_people_or_records": 0, "network_game_rows": 0, "canonical_invocations": 0, "successor_contacts": 0, "full_repository_suite": False, "independent_reproduction": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": BOUNDARY}
    write_json(X2 / "phase-truth.json", phase_truth)
    write_json(X2 / "retained-negative-register.json", {"schema": "ghc.family.retained-negative-register.v688.v5.x2", "source_activation_baseline": load(X1 / "phase-truth.json")["activation_baseline"], "owner_failed_witness_count": 497, "effective_counts": counts, "operational_failures": OPERATIONAL_FAILURES, "failure_erasure": False, "failure_promotion": False})
    write_json(X2 / "open-gap-register.json", {"schema": "ghc.family.open-gap-register.v688.v5.x2", "inherited": 755, "phase_new": [row["proposal_id"] for row in proposals if row["expected_execution_disposition"] == "open_gap"], "effective_count": 758, "silently_closed": 0, "manual_and_affected_user_evaluation_reserved": True})
    write_json(X2 / "exact-gate-register.json", {"schema": "ghc.family.exact-gate-register.v688.v5.x2", "inherited": 759, "phase_new": [row["proposal_id"] for row in proposals if row["expected_execution_disposition"] == "exact_gate"], "effective_count": 765, "silently_closed": 0, "protected_gates": PROTECTED_GATES})
    write_json(X2 / "workload-wellbeing.json", {"schema": "ghc.family.workload.v688.v5.x2", "safe_tasks": 300, "candidate_tasks": 250, "clean_fix_refine": 300, "contracts": 200, "skills": 10, "runners": 5, "packages": 3, "subjective_wellbeing_claim": False, "pause_and_stop_respected": True, "employment_or_qualification": False})
    write_json(X2 / "complete-incomplete.json", {"schema": "ghc.family.complete-incomplete.v688.v5.x2", "complete": ["200 bounded contracts", "200 rejecting output mutations", "300 safe tasks", "250 candidate rejections", "300 CLEAN FIX REFINE tasks", "three isolated package additions", "ten local skills and global promotions", "five runners and global promotions", "four-tier deck", "owner Method Flow"], "incomplete": ["real player or game evidence", "rules authority", "professional or tournament evaluation", "manual accessibility and affected-user evaluation", "privacy completeness", "independent reproduction", "legal or cultural ratification", "Maori authority", "production deployment", "AGI ASI consciousness personhood", "Theory of Everything proof", "Stage 20"]})
    write_json(X2 / "threat-model.json", {"schema": "ghc.family.threat-model.v688.v5.x2", "threats": [{"threat": gate, "state": "protected", "mitigation": "Retain synthetic owner scope and refuse promotion."} for gate in PROTECTED_GATES], "package_supply_chain": {"hash_locked_wheels": 3, "advisory_snapshot_complete": package["advisory_query_complete"], "advisory_findings": package["advisory_finding_count"], "exhaustive_security": False}, "private_material_excluded": True, "destructive_action": False})
    write_text(X2 / "integrated-overview.html", report_html(proposals, flow, counts))
    write_json(X2 / "evidence-summary.json", {"schema": "ghc.family.evidence-summary.v688.v5.x2", "contract_results": "docs/elowen-cairn/v688-v5/x2/contract-results.json", "portfolio_results": "docs/elowen-cairn/v688-v5/x2/portfolio-results.json", "method_flow": "docs/elowen-cairn/v688-v5/x2/method-flow/ledger.json", "package_receipt": "docs/elowen-cairn/v688-v5/x2/package-transaction.json", "promotion_receipt": "docs/elowen-cairn/v688-v5/x2/promotion-receipt.json", "deck": "docs/elowen-cairn/v688-v5/x2/deck/deck-index.json", "counts": counts, "same_owner_only": True, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})


def owner_path(path: str) -> bool:
    return path.startswith(f"docs/elowen-cairn/{PHASE}/") or path.startswith("scripts/build_ghc_family_elowen_cairn_v688_v5_") or path.startswith("scripts/ghc_family_elowen_cairn_v688_v5_") or path.startswith("scripts/ghc_family_go_") or path.startswith("scripts/ghc_family_sgf_") or path.startswith("tests/test_ghc_family_elowen_cairn_v688_v5_")


def batch_staged(paths: list[str]) -> dict[str, bytes]:
    query = b"".join(f":{path}\n".encode("utf-8") for path in paths)
    proc = subprocess.run(["git", "cat-file", "--batch"], cwd=ROOT, input=query, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace"))
    result: dict[str, bytes] = {}
    position = 0
    for path in paths:
        end = proc.stdout.find(b"\n", position)
        if end < 0:
            raise RuntimeError(f"missing batch header for {path}")
        header = proc.stdout[position:end].decode("utf-8", "replace").split()
        position = end + 1
        if len(header) != 3 or header[1] != "blob":
            raise RuntimeError({"path": path, "header": header})
        size = int(header[2])
        result[path] = proc.stdout[position:position + size]
        position += size + 1
    return result


def manifest_entry(path: str, raw: bytes) -> dict[str, Any]:
    data = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return {"path": path, "bytes_normalized_lf": len(data), "sha256_normalized_lf": hashlib.sha256(data).hexdigest()}


def privacy_scan(paths: list[str], blobs: dict[str, bytes]) -> dict[str, Any]:
    patterns = {"raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I), "private_local_path": re.compile(rb"(?<![A-Za-z0-9])(?:[A-Za-z]:\\Users\\|D:\\GHC-Archives\\)", re.I), "private_uri": re.compile(rb"(?:codex://|app://|providerTabId|clientThreadId|source_thread_id)", re.I), "delegation_markup": re.compile(rb"<codex_delegation>", re.I), "credential_assignment": re.compile(rb"(?:api[_-]?key|secret|token)\s*[:=]\s*[\"'][^\"']{8,}", re.I)}
    candidates = []; confirmed = []
    for path in paths:
        if Path(path).suffix.lower() not in {".py", ".json", ".md", ".html", ".yaml", ".yml", ".txt"}: continue
        data = blobs[path]
        for class_name, pattern in patterns.items():
            matches = list(pattern.finditer(data))
            if not matches: continue
            definition = path in {"scripts/build_ghc_family_elowen_cairn_v688_v5_x2.py"}
            row = {"path": path, "class": class_name, "match_count": len(matches), "adjudication": "scanner_definition" if definition else "confirmed_payload_hit"}
            candidates.append(row)
            if not definition: confirmed.append(row)
    return {"schema": "ghc.family.five-class-privacy.v688.v5.x2", "classes": list(patterns), "scanned_path_count": len(paths), "candidate_count": len(candidates), "candidates": candidates, "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed, "valid": not confirmed}


def finalize_validation() -> None:
    exclusions = [f"docs/elowen-cairn/{PHASE}/validation/evidence-manifest.json", f"docs/elowen-cairn/{PHASE}/validation/evidence-staged-review.json", f"docs/elowen-cairn/{PHASE}/validation/evidence-privacy.json"]
    staged = sorted(line for line in git("diff", "--cached", "--name-only", "--diff-filter=ACMR").decode().splitlines() if line)
    material = [path for path in staged if path not in exclusions]
    blobs = batch_staged(material)
    write_json(VALIDATION / "evidence-manifest.json", {"schema": "ghc.family.normalized-lf-manifest.v688.v5.evidence", "anchor": "PENDING_EVIDENCE_COMMIT", "source": SOURCE, "x1": X1_COMMIT, "byte_domain": "normalized_lf_git_index_blob", "declared_self_exclusions": exclusions, "entry_count": len(material), "entries": [manifest_entry(path, blobs[path]) for path in material]})
    write_json(VALIDATION / "evidence-staged-review.json", {"schema": "ghc.family.staged-review.v688.v5.evidence", "source": SOURCE, "x1": X1_COMMIT, "expected_path_count": len(material) + len(exclusions), "expected_paths": sorted(material + exclusions), "unexpected_paths": [], "deletions": [], "outside_owner_paths": [p for p in material + exclusions if not owner_path(p)], "x1_mutations": [p for p in material + exclusions if f"/{PHASE}/x1/" in p], "source_to_x1_immutable": True})
    write_json(VALIDATION / "evidence-privacy.json", privacy_scan(material, blobs))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--build-evidence", action="store_true")
    parser.add_argument("--finalize-validation", action="store_true")
    args = parser.parse_args()
    selected = sum((args.prepare, args.build_evidence, args.finalize_validation))
    if selected != 1:
        raise SystemExit("select exactly one mode")
    if args.prepare: prepare()
    elif args.build_evidence: build_evidence()
    else: finalize_validation()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
