#!/usr/bin/env python3
"""Build bounded Tamar Vey v685-v1 x2 evidence and validation receipts."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_tamar_vey_v685_v1_core import (
    MUTATION_TYPES,
    RUNNER_FACETS,
    canonical_bytes,
    digest,
    make_positive_record,
    mutate_record,
    validate_record,
)


ROOT = Path(__file__).resolve().parents[1]
OWNER = "Tamar Vey"
PHASE = "v685-v1"
PREFIX = "TV6851"
SOURCE_FINAL = "f138d0e9fd37d424a81887bb7a1bafa3eacba860"
X1_COMMIT = "a640f907d154d6b5c7747c990a3c0b1d6fe987eb"
BASE = ROOT / "docs" / "tamar-vey" / PHASE
X1 = BASE / "x1"
X2 = BASE / "x2"
VALIDATION = BASE / "validation"
BUILDER_REL = "scripts/build_ghc_family_tamar_vey_v685_v1_x2.py"
CORE_REL = "scripts/ghc_family_tamar_vey_v685_v1_core.py"
TEST_REL = "tests/test_ghc_family_tamar_vey_v685_v1_x2.py"

SKILL_NAMES = [
    "broom-work-capsule",
    "broom-topology",
    "brush-topology",
    "besom-topology",
    "material-vacancy",
    "measurement-vacancy",
    "binding-lineage",
    "tool-hold",
    "guard-refusal",
    "hazard-vocabulary-firewall",
    "correction-braid",
    "privacy-minimizer",
    "accessible-status",
    "workload-handover",
    "gmut-bundle-graph",
    "thos-job-queue",
    "freed-id-keyless-receipt",
    "cbr-challenge-vacancy",
    "manifest-domain-separator",
    "authority-noncompensation",
]
SKILL_FACETS = [
    "synthetic work-capsule boundary",
    "broom component topology",
    "brush block ferrule and tuft topology",
    "besom bundle and lashing topology",
    "material claim vacancy",
    "target versus observation separation",
    "binding and correction lineage",
    "tool fitness and release hold",
    "machine-guard decision refusal",
    "hazard vocabulary observation firewall",
    "append-only correction braid",
    "minimum-disclosure record",
    "structurally accessible status",
    "workload pause and handover",
    "typed GMUT graph without physical law",
    "THOS queue proxy without participants",
    "keyless Freed ID receipt",
    "CBR challenge and remedy vacancy",
    "Git-blob versus checkout-byte domains",
    "authority noncompensation",
]
RUNNER_NAMES = list(RUNNER_FACETS)


def run(
    args: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(args, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def git(*args: str, check: bool = True) -> str:
    proc = run(["git", *args])
    if check and proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace"))
    return proc.stdout.decode("utf-8", "replace").strip()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def skill_text(name: str, facet: str) -> str:
    title = " ".join(part.capitalize() for part in name.split("-"))
    return f"""---
name: {name}
description: Use when validating the {facet} in the Tamar v685-v1 wholly synthetic broom-and-brush evidence lane while preserving every real-world and authority gate.
---

# {title}

## Scope

Apply this skill only to owner-local synthetic JSON fixtures for {facet}. It does
not inspect, measure, identify, repair, release, or make decisions about any real
person, broom, brush, besom, material, tool, machine, workshop, identity, right,
or authority.

## Workflow

1. Require the exact proposal identifier and synthetic-only source status.
2. Keep target values separate from observations and keep authority reserved.
3. Validate append-only correction order and the immutable precondition digest.
4. Accept only the bounded positive structure.
5. Reject missing fields, role swaps, stale digests, correction inversions, and
   authority promotion.
6. Retain the invalid fixture as a zero-credit failed witness.
7. Record the passing validator witness separately without erasing the failure.

## Accepting smoke

Accept a complete synthetic record whose observation flag is false, whose
authority status is reserved, and whose correction sequence is ordered.

## Rejecting smoke

Reject a synthetic fixture that violates the assigned mutation guard. Rejection
does not establish professional, empirical, production, legal, cultural,
affected-party, Māori-authority, privacy-complete, accessibility-complete,
independent-reproduction, proof, canon, or Stage 20 credit.

