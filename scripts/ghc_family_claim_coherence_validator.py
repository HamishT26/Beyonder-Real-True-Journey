#!/usr/bin/env python3
"""Validate a GHC Family claim-coherence phase with bounded, fail-closed checks."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


TRUTH_LABELS = {"completed", "represented", "open_gap", "exact_gate"}
EXPECTED_DISTRIBUTION = {
    "completed": 6,
    "represented": 2,
    "open_gap": 1,
    "exact_gate": 1,
}
PROTECTED_CLAIMS = {
    "empirical_gmut_confirmation",
    "detected_force",
    "unique_prediction",
    "theory_of_everything",
    "real_thos_superiority",
    "agi",
    "asi",
    "consciousness",
    "personhood",
    "freed_id_cryptographic_assurance",
    "freed_id_production_interoperability",
    "enacted_law",
    "cultural_ratification",
    "maori_authority",
    "maori_data_governance_authority",
    "deployment",
    "exhaustive_security",
    "complete_accessibility_conformance",
    "proof_or_canon",
    "independent_team_reproduction",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def validate(
    phase: Path,
    allow_pending_snapshot: bool = False,
    require_report: bool = False,
) -> dict[str, Any]:
    phase = phase.resolve()
    passed: list[str] = []
    issues: list[str] = []

    def check(condition: bool, label: str) -> None:
        if condition:
            passed.append(label)
        else:
            issues.append(label)

    required = [
        "x1-proposals.json",
        "x1-preregistration.md",
        "x2-proposal-ledger.json",
        "phase-truth.json",
        "exact-open-gate-register.json",
        "retained-negative-register.json",
        "complete-incomplete-checklist.json",
        "wellbeing-check.md",
        "v642-v4-integrated-overview.md",
        "environment/startup-receipt.json",
        "environment/version-receipt.json",
        "provenance/prior-proposal-collision-audit.json",
        "provenance/frozen-chain-proposal-index.json",
        "sources/source-ledger.json",
        "tooling/ghc-family-index.json",
        "tooling/selected-toolchain.json",
        "tooling/executed-toolchain.json",
        "workflow/route-preregistration.json",
        "workflow/validation-dependency-graph.json",
        "workflow/atomic-publication-vectors.json",
        "workflow/publication-barrier-receipt.json",
        "reproduction/worktree-lease-contract.json",
        "reproduction/partial-checkout-vectors.json",
        "reproduction/quarantine-recovery-receipt.json",
        "physics/field-redefinition-contract.json",
        "physics/gauge-orbit-vectors.json",
        "physics/identifiability-claim-boundary.json",
        "empirical/posterior-predictive-contract.json",
        "empirical/discrepancy-vectors.json",
        "empirical/real-row-promotion-lock.json",
        "thos/interference-estimand-contract.json",
        "thos/spillover-mutation-vectors.json",
        "thos/network-exposure-preregistration.json",
        "thos/real-arm-gap.json",
        "freed-id/cryptosuite-agility-profile.json",
        "freed-id/downgrade-negotiation-vectors.json",
        "freed-id/production-assurance-boundary.json",
        "cbr/maori-data-governance-gate.json",
        "cbr/secondary-use-authority-vectors.json",
        "cbr/collective-consent-and-benefit-register.json",
        "reproduction/blind-challenge-manifest.json",
        "reproduction/return-attestation-schema.json",
        "reproduction/independence-declaration-boundary.json",
        "reproduction/independent-team-gap.json",
        "accessibility/evidence-map.json",
        "accessibility/keyboard-landmark-vectors.json",
        "accessibility/manual-evaluation-reservation.json",
        "stage20/protected-claim-lattice.json",
        "validation/claim-contradiction-vectors.json",
        "stage20/terminal-verdict.json",
        "validation/execution-negative-log.json",
        "reproduction/manifest.json",
        "reproduction/clean-snapshot-validation.json",
    ]
    for rel in required:
        check((phase / rel).is_file(), f"required file exists: {rel}")
    if any(not (phase / rel).is_file() for rel in required):
        return {
            "schema": "ghc.family.claim-coherence-validation.v1",
            "valid": False,
            "checks_passed": len(passed),
            "checks_total": len(passed) + len(issues),
            "issues": issues,
        }

    json_files = sorted(phase.rglob("*.json"))
    parsed: dict[Path, Any] = {}
    for path in json_files:
        try:
            parsed[path] = load(path)
            check(True, f"JSON parses: {path.relative_to(phase).as_posix()}")
        except Exception:
            check(False, f"JSON parses: {path.relative_to(phase).as_posix()}")

    x1 = load(phase / "x1-proposals.json")
    audit = load(phase / "provenance/prior-proposal-collision-audit.json")
    sources = load(phase / "sources/source-ledger.json")
    x2 = load(phase / "x2-proposal-ledger.json")
    truth = load(phase / "phase-truth.json")
    chain = load(phase / "provenance/frozen-chain-proposal-index.json")
    negatives = load(phase / "retained-negative-register.json")
    gates = load(phase / "exact-open-gate-register.json")
    manifest = load(phase / "reproduction/manifest.json")
    snapshot = load(phase / "reproduction/clean-snapshot-validation.json")

    check(x1["phase"] == "v642-gmut-thos-v4-x1-x2", "x1 phase identity")
    check(x1["owner"] == "Ilyra Fen", "x1 owner identity")
    check(x1["proposal_count"] == 10, "x1 declares ten proposals")
    check(len(x1["proposals"]) == 10, "x1 contains ten proposals")
    check(len({row["proposal_id"] for row in x1["proposals"]}) == 10, "x1 proposal identifiers unique")
    check(len({row["title"] for row in x1["proposals"]}) == 10, "x1 proposal titles unique")
    check(set(x1["outcome_classes"]) == TRUTH_LABELS, "x1 truth labels exact")
    check(x1["expected_disposition_counts"] == EXPECTED_DISTRIBUTION, "x1 expected distribution")
    check(x1["expected_counts_are_results"] is False, "x1 expected counts are not results")
    check(x1["prior_frozen_proposal_count"] == 100, "x1 predecessor count")
    check(audit["prior_phase_counts"]["total"] == 100, "collision audit covers 100 predecessors")
    check(audit["exact_title_collisions"] == 0, "collision audit has zero exact titles")
    check(audit["semantic_delta_review_passed"] is True, "semantic novelty review passes")
    check(len(audit["checks"]) == 10, "collision audit covers ten candidates")
    check(all(row["distinct"] for row in audit["checks"]), "all candidates marked semantically distinct")
    check(len(audit["x1_execution_negatives"]) >= 2, "x1 failures retained")

    check(sources["effective_source_count"] == 54, "effective source count is 54")
    check(sum(sources["effective_status_counts"].values()) == 54, "source status counts sum")
    check(set(sources["effective_status_counts"]) == {"current", "stable", "draft", "watch"}, "four source status classes")
    check(sources["added_source_count"] == 8, "eight phase-local sources added")
    check(len(sources["added_sources"]) == 8, "eight added source records")
    check(all(row["url"].startswith("https://") for row in sources["added_sources"]), "source URLs use HTTPS")
    check(any(row["status_class"] == "draft" for row in sources["added_sources"]), "draft source visible")
    check("not validation" in sources["boundary"].lower(), "source boundary non-validation wording")

    check(x2["proposal_count"] == 10, "x2 declares ten proposals")
    check(len(x2["proposals"]) == 10, "x2 contains ten proposals")
    check(x2["disposition_counts"] == EXPECTED_DISTRIBUTION, "x2 observed distribution exact")
    check(x2["all_executed_as_far_as_evidence_permits"] is True, "x2 evidence-permitted execution complete")
    check(x2["x1_commit"] == truth["x1_commit"], "x1 commit consistent across ledgers")
    check(x2["evidence_commit"] == truth["evidence_commit"], "evidence commit consistent across ledgers")
    for row in x2["proposals"]:
        check(row["expected_disposition"] == row["observed_disposition"], f"expected and observed agree: {row['proposal_id']}")
        check(row["observed_disposition"] in TRUTH_LABELS, f"truth label valid: {row['proposal_id']}")
        check(row["executed_as_far_as_evidence_permits"] is True, f"executed as evidence permits: {row['proposal_id']}")
        check(all((phase / rel).is_file() for rel in row["evidence"]), f"evidence files exist: {row['proposal_id']}")
        check(bool(row["protected_gates_remain"]), f"protected gates retained: {row['proposal_id']}")

    check(chain["proposal_count"] == 110, "frozen chain count is 110")
    check(len(chain["records"]) == 110, "frozen chain has 110 records")
    check(len({row["proposal_id"] for row in chain["records"]}) == 110, "frozen chain proposal IDs unique")
    check(len({row["title"] for row in chain["records"]}) == 110, "frozen chain titles unique")
    check(chain["exact_duplicate_titles"] == [], "frozen chain duplicate title list empty")
    check(chain["version_counts"].get("v642-v4") == 10, "frozen chain includes ten v642-v4 records")

    vector_paths = [
        "workflow/atomic-publication-vectors.json",
        "reproduction/partial-checkout-vectors.json",
        "physics/gauge-orbit-vectors.json",
        "empirical/discrepancy-vectors.json",
        "thos/spillover-mutation-vectors.json",
        "freed-id/downgrade-negotiation-vectors.json",
        "cbr/secondary-use-authority-vectors.json",
        "reproduction/blind-challenge-manifest.json",
        "accessibility/keyboard-landmark-vectors.json",
        "validation/claim-contradiction-vectors.json",
    ]
    for rel in vector_paths:
        rows = load(phase / rel)["vectors"]
        check(len(rows) >= 3, f"negative and positive vectors present: {rel}")
        check(all(row["matches_expected"] for row in rows), f"all vector expectations match: {rel}")
        check(any(not bool(row.get("actual", row.get("passes", True))) or row.get("actual") in {"reject", "reject_packet", "reject_protocol", "exact_gate", "open_gap", "quarantine_owned", "refuse_foreign", "reject_independence_claim"} for row in rows), f"rejecting vector retained: {rel}")

    field = load(phase / "physics/field-redefinition-contract.json")
    empirical = load(phase / "empirical/real-row-promotion-lock.json")
    thos = load(phase / "thos/real-arm-gap.json")
    freed = load(phase / "freed-id/production-assurance-boundary.json")
    cbr = load(phase / "cbr/maori-data-governance-gate.json")
    independence = load(phase / "reproduction/independent-team-gap.json")
    a11y = load(phase / "accessibility/manual-evaluation-reservation.json")
    terminal = load(phase / "stage20/terminal-verdict.json")
    check(field["real_measurement_rows"] == 0, "GMUT has zero real rows")
    check(field["empirical_confirmation"] is False, "GMUT empirical confirmation false")
    check(field["theory_of_everything"] is False, "Theory of Everything false")
    check(empirical["real_measurement_rows"] == 0, "posterior predictive lock has zero real rows")
    check(empirical["promotion_allowed"] is False, "empirical promotion locked")
    check(thos["blind_matched_budget_real_arms"] == 0, "THOS has zero real arms")
    check(thos["real_thos_superiority"] is False, "THOS superiority false")
    check(all(thos[key] is False for key in ["agi", "asi", "consciousness", "personhood"]), "THOS identity and frontier claims false")
    check(sum(freed[key] for key in ["real_keys", "real_proofs", "live_resolvers_or_status_services", "interoperability_partners", "independent_security_reviews", "independent_privacy_reviews", "trust_governance_authorities"]) == 0, "Freed ID production evidence zero")
    check(freed["production_assurance"] is False, "Freed ID production assurance false")
    check(cbr["technical_artifact_can_grant_maori_authority"] is False, "technical artifact cannot grant Māori authority")
    check(cbr["authorized_participants_present"] == 0, "CBR authorized participants absent")
    check(independence["independent_team_count"] == 0, "independent team absent")
    check(independence["independent_reproduction_established"] is False, "independent reproduction false")
    check(a11y["complete_accessibility_conformance"] is False, "complete accessibility conformance false")
    check(a11y["qualified_manual_evaluation_completed"] is False, "manual accessibility evaluation not invented")
    check(terminal["verdict"] == "NOT_READY_FOR_STAGE_20", "terminal verdict not ready")

    negative_ids = [row["negative_id"] for row in negatives["negatives"]]
    check(negatives["inherited_count"] == 96, "96 inherited negatives")
    check(negatives["new_count"] >= 22, "at least 22 phase-local negatives")
    check(negatives["negative_count"] == len(negative_ids), "negative count matches records")
    check(len(set(negative_ids)) == len(negative_ids), "negative identifiers unique")
    check(negatives["all_retained"] is True, "all negatives retained")
    check(negatives["erasure_permitted"] is False, "negative erasure forbidden")
    check(all(f"V6423-N{number}" in negative_ids for number in range(21, 29)), "all eight v642-v3 execution negatives preserved")
    check(all(f"V6424-N{number:02d}" in negative_ids for number in range(1, 21)), "all twenty bounded v642-v4 negatives preserved")
    check(all(value in negative_ids for value in ["V6424-X1-N01", "V6424-X1-N02"]), "both x1 negatives preserved")

    check(gates["open_gap_count"] == 5, "five open gaps")
    check(gates["exact_gate_count"] == 6, "six exact gates")
    check(gates["silently_closed"] == 0, "no gate silently closed")
    check(len(gates["gates"]) == 11, "gate register contains eleven gates")
    check(Counter(row["gate_class"] for row in gates["gates"]) == {"open_gap": 5, "exact_gate": 6}, "gate class distribution exact")
    check(all(row["state"] in {"open", "deferred"} for row in gates["gates"]), "all gates remain open or deferred")

    check(truth["proposal_count"] == 10, "phase truth proposal count")
    check(truth["disposition_counts"] == EXPECTED_DISTRIBUTION, "phase truth distribution")
    check(truth["retained_negative_count"] == negatives["negative_count"], "phase truth negative count")
    check(truth["open_gap_count"] == 5 and truth["exact_gate_count"] == 6, "phase truth gate counts")
    check(set(truth["protected_claims"]) == PROTECTED_CLAIMS, "protected claim key set exact")
    check(all(value is False for value in truth["protected_claims"].values()), "all protected claims false")
    check("Māori authority" in truth["maori_authority_boundary"], "exact Māori authority boundary retained")
    check(truth["independent_team_gap"] == "open", "independent team gap open")
    check(truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", "phase truth terminal verdict")

    manifest_records = manifest["files"]
    check(manifest["file_count"] == len(manifest_records), "manifest count matches records")
    check(len({row["path"] for row in manifest_records}) == len(manifest_records), "manifest paths unique")
    check(manifest["same_owner_repeatability_only"] is True, "manifest bounds repeatability")
    check(manifest["independent_reproduction_established"] is False, "manifest independent reproduction false")
    for row in manifest_records:
        target = phase / row["path"]
        check(target.is_file(), f"manifest file exists: {row['path']}")
        check(target.is_file() and digest(target) == row["normalized_sha256"], f"manifest hash matches: {row['path']}")

    overview = (phase / "v642-v4-integrated-overview.md").read_text(encoding="utf-8")
    overview_words = len(re.findall(r"\b[\w'-]+\b", overview, flags=re.UNICODE))
    check(overview_words >= 1800, "overview meets three-page word floor")
    check("NOT_READY_FOR_STAGE_20" in overview, "overview terminal verdict visible")
    check("same-owner repeatability" in overview.lower(), "overview same-owner boundary visible")
    check("Māori concepts, wording, data, and governance remain under Māori authority" in overview, "overview Māori authority boundary visible")
    check("PLANNED_NOT_SENT" in overview, "overview route truth visible")

    if allow_pending_snapshot:
        check(snapshot["state"] in {"pending", "verified"}, "snapshot state allowed during candidate validation")
        check(x2["snapshot_state"] in {"pending", "verified"}, "x2 snapshot state allowed during candidate validation")
    else:
        check(snapshot["state"] == "verified", "clean snapshot validation verified")
        check(snapshot["snapshot_count"] >= 2, "at least two clean evidence snapshots")
        check(x2["snapshot_state"] == "verified", "x2 snapshot state verified")
        check(truth["same_owner_repeatability"] == "verified_bounded", "same-owner repeatability verified and bounded")
    check(snapshot["independent_reproduction_established"] is False, "snapshot evidence not independent reproduction")

    report_path = phase / "deliverables/v642-v4-claim-coherence-report.html"
    if require_report:
        check(report_path.is_file(), "static HTML report exists")
        report = report_path.read_text(encoding="utf-8") if report_path.is_file() else ""
        for token, label in [
            ('<html lang="en">', "report language"),
            ('href="#main"', "report skip link"),
            ('<main id="main">', "report main landmark"),
            ("<th scope=\"col\">", "report table headers"),
            ("prefers-reduced-motion", "report reduced motion"),
            (":focus-visible", "report visible focus"),
            ("Automated structure is not complete accessibility conformance.", "report accessibility boundary"),
            ("NOT_READY_FOR_STAGE_20", "report terminal verdict"),
        ]:
            check(token in report, label)

    privacy_patterns = {
        "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "raw_task_value": re.compile(r"[\"'](?:thread|task|session)_?id[\"']\s*[:=]\s*[\"'][^\"']+[\"']", re.I),
        "private_route_scheme": re.compile(r"\b(?:app|codex)://\S+", re.I),
        "private_windows_path": re.compile(r"(?<![A-Za-z0-9])(?:[A-Za-z]:\\(?:Users|GHC-Archives|ProgramData|Windows)\\[^\s\"']+)", re.I),
        "credential_material": re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY|bearer\s+[A-Za-z0-9._-]{16,}", re.I),
        "session_stream_file": re.compile(r"rollout-[^\s\"']+\.jsonl|sessions[\\/][^\s\"']+\.jsonl", re.I),
        "image_payload": re.compile(r"data:image/", re.I),
        "transcript_payload": re.compile(r"[\"'](?:raw_)?transcript[\"']\s*:\s*(?:[\"'][^\"']+[\"']|\[|\{)", re.I),
        "private_app_state_value": re.compile(r"[\"'](?:private_app_state|raw_browser_route|callable_id)[\"']\s*:\s*[\"'][^\"']+[\"']", re.I),
    }
    privacy_hits: list[dict[str, str]] = []
    public_files = sorted(path for path in phase.rglob("*") if path.is_file())
    for path in public_files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for name, pattern in privacy_patterns.items():
            for match in pattern.finditer(text):
                privacy_hits.append(
                    {
                        "file": path.relative_to(phase).as_posix(),
                        "class": name,
                        "sample": match.group(0)[:80],
                    }
                )
    check(not privacy_hits, "concrete-value privacy scan has zero hits")

    return {
        "schema": "ghc.family.claim-coherence-validation.v1",
        "valid": not issues,
        "checks_passed": len(passed),
        "checks_total": len(passed) + len(issues),
        "issues": issues,
        "proposal_count": 10,
        "disposition_counts": EXPECTED_DISTRIBUTION,
        "retained_negative_count": negatives["negative_count"],
        "open_gap_count": gates["open_gap_count"],
        "exact_gate_count": gates["exact_gate_count"],
        "json_files_parsed": len(json_files),
        "manifest_files": manifest["file_count"],
        "overview_words": overview_words,
        "privacy": {
            "files_scanned": len(public_files),
            "pattern_classes": len(privacy_patterns),
            "hits": privacy_hits,
        },
        "snapshot_state": snapshot["state"],
        "terminal_verdict": truth["terminal_verdict"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase-dir", type=Path, required=True)
    parser.add_argument("--allow-pending-snapshot", action="store_true")
    parser.add_argument("--require-report", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = validate(args.phase_dir, args.allow_pending_snapshot, args.require_report)
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    print(rendered, end="")
    raise SystemExit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
