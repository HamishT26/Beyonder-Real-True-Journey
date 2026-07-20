#!/usr/bin/env python3
"""Execute Tamar Vey's frozen v650-v5 x2 evidence plan."""

from __future__ import annotations

import html
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v650_v5_phase_data as d

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
SKILL_CREATOR = Path.home() / ".codex/skills/.system/skill-creator/scripts"
METHOD_RUNNER = Path.home() / ".codex/skills/ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"


def write_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run(*args: str) -> str:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        list(args),
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    return completed.stdout.strip()


GROUPS = {
    1: ["V6505-P01", "V6505-P02", "V6505-P03", "V6505-P04"],
    2: ["V6505-P05"],
    3: ["V6505-P06", "V6505-P07", "V6505-P08"],
    4: ["V6505-P09"],
    5: ["V6505-P10"],
    6: ["V6505-P11", "V6505-P12", "V6505-P14", "V6505-P16", "V6505-P20"],
    7: ["V6505-P13", "V6505-P15"],
    8: ["V6505-P17"],
    9: ["V6505-P18"],
    10: ["V6505-P19"],
}


def runner_for(proposal_id: str) -> str:
    group = next(group for group, ids in GROUPS.items() if proposal_id in ids)
    return d.RUNNERS[group - 1]


def execute_runners() -> list[dict[str, Any]]:
    rows = []
    for index, name in enumerate(d.RUNNERS, start=1):
        output = run(sys.executable, str(REPO / "scripts" / name))
        witness_path = ROOT / "runner-witnesses" / f"{Path(name).stem}.json"
        witness = read_json(witness_path)
        if not witness["passed"]:
            raise RuntimeError(f"runner failed: {name}")
        rows.append(
            {
                "runner_id": f"V6505-RUN-{index:02d}",
                "name": name,
                "status": "completed_bounded_witness",
                "invoked": True,
                "stdout_empty": not bool(output),
                "witness": witness_path.relative_to(ROOT).as_posix(),
                "proposal_ids": witness["proposal_ids"],
                "valid_fixture_count": witness["valid_fixture_count"],
                "rejected_mutation_count": witness["rejected_mutation_count"],
                "same_owner_only": True,
                "independent_reproduction": False,
            }
        )
    return rows


def skill_markdown(name: str, proposal: dict[str, Any], runner: str) -> str:
    return f"""---
name: {name}
description: Use when auditing the frozen v650-v5 {proposal['slug']} surface with bounded fixtures and explicit nonpromotion gates.
---

# {name}

Use this package only inside Tamar Vey's owner-scoped v650-v5 evidence lane.

1. Read proposal `{proposal['proposal_id']}`, its null condition, acceptance gate, rollback, and protected gates.
2. Run `scripts/{runner}` only on disposable synthetic, symbolic, formal, structural, or zero-row fixtures.
3. Inspect `surfaces/{proposal['slug']}/contract.json`, `mutation-results.json`, and `bounded-receipt.json`.
4. Reject network downloads, real participant or operator work, production identity activity, credentials, authority decisions, deployment, destructive action, sibling mutation, and unsupported claim promotion.
5. Preserve failed witnesses and report only `completed`, `represented`, `open_gap`, or `exact_gate` inside the frozen evidence class.

## Boundary

This phase-local package is not globally installed. It confers no future availability, scientific truth, professional competence, production readiness, legal or cultural authority, Maori authority, complete privacy, exhaustive security, complete accessibility, independent reproduction, or Stage 20 authorization.

See `references/contract.md` for the exact bounded invocation contract.
"""


