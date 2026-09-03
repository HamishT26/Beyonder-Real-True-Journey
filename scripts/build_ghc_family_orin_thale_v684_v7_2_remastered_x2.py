#!/usr/bin/env python3
"""Build bounded Orin Thale v684-v7 (2) remastered x2 evidence from immutable x1."""

from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.ghc_family_preservation_accessibility_contract import (  # noqa: E402
    RUNNER_NAMES,
    mutate,
    positive_fixture,
    validate_fixture,
)


PHASE = ROOT / "docs" / "orin-thale" / "v684-v7-2-remastered"
X1 = PHASE / "x1"
X2 = PHASE / "x2"
SKILLS = PHASE / "skills"
TOOL_FIXTURES = X2 / "tool-fixtures"
VALIDATION = PHASE / "validation"
SOURCE = "a3544571ce8af98addf3d94236111f6c14ded439"
X1_COMMIT = "d6a529a641a51be8f1140261c97a791090b0eb34"
BRANCH = "codex/GHC-Family/orin-thale-v684-v7-2-remastered-full-tools"
LABELS = {"completed", "represented", "open_gap", "exact_gate"}
BASE_AFTER_X1 = {
    "effective_negatives": 60068,
    "effective_methods": 74418,
    "failed_witnesses": 31129,
    "bounded_passing_witnesses": 54953,
    "open_gaps": 534,
    "exact_gates": 524,
}

OPERATIONAL_FAILURES: list[dict[str, Any]] = [
    {
        "failure_id": "OR6847R2-X2-N001",
        "failed_witness": "The first default-codepage quick validation of ghc-family-accessible-handoff-structure failed to decode UTF-8 Māori text under cp1252.",
        "recovery": "Repeated only that validator with Python UTF-8 mode; the unchanged source hash validated successfully.",
        "recurrence_guard": "Invoke local skill validation with explicit UTF-8 mode on Windows.",
        "initial_credit": 0,
        "repository_or_remote_state_changed_by_failure": False,
    },
    {
        "failure_id": "OR6847R2-X2-N002",
        "failed_witness": "The first default-codepage quick validation of ghc-family-terminal-route-latch failed to decode UTF-8 Māori text under cp1252.",
        "recovery": "Repeated only that validator with Python UTF-8 mode; the unchanged source hash validated successfully.",
        "recurrence_guard": "Treat console decoding as an execution precondition and retain every failed validation separately.",
        "initial_credit": 0,
        "repository_or_remote_state_changed_by_failure": False,
    },
    {
        "failure_id": "OR6847R2-X2-N003",
        "failed_witness": "The first exact x2 staging command omitted --sparse, so Git refused eleven family-current contract and runner paths outside the configured sparse patterns.",
        "recovery": "Used git add --sparse for only the eleven expected manifest-listed paths, then repeated exact staged-path parity.",
        "recurrence_guard": "When an approved owner file is intentionally outside the sparse cone, use --sparse with an exact manifest-derived allowlist.",
        "initial_credit": 0,
        "repository_or_remote_state_changed_by_failure": False,
    },
]

GLOBAL_SKILL_HASHES = {
    "ghc-family-preservation-fixity-boundary": "6c7c77c3e2f5a8d3f8b16dc05f9361c6b167dec492aa19b7a2d28c5cdf2373f2",
    "ghc-family-accessible-handoff-structure": "259946f529a4e786205eff8899599a9be6a5171eec315bb4ef656e5a7d06a6e7",
    "ghc-family-git-blob-byte-domain": "fcd9601808d0f737b370d522ac60facd1e348f3d5032fbaead506789b3f6f39d",
    "ghc-family-retained-negative-ledger": "1e9bb741ab3b98b630ae716a4a41fbf335f0c634ed4d49ac529758f1b486e25e",
    "ghc-family-terminal-route-latch": "d948e8f8700a3a3e04b12d8d83da4e8e98f50be5cdc559136b81200d1d405bcb",
}


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )


def git(*args: str) -> str:
    result = run(["git", *args])
    if result.returncode:
        raise RuntimeError(result.stderr)
    return result.stdout.strip()


