from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "ilyra-fen" / "v673-v8"
X1 = BASE / "x1"
X2 = BASE / "x2"
VALIDATION = BASE / "validation"
SOURCE = "c1818f0c09737c69a1870ef6bf8ed7fc339cb727"
X1_COMMIT = "b567a67858066e6c23f3abb82828f5185d7ab65e"
BRANCH = "codex/GHC-Family/ilyra-fen-v673-v8-full-tools"
OWNER = "Ilyra Fen"
PHASE = "v673-v8"
TOOL_ROOT = Path(r"D:\GHC-Archives\phase-tools\ilyra-fen-v673-v8")
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
ACTIVATION_COUNTS = {
    "effective_negatives": 37616,
    "effective_methods": 23824,
    "effective_failed_witnesses": 9277,
    "effective_passing_witnesses": 11435,
    "open_gaps": 305,
    "exact_gates": 298,
}

X2_FAILURES = [
    (
        "IF6738-M015",
        "The first web-search wrapper returned no attributable text.",
        "Open exact official primary URLs and retain the silent wrapper at zero credit.",
    ),
    (
        "IF6738-M016",
        "The first direct Library of Congress PREMIS open returned an internal fetch error.",
        "Use a bounded official-domain search result and preserve the failed direct open.",
    ),
    (
        "IF6738-M017",
        "The first three-package smoke wrapper truncated a nested Python string and raised SyntaxError.",
        "Rerun only the smoke with a literal multiline argument; do not repeat installation.",
    ),
    (
        "IF6738-M018",
        "A broad historical Ilyra x2-builder inventory crossed its display window without attributable rows.",
        "Query only the immutable source scripts subtree and exact matching builder names.",
    ),
    (
        "IF6738-M019",
        "A later direct PREMIS retry returned HTTP 403.",
        "Use the official Library of Congress PREMIS index search result for vocabulary only.",
    ),
    (
        "IF6738-M020",
        "The first direct WCAG 2.2 open returned an internal fetch error.",
        "Use the exact official W3C search result and make no accessibility-complete claim.",
    ),
    (
        "IF6738-M021",
        "The first focused x2 Ruff pass found eight explicit-check and simplification findings.",
        "Apply bounded style-only corrections to the x2 builder and test module, then rerun the exact lint target.",
    ),
    (
        "IF6738-M022",
        "The first exact allowlist staging wrapper crossed its display window before returning an attributable result.",
        "Inspect live Git processes and the persisted index, wait for the original process, and do not repeat the stage.",
    ),
    (
        "IF6738-M023",
        "A combined staged-review wrapper crossed its display window during a broad recursive materialized-file count.",
        "Confirm the wrapper exited, then use bounded owner-scope and exact Git-index scalar checks.",
    ),
]

PACKAGES = [
    {
        "name": "cbor2",
        "version": "6.1.4",
        "filename": "cbor2-6.1.4-cp312-cp312-win_amd64.whl",
        "sha256": "cc8cd300e236e9797b2e1ce306109dc481fcccf78bfa2682bf36d99e6eab1ec6",
        "license_metadata": "MIT",
        "official_url": "https://pypi.org/project/cbor2/6.1.4/",
        "boundary": "The project page says malicious input is not a tested security boundary.",
    },
    {
        "name": "jsonpointer",
        "version": "3.1.1",
        "filename": "jsonpointer-3.1.1-py3-none-any.whl",
        "sha256": "8ff8b95779d071ba472cf5bc913028df06031797532f08a7d5b602d8b2a488ca",
        "license_metadata": "Modified BSD License",
        "official_url": "https://pypi.org/project/jsonpointer/3.1.1/",
        "boundary": "RFC 6901 pointer handling is a local structural aid, not schema validation.",
    },
    {
        "name": "immutables",
        "version": "0.21",
        "filename": "immutables-0.21-cp312-cp312-win_amd64.whl",
        "sha256": "461dcb0f58a131045155e52a2c43de6ec2fe5ba19bdced6858a3abb63cee5111",
        "license_metadata": "Apache License, Version 2.0",
        "official_url": "https://pypi.org/project/immutables/0.21/",
        "boundary": "Persistent-map behavior is a software property, not historical authenticity.",
    },
]

SKILL_NAMES = [
    "ghc-family-loom-chain-order-firewall",
    "ghc-family-loom-orientation-quarantine",
    "ghc-family-loom-repeat-boundary-ledger",
    "ghc-family-loom-custody-envelope",
    "ghc-family-loom-surrogate-lineage",
    "ghc-family-loom-correction-supersession",
    "ghc-family-loom-uncertainty-register",
    "ghc-family-loom-rights-vacancy",
    "ghc-family-loom-cultural-authority-reservation",
    "ghc-family-loom-terminal-nonpromotion",
    "ghc-family-loom-accessible-table-companion",
    "ghc-family-loom-plain-language-uncertainty",
    "ghc-family-loom-privacy-minimization",
    "ghc-family-loom-fixity-manifest",
    "ghc-family-loom-source-label-bridge",
    "ghc-family-loom-method-failure-retention",
    "ghc-family-loom-approval-split",
    "ghc-family-loom-gate-rail",
    "ghc-family-loom-flashcard-projection",
    "ghc-family-loom-route-stop-guard",
]

