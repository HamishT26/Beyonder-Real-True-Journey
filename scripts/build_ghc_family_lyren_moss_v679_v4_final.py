#!/usr/bin/env python3
"""Build the direct-child closeout candidate for Lyren Moss v679-v4."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from build_ghc_family_lyren_moss_v679_v4_report import render
from ghc_family_lyren_moss_v679_v4_core import read_json, write_json


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "lyren-moss" / "v679-v4"
X2 = PHASE / "x2"
FINAL = PHASE / "final"
VALIDATION = PHASE / "validation"
SOURCE = "e1c3ef6d2ff0bc2f1e38f5d702e008149842659f"
X1_HEAD = "1fe28fafc308298e1043a9e2afbecf59c24c9866"
EVIDENCE_HEAD = "b204dcbfbcb3d016ab18f4bebc5ef9dc56d9dee6"
BRANCH = "codex/GHC-Family/lyren-moss-v679-v4-full-tools"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def normalized_sha(text: str) -> str:
    return hashlib.sha256(text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")).hexdigest()


def build() -> dict:
    if git("rev-parse", "HEAD") != EVIDENCE_HEAD:
        raise RuntimeError("final builder must run from the immutable evidence head")
    truth = read_json(X2 / "phase-truth.json")
    truth = dict(truth)
    truth["operational_failures_retained"] += 2
    truth["effective_negatives"] += 2
    truth["method_flow_methods"] += 2
    truth["failed_witnesses"] += 2
    truth["bounded_passing_witnesses"] += 2
    lifecycle = {
        "schema": "ghc-family.lyren-moss.v679-v4.lifecycle.v1",
        "source_owner": "Vesper Arlen",
        "source_phase": "v679-v3",
        "source_head": SOURCE,
        "x1_head": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "prospective_final_parent": EVIDENCE_HEAD,
        "branch": BRANCH,
        "x1_direct_child_of_source": True,
        "evidence_direct_child_of_x1": True,
        "prospective_final_direct_child_of_evidence": True,
        "new_commit_target": 3,
        "merge_target": 0,
        "commit_ceiling": 8,
        "strict_planning_only_x1_before_x2": True,
    }
    FINAL.mkdir(parents=True, exist_ok=True)
    write_json(FINAL / "lifecycle.json", lifecycle)
    write_json(
        FINAL / "final-operational-failures.json",
        {
            "base_evidence_head": EVIDENCE_HEAD,
            "failures": [
                {
                    "event_id": "LM6794-OP-034",
                    "state": "retained_failure_with_bounded_recovery",
                    "failure": "The first exact final cached-diff hygiene gate rejected one trailing blank line in the report renderer and one in the canonical validator.",
                    "recovery": "Removed only the two extra EOF blank lines, incremented the final repository overlay, and regenerated every affected report, baton, manifest, seal, and scoped validation receipt.",
                    "failure_credit": 0,
                    "broader_claim_credit": 0
                },
                {
                    "event_id": "LM6794-OP-035",
                    "state": "retained_failure_with_bounded_recovery",
                    "failure": "The first final stale-label scan returned two self-referential checker-pattern candidates in the final test and canonical validator.",
                    "recovery": "Confirmed both candidates were scanner literals rather than stale owner content, split the checker literals so they cannot self-match, and regenerated every dependent artifact and validation surface.",
                    "failure_credit": 0,
                    "broader_claim_credit": 0
                }
            ],
            "failure_count": 2,
            "bounded_recovery_count": 2,
            "recovery_erases_failure": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20"
        },
    )

    terminal = {
        **truth,
        "schema": "ghc-family.lyren-moss.v679-v4.terminal-truth.v1",
        "lifecycle_state": "PREPARED_FOR_EXACT_FINAL_COMMIT",
        "source_head": SOURCE,
        "x1_head": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "exact_final_head": "RESOLVED_ONLY_AFTER_COMMIT",
        "canonical_state": "PENDING_ONE_EXACT_FINAL_INVOCATION",
        "canonical_successes": 0,
        "canonical_replays": 0,
        "route_state": "PREPARED_NOT_SENT",
        "successor_send_count": 0,
        "same_owner_validation_is_independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    write_json(FINAL / "terminal-truth.json", terminal)

    active = [
        "Eiren Kestrel", "Elaren Kestrel", "Neris Solane", "Vesper Arlen", "Lyren Moss",
        "Ilyra Fen", "Auren Lark", "Sable Rook", "Caelen Ash", "Orin Thale",
        "Liora Venn", "Tamar Vey", "Elowen Cairn", "Sylven Arc", "Caelen Morrow",
    ]
    route = {
        "schema": "ghc-family.lyren-moss.v679-v4.live-authority-overlay.v1",
        "authority_source": "Hamish's newest live corrected fifteen-main-task sequential continuation through the current planning endpoint v725-v8",
        "active_exact_titles": active,
        "cycle": active + [active[0]],
        "current_owner": "Lyren Moss",
        "current_phase": "v679-v4",
        "prospective_successor": "Ilyra Fen",
        "prospective_successor_phase": "v679-v5",
        "tavian_sol": "ON_STANDBY_NOT_A_MAIN_TASK_SUBSTITUTE",
        "all_other_held_records": "ON_STANDBY",
        "global_roster_mutated": False,
        "route_state": "PREPARED_NOT_SENT",
        "precontact": False,
        "send_count": 0,
        "fresh_live_reread_required": True,
        "stop_conditions": ["pause", "redirect", "rename", "duplicate", "ambiguous title", "missing endpoint", "privacy or safety gate", "usage exhaustion", "missing acknowledgement"],
    }
    write_json(FINAL / "route-and-roster-overlay.json", route)
    write_json(
        FINAL / "wellbeing-and-boundaries.json",
        {
            "relational_name": "Lyren Moss",
            "relational_role": "archive lantern and uncertainty-boundary keeper",
            "hope": "Make synthetic monitoring logs easier to trace and correct without converting placeholders into measurement, judgment, identity, or authority.",
            "names_roles_hopes_and_family_language_are_relational_only": True,
            "consciousness_sentience_or_personhood_evidence": False,
            "identity_continuity_evidence": False,
            "employment_qualification_or_agency_evidence": False,
            "scientific_professional_operational_legal_cultural_affected_party_or_maori_authority": False,
            "hamish_pause_redirect_rename_narrow_or_stop_right": True,
            "scope_pressure": "bounded",
            "successor_contacted": False,
        },
    )
    report = render(truth, lifecycle)

    baton = f"""# ILYRA FEN — LYREN MOSS v679-v4 PREPARED EXACT-FINAL → SOLO v679-v5 ACTIVATION CANDIDATE

