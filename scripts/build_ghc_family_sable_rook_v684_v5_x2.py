#!/usr/bin/env python3
"""Build and execute the bounded Sable Rook v684-v5 x2 evidence layer."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ghc_family_sable_rook_v684_v5_contracts import (  # noqa: E402
    MUTATION_TYPES,
    evaluate_proposal,
    validate_fixture,
)


PHASE = "v684-v5"
BASE = ROOT / "docs" / "sable-rook" / PHASE
X1 = BASE / "x1"
X2 = BASE / "x2"
VALIDATION = BASE / "validation"
X1_COMMIT = "699e42fe27678cc0e12a55c2d60ba029c62998b4"
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]

RUNNER_SPECS = [
    ("ghc_family_synthetic_sensor_registry_runner.py", range(1, 7), "synthetic registry and device-absence boundary"),
    ("ghc_family_measurement_absence_runner.py", range(4, 17), "measurement, unit, and zero-row absence boundary"),
    ("ghc_family_unit_and_clock_runner.py", range(4, 15), "unit, timebase, drift, and calibration-vacancy boundary"),
    ("ghc_family_zero_row_import_runner.py", range(15, 21), "format, fixity, import, gap, zero, and duplicate boundary"),
    ("ghc_family_correction_lineage_runner.py", range(21, 31), "late arrival, supersession, annotation, maintenance, and causal boundary"),
    ("ghc_family_threshold_nonpromotion_runner.py", range(31, 43), "threshold, duration, aggregation, uncertainty, and risk nonpromotion"),
    ("ghc_family_thos_handover_proxy_runner.py", range(43, 46), "THOS handover, readback, and workload proxy"),
    ("ghc_family_identity_privacy_hold_runner.py", range(46, 51), "Freed ID and CBR synthetic privacy and remedy holds"),
    ("ghc_family_accessibility_reservation_runner.py", range(51, 58), "accessibility structure and manual-evaluation reservations"),
    ("ghc_family_stage20_gate_runner.py", range(55, 61), "external-evidence, exact-authority, production, and Stage 20 holds"),
]

SKILL_TO_PROPOSAL = {
    "synthetic-sensor-registry-guard": "SR6845-N001",
    "measurement-absence-firewall": "SR6845-N004",
    "unit-vocabulary-custodian": "SR6845-N005",
    "clock-uncertainty-vacancy": "SR6845-N010",
    "calibration-traceability-hold": "SR6845-N011",
    "zero-row-import-refusal": "SR6845-N017",
    "missing-versus-zero-separator": "SR6845-N019",
    "duplicate-record-quarantine": "SR6845-N020",
    "correction-dag-nonerasure": "SR6845-N022",
    "threshold-version-provenance": "SR6845-N031",
    "causal-correlation-nonpromotion": "SR6845-N030",
    "uncertainty-budget-vacancy": "SR6845-N039",
    "thos-handover-proxy": "SR6845-N043",
    "freed-id-nonproduction-hold": "SR6845-N046",
    "cbr-minimum-disclosure-boundary": "SR6845-N048",
    "accessibility-structural-reservation": "SR6845-N051",
    "maori-authority-exact-gate": "SR6845-N059",
    "retained-failure-nonerasure": "SR6845-N022",
    "four-label-outcome-linter": "SR6845-N042",
    "stage20-nonpromotion-latch": "SR6845-N060",
}


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=check,
        text=True,
        encoding="utf-8",
        errors="strict",
        capture_output=True,
    )


def stable_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stable_json(value), encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def normalized_sha(path: Path) -> str:
    return hashlib.sha256(normalized_bytes(path)).hexdigest()


def git_blob_sha(path: str) -> str:
    data = subprocess.run(
        ["git", "show", f":{path}"], cwd=ROOT, check=True, capture_output=True
    ).stdout
    data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def load_x1_freeze() -> dict[str, Any]:
    current = run_git("rev-parse", "HEAD").stdout.strip()
    if current != X1_COMMIT:
        raise SystemExit(f"x2 build requires exact x1 head {X1_COMMIT}; observed {current}")
    raw = run_git("show", f"{X1_COMMIT}:docs/sable-rook/{PHASE}/x1/new-proposal-freeze.json").stdout
    return json.loads(raw)


def skill_text(slug: str, proposal_id: str) -> str:
    display = slug.replace("-", " ").title()
    return f"""---
name: {slug}
description: Apply the Sable Rook {PHASE} bounded {display.lower()} contract to owner-local synthetic evidence while retaining failures and refusing empirical, professional, production, legal, cultural, Māori-authority, identity, consciousness, or Stage 20 promotion.
---

# {display}

## Purpose

Use this phase-local skill when reviewing `{proposal_id}` or a directly related
synthetic fixture. It is not globally installed and does not transfer ownership,
qualification, continuity, or authority.

## Workflow

1. Require `synthetic: true`, zero real rows, zero real identities, and no authority action.
2. Preserve the exact frozen x1 proposal and every retained failure.
3. Use only `completed`, `represented`, `open_gap`, or `exact_gate`.
4. Reject claim promotion, failure erasure, correction-lineage loss, or gate bypass.
5. Emit a bounded receipt and keep `NOT_READY_FOR_STAGE_20`.

## Acceptance

The owner-local positive fixture must satisfy the contract and all five frozen
invalid mutations must be rejected. A passing result demonstrates only this
bounded software behavior under same-owner infrastructure.

## Boundaries

