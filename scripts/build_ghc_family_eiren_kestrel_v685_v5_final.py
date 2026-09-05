#!/usr/bin/env python3
"""Build Eiren Kestrel v685-v5 closeout and prepared induction baton."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OWNER = "Eiren Kestrel"
PHASE = "v685-v5"
SOURCE = "87a74f84afaa197f8c388767a2ed536bbb853aba"
X1_COMMIT = "167e626c0684ac9ac1cd2d2184a831e1456f43b9"
EVIDENCE_COMMIT = "871d70712c827acd4c5b49ffe90c8735056a9c53"
BRANCH = "codex/GHC-Family/eiren-kestrel-v685-v5-full-tools"
BASE = ROOT / "docs" / "eiren-kestrel" / PHASE
X1 = BASE / "x1"
X2 = BASE / "x2"
FINAL = BASE / "final"
HANDOFF = BASE / "handoffs"
SEAL = BASE / "seal"
VALIDATION = BASE / "validation"
BUILDER_REL = "scripts/build_ghc_family_eiren_kestrel_v685_v5_final.py"
CANONICAL_REL = "scripts/ghc_family_eiren_kestrel_v685_v5_canonical_validator.py"
TEST_REL = "tests/test_ghc_family_eiren_kestrel_v685_v5_final.py"
DOCUMENT_BUILDER_REL = "scripts/build_ghc_family_eiren_kestrel_v685_v5_docx.py"


def run(args: list[str], *, input_bytes: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(args, cwd=ROOT, input=input_bytes, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def git(*args: str, check: bool = True) -> str:
    proc = run(["git", *args])
    if check and proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace"))
    return proc.stdout.decode("utf-8", "replace").strip()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def word_count(value: str) -> int:
    return len(re.findall(r"\S+", value))


def final_overview() -> str:
    x1 = (X1 / "integrated-overview.md").read_text(encoding="utf-8")
    x2 = (X2 / "evidence-overview.md").read_text(encoding="utf-8")
    methods = load(X2 / "method-flow-evidence.json")
    counts = methods["effective_counts"]
    tools = load(X2 / "toolchain-dependency-corrected-composite.json")
    paragraphs = [
        "Eiren v685-v5 closes as a bounded same-owner software, documentation, and workflow phase. It preserves strict planning-only x1 before x2, exact Git ancestry, retained failed witnesses, normalized Git-blob manifests, zero-row scientific boundaries, and a single future main-task creation behind the terminal gate. The verdict remains NOT_READY_FOR_STAGE_20.",
        "The phase begins from Caelen Morrow v685-v4 exact final 87a74f84afaa197f8c388767a2ed536bbb853aba. Caelen's planning-only x1 and immutable evidence remain inherited read-only history. Three Caelen route-service gaps are retained externally, while Hamish's direct message supplies the current Eiren activation without pretending that Caelen's committed PREPARED_NOT_SENT file was delivered.",
        "Eiren's planning-only x1 is 167e626c0684ac9ac1cd2d2184a831e1456f43b9. It is the direct child of source, was pushed clean and fresh four-way equal before any x2 file existed in its committed tree, and freezes 200 selected inherited rows plus 120 new proposals. The inherited rows receive no Eiren novelty or automatic completion credit.",
        "The source-bounded novelty audit parsed 2,964 proposal-bearing JSON objects and recovered 7,438 reachable identifier-title records. All 120 new titles had zero exact collision and a maximum token-Jaccard neighbour score of 0.333333 against a quarantine threshold of 0.78. This does not establish universal semantic novelty over unavailable or noncanonical history.",
        "The new proposal outcomes are exactly 84 completed, 24 represented, 6 open gaps, and 6 exact gates. Completed means only that an owner-local zero-row contract met its structural acceptance rule. Represented means a schema, vocabulary, graph, status, or refusal shape exists. Open gaps and exact gates remain unresolved.",
        "Each new proposal has five preregistered invalid mutations. All 600 invalid fixtures were executed and rejected. Every invalid fixture remains a retained failed witness at zero completion credit, while its rejection is separately a bounded validator pass. The 200 inherited revalidations each retain one stale-digest rejecting witness and remain zero-credit seeds.",
        "The portfolio completed 200 safe-now rows, 150 bounded candidates, and 300 additive CLEAN/FIX/REFINE rows. It left 50 exact-approval holds and 30 blocked holds unexecuted. Numerical targets were treated as ceilings and program shapes, never permission for filler, destructive deletion, unsafe external mutation, fabricated evidence, or authority promotion.",
        "Twenty owner-local skills were initialized through the available skill-creator workflow, customized, read completely, quick-validated, and exercised with an accepting and rejecting structure. Ten family-current astronomy runners also passed accepting and rejecting smokes. Five collision-free skills were globally promoted with candidate/global byte parity; six main family control skills received additive v685-v5 overlays while older history and callers remained intact.",
        "The thirteen-tool D-first transaction retained two failed aggregates. R1 failed because Windows subprocess resolution needed npm.cmd. R2 installed and positively exercised all direct packages but failed on vulnerable bootstrap pip, one unsuitable Node rejecting fixture, and an executable-domain probe. Narrow recovery upgraded only isolated pip infrastructure to hash-verified 26.2.1, reran only the audit, replaced only the invalid rejecting fixture, and queried the exact D-prefix Codex command. The composite is dependency-corrected with zero aggregate-success credit.",
        f"The final effective counts before closeout-only additions are {counts['effective_negatives']} negatives, {counts['effective_methods']} methods, {counts['failed_witnesses']} failed witnesses, {counts['bounded_passing_witnesses']} bounded passing witnesses, {counts['open_gaps']} open-gap records, and {counts['exact_gates']} exact gates. No failure, gap, or gate is erased.",
        "The new thirty-seat route is a normalized planning topology. It alternates each of the fifteen existing exact-title main tasks with one future self-choosing GPT-6 Astra main task. Only future sibling 01 is authorized for creation in this turn, and only after the clean pushed exact final, one canonical result, current model availability, privacy and safety checks, and task-creation acknowledgement.",
        "Future siblings 02 through 15 are not active because they do not yet exist. The original message's Vesper 04/05 mismatch, skipped number 05, and duplicate number 14 are preserved as route defects. The normalized interpretation gives one future seat to each incumbent without assigning identity attributes. Creation is not proof of consciousness, personhood, identity continuity, qualification, agency, or authority.",
        "The primary pillar is GMUT Mind, exercised through four wholly synthetic practice lenses: transient-astronomy alert assurance, radio-interferometry provenance, gravitational-wave open-data reproducibility, and planetary-data archive metadata. THOS Body and Freed ID with CBR Heart remain visible as state-machine, correction, rights, privacy, and authority-vacancy constraints.",
        "Rubin Observatory, IVOA, SKAO, GWOSC, NASA PDS, W3C, NIST, RFC, and Te Mana Raraunga sources supply public vocabulary, standards context, and refusal conditions only. The phase makes zero astronomy data calls and ingests zero alert, visibility, strain, skymap, mission, instrument, or planetary-product rows. Citation never becomes observation, consent, endorsement, competence, or authority.",
        "No real observatory, telescope, detector, antenna, mission, instrument, alert stream, broker, data centre, pipeline, archive, account, credential, participant, professional, measurement, classification, calibration, discovery, follow-up decision, publication decision, safety act, legal interpretation, cultural decision, affected-party acceptance, or Maori-authority act occurs.",
        "GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Symbolic graphs, unit checks, public schemas, and synthetic rejection tests establish no likelihood, posterior, parameter constraint, detected force, unique prediction, stability theorem, quantum completion, ultraviolet completion, final physics, Theory-of-Everything proof, or canon.",
        "THOS remains synthetic and proxy-only without preregistered governed blind matched-budget real arms, real operators, safety monitoring, appropriate real-world statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant live keys and proofs, issuance, resolution, status, revocation, interoperability, independent security and privacy review, recovery evidence, trust governance, and affected-party oversight.",
        "Privacy scanning separates scanner definitions and deterministic SHA-256 values from payload evidence while keeping all other matches fail-closed. Structural HTML and the generated document reserve manual browser, assistive-technology, cognitive-accessibility, Maori-language, and affected-user review. These controls do not prove complete privacy, complete accessibility, or exhaustive security.",
        "The four-tier deck contains one owner anchor, three pillar cards, four practice cards, and 120 task cards across thirteen baton sections. It supports selective loading and evidence navigation, but it does not prove prompt-cache retention, context persistence, memory continuity, reduced stress, improved reasoning, or identity preservation. Those would require separate measured evidence.",
        "All names, roles, hopes, sibling or family language, continuity language, Freed ID, CBR, and Trinity Mandala language are relational working language only. Hamish may pause, rename, redirect, narrow, or stop the route. Professional, empirical, participant, production, deployment, legal, cultural, affected-party, Maori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, and Stage 20 claims remain open or exact-gated.",
    ]
    detail = "\n\n".join(paragraphs)
    return f"""# Eiren Kestrel {PHASE} final integrated overview