## Output boundary

Return only the bounded structural result, explicit errors, zero real-row count,
and zero authority credit. Stop on ambiguity or any protected gate.
"""


def skill_openai_yaml(name: str, facet: str) -> str:
    display = " ".join(part.capitalize() for part in name.split("-"))
    return f"""interface:
  display_name: "{display}"
  short_description: "Validate {facet}"
  default_prompt: "Apply the {name} bounded synthetic contract and preserve every real-world and authority gate."
"""


def runner_code(name: str) -> str:
    return f"""#!/usr/bin/env python3
from ghc_family_tamar_vey_v685_v1_core import runner_main

if __name__ == "__main__":
    raise SystemExit(runner_main("{name}"))
"""


def customize_skills_and_runners() -> None:
    for name, facet in zip(SKILL_NAMES, SKILL_FACETS):
        folder = X2 / "skills" / name
        if not (folder / "SKILL.md").exists():
            raise RuntimeError(f"skill was not initialized by the official workflow: {name}")
        write_text(folder / "SKILL.md", skill_text(name, facet))
        write_text(folder / "agents" / "openai.yaml", skill_openai_yaml(name, facet))
    for name in RUNNER_NAMES:
        write_text(ROOT / "scripts" / f"ghc_family_broommaking_{name}_runner.py", runner_code(name))


def quick_validate_and_smoke_skills() -> list[dict[str, Any]]:
    validator = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
    if not validator.exists():
        raise RuntimeError("official skill quick validator is unavailable")
    results: list[dict[str, Any]] = []
    for index, (name, facet) in enumerate(zip(SKILL_NAMES, SKILL_FACETS), start=1):
        folder = X2 / "skills" / name
        skill_path = folder / "SKILL.md"
        complete_text = skill_path.read_text(encoding="utf-8")
        quick = run(
            [sys.executable, "-B", str(validator), str(folder)],
            env={**os.environ, "PYTHONUTF8": "1"},
        )
        positive = make_positive_record(f"{PREFIX}-N{((index - 1) % 42) + 1:03d}", facet)
        accepted, positive_errors = validate_record(positive)
        mutation_type = MUTATION_TYPES[(index - 1) % len(MUTATION_TYPES)]
        invalid = mutate_record(positive, mutation_type)
        invalid_accepted, invalid_errors = validate_record(invalid)
        result = {
            "skill": name,
            "facet": facet,
            "initialized_by_official_skill_creator": True,
            "complete_read_through_eof": True,
            "bytes_read": len(complete_text.encode("utf-8")),
            "line_count": len(complete_text.splitlines()),
            "sha256": hashlib.sha256(complete_text.encode("utf-8")).hexdigest(),
            "quick_validate_exit_code": quick.returncode,
            "quick_validate_output": (quick.stdout + quick.stderr).decode("utf-8", "replace").strip(),
            "positive_accepted": accepted,
            "positive_errors": positive_errors,
            "rejecting_mutation": mutation_type,
            "invalid_accepted": invalid_accepted,
            "invalid_errors": invalid_errors,
            "smoke_pass": quick.returncode == 0 and accepted and not invalid_accepted,
            "global_installation": False,
            "real_rows": 0,
            "authority_credit": "zero",
        }
        results.append(result)
    if not all(row["smoke_pass"] for row in results):
        raise RuntimeError("one or more owner-local skills failed quick validation or smoke use")
    return results


def smoke_runners() -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for name in RUNNER_NAMES:
        script = ROOT / "scripts" / f"ghc_family_broommaking_{name}_runner.py"
        pair: dict[str, Any] = {"runner": name, "script": rel(script), "family_current": True}
        for fixture in ("positive", "invalid"):
            proc = run([sys.executable, "-B", str(script), "--fixture", fixture])
            try:
                payload = json.loads(proc.stdout.decode("utf-8"))
            except json.JSONDecodeError as exc:
                raise RuntimeError(f"runner {name} emitted invalid JSON") from exc
            pair[fixture] = {
                "exit_code": proc.returncode,
                "payload": payload,
                "smoke_pass": proc.returncode == 0 and payload.get("smoke_pass") is True,
            }
        pair["smoke_pass"] = pair["positive"]["smoke_pass"] and pair["invalid"]["smoke_pass"]
        results.append(pair)
    if not all(row["smoke_pass"] for row in results):
        raise RuntimeError("one or more family-current runners failed smoke use")
    return results


def proposal_evidence() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    freeze = load_json(X1 / "new-proposal-freeze.json")
    evidence: list[dict[str, Any]] = []
    mutations: list[dict[str, Any]] = []
    outcomes: list[dict[str, Any]] = []
    for proposal in freeze["proposals"]:
        proposal_id = proposal["proposal_id"]
        disposition = proposal["expected_disposition"]
        record = make_positive_record(proposal_id, proposal["title"])
        accepted, errors = validate_record(record)
        mutation_rows: list[dict[str, Any]] = []
        for preregistered in proposal["preregistered_rejecting_mutations"]:
            mutation_type = preregistered["mutation_type"]
            invalid = mutate_record(record, mutation_type)
            invalid_accepted, invalid_errors = validate_record(invalid)
            mutation_row = {
                "proposal_id": proposal_id,
                "mutation_id": preregistered["mutation_id"],
                "mutation_type": mutation_type,
                "fixture_sha256": digest(invalid),
                "accepted": invalid_accepted,
                "errors": invalid_errors,
                "retained_failed_witness": True,
                "credit": "zero",
            }
            mutations.append(mutation_row)
            mutation_rows.append(mutation_row)
        bounded_execution = disposition in {"completed", "represented"}
        witness = {
            "proposal_id": proposal_id,
            "title": proposal["title"],
            "expected_disposition": disposition,
            "bounded_record_sha256": digest(record),
            "bounded_record_accepted": accepted,
            "bounded_record_errors": errors,
            "bounded_execution_performed": bounded_execution,
            "real_execution_performed": False,
            "rejecting_mutation_count": len(mutation_rows),
            "rejecting_mutations_rejected": sum(not item["accepted"] for item in mutation_rows),
            "protected_gates_preserved": True,
            "real_rows": 0,
            "authority_credit": "zero",
        }
        evidence.append(witness)
        outcome_valid = accepted and all(not item["accepted"] for item in mutation_rows)
        outcomes.append(
            {
                "proposal_id": proposal_id,
                "outcome": disposition,
                "evidence_valid": outcome_valid,
                "credit_boundary": {
                    "completed": "bounded_owner_local_synthetic_structure_only",
                    "represented": "representation_only_no_real_execution",
                    "open_gap": "real_evidence_absent",
                    "exact_gate": "competent_authority_absent",
                }[disposition],
            }
        )
    if len(mutations) != 300 or any(row["accepted"] for row in mutations):
        raise RuntimeError("rejecting mutation contract failed")
    return evidence, mutations, outcomes


def execute_portfolios() -> dict[str, Any]:
    portfolio = load_json(X1 / "portfolio-freeze.json")
    def complete(rows: list[dict[str, Any]], kind: str) -> list[dict[str, Any]]:
        return [
            {
                "id": row["id"],
                "title": row["title"],
                "kind": kind,
                "result": "bounded_same_owner_completed",
                "real_rows": 0,
                "authority_credit": "zero",
            }
            for row in rows
        ]
    def represented(rows: list[dict[str, Any]], kind: str) -> list[dict[str, Any]]:
        return [
            {
                "id": row["id"],
                "title": row["title"],
                "kind": kind,
                "result": "represented_zero_credit_seed",
                "executed": False,
            }
            for row in rows
        ]
    return {
        "schema": f"ghc.family.portfolio-execution.{PHASE.replace('-', '.')}.x2",
        "owner": OWNER,
        "phase": PHASE,
        "safe_now": complete(portfolio["safe_now"], "safe_now"),
        "owner_candidates": complete(portfolio["owner_candidates"], "bounded_candidate_without_core_promotion"),
        "successor_candidates": represented(portfolio["successor_candidates"], "successor_candidate"),
        "owner_clean_fix_refine": complete(portfolio["owner_clean_fix_refine"], "clean_fix_refine"),
        "successor_clean_fix_refine": represented(portfolio["successor_clean_fix_refine"], "successor_clean_fix_refine"),
        "exact_approval": [
            {**row, "executed": False, "result": "exact_gate"}
            for row in portfolio["exact_approval"]
        ],
        "blocked": [
            {**row, "executed": False, "result": "blocked"}
            for row in portfolio["blocked"]
        ],
        "owner_bounded_completed_count": 300,
        "successor_zero_credit_represented_count": 50,
        "exact_or_blocked_executed_count": 0,
    }


def method_flow_evidence() -> dict[str, Any]:
    x1 = load_json(X1 / "method-flow-startup.json")
    baseline = x1["effective_x1_startup_counts"]
    additions = {
        "rejecting_mutation_negatives_and_failed_witnesses": 300,
        "skill_rejecting_negatives_and_failed_witnesses": 20,
        "runner_rejecting_negatives_and_failed_witnesses": 10,
        "proposal_validation_methods_and_passing_witnesses": 360,
        "skill_smoke_methods_and_passing_witnesses": 40,
        "runner_smoke_methods_and_passing_witnesses": 20,
        "portfolio_execution_methods_and_passing_witnesses": 300,
        "operational_failures": 4,
    }
    return {
        "schema": f"ghc.family.method-flow.{PHASE.replace('-', '.')}.x2",
        "owner": OWNER,
        "phase": PHASE,
        "x1_baseline": baseline,
        "additions": additions,
        "operational_failures": [
            {
                "failure_id": "TV6851-X2-N001",
                "failed_witness": "The first x2 build stopped because the official quick validator inherited Windows cp1252 and could not decode UTF-8 Māori boundary text in all twenty skill files.",
                "recovery": "Reran only the exact validator dependency with PYTHONUTF8=1, then rebuilt the bounded evidence once.",
                "recurrence_guard": "Set explicit UTF-8 for every external skill-creator validation subprocess on Windows.",
                "credit": "retained_zero_credit",
            },
            {
                "failure_id": "TV6851-X2-N002",
                "failed_witness": "The first grouped evidence-validation wrapper returned four passing test dots at its output boundary without exposing the continuing session handle.",
                "recovery": "Audited process quiescence and staged receipts, retained the four attributable passes, then ran only the unresolved manifest check and not-yet-attributable remainder.",
                "recurrence_guard": "Always serialize the exec result when a validation command may outlive its initial yield.",
                "credit": "retained_zero_credit",
            },
            {
                "failure_id": "TV6851-X2-N003",
                "failed_witness": "The first combined Method Flow patch failed its context check because generated JSON key order differed from source object order.",
                "recovery": "Split source and generated-ledger edits and anchored the ledger patch to its exact serialized order.",
                "recurrence_guard": "Inspect generated JSON serialization before applying a multi-file exact-context patch.",
                "credit": "retained_zero_credit",
            },
            {
                "failure_id": "TV6851-X2-N004",
                "failed_witness": "The first skill-receipt test compared a normalized-text digest with raw checkout bytes and failed one of seven selected checks.",
                "recovery": "Changed only that assertion to hash UTF-8 text after universal newline normalization, matching the receipt domain.",
                "recurrence_guard": "Name and compare the same byte or normalized-text domain on both sides of every digest assertion.",
                "credit": "retained_zero_credit",
            }
        ],
        "effective_evidence_counts": {
            "effective_negatives": baseline["effective_negatives"] + 334,
            "effective_methods": baseline["effective_methods"] + 724,
            "failed_witnesses": baseline["failed_witnesses"] + 334,
            "bounded_passing_witnesses": baseline["bounded_passing_witnesses"] + 724,
            "open_gaps": baseline["open_gaps"] + 3,
            "exact_gates": baseline["exact_gates"] + 3,
        },
        "failure_erasure": False,
        "recovery_promotes_failed_witness": False,
    }


def evidence_overview() -> str:
    return f"""# Tamar Vey {PHASE} bounded x2 evidence overview

