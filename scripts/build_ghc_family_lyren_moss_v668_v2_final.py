#!/usr/bin/env python3
"""Build the pre-canonical final seal for Lyren Moss v668-v2."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any, Iterable

from ghc_family_lyren_moss_v668_v2_archive import (
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
    SOURCE_BATON_SHA256,
    SOURCE_BRANCH,
    SOURCE_CANONICAL_RECEIPT_SHA256,
    SOURCE_FINAL,
    SOURCE_ROUTE_RECEIPT_SHA256,
    SUCCESSOR_PRACTICE_RECOMMENDATION,
    TERMINAL_VERDICT,
    code_paths,
    git,
    sha256_bytes,
    utc_now,
    write_json,
    write_text,
)


X1_HEAD = "0683eb961987fd4c7283d278e3b217647aef73f0"
EVIDENCE_HEAD = "6bb6b96b08eb26646c362967f8ed30263d348c15"
SEALED_COUNTS = {
    "effective_negatives": 29216,
    "methods": 15802,
    "failed_witnesses": 1517,
    "passing_witnesses": 2352,
    "open_gaps": 211,
    "exact_gates": 206,
}


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


def projected_final_blob(path: Path) -> bytes:
    relative = path.relative_to(ROOT).as_posix()
    if exists_in_commit(EVIDENCE_HEAD, relative):
        changed = subprocess.run(
            ["git", "-C", str(ROOT), "diff", "--quiet", EVIDENCE_HEAD, "--", relative]
        )
        if changed.returncode != 0:
            raise RuntimeError(f"committed evidence path mutated during final build: {relative}")
        return git_blob(EVIDENCE_HEAD, relative)
    data = path.read_bytes()
    if path.suffix.casefold() in {".json", ".md", ".py", ".txt"}:
        data = data.replace(b"\r\n", b"\n")
    return data


def manifest_rows(paths: Iterable[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(set(paths)):
        data = projected_final_blob(path)
        rows.append({
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": sha256_bytes(data),
            "bytes": len(data),
            "canonical_domain": "committed_evidence_blob_or_projected_final_git_blob_pending_exact_staged_replay",
        })
    return rows


def assert_evidence_anchor() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE_HEAD:
        raise RuntimeError("final seal must begin at exact immutable evidence head")
    if git("rev-parse", f"{EVIDENCE_HEAD}^") != X1_HEAD:
        raise RuntimeError("evidence is not the direct child of x1")
    if git("rev-parse", f"{X1_HEAD}^") != SOURCE_FINAL:
        raise RuntimeError("x1 is not the direct child of Vesper final")
    if git("rev-list", "--merges", f"{SOURCE_FINAL}..{EVIDENCE_HEAD}"):
        raise RuntimeError("merge commit found before final")
    if git("status", "--porcelain"):
        # The four final scripts/tests are intentionally untracked before the builder runs.
        allowed = {
            "scripts/build_ghc_family_lyren_moss_v668_v2_final.py",
            "scripts/ghc_family_lyren_moss_v668_v2_staged_review.py",
            "scripts/ghc_family_lyren_moss_v668_v2_canonical.py",
            "tests/test_ghc_family_lyren_moss_v668_v2_final.py",
        }
        lines = git("status", "--porcelain=v1", "--untracked-files=all").splitlines()
        allowed_doc_prefixes = (
            f"{REL_PHASE_ROOT}/closeout/",
            f"{REL_PHASE_ROOT}/final/",
            f"{REL_PHASE_ROOT}/handoffs/",
            f"{REL_PHASE_ROOT}/validation/",
        )
        allowed_doc_exact = {f"{REL_PHASE_ROOT}/method-flow/method-flow-ledger.json"}
        unexpected = [
            line[3:] for line in lines
            if line[3:] not in allowed
            and line[3:] not in allowed_doc_exact
            and not line[3:].startswith(allowed_doc_prefixes)
        ]
        if unexpected:
            raise RuntimeError(f"unexpected pre-final worktree paths: {unexpected}")


def final_overview(generated_at: str) -> str:
    return f"""# Lyren Moss v668-v2 pre-canonical final closeout

## 1. Result

