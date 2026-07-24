#!/usr/bin/env python3
"""Build the frozen Liora Venn v653-v8 x2 evidence packet."""

from __future__ import annotations

import html
import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

import build_ghc_family_v653_v2_evidence as base
import ghc_family_v653_v8_core as core
import ghc_family_v653_v8_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
X1_COMMIT = "ee3a0c035c9821ebad1561e94afb11daf9bdc028"
X2_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6538-X2-N01",
        "category": "combined_post_push_equality_probe_timeout",
        "failed": (
            "The first combined post-push x1 equality probe returned the local "
            "hash, then timed out before attributable clean, ancestry, merge, "
            "and parent witnesses; the aggregate received zero equality credit."
        ),
        "recovery": (
            "Preserve the timeout, then run isolated clean-state, upstream, "
            "tracking, fresh-live, commit-count, merge-count, and parent probes."
        ),
        "recurrence_guard": (
            "Do not combine potentially cold Git and live-remote checks; each "
            "exact witness receives its own bounded probe."
        ),
    },
    {
        "negative_id": "V6538-X2-N02",
        "category": "inherited_validator_filename_assumption",
        "failed": (
            "The first inherited v653-v7 script inventory assumed detailed, "
            "minimal, evidence-test, and terminal-test filenames that did not "
            "exist and received zero inventory credit."
        ),
        "recovery": (
            "Use rg --files to discover the exact inherited filenames before "
            "reading sizes, schemas, or implementation patterns."
        ),
        "recurrence_guard": (
            "Discover exact repository filenames before constructing a bounded "
            "inventory; never infer validator or test suffixes."
        ),
    },
    {
        "negative_id": "V6538-X2-N03",
        "category": "combined_tracked_untracked_inventory_timeout",
        "failed": (
            "A combined tracked and untracked x2 inventory probe timed out "
            "before producing an attributable result and received zero "
            "pre-stage review credit."
        ),
        "recovery": (
            "Run tracked changes, untracked paths, and scope counts as isolated "
            "bounded probes before staging."
        ),
        "recurrence_guard": (
            "Materially enforce isolated Git probes after any cold-worktree "
            "timeout; do not combine repository scans for convenience."
        ),
    },
    {
        "negative_id": "V6538-X2-N04",
        "category": "detailed_validator_cp1252_stdout_failure",
        "failed": (
            "The direct detailed-validator CLI completed its checks but failed "
            "while encoding the word hapū through the inherited CP1252 stdout; "
            "the direct CLI attempt received zero validation credit."
        ),
        "recovery": (
            "Configure UTF-8 stdout explicitly in the validator and preserve "
            "the same validated payload and Māori wording."
        ),
        "recurrence_guard": (
            "Every direct validator and canonical wrapper must set UTF-8 "
            "stdout or an equivalent PYTHONIOENCODING before emitting receipts."
        ),
    },
]