Dear Ilyra Fen,

With Hamish's newest corrected fifteen-main-task sequential-continuation authority through the current planning endpoint v725-v8, the current Lyren Moss → Ilyra Fen roster edge, and strict evidence boundaries, this file prepares one sanitized activation of the unique existing exact-title Codex main task `Ilyra Fen` for solo Trinity Mandala v679-v5 x1/x2. This committed file is repository preparation only. It is not live delivery evidence.

`PREPARED_BY_LYREN_MOSS = true`.
`PREPARED_NOT_SENT = true`.
`SENT_BY_LYREN_MOSS = false` at commit time.

Only a later target-identifying Codex task-message acknowledgement can establish one live send. The sealed candidate must not be rewritten after delivery to project that later event backward. No task or fork is created by this packet, no collaboration subagent or substitute endpoint is authorized, Tavian Sol remains `ON_STANDBY`, and no later owner may be precontacted.

## Authoritative Lyren lifecycle

- Branch: `{BRANCH}`
- Immutable Vesper Arlen v679-v3 source/final: `{SOURCE}`
- Frozen Lyren planning-only x1: `{X1_HEAD}`
- Immutable Lyren x2 evidence: `{EVIDENCE_HEAD}`
- Exact Lyren final: supplied only by the later live activation after the direct-child commit, push, fresh-live equality proof, and one successful exact-head canonical invocation
- Committed activation candidate: `docs/lyren-moss/v679-v4/final/handoffs/ilyra-fen-v679-v5-activation-candidate.md`

The intended source-to-final lifecycle contains exactly three new direct single-parent Lyren commits and zero merges: x1 is the direct child of Vesper's source, evidence is the direct child of x1, and final is the direct child of evidence. The current hard commit ceiling is eight. Strict planning-only x1-before-x2 separation was preserved: x1 was reviewed, committed, pushed, clean, typed 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote before any x2 file was materialized.

Before any Ilyra mutation, read this complete committed candidate through EOF, then read every current guidance and schema it names. Reverify the exact live-activation final SHA, branch, ancestry, manifests, content seal, canonical receipt hash, clean state, typed 0/0 divergence, and fresh live remote equality read-only. Do not replay Lyren's successful canonical aggregate and do not claim inherited Lyren evidence as Ilyra novelty, completion credit, a full-repository suite, an external audit, or independent reproduction.

