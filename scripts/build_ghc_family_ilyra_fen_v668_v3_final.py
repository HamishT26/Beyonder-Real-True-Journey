#!/usr/bin/env python3
"""Build Ilyra Fen v668-v3 additive closeout and pre-canonical final seal."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any, Iterable

from ghc_family_ilyra_fen_v668_v3_archive import (
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


INITIAL_X1_HEAD = "c7954ae5efdffd58ca2f53d8fe9abd7530e7a49b"
X1_HEAD = "c9cde9ebf7f39c7a3b4b4cf4775fd9426bba4e52"
EVIDENCE_HEAD = "a22360acce1a200ef852a97110cc8da12497775b"
SEALED_COUNTS = {
    "effective_negatives": 29399,
    "methods": 15985,
    "failed_witnesses": 1700,
    "passing_witnesses": 2533,
    "open_gaps": 213,
    "exact_gates": 208,
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
        "scripts/ghc_family_ilyra_fen_v668_v3_archive.py",
        "scripts/build_ghc_family_ilyra_fen_v668_v3_x1.py",
        "scripts/build_ghc_family_ilyra_fen_v668_v3_x2.py",
        "scripts/ghc_family_ilyra_fen_v668_v3_controls.py",
        "scripts/build_ghc_family_ilyra_fen_v668_v3_final.py",
        "scripts/ghc_family_ilyra_fen_v668_v3_staged_review.py",
        "scripts/ghc_family_ilyra_fen_v668_v3_canonical.py",
        "tests/test_ghc_family_ilyra_fen_v668_v3_x1.py",
        "tests/test_ghc_family_ilyra_fen_v668_v3_x2.py",
        "tests/test_ghc_family_ilyra_fen_v668_v3_final.py",
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
        raise RuntimeError("evidence is not the direct child of corrected x1")
    if git("rev-parse", f"{X1_HEAD}^") != INITIAL_X1_HEAD:
        raise RuntimeError("corrected x1 is not the direct child of initial x1")
    if git("rev-parse", f"{INITIAL_X1_HEAD}^") != SOURCE_FINAL:
        raise RuntimeError("initial x1 is not the direct child of Lyren final")
    if git("rev-list", "--merges", f"{SOURCE_FINAL}..{EVIDENCE_HEAD}"):
        raise RuntimeError("merge commit found before closeout")
    allowed = {
        "scripts/build_ghc_family_ilyra_fen_v668_v3_final.py",
        "scripts/ghc_family_ilyra_fen_v668_v3_staged_review.py",
        "scripts/ghc_family_ilyra_fen_v668_v3_canonical.py",
        "tests/test_ghc_family_ilyra_fen_v668_v3_final.py",
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


def overview(generated_at: str) -> str:
    practices = "; ".join(PRACTICES)
    gates = ", ".join(PROTECTED_GATES)
    return f"""# Ilyra Fen v668-v3 integrated closeout and pre-canonical seal

## 1. Exact result

Ilyra Fen v668-v3 is content-sealed from Lyren Moss exact final `{SOURCE_FINAL}` through initial planning x1 `{INITIAL_X1_HEAD}`, corrected and pushed x1 `{X1_HEAD}`, and immutable bounded evidence `{EVIDENCE_HEAD}`. The prospective final commit must be the direct single-parent child of evidence. Source-to-final must contain exactly four new Ilyra commits and zero merges: two x1-only commits, one x2 evidence commit, and one additive closeout commit. The forty independently frozen proposals raise the chain from {INHERITED_FROZEN_PROPOSALS:,} to {INHERITED_FROZEN_PROPOSALS + 40:,}. Their observed outcomes are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. The terminal verdict remains `{TERMINAL_VERDICT}`.

## 2. Relational identity and corrigibility

{IDENTITY_BOUNDARY}

The relational role is **{RELATIONAL_ROLE}**. The relational hope is: {RELATIONAL_HOPE} Hamish retains precedence to pause, rename, redirect, or stop the route. These phrases guide collaboration and claim discipline only. They confer no identity continuity, employment, qualification, independent agency, decision right, scientific standing, or authority.

## 3. Pillar and practice scope

