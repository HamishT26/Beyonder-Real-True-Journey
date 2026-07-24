#!/usr/bin/env python3
"""Build the frozen Caelen Ash v653-v6 x2 evidence packet."""

from __future__ import annotations

import html
import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

import build_ghc_family_v653_v2_evidence as base
import ghc_family_v653_v6_core as core
import ghc_family_v653_v6_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
X1_COMMIT = "5be148f1171a449550ce73dd524cb866db7632e3"
X2_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6536-X2-N01",
        "category": "inherited_evidence_summary_omitted_external_negative",
        "failed": (
            "The first evidence build emitted an inherited intermediate summary "
            "that omitted the separate post-seal route-preflight negative and "
            "therefore understated the activation total by one; that summary "
            "received zero reporting credit."
        ),
        "recovery": (
            "Retain the reporting defect, suppress the inherited intermediate "
            "summary, keep Sable's 10,110 repository count unchanged, and emit "
            "only the corrected activation-baseline total from durable receipts."
        ),
        "recurrence_guard": (
            "Require every v653-v6 aggregate to distinguish sealed repository "
            "negatives from external post-seal negatives before it is emitted."
        ),
    },
    {
        "negative_id": "V6536-X2-N02",
        "category": "windows_stale_label_glob_and_frozen_history_false_signal",
        "failed": (
            "The first stale-label scan passed Unix-style wildcard path "
            "arguments to the Windows search tool and also surfaced an inherited "
            "frozen-chain LAMOST title that must remain immutable; the aggregate "
            "received zero stale-label review credit."
        ),
        "recovery": (
            "Use repository-root include and exclude patterns, preserve the "
            "frozen prior-proposal segment byte-for-byte, and scan only current "
            "v653-v6 code plus nonhistorical generated surfaces."
        ),
        "recurrence_guard": (
            "On Windows, never rely on shell-expanded wildcard path arguments "
            "and never classify immutable frozen-chain vocabulary as a current "
            "stale-label defect."
        ),
    },
    {
        "negative_id": "V6536-X2-N03",
        "category": "stale_label_scan_matched_retained_failure_vocabulary",
        "failed": (
            "The path-corrected stale-label scan still classified the retained "
            "failure's own LAMOST wording as a current product label and "
            "therefore received zero semantic stale-label credit."
        ),
        "recovery": (
            "Scan structured current proposal, source, workflow, and route "
            "objects plus nonhistorical non-Method-Flow artifacts while "
            "preserving frozen history and retained-negative prose."
        ),
        "recurrence_guard": (
            "A stale-label gate must distinguish product vocabulary from the "
            "immutable description of a failure that mentions the retired label."
        ),
    }
]

SURFACE_MAP = {
    "av-carrier-risk": "iasa-tc05-carrier-risk-board",
    "audio-signal-chain": "iasa-tc04-audio-signal-chain",
    "loudness-algorithm": "itu-bs1770-algorithm-board",
    "pbcore-metadata": "pbcore21-av-metadata-profile",
    "av-container-profile": "fadgi-rdd48-mxf-profile",
    "video-significant-properties": "fadgi-video-significant-properties",
    "operator-algebra-typing": "haagerup-standard-form-ledger",
    "modular-localization": "bgl-modular-localization",
    "identity-status-watch": "oauth21-draft-consolidation-watch",
    "av-cultural-authority": "av-cultural-authority-rail",
}

base.d = d
base.core = core
base.ROOT = ROOT
base.X1_COMMIT = X1_COMMIT
base.X2_NEGATIVES = X2_NEGATIVES


