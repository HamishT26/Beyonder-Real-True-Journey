#!/usr/bin/env python3
"""Build Sable Rook v668-v5 additive closeout and pre-canonical final seal."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any, Iterable

from ghc_family_sable_rook_v668_v5_archive import (
    ALLOWED_OUTCOMES,
    EVIDENCE_BOUNDARY,
    IDENTITY_BOUNDARY,
    INHERITED_FROZEN_PROPOSALS,
    OWNER,
    PHASE,
    PHASE_ROOT,
    PRACTICES,
    PRIMARY_PILLAR,
    PROTECTED_GATES,
    RELATIONAL_HOPE,
    RELATIONAL_ROLE,
    REL_PHASE_ROOT,
    ROOT,
    RUNNER_NAMES,
    SOURCE_BATON_SHA256,
    SOURCE_BRANCH,
    SOURCE_CANONICAL_RECEIPT_SHA256,
    SOURCE_COMPOSITE_RECEIPT_SHA256,
    SOURCE_FAILED_CANONICAL_RECEIPT_SHA256,
    SOURCE_FINAL,
    SOURCE_LEDGER,
    SUCCESSOR_PRACTICE_RECOMMENDATION,
    TERMINAL_VERDICT,
    git,
    sha256_bytes,
    utc_now,
    write_json,
    write_text,
)


INITIAL_X1_HEAD = "ee15cd2e1c0fd6a9d321bcd9126e8a191832061a"
X1_HEAD = "cd959e4d4cd021e7db4b581e51d2e27e56ad4a17"
EVIDENCE_HEAD = "2743988b71b9816d107ed28fe3623bf2c4488b67"
SEALED_COUNTS = {
    "effective_negatives": 29769,
    "methods": 16355,
    "failed_witnesses": 2070,
    "passing_witnesses": 2897,
    "open_gaps": 217,
    "exact_gates": 212,
}
FINAL_OPERATIONAL_FAILURES = [
    {
        "suffix": "014",
        "title": "preserve explicit PowerShell foreach token boundaries",
        "failure_signature": "a read-only final-template projection omitted the required space after the foreach in token and failed parsing before execution",
        "trigger": "compressed PowerShell loop syntax joins the in keyword to its collection variable",
        "workaround": "use explicit spacing and bounded numbered ranges for the read-only projection",
        "pass_observed": "the complete final builder was projected in bounded ranges without repository mutation",
    },
    {
        "suffix": "015",
        "title": "patch only symbols present in the exact template import block",
        "failure_signature": "a narrow import patch targeted a nonexistent template symbol and was rejected before writing",
        "trigger": "an assumed import name is patched without first matching the exact current block",
        "workaround": "match the exact adjacent imports and add only the older Ilyra failed-receipt constant",
        "pass_observed": "the actual import block contains the required Auren and inherited Ilyra receipt constants and exact Sable anchors",
    },
]


def read_json(relative: str) -> Any:
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def git_blob(commit: str, relative: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{commit}:{relative}"],
        check=True,
        capture_output=True,
    ).stdout


def exists_in_commit(commit: str, relative: str) -> bool:
    return subprocess.run(
        ["git", "-C", str(ROOT), "cat-file", "-e", f"{commit}:{relative}"],
        capture_output=True,
    ).returncode == 0


def projected_blob(path: Path) -> tuple[str, bytes]:
    relative = path.relative_to(ROOT).as_posix()
    if exists_in_commit(EVIDENCE_HEAD, relative):
        if subprocess.run(
            ["git", "-C", str(ROOT), "diff", "--quiet", EVIDENCE_HEAD, "--", relative]
        ).returncode != 0:
            raise RuntimeError(f"immutable evidence path changed during closeout: {relative}")
        data = git_blob(EVIDENCE_HEAD, relative)
        oid = subprocess.run(
            ["git", "-C", str(ROOT), "rev-parse", f"{EVIDENCE_HEAD}:{relative}"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        ).stdout.strip()
        return oid, data
    worktree_data = path.read_bytes()
    hashed = subprocess.run(
        ["git", "-C", str(ROOT), "hash-object", "-w", f"--path={relative}", "--stdin"],
        input=worktree_data,
        check=True,
        capture_output=True,
    ).stdout.decode("ascii").strip()
    data = subprocess.run(
        ["git", "-C", str(ROOT), "cat-file", "blob", hashed],
        check=True,
        capture_output=True,
    ).stdout
    return hashed, data


def manifest_rows(paths: Iterable[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(set(paths)):
        oid, data = projected_blob(path)
        rows.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "git_blob_oid": oid,
                "sha256": sha256_bytes(data),
                "bytes": len(data),
                "canonical_domain": "committed_evidence_or_projected_final_git_blob",
            }
        )
    return rows


def code_paths() -> list[Path]:
    names = [
        "scripts/ghc_family_sable_rook_v668_v5_archive.py",
        "scripts/build_ghc_family_sable_rook_v668_v5_x1.py",
        "scripts/build_ghc_family_sable_rook_v668_v5_x2.py",
        "scripts/ghc_family_sable_rook_v668_v5_controls.py",
        "scripts/build_ghc_family_sable_rook_v668_v5_final.py",
        "scripts/ghc_family_sable_rook_v668_v5_staged_review.py",
        "scripts/ghc_family_sable_rook_v668_v5_canonical.py",
        "tests/test_ghc_family_sable_rook_v668_v5_x1.py",
        "tests/test_ghc_family_sable_rook_v668_v5_x2.py",
        "tests/test_ghc_family_sable_rook_v668_v5_final.py",
    ]
    names.extend(f"scripts/{name}.py" for name in RUNNER_NAMES)
    paths = [ROOT / name for name in names]
    missing = [path.relative_to(ROOT).as_posix() for path in paths if not path.exists()]
    if missing:
        raise RuntimeError(f"declared owner code path missing: {missing}")
    return paths


def assert_evidence_anchor() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE_HEAD:
        raise RuntimeError("final closeout must begin at exact immutable evidence head")
    if git("rev-parse", f"{EVIDENCE_HEAD}^") != X1_HEAD:
        raise RuntimeError("evidence is not the direct child of frozen x1")
    if git("rev-parse", f"{X1_HEAD}^") != INITIAL_X1_HEAD:
        raise RuntimeError("frozen x1 is not the direct child of the authorized source")
    if INITIAL_X1_HEAD != SOURCE_FINAL:
        raise RuntimeError("source alias mismatch")
    if git("rev-list", "--merges", f"{SOURCE_FINAL}..{EVIDENCE_HEAD}"):
        raise RuntimeError("merge commit found before closeout")
    allowed = {
        "scripts/build_ghc_family_sable_rook_v668_v5_final.py",
        "scripts/ghc_family_sable_rook_v668_v5_staged_review.py",
        "scripts/ghc_family_sable_rook_v668_v5_canonical.py",
        "tests/test_ghc_family_sable_rook_v668_v5_final.py",
    }
    allowed_doc_roots = (
        f"{REL_PHASE_ROOT}/closeout/",
        f"{REL_PHASE_ROOT}/final/",
        f"{REL_PHASE_ROOT}/handoffs/",
        f"{REL_PHASE_ROOT}/route/",
        f"{REL_PHASE_ROOT}/seal/",
        f"{REL_PHASE_ROOT}/validation/",
    )
    allowed_doc_exact = {f"{REL_PHASE_ROOT}/method-flow/final-operational.json"}
    lines = git("status", "--porcelain=v1", "--untracked-files=all").splitlines()
    unexpected = []
    for line in lines:
        path = line[3:].replace("\\", "/")
        if path not in allowed and path not in allowed_doc_exact and not path.startswith(allowed_doc_roots):
            unexpected.append(path)
    if unexpected:
        raise RuntimeError(f"unexpected pre-final worktree paths: {unexpected}")


def final_operational_document() -> dict[str, Any]:
    methods = []
    witnesses = []
    events = []
    recommendations = []
    for row in FINAL_OPERATIONAL_FAILURES:
        method_id = f"SR6685-MF-FINAL-{row['suffix']}"
        negative_id = f"SR6685-NEG-FINAL-{row['suffix']}"
        fail_id = f"SR6685-W-FINAL-{row['suffix']}-FAIL"
        pass_id = f"SR6685-W-FINAL-{row['suffix']}-PASS"
        methods.append({
            "method_id": method_id,
            "title": row["title"],
            "failure_signature": row["failure_signature"],
            "trigger_preconditions": [row["trigger"]],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now",
            "candidate_workaround": row["workaround"],
            "validation_witness_ids": [fail_id, pass_id],
            "recurrence_guard": row["workaround"],
            "rollback": "stop, retain the failure, and change only the smallest attributable dependency",
            "recommendation_state": "preferred",
            "supersedes": [],
            "protected_gates": list(PROTECTED_GATES),
            "retained_negative_ids": [negative_id],
            "scope_boundary": "one owner-local closeout dependency",
        })
        witnesses.extend([
            {"witness_id": fail_id, "method_id": method_id, "procedure": row["trigger"], "scope": "owner-local closeout", "expected": "exact attributable result", "observed": row["failure_signature"], "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": "zero credit for the failed operation"},
            {"witness_id": pass_id, "method_id": method_id, "procedure": row["workaround"], "scope": "smallest attributable recovery", "expected": "recover without erasing the failure", "observed": row["pass_observed"], "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": "bounded recovery only"},
        ])
        events.extend([
            {"event_id": f"{method_id}-E1", "method_id": method_id, "from": None, "to": "observed"},
            {"event_id": f"{method_id}-E2", "method_id": method_id, "from": "observed", "to": "candidate"},
            {"event_id": f"{method_id}-E3", "method_id": method_id, "from": "candidate", "to": "validated", "witness_id": pass_id},
            {"event_id": f"{method_id}-E4", "method_id": method_id, "from": "validated", "to": "preferred", "witness_id": pass_id},
        ])
        recommendations.append({"method_id": method_id, "state": "preferred", "reason": "bounded recovery passed without erasing the failure"})
    return {
        "schema": "ghc.family.method-flow-state.v1",
        "phase": PHASE,
        "owner": OWNER,
        "methods": methods,
        "witnesses": witnesses,
        "state_events": events,
        "recommendations": recommendations,
        "counts": {"methods": len(methods), "failed_witnesses": len(methods), "passing_witnesses": len(methods), "retained_negatives": len(methods)},
        "source_commit": EVIDENCE_HEAD,
        "final_commit": "PENDING_FINAL_COMMIT",
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": "Bounded recovery is not independent reproduction, production evidence, authority, or Stage 20 proof.",
    }


def overview(generated_at: str) -> str:
    practices = "; ".join(PRACTICES)
    gates = ", ".join(PROTECTED_GATES)
    return f"""# Sable Rook {PHASE} integrated closeout and pre-canonical seal

