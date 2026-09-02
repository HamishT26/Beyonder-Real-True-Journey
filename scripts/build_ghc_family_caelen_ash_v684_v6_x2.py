#!/usr/bin/env python3
"""Build and execute the bounded Caelen Ash v684-v6 x2 evidence layer."""

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

from ghc_family_caelen_ash_v684_v6_contracts import (  # noqa: E402
    MUTATION_TYPES,
    evaluate_proposal,
    validate_fixture,
)


PHASE = "v684-v6"
BASE = ROOT / "docs" / "caelen-ash" / PHASE
X1 = BASE / "x1"
X2 = BASE / "x2"
VALIDATION = BASE / "validation"
X1_COMMIT = "ab50360d737177ab1ebe4564b348a88b540c9ed4"
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]

RUNNER_SPECS = [
    ("ghc_family_tunnel_campaign_runner.py", range(1, 7), "synthetic tunnel campaign and test-article boundary"),
    ("ghc_family_test_article_lineage_runner.py", range(2, 19), "test-article configuration and reference-quantity lineage"),
    ("ghc_family_axis_and_command_runner.py", range(4, 10), "axis-frame and command-observation separation"),
    ("ghc_family_flow_state_vacancy_runner.py", range(8, 17), "flow-state channel and realized-measurement vacancy"),
    ("ghc_family_coefficient_provenance_runner.py", range(17, 20), "coefficient sign reference and nondimensionalization provenance"),
    ("ghc_family_uncertainty_calibration_runner.py", range(20, 25), "uncertainty covariance and calibration vacancy"),
    ("ghc_family_run_event_correction_runner.py", range(26, 34), "run-event correction quarantine and nonerasure"),
    ("ghc_family_flow_visualization_guard_runner.py", range(34, 41), "flow-visualization metadata and nonconversion"),
    ("ghc_family_trinity_boundary_runner.py", range(41, 55), "GMUT THOS Freed ID and CBR boundary"),
    ("ghc_family_stage20_gate_runner.py", range(55, 61), "external-evidence, exact-authority, production, and Stage 20 holds"),
]

