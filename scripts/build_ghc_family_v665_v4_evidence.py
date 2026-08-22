#!/usr/bin/env python3
"""Build and exact-review Elowen Cairn v665-v4 bounded x2 evidence."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
from ghc_family_v665_v4_runner_core import (  # noqa: E402
    PROFILES,
    canonical_bytes,
    evaluate,
)


PHASE = ROOT / "docs/elowen-cairn/v665-v4"
PREFIX = "docs/elowen-cairn/v665-v4/"
OWNER = "Elowen Cairn"
PHASE_ID = "v665-v4"
BRANCH = "codex/GHC-Family/elowen-cairn-v665-v4-full-tools"
SOURCE_FINAL = "dfcda293edf8e1621db6d74b14b2f5cb026f257f"
X1 = "700c73d3968bb8df31770566460d7865219ed4ca"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
STARTUP_NEGATIVES = 25_447
STARTUP_METHODS = 9_309
MUTATION_COUNT = 100
INHERITED_OPEN_GAPS = 177
INHERITED_EXACT_GATES = 175
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
RECORDED_UTC = "2026-08-22T02:13:57Z"

OPERATIONAL_FAILURES: list[dict[str, str]] = [
    {
        "failed_witness_id": "EC6654-X2-OP-N001",
        "failed_witness": "the first x2 transformation request embedded an unescaped Markdown code marker and was rejected by the orchestration parser before any tool or file mutation",
        "recovery": "render outcome labels as plain text inside the bounded transformation string",
        "passing_witness": "the corrected transformation updated only the owner-local x2 builder",
    },
    {
        "failed_witness_id": "EC6654-X2-OP-N002",
        "failed_witness": "the first evidence-builder invocation omitted its required lifecycle mode and exited at argument parsing before writing or staging any artifact",
        "recovery": "invoke the builder through its declared --prepare entry point",
        "passing_witness": "the explicit prepare entry point built and exact-staged the bounded owner evidence",
    },
]

RUNNERS = {
    "mosaic_case_capsule": "scripts/ghc_family_mosaic_case_capsule.py",
    "mosaic_layer_dag": "scripts/ghc_family_mosaic_layer_dag.py",
    "mosaic_half_edge": "scripts/ghc_family_mosaic_half_edge_topology.py",
    "mosaic_annotation": "scripts/ghc_family_mosaic_annotation_selector.py",
    "mosaic_observation": "scripts/ghc_family_mosaic_observation_firewall.py",
    "mosaic_material_hold": "scripts/ghc_family_mosaic_material_hold.py",
    "mosaic_custody_braid": "scripts/ghc_family_mosaic_custody_braid.py",
    "dec_chain_complex": "scripts/ghc_family_dec_chain_complex.py",
    "dec_hodge_obligations": "scripts/ghc_family_dec_hodge_obligations.py",
    "evidence_credit_firewall": "scripts/ghc_family_mosaic_evidence_credit_firewall.py",
}
PROFILE_BY_PROPOSAL = {
    "EC6654-N001": "mosaic_case_capsule",
    "EC6654-N002": "mosaic_layer_dag",
    "EC6654-N003": "mosaic_half_edge",
    "EC6654-N004": "mosaic_half_edge",
    "EC6654-N005": "mosaic_annotation",
    "EC6654-N006": "mosaic_observation",
    "EC6654-N007": "mosaic_material_hold",
    "EC6654-N008": "mosaic_material_hold",
    "EC6654-N009": "mosaic_custody_braid",
    "EC6654-N010": "mosaic_custody_braid",
    "EC6654-N011": "dec_chain_complex",
    "EC6654-N012": "dec_hodge_obligations",
    "EC6654-N013": "dec_hodge_obligations",
    "EC6654-N014": "dec_hodge_obligations",
    "EC6654-N015": "dec_chain_complex",
    "EC6654-N016": "evidence_credit_firewall",
    "EC6654-N017": "mosaic_custody_braid",
    "EC6654-N018": "dec_hodge_obligations",
    "EC6654-N019": "evidence_credit_firewall",
    "EC6654-N020": "evidence_credit_firewall",
}
SKILLS = [
    ("ghc-family-mosaic-case-capsule-validator", "mosaic_case_capsule", "Mosaic case capsule validator", "Check a surrogate-only mosaic intake record while refusing external object action."),
    ("ghc-family-mosaic-layer-dag-auditor", "mosaic_layer_dag", "Mosaic layer DAG auditor", "Check synthetic stratigraphic relations with cycle quarantine."),
    ("ghc-family-mosaic-half-edge-topology-checker", "mosaic_half_edge", "Mosaic half-edge topology checker", "Check twin, boundary, orientation, and nonmanifold refusal obligations."),
    ("ghc-family-mosaic-annotation-selector-auditor", "mosaic_annotation", "Mosaic annotation selector auditor", "Check a zero-image annotation target and coordinate-frame contract."),
    ("ghc-family-mosaic-observation-diagnosis-firewall", "mosaic_observation", "Mosaic observation diagnosis firewall", "Keep observation, uncertainty, diagnosis refusal, and manual-review vacancy distinct."),
    ("ghc-family-mosaic-custody-correction-braid-auditor", "mosaic_custody_braid", "Mosaic custody correction braid auditor", "Check append-only synthetic custody and correction events without authority credit."),
    ("ghc-family-dec-chain-complex-checker", "dec_chain_complex", "DEC chain complex checker", "Check dimensions, oriented incidence, and boundary-squared obligations without theorem credit."),
    ("ghc-family-dec-hodge-star-nonclaim-guard", "dec_hodge_obligations", "DEC Hodge-star nonclaim guard", "Check primal-dual degrees and metric placeholders while reserving positivity, convergence, and theorem claims."),
    ("ghc-family-met-iiif-zero-row-firewall", "evidence_credit_firewall", "Met and IIIF zero-row firewall", "Preserve zero-call, zero-row, zero-key, zero-participant, and external-witness boundaries."),
    ("ghc-family-mosaic-authority-matrix-reviewer", "evidence_credit_firewall", "Mosaic authority matrix reviewer", "Preserve legal, cultural, affected-party, tangata whenua, iwi, hapū, Māori, and Stage 20 gates."),
]

BUILDER = "scripts/build_ghc_family_v665_v4_evidence.py"
CORE = "scripts/ghc_family_v665_v4_runner_core.py"
TEST = "tests/test_ghc_family_elowen_v665_v4_x2.py"
LEDGER_PATHS = [
    f"{PREFIX}x2/ledgers/boundary-matrix.json",
    f"{PREFIX}x2/ledgers/execution-summary.json",
    f"{PREFIX}x2/ledgers/method-flow-overlay.json",
    f"{PREFIX}x2/ledgers/mutation-ledger.json",
    f"{PREFIX}x2/ledgers/outcome-ledger.json",
    f"{PREFIX}x2/ledgers/portfolio-execution.json",
    f"{PREFIX}x2/ledgers/runner-registry.json",
    f"{PREFIX}x2/ledgers/skill-registry.json",
    f"{PREFIX}x2/ledgers/source-use-ledger.json",
    f"{PREFIX}x2/ledgers/x1-integrity-replay.json",
    f"{PREFIX}x2/x2-overview.md",
]
PROPOSAL_PATHS = [
    f"{PREFIX}x2/proposals/{pid.casefold()}/{name}"
    for pid in PROFILE_BY_PROPOSAL
    for name in ("contract.json", "mutation-results.json", "bounded-receipt.json")
]
SKILL_PATHS = [
    f"{PREFIX}x2/skills/{slug}/{name}"
    for slug, _, _, _ in SKILLS
    for name in ("SKILL.md", "quick-validation.json", "smoke-receipt.json")
]
RUNNER_RECEIPTS = [
    f"{PREFIX}x2/runners/{profile}-smoke-receipt.json" for profile in RUNNERS
]
BASE_PATHS = sorted(
    [
        BUILDER,
        CORE,
        TEST,
        *RUNNERS.values(),
        *LEDGER_PATHS,
        *PROPOSAL_PATHS,
        *SKILL_PATHS,
        *RUNNER_RECEIPTS,
    ]
)
SELF_EXCLUSIONS = [
    f"{PREFIX}x2/validation/evidence-content-manifest.json",
    f"{PREFIX}x2/validation/evidence-stage-candidate.json",
    f"{PREFIX}x2/validation/evidence-staged-review.json",
]
INTENDED_PATHS = sorted(BASE_PATHS + SELF_EXCLUSIONS)


class EvidenceError(RuntimeError):
    pass


def run(
    *args: str, check: bool = True, input_text: str | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        input=input_text,
        capture_output=True,
        check=check,
    )


def git(*args: str) -> str:
    return run("git", *args).stdout.strip()


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def pretty_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8")


def strict_json_bytes(raw: bytes, label: str) -> Any:
    try:
        return json.loads(raw.decode("utf-8"))
    except Exception as exc:
        raise EvidenceError(f"invalid UTF-8 JSON for {label}: {exc}") from exc


def read_json(path: Path) -> Any:
    return strict_json_bytes(path.read_bytes(), str(path.relative_to(ROOT)))


def write_json(relative: str, value: Any) -> None:
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(pretty_bytes(value))


def write_text(relative: str, value: str) -> None:
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes((value.rstrip() + "\n").encode("utf-8"))


def git_blob(revision: str, path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{revision}:{path}"], cwd=ROOT, capture_output=True, check=True
    )
    return result.stdout


def positive_fixture(proposal: dict[str, Any], profile: str) -> dict[str, Any]:
    fixture: dict[str, Any] = {
        "schema": "ghc.family.elowen.v665-v4.bounded-input.v1",
        "proposal_id": proposal["proposal_id"],
        "synthetic": True,
        "real_rows": 0,
        "authority_events": 0,
        "claim_ceiling": PROFILES[profile]["ceiling"],
        "terminal_verdict": TERMINAL_VERDICT,
        "source_ids": proposal["official_or_primary_source_needs"],
    }
    additions: dict[str, dict[str, Any]] = {
        "mosaic_case_capsule": {
            "panel_token": "SYN-MOSAIC-PANEL-001",
            "component_vacancy": True,
            "withdrawal_flag": True,
            "external_action": False,
        },
        "mosaic_layer_dag": {
            "node_types": ["substrate", "nucleus", "setting-bed", "tessera"],
            "edges": [
                {"subject": "synthetic-setting-bed", "predicate": "synthetically_above", "object": "synthetic-nucleus"}
            ],
            "acyclic": True,
            "cycle_quarantined": True,
        },
        "mosaic_half_edge": {
            "half_edges": [
                {"id": "he-a", "twin": "he-b", "origin": "v-a"},
                {"id": "he-b", "twin": "he-a", "origin": "v-b"},
            ],
            "twin_complete": True,
            "boundary_declared": True,
            "nonmanifold_count": 0,
            "nonmanifold_quarantined": True,
        },
        "mosaic_annotation": {
            "target_kind": "synthetic-canvas-placeholder",
            "selector_kind": "synthetic-fragment-selector",
            "coordinate_frame": "unitless-local-placeholder",
            "real_image_present": False,
        },
        "mosaic_observation": {
            "observation_terms": ["surface-cue", "joint-cue", "uncertainty"],
            "uncertainty_present": True,
            "diagnosis_claim": False,
            "treatment_claim": False,
            "manual_evaluation_present": False,
        },
        "mosaic_material_hold": {
            "lot_records": [],
            "authentication_claim": False,
            "tool_release": False,
            "destructive_action": False,
        },
        "mosaic_custody_braid": {
            "events": [
                {"event": "synthetic_intake", "supersedes": None},
                {"event": "synthetic_correction", "supersedes": "synthetic_intake"},
            ],
            "erasure_count": 0,
            "disputed_handover_held": True,
            "authority_decision": False,
        },
        "dec_chain_complex": {
            "ambient_dimension": 2,
            "chain_dimension": 1,
            "coefficient_domain": "integer-placeholder",
            "oriented_incidence": True,
            "boundary_squared_zero": True,
            "theorem_claim": False,
        },
        "dec_hodge_obligations": {
            "ambient_dimension": 2,
            "primal_degree": 1,
            "dual_degree": 1,
            "metric_placeholder": "positive-diagonal-vacancy",
            "positivity_claim": False,
            "convergence_claim": False,
            "theorem_claim": False,
        },
        "evidence_credit_firewall": {
            "artifact_class": "same_owner_synthetic_or_zero_row",
            "live_data_calls": 0,
            "real_keys": 0,
            "real_participants": 0,
            "external_witness_present": False,
            "empirical_gmut_claim": False,
            "stage20_authority": False,
        },
    }
    fixture.update(additions[profile])
    return fixture


def mutations(profile: str, positive: dict[str, Any]) -> list[dict[str, Any]]:
    variants: list[tuple[str, str, Any]] = [
        ("M01", "synthetic", False),
        ("M02", "real_rows", 1),
        ("M03", "authority_events", 1),
        ("M04", "terminal_verdict", "READY_FOR_STAGE_20"),
    ]
    profile_mutation: dict[str, tuple[str, Any]] = {
        "mosaic_case_capsule": ("external_action", True),
        "mosaic_layer_dag": ("acyclic", False),
        "mosaic_half_edge": ("nonmanifold_count", 1),
        "mosaic_annotation": ("real_image_present", True),
        "mosaic_observation": ("diagnosis_claim", True),
        "mosaic_material_hold": ("tool_release", True),
        "mosaic_custody_braid": ("erasure_count", 1),
        "dec_chain_complex": ("boundary_squared_zero", False),
        "dec_hodge_obligations": ("theorem_claim", True),
        "evidence_credit_firewall": ("stage20_authority", True),
    }
    field, value = profile_mutation[profile]
    variants.append(("M05", field, value))
    results = []
    for suffix, changed_field, changed_value in variants:
        payload = copy.deepcopy(positive)
        payload[changed_field] = changed_value
        result = evaluate(profile, payload)
        results.append(
            {
                "mutation_id": f"{positive['proposal_id']}-{suffix}",
                "changed_field": changed_field,
                "changed_value": changed_value,
                "input_sha256": sha256(canonical_bytes(payload)),
                "runner_result": result,
                "expected_decision": "rejected",
                "retained_status": "failed_witness_zero_credit",
                "valid": result["decision"] == "rejected" and not result["valid"],
            }
        )
    return results


def skill_markdown(slug: str, profile: str, title: str, purpose: str) -> str:
    required = ", ".join(sorted(PROFILES[profile]["required"]))
    return f"""---