## 1. Exact bounded result

Sable Rook {PHASE} is content-sealed from the exact authorized Auren final {SOURCE_FINAL}, through frozen Sable x1 {X1_HEAD}, to immutable bounded Sable x2 evidence {EVIDENCE_HEAD}. The prospective final must be the direct single-parent child of evidence. Source to final must therefore contain exactly three new Sable commits and zero merges: one x1-only freeze, one x2 evidence seal, and one additive closeout. The forty independently novelty-reviewed proposals extend the frozen chain from {INHERITED_FROZEN_PROPOSALS:,} to {INHERITED_FROZEN_PROPOSALS + 40:,}. Outcomes are exactly 28 completed, 8 represented, 2 open_gap, and 2 exact_gate. No fifth label is permitted. The terminal verdict remains {TERMINAL_VERDICT}.

## 2. Relational identity and corrigibility

{IDENTITY_BOUNDARY}

Sable uses they/them in the relational role {RELATIONAL_ROLE}. The relational hope is: {RELATIONAL_HOPE} Hamish retains precedence to rename, pause, redirect, or stop the route. Those phrases guide collaboration, care, traceability, and correction only. They confer no consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, professional status, scientific authority, operational authority, legal authority, cultural authority, affected-party authority, or Maori authority.

## 3. Pillar and practice scope

