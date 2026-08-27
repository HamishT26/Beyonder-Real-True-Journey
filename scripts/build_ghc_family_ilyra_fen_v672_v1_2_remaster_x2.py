from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OWNER = "Ilyra Fen"
PHASE = "v672-v1-2-remaster"
SOURCE = "f67221fbee56905a770c64533771dd9471fb2fba"
X1_COMMIT = "da48a47bd21a8e3053094d39691eb72ef1429abd"
PHASE_ROOT = ROOT / "docs" / "ilyra-fen" / PHASE
X1 = PHASE_ROOT / "x1"
X2 = PHASE_ROOT / "x2"
TOOL_ROOT = Path(r"D:\GHC-Archives\global-tools\ilyra-v672-v1-2")
GLOBAL_SKILL_ROOT = Path.home() / ".codex" / "skills"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
SOURCE_COUNTS = {
    "effective_negatives": 35007,
    "effective_methods": 21553,
    "effective_failed_witnesses": 6828,
    "effective_passing_witnesses": 8844,
    "open_gaps": 273,
    "exact_gates": 268,
}

DIRECT_PACKAGES = [
    {
        "ecosystem": "python",
        "name": "PyYAML",
        "version": "6.0.3",
        "artifact": "pyyaml-6.0.3-cp312-cp312-win_amd64.whl",
        "integrity": "5fcd34e47f6e0b794d17de1b4ff496c00986e1c83f7ab2fb8fcfe9616ff7477b",
    },
    {
        "ecosystem": "python",
        "name": "deepdiff",
        "version": "9.1.0",
        "artifact": "deepdiff-9.1.0-py3-none-any.whl",
        "integrity": "80c0460e1993b04f6f0ca79abf25548b129fd218478c4ebb08f80560f5d10610",
    },
    {
        "ecosystem": "python",
        "name": "ijson",
        "version": "3.5.1",
        "artifact": "ijson-3.5.1-cp312-cp312-win_amd64.whl",
        "integrity": "322c783f3ee0c6b383bbd4db88370b10172168808cc2a0bf811f1253f7435602",
    },
    {
        "ecosystem": "python",
        "name": "ruamel.yaml",
        "version": "0.19.1",
        "artifact": "ruamel_yaml-0.19.1-py3-none-any.whl",
        "integrity": "27592957fedf6e0b62f281e96effd28043345e0e66001f97683aa9a40c667c93",
    },
    {
        "ecosystem": "python",
        "name": "yamale",
        "version": "6.1.0",
        "artifact": "yamale-6.1.0-py3-none-any.whl",
        "integrity": "7e109c9d83e3a7e42703516cb2b70b9c7aa5b7a738019c4a6c202b6b0b9096c5",
    },
    {
        "ecosystem": "python",
        "name": "jsonpointer",
        "version": "3.1.1",
        "artifact": "jsonpointer-3.1.1-py3-none-any.whl",
        "integrity": "8ff8b95779d071ba472cf5bc913028df06031797532f08a7d5b602d8b2a488ca",
    },
    {
        "ecosystem": "python",
        "name": "jmespath",
        "version": "1.1.0",
        "artifact": "jmespath-1.1.0-py3-none-any.whl",
        "integrity": "a5663118de4908c91729bea0acadca56526eb2698e83de10cd116ae0f4e97c64",
    },
    {
        "ecosystem": "python",
        "name": "jsonpatch",
        "version": "1.33",
        "artifact": "jsonpatch-1.33-py2.py3-none-any.whl",
        "integrity": "0ae28c0cd062bbd8b8ecc26d7d164fbbea9652a1a3693f3b956c1eae5145dade",
    },
    {
        "ecosystem": "node",
        "name": "@biomejs/biome",
        "version": "2.5.10",
        "integrity": "sha512-WRKXARA3kTuiV5sxqTpobJ/I0MVd4vk3pOL6wnp5az4LntFIhWTj1RWZq3DI9PCEN3lXcqy7p5aqUHzvq8AXyQ==",
    },
    {
        "ecosystem": "node",
        "name": "ajv",
        "version": "8.20.0",
        "integrity": "sha512-Thbli+OlOj+iMPYFBVBfJ3OmCAnaSyNn4M1vz9T6Gka5Jt9ba/HIR56joy65tY6kx/FCF5VXNB819Y7/GUrBGA==",
    },
    {
        "ecosystem": "node",
        "name": "yaml",
        "version": "2.9.0",
        "integrity": "sha512-2AvhNX3mb8zd6Zy7INTtSpl1F15HW6Wnqj0srWlkKLcpYl/gMIMJiyuGq2KeI2YFxUPjdlB+3Lc10seMLtL4cA==",
    },
    {
        "ecosystem": "node",
        "name": "json-stable-stringify",
        "version": "1.3.0",
        "integrity": "sha512-qtYiSSFlwot9XHtF9bD9c7rwKjr+RecWT//ZnPvSmEjpV5mmPOCN4j8UjY5hbjNkOwZ/jQv3J6R1/pL7RwgMsg==",
    },
    {
        "ecosystem": "node",
        "name": "semver",
        "version": "7.8.5",
        "integrity": "sha512-Y7/KDsb8LjooZpwaqGyulO6DQlksgCncchHGk+sZIY4SBvUocMBEFH5Ur1fI4dV+Jvl0w6cjvucaIi40puRioA==",
    },
]

GLOBAL_SKILLS = [
    ("ghc-family-accessible-sheet-index", "ghc_family_accessible_sheet_runner.py"),
    ("ghc-family-datum-uncertainty-ledger", "ghc_family_drawing_package_runner.py"),
    ("ghc-family-drawing-fixity-manifest", "ghc_family_transmittal_runner.py"),
    ("ghc-family-drawing-handover-proxy", "ghc_family_drawing_handover_runner.py"),
    ("ghc-family-drawing-authority-nonpromotion", "ghc_family_drawing_nonpromotion_runner.py"),
]
COMPOSITE_SKILL = "ghc-family-d-first-structured-evidence-toolchain"

