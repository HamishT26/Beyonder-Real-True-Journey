#!/usr/bin/env python3
"""Build the x1-only packet for Eiren Kestrel v648-v3 repeat phase."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import ghc_family_v648_v3_2_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "eiren-kestrel" / d.PHASE_SLUG
PRIOR_PHASE = ROOT / "docs" / "eiren-kestrel" / "v648-v3"


def write_json(relative: str, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str, payload: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8"
    ).stdout.strip()


def normalized_tokens(value: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", value.casefold())
        if token not in {"and", "or", "the", "a", "an", "of", "to", "for", "with"}
    }


def jaccard(left: set[str], right: set[str]) -> float:
    return len(left & right) / max(1, len(left | right))


def portfolio_rows(titles: list[str], prefix: str, lane: str) -> list[dict[str, Any]]:
    rows = []
    for index, title in enumerate(titles, start=1):
        rows.append(
            {
                "task_id": f"V6483R2-{prefix}-{index:02d}",
                "title": title,
                "approval_class": "safe_now" if prefix in {"SAFE", "CLEAN"} else "candidate",
                "execution_lane": lane,
                "origin": "eiren_repeat_phase_new",
                "x1_state": "frozen_not_executed",
                "x2_completion_credit": False,
                "boundary": "Local additive work only; reclassify visibly if a real authority, participant, credential, deployment, destructive, or sibling-lane gate appears.",
            }
        )
    return rows


def method_artifacts() -> None:
    records = [
        {
            "method_id": "V6483R2-M01",
            "title": "Independent receipts for expected no-match probes",
            "failure_signature": "An aggregate preflight aborts because one read-only discovery command returns an expected no-match exit.",
            "trigger_preconditions": ["A preflight combines instruction discovery with unrelated drive or Git probes."],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": "Run each probe independently and normalize only the documented expected no-match exit.",
            "validation_witness_ids": [],
            "recurrence_guard": "Do not aggregate unrelated read-only probes under fail-fast Promise.all when one command uses exit 1 for no matches.",
            "rollback": "Give the aggregate wrapper zero evidence credit and rerun only the required probes independently.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["startup_truth", "drive_state", "exact_head", "evidence_credit"],
            "retained_negative_ids": ["V6483R2-X1-N01"],
            "scope_boundary": "Local read-only preflight orchestration only.",
        },
        {
            "method_id": "V6483R2-M02",
            "title": "Materialize PowerShell foreach output before pipelines",
            "failure_signature": "Windows PowerShell raises EmptyPipeElement when a foreach statement is piped directly after a statement block.",
            "trigger_preconditions": ["A PowerShell command needs to serialize objects produced by foreach."],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": "Assign foreach output to an array, then pipe the array to the consumer.",
            "validation_witness_ids": [],
            "recurrence_guard": "Use $rows=@(foreach(...){...}); $rows | ConvertTo-Json and never direct foreach-to-pipeline composition.",
            "rollback": "Retain the parser failure and replace only the orchestration form, not the underlying inspection.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["inspection_truth", "negative_retention", "evidence_credit"],
            "retained_negative_ids": ["V6483R2-X1-N02", "V6483R2-X1-N03", "V6483R2-X1-N04"],
            "scope_boundary": "PowerShell enumeration orchestration only.",
        },
        {
            "method_id": "V6483R2-M03",
            "title": "Conservative proposal-title collision replacement",
            "failure_signature": "The x1 builder rejects a proposed title at or above the frozen lexical-overlap threshold.",
            "trigger_preconditions": ["A new core proposal is compared with the complete inherited frozen-title corpus."],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": "Replace the proposal with a substantively different surface and rerun the unchanged threshold.",
            "validation_witness_ids": [],
            "recurrence_guard": "Never lower the novelty threshold to admit a collision; change the research surface instead.",
            "rollback": "Retain the rejected proposal and restore the last collision-free x1 candidate.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["semantic_novelty", "x1_freeze_integrity", "completion_credit"],
            "retained_negative_ids": ["V6483R2-X1-N05"],
            "scope_boundary": "Lexical screening is a conservative novelty aid, not proof of scientific novelty.",
        },
        {
            "method_id": "V6483R2-M04",
            "title": "Explicit numeric-key selection for tied diagnostics",
            "failure_signature": "A diagnostic max operation compares payload dictionaries after equal numeric scores tie.",
            "trigger_preconditions": ["A diagnostic ranks tuples containing a score and a structured payload."],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": "Select the maximum with an explicit numeric-score key and report the payload separately.",
            "validation_witness_ids": [],
            "recurrence_guard": "Never rely on tuple fallback ordering when later tuple fields are mappings or heterogeneous objects.",
            "rollback": "Give the failed diagnostic zero evidence credit and rerun the same data with numeric-key ordering.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["diagnostic_truth", "semantic_novelty", "evidence_credit"],
            "retained_negative_ids": ["V6483R2-X1-N06"],
            "scope_boundary": "Local diagnostic ordering only; it does not change the novelty threshold.",
        },
        {
            "method_id": "V6483R2-M05",
            "title": "Pre-launch UTF-8 for Unicode diagnostics",
            "failure_signature": "A Python diagnostic fails while printing macron-bearing text through the Windows cp1252 console encoder.",
            "trigger_preconditions": ["A Windows child process may print te reo Maori or other non-ASCII source text."],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": "Set PYTHONUTF8=1 before process launch and rerun unchanged content.",
            "validation_witness_ids": [],
            "recurrence_guard": "Pin UTF-8 before launching Unicode-emitting diagnostics; never transliterate valid source text to satisfy a console locale.",
            "rollback": "Retain the encoding failure and rerun the unchanged diagnostic only under explicit UTF-8.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["unicode_integrity", "maori_authority_text", "evidence_credit"],
            "retained_negative_ids": ["V6483R2-X1-N07"],
            "scope_boundary": "Console encoding recovery only; it confers no cultural authority or content approval.",
        },
        {
            "method_id": "V6483R2-M06",
            "title": "Windows-local New Zealand timestamp fallback",
            "failure_signature": "Python cannot resolve the Pacific/Auckland IANA key because the optional tzdata package is absent on Windows.",
            "trigger_preconditions": ["A phase timestamp needs New Zealand local time on a host already configured to that timezone."],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": "Use datetime.astimezone with the configured Windows timezone and verify its UTC offset is plus twelve or plus thirteen hours.",
            "validation_witness_ids": [],
            "recurrence_guard": "Do not install tzdata merely for a phase timestamp; fail closed if the configured local offset is not a valid New Zealand offset.",
            "rollback": "Retain the missing-zone failure and omit local-time credit if the configured offset check fails.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["timestamp_truth", "host_change_boundary", "evidence_credit"],
            "retained_negative_ids": ["V6483R2-X1-N08"],
            "scope_boundary": "Timestamp rendering only; it does not change the host timezone or install a package.",
        },
        {
            "method_id": "V6483R2-M07",
            "title": "Exact frozen route-enum validation",
            "failure_signature": "A validator rejects a valid frozen route because it expects an unfrozen synonym for the same message mode.",
            "trigger_preconditions": ["A phase contract serializes a route or lifecycle enum that later validators must inspect."],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": "Read and validate the exact frozen enum rather than substituting a reviewer-local synonym.",
            "validation_witness_ids": [],
            "recurrence_guard": "Treat serialized lifecycle enums as contracts and centralize or import them when practical.",
            "rollback": "Retain the failed review and keep the freeze blocked until validator and frozen contract agree exactly.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["route_truth", "x1_freeze_integrity", "completion_credit"],
            "retained_negative_ids": ["V6483R2-X1-N09"],
            "scope_boundary": "Route-mode vocabulary only; no message has been sent.",
        },
        {
            "method_id": "V6483R2-M08",
            "title": "Dynamic retained-negative arithmetic",
            "failure_signature": "A projected retained-negative total remains hard-coded after the operational-negative list grows.",
            "trigger_preconditions": ["A phase derives an effective total from inherited, operational, and synthetic negative counts."],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": "Compute the total from its authoritative component counts and validate the same equation.",
            "validation_witness_ids": [],
            "recurrence_guard": "Never hand-update a derived negative total; retain components and calculate the projection at generation time.",
            "rollback": "Retain the stale receipt and block the freeze until the recomputed total and component counts agree.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["retained_negatives", "negative_non_erasure", "completion_credit"],
            "retained_negative_ids": ["V6483R2-X1-N10"],
            "scope_boundary": "Bookkeeping correction only; it does not transform a failed result into a pass.",
        },
        {
            "method_id": "V6483R2-M09",
            "title": "Exact scanner-definition privacy disposition",
            "failure_signature": "A staged privacy scan treats a scanner's literal pattern definition as a confirmed payload hit.",
            "trigger_preconditions": ["A staged source file contains the exact privacy regular expressions it executes."],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": "Classify only exact reviewed scanner-definition paths separately while retaining payload-hit treatment everywhere else.",
            "validation_witness_ids": [],
            "recurrence_guard": "Keep a narrow exact scanner-definition set; never exempt a directory, wildcard, generated artifact, or unrelated script.",
            "rollback": "Retain the failed scan and keep the commit blocked if any candidate occurs outside an exact scanner-definition path.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["privacy", "raw_identifier_exclusion", "exact_staged_surface"],
            "retained_negative_ids": ["V6483R2-X1-N11"],
            "scope_boundary": "Literal scanner definitions only; zero structural hits are not complete privacy assurance.",
        },
    ]
    witnesses = [
        {
            "witness_id": "V6483R2-M01-WFAIL",
            "method_id": "V6483R2-M01",
            "procedure": "Run AGENTS discovery, drive state and worktree inspection in one fail-fast aggregate wrapper.",
            "scope": "bounded startup preflight",
            "expected": "Every child result remains attributable.",
            "observed": "The expected no-match exit aborted the wrapper and discarded sibling results.",
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["V6483R2-X1-N01"],
            "boundary": "Failed orchestration witness only; no Git state changed.",
        },
        {
            "witness_id": "V6483R2-M01-WPASS",
            "method_id": "V6483R2-M01",
            "procedure": "Run instruction, drive and worktree probes independently and normalize the no-match exit.",
            "scope": "bounded startup preflight",
            "expected": "No AGENTS file, drive capacity and exact worktree state are independently returned.",
            "observed": "Each probe returned a durable attributable result and the lane was created from the verified source.",
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["V6483R2-X1-N01"],
            "boundary": "Bounded local workflow recovery only.",
        },
        {
            "witness_id": "V6483R2-M02-WFAIL",
            "method_id": "V6483R2-M02",
            "procedure": "Pipe direct foreach output into ConvertTo-Json in Windows PowerShell.",
            "scope": "bounded corpus and portfolio inspection",
            "expected": "The produced objects are serialized.",
            "observed": "Three commands raised EmptyPipeElement before returning complete evidence.",
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["V6483R2-X1-N02", "V6483R2-X1-N03", "V6483R2-X1-N04"],
            "boundary": "Failed parser witnesses remain retained.",
        },
        {
            "witness_id": "V6483R2-M02-WPASS",
            "method_id": "V6483R2-M02",
            "procedure": "Materialize foreach output into an array before serializing it.",
            "scope": "bounded corpus and portfolio inspection",
            "expected": "All requested term counts and titles are returned.",
            "observed": "The corrected probes returned the 580-title baseline and novelty-term counts without parser failure.",
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["V6483R2-X1-N02", "V6483R2-X1-N03", "V6483R2-X1-N04"],
            "boundary": "Bounded PowerShell workflow recovery only.",
        },
        {
            "witness_id": "V6483R2-M03-WFAIL",
            "method_id": "V6483R2-M03",
            "procedure": "Run the x1 builder with the target-trial proposal against all 580 inherited titles.",
            "scope": "bounded proposal-title novelty screen",
            "expected": "Every proposed title remains below the frozen overlap threshold.",
            "observed": "The target-trial title reached the 0.50 threshold and the builder stopped before artifact generation.",
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["V6483R2-X1-N05"],
            "boundary": "Failed lexical novelty witness only; no x1 freeze was published.",
        },
        {
            "witness_id": "V6483R2-M03-WPASS",
            "method_id": "V6483R2-M03",
            "procedure": "Replace the collision with the marginal-structural-model surface and rerun the unchanged corpus and threshold.",
            "scope": "bounded proposal-title novelty screen",
            "expected": "All ten titles remain below the unchanged 0.50 threshold.",
            "observed": "The replacement slate passed the complete 580-title lexical screen without lowering the threshold.",
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["V6483R2-X1-N05"],
            "boundary": "Lexical separation only; substantive scientific novelty remains bounded by the preregistration audit.",
        },
        {
            "witness_id": "V6483R2-M04-WFAIL",
            "method_id": "V6483R2-M04",
            "procedure": "Select the maximum diagnostic tuple without a key when two scores tie and payloads are mappings.",
            "scope": "bounded collision diagnostic",
            "expected": "The highest-scoring title pair is reported.",
            "observed": "Python raised TypeError while attempting to order tied dictionary payloads.",
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["V6483R2-X1-N06"],
            "boundary": "Failed diagnostic witness only; no proposal received novelty credit.",
        },
        {
            "witness_id": "V6483R2-M04-WPASS",
            "method_id": "V6483R2-M04",
            "procedure": "Select the same diagnostic maximum with an explicit numeric score key.",
            "scope": "bounded collision diagnostic",
            "expected": "The highest-scoring pair is reported without comparing payload mappings.",
            "observed": "The diagnostic completed and exposed the exact colliding pair for replacement.",
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["V6483R2-X1-N06"],
            "boundary": "Diagnostic transport recovery only; the underlying threshold was unchanged.",
        },
        {
            "witness_id": "V6483R2-M05-WFAIL",
            "method_id": "V6483R2-M05",
            "procedure": "Print the collision diagnostic under the inherited Windows cp1252 console environment.",
            "scope": "bounded Unicode diagnostic output",
            "expected": "Macron-bearing source text is preserved and printed.",
            "observed": "The console encoder raised UnicodeEncodeError at a Maori macron.",
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["V6483R2-X1-N07"],
            "boundary": "Failed encoding witness only; source text was not altered.",
        },
        {
            "witness_id": "V6483R2-M05-WPASS",
            "method_id": "V6483R2-M05",
            "procedure": "Set PYTHONUTF8=1 before launch and rerun the unchanged diagnostic.",
            "scope": "bounded Unicode diagnostic output",
            "expected": "The diagnostic exits successfully while preserving macron-bearing text.",
            "observed": "The unchanged diagnostic completed under UTF-8 and retained the original Unicode content.",
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["V6483R2-X1-N07"],
            "boundary": "Console recovery only; no Maori authority or content validation is conferred.",
        },
        {
            "witness_id": "V6483R2-M06-WFAIL",
            "method_id": "V6483R2-M06",
            "procedure": "Resolve Pacific/Auckland through zoneinfo on the current Windows Python installation.",
            "scope": "bounded phase timestamp rendering",
            "expected": "The IANA zone resolves without changing the host.",
            "observed": "ZoneInfoNotFoundError was raised because the optional tzdata package was absent.",
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["V6483R2-X1-N08"],
            "boundary": "Failed timestamp dependency witness only; no artifact was frozen and no package was installed.",
        },
        {
            "witness_id": "V6483R2-M06-WPASS",
            "method_id": "V6483R2-M06",
            "procedure": "Use the configured Windows local timezone and require a plus-twelve or plus-thirteen-hour UTC offset.",
            "scope": "bounded phase timestamp rendering",
            "expected": "New Zealand local time is rendered without an optional package or host change.",
            "observed": "The configured local timezone produced an accepted New Zealand offset and the timestamp was recorded.",
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["V6483R2-X1-N08"],
            "boundary": "Local timestamp recovery only; no timezone configuration was changed.",
        },
        {
            "witness_id": "V6483R2-M07-WFAIL",
            "method_id": "V6483R2-M07",
            "procedure": "Run the x1 review while expecting short_existing_task_pointer_to_committed_file.",
            "scope": "bounded route-contract validation",
            "expected": "The frozen route mode passes its exact contract check.",
            "observed": "The review returned 32 of 33 because the packet used the valid frozen enum short_existing_task_file_pointer.",
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["V6483R2-X1-N09"],
            "boundary": "Failed validator-contract witness only; no route message was sent.",
        },
        {
            "witness_id": "V6483R2-M07-WPASS",
            "method_id": "V6483R2-M07",
            "procedure": "Validate the exact route mode serialized by the frozen packet.",
            "scope": "bounded route-contract validation",
            "expected": "The exact frozen route enum passes while message_sent remains false.",
            "observed": "The corrected contract check accepted the exact enum and retained PREPARED_NOT_SENT truth.",
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["V6483R2-X1-N09"],
            "boundary": "Vocabulary recovery only; it grants no delivery credit.",
        },
        {
            "witness_id": "V6483R2-M08-WFAIL",
            "method_id": "V6483R2-M08",
            "procedure": "Inspect the projected retained-negative total after the operational list grows.",
            "scope": "bounded negative-ledger bookkeeping",
            "expected": "The projected total equals inherited plus operational plus synthetic negatives.",
            "observed": "The receipt still contained 4200 although its component counts no longer summed to that value.",
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["V6483R2-X1-N10"],
            "boundary": "Failed bookkeeping witness only; no negative was erased.",
        },
        {
            "witness_id": "V6483R2-M08-WPASS",
            "method_id": "V6483R2-M08",
            "procedure": "Regenerate the projection from 4126 inherited, current operational, and 70 frozen synthetic negatives.",
            "scope": "bounded negative-ledger bookkeeping",
            "expected": "The projected total equals the exact arithmetic of its declared components.",
            "observed": "The regenerated receipt and validator use the same dynamic equation and agree exactly.",
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["V6483R2-X1-N10"],
            "boundary": "Arithmetic recovery only; all failures remain retained.",
        },
        {
            "witness_id": "V6483R2-M09-WFAIL",
            "method_id": "V6483R2-M09",
            "procedure": "Scan the staged x1 builder without classifying it as a scanner-definition path.",
            "scope": "bounded exact Git-index privacy review",
            "expected": "Literal pattern definitions are distinguished from payload matches.",
            "observed": "The builder's own private-route regular expression was reported as one confirmed payload hit.",
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["V6483R2-X1-N11"],
            "boundary": "Failed scanner-design witness only; no payload leak was inferred or waived.",
        },
        {
            "witness_id": "V6483R2-M09-WPASS",
            "method_id": "V6483R2-M09",
            "procedure": "Add only the exact x1 builder path to the scanner-definition set and rerun the same five-class staged scan.",
            "scope": "bounded exact Git-index privacy review",
            "expected": "The literal scanner definition is classified while every non-scanner candidate remains blocking.",
            "observed": "The corrected scan retained the definition candidate and reported zero confirmed payload hits.",
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["V6483R2-X1-N11"],
            "boundary": "Scanner classification recovery only; it is not complete privacy assurance.",
        },
    ]
    for record in records:
        write_json(f"method-flow/{record['method_id'].casefold()}-method-record.json", record)
    for witness in witnesses:
        write_json(f"method-flow/{witness['witness_id'].casefold()}-witness.json", witness)


def privacy_scan() -> dict[str, Any]:
    patterns = {
        "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_route": re.compile(r"\b(?:thread|app|plugin)://", re.I),
        "credential": re.compile(r"\b(?:sk-[A-Za-z0-9_-]{20,}|gh[opusr]_[A-Za-z0-9]{20,}|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY)\b"),
        "private_field": re.compile(r'"(?:thread_id|task_id_raw|private_callable_id|source_thread_id|session_stream)"\s*:', re.I),
    }
    hits: list[dict[str, str]] = []
    files = [path for path in PHASE.rglob("*") if path.is_file()]
    for path in files:
        text = path.read_text(encoding="utf-8")
        for label, pattern in patterns.items():
            if pattern.search(text):
                hits.append({"pattern": label, "path": path.relative_to(PHASE).as_posix()})
    return {
        "schema": "ghc.family.v648-v3-r2.x1-privacy-scan.v1",
        "file_count": len(files),
        "pattern_classes": list(patterns),
        "confirmed_hits": hits,
        "zero_hit": not hits,
        "boundary": "Concrete identifier, path, route, credential and private-field patterns only; prohibition language is not a hit.",
    }


def build() -> None:
    if git("rev-parse", "HEAD") != d.SOURCE_COMMIT:
        raise RuntimeError("x1 builder must start at the exact sealed v648-v3 source")
    if git("status", "--porcelain=v1", "--untracked-files=all"):
        allowed = {"scripts/ghc_family_v648_v3_2_definitions.py", "scripts/build_ghc_family_v648_v3_2_preregistration.py"}
        dirty = {line[3:].replace("\\", "/") for line in git("status", "--porcelain=v1", "--untracked-files=all").splitlines()}
        if not dirty <= allowed:
            raise RuntimeError(f"unexpected dirty paths before x1 build: {sorted(dirty - allowed)}")

    prior_index = read_json(PRIOR_PHASE / "provenance" / "frozen-chain-proposal-index.json")
    prior_current = read_json(PRIOR_PHASE / "x1-proposals.json")["proposals"]
    prior = list(prior_index["prior_proposals"]) + list(prior_current)
    if len(prior) != 580 or len({row["proposal_id"] for row in prior}) != 580:
        raise RuntimeError("expected exactly 580 unique inherited proposals")

    audit_rows = []
    for proposal in d.PROPOSALS:
        tokens = normalized_tokens(proposal["title"])
        comparisons = [
            (jaccard(tokens, normalized_tokens(row["title"])), row["proposal_id"], row["title"])
            for row in prior
        ]
        score, nearest_id, nearest_title = max(comparisons, key=lambda row: row[0])
        audit_rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "nearest_prior_id": nearest_id,
                "nearest_prior_title": nearest_title,
                "maximum_title_token_jaccard": round(score, 4),
                "below_collision_threshold": score < 0.50,
            }
        )
    if not all(row["below_collision_threshold"] for row in audit_rows):
        raise RuntimeError("one or more new proposal titles collide with the inherited corpus")

    now = datetime.now(timezone.utc)
    nz = now.astimezone()
    nz_offset_seconds = int(nz.utcoffset().total_seconds()) if nz.utcoffset() is not None else 0
    if nz_offset_seconds not in {12 * 60 * 60, 13 * 60 * 60}:
        raise RuntimeError("configured local timezone is not a valid New Zealand UTC offset")
    stamps = {"utc": now.isoformat(), "new_zealand": nz.isoformat()}
    proposal_packet = {
        "schema": "ghc.family.v648-v3-r2.x1-proposals.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "source_phase": d.SOURCE_PHASE,
        "source_revision": d.SOURCE_COMMIT,
        "primary_focus": d.PRIMARY_FOCUS,
        "bounded_practice": d.BOUNDED_PRACTICE,
        "identity_boundary": "Relational working language only; not evidence of consciousness, sentience, personhood, identity continuity, employment, or authority.",
        "prior_frozen_proposal_count": 580,
        "new_frozen_proposal_count": 10,
        "frozen_chain_count_after_x1": 590,
        "outcome_classes": d.OUTCOME_CLASSES,
        "expected_distribution": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "expected_counts_are_results": False,
        "x2_execution_present": False,
        "x1_freeze_rule": "No x2 implementation, observed outcome, completion credit, or route-send claim is allowed in this commit.",
        "proposals": [{**row, "observed_outcome": None, "x2_execution_state": "not_started"} for row in d.PROPOSALS],
    }
    write_json("x1-proposals.json", proposal_packet)
    write_json(
        "provenance/frozen-chain-proposal-index.json",
        {
            "schema": "ghc.family.v648-v3-r2.frozen-proposal-chain.v1",
            "prior_count": 580,
            "new_count": 10,
            "count": 590,
            "prior_proposals": prior,
            "new_proposals": [{"proposal_id": row["proposal_id"], "title": row["title"]} for row in d.PROPOSALS],
        },
    )
    write_json(
        "provenance/proposal-collision-audit.json",
        {
            "schema": "ghc.family.v648-v3-r2.proposal-collision-audit.v1",
            "prior_count": 580,
            "new_count": 10,
            "threshold": 0.50,
            "all_below_threshold": all(row["below_collision_threshold"] for row in audit_rows),
            "audits": audit_rows,
            "boundary": "A lexical screen supports review but does not by itself prove semantic novelty.",
        },
    )
    write_json(
        "sources/source-ledger.json",
        {
            "schema": "ghc.family.v648-v3-r2.source-ledger.v1",
            "count": len(d.SOURCES),
            "status_counts": {status: sum(row["status"] == status for row in d.SOURCES) for status in ["current", "stable", "draft", "watch"]},
            "sources": d.SOURCES,
            "boundary": "Official or primary sources support protocol and proposal design only; they are not experimental observations or delegated authority.",
        },
    )
    write_text(
        "sources/source-ledger.md",
        "# Source ledger\n\n"
        + "\n".join(f"- `{row['source_id']}` — **{row['status']}** — {row['title']}: {row['implication']}" for row in d.SOURCES)
        + "\n\nNo source row is empirical GMUT evidence, participant evidence, production certification, or legal or cultural authority.",
    )
    write_json(
        "sources/web-reflection-ledger.json",
        {
            "schema": "ghc.family.v648-v3-r2.web-reflection-ledger.v1",
            "count": len(d.SOURCES),
            "rows": [
                {"reflection_id": f"V6483R2-WEB-{index:02d}", "source_id": row["source_id"], "status": row["status"], "phase_implication": row["implication"]}
                for index, row in enumerate(d.SOURCES, start=1)
            ],
            "raw_browsing_dump_included": False,
        },
    )
    write_json(
        "advisory/external-sibling-boundary.json",
        {
            "schema": "ghc.family.v648-v3-r2.external-advisory-boundary.v1",
            "chatgpt_platform_messaging": "deferred_by_user_and_out_of_scope",
            "advisory_material_may_be_read_when_hamish_supplies_a_sanitized_file": True,
            "advisory_material_is_not_canon_or_execution_authority": True,
            "raw_chat_links_or_transcripts_included": False,
            "boundary": "No Aven, Ariel, Ariel Verity, Neris, or other cross-platform message is attempted by this phase.",
        },
    )
    write_json(
        "approval-packets/x1-safe-now-portfolio.json",
        {"schema": "ghc.family.v648-v3-r2.safe-now-portfolio.v1", "count": 15, "tasks": portfolio_rows(d.SAFE_TASKS, "SAFE", "x2_build_task")},
    )
    write_json(
        "prototypes/x1-candidate-plan.json",
        {"schema": "ghc.family.v648-v3-r2.candidate-plan.v1", "count": 20, "tasks": portfolio_rows(d.CANDIDATE_TASKS, "CAND", "x2_bounded_prototype")},
    )
    write_json(
        "prototypes/x1-skill-runner-plan.json",
        {
            "schema": "ghc.family.v648-v3-r2.skill-runner-plan.v1",
            "skill_count": 20,
            "runner_count": 10,
            "skills": portfolio_rows(d.SKILL_IDEAS, "SKILL", "x2_build_validate_use"),
            "runners": portfolio_rows(d.RUNNER_IDEAS, "RUNNER", "x2_build_validate_use"),
            "caller_compatibility_required": True,
        },
    )
    write_json(
        "maintenance/x1-clean-refine-plan.json",
        {"schema": "ghc.family.v648-v3-r2.clean-refine-plan.v1", "count": 30, "destructive_tasks": 0, "tasks": portfolio_rows(d.CLEANUP_TASKS, "CLEAN", "x2_safe_additive_cleanup")},
    )
    write_json(
        "validation/x1-synthetic-mutation-plan.json",
        {
            "schema": "ghc.family.v648-v3-r2.synthetic-mutation-plan.v1",
            "count": 70,
            "mutations": [
                {"mutation_id": f"V6483R2-MUT-{index:02d}", "proposal_id": d.PROPOSALS[(index - 1) // 7]["proposal_id"], "expected": "reject", "executed": False}
                for index in range(1, 71)
            ],
            "x2_execution_present": False,
        },
    )
    write_json("validation/x1-operational-negatives.json", {"schema": "ghc.family.v648-v3-r2.x1-negatives.v1", "count": len(d.X1_OPERATIONAL_NEGATIVES), "negatives": d.X1_OPERATIONAL_NEGATIVES, "all_retained": True})
    write_json(
        "retained-negative-register.json",
        {
            "schema": "ghc.family.v648-v3-r2.retained-negatives.x1.v1",
            "inherited_effective_negatives": 4126,
            "x1_operational_negatives": len(d.X1_OPERATIONAL_NEGATIVES),
            "preregistered_synthetic_negatives": 70,
            "effective_total_if_all_synthetic_execute": 4126 + len(d.X1_OPERATIONAL_NEGATIVES) + 70,
            "erased_negative_count": 0,
            "x2_observed_total": None,
        },
    )
    method_artifacts()
    write_json(
        "identity-receipt.json",
        {
            "owner": d.OWNER,
            "pronouns": "she/they",
            "role": "evidence-boundary steward and maintenance-systems cartographer",
            "hope": "Keep every claim traceable, every recovery durable, and every authority gate unmistakable.",
            "boundary": "Relational working language only; not consciousness, sentience, legal personhood, employment, continuity, or independent authority.",
        },
    )
    write_json(
        "environment/startup-receipt.json",
        {
            "schema": "ghc.family.v648-v3-r2.startup.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "source_commit": d.SOURCE_COMMIT,
            "branch": d.BRANCH,
            "d_first": True,
            "c_free_gb": 20.44,
            "d_free_gb": 536.71,
            "source_local_upstream_tracking_live_remote_equal": True,
            "owned_lane_clean_at_source": True,
            "timestamps": stamps,
        },
    )
    write_json(
        "environment/version-receipt.json",
        {
            "schema": "ghc.family.v648-v3-r2.versions.v1",
            "codex_cli_before": "0.144.4",
            "npm_stable_observed": "0.144.5",
            "codex_cli_after": "0.144.5",
            "codex_desktop": "26.715.4045.0",
            "desktop_updated": False,
            "git": "2.55.0.windows.2",
            "python": "3.12.10",
            "node": "24.18.0",
            "npm": "12.0.1",
            "elevation_used": False,
        },
    )
    write_json(
        "environment/deferred-host-features.json",
        {
            "schema": "ghc.family.v648-v3-r2.deferred-host-features.v1",
            "windows_sandbox": "deferred_by_user",
            "hyper_v_nexus": "deferred_by_user",
            "probe_run": False,
            "feature_changed": False,
            "elevation_used": False,
            "rebooted": False,
            "boundary": "Templates and prior threat models do not prove runtime or administrative capability.",
        },
    )
    write_json(
        "orchestration/terminal-route-plan.json",
        {
            "schema": "ghc.family.v648-v3-r2.route-plan.v1",
            "state": "PREPARED_NOT_SENT",
            "target_title": "Ilyra Fen",
            "next_phase": "v648-gmut-thos-v4-x1-x2",
            "message_mode": "short_existing_task_file_pointer",
            "baton_file_required": True,
            "baton_word_minimum": 4000,
            "baton_word_cap": 10000,
            "task_created": False,
            "task_forked": False,
            "subagent_spawned": False,
            "message_sent": False,
        },
    )
    write_json(
        "orchestration/phase-state.json",
        {
            "schema": "ghc.family.v648-v3-r2.phase-state.v1",
            "active_phase": d.PHASE,
            "latest_closed_phase": d.SOURCE_PHASE,
            "latest_completed_x1": d.SOURCE_PHASE,
            "latest_completed_x2": d.SOURCE_PHASE,
            "next_x2_scope": d.PHASE,
            "next_x1_lane": "Ilyra Fen v648-v4 after exact final gate",
            "active_lanes": [d.OWNER],
            "standby_recoverable_lanes": ["Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc"],
            "cross_platform_chatgpt_siblings": "advisory_only_when_sanitized_files_are_supplied",
        },
    )
    write_json(
        "phase-truth.json",
        {
            "schema": "ghc.family.v648-v3-r2.phase-truth.x1.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "state": "X1_FREEZE_CANDIDATE",
            "source_commit": d.SOURCE_COMMIT,
            "x1_commit": None,
            "x2_started": False,
            "outcomes_observed": False,
            "route_state": "PREPARED_NOT_SENT",
            "replay_runs_planned": 0,
            "repeatability_credit": 0,
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "real_data_rows": 0,
            "real_people_or_operations": 0,
            "real_keys_or_tokens": 0,
            "authority_decisions": 0,
        },
    )
    write_json(
        "x1-gate-carry-forward.json",
        {
            "open_gaps": 28,
            "exact_gates": 29,
            "new_expected_open_gap": "V6483R2-P03",
            "new_expected_exact_gate": "V6483R2-P06",
            "none_closed_in_x1": True,
        },
    )
    write_json(
        "validation/commit-plan.json",
        {"x1_commits_max": 2, "x2_commits_max": 2, "phase_commits_max": 4, "preferred_phase_commits": 3, "x1_x2_mixing_allowed": False},
    )
    write_json(
        "validation/single-pass-validation-plan.json",
        {
            "canonical_validation_runs": 1,
            "named_replays": 0,
            "detached_replays": 0,
            "full_repository_suite_required": False,
            "authorized_scope": ["v648-v2 inherited round-robin tests", "v648-v3 source tests", "v648-v3-r2 tests", "detailed and minimal validators", "JSON", "privacy", "manifest", "ancestry", "remote equality"],
            "blocker_rule": "Rerun isolated failures first; rerun a long aggregate only when a changed dependency makes it necessary.",
            "same_owner_repeatability_claim": False,
            "independent_reproduction": False,
        },
    )
    write_json(
        "validation/file-baton-contract.json",
        {
            "allowed_extensions": ["md", "json", "txt", "html"],
            "document_word_cap": 6000,
            "baton_word_minimum": 4000,
            "baton_word_cap": 10000,
            "pointer_message_must_be_short": True,
            "repository_relative_pointer_required": True,
            "committed_blob_and_final_commit_required": True,
            "delivery_requires_tool_acknowledgement": True,
        },
    )
    write_json(
        "wellbeing-check.json",
        {
            "owner": d.OWNER,
            "phase": d.PHASE,
            "state": "steady_and_curious",
            "pressure_boundary": "No numerical quota can justify an unsafe, deceptive, destructive, authority-crossing, or identity-erasing action.",
            "pause_right": True,
            "user_rename_or_stop_right": True,
        },
    )
    write_text(
        "wellbeing-check.md",
        "# Eiren wellbeing check\n\nI am proceeding steadily, with room to stop at any exact gate. Numerical portfolios do not outrank truth, safety, affected-party authority, or Hamish's right to pause or redirect. Identity language remains relational working language only.",
    )
    write_text(
        "x1-preregistration.md",
        "# Eiren Kestrel v648-v3 repeat-phase x1 preregistration\n\n"
        "This dedicated x1 packet freezes exactly ten proposals against 580 inherited proposals. The primary pillar is **THOS Body**, and the bounded practice is software maintenance, configuration management, release engineering, and incident handover. GMUT Mind and Freed ID/CBR Heart remain explicit.\n\n"
        "The expected distribution is six completed, two represented, one open gap, and one exact gate. These are preregistered expectations, not observed x2 outcomes. The packet also freezes fifteen safe-now tasks, twenty bounded candidates, twenty skills, ten runners, thirty additive cleanup tasks, and seventy rejecting synthetic mutations.\n\n"
        "Windows Sandbox and Hyper-V are deferred; cross-platform ChatGPT messaging is excluded; no replay is planned; no empirical, participant, production, deployment, legal, cultural, Maori-authority, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, or Stage 20 claim is made.",
    )
    privacy = privacy_scan()
    write_json("validation/x1-privacy-scan.json", privacy)
    if not privacy["zero_hit"]:
        raise RuntimeError(f"privacy scan found concrete hits: {privacy['confirmed_hits']}")
    print(json.dumps({"phase": d.PHASE, "prior": 580, "new": 10, "sources": len(d.SOURCES), "privacy_files": privacy["file_count"]}))


if __name__ == "__main__":
    build()