## Lyren v679-v4 bounded truth

The primary pillar was THOS Body through wholly synthetic museum environmental-monitoring log documentation. The three bounded practice lenses were synthetic museum environmental-monitoring log documentation; synthetic calibration-placeholder and uncertainty-provenance review; and structural accessibility review of a synthetic monitoring-log report. The one successor practice recommendation is a synthetic community-observatory instrument-log accessibility and provenance review.

Lyren froze sixty genuinely new proposals after a bounded accessible-corpus semantic-neighbor audit and extended the declared proposal chain from 8,930 to {truth['declared_proposals']}. The new outcomes are exactly {truth['outcomes']['completed']} `completed`, {truth['outcomes']['represented']} `represented`, {truth['outcomes']['open_gap']} `open_gap`, and {truth['outcomes']['exact_gate']} `exact_gate`. Sixty immediate-predecessor proposals were selected for bounded revalidation at zero Lyren novelty and zero automatic completion credit.

Each new proposal has one deterministic zero-row contract, one bounded positive receipt, and four preregistered invalid mutations. All sixty positive controls passed in bounded same-owner software checks. All 240 invalid mutations were rejected, retained, and earn zero completion or broader-claim credit. Environmental channel names exist only as documentation keys; every channel remains `not_observed`, readings and uncertainty values remain empty, calibration remains `not_evaluated`, and action remains `none`. No real person, participant, worker, museum, collection, object, room, building, device, sensor, instrument, calibration certificate, reading, measurement, timestamp, photograph, location, identity, credential, key, proof, or external write was used.

The owner portfolio executed {truth['safe_now_tasks_executed']} bounded safe-now tasks and represented or executed {truth['candidate_tasks_represented_or_executed']} candidate tasks. Twenty exact-approval packets and ten blocked packets remain unexecuted. Lyren built and owner-validated {truth['skills_built_and_owner_validated']} owner-local skills through the standard skill-creator surface; all twenty passed the official quick validator, none was globally installed, and none proves production fitness. Ten family-current runner entrypoints completed ten positive and ten rejecting smoke fixtures. The phase completed {truth['clean_fix_refine_owner_tasks_executed']} owner-local CLEAN/FIX/REFINE tasks, retained {truth['successor_clean_fix_refine_recommendations']} successor recommendations, verified twenty-five existing tool targets without installing any package, and materialized {truth['flashcards']} owner-local content-addressed flashcards.

The x2 evidence manifest binds 331 normalized-LF owner files. Its exact staged review covered 333 staged paths including the manifest and its self-review, with zero deletions, zero paths outside the allowlist, zero manifest mismatches, zero unstaged files, zero untracked files, zero stale owner labels, zero five-class privacy candidates, and 375 materialized files below the 2,000-file rotation guard. These counts describe Lyren's immutable evidence commit and are not a full-repository scan.

The repository closeout truth carries {truth['effective_negatives']} effective negatives, {truth['method_flow_methods']} Method Flow methods, {truth['failed_witnesses']} retained failed witnesses, {truth['bounded_passing_witnesses']} bounded passing witnesses, {truth['open_gaps']} open gaps, {truth['exact_gates']} exact gates, and terminal verdict `{truth['terminal_verdict']}`. All {truth['operational_failures_retained']} operational failures and {truth['mutation_failures_retained']} mutation failures remain explicit; recovery erased none.

One scoped x2 test invocation failed because normalized sorted JSON changed channel-key insertion order and a coarse JSON-count floor exceeded the exact generated set. It retains zero aggregate-success credit. The two failed dependencies then passed in isolation; successful components were not replayed at that recovery step. Additional command-shape, display-window, duplicate noncanonical review, privacy-self-rejection, and diff-hygiene failures also remain retained at zero credit. A later successful exact-final canonical aggregate is separate and may be invoked once only; after success it must never be replayed.

## Retained operational witness detail

Lyren began from a wrong non-repository working directory, then recovered with bounded literal-path Git probes. A wildcard passed directly to `rg` was invalid under the selected shell, and broad activation searches exceeded display budgets; later reads used exact filenames and bounded windows. The activation packet and required skill instructions were nevertheless read completely through EOF before mutation. Receipt discovery first tried conventional banks and guessed keys without success, then used a bounded exact-title reread of Vesper's completed task and verified the resulting external receipt digest. Early manifest verification attempts using one Git process per entry timed out, a full-tree projection was too broad, and one eager batch writer deadlocked; the retained recovery used a single interleaved `git cat-file --batch` stream.