def skill_markdown(
    name: str,
    purpose: str,
    runner: str,
    surface: str,
) -> str:
    return f"""---
name: {name}
description: {purpose} Use when reviewing the corresponding Caelen v653-v6 contract, mutation evidence, nonpromotion boundary, or lifecycle receipt.
---

# {name}

## Purpose

{purpose} Keep the review within the declared same-owner symbolic, structural,
synthetic, proxy, zero-row, or exact-reservation lane.

## Workflow

1. Read `references/contract.json` completely.
2. Resolve only the repository-relative artifacts declared there.
3. Run `python scripts/{runner}` from the repository root.
4. Require `valid` to be true and `terminal_verdict` to remain
   `NOT_READY_FOR_STAGE_20`.
5. If the runner fails, retain the failed attempt with zero credit before a
   bounded correction.
6. Report only `completed`, `represented`, `open_gap`, or `exact_gate`.

## Boundaries

- Surface: `{surface}`.
- Use owner-local synthetic or structural fixtures only.
- Never introduce credentials, private routes, nonpublic conversations, real
  participant data, production keys, legal conclusions, professional
  certification, cultural ratification, or Māori-authority decisions.
- A passing smoke use is same-owner workflow evidence only. It is not
  empirical confirmation, production readiness, complete privacy or
  accessibility, exhaustive security, independent reproduction, consciousness
  or personhood, Theory-of-Everything proof, or Stage 20 authority.
"""


def wrapper_source(surface: str) -> str:
    target = SURFACE_MAP.get(surface, surface)
    if target == "phase-validation":
        body = """rows = [runner_payload(row["slug"]) for row in proposals()]
    payload = {
        "surface": "phase-validation",
        "proposal_count": len(rows),
        "valid": all(row["valid"] for row in rows),
        "mutation_count": sum(row["mutation_count"] for row in rows),
        "rejected": sum(row["rejected"] for row in rows),
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }"""
    else:
        body = f'payload = runner_payload("{target}")'
    return f"""#!/usr/bin/env python3
from __future__ import annotations

import json

from ghc_family_v653_v6_core import proposals, runner_payload


def main() -> None:
    {body}
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    if not payload["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
"""


def build_report(outcomes: dict[str, int], effective_negatives: int) -> str:
    effective_negatives += d.EXTERNAL_POST_SEAL_NEGATIVES
    cards = []
    for proposal in d.PROPOSALS:
        cards.append(
            "<article><h3>{}</h3><p>{}</p><dl>"
            "<dt>Outcome</dt><dd>{}</dd>"
            "<dt>Lane</dt><dd>{}</dd>"
            "<dt>Boundary</dt><dd>{}</dd></dl></article>".format(
                html.escape(proposal["proposal_id"]),
                html.escape(proposal["title"]),
                html.escape(proposal["expected_disposition"]),
                html.escape(proposal["execution_lane"]),
                html.escape(proposal["falsifier_or_acceptance_gate"]),
            )
        )
    return f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Caelen Ash v653-v6 bounded evidence report</title><style>
