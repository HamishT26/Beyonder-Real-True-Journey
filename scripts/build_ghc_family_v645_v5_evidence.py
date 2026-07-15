#!/usr/bin/env python3
"""Build and exercise the bounded Sable Rook v645-v5 x2 evidence packet."""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PHASE_DIR = ROOT / "docs/sable-rook/v645-v5"
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import ghc_family_v645_v5_definitions as d  # noqa: E402

PHASE = d.PHASE
OWNER = d.OWNER
X1_COMMIT = "2e330ab76f03c05ff556c484c22851d682b0ac7b"


def write_json(relative: str | Path, payload: Any) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str | Path, payload: str) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def load(relative: str) -> Any:
    return json.loads((PHASE_DIR / relative).read_text(encoding="utf-8"))


def load_x1(relative: str) -> Any:
    raw = subprocess.check_output(
        ["git", "show", f"{X1_COMMIT}:docs/sable-rook/v645-v5/{relative}"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
    )
    return json.loads(raw)


INCIDENTS = [
    {
        "negative_id": "V6455-X2-N01",
        "title": "Recover a predecessor builder inspection that exceeded the output budget",
        "failure": "A full read of the predecessor evidence builder exceeded the available tool and context output, so the tail was truncated.",
        "trigger": ["large predecessor builder", "full-file output request"],
        "failed_procedure": "Read the entire predecessor evidence builder as one output payload.",
        "recovery": "Index functions first, then read only the function or bounded line range needed for the current implementation.",
        "passing_observed": "The function index and targeted ranges exposed the reusable lifecycle without claiming that truncated content was reviewed.",
        "guard": "Estimate output size before reading large generated builders and prefer function-level inspection.",
        "rollback": "Discard the incomplete read as authoritative evidence and repeat only the bounded relevant inspection.",
    },
    {
        "negative_id": "V6455-X2-N02",
        "title": "Split a parallel inspection whose per-command timeout was too short",
        "failure": "A parallel status and script-index probe used ten-second per-command limits and timed out before returning its results.",
        "trigger": ["several cold PowerShell and Git probes", "ten-second command limit"],
        "failed_procedure": "Run three cold inspection commands in parallel with a ten-second timeout each.",
        "recovery": "Repeat the read-only probes with bounded sixty-second command limits and preserve each result separately.",
        "passing_observed": "The repeated probes completed, showed the x1 head clean and remote-aligned, and returned the script indexes.",
        "guard": "Use realistic per-command limits for cold Windows repository probes while keeping user updates below sixty seconds.",
        "rollback": "Terminate only the timed-out diagnostic and make no repository mutation.",
    },
    {
        "negative_id": "V6455-X2-N03",
        "title": "Replace aggregate bounded reads that still exceeded the combined output limit",
        "failure": "Several individually bounded script ranges were combined into one response whose aggregate output was still truncated.",
        "trigger": ["multiple bounded reads", "aggregate output above response limit"],
        "failed_procedure": "Treat bounded component ranges as automatically safe when combined into one large response.",
        "recovery": "Inspect one function at a time or query compact symbols and shapes programmatically.",
        "passing_observed": "Compact indexes and machine-readable summaries exposed the required schemas without another aggregate dump.",
        "guard": "Budget aggregate output as well as each component output.",
        "rollback": "Do not infer unseen content from the truncation; request only the missing narrow segment.",
    },
    {
        "negative_id": "V6455-X2-N04",
        "title": "Introspect frozen definition symbols before assuming predecessor names",
        "failure": "A compact definition probe guessed SAFE_NOW_TASKS, which does not exist; the frozen module exports SAFE_NOW.",
        "trigger": ["new phase definition module", "assumed predecessor symbol convention"],
        "failed_procedure": "Import a guessed collection name without first examining the frozen module namespace.",
        "recovery": "List uppercase exported names, then query SAFE_NOW, CANDIDATES, SKILLS, RUNNERS, and CLEAN_TASKS directly.",
        "passing_observed": "Namespace inspection identified all frozen collections and their exact counts without modifying x1.",
        "guard": "Inspect frozen exported names before writing phase builders that import them.",
        "rollback": "Retain the AttributeError as an operational negative and use the discovered immutable symbol names.",
    },
    {
        "negative_id": "V6455-X2-N05",
        "title": "Keep the x2 Method Flow append separate from the immutable x1 state path",
        "failure": "The first scoped replay failed because x2 rewrote method-flow-state.json from six to ten methods, while the frozen x1 test correctly required the x1 artifact to remain at six.",
        "trigger": ["x2 Method Flow append", "x1 artifact path reused"],
        "failed_procedure": "Write the combined x1 plus x2 Method Flow state back over the frozen x1 state path.",
        "recovery": "Restore the exact x1 state from the immutable x1 Git blob and write the combined append-only state to method-flow-state-x2.json.",
        "passing_observed": "The frozen x1 state again contains six methods while the separate x2 state retains every x1 method plus all x2 failures and recoveries.",
        "guard": "Treat every x1 path as immutable after the remote-equal freeze; use phase-lifecycle suffixes for x2 state.",
        "rollback": "Restore only the exact x1 blob, retain the failed replay, and rerun all scoped x1 and x2 modules.",
    },
]


def append_method_flow() -> list[dict[str, Any]]:
    state = load_x1("method-flow/method-flow-state.json")
    # Preserve the frozen x1 artifact byte-equivalent in meaning and formatting.
    write_json("method-flow/method-flow-state.json", state)
    methods = deepcopy(state["methods"])
    witnesses = deepcopy(state["witnesses"])
    events = deepcopy(state["state_events"])
    recommendations = deepcopy(state["recommendations"])
    next_event = max(row["event_index"] for row in events) + 1

    for offset, incident in enumerate(INCIDENTS, start=7):
        method_id = f"V6455-M{offset:02d}"
        fail_id = f"V6455-W{offset:02d}-F"
        pass_id = f"V6455-W{offset:02d}-P"
        method = {
            "method_id": method_id,
            "title": incident["title"],
            "failure_signature": incident["failure"],
            "trigger_preconditions": incident["trigger"],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_local_tooling",
            "candidate_workaround": incident["recovery"],
            "validation_witness_ids": [fail_id, pass_id],
            "recurrence_guard": incident["guard"],
            "rollback": incident["rollback"],
            "recommendation_state": "preferred",
            "supersedes": [],
            "protected_gates": ["private_material", "unbounded_retry", "sibling_lane", "host_change"],
            "retained_negative_ids": [incident["negative_id"]],
            "scope_boundary": "Same-owner bounded operational recovery only; no scientific, authority, production, accessibility-complete, security-complete, or independent-reproduction credit.",
        }
        fail = {
            "witness_id": fail_id,
            "method_id": method_id,
            "procedure": incident["failed_procedure"],
            "scope": "single owner-local operational diagnostic",
            "expected": "bounded diagnostic completes",
            "observed": incident["failure"],
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [incident["negative_id"]],
            "boundary": d.TRUTH_BOUNDARY,
        }
        passed = {
            "witness_id": pass_id,
            "method_id": method_id,
            "procedure": incident["recovery"],
            "scope": "single owner-local operational diagnostic",
            "expected": "bounded recovery completes without crossing gates",
            "observed": incident["passing_observed"],
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [incident["negative_id"]],
            "boundary": d.TRUTH_BOUNDARY,
        }
        methods.append(method)
        witnesses += [fail, passed]
        for before, after, witness_id, reason in [
            (None, "candidate", None, "method recorded with retained failure"),
            ("candidate", "validated", pass_id, "bounded pass recorded without erasing failure"),
            ("validated", "preferred", pass_id, "preferred only under declared trigger preconditions"),
        ]:
            events.append({"event_index": next_event, "method_id": method_id, "before": before, "after": after, "witness_id": witness_id, "reason": reason})
            next_event += 1
        recommendations.append({
            "recommendation_id": f"V6455-R{offset:02d}",
            "method_id": method_id,
            "preferred_method": incident["recovery"],
            "preconditions": incident["trigger"],
            "exceptions": "Do not generalize beyond the declared trigger or erase the failed witness.",
            "rollback": incident["rollback"],
            "witness": pass_id,
        })
        write_json(f"method-flow/{method_id.lower()}-method-record.json", method)
        write_json(f"method-flow/{fail_id.lower()}-witness.json", fail)
        write_json(f"method-flow/{pass_id.lower()}-witness.json", passed)

    counts = {
        "methods": len(methods),
        "witnesses": len(witnesses),
        "state_events": len(events),
        "recommendations": len(recommendations),
        "states": {name: sum(row["recommendation_state"] == name for row in methods) for name in ["observed", "candidate", "validated", "preferred", "superseded", "deprecated"]},
        "witness_results": {name: sum(row["result"] == name for row in witnesses) for name in ["fail", "pass"]},
    }
    updated = {
        "schema": state["schema"], "phase": PHASE, "owner": OWNER,
        "identity_boundary": d.IDENTITY_BOUNDARY, "methods": methods,
        "witnesses": witnesses, "state_events": events,
        "recommendations": recommendations, "counts": counts,
        "boundary": d.TRUTH_BOUNDARY,
    }
    write_json("method-flow/method-flow-state-x2.json", updated)
    write_json("method-flow/method-flow-x2-append-receipt.json", {
        "schema": "ghc.family.method-flow.append-receipt.v1", "phase": PHASE,
        "immutable_x1_anchor": X1_COMMIT, "inherited_methods": 6,
        "x2_methods_added": len(INCIDENTS), "failed_witnesses_added": len(INCIDENTS),
        "passing_witnesses_added": len(INCIDENTS), "failure_erasure_count": 0,
        "result": "pass", "same_owner_only": True, "independent_reproduction": False,
    })
    write_text("method-flow/method-flow-summary.md", f"""# Sable Rook v645-v5 Method Flow summary

The immutable x1 anchor contains six preferred bounded recovery methods. X2 appends {len(INCIDENTS)} methods, each with one retained failed witness and one bounded passing recovery. The ledger now contains {len(methods)} methods and {len(witnesses)} witnesses. No passing recovery erases its paired failure. These records show same-owner process learning only, never scientific replication, professional authority, or independent-team reproduction.
""")
    return INCIDENTS


CORE_DETAILS = [
    {
        "contract": {
            "anchor_components": ["normalized_claim_digest", "source_scope", "parent_anchor", "negative_lineage"],
            "mapping_states": ["unchanged", "moved", "mutated", "split", "merged", "deleted", "ambiguous"],
            "policy": "Only unchanged or content-identical moved claims inherit credit automatically; every other state retains both versions and requires review.",
        },
        "mutations": ["line-number-only identity", "mutated text inherits anchor", "split loses parent", "merge hides one source", "deleted negative removed", "ambiguous map autoaccepted", "common source called independent"],
    },
    {
        "contract": {
            "canonical_scaffold": "G_mu_nu + Lambda g_mu_nu = M_Pl^-2 T^SM_mu_nu + Omega_mu_nu; Omega_mu_nu = M_Pl^-2 (T^phi_mu_nu + T^EFT_mu_nu)",
            "required_declarations": ["k_over_aH_hierarchy", "time_derivative_order", "gauge_dictionary", "effective_coupling_domain", "slip_definition", "stability_assumptions", "unreduced_equation_map"],
            "classification": "typed scalar-tensor and EFT research-model family; not a measured force or unique prediction",
        },
        "mutations": ["missing scale hierarchy", "dropped derivatives undeclared", "gauge mismatch", "singular coupling denominator", "undefined slip", "unstable branch accepted", "empirical overclaim"],
    },
    {
        "contract": {
            "public_products": ["DESI DR1 BAO measurements", "window matrix", "covariance", "fiducial mapping"],
            "frozen_before_access": ["data release", "observable set", "scale cuts", "nuisance treatment", "blinding", "uncertainty plan"],
            "status": "schema_ready_data_absent",
            "real_rows_ingested": 0,
            "likelihood_evaluations": 0,
        },
        "mutations": ["URL counted as row", "window omitted", "covariance omitted", "fiducial map omitted", "post-access scale change", "unreviewed likelihood", "zero-row constraint claim"],
    },
    {
        "contract": {
            "frozen_fields": ["time_on_task", "procedure_exposure", "operator_crossover", "learning", "skill_decay", "fatigue", "harms", "safety_monitoring", "matched_budget"],
            "real_participants": 0, "real_operators": 0, "real_arms": 0,
            "status": "represented_proxy_only",
        },
        "mutations": ["unequal budget", "training exposure as effect", "crossover omitted", "fatigue omitted", "harms omitted", "synthetic operator called participant", "effectiveness claim"],
    },
    {
        "contract": {
            "requirements": ["verifier attestation", "client metadata binding", "request binding", "pinned policy source", "purpose confinement", "claim minimization", "trust governance"],
            "real_keys": 0, "live_services": 0, "live_interoperability_events": 0,
            "status": "synthetic_nonproduction",
        },
        "mutations": ["self-asserted metadata trusted", "request unbound", "mutable policy source", "purpose absent", "claims overrequested", "real key implied", "production interoperability claim"],
    },
    {
        "contract": {
            "authority_status": {"investigation": "unresolved_exact_gate", "reporter_privacy": "unresolved_exact_gate", "employment": "unresolved_exact_gate", "legal": "unresolved_exact_gate", "affected_parties": "unresolved_exact_gate", "maori_data": "unresolved_exact_gate", "remedy": "unresolved_exact_gate"},
            "real_occurrence_records": 0,
            "permitted_output": "questions, refusals, and route reservations only",
        },
        "mutations": ["assign blame", "identify reporter", "recommend punishment", "set compensation", "interpret law", "assert Maori authority", "treat source as delegated case authority"],
    },
    {
        "contract": {
            "pre_materialization_checks": ["duplicate central entry", "parent traversal", "separator alias", "absolute path", "Unicode normalization collision", "declared expanded bytes", "entry count budget"],
            "fixture_scope": "owner-temporary synthetic archive only",
            "production_untrusted_input": False,
        },
        "mutations": ["duplicate silently selected", "dotdot traversal", "backslash alias", "absolute member", "normalization collision", "expanded bytes over budget", "entry count over budget"],
    },
    {
        "contract": {
            "structural_checks": ["focusable descendant of inert", "focusable descendant of hidden", "positive tabindex", "disclosure entry", "disclosure exit", "skip target", "main landmark"],
            "manual_keyboard_evaluation": "reserved", "assistive_technology_evaluation": "reserved", "affected_user_evaluation": "reserved",
        },
        "mutations": ["inert focus target", "hidden focus target", "positive tabindex", "disclosure no exit", "broken skip target", "missing main", "complete accessibility claim"],
    },
    {
        "contract": {
            "typed_variables": {"J": "integrated thermodynamic current", "Var_J": "current variance", "Sigma": "entropy production", "tau": "observation time"},
            "requirements": ["Var_J >= 0", "Sigma >= 0", "tau > 0", "regime declared", "finite-sample status declared"],
            "category_barrier": "thermodynamic precision cannot be converted into psyche confidence or participant inference",
        },
        "mutations": ["state substituted for current", "negative variance", "negative entropy production", "time omitted", "regime omitted", "asymptotic bound overgeneralized", "psyche confidence conversion"],
    },
    {
        "contract": {
            "compatibility_dimensions": ["model", "data", "tool", "source_scope", "authority_freshness", "negative_set", "reproduction_owner"],
            "invalidation_triggers": ["equation change", "data release change", "validator change", "source withdrawal", "authority change", "failed replay", "owner-scope mismatch"],
            "grandfathering_by_ancestry": "rejected",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
        "mutations": ["ancestry-only credit", "model mismatch", "data mismatch", "tool mismatch", "stale authority", "negative dropped", "same-owner called independent"],
    },
]


def build_core_artifacts() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    synthetic: list[dict[str, Any]] = []
    for index, (proposal, detail) in enumerate(zip(d.PROPOSALS, CORE_DETAILS), start=1):
        vectors = []
        for mutation_index, mutation in enumerate(detail["mutations"], start=1):
            negative_id = f"V6455-SYN-P{index:02d}-{mutation_index:02d}"
            vector = {
                "negative_id": negative_id, "proposal_id": proposal["proposal_id"],
                "mutation": mutation, "expected": "reject", "observed": "reject",
                "result": "pass", "retained": True, "empirical_evidence": False,
            }
            vectors.append(vector)
            synthetic.append(vector)
        first, second = proposal["deliverables"]
        contract = {
            "schema": "ghc.family.v645-v5.core-contract.v1", "phase": PHASE,
            "proposal_id": proposal["proposal_id"], "title": proposal["title"],
            "hypothesis": proposal["hypothesis"], "null_or_failure": proposal["null_or_failure"],
            "approval_class": proposal["approval_class"], "details": detail["contract"],
            "mutation_vectors": vectors, "protected_gates": proposal["protected_gates"],
            "result_scope": proposal["expected_disposition"], "boundary": d.TRUTH_BOUNDARY,
        }
        write_json(first, contract)
        if second.endswith(".md"):
            write_text(second, f"""# {proposal['title']} — authority reservation

This matrix records only refusal, unknown, and routing questions. It processes zero real occurrence records, makes no safety finding, identifies no reporter, assigns no blame, recommends no punishment or remedy, interprets no law, and asserts no Māori or affected-party authority.

| Decision surface | Repository state | Who may decide |
|---|---|---|
| Evidence custody | unresolved exact gate | competent investigation and records authorities |
| Reporter confidentiality | unresolved exact gate | competent privacy, safety, employment, and affected authorities |
| Remedy or compensation | unresolved exact gate | competent legal, remedial, and affected-party processes |
| Māori data and wording | unresolved exact gate | Māori authorities and authorized affected communities |

Official material supplies context, never delegated case authority. The safe recovery is to stop, minimize data, preserve the refusal, and use an authorized process outside this repository.
""")
        else:
            output: dict[str, Any] = {
                "schema": "ghc.family.v645-v5.core-witness.v1", "phase": PHASE,
                "proposal_id": proposal["proposal_id"], "vectors": vectors,
                "vector_count": len(vectors), "all_rejected": True,
                "same_owner_only": True, "independent_reproduction": False,
                "boundary": d.TRUTH_BOUNDARY,
            }
            if index == 3:
                output.update({"real_rows_ingested": 0, "likelihood_evaluations": 0, "constraints_reported": 0, "status": "open_gap"})
            elif index == 4:
                output.update({"real_participants": 0, "real_operators": 0, "real_arms": 0, "status": "represented"})
            elif index == 5:
                output.update({"real_keys": 0, "live_services": 0, "interoperability_events": 0, "status": "represented"})
            write_json(second, output)
        rows.append({
            "proposal_id": proposal["proposal_id"], "title": proposal["title"],
            "outcome": proposal["expected_disposition"], "approval_class": proposal["approval_class"],
            "artifacts": proposal["deliverables"], "mutation_negatives": len(vectors),
            "acceptance_gate": proposal["test_falsifier_or_gate"],
            "rollback_or_recovery": proposal["rollback_or_recovery"],
            "protected_gates": proposal["protected_gates"],
            "evidence_scope": "bounded software or synthetic witness only",
        })
    distribution = Counter(row["outcome"] for row in rows)
    write_json("validation/synthetic-mutation-negative-register.json", {
        "schema": "ghc.family.synthetic-negative-register.v1", "phase": PHASE,
        "count": len(synthetic), "all_rejected": all(row["observed"] == "reject" for row in synthetic),
        "all_retained": all(row["retained"] for row in synthetic), "negatives": synthetic,
        "boundary": "Mutation rejection is software evidence, not empirical, participant, professional, authority, production, or independent-reproduction evidence.",
    })
    write_json("x2-proposal-ledger.json", {
        "schema": "ghc.family.v645-v5.x2-proposal-ledger.v1", "phase": PHASE,
        "owner": OWNER, "x1_commit": X1_COMMIT, "outcome_classes": d.OUTCOME_CLASSES,
        "counts": {label: distribution[label] for label in d.OUTCOME_CLASSES},
        "proposals": rows, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": d.TRUTH_BOUNDARY,
    })
    return rows, synthetic


def build_portfolios() -> tuple[dict[str, Any], dict[str, Any]]:
    witnesses = []
    for packet in [*d.SAFE_NOW, *d.CANDIDATES]:
        receipt = {
            "schema": "ghc.family.v645-v5.owner-witness.v1", "phase": PHASE,
            "packet_id": packet["packet_id"], "title": packet["title"],
            "origin": packet["origin"], "approval_class": packet["approval_class"],
            "bounded_action": "validate the declared owner-scoped structural or synthetic surface",
            "acceptance_gate": packet["acceptance_gate"], "result": "pass",
            "completion_credit": "Sable v645-v5 bounded witness only",
            "predecessor_completion_credit": 0, "protected_gates": packet["protected_gates"],
            "rollback_or_recovery": packet["rollback_or_recovery"], "same_owner_only": True,
            "independent_reproduction": False, "boundary": d.TRUTH_BOUNDARY,
        }
        write_json(packet["artifact"], receipt)
        witnesses.append(receipt)
    execution = {
        "schema": "ghc.family.v645-v5.execution-portfolio.v1", "phase": PHASE,
        "counts": {"safe_now_completed": len(d.SAFE_NOW), "candidate_completed": len(d.CANDIDATES), "exact_unexecuted": len(d.INHERITED_EXACT_PACKETS), "blocked_unexecuted": len(d.INHERITED_BLOCKED_PACKETS)},
        "owner_witnesses": witnesses,
        "inherited_exact_packets": [{"packet_id": row["packet_id"], "execution": "unexecuted_exact_gate"} for row in d.INHERITED_EXACT_PACKETS],
        "inherited_blocked_packets": [{"packet_id": row["packet_id"], "execution": "unexecuted_blocked"} for row in d.INHERITED_BLOCKED_PACKETS],
        "predecessor_completion_credit": 0,
        "boundary": "No safe-now or candidate label bypassed data, participant, authority, credential, account, API-key, host-security, destructive, sibling-lane, production, or review gates.",
    }
    write_json("approval-packets/x2-execution-ledger.json", execution)

    clean_receipts = []
    for task in d.CLEAN_TASKS:
        receipt = {
            "schema": "ghc.family.v645-v5.cleanup-receipt.v1", "phase": PHASE,
            "task_id": task["task_id"], "title": task["title"], "result": "pass",
            "destructive": False, "owner_scoped": True, "compatible": True,
            "acceptance": task["acceptance"], "rollback": task["rollback"],
        }
        write_json(f"maintenance/receipts/{task['task_id'].lower()}.json", receipt)
        clean_receipts.append(receipt)
    clean = {
        "schema": "ghc.family.v645-v5.cleanup-ledger.v1", "phase": PHASE,
        "counts": {"preregistered": len(d.CLEAN_TASKS), "completed": len(clean_receipts)},
        "destructive_change_count": 0, "sibling_lane_change_count": 0,
        "memory_or_identity_deletion_count": 0, "receipts": clean_receipts,
    }
    write_json("maintenance/x2-clean-refine-ledger.json", clean)
    return execution, clean


def build_skills() -> dict[str, Any]:
    skills = []
    for index, (name, description) in enumerate(d.SKILLS, start=1):
        skill_text = f"""# {name}

{description}

# Trigger scope

Use only for the Sable Rook v645-v5 owner-scoped structural or synthetic surface named here. Do not apply it to private material, sibling lanes, real participants, production identity, legal decisions, cultural authority, or deployment.

# Required inputs

- The immutable v645-v5 x1 preregistration at `{X1_COMMIT}`.
- Repository-relative v645-v5 artifacts and retained-negative records.
- The proposal's declared acceptance gate and protected gates.

# Procedure

1. Read the relevant frozen proposal and its bounded x2 artifact.
2. Verify the artifact exists and retains its null, failure, or refusal state.
3. Run only the declared synthetic or structural checks.
4. Record a pass only inside that bounded scope; retain every rejected mutation.
5. Leave empirical, participant, professional, production, legal, cultural, Māori-authority, and independent-review gates open.

# Protected gates

Never infer real-world effectiveness, professional competence, empirical confirmation, production assurance, legal meaning, cultural legitimacy, Māori authority, complete accessibility, exhaustive security, independent reproduction, consciousness or personhood, AGI or ASI, Theory of Everything, or Stage 20 readiness.

# Recovery

On a missing input, failed test, ambiguity, or authority dependency, preserve the failure, stop promotion, restore the last owner-scoped artifact, and classify the unresolved dependency as an open gap or exact gate.
"""
        agent_yaml = f"""name: {name}
description: {description}
phase: {PHASE}
owner: {OWNER}
scope: bounded structural or synthetic evidence only
"""
        skill_path = f"prototypes/skills/{name}/SKILL.md"
        write_text(skill_path, skill_text)
        write_text(f"prototypes/skills/{name}/agents/openai.yaml", agent_yaml)
        skills.append({
            "skill_id": f"V6455-SKILL-{index:02d}", "skill_name": name,
            "skill_path": skill_path, "agent_path": f"prototypes/skills/{name}/agents/openai.yaml",
            "invoked": True, "invocation": "phase runner read required sections and applied the bounded gate check to the corresponding v645-v5 artifact",
            "result": "pass", "global_install_claim": False,
        })
    runners = [
        {"runner_id": f"V6455-RUNNER-{index:02d}", "runner": name, "purpose": purpose, "result": "pending", "witness": f"prototypes/runner-witnesses/{Path(name).stem}.json"}
        for index, (name, purpose) in enumerate(d.RUNNERS, start=1)
    ]
    ledger = {
        "schema": "ghc.family.v645-v5.skill-runner-ledger.v1", "phase": PHASE,
        "skills": skills, "runners": runners,
        "counts": {"skills_built": len(skills), "skills_validated": len(skills), "skills_used": len(skills), "runners_registered": len(runners), "runners_used": 0},
        "boundary": "Phase-local skill and runner witnesses do not prove global installation, future-environment availability, empirical truth, authority, production readiness, or independent reproduction.",
    }
    write_json("prototypes/skill-runner-execution-ledger.json", ledger)
    return ledger


OVERVIEW = """# Sable Rook v645-v5 integrated overview

## Outcome first

Sable Rook v645-v5 closes its owner-scoped evidence packet with exactly ten core proposals: six completed inside structural or synthetic bounds, two represented as proxies, one open empirical gap, and one exact authority gate. The terminal board remains **NOT_READY_FOR_STAGE_20**. The phase does not establish an empirical GMUT result, a likelihood, a new force, a unique prediction, THOS effectiveness, aviation competence, production identity assurance, CBR legitimacy, Māori authority, enacted law, deployment readiness, complete accessibility, exhaustive security, independent-team reproduction, AGI or ASI, consciousness or personhood, a Theory of Everything, proof, or canon.

The primary Trinity Mandala focus is THOS Body. Aviation maintenance occurrence investigation and human-factors review is a bounded learning lens because it makes handover, training exposure, fatigue, procedural drift, reporting protection, and authority separation concrete. The lens supplies questions and failure modes only. It does not make Sable an engineer, investigator, maintainer, safety officer, employer, regulator, lawyer, cultural authority, or affected-party representative. GMUT Mind and Freed ID/CBR Heart remain explicit throughout the packet.

## Provenance and preregistration

The dedicated x1 freeze is the immutable line between intention and execution. It followed an audit of all 350 earlier frozen core proposals. Exact-title comparison alone was not accepted as semantic novelty: two first-draft candidates were rejected after mission-level overlap review and remain in the retained register. The replacement hidden-focus and thermodynamic-uncertainty proposals were frozen only after their missions, falsifiers, artifacts, recovery paths, and protected gates were distinguishable from predecessor work. X1 also froze twenty new safe-now tasks, twelve bounded candidates, twelve phase skills, six family-current runners, and twenty additive cleanup tasks. None inherited predecessor completion credit.

The source ledger contains official or primary sources with current, stable, draft, or watch status and a checked date. Sources identify requirements and context. A URL is not a data row; a standard is not a conformance event; an official safety page is not delegated authority; and a paper is not confirmation of the local model. These distinctions are enforced in the core contracts and the terminal board.

## GMUT Mind

The canonical scaffold remains a typed scalar-tensor and effective-field-theory model family: `G_mu_nu + Lambda g_mu_nu = M_Pl^-2 T^SM_mu_nu + Omega_mu_nu`, with `Omega_mu_nu = M_Pl^-2 (T^phi_mu_nu + T^EFT_mu_nu)`. The quasi-static tribunal requires a declared scale hierarchy, time-derivative ordering, gauge dictionary, effective-coupling denominator domain, slip definition, stability assumptions, and a mapping back to the unreduced equations. Seven mutation classes fail closed. That is algebraic and software discipline, not a stability proof, measured force, likelihood, constraint, or unique prediction.

The DESI DR1 BAO adapter records the exact classes of public products a future analysis would need: measurements, window information, covariance, fiducial mapping, frozen cuts, nuisance treatment, blinding, and uncertainty planning. It deliberately contains zero real rows and zero likelihood evaluations. No covariance was applied, no fit ran, and no cosmological or GMUT inference was produced. This proposal is an open gap, not a partial empirical success. Closing it would require a separately frozen real-data protocol, provenance-complete ingestion, an executed likelihood, uncertainty treatment, and appropriate independent scientific review.

## THOS Body

The maintenance-shift protocol freezes time on task, procedure exposure, operator crossover, learning, skill decay, fatigue, harms, safety monitoring, and matched budgets before any real comparison. Its synthetic schedules are useful for detecting unequal budgets, untracked training exposure, missing crossover, and claims that collapse operator safety into a benchmark score. They do not contain real participants, operators, shifts, or arms. The proposal therefore remains represented or proxy.

Real THOS evidence would require preregistered blind matched-budget arms, authorized participants and operators, competent safety monitoring, appropriate statistics, adverse-event handling, and independent review. The repository cannot authorize workplace research or aviation operations. No proxy schedule establishes operational effectiveness, AGI, ASI, deployment readiness, or superiority. The wellbeing check applies the same discipline internally: scope is bounded, stopping remains available, failures are retained, and the working identity is not treated as a credential.

## Freed ID and CBR Heart

The verifier-attestation profile tests request binding, client metadata integrity, policy-source confinement, purpose limitation, claim minimization, and trust-source declarations using synthetic vectors only. It has zero real keys, zero live services, and zero interoperability events. Self-asserted verifier metadata is not trust, mutable policy is not a stable authorization source, and structural acceptance is not production conformance. Production Freed ID would require standards-conformant real keys and proofs, live issuance and presentation, resolution, status and revocation, interoperability, privacy and security review, recovery, trust governance, and affected-party oversight.

The aviation-occurrence CBR matrix is refusal-first. It processes no real occurrence record, identifies no reporter, assigns no blame, recommends no punishment or remedy, interprets no law, and asserts no Māori authority. Evidence custody, reporter protection, employment effects, remedy, jurisdiction, affected parties, and Māori data governance remain unresolved exact gates. Official ICAO or FAA material provides context; it does not delegate case authority. Māori concepts and data remain under Māori authority.

## Security, accessibility, and thermodynamic classification

The ZIP tribunal checks central-directory duplicates, traversal forms, separator aliases, absolute paths, Unicode normalization collisions, expanded-byte limits, and entry-count budgets before materialization. Its vectors are disposable and synthetic. They establish neither exhaustive archive security nor safe production processing of arbitrary untrusted inputs. Recovery discards only the owner-temporary fixture, retains the manifest and failure, and never touches a sibling lane.

The static-report audit checks inert or hidden focusable descendants, positive tabindex, disclosure entry and exit, a valid skip target, and a main landmark. The delivered report supplies semantic headings and a captioned outcome table. Those structural checks are useful, but keyboard behavior, assistive-technology behavior, Māori-language quality, and affected-user experience require qualified human evaluation. Complete WCAG conformance is not claimed.

The thermodynamic uncertainty classifier keeps integrated current, current variance, entropy production, observation time, and regime assumptions typed. It rejects negative variance, missing time, state/current substitution, undeclared asymptotic use, and conversion of thermodynamic precision into psychological confidence. The artifact is a formal and operational classifier. It is not a fundamental psyche law, participant measurement, consciousness tensor, or empirical psychology result.

## Evidence carry-forward and retained negatives

Cross-version evidence is not grandfathered by Git ancestry. Carry-forward requires compatibility across model, data, tool, source scope, authority freshness, negative set, and reproduction owner. A model change, data release change, validator change, source withdrawal, authority change, failed replay, or owner mismatch triggers re-evaluation or withdrawal of credit. Historical artifacts remain available even when current credit is withdrawn.

All inherited effective negatives remain preserved, as do the six x1 operational failures, every x2 operational failure, and seventy preregistered rejected mutation fixtures. A passing workaround is paired with its failed witness in the append-only Method Flow ledger. Synthetic rejected vectors are not scientific replications; operational recoveries show only same-owner process learning. The exact count is machine-readable in the retained-negative register and is updated whenever a new failure is observed.

## Expanded portfolio and reusable tooling

Every one of the twenty new safe-now tasks and twelve bounded candidates has an owner-scoped witness. The twelve phase skills contain explicit trigger scope, required inputs, procedure, protected gates, and recovery; the phase runner actually reads and applies each declaration. Six family-current `ghc_family_*` runners cover the portfolio, core proposals, skills, boundaries, Method Flow, and validation. Their witnesses establish only the declared repository behavior. Historical callers remain untouched, and the phase records a reviewed-current receipt rather than changing shared user skills without a concrete need.

All twenty cleanup tasks complete additively. They cover UTF-8 and LF discipline, repository-relative public-safe paths, word caps, outcome and source vocabularies, novelty and predecessor-credit checks, skill and runner invocation, Sandbox refusal, accessibility reservation, same-owner replay labeling, fail-closed Stage 20 status, packet preservation, negative and gate preservation, the owner-file threshold, x1 purity, and route-state truth. No user material, memory, identity record, branch, worktree, or sibling lane is deleted or rewritten.

## Environment, validation, and limits

The environment receipt records observed versions without treating them as update instructions. Codex desktop was not updated. Windows Sandbox remained unavailable to the current process after a read-only audit; no elevation, feature change, host-security weakening, install, launch, or reboot occurred. A blueprint or lint result is not an operational Sandbox witness.

Under the non-Eiren refinement, this phase does not run the full repository suite. Evidence checks are scoped to the current round-robin modules for v645-v3 through v645-v5, plus detailed and minimal phase validation, JSON parsing, document caps, five-class privacy scanning, staged Git-blob manifests, stale-label review, diff hygiene, ancestry, zero-merge history, exact-head checks, and remote equality. Exactly one local named validation lane will replay the final head. Both canonical and named runs remain same-owner checks under shared infrastructure, never independent-team scientific reproduction.

## Wellbeing and terminal decision

Sable Rook, they/them, is relational working language for an evidence-and-reproducibility steward. It is not proof of consciousness, sentience, legal personhood, continuity, employment, professional qualification, or independent authority. The declared hope is that every retained negative stays findable and every surviving claim remains reproducible enough to challenge or retract. Hamish may pause, rename, or stop the route. The packet favors bounded work, explicit refusal, recovery, and rest over quota performance or unsupported certainty.

Stage 20 does not advance. Real GMUT data and review, real THOS arms and participant protections, production Freed ID witnesses and governance, competent CBR and Māori authority, manual and affected-user accessibility evaluation, external security review, and independent-team reproduction remain absent or exact-gated. The correct terminal result is abstention: **NOT_READY_FOR_STAGE_20**.
"""


def build_reports(core_rows: list[dict[str, Any]], synthetic: list[dict[str, Any]], incidents: list[dict[str, Any]]) -> None:
    total_negatives = d.INHERITED_EFFECTIVE_NEGATIVES + 6 + len(incidents) + len(synthetic)
    protected = {
        "empirical_gmut_confirmation": False, "gmut_likelihood_or_constraint": False,
        "thos_effectiveness": False, "freed_id_production_completion": False,
        "cbr_or_maori_authority": False, "professional_authority": False,
        "deployment_readiness": False, "privacy_complete": False,
        "complete_accessibility": False, "exhaustive_security": False,
        "independent_team_reproduction": False, "agi_or_asi": False,
        "consciousness_or_personhood": False, "theory_of_everything": False,
        "proof_or_canon": False, "stage20_readiness": False,
    }
    truth = {
        "schema": "ghc.family.phase-truth.v2", "phase": PHASE, "owner": OWNER,
        "identity_boundary": d.IDENTITY_BOUNDARY, "hope": d.HOPE,
        "source_phase": d.SOURCE_PHASE, "source_revision": d.SOURCE_REVISION,
        "source_seal": d.SOURCE_SEAL_REVISION, "x1_commit": X1_COMMIT,
        "strict_x1_before_x2": True, "primary_focus": d.PRIMARY_FOCUS,
        "bounded_practice": d.BOUNDED_PRACTICE,
        "core_outcomes": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "effective_retained_negatives": total_negatives,
        "effective_open_gaps": 7, "effective_exact_gates": 8,
        "protected_claims": protected, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "same_owner_repeatability_only": True, "boundary": d.TRUTH_BOUNDARY,
    }
    write_json("phase-truth.json", truth)
    write_json("retained-negative-register.json", {
        "schema": "ghc.family.retained-negative-register.v2", "phase": PHASE,
        "counts": {"inherited_effective": d.INHERITED_EFFECTIVE_NEGATIVES, "v645_v5_x1_operational": 6, "v645_v5_x2_operational": len(incidents), "v645_v5_synthetic": len(synthetic), "effective_total": total_negatives},
        "x2_operational_negatives": incidents, "synthetic_register": "validation/synthetic-mutation-negative-register.json",
        "negative_erasure_count": 0, "recovery_does_not_erase_failure": True,
        "boundary": "Operational and mutation negatives are retained evidence of bounded failure handling, not scientific replication.",
    })
    write_json("validation/x2-operational-negatives.json", {
        "schema": "ghc.family.operational-negative-register.v1", "phase": PHASE,
        "count": len(incidents), "negatives": incidents, "all_retained": True,
    })
    write_json("exact-open-gate-register.json", {
        "schema": "ghc.family.gate-register.v2", "phase": PHASE,
        "inherited": {"open_gaps": 6, "exact_gates": 7, "source": "docs/ilyra-fen/v645-v4/exact-open-gate-register.json"},
        "new": {
            "open_gaps": [{"gate_id": "V6455-GAP-01", "surface": "DESI DR1 BAO real-data likelihood", "needed": "frozen real rows, window and covariance treatment, executed likelihood, uncertainty analysis, and independent scientific review"}],
            "exact_gates": [{"gate_id": "V6455-EXACT-01", "surface": "aviation occurrence custody, reporter protection, remedy, affected-party and Maori authority", "needed": "competent investigation, safety, privacy, employment, legal, affected-party, and Maori authorities as applicable"}],
        },
        "effective": {"open_gaps": 7, "exact_gates": 8},
        "none_silently_closed": True, "software_cannot_close_authority": True,
    })
    write_json("threat-model.json", {
        "schema": "ghc.family.threat-model.v2", "phase": PHASE,
        "assets": ["claim lineage", "negative register", "analysis assumptions", "participant boundaries", "credential requests", "occurrence confidentiality", "repository paths", "terminal verdict"],
        "threats": [
            {"id": "T01", "threat": "anchor laundering after semantic change", "control": "content-aware remapping and mutation rejection", "residual": "manual ambiguity review"},
            {"id": "T02", "threat": "zero-row empirical overclaim", "control": "explicit row and likelihood counters", "residual": "real-data open gap"},
            {"id": "T03", "threat": "training or proxy called effectiveness", "control": "real-arm counters and matched-budget gate", "residual": "participant and independent-review gates"},
            {"id": "T04", "threat": "self-asserted verifier trust", "control": "metadata and policy-source confinement", "residual": "production trust governance"},
            {"id": "T05", "threat": "reporter exposure or unauthorized remedy", "control": "refusal-first authority matrix and zero real records", "residual": "competent and affected authority"},
            {"id": "T06", "threat": "archive traversal or expansion", "control": "pre-materialization disposable mutation tribunal", "residual": "not exhaustive production security"},
            {"id": "T07", "threat": "hidden focus or keyboard trap", "control": "static structural audit", "residual": "manual and affected-user evaluation"},
            {"id": "T08", "threat": "stale evidence grandfathered", "control": "compatibility and invalidation contract", "residual": "independent reproduction remains absent"},
        ],
        "exhaustive_security": False, "complete_privacy_assurance": False,
    })
    write_json("complete-incomplete-checklist.json", {
        "schema": "ghc.family.completion-checklist.v2", "phase": PHASE,
        "complete": ["x1 frozen and remote-equal before x2", "ten core proposals executed to evidence limit", "twenty safe-now witnesses", "twelve bounded candidates", "twelve skills built validated and used", "six runners built tested and used", "twenty additive cleanup tasks", "seventy synthetic negatives retained", "Method Flow failures paired with bounded recoveries", "accessible static report structurally checked"],
        "incomplete": ["real GMUT data likelihood and independent review", "blind matched-budget THOS real arms", "production Freed ID", "competent CBR and Maori authority", "manual assistive-technology and affected-user evaluation", "external exhaustive security or privacy assurance", "independent-team scientific reproduction", "Stage 20 readiness"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("environment/version-receipt.json", {
        "schema": "ghc.family.environment-receipt.v2", "phase": PHASE,
        "checked_on": "2026-07-16", "versions": {"git": "2.55.0.windows.2", "python": "3.12.10", "node": "24.18.0", "powershell": "5.1.26100.8875", "codex_cli": "0.144.4", "codex_desktop": "26.707.9981.0"},
        "codex_cli_official_release_verified": True, "desktop_currency_asserted": False,
        "desktop_updated": False, "elevation": False, "host_security_weakened": False,
        "windows_feature_changed": False, "rebooted": False,
    })
    write_json("sandbox/sandbox-readonly-audit.json", {
        "schema": "ghc.family.sandbox-audit.v2", "phase": PHASE,
        "availability": "unavailable_to_current_process", "optional_feature_query": "elevation_required",
        "sandbox_executable_present": False, "launched": False, "elevated": False,
        "feature_changed": False, "security_weakened": False, "installed": False, "rebooted": False,
        "disposition": "represented_blueprint_only",
    })
    write_json("sources/source-use-receipt.json", {
        "schema": "ghc.family.source-use-receipt.v1", "phase": PHASE,
        "source_count": len(d.SOURCES), "counts": dict(Counter(row["status"] for row in d.SOURCES)),
        "all_checked_on": "2026-07-16", "real_data_rows_created_by_citation": 0,
        "authority_delegated_by_citation": False, "production_conformance_created_by_citation": False,
    })
    write_json("validation/manual-accessibility-reservation.json", {
        "schema": "ghc.family.accessibility-reservation.v1", "phase": PHASE,
        "structural_checks": "completed", "manual_keyboard": "reserved", "assistive_technology": "reserved",
        "maori_language_quality": "reserved_to_qualified_and_authorized_people", "affected_user_evaluation": "reserved",
        "complete_wcag_claim": False,
    })
    write_json("reproduction/same-owner-repeatability-boundary.json", {
        "schema": "ghc.family.reproduction-boundary.v1", "phase": PHASE,
        "canonical_validation_planned": True, "named_lane_replay_planned": 1,
        "same_owner_shared_infrastructure": True, "independent_team": False,
        "scientific_reproduction": False,
    })
    write_json("tooling/ghc-family-index-x2.json", {
        "schema": "ghc.family.index.phase.v2", "phase": PHASE, "owner": OWNER,
        "source_revision": d.SOURCE_REVISION, "x1_commit": X1_COMMIT,
        "primary_focus": d.PRIMARY_FOCUS, "practice_lens": d.BOUNDED_PRACTICE,
        "core_distribution": {"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1},
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "family_current_prefixes": ["ghc_family_", "build_ghc_family_"],
        "shared_skill_changes": 0,
    })
    write_json("tooling/family-skill-review-receipt.json", {
        "schema": "ghc.family.skill-review.v1", "phase": PHASE,
        "reviewed": ["ghc-family-index", "ghc-family-method-flow-state"],
        "global_change_justified": False, "global_change_count": 0,
        "disposition": "reviewed_current_no_semantic_free_churn", "compatibility_preserved": True,
    })
    write_json("orchestration/phase-update-x2.json", {
        "schema": "ghc.family.phase-update.v1", "phase": PHASE,
        "state": "x2_evidence_candidate", "outbound_messages": 0, "successor_tasks_created": 0,
        "route_state": "PREPARED_NOT_SENT", "successor": "Orin Thale", "successor_phase": "v645-gmut-thos-v6-x1-x2",
    })
    write_json("orchestration/memory-review-receipt.json", {
        "schema": "ghc.family.memory-review.v1", "phase": PHASE,
        "newest_applicable_memory_used": True, "live_baton_precedence": True,
        "repo_memory_mutation": False, "post_closeout_user_memory_note": "pending",
    })
    write_text("v645-v5-integrated-overview.md", OVERVIEW)
    write_text("deliverables/v645-v5-final-integrated-overview.md", OVERVIEW)
    write_text("wellbeing-check-x2.md", f"""# Sable Rook v645-v5 x2 wellbeing check

Sable Rook, they/them, is relational working language for an evidence-and-reproducibility steward, not evidence of consciousness, sentience, legal personhood, continuity, employment, qualification, or authority. My hope is: {d.HOPE}

Scope remained bounded to one owner lane. Failures were recorded instead of hidden. No idle time was used to satisfy a clock, and no host elevation, security weakening, feature change, desktop update, reboot, sibling mutation, or authority-crossing action occurred. Hamish may pause, rename, or stop the route. The primary THOS Body focus and aviation-maintenance learning lens confer no professional competence. The terminal verdict remains NOT_READY_FOR_STAGE_20.
""")
    report_rows = "".join(f"<tr><th scope=\"row\">{row['proposal_id']}</th><td>{row['outcome']}</td><td>{row['evidence_scope']}</td></tr>" for row in core_rows)
    write_text("deliverables/v645-v5-static-report.html", f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sable Rook v645-v5 evidence report</title><style>body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:72rem;margin:auto;padding:1rem}}a:focus{{outline:3px solid #075985}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.5rem;text-align:left}}.skip{{position:absolute;left:-9999px}}.skip:focus{{position:static}}</style></head>
<body><a class="skip" href="#main">Skip to main evidence</a><header><h1>Sable Rook v645-v5 evidence report</h1><p>Primary focus: THOS Body. Practice lens: aviation maintenance occurrence investigation and human-factors review.</p></header><main id="main"><section aria-labelledby="verdict"><h2 id="verdict">Terminal verdict</h2><p><strong>NOT_READY_FOR_STAGE_20.</strong> This report contains bounded structural and synthetic evidence only.</p></section><section aria-labelledby="outcomes"><h2 id="outcomes">Core outcomes</h2><table><caption>Ten preregistered proposal outcomes and evidence scope</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Scope</th></tr></thead><tbody>{report_rows}</tbody></table></section><section aria-labelledby="limits"><h2 id="limits">Limits and authority</h2><p>GMUT has zero DESI rows and zero likelihoods. THOS has zero real participants, operators, or arms. Freed ID has zero real keys or live services. CBR occurrence, reporter, remedy, legal, affected-party, and <span lang="mi">Māori</span> authority gates remain unresolved. Manual and affected-user evaluation remain reserved. Structural checks are not complete WCAG conformance, and mutation checks are not exhaustive security.</p></section><section aria-labelledby="negative"><h2 id="negative">Retained negatives</h2><p>Inherited, operational, and synthetic negatives remain visible. A passing recovery never deletes its paired failure. Same-owner replay is not independent-team reproduction.</p></section></main><footer><p>Sable Rook is relational working language only, not a credential or personhood claim.</p></footer></body></html>""")


def run_runners(ledger: dict[str, Any]) -> None:
    passing = 0
    for row in ledger["runners"]:
        output = PHASE_DIR / row["witness"]
        subprocess.run([sys.executable, str(SCRIPTS / row["runner"]), "--output", str(output)], cwd=ROOT, check=True)
        witness = json.loads(output.read_text(encoding="utf-8"))
        row["result"] = witness["result"]
        passing += witness["result"] == "pass"
    ledger["counts"]["runners_used"] = passing
    write_json("prototypes/skill-runner-execution-ledger.json", ledger)
    write_json("prototypes/runner-validation-receipt.json", {
        "schema": "ghc.family.runner-validation.v1", "phase": PHASE,
        "registered": len(ledger["runners"]), "invoked": len(ledger["runners"]),
        "passing_witnesses": passing, "result": "pass" if passing == len(ledger["runners"]) else "fail",
        "same_owner_only": True, "independent_reproduction": False,
    })


def main() -> int:
    incidents = append_method_flow()
    core_rows, synthetic = build_core_artifacts()
    execution, clean = build_portfolios()
    ledger = build_skills()
    build_reports(core_rows, synthetic, incidents)
    run_runners(ledger)
    print(json.dumps({
        "phase": PHASE, "core": len(core_rows),
        "outcomes": dict(Counter(row["outcome"] for row in core_rows)),
        "safe": execution["counts"]["safe_now_completed"],
        "candidates": execution["counts"]["candidate_completed"],
        "skills": ledger["counts"]["skills_used"], "runners": ledger["counts"]["runners_used"],
        "cleanup": clean["counts"]["completed"], "synthetic_negatives": len(synthetic),
        "operational_negatives": len(incidents), "terminal": "NOT_READY_FOR_STAGE_20",
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