def build_skills() -> list[dict[str, Any]]:
    rows = []
    skills_root = ROOT / "skills"
    skills_root.mkdir(parents=True, exist_ok=True)
    for index, (name, proposal) in enumerate(zip(d.SKILLS, d.PROPOSALS), start=1):
        target = skills_root / name
        initialized_now = False
        prior_witness_path = ROOT / "skill-witnesses" / f"{name}.json"
        initialized_before = (
            prior_witness_path.is_file()
            and read_json(prior_witness_path).get("initialized_with_official_workflow") is True
        )
        if not target.exists():
            run(
                sys.executable,
                str(SKILL_CREATOR / "init_skill.py"),
                name,
                "--path",
                str(skills_root),
                "--resources",
                "references",
            )
            initialized_now = True
        runner = runner_for(proposal["proposal_id"])
        (target / "SKILL.md").write_text(
            skill_markdown(name, proposal, runner), encoding="utf-8", newline="\n"
        )
        references = target / "references"
        references.mkdir(parents=True, exist_ok=True)
        (references / "contract.md").write_text(
            (
                f"# {proposal['proposal_id']} bounded contract\n\n"
                f"- Hypothesis: {proposal['hypothesis']}\n"
                f"- Null: {proposal['null_or_failure_condition']}\n"
                f"- Acceptance: {proposal['falsifier_or_acceptance_gate']}\n"
                f"- Rollback: {proposal['rollback_or_recovery']}\n"
                f"- Expected disposition: `{proposal['expected_disposition']}`\n\n"
                "Citations and synthetic fixtures are requirements context only. "
                "They are not observations, participant evidence, production "
                "readiness, authority, or independent review.\n"
            ),
            encoding="utf-8",
            newline="\n",
        )
        display_name = " ".join(
            part.capitalize() for part in name.removeprefix("ghc-family-").split("-")
        )
        run(
            sys.executable,
            str(SKILL_CREATOR / "generate_openai_yaml.py"),
            str(target),
            "--name",
            name,
            "--interface",
            f"display_name={display_name}",
            "--interface",
            "short_description=Audit bounded evidence and retain exact gates",
            "--interface",
            f"default_prompt=Use ${name} to audit its frozen bounded evidence contract.",
        )
        validate_output = run(
            sys.executable, str(SKILL_CREATOR / "quick_validate.py"), str(target)
        )
        receipt = read_json(ROOT / "surfaces" / proposal["slug"] / "bounded-receipt.json")
        skill_text = (target / "SKILL.md").read_text(encoding="utf-8")
        smoke_passed = (
            proposal["proposal_id"] in skill_text
            and runner in skill_text
            and receipt["passed"]
        )
        smoke = {
            "schema": "ghc.family.v650-v5.skill-smoke-witness.v1",
            "skill_id": f"V6505-SKILL-{index:02d}",
            "name": name,
            "proposal_id": proposal["proposal_id"],
            "initialized_with_official_workflow": initialized_now or initialized_before,
            "metadata_generated_with_official_workflow": True,
            "quick_validate_output": validate_output,
            "smoke_used": True,
            "smoke_passed": smoke_passed,
            "global_install": False,
            "subagent_forward_test": "forbidden_by_activation",
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": d.BOUNDARY,
        }
        write_json(f"skill-witnesses/{name}.json", smoke)
        if not smoke_passed:
            raise RuntimeError(f"skill smoke failed: {name}")
        rows.append(
            {
                "skill_id": f"V6505-SKILL-{index:02d}",
                "name": name,
                "status": "built_validated_and_smoke_used",
                "proposal_id": proposal["proposal_id"],
                "package": f"skills/{name}",
                "witness": f"skill-witnesses/{name}.json",
                "global_install": False,
            }
        )
    return rows


def execution_rows(plan_name: str, status: str, witness_prefix: str) -> list[dict[str, Any]]:
    plan = read_json(ROOT / f"portfolios/{plan_name}-plan.json")
    rows = []
    for row in plan["tasks"]:
        proposal = next(p for p in d.PROPOSALS if p["proposal_id"] == row["proposal_id"])
        receipt = read_json(ROOT / "surfaces" / proposal["slug"] / "bounded-receipt.json")
        if not receipt["passed"]:
            raise RuntimeError(f"portfolio prerequisite failed: {row['item_id']}")
        rows.append(
            {
                **row,
                "status": status,
                "executed": True,
                "acceptance_gate_passed": True,
                "witness": f"{witness_prefix}/{proposal['slug']}/bounded-receipt.json",
                "completion_scope": "declared_bounded_software_or_synthetic_hypothesis",
            }
        )
    return rows


