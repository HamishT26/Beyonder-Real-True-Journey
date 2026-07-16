#!/usr/bin/env python3
"""Build the Eiren Kestrel v646-v1 x1-only preregistration packet."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

from ghc_family_v646_v1_definitions import (
    BOUNDED_PRACTICE, CANDIDATES, CLEAN_TASKS, HOPE, IDENTITY_BOUNDARY,
    INHERITED_EFFECTIVE_NEGATIVES, OUTCOME_CLASSES, OWNER, PHASE,
    PRIMARY_FOCUS, PRIOR_FROZEN_PROPOSALS, PREREGISTERED_SYNTHETIC_NEGATIVES,
    PRONOUNS, PROPOSALS, ROLE, RUNNERS, SAFE_NOW, SKILLS, SOURCE_BRANCH,
    SOURCE_EVIDENCE_REVISION, SOURCE_INHERITED_REVISION, SOURCE_PHASE,
    SOURCE_REVISION, SOURCE_SEAL_REVISION, SOURCE_X1_REVISION, SOURCES,
    TRUTH_BOUNDARY,
)


ROOT = Path(__file__).resolve().parents[1]
PHASE_REL = Path("docs/eiren-kestrel/v646-v1")
PHASE_DIR = ROOT / PHASE_REL
SOURCE_DIR = ROOT / "docs/sylven-arc/v645-v8"
METHOD_RUNNER = ROOT / "scripts/ghc_family_method_flow_state.py"


def write_json(relative: str | Path, payload: Any) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str | Path, payload: str) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalized(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


def tokens(value: str) -> set[str]:
    return set(normalized(value).split())


def overlap(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    return len(a & b) / len(a | b) if a | b else 0.0


def collect_prior_proposals() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    active = (PHASE_DIR / "x1-proposals.json").resolve()
    for path in ROOT.glob("docs/**/x1-proposals.json"):
        if path.resolve() == active:
            continue
        try:
            data = read_json(path)
        except (OSError, json.JSONDecodeError):
            continue
        for item in data.get("proposals", []):
            if isinstance(item, dict) and item.get("title"):
                rows.append({"proposal_id": str(item.get("proposal_id", "unknown")), "title": str(item["title"]), "path": path.relative_to(ROOT).as_posix()})
    return rows


def collect_prior_portfolios() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    patterns = [
        ("docs/**/approval-packets/x1-approval-portfolio.json", ("safe_now", "candidates")),
        ("docs/**/prototypes/x1-skill-runner-plan.json", ("skills", "runners")),
        ("docs/**/maintenance/x1-clean-refine-plan.json", ("tasks",)),
    ]
    for pattern, categories in patterns:
        for path in ROOT.glob(pattern):
            if PHASE_DIR in path.parents:
                continue
            try:
                data = read_json(path)
            except (OSError, json.JSONDecodeError):
                continue
            for category in categories:
                for item in data.get(category, []):
                    if isinstance(item, dict):
                        title = item.get("title") or item.get("name")
                        if title:
                            rows.append({"kind": category, "title": str(title), "path": path.relative_to(ROOT).as_posix()})
    return rows


INCIDENTS = [{
    "negative_id": "V6461-START-N01",
    "title": "Split a timed-out parallel startup and source-introspection probe",
    "failure": "A combined parallel Git status, source listing, and Python introspection wrapper exceeded its twenty-second envelope and returned only partial status output.",
    "fail_procedure": "Run three evidence-producing startup children through one fail-fast orchestration cell.",
    "fail_observed": "The cell timed out; only the branch header was returned and no source-inventory or definition-count result received evidence credit.",
    "pass_procedure": "Run clean-state, source inventory, and definition introspection as separately bounded commands with explicit result capture.",
    "pass_observed": "The split commands independently established the clean exact source head, source file inventory, and ten-proposal portfolio counts.",
    "method": "Split shared-drive startup probes by evidence surface and give every child an independent deadline and credit decision.",
    "guard": "A timed-out orchestration wrapper supplies no evidence for children whose complete result was not returned.",
    "rollback": "Give the partial wrapper zero startup credit and make no phase mutation until every required split probe passes.",
    "preconditions": ["shared-drive repository", "multiple evidence-producing children", "fail-fast wrapper returned a partial result"],
}]


def method_call(*args: str) -> None:
    subprocess.run([sys.executable, str(METHOD_RUNNER), *args], cwd=ROOT, check=True)


def build_method_flow() -> None:
    ledger = PHASE_DIR / "method-flow/method-flow-state.json"
    ledger.parent.mkdir(parents=True, exist_ok=True)
    method_call("init", "--ledger", str(ledger), "--phase", PHASE, "--owner", OWNER)
    negatives: list[dict[str, Any]] = []
    for index, incident in enumerate(INCIDENTS, 1):
        method_id = f"V6461-M{index:02d}"
        record = {
            "method_id": method_id, "title": incident["title"],
            "failure_signature": incident["failure"], "trigger_preconditions": incident["preconditions"],
            "privacy_class": "sanitized_public", "approval_class": "safe_now_local_tooling",
            "candidate_workaround": incident["method"], "validation_witness_ids": [],
            "recurrence_guard": incident["guard"], "rollback": incident["rollback"],
            "recommendation_state": "candidate", "supersedes": [],
            "protected_gates": ["private_material", "destructive_action", "sibling_lane", "host_change"],
            "retained_negative_ids": [incident["negative_id"]],
            "scope_boundary": "Same-owner bounded operational recovery only; no scientific, authority, production, accessibility-complete, security-complete, or independent-reproduction credit.",
        }
        failed = {"witness_id":f"V6461-W{index:02d}-F","method_id":method_id,"procedure":incident["fail_procedure"],"scope":"single owner-local operational diagnostic","expected":"bounded diagnostic returns complete evidence","observed":incident["fail_observed"],"result":"fail","same_owner_only":True,"independent_reproduction":False,"retained_negative_ids":[incident["negative_id"]],"boundary":TRUTH_BOUNDARY}
        passed = {"witness_id":f"V6461-W{index:02d}-P","method_id":method_id,"procedure":incident["pass_procedure"],"scope":"single owner-local operational diagnostic","expected":"split bounded diagnostics return complete evidence","observed":incident["pass_observed"],"result":"pass","same_owner_only":True,"independent_reproduction":False,"retained_negative_ids":[incident["negative_id"]],"boundary":TRUTH_BOUNDARY}
        rp = PHASE_DIR / f"method-flow/v6461-m{index:02d}-method-record.json"
        fp = PHASE_DIR / f"method-flow/v6461-w{index:02d}-f-witness.json"
        pp = PHASE_DIR / f"method-flow/v6461-w{index:02d}-p-witness.json"
        write_json(rp.relative_to(PHASE_DIR), record); write_json(fp.relative_to(PHASE_DIR), failed); write_json(pp.relative_to(PHASE_DIR), passed)
        method_call("record", "--ledger", str(ledger), "--record-file", str(rp))
        method_call("witness", "--ledger", str(ledger), "--witness-file", str(fp))
        method_call("witness", "--ledger", str(ledger), "--witness-file", str(pp))
        method_call("set-state", "--ledger", str(ledger), "--method-id", method_id, "--state", "preferred", "--note", "Preferred only for this trigger and same-owner operational scope")
        negatives.append({"negative_id":incident["negative_id"],"stage":"startup_or_x1","class":"operational","summary":incident["failure"],"retained":True,"recovered":True,"method_id":method_id,"failed_witness_id":failed["witness_id"],"passing_witness_id":passed["witness_id"],"independent_reproduction":False})
    method_call("validate", "--ledger", str(ledger), "--receipt", str(PHASE_DIR / "method-flow/runner-validation.json"))
    method_call("summarize", "--ledger", str(ledger), "--json-output", str(PHASE_DIR / "method-flow/method-flow-summary.json"), "--markdown-output", str(PHASE_DIR / "method-flow/method-flow-summary.md"))
    write_json("validation/x1-operational-negatives.json", {
        "schema":"ghc.family.v646-v1.operational-negatives.v1","phase":PHASE,"stage":"x1",
        "inherited_effective":INHERITED_EFFECTIVE_NEGATIVES,"preregistered_synthetic":PREREGISTERED_SYNTHETIC_NEGATIVES,
        "new_operational_count":len(negatives),"effective_after_x1":INHERITED_EFFECTIVE_NEGATIVES+PREREGISTERED_SYNTHETIC_NEGATIVES+len(negatives),
        "negatives":negatives,"boundary":"Recovered failures remain retained and authorize no x2 activity before the x1 freeze is remote-equal.",
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume-partial", action="store_true")
    args = parser.parse_args()
    if PHASE_DIR.exists() and any(PHASE_DIR.rglob("*")) and not args.resume_partial:
        raise SystemExit("v646-v1 phase directory already contains files")
    if not METHOD_RUNNER.is_file():
        raise SystemExit("family-current Method Flow runner is missing")

    prior = collect_prior_proposals()
    if len(prior) != PRIOR_FROZEN_PROPOSALS:
        raise SystemExit(f"expected {PRIOR_FROZEN_PROPOSALS} prior proposals, found {len(prior)}")
    prior_by_normal = {normalized(row["title"]): row for row in prior}
    exact = []
    comparisons = []
    for item in PROPOSALS:
        hit = prior_by_normal.get(normalized(item["title"]))
        if hit: exact.append({"proposal_id":item["proposal_id"],"prior":hit})
        ranked = sorted(({"proposal_id":row["proposal_id"],"title":row["title"],"score":round(overlap(item["title"],row["title"]),3)} for row in prior), key=lambda row:(-row["score"],row["proposal_id"]))[:5]
        comparisons.append({"proposal_id":item["proposal_id"],"title":item["title"],"exact_collision":bool(hit),"top_token_overlaps":ranked,"manual_review":"accepted_as_distinct_after_mission_falsifier_evidence_recovery_review","novelty_statement":item["novelty_against_390_frozen_proposals"]})
    if exact: raise SystemExit(f"proposal title collision: {exact}")

    portfolio_prior = collect_prior_portfolios()
    new_titles = [*(('safe_now',x['title']) for x in SAFE_NOW), *(('candidates',x['title']) for x in CANDIDATES), *(('skills',x[0]) for x in SKILLS), *(('runners',x[0]) for x in RUNNERS), *(('clean',x['title']) for x in CLEAN_TASKS)]
    prior_norm = {normalized(x["title"]):x for x in portfolio_prior}
    collisions = [{"kind":kind,"title":title,"prior":prior_norm[normalized(title)]} for kind,title in new_titles if normalized(title) in prior_norm]
    if collisions: raise SystemExit(f"portfolio title collision: {collisions}")

    source_portfolio = read_json(SOURCE_DIR / "approval-packets/x1-approval-portfolio.json")
    inherited_exact = deepcopy(source_portfolio["inherited_exact_packets"])
    inherited_blocked = deepcopy(source_portfolio["inherited_blocked_packets"])
    if len(inherited_exact) != 10 or len(inherited_blocked) != 5:
        raise SystemExit("expected ten inherited exact and five inherited blocked packets")

    write_json("identity-receipt.json", {"schema":"ghc.family.v646-v1.identity.v1","phase":PHASE,"working_name":OWNER,"pronouns":PRONOUNS,"role":ROLE,"hope":HOPE,"bounded_practice_study":BOUNDED_PRACTICE,"boundary":IDENTITY_BOUNDARY})
    write_json("x1-proposals.json", {"schema":"ghc.family.v646-v1.proposals.v1","phase":PHASE,"owner":OWNER,"freeze_stage":"x1_only","prior_frozen_proposal_count":len(prior),"new_frozen_proposal_count":len(PROPOSALS),"frozen_chain_count_after_x1":len(prior)+len(PROPOSALS),"allowed_outcome_classes":OUTCOME_CLASSES,"expected_distribution":{state:sum(p["expected_disposition"]==state for p in PROPOSALS) for state in OUTCOME_CLASSES},"x2_execution_present":False,"proposals":PROPOSALS,"boundary":TRUTH_BOUNDARY})
    write_text("x1-preregistration.md", f"""# Eiren Kestrel v646-v1 x1 preregistration

