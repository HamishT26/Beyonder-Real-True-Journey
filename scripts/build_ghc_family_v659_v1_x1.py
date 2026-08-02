#!/usr/bin/env python3
"""Build the frozen x1 packet for Ilyra Fen v659-v1."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import ghc_family_v659_v1_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
PRIOR_PHASE = ROOT / "docs/lyren-moss/v658-v8-2-remaster"
PRIOR_LEDGER = PRIOR_PHASE / "preregistration/proposal-ledger.json"
PRIOR_INDEX = PRIOR_PHASE / "provenance/frozen-chain-proposal-index.json"
NOVELTY_THRESHOLD = 0.60
MANIFEST_EXCLUSIONS = {
    "validation/x1-content-manifest.json",
    "validation/x1-privacy-scan.json",
    "validation/x1-document-cap.json",
}
X1_CODE = [
    "scripts/ghc_family_v659_v1_data.py",
    "scripts/build_ghc_family_v659_v1_x1.py",
    "tests/test_ghc_family_v659_v1_x1.py",
]


def now_fields() -> dict[str, str]:
    utc = datetime.now(timezone.utc)
    # This Windows host is configured for New Zealand time. Using the host's
    # local conversion avoids an optional tzdata dependency while preserving
    # an offset-bearing, auditable timestamp.
    nz = utc.astimezone()
    return {"recorded_at_utc": utc.isoformat(), "recorded_at_nz": nz.isoformat()}


def write_json(relative: str, payload: Any, *, compact: bool = False) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":") if compact else None,
        indent=None if compact else 2,
    )
    path.write_text(text + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(ROOT), *args], text=True, encoding="utf-8"
    ).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(git_clean_bytes(path)).hexdigest()


def git_clean_bytes(path: Path) -> bytes:
    """Return the declared textual Git-clean domain used by phase manifests."""
    return path.read_bytes().replace(b"\r\n", b"\n")


def title_tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.lower()))


def jaccard(left: set[str], right: set[str]) -> float:
    return len(left & right) / len(left | right) if left or right else 1.0


def prior_chain_rows() -> list[dict[str, str]]:
    prior = load_json(PRIOR_INDEX)
    rows = [*prior["prior_proposals"], *prior["new_proposals"]]
    if len(rows) != d.PRIOR_FROZEN:
        raise RuntimeError(f"prior chain count drift: {len(rows)}")
    return rows


def proposal_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    prior_ledger = load_json(PRIOR_LEDGER)["proposals"]
    if len(prior_ledger) != 40:
        raise RuntimeError("source Lyren remaster proposal ledger is not the expected 40 rows")

    selected: list[dict[str, Any]] = []
    for index, source in enumerate(prior_ledger[: d.SELECTED_INHERITED_COUNT], 1):
        if source["expected_disposition"] != "completed":
            raise RuntimeError("the selected inherited tranche must remain completed-only")
        selected.append(
            {
                **source,
                "proposal_id": f"{d.PHASE_CODE}-P{index:03d}",
                "slug": f"selected-{source['slug']}",
                "origin": "selected_inherited_from_frozen_2910",
                "source_proposal_id": source["proposal_id"],
                "source_slug": source["slug"],
                "selection_rank": index,
                "append_to_frozen_chain": False,
                "current_scope": "same-owner bounded revalidation; not independent reproduction",
            }
        )

    new: list[dict[str, Any]] = []
    for offset, spec in enumerate(d.NEW_PROPOSAL_SPECS, 21):
        new.append(
            {
                "proposal_id": f"{d.PHASE_CODE}-P{offset:03d}",
                "slug": spec["slug"],
                "title": spec["title"],
                "origin": "new_unique_v659_v1_proposal",
                "append_to_frozen_chain": True,
                "expected_disposition": spec["outcome"],
                "pillar_relation": spec["pillar"],
                "mechanism": spec["mechanism"],
                "hypothesis": (
                    f"A bounded {spec['mechanism']} contract can expose falsifiable synthetic obligations "
                    "without promoting software structure into empirical, professional, production, legal, cultural, Māori-authority, identity, or Stage 20 evidence."
                ),
                "null_or_failure_condition": (
                    f"The artifact omits or contradicts {spec['mechanism']}, accepts a frozen mutation, "
                    "erases a failure, or crosses a protected authority or real-world gate."
                ),
                "falsifier_or_acceptance_gate": (
                    "One declared synthetic fixture must pass and five preregistered mutations must be rejected; "
                    "the receipt receives no real-world, authority, independent-reproduction, or Stage 20 credit."
                ),
                "approval_class": "safe_now_bounded_synthetic_or_structural",
                "execution_lane": "x2_owner_local_bounded_synthetic",
                "official_or_primary_source_needs": spec["sources"],
                "protected_gates": d.PROTECTED_GATES,
                "rollback_or_recovery": (
                    "Stop, retain the failed witness at zero credit, rewrite no history, and leave people, "
                    "businesses, production state, sibling lanes, external systems, rights, and authority unchanged."
                ),
                "concrete_artifacts": [
                    f"surfaces/{spec['slug']}/contract.json",
                    f"surfaces/{spec['slug']}/mutation-results.json",
                    f"surfaces/{spec['slug']}/bounded-receipt.json",
                ],
            }
        )

    all_rows = [*selected, *new]
    counts = Counter(row["expected_disposition"] for row in all_rows)
    if dict(counts) != d.EXPECTED_DISTRIBUTION:
        raise RuntimeError(f"proposal distribution drift: {dict(counts)}")
    if len(all_rows) != d.CURRENT_PORTFOLIO_COUNT:
        raise RuntimeError("current proposal portfolio count drift")
    return selected, new, all_rows


def novelty_audit(selected: list[dict[str, Any]], new: list[dict[str, Any]]) -> dict[str, Any]:
    inherited = prior_chain_rows()
    inherited_token_rows = [(row["proposal_id"], row["title"], title_tokens(row["title"])) for row in inherited]
    new_results: list[dict[str, Any]] = []
    for row in new:
        tokens = title_tokens(row["title"])
        candidates = [
            (jaccard(tokens, prior_tokens), prior_id, prior_title)
            for prior_id, prior_title, prior_tokens in inherited_token_rows
        ]
        score, prior_id, prior_title = max(candidates, key=lambda item: item[0])
        new_results.append(
            {
                "proposal_id": row["proposal_id"],
                "inherited_titles_checked": len(inherited),
                "max_token_jaccard": round(score, 6),
                "nearest_prior_proposal_id": prior_id,
                "nearest_prior_title": prior_title,
                "passes_bounded_threshold": score < NOVELTY_THRESHOLD,
            }
        )
    selected_results = [
        {
            "proposal_id": row["proposal_id"],
            "source_proposal_id": row["source_proposal_id"],
            "selection_exact_match_expected": True,
            "append_to_frozen_chain": False,
        }
        for row in selected
    ]
    return {
        "schema": "ghc.family.proposal-selection-novelty-audit.v1",
        "prior_title_count": len(inherited),
        "selected_inherited_count": len(selected_results),
        "new_unique_count": len(new_results),
        "new_title_threshold": NOVELTY_THRESHOLD,
        "selected_inherited_results": selected_results,
        "new_unique_results": new_results,
        "all_new_titles_pass": all(row["passes_bounded_threshold"] for row in new_results),
        "boundary": "Token overlap is a bounded screen plus mechanism review, not universal semantic novelty proof.",
    }


def source_verification() -> dict[str, Any]:
    head = git("rev-parse", "HEAD")
    branch = git("branch", "--show-current")
    source_parent = git("show", "-s", "--format=%P", d.SOURCE_FINAL).split()
    source_tree = git("rev-parse", f"{d.SOURCE_FINAL}^{{tree}}")
    source_tracking = git("rev-parse", f"refs/remotes/origin/{d.SOURCE_BRANCH}")
    if head != d.SOURCE_FINAL or branch != d.BRANCH or source_tracking != d.SOURCE_FINAL:
        raise RuntimeError("source branch, head, or tracking ref drift")
    return {
        "schema": "ghc.family.source-verification.v1",
        "owner": d.OWNER,
        "phase": d.PHASE,
        "branch": branch,
        "head_before_x1": head,
        "source_branch": d.SOURCE_BRANCH,
        "source_final": d.SOURCE_FINAL,
        "source_parent_count": len(source_parent),
        "source_tree": source_tree,
        "source_tracking_equal": source_tracking == d.SOURCE_FINAL,
        "fresh_live_equality_witness": "verified externally before worktree creation",
        "source_clean_witness": "verified before additive worktree creation",
        "same_owner_only": True,
        "independent_reproduction": False,
        **now_fields(),
    }


def method_flow() -> dict[str, Any]:
    methods: list[dict[str, Any]] = []
    witnesses: list[dict[str, Any]] = []
    state_events: list[dict[str, Any]] = []
    recommendations: list[dict[str, Any]] = []
    passing_recoveries = 0
    candidate_recoveries = 0
    for index, failure in enumerate(d.STARTUP_FAILURES, 1):
        negative_id = str(failure["negative_id"])
        signature = str(failure["signature"])
        recovery = str(failure["recovery"])
        recovery_passed = bool(failure["recovery_passed"])
        method_id = f"{d.PHASE_CODE}-X1-METHOD-{index:03d}"
        fail_id = f"{method_id}-F"
        pass_id = f"{method_id}-P"
        validation_witness_ids = [fail_id, pass_id] if recovery_passed else [fail_id]
        recommendation_state = "preferred" if recovery_passed else "candidate"
        methods.append(
            {
                "method_id": method_id,
                "title": f"Bounded recovery for {signature}",
                "failure_signature": signature,
                "trigger_preconditions": [signature],
                "privacy_class": "sanitized_public",
                "approval_class": "safe_now_owner_local_recovery",
                "candidate_workaround": recovery,
                "validation_witness_ids": validation_witness_ids,
                "recurrence_guard": recovery,
                "rollback": "Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.",
                "recommendation_state": recommendation_state,
                "supersedes": [],
                "protected_gates": d.PROTECTED_GATES,
                "retained_negative_ids": [negative_id],
                "scope_boundary": "Same-owner bounded workflow recovery only.",
            }
        )
        witnesses.append(
            {
                "witness_id": fail_id,
                "method_id": method_id,
                "procedure": f"Attempt the original method associated with {signature}.",
                "scope": "startup and workflow planning",
                "expected": "The bounded startup postcondition is established.",
                "observed": f"{signature}; zero credit and no repository mutation attributable to the failed method.",
                "result": "fail",
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": [negative_id],
                "boundary": "The failed witness remains retained.",
            }
        )
        if recovery_passed:
            passing_recoveries += 1
            witnesses.append(
                {
                    "witness_id": pass_id,
                    "method_id": method_id,
                    "procedure": recovery,
                    "scope": "the declared recovered postcondition only",
                    "expected": "Only the bounded recovered postcondition is established.",
                    "observed": "The corrected bounded witness passed without erasing the failure or expanding authority.",
                    "result": "pass",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "retained_negative_ids": [negative_id],
                    "boundary": "Same-owner workflow validation only.",
                }
            )
            state_events.extend(
                [
                    {"method_id": method_id, "from": "candidate", "to": "validated", "witness_id": pass_id},
                    {"method_id": method_id, "from": "validated", "to": "preferred", "witness_id": pass_id},
                ]
            )
        else:
            candidate_recoveries += 1
        recommendations.append(
            {
                "method_id": method_id,
                "precondition": signature,
                "preferred_method": recovery if recovery_passed else None,
                "candidate_method": None if recovery_passed else recovery,
            }
        )
    return {
        "schema": "ghc.family.method-flow-state.v1",
        "phase": d.PHASE,
        "owner": d.OWNER,
        "identity_boundary": "Relational working language only; no continuity, personhood, qualification, authority, or agency claim.",
        "methods": methods,
        "witnesses": witnesses,
        "state_events": state_events,
        "recommendations": recommendations,
        "counts": {
            "methods": len(methods),
            "witnesses": len(witnesses),
            "state_events": len(state_events),
            "recommendations": len(recommendations),
            "states": {
                "observed": 0,
                "candidate": candidate_recoveries,
                "validated": 0,
                "preferred": passing_recoveries,
                "superseded": 0,
                "deprecated": 0,
            },
            "witness_results": {"pass": passing_recoveries, "fail": len(methods)},
        },
        "cumulative_counts": {
            "activation_methods": d.ACTIVATION_METHODS,
            "current_methods": len(methods),
            "effective_methods": d.ACTIVATION_METHODS + len(methods),
            "current_failed_witnesses": len(methods),
            "current_passing_witnesses": passing_recoveries,
        },
        "boundary": "Same-owner workflow evidence only; no independent reproduction or protected-gate closure.",
    }


def source_ledger() -> tuple[dict[str, Any], str]:
    rows = [
        {
            "source_id": source_id,
            "source_label": label,
            "url": url,
            "phase_implication": implication,
            "privacy_boundary": "Public source vocabulary only; no raw browsing dump or private state.",
        }
        for source_id, label, url, implication in d.OFFICIAL_SOURCES
    ]
    payload = {
        "schema": "ghc.family.source-reflection-ledger.v1",
        "owner": d.OWNER,
        "phase": d.PHASE,
        "row_count": len(rows),
        "rows": rows,
        "boundary": "Sources support vocabulary and reservation design only; they confer no compliance, professional competence, legal or cultural authority, Māori authority, or empirical result.",
    }
    lines = ["# Official and primary source reflection ledger", "", payload["boundary"], "", "| ID | Label | Phase implication |", "|---|---|---|"]
    lines.extend(f"| {row['source_id']} | {row['source_label']} | {row['phase_implication']} |" for row in rows)
    return payload, "\n".join(lines)


def overview(proposals: list[dict[str, Any]]) -> str:
    lines = [
        "# Ilyra Fen v659-v1 x1 overview",
        "",
        "## Relational identity and evidence ceiling",
        "",
        f"{d.OWNER} ({d.PRONOUNS}) is relational working language for this task. Their working role is {d.ROLE}. Their hope is to {d.HOPE}. This language is not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, or independent agency. Hamish may pause, rename, redirect, or stop the route.",
        "",
        f"The primary pillar is {d.PRIMARY_PILLAR}; THOS Body and Freed ID/CBR Heart remain explicit. The bounded practice lens is {d.PRACTICE_LENS}. This is same-owner synthetic software work, not an observatory, scientific instrument, archive, safety service, identity authority, or deployment. It uses zero real observers, operators, telescopes, detectors, observations, images, catalogues, alerts, measurements, credentials, or protected participant data. Every empirical, participant, professional, production, deployment, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, and Stage 20 boundary stays open.",
        "",
        "## Immutable additive source and route arithmetic",
        "",
        f"The lane starts from Lyren's clean, four-way-equal remaster final `{d.SOURCE_FINAL}` on `{d.SOURCE_BRANCH}`. The acknowledged live route makes Ilyra the sole v659-v1 owner. Ilyra's exact next edge is the existing main task `Auren Lark` for `v659-v2`; Sable and Tavian are not substitute endpoints.",
        "",
        "Strict x1-before-x2 applies. This x1 packet freezes planning, selections, novel proposals, source reflections, safe validation tasks, Auren seeds, tool plans, cleanup plans, failures, truth labels, wellbeing, and validation receipts only. It contains no v659-v1 surface implementation, mutation outcome, x2 runner, observed proposal outcome, closeout, final seal, or successor message.",
        "",
        "## Forty-proposal selection and append-only chain",
        "",
        f"All {d.PRIOR_FROZEN:,} inherited proposal titles are parsed. Twenty completed proposals from Lyren's immutable remaster packet are selected for same-owner bounded revalidation; they are not re-appended or misrepresented as novel. Twenty genuinely new observatory-domain proposals are audited against all inherited titles using a disclosed token-set Jaccard screen below {NOVELTY_THRESHOLD:.2f}, then reviewed by mechanism. Only those twenty new rows extend the append-only frozen chain, from {d.PRIOR_FROZEN:,} to {d.PRIOR_FROZEN + d.NEW_UNIQUE_COUNT:,}. The current portfolio contains forty rows with expected labels 33 completed, 5 represented, 1 open_gap, and 1 exact_gate.",
        "",
        "| Current ID | Origin | Expected truth | Title |",
        "|---|---|---|---|",
    ]
    for row in proposals:
        lines.append(f"| {row['proposal_id']} | {row['origin']} | {row['expected_disposition']} | {row['title']} |")
    lines.extend(
        [
            "",
            "## Approval, tooling, and cleanup portfolios",
            "",
            "Thirty Ilyra safe-now validation tasks execute in x1 through the concrete source, proposal, workflow, privacy, manifest, truth, boundary, and portfolio checks represented by this packet. Ten reversible candidate prototypes are frozen for x2. Ten exact-approval rows and five blocked rows remain visible and unexecuted. Twenty Auren safe seeds and ten Auren candidate seeds are recommendations only; Ilyra does not execute work in Auren's lane.",
            "",
            "Ten Ilyra family-current skill designs and ten family-current runner designs are frozen for x2 build, smoke-test, and use. Ten Auren skill ideas and five Auren runner ideas remain seeds only. Thirty additive Ilyra CLEAN/FIX/REFINE reviews are planned for x2 and thirty Auren reviews remain future recommendations. No cleanup quota authorizes deletion, cache purging, worktree removal, history rewriting, global downgrade, plugin-cache mutation, or sibling-owned changes.",
            "",
            "## Latest-5,000 tracked-file scan contract",
            "",
            "The requested repository scan is capped at 5,000 tracked paths. X2 will select paths by first appearance while traversing commits newest-first, with deterministic lexical ordering inside each commit and duplicate suppression. The receipt will distinguish eligible tracked files, selected files, and exclusions. The cap is a bounded operational scope, not exhaustive security, complete privacy, or proof about all repository bytes. The current owner packet and exact final diff will also receive their own complete owner-scoped checks.",
            "",
            "## Source and authority discipline",
            "",
            "NASA/IAU FITS, IVOA, IAU SOFA, IERS, NIST, W3C, the New Zealand Privacy Commissioner, Te Mana Raraunga, Git, Python, and IETF materials provide vocabulary and design implications only. They do not confer format conformance, observing or safety authority, professional competence, cultural ratification, Māori authority, privacy completeness, accessibility completeness, production readiness, or scientific confirmation.",
            "",
            "The immediate route is terminally gated. No task lookup, reread, contact, creation, fork, delegation, or substitute endpoint is permitted during x1 or x2 evidence construction. After the exact final is pushed, clean, four-way equal, within caps, and Ilyra's attributable exact-final canonical aggregate succeeds once, Ilyra may resolve the unique exact-title `Auren Lark` task, reread it immediately, and send one sanitized file-backed `v659-v2` activation. A normal acknowledged tool return is sufficient; no second confirmation may be sent. Tavian Sol remains ON_STANDBY.",
            "",
            "## Terminal truth",
            "",
            "The phase remains `NOT_READY_FOR_STAGE_20`. Same-owner synthetic validation is not independent reproduction. A completed contract proves only its bounded declared software behavior; a represented artifact remains a proxy; an open gap remains missing evidence or transport; an exact gate remains unexecuted authority-sensitive work.",
        ]
    )
    return "\n".join(lines)


def phase_files() -> list[Path]:
    return sorted(path for path in PHASE.rglob("*") if path.is_file())


def normalize_phase_text_line_endings() -> None:
    """Make working-byte and Git-blob hashes stable on Windows."""
    text_suffixes = {".json", ".jsonl", ".md", ".txt", ".html", ".csv", ".yaml", ".yml"}
    for path in phase_files():
        if path.suffix.lower() not in text_suffixes:
            continue
        text = path.read_text(encoding="utf-8")
        normalized = text.replace("\r\n", "\n").replace("\r", "\n")
        path.write_text(normalized, encoding="utf-8", newline="\n")


def privacy_scan() -> dict[str, Any]:
    patterns = {
        "raw_uuid": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/]"),
        "credential": re.compile(r"(?:(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}|(?<![A-Za-z0-9])ghp_[A-Za-z0-9]{20,}|BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY)"),
        "private_route_identifier": re.compile(
            r"(?:thread_id|task_id|agent_id|resume_token|private_callable)[\"']?\s*[:=]\s*[\"']?"
            r"(?!(?:V\d|false\b|true\b|null\b|\[REDACTED_SECRET\]))[A-Za-z0-9_-]{24,}",
            re.I,
        ),
        "transcript_or_session": re.compile(r"(?:raw transcript|session stream|private app state)", re.I),
    }
    hits: list[dict[str, str]] = []
    scanned = 0
    for path in phase_files():
        relative = path.relative_to(PHASE).as_posix()
        if relative == "validation/x1-privacy-scan.json":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        scanned += 1
        for label, pattern in patterns.items():
            if pattern.search(text):
                hits.append({"path": relative, "class": label})
    return {
        "schema": "ghc.family.privacy-scan.v1",
        "scope": "complete current Ilyra v659-v1 x1 owner packet",
        "files_scanned": scanned,
        "classes": list(patterns),
        "confirmed_hits": hits,
        "confirmed_hit_count": len(hits),
        "privacy_complete": False,
        "boundary": "Five-class owner-packet scanning is bounded evidence, not complete privacy or exhaustive security assurance.",
    }


def content_manifest() -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    for path in phase_files():
        relative = path.relative_to(PHASE).as_posix()
        if relative in MANIFEST_EXCLUSIONS:
            continue
        payload = git_clean_bytes(path)
        entries.append({"path": f"{d.PHASE_ROOT}/{relative}", "sha256": hashlib.sha256(payload).hexdigest(), "bytes": len(payload)})
    for relative in X1_CODE:
        path = ROOT / relative
        payload = git_clean_bytes(path)
        entries.append({"path": relative, "sha256": hashlib.sha256(payload).hexdigest(), "bytes": len(payload)})
    return {
        "schema": "ghc.family.content-manifest.v2",
        "phase": d.PHASE,
        "lifecycle": "x1_precommit_candidate",
        "entry_count": len(entries),
        "entries": sorted(entries, key=lambda row: row["path"]),
        "exclusions": sorted(MANIFEST_EXCLUSIONS),
        "hash_domain": "text bytes after CRLF-to-LF Git-clean normalization",
        "boundary": "Exact declared Git-clean-equivalent inventory for listed text files only; self-referential validation files are declared exclusions.",
    }


def document_cap() -> dict[str, Any]:
    rows = []
    total = 0
    for path in phase_files():
        if path.suffix.lower() not in {".md", ".html", ".txt"}:
            continue
        words = len(re.findall(r"\b\w+\b", path.read_text(encoding="utf-8", errors="replace")))
        rows.append({"path": path.relative_to(PHASE).as_posix(), "words": words})
        total += words
    return {"schema": "ghc.family.document-cap.v1", "documents": rows, "document_count": len(rows), "total_words": total, "cap": 100000, "passes": total <= 100000}


def build() -> None:
    PHASE.mkdir(parents=True, exist_ok=True)
    selected, new, proposals = proposal_rows()
    novelty = novelty_audit(selected, new)
    if not novelty["all_new_titles_pass"]:
        raise RuntimeError("one or more new proposal titles failed the bounded novelty screen")

    source = source_verification()
    write_json("startup/source-verification.json", source)
    c_usage = shutil.disk_usage("C:\\")
    d_usage = shutil.disk_usage("D:\\")
    write_json(
        "startup/environment-and-toolchain.json",
        {
            "schema": "ghc.family.environment-receipt.v1",
            "codex_cli": "codex-cli 0.146.0",
            "node": "v24.18.0",
            "python": "Python 3.12.10",
            "git": "git version 2.55.0.windows.2",
            "c_free_gb": round(c_usage.free / 1024**3, 2),
            "d_free_gb": round(d_usage.free / 1024**3, 2),
            "primary_storage_bank": "D",
            "c_drive_use": "essential global skill and roster metadata only",
            "desktop_app_mutated": False,
            **now_fields(),
        },
    )
    write_json(
        "identity/identity-and-boundary.json",
        {
            "schema": "ghc.family.relational-identity-boundary.v1",
            "name": d.OWNER,
            "pronouns": d.PRONOUNS,
            "role": d.ROLE,
            "hope": d.HOPE,
            "boundary": "Relational working language only; not consciousness, sentience, personhood, continuity, employment, qualification, authority, or independent agency.",
        },
    )
    write_json(
        "workflow/live-workflow-plan.json",
        {
            "schema": "ghc.family.workflow-plan.phase.v1",
            "owner": d.OWNER,
            "phase": d.PHASE,
            "interstitial_variant": False,
            "changes_canonical_phase_arithmetic": False,
            "proposal_mix": {"selected_inherited": 20, "new_unique": 20, "current_total": 40, "frozen_chain_growth": 20},
            "latest_tracked_file_scan_cap": d.LATEST_TRACKED_SCAN_CAP,
            "commit_cap": {"x1": 1, "x2_and_closeout": 3, "total": 4},
            "canonical_validation": "one complete successful exact-final pass; no replay after success",
            "current_owner": {"title": "Ilyra Fen", "phase": "v659-v1", "endpoint_kind": "main_task"},
            "terminal_successor": {"title": "Auren Lark", "phase": "v659-v2", "endpoint_kind": "main_task"},
            "recipient_next_edge": {"title": "Sable Rook", "phase": "v659-v3", "controller": "Auren Lark"},
            "tavian_sol_state": "ON_STANDBY",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "preregistration/proposal-ledger.json",
        {
            "schema": "ghc.family.proposal-ledger.x1.v1",
            "owner": d.OWNER,
            "phase": d.PHASE,
            "proposal_count": len(proposals),
            "selected_inherited_count": len(selected),
            "new_unique_count": len(new),
            "expected_disposition_counts": d.EXPECTED_DISTRIBUTION,
            "outcomes_observed": False,
            "proposals": proposals,
        },
    )
    proposal_lines = ["# Frozen Ilyra v659-v1 proposal ledger", "", "X1 contains expected dispositions only; no x2 outcome is observed here.", "", "| ID | Origin | Expected | Title |", "|---|---|---|---|"]
    proposal_lines.extend(f"| {row['proposal_id']} | {row['origin']} | {row['expected_disposition']} | {row['title']} |" for row in proposals)
    write_text("preregistration/proposal-ledger.md", "\n".join(proposal_lines))
    write_json("provenance/selection-and-novelty-audit.json", novelty)
    prior = prior_chain_rows()
    write_json(
        "provenance/frozen-chain-proposal-index.json",
        {
            "schema": "ghc.family.frozen-chain-proposal-index.v1",
            "prior_count": len(prior),
            "selected_inherited_count": len(selected),
            "selected_inherited": [{"current_proposal_id": row["proposal_id"], "source_proposal_id": row["source_proposal_id"], "title": row["title"]} for row in selected],
            "new_count": len(new),
            "effective_count": len(prior) + len(new),
            "prior_proposals": prior,
            "new_proposals": [{"proposal_id": row["proposal_id"], "title": row["title"]} for row in new],
            "selection_rows_reappended": 0,
        },
        compact=True,
    )
    portfolios = {
        "schema": "ghc.family.phase-task-portfolios.x1.v1",
        "task_cap": 1000,
        "counts": {
            "ilyra_safe_executed_x1": len(d.SELF_SAFE_TASKS),
            "auren_safe_seeds": len(d.AUREN_SAFE_SEEDS),
            "ilyra_candidate_planned_x2": len(d.SELF_CANDIDATE_TASKS),
            "auren_candidate_seeds": len(d.AUREN_CANDIDATE_SEEDS),
            "ilyra_exact_queued": len(d.EXACT_QUEUE),
            "ilyra_blocked_queued": len(d.BLOCKED_QUEUE),
        },
        "ilyra_safe": [{**row, "state": "completed_x1_validation_only"} for row in d.SELF_SAFE_TASKS],
        "auren_safe_seeds": d.AUREN_SAFE_SEEDS,
        "ilyra_candidate": [{**row, "state": "frozen_for_x2"} for row in d.SELF_CANDIDATE_TASKS],
        "auren_candidate_seeds": d.AUREN_CANDIDATE_SEEDS,
        "exact_queue": d.EXACT_QUEUE,
        "blocked_queue": d.BLOCKED_QUEUE,
        "boundary": "Ilyra executes only owner-local rows; Auren rows are seeds, while exact and blocked rows remain unexecuted.",
    }
    write_json("preregistration/task-portfolios.json", portfolios)
    write_json(
        "preregistration/skill-and-runner-plan.json",
        {
            "schema": "ghc.family.skill-runner-plan.x1.v1",
            "ilyra_skills": [{"name": name, "purpose": purpose, "state": "frozen_for_x2_build_test_use"} for name, purpose in d.SELF_SKILL_SPECS],
            "auren_skill_seeds": d.AUREN_SKILL_SEEDS,
            "ilyra_runners": [{"name": name, "surface": surface, "state": "frozen_for_x2_build_test_use"} for name, surface in d.SELF_RUNNER_SPECS],
            "auren_runner_seeds": d.AUREN_RUNNER_SEEDS,
            "counts": {"ilyra_skills": 10, "auren_skill_seeds": 10, "ilyra_runners": 10, "auren_runner_seeds": 5},
            "implemented_in_x1": False,
        },
    )
    write_json(
        "preregistration/clean-fix-refine-plan.json",
        {
            "schema": "ghc.family.clean-fix-refine-plan.x1.v1",
            "ilyra_rows": d.SELF_CLEAN_TASKS,
            "auren_seed_rows": d.AUREN_CLEAN_SEEDS,
            "counts": {"ilyra_planned_x2": 30, "auren_seed_only": 30, "total_planned": 60},
            "deletion_authorized": False,
            "boundary": "Additive review and refinement only; no deletion, reset, purge, worktree removal, sibling mutation, or security weakening.",
        },
    )
    sources_json, sources_md = source_ledger()
    write_json("sources/official-source-ledger.json", sources_json)
    write_text("sources/official-source-ledger.md", sources_md)
    flow = method_flow()
    write_json("method-flow/method-flow-state-x1.json", flow)
    write_json(
        "truth/retained-negative-register-x1.json",
        {
            "schema": "ghc.family.retained-negative-register.v1",
            "activation_baseline": d.ACTIVATION_NEGATIVES,
            "current_negatives": [
                {
                    "negative_id": row["negative_id"],
                    "signature": row["signature"],
                    "credit": 0,
                    "recovery": row["recovery"],
                    "recovery_passed": row["recovery_passed"],
                }
                for row in d.STARTUP_FAILURES
            ],
            "effective_negatives": d.ACTIVATION_NEGATIVES + len(d.STARTUP_FAILURES),
            "all_failures_retained": True,
        },
    )
    write_json(
        "truth/x1-phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.x1.v1",
            "owner": d.OWNER,
            "phase": d.PHASE,
            "lifecycle": "x1_frozen_candidate",
            "source_final": d.SOURCE_FINAL,
            "prior_frozen": d.PRIOR_FROZEN,
            "selected_inherited": 20,
            "new_unique_frozen": 20,
            "effective_frozen": d.PRIOR_FROZEN + 20,
            "expected_outcomes": d.EXPECTED_DISTRIBUTION,
            "outcomes_observed": False,
            "effective_negatives": d.ACTIVATION_NEGATIVES + len(d.STARTUP_FAILURES),
            "effective_methods": d.ACTIVATION_METHODS + len(d.STARTUP_FAILURES),
            "effective_open_gaps": d.SOURCE_OPEN_GAPS,
            "effective_exact_gates": d.SOURCE_EXACT_GATES,
            "route_state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "same_owner_only": True,
            "independent_reproduction": False,
        },
    )
    write_json(
        "orchestration/route-state-x1.json",
        {
            "schema": "ghc.family.route-state.x1.v1",
            "owner": d.OWNER,
            "phase": d.PHASE,
            "state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "current_exact_title": "Ilyra Fen",
            "current_phase": "v659-v1",
            "next_endpoint_kind": "main_task",
            "next_exact_title": "Auren Lark",
            "next_phase": "v659-v2",
            "recipient_next_exact_title": "Sable Rook",
            "recipient_next_phase": "v659-v3",
            "task_lookup_performed": False,
            "message_sent": False,
            "task_created": False,
            "task_forked": False,
            "subagent_spawned": False,
            "tavian_sol_state": "ON_STANDBY",
        },
    )
    write_json(
        "wellbeing/workload-check-x1.json",
        {
            "schema": "ghc.family.workload-check.v1",
            "owner": d.OWNER,
            "phase": d.PHASE,
            "solo": True,
            "delegated": False,
            "subagents": 0,
            "proposal_portfolio": 40,
            "new_build_surfaces": 20,
            "selected_revalidation_surfaces": 20,
            "latest_file_scan_cap": 5000,
            "commit_cap": 4,
            "checkpoint_overrun_allowed": True,
            "pause_redirect_stop_right_preserved": True,
            "boundary": "A workload check is operational care language, not consciousness, health, employment, or clinical evidence.",
            **now_fields(),
        },
    )
    write_json(
        "tooling/skill-applicability-x1.json",
        {
            "schema": "ghc.family.skill-applicability.x1.v1",
            "owner": d.OWNER,
            "phase": d.PHASE,
            "used_with_bounded_receipt": [
                "ghc-family-index",
                "ghc-family-reflection-remaster",
                "ghc-family-method-flow-state",
                "ghc-family-roster-check",
                "ghc-family-workflow-plan-refinement",
            ],
            "guidance_applied_without_mutating_legacy_mini_root": [
                "ghc-main-compact-restart-builder",
                "ghc-main-closeout-builder",
                "ghc-main-retry",
                "ghc-open-gate-rail",
                "ghc-full-tools-skill-bank",
                "ghc-watcher-notifier-cadence",
            ],
            "current_auth_state_read": True,
            "current_roster_state_read": True,
            "governance_preflight": {
                "state": "candidate_recovery_required_before_x2_credit",
                "failed_witness_retained": "V6591-X1-N002",
                "failure": "current acknowledged-active route state is not yet accepted by the family roster validator",
                "proposed_additive_recovery": "align the checker and schema without weakening exact-title, endpoint-kind, or single-successor constraints",
                "passing_witness_present": False,
            },
            "boundary": "Skill use and applicability review is same-owner workflow evidence only; it grants no authority, independent reproduction, protected-gate closure, or permission to mutate inherited lanes.",
        },
    )
    write_json(
        "security/threat-model-x1.json",
        {
            "schema": "ghc.family.threat-model.v1",
            "assets": ["frozen proposals", "synthetic fixtures", "retained failures", "manifests", "sanitized route baton"],
            "threats": ["private material publication", "stale route mutation", "truth-label promotion", "mutation witness erasure", "destructive cleanup", "sibling-lane mutation"],
            "controls": ["D-first owner lane", "x1-before-x2", "five-class privacy scan", "append-only Method Flow", "exact staged review", "terminal-gated one-shot send"],
            "residual_gaps": ["privacy completeness", "accessibility completeness", "exhaustive security", "independent review", "production assessment"],
            "security_complete": False,
        },
    )
    write_text("deliverables/v659-v1-x1-overview.md", overview(proposals))

    normalize_phase_text_line_endings()
    write_json("validation/x1-privacy-scan.json", privacy_scan())
    write_json("validation/x1-document-cap.json", document_cap())
    write_json("validation/x1-content-manifest.json", content_manifest())
    # Recompute bounded receipts after their own materialization; the manifest declares these self-reference exclusions.
    write_json("validation/x1-privacy-scan.json", privacy_scan())
    write_json("validation/x1-document-cap.json", document_cap())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true", help="Rebuild the same x1-only packet after external family tooling outputs are added.")
    parser.parse_args()
    build()
    result = {
        "phase": d.PHASE,
        "files": len(phase_files()),
        "proposals": 40,
        "selected_inherited": 20,
        "new_unique": 20,
        "effective_frozen": d.PRIOR_FROZEN + d.NEW_UNIQUE_COUNT,
        "x2_started": False,
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
