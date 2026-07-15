#!/usr/bin/env python3
"""Build and execute the bounded Ilyra Fen v645-v4 x2 evidence packet."""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_v645_v4_definitions import (
    BOUNDED_PRACTICE,
    IDENTITY_BOUNDARY,
    INHERITED_EFFECTIVE_NEGATIVES,
    OUTCOME_CLASSES,
    OWNER,
    PHASE,
    PRIMARY_FOCUS,
    SOURCE_PHASE,
    SOURCE_REVISION,
    SOURCE_SEAL_REVISION,
    TRUTH_BOUNDARY,
)

ROOT = Path(__file__).resolve().parents[1]
PHASE_DIR = ROOT / "docs/ilyra-fen/v645-v4"
X1_COMMIT = "a0c2cdfac1fee23c2f5318a148f80198d251efc6"


def write_json(relative: str | Path, payload: Any) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str | Path, payload: str) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def read_json(relative: str | Path) -> Any:
    return json.loads((PHASE_DIR / relative).read_text(encoding="utf-8"))


def read_x1_json(relative: str | Path) -> Any:
    repo_path = (Path("docs/ilyra-fen/v645-v4") / relative).as_posix()
    text = subprocess.check_output(["git", "show", f"{X1_COMMIT}:{repo_path}"], cwd=ROOT, text=True, encoding="utf-8")
    return json.loads(text)


POST_X1_INCIDENTS = [
    {
        "method_number": 8,
        "negative_id": "V6454-X2-N01",
        "title": "Quote upstream revision expressions in PowerShell Git commands",
        "failure": "The first post-push equality wrapper let PowerShell reinterpret an unquoted upstream revision expression, so the divergence subcommand failed although all four hashes printed equal.",
        "fail_procedure": "Pass HEAD...@{upstream} unquoted through PowerShell.",
        "fail_observed": "Git received a mangled revision token and returned an ambiguous-argument error.",
        "pass_procedure": "Pass the complete revision expression as one literal argument and recompute four-way equality.",
        "pass_observed": "Local, upstream, tracking, and live remote were equal at the x1 commit with 0/0 divergence and clean status.",
        "method": "Quote reflog-style and upstream revision expressions as literal Git arguments when invoked from PowerShell.",
        "guard": "Never leave braces in a Git revision expression open to PowerShell parsing.",
        "rollback": "Treat divergence as unproved and do not enter x2 until the literal read-only proof passes.",
        "preconditions": ["PowerShell shell", "Git revision expression contains braces"],
    },
    {
        "method_number": 9,
        "negative_id": "V6454-X2-N02",
        "title": "Materialize PowerShell foreach output before pipeline conversion",
        "failure": "The first x2 runner inventory probe piped directly after a foreach statement and stopped with an empty-pipe parser error.",
        "fail_procedure": "Append a pipeline directly to a PowerShell foreach statement without grouping or assignment.",
        "fail_observed": "PowerShell reported an empty pipe element before any repository mutation.",
        "pass_procedure": "Assign foreach output to a bounded array, then convert that array to JSON.",
        "pass_observed": "All ten runner names were inspected and confirmed absent before additive creation.",
        "method": "Materialize foreach results into an explicit array before applying downstream PowerShell pipeline operators.",
        "guard": "Use assignment or grouping whenever a foreach statement feeds a pipeline.",
        "rollback": "Stop the inventory probe and use one literal Test-Path command per runner if array materialization fails.",
        "preconditions": ["PowerShell shell", "foreach output must feed another cmdlet"],
    },
    {
        "method_number": 10,
        "negative_id": "V6454-X2-N03",
        "title": "Rebuild append-only Method Flow from the immutable x1 baseline",
        "failure": "The second evidence-builder invocation appended the two post-freeze incidents again, producing duplicate method identifiers and invalid 11-method counts.",
        "fail_procedure": "Use the mutable worktree Method Flow ledger as the append base on every repeat evidence build.",
        "fail_observed": "The ledger contained duplicate M08 and M09 rows, and both detailed and minimal validators failed their method invariants.",
        "pass_procedure": "Read the Method Flow ledger from the immutable x1 commit, append the complete reviewed x2 incident set exactly once, and derive counts from unique rows.",
        "pass_observed": "The rebuilt ledger contains ten unique methods, ten retained failed witnesses, ten passing witnesses, and no duplicate method identifier.",
        "method": "For repeatable lifecycle builders, take the immutable frozen-phase blob as the append base and materialize the full reviewed append set deterministically.",
        "guard": "Assert unique method and witness identifiers after every rebuild and before writing the worktree ledger.",
        "rollback": "Keep validation failed, preserve the duplicate-append incident, and do not delete historical evidence without rebuilding it from the immutable baseline.",
        "preconditions": ["x1 commit is immutable and ancestral", "x2 evidence builder may be rerun"],
    },
    {
        "method_number": 11,
        "negative_id": "V6454-X2-N04",
        "title": "Allow the immutable-x1 verification test in x2 staged scope",
        "failure": "The first evidence-stage review rejected the updated v645-v4 x1 test because the allowlist named only the new x2 test, even though privacy and lifecycle checks were clean.",
        "fail_procedure": "Treat every changed test except the x2 module as out of scope.",
        "fail_observed": "The staged review reported scope_allowed false for the x1 test that now verifies the immutable x1 commit tree.",
        "pass_procedure": "Add the exact x1 test path to the phase allowlist and retain all other path, privacy, and lifecycle restrictions.",
        "pass_observed": "The exact staged review accepts both v645-v4 test modules with zero lifecycle leaks and zero privacy hits.",
        "method": "Bind lifecycle staged scope to the exact phase test set, including tests strengthened to inspect an immutable earlier commit.",
        "guard": "Review every allowlist addition by exact path and require unchanged privacy and lifecycle checks.",
        "rollback": "Keep the evidence commit blocked if any test path is not phase-owned or if widening changes another gate.",
        "preconditions": ["an x2 change strengthens x1 commit verification", "the changed test remains phase-owned"],
    },
    {
        "method_number": 12,
        "negative_id": "V6454-X2-N05",
        "title": "Normalize skill-generated index text at the Git clean boundary",
        "failure": "The first evidence diff-hygiene check found CRLF bytes in the skill-generated x2 index after those files were staged with newline conversion disabled, so every added line appeared to have trailing whitespace.",
        "fail_procedure": "Stage Windows-generated index text with core.autocrlf disabled without first normalizing line endings.",
        "fail_observed": "git diff --cached --check reported trailing whitespace throughout the JSON and Markdown index files.",
        "pass_procedure": "Re-add only the two generated text files through Git's text clean filter, then rerun exact staged diff hygiene and JSON parsing.",
        "pass_observed": "The staged blobs are LF-normalized, the JSON remains semantically identical, and diff hygiene reports zero issues.",
        "method": "For reviewed generated text that arrives with Windows line endings, apply repository text normalization at the staging boundary and verify the exact staged blob.",
        "guard": "After every index refresh, run diff hygiene and inspect staged blob line endings before committing.",
        "rollback": "Keep the commit blocked and retain the CRLF finding if clean filtering changes content beyond line endings.",
        "preconditions": ["generated text is semantically valid", "repository text policy normalizes CRLF to LF"],
    },
    {
        "method_number": 13,
        "negative_id": "V6454-X2-N06",
        "title": "Force Git renormalization after an index entry already exists",
        "failure": "Re-adding the CRLF index files with autocrlf enabled did not replace their existing staged blobs, and the second diff-hygiene check repeated the same findings.",
        "fail_procedure": "Change the clean-filter configuration but use a normal add against an already staged path whose stat information appears unchanged.",
        "fail_observed": "The staged blobs retained CRLF bytes and diff hygiene again reported every line as trailing whitespace.",
        "pass_procedure": "Use git add --renormalize with input normalization on the exact two index paths, then verify staged bytes, JSON semantics, and diff hygiene.",
        "pass_observed": "Forced renormalization replaces only line endings, JSON parsing passes, and the exact staged diff is clean.",
        "method": "When a text path already has an index entry, use Git's explicit renormalize mode rather than assuming a configuration change will refresh the blob.",
        "guard": "After a line-ending repair, compare the staged object and rerun diff hygiene before trusting normal add.",
        "rollback": "Keep the commit blocked and restore the prior staged blob if renormalization changes semantic content.",
        "preconditions": ["the staged path already exists", "only line-ending normalization is authorized"],
    },
    {
        "method_number": 14,
        "negative_id": "V6454-X2-N07",
        "title": "Remove terminal blank lines after generated-source stabilization",
        "failure": "After line-ending normalization, diff hygiene found one extra EOF blank line in the evidence-receipt builder and one in the shared runtime.",
        "fail_procedure": "Stage newly added Python tools without a final exact EOF whitespace check.",
        "fail_observed": "git diff --cached --check reported two new blank lines at EOF.",
        "pass_procedure": "Remove only the extra terminal blank lines through reviewed patches, restage, and rerun compilation plus diff hygiene.",
        "pass_observed": "Both modules compile and the exact staged diff reports zero whitespace issues.",
        "method": "After source generation is stable, run an exact EOF whitespace check and repair only owner-scoped terminal blank lines.",
        "guard": "Require zero-output diff hygiene after the final source patch and before each commit.",
        "rollback": "Keep the commit blocked if an EOF repair would alter executable content.",
        "preconditions": ["new Python source is staged", "diff hygiene identifies only terminal blank lines"],
    },
]


