#!/usr/bin/env python3
"""Review the Sable Rook v646-v3 x1 freeze before commit."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = Path("docs/sable-rook/v646-v3")
PHASE = ROOT / PHASE_REL
OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
REQUIRED_PROPOSAL = {
    "proposal_id", "title", "mission_surface", "hypothesis", "null_or_failure",
    "approval_class", "execution_lane", "current_primary_or_official_source_needs",
    "concrete_artifacts", "test_falsifier_or_acceptance_gate", "rollback_or_recovery",
    "protected_gates", "expected_disposition", "novelty_against_410_frozen_proposals",
}
PRIVATE = {
    "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b"),
    "delegation_markup": re.compile(r"(?i)<" + r"\/?" + "codex_" + r"delegation>|<source_" + "thread_id>"),
    "private_uri": re.compile(r"(?i)\b(?:app|plugin|codex|vscode)://"),
    "private_local_path": re.compile(r"(?i)(?:\b[A-Z]:[\\/]+(?:Users|GHC-Archives)[\\/]+|/(?:home|users)/)"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s,;]+"),
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str, binary: bool = False) -> str | bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=not binary, encoding=None if binary else "utf-8")


def phase_files() -> list[Path]:
    return sorted(path for path in PHASE.rglob("*") if path.is_file())


def scan_payload(name: str, payload: str) -> list[dict[str, Any]]:
    hits = []
    for kind, pattern in PRIVATE.items():
        for match in pattern.finditer(payload):
            hits.append({"path": name, "class": kind, "offset": match.start()})
    return hits


def structural() -> dict[str, Any]:
    issues: list[str] = []
    lifecycle_has_advanced = (PHASE / "phase-truth.json").exists()
    proposals = load(PHASE / "x1-proposals.json")
    rows = proposals.get("proposals", [])
    if proposals.get("prior_frozen_proposal_count") != 410:
        issues.append("prior proposal count is not 410")
    if proposals.get("new_frozen_proposal_count") != 10 or len(rows) != 10:
        issues.append("new proposal count is not 10")
    if proposals.get("frozen_chain_count_after_x1") != 420:
        issues.append("frozen chain count is not 420")
    if proposals.get("x2_execution_present") is not False:
        issues.append("x2 execution is present")
    if len({row.get("proposal_id") for row in rows}) != 10 or len({row.get("title") for row in rows}) != 10:
        issues.append("proposal ids or titles are not unique")
    for row in rows:
        missing = REQUIRED_PROPOSAL - set(row)
        if missing:
            issues.append(f"{row.get('proposal_id')} missing {sorted(missing)}")
        if row.get("expected_disposition") not in OUTCOMES:
            issues.append(f"{row.get('proposal_id')} invalid disposition")
    if proposals.get("expected_distribution") != {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}:
        issues.append("expected distribution mismatch")

    collision = load(PHASE / "provenance/prior-proposal-collision-audit.json")
    if collision.get("prior_frozen_proposal_count") != 410 or collision.get("exact_title_collision_count") != 0:
        issues.append("proposal novelty audit failed")
    if len(collision.get("comparisons", [])) != 10:
        issues.append("proposal comparison count mismatch")
    if any(row.get("manual_result") != "distinct" for row in collision.get("comparisons", [])):
        issues.append("manual semantic novelty result missing")
    portfolio_collision = load(PHASE / "provenance/prior-portfolio-collision-audit.json")
    if portfolio_collision.get("exact_collision_count") != 0:
        issues.append("portfolio title collision found")

    portfolio = load(PHASE / "approval-packets/x1-approval-portfolio.json")
    expected_counts = {
        "safe_now": 30,
        "safe_reviewed_after_rewrite": 15,
        "safe_new_sable": 15,
        "candidates": 20,
        "candidate_reviewed_after_rewrite": 10,
        "candidate_new_sable": 10,
        "inherited_exact": 10,
        "inherited_blocked": 5,
    }
    if portfolio.get("counts") != expected_counts:
        issues.append("approval portfolio counts mismatch")
    if portfolio.get("completion_credit_before_x2") != 0:
        issues.append("portfolio has pre-x2 completion credit")
    if any(row.get("x1_state") != "preregistered_no_completion_credit" for row in portfolio.get("safe_now", []) + portfolio.get("candidates", [])):
        issues.append("supporting packet has completion credit")
    if any(row.get("x2_execution") not in {"do_not_execute", "prohibited_without_new_evidence"} for row in portfolio.get("inherited_exact_packets", []) + portfolio.get("inherited_blocked_packets", [])):
        issues.append("exact or blocked execution boundary missing")

    tools = load(PHASE / "prototypes/x1-skill-runner-plan.json")
    if len(tools.get("skills", [])) != 20 or len(tools.get("runners", [])) != 10:
        issues.append("skill or runner count mismatch")
    if any(row.get("x2_state") != "preregistered_not_built_or_used" for row in tools.get("skills", []) + tools.get("runners", [])):
        issues.append("tool prototype has pre-x2 credit")
    cleanup = load(PHASE / "maintenance/x1-clean-refine-plan.json")
    if len(cleanup.get("tasks", [])) != 30 or cleanup.get("destructive_task_count") != 0 or cleanup.get("completion_credit_before_x2") != 0:
        issues.append("cleanup plan boundary mismatch")

    sources = load(PHASE / "sources/source-ledger.json")
    if len(sources.get("sources", [])) != 19:
        issues.append("source ledger count mismatch")
    if any(row.get("status") not in {"current", "stable", "draft", "watch"} for row in sources.get("sources", [])):
        issues.append("invalid source status")
    if any(sources.get(key) != 0 for key in ("real_data_rows_ingested", "likelihood_evaluations", "real_participants", "real_keys_or_proofs")):
        issues.append("source ledger overstates execution")

    method = load(PHASE / "method-flow/runner-validation.json")
    negatives = load(PHASE / "validation/x1-operational-negatives.json")
    if not method.get("valid"):
        issues.append("Method Flow validation failed")
    operational_rows = negatives.get("new_x1_operational_rows", [])
    operational_count = negatives.get("new_x1_operational")
    if operational_count != len(operational_rows):
        issues.append("x1 operational negative cardinality mismatch")
    if method.get("method_count", 0) < 1 or method.get("witness_count", 0) < operational_count:
        issues.append("Method Flow does not retain every operational failure")
    expected_effective = 2619 + 70 + len(operational_rows)
    if negatives.get("inherited_effective") != 2619 or negatives.get("preregistered_synthetic") != 70 or negatives.get("effective_after_x1") != expected_effective:
        issues.append("negative accounting mismatch")

    forbidden = ["phase-truth.json", "x2-proposal-ledger.json", "closeout-receipt.json", "seal-receipt.json", "final-validation-record.json"]
    if not lifecycle_has_advanced and any((PHASE / name).exists() for name in forbidden):
        issues.append("x2 or closeout artifact exists before the x1 freeze")
    required_index = [PHASE / "tooling/x1-index/ghc-family-index.json", PHASE / "tooling/x1-index/ghc-family-index.md"]
    if any(not path.is_file() for path in required_index):
        issues.append("phase-scoped GHC Family Index is missing")
    return {
        "schema": "ghc.family.v646-v3.x1-structural-review.v1",
        "proposal_count": len(rows),
        "file_count": len(phase_files()),
        "lifecycle_has_advanced": lifecycle_has_advanced,
        "issues": issues,
        "valid": not issues,
    }


def privacy_from_worktree() -> dict[str, Any]:
    hits = []
    files = phase_files()
    for path in files:
        try:
            payload = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        hits.extend(scan_payload(path.relative_to(ROOT).as_posix(), payload))
    return {
        "schema": "ghc.family.v646-v3.privacy-review.v1",
        "pattern_classes": sorted(PRIVATE),
        "file_count": len(files),
        "confirmed_hits": hits,
        "confirmed_hit_count": len(hits),
        "valid": not hits,
        "boundary": "A bounded zero-hit scan is not complete privacy or security assurance.",
    }


def staged_review() -> tuple[dict[str, Any], dict[str, Any]]:
    paths = [line for line in str(git("diff", "--cached", "--name-only", "--diff-filter=ACMR")).splitlines() if line]
    issues = []
    allowed_prefix = PHASE_REL.as_posix() + "/"
    allowed_files = {
        "scripts/ghc_family_v646_v3_definitions.py",
        "scripts/build_ghc_family_v646_v3_preregistration.py",
        "scripts/ghc_family_v646_v3_x1_review.py",
        "tests/test_ghc_family_v646_v3_x1.py",
    }
    manifest_entries = []
    manifest_path = (PHASE_REL / "validation/x1-staged-manifest.json").as_posix()
    for path in paths:
        if not (path.startswith(allowed_prefix) or path in allowed_files):
            issues.append(f"unexpected staged path: {path}")
        blob = git("show", f":{path}", binary=True)
        assert isinstance(blob, bytes)
        if path.endswith(".json"):
            try:
                json.loads(blob.decode("utf-8"))
            except Exception as exc:
                issues.append(f"invalid staged JSON {path}: {exc}")
        try:
            hits = scan_payload(path, blob.decode("utf-8"))
        except UnicodeDecodeError:
            hits = []
        if hits:
            issues.append(f"privacy hits in staged {path}: {hits}")
        if path != manifest_path:
            manifest_entries.append({"path": path, "sha256": hashlib.sha256(blob).hexdigest(), "bytes": len(blob)})
    lifecycle_names = {"phase-truth.json", "x2-proposal-ledger.json", "closeout-receipt.json", "seal-receipt.json", "final-validation-record.json"}
    leaks = [path for path in paths if Path(path).name in lifecycle_names]
    if leaks:
        issues.append(f"x2 lifecycle files staged in x1: {leaks}")
    if len(paths) < 20:
        issues.append("staged x1 surface unexpectedly small")
    review = {
        "schema": "ghc.family.v646-v3.x1-staged-review.v1",
        "staged_file_count": len(paths),
        "staged_paths": paths,
        "lifecycle_leaks": leaks,
        "issues": issues,
        "valid": not issues,
    }
    manifest = {
        "schema": "ghc.family.v646-v3.x1-staged-manifest.v1",
        "phase": "v646-gmut-thos-v3-x1-x2",
        "hash_domain": "exact staged Git-index blobs excluding this self-referential manifest",
        "entry_count": len(manifest_entries),
        "entries": manifest_entries,
    }
    return review, manifest


def write_receipts(structure: dict[str, Any], privacy: dict[str, Any], staged: dict[str, Any] | None, manifest: dict[str, Any] | None) -> None:
    target = PHASE / "validation"
    target.mkdir(parents=True, exist_ok=True)
    (target / "x1-structural-review.json").write_text(json.dumps(structure, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    (target / "x1-privacy-review.json").write_text(json.dumps(privacy, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    if staged is not None and manifest is not None:
        (target / "x1-staged-review.json").write_text(json.dumps(staged, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        (target / "x1-staged-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staged", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    structure = structural()
    privacy = privacy_from_worktree()
    staged = manifest = None
    if args.staged:
        staged, manifest = staged_review()
    valid = structure["valid"] and privacy["valid"] and (staged is None or staged["valid"])
    if args.write:
        write_receipts(structure, privacy, staged, manifest)
    print(json.dumps({"structure": structure, "privacy": privacy, "staged": staged, "manifest_entries": None if manifest is None else manifest["entry_count"], "valid": valid}, ensure_ascii=False))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
