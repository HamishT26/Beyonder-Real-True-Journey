#!/usr/bin/env python3
"""Build the frozen planning-only corpus for Auren Lark v707-v4.

The builder reads Mira's committed proposal ledger only to create explicit
zero-credit provenance references.  It does not execute or replay Mira's
domain solver, tests, skills, runners, hooks, or canonical validator.
"""

from __future__ import annotations

from hashlib import sha1, sha256
import json
from pathlib import Path
import subprocess
from typing import Any


SOURCE = "10a3c34c01f06a26ba771d9738fe90e5714b797c"
BRANCH = "codex/GHC-Family/auren-lark-main-4"
PHASE = "v707-v4"
OWNER = "Auren Lark"
PREFIX = "docs/auren-lark/v707-v4"
SOURCE_PROPOSALS = "docs/mira-fenwick/v707-v3/planning/proposals.json"
BOUNDARY = (
    "Finite synthetic same-owner software and documentation evidence only. "
    "No independent reproduction, empirical GMUT confirmation, production THOS or Freed ID, "
    "participant result, professional judgment, deployment authority, legal or cultural conclusion, "
    "affected-party or Maori authority, complete privacy, accessibility or security assurance, AGI or ASI, "
    "consciousness or personhood evidence, Theory-of-Everything proof, canon, or Stage 20 readiness."
)


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def digest(value: Any) -> str:
    return sha256(canonical_bytes(value)).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=repo, text=True).strip()


def git_blob(repo: Path, commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=repo)


def git_oid(data: bytes) -> str:
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def fixture(fid: str, terms: list[str], rules: list[tuple[str, str]], description: str) -> dict[str, Any]:
    row = {
        "fixture_id": fid,
        "terms": terms,
        "rules": [{"source": a, "target": b} for a, b in rules],
        "description": description,
        "synthetic": True,
        "external_observation": False,
    }
    row["fixture_sha256"] = digest(row)
    return row


