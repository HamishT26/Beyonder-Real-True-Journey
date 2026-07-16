#!/usr/bin/env python3
"""Build Eiren Kestrel v647-v5 strict x1-only preregistration artifacts."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v647_v5_definitions as d


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/eiren-kestrel/v647-v5"
SOURCE_PHASE = ROOT / "docs/sylven-arc/v647-v4"


def write_json(relative: str | Path, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str | Path, payload: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalized(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.casefold()))


def tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.casefold()))


def overlap(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    return len(a & b) / len(a | b) if a | b else 0.0


def prior_proposals() -> list[dict[str, str]]:
    inherited = read_json(SOURCE_PHASE / "provenance/frozen-chain-proposal-index.json")
    rows = list(inherited.get("prior_proposals", []))
    if len(rows) != 500:
        raise RuntimeError(f"expected 500 indexed proposals, found {len(rows)}")
    source_x1 = read_json(SOURCE_PHASE / "x1-proposals.json")
    source_rows = source_x1.get("proposals", [])
    if len(source_rows) != 10:
        raise RuntimeError(f"expected ten Sylven proposals, found {len(source_rows)}")
    source_path = "docs/sylven-arc/v647-v4/x1-proposals.json"
    rows.extend(
        {"path": source_path, "proposal_id": row["proposal_id"], "title": row["title"]}
        for row in source_rows
    )
    if len(rows) != d.PRIOR_FROZEN_PROPOSALS:
        raise RuntimeError(f"expected {d.PRIOR_FROZEN_PROPOSALS} prior proposals, found {len(rows)}")
    return rows


def prior_portfolio_titles() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    patterns = [
        ("docs/**/approval-packets/x1-approval-portfolio.json", ("safe_now", "candidates", "exact_approval", "blocked")),
        ("docs/**/prototypes/x1-skill-runner-plan.json", ("skills", "runners")),
        ("docs/**/maintenance/x1-clean-refine-plan.json", ("tasks",)),
    ]
    for pattern, categories in patterns:
        for path in ROOT.glob(pattern):
            if PHASE in path.parents:
                continue
            try:
                data = read_json(path)
            except (OSError, json.JSONDecodeError):
                continue
            for category in categories:
                for item in data.get(category, []):
                    if not isinstance(item, dict):
                        continue
                    title = item.get("title") or item.get("name")
                    if title:
                        rows.append({"category": category, "title": str(title), "path": path.relative_to(ROOT).as_posix()})
    return rows


def proposal_audit(prior: list[dict[str, str]]) -> dict[str, Any]:
    by_norm: dict[str, list[dict[str, str]]] = {}
    for row in prior:
        by_norm.setdefault(normalized(row["title"]), []).append(row)
    collisions = []
    nearest = []
    for proposal in d.PROPOSALS:
        norm = normalized(proposal["title"])
        for row in by_norm.get(norm, []):
            collisions.append({"proposal_id": proposal["proposal_id"], "title": proposal["title"], "prior": row})
        ranked = sorted(
            (
                {"overlap": round(overlap(proposal["title"], row["title"]), 4), "prior_id": row["proposal_id"], "prior_title": row["title"], "path": row["path"]}
                for row in prior
            ),
            key=lambda row: (-row["overlap"], row["path"], row["prior_id"]),
        )[:5]
        nearest.append({"proposal_id": proposal["proposal_id"], "title": proposal["title"], "nearest": ranked})
    return {
        "schema": "ghc.family.v647-v5.prior-proposal-collision-audit.v1",
        "prior_count": len(prior),
        "new_count": len(d.PROPOSALS),
        "exact_collision_count": len(collisions),
        "exact_collisions": collisions,
        "nearest_neighbors": nearest,
        "valid": not collisions and len(prior) == d.PRIOR_FROZEN_PROPOSALS,
        "boundary": "Title and bounded token-overlap review supports preregistration novelty only; it is not scientific originality, patent review, or independent reproduction.",
    }


def current_portfolio_rows() -> list[dict[str, str]]:
    rows = []
    for category, titles in (
        ("safe_now", d.SAFE_TASK_TITLES),
        ("candidates", d.CANDIDATE_TITLES),
        ("skills", [name for name, _ in d.SKILL_SPECS]),
        ("runners", d.RUNNER_TITLES),
        ("tasks", d.CLEAN_TASK_TITLES),
        ("exact_approval", d.EXACT_PACKET_TITLES),
        ("blocked", d.BLOCKED_PACKET_TITLES),
    ):
        rows.extend({"category": category, "title": title} for title in titles)
    return rows


def portfolio_audit(prior: list[dict[str, str]]) -> dict[str, Any]:
    current = current_portfolio_rows()
    prior_by_norm: dict[str, list[dict[str, str]]] = {}
    for row in prior:
        prior_by_norm.setdefault(normalized(row["title"]), []).append(row)
    collisions = []
    for row in current:
        for earlier in prior_by_norm.get(normalized(row["title"]), []):
            collisions.append({"current": row, "prior": earlier})
    norms = Counter(normalized(row["title"]) for row in current)
    within = sorted(key for key, count in norms.items() if count > 1)
    return {
        "schema": "ghc.family.v647-v5.prior-portfolio-collision-audit.v1",
        "prior_title_count": len(prior),
        "current_title_count": len(current),
        "exact_collision_count": len(collisions),
        "exact_collisions": collisions,
        "within_current_duplicates": within,
        "valid": not collisions and not within,
        "boundary": "Exact normalized-title review is a bounded novelty gate, not a claim that broader concepts have no predecessors.",
    }


def task_rows(prefix: str, titles: list[str], approval_class: str) -> list[dict[str, Any]]:
    return [
        {
            "task_id": f"V6475-{prefix}-{index:02d}",
            "title": title,
            "approval_class": approval_class,
            "x1_state": "preregistered_no_completion_credit",
            "x2_completion_credit": False,
            "protected_gates": ["external_state", "sibling_lane", "destructive_action", "authority", "stage20"],
        }
        for index, title in enumerate(titles, 1)
    ]


def build() -> None:
    prior = prior_proposals()
    proposal_review = proposal_audit(prior)
    portfolio_review = portfolio_audit(prior_portfolio_titles())
    if not proposal_review["valid"]:
        raise RuntimeError(f"proposal collisions: {proposal_review['exact_collisions']}")
    if not portfolio_review["valid"]:
        raise RuntimeError(f"portfolio collisions: {portfolio_review['exact_collisions'][:10]} duplicates={portfolio_review['within_current_duplicates']}")

    method_state = read_json(PHASE / "method-flow/method-flow-state.json")
    expected_methods = len(d.X1_OPERATIONAL_NEGATIVES)
    if method_state.get("counts", {}).get("methods") != expected_methods:
        raise RuntimeError("Method Flow count does not match retained x1 operational negatives")
    if method_state.get("counts", {}).get("witness_results") != {"fail": expected_methods, "pass": expected_methods}:
        raise RuntimeError("Method Flow failed/passing witness parity is incomplete")

    write_json("identity-receipt.json", {
        "schema": "ghc.family.v647-v5.identity.v1", "phase": d.PHASE, "owner": d.OWNER,
        "pronouns": d.PRONOUNS, "relational_working_role": d.ROLE, "hope": d.HOPE,
        "identity_boundary": d.IDENTITY_BOUNDARY, "independent_authority": False,
    })
    write_json("environment/startup-receipt.json", {
        "schema": "ghc.family.v647-v5.startup.v1", "phase": d.PHASE, "owner": d.OWNER,
        "source_phase": d.SOURCE_PHASE, "source_branch": d.SOURCE_BRANCH, "source_revision": d.SOURCE_REVISION,
        "source_ancestry_verified": True, "source_remote_equality_verified": True, "source_clean": True,
        "eiren_fast_forward_only": True, "eiren_remote_equality_after_fast_forward": True,
        "no_merge": True, "no_reset": True, "no_force_push": True, "no_sibling_mutation": True,
        "validation_mode": "canonical plus one later local-only named replay; never detached",
    })
    write_json("environment/version-receipt.json", {
        "schema": "ghc.family.v647-v5.versions.v1", "verification_only": True,
        "codex_cli": "0.144.4", "codex_desktop": "26.707.9981.0", "chatgpt_desktop": "1.2026.190.0",
        "python": "3.12.10", "git": "2.55.0.windows.2", "desktop_updated": False,
        "elevation": False, "host_security_weakened": False, "windows_feature_changed": False,
        "unrelated_software_installed": False, "rebooted": False,
    })
    write_json("environment/rotation-guard.json", {
        "schema": "ghc.family.v647-v5.rotation.v1", "owner_generated_threshold": 15000,
        "scope": "new Eiren owner-generated files only", "inherited_files_are_trigger": False,
        "replacement_required_at_x1": False, "decision": "continue_existing_clean_canonical_lane",
    })
    write_json("focus/primary-focus-receipt.json", {
        "schema": "ghc.family.v647-v5.focus.v1", "primary_focus": d.PRIMARY_FOCUS,
        "bounded_human_practice": d.BOUNDED_PRACTICE,
        "practice_boundary": "Synthetic learning and design lens only; no employment, professional competence, emergency authority, operational command, legal authority, cultural authority, Māori authority, participant evidence, or affected-party authorization.",
        "other_pillars_visible": ["GMUT Mind", "THOS Body"],
    })
    write_json("sources/source-ledger.json", {
        "schema": "ghc.family.v647-v5.source-ledger.v1", "phase": d.PHASE, "source_count": len(d.SOURCES),
        "status_counts": dict(Counter(row["status"] for row in d.SOURCES)), "sources": d.SOURCES,
        "real_rows": 0, "real_people_or_operations": 0, "real_keys_or_tokens": 0,
        "authority_delegated": False, "network_execution_credit": 0,
        "boundary": d.TRUTH_BOUNDARY,
    })
    source_lines = ["# v647-v5 source ledger", "", "Official and primary sources bound the x1 designs; they do not supply real observations, participants, keys, authority, or outcome evidence.", ""]
    source_lines.extend(f"- **{row['source_id']} — {row['title']}** ({row['status']}): {row['url']} — {row['use']}" for row in d.SOURCES)
    write_text("sources/source-ledger.md", "\n".join(source_lines))

    write_json("provenance/frozen-chain-proposal-index.json", {
        "schema": "ghc.family.v647-v5.prior-proposal-index.v1", "count": len(prior), "prior_proposals": prior,
    })
    write_json("provenance/prior-proposal-collision-audit.json", proposal_review)
    write_json("provenance/prior-portfolio-collision-audit.json", portfolio_review)
    write_json("x1-proposals.json", {
        "schema": "ghc.family.v647-v5.x1-proposals.v1", "phase": d.PHASE, "owner": d.OWNER,
        "freeze_stage": "x1_only", "x2_execution_present": False,
        "prior_frozen_proposal_count": d.PRIOR_FROZEN_PROPOSALS, "new_frozen_proposal_count": 10, "frozen_chain_count_after_x1": d.PRIOR_FROZEN_PROPOSALS + 10,
        "allowed_outcome_classes": d.OUTCOME_CLASSES,
        "expected_distribution": dict(Counter(row["expected_disposition"] for row in d.PROPOSALS)),
        "primary_focus": d.PRIMARY_FOCUS, "bounded_human_practice": d.BOUNDED_PRACTICE,
        "proposals": d.PROPOSALS, "boundary": d.TRUTH_BOUNDARY,
    })

    safe = task_rows("SAFE", d.SAFE_TASK_TITLES, "safe_now_owner_scoped")
    candidates = task_rows("CAND", d.CANDIDATE_TITLES, "candidate_bounded_prototype")
    exact = task_rows("EXACT", d.EXACT_PACKET_TITLES, "exact_approval_not_granted")
    blocked = task_rows("BLOCK", d.BLOCKED_PACKET_TITLES, "blocked_prohibited")
    write_json("approval-packets/x1-approval-portfolio.json", {
        "schema": "ghc.family.v647-v5.x1-approval-portfolio.v1", "phase": d.PHASE,
        "safe_now_count": len(safe), "candidate_count": len(candidates),
        "exact_approval_count": len(exact), "blocked_count": len(blocked),
        "safe_now": safe, "candidates": candidates, "exact_approval": exact, "blocked": blocked,
        "completion_credit_before_x2": 0, "x2_execution_present": False,
        "boundary": "Quotas do not authorize unsafe work. Exact and blocked packets remain visibly unexecuted.",
    })
    skills = [
        {"skill_id": f"V6475-SKILL-{index:02d}", "name": name, "title": purpose,
         "x1_state": "preregistered_no_completion_credit", "built": False, "validated": False, "invoked": False,
         "compatibility": "family-current additive skill"}
        for index, (name, purpose) in enumerate(d.SKILL_SPECS, 1)
    ]
    runners = [
        {"runner_id": f"V6475-RUN-{index:02d}", "name": name, "title": name.replace("_", " ").removesuffix(" py"),
         "x1_state": "preregistered_no_completion_credit", "built": False, "validated": False, "invoked": False,
         "compatibility": "family-current ghc_family_* caller"}
        for index, name in enumerate(d.RUNNER_TITLES, 1)
    ]
    write_json("prototypes/x1-skill-runner-plan.json", {
        "schema": "ghc.family.v647-v5.x1-skill-runner-plan.v1", "phase": d.PHASE,
        "skill_count": len(skills), "runner_count": len(runners), "skills": skills, "runners": runners,
        "completion_credit_before_x2": 0, "x2_execution_present": False,
        "creator_skill_used": True, "caller_compatibility_required": True,
    })
    clean = task_rows("CLEAN", d.CLEAN_TASK_TITLES, "safe_now_additive_clean_fix_refine")
    write_json("maintenance/x1-clean-refine-plan.json", {
        "schema": "ghc.family.v647-v5.x1-clean-refine-plan.v1", "phase": d.PHASE,
        "task_count": len(clean), "tasks": clean, "completion_credit_before_x2": 0,
        "deletion_authorized": False, "downgrade_authorized": False, "x2_execution_present": False,
    })
    write_json("validation/x1-operational-negatives.json", {
        "schema": "ghc.family.v647-v5.x1-operational-negatives.v1", "phase": d.PHASE,
        "inherited_effective_negatives": d.INHERITED_EFFECTIVE_NEGATIVES,
        "count": len(d.X1_OPERATIONAL_NEGATIVES), "negatives": d.X1_OPERATIONAL_NEGATIVES,
        "observed_effective_after_x1": d.INHERITED_EFFECTIVE_NEGATIVES + len(d.X1_OPERATIONAL_NEGATIVES),
        "preregistered_synthetic_mutation_negatives": d.PREREGISTERED_SYNTHETIC_NEGATIVES,
        "synthetic_mutations_executed_in_x1": 0, "failure_erasure_count": 0,
    })
    write_json("orchestration/memory-review-receipt.json", {
        "schema": "ghc.family.v647-v5.memory-review.v1", "newest_applicable_memory_used": True,
        "applied": ["exact source and equality before mutation", "x1 freeze before x2", "retain failures", "Eiren full-suite ownership", "one named replay", "one terminal baton"],
        "private_memory_material_copied": False,
    })
    write_json("orchestration/phase-update.json", {
        "schema": "ghc.family.v647-v5.phase-update.v1", "phase": d.PHASE, "owner": d.OWNER,
        "state": "X1_PREREGISTRATION_READY_FOR_FREEZE", "x1_only": True, "x2_started": False,
        "no_task_creation": True, "no_delegation": True, "no_sibling_mutation": True,
        "source_revision": d.SOURCE_REVISION, "prior_proposals_audited": d.PRIOR_FROZEN_PROPOSALS, "new_proposals": 10,
    })
    write_json("orchestration/terminal-route-plan.json", {
        "schema": "ghc.family.v647-v5.terminal-route-plan.v1", "current_state": "PREPARED_NOT_SENT",
        "target_title": "Ilyra Fen", "target_phase": "v647-gmut-thos-v6-x1-x2", "send_count": 0,
        "task_creation_authorized": False, "send_gate": "exact final clean pushed remote-equal head plus full suite and one named replay",
        "route_order": ["Eiren Kestrel", "Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc"],
    })

    overview = f"""# Eiren Kestrel v647-v5 x1 preregistration

