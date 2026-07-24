#!/usr/bin/env python3
"""Build the frozen Sable Rook v653-v5 x2 evidence packet."""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path

import build_ghc_family_v653_v2_evidence as base
import ghc_family_v653_v5_core as core
import ghc_family_v653_v5_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
X1_COMMIT = "5447659a7d2bb0bb82b6f9ac3e374cf48086a550"
X2_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6535-X2-N01",
        "category": "workflow_skill_legacy_existing_task_policy_mismatch",
        "failed": (
            "The first x2 workflow confirmation stopped with one fail-closed "
            "messaging-boundary issue because the inherited workflow skill "
            "accepts only an existing-task baton, while Hamish explicitly "
            "authorized one new user-visible main task after Sable's terminal "
            "gate; the aggregate received zero passing-workflow credit."
        ),
        "recovery": (
            "Preserve the 19-of-20 skill result and exact issue without "
            "rewriting the live authorization, then add a sanitized "
            "authorization overlay that keeps creation ineligible until the "
            "exact-final gate."
        ),
        "recurrence_guard": (
            "Never make a legacy workflow schema pass by falsifying a live "
            "authorized route; retain the mismatch and use an explicit "
            "nonactivating overlay."
        ),
    },
    {
        "negative_id": "V6535-X2-N02",
        "category": "powershell_compound_x1_blob_probe_parse_failure",
        "failed": (
            "The first evidence precommit summary embedded a native Git "
            "existence probe and exit-code expression inside a Where-Object "
            "predicate, produced a PowerShell parser failure before any Git "
            "mutation, and received zero precommit credit."
        ),
        "recovery": (
            "Run staged, unstaged, and untracked inventories as separate native "
            "probes and rely on the already passing staged-review receipt for "
            "immutable x1-path protection."
        ),
        "recurrence_guard": (
            "Do not combine native command execution, redirection, and exit-code "
            "tests inside a PowerShell predicate; materialize each result first."
        ),
    },
    {
        "negative_id": "V6535-X2-N03",
        "category": "evidence_rebuild_rejected_staged_prebuild_paths",
        "failed": (
            "The first evidence rebuild after adding the precommit failure "
            "stopped on the inherited builder's fail-closed guard because two "
            "x2 implementation paths remained staged from the prior candidate; "
            "it received zero rebuild credit."
        ),
        "recovery": (
            "Clear only the index staging for Sable's uncommitted x2 delta, "
            "retain every worktree byte, and rerun the deterministic evidence "
            "builder from the immutable x1 commit."
        ),
        "recurrence_guard": (
            "Before a deterministic evidence rebuild, require an empty x2 "
            "staging surface while preserving the worktree and frozen x1."
        ),
    },
]