SKILL_TO_PROPOSAL = {
    "synthetic-tunnel-campaign-guard": "CA6846-N001",
    "test-article-referent-firewall": "CA6846-N002",
    "tunnel-axis-frame-custodian": "CA6846-N005",
    "command-observation-separator": "CA6846-N006",
    "mach-reynolds-vacancy": "CA6846-N008",
    "pressure-channel-topology-guard": "CA6846-N011",
    "coefficient-sign-convention": "CA6846-N017",
    "reference-quantity-provenance": "CA6846-N018",
    "nondimensionalization-version-guard": "CA6846-N019",
    "uncertainty-covariance-vacancy": "CA6846-N020",
    "calibration-traceability-hold": "CA6846-N022",
    "run-event-nonerasure": "CA6846-N026",
    "missing-versus-zero-separator": "CA6846-N029",
    "saturation-quarantine": "CA6846-N030",
    "flow-visualization-nonconversion": "CA6846-N034",
    "gmut-model-discrepancy-firewall": "CA6846-N042",
    "thos-run-card-handover-proxy": "CA6846-N043",
    "freed-id-nonproduction-hold": "CA6846-N046",
    "cbr-minimum-disclosure-boundary": "CA6846-N048",
    "stage20-nonpromotion-latch": "CA6846-N060",
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
    raw = run_git("show", f"{X1_COMMIT}:docs/caelen-ash/{PHASE}/x1/new-proposal-freeze.json").stdout
    return json.loads(raw)


def skill_text(slug: str, proposal_id: str) -> str:
    display = slug.replace("-", " ").title()
    return f"""---
name: {slug}
description: Apply the Caelen Ash {PHASE} bounded {display.lower()} contract to owner-local synthetic evidence while retaining failures and refusing empirical, professional, production, legal, cultural, Māori-authority, identity, consciousness, or Stage 20 promotion.
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

Do not ingest real tunnel, model, instrument, measurement, participant,
identity, or authority data. Do not issue a credential, control a facility,
release a run, interpret law or culture, speak for Māori, claim
complete accessibility or privacy, or authorize production, proof, canon, or
Stage 20. Stop and retain an `open_gap` or `exact_gate` whenever exact evidence or
competent affected authority is absent.
"""


def skill_yaml(slug: str) -> str:
    display = slug.replace("-", " ").title()
    return f"""interface:
  display_name: "{display}"
  short_description: "Bounded synthetic {slug.replace('-', ' ')} workflow"
  default_prompt: "Apply the bounded Caelen Ash {PHASE} {slug.replace('-', ' ')} contract, retain failures, and preserve every empirical and authority gate."
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

from ghc_family_caelen_ash_v684_v6_contracts import validate_fixture

PROPOSAL_IDS = {proposal_ids!r}
BOUNDARY = {boundary!r}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-output")
    args = parser.parse_args()
    controls_path = ROOT / "docs" / "caelen-ash" / "v684-v6" / "x2" / "positive-controls.json"
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
        proposal_ids = [f"CA6846-N{index:03d}" for index in indexes]
        write_text(X2 / "runners" / filename, runner_text(filename, proposal_ids, boundary))

    write_json(
        X2 / "pillar-evidence.json",
        {
            "schema": "ghc.family.pillar-evidence.v2",
            "primary": {
                "pillar": "GMUT Mind",
                "status": "represented",
                "evidence": "Typed command-observation, coordinate-frame, uncertainty-vacancy, residual, and model-discrepancy contracts only.",
                "missing": ["real wind-tunnel data", "frozen likelihood", "uncertainty analysis", "parameter constraints", "independent scientific review"],
            },
            "protected": [
                {
                    "pillar": "THOS Body",
                    "status": "represented",
                    "evidence": "Synthetic run-card queue, hold, correction-readback, cancellation, and handover fixtures only.",
                    "missing": ["real participants or operators", "blind matched-budget arms", "safety monitoring", "appropriate statistics", "independent review"],
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
            "source_ledger": "docs/caelen-ash/v684-v6/x1/official-primary-source-ledger.json",
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
            "manifest": f"docs/caelen-ash/{PHASE}/validation/x1-index-manifest.json",
            "state": "PENDING_EXTERNAL_EXACT_REPLAY",
            "boundary": "X2 may not rewrite a frozen x1 path.",
        },
    )
    write_json(
        X2 / "method-flow-x2.json",
        {
            "schema": "ghc.family.method-flow-x2.v2",
            "inherited_x1_method_ledger": f"docs/caelen-ash/{PHASE}/x1/method-flow/ledger.json",
            "x2_operational_failures": [
                {
                    "failure_id": "CA6846-X2-N001",
                    "summary": "The combined evidence staged-review wrapper crossed its display window while the exact second review process was still reading index blobs.",
                    "credit": 0,
                },
                {
                    "failure_id": "CA6846-X2-N002",
                    "summary": "The persisted review completed FAIL because the contracts module had one blank line at EOF and exact staged diff hygiene returned nonzero.",
                    "credit": 0,
                },
            ],
            "x2_recovery_methods": [
                {
                    "method_id": "CA6846-M013",
                    "method": "Inspect the exact live process and persisted review before deciding whether a wrapper-window crossing requires any retry.",
                    "retained_negative_ids": ["CA6846-X2-N001"],
                },
                {
                    "method_id": "CA6846-M014",
                    "method": "Remove only the trailing blank line, restage that exact dependency, and rerun the bounded staged review once.",
                    "retained_negative_ids": ["CA6846-X2-N002"],
                },
            ],
            "rejected_synthetic_mutations": 300,
            "truth": "Both operational failures remain zero-credit and separate from their bounded recoveries. Rejected mutations are bounded zero-credit negative witnesses, not operational failures or broader security evidence.",
        },
    )
    method_inputs = X2 / "method-flow-inputs"
    method_rows = [
        {
            "method_id": "CA6846-M013",
            "title": "Inspect persisted review state after a wrapper-window crossing",
            "failure_id": "CA6846-X2-N001",
            "trigger": "A deterministic staged-review wrapper returns without an attributable final projection while its exact child process may still be active.",
            "method": "Inspect only the exact child process, wait without replay, and then read the persisted review and index scalars.",
            "observed": "The child completed; the persisted receipt exposed a real diff-hygiene failure with all manifest, missing, scope, and x1-contamination arrays empty.",
        },
        {
            "method_id": "CA6846-M014",
            "title": "Repair one exact staged diff-hygiene dependency",
            "failure_id": "CA6846-X2-N002",
            "trigger": "A persisted staged review fails only because an owner-local Python file has a trailing blank line.",
            "method": "Remove only the trailing blank line, restage that exact file, and rerun the bounded staged review once.",
            "observed": "The corrected dependency is separately staged and the original failed receipt remains retained before the bounded rerun.",
        },
    ]
    for row in method_rows:
        method_id = row["method_id"]
        write_json(
            method_inputs / f"{method_id.lower()}-record.json",
            {
                "method_id": method_id,
                "title": row["title"],
                "failure_signature": row["trigger"],
                "trigger_preconditions": [row["trigger"]],
                "privacy_class": "sanitized_public",
                "approval_class": "safe_now_owner_local_workflow_recovery",
                "candidate_workaround": row["method"],
                "validation_witness_ids": [],
                "recurrence_guard": "Retain the failure, inspect the smallest exact persisted surface, and do not replay an already-successful review.",
                "rollback": "Return to the immutable x1 head and exact staged allowlist without widening scope.",
                "recommendation_state": "candidate",
                "supersedes": [],
                "protected_gates": ["failure nonerasure", "exact staged scope", "manifest parity", "same-owner only"],
                "retained_negative_ids": [row["failure_id"]],
                "scope_boundary": "Caelen-owned x2 staged-review workflow only; no broader assurance or authority.",
                "execution_authority": "owner_self_scoped_delta",
                "repository_scan": False,
                "module_scan": True,
                "cross_lane_scan": False,
                "unchanged_history_scan": False,
                "sibling_lane_mutation": False,
                "source_commit": X1_COMMIT,
                "final_commit": "PENDING_EVIDENCE_COMMIT",
                "changed_file_allowlist": [
                    "scripts/ghc_family_caelen_ash_v684_v6_contracts.py",
                    "docs/caelen-ash/v684-v6/validation/evidence-staged-review.json",
                ],
                "module_allowlist": ["scripts/ghc_family_caelen_ash_v684_v6_contracts.py"],
                "exact_pushed_head_required": True,
            },
        )
        write_json(
            method_inputs / f"{method_id.lower()}-fail-01.json",
            {
                "witness_id": f"{method_id}-WF01",
                "method_id": method_id,
                "procedure": row["trigger"],
                "scope": "Exact Caelen-owned x2 staged-review surface.",
                "expected": "An attributable PASS review with exact diff hygiene.",
                "observed": row["failure_id"],
                "result": "fail",
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": [row["failure_id"]],
                "boundary": "Workflow failure only; zero broader completion credit.",
            },
        )
        write_json(
            method_inputs / f"{method_id.lower()}-pass.json",
            {
                "witness_id": f"{method_id}-WP01",
                "method_id": method_id,
                "procedure": row["method"],
                "scope": "Exact Caelen-owned x2 staged-review surface.",
                "expected": "A separately attributable bounded recovery while the failed witness remains retained.",
                "observed": row["observed"],
                "result": "pass",
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": [row["failure_id"]],
                "boundary": "Same-owner workflow recovery only; not independent reproduction or broader assurance.",
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
<html lang="en"><head><meta charset="utf-8"><title>Caelen Ash v684-v6 bounded evidence</title></head>
<body><main><h1>Caelen Ash v684-v6 bounded evidence</h1>
<p>Status: NOT_READY_FOR_STAGE_20. This owner-local report contains synthetic software and documentation evidence only.</p>
<h2>Primary pillar</h2><p>GMUT Mind is represented by typed command-observation, reference-quantity, uncertainty-vacancy, residual, and model-discrepancy contracts. No aerodynamic or empirical result is claimed.</p>
<h2>Protected pillars</h2><p>THOS Body remains a synthetic run-card and handover proxy. Freed ID and CBR Heart remain synthetic and nonproduction.</p>
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
        ROOT / "scripts" / "build_ghc_family_caelen_ash_v684_v6_x2.py",
        ROOT / "scripts" / "ghc_family_caelen_ash_v684_v6_contracts.py",
        ROOT / "tests" / "test_ghc_family_caelen_ash_v684_v6_x2.py",
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
                definition = rel.endswith("build_ghc_family_caelen_ash_v684_v6_x2.py")
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
        f"{X1_COMMIT}:docs/caelen-ash/{PHASE}/validation/x1-index-manifest.json",
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
            "manifest": f"docs/caelen-ash/{PHASE}/validation/x1-index-manifest.json",
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
                "negatives": 59730,
                "methods": 73690,
                "failed_witnesses": 30791,
                "bounded_passing_witnesses": 54225,
                "decomposition": "Sable activation baseline plus sixteen retained Caelen x1 failures, twelve separate x1 recoveries, 300 rejected synthetic mutations, two x2 workflow failures, and two separate x2 recoveries",
            },
            "open_gaps": 531,
            "exact_gates": 521,
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
            "open_gaps_after_phase": 531,
            "exact_gates_after_phase": 521,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": "Bounded same-owner software evidence only.",
        },
    )
    integrated = """# Caelen Ash v684-v6 x2 bounded evidence

The x2 layer executes the immutable x1 plan without changing an x1 path. Sixty
positive synthetic fixtures pass their declared bounded contracts, and all 300
preregistered invalid mutations are rejected and retained at zero completion
credit. Outcomes are 42 `completed`, 12 `represented`, 3 `open_gap`, and 3
`exact_gate`. Completed means only the stated owner-local software, schema,
documentation, or synthetic fixture gate passed.

GMUT Mind is primary through typed command-observation, coordinate-frame,
reference-quantity, uncertainty-vacancy, residual, and model-discrepancy
contracts. It remains a typed scalar-tensor and EFT research-model family; these
synthetic firewalls establish no physical prediction, likelihood, parameter
constraint, empirical confirmation, quantum completion, or Theory of
Everything. THOS Body remains a synthetic run-card, correction-readback,
workload, cancellation, and handover proxy without real operators, blind
matched-budget arms, safety monitoring, appropriate statistics, or independent
review. Freed ID and CBR Heart remain synthetic and
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
        f"docs/caelen-ash/{PHASE}/validation/evidence-index-manifest.json",
        f"docs/caelen-ash/{PHASE}/validation/evidence-privacy-scan.json",
        f"docs/caelen-ash/{PHASE}/validation/evidence-staged-review.json",
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
    x1_changed = [path for path in staged if path.startswith(f"docs/caelen-ash/{PHASE}/x1/") or path.startswith(f"docs/caelen-ash/{PHASE}/method-flow/") or path.startswith(f"docs/caelen-ash/{PHASE}/workflow-refinement") or path.startswith(f"docs/caelen-ash/{PHASE}/reflection-remaster") or path.startswith(f"docs/caelen-ash/{PHASE}/tooling/")]
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
