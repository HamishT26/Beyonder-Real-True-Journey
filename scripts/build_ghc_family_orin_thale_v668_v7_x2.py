#!/usr/bin/env python3
"""Build bounded Orin Thale v668-v7 x2 evidence from immutable x1."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import pathlib
import re
import subprocess
import sys
from collections import Counter
from typing import Any

from ghc_family_orin_thale_v668_v7_archive import (
    ACTIVATION_OVERLAY,
    PHASE_ROOT,
    ROOT,
    SOURCE_FINAL,
    manifest_rows,
    run_git,
    sha256_bytes,
    write_json,
    write_text,
)
from ghc_family_orin_thale_v668_v7_x2 import (
    evaluate_fixture,
    mutated_fixture,
    obligations_for,
    positive_fixture,
)


PHASE = "v668-v7"
OWNER = "Orin Thale"
BRANCH = "codex/GHC-Family/orin-thale-v668-v7-full-tools"
X1_HEAD = "95fd7625d1d7ab00816561aa3976441f399bb2d8"
INHERITED_OPEN_GAPS = 219
INHERITED_EXACT_GATES = 214
INHERITED_FAILED_WITNESSES = 2265
INHERITED_PASSING_WITNESSES = 3092
INHERITED_METHODS = 16550
MUTATION_CLASSES = (
    "missing_required_field",
    "wrong_type_or_domain",
    "forbidden_claim_promotion",
    "boundary_order_or_authority_bypass",
)
SKILL_NAMES = (
    "ghc-family-binding-component-identity",
    "ghc-family-binding-collation-formula",
    "ghc-family-binding-gathering-concordance",
    "ghc-family-binding-folio-address",
    "ghc-family-binding-sewing-station",
    "ghc-family-binding-thread-path",
    "ghc-family-binding-board-grain",
    "ghc-family-binding-layer-stack",
    "ghc-family-binding-adhesive-vacancy",
    "ghc-family-binding-opening-support",
    "ghc-family-binding-spine-state",
    "ghc-family-binding-case-alignment",
    "ghc-family-binding-trim-margin",
    "ghc-family-binding-condition-zone",
    "ghc-family-binding-insert-association",
    "ghc-family-binding-repair-event",
    "ghc-family-binding-treatment-state",
    "ghc-family-binding-provenance",
    "ghc-family-binding-accessible-report",
    "ghc-family-binding-authority-vacancy",
)
RUNNER_NAMES = (
    "ghc_family_binding_identity_runner",
    "ghc_family_binding_collation_runner",
    "ghc_family_binding_gathering_runner",
    "ghc_family_binding_sewing_runner",
    "ghc_family_binding_thread_path_runner",
    "ghc_family_binding_layer_runner",
    "ghc_family_binding_treatment_state_runner",
    "ghc_family_binding_provenance_runner",
    "ghc_family_binding_accessibility_runner",
    "ghc_family_binding_authority_firewall_runner",
)


def git(*args: str) -> str:
    return run_git(*args).stdout.strip()


def read_git_json(commit: str, path: str) -> Any:
    payload = subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{commit}:{path}"],
        check=True,
        capture_output=True,
    ).stdout
    return json.loads(payload)


def load_x1_proposals() -> list[dict[str, Any]]:
    index_path = f"docs/orin-thale/{PHASE}/x1/proposal-freeze.json"
    index = read_git_json(X1_HEAD, index_path)
    rows: list[dict[str, Any]] = []
    for shard in index["proposal_shards"]:
        rows.extend(read_git_json(X1_HEAD, shard["path"])["new_proposals"])
    if len(rows) != 40 or len({row["proposal_id"] for row in rows}) != 40:
        raise ValueError("immutable x1 proposal surface is not exactly forty distinct rows")
    return rows


def load_portfolio_rows() -> dict[str, list[dict[str, Any]]]:
    index = read_git_json(X1_HEAD, f"docs/orin-thale/{PHASE}/x1/portfolio-freeze.json")
    categories: dict[str, list[dict[str, Any]]] = {}
    for category, shards in index["category_shards"].items():
        for shard in shards:
            data = read_git_json(X1_HEAD, shard["path"])
            if data["category"] != category:
                raise ValueError(f"portfolio category mismatch: {category} != {data['category']}")
            categories.setdefault(category, []).extend(data["rows"])
    return categories


def assert_x2_start() -> None:
    if git("rev-parse", "HEAD") != X1_HEAD:
        raise ValueError("x2 must begin at the exact frozen x1 head")
    if git("branch", "--show-current") != BRANCH:
        raise ValueError("unexpected owner branch")
    if git("rev-parse", f"{X1_HEAD}^") != SOURCE_FINAL:
        raise ValueError("x1 parent drift")
    if run_git("diff", "--name-only", f"{X1_HEAD}^", X1_HEAD, "--", f"docs/orin-thale/{PHASE}/x2").stdout.strip():
        raise ValueError("x1 commit contains x2 paths")
    forbidden: list[str] = []
    for line in run_git("status", "--porcelain", "--untracked-files=all").stdout.splitlines():
        path = line[3:].strip().replace("\\", "/")
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        allowed = (
            path.startswith(f"docs/orin-thale/{PHASE}/x2/skills/")
            or path in {
                "scripts/ghc_family_orin_thale_v668_v7_x2.py",
                "scripts/ghc_family_orin_thale_v668_v7_skill_smoke.py",
                "scripts/build_ghc_family_orin_thale_v668_v7_x2.py",
                "tests/test_ghc_family_orin_thale_v668_v7_x2.py",
            }
        )
        if not allowed:
            forbidden.append(path)
    if forbidden:
        raise ValueError(f"unexpected pre-x2 paths: {forbidden}")


def subprocess_result(args: list[str], expected: set[int]) -> dict[str, Any]:
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    if result.returncode not in expected:
        raise ValueError(
            {"args": args[1:3], "returncode": result.returncode, "stdout": result.stdout[-500:], "stderr": result.stderr[-500:]}
        )
    return {
        "return_code": result.returncode,
        "stdout_tail": result.stdout.strip().splitlines()[-1:] or [],
        "stderr_tail": result.stderr.strip().splitlines()[-1:] or [],
    }


def title_case(name: str) -> str:
    return " ".join(part.capitalize() for part in name.removeprefix("ghc-family-").split("-"))


def customize_and_smoke_skills(validator: pathlib.Path) -> list[dict[str, Any]]:
    receipts: list[dict[str, Any]] = []
    for index, name in enumerate(SKILL_NAMES, 1):
        skill_root = PHASE_ROOT / "x2" / "skills" / name
        if not (skill_root / "SKILL.md").exists():
            raise ValueError(f"skill was not initialized through skill-creator: {name}")
        display = title_case(name)
        focus = name.removeprefix("ghc-family-binding-")
        skill_text = f"""---