This packet freezes ten core proposals after a counted review of all 510 inherited frozen proposals. Its expected dispositions are six completed, two represented, one open gap, and one exact gate. Nothing in x1 earns x2 completion credit.

The primary focus is **{d.PRIMARY_FOCUS}**. The bounded practice lens is **{d.BOUNDED_PRACTICE}**. It is a synthetic learning and design lens only: no employment, professional qualification, emergency command, public-warning authority, legal or cultural authority, Māori authority, participant evidence, or affected-party authorization is claimed.

The expanded portfolio freezes 30 safe-now owner-scoped tasks, 20 candidate prototypes, 20 phase-local skill designs, 10 family-current runner designs, and 30 additive clean/fix/refine tasks. Ten exact-approval packets and five blocked packets remain unexecuted. Quotas never broaden authorization.

GMUT remains a typed scalar-tensor and EFT research-model family. The ADM work is a typed symbolic obligation board, not empirical confirmation or a Theory of Everything. Pantheon+ is preregistered to fail closed on zero rows. THOS library handover remains synthetic and non-operational. Freed ID PAR remains synthetic and nonproduction. CBR library access, privacy, children, disability, digital-exclusion remedy, legal, cultural, data-governance, and Māori matters remain exact-gated.

Seven owner-local workflow failures are retained with seven passing bounded recovery witnesses. Same-owner recovery is not independent reproduction. Eiren alone will run the complete repository suite after x2, plus exactly one local-only named replay. The terminal route to Ilyra Fen is prepared, not sent.