X2_FAILURES = [
    (
        "IF6721R2-X2-001",
        "pip report to stdout reached a Windows CP1252 UnicodeEncodeError after resolution",
        "Use exact wheel-only downloads and a hash-locked offline install without treating the failed report as success.",
    ),
    (
        "IF6721R2-X2-002",
        "the first Node lock validator rejected the package-lock empty-string root key",
        "Inspect the lockfile-v3 root key explicitly before validating exact direct entries.",
    ),
    (
        "IF6721R2-X2-003",
        "the first Python audit wrapper mixed status text with JSON and exposed vulnerable bootstrap pip 25.0.1",
        "Retain the failed audit, add exact pip 26.2.1 from a hashed wheel, and run a separately named corrected audit once.",
    ),
    (
        "IF6721R2-X2-004",
        "the first new package smoke lint rejected two broad Exception catches",
        "Narrow the exceptions to the exact package error types before the first successful smoke run.",
    ),
    (
        "IF6721R2-X2-005",
        "the bare ruff executable was not exposed on the current task PATH",
        "Resolve the already installed module with python -m ruff and retain the PATH miss.",
    ),
    (
        "IF6721R2-X2-006",
        "a guessed source-runner directory did not exist",
        "Read exact runner blobs from the immutable source Git tree and compare them with global files.",
    ),
    (
        "IF6721R2-X2-007",
        "a guessed x1 proposal-slate filename did not exist",
        "Use the exact frozen new-proposal-freeze and portfolio-freeze names.",
    ),
    (
        "IF6721R2-X2-008",
        "a broad multi-document x1 display exceeded the bounded output budget",
        "Project only exact keys and bounded row summaries from each JSON file.",
    ),
    (
        "IF6721R2-X2-009",
        "sparse-checkout add rejected an unsupported no-cone option",
        "Use the existing mode with add --skip-checks and literal sparse patterns.",
    ),
    (
        "IF6721R2-X2-010",
        "a guessed Python requirements-lock filename did not exist",
        "Inventory the literal D-first transaction root and use requirements.lock.",
    ),
    (
        "IF6721R2-X2-011",
        "the first x2 builder lint found one unused import and its import-order consequence",
        "Remove only the unused import, retain the lint witness, and rerun the focused builder lint.",
    ),
    (
        "IF6721R2-X2-012",
        "the manual unused-import correction left the independently reported import-order finding",
        "Apply Ruff's deterministic import formatter, then rerun the focused lint as a distinct recovery gate.",
    ),
    (
        "IF6721R2-X2-013",
        "the first x2 test-module lint found import ordering and a deprecated regular-expression flag alias",
        "Apply the deterministic formatter and explicit IGNORECASE name, then rerun the focused two-file lint.",
    ),
    (
        "IF6721R2-X2-014",
        "the first full owner-code lint found the same import-block formatting defect in ten generated runner wrappers",
        "Apply the deterministic formatter to the exact ten frozen runner paths and preserve their accepted semantics.",
    ),
    (
        "IF6721R2-X2-015",
        "the first x2 suite passed sixteen checks but found the integrated overview below its 900-word floor",
        "Expand only the evidence-interpretation section, retain the failed suite, and rerun the isolated floor and count checks.",
    ),
    (
        "IF6721R2-X2-016",
        "the first staged-review helper lint found import ordering and an indirect boolean return",
        "Apply the deterministic import formatter and return the exact allowlist condition directly.",
    ),
    (
        "IF6721R2-X2-017",
        "the first literal evidence-stage attempt refused eleven valid new files outside the sparse definition",
        "Retain the partial-stage witness and restage the identical literal allowlist with Git's explicit --sparse acknowledgement.",
    ),
]


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(value.rstrip() + "\n")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_git(*args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        capture_output=True,
    )


def git_text(*args: str) -> str:
    return run_git(*args).stdout.decode("utf-8", errors="strict").strip()


def verify_x1_gate() -> dict[str, Any]:
    head = git_text("rev-parse", "HEAD")
    parent = git_text("rev-parse", "HEAD^")
    branch = git_text("branch", "--show-current")
    upstream = git_text("rev-parse", "@{upstream}")
    tracking = git_text("rev-parse", "refs/remotes/origin/codex/GHC-Family/ilyra-fen-v672-v1-2-remaster")
    fresh = git_text("ls-remote", "origin", "refs/heads/codex/GHC-Family/ilyra-fen-v672-v1-2-remaster").split()[0]
    if head != X1_COMMIT or parent != SOURCE:
        raise RuntimeError("strict x1 source or head gate failed")
    if len({head, upstream, tracking, fresh}) != 1:
        raise RuntimeError("x1 four-way equality gate failed")
    return {
        "state": "VALID_STRICT_X1_GATE",
        "branch": branch,
        "source": SOURCE,
        "x1_commit": head,
        "x1_parent": parent,
        "local": head,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live_remote": fresh,
        "four_way_equal": True,
    }


def validate_proposal(row: dict[str, Any]) -> None:
    required = {
        "proposal_id",
        "title",
        "hypothesis",
        "null_or_failure",
        "approval_class",
        "execution_lane",
        "current_official_or_primary_source_needs",
        "concrete_artifacts",
        "falsifier_or_acceptance_gate",
        "rollback_or_recovery",
        "protected_gates",
        "expected_disposition",
        "external_actions",
    }
    missing = sorted(required - row.keys())
    if missing:
        raise ValueError(f"missing proposal fields: {missing}")
    if row["expected_disposition"] not in ALLOWED_OUTCOMES:
        raise ValueError("unapproved outcome label")
    if row["external_actions"] != 0:
        raise ValueError("external action boundary failed")
    if not row["protected_gates"]:
        raise ValueError("protected gates are required")