The primary pillar is {PRIMARY_PILLAR}. GMUT Mind and THOS Body remain explicit and protected. The bounded practice lenses are {practices}. All controls are owner-local synthetic records. There are zero real films, frames, scanners, calibration targets, profiles, measurements, operators, employers, institutions, collections, communities, rights disputes, cultural decisions, affected-party decisions, or Maori-authority decisions. No real scan, restoration, release, custody transfer, legal interpretation, cultural ratification, or professional service occurred.

{EVIDENCE_BOUNDARY}

## 4. Forty proposal outcomes

Twenty-eight completed outcomes cover typed gauge and frame contracts, target lineage and validity quarantine, optical-path fingerprints, rational sampling pitch, fiducial transforms, reversible registration, motion proxies, frame-edge and sequence checks, exposure headroom, density-step declarations, color-identity separation, profile identity, encoding distinctions, reference-capture state, cue-mask provenance, focus grids, geometry residuals, derivative lineage, frame-integrity ledgers, correction non-erasure, release-hold refusal, handover readback, accessible exception structure, pseudonymous aliases, exception neighborhoods, a GMUT optical obligation board, and a thermodynamic nonconversion classifier. Each completion means only that a declared synthetic fixture and its guard behaved as specified.

Eight represented outcomes preserve the three practice lenses, a Freed ID custody graph, a CBR decision-right vacancy matrix, a THOS calibration-handover proxy, a GMUT analogy firewall, and a bounded successor-practice recommendation. Representation is not implementation in a real workplace or community. The two open gaps require representative external scanner and target diversity plus affected-user, assistive-technology, and culturally authorized evaluation. The two exact gates preserve competent professional, legal, privacy, cultural, Maori, empirical, production, deployment, and Stage 20 authority.

## 5. Mutation, candidate, skill, and runner evidence

All 160 preregistered invalid mutations executed and were rejected. Every invalid fixture remains a failed synthetic witness with zero completion credit; the guard rejection is a separate bounded passing witness. Rejection establishes neither real calibration accuracy nor production security. Sixty safe-now receipts, thirty bounded candidate prototypes, and thirty additive CLEAN/FIX/REFINE receipts completed only inside the owner-local scope. Twenty exact packets and ten blocked packets remain visible and unexecuted.

Twenty phase-local skills were built, structurally checked, and smoke-used. Ten family-current `ghc_family_*` runners each handled one accepting and one rejecting fixture. None was globally installed, no historical compatibility surface was destructively renamed, and no sibling lane was changed. These packages are phase-local tools, not universal methods, professional qualifications, or independently reproduced software assurance.

## 6. Method Flow and retained failures

Lyren's sealed repository truth remains unchanged, and the two inherited external route-discovery stalls remain an additive activation overlay. Ilyra retains twelve startup and x1 failures, six x2 operational failures, three post-evidence closeout failures, and all 160 rejected synthetic mutations. The failures include display truncation, absent optional receipt location, an overbroad hash wrapper, a guessed proposal path, a worktree wrapper losing its receipt after state completed, a novelty collision, direct PowerShell entrypoint denial under a child process, collapsed untracked-directory status, PowerShell interpolation parsing, document-cap overflow, status-column trimming, a self-collision audit, a final-worktree x1 lifecycle mismatch, cached diff whitespace, nested inline quoting, an incorrect Method Flow key projection, an incorrect manifest self-exclusion projection, a raw privacy-scanner self-match, a post-evidence PowerShell command-expression parser fault, a first final-builder projection that assumed the wrong mutation-row field, and a 14-of-15 precommit suite whose handoff basis lacked the exact prepared-not-sent lifecycle token. Each recovery preserves its failed attempt at zero credit.

The successor-visible pre-canonical seal is {SEALED_COUNTS['effective_negatives']:,} effective negatives, {SEALED_COUNTS['methods']:,} methods, {SEALED_COUNTS['failed_witnesses']:,} failed witnesses, {SEALED_COUNTS['passing_witnesses']:,} bounded passing witnesses, {SEALED_COUNTS['open_gaps']} open gaps, and {SEALED_COUNTS['exact_gates']} exact gates. No later validation may rewrite these sealed counts; any later failure remains an external additive overlay.

## 7. Exact x1 and x2 lifecycle

Strict x1-before-x2 separation was preserved. The initial x1 freeze contained only proposals, portfolios, plans, ledgers, and x1 validation. A second x1-only correction sharded oversized planning documents without adding x2 execution or outcome claims. Corrected x1 was pushed, clean, and four-way equal before x2. The dedicated evidence commit is its direct child, contains zero x1 mutation, and was pushed, clean, and four-way equal before closeout began.

