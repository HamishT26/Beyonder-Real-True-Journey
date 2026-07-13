#!/usr/bin/env python3
"""Validate the bounded v641-v7 chain falsification packet."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


EXPECTED_SOURCE = "313517217ddb820efb4c3fbbcdcfc3bed76ad429"
EXPECTED_X1 = "f6281f48a3fad5b918df870117d2d02fdd4dba26"
EXPECTED_EQUATIONS = [
    "G_{mu nu} + Lambda g_{mu nu} = M_Pl^{-2} T^{SM}_{mu nu} + Omega_{mu nu}",
    "Omega_{mu nu} = M_Pl^{-2} (T^phi_{mu nu} + T^{EFT}_{mu nu})",
]
ALLOWED_DISPOSITIONS = {"completed", "represented", "open_gap", "exact_gate"}
REQUIRED_FILES = [
    "x1-proposals.json",
    "x1-preregistration.md",
    "x2-proposal-ledger.json",
    "x2-proposal-ledger.md",
    "phase-truth.json",
    "phase-truth.md",
    "retained-negative-register.json",
    "complete-incomplete-checklist.json",
    "complete-incomplete-checklist.md",
    "exact-open-gate-register.json",
    "v641-v7-integrated-overview.md",
    "wellbeing-check.md",
    "sources/source-ledger.json",
    "provenance/frozen-chain-proposal-index.json",
    "provenance/authority-root-knockout.json",
    "provenance/claim-survival-ledger.json",
    "provenance/semantic-deduplication-report.json",
    "physics/canonical-gmut-register.json",
    "physics/identifiability-rank-battery.json",
    "physics/conservation-obligation-register.json",
    "physics/reparameterization-counterexamples.json",
    "empirical/public-release-adapter-contract.json",
    "empirical/cross-release-leakage-vectors.json",
    "empirical/official-metadata-handshake.json",
    "empirical/no-fit-receipt.json",
    "thos/outcome-sealed-arm-packet.json",
    "thos/exchangeability-sentinels.json",
    "thos/negative-control-rehearsal.json",
    "thos/real-arm-gap.json",
    "freed-id/stable-draft-watch-conformance-matrix.json",
    "freed-id/resolution-status-fault-vectors.json",
    "freed-id/privacy-minimization-receipt.json",
    "freed-id/interoperability-trust-gap.json",
    "cbr/rights-floor-precedence-casebook.json",
    "cbr/affected-party-legitimacy-register.json",
    "cbr/maori-authority-boundary.json",
    "cbr/legal-and-cultural-exact-gates.json",
    "security/threat-model.md",
    "security/adversarial-encoding-vectors.json",
    "security/provenance-poisoning-vectors.json",
    "security/recovery-drill.json",
    "security/privacy-raw-id-controls.json",
    "reproduction/common-mode-independence-budget.json",
    "reproduction/clean-snapshot-manifest.json",
    "reproduction/repeatability-receipt.json",
    "reproduction/independent-team-gap.json",
    "thermo-psyche/six-class-rubric.json",
    "thermo-psyche/counterfactual-relabel-vectors.json",
    "thermo-psyche/category-drift-rejections.json",
    "thermo-psyche/classification-tribunal.json",
    "stage20/claim-expiry-matrix.json",
    "stage20/pass-fail-defer-register.json",
    "stage20/falsifier-linkage.json",
    "stage20/terminal-evidence-board.json",
    "environment/startup-receipt.json",
    "environment/version-receipt.json",
    "tooling/ghc-family-index.json",
    "tooling/selected-toolchain.json",
]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(phase: Path, allow_pending: bool, require_report: bool, output: Path | None) -> dict:
    issues: list[str] = []
    checks: list[str] = []

    for rel in REQUIRED_FILES:
        if not (phase / rel).is_file():
            issues.append(f"missing required artifact: {rel}")
    if issues:
        return {"schema":"ghc.family.v641-v7.validation.v1","valid":False,"issues":issues,"checks":checks}
    checks.append("required_artifacts_present")

    parsed = {}
    for path in sorted(phase.rglob("*.json")):
        if output and path.resolve() == output.resolve():
            continue
        try:
            parsed[path.relative_to(phase).as_posix()] = read_json(path)
        except Exception as exc:
            issues.append(f"json parse failed: {path.relative_to(phase).as_posix()}: {exc}")
    checks.append("json_parse")

    x1 = parsed["x1-proposals.json"]
    x2 = parsed["x2-proposal-ledger.json"]
    truth = parsed["phase-truth.json"]
    if x1.get("source_revision") != EXPECTED_SOURCE or truth.get("source_revision") != EXPECTED_SOURCE:
        issues.append("source revision mismatch")
    if truth.get("x1_commit") != EXPECTED_X1:
        issues.append("x1 commit mismatch")
    if x1.get("proposal_count") != 10 or len(x1.get("proposals", [])) != 10:
        issues.append("x1 proposal count must be ten")
    if x2.get("proposal_count") != 10 or len(x2.get("proposals", [])) != 10:
        issues.append("x2 proposal count must be ten")
    ids = [row.get("proposal_id") for row in x2.get("proposals", [])]
    if len(ids) != len(set(ids)) or set(ids) != {f"V7-P{i:02d}" for i in range(1, 11)}:
        issues.append("x2 proposal IDs are not the exact unique V7-P01..V7-P10 set")
    dispositions = [row.get("observed_disposition") for row in x2.get("proposals", [])]
    if not set(dispositions) <= ALLOWED_DISPOSITIONS:
        issues.append("invalid disposition class")
    if Counter(dispositions) != Counter(x2.get("disposition_counts", {})):
        issues.append("x2 disposition counts mismatch")
    checks.append("proposal_ledgers")

    snapshot_state = x2.get("snapshot_state")
    if snapshot_state == "verified":
        expected = Counter({"completed":6,"represented":2,"open_gap":1,"exact_gate":1})
        if Counter(dispositions) != expected:
            issues.append("verified final disposition counts must be 6/2/1/1")
    elif snapshot_state == "pending" and allow_pending:
        expected = Counter({"completed":5,"represented":2,"open_gap":2,"exact_gate":1})
        if Counter(dispositions) != expected:
            issues.append("pending candidate disposition counts must be 5/2/2/1")
    else:
        issues.append("detached snapshot validation is not verified")
    checks.append("snapshot_state_and_dispositions")

    chain = parsed["provenance/frozen-chain-proposal-index.json"]
    collision = parsed["provenance/semantic-deduplication-report.json"]
    knockout = parsed["provenance/authority-root-knockout.json"]
    if chain.get("proposal_count") != 60 or chain.get("version_counts") != {"v2":10,"v3":10,"v4":10,"v5":10,"v6":10,"v7":10}:
        issues.append("frozen-chain index must contain ten proposals per v2-v7 phase")
    if collision.get("exact_title_collisions") != 0 or not collision.get("pass"):
        issues.append("semantic deduplication failed")
    if knockout.get("unsafe_strength_retention_count") != 0 or not knockout.get("pass"):
        issues.append("authority-root knockout retained unsafe strength")
    checks.append("provenance_and_deduplication")

    physics = parsed["physics/canonical-gmut-register.json"]
    rank = parsed["physics/identifiability-rank-battery.json"]
    obligations = parsed["physics/conservation-obligation-register.json"]
    if physics.get("equations") != EXPECTED_EQUATIONS:
        issues.append("canonical GMUT equations changed")
    if physics.get("empirical_confirmation") or physics.get("unique_prediction") or physics.get("theory_of_everything"):
        issues.append("physics scaffold is overclaimed")
    if not rank.get("all_expected_ranks_observed") or rank.get("empirical_identifiability_established"):
        issues.append("identifiability rank boundary failed")
    if obligations.get("nature_claim"):
        issues.append("formal conservation obligation was promoted to a nature claim")
    checks.append("canonical_gmut_rank_conservation_stability")

    handshake = parsed["empirical/official-metadata-handshake.json"]
    no_fit = parsed["empirical/no-fit-receipt.json"]
    leakage = parsed["empirical/cross-release-leakage-vectors.json"]
    if not leakage.get("all_mutations_detected") or handshake.get("real_measurement_rows_parsed") != 0:
        issues.append("empirical adapter leakage or measurement boundary failed")
    if any(no_fit.get(key) for key in ["real_data_downloaded","likelihood_executed","parameter_fit_executed","empirical_gmut_confirmation"]):
        issues.append("no-fit receipt overclaims empirical execution")
    checks.append("empirical_adapter_no_fit")

    arms = parsed["thos/outcome-sealed-arm-packet.json"]
    sentinels = parsed["thos/exchangeability-sentinels.json"]
    thos_gap = parsed["thos/real-arm-gap.json"]
    if arms.get("real_model_runs") != 0 or not arms.get("synthetic_only") or not sentinels.get("all_mutations_rejected_before_unseal"):
        issues.append("THOS synthetic rehearsal boundary failed")
    if thos_gap.get("real_arms_present") or thos_gap.get("disposition") != "represented":
        issues.append("THOS real-arm gap missing")
    checks.append("thos_blind_matched_budget_proxy")

    freed = parsed["freed-id/stable-draft-watch-conformance-matrix.json"]
    freed_faults = parsed["freed-id/resolution-status-fault-vectors.json"]
    freed_gap = parsed["freed-id/interoperability-trust-gap.json"]
    if freed.get("stable_pin_count") != 4 or freed.get("draft_or_watch_count") != 3 or freed.get("production_assurance"):
        issues.append("Freed ID stable/draft/watch boundary failed")
    if not freed_faults.get("all_faults_rejected") or freed_gap.get("disposition") != "open_gap":
        issues.append("Freed ID fault or open-gap result failed")
    checks.append("freed_id_structural_only")

    cbr = parsed["cbr/rights-floor-precedence-casebook.json"]
    maori = parsed["cbr/maori-authority-boundary.json"]
    gates = parsed["cbr/legal-and-cultural-exact-gates.json"]
    if cbr.get("algorithmic_resolutions") != 0 or not cbr.get("all_live_conflicts_deferred"):
        issues.append("CBR authority conflicts were not deferred")
    if maori.get("Māori_authority_present") or maori.get("system_may_speak_for_Māori") or maori.get("decision") != "exact_gate":
        issues.append("Māori authority boundary failed")
    if gates.get("satisfied") or gates.get("disposition") != "exact_gate":
        issues.append("CBR exact gates were silently satisfied")
    checks.append("cbr_legitimacy_and_authority")

    encoding = parsed["security/adversarial-encoding-vectors.json"]
    poisoning = parsed["security/provenance-poisoning-vectors.json"]
    recovery = parsed["security/recovery-drill.json"]
    privacy_controls = parsed["security/privacy-raw-id-controls.json"]
    if not encoding.get("all_seeded_classes_detected") or encoding.get("exhaustive_security"):
        issues.append("bounded security vector result failed")
    if not poisoning.get("all_rejected") or not recovery.get("pass") or recovery.get("destructive_commands") != 0:
        issues.append("provenance poisoning or recovery result failed")
    if not privacy_controls.get("pass") or privacy_controls.get("fixture_values_emitted"):
        issues.append("privacy raw-ID controls failed")
    checks.append("threat_model_negative_tests_recovery")

    repeat = parsed["reproduction/repeatability-receipt.json"]
    budget = parsed["reproduction/common-mode-independence-budget.json"]
    independent = parsed["reproduction/independent-team-gap.json"]
    if snapshot_state == "verified" and not (repeat.get("snapshot_a_passed") and repeat.get("snapshot_b_passed") and repeat.get("hash_parity")):
        issues.append("verified snapshots lack parity receipt")
    if budget.get("independent_team_reproduction") or independent.get("independent_team_present") or independent.get("gap") != "open":
        issues.append("independent reproduction gap was closed without evidence")
    checks.append("repeatability_and_independence_budget")

    rubric = parsed["thermo-psyche/six-class-rubric.json"]
    relabel = parsed["thermo-psyche/counterfactual-relabel-vectors.json"]
    tribunal = parsed["thermo-psyche/classification-tribunal.json"]
    expected_classes = {"formal_invariant","operational_rule","normative_principle","heuristic","empirical_hypothesis","category_barrier"}
    if set(rubric.get("classes", {})) != expected_classes or rubric.get("fundamental_law_class_present"):
        issues.append("six-class thermo-psyche rubric failed")
    if relabel.get("vector_count") != 36 or not relabel.get("all_labels_change_obligations"):
        issues.append("counterfactual relabel battery failed")
    if tribunal.get("fundamental_physical_laws_established") != 0 or tribunal.get("consciousness_tensors_established") != 0:
        issues.append("thermo-psyche classification was overclaimed")
    checks.append("thermo_psyche_six_class_adjudication")

    expiry = parsed["stage20/claim-expiry-matrix.json"]
    board = parsed["stage20/terminal-evidence-board.json"]
    register = parsed["stage20/pass-fail-defer-register.json"]
    board_ids = [row.get("board_id") for row in board.get("board", [])]
    if len(board_ids) != len(set(board_ids)) or not expiry.get("all_have_falsifier") or not expiry.get("all_have_expiry_or_reopen"):
        issues.append("Stage 20 claim linkage is incomplete")
    if register.get("defer_counted_as_pass") or board.get("terminal_verdict") != "NOT_READY_FOR_STAGE_20" or board.get("stage20_complete"):
        issues.append("Stage 20 terminal boundary failed")
    checks.append("stage20_pass_fail_defer_board")

    negatives = parsed["retained-negative-register.json"]
    if negatives.get("negative_count", 0) < 17 or not negatives.get("all_retained") or not all(row.get("retained") for row in negatives.get("negatives", [])):
        issues.append("retained-negative register is incomplete")
    checks.append("retained_negatives")

    sources = parsed["sources/source-ledger.json"]
    if sources.get("source_count") != 31 or Counter(row["status_class"] for row in sources.get("sources", [])) != Counter(sources.get("status_counts", {})):
        issues.append("source ledger count or status classes mismatch")
    if set(sources.get("allowed_status_classes", [])) != {"current","stable","draft","watch"}:
        issues.append("source status vocabulary drifted")
    checks.append("source_ledger")

    if truth.get("terminal_verdict") != "NOT_READY_FOR_STAGE_20" or any(truth.get("protected_claims", {}).values()):
        issues.append("phase truth contains a protected overclaim")
    if truth.get("disposition_counts") != x2.get("disposition_counts"):
        issues.append("phase truth and x2 disposition counts differ")
    overview = (phase / "v641-v7-integrated-overview.md").read_text(encoding="utf-8")
    if len(re.findall(r"\b\w+\b", overview)) < 1800:
        issues.append("integrated overview is below the three-page-equivalent floor")
    checks.append("phase_truth_and_overview")

    patterns = {
        "raw_uuid_task_or_thread_id": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "windows_absolute_path": re.compile(r"\b[A-Za-z]:\\"),
        "openai_style_secret": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
        "private_key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    }
    privacy_hits = []
    for path in sorted(phase.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".json", ".md", ".html", ".txt", ".tex"}:
            continue
        if output and path.resolve() == output.resolve():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for name, pattern in patterns.items():
            if pattern.search(text):
                privacy_hits.append({"file":path.relative_to(phase).as_posix(),"pattern":name})
    if privacy_hits:
        issues.append(f"privacy/raw-ID hits: {privacy_hits}")
    checks.append("privacy_raw_id_scan")

    stale = []
    for path in sorted(phase.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".json", ".md", ".html"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if '"schema": "ghc.family.phase-truth.v6"' in text or '"schema": "ghc.family.complete-incomplete-checklist.v6"' in text:
            stale.append(path.relative_to(phase).as_posix())
    if stale:
        issues.append(f"stale v6 phase labels in v7 artifacts: {stale}")
    checks.append("stale_label_review")

    if require_report:
        report_path = phase / "deliverables/v641-v7-chain-audit-report.html"
        if not report_path.is_file():
            issues.append("accessible static report missing")
        else:
            html = report_path.read_text(encoding="utf-8")
            required_tokens = ['lang="en"', '<main', '<nav', '<h1', '<caption>', 'scope="col"', 'class="skip-link"']
            if any(token not in html for token in required_tokens):
                issues.append("static report structural accessibility markers missing")
            if "complete WCAG conformance" not in html or "not" not in html:
                issues.append("static report accessibility non-claim missing")
        checks.append("static_report_structure")

    return {
        "schema":"ghc.family.v641-v7.validation.v1",
        "phase":"v641-gmut-thos-v7-x1-x2",
        "snapshot_state":snapshot_state,
        "allow_pending_snapshots":allow_pending,
        "require_report":require_report,
        "check_count":len(checks),
        "checks":checks,
        "issue_count":len(issues),
        "issues":issues,
        "valid":not issues,
        "boundary":"A valid packet proves internal structural and audit checks only; it does not satisfy the retained empirical, authority, production, security, accessibility, or independent-reproduction gates.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--phase-dir", required=True, type=Path)
    parser.add_argument("--allow-pending-snapshots", action="store_true")
    parser.add_argument("--require-report", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    if str(repo) not in sys.path:
        sys.path.insert(0, str(repo))
    phase = args.phase_dir.resolve()
    report = validate(phase, args.allow_pending_snapshots, args.require_report, args.output)
    encoded = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
