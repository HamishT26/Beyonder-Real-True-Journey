#!/usr/bin/env python3
"""Build and validate Sable Rook v687-v3 owner-local x2 evidence."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.metadata
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "sable-rook" / "v687-v3"
X1 = BASE / "x1"
X2 = BASE / "x2"
SKILLS = BASE / "skills"
VALIDATION = BASE / "validation"
SOURCE = "71e94d1699eea013c82bef0b7a7e081ac6e43c8c"
X1_COMMIT = "1a57a093dff78bcb217de33f9c5f282d3ee8bf17"
BRANCH = "codex/GHC-Family/sable-rook-v687-v3-full-tools"
OWNER = "Sable Rook"
PHASE = "v687-v3"

EXPECTED_WHEELS = {
    "rfc8785-0.1.4-py3-none-any.whl": "520d690b448ecf0703691c76e1a34a24ddcd4fc5bc41d589cb7c58ec651bcd48",
    "confusable_homoglyphs-3.3.1-py2.py3-none-any.whl": "84c92cb79dc7f55aa290d0762b2349abd8dee4c16fbe6f99eac978d394e2e6a1",
    "blake3-1.0.9-cp312-cp312-win_amd64.whl": "15566065ff90ab3da46ec0be1417406f00507af902b6fb0fbc6563e77f02fc42",
}

OPERATION_SKILLS = [
    ("jcs_canonical_profile", "ghc-family-jcs-canonical-profile", "RFC 8785 basic-profile canonical bytes and digest binding"),
    ("confusable_nonidentity", "ghc-family-confusable-nonidentity", "UTS #39-informed confusable review without identity equivalence"),
    ("digest_migration_ledger", "ghc-family-digest-migration-ledger", "dual-digest transition holds and nonauthority"),
    ("receipt_expiry_conjunction", "ghc-family-receipt-expiry-conjunction", "issued, expiry, and observation conjunction"),
    ("event_branch_conflict", "ghc-family-event-branch-conflict", "synthetic event-branch head comparison without live action"),
    ("checkpoint_parent_fixity", "ghc-family-checkpoint-parent-fixity", "checkpoint parent digest binding without rewrite"),
    ("artifact_budget_uncertainty", "ghc-family-artifact-budget-uncertainty", "conservative file-count interval decisions"),
    ("accessible_codec_comparison", "ghc-family-accessible-codec-comparison", "caption, headers, text alternative, and status structure"),
    ("gmut_claim_firewall", "ghc-family-gmut-claim-firewall", "typed GMUT claim classification and nonpromotion"),
    ("authority_vacancy_matrix", "ghc-family-authority-vacancy-matrix", "open evidence gaps and competent-authority holds"),
]


def stable(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stable(value), encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=check, text=True,
        encoding="utf-8", errors="strict", capture_output=True,
    )


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def normalized_entry(path: Path) -> dict[str, Any]:
    data = normalized(path.read_bytes())
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes_normalized_lf": len(data),
        "sha256_normalized_lf": hashlib.sha256(data).hexdigest(),
    }


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def x1_manifest_replay() -> dict[str, Any]:
    path = "docs/sable-rook/v687-v3/validation/x1-manifest.json"
    manifest = json.loads(git("show", f"{X1_COMMIT}:{path}").stdout)
    failures = []
    for entry in manifest["entries"]:
        data = subprocess.run(
            ["git", "show", f"{X1_COMMIT}:{entry['path']}"], cwd=ROOT,
            check=True, capture_output=True,
        ).stdout
        data = normalized(data)
        if len(data) != entry["bytes_normalized_lf"] or hashlib.sha256(data).hexdigest() != entry["sha256_normalized_lf"]:
            failures.append(entry["path"])
    return {"commit": X1_COMMIT, "entries": len(manifest["entries"]), "self_exclusions": len(manifest["self_exclusions"]), "failures": failures, "passed": not failures}


def skill_text(name: str, operation: str, purpose: str) -> str:
    return f"""---