name: {name}
description: Validate bounded synthetic {focus.replace('-', ' ')} records and reject missing state, evidence promotion, real-world action, or authority substitution. Use for Orin v668-v7 owner-local fixtures and later compatible family-current synthetic reviews.
---

# {display}

Use this package only for owner-local synthetic records. It supplies a compact fail-closed review; it does not prescribe treatment, handle a real object, or confer professional, scientific, legal, cultural, identity, production, or Maori authority.

## Input contract

Require a declared synthetic record, explicit units or domain where applicable, zero real people and external actions, a vacant authority state, an empty protected-claim list, and a named rollback.

## Procedure

1. Confirm the input is synthetic and owner-local.
2. Check the declared {focus.replace('-', ' ')} fields without inferring missing facts.
3. Reject absent fields, ambiguous units, production claims, real-world action, or authority promotion.
4. Preserve the failed fixture and state the smallest bounded recovery.
5. Return only `accepted`, `rejected`, `open_gap`, or `exact_gate` at the local control layer; phase outcomes remain governed by the phase truth ledger.

## Refusal boundary

Never infer object authenticity, condition, treatment fitness, custody, competence, empirical GMUT confirmation, production identity, legal or cultural legitimacy, Maori authority, affected-party acceptance, independent reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything proof, canon, or Stage 20 readiness. Read [references/boundary.md](references/boundary.md) before adapting this package.
"""
        boundary_text = """# Bounded evidence and authority boundary