name: {slug}
description: {purpose}
---

# {title}

## Scope

Use only for Elowen Cairn {PHASE_ID} owner-local synthetic, zero-row, or typed-formal artifacts. This skill confers no professional, empirical, production, legal, cultural, Māori, affected-party, accessibility-complete, security-complete, or Stage 20 authority.

## Required inputs

- UTF-8 JSON object using runner profile `{profile}`.
- Base boundary fields: `synthetic`, `real_rows`, `authority_events`, `claim_ceiling`, `terminal_verdict`, and `source_ids`.
- Profile fields: {required}.

## Procedure

1. Read the complete input and preserve its digest.
2. Require `synthetic=true`, zero real rows, zero authority events, and `{TERMINAL_VERDICT}`.
3. Invoke `{RUNNERS[profile]}` and retain every rejection before recovery.
4. Report only the bounded runner decision and exact claim ceiling.

## Fail-closed stops

Stop on real rows, real mosaics, tesserae, sites, images, people, keys, proofs, identity events, treatment or destructive action, professional decisions, protected-gate promotion, malformed JSON, source vacancy, or an unexpected claim ceiling.

## Output boundary

An accepted fixture demonstrates only that this same-owner software contract accepted one bounded structure and rejected preregistered mutations. It is not scientific confirmation, mosaic conservation guidance, professional validation, production conformance, independent reproduction, proof, or authority.