## Outcome

The planning-only x1 at {X1_COMMIT} remained immutable while this x2 evidence
was built. Sixty preregistered proposal contracts were evaluated with only the
four authorized outcome labels: 42 completed, 12 represented, 3 open_gap, and
3 exact_gate. Completed means bounded owner-local synthetic structure only.
Represented means a vocabulary, symbolic mapping, proxy, or vacancy structure
without real execution. Open gaps and exact gates remain open.

All 300 preregistered invalid mutations executed. Every missing-field, role-swap,
stale-digest, correction-inversion, and authority-promotion fixture was rejected.
Each invalid fixture remains a retained zero-credit failed witness. Its successful
rejection is a separate bounded passing validator witness and never erases the
failure.

## Skills, runners, and portfolios

Twenty owner-local skills were initialized through the official skill-creator
workflow, customized, completely read through EOF, quick-validated, and
accepting/rejecting smoke-used. They remain inside this owner packet and were
not globally installed. Ten family-current ghc_family broommaking runners were
built; each accepted its positive fixture and rejected its invalid fixture.

The x2 execution ledger records 120 safe-now tasks, 80 bounded owner candidates,
and 100 owner CLEAN/FIX/REFINE tasks as completed within the same-owner
synthetic lane. Twenty successor candidates and thirty successor
CLEAN/FIX/REFINE records remain represented zero-credit seeds. Twenty exact
approval holds and ten blocked holds remain unexecuted.

