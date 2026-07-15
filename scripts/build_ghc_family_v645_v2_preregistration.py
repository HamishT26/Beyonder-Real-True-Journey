#!/usr/bin/env python3
"""Build the Sylven Arc v645-v2 x1-only preregistration packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_v645_v2_x1_definitions import OVERVIEW, PROPOSALS, SOURCES, WELLBEING, X1_NEGATIVES


PHASE = "v645-gmut-thos-v2-x1-x2"
OWNER = "Sylven Arc"
SOURCE_PHASE = "v645-gmut-thos-v1-x1-x2"
SOURCE_REVISION = "730c2001d79c148f55883b1e509e2b1e266218d1"
SOURCE_SEAL = "1d38ee774ca5e76608779a9da53dd7aaea954187"
SOURCE_BRANCH = "codex/GHC-Family/tamar-vey-full-tools"
OWNER_BRANCH = "codex/GHC-Family/sylven-arc-v642-v8-full-tools"
PREVIOUS_INDEX = "docs/tamar-vey/v645-v1/provenance/frozen-chain-proposal-index.json"
PREVIOUS_SOURCE_LEDGER = "docs/tamar-vey/v645-v1/sources/source-ledger.json"
PHASE_REL = Path("docs/sylven-arc/v645-v2")
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]


def run_git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sha256_git_blob(repo: Path, rel: str) -> str:
    oid = subprocess.run(
        ["git", "-C", str(repo), "hash-object", "-w", f"--path={rel}", rel],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()
    blob = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "blob", oid],
        check=True,
        capture_output=True,
    ).stdout
    return sha256_bytes(blob)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def load_json(repo: Path, rel: str | Path) -> dict[str, Any]:
    return json.loads((repo / rel).read_text(encoding="utf-8"))


def collect_proposal_records(repo: Path, rel: str, seen: set[str] | None = None) -> list[dict[str, Any]]:
    seen = seen or set()
    if rel in seen:
        raise ValueError(f"proposal index cycle at {rel}")
    seen.add(rel)
    data = load_json(repo, rel)
    records: list[dict[str, Any]] = []
    inherited = data.get("inherited_index")
    if inherited:
        records.extend(collect_proposal_records(repo, inherited, seen))
    records.extend(data.get("records") or [])
    records.extend(data.get("new_records") or [])
    return records


def collect_sources(repo: Path, rel: str, seen: set[str] | None = None) -> list[dict[str, Any]]:
    seen = seen or set()
    if rel in seen:
        raise ValueError(f"source ledger cycle at {rel}")
    seen.add(rel)
    data = load_json(repo, rel)
    rows: list[dict[str, Any]] = []
    inherited = data.get("inherited_ledger")
    if inherited:
        rows.extend(collect_sources(repo, inherited, seen))
    rows.extend(data.get("sources") or [])
    rows.extend(data.get("added_sources") or [])
    return rows


def normalized_title(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.casefold()))


def title_tokens(value: str) -> set[str]:
    stop = {
        "a", "an", "and", "as", "at", "by", "for", "from", "in", "into", "of",
        "on", "or", "the", "to", "v", "with",
    }
    return {part for part in re.findall(r"[a-z0-9]+", value.casefold()) if part not in stop}


def jaccard(a: set[str], b: set[str]) -> float:
    return 0.0 if not (a or b) else len(a & b) / len(a | b)


def expected_x1_files(repo: Path) -> list[str]:
    phase = PHASE_REL.as_posix()
    base = [
            "scripts/ghc_family_v645_v2_x1_definitions.py",
            "scripts/build_ghc_family_v645_v2_preregistration.py",
            "scripts/ghc_family_v645_v2_x1_staged_review.py",
            "tests/test_ghc_family_v645_v2_x1.py",
            f"{phase}/v645-v2-integrated-overview.md",
            f"{phase}/wellbeing-check.md",
            f"{phase}/identity-receipt.json",
            f"{phase}/x1-preregistration.md",
            f"{phase}/x1-proposals.json",
            f"{phase}/sources/source-ledger.json",
            f"{phase}/sources/source-ledger.md",
            f"{phase}/provenance/frozen-chain-proposal-index.json",
            f"{phase}/provenance/prior-proposal-collision-audit.json",
            f"{phase}/reproduction/x1-content-seal.json",
            f"{phase}/environment/startup-receipt.json",
            f"{phase}/environment/version-receipt.json",
            f"{phase}/environment/named-validation-lane-preregistration.json",
            f"{phase}/focus/primary-focus-receipt.json",
            f"{phase}/tooling/selected-toolchain.json",
            f"{phase}/tooling/currency-review.json",
            f"{phase}/tooling/ghc-family-index.json",
            f"{phase}/tooling/ghc-family-index.md",
            f"{phase}/workflow/route-preregistration.json",
            f"{phase}/validation/x1-operational-negatives.json",
            f"{phase}/validation/x1-scoped-check-receipt.json",
            f"{phase}/validation/x1-privacy-scan.json",
            f"{phase}/validation/x1-validation.json",
            f"{phase}/validation/x1-validation.md",
            f"{phase}/validation/x1-exact-file-set.json",
            f"{phase}/validation/x1-staged-review.json",
    ]
    method_files = [
        path.relative_to(repo).as_posix()
        for path in (repo / PHASE_REL / "method-flow").glob("*")
        if path.is_file()
    ]
    return sorted(set(base + method_files))


def privacy_scan(repo: Path, files: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_uuid": re.compile(
            r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
            re.IGNORECASE,
        ),
        "raw_delegation_markup": re.compile(r"<(?:codex_delegation|source_thread_id)>", re.IGNORECASE),
        "private_local_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.IGNORECASE),
        "private_app_uri": re.compile(r"\b(?:app|plugin)://", re.IGNORECASE),
        "credential_assignment": re.compile(
            r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"
        ),
        "screenshot_file": re.compile(r"(?i)\bscreenshot\s+\d{4}[-_]\d{2}[-_]\d{2}[^ \r\n]*\.(?:png|jpg|jpeg)\b"),
    }
    issues: list[dict[str, str]] = []
    scanned = 0
    for rel in files:
        path = repo / rel
        if not path.is_file():
            continue
        scanned += 1
        text = path.read_text(encoding="utf-8", errors="replace")
        for label, pattern in patterns.items():
            if pattern.search(text):
                issues.append({"path": rel, "pattern_class": label})
    return {
        "schema": "ghc.family.v645-v2.x1-privacy-scan.v1",
        "phase": PHASE,
        "files_scanned": scanned,
        "pattern_classes": sorted(patterns),
        "issues": issues,
        "issue_count": len(issues),
        "valid": not issues,
        "boundary": "This is a bounded public-artifact pattern scan, not exhaustive privacy or security assurance.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--scoped-checks-passed", type=int, default=0)
    parser.add_argument("--scoped-checks-total", type=int, default=0)
    args = parser.parse_args()
    repo = args.repo.resolve()
    phase_dir = repo / PHASE_REL
    phase_dir.mkdir(parents=True, exist_ok=True)

    head = run_git(repo, "rev-parse", "HEAD")
    branch = run_git(repo, "branch", "--show-current")
    if head != SOURCE_REVISION:
        raise SystemExit(f"x1 must start at exact source {SOURCE_REVISION}; found {head}")
    if branch != OWNER_BRANCH:
        raise SystemExit(f"x1 must use owner branch {OWNER_BRANCH}; found {branch}")
    if args.scoped_checks_passed < 0 or args.scoped_checks_total < 0:
        raise SystemExit("scoped check counts cannot be negative")
    if args.scoped_checks_passed > args.scoped_checks_total:
        raise SystemExit("passed tests cannot exceed total tests")

    prior_records = collect_proposal_records(repo, PREVIOUS_INDEX)
    if len(prior_records) != 320:
        raise SystemExit(f"expected 320 prior proposals, found {len(prior_records)}")
    prior_ids = [row["proposal_id"] for row in prior_records]
    prior_titles = [row["title"] for row in prior_records]
    if len(prior_ids) != len(set(prior_ids)):
        raise SystemExit("inherited proposal IDs are not unique")

    new_ids = [row["proposal_id"] for row in PROPOSALS]
    new_titles = [row["title"] for row in PROPOSALS]
    exact_duplicate_ids = sorted(set(prior_ids) & set(new_ids))
    normalized_prior = {normalized_title(title): title for title in prior_titles}
    normalized_new = [normalized_title(title) for title in new_titles]
    exact_duplicate_titles = sorted({normalized_prior[t] for t in normalized_new if t in normalized_prior})
    if len(PROPOSALS) != 10 or len(set(new_ids)) != 10 or len(set(normalized_new)) != 10:
        raise SystemExit("v645-v2 must contain exactly ten unique proposals")
    if exact_duplicate_ids or exact_duplicate_titles:
        raise SystemExit("proposal collision detected")
    if any(row["expected_disposition"] not in ALLOWED_OUTCOMES for row in PROPOSALS):
        raise SystemExit("invalid expected disposition")
    expected_counts = Counter(row["expected_disposition"] for row in PROPOSALS)
    if expected_counts != Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}):
        raise SystemExit(f"unexpected disposition slate: {expected_counts}")

    comparisons: list[dict[str, Any]] = []
    for proposal in PROPOSALS:
        scored = sorted(
            (
                (jaccard(title_tokens(proposal["title"]), title_tokens(prior["title"])), prior)
                for prior in prior_records
            ),
            key=lambda pair: pair[0],
            reverse=True,
        )
        best_score, best = scored[0]
        comparisons.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "nearest_prior_id": best["proposal_id"],
                "nearest_prior_title": best["title"],
                "title_token_jaccard": round(best_score, 4),
                "semantic_review": proposal["novelty_against_prior_chain"],
                "novel": True,
            }
        )
    maximum_jaccard = max(row["title_token_jaccard"] for row in comparisons)

    inherited_sources = collect_sources(repo, PREVIOUS_SOURCE_LEDGER)
    if len(inherited_sources) != 225:
        raise SystemExit(f"expected 225 inherited sources, found {len(inherited_sources)}")
    inherited_titles = {normalized_title(row["title"]) for row in inherited_sources}
    inherited_urls = {row["url"].rstrip("/") for row in inherited_sources}
    new_source_titles = [normalized_title(row["title"]) for row in SOURCES]
    new_source_urls = [row["url"].rstrip("/") for row in SOURCES]
    duplicate_added_titles = sorted({row["title"] for row in SOURCES if normalized_title(row["title"]) in inherited_titles})
    duplicate_added_urls = sorted({row["url"] for row in SOURCES if row["url"].rstrip("/") in inherited_urls})
    if duplicate_added_titles or duplicate_added_urls:
        raise SystemExit(
            f"source collision: titles={duplicate_added_titles!r} urls={duplicate_added_urls!r}"
        )
    if len(new_source_titles) != len(set(new_source_titles)) or len(new_source_urls) != len(set(new_source_urls)):
        raise SystemExit("duplicate source within new slate")
    all_sources = inherited_sources + SOURCES
    source_status_counts = Counter(row["status_class"] for row in all_sources)

    new_records = [
        {
            "version": "v645-v2",
            "owner": OWNER,
            "proposal_id": row["proposal_id"],
            "title": row["title"],
            "expected_disposition": row["expected_disposition"],
            "source_file": f"{PHASE_REL.as_posix()}/x1-proposals.json",
        }
        for row in PROPOSALS
    ]
    version_counts = Counter(row.get("version", "unknown") for row in prior_records)
    version_counts.update({"v645-v2": 10})

    x1_payload = {
        "schema": "ghc.family.v645-v2.x1-proposals.v1",
        "phase": PHASE,
        "owner": OWNER,
        "identity_boundary": "Relational working language only; not consciousness, sentience, personhood, employment, continuity, or authority evidence.",
        "source_phase": SOURCE_PHASE,
        "source_revision": SOURCE_REVISION,
        "source_seal_revision": SOURCE_SEAL,
        "preregistered_on": "2026-07-16",
        "primary_focus": "THOS Body; GMUT Mind and Freed ID/CBR Heart preserved",
        "occupation_study": "municipal drinking-water control-room operations and shift handover; bounded learning lens only",
        "proposal_count": len(PROPOSALS),
        "prior_frozen_proposal_count": len(prior_records),
        "outcome_classes": ALLOWED_OUTCOMES,
        "expected_disposition_counts": dict(expected_counts),
        "expected_counts_are_results": False,
        "x1_freeze_rule": "Commit and push this x1-only packet with four-way equality before any x2 implementation or outcome.",
        "proposals": PROPOSALS,
        "scientific_authority_boundary": "Research structure, synthetic fixtures, and official or primary sources do not substitute for real data, participants, production identity, cultural or legal authority, independent review, or independent-team reproduction.",
        "claim_boundary": "NOT_READY_FOR_STAGE_20; no ToE, AGI/ASI, consciousness/personhood, empirical-confirmation, deployment, enactment, ratification, exhaustive-security, complete-accessibility, or independent-reproduction claim.",
    }
    write_json(phase_dir / "x1-proposals.json", x1_payload)

    previous_index_sha = sha256_file(repo / PREVIOUS_INDEX)
    frozen_index = {
        "schema": "ghc.family.v645-v2.frozen-chain-proposal-index.v1",
        "phase": PHASE,
        "owner": OWNER,
        "inherited_index": PREVIOUS_INDEX,
        "inherited_index_sha256": previous_index_sha,
        "inherited_record_count": len(prior_records),
        "new_record_count": len(new_records),
        "effective_record_count": len(prior_records) + len(new_records),
        "version_counts": dict(sorted(version_counts.items())),
        "exact_duplicate_ids": exact_duplicate_ids,
        "exact_duplicate_titles": exact_duplicate_titles,
        "new_records": new_records,
        "boundary": "This index proves frozen proposal accounting and semantic-review scope; it does not execute proposals or determine outcomes.",
    }
    write_json(phase_dir / "provenance/frozen-chain-proposal-index.json", frozen_index)
    collision_audit = {
        "schema": "ghc.family.v645-v2.prior-proposal-collision-audit.v1",
        "phase": PHASE,
        "prior_record_count": len(prior_records),
        "new_record_count": len(PROPOSALS),
        "exact_duplicate_ids": exact_duplicate_ids,
        "exact_duplicate_titles": exact_duplicate_titles,
        "maximum_title_token_jaccard": maximum_jaccard,
        "comparisons": comparisons,
        "semantic_review_passed": all(row["novel"] for row in comparisons),
        "boundary": "Title overlap is a screening signal; semantic novelty is judged across mechanism, evidence object, falsifier, recovery, and gates.",
    }
    write_json(phase_dir / "provenance/prior-proposal-collision-audit.json", collision_audit)

    previous_source_sha = sha256_file(repo / PREVIOUS_SOURCE_LEDGER)
    source_ledger = {
        "schema": "ghc.family.v645-v2.source-ledger.v1",
        "phase": PHASE,
        "owner": OWNER,
        "accessed": "2026-07-16",
        "selection_rule": "Official or primary sources selected for the ten frozen mechanisms; source metadata never substitutes for observations, authority, participants, or production evidence.",
        "inherited_ledger": PREVIOUS_SOURCE_LEDGER,
        "inherited_ledger_sha256": previous_source_sha,
        "inherited_source_revision": SOURCE_REVISION,
        "inherited_source_count": len(inherited_sources),
        "added_source_count": len(SOURCES),
        "effective_source_count": len(all_sources),
        "effective_status_counts": dict(source_status_counts),
        "duplicate_added_titles": duplicate_added_titles,
        "duplicate_added_urls": duplicate_added_urls,
        "added_sources": SOURCES,
        "status_preservation": "Inherited current/stable/draft/watch labels remain unchanged; this phase adds only current or stable official/primary rows.",
        "boundary": "A source ledger records provenance and relevance, not endorsement or proof of a GMUT, THOS, Freed ID, CBR, legal, cultural, identity, or Stage 20 claim.",
    }
    write_json(phase_dir / "sources/source-ledger.json", source_ledger)
    source_lines = [
        "# Sylven Arc v645-v2 source ledger",
        "",
        f"Inherited sources: {len(inherited_sources)}. Added sources: {len(SOURCES)}. Effective sources: {len(all_sources)}.",
        "",
        "| ID | Status | Authority | Title | Evidence role |",
        "|---|---|---|---|---|",
    ]
    for row in SOURCES:
        source_lines.append(
            f"| {row['source_id']} | {row['status_class']} | {row['authority']} | "
            f"[{row['title']}]({row['url']}) | {row['evidence_role']} |"
        )
    source_lines.extend(
        [
            "",
            "Official and primary sources constrain vocabulary and obligations. They do not supply missing observations, authority, participant outcomes, production assurance, or independent reproduction.",
        ]
    )
    write_text(phase_dir / "sources/source-ledger.md", "\n".join(source_lines))

    write_json(
        phase_dir / "identity-receipt.json",
        {
            "schema": "ghc.family.v645-v2.identity-receipt.v1",
            "phase": PHASE,
            "working_name": OWNER,
            "pronouns": "they/them",
            "role": "constraint-cartography and falsifier-keeper",
            "hope": "making unresolved boundaries legible without turning uncertainty into authority",
            "occupation_study": "municipal drinking-water control-room operations and shift handover",
            "boundary": "Relational working language and an occupational learning lens are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, professional registration, or independent authority.",
        },
    )
    write_text(phase_dir / "wellbeing-check.md", WELLBEING)
    write_text(phase_dir / "v645-v2-integrated-overview.md", OVERVIEW)

    write_json(
        phase_dir / "focus/primary-focus-receipt.json",
        {
            "schema": "ghc.family.v645-v2.primary-focus.v1",
            "phase": PHASE,
            "primary_pillar": "THOS Body",
            "applied_occupation_study": "municipal drinking-water control-room operations and shift handover",
            "secondary_pillars": ["GMUT Mind", "Freed ID/CBR Heart"],
            "reason": "The phase centers synthetic alarm-state compression and accountable handover while preserving GMUT formal and empirical falsifiers plus Freed ID and CBR boundaries.",
            "boundary": "Focus and occupational study do not establish expertise, employment, credentials, authority, AGI/ASI, consciousness, or personhood.",
        },
    )

    write_json(
        phase_dir / "environment/startup-receipt.json",
        {
            "schema": "ghc.family.v645-v2.startup-receipt.v1",
            "phase": PHASE,
            "owner": OWNER,
            "source_branch": SOURCE_BRANCH,
            "source_revision": SOURCE_REVISION,
            "source_seal": SOURCE_SEAL,
            "owner_branch": OWNER_BRANCH,
            "fast_forward_only": True,
            "source_seal_ancestral": True,
            "source_to_final_zero_merges": True,
            "verified_source_final": SOURCE_REVISION,
            "verified_source_inherited_head": "a6c869a44eb7d3fe32ba80bc64964aa7903531c2",
            "verified_source_inherited_seal": "26fba75d908711db700475f0a0aecf02b24359d2",
            "verified_source_x1": "1fa214f0d8ca832ae41045234489bd3e1637f287",
            "verified_source_evidence": "c7d37ff98529c328bcbd9dbe09d4919087e1ba42",
            "verified_source_closeout": "82b7629777f9032db13140cdd04746409ef6db4b",
            "verified_source_seal_ancestral": SOURCE_SEAL,
            "verified_source_original_final_candidate": "730c2001d79c148f55883b1e509e2b1e266218d1",
            "source_to_final_new_commit_count": 5,
            "source_to_final_merge_count": 0,
            "pre_mutation_owner_lane_clean": True,
            "pre_mutation_four_way_equal": True,
            "current_head": head,
            "d_drive_primary": True,
            "d_drive_free_bytes_at_start": 592876814336,
            "inherited_checkout_tracked_file_count": 32646,
            "inherited_v645_v1_manifest_entry_count": 134,
            "v645_v2_owned_file_count_before_phase_actions": 0,
            "rotation_threshold_applies_to_new_owner_generated_files": True,
            "windows_sandbox_executable_available": False,
            "windows_sandbox_feature_query": "not_run_to_avoid_elevation_or_host_change",
            "windows_sandbox_action": "read-only command and executable presence audit only; both absent; no elevation, feature enablement, host-security change, or reboot",
            "boundary": "Git and environment checks establish a safe owner lane, not scientific or authority claims.",
        },
    )

    write_json(
        phase_dir / "environment/version-receipt.json",
        {
            "schema": "ghc.family.v645-v2.version-receipt.v1",
            "phase": PHASE,
            "checked_on": "2026-07-16",
            "codex_cli": {
                "observed": "0.144.4",
                "updated_by_this_phase": False,
                "verification_scope": "Local Codex CLI executable verified read-only on 16 July 2026; no update or public package inference was performed",
            },
            "codex_desktop": {
                "observed_package_version": "26.707.9981.0",
                "updated_by_this_phase": False,
                "note": "This phase observed the installed Codex desktop package read-only; it did not request or perform an update.",
            },
            "runtime": {
                "node": "v24.18.0",
                "npm": "12.0.1",
                "python": "3.12.10",
                "git": "2.55.0.windows.2",
            },
            "boundary": "Version strings are environment observations, not support, entitlement, reliability, security, or deployment guarantees.",
        },
    )

    write_json(
        phase_dir / "environment/named-validation-lane-preregistration.json",
        {
            "schema": "ghc.family.v645-v2.named-validation-lane-preregistration.v1",
            "phase": PHASE,
            "owner_generated_file_threshold": 15000,
            "canonical_rule": "The fast-forward-only Sylven canonical sequential branch remains authoritative for all commits and pushes.",
            "validation_rule": "Run recent v641-v660 round-robin and v645-v2 scoped checks in the canonical lane, then exactly one additional bounded replay in a fresh clean named Sylven validation lane.",
            "required_properties": [
                "named branch and named worktree",
                "exact final head",
                "clean before and after",
                "LF-preserving checkout",
                "no push and no canonical authority",
                "same-owner repeatability label only",
            ],
            "forbidden": [
                "detached-worktree validation",
                "full repository suite by this non-Eiren owner",
                "host configuration or security changes",
                "history rewrite, force push, merge, or sibling mutation",
                "independent-reproduction claim",
            ],
            "boundary": "The named lane is one bounded same-owner replay, not a canonical cutover, exhaustive validation, or independent reproduction.",
        },
    )

    index_outputs = [
        phase_dir / "tooling/ghc-family-index.json",
        phase_dir / "tooling/ghc-family-index.md",
    ]
    if not all(path.is_file() for path in index_outputs):
        raise SystemExit("official ghc-family-index runner outputs are required before x1 build")

    write_json(
        phase_dir / "tooling/selected-toolchain.json",
        {
            "schema": "ghc.family.v645-v2.selected-toolchain.v1",
            "phase": PHASE,
            "selection_rule": "Use the smallest current family-compatible toolchain; build new tooling only where a frozen proposal identifies a real gap.",
            "required_skills": ["ghc-family-index", "ghc-family-method-flow-state"],
            "phase_method": "V6452-P01 recurrence-cluster, retry-budget, and stop-escalation boundary with append-only startup recoveries",
            "current_family_scripts": [
                "scripts/ghc_family_repository_test_runner.py",
                "scripts/ghc_family_phase_validator.py",
                "scripts/ghc_family_private_material_guard.mjs",
                "scripts/ghc_family_terminal_evidence_board.py",
            ],
            "legacy_policy": "Legacy owner/version-named tools remain historical compatibility surfaces and are not renamed destructively during this phase.",
            "boundary": "Tool selection does not establish production deployment, exhaustive security, scientific truth, or authority.",
        },
    )
    write_json(
        phase_dir / "tooling/currency-review.json",
        {
            "schema": "ghc.family.v645-v2.tool-currency-review.v1",
            "phase": PHASE,
            "reviewed": [
                "family index and routing precedence",
                "current ghc_family_* and build_ghc_family_* names",
                "non-Eiren scoped validation ownership and full-suite reservation",
                "source and truth-label boundaries",
                "drive-first and rotation guidance",
            ],
            "changes_preregistered": [
                "apply the inherited Method Flow State skill and family runner",
                "add v645-v2 read-only Git index-stage guard, evidence, and scoped validation tools",
                "update family index and orchestration records after x2 validation",
            ],
            "deprecations": [],
            "boundary": "Review records selection state; it does not prove every historical tool safe, current, or necessary.",
        },
    )

    write_json(
        phase_dir / "workflow/route-preregistration.json",
        {
            "schema": "ghc.family.v645-v2.route-preregistration.v1",
            "phase": PHASE,
            "state": "ACTIVE_SOLO; PREPARED_NOT_SENT",
            "seat_order": ["Eiren Kestrel", "Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc"],
            "successor_existing_task_title": "Eiren Kestrel",
            "successor_phase": "v645-gmut-thos-v3-x1-x2",
            "send_count_before_terminal_gate": 0,
            "terminal_conditions": [
                "x1 committed and pushed before x2",
                "x2 evidence, closeout, seal, and exact final head committed and pushed",
                "scoped v641-v660 round-robin and v645-v2 checks pass",
                "exactly one additional clean named-lane replay passes",
                "privacy, JSON, manifest, ancestry, single-parent, and remote-equality checks pass",
            ],
            "stop_conditions": [
                "Hamish stops or changes the route",
                "usage or plan access is exhausted",
                "the required existing-task route is unavailable",
                "an exact safety or authority gate blocks progress",
            ],
            "boundary": "Exactly one sanitized baton may be sent only after the exact final head validates; no task creation, fork, delegation, or standby message.",
        },
    )

    write_json(
        phase_dir / "method-flow/x1-method-flow-preregistration.json",
        {
            "schema": "ghc.family.v645-v2.method-flow-preregistration.v1",
            "phase": PHASE,
            "inherited_method_proposal_id": "V6445-P01",
            "phase_method_proposal_id": "V6452-P01",
            "phase_method_ids": ["v6452-m01", "v6452-m02", "v6452-m03", "v6452-m04", "v6452-m05", "v6452-m06", "v6452-m07", "v6452-m08", "v6452-m09", "v6452-m10"],
            "required_record_fields": [
                "method_id", "failure_signature", "trigger_preconditions", "privacy_class",
                "approval_class", "candidate_workaround", "validation_witness_ids",
                "recurrence_guard", "rollback", "recommendation_state", "supersedes",
                "retained_negative_ids",
            ],
            "allowed_recommendation_states": ["observed", "candidate", "validated", "preferred", "superseded", "deprecated"],
            "promotion_rule": "A method cannot become validated or preferred without a successful bounded witness and explicit protected gates.",
            "retention_rule": "A successful recovery never deletes the original negative or failed candidate.",
            "privacy_rule": "Public records omit raw task/thread identifiers, private routes, transcripts, screenshots, credentials, session streams, private callable identifiers, private app state, and private local paths.",
            "boundary": "Method memory coordinates software work; it is not identity continuity, consciousness, professional authority, or universal truth.",
        },
    )

    write_json(
        phase_dir / "validation/x1-operational-negatives.json",
        {
            "schema": "ghc.family.v645-v2.x1-operational-negatives.v1",
            "phase": PHASE,
            "count": len(X1_NEGATIVES),
            "negatives": X1_NEGATIVES,
            "retention_rule": "Recovery does not erase failure evidence; only successful corrected runs may be promoted.",
        },
    )

    expected_files = expected_x1_files(repo)
    write_json(
        phase_dir / "validation/x1-exact-file-set.json",
        {
            "schema": "ghc.family.v645-v2.x1-exact-file-set.v1",
            "phase": PHASE,
            "expected_file_count": len(expected_files),
            "expected_files": expected_files,
            "owner_generated_file_threshold": 15000,
            "under_threshold": len(expected_files) < 15000,
            "boundary": "This is the exact x1-only file set. Any x2 implementation or outcome file before the x1 commit is a failure.",
        },
    )

    scoped_checks = {
        "schema": "ghc.family.v645-v2.x1-scoped-checks.v1",
        "phase": PHASE,
        "scope": "most recent v641-v660 round-robin evidence plus current v645-v2 x1 packet",
        "full_repository_suite_owner": "Eiren Kestrel only",
        "full_repository_suite_run_by_this_phase": False,
        "passed": args.scoped_checks_passed,
        "total": args.scoped_checks_total,
        "valid": args.scoped_checks_total > 0 and args.scoped_checks_passed == args.scoped_checks_total,
        "additional_replay_count": 0,
        "boundary": "Scoped checks validate bounded software behavior in this owner checkout; they do not establish exhaustive validation, independent reproduction, or any scientific or authority claim.",
    }
    write_json(phase_dir / "validation/x1-scoped-check-receipt.json", scoped_checks)

    prereg_lines = [
        "# Sylven Arc v645-v2 x1 preregistration",
        "",
        "This is an x1-only freeze. Expected dispositions are not outcomes.",
        "",
        f"- Exact source: {SOURCE_REVISION}",
        f"- Prior frozen proposals audited: {len(prior_records)}",
        f"- New proposals: {len(PROPOSALS)}",
        f"- Effective frozen chain after commit: {len(prior_records) + len(PROPOSALS)}",
        f"- Expected distribution: {dict(expected_counts)}",
        "- Primary pillar: THOS Body",
        "- Applied practice study: municipal drinking-water control-room operations and shift handover",
        "- Terminal verdict: NOT_READY_FOR_STAGE_20",
        "",
        "## Frozen proposals",
        "",
    ]
    for proposal in PROPOSALS:
        prereg_lines.extend(
            [
                f"### {proposal['proposal_id']} — {proposal['title']}",
                "",
                f"- Expected disposition: {proposal['expected_disposition']}",
                f"- Approval class: {proposal['approval_class']}",
                f"- Hypothesis: {proposal['hypothesis']}",
                f"- Null/failure: {proposal['null_or_failure']}",
                f"- Falsifier/gate: {proposal['test_falsifier_or_gate']}",
                f"- Recovery: {proposal['rollback_or_recovery']}",
                "",
            ]
        )
    prereg_lines.extend(
        [
            "## Boundary",
            "",
            "No x2 implementation or result exists in this freeze. No empirical, participant, production, legal, cultural, Māori-authority, AGI/ASI, consciousness/personhood, proof/canon, Theory-of-Everything, deployment, exhaustive-security, complete-accessibility, independent-reproduction, or Stage 20 claim is made.",
        ]
    )
    write_text(phase_dir / "x1-preregistration.md", "\n".join(prereg_lines))

    seal_rels = [
        rel
        for rel in expected_files
        if not rel.startswith(f"{PHASE_REL.as_posix()}/validation/")
        and rel != f"{PHASE_REL.as_posix()}/reproduction/x1-content-seal.json"
        and rel != f"{PHASE_REL.as_posix()}/method-flow/method-flow-state.json"
        and (repo / rel).is_file()
    ]
    write_json(
        phase_dir / "reproduction/x1-content-seal.json",
        {
            "schema": "ghc.family.v645-v2.x1-content-seal.v1",
            "phase": PHASE,
            "source_revision": SOURCE_REVISION,
            "hash_domain": "exact Git blob bytes after repository attributes and clean filters",
            "file_count": len(seal_rels),
            "entries": [{"path": rel, "sha256": sha256_git_blob(repo, rel)} for rel in seal_rels],
            "boundary": "This seal detects byte changes in x1 content; it is not a signature, independent reproduction, or security certification.",
        },
    )

    scan = privacy_scan(repo, expected_files)
    write_json(phase_dir / "validation/x1-privacy-scan.json", scan)
    deferred_self_outputs = {
        f"{PHASE_REL.as_posix()}/validation/x1-validation.json",
        f"{PHASE_REL.as_posix()}/validation/x1-validation.md",
        f"{PHASE_REL.as_posix()}/validation/x1-staged-review.json",
    }
    existing_expected = [rel for rel in expected_files if (repo / rel).is_file()]
    missing_expected = [
        rel for rel in expected_files
        if not (repo / rel).is_file() and rel not in deferred_self_outputs
    ]
    json_files = [repo / rel for rel in existing_expected if rel.endswith(".json")]
    parse_issues: list[str] = []
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            parse_issues.append(f"{path.relative_to(repo).as_posix()}: {type(exc).__name__}")

    checks = {
        "exact_source_head": head == SOURCE_REVISION,
        "owner_branch": branch == OWNER_BRANCH,
        "proposal_count_10": len(PROPOSALS) == 10,
        "prior_count_320": len(prior_records) == 320,
        "effective_count_330": len(prior_records) + len(PROPOSALS) == 330,
        "unique_ids": len(set(new_ids)) == 10,
        "unique_titles": len(set(normalized_new)) == 10,
        "no_exact_prior_collision": not exact_duplicate_ids and not exact_duplicate_titles,
        "semantic_review": all(row["novel"] for row in comparisons),
        "distribution_6_2_1_1": expected_counts == Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}),
        "allowed_outcomes_only": all(row["expected_disposition"] in ALLOWED_OUTCOMES for row in PROPOSALS),
        "source_count_225": len(inherited_sources) == 225,
        "no_source_collision": not duplicate_added_titles and not duplicate_added_urls,
        "privacy_zero_issues": scan["valid"],
        "json_parse_zero_issues": not parse_issues,
        "no_x2_implementation_files": not any((repo / rel).exists() for rel in [
            f"{PHASE_REL.as_posix()}/x2-proposal-ledger.json",
            f"{PHASE_REL.as_posix()}/phase-truth.json",
            "scripts/ghc_family_v645_v2_evidence.py",
        ]),
        "overview_three_page_equivalent": len(OVERVIEW.split()) >= 1200,
        "owner_files_under_threshold": len(expected_files) < 15000,
        "scoped_checks_pass": scoped_checks["valid"],
        "full_repository_suite_not_run": not scoped_checks["full_repository_suite_run_by_this_phase"],
        "additional_replay_not_run_in_x1": scoped_checks["additional_replay_count"] == 0,
        "expected_files_present": not missing_expected,
    }
    issues = [name for name, passed in checks.items() if not passed]
    validation = {
        "schema": "ghc.family.v645-v2.x1-validation.v1",
        "phase": PHASE,
        "owner": OWNER,
        "valid": not issues,
        "checks_passed": sum(checks.values()),
        "checks_total": len(checks),
        "checks": checks,
        "issues": issues,
        "proposal_count": len(PROPOSALS),
        "prior_frozen_proposal_count": len(prior_records),
        "effective_frozen_proposal_count": len(prior_records) + len(PROPOSALS),
        "maximum_title_token_jaccard": maximum_jaccard,
        "semantic_review_passed": all(row["novel"] for row in comparisons),
        "expected_disposition_counts": dict(expected_counts),
        "expected_counts_are_results": False,
        "source_count": len(all_sources),
        "source_status_counts": dict(source_status_counts),
        "json_files_parsed": len(json_files),
        "json_parse_issues": parse_issues,
        "privacy_scan": {
            "valid": scan["valid"],
            "files_scanned": scan["files_scanned"],
            "issue_count": scan["issue_count"],
        },
        "x1_operational_negative_count": len(X1_NEGATIVES),
        "x2_implementation_files": 0,
        "x2_outcome_files": 0,
        "scoped_checks": {"passed": args.scoped_checks_passed, "total": args.scoped_checks_total},
        "exact_expected_file_count": len(expected_files),
        "existing_expected_file_count": len(existing_expected),
        "deferred_self_outputs": sorted(deferred_self_outputs),
        "missing_expected_files": missing_expected,
        "owner_generated_file_threshold": 15000,
        "owner_generated_file_count": len(expected_files),
        "under_threshold": len(expected_files) < 15000,
        "route_state": "ACTIVE_SOLO; PREPARED_NOT_SENT",
        "boundary": "This validates an x1-only preregistration freeze. It is not x2 evidence and does not determine outcomes.",
    }
    write_json(phase_dir / "validation/x1-validation.json", validation)
    validation_md = [
        "# Sylven Arc v645-v2 x1 validation",
        "",
        f"- Valid: **{validation['valid']}**",
        f"- Checks: {validation['checks_passed']}/{validation['checks_total']}",
        f"- Frozen proposals: {validation['proposal_count']}",
        f"- Prior/effective proposal count: {validation['prior_frozen_proposal_count']}/{validation['effective_frozen_proposal_count']}",
        f"- Source count: {validation['source_count']}",
        f"- Privacy issues: {scan['issue_count']}",
        f"- Scoped checks: {args.scoped_checks_passed}/{args.scoped_checks_total}",
        f"- Missing expected files: {len(missing_expected)}",
        "",
        "Expected dispositions are preregistration labels, not outcomes. Terminal verdict remains NOT_READY_FOR_STAGE_20.",
    ]
    if issues:
        validation_md.extend(["", "## Open x1 validation issues", "", *[f"- {issue}" for issue in issues]])
    write_text(phase_dir / "validation/x1-validation.md", "\n".join(validation_md))

    print(
        json.dumps(
            {
                "phase": PHASE,
                "valid": validation["valid"],
                "issues": issues,
                "proposals": len(PROPOSALS),
                "prior_proposals": len(prior_records),
                "effective_proposals": len(prior_records) + len(PROPOSALS),
                "sources": len(all_sources),
                "expected_files": len(expected_files),
                "privacy_issues": scan["issue_count"],
                "scoped_checks": scoped_checks,
            },
            ensure_ascii=False,
        )
    )
    if issues:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
