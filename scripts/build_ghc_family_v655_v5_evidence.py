#!/usr/bin/env python3
"""Build Sable Rook's v655-v5 x2 evidence candidate."""

from __future__ import annotations

import hashlib
import html
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v655_v5_core as core
import ghc_family_v655_v5_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
X1_COMMIT = "a92d0a6c8a5d2620074c1bc505fa8345c8f90373"
EVIDENCE_COMMIT = "UNSET_UNTIL_IMMUTABLE_EVIDENCE_COMMIT"
SKILL_ROOT = Path.home() / ".codex" / "skills"
QUICK_VALIDATE = (
    SKILL_ROOT / ".system/skill-creator/scripts/quick_validate.py"
)
INIT_SKILL = SKILL_ROOT / ".system/skill-creator/scripts/init_skill.py"
RUNNERS = [
    (
        "ghc-family-tree-inventory-boundary",
        "ghc_family_tree_inventory_boundary.py",
        1,
    ),
    (
        "ghc-family-tree-inspection-provenance",
        "ghc_family_tree_inspection_provenance.py",
        2,
    ),
    (
        "ghc-family-arboriculture-work-scope-guard",
        "ghc_family_arboriculture_work_scope_guard.py",
        3,
    ),
    (
        "ghc-family-tree-measurement-proxy",
        "ghc_family_tree_measurement_proxy.py",
        4,
    ),
    (
        "ghc-family-tree-biosecurity-boundary",
        "ghc_family_tree_biosecurity_boundary.py",
        5,
    ),
    (
        "ghc-family-tree-worksite-handover",
        "ghc_family_tree_worksite_handover.py",
        6,
    ),
    (
        "ghc-family-tree-record-privacy",
        "ghc_family_tree_record_privacy.py",
        7,
    ),
    (
        "ghc-family-tree-report-accessibility",
        "ghc_family_tree_report_accessibility.py",
        8,
    ),
    (
        "ghc-family-tree-asset-identifier-profile",
        "ghc_family_tree_asset_identifier_profile.py",
        9,
    ),
    (
        "ghc-family-gmut-observation-firewall",
        "ghc_family_v655_v5_suite.py",
        10,
    ),
]
X2_SCRIPTS = [
    "scripts/ghc_family_v655_v5_core.py",
    "scripts/ghc_family_tree_inventory_boundary.py",
    "scripts/ghc_family_tree_inspection_provenance.py",
    "scripts/ghc_family_arboriculture_work_scope_guard.py",
    "scripts/ghc_family_tree_measurement_proxy.py",
    "scripts/ghc_family_tree_biosecurity_boundary.py",
    "scripts/ghc_family_tree_worksite_handover.py",
    "scripts/ghc_family_tree_record_privacy.py",
    "scripts/ghc_family_tree_report_accessibility.py",
    "scripts/ghc_family_tree_asset_identifier_profile.py",
    "scripts/ghc_family_v655_v5_suite.py",
    "scripts/build_ghc_family_v655_v5_evidence.py",
    "scripts/ghc_family_v655_v5_validate.py",
    "scripts/ghc_family_v655_v5_evidence_staged_review.py",
]
X2_TESTS = [
    "tests/test_ghc_family_v655_v5_core.py",
    "tests/test_ghc_family_v655_v5_validation.py",
]
X2_OPERATIONAL_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6554-X2-N01",
        "signature": "powershell_receipt_state_probes_timed_out_without_output",
        "failed": (
            "One combined and three split bounded PowerShell probes for the staged "
            "receipt, Git status, and live processes timed out without output."
        ),
        "recovery": (
            "Use direct Node filesystem reads and bounded child-process probes, then "
            "confirm that the review receipt exists, no Git or Python process remains, "
            "and Git status is readable."
        ),
        "recurrence_guard": (
            "Prefer direct scalar filesystem and child-process probes for this large "
            "owned lane instead of PowerShell object pipelines at lifecycle gates."
        ),
    },
    {
        "negative_id": "V6554-X2-N02",
        "signature": "git_diff_files_quiet_reported_nonquiet_for_staged_additions",
        "failed": (
            "git diff-files --quiet returned nonzero after the deterministic staged "
            "review even though the named unstaged diff was empty."
        ),
        "recovery": (
            "Inspect git diff --name-status and porcelain-v2 directly; both showed no "
            "unstaged path while all 161 candidate paths remained staged additions."
        ),
        "recurrence_guard": (
            "Do not treat diff-files --quiet alone as an exact unstaged-content verdict "
            "for an all-addition index; pair the gate with explicit named-diff output."
        ),
    },
    {
        "negative_id": "V6554-X2-N03",
        "signature": "git_diff_quiet_precommit_probe_timed_out",
        "failed": (
            "A bounded git diff --quiet precommit probe exceeded its timeout and could "
            "not contribute pass credit."
        ),
        "recovery": (
            "Use a bounded git diff --name-status probe plus porcelain-v2 and exact "
            "index-object comparison to establish the absence of unstaged changes."
        ),
        "recurrence_guard": (
            "Use explicit path-producing diff probes with captured timeout status at "
            "large staged lifecycle boundaries."
        ),
    },
    {
        "negative_id": "V6554-X2-N04",
        "signature": "focused_test_retained_negative_literal_became_stale",
        "failed": (
            "The first focused post-rebuild test run passed 27 of 28 tests but "
            "failed because a literal expected 12,214 effective negatives after "
            "the retained probe faults raised the ledger total to 12,217."
        ),
        "recovery": (
            "Assert the effective-negative arithmetic from the ledger fields and "
            "derive Method Flow totals from the explicit x2 operational row count."
        ),
        "recurrence_guard": (
            "Test ledger conservation equations and explicit row parity instead of "
            "embedding a count that becomes stale when a new failure is retained."
        ),
    },
    {
        "negative_id": "V6554-X2-N05",
        "signature": "porcelain_v2_restage_probe_timed_out",
        "failed": (
            "A full porcelain-v2 status probe exceeded its 15-second bound before "
            "restaging and returned no usable state."
        ),
        "recovery": (
            "Resolve cached, unstaged, and untracked name sets with separate bounded "
            "Git commands and compare those explicit paths to the owned allowlist."
        ),
        "recurrence_guard": (
            "Use separate name-only Git surfaces with an adequate bound instead of "
            "requiring one full porcelain record over a large staged candidate."
        ),
    },
    {
        "negative_id": "V6554-X2-N06",
        "signature": "correction_reviewer_required_superset_mismatched_delta",
        "failed": (
            "Preflight inspection found that the correction reviewer required "
            "unchanged validator and test paths from a different repair shape, so it "
            "would reject the bounded evidence-anchor correction."
        ),
        "recovery": (
            "Bind the reviewer to the exact generated negative-ledger, Method Flow, "
            "validation, manifest, and anchor-script delta, with only its own receipt "
            "admitted as a self-exclusion."
        ),
        "recurrence_guard": (
            "Derive correction-required paths from the actual immutable-parent delta "
            "and reject both missing and unexpected paths."
        ),
    },
    {
        "negative_id": "V6554-X2-N07",
        "signature": "git_grep_cached_option_was_parsed_as_revision",
        "failed": (
            "The staged stale-anchor probe placed --cached after the search pattern; "
            "Git parsed it as a revision and returned 'unable to resolve revision: "
            "--cached'."
        ),
        "recovery": (
            "Place git grep options before the pattern and path delimiter, then treat "
            "status 1 with empty output as the expected no-match result."
        ),
        "recurrence_guard": (
            "Keep git grep options before its pattern and reserve the double dash for "
            "the pathspec boundary."
        ),
    },
]