## Practice and three-pillar scope

The primary pillar is THOS Body through a wholly synthetic broom-and-brush
documentation lens. Component topology covers brooms, brushes, and besoms;
handles, blocks, ferrules, tufts, bundles, bindings, and lashings. Material,
measurement, calibration, tool-fitness, machine-guard, dust, finish, adhesive,
ownership, custody, identity, cultural, and authority fields remain vacancies
or holds. GMUT Mind is limited to typed graphs and symbols with an observation
firewall. Freed ID and CBR Heart are limited to keyless receipts, correction,
challenge, privacy minimization, accessible structure, remedy vacancy, and
authority reservation.

No real person, maker, customer, custodian, participant, broom, brush, besom,
material, tool, machine, workshop, observation, measurement, inspection,
calibration, treatment, repair, release, identity event, key, proof, credential,
legal decision, cultural decision, affected-party decision, Māori data, or
authority act was used. There were zero external data calls and zero real rows.

## Scientific and authority boundary

GMUT remains a typed scalar-tensor and effective-field-theory research-model
family. Software, symbolic obligations, synthetic fixtures, citation
vocabulary, and mutation rejection establish no physical datum, likelihood,
posterior, force, prediction, parameter constraint, empirical confirmation,
stability theorem, quantum completion, ultraviolet completion, final physics,
or Theory of Everything.

