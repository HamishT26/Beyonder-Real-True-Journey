from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}
REQUIRED = [
    "x1-proposals.json",
    "sources/source-ledger.json",
    "provenance/sequential-ancestry.json",
    "provenance/cumulative-dependency-graph.json",
    "provenance/x1-x2-boundary-audit.json",
    "physics/equation-register-covenant.json",
    "physics/translation-typecheck.json",
    "physics/null-limit-and-conservation-audit.json",
    "falsification/inherited-negative-register.json",
    "falsification/mutation-tribunal.json",
    "falsification/negative-to-downgrade-trace.json",
    "empirical/promotion-docket.json",
    "empirical/baseline-authorization-boundary.json",
    "empirical/missing-evidence-register.json",
    "thos/observed-coordination-costs.json",
    "thos/observed-versus-proxy-ledger.json",
    "thos/blind-evidence-audit.json",
    "thermo-psyche/candidate-register.json",
    "thermo-psyche/classification-tribunal.json",
    "thermo-psyche/mutation-results.json",
    "freed-id/assurance-lattice.json",
    "freed-id/non-escalation-proof.json",
    "freed-id/composition-gap-register.json",
    "cbr/authority-matrix.json",
    "cbr/empty-chair-veto.json",
    "cbr/dissent-remedy-and-revocation-gate.json",
    "assurance/cumulative-privacy-security-replay.json",
    "assurance/cross-owner-internal-reproduction.json",
    "assurance/inherited-negative-replay.json",
    "reproduction/manifest.json",
    "reproduction/hash-parity.json",
    "reproduction/reproduction-report.json",
    "reproduction/negative-replay.json",
    "stage20/terminal-evidence-board.json",
    "stage20/claim-sunset-register.json",
    "stage20/external-review-packet.json",
    "x2-proposal-ledger.json",
    "phase-truth.json",
    "complete-incomplete-checklist.json",
    "v641-v6-integrated-overview.md",
    "deliverables/v641-v6-terminal-evidence-report.html",
    "validation/accessibility-audit.json",
    "validation/privacy-scan.json",
    "validation/retained-negative-results.json",
    "validation/test-receipt.json",
]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the additive v641-v6 terminal packet.")
    parser.add_argument("--phase-dir", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    phase = args.phase_dir.resolve()
    output = (args.output or phase / "validation/core-validation.json").resolve()
    issues: list[str] = []

    for rel in REQUIRED:
        if not (phase / rel).is_file():
            issues.append(f"missing required artifact: {rel}")

    json_files = list(phase.rglob("*.json"))
    parsed: dict[Path, Any] = {}
    for path in json_files:
        try:
            parsed[path] = load(path)
        except Exception as exc:
            issues.append(f"invalid JSON {path.relative_to(phase)}: {exc}")

    def data(rel: str) -> Any:
        return parsed.get(phase / rel, {})

    x1 = data("x1-proposals.json")
    ledger = data("x2-proposal-ledger.json")
    truth = data("phase-truth.json")
    board = data("stage20/terminal-evidence-board.json")
    negatives = data("falsification/inherited-negative-register.json")
    empirical = data("empirical/promotion-docket.json")
    thos = data("thos/blind-evidence-audit.json")
    freed = data("freed-id/assurance-lattice.json")
    cbr = data("cbr/authority-matrix.json")
    ancestry = data("provenance/sequential-ancestry.json")
    typecheck = data("physics/translation-typecheck.json")
    thermo = data("thermo-psyche/candidate-register.json")
    reproduction = data("reproduction/reproduction-report.json")
    parity = data("reproduction/hash-parity.json")
    privacy = data("validation/privacy-scan.json")
    accessibility = data("validation/accessibility-audit.json")
    tests = data("validation/test-receipt.json")

    proposals = x1.get("proposals", [])
    if len(proposals) != 10 or len({row.get("proposal_id") for row in proposals}) != 10:
        issues.append("x1 must contain exactly ten unique proposals")
    rows = ledger.get("rows", [])
    if len(rows) != 10 or len({row.get("proposal_id") for row in rows}) != 10:
        issues.append("x2 ledger must contain exactly ten unique rows")
    dispositions = [row.get("disposition") for row in rows]
    if not set(dispositions) <= ALLOWED:
        issues.append("x2 ledger contains an invalid truth label")
    expected_counts = {key: dispositions.count(key) for key in ["completed", "represented", "open_gap", "exact_gate"]}
    if ledger.get("disposition_counts") != expected_counts:
        issues.append("ledger disposition counts do not reconcile")
    if truth.get("disposition_counts") != expected_counts or board.get("disposition_counts") != expected_counts:
        issues.append("truth or Stage 20 counts disagree with the ledger")
    if expected_counts not in [
        {"completed": 5, "represented": 1, "open_gap": 3, "exact_gate": 1},
        {"completed": 6, "represented": 1, "open_gap": 2, "exact_gate": 1},
    ]:
        issues.append("distribution is outside the preregistered pending or verified ceiling")

    if not ancestry.get("all_edges_strict"):
        issues.append("sequential ancestry did not pass")
    if not typecheck.get("all_category_barriers_hold"):
        issues.append("translation category barriers did not hold")
    required_inherited = {"REPRO-V4-N01", "REPRO-V4-N02", "VALID-V5-N01", "VALID-V5-N02", "COMPAT-V5-N03", "CLI-V5-N04", "REPRO-V5-N05"}
    negative_ids = set(negatives.get("negative_ids", []))
    if negatives.get("negative_count") != 9 or len(negative_ids) != 9 or not required_inherited <= negative_ids:
        issues.append("seven inherited plus two observed v6 negatives must be retained")
    if thermo.get("candidate_count") != 7 or thermo.get("fundamental_physical_laws_established") != 0:
        issues.append("thermo-psyche classification inflated a fundamental-law claim")
    if empirical.get("promotion_authorized") is not False or empirical.get("gmute_confirmation") is not False:
        issues.append("empirical promotion must remain blocked")
    if thos.get("disposition") != "represented" or thos.get("matched_budget_real_arms") is not False:
        issues.append("THOS must remain represented without real arms")
    if freed.get("current_highest_level") != "L1_structural" or freed.get("current_disposition") != "open_gap":
        issues.append("Freed ID assurance state is inflated")
    if cbr.get("disposition") != "exact_gate" or cbr.get("enactment_authorized") is not False:
        issues.append("CBR authority gate is not preserved")
    if board.get("terminal_verdict") != "NOT_READY_FOR_STAGE_20":
        issues.append("Stage 20 verdict must remain NOT_READY")
    if any(value is not False for value in board.get("protected_claims", {}).values()):
        issues.append("one or more protected claims were promoted")

    state = reproduction.get("state")
    if state == "cross_owner_internal_repeatability_verified":
        if not parity.get("verified") or reproduction.get("verified_snapshot_count", 0) < 2:
            issues.append("verified reproduction lacks two matching snapshots")
        if expected_counts != {"completed": 6, "represented": 1, "open_gap": 2, "exact_gate": 1}:
            issues.append("verified reproduction must resolve to 6/1/2/1")
    elif state == "pending_clean_snapshots":
        if expected_counts != {"completed": 5, "represented": 1, "open_gap": 3, "exact_gate": 1}:
            issues.append("pending reproduction must remain 5/1/3/1")
    else:
        issues.append("unknown reproduction state")
    if reproduction.get("independent_scientific_reproduction") is not False:
        issues.append("internal replay was mislabeled independent")

    if privacy.get("valid") is not True or privacy.get("hit_count") != 0:
        issues.append("privacy scan is not a zero-hit valid receipt")
    if accessibility.get("valid") is not True or accessibility.get("full_wcag_conformance_established") is not False:
        issues.append("accessibility boundary is invalid")
    if tests.get("failed") != 0 or tests.get("passed", 0) < 100:
        issues.append("full inherited plus v6 test receipt is incomplete")

    overview = (phase / "v641-v6-integrated-overview.md").read_text(encoding="utf-8") if (phase / "v641-v6-integrated-overview.md").exists() else ""
    overview_words = len(re.findall(r"\b\w+[\w'-]*\b", overview))
    if overview_words < 2000:
        issues.append(f"integrated overview is too short: {overview_words} words")
    report = (phase / "deliverables/v641-v6-terminal-evidence-report.html").read_text(encoding="utf-8") if (phase / "deliverables/v641-v6-terminal-evidence-report.html").exists() else ""
    for marker in ['<html lang="en">', '<main id="main">', 'aria-label="Report sections"', "NOT_READY_FOR_STAGE_20"]:
        if marker not in report:
            issues.append(f"report structural marker missing: {marker}")

    receipt = {
        "schema": "ghc.family.terminal-evidence-validation.v6",
        "phase": "v641-gmut-thos-v6-x1-x2",
        "valid": not issues,
        "issues": issues,
        "required_artifact_count": len(REQUIRED),
        "json_file_count": len(json_files),
        "proposal_count": len(rows),
        "disposition_counts": expected_counts,
        "negative_count": negatives.get("negative_count"),
        "overview_word_count": overview_words,
        "privacy_scanned_file_count": privacy.get("scanned_file_count"),
        "privacy_hit_count": privacy.get("hit_count"),
        "tests_passed": tests.get("passed"),
        "reproduction_state": state,
        "terminal_verdict": board.get("terminal_verdict"),
        "boundary": "Validation covers local artifacts and declared checks only; external scientific legal cultural deployment security accessibility consciousness personhood and independence claims remain unestablished.",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0 if receipt["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