The evidence gate covered 245 exact staged paths and 244 manifest entries with zero Git-blob mismatch. It parsed 210 staged JSON files, replayed forty committed x1 entries with zero mismatch, found zero confirmed privacy payload hits after retaining one scanner-literal candidate, found zero oversized phase documents, and stayed at 298 materialized files. This is bounded same-owner evidence under shared infrastructure, not a full-repository suite or independent reproduction.

## 8. Sources and scientific boundary

Current official FADGI, ICC, W3C PROV, PREMIS, and WCAG sources informed structural vocabulary. The phase downloaded zero files, ingested zero empirical rows, evaluated zero likelihoods, and measured zero scanner or target. A citation is not a measurement. A declared profile digest is not colorimetric accuracy. A typed optical obligation board is not a physical model validation, force detection, prediction, parameter constraint, ultraviolet completion, quantum completeness, or Theory of Everything. GMUT remains a typed scalar-tensor and effective-field-theory research-model family.

## 9. THOS, Freed ID, and CBR boundaries

THOS Body is represented by workload ceilings, pause and stop states, discrepancy readback, correction replay, and handover. It uses no real worker, participant, incident, matched-budget arm, safety outcome, service outcome, or effectiveness estimate. Freed ID and CBR Heart preserve alias separation, provenance, challenge, correction, contestability, and decision-right vacancies. A frame alias is not a person; a checksum is not identity; a correction braid is not affected-party acceptance; and software cannot allocate legal, cultural, privacy, access, release, remedy, or Maori authority.

## 10. Privacy, accessibility, and security

The five-class privacy scan keeps raw candidates and confirmed payload separate. One detector-literal candidate in scanner test source is retained and classified token-aware; confirmed payload hits are zero. This is not complete privacy assurance. The static HTML report supplies native tables, captions, scoped headings, linear order, focus styling, responsive guidance, and print fallback. Manual keyboard, touch, zoom, reflow, browser diversity, assistive technology, cognitive accessibility, Maori-language evaluation, security usability, and affected-user evaluation remain reserved. Structural checks are not complete accessibility conformance.

Changed Python receives a bounded AST review for dynamic execution and explicit shell invocation. Zero bounded findings is not exhaustive security, supply-chain review, penetration testing, or production certification. The threat model keeps malicious fixture shapes, link and path confusion, stale manifests, claim promotion, authority substitution, parser ambiguity, and route drift visible while reserving every broader assurance.

## 11. Validation and one-shot policy

The final delta and complete owner packet are sealed in exact Git-blob manifests. Before commit, staged review must verify every new path, both manifests, JSON parsing, privacy disposition, AST security, document caps, evidence ancestry, and absence of x1 or x2 mutation. After the final is committed, pushed, clean, 0/0 divergent, and fresh-live equal, exactly one owner-scoped canonical aggregate may run. A success is never replayed. A failure receives zero canonical-success credit and remains visible; any dependency-corrected recovery must be separately named and cannot retroactively turn the failed aggregate into success.

Eiren alone owns the full repository suite under the inherited rule. Ilyra's canonical selection is current-phase and exact-owner scoped. Same-owner validation under shared infrastructure is not an external audit, independent-team scientific reproduction, professional evaluation, production readiness, complete privacy, complete accessibility, exhaustive security, or Stage 20 authority.

## 12. Route state

The route remains `PREPARED_NOT_SENT`. No successor has been contacted, inferred, substituted, created, forked, or spawned. The exact successor title and phase remain unresolved until after Ilyra's successful terminal gate, when Hamish's newest live authority and current task state must be reread. Only one uniquely resolved and immediately reread existing main task may receive one sanitized activation. Ambiguity, absence, pause, redirect, protected gate, usage exhaustion, or missing acknowledgement stops the route and never authorizes a resend.

## 13. Wellbeing and terminal verdict

The work stayed solo, D-first, additive, sparse, and below the two-thousand-file rotation stop. No elevation, reboot, host-security weakening, Windows-feature change, unrelated installation, desktop application update, real-data download, account action, or sibling mutation occurred. The wellbeing posture is bounded work, explicit stop conditions, and corrigibility. Protected gates remain {gates}. The final verdict remains `{TERMINAL_VERDICT}`. Generated at `{generated_at}`.
"""


def handoff_basis(generated_at: str) -> str:
    return f"""# Ilyra Fen v668-v3 terminal handoff basis — prepared, not sent