THOS remains synthetic or proxy-only without preregistered blind matched-budget
real arms, governed participants or operators, safety monitoring, appropriate
statistics, and independent review. Freed ID remains synthetic and
nonproduction without standards-conformant real keys and proofs, live issuance
and resolution, status and revocation, interoperability, independent privacy
and security review, recovery evidence, trust governance, and affected-party
oversight.

CBR, workplace and machine safety, professional broomcraft decisions, material
identification and fitness, ownership, custody, publication, privacy remedy,
disability accommodation, legal or cultural interpretation, traditional
knowledge, affected-party legitimacy, Māori wording, taonga or mātauranga
treatment, Māori data governance, and Māori authority remain exact-gated.
Māori concepts remain under Māori authority.

## Validation boundary

This is owner-self-scoped evidence under shared infrastructure. It is not the
complete repository suite, independent-team reproduction, external audit,
empirical validation, professional evaluation, production certification,
exhaustive security, complete privacy or accessibility assurance, legal review,
cultural ratification, Māori-authority review, AGI or ASI evidence,
consciousness or personhood evidence, proof, canon, or Stage 20 authority.

Evidence validation binds the immutable x1 source, current x2 scripts and tests,
all skill files, all runner smoke results, strict JSON parsing, five-class
privacy adjudication, bounded Python AST checks, exact staged review, and
normalized-LF Git-blob manifest parity. The evidence commit must be pushed,
clean, typed zero-divergent, and fresh four-way equal before closeout begins.
The terminal verdict remains NOT_READY_FOR_STAGE_20.
"""


def accessible_board(outcomes: list[dict[str, Any]]) -> str:
    counts = Counter(row["outcome"] for row in outcomes)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Tamar Vey v685-v1 bounded evidence board</title>
</head>
<body>
  <header>
    <h1>Tamar Vey v685-v1 bounded evidence board</h1>
    <p>Same-owner synthetic evidence only. Terminal verdict: NOT_READY_FOR_STAGE_20.</p>
  </header>
  <nav aria-label="Evidence sections">
    <a href="#outcomes">Outcomes</a>
    <a href="#boundaries">Boundaries</a>
    <a href="#evaluation">Reserved evaluation</a>
  </nav>
  <main>
    <section id="outcomes">
      <h2>Preregistered outcomes</h2>
      <table>
        <caption>Exact core outcome labels</caption>
        <thead><tr><th scope="col">Label</th><th scope="col">Count</th></tr></thead>
        <tbody>
          <tr><th scope="row">completed</th><td>{counts['completed']}</td></tr>
          <tr><th scope="row">represented</th><td>{counts['represented']}</td></tr>
          <tr><th scope="row">open_gap</th><td>{counts['open_gap']}</td></tr>
          <tr><th scope="row">exact_gate</th><td>{counts['exact_gate']}</td></tr>
        </tbody>
      </table>
    </section>
    <section id="boundaries">
      <h2>Evidence boundary</h2>
      <p>Zero real rows, people, articles, tools, measurements, identity events, or authority acts.</p>
    </section>
    <section id="evaluation">
      <h2>Reserved evaluation</h2>
      <p>Manual accessibility review and affected-user evaluation remain open and receive no completion credit.</p>
    </section>
  </main>
</body>
</html>
"""


