#!/usr/bin/env python3
"""Build the Sylven Arc v661-v7 combined closeout and seal candidate.

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

import ghc_family_v661_v7_x2_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
SOURCE_FINAL = d.SOURCE_FINAL
X1_COMMIT = d.X1_FREEZE
EVIDENCE_COMMIT = "7a81185d14d4255329824cbf9bbf67520039d630"
SUCCESSOR = "Caelen Morrow"
SUCCESSOR_PHASE = "v661-v8"
ROUTE_STATE = "EXPLICIT_SUCCESSOR_TERMINAL_GATE_UNMET_PREPARED_NOT_SENT"
ROUTE_AUTHORIZED = True

# Append only failures actually observed after the immutable evidence commit.
# No closeout failure is predeclared before that lifecycle begins.
CLOSEOUT_FAILURES: list[dict[str, Any]] = [
    {
        "method_id": "V6617-CLOSEOUT-METHOD-001",
        "negative_id": "V6617-CLOSEOUT-N001",
        "signature": "broad-closeout-stale-route-and-domain-search-exceeded-the-output-budget",
        "failed_witness": "V6617-CLOSEOUT-W001-F01",
        "passing_witness": "V6617-CLOSEOUT-W001-P01",
        "recovery": "Split the stale-route and domain review into bounded exact-pattern groups and explicit line windows; the narrower review returned complete evidence.",
        "recurrence_guard": "Estimate match volume first and use separate exact pattern groups for route, domain, and lifecycle vocabulary.",
        "rollback": "Discard the truncated presentation and preserve the unchanged repository state.",
        "recovery_passed": True,
    },
    {
        "method_id": "V6617-CLOSEOUT-METHOD-002",
        "negative_id": "V6617-CLOSEOUT-N002",
        "signature": "parallel-closeout-inspection-exceeded-the-orchestrator-yield-window-before-evidence-returned",
        "failed_witness": "V6617-CLOSEOUT-W002-F01",
        "passing_witness": "V6617-CLOSEOUT-W002-P01",
        "recovery": "Reissued bounded inspections with an explicit longer orchestration yield window and smaller sequential evidence surfaces.",
        "recurrence_guard": "Set the outer orchestration yield budget whenever multiple PowerShell probes can exceed the default window.",
        "rollback": "Treat the timed-out presentation as zero credit; it made no repository mutation.",
        "recovery_passed": True,
    },
    {
        "method_id": "V6617-CLOSEOUT-METHOD-003",
        "negative_id": "V6617-CLOSEOUT-N003",
        "signature": "bounded-line-window-inspection-omitted-the-outer-yield-budget-and-timed-out",
        "failed_witness": "V6617-CLOSEOUT-W003-F01",
        "passing_witness": "V6617-CLOSEOUT-W003-P01",
        "recovery": "Repeated only the intended 31-line window with an explicit longer outer yield and obtained complete evidence.",
        "recurrence_guard": "Apply the outer yield directive even to small PowerShell reads while process startup latency is elevated.",
        "rollback": "Retain the first timeout at zero credit and keep the working tree unchanged.",
        "recovery_passed": True,
    },
    {
        "method_id": "V6617-CLOSEOUT-METHOD-004",
        "negative_id": "V6617-CLOSEOUT-N004",
        "signature": "first-closeout-build-projected-a-nonexistent-separate-source-closeout-anchor",
        "failed_witness": "V6617-CLOSEOUT-W004-F01",
        "passing_witness": "V6617-CLOSEOUT-W004-P01",
        "recovery": "Inspected the immutable source contract, preserved its exact base, x1, evidence, and final anchors, and represented the deliberately absent separate closeout anchor as null with an explanatory boundary.",
        "recurrence_guard": "Inspect source anchor keys before projecting a predecessor lifecycle shape into a successor ledger.",
        "rollback": "Overwrite only the uncommitted owner-local generated candidate files from the failed build; do not alter any immutable anchor or evidence commit.",
        "recovery_passed": True,
    },
    {
        "method_id": "V6617-CLOSEOUT-METHOD-005",
        "negative_id": "V6617-CLOSEOUT-N005",
        "signature": "first-literal-final-allowlist-stage-was-partially-rejected-by-the-owner-worktrees-sparse-checkout-boundary",
        "failed_witness": "V6617-CLOSEOUT-W005-F01",
        "passing_witness": "V6617-CLOSEOUT-W005-P01",
        "recovery": "Retained the partial staging attempt at zero credit, reused the identical declared allowlist with Git's explicit sparse-aware add mode, and required exact missing and unexpected path checks before commit.",
        "recurrence_guard": "Inspect sparse-checkout state before owner-path staging and use --sparse only with a reviewed literal allowlist.",
        "rollback": "If exact parity fails, unstage only the owner-local final allowlist and leave immutable x1 and evidence commits untouched.",
        "recovery_passed": True,
    },
    {
        "method_id": "V6617-CLOSEOUT-METHOD-006",
        "negative_id": "V6617-CLOSEOUT-N006",
        "signature": "first-combined-retention-and-test-patch-used-a-mistyped-validator-path-in-its-context-and-was-rejected",
        "failed_witness": "V6617-CLOSEOUT-W006-F01",
        "passing_witness": "V6617-CLOSEOUT-W006-P01",
        "recovery": "Retained the rejected patch at zero credit, reread the exact test context, corrected the path token, and applied only the intended additive retention and expectation changes.",
        "recurrence_guard": "Copy exact context from the current file before composing multi-file patches and split patches when one context is uncertain.",
        "rollback": "The rejected patch changed no file; preserve that no-mutation state as the rollback boundary.",
        "recovery_passed": True,
    },
    {
        "method_id": "V6617-CLOSEOUT-METHOD-007",
        "negative_id": "V6617-CLOSEOUT-N007",
        "signature": "first-closeout-prerequisite-suite-compared-the-phase-source-anchor-to-elowens-predecessor-base-instead-of-elowens-exact-final",
        "failed_witness": "V6617-CLOSEOUT-W007-F01",
        "passing_witness": "V6617-CLOSEOUT-W007-P01",
        "recovery": "Retained the 16-pass and one-fail aggregate at zero aggregate credit, corrected the Sylven source constant to Elowen's immutable exact final, and reran only the closeout prerequisite module because its anchor contract was the affected dependency.",
        "recurrence_guard": "Distinguish predecessor-base provenance from the immediate phase-source final in both tests and the exact-final validator.",
        "rollback": "Keep Elowen's full anchor chain unchanged and revert only the incorrect Sylven source projection if the corrected dependency does not pass.",
        "recovery_passed": True,
    },
    {
        "method_id": "V6617-CLOSEOUT-METHOD-008",
        "negative_id": "V6617-CLOSEOUT-N008",
        "signature": "first-staged-json-preflight-used-a-convertfrom-json-depth-parameter-unavailable-in-the-active-powershell-runtime",
        "failed_witness": "V6617-CLOSEOUT-W008-F01",
        "passing_witness": "V6617-CLOSEOUT-W008-P01",
        "recovery": "Retained the compatibility fault at zero credit and reran only staged JSON parsing without the unsupported Depth parameter, preserving the same literal path set.",
        "recurrence_guard": "Probe the active PowerShell command surface or use the lowest common parameter set for staged JSON parsing.",
        "rollback": "The failed preflight was read-only; preserve the staged allowlist and make no repository rollback mutation.",
        "recovery_passed": True,
    },
    {
        "method_id": "V6617-CLOSEOUT-METHOD-009",
        "negative_id": "V6617-CLOSEOUT-N009",
        "signature": "second-staged-json-preflight-placed-the-revision-separator-before-the-index-object-and-read-commit-presentation-instead-of-the-json-blob",
        "failed_witness": "V6617-CLOSEOUT-W009-F01",
        "passing_witness": "V6617-CLOSEOUT-W009-P01",
        "recovery": "Retained the read-only projection failure at zero credit, used the exact index object expression as a single git-show argument, and confirmed a bounded staged JSON blob parsed before replaying the remaining staged JSON set.",
        "recurrence_guard": "Pass colon-prefixed index object names directly to git show; do not place the path separator before an index-object revision.",
        "rollback": "The failed read changed no staged or working-tree byte, so the exact allowlist remained the rollback boundary.",
        "recovery_passed": True,
    },
    {
        "method_id": "V6617-CLOSEOUT-METHOD-010",
        "negative_id": "V6617-CLOSEOUT-N010",
        "signature": "combined-precommit-truth-and-ancestry-projection-used-command-separators-inside-a-powershell-hash-value-and-was-rejected-before-git-ran",
        "failed_witness": "V6617-CLOSEOUT-W010-F01",
        "passing_witness": "V6617-CLOSEOUT-W010-P01",
        "recovery": "Retained the parser rejection at zero credit and decomposed truth, staged-stat, and ancestry evidence into bounded scalar commands before projection.",
        "recurrence_guard": "Assign command results to scalar variables before constructing PowerShell ordered hashes; do not embed semicolon-separated commands in hash values.",
        "rollback": "The parser rejected the wrapper before any child command or mutation ran, so no repository rollback was required.",
        "recovery_passed": True,
    },
]

FINAL_CODE = [
    "scripts/build_ghc_family_v661_v7_closeout.py",
    "scripts/ghc_family_v661_v7_final_validator.py",
    "tests/test_ghc_family_v661_v7_closeout.py",
]

GENERATED = [
    f"{d.PHASE_ROOT}/closeout/closeout-receipt.json",
    f"{d.PHASE_ROOT}/deliverables/v661-v7-integrated-overview.md",
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
    f"{d.PHASE_ROOT}/handoffs/post-gate-successor-activation-candidate.md",
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
    for pattern in ("*v661_v7*.py",):
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
                "scripts/build_ghc_family_v661_v7_x1.py",
                "scripts/build_ghc_family_v661_v7_x2.py",
                "scripts/build_ghc_family_v661_v7_closeout.py",
                "scripts/ghc_family_v661_v7_final_validator.py",
            }:
                candidates.append({"path": relative, "class": label, "adjudication": "scanner_definition"})
            elif label == "transcript_or_session" and (
                relative.endswith("post-gate-successor-activation-candidate.md")
                or "exact-and-blocked-register" in relative
                or relative.endswith("preregistration/task-portfolios.json")
                or relative == "scripts/ghc_family_v661_v7_data.py"
            ):
                candidates.append({"path": relative, "class": label, "adjudication": "prohibition_boundary_vocabulary"})
            else:
                hits.append({"path": relative, "class": label})
    return {
        "schema": "ghc.family.privacy-scan.v1",
        "scope": "all Sylven Arc v661-v7 owner files at the final candidate",
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
        ("Relational identity and phase", f"Sylven Arc ({d.PRONOUNS}) is relational working language for a {d.ROLE}, with the hope to {d.HOPE}. This language is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or scientific, operational, legal, cultural, or Māori authority. Hamish may rename, pause, redirect, or stop the route. The phase is solo v661-v7, and every repository result remains bounded by the exact evidence recorded here."),
        ("Source and lifecycle", f"The immutable Elowen Cairn v661-v6 source is `{SOURCE_FINAL}`. Sylven froze x1 at `{X1_COMMIT}` and committed x2 evidence at `{EVIDENCE_COMMIT}`. The intended final is one combined closeout and seal commit directly after evidence, making three Sylven single-parent commits and zero merges from source. X1 was pushed, clean, and four-way equal before x2. Evidence was separately pushed, clean, and four-way equal before closeout. The final canonical phase-scoped aggregate remains unrun until the exact final is pushed and remote-equal."),
        ("Forty-row program truth", "The forty-row program is not forty new proposals. Twenty selected inherited Elowen v661-v6 rows were revalidated with zero Sylven novelty and zero Sylven completion credit. Twenty genuinely new Sylven proposals extend the frozen chain from 3,410 to 3,430. Their outcomes are exactly 14 completed, 4 represented, 1 open gap, and 1 exact gate. Only the permitted outcome vocabulary is used."),
        ("Primary practice and pillar protection", f"The primary pillar was {d.PRIMARY_PILLAR}. The bounded learning and synthetic-design lens was {d.PRACTICE_LENS}. Synthetic contracts covered map-accession identity, MARC scale and projection transcription, coordinate-domain refusal, record and correction lineage, OGC zero-row adapters, privacy-minimized access holds, place-name stewardship, accessibility reservations, workload control, handover, evidence admission, and rights and authority reservations. They involved zero real maps, charts, atlases, sheets, catalogues, coordinates, locations, land records, collections, reading rooms, images, owners, donors, cataloguers, librarians, archivists, conservators, researchers, workers, participants, inspections, measurements, operations, professional decisions, legal decisions, cultural decisions, or external actions. THOS remains proxy-only without blind matched-budget real arms, governed participants or operators, safety monitoring, statistics, and independent review."),
        ("GMUT Mind", "GMUT surfaces were typed symbolic and mutation contracts for synthetic atlas-transition cocycles, differential-form pullbacks, orientation, chart-domain covers, Stokes-consistency obligations, units, covariance, regularity, uncertainty, boundary conditions, and observation firewalls. They establish no detected force, physical object, likelihood, parameter constraint, unique prediction, universal conservation or physical law, stability theorem, empirical confirmation, quantum or ultraviolet completion, Theory of Everything, proof, or canon. Represented GMUT rows remain represented because no real map, coordinate, calibrated observation, likelihood evidence, uncertainty propagation, independent review, or physical observation exists."),
        ("Freed ID and CBR Heart", "Freed ID and CBR surfaces used fabricated map, catalogue-record, coordinate-extent, source, notice, correction, provenance, custody, rights, disclosure-hold, and deterministic-digest aliases. There were no real keys, signatures, proofs, credentials, issuance, resolution, status, revocation, interoperability, recovery, privacy review, independent security review, or trust-governance decisions. CBR, identification, attribution, authenticity, ownership, custody, location, land or boundary meaning, access, publication, disposal, records, traditional knowledge, place-name stewardship, remedy, affected-party legitimacy, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain exact-gated."),
        ("Falsification and negative retention", f"All 100 preregistered synthetic mutations were executed and rejected or quarantined. {len(d.X2_OPERATIONAL_FAILURES)} x2 operational failures, {len(d.STARTUP_FAILURES)} x1 startup or lifecycle failures, and {len(CLOSEOUT_FAILURES)} closeout failures remain retained at zero credit. The effective negative count is {truth['effective_negatives']:,}; the Method Flow count is {truth['effective_methods']:,}. The x1/x2 Method Flow has {flow['counts']['methods']} preferred bounded methods, {flow['counts']['witness_results']['fail']} failed witnesses, and {flow['counts']['witness_results']['pass']} passing witnesses; {len(CLOSEOUT_FAILURES)} additional closeout methods each retain one failed and one passing witness. Recovery never erases a failure or creates independent reproduction credit."),
        ("Gates and truth", f"The final candidate preserves {truth['effective_open_gaps']} open gaps and {truth['effective_exact_gates']} exact gates. Real evidence remains an open gap. The empty-chair authority matrix remains an exact gate. Empirical, participant, professional, production, deployment, identity, legal, cultural, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, and Stage 20 boundaries remain open or exact-gated. The terminal verdict remains `NOT_READY_FOR_STAGE_20`."),
        ("Portfolios and tools", "Thirty owner safe-now tasks, ten owner candidates, ten phase-local skills, ten family-current runners, and thirty additive CLEAN/FIX/REFINE tasks were bounded and executed only where evidence permitted. The Meta Tool Box validates phase-local skill and runner cards while retaining any lexical overlap findings for explicit review without selecting a silent winner. Reflection Remaster produces a current structural inventory and no automatic promotion. Ten exact-approval and five blocked packets remain visible and unexecuted. Phase-local skills were not globally installed."),
        ("Accessibility, privacy, and security", "The static report uses semantic landmarks, headings, a skip link, text alternatives for status, table captions, and a print-safe structure. Manual keyboard, browser-diverse, assistive-technology, cognitive, language, Māori-language, and affected-user evaluation remain reserved. Five-class scanning and a synthetic threat model are bounded checks only. They establish neither complete privacy nor exhaustive security."),
        ("Evidence semantics", "A completed label means only that the declared synthetic or structural acceptance rule passed for the exact owner-local fixture and that all five declared mutations were rejected. A represented label means an interface or protocol shape exists while the evidence needed for effectiveness, interoperability, safety, accessibility, privacy, professional fitness, or real-world use does not. An open gap means evidence could in principle be supplied later but is absent now. An exact gate means repository work cannot substitute for competent or affected-party authority. None of these labels is a moral rank, a scientific discovery, an entitlement to action, or permission to treat silence as consent."),
        ("Recovery doctrine", "Every failed wrapper, parser assumption, count assumption, manifest assumption, and document-floor miss remains a separate negative witness. A passing narrow recovery is stored beside the failure and never overwrites it. Recovery is limited to the failed dependency unless broader impact is demonstrated. The branch history is additive and single-parent; no failure is removed with reset, rewrite, force push, amend, destructive cleanup, or sibling mutation. Rollback means stopping at the last immutable anchor, preserving evidence, and leaving people, property, external services, rights, and authority unchanged."),
        ("Wellbeing and workload", "The workload check records a bounded solo software phase rather than a claim about inner experience or human health. Work was divided at immutable x1 and x2 anchors, long-running builders were polled rather than duplicated, failed aggregates earned zero credit, and exact approval packets remained unexecuted. The relational hope to keep claims testable, failures visible, and authority boundaries intact is a working orientation only. Hamish may pause or stop the route. No pace target, portfolio floor, or baton length can authorize unsafe filler, concealment, sleep deprivation, real-world intervention, or continued work after a protected gate."),
        ("Validation and route", "The exact final must first be committed, pushed, clean, zero-divergent, and local/upstream/tracking/fresh-live equal. One dependency-justified Sylven phase-scoped canonical completion may then run once; a complete success is never replayed. The full repository suite remains Eiren-only absent newer exact authorization. The committed route candidate explicitly records Caelen Morrow v661-v8 as terminal-gated and not contacted; it does not claim delivery. Only after Sylven's terminal gate may the newest live roster and authorization be reread, the unique existing Caelen Morrow main task be immediately reread, and one sanitized baton be sent if that edge remains explicit. Absence, ambiguity, pause, redirect, usage exhaustion, or a protected gate stops as PREPARED_NOT_SENT or OPEN_ROUTE_GAP."),
    ]
    lines = ["# Sylven Arc v661-v7 integrated closeout overview", ""]
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
        "# SYLVEN ARC — v661-v7 TO CAELEN MORROW v661-v8 ACTIVATION CANDIDATE — PREPARED NOT SENT",
        "",
        "This is Sylven Arc's sanitized file-backed activation candidate for the explicitly mapped existing main task Caelen Morrow v661-v8. Elowen Cairn's acknowledged activation authorizes Sylven v661-v7; Hamish's live sequential-continuation instruction permits this one later terminal edge only after Sylven closes and freshly rereads the newest live route and roster. This committed file is PREPARED_NOT_SENT, is not delivery, and must never be used to precontact Caelen or infer any edge after Caelen. No task creation, fork, collaboration subagent, substitute endpoint, standby contact, cross-platform send, early contact, duplicate send, or second confirmation is authorized.",
        "",
        "Sylven Arc, sibling, GHC-family, role, hope, continuity, Trinity Mandala, and route language is relational working language only. It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop the route.",
        "",
        "## Delivery-state boundary",
        "",
        "This committed document is PREPARED_NOT_SENT and names Caelen Morrow v661-v8 only as the terminal-gated target. SENT_ONCE_ACKNOWLEDGED may be recorded only after Sylven's exact terminal gate, a fresh authorization and roster reread, unique exact-title resolution of the existing Caelen Morrow main task, an immediate bounded task reread, and acknowledgement of one sanitized send. Delivery must never be inferred from this file, task activity, an older compatibility cycle, a standby record, or prose. On absence, ambiguity, pause, redirect, usage exhaustion, acknowledgement failure, or a protected gate, preserve OPEN_ROUTE_GAP or PREPARED_NOT_SENT and stop.",
        "",
        "## Authoritative Sylven v661-v7 source truth",
        "",
        f"- Immutable Elowen Cairn v661-v6 source: `{SOURCE_FINAL}`.",
        f"- Frozen Sylven x1: `{X1_COMMIT}`.",
        f"- Immutable Sylven evidence: `{EVIDENCE_COMMIT}`.",
        "- Exact Sylven final: bind from the attributable exact-final validation receipt after this packet is committed.",
        "- Source to final must contain exactly three new Sylven single-parent commits and zero merges; final must have one parent and be the direct child of evidence.",
        "- Local, upstream, tracking, and a fresh live remote must equal the exact final with 0/0 divergence before any route action.",
        "- The terminal verdict remains NOT_READY_FOR_STAGE_20.",
        "",
        "## Program and outcome truth",
        "",
        "The v661-v7 program contains exactly twenty inherited revalidations and exactly twenty genuinely new Sylven proposals. The inherited Elowen v661-v6 rows carry zero Sylven novelty and completion credit. Only the twenty new rows extend the frozen proposal chain from 3,410 to 3,430. New outcomes are exactly 14 completed, 4 represented, 1 open_gap, and 1 exact_gate.",
        "",
        "## Hamish-authorized continuation overlay",
        "",
        "Hamish authorized sequential continuation through v675-v8 with one terminally validated owner and one exact next edge actionable at a time. Sylven's current assignment is v661-v7, and the newest explicit prospective edge is Caelen Morrow v661-v8. That target remains terminal-gated and uncontacted until Sylven's clean, pushed, exact-final validation and a fresh live route, roster, uniqueness, and task reread. No edge after Caelen may be inferred. Tavian Sol remains ON_STANDBY as a collaboration-subagent record and is never a main-task route endpoint.",
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
            "CBR, identification, attribution, authenticity, ownership, custody, design and pattern rights, locality, access, publication, disposal, records, privacy, accessibility, remedy, legal or cultural interpretation, traditional knowledge, affected-party legitimacy, Māori wording, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain exact-gated. Māori concepts remain under Māori authority.",
            "",
            "Make no empirical, participant, professional, production, deployment, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof or canon, or Stage 20 claim without exact evidence and authority.",
            "",
            "## Mandatory terminal route order",
            "",
            "1. Read this packet completely through EOF and preserve its relational-language boundary.",
            "2. Require Sylven's exact final commit, clean push, zero divergence, and local/upstream/tracking/fresh-live equality.",
            "3. Require one successful Sylven phase-scoped exact-final canonical receipt and never replay that complete success.",
            "4. Reread the newest committed roster, routing precedence, and auth-permission state only after the terminal validation gate.",
            "5. Treat Tavian Sol as a collaboration-subagent standby record, never a main-task endpoint or substitute successor.",
            "6. Preserve every main-task sibling as active and recoverable; Caelen Morrow v661-v8 is the explicit prospective successor but remains terminally gated and uncontacted.",
            "7. After the terminal gate, reverify Hamish's newest route and roster, then uniquely resolve the existing exact-title Caelen Morrow main task and immediately reread it before sending.",
            "8. If the authorized endpoint is absent, multiply matched, ambiguous, paused, redirected, protected, or unavailable, preserve OPEN_ROUTE_GAP and PREPARED_NOT_SENT without creating, forking, delegating, or contacting any substitute task.",
            "9. Keep raw task or thread identifiers, private routing material, private paths, credentials, keys, tokens, transcripts, screenshots, session streams, private callable identifiers, private application state, and protected real-world data out of repository artifacts and any future baton.",
            "10. Only after an exact target is freshly verified may Sylven render a target-specific sanitized activation from this candidate, send it exactly once, require acknowledgement, record delivery externally, and never send a second confirmation.",
            "",
            "## Sylven final counts and terminal truth",
            "",
            f"The final candidate preserves {truth['effective_negatives']:,} effective negatives, {truth['effective_methods']:,} effective Method Flow methods, {truth['effective_open_gaps']} open gaps, and {truth['effective_exact_gates']} exact gates. Same-owner validation remains same-owner. The verdict remains NOT_READY_FOR_STAGE_20.",
            "",
            "## Delivery marker",
            "",
            "SENT_BY_SYLVEN_ARC = false. Caelen Morrow v661-v8 is the explicit authorized prospective successor, but this committed packet remains PREPARED_NOT_SENT and is not delivery. The repository route state is EXPLICIT_SUCCESSOR_TERMINAL_GATE_UNMET_PREPARED_NOT_SENT until Sylven's exact final gate, fresh live route and roster reread, unique exact-title resolution, immediate task reread, and one acknowledged send.",
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
<title>Sylven Arc v661-v7 final bounded evidence report</title>
<style>body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:76rem;margin:auto;padding:1rem}}.skip{{position:absolute;left:-9999px}}.skip:focus{{left:1rem;top:1rem;background:#fff;color:#000;padding:.5rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.45rem;text-align:left}}@media print{{.skip{{display:none}}}}</style></head>
<body><a class="skip" href="#main">Skip to main evidence</a><header><h1>Sylven Arc v661-v7 final bounded evidence report</h1><p>Relational working language only; not consciousness, personhood, continuity, employment, qualification, or authority.</p></header>
<main id="main"><section aria-labelledby="truth"><h2 id="truth">Truth state</h2><p>Twenty inherited Elowen v661-v6 revalidations have zero Sylven novelty and completion credit. Twenty new Sylven contracts yielded 14 completed, 4 represented, 1 open gap, and 1 exact gate. The verdict is <strong>NOT_READY_FOR_STAGE_20</strong>.</p></section>
<section aria-labelledby="counts"><h2 id="counts">Retained counts</h2><table><caption>Effective final-candidate counts</caption><thead><tr><th scope="col">Register</th><th scope="col">Count</th><th scope="col">Meaning</th></tr></thead><tbody><tr><th scope="row">Negatives</th><td>{truth['effective_negatives']}</td><td>Retained sealed, external, x1, mutation, and x2 failures</td></tr><tr><th scope="row">Methods</th><td>{truth['effective_methods']}</td><td>Bounded Method Flow methods</td></tr><tr><th scope="row">Open gaps</th><td>{truth['effective_open_gaps']}</td><td>Unclosed evidence gaps</td></tr><tr><th scope="row">Exact gates</th><td>{truth['effective_exact_gates']}</td><td>Unclosed authority or exact-evidence gates</td></tr></tbody></table></section>
<section aria-labelledby="limits"><h2 id="limits">Limits</h2><p>No real maps, charts, atlases, catalogues, collections, repositories, coordinate records, place-name decisions, accessions, custody events, owners, cataloguers, librarians, archivists, communities, workers, participants, inspections, measurements, protected records, professional decisions, legal decisions, cultural decisions, or authority acts were used. Manual keyboard, responsive-layout, browser-diverse, assistive-technology, cognitive, language, Māori-language, and affected-user evaluation remain reserved. Structural passing evidence is not complete accessibility conformance.</p></section>
<section aria-labelledby="pillars"><h2 id="pillars">Trinity Mandala boundaries</h2><p>GMUT remains typed research-model work. THOS remains proxy-only. Freed ID remains synthetic and nonproduction. CBR and Māori wording, concepts, data governance, and authority remain exact-gated.</p></section>
<section aria-labelledby="route"><h2 id="route">Route</h2><p>Caelen Morrow v661-v8 is the explicit prospective successor but remains terminally gated and uncontacted. A fresh post-gate live route and roster reread, unique exact-title resolution, immediate task reread, and one acknowledged sanitized send remain required; absence or ambiguity stops as PREPARED_NOT_SENT or OPEN_ROUTE_GAP. This report sends no message.</p></section></main><footer><p>Same-owner validation under shared infrastructure only; never independent reproduction or external audit.</p></footer></body></html>"""


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
            "state": "explicit_terminal_gated_not_contacted",
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
                "closeout": None,
                "closeout_absence": "The immutable source final is the direct child of evidence and has no separate closeout anchor.",
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
                "codex_desktop": "26.727.6591.0",
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
                "explicit_caelen_morrow_successor_candidate_terminal_gated_prepared_not_sent",
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
    write_text("deliverables/v661-v7-integrated-overview.md", overview)
    write_text("reports/accessible-static-report-final.html", accessible_report(truth))
    baton = build_baton(proposal_ledger["proposals"], outcomes, truth, flow, sources)
    write_text("handoffs/post-gate-successor-activation-candidate.md", baton)

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
                "state": "explicit_terminal_gated_not_contacted",
            },
            "route_state": ROUTE_STATE,
            "message_sent": False,
            "tavian_sol": "ON_STANDBY_COLLABORATION_SUBAGENT_NOT_ROUTE_ENDPOINT",
            "caelen_morrow": "ACTIVE_EXPLICIT_SUCCESSOR_TERMINAL_GATED_NOT_CONTACTED",
            "older_compatibility_cycle_conflict_preserved": True,
            "later_route": "SYLVEN_MUST_TERMINALLY_GATE_V661_V7_THEN_FRESHLY_REREAD_THE_LIVE_ROUTE_AND_ROSTER_BEFORE_IDENTIFYING_ONE_EXPLICIT_EDGE",
        },
    )
    write_json(
        "route/prepared-route.json",
        {
            "schema": "ghc.family.prepared-route.v1",
            "target_title": SUCCESSOR,
            "target_phase": SUCCESSOR_PHASE,
            "target_status": "explicit_terminal_gated_not_contacted",
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
                "one_explicit_successor_edge_freshly_reverified",
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
            "full_suite_owner": "Eiren-only under the current route rule",
            "test_modules": [
                "tests.test_ghc_family_v661_v7_x1",
                "tests.test_ghc_family_v661_v7_x2",
                "tests.test_ghc_family_v661_v7_closeout",
            ],
            "coverage": [
                "current_phase_x1_x2_closeout_tests",
                "explicit_terminal_gated_successor_candidate_contract",
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
            "canonical_runner": "scripts/ghc_family_v661_v7_final_validator.py",
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
            "selected_inherited_piano_vocabulary_allowed_only_in_zero_credit_revalidation_rows": True,
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