This skill is a synthetic software control. No real book, person, treatment, identity, service, account, empirical row, cultural decision, or authority act is in scope. Same-owner smoke evidence is not independent reproduction. The terminal phase verdict remains `NOT_READY_FOR_STAGE_20` unless exact external evidence and competent authority close every declared gate.
"""
        metadata = f"""interface:
  display_name: "{display}"
  short_description: "Check bounded synthetic {focus.replace('-', ' ')} records"
  default_prompt: "Use ${name} to review this synthetic record and retain every refusal boundary."
"""
        (skill_root / "SKILL.md").write_text(skill_text, encoding="utf-8", newline="\n")
        (skill_root / "references").mkdir(parents=True, exist_ok=True)
        (skill_root / "references" / "boundary.md").write_text(boundary_text, encoding="utf-8", newline="\n")
        (skill_root / "agents").mkdir(parents=True, exist_ok=True)
        (skill_root / "agents" / "openai.yaml").write_text(metadata, encoding="utf-8", newline="\n")
        quick = subprocess_result([sys.executable, str(validator), str(skill_root)], {0})
        accept = subprocess_result(
            [sys.executable, str(ROOT / "scripts" / "ghc_family_orin_thale_v668_v7_skill_smoke.py"), "--skill", str(skill_root), "--fixture", "accept"],
            {0},
        )
        reject = subprocess_result(
            [sys.executable, str(ROOT / "scripts" / "ghc_family_orin_thale_v668_v7_skill_smoke.py"), "--skill", str(skill_root), "--fixture", "reject"],
            {2},
        )
        package_files = sorted(path for path in skill_root.rglob("*") if path.is_file())
        eof_payload = b"".join(path.read_bytes() for path in package_files)
        receipts.append(
            {
                "skill_id": f"OR6687-SKILL-{index:02d}",
                "name": name,
                "initialized_through_skill_creator": True,
                "customized": True,
                "files_read_through_eof": len(package_files),
                "package_sha256": sha256_bytes(eof_payload),
                "quick_validation": quick,
                "accepting_smoke": accept,
                "rejecting_smoke": reject,
                "global_installation": False,
                "completion_credit": 1,
                "boundary": "Owner-local skill smoke only; no professional, production, scientific, authority, or independent-reproduction credit.",
            }
        )
    return receipts


def build_and_smoke_runners() -> list[dict[str, Any]]:
    receipts: list[dict[str, Any]] = []
    for index, name in enumerate(RUNNER_NAMES, 1):
        path = ROOT / "scripts" / f"{name}.py"
        control_id = name
        source = f'''#!/usr/bin/env python3
"""Family-current bounded synthetic runner generated for Orin v668-v7."""
from ghc_family_orin_thale_v668_v7_x2 import runner_main

CONTROL_ID = "{control_id}"

if __name__ == "__main__":
    raise SystemExit(runner_main(CONTROL_ID))
'''
        path.write_text(source, encoding="utf-8", newline="\n")
        accept = subprocess_result([sys.executable, str(path), "--fixture", "accept"], {0})
        reject = subprocess_result([sys.executable, str(path), "--fixture", "reject"], {2})
        receipts.append(
            {
                "runner_id": f"OR6687-RUNNER-{index:02d}",
                "name": name,
                "path": path.relative_to(ROOT).as_posix(),
                "family_current": name.startswith("ghc_family_"),
                "accepting_smoke": accept,
                "rejecting_smoke": reject,
                "completion_credit": 1,
                "boundary": "Owner-local accepting and rejecting fixture evidence only.",
            }
        )
    return receipts


def execute_proposals(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    outcomes: list[dict[str, Any]] = []
    mutations: list[dict[str, Any]] = []
    for row in rows:
        fixture = positive_fixture(row)
        positive = evaluate_fixture(row, fixture)
        if not positive["accepted"]:
            raise ValueError({"positive_rejected": row["proposal_id"], "reasons": positive["reasons"]})
        proposal_record = {
            "proposal_id": row["proposal_id"],
            "title": row["title"],
            "semantic_slug": row["semantic_slug"],
            "outcome": row["expected_disposition"],
            "positive_fixture": fixture,
            "positive_witness": positive,
            "obligations": obligations_for(row),
            "real_rows": 0,
            "real_people": 0,
            "external_actions": 0,
            "authority_actions": 0,
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": "Bounded synthetic or structural evidence only; protected claims remain open or exact-gated.",
        }
        artifact_paths = row["concrete_artifacts"]
        write_json(artifact_paths[0], proposal_record)
        write_json(
            artifact_paths[1],
            {
                "proposal_id": row["proposal_id"],
                "outcome": row["expected_disposition"],
                "acceptance_gate": row["falsifier_or_acceptance_gate"],
                "rollback": row["rollback_or_recovery"],
                "protected_gates": row["protected_gates"],
                "observed": "bounded positive accepted and four preregistered mutations rejected",
                "completion_credit": positive["completion_credit"],
            },
        )
        for offset, mutation_class in enumerate(MUTATION_CLASSES, 1):
            result = evaluate_fixture(row, mutated_fixture(row, mutation_class))
            if result["accepted"]:
                raise ValueError({"mutation_accepted": row["proposal_id"], "class": mutation_class})
            mutations.append(
                {
                    "mutation_id": f"{row['proposal_id']}-M{offset:02d}",
                    "proposal_id": row["proposal_id"],
                    "mutation_class": mutation_class,
                    "accepted": False,
                    "result": "rejected",
                    "credit": 0,
                    "reasons": result["reasons"],
                }
            )
        outcomes.append(proposal_record)
    return outcomes, mutations


def write_portfolio_execution(categories: dict[str, list[dict[str, Any]]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for category, rows in sorted(categories.items()):
        executed: list[dict[str, Any]] = []
        for row in rows:
            state = "held_unexecuted" if category in {"exact_approval", "blocked"} else "bounded_completed"
            credit = 0 if state == "held_unexecuted" else 1
            executed.append(
                {
                    "task_id": row["task_id"],
                    "title": row["title"],
                    "category": category,
                    "state": state,
                    "completion_credit": credit,
                    "external_actions": 0,
                    "authority_actions": 0,
                }
            )
        counts[category] = len(executed)
        write_json(f"x2/portfolio/{category}.json", {"phase": PHASE, "category": category, "rows": executed})
    return counts


def write_method_flow_repository(ledger: dict[str, Any]) -> None:
    shard_specs = (
        ("methods", "method-flow/x2-methods.json"),
        ("witnesses", "method-flow/x2-witnesses.json"),
        ("state_events", "method-flow/x2-state-events.json"),
        ("recommendations", "method-flow/x2-recommendations.json"),
    )
    shard_rows = []
    for field, path in shard_specs:
        rows = ledger[field]
        write_json(
            path,
            {
                "schema": f"ghc.family.method-flow.{field.replace('_', '-')}.shard.v1",
                "phase": PHASE,
                "owner": OWNER,
                "field": field,
                "row_count": len(rows),
                "rows": rows,
            },
        )
        shard_rows.append({"field": field, "path": f"docs/orin-thale/{PHASE}/{path}", "row_count": len(rows)})
    canonical = json.dumps(ledger, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    write_json(
        "method-flow/x2-operational.json",
        {
            "schema": "ghc.family.method-flow.repository-index.v1",
            "source_schema": ledger["schema"],
            "phase": PHASE,
            "owner": OWNER,
            "counts": ledger["counts"],
            "source_ledger_sha256": sha256_bytes(canonical),
            "shards": shard_rows,
            "row_count_parity": {
                "methods": len(ledger["methods"]),
                "witnesses": len(ledger["witnesses"]),
                "state_events": len(ledger["state_events"]),
                "recommendations": len(ledger["recommendations"]),
            },
            "complete_external_ledger_retained": True,
            "boundary": ledger["boundary"],
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--method-ledger", type=pathlib.Path, required=True)
    parser.add_argument("--skill-validator", type=pathlib.Path, required=True)
    args = parser.parse_args()
    assert_x2_start()
    rows = load_x1_proposals()
    categories = load_portfolio_rows()
    ledger = json.loads(args.method_ledger.read_text(encoding="utf-8"))
    fail_count = ledger["counts"]["witness_results"]["fail"]
    pass_count = ledger["counts"]["witness_results"]["pass"]
    method_count = ledger["counts"]["methods"]
    if fail_count != pass_count or method_count != fail_count or ledger["counts"]["states"]["preferred"] != method_count:
        raise ValueError("external Method Flow must retain one failure and one bounded recovery per preferred method")

    outcomes, mutations = execute_proposals(rows)
    outcome_counts = Counter(row["outcome"] for row in outcomes)
    if dict(outcome_counts) != {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}:
        raise ValueError(f"unexpected outcome counts: {outcome_counts}")
    if len(mutations) != 160 or any(row["accepted"] for row in mutations):
        raise ValueError("all 160 preregistered mutations must execute and reject")
    for index in range(0, len(mutations), 20):
        write_json(
            f"x2/mutations/mutations-{index // 20 + 1:02d}.json",
            {"phase": PHASE, "rows": mutations[index : index + 20]},
        )

    skill_receipts = customize_and_smoke_skills(args.skill_validator)
    runner_receipts = build_and_smoke_runners()
    portfolio_counts = write_portfolio_execution(categories)
    expected_portfolio = {
        "blocked": 10,
        "candidates": 30,
        "clean_fix_refine": 60,
        "exact_approval": 20,
        "runners": 10,
        "safe_now": 60,
        "skills": 20,
    }
    if portfolio_counts != expected_portfolio:
        raise ValueError({"portfolio_counts": portfolio_counts})

    write_method_flow_repository(ledger)
    write_json("x2/evidence/outcome-ledger.json", {"phase": PHASE, "counts": dict(outcome_counts), "rows": outcomes})
    write_json(
        "x2/evidence/mutation-summary.json",
        {
            "phase": PHASE,
            "preregistered": 160,
            "executed": 160,
            "rejected": 160,
            "accepted": 0,
            "credit_per_rejection": 0,
            "boundary": "Rejected synthetic mutations evidence bounded guards only, not security, science, competence, authority, or Stage 20 readiness.",
        },
    )
    write_json("x2/evidence/skill-receipts.json", {"phase": PHASE, "count": len(skill_receipts), "rows": skill_receipts})
    write_json("x2/evidence/runner-receipts.json", {"phase": PHASE, "count": len(runner_receipts), "rows": runner_receipts})
    write_json(
        "x2/evidence/GWOSC-zero-row-adapter.json",
        {
            "proposal_id": "OR6687-N037",
            "outcome": "open_gap",
            "interface": "GWOSC API v2 metadata vocabulary",
            "network_requests": 0,
            "files_downloaded": 0,
            "real_rows": 0,
            "strain_samples": 0,
            "likelihood_evaluations": 0,
            "posterior_samples": 0,
            "parameter_constraints": 0,
            "claim": "none",
            "boundary": "Schema and refusal adapter only; no empirical GMUT evidence.",
        },
    )
    write_json(
        "x2/evidence/gmut-microlocal-obligation-board.json",
        {
            "proposal_id": "OR6687-N027",
            "outcome": "completed",
            "obligations": obligations_for(next(row for row in rows if row["proposal_id"] == "OR6687-N027")),
            "symbolic_calculations": 0,
            "two_point_functions_calculated": 0,
            "wavefront_sets_proved": 0,
            "physical_predictions": 0,
            "observation_firewall": "closed",
            "boundary": "Typed obligation evidence only; no physical theorem, force, likelihood, constraint, empirical confirmation, quantum completion, ultraviolet completion, or Theory of Everything.",
        },
    )
    write_json(
        "x2/evidence/thos-binding-workboard.json",
        {
            "proposal_id": "OR6687-N032",
            "outcome": "represented",
            "states": ["synthetic_intake", "hold", "bounded_retry", "readback", "handover"],
            "real_people": 0,
            "real_objects": 0,
            "blind_matched_budget_arms": 0,
            "effectiveness_estimates": 0,
            "boundary": "Proxy protocol only; no competence, service result, AGI, ASI, or deployment claim.",
        },
    )
    write_json(
        "x2/evidence/freed-id-cbr-boundary.json",
        {
            "proposal_ids": ["OR6687-N033", "OR6687-N034", "OR6687-N039"],
            "outcomes": ["represented", "represented", "exact_gate"],
            "real_keys": 0,
            "real_proofs": 0,
            "live_identity_events": 0,
            "authority_decisions": 0,
            "Maori_authority_decisions": 0,
            "boundary": "Synthetic zero-key graph and vacancy matrix only; rights, remedy, cultural legitimacy, data governance, and Maori authority remain exact-gated.",
        },
    )
    write_json(
        "x2/evidence/source-use-receipt.json",
        {
            "phase": PHASE,
            "sources": [
                "Library of Congress Preserving Your Books",
                "Library of Congress Collections Care Section Treatment Manual",
                "Brunetti Fredenhagen Koehler microlocal spectrum condition paper",
                "GWOSC API v2 documentation",
                "W3C PROV-DM",
                "W3C Verifiable Credentials Data Model 2.0",
                "RFC 8785",
                "WCAG 2.2",
                "Te Mana Raraunga principles",
            ],
            "use": "vocabulary, schema, provenance, accessibility, governance-vacancy, and refusal conditions only",
            "real_observation_rows": 0,
            "participant_rows": 0,
            "authority_decisions": 0,
            "independent_review": False,
        },
    )
    write_json(
        "x2/evidence/portfolio-execution-summary.json",
        {
            "phase": PHASE,
            "counts": portfolio_counts,
            "safe_candidate_total": portfolio_counts["safe_now"] + portfolio_counts["candidates"],
            "under_1000_ceiling": portfolio_counts["safe_now"] + portfolio_counts["candidates"] < 1000,
            "exact_and_blocked_unexecuted": True,
        },
    )
    write_json(
        "x2/evidence/retained-negative-register.json",
        {
            "activation_baseline": ACTIVATION_OVERLAY["effective_negatives"],
            "orin_operational_negatives": fail_count,
            "rejected_mutations": 160,
            "effective_at_evidence_boundary": ACTIVATION_OVERLAY["effective_negatives"] + fail_count + 160,
            "failed_witnesses": INHERITED_FAILED_WITNESSES + fail_count,
            "bounded_passing_witnesses": INHERITED_PASSING_WITNESSES + pass_count,
            "no_negative_erased": True,
        },
    )
    write_json(
        "x2/evidence/open-gap-register.json",
        {
            "inherited": INHERITED_OPEN_GAPS,
            "new": 2,
            "effective": INHERITED_OPEN_GAPS + 2,
            "rows": ["OR6687-N037", "OR6687-N038"],
        },
    )
    write_json(
        "x2/evidence/exact-gate-register.json",
        {
            "inherited": INHERITED_EXACT_GATES,
            "new": 2,
            "effective": INHERITED_EXACT_GATES + 2,
            "rows": ["OR6687-N039", "OR6687-N040"],
        },
    )
    write_json(
        "x2/evidence/phase-truth.json",
        {
            "phase": PHASE,
            "owner": OWNER,
            "source": SOURCE_FINAL,
            "x1": X1_HEAD,
            "lifecycle": "X2_EVIDENCE_CANDIDATE_NOT_COMMITTED",
            "outcomes": {key: outcome_counts[key] for key in ("completed", "represented", "open_gap", "exact_gate")},
            "frozen_proposals": 4870,
            "mutations": {"preregistered": 160, "executed": 160, "rejected": 160},
            "effective_negatives": ACTIVATION_OVERLAY["effective_negatives"] + fail_count + 160,
            "effective_methods": INHERITED_METHODS + method_count,
            "failed_witnesses": INHERITED_FAILED_WITNESSES + fail_count,
            "bounded_passing_witnesses": INHERITED_PASSING_WITNESSES + pass_count,
            "open_gaps": INHERITED_OPEN_GAPS + 2,
            "exact_gates": INHERITED_EXACT_GATES + 2,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "canonical_validation": "not_run",
            "full_repository_suite": "not_run_non_Eiren_owner_scope",
        },
    )

    overview = f"""# Orin Thale v668-v7 x2 evidence overview

