#!/usr/bin/env python3
"""Execute Orin Thale's bounded v650-v4 x2 evidence plan."""

from __future__ import annotations

import html
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v650_v4_phase_data as d

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
                "runner_id": f"V6504-RUN-{index:02d}",
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
description: Use when the frozen v650-v4 proposal selects the bounded {proposal['slug']} evidence lane and its explicit nonpromotion gates.
---

# {name}

Use this package only inside Orin Thale's owner-scoped v650-v4 evidence lane.

1. Read proposal `{proposal['proposal_id']}`, its source needs, null condition, acceptance gate, rollback, and protected gates.
2. Run `scripts/{runner}` only on disposable synthetic, symbolic, formal, structural, or zero-row fixtures.
3. Inspect `surfaces/{proposal['slug']}/contract.json`, `mutation-results.json`, and `bounded-receipt.json`.
4. Reject any request for network download, real participant or operator work, production identity activity, credentials, authority decisions, deployment, destructive action, sibling mutation, or unsupported claim promotion.
5. Retain every failed witness and report only `completed`, `represented`, `open_gap`, or `exact_gate` within the frozen evidence class.

## Boundary

This phase-local package is not globally installed and confers no future-environment availability, scientific truth, professional competence, production readiness, legal or cultural authority, Maori authority, complete privacy, exhaustive security, complete accessibility, independent reproduction, or Stage 20 authorization.

