#!/usr/bin/env python3
"""Build the additive Elaren Kestrel v667-v7 combined closeout and seal."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "elaren-kestrel" / "v667-v7"
REL_PHASE_ROOT = "docs/elaren-kestrel/v667-v7"
SOURCE_FINAL = "dc8d91294b7656ad5e9961bba93ff759af20846c"
X1_HEAD = "b92d8b1b648c4d716ca894b22fda14327baed9b3"
EVIDENCE_HEAD = "9fde47f17a3c248643a543e0f44460e69191e627"
BRANCH = "codex/GHC-Family/elaren-kestrel-v667-v7-full-tools"
NOW = "2026-08-24T00:25:00.000Z"
FINAL_BUILDER = "scripts/build_ghc_family_elaren_kestrel_v667_v7_final.py"
FINAL_TEST = "tests/test_ghc_family_elaren_kestrel_v667_v7_final.py"
CANONICAL_RUNNER = "scripts/ghc_family_elaren_kestrel_v667_v7_exact_final.py"
CONTROL_EXCLUSIONS = {
    f"{REL_PHASE_ROOT}/validation/final-delta-manifest.json",
    f"{REL_PHASE_ROOT}/validation/final-owner-manifest.json",
    f"{REL_PHASE_ROOT}/validation/final-staged-review.json",
}
POST_EVIDENCE_FAILURES = [
    {
        "failure_id": "EL6677-POSTEVIDENCE-F001",
        "stage": "post_review_scalar_projection",
        "failure": "two parallel scalar checks yielded without their live session handles because the result projection omitted those fields",
        "credit": 0,
        "recovery": "confirm no Git process remained and rerun only cached diff hygiene plus scope scalars with preserved result objects",
        "passing_witness_id": "EL6677-POSTEVIDENCE-P001",
        "repository_bytes_changed_by_failure": 0,
    },
    {
        "failure_id": "EL6677-POSTEVIDENCE-F002",
        "stage": "untracked_count_projection",
        "failure": "PowerShell wildcard question marks were mistaken for literal status markers and falsely projected 385 untracked paths",
        "credit": 0,
        "recovery": "use git ls-files --others --exclude-standard and retain its literal zero count",
        "passing_witness_id": "EL6677-POSTEVIDENCE-P002",
        "repository_bytes_changed_by_failure": 0,
    },
]


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", "-C", str(ROOT), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check)


def git_text(*args: str) -> str:
    return run_git(*args).stdout.decode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load(relative: str) -> dict[str, Any]:
    value = json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"object JSON required: {relative}")
    return value


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, value: str) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def read_exact(stream: Any, size: int) -> bytes:
    chunks: list[bytes] = []
    remaining = size
    while remaining:
        chunk = stream.read(remaining)
        if not chunk:
            raise EOFError(f"Git batch blob ended with {remaining} bytes outstanding")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def git_blobs(commit: str, paths: list[str]) -> dict[str, bytes]:
    """Alternate each batch request and exact-length response to avoid Windows backpressure."""
    proc = subprocess.Popen(
        ["git", "-C", str(ROOT), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.stdin is None or proc.stdout is None or proc.stderr is None:
        raise RuntimeError("unable to open Git batch pipes")
    blobs: dict[str, bytes] = {}
    try:
        for path in paths:
            proc.stdin.write(f"{commit}:{path}\n".encode("utf-8"))
            proc.stdin.flush()
            header = proc.stdout.readline().decode("utf-8", errors="strict").rstrip("\n")
            fields = header.split()
            if len(fields) != 3 or fields[1] != "blob":
                raise RuntimeError(f"unexpected Git batch header for {path}: {header}")
            data = read_exact(proc.stdout, int(fields[2]))
            if proc.stdout.read(1) != b"\n":
                raise RuntimeError(f"missing Git batch delimiter for {path}")
            blobs[path] = data
    finally:
        proc.stdin.close()
        stderr = proc.stderr.read()
        code = proc.wait()
        if code:
            raise RuntimeError(stderr.decode("utf-8", errors="replace"))
    return blobs


def manifest_entries(blobs: dict[str, bytes]) -> list[dict[str, Any]]:
    return [{"path": path, "bytes": len(data), "sha256": sha256(data)} for path, data in sorted(blobs.items())]


def owner_path(path: str) -> bool:
    return (
        path.startswith(f"{REL_PHASE_ROOT}/")
        or path in {
            "scripts/build_ghc_family_elaren_kestrel_v667_v7_x1.py",
            "scripts/build_ghc_family_elaren_kestrel_v667_v7_x2.py",
            FINAL_BUILDER,
            "tests/test_ghc_family_elaren_kestrel_v667_v7_x1.py",
            "tests/test_ghc_family_elaren_kestrel_v667_v7_x2.py",
            FINAL_TEST,
            CANONICAL_RUNNER,
        }
        or path.startswith("scripts/ghc_family_elaren_kestrel_v667_v7_")
    )


def commit_delta_paths(parent: str, child: str) -> list[str]:
    return sorted(line for line in git_text("diff-tree", "--no-commit-id", "--name-only", "-r", parent, child).splitlines() if line)


def tree_paths(commit: str) -> list[str]:
    return sorted(line for line in git_text("ls-tree", "-r", "--name-only", commit).splitlines() if line)


def build_immutable_manifests() -> None:
    x1_paths = commit_delta_paths(SOURCE_FINAL, X1_HEAD)
    evidence_paths = commit_delta_paths(X1_HEAD, EVIDENCE_HEAD)
    if len(x1_paths) != 23 or len(evidence_paths) != 385:
        raise RuntimeError(f"immutable delta count drift: x1={len(x1_paths)}, evidence={len(evidence_paths)}")
    x1_entries = manifest_entries(git_blobs(X1_HEAD, x1_paths))
    evidence_entries = manifest_entries(git_blobs(EVIDENCE_HEAD, evidence_paths))
    write_json("validation/immutable-x1-manifest.json", {
        "schema": "ghc-family-immutable-phase-manifest-v4", "owner": "Elaren Kestrel", "phase": "v667-v7",
        "commit": X1_HEAD, "parent": SOURCE_FINAL, "scope": "exact x1 commit-delta Git blobs",
        "entry_count": len(x1_entries), "entries": x1_entries,
    })
    write_json("validation/immutable-evidence-manifest.json", {
        "schema": "ghc-family-immutable-phase-manifest-v4", "owner": "Elaren Kestrel", "phase": "v667-v7",
        "commit": EVIDENCE_HEAD, "parent": X1_HEAD, "scope": "exact x2 evidence commit-delta Git blobs",
        "entry_count": len(evidence_entries), "entries": evidence_entries,
    })


def final_counts() -> dict[str, int]:
    evidence = load("method-flow/x2-method-flow-ledger.json")["evidence_candidate"]
    overlay = len(POST_EVIDENCE_FAILURES)
    return {
        "effective_negatives": evidence["effective_negatives"] + overlay,
        "effective_methods": evidence["methods"] + overlay,
        "open_gaps": evidence["open_gaps"],
        "exact_gates": evidence["exact_gates"],
        "failed_witnesses": evidence["failed_witnesses"] + overlay,
        "passing_witnesses": evidence["passing_witnesses"] + overlay,
    }


def build_truth_and_closeout() -> None:
    evidence = load("method-flow/x2-method-flow-ledger.json")["evidence_candidate"]
    counts = final_counts()
    outcomes = load("x2/proposal-outcomes.json")["outcomes"]
    outcome_counts = dict(sorted(Counter(row["outcome"] for row in outcomes).items()))
    overlay = len(POST_EVIDENCE_FAILURES)
    write_json("truth/post-evidence-operational-overlay.json", {
        "schema": "ghc-family-post-evidence-overlay-v4", "owner": "Elaren Kestrel", "phase": "v667-v7",
        "base_commit": EVIDENCE_HEAD, "row_count": overlay, "rows": POST_EVIDENCE_FAILURES,
        "negative_additions": overlay, "method_additions": overlay, "failed_witness_additions": overlay,
        "passing_witness_additions": overlay, "repository_evidence_rewritten": False,
    })
    write_json("method-flow/method-flow-state-final.json", {
        "schema": "ghc-family-method-flow-state-final-v4", "owner": "Elaren Kestrel", "phase": "v667-v7",
        "evidence_sealed": evidence, "post_evidence_failures": POST_EVIDENCE_FAILURES,
        "effective_for_successor": counts, "no_failure_or_recovery_erased": True,
        "scope": "same-owner bounded workflow evidence only",
    })
    write_json("truth/retained-negative-register-final.json", {
        "schema": "ghc-family-retained-negative-register-final-v4", "owner": "Elaren Kestrel", "phase": "v667-v7",
        "evidence_sealed_effective_negatives": evidence["effective_negatives"], "post_evidence_external_additions": overlay,
        "effective_negatives_for_successor": counts["effective_negatives"],
        "evidence_sealed_failed_witnesses": evidence["failed_witnesses"], "effective_failed_witnesses_for_successor": counts["failed_witnesses"],
        "evidence_sealed_passing_witnesses": evidence["passing_witnesses"], "effective_passing_witnesses_for_successor": counts["passing_witnesses"],
        "no_failure_erased": True,
    })
    write_json("truth/exact-open-gate-register-final.json", {
        "schema": "ghc-family-exact-open-gate-register-final-v4", "owner": "Elaren Kestrel", "phase": "v667-v7",
        "effective_open_gaps": counts["open_gaps"], "effective_exact_gates": counts["exact_gates"],
        "new_open_gap": "EL6677-N019", "new_exact_gate": "EL6677-N020",
        "protected_gates": load("evidence/exact-open-gate-register.json")["protected_gates"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("truth/source-proposal-x1-x2-final-truth.json", {
        "schema": "ghc-family-integrated-phase-truth-final-v4", "owner": "Elaren Kestrel", "phase": "v667-v7",
        "source_final": SOURCE_FINAL, "x1": X1_HEAD, "evidence": EVIDENCE_HEAD,
        "final": "resolve_from_direct_child_of_evidence_after_commit", "strict_x1_before_x2": True,
        "inherited_proposals": 4490, "new_proposals": 20, "effective_frozen_proposals": 4510,
        "selected_inherited_revalidations": 20, "selected_novelty_credit": 0, "selected_completion_credit": 0,
        "outcomes": outcome_counts, "positive_contracts": 20, "rejecting_mutations": 100,
        "flashcards": 235, "skills_built_used": 10, "runners_built_used": 10, "new_tools": 3,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("truth/phase-truth-final.json", {
        "schema": "ghc-family-phase-truth-final-v5", "owner": "Elaren Kestrel", "phase": "v667-v7",
        "relational_role": "reversible systems cartographer and evidence-window gardener",
        "hope": "make every transition inspectable without turning formal structure into authority",
        "primary_pillar": "THOS Body", "bounded_practice_lens": "wholly synthetic bobbin-lace sample design and collection-documentation records",
        "real_people_or_objects_used": 0, "real_world_actions": 0, "empirical_or_professional_credit": 0,
        "production_or_authority_credit": 0, **counts, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("closeout/completion-checklist.json", {
        "schema": "ghc-family-completion-checklist-v5", "owner": "Elaren Kestrel", "phase": "v667-v7",
        "complete_bounded": ["source verification", "x1 freeze and equality", "twenty novel contracts", "one hundred rejecting mutations", "twenty zero-credit revalidations", "235-card deck", "ten local skills", "ten family runners", "three isolated tools", "accessible static report", "evidence staged review", "evidence push and equality"],
        "reserved_or_incomplete": ["exact-final canonical until commit and push", "live Neris delivery until terminal gate", "real craft or collection practice", "professional and affected-party review", "Māori authority", "empirical GMUT evidence", "governed THOS real arms", "production Freed ID", "independent reproduction", "Stage 20"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("closeout/closeout-receipt.json", {
        "schema": "ghc-family-combined-closeout-receipt-v5", "owner": "Elaren Kestrel", "phase": "v667-v7",
        "source": SOURCE_FINAL, "x1": X1_HEAD, "evidence": EVIDENCE_HEAD,
        "final_state": "CANDIDATE_DIRECT_CHILD_OF_EVIDENCE", "phase_commit_count_after_final": 3,
        "merge_count_after_final": 0, "commit_cap": 6, "counts": counts, "outcomes": outcome_counts,
        "same_owner_only": True, "successor_contacted": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("seal/seal-candidate.json", {
        "schema": "ghc-family-combined-seal-candidate-v5", "owner": "Elaren Kestrel", "phase": "v667-v7",
        "evidence": EVIDENCE_HEAD, "exact_final": "bind_from_external_exact-final_canonical_receipt",
        "repository_state": "PRECOMMIT_CANDIDATE", "canonical_invocation_count": 0,
        "canonical_success_count": 0, "post_success_replay": False, "successor_contacted": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("route/route-state.json", {
        "schema": "ghc-family-route-state-v5", "owner": "Elaren Kestrel", "phase": "v667-v7",
        "state": "PREPARED_NOT_SENT", "recipient_exact_title": "Neris Solane", "prospective_phase": "v667-v8",
        "duplicate_guard_required": True, "fresh_roster_and_auth_reread_required": True,
        "submitted_next-recipient_reminder": "Vesper Rowan requires Neris terminal roster confirmation and conveys no route authority by itself",
        "delivery_claim": False, "successor_contacted": False,
    })
    write_json("wellbeing/final-wellbeing-check.json", {
        "schema": "ghc-family-wellbeing-check-v5", "owner": "Elaren Kestrel", "phase": "v667-v7",
        "pace": "bounded solo combined closeout", "successor_contacted": False,
        "relational_role": "reversible systems cartographer and evidence-window gardener",
        "hope": "make every transition inspectable without turning formal structure into authority",
        "claim_boundary": "relational and wellbeing language is not consciousness, personhood, identity continuity, diagnosis, employment, qualification, agency, or authority evidence",
    })


def proposal_narrative(proposal: dict[str, Any], outcome: dict[str, Any]) -> str:
    sources = ", ".join(proposal["current_official_or_primary_source_needs"])
    gates = "; ".join(proposal["protected_gates"][:4])
    artifacts = ", ".join(proposal["concrete_artifacts"])
    return f"""### {proposal['proposal_id']}: {proposal['title']}