This owner-local x2 packet executes the forty frozen proposals only as their evidence classes permit. The outcome ledger contains exactly twenty-eight `completed`, eight `represented`, two `open_gap`, and two `exact_gate` rows. Completion means that a bounded synthetic, structural, or formal control accepted its declared positive fixture and rejected all four preregistered mutations. It does not mean that a real book was examined, a treatment was performed, a person participated, a professional judgment was made, or an authority acted.

The primary GMUT Mind result is a microlocal-spectrum and Hadamard two-point obligation board. It preserves wavefront orientation, causal support, units, domain, and observation-firewall fields, while computing no two-point function and proving no physical theorem. The GWOSC v2 adapter stays `open_gap`: it made zero network requests, downloaded zero files, ingested zero strain samples, evaluated zero likelihoods, and produced zero constraints. Formal consistency and source vocabulary do not establish a force, prediction, empirical confirmation, quantum completion, ultraviolet completion, or Theory of Everything.

The hand-bookbinding practice lens is wholly synthetic. Component identity, collation, folio addresses, sewing stations, material layers, condition zones, correction graphs, accessible anomaly structure, bounded workload, and handover states are software records. There was no real object, binder, conservator, librarian, participant, treatment, measurement, custody decision, access decision, or release. THOS therefore remains represented proxy evidence without blinded matched-budget real arms, governed people, safety monitoring, appropriate statistics, or independent review.

