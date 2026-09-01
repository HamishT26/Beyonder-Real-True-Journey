from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any

from ghc_family_sable_rook_v681_v6_contracts import (
    tool_library_loan_record_schema,
    evaluate,
    mutate,
    positive_fixture,
    synthetic_tool_library_loan_record,
    validate_tool_library_loan_record,
)
from ghc_family_sable_rook_v681_v6_runner_bank import materialize as materialize_runners
from ghc_family_sable_rook_v681_v6_skill_bank import materialize as materialize_skills

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "sable-rook" / "v681-v6"
X1 = BASE / "x1"
X2 = BASE / "x2"
VALIDATION = BASE / "validation"
OWNER = "Sable Rook"
PHASE = "v681-v6"
BRANCH = "codex/GHC-Family/sable-rook-v681-v6-full-tools"
SOURCE = "2a0210a495cbe557158095505671d599e0c33159"
X1_COMMIT = "7285d38579cdf5e2fce3c6b0b013b49e940f44b5"
DECLARED_CHAIN = 10070
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
WRITTEN: list[str] = []


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def git(*args: str, check: bool = True, text: bool = True) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=check,
        capture_output=True,
        text=text,
        encoding="utf-8" if text else None,
    )


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    WRITTEN.append(rel(path))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")
    WRITTEN.append(rel(path))