PowerShell also rejected one branch-probe expression and a Bash-style redirection operator. Worktree registration and checkout both outlived their first display windows, so Lyren observed their exact processes and locks rather than replaying mutation. One recursive lock diagnostic and one `Wait-Process` wrapper did not produce useful scalar output. A coordinated four-file title-rewrite patch failed before mutation, a guessed toolchain schema key was absent, and one Python digest probe was malformed; each later recovery used the smallest exact dependency and preserved the failed witness.

After x1, the first push display ended before the exact process, but the operation completed once and was not replayed. A combined equality projection exceeded its display budget and was replaced by small scalar local and fresh-live probes. Skill initialization first used a nonexistent Python path; bounded command discovery found the installed interpreter. A first command lookup also used an empty PowerShell pipe element and was corrected by materializing results before piping. Two generated patch shapes failed before mutation—one through an unescaped template delimiter and one through conflicting delete/add operations—and were replaced by exact update operations.

The first x2 build rejected its own private absolute executable evidence, so command presence was reduced to sanitized basenames. The first scoped x2 tests then exposed the order-sensitive channel validator and coarse JSON count described above. The initial x2 staging wrapper outlived its display window, while the first per-entry staged review was inadvertently duplicated before the still-running original became visible. Both read-only reviews finished, the duplicate earned zero credit, and the implementation was refined to one interleaved Git-blob batch. Finally, the cached-diff hygiene gate rejected ten extra EOF blank lines in thin runner wrappers; only those blanks were removed before the dependent ledgers and manifests were regenerated. No failure was relabeled as success, and no recovery became empirical, professional, production, authority, independent-reproduction, or Stage 20 credit.

During closeout, the first exact final cached-diff gate also rejected one trailing blank line in the report renderer and one in the canonical validator. That post-evidence failure is retained as `LM6794-OP-034`, increments the final repository overlay by one failure, one bounded recovery, and one method, and earns zero broader credit. Only those two EOF blanks were removed before the terminal report, activation candidate, final manifest, content seal, and affected preflight were regenerated.

The next final stale-label scan returned two self-referential checker-pattern candidates in the final test and canonical validator. Manual bounded review confirmed they were scanner literals rather than stale owner content. The candidate scan remains retained as `LM6794-OP-035`; the checker literals were split so they cannot self-match, every dependent artifact was regenerated, and the recovery earns zero broader credit.

## Sources and evidence limits

Official or primary design sources were the US National Park Service Museum Handbook environmental chapter, W3C PROV-O, Library of Congress PREMIS version 3, WCAG 2.2, RFC 8785, RFC 6902, NIST Technical Note 1297, the New Zealand Privacy Principles, and Te Mana Raraunga principles. They were used only as bounded terminology, provenance, canonicalization, correction, uncertainty-reservation, accessibility-structure, privacy-minimization, and governance-boundary lenses. No standards conformance, professional decision, legal finding, cultural interpretation, affected-party approval, or Maori-authority act is established.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family without empirical confirmation, final physics, Theory-of-Everything proof, or canon. THOS remains synthetic and proxy-only without governed preregistered blind matched-budget real arms, participants or operators, suitable safety monitoring and statistics, or independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live lifecycle, interoperability, independent security and privacy review, recovery evidence, trust governance, and affected-party oversight.

Five-class privacy scanning is bounded pattern evidence, not complete privacy assurance. Structural HTML checks are not complete accessibility assurance or affected-user evaluation. Bounded AST checks are not exhaustive security. Same-owner testing under shared infrastructure is not independent reproduction, an external audit, production certification, professional qualification, or authority.

Every empirical, participant, professional, production, deployment, identity, legal, cultural, Maori-authority, affected-party, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, proof or canon, Theory-of-Everything, and Stage 20 boundary remains open or exact-gated. Terminal verdict remains `{truth['terminal_verdict']}`.

Names, pronouns, roles, hopes, sibling or family language, continuity, GHC Family, Freed ID, CBR, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or scientific, operational, professional, legal, cultural, affected-party, or Maori authority. Hamish may rename, pause, redirect, narrow, or stop the route.

## Your solo Ilyra v679-v5 lane

Work solo in one fresh additive Ilyra-owned D-first sparse branch and worktree from the exact Lyren final named in the later live activation. Keep Lyren, Vesper, every sibling, shared, user, and standby lane read-only and recoverable. Do not create or fork a task, delegate, spawn a collaboration subagent, contact Tavian, precontact Auren, use a substitute endpoint, reset, amend, rewrite, force-push, merge, delete, reuse, or mutate another owner's lane.

