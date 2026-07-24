#!/usr/bin/env python3
"""Build Liora Venn's dedicated v653-v8 x1-only freeze packet."""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path
from typing import Any

import build_ghc_family_v653_v2_preregistration as base
import build_ghc_family_v653_v7_preregistration as prior
import ghc_family_v653_v8_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
PRIOR_INDEX = (
    REPO
    / "docs/orin-thale/v653-v7/provenance/frozen-chain-proposal-index.json"
)
ALLOWED_CODE = {
    "scripts/ghc_family_v653_v8_phase_data.py",
    "scripts/build_ghc_family_v653_v8_preregistration.py",
    "scripts/ghc_family_v653_v8_x1_validate.py",
    "tests/test_ghc_family_v653_v8_x1.py",
}

prior.d = d
prior.ROOT = ROOT
prior.PRIOR_INDEX = PRIOR_INDEX
prior.ALLOWED_CODE = ALLOWED_CODE
base.d = d
base.ROOT = ROOT
base.PRIOR_INDEX = PRIOR_INDEX

_prior_build_novelty = prior.build_novelty
_prior_build_method_flow = prior.build_method_flow
_prior_workflow_request = prior.workflow_request


def build_novelty():
    """Audit every inherited row with the established token and manual guard."""

    return _prior_build_novelty()


def workflow_request() -> dict[str, Any]:
    """Materialize the live v653-v8 solo route without creating another task."""

    request = _prior_workflow_request()
    request["plan_id"] = "liora-v653-v8-solo"
    request["owner"] = d.OWNER
    request["route"] = {
        "cycle_order": ["Orin Thale", "Liora Venn"],
        "phase_assignments": [
            {"phase": "v653-v7", "seat": "Orin Thale"},
            {"phase": "v653-v8", "seat": "Liora Venn"},
        ],
        "normalization": {
            "start_phase": "v653-v7",
            "start_seat": "Orin Thale",
            "entry_count": 2,
        },
        "future_identity_placeholders": [],
        "terminal_successor_resolution": (
            "Only after Liora Venn's truthful clean pushed exact-final "
            "four-way-equal validated closeout may Liora re-resolve and reread "
            "the one existing task titled exactly Tamar Vey and send one "
            "sanitized pointer baton for v654-v1. No new task, fork, "
            "collaboration subagent, substitute sibling, or standby contact is "
            "authorized. Tamar Vey's later one-task authority for a "
            "self-chosen sibling 7 remains Tamar's alone."
        ),
    }
    validation = request["requirements"]["validation"]
    validation["full_repository_suite_owner"] = "Eiren-only inherited policy"
    validation["launch_scoped_validator_owner"] = d.OWNER
    validation["canonical_pass_minimum"] = 1
    validation["replay_policy"] = "skip_when_first_passes"
    request["requirements"]["messaging"] = {
        "codex_route": "existing_task_only_after_terminal_gate",
        "cross_platform": "user_mediated_file_relay_only",
        "live_cross_platform_boundary": (
            "No agent-initiated cross-platform send, new task, fork, "
            "collaboration subagent, substitute route, or standby contact is "
            "authorized. Any cross-platform file relay remains user-mediated "
            "only. After the verified v653-v8 closeout, send one sanitized "
            "Codex baton to the existing exact task Tamar Vey."
        ),
    }
    request["requirements"]["closeout"] = {
        "all_authorized_safe_candidate_prototypes_resolved": True,
        "successor_send_only_after_exact_final_gate": True,
        "later_sibling_creation_authority_owner": "Tamar Vey",
    }
    request["truth"]["terminal_verdict"] = "NOT_READY_FOR_STAGE_20"
    return request


