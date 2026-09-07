"""Validate and manifest Tamar v688-v3 planning-only x1."""
from __future__ import annotations

import ast
import collections
import hashlib
import json
import os
import pathlib
import re
import subprocess


ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = ROOT / "docs/tamar-vey/v688-v3"
BANK = pathlib.Path(os.environ["GHC_OWNER_BANK"])
SOURCE = "c4c676d81235bc6e453bb867b0c0f0de121b7733"
PREFIX = "docs/tamar-vey/v688-v3/"
SCRIPT_PREFIX = "scripts/tamar_vey_v688_v3/"
MANIFEST = PREFIX + "validation/x1-manifest.json"
STAGED = PREFIX + "validation/x1-staged-review.json"
CHECKS = PREFIX + "validation/x1-checks.json"
PRIVACY = PREFIX + "validation/x1-privacy.json"
PATTERNS = {
    "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b"),
    "private_local_path": re.compile(r"(?i)\b[A-Z]:[\\/]"),
    "private_uri": re.compile(r"(?:codex|app|thread|session)://"),
    "delegation_markup": re.compile(r"<(?:codex_delegation|source_thread_id)>"),
    "credential_assignment": re.compile(r"(?i)(?:api_key|password|secret)\s*[:=]\s*[\"'][A-Za-z0-9_+/=-]{16,}"),
}


def pairs(sequence):
    result = {}
    for key, value in sequence:
        if key in result:
            raise ValueError("DUPLICATE_KEY")
        result[key] = value
    return result


def strict(raw):
    return json.loads(
        raw,
        object_pairs_hook=pairs,
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError("NONFINITE")),
    )


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def write(relative, value):
    path = BASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def git(*args):
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        timeout=45,
    ).stdout.decode("utf-8").strip()


def owner_files(include_manifest=True):
    paths = []
    for root in [BASE, ROOT / "scripts/tamar_vey_v688_v3"]:
        if root.exists():
            paths.extend(path for path in root.rglob("*") if path.is_file() and "__pycache__" not in path.parts)
    relative = sorted({path.relative_to(ROOT).as_posix() for path in paths})
    if not include_manifest:
        relative = [path for path in relative if path != MANIFEST]
    return relative


def privacy_scan(paths):
    candidates = []
    confirmed = []
    for relative in paths:
        text = (ROOT / relative).read_text(encoding="utf-8")
        for kind, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                reason = None
                if relative.endswith("validate_ghc_family_font_x1.py"):
                    reason = "scanner_definition"
                elif kind == "private_local_path" and match.group(0).upper() in {"C:/", "D:/", "C:\\", "D:\\"}:
                    reason = "generic_drive_root_policy_literal"
                item = {"path": relative, "class": kind, "offset": match.start(), "classification": reason or "confirmed"}
                candidates.append(item)
                if reason is None:
                    confirmed.append(item)
    return candidates, confirmed


