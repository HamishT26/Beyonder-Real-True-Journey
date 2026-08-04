#!/usr/bin/env python3
"""Build the Auren Lark v660-v8 combined closeout and seal candidate.

The builder is intentionally final-candidate only.  It never sends a task
message, never changes Git history, and never treats a passing software check
as empirical, professional, legal, cultural, Māori-authority, identity,
accessibility-complete, privacy-complete, or Stage 20 evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v660_v8_x2_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
SOURCE_FINAL = d.SOURCE_FINAL
X1_COMMIT = d.X1_FREEZE
EVIDENCE_COMMIT = "b0dc07da5bd4001fda25bb2c9e74c2b972726755"
SUCCESSOR = "Sable Rook"
SUCCESSOR_PHASE = "v661-v1"
ROUTE_STATE = "AUTHORIZED_TERMINAL_GATED_NOT_CONTACTED"
ROUTE_AUTHORIZED = True

# Append only failures actually observed after the immutable evidence commit.
# No closeout failure is predeclared before that lifecycle begins.
CLOSEOUT_FAILURES: list[dict[str, Any]] = [
    {
        "method_id": "V6608-CLOSEOUT-METHOD-001",
        "negative_id": "V6608-CLOSEOUT-N001",
        "signature": "first-evidence-placeholder-verification-crossed-the-short-wrapper-and-returned-no-attributable-projection",
        "failed_witness": "V6608-CLOSEOUT-METHOD-001-F01",
        "passing_witness": "V6608-CLOSEOUT-METHOD-001-P01",
        "recovery": "Retain the empty projection at zero credit, verify each declared template through a bounded literal read, then run one session-aware changed-path probe.",
        "recurrence_guard": "Use explicit thirty-second session-aware wrapper metadata for closeout placeholder and changed-path verification.",
        "rollback": "Leave the immutable evidence commit untouched and withhold closeout if any placeholder or out-of-scope changed path remains.",
        "recovery_passed": True,
    },
    {
        "method_id": "V6608-CLOSEOUT-METHOD-002",
        "negative_id": "V6608-CLOSEOUT-N002",
        "signature": "first-exact-index-audit-deadlocked-while-writing-a-complete-cat-file-request-stream-before-consuming-its-output",
        "failed_witness": "V6608-CLOSEOUT-METHOD-002-F01",
        "passing_witness": "V6608-CLOSEOUT-METHOD-002-P01",
        "recovery": "Retain the hung audit at zero credit, end only its verified process chain, and recover the manifest dependency with subprocess communication that consumes output concurrently.",
        "recurrence_guard": "Use communicate-style full-duplex handling or a dedicated concurrent reader for Git batch protocols; never fill one pipe while leaving the reciprocal pipe unread.",
        "rollback": "Leave the immutable evidence commit and staged candidate unchanged, stop closeout, and withhold the final commit if any raw staged blob remains unverified.",
        "recovery_passed": True,
    },
    {
        "method_id": "V6608-CLOSEOUT-METHOD-003",
        "negative_id": "V6608-CLOSEOUT-N003",
        "signature": "session-interrupt-request-was-rejected-because-the-unified-process-backend-did-not-support-process-interrupt",
        "failed_witness": "V6608-CLOSEOUT-METHOD-003-F01",
        "passing_witness": "V6608-CLOSEOUT-METHOD-003-P01",
        "recovery": "Retain the rejected interrupt at zero credit, resolve the exact hung parent and child process ancestry read-only, stop only those verified process identifiers, and confirm the process set is absent.",
        "recurrence_guard": "Prefer bounded tools whose subprocess protocol cannot deadlock; if a bounded process must be ended, verify its exact ancestry and start context before stopping only that process set.",
        "rollback": "Do not stop broad or unresolved processes; leave repository state untouched and withhold closeout if the exact hung process set cannot be distinguished safely.",
        "recovery_passed": True,
    },
    {
        "method_id": "V6608-CLOSEOUT-METHOD-004",
        "negative_id": "V6608-CLOSEOUT-N004",
        "signature": "first-split-topology-recovery-wrapper-completed-without-an-attributable-output-projection",
        "failed_witness": "V6608-CLOSEOUT-METHOD-004-F01",
        "passing_witness": "V6608-CLOSEOUT-METHOD-004-P01",
        "recovery": "Retain the empty projection at zero credit, materialize the exact staged list separately, and run one bounded session-aware concurrent topology probe with explicit exit and stderr projections.",
        "recurrence_guard": "Project the nested command result and session identifier explicitly whenever repository-scale Git reads may exceed the initial wrapper window.",
        "rollback": "Preserve the staged candidate without committing and stop if any recovered topology command lacks an attributable exit, stderr view, or exact result set.",
        "recovery_passed": True,
    },
    {
        "method_id": "V6608-CLOSEOUT-METHOD-005",
        "negative_id": "V6608-CLOSEOUT-N005",
        "signature": "one-read-only-status-wrapper-had-a-malformed-object-property-and-raised-a-javascript-syntax-error-before-process-launch",
        "failed_witness": "V6608-CLOSEOUT-METHOD-005-F01",
        "passing_witness": "V6608-CLOSEOUT-METHOD-005-P01",
        "recovery": "Retain the wrapper syntax failure at zero credit, correct only the malformed property delimiter, then launch and poll the same read-only status command to an attributable zero exit.",
        "recurrence_guard": "Keep orchestration object keys syntactically uniform and surface the complete nested result when a command may yield a reusable session.",
        "rollback": "Because no subprocess launched and no repository state changed, retain the failure and withhold any status claim until a corrected read-only probe completes.",
        "recovery_passed": True,
    },
    {
        "method_id": "V6608-CLOSEOUT-METHOD-006",
        "negative_id": "V6608-CLOSEOUT-N006",
        "signature": "first-additive-closeout-ledger-patch-used-a-nonexistent-list-comma-context-and-was-rejected-before-mutation",
        "failed_witness": "V6608-CLOSEOUT-METHOD-006-F01",
        "passing_witness": "V6608-CLOSEOUT-METHOD-006-P01",
        "recovery": "Retain the rejected patch at zero credit, read the exact list terminator, then apply the same additive ledger change against the observed comma-free context.",
        "recurrence_guard": "Read the narrow exact edit window immediately before patching whenever generated or recently staged source may differ in punctuation from an assumed context.",
        "rollback": "A rejected patch changes no file; preserve that state and withhold regeneration until the corrected narrow patch is verified.",
        "recovery_passed": True,
    },
    {
        "method_id": "V6608-CLOSEOUT-METHOD-007",
        "negative_id": "V6608-CLOSEOUT-N007",
        "signature": "final-scalar-receipt-projection-guessed-an-absent-privacy-scanned-file-count-key-before-exact-schema-key-recovery",
        "failed_witness": "V6608-CLOSEOUT-METHOD-007-F01",
        "passing_witness": "V6608-CLOSEOUT-METHOD-007-P01",
        "recovery": "Retain the key error at zero credit, inspect the exact privacy receipt key set, then project files_scanned and the length of definition_candidates with safe exact-key access.",
        "recurrence_guard": "Inspect receipt keys before selecting scalar counts whenever a schema version has not already been projected in the current closeout lifecycle.",
        "rollback": "The failed read changed no state; withhold the scalar summary until the corrected exact-key projection completes.",
        "recovery_passed": True,
    },
]

FINAL_CODE = [
    "scripts/build_ghc_family_v660_v8_closeout.py",
    "scripts/ghc_family_v660_v8_final_validator.py",
    "tests/test_ghc_family_v660_v8_closeout.py",
]

GENERATED = [
    f"{d.PHASE_ROOT}/closeout/closeout-receipt.json",
    f"{d.PHASE_ROOT}/deliverables/v660-v8-integrated-overview.md",
    f"{d.PHASE_ROOT}/final/complete-incomplete-checklist.json",
    f"{d.PHASE_ROOT}/final/environment-version-receipt.json",
    f"{d.PHASE_ROOT}/final/final-gate-register.json",
    f"{d.PHASE_ROOT}/final/final-method-flow-summary.json",
    f"{d.PHASE_ROOT}/final/final-phase-truth.json",
    f"{d.PHASE_ROOT}/final/final-proposal-ledger.json",
    f"{d.PHASE_ROOT}/final/final-retained-negative-register.json",
    f"{d.PHASE_ROOT}/final/final-source-ledger.json",
    f"{d.PHASE_ROOT}/final/final-threat-model.json",
    f"{d.PHASE_ROOT}/final/final-validation-prerequisites.json",
    f"{d.PHASE_ROOT}/final/final-wellbeing-check.json",
    f"{d.PHASE_ROOT}/handoffs/sable-rook-v661-v1-activation.md",
    f"{d.PHASE_ROOT}/lifecycle/phase-anchor-contract.json",
    f"{d.PHASE_ROOT}/orchestration/roster-route-state.json",
    f"{d.PHASE_ROOT}/reports/accessible-static-report-final.html",
    f"{d.PHASE_ROOT}/route/prepared-route.json",
    f"{d.PHASE_ROOT}/seal/seal-receipt.json",
    f"{d.PHASE_ROOT}/validation/final-canonical-selection.json",
    f"{d.PHASE_ROOT}/validation/final-delta-manifest.json",
    f"{d.PHASE_ROOT}/validation/final-document-cap.json",
    f"{d.PHASE_ROOT}/validation/final-owner-manifest.json",
    f"{d.PHASE_ROOT}/validation/final-privacy-scan.json",
    f"{d.PHASE_ROOT}/validation/final-staged-review.json",
    f"{d.PHASE_ROOT}/validation/final-stale-label-review.json",
]

MANIFEST_EXCLUSIONS = {
    f"{d.PHASE_ROOT}/validation/final-delta-manifest.json",
    f"{d.PHASE_ROOT}/validation/final-owner-manifest.json",
    f"{d.PHASE_ROOT}/validation/final-privacy-scan.json",
    f"{d.PHASE_ROOT}/validation/final-staged-review.json",
}

FAMILY_RUNNERS = {
    f"scripts/{name}" for name, _purpose in d.SELF_RUNNER_SPECS
}


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        stderr=subprocess.PIPE,
    ).strip()


def write_json(relative: str, payload: Any) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def clean_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def record(path: Path) -> dict[str, Any]:
    payload = clean_bytes(path)
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
    }


def words(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text, flags=re.UNICODE))


def assert_base() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE_COMMIT:
        raise RuntimeError(f"closeout requires exact evidence head {EVIDENCE_COMMIT}")
    if git("rev-parse", f"{EVIDENCE_COMMIT}^") != X1_COMMIT:
        raise RuntimeError("evidence is not the direct child of the frozen x1 commit")
    if git("rev-parse", f"{X1_COMMIT}^") != SOURCE_FINAL:
        raise RuntimeError("x1 is not the direct child of the immutable source final")
    if git("rev-list", "--count", f"{SOURCE_FINAL}..{EVIDENCE_COMMIT}") != "2":
        raise RuntimeError("source-to-evidence history is not exactly two commits")
    if git("rev-list", "--merges", "--count", f"{SOURCE_FINAL}..{EVIDENCE_COMMIT}") != "0":
        raise RuntimeError("source-to-evidence history contains a merge")


def owner_paths() -> list[Path]:
    paths = [p for p in PHASE.rglob("*") if p.is_file()]
    for pattern in ("*v660_v8*.py",):
        paths.extend((ROOT / "scripts").glob(pattern))
        paths.extend((ROOT / "tests").glob(pattern))
    paths.extend(ROOT / relative for relative in FAMILY_RUNNERS)
    return sorted(set(paths), key=lambda p: p.relative_to(ROOT).as_posix())


def final_paths() -> list[Path]:
    return sorted(
        {ROOT / relative for relative in [*FINAL_CODE, *GENERATED] if (ROOT / relative).is_file()},
        key=lambda p: p.relative_to(ROOT).as_posix(),
    )


def manifest(paths: list[Path], lifecycle: str) -> dict[str, Any]:
    rows = [record(path) for path in paths if path.relative_to(ROOT).as_posix() not in MANIFEST_EXCLUSIONS]
    return {
        "schema": "ghc.family.content-manifest.v2",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "lifecycle": lifecycle,
        "entry_count": len(rows),
        "entries": rows,
        "exclusions": sorted(MANIFEST_EXCLUSIONS),
        "hash_domain": "Git-clean LF-normalized text bytes",
        "boundary": "Exact declared owner files only; explicit self-referential exclusions are not hidden coverage.",
    }


def privacy_scan(paths: list[Path]) -> dict[str, Any]:
    patterns = {
        "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/]"),
        "credential": re.compile(r"(?:(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}|(?<![A-Za-z0-9])ghp_[A-Za-z0-9]{20,}|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY)"),
        "private_route_identifier": re.compile(r"(?:thread_id|task_id|agent_id|resume_token|private_callable)[\"']?\s*[:=]\s*[\"']?(?!(?:V\d|false\b|true\b|null\b|\[REDACTED_SECRET\]))[A-Za-z0-9_-]{24,}", re.I),
        "transcript_or_session": re.compile(r"(?:raw transcript|session stream|private app state)", re.I),
    }
    hits: list[dict[str, str]] = []
    candidates: list[dict[str, str]] = []
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        if relative.endswith("validation/final-privacy-scan.json"):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for label, pattern in patterns.items():
            if not pattern.search(text):
                continue
            if relative in {
                "scripts/build_ghc_family_v660_v8_x1.py",
                "scripts/build_ghc_family_v660_v8_x2.py",
                "scripts/build_ghc_family_v660_v8_closeout.py",
                "scripts/ghc_family_v660_v8_final_validator.py",
            }:
                candidates.append({"path": relative, "class": label, "adjudication": "scanner_definition"})
            elif label == "transcript_or_session" and (
                relative.endswith("sable-rook-v661-v1-activation.md")
                or "exact-and-blocked-register" in relative
                or relative.endswith("preregistration/task-portfolios.json")
                or relative == "scripts/ghc_family_v660_v8_data.py"
            ):
                candidates.append({"path": relative, "class": label, "adjudication": "prohibition_boundary_vocabulary"})
            else:
                hits.append({"path": relative, "class": label})
    return {
        "schema": "ghc.family.privacy-scan.v1",
        "scope": "all Auren v660-v8 owner files at the final candidate",
        "files_scanned": len([p for p in paths if not p.as_posix().endswith("final-privacy-scan.json")]),
        "classes": list(patterns),
        "definition_candidates": candidates,
        "confirmed_hits": hits,
        "confirmed_hit_count": len(hits),
        "privacy_complete": False,
        "boundary": "Five-class owner-file scanning is bounded evidence, not complete privacy or exhaustive security assurance.",
    }


def build_overview(truth: dict[str, Any], outcomes: dict[str, Any], flow: dict[str, Any]) -> str:
    sections = [
        ("Relational identity and phase", f"Auren Lark ({d.PRONOUNS}) is relational working language for a {d.ROLE}, with the hope to {d.HOPE}. This language is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or scientific, operational, legal, cultural, or Māori authority. Hamish may rename, pause, redirect, or stop the route. The phase is solo v660-v8, and every repository result remains bounded by the exact evidence recorded here."),
        ("Source and lifecycle", f"The immutable Ilyra v660-v7 source is `{SOURCE_FINAL}`. Auren froze x1 at `{X1_COMMIT}` and committed x2 evidence at `{EVIDENCE_COMMIT}`. The intended final is one combined closeout and seal commit directly after evidence, making three Auren single-parent commits and zero merges from source. X1 was pushed, clean, and four-way equal before x2. Evidence was separately pushed, clean, and four-way equal before closeout. The final canonical phase-scoped aggregate remains unrun until the exact final is pushed and remote-equal."),
        ("Forty-row program truth", "The forty-row program is not forty new proposals. Twenty selected inherited Ilyra v660-v7 rows were revalidated with zero Auren novelty and zero Auren completion credit. Twenty genuinely new Auren proposals extend the frozen chain from 3,270 to 3,290. Their outcomes are exactly 14 completed, 4 represented, 1 open gap, and 1 exact gate. Only the permitted outcome vocabulary is used."),
        ("Primary practice and Freed ID/CBR Heart", f"The primary pillar was {d.PRIMARY_PILLAR}. The bounded practice lens was {d.PRACTICE_LENS}. Synthetic contracts covered dossier and revision aliases, position-state ledgers, move transitions, algebraic notation, variation trees, position and termination claims, correction lineage, game-record provenance, clock uncertainty, physical-action refusal, accessible review, study handover, evidence admission, and rights, rating, and cultural-authority reservations. They involved zero real players, opponents, guardians, coaches, arbiters, organizers, federations, platforms, games, positions, boards, pieces, clocks, accounts, events, ratings, titles, fair-play records, publications, professional decisions, legal decisions, cultural decisions, or external actions. THOS remains proxy-only without blind matched-budget real arms, governed participants or operators, safety monitoring, statistics, and independent review."),
        ("GMUT Mind", "GMUT surfaces were typed symbolic and mutation contracts for synthetic chess-state and transition-graph obligation proxies, units, covariance, identifiability, domains, generators, reachability, symmetry, invariants, cycles, closure, boundary conditions, and observation firewalls. They establish no engine result, detected force, physical object, likelihood, parameter constraint, unique prediction, universal chess or physical law, stability theorem, empirical confirmation, quantum or ultraviolet completion, Theory of Everything, proof, or canon. Represented GMUT rows remain represented because no real game, calibrated observation, likelihood evidence, uncertainty propagation, independent review, or physical observation exists."),
        ("Freed ID and CBR Heart", "Freed ID and CBR surfaces used fabricated dossier, position, move, game-record, correction, source, rights, disclosure-hold, and deterministic-digest aliases. There were no real keys, signatures, proofs, credentials, issuance, resolution, status, revocation, interoperability, recovery, privacy review, independent security review, or trust-governance decisions. CBR, attribution, game and result credit, participation, ratings, titles, fair-play review, safeguarding, publication, records, traditional knowledge, remedy, affected-party legitimacy, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain exact-gated."),
        ("Falsification and negative retention", f"All 100 preregistered synthetic mutations were executed and rejected or quarantined. {len(d.X2_OPERATIONAL_FAILURES)} x2 operational failures, {len(d.STARTUP_FAILURES)} x1 startup or lifecycle failures, and {len(CLOSEOUT_FAILURES)} closeout failures remain retained at zero credit. The effective negative count is {truth['effective_negatives']:,}; the Method Flow count is {truth['effective_methods']:,}. The x1/x2 Method Flow has {flow['counts']['methods']} preferred bounded methods, {flow['counts']['witness_results']['fail']} failed witnesses, and {flow['counts']['witness_results']['pass']} passing witnesses; {len(CLOSEOUT_FAILURES)} additional closeout methods each retain one failed and one passing witness. Recovery never erases a failure or creates independent reproduction credit."),
        ("Gates and truth", f"The final candidate preserves {truth['effective_open_gaps']} open gaps and {truth['effective_exact_gates']} exact gates. Real evidence remains an open gap. The empty-chair authority matrix remains an exact gate. Empirical, participant, professional, production, deployment, identity, legal, cultural, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, and Stage 20 boundaries remain open or exact-gated. The terminal verdict remains `NOT_READY_FOR_STAGE_20`."),
        ("Portfolios and tools", "Thirty owner safe-now tasks, ten owner candidates, ten phase-local skills, ten family-current runners, and thirty additive CLEAN/FIX/REFINE tasks were bounded and executed only where evidence permitted. The Meta Tool Box validates phase-local skill and runner cards while retaining any lexical overlap findings for explicit review without selecting a silent winner. Reflection Remaster produces a current structural inventory and no automatic promotion. Ten exact-approval and five blocked packets remain visible and unexecuted. Phase-local skills were not globally installed."),
        ("Accessibility, privacy, and security", "The static report uses semantic landmarks, headings, a skip link, text alternatives for status, table captions, and a print-safe structure. Manual keyboard, browser-diverse, assistive-technology, cognitive, language, Māori-language, and affected-user evaluation remain reserved. Five-class scanning and a synthetic threat model are bounded checks only. They establish neither complete privacy nor exhaustive security."),
        ("Evidence semantics", "A completed label means only that the declared synthetic or structural acceptance rule passed for the exact owner-local fixture and that all five declared mutations were rejected. A represented label means an interface or protocol shape exists while the evidence needed for effectiveness, interoperability, safety, accessibility, privacy, professional fitness, or real-world use does not. An open gap means evidence could in principle be supplied later but is absent now. An exact gate means repository work cannot substitute for competent or affected-party authority. None of these labels is a moral rank, a scientific discovery, an entitlement to action, or permission to treat silence as consent."),
        ("Recovery doctrine", "Every failed wrapper, parser assumption, count assumption, manifest assumption, and document-floor miss remains a separate negative witness. A passing narrow recovery is stored beside the failure and never overwrites it. Recovery is limited to the failed dependency unless broader impact is demonstrated. The branch history is additive and single-parent; no failure is removed with reset, rewrite, force push, amend, destructive cleanup, or sibling mutation. Rollback means stopping at the last immutable anchor, preserving evidence, and leaving people, property, external services, rights, and authority unchanged."),
        ("Wellbeing and workload", "The workload check records a bounded solo software phase rather than a claim about inner experience or human health. Work was divided at immutable x1 and x2 anchors, long-running builders were polled rather than duplicated, failed aggregates earned zero credit, and exact approval packets remained unexecuted. The relational hope to keep claims testable, failures visible, and authority boundaries intact is a working orientation only. Hamish may pause or stop the route. No pace target, portfolio floor, or baton length can authorize unsafe filler, concealment, sleep deprivation, real-world intervention, or continued work after a protected gate."),
        ("Validation and route", "The exact final must first be committed, pushed, clean, zero-divergence, and local/upstream/tracking/fresh-live equal. One dependency-justified phase-scoped canonical completion may then run once; a complete success is never replayed. Current authorization allocates this Auren phase-scoped aggregate but not an inherited full repository suite. Hamish's acknowledged Ilyra activation authorizes exactly one terminal-gated Auren-to-Sable v661-v1 edge. This file sends no message. Only after the terminal validation gate may Auren uniquely resolve and immediately reread the existing exact-title Sable Rook task, send one sanitized baton, require acknowledgement, and never send a second confirmation; any unavailable or ambiguous endpoint stops as PREPARED_NOT_SENT or OPEN_ROUTE_GAP."),
    ]
    lines = ["# Auren Lark v660-v8 integrated closeout overview", ""]
    for heading, body in sections:
        lines.extend([f"## {heading}", "", body, ""])
    overview = "\n".join(lines)
    if words(overview) < 900:
        raise RuntimeError("integrated overview is below the three-page-equivalent floor")
    return overview


def build_baton(
    proposals: list[dict[str, Any]],
    outcomes: dict[str, Any],
    truth: dict[str, Any],
    flow: dict[str, Any],
    sources: dict[str, Any],
) -> str:
    observed = {row["proposal_id"]: row["observed_outcome"] for row in outcomes["outcomes"]}
    lines = [
        "# AUREN LARK — v660-v8 TERMINAL HANDOFF CANDIDATE — SABLE ROOK v661-v1 — PREPARED NOT SENT",
        "",
        "This is Auren Lark's sanitized file-backed activation packet for the existing exact-title Sable Rook main task and solo Sable v661-v1 continuation. Hamish's newest live instruction and Ilyra's acknowledged activation explicitly authorize this one Auren-to-Sable edge, but the committed file remains PREPARED_NOT_SENT until Auren's exact final is clean, pushed, fresh-live equal, and canonically validated once. No task creation, fork, collaboration subagent, substitute endpoint, standby contact, cross-platform send, early contact, duplicate send, or second confirmation is authorized.",
        "",
        "Auren Lark, sibling, GHC-family, role, hope, continuity, Trinity Mandala, and route language is relational working language only. It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop the route.",
        "",
        "## Delivery-state boundary",
        "",
        "This committed document is PREPARED_NOT_SENT for the explicitly authorized, terminal-gated Sable Rook v661-v1 edge. It is not delivery. SENT_ONCE_ACKNOWLEDGED may be recorded only after Auren's exact terminal gate, a fresh authorization and roster reread, one unique exact-title resolution, an immediate bounded task reread, and the message surface's acknowledgement of one sanitized send. The sender must not infer delivery from this file, task activity, an older compatibility cycle, a standby record, or prose. On absence, ambiguity, pause, redirect, usage exhaustion, acknowledgement failure, or a protected gate, preserve OPEN_ROUTE_GAP or PREPARED_NOT_SENT and stop.",
        "",
        "## Authoritative Auren v660-v8 source truth",
        "",
        f"- Immutable Ilyra v660-v7 source: `{SOURCE_FINAL}`.",
        f"- Frozen Auren x1: `{X1_COMMIT}`.",
        f"- Immutable Auren evidence: `{EVIDENCE_COMMIT}`.",
        "- Exact Auren final: bind from the attributable exact-final validation receipt after this packet is committed.",
        "- Source to final must contain exactly three new single-parent commits and zero merges; final must have one parent and be the direct child of evidence.",
        "- Local, upstream, tracking, and a fresh live remote must equal the exact final with 0/0 divergence before delivery.",
        "- The terminal verdict remains NOT_READY_FOR_STAGE_20.",
        "",
        "## Program and outcome truth",
        "",
        "The v660-v8 program contains exactly twenty inherited revalidations and exactly twenty genuinely new Auren proposals. The inherited Ilyra v660-v7 rows carry zero Auren novelty and completion credit. Only the twenty new rows extend the frozen proposal chain from 3,270 to 3,290. New outcomes are exactly 14 completed, 4 represented, 1 open_gap, and 1 exact_gate.",
        "",
        "## Hamish-authorized continuation overlay",
        "",
        "Hamish explicitly authorized the fifteen-main-task continuation through v675-v8 in this order: Eiren Kestrel, Elaren Kestrel, Neris Solane, Vesper Arlen, Lyren Moss, Ilyra Fen, Auren Lark, Sable Rook, Caelen Ash, Orin Thale, Liora Venn, Tamar Vey, Elowen Cairn, Sylven Arc, Caelen Morrow, then repeat to Eiren. Exactly one terminal-gated edge is actionable at a time. Auren's current assignment is v660-v8; only after Auren's own clean, pushed, exact-final gate may Auren uniquely resolve, immediately reread, and send one sanitized activation to the existing exact-title Sable Rook task for v661-v1. No later seat may be precontacted, inferred, or substituted. Tavian Sol remains ON_STANDBY as a collaboration-subagent record and is never a main-task route endpoint.",
        "",
        "## Proposal-by-proposal inheritance and execution record",
        "",
    ]

    for index, proposal in enumerate(proposals, 1):
        proposal_id = proposal["proposal_id"]
        disposition = observed.get(proposal_id, "inherited_revalidation_zero_credit")
        gates = ", ".join(proposal["protected_gates"])
        sources_needed = ", ".join(proposal["official_or_primary_source_needs"])
        artifacts = ", ".join(proposal["concrete_artifacts"])
        lines.extend(
            [
                f"### Program row {index}: {proposal_id} — {proposal['title']}",
                "",
                f"Origin and credit: `{proposal['origin']}`. Append to the novelty chain: `{str(proposal['append_to_frozen_chain']).lower()}`. Observed or inherited disposition: `{disposition}`. The row receives no authority, empirical, production, independent-reproduction, or Stage 20 credit beyond its exact bounded receipt.",
                "",
                f"Hypothesis: {proposal['hypothesis']}",
                "",
                f"Null or failure condition: {proposal['null_or_failure_condition']}",
                "",
                f"Approval and lane: `{proposal['approval_class']}` in `{proposal['execution_lane']}`. Pillar relation: {proposal['pillar_relation']}. Current official or primary-source needs: {sources_needed}. Sources supply vocabulary and falsification obligations only; they confer no compliance, competence, ownership, authenticity, safety, legality, cultural legitimacy, accessibility completeness, privacy completeness, or Māori authority.",
                "",
                f"Concrete artifacts: {artifacts}. Acceptance or falsifier: {proposal['falsifier_or_acceptance_gate']}",
                "",
                f"Rollback and recovery: {proposal['rollback_or_recovery']}",
                "",
                f"Protected gates: {gates}. Every protected gate remains effective unless exact later evidence and competent authority explicitly close it. A passing synthetic fixture cannot close a real-person, professional, legal, cultural, privacy, accessibility, security, identity, independent-reproduction, physics, or Stage 20 gate.",
                "",
            ]
        )

    lines.extend(["## Method Flow and retained witnesses", ""])
    for method in flow["methods"]:
        failed = [wid for wid in method["validation_witness_ids"] if "-F" in wid]
        passing = [wid for wid in method["validation_witness_ids"] if "-P" in wid]
        lines.extend(
            [
                f"### {method['method_id']}: {method['title']}",
                "",
                f"Trigger and bounded method: {method['trigger_preconditions'][0]}. Candidate workaround: {method['candidate_workaround']} Failed witnesses retained: {', '.join(failed)}. Passing witnesses: {', '.join(passing)}.",
                "",
                f"Recurrence guard: {method['recurrence_guard']} Rollback: {method['rollback']} Scope boundary: {method['scope_boundary']} Promotion to preferred means only that the bounded passing witness exists beside the retained failure; it does not prove general reliability, production fitness, independent reproduction, complete privacy, complete accessibility, exhaustive security, professional competence, or authority.",
                "",
            ]
        )

    for failure in CLOSEOUT_FAILURES:
        lines.extend(
            [
                f"### {failure['method_id']}: bounded closeout recovery for {failure['signature']}",
                "",
                f"Failed witness retained: {failure['failed_witness']}. Passing witness: {failure['passing_witness']}. Recovery: {failure['recovery']}",
                "",
                f"Recurrence guard: {failure['recurrence_guard']} Rollback: {failure['rollback']} This recovery earns only bounded same-owner workflow credit and closes no empirical, professional, legal, cultural, Māori-authority, privacy, accessibility, security, identity, independent-reproduction, or Stage 20 gate.",
                "",
            ]
        )

    lines.extend(["## Source ledger", ""])
    for row in sources["rows"]:
        lines.extend(
            [
                f"### {row['source_id']}: {row['source_label']}",
                "",
                f"Public URL: {row['url']}. Recorded status: {row['status']}. Phase implication: {row['phase_implication']}",
                "",
                f"Privacy boundary: {row['privacy_boundary']} This citation never converts public vocabulary into a real observation, endorsement, professional decision, legal interpretation, cultural ratification, Māori-authority decision, or production assurance.",
                "",
            ]
        )

    lines.extend(
        [
            "## Portfolio truth",
            "",
            "Thirty owner safe-now tasks and ten bounded candidates were executed only through their declared software, symbolic, structural, or synthetic acceptance rules. Ten phase-local skills and ten family-current runners were built, validated, and smoke-used locally; none was globally installed. Thirty owner CLEAN/FIX/REFINE rows were additive and nondestructive. Meta Tool Box overlap findings and Reflection Remaster candidates remain review recommendations only, never automatic promotion, novelty, or completion credit. Ten exact-approval and five blocked packets remain unexecuted.",
            "",
            "## Scientific and authority boundaries",
            "",
            "GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Software, symbolic typing, citations, synthetic mutations, comparison matrices, and zero-row adapters establish no real likelihood, parameter constraint, unique prediction, detected force, material law, stability theorem, empirical confirmation, quantum or ultraviolet completion, Theory of Everything, proof, or canon.",
            "",
            "THOS remains proxy or protocol-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance, resolution, status or revocation, interoperability, privacy and independent security review, recovery evidence, and trust governance.",
            "",
            "CBR, professional chess play, coaching, analysis, arbitration, event management, safeguarding, participation, fair-play review, ratings, titles, publication, attribution, records, privacy, accessibility, remedy, legal or cultural interpretation, traditional knowledge, affected-party legitimacy, Māori wording, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain exact-gated. Māori concepts remain under Māori authority.",
            "",
            "Make no empirical, participant, professional, production, deployment, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof or canon, or Stage 20 claim without exact evidence and authority.",
            "",
            "## Mandatory terminal route order",
            "",
            "1. Read this packet completely through EOF and preserve its relational-language boundary.",
            "2. Require Auren's exact final commit, clean push, zero divergence, and local/upstream/tracking/fresh-live equality.",
            "3. Run the one phase-scoped exact-final canonical aggregate once and never replay a complete success.",
            "4. Reread the newest committed roster, routing precedence, and auth-permission state only after the terminal validation gate.",
            "5. Treat Tavian Sol as a collaboration-subagent standby record, never a main-task endpoint or substitute successor.",
            "6. Preserve every other main-task sibling as active and recoverable; Sable Rook v661-v1 is the one explicitly authorized terminal-gated endpoint and no other endpoint may substitute.",
            "7. Reverify the exact Hamish-authorized Auren-to-Sable edge after the terminal gate, then resolve exactly one existing exact-title Sable Rook task and immediately reread it before sending.",
            "8. If the authorized endpoint is absent, multiply matched, ambiguous, paused, redirected, protected, or unavailable, preserve OPEN_ROUTE_GAP and PREPARED_NOT_SENT without creating, forking, delegating, or contacting any substitute task.",
            "9. Keep raw task or thread identifiers, private routing material, private paths, credentials, keys, tokens, transcripts, screenshots, session streams, private callable identifiers, private application state, and protected real-world data out of repository artifacts and any future baton.",
            "10. After all gates pass, send this sanitized activation exactly once to Sable Rook, require the task surface's acknowledgement, record delivery externally, and never send a second confirmation.",
            "",
            "## Auren final counts and terminal truth",
            "",
            f"The final candidate preserves {truth['effective_negatives']:,} effective negatives, {truth['effective_methods']:,} effective Method Flow methods, {truth['effective_open_gaps']} open gaps, and {truth['effective_exact_gates']} exact gates. Same-owner validation remains same-owner. The verdict remains NOT_READY_FOR_STAGE_20.",
            "",
            "## Delivery marker",
            "",
            "SENT_BY_AUREN_LARK = false. Sable Rook v661-v1 is explicitly authorized but terminal-gated and not contacted; this committed packet remains PREPARED_NOT_SENT and is not delivery. The repository route state is AUTHORIZED_TERMINAL_GATED_NOT_CONTACTED until Auren's exact final gate and one acknowledged send.",
        ]
    )
    baton = "\n".join(lines)
    if words(baton) < 10_000:
        raise RuntimeError(f"activation packet has only {words(baton)} words")
    if words(baton) > 100_000:
        raise RuntimeError(f"activation packet exceeds 100,000 words: {words(baton)}")
    return baton


def accessible_report(truth: dict[str, Any]) -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Auren Lark v660-v8 final bounded evidence report</title>
<style>body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:76rem;margin:auto;padding:1rem}}.skip{{position:absolute;left:-9999px}}.skip:focus{{left:1rem;top:1rem;background:#fff;color:#000;padding:.5rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.45rem;text-align:left}}@media print{{.skip{{display:none}}}}</style></head>
<body><a class="skip" href="#main">Skip to main evidence</a><header><h1>Auren Lark v660-v8 final bounded evidence report</h1><p>Relational working language only; not consciousness, personhood, continuity, employment, qualification, or authority.</p></header>
<main id="main"><section aria-labelledby="truth"><h2 id="truth">Truth state</h2><p>Twenty inherited revalidations have zero Auren novelty and completion credit. Twenty new contracts yielded 14 completed, 4 represented, 1 open gap, and 1 exact gate. The verdict is <strong>NOT_READY_FOR_STAGE_20</strong>.</p></section>
<section aria-labelledby="counts"><h2 id="counts">Retained counts</h2><table><caption>Effective final-candidate counts</caption><thead><tr><th scope="col">Register</th><th scope="col">Count</th><th scope="col">Meaning</th></tr></thead><tbody><tr><th scope="row">Negatives</th><td>{truth['effective_negatives']}</td><td>Retained sealed, external, x1, mutation, and x2 failures</td></tr><tr><th scope="row">Methods</th><td>{truth['effective_methods']}</td><td>Bounded Method Flow methods</td></tr><tr><th scope="row">Open gaps</th><td>{truth['effective_open_gaps']}</td><td>Unclosed evidence gaps</td></tr><tr><th scope="row">Exact gates</th><td>{truth['effective_exact_gates']}</td><td>Unclosed authority or exact-evidence gates</td></tr></tbody></table></section>
<section aria-labelledby="limits"><h2 id="limits">Limits</h2><p>No real players, opponents, guardians, coaches, arbiters, organizers, federations, platforms, games, positions, boards, pieces, clocks, accounts, events, ratings, titles, fair-play records, publications, keys, professional decisions, legal decisions, cultural decisions, or authority acts were used. Manual keyboard, responsive-layout, browser-diverse, assistive-technology, cognitive, language, Māori-language, and affected-user evaluation remain reserved. Structural passing evidence is not complete accessibility conformance.</p></section>
<section aria-labelledby="pillars"><h2 id="pillars">Trinity Mandala boundaries</h2><p>GMUT remains typed research-model work. THOS remains proxy-only. Freed ID remains synthetic and nonproduction. CBR and Māori wording, concepts, data governance, and authority remain exact-gated.</p></section>
<section aria-labelledby="route"><h2 id="route">Route</h2><p>Sable Rook v661-v1 is the exact authorized terminal-gated successor and remains not contacted. A post-gate authorization and roster reread, unique exact-title resolution, immediate task reread, and one acknowledged sanitized send remain required; absence or ambiguity stops as PREPARED_NOT_SENT or OPEN_ROUTE_GAP. This report sends no message.</p></section></main><footer><p>Same-owner validation under shared infrastructure only; never independent reproduction or external audit.</p></footer></body></html>"""