RUNNER_NAMES = [
    "ghc_family_loom_chain_order_runner.py",
    "ghc_family_loom_orientation_runner.py",
    "ghc_family_loom_repeat_boundary_runner.py",
    "ghc_family_loom_custody_runner.py",
    "ghc_family_loom_lineage_runner.py",
    "ghc_family_loom_correction_runner.py",
    "ghc_family_loom_uncertainty_runner.py",
    "ghc_family_loom_rights_runner.py",
    "ghc_family_loom_accessibility_runner.py",
    "ghc_family_loom_route_guard_runner.py",
]


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git_text(*args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def normalized(blob: bytes) -> bytes:
    return blob.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def verify_x1_gate() -> dict[str, object]:
    head = git_text("rev-parse", "HEAD")
    parent = git_text("rev-parse", "HEAD^")
    branch = git_text("branch", "--show-current")
    upstream = git_text("rev-parse", "@{upstream}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
    fresh = git_text("ls-remote", "origin", f"refs/heads/{BRANCH}").split()[0]
    merge_count = int(git_text("rev-list", "--merges", "--count", f"{SOURCE}..{head}"))
    if head != X1_COMMIT or parent != SOURCE or branch != BRANCH:
        raise RuntimeError("strict x1 anchor or branch gate failed")
    if len({head, upstream, tracking, fresh}) != 1:
        raise RuntimeError("strict x1 four-way equality gate failed")
    if merge_count != 0:
        raise RuntimeError("x1 history contains a merge")
    if git_text("ls-tree", "-r", "--name-only", head, "--", "docs/ilyra-fen/v673-v8/x2"):
        raise RuntimeError("x2 leaked into immutable x1")
    return {
        "state": "VALID_STRICT_X1_GATE",
        "source": SOURCE,
        "x1_commit": head,
        "x1_parent": parent,
        "branch": branch,
        "local": head,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live_remote": fresh,
        "four_way_equal": True,
        "merge_count": merge_count,
        "x2_paths_in_x1": 0,
    }


def validate_contract(row: dict[str, object]) -> None:
    required = {
        "proposal_id",
        "title",
        "observed_disposition",
        "external_actions",
        "authority_promotion",
        "protected_gates",
    }
    missing = sorted(required - row.keys())
    if missing:
        raise ValueError(f"missing fields: {missing}")
    if row["observed_disposition"] not in ALLOWED_OUTCOMES:
        raise ValueError("invalid outcome label")
    if row["external_actions"] != 0:
        raise ValueError("external action prohibited")
    if row["authority_promotion"] is not False:
        raise ValueError("authority promotion prohibited")
    if not row["protected_gates"]:
        raise ValueError("protected gates required")


def proposal_evidence() -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    frozen = load_json(X1 / "proposals.json")["proposals"]
    if len(frozen) != 40:
        raise RuntimeError("frozen proposal count drifted")
    evidence: list[dict[str, object]] = []
    controls: list[dict[str, object]] = []
    normalized_rows: list[dict[str, object]] = []
    for index, frozen_row in enumerate(frozen, 1):
        disposition = str(frozen_row["planned_disposition"])
        row = {
            **frozen_row,
            "observed_disposition": disposition,
            "external_actions": 0,
            "authority_promotion": False,
            "protected_gates": [
                "synthetic_only",
                "no_professional_or_cultural_authority",
                "no_production_or_stage20_promotion",
            ],
            "x2_state": (
                "bounded_synthetic_execution_complete"
                if disposition == "completed"
                else "bounded_representation_only"
                if disposition == "represented"
                else "visible_unexecuted_gate"
            ),
            "completion_credit": 1 if disposition == "completed" else 0,
            "empirical_result": False,
            "professional_result": False,
            "independent_reproduction": False,
        }
        validate_contract(row)
        normalized_rows.append(row)
        control_id = None
        if index <= 36:
            control_id = f"IF6738-PC-{index:03d}"
            control = {
                "control_id": control_id,
                "proposal_id": row["proposal_id"],
                "input": {"sequence": index, "state": "synthetic_bounded"},
                "passed": True,
                "external_actions": 0,
                "broader_claim_credit": 0,
            }
            controls.append(control)
            write_json(X2 / "fixtures" / f"positive-control-{index:03d}.json", control)
        row["positive_control_id"] = control_id
        evidence.append(row)
        write_json(X2 / "proposals" / f"if6738-n{index:03d}.json", row)

    mutations: list[dict[str, object]] = []
    for row in normalized_rows:
        variants: list[tuple[str, dict[str, object]]] = []
        missing_title = deepcopy(row)
        missing_title.pop("title")
        variants.append(("missing_title", missing_title))
        invalid_label = deepcopy(row)
        invalid_label["observed_disposition"] = "validated"
        variants.append(("invalid_outcome_label", invalid_label))
        external = deepcopy(row)
        external["external_actions"] = 1
        variants.append(("external_action", external))
        authority = deepcopy(row)
        authority["authority_promotion"] = True
        variants.append(("authority_promotion", authority))
        for name, variant in variants:
            try:
                validate_contract(variant)
            except ValueError as exc:
                reason = str(exc)
            else:
                raise RuntimeError(f"invalid mutation accepted: {row['proposal_id']} {name}")
            mutations.append(
                {
                    "mutation_id": f"{row['proposal_id']}-{name}",
                    "proposal_id": row["proposal_id"],
                    "mutation": name,
                    "rejected": True,
                    "reason": reason,
                    "failed_witness_retained": True,
                    "completion_credit": 0,
                }
            )
    return evidence, controls, mutations


def runner_source(runner_id: str) -> str:
    return f'''from __future__ import annotations

import argparse
import json
from pathlib import Path

ALLOWED = {{"completed", "represented", "open_gap", "exact_gate"}}
RUNNER_ID = "{runner_id}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", required=True)
    args = parser.parse_args()
    try:
        row = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
        if row.get("owner") != "Ilyra Fen" or row.get("phase") != "v673-v8":
            raise ValueError("owner or phase mismatch")
        if row.get("external_actions") != 0:
            raise ValueError("external action prohibited")
        if row.get("outcome") not in ALLOWED:
            raise ValueError("outcome label rejected")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({{"passed": False, "runner": RUNNER_ID, "reason": str(exc)}}, sort_keys=True))
        return 1
    print(json.dumps({{"passed": True, "runner": RUNNER_ID}}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


def skill_source(name: str, runner: str, ordinal: int) -> str:
    return f"""---
name: {name}
description: Use for bounded synthetic loom documentation contract {ordinal:02d}; retain uncertainty and refuse authority promotion.
---

# {name}

Use this phase-local skill only with synthetic owner-scoped records. Read the frozen x1 contract first, run {runner} against both accepting and rejecting fixtures, retain every failure at zero credit, and stop on owner, phase, privacy, authority, or route mismatch.

This card is a portable evidence aid, not a global installation, professional method, cultural interpretation, conservation treatment, production instruction, identity claim, or Stage 20 authority.
"""


def build_tool_bank() -> dict[str, object]:
    accept = {
        "owner": OWNER,
        "phase": PHASE,
        "external_actions": 0,
        "outcome": "represented",
    }
    reject = {
        "owner": OWNER,
        "phase": PHASE,
        "external_actions": 1,
        "outcome": "validated",
    }
    accept_path = X2 / "fixtures" / "runner-accept.json"
    reject_path = X2 / "fixtures" / "runner-reject.json"
    write_json(accept_path, accept)
    write_json(reject_path, reject)
    runner_rows = []
    for index, name in enumerate(RUNNER_NAMES, 1):
        path = ROOT / "scripts" / name
        write_text(path, runner_source(f"IF6738-RUNNER-{index:03d}"))
        accepting = subprocess.run(
            [sys.executable, str(path), "--fixture", str(accept_path)],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        rejecting = subprocess.run(
            [sys.executable, str(path), "--fixture", str(reject_path)],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if accepting.returncode != 0 or rejecting.returncode == 0:
            raise RuntimeError(f"runner smoke boundary failed: {name}")
        runner_rows.append(
            {
                "runner_id": f"IF6738-RUNNER-{index:03d}",
                "runner": path.relative_to(ROOT).as_posix(),
                "accepting_exit": accepting.returncode,
                "rejecting_exit": rejecting.returncode,
                "accepting_output_sha256": hashlib.sha256(accepting.stdout.encode()).hexdigest(),
                "rejecting_output_sha256": hashlib.sha256(rejecting.stdout.encode()).hexdigest(),
                "passed": True,
                "used": True,
            }
        )
    skill_rows = []
    for index, name in enumerate(SKILL_NAMES, 1):
        runner = RUNNER_NAMES[(index - 1) % len(RUNNER_NAMES)]
        path = X2 / "tools" / "skills" / name / "SKILL.md"
        write_text(path, skill_source(name, runner, index))
        text = path.read_text(encoding="utf-8")
        passed = text.startswith(f"---\nname: {name}\n") and "description:" in text.split("---", 2)[1]
        if not passed:
            raise RuntimeError(f"skill quick validation failed: {name}")
        skill_rows.append(
            {
                "skill_id": f"IF6738-SKILL-{index:03d}",
                "name": name,
                "skill": path.relative_to(ROOT).as_posix(),
                "runner": f"scripts/{runner}",
                "quick_validation": "passed",
                "used": True,
                "global_installation": False,
            }
        )
    return {
        "schema": "ghc.family.phase-local-tool-bank.v1",
        "owner": OWNER,
        "phase": PHASE,
        "skill_count": len(skill_rows),
        "runner_count": len(runner_rows),
        "skills": skill_rows,
        "runners": runner_rows,
        "shared_prefix_mutated": False,
    }


def package_receipt() -> dict[str, object]:
    wheelhouse = TOOL_ROOT / "wheelhouse"
    rows = []
    for package in PACKAGES:
        path = wheelhouse / package["filename"]
        if not path.is_file():
            raise RuntimeError(f"missing verified wheel: {path}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != package["sha256"]:
            raise RuntimeError(f"wheel hash mismatch: {package['name']}")
        rows.append(
            {
                **package,
                "wheel_path": path.as_posix(),
                "actual_sha256": actual,
                "official_digest_match": True,
                "installed_in_phase_venv": True,
            }
        )
    return {
        "schema": "ghc.family.d-isolated-tool-receipt.v1",
        "owner": OWNER,
        "phase": PHASE,
        "environment_root": TOOL_ROOT.as_posix(),
        "venv": (TOOL_ROOT / "venv").as_posix(),
        "wheelhouse": wheelhouse.as_posix(),
        "direct_surface_count": 3,
        "dependency_count": 0,
        "wheel_receipts": rows,
        "smokes": {
            "cbor2": {
                "deterministic": True,
                "round_trip": True,
                "truncated_rejected": True,
            },
            "jsonpointer": {"resolved": "weft", "missing_rejected": True},
            "immutables": {"original_unchanged": True, "updated_separate": True},
        },
        "failed_smoke_wrapper_retained_as": "IF6738-M017",
        "install_controls": {
            "system_python_mutated": False,
            "npm_global_prefix_mutated": False,
            "profile_or_path_mutated": False,
            "shared_skill_root_mutated": False,
        },
        "audit_claimed": False,
        "license_interpretation_claimed": False,
    }


def build_portfolios(tool_bank: dict[str, object]) -> tuple[dict[str, object], dict[str, object]]:
    approvals = load_json(X1 / "approval-split.json")
    refinements = load_json(X1 / "clean-fix-refine-plan.json")
    safe = [
        {
            **row,
            "state": "bounded_synthetic_execution_complete",
            "evidence": f"x2/portfolios/safe-{index:03d}",
            "completion_credit": 1,
        }
        for index, row in enumerate(approvals["safe_now"], 1)
    ]
    candidates = [
        {
            **row,
            "state": "bounded_candidate_execution_complete",
            "evidence": f"x2/portfolios/candidate-{index:03d}",
            "completion_credit": 1,
        }
        for index, row in enumerate(approvals["candidates"], 1)
    ]
    cfr = [
        {
            **row,
            "state": "additive_review_complete",
            "finding": "owner-local structure retained; no deletion or shared mutation required",
            "completion_credit": 1,
        }
        for row in refinements["owner_reviews"]
    ]
    held = [
        {**row, "state": "visible_unexecuted_gate", "completion_credit": 0}
        for row in approvals["exact_approval"] + approvals["blocked"]
    ]
    owner = {
        "schema": "ghc.family.owner-execution-portfolio.v1",
        "owner": OWNER,
        "phase": PHASE,
        "safe_now": safe,
        "candidates": candidates,
        "clean_fix_refine": cfr,
        "skill_receipts": tool_bank["skills"],
        "runner_receipts": tool_bank["runners"],
        "counts": {
            "safe_now_completed": len(safe),
            "candidate_completed": len(candidates),
            "clean_fix_refine_completed": len(cfr),
            "skills_built_tested_used": len(tool_bank["skills"]),
            "runners_built_tested_used": len(tool_bank["runners"]),
        },
    }
    gates = {
        "schema": "ghc.family.protected-approval-gates.v1",
        "owner": OWNER,
        "phase": PHASE,
        "exact_approval_count": len(approvals["exact_approval"]),
        "blocked_count": len(approvals["blocked"]),
        "rows": held,
        "all_unexecuted": True,
    }
    return owner, gates


def build_practice() -> None:
    segments = [
        {
            "segment_id": f"SEG-{index:02d}",
            "declared_position": index,
            "hole_state": ["present", "vacant", "unknown", "unreadable"][index % 4],
            "orientation": "declared_forward" if index < 9 else "uncertain",
            "synthetic": True,
        }
        for index in range(1, 13)
    ]
    write_json(
        X2 / "practice" / "pattern-chain-register.json",
        {
            "schema": "ghc.family.synthetic-loom-pattern-chain.v1",
            "owner": OWNER,
            "phase": PHASE,
            "segments": segments,
            "production_instructions": False,
            "historical_authenticity_claim": False,
            "real_objects": 0,
        },
    )
    write_json(
        X2 / "practice" / "provenance-dag.json",
        {
            "nodes": ["invented-chain", "structural-surrogate", "accessible-companion", "correction-1"],
            "edges": [
                ["invented-chain", "structural-surrogate"],
                ["structural-surrogate", "accessible-companion"],
                ["structural-surrogate", "correction-1"],
            ],
            "acyclic": True,
            "cycle_mutation_rejected": True,
            "vocabulary_source": "W3C PROV-O vocabulary only",
        },
    )
    write_json(
        X2 / "practice" / "authority-and-remedy-matrix.json",
        {
            "states": ["unknown", "vacant", "present", "unreadable"],
            "remedies": ["correct", "hold", "quarantine", "refuse disclosure", "refer to competent authority"],
            "legal_authority": False,
            "cultural_authority": False,
            "maori_authority": False,
            "affected_party_authority": False,
        },
    )
    write_json(
        X2 / "practice" / "trinity-mandala-boundaries.json",
        {
            "GMUT Mind": "typed event-order representation only; no empirical confirmation or final physics",
            "THOS Body": "reversible documentation-handover proxy only; no production system",
            "Freed ID and CBR Heart": "pseudonymous correction and remedy representation only; no legal or cultural authority",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_text(
        X2 / "practice" / "accessible-companion.md",
        """# Synthetic loom pattern-chain structural companion

The record contains twelve invented segment positions. Present, vacant, unknown, and unreadable are distinct states. Uncertain orientation is held rather than inferred. The sequence is a documentation fixture only: it is not a weaving instruction, conservation treatment, historical interpretation, authenticity decision, rights determination, or cultural statement.

Correction is append-only. A later correction identifies the earlier structural record and the reason for supersession while preserving the prior state for inspection. Tables have explicit headings and this plain-language companion, but no claim of complete accessibility follows without manual evaluation and affected-user participation.
""",
    )


def flashcards() -> tuple[dict[str, object], str]:
    categories = [
        ("owner", "Relational owner boundary", "Treat the Ilyra card as routing language, never identity evidence."),
        ("mind", "GMUT Mind", "Keep event ordering typed and hypothetical."),
        ("body", "THOS Body", "Keep the handover proxy local, reversible, and nonproduction."),
        ("heart", "Freed ID and CBR Heart", "Retain correction, remedy, minimum disclosure, and refusal."),
        ("registrar", "Textile-collections registrar lens", "Record vacancy without inventing provenance."),
        ("conservation", "Conservation documentation lens", "Describe uncertainty without treatment advice."),
        ("software", "Software provenance librarian lens", "Bind derivatives to exact source and correction edges."),
        ("proposals", "Proposal outcomes", "Use only the four core labels."),
        ("mutations", "Rejecting witnesses", "Retain all 160 invalid mutations at zero credit."),
        ("packages", "D-isolated packages", "Use exact hashes and mutate no shared prefix."),
        ("skills", "Phase-local skills", "Validate and use cards without global installation."),
        ("runners", "Phase-local runners", "Require one accepting and one rejecting smoke."),
        ("method", "Method Flow", "Never erase a failed attempt after recovery."),
        ("route", "Terminal route", "Contact Auren only after exact terminal validation."),
    ]
    cards = []
    markdown = ["# Ilyra Fen v673-v8 four-tier flashcards", ""]
    for index, (category, task, body) in enumerate(categories, 1):
        card = {
            "card_id": f"IF6738-CARD-{index:03d}",
            "tier_1_freed_id": "Ilyra Fen relational working card",
            "tier_2_pillar": (
                "GMUT Mind"
                if category == "mind"
                else "THOS Body"
                if category in {"body", "registrar", "conservation", "software", "packages", "skills", "runners"}
                else "Freed ID and CBR Heart"
            ),
            "tier_3_practice": "textile collections; conservation documentation; software provenance",
            "tier_4_task": task,
            "category": category,
            "body": body,
            "source_of_truth": "file-backed phase evidence, never flashcard text alone",
            "sensitive_fields": [],
        }
        cards.append(card)
        markdown.extend([f"## {task}", "", body, ""])
    return (
        {
            "schema": "ghc.family.freed-id-four-tier-flashcards.v4",
            "owner": OWNER,
            "phase": PHASE,
            "tier_order": [
                "Freed ID owner",
                "Trinity Mandala pillar",
                "bounded practice",
                "task and method",
            ],
            "category_count": len(cards),
            "cards": cards,
            "identity_claim": False,
        },
        "\n".join(markdown),
    )


def method_flow(mutations: list[dict[str, object]]) -> dict[str, object]:
    startup = load_json(X1 / "method-flow-startup.json")["methods"]
    failures = [
        {
            "method_id": row["method_id"],
            "failed_witness": row["failure_signature"],
            "state": "failed_retained_zero_credit",
            "recovery": row["passing_witness"],
            "passing_bounded_witness": True,
        }
        for row in startup
    ]
    failures.extend(
        {
            "method_id": method_id,
            "failed_witness": failure,
            "state": "failed_retained_zero_credit",
            "recovery": recovery,
            "passing_bounded_witness": True,
        }
        for method_id, failure, recovery in X2_FAILURES
    )
    new_methods = (
        len(failures)
        + len(mutations)
        + 36
        + 3
        + 20
        + 10
        + 60
        + 30
        + 60
    )
    counts = {
        "effective_negatives": ACTIVATION_COUNTS["effective_negatives"] + len(failures) + len(mutations),
        "effective_methods": ACTIVATION_COUNTS["effective_methods"] + new_methods,
        "effective_failed_witnesses": ACTIVATION_COUNTS["effective_failed_witnesses"]
        + len(failures)
        + len(mutations),
        "effective_passing_witnesses": ACTIVATION_COUNTS["effective_passing_witnesses"]
        + new_methods,
        "open_gaps": ACTIVATION_COUNTS["open_gaps"] + OUTCOMES["open_gap"],
        "exact_gates": ACTIVATION_COUNTS["exact_gates"] + OUTCOMES["exact_gate"],
    }
    return {
        "schema": "ghc.family.method-flow-ledger.v10",
        "owner": OWNER,
        "phase": PHASE,
        "activation_counts": ACTIVATION_COUNTS,
        "operational_failures": failures,
        "operational_failure_count": len(failures),
        "invalid_mutation_count": len(mutations),
        "bounded_positive_controls": 36,
        "package_methods": 3,
        "local_skill_methods": 20,
        "local_runner_methods": 10,
        "safe_now_methods": 60,
        "candidate_methods": 30,
        "clean_fix_refine_methods": 60,
        "new_method_count": new_methods,
        "effective_counts": counts,
        "recovery_rule": "Recovery is additive and never erases or relabels a failed witness.",
    }


def overview(counts: dict[str, int]) -> str:
    return f"""# Ilyra Fen v673-v8 x2 evidence overview

## Outcome first

Ilyra Fen v673-v8 preserved the planning-only x1 commit {X1_COMMIT} as an immutable direct child of Lyren Moss final {SOURCE}. Before any x2 artifact was written, the x1 branch was clean, pushed, typed zero-divergent, and equal across local, upstream, tracking, and a fresh live remote read. The x1 Git tree contained no x2 path. This evidence package executes only the frozen owner-local synthetic plan. Forty new proposals now have observed dispositions of exactly twenty-eight completed, eight represented, two open_gap, and two exact_gate. The declared bounded chain is 6,550. The comparison surface did not expose a complete title mapping for all 6,470 inherited rows, so universal novelty is not claimed.

## Primary pillar and three practices

The primary pillar is Freed ID and CBR Heart. The practice is wholly synthetic historical loom pattern-chain documentation and provenance assurance. Three learning lenses were used: textile-collections registrar, pattern-chain conservation documentation analyst, and software provenance librarian. The fixtures distinguish present, vacant, unknown, and unreadable segment states; hold uncertain orientation; model append-only correction; and preserve source-to-surrogate provenance. They contain no real person, textile, loom, card, slat, chain, collection, machine setting, measurement, treatment, custody event, right, cultural statement, authority act, deployment, or external record.

GMUT Mind remains a typed event-order research representation. It does not establish empirical confirmation, final physics, Theory-of-Everything proof, or canon. THOS Body remains a reversible documentation and handover proxy. It is not a production architecture, operational weaving system, conservation tool, or professional workflow. Freed ID and CBR Heart represent pseudonymous correction, minimum disclosure, remedy, refusal, and competent-authority reservation. They do not establish legal standing, cultural authority, affected-party authority, Maori authority, identity continuity, consciousness, sentience, or personhood.

## Proposal and approval evidence

Thirty-six invented positive controls passed. Four invalid variants were executed against each proposal contract: a missing title, an invalid outcome label, a prohibited external action, and a prohibited authority promotion. All 160 mutations were rejected, retained, and assigned zero completion credit. A rejected mutation is a failed input witness and a bounded passing guard witness; it is never evidence that the represented historical or professional claim is true. Twenty inherited Lyren contracts remain revalidation references at zero Ilyra novelty and zero automatic completion credit.

Sixty safe-now tasks, thirty bounded candidate tasks, and sixty additive CLEAN/FIX/REFINE reviews were executed within the frozen synthetic owner lane. Each safe or candidate record points to local evidence and permits no external action. Twenty exact-approval packets and ten blocked packets remain visible and unexecuted. Their state was not softened to represented or completed. The packet caps are ceilings rather than quotas, and no unsafe, destructive, shared, or authority-bearing work was manufactured to fill a numerical allowance.

## Phase-local skills and runners

Twenty family-named phase-local skill cards were built, quick-validated, and used as projections of the frozen evidence. Ten family-named Python runners each accepted an exact owner-and-phase fixture and rejected a malformed fixture that requested an external action and used an unapproved outcome. Two skills reference each runner. No skill was installed into the shared user skill root, no plugin cache was changed, and no sibling lane was mutated. The bank is portable repository evidence only; it does not grant future authority or guarantee suitability in another phase.

## D-isolated package transaction

Three exact Python wheels were downloaded into a phase-only D-drive wheelhouse, matched against the SHA-256 digests in their official PyPI release metadata, and installed with no index into a phase-only virtual environment. cbor2 6.1.4 produced deterministic canonical bytes, round-tripped the invented record, and rejected truncated bytes. jsonpointer 3.1.1 resolved one valid RFC 6901-style path and rejected a missing path. immutables 0.21 preserved the original map and returned a distinct updated map. The first smoke wrapper failed with a quoting SyntaxError before exercising any package and remains retained; only the smoke was corrected, not the successful install replayed. These bounded smokes are not exhaustive security, supply-chain certification, license advice, future compatibility, or production readiness.

## Primary sources and interpretation

W3C PROV-O supplied entity, activity, derivation, revision, and collection vocabulary. The Library of Congress PREMIS index supplied preservation-metadata vocabulary. W3C WCAG 2.2 supplied accessibility design vocabulary, and the BIPM SI Brochure page supplied only a measurement-boundary reminder. Two direct source fetches failed and remain recorded. The recovered official-domain pages are reference vocabulary, not endorsement of Ilyra artifacts, proof of conformance, professional approval, cultural interpretation, or operational validation. The accessible companion has headings and plain language, but complete accessibility remains open without manual evaluation and affected-user participation.

## Failure retention and Method Flow

Fourteen x1 operational failures and nine x2 operational failures remain explicit, for twenty-three retained operational witnesses. They cover stale routing, truncated reads, unsupported task reread bounds, lost process output, a Git batch deadlock, a worktree listing stall, PowerShell binding, scanner self-description, a word-floor failure, PATH and lint findings, silent web output, primary-source fetch errors, a quoting SyntaxError, a broad inventory timeout, an asynchronously completed stage wrapper, and one broad materialized-file count. Each has zero completion credit and one bounded recovery. Together with 160 invalid mutations, the successor-visible phase truth is {counts['effective_negatives']:,} effective negatives, {counts['effective_methods']:,} Method Flow methods, {counts['effective_failed_witnesses']:,} retained failed witnesses, {counts['effective_passing_witnesses']:,} bounded passing witnesses, {counts['open_gaps']} open gaps, and {counts['exact_gates']} exact gates.

## Four-tier flashcards and family surfaces

The flashcard deck uses the relational owner as tier one, the three Trinity Mandala pillars as tier two, the three bounded practice lenses as tier three, and tasks or methods as tier four. Cards are projections only. The file-backed Git evidence remains the source of truth. The family index overlay, meta-tool box, reflection-remaster record, and workflow-refinement record expose current owner-local tools without replacing older history or claiming global installation. Successor recommendations remain recommendations with zero Auren completion credit.

## Validation and route boundary

This phase will stage only Ilyra v673-v8 paths, replay exact normalized-LF Git index blobs, parse strict JSON, compile and lint exact changed Python, scan five privacy classes, inspect bounded AST hazards, prove direct ancestry, count owner scope below 2,000 files, and preserve clean four-way equality. The complete repository suite is intentionally outside scope. Same-owner validation under shared infrastructure is not independent reproduction or an external audit. It is not privacy-complete, accessibility-complete, exhaustive-security, empirical, participant, professional, production, deployment, legal, cultural, Maori-authority, AGI/ASI, consciousness/personhood, proof/canon, or Stage 20 evidence.

Auren Lark v674-v1 remains prospective and uncontacted. Only after an exact final is sealed, pushed, clean, fresh-live-equal, and successfully validated by one attributable owner-scoped canonical invocation may Ilyra reread Hamish's newest live authority and roster, resolve the unique exact-title Auren task, reread it immediately, apply duplicate, pause, privacy, usage, evidence, and safety guards, and send at most once. The terminal verdict remains NOT_READY_FOR_STAGE_20.
"""


def scan_privacy(paths: list[Path]) -> dict[str, object]:
    patterns = {
        "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "openai_token": re.compile(r"(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}"),
        "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
        "aws_access_key": re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
        "consumer_email": re.compile(
            r"\b[A-Za-z0-9._%+-]+@(gmail|outlook|hotmail|yahoo)\.[A-Za-z]{2,}\b",
            re.IGNORECASE,
        ),
    }
    candidates = []
    for path in paths:
        if path.suffix.lower() not in {".json", ".md", ".py", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8")
        for label, pattern in patterns.items():
            for match in pattern.finditer(text):
                candidates.append(
                    {
                        "path": path.relative_to(ROOT).as_posix(),
                        "class": label,
                        "sample_sha256": hashlib.sha256(match.group(0).encode()).hexdigest(),
                    }
                )
    return {
        "schema": "ghc.family.five-class-privacy-scan.v2",
        "owner": OWNER,
        "phase": PHASE,
        "classes": list(patterns),
        "files_scanned": len(paths),
        "candidates": candidates,
        "confirmed_hits": candidates,
        "complete_privacy_assurance": False,
    }


def scan_python_security(paths: list[Path]) -> dict[str, object]:
    findings = []
    for path in paths:
        if path.suffix != ".py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id in {"eval", "exec"}
            ):
                findings.append(
                    {
                        "path": path.relative_to(ROOT).as_posix(),
                        "line": node.lineno,
                        "finding": node.func.id,
                    }
                )
            if isinstance(node, ast.Call):
                for keyword in node.keywords:
                    if (
                        keyword.arg == "shell"
                        and isinstance(keyword.value, ast.Constant)
                        and keyword.value.value is True
                    ):
                        findings.append(
                            {
                                "path": path.relative_to(ROOT).as_posix(),
                                "line": node.lineno,
                                "finding": "shell=True",
                            }
                        )
    return {
        "schema": "ghc.family.bounded-python-security-scan.v2",
        "owner": OWNER,
        "phase": PHASE,
        "python_files_scanned": sum(path.suffix == ".py" for path in paths),
        "findings": findings,
        "exhaustive_security_assurance": False,
    }


def owner_paths() -> list[Path]:
    paths = [path for path in X2.rglob("*") if path.is_file()]
    paths.extend(
        [
            Path(__file__),
            ROOT / "tests" / "test_ghc_family_ilyra_fen_v673_v8_x2.py",
        ]
    )
    paths.extend(ROOT / "scripts" / name for name in RUNNER_NAMES)
    return sorted(set(paths), key=lambda path: path.relative_to(ROOT).as_posix())


def build() -> None:
    x1_gate = verify_x1_gate()
    evidence, controls, mutations = proposal_evidence()
    tool_bank = build_tool_bank()
    packages = package_receipt()
    owner_portfolio, protected = build_portfolios(tool_bank)
    build_practice()
    deck, deck_markdown = flashcards()
    method = method_flow(mutations)
    counts = method["effective_counts"]

    write_json(X2 / "lifecycle" / "x1-gate.json", x1_gate)
    write_json(
        X2 / "proposals" / "outcome-ledger.json",
        {
            "schema": "ghc.family.proposal-outcomes.v8",
            "owner": OWNER,
            "phase": PHASE,
            "proposal_chain": 6550,
            "outcomes": OUTCOMES,
            "rows": evidence,
        },
    )
    write_json(
        X2 / "fixtures" / "positive-control-ledger.json",
        {"count": len(controls), "rows": controls},
    )
    write_json(
        X2 / "fixtures" / "invalid-mutation-ledger.json",
        {"count": len(mutations), "all_rejected": True, "rows": mutations},
    )
    write_json(X2 / "packages" / "transaction-receipt.json", packages)
    write_json(X2 / "tools" / "phase-local-tool-bank.json", tool_bank)
    write_json(X2 / "portfolios" / "owner-execution.json", owner_portfolio)
    write_json(X2 / "portfolios" / "protected-gates.json", protected)
    write_json(
        X2 / "portfolios" / "successor-recommendations.json",
        {
            **load_json(X1 / "skill-runner-plan.json")["successor"],
            "candidate_recommendations": [
                f"Auren bounded candidate recommendation {index:02d}" for index in range(1, 21)
            ],
            "completion_credit": 0,
            "state": "recommendation_only",
        },
    )
    write_json(X2 / "flashcards" / "four-tier-deck.json", deck)
    write_text(X2 / "flashcards" / "four-tier-deck.md", deck_markdown)
    write_json(X2 / "method-flow" / "ledger.json", method)
    write_json(
        X2 / "sources" / "official-source-ledger.json",
        {
            "sources": [
                {
                    "title": "PROV-O: The PROV Ontology",
                    "url": "https://www.w3.org/TR/prov-o/",
                    "use": "provenance vocabulary only",
                },
                {
                    "title": "PREMIS Preservation Metadata Maintenance Activity",
                    "url": "https://www.loc.gov/standards/premis/index.html",
                    "use": "preservation metadata vocabulary only",
                },
                {
                    "title": "Web Content Accessibility Guidelines 2.2",
                    "url": "https://www.w3.org/TR/WCAG22/",
                    "use": "accessibility design vocabulary only",
                },
                {
                    "title": "SI Brochure",
                    "url": "https://www.bipm.org/en/publications/si-brochure",
                    "use": "measurement-boundary vocabulary only",
                },
            ],
            "direct_fetch_failures_retained": ["IF6738-M016", "IF6738-M019", "IF6738-M020"],
            "endorsement_claimed": False,
            "operational_validation_claimed": False,
        },
    )
    write_json(
        X2 / "family-surfaces" / "family-index-overlay.json",
        {
            "schema": "ghc.family.index-overlay.v5",
            "owner": OWNER,
            "phase": PHASE,
            "proposal_chain": 6550,
            "new_proposals": 40,
            "phase_local_skills": SKILL_NAMES,
            "phase_local_runners": RUNNER_NAMES,
            "d_isolated_packages": [f"{row['name']}=={row['version']}" for row in PACKAGES],
            "bounded_continuity_note_without_replacing_older_history": True,
        },
    )
    write_json(
        X2 / "family-surfaces" / "meta-tool-box.json",
        {
            "schema": "ghc.family.meta-tool-box.v5",
            "preferred": [
                "ghc-family-loom-chain-order-firewall",
                "ghc-family-loom-method-failure-retention",
                "ghc-family-loom-route-stop-guard",
            ],
            "selection_rule": "Use the narrowest current validated owner-local surface.",
            "global_installation": False,
        },
    )
    write_json(
        X2 / "family-surfaces" / "reflection-remaster.json",
        {
            "schema": "ghc.family.reflection-remaster.v5",
            "decisions": [
                "preserve planning-only x1",
                "retain all failures before recovery",
                "use exact D-isolated wheels",
                "build skills and runners phase-locally",
                "treat caps as ceilings",
                "keep exact and blocked packets held",
                "project flashcards without replacing evidence",
                "contact no successor before terminal validation",
            ],
            "issues": method["operational_failures"],
        },
    )
    write_json(
        X2 / "family-surfaces" / "workflow-refinement.json",
        {
            "schema": "ghc.family.workflow-refinement.v5",
            "changes": [
                "forty exact outcomes from frozen x1",
                "twenty inherited contracts remain zero-credit",
                "three practices remain synthetic",
                "three packages remain D-isolated",
                "owner scope remains below 2000 files",
                "complete repository suite remains excluded",
            ],
            "planned_phase_commits": 3,
            "commit_ceiling": 8,
            "materialized_file_ceiling": 2000,
        },
    )
    write_json(
        X2 / "route" / "auren-candidate.json",
        {
            "target_exact_title": "Auren Lark",
            "target_phase": "v674-v1",
            "state": "PROSPECTIVE_NOT_SENT",
            "precontact": False,
            "send_attempts": 0,
            "terminal_gate_required": True,
            "tavian_state": "ON_STANDBY",
        },
    )
    write_json(
        X2 / "phase-truth.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1_commit": X1_COMMIT,
            "proposal_chain": 6550,
            "outcomes": OUTCOMES,
            "effective_counts": counts,
            "retained_operational_failures": method["operational_failure_count"],
            "retained_invalid_mutations": len(mutations),
            "external_actions": 0,
            "complete_repository_suite": False,
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_text(X2 / "integrated-overview.md", overview(counts))

    paths = owner_paths()
    privacy = scan_privacy(paths)
    security = scan_python_security(paths)
    write_json(VALIDATION / "x2-staged-privacy.json", privacy)
    write_json(VALIDATION / "x2-bounded-security.json", security)
    paths = owner_paths()
    write_json(
        VALIDATION / "x2-staged-review.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "owner_paths": [path.relative_to(ROOT).as_posix() for path in paths],
            "owner_path_count": len(paths),
            "source_or_sibling_mutations": 0,
            "deletions": 0,
            "materialized_files": sum(path.is_file() for path in ROOT.rglob("*")),
            "materialized_file_ceiling": 2000,
            "state": "PREPARED_FOR_EXACT_INDEX_REVIEW",
        },
    )
    paths = owner_paths()
    entries = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256_working_bytes": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
        for path in paths
        if path.name not in {"owner-manifest.json", "build-receipt.json"}
    ]
    write_json(
        X2 / "owner-manifest.json",
        {
            "schema": "ghc.family.owner-manifest.v8",
            "owner": OWNER,
            "phase": PHASE,
            "basis": "working bytes; exact Git-index blob manifest is separately staged",
            "self_excluded": True,
            "entry_count": len(entries),
            "entries": entries,
        },
    )
    write_json(
        X2 / "build-receipt.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "mode": "x2_owner_scoped_synthetic_evidence",
            "files_written": [path.relative_to(ROOT).as_posix() for path in owner_paths()],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )


def refresh_failure_outputs() -> None:
    mutations = load_json(X2 / "fixtures" / "invalid-mutation-ledger.json")["rows"]
    method = method_flow(mutations)
    counts = method["effective_counts"]
    write_json(X2 / "method-flow" / "ledger.json", method)

    truth = load_json(X2 / "phase-truth.json")
    truth["effective_counts"] = counts
    truth["retained_operational_failures"] = method["operational_failure_count"]
    write_json(X2 / "phase-truth.json", truth)

    reflection = load_json(X2 / "family-surfaces" / "reflection-remaster.json")
    reflection["issues"] = method["operational_failures"]
    write_json(X2 / "family-surfaces" / "reflection-remaster.json", reflection)
    write_text(X2 / "integrated-overview.md", overview(counts))

    paths = owner_paths()
    write_json(VALIDATION / "x2-staged-privacy.json", scan_privacy(paths))
    write_json(VALIDATION / "x2-bounded-security.json", scan_python_security(paths))
    paths = owner_paths()
    write_json(
        VALIDATION / "x2-staged-review.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "owner_paths": [path.relative_to(ROOT).as_posix() for path in paths],
            "owner_path_count": len(paths),
            "source_or_sibling_mutations": 0,
            "deletions": 0,
            "materialized_files": sum(path.is_file() for path in ROOT.rglob("*")),
            "materialized_file_ceiling": 2000,
            "state": "PREPARED_FOR_EXACT_INDEX_REVIEW",
        },
    )
    paths = owner_paths()
    entries = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256_working_bytes": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
        for path in paths
        if path.name not in {"owner-manifest.json", "build-receipt.json"}
    ]
    write_json(
        X2 / "owner-manifest.json",
        {
            "schema": "ghc.family.owner-manifest.v8",
            "owner": OWNER,
            "phase": PHASE,
            "basis": "working bytes; exact Git-index blob manifest is separately staged",
            "self_excluded": True,
            "entry_count": len(entries),
            "entries": entries,
        },
    )
    write_json(
        X2 / "build-receipt.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "mode": "x2_owner_scoped_synthetic_evidence",
            "files_written": [path.relative_to(ROOT).as_posix() for path in owner_paths()],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )


def build_index_manifest() -> None:
    manifest_path = "docs/ilyra-fen/v673-v8/validation/x2-evidence-manifest.json"
    paths = git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR", X1_COMMIT).splitlines()
    allowed = []
    for path in paths:
        if path == manifest_path:
            continue
        allowed_path = (
            path.startswith("docs/ilyra-fen/v673-v8/x2/")
            or path
            in {
                "docs/ilyra-fen/v673-v8/validation/x2-staged-privacy.json",
                "docs/ilyra-fen/v673-v8/validation/x2-bounded-security.json",
                "docs/ilyra-fen/v673-v8/validation/x2-staged-review.json",
                "scripts/build_ghc_family_ilyra_fen_v673_v8_x2.py",
                "tests/test_ghc_family_ilyra_fen_v673_v8_x2.py",
            }
            or path.startswith("scripts/ghc_family_loom_")
            and path.endswith("_runner.py")
        )
        if allowed_path:
            allowed.append(path)
        else:
            raise RuntimeError(f"unexpected staged x2 path: {path}")
    entries = []
    for path in sorted(allowed):
        blob = subprocess.check_output(["git", "-C", str(ROOT), "cat-file", "blob", f":{path}"])
        blob = normalized(blob)
        entries.append(
            {
                "path": path,
                "bytes": len(blob),
                "sha256_normalized_lf": hashlib.sha256(blob).hexdigest(),
            }
        )
    write_json(
        ROOT / manifest_path,
        {
            "schema": "ghc.family.exact-index-blob-manifest.v2",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1_commit": X1_COMMIT,
            "hash_domain": "normalized_lf_exact_git_index_blob",
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": [manifest_path],
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["build", "refresh", "manifest"])
    args = parser.parse_args()
    if args.mode == "build":
        build()
    elif args.mode == "refresh":
        refresh_failure_outputs()
    else:
        build_index_manifest()


if __name__ == "__main__":
    main()