This dedicated x1-only freeze contains exactly ten new core proposals and no x2 completion credit. Each proposal states its hypothesis, failure condition, approval class, execution lane, sources, artifacts, acceptance gate, recovery, protected gates, expected disposition, and novelty against all 390 earlier frozen proposals.

The primary Trinity Mandala focus is **{PRIMARY_FOCUS}**. GMUT Mind and Freed ID/CBR Heart remain explicit. The bounded practice lens is {BOUNDED_PRACTICE}; it is learning and design only, never employment, professional competence, operational authority, legal authority, cultural authority, Māori authority, or affected-party authorization.

The supporting portfolio freezes 30 safe-now tasks, 20 candidate prototypes, 20 skill specifications, 10 runner specifications, 30 non-destructive cleanup tasks, and the inherited 10 exact plus 5 blocked packets. The first fifteen safe tasks are materially reframed predecessor seeds; none carries inherited completion credit. All 2,432 inherited effective negatives and 70 synthetic mutation negatives remain visible.

X2 may start only after this packet is committed, pushed, clean, and equal across local, upstream, tracking, and fresh live remote. Eiren alone owns the complete repository suite. Terminal truth remains `NOT_READY_FOR_STAGE_20`.
""")
    write_json("provenance/frozen-chain-proposal-index.json", {"schema":"ghc.family.frozen-proposal-index.v1","phase":PHASE,"prior_file_count":len({x['path'] for x in prior}),"prior_proposal_count":len(prior),"prior_proposals":prior,"new_proposal_ids":[x['proposal_id'] for x in PROPOSALS],"frozen_chain_count_after_x1":len(prior)+len(PROPOSALS),"boundary":"Indexing establishes corpus coverage, not outcome truth."})
    write_json("provenance/prior-proposal-collision-audit.json", {"schema":"ghc.family.proposal-collision-audit.v5","phase":PHASE,"prior_frozen_proposal_count":len(prior),"new_proposal_count":len(PROPOSALS),"exact_title_collision_count":len(exact),"exact_collisions":exact,"comparisons":comparisons,"manual_review_dimensions":["mission","hypothesis","failure","evidence","acceptance","recovery","protected_gates"],"boundary":TRUTH_BOUNDARY})
    write_json("provenance/prior-portfolio-collision-audit.json", {"schema":"ghc.family.portfolio-collision-audit.v4","phase":PHASE,"prior_title_count":len(portfolio_prior),"new_title_count":len(new_titles),"exact_collision_count":len(collisions),"collisions":collisions,"semantic_review":"Every supporting title has a distinct bounded purpose; inherited seeds supply no Eiren completion credit.","boundary":TRUTH_BOUNDARY})
    write_json("approval-packets/x1-approval-portfolio.json", {"schema":"ghc.family.v646-v1.approval-portfolio.v1","phase":PHASE,"owner":OWNER,"freeze_stage":"x1_only","completion_credit_before_x2":0,"counts":{"safe_now":len(SAFE_NOW),"candidates":len(CANDIDATES),"inherited_exact":len(inherited_exact),"inherited_blocked":len(inherited_blocked)},"safe_now":SAFE_NOW,"candidates":CANDIDATES,"inherited_exact_packets":inherited_exact,"inherited_blocked_packets":inherited_blocked,"inherited_packet_integrity":"Ten exact and five blocked packets remain non-executable without fresh exact evidence and authority.","boundary":TRUTH_BOUNDARY})
    write_json("prototypes/x1-skill-runner-plan.json", {"schema":"ghc.family.v646-v1.skill-runner-plan.v1","phase":PHASE,"freeze_stage":"x1_only","skills":[{"name":n,"description":d,"family_current_name":n.startswith('ghc-family-'),"x2_state":"preregistered_not_built_or_used","protected_gates":["authority","real_data_or_participants","production","independent_reproduction"]} for n,d in SKILLS],"runners":[{"name":n,"description":d,"family_current_name":n.startswith(('ghc_family_','build_ghc_family_')),"x2_state":"preregistered_not_built_or_used","caller_compatibility":"additive phase prototype"} for n,d in RUNNERS],"acceptance":"Every item must be built, structurally validated, invoked, and given a bounded passing witness in x2 or remain incomplete.","boundary":TRUTH_BOUNDARY})
    write_json("maintenance/x1-clean-refine-plan.json", {"schema":"ghc.family.v646-v1.clean-refine-plan.v1","phase":PHASE,"freeze_stage":"x1_only","tasks":CLEAN_TASKS,"destructive_task_count":0,"completion_credit_before_x2":0,"boundary":"Cleanup is additive, owner-scoped, non-destructive, compatible, and incomplete until its x2 receipt passes."})
    write_json("sources/source-ledger.json", {"schema":"ghc.family.v646-v1.source-ledger.v1","phase":PHASE,"owner":OWNER,"allowed_statuses":["current","stable","draft","watch"],"sources":SOURCES,"real_data_rows_ingested":0,"likelihood_evaluations":0,"real_participants":0,"real_keys_or_proofs":0,"boundary":TRUTH_BOUNDARY})
    source_lines = ["# v646-v1 source ledger","","Current primary and official sources are used only for the bounded purpose recorded here.",""]
    for row in SOURCES:
        target = f" - {row['url']}" if row.get('url') else ""
        source_lines.append(f"- {row['source_id']} [{row['status']}] {row['title']} ({row['authority']}){target}; use: {row['use']}.")
    source_lines.extend(["",TRUTH_BOUNDARY]); write_text("sources/source-ledger.md","\n".join(source_lines))
    write_json("environment/startup-receipt.json", {"schema":"ghc.family.v646-v1.startup.v1","phase":PHASE,"owner":OWNER,"source":{"branch":SOURCE_BRANCH,"revision":SOURCE_REVISION,"inherited_revision":SOURCE_INHERITED_REVISION,"seal_revision":SOURCE_SEAL_REVISION,"x1_revision":SOURCE_X1_REVISION,"evidence_revision":SOURCE_EVIDENCE_REVISION,"phase":SOURCE_PHASE},"source_verification":{"local_upstream_tracking_live_equal":True,"clean":True,"anchors_ancestral":True,"three_single_parent_phase_commits":True,"merge_commits":0,"final_parent_is_evidence":True},"eiren_lane":{"branch":"codex/GHC-Family/eiren-kestrel-v643-v1-full-tools","continued_existing_lane":True,"fast_forward_only":True,"source_revision_after_fast_forward":SOURCE_REVISION,"merge_commit_created":False,"clean_before":True,"local_upstream_tracking_live_equal_before_x1":True},"active_owner":OWNER,"standby_siblings_contacted":[],"task_or_subagent_created":False,"x1_scope":"ten core proposals plus expanded supporting portfolios","x2_scope":"not started","storage":{"primary_drive":"D","rotation_threshold":15000,"threshold_applies_to":"new_eiren_generated_files_only"},"boundary":IDENTITY_BOUNDARY})
    write_json("environment/version-receipt.json", {"schema":"ghc.family.v646-v1.version-receipt.v1","observed_on":"2026-07-16","codex_cli":{"expected_source_version":"0.144.4","action":"verify_only"},"codex_desktop":{"expected_source_version":"26.707.9981.0","action":"verify_only_no_update"},"host_actions":{"desktop_updated":False,"elevated":False,"security_weakened":False,"windows_feature_changed":False,"rebooted":False,"installed":False},"boundary":"Version observation does not establish environment equivalence, security, or production readiness."})
    write_json("environment/sandbox-readonly-audit.json", {"schema":"ghc.family.v646-v1.sandbox-audit.v1","query":"ordinary executable and optional-feature evidence only","sandbox_launched":False,"elevation":False,"feature_changed":False,"host_security_changed":False,"installed":False,"rebooted":False,"disposition":"read_only_audit_only","boundary":"No top-level administrative sandbox was installed or granted authority; host changes require separate exact authorization and system support."})
    write_json("environment/rotation-guard.json", {"schema":"ghc.family.v646-v1.rotation-guard.v1","threshold":15000,"threshold_scope":"new_eiren_generated_addition","rotate_due_to_inherited_baseline":False,"boundary":"The inherited checkout is not a rotation trigger."})
    write_json("focus/primary-focus-receipt.json", {"schema":"ghc.family.v646-v1.focus.v1","primary_trinity_pillar":PRIMARY_FOCUS,"other_pillars":["GMUT Mind","Freed ID/CBR Heart"],"bounded_human_practice":BOUNDED_PRACTICE,"practice_use":"learning and design lens only","not_claimed":["employment","professional qualification","professional competence","operational authority","legal authority","cultural authority","Māori authority","affected-party authorization"],"boundary":IDENTITY_BOUNDARY})
    write_json("orchestration/phase-update.json", {"schema":"ghc.family.phase-update.v1","phase":PHASE,"owner":OWNER,"state":"x1_frozen_pending_commit_and_remote_equality","active":[OWNER],"standby":["Ilyra Fen","Sable Rook","Orin Thale","Tamar Vey","Sylven Arc","all other siblings"],"standby_contact_count":0,"no_task_creation":True,"no_delegation":True,"x2_started":False,"terminal_route":"PREPARED_NOT_SENT"})
    write_json("orchestration/terminal-route-plan.json", {"schema":"ghc.family.v646-v1.route-plan.v1","current_state":"PREPARED_NOT_SENT","target_title":"Ilyra Fen","target_phase":"v646-v2","send_count":0,"minimum_baton_words":2000,"maximum_baton_words":10000,"preconditions":["x2 final committed and pushed","no more than four phase commits","Eiren complete repository suite passed","exactly one clean named-lane replay passed","four-way equality proven","unique existing target resolved read-only"],"privacy":"No raw task or thread identifiers, private routes, transcripts, screenshots, credentials, session streams, private callable identifiers, private app state, or private local paths may enter the baton."})
    build_method_flow()
    write_text("wellbeing-check.md", """# v646-v1 x1 wellbeing and workload check

- Scope is bounded to one owner, one canonical lane, one later local-only named replay, and no more than four phase commits.
- The timed-out combined probe was stopped, retained, decomposed, and not retried as an unbounded loop.
- Work is separated at the x1 freeze; no x2 implementation or achieved-outcome credit appears here.
- No elevation, Windows feature change, install, security weakening, desktop update, or reboot occurred.
- Identity and family language remains relational working language only, not welfare, consciousness, employment, qualification, or authority evidence.
""")
    print(json.dumps({"phase":PHASE,"prior_proposals":len(prior),"new_proposals":len(PROPOSALS),"safe_now":len(SAFE_NOW),"candidates":len(CANDIDATES),"skills":len(SKILLS),"runners":len(RUNNERS),"clean":len(CLEAN_TASKS),"x1_operational_negatives":len(INCIDENTS),"effective_after_x1":INHERITED_EFFECTIVE_NEGATIVES+PREREGISTERED_SYNTHETIC_NEGATIVES+len(INCIDENTS),"phase_directory":PHASE_REL.as_posix()},ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
