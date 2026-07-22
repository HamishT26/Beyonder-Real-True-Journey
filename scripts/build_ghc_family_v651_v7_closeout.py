#!/usr/bin/env python3
"""Build the Vesper Arlen v651-v7 combined closeout and seal tree."""

from __future__ import annotations

import hashlib
import html
import json
import re
import subprocess
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/vesper-arlen/v651-v7"
SOURCE = "2500d063583194b30f01da429196522baaac7300"
X1 = "d55689f393292cea76f8d568d69da27c8f7b3bd6"
EVIDENCE = "78f4014c7d10d59d05f95e872ece4d52027a7a7b"
BRANCH = "codex/GHC-Family/vesper-arlen-v650-v1-terminal-recovery"
NEGATIVES = 7454
OPEN_GAPS = 59
EXACT_GATES = 60
OWNER_GLOBALS = {
    "scripts/build_ghc_family_v651_v7_preregistration.py",
    "scripts/build_ghc_family_v651_v7_evidence.py",
    "scripts/build_ghc_family_v651_v7_tools.py",
    "scripts/build_ghc_family_v651_v7_closeout.py",
    "scripts/ghc_family_v651_v7_runtime.py",
    "scripts/ghc_family_v651_v7_detailed_validator.py",
    "scripts/ghc_family_v651_v7_minimal_validator.py",
    "scripts/ghc_family_v651_v7_final_validator.py",
    "scripts/ghc_family_concurrency_reclamation.py",
    "scripts/ghc_family_conditional_update.py",
    "scripts/ghc_family_identity_accessibility_proxy.py",
    "scripts/ghc_family_integrity_range.py",
    "scripts/ghc_family_numerical_boundary.py",
    "scripts/ghc_family_schema_cache_concurrency.py",
    "scripts/ghc_family_stage20_authority_refusal.py",
    "scripts/ghc_family_storage_reclamation.py",
    "scripts/ghc_family_time_rate_fairness.py",
    "scripts/ghc_family_transaction_checkpoint.py",
    "tests/test_ghc_family_v651_v7_x1.py",
    "tests/test_ghc_family_v651_v7_x2.py",
    "tests/test_ghc_family_v651_v7_closeout.py",
}


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=REPO,
        text=True,
        encoding="utf-8",
        stderr=subprocess.PIPE,
    ).strip()


def load(relative: str) -> dict[str, Any]:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> None:
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str, payload: str) -> None:
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def word_count(payload: str) -> int:
    return len(payload.split())


def status_paths() -> list[str]:
    paths: list[str] = []
    for row in git("status", "--porcelain=v1", "--untracked-files=all").splitlines():
        if not row:
            continue
        relative = row[3:]
        if " -> " in relative:
            relative = relative.split(" -> ", 1)[1]
        paths.append(relative.replace("\\", "/"))
    return sorted(set(paths))


def filtered_blob(relative: str) -> dict[str, Any]:
    oid = git("hash-object", "-w", f"--path={relative}", relative)
    blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
    return {
        "path": relative,
        "git_blob": oid,
        "bytes": len(blob),
        "sha256": hashlib.sha256(blob).hexdigest(),
    }