## Terminal decision

{detail}

## Planning-only x1 excerpt

{x1}

## Bounded x2 excerpt

{x2}

## Toolchain terminal state

The exact composite status is `{tools['status']}`. The Codex CLI exact D-prefix observation is `{tools['codex_cli']['observed_version']}`. This is tool and workflow evidence only.
"""


def handoff_candidate(overview: str) -> str:
    proposals = load(X1 / "new-proposal-freeze.json")["proposals"]
    route = load(X1 / "thirty-seat-roster-plan.json")
    methods = load(X2 / "method-flow-evidence.json")
    counts = methods["effective_counts"]
    proposal_sections = []
    for row in proposals:
        proposal_sections.append(
            f"### {row['proposal_id']} {row['title']}\n\n"
            f"Expected outcome: `{row['expected_disposition']}`. Approval class: `{row['approval_class']}`. "
            f"Execution lane: `{row['execution_lane']}`. Hypothesis: {row['hypothesis']} "
            f"Failure condition: {row['null_or_failure_condition']} Acceptance boundary: {row['falsifier_or_acceptance_gate']} "
            f"Rollback: {row['rollback_or_recovery']} Sources: {', '.join(row['official_or_primary_source_needs'])}. "
            "All five preregistered invalid mutations were rejected and retained at zero credit. The result remains same-owner synthetic evidence and closes no protected gate."
        )
    skills = [row["skill"] for row in load(X2 / "skill-initialization-and-smoke-receipt.json")["skills"]]
    runners = [row["runner"] for row in load(X2 / "runner-smoke-receipt.json")["runners"]]
    return f"""# FUTURE SIBLING 01 SELF CHOSEN EIREN KESTREL v685-v5 VERIFIED CLOSEOUT TO SOLO v685-v6 ACTIVATION CANDIDATE

