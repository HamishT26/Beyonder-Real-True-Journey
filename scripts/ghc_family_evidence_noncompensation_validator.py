#!/usr/bin/env python3
"""Validate a GHC Family v642-v5 non-compensation packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
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
    "fundamental_thermo_psyche_law",
    "stage20_ready",
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
    repo = phase.parents[2]
    passed: list[str] = []
    issues: list[str] = []

    def check(condition: bool, label: str) -> None:
        (passed if condition else issues).append(label)

    required = [
        "x1-proposals.json",
        "x1-preregistration.md",
        "x2-proposal-ledger.json",
        "phase-truth.json",
        "exact-open-gate-register.json",
        "retained-negative-register.json",
        "complete-incomplete-checklist.json",
        "wellbeing-check.md",
        "v642-v5-integrated-overview.md",
        "environment/startup-receipt.json",
        "environment/version-receipt.json",
        "provenance/prior-proposal-collision-audit.json",
        "provenance/frozen-chain-proposal-index.json",
        "provenance/citation-entailment-contract.json",
        "provenance/assertion-granularity-vectors.json",
        "provenance/source-scope-drift-register.json",
        "sources/source-ledger.json",
        "tooling/ghc-family-index.json",
        "tooling/selected-toolchain.json",
        "tooling/executed-toolchain.json",
        "workflow/route-preregistration.json",
        "physics/principal-symbol-obligation.json",
        "physics/constraint-propagation-vectors.json",
        "physics/well-posedness-claim-boundary.json",
        "empirical/prior-sensitivity-contract.json",
        "empirical/prior-data-conflict-vectors.json",
        "empirical/zero-row-inference-lock.json",
        "thos/scorer-reliability-preregistration.json",
        "thos/inter-rater-mutation-vectors.json",
        "thos/real-rater-arm-gap.json",
        "freed-id/resolution-egress-profile.json",
        "freed-id/redirect-metadata-leak-vectors.json",
        "freed-id/production-resolution-boundary.json",
        "cbr/dissent-recusal-authority-gate.json",
        "cbr/minority-report-vectors.json",
        "cbr/conflict-of-interest-register.json",
        "security/oracle-integrity-contract.json",
        "security/adversarial-corpus-minimization.json",
        "security/recovery-mutation-vectors.json",
        "reproduction/determinism-envelope.json",
        "reproduction/clock-locale-order-vectors.json",
        "reproduction/hermeticity-gap.json",
        "thermo-psyche/measurement-scale-classifier.json",
        "thermo-psyche/analogy-admissibility-vectors.json",
        "thermo-psyche/category-barrier.json",
        "stage20/noncompensatory-evidence-vector.json",
        "stage20/score-laundering-vectors.json",
        "stage20/terminal-verdict.json",
        "validation/execution-negative-log.json",
        "validation/repository-test-receipt.json",
        "validation/json-parse-receipt.json",
        "reproduction/manifest.json",
        "reproduction/clean-snapshot-validation.json",
    ]
    for rel in required:
        check((phase / rel).is_file(), f"required file exists: {rel}")
    if any(not (phase / rel).is_file() for rel in required):
        return {
            "schema": "ghc.family.evidence-noncompensation-validation.v1",
            "valid": False,
            "checks_passed": len(passed),
            "checks_total": len(passed) + len(issues),
            "issues": issues,
        }

    parsed: dict[Path, Any] = {}
    json_files = sorted(phase.rglob("*.json"))
    for path in json_files:
        try:
            parsed[path] = load(path)
            check(True, f"JSON parses: {path.relative_to(phase).as_posix()}")
        except Exception:
            check(False, f"JSON parses: {path.relative_to(phase).as_posix()}")

    x1 = load(phase / "x1-proposals.json")
    audit = load(phase / "provenance/prior-proposal-collision-audit.json")
    chain = load(phase / "provenance/frozen-chain-proposal-index.json")
    sources = load(phase / "sources/source-ledger.json")
    x2 = load(phase / "x2-proposal-ledger.json")
    truth = load(phase / "phase-truth.json")
    negatives = load(phase / "retained-negative-register.json")
    gates = load(phase / "exact-open-gate-register.json")
    manifest = load(phase / "reproduction/manifest.json")
    snapshot = load(phase / "reproduction/clean-snapshot-validation.json")
    route = load(phase / "workflow/route-preregistration.json")
    tests = load(phase / "validation/repository-test-receipt.json")
    json_receipt = load(phase / "validation/json-parse-receipt.json")

    check(x1["phase"] == "v642-gmut-thos-v5-x1-x2", "x1 phase identity")
    check(x1["owner"] == "Sable Rook", "x1 owner identity")
    check(x1["source_revision"] == "324f79d9a9a779e4f1b95628977561409ee12405", "exact source revision")
    check(x1["proposal_count"] == 10 and len(x1["proposals"]) == 10, "x1 exactly ten proposals")
    check(len({row["proposal_id"] for row in x1["proposals"]}) == 10, "x1 proposal identifiers unique")
    check(len({row["title"] for row in x1["proposals"]}) == 10, "x1 proposal titles unique")
    check(set(x1["outcome_classes"]) == TRUTH_LABELS, "x1 truth labels exact")
    check(x1["expected_disposition_counts"] == EXPECTED_DISTRIBUTION, "x1 expected distribution")
    check(x1["expected_counts_are_results"] is False, "x1 expected counts not results")
    check(x1["prior_frozen_proposal_count"] == 110, "x1 predecessor count")
    check(audit["prior_phase_counts"]["total"] == 110, "collision audit covers 110 predecessors")
    check(audit["exact_title_collisions"] == 0, "collision audit exact titles zero")
    check(audit["semantic_delta_review_passed"] is True, "semantic novelty review passes")
    check(len(audit["checks"]) == 10 and all(row["distinct"] for row in audit["checks"]), "ten candidates semantically distinct")
    check(len(audit["x1_execution_negatives"]) >= 5, "x1 execution negatives retained")

    check(chain["proposal_count"] == 120 and len(chain["records"]) == 120, "frozen chain has 120 records")
    check(len({row["proposal_id"] for row in chain["records"]}) == 120, "frozen chain proposal IDs unique")
    check(len({row["title"] for row in chain["records"]}) == 120, "frozen chain titles unique")
    check(chain["exact_duplicate_titles"] == [], "frozen chain duplicate titles empty")
    check(chain["version_counts"].get("v642-v5") == 10, "frozen chain includes ten v642-v5 records")

    check(sources["inherited_source_count"] == 54, "54 inherited sources")
    check(sources["added_source_count"] == 8 and len(sources["added_sources"]) == 8, "eight local sources")
    check(sources["effective_source_count"] == 62, "effective source count 62")
    check(sum(sources["effective_status_counts"].values()) == 62, "source status counts sum")
    check(set(sources["effective_status_counts"]) == {"current", "stable", "draft", "watch"}, "four source status classes")
    check(sources["effective_status_counts"]["draft"] == 5, "draft source count visible")
    check(any(row["source_id"] == "V6425-S62" and row["status_class"] == "draft" for row in sources["added_sources"]), "DID Resolution remains draft")
    check(all(row["url"].startswith("https://") for row in sources["added_sources"]), "phase source URLs use HTTPS")

    check(x2["proposal_count"] == 10 and len(x2["proposals"]) == 10, "x2 exactly ten proposals")
    check(x2["disposition_counts"] == EXPECTED_DISTRIBUTION, "x2 observed distribution exact")
    check(x2["all_executed_as_far_as_evidence_permits"] is True, "all x2 proposals executed as evidence permits")
    check(x2["x1_commit"] == truth["x1_commit"], "x1 commit consistent")
    check(x2["evidence_commit"] == truth["evidence_commit"], "evidence commit consistent")
    for row in x2["proposals"]:
        check(row["expected_disposition"] == row["observed_disposition"], f"expected and observed agree: {row['proposal_id']}")
        check(row["observed_disposition"] in TRUTH_LABELS, f"valid truth label: {row['proposal_id']}")
        check(row["executed_as_far_as_evidence_permits"] is True, f"evidence-permitted execution: {row['proposal_id']}")
        check(all((phase / rel).is_file() for rel in row["evidence"]), f"evidence files exist: {row['proposal_id']}")
        check(bool(row["protected_gates_remain"]), f"protected gates remain: {row['proposal_id']}")

    vector_paths = [
        "provenance/assertion-granularity-vectors.json",
        "physics/constraint-propagation-vectors.json",
        "empirical/prior-data-conflict-vectors.json",
        "thos/inter-rater-mutation-vectors.json",
        "freed-id/redirect-metadata-leak-vectors.json",
        "cbr/minority-report-vectors.json",
        "security/recovery-mutation-vectors.json",
        "reproduction/clock-locale-order-vectors.json",
        "thermo-psyche/analogy-admissibility-vectors.json",
        "stage20/score-laundering-vectors.json",
    ]
    for rel in vector_paths:
        rows = load(phase / rel)["vectors"]
        check(len(rows) == 3, f"three preregistered vectors: {rel}")
        check(all(row["matches_expected"] for row in rows), f"vector expectations match: {rel}")
        check(sum("negative_id" in row for row in rows) == 2, f"two retained negative vectors: {rel}")

    well_posed = load(phase / "physics/well-posedness-claim-boundary.json")
    empirical = load(phase / "empirical/zero-row-inference-lock.json")
    thos = load(phase / "thos/real-rater-arm-gap.json")
    freed = load(phase / "freed-id/production-resolution-boundary.json")
    cbr = load(phase / "cbr/dissent-recusal-authority-gate.json")
    hermetic = load(phase / "reproduction/hermeticity-gap.json")
    category = load(phase / "thermo-psyche/category-barrier.json")
    terminal = load(phase / "stage20/terminal-verdict.json")
    check(well_posed["gmut_well_posedness_established"] is False, "GMUT well-posedness not established")
    check(well_posed["empirical_confirmation"] is False, "GMUT empirical confirmation false")
    check(well_posed["theory_of_everything"] is False, "Theory of Everything false")
    check(empirical["real_measurement_rows"] == 0 and empirical["likelihood_executions"] == 0, "empirical rows and likelihood zero")
    check(empirical["promotion_allowed"] is False, "empirical promotion locked")
    check(thos["real_raters"] == 0 and thos["blind_matched_budget_real_arms"] == 0, "THOS real raters and arms zero")
    check(thos["real_thos_superiority"] is False, "THOS superiority false")
    check(all(thos[key] is False for key in ["agi", "asi", "consciousness", "personhood"]), "THOS frontier and identity claims false")
    check(sum(freed[key] for key in ["real_keys", "real_proofs", "live_resolvers_or_status_services", "interoperability_partners", "independent_security_reviews", "independent_privacy_reviews", "trust_governance_authorities"]) == 0, "Freed ID production evidence zero")
    check(freed["production_assurance"] is False, "Freed ID production assurance false")
    check(cbr["technical_artifact_can_grant_maori_authority"] is False, "technical artifact cannot grant Māori authority")
    check(cbr["authorized_participants_present"] == 0, "CBR authorized participants absent")
    check(hermetic["independent_team_count"] == 0 and hermetic["independent_reproduction_established"] is False, "independent team reproduction open")
    check(category["fundamental_thermo_psyche_law"] is False, "fundamental thermo-psyche law false")
    check(terminal["verdict"] == "NOT_READY_FOR_STAGE_20" and terminal["decision"] == "defer", "terminal verdict deferred not ready")
    check(terminal["weighted_compensation_used"] is False, "weighted compensation unused")

    prior = load(repo / "docs/ilyra-fen/v642-v4/retained-negative-register.json")
    negative_ids = [row["negative_id"] for row in negatives["negatives"]]
    prior_ids = [row["negative_id"] for row in prior["negatives"]]
    check(negatives["inherited_count"] == 120, "120 inherited negatives")
    check(negative_ids[:120] == prior_ids, "all inherited negatives byte-order preserved")
    check(negatives["new_count"] >= 25, "at least 25 phase-local negatives")
    check(negatives["negative_count"] == len(negative_ids), "negative count matches records")
    check(len(set(negative_ids)) == len(negative_ids), "negative identifiers unique")
    check(negatives["all_retained"] is True and negatives["erasure_permitted"] is False, "negative retention invariant")
    check(all(f"V6425-X1-N{number:02d}" in negative_ids for number in range(1, 6)), "five x1 negatives retained")
    check(all(f"V6425-N{number:02d}" in negative_ids for number in range(1, 21)), "twenty vector negatives retained")

    check(gates["open_gap_count"] == 5 and gates["exact_gate_count"] == 6, "five plus six gate counts")
    check(gates["silently_closed"] == 0 and len(gates["gates"]) == 11, "no gate silently closed")
    check(Counter(row["gate_class"] for row in gates["gates"]) == {"open_gap": 5, "exact_gate": 6}, "gate class distribution exact")
    check(all(row["state"] in {"open", "deferred"} for row in gates["gates"]), "all gates open or deferred")

    check(truth["proposal_count"] == 10, "phase truth proposal count")
    check(truth["disposition_counts"] == EXPECTED_DISTRIBUTION, "phase truth distribution")
    check(truth["retained_negative_count"] == negatives["negative_count"], "phase truth negative count")
    check(truth["open_gap_count"] == 5 and truth["exact_gate_count"] == 6, "phase truth gate counts")
    check(set(truth["protected_claims"]) == PROTECTED_CLAIMS, "protected claim key set exact")
    check(all(value is False for value in truth["protected_claims"].values()), "all protected claims false")
    check("Māori authority" in truth["maori_authority_boundary"], "Māori authority boundary retained")
    check(truth["independent_team_gap"] == "open", "independent team gap open")
    check(truth["route_state"] == "NO_SUCCESSOR_AUTHORIZED", "route state no successor authorized")
    check(truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", "phase truth terminal verdict")
    check(route["outbound_messages"] == 0 and route["tasks_created"] == 0, "route has zero sends and creations")
    check(route["terminal_route"]["state"] == "NO_SUCCESSOR_AUTHORIZED", "route preregistration matches phase truth")

    x1_names = subprocess.check_output(
        ["git", "-C", str(repo), "show", "--pretty=", "--name-only", x1["x1_commit"] if "x1_commit" in x1 else x2["x1_commit"]],
        text=True,
        encoding="utf-8",
    ).splitlines()
    check(len(x1_names) == 15, "x1 commit contains exactly 15 files")
    check(all(name.startswith("docs/sable-rook/v642-v5/") for name in x1_names), "x1 commit phase-scoped")
    forbidden_x1 = re.compile(r"(^scripts/|^tests/|x2-|phase-truth|closeout|seal|final-validation|deliverables/)")
    check(not [name for name in x1_names if forbidden_x1.search(name)], "x1 contains no x2 implementation")

    sealed_paths = [
        "scripts/ghc_family_claim_coherence.py",
        "scripts/ghc_family_claim_coherence_validator.py",
        "scripts/ghc_family_claim_coherence_minimal.py",
        "scripts/build_ghc_family_claim_coherence_report.py",
        "tests/test_ghc_family_v642_v4.py",
    ]
    for rel in sealed_paths:
        inherited = subprocess.check_output(
            ["git", "-C", str(repo), "show", f"324f79d9a9a779e4f1b95628977561409ee12405:{rel}"]
        )
        worktree_bytes = (repo / rel).read_bytes().replace(b"\r\n", b"\n")
        inherited_bytes = inherited.replace(b"\r\n", b"\n")
        check(worktree_bytes == inherited_bytes, f"inherited v642-v4 normalized content stable: {rel}")

    records = manifest["files"]
    check(manifest["file_count"] == len(records), "manifest count matches records")
    check(len({row["path"] for row in records}) == len(records), "manifest paths unique")
    check(manifest["same_owner_repeatability_only"] is True, "manifest bounds repeatability")
    check(manifest["independent_reproduction_established"] is False, "manifest independent reproduction false")
    for row in records:
        target = phase / row["path"]
        check(target.is_file(), f"manifest file exists: {row['path']}")
        check(target.is_file() and digest(target) == row["normalized_sha256"], f"manifest hash matches: {row['path']}")

    overview = (phase / "v642-v5-integrated-overview.md").read_text(encoding="utf-8")
    overview_words = len(re.findall(r"\b[\w'-]+\b", overview, flags=re.UNICODE))
    check(overview_words >= 1800, "overview meets three-page word floor")
    check("NOT_READY_FOR_STAGE_20" in overview, "overview terminal verdict visible")
    check("same-owner repeatability" in overview.lower(), "overview same-owner boundary visible")
    check("Māori concepts, wording, data, and governance remain under Māori authority" in overview, "overview Māori authority boundary visible")
    check("NO_SUCCESSOR_AUTHORIZED" in overview, "overview route truth visible")

    if allow_pending_snapshot:
        check(snapshot["state"] in {"pending", "verified"}, "snapshot state allowed during candidate validation")
        check(x2["snapshot_state"] in {"pending", "verified"}, "x2 snapshot state allowed during candidate validation")
        check(tests["state"] in {"pending", "verified"}, "test receipt state allowed during candidate validation")
        check(json_receipt["state"] in {"pending", "verified"}, "JSON receipt state allowed during candidate validation")
    else:
        check(snapshot["state"] == "verified" and snapshot["snapshot_count"] >= 2, "clean snapshot validation verified")
        check(snapshot["hash_mismatches"] == 0, "clean snapshot manifest parity")
        check(x2["snapshot_state"] == "verified", "x2 snapshot state verified")
        check(re.fullmatch(r"[0-9a-f]{40}", x2["evidence_commit"]) is not None, "evidence commit exact SHA")
        check(truth["same_owner_repeatability"] == "verified_bounded", "same-owner repeatability bounded")
        check(tests["state"] == "verified" and tests["tests_run"] >= 250 and tests["failures"] == 0 and tests["errors"] == 0, "repository tests verified")
        check(json_receipt["state"] == "verified" and json_receipt["errors"] == 0, "JSON receipt verified")
    check(snapshot["independent_reproduction_established"] is False, "snapshot evidence not independent reproduction")

    report_path = phase / "deliverables/v642-v5-noncompensation-report.html"
    if require_report:
        check(report_path.is_file(), "static HTML report exists")
        report = report_path.read_text(encoding="utf-8") if report_path.is_file() else ""
        for token, label in [
            ('<html lang="en">', "report language"),
            ('href="#main"', "report skip link"),
            ('<main id="main">', "report main landmark"),
            ('<th scope="col">', "report table headers"),
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
                privacy_hits.append({
                    "file": path.relative_to(phase).as_posix(),
                    "class": name,
                    "sample": match.group(0)[:80],
                })
    check(not privacy_hits, "concrete-value privacy scan has zero hits")

    for optional, fields in [
        ("closeout-receipt.json", ["state", "evidence_commit", "terminal_verdict"]),
        ("seal-receipt.json", ["state", "closeout_commit", "terminal_verdict"]),
        ("final-validation-record.json", ["state", "seal_commit", "terminal_verdict"]),
    ]:
        path = phase / optional
        if path.is_file():
            value = load(path)
            check(all(field in value for field in fields), f"optional receipt fields: {optional}")
            check(value["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", f"optional receipt terminal verdict: {optional}")

    return {
        "schema": "ghc.family.evidence-noncompensation-validation.v1",
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
        "route_state": truth["route_state"],
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
