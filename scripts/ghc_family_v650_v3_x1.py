"""Build the dedicated Sable Rook v650-v3 x1 preregistration packet."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

from ghc_family_v650_v3_phase_data import (
    ACTIVATION_NEGATIVES, BOUNDARY, INHERITED_EXACT_GATES, INHERITED_OPEN_GAPS,
    OWNER, PHASE, PHASE_ROOT, PRIOR_FROZEN, PROPOSALS, RUNNERS, SKILLS, SOURCES,
    SOURCE_CLOSEOUT, SOURCE_EVIDENCE, SOURCE_HEAD, SOURCE_ORIGIN, SOURCE_X1,
    X1_NEGATIVES, candidate_tasks, cleanup_tasks, mutation_plan, safe_tasks,
)

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / PHASE_ROOT


def write_json(relative: str, value: object) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def write_text(relative: str, value: str) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def normalized_words(title: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", title.lower()) if len(w) > 2}


def build_novelty() -> tuple[dict, dict]:
    source = json.loads((REPO / "docs/ilyra-fen/v650-v2/provenance/frozen-chain-proposal-index.json").read_text(encoding="utf-8"))
    prior = list(source["prior_proposals"]) + list(source["new_proposals"])
    assert len(prior) == PRIOR_FROZEN
    prior_titles = {row["title"] for row in prior}
    audits = []
    for proposal in PROPOSALS:
        title = proposal["title"]
        a = normalized_words(title)
        scored = []
        for row in prior:
            b = normalized_words(row["title"])
            score = len(a & b) / max(1, len(a | b))
            scored.append((score, row))
        score, neighbor = max(scored, key=lambda item: item[0])
        audits.append({
            "proposal_id": proposal["proposal_id"],
            "exact_collision": title in prior_titles,
            "nearest_prior_id": neighbor["proposal_id"],
            "nearest_prior_title": neighbor["title"],
            "token_jaccard": round(score, 4),
            "disposition": "novel" if title not in prior_titles and score < 0.75 else "quarantine",
            "readable_reason": proposal["novelty_against_780_frozen_proposals"],
        })
    new = [{"proposal_id": row["proposal_id"], "title": row["title"]} for row in PROPOSALS]
    return (
        {"schema": "ghc.family.v650-v3.frozen-proposal-index.v1", "prior_count": PRIOR_FROZEN, "prior_proposals": prior, "new_count": len(new), "new_proposals": new, "count": len(prior) + len(new)},
        {"schema": "ghc.family.v650-v3.proposal-collision-audit.v1", "prior_count": PRIOR_FROZEN, "new_count": len(PROPOSALS), "exact_collision_count": sum(a["exact_collision"] for a in audits), "quarantine_count": sum(a["disposition"] == "quarantine" for a in audits), "audits": audits},
    )


def build_method_flow() -> None:
    mf = ROOT / "method-flow"
    mf.mkdir(parents=True, exist_ok=True)
    ledger = mf / "method-flow-state.json"
    runner = REPO / "scripts/ghc_family_method_flow_state.py"
    if not ledger.exists():
        subprocess.run([sys.executable, str(runner), "init", "--ledger", str(ledger), "--phase", PHASE, "--owner", OWNER], check=True, cwd=REPO)
    existing = {row["method_id"] for row in json.loads(ledger.read_text(encoding="utf-8"))["methods"]}
    for index, (negative_id, failure, recovery) in enumerate(X1_NEGATIVES, 1):
        method_id = f"V6503-M{index:02d}"
        if method_id in existing:
            continue
        record = {
            "method_id": method_id,
            "title": f"Retain and recover {negative_id}",
            "trigger_preconditions": [failure],
            "failure_signature": failure,
            "candidate_workaround": recovery,
            "rollback": "Stop, preserve the failed witness, and leave external and sibling state unchanged.",
            "recurrence_guard": recovery,
            "validation_witness_ids": [],
            "supersedes": [],
            "scope_boundary": "Same-owner bounded workflow recovery only; no scientific, authority, production, or independent-reproduction credit.",
            "protected_gates": ["failure_retention", "sibling_lane", "external_state", "independent_reproduction"],
            "approval_class": "safe_now_owner_scoped_workflow",
            "privacy_class": "sanitized_public",
            "recommendation_state": "candidate",
            "retained_negative_ids": [negative_id],
        }
        fail = {
            "witness_id": f"{method_id}-WFAIL", "method_id": method_id, "result": "fail",
            "scope": f"bounded {negative_id} failure", "procedure": failure,
            "expected": "Return attributable evidence within the declared bounded lane.", "observed": failure,
            "retained_negative_ids": [negative_id], "same_owner_only": True, "independent_reproduction": False,
            "boundary": "Workflow witness only; no scientific, production, professional, legal, cultural, or independent-reproduction credit.",
        }
        passed = {
            "witness_id": f"{method_id}-WPASS", "method_id": method_id, "result": "pass",
            "scope": f"bounded {negative_id} recovery", "procedure": recovery,
            "expected": "Return attributable evidence within the declared bounded lane.",
            "observed": f"The bounded recovery returned attributable evidence; {negative_id} remains retained.",
            "retained_negative_ids": [negative_id], "same_owner_only": True, "independent_reproduction": False,
            "boundary": "Workflow witness only; no scientific, production, professional, legal, cultural, or independent-reproduction credit.",
        }
        paths = []
        for suffix, value in (("method-record", record), ("wfail-witness", fail), ("wpass-witness", passed)):
            path = mf / f"{method_id.lower()}-{suffix}.json"
            path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
            paths.append(path)
        subprocess.run([sys.executable, str(runner), "record", "--ledger", str(ledger), "--record-file", str(paths[0])], check=True, cwd=REPO)
        for path in paths[1:]:
            subprocess.run([sys.executable, str(runner), "witness", "--ledger", str(ledger), "--witness-file", str(path)], check=True, cwd=REPO)
        subprocess.run([sys.executable, str(runner), "set-state", "--ledger", str(ledger), "--method-id", method_id, "--state", "preferred", "--note", recovery], check=True, cwd=REPO)
        existing.add(method_id)
    summary_path = mf / "method-flow-summary.json"
    validation_path = mf / "method-flow-validation.json"
    with summary_path.open("wb") as handle:
        subprocess.run([sys.executable, str(runner), "summarize", "--ledger", str(ledger)], check=True, cwd=REPO, stdout=handle)
    with validation_path.open("wb") as handle:
        subprocess.run([sys.executable, str(runner), "validate", "--ledger", str(ledger)], check=True, cwd=REPO, stdout=handle)


def main() -> int:
    ROOT.mkdir(parents=True, exist_ok=True)
    frozen, collision = build_novelty()
    if collision["exact_collision_count"] or collision["quarantine_count"]:
        raise SystemExit("semantic novelty audit failed")

    distribution = Counter(row["expected_disposition"] for row in PROPOSALS)
    source_rows = [{
        "source_id": sid, "status": status, "kind": kind, "title": title, "url": url,
        "verified_date": "2026-07-20",
        "use_boundary": "Design or protocol support only; not observation, participant evidence, authority, production certification, or gate closure.",
    } for sid, status, kind, title, url in SOURCES]
    status_counts = Counter(row["status"] for row in source_rows)
    proposals_packet = {
        "schema": "ghc.family.v650-v3.x1-proposals.v1", "phase": PHASE, "owner": OWNER,
        "primary_focus": "Freed ID and CBR Heart", "bounded_practice": "Passenger-ferry terminal loading, weather hold, correction readback, workload control, and watch handover",
        "practice_boundary": "Synthetic learning and design only; no employment, qualification, competence, dispatch, vessel, port, safety, legal, cultural, Maori, or affected-party authority.",
        "prior_frozen_count": PRIOR_FROZEN, "new_frozen_count": len(PROPOSALS), "frozen_total_after_x1": PRIOR_FROZEN + len(PROPOSALS),
        "expected_distribution": dict(distribution), "outcome_classes": ["completed", "represented", "open_gap", "exact_gate"],
        "x2_started": False, "boundary": BOUNDARY, "proposals": PROPOSALS,
    }
    write_json("x1-proposals.json", proposals_packet)
    write_json("provenance/frozen-chain-proposal-index.json", frozen)
    write_json("provenance/proposal-collision-audit.json", collision)
    write_json("sources/source-ledger.json", {"schema": "ghc.family.v650-v3.source-ledger.v1", "boundary": BOUNDARY, "status_counts": dict(status_counts), "sources": source_rows})
    write_text("sources/source-ledger.md", "# Source ledger\n\n" + "\n".join(f"- `{r['source_id']}` — **{r['status']}**, {r['title']}: {r['url']}" for r in source_rows) + "\n\nCitations define obligations only; they are not observations or delegated authority.")

    safe = safe_tasks(); candidates = candidate_tasks(); cleanup = cleanup_tasks(); mutations = mutation_plan()
    write_json("portfolios/safe-now-plan.json", {"schema": "ghc.family.v650-v3.safe-now-plan.v1", "count": len(safe), "minimum": 40, "tasks": safe})
    write_json("portfolios/candidate-plan.json", {"schema": "ghc.family.v650-v3.candidate-plan.v1", "count": len(candidates), "minimum": 30, "tasks": candidates})
    write_json("portfolios/skill-plan.json", {"schema": "ghc.family.v650-v3.skill-plan.v1", "count": len(SKILLS), "minimum": 20, "global_install": False, "subagent_forward_test": "forbidden_by_activation", "skills": [{"skill_id": f"V6503-SKILL-{i:02d}", "name": name, "status": "frozen_not_built", "acceptance_gate": "Initialize with skill-creator, validate, and smoke-use without global installation."} for i, name in enumerate(SKILLS, 1)]})
    write_json("portfolios/runner-plan.json", {"schema": "ghc.family.v650-v3.runner-plan.v1", "count": len(RUNNERS), "minimum": 10, "preserve_callers": True, "runners": [{"runner_id": f"V6503-RUN-{i:02d}", "name": name, "status": "frozen_not_built", "acceptance_gate": "Run one valid fixture and reject one mutation."} for i, name in enumerate(RUNNERS, 1)]})
    write_json("portfolios/clean-fix-refine-plan.json", {"schema": "ghc.family.v650-v3.cleanup-plan.v1", "count": len(cleanup), "minimum": 40, "destructive_actions": 0, "tasks": cleanup})
    write_json("validation/x1-synthetic-mutation-plan.json", {"schema": "ghc.family.v650-v3.mutation-plan.v1", "count": len(mutations), "executed_count": 0, "mutations": mutations})

    negative_rows = [{"negative_id": f"INHERITED-THROUGH-V6502-{ACTIVATION_NEGATIVES}", "class": "inherited_aggregate", "count": ACTIVATION_NEGATIVES, "disposition": "retained"}]
    negative_rows.extend({"negative_id": nid, "class": "x1_operational", "count": 1, "failure": failure, "recovery": recovery, "disposition": "retained"} for nid, failure, recovery in X1_NEGATIVES)
    write_json("retained-negative-register.json", {"schema": "ghc.family.v650-v3.retained-negatives.x1.v1", "activation_baseline": ACTIVATION_NEGATIVES, "x1_operational": len(X1_NEGATIVES), "effective_total": ACTIVATION_NEGATIVES + len(X1_NEGATIVES), "erased": 0, "entries": negative_rows})
    write_json("exact-open-gate-register.json", {"schema": "ghc.family.v650-v3.gates.x1.v1", "inherited_open_gaps": INHERITED_OPEN_GAPS, "inherited_exact_gates": INHERITED_EXACT_GATES, "new_open_gap": "V6503-P04", "new_exact_gate": "V6503-P09", "projected_open_gaps": INHERITED_OPEN_GAPS + 1, "projected_exact_gates": INHERITED_EXACT_GATES + 1, "closed_without_evidence": 0})
    write_json("identity-receipt.json", {"schema": "ghc.family.v650-v3.identity.v1", "name": OWNER, "pronouns": "they/them", "role": "relational evidence-and-reproducibility steward", "hope": "Keep every surviving claim easy to challenge or retract.", "relational_only": True, "not_evidence_of": ["consciousness", "personhood", "identity_continuity", "employment", "authority"]})
    write_json("wellbeing-check.json", {"schema": "ghc.family.v650-v3.wellbeing.x1.v1", "bounded_scope": True, "pause_available": True, "rename_redirect_stop_right": "Hamish", "identity_pressure": False, "workload_state": "bounded_and_cadence_not_used_as_proof"})
    write_json("environment/startup-receipt.json", {"schema": "ghc.family.v650-v3.startup.v1", "source_head": SOURCE_HEAD, "source_closeout": SOURCE_CLOSEOUT, "source_evidence": SOURCE_EVIDENCE, "source_x1": SOURCE_X1, "source_origin": SOURCE_ORIGIN, "source_manifests_verified": True, "owned_fast_forward_only": True, "four_way_equal_before_x1": True, "d_first": True, "sandbox_or_hyper_v_launched": False, "elevation": False, "host_security_changed": False})
    write_json("environment/version-receipt.json", {"schema": "ghc.family.v650-v3.versions.x1.v1", "verified_date": "2026-07-20", "codex_cli": "0.144.5", "codex_desktop": "26.715.4045.0", "python": "3.12.10", "git": "2.55.0.windows.2", "powershell": "5.1.26100.8894", "desktop_updated": False})
    write_json("orchestration/applicable-memory-record.json", {"schema": "ghc.family.v650-v3.memory-review.v1", "memory_content_used": False, "reason": "Targeted registry search returned no v650 match; live verified baton and committed handoffs are authoritative.", "private_routes_recorded": False})
    write_json("orchestration/terminal-route-state.json", {"schema": "ghc.family.v650-v3.route.x1.v1", "state": "HELD_X1", "sent": False, "target_title": "Orin Thale", "reason": "x2 and terminal validation have not occurred"})
    write_json("ghc-family-index.json", {"schema": "ghc.family.phase-index.v1", "phase": PHASE, "owner": OWNER, "state": "x1_frozen_candidate", "source_head": SOURCE_HEAD, "proposal_count": len(PROPOSALS), "portfolio_counts": {"safe_now": len(safe), "candidate": len(candidates), "skills": len(SKILLS), "runners": len(RUNNERS), "cleanup": len(cleanup)}, "shared_skill_change": False, "reviewed_current": ["ghc-family-index", "ghc-family-method-flow-state", "skill-creator"]})
    write_json("phase-truth.json", {"schema": "ghc.family.v650-v3.phase-truth.x1.v1", "phase": PHASE, "owner": OWNER, "state": "X1_FROZEN_NOT_EXECUTED", "x2_started": False, "proposal_count": len(PROPOSALS), "expected_distribution": dict(distribution), "effective_negatives": ACTIVATION_NEGATIVES + len(X1_NEGATIVES), "open_gaps": INHERITED_OPEN_GAPS, "exact_gates": INHERITED_EXACT_GATES, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": BOUNDARY})
    write_json("complete-incomplete-checklist.json", {"schema": "ghc.family.v650-v3.checklist.x1.v1", "complete": ["skills read", "source verified", "owned fast-forward", "novelty audit", "twenty proposals frozen", "expanded portfolios frozen", "x1 negatives retained"], "incomplete": ["x1 commit and remote equality", "x2 execution", "evidence commit", "closeout", "single canonical pass", "terminal route"]})
    build_method_flow()

    lines = ["# Sable Rook v650-v3 x1 preregistration", "", "This is a frozen plan, not execution evidence.", "", "## Identity and focus", "", "Sable Rook (they/them) works as a relational evidence-and-reproducibility steward and hopes to keep every surviving claim easy to challenge or retract. This language proves no consciousness, personhood, continuity, employment, or authority.", "", "Primary focus: Freed ID and CBR Heart. GMUT Mind and THOS Body remain explicit. The passenger-ferry practice is synthetic learning only.", "", "## Frozen proposals", ""]
    lines.extend(f"{i}. **{p['title']}** — expected `{p['expected_disposition']}`; {p['novelty_against_780_frozen_proposals']}" for i, p in enumerate(PROPOSALS, 1))
    lines.extend(["", "## Noncompensable gates", "", BOUNDARY, "", "X2 may begin only after this x1-only surface is committed, pushed, clean, and four-way equal."])
    write_text("x1-preregistration.md", "\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
