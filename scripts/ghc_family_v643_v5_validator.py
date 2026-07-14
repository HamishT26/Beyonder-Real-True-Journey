#!/usr/bin/env python3
"""Detailed validator for the Tamar Vey v643-v5 evidence packet."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
from pathlib import Path
from typing import Any


PHASE_REL = "docs/tamar-vey/v643-v5"
TRUTH_LABELS = ["completed", "represented", "open_gap", "exact_gate"]
EXPECTED_DISTRIBUTION = {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}
PRIVATE_PATTERNS = {
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "bearer_token": re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{16,}"),
    "conversation_url": re.compile(r"https?://(?:chatgpt\.com|chat\.openai\.com)/(?:c|share)/[A-Za-z0-9-]+", re.I),
    "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "openai_style_secret": re.compile(r"(?<![A-Za-z0-9_-])sk-[A-Za-z0-9_-]{20,}"),
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "raw_uuid": re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"),
    "windows_absolute_path": re.compile(r"(?i)(?:^|[\s\"'(])(?:[A-Z]:\\|\\\\[^\s\\]+\\[^\s\\]+\\)"),
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalized_bytes(path: Path) -> bytes:
    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return data
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def normalized_sha256(path: Path) -> str:
    return hashlib.sha256(normalized_bytes(path)).hexdigest()


def load_engine(repo: Path):
    path = repo / "scripts/ghc_family_v643_v5_evidence.py"
    spec = importlib.util.spec_from_file_location("ghc_family_v643_v5_evidence_for_validation", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=repo, check=True, text=True, encoding="utf-8", stdout=subprocess.PIPE).stdout.strip()


def validate(repo: Path, phase: Path | None = None, allow_pending_snapshot: bool = False) -> dict[str, Any]:
    repo = repo.resolve()
    phase = (phase or (repo / PHASE_REL)).resolve()
    engine = load_engine(repo)
    checks: list[str] = []
    issues: list[str] = []

    def check(condition: bool, name: str, detail: str | None = None) -> None:
        checks.append(name)
        if not condition:
            issues.append(detail or name)

    required = [
        "identity-receipt.json",
        "x1-proposals.json",
        "x2-proposal-ledger.json",
        "evidence/evidence-ledger.json",
        "retained-negative-register.json",
        "exact-open-gate-register.json",
        "threat-model.json",
        "phase-truth.json",
        "complete-incomplete-checklist.json",
        "environment/x2-execution-receipt.json",
        "reproduction/independent-team-gap.json",
        "reproduction/evidence-snapshot-plan.json",
        "reproduction/x1-content-seal.json",
        "reproduction/manifest.json",
        "tooling/executed-toolchain.json",
        "stage20/domain-veto-evidence-board.json",
        "deliverables/v643-v5-boundary-evidence-report.html",
        "deliverables/v643-v5-final-integrated-overview.md",
        "accessibility/static-report-receipt.json",
        "validation/x2-privacy-scan.json",
    ]
    for relative in required:
        check((phase / relative).is_file(), f"required:{relative}")

    json_files = sorted(phase.rglob("*.json"))
    for path in json_files:
        relative = path.relative_to(phase).as_posix()
        try:
            load(path)
            check(True, f"json:{relative}")
        except Exception as exc:
            check(False, f"json:{relative}", f"{relative}: {exc}")

    proposals = load(phase / "x1-proposals.json")
    proposal_rows = proposals["proposals"]
    check(proposals["proposal_count"] == 10, "proposal-count-declared")
    check(len(proposal_rows) == 10, "proposal-count-observed")
    check(proposals["prior_frozen_proposal_count"] == 190, "prior-frozen-190")
    check(proposals["outcome_classes"] == TRUTH_LABELS, "truth-label-vocabulary")
    check(proposals["expected_disposition_counts"] == EXPECTED_DISTRIBUTION, "expected-distribution")
    check(proposals["expected_counts_are_results"] is False, "expected-not-results")
    check(len({row["proposal_id"] for row in proposal_rows}) == 10, "proposal-ids-unique")
    check(len({row["title"] for row in proposal_rows}) == 10, "proposal-titles-unique")

    x2 = load(phase / "x2-proposal-ledger.json")
    check(x2["source_commit"] == engine.SOURCE_COMMIT, "source-commit")
    check(x2["source_seal"] == engine.SOURCE_SEAL, "source-seal")
    check(x2["x1_commit"] == engine.X1_COMMIT, "x1-commit")
    check(x2["proposal_count"] == 10, "x2-proposal-count")
    check(x2["case_count"] == 80, "x2-case-count")
    check(x2["synthetic_rejection_count"] == 70, "x2-rejection-count")
    check(x2["distribution"] == EXPECTED_DISTRIBUTION, "x2-distribution")
    check(x2["x1_before_x2_preserved"] is True, "x1-before-x2")
    observed = {row["proposal_id"]: row["observed_disposition"] for row in x2["proposals"]}
    check(observed == engine.OBSERVED, "observed-disposition-map")

    evaluated = engine.evaluate_catalog()
    check(len(evaluated) == 10, "catalog-proposal-count")
    for proposal in proposal_rows:
        pid = proposal["proposal_id"]
        check(pid in evaluated, f"catalog-present:{pid}")
        rows = evaluated[pid]
        check(len(rows) == 8, f"case-count:{pid}")
        check(sum(row["accepted"] for row in rows) == 1, f"accepted-count:{pid}")
        check(sum(not row["accepted"] for row in rows) == 7, f"rejected-count:{pid}")
        for row in rows:
            check(row["matched_expectation"] is True, f"expectation:{row['case_id']}")
            check(row["accepted"] == row["expected_accepted"], f"decision:{row['case_id']}")
            check(isinstance(row["reasons"], list), f"reasons-list:{row['case_id']}")
            check((not row["accepted"]) == bool(row["reasons"]), f"reason-polarity:{row['case_id']}")
            check(isinstance(row["details"], dict), f"details-map:{row['case_id']}")
        for relative in proposal["deliverables"]:
            artifact = phase / relative
            check(artifact.is_file(), f"deliverable:{pid}:{relative}")
            if artifact.is_file():
                payload = load(artifact)
                check(payload["phase"] == engine.PHASE, f"deliverable-phase:{relative}")
                check(payload["owner"] == engine.OWNER, f"deliverable-owner:{relative}")
                check(payload["proposal_id"] == pid, f"deliverable-proposal:{relative}")
                check(not payload.get("external_claims_established", []), f"no-external-claims:{relative}")

    negatives = load(phase / "retained-negative-register.json")
    expected_negative_count = 721 + 14 + 70 + len(engine.X2_OPERATIONAL_NEGATIVES)
    check(negatives["inherited_count"] == 721, "inherited-negatives-721")
    check(negatives["x1_operational_count"] == 14, "x1-negatives-14")
    check(negatives["new_synthetic_count"] == 70, "synthetic-negatives-70")
    check(negatives["x2_operational_count"] == len(engine.X2_OPERATIONAL_NEGATIVES), "x2-negative-count")
    check(negatives["negative_count"] == expected_negative_count, "effective-negative-count")
    check(len(negatives["negatives"]) == expected_negative_count, "negative-row-count")
    check(negatives["all_retained"] is True, "all-negatives-retained")
    check(negatives["erasure_permitted"] is False, "negative-erasure-forbidden")
    negative_ids = []
    for index, row in enumerate(negatives["negatives"]):
        negative_id = row.get("negative_id")
        check(isinstance(negative_id, str) and bool(negative_id), f"negative-id:{index}")
        check(row.get("retained") is True, f"negative-retained:{negative_id or index}")
        negative_ids.append(negative_id)
    check(len(negative_ids) == len(set(negative_ids)), "negative-ids-unique")

    gates = load(phase / "exact-open-gate-register.json")
    check(gates["open_gap_count"] == 5, "open-gap-count")
    check(gates["exact_gate_count"] == 6, "exact-gate-count")
    check(len(gates["open_gaps"]) == 5, "open-gap-rows")
    check(len(gates["exact_gates"]) == 6, "exact-gate-rows")
    check(gates["all_visible"] is True, "all-gates-visible")
    check(gates["none_silently_closed"] is True, "no-gate-silently-closed")
    for row in gates["open_gaps"]:
        check(bool(row["needs"]), f"open-gap-needs:{row['gate_id']}")
    for row in gates["exact_gates"]:
        check(bool(row["reserved_to"]), f"exact-gate-authority:{row['gate_id']}")

    truth = load(phase / "phase-truth.json")
    check(truth["distribution"] == EXPECTED_DISTRIBUTION, "truth-distribution")
    check(truth["case_count"] == 80, "truth-case-count")
    check(truth["synthetic_rejection_count"] == 70, "truth-rejections")
    check(truth["retained_negative_count"] == expected_negative_count, "truth-negative-count")
    check(truth["open_gap_count"] == 5, "truth-open-gaps")
    check(truth["exact_gate_count"] == 6, "truth-exact-gates")
    check(truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", "stage20-verdict")
    check(truth["independent_team_reproduction"] is False, "independent-reproduction-false")
    check(all(value is False for value in truth["protected_claims"].values()), "protected-claims-false")
    check(truth["outbound_message_count"] == 0, "no-outbound-message")
    check(truth["successor_task_count"] == 0, "no-successor-task")
    check(truth["subagent_count"] == 0, "no-subagent")

    evidence = load(phase / "evidence/evidence-ledger.json")
    for key in ["empirical_rows", "real_participants", "real_arms", "real_raters", "real_keys_or_proofs", "legal_or_cultural_ratifications", "independent_team_returns"]:
        check(evidence[key] == 0, f"external-evidence-zero:{key}")
    execution = load(phase / "environment/x2-execution-receipt.json")
    for key in ["real_data_downloaded", "desktop_updated", "elevation_used", "host_security_changed", "windows_feature_changed", "rebooted"]:
        check(execution[key] is False, f"execution-boundary:{key}")
    for key in ["real_participants_or_raters", "real_arms", "real_keys_or_proofs", "live_services_or_deployments", "accounts_or_api_keys_changed"]:
        check(execution[key] == 0, f"execution-zero:{key}")

    x1_seal = load(phase / "reproduction/x1-content-seal.json")
    check(x1_seal["x1_commit"] == engine.X1_COMMIT, "x1-seal-commit")
    check(x1_seal["entry_count"] == 30, "x1-seal-entry-count")
    check(x1_seal["all_unchanged"] is True, "x1-seal-all-unchanged")
    for row in x1_seal["entries"]:
        target = repo / row["repo_path"]
        check(target.is_file(), f"x1-seal-file:{row['repo_path']}")
        if target.is_file():
            check(normalized_sha256(target) == row["working_sha256_lf_normalized"], f"x1-seal-hash:{row['repo_path']}")
            check(row["unchanged"] is True, f"x1-seal-unchanged:{row['repo_path']}")

    privacy = load(phase / "validation/x2-privacy-scan.json")
    check(privacy["valid"] is True, "privacy-valid")
    check(privacy["hit_count"] == 0, "privacy-zero-hits")
    privacy_hits = []
    for path in sorted(p for p in phase.rglob("*") if p.is_file()):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for name, pattern in PRIVATE_PATTERNS.items():
            for match in pattern.finditer(text):
                privacy_hits.append({"path": path.relative_to(phase).as_posix(), "class": name, "match": match.group(0)})
        check("\ufffd" not in text, f"replacement-character-absent:{path.relative_to(phase).as_posix()}")
    check(not privacy_hits, "semantic-privacy-zero", str(privacy_hits))

    report = (phase / "deliverables/v643-v5-boundary-evidence-report.html").read_text(encoding="utf-8")
    for marker in ["<html lang=\"en-NZ\">", "href=\"#main\"", "<main id=\"main\">", "<caption>", "scope=\"col\"", "scope='row'", ":focus-visible", "forced-colors", "@media print"]:
        check(marker in report, f"report-marker:{marker}")
    check("<script" not in report.casefold(), "report-script-free")
    receipt = load(phase / "accessibility/static-report-receipt.json")
    check(receipt["static"] is True, "report-static")
    check(receipt["script_dependency"] is False, "report-script-independent")
    check(receipt["manual_accessibility_evaluation"] is False, "manual-accessibility-reserved")
    check(receipt["affected_user_evaluation"] is False, "affected-user-evaluation-reserved")
    check(receipt["complete_accessibility_conformance"] is False, "complete-accessibility-unclaimed")
    final_overview = (phase / "deliverables/v643-v5-final-integrated-overview.md").read_text(encoding="utf-8")
    check(len(final_overview.split()) >= 1500, "final-overview-three-page-equivalent")
    check("NOT_READY_FOR_STAGE_20" in final_overview, "final-overview-verdict")

    manifest = load(phase / "reproduction/manifest.json")
    check(manifest["entry_count"] == len(manifest["entries"]), "manifest-entry-count")
    check(len({row["repo_path"] for row in manifest["entries"]}) == manifest["entry_count"], "manifest-paths-unique")
    for row in manifest["entries"]:
        target = repo / row["repo_path"]
        check(target.is_file(), f"manifest-file:{row['repo_path']}")
        if target.is_file():
            payload = normalized_bytes(target)
            check(hashlib.sha256(payload).hexdigest() == row["sha256_lf_normalized"], f"manifest-hash:{row['repo_path']}")
            check(len(payload) == row["bytes_lf_normalized"], f"manifest-bytes:{row['repo_path']}")

    reproduction = load(phase / "reproduction/independent-team-gap.json")
    check(reproduction["independent_team_protocol_owned"] is False, "independent-protocol-absent")
    check(reproduction["independent_team_return_received"] is False, "independent-return-absent")
    check(reproduction["independent_team_reproduction_established"] is False, "independent-reproduction-open")
    if allow_pending_snapshot:
        check(manifest["snapshot_state"] in {"pending", "verified"}, "snapshot-state-pending-or-verified")
    else:
        check(manifest["snapshot_state"] == "verified", "snapshot-state-verified")
        check(truth["same_owner_repeatability"] is True, "same-owner-repeatability-verified")

    for commit, label in [(engine.SOURCE_COMMIT, "source"), (engine.SOURCE_SEAL, "source-seal"), (engine.X1_COMMIT, "x1")]:
        result = subprocess.run(["git", "merge-base", "--is-ancestor", commit, "HEAD"], cwd=repo)
        check(result.returncode == 0, f"{label}-ancestral")

    return {
        "schema": "ghc.family.v643-v5.detailed-validation.v1",
        "phase": engine.PHASE,
        "owner": engine.OWNER,
        "valid": not issues,
        "checks_passed": len(checks) - len(issues),
        "checks_total": len(checks),
        "issues": issues,
        "json_files_parsed": len(json_files),
        "privacy_hits": privacy_hits,
        "proposal_count": 10,
        "case_count": 80,
        "synthetic_rejection_count": 70,
        "retained_negative_count": expected_negative_count,
        "manifest_entries": manifest["entry_count"],
        "snapshot_state": manifest["snapshot_state"],
        "same_owner_repeatability": truth["same_owner_repeatability"],
        "independent_team_reproduction": False,
        "terminal_verdict": truth["terminal_verdict"],
        "boundary": engine.BOUNDARY,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--phase", type=Path)
    parser.add_argument("--allow-pending-snapshot", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = validate(args.repo, args.phase, args.allow_pending_snapshot)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        output = args.output if args.output.is_absolute() else args.repo / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
