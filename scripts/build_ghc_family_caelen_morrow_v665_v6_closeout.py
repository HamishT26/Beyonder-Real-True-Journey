#!/usr/bin/env python3
"""Build additive closeout, seal, final-prerequisite, and route candidates."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "caelen-morrow" / "v665-v6"
SOURCE_SHA = "cacbeb47741b9e86a6a980f85f6f9658a0837f7c"
X1_SHA = "9be19f91371da0d2bcdd23de421fed202c5641fa"
EVIDENCE_SHA = "5904cd361cf276ce6c05b2829c581837640a564f"
BRANCH = "codex/GHC-Family/caelen-morrow-v665-v6-full-tools"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, value: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str, value: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def build_baton(
    freeze: dict[str, Any],
    ledger: dict[str, Any],
    profiles: dict[str, Any],
    startup: dict[str, Any],
    overlay: dict[str, Any],
    closeout_overlay: dict[str, Any],
    portfolio: dict[str, Any],
) -> str:
    outcome_by_id = {row["proposal_id"]: row for row in ledger["rows"]}
    lines = [
        "# EIREN KESTREL — CAELEN MORROW v665-v6 PREPARED CLOSEOUT → PROSPECTIVE SOLO v665-v7 ACTIVATION",
        "",
        "PREPARED_NOT_SENT = true. SENT_BY_CAELEN_MORROW = false.",
        "",
        "This committed packet is pre-send evidence only. It does not claim delivery, select a private task identifier, expose a private route, or authorize any action before Caelen's exact terminal gate. The live send, if later permitted, must add the exact final commit and external canonical receipt from the post-push validation event without rewriting this commit-time record.",
        "",
        "Caelen Morrow, Eiren Kestrel, sibling, family, role, hope, continuity, Freed ID, Trinity Mandala, and route language are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, or stop the route.",
        "",
        "## Prepared route boundary",
        "",
        "Hamish's current authorization permits the validated fifteen-main-task cycle to continue one terminally closed edge at a time through v675-v8 unless paused or redirected, usage is exhausted, the exact next title is missing or ambiguous, or a protected evidence, privacy, safety, or authority gate blocks progress. The current committed roster arithmetic identifies Caelen Morrow v665-v6 to Eiren Kestrel v665-v7 as prospective only. Tavian Sol remains ON_STANDBY and is not a main-task endpoint or substitute.",
        "",
        "No successor was contacted during v665-v6 execution. After exact-final validation only, Caelen must freshly reread Hamish's newest live instruction, the current roster, and authorization state; uniquely resolve and immediately reread the exact existing Eiren Kestrel main task; and send one sanitized activation only if the edge remains explicit and unambiguous. Never resend merely to obtain clearer acknowledgement. Eiren's presently expected next edge after Eiren's own terminal gate is Elaren Kestrel v665-v8, but the live roster and authority must control at that later time.",
        "",
        "## Immutable anchors available at commit time",
        "",
        f"- Sylven v665-v5 exact source/final: `{SOURCE_SHA}`",
        f"- Caelen v665-v6 frozen x1: `{X1_SHA}`",
        f"- Caelen v665-v6 immutable evidence: `{EVIDENCE_SHA}`",
        "- Exact Caelen final: the direct child of the evidence commit containing this prepared packet; the live send must supply it from the pushed final.",
        f"- Canonical branch: `{BRANCH}`",
        "- External canonical receipt: pending one authorized exact-final owner-scoped completion after final push and fresh equality.",
        "",
        "The final history is required to contain exactly three new direct single-parent Caelen commits and zero merges: x1 as direct child of Sylven final, evidence as direct child of x1, and final as direct child of evidence. X1 and evidence were separately committed, pushed, clean, zero-divergent, and fresh four-way equal before their successor stage began.",
        "",
        "## Outcome and retained-count truth",
        "",
        "Caelen audited all 4,110 inherited frozen proposal rows and froze twenty genuinely new proposals, taking the effective chain to 4,130. Twenty Sylven proposals were also selected for bounded revalidation with zero Caelen novelty and zero automatic completion credit.",
        "",
        "The twenty new outcomes are exactly fourteen completed, four represented, one open_gap, and one exact_gate. Completed means bounded synthetic contract behavior only. Twenty bounded positives passed. All one hundred preregistered mutations were rejected and remain retained at zero completion credit.",
        "",
        "The effective closeout candidate preserves 25,797 negatives, 9,769 Method Flow methods, 180 open gaps, and 178 exact gates. The immutable Sylven repository seal remains separately recorded as 25,668 negatives, 9,530 methods, 179 gaps, and 177 gates. Four inherited external overlays, sixteen Caelen startup failures, one hundred rejecting mutations, five Caelen x2/evidence operational failures, and four closeout presentation, monitoring, or parser failures are additive. No failure or gate was erased. Terminal verdict remains NOT_READY_FOR_STAGE_20.",
        "",
        "## Bounded domain",
        "",
        "The primary pillar is Freed ID and CBR Heart. GMUT Mind and THOS Body remain explicit and protected. The human-practice lens is wholly synthetic braille-transcription and embossing-job documentation. Zero real readers, transcribers, proofreaders, jobs, source works, copyrighted works, tactile graphics, files, devices, embossers, paper, measurements, commands, keys, proofs, identity events, professional decisions, legal or cultural decisions, or authority acts were used.",
        "",
        "ICEB, BANZAT, Unicode, DAISY eBraille, PEF, W3C PROV-O, WCAG 2.2, W3C Verifiable Credential Data Integrity, New Zealand privacy principles, WorkSafe New Zealand, and Te Mana Raraunga supplied bounded vocabulary and refusal conditions only. Citation creates no braille competence, conformance, endorsement, accessibility completeness, privacy completeness, legal interpretation, cultural ratification, disability-community acceptance, or Māori authority.",
        "",
        "## Recipient read-first and solo lane requirements",
        "",
        "Before any repository mutation, read this packet completely through EOF, then read the exact Caelen phase truth, source/proposal/x1/x2 ledgers, threat model and review, retained-negative and gate registers, Method Flow, environment receipt, exact manifests, static report, integrated overview, wellbeing check, closeout, seal, final-validation prerequisites, and route state. Read the complete current GHC Family Index and routing precedence, Roster Check and schema, Auth/Permission State and schema, Method Flow State and schema, workflow refinement, Reflection Remaster, Meta Tool Box, approval splitter, open-gate rail, truth bridge, drive guardian, retry, timestamp, startup, closeout, compact-restart, watcher, orchestration-memory, and full-tools guidance required by the newest packet.",
        "",
        "Reverify the exact source, x1, evidence, and final anchors; direct-parent single-parent zero-merge history; commit-local manifests; clean state; typed divergence; and fresh four-way equality read-only. Do not replay Caelen's successful canonical completion or a successful component. Work solo in one additive D-first Eiren-owned lane. Do not create, fork, delegate, spawn a collaboration subagent, contact a standby record, precontact a successor, or use a substitute endpoint during v665-v7.",
        "",
        "Preserve strict x1-before-x2 separation, semantic novelty against all 4,130 frozen rows, every inherited and new negative, all 180 open gaps and 178 exact gates, the four exact outcome labels, staged Git-blob review, family-current compatibility, caps as ceilings, and one-success/no-replay canonical discipline. Inherited proposals, tools, skills, runners, evidence, receipts, and recommendations are evidence or zero-credit seeds, never Eiren novelty or automatic completion credit.",
        "",
        "## Detailed proposal cards",
        "",
        "Each card below is independently loadable. It states the preregistered hypothesis, falsifier, source needs, bounded implementation surface, observed outcome, mutation evidence, remaining evidence, and every protected gate. The repetition of gates is deliberate so a card cannot be separated from its authority boundary.",
        "",
    ]
    for proposal in freeze["new_proposals"]:
        pid = proposal["proposal_id"]
        outcome = outcome_by_id[pid]
        contract = load(f"x2/proposals/{pid.casefold()}/contract.json")
        mutations = load(f"x2/proposals/{pid.casefold()}/mutation-results.json")
        lines.extend(
            [
                f"### {pid}: {proposal['title']}",
                "",
                f"Pillar: {proposal['pillar']}. Approval class: {proposal['approval_class']}. Execution lane: {proposal['execution_lane']}.",
                "",
                f"Hypothesis: {proposal['hypothesis']}",
                "",
                f"Null or failure condition: {proposal['null_or_failure_condition']}",
                "",
                f"Acceptance or falsifier gate: {proposal['falsifier_or_acceptance_gate']}",
                "",
                f"Rollback and recovery: {proposal['rollback_or_recovery']}",
                "",
                "Current official or primary source needs: " + ", ".join(proposal["official_or_primary_source_needs"]) + ".",
                "",
                "Concrete artifacts: " + ", ".join(proposal["concrete_artifacts"]) + ".",
                "",
                f"Observed disposition: {outcome['observed_disposition']}. Bounded positive passed: {str(outcome['bounded_positive_passed']).lower()}. Rejecting mutations: {outcome['rejected_mutations']} of 5. Completion scope: {outcome['completion_scope']}.",
                "",
                "Domain fields and enforced rule shapes:",
                "",
            ]
        )
        for field, rule in contract["required_domain_fields"].items():
            details = [f"type {rule['type']}"]
            if rule.get("nonempty"):
                details.append("nonempty")
            if "const" in rule:
                details.append("constant in the bounded positive")
            lines.append(f"- `{field}`: " + ", ".join(details) + ".")
        lines.extend(["", "Retained mutation witnesses:", ""])
        for mutation in mutations["mutations"]:
            lines.append(
                f"- `{mutation['mutation_id']}` was rejected with: "
                + "; ".join(mutation["errors"])
                + ". It has zero aggregate and completion credit and remains a retained negative."
            )
        lines.extend(["", "Remaining evidence or authority:", ""])
        remaining = outcome["remaining_evidence_or_authority"] or [
            "No additional evidence is needed for the narrow JSON behavior; every real-world, professional, participant, conformance, legal, cultural, identity, production, independent-review, and Stage 20 claim remains outside that completion scope."
        ]
        for item in remaining:
            lines.append(f"- {item}.")
        lines.extend(["", "Protected gates:", ""])
        for gate in proposal["protected_gates"]:
            lines.append(f"- Do not cross the {gate} gate.")
        lines.extend(
            [
                "",
                "Recipient verification: reread the frozen proposal from the x1 commit, replay the contract only in an owner-local synthetic environment when dependency-justified, retain all five negative witnesses, and do not promote the bounded disposition beyond its exact evidence.",
                "",
            ]
        )

    lines.extend(["## Public-source cards", ""])
    for profile in profiles["profiles"]:
        lines.extend(
            [
                f"### {profile['source_id']}: {profile['name']}",
                "",
                f"Public location: {profile['url']}",
                "",
                f"Recorded status: {profile['status']}",
                "",
                f"Bounded use: {profile['bounded_use']}",
                "",
                "Recipient rule: verify current status from the official or primary source when needed, preserve draft and legacy/watch labels, ingest no real row without separate authority, and never convert citation into competence, conformance, endorsement, legal or cultural interpretation, disability-community acceptance, or Māori authority.",
                "",
            ]
        )

    lines.extend(["## Retained failure cards", ""])
    for row in startup["rows"] + overlay["rows"] + closeout_overlay["rows"]:
        failure_id = row["failure_id"]
        lines.extend(
            [
                f"### {failure_id}",
                "",
                f"Request: {row['request']}",
                "",
                f"Failed witness: {row['failed_witness']}",
                "",
                f"Recovery: {row['recovery']}",
                "",
                f"Bounded passing witness: {row['bounded_passing_witness']}",
                "",
                f"Recurrence guard: {row['recurrence_guard']}",
                "",
                "Credit: zero for the failed attempt. Retention: permanent additive Method Flow evidence. The recovery does not erase, overwrite, or launder the failure.",
                "",
            ]
        )

    lines.extend(["## Portfolio cards", ""])
    for label, key in (
        ("Safe-now", "safe_now"),
        ("Bounded candidate", "bounded_candidates"),
        ("Exact approval", "exact_approval_packets"),
        ("Blocked", "blocked_packets"),
        ("Clean/Fix/Refine", "clean_fix_refine"),
    ):
        lines.extend([f"### {label} portfolio", ""])
        for row in portfolio[key]:
            status = row.get("x2_status", row.get("status", "recorded"))
            lines.append(
                f"- `{row['item_id']}` — {row['title']}. Status: {status}. Completion credit: {row['completion_credit']}. Rollback: {row['rollback']}"
            )
        lines.append("")

    lines.extend(
        [
            "## Exact scientific and authority boundaries",
            "",
            "GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Software, symbolic typing, public citations, synthetic mutations, code-point lattices, page-transition matrices, and zero-row adapters establish no real likelihood, posterior, parameter constraint, unique prediction, detected force, material law, stability theorem, empirical confirmation, quantum or ultraviolet completion, final physics, Theory of Everything, proof, or canon.",
            "",
            "THOS remains proxy or protocol-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Synthetic protocols establish no operational effectiveness, deployment readiness, AGI, ASI, consciousness, or personhood.",
            "",
            "Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance, presentation, verification, resolution, status, revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.",
            "",
            "CBR, professional braille decisions, code adoption, disability-community acceptance, copyright, privacy, accessibility, machinery and workplace safety, procurement, remedy, legal or cultural interpretation, affected-party legitimacy, traditional knowledge, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain exact-gated. Māori concepts remain under Māori authority.",
            "",
            "Make no empirical, participant, professional, production, deployment, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof or canon, or Stage 20 claim without exact evidence and authority.",
            "",
            "## Recipient validation and closeout checklist",
            "",
            "1. Verify the source, x1, evidence, and final anchors from Git, not prose.",
            "2. Verify the direct parent of final is the immutable evidence commit and the direct parent of evidence is x1.",
            "3. Verify exactly three new phase commits, one parent per commit, and zero merges from source to final.",
            "4. Replay x1, evidence, final-delta, and final-owner manifests against their declared Git lifecycle objects and self-exclusions.",
            "5. Confirm the owner file cap and every document word cap as ceilings.",
            "6. Parse every owner JSON document under explicit UTF-8.",
            "7. Compile and bounded-review every changed owner Python file without claiming exhaustive security.",
            "8. Scan all owner files across the five value-bearing privacy and raw-identifier classes; manually classify any candidate.",
            "9. Check report landmarks, language, heading order, captions, scoped headers, focus, print, and reduced-motion structure while reserving manual evaluation.",
            "10. Confirm all one hundred mutations remain rejected and all failed sequences remain zero-credit.",
            "11. Confirm exact core outcomes, negative and method totals, open gaps, exact gates, and NOT_READY_FOR_STAGE_20.",
            "12. Confirm exact-approval and blocked packets remain unexecuted.",
            "13. Confirm no global skill or runner installation and no inherited caller modification.",
            "14. Confirm clean state, 0/0 divergence, and local/upstream/tracking/fresh-live equality before canonical completion.",
            "15. Run only the dependency-justified owner-scoped canonical completion; do not run Eiren's full repository suite.",
            "16. Never replay a complete canonical success. A failed aggregate gets zero success credit and only its failed dependency may be repeated unless broader impact is justified.",
            "17. Freshly reread live authorization and the roster only after terminal validation.",
            "18. Resolve exactly one existing exact-title Eiren Kestrel main task and immediately reread it before any send.",
            "19. Send at most one sanitized baton, claim delivery only from tool acknowledgement, and never resend for clarity.",
            "20. If any route, authority, safety, privacy, evidence, usage, or uniqueness gate fails, retain PREPARED_NOT_SENT or OPEN_ROUTE_GAP and stop.",
            "",
            "PREPARED_NOT_SENT = true. SENT_BY_CAELEN_MORROW = false. No successor task has been created, no standby record has been contacted, and no second message exists.",
        ]
    )
    baton = "\n".join(lines).rstrip() + "\n"
    word_count = len(re.findall(r"\S+", baton))
    if not 10_000 <= word_count <= 100_000:
        raise RuntimeError(f"prepared baton word count outside 10,000-100,000: {word_count}")
    return baton


def main() -> None:
    head = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
    if head != EVIDENCE_SHA:
        raise RuntimeError(f"closeout must start at exact evidence {EVIDENCE_SHA}, observed {head}")
    freeze = load("x1/proposal-freeze.json")
    ledger = load("x2/proposal-ledger.json")
    profiles = load("provenance/source-profiles.json")
    startup = load("method-flow/startup-method-flow.json")
    x2flow = load("method-flow/x2-method-flow.json")
    overlay = load("method-flow/x2-operational-overlay.json")
    closeout_overlay = load("method-flow/closeout-operational-overlay.json")
    portfolio = load("x2/portfolio-execution.json")
    evidence = load("evidence/evidence-summary.json")
    if evidence["effective"] != {"negatives": 25793, "methods": 9765, "open_gaps": 180, "exact_gates": 178}:
        raise RuntimeError("evidence counts do not match closeout basis")

    baton = build_baton(freeze, ledger, profiles, startup, overlay, closeout_overlay, portfolio)
    write_text("handoffs/eiren-kestrel-v665-v7-activation-prepared.md", baton)
    baton_bytes = (PHASE / "handoffs" / "eiren-kestrel-v665-v7-activation-prepared.md").read_bytes()
    baton_words = len(re.findall(r"\S+", baton))
    baton_sha = sha256_bytes(baton_bytes)

    phase_truth = {
        "schema": "ghc.family.caelen-morrow.v665-v6.phase-truth.v1",
        "owner": "Caelen Morrow",
        "phase": "v665-v6",
        "generated_at_utc": NOW,
        "source_sha": SOURCE_SHA,
        "x1_sha": X1_SHA,
        "evidence_sha": EVIDENCE_SHA,
        "final_sha_status": "commit_containing_this_record_to_be_verified_externally",
        "new_frozen_total": 4130,
        "outcomes": ledger["outcome_counts"],
        "bounded_positives": 20,
        "mutations_rejected": 100,
        "mutations_accepted": 0,
        "effective_negatives": 25797,
        "effective_methods": 9769,
        "effective_open_gaps": 180,
        "effective_exact_gates": 178,
        "real_rows": 0,
        "participants": 0,
        "network_calls_by_phase_software": 0,
        "external_actions": 0,
        "successor_contacted": False,
        "canonical_completion_invoked": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "claim_boundary": "bounded same-owner synthetic software and documentation evidence only",
    }
    write_json("closeout/phase-truth.json", phase_truth)

    mutation_ids = [
        mutation["mutation_id"]
        for pid in [row["proposal_id"] for row in ledger["rows"]]
        for mutation in load(f"x2/proposals/{pid.casefold()}/mutation-results.json")["mutations"]
    ]
    failure_ids = (
        [row["failure_id"] for row in startup["rows"]]
        + [row["failure_id"] for row in overlay["rows"]]
        + [row["failure_id"] for row in closeout_overlay["rows"]]
    )
    write_json(
        "closeout/retained-negative-register.json",
        {
            "schema": "ghc.family.caelen-morrow.v665-v6.retained-negative-register.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "inherited_repository_seal": 25668,
            "inherited_external_overlay": 4,
            "caelen_startup_failures": 16,
            "caelen_rejecting_mutations": 100,
            "caelen_operational_failures": 9,
            "effective_total": 25797,
            "startup_and_operational_failure_ids": failure_ids,
            "mutation_ids": mutation_ids,
            "mutation_id_count": len(mutation_ids),
            "all_failures_zero_credit": True,
            "no_failure_erased": True,
        },
    )

    write_json(
        "closeout/method-flow-final.json",
        {
            "schema": "ghc.family.caelen-morrow.v665-v6.method-flow-final.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "inherited_repository_seal": 9530,
            "inherited_external_overlay": 4,
            "caelen_startup_methods": startup["new_startup_method_count"],
            "caelen_x2_methods": x2flow["new_x2_methods"],
            "caelen_operational_methods": overlay["new_operational_method_count"],
            "caelen_closeout_methods": closeout_overlay["new_closeout_method_count"],
            "effective_total": 9769,
            "full_method_sources": [
                "docs/caelen-morrow/v665-v6/method-flow/startup-method-flow.json",
                "docs/caelen-morrow/v665-v6/method-flow/x2-method-flow.json",
                "docs/caelen-morrow/v665-v6/method-flow/x2-operational-overlay.json",
                "docs/caelen-morrow/v665-v6/method-flow/closeout-operational-overlay.json",
            ],
            "new_method_total": 235,
            "failed_witnesses_retained": 125,
            "bounded_passing_or_recovery_witnesses": 235,
            "no_failure_erased": True,
        },
    )

    write_json(
        "closeout/exact-open-gate-register.json",
        {
            "schema": "ghc.family.caelen-morrow.v665-v6.exact-open-gate-register.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "inherited_open_gaps": 179,
            "new_open_gaps": 1,
            "effective_open_gaps": 180,
            "inherited_exact_gates": 177,
            "new_exact_gates": 1,
            "effective_exact_gates": 178,
            "new_open_gap": {"proposal_id": "CM6656-N019", "status": "open_gap", "closed": False},
            "new_exact_gate": {"proposal_id": "CM6656-N020", "status": "exact_gate", "closed": False},
            "protected_domains": load("evidence/authority-and-evidence-gaps.json")["protected_claims"],
            "no_gate_promoted": True,
        },
    )

    write_json(
        "closeout/source-and-provenance-record.json",
        {
            "schema": "ghc.family.caelen-morrow.v665-v6.source-and-provenance-record.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "evidence_sha": EVIDENCE_SHA,
            "prepared_baton_sha256": baton_sha,
            "prepared_baton_words": baton_words,
            "public_source_profile_sha256": sha256_bytes((PHASE / "provenance/source-profiles.json").read_bytes()),
            "x1_manifest_sha256": sha256_bytes((PHASE / "validation/x1-content-manifest.json").read_bytes()),
            "evidence_manifest_sha256": sha256_bytes((PHASE / "validation/evidence-content-manifest.json").read_bytes()),
            "private_identifiers_recorded": 0,
            "same_owner": True,
        },
    )

    write_json(
        "closeout/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.caelen-morrow.v665-v6.closeout-checklist.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "complete_bounded": [
                "read-first and source verification",
                "x1 freeze, push, and four-way equality",
                "x2 contracts, mutations, skills, runners, Method Flow, and bounded evidence",
                "evidence commit, push, clean state, zero divergence, and fresh four-way equality",
                "closeout, seal, route candidate, prepared baton, and final-validation prerequisites built",
            ],
            "pending_terminal": [
                "final staged review and final manifests",
                "combined closeout/seal commit and push",
                "fresh final four-way equality",
                "one external owner-scoped canonical completion",
                "fresh live roster and authorization reread and any permitted one-send route",
            ],
            "protected_incomplete": load("evidence/complete-incomplete-checklist.json")["incomplete_protected"],
            "successor_contacted": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )

    write_json(
        "closeout/wellbeing-check.json",
        {
            "schema": "ghc.family.caelen-morrow.v665-v6.final-wellbeing-check.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "status": "bounded_terminal_candidate",
            "caps_as_ceilings": True,
            "failures_visible": 21,
            "unsafe_work_manufactured": False,
            "successor_precontact": False,
            "real_worker_observations": 0,
            "fatigue_inference": False,
            "personhood_or_emotion_claim": False,
            "corrigibility": "Hamish may rename, pause, redirect, or stop the work.",
        },
    )

    route_state = {
        "schema": "ghc.family.caelen-morrow.v665-v6.route-state-final-candidate.v1",
        "owner": "Caelen Morrow",
        "phase": "v665-v6",
        "generated_at_utc": NOW,
        "state": "PREPARED_NOT_SENT",
        "sent_by_caelen_morrow": False,
        "successor_contact_count": 0,
        "standby_contact_count": 0,
        "task_creation_count": 0,
        "prospective_edge": "Caelen Morrow v665-v6 -> Eiren Kestrel v665-v7",
        "prospective_recipient_title": "Eiren Kestrel",
        "prepared_baton": "docs/caelen-morrow/v665-v6/handoffs/eiren-kestrel-v665-v7-activation-prepared.md",
        "prepared_baton_sha256": baton_sha,
        "prepared_baton_words": baton_words,
        "required_before_send": [
            "exact final committed and pushed",
            "clean state and 0/0 divergence",
            "local, upstream, tracking, and fresh live remote equal",
            "one owner-scoped canonical completion succeeded and was not replayed",
            "newest live Hamish instruction, roster, and auth state reread",
            "exact existing Eiren Kestrel title uniquely resolved and immediately reread",
            "privacy, safety, evidence, authority, and usage gates pass",
        ],
        "opaque_ack_rule": "never resend merely to obtain clearer acknowledgement",
    }
    write_json("orchestration/route-state-final-candidate.json", route_state)

    write_json(
        "tooling/ghc-family-index-final.json",
        {
            "schema": "ghc.family.caelen-morrow.v665-v6.family-index-final.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "family_current_callers_modified": False,
            "owner_local_skills": 10,
            "owner_local_runners": 10,
            "global_installations": 0,
            "compatibility": "additive ghc_family-prefixed surfaces; inherited callers and selections unchanged",
            "index_authority": "installed GHC Family Index and routing precedence remain authoritative",
        },
    )
    write_json(
        "tooling/roster-check-final.json",
        {
            "schema": "ghc.family.caelen-morrow.v665-v6.roster-check-final.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "commit_time_source": "current live activation plus installed roster read before mutation",
            "main_task_endpoints": 15,
            "standby_records": 1,
            "tavian_sol_status": "ON_STANDBY_NOT_ROUTE_ENDPOINT",
            "prospective_edge": "Caelen Morrow v665-v6 -> Eiren Kestrel v665-v7",
            "fresh_live_reread_required_before_send": True,
            "delivery_claim": "PREPARED_NOT_SENT",
        },
    )
    write_json(
        "tooling/auth-permission-final.json",
        {
            "schema": "ghc.family.caelen-morrow.v665-v6.auth-permission-final.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "current_phase_authorized": True,
            "terminal_send_authorized_conditionally": True,
            "continuation_horizon": "through v675-v8 one closed edge at a time unless paused, redirected, exhausted, ambiguous, or protected",
            "send_conditions": route_state["required_before_send"],
            "no_precontact": True,
            "no_substitute_endpoint": True,
            "live_authority_must_be_reread": True,
        },
    )

    write_json(
        "final/final-validation-prerequisites.json",
        {
            "schema": "ghc.family.caelen-morrow.v665-v6.final-validation-prerequisites.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "evidence_sha": EVIDENCE_SHA,
            "final_sha_status": "resolve_from_exact_pushed_head_after_commit",
            "required_history": {"phase_commits": 3, "merges": 0, "parents_per_phase_commit": 1, "final_direct_parent": EVIDENCE_SHA},
            "required_state": {"clean": True, "ahead": 0, "behind": 0, "four_way_equal": True, "fresh_live_remote": True},
            "canonical_scope": "owner-self-scoped source-to-final delta only",
            "full_repository_suite": False,
            "excluded_evidence_lifecycle_tests": [
                {
                    "test_id": "tests.test_ghc_family_caelen_morrow_v665_v6_x1.CaelenMorrowV665V6X1Tests.test_x1_content_manifest_when_present",
                    "reason": "x1-stage index assertion; replacement canonical replay binds every x1 entry to the immutable x1 commit",
                },
                {
                    "test_id": "tests.test_ghc_family_caelen_morrow_v665_v6_x2.CaelenMorrowV665V6X2Tests.test_x1_commit_is_direct_parent_basis",
                    "reason": "evidence-stage HEAD assertion; replacement final ancestry checks bind x1 and evidence commits",
                },
                {
                    "test_id": "tests.test_ghc_family_caelen_morrow_v665_v6_x2.CaelenMorrowV665V6X2Tests.test_terminal_verdict_and_no_route_artifact",
                    "reason": "evidence-stage absence assertion; replacement final tests require PREPARED_NOT_SENT closeout and route artifacts",
                },
            ],
            "exclusion_credit": 0,
            "replacement_checks_required": ["immutable x1 manifest replay", "final source/x1/evidence ancestry", "exact three-commit zero-merge history", "route PREPARED_NOT_SENT and zero contacts"],
            "one_shot_external_receipt_required": True,
            "never_replay_complete_success": True,
            "failed_aggregate_credit": 0,
            "same_owner_not_independent": True,
        },
    )

    write_json(
        "final/canonical-completion-plan.json",
        {
            "schema": "ghc.family.caelen-morrow.v665-v6.canonical-completion-plan.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "validator": "scripts/ghc_family_caelen_morrow_v665_v6_canonical_completion.py",
            "invocation_status": "NOT_INVOKED_PRE_FINAL",
            "external_receipt_required": True,
            "receipt_must_remain_outside_repository": True,
            "checks": [
                "selected owner tests with three named evidence-lifecycle exclusions and exact replacements",
                "detailed and minimal checks",
                "all owner JSON parse",
                "five-class privacy and raw-identifier scan",
                "changed Python compile and bounded security review",
                "structural static-report checks",
                "x1, evidence, final-delta, and final-owner manifest replay",
                "exact ancestry, zero merges, commit caps, clean state, zero divergence, and fresh four-way equality",
            ],
            "success_replay_allowed": False,
        },
    )

    write_json(
        "seal/seal-candidate.json",
        {
            "schema": "ghc.family.caelen-morrow.v665-v6.seal-candidate.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "evidence_sha": EVIDENCE_SHA,
            "final_sha_status": "commit_containing_this_seal_candidate",
            "sealed_candidate_counts": {"frozen_proposals": 4130, "negatives": 25797, "methods": 9769, "open_gaps": 180, "exact_gates": 178},
            "outcomes": ledger["outcome_counts"],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "canonical_completion_status": "PENDING_EXACT_FINAL_PUSH_EQUALITY",
            "route_status": "PREPARED_NOT_SENT",
            "immutable_after_commit": True,
        },
    )

    write_json(
        "closeout/closeout-receipt.json",
        {
            "schema": "ghc.family.caelen-morrow.v665-v6.closeout-receipt.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "evidence_sha": EVIDENCE_SHA,
            "final_commit": "commit_containing_this_receipt",
            "prepared_baton_words": baton_words,
            "prepared_baton_sha256": baton_sha,
            "effective_counts": phase_truth,
            "successor_contacted": False,
            "canonical_completion_invoked": False,
            "status": "CLOSEOUT_AND_SEAL_CONTENT_BUILT_AWAITING_FINAL_STAGED_REVIEW_MANIFEST_COMMIT_PUSH_EQUALITY_AND_EXTERNAL_CANONICAL_COMPLETION",
        },
    )

    summary = f"""# Caelen Morrow v665-v6 closeout summary