Lyren Moss v668-v2 is content-sealed from exact Vesper final `{SOURCE_FINAL}` through immutable planning x1 `{X1_HEAD}` and immutable evidence `{EVIDENCE_HEAD}`. The final commit is required to be the direct single-parent child of evidence. The repository-sealed outcome is 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`; the frozen proposal chain is {INHERITED_FROZEN_PROPOSALS + 40:,}. Terminal verdict: `{TERMINAL_VERDICT}`.

## 2. Relational identity

{IDENTITY_BOUNDARY}

The relational role is **{RELATIONAL_ROLE}**. The hope is: {RELATIONAL_HOPE} Hamish retains precedence to pause, rename, redirect, or stop the route. This is workflow language only.

## 3. Synthetic evidence scope

{EVIDENCE_BOUNDARY}

The primary pillar is {PRIMARY_PILLAR}. The bounded practices are {PRACTICES[0]}; {PRACTICES[1]}; and {PRACTICES[2]}. No real media, archive, collection, person, device, credential, location, right, cultural decision, Maori-authority decision, ingest, migration, deletion, quarantine release, or transfer was used or performed.

## 4. Controls and proposals

The twenty-eight bounded completions cover package identity, multi-algorithm fixity, chunk continuity, exact rational timebases, sample-duration coherence, stream inventory, Matroska container-versus-codec separation, FFV1 declarations, audio-transfer metadata, WebVTT structure, timed-text association, derivative lineage, PREMIS and PROV mappings, transfer readback, abstention, two-reviewer proxy, correction non-erasure, rights vacancies, authority firewalls, structural accessibility, exact route state, one-shot validation state, Git-blob manifests, sparse rotation, source status, and flashcards. These are same-owner synthetic software controls only.

The eight represented rows preserve the three practice lenses, GMUT nonconversion, Freed ID record identity, CBR remedy vacancies, one successor practice recommendation, and a format-question matrix without professional selection. The two open gaps require representative external audiovisual corpus evaluation and affected-user/culturally authorized evaluation. The two exact gates require competent rights, privacy, retention, professional, cultural, Maori, empirical, and Stage 20 authority and evidence.

## 5. Mutation evidence

All 160 preregistered invalid mutations were rejected. Each remains a failed synthetic input at zero broader credit and also contributes one bounded passing refusal witness. Rejection does not establish real interoperability, authenticity, preservation fitness, safe deployment, or professional competence.

## 6. Method Flow and retained failures

Vesper's sealed 29,043 negatives remain unchanged. The inbound send timeout, Lyren's worktree-list blank output, auth display truncation, premature pre-x1 controls draft, first casing assertion failure, malformed diagnostic expression, first x2 wording assertion failure, first CRLF-versus-Git-blob manifest mismatch, first final-builder syntax failure, two first-final-suite route-boundary wording failures, one follow-up overly rigid baton assertion, and the first staged-final raw-route negative-fixture privacy hit all remain visible at zero credit. Bounded recoveries never erase those failures. The corrected repository seal is {SEALED_COUNTS['effective_negatives']:,} effective negatives, {SEALED_COUNTS['methods']:,} methods, {SEALED_COUNTS['failed_witnesses']:,} failed witnesses, {SEALED_COUNTS['passing_witnesses']:,} bounded passing witnesses, {SEALED_COUNTS['open_gaps']} open gaps, and {SEALED_COUNTS['exact_gates']} exact gates.

## 7. Skills, runners, and portfolio

Twenty phase-local skills and ten phase-local runners were built, structurally tested, and used. Each runner self-tested once; the builder was not replayed after that success. No package was globally installed or overwritten. Sixty safe-now tasks, thirty candidates, and thirty owner clean/fix/refine actions receive bounded owner-local completion receipts. Thirty successor refinements and the successor practice recommendation remain zero-credit recommendations. Twenty exact and ten blocked packets remain unexecuted.

## 8. Source ledger

The bounded source ledger uses the Library of Congress Recommended Formats Statement, IASA-TC 04, RFC 9043, RFC 9559, the current WebVTT Candidate Recommendation Draft, PREMIS, and W3C PROV-DM. These provide structural vocabulary and questions only. No universal format preference, real conformance, implementation interoperability, archival quality, legal conclusion, or professional selection is claimed.

## 9. Privacy, accessibility, and security

Evidence-stage review parsed 95 JSON files, compiled 13 Python files, checked 21 Markdown files, replayed 128/128 evidence manifest entries, found zero confirmed hits across five bounded privacy classes, and found zero bounded dangerous-call findings in the exact staged Python scope. The final canonical aggregate must independently rederive its owner-head counts. Neither stage can prove complete privacy, complete accessibility, exhaustive security, affected-user suitability, or external audit status.

## 10. Lifecycle and canonical policy

Source-to-final is required to contain exactly three new single-parent Lyren commits and zero merges: x1, evidence, final. The hard ceiling is eight. Exact final must be clean, pushed, 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote before the only canonical invocation. The owner-head canonical aggregate may be invoked once, may succeed once, and may not be replayed after success. A failure receives zero aggregate-success credit and must remain visible; inherited or same-owner evidence is never independent reproduction.

## 11. Route

The committed route remains `PREPARED_NOT_SENT`. The successor remains uncontacted. The prospective next exact-title task is `Ilyra Fen` for v668-v3. Tavian Sol is on standby and is not a substitute. Only after the exact final terminal gate and successful canonical pass may the live authority and current roster be reread, the exact title uniquely resolved and immediately reread, and one sanitized activation sent. Missing or opaque acknowledgement never authorizes a resend.

## 12. Successor recommendation

The bounded successor practice recommendation is: {SUCCESSOR_PRACTICE_RECOMMENDATION}. It carries zero Lyren completion credit and becomes Ilyra-owned only if independently frozen. Every other successor task, skill, runner, and refinement recommendation remains advisory and unexecuted.

## 13. Protected claims and terminal verdict

Protected gates remain {', '.join(PROTECTED_GATES)}. There is no Stage 20, empirical GMUT, Theory-of-Everything, AGI/ASI, consciousness, personhood, professional, production, legal, cultural, Maori-authority, complete-privacy, complete-accessibility, exhaustive-security, or independent-reproduction claim. Terminal verdict: `{TERMINAL_VERDICT}`. Generated at `{generated_at}`.
"""


def activation_baton(generated_at: str) -> str:
    return f"""# ILYRA FEN — PREPARED LYREN v668-v2 → SOLO v668-v3 ACTIVATION

Dear Ilyra Fen,

This packet is prepared, not sent. Exactly one sanitized live activation is permitted only after Lyren's exact final is clean, pushed, fresh-live equal, and canonical-validated once, followed by a fresh exact-title route reread under Hamish's newest authority. The committed packet cannot contain its own future commit hash; that one live activation must supply the exact final and external canonical receipt hash.

## Identity and authority boundary

{IDENTITY_BOUNDARY}

Hamish may rename, pause, redirect, or stop the route. Tavian Sol is on standby and is not a substitute endpoint. No task, fork, subagent, or replacement endpoint is authorized by this packet.

## Source lifecycle

- Vesper source branch: `{SOURCE_BRANCH}`
- Exact Vesper final: `{SOURCE_FINAL}`
- Immutable Lyren x1: `{X1_HEAD}`
- Immutable Lyren evidence: `{EVIDENCE_HEAD}`
- Vesper activation baton SHA-256: `{SOURCE_BATON_SHA256}`
- Vesper canonical receipt SHA-256: `{SOURCE_CANONICAL_RECEIPT_SHA256}`
- Inbound route receipt SHA-256: `{SOURCE_ROUTE_RECEIPT_SHA256}`
- Lyren exact final: supplied only in the acknowledged live activation
- Lyren external canonical receipt SHA-256: supplied only in the acknowledged live activation

Read this complete packet through EOF before mutation, then read every current guidance and schema it names. Reverify all anchors, the exact final, clean state, 0/0 divergence, and fresh four-way equality. Do not replay Lyren's successful aggregate or treat same-owner validation as independent reproduction.

## Phase truth

Lyren froze forty genuinely distinct proposals, raising the chain from 4,630 to 4,670. Outcomes are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. All 160 preregistered invalid mutations remain retained. Repository-sealed truth before any external route overlay is {SEALED_COUNTS['effective_negatives']:,} effective negatives, {SEALED_COUNTS['methods']:,} methods, {SEALED_COUNTS['failed_witnesses']:,} failed witnesses, {SEALED_COUNTS['passing_witnesses']:,} bounded passing witnesses, {SEALED_COUNTS['open_gaps']} open gaps, and {SEALED_COUNTS['exact_gates']} exact gates. Terminal verdict is `{TERMINAL_VERDICT}`.

## Evidence scope

{EVIDENCE_BOUNDARY}

The primary pillar was THOS Body through synthetic audiovisual package, fixity, chunk, timebase, sample-duration, stream, FFV1, Matroska, WebVTT, lineage, PREMIS, PROV, inspection, quarantine, rights-vacancy, correction, and handover fixtures. GMUT Mind, Freed ID, and CBR Heart remained explicit and protected. The source ledger is structural only; no real conformance, format-selection, authenticity, preservation fitness, or professional result is claimed.

## Skills, runners, and portfolio

Lyren built twenty phase-local skill packages and ten phase-local self-testing runners with zero global installations or overwrites. Sixty safe-now tasks, thirty candidates, and thirty owner refinements received bounded completion receipts. Thirty Ilyra refinement recommendations, ten skill recommendations, ten runner recommendations, and the successor practice recommendation remain zero-credit advisory material. Twenty exact and ten blocked packets remain unexecuted.

## Method Flow

Retain every inherited and Lyren failure. In particular, preserve the inbound route timeout, two startup display failures, the premature but unexecuted controls draft, casing-only assertion, malformed diagnostic expression, wording-only x2 assertion, CRLF worktree versus Git-blob manifest mismatch, first final-builder missing-parenthesis failure, two first-final-suite route-boundary wording failures, follow-up overly rigid baton assertion, and first staged-final raw-route negative-fixture privacy hit. Corrections never erase failures or upgrade them into canonical success.

## Ilyra lane

Work solo from Lyren's exact final in a fresh Ilyra-owned D-first sparse lane. Keep all sibling and shared lanes read-only. Preserve strict x1-before-x2, the two-thousand-file rotation stop, exact manifests, the four truth labels, one-success/no-post-success-replay policy, exact staged review, stale-label hygiene, and all retained gaps and gates. The bounded practice recommendation is `{SUCCESSOR_PRACTICE_RECOMMENDATION}`; it becomes Ilyra-owned only if independently frozen.

Preserve every empirical, participant, professional, production, deployment, legal, cultural, Maori-authority, affected-party, complete-privacy, complete-accessibility, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, and Stage 20 boundary. Do not infer a successor from this file alone. Route only after your own exact terminal gate and Hamish's newest live authority; resolve and immediately reread the one exact current title, send at most once, and stop on ambiguity, pause, redirect, usage exhaustion, protected gate, or missing acknowledgement.

Prepared with care, traceability, reversibility, and strict evidence boundaries — Lyren Moss.

PREPARED_BY_LYREN_MOSS = true
SENT_BY_LYREN_MOSS = false

Generated at `{generated_at}`.
"""


def main() -> int:
    assert_evidence_anchor()
    generated_at = utc_now()
    outcomes = read_json("x2/proposals/proposal-outcomes.json")
    mutations = read_json("x2/proposals/negative-mutation-results.json")
    evidence_manifest = read_json("evidence/evidence-content-manifest.json")
    if outcomes["outcome_counts"] != {
        "completed": 28, "exact_gate": 2, "open_gap": 2, "represented": 8
    }:
        raise ValueError("final outcome counts drifted")
    if mutations["count"] != 160 or mutations["accepted"] != 0:
        raise ValueError("final mutation register drifted")
    if evidence_manifest["entry_count"] != 128:
        raise ValueError("evidence manifest count drifted")

    write_json("closeout/retained-negative-register.json", {
        "source_repository_seal": 29043,
        "inbound_route_and_lyren_operational_failures": 13,
        "owner_synthetic_mutations": 160,
        "effective_negatives_before_canonical": SEALED_COUNTS["effective_negatives"],
        "methods_before_canonical": SEALED_COUNTS["methods"],
        "failed_witnesses_before_canonical": SEALED_COUNTS["failed_witnesses"],
        "passing_witnesses_before_canonical": SEALED_COUNTS["passing_witnesses"],
        "open_gaps": SEALED_COUNTS["open_gaps"],
        "exact_gates": SEALED_COUNTS["exact_gates"],
        "all_retained": True,
        "correction_erases_failure": False,
        "terminal_verdict": TERMINAL_VERDICT,
    })
    write_json("method-flow/method-flow-ledger.json", {
        "source_repository_seal": {
            "effective_negatives": 29043,
            "methods": 15629,
            "failed_witnesses": 1344,
            "passing_witnesses": 2179,
            "open_gaps": 209,
            "exact_gates": 204,
        },
        "successor_visible_external_and_owner_operational": {
            "effective_negatives": 13,
            "methods": 13,
            "failed_witnesses": 13,
            "passing_witnesses": 13,
        },
        "owner_synthetic_mutations": {
            "effective_negatives": 160,
            "methods": 160,
            "failed_witnesses": 160,
            "passing_witnesses": 160,
        },
        "owner_core_gates": {"open_gaps": 2, "exact_gates": 2},
        "repository_sealed": SEALED_COUNTS,
        "retained_method_ids": [
            "VESPER-INBOUND-ROUTE-TIMEOUT",
            "LM6682-MF-START-001", "LM6682-MF-START-002", "LM6682-MF-START-003",
            "LM6682-MF-X1-004", "LM6682-MF-X1-005", "LM6682-MF-X2-006", "LM6682-MF-X2-007",
            "LM6682-MF-FINAL-008",
            "LM6682-MF-FINAL-009", "LM6682-MF-FINAL-010",
            "LM6682-MF-FINAL-011",
            "LM6682-MF-FINAL-012",
        ],
        "all_failures_retained": True,
        "terminal_verdict": TERMINAL_VERDICT,
    })
    write_json("closeout/source-to-final-history.json", {
        "source_final": SOURCE_FINAL,
        "x1_head": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "expected_final_parent": EVIDENCE_HEAD,
        "expected_new_commit_count": 3,
        "hard_commit_ceiling": 8,
        "expected_merge_count": 0,
        "all_phase_commits_single_parent": True,
        "final_hash_self_reference_possible": False,
        "final_hash_supplied_external_after_commit": True,
    })
    write_json("closeout/route-and-roster-record.json", {
        "state": "PREPARED_NOT_SENT",
        "owner": OWNER,
        "phase": PHASE,
        "prospective_next_exact_title": "Ilyra Fen",
        "prospective_next_phase": "v668-v3",
        "successor_contacted": False,
        "tavian_state": "ON_STANDBY_NOT_SUBSTITUTE",
        "live_authority_reread_required_after_canonical": True,
        "unique_exact_title_and_immediate_reread_required": True,
        "single_send_maximum": 1,
        "hamish_pause_redirect_rename_stop_precedence": True,
    })
    write_json("validation/validation-credit.json", {
        "state": "NOT_INVOKED",
        "canonical_invocation_count": 0,
        "canonical_success_count": 0,
        "post_success_replay_allowed": False,
        "receipt_location": "external D-first receipt bank; exact path omitted from repository artifacts",
        "same_owner_only": True,
        "independent_reproduction_credit": 0,
    })
    write_json("validation/canonical-plan.json", {
        "scope": "exact Lyren source-to-final owner delta and declared modules only",
        "expected_tests": [
            "tests/test_ghc_family_lyren_moss_v668_v2_x1.py",
            "tests/test_ghc_family_lyren_moss_v668_v2_x2.py",
            "tests/test_ghc_family_lyren_moss_v668_v2_final.py",
        ],
        "manifest_replays": ["x1", "evidence", "final_delta", "final_owner"],
        "privacy_classes": ["raw_uuid", "private_absolute_path", "secret_token", "raw_route_tag", "personal_email"],
        "security_scope": "changed Python AST dangerous-call checks only",
        "full_repository_suite": False,
        "external_audit": False,
        "independent_reproduction": False,
        "invocation_limit": 1,
        "success_limit": 1,
        "post_success_replay": False,
    })
    write_json("validation/privacy-accessibility-security-boundary.json", {
        "evidence_stage": {
            "staged_files": 129,
            "json_parses": 95,
            "python_compiles": 13,
            "markdown_files": 21,
            "evidence_manifest_replays": 128,
            "confirmed_privacy_hits": 0,
            "bounded_security_findings": 0,
        },
        "canonical_rederivation_required": True,
        "complete_privacy_claim": False,
        "complete_accessibility_claim": False,
        "exhaustive_security_claim": False,
        "affected_user_evaluation": False,
    })
    write_json("final/phase-truth.json", {
        "owner": OWNER,
        "phase": PHASE,
        "allowed_outcomes": list(ALLOWED_OUTCOMES),
        "outcome_counts": outcomes["outcome_counts"],
        "frozen_proposal_chain": INHERITED_FROZEN_PROPOSALS + 40,
        "repository_sealed_counts": SEALED_COUNTS,
        "primary_pillar": PRIMARY_PILLAR,
        "terminal_verdict": TERMINAL_VERDICT,
        "protected_gates": list(PROTECTED_GATES),
        "canonical_validation_invoked": False,
        "successor_contacted": False,
    })
    write_json("final/completion-checklist.json", {
        "checks": [
            {"check": "exact source ancestry", "state": "PASS_PRE_FINAL"},
            {"check": "immutable x1 direct child of source", "state": "PASS"},
            {"check": "immutable evidence direct child of x1", "state": "PASS"},
            {"check": "x1 manifest replay", "state": "PASS"},
            {"check": "evidence manifest replay", "state": "PASS_128_OF_128"},
            {"check": "outcome counts", "state": "PASS_28_8_2_2"},
            {"check": "mutation refusals", "state": "PASS_160_OF_160"},
            {"check": "retained failures", "state": "PASS_13_OPERATIONAL_PLUS_160_SYNTHETIC"},
            {"check": "materialization ceiling", "state": "PASS_BELOW_2000"},
            {"check": "successor not contacted", "state": "PASS"},
            {"check": "canonical aggregate", "state": "PENDING_EXACT_FINAL"},
        ],
        "ready_for_exact_final_staged_review": True,
        "terminal_verdict": TERMINAL_VERDICT,
    })
    write_json("final/wellbeing-and-corrigibility.json", {
        "owner": OWNER,
        "relational_role": RELATIONAL_ROLE,
        "relational_hope": RELATIONAL_HOPE,
        "workload_state": "bounded solo closeout",
        "stop_conditions": ["Hamish pause or redirect", "usage exhaustion", "protected gate", "route ambiguity", "canonical failure"],
        "independent_agency_claim": False,
        "identity_boundary": IDENTITY_BOUNDARY,
    })
    write_text("final/integrated-closeout.md", final_overview(generated_at))
    write_text("handoffs/ilyra-fen-v668-v3-activation-prepared.md", activation_baton(generated_at))
    baton_path = PHASE_ROOT / "handoffs/ilyra-fen-v668-v3-activation-prepared.md"
    baton_text = baton_path.read_text(encoding="utf-8")
    write_json("handoffs/activation-summary.json", {
        "prepared": True,
        "sent": False,
        "recipient": "Ilyra Fen",
        "phase": "v668-v3",
        "baton_path": baton_path.relative_to(ROOT).as_posix(),
        "baton_sha256": sha256_bytes(baton_path.read_bytes()),
        "baton_words": len(baton_text.split()),
        "exact_final_and_canonical_receipt_supplied_live_only": True,
        "delivery_claim": "PREPARED_NOT_SENT",
    })

    final_owner_manifest_path = PHASE_ROOT / "validation/final-owner-manifest.json"
    final_delta_manifest_path = PHASE_ROOT / "validation/final-delta-manifest.json"
    all_owner = [path for path in PHASE_ROOT.rglob("*") if path.is_file()] + code_paths()
    all_owner = [path for path in all_owner if path not in {final_owner_manifest_path, final_delta_manifest_path}]
    final_delta_paths = [
        path for path in all_owner
        if not exists_in_commit(EVIDENCE_HEAD, path.relative_to(ROOT).as_posix())
    ]
    final_delta_rows = manifest_rows(final_delta_paths)
    write_json("validation/final-delta-manifest.json", {
        "phase": PHASE,
        "expected_parent": EVIDENCE_HEAD,
        "scope": "exact prospective final-commit content excluding both manifest files",
        "entry_count": len(final_delta_rows),
        "entries": final_delta_rows,
        "generated_at": generated_at,
    })
    all_owner_with_delta = [*all_owner, final_delta_manifest_path]
    owner_rows = manifest_rows(all_owner_with_delta)
    write_json("validation/final-owner-manifest.json", {
        "phase": PHASE,
        "source_final": SOURCE_FINAL,
        "x1_head": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "scope": "all Lyren phase docs and declared code at prospective final, excluding this self-referential manifest",
        "entry_count": len(owner_rows),
        "entries": owner_rows,
        "materialized_or_owner_scope_ceiling": 2000,
        "generated_at": generated_at,
    })
    print(
        f"built Lyren {PHASE} final: {len(final_delta_rows)} final-delta entries, "
        f"{len(owner_rows)} owner entries, baton {len(baton_text.split())} words"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