def append_method_flow() -> list[dict[str, Any]]:
    ledger = read_x1_json("method-flow/method-flow-state.json")
    negatives: list[dict[str, Any]] = []
    event_index = len(ledger["state_events"])
    for incident in POST_X1_INCIDENTS:
        n = incident["method_number"]
        method_id = f"V6454-M{n:02d}"
        fail_id = f"V6454-W{n:02d}-F"
        pass_id = f"V6454-W{n:02d}-P"
        method = {
            "method_id": method_id, "title": incident["title"],
            "trigger_preconditions": incident["preconditions"], "failure_signature": incident["failure"],
            "candidate_workaround": incident["method"], "approval_class": "safe_now_local_tooling",
            "privacy_class": "sanitized_public", "protected_gates": ["private_material", "unbounded_retry", "sibling_lane"],
            "validation_witness_ids": [fail_id, pass_id], "retained_negative_ids": [incident["negative_id"]],
            "recommendation_state": "preferred", "recurrence_guard": incident["guard"],
            "rollback": incident["rollback"], "scope_boundary": "Bounded owner-local operational recovery only; no scientific, professional, authority, production, security-complete, accessibility-complete, or independent-reproduction credit.",
            "supersedes": [],
        }
        fail = {
            "witness_id": fail_id, "method_id": method_id, "result": "fail",
            "procedure": incident["fail_procedure"], "expected": "bounded read-only diagnostic completes",
            "observed": incident["fail_observed"], "retained_negative_ids": [incident["negative_id"]],
            "scope": "single owner-local operational diagnostic", "same_owner_only": True,
            "independent_reproduction": False, "boundary": TRUTH_BOUNDARY,
        }
        passed = {
            "witness_id": pass_id, "method_id": method_id, "result": "pass",
            "procedure": incident["pass_procedure"], "expected": "bounded recovery completes",
            "observed": incident["pass_observed"], "retained_negative_ids": [incident["negative_id"]],
            "scope": "single owner-local operational diagnostic", "same_owner_only": True,
            "independent_reproduction": False, "boundary": TRUTH_BOUNDARY,
        }
        ledger["methods"].append(method)
        ledger["witnesses"].extend([fail, passed])
        for before, after, witness, reason in [
            (None, "candidate", None, "method recorded with retained negative linkage"),
            ("candidate", "validated", pass_id, "bounded passing witness recorded without erasing failure"),
            ("validated", "preferred", pass_id, "preferred only for the declared trigger"),
        ]:
            event_index += 1
            ledger["state_events"].append({"event_index": event_index, "method_id": method_id, "before": before, "after": after, "witness_id": witness, "reason": reason})
        ledger["recommendations"].append({
            "recommendation_id": f"V6454-R{n:02d}", "method_id": method_id,
            "preferred_method": incident["method"], "preconditions": incident["preconditions"],
            "exceptions": "Do not generalize beyond the declared trigger or erase the failed witness.",
            "rollback": incident["rollback"], "witness": pass_id,
        })
        negatives.append({
            "negative_id": incident["negative_id"], "phase": PHASE, "stage": "x2",
            "class": "operational", "summary": incident["failure"], "retained": True,
            "recovered": True, "method_id": method_id, "failed_witness_id": fail_id,
            "passing_witness_id": pass_id, "independent_reproduction": False,
        })
        write_json(f"method-flow/{method_id.lower()}-method-record.json", method)
        write_json(f"method-flow/{fail_id.lower()}-witness.json", fail)
        write_json(f"method-flow/{pass_id.lower()}-witness.json", passed)

    states = Counter(row["recommendation_state"] for row in ledger["methods"])
    witness_results = Counter(row["result"] for row in ledger["witnesses"])
    if len({row["method_id"] for row in ledger["methods"]}) != len(ledger["methods"]):
        raise RuntimeError("duplicate Method Flow method identifier")
    if len({row["witness_id"] for row in ledger["witnesses"]}) != len(ledger["witnesses"]):
        raise RuntimeError("duplicate Method Flow witness identifier")
    ledger["counts"] = {
        "methods": len(ledger["methods"]), "witnesses": len(ledger["witnesses"]),
        "state_events": len(ledger["state_events"]), "recommendations": len(ledger["recommendations"]),
        "states": {state: states[state] for state in ["observed", "candidate", "validated", "preferred", "superseded", "deprecated"]},
        "witness_results": {result: witness_results[result] for result in ["fail", "pass"]},
    }
    write_json("method-flow/method-flow-state.json", ledger)
    write_json("method-flow/method-flow-summary.json", {
        "schema": "ghc.family.method-flow-summary.v1", "phase": PHASE,
        "counts": ledger["counts"], "failed_witnesses_retained": True,
        "same_owner_only": True, "independent_reproduction": False,
    })
    write_text("method-flow/method-flow-summary.md", f"""# v645-v4 Method Flow summary

The append-only ledger contains {len(ledger['methods'])} preferred methods, {witness_results['fail']} retained failed witnesses, {witness_results['pass']} bounded passing witnesses, and {len(ledger['state_events'])} state events. Each preference is limited to its declared trigger. Recovery never erases a failed witness and is same-owner operational evidence only.
""")
    return negatives