def main():
    if git("rev-parse", "HEAD") != SOURCE:
        raise RuntimeError("x1 validation requires the exact immutable Orren final")
    if (BASE / "x2").exists():
        raise RuntimeError("x1 validation refuses an x2 tree")
    if (BANK / "environment").exists():
        raise RuntimeError("Package environment exists before x1 freeze")

    proposals = strict((BASE / "x1/new-proposals.json").read_text(encoding="utf-8"))
    rows = proposals["proposals"]
    if proposals["count"] != len(rows) or len(rows) != 200 or not proposals["planning_only"]:
        raise RuntimeError("Proposal count or planning state mismatch")
    if proposals["chain_before"] != 15830 or proposals["chain_after"] != 16030:
        raise RuntimeError("Proposal chain mismatch")
    if len({row["proposal_id"] for row in rows}) != 200 or len({row["title"] for row in rows}) != 200:
        raise RuntimeError("Proposal identifiers or titles are not unique")
    if len({sha(row["input"]) for row in rows}) != 200:
        raise RuntimeError("Proposal complete inputs are not unique")
    outcomes = collections.Counter(row["expected_execution_disposition"] for row in rows)
    if outcomes != {"completed": 178, "represented": 17, "open_gap": 2, "exact_gate": 3}:
        raise RuntimeError(f"Outcome planning mismatch: {outcomes}")

    required = {
        "proposal_id",
        "operation",
        "title",
        "input",
        "expected_output",
        "expected_execution_disposition",
        "approval_class",
        "concrete_artifact",
        "execution_lane",
        "external_credit",
        "falsifier_or_acceptance_gate",
        "hypothesis",
        "null_or_failure_condition",
        "pillar",
        "practice",
        "protected_gates",
        "rollback_or_recovery",
        "schema",
        "skill",
        "source_kind",
        "source_status",
    }
    if any(not required.issubset(row) for row in rows):
        raise RuntimeError("Proposal required-field mismatch")

    inherited = strict((BASE / "x1/inherited-review.json").read_text(encoding="utf-8"))
    if inherited["count"] != 200 or len(inherited["rows"]) != 200:
        raise RuntimeError("Inherited review count mismatch")
    if any(row["novelty_credit"] != 0 or row["completion_credit"] != 0 for row in inherited["rows"]):
        raise RuntimeError("Inherited review received credit")
    novelty = strict((BASE / "x1/novelty-review.json").read_text(encoding="utf-8"))
    if novelty["universal_novelty_claimed"] or len(novelty["reviews"]) != 200:
        raise RuntimeError("Novelty scope mismatch")
    if any(row["exact_title_collision"] or row["exact_input_collision"] or row["token_jaccard"] >= 0.78 for row in novelty["reviews"]):
        raise RuntimeError("Novelty quarantine remains")

    portfolio = strict((BASE / "x1/portfolio-plan.json").read_text(encoding="utf-8"))
    expected_counts = {"safe": 300, "candidates": 250, "clean_fix_refine": 300, "exact_packets": 50, "blocked_packets": 30}
    if portfolio["counts"] != expected_counts:
        raise RuntimeError("Portfolio count declaration mismatch")
    if any(len(portfolio[key]) != value for key, value in expected_counts.items()):
        raise RuntimeError("Portfolio array count mismatch")
    if any(row["executed"] for row in portfolio["exact_packets"] + portfolio["blocked_packets"]):
        raise RuntimeError("Held packet was executed in x1")
    release_validation = strict((BASE / "x1/tooling/release-profile-validation.json").read_text(encoding="utf-8"))
    if release_validation["status"] != "PASS" or release_validation["issues"]:
        raise RuntimeError("Current release-profile validation failed")
    reconciliation = strict((BASE / "x1/tooling/workflow-plan-current-release-reconciliation.json").read_text(encoding="utf-8"))
    if reconciliation["legacy_workflow_audit"]["policy_checks_passed"] != 19 or reconciliation["current_release_profile"]["profile_validation"] != "PASS":
        raise RuntimeError("Workflow reconciliation mismatch")

    plan = strict((BASE / "x1/skill-runner-plan.json").read_text(encoding="utf-8"))
    if len(plan["skills"]) != 10 or len(plan["runners"]) != 5 or plan["global_overwrites_allowed"]:
        raise RuntimeError("Skill or runner plan mismatch")
    global_skill_root = pathlib.Path.home() / ".codex" / "skills"
    global_runner_root = pathlib.Path.home() / ".codex" / "scripts"
    collisions = [row["name"] for row in plan["skills"] if (global_skill_root / row["name"]).exists()]
    collisions += [row["name"] for row in plan["runners"] if (global_runner_root / row["name"]).exists()]
    if (global_runner_root / plan["shared_core"]).exists():
        collisions.append(plan["shared_core"])
    if collisions:
        raise RuntimeError("Global destination collision: " + ", ".join(collisions))

    wheel_plan = strict((BASE / "x1/wheel-readback.json").read_text(encoding="utf-8"))
    if len(wheel_plan["rows"]) != 3 or wheel_plan["package_code_executed"]:
        raise RuntimeError("Wheel plan mismatch")
    for row in wheel_plan["rows"]:
        path = BANK / "wheels" / row["wheel"]
        raw = path.read_bytes()
        if len(raw) != row["bytes"] or hashlib.sha256(raw).hexdigest() != row["sha256"] or row["installed"]:
            raise RuntimeError("Wheel readback mismatch: " + row["name"])

    ledger = strict((BASE / "x1/method-flow/ledger.json").read_text(encoding="utf-8"))
    if len(ledger["methods"]) != ledger["counts"]["methods"] or len(ledger["witnesses"]) != ledger["counts"]["witnesses"]:
        raise RuntimeError("Method Flow count mismatch")
    if collections.Counter(witness["result"] for witness in ledger["witnesses"]) != ledger["counts"]["witness_results"]:
        raise RuntimeError("Method Flow witness result mismatch")
    if any(method["recommendation_state"] != "preferred" for method in ledger["methods"]):
        raise RuntimeError("Startup recovery method lacks preferred state")

    initial_paths = owner_files(include_manifest=False)
    json_count = 0
    ast_count = 0
    largest_words = 0
    security_findings = []
    for relative in initial_paths:
        path = ROOT / relative
        text = path.read_text(encoding="utf-8")
        largest_words = max(largest_words, len(text.split()))
        if path.suffix == ".json":
            strict(text)
            json_count += 1
        if path.suffix == ".py":
            tree = ast.parse(text, filename=relative)
            ast_count += 1
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "compile", "__import__"}:
                        security_findings.append({"path": relative, "line": node.lineno, "finding": "dynamic_execution"})
                    if any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                        security_findings.append({"path": relative, "line": node.lineno, "finding": "shell_true"})
    if largest_words >= 100000 or security_findings:
        raise RuntimeError("Word ceiling or bounded code review failed")

    candidates, confirmed = privacy_scan(initial_paths)
    if confirmed:
        raise RuntimeError("Confirmed private material found before x1 staging")
    write(
        "validation/x1-privacy.json",
        {
            "schema": "ghc.family.five-class-privacy-adjudication.v1",
            "classes": list(PATTERNS),
            "scanned_files": len(initial_paths),
            "candidates": candidates,
            "candidate_count": len(candidates),
            "confirmed_hits": [],
            "confirmed_hit_count": 0,
            "same_owner_only": True,
        },
    )
    write(
        "validation/x1-checks.json",
        {
            "schema": "ghc.family.font-x1-checks.v1",
            "source": SOURCE,
            "planning_contracts": 200,
            "inherited_reviews": 200,
            "safe_procedures": 300,
            "candidate_procedures": 250,
            "clean_fix_refine": 300,
            "exact_packets": 50,
            "blocked_packets": 30,
            "skills_planned": 10,
            "runners_planned": 5,
            "packages_downloaded_hash_matched": 3,
            "packages_installed": 0,
            "x2_tree_present": False,
            "json_documents": json_count,
            "python_ast": ast_count,
            "bounded_security_findings": security_findings,
            "largest_document_words_before_validation_receipts": largest_words,
            "release_profile_status": "PASS",
            "legacy_workflow_policy_checks": "19/20 retained zero-credit compatibility result",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )

    prospective = sorted(set(owner_files(include_manifest=False) + [STAGED, MANIFEST]))
    write(
        "validation/x1-staged-review.json",
        {
            "schema": "ghc.family.exact-staged-review.v1",
            "parent": SOURCE,
            "allowed_change": "A",
            "allowed_paths": prospective,
            "count": len(prospective),
            "x2_paths": [],
            "deletions": 0,
            "outside_owner_paths": 0,
        },
    )

    final_without_manifest = owner_files(include_manifest=False)
    candidates, confirmed = privacy_scan(final_without_manifest)
    if confirmed:
        raise RuntimeError("Confirmed private material found in completed x1 surface")
    write(
        "validation/x1-privacy.json",
        {
            "schema": "ghc.family.five-class-privacy-adjudication.v1",
            "classes": list(PATTERNS),
            "scanned_files": len(final_without_manifest),
            "candidates": candidates,
            "candidate_count": len(candidates),
            "confirmed_hits": [],
            "confirmed_hit_count": 0,
            "same_owner_only": True,
        },
    )
    final_without_manifest = owner_files(include_manifest=False)
    entries = []
    for relative in final_without_manifest:
        raw = (ROOT / relative).read_bytes().replace(b"\r\n", b"\n")
        entries.append(
            {
                "path": relative,
                "bytes_normalized_lf": len(raw),
                "sha256_normalized_lf": hashlib.sha256(raw).hexdigest(),
            }
        )
    write(
        "validation/x1-manifest.json",
        {
            "schema": "ghc.family.normalized-lf-manifest.v1",
            "source": SOURCE,
            "anchor": "PENDING_X1_COMMIT",
            "byte_domain": "normalized_lf_git_blob",
            "entries": entries,
            "entry_count": len(entries),
            "declared_self_exclusions": [MANIFEST],
        },
    )

    all_paths = owner_files(include_manifest=True)
    if len(all_paths) >= 2000:
        raise RuntimeError("Owner-file ceiling reached")
    status_paths = []
    raw_status = git("status", "--porcelain=v1", "--untracked-files=all")
    for line in raw_status.splitlines():
        if line:
            status_paths.append(line[3:].replace("\\", "/"))
    if any(not (path.startswith(PREFIX) or path.startswith(SCRIPT_PREFIX)) for path in status_paths):
        raise RuntimeError("Uncommitted path outside the owner x1 scope")
    if set(all_paths) != set(prospective):
        raise RuntimeError("Exact x1 staged-surface projection drift")
    print(
        json.dumps(
            {
                "status": "VALID_PLANNING_ONLY_X1_PRESTAGE",
                "owner_files": len(all_paths),
                "manifest_entries": len(entries),
                "manifest_exclusions": 1,
                "planning_contracts": 200,
                "outcomes": dict(outcomes),
                "privacy_candidates": len(candidates),
                "privacy_confirmed": 0,
                "security_findings": 0,
                "x2_tree": False,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