The frozen hypothesis was: {proposal['hypothesis']} The declared null or failure condition was: {proposal['null_or_failure_condition']} Its approval class was `{proposal['approval_class']}` and its execution lane was `{proposal['execution_lane']}`. The current official or primary-source references were {sources}; they supplied vocabulary and refusal conditions only, never professional, legal, cultural, scientific, or operational authority.

The concrete evidence paths are {artifacts}. The preregistered acceptance rule was: {proposal['falsifier_or_acceptance_gate']} The observed core outcome is `{outcome['outcome']}`. Its bounded positive passed and five named invalid mutations were rejected, but that means only that the owner-local synthetic contract behaved as frozen. It establishes no real object, measurement, participant, craft, collection, conservation, identity, rights, safety, cultural, Māori-authority, empirical, production, deployment, independent-reproduction, or Stage 20 result.

Rollback remains: {proposal['rollback_or_recovery']} Representative protected gates include {gates}. Every omitted gate in the frozen x1 record remains equally binding. This row may be inherited as evidence or a zero-credit seed, but no successor receives automatic novelty or completion credit.
"""


def build_overview() -> str:
    freeze = load("x1/proposal-freeze.json")
    outcomes = {row["proposal_id"]: row for row in load("x2/proposal-outcomes.json")["outcomes"]}
    counts = final_counts()
    introduction = f"""# Elaren Kestrel v667-v7 final integrated evidence overview