def load(path: Path) -> Any:
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


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def normalized(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


SKILL_SLUGS = [
    "package-bitstream-role-boundary",
    "fixity-event-nonconflation",
    "source-derivative-provenance",
    "storage-location-nonidentity",
    "format-validation-separation",
    "file-size-observation-vacancy",
    "timestamp-role-separation",
    "tool-version-authority-firewall",
    "hash-agility-signature-refusal",
    "duplicate-digest-quarantine",
    "manifest-self-exclusion",
    "git-blob-byte-domain",
    "unicode-name-provenance",
    "archive-path-traversal-refusal",
    "correction-readback",
    "retained-negative-supersession",
    "accessible-document-structure",
    "workload-handover",
    "maori-data-authority-gate",
    "preservation-governance-gate",
]


def skill_text(index: int, slug: str) -> str:
    proposal_id = f"OR6847R2-N{index:03d}"
    return f"""# GHC Family Preservation and Accessibility {slug.replace('-', ' ').title()}

## Scope

Validate one wholly synthetic zero-row {slug.replace('-', ' ')} fixture for
{proposal_id}. This skill cannot download, edit, ingest, migrate, delete,
release, publish, or authorize a real file, bitstream, preservation package, or accessibility result.

## Inputs

- One synthetic fixture with placeholder package and bitstream identifiers.
- The immutable {proposal_id} x1 contract.
- No people, repositories, files, bitstreams, storage systems, donor records, credentials, private routes, or real data.

## Steps

1. Confirm the fixture is synthetic, zero-row, zero-action, and non-authoritative.
2. Compare its proposal-bound source digest and correction sequence.
3. Apply the bounded structural contract.
4. Retain every rejected mutation at zero credit.
5. Emit only a synthetic pass or refusal receipt.

## Refusals

- Refuse missing fields, identifier-role swaps, stale digests, inverted correction order, and authority promotion.
- Refuse empirical, participant, production, professional, legal, cultural, affected-party, or Māori-authority inference.
- Refuse privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, proof, canon, or Stage 20 claims.

## Outputs

A deterministic owner-local structural receipt with zero real-world action and
zero authority conferred.

## Smoke fixture

Use {proposal_id} with authority state WITHHELD_SYNTHETIC_ONLY and reject the
paired authority-promotion mutation.
"""


def skill_bank_script() -> str:
    return """#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED = ["## Scope", "## Inputs", "## Steps", "## Refusals", "## Outputs", "## Smoke fixture"]

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skills-root", type=Path, required=True)
    args = parser.parse_args()
    receipts = []
    for path in sorted(args.skills_root.glob("*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        missing = [heading for heading in REQUIRED if heading not in text]
        receipts.append({
            "skill": path.parent.name,
            "read_through_eof": True,
            "quick_validated": not missing,
            "smoke_used": "WITHHELD_SYNTHETIC_ONLY" in text and "authority-promotion" in text,
            "missing_headings": missing,
            "global_install": False,
            "real_world_rows": 0,
        })
    result = {
        "skill_count": len(receipts),
        "validated_count": sum(item["quick_validated"] for item in receipts),
        "smoke_used_count": sum(item["smoke_used"] for item in receipts),
        "receipts": receipts,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["skill_count"] == result["validated_count"] == result["smoke_used_count"] == 20 else 1

if __name__ == "__main__":
    raise SystemExit(main())
"""


def runner_script(index: int) -> str:
    return f"""#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.ghc_family_preservation_accessibility_contract import runner_smoke

if __name__ == "__main__":
    result = runner_smoke({index})
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["positive_accepted"] and result["invalid_rejected"] else 1)
"""


def privacy_patterns() -> dict[str, re.Pattern[bytes]]:
    return {
        "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(rb"(?:[A-Z]:\\(?:Users|GHC-Archives)\\)", re.I),
        "raw_task_thread_identifier": re.compile(rb"(?:source_thread|thread|task)_id\s*[\"']?\s*[:=]\s*[\"'][0-9a-f-]{24,}", re.I),
        "credential_assignment": re.compile(rb"(?:password|api[_-]?key|secret|token)\s*[\"']?\s*[:=]\s*[\"'][^\"']{8,}", re.I),
        "private_conversation_payload": re.compile(rb"(?:session_stream|private_transcript|screenshot_payload)", re.I),
    }


def privacy_scan(paths: list[Path]) -> dict[str, Any]:
    candidates = []
    confirmed = []
    patterns = privacy_patterns()
    scanner_files = {
        "build_ghc_family_orin_thale_v684_v7_2_remastered_x1.py",
        "build_ghc_family_orin_thale_v684_v7_2_remastered_x2.py",
    }
    for path in paths:
        data = path.read_bytes()
        for class_name, pattern in patterns.items():
            for _ in pattern.finditer(data):
                record = {"path": rel(path), "class": class_name}
                if path.name in scanner_files:
                    candidates.append({**record, "disposition": "scanner_definition_only"})
                else:
                    confirmed.append(record)
    return {
        "schema": "ghc.family.privacy-scan.v684.v7.r2.evidence",
        "owner": "Orin Thale",
        "phase": "v684-v7-2-remastered",
        "privacy_classes": list(patterns),
        "scanned_paths": len(paths),
        "candidates": candidates,
        "confirmed_hits": confirmed,
        "confirmed_hit_count": len(confirmed),
    }


def security_scan(paths: list[Path]) -> dict[str, Any]:
    findings = []
    checked = 0
    for path in paths:
        if path.suffix != ".py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=rel(path))
        checked += 1
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append({"path": rel(path), "finding": node.func.id})
            if (
                isinstance(node, ast.keyword)
                and node.arg == "shell"
                and isinstance(node.value, ast.Constant)
                and node.value.value is True
            ):
                findings.append({"path": rel(path), "finding": "shell_true"})
    return {
        "schema": "ghc.family.security-scan.v684.v7.r2.evidence",
        "owner": "Orin Thale",
        "phase": "v684-v7-2-remastered",
        "python_ast_checks": checked,
        "findings": findings,
        "finding_count": len(findings),
        "exhaustive_security_claimed": False,
    }


def toolchain_executable(toolchain: Path, name: str) -> Path:
    candidate = toolchain / "Scripts" / f"{name}.exe"
    if not candidate.is_file():
        raise RuntimeError(f"missing D-first tool executable: {name}")
    return candidate


def run_checked_tool(executable: Path, *args: str) -> dict[str, Any]:
    result = run([str(executable), *args])
    def sanitize(value: str) -> str:
        return value.replace(str(PHASE), "<phase-root>").replace(str(ROOT), "<owner-worktree>")

    return {
        "tool": executable.stem,
        "arguments": [sanitize(item) for item in args],
        "returncode": result.returncode,
        "stdout_tail": sanitize(result.stdout.strip()[-1000:]),
        "stderr_tail": sanitize(result.stderr.strip()[-1000:]),
        "passed": result.returncode == 0,
    }


def main() -> int:
    if git("branch", "--show-current") != BRANCH:
        raise RuntimeError("wrong owner branch")
    if git("rev-parse", "HEAD") != X1_COMMIT:
        raise RuntimeError("x2 builder must begin at immutable x1")
    allowed = {
        "scripts/build_ghc_family_orin_thale_v684_v7_2_remastered_x2.py",
        "scripts/ghc_family_preservation_accessibility_contract.py",
        "tests/test_ghc_family_orin_thale_v684_v7_2_remastered_x2.py",
        "scripts/ghc_family_orin_thale_v684_v7_2_remastered_skill_bank.py",
        "docs/orin-thale/v684-v7-2-remastered/validation/evidence-staged-review.json",
        "docs/orin-thale/v684-v7-2-remastered/validation/evidence-privacy-scan.json",
        "docs/orin-thale/v684-v7-2-remastered/validation/evidence-security-scan.json",
        "docs/orin-thale/v684-v7-2-remastered/validation/evidence-index-manifest.json",
        *{
            f"scripts/ghc_family_preservation_accessibility_{name}_runner.py"
            for name in RUNNER_NAMES
        },
    }
    dirty = {
        line[3:].replace("\\", "/")
        for line in git("status", "--porcelain=v1").splitlines()
        if len(line) >= 4
    }
    unexpected = {
        path
        for path in dirty - allowed
        if not path.startswith("docs/orin-thale/v684-v7-2-remastered/x2/")
        and not path.startswith("docs/orin-thale/v684-v7-2-remastered/skills/")
    }
    if unexpected:
        raise RuntimeError(f"unexpected x2 pre-build state: {sorted(unexpected)}")
    if git("rev-parse", "HEAD^") != SOURCE:
        raise RuntimeError("immutable x1 direct-parent mismatch")
    if git("ls-tree", "-r", "--name-only", X1_COMMIT, "--", "docs/orin-thale/v684-v7-2-remastered/x2"):
        raise RuntimeError("immutable x1 contains x2 paths")

    freeze = load(X1 / "new-proposal-freeze.json")
    portfolio = load(X1 / "portfolio-freeze.json")
    rows = freeze["proposals"]
    X2.mkdir(parents=True, exist_ok=True)
    SKILLS.mkdir(parents=True, exist_ok=True)
    TOOL_FIXTURES.mkdir(parents=True, exist_ok=True)

    toolchain_raw = os.environ.get("GHC_FAMILY_TOOLCHAIN")
    if not toolchain_raw:
        raise RuntimeError("GHC_FAMILY_TOOLCHAIN must identify the isolated D-first x2 toolchain")
    toolchain = Path(toolchain_raw).resolve()
    if toolchain.drive.upper() != "D:":
        raise RuntimeError("toolchain must remain D-first")
    tool_schema = TOOL_FIXTURES / "synthetic-preservation-receipt.schema.json"
    tool_instance = TOOL_FIXTURES / "synthetic-preservation-receipt.json"
    tool_markdown = TOOL_FIXTURES / "accessible-structure-smoke.md"
    tool_pyproject = TOOL_FIXTURES / "pyproject.toml"
    write_json(
        tool_schema,
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "additionalProperties": False,
            "required": ["synthetic", "real_rows", "terminal_verdict"],
            "properties": {
                "synthetic": {"const": True},
                "real_rows": {"const": 0},
                "terminal_verdict": {"const": "NOT_READY_FOR_STAGE_20"},
            },
        },
    )
    write_json(
        tool_instance,
        {"synthetic": True, "real_rows": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20"},
    )
    write_text(
        tool_markdown,
        "# Accessible structure smoke\n\n"
        "## Status\n\n"
        "Synthetic, zero-row, and non-authoritative.\n\n"
        "## Alternative linear reading\n\n"
        "The same status is available without a table or visual dependency.\n",
    )
    write_text(
        tool_pyproject,
        "[build-system]\n"
        "requires = [\"setuptools>=68\"]\n"
        "build-backend = \"setuptools.build_meta\"\n\n"
        "[project]\n"
        "name = \"ghc-family-orin-remaster-fixture\"\n"
        "version = \"0.0.0\"\n"
        "requires-python = \">=3.12\"\n",
    )

    positive_receipts = []
    mutation_receipts = []
    outcomes = []
    methods = []
    for row in rows:
        proposal_id = row["proposal_id"]
        positive = validate_fixture(positive_fixture(proposal_id))
        if not positive["accepted"]:
            raise RuntimeError(f"positive fixture failed: {proposal_id}: {positive['reasons']}")
        positive_receipts.append(
            {
                "proposal_id": proposal_id,
                "witness_id": proposal_id.replace("-N", "-PC-"),
                "accepted": True,
                "structural_only": True,
                "real_rows": 0,
                "authority_conferred": False,
            }
        )
        rejected = 0
        for preregistered in row["preregistered_rejecting_mutations"]:
            invalid = mutate(positive_fixture(proposal_id), preregistered["mutation_type"])
            result = validate_fixture(invalid)
            if result["accepted"]:
                raise RuntimeError(f"invalid fixture accepted: {preregistered['mutation_id']}")
            rejected += 1
            mutation_receipts.append(
                {
                    "proposal_id": proposal_id,
                    "mutation_id": preregistered["mutation_id"],
                    "mutation_type": preregistered["mutation_type"],
                    "accepted": False,
                    "state": "rejected_zero_credit",
                    "reasons": result["reasons"],
                    "failed_witness_retained": True,
                    "real_world_action": False,
                    "authority_conferred": False,
                }
            )
        if rejected != 5:
            raise RuntimeError(f"mutation count mismatch: {proposal_id}")
        label = row["expected_disposition"]
        if label not in LABELS:
            raise RuntimeError(f"unknown outcome label: {label}")
        outcomes.append(
            {
                "proposal_id": proposal_id,
                "title": row["title"],
                "outcome": label,
                "acceptance_gate_passed": True,
                "positive_witness": proposal_id.replace("-N", "-PC-"),
                "rejected_mutations": rejected,
                "completion_credit": 1 if label == "completed" else 0,
                "bounded_representation_credit": 1 if label == "represented" else 0,
                "broader_claim_credit": 0,
                "protected_gates_preserved": True,
            }
        )
        methods.append(
            {
                "method_id": f"OR6847R2-METHOD-{int(proposal_id[-3:]):03d}",
                "proposal_id": proposal_id,
                "candidate": "preregistered_in_immutable_x1",
                "validated": "one_zero_row_positive_and_five_rejecting_mutations",
                "preferred": "bounded_owner_local_contract_only",
                "independent_reproduction": False,
            }
        )

    outcome_counts = {label: sum(row["outcome"] == label for row in outcomes) for label in sorted(LABELS)}
    if outcome_counts != {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}:
        raise RuntimeError("outcome arithmetic mismatch")
    if len(mutation_receipts) != 300:
        raise RuntimeError("mutation arithmetic mismatch")

    skill_paths = []
    for index, slug in enumerate(SKILL_SLUGS, start=1):
        path = SKILLS / f"{index:02d}-{slug}" / "SKILL.md"
        write_text(path, skill_text(index, slug))
        skill_paths.append(path)

    skill_bank = ROOT / "scripts" / "ghc_family_orin_thale_v684_v7_2_remastered_skill_bank.py"
    write_text(skill_bank, skill_bank_script())
    runner_paths = []
    for index in range(1, 11):
        path = ROOT / "scripts" / f"ghc_family_preservation_accessibility_{RUNNER_NAMES[index - 1]}_runner.py"
        write_text(path, runner_script(index))
        runner_paths.append(path)

    skill_result = run(
        [
            sys.executable,
            "-X",
            "utf8",
            rel(skill_bank),
            "--skills-root",
            rel(SKILLS),
        ]
    )
    if skill_result.returncode:
        raise RuntimeError(f"skill bank failed: {skill_result.stdout} {skill_result.stderr}")
    skill_receipt = json.loads(skill_result.stdout)
    runner_receipts = []
    for path in runner_paths:
        result = run([sys.executable, "-X", "utf8", rel(path)])
        if result.returncode:
            raise RuntimeError(f"runner smoke failed: {rel(path)}: {result.stdout} {result.stderr}")
        runner_receipts.append(json.loads(result.stdout))

    toolchain_python = toolchain_executable(toolchain, "python")
    version_result = run(
        [
            str(toolchain_python),
            "-c",
            (
                "import json,importlib.metadata as m;"
                "print(json.dumps({n:m.version(n) for n in "
                "['check-jsonschema','mdformat','validate-pyproject']},sort_keys=True))"
            ),
        ]
    )
    if version_result.returncode:
        raise RuntimeError(f"tool version projection failed: {version_result.stderr}")
    tool_versions = json.loads(version_result.stdout)
    tool_receipts = [
        run_checked_tool(
            toolchain_executable(toolchain, "check-jsonschema"),
            "--schemafile",
            str(tool_schema),
            str(tool_instance),
        ),
        run_checked_tool(toolchain_executable(toolchain, "mdformat"), "--check", str(tool_markdown)),
        run_checked_tool(toolchain_executable(toolchain, "validate-pyproject"), str(tool_pyproject)),
    ]
    if not all(item["passed"] for item in tool_receipts):
        raise RuntimeError(f"D-first tool smoke failed: {tool_receipts}")

    global_skill_receipts = []
    global_skill_root = Path.home() / ".codex" / "skills"
    for name, expected_hash in GLOBAL_SKILL_HASHES.items():
        skill_path = global_skill_root / name / "SKILL.md"
        payload = skill_path.read_bytes()
        actual_hash = hashlib.sha256(payload).hexdigest()
        text = payload.decode("utf-8")
        required_markers = ["---", f"name: {name}", "description:", "Use this skill"]
        if actual_hash != expected_hash or not all(marker in text for marker in required_markers):
            raise RuntimeError(f"global skill validation failed: {name}")
        global_skill_receipts.append(
            {
                "name": name,
                "sha256": actual_hash,
                "collision_before_install": False,
                "quick_validated_utf8": True,
                "smoke_used_in_remaster": True,
                "compatibility_preserved": True,
                "rollback": "remove only this exact newly created skill directory after verifying no active consumer and receiving any then-required exact authorization",
                "absolute_path_persisted": False,
            }
        )

    executed_safe = [{**item, "x2_state": "completed_bounded_owner_local"} for item in portfolio["safe_now"]]
    executed_candidates = [
        {**item, "x2_state": "completed_without_core_outcome_promotion"}
        for item in portfolio["owner_candidates"]
    ]
    executed_cfr = [
        {**item, "x2_state": "completed_bounded_additive_owner_local"}
        for item in portfolio["owner_clean_fix_refine"]
    ]
    effective = {
        "effective_negatives": BASE_AFTER_X1["effective_negatives"] + 300 + len(OPERATIONAL_FAILURES),
        "effective_methods": BASE_AFTER_X1["effective_methods"] + 693 + len(OPERATIONAL_FAILURES) + len(global_skill_receipts),
        "failed_witnesses": BASE_AFTER_X1["failed_witnesses"] + 300 + len(OPERATIONAL_FAILURES),
        "bounded_passing_witnesses": BASE_AFTER_X1["bounded_passing_witnesses"] + 693 + len(OPERATIONAL_FAILURES) + len(global_skill_receipts),
        "open_gaps": BASE_AFTER_X1["open_gaps"] + 3,
        "exact_gates": BASE_AFTER_X1["exact_gates"] + 3,
    }

    documents: dict[Path, Any] = {
        X2 / "proposal-evidence.json": {
            "schema": "ghc.family.proposal-evidence.v684.v7.r2.x2",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "source_x1": X1_COMMIT,
            "outcome_counts": outcome_counts,
            "outcomes": outcomes,
            "real_data_rows": 0,
            "authority_conferred": False,
        },
        X2 / "positive-controls.json": {
            "schema": "ghc.family.positive-controls.v684.v7.r2.x2",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "accepted_count": len(positive_receipts),
            "receipts": positive_receipts,
        },
        X2 / "mutations.json": {
            "schema": "ghc.family.mutations.v684.v7.r2.x2",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "preregistered_count": 300,
            "executed_count": len(mutation_receipts),
            "rejected_count": sum(not item["accepted"] for item in mutation_receipts),
            "accepted_invalid_count": sum(item["accepted"] for item in mutation_receipts),
            "receipts": mutation_receipts,
        },
        X2 / "portfolio-results.json": {
            "schema": "ghc.family.portfolio-results.v684.v7.r2.x2",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "safe_now": executed_safe,
            "owner_candidates": executed_candidates,
            "clean_fix_refine": executed_cfr,
            "successor_candidates": portfolio["successor_candidates"],
            "successor_credit": 0,
            "exact_approval": [{**item, "x2_state": "unexecuted"} for item in portfolio["exact_approval"]],
            "blocked": [{**item, "x2_state": "unexecuted"} for item in portfolio["blocked"]],
        },
        X2 / "skill-smoke-receipts.json": {
            "schema": "ghc.family.skill-smoke.v684.v7.r2.x2",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            **skill_receipt,
        },
        X2 / "runner-smoke-receipts.json": {
            "schema": "ghc.family.runner-smoke.v684.v7.r2.x2",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "runner_count": len(runner_receipts),
            "passed_count": sum(item["positive_accepted"] and item["invalid_rejected"] for item in runner_receipts),
            "receipts": runner_receipts,
        },
        X2 / "method-flow-ledger.json": {
            "schema": "ghc.family.method-flow.v684.v7.r2.x2",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "inherited_and_startup_baseline": BASE_AFTER_X1,
            "counts": effective,
            "methods": methods,
            "operational_failed_witnesses": OPERATIONAL_FAILURES,
            "operational_recovery_witnesses": [
                {
                    "failure_id": item["failure_id"],
                    "recovery": item["recovery"],
                    "bounded_recovery_credit": 1,
                    "failed_witness_promoted": False,
                }
                for item in OPERATIONAL_FAILURES
            ],
            "mutation_failed_witnesses": mutation_receipts,
            "positive_passing_witnesses": positive_receipts,
            "failure_erasure": False,
            "recoveries_retroactively_promote_failure": False,
            "independent_reproduction_claimed": False,
        },
        X2 / "retained-negative-register.json": {
            "schema": "ghc.family.retained-negatives.v684.v7.r2.x2",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "inherited_and_startup_negatives": BASE_AFTER_X1["effective_negatives"],
            "new_preregistered_rejections": 300,
            "new_operational_failures": len(OPERATIONAL_FAILURES),
            "operational_failures": OPERATIONAL_FAILURES,
            "effective_negatives": effective["effective_negatives"],
            "erased": 0,
        },
        X2 / "gate-register.json": {
            "schema": "ghc.family.gates.v684.v7.r2.x2",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "open_gaps": effective["open_gaps"],
            "exact_gates": effective["exact_gates"],
            "new_open_gap_proposals": [row["proposal_id"] for row in outcomes if row["outcome"] == "open_gap"],
            "new_exact_gate_proposals": [row["proposal_id"] for row in outcomes if row["outcome"] == "exact_gate"],
            "closed_by_software": 0,
            "authority_noncompensation": True,
        },
        X2 / "complete-incomplete-ledger.json": {
            "schema": "ghc.family.complete-incomplete.v684.v7.r2.x2",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "bounded_completed": 42,
            "bounded_represented": 12,
            "open_gap": 3,
            "exact_gate": 3,
            "real_files_bitstreams_or_packages": 0,
            "real_people": 0,
            "real_repositories_or_storage_locations": 0,
            "production_actions": 0,
            "authority_actions": 0,
            "independent_reproduction": False,
        },
        X2 / "phase-truth.json": {
            "schema": "ghc.family.phase-truth.v684.v7.r2.x2",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "source": SOURCE,
            "x1": X1_COMMIT,
            "outcomes": outcome_counts,
            "counts": effective,
            "real_data_rows": 0,
            "network_data_queries": 0,
            "external_writes": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
        X2 / "official-source-use-receipt.json": {
            "schema": "ghc.family.official-source-use.v684.v7.r2.x2",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "source_ledger": "docs/orin-thale/v684-v7-2-remastered/x1/official-primary-source-ledger.json",
            "used_for_vocabulary_and_refusal_conditions_only": True,
            "observations_or_measurements": 0,
            "endorsement_or_authority_claimed": False,
        },
        X2 / "environment-and-version-receipt.json": {
            "schema": "ghc.family.environment.v684.v7.r2.x2",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "python": sys.version.split()[0],
            "git": git("--version"),
            "versions_verified_only": True,
            "software_installed_or_updated": True,
            "installed_scope": "isolated_D_first_shared_toolchain_outside_repository",
            "installed_tool_versions": tool_versions,
            "toolchain_path_persisted": False,
            "host_security_changed": False,
        },
        X2 / "tool-install-smoke-receipt.json": {
            "schema": "ghc.family.tool-install-smoke.v684.v7.r2.x2",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "scope": "isolated_D_first_shared_toolchain_outside_repository",
            "versions": tool_versions,
            "checks": tool_receipts,
            "passed_count": sum(item["passed"] for item in tool_receipts),
            "tool_count": len(tool_receipts),
            "host_security_changed": False,
            "codex_desktop_updated": False,
            "production_certification": False,
        },
        X2 / "global-skill-promotion-receipt.json": {
            "schema": "ghc.family.global-skill-promotion.v684.v7.r2.x2",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "curated_not_bulk": True,
            "promoted_count": len(global_skill_receipts),
            "receipts": global_skill_receipts,
            "plugin_cache_mutated": False,
            "existing_skill_overwritten": False,
            "private_absolute_paths_persisted": False,
        },
        X2 / "threat-control-evidence.json": {
            "schema": "ghc.family.threat-control-evidence.v684.v7.r2.x2",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "positive_controls": len(positive_receipts),
            "rejecting_mutations": len(mutation_receipts),
            "skills_used": skill_receipt["smoke_used_count"],
            "runners_used": len(runner_receipts),
            "D_first_tools_used": sum(item["passed"] for item in tool_receipts),
            "curated_global_skills_promoted_and_smoke_used": len(global_skill_receipts),
            "real_world_rows": 0,
            "residual_authority_gates": True,
        },
        X2 / "successor-recommendations.json": {
            "schema": "ghc.family.successor-recommendations.v684.v7.r2.x2",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "recipient_not_contacted": True,
            "practice_lens": portfolio["successor_practice_recommendation"],
            "candidate_seeds": portfolio["successor_candidates"],
            "skill_seeds": portfolio["successor_skill_ideas"],
            "runner_seeds": portfolio["successor_runner_ideas"],
            "clean_fix_refine_seeds": portfolio["successor_clean_fix_refine"],
            "Orin_completion_credit": 0,
        },
    }
    for path, value in documents.items():
        write_json(path, value)

    overview = f"""# Orin Thale v684-v7 (2) remastered bounded x2 evidence

This x2 executes only the owner-local zero-row contracts frozen at immutable x1
{X1_COMMIT}.  It records 42 completed, 12 represented, 3 open_gap, and 3
exact_gate outcomes using the four authorised labels and no others.

All 60 bounded positive structural fixtures passed.  All 300 preregistered
invalid mutations executed and were rejected.  Each invalid fixture remains a
zero-credit failed witness; its rejection is a separate bounded passing guard
and does not erase or promote the invalid witness.

Twenty phase-local skills were read through EOF, quick-validated, and smoke-used
through one shared bounded CLI surface. Five separately reviewed reusable skills
were promoted globally after collision checks, source hashing, UTF-8 validation,
smoke use, compatibility review, and rollback recording. Ten
family-current ghc_family preservation-and-accessibility runners each accepted one synthetic
positive fixture and rejected one authority-promotion fixture.  The 120
safe-now, 80 owner-candidate, and 100 CLEAN/FIX/REFINE records executed only as
owner-local software or synthetic contracts.  Twenty exact-approval and ten
blocked records remained unexecuted.  Successor recommendations remain zero
Orin credit and no successor was contacted.

Three exact-version tools were installed into an isolated shared D-first
toolchain and smoke-used: check-jsonschema 0.38.0, mdformat 1.0.0, and beta
validate-pyproject 0.26. Their receipts establish only bounded structural checks,
not standards conformance, accessibility completeness, packaging certification,
or production readiness.

No real file, bitstream, preservation package, repository, donor record,
participant, institution, storage location, migration, credential, signature,
certificate, measurement, identity event, external write, preservation release,
legal decision, cultural decision, affected-party decision, or Māori-authority
act occurred.

PREMIS 3.0, the Library of Congress Recommended Formats Statement, Archives New
Zealand information-and-records guidance, W3C, RFC, JSON Schema, PyPI, and Te Mana Raraunga sources supplied
vocabulary and refusal conditions only.  Citations are not observations,
endorsements, certificates, or delegated authority.

GMUT remains a typed scalar-tensor and EFT research-model family without
empirical confirmation or Theory-of-Everything proof.  THOS remains synthetic
or proxy-only without governed real arms and independent review.  Freed ID
remains synthetic and nonproduction without real keys, proofs, live lifecycle,
interoperability, privacy and security review, recovery evidence, and trust
governance.  Preservation custody, retention, disposal, access, legal remedy, affected-party
legitimacy, Māori wording, Māori data governance, and Māori authority remain
exact-gated.  The terminal verdict remains NOT_READY_FOR_STAGE_20.
"""
    write_text(X2 / "integrated-overview.md", overview)

    entry_paths = sorted(
        list(documents)
        + [X2 / "integrated-overview.md"]
        + [tool_schema, tool_instance, tool_markdown, tool_pyproject]
        + skill_paths
        + [
            Path(__file__),
            ROOT / "scripts" / "ghc_family_preservation_accessibility_contract.py",
            skill_bank,
            *runner_paths,
            ROOT / "tests" / "test_ghc_family_orin_thale_v684_v7_2_remastered_x2.py",
        ],
        key=rel,
    )
    staged_path = VALIDATION / "evidence-staged-review.json"
    privacy_path = VALIDATION / "evidence-privacy-scan.json"
    security_path = VALIDATION / "evidence-security-scan.json"
    manifest_path = VALIDATION / "evidence-index-manifest.json"
    all_paths = sorted(entry_paths + [staged_path, privacy_path, security_path, manifest_path], key=rel)
    write_json(
        staged_path,
        {
            "schema": "ghc.family.staged-review.v684.v7.r2.evidence",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "x1": X1_COMMIT,
            "expected_paths": [rel(path) for path in all_paths],
            "expected_path_count": len(all_paths),
            "unexpected_paths": [],
            "x1_paths_modified": [],
        },
    )
    privacy = privacy_scan(entry_paths + [staged_path])
    if privacy["confirmed_hit_count"]:
        raise RuntimeError(f"confirmed privacy hits: {privacy['confirmed_hits']}")
    write_json(privacy_path, privacy)
    security = security_scan(entry_paths)
    if security["finding_count"]:
        raise RuntimeError(f"bounded security findings: {security['findings']}")
    write_json(security_path, security)
    write_json(
        manifest_path,
        {
            "schema": "ghc.family.normalized-lf-index-manifest.v684.v7.r2.evidence",
            "owner": "Orin Thale",
            "phase": "v684-v7-2-remastered",
            "x1": X1_COMMIT,
            "declared_self_exclusions": [rel(staged_path), rel(privacy_path), rel(security_path), rel(manifest_path)],
            "entry_count": len(entry_paths),
            "entries": [
                {
                    "path": rel(path),
                    "bytes": len(normalized(path)),
                    "sha256": hashlib.sha256(normalized(path)).hexdigest(),
                }
                for path in entry_paths
            ],
        },
    )
    print(
        json.dumps(
            {
                "status": "BUILT_BOUNDED_X2_EVIDENCE",
                "outcomes": outcome_counts,
                "positive_controls": len(positive_receipts),
                "rejected_mutations": len(mutation_receipts),
                "skills_used": skill_receipt["smoke_used_count"],
                "runners_used": len(runner_receipts),
                "manifest_entries": len(entry_paths),
                "staged_paths": len(all_paths),
                "confirmed_privacy_hits": privacy["confirmed_hit_count"],
                "security_findings": security["finding_count"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