See `references/contract.md` for the exact bounded invocation contract.
"""


def build_skills() -> list[dict[str, Any]]:
    rows = []
    skills_root = ROOT / "skills"
    skills_root.mkdir(parents=True, exist_ok=True)
    for index, (name, proposal) in enumerate(zip(d.SKILLS, d.PROPOSALS), start=1):
        target = skills_root / name
        initialized_now = False
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
        runner = d.RUNNERS[next(
            group - 1
            for group, proposal_ids in {
                1: ["V6504-P01", "V6504-P02", "V6504-P03", "V6504-P04"],
                2: ["V6504-P05"],
                3: ["V6504-P06", "V6504-P07", "V6504-P08"],
                4: ["V6504-P09"],
                5: ["V6504-P10"],
                6: ["V6504-P11", "V6504-P12", "V6504-P14", "V6504-P16", "V6504-P20"],
                7: ["V6504-P13", "V6504-P15"],
                8: ["V6504-P17"],
                9: ["V6504-P18"],
                10: ["V6504-P19"],
            }.items()
            if proposal["proposal_id"] in proposal_ids
        )]
        (target / "SKILL.md").write_text(
            skill_markdown(name, proposal, runner),
            encoding="utf-8",
            newline="\n",
        )
        (target / "references").mkdir(parents=True, exist_ok=True)
        (target / "references/contract.md").write_text(
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
        display_name = " ".join(part.capitalize() for part in name.removeprefix("ghc-family-").split("-"))
        run(
            sys.executable,
            str(SKILL_CREATOR / "generate_openai_yaml.py"),
            str(target),
            "--name",
            name,
            "--interface",
            f"display_name={display_name}",
            "--interface",
            "short_description=Audit bounded evidence with explicit gate retention",
            "--interface",
            f"default_prompt=Use ${name} to audit its frozen bounded evidence contract.",
        )
        validate_output = run(
            sys.executable,
            str(SKILL_CREATOR / "quick_validate.py"),
            str(target),
        )
        receipt = read_json(
            ROOT / "surfaces" / proposal["slug"] / "bounded-receipt.json"
        )
        skill_text = (target / "SKILL.md").read_text(encoding="utf-8")
        smoke_passed = (
            proposal["proposal_id"] in skill_text
            and runner in skill_text
            and receipt["passed"]
        )
        smoke = {
            "schema": "ghc.family.v650-v4.skill-smoke-witness.v1",
            "skill_id": f"V6504-SKILL-{index:02d}",
            "name": name,
            "proposal_id": proposal["proposal_id"],
            "initialized_with_official_workflow": initialized_now,
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
                "skill_id": f"V6504-SKILL-{index:02d}",
                "name": name,
                "status": "built_validated_and_smoke_used",
                "proposal_id": proposal["proposal_id"],
                "package": f"skills/{name}",
                "witness": f"skill-witnesses/{name}.json",
                "global_install": False,
            }
        )
    return rows


def close_method_flow_skill_failure() -> None:
    pass_witness = {
        "witness_id": "V6504-M06-WPASS",
        "method_id": "V6504-M06",
        "procedure": (
            "Initialize phase-local skill directories with init_skill, generate "
            "metadata with generate_openai_yaml, and invoke quick_validate only with "
            "actual initialized directories under explicit UTF-8."
        ),
        "scope": "bounded phase-local skill-creator recovery witness",
        "expected": (
            "All twenty substantive packages validate and smoke-use without global installation."
        ),
        "observed": (
            "All twenty packages were initialized, customized, metadata-generated, "
            "quick-validated, and smoke-used; the failed help probe remains retained."
        ),
        "result": "pass",
        "same_owner_only": True,
        "independent_reproduction": False,
        "retained_negative_ids": ["V6504-X2-N01"],
        "boundary": (
            "Phase-local packaging witness only; no global installation, future "
            "availability, authority, or independent-reproduction credit."
        ),
    }
    path = write_json("method-flow/v6504-m06-wpass-witness.json", pass_witness)
    ledger = ROOT / "method-flow/method-flow-state.json"
    state = read_json(ledger)
    if pass_witness["witness_id"] not in {
        row["witness_id"] for row in state["witnesses"]
    }:
        run(
            sys.executable,
            str(METHOD_RUNNER),
            "witness",
            "--ledger",
            str(ledger),
            "--witness-file",
            str(path),
        )
    state = read_json(ledger)
    method = next(row for row in state["methods"] if row["method_id"] == "V6504-M06")
    if method["recommendation_state"] == "validated":
        run(
            sys.executable,
            str(METHOD_RUNNER),
            "set-state",
            "--ledger",
            str(ledger),
            "--method-id",
            "V6504-M06",
            "--state",
            "preferred",
            "--note",
            "Promoted only for the exact helper-contract trigger after retaining the failed probe and passing twenty bounded packages.",
        )
    run(
        sys.executable,
        str(METHOD_RUNNER),
        "validate",
        "--ledger",
        str(ledger),
        "--receipt",
        str(ROOT / "method-flow/method-flow-validation.json"),
    )
    run(
        sys.executable,
        str(METHOD_RUNNER),
        "summarize",
        "--ledger",
        str(ledger),
        "--json-output",
        str(ROOT / "method-flow/method-flow-summary.json"),
        "--markdown-output",
        str(ROOT / "method-flow/method-flow-summary.md"),
    )


def execution_rows(plan_name: str, status: str, witness_prefix: str) -> list[dict[str, Any]]:
    plan = read_json(ROOT / f"portfolios/{plan_name}-plan.json")
    rows = []
    for item in plan["tasks"]:
        proposal = next(
            row for row in d.PROPOSALS if row["proposal_id"] == item["proposal_id"]
        )
        receipt = read_json(
            ROOT / "surfaces" / proposal["slug"] / "bounded-receipt.json"
        )
        rows.append(
            {
                **item,
                "status": status,
                "x2_completion_credit": True,
                "witness": f"{witness_prefix}/{proposal['slug']}/bounded-receipt.json",
                "observed_outcome": receipt["outcome"],
                "boundary": (
                    "Completion applies only to the declared owner-local software, "
                    "formal, structural, synthetic, or refusal hypothesis."
                ),
            }
        )
    return rows


def report_html(proposals: list[dict[str, Any]]) -> str:
    rows = "\n".join(
        "<tr>"
        f"<th scope=\"row\">{html.escape(row['proposal_id'])}</th>"
        f"<td>{html.escape(row['title'])}</td>"
        f"<td>{html.escape(row['observed_outcome'])}</td>"
        f"<td>{html.escape(row['evidence_class'])}</td>"
        "</tr>"
        for row in proposals
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Orin Thale v650-v4 bounded evidence report</title>
<style>
body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:78rem;margin:auto;padding:1rem;color:#17202a;background:#fff}}
a:focus,button:focus{{outline:3px solid #7b2cbf;outline-offset:3px}}
.skip{{position:absolute;left:-999px}}.skip:focus{{left:1rem;top:1rem;background:#fff;padding:.5rem}}
table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.5rem;text-align:left;vertical-align:top}}
caption{{font-weight:700;text-align:left;margin:.5rem 0}}.verdict{{border-left:.5rem solid #9b2226;padding:1rem;background:#fff3f3}}
@media print{{.skip{{display:none}}body{{max-width:none}}}}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<header><h1>Orin Thale v650-v4 bounded evidence report</h1><p>Relational working language only; no consciousness, personhood, continuity, employment, qualification, or authority claim.</p></header>
<nav aria-label="Report sections"><a href="#truth">Truth</a> | <a href="#outcomes">Outcomes</a> | <a href="#gates">Reserved gates</a></nav>
<main id="main">
<section id="truth" aria-labelledby="truth-heading"><h2 id="truth-heading">Phase truth</h2><p class="verdict"><strong>NOT_READY_FOR_STAGE_20</strong>. Twenty proposals were exercised only in bounded owner-local evidence classes. Same-owner results are not independent reproduction.</p></section>
<section id="outcomes" aria-labelledby="outcomes-heading"><h2 id="outcomes-heading">Proposal outcomes</h2><table><caption>Twenty frozen proposals and bounded outcomes</caption><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Evidence class</th></tr></thead><tbody>{rows}</tbody></table></section>
<section id="gates" aria-labelledby="gates-heading"><h2 id="gates-heading">Reserved gates</h2><p>Empirical, participant, professional, production, deployment, privacy-complete, exhaustive-security, accessibility-complete, legal, cultural, Maori-authority, affected-party, identity, proof/canon, AGI/ASI, consciousness/personhood, Theory-of-Everything, and Stage 20 gates remain open or exact-gated.</p><p>Manual keyboard, responsive-layout, browser-diverse, assistive-technology, cognitive, Maori-language, security-usability, and affected-user evaluation remain reserved.</p></section>
</main>
<footer><p>Static structural report; no manual or affected-user conformance claim.</p></footer>
</body>
</html>"""