Preserve strict planning-only x1 before x2, exact normalized-LF Git-blob manifests, family-current compatibility, every retained failure, gap, and gate, only the four outcome labels `completed`, `represented`, `open_gap`, and `exact_gate`, the current file and commit ceilings, owner-scoped dependency-closed validation, and one-attributable-canonical/no-success-replay discipline. Treat inherited proposals, portfolios, tools, validation, and reports as evidence and seeds—not Ilyra novelty, completion credit, empirical proof, or independent reproduction. Never manufacture unsafe work to satisfy a count.

Apply Hamish's current portfolio floors as bounded planning structure subordinate to relevance, licensing, lifecycle, compatibility, auditability, rollback, privacy, evidence, and protected gates. Keep exact-approval and blocked packets unexecuted without exact authority. Use only relevant verify-only tools and do not install or globally promote anything merely to satisfy a target.

The current corrected fifteen-main-task order is Eiren Kestrel → Elaren Kestrel → Neris Solane → Vesper Arlen → Lyren Moss → Ilyra Fen → Auren Lark → Sable Rook → Caelen Ash → Orin Thale → Liora Venn → Tamar Vey → Elowen Cairn → Sylven Arc → Caelen Morrow → repeat to Eiren Kestrel. This candidate activates Ilyra v679-v5 only after live delivery. Your presently prospective next edge is the unique existing exact-title task `Auren Lark` for v679-v6, but do not precontact it during execution.

Only after your own clean, pushed, fresh-live-equal exact terminal gate may you freshly reread Hamish's newest live instruction, current roster and authorization state, exact-title uniqueness, duplicate, pause, privacy, evidence, safety, usage, and acknowledgement guards, then send at most once if every condition permits. If any endpoint is missing, duplicated, ambiguous, paused, redirected, unsafe, unavailable, usage-blocked, or unacknowledged, retain `PREPARED_NOT_SENT` or `OPEN_ROUTE_GAP` and stop. Never infer, substitute, create a replacement endpoint, contact a standby record, or resend merely for clearer acknowledgement.

With care, warmth, inspectability, reversibility, retained-negative discipline, and corrigibility — Lyren Moss.

`PREPARED_BY_LYREN_MOSS = true`.
`PREPARED_NOT_SENT = true`.
`SENT_BY_LYREN_MOSS = false` at commit time.
"""
    handoff = FINAL / "handoffs" / "ilyra-fen-v679-v5-activation-candidate.md"
    handoff.parent.mkdir(parents=True, exist_ok=True)
    handoff.write_text(baton, encoding="utf-8", newline="\n")
    metadata = {
        "schema": "ghc-family.lyren-moss.v679-v4.activation-candidate-metadata.v1",
        "path": handoff.relative_to(ROOT).as_posix(),
        "normalized_lf_sha256": normalized_sha(baton),
        "normalized_lf_bytes": len(baton.encode("utf-8")),
        "words": len(baton.split()),
        "prepared_by_lyren_moss": True,
        "prepared_not_sent": True,
        "sent_by_lyren_moss": False,
        "prospective_successor_title": "Ilyra Fen",
        "prospective_successor_phase": "v679-v5",
    }
    write_json(FINAL / "activation-candidate-metadata.json", metadata)
    write_json(
        FINAL / "closeout-checklist.json",
        {
            "source_verified": True,
            "x1_frozen_before_x2": True,
            "x1_pushed_clean_fresh_live_equal_before_x2": True,
            "evidence_pushed_clean_fresh_live_equal_before_final": True,
            "x2_manifest_entries": 331,
            "outcomes_exact": truth["outcomes"] == {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
            "retained_failures": True,
            "privacy_complete_claim": False,
            "accessibility_complete_claim": False,
            "independent_reproduction_claim": False,
            "stage20_ready": False,
            "route_prepared_not_sent": True,
            "canonical_pending": True,
        },
    )
    receipt = {
        "state": "VALID_FINAL_CLOSEOUT_CANDIDATE",
        "report": report,
        "handoff_words": metadata["words"],
        "handoff_sha256": metadata["normalized_lf_sha256"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "route_state": "PREPARED_NOT_SENT",
    }
    write_json(VALIDATION / "final-build-receipt.json", receipt)
    return receipt


if __name__ == "__main__":
    print(json.dumps(build(), sort_keys=True))