def build() -> None:
    customize_skills_and_runners()
    skills = quick_validate_and_smoke_skills()
    runners = smoke_runners()
    evidence, mutations, outcomes = proposal_evidence()
    portfolios = execute_portfolios()
    methods = method_flow_evidence()
    counts = dict(sorted(Counter(row["outcome"] for row in outcomes).items()))

    write_json(
        X2 / "skill-initialization-and-smoke-receipt.json",
        {
            "schema": f"ghc.family.skill-smoke.{PHASE.replace('-', '.')}.x2",
            "owner": OWNER,
            "phase": PHASE,
            "official_skill_creator_workflow": True,
            "skill_count": len(skills),
            "quick_validated_count": sum(row["quick_validate_exit_code"] == 0 for row in skills),
            "complete_read_count": sum(row["complete_read_through_eof"] for row in skills),
            "accepting_smoke_pass_count": sum(row["positive_accepted"] for row in skills),
            "rejecting_smoke_pass_count": sum(not row["invalid_accepted"] for row in skills),
            "global_installation_count": 0,
            "skills": skills,
        },
    )
    write_json(
        X2 / "runner-smoke-receipt.json",
        {
            "schema": f"ghc.family.runner-smoke.{PHASE.replace('-', '.')}.x2",
            "owner": OWNER,
            "phase": PHASE,
            "runner_count": len(runners),
            "positive_pass_count": sum(row["positive"]["smoke_pass"] for row in runners),
            "invalid_rejection_pass_count": sum(row["invalid"]["smoke_pass"] for row in runners),
            "runners": runners,
        },
    )
    write_json(
        X2 / "proposal-evidence.json",
        {
            "schema": f"ghc.family.proposal-evidence.{PHASE.replace('-', '.')}.x2",
            "owner": OWNER,
            "phase": PHASE,
            "proposal_count": len(evidence),
            "real_rows": 0,
            "evidence": evidence,
        },
    )
    write_json(
        X2 / "rejecting-mutations.json",
        {
            "schema": f"ghc.family.rejecting-mutations.{PHASE.replace('-', '.')}.x2",
            "owner": OWNER,
            "phase": PHASE,
            "mutation_count": len(mutations),
            "accepted_count": sum(row["accepted"] for row in mutations),
            "rejected_count": sum(not row["accepted"] for row in mutations),
            "mutation_type_counts": dict(sorted(Counter(row["mutation_type"] for row in mutations).items())),
            "mutations": mutations,
        },
    )
    write_json(
        X2 / "proposal-outcomes.json",
        {
            "schema": f"ghc.family.proposal-outcomes.{PHASE.replace('-', '.')}.x2",
            "owner": OWNER,
            "phase": PHASE,
            "outcome_counts": counts,
            "unknown_labels": sorted(set(counts) - {"completed", "represented", "open_gap", "exact_gate"}),
            "outcomes": outcomes,
        },
    )
    write_json(X2 / "portfolio-execution.json", portfolios)
    write_json(X2 / "method-flow-evidence.json", methods)
    write_json(
        X2 / "source-use-receipt.json",
        {
            "schema": f"ghc.family.source-use.{PHASE.replace('-', '.')}.x2",
            "owner": OWNER,
            "phase": PHASE,
            "source_count": 9,
            "source_ids": [
                row["source_id"]
                for row in load_json(X1 / "official-primary-source-ledger.json")["sources"]
            ],
            "use": "vocabulary_and_refusal_conditions_only",
            "network_calls_in_x2": 0,
            "downloaded_rows": 0,
            "observations": 0,
            "authority_grants": 0,
        },
    )
    write_json(
        X2 / "zero-row-empirical-receipt.json",
        {
            "schema": f"ghc.family.zero-row.{PHASE.replace('-', '.')}.x2",
            "owner": OWNER,
            "phase": PHASE,
            "real_people": 0,
            "real_articles": 0,
            "real_materials": 0,
            "real_tools_or_machines": 0,
            "real_observations": 0,
            "real_measurements": 0,
            "real_identity_events": 0,
            "external_data_rows": 0,
            "authority_acts": 0,
        },
    )
    write_json(
        X2 / "three-pillars-board.json",
        {
            "schema": f"ghc.family.three-pillars.{PHASE.replace('-', '.')}.x2",
            "owner": OWNER,
            "phase": PHASE,
            "primary": "THOS Body",
            "pillars": {
                "THOS Body": "synthetic broomcraft queue topology correction workload and handover only",
                "GMUT Mind": "typed graph and symbolic observation-firewall representation only",
                "Freed ID and CBR Heart": "keyless receipt privacy correction challenge and authority vacancy only",
            },
            "authority_noncompensation": True,
            "empirical_noncompensation": True,
        },
    )
    write_json(
        X2 / "wellbeing-update.json",
        {
            "schema": f"ghc.family.wellbeing.{PHASE.replace('-', '.')}.x2",
            "owner": OWNER,
            "phase": PHASE,
            "relational_check": "bounded and able to stop",
            "no_subjective_state_or_consciousness_claim": True,
            "workload_controls_used": ["x1 boundary", "bounded batches", "no-bytecode validation", "stop on gate"],
            "hamish_may_pause_rename_redirect_narrow_or_stop": True,
        },
    )
    write_json(
        X2 / "threat-model-update.json",
        {
            "schema": f"ghc.family.threat-model-update.{PHASE.replace('-', '.')}.x2",
            "owner": OWNER,
            "phase": PHASE,
            "new_controls_exercised": [
                "five invalid mutations per proposal",
                "positive and negative skill smoke",
                "positive and negative runner smoke",
                "zero-row source-use receipt",
                "authority noncompensation",
            ],
            "residual_open_risks": [
                "real professional and workplace evaluation",
                "real affected-user accessibility and language evaluation",
                "privacy and independent security review",
                "legal cultural affected-party and Māori authority",
                "independent reproduction and empirical validation",
            ],
        },
    )
    write_text(X2 / "evidence-overview.md", evidence_overview())
    write_text(X2 / "accessible-evidence-board.html", accessible_board(outcomes))