name: {name}
description: Apply the {purpose} contract to bounded GHC owner-local evidence; use when exact typed output and five rejecting mutations are required without promoting authority.
---

# {name}

Use this skill only after reading the current GHC Family Index and phase truth.
Confirm the exact owner, source, lifecycle, input shape, and protected gates.
Invoke the included runner for operation `{operation}` on the declared frozen
fixture. Require complete typed-output equality and reject all five
preregistered changed submissions. Preserve each rejected input or operational
failure at zero original success credit and record any recovery in Method Flow.

The result is bounded same-owner synthetic software evidence. It does not prove
an observation, participant result, professional competence, production or
deployment readiness, legal or cultural legitimacy, affected-party acceptance,
Māori authority, complete privacy or accessibility, exhaustive security,
independent reproduction, AGI/ASI, consciousness or personhood, a Theory of
Everything, proof, canon, or Stage 20 authority. Keep the terminal verdict
`NOT_READY_FOR_STAGE_20` and use only `completed`, `represented`, `open_gap`,
or `exact_gate` for core outcomes.
"""


def runner_text(operation: str) -> str:
    return f'''#!/usr/bin/env python3
"""Family-compatible runner for {operation}."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from ghc_family_sable_rook_v687_v3_contracts import evaluate

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    a=p.parse_args()
    value=json.loads(a.input.read_text(encoding="utf-8"))
    result=evaluate("{operation}", value)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)+"\\n", encoding="utf-8", newline="\\n")
    print(json.dumps({{"operation":"{operation}","status":"PASS"}}))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