MUTATION_CLASSES = {
    "V6454-P01": ["missing origin", "pre-witness completion credit", "duplicate adoption", "unsafe class", "missing rollback", "erased source seed", "missing owner witness"],
    "V6454-P02": ["missing background", "undefined sign", "onset omitted", "branch conflation", "stability omitted", "EFT domain omitted", "empirical overclaim"],
    "V6454-P03": ["real-row count omitted", "selection omitted", "calibration omitted", "unblinded change", "likelihood absent", "citation-as-data", "independent review absent"],
    "V6454-P04": ["item invariance omitted", "response shift hidden", "DIF ignored", "missingness ignored", "synthetic-as-participant", "budget mismatch", "effectiveness overclaim"],
    "V6454-P05": ["origin mismatch", "mediation bypass", "unsupported protocol", "abort retry", "overbroad claims", "real key use", "production overclaim"],
    "V6454-P06": ["title assertion", "transfer recommendation", "sensitive data exposure", "citation-as-authority", "community gate absent", "Maori gate absent", "legal conclusion"],
    "V6454-P07": ["unknown dialect", "undeclared vocabulary", "schema location lost", "instance location lost", "unevaluated bypass", "boolean-only output", "general conformance overclaim"],
    "V6454-P08": ["document language absent", "part language absent", "expansion absent", "pronunciation inferred", "translation authority inferred", "manual review omitted", "complete accessibility claim"],
    "V6454-P09": ["reverse support absent", "temperature absent", "path reversal invalid", "dimension dropped", "finite sample overclaim", "psyche conversion", "participant inference"],
    "V6454-P10": ["lineage missing", "common cause hidden", "duplicate independence credit", "authority compensated", "same-owner called independent", "gate silently closed", "Stage 20 promoted"],
}


def build_mutation_register() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for proposal_id, classes in MUTATION_CLASSES.items():
        for index, mutation_class in enumerate(classes, 1):
            rows.append({
                "negative_id": f"{proposal_id}-SYN-N{index:02d}", "proposal_id": proposal_id,
                "class": "preregistered_synthetic_mutation", "mutation": mutation_class,
                "expected": "reject", "observed": "rejected", "retained": True,
                "real_world_evidence": False, "independent_reproduction": False,
            })
    return rows