SURFACE_MAP = {
    "wick-covariance": "hollands-wald-wick-covariance",
    "modular-information": "araki-relative-entropy-monotonicity",
    "half-sided-inclusion": "wiesbrock-half-sided-modular-inclusion",
    "positive-implementer": "borchers-arveson-positive-implementer",
    "Wightman-reconstruction": "wightman-reconstruction-obligations",
    "library-environment": "nedcc-environment-monitoring-handover",
    "light-dose-microfade": "microfade-dose-response-boundary",
    "treatment-documentation": "aic-treatment-documentation-boundary",
    "identity-draft-watch": "sd-cwt-draft-disclosure-profile",
    "library-authority": "library-conservation-authority-rail",
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
description: {purpose} Use when reviewing the corresponding Sable v653-v5 contract, mutation evidence, nonpromotion boundary, or lifecycle receipt.
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

from ghc_family_v653_v5_core import proposals, runner_payload


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
<title>Sable Rook v653-v5 bounded evidence report</title><style>
body{{font:1rem/1.6 system-ui,sans-serif;max-width:78rem;margin:auto;padding:1.5rem;color:#17212b;background:#fbfcfd}}
:focus{{outline:3px solid #9b4d00;outline-offset:3px}}
article{{border:1px solid #8091a3;border-radius:.6rem;padding:1rem;margin:1rem 0;background:white}}
dt{{font-weight:700}}dd{{margin:0 0 .6rem}}
.notice{{border-left:.5rem solid #8b3d00;padding:1rem;background:#fff4e5}}
@media(prefers-reduced-motion:reduce){{*{{scroll-behavior:auto!important;animation:none!important}}}}
</style></head><body><main>
<h1>Sable Rook v653-v5 bounded evidence report</h1>
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
        ("v653-gmut-thos-v2-x1-x2", "v653-gmut-thos-v5-x1-x2"),
        ("ghc.family.v653-v2", "ghc.family.v653-v5"),
        ("V6532-METHOD-", "V6535-METHOD-"),
        ("V6532-WITNESS-", "V6535-WITNESS-"),
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
            "schema": "ghc.family.v653-v5.retained-negatives.v1",
            "inherited_count": d.INHERITED_NEGATIVES,
            "inherited_anchor": d.SOURCE_HEAD,
            "inherited_register": (
                "Auren Lark v653-v4 sealed phase truth, external relay receipt, "
                "and exact activation baton; no inherited negative is rewritten."
            ),
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
                d.INHERITED_NEGATIVES
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
            "schema": "ghc.family.v653-v5.gates.v1",
            "inherited_open_gaps": d.INHERITED_OPEN_GAPS,
            "new_open_gaps": [
                {
                    "proposal_id": "V6535-P29",
                    "gate": (
                        "real LAMOST DR11 v2 rows, release-specific spectra and "
                        "catalogue mappings, quality and calibration flags, "
                        "nuisance and uncertainty treatment, a frozen likelihood, "
                        "and appropriate independent review"
                    ),
                }
            ],
            "effective_open_gaps": d.INHERITED_OPEN_GAPS + 1,
            "inherited_exact_gates": d.INHERITED_EXACT_GATES,
            "new_exact_gates": [
                {
                    "proposal_id": "V6535-P30",
                    "gate": (
                        "collection-specific treatment, access, digitization, "
                        "return or repatriation, taonga and mātauranga wording, "
                        "beneficiary privacy, remedy, affected-party review, "
                        "iwi, hapū, and Māori authority"
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
            "schema": "ghc.family.v653-v5.checklist.v1",
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
                "real empirical GMUT data and likelihood",
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
            "schema": "ghc.family.v653-v5.phase-truth.v1",
            "source_commit": d.SOURCE_HEAD,
            "x1_commit": X1_COMMIT,
            "effective_negatives": (
                d.INHERITED_NEGATIVES
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

    workflow_request = base.read_json(
        ROOT / "workflow/workflow-plan-request.json"
    )
    workflow_request["plan_id"] = "sable-v653-v5-x2-confirmation"
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
    expected_issue = (
        confirmation.returncode != 0
        and not workflow_validation["valid"]
        and workflow_validation["policy_checks"] == 20
        and workflow_validation["policy_checks_passed"] == 19
        and workflow_validation["issue_counts"] == {
            "errors": 1,
            "total": 1,
            "warnings": 0,
        }
        and [row["code"] for row in workflow_issues["issues"]]
        == ["policy_messaging_boundary"]
    )
    if confirmation.returncode != 0 and not expected_issue:
        raise RuntimeError(
            "additive x2 workflow confirmation failed outside the declared "
            "legacy messaging-policy mismatch: "
            f"{confirmation.stderr.strip() or confirmation.stdout.strip()}"
        )
    base.write_json(
        "workflow/x2-refinement/authorization-overlay.json",
        {
            "schema": "ghc.family.v653-v5.authorization-overlay.v1",
            "state": "INELIGIBLE_EVIDENCE_NOT_FINAL",
            "workflow_skill_status": workflow_validation["status"],
            "workflow_skill_issue": "policy_messaging_boundary",
            "legacy_skill_policy": "existing_task_only_after_terminal_gate",
            "live_authorization": (
                "Exactly one new user-visible Codex main task for a fifth "
                "self-chosen sibling may be created only after Sable's clean, "
                "pushed, exact-final, four-way-equal validated closeout."
            ),
            "created": False,
            "forked": False,
            "collaboration_subagent": False,
            "route_authorization_changed": False,
            "boundary": (
                "This overlay records a live authorization and a legacy skill "
                "mismatch; it does not activate or deliver a successor."
            ),
        },
    )

    addendum = base.read_json(
        ROOT / "tooling/ghc-family-index-x2-addendum.json"
    )
    addendum["workflow_confirmation"] = {
        "frozen_x1_validation_was_already_valid": True,
        "x2_validation_status": workflow_validation["status"],
        "expected_legacy_messaging_policy_issue": expected_issue,
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