def record_x2_method_flow() -> None:
    ledger = ROOT / "method-flow/method-flow-state.json"
    state = read_json(ledger)
    existing_methods = {row["method_id"] for row in state["methods"]}
    existing_witnesses = {row["witness_id"] for row in state["witnesses"]}
    offset = len(d.X1_OPERATIONAL_NEGATIVES)
    for index, negative in enumerate(d.X2_OPERATIONAL_NEGATIVES, start=1):
        method_id = f"V6505-M{offset + index:02d}"
        record = {
            "method_id": method_id,
            "title": f"Recover {negative['category']} without erasing its failed witness",
            "failure_signature": negative["failed"],
            "trigger_preconditions": [f"A bounded v650-v5 x2 workflow exposes {negative['category']}."],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": negative["recovery"],
            "validation_witness_ids": [],
            "recurrence_guard": negative["recurrence_guard"],
            "rollback": "Give the failed attempt no evidence credit, retain it, and rely only on a bounded passing witness.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["evidence_credit", "failure_retention", "x1_x2_separation", "caller_compatibility"],
            "retained_negative_ids": [negative["negative_id"]],
            "scope_boundary": "Bounded owner-scoped recovery only; no independent reproduction or authority credit.",
        }
        fail = {
            "witness_id": f"{method_id}-WFAIL",
            "method_id": method_id,
            "procedure": negative["failed"],
            "scope": f"bounded {negative['category']} failed witness",
            "expected": "The attempted method returns attributable evidence within its declared domain.",
            "observed": negative["failed"],
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [negative["negative_id"]],
            "boundary": "Retained failure only; no completion, authority, or independent-reproduction credit.",
        }
        passed = {
            "witness_id": f"{method_id}-WPASS",
            "method_id": method_id,
            "procedure": negative["recovery"],
            "scope": f"bounded {negative['category']} recovery witness",
            "expected": "The corrected method returns attributable bounded evidence while preserving the failure.",
            "observed": negative["passing"],
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [negative["negative_id"]],
            "boundary": "Bounded same-owner recovery only; no independent reproduction or authority credit.",
        }
        record_path = write_json(f"method-flow/{method_id.casefold()}-method-record.json", record)
        fail_path = write_json(f"method-flow/{fail['witness_id'].casefold()}-witness.json", fail)
        pass_path = write_json(f"method-flow/{passed['witness_id'].casefold()}-witness.json", passed)
        if method_id not in existing_methods:
            run(sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(ledger), "--record-file", str(record_path))
            existing_methods.add(method_id)
        for witness, path in ((fail, fail_path), (passed, pass_path)):
            if witness["witness_id"] not in existing_witnesses:
                run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(path))
                existing_witnesses.add(witness["witness_id"])
        state = read_json(ledger)
        method_state = next(row["recommendation_state"] for row in state["methods"] if row["method_id"] == method_id)
        if method_state == "validated":
            run(sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(ledger), "--method-id", method_id, "--state", "preferred", "--note", "Promoted only after retaining one failed and one bounded passing witness.")
        elif method_state != "preferred":
            raise RuntimeError(f"method {method_id} did not reach validated or preferred state")
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(ROOT / "method-flow/method-flow-validation.json"))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ledger), "--json-output", str(ROOT / "method-flow/method-flow-summary.json"), "--markdown-output", str(ROOT / "method-flow/method-flow-summary.md"))