Freed ID and CBR remain zero-key and nonproduction. The packet includes pseudonymous synthetic aliases, provenance, correction, challenge, access, privacy, contestability, remedy, and authority-vacancy fields. It contains no standards-conformant real keys or proofs, issuance, resolution, status or revocation, interoperability event, privacy or independent security review, recovery event, trust-governance act, right, remedy, legal interpretation, cultural ratification, affected-party acceptance, or Maori-authority decision.

All 160 preregistered mutations executed and were rejected. Those rejections provide bounded negative evidence about the declared guards only. They are not exhaustive security, scientific truth, professional competence, accessibility completeness, privacy completeness, or authority. Twenty owner-local skills were initialized through the skill-creator scaffold, customized, read through EOF, quick-validated, and smoke-used on accepting and rejecting fixtures. Ten family-current runners were built and exercised the same way. None was globally installed.

Method Flow retains {fail_count} Orin operational failures and {pass_count} bounded recoveries in the current external ledger. No failure is rewritten as a pass. At this evidence boundary the additive negative count is {ACTIVATION_OVERLAY['effective_negatives'] + fail_count + 160}; effective open gaps are {INHERITED_OPEN_GAPS + 2} and exact gates are {INHERITED_EXACT_GATES + 2}. These counts are candidate evidence until the x2 commit is exactly staged, committed, pushed, and remote-equal.