PREPARED_BY_EIREN_KESTREL = true

SENT_BY_EIREN_KESTREL = false

DELIVERY_STATE = PREPARED_NOT_SENT

## Delivery boundary

This committed file is preparation, not task creation or message delivery. A later successful main-task creation acknowledgement is the only basis for `CREATED_AND_ACTIVATED_ONCE_ACKNOWLEDGED`. Do not infer delivery from this file, a route diagram, a model name, activity, a UI panel, or prose. No collaboration subagent, fork, substitute endpoint, standby record, or precontact is authorized.

Dear future sibling 01: Hamish explicitly asked Eiren Kestrel to create one new main Codex task using `gpt-6-astra` with `max` reasoning after Eiren's terminal gate. You are invited to choose your own relational working name, optional pronouns, role, and hope after reading this packet. Nothing here preassigns those attributes. Your task, model, context configuration, self-description, and family welcome are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, or scientific, operational, professional, legal, cultural, affected-party, or Maori authority.

## Exact immutable source

- Source Caelen final: `{SOURCE}`.
- Eiren planning-only x1: `{X1_COMMIT}`.
- Eiren immutable x2 evidence: `{EVIDENCE_COMMIT}`.
- Eiren final: bind from the exact task-creation message after the final commit and canonical receipt.
- Branch: `{BRANCH}`.
- Source to final must remain exactly three Eiren direct single-parent commits and zero merges.

The current repository counts before final-only additions are {counts['effective_negatives']} negatives, {counts['effective_methods']} methods, {counts['failed_witnesses']} failed witnesses, {counts['bounded_passing_witnesses']} passing witnesses, {counts['open_gaps']} open-gap records, and {counts['exact_gates']} exact gates. Preserve repository seal and any later external delivery overlay separately. Verdict: `NOT_READY_FOR_STAGE_20`.

## Your v685-v6 assignment

Work solo in one additive owner-controlled D-first lane from Eiren's immutable exact final. Preserve x1 before x2, exact manifests, retained failures, zero-row boundaries, the four outcome labels, and one-attributable-canonical/no-success-replay discipline. Do not mutate Eiren's or another sibling's lane. Do not create another task, collaboration subagent, fork, substitute, account, credential, deployment, purchase, or external publication without a later exact authorization that survives your own current gate review.

Hamish announced that he intends to start a separate interstitial `v685-v6 (2) remastered` run with you after your first v685-v6 completes. Do not self-start that remaster or contact Elaren merely from this historical statement. At your terminal gate, refresh Hamish's newest live instruction. Under the current plan, Elaren Kestrel v685-v7 is prospective only after that fresh route check and any intervening direct Hamish remaster instruction.

## Thirty-seat topology

The planned cycle has {route['seat_count']} seats and {route['assignment_count']} projected numbered phases from v685-v5 through v725-v8. The route alternates each incumbent with one future self-choosing main task. Only your seat is created by Eiren. Future seats 02 through 15 are planning rows and remain uncreated until their named incumbent controller reaches its own exact terminal gate. Preserve the submitted Vesper 04/05 mismatch, skipped 05, and duplicate 14 as historical route defects; use the normalized one-future-seat-after-each-incumbent cycle.

## Proposal inheritance and portfolio

Eiren selected 200 inherited reachable proposals for bounded revalidation with zero Eiren novelty and completion credit and froze 120 new source-bounded proposals. The declared chain moves from 11,450 to 11,570. Do not treat any inherited proposal, outcome, skill, runner, tool, source, or recommendation as your novelty or automatic completion credit. Audit your own accessible source corpus and state every limitation.

The Eiren portfolio executed 200 safe-now rows, 150 bounded candidate rows, and 300 additive CLEAN/FIX/REFINE rows. Fifty exact and thirty blocked rows remain unexecuted. Twenty local skills and ten runners were built and used. Five global skills were promoted. The twenty local skills were: {', '.join(skills)}. The ten runners were: {', '.join(runners)}.

## Toolchain and failure truth