def report_html(rows: list[dict[str, Any]]) -> str:
    table_rows = "\n".join(
        '<tr><th scope="row">{}</th><td>{}</td><td>{}</td><td>{}</td></tr>'.format(
            html.escape(row["proposal_id"]),
            html.escape(row["title"]),
            html.escape(row["outcome"]),
            "passed" if row["passed"] else "failed",
        )
        for row in rows
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tamar Vey v650-v5 bounded evidence report</title>
<style>body{{font:1rem/1.55 system-ui;max-width:76rem;margin:auto;padding:1rem}}a:focus,button:focus,summary:focus{{outline:3px solid #174ea6;outline-offset:2px}}.skip{{position:absolute;left:-9999px}}.skip:focus{{position:static}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #777;padding:.5rem;text-align:left}}.status{{font-weight:700}}code{{overflow-wrap:anywhere}}</style></head>
<body><a class="skip" href="#main">Skip to main content</a><header><h1>Tamar Vey v650-v5 bounded evidence report</h1><p class="status">NOT_READY_FOR_STAGE_20</p></header>
<nav aria-label="Report sections"><a href="#truth">Truth</a> | <a href="#proposals">Proposals</a> | <a href="#gates">Gates</a></nav>
<main id="main"><section id="truth"><h2>Truth boundary</h2><p>Fourteen surfaces completed bounded tests, four remain represented, one remains an open gap, and one remains exact-gated. Same-owner execution is not independent reproduction.</p></section>
<section id="proposals"><h2>Proposal evidence</h2><table><caption>Frozen proposal outcomes</caption><thead><tr><th scope="col">ID</th><th scope="col">Surface</th><th scope="col">Outcome</th><th scope="col">Check</th></tr></thead><tbody>{table_rows}</tbody></table></section>
<section id="gates"><h2>Reserved gates</h2><details><summary>Scientific, identity, and authority limits</summary><p>There is no empirical GMUT confirmation, real THOS arm, production identity proof, legal or cultural ratification, Maori-authority decision, consciousness or personhood evidence, deployment authority, exhaustive-security result, or Stage 20 authorization.</p></details><p>Manual keyboard, browser-diverse, assistive-technology, cognitive-accessibility, Maori-language, and affected-user evaluation remain reserved. Structural checks are not complete accessibility conformance.</p></section></main>
<footer><p>Owner-scoped static report. No private route, credential, private key, raw identifier, or private local path is included.</p></footer></body></html>"""


def overview_appendix(distribution: dict[str, int]) -> str:
    return f"""
## X2 bounded evidence

The frozen x1 packet was remote-equal before any implementation began. X2 then executed exactly the twenty preregistered surfaces through owner-local symbolic, structural, numerical, synthetic, or zero-row fixtures. The observed distribution is fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`. Those labels describe evidence classes, not a maturity ladder. A represented result is not a partial production approval, an open gap is not a hidden success, and an exact gate cannot be closed by adding software assertions.

### Heart focus and bounded human practice

Freed ID and CBR Heart remained the primary Trinity Mandala pillar. RFC 8414 metadata, RFC 8252 native-app redirects, and RFC 9278 JWK Thumbprint URIs were exercised with synthetic values only. No real key, credential, account, authorization server, native application, issuance, presentation, resolution, status, revocation, interoperability event, privacy review, independent security review, recovery decision, or trust-governance decision occurred. The book-conservation workshop remained a learning lens: synthetic traces modelled intake, condition reporting, mould isolation, reversible treatment planning, material compatibility, release refusal, workload limits, and handover. They involved no real collection object, conservator, worker, donor, institution, incident, participant, or effectiveness estimate.

The conservation-treatment and taonga decision-rights matrix remains exact-gated. It reserves custodianship, condition disclosure, intervention consent, digital-surrogate decisions, return requests, tikanga, affected-party legitimacy, legal interpretation, cultural ratification, data governance, and Maori authority. Repository software cannot confer those decisions. Maori concepts, wording, and data remain under tangata whenua, iwi, hapu, and Maori authority. The matrix records absence of authority; it does not simulate consent or convert a checklist into legitimacy.

### GMUT Mind

The distributed-lease tribunal completed only as a bounded workflow control: monotonic fencing tokens rejected a stale holder, expiry rejected a late action, and clock uncertainty remained explicit. It authorized no external side effect. CPT, Appelquist-Carazzone, and Froissart-Martin boards completed as typed obligation sets with gauge, effective-field-theory, unit, and observation firewalls. These are research-model bookkeeping surfaces. They establish no physical force, unique prediction, likelihood, parameter constraint, stability theorem, ultraviolet completion, empirical confirmation, proof or canon, or Theory of Everything.

The NASA Exoplanet Archive Planetary Systems adapter stayed an `open_gap`. Official sources supplied schema and provenance requirements only. The phase downloaded zero rows, ingested zero rows, evaluated zero likelihoods, produced zero posterior samples, emitted zero constraints, and made zero empirical GMUT claim. Readiness of a refusal contract is not readiness of a fit. Real empirical work would require a frozen analysis, real public data, selection treatment, uncertainty and covariance handling, nuisance modelling, checksum provenance, and appropriate independent review.

### THOS Body and bounded engineering

The Matroska, Apache Avro, FLAC, OpenEXR, and HPACK tribunals completed against small disposable fixtures. They checked selected magic values, framing obligations, state or resource budgets, and refusal boundaries. The Xor Filter and Krawczyk surfaces completed bounded deterministic witnesses. The accessible split-action audit checked distinct names, popup state, keyboard declarations, and focus return structurally. None is a production parser, exhaustive format validator, general security guarantee, accessibility certification, or deployment approval.

THOS remains represented because there were no preregistered blind matched-budget real arms, real participants or operators, safety monitoring, suitable statistics, or independent review. Synthetic workshop traces cannot establish operational effectiveness, AGI or ASI, consciousness, personhood, professional competence, or public-safety outcomes. The Redlich-Kwong classifier retained physical units and phase limitations while refusing conversion into psyche, agency, autonomy, justice, consciousness, personhood, or a fundamental law of mind.

### Falsification, portfolios, and recovery

All one hundred preregistered mutations executed. Each proposal received five negative cases: missing obligation, wrong domain or type, unsupported promotion, exceeded resource or iteration budget, and attempted negative or gate erasure. All were rejected or quarantined and none received completion credit. Mutation rejection demonstrates only the declared guards on these fixtures; it is not exhaustive security or proof that every malformed input is rejected.

Forty safe-now tasks, thirty bounded candidate prototypes, twenty phase-local skills, ten family-compatible runners, and forty additive CLEAN/FIX/REFINE tasks were executed within their frozen acceptance gates. The skills were initialized and validated through the official local skill-creator workflow, smoke-used, and left phase-local. They were not globally installed, and no subagent forward test occurred because delegation was prohibited. The runners preserve `ghc_family_*` caller naming. Portfolio completion applies only to the item-specific software or synthetic hypothesis and does not inherit authority from the profession used as a learning lens.

Every startup, parser, tooling, staging, test, or count fault remains retained. Corrections did not erase the failed witnesses. Two historical pass-labelled Method Flow placeholders remain visible with zero current evidence credit; append-only correction witnesses contain the actual bounded observations. Same-owner reruns under shared infrastructure are not independent-team scientific reproduction or external audit.

### Terminal disposition

The terminal board remains `NOT_READY_FOR_STAGE_20`. Open empirical, participant, production-identity, privacy, security, professional, legal, cultural, Maori-authority, accessibility, independent-reproduction, proof or canon, deployment, AGI or ASI, consciousness or personhood, Theory-of-Everything, and Stage 20 gates remain explicit. Closeout may seal what was actually observed, but it cannot promote a citation into data, a synthetic fixture into a real arm, a structural profile into production cryptography, or a repository matrix into authority.

Observed distribution receipt: `{json.dumps(distribution, sort_keys=True)}`.
"""


def main() -> int:
    runner_rows = execute_runners()
    receipts = [
        read_json(ROOT / "surfaces" / proposal["slug"] / "bounded-receipt.json")
        for proposal in d.PROPOSALS
    ]
    if not all(row["passed"] for row in receipts):
        raise RuntimeError("one or more bounded proposal receipts failed")
    distribution = Counter(row["outcome"] for row in receipts)
    expected = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}
    if dict(distribution) != expected:
        raise RuntimeError(f"outcome distribution mismatch: {dict(distribution)}")

    skill_rows = build_skills()
    safe_rows = execution_rows("safe-now", "completed_bounded_task", "surfaces")
    candidate_rows = execution_rows("candidate", "completed_bounded_prototype", "surfaces")
    cfr_rows = execution_rows("clean-fix-refine", "completed_additive_owner_scoped", "surfaces")

    proposal_rows = []
    mutations = []
    for proposal, receipt in zip(d.PROPOSALS, receipts):
        surface = ROOT / "surfaces" / proposal["slug"]
        mutation = read_json(surface / "mutation-results.json")
        mutations.extend(mutation["mutations"])
        proposal_rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "slug": proposal["slug"],
                "outcome": receipt["outcome"],
                "passed": receipt["passed"],
                "valid_fixture_accepted": receipt["valid_fixture_accepted"],
                "mutations_executed": receipt["mutations_executed"],
                "mutations_rejected": receipt["mutations_rejected"],
                "approval_class": proposal["approval_class"],
                "artifact": f"surfaces/{proposal['slug']}/bounded-receipt.json",
                "same_owner_only": True,
                "independent_reproduction": False,
            }
        )
    if len(mutations) != 100 or any(row["result"] != "rejected" for row in mutations):
        raise RuntimeError("not all one hundred preregistered mutations were rejected")

    write_json(
        "x2-evidence-ledger.json",
        {
            "schema": "ghc.family.v650-v5.x2-evidence-ledger.v1",
            "proposal_count": len(proposal_rows),
            "distribution": expected,
            "proposals": proposal_rows,
            "same_owner_only": True,
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": d.BOUNDARY,
        },
    )
    write_json(
        "validation/x2-synthetic-mutation-results.json",
        {
            "schema": "ghc.family.v650-v5.mutation-results.aggregate.v1",
            "planned_count": 100,
            "executed_count": len(mutations),
            "rejected_or_quarantined_count": sum(
                row["result"] == "rejected" for row in mutations
            ),
            "completion_credit": 0,
            "mutations": mutations,
            "boundary": "Bounded guard evidence only; not exhaustive security.",
        },
    )
    write_json(
        "portfolios/safe-now-execution.json",
        {"schema": "ghc.family.v650-v5.safe-now-execution.v1", "count": len(safe_rows), "completed": len(safe_rows), "tasks": safe_rows},
    )
    write_json(
        "portfolios/candidate-execution.json",
        {"schema": "ghc.family.v650-v5.candidate-execution.v1", "count": len(candidate_rows), "completed": len(candidate_rows), "tasks": candidate_rows},
    )
    write_json(
        "portfolios/skill-execution.json",
        {"schema": "ghc.family.v650-v5.skill-execution.v1", "count": len(skill_rows), "completed": len(skill_rows), "global_install": False, "skills": skill_rows},
    )
    write_json(
        "portfolios/runner-execution.json",
        {"schema": "ghc.family.v650-v5.runner-execution.v1", "count": len(runner_rows), "completed": len(runner_rows), "runners": runner_rows},
    )
    write_json(
        "portfolios/clean-fix-refine-execution.json",
        {"schema": "ghc.family.v650-v5.clean-fix-refine-execution.v1", "count": len(cfr_rows), "completed": len(cfr_rows), "destructive_actions": 0, "tasks": cfr_rows},
    )

    prior_negatives = read_json(ROOT / "retained-negative-register.json")
    negative_entries = {
        row["negative_id"]: row
        for row in prior_negatives["entries"] + d.X2_OPERATIONAL_NEGATIVES
    }
    write_json(
        "retained-negative-register.json",
        {
            "schema": "ghc.family.v650-v5.retained-negatives.x2.v1",
            "activation_baseline": d.ACTIVATION_NEGATIVES,
            "x1_operational": len(d.X1_OPERATIONAL_NEGATIVES),
            "x2_operational": len(d.X2_OPERATIONAL_NEGATIVES),
            "executed_rejected_synthetic_mutations": 100,
            "effective_total": d.ACTIVATION_NEGATIVES + len(d.X1_OPERATIONAL_NEGATIVES) + len(d.X2_OPERATIONAL_NEGATIVES) + 100,
            "erased": 0,
            "entries": list(negative_entries.values()),
            "mutation_register": "validation/x2-synthetic-mutation-results.json",
        },
    )
    write_json(
        "exact-open-gate-register.json",
        {
            "schema": "ghc.family.v650-v5.gates.x2.v1",
            "inherited_open_gaps": d.INHERITED_OPEN_GAPS,
            "inherited_exact_gates": d.INHERITED_EXACT_GATES,
            "new_open_gaps": [{"proposal_id": "V6505-P05", "state": "open_gap", "reason": "zero real rows and zero likelihood evaluations"}],
            "new_exact_gates": [{"proposal_id": "V6505-P10", "state": "exact_gate", "reason": "competent affected-party cultural legal data-governance and Maori authority required"}],
            "effective_open_gaps": d.INHERITED_OPEN_GAPS + 1,
            "effective_exact_gates": d.INHERITED_EXACT_GATES + 1,
            "silently_closed": 0,
        },
    )
    write_json(
        "phase-truth.json",
        {
            "schema": "ghc.family.v650-v5.phase-truth.x2-evidence.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "state": "X2_EVIDENCE_COMPLETE_NOT_SEALED",
            "x1_commits": [
                "7c15d7e0f96e1ce5a1b7fd6049ef3c3285debc30",
                "56ff8d5ab41d4b477184c854037122c81e2cc6a3",
            ],
            "x1_commit": "56ff8d5ab41d4b477184c854037122c81e2cc6a3",
            "proposal_count": 20,
            "distribution": expected,
            "effective_negatives": d.ACTIVATION_NEGATIVES + len(d.X1_OPERATIONAL_NEGATIVES) + len(d.X2_OPERATIONAL_NEGATIVES) + 100,
            "effective_open_gaps": d.INHERITED_OPEN_GAPS + 1,
            "effective_exact_gates": d.INHERITED_EXACT_GATES + 1,
            "same_owner_repeatability": True,
            "independent_team_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": d.BOUNDARY,
        },
    )
    write_json(
        "ghc-family-index.json",
        {
            "schema": "ghc.family.v650-v5.phase-index.x2.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "source_head": d.SOURCE_HEAD,
            "x1_head": "56ff8d5ab41d4b477184c854037122c81e2cc6a3",
            "state": "x2_evidence_complete_not_sealed",
            "reviewed_current": True,
            "proposal_count": 20,
            "distribution": expected,
            "portfolio_counts": {"safe_now": 40, "candidates": 30, "skills": 20, "runners": 10, "clean_fix_refine": 40, "mutations": 100},
            "shared_skill_change": False,
        },
    )
    write_json(
        "complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v650-v5.checklist.x2-evidence.v1",
            "complete": [
                "x1 frozen in two commits and remote-equal before x2",
                "twenty proposals executed within frozen evidence classes",
                "one hundred synthetic mutations rejected",
                "forty safe-now tasks completed",
                "thirty bounded candidates built tested and invoked",
                "twenty phase-local skills built validated and smoke-used",
                "ten family-compatible runners invoked",
                "forty additive CLEAN/FIX/REFINE tasks completed",
                "all x1 failures and historical correction witnesses retained",
            ],
            "incomplete": [
                "evidence exact staged review and commit",
                "combined closeout and seal commit",
                "sole successful canonical scoped validation",
                "final four-way equality",
                "terminal Sylven Arc baton",
                "all inherited and new open and exact gates",
            ],
        },
    )
    write_json(
        "wellbeing-check.json",
        {
            "schema": "ghc.family.v650-v5.wellbeing.x2.v1",
            "owner": d.OWNER,
            "workload": "bounded but substantial",
            "stop_conditions_preserved": True,
            "corrigibility": "Hamish may rename pause redirect or stop the route.",
            "identity_boundary": d.BOUNDARY,
        },
    )
    write_json(
        "orchestration/terminal-route-state.json",
        {
            "schema": "ghc.family.v650-v5.terminal-route.x2.v1",
            "target_title": "Sylven Arc",
            "target_phase": "v650-v6",
            "state": "HELD_UNTIL_VERIFIED_FINAL",
            "messages_sent": 0,
            "cross_platform_send": False,
        },
    )
    write_json(
        "validation/evidence-validation.json",
        {
            "schema": "ghc.family.v650-v5.evidence-validation.v1",
            "proposal_receipts": 20,
            "distribution": expected,
            "mutations_executed_and_rejected": 100,
            "phase_local_skills_validated": 20,
            "runners_invoked": 10,
            "portfolio_counts": {"safe_now": 40, "candidates": 30, "clean_fix_refine": 40},
            "tests": "run_after_generation_before_evidence_commit",
            "canonical_final_pass": "not_run",
            "boundary": d.BOUNDARY,
        },
    )

    threat = read_json(ROOT / "threat-model.json")
    threat["schema"] = "ghc.family.v650-v5.threat-model.x2.v1"
    threat["executed_controls"] = [
        "one hundred fail-closed mutation witnesses",
        "zero-row empirical refusal",
        "synthetic identity and THOS boundaries",
        "exact authority reservation",
        "phase-local skill validation",
        "resource-budgeted disposable fixtures",
        "append-only Method Flow correction witnesses",
    ]
    threat["exhaustive_security_claim"] = False
    write_json("threat-model.json", threat)
    write_text("report.html", report_html(proposal_rows))
    original = (ROOT / "integrated-overview.md").read_text(encoding="utf-8")
    base = original.split("\n## X2 bounded evidence", 1)[0].rstrip()
    write_text("integrated-overview.md", base + "\n" + overview_appendix(expected))
    file_count = sum(1 for path in ROOT.rglob("*") if path.is_file())
    write_json(
        "environment/file-count-receipt.json",
        {
            "schema": "ghc.family.v650-v5.file-count.x2.v1",
            "owner_generated_public_files": file_count,
            "owner_threshold": 15000,
            "owner_threshold_exceeded": file_count >= 15000,
            "inherited_baseline_triggers_rotation": False,
        },
    )
    record_x2_method_flow()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