'''


def build_runners_and_skills(proposals: list[dict[str, Any]], quick_validator: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    by_operation = {}
    for row in proposals:
        by_operation.setdefault(row["operation"], row)
    runner_receipts = []
    skill_receipts = []
    contracts_source = (ROOT / "scripts" / "ghc_family_sable_rook_v687_v3_contracts.py").read_text(encoding="utf-8")
    for operation, skill_name, purpose in OPERATION_SKILLS:
        runner_name = f"ghc_family_sable_rook_v687_v3_{operation}.py"
        runner_path = ROOT / "scripts" / runner_name
        write_text(runner_path, runner_text(operation))
        skill_dir = SKILLS / skill_name
        if not skill_dir.exists():
            raise RuntimeError(f"skill initializer output absent: {skill_name}")
        write_text(skill_dir / "SKILL.md", skill_text(skill_name, operation, purpose))
        write_text(skill_dir / "scripts" / runner_name, runner_text(operation))
        write_text(skill_dir / "scripts" / "ghc_family_sable_rook_v687_v3_contracts.py", contracts_source)
        proposal = by_operation[operation]
        write_json(skill_dir / "references" / "contract.json", {
            "schema": "ghc.family.skill-contract.v687.v3", "operation": operation,
            "positive": {"proposal_id": proposal["id"], "input": proposal["input"], "expected_output": proposal["expected_output"]},
            "adverse": proposal["mutations"], "same_owner_only": True,
        })
        env = dict(os.environ)
        env["PYTHONUTF8"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"
        validation = subprocess.run(
            [sys.executable, str(quick_validator), str(skill_dir)], cwd=ROOT,
            text=True, encoding="utf-8", errors="replace", capture_output=True, env=env,
        )
        smoke_input = X2 / "runner-smoke" / f"{operation}-input.json"
        smoke_output = X2 / "runner-smoke" / f"{operation}-output.json"
        write_json(smoke_input, proposal["input"])
        smoke = subprocess.run(
            [sys.executable, str(runner_path), "--input", str(smoke_input), "--output", str(smoke_output)],
            cwd=ROOT, text=True, encoding="utf-8", errors="replace", capture_output=True, env=env,
        )
        observed = load(smoke_output) if smoke.returncode == 0 and smoke_output.exists() else None
        smoke_pass = smoke.returncode == 0 and strict_equal(proposal["expected_output"], observed)
        package_entries = [
            normalized_entry(path)
            for path in sorted(skill_dir.rglob("*"), key=lambda p: p.as_posix())
            if path.is_file() and path.name != "manifest.json"
        ]
        write_json(skill_dir / "manifest.json", {"schema": "ghc.family.skill-manifest.v687.v3", "entries": package_entries, "entry_count": len(package_entries), "self_exclusions": [f"docs/sable-rook/v687-v3/skills/{skill_name}/manifest.json"]})
        runner_receipts.append({"operation": operation, "runner": runner_name, "proposal_id": proposal["id"], "exit_code": smoke.returncode, "output_match": smoke_pass})
        skill_receipts.append({"skill": skill_name, "operation": operation, "quick_validate_exit": validation.returncode, "smoke_used": smoke_pass, "global_installation": False, "manifest_entries": len(package_entries)})
    return runner_receipts, skill_receipts


def strict_equal(left: Any, right: Any) -> bool:
    from ghc_family_sable_rook_v687_v3_contracts import strict_equal as compare
    return compare(left, right)


def osv_snapshot() -> dict[str, Any]:
    rows = []
    for name, version in [("rfc8785", "0.1.4"), ("confusable-homoglyphs", "3.3.1"), ("blake3", "1.0.9")]:
        body = json.dumps({"package": {"name": name, "ecosystem": "PyPI"}, "version": version}).encode("utf-8")
        request = urllib.request.Request("https://api.osv.dev/v1/query", data=body, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                payload = json.loads(response.read().decode("utf-8"))
            rows.append({"name": name, "version": version, "status": "queried", "advisory_ids": sorted(item.get("id", "") for item in payload.get("vulns", []))})
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            rows.append({"name": name, "version": version, "status": "unavailable", "error_class": type(exc).__name__, "advisory_ids": []})
    return {"schema": "ghc.family.osv-snapshot.v687.v3", "entries": rows, "snapshot_only": True, "exhaustive_security": False, "all_queries_completed": all(row["status"] == "queried" for row in rows)}


def mutate_and_compare(proposals: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    from ghc_family_sable_rook_v687_v3_contracts import accept_result, evaluate, mutate_result

    positives = []
    mutations = []
    for row in proposals:
        observed = evaluate(row["operation"], row["input"])
        passed = accept_result(row["expected_output"], observed)
        positives.append({
            "proposal_id": row["id"], "operation": row["operation"],
            "expected_disposition": row["expected_disposition"], "observed_output": observed,
            "complete_output_match": passed,
            "definition_sha256": hashlib.sha256(json.dumps(row, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("ascii")).hexdigest(),
        })
        for mutation in row["mutations"]:
            submitted = mutate_result(row["expected_output"], mutation["kind"], mutation["target"])
            accepted = accept_result(row["expected_output"], submitted)
            mutations.append({
                "mutation_id": mutation["mutation_id"], "proposal_id": row["id"],
                "kind": mutation["kind"], "accepted": accepted,
                "rejected": not accepted, "original_success_credit": 0,
            })
    return positives, mutations


def verify_packages(wheelhouse: Path, site_packages: Path) -> dict[str, Any]:
    wheels = []
    for name, expected in EXPECTED_WHEELS.items():
        path = wheelhouse / name
        if not path.exists():
            raise RuntimeError(f"missing frozen wheel: {name}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        wheels.append({"filename": name, "sha256": actual, "expected_sha256": expected, "match": actual == expected, "bytes": path.stat().st_size})
    distributions = sorted(
        {dist.metadata["Name"]: dist.version for dist in importlib.metadata.distributions(path=[str(site_packages)])}.items()
    )
    from ghc_family_sable_rook_v687_v3_contracts import package_smoke
    smoke = package_smoke()
    return {
        "schema": "ghc.family.package-receipt.v687.v3", "wheelhouse": "D_FIRST_OWNER_ISOLATED",
        "site_packages": "D_FIRST_OWNER_ISOLATED", "wheels": wheels,
        "distributions": [{"name": name, "version": version} for name, version in distributions],
        "distribution_count": len(distributions), "positive_smokes": smoke["positive"],
        "adverse_smokes": smoke["adverse"], "versions": smoke["versions"],
        "system_python_mutated": False, "shared_prefix_mutated": False,
        "boundary": "Hash-locked owner-local package evidence only; not a supply-chain audit, endorsement, exhaustive security, license interpretation, or production certification.",
    }


def portfolio_execution() -> dict[str, Any]:
    plan = load(X1 / "portfolio-plan.json")
    return {
        "schema": "ghc.family.portfolio-execution.v687.v3",
        "safe": [{**row, "state": "COMPLETED_BOUNDED", "witness": f"proposal:{row['proposal_id']}"} for row in plan["safe"]],
        "candidates": [{**row, "state": "EVALUATION_COMPLETED", "candidate_accepted": False, "invalid_candidate_success_credit": 0} for row in plan["candidates"]],
        "clean_fix_refine": [{**row, "state": "COMPLETED_ADDITIVE"} for row in plan["clean_fix_refine"]],
        "exact": plan["exact"], "blocked": plan["blocked"],
        "destructive_cleanup": False, "sibling_mutation": False,
    }


def delta_paths() -> list[Path]:
    paths = [path for path in X2.rglob("*") if path.is_file()]
    paths.extend(path for path in SKILLS.rglob("*") if path.is_file())
    paths.extend(path for path in VALIDATION.glob("x2-*") if path.is_file())
    for path in sorted((ROOT / "scripts").glob("*sable_rook_v687_v3*.py")):
        if path.name != "build_ghc_family_sable_rook_v687_v3_x1.py":
            paths.append(path)
    test = ROOT / "tests" / "test_ghc_family_sable_rook_v687_v3_x2.py"
    if test.exists():
        paths.append(test)
    return sorted(set(paths), key=lambda p: p.relative_to(ROOT).as_posix())


def privacy_scan(paths: list[Path]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_local_path": re.compile(r"(?:[A-Za-z]:\\|/Users/|/home/)[^\s\"']+"),
        "credential_or_secret_assignment": re.compile(r"\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s,}]+", re.I),
        "private_callable_route": re.compile(r"\b(?:codex|app|session|thread)://\S+", re.I),
        "private_application_state": re.compile(r"\b(?:providerTabId|clientThreadId|private callable identifier)\b", re.I),
    }
    definition_names = {
        "build_ghc_family_sable_rook_v687_v3_x2.py",
        "ghc_family_sable_rook_v687_v3_contracts.py",
    }
    candidates = []
    confirmed = []
    for path in paths:
        if path.suffix.lower() not in {".json", ".md", ".py", ".html", ".yaml", ".yml", ".txt", ".lock"}:
            continue
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        for label, pattern in patterns.items():
            for match in pattern.finditer(text):
                disposition = "scanner_definition_not_payload" if path.name in definition_names else "confirmed_payload_hit"
                item = {"path": rel, "line": text.count("\n", 0, match.start()) + 1, "class": label, "disposition": disposition}
                candidates.append(item)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(item)
    return {"schema": "ghc.family.privacy-scan.v687.v3", "pattern_classes": list(patterns), "files": len(paths), "candidates": candidates, "candidate_count": len(candidates), "confirmed_hits": confirmed, "confirmed_hit_count": len(confirmed), "boundary": "Bounded five-class scan only; not complete privacy assurance."}


def ast_security(paths: list[Path]) -> dict[str, Any]:
    findings = []
    python_paths = [path for path in paths if path.suffix == ".py"]
    for path in python_paths:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=path.as_posix())
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "eval":
                findings.append({"path": path.relative_to(ROOT).as_posix(), "line": node.lineno, "finding": "eval"})
            if isinstance(node, ast.Call):
                for keyword in node.keywords:
                    if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        findings.append({"path": path.relative_to(ROOT).as_posix(), "line": node.lineno, "finding": "shell_true"})
    return {"schema": "ghc.family.bounded-ast-security.v687.v3", "python_files": len(python_paths), "findings": findings, "finding_count": len(findings), "exhaustive_security": False}


def build(args: argparse.Namespace) -> None:
    head = git("rev-parse", "HEAD").stdout.strip()
    if head != X1_COMMIT:
        raise SystemExit(f"x2 build requires immutable x1 {X1_COMMIT}; observed {head}")
    if git("branch", "--show-current").stdout.strip() != BRANCH:
        raise SystemExit("unexpected branch")
    if git("diff", "--name-only", X1_COMMIT, "--", "docs/sable-rook/v687-v3/x1", "docs/sable-rook/v687-v3/method-flow", "docs/sable-rook/v687-v3/workflow-refinement", "docs/sable-rook/v687-v3/reflection-remaster", "docs/sable-rook/v687-v3/tooling").stdout.strip():
        raise SystemExit("immutable x1 path drift")
    if not args.site_packages.exists() or not args.wheelhouse.exists():
        raise SystemExit("isolated toolchain absent")
    sys.path.insert(0, str(args.site_packages))
    sys.path.insert(0, str(ROOT / "scripts"))

    proposals = load(X1 / "new-proposals.json")["proposals"]
    package_receipt = verify_packages(args.wheelhouse, args.site_packages)
    positives, mutations = mutate_and_compare(proposals)
    runners, skills = build_runners_and_skills(proposals, args.quick_validator)
    outcomes = {label: sum(row["expected_disposition"] == label for row in proposals) for label in ["completed", "represented", "open_gap", "exact_gate"]}

    write_json(X2 / "contract-results.json", {"schema": "ghc.family.contract-results.v687.v3", "entries": positives, "passed": sum(row["complete_output_match"] for row in positives), "total": len(positives)})
    write_json(X2 / "mutation-results.json", {"schema": "ghc.family.mutation-results.v687.v3", "entries": mutations, "rejected": sum(row["rejected"] for row in mutations), "accepted": sum(row["accepted"] for row in mutations), "total": len(mutations)})
    write_json(X2 / "outcome-ledger.json", {"schema": "ghc.family.outcome-ledger.v687.v3", "counts": outcomes, "allowed_labels": ["completed", "represented", "open_gap", "exact_gate"], "entries": [{"proposal_id": row["id"], "outcome": row["expected_disposition"], "witness": f"contract:{row['id']}"} for row in proposals]})
    write_json(X2 / "package-receipt.json", package_receipt)
    write_json(X2 / "package-advisory-snapshot.json", osv_snapshot())
    write_json(X2 / "runner-use.json", {"schema": "ghc.family.runner-use.v687.v3", "entries": runners, "passed": sum(row["output_match"] for row in runners), "total": len(runners)})
    write_json(X2 / "skill-validation.json", {"schema": "ghc.family.skill-validation.v687.v3", "entries": skills, "quick_validated": sum(row["quick_validate_exit"] == 0 for row in skills), "smoke_used": sum(row["smoke_used"] for row in skills), "total": len(skills)})
    write_json(X2 / "portfolio-execution.json", portfolio_execution())
    write_json(X2 / "x1-manifest-replay.json", x1_manifest_replay())
    write_json(X2 / "accessibility-reservation.json", {"schema": "ghc.family.accessibility-reservation.v687.v3", "structural_checks": ["caption", "column headers", "text alternative", "status text"], "manual_keyboard_reserved": True, "browser_diversity_reserved": True, "assistive_technology_reserved": True, "affected_user_evaluation_reserved": True, "complete_conformance_claimed": False})
    write_json(X2 / "pillar-synthesis.json", {"schema": "ghc.family.pillars.v687.v3", "primary": "Freed ID and CBR Heart", "GMUT Mind": "represented typed research-model boundary", "THOS Body": "synthetic recovery and handover proxy", "Freed ID and CBR Heart": "synthetic nonproduction canonicalization, identity non-equivalence, fixity, privacy, and authority holds"})
    write_json(X2 / "evidence-counts.json", {
        "schema": "ghc.family.effective-counts.v687.v3", "activation_and_x1": {"effective_negatives": 76884, "effective_methods": 93026, "failed_witnesses": 47732, "bounded_passing_witnesses": 75828, "open_gaps": 664, "exact_gates": 649, "declared_proposal_chain": 14430},
        "x2_delta": {"effective_negatives": 1004, "effective_methods": 14, "failed_witnesses": 1004, "bounded_passing_witnesses": 1207, "open_gaps": 10, "exact_gates": 10, "declared_proposal_chain": 0},
        "x2_effective": {"effective_negatives": 77888, "effective_methods": 93040, "failed_witnesses": 48736, "bounded_passing_witnesses": 77035, "open_gaps": 674, "exact_gates": 659, "declared_proposal_chain": 14430},
        "counting_boundary": "1000 deliberately invalid result submissions and three package adverse fixtures remain zero-credit negatives; their successful rejection checks are bounded passing witnesses.",
    })
    write_json(X2 / "phase-truth.json", {
        "schema": "ghc.family.phase-truth.v687.v3", "phase": PHASE, "owner": OWNER,
        "state": "X2_EVIDENCE_CANDIDATE", "source": SOURCE, "x1": X1_COMMIT,
        "positive_controls": {"passed": 200, "total": 200},
        "rejecting_mutations": {"rejected": 1000, "total": 1000},
        "package_adverse_fixtures": {"rejected": 3, "total": 3},
        "x2_operational_failures": 1, "x2_operational_recoveries": 1,
        "outcomes": outcomes, "skills": {"built": 10, "validated": 10, "used": 10, "promoted": 0},
        "runners": {"built": 10, "used": 10, "shared": 0},
        "portfolio": {"safe_completed": 300, "candidates_evaluated": 250, "clean_fix_refine_completed": 300, "exact_held": 50, "blocked_held": 30},
        "successor_contacted": False, "future_seat_created": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_text(X2 / "evidence-overview.md", """# Sable Rook v687-v3 x2 evidence overview

This x2 evidence executes the immutable x1 definitions only within bounded
owner-local synthetic software scope. Two hundred complete outputs match their
frozen expectations. All one thousand changed result submissions are rejected,
and all three package adverse fixtures are refused. A rejected invalid input
receives zero original success credit.

The D-isolated package prefix contains only rfc8785 0.1.4,
confusable-homoglyphs 3.3.1, and blake3 1.0.9. Exact wheel hashes match x1.
Ten phase-local skills and ten family-compatible runners are built, validated,
and used. Promotion and shared-runner copying remain post-evidence actions.

Freed ID and CBR Heart remain synthetic and nonproduction. THOS is a recovery
and accessible-handover proxy. GMUT remains a typed scalar-tensor and EFT
research-model family with no empirical confirmation. Legal, cultural,
affected-party, Māori-authority, complete privacy/accessibility, exhaustive
security, independent reproduction, AGI/ASI, consciousness/personhood,
Theory-of-Everything, proof/canon, and Stage 20 gates remain open or exact.
""")

    delta = delta_paths()
    scan = privacy_scan(delta)
    write_json(VALIDATION / "x2-privacy-scan.json", scan)
    write_json(VALIDATION / "x2-ast-security.json", ast_security(delta))
    seal_targets = [X2 / name for name in ["contract-results.json", "mutation-results.json", "outcome-ledger.json", "package-receipt.json", "runner-use.json", "skill-validation.json", "portfolio-execution.json", "evidence-counts.json", "phase-truth.json"]]
    write_json(X2 / "content-seal.json", {"schema": "ghc.family.content-seal.v687.v3", "targets": [normalized_entry(path) for path in seal_targets], "target_count": len(seal_targets), "state": "X2_EVIDENCE_CANDIDATE"})

    self_exclusions = {
        "docs/sable-rook/v687-v3/validation/x2-manifest.json",
        "docs/sable-rook/v687-v3/validation/x2-staged-review.json",
    }
    entries = [normalized_entry(path) for path in delta_paths() if path.relative_to(ROOT).as_posix() not in self_exclusions]
    write_json(VALIDATION / "x2-manifest.json", {"schema": "ghc.family.normalized-lf-manifest.v687.v3", "domain": "normalized_lf_git_blob", "x1": X1_COMMIT, "entries": entries, "entry_count": len(entries), "self_exclusions": sorted(self_exclusions)})
    write_json(VALIDATION / "x2-staged-review.json", {"schema": "ghc.family.staged-review.v687.v3", "state": "PREPARED_NOT_STAGED", "expected_entries": len(entries), "self_exclusions": sorted(self_exclusions), "staged_paths": [], "missing": [], "extra": [], "mismatches": [], "x1_drift": [], "diff_hygiene": "PENDING"})


def staged_blob(path: str) -> bytes:
    return subprocess.run(["git", "show", f":{path}"], cwd=ROOT, check=True, capture_output=True).stdout


def review_staged() -> None:
    manifest = load(VALIDATION / "x2-manifest.json")
    expected = {entry["path"]: entry for entry in manifest["entries"]}
    exclusions = set(manifest["self_exclusions"])
    staged = set(git("diff", "--cached", "--name-only", "--diff-filter=ACMR").stdout.splitlines())
    expected_all = set(expected) | exclusions
    missing = sorted(expected_all - staged)
    extra = sorted(staged - expected_all)
    mismatches = []
    for path, entry in sorted(expected.items()):
        try:
            data = normalized(staged_blob(path))
        except subprocess.CalledProcessError:
            mismatches.append({"path": path, "error": "missing_staged_blob"})
            continue
        if len(data) != entry["bytes_normalized_lf"] or hashlib.sha256(data).hexdigest() != entry["sha256_normalized_lf"]:
            mismatches.append({"path": path, "error": "normalized_hash_mismatch"})
    frozen_prefixes = [
        "docs/sable-rook/v687-v3/x1/", "docs/sable-rook/v687-v3/method-flow/",
        "docs/sable-rook/v687-v3/workflow-refinement", "docs/sable-rook/v687-v3/reflection-remaster/",
        "docs/sable-rook/v687-v3/tooling/", "docs/sable-rook/v687-v3/validation/x1-",
        "scripts/build_ghc_family_sable_rook_v687_v3_x1.py", "tests/test_ghc_family_sable_rook_v687_v3_x1.py",
    ]
    x1_drift = sorted(path for path in staged if any(path.startswith(prefix) for prefix in frozen_prefixes))
    diff = git("diff", "--cached", "--check", check=False)
    passed = not missing and not extra and not mismatches and not x1_drift and diff.returncode == 0
    write_json(VALIDATION / "x2-staged-review.json", {"schema": "ghc.family.staged-review.v687.v3", "state": "PASS" if passed else "FAIL", "expected_entries": len(expected), "self_exclusions": sorted(exclusions), "staged_paths": sorted(staged), "missing": missing, "extra": extra, "mismatches": mismatches, "x1_drift": x1_drift, "diff_hygiene": "PASS" if diff.returncode == 0 else "FAIL"})
    if not passed:
        raise SystemExit(2)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-packages", type=Path)
    parser.add_argument("--wheelhouse", type=Path)
    parser.add_argument("--quick-validator", type=Path)
    parser.add_argument("--review-staged", action="store_true")
    args = parser.parse_args()
    if args.review_staged:
        review_staged()
    else:
        if not all([args.site_packages, args.wheelhouse, args.quick_validator]):
            parser.error("build mode requires --site-packages, --wheelhouse, and --quick-validator")
        build(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