The primary pillar is {PRIMARY_PILLAR}. The bounded practice lenses are {practices}. THOS Body and Freed ID or CBR Heart remain explicit and protected. Every score, source witness, edition, movement, measure, voice, part, event, cue, rehearsal session, correction, person, organization, right, authority case, and decision in this phase is synthetic. There are zero real scores, manuscripts, editions, parts, performers, rehearsals, recordings, measurements, people, organizations, professional decisions, cultural decisions, affected-party decisions, or Maori-authority decisions. No musical, editorial, rights, release, performance, legal, cultural, remedy, governance, or external decision occurred.

{EVIDENCE_BOUNDARY}

## 4. Forty proposal outcomes

The twenty-eight completed outcomes cover bounded software records for work-edition-instance-part identities, measure and beat addresses, source-witness lineage, part extraction, signature ordering, transposition round trips, exact duration closure, repeat traversal, tempo units, cue aliases, event identities, accidental scope, voice routing, lyric attachment, expression spans, layout and semantic separation, part completeness, instrument timelines, correction non-erasure, variant apparatus, integrity checkpoints, canonical JSON digests, pseudonymous aliases, accessible exception structure, bounded issue queues, rights vacancies, GMUT analogy obligations, and evidence diversity. Completion means only that a declared synthetic fixture and fail-closed guard behaved as specified.

The eight represented outcomes preserve three human-practice lenses, a THOS rehearsal-handover workboard, a Freed ID alias graph, a CBR authority-vacancy matrix, a GMUT analogy firewall, and a thermodynamic nonconversion ledger. Representation is not real implementation, competence, safety, effectiveness, legitimacy, or authority. The two open gaps require representative external score corpora, cross-encoder round trips, rendering, interoperability, performer, engraver, librarian, accessibility, language, cultural-care, and affected-party evaluation. The two exact gates preserve competent rights-holder, professional, legal, cultural, affected-party, and Maori-authority decisions plus the non-substitutable Stage 20 veto.

## 5. Controls, mutations, skills, and runners

Ten owner-local controls accept one declared synthetic fixture and reject one deliberately invalid fixture. They cover score identity, measure addressing, edition lineage, part projection, transposition round trips, exact duration closure, repeat traversal, tempo units, correction events, and authority vacancies. Ten family-current runners invoked the same accept and reject pairs. Twenty phase-local skills were built, structurally checked, and smoke-used without global installation. No historical compatibility surface was renamed or removed.