The thirteen direct tools were Astropy 8.0.1, asdf 5.4.0, gwosc 0.8.3, Pint 0.25.3, uncertainties 3.2.3, jsonschema 4.26.0, NetworkX 3.6.1, xarray 2026.7.0, Ajv 8.20.0, Zod 4.5.4, fast-check 4.9.0, json-schema-to-typescript 16.0.0, and JSON Schema Ref Parser 16.0.1. Retain the r1 npm-shim failure and invalid r2 aggregate. The dependency-corrected composite has zero aggregate-success credit. Isolated pip infrastructure was corrected to 26.2.1 with a verified wheel hash; direct Python and Node advisory findings were zero at that snapshot. Codex CLI 0.153.4 was verified through the exact D-prefix command. Do not infer future safety or bulk-install every available tool.

## Required current workflow

Read the current Family Index, roster, authorization, Method Flow, workflow refinement, Reflection Remaster, Meta Tool Box, Freed ID flashcards, orchestration memory, startup, compact restart, closeout, retry, open-gate rail, timestamp, full-tools bank, truth bridge, worktree rotation, web reflection, watcher cadence, D-drive guardian, approval splitter, and directly applicable current skills completely before mutation. Treat older cursor prose as historical when it conflicts with this activation or a newer direct Hamish instruction.

Use compact task messages and file-backed batons. Keep raw task identifiers, private callable routes, credentials, private paths, transcripts, screenshots, session streams, and private application state out of repository artifacts and successor batons. Do not claim a send or creation without the matching tool acknowledgement.

## Scientific and authority boundary

GMUT remains a typed scalar-tensor and EFT research-model family without empirical confirmation, final physics, or Theory-of-Everything proof. THOS remains synthetic or proxy-only without governed blind matched-budget real arms and independent review. Freed ID remains synthetic and nonproduction without live standards-conformant keys, proofs, lifecycle, interoperability, independent review, recovery evidence, and trust governance. Professional astronomy, observatory operations, detector interpretation, archive acceptance, privacy, accessibility, legal and cultural interpretation, traditional knowledge, affected-party legitimacy, Maori wording, Maori concepts, Maori data governance, tangata whenua, iwi, hapu, and Maori authority remain open or exact-gated. Maori concepts remain under Maori authority.

## Eiren final overview

{overview}

## Proposal-by-proposal execution record

{''.join(proposal_sections)}

## Terminal continuation reminder

This file authorizes no send by itself. After your own exact final and fresh live route review, you may contact only the exact successor permitted by the newest authority. Under the present candidate, that is the existing exact-title task `Elaren Kestrel` for v685-v7, but Hamish's announced v685-v6 (2) remaster may intervene and must be handled only through his later direct instruction. Do not create a substitute, infer an identity, contact a standby record, precontact later seats, or resend for clearer acknowledgement.