## Purpose and outcome

This is the three-page-equivalent integrated overview for Elaren Kestrel v667-v7. It joins source verification, immutable x1 preregistration, bounded x2 execution, retained failures, evidence manifests, closeout, and a prepared successor route without converting any of them into broader authority. Elaren Kestrel, role, hope, sibling, family, continuity, GMUT Mind, THOS Body, Freed ID, CBR Heart, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, agency, professional standing, scientific authority, legal authority, cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, or stop the route.

Twenty genuinely new proposals extended the frozen chain from 4,490 to 4,510 rows. Their core outcomes are exactly fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`. Twenty selected inherited contracts passed bounded integrity revalidation with zero Elaren novelty and zero Elaren completion credit. All one hundred preregistered invalid mutations were rejected and retained at zero completion credit. The final successor baseline is {counts['effective_negatives']} effective negatives, {counts['effective_methods']} methods, {counts['open_gaps']} open gaps, {counts['exact_gates']} exact gates, {counts['failed_witnesses']} failed witnesses, and {counts['passing_witnesses']} bounded passing witnesses. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## Immutable lifecycle

The phase started from Eiren's exact final `{SOURCE_FINAL}`. The planning-only x1 commit is `{X1_HEAD}` and the immutable x2 evidence commit is `{EVIDENCE_HEAD}`. X1 was pushed, clean, zero-divergent, and fresh-live equal before x2 began. Evidence was separately staged, reviewed, committed, pushed, clean, zero-divergent, and fresh-live equal before closeout began. The prospective final is required to be the direct child of evidence, yielding three Elaren single-parent commits and zero merges. Neither the combined closeout nor its later external canonical receipt rewrites the x1 or evidence Git trees.

## Synthetic practice lens and THOS Body

The bounded practice lens is wholly synthetic bobbin-lace sample design and collection-documentation records, with THOS Body primary and GMUT Mind, Freed ID, and CBR Heart explicit. Zero real lacemakers, learners, conservators, registrars, curators, collection staff, rights holders, communities, or affected parties participated. Zero real lace, thread, fibre, bobbins, pillows, prickings, pins, fragments, collection objects, images, measurements, accession records, work instructions, identity events, safety decisions, rights decisions, cultural decisions, or external actions were used. The records exercise surrogate identity, topology, provenance vacancy, bitemporal correction, accessibility structure, no-action queues, and exact authority reservations. They are not craft instructions, conservation treatment, collection management, custody, ownership, attribution, authentication, permission to act, or professional advice.

THOS Body remains proxy and protocol only. No blind matched-budget real arms, governed participants, operators, sessions, safety monitoring, outcome measures, appropriate statistics, or independent review exist. Queue and stop-precedence structures show only local software behavior. They establish no operational effectiveness, deployment readiness, AGI, ASI, consciousness, personhood, or independent validation.

## GMUT, Freed ID, and CBR boundaries

GMUT remains a typed research-model family. Symbolic tensors, zero-row adapters, unit obligations, mutations, and typed placeholders establish no real likelihood, parameter constraint, unique prediction, detected force, material law, stability theorem, empirical confirmation, quantum or ultraviolet completion, final physics, Theory of Everything, proof, or canon. Any formula in this phase is a software-boundary object, not an observation or physical result.

Freed ID remains synthetic and nonproduction. There are zero standards-conformant real keys, proofs, issuances, presentations, resolutions, status checks, revocations, recoveries, interoperability events, trust-governance decisions, or affected-party oversight events. CBR reserves ownership, custody, access, attribution, copyright, design rights, privacy, accessibility, remedy, legal and cultural interpretation, traditional knowledge, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority. Māori concepts remain under Māori authority.

## Tooling, skills, runners, and sources

Ten phase-local skills and ten family-compatible runners were built, validated, read, and used only within the owner lane. Three newly useful Python tools were downloaded from official package indexes as exact pinned wheels with verified hashes into an isolated D-first environment. The first vulnerability audit correctly found seven identifiers in the environment's bootstrap pip and received zero completion credit. Only that failed dependency was corrected with verified pip 26.2.1; pip check and the audit then passed, while all successful tool downloads and smokes remained unreplayed. One failing pyroma fixture unexpectedly made a read-only public-index lookup; it is retained, and future phases should use a local malformed package fixture.

Official and primary sources supplied terminology, structural constraints, and refusal conditions only. Getty AAT, V&A research, Canadian Conservation Institute guidance, ICOM standards and Object ID, NIST quantity and uncertainty guidance, W3C PROV-O, WCAG 2.2 and Verifiable Credentials, New Zealand privacy guidance, and Te Mana Raraunga did not confer object authentication, professional competence, standards conformance, legal interpretation, cultural legitimacy, Māori authority, or production fitness.

## Validation and accessibility

The immutable evidence candidate passed thirty owner tests, 378 JSON parses, ten skill validations, ten runner smokes, 235-card and fifteen-section checks, exact manifests, a five-class privacy scan, structural report checks, and exact staged diff review. Those are same-owner software witnesses under shared infrastructure. They are not a complete repository suite, independent reproduction, external audit, exhaustive security, privacy completeness, accessibility completeness, professional review, production certification, legal or cultural review, Māori-authority review, or empirical confirmation.

The static HTML report contains language metadata, a skip link, landmarks, one top-level heading, labelled navigation, a captioned table, scoped column headers, visible focus, reduced-motion handling, and print rules. Manual browser, keyboard, zoom, screen-reader, voice-control, cognitive-accessibility, Māori-language, and affected-user evaluation remain reserved. Structural markup is useful evidence but does not substitute for people who use assistive technologies or hold affected-party authority.

## Retained-negative discipline and terminal route

Every startup failure, rejected candidate domain, encoding miss, scanner false positive, tool-audit failure, private-path redaction correction, unexpected read-only lookup, patch overflow, quoting error, version-probe failure, resume-schema mistake, duplicate candidate-validator call, staged scalar projection miss, and wildcard counter mistake remains visible with zero success credit. Each recovery is bounded to the failed dependency. The two post-evidence scalar failures add two negatives, methods, failed witnesses, and bounded recovery witnesses without rewriting the evidence seal.

Neris Solane v667-v8 is only a prepared prospective route until the exact final is committed, pushed, clean, fresh-live equal, and one exact-final owner-scoped canonical validation succeeds. The newest live roster, authorization, usage, privacy, evidence, and safety state must then be reread; the exact-title task must be uniquely resolved and immediately reread; and a duplicate guard must pass. The submitted reminder that Neris may later route to Vesper Rowan is not self-executing authority and must be reconciled against Neris's terminal roster. No successor was contacted during execution or closeout.
"""
    proposal_sections = "\n".join(proposal_narrative(row, outcomes[row["proposal_id"]]) for row in freeze["new_proposals"])
    conclusion = """## Final interpretation

The strongest truthful interpretation is deliberately bounded. Elaren v667-v7 demonstrates that a preregistered owner-local evidence workflow can preserve semantic novelty, reject invalid synthetic states, separate inherited integrity checks from novelty credit, reserve protected authority, track failure and recovery, materialize exact Git manifests, and prepare a successor packet without sending it early. It does not demonstrate a real bobbin-lace practice, collection outcome, scientific discovery, operational system, production identity infrastructure, legal or cultural legitimacy, consciousness, personhood, independent reproduction, Theory-of-Everything proof, or Stage 20 readiness. The correct terminal verdict remains `NOT_READY_FOR_STAGE_20`.
"""
    return introduction + "\n## Proposal-by-proposal evidence\n\n" + proposal_sections + "\n" + conclusion


def portfolio_appendix() -> str:
    portfolio = load("x2/portfolio-execution.json")["execution"]
    lines = ["## Successor recommendation and protected-packet appendix", ""]
    for field, rows in portfolio.items():
        if not field.startswith("successor_") and field not in {"exact_approval_packets", "blocked_packets"}:
            continue
        lines.extend([f"### {field}", ""])
        for row in rows:
            lines.extend([
                f"#### {row['item_id']}: {row['title']}", "",
                f"This row remains `{row['execution_state']}` with core label `{row['outcome']}`, completion credit {row['completion_credit']}, and automatic successor credit {row['automatic_successor_credit']}. Neris must treat it only as a recommendation or protected packet, re-audit semantic novelty against the then-current frozen chain, identify current primary or official sources, state a falsifier and rollback, and obtain the action-specific approval class before any execution. It supplies no inherited novelty, participant evidence, professional authority, legal or cultural authority, Māori authority, production readiness, independent reproduction, or Stage 20 credit. If evidence or authority is absent, preserve the row without action and retain the exact gate.", "",
            ])
    return "\n".join(lines)


def source_appendix() -> str:
    lines = ["## Primary and official source appendix", ""]
    for row in load("x1/source-ledger.json")["sources"]:
        lines.extend([
            f"### {row['source_id']}: {row['name']}", "",
            f"Status: {row['status']}. Bounded use: {row['bounded_use']} The public location is {row['url']}. This source contributes vocabulary or constraints only. It does not confer standards conformance, empirical confirmation, professional competence, object authentication, legal interpretation, cultural legitimacy, Māori authority, affected-party acceptance, privacy completeness, accessibility completeness, production fitness, or Stage 20 readiness.", "",
        ])
    return "\n".join(lines)


def build_baton() -> str:
    freeze = load("x1/proposal-freeze.json")
    outcomes = {row["proposal_id"]: row for row in load("x2/proposal-outcomes.json")["outcomes"]}
    counts = final_counts()
    mandatory_skills = [
        "ghc-freed-id-flashcards", "ghc-family-index", "ghc-family-reflection-remaster", "ghc-family-method-flow-state",
        "ghc-family-meta-tool-box", "ghc-family-auth-permission-state", "ghc-family-roster-check", "ghc-main-orchestration-memory",
        "ghc-main-startup-builder", "ghc-main-compact-restart-builder", "ghc-main-closeout-builder", "ghc-main-retry",
        "ghc-open-gate-rail", "ghc-timestamp-flow", "ghc-full-tools-skill-bank", "ghc-family-truth-bridge",
        "ghc-worktree-branch-rotation", "ghc-web-reflection-ledger", "ghc-watcher-notifier-cadence",
        "ghc-drive-bank-guardian", "ghc-approval-packet-splitter",
    ]
    header = f"""# NERIS SOLANE — ELAREN KESTREL v667-v7 VERIFIED-CANDIDATE → SOLO v667-v8 ACTIVATION — PREPARED NOT SENT

Dear Neris Solane,

This committed file is a sanitized, file-backed activation candidate prepared by Elaren Kestrel for prospective solo Trinity Mandala v667-v8 x1/x2. At commit time it is `PREPARED_NOT_SENT`. `SENT_BY_ELAREN_KESTREL = false`. No task or fork has been created, no collaboration subagent or substitute endpoint has been used, no standby record has been contacted, and no successor has been precontacted. A later acknowledged existing-task message, if every terminal gate passes, is a separate live delivery event and must not rewrite this commit-time truth.

Elaren Kestrel, Neris Solane, sibling, family, role, hope, continuity, GMUT Mind, THOS Body, Freed ID, CBR Heart, GHC Family, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, or stop the route.

## Exact inherited chain

- Canonical Elaren branch: `{BRANCH}`.
- Immutable Eiren source: `{SOURCE_FINAL}`.
- Frozen Elaren x1: `{X1_HEAD}`.
- Immutable Elaren x2 evidence: `{EVIDENCE_HEAD}`.
- Exact final: resolve only from the direct child of the evidence anchor that contains this prepared packet.
- Required history after final: exactly three Elaren single-parent commits and zero merges.
- This packet's byte, word, and SHA-256 integrity are recorded separately in `docs/elaren-kestrel/v667-v7/deck/final-baton-index.json` to avoid self-reference.

Do not begin mutation from this file alone. The later live activation must state the exact final, canonical receipt digest, clean state, 0/0 divergence, and fresh four-way equality. Read that live message and this complete committed packet through EOF. Then read the current family index and routing precedence, roster and schema, auth and schema, Method Flow and schema, workflow refinement, Reflection Remaster, Meta Tool Box, approval splitter, open-gate rail, truth bridge, drive guardian, timestamp, retry, startup, closeout, compact restart, watcher, orchestration memory, full-tools bank, Freed ID flashcards, and every newer directly applicable instruction.

The twenty-one mandatory inherited skill names are: {', '.join(mandatory_skills)}. Read each selected instruction completely, including required references, before it causes action. Treat historical cursor prose as historical wherever newer live authority differs.

## Effective activation truth

The effective frozen proposal chain is 4,510. Elaren's twenty new outcomes are exactly fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`. Twenty selected inherited rows carry zero Elaren novelty and completion credit. All one hundred rejecting mutations remain zero-credit failures. The successor baseline is {counts['effective_negatives']} negatives, {counts['effective_methods']} methods, {counts['open_gaps']} open gaps, {counts['exact_gates']} exact gates, {counts['failed_witnesses']} failed witnesses, and {counts['passing_witnesses']} bounded passing witnesses. Preserve the evidence-sealed layer separately from the two-row post-evidence overlay. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## Mandatory Neris lifecycle