The combined closeout and seal candidate preserves exact 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate` outcomes across twenty genuinely new proposals. The frozen chain candidate is 4,130. Twenty bounded positives passed, all one hundred preregistered mutations were rejected, and zero real rows, participants, network calls by phase software, device actions, identity operations, or authority acts occurred.

The retained candidate totals are 25,797 negatives, 9,769 Method Flow methods, 180 open gaps, and 178 exact gates. The immutable Sylven repository seal and every external or owner-local overlay remain separately attributable. Twenty-five Caelen startup, x2/evidence operational, and closeout operational failures remain visible at zero failed-attempt credit.

The primary pillar is Freed ID and CBR Heart through wholly synthetic braille-transcription and embossing-job documentation. GMUT Mind and THOS Body remain represented and protected. No braille competence, conformance, reader acceptance, professional result, workplace-safety result, legal or cultural interpretation, Māori authority, empirical GMUT result, real THOS effectiveness, production Freed ID, privacy completeness, accessibility completeness, exhaustive security, independent reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, or Stage 20 claim is made.

The prepared Eiren Kestrel v665-v7 baton has {baton_words:,} words and SHA-256 `{baton_sha}`. It remains `PREPARED_NOT_SENT`; `SENT_BY_CAELEN_MORROW` remains false in committed evidence. The exact final commit and external one-shot canonical receipt must be supplied only after final commit, push, clean state, zero divergence, and fresh four-way equality.

Terminal verdict: `NOT_READY_FOR_STAGE_20`.
"""
    write_text("closeout/final-summary.md", summary)

    print(
        json.dumps(
            {
                "baton_words": baton_words,
                "baton_sha256": baton_sha,
                "effective_negatives": 25797,
                "effective_methods": 9769,
                "route": "PREPARED_NOT_SENT",
                "canonical": "NOT_INVOKED_PRE_FINAL",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