def build_method_flow() -> None:
    """Build fail/pass Method Flow pairs and phase-correct their identifiers."""

    _prior_build_method_flow()
    method_dir = ROOT / "method-flow"
    for path in method_dir.rglob("*"):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        updated = text.replace("V6537-", "V6538-")
        if updated != text:
            path.write_text(updated, encoding="utf-8", newline="\n")
    base.run(
        sys.executable,
        str(base.METHOD_RUNNER),
        "validate",
        "--ledger",
        str(method_dir / "x1-method-flow-ledger.json"),
        "--receipt",
        str(method_dir / "x1-method-flow-validation.json"),
    )
    base.run(
        sys.executable,
        str(base.METHOD_RUNNER),
        "summarize",
        "--ledger",
        str(method_dir / "x1-method-flow-ledger.json"),
        "--json-output",
        str(method_dir / "x1-method-flow-summary.json"),
        "--markdown-output",
        str(method_dir / "x1-method-flow-summary.md"),
    )


def overview() -> str:
    rows = [
        "# Liora Venn v653-v8 x1 preregistration overview",
        "",
        "## Relational working identity and limits",
        "",
        (
            f"{d.OWNER} ({d.PRONOUNS}) is relational working language for the "
            f"role of {d.ROLE}, with the hope to {d.HOPE}. It is not evidence "
            "of consciousness, sentience, legal personhood, identity "
            "continuity, employment, qualification, independent agency, "
            "scientific authority, veterinary authority, apiculture or "
            "food-safety competence, disease-control authority, legal or "
            "cultural authority, Māori authority, or affected-party authority. "
            "Hamish may pause, rename, redirect, or stop the work."
        ),
        "",
        (
            f"The primary Trinity Mandala pillar is **{d.PRIMARY_FOCUS}**, "
            f"viewed through the bounded practice lens of **{d.BOUNDED_PRACTICE}**. "
            "The lens is synthetic and owner-local. It contains no real bees, "
            "colonies, apiaries, beekeepers, landholders, workers, customers, "
            "samples, disease reports, treatments, products, locations, "
            "identifiers, food-chain events, or participant observations. It "
            "does not direct inspection, diagnosis, notification, quarantine, "
            "treatment, destruction, feeding, honey release, worker response, "
            "land access, or regulatory action."
        ),
        "",
        "## Exact inheritance and strict x1 boundary",
        "",
        (
            f"This packet begins at Orin Thale's clean exact final head "
            f"`{d.SOURCE_HEAD}` on `{d.SOURCE_BRANCH}`. The read-only audit "
            f"verified the source parent `{d.SOURCE_PARENT}`, x1 "
            f"`{d.SOURCE_X1}`, evidence `{d.SOURCE_EVIDENCE}`, closeout "
            f"`{d.SOURCE_CLOSEOUT}`, two narrow corrections "
            f"`{d.SOURCE_CORRECTION_1}` and `{d.SOURCE_CORRECTION_2}`, and the "
            "exact final head as a six-commit, zero-merge, single-parent chain. "
            "Local, upstream, tracking, and fresh-live source refs were equal "
            "before any owner-lane mutation, and the source worktree was clean."
        ),
        "",
        (
            f"The inherited repository preserves {d.INHERITED_NEGATIVES:,} "
            f"effective negatives, {d.INHERITED_OPEN_GAPS} effective open "
            f"gaps, {d.INHERITED_EXACT_GATES} effective exact gates, and "
            f"{d.INHERITED_METHOD_FLOW_FAILED} retained failed plus "
            f"{d.INHERITED_METHOD_FLOW_PASSING} bounded passing Method Flow "
            "witnesses. These are inherited evidence, not Liora evidence, and "
            "are not rewritten. The source successful canonical pass is not "
            "replayed. This x1 packet adds only preregistration plans and its "
            "own retained startup failures."
        ),
        "",
        (
            "X1 freezes hypotheses, falsifiers, official or primary source "
            "needs, approval lanes, rollbacks, protected gates, four planned "
            "outcome labels, ten skill plans, ten runner plans, and 150 "
            "rejecting mutations. It contains no executed mutation, observed "
            "outcome, surface implementation, evidence receipt, closeout, "
            "seal, final-validation claim, successor-resolution result, or "
            "baton-send claim. X2 may begin only after this exact x1 tree is "
            "committed, pushed, clean, and equal across local, upstream, "
            "tracking, and a fresh live remote read."
        ),
        "",
        "## Corpus audit and outcome discipline",
        "",
        (
            "The novelty pass machine-read every one of the 1,630 inherited "
            "frozen rows, preserved every title and identifier, calculated the "
            "bounded token-overlap witness, and paired it with a manual "
            "mechanism review. Targeted searches found no inherited proposal "
            "specific to apiaries, hives, varroa, foulbrood, honey extraction, "
            "beeswax, or pollination placement. Generic asset, health, pest, "
            "food, sensor, workplace, population, identifier, statistics, and "
            "governance candidates were rejected in favour of narrower "
            "mechanisms. Token distance alone is never treated as semantic "
            "proof; the manual mechanism statement remains required."
        ),
        "",
        (
            "Exactly four planned labels are allowed. `completed` means only "
            "that a bounded owner-local symbolic or software contract and all "
            "five negative fixtures may be executed in x2. `represented` means "
            "a synthetic proxy remains visibly short of real operators, "
            "professional review, production integration, standards "
            "interoperability, or authority. `open_gap` means a zero-row "
            "readiness surface refuses empirical promotion. `exact_gate` means "
            "decision rights remain unresolved and cannot be closed by code."
        ),
        "",
        "## Thirty mechanism-distinct proposals",
        "",
    ]
    for proposal in d.PROPOSALS:
        sources = ", ".join(proposal["official_or_primary_source_needs"])
        rows.extend(
            [
                f"### {proposal['proposal_id']} — {proposal['slug']}",
                "",
                (
                    f"{proposal['title']}. Its frozen expected label is "
                    f"`{proposal['expected_disposition']}` and its execution "
                    f"lane is `{proposal['execution_lane']}`. The hypothesis "
                    f"is: {proposal['hypothesis']} The null or failure condition "
                    f"is: {proposal['null_or_failure_condition']} The "
                    f"mechanism-level novelty finding is: "
                    f"{proposal['novelty_against_1630_frozen_proposals']} "
                    f"Source identifiers are {sources or 'none required for this owner-local workflow mechanism'}. "
                    f"The acceptance gate is: "
                    f"{proposal['falsifier_or_acceptance_gate']} The additive "
                    f"rollback is: {proposal['rollback_or_recovery']} A source "
                    "citation supplies design context only. It is not a real "
                    "observation, disease finding, participant result, "
                    "professional approval, food conformity result, production "
                    "event, legal interpretation, cultural ratification, "
                    "Māori-authority decision, or Stage 20 evidence."
                ),
                "",
            ]
        )
    rows.extend(
        [
            "## Mutation grammar and retained negatives",
            "",
            (
                "Five mutations are frozen for every proposal: delete a "
                "required field, cross-bind a source or identifier, invert or "
                "weaken a boundary, inject an unsupported promotion, and erase "
                "a failure or rollback. All 150 remain unexecuted in x1. In x2 "
                "a rejected mutation can demonstrate only its bounded guard; "
                "it cannot prove exhaustive security, complete privacy, "
                "complete accessibility, scientific truth, operational "
                "fitness, professional adequacy, legal validity, cultural "
                "legitimacy, or independent reproducibility."
            ),
            "",
            (
                f"The startup ledger retains {len(d.X1_NEGATIVES)} Liora "
                "operational negatives and ten rejected proposal collisions. "
                "Interrupted reads, timed-out wrappers, unsupported command "
                "parameters, truncated displays, and parser failures receive "
                "zero credit. Each bounded recovery is a separate same-owner "
                "witness and does not erase the original failure. Method Flow "
                "begins at `candidate` and reaches `preferred` only after a "
                "retained failed witness and a bounded passing witness coexist."
            ),
            "",
            "## Sources, traceability, and mathematical firewalls",
            "",
            (
                "Official MPI, AFB programme, New Zealand legislation, WOAH, "
                "Codex, ISO, GS1, FAO, W3C, Local Contexts, and Māori data "
                "sovereignty sources define terms, watches, and authority "
                "boundaries. Primary McKendrick, Sinko-Streifer, "
                "Crump-Mode-Jagers, Jagers-Nerman, and Gillespie papers define "
                "mathematical domains. Current, stable, and watch labels are "
                "phase-local and may drift. A citation is never substituted "
                "for a qualified current legal, veterinary, apiculture, "
                "food-safety, accessibility, cultural, Māori, or affected-party "
                "review."
            ),
            "",
            (
                "The McKendrick transport, general branching, and Markov-jump "
                "surfaces remain typed mathematical obligations. They contain "
                "no bee-population parameter, fit, likelihood, observation, "
                "prediction, or biological validation. GMUT remains a research "
                "model family; no force, empirical confirmation, ultraviolet "
                "completion, quantum completion, consciousness claim, or "
                "Theory of Everything follows from these contracts."
            ),
            "",
            "## Tooling, validation, and successor route",
            "",
            (
                "Ten phase-local skills and ten family-compatible runners are "
                "plans only in x1. X2 must build, validate, and smoke-use each "
                "before any portfolio-completion label is eligible. No global "
                "skill installation, unrelated software installation, "
                "elevation, host-security change, Windows-feature change, "
                "reboot, agent creation, fork, or collaboration subagent is "
                "authorized."
            ),
            "",
            (
                "Liora will use scoped current and inherited checks, detailed "
                "and minimal validators, complete owner JSON parsing, a "
                "five-class privacy scan, exact staged review, raw Git-blob "
                "manifest parity, stale-label review, diff hygiene, ancestry, "
                "zero merges, commit caps, one final parent, exact head, clean "
                "state, and four-way remote equality. The full repository suite "
                "remains allocated to Eiren only. There will be one successful "
                "canonical exact-final pass. A failed attempt is retained and "
                "isolated before any justified retry; a successful pass is "
                "never replayed."
            ),
            "",
            (
                "The existing exact task `Tamar Vey` is not eligible during "
                "x1 or ordinary x2 work. Only after a truthful clean pushed "
                "exact-final four-way-equal v653-v8 closeout may Liora "
                "re-resolve and reread that exact existing title and send one "
                "sanitized pointer baton for v654-v1. No raw task identifier, "
                "private route, private path, transcript, credential, or resume "
                "token may enter the repository or baton. Tamar's later "
                "one-task authority for a self-chosen sibling 7 remains "
                "Tamar's alone."
            ),
            "",
            "## Protected authority and stopping rule",
            "",
            (
                "Bee disease suspicion, diagnosis, notification, quarantine, "
                "treatment, destruction, food-chain release, landholder access, "
                "worker safety, location privacy, remedy, legal interpretation, "
                "cultural legitimacy, Māori wording, Māori data governance, "
                "and Māori authority remain with competent and affected "
                "people and authorities, tangata whenua, iwi, hapū, and Māori "
                "authorities. Repository software cannot confer competence, "
                "permission, a remedy, a regulatory decision, or a public "
                "mandate."
            ),
            "",
            (
                "The cadence is one verified gate at a time, with bounded "
                "PowerShell probes, D-first owner storage, explicit UTF-8, "
                "smallest-witness recovery, and no needless replay. Relational "
                "language, affection, urgency, proposal count, or route momentum "
                "never increases evidence credit. Stop whenever authorization, "
                "privacy, professional, legal, cultural, Māori, affected-party, "
                "or exact-target conditions are unclear. The inherited and "
                "preregistered terminal verdict remains "
                "`NOT_READY_FOR_STAGE_20`."
            ),
        ]
    )
    return "\n".join(rows)