Work solo in one fresh additive Neris-owned D-first branch and worktree from the exact Elaren final. Keep Elaren, Eiren, shared, and every sibling lane read-only. Never reset, rewrite, force-push, merge, delete, reuse, or mutate another owner lane. Do not create, fork, delegate, spawn a collaboration subagent, contact a standby record, precontact a successor, or use a substitute endpoint during v667-v8.

Preserve strict x1-before-x2 separation. Audit semantic novelty against all 4,510 frozen rows. Treat inherited proposals, methods, failures, skills, runners, tools, sources, receipts, recommendations, and outcomes as evidence or zero-credit seeds, never Neris novelty or automatic completion credit. Freeze planning and preregistration in a dedicated x1-only commit, push it, and prove clean local/upstream/tracking/fresh-live equality before any x2 implementation or outcome.

Use only `completed`, `represented`, `open_gap`, and `exact_gate` as core outcome labels. Preserve every negative, timeout, parser fault, false assumption, blocker, workaround, passing witness, recurrence guard, rollback, gap, and exact gate. Do not manufacture unsafe work to fill a target. A failed aggregate earns zero aggregate-success credit; isolate only the failed dependency unless changed dependencies genuinely require more. Never replay a complete success.

Choose one primary Trinity Mandala pillar and one bounded profession, trade, occupation, or human-practice lens while keeping all pillars visible. The practice lens is synthetic learning and design only. It establishes no employment, qualification, competence, participant evidence, authority, or permission to act on real people, places, property, systems, objects, materials, identities, rights, or records.