FIXTURES = [
    fixture("AR01-CHAIN", ["a", "b", "c"], [("a", "b"), ("b", "c")], "A terminating chain with one normal form."),
    fixture("AR02-DIAMOND", ["a", "b", "c", "d"], [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d")], "A finite joinable diamond."),
    fixture("AR03-SPLIT", ["a", "b", "c"], [("a", "b"), ("a", "c")], "A terminating nonjoinable split."),
    fixture("AR04-DEEP-DIAMOND", ["a", "b", "c", "d", "e"], [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d"), ("d", "e")], "A deeper confluent terminating reduction."),
    fixture("AR05-CYCLE", ["a", "b"], [("a", "b"), ("b", "a")], "A two-term cycle with no normal form."),
    fixture("AR06-CYCLE-EXIT", ["a", "b", "c"], [("a", "b"), ("b", "a"), ("b", "c")], "A cycle with a reachable normal form."),
    fixture("AR07-TWO-COMPONENTS", ["a", "b", "c", "d"], [("a", "b"), ("c", "d")], "Two disconnected terminating components."),
    fixture("AR08-SELF-LOOP", ["a", "b"], [("a", "a"), ("a", "b")], "A self-loop plus an exit."),
    fixture("AR09-MULTI-JOIN", ["a", "b", "c", "d", "e", "f"], [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d"), ("b", "e"), ("c", "e"), ("d", "f"), ("e", "f")], "Two intermediate joins reaching one normal form."),
    fixture("AR10-DEEP-SPLIT", ["a", "b", "c", "d", "e"], [("a", "b"), ("a", "c"), ("b", "d"), ("c", "e")], "A nonconfluent deep split."),
    fixture("AR11-CYCLIC-JOIN", ["a", "b", "c", "d"], [("a", "b"), ("a", "c"), ("b", "a"), ("b", "d"), ("c", "d")], "A cyclic relation whose visible peak can join."),
    fixture("AR12-THREE-FAN", ["a", "b", "c", "d", "e"], [("a", "b"), ("a", "c"), ("a", "d"), ("b", "e"), ("c", "e"), ("d", "e")], "A three-way fan with a common reduct."),
    fixture("AR13-GRID", ["a", "b", "c", "d", "e", "f"], [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d"), ("d", "e"), ("c", "f"), ("f", "e")], "A finite grid-shaped confluent reduction."),
    fixture("AR14-ISOLATED", ["a", "b", "c", "d", "e"], [("a", "b"), ("c", "d")], "Two one-step reductions and an isolated normal term."),
    fixture("AR15-REDUNDANT", ["a", "b", "c", "d", "e"], [("a", "b"), ("b", "c"), ("a", "c"), ("c", "d"), ("b", "d"), ("d", "e")], "A terminating chain with redundant shortcut rules."),
]


OPERATIONS = [
    (1, "record-shape", "x1", "completed", "Validate the finite abstract-reduction-system record shape."),
    (2, "relation-normalization", "x1", "completed", "Normalize and deduplicate the declared reduction relation."),
    (3, "reflexive-transitive-closure", "x1", "completed", "Compute exact finite reflexive-transitive reachability."),
    (4, "strong-components", "x1", "completed", "Compute strongly connected reduction components."),
    (5, "termination-status", "x1", "completed", "Decide finite acyclicity after excluding no edges."),
    (6, "normal-forms", "x1", "completed", "Enumerate terms with no outgoing reduction."),
    (7, "descendant-sets", "x1", "completed", "Compute exact descendant sets for every term."),
    (8, "local-peaks", "x1", "completed", "Enumerate pairs of one-step reducts from a common source."),
    (9, "joinability", "x1", "completed", "Decide whether each ordered term pair has a common reduct."),
    (10, "local-confluence", "x1", "completed", "Check joinability of every finite local peak."),
    (11, "global-confluence", "x2", "completed", "Check joinability of every pair reachable from a common ancestor."),
    (12, "unique-normal-form", "x2", "completed", "Check whether each term reaches at most one normal form."),
    (13, "newman-implication", "x2", "completed", "Record the bounded implication from termination plus local confluence to confluence."),
    (14, "rule-deletion", "x2", "completed", "Compute a deterministic one-rule-deletion comparison."),
    (15, "relabel-covariance", "x2", "completed", "Check exact invariants under deterministic term relabeling."),
    (16, "strategy-trace", "x2", "completed", "Compute a deterministic lexicographic reduction trace."),
    (17, "accessible-summary", "x2", "completed", "Render a compact text account of the finite result."),
    (18, "three-coordinate-model", "x2", "represented", "Represent term count, rule count, and local-peak count."),
    (19, "empirical-calibration-gap", "x2", "open_gap", "Retain the absence of real empirical calibration evidence."),
    (20, "deployment-authority-hold", "x2", "exact_gate", "Hold operational use behind competent authority and affected-party gates."),
]


FAILURES = [
    ("AL7074-ACT-N01", "Combined skill read exceeded the bounded projection and was truncated.", "Read each selected skill completely in bounded individual groups."),
    ("AL7074-ACT-N02", "A PowerShell inventory projection used an empty pipeline element and failed parsing.", "Materialize the foreach result before piping to JSON."),
    ("AL7074-ACT-N03", "A JavaScript wrapper accidentally contained PowerShell syntax and failed before tool invocation.", "Keep orchestration JavaScript and shell source in separate literal domains."),
    ("AL7074-ACT-N04", "A manifest-replay wrapper assumed btoa existed in the isolated JavaScript runtime.", "Pass bounded Python source through a PowerShell literal here-string instead."),
    ("AL7074-ACT-N05", "A whole-file workflow projection exceeded the output cap and was truncated.", "Read the immutable workflow in explicit contiguous line chunks through EOF."),
    ("AL7074-ACT-N06", "The first source-proposal projection assumed a records property and produced a null index failure.", "Inspect top-level keys before selecting the proposal collection."),
    ("AL7074-ACT-N07", "A second source-proposal projection still indexed the absent records property after decoding.", "Bind the verified proposals property and then inspect its first element."),
]


def method_flow() -> dict[str, Any]:
    methods = []
    witnesses = []
    events = []
    for index, (negative, failure, recovery) in enumerate(FAILURES, 1):
        method_id = f"AL7074-MF-{index:03d}"
        fail_id = f"AL7074-WF-{index:03d}"
        pass_id = f"AL7074-WP-{index:03d}"
        methods.append({
            "method_id": method_id,
            "title": f"Bounded activation recovery {index}",
            "failure_signature": failure,
            "trigger_preconditions": ["read-only activation or source-verification projection", "no repository mutation completed"],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now",
            "candidate_workaround": recovery,
            "validation_witness_ids": [pass_id],
            "recurrence_guard": recovery,
            "rollback": "Discard only the failed transient projection; preserve the failure record and any immutable source state.",
            "recommendation_state": "validated",
            "supersedes": [],
            "protected_gates": ["source_fixity", "privacy", "no_replay", "authority_boundary"],
            "retained_negative_ids": [negative],
            "scope_boundary": BOUNDARY,
            "execution_authority": "owner_self_scoped_delta",
            "repository_scan": False,
            "module_scan": False,
            "cross_lane_scan": False,
            "unchanged_history_scan": False,
            "sibling_lane_mutation": False,
            "source_commit": SOURCE,
            "final_commit": SOURCE,
            "changed_file_allowlist": [],
            "module_allowlist": [],
            "exact_pushed_head_required": False,
        })
        witnesses.extend([
            {"witness_id": fail_id, "method_id": method_id, "procedure": "Original bounded wrapper or projection.", "scope": "Activation-stage read-only verification.", "expected": "A usable bounded projection.", "observed": failure, "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative], "boundary": BOUNDARY},
            {"witness_id": pass_id, "method_id": method_id, "procedure": recovery, "scope": "Activation-stage read-only recovery.", "expected": "Exact source or instruction content recovered without replay or mutation.", "observed": "The focused recovery passed and the original failure remained retained.", "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative], "boundary": BOUNDARY},
        ])
        events.append({"event_id": f"AL7074-EV-{index:03d}", "method_id": method_id, "from": "candidate", "to": "validated", "witness_id": pass_id})
    return {
        "schema": "ghc.family.method-flow-state.v1",
        "phase": PHASE,
        "owner": OWNER,
        "identity_boundary": BOUNDARY,
        "execution_authority": "owner_self_scoped_delta",
        "methods": methods,
        "witnesses": witnesses,
        "state_events": events,
        "recommendations": [{"method_id": m["method_id"], "state": "validated"} for m in methods],
        "counts": {"methods": len(methods), "witnesses": len(witnesses), "pass": len(FAILURES), "fail": len(FAILURES), "negatives": len(FAILURES), "open_gaps": 0, "exact_gates": 0},
        "boundary": BOUNDARY,
    }


def build() -> None:
    repo = Path(git(Path.cwd(), "rev-parse", "--show-toplevel"))
    root = repo / PREFIX
    planning = root / "planning"
    source_proposals = json.loads(git_blob(repo, SOURCE, SOURCE_PROPOSALS).decode("utf-8"))["proposals"]
    if len(source_proposals) != 300:
        raise RuntimeError("Expected exactly 300 inherited source proposals")

    identity = {
        "owner": OWNER,
        "phase": PHASE,
        "pronouns": "they/them",
        "relational_role": "finite-reduction confluence cartographer",
        "hope": "Make every reduction path, counterexample, correction, and authority limit inspectable.",
        "working_language_only": True,
        "not_evidence_of": ["consciousness", "sentience", "legal_personhood", "identity_continuity", "employment", "qualification", "independent_agency", "scientific_authority", "operational_authority", "professional_authority", "legal_authority", "cultural_authority", "affected_party_authority", "Maori_authority"],
        "hamish_may": ["rename", "pause", "narrow", "redirect", "stop"],
        "boundary": BOUNDARY,
    }
    source_proof = {
        "source_owner": "Mira Fenwick",
        "source_phase": "v707-v3",
        "source_branch": "codex/GHC-Family/mira-fenwick-main-4",
        "source_commit": SOURCE,
        "source_baton_sha256": "c955052889890a08f0ee855b81d8165aa55fc5794365cf55b6e2abfe020e989d",
        "source_canonical_receipt_sha256": "c7aa9a621b6e74b30c45a01473fd37edefc2539551f2f24f62cb21fd468d0b55",
        "source_canonical_payload_sha256": "b1b110582ab7848b0d544d870ceb461c16d4bd8577f596523bb421e64360b4d6",
        "source_manifest_replay": {"planning": 20, "x1": 26, "x2": 36, "final": 100, "mismatches": 0},
        "source_canonical_replayed": False,
        "source_solver_or_tests_replayed": False,
        "source_fold_count": 1,
        "boundary": BOUNDARY,
    }
    workflow = {
        "profile": "v19",
        "owner": OWNER,
        "phase": PHASE,
        "predecessor": {"owner": "Mira Fenwick", "phase": "v707-v3"},
        "successor": {"owner": "Sable Rook", "phase": "v707-v5", "state": "terminally_gated_not_contacted"},
        "formal_endpoint": {"owner": "Eiren Kestrel", "phase": "v725-v8"},
        "authority_hashes": {
            "v19_pointer": "da52e205f65c9f8b526bc6b309bb79d40d1dea9d75947c59eead4e6b27f3cdf8",
            "v19_authority": "98a3691d18ff77a7aa520cadc64f31599a1fc91d69e43ca207fd995eb7bc2224",
            "v19_roster": "7bc8e76ecb0540edb550e30c9a79ef9e584cd8f563a71371a93a8d5847b3e6df",
            "v18_workflow_base": "da328c767e64a213a85953fe6c94b9836624faae2576f4faa4cc71fe3a082c05",
            "v18_authorization_base": "0c1dc05066e8bb337f97bd2583e2983626f349f75e67191782f16dc15e65d611",
        },
        "model_admission": {"model": "gpt-5.6-sol", "preflight_passed": True, "mutation_performed": False, "model_request_sent": False},
        "one_canonical_success_no_replay": True,
        "one_terminal_send_after_gate": True,
        "boundary": BOUNDARY,
    }
    operations = [{"operation": n, "mechanism": mechanism, "stage": stage, "disposition": disposition, "title": title, "definition_sha256": digest({"operation": n, "mechanism": mechanism, "stage": stage, "disposition": disposition, "title": title})} for n, mechanism, stage, disposition, title in OPERATIONS]
    proposals = []
    for op in operations:
        for fx in FIXTURES:
            number = len(proposals) + 1
            proposals.append({
                "id": f"AL7074-P{number:03d}",
                "operation": op["operation"],
                "mechanism": op["mechanism"],
                "stage": op["stage"],
                "expected_disposition": op["disposition"],
                "title": f"{op['title']} {fx['fixture_id']}",
                "fixture_id": fx["fixture_id"],
                "fixture_sha256": fx["fixture_sha256"],
                "definition_sha256": op["definition_sha256"],
                "scope": "Declared finite synthetic abstract-reduction fixture and mechanism only; established finite mathematics and a new Auren implementation case.",
                "falsifier": "Schema acceptance of an invalid subject, disagreement with an independent finite oracle, broken relabel or transformation invariant, changed digest, or promotion beyond the declared disposition.",
            })
    if len(proposals) != 300:
        raise RuntimeError("Planning contract count drift")
    inherited = [{
        "source_id": row["id"],
        "source_owner": "Mira Fenwick",
        "source_phase": "v707-v3",
        "source_commit": SOURCE,
        "source_fixture_id": row["fixture_id"],
        "source_mechanism": row["mechanism"],
        "source_definition_sha256": row["definition_sha256"],
        "source_fixture_sha256": row["fixture_sha256"],
        "novelty_credit": 0,
        "completion_credit": 0,
        "execution_replayed": False,
    } for row in source_proposals]
    exact_packets = [{"packet_id": f"AL7074-EX-{i:03d}", "class": "exact_approval", "state": "held_unexecuted", "requires": "An exact named prerequisite and separately attributable evidence at execution time.", "credit": 0} for i in range(1, 51)]
    blocked_packets = [{"packet_id": f"AL7074-BL-{i:03d}", "class": "blocked", "state": "held_unexecuted", "requires": "External empirical, participant, professional, production, legal, cultural, affected-party, Maori-authority, complete-assurance, or protected evidence.", "credit": 0} for i in range(1, 31)]
    laws = [{"hypothesis_id": f"AL7074-LH-{i:02d}", "state": "hypothesis_only", "claim": text, "validated_law": False, "completion_credit": 0, "boundary": BOUNDARY} for i, text in enumerate([
        "Finite reduction entropy should not be identified with physical entropy without a declared bridge and data.",
        "Confluence may model consistency only inside a declared reduction semantics.",
        "A unique normal form is not a unique real-world truth.",
        "Termination is relative to the encoded relation and finite universe.",
        "Joinability can represent reversible correction without erasing divergent history.",
        "Local consistency cannot imply global authority without explicit prerequisites.",
        "Acyclic provenance may support auditability but not legitimacy by itself.",
        "Reduction strategies expose ordering assumptions rather than neutral inevitability.",
        "Countermodels should remain first-class alongside passing certificates.",
        "A held gate is evidence of a boundary, not evidence that the gated claim is false.",
        "Exact finite closure cannot establish open-world completeness.",
        "Relabel covariance can test representation dependence without proving empirical invariance.",
        "Rule deletion sensitivity can reveal brittle conclusions without identifying causal effects.",
        "Accessible summaries should preserve uncertainty and authority reservations.",
        "No formal reduction system establishes consciousness, personhood, or moral status on its own.",
    ], 1)]
    probes = [{"probe_id": f"AL7074-OP-{i:02d}", "state": "open", "question": text, "completion_credit": 0, "boundary": BOUNDARY} for i, text in enumerate([
        "How should finite confluence certificates compose across changing rule versions?",
        "What minimal provenance is needed to audit a corrected reduction relation?",
        "How can nontermination witnesses remain accessible without implying operational risk?",
        "When does bounded joinability remain stable under conservative extension?",
        "How should authority gates propagate through derived summaries?",
        "Can two independent encodings expose hidden representation dependence?",
        "What counterexample budget best guards finite normal-form claims?",
        "How should incomplete rule discovery be represented without false closure?",
        "What accessibility features best expose divergent paths and held gates?",
        "How can exact finite evidence coexist with unresolved empirical calibration?",
        "Which correction lineages preserve non-erasure under schema migration?",
        "How should rule-deletion sensitivity be distinguished from causal inference?",
        "What competent review is required before formal consistency affects people?",
        "How can cultural and Maori authority remain explicit rather than encoded by proxy?",
        "What external evidence would be necessary to move beyond NOT_READY_FOR_STAGE_20?",
    ], 1)]
    practices = [{"practice_id": f"AL7074-PR-{i:02d}", "practice": name, "state": "bounded_learning_lens", "qualification_claimed": False} for i, name in enumerate([
        "abstract rewriting systems researcher", "formal methods engineer", "proof artifact librarian", "compiler transformation analyst", "incident workflow analyst", "accessibility documentation specialist", "provenance archivist", "governance policy analyst",
    ], 1)]
    successors = [{"recommendation_id": f"AL7074-SR-{i:02d}", "prospective_owner": "Sable Rook", "practice": name, "state": "advisory_zero_credit", "qualification_claimed": False} for i, name in enumerate([
        "term-rewriting verification analyst", "software configuration migration reviewer", "digital-preservation accession specialist", "accessible formal-methods educator",
    ], 1)]
    hooks = [{"hook_id": f"AL7074-HOOK-{i:02d}", "name": name, "planned_stage": "x2", "installed": False, "live_host_observations": 0, "state": "planned"} for i, name in enumerate([
        "record-shape advisory", "closure advisory", "termination advisory", "normal-form advisory", "peak advisory", "joinability advisory", "confluence advisory", "rule-deletion advisory", "relabel advisory", "authority-hold advisory",
    ], 1)]
    capability_plan = {
        "x1": {"skills": [f"ghc-family-reduction-{name}" for name in ["record-shape", "relation-normalization", "closure", "strong-components", "termination", "normal-forms", "descendants", "local-peaks", "joinability", "local-confluence"]], "runners": [f"ghc_family_reduction_x1_{i:02d}.py" for i in range(1, 6)]},
        "x2": {"skills": [f"ghc-family-reduction-{name}" for name in ["global-confluence", "unique-normal-form", "newman-implication", "rule-deletion", "relabel-covariance", "strategy-trace", "accessible-summary", "three-coordinate-model", "empirical-gap", "authority-hold"]], "runners": [f"ghc_family_reduction_x2_{i:02d}.py" for i in range(1, 6)]},
        "successor_skill_ideas": ["finite reduction provenance", "accessible divergence view", "rule version reconciliation", "held-gate propagation", "countermodel index"],
        "successor_runner_ideas": ["provenance replay", "divergence renderer", "version differ", "gate auditor", "countermodel verifier"],
    }
    workload = {
        "inherited_zero_credit": 300,
        "new_contracts": 300,
        "safe_x1": 450,
        "candidate_x1": 300,
        "refusal_x1": 300,
        "cfr_x1": 300,
        "safe_x2": 450,
        "candidate_x2": 300,
        "refusal_x2": 300,
        "cfr_x2": 300,
        "exact_held": 50,
        "blocked_held": 30,
        "skills_x1": 10,
        "skills_x2": 10,
        "runners_x1": 5,
        "runners_x2": 5,
        "x1_tests": 20,
        "x2_tests": 30,
        "x2_models": 15,
        "hooks": 10,
        "law_hypotheses": 15,
        "open_problem_probes": 15,
        "practices": 8,
        "successor_practices": 4,
        "planned_purchased_spend_usd": 0,
    }
    definitions = {
        "domain": "finite abstract reduction systems and exact confluence bookkeeping",
        "fixture_count": 15,
        "operation_count": 20,
        "contract_count": 300,
        "stages": {"x1": [row[1] for row in OPERATIONS if row[2] == "x1"], "x2": [row[1] for row in OPERATIONS if row[2] == "x2"]},
        "outcomes": {"completed": 255, "represented": 15, "open_gap": 15, "exact_gate": 15},
        "malformed_subject_policy": "Every invalid subject remains failed at zero original credit even when a separate refusal guard or corrected-copy witness passes.",
        "byte_domain": "raw Git blob SHA-1 and SHA-256; UTF-8 text authored with LF line endings",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": BOUNDARY,
    }

    write_json(planning / "identity.json", identity)
    write_json(planning / "source-proof.json", source_proof)
    write_json(planning / "workflow-v19.json", workflow)
    write_json(planning / "definitions.json", definitions)
    write_json(planning / "fixtures.json", {"count": 15, "fixtures": FIXTURES, "boundary": BOUNDARY})
    write_json(planning / "operations.json", {"count": 20, "operations": operations, "boundary": BOUNDARY})
    write_json(planning / "proposals.json", {"count": 300, "planning_only": True, "outcomes": definitions["outcomes"], "proposals": proposals, "boundary": BOUNDARY})
    write_json(planning / "inherited-zero-credit.json", {"count": 300, "source_fold_count": 1, "records": inherited, "boundary": BOUNDARY})
    write_json(planning / "approval-packets.json", {"exact_count": 50, "blocked_count": 30, "exact": exact_packets, "blocked": blocked_packets, "boundary": BOUNDARY})
    write_json(planning / "law-hypotheses.json", {"count": 15, "records": laws, "boundary": BOUNDARY})
    write_json(planning / "open-problem-probes.json", {"count": 15, "records": probes, "boundary": BOUNDARY})
    write_json(planning / "practices.json", {"count": 8, "records": practices, "boundary": BOUNDARY})
    write_json(planning / "successor-recommendations.json", {"count": 4, "records": successors, "boundary": BOUNDARY})
    write_json(planning / "hook-plan.json", {"count": 10, "records": hooks, "boundary": BOUNDARY})
    write_json(planning / "capability-plan.json", capability_plan)
    write_json(planning / "workload.json", workload)
    write_json(planning / "method-flow.json", method_flow())

    write_text(planning / "plan.md", f"""# Auren Lark v707-v4 planning-only freeze

## Scope

This planning state freezes a new finite abstract-reduction-system and confluence domain before x1 implementation. It contains fifteen wholly synthetic fixtures, twenty frozen mechanisms, 300 new contracts, and 300 inherited Mira references with zero Auren novelty and completion credit. It does not execute the x1 or x2 domain, tests, skills, runners, hooks, or canonical validator.

## Lifecycle

The source is Mira Fenwick exact final `{SOURCE}`. Planning must be committed, pushed, clean, typed 0/0 divergent, and fresh-live equal before x1 work begins. X1 must meet the same gate before x2 begins. X2 must meet the same gate before final closeout begins. The one owner-scoped metadata canonical may run only after the clean pushed exact final and may not be replayed after success.

## Evidence and credit

The four exact outcome labels are `completed`, `represented`, `open_gap`, and `exact_gate`. Every malformed subject remains failed at zero original credit even if a distinct refusal or corrected-copy witness passes. Inherited proposals, source evidence, and predecessor validation remain attributable to Mira and receive zero Auren novelty or automatic completion credit.

## Boundaries

{BOUNDARY}

`Auren Lark`, they/them, the role `finite-reduction confluence cartographer`, and the declared hope are relational working language only. Hamish may rename, pause, narrow, redirect, or stop the route. Sable Rook v707-v5 remains prospective and uncontacted until Auren's own terminal gate.
""")
    write_text(planning / "planning-freeze.md", f"""# Frozen planning declaration

- owner: {OWNER}
- phase: {PHASE}
- source: `{SOURCE}`
- branch: `{BRANCH}`
- domain: finite abstract reduction systems and exact confluence bookkeeping
- new contracts: 300
- inherited zero-credit references: 300
- outcomes: 255 completed / 15 represented / 15 open_gap / 15 exact_gate
- source solver, tests, skills, runners, hooks, and canonical replayed: no
- x1 executed: no
- x2 executed: no
- successor contacted: no
- terminal verdict: `NOT_READY_FOR_STAGE_20`

This file freezes definitions and counts before x1 implementation. Later corrections, if required, must be additive and must not erase this state.
""")

    manifest_path = planning / "manifest.json"
    entries = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path == manifest_path:
            continue
        data = path.read_bytes()
        entries.append({"path": path.relative_to(repo).as_posix(), "bytes": len(data), "git_blob_sha1": git_oid(data), "sha256": sha256(data).hexdigest()})
    write_json(manifest_path, {"schema": "ghc.family.git-blob-manifest.v1", "count": len(entries), "entries": entries, "self_exclusions": ["planning/manifest.json"], "boundary": "Raw Git-blob byte parity only; not semantic correctness or independent reproduction."})
    print(json.dumps({"state": "PLANNING_BUILT", "files": len(entries) + 1, "contracts": len(proposals), "inherited": len(inherited), "activation_failures_retained": len(FAILURES)}, sort_keys=True))


if __name__ == "__main__":
    build()