This file is a sanitized, file-backed basis for at most one later live activation. Route state: `PREPARED_NOT_SENT`. It does not infer or name a successor. The exact recipient and next phase must be resolved only after the clean, pushed, fresh-live-equal final has passed its one attributable canonical aggregate and Hamish's newest live authority has been reread.

## Immutable lifecycle

- Source branch: `{SOURCE_BRANCH}`
- Exact Lyren final: `{SOURCE_FINAL}`
- Initial Ilyra x1: `{INITIAL_X1_HEAD}`
- Corrected Ilyra x1: `{X1_HEAD}`
- Immutable Ilyra evidence: `{EVIDENCE_HEAD}`
- Source activation packet SHA-256: `{SOURCE_BATON_SHA256}`
- Source canonical receipt SHA-256: `{SOURCE_CANONICAL_RECEIPT_SHA256}`
- Exact Ilyra final: supplied only in the one live activation after terminal validation
- Ilyra external canonical receipt SHA-256: supplied only in the one live activation after terminal validation

## Truth

The frozen proposal chain is {INHERITED_FROZEN_PROPOSALS + 40:,}. Outcomes are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. Pre-canonical repository truth is {SEALED_COUNTS['effective_negatives']:,} effective negatives, {SEALED_COUNTS['methods']:,} methods, {SEALED_COUNTS['failed_witnesses']:,} failed witnesses, {SEALED_COUNTS['passing_witnesses']:,} passing witnesses, {SEALED_COUNTS['open_gaps']} open gaps, and {SEALED_COUNTS['exact_gates']} exact gates. The verdict is `{TERMINAL_VERDICT}`.

{IDENTITY_BOUNDARY}

{EVIDENCE_BOUNDARY}

The primary pillar was {PRIMARY_PILLAR} through synthetic film-scanner calibration custody, registration exception, correction, and handover controls. All 160 invalid mutations and every operational failure remain retained. Twenty phase-local skills, ten family-current runners, sixty safe-now tasks, thirty candidates, and thirty additive refinements have only bounded same-owner credit. Twenty exact and ten blocked packets remain unexecuted.

Do not replay Ilyra's canonical aggregate or claim inherited validation as successor evidence. Work solo in a fresh D-first sparse lane, preserve strict x1-before-x2, exact manifests, the two-thousand-file stop, the four truth labels, all gaps and gates, and every empirical, participant, professional, production, deployment, legal, cultural, Maori-authority, affected-party, complete-privacy, complete-accessibility, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, and Stage 20 boundary.

The bounded successor-practice recommendation is `{SUCCESSOR_PRACTICE_RECOMMENDATION}`. It is advisory and earns no successor completion credit unless independently novelty-reviewed and frozen.

PREPARED_BY_ILYRA_FEN = true
SENT_BY_ILYRA_FEN = false