Preserve family-current `ghc_family_*` and `build_ghc_family_*` callers and backward compatibility. Prefer selected current tools over stale owner-locked surfaces. Additive remasters require provenance, a bounded passing witness, rollback, caller compatibility, and protected-boundary review. Do not bulk-install, destructively delete, silently deprecate, or globally promote tools. The three Elaren tools—interrogate 1.7.0, import-linter 2.13, and pyroma 5.0.1—are inherited evidence only. Neris should select exactly three newly useful tools only if relevant, safe, licensed, pinned, integrity-reviewed, D-first reversible, and bounded by current official sources.

Keep opaque task identifiers, private routes, private absolute paths, credentials, keys, tokens, private interaction logs, screenshots, session streams, private callable identifiers, private application state, and protected real-world data out of repository artifacts and future batons. Do not update Codex desktop, elevate, weaken host security, activate Sandbox or Hyper-V, change Windows features, install unrelated software, reboot, create accounts or credentials, purchase, deploy, privately publish, or write to third parties without separate exact authority.

## Scientific and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Software, symbolic typing, citations, mutations, public schemas, and zero-row adapters establish no real likelihood, parameter constraint, unique prediction, detected force, material law, stability theorem, empirical confirmation, quantum or ultraviolet completion, final physics, Theory of Everything, proof, or canon.