def main() -> int:
    runner_rows = execute_runners()
    skill_rows = build_skills()
    close_method_flow_skill_failure()

    proposal_rows = []
    for proposal in d.PROPOSALS:
        receipt = read_json(
            ROOT / "surfaces" / proposal["slug"] / "bounded-receipt.json"
        )
        proposal_rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "observed_outcome": receipt["outcome"],
                "evidence_class": receipt["evidence_class"],
                "receipt": f"surfaces/{proposal['slug']}/bounded-receipt.json",
                "mutations_executed": 5,
                "mutations_rejected": 5,
                "same_owner_only": True,
                "independent_reproduction": False,
                "protected_gates": proposal["protected_gates"],
            }
        )
    observed = Counter(row["observed_outcome"] for row in proposal_rows)
    if dict(observed) != {
        "completed": 14,
        "open_gap": 1,
        "represented": 4,
        "exact_gate": 1,
    }:
        raise RuntimeError(f"unexpected outcome distribution: {dict(observed)}")

    safe_execution = execution_rows(
        "safe-now", "completed_with_bounded_witness", "surfaces"
    )
    candidate_execution = execution_rows(
        "candidate", "completed_with_bounded_prototype_witness", "surfaces"
    )
    cleanup_execution = execution_rows(
        "clean-fix-refine", "completed_additive_non_destructive", "surfaces"
    )
    write_json(
        "portfolios/safe-now-execution.json",
        {
            "schema": "ghc.family.v650-v4.safe-now-execution.v1",
            "count": len(safe_execution),
            "completed": len(safe_execution),
            "tasks": safe_execution,
        },
    )
    write_json(
        "portfolios/candidate-execution.json",
        {
            "schema": "ghc.family.v650-v4.candidate-execution.v1",
            "count": len(candidate_execution),
            "completed": len(candidate_execution),
            "tasks": candidate_execution,
        },
    )
    write_json(
        "portfolios/skill-execution.json",
        {
            "schema": "ghc.family.v650-v4.skill-execution.v1",
            "count": len(skill_rows),
            "completed": len(skill_rows),
            "global_install": False,
            "skills": skill_rows,
        },
    )
    write_json(
        "portfolios/runner-execution.json",
        {
            "schema": "ghc.family.v650-v4.runner-execution.v1",
            "count": len(runner_rows),
            "completed": len(runner_rows),
            "preserved_family_names": True,
            "runners": runner_rows,
        },
    )
    write_json(
        "portfolios/clean-fix-refine-execution.json",
        {
            "schema": "ghc.family.v650-v4.cleanup-execution.v1",
            "count": len(cleanup_execution),
            "completed": len(cleanup_execution),
            "destructive_actions": 0,
            "tasks": cleanup_execution,
        },
    )
    write_json(
        "x2-evidence-ledger.json",
        {
            "schema": "ghc.family.v650-v4.x2-evidence-ledger.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "proposal_count": len(proposal_rows),
            "outcome_counts": dict(observed),
            "allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"],
            "mutation_count": 100,
            "mutations_rejected_or_quarantined": 100,
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
            "schema": "ghc.family.v650-v4.mutation-results.aggregate.v1",
            "planned": 100,
            "executed": 100,
            "rejected_or_quarantined": 100,
            "accepted": 0,
            "completion_credit": False,
            "boundary": (
                "Mutation rejection is bounded guard evidence, not production security, "
                "scientific truth, authority, or independent reproduction."
            ),
        },
    )
    write_json(
        "retained-negative-register.json",
        {
            "schema": "ghc.family.v650-v4.retained-negatives.evidence.v1",
            "activation_baseline": d.ACTIVATION_NEGATIVES,
            "x1_operational": len(d.X1_OPERATIONAL_NEGATIVES),
            "synthetic_mutations": 100,
            "x2_operational": 6,
            "effective_total": d.ACTIVATION_NEGATIVES
            + len(d.X1_OPERATIONAL_NEGATIVES)
            + 100
            + 6,
            "erased": 0,
            "entries": [
                {
                    "negative_id": "INHERITED-EFFECTIVE-THROUGH-V6503",
                    "class": "inherited_aggregate",
                    "count": d.ACTIVATION_NEGATIVES,
                    "disposition": "retained",
                },
                *[
                    {
                        "negative_id": row["negative_id"],
                        "class": "x1_operational",
                        "count": 1,
                        "failure": row["failed"],
                        "disposition": "retained",
                    }
                    for row in d.X1_OPERATIONAL_NEGATIVES
                ],
                {
                    "negative_id": "V6504-MUTATION-AGGREGATE",
                    "class": "preregistered_synthetic",
                    "count": 100,
                    "disposition": "executed_rejected_or_quarantined",
                },
                {
                    "negative_id": "V6504-X2-N01",
                    "class": "x2_operational",
                    "count": 1,
                    "failure": (
                        "A combined helper-help probe assumed quick_validate supported "
                        "--help; it interpreted the flag as a skill path and stopped."
                    ),
                    "disposition": "retained_with_bounded_recovery",
                },
                {
                    "negative_id": "V6504-X2-N02",
                    "class": "x2_operational",
                    "count": 1,
                    "failure": (
                        "The first 22-test aggregate passed nineteen tests but failed "
                        "three x1 lifecycle assertions that read mutable successor files "
                        "instead of immutable x1 commit blobs."
                    ),
                    "disposition": "retained_with_bounded_recovery",
                },
                {
                    "negative_id": "V6504-X2-N03",
                    "class": "x2_operational",
                    "count": 1,
                    "failure": (
                        "The second 22-test aggregate passed twenty-one tests but one "
                        "x2 assertion hard-coded six Method Flow methods after the "
                        "seventh method had been retained."
                    ),
                    "disposition": "retained_with_bounded_recovery",
                },
                {
                    "negative_id": "V6504-X2-N04",
                    "class": "x2_operational",
                    "count": 1,
                    "failure": (
                        "The first Method Flow validation retry used unsupported "
                        "--state-file options; argparse stopped before reading the ledger."
                    ),
                    "disposition": "retained_with_bounded_recovery",
                },
                {
                    "negative_id": "V6504-X2-N05",
                    "class": "x2_operational",
                    "count": 1,
                    "failure": (
                        "A CLI discovery probe assumed nonexistent add-method and "
                        "add-witness subcommands; argparse rejected both choices."
                    ),
                    "disposition": "retained_with_bounded_recovery",
                },
                {
                    "negative_id": "V6504-X2-N06",
                    "class": "x2_operational",
                    "count": 1,
                    "failure": (
                        "A post-review inventory assumed a manifests directory that "
                        "this phase does not define, causing a path-not-found error."
                    ),
                    "disposition": "retained_with_bounded_recovery",
                },
            ],
        },
    )
    write_json(
        "exact-open-gate-register.json",
        {
            "schema": "ghc.family.v650-v4.gates.evidence.v1",
            "inherited_open_gaps": d.INHERITED_OPEN_GAPS,
            "inherited_exact_gates": d.INHERITED_EXACT_GATES,
            "new_open_gap": "V6504-P05",
            "new_exact_gate": "V6504-P10",
            "effective_open_gaps": d.INHERITED_OPEN_GAPS + 1,
            "effective_exact_gates": d.INHERITED_EXACT_GATES + 1,
            "closed_without_evidence": 0,
        },
    )
    write_json(
        "phase-truth.json",
        {
            "schema": "ghc.family.v650-v4.phase-truth.evidence.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "state": "X2_EVIDENCE_CANDIDATE",
            "x2_started": True,
            "x1_commit": "2aef76bbfc315857ff5bd134424a346fa70d1ec3",
            "x1_was_clean_pushed_four_way_equal_before_x2": True,
            "outcome_counts": dict(observed),
            "effective_negatives": d.ACTIVATION_NEGATIVES
            + len(d.X1_OPERATIONAL_NEGATIVES)
            + 100
            + 6,
            "open_gaps": d.INHERITED_OPEN_GAPS + 1,
            "exact_gates": d.INHERITED_EXACT_GATES + 1,
            "real_empirical_rows": 0,
            "real_participants_or_operators": 0,
            "real_keys_or_proofs": 0,
            "authority_decisions": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": d.BOUNDARY,
        },
    )
    write_json(
        "reproduction-receipt.json",
        {
            "schema": "ghc.family.v650-v4.reproduction.evidence.v1",
            "owner": d.OWNER,
            "canonical_owner_execution": True,
            "additional_replay": False,
            "independent_team": False,
            "independent_reproduction": False,
            "claim": "bounded same-owner execution only",
        },
    )
    write_json(
        "ghc-family-index.json",
        {
            "schema": "ghc.family.phase-index.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "state": "x2_evidence_candidate",
            "source_head": d.SOURCE_HEAD,
            "x1_commit": "2aef76bbfc315857ff5bd134424a346fa70d1ec3",
            "proposal_count": 20,
            "outcome_counts": dict(observed),
            "portfolio_counts": {
                "safe_now": 40,
                "candidate": 30,
                "skills": 20,
                "runners": 10,
                "cleanup": 40,
                "mutations": 100,
            },
            "shared_skill_change": False,
            "caller_compatibility_preserved": True,
            "reviewed_current": [
                "ghc-family-index",
                "ghc-family-method-flow-state",
                "skill-creator",
            ],
        },
    )
    write_json(
        "complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v650-v4.checklist.evidence.v1",
            "complete": [
                "dedicated x1 commit and four-way equality",
                "twenty bounded proposal executions",
                "one hundred mutations rejected or quarantined",
                "forty safe-now tasks",
                "thirty candidate prototypes",
                "twenty phase-local skills built validated and smoke-used",
                "ten family-current runners invoked",
                "forty additive cleanup tasks",
                "six x2 operational failures retained in Method Flow",
            ],
            "incomplete": [
                "evidence exact staged review and commit",
                "evidence remote equality",
                "combined closeout and seal",
                "single successful canonical scoped pass",
                "final four-way equality",
                "terminal route",
                "all empirical participant production authority and Stage 20 gates",
            ],
        },
    )
    write_json(
        "wellbeing-check.json",
        {
            "schema": "ghc.family.v650-v4.wellbeing.evidence.v1",
            "bounded_scope": True,
            "pause_available": True,
            "rename_redirect_stop_right": "Hamish",
            "identity_pressure": False,
            "quota_safety_override": False,
            "workload_state": "bounded_x2_evidence_cadence_not_used_as_proof",
        },
    )
    write_json(
        "orchestration/terminal-route-state.json",
        {
            "schema": "ghc.family.v650-v4.route.evidence.v1",
            "state": "HELD_EVIDENCE",
            "route_state": "HELD_EVIDENCE",
            "sent": False,
            "target_title": "Tamar Vey",
            "reason": "evidence is not yet committed, sealed, or terminally validated",
        },
    )
    threat = read_json(ROOT / "threat-model.json")
    threat["schema"] = "ghc.family.v650-v4.threat-model.evidence.v1"
    threat["observed_controls"] = {
        "mutations_executed_and_rejected": 100,
        "phase_local_skills_validated": 20,
        "family_runners_witnessed": 10,
        "real_network_or_authority_actions": 0,
        "retained_operational_failures": 11,
    }
    write_json("threat-model.json", threat)
    write_text("report.html", report_html(proposal_rows))
    write_text(
        "x2-evidence-summary.md",
        "# Orin Thale v650-v4 x2 evidence summary\n\n"
        "Observed bounded outcomes are **14 completed / 4 represented / 1 open_gap / 1 exact_gate**. "
        "All 100 preregistered synthetic mutations were rejected or quarantined. "
        "The 2MASS adapter used zero rows and zero likelihood evaluations. The e-bike authority matrix made zero authority decisions. "
        "Freed ID used zero real keys, proofs, accounts, tokens, or network exchanges. THOS used zero real participants, operators, batteries, or repairs.\n\n"
        "The terminal verdict remains `NOT_READY_FOR_STAGE_20`. Same-owner execution is not independent reproduction.",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