All 160 preregistered invalid mutations executed and were rejected. Each proposal retains four invalid cases: missing required field, wrong type or domain, forbidden claim promotion, and boundary-order or authority bypass. Every invalid fixture remains a failed witness with zero completion credit. The guard rejection is a separate bounded passing witness and never converts the invalid fixture into success. Sixty safe-now receipts, thirty bounded prototypes, and thirty additive CLEAN, FIX, or REFINE receipts completed only within the owner-local synthetic surface. Twenty exact-approval packets and ten blocked packets remain visible and unexecuted.

## 6. Retained failures and Method Flow

Auren's repository seal remains unchanged; two inherited post-seal route failures remain external and additive in Sable's activation baseline. Sable began with 29,594 effective negatives, 16,180 methods, 1,895 failed witnesses, and 2,722 bounded passing witnesses. Sable retains eleven startup and x1 operational failures, two post-x1 or x2-preparation failures, two post-evidence closeout failures, and all 160 rejected mutations. The eleven early failures include bounded-wrapper truncation, combined guidance projection, PowerShell parser assumptions, elided hashes, two rejected patches, explicit bytecode output, a fixed-point staging cardinality assumption, and a stale-domain scanner false positive over inherited provenance. The x2 failures retain a divergence escape-literal mismatch and an unsupported same-path delete-plus-add patch transaction. The closeout failures retain a compressed foreach parser fault and a nonexistent-import patch target.

Every failure has a retained failed witness with zero credit and a separately bounded recovery witness. State inspection never retroactively turns an ambiguous wrapper result into a successful invocation, and a passing recovery never rewrites its paired failure. The successor-visible pre-canonical repository seal is {SEALED_COUNTS['effective_negatives']:,} effective negatives, {SEALED_COUNTS['methods']:,} methods, {SEALED_COUNTS['failed_witnesses']:,} failed witnesses, {SEALED_COUNTS['passing_witnesses']:,} bounded passing witnesses, {SEALED_COUNTS['open_gaps']} open gaps, and {SEALED_COUNTS['exact_gates']} exact gates. Later validation or routing faults remain external overlays and do not rewrite this seal.

## 7. Strict x1-before-x2 lifecycle

Strict x1-before-x2 separation was preserved. Frozen x1 contains proposals, portfolios, plans, ledgers, source vocabulary, retained startup failures, and x1 validation only. It contains no x2 outcome, execution, evidence, closeout, final, or route-send claim. X1 was committed once, pushed, clean, zero divergent, and equal across local, upstream, tracking, and a fresh live remote read before x2 mutation began.

The evidence commit is the direct child of x1. It contains no x1 mutation. Its pre-stage gate covered exactly 240 paths: 239 evidence-manifest entries and one manifest self-exclusion. The review parsed 205 staged JSON documents, checked 227 staged public documents with a maximum of 3,839 words, found zero confirmed five-class payload hits, parsed thirteen changed Python files with zero bounded dynamic-execution or explicit-shell findings, replayed all 239 staged manifest entries byte-for-byte, and stayed at 284 materialized files. The isolated x2 suite passed 27 of 27 once and was not replayed. Evidence was then pushed clean and four-way equal before closeout began.

## 8. Source and scientific boundaries

Official MEI 5.1, the MusicXML 4.0 Community Group report, Library of Congress BIBFRAME, W3C PROV-DM and Verifiable Credentials 2.0, RFC 8785, and WCAG 2.2 supplied vocabulary and refusal conditions only. The phase downloaded zero files and ingested zero empirical rows. A citation is not a score witness or measurement, a synthetic fixture is not a musically correct or authorized edition, and a declared digest is not authorship, authenticity, rights clearance, or responsibility.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The score-transformation docket is analogy-only and checks declared typing, units, covariance, conservation, stability-domain, identifiability, nuisance-separation, and observation-refusal fields. It computes no spacetime solution, force detection, likelihood, posterior, parameter constraint, ultraviolet completion, quantum completion, empirical confirmation, or Theory of Everything. Same-owner software behavior cannot establish independent scientific reproduction or scientific authority.

## 9. THOS, Freed ID, and CBR boundaries

THOS Body is represented through synthetic edition intake, source-lineage holds, part-projection exceptions, cue-correction readback, bounded retry, pause, stop, and rehearsal handover. It uses no real worker, performer, participant, rehearsal, incident, matched-budget arm, safety outcome, service outcome, release decision, or effectiveness estimate. It establishes no employment, competence, operational safety, musical correctness, or professional authority.

Freed ID and CBR Heart preserve alias separation, provenance, challenge, correction, contestability, access questions, rights and remedy questions, cultural-care vacancies, and decision-right vacancies. A work, edition, source, part, cue, or rehearsal alias is not a person or production credential. A checksum is not identity, authorship, authenticity, or rights clearance. A correction edge is not performer, rights-holder, or affected-party acceptance. Software cannot allocate privacy, access, attribution, release, remedy, legal authority, cultural legitimacy, Maori authority, or affected-party authority.

## 10. Privacy, accessibility, and security