Terminal verdict at x1: **NOT_READY_FOR_STAGE_20**.
"""
    write_text("x1-preregistration.md", overview)

    frozen = [
        "x1-proposals.json",
        "approval-packets/x1-approval-portfolio.json",
        "prototypes/x1-skill-runner-plan.json",
        "maintenance/x1-clean-refine-plan.json",
        "sources/source-ledger.json",
        "provenance/prior-proposal-collision-audit.json",
        "provenance/prior-portfolio-collision-audit.json",
    ]
    write_json("reproduction/x1-content-seal.json", {
        "schema": "ghc.family.v647-v5.x1-content-seal.v1", "phase": d.PHASE,
        "hash_domain": "working_tree_utf8_bytes_to_be_verified_as_exact_x1_git_blobs",
        "path_count": len(frozen),
        "frozen_paths": [{"path": path, "sha256": hashlib.sha256((PHASE / path).read_bytes()).hexdigest()} for path in frozen],
        "x2_execution_present": False, "source_revision": d.SOURCE_REVISION,
    })


def main() -> int:
    build()
    result = {
        "phase": d.PHASE, "prior_proposals": d.PRIOR_FROZEN_PROPOSALS, "new_proposals": 10, "frozen_total": d.PRIOR_FROZEN_PROPOSALS + 10,
        "safe_now": len(d.SAFE_TASK_TITLES), "candidates": len(d.CANDIDATE_TITLES),
        "skills": len(d.SKILL_SPECS), "runners": len(d.RUNNER_TITLES), "clean_refine": len(d.CLEAN_TASK_TITLES),
        "x1_operational_negatives": len(d.X1_OPERATIONAL_NEGATIVES), "result": "pass",
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
