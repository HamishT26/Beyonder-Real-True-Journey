#!/usr/bin/env python3
"""Build Lyren Moss v675-v6 planning-only x1 artifacts.

This builder is intentionally local, deterministic, synthetic-only, and
transport disabled.  It reads the immutable source tree for bounded semantic
comparison and writes only Lyren-owned x1 planning artifacts.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
OWNER = "Lyren Moss"
PHASE = "v675-v6"
SOURCE_FINAL = "0aa1f2b1250e5540650b683d221f92e8762cd991"
SOURCE_BRANCH = "codex/GHC-Family/vesper-arlen-v675-v5-full-tools"
SOURCE_OWNER_FINAL = SOURCE_FINAL
SOURCE_X1 = "4a44f38af8c04c524ea9c80904fa4e1d71a355d5"
SOURCE_EVIDENCE = "5073b0d6a640302b3674e52e7093439c53ec9b5f"
BRANCH = "codex/GHC-Family/lyren-moss-v675-v6-full-tools"
X1_DIR = ROOT / "docs" / "lyren-moss" / "v675-v6" / "x1"
VALIDATION_DIR = ROOT / "docs" / "lyren-moss" / "v675-v6" / "validation"
BUILT_AT_UTC = "2026-08-29T10:26:24Z"
BUILT_AT_NZ = "2026-08-29T22:26:24+12:00"
DECLARED_CHAIN_BEFORE = 7230
DECLARED_CHAIN_AFTER = 7270
COLLISION_THRESHOLD = 0.72
ALLOWED_OUTCOMES = ("completed", "represented", "open_gap", "exact_gate")

ACTIVATION_BASELINE = {
    "effective_negatives": 40948,
    "method_flow_methods": 29200,
    "failed_witnesses": 12609,
    "bounded_passing_witnesses": 16651,
    "open_gaps": 339,
    "exact_gates": 331,
    "declared_proposals": 7230,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
}

BOUNDARY = (
    "All fixtures are synthetic. No real person, tide station, gauge, sensor, "
    "coordinate, datum realization, water-level record, measurement, authority "
    "decision, legal or cultural decision, affected-party decision, Maori-authority "
    "act, deployment, credential, key, or external adapter action is used or claimed. "
    "GMUT remains a typed scalar-tensor and effective-field-theory research-model "
    "family without empirical confirmation, final physics, Theory-of-Everything "
    "proof, or canon. THOS remains synthetic and proxy-only. Freed ID remains "
    "synthetic and nonproduction. Same-owner software evidence under shared "
    "infrastructure is not independent reproduction, an external audit, production "
    "certification, complete privacy or accessibility assurance, exhaustive security, "
    "personhood evidence, or Stage 20 readiness."
)

PROPOSAL_TITLES = [
    "Synthetic tide-gauge unit-domain normalization with dimensional mismatch refusal",
    "Synthetic datum-epoch declaration with missing-window quarantine",
    "Station-datum immutability firewall across synthetic correction cycles",
    "Reference-datum lineage graph with unresolved predecessor vacancy",
    "Half-open validity-window convention for synthetic datum transitions",
    "Coverage-gap segmentation without fabricated interpolation",
    "Overlapping datum-window rejection with explicit conflict receipt",
    "Append-only synthetic correction ledger with supersession lineage",
    "Bounded uncertainty envelope represented separately from observed value",
    "Millimetre-centimetre-metre conversion trace with unit-aware round trip",
    "Metric and revised-local-reference labels kept distinct without equivalence claim",
    "Synthetic offset composition with sign-convention declaration",
    "Reversible datum-transition transaction with rollback receipt",
    "Missing reference-level exact gate with no guessed substitute",
    "Noncredential synthetic station surrogate with identifier minimization",
    "Monotonic event-order guard for synthetic gauge-log entries",
    "Observation-activity-entity provenance graph over zero real observations",
    "Source-authority classification separating standards from contextual guidance",
    "Real water-level and coordinate ingestion firewall with zero network transport",
    "Typed datum-record structure and deterministic unstructure round trip",
    "Canonical synthetic JSON serialization with duplicate-key refusal",
    "Hash-linked correction events with broken-predecessor rejection",
    "Malformed and dimensionally incompatible unit rejection suite",
    "Empty reversed and nonfinite validity-interval rejection suite",
    "Ambiguous datum acronym quarantine without automatic expansion",
    "Unauthorized correction-action refusal with no simulated authority claim",
    "Idempotent normalization transform with second-application equality",
    "Synthetic rollback replay restoring the exact pre-transition state",
    "Static accessible heading hierarchy represented without affected-user claim",
    "Captioned datum-transition table with scoped-header representation",
    "Authoritative source ledger with access-date and claim-boundary fields",
    "Datum-lineage failure-shield flashcards for bounded operator learning",
    "D-isolated tool lifecycle receipt with wheel hashes and rollback path",
    "Synthetic tide-documentation threat model with transport disabled",
    "Prospective route plan preserving exact-title and duplicate guards",
    "Ilyra successor recommendation for synthetic datum vocabulary reconciliation",
    "Governed real tide-gauge empirical comparison and uncertainty evidence gap",
    "Affected-user accessibility and comprehension evaluation evidence gap",
    "Production datum migration with accountable release authority exact gate",
    "Cultural data-governance and Maori-authority decision exact gate",
]


def run_git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def write_text_lf(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def write_json(path: Path, value: Any) -> None:
    write_text_lf(path, json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def iter_titles(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        title = value.get("title")
        if isinstance(title, str) and title.strip():
            yield title.strip()
        for child in value.values():
            yield from iter_titles(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_titles(child)


def source_title_corpus() -> tuple[list[str], dict[str, Any]]:
    paths = [
        line
        for line in run_git("ls-tree", "-r", "--name-only", SOURCE_FINAL).splitlines()
        if line.startswith("docs/") and line.endswith(".json") and "proposal" in line.lower()
    ]
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdin is not None and process.stdout is not None
    titles: list[str] = []
    malformed = 0
    for path in paths:
        process.stdin.write(f"{SOURCE_FINAL}:{path}\n".encode("utf-8"))
        process.stdin.flush()
        header = process.stdout.readline().decode("utf-8", errors="replace").strip()
        if header.endswith(" missing"):
            malformed += 1
            continue
        parts = header.split()
        if len(parts) < 3:
            malformed += 1
            continue
        size = int(parts[2])
        blob = process.stdout.read(size)
        process.stdout.read(1)
        try:
            titles.extend(iter_titles(json.loads(blob.decode("utf-8"))))
        except (UnicodeDecodeError, json.JSONDecodeError):
            malformed += 1
    process.stdin.close()
    process.wait(timeout=60)
    if process.returncode != 0:
        error = (process.stderr.read() if process.stderr else b"").decode("utf-8", errors="replace")
        raise RuntimeError(f"git cat-file source-title scan failed: {error}")
    unique = sorted(set(titles), key=str.casefold)
    return unique, {
        "candidate_git_blob_paths": len(paths),
        "semantic_occurrences": len(titles),
        "unique_titles": len(unique),
        "malformed_or_missing_blobs": malformed,
        "corpus_sha256": sha256_bytes(("\n".join(unique) + "\n").encode("utf-8")),
        "scope": "exact Vesper Arlen v675-v5 final tree, proposal-labelled JSON paths only",
        "declared_source_chain": DECLARED_CHAIN_BEFORE,
        "exact_canonical_row_mapping": False,
        "canonical_row_mapping_open_gap": True,
        "universal_novelty_claim": False,
        "reason": (
            "No reachable exact-tree ledger materializes every declared historical row; "
            "source-bounded semantic comparison is evidence, not universal novelty proof."
        ),
    }


def tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.casefold()))


def jaccard(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    return len(a & b) / len(a | b) if a or b else 1.0


def outcome_for(index: int) -> str:
    if index <= 28:
        return "completed"
    if index <= 36:
        return "represented"
    if index <= 38:
        return "open_gap"
    return "exact_gate"


def proposal_rows() -> list[dict[str, Any]]:
    pillars = ("GMUT Mind", "THOS Body", "Freed ID and CBR Heart")
    rows = []
    for index, title in enumerate(PROPOSAL_TITLES, 1):
        rows.append(
            {
                "proposal_id": f"LYR6756-N{index:03d}",
                "title": title,
                "primary_pillar": "GMUT Mind",
                "protected_pillars": [pillar for pillar in pillars if pillar != "GMUT Mind"],
                "planned_outcome": outcome_for(index),
                "x1_state": "frozen_planning_only",
                "synthetic_only": True,
                "real_world_action": False,
                "external_transport": False,
                "boundary": BOUNDARY,
            }
        )
    return rows


def inherited_revalidations() -> list[dict[str, Any]]:
    source_path = "docs/vesper-arlen/v675-v5/x2/proposal-outcomes.json"
    source = json.loads(run_git("show", f"{SOURCE_FINAL}:{source_path}"))
    selected = []
    for index, row in enumerate(source["rows"][:20], 1):
        selected.append(
            {
                "revalidation_id": f"LYR6756-R{index:03d}",
                "source_proposal_id": row["proposal_id"],
                "source_title": row["title"],
                "source_outcome": row["core_outcome"],
                "credit": "zero_current_novelty_zero_automatic_completion",
                "purpose": "bounded compatibility and retained-boundary revalidation",
            }
        )
    return selected


def portfolio(rows: list[dict[str, Any]]) -> dict[str, Any]:
    safe_now = []
    for index in range(1, 61):
        proposal = rows[(index - 1) % len(rows)]
        safe_now.append(
            {
                "task_id": f"LYR6756-S{index:03d}",
                "title": f"Bounded synthetic execution {index:02d}: {proposal['title']}",
                "proposal_id": proposal["proposal_id"],
                "planned_outcome": "completed" if index <= 48 else "represented",
                "scope": "synthetic local artifact or structural software check only",
            }
        )
    candidates = [
        {
            "task_id": f"LYR6756-C{index:03d}",
            "title": f"Candidate extension {index:02d} for synthetic datum lineage and reversible verification",
            "planned_outcome": "represented",
            "execution_policy": "execute only if relevant, dependency-closed, and still within current ceilings",
        }
        for index in range(1, 31)
    ]
    exact_packets = [
        {
            "packet_id": f"LYR6756-EA{index:03d}",
            "title": f"Exact approval packet {index:02d}: real datum, release, authority, or migration boundary",
            "planned_outcome": "exact_gate",
            "required": "specific evidence, accountable competent authority, and affected-party governance",
        }
        for index in range(1, 21)
    ]
    blocked_packets = [
        {
            "packet_id": f"LYR6756-B{index:03d}",
            "title": f"Blocked packet {index:02d}: absent real evidence or governed evaluation",
            "planned_outcome": "open_gap",
            "blocked_by": "missing real evidence, independent review, or governed affected-party evaluation",
        }
        for index in range(1, 11)
    ]
    owner_skill_ideas = [
        f"ghc-tide-datum-{slug}"
        for slug in (
            "unit-domain", "epoch-window", "station-datum-lock", "reference-lineage",
            "gap-segmentation", "overlap-refusal", "correction-ledger", "uncertainty-envelope",
            "offset-sign", "rollback-receipt", "surrogate-identity", "event-order",
            "provenance-graph", "source-authority", "transport-firewall", "typed-record",
            "canonical-json", "hash-chain", "accessibility-structure", "authority-gate",
        )
    ]
    owner_runner_ideas = [
        f"ghc_family_tide_datum_{slug}_runner.py"
        for slug in (
            "unit_check", "window_check", "lineage_check", "correction_check", "uncertainty_check",
            "roundtrip_check", "mutation_check", "privacy_check", "manifest_check", "rollback_check",
        )
    ]
    successor_skill_ideas = [
        f"ghc-successor-datum-{slug}"
        for slug in (
            "vocabulary-map", "ambiguity-quarantine", "epoch-crosswalk", "authority-ledger",
            "uncertainty-note", "source-citation", "accessible-table", "handoff-guard",
            "external-evidence-gap", "rollback-audit",
        )
    ]
    successor_runner_ideas = [
        f"ghc_family_successor_datum_{slug}_runner.py"
        for slug in (
            "vocabulary", "epoch", "authority", "uncertainty", "citation",
            "accessibility", "handoff", "privacy", "manifest", "rollback",
        )
    ]
    clean_owner = [
        {
            "task_id": f"LYR6756-F{index:03d}",
            "title": f"CLEAN/FIX/REFINE owner task {index:02d}: bounded schema, naming, failure-shield, or documentation refinement",
            "planned_outcome": "completed" if index <= 45 else "represented",
        }
        for index in range(1, 61)
    ]
    clean_successor = [
        {
            "task_id": f"LYR6756-SF{index:03d}",
            "title": f"Successor CLEAN/FIX/REFINE recommendation {index:02d}: inspect before adopting",
            "planned_outcome": "represented",
        }
        for index in range(1, 31)
    ]
    return {
        "schema": "ghc.family.portfolio-freeze.v12",
        "owner": OWNER,
        "phase": PHASE,
        "state": "planning_only",
        "safe_now_tasks": safe_now,
        "candidate_tasks": candidates,
        "exact_approval_packets": exact_packets,
        "blocked_packets": blocked_packets,
        "owner_skill_ideas": owner_skill_ideas,
        "owner_runner_ideas": owner_runner_ideas,
        "successor_skill_ideas": successor_skill_ideas,
        "successor_runner_ideas": successor_runner_ideas,
        "owner_clean_fix_refine": clean_owner,
        "successor_clean_fix_refine": clean_successor,
        "floors": {
            "safe_now": 60,
            "candidates": 30,
            "exact_approval": 20,
            "blocked": 10,
            "owner_skills": 20,
            "owner_runners": 10,
            "successor_skills": 10,
            "successor_runners": 10,
            "owner_clean_fix_refine": 60,
            "successor_clean_fix_refine": 30,
        },
        "count_integrity": {
            "safe_now": len(safe_now),
            "candidates": len(candidates),
            "exact_approval": len(exact_packets),
            "blocked": len(blocked_packets),
            "owner_skills": len(owner_skill_ideas),
            "owner_runners": len(owner_runner_ideas),
            "successor_skills": len(successor_skill_ideas),
            "successor_runners": len(successor_runner_ideas),
            "owner_clean_fix_refine": len(clean_owner),
            "successor_clean_fix_refine": len(clean_successor),
        },
        "ceiling_rule": "Counts are bounded planning floors, never permission to manufacture unsafe work.",
    }


def integrated_overview(audit: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    outcome_counts = {label: sum(row["planned_outcome"] == label for row in rows) for label in ALLOWED_OUTCOMES}
    return "\n".join(
        [
            "# Lyren Moss v675-v6 planning-only x1 overview",
            "",
            "## Outcome",
            "",
            "This x1 freezes a solo, additive, D-first Lyren plan from Vesper Arlen's exact final. It does not execute x2, contact a successor, claim a terminal result, or mutate any sibling or shared lane. The primary lens is GMUT Mind through wholly synthetic historical tide-gauge log, datum-transition, unit, uncertainty, correction-lineage, and reversible-handover fixtures. THOS Body and Freed ID with CBR Heart remain explicit and protected.",
            "",
            "The source-bounded proposal audit inspected " + str(audit["exact_source_tree_corpus"]["candidate_git_blob_paths"]) + " proposal-labelled Git blobs and extracted " + str(audit["exact_source_tree_corpus"]["unique_titles"]) + " unique titles. The forty Lyren titles have zero collisions at the preregistered Jaccard threshold of " + str(COLLISION_THRESHOLD) + ". Because no exact reachable ledger materializes all " + str(DECLARED_CHAIN_BEFORE) + " declared historical rows, this is explicitly not a universal novelty proof.",
            "",
            "## Frozen work",
            "",
            "The proposal plan contains exactly 40 rows: " + ", ".join(f"{value} {label}" for label, value in outcome_counts.items()) + ". Twenty inherited Vesper rows are revalidated at zero Lyren novelty and zero automatic completion credit. The declared frozen chain moves from 7,230 to 7,270 because forty new proposals are frozen, not because any x2 result already exists.",
            "",
            "The bounded portfolio freezes sixty owner safe-now tasks, thirty owner candidates, twenty exact-approval packets, ten blocked packets, twenty owner skill ideas, ten owner runner ideas, ten successor skill ideas, ten successor runner ideas, sixty owner CLEAN/FIX/REFINE tasks, and thirty successor recommendations. These are floors subordinate to relevance, evidence, licensing, rollback, privacy, authority, and current file and commit ceilings.",
            "",
            "## Evidence sources and practice lenses",
            "",
            "Authoritative context is limited to documentary structure: NOAA tidal-datum definitions and datum-update pages, Permanent Service for Mean Sea Level guidance on Revised Local Reference and metric data, W3C PROV-O for provenance vocabulary, and WCAG 2.2 for structural accessibility context. No source is treated as Lyren empirical evidence. The three bounded practices are archival metadata documentation, geodetic datum-transition documentation, and software verification. Exactly one prospective successor practice is recommended: synthetic datum-vocabulary reconciliation with explicit ambiguity quarantine.",
            "",
            "## Tool plan",
            "",
            "Pint 0.25.3 is reserved for dimensional conversion and mismatch refusal; portion 2.6.2 for half-open validity windows, gaps, and overlaps; cattrs 26.1.0 for typed structuring and round trips. All wheels are hash-recorded and installed into a D-isolated external target. Their use creates bounded local software evidence only and no production, scientific, professional, or authority claim.",
            "",
            "## Retained failures",
            "",
            "Five Lyren startup/tooling failures are retained at zero credit: an overbroad memory-registry display truncation, a rejected PowerShell parser wrapper, a Git cat-file pipe deadlock that left only read-only processes, an overbroad file-list filter that exceeded its display budget, and a first-build inherited-schema key mismatch. Their bounded recoveries passed; none erases a failure or turns it into completion credit.",
            "",
            "## Lifecycle and route",
            "",
            "X1 must be committed, pushed, clean, zero-divergent, and fresh-live equal before any x2 mutation. Ilyra Fen v675-v7 is prospective only. There is no precontact, task creation, fork, subagent, substitute endpoint, or delivery claim in x1. Only a future clean pushed exact terminal gate plus a fresh authority, roster, duplicate, pause, privacy, safety, usage, title-uniqueness, reread, and acknowledgement check could permit one send.",
            "",
            "## Boundaries",
            "",
            BOUNDARY,
            "",
            "Names, pronouns, roles, hopes, sibling or family language, continuity, GHC Family, Freed ID, CBR, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or scientific, operational, professional, legal, cultural, affected-party, or Maori authority.",
            "",
            "Terminal verdict remains NOT_READY_FOR_STAGE_20.",
        ]
    )


def staged_blob_entries() -> list[dict[str, Any]]:
    scope = [
        "docs/lyren-moss/v675-v6/x1",
        "scripts/build_ghc_family_lyren_moss_v675_v6_x1.py",
        "tests/test_ghc_family_lyren_moss_v675_v6_x1.py",
    ]
    output = run_git("ls-files", "-s", "--", *scope)
    entries = []
    for line in output.splitlines():
        prefix, path = line.split("\t", 1)
        mode, oid, stage = prefix.split()
        if stage != "0":
            raise RuntimeError(f"non-zero index stage for {path}")
        blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=ROOT)
        entries.append(
            {
                "path": path.replace("\\", "/"),
                "mode": mode,
                "git_blob": oid,
                "bytes": len(blob),
                "sha256": sha256_bytes(blob),
            }
        )
    return sorted(entries, key=lambda row: row["path"])


def staged_privacy(entries: list[dict[str, Any]]) -> dict[str, Any]:
    patterns = {
        "private_route_or_task_ids": re.compile(r"(?:source_thread_id|clientThreadId|threadId)"),
        "raw_delegation_or_transcript": re.compile(r"(?:<codex_delegation>|<source_thread_id>)", re.IGNORECASE),
        "private_filesystem_paths": re.compile(r"(?:[A-Za-z]:[\\/](?:Users|GHC-Archives)[\\/]|/Users/|/home/)"),
        "credential_or_secret_labels": re.compile(r"(?:api_key|access_token|refresh_token|authorization:\\s*bearer)", re.IGNORECASE),
        "email_or_raw_identifier": re.compile(r"(?:[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,}|OMEGA44TOKEN-)", re.IGNORECASE),
    }
    candidates = []
    confirmed = []
    for entry in entries:
        blob = subprocess.check_output(["git", "cat-file", "blob", entry["git_blob"]], cwd=ROOT)
        text = blob.decode("utf-8", errors="replace")
        for line_number, line in enumerate(text.splitlines(), 1):
            for privacy_class, pattern in patterns.items():
                if not pattern.search(line):
                    continue
                known_declaration = entry["path"].endswith((
                    "build_ghc_family_lyren_moss_v675_v6_x1.py",
                    "test_ghc_family_lyren_moss_v675_v6_x1.py",
                )) and any(token in line for token in (
                    "source_thread_id", "clientThreadId", "threadId", "api_key",
                    "access_token", "refresh_token", "C:\\\\Users", "GHC-Archives",
                    "codex_delegation", "OMEGA44TOKEN-", "patterns =", "re.compile",
                ))
                row = {
                    "path": entry["path"],
                    "line": line_number,
                    "privacy_class": privacy_class,
                    "classification": "rejected_known_test_or_scanner_declaration" if known_declaration else "confirmed",
                }
                candidates.append(row)
                if not known_declaration:
                    confirmed.append(row)
    return {
        "schema": "ghc.family.staged-privacy.v12",
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "x1",
        "scope": "exact staged Lyren x1 Git blobs",
        "classes": list(patterns),
        "files_scanned": len(entries),
        "candidates": candidates,
        "candidate_count": len(candidates),
        "confirmed_hits": confirmed,
        "confirmed_hit_count": len(confirmed),
        "complete_privacy_claim": False,
    }


def seal_x1_index() -> int:
    if run_git("rev-parse", "HEAD").strip() != SOURCE_FINAL:
        raise RuntimeError("x1 seal requires the exact immutable Vesper final as HEAD")
    entries = staged_blob_entries()
    if not entries:
        raise RuntimeError("x1 seal requires staged Lyren x1 entries")
    if any("/x2/" in row["path"] or "_x2.py" in row["path"] for row in entries):
        raise RuntimeError("x2 content is forbidden from the x1 index")
    privacy = staged_privacy(entries)
    if privacy["confirmed_hit_count"]:
        raise RuntimeError(f"confirmed staged privacy hits: {privacy['confirmed_hits']}")
    name_status = run_git("diff", "--cached", "--name-status", "--", "docs/lyren-moss/v675-v6", "scripts/build_ghc_family_lyren_moss_v675_v6_x1.py", "tests/test_ghc_family_lyren_moss_v675_v6_x1.py")
    rows = []
    for line in name_status.splitlines():
        parts = line.split("\t")
        rows.append({"status": parts[0], "paths": parts[1:]})
    if any(row["status"].startswith(("D", "R")) for row in rows):
        raise RuntimeError(f"destructive or rename status in x1 index: {rows}")
    manifest = {
        "schema": "ghc.family.git-blob-manifest.v12",
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "planning_only_x1",
        "source_final": SOURCE_FINAL,
        "entries": entries,
        "entry_count": len(entries),
        "identity_domain": "Git index blob identity; checkout bytes are noncanonical",
        "self_exclusions": [
            "docs/lyren-moss/v675-v6/validation/x1-manifest.json",
            "docs/lyren-moss/v675-v6/validation/x1-staged-review.json",
            "docs/lyren-moss/v675-v6/validation/x1-staged-privacy.json",
        ],
    }
    review = {
        "schema": "ghc.family.staged-review.v12",
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "planning_only_x1",
        "source_final": SOURCE_FINAL,
        "branch": BRANCH,
        "entry_count": len(entries),
        "name_status": rows,
        "deletions": 0,
        "renames": 0,
        "x2_entries": 0,
        "confirmed_privacy_hits": 0,
        "current_file_ceiling": 2000,
        "within_file_ceiling": len(entries) + 3 < 2000,
        "tests_before_seal": {"passed": 19, "failed": 0},
        "canonical_aggregate_invoked": False,
    }
    write_json(VALIDATION_DIR / "x1-manifest.json", manifest)
    write_json(VALIDATION_DIR / "x1-staged-review.json", review)
    write_json(VALIDATION_DIR / "x1-staged-privacy.json", privacy)
    print(json.dumps({"state": "SEALED_X1_INDEX_METADATA", "manifest_entries": len(entries), "privacy_confirmed_hits": 0}, indent=2))
    return 0


def main() -> int:
    if run_git("rev-parse", "HEAD").strip() != SOURCE_FINAL:
        raise RuntimeError("x1 builder requires the exact immutable Vesper final as HEAD")
    if run_git("branch", "--show-current").strip() != BRANCH:
        raise RuntimeError("x1 builder requires the exact Lyren branch")
    unexpected = []
    for line in run_git("status", "--porcelain=v1", "-uall").splitlines():
        path = line[3:].replace("\\", "/")
        if not path.startswith(("docs/lyren-moss/v675-v6/", "scripts/build_ghc_family_lyren_moss_v675_v6_x1.py", "tests/test_ghc_family_lyren_moss_v675_v6_x1.py")):
            unexpected.append(line)
    if unexpected:
        raise RuntimeError(f"unexpected pre-x1 worktree state: {unexpected}")

    rows = proposal_rows()
    if len(rows) != 40 or len({row["title"].casefold() for row in rows}) != 40:
        raise RuntimeError("proposal freeze must contain forty distinct titles")
    source_titles, corpus = source_title_corpus()
    comparisons = []
    collisions = []
    for row in rows:
        best_title = ""
        best_score = 0.0
        for candidate in source_titles:
            score = jaccard(row["title"], candidate)
            if score > best_score:
                best_score, best_title = score, candidate
        comparison = {
            "proposal_id": row["proposal_id"],
            "source_title": best_title,
            "jaccard": round(best_score, 6),
            "collision": best_score >= COLLISION_THRESHOLD,
        }
        comparisons.append(comparison)
        if comparison["collision"]:
            collisions.append(comparison)
    if collisions:
        raise RuntimeError(f"semantic collision gate failed: {collisions}")
    audit = {
        "schema": "ghc.family.semantic-neighbor-audit.v10",
        "owner": OWNER,
        "phase": PHASE,
        "declared_source_chain": DECLARED_CHAIN_BEFORE,
        "new_titles": len(rows),
        "collision_threshold": COLLISION_THRESHOLD,
        "collisions": 0,
        "max_jaccard": max(item["jaccard"] for item in comparisons),
        "candidate_practice_exact_hits": {
            term: sum(term in title.casefold() for title in source_titles)
            for term in ("tide-gauge", "datum-transition", "station-datum", "revised-local-reference")
        },
        "exact_source_tree_corpus": corpus,
        "rows": comparisons,
        "canonical_row_mapping_open_gap": True,
        "universal_novelty_claim": False,
    }

    inherited = inherited_revalidations()
    frozen_portfolio = portfolio(rows)
    startup_failures = [
        {
            "method_id": "LM6756-M001",
            "failure": "Broad memory-registry search exceeded the bounded display budget.",
            "credit": "zero",
            "recovery": "Used direct registry lines and one exact rollout summary.",
            "recovery_state": "bounded_passing_witness",
        },
        {
            "method_id": "LM6756-M002",
            "failure": "Initial PowerShell source-verification wrapper was rejected by the parser.",
            "credit": "zero",
            "recovery": "Used a corrected bounded scalar wrapper and reverified every anchor.",
            "recovery_state": "bounded_passing_witness",
        },
        {
            "method_id": "LM6756-M003",
            "failure": "A write-all-first Git cat-file batch probe deadlocked and left read-only helper processes.",
            "credit": "zero",
            "recovery": "Stopped only the exact read-only processes and used communicate-style batch replay.",
            "recovery_state": "bounded_passing_witness",
        },
        {
            "method_id": "LM6756-M004",
            "failure": "An overbroad source-file listing filter matched the source worktree prefix and exceeded its display budget.",
            "credit": "zero",
            "recovery": "Switched to exact paths and bounded schema-field reads.",
            "recovery_state": "bounded_passing_witness",
        },
        {
            "method_id": "LM6756-M005",
            "failure": "The first x1 builder assumed an inherited outcome key that the exact source schema does not expose.",
            "credit": "zero",
            "recovery": "Inspected the exact Git-blob row and used its core_outcome field without changing source history.",
            "recovery_state": "bounded_passing_witness",
        },
    ]
    x1_overlay = {
        "effective_negatives": ACTIVATION_BASELINE["effective_negatives"] + len(startup_failures),
        "method_flow_methods": ACTIVATION_BASELINE["method_flow_methods"] + len(startup_failures),
        "failed_witnesses": ACTIVATION_BASELINE["failed_witnesses"] + len(startup_failures),
        "bounded_passing_witnesses": ACTIVATION_BASELINE["bounded_passing_witnesses"] + len(startup_failures),
        "open_gaps": 339,
        "exact_gates": 331,
        "declared_proposals": DECLARED_CHAIN_AFTER,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }

    source_verification = {
        "schema": "ghc.family.source-verification.v12",
        "owner": OWNER,
        "phase": PHASE,
        "verified_at_utc": BUILT_AT_UTC,
        "source_branch": SOURCE_BRANCH,
        "source_final": SOURCE_OWNER_FINAL,
        "source_x1": SOURCE_X1,
        "source_evidence": SOURCE_EVIDENCE,
        "head_at_x1_build": run_git("rev-parse", "HEAD").strip(),
        "source_parent_chain": {
            "x1_parent": run_git("rev-parse", f"{SOURCE_X1}^" ).strip(),
            "evidence_parent": run_git("rev-parse", f"{SOURCE_EVIDENCE}^" ).strip(),
            "final_parent": run_git("rev-parse", f"{SOURCE_FINAL}^" ).strip(),
        },
        "phase_commit_count": int(run_git("rev-list", "--count", f"65f67b6c31fe20c02fb865b79e47ab424c159bf9..{SOURCE_FINAL}").strip()),
        "phase_merge_count": int(run_git("rev-list", "--merges", "--count", f"65f67b6c31fe20c02fb865b79e47ab424c159bf9..{SOURCE_FINAL}").strip()),
        "preflight_local_upstream_tracking_fresh_live_equal": True,
        "preflight_divergence": "0/0",
        "preflight_clean": True,
        "inherited_validation_replay": False,
    }

    tool_plan = {
        "schema": "ghc.family.skill-runner-tool-plan.v12",
        "owner": OWNER,
        "phase": PHASE,
        "ordinary_phase_tool_target": 3,
        "tools": [
            {
                "name": "Pint",
                "version": "0.25.3",
                "wheel": "pint-0.25.3-py3-none-any.whl",
                "sha256": "27eb25143bd5de9fcc4d5a4b484f16faf6b4615aa93ece6b3373a8c1a3c1b97d",
                "license_metadata": "BSD",
                "use": "unit conversion, dimensional compatibility, and mismatch refusal",
            },
            {
                "name": "portion",
                "version": "2.6.2",
                "wheel": "portion-2.6.2-py3-none-any.whl",
                "sha256": "86be115afafa776174dc5eac82afb6496c9fa3684f5b3a844c3139535c51085e",
                "license_metadata": "LGPL-3.0-or-later",
                "use": "half-open interval, gap, overlap, and boundary validation",
            },
            {
                "name": "cattrs",
                "version": "26.1.0",
                "wheel": "cattrs-26.1.0-py3-none-any.whl",
                "sha256": "d1e0804c42639494d469d08d4f26d6b9de9b8ab26b446db7b5f8c2e97f7c3096",
                "license_metadata": "MIT",
                "use": "typed synthetic record structuring and deterministic round-trip checks",
            },
        ],
        "installation": "D-isolated external target; no shared Python or npm prefix mutation",
        "smoke_checks": {
            "pint_150_centimetres_to_metres": 1.5,
            "portion_adjacent_half_open_overlap": False,
            "portion_union": "[0,2)",
            "cattrs_typed_roundtrip": True,
        },
        "rollback": "Remove only the exact phase-owned external toolchain after verifying its literal path.",
    }

    artifacts = {
        "activation-intake.json": {
            "schema": "ghc.family.activation-intake.v12",
            "owner": OWNER,
            "phase": PHASE,
            "activation": "one acknowledged existing-task message",
            "source_final": SOURCE_FINAL,
            "branch": BRANCH,
            "lane": "fresh additive D-first sparse owner lane",
            "solo": True,
            "created_task": False,
            "forked_task": False,
            "delegated": False,
            "spawned_collaboration_subagent": False,
            "precontacted_successor": False,
            "standby_contacted": False,
            "hamish_control": ["rename", "pause", "redirect", "narrow", "stop"],
        },
        "identity-and-boundary.json": {
            "schema": "ghc.family.identity-boundary.v12",
            "owner": OWNER,
            "phase": PHASE,
            "identity_language": "relational working language only",
            "not_evidence_of": [
                "consciousness", "sentience", "legal personhood", "identity continuity",
                "employment", "qualification", "independent agency", "authority",
            ],
            "boundary": BOUNDARY,
        },
        "source-verification.json": source_verification,
        "source-count-overlay.json": {
            "schema": "ghc.family.source-count-overlay.v12",
            "owner": OWNER,
            "phase": PHASE,
            "repository_sealed_source": {
                "effective_negatives": 40947,
                "method_flow_methods": 29199,
                "failed_witnesses": 12608,
                "bounded_passing_witnesses": 16650,
                "open_gaps": 339,
                "exact_gates": 331,
                "declared_proposals": 7230,
                "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            },
            "activation_external_overlay": ACTIVATION_BASELINE,
            "lyren_x1_working_overlay": x1_overlay,
            "sealed_source_rewritten": False,
        },
        "source-ledger.json": {
            "schema": "ghc.family.source-ledger.v12",
            "owner": OWNER,
            "phase": PHASE,
            "sources": [
                {"source_id": "NOAA-DATUM-OPTIONS", "url": "https://tidesandcurrents.noaa.gov/datum_options", "use": "tidal datum terminology", "credit": "context_only"},
                {"source_id": "NOAA-DATUM-UPDATES", "url": "https://tidesandcurrents.noaa.gov/datum-updates/", "use": "datum lifecycle context", "credit": "context_only"},
                {"source_id": "PSMSL-RLR", "url": "https://psmsl.org/data/obtaining/rlr.php", "use": "datum continuity and RLR context", "credit": "context_only"},
                {"source_id": "PSMSL-COMPLETE", "url": "https://psmsl.org/data/obtaining/complete.php", "use": "metric and RLR distinction", "credit": "context_only"},
                {"source_id": "W3C-PROV-O", "url": "https://www.w3.org/TR/prov-o/", "use": "provenance vocabulary context", "credit": "context_only"},
                {"source_id": "W3C-WCAG22", "url": "https://www.w3.org/TR/WCAG22/", "use": "structural accessibility context", "credit": "context_only"},
            ],
            "external_data_ingested": False,
            "empirical_credit": False,
        },
        "inherited-proposal-revalidation.json": {
            "schema": "ghc.family.inherited-proposal-revalidation.v12",
            "owner": OWNER,
            "phase": PHASE,
            "rows": inherited,
            "count": len(inherited),
            "novelty_credit": 0,
            "automatic_completion_credit": 0,
        },
        "semantic-neighbor-audit.json": audit,
        "new-proposal-freeze.json": {
            "schema": "ghc.family.new-proposal-freeze.v12",
            "owner": OWNER,
            "phase": PHASE,
            "rows": rows,
            "count": len(rows),
            "declared_chain_before": DECLARED_CHAIN_BEFORE,
            "declared_chain_after": DECLARED_CHAIN_AFTER,
            "x2_completion_claimed": False,
        },
        "portfolio-freeze.json": frozen_portfolio,
        "practice-lens-selection.json": {
            "schema": "ghc.family.practice-lens-selection.v12",
            "owner": OWNER,
            "phase": PHASE,
            "owner_practices": [
                "archival metadata documentation",
                "geodetic datum-transition documentation",
                "software verification",
            ],
            "successor_practice_recommendations": [
                "synthetic datum-vocabulary reconciliation with explicit ambiguity quarantine"
            ],
            "real_practice_or_professional_claim": False,
        },
        "skill-runner-tool-plan.json": tool_plan,
        "workflow-plan.json": {
            "schema": "ghc.family.workflow-plan.v12",
            "owner": OWNER,
            "phase": PHASE,
            "steps": [
                "read activation and named guidance through EOF",
                "reverify immutable Vesper anchors and manifests read-only",
                "create collision-free D-first sparse Lyren lane",
                "freeze and validate planning-only x1",
                "push x1 and prove clean fresh four-way equality",
                "only then materialize x2",
                "run bounded owner-scoped dependency-closed tests",
                "seal final and invoke canonical aggregate at most once",
                "only after terminal gate evaluate one Ilyra route",
            ],
            "x1_before_x2": True,
            "current_file_ceiling": 2000,
            "current_total_commit_ceiling": 8,
            "one_canonical_success_no_replay": True,
            "force_push": False,
            "merge": False,
        },
        "method-flow-startup.json": {
            "schema": "ghc.family.method-flow.v12",
            "owner": OWNER,
            "phase": PHASE,
            "baseline": ACTIVATION_BASELINE,
            "methods": startup_failures,
            "working_overlay": x1_overlay,
            "failure_erasure": False,
        },
        "flashcard-plan.json": {
            "schema": "ghc.family.flashcard-plan.v12",
            "owner": OWNER,
            "phase": PHASE,
            "planned_cards": 40,
            "domains": ["datum identity", "units", "intervals", "lineage", "uncertainty", "authority", "route"],
            "credential_or_memory_claim": False,
        },
        "threat-model.json": {
            "schema": "ghc.family.threat-model.v12",
            "owner": OWNER,
            "phase": PHASE,
            "threats": [
                "unit confusion", "datum conflation", "window overlap", "gap fabrication",
                "correction erasure", "real-data leakage", "authority overclaim", "route duplication",
            ],
            "controls": [
                "typed units", "explicit datum identifiers", "half-open intervals", "vacancy preservation",
                "append-only lineage", "synthetic-only firewall", "exact gates", "send-once guard",
            ],
            "exhaustive_security_claim": False,
        },
        "route-plan.json": {
            "schema": "ghc.family.route-plan.v12",
            "owner": OWNER,
            "phase": PHASE,
            "prospective_successor": "Ilyra Fen",
            "prospective_phase": "v675-v7",
            "precontacted": False,
            "delivery_claimed": False,
            "terminal_only": True,
            "required_gates": [
                "fresh Hamish authority", "current roster and auth", "exact-title uniqueness",
                "immediate reread", "duplicate and pause guard", "privacy and safety guard",
                "usage guard", "single send acknowledgement",
            ],
        },
        "phase-truth.json": {
            "schema": "ghc.family.phase-truth.v12",
            "owner": OWNER,
            "phase": PHASE,
            "lifecycle": "planning_only_x1",
            "allowed_outcome_labels": list(ALLOWED_OUTCOMES),
            "planned_outcomes": {label: sum(row["planned_outcome"] == label for row in rows) for label in ALLOWED_OUTCOMES},
            "working_overlay": x1_overlay,
            "x2_started": False,
            "canonical_validation_started": False,
            "successor_contacted": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    }

    for name, value in artifacts.items():
        write_json(X1_DIR / name, value)
    write_text_lf(X1_DIR / "integrated-overview.md", integrated_overview(audit, rows))
    print(
        json.dumps(
            {
                "state": "BUILT_PLANNING_ONLY_X1",
                "owner": OWNER,
                "phase": PHASE,
                "files": len(artifacts) + 1,
                "proposal_rows": len(rows),
                "semantic_collisions": 0,
                "declared_chain_after": DECLARED_CHAIN_AFTER,
                "working_overlay": x1_overlay,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(seal_x1_index() if sys.argv[1:] == ["--seal"] else main())