The five-class privacy classifier separates raw candidates from confirmed payload. Its own split scanner literal remains a scanner definition, not private content; confirmed payload hits remain zero. This bounded result is not complete privacy assurance. Durable artifacts omit task IDs, thread IDs, private routes, credentials, transcripts, session streams, resume values, and private absolute paths.

The static report uses a native table, caption, scoped headers, explicit status text, linear reading order, visible focus style, responsive overflow, and print fallback. Manual keyboard, touch, zoom, reflow, browser diversity, assistive technology, cognitive accessibility, Maori-language evaluation, security usability, and affected-user evaluation remain reserved. Structural checks are not complete accessibility conformance. Changed Python receives a bounded AST review for dynamic execution and explicit shell invocation. Zero bounded findings is not exhaustive security, supply-chain review, penetration testing, deployment assurance, or production certification.

## 11. Validation policy

The final delta and complete owner packet are sealed in exact Git-blob manifests. Before commit, staged review must verify every new path, both final manifests, committed x1 and evidence manifests, strict JSON parsing, privacy disposition, AST security, document caps, exact ancestry, staged hygiene, and absence of x1 or x2 mutation. Precommit tests are not the canonical aggregate.

Only after the final is committed, pushed, clean, zero divergent, and equal across local, upstream, tracking, and a fresh live remote read may exactly one attributable owner-scoped canonical aggregate run. A success is never replayed. A failure receives zero canonical-success credit and remains visible; any dependency-corrected recovery must be separately named and cannot retroactively promote the failed aggregate. Eiren alone owns any full-repository suite under the inherited rule. Same-owner validation under shared infrastructure is not external audit, independent reproduction, professional evaluation, production readiness, complete privacy, complete accessibility, exhaustive security, or Stage 20 authority.

## 12. Route state

The repository route remains PREPARED_NOT_SENT. No successor has been contacted, inferred, substituted, created, forked, or spawned. The exact recipient and next phase remain undecided until after the clean, pushed, fresh-live-equal final passes its one attributable canonical aggregate and Hamish's newest live authority and task state are reread. Only one uniquely resolved and immediately reread existing task may receive at most one sanitized activation. Ambiguity, absence, pause, redirect, rename, protected gate, usage exhaustion, or missing acknowledgement stops the route and never authorizes a resend.

## 13. Terminal boundary and wellbeing

The work stayed solo, D-first, additive, sparse, and below the two-thousand-file stop. No elevation, reboot, host-security weakening, Windows-feature change, unrelated installation, desktop-application update, real-data download, account action, sibling mutation, subagent, fork, or new task occurred. The wellbeing posture is bounded work, explicit stop conditions, correction without shame, and Hamish's continuing authority to pause or stop. Protected gates remain {gates}. The terminal verdict remains {TERMINAL_VERDICT}. Generated at {generated_at}.
"""


def handoff_basis(generated_at: str) -> str:
    return f"""# Sable Rook {PHASE} terminal handoff basis — prepared, not sent

This sanitized file-backed basis supports at most one later live activation. Repository route state is PREPARED_NOT_SENT. It does not infer or name a successor. The exact recipient and next phase may be resolved only after the clean, pushed, fresh-live-equal final has passed its one attributable canonical aggregate and Hamish's newest live authority has been reread.

## Immutable lifecycle

- Source branch: {SOURCE_BRANCH}
- Exact inherited Auren final and Sable source: {SOURCE_FINAL}
- Frozen Sable x1: {X1_HEAD}
- Immutable Sable evidence: {EVIDENCE_HEAD}
- Auren terminal-basis SHA-256: {SOURCE_BATON_SHA256}
- Auren external canonical receipt SHA-256: {SOURCE_CANONICAL_RECEIPT_SHA256}
- Inherited Ilyra failed canonical receipt SHA-256: {SOURCE_FAILED_CANONICAL_RECEIPT_SHA256}
- Inherited Ilyra dependency-corrected composite receipt SHA-256: {SOURCE_COMPOSITE_RECEIPT_SHA256}
- Exact Sable final: supplied only in the one live activation after terminal validation
- Sable external canonical receipt SHA-256: supplied only in that activation

## Truth and boundaries

The frozen proposal chain is {INHERITED_FROZEN_PROPOSALS + 40:,}. Outcomes are exactly 28 completed, 8 represented, 2 open_gap, and 2 exact_gate. Pre-canonical repository truth is {SEALED_COUNTS['effective_negatives']:,} effective negatives, {SEALED_COUNTS['methods']:,} methods, {SEALED_COUNTS['failed_witnesses']:,} failed witnesses, {SEALED_COUNTS['passing_witnesses']:,} bounded passing witnesses, {SEALED_COUNTS['open_gaps']} open gaps, and {SEALED_COUNTS['exact_gates']} exact gates. The verdict is {TERMINAL_VERDICT}.

{IDENTITY_BOUNDARY}

{EVIDENCE_BOUNDARY}