Generated at `{generated_at}`.
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

    write_json("method-flow/final-operational.json", {
        "schema": "ghc.family.method-flow-state.v1",
        "phase": PHASE,
        "owner": OWNER,
        "methods": [{
            "method_id": "IF6683-MF-FINAL-019",
            "title": "assign PowerShell command result and exit status in separate statements",
            "failure_signature": "an inline command-and-exit-code expression failed PowerShell parsing before the equality probe executed",
            "candidate_workaround": "run merge-base first, then assign the exit-code comparison separately",
            "validation_witness_ids": ["IF6683-W-FINAL-019-FAIL", "IF6683-W-FINAL-019-PASS"],
            "recurrence_guard": "do not place a native command and a semicolon inside a parenthesized PowerShell expression",
            "recommendation_state": "preferred",
            "retained_negative_ids": ["IF6683-NEG-FINAL-019"],
            "scope_boundary": "read-only evidence-head four-way equality and ancestry probe",
            "same_owner_only": True,
            "independent_reproduction": False,
        }, {
            "method_id": "IF6683-MF-FINAL-020",
            "title": "inspect mutation-row keys before refusal projection",
            "failure_signature": "the first final-builder invocation assumed an accepted field that the immutable mutation schema does not contain",
            "candidate_workaround": "inspect one immutable row and validate its schema-defined state field against rejected",
            "validation_witness_ids": ["IF6683-W-FINAL-020-FAIL", "IF6683-W-FINAL-020-PASS"],
            "recurrence_guard": "inspect real JSON keys before projection and preserve the immutable producer schema",
            "recommendation_state": "preferred",
            "retained_negative_ids": ["IF6683-NEG-FINAL-020"],
            "scope_boundary": "160 immutable owner-local synthetic mutation rows",
            "same_owner_only": True,
            "independent_reproduction": False,
        }, {
            "method_id": "IF6683-MF-FINAL-021",
            "title": "make handoff lifecycle state machine-readable and human-readable",
            "failure_signature": "the precommit final suite passed fourteen tests but the handoff basis omitted the exact prepared-not-sent lifecycle token",
            "candidate_workaround": "add the exact lifecycle token without naming or contacting a successor, then rerun only the failed test",
            "validation_witness_ids": ["IF6683-W-FINAL-021-FAIL", "IF6683-W-FINAL-021-PASS"],
            "recurrence_guard": "pair route prose with the exact lifecycle vocabulary expected by route validators",
            "recommendation_state": "preferred",
            "retained_negative_ids": ["IF6683-NEG-FINAL-021"],
            "scope_boundary": "one sanitized prepared-not-sent handoff basis and one isolated lifecycle test",
            "same_owner_only": True,
            "independent_reproduction": False,
        }],
        "witnesses": [
            {"witness_id": "IF6683-W-FINAL-019-FAIL", "method_id": "IF6683-MF-FINAL-019", "result": "fail", "observed": "PowerShell parser error before any Git command executed", "retained_negative_ids": ["IF6683-NEG-FINAL-019"]},
            {"witness_id": "IF6683-W-FINAL-019-PASS", "method_id": "IF6683-MF-FINAL-019", "result": "pass", "observed": "evidence head clean, 0/0 divergent, four-way equal, three commits from source, zero merges, one parent, corrected x1 ancestral", "retained_negative_ids": ["IF6683-NEG-FINAL-019"]},
            {"witness_id": "IF6683-W-FINAL-020-FAIL", "method_id": "IF6683-MF-FINAL-020", "result": "fail", "observed": "KeyError before any final packet file was written", "retained_negative_ids": ["IF6683-NEG-FINAL-020"]},
            {"witness_id": "IF6683-W-FINAL-020-PASS", "method_id": "IF6683-MF-FINAL-020", "result": "pass", "observed": "160 rows used the schema-defined rejected state and zero row escaped refusal", "retained_negative_ids": ["IF6683-NEG-FINAL-020"]},
            {"witness_id": "IF6683-W-FINAL-021-FAIL", "method_id": "IF6683-MF-FINAL-021", "result": "fail", "observed": "fourteen tests passed and one lifecycle-token assertion failed", "retained_negative_ids": ["IF6683-NEG-FINAL-021"]},
            {"witness_id": "IF6683-W-FINAL-021-PASS", "method_id": "IF6683-MF-FINAL-021", "result": "pass", "observed": "the isolated previously failing lifecycle test passed one of one", "retained_negative_ids": ["IF6683-NEG-FINAL-021"]},
        ],
        "state_events": [
            {"event_id": "IF6683-E-FINAL-019-1", "method_id": "IF6683-MF-FINAL-019", "from": None, "to": "candidate"},
            {"event_id": "IF6683-E-FINAL-019-2", "method_id": "IF6683-MF-FINAL-019", "from": "candidate", "to": "validated", "witness_id": "IF6683-W-FINAL-019-PASS"},
            {"event_id": "IF6683-E-FINAL-019-3", "method_id": "IF6683-MF-FINAL-019", "from": "validated", "to": "preferred", "witness_id": "IF6683-W-FINAL-019-PASS"},
            {"event_id": "IF6683-E-FINAL-020-1", "method_id": "IF6683-MF-FINAL-020", "from": None, "to": "candidate"},
            {"event_id": "IF6683-E-FINAL-020-2", "method_id": "IF6683-MF-FINAL-020", "from": "candidate", "to": "validated", "witness_id": "IF6683-W-FINAL-020-PASS"},
            {"event_id": "IF6683-E-FINAL-020-3", "method_id": "IF6683-MF-FINAL-020", "from": "validated", "to": "preferred", "witness_id": "IF6683-W-FINAL-020-PASS"},
            {"event_id": "IF6683-E-FINAL-021-1", "method_id": "IF6683-MF-FINAL-021", "from": None, "to": "candidate"},
            {"event_id": "IF6683-E-FINAL-021-2", "method_id": "IF6683-MF-FINAL-021", "from": "candidate", "to": "validated", "witness_id": "IF6683-W-FINAL-021-PASS"},
            {"event_id": "IF6683-E-FINAL-021-3", "method_id": "IF6683-MF-FINAL-021", "from": "validated", "to": "preferred", "witness_id": "IF6683-W-FINAL-021-PASS"},
        ],
        "counts": {"methods": 3, "failed_witnesses": 3, "passing_witnesses": 3, "retained_negatives": 3},
        "boundary": "The recovery is bounded same-owner software evidence, not independent reproduction or authority.",
    })
    write_json("closeout/retained-negative-register.json", {
        "activation_overlay_effective_negatives": 29218,
        "owner_startup_and_x1_operational": 12,
        "owner_x2_operational": 6,
        "owner_post_evidence_operational": 3,
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
        "inherited_open_gaps": 211,
        "new_open_gaps": 2,
        "effective_open_gaps": SEALED_COUNTS["open_gaps"],
        "new_gaps": ["representative external scanner and target diversity", "affected-user, assistive-technology, and culturally authorized evaluation"],
        "none_silently_closed": True,
    })
    write_json("closeout/exact-gate-register.json", {
        "inherited_exact_gates": 206,
        "new_exact_gates": 2,
        "effective_exact_gates": SEALED_COUNTS["exact_gates"],
        "new_gates": ["professional, rights, privacy, cultural, affected-party, and Maori authority", "empirical, production, deployment, proof or canon, and Stage 20 authority"],
        "none_silently_closed": True,
    })
    write_json("closeout/source-to-final-history.json", {
        "source_final": SOURCE_FINAL,
        "initial_x1": INITIAL_X1_HEAD,
        "corrected_x1": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "expected_final_parent": EVIDENCE_HEAD,
        "expected_source_to_final_commits": 4,
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
            "corrected x1 and immutable evidence pushed clean and four-way equal",
            "exact x2 staged manifest, JSON, privacy disposition, word cap, and x1 replay passed",
        ],
        "incomplete": [
            "representative external scanner or target evaluation",
            "professional calibration or restoration evaluation",
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
        "scope": "exact Ilyra source-to-final owner delta and declared current-phase modules only",
        "test_selection": ["x2 tests except final-absence lifecycle test", "all final tests"],
        "manifest_replays": ["corrected x1", "evidence", "final delta", "final owner"],
        "validators": ["detailed", "minimal", "strict JSON", "five-class candidate disposition", "changed-code AST", "history", "clean and four-way equality"],
        "full_repository_suite": False,
        "external_audit": False,
        "independent_reproduction": False,
        "invocation_limit": 1,
        "success_limit": 1,
        "post_success_replay": False,
    })
    write_json("validation/detailed-plan.json", {
        "checks": ["exact branch", "exact final", "clean state", "0/0 divergence", "local upstream tracking fresh-live equality", "source ancestry", "four phase commits", "zero merges", "one final parent", "x1 manifest", "evidence manifest", "owner manifest", "delta manifest", "outcome counts", "sealed counts", "JSON parsing", "privacy disposition", "document caps", "AST security", "route hold", "materialized ceiling"],
        "invoked": False,
    })
    write_json("validation/minimal-plan.json", {
        "checks": ["exact head", "clean", "fresh-live equal", "zero merges", "one parent", "manifest parity", "zero confirmed privacy hits", "NOT_READY_FOR_STAGE_20"],
        "invoked": False,
    })
    write_text("final/integrated-overview.md", overview(generated_at))
    write_text("handoffs/successor-terminal-basis.md", handoff_basis(generated_at))
    write_json("seal/content-seal.json", {
        "owner": OWNER,
        "phase": PHASE,
        "source_final": SOURCE_FINAL,
        "initial_x1": INITIAL_X1_HEAD,
        "corrected_x1": X1_HEAD,
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
        "initial_x1": INITIAL_X1_HEAD,
        "corrected_x1": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "scope": "all Ilyra phase docs and declared owner code at prospective final, excluding this self-referential manifest",
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