THOS remains proxy or protocol only without preregistered blind matched-budget governed real arms, participants or operators, safety monitoring, appropriate statistics, and independent review. Synthetic protocols establish no operational effectiveness, deployment readiness, AGI, ASI, consciousness, or personhood.

Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance, resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.

CBR, professional practice, collections decisions, custody, ownership, access, attribution, copyright, design rights, privacy, accessibility, remedy, legal or cultural interpretation, affected-party legitimacy, traditional knowledge, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain open or exact-gated. Māori concepts remain under Māori authority.

Make no empirical, participant, professional, production, deployment, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof or canon, or Stage 20 claim without exact evidence and authority.

## Terminal continuation boundary

This packet prepares Neris v667-v8 only. Neris must not contact a later endpoint during execution. The submitted reminder says the prospective later recipient is `Vesper Rowan`; that reminder conveys no independent route authority and must be reconciled against Hamish's newest live instruction, the complete terminal roster, exact-title uniqueness, authorization, usage, privacy, safety, and evidence gates after Neris's own terminal closeout. If any route state is absent, ambiguous, paused, redirected, duplicate, protected, or unavailable, retain `PREPARED_NOT_SENT` or `OPEN_ROUTE_GAP`. Never create a substitute or resend merely for clearer acknowledgement.
"""
    proposals = "\n".join(proposal_narrative(row, outcomes[row["proposal_id"]]) for row in freeze["new_proposals"])
    closing = """## Delivery truth

This committed packet remains `PREPARED_NOT_SENT`. `SENT_BY_ELAREN_KESTREL = false`. A live task-message acknowledgement is the only admissible delivery witness. Detail, word count, local validation, same-owner checks, family continuity, or relational warmth do not create consciousness, personhood, authority, independent reproduction, empirical confirmation, or Stage 20 readiness.