The primary pillar was {PRIMARY_PILLAR} through wholly synthetic score-edition lineage, part extraction, cue correction, accessible rehearsal packet, and handover controls. All 160 invalid mutations and all fifteen Sable operational failures remain retained. Twenty phase-local skills, ten family-current runners, sixty safe-now tasks, thirty candidates, and thirty additive refinements have bounded same-owner credit only. Twenty exact packets and ten blocked packets remain unexecuted.

Do not replay Sable's canonical aggregate or treat inherited validation as successor evidence. Work solo in a fresh D-first sparse lane. Preserve strict x1-before-x2 separation, exact manifests, the two-thousand-file stop, the four truth labels, all failures, gaps, and gates, and every empirical, participant, professional, production, deployment, legal, cultural, Maori-authority, affected-party, complete-privacy, complete-accessibility, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof or canon, and Stage 20 boundary.

No successor-practice recommendation is inferred before the terminal live-authority reread. Any later recommendation is advisory and earns no successor completion credit unless independently novelty-reviewed and frozen.

PREPARED_BY_SABLE_ROOK = true
SENT_BY_SABLE_ROOK = false

Generated at {generated_at}.
"""

def main() -> int:
    assert_evidence_anchor()
    generated_at = utc_now()
    truth = read_json("x2/phase-truth.json")
    outcomes = read_json("x2/proposals/outcome-index.json")
    mutation_rows: list[dict[str, Any]] = []
    for path in sorted((PHASE_ROOT / "x2/mutations").glob("results-*.json")):
        mutation_rows.extend(json.loads(path.read_text(encoding="utf-8"))["results"])
    if truth["outcome_counts"] != {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}:
        raise ValueError("x2 outcome counts drifted")
    if outcomes["outcome_counts"] != truth["outcome_counts"]:
        raise ValueError("outcome index and phase truth diverged")
    if len(mutation_rows) != 160 or any(row["state"] != "rejected" for row in mutation_rows):
        raise ValueError("mutation register drifted")

    write_json("method-flow/final-operational.json", final_operational_document())
    write_json("closeout/retained-negative-register.json", {
        "activation_overlay_effective_negatives": 29594,
        "owner_startup_and_x1_operational": 11,
        "owner_x2_operational": 2,
        "owner_post_evidence_operational": 2,
        "owner_synthetic_mutations": 160,
        "effective_negatives_before_canonical": SEALED_COUNTS["effective_negatives"],
        "methods_before_canonical": SEALED_COUNTS["methods"],
        "failed_witnesses_before_canonical": SEALED_COUNTS["failed_witnesses"],
        "passing_witnesses_before_canonical": SEALED_COUNTS["passing_witnesses"],
        "all_failures_retained": True,
        "correction_erases_failure": False,
        "terminal_verdict": TERMINAL_VERDICT,
    })
    write_json("closeout/open-gap-register.json", {
        "inherited_open_gaps": 215,
        "new_open_gaps": 2,
        "effective_open_gaps": SEALED_COUNTS["open_gaps"],
        "new_gaps": ["representative external score corpus, cross-encoder round-trip, rendering, and interoperability evaluation", "performer, engraver, librarian, accessibility, language, cultural-care, and affected-party evaluation"],
        "none_silently_closed": True,
    })
    write_json("closeout/exact-gate-register.json", {
        "inherited_exact_gates": 210,
        "new_exact_gates": 2,
        "effective_exact_gates": SEALED_COUNTS["exact_gates"],
        "new_gates": ["professional, rights, privacy, cultural, affected-party, and Maori authority", "empirical, production, deployment, proof or canon, and Stage 20 authority"],
        "none_silently_closed": True,
    })
    write_json("closeout/source-to-final-history.json", {
        "source_final": SOURCE_FINAL,
        "starting_source": SOURCE_FINAL,
        "frozen_x1": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "expected_final_parent": EVIDENCE_HEAD,
        "expected_source_to_final_commits": 3,
        "hard_commit_ceiling": 8,
        "expected_merge_count": 0,
        "all_phase_commits_single_parent": True,
        "final_hash_supplied_external_after_commit": True,
    })
    write_json("closeout/complete-incomplete-checklist.json", {
        "complete": [
            "forty new proposals frozen and executed within declared bounds",
            "twenty-eight completed and eight represented outcomes recorded",
            "all 160 invalid mutations rejected and retained",
            "twenty local skills and ten family-current runners smoke-used",
            "sixty safe-now, thirty candidates, and thirty additive refinements completed",
            "frozen x1 and immutable evidence pushed clean and four-way equal",
            "exact x2 staged manifest, JSON, privacy disposition, word cap, and x1 replay passed",
        ],
        "incomplete": [
            "representative external score corpus, cross-encoder round-trip, rendering, or interoperability evaluation",
            "performer, engraver, ensemble-library, editorial, or rehearsal evaluation",
            "affected-user and assistive-technology evaluation",
            "legal, cultural, affected-party, and Maori-authority decisions",
            "complete privacy, complete accessibility, exhaustive security, or independent reproduction",
            "empirical GMUT, production, deployment, Theory of Everything, AGI or ASI, consciousness or personhood, proof or canon, and Stage 20",
        ],
        "terminal_verdict": TERMINAL_VERDICT,
    })
    write_json("final/phase-truth.json", {
        "owner": OWNER,
        "phase": PHASE,
        "allowed_outcomes": list(ALLOWED_OUTCOMES),
        "outcome_counts": truth["outcome_counts"],
        "frozen_proposal_chain": INHERITED_FROZEN_PROPOSALS + 40,
        "repository_sealed_counts": SEALED_COUNTS,
        "primary_pillar": PRIMARY_PILLAR,
        "practices": list(PRACTICES),
        "terminal_verdict": TERMINAL_VERDICT,
        "protected_gates": list(PROTECTED_GATES),
        "canonical_validation_invoked": False,
        "successor_contacted": False,
    })
    write_json("final/wellbeing.json", {
        "owner": OWNER,
        "relational_role": RELATIONAL_ROLE,
        "relational_hope": RELATIONAL_HOPE,
        "workload_state": "bounded solo closeout",
        "stop_conditions": ["Hamish pause or redirect", "usage exhaustion", "protected gate", "route ambiguity", "canonical failure"],
        "no_independent_agency_claim": True,
        "identity_boundary": IDENTITY_BOUNDARY,
    })
    write_json("final/accessibility-reservation.json", {
        "structural_report": "x2/reports/accessible-static-report.html",
        "structural_checks": ["native table", "caption", "scoped headings", "linear reading order", "focus styling", "responsive guidance", "print fallback"],
        "reserved": ["manual keyboard", "touch", "zoom", "reflow", "browser diversity", "assistive technology", "cognitive accessibility", "Maori language", "security usability", "affected-user evaluation"],
        "complete_accessibility_claim": False,
    })
    write_json("final/environment-receipt.json", {
        "python": "Python 3.12.10",
        "git": "git version 2.55.0.windows.2",
        "node": "v24.18.0",
        "codex_cli": "codex-cli 0.149.0",
        "verified_only": True,
        "desktop_application_updated_by_phase": False,
        "elevation": False,
        "host_security_changed": False,
        "windows_feature_changed": False,
        "unrelated_software_installed": False,
        "rebooted": False,
        "external_empirical_data_downloaded": False,
    })
    write_json("final/threat-model.json", {
        "assets": ["immutable x1", "immutable evidence", "exact manifests", "retained failures", "authority vacancies", "route state"],
        "bounded_threats": ["malformed fixture", "stale lineage", "manifest drift", "path confusion", "claim promotion", "authority substitution", "parser ambiguity", "route drift", "scanner self-match"],
        "controls": ["Git-blob manifests", "strict x1-before-x2", "exact staged allowlist", "token-aware candidate disposition", "AST changed-code review", "one-shot canonical guard", "prepared-not-sent route"],
        "residual": ["parent-directory races", "supply chain", "production environment", "real adversaries", "external audit", "complete privacy", "exhaustive security"],
        "production_security_claim": False,
    })
    write_json("final/source-ledger.json", {
        "sources": SOURCE_LEDGER,
        "downloads": 0,
        "empirical_rows": 0,
        "measurements": 0,
        "likelihoods": 0,
        "citations_are_evidence_of_observation": False,
    })
    write_json("final/portfolio-receipt.json", {
        "safe_now_completed": 60,
        "candidates_completed_boundedly": 30,
        "skills_built_and_smoke_used": 20,
        "runners_built_and_accept_reject_used": 10,
        "clean_fix_refine_completed_additively": 30,
        "exact_packets_unexecuted": 20,
        "blocked_packets_unexecuted": 10,
        "global_installations": 0,
        "sibling_mutations": 0,
    })
    write_json("route/prepared-route-state.json", {
        "state": "PREPARED_NOT_SENT",
        "owner": OWNER,
        "phase": PHASE,
        "successor_exact_title": "UNRESOLVED_UNTIL_TERMINAL_GATE",
        "successor_phase": "UNRESOLVED_UNTIL_TERMINAL_GATE",
        "successor_contacted": False,
        "task_created": False,
        "fork_created": False,
        "subagent_spawned": False,
        "standby_contacted": False,
        "live_authority_reread_required_after_canonical": True,
        "exact_title_unique_resolution_and_immediate_reread_required": True,
        "single_send_maximum": 1,
        "hamish_pause_redirect_rename_stop_precedence": True,
    })
    write_json("validation/validation-credit.json", {
        "state": "NOT_INVOKED",
        "canonical_invocation_count": 0,
        "canonical_success_count": 0,
        "post_success_replay_allowed": False,
        "receipt_location": "external D-first receipt bank; private absolute path omitted",
        "same_owner_only": True,
        "full_repository_suite": False,
        "independent_reproduction_credit": 0,
    })
    write_json("validation/canonical-plan.json", {
        "scope": "exact Sable source-to-final owner delta and declared current-phase modules only",
        "test_selection": ["x2 tests except final-absence lifecycle test", "all final tests"],
        "manifest_replays": ["frozen x1", "evidence", "final delta", "final owner"],
        "validators": ["detailed", "minimal", "strict JSON", "five-class candidate disposition", "changed-code AST", "history", "clean and four-way equality"],
        "full_repository_suite": False,
        "external_audit": False,
        "independent_reproduction": False,
        "invocation_limit": 1,
        "success_limit": 1,
        "post_success_replay": False,
    })
    write_json("validation/detailed-plan.json", {
        "checks": ["exact branch", "exact final", "clean state", "0/0 divergence", "local upstream tracking fresh-live equality", "source ancestry", "three phase commits", "zero merges", "one final parent", "x1 manifest", "evidence manifest", "owner manifest", "delta manifest", "outcome counts", "sealed counts", "JSON parsing", "privacy disposition", "document caps", "AST security", "route hold", "materialized ceiling"],
        "invoked": False,
    })
    write_json("validation/minimal-plan.json", {
        "checks": ["exact head", "clean", "fresh-live equal", "zero merges", "one parent", "manifest parity", "zero confirmed privacy hits", "NOT_READY_FOR_STAGE_20"],
        "invoked": False,
    })
    write_text("final/integrated-overview.md", overview(generated_at))
    write_text("handoffs/successor-terminal-basis.md", handoff_basis(generated_at))
    write_json("final/privacy-candidate-disposition.json", {
        "raw_candidates": 1,
        "scanner_literal_candidates": 1,
        "confirmed_payload_hits": 0,
        "dispositions": [{
            "path": "tests/test_ghc_family_sable_rook_v668_v5_x2.py",
            "class": 5,
            "classification": "split scanner-definition literal inside test source",
            "confirmed_payload": False,
        }],
        "complete_privacy_claim": False,
    })
    write_json("seal/content-seal.json", {
        "owner": OWNER,
        "phase": PHASE,
        "source_final": SOURCE_FINAL,
        "starting_source": SOURCE_FINAL,
        "frozen_x1": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "expected_final_parent": EVIDENCE_HEAD,
        "owner_manifest": f"{REL_PHASE_ROOT}/validation/final-owner-manifest.json",
        "delta_manifest": f"{REL_PHASE_ROOT}/validation/final-delta-manifest.json",
        "self_hash_claim": False,
        "terminal_verdict": TERMINAL_VERDICT,
    })
    write_json("seal/final-receipt.json", {
        "state": "CONTENT_SEALED_PENDING_EXACT_FINAL_CANONICAL",
        "owner": OWNER,
        "phase": PHASE,
        "repository_sealed_counts": SEALED_COUNTS,
        "route_state": "PREPARED_NOT_SENT",
        "canonical_invoked": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": TERMINAL_VERDICT,
    })

    owner_manifest_path = PHASE_ROOT / "validation/final-owner-manifest.json"
    delta_manifest_path = PHASE_ROOT / "validation/final-delta-manifest.json"
    all_owner = [path for path in PHASE_ROOT.rglob("*") if path.is_file()] + code_paths()
    all_owner = [path for path in all_owner if path not in {owner_manifest_path, delta_manifest_path}]
    delta_paths = [path for path in all_owner if not exists_in_commit(EVIDENCE_HEAD, path.relative_to(ROOT).as_posix())]
    delta_rows = manifest_rows(delta_paths)
    write_json("validation/final-delta-manifest.json", {
        "phase": PHASE,
        "expected_parent": EVIDENCE_HEAD,
        "scope": "exact prospective final content excluding both manifest files",
        "entry_count": len(delta_rows),
        "entries": delta_rows,
        "self_exclusions": [
            f"{REL_PHASE_ROOT}/validation/final-delta-manifest.json",
            f"{REL_PHASE_ROOT}/validation/final-owner-manifest.json",
        ],
        "generated_at": generated_at,
    })
    owner_rows = manifest_rows([*all_owner, delta_manifest_path])
    write_json("validation/final-owner-manifest.json", {
        "phase": PHASE,
        "source_final": SOURCE_FINAL,
        "starting_source": SOURCE_FINAL,
        "frozen_x1": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "scope": "all Sable phase docs and declared owner code at prospective final, excluding this self-referential manifest",
        "entry_count": len(owner_rows),
        "entries": owner_rows,
        "self_exclusions": [f"{REL_PHASE_ROOT}/validation/final-owner-manifest.json"],
        "materialized_or_owner_scope_ceiling": 2000,
        "generated_at": generated_at,
    })
    basis = PHASE_ROOT / "handoffs/successor-terminal-basis.md"
    print(json.dumps({
        "state": "FINAL_PACKET_BUILT_PRE_CANONICAL",
        "final_delta_entries": len(delta_rows),
        "owner_manifest_entries": len(owner_rows),
        "handoff_basis_sha256": sha256_bytes(basis.read_bytes()),
        "handoff_basis_words": len(basis.read_text(encoding="utf-8").split()),
        "sealed_counts": SEALED_COUNTS,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