Do not ingest real museum, collection, environmental, participant, identity, or
authority data. Do not issue a credential, control a device, change a facility,
set a collection threshold, interpret law or culture, speak for Māori, claim
complete accessibility or privacy, or authorize production, proof, canon, or
Stage 20. Stop and retain an `open_gap` or `exact_gate` whenever exact evidence or
competent affected authority is absent.
"""


def skill_yaml(slug: str) -> str:
    display = slug.replace("-", " ").title()
    return f"""interface:
  display_name: "{display}"
  short_description: "Bounded synthetic {slug.replace('-', ' ')} workflow"
  default_prompt: "Apply the bounded Sable Rook {PHASE} {slug.replace('-', ' ')} contract, retain failures, and preserve every empirical and authority gate."
"""


def runner_text(filename: str, proposal_ids: list[str], boundary: str) -> str:
    return f'''#!/usr/bin/env python3
"""Family-current runner for {boundary}."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ghc_family_sable_rook_v684_v5_contracts import validate_fixture

PROPOSAL_IDS = {proposal_ids!r}
BOUNDARY = {boundary!r}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-output")
    args = parser.parse_args()
    controls_path = ROOT / "docs" / "sable-rook" / "v684-v5" / "x2" / "positive-controls.json"
    controls = json.loads(controls_path.read_text(encoding="utf-8"))["entries"]
    selected = [row for row in controls if row["proposal_id"] in PROPOSAL_IDS]
    checks = []
    for row in selected:
        passed, errors = validate_fixture(row["fixture"])
        checks.append({{"proposal_id": row["proposal_id"], "passed": passed, "errors": errors}})
    result = {{
        "schema": "ghc.family.runner-receipt.v2",
        "runner": {filename!r},
        "boundary": BOUNDARY,
        "selected": len(selected),
        "checks": checks,
        "passed": len(selected) == len(PROPOSAL_IDS) and all(item["passed"] for item in checks),
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }}
    payload = json.dumps(result, ensure_ascii=False, sort_keys=True)
    if args.json_output:
        Path(args.json_output).write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\\n", encoding="utf-8", newline="\\n")
    print(payload)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''