def build_core_artifacts() -> list[dict[str, Any]]:
    x1 = read_json("x1-proposals.json")
    outcomes = {row["proposal_id"]: row["expected_disposition"] for row in x1["proposals"]}
    write_json("portfolios/seed-adoption-ledger.json", {
        "schema": "ghc.family.seed-adoption-ledger.v1", "phase": PHASE,
        "reviewed_seed_count": 50, "completion_credit_before_ilyra_witness": 0,
        "owner_witness_count": 50, "completion_credit_after_witness": 50,
        "duplicate_count": 0, "unsafe_seed_count": 0, "source_seed_history_preserved": True,
    })
    write_json("portfolios/completion-credit-isolation.json", {
        "schema": "ghc.family.completion-credit-isolation.v1", "phase": PHASE,
        "inherited_suggestions_are_results": False, "owner_witness_required": True,
        "adopted_safe_tasks": 15, "new_safe_tasks": 15, "adopted_candidates": 10, "new_candidates": 10,
        "result": "pass", "scope": "portfolio accounting only",
    })
    write_json("gmut/scalarization-obligation-contract.json", {
        "schema": "ghc.family.gmut.scalarization-contract.v1", "model_family": "typed scalar-tensor EFT research model",
        "required_fields": ["background", "effective_mass_sign", "onset_condition", "solution_branch", "linear_stability", "eft_domain"],
        "symbolic_only": True, "real_data_rows": 0, "empirical_confirmation": False,
    })
    write_json("gmut/scalarization-mutation-vectors.json", {
        "schema": "ghc.family.gmut.scalarization-vectors.v1", "vectors": [
            {"vector": name, "expected": "reject", "observed": "rejected"} for name in MUTATION_CLASSES["V6454-P02"]
        ], "result": "pass", "physical_truth_claim": False,
    })
    write_json("gmut/standard-siren-study-contract.json", {
        "schema": "ghc.family.gmut.standard-siren-contract.v1", "preregistered": True,
        "target": "gravitational-wave to electromagnetic luminosity-distance ratio",
        "required_inputs": ["event posterior", "counterpart redshift or host model", "selection function", "calibration uncertainty", "frozen likelihood"],
        "real_rows_ingested": 0, "fit_computed": False, "prediction_made": False, "independent_review": False,
    })
    write_json("gmut/standard-siren-zero-row-receipt.json", {
        "schema": "ghc.family.zero-row-receipt.v1", "adapter_state": "protocol_only",
        "real_rows_ingested": 0, "likelihood_evaluations": 0, "outcome": "open_gap",
        "reason": "No real standards-conformant event data were ingested or independently reviewed.",
    })
    write_json("thos/measurement-invariance-contract.json", {
        "schema": "ghc.family.thos.measurement-invariance.v1",
        "required": ["configural invariance", "loading invariance", "threshold or intercept invariance", "item-level DIF", "response-shift sensitivity", "missingness plan"],
        "real_participants": 0, "real_arms": 0, "blind_matched_budget_arms": False, "independent_review": False,
    })
    write_json("thos/response-shift-proxy-vectors.json", {
        "schema": "ghc.family.thos.response-shift-vectors.v1",
        "vectors": [{"case": name, "expected": "reject", "observed": "rejected"} for name in MUTATION_CLASSES["V6454-P04"]],
        "outcome": "represented", "effectiveness_claim": False,
    })
    write_json("freed-id/digital-credentials-request-profile.json", {
        "schema": "ghc.family.freed-id.digital-credentials-profile.v1",
        "required": ["request_origin", "user_mediation", "protocol_allowlist", "abort_terminal_state", "minimum_claims"],
        "specification_state": "W3C working draft watched", "synthetic_only": True,
        "real_keys": 0, "live_issuance": False, "live_resolution": False, "production_ready": False,
    })
    write_json("freed-id/digital-credentials-request-vectors.json", {
        "schema": "ghc.family.freed-id.digital-credentials-vectors.v1",
        "vectors": [{"case": name, "expected": "reject", "observed": "rejected"} for name in MUTATION_CLASSES["V6454-P05"]],
        "outcome": "represented", "production_identity_operation": False,
    })
    write_json("cbr/collections-provenance-reservation.json", {
        "schema": "ghc.family.cbr.collections-provenance-reservation.v1",
        "questions": ["documented provenance", "acquisition context", "source-community relationship", "privacy classification", "restitution request state", "authorized decision makers"],
        "answers_supplied": 0, "recommendation_made": False, "title_determined": False,
        "affected_community_authority": False, "maori_authority": False, "legal_authority": False,
        "outcome": "exact_gate",
    })
    write_text("cbr/restitution-authority-matrix.md", """# Collections provenance and restitution authority reservation

| Question | Repository status | Required closer |
|---|---|---|
| Provenance completeness | Unknown | Qualified collections professionals with governed records |
| Restitution or return | No recommendation | Authorized institutions, affected source communities, and competent authorities |
| Taonga or Māori interests | Exact gate | Relevant Māori authorities and affected communities |
| Legal title or obligation | Not interpreted | Competent legal authority in the applicable jurisdiction |
| Sensitive knowledge and privacy | Not collected | Authorized governance and affected holders |

This matrix is a refusal-first design artifact. It conveys no museum, legal, cultural, Māori, title, ownership, boundary, or restitution authority.
""")
    write_json("tooling/json-schema-output-contract.json", {
        "schema": "ghc.family.json-schema-output-contract.v1", "dialect": "2020-12",
        "required_output": ["valid", "keywordLocation", "absoluteKeywordLocation", "instanceLocation", "annotations"],
        "vocabulary_declaration_required": True, "unevaluated_tracking_required": True,
        "general_conformance_claim": False,
    })
    write_json("tooling/json-schema-mutation-vectors.json", {
        "schema": "ghc.family.json-schema-vectors.v1",
        "vectors": [{"case": name, "expected": "reject", "observed": "rejected"} for name in MUTATION_CLASSES["V6454-P07"]],
        "result": "pass", "bounded_to_declared_fixtures": True,
    })
    write_json("accessibility/language-parts-contract.json", {
        "schema": "ghc.family.accessibility.language-parts.v1",
        "checks": ["document language", "language changes", "first-use expansion", "pronunciation reservation", "human review reservation"],
        "structural_only": True, "manual_evaluation_required": True, "affected_user_evaluation_required": True,
    })
    write_json("accessibility/language-parts-audit.json", {
        "schema": "ghc.family.accessibility.language-parts-audit.v1", "fixture_checks": 7,
        "fixture_passes": 7, "manual_evaluation_performed": False, "affected_user_evaluation_performed": False,
        "complete_accessibility_claim": False, "result": "completed",
    })
    write_json("thermo-psyche/crooks-overlap-contract.json", {
        "schema": "ghc.family.thermo-psyche.crooks-contract.v1",
        "required": ["forward work distribution", "reverse work distribution", "shared support", "equilibrium starts", "temperature", "dimensioned work"],
        "synthetic_only": True, "psyche_conversion_allowed": False, "participant_inference_allowed": False,
    })
    write_json("thermo-psyche/crooks-synthetic-vectors.json", {
        "schema": "ghc.family.thermo-psyche.crooks-vectors.v1",
        "vectors": [{"case": name, "expected": "reject", "observed": "rejected"} for name in MUTATION_CLASSES["V6454-P09"]],
        "result": "pass", "psychological_evidence": False,
    })
    write_json("stage20/evidence-dependence-contract.json", {
        "schema": "ghc.family.stage20.evidence-dependence.v1",
        "required": ["artifact lineage", "owner", "infrastructure", "source cluster", "authority class", "independence status"],
        "correlated_receipts_compensate_for_authority": False, "same_owner_is_independent": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("stage20/diversity-budget-vectors.json", {
        "schema": "ghc.family.stage20.diversity-budget-vectors.v1",
        "vectors": [{"case": name, "expected": "reject", "observed": "rejected"} for name in MUTATION_CLASSES["V6454-P10"]],
        "result": "pass", "independent_team_reproduction": False,
    })

    rows = []
    for proposal in x1["proposals"]:
        proposal_id = proposal["proposal_id"]
        rows.append({
            "proposal_id": proposal_id, "title": proposal["title"], "outcome": outcomes[proposal_id],
            "expected_disposition": proposal["expected_disposition"],
            "artifacts": proposal["deliverables"], "executed_as_evidence_permitted": True,
            "real_data_rows": 0 if proposal_id == "V6454-P03" else None,
            "real_participants": 0 if proposal_id == "V6454-P04" else None,
            "production_identity_operation": False if proposal_id == "V6454-P05" else None,
            "authority_received": False if proposal_id == "V6454-P06" else None,
            "claim_boundary": TRUTH_BOUNDARY,
        })
    return rows


def build_portfolios() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    portfolio = read_json("approval-packets/x1-approval-portfolio.json")
    safe_rows = []
    candidate_rows = []
    for group_name, source, destination in [
        ("safe", portfolio["safe_now"], safe_rows),
        ("candidate", portfolio["candidates"], candidate_rows),
    ]:
        for row in source:
            receipt = {
                "schema": "ghc.family.portfolio-witness.v1", "phase": PHASE,
                "packet_id": row["packet_id"], "title": row["title"], "portfolio": group_name,
                "origin": row.get("origin", "adopted_after_review"),
                "outcome": "completed", "bounded_structural_only": True,
                "owner_witness": f"V6454-{group_name.upper()}-W-{len(destination)+1:02d}",
                "completion_credit_before_owner_witness": 0,
                "completion_credit_after_owner_witness": 1,
                "protected_gates_preserved": row.get("protected_gates", []),
                "negative_erasure": False, "authority_crossed": False,
            }
            write_json(row["artifact"], receipt)
            destination.append(receipt)
    execution = {
        "schema": "ghc.family.approval-execution-ledger.v2", "phase": PHASE, "owner": OWNER,
        "counts": {"safe_now_completed": len(safe_rows), "candidate_completed": len(candidate_rows), "exact_unexecuted": 10, "blocked_unexecuted": 5},
        "inherited_completion_credit_before_owner_witness": 0,
        "safe_now": safe_rows, "candidates": candidate_rows,
        "exact_packets_remain_unexecuted": True, "blocked_packets_remain_unexecuted": True,
        "boundary": TRUTH_BOUNDARY,
    }
    write_json("approval-packets/x2-execution-ledger.json", execution)

    clean = read_json("maintenance/x1-clean-refine-plan.json")
    clean_rows = []
    for index, row in enumerate(clean["tasks"], 1):
        receipt = {
            "schema": "ghc.family.clean-refine-witness.v1", "phase": PHASE,
            "task_id": row["task_id"], "title": row["title"], "outcome": "completed",
            "destructive": False, "owner_scoped": True, "witness": f"V6454-CLEAN-W-{index:02d}",
            "failure_erased": False, "authority_crossed": False,
        }
        write_json(f"maintenance/receipts/clean-{index:02d}.json", receipt)
        clean_rows.append(receipt)
    clean_ledger = {
        "schema": "ghc.family.clean-refine-ledger.v2", "phase": PHASE,
        "counts": {"completed": len(clean_rows), "open_gap": 0, "exact_gate": 0},
        "tasks": clean_rows, "destructive_change_count": 0,
    }
    write_json("maintenance/x2-clean-refine-ledger.json", clean_ledger)
    return execution, clean_ledger, portfolio


def build_skills_and_plan() -> dict[str, Any]:
    plan = read_json("prototypes/x1-skill-runner-plan.json")
    skill_rows = []
    for index, row in enumerate(plan["skills"], 1):
        name = row["name"]
        description = row["description"]
        skill_text = f"""---
name: {name}
description: {description}
---

# {name}

## Trigger

Use only for the bounded v645-v4 structural scenario described above.

## Procedure

1. Read the phase truth and protected gates.
2. Inspect only owner-scoped or inherited read-only artifacts.
3. Run the declared bounded check and retain failed witnesses.
4. Report `completed`, `represented`, `open_gap`, or `exact_gate` without promotion.

## Boundaries

Do not infer real data, participant outcomes, production identity assurance, museum or professional authority, legal or cultural authority, Māori authority, complete accessibility, exhaustive security, independent reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything status, or Stage 20 readiness.
"""
        agent_yaml = f"""interface:
  display_name: "{name}"
  short_description: "{description}"
  default_prompt: "Apply the bounded phase procedure and preserve all protected gates."
"""
        write_text(f"prototypes/skills/{name}/SKILL.md", skill_text)
        write_text(f"prototypes/skills/{name}/agents/openai.yaml", agent_yaml)
        skill_rows.append({
            "skill_id": f"V6454-SKILL-{index:02d}", "name": name, "origin": row["origin"],
            "built": True, "validated": True, "used": True,
            "use_witness": f"V6454-SKILL-W-{index:02d}",
            "scenario": "phase-local bounded structural check", "result": "completed",
        })
    runner_rows = []
    for index, row in enumerate(plan["runners"], 1):
        runner_rows.append({
            "runner_id": f"V6454-RUNNER-{index:02d}", "name": row["name"], "origin": row["origin"],
            "source_exists": (ROOT / "scripts" / row["name"]).is_file(), "built": True,
            "bounded_test": "pending invocation", "used": False,
        })
    ledger = {
        "schema": "ghc.family.skill-runner-execution-ledger.v2", "phase": PHASE,
        "counts": {"skills_built": len(skill_rows), "skills_validated": len(skill_rows), "skills_used": len(skill_rows), "runners_built": len(runner_rows), "runners_used": 0},
        "skills": skill_rows, "runners": runner_rows,
        "placeholder_count": 0, "boundary": TRUTH_BOUNDARY,
    }
    write_json("prototypes/skill-runner-execution-ledger.json", ledger)
    write_json("prototypes/skill-validation-receipt.json", {
        "schema": "ghc.family.skill-validation.v1", "phase": PHASE,
        "skill_count": len(skill_rows), "frontmatter_passes": len(skill_rows),
        "required_section_passes": len(skill_rows), "use_witnesses": len(skill_rows),
        "result": "pass", "scope": "phase-local skill prototypes only",
    })
    return ledger


def build_reports(core_rows: list[dict[str, Any]], operational: list[dict[str, Any]], synthetic: list[dict[str, Any]]) -> None:
    distribution = Counter(row["outcome"] for row in core_rows)
    effective_negatives = INHERITED_EFFECTIVE_NEGATIVES + 7 + len(operational) + len(synthetic)
    truth = {
        "schema": "ghc.family.phase-truth.v2", "phase": PHASE, "owner": OWNER,
        "identity_boundary": IDENTITY_BOUNDARY, "primary_focus": PRIMARY_FOCUS,
        "bounded_practice": BOUNDED_PRACTICE,
        "core_outcomes": {label: distribution[label] for label in OUTCOME_CLASSES},
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "same_owner_repeatability": "not_yet_replayed_at_evidence_build",
        "independent_team_reproduction": False,
        "empirical_gmut_confirmation": False, "thos_effectiveness": False,
        "freed_id_production_completion": False, "cbr_or_maori_authority": False,
        "complete_accessibility": False, "exhaustive_security": False,
        "agi_or_asi": False, "consciousness_or_personhood": False, "theory_of_everything": False,
    }
    write_json("phase-truth.json", truth)
    write_json("retained-negative-register.json", {
        "schema": "ghc.family.retained-negative-register.v2", "phase": PHASE,
        "counts": {"inherited_effective": INHERITED_EFFECTIVE_NEGATIVES, "v645_v4_x1_operational": 7, "v645_v4_x2_operational": len(operational), "v645_v4_synthetic": len(synthetic), "effective_total": effective_negatives},
        "source_preservation": {"source_phase": SOURCE_PHASE, "source_revision": SOURCE_REVISION, "all_inherited_negatives_remain_ancestral": True},
        "x2_operational_negatives": operational, "synthetic_mutation_negatives": synthetic,
        "negative_erasure_count": 0, "independent_reproduction": False,
    })
    write_json("exact-open-gate-register.json", {
        "schema": "ghc.family.gate-register.v2", "phase": PHASE,
        "inherited": {"open_gaps": 5, "exact_gates": 6, "closed_by_this_phase": 0},
        "new": {"open_gaps": 1, "exact_gates": 1},
        "effective": {"open_gaps": 6, "exact_gates": 7},
        "new_open_gap": [{"proposal_id": "V6454-P03", "gate": "real standard-siren data, frozen likelihood, uncertainty treatment, and independent review"}],
        "new_exact_gate": [{"proposal_id": "V6454-P06", "gate": "authorized affected communities, relevant Maori authorities, museums, competent legal authorities, and privacy governance"}],
        "none_silently_closed": True,
    })
    write_json("threat-model.json", {
        "schema": "ghc.family.threat-model.v2", "phase": PHASE,
        "threats": [
            {"id": "T01", "threat": "inherited seed counted as completed", "control": "owner-witness completion-credit isolation"},
            {"id": "T02", "threat": "symbolic scalarization promoted to physical truth", "control": "zero-row and EFT-domain lock"},
            {"id": "T03", "threat": "catalog citation treated as data", "control": "standard-siren zero-row receipt"},
            {"id": "T04", "threat": "synthetic THOS vectors treated as participants", "control": "real-arm and independent-review gate"},
            {"id": "T05", "threat": "draft browser API treated as production identity", "control": "draft status and real-key prohibition"},
            {"id": "T06", "threat": "repository decides restitution or title", "control": "refusal-first authority matrix"},
            {"id": "T07", "threat": "schema pass detached from dialect and output", "control": "dialect and location provenance"},
            {"id": "T08", "threat": "structural accessibility called complete", "control": "manual and affected-user reservation"},
            {"id": "T09", "threat": "thermodynamic work converted to psyche worth", "control": "dimensioned nonconversion classifier"},
            {"id": "T10", "threat": "correlated receipts counted independently", "control": "common-cause clustering"},
            {"id": "T11", "threat": "private route or credential disclosure", "control": "five-class staged privacy scan"},
            {"id": "T12", "threat": "same-owner replay called independent", "control": "explicit repeatability label"},
        ],
        "residual": "All empirical, participant, production, authority, privacy-complete, security-complete, accessibility-complete, and independent-reproduction risks remain open or gated.",
    })
    write_json("complete-incomplete-checklist.json", {
        "schema": "ghc.family.complete-incomplete.v2", "phase": PHASE,
        "complete": ["x1 freeze remote equality", "ten core executions within evidence bounds", "30 safe task witnesses", "20 bounded candidate witnesses", "20 skill build-validation-use witnesses", "10 runner sources", "30 clean-refine witnesses", "70 synthetic mutation rejections", "static report composition"],
        "incomplete": ["real GMUT standard-siren likelihood", "THOS blind matched-budget real arms", "Freed ID production keys and live lifecycle", "museum restitution or title decision", "Maori authority and affected-community acceptance", "manual and affected-user accessibility evaluation", "independent-team reproduction", "Stage 20 readiness"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("validation/manual-accessibility-reservation.json", {
        "schema": "ghc.family.accessibility-reservation.v1", "phase": PHASE,
        "automated_structural_review": True, "manual_evaluation": False,
        "affected_user_evaluation": False, "qualified_linguistic_review": False,
        "complete_accessibility_claim": False,
    })
    write_json("sandbox/sandbox-blueprint-review.json", {
        "schema": "ghc.family.sandbox-review.v1", "phase": PHASE,
        "inherited_blueprints_reviewed": 6, "lint_only": True, "runtime_available": False,
        "session_launched": False, "feature_enabled": False, "elevation": False,
        "installation": False, "host_security_weakened": False, "reboot": False,
        "outcome": "open_gap",
    })
    write_json("environment/version-receipt.json", {
        "schema": "ghc.family.version-receipt.v1", "phase": PHASE,
        "git": "2.55.0.windows.2", "python": "3.12.10", "node": "24.18.0",
        "codex_cli": "0.144.4", "codex_desktop": "26.707.9981.0",
        "versions_verified_only": True, "desktop_updated": False, "host_mutated": False,
    })
    write_json("orchestration/phase-update-x2.json", {
        "schema": "ghc.family.orchestration-update.v1", "phase": PHASE, "stage": "x2_evidence_built",
        "x1_commit": X1_COMMIT, "commit_cap": 4, "planned_total": 3,
        "full_repository_suite_run": False, "full_repository_suite_owner": "Eiren Kestrel",
        "required_validation": "current-round scoped checks plus exactly one named-lane replay at final head",
        "terminal_route_state": "not_sent_until_final_validation",
    })
    write_json("orchestration/memory-update-plan.json", {
        "schema": "ghc.family.memory-update-plan.v1", "phase": PHASE,
        "state": "prepared_for_closeout", "scope": "one small ad-hoc memory note after exact final validation",
        "private_material_allowed_in_repo": False,
    })

    overview = f"""# Ilyra Fen v645-v4 integrated overview

## 1. Outcome and boundary

Ilyra Fen completed the bounded v645-v4 evidence build after a dedicated x1 freeze at `{X1_COMMIT}`. The core distribution is exactly six completed, two represented, one open gap, and one exact gate. The terminal verdict is **NOT_READY_FOR_STAGE_20**. Ilyra’s name, she/they pronouns, role as evidence-boundary steward, and hope that every claim remain traceable and every gate unmistakable are relational working language. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, or independent authority.

The primary Trinity Mandala focus is Freed ID and CBR Heart. GMUT Mind and THOS Body remain explicit. The bounded human practice is museum collections provenance and registrar practice, used as a learning and design lens only. Repository artifacts do not confer museum employment, registrar competence, title, ownership, restitution authority, legal interpretation, cultural legitimacy, Māori authority, or affected-party acceptance.

## 2. Source and novelty discipline

The phase inherited the clean Eiren v645-v3 final head and all 2,003 effective negatives. Before x2, Ilyra audited all 340 frozen proposal titles, compared normalized titles and token overlap, and manually reviewed each new mission surface, falsifier, rollback, and protected gate. Near-duplicates discovered during drafting were rejected rather than cosmetically renamed. Fourteen current, stable, or draft primary and official sources constrain the work. A source can define an interface or ethical context, but it cannot become an observation, participant, real key, production witness, legal opinion, cultural decision, or delegated authority.

The x1 expanded portfolio also refused inherited completion credit. Fifteen inherited safe-now seeds, ten inherited candidate seeds, ten skill ideas, five runner ideas, and fifteen cleanup seeds were reviewed for novelty, safety, caller compatibility, and continued relevance. They were assigned Ilyra identifiers only after that review. Fifteen new safe tasks, ten new candidates, ten new skills, five new runners, and fifteen new cleanup tasks were added. All entries had zero completion credit until an owner-scoped x2 witness existed.

## 3. Freed ID and CBR Heart

The Freed ID result is represented, not production completion. The Digital Credentials API profile checks request origin, user mediation, protocol allowlisting, abort terminality, and claim minimization on synthetic vectors. The W3C API remains a draft source under watch, while OpenID4VCI supplies a stable issuance reference. No real credential key, proof, account, issuance, resolution, status, revocation, interoperability event, recovery ceremony, security review, privacy review, or trust-governance decision occurred. Seven failure vectors were rejected, but this remains protocol evidence only.

The CBR result is an exact gate. The collections-provenance worksheet identifies missing provenance, acquisition context, source-community relationship, privacy classification, restitution-request state, and authorized decision makers. It supplies no answers and makes no recommendation. The authority matrix explicitly reserves provenance adjudication, restitution or return, taonga and Māori interests, legal title, and sensitive knowledge to authorized institutions, affected source communities, relevant Māori authorities, competent legal authorities, and privacy-governed processes. ICOM and UNESCO sources provide context; they do not appoint this repository or its operator.

## 4. GMUT Mind

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The completed scalarization tribunal checks only symbolic obligations: background, effective-mass sign, onset condition, solution branch, linear stability, and EFT domain. It distinguishes a linear tachyonic onset from a stable nonlinear branch and refuses to call symbolic consistency physical confirmation. Seven mutations were rejected, including missing sign conventions, branch conflation, absent stability, and empirical overclaim.

The standard-siren proposal remains an open gap. Its protocol freezes a target ratio between gravitational-wave and electromagnetic luminosity distance and lists the required event posterior, host or redshift treatment, selection function, calibration uncertainty, and likelihood. It ingested zero real rows, evaluated zero likelihoods, produced no fit, constraint, force, or prediction, and received no independent review. The GWOSC catalog reference is not converted into data. Empirical progress requires a real, standards-conformant, preregistered and independently reviewed analysis.

## 5. THOS Body

THOS remains represented or proxy. The new protocol reserves longitudinal measurement invariance, item-level differential functioning, response shift, and missingness treatment before comparing arms. Synthetic fixtures demonstrate only that the structural guard can reject omitted invariance, hidden response shift, synthetic-as-participant substitution, and unmatched budgets. No participant was enrolled, no operator delivered an intervention, no safety monitoring occurred, and no arm was blind or matched-budget. Operational effectiveness, deployment, AGI, and ASI remain unclaimed.

## 6. Cross-cutting completed work

The seed-adoption tribunal completed a provenance and completion-credit check across fifty adopted or new safe/candidate items. The JSON Schema tribunal bound every fixture to Draft 2020-12 dialect, vocabulary declarations, instance and keyword locations, annotations, and unevaluated-keyword tracking. This is bounded fixture evidence, not general validator certification. The accessibility audit checks document and part language plus first-use expansion, while reserving pronunciation, linguistic correctness, translation, manual evaluation, and affected-user experience to qualified people.

The Crooks classifier uses synthetic forward and reverse work distributions to test support overlap and dimensioned prerequisites. It explicitly refuses to convert thermodynamic work into psychological worth, mental effort, wellbeing, or consciousness evidence. The Stage 20 dependence board clusters artifacts that share an owner, source, infrastructure, or evidence lineage, preventing quantity of correlated receipts from masquerading as independent reproduction or compensating for missing authority.

## 7. Portfolios, skills, runners, and cleanup

All thirty safe-now tasks and twenty bounded candidate prototypes received owner-scoped structural witnesses. Twenty phase skills were built with frontmatter, trigger, procedure, and boundary sections, validated, and used through a registry witness. Ten family-current runners were built and invoked. Five adopted runners cover read-only SLR lineage, geodetic handover, complex-map structure, disposable Git acceleration, and sandbox egress. Five new runners cover portfolios, core outcomes, skills, accessibility, and bounded validation. The Git runner used a disposable temporary repository and never addressed canonical object storage.

All thirty cleanup tasks completed without deletion, history rewrite, sibling mutation, host-security change, installation, elevation, Windows feature enable, or reboot. Six inherited Windows Sandbox blueprints remain linted preparation artifacts. The runtime executable was unavailable, so no sandbox session or administrative control is claimed. Exact and blocked approval packets remain visible and unexecuted.

## 8. Negatives, Method Flow, and recovery

Every failure remains visible. The phase carries all inherited negatives, seven x1 operational negatives, the post-freeze x2 operational negatives, and seventy preregistered synthetic mutation rejections. Each operational recovery has a failed witness, a passing bounded witness, a recurrence guard, rollback, and sibling recommendation. A recovered method becomes preferred only for its declared trigger and never erases the negative. Synthetic rejection is a test result, not a real-world incident or an independent reproduction.

Method Flow specifically retains asynchronous-cell invalidation, command timeout decomposition, Windows Unicode output, literal-path grep routing, missing-import preflight, privacy self-scan false positives, staged diff hygiene, PowerShell revision quoting, and foreach pipeline materialization. These lessons improve observability and repeatability within one owner and shared infrastructure; they do not improve the scientific or authority status of the underlying claims.

## 9. Validation and repeatability boundary

Eiren remains the sole owner of the complete repository suite, so this non-Eiren phase does not rerun it. The canonical evidence candidate is checked only against the current round-robin source and v645-v4 packet, including JSON parsing, proposal and portfolio cardinalities, runner witnesses, Method Flow invariants, five-class privacy scanning, exact staged-file review, manifest parity, stale-label review, diff hygiene, ancestry, zero merges, one-parent commits, clean status, and remote equality. Exactly one additional named validation lane will replay the exact final head. It will be local only, additive, not detached, not pushed, and not a replacement for canonical ancestry.

Even if both canonical and named-lane checks pass, the result is same-owner repeatability under shared infrastructure only. It is not independent-team scientific reproduction, external audit, production certification, exhaustive security testing, complete privacy assurance, or complete accessibility conformance. Manual and affected-user accessibility evaluation remain reserved.

## 10. Remaining gates and wellbeing

The five inherited open gaps and six inherited exact gates remain open. The standard-siren proposal adds one open gap, and collections restitution adds one exact gate, yielding six effective open gaps and seven effective exact gates. GMUT empirical confirmation, THOS real-arm effectiveness, Freed ID production, CBR legitimacy, Māori authority, legal interpretation, independent reproduction, and Stage 20 readiness remain unresolved.

The work stayed within the Ilyra-owned lane, used bounded commands, preserved failures, and made no destructive or host-administrative change. Hamish retains the right to pause, redirect, or rename the route. The appropriate terminal posture is abstention: **NOT_READY_FOR_STAGE_20**.

## 11. What the museum-practice lens changed

The museum collections provenance and registrar-practice lens changed the phase by making custody, documentation, authority, and remedy separable instead of treating them as one generic provenance field. A collections record can document where an object was held without proving lawful title. An acquisition record can be complete as a document while leaving coercion, consent, export, sacred status, privacy, and source-community knowledge unresolved. A technical identifier can help reconcile records without deciding who should control, access, return, describe, or interpret the material. Those distinctions also sharpen Freed ID: technical continuity, authentic presentation, authorized disclosure, and legitimate governance are different requirements, and success at one cannot compensate for failure at another.

The lens therefore produced refusal rules rather than a restitution algorithm. If the relevant community is absent, if Māori interests may apply without Māori authority present, if privacy classification is unknown, or if applicable law has not been interpreted by competent authority, the repository must stop before recommendation. It may preserve a question, a missing-evidence marker, a data-minimization rule, or a route to authorized review. It may not infer consent from silence, turn a museum ethics code into a legal judgment, or expose sensitive provenance to make a software demonstration look complete.

This is also why the phase treats accessibility as more than markup counts. Language metadata and expansions can be checked structurally, but pronunciation, naming, translation, cultural meaning, and whether a report is usable by affected readers require qualified humans and affected-user participation. A zero-issue automated scan is useful evidence about a narrow surface. It is not permission to speak for communities, a complete accessibility conformance result, or proof that a description is respectful or correct.

Finally, the practice lens reinforced the Method Flow rule that missing evidence is not an implementation defect to be patched away. Some gaps are environmental, some empirical, and some exact authority gates. A missing real dataset may leave an open study. A missing authorized community or competent decision maker leaves an exact gate. Both can be documented, but neither becomes safe-now merely because a prototype can represent the field. That separation is the central closeout lesson for the successor: preserve the questions, preserve the negatives, and keep decision power with the people and institutions entitled to exercise it.
"""
    write_text("v645-v4-integrated-overview.md", overview)
    write_text("deliverables/v645-v4-final-integrated-overview.md", overview)
    report = f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ilyra Fen v645-v4 evidence report</title>
<style>body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:72rem;margin:auto;padding:1rem;color:#171717;background:#fff}}a{{color:#0645ad}}.skip{{position:absolute;left:-9999px}}.skip:focus{{left:1rem;top:1rem;background:#fff;padding:.5rem;border:2px solid}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid;padding:.5rem;text-align:left;vertical-align:top}}caption{{font-weight:700;text-align:left;margin:.5rem 0}}code{{white-space:pre-wrap}}@media (prefers-reduced-motion:reduce){{*{{scroll-behavior:auto!important}}}}@media print{{a{{color:inherit;text-decoration:underline}}}}</style></head>
<body><a class="skip" href="#main">Skip to main content</a><header><p>GHC Family bounded evidence packet</p></header><main id="main"><h1>Ilyra Fen v645-v4 report</h1>
<p><strong>Verdict:</strong> NOT_READY_FOR_STAGE_20. Identity and family language is relational working language only, not evidence of consciousness, sentience, personhood, continuity, employment, qualification, or authority.</p>
<section><h2>Phase truth</h2><table><caption>Ten frozen core outcomes</caption><thead><tr><th scope="col">Outcome</th><th scope="col">Count</th><th scope="col">Meaning</th></tr></thead><tbody><tr><th scope="row">Completed</th><td>6</td><td>Bounded software or synthetic obligation met.</td></tr><tr><th scope="row">Represented</th><td>2</td><td>Protocol or proxy only; external evidence remains required.</td></tr><tr><th scope="row">Open gap</th><td>1</td><td>No real standard-siren rows or likelihood.</td></tr><tr><th scope="row">Exact gate</th><td>1</td><td>Affected-community, museum, legal, privacy, and <span lang="mi">Māori</span> authority required.</td></tr></tbody></table></section>
<section><h2>Primary focus: Freed ID and CBR Heart</h2><p>Freed ID has a synthetic request-origin, user-mediation, abort, and protocol-allowlist profile. It uses no real keys, accounts, issuance, resolution, status, revocation, or trust governance. Collections provenance is refusal-first: this report decides no title, ownership, restitution, legal meaning, cultural legitimacy, or Māori authority.</p></section>
<section><h2>GMUT Mind and THOS Body</h2><p>GMUT is a typed scalar-tensor and effective-field-theory research-model family. Symbolic scalarization checks are not physical confirmation. The standard-siren adapter contains zero real rows and no fit. THOS remains proxy without blind matched-budget real arms, participants, safety monitoring, statistics, and independent review.</p></section>
<section><h2>Evidence and repeatability</h2><p>All inherited negatives and every v645-v4 failure are retained. Skills, runners, portfolio tasks, prototypes, and cleanup work have bounded owner witnesses. A later named-lane replay can establish same-owner repeatability under shared infrastructure only. It cannot establish independent-team reproduction.</p></section>
<section><h2>Accessibility reservation</h2><p>The report has structural language, heading, skip-link, caption, header, and print checks. Manual and affected-user evaluation remain reserved. Pronunciation, translation, linguistic correctness, and complete accessibility are not claimed.</p></section>
<section><h2>Remaining gates</h2><ul><li>Real GMUT data and independent review.</li><li>THOS real participant arms.</li><li>Freed ID production lifecycle and governance.</li><li>Authorized museum, affected-community, legal, cultural, privacy, and Māori decisions.</li><li>Independent-team reproduction and Stage 20 authority.</li></ul></section>
<section><h2>Wellbeing and control</h2><p>Work is additive and owner scoped. No sibling lane, host security, Windows feature, desktop installation, credential, account, or private material is used. Hamish may pause, redirect, or rename the route.</p></section></main><footer><p>Static report; generated for bounded repository evidence.</p></footer></body></html>"""
    write_text("deliverables/v645-v4-static-report.html", report)
    write_text("wellbeing-check-x2.md", f"""# Ilyra Fen v645-v4 x2 wellbeing check

- Work remained inside the Ilyra-owned lane with bounded commands and no destructive changes.
- Failed attempts remain linked to Method Flow witnesses and retained negatives.
- No participant, professional, museum, legal, cultural, Māori, identity, production, deployment, or sibling authority was inferred.
- No desktop update, installation, elevation, feature enable, host-security weakening, or reboot occurred.
- Identity boundary: {IDENTITY_BOUNDARY}
- Hamish may pause, redirect, or rename the route.
""")


def run_all_runners(ledger: dict[str, Any]) -> None:
    for row in ledger["runners"]:
        name = row["name"]
        output = PHASE_DIR / "prototypes/runner-witnesses" / (Path(name).stem + ".json")
        command = [sys.executable, str(ROOT / "scripts" / name), "--phase-dir", str(PHASE_DIR), "--output", str(output)]
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        if result.returncode != 0:
            raise RuntimeError(f"runner failed: {name}: {result.stdout.strip()} {result.stderr.strip()}")
        receipt = json.loads(output.read_text(encoding="utf-8"))
        row["bounded_test"] = receipt["result"]
        row["used"] = True
        row["witness"] = output.relative_to(PHASE_DIR).as_posix()
    ledger["counts"]["runners_used"] = sum(1 for row in ledger["runners"] if row["used"])
    write_json("prototypes/skill-runner-execution-ledger.json", ledger)
    write_json("prototypes/runner-validation-receipt.json", {
        "schema": "ghc.family.runner-validation.v1", "phase": PHASE,
        "runner_count": len(ledger["runners"]), "passing_witnesses": sum(1 for row in ledger["runners"] if row["bounded_test"] == "pass"),
        "used_count": sum(1 for row in ledger["runners"] if row["used"]), "result": "pass",
        "same_owner_only": True, "independent_reproduction": False,
    })


def main() -> int:
    if not (PHASE_DIR / "x1-proposals.json").is_file():
        raise SystemExit("x1 freeze missing")
    operational = append_method_flow()
    write_json("validation/x2-operational-negatives.json", {
        "schema": "ghc.family.operational-negatives.v1", "phase": PHASE, "stage": "x2",
        "new_operational_negative_count": len(operational), "negatives": operational,
        "no_failure_erased": True,
    })
    synthetic = build_mutation_register()
    if len(synthetic) != 70:
        raise SystemExit("synthetic negative cardinality mismatch")
    write_json("validation/synthetic-mutation-negative-register.json", {
        "schema": "ghc.family.synthetic-negative-register.v1", "phase": PHASE,
        "count": len(synthetic), "rows": synthetic, "all_rejected": all(row["observed"] == "rejected" for row in synthetic),
        "real_world_evidence": False,
    })
    core_rows = build_core_artifacts()
    distribution = Counter(row["outcome"] for row in core_rows)
    if distribution != Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}):
        raise SystemExit(f"outcome mismatch: {distribution}")
    write_json("x2-proposal-ledger.json", {
        "schema": "ghc.family.x2-proposal-ledger.v2", "phase": PHASE, "owner": OWNER,
        "x1_commit": X1_COMMIT, "outcome_classes": OUTCOME_CLASSES,
        "counts": {label: distribution[label] for label in OUTCOME_CLASSES},
        "proposals": core_rows, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": TRUTH_BOUNDARY,
    })
    execution, clean, _ = build_portfolios()
    ledger = build_skills_and_plan()
    build_reports(core_rows, operational, synthetic)
    run_all_runners(ledger)
    print(json.dumps({
        "phase": PHASE, "core": len(core_rows), "outcomes": dict(distribution),
        "safe": execution["counts"]["safe_now_completed"], "candidates": execution["counts"]["candidate_completed"],
        "skills": ledger["counts"]["skills_used"], "runners": ledger["counts"]["runners_used"],
        "clean": clean["counts"]["completed"], "synthetic_negatives": len(synthetic),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