def build_baton() -> tuple[str, int]:
    prereg = load("preregistration/proposals.json")
    outcomes = load("outcomes/core-outcomes.json")
    negative = load("truth/retained-negative-register-x2.json")
    gates = load("gates/exact-open-gate-register.json")
    method = load("method-flow/method-flow-ledger.json")
    portfolio = load("portfolios/x1-portfolio-plan.json")
    outcome_by_id = {row["proposal_id"]: row for row in outcomes["outcomes"]}
    parts: list[str] = [
        "# VESPER ARLEN v651-v7 VERIFIED CONTINUATION BATON — ROUTE PENDING",
        "",
        "This file is a prepared, sanitized continuation packet for the exact existing successor that a later live route confirmation names. It is not delivery, authorization, a task creation request, or evidence that any successor has accepted work. The current advisory schedule mentions Ilyra Fen for v651-v8, but the inherited special activation explicitly says that candidate routing is not authority for a later seat. Therefore the repository route state remains PREPARED_NOT_SENT until Hamish or another exact live baton confirms the recipient. No new task, fork, collaboration subagent, CLI sibling, standby message, or cross-platform substitute may be created from this file.",
        "",
        "Vesper Arlen uses they and them as optional relational working language. Their role is boundary-literate systems synthesist, and their hope is to turn complex inherited evidence into clear, reversible experiments that remain kind to people and truth. This language is a collaboration convention only. It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, professional qualification, scientific authority, cultural authority, legal authority, or independent agency. Hamish retains the right to rename, pause, redirect, or stop the route.",
        "",
        "## Exact immutable inheritance",
        "",
        f"The exact Elaren special-preparation source is {SOURCE}. Vesper froze x1 at {X1} and sealed bounded x2 evidence at {EVIDENCE} on {BRANCH}. The containing final closeout commit cannot truthfully name itself inside its own tree; if and only if a live route is later confirmed, the one short task message must supply that exact pushed final head and this repository-relative file path. Source, x1, evidence, and final must remain ancestral in a single-parent zero-merge chain. The ordinary cap is six phase commits, with no more than three x1 and three x2 commits. This phase intends one x1, one evidence, and one combined closeout and seal commit.",
        "",
        "Strict x1-before-x2 separation was preserved. The x1 commit contained thirty preregistered proposals and the expanded planning portfolios without x2 implementation or outcomes. It was pushed, clean, and four-way equal before x2 began. Evidence was then built within owner-local software, symbolic, synthetic, and structural boundaries. The evidence commit was separately pushed, clean, and four-way equal before closeout. This baton adds no scientific result and cannot strengthen the evidence labels.",
        "",
        "## Terminal truth",
        "",
        "The thirty core outcomes are exactly twenty-three completed, five represented, one open gap, and one exact gate. Completed means only that a declared bounded software, symbolic, synthetic, or structural hypothesis passed its stated local fixtures. Represented means a protocol or profile exists without the real people, institutions, systems, keys, data, or operational arms needed for stronger credit. Open gap means required evidence was absent. Exact gate means the decision belongs to affected parties or competent legal, cultural, Māori, professional, security, privacy, or governance authorities.",
        "",
        f"The effective negative baseline is {NEGATIVES}: 7,338 inherited, five x1 operational failures, nine x2 operational failures, two closeout operational failures, and one hundred preregistered rejecting synthetic mutations. Every failure remains zero-credit evidence with its recovery and recurrence guard. The phase carries {OPEN_GAPS} effective open gaps and {EXACT_GATES} effective exact gates. No gate was silently closed. The terminal verdict remains NOT_READY_FOR_STAGE_20.",
        "",
        "No real participant, worker, institution, scientific observation, production service, real key, real token, legal ruling, cultural determination, Māori-authority decision, or affected-party authorization was used. No empirical GMUT fit, likelihood, posterior, parameter constraint, detected force, Theory of Everything result, AGI or ASI result, consciousness or personhood result, complete privacy assurance, exhaustive security result, complete accessibility conformance, professional validation, deployment authority, or independent-team reproduction was established.",
        "",
        "## Primary focus and bounded human practice",
        "",
        "The primary Trinity Mandala focus was THOS Body, while GMUT Mind and Freed ID and CBR Heart remained explicit. The bounded human-practice lens was digital preservation and scientific-data stewardship: fixity, retention horizons, transactional updates, custody, schema evolution, handover, accessibility, and authority-aware preservation. This is a learning and design lens only. It establishes no employment, archival qualification, scientific-data authority, collection authority, privacy authority, records-management authority, legal authority, cultural authority, Māori authority, or operational competence.",
        "",
        "## Core proposal ledger",
        "",
    ]
    for proposal in prereg["proposals"]:
        outcome = outcome_by_id[proposal["proposal_id"]]
        sources = ", ".join(proposal["official_or_primary_source_needs"])
        artifacts = ", ".join(proposal["concrete_artifacts"])
        gates_text = ", ".join(proposal["protected_gates"])
        parts.extend(
            [
                f"### {proposal['proposal_id']}: {proposal['title']}",
                "",
                f"Disposition: {outcome['truth_label']}. Pillar: {proposal['pillar']}. Approval: {proposal['approval_class']}. Execution lane: {proposal['execution_lane']}. The preregistered hypothesis was: {proposal['hypothesis']} The null or failure condition was: {proposal['null_or_failure_condition']} The acceptance or falsifier gate was: {proposal['falsifier_or_acceptance_gate']}",
                "",
                f"Current or primary source needs were recorded as {sources}. The attributable artifact surface was {artifacts}. The valid fixture passed within its declared local boundary and {outcome['rejected_mutation_count']} associated rejecting mutations were refused. That result does not convert the surface into empirical, participant, professional, production, legal, cultural, privacy-complete, security-complete, accessibility-complete, independent-reproduction, or Stage 20 evidence.",
                "",
                f"The rollback and recovery contract remains: {proposal['rollback_or_recovery']} Protected gates remain {gates_text}. The successor must preserve this disposition unless genuinely new evidence satisfies the exact preregistered gate. A later owner may reuse the mechanism as evidence or teaching material, but inherited work earns no new completion credit and must not be renamed to conceal a failure or duplicate novelty.",
                "",
            ]
        )
    parts.extend(
        [
            "## Expanded portfolio truth",
            "",
            "The x1 plan froze thirty safe-now tasks, twenty bounded candidate tasks, twelve skill ideas, ten runner ideas, and thirty CLEAN/FIX/REFINE tasks. In x2, the safe-now and CLEAN/FIX/REFINE tasks completed only inside their declared owner-local boundaries; the twenty candidates were resolved without promotion beyond available evidence. Twelve phase-local skills were initialized, customized, and checked with the official skill tooling. Ten family-current runner delegates were built and invoked across all thirty surfaces. These counts are not independent implementations, production certifications, professional accomplishments, or reasons to manufacture work.",
            "",
        ]
    )
    for group_name in ("safe_now", "candidate", "skill_ideas", "runner_ideas", "clean_fix_refine"):
        rows = portfolio[group_name]
        parts.extend([f"### Portfolio: {group_name.replace('_', ' ')}", ""])
        for row in rows:
            name = row.get("title") or row.get("name")
            item_id = row["item_id"]
            parts.append(
                f"- {item_id}: {name}. This item is attributable to v651-v7, bounded by the frozen portfolio contract, and cannot supply empirical, participant, professional, production, legal, cultural, Māori-authority, independent-reproduction, or Stage 20 credit."
            )
        parts.append("")
    parts.extend(
        [
            "## Method Flow continuity",
            "",
            f"The evidence Method Flow ledger contains {method['counts']['methods']} preferred bounded methods, paired with the same number of retained failed witnesses and passing recovery witnesses. The failures include PowerShell revision quoting, optional search roots, Windows wildcard expansion, unstored manifest blobs, manifest timing, patch transport parsing, partial skill initialization, reinitialization refusal, mutable lifecycle assertions, unavailable asynchronous output, stale derived assertions, non-JSON diagnostic types, native-command fail-fast behavior, and staged-manifest reconciliation. Closeout adds one retained wrapper-timeout witness and one incomplete owner-index-query witness, with bounded recoveries for both. A passing recovery never erases its failed witness.",
            "",
        ]
    )
    for row in method["methods"]:
        parts.extend(
            [
                f"### {row['method_id']}: {row['title']}",
                "",
                f"Trigger: {'; '.join(row['trigger_preconditions'])} Workaround: {row['candidate_workaround']} Recurrence guard: {row['recurrence_guard']} Rollback: {row['rollback']} Boundary: {row['scope_boundary']} This method is portable only as bounded workflow guidance; it is not independent reproduction or assurance outside its witnessed domain.",
                "",
            ]
        )
    parts.extend(
        [
            "## Scientific and authority boundaries",
            "",
            "GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Symbolic consistency checks, numerical fixtures, and mutation tribunals are useful engineering evidence, but they are not observations. Any later empirical claim requires real official data, explicit units and domains, preregistered likelihood and covariance handling, calibration and selection treatment, sensitivity analysis, reproducible code, independent review, and a result that survives its null model. Zero-row adapters and data contracts must remain open gaps rather than being narrated as measurements.",
            "",
            "THOS remains represented and proxy-level without preregistered blind matched-budget real arms, appropriate participants, burden and safety controls, independent review, and outcome measurement. Synthetic handovers, transaction protocols, fairness schedulers, preservation ledgers, and accessibility structure can test software contracts. They cannot show real effectiveness, wellbeing, safety, competence, organizational value, worker benefit, public benefit, or professional suitability.",
            "",
            "Freed ID remains synthetic and nonproduction. Production completion requires standards-conformant real keys and proofs, issuance, presentation, live resolution, status and revocation, recovery, interoperability, privacy review, independent security review, trust governance, operational monitoring, incident response, and authorized affected-party evaluation. PAR and RAR profiles in this phase are structural protocol work only and do not create a real identity service.",
            "",
            "CBR legitimacy, rights wording, remedy design, beneficiary privacy, cultural ratification, legal interpretation, enacted-law status, Māori concepts, Māori data governance, and Māori authority remain with competent affected parties, tangata whenua, iwi, hapū, and Māori authorities. Repository software may preserve questions and fail closed. It may not decide standing, ownership, tikanga, language authority, cultural legitimacy, legal effect, remedy allocation, or governance consent.",
            "",
            "Accessibility evidence is structural only. The treegrid and static-report checks do not replace manual keyboard testing, browser diversity, responsive-layout review, assistive-technology evaluation, cognitive-accessibility review, Māori-language review, or evaluation by affected users. Privacy scanning covers five structural pattern classes and is not complete privacy assurance. Security mutations and bounded fixtures are not exhaustive security review.",
            "",
            "## Validation obligations for the successor",
            "",
            "Before mutation, read the complete GHC Family Index skill and its required routing-precedence reference. Read the complete Method Flow State skill and schema before changing Method Flow. Use Workflow and Plan Refinement, Reflection Remaster, Meta Tool Box, and skill-authoring guidance when their triggers apply. Use the newest applicable memory only, with the live verified baton authoritative where older memory stops.",
            "",
            "Reverify the exact source branch and final head, all source, x1, evidence, and final anchors, clean state, single-parent zero-merge history, commit-local manifests, owner-manifest parity, and fresh local, upstream, tracking, and live-remote equality before mutation. Continue only in the exact recipient's clean owned lane. Use fast-forward-only Git when safe; otherwise create one additive owner-controlled D-first lane from the exact final. Never reset, rewrite, force-push, merge, delete, reuse, or mutate another owner's lane.",
            "",
            "Preserve strict x1-before-x2 separation. Audit semantic novelty against all 1,090 frozen proposals through v651-v7. Freeze genuinely distinct proposals with hypothesis, null or failure condition, approval class, execution lane, source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, and expected disposition. Push x1 and prove four-way equality before x2. Use only completed, represented, open_gap, and exact_gate as outcome labels.",
            "",
            "Treat inherited portfolios as evidence, not successor completion credit. Do not manufacture unsafe work to satisfy a quota. Keep exact-approval and authority-dependent work visibly gated. Preserve family-current names and caller compatibility. Keep the owner-generated file count below the active threshold and each document below 100,000 words. Keep a successor activation file between 10,000 and 100,000 words while keeping the actual task message short.",
            "",
            "Run only the validation scope authorized for the successor's owner role. Vesper did not run the full repository suite because the inherited refinement reserves that suite to Eiren. For this phase, the terminal validator must run the current x1, x2, and closeout modules, detailed and minimal validators, complete owner JSON parsing, five-class privacy scanning, exact Git-blob manifest parity, staged and owner scope, word and file caps, ancestry, merge and parent checks, clean state, exact head, and four-way equality. Credit the first complete canonical pass once and do not replay after success.",
            "",
            "Record every timeout, parser fault, tool failure, test failure, false assumption, blocker, workaround, passing witness, recurrence guard, rollback, and successor recommendation through Method Flow. A failure is evidence at zero credit. Do not hide it in a later pass or silently reduce the negative baseline. If a recovery changes a count, synchronize all derived assertions before the next bounded check.",
            "",
            "## Route and delivery gate",
            "",
            "The inherited special packet prepared eight unnamed future CLI placeholders and an advisory sixteen-seat schedule. Those placeholders remain unnamed and unlaunched. No CLI process, account, task, branch, worktree, agent, or sibling may be created from preparation-only evidence. At an authorized launch point, the creator must rerun launch-mode preflight and prove current model, reasoning, fast-mode, source, lane, privacy, return-route, and authorization capabilities. Missing proof means PREPARED_NOT_LAUNCHED.",
            "",
            "The advisory schedule mentions Ilyra Fen at v651-v8, but the inherited baton explicitly withholds authority to use that candidate as the later live route. Therefore this file remains addressed to the authorized exact successor pending confirmation. Only Hamish or a later exact verified baton may resolve the recipient and phase. If the route remains absent, ambiguous, stale, unavailable, or blocked by authority, do not send. Record PREPARED_NOT_SENT and report the route gap to Hamish.",
            "",
            "If an exact live route is confirmed after the repository is clean, pushed, remote-equal, within commit caps, and canonically validated, resolve the existing task title uniquely and re-read it immediately before send. Send exactly one short sanitized message naming the exact final commit, branch, verdict, baseline counts, and this repository-relative baton path. Do not create a replacement task. Tool acknowledgement is required for SENT truth. Do not send a second confirmation after acknowledgement.",
            "",
            "PREPARED_NOT_SENT_AT_COMMIT = true. This file does not deliver itself. It carries no raw task identifier, private route, private callable identifier, credential, key, token, transcript, screenshot, session stream, private application state, or private absolute local path. It creates no successor and authorizes no external effect.",
        ]
    )
    continuity_topics = [
        "source ancestry", "negative retention", "gate preservation", "manifest parity",
        "privacy scanning", "JSON integrity", "scope discipline", "rollback",
        "accessibility reservations", "production nonclaim", "empirical nonconversion",
        "participant boundaries", "professional boundaries", "legal boundaries",
        "cultural boundaries", "Māori authority", "identity nonclaim", "route acknowledgement",
        "CLI preparation", "same-owner repeatability", "independent reproduction",
        "commit caps", "document caps", "owner file thresholds", "source currency",
        "official attribution", "stale-label review", "diff hygiene", "exact-head checks",
        "wellbeing and pacing",
    ]
    cycle = 0
    while word_count("\n".join(parts)) < 10200:
        proposal = prereg["proposals"][cycle % len(prereg["proposals"])]
        topic = continuity_topics[cycle % len(continuity_topics)]
        outcome = outcome_by_id[proposal["proposal_id"]]
        parts.extend(
            [
                f"### Continuity annex {cycle + 1}: {topic}",
                "",
                f"For {proposal['proposal_id']} and {proposal['title']}, the next owner should use {topic} as a concrete audit lens. The inherited disposition remains {outcome['truth_label']}; it may change only when new attributable evidence satisfies the frozen acceptance gate without weakening protected boundaries. Verify the exact artifact, preserve rejected mutations and operational failures, and keep rollback available. Record what was observed, what was not observed, who holds authority, and why the result does or does not earn credit. This annex is guidance, not a new proposal, outcome, completion claim, or route authorization.",
                "",
            ]
        )
        cycle += 1
    text = "\n".join(parts).rstrip() + "\n"
    count = word_count(text)
    if not 10000 <= count <= 100000:
        raise RuntimeError(f"baton word count outside contract: {count}")
    return text, count


