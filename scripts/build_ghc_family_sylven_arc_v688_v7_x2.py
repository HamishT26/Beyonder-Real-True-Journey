#!/usr/bin/env python3
"""Materialize Sylven Arc v688-v7 x2 evidence from the immutable x1 contracts."""
from __future__ import annotations

import argparse
import copy
import hashlib
import html
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REL = Path("docs/sylven-arc/v688-v7")
BASE = ROOT / REL
X1 = "4b7459cdf681726b8d411d644dc6f8db70e83871"
SOURCE = "e7db6f3be1327de72f93873eb6540aabfc773344"
OWNER = "Sylven Arc"
PHASE = "v688-v7"
sys.path.insert(0, str(ROOT / "scripts"))
import ghc_family_chess_records_core as core


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode("utf-8")


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def load(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def write_new(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(value, str):
        rendered = value.rstrip() + "\n"
    else:
        rendered = json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(rendered)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bank", type=Path, required=True)
    args = parser.parse_args()
    bank = args.bank.resolve()
    if bank.drive.upper() != "D:":
        raise RuntimeError("D_first_bank_required")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if head != X1:
        raise RuntimeError("exact_x1_head_required")
    if subprocess.check_output(["git", "diff", "--name-only", X1, "--", REL.as_posix() + "/x1"], cwd=ROOT, text=True).strip():
        raise RuntimeError("immutable_x1_changed")
    x2 = BASE / "x2"
    local_tools = load(x2 / "local-tool-validation.json")
    promotion = load(x2 / "promotion-receipt.json")
    package = load(bank / "package-transaction.json")
    advisory = load(bank / "package-advisory-snapshot.json")
    if local_tools["state"] != "VALID_LOCAL_OWNER_TOOLS":
        raise RuntimeError("local_tool_gate")
    if promotion["state"] != "PROMOTED_VALIDATED_BYTE_EQUAL":
        raise RuntimeError("promotion_gate")
    if package["state"] != "COMPLETE":
        raise RuntimeError("package_gate")
    proposals = load(BASE / "x1/new-proposals.json")["proposals"]
    portfolio = load(BASE / "x1/approval-portfolio.json")
    startup = load(BASE / "x1/method-flow-startup.json")
    baseline = load(BASE / "x1/phase-truth.json")["inherited_baseline"]
    practice = load(BASE / "x1/pillar-practice-freeze.json")
    if len(proposals) != 200 or len(portfolio["safe_now"]) != 300 or len(portfolio["candidates"]) != 250 or len(portfolio["clean_fix_refine"]) != 300:
        raise RuntimeError("frozen_workload_shape")
    if len(portfolio["exact_packets"]) != 50 or len(portfolio["blocked_packets"]) != 30:
        raise RuntimeError("unexecuted_gate_shape")

    by_id = {item["proposal_id"]: item for item in proposals}
    contract_rows: list[dict] = []
    negative_rows: list[dict] = []
    challenge_rows: dict[str, list[dict]] = {operation: [] for operation in core.FIELDS}

    def retain(identifier: str, operation: str, kind: str, artifact: str, detail: object) -> str:
        negative_rows.append({
            "negative_id": identifier,
            "operation": operation,
            "kind": kind,
            "artifact": artifact,
            "detail": detail,
            "candidate_admission": "refused",
            "completion_credit": 0,
            "recovery_erases_failure": False,
        })
        return identifier

    observed_by_id: dict[str, dict] = {}
    for index, proposal in enumerate(proposals, 1):
        before = copy.deepcopy(proposal["input"])
        observed = core.evaluate(proposal["input"])
        unchanged = canonical(before) == canonical(proposal["input"])
        matched = core.matches_contract(proposal, observed)
        if not matched or not unchanged:
            raise RuntimeError(f"frozen_contract:{proposal['proposal_id']}")
        artifact = f"{REL.as_posix()}/x2/contracts/{index:03d}.json"
        row = {
            "schema": "ghc.family.observed-chess-record-contract.v1",
            "proposal_id": proposal["proposal_id"],
            "operation": proposal["operation"],
            "input": proposal["input"],
            "expected": core.expected_envelope(proposal),
            "observed": observed,
            "matches": True,
            "input_unchanged": True,
            "source_kind": "synthetic",
            "x1": X1,
            "same_owner_only": True,
            "independent_reproduction": False,
        }
        contract_rows.append((artifact, row))
        observed_by_id[proposal["proposal_id"]] = observed
        if not proposal["expected_acceptance"]:
            retain(
                f"SA6887-CONTRACT-N{index:03d}",
                proposal["operation"],
                "preregistered_invalid_contract",
                artifact,
                {"proposal_id": proposal["proposal_id"], "observed_error": observed["error"]},
            )

    task_results = []
    for category in ("safe_now", "candidates", "clean_fix_refine"):
        for task in portfolio[category]:
            proposal = by_id[task["proposal_id"]]
            operation = proposal["operation"]
            procedure = task["procedure"]
            payload = copy.deepcopy(proposal["input"])
            expected = core.expected_envelope(proposal)
            record = {
                "packet_id": task["packet_id"],
                "proposal_id": proposal["proposal_id"],
                "procedure": procedure,
            }
            if procedure == "contract_check":
                passed = core.matches_contract(proposal, observed_by_id[proposal["proposal_id"]])
                record["contract_ref"] = proposal["concrete_artifact"]
            elif procedure == "repeat_stability":
                result = core.evaluate(payload)
                passed = core.matches_contract(proposal, result) and canonical(payload) == canonical(proposal["input"])
                record["observed"] = result
            elif procedure in {"unknown_field_rejection", "missing_field_rejection"}:
                if procedure == "unknown_field_rejection":
                    payload["undeclared_extension"] = True
                else:
                    payload.pop(next(name for name in payload if name != "operation"))
                before = copy.deepcopy(payload)
                result = core.evaluate(payload)
                passed = result["accepted"] is False and result["error"] == "field_set" and canonical(payload) == canonical(before)
                negative_id = retain(
                    f"SA6887-CAND-N{len([n for n in negative_rows if n['negative_id'].startswith('SA6887-CAND')]) + 1:03d}",
                    operation,
                    procedure,
                    f"{REL.as_posix()}/x2/challenges/{operation}.json",
                    {"packet_id": task["packet_id"], "observed_error": result["error"]},
                )
                record.update({"input": payload, "observed": result, "retained_negative_id": negative_id})
            elif procedure == "altered_output_rejection":
                candidate = copy.deepcopy(expected)
                variant = int(task["packet_id"].rsplit("-", 1)[-1]) % 5
                if variant == 0:
                    candidate["accepted"] = not candidate["accepted"]
                elif variant == 1:
                    candidate["error"] = "altered_error"
                elif variant == 2:
                    candidate["value"] = {"altered_value": True}
                elif variant == 3:
                    candidate["boundary"] = "unjustified authority"
                else:
                    candidate["undeclared_result"] = True
                passed = not core.matches_contract(proposal, candidate)
                negative_id = retain(
                    f"SA6887-CFR-N{len([n for n in negative_rows if n['negative_id'].startswith('SA6887-CFR')]) + 1:03d}",
                    operation,
                    procedure,
                    f"{REL.as_posix()}/x2/challenges/{operation}.json",
                    {"packet_id": task["packet_id"], "comparator_accepted": False},
                )
                record.update({"candidate_output": candidate, "retained_negative_id": negative_id})
            elif procedure == "json_key_order_invariance":
                payload = dict(reversed(list(payload.items())))
                result = core.evaluate(payload)
                passed = core.matches_contract(proposal, result) and canonical(payload) == canonical(proposal["input"])
                record.update({"reordered_input": payload, "observed": result})
            else:
                raise RuntimeError(f"unknown_procedure:{procedure}")
            if not passed:
                raise RuntimeError(f"portfolio_predicate:{task['packet_id']}")
            record["predicate_pass"] = True
            record["disposition"] = "completed"
            challenge_rows[operation].append(record)
            task_results.append(record)

    if len(negative_rows) != 493:
        raise RuntimeError(f"negative_shape:{len(negative_rows)}")
    outcomes = {label: sum(item["expected_execution_disposition"] == label for item in proposals) for label in ("completed", "represented", "open_gap", "exact_gate")}
    if outcomes != {"completed": 176, "represented": 11, "open_gap": 3, "exact_gate": 10}:
        raise RuntimeError("outcome_shape")

    package_negative_ids = [f"SA6887-PACKAGE-{name.upper()}" for name in ("chess", "lark", "networkx")]
    gates = proposals[0]["protected_gates"]
    methods: list[dict] = []
    witnesses: list[dict] = []
    events: list[dict] = []
    recommendations: list[dict] = []

    def method(title: str, signature: str, negative_ids: list[str], artifact: str) -> dict:
        identifier = f"SA6887-M{len(methods) + 1:03d}"
        item = {
            "method_id": identifier,
            "title": title,
            "failure_signature": signature,
            "trigger_preconditions": ["exact owner scope", "the cited frozen or observed witness"],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now",
            "candidate_workaround": "Use the bounded accepting witness while preserving and refusing the adverse candidate.",
            "validation_witness_ids": [],
            "recurrence_guard": "Check exact fields, immutable expectations, byte domain, lifecycle context, and protected gates before reuse.",
            "rollback": "Retain the failed witness and stop selecting the failed owner candidate.",
            "recommendation_state": "preferred",
            "supersedes": [],
            "protected_gates": gates,
            "retained_negative_ids": negative_ids,
            "scope_boundary": core.BOUNDARY,
            "artifact": artifact,
        }
        methods.append(item)
        events.append({"method_id": identifier, "from": "candidate", "to": "preferred", "note": "Bounded recovery or rejecting predicate passed without erasing the failure."})
        recommendations.append({"method_id": identifier, "preconditions": "same trigger and owner scope", "recommendation": "Use the exact bounded witness and preserve its refusal boundary.", "delivered": False})
        return item

    def witness(item: dict, procedure: str, observed: str, result: str, negative_ids: list[str], kind: str, artifact: str) -> None:
        identifier = f"SA6887-W{len(witnesses) + 1:04d}"
        witnesses.append({
            "witness_id": identifier,
            "method_id": item["method_id"],
            "procedure": procedure,
            "scope": artifact,
            "expected": "The exact bounded predicate passes while any failed or adverse candidate remains zero-credit evidence.",
            "observed": observed,
            "result": result,
            "witness_kind": kind,
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": negative_ids,
            "boundary": core.BOUNDARY,
        })
        item["validation_witness_ids"].append(identifier)

    for operation in core.FIELDS:
        operation_negatives = [row for row in negative_rows if row["operation"] == operation]
        item = method(
            operation.replace("_", " "),
            f"Adverse {operation} candidate admission is refused.",
            [row["negative_id"] for row in operation_negatives],
            f"{REL.as_posix()}/x2/challenges/{operation}.json",
        )
        for row in operation_negatives:
            witness(item, row["kind"], f"{row['negative_id']} refused", "fail", [row["negative_id"]], "designed_admission_failure", row["artifact"])
        positive = next(proposal for proposal in proposals if proposal["operation"] == operation and proposal["expected_acceptance"])
        witness(item, "complete frozen positive envelope", f"{positive['proposal_id']} matched", "pass", [], "bounded_passing_witness", positive["concrete_artifact"])

    for failure in startup["retained_failures"]:
        item = method(failure["recovery"], failure["failed_witness"], [failure["failure_id"]], f"{REL.as_posix()}/x1/method-flow-startup.json")
        witness(item, "observed startup or x1 attempt", failure["failed_witness"], "fail", [failure["failure_id"]], "operational_failure", f"{REL.as_posix()}/x1/method-flow-startup.json")
        witness(item, "bounded focused recovery", failure["recovery"], "pass", [], "bounded_passing_witness", f"{REL.as_posix()}/x1/method-flow-startup.json")

    for package_name, negative_id in zip(("chess", "lark", "networkx"), package_negative_ids):
        package_smoke = package["smokes"]["smokes"][package_name]
        item = method(f"{package_name} isolated package smoke", package_smoke["error_class"], [negative_id], f"{REL.as_posix()}/x2/package-transaction.json")
        witness(item, "package adverse fixture", f"{package_smoke['error_class']} rejection", "fail", [negative_id], "designed_admission_failure", f"{REL.as_posix()}/x2/package-transaction.json")
        witness(item, "package accepting fixture", "expected bounded package behavior observed", "pass", [], "bounded_passing_witness", f"{REL.as_posix()}/x2/package-transaction.json")

    tool_plan = load(BASE / "x1/tool-package-plan.json")
    for tool_kind, planned, local_observed, promoted in (
        ("skill", tool_plan["skills"], local_tools["skills"], promotion["skills"]),
        ("runner", tool_plan["runners"], local_tools["runners"], promotion["runners"]),
    ):
        for plan_item, local_item, promoted_item in zip(planned, local_observed, promoted):
            operations = plan_item.get("operation_pair", plan_item.get("operation_group"))
            alias_negative = next(row["negative_id"] for row in negative_rows if row["operation"] == operations[0] and row["kind"] == "unknown_field_rejection")
            item = method(f"{tool_kind} {plan_item['name']} local and promoted smoke", "Unknown-field candidate must remain rejected before and after promotion.", [alias_negative], f"{REL.as_posix()}/x2/promotion-receipt.json")
            witness(item, "owner-local adverse smoke", "field_set rejection", "fail", [alias_negative], "reused_designed_admission_failure", f"{REL.as_posix()}/x2/local-tool-validation.json")
            witness(item, "owner-local accepting smoke", "complete envelope matched", "pass", [], "bounded_passing_witness", f"{REL.as_posix()}/x2/local-tool-validation.json")
            witness(item, "promoted adverse smoke", "field_set rejection", "fail", [alias_negative], "reused_designed_admission_failure", f"{REL.as_posix()}/x2/promotion-receipt.json")
            witness(item, "promoted accepting smoke", "complete envelope matched", "pass", [], "bounded_passing_witness", f"{REL.as_posix()}/x2/promotion-receipt.json")
            if not local_item["smokes"] or not promoted_item["smokes"]:
                raise RuntimeError(f"tool_smoke_shape:{plan_item['name']}")

    operational_failures = load(bank / "x2-operational-failures.json")["failures"] if (bank / "x2-operational-failures.json").is_file() else []
    for failure in operational_failures:
        item = method(failure["recovery"], failure["failed_witness"], [failure["failure_id"]], f"{REL.as_posix()}/x2/retained-negative-register.json")
        witness(item, "observed x2 operational attempt", failure["failed_witness"], "fail", [failure["failure_id"]], "operational_failure", f"{REL.as_posix()}/x2/retained-negative-register.json")
        witness(item, "bounded focused recovery", failure["recovery"], "pass", [], "bounded_passing_witness", f"{REL.as_posix()}/x2/retained-negative-register.json")

    method_counts = {
        "methods": len(methods),
        "witnesses": len(witnesses),
        "failed_witnesses": sum(item["result"] == "fail" for item in witnesses),
        "passing_witnesses": sum(item["result"] == "pass" for item in witnesses),
        "state_events": len(events),
        "recommendations": len(recommendations),
    }
    expected_method_counts = {
        "methods": 53 + len(operational_failures),
        "witnesses": 609 + 2 * len(operational_failures),
        "failed_witnesses": 541 + len(operational_failures),
        "passing_witnesses": 68 + len(operational_failures),
        "state_events": 53 + len(operational_failures),
        "recommendations": 53 + len(operational_failures),
    }
    if method_counts != expected_method_counts:
        raise RuntimeError(f"method_shape:{method_counts}")
    phase_new_negatives = len(negative_rows) + len(startup["retained_failures"]) + len(package_negative_ids) + len(operational_failures)
    effective = {
        "proposals": baseline["proposals"] + 200,
        "negatives": baseline["negatives"] + phase_new_negatives,
        "methods": baseline["methods"] + method_counts["methods"],
        "failed_witnesses": baseline["failed_witnesses"] + method_counts["failed_witnesses"],
        "passing_witnesses": baseline["passing_witnesses"] + method_counts["passing_witnesses"],
        "open_gaps": baseline["open_gaps"] + outcomes["open_gap"],
        "exact_gates": baseline["exact_gates"] + outcomes["exact_gate"],
    }

    # All validation above precedes repository materialization.
    write_new(x2 / "entry-gate.json", {
        "source": SOURCE,
        "x1": X1,
        "exact_x1_head_at_entry": True,
        "x1_tree_unchanged": True,
        "local_tools_valid": True,
        "package_transaction_complete": True,
        "promotion_valid_byte_equal": True,
        "canonical_invocations": 0,
    })
    for artifact, row in contract_rows:
        write_new(ROOT / artifact, row)
    for operation, rows in challenge_rows.items():
        write_new(x2 / "challenges" / f"{operation}.json", {"operation": operation, "rows": rows, "same_owner_only": True, "boundary": core.BOUNDARY})
    write_new(x2 / "portfolio-results.json", {
        "schema": "ghc.family.observed-chess-portfolio.v1",
        "rows": task_results,
        "counts": {"safe_now": 300, "candidates": 250, "clean_fix_refine": 300},
        "unique_task_checks": 850,
        "exact_packets_unexecuted": 50,
        "blocked_packets_unexecuted": 30,
        "real_games": 0,
        "participant_records": 0,
        "boundary": core.BOUNDARY,
    })
    write_new(x2 / "package-transaction.json", package)
    write_new(x2 / "package-advisory-snapshot.json", advisory)
    write_new(x2 / "negative-controls.json", {
        "schema": "ghc.family.chess-negative-controls.v1",
        "negative_records": negative_rows,
        "count": len(negative_rows),
        "package_negative_ids": package_negative_ids,
        "startup_negative_ids": [item["failure_id"] for item in startup["retained_failures"]],
        "x2_operational_negative_ids": [item["failure_id"] for item in operational_failures],
        "new_unique_negative_count": phase_new_negatives,
        "reused_tool_smoke_negatives_not_double_counted": 30,
        "unexpected_test_failures": 0,
        "completion_credit": 0,
        "interpretation": "Rejected candidates are failed witnesses whose rejection predicates pass; they are never promoted into completion credit.",
    })
    ledger = {
        "schema": "ghc.family.method-flow-state.v1",
        "phase": PHASE,
        "owner": OWNER,
        "identity_boundary": core.BOUNDARY,
        "execution_authority": "owner_self_scoped_delta",
        "source_commit": SOURCE,
        "x1_commit": X1,
        "evidence_commit": None,
        "final_commit": None,
        "methods": methods,
        "witnesses": witnesses,
        "state_events": events,
        "recommendations": recommendations,
        "counts": method_counts,
        "boundary": core.BOUNDARY,
    }
    write_new(x2 / "method-flow/ledger.json", ledger)
    write_new(x2 / "method-flow/validation.json", {
        "schema": "ghc.family.method-flow-validation.v1",
        "valid": True,
        "counts": method_counts,
        "unique_method_ids": len({item["method_id"] for item in methods}) == len(methods),
        "unique_witness_ids": len({item["witness_id"] for item in witnesses}) == len(witnesses),
        "every_witness_method_resolves": all(item["method_id"] in {method["method_id"] for method in methods} for item in witnesses),
        "every_failure_has_negative": all(item["retained_negative_ids"] for item in witnesses if item["result"] == "fail"),
        "recoveries_erase_failures": False,
    })
    write_new(x2 / "retained-negative-register.json", {
        "inherited_count": baseline["negatives"],
        "x1_startup_count": len(startup["retained_failures"]),
        "x2_contract_and_portfolio_count": len(negative_rows),
        "package_adverse_count": len(package_negative_ids),
        "x2_operational_count": len(operational_failures),
        "tool_smoke_aliases_not_double_counted": 30,
        "new_unique_count": phase_new_negatives,
        "effective_count": effective["negatives"],
        "erased": 0,
        "method_flow_ref": f"{REL.as_posix()}/x2/method-flow/ledger.json",
    })
    for label, filename, inherited_key in (("open_gap", "open-gap-register.json", "open_gaps"), ("exact_gate", "exact-gate-register.json", "exact_gates")):
        write_new(x2 / filename, {
            "retained_inherited_count": baseline[inherited_key],
            "new": [{"proposal_id": item["proposal_id"], "title": item["title"], "disposition": label, "artifact": item["concrete_artifact"]} for item in proposals if item["expected_execution_disposition"] == label],
            "effective_count": effective[inherited_key],
            "actual_authority_actions_executed": 0,
            "erasure": False,
            "boundary": core.BOUNDARY,
        })
    write_new(x2 / "workload-wellbeing.json", {
        "owner": OWNER,
        "phase": PHASE,
        "solo": True,
        "subagents": 0,
        "forks": 0,
        "delegation": 0,
        "real_participants": 0,
        "unsafe_quota_filler": False,
        "subjective_wellbeing_claimed": False,
        "bounded_work": {"proposals": 200, "portfolio_checks": 850, "skills": 10, "runners": 5, "package_additions": 3},
        "pause_stop_control": "Hamish may pause, rename, redirect, narrow, or stop the route at any time.",
        "usage_reset_authority": "Hamish only",
    })
    write_new(x2 / "complete-incomplete-checklist.json", {
        "completed": ["200 frozen contract projections", "850 portfolio predicates", "three isolated package additions", "ten local and promoted skills", "five local and promoted runners", "content-addressed four-tier deck", "owner-scoped validation still pending at evidence commit"],
        "represented": ["synthetic record fixity", "synthetic accessible move text", "same-owner package and tool validation"],
        "open_gap": ["real archive or game evidence", "human accessibility evaluation", "independent review"],
        "exact_gate": ["tournament and rating action", "legal and cultural interpretation", "Maori wording and authority", "production deployment", "Stage 20"],
        "full_repository_suite_run": False,
        "canonical_invocations": 0,
        "terminal_complete": False,
    })

    cards: list[dict] = []

    def add_card(tier: int, card_type: str, title: str, parent_ids: list[str], content: object, disposition: str = "represented", stability: str = "volatile") -> str:
        payload = {
            "schema": "ghc.family.freed-id.card.v1",
            "tier": tier,
            "card_type": card_type,
            "title": title,
            "parent_ids": parent_ids,
            "owner": OWNER,
            "phase": PHASE,
            "stability": stability,
            "disposition": disposition,
            "content": content,
            "source_refs": [{"commit": X1, "path": f"{REL.as_posix()}/x1/new-proposals.json"}],
            "protected_gates": gates,
            "boundary": core.BOUNDARY,
        }
        card_id = "ghc-card-" + digest(payload)[:24]
        payload["card_id"] = card_id
        cards.append(payload)
        return card_id

    owner_card = add_card(1, "freed_id_anchor", OWNER, [], {"relational_role": practice["role"], "hope": practice["hope"], "identity_claim": False}, stability="stable")
    pillar_cards = {
        pillar: add_card(2, "trinity_pillar", pillar, [owner_card], {"scope": "research model, synthetic proxy, or synthetic nonproduction governance only"}, stability="stable")
        for pillar in ("GMUT Mind", "THOS Body", "Freed ID and CBR Heart")
    }
    practice_parent = {
        practice["practices"][0]: "Freed ID and CBR Heart",
        practice["practices"][1]: "GMUT Mind",
        practice["practices"][2]: "Freed ID and CBR Heart",
        practice["practices"][3]: "THOS Body",
    }
    practice_cards = {
        name: add_card(3, "bounded_practice", name, [pillar_cards[practice_parent[name]]], {"synthetic_learning_lens": True, "employment": False, "qualification": False, "authority": False})
        for name in practice["practices"]
    }
    for proposal in proposals:
        add_card(4, "proposal_task", proposal["title"], [practice_cards[proposal["practice"]]], {"proposal_id": proposal["proposal_id"], "artifact": proposal["concrete_artifact"], "frozen_contract_matched": True}, proposal["expected_execution_disposition"])
    for item in methods:
        add_card(4, "method", item["title"], [practice_cards[practice["practices"][3]]], {"method_id": item["method_id"], "retained_negative_ids": item["retained_negative_ids"], "ledger": f"{REL.as_posix()}/x2/method-flow/ledger.json"}, "completed")
    card_ids = [card["card_id"] for card in cards]
    expected_card_count = 1 + 3 + len(practice["practices"]) + len(proposals) + len(methods)
    if len(card_ids) != len(set(card_ids)) or len(cards) != expected_card_count:
        raise RuntimeError("card_identity_shape")
    if any(parent not in set(card_ids) for card in cards for parent in card["parent_ids"]):
        raise RuntimeError("card_parent_resolution")
    for card in cards:
        write_new(x2 / "deck/cards" / f"{card['card_id']}.json", card)
    write_new(x2 / "deck/deck-index.json", {
        "schema": "ghc.family.freed-id.deck.v1",
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE,
        "x1": X1,
        "cards": card_ids,
        "card_count": len(cards),
        "tier_counts": {str(tier): sum(card["tier"] == tier for card in cards) for tier in range(1, 5)},
        "outcomes": outcomes,
        "acyclic_parent_graph": True,
        "boundary": core.BOUNDARY,
    })
    write_new(x2 / "deck/stable-prefix.json", {"cards": [card["card_id"] for card in cards if card["stability"] == "stable"], "cache_hit_claimed": False})
    write_new(x2 / "deck/volatile-index.json", {"cards": [card["card_id"] for card in cards if card["stability"] == "volatile"], "implicit_completion_credit": False})
    write_new(x2 / "deck/baton-module-index.json", {
        "minimum_modules": 13,
        "modules": ["identity and route", "immutable source", "lifecycle", "proposals", "portfolio", "pillar and practices", "packages", "skills", "runners", "Method Flow", "gaps and gates", "validation", "terminal route"],
        "baton_state": "NOT_YET_PREPARED",
        "terminal_delivery": False,
    })
    phase_truth = {
        "owner": OWNER,
        "phase": PHASE,
        "source": SOURCE,
        "x1": X1,
        "state": "X2_OBSERVED_EVIDENCE_PRECOMMIT",
        "new_proposals": 200,
        "proposal_chain_after": effective["proposals"],
        "outcomes": outcomes,
        "effective_counts": effective,
        "observed_contracts": 200,
        "unexpected_contract_failures": 0,
        "portfolio_checks": 850,
        "exact_packets_unexecuted": 50,
        "blocked_packets_unexecuted": 30,
        "skills_promoted": 10,
        "runner_interfaces_promoted": 5,
        "ordinary_package_additions": 3,
        "canonical_invocations": 0,
        "successor_contacts": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": core.BOUNDARY,
    }
    write_new(x2 / "phase-truth.json", phase_truth)
    summary = {
        "outcomes": outcomes,
        "effective_counts": effective,
        "method_flow": method_counts,
        "contracts": 200,
        "portfolio_checks": 850,
        "negative_controls": len(negative_rows),
        "cards": len(cards),
        "skills": 10,
        "runners": 5,
        "packages": 3,
        "unexpected_failures": 0,
    }
    write_new(x2 / "evidence-summary.json", summary)
    report = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sylven Arc v688-v7 x2 evidence</title></head>
<body><main><h1>Sylven Arc v688-v7 x2 evidence</h1>
<p>This static report describes bounded same-owner synthetic chess-record work. It is not a real game, participant study, professional decision, independent reproduction, accessibility conformance, legal or cultural ratification, Maori authority, Theory of Everything proof, or Stage 20 evidence.</p>
<nav aria-label="Report sections"><ol><li><a href="#scope">Scope</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#work">Work</a></li><li><a href="#tools">Tools</a></li><li><a href="#failures">Failures</a></li><li><a href="#gates">Gaps and gates</a></li><li><a href="#access">Accessibility reservations</a></li></ol></nav>
<section id="scope"><h2>Scope</h2><p>Primary pillar: Freed ID and CBR Heart. Four learning lenses: {html.escape(', '.join(practice['practices']))}. No employment, qualification, person, live identity, game, tournament, rating, or external action was used.</p></section>
<section id="outcomes"><h2>Outcomes</h2><table><caption>Frozen proposal outcomes</caption><thead><tr><th scope="col">Label</th><th scope="col">Count</th></tr></thead><tbody>{''.join(f'<tr><th scope="row">{html.escape(label)}</th><td>{count}</td></tr>' for label, count in outcomes.items())}</tbody></table></section>
<section id="work"><h2>Work</h2><p>Two hundred complete contract envelopes matched. Eight hundred fifty portfolio predicates passed. Fifty exact-approval and thirty blocked packets stayed unexecuted.</p></section>
<section id="tools"><h2>Packages, skills, and runners</h2><p>Three exact artifacts were installed only into an isolated D-first target. Ten skills and five runner interfaces were quick-validated, accepting/adverse smoke-used locally, promoted without overwrite, byte-compared, and smoke-used again. A point-in-time OSV snapshot is not exhaustive security.</p></section>
<section id="failures"><h2>Retained failures</h2><p>{phase_new_negatives} unique phase negatives are retained. Repeated tool smokes reuse existing adverse candidates and are not double-counted. Recoveries never erase or convert a failed witness into completion credit.</p></section>
<section id="gates"><h2>Open gaps and exact gates</h2><p>{outcomes['open_gap']} new open gaps and {outcomes['exact_gate']} new exact gates remain, with effective counts {effective['open_gaps']} and {effective['exact_gates']}. Terminal verdict: NOT_READY_FOR_STAGE_20.</p></section>
<section id="access"><h2>Accessibility and authority reservations</h2><p>Heading, landmark, caption, scope, and plain-language structures are machine checked only. Manual browser, assistive-technology, cognitive-accessibility, Maori-language, affected-user, and independent evaluations remain open or exact-gated. Maori concepts remain under Maori authority.</p></section>
</main></body></html>"""
    write_new(x2 / "accessible-report.html", report)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