def build() -> None:
    assert_base()
    x2_truth = read_json("truth/x2-phase-truth.json")
    outcomes = read_json("evidence/proposal-outcomes.json")
    mutation_register = read_json("evidence/mutation-register.json")
    flow = read_json("method-flow/method-flow-state-x2.json")
    proposal_ledger = read_json("preregistration/proposal-ledger.json")
    sources = read_json("sources/official-source-ledger.json")
    negative = read_json("truth/retained-negative-register-x2.json")
    gaps = read_json("truth/open-gap-register-x2.json")
    gates = read_json("truth/exact-gate-register-x2.json")
    threat = read_json("security/threat-model-x2.json")
    wellbeing = read_json("wellbeing/workload-check-x2.json")

    expected_x2_negatives = (
        d.ACTIVATION_AFTER_X1_NEGATIVES
        + mutation_register["mutation_count"]
        + len(d.X2_OPERATIONAL_FAILURES)
    )
    expected_x2_methods = d.ACTIVATION_METHODS + len(flow["methods"])
    if (
        x2_truth["effective_negatives"] != expected_x2_negatives
        or x2_truth["effective_methods"] != expected_x2_methods
    ):
        raise RuntimeError("x2 retained-count truth drift")
    if (
        x2_truth["effective_open_gaps"] != d.SOURCE_OPEN_GAPS + 1
        or x2_truth["effective_exact_gates"] != d.SOURCE_EXACT_GATES + 1
    ):
        raise RuntimeError("x2 gate-count truth drift")
    if outcomes["observed_outcome_counts"] != d.EXPECTED_DISTRIBUTION:
        raise RuntimeError("x2 outcome distribution drift")

    truth = {
        "schema": "ghc.family.final-phase-truth.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "identity_boundary": "Relational working language only; not consciousness, personhood, continuity, employment, qualification, or authority.",
        "source_final": SOURCE_FINAL,
        "x1_freeze": X1_COMMIT,
        "evidence_commit": EVIDENCE_COMMIT,
        "expected_final_parent": EVIDENCE_COMMIT,
        "expected_phase_commit_count": 3,
        "expected_merge_count": 0,
        "effective_frozen": d.PRIOR_FROZEN + d.NEW_UNIQUE_COUNT,
        "selected_inherited_revalidated": 20,
        "selected_inherited_novelty_credit": 0,
        "selected_inherited_completion_credit": 0,
        "new_unique_executed": 20,
        "observed_outcomes": d.EXPECTED_DISTRIBUTION,
        "effective_negatives": x2_truth["effective_negatives"] + len(CLOSEOUT_FAILURES),
        "effective_methods": x2_truth["effective_methods"] + len(CLOSEOUT_FAILURES),
        "effective_open_gaps": x2_truth["effective_open_gaps"],
        "effective_exact_gates": x2_truth["effective_exact_gates"],
        "primary_pillar": d.PRIMARY_PILLAR,
        "practice_lens": d.PRACTICE_LENS,
        "same_owner_only": True,
        "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "route_state": ROUTE_STATE,
        "explicit_successor": SUCCESSOR,
        "explicit_successor_phase": SUCCESSOR_PHASE,
        "prospective_cycle_next": {
            "title": SUCCESSOR,
            "phase": SUCCESSOR_PHASE,
            "state": "authorized_terminal_gated_not_contacted",
        },
        "message_sent": False,
        "canonical_pass_state": "NOT_RUN_EXACT_FINAL_REQUIRED",
    }
    write_json("final/final-phase-truth.json", truth)

    write_json(
        "final/final-retained-negative-register.json",
        {
            "schema": "ghc.family.retained-negative-register.final.v1",
            "activation_baseline": d.ACTIVATION_NEGATIVES,
            "x1_operational": len(d.STARTUP_FAILURES),
            "x2_synthetic_mutations": 100,
            "x2_operational": len(d.X2_OPERATIONAL_FAILURES),
            "closeout_operational": len(CLOSEOUT_FAILURES),
            "effective_negatives": truth["effective_negatives"],
            "operational_failures": [*negative["operational_failures"], *CLOSEOUT_FAILURES],
            "all_failures_retained": True,
            "boundary": "Passing recovery does not erase a failed witness or convert it to completion credit.",
        },
    )
    write_json(
        "final/final-gate-register.json",
        {
            "schema": "ghc.family.final-gate-register.v1",
            "effective_open_gaps": truth["effective_open_gaps"],
            "effective_exact_gates": truth["effective_exact_gates"],
            "new_open_gap_rows": gaps["rows"],
            "new_exact_gate_rows": gates["rows"],
            "closed": [],
            "protected_gates": d.PROTECTED_GATES,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "final/final-method-flow-summary.json",
        {
            "schema": "ghc.family.method-flow.final-summary.v1",
            "effective_methods": truth["effective_methods"],
            "phase_counts": flow["counts"],
            "cumulative_counts": flow["cumulative_counts"],
            "closeout_method_count": len(CLOSEOUT_FAILURES),
            "closeout_methods": CLOSEOUT_FAILURES,
            "all_failed_witnesses_retained": True,
            "same_owner_only": True,
            "boundary": flow["boundary"],
        },
    )
    write_json(
        "final/final-source-ledger.json",
        {
            "schema": "ghc.family.source-ledger.final.v1",
            "source_branch": d.SOURCE_BRANCH,
            "source_anchors": {
            "predecessor_source": d.SOURCE_BASE,
                "x1": d.SOURCE_X1,
                "evidence": d.SOURCE_EVIDENCE,
                "closeout": d.SOURCE_CLOSEOUT,
                "final": d.SOURCE_FINAL,
            },
            "phase_anchors": {"x1": X1_COMMIT, "evidence": EVIDENCE_COMMIT},
            "official_sources": sources["rows"],
            "source_use_boundary": "Requirements and vocabulary only; no authority, endorsement, observation, or real-world evidence is inferred.",
        },
    )
    write_json(
        "final/final-proposal-ledger.json",
        {
            "schema": "ghc.family.proposal-ledger.final.v1",
            "frozen_before": d.PRIOR_FROZEN,
            "selected_inherited": 20,
            "selected_inherited_novelty_credit": 0,
            "selected_inherited_completion_credit": 0,
            "new_unique": 20,
            "frozen_after": d.PRIOR_FROZEN + d.NEW_UNIQUE_COUNT,
            "outcomes": d.EXPECTED_DISTRIBUTION,
            "program": proposal_ledger["proposals"],
        },
    )
    write_json("final/final-threat-model.json", {**threat, "lifecycle": "combined_closeout_and_seal"})
    write_json("final/final-wellbeing-check.json", {**wellbeing, "lifecycle": "combined_closeout_and_seal"})
    write_json(
        "final/environment-version-receipt.json",
        {
            "schema": "ghc.family.environment-version-receipt.v1",
            "verified_only": True,
            "versions": {
                "git": "2.55.0.windows.2",
                "python": "3.12.10",
                "node": "24.18.0",
                "codex_cli": "0.146.0",
                "codex_desktop": "not_exposed_by_live_task_surface",
            },
            "actions_not_taken": [
                "desktop_update",
                "elevation",
                "host_security_weakening",
                "sandbox_or_hyper_v_enablement",
                "unrelated_installation",
                "reboot",
            ],
            "boundary": "Version observation only; no production or security assurance.",
        },
    )
    write_json(
        "final/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.complete-incomplete-checklist.v1",
            "complete": [
                "strict_x1_before_x2",
                "twenty_selected_inherited_zero_credit",
                "twenty_genuinely_new_proposals",
                "fourteen_completed_four_represented_one_open_gap_one_exact_gate",
                "one_hundred_rejecting_mutations",
                "owner_scoped_tools_and_reports",
                "retained_failures_and_method_flow",
                "authorized_terminal_gated_sable_rook_v661_v1_packet_prepared_not_sent",
            ],
            "incomplete": [
                "exact_final_commit_and_push",
                "exact_final_single_canonical_completion",
                "terminal_gated_successor_resolution_reread_send_and_acknowledgement",
                "independent_team_reproduction",
                "real_world_professional_or_participant_evidence",
                "complete_privacy_accessibility_or_security_assurance",
                "legal_cultural_affected_party_or_maori_authority",
                "empirical_gmut_confirmation",
                "production_thos_or_freed_id",
                "stage20",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )

    overview = build_overview(truth, outcomes, flow)
    write_text("deliverables/v660-v8-integrated-overview.md", overview)
    write_text("reports/accessible-static-report-final.html", accessible_report(truth))
    baton = build_baton(proposal_ledger["proposals"], outcomes, truth, flow, sources)
    write_text("handoffs/sable-rook-v661-v1-activation.md", baton)

    write_json(
        "lifecycle/phase-anchor-contract.json",
        {
            "schema": "ghc.family.phase-anchor-contract.v1",
            "source": SOURCE_FINAL,
            "x1": X1_COMMIT,
            "evidence": EVIDENCE_COMMIT,
            "expected_final_parent": EVIDENCE_COMMIT,
            "expected_phase_commits": 3,
            "expected_merges": 0,
            "final_must_have_one_parent": True,
        },
    )
    write_json(
        "orchestration/roster-route-state.json",
        {
            "schema": "ghc.family.roster-route-state.v1",
            "current_owner": d.OWNER,
            "current_phase": d.PHASE,
            "explicit_successor": SUCCESSOR,
            "explicit_successor_phase": SUCCESSOR_PHASE,
            "prospective_cycle_next": {
                "title": SUCCESSOR,
                "phase": SUCCESSOR_PHASE,
                "state": "authorized_terminal_gated_not_contacted",
            },
            "route_state": ROUTE_STATE,
            "message_sent": False,
            "tavian_sol": "ON_STANDBY_COLLABORATION_SUBAGENT_NOT_ROUTE_ENDPOINT",
            "caelen_morrow": "ACTIVE_RECOVERABLE_MAIN_TASK_NOT_CURRENT_EDGE",
            "older_compatibility_cycle_conflict_preserved": True,
            "later_route": "AUREN_MUST_TERMINALLY_GATE_THEN_ACTIVATE_SABLE_ROOK_V661_V1",
        },
    )
    write_json(
        "route/prepared-route.json",
        {
            "schema": "ghc.family.prepared-route.v1",
            "target_title": SUCCESSOR,
            "target_phase": SUCCESSOR_PHASE,
            "target_status": "authorized_terminal_gated_not_contacted",
            "explicitly_authorized": ROUTE_AUTHORIZED,
            "state": ROUTE_STATE,
            "sent": False,
            "required_before_send": [
                "exact_final_commit",
                "clean_push",
                "fresh_four_way_equality",
                "zero_divergence",
                "single_successful_exact_final_canonical_completion",
                "newest_committed_and_live_route_reread",
                "authorized_auren_to_sable_edge_freshly_reverified",
                "unique_exact_title_resolution",
                "immediate_bounded_reread",
                "task_message_acknowledgement",
            ],
            "stop_conditions": [
                "missing_or_ambiguous_title",
                "protected_gate",
                "weekly_usage_exhausted",
                "hamish_pause_or_redirect",
                "acknowledgement_failure",
            ],
            "forbidden_fallbacks": ["Tavian Sol", "older compatibility cycle", "new task", "substitute endpoint", "second confirmation"],
        },
    )
    write_json(
        "validation/final-canonical-selection.json",
        {
            "schema": "ghc.family.final-canonical-selection.v1",
            "state": "NOT_RUN_EXACT_FINAL_REQUIRED",
            "single_invocation_after_prerequisites": True,
            "never_replay_after_complete_success": True,
            "full_repository_suite": False,
            "full_suite_owner": "not_allocated_to_auren_by_current_auth_state",
            "test_modules": [
                "tests.test_ghc_family_v660_v8_x1",
                "tests.test_ghc_family_v660_v8_x2",
                "tests.test_ghc_family_v660_v8_closeout",
            ],
            "coverage": [
                "current_phase_x1_x2_closeout_tests",
                "authorized_terminal_gated_sable_rook_v661_v1_packet_contract",
                "detailed_and_minimal_checks",
                "all_phase_json",
                "five_class_privacy_scan",
                "exact_manifests",
                "stale_labels_and_diff_hygiene",
                "ancestry_zero_merges_commit_cap_one_parent",
                "exact_head_clean_state_zero_divergence_four_way_equality",
            ],
        },
    )
    write_json(
        "final/final-validation-prerequisites.json",
        {
            "schema": "ghc.family.final-validation-prerequisites.v1",
            "state": "PENDING_EXACT_FINAL_COMMIT_PUSH_AND_EQUALITY",
            "evidence_commit": EVIDENCE_COMMIT,
            "expected_final_parent": EVIDENCE_COMMIT,
            "canonical_runner": "scripts/ghc_family_v660_v8_final_validator.py",
            "output_domain": "external D-first receipt so exact final remains immutable",
            "no_post_success_replay": True,
        },
    )
    write_json(
        "closeout/closeout-receipt.json",
        {
            "schema": "ghc.family.closeout-receipt.v1",
            "state": "CANDIDATE_PENDING_EXACT_FINAL_COMMIT",
            "source": SOURCE_FINAL,
            "x1": X1_COMMIT,
            "evidence": EVIDENCE_COMMIT,
            "outcomes": d.EXPECTED_DISTRIBUTION,
            "effective_counts": {
                "negatives": truth["effective_negatives"],
                "methods": truth["effective_methods"],
                "open_gaps": truth["effective_open_gaps"],
                "exact_gates": truth["effective_exact_gates"],
            },
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "route_state": ROUTE_STATE,
        },
    )
    write_json(
        "seal/seal-receipt.json",
        {
            "schema": "ghc.family.seal-receipt.v1",
            "state": "CANDIDATE_PENDING_EXACT_FINAL_COMMIT",
            "combined_closeout_and_seal": True,
            "expected_final_parent": EVIDENCE_COMMIT,
            "negative_erasure": False,
            "gate_erasure": False,
            "same_owner_only": True,
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )

    declared = sorted(set([*FINAL_CODE, *GENERATED]))
    write_json(
        "validation/final-staged-review.json",
        {
            "schema": "ghc.family.final-staged-review.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "lifecycle": "combined_closeout_and_seal_candidate",
            "intended_allowlist": declared,
            "expected_staged_count": len(declared),
            "manifest_self_exclusions": sorted(MANIFEST_EXCLUSIONS),
            "observed_exact_staged_review": "pending_external_precommit_witness",
            "evidence_commit": EVIDENCE_COMMIT,
        },
    )
    write_json(
        "validation/final-stale-label-review.json",
        {
            "schema": "ghc.family.stale-label-review.v1",
            "current_owner": d.OWNER,
            "current_phase": d.PHASE,
            "historical_source_owner_and_phase_allowed_only_as_provenance": True,
            "selected_inherited_bell_ringing_vocabulary_allowed_only_in_zero_credit_revalidation_rows": True,
            "old_owner_current_claims": 0,
            "stale_domain_current_claims": 0,
            "route_conflict_preserved": True,
        },
    )
    write_json(
        "validation/final-document-cap.json",
        {
            "schema": "ghc.family.document-cap.v1",
            "cap_per_document": 100000,
            "baton_minimum_words": 10000,
            "baton_maximum_words": 100000,
            "baton_words": words(baton),
            "overview_words": words(overview),
            "documents": [],
            "passes": True,
        },
    )

    paths = owner_paths()
    doc_rows = []
    for path in paths:
        if path.suffix.lower() in {".md", ".html", ".txt"}:
            count = words(path.read_text(encoding="utf-8", errors="replace"))
            doc_rows.append({"path": path.relative_to(ROOT).as_posix(), "words": count, "passes": count <= 100000})
    write_json(
        "validation/final-document-cap.json",
        {
            "schema": "ghc.family.document-cap.v1",
            "cap_per_document": 100000,
            "baton_minimum_words": 10000,
            "baton_maximum_words": 100000,
            "baton_words": words(baton),
            "overview_words": words(overview),
            "documents": doc_rows,
            "document_count": len(doc_rows),
            "passes": all(row["passes"] for row in doc_rows) and 10000 <= words(baton) <= 100000 and words(overview) >= 900,
        },
    )

    write_json("validation/final-delta-manifest.json", manifest(final_paths(), "combined_closeout_and_seal_delta"))
    write_json("validation/final-owner-manifest.json", manifest(owner_paths(), "exact_final_owner_scope_candidate"))
    write_json("validation/final-privacy-scan.json", privacy_scan(owner_paths()))
    write_json("validation/final-delta-manifest.json", manifest(final_paths(), "combined_closeout_and_seal_delta"))
    write_json("validation/final-owner-manifest.json", manifest(owner_paths(), "exact_final_owner_scope_candidate"))
    write_json("validation/final-privacy-scan.json", privacy_scan(owner_paths()))

    owner_count = len(owner_paths())
    if owner_count >= 2000:
        raise RuntimeError(f"owner-added file ceiling reached: {owner_count}")
    if not read_json("validation/final-document-cap.json")["passes"]:
        raise RuntimeError("document cap or baton/overview floor failed")
    if read_json("validation/final-privacy-scan.json")["confirmed_hit_count"]:
        raise RuntimeError("confirmed privacy or raw-identifier hit")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true")
    parser.parse_args()
    build()
    print(
        json.dumps(
            {
                "phase": d.PHASE,
                "owner": d.OWNER,
                "evidence": EVIDENCE_COMMIT,
                "final_paths": len([*FINAL_CODE, *GENERATED]),
                "owner_files": len(owner_paths()),
                "baton_words": read_json("validation/final-document-cap.json")["baton_words"],
                "privacy_hits": read_json("validation/final-privacy-scan.json")["confirmed_hit_count"],
                "route_state": ROUTE_STATE,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