body{{font:1rem/1.6 system-ui,sans-serif;max-width:78rem;margin:auto;padding:1.5rem;color:#17212b;background:#fbfcfd}}
:focus{{outline:3px solid #9b4d00;outline-offset:3px}}
article{{border:1px solid #8091a3;border-radius:.6rem;padding:1rem;margin:1rem 0;background:white}}
dt{{font-weight:700}}dd{{margin:0 0 .6rem}}
.notice{{border-left:.5rem solid #8b3d00;padding:1rem;background:#fff4e5}}
@media(prefers-reduced-motion:reduce){{*{{scroll-behavior:auto!important;animation:none!important}}}}
</style></head><body><main>
<h1>Caelen Ash v653-v6 bounded evidence report</h1>
<p class="notice"><strong>Boundary:</strong> Same-owner synthetic and
structural evidence only. Manual and affected-user accessibility evaluation is
reserved. No empirical confirmation, production readiness, professional
approval, legal or cultural authority, Māori authority, independent
reproduction, Theory-of-Everything proof, or Stage 20 authority is claimed.</p>
<h2>Truth summary</h2><p>Outcomes: {html.escape(str(outcomes))}. Effective
retained negatives: {effective_negatives}. Terminal verdict:
NOT_READY_FOR_STAGE_20.</p>
<h2>Proposal evidence</h2>{''.join(cards)}
<h2>External incompleteness</h2><p>Real data, blind matched-budget arms,
independent review, production identity infrastructure, affected-party
participation, professional, legal, cultural and Māori authority, qualified
manual accessibility review, and independent-team reproduction remain open or
exact-gated.</p>
</main></body></html>"""


def _postprocess_generated_files() -> None:
    replacements = [
        ("v653-gmut-thos-v2-x1-x2", "v653-gmut-thos-v6-x1-x2"),
        ("ghc.family.v653-v2", "ghc.family.v653-v6"),
        ("V6532-METHOD-", "V6536-METHOD-"),
        ("V6532-WITNESS-", "V6536-WITNESS-"),
        ("MÄori", "Māori"),
        ("hapÅ«", "hapū"),
        ("â€”", "—"),
    ]
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        updated = text
        for old, new in replacements:
            updated = updated.replace(old, new)
        if updated != text:
            path.write_text(updated, encoding="utf-8", newline="\n")

    base.write_json(
        "retained-negative-register-x2.json",
        {
            "schema": "ghc.family.v653-v6.retained-negatives.v1",
            "inherited_count": d.INHERITED_NEGATIVES,
            "inherited_anchor": d.SOURCE_HEAD,
            "inherited_register": (
                "Sable Rook v653-v5 sealed phase truth at 10,110 repository "
                "negatives; no inherited negative is rewritten."
            ),
            "external_post_seal_count": d.EXTERNAL_POST_SEAL_NEGATIVES,
            "external_post_seal": [
                {
                    "negative_id": "V6535-POST-N01",
                    "category": "task_registry_advertised_query_argument_rejected",
                    "credit": "retained_negative",
                    "boundary": (
                        "External read-only route-preflight evidence only; it "
                        "does not alter Sable's sealed repository count."
                    ),
                }
            ],
            "activation_negative_baseline": d.ACTIVATION_NEGATIVE_BASELINE,
            "x1_operational_count": len(d.X1_NEGATIVES),
            "x1_operational_ids": [row[0] for row in d.X1_NEGATIVES],
            "x2_operational_count": len(X2_NEGATIVES),
            "x2_operational": X2_NEGATIVES,
            "synthetic_mutation_count": len(d.PROPOSALS)
            * len(d.MUTATION_KINDS),
            "synthetic_mutations": [
                {
                    "negative_id": result["mutation_id"],
                    "proposal_id": proposal["proposal_id"],
                    "category": result["kind"],
                    "observed": result["observed"],
                    "credit": "retained_negative",
                }
                for proposal in d.PROPOSALS
                for result in core.evaluate_surface(proposal["slug"])[
                    "mutation_results"
                ]
            ],
            "effective_total": (
                d.ACTIVATION_NEGATIVE_BASELINE
                + len(d.X1_NEGATIVES)
                + len(X2_NEGATIVES)
                + len(d.PROPOSALS) * len(d.MUTATION_KINDS)
            ),
            "none_erased": True,
        },
    )
    base.write_json(
        "exact-open-gate-register-x2.json",
        {
            "schema": "ghc.family.v653-v6.gates.v1",
            "inherited_open_gaps": d.INHERITED_OPEN_GAPS,
            "new_open_gaps": [
                {
                    "proposal_id": "V6536-P29",
                    "gate": (
                        "released Gaia DR4 tables and schema, real rows, "
                        "release-specific quality and calibration fields, "
                        "selection, nuisance and uncertainty treatment, a frozen "
                        "likelihood, and appropriate independent review"
                    ),
                }
            ],
            "effective_open_gaps": d.INHERITED_OPEN_GAPS + 1,
            "inherited_exact_gates": d.INHERITED_EXACT_GATES,
            "new_exact_gates": [
                {
                    "proposal_id": "V6536-P30",
                    "gate": (
                        "recording-specific description, access, playback, "
                        "transfer, digitization, sacred or restricted content, "
                        "notice, takedown, return or repatriation, taonga and "
                        "mātauranga wording, beneficiary privacy, remedy, "
                        "affected-party review, iwi, hapū, and Māori authority"
                    ),
                }
            ],
            "effective_exact_gates": d.INHERITED_EXACT_GATES + 1,
            "none_silently_closed": True,
        },
    )
    base.write_json(
        "complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v653-v6.checklist.v1",
            "complete_bounded": [
                "thirty frozen proposals executed",
                "150 frozen mutations rejected and retained",
                "ten phase-local skills initialized, customized, quick-validated, and smoke-used",
                "ten family-compatible runners built and invoked",
                "safe, candidate, and cleanup portfolios resolved within bounded lanes",
                "accessible static report generated with manual evaluation reserved",
            ],
            "pending_lifecycle": [
                "evidence commit",
                "combined closeout, seal, and final commit",
                "one exact-final canonical pass",
            ],
            "incomplete_external": [
                "released Gaia DR4 data, real empirical GMUT data, and likelihood",
                "blind matched-budget THOS arms and independent review",
                "production Freed ID keys, proofs, issuance, resolution, status, revocation, interoperability, recovery, privacy and security review, and governance",
                "affected-party, professional, legal, cultural, iwi, hapū, and Māori authority",
                "qualified manual and affected-user accessibility evaluation",
                "independent-team reproduction and Stage 20 authority",
            ],
            "route_state": "NOT_ELIGIBLE_EVIDENCE_NOT_FINAL",
        },
    )
    truth = base.read_json(ROOT / "phase-truth.json")
    truth.update(
        {
            "schema": "ghc.family.v653-v6.phase-truth.v1",
            "source_commit": d.SOURCE_HEAD,
            "x1_commit": X1_COMMIT,
            "sealed_source_repository_negatives": d.INHERITED_NEGATIVES,
            "external_post_seal_negatives": d.EXTERNAL_POST_SEAL_NEGATIVES,
            "activation_negative_baseline": d.ACTIVATION_NEGATIVE_BASELINE,
            "effective_negatives": (
                d.ACTIVATION_NEGATIVE_BASELINE
                + len(d.X1_NEGATIVES)
                + len(X2_NEGATIVES)
                + len(d.PROPOSALS) * len(d.MUTATION_KINDS)
            ),
            "effective_open_gaps": d.INHERITED_OPEN_GAPS + 1,
            "effective_exact_gates": d.INHERITED_EXACT_GATES + 1,
            "route_state": "NOT_ELIGIBLE_EVIDENCE_NOT_FINAL",
        }
    )
    base.write_json("phase-truth.json", truth)

    build_receipt = base.read_json(
        ROOT / "validation/evidence-build-receipt.json"
    )
    build_receipt.update(
        {
            "sealed_source_repository_negatives": d.INHERITED_NEGATIVES,
            "external_post_seal_negatives": d.EXTERNAL_POST_SEAL_NEGATIVES,
            "activation_negative_baseline": d.ACTIVATION_NEGATIVE_BASELINE,
            "effective_negatives": (
                d.ACTIVATION_NEGATIVE_BASELINE
                + len(d.X1_NEGATIVES)
                + len(X2_NEGATIVES)
                + len(d.PROPOSALS) * len(d.MUTATION_KINDS)
            ),
        }
    )
    base.write_json(
        "validation/evidence-build-receipt.json",
        build_receipt,
    )

    workflow_request = base.read_json(
        ROOT / "workflow/workflow-plan-request.json"
    )
    workflow_request["plan_id"] = "caelen-v653-v6-x2-confirmation"
    workflow_request["requirements"]["baton_words"] = {
        "minimum": 10000,
        "maximum": 100000,
        "file_artifact": True,
    }
    confirmed_request_path = base.write_json(
        "workflow/x2-refinement/workflow-plan-request.json",
        workflow_request,
    )
    workflow_runner = (
        Path.home()
        / ".codex/skills/ghc-family-workflow-plan-refinement/scripts/"
        "ghc_family_workflow_plan_refinement.py"
    )
    confirmation = base.run(
        sys.executable,
        str(workflow_runner),
        str(confirmed_request_path),
        "--out-dir",
        str(ROOT / "workflow/x2-refinement"),
        check=False,
    )
    workflow_validation = base.read_json(
        ROOT / "workflow/x2-refinement/workflow-plan-validation.json"
    )
    workflow_issues = base.read_json(
        ROOT / "workflow/x2-refinement/workflow-plan-issues.json"
    )
    workflow_confirmation_passed = (
        confirmation.returncode == 0
        and workflow_validation["valid"]
        and workflow_validation["policy_checks"]
        == workflow_validation["policy_checks_passed"]
        and workflow_validation["issue_counts"]
        == {"errors": 0, "total": 0, "warnings": 0}
        and workflow_issues["counts"]["errors"] == 0
        and workflow_issues["counts"]["warnings"] == 0
        and workflow_issues["counts"]["issues"] == 0
    )
    if not workflow_confirmation_passed:
        raise RuntimeError(
            "additive x2 workflow confirmation failed: "
            f"{confirmation.stderr.strip() or confirmation.stdout.strip()}"
        )
    base.write_json(
        "workflow/x2-refinement/authorization-overlay.json",
        {
            "schema": "ghc.family.v653-v6.authorization-overlay.v1",
            "state": "INELIGIBLE_EVIDENCE_NOT_FINAL",
            "workflow_skill_status": workflow_validation["status"],
            "workflow_skill_issue": None,
            "legacy_skill_policy": "existing_task_only_after_terminal_gate",
            "live_authorization": (
                "Exactly one sanitized activation may be sent to the unique "
                "existing task titled exactly Orin Thale only after Caelen's "
                "clean, pushed, exact-final, four-way-equal validated closeout."
            ),
            "target_task_created": False,
            "sent": False,
            "forked": False,
            "collaboration_subagent": False,
            "route_authorization_changed": False,
            "boundary": (
                "This overlay records the live authorization and passing "
                "workflow confirmation; it does not activate or deliver Orin."
            ),
        },
    )

    addendum = base.read_json(
        ROOT / "tooling/ghc-family-index-x2-addendum.json"
    )
    addendum["workflow_confirmation"] = {
        "frozen_x1_validation_was_already_valid": True,
        "x2_validation_status": workflow_validation["status"],
        "workflow_confirmation_passed": workflow_confirmation_passed,
        "expected_legacy_messaging_policy_issue": False,
        "policy_checks": workflow_validation["policy_checks"],
        "policy_checks_passed": workflow_validation[
            "policy_checks_passed"
        ],
        "route_authorization_changed": False,
    }
    base.write_json("tooling/ghc-family-index-x2-addendum.json", addendum)

    ledger = ROOT / "method-flow/evidence-method-flow-ledger.json"
    if ledger.exists():
        base.run(
            sys.executable,
            str(base.METHOD_RUNNER),
            "validate",
            "--ledger",
            str(ledger),
            "--receipt",
            str(ROOT / "method-flow/evidence-method-flow-validation.json"),
        )
        base.run(
            sys.executable,
            str(base.METHOD_RUNNER),
            "summarize",
            "--ledger",
            str(ledger),
            "--json-output",
            str(ROOT / "method-flow/evidence-method-flow-summary.json"),
            "--markdown-output",
            str(ROOT / "method-flow/evidence-method-flow-summary.md"),
        )


def build() -> None:
    base.skill_markdown = skill_markdown
    base.wrapper_source = wrapper_source
    base.build_report = build_report
    with redirect_stdout(io.StringIO()):
        base.build()
    _postprocess_generated_files()
    truth = base.read_json(ROOT / "phase-truth.json")
    print(
        json.dumps(
            {
                "valid": True,
                "phase": d.PHASE,
                "outcomes": truth["outcomes"],
                "mutations": truth["mutations_executed_and_rejected"],
                "skills": truth["skills_initialized_validated_and_smoke_used"],
                "runners": truth["runners_built_and_invoked"],
                "negatives": truth["effective_negatives"],
                "route": truth["route_state"],
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    build()
