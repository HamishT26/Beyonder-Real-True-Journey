#!/usr/bin/env python3
"""Detailed validator for the bounded v643-v1 rights-resilience packet."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
import ghc_family_rights_resilience as engine  # noqa: E402


REQUIRED_PROPOSAL_FIELDS = {
    "proposal_id", "title", "mission_surface", "hypothesis", "null_or_failure",
    "approval_class", "execution_lane", "authoritative_source_needs", "deliverables",
    "test_falsifier_or_gate", "rollback_or_recovery", "protected_gates",
    "expected_disposition", "novelty_against_prior_chain",
}


def validate(repo: Path, phase: Path | None = None, allow_pending_snapshot: bool = False) -> dict[str, Any]:
    repo = repo.resolve()
    phase = (phase or repo / "docs/eiren-kestrel/v643-v1").resolve()
    checks: list[dict[str, Any]] = []
    issues: list[str] = []

    def check(label: str, condition: bool, detail: Any = None) -> None:
        passed = bool(condition)
        checks.append({"label": label, "passed": passed, "detail": detail})
        if not passed:
            issues.append(label if detail is None else f"{label}: {detail}")

    def read(relative: str) -> Any:
        target = phase / relative
        try:
            value = json.loads(target.read_text(encoding="utf-8"))
            check(f"json:{relative}", True)
            return value
        except Exception as exc:  # pragma: no cover - diagnostic path
            check(f"json:{relative}", False, str(exc))
            return {}

    required = [
        "x1-proposals.json", "x1-preregistration.md", "x2-proposal-ledger.json",
        "phase-truth.json", "complete-incomplete-checklist.json", "retained-negative-register.json",
        "exact-open-gate-register.json", "threat-model.json", "v643-v1-integrated-overview.md",
        "wellbeing-check.md", "evidence/evidence-ledger.json", "reproduction/manifest.json",
        "reproduction/independent-team-gap.json", "deliverables/v643-v1-rights-resilience-report.html",
        "accessibility/static-report-receipt.json", "sources/source-ledger.json",
        "provenance/frozen-chain-proposal-index.json", "provenance/prior-proposal-collision-audit.json",
        "validation/x1-exact-file-set.json", "validation/x1-privacy-scan.json", "validation/x1-validation.json",
    ]
    for relative in required:
        check(f"required:{relative}", (phase / relative).is_file())

    x1 = read("x1-proposals.json")
    proposals = list(x1.get("proposals", []))
    check("phase-id", x1.get("phase") == engine.PHASE, x1.get("phase"))
    check("owner", x1.get("owner") == engine.OWNER, x1.get("owner"))
    check("source-commit", x1.get("source_revision") == engine.SOURCE_COMMIT, x1.get("source_revision"))
    check("proposal-count", len(proposals) == 10, len(proposals))
    check("prior-frozen-count", x1.get("prior_frozen_proposal_count") == 150)
    ids = [proposal.get("proposal_id") for proposal in proposals]
    check("proposal-ids-unique", len(ids) == len(set(ids)) == 10)
    for proposal in proposals:
        pid = proposal.get("proposal_id", "missing")
        for field in sorted(REQUIRED_PROPOSAL_FIELDS):
            value = proposal.get(field)
            check(f"proposal-field:{pid}:{field}", value not in (None, "", []))
        check(f"proposal-disposition:{pid}", proposal.get("expected_disposition") in engine.TRUTH_LABELS)
        check(f"proposal-deliverable-count:{pid}", len(proposal.get("deliverables", [])) == 3)
        check(f"proposal-source-needs:{pid}", len(proposal.get("authoritative_source_needs", [])) >= 3)
        check(f"proposal-protected-gates:{pid}", len(proposal.get("protected_gates", [])) >= 3)
    expected_distribution = {label: sum(proposal.get("expected_disposition") == label for proposal in proposals) for label in engine.TRUTH_LABELS}
    check("expected-distribution", expected_distribution == {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}, expected_distribution)

    catalog = engine.fixture_catalog()
    evaluated = engine.evaluate_catalog()
    check("fixture-group-count", len(catalog) == 10, len(catalog))
    check("fixture-case-count", sum(len(rows) for rows in catalog.values()) == 80)
    check("fixture-rejection-count", sum(not row["accepted"] for rows in evaluated.values() for row in rows) == 70)
    for pid, rows in evaluated.items():
        check(f"fixture-group-size:{pid}", len(rows) == 8, len(rows))
        for row in rows:
            check(f"fixture-match:{row['case_id']}", row["matched_expectation"], row.get("reasons"))

    x2 = read("x2-proposal-ledger.json")
    check("x2-source", x2.get("source_commit") == engine.SOURCE_COMMIT)
    check("x2-x1", x2.get("x1_commit") == engine.X1_COMMIT)
    check("x2-order", x2.get("x1_before_x2_preserved") is True)
    check("x2-counts", (x2.get("proposal_count"), x2.get("case_count"), x2.get("synthetic_rejection_count")) == (10, 80, 70))
    check("x2-distribution", x2.get("distribution") == {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}, x2.get("distribution"))

    for proposal in proposals:
        pid = proposal["proposal_id"]
        for index, relative in enumerate(proposal["deliverables"]):
            check(f"deliverable-exists:{pid}:{index}", (phase / relative).is_file(), relative)
            artifact = read(relative)
            check(f"deliverable-phase:{pid}:{index}", artifact.get("phase") == engine.PHASE)
            check(f"deliverable-owner:{pid}:{index}", artifact.get("owner") == engine.OWNER)
            check(f"deliverable-proposal:{pid}:{index}", artifact.get("proposal_id") == pid)
            check(f"deliverable-boundary:{pid}:{index}", bool(artifact.get("boundary")))

    negatives = read("retained-negative-register.json")
    negative_rows = negatives.get("negatives", [])
    check("negative-inherited-count", negatives.get("inherited_count") == 401)
    check("negative-new-synthetic", negatives.get("new_synthetic_count") == 70)
    check("negative-new-operational", negatives.get("new_operational_count") == 9)
    check("negative-total", negatives.get("negative_count") == 480 == len(negative_rows), (negatives.get("negative_count"), len(negative_rows)))
    check("negative-retention", negatives.get("all_retained") is True and negatives.get("erasure_permitted") is False)
    negative_ids = [row.get("negative_id") for row in negative_rows]
    check("negative-ids-unique", len(negative_ids) == len(set(negative_ids)))
    inherited = json.loads((repo / "docs/sylven-arc/v642-v8/retained-negative-register.json").read_text(encoding="utf-8"))
    inherited_ids = {row.get("negative_id") for row in inherited.get("negatives", [])}
    check("all-inherited-negatives-present", inherited_ids.issubset(set(negative_ids)), len(inherited_ids))
    for row in (item for item in negative_rows if item.get("origin") in {"v643-v1-preregistered-synthetic", "v643-v1-operational"}):
        check(f"new-negative-retained:{row.get('negative_id')}", row.get("retained") is True)

    gates = read("exact-open-gate-register.json")
    check("open-gap-count", gates.get("open_gap_count") == len(gates.get("open_gaps", [])) == 5)
    check("exact-gate-count", gates.get("exact_gate_count") == len(gates.get("exact_gates", [])) == 6)
    check("maori-authority-visible", any("Māori" in item.get("surface", "") for item in gates.get("exact_gates", [])))

    truth = read("phase-truth.json")
    check("truth-terminal", truth.get("terminal_verdict") == "NOT_READY_FOR_STAGE_20")
    check("truth-distribution", truth.get("distribution") == {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})
    check("truth-negatives", truth.get("retained_negative_count") == 480)
    check("truth-gates", (truth.get("open_gap_count"), truth.get("exact_gate_count")) == (5, 6))
    check("truth-route-unsent", truth.get("outbound_message_count") == 0 and truth.get("route_state") == "SUCCESSOR_MESSAGE_NOT_SENT")
    check("truth-no-agents", truth.get("successor_task_count") == 0 and truth.get("subagent_count") == 0)
    check("truth-independent-open", truth.get("independent_team_reproduction") is False)
    if allow_pending_snapshot:
        check("truth-snapshot-state", truth.get("same_owner_repeatability") in (False, True))
    else:
        check("truth-snapshot-verified", truth.get("same_owner_repeatability") is True)

    manifest = read("reproduction/manifest.json")
    entries = manifest.get("entries", [])
    check("manifest-entry-count", manifest.get("entry_count") == len(entries) == 60, len(entries))
    paths = [row.get("path") for row in entries]
    check("manifest-paths-unique", len(paths) == len(set(paths)))
    for row in entries:
        target = phase / row["path"]
        check(f"manifest-exists:{row['path']}", target.is_file())
        if target.is_file():
            check(f"manifest-hash:{row['path']}", engine.normalized_sha256(target) == row.get("sha256_lf_normalized"))
    if allow_pending_snapshot:
        check("manifest-snapshot-state", manifest.get("snapshot_state") in ("pending", "verified"))
    else:
        check("manifest-snapshot-verified", manifest.get("snapshot_state") == "verified")

    x1_set = read("validation/x1-exact-file-set.json")
    for row in x1_set.get("files", []):
        target = repo / row["path"]
        check(f"x1-bound-file:{row['path']}", target.is_file())
        if target.is_file():
            check(f"x1-bound-hash:{row['path']}", engine.normalized_sha256(target) == row["sha256"])

    report = (phase / "deliverables/v643-v1-rights-resilience-report.html").read_text(encoding="utf-8") if (phase / "deliverables/v643-v1-rights-resilience-report.html").is_file() else ""
    for marker in ("<html lang=\"en-NZ\">", "Skip to main content", "<main id=\"main\">", "<caption>", "scope=\"col\"", "scope='row'", "NOT_READY_FOR_STAGE_20"):
        check(f"report-marker:{marker}", marker in report)
    check("report-no-script", "<script" not in report.lower())
    check("report-no-private-path", re.search(r"[A-Za-z]:[\\/]", report) is None)
    overview = (phase / "v643-v1-integrated-overview.md").read_text(encoding="utf-8") if (phase / "v643-v1-integrated-overview.md").is_file() else ""
    check("overview-three-page-equivalent", len(re.findall(r"\b\w+\b", overview)) >= 1800, len(re.findall(r"\b\w+\b", overview)))
    check("overview-all-proposals", all(proposal["proposal_id"] in overview for proposal in proposals))
    check("overview-terminal-boundary", "NOT_READY_FOR_STAGE_20" in overview)

    json_files = list(phase.rglob("*.json"))
    for target in json_files:
        try:
            json.loads(target.read_text(encoding="utf-8"))
            check(f"all-json:{target.relative_to(phase).as_posix()}", True)
        except Exception as exc:
            check(f"all-json:{target.relative_to(phase).as_posix()}", False, str(exc))

    privacy_path = phase / "validation/privacy-scan.json"
    if privacy_path.is_file():
        privacy = read("validation/privacy-scan.json")
        check("privacy-valid", privacy.get("valid") is True)
        check("privacy-zero-hits", privacy.get("hit_count") == 0)
    else:
        check("privacy-pending-allowed", allow_pending_snapshot, "validation/privacy-scan.json missing")

    protected_false = [
        "READY_FOR_STAGE_20", "empirically confirmed GMUT", "production Freed ID complete",
        "CBR enacted", "independent reproduction established", "exhaustive security established",
    ]
    # Validator receipts intentionally echo protected phrases as negative-test
    # labels.  Scan the public evidence corpus, but exclude the validation
    # directory so a successful receipt cannot poison its own next replay.
    public_text = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in phase.rglob("*")
        if path.is_file()
        and path.suffix.lower() in {".json", ".md", ".html"}
        and path.relative_to(phase).parts[0] != "validation"
    )
    for phrase in protected_false:
        if phrase == "READY_FOR_STAGE_20":
            unsafe = re.search(r"(?<!NOT_)READY_FOR_STAGE_20", public_text) is not None
        else:
            unsafe = phrase.lower() in public_text.lower()
        check(f"protected-claim-absent:{phrase}", not unsafe)

    return {"schema": "ghc.family.v643-v1.detailed-validation.v1", "phase": engine.PHASE, "owner": engine.OWNER, "valid": not issues, "check_count": len(checks), "passed_count": sum(row["passed"] for row in checks), "issue_count": len(issues), "issues": issues, "checks": checks, "allow_pending_snapshot": allow_pending_snapshot, "boundary": engine.BOUNDARY}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--phase", type=Path)
    parser.add_argument("--allow-pending-snapshot", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = validate(args.repo, args.phase, args.allow_pending_snapshot)
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8", newline="\n")
    print(json.dumps({key: result[key] for key in ("valid", "check_count", "passed_count", "issue_count", "issues")}, ensure_ascii=False, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