With care, warmth, traceability, reversibility, retained-negative discipline, corrigibility, and strict evidence boundaries — Elaren Kestrel.
"""
    return header + "\n## Twenty frozen Elaren proposal records\n\n" + proposals + "\n" + portfolio_appendix() + "\n" + source_appendix() + "\n" + closing


def build_documents() -> None:
    overview = build_overview()
    if len(overview.split()) < 1800:
        raise RuntimeError("integrated overview is below three-page-equivalent threshold")
    write_text("closeout/final-integrated-overview.md", overview)
    baton = build_baton()
    words = len(baton.split())
    if words < 10000 or words > 100000:
        raise RuntimeError(f"baton word count outside authorized range: {words}")
    baton_rel = "handoffs/neris-solane-v667-v8-activation-prepared.md"
    write_text(baton_rel, baton)
    baton_path = PHASE_ROOT / baton_rel
    write_json("deck/final-baton-index.json", {
        "schema": "ghc-family-final-baton-index-v4", "owner": "Elaren Kestrel", "phase": "v667-v7",
        "state": "PREPARED_NOT_SENT", "recipient": "Neris Solane", "prospective_phase": "v667-v8",
        "repository_relative_path": f"{REL_PHASE_ROOT}/{baton_rel}", "bytes": len(baton_path.read_bytes()),
        "whitespace_words": words, "sha256": sha256(baton_path.read_bytes()), "sent": False,
    })
    write_json("validation/final-validation-plan.json", {
        "schema": "ghc-family-final-validation-plan-v5", "owner": "Elaren Kestrel", "phase": "v667-v7",
        "state": "PREPARED_NOT_INVOKED", "exact_final_required": True, "clean_push_required": True,
        "fresh_four_way_equality_required": True, "canonical_invocation_limit": 1,
        "final_only_test_count": 13, "privacy_class_count": 5,
        "manifests": ["immutable-x1", "immutable-evidence", "final-delta", "final-owner"],
        "successful_replay_allowed": False, "successor_contact_before_success": False,
    })


def candidate_owner_paths() -> list[Path]:
    paths = [path for path in PHASE_ROOT.rglob("*") if path.is_file()]
    named = [
        ROOT / "scripts/build_ghc_family_elaren_kestrel_v667_v7_x1.py",
        ROOT / "scripts/build_ghc_family_elaren_kestrel_v667_v7_x2.py",
        ROOT / FINAL_BUILDER,
        ROOT / "tests/test_ghc_family_elaren_kestrel_v667_v7_x1.py",
        ROOT / "tests/test_ghc_family_elaren_kestrel_v667_v7_x2.py",
        ROOT / FINAL_TEST,
        ROOT / CANONICAL_RUNNER,
    ]
    named.extend(ROOT / "scripts" / f"ghc_family_elaren_kestrel_v667_v7_{name}.py" for name in ["canonical", "common", "contracts", "manifests", "method_flow", "mutations", "reports", "revalidation", "sources", "tools", "validation"])
    paths.extend(path for path in named if path.is_file())
    return sorted({path.resolve() for path in paths})


def privacy_candidates(path: str, data: bytes) -> list[dict[str, str]]:
    classes = {
        "opaque_task_identifier": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_drive_path": re.compile(rb"\b[A-Z]:(?:\\|/|%5c)", re.I),
        "credential_assignment": re.compile(rb"(?i)(api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*['\"]?[A-Za-z0-9_./+-]{12,}"),
        "raw_thread_or_session_field": re.compile(rb"(?i)(source_thread_id|session_stream|private_callable_id)\s*[:=]"),
        "resume_or_private_route_value": re.compile(rb"(?i)(resume_value|private_route)\s*[:=]\s*['\"]?[^\s'\"]{8,}"),
    }
    return [{"path": path, "class": name} for name, pattern in classes.items() if pattern.search(data)]


def build_candidate() -> None:
    if git_text("rev-parse", "HEAD").strip() != EVIDENCE_HEAD:
        raise RuntimeError("final builder requires the immutable evidence head")
    if git_text("rev-parse", "HEAD^").strip() != X1_HEAD:
        raise RuntimeError("evidence parent is not the frozen x1")
    build_immutable_manifests()
    build_truth_and_closeout()
    build_documents()
    write_json("validation/final-delta-manifest.json", {
        "schema": "ghc-family-final-delta-manifest-v5", "owner": "Elaren Kestrel", "phase": "v667-v7",
        "status": "PREPARED_REQUIRES_STAGED_REVIEW", "base_commit": EVIDENCE_HEAD,
        "exclusions": sorted(CONTROL_EXCLUSIONS), "entry_count": 0, "entries": [],
    })
    write_json("validation/final-owner-manifest.json", {
        "schema": "ghc-family-final-owner-manifest-v5", "owner": "Elaren Kestrel", "phase": "v667-v7",
        "status": "PREPARED_REQUIRES_STAGED_REVIEW", "base_commit": EVIDENCE_HEAD,
        "exclusions": sorted(CONTROL_EXCLUSIONS), "entry_count": 0, "entries": [],
    })
    write_json("validation/final-staged-review.json", {
        "schema": "ghc-family-final-staged-review-v5", "owner": "Elaren Kestrel", "phase": "v667-v7",
        "status": "PREPARED_REQUIRES_EXACT_STAGING", "base_commit": EVIDENCE_HEAD,
        "successor_contacted": False,
    })


def replay_manifest(commit: str, manifest: dict[str, Any]) -> None:
    blobs = git_blobs(commit, [row["path"] for row in manifest["entries"]])
    for row in manifest["entries"]:
        data = blobs[row["path"]]
        if len(data) != row["bytes"] or sha256(data) != row["sha256"]:
            raise AssertionError(f"manifest mismatch: {row['path']}")


def validate_tree(*, allow_placeholders: bool) -> dict[str, Any]:
    required = [
        "closeout/closeout-receipt.json", "closeout/completion-checklist.json", "closeout/final-integrated-overview.md",
        "deck/final-baton-index.json", "handoffs/neris-solane-v667-v8-activation-prepared.md",
        "method-flow/method-flow-state-final.json", "route/route-state.json", "seal/seal-candidate.json",
        "truth/post-evidence-operational-overlay.json", "truth/retained-negative-register-final.json",
        "truth/exact-open-gate-register-final.json", "truth/source-proposal-x1-x2-final-truth.json", "truth/phase-truth-final.json",
        "validation/immutable-x1-manifest.json", "validation/immutable-evidence-manifest.json",
        "validation/final-delta-manifest.json", "validation/final-owner-manifest.json", "validation/final-staged-review.json",
        "validation/final-validation-plan.json", "wellbeing/final-wellbeing-check.json",
    ]
    missing = [path for path in required if not (PHASE_ROOT / path).is_file()]
    if missing:
        raise AssertionError(f"missing final candidate paths: {missing}")
    json_paths = sorted(PHASE_ROOT.rglob("*.json"))
    for path in json_paths:
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise AssertionError(f"JSON root is not object: {rel(path)}")
    expected_counts = {"effective_negatives": 28304, "effective_methods": 14445, "open_gaps": 199, "exact_gates": 197, "failed_witnesses": 588, "passing_witnesses": 1015}
    if final_counts() != expected_counts:
        raise AssertionError(f"final count mismatch: {final_counts()}")
    truth = load("truth/phase-truth-final.json")
    if any(truth[key] != value for key, value in expected_counts.items()):
        raise AssertionError("phase truth count mismatch")
    outcomes = Counter(row["outcome"] for row in load("x2/proposal-outcomes.json")["outcomes"])
    if outcomes != Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}):
        raise AssertionError("outcome distribution mismatch")
    overview = (PHASE_ROOT / "closeout/final-integrated-overview.md").read_text(encoding="utf-8")
    baton_path = PHASE_ROOT / "handoffs/neris-solane-v667-v8-activation-prepared.md"
    baton = baton_path.read_text(encoding="utf-8")
    if len(overview.split()) < 1800:
        raise AssertionError("overview is below three-page-equivalent threshold")
    if not 10000 <= len(baton.split()) <= 100000:
        raise AssertionError("baton word count outside authorized range")
    baton_index = load("deck/final-baton-index.json")
    if baton_index["bytes"] != len(baton_path.read_bytes()) or baton_index["whitespace_words"] != len(baton.split()) or baton_index["sha256"] != sha256(baton_path.read_bytes()):
        raise AssertionError("baton integrity mismatch")
    if baton_index["sent"] or "SENT_BY_ELAREN_KESTREL = false" not in baton:
        raise AssertionError("prepared route delivery truth mismatch")
    route = load("route/route-state.json")
    if route["state"] != "PREPARED_NOT_SENT" or route["delivery_claim"] or route["successor_contacted"]:
        raise AssertionError("premature route claim")
    x1_manifest = load("validation/immutable-x1-manifest.json")
    evidence_manifest = load("validation/immutable-evidence-manifest.json")
    if x1_manifest["entry_count"] != 23 or evidence_manifest["entry_count"] != 385:
        raise AssertionError("immutable manifest count mismatch")
    replay_manifest(X1_HEAD, x1_manifest)
    replay_manifest(EVIDENCE_HEAD, evidence_manifest)
    final_delta = load("validation/final-delta-manifest.json")
    final_owner = load("validation/final-owner-manifest.json")
    staged = load("validation/final-staged-review.json")
    if allow_placeholders:
        if final_delta["status"] not in {"PREPARED_REQUIRES_STAGED_REVIEW", "PASS"} or final_owner["status"] not in {"PREPARED_REQUIRES_STAGED_REVIEW", "PASS"}:
            raise AssertionError("unknown final manifest state")
    elif final_delta["status"] != "PASS" or final_owner["status"] != "PASS" or staged["status"] != "PASS":
        raise AssertionError("final staged controls are not passed")
    candidates: list[dict[str, str]] = []
    for path in candidate_owner_paths():
        candidates.extend(privacy_candidates(rel(path), path.read_bytes()))
    if candidates:
        raise AssertionError(f"privacy candidates: {candidates}")
    return {
        "status": "PASS", "json_documents": len(json_paths), "owner_files": len(candidate_owner_paths()),
        "overview_words": len(overview.split()), "baton_words": len(baton.split()),
        "x1_manifest_entries": x1_manifest["entry_count"], "evidence_manifest_entries": evidence_manifest["entry_count"],
        "final_delta_entries": final_delta["entry_count"], "final_owner_entries": final_owner["entry_count"],
        "staged_status": staged["status"], "privacy_candidates": 0,
    }


def index_blob(path: str) -> bytes:
    result = run_git("show", f":{path}", check=False)
    if result.returncode:
        raise RuntimeError(f"cannot read staged blob: {path}")
    return result.stdout


def staged_review() -> None:
    validate_tree(allow_placeholders=True)
    diff_check = run_git("diff", "--cached", "--check", check=False)
    if diff_check.returncode:
        raise RuntimeError(diff_check.stdout.decode("utf-8", errors="replace") + diff_check.stderr.decode("utf-8", errors="replace"))
    rows = [line for line in git_text("diff", "--cached", "--name-status", EVIDENCE_HEAD).splitlines() if line]
    if not rows:
        raise RuntimeError("no staged final paths")
    staged_paths: list[str] = []
    non_additive: list[str] = []
    for row in rows:
        status, path = row.split("\t", 1)
        staged_paths.append(path)
        if status != "A":
            non_additive.append(f"{status}:{path}")
    if non_additive:
        raise RuntimeError(f"final closeout must be additive: {non_additive}")
    disallowed = [path for path in staged_paths if not owner_path(path)]
    if disallowed:
        raise RuntimeError(f"disallowed final paths: {disallowed}")
    staged_blobs = {path: index_blob(path) for path in staged_paths}
    delta_blobs = {path: data for path, data in staged_blobs.items() if path not in CONTROL_EXCLUSIONS}
    evidence_owner_paths = [path for path in tree_paths(EVIDENCE_HEAD) if owner_path(path)]
    unchanged = [path for path in evidence_owner_paths if path not in staged_blobs and path not in CONTROL_EXCLUSIONS]
    owner_blobs = git_blobs(EVIDENCE_HEAD, unchanged)
    owner_blobs.update(delta_blobs)
    final_owner_paths = sorted((set(evidence_owner_paths) | set(staged_paths)) - CONTROL_EXCLUSIONS)
    if sorted(owner_blobs) != final_owner_paths:
        raise RuntimeError("prospective final owner manifest scope mismatch")
    candidates: list[dict[str, str]] = []
    for path, data in owner_blobs.items():
        candidates.extend(privacy_candidates(path, data))
    if candidates:
        raise RuntimeError(f"staged privacy candidates: {candidates}")
    write_json("validation/final-delta-manifest.json", {
        "schema": "ghc-family-final-delta-manifest-v5", "owner": "Elaren Kestrel", "phase": "v667-v7",
        "status": "PASS", "base_commit": EVIDENCE_HEAD, "scope": "staged final delta Git blobs excluding controls",
        "exclusions": sorted(CONTROL_EXCLUSIONS), "entry_count": len(delta_blobs), "entries": manifest_entries(delta_blobs),
    })
    write_json("validation/final-owner-manifest.json", {
        "schema": "ghc-family-final-owner-manifest-v5", "owner": "Elaren Kestrel", "phase": "v667-v7",
        "status": "PASS", "base_commit": EVIDENCE_HEAD, "scope": "prospective exact-final owner Git blobs excluding controls",
        "exclusions": sorted(CONTROL_EXCLUSIONS), "entry_count": len(owner_blobs), "entries": manifest_entries(owner_blobs),
    })
    write_json("validation/final-staged-review.json", {
        "schema": "ghc-family-final-staged-review-v5", "owner": "Elaren Kestrel", "phase": "v667-v7",
        "generated_at_utc": NOW, "status": "PASS", "base_commit": EVIDENCE_HEAD,
        "staged_path_count": len(staged_paths), "staged_paths": staged_paths,
        "additive_path_count": len(staged_paths), "non_additive_paths": [], "diff_check": "PASS",
        "privacy_class_count": 5, "privacy_candidate_count": 0, "privacy_confirmed_hit_count": 0,
        "immutable_x1_or_evidence_changes": 0, "final_delta_manifest_entries": len(delta_blobs),
        "final_owner_manifest_entries": len(owner_blobs), "manifest_self_exclusions": sorted(CONTROL_EXCLUSIONS),
        "successor_contacted": False,
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--allow-placeholders", action="store_true")
    parser.add_argument("--staged-review", action="store_true")
    args = parser.parse_args()
    if args.staged_review:
        staged_review()
        print(json.dumps({"status": "PASS", "mode": "final-staged-review"}, sort_keys=True))
        return 0
    if args.validate:
        print(json.dumps(validate_tree(allow_placeholders=args.allow_placeholders), sort_keys=True))
        return 0
    build_candidate()
    print(json.dumps({"status": "PASS", "mode": "final-candidate-built"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