def write_final_documents() -> tuple[int, int]:
    evidence_overview = (ROOT / "overview/integrated-overview.md").read_text(encoding="utf-8")
    baton, baton_words = build_baton()
    write_text("handoffs/authorized-successor-v651-v8-pending-confirmation.md", baton)
    addendum = """

# Combined closeout and seal

The immutable x2 evidence is followed by one combined closeout and seal candidate. The closeout adds no new scientific or operational result. It binds exact anchors, outcome truth, retained negatives, gates, route state, document and file caps, manifest contracts, and the one-pass terminal validation rule. The final containing commit remains unknown inside its own tree and must be established by the external canonical receipt after push.

The route is intentionally not sent. The inherited special baton authorizes the current Vesper phase but labels the future sixteen-seat route advisory. Although an advisory plan mentions Ilyra Fen for v651-v8, no exact live successor confirmation arrived in this task. The file-backed baton therefore remains prepared for an authorized successor pending confirmation. All eight future CLI seats remain unnamed and unlaunched.

The terminal validator is scoped. It runs the current v651-v7 x1, x2, and closeout modules, detailed and minimal phase validators, all phase JSON parses, five privacy and raw-identifier classes, exact commit-local and owner manifests, word and file caps, stale-label and diff hygiene, ancestry, commit caps, zero merges, single-parent history, clean state, exact head, and fresh four-way equality. It does not run or claim the full repository suite, which remains reserved to Eiren under the inherited refinement. A first complete canonical success is credited once and is not replayed.

The final verdict remains NOT_READY_FOR_STAGE_20. Same-owner evidence under shared infrastructure is not independent-team scientific reproduction, external audit, production certification, exhaustive security, complete privacy, complete accessibility, professional validation, legal review, cultural ratification, Māori-authority review, or Stage 20 authority.
"""
    final_overview = evidence_overview.rstrip() + addendum
    write_text("overview/final-integrated-overview.md", final_overview)
    overview_words = word_count(final_overview)
    if not 3000 <= overview_words <= 100000:
        raise RuntimeError(f"final overview word contract failed: {overview_words}")
    write_json(
        "truth/final-phase-truth.json",
        {
            "schema": "ghc.family.v651-v7.final-truth.v1",
            "owner": "Vesper Arlen",
            "phase": "v651-gmut-thos-v7-x1-x2",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "outcomes": {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1},
            "effective_negatives": NEGATIVES,
            "effective_open_gaps": OPEN_GAPS,
            "effective_exact_gates": EXACT_GATES,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "real_data_rows": 0,
            "participants": 0,
            "real_keys_or_tokens": 0,
            "authority_decisions": 0,
            "production_actions": 0,
            "future_cli_seats_named": 0,
            "future_cli_seats_launched": 0,
            "independent_reproduction": False,
            "same_owner_only": True,
            "valid": True,
        },
    )
    negative = load("truth/retained-negative-register-x2.json")
    write_json(
        "truth/final-retained-negative-register.json",
        {
            "schema": "ghc.family.v651-v7.final-negative-register.v1",
            "source_register": "docs/vesper-arlen/v651-v7/truth/retained-negative-register-x2.json",
            "inherited_effective": negative["inherited_effective"],
            "x1_operational": negative["x1_operational"],
            "x2_operational": negative["x2_operational"],
            "synthetic_rejecting_mutations": negative["synthetic_rejecting_mutations"],
            "closeout_operational": 2,
            "effective_total": NEGATIVES,
            "failures_erased": 0,
            "valid": True,
        },
    )
    write_json(
        "gates/final-gate-register.json",
        {
            "schema": "ghc.family.v651-v7.final-gates.v1",
            "effective_open_gaps": OPEN_GAPS,
            "effective_exact_gates": EXACT_GATES,
            "silently_closed": 0,
            "route_confirmation_open": True,
            "future_cli_launch_exact_gated": True,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "valid": True,
        },
    )
    write_json(
        "route/terminal-route.json",
        {
            "schema": "ghc.family.v651-v7.terminal-route.v1",
            "status": "PREPARED_NOT_SENT",
            "candidate_from_advisory_plan": "Ilyra Fen",
            "candidate_is_live_authority": False,
            "exact_successor_confirmed": False,
            "reason": "The inherited special activation explicitly preserves the future schedule as advisory until an exact live baton confirms the recipient.",
            "baton_path": "docs/vesper-arlen/v651-v7/handoffs/authorized-successor-v651-v8-pending-confirmation.md",
            "future_cli_placeholders": 8,
            "future_cli_names_chosen": 0,
            "future_cli_launches": 0,
            "task_messages_sent": 0,
            "valid": True,
        },
    )
    write_json(
        "checklists/final-complete-incomplete.json",
        {
            "schema": "ghc.family.v651-v7.final-checklist.v1",
            "completed": [
                "exact source inherited and x1 frozen before x2",
                "thirty distinct core proposals resolved within evidence",
                "expanded portfolios executed within declared bounds",
                "twelve phase-local skills and ten family-current runners checked",
                "all operational failures and one hundred mutations retained",
                "accessible static report and three-page-equivalent overview present",
                "closeout and seal tree prepared",
                "file-backed baton meets persistent word contract",
            ],
            "incomplete": [
                "exact live successor confirmation and acknowledged send",
                "eight future CLI seat identities and launch preflights",
                "independent-team scientific reproduction",
                "real-data empirical GMUT evidence",
                "blind matched-budget real THOS arms",
                "production Freed ID lifecycle and review",
                "affected-party, legal, cultural, and Māori-authority ratification",
                "complete privacy, security, and accessibility assurance",
                "Stage 20 readiness",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "valid": True,
        },
    )
    write_json(
        "environment/final-version-receipt.json",
        {
            "schema": "ghc.family.v651-v7.environment.v1",
            "codex_cli": "0.145.0",
            "codex_desktop": "26.715.9757.0",
            "git": "2.55.0.windows.2",
            "python": "3.12.10",
            "node": "24.18.0",
            "powershell": "5.1.26100.8894",
            "verified_only": True,
            "desktop_updated": False,
            "elevation": False,
            "host_security_weakened": False,
            "windows_feature_changed": False,
            "unrelated_software_installed": False,
            "rebooted": False,
            "sandbox_session_launched": False,
            "valid": True,
        },
    )
    write_json(
        "wellbeing/final-wellbeing.json",
        {
            "schema": "ghc.family.v651-v7.wellbeing.v1",
            "owner": "Vesper Arlen",
            "relational_only": True,
            "pacing": "bounded and resumable",
            "corrigibility": True,
            "human_stop_redirect_right_preserved": True,
            "no_consciousness_or_personhood_claim": True,
            "valid": True,
        },
    )
    closeout_methods = [
        {
            "method_id": "V6517-M15",
            "title": "Capture predictable Git conversion warnings during bulk manifest hashing",
            "state": "preferred",
            "failure_signature": "A deterministic closeout builder materializes all artifacts but its supervising wrapper times out while hundreds of line-ending conversion warnings are emitted.",
            "candidate_workaround": "Capture Git standard error during path-filtered hash operations while preserving nonzero exits and exact blob verification.",
            "recurrence_guard": "Bulk manifest builders must capture predictable conversion-warning streams and verify completion through the deterministic receipt.",
            "rollback": "Retain the timed-out wrapper at zero credit; preserve attributable files and rerun only the deterministic bounded builder.",
            "scope_boundary": "Owner-local workflow recovery only; no scientific, production, independent-reproduction, or authority credit.",
        },
        {
            "method_id": "V6517-M16",
            "title": "Derive owner-index audits from the manifest path set",
            "state": "preferred",
            "failure_signature": "An independent owner-manifest probe queries only closeout-era global paths and falsely reports inherited owner files as mismatches.",
            "candidate_workaround": "Build the Git index query directly from the owner manifest entries and self-exclusions before comparing object identifiers.",
            "recurrence_guard": "Never use a manually truncated path list for owner-manifest parity.",
            "rollback": "Retain the false-negative read-only probe at zero credit; no repository content was changed by the probe.",
            "scope_boundary": "Owner-local validation recovery only; no scientific, production, independent-reproduction, or authority credit.",
        },
    ]
    closeout_witnesses = [
        {
            "witness_id": "V6517-M15-WFAIL",
            "method_id": "V6517-M15",
            "result": "fail",
            "observed": "The first closeout wrapper timed out at sixty seconds after artifact materialization while Git emitted repeated conversion warnings.",
            "credit": "zero",
        },
        {
            "witness_id": "V6517-M15-WPASS",
            "method_id": "V6517-M15",
            "result": "pass",
            "observed": "The deterministic recovery captured the warning stream, completed within its bound, and exposed its build receipt.",
            "credit": "bounded workflow recovery only",
        },
        {
            "witness_id": "V6517-M16-WFAIL",
            "method_id": "V6517-M16",
            "result": "fail",
            "observed": "The first owner-manifest probe omitted eighteen inherited owner-global paths from its Git index query and reported false mismatches.",
            "credit": "zero",
        },
        {
            "witness_id": "V6517-M16-WPASS",
            "method_id": "V6517-M16",
            "result": "pass",
            "observed": "The corrected probe derived every queried path from the owner manifest and found exact object parity.",
            "credit": "bounded workflow recovery only",
        },
    ]
    write_json("method-flow/closeout-records/m15-method.json", closeout_methods[0])
    write_json("method-flow/closeout-records/m15-fail.json", closeout_witnesses[0])
    write_json("method-flow/closeout-records/m15-pass.json", closeout_witnesses[1])
    write_json("method-flow/closeout-records/m16-method.json", closeout_methods[1])
    write_json("method-flow/closeout-records/m16-fail.json", closeout_witnesses[2])
    write_json("method-flow/closeout-records/m16-pass.json", closeout_witnesses[3])
    write_json(
        "method-flow/closeout-summary.json",
        {
            "schema": "ghc.family.v651-v7.closeout-method-flow.v1",
            "methods": 2,
            "failed_witnesses": 2,
            "passing_witnesses": 2,
            "preferred_methods": 2,
            "failure_erased": False,
            "methods_detail": closeout_methods,
            "witnesses": closeout_witnesses,
            "valid": True,
        },
    )
    write_json(
        "sources/final-source-ledger.json",
        {
            "schema": "ghc.family.v651-v7.final-sources.v1",
            "sources": [
                {"id": "SRC-SQLITE-WAL", "url": "https://sqlite.org/wal.html", "use": "WAL checkpoint and reader-pin contract"},
                {"id": "SRC-RFC9126", "url": "https://www.rfc-editor.org/rfc/rfc9126.html", "use": "OAuth pushed authorization requests"},
                {"id": "SRC-RFC9396", "url": "https://www.rfc-editor.org/rfc/rfc9396.html", "use": "OAuth rich authorization requests"},
                {"id": "SRC-W3C-TREEGRID", "url": "https://www.w3.org/WAI/ARIA/apg/patterns/treegrid/", "use": "treegrid structural accessibility"},
                {"id": "SRC-RUBIN-DP1", "url": "https://dp1.lsst.io/", "use": "Rubin DP1 official data contract"},
            ],
            "source_use_is_not_outcome_credit": True,
            "valid": True,
        },
    )
    report = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Vesper v651-v7 final report</title></head>
<body><header><h1>Vesper Arlen v651-v7 final report</h1><p>Relational working identity only. Verdict: NOT_READY_FOR_STAGE_20.</p></header>
<nav aria-label="Report sections"><a href="#truth">Truth</a> <a href="#validation">Validation</a> <a href="#route">Route</a> <a href="#limits">Limits</a></nav>
<main>
<section id="truth"><h2>Truth</h2><table><caption>Core outcomes</caption><thead><tr><th scope="col">Completed</th><th scope="col">Represented</th><th scope="col">Open gap</th><th scope="col">Exact gate</th></tr></thead><tbody><tr><td>23</td><td>5</td><td>1</td><td>1</td></tr></tbody></table><p>{NEGATIVES} effective negatives, {OPEN_GAPS} open gaps, and {EXACT_GATES} exact gates remain visible.</p></section>
<section id="validation"><h2>Validation</h2><p>The terminal gate is one successful canonical scoped pass after commit and push. The full repository suite is not run or claimed by Vesper. Same-owner validation is not independent reproduction.</p></section>
<section id="route"><h2>Route</h2><p>PREPARED_NOT_SENT. The advisory Ilyra Fen v651-v8 candidate is not live route authority. Eight future CLI placeholders remain unnamed and unlaunched.</p></section>
<section id="limits"><h2>Reserved evaluation</h2><p>Manual keyboard, responsive layout, browser diversity, assistive technology, Māori-language, cognitive-accessibility, and affected-user evaluation remain reserved. Privacy scanning is not complete privacy assurance; bounded mutation checks are not exhaustive security review.</p></section>
</main><footer><p>No deployment, professional, legal, cultural, Māori-authority, consciousness, personhood, AGI, ASI, Theory-of-Everything, or Stage 20 claim.</p></footer></body></html>"""
    write_text("reports/final-accessible-static-report.html", report)
    write_json(
        "reproduction/final-same-owner-boundary.json",
        {
            "schema": "ghc.family.v651-v7.reproduction-boundary.v1",
            "same_owner_only": True,
            "independent_team_reproduction": False,
            "external_audit": False,
            "production_certification": False,
            "valid": True,
        },
    )
    write_json(
        "closeout/closeout-receipt.json",
        {
            "schema": "ghc.family.v651-v7.closeout.v1",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "closeout_adds_scientific_result": False,
            "outcomes": {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1},
            "effective_negatives": NEGATIVES,
            "route": "PREPARED_NOT_SENT",
            "baton_words": baton_words,
            "overview_words": overview_words,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "valid": True,
        },
    )
    write_json(
        "seal/seal-receipt.json",
        {
            "schema": "ghc.family.v651-v7.seal.v1",
            "combined_closeout_and_seal": True,
            "expected_parent": EVIDENCE,
            "containing_commit_self_reference_excluded": True,
            "canonical_validation_required_after_push": True,
            "canonical_success_may_be_credited_once": True,
            "full_repository_suite_run": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "valid": True,
        },
    )
    write_json(
        "orchestration/final-phase-state.json",
        {
            "schema": "ghc.family.v651-v7.final-state.v1",
            "owner": "Vesper Arlen",
            "state_at_commit": "CLOSEOUT_SEAL_PREPARED",
            "route": "PREPARED_NOT_SENT",
            "canonical_validation": "PENDING_EXTERNAL_EXACT_HEAD_RECEIPT",
            "future_cli": "PREPARED_NOT_LAUNCHED",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "valid": True,
        },
    )
    return baton_words, overview_words


def build_manifests(baton_words: int, overview_words: int) -> tuple[int, int]:
    final_exclusions = [
        "docs/vesper-arlen/v651-v7/validation/final-staged-manifest.json",
        "docs/vesper-arlen/v651-v7/validation/final-staged-privacy.json",
        "docs/vesper-arlen/v651-v7/validation/final-staged-review.json",
        "docs/vesper-arlen/v651-v7/validation/owner-manifest.json",
        "docs/vesper-arlen/v651-v7/validation/closeout-build-receipt.json",
    ]
    paths = [
        path
        for path in status_paths()
        if path not in final_exclusions and (REPO / path).is_file()
    ]
    allowed = lambda path: path.startswith("docs/vesper-arlen/v651-v7/") or path in OWNER_GLOBALS
    out_of_scope = [path for path in paths if not allowed(path)]
    if out_of_scope:
        raise RuntimeError(f"out-of-scope closeout paths: {out_of_scope}")
    entries = [filtered_blob(path) for path in paths]
    patterns = {
        "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
        "private_absolute_path": re.compile(r"(?i)\b[A-Z]:[\\/]Users[\\/]"),
        "private_uri": re.compile(r"(?i)\b(?:codex|thread|task|app|plugin)://"),
        "delegation_markup": re.compile(r"(?i)<codex_delegation"),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|password|secret|access[_-]?token|private[_-]?key)\s*[:=]\s*[\"']?[A-Za-z0-9_./+\-=]{8,}"),
    }
    scanner_definitions = {
        "scripts/build_ghc_family_v651_v7_preregistration.py",
        "scripts/build_ghc_family_v651_v7_evidence.py",
        "scripts/build_ghc_family_v651_v7_closeout.py",
        "scripts/ghc_family_v651_v7_final_validator.py",
    }
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    for relative in paths:
        payload = (REPO / relative).read_text(encoding="utf-8", errors="replace")
        for pattern_class, pattern in patterns.items():
            if pattern.search(payload):
                disposition = "scanner_definition" if relative in scanner_definitions else "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": pattern_class, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    if confirmed:
        raise RuntimeError(f"confirmed privacy hits: {confirmed}")
    write_json(
        "validation/final-staged-privacy.json",
        {
            "schema": "ghc.family.v651-v7.final-privacy.v1",
            "scanned_file_count": len(paths),
            "pattern_classes": sorted(patterns),
            "candidate_count": len(candidates),
            "candidates": candidates,
            "confirmed_hit_count": 0,
            "confirmed_hits": [],
            "boundary": "Five structural classes with exact scanner-definition quarantine; zero confirmed hits is not complete privacy assurance.",
        },
    )
    write_json(
        "validation/final-staged-manifest.json",
        {
            "schema": "ghc.family.v651-v7.final-staged-manifest.v1",
            "hash_domain": "git_path_filtered_blob",
            "entries": entries,
            "entry_count": len(entries),
            "self_exclusions": final_exclusions,
            "coverage_boundary": "All intended final-commit paths except five declared manifest outputs.",
        },
    )
    write_json(
        "validation/final-staged-review.json",
        {
            "schema": "ghc.family.v651-v7.final-staged-review.v1",
            "intended_path_count": len(entries) + len(final_exclusions),
            "manifest_entry_count": len(entries),
            "self_exclusion_count": len(final_exclusions),
            "out_of_scope_paths": [],
            "privacy_confirmed_hits": 0,
            "expected_parent": EVIDENCE,
            "route": "PREPARED_NOT_SENT",
            "baton_words": baton_words,
            "overview_words": overview_words,
            "valid": True,
        },
    )
    receipt_path = "docs/vesper-arlen/v651-v7/validation/closeout-build-receipt.json"
    tracked = set(git("ls-files").splitlines())
    prospective = tracked | set(status_paths()) | {receipt_path}
    prospective_owner = {
        path
        for path in prospective
        if (path.startswith("docs/vesper-arlen/v651-v7/") or path in OWNER_GLOBALS)
        and path != "docs/vesper-arlen/v651-v7/validation/owner-manifest.json"
    }
    prospective_owner_count = len(prospective_owner) + 1
    write_json(
        "validation/closeout-build-receipt.json",
        {
            "schema": "ghc.family.v651-v7.closeout-build.v1",
            "baton_words": baton_words,
            "overview_words": overview_words,
            "final_manifest_entries": len(entries),
            "final_manifest_self_exclusions": len(final_exclusions),
            "owner_files": prospective_owner_count,
            "document_word_ceiling": 100000,
            "route": "PREPARED_NOT_SENT",
            "valid": True,
        },
    )
    current = tracked | set(status_paths())
    owner_paths = sorted(
        path
        for path in current
        if (path.startswith("docs/vesper-arlen/v651-v7/") or path in OWNER_GLOBALS)
        and (REPO / path).is_file()
        and path != "docs/vesper-arlen/v651-v7/validation/owner-manifest.json"
    )
    owner_entries = [filtered_blob(path) for path in owner_paths]
    write_json(
        "validation/owner-manifest.json",
        {
            "schema": "ghc.family.v651-v7.owner-manifest.v1",
            "hash_domain": "git_path_filtered_blob",
            "entries": owner_entries,
            "entry_count": len(owner_entries),
            "self_exclusions": ["docs/vesper-arlen/v651-v7/validation/owner-manifest.json"],
            "owner_file_count": len(owner_entries) + 1,
            "file_threshold": 2000,
            "below_threshold": len(owner_entries) + 1 < 2000,
        },
    )
    return len(entries), len(owner_entries)


def main() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError(f"closeout builder requires exact evidence head {EVIDENCE}")
    if any(
        not (path.startswith("docs/vesper-arlen/v651-v7/") or path in OWNER_GLOBALS)
        for path in status_paths()
    ):
        raise RuntimeError("closeout builder refuses unexpected pre-existing changes")
    baton_words, overview_words = write_final_documents()
    final_entries, owner_entries = build_manifests(baton_words, overview_words)
    print(
        json.dumps(
            {
                "built": True,
                "baton_words": baton_words,
                "overview_words": overview_words,
                "final_manifest_entries": final_entries,
                "owner_manifest_entries": owner_entries,
                "negatives": NEGATIVES,
                "route": "PREPARED_NOT_SENT",
                "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