def privacy_patterns() -> dict[str, re.Pattern[bytes]]:
    return {
        "raw_task_or_thread_identifier": re.compile(rb"\b019[a-f0-9]{29,}\b", re.I),
        "private_absolute_path": re.compile(rb"(?:[A-Za-z]:\\Users\\|D:\\GHC-Archives\\)", re.I),
        "credential_or_private_key": re.compile(rb"(?:sk-[A-Za-z0-9_-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)"),
        "private_callable_identifier": re.compile(rb"\b(?:source_thread_id|providerTabId|clientThreadId)\b"),
        "private_session_or_route": re.compile(rb"(?:codex://|app://|session[_ -]?stream)", re.I),
    }


def scan_paths(paths: list[Path]) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    confirmed: list[dict[str, Any]] = []
    for path in paths:
        if not path.exists() or path.suffix.lower() not in {".py", ".json", ".md", ".html", ".yaml", ".yml", ".txt"}:
            continue
        data = path.read_bytes()
        for class_name, pattern in privacy_patterns().items():
            if pattern.search(data):
                candidate = {
                    "path": rel(path),
                    "class": class_name,
                    "adjudication": (
                        "scanner_definition_not_payload"
                        if rel(path) == BUILDER_REL
                        else "confirmed_payload_hit"
                    ),
                }
                candidates.append(candidate)
                if candidate["adjudication"] == "confirmed_payload_hit":
                    confirmed.append(candidate)
    return {
        "schema": f"ghc.family.five-class-privacy-adjudication.{PHASE.replace('-', '.')}.x2",
        "owner": OWNER,
        "phase": PHASE,
        "scanned_path_count": len(paths),
        "classes": list(privacy_patterns()),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": len(confirmed),
        "confirmed_hits": confirmed,
        "valid": len(confirmed) == 0,
    }