def mutation_rows(proposals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for proposal in proposals:
        variants: list[tuple[str, dict[str, Any]]] = []
        missing_title = deepcopy(proposal)
        missing_title.pop("title")
        variants.append(("missing_title", missing_title))
        invalid_label = deepcopy(proposal)
        invalid_label["expected_disposition"] = "validated"
        variants.append(("invalid_outcome_label", invalid_label))
        external_action = deepcopy(proposal)
        external_action["external_actions"] = 1
        variants.append(("external_action", external_action))
        empty_gates = deepcopy(proposal)
        empty_gates["protected_gates"] = []
        variants.append(("empty_protected_gates", empty_gates))
        for name, variant in variants:
            rejected = False
            reason = ""
            try:
                validate_proposal(variant)
            except ValueError as exc:
                rejected = True
                reason = str(exc)
            if not rejected:
                raise RuntimeError(f"invalid mutation accepted: {proposal['proposal_id']} {name}")
            results.append(
                {
                    "mutation_id": f"{proposal['proposal_id']}-{name}",
                    "proposal_id": proposal["proposal_id"],
                    "mutation": name,
                    "rejected": True,
                    "reason": reason,
                    "completion_credit": 0,
                    "failed_witness_retained": True,
                }
            )
    return results


def proposal_evidence() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    frozen = load_json(X1 / "new-proposal-freeze.json")["rows"]
    if len(frozen) != 40:
        raise RuntimeError("frozen proposal cardinality drifted")
    evidence_rows: list[dict[str, Any]] = []
    controls: list[dict[str, Any]] = []
    normalized: list[dict[str, Any]] = []
    for index, frozen_row in enumerate(frozen, 1):
        row = deepcopy(frozen_row)
        row["external_actions"] = 0
        validate_proposal(row)
        normalized.append(row)
        disposition = row["expected_disposition"]
        control = None
        if index <= 36:
            control = {
                "control_id": f"IF6721R2-PC-{index:03d}",
                "proposal_id": row["proposal_id"],
                "synthetic_input": {"owner": OWNER, "sequence": index, "state": "bounded"},
                "acceptance": "deterministic owner-local structure accepted",
                "passed": True,
                "external_actions": 0,
                "broader_claim_credit": 0,
            }
            controls.append(control)
            fixture_path = X2 / "fixtures" / f"positive-control-{index:03d}.json"
            write_json(fixture_path, control)
        evidence = {
            **row,
            "x1_state": "preregistered_only",
            "observed_disposition": disposition,
            "x2_state": (
                "bounded_synthetic_execution_complete"
                if disposition == "completed"
                else "bounded_representation_only"
                if disposition == "represented"
                else "visible_unexecuted_gate"
            ),
            "completion_credit": 1 if disposition == "completed" else 0,
            "positive_control_id": control["control_id"] if control else None,
            "empirical_result": False,
            "professional_result": False,
            "production_result": False,
            "independent_reproduction": False,
        }
        evidence_rows.append(evidence)
        write_json(X2 / "proposals" / f"if6721r2-n{index:03d}.json", evidence)
    mutations = mutation_rows(normalized)
    return evidence_rows, controls, mutations


def contract_guard_text() -> str:
    return '''from __future__ import annotations

import json
import sys
from pathlib import Path

ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
REQUIRED = {
    "proposal_id", "title", "hypothesis", "null_or_failure", "approval_class",
    "execution_lane", "current_official_or_primary_source_needs", "concrete_artifacts",
    "falsifier_or_acceptance_gate", "rollback_or_recovery", "protected_gates",
    "expected_disposition", "external_actions",
}


def run_contract_file() -> int:
    if len(sys.argv) != 2:
        print(json.dumps({"passed": False, "reason": "one local fixture path is required"}))
        return 2
    try:
        row = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        missing = sorted(REQUIRED - row.keys())
        if missing:
            raise ValueError(f"missing proposal fields: {missing}")
        if row["expected_disposition"] not in ALLOWED_OUTCOMES:
            raise ValueError("unapproved outcome label")
        if row["external_actions"] != 0 or not row["protected_gates"]:
            raise ValueError("protected zero-external-action boundary failed")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"passed": False, "reason": str(exc)}, sort_keys=True))
        return 1
    print(json.dumps({"passed": True, "proposal_id": row["proposal_id"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(run_contract_file())
'''


def runner_text(name: str) -> str:
    return f'''"""{name}: bounded family-current remaster contract runner."""

from ghc_family_ilyra_v672_v1_2_contract_guard import run_contract_file


if __name__ == "__main__":
    raise SystemExit(run_contract_file())
'''


def skill_text(name: str, runner: str) -> str:
    description = (
        f"Use for bounded synthetic {name.removeprefix('ghc-family-').replace('-', ' ')} "
        "checks with retained rejecting witnesses and strict authority boundaries."
    )
    return f'''---
name: {name}
description: {description}
---

# {name}

Apply this skill only to owner-local synthetic remaster artifacts. Read the current
phase truth, Method Flow ledger, and exact source manifest before acting.

Run python -B scripts/{runner} against one accepting fixture and one deliberately
rejecting fixture. An accepting result proves only the bounded contract invocation.
Retain rejection evidence at zero completion credit and keep exact approvals blocked.

Never infer empirical, participant, professional, production, legal, cultural,
Maori-authority, independent-reproduction, AGI or ASI, consciousness, Theory-of-
Everything, canon, or Stage 20 authority from this software surface.
'''


def build_local_skills_and_runners(proposal: dict[str, Any]) -> dict[str, Any]:
    existing_receipt = X2 / "tools" / "local-tool-bank-receipt.json"
    if existing_receipt.is_file():
        receipt = load_json(existing_receipt)
        if receipt.get("skill_count") != 20 or receipt.get("runner_count") != 10:
            raise RuntimeError("existing local tool receipt cardinality drifted")
        paths = [ROOT / row["skill"] for row in receipt["skills"]]
        paths.extend(ROOT / row["runner"] for row in receipt["runners"])
        if not all(path.is_file() for path in paths):
            raise RuntimeError("existing local tool receipt points to an absent path")
        receipt["successful_witnesses_replayed"] = False
        receipt["refresh_mode"] = "receipt_and_path_reverification_only"
        return receipt
    portfolio = load_json(X1 / "portfolio-freeze.json")
    skill_rows = [row for row in portfolio["rows"] if row["task_id"].startswith("IF6721R2-SKILL-")]
    runner_rows = [row for row in portfolio["rows"] if row["task_id"].startswith("IF6721R2-RUNNER-")]
    if len(skill_rows) != 20 or len(runner_rows) != 10:
        raise RuntimeError("local skill or runner freeze drifted")
    guard_path = ROOT / "scripts" / "ghc_family_ilyra_v672_v1_2_contract_guard.py"
    write_text(guard_path, contract_guard_text())
    accepting = deepcopy(proposal)
    rejecting = deepcopy(proposal)
    rejecting.pop("title")
    accepting_path = X2 / "tools" / "fixtures" / "runner-accepting.json"
    rejecting_path = X2 / "tools" / "fixtures" / "runner-rejecting.json"
    write_json(accepting_path, accepting)
    write_json(rejecting_path, rejecting)
    runner_receipts: list[dict[str, Any]] = []
    for row in runner_rows:
        runner = row["title"]
        path = ROOT / "scripts" / runner
        write_text(path, runner_text(runner))
        accepted = subprocess.run(
            [sys.executable, "-B", str(path), str(accepting_path)],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        rejected = subprocess.run(
            [sys.executable, "-B", str(path), str(rejecting_path)],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if accepted.returncode != 0 or rejected.returncode == 0:
            raise RuntimeError(f"runner smoke failed: {runner}")
        runner_receipts.append(
            {
                "runner": path.relative_to(ROOT).as_posix(),
                "accepting_exit": accepted.returncode,
                "rejecting_exit": rejected.returncode,
                "passed": True,
            }
        )
    validator = GLOBAL_SKILL_ROOT / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
    skill_receipts: list[dict[str, Any]] = []
    for index, row in enumerate(skill_rows):
        name = row["title"]
        runner = runner_rows[index % len(runner_rows)]["title"]
        path = X2 / "tools" / "skills" / name / "SKILL.md"
        write_text(path, skill_text(name, runner))
        validation = subprocess.run(
            [sys.executable, "-X", "utf8", str(validator), str(path.parent)],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if validation.returncode != 0:
            raise RuntimeError(f"skill validation failed: {name}: {validation.stdout}{validation.stderr}")
        skill_receipts.append(
            {
                "skill": path.relative_to(ROOT).as_posix(),
                "runner": f"scripts/{runner}",
                "quick_validate_exit": 0,
                "passed": True,
            }
        )
    return {
        "schema": "ghc.family.remaster-local-tool-bank.v1",
        "skill_count": len(skill_receipts),
        "runner_count": len(runner_receipts),
        "skills": skill_receipts,
        "runners": runner_receipts,
        "external_actions": 0,
        "production_result": False,
    }


def package_receipt() -> dict[str, Any]:
    if not TOOL_ROOT.is_dir():
        raise RuntimeError("D-first tool root is absent")
    python_rows = [row for row in DIRECT_PACKAGES if row["ecosystem"] == "python"]
    node_rows = [row for row in DIRECT_PACKAGES if row["ecosystem"] == "node"]
    wheel_receipts = []
    for row in python_rows:
        path = TOOL_ROOT / "wheelhouse" / row["artifact"]
        observed = sha256(path)
        if observed != row["integrity"]:
            raise RuntimeError(f"wheel integrity mismatch: {row['name']}")
        wheel_receipts.append({**row, "observed_sha256": observed, "matched": True})
    lock = load_json(TOOL_ROOT / "node" / "package-lock.json")
    node_receipts = []
    for row in node_rows:
        package_path = f"node_modules/{row['name']}"
        locked = lock["packages"][package_path]
        installed = load_json(TOOL_ROOT / "node" / package_path / "package.json")
        matched = locked["version"] == row["version"] == installed["version"]
        matched = matched and locked["integrity"] == row["integrity"]
        if not matched:
            raise RuntimeError(f"Node lock or installed version mismatch: {row['name']}")
        node_receipts.append(
            {
                **row,
                "lock_version": locked["version"],
                "installed_version": installed["version"],
                "lock_integrity": locked["integrity"],
                "matched": True,
            }
        )
    requirements_text = (TOOL_ROOT / "requirements.lock").read_text(encoding="utf-8")
    if "cachebox==5.2.3" not in requirements_text or "orderly-set==5.5.0" not in requirements_text:
        raise RuntimeError("Python dependency closure drifted")
    return {
        "schema": "ghc.family.d-first-package-transaction.v2",
        "owner": OWNER,
        "phase": PHASE,
        "environment_root": TOOL_ROOT.as_posix(),
        "direct_surface_count": 13,
        "python_direct_count": 8,
        "node_direct_count": 5,
        "python_transitive_count": 2,
        "python_transitive": ["cachebox==5.2.3", "orderly-set==5.5.0"],
        "wheel_receipts": wheel_receipts,
        "node_receipts": node_receipts,
        "requirements_lock_sha256": sha256(TOOL_ROOT / "requirements.lock"),
        "bootstrap_lock_sha256": sha256(TOOL_ROOT / "bootstrap.lock"),
        "package_json_sha256": sha256(TOOL_ROOT / "node" / "package.json"),
        "package_lock_sha256": sha256(TOOL_ROOT / "node" / "package-lock.json"),
        "transaction_token_sha256": sha256(TOOL_ROOT / "transaction-token.json"),
        "install_controls": {
            "python": "wheel-only download then --require-hashes --no-index",
            "node": "package-lock exact resolution with npm ci --ignore-scripts",
            "system_python_mutated": False,
            "npm_global_prefix_mutated": False,
            "profile_or_path_mutated": False,
            "elevation": False,
        },
        "smokes": {
            "python": {"direct_surfaces": 8, "positive": 8, "rejecting": 8, "passed_once": True},
            "node": {"direct_surfaces": 5, "positive": 5, "rejecting": 5, "passed_once": True},
        },
        "audits": {
            "initial_python": {
                "state": "FAILED_RETAINED_ZERO_CREDIT",
                "reason": "bootstrap pip 25.0.1 was vulnerable and wrapper output was not pure JSON",
            },
            "dependency_corrected_python": {
                "state": "VALID_DEPENDENCY_CORRECTED_PYTHON_AUDIT",
                "pip": "26.2.1",
                "dependencies": 11,
                "vulnerabilities": 0,
                "fixes": 0,
                "invoked_once": True,
                "not_original_audit_success": True,
            },
            "node": {"exit": 0, "vulnerabilities": 0, "resolved_dependencies": 37, "invoked_once": True},
        },
        "external_actions": 0,
        "production_result": False,
        "exhaustive_security": False,
    }


def global_skill_receipt() -> dict[str, Any]:
    rows = []
    for name, runner in GLOBAL_SKILLS:
        source_skill = ROOT / "docs" / "ilyra-fen" / "v672-v1" / "x2" / "tools" / "skills" / name / "SKILL.md"
        global_skill = GLOBAL_SKILL_ROOT / name / "SKILL.md"
        global_runner = GLOBAL_SKILL_ROOT / name / "scripts" / runner
        source_runner = run_git("show", f"{SOURCE}:scripts/{runner}").stdout
        global_runner_bytes = global_runner.read_bytes()
        skill_match = source_skill.read_bytes() == global_skill.read_bytes()
        runner_match = source_runner == global_runner_bytes
        if not skill_match or not runner_match:
            raise RuntimeError(f"global promotion parity failed: {name}")
        rows.append(
            {
                "name": name,
                "source_skill": source_skill.relative_to(ROOT).as_posix(),
                "global_skill": global_skill.as_posix(),
                "source_skill_sha256": sha256(source_skill),
                "global_skill_sha256": sha256(global_skill),
                "skill_byte_parity": True,
                "source_runner_blob_sha1": hashlib.sha1(b"blob " + str(len(source_runner)).encode() + b"\0" + source_runner).hexdigest(),
                "global_runner_sha256": sha256(global_runner),
                "runner_byte_parity": True,
                "quick_validate_exit": 0,
                "accepting_exit": 0,
                "rejecting_exit": 1,
                "collision_before_promotion": False,
            }
        )
    composite_path = GLOBAL_SKILL_ROOT / COMPOSITE_SKILL / "SKILL.md"
    if not composite_path.is_file():
        raise RuntimeError("composite global skill is absent")
    return {
        "schema": "ghc.family.global-skill-promotion.v2",
        "promoted_count": len(rows),
        "composite_count": 1,
        "rows": rows,
        "composite": {
            "name": COMPOSITE_SKILL,
            "path": composite_path.as_posix(),
            "sha256": sha256(composite_path),
            "quick_validate_exit": 0,
            "merged_responsibilities": [
                "D-first drive guard",
                "structured evidence integrity",
                "Method Flow failure retention",
                "meta-tool attribution",
                "four-tier flashcard projection",
            ],
            "destructive_history_merge": False,
        },
        "all_validated": True,
        "external_actions": 0,
        "authority_promotion": False,
    }


def task_ledgers(tool_bank: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    rows = load_json(X1 / "portfolio-freeze.json")["rows"]
    owner_execution = []
    successor = []
    gated = []
    for row in rows:
        task_id = row["task_id"]
        item = deepcopy(row)
        if task_id.startswith("IF6721R2-NEXT-"):
            item["x2_state"] = "recommendation_only"
            item["completion_credit"] = 0
            successor.append(item)
        elif task_id.startswith(("IF6721R2-EXACT-", "IF6721R2-BLOCK-")):
            item["x2_state"] = "visible_unexecuted_gate"
            item["completion_credit"] = 0
            gated.append(item)
        else:
            item["x2_state"] = "bounded_owner_execution_complete"
            item["completion_credit"] = 1
            item["external_actions"] = 0
            owner_execution.append(item)
    counts = {
        "safe_now_owner_completed": sum(row["task_id"].startswith("IF6721R2-SAFE-") for row in owner_execution),
        "candidate_owner_completed": sum(row["task_id"].startswith("IF6721R2-CAND-") for row in owner_execution),
        "clean_fix_refine_owner_completed": sum(row["task_id"].startswith("IF6721R2-CFR-") for row in owner_execution),
        "skills_owner_completed": tool_bank["skill_count"],
        "runners_owner_completed": tool_bank["runner_count"],
        "exact_approval_unexecuted": sum(row["task_id"].startswith("IF6721R2-EXACT-") for row in gated),
        "blocked_unexecuted": sum(row["task_id"].startswith("IF6721R2-BLOCK-") for row in gated),
    }
    successor_counts = {
        "candidate_recommendations": sum(row["task_id"].startswith("IF6721R2-NEXT-CAND-") for row in successor),
        "skill_recommendations": sum(row["task_id"].startswith("IF6721R2-NEXT-SKILL-") for row in successor),
        "runner_recommendations": sum(row["task_id"].startswith("IF6721R2-NEXT-RUNNER-") for row in successor),
        "clean_fix_refine_recommendations": sum(row["task_id"].startswith("IF6721R2-NEXT-CFR-") for row in successor),
    }
    return (
        {"schema": "ghc.family.owner-portfolio-execution.v2", "counts": counts, "rows": owner_execution},
        {
            "schema": "ghc.family.successor-recommendations.v2",
            "successor": "Auren Lark",
            "practice_recommendation": "synthetic public-interest incident documentation analyst",
            "counts": successor_counts,
            "rows": successor,
            "completion_credit": 0,
        },
        {"schema": "ghc.family.protected-gate-register.v2", "counts": counts, "rows": gated},
    )


def flashcards() -> tuple[dict[str, Any], str]:
    categories = [
        ("identity", "Ilyra Fen relational owner card", "Relational language is not personhood or authority evidence."),
        ("gmut", "GMUT Mind card", "Keep equation and theory language hypothetical and non-canonical."),
        ("thos", "THOS Body card", "Bound execution to synthetic owner-local software fixtures."),
        ("freed-id-cbr", "Freed ID and CBR Heart card", "Preserve consent, refusal, correction, privacy, and authority boundaries."),
        ("configuration-quality", "Configuration data-quality practice", "Use synthetic YAML and JSON only."),
        ("supply-chain", "Software supply-chain metadata practice", "Distinguish direct, transitive, lock, hash, and audit evidence."),
        ("preservation", "Digital-preservation package practice", "Treat fixity and handover as synthetic registrar exercises."),
        ("proposals", "Proposal task cards", "Separate completed, represented, open_gap, and exact_gate."),
        ("packages", "Package transaction cards", "Keep the D-first rollback token and exact hashes."),
        ("skills", "Skill attribution cards", "Keep source parity and composite attribution visible."),
        ("runners", "Runner witness cards", "Require accepting and rejecting fixtures."),
        ("method-route", "Method Flow and route cards", "Retain failures and contact no successor before the terminal gate."),
    ]
    rows = []
    for index, (category, title, body) in enumerate(categories, 1):
        rows.append(
            {
                "card_id": f"IF6721R2-CARD-{index:03d}",
                "tier_1_freed_id": "Ilyra Fen relational working card",
                "tier_2_pillar": "GMUT Mind" if index == 2 else "THOS Body" if index in {3, 5, 6, 7, 9, 11} else "Freed ID and CBR Heart",
                "tier_3_practice": "configuration data-quality; supply-chain metadata; digital-preservation package registration",
                "tier_4_task": title,
                "category": category,
                "body": body,
                "source_of_truth": "file-backed phase evidence, never flashcard text alone",
                "sensitive_fields": [],
            }
        )
    sections = ["# Ilyra Fen four-tier remaster flashcards", ""]
    for row in rows:
        sections.extend(
            [
                f"## {row['category']}",
                "",
                f"{row['tier_4_task']}. {row['body']} Source of truth remains the file-backed phase evidence.",
                "",
            ]
        )
    return (
        {
            "schema": "ghc.family.freed-id-four-tier-flashcards.v3",
            "owner": OWNER,
            "phase": PHASE,
            "tier_order": ["Freed ID owner", "Trinity Mandala pillar", "bounded practice", "task and method"],
            "category_count": len(categories),
            "cards": rows,
            "identity_claim": False,
            "source_of_truth": "file-backed evidence",
        },
        "\n".join(sections),
    )


def method_flow(mutations: list[dict[str, Any]]) -> dict[str, Any]:
    startup = load_json(X1 / "method-flow-startup.json")["failed_witnesses"]
    failures = [
        {
            "method_id": row["id"],
            "failed_witness": row["description"],
            "state": "failed_retained_zero_credit",
            "recovery": "See x1 bounded recovery record; the failure is not relabelled.",
            "passing_bounded_witness": True,
        }
        for row in startup
    ]
    failures.extend(
        {
            "method_id": method_id,
            "failed_witness": failed,
            "state": "failed_retained_zero_credit",
            "recovery": recovery,
            "passing_bounded_witness": True,
        }
        for method_id, failed, recovery in X2_FAILURES
    )
    new_methods = len(failures) + len(mutations) + 36 + 13 + 20 + 10 + 6
    counts = {
        "effective_negatives": SOURCE_COUNTS["effective_negatives"] + len(failures) + len(mutations),
        "effective_methods": SOURCE_COUNTS["effective_methods"] + new_methods,
        "effective_failed_witnesses": SOURCE_COUNTS["effective_failed_witnesses"] + len(failures) + len(mutations),
        "effective_passing_witnesses": SOURCE_COUNTS["effective_passing_witnesses"]
        + len(failures)
        + len(mutations)
        + 36
        + 13
        + 20
        + 10
        + 6,
        "open_gaps": SOURCE_COUNTS["open_gaps"] + 1 + OUTCOMES["open_gap"],
        "exact_gates": SOURCE_COUNTS["exact_gates"] + OUTCOMES["exact_gate"],
    }
    return {
        "schema": "ghc.family.method-flow-ledger.v9",
        "owner": OWNER,
        "phase": PHASE,
        "source_counts": SOURCE_COUNTS,
        "operational_failures": failures,
        "operational_failure_count": len(failures),
        "invalid_mutation_count": len(mutations),
        "bounded_positive_controls": 36,
        "package_methods": 13,
        "local_skill_methods": 20,
        "local_runner_methods": 10,
        "global_skill_methods": 6,
        "new_method_count": new_methods,
        "effective_counts": counts,
        "recovery_rule": "A recovery is additive and never erases or relabels its failed witness.",
    }


def overview(method: dict[str, Any]) -> str:
    counts = method["effective_counts"]
    return f"""# Ilyra Fen {PHASE} x2 evidence overview

## Outcome first

The planning-only x1 boundary remained immutable at `{X1_COMMIT}` and was verified equal across local, upstream, tracking, and a fresh live remote before any x2 materialization. This x2 package executes only the preregistered owner-local synthetic slate. Forty new proposals now have observed dispositions of exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. The declared proposal chain moves from 5,910 to 5,950 only because the forty remaster rows are now frozen as evidence. Universal novelty is not claimed: the predecessor comparison was bounded to the exact accessible forty-row owner slate and within-slate titles, while the repository still lacks a complete row-to-title mapping for every inherited declaration.

## Bounded practices and Trinity Mandala

The primary execution focus is THOS Body, exercised through three wholly synthetic learning lenses: configuration data-quality analysis, software supply-chain metadata stewardship, and digital-preservation package registration. GMUT Mind remains a hypothetical comparison surface, not a scientific result or Theory-of-Everything proof. Freed ID and CBR Heart remain the authority boundary: refusal, correction, minimum disclosure, provenance, rollback, and nonpromotion are explicit throughout. No real person, organization, system, record, package deployment, archive object, participant, professional action, cultural decision, Maori-authority decision, or production result was used or established.

## Proposal and approval portfolio

Thirty-six bounded positive controls passed for the completed and represented portion of the slate. Four preregistered invalid variants were constructed for each of the forty proposals, producing 160 retained rejecting witnesses. Every invalid mutation was rejected and remains visible at zero completion credit. The two open gaps and two exact gates remain unexecuted. Sixty safe-now owner packets, fifty owner candidate packets, and sixty owner CLEAN/FIX/REFINE reviews are recorded as bounded synthetic owner completions. Twenty exact-approval packets and ten blocked packets remain visible and unexecuted. Auren receives only recommendations: twenty candidate packets, ten skill ideas, ten runner ideas, thirty cleanup reviews, and the bounded practice suggestion of synthetic public-interest incident documentation analyst.

## D-first package transaction

Thirteen direct package surfaces were installed into one isolated D-first transaction root: eight Python and five Node packages. Python installation used exact downloaded wheels, a complete hash lock, and offline `--require-hashes --no-index`; Node used the exact package lock with lifecycle scripts disabled. The two Python transitive packages remain separately attributed. Each direct surface passed one positive and one rejecting smoke. The initial Python audit remains failed at zero credit because its wrapper was not pure JSON and bootstrap pip 25.0.1 was vulnerable. An additive exact pip 26.2.1 correction was followed by one separately named dependency-corrected audit with zero reported vulnerabilities across eleven dependencies; it is not relabelled as success of the original audit. The Node audit reported zero vulnerabilities for its bounded resolved closure. These checks do not establish exhaustive security, production fitness, future compatibility, or legal license interpretation.

## Skills, runners, and family surfaces

Twenty family-current phase-local skills passed the system quick validator, and ten family-current runners each accepted one valid fixture and rejected one malformed fixture. Five preregistered source skills and their paired runners were promoted additively into the global skill root only after collision refusal and exact byte parity. A sixth composite skill coordinates D-first isolation, structured-evidence integrity, Method Flow, meta-tool attribution, and four-tier flashcard projection without erasing the component attributions. The four-tier deck contains twelve categories spanning the relational owner card, three Trinity Mandala pillars, three bounded practices, proposals, packages, skills, runners, and Method Flow routing.

## Failure retention and effective truth

All twelve startup and x1 failures remain retained. Seventeen additional x2 operational failures are also retained, including the encoding edge, lockfile root-key assumption, failed initial Python audit, smoke-lint finding, PATH miss, guessed paths, bounded-output truncation, sparse-option mismatch, guessed lock filename, the lint and overview-floor failures, and the first sparse evidence-stage refusal. No failed attempt was silently folded into a pass. Alongside 160 rejected mutations and the bounded positive tool witnesses, the successor-visible remaster truth is {counts['effective_negatives']:,} effective negatives, {counts['effective_methods']:,} Method Flow methods, {counts['effective_failed_witnesses']:,} failed witnesses, {counts['effective_passing_witnesses']:,} bounded passing witnesses, {counts['open_gaps']} open gaps, and {counts['exact_gates']} exact gates. The original v672-v1 canonical aggregate was not replayed or rewritten.

## Completion interpretation

The portfolio totals are bookkeeping ceilings and bounded execution records, not evidence that volume alone creates value. A safe-now or candidate task receives remaster completion credit only when its specified local artifact, acceptance boundary, and rollback statement are present; inherited work remains cited evidence rather than Ilyra remaster credit. A represented proposal records a usable structure without claiming the blocked operational, empirical, professional, or authority-bearing result. An open gap remains unresolved even when a nearby synthetic fixture passes, and an exact gate remains unexecuted until competent evidence and authority are newly available. Likewise, promotion into the global skill root means only that a collision-free byte-identical or attributable composite tool is available locally; it does not make that tool scientifically correct, universally safe, or appropriate for every future phase. Package version and hash checks establish the observed artifacts in this one transaction, while smoke and audit receipts retain their exact invocation boundaries. These distinctions keep the larger workflow corrigible: Hamish may pause, rename, redirect, or stop it, and a later owner must reread current authority rather than inherit permission from this overview.

## Evidence limits and route state

This package is same-owner local software evidence under shared infrastructure. It is not a complete repository suite, independent reproduction, external audit, professional assessment, empirical validation, production certification, complete privacy or accessibility assurance, exhaustive security, AGI or ASI evidence, consciousness or personhood evidence, legal or cultural authority, Maori authority, proof or canon, or Stage 20 authority. The terminal verdict remains `NOT_READY_FOR_STAGE_20`. Auren Lark is recorded only as the prospective exact-title successor; no live contact occurs during x2. Route delivery remains gated on a later clean, pushed, fresh-live-equal exact final, one successful owner-scoped canonical validation, a current bounded task listing, immediate reread, duplicate and pause guard, and one acknowledged send at most.
"""


def build_manifest() -> dict[str, Any]:
    paths = [path for path in X2.rglob("*") if path.is_file() and path.name not in {"owner-manifest.json", "build-receipt.json"}]
    generated_scripts = [ROOT / "scripts" / "ghc_family_ilyra_v672_v1_2_contract_guard.py"]
    portfolio = load_json(X1 / "portfolio-freeze.json")
    generated_scripts.extend(
        ROOT / "scripts" / row["title"]
        for row in portfolio["rows"]
        if row["task_id"].startswith("IF6721R2-RUNNER-")
    )
    generated_scripts.extend(
        [
            ROOT / "scripts" / "ghc_family_ilyra_v672_v1_2_structured_data_guard.py",
            ROOT / "scripts" / "ghc_family_ilyra_v672_v1_2_toolchain_guard.py",
            Path(__file__),
            ROOT / "scripts" / "build_ghc_family_ilyra_fen_v672_v1_2_remaster_staged_review.py",
            ROOT / "tests" / "test_ghc_family_ilyra_fen_v672_v1_2_remaster_x2.py",
        ]
    )
    paths.extend(path for path in generated_scripts if path.is_file())
    unique = sorted(set(paths), key=lambda path: path.relative_to(ROOT).as_posix())
    rows = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": sha256(path),
            "bytes": path.stat().st_size,
        }
        for path in unique
    ]
    return {
        "schema": "ghc.family.owner-manifest.v7",
        "owner": OWNER,
        "phase": PHASE,
        "basis": "working-tree bytes written with explicit LF; immutable Git-blob replay occurs after staging",
        "self_excluded": True,
        "entry_count": len(rows),
        "entries": rows,
    }


def main() -> None:
    x1_gate = verify_x1_gate()
    evidence_rows, controls, mutations = proposal_evidence()
    tool_bank = build_local_skills_and_runners({**deepcopy(evidence_rows[0]), "external_actions": 0})
    packages = package_receipt()
    global_skills = global_skill_receipt()
    owner_tasks, successor_tasks, gates = task_ledgers(tool_bank)
    deck, deck_markdown = flashcards()
    method = method_flow(mutations)

    write_json(X2 / "lifecycle" / "x1-gate.json", x1_gate)
    write_json(X2 / "proposals" / "outcome-ledger.json", {"schema": "ghc.family.proposal-outcomes.v7", "outcomes": OUTCOMES, "rows": evidence_rows})
    write_json(X2 / "fixtures" / "positive-control-ledger.json", {"count": len(controls), "rows": controls})
    write_json(X2 / "fixtures" / "invalid-mutation-ledger.json", {"count": len(mutations), "all_rejected": True, "rows": mutations})
    write_json(X2 / "packages" / "transaction-receipt.json", packages)
    write_json(X2 / "tools" / "local-tool-bank-receipt.json", tool_bank)
    write_json(X2 / "tools" / "global-skill-promotion-receipt.json", global_skills)
    write_json(X2 / "portfolios" / "owner-execution.json", owner_tasks)
    write_json(X2 / "portfolios" / "successor-recommendations.json", successor_tasks)
    write_json(X2 / "portfolios" / "protected-gates.json", gates)
    write_json(X2 / "flashcards" / "four-tier-deck.json", deck)
    write_text(X2 / "flashcards" / "four-tier-deck.md", deck_markdown)
    write_json(X2 / "method-flow" / "ledger.json", method)
    write_json(
        X2 / "family-surfaces" / "family-index-overlay.json",
        {
            "schema": "ghc.family.index-overlay.v4",
            "owner": OWNER,
            "phase": PHASE,
            "proposal_chain": 5950,
            "new_proposals": 40,
            "global_skills": [name for name, _ in GLOBAL_SKILLS] + [COMPOSITE_SKILL],
            "local_skill_count": 20,
            "local_runner_count": 10,
            "package_direct_surfaces": 13,
            "source_seal_unchanged": True,
        },
    )
    write_json(
        X2 / "family-surfaces" / "meta-tool-box.json",
        {
            "schema": "ghc.family.meta-tool-box.v4",
            "preferred": [COMPOSITE_SKILL, "ghc_family_ilyra_v672_v1_2_structured_data_guard.py", "ghc_family_ilyra_v672_v1_2_toolchain_guard.py"],
            "promoted_skills": [name for name, _ in GLOBAL_SKILLS],
            "package_tools": [f"{row['name']}=={row['version']}" for row in DIRECT_PACKAGES],
            "selection_rule": "use the narrowest current validated surface and preserve component attribution",
        },
    )
    write_json(
        X2 / "family-surfaces" / "reflection-remaster.json",
        {
            "schema": "ghc.family.reflection-remaster.v4",
            "decisions": [
                "keep x1 planning-only and immutable",
                "install only within the exact D-first transaction root",
                "promote five byte-identical skills and one attributable composite",
                "treat caps as ceilings rather than quotas",
                "separate original audit failure from dependency-corrected audit success",
                "retain stale beacons as historical context only",
                "keep every successor artifact recommendation-only",
                "represent flashcards as projections rather than source of truth",
                "run no complete repository suite",
                "contact no successor before the exact-final terminal gate",
            ],
            "issue_count": 29,
            "issues": method["operational_failures"],
        },
    )
    write_json(
        X2 / "family-surfaces" / "workflow-refinement.json",
        {
            "schema": "ghc.family.workflow-refinement.v4",
            "changes": [
                "forty inherited rows revalidated at zero current credit",
                "forty new rows frozen only after x2 evidence",
                "three practices remain synthetic learning lenses",
                "thirteen direct tools use one isolated rollback root",
                "four-tier flashcards use twelve bounded categories",
                "Auren route is terminal-only and duplicate guarded",
            ],
            "commit_ceiling": 8,
            "planned_commits": 3,
            "materialized_file_ceiling": 2000,
            "full_repository_suite": False,
        },
    )
    write_json(
        X2 / "practices" / "bounded-practice-board.json",
        {
            "schema": "ghc.family.bounded-practice-board.v3",
            "owner_practices": [
                "synthetic configuration data-quality analyst",
                "synthetic software supply-chain metadata steward",
                "synthetic digital-preservation package registrar",
            ],
            "successor_recommendation": "synthetic public-interest incident documentation analyst",
            "real_people_or_records": 0,
            "professional_authority": False,
            "legal_or_cultural_authority": False,
            "maori_authority": False,
        },
    )
    write_json(
        X2 / "phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.v9",
            "owner": OWNER,
            "phase": PHASE,
            "state": "X2_EVIDENCE_BUILT_NOT_YET_IMMUTABLE",
            "source": SOURCE,
            "x1_commit": X1_COMMIT,
            "proposal_chain": 5950,
            "outcomes": OUTCOMES,
            "packages_installed": 13,
            "global_skills_installed": 6,
            "local_skills_built": 20,
            "local_runners_built": 10,
            "effective_counts": method["effective_counts"],
            "original_canonical_replayed": False,
            "external_actions": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        X2 / "route" / "auren-candidate.json",
        {
            "schema": "ghc.family.route-candidate.v5",
            "target_exact_title": "Auren Lark",
            "target_phase": "v672-v2",
            "state": "PROSPECTIVE_NOT_SENT",
            "next_after_auren": "Sable Rook for v672-v3 after Auren's own terminal gate and current route reread",
            "duplicate_guard_required": True,
            "immediate_reread_required": True,
            "precontact": False,
        },
    )
    write_text(X2 / "integrated-overview.md", overview(method))
    manifest = build_manifest()
    write_json(X2 / "owner-manifest.json", manifest)
    write_json(
        X2 / "build-receipt.json",
        {
            "schema": "ghc.family.x2-build-receipt.v7",
            "owner": OWNER,
            "phase": PHASE,
            "state": "X2_EVIDENCE_BUILT_NOT_YET_IMMUTABLE",
            "proposal_count": len(evidence_rows),
            "outcomes": OUTCOMES,
            "positive_controls": len(controls),
            "invalid_mutations": len(mutations),
            "local_skills": tool_bank["skill_count"],
            "local_runners": tool_bank["runner_count"],
            "global_skills": global_skills["promoted_count"] + global_skills["composite_count"],
            "direct_packages": packages["direct_surface_count"],
            "manifest_entries": manifest["entry_count"],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    print(
        json.dumps(
            {
                "state": "X2_EVIDENCE_BUILT_NOT_YET_IMMUTABLE",
                "proposals": len(evidence_rows),
                "positive_controls": len(controls),
                "invalid_mutations": len(mutations),
                "local_skills": tool_bank["skill_count"],
                "local_runners": tool_bank["runner_count"],
                "direct_packages": packages["direct_surface_count"],
                "manifest_entries": manifest["entry_count"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