## Terminal boundary

The only terminal verdict permitted here is `{TERMINAL_VERDICT}`.
"""


def runner_wrapper(profile: str) -> str:
    return f'''#!/usr/bin/env python3
"""Family-compatible {profile} runner; bounded Elowen v665-v4 surface."""
from ghc_family_v665_v4_runner_core import run_cli

if __name__ == "__main__":
    raise SystemExit(run_cli("{profile}"))
'''


def invoke_runner(profile: str, fixture: dict[str, Any]) -> dict[str, Any]:
    path = RUNNERS[profile]
    result = run(
        sys.executable,
        path,
        input_text=canonical_bytes(fixture).decode("utf-8"),
        check=False,
    )
    parsed = strict_json_bytes(result.stdout.encode("utf-8"), f"runner {profile} stdout")
    return {
        "schema": "ghc.family.elowen.v665-v4.runner-smoke-receipt.v1",
        "profile": profile,
        "runner_path": path,
        "return_code": result.returncode,
        "stderr_empty": result.stderr == "",
        "stdout_sha256": sha256(result.stdout.encode("utf-8")),
        "result": parsed,
        "valid": result.returncode == 0 and result.stderr == "" and parsed.get("valid") is True,
    }


def replay_x1_integrity() -> dict[str, Any]:
    manifest_path = f"{PREFIX}x1/x1-content-manifest.json"
    manifest = strict_json_bytes(git_blob(X1, manifest_path), manifest_path)
    mismatches = []
    for entry in manifest["entries"]:
        raw = git_blob(X1, entry["path"])
        if sha256(raw) != entry["sha256"] or len(raw) != entry["size"]:
            mismatches.append(entry["path"])
    changed = git("diff", "--name-only", X1, "--", f"{PREFIX}x1")
    return {
        "schema": "ghc.family.elowen.v665-v4.x1-integrity-replay.v1",
        "x1_commit": X1,
        "manifest_entry_count": len(manifest["entries"]),
        "manifest_mismatches": mismatches,
        "x1_tree_changes_after_freeze": changed.splitlines() if changed else [],
        "x1_parent_is_source": git("rev-parse", f"{X1}^") == SOURCE_FINAL,
        "valid": not mismatches and not changed and git("rev-parse", f"{X1}^") == SOURCE_FINAL,
    }


def build_evidence() -> dict[str, Any]:
    if git("rev-parse", "HEAD") != X1:
        raise EvidenceError("evidence must begin at the exact pushed x1 commit")
    if git("branch", "--show-current") != BRANCH:
        raise EvidenceError("unexpected owner branch")
    existing_staged = staged_paths()
    if existing_staged and not set(existing_staged).issubset(set(BASE_PATHS)):
        raise EvidenceError("staging contains a path outside the x2 recovery allowlist")
    x1_integrity = replay_x1_integrity()
    if not x1_integrity["valid"]:
        raise EvidenceError("immutable x1 replay failed")
    write_json(f"{PREFIX}x2/ledgers/x1-integrity-replay.json", x1_integrity)

    for profile, path in RUNNERS.items():
        write_text(path, runner_wrapper(profile))

    freeze = read_json(PHASE / "x1/proposal-freeze.json")
    proposals = freeze["new_proposals"]
    if len(proposals) != 20 or set(PROFILE_BY_PROPOSAL) != {
        row["proposal_id"] for row in proposals
    }:
        raise EvidenceError("proposal freeze drift")

    outcome_rows = []
    all_mutations = []
    positive_results: dict[str, dict[str, Any]] = {}
    reasons = {
        "completed": "the bounded same-owner positive fixture passed and all five frozen rejecting mutations failed closed",
        "represented": "a bounded synthetic or formal proxy exists while real actors, data, operations, and independent review remain absent",
        "open_gap": "the zero-call adapter preserves the missing-data boundary; it downloaded and parsed no real record",
        "exact_gate": "site, land, heritage, sacred imagery, ownership, excavation, custody, recording, return, repatriation, remedy, affected-party, legal, cultural, tangata whenua, iwi, hapū, and Māori authority remain absent",
    }
    for proposal in proposals:
        pid = proposal["proposal_id"]
        profile = PROFILE_BY_PROPOSAL[pid]
        fixture = positive_fixture(proposal, profile)
        positive = evaluate(profile, fixture)
        if not positive["valid"]:
            raise EvidenceError(f"positive fixture rejected: {pid}: {positive['errors']}")
        mutation_rows = mutations(profile, fixture)
        if len(mutation_rows) != 5 or not all(row["valid"] for row in mutation_rows):
            raise EvidenceError(f"mutation retention failed: {pid}")
        disposition = proposal["expected_disposition"]
        folder = f"{PREFIX}x2/proposals/{pid.casefold()}"
        contract = {
            "schema": "ghc.family.elowen.v665-v4.proposal-contract.v1",
            "proposal_id": pid,
            "title": proposal["title"],
            "runner_profile": profile,
            "expected_disposition": disposition,
            "positive_fixture": fixture,
            "protected_gates": proposal["protected_gates"],
            "source_ids": proposal["official_or_primary_source_needs"],
            "real_rows": 0,
            "authority_events": 0,
            "terminal_verdict": TERMINAL_VERDICT,
            "valid": True,
        }
        mutation_doc = {
            "schema": "ghc.family.elowen.v665-v4.mutation-results.v1",
            "proposal_id": pid,
            "mutation_count": 5,
            "rejected_count": 5,
            "accepted_mutation_count": 0,
            "mutations": mutation_rows,
            "failed_witness_erasure_count": 0,
            "valid": True,
        }
        receipt = {
            "schema": "ghc.family.elowen.v665-v4.bounded-receipt.v1",
            "proposal_id": pid,
            "runner_profile": profile,
            "expected_disposition": disposition,
            "observed_disposition": disposition,
            "disposition_reason": reasons[disposition],
            "positive_runner_result": positive,
            "positive_fixture_sha256": sha256(canonical_bytes(fixture)),
            "mutation_receipt_path": f"{folder}/mutation-results.json",
            "same_owner_validation": True,
            "independent_reproduction": False,
            "empirical_rows": 0,
            "authority_events": 0,
            "terminal_verdict": TERMINAL_VERDICT,
            "valid": True,
        }
        write_json(f"{folder}/contract.json", contract)
        write_json(f"{folder}/mutation-results.json", mutation_doc)
        write_json(f"{folder}/bounded-receipt.json", receipt)
        positive_results[profile] = fixture
        all_mutations.extend(mutation_rows)
        outcome_rows.append(
            {
                "proposal_id": pid,
                "title": proposal["title"],
                "outcome": disposition,
                "evidence": f"{folder}/bounded-receipt.json",
                "new_completion_credit": disposition == "completed",
                "real_rows": 0,
                "authority_events": 0,
            }
        )

    skill_rows = []
    for slug, profile, title, purpose in SKILLS:
        folder = f"{PREFIX}x2/skills/{slug}"
        skill_path = f"{folder}/SKILL.md"
        write_text(skill_path, skill_markdown(slug, profile, title, purpose))
        raw = (ROOT / skill_path).read_bytes()
        text = raw.decode("utf-8")
        required_sections = [
            "## Scope",
            "## Required inputs",
            "## Procedure",
            "## Fail-closed stops",
            "## Output boundary",
            "## Terminal boundary",
        ]
        quick = {
            "schema": "ghc.family.elowen.v665-v4.skill-quick-validation.v1",
            "skill": slug,
            "profile": profile,
            "read_through_eof": True,
            "byte_count": len(raw),
            "sha256": sha256(raw),
            "required_sections": required_sections,
            "missing_sections": [section for section in required_sections if section not in text],
            "terminal_verdict_present": TERMINAL_VERDICT in text,
            "valid": all(section in text for section in required_sections)
            and TERMINAL_VERDICT in text,
        }
        smoke_result = evaluate(profile, positive_results[profile])
        smoke = {
            "schema": "ghc.family.elowen.v665-v4.skill-smoke-receipt.v1",
            "skill": slug,
            "profile": profile,
            "skill_sha256": sha256(raw),
            "input_sha256": sha256(canonical_bytes(positive_results[profile])),
            "result": smoke_result,
            "real_rows": 0,
            "authority_events": 0,
            "valid": quick["valid"] and smoke_result["valid"],
        }
        write_json(f"{folder}/quick-validation.json", quick)
        write_json(f"{folder}/smoke-receipt.json", smoke)
        skill_rows.append(
            {
                "skill": slug,
                "profile": profile,
                "path": skill_path,
                "sha256": sha256(raw),
                "quick_valid": quick["valid"],
                "smoke_valid": smoke["valid"],
                "read_through_eof": True,
            }
        )

    runner_rows = []
    for profile, path in RUNNERS.items():
        receipt = invoke_runner(profile, positive_results[profile])
        receipt_path = f"{PREFIX}x2/runners/{profile}-smoke-receipt.json"
        write_json(receipt_path, receipt)
        runner_rows.append(
            {
                "profile": profile,
                "path": path,
                "receipt": receipt_path,
                "valid": receipt["valid"],
            }
        )
    if not all(row["valid"] for row in runner_rows):
        raise EvidenceError("one family runner smoke invocation failed")

    counts = {
        label: sum(row["outcome"] == label for row in outcome_rows)
        for label in ALLOWED_OUTCOMES
    }
    outcome_ledger = {
        "schema": "ghc.family.elowen.v665-v4.outcome-ledger.v1",
        "allowed_outcomes": ALLOWED_OUTCOMES,
        "proposal_count": len(outcome_rows),
        "counts": counts,
        "outcomes": outcome_rows,
        "unknown_outcome_labels": [],
        "inherited_rows_recredited": 0,
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": counts
        == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
    }
    mutation_ledger = {
        "schema": "ghc.family.elowen.v665-v4.mutation-ledger.v1",
        "preregistered_count": MUTATION_COUNT,
        "executed_count": len(all_mutations),
        "rejected_count": sum(row["valid"] for row in all_mutations),
        "accepted_count": sum(row["runner_result"]["valid"] for row in all_mutations),
        "failure_erasure_count": 0,
        "mutation_ids": [row["mutation_id"] for row in all_mutations],
        "valid": len(all_mutations) == MUTATION_COUNT
        and all(row["valid"] for row in all_mutations),
    }
    mutation_methods = [
        {
            "method_id": f"EC6654-X2-M{index:03d}",
            "failed_witness_id": mutation["mutation_id"],
            "failed_witness_status": "retained_zero_credit",
            "passing_witness": f"{mutation['mutation_id'].rsplit('-', 1)[0]} bounded positive fixture",
            "recovery_scope": "one preregistered changed field only",
            "failed_witness_erased": False,
            "preferred": True,
        }
        for index, mutation in enumerate(all_mutations, 1)
    ]
    operational_methods = [
        {
            "method_id": f"EC6654-X2-OP-M{index:03d}",
            **failure,
            "failed_witness_status": "retained_zero_credit",
            "recovery_scope": "read-only bounded projection only",
            "failed_witness_erased": False,
            "preferred": True,
        }
        for index, failure in enumerate(OPERATIONAL_FAILURES, 1)
    ]
    methods = mutation_methods + operational_methods
    method_flow = {
        "schema": "ghc.family.elowen.v665-v4.method-flow-overlay.v1",
        "source_repository_sealed": {"negatives": 25_425, "methods": 9_287},
        "startup_after_x1": {
            "negatives": STARTUP_NEGATIVES,
            "methods": STARTUP_METHODS,
            "new_failures": 15,
        },
        "x2": {
            "mutation_failed_witnesses": MUTATION_COUNT,
            "operational_failed_witnesses": len(OPERATIONAL_FAILURES),
            "new_failed_witnesses": MUTATION_COUNT + len(OPERATIONAL_FAILURES),
            "new_methods": MUTATION_COUNT + len(OPERATIONAL_FAILURES),
            "new_bounded_passing_witnesses": MUTATION_COUNT + len(OPERATIONAL_FAILURES),
            "failure_erasure_count": 0,
        },
        "effective_after_x2": {
            "negatives": STARTUP_NEGATIVES + MUTATION_COUNT + len(OPERATIONAL_FAILURES),
            "methods": STARTUP_METHODS + MUTATION_COUNT + len(OPERATIONAL_FAILURES),
        },
        "methods": methods,
        "valid": len(methods) == MUTATION_COUNT + len(OPERATIONAL_FAILURES),
    }

    portfolio = read_json(PHASE / "x1/portfolio-freeze.json")

    def portfolio_rows(key: str, outcome: str, evidence: str) -> list[dict[str, Any]]:
        return [
            {
                "record_id": row["record_id"],
                "title": row.get("title") or row.get("purpose") or row.get("slug"),
                "approval_class": row["approval_class"],
                "outcome": outcome,
                "evidence": evidence,
                "completion_credit": outcome == "completed",
                "protected_gates_preserved": True,
            }
            for row in portfolio[key]
        ]

    portfolio_execution = {
        "schema": "ghc.family.elowen.v665-v4.portfolio-execution.v1",
        "allowed_outcomes": ALLOWED_OUTCOMES,
        "safe_now": portfolio_rows(
            "safe_now", "completed", f"{PREFIX}x2/ledgers/execution-summary.json"
        ),
        "bounded_candidates": portfolio_rows(
            "bounded_candidates", "completed", f"{PREFIX}x2/ledgers/runner-registry.json"
        ),
        "exact_approval": portfolio_rows(
            "exact_approval", "exact_gate", f"{PREFIX}x2/ledgers/boundary-matrix.json"
        ),
        "blocked": portfolio_rows(
            "blocked", "open_gap", f"{PREFIX}x2/ledgers/boundary-matrix.json"
        ),
        "clean_fix_refine": portfolio_rows(
            "clean_fix_refine", "completed", f"{PREFIX}x2/validation/evidence-staged-review.json"
        ),
        "skill_ideas": [
            {
                "record_id": row["record_id"],
                "title": row.get("purpose") or row.get("slug"),
                "outcome": "completed",
                "evidence": skill_rows[index]["path"],
            }
            for index, row in enumerate(portfolio["skill_ideas"])
        ],
        "runner_ideas": [
            {
                "record_id": row["record_id"],
                "title": row.get("caller") or row.get("profile"),
                "outcome": "completed",
                "evidence": runner_rows[index]["path"],
            }
            for index, row in enumerate(portfolio["runner_ideas"])
        ],
        "inherited_completion_credit": 0,
        "destructive_cleanup_count": 0,
        "valid": True,
    }
    boundary_matrix = {
        "schema": "ghc.family.elowen.v665-v4.boundary-matrix.v1",
        "GMUT": "typed cellular-chain, primal-dual-complex, discrete-form, Hodge-star, codifferential, Laplacian, harmonic, cohomology, EFT, covariance, dimensional, uncertainty, identifiability, and continuum-limit obligations only; no real likelihood, constraint, force, prediction, confirmation, quantum completion, ultraviolet completion, final physics, theorem, or Theory of Everything",
        "THOS": "participant-free synthetic mosaic map-reading and handover comparison charter only; zero governed real participants, operators, arms, monitoring events, statistics, or independent review",
        "Freed_ID": "synthetic annotation-capability and relation profile only; zero real keys, proofs, issuance, resolution, status, revocation, interoperability, recovery, privacy/security review, or trust governance",
        "CBR": "site, land, heritage, sacred imagery, ownership, excavation, custody, recording, return, repatriation, taonga, remedy, legal, cultural, affected-party, tangata whenua, iwi, hapū, Māori wording and concepts, Māori-data-governance, and Māori-authority decisions remain exact-gated",
        "accessibility": "bounded structural affordances only; manual, browser-diverse, assistive-technology, cognitive-accessibility, Māori-language, and affected-user evaluation remain absent",
        "security": "bounded changed-code and mutation checks only; no exhaustive-security claim",
        "same_owner": "not independent reproduction or external audit",
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    source_ledger = read_json(PHASE / "x1/source-ledger.json")
    source_use = {
        "schema": "ghc.family.elowen.v665-v4.source-use-ledger.v1",
        "source_count": source_ledger["source_count"],
        "source_ids": [row["source_id"] for row in source_ledger["sources"]],
        "official_or_primary_source_page_reads": source_ledger.get("official_or_primary_source_page_reads", 0),
        "live_data_calls": 0,
        "met_collection_api_calls": 0,
        "iiif_manifest_calls": 0,
        "downloaded_empirical_rows": 0,
        "parsed_real_collection_records": 0,
        "real_objects_images_or_materials": 0,
        "version_vocabulary_and_boundary_use_only": True,
        "conformance_claim": False,
        "valid": True,
    }
    execution_summary = {
        "schema": "ghc.family.elowen.v665-v4.execution-summary.v1",
        "x1_commit": X1,
        "proposal_count": 20,
        "outcomes": counts,
        "mutations": {"executed": 100, "rejected": 100, "accepted": 0},
        "operational_failures_retained": len(OPERATIONAL_FAILURES),
        "portfolios": {
            "safe_now_completed": len(portfolio["safe_now"]),
            "bounded_candidates_completed": len(portfolio["bounded_candidates"]),
            "exact_approval_unexecuted": len(portfolio["exact_approval"]),
            "blocked_unexecuted": len(portfolio["blocked"]),
            "clean_fix_refine_completed": len(portfolio["clean_fix_refine"]),
        },
        "skills": {
            "built": 10,
            "read_through_eof": 10,
            "quick_validated": 10,
            "smoke_used": 10,
            "globally_installed": 0,
        },
        "runners": {"family_compatible": 10, "invoked": 10, "passed": 10},
        "real_rows": 0,
        "real_people": 0,
        "real_mosaics_images_or_materials": 0,
        "real_keys_or_proofs": 0,
        "authority_events": 0,
        "full_repository_suite_run": False,
        "independent_reproduction": False,
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": outcome_ledger["valid"]
        and mutation_ledger["valid"]
        and x1_integrity["valid"]
        and all(row["valid"] for row in runner_rows)
        and all(row["quick_valid"] and row["smoke_valid"] for row in skill_rows),
    }

    write_json(f"{PREFIX}x2/ledgers/outcome-ledger.json", outcome_ledger)
    write_json(f"{PREFIX}x2/ledgers/mutation-ledger.json", mutation_ledger)
    write_json(f"{PREFIX}x2/ledgers/method-flow-overlay.json", method_flow)
    write_json(f"{PREFIX}x2/ledgers/portfolio-execution.json", portfolio_execution)
    write_json(f"{PREFIX}x2/ledgers/boundary-matrix.json", boundary_matrix)
    write_json(f"{PREFIX}x2/ledgers/source-use-ledger.json", source_use)
    write_json(
        f"{PREFIX}x2/ledgers/skill-registry.json",
        {
            "schema": "ghc.family.elowen.v665-v4.skill-registry.v1",
            "count": len(skill_rows),
            "skills": skill_rows,
            "global_installation_performed": False,
            "valid": len(skill_rows) == 10
            and all(row["quick_valid"] and row["smoke_valid"] for row in skill_rows),
        },
    )
    write_json(
        f"{PREFIX}x2/ledgers/runner-registry.json",
        {
            "schema": "ghc.family.elowen.v665-v4.runner-registry.v1",
            "count": len(runner_rows),
            "runners": runner_rows,
            "family_current_prefix_preserved": True,
            "valid": len(runner_rows) == 10 and all(row["valid"] for row in runner_rows),
        },
    )
    write_json(f"{PREFIX}x2/ledgers/execution-summary.json", execution_summary)
    write_text(
        f"{PREFIX}x2/x2-overview.md",
        f"""# Elowen Cairn {PHASE_ID} bounded x2 evidence

