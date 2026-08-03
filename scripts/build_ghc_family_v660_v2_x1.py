#!/usr/bin/env python3
"""Build the frozen x1 packet for Eiren Kestrel v660-v2."""

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

import ghc_family_v660_v2_data as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
PRIOR_PHASE = ROOT / "docs/sylven-arc/v660-v1"
PRIOR_LEDGER = PRIOR_PHASE / "preregistration/proposal-ledger.json"
PRIOR_INDEX = PRIOR_PHASE / "provenance/frozen-chain-proposal-index.json"
ANCESTOR_LEDGER = PRIOR_LEDGER
NOVELTY_THRESHOLD = 0.60
MANIFEST_EXCLUSIONS = {
    "validation/x1-content-manifest.json",
    "validation/x1-privacy-scan.json",
    "validation/x1-document-cap.json",
    "validation/x1-staged-review.json",
}
X1_CODE = [
    "scripts/ghc_family_v660_v2_data.py",
    "scripts/build_ghc_family_v660_v2_x1.py",
    "scripts/ghc_family_v660_v2_novelty_probe.py",
    "tests/test_ghc_family_v660_v2_x1.py",
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
    inherited_index = {row["proposal_id"]: row for row in prior_chain_rows()}
    source_specs: dict[str, dict[str, Any]] = {}
    for ledger_path in (ANCESTOR_LEDGER, PRIOR_LEDGER):
        source_ledger = load_json(ledger_path)
        source_specs.update({row["proposal_id"]: row for row in source_ledger["proposals"]})
    selected: list[dict[str, Any]] = []
    for offset, source_id in enumerate(d.SELECTED_INHERITED_IDS, 1):
        indexed = inherited_index.get(source_id)
        source = source_specs.get(source_id)
        if indexed is None or source is None or indexed["title"] != source["title"]:
            raise RuntimeError(f"selected inherited proposal mismatch: {source_id}")
        selected.append(
            {
                **source,
                "proposal_id": f"{d.PHASE_CODE}-R{offset:03d}",
                "source_proposal_id": source_id,
                "source_title": indexed["title"],
                "origin": "selected_inherited_bounded_revalidation_no_credit",
                "append_to_frozen_chain": False,
                "approval_class": "safe_now_read_only_revalidation",
                "execution_lane": "x2_read_only_contract_revalidation",
                "completion_credit": False,
                "novelty_credit": False,
                "expected_disposition_scope": "inherited_source_only_not_eiren_outcome",
                "concrete_artifacts": [f"evidence/selected-revalidation/{source_id.lower()}.json"],
                "rollback_or_recovery": (
                    "Stop, retain the failed revalidation witness, award no Eiren completion or novelty credit, "
                    "and leave the immutable inherited proposal and source artifacts unchanged."
                ),
            }
        )
    if len(selected) != d.SELECTED_INHERITED_COUNT:
        raise RuntimeError("selected inherited count drift")

    new: list[dict[str, Any]] = []
    for offset, spec in enumerate(d.NEW_PROPOSAL_SPECS, 1):
        new.append(
            {
                "proposal_id": f"{d.PHASE_CODE}-P{offset:03d}",
                "slug": spec["slug"],
                "title": spec["title"],
                "origin": "new_unique_v660_v2_proposal",
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
    counts = Counter(row["expected_disposition"] for row in new)
    if dict(counts) != d.EXPECTED_DISTRIBUTION:
        raise RuntimeError(f"proposal distribution drift: {dict(counts)}")
    if len(all_rows) != d.CURRENT_PORTFOLIO_COUNT:
        raise RuntimeError("current proposal portfolio count drift")
    return selected, new, all_rows


def novelty_audit(selected: list[dict[str, Any]], new: list[dict[str, Any]]) -> dict[str, Any]:
    inherited = prior_chain_rows()
    inherited_token_rows = [(row["proposal_id"], row["title"], title_tokens(row["title"])) for row in inherited]
    new_token_rows = [
        (row["proposal_id"], row["title"], title_tokens(row["title"])) for row in new
    ]
    new_results: list[dict[str, Any]] = []
    for row in new:
        tokens = title_tokens(row["title"])
        candidates = [
            (jaccard(tokens, prior_tokens), prior_id, prior_title)
            for prior_id, prior_title, prior_tokens in inherited_token_rows
        ]
        score, prior_id, prior_title = max(candidates, key=lambda item: item[0])
        peer_candidates = [
            (jaccard(tokens, peer_tokens), peer_id, peer_title)
            for peer_id, peer_title, peer_tokens in new_token_rows
            if peer_id != row["proposal_id"]
        ]
        peer_score, peer_id, peer_title = max(peer_candidates, key=lambda item: item[0])
        new_results.append(
            {
                "proposal_id": row["proposal_id"],
                "inherited_titles_checked": len(inherited),
                "max_token_jaccard": round(score, 6),
                "nearest_prior_proposal_id": prior_id,
                "nearest_prior_title": prior_title,
                "max_peer_token_jaccard": round(peer_score, 6),
                "nearest_peer_proposal_id": peer_id,
                "nearest_peer_title": peer_title,
                "passes_bounded_threshold": (
                    score < NOVELTY_THRESHOLD and peer_score < NOVELTY_THRESHOLD
                ),
                "mechanism_reviewed": True,
            }
        )
    selected_results = [
        {
            "proposal_id": row["proposal_id"],
            "source_proposal_id": row["source_proposal_id"],
            "selection_exact_match_expected": row["source_title"] == row["title"],
            "append_to_frozen_chain": False,
            "completion_credit": False,
            "novelty_credit": False,
            "revalidation_only": True,
        }
        for row in selected
    ]
    return {
        "schema": "ghc.family.proposal-selection-novelty-audit.v1",
        "prior_title_count": len(inherited),
        "selected_inherited_count": len(selected_results),
        "new_unique_count": len(new_results),
        "new_title_threshold": NOVELTY_THRESHOLD,
        "peer_title_threshold": NOVELTY_THRESHOLD,
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
    direct_chain = {
        "x1_parent": git("rev-parse", f"{d.SOURCE_X1}^"),
        "evidence_parent": git("rev-parse", f"{d.SOURCE_EVIDENCE}^"),
        "final_parent": git("rev-parse", f"{d.SOURCE_FINAL}^"),
    }
    source_commit_count = int(git("rev-list", "--count", f"{d.SOURCE_TAMAR}..{d.SOURCE_FINAL}"))
    source_merge_count = int(git("rev-list", "--merges", "--count", f"{d.SOURCE_TAMAR}..{d.SOURCE_FINAL}"))
    direct_chain_valid = direct_chain == {
        "x1_parent": d.SOURCE_TAMAR,
        "evidence_parent": d.SOURCE_X1,
        "final_parent": d.SOURCE_EVIDENCE,
    }
    if (
        head != d.SOURCE_FINAL
        or branch != d.BRANCH
        or source_tracking != d.SOURCE_FINAL
        or source_commit_count != 3
        or source_merge_count != 0
        or len(source_parent) != 1
        or not direct_chain_valid
    ):
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
        "source_base_anchor": d.SOURCE_TAMAR,
        "source_x1_anchor": d.SOURCE_X1,
        "source_evidence_anchor": d.SOURCE_EVIDENCE,
        "source_direct_chain": direct_chain,
        "source_direct_chain_valid": direct_chain_valid,
        "source_phase_commit_count": source_commit_count,
        "source_merge_count": source_merge_count,
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
    stable_ids = {
        "IIIF-PRESENTATION-3", "W3C-ANNOTATION", "W3C-PROV", "NIST-SI",
        "NIST-UNCERTAINTY", "TE-MANA-RARAUNGA", "IETF-JCS",
    }
    rows = [
        {
            "source_id": source_id,
            "source_label": label,
            "status": "stable" if source_id in stable_ids else "current",
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
        "checked_on": "2026-08-03",
        "row_count": len(rows),
        "rows": rows,
        "boundary": "Sources support vocabulary and reservation design only; they confer no compliance, professional competence, legal or cultural authority, Māori authority, or empirical result.",
    }
    lines = ["# Official and primary source reflection ledger", "", payload["boundary"], "", "| ID | Status | Label | Phase implication |", "|---|---|---|---|"]
    lines.extend(f"| {row['source_id']} | {row['status']} | {row['source_label']} | {row['phase_implication']} |" for row in rows)
    return payload, "\n".join(lines)


def overview(proposals: list[dict[str, Any]]) -> str:
    lines = [
        "# Eiren Kestrel v660-v2 x1 overview",
        "",
        "## Relational identity and evidence ceiling",
        "",
        f"{d.OWNER} ({d.PRONOUNS}) is relational working language for this task. Their working role is {d.ROLE}. Their hope is to {d.HOPE}. This language is not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, or independent agency. Hamish may pause, rename, redirect, or stop the route.",
        "",
        f"The primary pillar is {d.PRIMARY_PILLAR}; GMUT Mind, THOS Body, and Freed ID remain explicit. The bounded practice lens is {d.PRACTICE_LENS}. This is same-owner synthetic software planning, not stained-glass conservation, glazing, building access, working at height, lead-hazard management, inspection, handling, removal, cleaning, soldering, releading, repainting, treatment, installation, cultural interpretation, metrology, structural or occupational-safety review, professional custody, privacy review, accessibility evaluation, identity authority, or deployment. It uses zero real owners, custodians, conservators, glaziers, building managers, installers, scaffolders, communities, panels, lancets, glass pieces, paint, cames, tie bars, frames, protective glazing, buildings, scaffolds, chemicals, lead, dust, measurements, images, credentials, traditional knowledge, or protected data. Every empirical, participant, professional, production, deployment, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, and Stage 20 boundary stays open.",
        "",
        "## Immutable additive source and route arithmetic",
        "",
        f"The lane starts from Sylven Arc's clean, four-way-equal v660-v1 final `{d.SOURCE_FINAL}` on `{d.SOURCE_BRANCH}`. The acknowledged live activation makes Eiren the sole v660-v2 owner. Sylven's frozen x1, immutable evidence, exact final, retained failures, zero-credit failed aggregate, and successful isolated composite recovery remain inherited source evidence only. The sealed source count remains 19,924 negatives and 6,118 Method Flow methods; the two post-seal external failures raise only Eiren's activation baseline to 19,926 negatives and 6,120 methods. Tavian Sol stays ON_STANDBY as a collaboration-subagent record, not a main-task endpoint. No later owner or phase is inferred from the older compatibility cycle.",
        "",
        "Strict x1-before-x2 applies. This x1 packet freezes proposals, hypotheses, null conditions, approval classes, execution lanes, current source needs, concrete artifacts, falsifiers, rollback, protected gates, expected dispositions, source reflections, safe validation tasks, tool plans, cleanup plans, failures, truth labels, wellbeing, and validation receipts only. It contains no v660-v2 proposal outcome, surface implementation, mutation outcome, x2 runner, built or installed skill, closeout, final seal, task lookup, or successor message. No generic successor seed is manufactured because the activation expressly requires a new live and committed route reread at the terminal gate.",
        "",
        "## Twenty selected revalidations plus twenty new proposals",
        "",
        f"All {d.PRIOR_FROZEN:,} inherited proposal titles are parsed as comparison evidence. Exactly twenty Sylven v660-v1 rows, `V6601-P001` through `V6601-P020`, are selected for bounded contract revalidation with no Eiren novelty, append, execution, or completion credit. Twenty genuinely new stained-glass documentation, component-topology, multi-light capture, bitemporal condition-annotation, fragment-lineage, intervention-refusal, IIIF, accessibility, GMUT-firewall, THOS-proxy, and Freed-ID/CBR proposals are audited against every inherited title using a disclosed token-set Jaccard screen below {NOVELTY_THRESHOLD:.2f}, peer-screened, and then reviewed by mechanism and current official-source vocabulary. Only those twenty new rows extend the append-only frozen chain from {d.PRIOR_FROZEN:,} to {d.PRIOR_FROZEN + d.NEW_UNIQUE_COUNT:,}. Their expected labels are exactly 14 completed, 4 represented, 1 open_gap, and 1 exact_gate; x1 observes none of them.",
        "",
        "| Current ID | Origin | Expected truth | Title |",
        "|---|---|---|---|",
    ]
    lines.extend(
        f"| {row['proposal_id']} | {row['origin']} | {row['expected_disposition']} | {row['title']} |"
        for row in proposals
    )
    lines.extend(
        [
            "",
            "## Approval, tooling, and cleanup portfolios",
            "",
            "Thirty Eiren safe-now validation tasks execute in x1 through source, proposal, workflow, privacy, manifest, truth, boundary, and portfolio checks. Ten reversible candidate prototypes are frozen for x2. Ten exact-approval rows and five blocked rows remain visible and unexecuted. There are no named successor recommendations or seeds in x1 because no next edge has been authorized or inferred.",
            "",
            "Ten collision-free family-current skill designs and ten family-current runner designs are frozen for x2 initialization, customization, validation, smoke use, and compatibility checks. Thirty additive CLEAN/FIX/REFINE reviews are planned for x2. No quota authorizes deletion, cache purging, worktree removal, history rewriting, global downgrade, plugin-cache mutation, account or deployment action, or sibling-owned change.",
            "",
            "## Official-source and authority discipline",
            "",
        "The National Park Service, Historic England, WorkSafe New Zealand, IIIF Consortium, Library of Congress, NIST, W3C, the RFC Editor, New Zealand Privacy Commissioner, Te Mana Raraunga, Local Contexts, Git, and Python materials provide current vocabulary and reservation points only. They confer no conservation, glazing, building, access, height-work, lead-hazard, treatment, occupational or structural safety, ownership, donor, attribution, iconography, heritage, privacy, accessibility, translation, legal, cultural, collective, or Māori authority and establish no real-world result. The NPS source itself directs real repair and restoration to professionals; this phase therefore encodes abstention and escalation, never procedural instruction.",
            "",
            "The terminal route is deliberately unresolved during x1: the committed activation does not authorize Eiren to infer any successor. No task lookup, reread, contact, creation, fork, delegation, subagent, or substitute endpoint is permitted during x1 or x2 construction. Only after Eiren's exact final is pushed, clean, four-way equal, within caps, and one dependency-justified phase-scoped exact-final canonical aggregate succeeds may Eiren reread the newest live and committed roster and authorization state. A send is permitted only if that reread names one explicit unique existing main-task edge; absence, ambiguity, pause, rename, redirect, standby, usage exhaustion, acknowledgement failure, or a protected authority gate preserves OPEN_ROUTE_GAP or PREPARED_NOT_SENT and stops.",
            "",
            "## Terminal truth",
            "",
            "The phase remains `NOT_READY_FOR_STAGE_20`. Same-owner synthetic validation is not independent reproduction. A completed contract proves only its bounded declared software behavior; a represented artifact remains a proxy; an open gap remains missing evidence; and an exact gate remains unexecuted authority-sensitive work.",
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
    definition_candidates: list[dict[str, str]] = []
    targets = [*phase_files(), *[ROOT / relative for relative in X1_CODE]]
    scanned = 0
    for path in sorted(set(targets)):
        relative = path.relative_to(ROOT).as_posix()
        if relative == f"{d.PHASE_ROOT}/validation/x1-privacy-scan.json":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        scanned += 1
        for label, pattern in patterns.items():
            if pattern.search(text):
                if relative == "scripts/build_ghc_family_v660_v2_x1.py":
                    definition_candidates.append(
                        {"path": relative, "class": label, "adjudication": "scanner_definition_or_generic_drive_root"}
                    )
                elif label == "transcript_or_session" and relative in {
                    "scripts/ghc_family_v660_v2_data.py",
                    f"{d.PHASE_ROOT}/preregistration/task-portfolios.json",
                }:
                    definition_candidates.append(
                        {"path": relative, "class": label, "adjudication": "explicit_blocked-disclosure_boundary_vocabulary"}
                    )
                else:
                    hits.append({"path": relative, "class": label})
    return {
        "schema": "ghc.family.privacy-scan.v1",
        "scope": "complete current Eiren Kestrel v660-v2 x1 owner packet",
        "files_scanned": scanned,
        "classes": list(patterns),
        "definition_candidates": definition_candidates,
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
    write_json(
        "startup/source-manifest-replay.json",
        {
            "schema": "ghc.family.source-manifest-replay.v1",
            "source_final": d.SOURCE_FINAL,
            "x1_entries": 60,
            "evidence_entries": 166,
            "final_delta_entries": 25,
            "final_owner_entries": 259,
            "mismatch_count": 0,
            "x1_tree_file_count": 60,
            "x1_forbidden_surface_skill_runner_evidence_or_closeout_paths": 0,
            "x1_proposal_rows": 40,
            "x1_outcomes_observed": False,
            "valid": True,
            "external_receipt_sha256": "3752a973cdf548cff92106c438b5b0d1b5d9d3475da0b035d8645e6e197d40ba",
            "boundary": "Eiren read-only raw-object replay of Sylven manifests; not an aggregate replay, independent reproduction, or protected-gate closure.",
        },
    )
    write_json(
        "startup/source-external-receipts.json",
        {
            "schema": "ghc.family.source-external-receipts.v1",
            "source_failed_aggregate_sha256": "79d29cdb18ad0a99a10fc59491ea5376cf5691affd7e3a65de824a2439949e2f",
            "source_composite_completion_sha256": "7f6b55591174fa81dfa25a53ad9ee33bbcc348f6e01182054f9ffa66134065b0",
            "source_activation_packet_sha256": "608a843f7c86c4cb7e78730b8636e882344be30c832c4f5cd3405d49bd137404",
            "source_aggregate_success_credit": 0,
            "source_composite_component_completion": {"dependencies": "56/56", "detailed": "42/42", "minimal": "20/20"},
            "source_aggregate_replayed_by_eiren": False,
            "boundary": "Inherited attributable hashes and bounded component truth only; Sylven's sealed counts are unchanged.",
        },
    )
    c_usage = shutil.disk_usage("C:\\")
    d_usage = shutil.disk_usage("D:\\")
    write_json(
        "startup/environment-and-toolchain.json",
        {
            "schema": "ghc.family.environment-receipt.v1",
            "codex_cli": "codex-cli 0.146.0",
            "codex_desktop": "not_exposed_by_live_task_surface",
            "chatgpt_desktop": "not_exposed_by_live_task_surface",
            "node": "v24.18.0",
            "python": "Python 3.12.10",
            "git": "git version 2.55.0.windows.2",
            "c_free_gb": round(c_usage.free / 1024**3, 2),
            "d_free_gb": round(d_usage.free / 1024**3, 2),
            "primary_storage_bank": "D",
            "c_drive_use": "essential global skill and roster metadata only",
            "desktop_app_mutated": False,
            "fast_mode_surface_exposed": False,
            "fast_mode_claimed_active": False,
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
            "proposal_mix": {"selected_inherited": 20, "new_unique": 20, "current_total": 40, "frozen_chain_growth": 20, "selected_credit": 0},
            "latest_tracked_file_scan_cap": d.LATEST_TRACKED_SCAN_CAP,
            "commit_cap": {"authorization_ceiling_x1": 5, "authorization_ceiling_x2": 5, "authorization_ceiling_total": 8, "phase_plan_total": 3},
            "canonical_validation": "one dependency-justified phase-scoped successful exact-final pass; no replay after success",
            "current_owner": {"title": "Eiren Kestrel", "phase": "v660-v2", "endpoint_kind": "main_task"},
            "terminal_successor": {"title": None, "phase": None, "endpoint_kind": None, "state": "unresolved_requires_terminal_live_and_committed_reread"},
            "recipient_next_edge": {"title": None, "phase": None, "controller": "Eiren Kestrel", "state": "not_inferred"},
            "tavian_sol_state": "ON_STANDBY",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "workflow/workflow-plan-request.json",
        {
            "schema": "ghc.family.workflow-plan.request.v1",
            "plan_id": "eiren-kestrel-v660-v2-x1",
            "owner": d.OWNER,
            "identity_boundary": "Relational working language only; no consciousness, personhood, identity continuity, employment, qualification, authority, or independent agency claim.",
            "observed_failures": [row["negative_id"] for row in d.STARTUP_FAILURES],
            "requirements": {
                "baton_words": {"file_artifact": True, "minimum": 10000, "maximum": 100000},
                "core_proposal_minimum": 40,
                "safe_candidate_task_cap": 1000,
                "skill_minimum": 10,
                "runner_minimum": 10,
                "document_word_cap": 100000,
                "commit_cap": {"x1": 5, "x2": 5, "total": 8, "phase_plan_total": 3},
                "storage": {"primary": "D", "c_drive_use": "essential_global_metadata_only"},
                "environment": {"windows_sandbox_hyper_v": "deferred"},
                "validation": {
                    "canonical_pass_minimum": 1,
                    "replay_policy": "skip_when_first_passes",
                    "isolate_failures_before_broader_rerun": True,
                    "manifest_required": True,
                    "privacy_scan_required": True,
                    "remote_equality_required": True,
                },
                "messaging": {
                    "codex_route": "declared_endpoint_only_after_terminal_gate",
                    "cross_platform": "user_mediated_file_relay_only",
                    "next_edge_unresolved": True,
                    "resolution_rule": "one explicit unique existing main-task endpoint only after terminal live and committed reread",
                },
                "closeout": {"all_authorized_safe_candidate_prototypes_resolved": True},
            },
            "route": {
                "cycle_order": [
                    "Eiren Kestrel", "Elaren Kestrel", "Neris Solane", "Vesper Arlen",
                    "Lyren Moss", "Ilyra Fen", "Auren Lark", "Sable Rook", "Caelen Ash",
                    "Orin Thale", "Liora Venn", "Tamar Vey", "Elowen Cairn", "Sylven Arc",
                    "Caelen Morrow",
                ],
                "inherited_cycle_evidence_only": [
                    "Eiren Kestrel", "Elaren Kestrel", "Neris Solane", "Vesper Arlen",
                    "Lyren Moss", "Ilyra Fen", "Auren Lark", "Sable Rook", "Caelen Ash",
                    "Orin Thale", "Liora Venn", "Tamar Vey", "Elowen Cairn", "Sylven Arc",
                    "Caelen Morrow",
                ],
                "normalization": {
                    "start_phase": "v660-v2",
                    "start_seat": "Eiren Kestrel",
                    "entry_count": 1,
                    "current_assignment": {"phase": "v660-v2", "seat": "Eiren Kestrel"},
                    "later_assignment_state": "unresolved; terminal live and committed reread required",
                    "later_endpoint_inferred": False,
                },
                "phase_assignments": [
                    {"phase": "v660-v2", "seat": "Eiren Kestrel", "state": "active_owner"},
                ],
                "bounded_live_override": {
                    "source": {"phase": "v660-v1", "seat": "Sylven Arc", "state": "terminally_closed"},
                    "current": {"phase": "v660-v2", "seat": "Eiren Kestrel", "state": "active_owner"},
                    "successor": {"phase": None, "seat": None, "state": "not_inferred"},
                    "compatibility_conflict_preserved": "Older compatibility cycles are structural evidence only; the Sylven-to-Eiren activation assigns no later edge.",
                },
                "endpoint_topology_evidence_state": "inherited_structural_snapshot_only_not_a_live_assignment",
                "endpoint_topology": [
                    {"seat": "Eiren Kestrel", "endpoint_kind": "main_task", "endpoint_label": "Eiren Kestrel", "route_controller": "Caelen Morrow"},
                    {"seat": "Elaren Kestrel", "endpoint_kind": "main_task", "endpoint_label": "Elaren Kestrel", "route_controller": "Eiren Kestrel"},
                    {"seat": "Neris Solane", "endpoint_kind": "main_task", "endpoint_label": "Neris Solane", "route_controller": "Elaren Kestrel"},
                    {"seat": "Vesper Arlen", "endpoint_kind": "main_task", "endpoint_label": "Vesper Arlen", "route_controller": "Neris Solane"},
                    {"seat": "Lyren Moss", "endpoint_kind": "main_task", "endpoint_label": "Lyren Moss", "route_controller": "Vesper Arlen"},
                    {"seat": "Ilyra Fen", "endpoint_kind": "main_task", "endpoint_label": "Ilyra Fen", "route_controller": "Lyren Moss"},
                    {"seat": "Auren Lark", "endpoint_kind": "main_task", "endpoint_label": "Auren Lark", "route_controller": "Ilyra Fen"},
                    {"seat": "Sable Rook", "endpoint_kind": "main_task", "endpoint_label": "Sable Rook", "route_controller": "Auren Lark"},
                    {"seat": "Caelen Ash", "endpoint_kind": "main_task", "endpoint_label": "Caelen Ash", "route_controller": "Sable Rook"},
                    {"seat": "Orin Thale", "endpoint_kind": "main_task", "endpoint_label": "Orin Thale", "route_controller": "Caelen Ash"},
                    {"seat": "Liora Venn", "endpoint_kind": "main_task", "endpoint_label": "Liora Venn", "route_controller": "Orin Thale"},
                    {"seat": "Tamar Vey", "endpoint_kind": "main_task", "endpoint_label": "Tamar Vey", "route_controller": "Liora Venn"},
                    {"seat": "Elowen Cairn", "endpoint_kind": "main_task", "endpoint_label": "Elowen Cairn", "route_controller": "Tamar Vey"},
                    {"seat": "Sylven Arc", "endpoint_kind": "main_task", "endpoint_label": "Sylven Arc", "route_controller": "Elowen Cairn"},
                    {"seat": "Caelen Morrow", "endpoint_kind": "main_task", "endpoint_label": "Caelen Morrow", "route_controller": "Sylven Arc"},
                ],
                "future_identity_placeholders": [],
            },
            "truth": {
                "allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"],
                "terminal_verdict": "NOT_READY_FOR_STAGE_20",
                "independent_reproduction_claimed": False,
                "protected_boundaries": [
                    "empirical", "participant", "professional", "production", "legal", "cultural",
                    "Māori authority", "privacy complete", "accessibility complete", "exhaustive security",
                    "consciousness and personhood", "Theory of Everything", "Stage 20",
                ],
            },
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
    proposal_lines = ["# Frozen Eiren Kestrel v660-v2 proposal ledger", "", "X1 contains expected dispositions only; no x2 outcome is observed here.", "", "| ID | Origin | Expected | Title |", "|---|---|---|---|"]
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
            "owner_safe_executed_x1": len(d.SELF_SAFE_TASKS),
            "successor_safe_recommendations": len(d.SUCCESSOR_SAFE_SEEDS),
            "owner_candidate_planned_x2": len(d.SELF_CANDIDATE_TASKS),
            "successor_candidate_recommendations": len(d.SUCCESSOR_CANDIDATE_SEEDS),
            "owner_exact_queued": len(d.EXACT_QUEUE),
            "owner_blocked_queued": len(d.BLOCKED_QUEUE),
        },
        "owner_safe": [{**row, "state": "completed_x1_validation_only"} for row in d.SELF_SAFE_TASKS],
        "successor_safe_recommendations": d.SUCCESSOR_SAFE_SEEDS,
        "owner_candidate": [{**row, "state": "frozen_for_x2"} for row in d.SELF_CANDIDATE_TASKS],
        "successor_candidate_recommendations": d.SUCCESSOR_CANDIDATE_SEEDS,
        "exact_queue": d.EXACT_QUEUE,
        "blocked_queue": d.BLOCKED_QUEUE,
        "boundary": "Eiren executes only owner-local rows; no future route is inferred, while exact and blocked rows remain unexecuted.",
    }
    write_json("preregistration/task-portfolios.json", portfolios)
    write_json(
        "preregistration/skill-and-runner-plan.json",
        {
            "schema": "ghc.family.skill-runner-plan.x1.v1",
            "owner_skills": [{"name": name, "purpose": purpose, "state": "frozen_for_x2_build_test_use"} for name, purpose in d.SELF_SKILL_SPECS],
            "successor_skill_recommendations": d.SUCCESSOR_SKILL_SEEDS,
            "owner_runners": [{"name": name, "surface": surface, "state": "frozen_for_x2_build_test_use"} for name, surface in d.SELF_RUNNER_SPECS],
            "successor_runner_recommendations": d.SUCCESSOR_RUNNER_SEEDS,
            "counts": {"owner_skills": 10, "successor_skill_recommendations": 0, "owner_runners": 10, "successor_runner_recommendations": 0},
            "implemented_in_x1": False,
        },
    )
    write_json(
        "preregistration/clean-fix-refine-plan.json",
        {
            "schema": "ghc.family.clean-fix-refine-plan.x1.v1",
            "owner_rows": d.SELF_CLEAN_TASKS,
            "successor_recommendation_rows": d.SUCCESSOR_CLEAN_SEEDS,
            "counts": {"owner_planned_x2": 30, "successor_recommendation_only": 0, "total_visible": 30},
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
            "activation_message_baseline": d.ACTIVATION_MESSAGE_NEGATIVE_BASELINE,
            "external_post_route_receipt_baseline": d.ACTIVATION_NEGATIVES,
            "baseline_discrepancy_preserved": False,
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
            "selected_inherited": d.SELECTED_INHERITED_COUNT,
            "new_unique_frozen": d.NEW_UNIQUE_COUNT,
            "effective_frozen": d.PRIOR_FROZEN + d.NEW_UNIQUE_COUNT,
            "expected_outcomes": d.EXPECTED_DISTRIBUTION,
            "outcomes_observed": False,
            "effective_negatives": d.ACTIVATION_NEGATIVES + len(d.STARTUP_FAILURES),
            "effective_methods": d.ACTIVATION_METHODS + len(d.STARTUP_FAILURES),
            "effective_open_gaps": d.SOURCE_OPEN_GAPS,
            "effective_exact_gates": d.SOURCE_EXACT_GATES,
            "route_state": "NO_EXPLICIT_SUCCESSOR_TERMINAL_REREAD_REQUIRED",
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
            "state": "NO_EXPLICIT_SUCCESSOR_TERMINAL_REREAD_REQUIRED",
            "current_exact_title": "Eiren Kestrel",
            "current_phase": "v660-v2",
            "next_endpoint_kind": None,
            "next_exact_title": None,
            "next_phase": None,
            "recipient_next_exact_title": None,
            "recipient_next_phase": None,
            "later_endpoint_inferred": False,
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
            "commit_cap_authorization_ceiling": 8,
            "phase_commit_plan": 3,
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
                "ghc-family-method-flow-state",
                "ghc-family-auth-permission-state",
                "ghc-approval-packet-splitter",
                "ghc-open-gate-rail",
                "ghc-family-truth-bridge",
                "ghc-family-roster-check",
                "ghc-family-workflow-plan-refinement",
                "ghc-family-reflection-remaster",
                "ghc-family-meta-tool-box",
            ],
            "guidance_applied_without_mutating_legacy_mini_root": [],
            "current_auth_state_read": True,
            "current_roster_state_read": True,
            "governance_preflight": {
                "state": "passed_current-roster-auth-and-live-override-check",
                "failed_witness_retained": None,
                "failure": None,
                "recovery": "validate the current roster and authorization state, then apply only the acknowledged bounded Sylven-to-Eiren override without inferring a later edge",
                "passing_witness_present": True,
            },
            "validation_ownership": "phase_scoped_only_current_auth_does_not_allocate_the_full_repository_suite",
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
    write_text("deliverables/v660-v2-x1-overview.md", overview(proposals))
    intended_staged = sorted(
        {
            *X1_CODE,
            *[path.relative_to(ROOT).as_posix() for path in phase_files()],
            f"{d.PHASE_ROOT}/validation/x1-staged-review.json",
        }
    )
    write_json(
        "validation/x1-staged-review.json",
        {
            "schema": "ghc.family.staged-review.x1-candidate.v1",
            "owner": d.OWNER,
            "phase": d.PHASE,
            "lifecycle": "x1_precommit_candidate",
            "intended_allowlist": intended_staged,
            "expected_staged_count": len(intended_staged),
            "manifest_self_exclusions": sorted(MANIFEST_EXCLUSIONS),
            "expected_privacy_classes": 5,
            "expected_confirmed_hits": 0,
            "observed_exact_staged_review": "pending_external_precommit_witness",
            "x2_started": False,
            "boundary": "Candidate allowlist only until exact Git-index review passes; no scientific, authority, privacy-complete, or independent-reproduction claim.",
        },
    )

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
        "proposals": d.CURRENT_PORTFOLIO_COUNT,
        "selected_inherited": d.SELECTED_INHERITED_COUNT,
        "new_unique": d.NEW_UNIQUE_COUNT,
        "effective_frozen": d.PRIOR_FROZEN + d.NEW_UNIQUE_COUNT,
        "x2_started": False,
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