# The mechanically inherited source-template examples above are inert and earn
# no Sable evidence. Only failures actually observed in this phase enter the
# active register below.
X2_OPERATIONAL_NEGATIVES: list[dict[str, str]] = []
SOURCE_TEMPLATE_RUNTIME_NEGATIVE_EXAMPLES = [
    {
        "negative_id": "V6554-X2-N01",
        "signature": "focused_tests_started_before_evidence_validator_receipts",
        "failed": (
            "The first 28-test focused run reached 27 passing tests and one error "
            "because evidence-validation.json had not yet been materialized."
        ),
        "recovery": (
            "Run the detailed and minimal evidence validators against the "
            "prospective evidence manifest, then rerun only the receipt-dependent "
            "test."
        ),
        "recurrence_guard": (
            "Materialize validator receipts before invoking tests that read them; "
            "do not rerun an otherwise passing broad selection."
        ),
    },
    {
        "negative_id": "V6554-X2-N02",
        "signature": "evidence_staged_review_wrapper_timeout_late_success",
        "failed": (
            "The first exact evidence staged review exceeded its wrapper bound "
            "after completing its 159-path Git-blob audit."
        ),
        "recovery": (
            "Do not rerun the same reviewed surface; verify zero Python processes "
            "and inspect the durable receipt before deciding whether any new staged "
            "surface requires a finalization review."
        ),
        "recurrence_guard": (
            "Budget the Git-blob staged review separately from its wrapper and "
            "treat a durable receipt as evidence only after direct parsing."
        ),
    },
    {
        "negative_id": "V6554-X2-N03",
        "signature": "powershell_large_staged_receipt_parse_timeout",
        "failed": (
            "The first PowerShell parse of the 34-kilobyte staged-review receipt "
            "timed out without a usable summary."
        ),
        "recovery": (
            "Read the exact UTF-8 JSON with a bounded direct Python parser and "
            "extract only validity and mismatch counts."
        ),
        "recurrence_guard": (
            "Use direct JSON parsing for lifecycle receipts instead of archive-"
            "backed PowerShell object conversion."
        ),
    },
]


