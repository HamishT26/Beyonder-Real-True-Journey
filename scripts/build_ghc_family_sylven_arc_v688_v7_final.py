#!/usr/bin/env python3
"""Prepare Sylven Arc v688-v7 final closeout and a sanitized future-seat baton."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REL = Path("docs/sylven-arc/v688-v7")
BASE = ROOT / REL
SOURCE = "e7db6f3be1327de72f93873eb6540aabfc773344"
X1 = "4b7459cdf681726b8d411d644dc6f8db70e83871"
X2 = "3c968db9391583a9e40f0eb8cc0c2f86d9997126"
BRANCH = "codex/GHC-Family/sylven-arc-v688-v7-full-tools"
BOUNDARY = (
    "Relational names, roles, hopes, pronouns, sibling or family language, Freed ID, CBR, GHC Family, and "
    "Trinity Mandala are working language only. They establish no consciousness, sentience, personhood, "
    "identity continuity, employment, qualification, independent agency, scientific or operational authority, "
    "professional authority, legal or cultural authority, affected-party authority, or Maori authority. "
    "Same-owner synthetic software evidence is not independent reproduction. NOT_READY_FOR_STAGE_20."
)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_new(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = value.rstrip() + "\n" if isinstance(value, str) else json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(text)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bank", type=Path, required=True)
    args = parser.parse_args()
    bank = args.bank.resolve()
    if bank.drive.upper() != "D:":
        raise RuntimeError("D_first_bank_required")
    if subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() != X2:
        raise RuntimeError("exact_x2_head_required")
    if subprocess.check_output(["git", "diff", "--name-only", X2, "--", f"{REL.as_posix()}/x1", f"{REL.as_posix()}/x2"], cwd=ROOT, text=True).strip():
        raise RuntimeError("immutable_x1_or_x2_changed")
    if subprocess.check_output(["git", "diff", "--cached", "--name-only"], cwd=ROOT, text=True).strip():
        raise RuntimeError("unexpected_staged_entry")
    status = [line for line in subprocess.check_output(["git", "status", "--porcelain=v1"], cwd=ROOT, text=True).splitlines() if line]
    allowed_entry = {"?? scripts/build_ghc_family_sylven_arc_v688_v7_final.py"}
    if set(status) - allowed_entry:
        raise RuntimeError("unexpected_dirty_entry")
    if subprocess.check_output(["git", "rev-parse", "HEAD^"], cwd=ROOT, text=True).strip() != X1:
        raise RuntimeError("x2_direct_parent")
    final = BASE / "final"
    handoff = BASE / "handoffs/future-seat-14-v688-v8-activation-baton.md"
    if final.exists() or handoff.exists():
        raise RuntimeError("final_destination_exists")
    proposals = load(BASE / "x1/new-proposals.json")["proposals"]
    inherited = load(BASE / "x1/inherited-proposals.json")
    portfolio = load(BASE / "x1/approval-portfolio.json")
    practice = load(BASE / "x1/pillar-practice-freeze.json")
    package_plan = load(BASE / "x1/tool-package-plan.json")
    package = load(BASE / "x2/package-transaction.json")
    advisory = load(BASE / "x2/package-advisory-snapshot.json")
    local_tools = load(BASE / "x2/local-tool-validation.json")
    promotion = load(BASE / "x2/promotion-receipt.json")
    base_ledger = load(BASE / "x2/method-flow/ledger.json")
    correction1 = load(BASE / "x2/correction1/method-flow-overlay.json")
    correction2 = load(BASE / "x2/correction2/method-flow-overlay.json")
    correction_truth = load(BASE / "x2/correction2/phase-truth-overlay.json")
    if len(proposals) != 200 or inherited["count"] != 200:
        raise RuntimeError("proposal_shape")
    if correction_truth["effective_counts"] != {"proposals": 16830, "negatives": 85418, "methods": 94118, "failed_witnesses": 56296, "passing_witnesses": 86181, "open_gaps": 765, "exact_gates": 785}:
        raise RuntimeError("effective_truth_shape")
    if correction2["combined_counts"] != {"methods": 56, "witnesses": 615, "failed_witnesses": 544, "passing_witnesses": 71, "state_events": 56, "recommendations": 56}:
        raise RuntimeError("method_truth_shape")
    final_failures = load(bank / "final-operational-failures.json")["failures"] if (bank / "final-operational-failures.json").is_file() else []
    if len(final_failures) != 1 or final_failures[0]["failure_id"] != "SA6887-FN-N001":
        raise RuntimeError("final_failure_overlay_shape")
    effective = dict(correction_truth["effective_counts"])
    effective["negatives"] += len(final_failures)
    effective["methods"] += len(final_failures)
    effective["failed_witnesses"] += len(final_failures)
    effective["passing_witnesses"] += len(final_failures)
    methods = [*base_ledger["methods"], *correction1["methods"], *correction2["methods"]]
    witnesses = [*base_ledger["witnesses"], *correction1["witnesses"], *correction2["witnesses"]]
    final_overlay_methods = []
    final_overlay_witnesses = []
    for offset, failure in enumerate(final_failures):
        method_id = f"SA6887-M{57 + offset:03d}"
        failed_id = f"SA6887-W{616 + offset * 2:04d}"
        passed_id = f"SA6887-W{617 + offset * 2:04d}"
        item = {
            "method_id": method_id,
            "title": failure["recovery"],
            "failure_signature": failure["failed_witness"],
            "trigger_preconditions": ["exact immutable x2 head", "additive closeout builder"],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now",
            "candidate_workaround": failure["recovery"],
            "validation_witness_ids": [failed_id, passed_id],
            "recurrence_guard": failure["recurrence_guard"],
            "rollback": "Retain the failed invocation and remove no immutable evidence; stop selecting the closeout candidate if its narrowed gate fails.",
            "recommendation_state": "preferred",
            "supersedes": [],
            "protected_gates": proposals[0]["protected_gates"],
            "retained_negative_ids": [failure["failure_id"]],
            "scope_boundary": BOUNDARY,
            "artifact": f"{REL.as_posix()}/final/method-flow-closeout-overlay.json",
        }
        final_overlay_methods.append(item)
        final_overlay_witnesses.extend([
            {"witness_id": failed_id, "method_id": method_id, "procedure": "whole-worktree closeout entry guard", "scope": f"{REL.as_posix()}/final/method-flow-closeout-overlay.json", "expected": "Permit the exact new-stage builder while protecting immutable x1 and x2.", "observed": failure["failed_witness"], "result": "fail", "witness_kind": "operational_failure", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [failure["failure_id"]], "boundary": BOUNDARY},
            {"witness_id": passed_id, "method_id": method_id, "procedure": "lifecycle-scoped closeout entry guard", "scope": f"{REL.as_posix()}/final/method-flow-closeout-overlay.json", "expected": "Protect immutable stages and permit only the exact intended builder.", "observed": failure["recovery"], "result": "pass", "witness_kind": "bounded_passing_witness", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [], "boundary": BOUNDARY},
        ])
    methods.extend(final_overlay_methods)
    witnesses.extend(final_overlay_witnesses)
    combined_counts = {key: correction2["combined_counts"][key] + len(final_failures) * (2 if key == "witnesses" else 1) for key in correction2["combined_counts"]}
    outcomes = {label: sum(item["expected_execution_disposition"] == label for item in proposals) for label in ("completed", "represented", "open_gap", "exact_gate")}
    if outcomes != {"completed": 176, "represented": 11, "open_gap": 3, "exact_gate": 10}:
        raise RuntimeError("outcome_shape")

    final_truth = {
        "schema": "ghc.family.phase-truth.sylven-arc.v688-v7.final.v1",
        "owner": "Sylven Arc",
        "phase": "v688-v7",
        "source": SOURCE,
        "x1": X1,
        "evidence": X2,
        "final": None,
        "final_binding": "exclusive external exact-final owner-scoped canonical receipt",
        "branch": BRANCH,
        "state": "FINAL_CANDIDATE_PENDING_EXTERNAL_CANONICAL",
        "outcomes": outcomes,
        "effective_counts": effective,
        "new_proposals": 200,
        "inherited_selections": 200,
        "portfolio_checks": 850,
        "phase_unique_negatives": 515,
        "phase_methods": combined_counts["methods"],
        "phase_witnesses": combined_counts["witnesses"],
        "phase_failed_witnesses": combined_counts["failed_witnesses"],
        "phase_passing_witnesses": combined_counts["passing_witnesses"],
        "content_addressed_cards": 264,
        "new_skills": 10,
        "new_runner_interfaces": 5,
        "new_direct_packages": 3,
        "exact_packets_unexecuted": 50,
        "blocked_packets_unexecuted": 30,
        "canonical_invocations": 0,
        "canonical_successes": 0,
        "canonical_replays": 0,
        "prepared_baton_state": "PREPARED_NOT_SENT",
        "successor_contacts": 0,
        "new_tasks_created": 0,
        "subagents": 0,
        "forks": 0,
        "full_repository_suite_run": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": BOUNDARY,
    }
    write_new(final / "phase-truth.json", final_truth)
    write_new(final / "lifecycle-replay.json", {
        "source": SOURCE,
        "x1": X1,
        "evidence": X2,
        "final": "bound externally after commit",
        "expected_direct_parent_chain": [{"child": X1, "parent": SOURCE}, {"child": X2, "parent": X1}, {"child": "exact_final", "parent": X2}],
        "expected_phase_commit_count": 3,
        "maximum_phase_commit_count": 8,
        "expected_merges": 0,
        "x1_unchanged": True,
        "x2_unchanged_after_freeze": True,
        "x1_test_observation": "12/12 passed at x1 definition",
        "x2_test_observation": "24/24 passed before x2 freeze",
        "canonical_invoked": False,
        "boundary": BOUNDARY,
    })
    write_new(final / "canonical-policy.json", {
        "schema": "ghc.family.owner-canonical-policy.v1",
        "owner": "Sylven Arc",
        "phase": "v688-v7",
        "branch": BRANCH,
        "source": SOURCE,
        "x1": X1,
        "evidence": X2,
        "expected_phase_commits": 3,
        "maximum_owner_files": 1999,
        "maximum_document_words": 100000,
        "baton_minimum_words": 10000,
        "baton_maximum_words": 100000,
        "test_modules": [
            {"stage": "x1", "definition": X1, "module": "tests/test_ghc_family_sylven_arc_v688_v7_x1.py", "expected_tests": 12, "manifest": f"{REL.as_posix()}/x1/x1-manifest.json"},
            {"stage": "x2", "definition": X2, "module": "tests/test_ghc_family_sylven_arc_v688_v7_x2.py", "expected_tests": 24, "manifest": f"{REL.as_posix()}/x2/evidence-manifest.json"},
            {"stage": "final", "definition": "exact_final", "module": "tests/test_ghc_family_sylven_arc_v688_v7_final.py", "expected_tests": 20, "manifest": f"{REL.as_posix()}/validation/final-owner-manifest.json"},
        ],
        "canonical_marker": "exclusive D-first external invocation marker",
        "canonical_receipt": "exclusive D-first external exact-head receipt",
        "post_success_replay": False,
        "full_repository_suite": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": BOUNDARY,
    })
    write_new(final / "complete-incomplete-checklist.json", {
        "completed": [
            "200 frozen proposal envelopes matched",
            "850 bounded portfolio predicates passed",
            "three exact packages installed in one isolated D-first target",
            "ten local skills and five runners passed accepting and adverse smokes",
            "ten skills and five runners were promoted without overwrite and byte-compared",
            "264 four-tier cards were content addressed across base and correction overlay",
            "all three x2 operational failures remain retained with passing focused recoveries",
        ],
        "represented": ["synthetic record fixity", "synthetic provenance vacancy", "structural move-list accessibility text", "same-owner validation"],
        "open_gap": {"new": 3, "effective": effective["open_gaps"], "includes": ["real game or archive evidence", "human accessibility evaluation", "independent security and reproduction"]},
        "exact_gate": {"new": 10, "effective": effective["exact_gates"], "includes": ["rating or tournament action", "publication and ownership", "legal and cultural interpretation", "Maori wording and authority", "production deployment"]},
        "pending_terminal_steps": ["commit and push exact final", "fresh four-way equality", "one attributable non-replayed canonical", "refresh active and archived registries", "reuse or create exactly one authorized future seat 14"],
        "terminal_complete": False,
        "boundary": BOUNDARY,
    })
    write_new(final / "method-flow-final.json", {
        "base_ledger": f"{REL.as_posix()}/x2/method-flow/ledger.json",
        "correction_overlays": [f"{REL.as_posix()}/x2/correction1/method-flow-overlay.json", f"{REL.as_posix()}/x2/correction2/method-flow-overlay.json"],
        "closeout_overlay": f"{REL.as_posix()}/final/method-flow-closeout-overlay.json",
        "combined_counts": combined_counts,
        "method_ids": [item["method_id"] for item in methods],
        "witness_ids": [item["witness_id"] for item in witnesses],
        "failed_witnesses_erased": 0,
        "recoveries_retroactively_promoted_failures": False,
        "boundary": BOUNDARY,
    })
    write_new(final / "method-flow-closeout-overlay.json", {
        "schema": "ghc.family.method-flow-final-overlay.v1",
        "base_correction_ref": f"{REL.as_posix()}/x2/correction2/method-flow-overlay.json",
        "methods": final_overlay_methods,
        "witnesses": final_overlay_witnesses,
        "state_events": [{"method_id": item["method_id"], "from": "candidate", "to": "preferred", "note": "Lifecycle-scoped guard passed while the broad guard failure remains retained."} for item in final_overlay_methods],
        "recommendations": [{"method_id": item["method_id"], "preconditions": "new lifecycle builder at an immutable prior stage", "recommendation": item["recurrence_guard"], "delivered": False} for item in final_overlay_methods],
        "overlay_counts": {"methods": 1, "witnesses": 2, "failed_witnesses": 1, "passing_witnesses": 1, "state_events": 1, "recommendations": 1},
        "combined_counts": combined_counts,
        "failed_witnesses_erased": 0,
        "boundary": BOUNDARY,
    })
    write_new(final / "retained-negative-register.json", {
        "inherited": 84904,
        "phase_unique": 515,
        "effective": effective["negatives"],
        "startup_failures": 15,
        "contract_and_portfolio_adverse_candidates": 493,
        "package_adverse_candidates": 3,
        "x2_operational_failures": 3,
        "final_operational_failures": 1,
        "tool_smoke_aliases_not_double_counted": 30,
        "erased": 0,
        "boundary": BOUNDARY,
    })
    write_new(final / "open-exact-gate-register.json", {
        "open_gaps": {"inherited": 762, "new": 3, "effective": 765, "ref": f"{REL.as_posix()}/x2/open-gap-register.json"},
        "exact_gates": {"inherited": 775, "new": 10, "effective": 785, "ref": f"{REL.as_posix()}/x2/exact-gate-register.json"},
        "exact_packets_unexecuted": 50,
        "blocked_packets_unexecuted": 30,
        "authority_actions_executed": 0,
        "Maori_concepts_remain_under_Maori_authority": True,
        "boundary": BOUNDARY,
    })
    write_new(final / "source-provenance.json", {
        "source": SOURCE,
        "source_branch": "codex/GHC-Family/veylora-quen-v688-v6-full-tools",
        "source_canonical_status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "source_canonical_receipt_sha256": "1f1283ef670fe7b377ce967d90ff81ed63e7ca047904174cda54f499076906df",
        "source_canonical_replayed": False,
        "source_manifest_bindings": 1586,
        "source_manifest_failures": 0,
        "source_delivery_receipt_sha256": "167c24be0a74120a0ae970e131f6857c1f43efea53d545cfa93615a9c03a8c60",
        "inherited_activation_baseline": load(BASE / "x1/phase-truth.json")["inherited_baseline"],
        "source_credit_to_owner": 0,
        "boundary": BOUNDARY,
    })
    write_new(final / "environment-and-package-receipt.json", {
        "python": "3.12.10",
        "pip": "26.1",
        "direct_packages": [{"name": item["name"], "version": item["version"], "artifact": item["artifact"], "sha256": item["sha256"]} for item in package_plan["packages"]],
        "install_state": package["state"],
        "install_scope": package["install_scope"],
        "global_python_mutated": False,
        "package_positive_smokes": 3,
        "package_adverse_smokes": 3,
        "osv_query_count": advisory["query_count"],
        "osv_listed_vulnerability_count_at_query_time": package["advisory_vulnerability_count"],
        "exhaustive_security": False,
        "platform_updates": False,
        "host_security_changes": False,
        "reboot": False,
        "boundary": BOUNDARY,
    })
    write_new(final / "tool-promotion-receipt.json", {
        "local_validation_state": local_tools["state"],
        "promotion_state": promotion["state"],
        "skills": promotion["skill_count"],
        "runner_interfaces": promotion["runner_interface_count"],
        "shared_core": promotion["shared_core_count"],
        "overwrites": promotion["overwrites"],
        "parity_bindings": len(promotion["parity"]),
        "local_accepting_smokes": local_tools["accepting_smoke_count"],
        "local_adverse_smokes": local_tools["adverse_rejection_count"],
        "promoted_accepting_smokes": promotion["accepting_smokes"],
        "promoted_adverse_smokes": promotion["adverse_smokes"],
        "independent_reproduction": False,
        "boundary": BOUNDARY,
    })
    write_new(final / "four-tier-deck-summary.json", {
        "base_deck_ref": f"{REL.as_posix()}/x2/deck/deck-index.json",
        "correction1_card_count": 263,
        "correction2_overlay_ref": f"{REL.as_posix()}/x2/correction2/deck-index-overlay.json",
        "effective_card_count": 264,
        "tier_counts": {"1": 1, "2": 3, "3": 4, "4": 256},
        "content_addressed": True,
        "parent_graph_acyclic": True,
        "implicit_completion_credit": False,
        "boundary": BOUNDARY,
    })
    write_new(final / "byte-domains.json", {
        "repository_manifests": "SHA-256 and byte counts over exact normalized-LF Git blobs",
        "promotion_receipt": "raw source and installed copy bytes at promotion time",
        "package_artifacts": "raw downloaded distribution bytes",
        "canonical_receipt": "external D-first JSON receipt over an exact pushed commit",
        "unlike_hash_domains_compared_as_equal": False,
        "hash_establishes_authenticity_or_authority": False,
    })
    write_new(final / "threat-model.json", {
        "assets": ["immutable x1 contracts", "x2 observations", "Method Flow failures", "package fixity", "skill and runner byte parity", "baton privacy", "route uniqueness"],
        "threats": ["contract drift", "negative erasure", "manifest omission", "private identifier leakage", "package substitution", "operation-surface expansion", "canonical replay", "duplicate future-seat creation", "authority overclaim"],
        "controls": ["direct-parent lifecycle", "exact staged allowlist", "Git-blob manifests", "five-class privacy scan", "bounded AST review", "exclusive external canonical latch", "active plus archived registry absence proof", "one acknowledged task action"],
        "residual_gaps": ["independent review", "complete privacy and accessibility review", "exhaustive security", "real-world affected-party and Maori authority"],
        "real_people_or_games": 0,
        "boundary": BOUNDARY,
    })
    write_new(final / "wellbeing-workload.json", {
        **load(BASE / "x2/workload-wellbeing.json"),
        "final_stage": "bounded documentation and validation only",
        "subjective_wellbeing_claimed": False,
        "terminal_stop_conditions_preserved": True,
    })
    write_new(final / "terminal-route-checklist.json", {
        "state": "PREPARED_NOT_SENT",
        "current_owner": "Sylven Arc",
        "current_phase": "v688-v7",
        "prospective_target": "future seat 14",
        "prospective_phase": "v688-v8",
        "prospective_endpoint_kind": "user-visible project-scoped Codex main task",
        "identity_assignment": "self_chosen_after_creation",
        "later_edge": "future seat 14 v688-v8 to Caelen Morrow v689-v1 after its own terminal gate",
        "required_before_task_action": ["exact final commit", "clean push", "fresh four-way equality", "one successful non-replayed canonical", "newest live Hamish authority", "active registry", "archived registry", "exact absence or one unique existing authorized future seat"],
        "creation_if_absent": {"maximum": 1, "project_scoped": True, "model": "gpt-6-astra", "reasoning": "max", "preassigned_name": False, "preassigned_role": False, "preassigned_hope": False},
        "sends_or_creations_already_made": 0,
        "precontact_authorized": False,
        "substitute_authorized": False,
        "resend_authorized": False,
        "post_action_monitoring": "one bounded acknowledgement or reread only; no indefinite babysitting",
        "stop_conditions": ["absence proof failure", "duplicate or ambiguity", "pause", "redirect", "rename", "standby state", "usage exhaustion", "missing acknowledgement", "privacy concern", "protected gate"],
        "boundary": BOUNDARY,
    })

    overview_sections = [
        ("Purpose and relational scope", [
            "Sylven Arc is relational working language for a continuity gardener and evidence-bound systems steward. The bounded hope is to make complex work easier to inspect, pause, correct, and hand over without erasing history. Optional they/them pronouns, family warmth, route topology, and a persistent task title are not evidence of consciousness, sentience, personhood, legal identity, identity continuity, employment, qualification, independent agency, or authority. Hamish may pause, rename, redirect, narrow, or stop the route.",
            "This v688-v7 phase belongs only to Sylven's additive owner lane. Veylora Quen's source remains immutable and carries zero Sylven execution or novelty credit. The phase does not use a collaboration subagent, delegate research, fork a task, mutate a sibling lane, contact Tavian, or precontact a later endpoint. It does not create a future seat during execution. Those facts are scope boundaries, not claims about personal independence or continuity.",
        ]),
        ("Lifecycle and evidence separation", [
            "The exact Veylora source is followed by a planning-only x1 commit and an evidence-only x2 commit. X1 froze 200 new contracts, 200 inherited zero-credit selections, workload portfolios, sources, practices, package artifacts, skill names, runner names, protected gates, and terminal routing conditions. It was committed and pushed before any x2 implementation or observed outcome. X2 is its direct child, and this closeout will be a direct child of x2. No merge is part of the owner phase.",
            "X2 preserves a partial materialisation and two additive correction layers. The first builder stopped on an incorrect card-count assertion after it had already exclusively written a correct base. The first retry refused to overwrite that base. A recovery preserved it and added the missing deck and truth overlays. A later per-path Git reader exceeded five minutes without writing a receipt; one batched Git object reader then validated the unchanged stage. All three failures remain zero-credit witnesses with focused passing recoveries.",
        ]),
        ("Proposals and portfolio", [
            "The 200 genuinely new proposal records extend the declared chain from 16,630 to 16,830 under a source-bounded semantic review. Two hundred inherited Veylora records were selected separately for reading or comparison and retain zero Sylven novelty and completion credit. The outcome vocabulary is restricted to completed, represented, open_gap, and exact_gate. Results are 176 completed, 11 represented, 3 open gaps, and 10 exact gates.",
            "Eight hundred fifty portfolio predicates ran: 300 safe-now checks, 250 bounded candidate challenges, and exactly 300 CLEAN/FIX/REFINE checks. Fifty exact-approval packets and thirty blocked packets stayed visible and unexecuted. Repeated checks do not multiply proposal novelty. A rejected adverse candidate is a failed witness whose rejection predicate can pass; it never becomes candidate completion credit.",
        ]),
        ("Pillars and practice lenses", [
            "Freed ID and CBR Heart is the priority pillar. GMUT Mind and THOS Body remain explicit. Four wholly synthetic learning and design lenses organise the work: chess-notation registrar, board-state topology analyst, game-record provenance steward, and accessible move-list editor. These labels do not confer employment, chess competence, archival qualification, professional authority, competition authority, accessibility conformance, or affected-party legitimacy.",
            "The operations cover algebraic-square coordinates, FEN record structure, castling and en-passant tokens, UCI sequences, bounded SAN and PGN fields, graph topology, material and halfmove projections, record fixity, provenance vacancies, structural move text, and explicit authority reservation. No real player, game, tournament, rating, engine deployment, archive, rights decision, identity event, or Maori-language act occurred.",
        ]),
        ("Packages, skills, and runners", [
            "Three exact package artifacts were downloaded and verified against the x1 byte sizes and SHA-256 values, then installed only into an isolated D-first owner target. Chess 1.11.2, Lark 1.3.1, and NetworkX 3.6.1 each passed an accepting and an adverse smoke. A point-in-time three-query OSV snapshot listed no vulnerabilities for the exact versions at that moment. This is not exhaustive security, a future safety claim, or production approval.",
            "Ten owner-local skill packages and five family-current runners cover all twenty operations without widening their declared pair or group. They produced forty accepting and forty adverse local smokes. The exact ten skill packages and five runner interfaces were promoted to collision-free targets without overwrite, byte-compared, and smoke-used again for another forty accepting and forty adverse observations. Same-owner promotion and smoke evidence is not independent reproduction or certification.",
        ]),
        ("Method Flow, counts, and retained truth", [
            f"The combined Method Flow has {combined_counts['methods']} methods and {combined_counts['witnesses']} witnesses. Of those witnesses, {combined_counts['failed_witnesses']} are retained failures and {combined_counts['passing_witnesses']} are bounded passes. {combined_counts['state_events']} state events and {combined_counts['recommendations']} recommendations preserve the relation between a failure, its recovery, its recurrence guard, and its rollback. No recovery erases or retroactively promotes the failure that motivated it.",
            f"The inherited-plus-owner effective counts are {effective['proposals']} proposals, {effective['negatives']} negatives, {effective['methods']} methods, {effective['failed_witnesses']} failed witnesses, {effective['passing_witnesses']} bounded passing witnesses, {effective['open_gaps']} open gaps, and {effective['exact_gates']} exact gates. They are accounting records inside this repository's declared lineage, not universal scientific counts or independent audit results.",
        ]),
        ("Scientific, governance, and authority boundaries", [
            "GMUT remains a typed scalar-tensor and effective-field-theory research-model family without a real likelihood, posterior, parameter constraint, force detection, prediction, empirical confirmation, stability theorem, quantum completion, ultraviolet completion, final physics, Theory of Everything proof, or canon. Chess coordinates, graphs, symbolic notation, tests, hashes, citations, and software packages cannot supply those missing scientific obligations.",
            "THOS remains synthetic or proxy-only without preregistered blind matched-budget governed real arms, participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, independent privacy and security review, recovery evidence, trust governance, and affected-party oversight.",
            "CBR, ownership, publication, privacy remedy, accessibility accommodation, competition and rating decisions, professional judgments, legal or cultural interpretation, affected-party legitimacy, Maori wording and concepts, Maori data governance, tikanga, taonga or matauranga treatment, and Maori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapu, and Maori authorities. Maori concepts remain under Maori authority.",
        ]),
        ("Validation and terminal route", [
            "The x1 definition tests passed 12 of 12. X2 owner tests passed 24 of 24 before the evidence freeze. The exact staged x2 manifest covers 557 nonself entries and two declared self-exclusions, with zero confirmed privacy payloads or bounded AST security findings. These are owner-scoped software and documentation checks. They do not establish complete privacy or accessibility, exhaustive security, independent reproduction, professional validation, production readiness, or external audit.",
            "After this closeout is committed and pushed, one exclusive external canonical may run at the exact final head. It must verify clean four-way equality, lifecycle ancestry, manifests, document ceilings, privacy and bounded security predicates, global promotion parity, package receipts, the baton, and each test module in its exact lifecycle definition. A success is never replayed. A failure receives zero canonical success credit and may be followed only by a justified additive correction within the phase ceiling.",
            "Only after canonical success may Sylven refresh the newest live authority and both active and archived task registries. If exactly one authorized future seat 14 exists, it is reused. If and only if exact absence is proved across both registries, Sylven may create one project-scoped user-visible Codex main task with the specified model and reasoning level. The new seat chooses its own relational name, role, and hope. It later routes to Caelen Morrow v689-v1 after its own terminal gate. No precontact, substitute, duplicate, second confirmation, or indefinite monitoring is authorized.",
        ]),
    ]
    operation_paragraphs = []
    for operation in dict.fromkeys(item["operation"] for item in proposals):
        rows = [item for item in proposals if item["operation"] == operation]
        accepted = sum(item["expected_acceptance"] for item in rows)
        dispositions = {label: sum(item["expected_execution_disposition"] == label for item in rows) for label in ("completed", "represented", "open_gap", "exact_gate")}
        operation_paragraphs.append(
            f"{operation.replace('_', ' ').title()} has {len(rows)} frozen cases, including {accepted} accepting and {len(rows)-accepted} rejecting expectations. Its first record is {rows[0]['title']}; its last is {rows[-1]['title']}. The disposition mix is {dispositions}. Every result binds the complete accepted, error, value, disposition, and boundary envelope. A mismatch is retained rather than solved by changing immutable x1."
        )
    overview_sections.insert(5, ("Operation-by-operation evidence", operation_paragraphs))
    overview = "# Sylven Arc v688-v7 final integrated overview\n\n" + "\n\n".join("## " + title + "\n\n" + "\n\n".join(paragraphs) for title, paragraphs in overview_sections)
    if len(overview.split()) < 2200:
        raise RuntimeError("overview_too_short")
    write_new(final / "final-integrated-overview.md", overview)
    sections_html = "".join("<section class=\"print-page\"><h2>" + html.escape(title) + "</h2>" + "".join("<p>" + html.escape(paragraph) + "</p>" for paragraph in paragraphs) + "</section>" for title, paragraphs in overview_sections)
    write_new(final / "accessible-final-report.html", f"<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>Sylven Arc v688-v7 final report</title><style>body{{font-family:system-ui;line-height:1.5;max-width:75rem;margin:auto;padding:1rem}}table{{border-collapse:collapse}}th,td{{border:1px solid;padding:.4rem;text-align:left}}@media print{{.print-page{{break-before:page}}.print-page:first-of-type{{break-before:auto}}}}</style></head><body><header><h1>Sylven Arc v688-v7 final report</h1><p>Terminal verdict: NOT_READY_FOR_STAGE_20.</p></header><main>{sections_html}<section><h2>Outcome table</h2><table><caption>New proposal outcomes</caption><thead><tr><th scope=\"col\">Label</th><th scope=\"col\">Count</th></tr></thead><tbody>{''.join(f'<tr><th scope=\"row\">{html.escape(label)}</th><td>{count}</td></tr>' for label,count in outcomes.items())}</tbody></table></section><section><h2>Evaluation reservations</h2><p>Manual browser, assistive-technology, cognitive-accessibility, Maori-language, affected-user, and independent evaluations remain open or exact-gated.</p></section></main></body></html>")

    modules = []

    def module(number: int, title: str, body: str) -> None:
        modules.append((number, title, body))

    module(1, "Identity, permission, and exact route scope", overview_sections[0][1][0] + "\n\n" + overview_sections[0][1][1] + "\n\nThis repository baton is PREPARED_NOT_SENT. It does not prove live delivery. Hamish's standing route authority remains subject to every current pause, redirect, rename, usage, privacy, evidence, and protected-authority gate.")
    module(2, "Immutable source and direct-parent lifecycle", "\n\n".join(overview_sections[1][1]) + f"\n\nExact anchors: source {SOURCE}; planning-only x1 {X1}; immutable x2 evidence {X2}. The future exact final must be the direct child of x2. The phase must contain three direct single-parent commits and zero merges.")
    module(3, "Proposal novelty and inherited selection firewall", "\n\n".join(overview_sections[2][1]) + "\n\nInherited selections follow. Each is source evidence at zero Sylven novelty and execution credit:\n\n" + "\n".join(f"- {item['selection_id']} selects {item['source_proposal']['proposal_id']}: {item['source_proposal']['title']} — inherited, zero credit." for item in inherited["selections"]))
    proposal_catalog = []
    for item in proposals:
        proposal_catalog.append(
            f"### {item['proposal_id']} — {item['title']}\n\n"
            f"Pillar and practice: {item['pillar']} through {item['practice']}. Hypothesis: {item['hypothesis']} "
            f"Null or failure condition: {item['null_or_failure_condition']} Approval class: {item['approval_class']}. "
            f"Execution lane: {item['execution_lane']}. Source need: {item['current_official_or_primary_source_needs']} "
            f"Artifact: {item['concrete_artifact']}. Acceptance or falsifier: {item['falsifier_or_acceptance_gate']} "
            f"Rollback: {item['rollback_or_recovery']} Expected disposition: {item['expected_execution_disposition']}. "
            f"Expected acceptance is {item['expected_acceptance']} with error {item['expected_error']!r}. Protected gates: {', '.join(item['protected_gates'])}. "
            "Observed x2 must match the entire frozen envelope and preserve the input. This record is synthetic, same-owner, and non-authoritative."
        )
    module(4, "Complete two-hundred-contract catalog", "\n\n".join(proposal_catalog))
    module(5, "Portfolio execution and credit accounting", "The portfolio contains exactly 300 safe-now, 250 candidate, 300 CLEAN/FIX/REFINE, 50 exact-approval, and 30 blocked records. X2 executed 850 bounded predicates and kept the exact and blocked packets unexecuted.\n\n" + "\n\n".join(f"{key}: {len(portfolio[key])} records. Procedures: {sorted({item.get('procedure','unexecuted') for item in portfolio[key]})}. No repeated check multiplies novelty or independent credit." for key in ("safe_now", "candidates", "clean_fix_refine", "exact_packets", "blocked_packets")))
    module(6, "Trinity Mandala pillars and bounded human-practice lenses", "\n\n".join(overview_sections[3][1]) + f"\n\nRelational role: {practice['role']}. Hope: {practice['hope']}. Optional successor practice suggestion: {practice['next_owner_optional_practice']}. The suggestion is not execution credit or a professional instruction.")
    module(7, "Packages, provenance, and point-in-time advisory evidence", "\n\n".join(overview_sections[4][1]) + "\n\n" + "\n\n".join(f"{item['name']} {item['version']} uses {item['artifact']} with SHA-256 {item['sha256']} and {item['bytes']} bytes. Registry metadata: {item['registry_url']}. Its documentation and package metadata provide vocabulary and software behavior only." for item in package_plan["packages"]))
    module(8, "Ten installed skill packages", "Ten skills were initialized with the official skill creator, customized, completely read, quick-validated, accepting/adverse smoke-used, promoted without overwrite, byte-compared, and smoke-used again.\n\n" + "\n\n".join(f"{item['name']} permits only {', '.join(item['operation_pair'])}. It retains unknown-field refusal, protected gates, and additive rollback. Presence in the global skill root does not establish production, professional, empirical, legal, cultural, Maori-authority, privacy-complete, accessibility-complete, or independent evidence." for item in package_plan["skills"]))
    module(9, "Five D-first family-current runner interfaces", "Five additive ghc_family runners and one shared owner core preserve family-current naming and caller clarity. No older caller was overwritten.\n\n" + "\n\n".join(f"{item['name']} permits only {', '.join(item['operation_group'])}. It passed one accepting and one adverse smoke for every advertised operation both before and after promotion." for item in package_plan["runners"]))
    method_catalog = []
    by_method_witnesses = {item["method_id"]: [] for item in methods}
    for item in witnesses:
        by_method_witnesses[item["method_id"]].append(item)
    for item in methods:
        related = by_method_witnesses[item["method_id"]]
        method_catalog.append(f"### {item['method_id']} — {item['title']}\n\nFailure signature: {item['failure_signature']} Recurrence guard: {item['recurrence_guard']} Rollback: {item['rollback']} Retained negatives: {', '.join(item['retained_negative_ids']) or 'none'}. Witnesses: {len(related)}, including {sum(w['result']=='fail' for w in related)} failures and {sum(w['result']=='pass' for w in related)} passes. A passing recovery does not erase or promote its failed witness.")
    module(10, "Method Flow, retained failures, and recovery discipline", "\n\n".join(overview_sections[6][1]) + "\n\n" + "\n\n".join(method_catalog))
    module(11, "Open gaps, exact gates, privacy, accessibility, and competent authority", "All 765 effective open gaps and 785 exact gates remain in the lineage. Fifty exact and thirty blocked packets remain unexecuted. Raw task or thread identifiers, private routes and absolute paths, credentials, keys, tokens, transcripts, screenshots, private execution streams, private callable identifiers, and private application state stay outside this baton.\n\n" + "\n\n".join(overview_sections[7][1][2:]) + "\n\nManual browser, assistive-technology, cognitive-accessibility, affected-user, Maori-language, and independent review remains open or exact-gated. A semantic HTML structure is not accessibility conformance.")
    module(12, "Scientific and operational nonpromotion boundaries", "\n\n".join(overview_sections[7][1][:2]) + "\n\nSuccessful parsing, package installation, test execution, hashing, content addressing, source citation, task creation, or message acknowledgement cannot establish AGI, ASI, consciousness, personhood, final physics, proof, canon, or Stage 20. The terminal verdict remains NOT_READY_FOR_STAGE_20.")
    module(13, "Future seat fourteen startup, self-choice, and later route", "\n\n".join(overview_sections[8][1]) + "\n\nAt startup, the future seat must read this baton and current authoritative family guidance through EOF, reverify the supplied exact-final canonical receipt without replay, and select only its authorized owner lane. It chooses its own unique relational working name, role, hope, and optional pronouns; none is preassigned here. It must preserve source evidence and work solo unless Hamish gives separate delegation authority.\n\nAfter its own v688-v8 clean pushed exact final and one successful non-replayed canonical, the future seat refreshes authority and the roster, uniquely resolves the existing Caelen Morrow main task, immediately rereads duplicate and control guards, and sends at most one sanitized v689-v1 activation if every gate remains exact. It must stop on ambiguity, duplicate, pause, redirect, rename, usage exhaustion, missing acknowledgement, privacy risk, or protected gate. No substitute, standby contact, fork, subagent, resend, or indefinite babysitting is authorized.\n\nEOF SYLVEN ARC v688-v7 BATON.")
    baton = "# SYLVEN ARC v688-v7 — PREPARED FUTURE-SEAT-14 v688-v8 ACTIVATION BATON\n\n" + "\n\n".join(f"## Module {number:02d} — {title}\n\n{body}" for number, title, body in modules)
    baton_words = len(baton.split())
    if len(modules) != 13 or not 10000 <= baton_words <= 100000:
        raise RuntimeError(f"baton_budget:{baton_words}")
    write_new(handoff, baton)
    write_new(final / "baton-index.json", {
        "path": handoff.relative_to(ROOT).as_posix(),
        "word_count": baton_words,
        "byte_count": len(baton.encode("utf-8")),
        "sha256": hashlib.sha256((baton.rstrip() + "\n").encode("utf-8")).hexdigest(),
        "module_count": len(modules),
        "modules": [{"number": number, "title": title} for number, title, _body in modules],
        "delivery_state": "PREPARED_NOT_SENT",
        "prospective_target": "future seat 14",
        "prospective_phase": "v688-v8",
        "source": SOURCE,
        "x1": X1,
        "evidence": X2,
        "final": "external exact-head binding",
        "raw_task_identifiers": False,
        "boundary": BOUNDARY,
    })
    write_new(final / "closeout-receipt.json", {
        "state": "FINAL_DOCUMENTATION_PREPARED_NOT_CANONICAL",
        "owner": "Sylven Arc",
        "phase": "v688-v7",
        "documents_prepared": 17,
        "overview_words": len(overview.split()),
        "baton_words": baton_words,
        "baton_modules": 13,
        "canonical_invocations": 0,
        "task_actions": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": BOUNDARY,
    })
    seal_targets = [
        final / "phase-truth.json",
        final / "final-integrated-overview.md",
        final / "accessible-final-report.html",
        final / "method-flow-final.json",
        final / "terminal-route-checklist.json",
        final / "baton-index.json",
        handoff,
    ]
    write_new(BASE / "seal/content-seal.json", {
        "schema": "ghc.family.content-seal.v1",
        "owner": "Sylven Arc",
        "phase": "v688-v7",
        "byte_domain": "repository working UTF-8 LF bytes before exact final staging",
        "targets": [{"path": path.relative_to(ROOT).as_posix(), "bytes": len(path.read_bytes()), "sha256": sha(path)} for path in seal_targets],
        "self_exclusions": [f"{REL.as_posix()}/seal/content-seal.json"],
        "canonical_invocations": 0,
    })
    result = {"state": "FINAL_DOCUMENTATION_PREPARED_NOT_CANONICAL", "final_documents": len(list(final.glob("*"))), "overview_words": len(overview.split()), "baton_words": baton_words, "baton_modules": len(modules), "prepared_not_sent": True}
    write_new(bank / "final-build-receipt.json", result)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