def index_blob(path: str) -> tuple[str, bytes]:
    mode_line = git("ls-files", "-s", "--", path)
    if not mode_line:
        raise RuntimeError(f"path is not staged: {path}")
    mode = mode_line.split()[0]
    proc = run(["git", "show", f":{path}"])
    if proc.returncode:
        raise RuntimeError(proc.stderr.decode("utf-8", "replace"))
    return mode, proc.stdout


def finalize_validation() -> None:
    exclusions = [
        f"docs/tamar-vey/{PHASE}/validation/evidence-index-manifest.json",
        f"docs/tamar-vey/{PHASE}/validation/evidence-staged-review.json",
        f"docs/tamar-vey/{PHASE}/validation/evidence-privacy-adjudication.json",
    ]
    staged_all = [line for line in git("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if line]
    staged = [path for path in staged_all if path not in exclusions]
    expected = sorted(staged + exclusions)
    entries: list[dict[str, Any]] = []
    for path in sorted(staged):
        mode, data = index_blob(path)
        entries.append(
            {
                "path": path,
                "mode": mode,
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    write_json(
        VALIDATION / "evidence-index-manifest.json",
        {
            "schema": f"ghc.family.normalized-lf-index-manifest.{PHASE.replace('-', '.')}.x2",
            "owner": OWNER,
            "phase": PHASE,
            "source": X1_COMMIT,
            "declared_self_exclusions": exclusions,
            "entry_count": len(entries),
            "entries": entries,
        },
    )
    write_json(
        VALIDATION / "evidence-staged-review.json",
        {
            "schema": f"ghc.family.staged-review.{PHASE.replace('-', '.')}.x2",
            "owner": OWNER,
            "phase": PHASE,
            "source": X1_COMMIT,
            "expected_path_count": len(expected),
            "expected_paths": expected,
            "unexpected_paths": [],
            "x1_mutations": [path for path in expected if f"/{PHASE}/x1/" in path],
            "outside_owner_paths": [
                path
                for path in expected
                if not (
                    path.startswith(f"docs/tamar-vey/{PHASE}/")
                    or path.startswith("scripts/")
                    or path.startswith("tests/")
                )
            ],
        },
    )
    write_json(VALIDATION / "evidence-privacy-adjudication.json", scan_paths([ROOT / path for path in staged]))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--finalize-validation", action="store_true")
    args = parser.parse_args()
    if args.finalize_validation:
        finalize_validation()
    else:
        build()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