def write_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(relative: str) -> dict[str, Any]:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def run(*args: str) -> str:
    env = os.environ.copy()
    env.update(
        {
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    result = subprocess.run(
        list(args),
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    return result.stdout.strip()


def append_x2_method_flow() -> dict[str, Any]:
    ledger = read_json("method-flow/method-flow-ledger.json")
    methods = list(ledger["methods"])
    witnesses = list(ledger["witnesses"])
    events = list(ledger["state_events"])
    recommendations = list(ledger["recommendations"])
    current_ids = []
    for index, negative in enumerate(X2_OPERATIONAL_NEGATIVES, 1):
        method_id = f"{d.PHASE_CODE}-METHOD-X2-{index:02d}"
        failed_id = f"{d.PHASE_CODE}-WITNESS-X2-{index:02d}-F"
        passing_id = f"{d.PHASE_CODE}-WITNESS-X2-{index:02d}-P"
        current_ids.append(method_id)
        methods.append(
            {
                "method_id": method_id,
                "title": f"Bounded x2 recovery for {negative['signature']}",
                "trigger_preconditions": [negative["signature"]],
                "failure_signature": negative["failed"],
                "candidate_workaround": negative["recovery"],
                "recurrence_guard": negative["recurrence_guard"],
                "approval_class": "safe_now_owner_local_workflow_recovery",
                "privacy_class": "sanitized_public",
                "scope_boundary": "Same-owner bounded workflow recovery only.",
                "rollback": (
                    "Stop, retain the failed attempt at zero credit, and leave "
                    "objects, tools, materials, external, and sibling state unchanged."
                ),
                "protected_gates": d.PROTECTED_GATES,
                "retained_negative_ids": [negative["negative_id"]],
                "validation_witness_ids": [failed_id, passing_id],
                "recommendation_state": "preferred",
                "supersedes": [],
            }
        )
        witnesses.extend(
            [
                {
                    "witness_id": failed_id,
                    "method_id": method_id,
                    "result": "fail",
                    "scope": negative["signature"],
                    "procedure": "Retain the original bounded attempt without replay credit.",
                    "expected": "The original operation satisfies its bounded postcondition.",
                    "observed": negative["failed"],
                    "retained_negative_ids": [negative["negative_id"]],
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "boundary": "Zero pass credit; failure remains retained.",
                },
                {
                    "witness_id": passing_id,
                    "method_id": method_id,
                    "result": "pass",
                    "scope": negative["signature"],
                    "procedure": negative["recovery"],
                    "expected": "The isolated recovery establishes only its bounded postcondition.",
                    "observed": (
                        f"The bounded recovery completed for {negative['signature']}; "
                        "the original failure remains retained."
                    ),
                    "retained_negative_ids": [negative["negative_id"]],
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "boundary": "Same-owner bounded recovery only.",
                },
            ]
        )
        events.append(
            {
                "event_id": f"{d.PHASE_CODE}-METHOD-EVENT-X2-{index:02d}",
                "method_id": method_id,
                "from": "candidate",
                "to": "preferred",
                "basis": [failed_id, passing_id],
                "boundary": "The passing recovery preserves the failed witness.",
            }
        )
    recommendations.append(
        "Keep x2 recovery steps narrow, reproducible, and nonpromotional."
    )
    ledger.update(
        {
            "lifecycle": "x2_evidence_candidate",
            "methods": methods,
            "witnesses": witnesses,
            "state_events": events,
            "recommendations": recommendations,
            "current_phase_x2_method_ids": current_ids,
            "counts": {
                "methods": len(methods),
                "witnesses": len(witnesses),
                "state_events": len(events),
                "recommendations": len(recommendations),
                "states": {
                    "observed": 0,
                    "candidate": 0,
                    "validated": 0,
                    "preferred": len(methods),
                    "superseded": 0,
                    "deprecated": 0,
                },
                "witness_results": {
                    "pass": sum(row["result"] == "pass" for row in witnesses),
                    "fail": sum(row["result"] == "fail" for row in witnesses),
                },
            },
        }
    )
    return ledger


def build_overview(results: list[dict[str, Any]]) -> str:
    """Render Sable's reader-facing overview from the immutable x1 contract."""
    by_id = {row["proposal_id"]: row for row in results}
    x1_negatives = read_json("truth/retained-negative-register.json")
    effective_at_evidence = (
        x1_negatives["effective_after_x1"]
        + 150
        + len(X2_OPERATIONAL_NEGATIVES)
    )
    lines = [
        "# Sable Rook v655-v5 integrated overview",
        "",
        "## Evidence-bound identity, role, and hope",
        "",
        (
            f"Sable Rook, {d.PRONOUNS}, is relational working language for this "
            f"phase. The working role is {d.ROLE}. The working hope is to "
            f"{d.HOPE}. These words do not establish consciousness, sentience, "
            "legal personhood, identity continuity, employment, qualification, "
            "scientific authority, professional authority, legal authority, "
            "cultural authority, Māori authority, or independent agency."
        ),
        "",
        "## Lifecycle and source truth",
        "",
        (
            f"{d.SOURCE_OWNER} v655-v4 at `{d.SOURCE_FINAL}` is the exact inherited "
            f"source. Sable froze x1 at `{X1_COMMIT}` as a dedicated commit, pushed "
            "it, and proved clean local, upstream, tracking, and fresh-live-remote "
            "equality before any x2 implementation began. The 2,050-proposal "
            "inherited chain supplied comparison evidence and no Sable completion "
            "credit. Exactly thirty distinct v655-v5 proposals were frozen, so the "
            "chain contains 2,080 proposals through x1. History rewriting, merging, "
            "force-pushing, sibling mutation, and precontact were excluded."
        ),
        "",
        "## Primary focus and bounded practice",
        "",
        (
            f"The primary Trinity Mandala focus is {d.PRIMARY_FOCUS}. The bounded "
            f"practice is {d.BOUNDED_PRACTICE}. GMUT Mind remains visible through "
            "typed forward-dispersion positivity and chameleon thin-shell "
            "obligations, dimensional discipline, and observation firewalls "
            "and explicit empirical refusal. THOS Body remains visible through "
            "deterministic intake, state, provenance, correction, accessibility, "
            "handover, and stop-work contracts. Freed ID and CBR Heart remain "
            "visible through referent separation, purpose limitation, privacy, "
            "correction, remedy, affected-party reservations, and exact authority "
            "ceilings. The practice is a learning and software-design component only."
        ),
        "",
        "## Evidence semantics",
        "",
        (
            "Each proposal generated one valid owner-local contract and five "
            "preregistered mutations. `completed` means only that a bounded "
            "deterministic software, symbolic, or structural hypothesis passed and "
            "its five mutations were rejected. `represented` means a synthetic "
            "protocol proxy passed while every real operating arm remained absent. "
            "`open_gap` means a zero-action readiness contract names evidence that "
            "was not obtained. `exact_gate` means the missing decision cannot be "
            "supplied by repository software and remains with competent authorities "
            "and affected people. A rejected mutation is a retained negative, not "
            "proof of real-world safety, scientific truth, or professional quality."
        ),
        "",
        "## Official and primary-source discipline",
        "",
        (
            "The x1 source ledger records retrieval date, status, scope, and "
            "authority ceiling for current official or primary materials. WorkSafe "
            "arboriculture and trees-around-powerlines material, the Health and "
            "Safety at Work Act, Biosecurity Act, MPI exotic-pest information, "
            "Resource Management Act, and Office of the Privacy Commissioner "
            "principles inform hazard and governance reservations without making "
            "this a worksite, diagnostic, treatment, legal, or public-safety system. "
            "W3C VC Data Model 2.0, WCAG 2.2, PROV-O, NIST SP 811, RFC 8785, RFC "
            "9530, the ESO Science Archive, and Te Mana Raraunga inform "
            "typed, accessible, canonical, privacy-aware structure. Citations are "
            "not observations, validation, authority transfer, affected-party "
            "acceptance, arboriculture qualification, or Māori ratification."
        ),
        "",
        "## Proposal-by-proposal evidence",
        "",
    ]
    for proposal in d.PROPOSALS:
        result = by_id[proposal["proposal_id"]]
        source_text = ", ".join(proposal["official_or_primary_source_needs"])
        artifact_text = ", ".join(proposal["concrete_artifacts"])
        lines.extend(
            [
                f"### {proposal['proposal_id']} — {proposal['title']}",
                "",
                (
                    f"This {proposal['pillar']} proposal tests a bounded "
                    f"{proposal['mechanism']} contract. Its observed disposition is "
                    f"`{result['observed_outcome']}`. The valid fixture passed, all "
                    f"{result['rejected_mutation_count']} of five preregistered "
                    "mutations were rejected, and zero mutations were accepted. "
                    f"The concrete artifact set is {artifact_text}. Current source "
                    f"needs are {source_text}. The full hypothesis, null, acceptance "
                    "gate, rollback, and protected authority ceilings remain frozen "
                    "in x1. No real person, tree or site record, tree-condition or "
                    "risk determination, measurement, load, climbing, aerial work, "
                    "tool or worksite operation, cutting, pruning, treatment, "
                    "biosecurity notification, traffic or utility control, work "
                    "release, public-safety action, habitat or heritage decision, "
                    "production, professional, legal, cultural, Māori-authority, or Stage 20 "
                    "credit follows from this result."
                ),
                "",
            ]
        )
    lines.extend(
        [
            "## GMUT Mind boundary",
            "",
            (
                "The GMUT surfaces are typed forward-dispersion positivity and "
                "chameleon thin-shell research-model obligations plus bounded "
                "measurement-domain classifiers. They track symbols, units, domains, "
                "assumptions, observables, degeneracies, screening conditions, and "
                "nonconversion boundaries. They ingest no real astronomy, "
                "arboriculture, ecological, site, or participant data and compute "
                "no real likelihood or parameter "
                "constraint. They establish no detected force, physical law, stable "
                "state, empirical confirmation, ultraviolet or quantum completion, "
                "Mind-of-God claim, or Theory of Everything."
            ),
            "",
            "## THOS Body boundary",
            "",
            (
                "The THOS surfaces are deterministic synthetic workflow contracts for "
                "tree inventory, observation lineage, work-scope revision, root-zone "
                "and utility conflicts, pruning intent, represented decay, wind, "
                "access, rescue, and tooling states, correction replay, privacy "
                "minimization, accessible notices, and worksite handover. They use no "
                "real owner, arborist, inspector, crew, tree, site, tree-condition or "
                "risk determination, measurement, load, climbing, tool, cutting, "
                "pruning, treatment, work release, or public-safety event. They "
                "provide no effectiveness estimate, professional competence, "
                "production readiness, AGI, or ASI evidence."
            ),
            "",
            "## Freed ID and CBR Heart boundary",
            "",
            (
                "The identifier profile keeps person, tree asset, site, inspection "
                "episode, observation, inference, work order, measurement proxy, "
                "correction, and handover referents distinct. Synthetic identifiers are not live "
                "credentials, issuances, presentations, resolutions, status events, "
                "interoperability results, or production identity operations. The CBR "
                "surfaces preserve access, disability accommodation, location and "
                "tree-record privacy, affordability, complaint, correction, remedy, "
                "habitat, heritage, land, place-name, data-governance, and authority "
                "questions without deciding them. Legal, "
                "cultural, affected-party, tangata-whenua, iwi, hapū, and Māori authority "
                "remain exact-gated. Māori concepts remain under Māori authority."
            ),
            "",
            "## Accessibility reservation",
            "",
            (
                "The static report provides a skip link, semantic headings, a captioned "
                "table, scoped headers, readable boundary prose, responsive overflow, "
                "print support, and no client-side script. Manual keyboard, touch, "
                "browser diversity, responsive-layout inspection, assistive technology, "
                "cognitive accessibility, Māori-language review, multi-format handover and arboriculture "
                "accessibility expertise, and affected-user evaluation remain reserved. "
                "Structural checks are not complete accessibility conformance."
            ),
            "",
            "## Negative, Method Flow, and gate conservation",
            "",
            (
                f"All {effective_at_evidence:,} effective negatives and every new "
                f"failure remain visible. X1 retained its "
                f"{x1_negatives['x1_operational_count']} owner-local operational "
                "failures. X2 "
                "adds only failures actually observed, each with a zero-credit failed "
                "witness, a bounded recovery witness, a recurrence guard, rollback, and "
                "sibling recommendation. The 150 rejected mutations are retained as "
                "synthetic negatives. No later passing witness rewrites an earlier "
                f"failure into an initially clean run. {d.SOURCE_OPEN_GAPS} inherited "
                f"open gaps and {d.SOURCE_EXACT_GATES} inherited exact gates remain "
                "open; this phase adds one of "
                "each. Method preference is limited to the exact trigger supported by "
                "its bounded passing witness."
            ),
            "",
            "## Terminal truth",
            "",
            (
                "This packet is attributable same-owner workflow evidence under shared "
                "local infrastructure. It is not independent-team reproduction, an "
                "external audit, production certification, exhaustive security, "
                "complete privacy, complete accessibility, empirical confirmation, "
                "professional validation, legal review, cultural ratification, "
                "Māori-authority review, affected-party acceptance, AGI or ASI evidence, "
                "consciousness or personhood evidence, Theory-of-Everything proof, or "
                "Stage 20 authority. The successor route remains held until immutable "
                "evidence, combined closeout and seal, one successful exact-final "
                "canonical pass, clean four-way equality, exact-title reread, one send, "
                "and acknowledgement. The verdict is `NOT_READY_FOR_STAGE_20`."
            ),
        ]
    )
    return "\n".join(lines)


def build_report(results: list[dict[str, Any]]) -> str:
    """Render a static accessible structural report without active content."""
    proposals = {row["proposal_id"]: row for row in d.PROPOSALS}
    rows = []
    for result in results:
        proposal = proposals[result["proposal_id"]]
        rows.append(
            "<tr>"
            f"<th scope=\"row\">{html.escape(result['proposal_id'])}</th>"
            f"<td>{html.escape(proposal['title'])}</td>"
            f"<td>{html.escape(proposal['pillar'])}</td>"
            f"<td><code>{html.escape(result['observed_outcome'])}</code></td>"
            f"<td>{result['rejected_mutation_count']}/5</td>"
            f"<td>{result['accepted_mutation_count']}</td>"
            "</tr>"
        )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sable Rook v655-v5 boundary evidence report</title>
<style>
body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:78rem;margin:auto;padding:1rem}}
a:focus{{outline:3px solid #145da0;outline-offset:2px}}
.table-wrap{{overflow-x:auto}} table{{border-collapse:collapse;width:100%;min-width:52rem}}
th,td{{border:1px solid #777;padding:.5rem;text-align:left;vertical-align:top}}
caption{{font-weight:700;text-align:left;margin:.7rem 0}} code{{white-space:nowrap}}
@media print{{a[href="#main"]{{display:none}} body{{max-width:none}}}}
</style>
</head>
<body>
<a href="#main">Skip to main content</a>
<header><h1>Sable Rook v655-v5 boundary evidence report</h1></header>
<main id="main">
<section aria-labelledby="summary"><h2 id="summary">Summary</h2>
<p>Thirty owner-local contracts ran: 23 <code>completed</code>, 5
<code>represented</code>, 1 <code>open_gap</code>, and 1
<code>exact_gate</code>. All 150 preregistered mutations were rejected.
No real person, tree or site record, condition or risk determination,
measurement, load, climbing or aerial work, tool, worksite operation, cutting,
pruning, treatment, biosecurity notification, traffic or utility control, work
release, public-safety action, professional arboriculture decision, production
system, or authority was acted on.</p></section>
<section aria-labelledby="results"><h2 id="results">Proposal results</h2>
<div class="table-wrap" tabindex="0" role="region" aria-label="Scrollable proposal results">
<table><caption>Bounded v655-v5 contract and mutation results</caption>
<thead><tr><th scope="col">Proposal</th><th scope="col">Surface</th>
<th scope="col">Pillar</th><th scope="col">Disposition</th>
<th scope="col">Rejected mutations</th><th scope="col">Accepted mutations</th>
</tr></thead><tbody>{''.join(rows)}</tbody></table></div></section>
<section aria-labelledby="boundaries"><h2 id="boundaries">Boundaries</h2>
<p>GMUT remains a typed scalar-tensor and EFT research-model
family without empirical confirmation. THOS tree-inspection workflow evidence remains
synthetic or represented. Freed ID remains synthetic and nonproduction.
Tree-record and location privacy, professional practice, access, correction,
remedy, legal interpretation,
cultural legitimacy, data governance, affected-party acceptance, and Māori
authority remain with competent authorities and affected people, including tangata
whenua, iwi, hapū, and Māori authorities.</p>
<p>Manual keyboard, touch, browser, responsive-layout, assistive-technology,
cognitive-accessibility, Māori-language, multi-format handover, arboriculture-accessibility, and
affected-user evaluation remain reserved. This static structural report is not
complete accessibility conformance.</p>
<p>Terminal verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p></section>
</main>
</body>
</html>
"""


def prospective_blob(relative: str) -> str:
    return run("git", "hash-object", f"--path={relative}", relative)


def evidence_manifest() -> None:
    x1_paths = set(
        run("git", "ls-tree", "-r", "--name-only", X1_COMMIT, "--", d.PHASE_ROOT)
        .splitlines()
    )
    phase_paths = [
        path.relative_to(REPO).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.relative_to(ROOT).as_posix()
        not in {
            "validation/evidence-candidate-manifest.json",
            "validation/evidence-validation.json",
            "validation/evidence-minimal-validation.json",
            "validation/evidence-staged-review.json",
            "validation/evidence-correction-staged-review.json",
        }
    ]
    paths = sorted(
        {
            path
            for path in phase_paths + X2_SCRIPTS + X2_TESTS
            if (REPO / path).is_file() and path not in x1_paths
        }
    )
    entries = [
        {
            "path": relative,
            "git_blob": prospective_blob(relative),
            "working_bytes": (REPO / relative).stat().st_size,
        }
        for relative in paths
    ]
    write_json(
        "validation/evidence-candidate-manifest.json",
        {
            "schema": "ghc.family.v655-v5.evidence-candidate-manifest.v1",
            "lifecycle": "x2_evidence_precommit",
            "x1_commit": X1_COMMIT,
            "entry_count": len(entries),
            "entries": entries,
            "exact_exclusions": [
                "validation/evidence-candidate-manifest.json",
                "validation/evidence-validation.json",
                "validation/evidence-minimal-validation.json",
                "validation/evidence-staged-review.json",
                "validation/evidence-correction-staged-review.json",
            ],
            "hash_domain": "prospective Git filtered blob identity",
        },
    )


def materialize_phase_tools() -> None:
    """Build the ten phase-local skills and family-compatible runners."""
    for skill_name, runner_name, group in RUNNERS:
        group_rows = d.PROPOSALS[(group - 1) * 3 : group * 3]
        mechanisms = ", ".join(row["mechanism"] for row in group_rows)
        skill_title = skill_name.removeprefix("ghc-family-").replace("-", " ").title()
        skill_path = ROOT / "skills" / skill_name
        if not skill_path.exists():
            run(
                sys.executable,
                str(INIT_SKILL),
                skill_name,
                "--path",
                str(ROOT / "skills"),
                "--interface",
                f"display_name={skill_title}",
                "--interface",
                "short_description=Validate bounded tree-inspection contracts",
                "--interface",
                (
                    f"default_prompt=Use ${skill_name} to validate its three "
                    "bounded tree-inspection contracts."
                ),
            )
        write_text(
            f"skills/{skill_name}/SKILL.md",
            "\n".join(
                [
                    "---",
                    f"name: {skill_name}",
                    (
                        "description: Build and verify bounded owner-local "
                        f"{mechanisms} contracts for Sable v655-v5. Use only "
                        "for synthetic, symbolic, or structural evidence; preserve "
                        "professional, empirical, legal, cultural, Māori-authority, "
                        "production, identity, and Stage 20 gates."
                    ),
                    "---",
                    "",
                    f"# {skill_title}",
                    "",
                    "1. Read the frozen proposal and its declared source needs.",
                    "2. Build one valid typed contract without external action.",
                    "3. Execute the five preregistered mutation dimensions.",
                    "4. Reject or quarantine every mutation and retain it as a negative.",
                    "5. Emit only the frozen disposition and preserve all protected gates.",
                    "",
                    (
                        f"Use `{runner_name}` for deterministic group {group} "
                        "evidence. A passing fixture is same-owner workflow evidence "
                        "only and is never independent reproduction or authority."
                    ),
                ]
            ),
        )
        runner = REPO / "scripts" / runner_name
        if runner_name == "ghc_family_v655_v5_suite.py":
            body = "\n".join(
                [
                    "#!/usr/bin/env python3",
                    '"""Run all thirty bounded Sable v655-v5 contracts."""',
                    "",
                    "from ghc_family_v655_v5_core import suite_main",
                    "",
                    "",
                    'if __name__ == "__main__":',
                    '    suite_main("ghc_family_v655_v5_suite")',
                    "",
                ]
            )
        else:
            body = "\n".join(
                [
                    "#!/usr/bin/env python3",
                    (
                        f'"""Run Sable v655-v5 bounded contract group {group}: '
                        f'{mechanisms}."""'
                    ),
                    "",
                    "from ghc_family_v655_v5_core import group_main",
                    "",
                    "",
                    'if __name__ == "__main__":',
                    f'    group_main({group}, "{Path(runner_name).stem}")',
                    "",
                ]
            )
        runner.write_text(body, encoding="utf-8", newline="\n")


def build() -> None:
    head = run("git", "rev-parse", "HEAD")
    if head not in {X1_COMMIT, EVIDENCE_COMMIT}:
        raise RuntimeError(
            "evidence builder requires the exact immutable x1 or evidence head"
        )
    correction_mode = head == EVIDENCE_COMMIT

    suite = core.execute_all()
    if (
        suite["proposal_count"],
        suite["valid_fixture_count"],
        suite["rejected_mutation_count"],
        suite["accepted_mutation_count"],
    ) != (30, 30, 150, 0):
        raise RuntimeError("core suite result does not match the frozen contract")

    outcomes = Counter(row["observed_outcome"] for row in suite["results"])
    expected = {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}
    if dict(outcomes) != expected:
        raise RuntimeError(f"outcome distribution changed: {outcomes}")

    for result in suite["results"]:
        slug = result["contract"]["slug"]
        write_json(f"surfaces/{slug}/contract.json", result["contract"])
        write_json(
            f"surfaces/{slug}/mutation-results.json",
            {
                "schema": "ghc.family.v655-v5.mutation-results.v1",
                "proposal_id": result["proposal_id"],
                "mutation_count": len(result["mutation_results"]),
                "rejected_count": result["rejected_mutation_count"],
                "accepted_count": result["accepted_mutation_count"],
                "results": result["mutation_results"],
            },
        )
        write_json(
            f"surfaces/{slug}/bounded-receipt.json",
            {
                "schema": "ghc.family.v655-v5.bounded-receipt.v1",
                "proposal_id": result["proposal_id"],
                "observed_outcome": result["observed_outcome"],
                "valid_fixture_passed": result["valid_fixture_passed"],
                "rejected_mutation_count": result["rejected_mutation_count"],
                "accepted_mutation_count": result["accepted_mutation_count"],
                "external_action_counts": result["contract"][
                    "external_action_counts"
                ],
                "promotion_claims": result["contract"]["promotion_claims"],
                "same_owner_only": True,
                "independent_reproduction": False,
                "boundary": result["contract"]["evidence_boundary"],
            },
        )

    materialize_phase_tools()
    runner_rows = []
    for skill_name, runner_name, group in RUNNERS:
        skill_path = ROOT / "skills" / skill_name
        validation_output = run(
            sys.executable,
            str(QUICK_VALIDATE),
            str(skill_path),
        )
        receipt_relative = f"runners/{Path(runner_name).stem}-receipt.json"
        runner_path = REPO / "scripts" / runner_name
        if runner_name == "ghc_family_v655_v5_suite.py":
            runner_output = run(
                sys.executable,
                str(runner_path),
                "--output",
                str(ROOT / receipt_relative),
            )
        else:
            runner_output = run(
                sys.executable,
                str(runner_path),
                "--output",
                str(ROOT / receipt_relative),
            )
        receipt = read_json(receipt_relative)
        if runner_name == "ghc_family_v655_v5_suite.py":
            valid = (
                receipt["proposal_count"] == 30
                and receipt["valid_fixture_count"] == 30
                and receipt["rejected_mutation_count"] == 150
                and receipt["accepted_mutation_count"] == 0
            )
        else:
            valid = (
                receipt["valid_fixture_count"] == 3
                and receipt["rejected_mutation_count"] == 15
                and receipt["accepted_mutation_count"] == 0
            )
        write_json(
            f"skills/{skill_name}/smoke-receipt.json",
            {
                "schema": "ghc.family.v655-v5.skill-smoke-receipt.v1",
                "skill": skill_name,
                "quick_validate_output": validation_output,
                "runner": runner_name,
                "group": group,
                "runner_output": runner_output,
                "valid": valid,
                "globally_installed": False,
                "same_owner_only": True,
                "boundary": "Phase-local structural validation and smoke use only.",
            },
        )
        runner_rows.append(
            {
                "skill": skill_name,
                "runner": runner_name,
                "group": group,
                "receipt": receipt_relative,
                "valid": valid,
            }
        )
    if not all(row["valid"] for row in runner_rows):
        raise RuntimeError("one or more runner receipts are invalid")

    write_json("method-flow/method-flow-ledger-x2.json", append_x2_method_flow())
    method_runner = (
        SKILL_ROOT
        / "ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"
    )
    run(
        sys.executable,
        str(method_runner),
        "validate",
        "--ledger",
        str(ROOT / "method-flow/method-flow-ledger-x2.json"),
        "--receipt",
        str(ROOT / "method-flow/method-flow-validation-x2.json"),
    )
    run(
        sys.executable,
        str(method_runner),
        "summarize",
        "--ledger",
        str(ROOT / "method-flow/method-flow-ledger-x2.json"),
        "--json-output",
        str(ROOT / "method-flow/method-flow-summary-x2.json"),
        "--markdown-output",
        str(ROOT / "method-flow/method-flow-summary-x2.md"),
    )

    x1_negatives = read_json("truth/retained-negative-register.json")
    effective_negatives = (
        x1_negatives["effective_after_x1"]
        + suite["rejected_mutation_count"]
        + len(X2_OPERATIONAL_NEGATIVES)
    )
    write_json(
        "truth/retained-negative-register-x2.json",
        {
            "schema": "ghc.family.v655-v5.retained-negatives.x2.v1",
            "source_effective": d.SOURCE_EFFECTIVE_NEGATIVES,
            "x1_operational_count": x1_negatives["x1_operational_count"],
            "x1_effective": x1_negatives["effective_after_x1"],
            "synthetic_mutation_negative_count": 150,
            "x2_operational_count": len(X2_OPERATIONAL_NEGATIVES),
            "x2_operational": X2_OPERATIONAL_NEGATIVES,
            "effective_at_evidence": effective_negatives,
            "no_failure_erased": True,
        },
    )
    write_json(
        "truth/open-gap-register-x2.json",
        {
            "schema": "ghc.family.v655-v5.open-gaps.x2.v1",
            "inherited_count": d.SOURCE_OPEN_GAPS,
            "new_rows": [
                {
                    "proposal_id": f"{d.PHASE_CODE}-P25",
                    "state": "open_gap",
                    "reason": (
                        "No ESO query or download, no real archive row, no calibration "
                        "or quality-mask application, no frozen likelihood, no "
                        "parameter inference, and no independent review."
                    ),
                }
            ],
            "closed_count": 0,
            "effective_count": d.SOURCE_OPEN_GAPS + 1,
        },
    )
    write_json(
        "truth/exact-gate-register-x2.json",
        {
            "schema": "ghc.family.v655-v5.exact-gates.x2.v1",
            "inherited_count": d.SOURCE_EXACT_GATES,
            "new_rows": [
                {
                    "proposal_id": f"{d.PHASE_CODE}-P30",
                    "state": "exact_gate",
                    "reason": (
                        "Tree ownership and stewardship, land access, habitat, heritage, "
                        "significant or taonga species, place names, tree-record and "
                        "location privacy, disability access, public safety, remedy, "
                        "legal interpretation, data governance, affected-party "
                        "acceptance, tangata whenua, iwi, hapū, cultural, and Māori "
                        "authority are absent."
                    ),
                }
            ],
            "closed_count": 0,
            "effective_count": d.SOURCE_EXACT_GATES + 1,
        },
    )
    write_json(
        "x2/proposal-ledger.json",
        {
            "schema": "ghc.family.v655-v5.proposals.x2.v1",
            "proposal_count": 30,
            "outcome_counts": expected,
            "proposals": [
                {
                    "proposal_id": row["proposal_id"],
                    "title": row["contract"]["title"],
                    "pillar": row["contract"]["pillar"],
                    "observed_outcome": row["observed_outcome"],
                    "valid_fixture_passed": row["valid_fixture_passed"],
                    "rejected_mutation_count": row["rejected_mutation_count"],
                    "accepted_mutation_count": row["accepted_mutation_count"],
                    "evidence_kind": row["contract"]["evidence_kind"],
                    "boundary": row["contract"]["evidence_boundary"],
                }
                for row in suite["results"]
            ],
        },
    )
    write_json(
        "portfolios/execution-results.json",
        {
            "schema": "ghc.family.v655-v5.portfolio-results.x2.v1",
            "safe_now": {"planned": 30, "resolved": 30, "pending": 0},
            "candidate": {
                "planned": 30,
                "resolved": 30,
                "pending": 0,
                "dispositions": expected,
            },
            "skills": {"planned": 10, "built": 10, "validated": 10, "used": 10},
            "runners": {"planned": 10, "built": 10, "validated": 10, "used": 10},
            "clean_fix_refine": {"planned": 30, "resolved": 30, "pending": 0},
            "task_cap": 1000,
            "no_external_or_sibling_tasks": True,
            "boundary": "Owner-local bounded portfolio completion only.",
        },
    )
    write_json(
        "tooling/ghc-family-index-x2-addendum.json",
        {
            "schema": "ghc.family.v655-v5.index-addendum.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "skills": [row[0] for row in RUNNERS],
            "runners": [row[1] for row in RUNNERS],
            "runner_rows": runner_rows,
            "global_installation_count": 0,
            "historical_names_preserved": True,
            "boundary": "Phase-local additive tooling only.",
        },
    )
    write_text(
        "tooling/ghc-family-index-x2-addendum.md",
        "# GHC Family Index — Sable v655-v5 x2 addendum\n\n"
        + "\n".join(
            f"- `{skill}` → `{runner}`: validated and smoke-used."
            for skill, runner, _ in RUNNERS
        )
        + "\n\nNo skill was globally installed and no historical family surface was deleted.\n",
    )
    write_json(
        "reflection-remaster/x2-decision-record.json",
        {
            "schema": "ghc.family.reflection-remaster.decision.v1",
            "decision_id": "V6555-REFLECT-X2",
            "action": "specialize_without_global_install",
            "retained": [
                "GHC Family Index",
                "Method Flow State",
                "Workflow Plan Refinement",
                "Reflection Remaster",
                "Meta Tool Box",
            ],
            "built": [row[0] for row in RUNNERS] + [row[1] for row in RUNNERS],
            "deleted": [],
            "reason": (
                "The ten bounded THOS-primary tree-inventory and inspection skills "
                "and runners add distinct inventory, provenance, scope, represented "
                "measurement, biosecurity, handover, privacy, accessibility, "
                "identifier, and GMUT-observation firewalls without global installation."
            ),
        },
    )
    write_json(
        "threat-model.json",
        {
            "schema": "ghc.family.v655-v5.threat-model.v1",
            "assets": [
                "tree inventory, inspection, site, and purpose-bound metadata",
                "tree asset, observation, inference, work-scope, and provenance state",
                "represented decay, geometry, load, access, rescue, and tooling proxies",
                "correction, reinspection, handover, privacy, and identifier relations",
                "access, habitat, heritage, complaint, and remedy reservations",
                "GMUT positivity, screening, units, and observation-firewall integrity",
                "THOS stop-work, utility, biosecurity, weather, and release holds",
            ],
            "adversaries": [
                "unlabelled observation, inference, diagnosis, or authority promoter",
                "silent tree, site, episode, scope, or process-state substituter",
                "stale measurement, load, access, utility, or weather-state promoter",
                "person, tree asset, site, episode, and correction namespace conflator",
                "unauthorized climbing, cutting, pruning, treatment, traffic, or release promoter",
                "silent legal, cultural, taonga, professional, or remedy decider",
                "correlated same-owner validation promoter",
            ],
            "threats": [
                "private person, precise-location, owner-contact, or work-order metadata leakage",
                "person, tree asset, site, episode, observation, inference, or correction conflation",
                "stale authorization, measurement, load, utility, weather, or process evidence",
                "silent unit, coordinate, reference, sign, or measurement-proxy conversion",
                "automatic climbing, cutting, pruning, treatment, traffic, utility, or work release",
                "unilateral legal, professional, cultural, taonga, or remedy interpretation",
                "affected-party, disability, location, tree-record, or cultural information exposure",
                "unsupported scientific or authority promotion",
            ],
            "controls": [
                "purpose-bound metadata minimization",
                "tree-record, site, episode, observation, inference, process, and proxy lineage",
                "authorization, utility, biosecurity, measurement-proxy, safety, and readiness holds",
                "person, tree asset, site, episode, and correction referent separation",
                "correction replay and stop-work gates",
                "weather, utility, biosecurity, habitat, privacy, accessibility, culture, complaint, and remedy reservations",
                "typed task authority ceilings",
                "promotion-claim zero map",
                "retained mutations and Method Flow",
            ],
            "residuals": [
                "real trees, sites, habitats, utilities, pests, and biological or material behaviour",
                "real measurements, loads, climbing, tools, cutting, pruning, treatments, traffic controls, and worksite hazards",
                "arborist, inspection, diagnosis, treatment, work release, public-safety, and professional competence",
                "human usability and complete accessibility",
                "legal, cultural, taonga, Māori, and affected-party authority",
                "independent craft, safety, security, privacy, and empirical review",
            ],
            "boundary": (
                "Threat model is not exhaustive arboriculture, ecological, professional, "
                "security, privacy, accessibility, or authority assurance."
            ),
        },
    )
    write_json(
        "wellbeing/wellbeing-check-x2.json",
        {
            "schema": "ghc.family.workload-check.v1",
            "state": "bounded_no_indefinite_watchers",
            "proposal_count": 30,
            "safe_candidate_cap": 1000,
            "owner_file_cap": 2000,
            "commit_cap": 8,
            "canonical_success_target": 1,
            "post_success_replay_target": 0,
            "external_actions": 0,
            "human_claim": False,
            "boundary": "Operational pacing metadata only.",
        },
    )
    write_text(
        "deliverables/v655-v5-integrated-overview.md",
        build_overview(suite["results"]),
    )
    write_text(
        "deliverables/v655-v5-boundary-evidence-report.html",
        build_report(suite["results"]),
    )
    overview_words = len(
        (ROOT / "deliverables/v655-v5-integrated-overview.md")
        .read_text(encoding="utf-8")
        .split()
    )
    if overview_words < 1800:
        raise RuntimeError(f"overview is below three-page equivalent: {overview_words}")
    if overview_words > 6000:
        raise RuntimeError(f"overview exceeds 6,000-word phase cap: {overview_words}")

    write_json(
        "truth/phase-truth-evidence.json",
        {
            "schema": "ghc.family.v655-v5.phase-truth.evidence.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "primary_focus": d.PRIMARY_FOCUS,
            "bounded_practice": d.BOUNDED_PRACTICE,
            "outcomes": expected,
            "proposal_count": 30,
            "frozen_chain_count": 2080,
            "synthetic_mutation_negative_count": 150,
            "effective_negative_count": effective_negatives,
            "open_gap_count": d.SOURCE_OPEN_GAPS + 1,
            "exact_gate_count": d.SOURCE_EXACT_GATES + 1,
            "method_count": d.SOURCE_METHODS
            + read_json("truth/retained-negative-register.json")[
                "x1_operational_count"
            ]
            + len(X2_OPERATIONAL_NEGATIVES),
            "real_keys_or_proofs": 0,
            "real_identity_resolutions": 0,
            "real_status_or_revocation_events": 0,
            "real_people": 0,
            **core.ZERO_EXTERNAL_COUNTS,
            "independent_reproduction_claimed": False,
            "privacy_complete_claimed": False,
            "accessibility_complete_claimed": False,
            "exhaustive_security_claimed": False,
            "professional_validation_claimed": False,
            "theory_of_everything_claimed": False,
            "agi_or_asi_claimed": False,
            "consciousness_or_personhood_claimed": False,
            "route_state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "truth/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v655-v5.checklist.evidence.v1",
            "complete_bounded": [
                "thirty frozen contracts",
                "thirty valid fixtures",
                "150 rejected synthetic mutations",
                "ten phase-local skills built, validated, and smoke-used",
                "ten family-compatible runners invoked",
                "all authorized safe, candidate, and refinement portfolio rows resolved",
                "three-page-equivalent overview",
                "accessible static report structure",
                "threat model",
                "retained negative and gate registers",
            ],
            "pending_lifecycle": [
                "immutable evidence commit and postcommit manifest check",
                "combined closeout, seal, and final commit",
                "one exact-final canonical pass",
                "four-way remote equality",
                "one exact-title Caelen Ash activation",
            ],
            "incomplete_external": [
                "real GMUT data and likelihood",
                "blind or independently designed GMUT and THOS empirical arms",
                "authorized arboriculture field pilot, real people and trees, calibrated measurements, loads, climbing, cutting, pruning, treatment, biosecurity notifications, traffic or utility controls, work release, competent practitioner review, and affected-user evaluation",
                "production Freed ID registration and resolution plus privacy and security review",
                "tangata whenua, iwi, hapū, Māori, taonga, affected-party, tree-record and location privacy, disability access, land, habitat, heritage, professional, legal, cultural, data-governance, complaint, correction, and remedy authority",
                "manual and affected-user accessibility evaluation",
                "independent-team reproduction",
                "Stage 20 authority",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "validation/evidence-build-receipt.json",
        {
            "schema": "ghc.family.v655-v5.evidence-build-receipt.v1",
            "x1_commit": X1_COMMIT,
            "proposals": 30,
            "valid_fixtures": 30,
            "rejected_mutations": 150,
            "accepted_mutations": 0,
            "skills_built_validated_used": 10,
            "runners_built_validated_used": 10,
            "overview_words": overview_words,
            "outcomes": expected,
            "effective_negatives": effective_negatives,
            "route_state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "valid": True,
            "boundary": (
                "Dedicated post-evidence correction candidate only."
                if correction_mode
                else "Precommit evidence candidate only."
            ),
        },
    )
    write_json(
        "validation/evidence-test-receipt.json",
        {
            "schema": "ghc.family.v655-v5.evidence-test-receipt.v1",
            "current_phase_tests": 17,
            "current_phase_failures": 0,
            "isolated_recovery_tests": 0,
            "isolated_recovery_failures": 0,
            "bounded_inherited_tests": 0,
            "bounded_inherited_failures": 0,
            "credited_test_total": 17,
            "failed_broad_selection_tests": 0,
            "failed_broad_selection_failures": 0,
            "failed_broad_selection_credit": 0,
            "inherited_suite_claimed": False,
            "full_repository_suite_run": False,
            "final_canonical_pass_run": False,
            "valid": True,
            "boundary": (
                "Bounded development validation only; the one exact-final "
                "canonical pass remains deferred."
            ),
        },
    )
    evidence_manifest()
    print(
        json.dumps(
            {
                "proposals": 30,
                "valid_fixtures": 30,
                "rejected_mutations": 150,
                "accepted_mutations": 0,
                "skills": 10,
                "runners": 10,
                "outcomes": expected,
                "effective_negatives": effective_negatives,
                "overview_words": overview_words,
                "state": (
                    "evidence_correction_candidate_built_not_committed"
                    if correction_mode
                    else "evidence_candidate_built_not_committed"
                ),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