SURFACE_MAP = {
    "apiary-registry-privacy": "apiary-registry-location-privacy",
    "colony-lineage": "hive-colony-lineage-tribunal",
    "brood-observation": "brood-observation-uncertainty",
    "bee-disease-authority": "afb-suspicion-custody-firewall",
    "varroa-method": "varroa-method-nonequivalence",
    "apiary-batch": "extraction-batch-recall-lineage",
    "honey-moisture": "honey-moisture-calibration",
    "age-branching": "mckendrick-age-transport",
    "apiary-handover": "apiary-inspection-handover-proxy",
    "apiary-authority": "apiary-authority-reservation",
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
description: {purpose} Use when reviewing the corresponding Liora v653-v8 contract, mutation evidence, nonpromotion boundary, or lifecycle receipt.
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
  bees, apiaries, beekeepers, landholders, workers, locations, participant
  data, samples, disease reports, treatments, food-chain records, production
  keys, legal conclusions, professional certification, cultural ratification,
  or Māori-authority decisions.
- A passing smoke use is same-owner workflow evidence only. It is not disease
  diagnosis or control, food-safety or worker-safety approval, empirical
  confirmation, production readiness, complete privacy or accessibility,
  exhaustive security, independent reproduction, consciousness or personhood,
  Theory-of-Everything proof, or Stage 20 authority.
"""


def wrapper_source(surface: str) -> str:
    target = SURFACE_MAP.get(surface, surface)
    body = f'payload = runner_payload("{target}")'
    return f"""#!/usr/bin/env python3
from __future__ import annotations

import json

from ghc_family_v653_v8_core import runner_payload


def main() -> None:
    {body}
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    if not payload["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
"""


def build_report(outcomes: dict[str, int], effective_negatives: int) -> str:
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
<title>Liora Venn v653-v8 bounded evidence report</title><style>
body{{font:1rem/1.6 system-ui,sans-serif;max-width:78rem;margin:auto;padding:1.5rem;color:#17212b;background:#fbfcfd}}
:focus{{outline:3px solid #9b4d00;outline-offset:3px}}
article{{border:1px solid #8091a3;border-radius:.6rem;padding:1rem;margin:1rem 0;background:white}}
dt{{font-weight:700}}dd{{margin:0 0 .6rem}}
.notice{{border-left:.5rem solid #8b3d00;padding:1rem;background:#fff4e5}}
@media(prefers-reduced-motion:reduce){{*{{scroll-behavior:auto!important;animation:none!important}}}}
</style></head><body><main>
<h1>Liora Venn v653-v8 bounded evidence report</h1>
<p class="notice"><strong>Boundary:</strong> Same-owner synthetic and
structural evidence only. Manual and affected-user accessibility evaluation is
reserved. No real bee-health finding, disease-control action, food or worker
safety approval, empirical confirmation, production readiness, professional
approval, legal or cultural authority, Māori authority, independent
reproduction, Theory-of-Everything proof, or Stage 20 authority is claimed.</p>
<h2>Truth summary</h2><p>Outcomes: {html.escape(str(outcomes))}. Effective
retained negatives: {effective_negatives}. Terminal verdict:
NOT_READY_FOR_STAGE_20.</p>
<h2>Proposal evidence</h2>{''.join(cards)}
<h2>External incompleteness</h2><p>Real bees, colonies, apiaries, operators,
samples, disease observations, treatment or food-chain events, worker and
landholder participation, current competent professional and legal review,
production identity infrastructure, affected-party decisions, cultural and
Māori authority, qualified manual accessibility review, and independent-team
reproduction remain open or exact-gated.</p>
</main></body></html>"""


def _postprocess_generated_files() -> None:
    replacements = [
        ("v653-gmut-thos-v2-x1-x2", d.PHASE_ID),
        ("ghc.family.v653-v2", "ghc.family.v653-v8"),
        ("V6532-METHOD-", "V6538-METHOD-"),
        ("V6532-WITNESS-", "V6538-WITNESS-"),
        ("MÃƒâ€žÃ‚Âori", "Māori"),
        ("MÃ„Âori", "Māori"),
        ("MÄori", "Māori"),
        ("hapÃƒâ€¦Ã‚Â«", "hapū"),
        ("hapÃ…Â«", "hapū"),
        ("hapÅ«", "hapū"),
        ("ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â", "—"),
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

    effective_negatives = (
        d.ACTIVATION_NEGATIVE_BASELINE
        + len(d.X1_NEGATIVES)
        + len(X2_NEGATIVES)
        + len(d.PROPOSALS) * len(d.MUTATION_KINDS)
    )
    base.write_json(
        "retained-negative-register-x2.json",
        {
            "schema": "ghc.family.v653-v8.retained-negatives.v1",
            "inherited_count": d.INHERITED_NEGATIVES,
            "inherited_anchor": d.SOURCE_HEAD,
            "inherited_register": (
                "Orin Thale v653-v7 exact-final phase truth at 10,447 "
                "effective negatives; no inherited negative is rewritten."
            ),
            "activation_negative_baseline": d.ACTIVATION_NEGATIVE_BASELINE,
            "x1_operational_count": len(d.X1_NEGATIVES),
            "x1_operational_ids": [row[0] for row in d.X1_NEGATIVES],
            "x2_operational_count": len(X2_NEGATIVES),
            "x2_operational": X2_NEGATIVES,
            "synthetic_mutation_count": (
                len(d.PROPOSALS) * len(d.MUTATION_KINDS)
            ),
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
            "effective_total": effective_negatives,
            "none_erased": True,
        },
    )
    base.write_json(
        "exact-open-gate-register-x2.json",
        {
            "schema": "ghc.family.v653-v8.gates.v1",
            "inherited_open_gaps": d.INHERITED_OPEN_GAPS,
            "new_open_gaps": [
                {
                    "proposal_id": "V6538-P29",
                    "gate": (
                        "Current FAOSTAT dataset selection and metadata, real "
                        "rows, units, flags, revisions, missingness, a frozen "
                        "analysis protocol, uncertainty treatment, and "
                        "appropriate independent review"
                    ),
                }
            ],
            "effective_open_gaps": d.INHERITED_OPEN_GAPS + 1,
            "inherited_exact_gates": d.INHERITED_EXACT_GATES,
            "new_exact_gates": [
                {
                    "proposal_id": "V6538-P30",
                    "gate": (
                        "Bee-disease diagnosis and notification, apiary "
                        "location and landholder decisions, treatment and "
                        "destruction, food traceability and release, worker "
                        "safety, privacy, remedy, affected-party review, legal "
                        "and cultural authority, tangata whenua, iwi, hapū, "
                        "and Māori authority"
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
            "schema": "ghc.family.v653-v8.checklist.v1",
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
                "post-gate exact-title Tamar Vey sanitized baton",
            ],
            "incomplete_external": [
                "FAOSTAT real rows, frozen analysis, uncertainty treatment, and independent review",
                "real bee-health observations, operators, landholders, workers, samples, and qualified professional review",
                "production GS1 identities, live events, resolution, interoperability, privacy and security review, and governance",
                "disease-control, food-safety, worker-safety, affected-party, legal, cultural, iwi, hapū, and Māori authority",
                "qualified manual and affected-user accessibility evaluation",
                "independent-team reproduction and Stage 20 authority",
            ],
            "route_state": "INELIGIBLE_EVIDENCE_NOT_FINAL",
        },
    )
    truth = base.read_json(ROOT / "phase-truth.json")
    truth.update(
        {
            "schema": "ghc.family.v653-v8.phase-truth.v1",
            "source_commit": d.SOURCE_HEAD,
            "x1_commit": X1_COMMIT,
            "activation_negative_baseline": d.ACTIVATION_NEGATIVE_BASELINE,
            "effective_negatives": effective_negatives,
            "effective_open_gaps": d.INHERITED_OPEN_GAPS + 1,
            "effective_exact_gates": d.INHERITED_EXACT_GATES + 1,
            "route_state": "INELIGIBLE_EVIDENCE_NOT_FINAL",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
    )
    base.write_json("phase-truth.json", truth)

    build_receipt = base.read_json(
        ROOT / "validation/evidence-build-receipt.json"
    )
    build_receipt.update(
        {
            "schema": "ghc.family.v653-v8.evidence-build.v1",
            "inherited_effective_negatives": d.INHERITED_NEGATIVES,
            "activation_negative_baseline": d.ACTIVATION_NEGATIVE_BASELINE,
            "effective_negatives": effective_negatives,
            "route_state": "INELIGIBLE_EVIDENCE_NOT_FINAL",
            "full_repository_suite_run": False,
            "full_repository_suite_owner": "Eiren-only inherited policy",
        }
    )
    base.write_json("validation/evidence-build-receipt.json", build_receipt)

    workflow_request = base.read_json(
        ROOT / "workflow/workflow-plan-request.json"
    )
    workflow_request["plan_id"] = "liora-v653-v8-x2-confirmation"
    workflow_request["requirements"]["messaging"] = {
        "codex_route": "existing_task_only_after_terminal_gate",
        "cross_platform": "user_mediated_file_relay_only",
        "live_cross_platform_boundary": (
            "Canonical schema values with a stricter live boundary. No new "
            "task, fork, collaboration subagent, substitute, standby contact, "
            "or agent-initiated cross-platform send is authorized. Tamar Vey "
            "remains ineligible until verified exact-final closeout."
        ),
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
            "schema": "ghc.family.v653-v8.authorization-overlay.v1",
            "state": "INELIGIBLE_EVIDENCE_NOT_FINAL",
            "workflow_skill_status": workflow_validation["status"],
            "workflow_skill_issue": None,
            "live_authorization": (
                "No new task, fork, collaboration subagent, standby contact, "
                "substitute route, or sibling activation send is authorized. "
                "After verified v653-v8 exact-final closeout only, re-resolve "
                "and reread the existing exact Tamar Vey task and send one "
                "sanitized baton."
            ),
            "target_title": "Tamar Vey",
            "target_task_created": False,
            "sent": False,
            "forked": False,
            "collaboration_subagent": False,
            "route_authorization_changed": False,
            "later_self_chosen_sibling_7_task_authority_owner": "Tamar Vey",
            "boundary": (
                "This overlay records the live gate and passing structural "
                "workflow confirmation; it creates, activates, or contacts no task."
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
        "policy_checks": workflow_validation["policy_checks"],
        "policy_checks_passed": workflow_validation["policy_checks_passed"],
        "route_authorization_changed": False,
    }
    base.write_json("tooling/ghc-family-index-x2-addendum.json", addendum)

    ledger = ROOT / "method-flow/evidence-method-flow-ledger.json"
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