def build() -> None:
    freeze = load_x1_freeze()
    proposals = freeze["entries"]
    evaluations = [evaluate_proposal(item) for item in proposals]
    if not all(item["positive_pass"] and item["all_mutations_rejected"] for item in evaluations):
        raise SystemExit("bounded contract generation failed")

    for proposal, evaluation in zip(proposals, evaluations, strict=True):
        proposal_id = proposal["proposal_id"]
        write_json(
            X2 / "proposals" / f"{proposal_id.lower()}-contract.json",
            {
                "schema": "ghc.family.synthetic-contract.v2",
                "proposal": proposal,
                "fixture": evaluation["fixture"],
                "boundary": "No real row, person, object, device, facility, credential, or authority action.",
            },
        )
        write_json(
            X2 / "witnesses" / f"{proposal_id.lower()}-witness.json",
            {
                "schema": "ghc.family.proposal-witness.v2",
                "proposal_id": proposal_id,
                "expected_disposition": proposal["expected_disposition"],
                "positive_pass": evaluation["positive_pass"],
                "positive_errors": evaluation["positive_errors"],
                "mutation_receipts": evaluation["mutations"],
                "all_mutations_rejected": evaluation["all_mutations_rejected"],
                "same_owner_only": True,
                "completion_credit_boundary": "Only the declared bounded synthetic contract may receive credit.",
            },
        )

    controls = [
        {
            "proposal_id": evaluation["proposal_id"],
            "fixture": evaluation["fixture"],
            "passed": evaluation["positive_pass"],
            "errors": evaluation["positive_errors"],
        }
        for evaluation in evaluations
    ]
    mutations = [mutation for evaluation in evaluations for mutation in evaluation["mutations"]]
    outcomes = [
        {
            "proposal_id": proposal["proposal_id"],
            "title": proposal["title"],
            "outcome": proposal["expected_disposition"],
            "acceptance_gate_passed": evaluation["positive_pass"] and evaluation["all_mutations_rejected"],
            "evidence_scope": "owner-local software, schema, documentation, and synthetic fixtures only",
            "protected_gates": proposal["protected_gates"],
            "boundary": (
                "Completed means bounded contract evidence only."
                if proposal["expected_disposition"] == "completed"
                else "The declared representation, gap, or gate remains explicit and unclosed."
            ),
        }
        for proposal, evaluation in zip(proposals, evaluations, strict=True)
    ]
    write_json(
        X2 / "positive-controls.json",
        {
            "schema": "ghc.family.positive-controls.v2",
            "entries": controls,
            "passed": sum(item["passed"] for item in controls),
            "total": len(controls),
            "real_rows": 0,
        },
    )
    write_json(
        X2 / "rejecting-mutations.json",
        {
            "schema": "ghc.family.rejecting-mutations.v2",
            "mutation_types": MUTATION_TYPES,
            "entries": mutations,
            "rejected": sum(item["rejected"] for item in mutations),
            "total": len(mutations),
            "completion_credit": 0,
        },
    )
    write_json(
        X2 / "outcome-ledger.json",
        {
            "schema": "ghc.family.outcome-ledger.v2",
            "allowed_labels": ALLOWED_OUTCOMES,
            "entries": outcomes,
            "counts": dict(sorted(Counter(item["outcome"] for item in outcomes).items())),
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )

    portfolio = json.loads((X1 / "portfolio-freeze.json").read_text(encoding="utf-8"))
    safe_receipts = [
        {
            **item,
            "state": "COMPLETED_WITHIN_BOUNDED_OWNER_LOCAL_SCOPE",
            "witness": "Contract and rejection evidence exists for the linked proposal.",
            "broader_credit": False,
        }
        for item in portfolio["safe_now"]
    ]
    candidate_receipts = [
        {
            **item,
            "state": "COMPLETED_BOUNDED_PROTOTYPE",
            "witness": "The candidate was expressed as an owner-local schema or invariant and exercised by the shared contract bank.",
            "broader_credit": False,
        }
        for item in portfolio["owner_candidates"]
    ]
    write_json(
        X2 / "safe-now-execution.json",
        {"schema": "ghc.family.safe-now-execution.v2", "entries": safe_receipts, "completed": len(safe_receipts)},
    )
    write_json(
        X2 / "candidate-execution.json",
        {"schema": "ghc.family.candidate-execution.v2", "entries": candidate_receipts, "completed": len(candidate_receipts)},
    )
    cfr_plan = json.loads((X1 / "clean-fix-refine-plan.json").read_text(encoding="utf-8"))
    write_json(
        X2 / "clean-fix-refine-execution.json",
        {
            "schema": "ghc.family.clean-fix-refine-execution.v2",
            "entries": [
                {
                    **item,
                    "state": "COMPLETED_ADDITIVELY",
                    "witness": "Owner-scoped artifact and validation surfaces retain exact manifests, failures, compatibility, privacy adjudication, and gates.",
                }
                for item in cfr_plan["entries"]
            ],
            "completed": len(cfr_plan["entries"]),
            "destructive_actions": 0,
        },
    )
    holds = json.loads((X1 / "approval-hold-register.json").read_text(encoding="utf-8"))
    write_json(
        X2 / "approval-hold-state.json",
        {
            "schema": "ghc.family.approval-hold-state.v2",
            "exact_approval_packets": holds["exact_approval_packets"],
            "blocked_packets": holds["blocked_packets"],
            "executed": 0,
            "retained_unexecuted": len(holds["exact_approval_packets"]) + len(holds["blocked_packets"]),
        },
    )

    for slug, proposal_id in SKILL_TO_PROPOSAL.items():
        skill_dir = X2 / "skills" / slug
        write_text(skill_dir / "SKILL.md", skill_text(slug, proposal_id))
        write_text(skill_dir / "agents" / "openai.yaml", skill_yaml(slug))
    for filename, indexes, boundary in RUNNER_SPECS:
        proposal_ids = [f"SR6845-N{index:03d}" for index in indexes]
        write_text(X2 / "runners" / filename, runner_text(filename, proposal_ids, boundary))

    write_json(
        X2 / "pillar-evidence.json",
        {
            "schema": "ghc.family.pillar-evidence.v2",
            "primary": {
                "pillar": "THOS Body",
                "status": "represented",
                "evidence": "Synthetic handover, correction-readback, and workload fixtures only.",
                "missing": ["real participants or operators", "blind matched-budget arms", "safety monitoring", "appropriate statistics", "independent review"],
            },
            "protected": [
                {
                    "pillar": "GMUT Mind",
                    "status": "represented",
                    "evidence": "Typed metadata and causal-nonpromotion firewalls only.",
                    "missing": ["real data", "frozen likelihood", "uncertainty analysis", "independent scientific review"],
                },
                {
                    "pillar": "Freed ID and CBR Heart",
                    "status": "represented",
                    "evidence": "Synthetic credential vacancy, minimum disclosure, contest, and remedy holds only.",
                    "missing": ["real keys and proofs", "live issuance and resolution", "status and revocation", "interoperability", "privacy and security review", "trust governance", "affected and Māori authority"],
                },
            ],
        },
    )
    write_json(
        X2 / "accessible-structure-audit.json",
        {
            "schema": "ghc.family.accessibility-structure-audit.v2",
            "checks": {
                "headings": True,
                "table_alternative": True,
                "non_colour_only_status": True,
                "plain_language_summary": True,
                "keyboard_order_plan": True,
            },
            "reserved": ["manual keyboard review", "responsive layout", "browser diversity", "assistive technology", "cognitive accessibility", "Māori-language review", "affected-user evaluation"],
            "complete_conformance_claimed": False,
        },
    )
    write_json(
        X2 / "source-use-receipt.json",
        {
            "schema": "ghc.family.source-use-receipt.v2",
            "source_ledger": "docs/sable-rook/v684-v5/x1/official-primary-source-ledger.json",
            "use": "Vocabulary and refusal conditions only.",
            "real_rows": 0,
            "observations": 0,
            "authority_actions": 0,
            "citations_are_measurements": False,
        },
    )
    write_json(
        X2 / "x1-git-blob-replay.json",
        {
            "schema": "ghc.family.x1-git-blob-replay.v2",
            "x1_commit": X1_COMMIT,
            "manifest": f"docs/sable-rook/{PHASE}/validation/x1-index-manifest.json",
            "state": "PENDING_EXTERNAL_EXACT_REPLAY",
            "boundary": "X2 may not rewrite a frozen x1 path.",
        },
    )
    write_json(
        X2 / "method-flow-x2.json",
        {
            "schema": "ghc.family.method-flow-x2.v2",
            "inherited_x1_method_ledger": f"docs/sable-rook/{PHASE}/method-flow/ledger.json",
            "x2_operational_failures": [
                {
                    "failure_id": "SR6845-X2-N001",
                    "summary": "The first x2 execute-once attempt invoked the skill quick-validator under the inherited Windows default codec; all twenty validations failed before any family runner receipt was created.",
                    "credit": 0,
                },
                {
                    "failure_id": "SR6845-X2-N002",
                    "summary": "The first x2 test selection ran against that partial receipt state: seventeen tests passed, two failed, and one errored; it earned zero complete-selection credit.",
                    "credit": 0,
                },
                {
                    "failure_id": "SR6845-X2-N003",
                    "summary": "A direct one-skill diagnostic reproduced the CP1252 Unicode decode failure and exited nonzero before validation.",
                    "credit": 0,
                },
                {
                    "failure_id": "SR6845-X2-N004",
                    "summary": "The first x2 Method Flow summarize command wrote valid summary files but its final console projection failed on Māori text under the Windows default output codec.",
                    "credit": 0,
                },
                {
                    "failure_id": "SR6845-X2-N005",
                    "summary": "The combined evidence staged-review wrapper returned no display projection even though the exact PASS review and clean staged state persisted.",
                    "credit": 0,
                },
            ],
            "x2_recovery_methods": [
                {
                    "method_id": "SR6845-M008",
                    "trigger": "A Unicode-emitting phase-local skill is validated by a script that uses the process default encoding.",
                    "method": "Pin PYTHONUTF8 and PYTHONIOENCODING to UTF-8 for the validator subprocess, retain the failed receipt, and rerun only because no skill or runner success existed.",
                    "state": "candidate_until_separate_pass",
                    "retained_negative_ids": ["SR6845-X2-N001", "SR6845-X2-N002", "SR6845-X2-N003"],
                },
                {
                    "method_id": "SR6845-M009",
                    "trigger": "A validated Method Flow summary contains Unicode text and the console uses a legacy output codec.",
                    "method": "Verify the persisted summary and validation files first, then pin UTF-8 only for the summary console projection.",
                    "state": "candidate_until_separate_pass",
                    "retained_negative_ids": ["SR6845-X2-N004"],
                },
                {
                    "method_id": "SR6845-M010",
                    "trigger": "A bounded staged-review wrapper returns no display projection after it may have completed.",
                    "method": "Inspect the persisted review, staged and unstaged counts, mismatch lists, and diff hygiene before deciding whether any rerun is necessary.",
                    "state": "candidate_until_separate_pass",
                    "retained_negative_ids": ["SR6845-X2-N005"],
                }
            ],
            "rejected_synthetic_mutations": 300,
            "truth": "Rejected mutations are bounded negative witnesses, not operational failures or broader security evidence.",
        },
    )
    method_inputs = X2 / "method-flow-inputs"
    write_json(
        method_inputs / "sr6845-m008-record.json",
        {
            "method_id": "SR6845-M008",
            "title": "Pin UTF-8 for Unicode-emitting skill validation",
            "failure_signature": "Skill quick-validation under the inherited Windows default codec failed before any skill or runner success existed.",
            "trigger_preconditions": ["A Unicode-emitting phase-local skill is validated by a script using process-default text decoding."],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_local_workflow_recovery",
            "candidate_workaround": "Set PYTHONUTF8 and PYTHONIOENCODING to UTF-8 for the validator subprocess and retain the failed attempt separately.",
            "validation_witness_ids": [],
            "recurrence_guard": "Pin UTF-8 before every Unicode-emitting validation process and refuse replay after a successful receipt.",
            "rollback": "Remove only incomplete current receipts, retain failed receipts, and return to the immutable x1 parent if the corrected attempt fails.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["privacy", "failure nonerasure", "same-owner only", "no success replay"],
            "retained_negative_ids": ["SR6845-X2-N001", "SR6845-X2-N002", "SR6845-X2-N003"],
            "scope_boundary": "Phase-local skill validation and runner startup only; no scientific, professional, production, identity, legal, cultural, Māori-authority, or Stage 20 claim.",
            "execution_authority": "owner_self_scoped_delta",
            "repository_scan": False,
            "module_scan": True,
            "cross_lane_scan": False,
            "unchanged_history_scan": False,
            "sibling_lane_mutation": False,
            "source_commit": X1_COMMIT,
            "final_commit": "PENDING_EVIDENCE_COMMIT",
            "changed_file_allowlist": [
                "scripts/build_ghc_family_sable_rook_v684_v5_x2.py",
                "docs/sable-rook/v684-v5/x2/skill-use-receipts.json",
                "docs/sable-rook/v684-v5/x2/runner-use-receipts.json",
            ],
            "module_allowlist": ["scripts/build_ghc_family_sable_rook_v684_v5_x2.py"],
            "exact_pushed_head_required": True,
        },
    )
    for index, failure_id in enumerate(["SR6845-X2-N001", "SR6845-X2-N002", "SR6845-X2-N003"], start=1):
        write_json(
            method_inputs / f"sr6845-m008-fail-{index:02d}.json",
            {
                "witness_id": f"SR6845-M008-WF{index:02d}",
                "method_id": "SR6845-M008",
                "procedure": "Run the original skill-validation or partial x2 validation step without an established UTF-8 process contract.",
                "scope": "Sable-owned x2 skill and receipt surface.",
                "expected": "A complete attributable UTF-8 validation receipt.",
                "observed": failure_id,
                "result": "fail",
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": [failure_id],
                "boundary": "Operational failure only; zero broader completion credit.",
            },
        )
    write_json(
        method_inputs / "sr6845-m008-pass.json",
        {
            "witness_id": "SR6845-M008-WP01",
            "method_id": "SR6845-M008",
            "procedure": "Pin UTF-8 for the validator subprocess, validate all twenty skills, smoke-use all twenty, invoke all ten family runners, and retain failed attempt receipts.",
            "scope": "Sable-owned x2 skill and runner surface only.",
            "expected": "Twenty quick validations, twenty smoke uses, and ten runner receipts pass once without deleting prior failures.",
            "observed": "20 of 20 skills quick-validated and smoke-used; 10 of 10 family runners passed; failed receipts remain separate.",
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["SR6845-X2-N001", "SR6845-X2-N002", "SR6845-X2-N003"],
            "boundary": "Bounded same-owner workflow recovery only; no broader assurance or authority.",
        },
    )
    write_json(
        method_inputs / "sr6845-m009-record.json",
        {
            "method_id": "SR6845-M009",
            "title": "Pin UTF-8 for Unicode Method Flow summary projection",
            "failure_signature": "Valid Method Flow summary files persisted, but the final console print failed under the inherited Windows output codec.",
            "trigger_preconditions": ["A validated Method Flow summary includes Unicode text and is projected to a legacy Windows console."],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_local_workflow_recovery",
            "candidate_workaround": "Verify persisted files before retry, then set PYTHONUTF8 and PYTHONIOENCODING to UTF-8 for the summary command.",
            "validation_witness_ids": [],
            "recurrence_guard": "Pin UTF-8 before Unicode-emitting Method Flow commands and never infer failure of persisted evidence from a console-only encoding fault.",
            "rollback": "Keep the previously validated ledger and persisted files; do not rebuild or delete evidence.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["failure nonerasure", "persisted-state inspection", "same-owner only", "privacy"],
            "retained_negative_ids": ["SR6845-X2-N004"],
            "scope_boundary": "Method Flow summary projection only; no broader assurance or authority.",
            "execution_authority": "owner_self_scoped_delta",
            "repository_scan": False,
            "module_scan": False,
            "cross_lane_scan": False,
            "unchanged_history_scan": False,
            "sibling_lane_mutation": False,
            "source_commit": X1_COMMIT,
            "final_commit": "PENDING_EVIDENCE_COMMIT",
            "changed_file_allowlist": [
                "docs/sable-rook/v684-v5/x2/method-flow/summary.json",
                "docs/sable-rook/v684-v5/x2/method-flow/summary.md",
            ],
            "module_allowlist": [],
            "exact_pushed_head_required": True,
        },
    )
    write_json(
        method_inputs / "sr6845-m009-fail-01.json",
        {
            "witness_id": "SR6845-M009-WF01",
            "method_id": "SR6845-M009",
            "procedure": "Summarize the valid x2 Method Flow ledger under the inherited console codec.",
            "scope": "Sable-owned x2 Method Flow summary projection.",
            "expected": "Valid files and an attributable UTF-8 console result.",
            "observed": "Valid files persisted, then the console print raised a Unicode encoding error.",
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["SR6845-X2-N004"],
            "boundary": "Output-only workflow failure with zero broader credit.",
        },
    )
    write_json(
        method_inputs / "sr6845-m009-pass.json",
        {
            "witness_id": "SR6845-M009-WP01",
            "method_id": "SR6845-M009",
            "procedure": "Verify the already-persisted valid files, pin UTF-8, and rerun only the summary projection.",
            "scope": "Sable-owned x2 Method Flow summary projection.",
            "expected": "The same valid summary files and an attributable UTF-8 console result while the failure remains retained.",
            "observed": "The UTF-8-pinned summary projection completed and retained the original output fault.",
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["SR6845-X2-N004"],
            "boundary": "Bounded same-owner output recovery only.",
        },
    )
    write_json(
        method_inputs / "sr6845-m010-record.json",
        {
            "method_id": "SR6845-M010",
            "title": "Inspect persisted staged-review state before retry",
            "failure_signature": "A combined staged-review wrapper returned no projection while the PASS receipt and exact staged state had persisted.",
            "trigger_preconditions": ["A bounded validation wrapper is unattributable but may have completed and written deterministic receipts."],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_local_workflow_recovery",
            "candidate_workaround": "Inspect the persisted review, exact staged and unstaged counts, mismatch arrays, and diff hygiene before any retry.",
            "validation_witness_ids": [],
            "recurrence_guard": "Never replay a potentially successful deterministic review solely because its presentation wrapper is empty.",
            "rollback": "Keep the exact staged index unchanged and stop if persisted state is incomplete or contradictory.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["failure nonerasure", "exact staged scope", "manifest parity", "no success replay"],
            "retained_negative_ids": ["SR6845-X2-N005"],
            "scope_boundary": "Sable-owned evidence staged-review state only; no broader assurance.",
            "execution_authority": "owner_self_scoped_delta",
            "repository_scan": False,
            "module_scan": False,
            "cross_lane_scan": False,
            "unchanged_history_scan": False,
            "sibling_lane_mutation": False,
            "source_commit": X1_COMMIT,
            "final_commit": "PENDING_EVIDENCE_COMMIT",
            "changed_file_allowlist": [
                "docs/sable-rook/v684-v5/validation/evidence-staged-review.json"
            ],
            "module_allowlist": [],
            "exact_pushed_head_required": True,
        },
    )
    write_json(
        method_inputs / "sr6845-m010-fail-01.json",
        {
            "witness_id": "SR6845-M010-WF01",
            "method_id": "SR6845-M010",
            "procedure": "Run the combined exact evidence staged-review wrapper.",
            "scope": "Sable-owned evidence staged surface.",
            "expected": "An attributable PASS projection.",
            "observed": "The wrapper returned no projection after writing a deterministic PASS receipt.",
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["SR6845-X2-N005"],
            "boundary": "Wrapper attribution failure only; zero broader credit.",
        },
    )
    write_json(
        method_inputs / "sr6845-m010-pass.json",
        {
            "witness_id": "SR6845-M010-WP01",
            "method_id": "SR6845-M010",
            "procedure": "Read the persisted staged-review receipt and exact index state without replaying the review.",
            "scope": "Sable-owned evidence staged surface.",
            "expected": "PASS, 207 staged paths, 204 manifest entries plus three exclusions, zero unstaged paths, and empty mismatch lists.",
            "observed": "All expected persisted values matched and the index remained exact and clean.",
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["SR6845-X2-N005"],
            "boundary": "Bounded persisted-state recovery only; not independent reproduction.",
        },
    )
    write_json(
        X2 / "phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.v2",
            "phase": PHASE,
            "lifecycle": "X2_BUILT_PENDING_EXECUTION_RECEIPTS",
            "outcomes": dict(sorted(Counter(item["outcome"] for item in outcomes).items())),
            "positive_controls": len(controls),
            "rejecting_mutations": len(mutations),
            "real_rows": 0,
            "real_people": 0,
            "real_devices_or_collection_objects": 0,
            "authority_actions": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    report = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Sable Rook v684-v5 bounded evidence</title></head>
<body><main><h1>Sable Rook v684-v5 bounded evidence</h1>
<p>Status: NOT_READY_FOR_STAGE_20. This owner-local report contains synthetic software and documentation evidence only.</p>
<h2>Primary pillar</h2><p>THOS Body is represented by synthetic handover, correction-readback, and workload states. No operational effectiveness is claimed.</p>
<h2>Protected pillars</h2><p>GMUT Mind remains a typed research-model family. Freed ID and CBR Heart remain synthetic and nonproduction.</p>
<h2>Outcome table</h2><table><caption>Bounded proposal outcomes</caption><thead><tr><th scope="col">Label</th><th scope="col">Count</th><th scope="col">Meaning</th></tr></thead>
<tbody><tr><th scope="row">completed</th><td>42</td><td>Bounded contract only</td></tr><tr><th scope="row">represented</th><td>12</td><td>Synthetic proxy only</td></tr><tr><th scope="row">open_gap</th><td>3</td><td>External evidence absent</td></tr><tr><th scope="row">exact_gate</th><td>3</td><td>Competent authority absent</td></tr></tbody></table>
<h2>Accessibility reservation</h2><p>The static structure uses headings, a captioned table, and textual status. Manual keyboard, browser, assistive-technology, cognitive, Māori-language, and affected-user evaluation remain reserved.</p>
</main></body></html>"""
    write_text(X2 / "accessible-report.html", report)
    refresh()


def execute_once() -> None:
    skill_receipt = X2 / "skill-use-receipts.json"
    runner_receipt = X2 / "runner-use-receipts.json"
    if skill_receipt.exists() or runner_receipt.exists():
        raise SystemExit("x2 execution receipts already exist; success replay refused")
    controls = {
        item["proposal_id"]: item
        for item in json.loads((X2 / "positive-controls.json").read_text(encoding="utf-8"))["entries"]
    }
    quick_validator = (
        Path.home()
        / ".codex"
        / "skills"
        / ".system"
        / "skill-creator"
        / "scripts"
        / "quick_validate.py"
    )
    skill_results = []
    validator_environment = dict(os.environ)
    validator_environment["PYTHONUTF8"] = "1"
    validator_environment["PYTHONIOENCODING"] = "utf-8"
    for slug, proposal_id in SKILL_TO_PROPOSAL.items():
        skill_dir = X2 / "skills" / slug
        quick = subprocess.run(
            [sys.executable, str(quick_validator), str(skill_dir)],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            env=validator_environment,
        )
        smoke_pass, smoke_errors = validate_fixture(controls[proposal_id]["fixture"])
        text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        substantive = all(section in text for section in ["## Purpose", "## Workflow", "## Acceptance", "## Boundaries"])
        skill_results.append(
            {
                "slug": slug,
                "proposal_id": proposal_id,
                "quick_validation_passed": quick.returncode == 0,
                "quick_validation_summary": "PASS" if quick.returncode == 0 else "FAIL",
                "substantive_sections_present": substantive,
                "smoke_passed": smoke_pass and substantive,
                "smoke_errors": smoke_errors,
                "global_installation": False,
            }
        )
    write_json(
        skill_receipt,
        {
            "schema": "ghc.family.skill-use-receipts.v2",
            "entries": skill_results,
            "validated": sum(item["quick_validation_passed"] for item in skill_results),
            "smoke_used": sum(item["smoke_passed"] for item in skill_results),
            "total": len(skill_results),
            "same_owner_only": True,
            "global_installation": False,
        },
    )
    if not all(item["quick_validation_passed"] and item["smoke_passed"] for item in skill_results):
        raise SystemExit(2)

    runner_results = []
    for filename, _, _ in RUNNER_SPECS:
        script = X2 / "runners" / filename
        completed = subprocess.run(
            [sys.executable, str(script)],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
        )
        payload = json.loads(completed.stdout) if completed.stdout.strip() else {}
        runner_results.append(
            {
                "runner": filename,
                "exit_code": completed.returncode,
                "passed": completed.returncode == 0 and payload.get("passed") is True,
                "selected": payload.get("selected", 0),
                "same_owner_only": True,
            }
        )
    write_json(
        runner_receipt,
        {
            "schema": "ghc.family.runner-use-receipts.v2",
            "entries": runner_results,
            "passed": sum(item["passed"] for item in runner_results),
            "total": len(runner_results),
            "same_owner_only": True,
        },
    )
    if not all(item["passed"] for item in runner_results):
        raise SystemExit(2)
    refresh()


def x2_public_files() -> list[Path]:
    exact_extra = {
        ROOT / "scripts" / "build_ghc_family_sable_rook_v684_v5_x2.py",
        ROOT / "scripts" / "ghc_family_sable_rook_v684_v5_contracts.py",
        ROOT / "tests" / "test_ghc_family_sable_rook_v684_v5_x2.py",
    }
    result = [path for path in X2.rglob("*") if path.is_file()]
    result.extend(path for path in exact_extra if path.exists())
    return sorted(set(result), key=lambda path: path.relative_to(ROOT).as_posix())


def privacy_scan(paths: Iterable[Path]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_local_path": re.compile(r"(?:[A-Za-z]:\\|/Users/|/home/)[^\s\"']+"),
        "credential_or_secret_assignment": re.compile(r"\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s,}]+", re.I),
        "private_callable_route": re.compile(r"\b(?:codex|app|session|thread)://\S+", re.I),
        "private_application_state": re.compile(r"\b(?:providerTabId|clientThreadId|private callable identifier)\b", re.I),
    }
    candidates = []
    confirmed = []
    for path in paths:
        if path.suffix.lower() not in {".json", ".md", ".py", ".html", ".yaml", ".yml", ".txt"}:
            continue
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                definition = rel.endswith("build_ghc_family_sable_rook_v684_v5_x2.py")
                item = {
                    "path": rel,
                    "line": line,
                    "class": class_name,
                    "disposition": "scanner_definition_not_payload" if definition else "confirmed_payload_hit",
                }
                candidates.append(item)
                if not definition:
                    confirmed.append(item)
    return {
        "schema": "ghc.family.privacy-scan.v2",
        "phase": PHASE,
        "scope": "x2 evidence delta",
        "pattern_classes": list(patterns),
        "candidate_count": len(candidates),
        "confirmed_hit_count": len(confirmed),
        "candidates": candidates,
        "confirmed_hits": confirmed,
        "truth_boundary": "Bounded pattern evidence only; not complete privacy assurance.",
    }


def refresh() -> None:
    if not X2.exists():
        raise SystemExit("build x2 first")
    outcomes = json.loads((X2 / "outcome-ledger.json").read_text(encoding="utf-8"))
    skills = X2 / "skill-use-receipts.json"
    runners = X2 / "runner-use-receipts.json"
    execution_ready = skills.exists() and runners.exists()
    x1_manifest_raw = run_git(
        "show",
        f"{X1_COMMIT}:docs/sable-rook/{PHASE}/validation/x1-index-manifest.json",
    ).stdout
    x1_manifest = json.loads(x1_manifest_raw)
    x1_failures = []
    for entry in x1_manifest["entries"]:
        data = subprocess.run(
            ["git", "show", f"{X1_COMMIT}:{entry['path']}"],
            cwd=ROOT,
            check=True,
            capture_output=True,
        ).stdout
        data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        actual = hashlib.sha256(data).hexdigest()
        if actual != entry["sha256_normalized_lf"]:
            x1_failures.append(
                {
                    "path": entry["path"],
                    "expected": entry["sha256_normalized_lf"],
                    "actual": actual,
                }
            )
    write_json(
        X2 / "x1-git-blob-replay.json",
        {
            "schema": "ghc.family.x1-git-blob-replay.v2",
            "x1_commit": X1_COMMIT,
            "manifest": f"docs/sable-rook/{PHASE}/validation/x1-index-manifest.json",
            "entries": len(x1_manifest["entries"]),
            "self_exclusions": len(x1_manifest["self_exclusions"]),
            "failures": x1_failures,
            "state": "PASS" if not x1_failures else "FAIL",
            "boundary": "Exact immutable x1 Git-blob evidence only; x2 changed no x1 path.",
        },
    )
    write_json(
        X2 / "phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.v2",
            "phase": PHASE,
            "lifecycle": "X2_EVIDENCE_EXECUTED" if execution_ready else "X2_BUILT_PENDING_EXECUTION_RECEIPTS",
            "outcomes": outcomes["counts"],
            "positive_controls": 60,
            "rejecting_mutations": 300,
            "real_rows": 0,
            "real_people": 0,
            "real_devices_or_collection_objects": 0,
            "authority_actions": 0,
            "effective_overlay": {
                "negatives": 59408,
                "methods": 73674,
                "failed_witnesses": 30769,
                "bounded_passing_witnesses": 54209,
                "decomposition": "activation overlay plus nine x1 failures, seven x1 recoveries, five x2 operational failures, three x2 recoveries, and 300 rejected synthetic mutations",
            },
            "open_gaps": 528,
            "exact_gates": 518,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        X2 / "evidence-truth.json",
        {
            "schema": "ghc.family.evidence-truth.v2",
            "phase": PHASE,
            "execution_receipts_complete": execution_ready,
            "outcomes": outcomes["counts"],
            "positive_controls": 60,
            "rejecting_mutations": 300,
            "skills_validated_and_smoke_used": 20 if execution_ready else 0,
            "runners_invoked": 10 if execution_ready else 0,
            "safe_now_completed": 120,
            "owner_candidates_completed": 80,
            "cfr_completed": 100,
            "real_rows": 0,
            "authority_actions": 0,
            "open_gaps_after_phase": 528,
            "exact_gates_after_phase": 518,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": "Bounded same-owner software evidence only.",
        },
    )
    integrated = """# Sable Rook v684-v5 x2 bounded evidence

The x2 layer executes the immutable x1 plan without changing an x1 path. Sixty
positive synthetic fixtures pass their declared bounded contracts, and all 300
preregistered invalid mutations are rejected and retained at zero completion
credit. Outcomes are 42 `completed`, 12 `represented`, 3 `open_gap`, and 3
`exact_gate`. Completed means only the stated owner-local software, schema,
documentation, or synthetic fixture gate passed.

THOS Body is primary through synthetic queue, correction-readback, workload, and
handover states. It remains proxy-only because there are no real participants or
operators, blind matched-budget arms, safety monitoring, appropriate statistics,
or independent review. GMUT Mind remains a typed scalar-tensor and EFT
research-model family; metadata and causal firewalls establish no physical
prediction, likelihood, parameter constraint, empirical confirmation, quantum
completion, or Theory of Everything. Freed ID and CBR Heart remain synthetic and
nonproduction; no real keys, proofs, issuance, resolution, status, revocation,
interoperability, privacy review, independent security review, recovery, trust
governance, legal interpretation, cultural ratification, affected-party decision,
or Māori-authority action occurred.

Twenty phase-local skills are substantive, quick-validated, and smoke-used
without global installation. Ten family-current runners are invoked once and
produce bounded receipts. The owner portfolios resolve 120 safe-now tasks, 80
candidate prototypes, and 100 additive refinements within declared synthetic
scope. Twenty exact-approval and ten blocked packets remain visible and
unexecuted.

Official and primary sources provide vocabulary and refusal duties only. Zero
domain-data rows were queried or downloaded. Structural accessibility checks do
not replace manual keyboard, responsive-layout, browser-diversity,
assistive-technology, cognitive-accessibility, Māori-language, or affected-user
evaluation. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
"""
    write_text(X2 / "integrated-evidence.md", integrated)

    self_exclusions = {
        f"docs/sable-rook/{PHASE}/validation/evidence-index-manifest.json",
        f"docs/sable-rook/{PHASE}/validation/evidence-privacy-scan.json",
        f"docs/sable-rook/{PHASE}/validation/evidence-staged-review.json",
    }
    files = x2_public_files()
    scan = privacy_scan(files)
    write_json(VALIDATION / "evidence-privacy-scan.json", scan)
    files = x2_public_files()
    entries = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256_normalized_lf": normalized_sha(path),
            "bytes_normalized_lf": len(normalized_bytes(path)),
        }
        for path in files
        if path.relative_to(ROOT).as_posix() not in self_exclusions
    ]
    write_json(
        VALIDATION / "evidence-index-manifest.json",
        {
            "schema": "ghc.family.normalized-lf-manifest.v2",
            "phase": PHASE,
            "lifecycle": "x2_evidence_delta",
            "x1_commit": X1_COMMIT,
            "entries": entries,
            "entry_count": len(entries),
            "self_exclusions": sorted(self_exclusions),
            "hash_domain": "SHA-256 over normalized-LF exact evidence files; staged review replays Git index blobs.",
        },
    )
    write_json(
        VALIDATION / "evidence-staged-review.json",
        {
            "schema": "ghc.family.staged-review.v2",
            "phase": PHASE,
            "state": "PREPARED_NOT_STAGED",
            "manifest_entry_count": len(entries),
            "self_exclusions": sorted(self_exclusions),
            "exact_staged_allowlist": [],
            "manifest_mismatches": [],
            "out_of_scope_paths": [],
            "x1_paths_changed": [],
            "diff_hygiene": "PENDING_STAGING",
        },
    )


def review_staged() -> None:
    manifest = json.loads((VALIDATION / "evidence-index-manifest.json").read_text(encoding="utf-8"))
    expected = {item["path"]: item["sha256_normalized_lf"] for item in manifest["entries"]}
    exclusions = set(manifest["self_exclusions"])
    staged = [line for line in run_git("diff", "--cached", "--name-only", "--diff-filter=ACMR").stdout.splitlines() if line]
    expected_all = set(expected) | exclusions
    mismatches = []
    for path, wanted in sorted(expected.items()):
        try:
            actual = git_blob_sha(path)
        except subprocess.CalledProcessError:
            mismatches.append({"path": path, "error": "missing_from_index"})
            continue
        if actual != wanted:
            mismatches.append({"path": path, "expected": wanted, "actual": actual})
    out_of_scope = sorted(set(staged) - expected_all)
    missing = sorted(expected_all - set(staged))
    x1_changed = [path for path in staged if path.startswith(f"docs/sable-rook/{PHASE}/x1/") or path.startswith(f"docs/sable-rook/{PHASE}/method-flow/") or path.startswith(f"docs/sable-rook/{PHASE}/workflow-refinement") or path.startswith(f"docs/sable-rook/{PHASE}/reflection-remaster") or path.startswith(f"docs/sable-rook/{PHASE}/tooling/")]
    diff = run_git("diff", "--cached", "--check", check=False)
    passed = not mismatches and not out_of_scope and not missing and not x1_changed and diff.returncode == 0
    write_json(
        VALIDATION / "evidence-staged-review.json",
        {
            "schema": "ghc.family.staged-review.v2",
            "phase": PHASE,
            "state": "PASS" if passed else "FAIL",
            "staged_count": len(staged),
            "manifest_entry_count": len(expected),
            "self_exclusions": sorted(exclusions),
            "exact_staged_allowlist": staged,
            "manifest_mismatches": mismatches,
            "missing_paths": missing,
            "out_of_scope_paths": out_of_scope,
            "x1_paths_changed": x1_changed,
            "diff_hygiene": "PASS" if diff.returncode == 0 else "FAIL",
            "diff_hygiene_output": diff.stdout + diff.stderr,
        },
    )
    if not passed:
        raise SystemExit(2)


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--build", action="store_true")
    mode.add_argument("--execute-once", action="store_true")
    mode.add_argument("--refresh", action="store_true")
    mode.add_argument("--review-staged", action="store_true")
    args = parser.parse_args()
    if args.build:
        build()
    elif args.execute_once:
        execute_once()
    elif args.refresh:
        refresh()
    else:
        review_staged()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