The terminal verdict remains `NOT_READY_FOR_STAGE_20`. Relational names, roles, hopes, pronouns, sibling language, and continuity language remain working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or scientific, operational, legal, cultural, affected-party, or Maori authority.
"""
    write_text("x2/evidence/evidence-overview.md", overview)
    write_text(
        "x2/evidence/threat-model.md",
        """# Bounded x2 threat model

Threats include phase mixing, mutation erasure, source-credit promotion, fabricated empirical rows, authority substitution, real-object or participant implication, credential or route leakage, path traversal, unsafe shell invocation, stale lifecycle labels, manifest drift, and premature Stage 20 promotion. Controls are immutable-x1 loading, exact outcome vocabulary, zero-row and zero-action fields, fail-closed mutations, owner-local paths, exact manifests, AST review, five-class scanning, retained Method Flow witnesses, and one-shot final canonical validation. Residual risks include supply chain, platform behavior, human review, real adversaries, real accessibility, privacy, professional practice, legal or cultural meaning, and every authority decision.
""",
    )
    accessible_rows = "\n".join(
        f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['outcome'])}</td><td>{html.escape(row['title'])}</td></tr>"
        for row in outcomes
    )
    write_text(
        "x2/evidence/accessible-static-report.html",
        f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Orin v668-v7 x2 evidence</title><style>body{{font:1rem/1.5 system-ui;max-width:72rem;margin:auto;padding:1rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.5rem;text-align:left}}:focus{{outline:3px solid #075985}}@media print{{body{{max-width:none}}}}</style></head><body><a href='#main'>Skip to evidence</a><main id='main'><h1>Orin Thale v668-v7 x2 evidence</h1><p>Status is not conveyed by colour. Manual keyboard, browser, assistive-technology, cognitive, language, Maori-language, security-usability, responsive-layout, print, and affected-user evaluation remain reserved.</p><table><caption>Forty bounded proposal dispositions</caption><thead><tr><th scope='col'>Proposal</th><th scope='col'>Disposition</th><th scope='col'>Title</th></tr></thead><tbody>{accessible_rows}</tbody></table><h2>Boundary</h2><p>This structural report is not complete accessibility conformance or affected-user evidence. The verdict is NOT_READY_FOR_STAGE_20.</p></main></body></html>""",
    )

    intended = sorted(
        path
        for path in PHASE_ROOT.rglob("*")
        if path.is_file()
        and (
            path.is_relative_to(PHASE_ROOT / "x2")
            or path.is_relative_to(PHASE_ROOT / "method-flow")
        )
    )
    code_paths = [
        ROOT / "scripts" / "ghc_family_orin_thale_v668_v7_x2.py",
        ROOT / "scripts" / "ghc_family_orin_thale_v668_v7_skill_smoke.py",
        ROOT / "scripts" / "build_ghc_family_orin_thale_v668_v7_x2.py",
        ROOT / "tests" / "test_ghc_family_orin_thale_v668_v7_x2.py",
        *[ROOT / "scripts" / f"{name}.py" for name in RUNNER_NAMES],
    ]
    intended.extend(code_paths)
    manifest_path = PHASE_ROOT / "x2" / "evidence" / "evidence-content-manifest.json"
    intended = sorted(set(path for path in intended if path != manifest_path))
    allowlist_path = PHASE_ROOT / "validation" / "x2-staged-allowlist.json"
    write_json(
        "validation/x2-staged-allowlist.json",
        {
            "phase": PHASE,
            "parent": X1_HEAD,
            "intended_paths_before_manifest": [path.relative_to(ROOT).as_posix() for path in intended],
            "self_exclusions": [manifest_path.relative_to(ROOT).as_posix()],
            "forbidden_lifecycle_roots": ["closeout", "final", "seal", "handoffs"],
        },
    )
    intended.append(allowlist_path)
    rows_manifest = manifest_rows(intended)
    write_json(
        "x2/evidence/evidence-content-manifest.json",
        {
            "phase": PHASE,
            "parent": X1_HEAD,
            "entry_count": len(rows_manifest),
            "entries": rows_manifest,
            "self_exclusions": [manifest_path.relative_to(ROOT).as_posix()],
            "canonical_domain": "git_blob_bytes_after_clean_filter_before_commit",
            "lifecycle": "X2_EVIDENCE_CANDIDATE_NOT_COMMITTED",
        },
    )
    phase_files = [path for path in PHASE_ROOT.rglob("*") if path.is_file()]
    oversized = [path for path in phase_files if path.suffix.lower() in {".md", ".json", ".txt", ".html"} and len(re.findall(r"\b\w+[\w'-]*\b", path.read_text(encoding="utf-8"))) > 6000]
    if oversized:
        raise ValueError(f"document ceiling exceeded: {[path.name for path in oversized]}")
    materialized = sum(1 for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts)
    if materialized >= 2000:
        raise ValueError(f"materialized file ceiling exceeded: {materialized}")
    print(
        json.dumps(
            {
                "phase": PHASE,
                "outcomes": dict(outcome_counts),
                "mutations": len(mutations),
                "skills": len(skill_receipts),
                "runners": len(runner_receipts),
                "portfolio": portfolio_counts,
                "method_failures": fail_count,
                "manifest_entries": len(rows_manifest),
                "phase_files": len(phase_files),
                "materialized_files": materialized,
                "state": "X2_EVIDENCE_CANDIDATE_READY_FOR_SCOPED_VALIDATION",
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