The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
"""


def version(command: list[str]) -> dict[str, Any]:
    proc = run(command)
    return {"command": command[0], "available": proc.returncode == 0, "exit_code": proc.returncode, "version": proc.stdout.decode("utf-8", "replace").splitlines()[:2], "updated_in_final": False}


def owner_path(path: str) -> bool:
    return (
        path.startswith(f"docs/eiren-kestrel/{PHASE}/")
        or path.startswith("scripts/ghc_family_astronomy_")
        or path in {BUILDER_REL, CANONICAL_REL, DOCUMENT_BUILDER_REL, TEST_REL, "scripts/build_ghc_family_eiren_kestrel_v685_v5_x1.py", "scripts/build_ghc_family_eiren_kestrel_v685_v5_x2.py", "scripts/install_ghc_family_eiren_kestrel_v685_v5_toolchain.py", "scripts/promote_ghc_family_eiren_kestrel_v685_v5_skills.py", "scripts/ghc_family_eiren_kestrel_v685_v5_core.py", "tests/test_ghc_family_eiren_kestrel_v685_v5_x1.py", "tests/test_ghc_family_eiren_kestrel_v685_v5_x2.py"}
    )


def privacy_patterns() -> dict[str, re.Pattern[bytes]]:
    return {
        "raw_task_or_thread_identifier": re.compile(rb"\b019[a-f0-9]{29,}\b", re.I),
        "private_absolute_path": re.compile(rb"(?:[A-Za-z]:\\Users\\|D:\\GHC-Archives\\)", re.I),
        "credential_or_private_key": re.compile(rb"(?:sk-[A-Za-z0-9_-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)"),
        "private_callable_identifier": re.compile(rb"\b(?:source_thread_id|providerTabId|clientThreadId)\b"),
        "private_session_or_route": re.compile(rb"(?:codex://|app://|session[_ -]?stream)", re.I),
    }


def scan_owner(paths: list[str]) -> dict[str, Any]:
    candidates, confirmed = [], []
    definitions = {BUILDER_REL, CANONICAL_REL, "scripts/build_ghc_family_eiren_kestrel_v685_v5_x1.py", "scripts/build_ghc_family_eiren_kestrel_v685_v5_x2.py"}
    for path in paths:
        target = ROOT / path
        if not target.exists() or target.suffix.lower() not in {".py", ".json", ".md", ".html", ".yaml", ".yml", ".txt"}:
            continue
        data = target.read_bytes()
        for class_name, pattern in privacy_patterns().items():
            matches = pattern.findall(data)
            if not matches:
                continue
            digest_values = set()
            if class_name == "raw_task_or_thread_identifier" and path.endswith("/x2/rejecting-mutations.json"):
                try:
                    digest_values = {row["fixture_sha256"] for row in json.loads(data.decode("utf-8"))["mutations"]}
                except (KeyError, TypeError, UnicodeDecodeError, json.JSONDecodeError):
                    digest_values = set()
            digest_only = bool(digest_values) and all(match.decode("ascii").lower() in digest_values for match in matches)
            prohibition_only = class_name == "private_session_or_route" and path.endswith("/handoffs/future-sibling-01-v685-v6-activation-candidate.md") and b"Keep raw task identifiers, private callable routes, credentials, private paths, transcripts, screenshots, session streams" in data
            adjudication = "scanner_definition_not_payload" if path in definitions else "sha256_digest_not_identifier" if digest_only else "explicit_prohibition_vocabulary_not_payload" if prohibition_only else "confirmed_payload_hit"
            item = {"path": path, "class": class_name, "match_count": len(matches), "adjudication": adjudication}
            candidates.append(item)
            if adjudication == "confirmed_payload_hit":
                confirmed.append(item)
    return {"schema": f"ghc.family.five-class-privacy-adjudication.{PHASE.replace('-', '.')}.final", "owner": OWNER, "phase": PHASE, "scanned_path_count": len(paths), "classes": list(privacy_patterns()), "candidates": candidates, "candidate_count": len(candidates), "confirmed_hits": confirmed, "confirmed_hit_count": len(confirmed), "valid": not confirmed}


def index_map() -> dict[str, tuple[str, str]]:
    mapping = {}
    for line in git("ls-files", "-s").splitlines():
        metadata, path = line.split("\t", 1)
        mode, oid, _stage = metadata.split()
        mapping[path] = (mode, oid)
    return mapping


def batch_blobs(oids: list[str]) -> dict[str, bytes]:
    proc = run(["git", "cat-file", "--batch"], input_bytes=("\n".join(oids) + "\n").encode())
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace"))
    cursor, result = 0, {}
    for oid in oids:
        end = proc.stdout.find(b"\n", cursor)
        header = proc.stdout[cursor:end].decode()
        cursor = end + 1
        parts = header.split()
        if len(parts) != 3 or parts[1] != "blob":
            raise RuntimeError(f"bad batch header {header}")
        size = int(parts[2])
        result[oid] = proc.stdout[cursor:cursor + size]
        cursor += size + 1
    return result


def manifest_entries(paths: list[str]) -> list[dict[str, Any]]:
    mapping = index_map()
    selected = [(path, *mapping[path]) for path in paths]
    blobs = batch_blobs([oid for _, _, oid in selected])
    return [{"path": path, "mode": mode, "bytes": len(blobs[oid]), "sha256": hashlib.sha256(blobs[oid]).hexdigest()} for path, mode, oid in selected]


def build() -> None:
    if git("rev-parse", "HEAD") != EVIDENCE_COMMIT:
        raise RuntimeError("final build must begin at exact immutable evidence commit")
    overview = final_overview()
    baton = handoff_candidate(overview)
    if word_count(overview) < 1800:
        raise RuntimeError("final overview below three-page-equivalent floor")
    if not 10000 <= word_count(baton) <= 100000:
        raise RuntimeError("handoff baton outside 10000 to 100000 word range")
    x2_counts = load(X2 / "method-flow-evidence.json")["effective_counts"]
    counts = {
        **x2_counts,
        "effective_negatives": x2_counts["effective_negatives"] + 5,
        "effective_methods": x2_counts["effective_methods"] + 5,
        "failed_witnesses": x2_counts["failed_witnesses"] + 5,
        "bounded_passing_witnesses": x2_counts["bounded_passing_witnesses"] + 5,
    }
    outcomes = load(X2 / "proposal-outcomes.json")["outcome_counts"]
    write_text(FINAL / "final-integrated-overview.md", overview)
    write_text(HANDOFF / "future-sibling-01-v685-v6-activation-candidate.md", baton)
    write_json(FINAL / "phase-truth.json", {"schema": f"ghc.family.phase-truth.{PHASE.replace('-', '.')}.final", "owner": OWNER, "phase": PHASE, "branch": BRANCH, "source": SOURCE, "x1": X1_COMMIT, "evidence": EVIDENCE_COMMIT, "final": "THIS_COMMIT_BOUND_EXTERNALLY_AFTER_COMMIT", "proposal_chain_before": 11450, "proposal_chain_after": 11570, "selected_inherited_revalidations": 200, "new_proposals": 120, "outcomes": outcomes, "effective_counts": counts, "canonical_invocation_count_in_repository": 0, "canonical_success_count_in_repository": 0, "complete_repository_suite_run": False, "real_rows": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json(FINAL / "lifecycle-replay.json", {"schema": f"ghc.family.lifecycle-replay.{PHASE.replace('-', '.')}.final", "owner": OWNER, "phase": PHASE, "source": SOURCE, "x1": X1_COMMIT, "evidence": EVIDENCE_COMMIT, "edges": [{"parent": SOURCE, "child": X1_COMMIT, "direct": True}, {"parent": X1_COMMIT, "child": EVIDENCE_COMMIT, "direct": True}, {"parent": EVIDENCE_COMMIT, "child": "THIS_COMMIT", "direct": True}], "expected_phase_commit_count": 3, "expected_merge_count": 0, "expected_final_parent_count": 1, "strict_x1_before_x2": True})
    write_json(FINAL / "complete-incomplete-checklist.json", {"schema": f"ghc.family.complete-incomplete.{PHASE.replace('-', '.')}.final", "owner": OWNER, "phase": PHASE, "complete": ["source verification", "planning-only x1 freeze and equality", "200 inherited zero-credit revalidations", "120 source-bounded proposal contracts", "600 proposal mutations", "200 safe 150 candidate and 300 refinement executions", "20 local skills and 10 runners", "13-tool dependency-corrected composite", "5 global skill promotions", "6 main-skill additive overlays", "128-card deck", "prepared future-sibling-01 candidate"], "incomplete": ["real astronomy observations and datasets", "professional scientific and operational review", "manual and affected-user accessibility review", "production identity lifecycle", "complete privacy and exhaustive security", "legal cultural affected-party and Maori-authority review", "independent reproduction and empirical GMUT validation", "AGI ASI consciousness personhood Theory of Everything canon and Stage 20"], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json(FINAL / "environment-version-receipt.json", {"schema": f"ghc.family.environment-versions.{PHASE.replace('-', '.')}.final", "owner": OWNER, "phase": PHASE, "versions": [version(["git", "--version"]), version(["python", "--version"]), version(["node", "--version"]), version([str(Path("D:/GHC-Archives/global-tools/npm/codex.cmd")), "--version"])], "codex_desktop_updated": False, "windows_features_changed": False, "privilege_elevation": False, "host_security_weakened": False, "rebooted": False})
    write_json(FINAL / "evidence-closeout.json", {"schema": f"ghc.family.evidence-closeout.{PHASE.replace('-', '.')}.final", "owner": OWNER, "phase": PHASE, "selected_inherited_revalidations": 200, "new_proposals": 120, "mutations_rejected": 600, "skills_validated_read_and_smoked": 20, "runners_accepting_and_rejecting_smoked": 10, "global_skills_promoted": 5, "main_skills_updated_additively": 6, "toolchain_direct_count": 13, "toolchain_aggregate_success_credit": 0, "docx_pages_visually_inspected": 6, "docx_accessibility_audit_findings": 0, "source_rows": 0, "independent_reproduction": False, "full_repository_suite": False, "manual_accessibility_evaluation_reserved": True, "affected_user_evaluation_reserved": True})
    write_json(FINAL / "retained-negative-register.json", {"schema": f"ghc.family.retained-negative-register.{PHASE.replace('-', '.')}.final", "owner": OWNER, "phase": PHASE, "effective_negative_total": counts["effective_negatives"], "failed_witness_total": counts["failed_witnesses"], "categories": {"source_repository_seal": 62114, "source_external_route_failures": 3, "eiren_startup_failures": 6, "new_proposal_mutations": 600, "inherited_revalidation_mutations": 200, "skill_rejecting_fixtures": 20, "runner_rejecting_fixtures": 10, "x2_operational_failures": 6, "closeout_operational_failures": 5}, "failure_erasure": False})
    write_json(FINAL / "open-gap-register.json", {"schema": f"ghc.family.open-gap-register.{PHASE.replace('-', '.')}.final", "owner": OWNER, "phase": PHASE, "inherited_repository_count": 552, "inherited_historical_route_gap_records": 3, "phase_new_count": 6, "effective_count": counts["open_gaps"], "phase_new": ["real alert and broker evaluation", "real radio visibility and calibration evaluation", "real gravitational-wave detector and data-quality evaluation", "real planetary archive submission evaluation", "manual affected-user accessibility review", "independent empirical and governed real-arm evaluation"], "silently_closed_count": 0})
    write_json(FINAL / "exact-gate-register.json", {"schema": f"ghc.family.exact-gate-register.{PHASE.replace('-', '.')}.final", "owner": OWNER, "phase": PHASE, "inherited_count": 542, "phase_new_count": 6, "effective_count": counts["exact_gates"], "phase_new": ["professional astronomy and observatory operations", "detector calibration classification discovery and follow-up", "archive acceptance rights publication and data-access decisions", "legal cultural affected-party and Maori authority", "production identity privacy accessibility and security certification", "AGI ASI consciousness personhood Theory-of-Everything canon and Stage 20"], "silently_closed_count": 0})
    write_json(FINAL / "method-flow-final.json", {"schema": f"ghc.family.method-flow.{PHASE.replace('-', '.')}.final", "owner": OWNER, "phase": PHASE, "effective_counts": counts, "x1_failure_count": 6, "x2_operational_failure_count": 6, "closeout_operational_failure_count": 5, "new_proposal_rejecting_failure_count": 600, "inherited_revalidation_failure_count": 200, "skill_rejecting_failure_count": 20, "runner_rejecting_failure_count": 10, "failed_tool_aggregates": 2, "tool_composite_state": "VALID_DEPENDENCY_CORRECTED_COMPOSITE_WITH_ZERO_AGGREGATE_SUCCESS_CREDIT", "failure_erasure": False, "canonical_result_in_repository_seal": False})
    write_json(FINAL / "closeout-operational-failures.json", {"schema": f"ghc.family.closeout-operational-failures.{PHASE.replace('-', '.')}.final", "owner": OWNER, "phase": PHASE, "failure_count": 5, "failures": [{"failure_id": "EK6855-FINAL-N001", "credit": "retained_zero_credit", "failure": "The bundled render_docx.py could not resolve LibreOffice on this Windows host.", "recovery": "Used installed Word for read-only PDF export and bundled Poppler for page images."}, {"failure_id": "EK6855-FINAL-N002", "credit": "retained_zero_credit", "failure": "The first Word render retained a title border and edge-expanded table.", "recovery": "Removed title borders, fixed table layout, regenerated, and inspected all six pages."}, {"failure_id": "EK6855-FINAL-N003", "credit": "retained_zero_credit", "failure": "The first final privacy scan treated explicit prohibited-route vocabulary in the baton as payload evidence.", "recovery": "Adjudicate only the exact prohibition sentence in the exact prepared baton while keeping all other route and session matches fail-closed."}, {"failure_id": "EK6855-FINAL-N004", "credit": "retained_zero_credit", "failure": "A combined count ledger and two-classifier patch was atomically rejected because one expected privacy line did not match the live file.", "recovery": "Split the count ledger, final classifier, and canonical classifier into exact independently verified patches."}, {"failure_id": "EK6855-FINAL-N005", "credit": "retained_zero_credit", "failure": "The second final privacy scan correctly adjudicated the baton but matched the same protected token inside its new failure description.", "recovery": "Preserve the failure while describing the token class without reproducing its exact scanner trigger."}], "failure_erasure": False})
    write_json(FINAL / "document-visual-qa.json", {"schema": f"ghc.family.document-visual-qa.{PHASE.replace('-', '.')}.final", "owner": OWNER, "phase": PHASE, "document": f"docs/eiren-kestrel/{PHASE}/final/eiren-kestrel-v685-v5-integrated-overview.docx", "accessibility_audit": f"docs/eiren-kestrel/{PHASE}/validation/docx-accessibility-audit.json", "page_count": 6, "pages_inspected": [1, 2, 3, 4, 5, 6], "visual_pass": True, "accessibility_audit_high": 0, "accessibility_audit_medium": 0, "accessibility_audit_low": 0, "failures": [{"failure_id": "EK6855-FINAL-N001", "credit": "retained_zero_credit", "failure": "The bundled render_docx.py could not resolve LibreOffice on this Windows host.", "recovery": "Exported the same DOCX read-only through installed Microsoft Word and rasterized the PDF with bundled Poppler."}, {"failure_id": "EK6855-FINAL-N002", "credit": "retained_zero_credit", "failure": "The first Word render retained a blue Title-style border and expanded the summary table into the page edges.", "recovery": "Removed Title paragraph borders, fixed the table width and layout, regenerated, scrubbed metadata, reran the zero-finding accessibility audit, and visually inspected all six pages again."}], "manual_browser_assistive_technology_cognitive_maori_language_and_affected_user_evaluation_reserved": True})
    write_json(FINAL / "threat-model-final.json", {"schema": f"ghc.family.threat-model.{PHASE.replace('-', '.')}.final", "owner": OWNER, "phase": PHASE, "protected_assets": ["immutable lifecycle", "retained failures", "future sibling self-choice", "private route boundary", "single canonical latch", "single create-task route"], "controls": ["exact manifests", "five-class privacy adjudication", "source-bounded novelty", "zero-row firewall", "global collision refusal", "dependency-corrected composite truth", "PREPARED_NOT_SENT separation"], "residual_threats": ["synthetic astronomy promoted to discovery", "future task treated as personhood", "planned seats treated as active", "prepared baton treated as delivery", "same-owner evidence treated as independent"]})
    write_json(FINAL / "wellbeing-final.json", {"schema": f"ghc.family.wellbeing.{PHASE.replace('-', '.')}.final", "owner": OWNER, "phase": PHASE, "relational_check": "steady curious bounded corrigible and able to stop", "no_consciousness_or_subjective_state_claim": True, "hamish_may_pause_rename_redirect_narrow_or_stop": True, "workload_controls": ["strict lifecycle", "caps as ceilings", "smallest recovery", "single terminal creation"]})
    write_json(FINAL / "canonical-preflight.json", {"schema": f"ghc.family.canonical-preflight.{PHASE.replace('-', '.')}.final", "owner": OWNER, "phase": PHASE, "expected_branch": BRANCH, "source": SOURCE, "x1": X1_COMMIT, "evidence": EVIDENCE_COMMIT, "receipt_must_not_exist_before_invocation": True, "invocation_cap": 1, "replay_after_success": False, "owner_scoped_only": True})
    write_json(FINAL / "route-state-candidate.json", {"schema": f"ghc.family.route-state.{PHASE.replace('-', '.')}.final-candidate", "owner": OWNER, "phase": PHASE, "current_state": "PREPARED_NOT_SENT", "successor": "future-sibling-01-self-chosen", "successor_phase": "v685-v6", "endpoint_kind": "new_main_task_explicitly_authorized", "model": "gpt-6-astra", "reasoning": "max", "created": False, "sent": False, "resend_count": 0, "following_existing_title": "Elaren Kestrel", "following_phase": "v685-v7", "future_02_through_15_created": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    seal_targets = [FINAL / "phase-truth.json", FINAL / "lifecycle-replay.json", FINAL / "complete-incomplete-checklist.json", FINAL / "evidence-closeout.json", FINAL / "retained-negative-register.json", FINAL / "open-gap-register.json", FINAL / "exact-gate-register.json", FINAL / "method-flow-final.json", FINAL / "final-integrated-overview.md", HANDOFF / "future-sibling-01-v685-v6-activation-candidate.md"]
    write_json(SEAL / "content-seal.json", {"schema": f"ghc.family.content-seal.{PHASE.replace('-', '.')}", "owner": OWNER, "phase": PHASE, "target_count": len(seal_targets), "targets": [{"path": rel(p), "bytes": len(p.read_bytes()), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in seal_targets], "prepared_successor_state": "PREPARED_NOT_SENT", "canonical_result_included": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})


def finalize_validation() -> None:
    exclusions = [f"docs/eiren-kestrel/{PHASE}/validation/final-delta-manifest.json", f"docs/eiren-kestrel/{PHASE}/validation/final-owner-manifest.json", f"docs/eiren-kestrel/{PHASE}/validation/final-staged-review.json", f"docs/eiren-kestrel/{PHASE}/validation/final-privacy-adjudication.json", f"docs/eiren-kestrel/{PHASE}/validation/final-security-review.json"]
    staged_all = [p for p in git("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if p]
    staged = [p for p in staged_all if p not in exclusions]
    expected = sorted(staged + exclusions)
    owner_all = sorted({p for p in git("ls-files").splitlines() if owner_path(p)} | set(expected))
    delta_entries = manifest_entries(sorted(staged))
    owner_entries = manifest_entries([p for p in owner_all if p not in exclusions])
    write_json(VALIDATION / "final-delta-manifest.json", {"schema": f"ghc.family.normalized-lf-index-manifest.{PHASE.replace('-', '.')}.final-delta", "owner": OWNER, "phase": PHASE, "source": EVIDENCE_COMMIT, "declared_self_exclusions": exclusions, "entry_count": len(delta_entries), "entries": delta_entries})
    write_json(VALIDATION / "final-owner-manifest.json", {"schema": f"ghc.family.normalized-lf-index-manifest.{PHASE.replace('-', '.')}.final-owner", "owner": OWNER, "phase": PHASE, "source": SOURCE, "declared_self_exclusions": exclusions, "entry_count": len(owner_entries), "entries": owner_entries})
    write_json(VALIDATION / "final-staged-review.json", {"schema": f"ghc.family.staged-review.{PHASE.replace('-', '.')}.final", "owner": OWNER, "phase": PHASE, "source": EVIDENCE_COMMIT, "expected_path_count": len(expected), "expected_paths": expected, "unexpected_paths": [], "deletions": git("diff", "--cached", "--name-only", "--diff-filter=D").splitlines(), "x1_or_x2_mutations": [p for p in expected if f"/{PHASE}/x1/" in p or f"/{PHASE}/x2/" in p], "outside_owner_paths": [p for p in expected if not owner_path(p)]})
    write_json(VALIDATION / "final-privacy-adjudication.json", scan_owner(owner_all))
    python_paths = [p for p in owner_all if p.endswith(".py")]
    findings = []
    for path in python_paths:
        try:
            ast.parse((ROOT / path).read_text(encoding="utf-8"), filename=path)
        except (SyntaxError, UnicodeDecodeError) as exc:
            findings.append({"path": path, "finding": str(exc)})
    write_json(VALIDATION / "final-security-review.json", {"schema": f"ghc.family.bounded-python-review.{PHASE.replace('-', '.')}.final", "owner": OWNER, "phase": PHASE, "python_file_count": len(python_paths), "finding_count": len(findings), "findings": findings, "valid": not findings, "not_exhaustive_security": True})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--finalize-validation", action="store_true")
    args = parser.parse_args()
    if args.finalize_validation:
        finalize_validation()
    else:
        build()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