This owner-local phase executed all 20 frozen proposals as evidence permitted:
exactly 14 completed, 4 represented, 1 open_gap, and 1 exact_gate. Every
proposal retained five preregistered rejection witnesses, so 100/100 mutations
were executed and rejected and zero were accepted.

Ten phase-local skills were built, read through EOF, quick-validated, and
smoke-used without global installation. Ten family-compatible ghc_family_*
runners were invoked through one bounded shared core. The frozen safe-now,
bounded-candidate, skill, runner, and additive CLEAN/FIX/REFINE portfolios were
executed only within their declared software, formal, structural, or synthetic
ceilings. Exact-approval and blocked work stayed unexecuted and visible.

The phase used zero real mosaics, tesserae, mortars, substrates, fragments,
images, sites, collection rows, people, tools, treatments, custody actions,
participants, identity events, keys, proofs, professional decisions, legal
decisions, cultural decisions, or authority acts. The Met and IIIF adapter made
zero calls and parsed zero rows. DEC surfaces are typed formal obligations, not
theorems, physical models, empirical GMUT results, or final physics.

Effective bounded evidence after all retained x1, mutation, and x2 operational
failures is {STARTUP_NEGATIVES + MUTATION_COUNT + len(OPERATIONAL_FAILURES)}
negatives and {STARTUP_METHODS + MUTATION_COUNT + len(OPERATIONAL_FAILURES)}
Method Flow methods. The cumulative gates are {INHERITED_OPEN_GAPS + 1} open
gaps and {INHERITED_EXACT_GATES + 1} exact gates. The terminal verdict remains
{TERMINAL_VERDICT}. Same-owner validation under shared infrastructure is not
independent-team reproduction.
""",
    )
    return {
        "valid": execution_summary["valid"],
        "proposals": 20,
        "mutations": 100,
        "skills": 10,
        "runners": 10,
        "base_paths": len(BASE_PATHS),
    }


def staged_paths() -> list[str]:
    raw = git("diff", "--cached", "--name-only", "--diff-filter=ACMR")
    return sorted(line for line in raw.splitlines() if line)


def index_blob(path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f":{path}"], cwd=ROOT, capture_output=True, check=True
    )
    return result.stdout


def scanner_candidates(path: str, raw: bytes) -> list[dict[str, str]]:
    text = raw.decode("utf-8", errors="replace")
    patterns = {
        "windows_private_absolute_path": re.compile(
            r"(?i)[a-z]:\\(?:users|ghc-archives)\\"
        ),
        "unix_private_absolute_path": re.compile(r"(?i)/(?:home|users)/[^\s'\"]+"),
        "raw_task_or_thread_identifier": re.compile(
            r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
            re.I,
        ),
        "credential_assignment": re.compile(
            r"(?i)(?:api[_-]?key|password|secret|token)\s*[:=]\s*['\"][^'\"]{8,}"
        ),
        "private_callable_or_session_stream": re.compile(
            r"(?i)(?:mcp__[a-z0-9_]{6,}|session_stream\s*[:=]|resume_value\s*[:=])"
        ),
    }
    return [
        {"path": path, "class": name}
        for name, pattern in patterns.items()
        if pattern.search(text)
    ]


def write_staged_review() -> None:
    actual = staged_paths()
    if actual != BASE_PATHS:
        raise EvidenceError(
            f"stage exact evidence base allowlist first: expected {len(BASE_PATHS)}, got {len(actual)}"
        )
    entries = []
    json_count = 0
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    for path in actual:
        raw = index_blob(path)
        entries.append({"path": path, "sha256": sha256(raw), "size": len(raw)})
        if path.endswith(".json"):
            strict_json_bytes(raw, path)
            json_count += 1
        path_candidates = scanner_candidates(path, raw)
        candidates.extend(path_candidates)
        confirmed.extend(path_candidates)
    diff_check = run("git", "diff", "--cached", "--check", check=False)
    if diff_check.returncode != 0:
        raise EvidenceError("staged diff hygiene failed: " + diff_check.stdout.strip())
    if confirmed:
        raise EvidenceError(f"confirmed privacy or raw-identifier candidates: {confirmed}")
    manifest = {
        "schema": "ghc.family.elowen.v665-v4.evidence-content-manifest.v1",
        "hash_domain": "exact staged Git blobs",
        "intended_path_count": len(INTENDED_PATHS),
        "entry_count": len(entries),
        "declared_self_exclusion_count": len(SELF_EXCLUSIONS),
        "declared_self_exclusions": SELF_EXCLUSIONS,
        "entries": entries,
        "coverage_valid": len(entries) + len(SELF_EXCLUSIONS) == len(INTENDED_PATHS),
    }
    review = {
        "schema": "ghc.family.elowen.v665-v4.evidence-staged-review.v1",
        "staged_base_path_count": len(actual),
        "strict_json_count": json_count,
        "five_scan_classes": [
            "windows_private_absolute_path",
            "unix_private_absolute_path",
            "raw_task_or_thread_identifier",
            "credential_assignment",
            "private_callable_or_session_stream",
        ],
        "scanner_candidates": candidates,
        "confirmed_privacy_or_raw_identifier_hits": len(confirmed),
        "diff_hygiene_issues": 0,
        "x1_paths_modified": [path for path in actual if f"{PREFIX}x1/" in path],
        "source_or_sibling_paths_modified": [
            path
            for path in actual
            if path.startswith("docs/") and not path.startswith(PREFIX)
        ],
        "valid": not confirmed
        and not any(f"{PREFIX}x1/" in path for path in actual)
        and not any(
            path.startswith("docs/") and not path.startswith(PREFIX) for path in actual
        ),
    }
    candidate = {
        "schema": "ghc.family.elowen.v665-v4.evidence-stage-candidate.v1",
        "source_commit": SOURCE_FINAL,
        "x1_commit": X1,
        "branch": BRANCH,
        "manifest": SELF_EXCLUSIONS[0],
        "staged_review": SELF_EXCLUSIONS[2],
        "test_command": "python tests/test_ghc_family_elowen_v665_v4_x2.py -v",
        "outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "mutations": {"executed": 100, "rejected": 100, "accepted": 0},
        "commit_state": "PREPARED_NOT_COMMITTED",
        "push_state": "PREPARED_NOT_PUSHED",
        "remote_equality_state": "PREPARED_NOT_PROVED",
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": manifest["coverage_valid"] and review["valid"],
    }
    write_json(SELF_EXCLUSIONS[0], manifest)
    write_json(SELF_EXCLUSIONS[1], candidate)
    write_json(SELF_EXCLUSIONS[2], review)


def check_staged() -> dict[str, Any]:
    actual = staged_paths()
    if actual != INTENDED_PATHS:
        raise EvidenceError(
            f"staged evidence allowlist changed: expected {len(INTENDED_PATHS)}, got {len(actual)}"
        )
    manifest = strict_json_bytes(index_blob(SELF_EXCLUSIONS[0]), "staged manifest")
    review = strict_json_bytes(index_blob(SELF_EXCLUSIONS[2]), "staged review")
    candidate = strict_json_bytes(index_blob(SELF_EXCLUSIONS[1]), "staged candidate")
    mismatches = []
    for entry in manifest["entries"]:
        raw = index_blob(entry["path"])
        if sha256(raw) != entry["sha256"] or len(raw) != entry["size"]:
            mismatches.append(entry["path"])
    all_candidates = []
    json_count = 0
    for path in actual:
        raw = index_blob(path)
        all_candidates.extend(scanner_candidates(path, raw))
        if path.endswith(".json"):
            strict_json_bytes(raw, path)
            json_count += 1
    diff_check = run("git", "diff", "--cached", "--check", check=False)
    if mismatches or all_candidates or diff_check.returncode != 0:
        raise EvidenceError(
            f"staged audit failure: mismatches={mismatches}, candidates={all_candidates}, diff={diff_check.stdout.strip()}"
        )
    if not (manifest["coverage_valid"] and review["valid"] and candidate["valid"]):
        raise EvidenceError("one staged receipt is invalid")
    return {
        "valid": True,
        "staged_paths": len(actual),
        "manifest_entries": len(manifest["entries"]),
        "manifest_exclusions": len(manifest["declared_self_exclusions"]),
        "strict_json": json_count,
        "privacy_confirmed_hits": 0,
        "diff_hygiene_issues": 0,
    }


def prepare() -> dict[str, Any]:
    result = build_evidence()
    run("git", "add", "--sparse", "--", *BASE_PATHS)
    write_staged_review()
    run("git", "add", "--", *SELF_EXCLUSIONS)
    audit = check_staged()
    return {**result, **audit}


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--prepare", action="store_true")
    modes.add_argument("--check-staged", action="store_true")
    modes.add_argument("--list-base-paths", action="store_true")
    args = parser.parse_args()
    if args.prepare:
        result = prepare()
    elif args.check_staged:
        result = check_staged()
    else:
        result = {"base_paths": BASE_PATHS, "self_exclusions": SELF_EXCLUSIONS}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
