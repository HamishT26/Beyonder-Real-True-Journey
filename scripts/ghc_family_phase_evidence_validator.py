#!/usr/bin/env python3
"""Validate a GHC family evidence phase without granting external truth claims."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


DISPOSITIONS = {"completed", "represented", "open_gap", "exact_gate"}
RAW_TASK_ID = re.compile(
    r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
    re.IGNORECASE,
)
WINDOWS_ABSOLUTE = re.compile(r"\b[A-Za-z]:\\")


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_phase(phase: Path) -> dict[str, Any]:
    issues: list[dict[str, str]] = []

    def issue(path: str, code: str, message: str) -> None:
        issues.append({"path": path, "code": code, "message": message})

    json_paths = sorted(phase.rglob("*.json"))
    parsed: dict[str, Any] = {}
    for path in json_paths:
        relative = path.relative_to(phase).as_posix()
        try:
            parsed[relative] = load(path)
        except (OSError, json.JSONDecodeError) as exc:
            issue(relative, "json_parse_failed", str(exc))

    required = [
        "x1-proposals.json",
        "sources/source-ledger.json",
        "provenance/source-independence-graph.json",
        "physics/canonical-gmut-audit.json",
        "physics/conservation-stability-sweep.json",
        "empirical/adapter-readiness.json",
        "thos/matched-budget-protocol.json",
        "thos/synthetic-scorer-proxy.json",
        "freed-id/minimum-profile.json",
        "freed-id/conformance-vectors.json",
        "freed-id/conformance-report.json",
        "cbr/legitimacy-crosswalk.json",
        "cbr/conflict-cases.json",
        "cbr/conflict-report.json",
        "security/red-team.json",
        "security/recovery-drill.json",
        "stage20/evidence-board.json",
        "stage20/decision-rehearsal.json",
        "reproduction/manifest.json",
        "reproduction/reproduction-report.json",
        "x2-proposal-ledger.json",
    ]
    x1_preview = parsed.get("x1-proposals.json", {})
    is_v3_refresh = x1_preview.get("phase") == "v641-gmut-thos-v3-x1-x2"
    if is_v3_refresh:
        required.extend(
            [
                "provenance/source-dedup-audit.json",
                "physics/variational-trace-audit.json",
                "physics/conservation-sensitivity-envelope.json",
                "empirical/baseline-readiness-matrix.json",
                "thos/power-contamination-audit.json",
                "freed-id/cryptographic-assurance-boundary.json",
                "cbr/authority-veto-matrix.json",
                "security/adversarial-fixtures.json",
                "stage20/expiry-contradiction-drill.json",
                "reproduction/hash-parity.json",
                "environment/version-receipt.json",
                "tooling/selected-toolchain.json",
            ]
        )
    for relative in required:
        if relative not in parsed:
            issue(relative, "required_artifact_missing", "required JSON artifact is absent")

    if issues:
        return {
            "schema": "ghc.family.phase-evidence-validation.v1",
            "valid": False,
            "json_file_count": len(json_paths),
            "issues": issues,
        }

    x1 = parsed["x1-proposals.json"]
    proposals = x1.get("proposals", [])
    proposal_fields = {
        "proposal_id",
        "hypothesis",
        "null",
        "authoritative_source_ids",
        "deliverables",
        "tests_and_falsifiers",
        "approval_class",
        "recovery",
        "protected_gates",
        "x1_status",
    }
    if is_v3_refresh:
        proposal_fields.add("decision_rule")
    if len(proposals) != 10 or len({row.get("proposal_id") for row in proposals}) != 10:
        issue("x1-proposals.json", "proposal_count_invalid", "expected ten unique proposals")
    for index, proposal in enumerate(proposals):
        missing = sorted(proposal_fields - proposal.keys())
        if missing:
            issue(
                f"x1-proposals.json#proposals[{index}]",
                "proposal_fields_missing",
                ", ".join(missing),
            )
        if proposal.get("x1_status") != "preregistered":
            issue(
                f"x1-proposals.json#proposals[{index}]",
                "x1_not_preregistered",
                str(proposal.get("x1_status")),
            )

    sources = parsed["sources/source-ledger.json"]
    source_rows = sources.get("sources", [])
    if sources.get("source_count") != len(source_rows) or len(source_rows) < 20:
        issue("sources/source-ledger.json", "source_count_invalid", "count mismatch or too few sources")
    if len({row.get("source_id") for row in source_rows}) != len(source_rows):
        issue("sources/source-ledger.json", "duplicate_source_id", "source IDs must be unique")
    for index, source in enumerate(source_rows):
        if not str(source.get("url", "")).startswith("https://"):
            issue(f"sources/source-ledger.json#sources[{index}]", "source_not_https", str(source.get("url")))
        if not source.get("authority_root"):
            issue(f"sources/source-ledger.json#sources[{index}]", "authority_root_missing", "")
        if source.get("snapshot_embedded") is not False:
            issue(f"sources/source-ledger.json#sources[{index}]", "snapshot_embedded", "must be false")
    if is_v3_refresh and len(source_rows) != 33:
        issue("sources/source-ledger.json", "v3_source_count_invalid", "expected 33 records")

    graph = parsed["provenance/source-independence-graph.json"]
    roots = {row["authority_root"] for row in source_rows}
    if graph.get("source_count") != len(source_rows):
        issue("provenance/source-independence-graph.json", "graph_source_count_mismatch", "")
    if graph.get("authority_root_count") != len(roots):
        issue("provenance/source-independence-graph.json", "graph_root_count_mismatch", "")
    if graph.get("authority_root_count", 0) >= graph.get("source_count", 0):
        issue("provenance/source-independence-graph.json", "dedup_not_demonstrated", "expected repeated authority roots")
    if is_v3_refresh:
        dedup = parsed["provenance/source-dedup-audit.json"]
        if not dedup.get("passed") or not dedup.get("deterministic_order"):
            issue("provenance/source-dedup-audit.json", "v3_dedup_audit_failed", "")
        if len(dedup.get("version_corrections", [])) < 2 or any(
            row.get("adds_independent_vote") is not False
            for row in dedup.get("version_corrections", [])
        ):
            issue(
                "provenance/source-dedup-audit.json",
                "v3_version_correction_invalid",
                "current-version corrections must not add independent votes",
            )

    canonical = parsed["physics/canonical-gmut-audit.json"]
    if not canonical.get("passed") or canonical.get("disposition") != "completed":
        issue("physics/canonical-gmut-audit.json", "canonical_audit_failed", "")
    if not canonical.get("negative_fixture", {}).get("rejected_as_expected"):
        issue("physics/canonical-gmut-audit.json", "category_collapse_not_rejected", "")
    if is_v3_refresh:
        trace = parsed["physics/variational-trace-audit.json"]
        if not trace.get("passed") or not all(
            row.get("matched") for row in trace.get("negative_fixtures", [])
        ):
            issue("physics/variational-trace-audit.json", "v3_variational_trace_failed", "")

    stability = parsed["physics/conservation-stability-sweep.json"]
    if not stability.get("passed") or not all(row.get("matched") for row in stability.get("stability_cases", [])):
        issue("physics/conservation-stability-sweep.json", "stability_sweep_failed", "")
    if is_v3_refresh:
        sensitivity = parsed["physics/conservation-sensitivity-envelope.json"]
        if not sensitivity.get("passed") or sensitivity.get("case_count", 0) < 9:
            issue(
                "physics/conservation-sensitivity-envelope.json",
                "v3_sensitivity_envelope_failed",
                "",
            )

    empirical = parsed["empirical/adapter-readiness.json"]
    if not empirical.get("validation", {}).get("valid"):
        issue("empirical/adapter-readiness.json", "adapter_validation_failed", "")
    if empirical.get("fit_status") != "NO_LIKELIHOOD_RUN_NO_EMPIRICAL_GMUT_CONFIRMATION":
        issue("empirical/adapter-readiness.json", "fit_boundary_missing", "")
    if any(row.get("status") == "fit_complete" for row in empirical.get("adapters", [])):
        issue("empirical/adapter-readiness.json", "fit_inflation", "fit_complete is forbidden without exact evidence")
    if is_v3_refresh:
        readiness = parsed["empirical/baseline-readiness-matrix.json"]
        if (
            readiness.get("row_count", 0) < 7
            or readiness.get("all_no_download") is not True
            or readiness.get("all_baselines_pending") is not True
            or readiness.get("disposition") != "open_gap"
        ):
            issue(
                "empirical/baseline-readiness-matrix.json",
                "v3_empirical_boundary_failed",
                "",
            )

    proxy = parsed["thos/synthetic-scorer-proxy.json"]
    if "not_agent_or_model_performance" not in proxy.get("interpretation_boundary", ""):
        issue("thos/synthetic-scorer-proxy.json", "synthetic_boundary_missing", "")
    protocol = parsed["thos/matched-budget-protocol.json"]
    if any(row.get("status") == "complete" for row in protocol.get("arms", [])):
        issue("thos/matched-budget-protocol.json", "blind_arm_false_completion", "")
    if is_v3_refresh:
        power = parsed["thos/power-contamination-audit.json"]
        if (
            power.get("all_matched") is not True
            or power.get("blind_arm_count") != 0
            or power.get("disposition") != "represented"
        ):
            issue("thos/power-contamination-audit.json", "v3_thos_boundary_failed", "")

    freed = parsed["freed-id/conformance-report.json"]
    if not freed.get("all_matched") or freed.get("vector_count") < 7:
        issue("freed-id/conformance-report.json", "freed_id_conformance_failed", "")
    if any(token not in freed.get("boundary", "") for token in ("no_signature_verification", "no_personhood")):
        issue("freed-id/conformance-report.json", "freed_id_boundary_missing", "")
    if is_v3_refresh:
        assurance = parsed["freed-id/cryptographic-assurance-boundary.json"]
        if not assurance.get("passed") or freed.get("vector_count", 0) < 10:
            issue(
                "freed-id/cryptographic-assurance-boundary.json",
                "v3_freed_id_boundary_failed",
                "",
            )
        if any(
            row.get("layer") in {"proof_verification", "did_resolution", "deployment"}
            and row.get("state", "").startswith("completed")
            for row in assurance.get("layers", [])
        ):
            issue(
                "freed-id/cryptographic-assurance-boundary.json",
                "v3_crypto_or_deploy_overclaim",
                "",
            )

    cbr = parsed["cbr/conflict-report.json"]
    if not cbr.get("all_matched") or cbr.get("case_count") < 6:
        issue("cbr/conflict-report.json", "cbr_rehearsal_failed", "")
    if "Māori authority" not in cbr.get("maori_authority_boundary", ""):
        issue("cbr/conflict-report.json", "maori_authority_boundary_missing", "")
    if is_v3_refresh:
        authority = parsed["cbr/authority-veto-matrix.json"]
        if (
            authority.get("all_matched") is not True
            or authority.get("disposition") != "exact_gate"
            or "Māori authority" not in authority.get("maori_authority_boundary", "")
        ):
            issue("cbr/authority-veto-matrix.json", "v3_authority_veto_failed", "")

    security = parsed["security/red-team.json"]
    if not security.get("all_matched") or security.get("fixture_count") < 7:
        issue("security/red-team.json", "security_fixture_failure", "")
    if "not an exhaustive security scan" not in security.get("boundary", ""):
        issue("security/red-team.json", "security_boundary_missing", "")
    if is_v3_refresh:
        adversarial = parsed["security/adversarial-fixtures.json"]
        if (
            adversarial.get("all_matched") is not True
            or adversarial.get("raw_fixture_retained") is not False
            or adversarial.get("fixture_count", 0) < 8
        ):
            issue("security/adversarial-fixtures.json", "v3_adversarial_fixture_failed", "")

    board = parsed["stage20/evidence-board.json"]
    board_fields = {
        "claim_id",
        "claim",
        "grade",
        "state",
        "evidence",
        "owner",
        "review_date",
        "dissent",
        "rejection_or_promotion_condition",
    }
    if is_v3_refresh:
        board_fields.update({"expiry_status", "contradiction_state"})
    if len(board.get("claims", [])) < 12:
        issue("stage20/evidence-board.json", "too_few_claims", "")
    for index, row in enumerate(board.get("claims", [])):
        missing = sorted(board_fields - row.keys())
        if missing:
            issue(f"stage20/evidence-board.json#claims[{index}]", "claim_fields_missing", ", ".join(missing))
        if row.get("grade") == "E4" and any(
            term in row.get("claim", "")
            for term in ("GMUT", "THOS", "consciousness", "personhood", "Freed ID", "CBR")
        ):
            issue(f"stage20/evidence-board.json#claims[{index}]", "unsupported_e4", row.get("claim", ""))
    if not all(row.get("not_prediction") is True for row in board.get("scenarios", [])):
        issue("stage20/evidence-board.json", "scenario_prediction_inflation", "")
    if is_v3_refresh:
        expiry = parsed["stage20/expiry-contradiction-drill.json"]
        if expiry.get("all_matched") is not True or len(expiry.get("fixtures", [])) < 5:
            issue(
                "stage20/expiry-contradiction-drill.json",
                "v3_expiry_contradiction_failed",
                "",
            )

    ledger = parsed["x2-proposal-ledger.json"]
    outcomes = ledger.get("outcomes", [])
    if len(outcomes) != 10 or len({row.get("proposal_id") for row in outcomes}) != 10:
        issue("x2-proposal-ledger.json", "outcome_count_invalid", "expected ten unique outcomes")
    disposition_counts = Counter(row.get("disposition") for row in outcomes)
    if set(disposition_counts) != DISPOSITIONS:
        issue(
            "x2-proposal-ledger.json",
            "disposition_classes_incomplete",
            f"observed {sorted(disposition_counts)}",
        )
    if ledger.get("summary") != {key: disposition_counts[key] for key in sorted(DISPOSITIONS)}:
        issue("x2-proposal-ledger.json", "disposition_summary_mismatch", "")

    reproduction = parsed["reproduction/reproduction-report.json"]
    if reproduction.get("status") == "verified_local_repeatability":
        if not re.fullmatch(r"[0-9a-f]{40}", str(reproduction.get("evidence_commit", ""))):
            issue("reproduction/reproduction-report.json", "evidence_commit_invalid", "")
        if not reproduction.get("clean_snapshot") or not reproduction.get("core_tests_passed"):
            issue("reproduction/reproduction-report.json", "repeatability_receipt_incomplete", "")
    if reproduction.get("independent_team") is not False:
        issue("reproduction/reproduction-report.json", "independence_overclaim", "")
    if is_v3_refresh:
        parity = parsed["reproduction/hash-parity.json"]
        if reproduction.get("status") == "verified_local_repeatability":
            if parity.get("all_match") is not True or not reproduction.get(
                "hash_parity_passed"
            ):
                issue(
                    "reproduction/hash-parity.json",
                    "v3_hash_parity_failed",
                    "",
                )
        environment = parsed["environment/version-receipt.json"]
        if environment.get("codex_desktop_updated_by_phase") is not False:
            issue(
                "environment/version-receipt.json",
                "codex_app_update_forbidden",
                "",
            )
        toolchain = parsed["tooling/selected-toolchain.json"]
        if (
            toolchain.get("historical_tools_executed") is not False
            or toolchain.get("mass_deletion_performed") is not False
        ):
            issue("tooling/selected-toolchain.json", "v3_toolchain_boundary_failed", "")

    for path in sorted(phase.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".json", ".md", ".html", ".tex"}:
            continue
        relative = path.relative_to(phase).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        if WINDOWS_ABSOLUTE.search(text):
            issue(relative, "local_absolute_path", "Windows absolute path is forbidden")
        if RAW_TASK_ID.search(text):
            issue(relative, "raw_task_id", "raw task/thread IDs are forbidden")

    return {
        "schema": "ghc.family.phase-evidence-validation.v1",
        "valid": not issues,
        "json_file_count": len(json_paths),
        "proposal_count": len(outcomes),
        "source_count": len(source_rows),
        "authority_root_count": len(roots),
        "dispositions": {key: disposition_counts[key] for key in sorted(DISPOSITIONS)},
        "reproduction_status": reproduction.get("status"),
        "issues": issues,
        "boundary": "local artifact validation does not close external empirical, legal, cultural, deployment, or independent-reproduction gaps",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-dir", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = validate_phase(args.phase_dir.resolve())
    encoded = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