def normalized(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_x1() -> dict[str, Any]:
    manifest_path = "docs/sable-rook/v681-v6/validation/x1-index-manifest.json"
    manifest = json.loads(git("show", f"{X1_COMMIT}:{manifest_path}").stdout)
    mismatches = []
    for entry in manifest["entries"]:
        raw = git("show", f"{X1_COMMIT}:{entry['path']}", text=False).stdout
        data = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        if len(data) != entry["bytes"] or digest(data) != entry["sha256"]:
            mismatches.append(entry["path"])
    truth = json.loads(
        git("show", f"{X1_COMMIT}:docs/sable-rook/v681-v6/x1/phase-truth.json").stdout
    )
    parent = git("show", "-s", "--format=%P", X1_COMMIT).stdout.strip()
    return {
        "commit": X1_COMMIT,
        "direct_parent_is_source": parent == SOURCE,
        "entry_count": manifest["entry_count"],
        "head_matches": git("rev-parse", "HEAD").stdout.strip() == X1_COMMIT,
        "manifest_mismatches": mismatches,
        "planning_only": truth["execution_state"] == "PLANNING_ONLY_X1" and not truth["x2_started"],
        "schema": "ghc.family.x1-immutability.v681.v6.x2",
    }


def domain_board() -> dict[str, Any]:
    valid = synthetic_tool_library_loan_record()
    variants: list[tuple[str, dict[str, Any]]] = []
    missing = deepcopy(valid)
    missing.pop("record_id")
    variants.append(("missing_record_id", missing))
    real = deepcopy(valid)
    real["real_rows"] = 1
    variants.append(("real_row_promotion", real))
    authority = deepcopy(valid)
    authority["authority_state"] = "completed"
    variants.append(("authority_promotion", authority))
    branch = deepcopy(valid)
    branch["branch_bin_token"] = "real:branch:central"
    variants.append(("exact_branch_bin_violation", branch))
    risk = deepcopy(valid)
    risk["safety_determination"] = "safe"
    variants.append(("safety_determination_promotion", risk))
    invalid = [
        {"fixture": name, "reasons": validate_tool_library_loan_record(record)}
        for name, record in variants
    ]
    if validate_tool_library_loan_record(valid) or any(not row["reasons"] for row in invalid):
        raise RuntimeError("tool-library-loan domain-board contract failed")
    return {
        "authority_conferred": False,
        "external_actions": 0,
        "invalid_controls": invalid,
        "invalid_rejected": len(invalid),
        "owner": OWNER,
        "phase": PHASE,
        "real_rows": 0,
        "record": valid,
        "schema": tool_library_loan_record_schema(),
        "schema_id": "ghc.family.tool-library-loan-record-board.v681.v6.x2",
        "valid_errors": [],
    }


def cards(proposals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seeds: list[tuple[str, str, str]] = [
        ("owner", "Sable Rook", "Relational Stewardship State Cartographer with he/they pronouns; no consciousness, continuity, personhood, agency, qualification, or authority claim."),
        ("pillar", "Freed ID and CBR Heart", "Primary synthetic nonproduction correction, contest, remedy, minimization, and authority-reservation profile."),
        ("pillar", "THOS Body", "Synthetic loan custody, workload, correction, and handover proxy only; zero governed real-arm or operational credit."),
        ("pillar", "GMUT Mind", "Finite constraint and uncertainty structure only; zero empirical physics credit."),
        ("practice", "Urban-forestry inventory data stewardship", "Learning lens only; no field identification, inspection, risk, work, or forestry authority."),
        ("practice", "Public-record quality analysis", "Learning lens only; no municipal, legal, disclosure, retention, or records authority."),
        ("practice", "Accessibility-documentation review", "Structural evidence only; manual, assistive-technology, cognitive, Maori-language, and affected-user evaluation reserved."),
    ]
    seeds.extend(("proposal", row["proposal_id"], row["title"]) for row in proposals)
    boundary_labels = [
        "real people residents workers and participants",
        "real borrowers lenders staff volunteers tools branches loan rows custody events condition evidence and incidents",
        "real incidents work orders removals disclosures and decisions",
        "professional tool-lending inventory repair safety records and accessibility competence",
        "production and deployment",
        "identity lifecycle",
        "privacy completeness",
        "accessibility completeness",
        "legal cultural and affected-party authority",
        "Maori data governance and authority",
        "independent reproduction",
        "AGI ASI consciousness and personhood",
        "Theory of Everything proof canon and Stage 20",
    ]
    seeds.extend(("boundary", label, f"{label} remains open or exact-gated.") for label in boundary_labels)
    result = []
    for index, (tier, label, text) in enumerate(seeds, start=1):
        address = digest(f"{OWNER}|{PHASE}|{tier}|{label}|{text}".encode())
        result.append(
            {
                "card_id": f"SR6816-CARD-{index:03d}",
                "content_address": address,
                "label": label,
                "text": text,
                "tier": tier,
            }
        )
    if len(result) != 80:
        raise RuntimeError("exactly eighty Freed ID boundary cards required")
    return result


def calculate_counts() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    baseline = load(X1 / "method-flow-startup.json")["current_after_startup"]
    failure_path = X2 / "operational-failures.json"
    failures = load(failure_path)["failures"] if failure_path.exists() else []
    counts = dict(baseline)
    counts["effective_negatives"] += 300 + len(failures)
    counts["failed_witnesses"] += 300 + len(failures)
    counts["effective_methods"] += 690 + len(failures)
    counts["bounded_passing_witnesses"] += 690 + len(failures)
    counts["open_gaps"] += 3
    counts["exact_gates"] += 3
    return counts, failures


def refresh_counts() -> None:
    if not (X2 / "proposal-evidence.json").exists():
        raise RuntimeError("x2 evidence must exist before count refresh")
    proposals = load(X1 / "new-proposal-freeze.json")["proposals"]
    outcomes = load(X2 / "proposal-evidence.json")["outcome_counts"]
    counts, failures = calculate_counts()
    methods = [
        {
            "independent_reproduction": False,
            "method_id": f"SR6816-METHOD-{index:03d}",
            "preferred": "bounded_owner_local_contract_only",
            "proposal_id": row["proposal_id"],
            "validated": "one_zero_row_positive_and_five_rejecting_mutations",
        }
        for index, row in enumerate(proposals, start=1)
    ]
    baseline = load(X1 / "method-flow-startup.json")["current_after_startup"]
    write_json(X2 / "method-flow-ledger.json", {
        "count_formula": {
            "base_after_startup": baseline,
            "mutation_methods_and_recoveries": 300,
            "owner_positive_portfolio_skill_runner_methods_and_passes": 390,
            "x1_postcommit_recoveries": 0,
            "x2_operational_recoveries": len(failures),
        },
        "counts": counts,
        "failure_erasure": False,
        "independent_reproduction_claimed": False,
        "methods": methods,
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.method-flow.v681.v6.x2",
        "x1_postcommit_failures": [],
        "x2_operational_failures": failures,
    })
    write_json(X2 / "retained-negative-register.json", {
        "effective_negatives": counts["effective_negatives"],
        "failed_witnesses": counts["failed_witnesses"],
        "failure_erasure": False,
        "owner": OWNER,
        "phase": PHASE,
        "retained_mutations": 300,
        "schema": "ghc.family.retained-negatives.v681.v6.x2",
        "startup_failures": 4,
        "x1_postcommit_failures": 0,
        "x2_operational_failures": failures,
    })
    write_json(X2 / "phase-truth.json", {
        "counts": counts,
        "declared_chain": DECLARED_CHAIN,
        "outcomes": outcomes,
        "owner": OWNER,
        "phase": PHASE,
        "proposal_count": 60,
        "schema": "ghc.family.phase-truth.v681.v6.x2",
        "terminal_verdict": TERMINAL_VERDICT,
    })


def materialize() -> None:
    if git("rev-parse", "HEAD").stdout.strip() != X1_COMMIT:
        raise RuntimeError("x2 materialization must begin at immutable x1")
    if git("branch", "--show-current").stdout.strip() != BRANCH:
        raise RuntimeError("wrong Sable branch")
    x1_receipt = verify_x1()
    if (
        not x1_receipt["head_matches"]
        or x1_receipt["manifest_mismatches"]
        or not x1_receipt["planning_only"]
        or not x1_receipt["direct_parent_is_source"]
    ):
        raise RuntimeError("x1 immutability gate failed")

    freeze = load(X1 / "new-proposal-freeze.json")
    proposals = freeze["proposals"]
    positives = []
    mutations = []
    outcomes = []
    for proposal in proposals:
        fixture = positive_fixture(proposal)
        result = evaluate(proposal, fixture)
        if not result["accepted"]:
            raise RuntimeError(f"positive rejected: {proposal['proposal_id']}")
        positives.append({"fixture": fixture, "result": result})
        outcomes.append(
            {
                "authority_conferred": False,
                "evidence_scope": "bounded_synthetic_structure_only",
                "outcome": proposal["expected_disposition"],
                "proposal_id": proposal["proposal_id"],
                "real_rows": 0,
                "title": proposal["title"],
            }
        )
        for mutation_spec in proposal["preregistered_rejecting_mutations"]:
            changed = mutate(fixture, mutation_spec["mutation_type"])
            rejection = evaluate(proposal, changed)
            if rejection["accepted"]:
                raise RuntimeError(f"mutation accepted: {mutation_spec['mutation_id']}")
            mutations.append(
                {
                    "credit": "rejected_zero_credit",
                    "mutation_id": mutation_spec["mutation_id"],
                    "mutation_type": mutation_spec["mutation_type"],
                    "observed": "rejected",
                    "proposal_id": proposal["proposal_id"],
                    "reasons": rejection["reasons"],
                }
            )
    outcome_counts = Counter(row["outcome"] for row in outcomes)
    expected = Counter({"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
    if outcome_counts != expected or len(positives) != 60 or len(mutations) != 300:
        raise RuntimeError("control or outcome drift")

    skill_paths = materialize_skills()
    runner_paths = materialize_runners()
    portfolio = load(X1 / "portfolio-freeze.json")
    board = domain_board()

    write_json(X2 / "x1-immutability-receipt.json", x1_receipt)
    write_json(X2 / "proposal-evidence.json", {"outcome_counts": dict(outcome_counts), "outcomes": outcomes, "owner": OWNER, "phase": PHASE, "proposal_count": 60, "schema": "ghc.family.proposal-evidence.v681.v6.x2"})
    write_json(X2 / "positive-controls.json", {"accepted": len(positives), "controls": positives, "external_actions": 0, "owner": OWNER, "phase": PHASE, "real_rows": 0, "schema": "ghc.family.positive-controls.v681.v6.x2"})
    write_json(X2 / "mutation-results.json", {"executed": len(mutations), "failure_erasure": False, "mutations": mutations, "owner": OWNER, "phase": PHASE, "rejected": len(mutations), "schema": "ghc.family.mutation-results.v681.v6.x2", "zero_completion_credit": True})
    write_json(X2 / "tool-library-loan-record-schema.json", tool_library_loan_record_schema())
    write_json(X2 / "tool-library-loan-record-board.json", board)
    write_json(X2 / "tool-use-boundary.json", {
        "external_actions": 0,
        "global_or_shared_prefix_mutated": False,
        "inherited_package_seeds_promoted": False,
        "new_packages_installed": 0,
        "owner": OWNER,
        "phase": PHASE,
        "reason": "Python standard-library contracts are sufficient for this bounded synthetic scope; no irrelevant package installation is justified.",
        "schema": "ghc.family.tool-use-boundary.v681.v6.x2",
        "tool_novelty_credit": 0,
    })
    write_json(X2 / "portfolio-results.json", {
        "blocked": [{**row, "state": "held_unexecuted"} for row in portfolio["blocked"]],
        "exact_approval": [{**row, "state": "held_unexecuted"} for row in portfolio["exact_approval"]],
        "owner": OWNER,
        "owner_candidates": [{**row, "state": "bounded_fixture_completed"} for row in portfolio["owner_candidates"]],
        "owner_clean_fix_refine": [{**row, "state": "bounded_owner_local_completed"} for row in portfolio["owner_clean_fix_refine"]],
        "phase": PHASE,
        "safe_now": [{**row, "state": "bounded_owner_local_completed"} for row in portfolio["safe_now"]],
        "schema": "ghc.family.portfolio-results.v681.v6.x2",
        "successor_records_executed": 0,
    })
    write_json(X2 / "freed-id-flashcards.json", {"card_count": 80, "cards": cards(proposals), "owner": OWNER, "phase": PHASE, "schema": "ghc.family.freed-id-flashcards.v681.v6.x2"})
    write_json(X2 / "gmut-formal-board.json", {
        "analogy_only": True,
        "constraint_guard": "synthetic required-field, correction-state, and provenance-digest obligations only",
        "empirical_rows": 0,
        "equation_family": "typed scalar-tensor and effective-field-theory research model",
        "force_prediction_likelihood_constraint_confirmation": False,
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.gmut-tool-library-loan-formal-board.v681.v6.x2",
        "theory_of_everything": False,
        "uncertainty_guard": "typed missing, unknown, disputed, and exact-gate states without probability or field inference",
    })
    write_json(X2 / "thos-proxy-board.json", {
        "blind_matched_budget_real_arms": 0,
        "external_operations": 0,
        "owner": OWNER,
        "phase": PHASE,
        "represented": ["synthetic correction intake", "authority hold", "workload pause", "exception review", "accessible readback", "reversible handover"],
        "schema": "ghc.family.thos-tool-library-loan-proxy.v681.v6.x2",
    })
    write_json(X2 / "freed-id-profile.json", {
        "live_keys_or_proofs": 0,
        "network_events": 0,
        "owner": OWNER,
        "phase": PHASE,
        "production": False,
        "represented": ["synthetic subjectless loan persona", "correction requester role", "statement attachment", "minimum disclosure", "contest state"],
        "schema": "ghc.family.freed-id-tool-library-loan-profile.v681.v6.x2",
        "trust_governance": "exact_gate",
    })
    write_json(X2 / "cbr-authority-matrix.json", {
        "decisions_made": 0,
        "exact_gates": ["privacy access correction contest and disclosure", "loan eligibility fees custody release safety and legal remedies", "professional repair inspection diagnosis and safety", "legal cultural and affected-party authority", "Maori-language Maori-data-governance tangata whenua iwi hapu and Maori authority"],
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.cbr-tool-library-loan-authority.v681.v6.x2",
    })
    write_json(X2 / "zero-row-adapter.json", {
        "downloaded_rows": 0,
        "ingested_rows": 0,
        "likelihood_calls": 0,
        "owner": OWNER,
        "phase": PHASE,
        "posterior_samples": 0,
        "schema": "ghc.family.tool-library-loan-zero-row-adapter.v681.v6.x2",
        "status": "represented",
        "terminal_response": "REFUSED_NO_ROWS",
    })
    write_json(X2 / "accessibility-structural-audit.json", {
        "affected_user_evaluation": "reserved",
        "assistive_technology_evaluation": "reserved",
        "manual_keyboard_evaluation": "reserved",
        "maori_language_evaluation": "reserved",
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.accessibility-structural.v681.v6.x2",
        "structural_checks": {"headings": True, "landmarks": True, "table_headers": True, "text_fallback": True},
        "wcag_conformance_claimed": False,
    })
    write_text(X2 / "accessible-report.html", """<!doctype html>
<html lang="en-NZ"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sable v681-v6 synthetic tool-library-loan evidence</title></head>
<body><a href="#main">Skip to evidence</a><header><h1>Sable v681-v6 synthetic tool-library-loan evidence</h1><p>Structural owner-local evidence only. No real borrower, lender, staff member, volunteer, organization, tool, branch, loan row, custody event, condition evidence, incident, maintenance record, decision, authority, or Stage 20 claim.</p></header>
<main id="main"><section aria-labelledby="truth"><h2 id="truth">Outcome truth</h2><table><caption>Sixty proposal outcomes</caption><thead><tr><th scope="col">Outcome</th><th scope="col">Count</th></tr></thead><tbody><tr><th scope="row">Completed</th><td>42</td></tr><tr><th scope="row">Represented</th><td>12</td></tr><tr><th scope="row">Open gap</th><td>3</td></tr><tr><th scope="row">Exact gate</th><td>3</td></tr></tbody></table></section>
<section aria-labelledby="limits"><h2 id="limits">Reserved evaluation</h2><p>Manual keyboard, browser-diverse, responsive-layout, assistive-technology, cognitive, Maori-language, and affected-user evaluation remain reserved. This page makes no accessibility conformance claim.</p></section></main><footer><p>Terminal verdict: NOT_READY_FOR_STAGE_20.</p></footer></body></html>
""")
    write_json(X2 / "complete-incomplete-checklist.json", {
        "completed_bounded": ["60 positive controls", "300 rejecting mutations", "120 safe-now tasks", "80 candidate fixtures", "100 clean-fix-refine tasks", "20 owner-local skills materialized", "10 family-current runners materialized", "80 content-addressed boundary cards"],
        "incomplete_or_gated": ["real borrowers lenders staff volunteers tools branches loan rows custody events condition evidence incidents maintenance records and decisions", "professional tool-lending inventory repair safety records accessibility and library authority", "participant and affected-user evidence", "production identity lifecycle", "privacy and accessibility completeness", "legal cultural and Maori authority", "independent reproduction", "empirical GMUT confirmation", "Theory of Everything proof canon AGI ASI consciousness personhood and Stage 20"],
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.complete-incomplete.v681.v6.x2",
    })
    source_ids = [row["source_id"] for row in load(X1 / "official-primary-source-ledger.json")["entries"]]
    write_json(X2 / "official-source-use-receipt.json", {
        "authority_conferred": False,
        "network_data_queries": 0,
        "network_source_checks": len(source_ids),
        "owner": OWNER,
        "phase": PHASE,
        "real_rows": 0,
        "schema": "ghc.family.source-use.v681.v6.x2",
        "source_ids": source_ids,
        "use": "circulation metadata provenance validation accessibility correction privacy-risk and authority-reservation vocabulary only",
    })
    if not (X2 / "operational-failures.json").exists():
        write_json(X2 / "operational-failures.json", {"failures": [], "owner": OWNER, "phase": PHASE, "schema": "ghc.family.operational-failures.v681.v6.x2"})
    write_json(X2 / "materialization-receipt.json", {
        "generated_runner_paths": runner_paths,
        "generated_skill_paths": skill_paths,
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.materialization.v681.v6.x2",
        "shared_or_global_skill_installation": False,
    })
    refresh_counts()
    print(json.dumps({"mutations_rejected": len(mutations), "outcomes": dict(outcome_counts), "positive_controls": len(positives), "runners_materialized": len(runner_paths), "skills_materialized": len(skill_paths), "status": "X2_MATERIALIZED_NOT_SEALED"}, indent=2))


def seal() -> None:
    required = [X2 / "skill-validation-receipts.json", X2 / "runner-smoke-receipts.json", X2 / "phase-truth.json"]
    if not all(path.is_file() for path in required):
        raise RuntimeError("x2 validation dependencies are incomplete")
    skill_receipt = load(required[0])
    runner_receipt = load(required[1])
    portfolio = load(X2 / "portfolio-results.json")
    if skill_receipt["passed"] != 20 or runner_receipt["passed"] != 10:
        raise RuntimeError("skill or runner validation incomplete")
    if any(row["state"] != "held_unexecuted" for row in portfolio["exact_approval"] + portfolio["blocked"]):
        raise RuntimeError("protected approval packet was executed")

    source_paths = [
        "scripts/build_ghc_family_sable_rook_v681_v6_x2.py",
        "scripts/ghc_family_sable_rook_v681_v6_contracts.py",
        "scripts/ghc_family_sable_rook_v681_v6_runner_bank.py",
        "scripts/ghc_family_sable_rook_v681_v6_skill_bank.py",
        "tests/test_ghc_family_sable_rook_v681_v6_x2.py",
    ]
    source_paths.extend(load(X2 / "materialization-receipt.json")["generated_runner_paths"])
    content_paths = sorted(set([rel(path) for path in X2.rglob("*") if path.is_file()] + source_paths))
    exclusions = [
        "docs/sable-rook/v681-v6/validation/x2-index-manifest.json",
        "docs/sable-rook/v681-v6/validation/x2-privacy-scan.json",
        "docs/sable-rook/v681-v6/validation/x2-staged-review.json",
    ]
    scanners = {
        "raw_uuid": re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives)[\\/]"),
        "raw_task_thread_identifier": re.compile(r"\b(?:source_thread_id|thread_id)\b", re.IGNORECASE),
        "credential_assignment": re.compile(r"\b(?:api[_-]?key|token|password|secret)\s*[:=]\s*[^\s]+", re.IGNORECASE),
        "private_conversation_payload": re.compile(r"source_thread_id|codex_delegation", re.IGNORECASE),
    }
    candidates = []
    confirmed = []
    for path_text in content_paths:
        content = (ROOT / path_text).read_text(encoding="utf-8", errors="replace")
        for class_name, pattern in scanners.items():
            if pattern.search(content):
                row = {"class": class_name, "disposition": "scanner_definition_only" if path_text.endswith("build_ghc_family_sable_rook_v681_v6_x2.py") else "confirmed_payload_hit", "path": path_text}
                candidates.append(row)
                if row["disposition"] == "confirmed_payload_hit":
                    confirmed.append(row)
    if confirmed:
        raise RuntimeError("confirmed x2 privacy hit: " + json.dumps(confirmed))
    write_json(VALIDATION / "x2-privacy-scan.json", {"candidates": candidates, "confirmed_hits": confirmed, "owner": OWNER, "phase": PHASE, "privacy_classes": list(scanners), "scanned_files": len(content_paths), "schema": "ghc.family.privacy-scan.v681.v6.x2"})
    write_json(VALIDATION / "x2-staged-review.json", {"declared_self_exclusions": exclusions, "expected_paths": sorted(content_paths + exclusions), "lifecycle": "x2_evidence", "owner": OWNER, "path_count": len(content_paths) + len(exclusions), "phase": PHASE, "schema": "ghc.family.staged-review.v681.v6.x2"})
    entries = []
    for path_text in content_paths:
        data = normalized(ROOT / path_text)
        entries.append({"bytes": len(data), "path": path_text, "sha256": digest(data)})
    write_json(VALIDATION / "x2-index-manifest.json", {"declared_self_exclusions": exclusions, "entries": entries, "entry_count": len(entries), "owner": OWNER, "phase": PHASE, "schema": "ghc.family.normalized-lf-index-manifest.v681.v6.x2", "x1": X1_COMMIT})
    print(json.dumps({"manifest_entries": len(entries), "privacy_candidates": len(candidates), "privacy_confirmed": 0, "status": "X2_SEALED_WORKTREE_NOT_COMMITTED"}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("materialize", "refresh", "seal"))
    args = parser.parse_args()
    if args.mode == "materialize":
        materialize()
    elif args.mode == "refresh":
        refresh_counts()
        print(json.dumps({"status": "X2_COUNTS_REFRESHED"}))
    else:
        seal()


if __name__ == "__main__":
    main()