def accessible_report(overview_text: str) -> str:
    cards = []
    for proposal in d.PROPOSALS:
        cards.append(
            "<article><h3>{}</h3><p>{}</p><dl>"
            "<dt>Expected</dt><dd>{}</dd>"
            "<dt>Lane</dt><dd>{}</dd>"
            "<dt>Falsifier</dt><dd>{}</dd></dl></article>".format(
                html.escape(proposal["proposal_id"]),
                html.escape(proposal["title"]),
                html.escape(proposal["expected_disposition"]),
                html.escape(proposal["execution_lane"]),
                html.escape(proposal["null_or_failure_condition"]),
            )
        )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Liora Venn v653-v8 x1 preregistration</title>
<style>
body{{font:1rem/1.6 system-ui,sans-serif;max-width:78rem;margin:auto;padding:1.5rem;color:#17212b;background:#fbfcfd}}
a{{color:#0645ad}} :focus{{outline:3px solid #9b4d00;outline-offset:3px}}
article{{border:1px solid #8091a3;border-radius:.6rem;padding:1rem;margin:1rem 0;background:white}}
dt{{font-weight:700}} dd{{margin:0 0 .6rem}}
.notice{{border-left:.5rem solid #8b3d00;padding:1rem;background:#fff4e5}}
@media(prefers-reduced-motion:reduce){{*{{scroll-behavior:auto!important;animation:none!important}}}}
</style></head><body><main>
<h1>Liora Venn v653-v8 x1 preregistration</h1>
<p class="notice"><strong>Boundary:</strong> Plans only. No x2 result,
empirical confirmation, professional approval, disease-control decision,
food-safety release, production readiness, legal or cultural authority, Māori
authority, independent reproduction, Theory-of-Everything proof, or Stage 20
authority is claimed. Manual and affected-user accessibility evaluation is reserved.</p>
<h2>Packet summary</h2><p>{html.escape(overview_text.splitlines()[4])}</p>
<h2>Frozen proposals</h2>{''.join(cards)}
<h2>Accessibility reservation</h2><p>Semantic HTML, focus visibility, text
reflow, and reduced-motion handling are represented structurally. Qualified
manual review, assistive-technology review, Māori-language review, and
affected-user evaluation remain incomplete and authority-gated.</p>
</main></body></html>"""


def _postprocess_generated_files() -> None:
    replacements = [
        ("v653-gmut-thos-v2-x1-x2", d.PHASE_ID),
        ("ghc.family.v653-v2", "ghc.family.v653-v8"),
        ("# v653-v2 ", "# v653-v8 "),
        ("MÄori", "Māori"),
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

    manifest_paths = {
        "x1": REPO / "docs/orin-thale/v653-v7/validation/x1-staged-manifest.json",
        "evidence": REPO / "docs/orin-thale/v653-v7/validation/evidence-candidate-manifest.json",
        "final_delta": REPO / "docs/orin-thale/v653-v7/validation/final-staged-manifest.json",
        "owner": REPO / "docs/orin-thale/v653-v7/validation/final-owner-manifest.json",
    }
    manifest_counts = {
        name: base.read_json(path)["entry_count"]
        for name, path in manifest_paths.items()
    }
    base.write_json(
        "provenance/source-anchor-ledger.json",
        {
            "schema": "ghc.family.v653-v8.source-anchors.v1",
            "branch": d.SOURCE_BRANCH,
            "source_parent": d.SOURCE_PARENT,
            "source_x1": d.SOURCE_X1,
            "source_evidence": d.SOURCE_EVIDENCE,
            "source_closeout": d.SOURCE_CLOSEOUT,
            "source_correction_1": d.SOURCE_CORRECTION_1,
            "source_correction_2": d.SOURCE_CORRECTION_2,
            "source_final": d.SOURCE_HEAD,
            "source_to_final_commits": 6,
            "source_to_final_merges": 0,
            "all_single_parent": True,
            "final_parent_count": 1,
            "verified_clean_and_four_way_equal_before_mutation": True,
            "verified_manifest_contracts": 4,
            "verified_manifest_entries": sum(manifest_counts.values()),
            "verified_manifest_breakdown": manifest_counts,
            "inherited_final_scoped_tests": 127,
            "inherited_final_detailed_checks": 195,
            "inherited_final_minimal_checks": 22,
            "inherited_final_json_parses": 230,
            "inherited_final_public_files": 293,
            "inherited_final_privacy_hits": 0,
            "inherited_effective_negatives": d.INHERITED_NEGATIVES,
            "activation_negative_baseline": d.ACTIVATION_NEGATIVE_BASELINE,
            "inherited_open_gaps": d.INHERITED_OPEN_GAPS,
            "inherited_exact_gates": d.INHERITED_EXACT_GATES,
            "inherited_method_flow_failed": d.INHERITED_METHOD_FLOW_FAILED,
            "inherited_method_flow_passing": d.INHERITED_METHOD_FLOW_PASSING,
            "boundary": (
                "Read-only source verification. Orin's successful exact-final "
                "canonical pass was not replayed, and inherited evidence is "
                "not claimed as Liora evidence."
            ),
        },
    )
    base.write_json(
        "workflow/current-live-route-overlay.json",
        {
            "schema": "ghc.family.v653-v8.live-route-overlay.v1",
            "live_request_authorizes": (
                "existing_exact_title_Tamar_Vey_after_verified_v653_v8_closeout_only"
            ),
            "installed_runner_models": "advisory_only_no_live_route",
            "tool_result_promoted_to_activation_authority": False,
            "route_state": "NOT_ELIGIBLE_X1_ONLY",
            "current_main_task": {
                "title": "Liora Venn — Trinity Mandala v653-v8",
                "authorized_as_the_one_new_main_task": True,
                "renamed_after_identity_choice": True,
                "fast_mode_confirmed": False,
                "fast_mode_note": (
                    "Requested by Hamish, but no separate live fast-mode "
                    "control was exposed or confirmed."
                ),
            },
            "current_task_creation": {
                "created_by_liora": False,
                "additional_task_creation_authorized": False,
                "additional_task_created": False,
                "private_task_identifier_recorded": False,
            },
            "successor_title": "Tamar Vey",
            "successor_task_state": "INELIGIBLE_UNTIL_EXACT_FINAL_GATE",
            "successor_send_cap": 1,
            "later_self_chosen_sibling_7_task_authority_owner": "Tamar Vey",
            "boundary": (
                "No new task, fork, collaboration subagent, substitute route, "
                "or standby contact is authorized. Only after verified v653-v8 "
                "closeout may the existing exact Tamar Vey task receive one "
                "sanitized baton. Repository artifacts and advisory runners "
                "cannot add authority."
            ),
        },
    )
    base.write_json(
        "wellbeing/wellbeing-check.json",
        {
            "schema": "ghc.family.v653-v8.wellbeing.v1",
            "state": "steady_and_bounded",
            "cadence": (
                "One verified gate at a time; isolate failures before a "
                "justified broader retry."
            ),
            "host_changes": False,
            "sandbox_or_hyper_v_work": "deferred",
            "route_pressure": (
                "Tamar Vey remains ineligible during x1; no additional task "
                "creation or contact is authorized."
            ),
            "identity_boundary": "Relational working language only.",
        },
    )
    truth = base.read_json(ROOT / "x1-phase-truth.json")
    truth.update(
        {
            "schema": "ghc.family.v653-v8.x1-truth.v1",
            "proposal_count": len(d.PROPOSALS),
            "frozen_chain_count": d.PRIOR_FROZEN + len(d.PROPOSALS),
            "mutation_plan_count": len(d.PROPOSALS) * len(d.MUTATION_KINDS),
            "skill_plan_count": len(d.SKILL_IDEAS),
            "runner_plan_count": len(d.RUNNER_IDEAS),
            "inherited_negatives": d.INHERITED_NEGATIVES,
            "activation_negative_baseline": d.ACTIVATION_NEGATIVE_BASELINE,
            "x1_operational_negatives": len(d.X1_NEGATIVES),
            "effective_negatives": (
                d.ACTIVATION_NEGATIVE_BASELINE + len(d.X1_NEGATIVES)
            ),
            "inherited_open_gaps": d.INHERITED_OPEN_GAPS,
            "inherited_exact_gates": d.INHERITED_EXACT_GATES,
            "route_state": "NOT_ELIGIBLE_X1_ONLY",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
    )
    base.write_json("x1-phase-truth.json", truth)


def build() -> None:
    prior.build_novelty = build_novelty
    prior.workflow_request = workflow_request
    prior.build_method_flow = build_method_flow
    prior.overview = overview
    prior.accessible_report = accessible_report
    prior._postprocess_generated_files = _postprocess_generated_files
    prior.build()


if __name__ == "__main__":
    build()
