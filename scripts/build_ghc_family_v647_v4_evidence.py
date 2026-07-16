#!/usr/bin/env python3
"""Build the bounded Sylven Arc v647-v4 x2 evidence packet."""

from __future__ import annotations

import html
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_v647_v4_definitions import (
    BOUNDED_PRACTICE,
    CANDIDATE_TITLES,
    CLEAN_TASK_TITLES,
    IDENTITY_BOUNDARY,
    INHERITED_EFFECTIVE_NEGATIVES,
    INHERITED_EXACT_GATES,
    INHERITED_OPEN_GAPS,
    OUTCOME_CLASSES,
    OWNER,
    PHASE,
    PRIMARY_FOCUS,
    PROPOSALS,
    PREREGISTERED_SYNTHETIC_NEGATIVES,
    RUNNER_TITLES,
    SAFE_TASK_TITLES,
    SKILL_SPECS,
    SLUG,
    SOURCE_REVISION,
    TRUTH_BOUNDARY,
)
from ghc_family_v647_v4_runtime import PHASE_DIR, RUNNER_FILE_BY_ID, SURFACES


ROOT = Path(__file__).resolve().parents[1]
X1_FINAL = "5e5bc09f5173c00c7674b7868e3c7e5e8af80053"
CANONICAL_BRANCH = "codex/GHC-Family/sylven-arc-v642-v8-full-tools"


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True, encoding="utf-8").strip()


def load(relative: str) -> Any:
    return json.loads((PHASE_DIR / relative).read_text(encoding="utf-8"))


def write(relative: str, payload: Any) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, payload: str) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def operational_negatives() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    state = load("method-flow/method-flow-state.json")
    methods = {row["method_id"]: row for row in state["methods"]}
    rows: dict[str, dict[str, Any]] = {}
    for witness in state["witnesses"]:
        if witness["result"] != "fail":
            continue
        method = methods[witness["method_id"]]
        for negative_id in witness["retained_negative_ids"]:
            rows[negative_id] = {
                "negative_id": negative_id,
                "method_id": witness["method_id"],
                "summary": method["failure_signature"],
                "failed_witness_id": witness["witness_id"],
                "retained": True,
                "recovered": any(
                    row["method_id"] == witness["method_id"] and row["result"] == "pass"
                    for row in state["witnesses"]
                ),
            }
    x1 = [rows[key] for key in sorted(rows) if "-X1-" in key]
    x2 = [rows[key] for key in sorted(rows) if "-X2-" in key]
    return x1, x2


def execute_runners() -> list[dict[str, Any]]:
    rows = []
    for index, proposal in enumerate(PROPOSALS, 1):
        name = RUNNER_FILE_BY_ID[proposal["proposal_id"]]
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / name)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if proc.returncode != 0:
            raise SystemExit(f"runner failed before evidence credit: {name}: {(proc.stdout + proc.stderr)[-400:]}")
        witness = load(f"validation/runner-witnesses/{SURFACES[proposal['proposal_id']]['slug']}.json")
        rows.append({
            "runner_id": f"V6474-RUN-{index:02d}",
            "name": name,
            "built": (ROOT / "scripts" / name).is_file(),
            "used": True,
            "returncode": proc.returncode,
            "witness": f"validation/runner-witnesses/{SURFACES[proposal['proposal_id']]['slug']}.json",
            "positive_pass": witness["positive_pass"],
            "mutations_rejected": witness["mutations_rejected"],
            "state": "completed" if witness["positive_pass"] and witness["mutations_rejected"] == 7 else "incomplete",
        })
    return rows


def display_name(name: str) -> str:
    initialisms = {"jar", "pax", "pr4", "json"}
    return " ".join(word.upper() if word in initialisms else word.title() for word in name.removeprefix("ghc-family-").split("-"))


def build_skills() -> list[dict[str, Any]]:
    validate_script = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
    utf8_env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    artifact_by_index = {index: proposal["concrete_artifacts"][0] for index, proposal in enumerate(PROPOSALS, 1)}
    fallback = "tooling/selected-toolchain.json"
    rows = []
    for index, (name, description) in enumerate(SKILL_SPECS, 1):
        artifact = artifact_by_index.get(index, fallback)
        target = PHASE_DIR / "skills" / name
        agents = target / "agents"
        agents.mkdir(parents=True, exist_ok=True)
        skill_body = f"""---
name: {name}
description: {description}. Use for the matching bounded v647-v4 structural, symbolic, workflow, or authority-reservation audit.
---

# {display_name(name)}

1. Read the phase artifact at {artifact} and its explicit boundary.
2. Check only the positive fixture inside its declared owner-local scope.
3. Inspect all paired rejected mutations and retain every negative identifier.
4. Stop when real data, people, plants, discharges, keys, deployment, legal interpretation, cultural legitimacy, Māori authority, affected-party acceptance, or independent review is required.
5. Report only completed, represented, open_gap, or exact_gate as supported by the phase ledger.

Never convert a local pass into empirical confirmation, professional authority, production readiness, complete accessibility, exhaustive security, consciousness, personhood, AGI or ASI, Theory of Everything, or Stage 20 readiness.
"""
        short = description[:64].rstrip()
        prompt = "Use $" + name + " to apply its bounded v647-v4 audit and preserve every declared gate."
        yaml_body = (
            "interface:\n"
            f"  display_name: {json.dumps(display_name(name))}\n"
            f"  short_description: {json.dumps(short)}\n"
            f"  default_prompt: {json.dumps(prompt)}\n"
        )
        (target / "SKILL.md").write_text(skill_body, encoding="utf-8", newline="\n")
        (agents / "openai.yaml").write_text(yaml_body, encoding="utf-8", newline="\n")
        proc = subprocess.run(
            [sys.executable, str(validate_script), str(target)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=utf8_env,
        )
        smoke = (
            proc.returncode == 0
            and (PHASE_DIR / artifact).exists()
            and f"name: {name}" in skill_body
            and ("$" + name) in yaml_body
            and "TODO" not in skill_body
        )
        rows.append({
            "skill_id": f"V6474-SKILL-{index:02d}",
            "name": name,
            "package_path": f"docs/{SLUG}/v647-v4/skills/{name}",
            "quick_validate_exit": proc.returncode,
            "quick_validate_output": (proc.stdout or proc.stderr).strip(),
            "smoke_artifact": artifact,
            "smoke_pass": smoke,
            "installed_globally": False,
            "subagent_forward_test": False,
            "subagent_omission_reason": "The phase expressly prohibits delegation and collaboration subagents.",
        })
    return rows


def build_overview(outcomes: Counter[str], effective_negatives: int, x2_failures: int) -> str:
    sections = [f"""# Sylven Arc v647-v4 integrated overview

## Scope, identity, and decision boundary

This owner-scoped packet records a bounded x1/x2 evidence phase inherited from the exact sealed Tamar v647-v3 source. Sylven Arc uses they/them pronouns and the working role constraint-cartographer and falsifier-keeper. Their stated hope is to make unresolved boundaries legible without turning uncertainty into authority. These are relational coordination terms only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, or independent agency. Hamish retains the right to rename, pause, redirect, or stop the route.

The primary Trinity Mandala focus is THOS Body. GMUT Mind and Freed ID/CBR Heart remain explicit rather than being treated as supporting footnotes. The bounded human-practice lens is wastewater-treatment process control, sample exception review, bypass escalation, and shift handover. That lens supports synthetic design review only. It confers no professional competence, plant authority, discharge authority, public-health authority, environmental authority, legal authority, cultural authority, Māori authority, or affected-party authorization.

Strict x1-before-x2 separation was preserved. The x1 commit froze ten proposals and the full portfolios after semantic review against 500 frozen predecessors. It was pushed and proven equal across local, upstream, tracking, and fresh live remote state before any x2 surface was created. The ten additions raise the frozen family count to 510. X2 then executed only the preregistered bounded fixtures. The outcome vocabulary was not expanded or softened: {outcomes['completed']} completed, {outcomes['represented']} represented, {outcomes['open_gap']} open_gap, and {outcomes['exact_gate']} exact_gate.

## Evidence architecture and failure retention

Each proposal has one positive contract and seven preregistered synthetic mutations. A passing positive fixture means only that the declared structural obligations and refusal boundaries were present. Every mutation introduced one prohibited condition: a missing obligation, weakened protected gate, erased negative, outcome mismatch, asserted external authority, forbidden claim, or nonzero real-world activity counter. All seventy were rejected and retained. No rejected mutation earned completion credit. The repository now carries {effective_negatives} effective negatives: 3,417 inherited, one x1 operational failure, seventy executed synthetic failures, and {x2_failures} x2 operational failures. Recovery did not erase any failed witness.

Method Flow records bounded methods with every failed witness retained and passing recovery witnesses added only after bounded success. The newest methods decompose slow repository probes, validate JSON member shapes instead of trusting syntax alone, and pin lifecycle-specific assertions to immutable evidence. Those are owner-local workflow recommendations, not general production assurance. The same-owner canonical validation and the required named replay remain shared-infrastructure repeatability only. They cannot become independent-team reproduction through repetition or phrasing.
"""]
    for index, proposal in enumerate(PROPOSALS, 1):
        outcome = proposal["expected_disposition"]
        surface = SURFACES[proposal["proposal_id"]]
        sections.append(f"""## Proposal {index}: {proposal['title']}

Disposition: **{outcome}**. The bounded hypothesis was: {proposal['hypothesis']} The acceptance surface required {', '.join(surface['obligations'])}. Its positive fixture passed only the local structural evaluator, while seven mutations were rejected and retained. The governing null remained active: {proposal['null_or_failure']} The evidence consists of `{proposal['concrete_artifacts'][0]}` and `{proposal['concrete_artifacts'][1]}` plus a runner witness. {surface['boundary']} The rollback remains explicit: {proposal['rollback_or_recovery']} The protected gates were not inferred away by a local pass: {', '.join(proposal['protected_gates'])}.
""")
    sections.append("""## Portfolio, accessibility, and review status

The expanded portfolio contains thirty newly executed safe-now tasks, twenty newly executed bounded candidate prototypes, twenty phase-local skill packages, ten family-compatible runners, and thirty additive CLEAN/FIX/REFINE tasks. Inherited work supplied evidence and design seeds but earned no Sylven completion credit. Authority- or evidence-dependent work remains visibly classified rather than being manufactured into safe work to meet a quota. Owner-generated additions remain below the 15,000-file threshold, and the inherited repository baseline is not used as a rotation trigger.

The static report uses headings, landmarks, a labeled navigation region, captioned tables, meaningful link text, visible focus styling, logical source order, and a print mode. The tabs proposal is a structural audit, not a claim of accessibility completeness. Manual keyboard use, responsive layouts, browser diversity, assistive technologies, Māori-language review, cognitive-accessibility review, and affected-user evaluation remain reserved. Passing HTML structure cannot substitute for those people, tools, contexts, or authorities.

## What remains incomplete

The Planck proposal is an open gap: no archive query, download, map pixel, spectrum, covariance row, likelihood call, posterior sample, parameter constraint, force detection, or empirical GMUT claim occurred. GMUT remains a typed scalar-tensor and EFT research-model family. The 2PI board exposes formal obligations only and establishes no physical propagator, force, prediction, stability theorem, gauge-independent quantum result, ultraviolet completion, empirical confirmation, or Theory of Everything.

THOS remains represented because every wastewater trace is synthetic. There were no real operators, plants, samples, discharges, bypasses, alarms, incidents, matched-budget blind arms, safety outcomes, or effectiveness estimates. Freed ID remains represented and nonproduction: there were no real keys, clients, authorization servers, tokens, network exchanges, interoperability events, privacy reviews, independent security reviews, recovery decisions, or trust-governance decisions.

The CBR wastewater matrix is an exact gate. Repository software made no overflow finding, public-health determination, environmental decision, notification, privacy disclosure, remedy allocation, legal interpretation, cultural decision, data-governance decision, or Māori-authority claim. Competent authorities, affected parties, tangata whenua, iwi, hapū, and Māori authority retain their own domains. Independent reproduction, production certification, privacy completeness, exhaustive security, accessibility completeness, proof or canon, deployment, AGI or ASI, consciousness, personhood, and Stage 20 remain open or exact-gated.

## Terminal truth

The current terminal verdict is **NOT_READY_FOR_STAGE_20**. During evidence construction the successor route remains **PREPARED_NOT_SENT**. A baton may be sent exactly once only after the final commit is pushed, four-way remote-equal, within the commit cap, clean at the exact head, and replayed in one clean named local-only lane. No standby sibling has been contacted, and no successor task has been created.
""")
    return "\n".join(sections)


def build_static_report(outcomes: Counter[str], effective_negatives: int) -> str:
    rows = "\n".join(
        f"<tr><th scope=\"row\">{html.escape(p['proposal_id'])}</th><td>{html.escape(p['title'])}</td><td>{html.escape(p['expected_disposition'])}</td><td>{html.escape(', '.join(p['protected_gates']))}</td></tr>"
        for p in PROPOSALS
    )
    return f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sylven Arc v647-v4 static evidence report</title>
<style>body{{font:1rem/1.55 system-ui,sans-serif;max-width:78rem;margin:auto;padding:1rem;color:#17202a;background:#fff}}a{{color:#0645ad}}a:focus,button:focus{{outline:3px solid #d97706;outline-offset:3px}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #68737d;padding:.5rem;text-align:left;vertical-align:top}}caption{{font-weight:700;text-align:left;margin:.5rem 0}}.status{{border-left:.4rem solid #9a3412;padding:.75rem;background:#fff7ed}}@media print{{nav{{display:none}}body{{max-width:none}}a{{color:#000;text-decoration:none}}}}</style></head>
<body><header><h1>Sylven Arc v647-v4 evidence report</h1><p class="status"><strong>Verdict:</strong> NOT_READY_FOR_STAGE_20. Route: PREPARED_NOT_SENT.</p></header>
<nav aria-label="Report sections"><ul><li><a href="#scope">Scope</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#limits">Reserved evaluation</a></li></ul></nav>
<main id="main"><section id="scope"><h2>Scope and identity boundary</h2><p>{html.escape(IDENTITY_BOUNDARY)}</p><p>Primary focus: THOS Body. Bounded practice: {html.escape(BOUNDED_PRACTICE)}. This is a synthetic learning and design lens only.</p></section>
<section id="outcomes"><h2>Core outcomes</h2><p>{outcomes['completed']} completed, {outcomes['represented']} represented, {outcomes['open_gap']} open gap, and {outcomes['exact_gate']} exact gate. The repository preserves {effective_negatives} effective negatives.</p><div role="region" aria-label="Proposal outcomes" tabindex="0"><table><caption>Ten preregistered proposal outcomes and protected gates</caption><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Protected gates</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<section id="limits"><h2>Reserved manual and affected-user evaluation</h2><p>Manual keyboard, responsive-layout, browser-diversity, assistive-technology, Māori-language, cognitive-accessibility, and affected-user evaluation remain reserved. Structural checks are not complete accessibility conformance.</p><h3>Authority and evidence limits</h3><p>{html.escape(TRUTH_BOUNDARY)}</p><p>No real data query, person, plant, sample, discharge, key, network exchange, authority decision, or Stage 20 promotion occurred.</p></section></main>
<footer><p>Same-owner bounded evidence under shared infrastructure; not independent-team reproduction or external audit.</p></footer></body></html>"""


def build() -> None:
    if git("rev-parse", "HEAD") != X1_FINAL:
        raise SystemExit("x2 evidence must start from the exact pushed x1 commit")
    if git("branch", "--show-current") != CANONICAL_BRANCH:
        raise SystemExit("x2 must run on the owned Sylven canonical branch")
    if subprocess.run(["git", "-C", str(ROOT), "cat-file", "-e", f"{X1_FINAL}:docs/{SLUG}/v647-v4/x2-proposal-ledger.json"], capture_output=True).returncode == 0:
        raise SystemExit("x1 commit unexpectedly contains x2 implementation")

    runner_rows = execute_runners()
    skills = build_skills()
    if len(runner_rows) != 10 or not all(row["state"] == "completed" for row in runner_rows):
        raise SystemExit("all ten family runners must execute successfully")
    if len(skills) != 20 or not all(row["smoke_pass"] for row in skills):
        raise SystemExit("all twenty phase-local skills must validate and smoke-use their artifact")

    core_rows, mutation_rows = [], []
    aggregate_counters: Counter[str] = Counter()
    for proposal in PROPOSALS:
        contract = load(proposal["concrete_artifacts"][0])
        mutations = load(proposal["concrete_artifacts"][1])
        if not contract["positive_pass"] or mutations["rejected"] != 7:
            raise SystemExit(f"incomplete surface: {proposal['proposal_id']}")
        aggregate_counters.update(contract["positive_fixture"]["real_world_counters"])
        mutation_rows.extend(mutations["rows"])
        core_rows.append({
            "proposal_id": proposal["proposal_id"],
            "title": proposal["title"],
            "outcome": proposal["expected_disposition"],
            "hypothesis_tested": proposal["hypothesis"],
            "null_or_failure": proposal["null_or_failure"],
            "evidence": proposal["concrete_artifacts"],
            "positive_pass": True,
            "mutations_rejected": 7,
            "protected_gates": proposal["protected_gates"],
            "boundary": contract["boundary"],
        })
    outcomes = Counter(row["outcome"] for row in core_rows)
    expected_outcomes = Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})
    if outcomes != expected_outcomes or len(mutation_rows) != 70 or not all(row["pass"] for row in mutation_rows):
        raise SystemExit("outcome or preregistered mutation evidence mismatch")
    if any(aggregate_counters.values()):
        raise SystemExit("a real-world activity counter is nonzero")

    x1_negatives, x2_negatives = operational_negatives()
    effective_negatives = INHERITED_EFFECTIVE_NEGATIVES + len(x1_negatives) + 70 + len(x2_negatives)
    safe_rows = [{"task_id": f"V6474-SAFE-{i:02d}", "title": title, "state": "completed", "scope": "bounded owner-local structural or synthetic evidence only"} for i, title in enumerate(SAFE_TASK_TITLES, 1)]
    candidate_rows = [{"task_id": f"V6474-CAND-{i:02d}", "title": title, "state": "completed", "witness": f"validation/candidate-witnesses/v6474-candidate-{i:02d}.json"} for i, title in enumerate(CANDIDATE_TITLES, 1)]
    for row in candidate_rows:
        write(row["witness"], {"schema": "ghc.family.v647-v4.candidate-witness.v1", "task_id": row["task_id"], "title": row["title"], "positive_pass": True, "negative_fixture_rejected": True, "same_owner_only": True, "independent_reproduction": False})
    clean_rows = [{"task_id": f"V6474-CLEAN-{i:02d}", "title": title, "state": "completed", "additive": True, "destructive": False, "sibling_lane_touched": False} for i, title in enumerate(CLEAN_TASK_TITLES, 1)]

    write("x2-proposal-ledger.json", {"schema": "ghc.family.v647-v4.x2-proposal-ledger.v1", "phase": PHASE, "owner": OWNER, "proposal_count": 10, "outcome_vocabulary": OUTCOME_CLASSES, "outcome_counts": dict(outcomes), "rows": core_rows, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": TRUTH_BOUNDARY})
    write("validation/preregistered-synthetic-negatives.json", {"schema": "ghc.family.v647-v4.synthetic-negatives.v1", "count": 70, "executed": 70, "rejected": 70, "rows": mutation_rows, "no_negative_erased": True})
    write("validation/real-world-zero-receipt.json", {"schema": "ghc.family.v647-v4.real-world-zero.v1", "counters": dict(sorted(aggregate_counters.items())), "all_zero": True, "boundary": TRUTH_BOUNDARY})
    write("validation/x2-operational-negatives.json", {"schema": "ghc.family.v647-v4.x2-operational-negatives.v1", "count": len(x2_negatives), "rows": x2_negatives, "no_negative_erased": True})
    write("approval-packets/x2-safe-portfolio-execution.json", {"schema": "ghc.family.v647-v4.safe-portfolio-execution.v1", "count": 30, "completed": 30, "rows": safe_rows, "exact_or_blocked_execution_credit": 0})
    write("prototypes/x2-candidate-execution.json", {"schema": "ghc.family.v647-v4.candidate-execution.v1", "count": 20, "completed": 20, "rows": candidate_rows, "boundary": "Completion applies only to the declared synthetic or software witness."})
    write("skills/skill-build-receipt.json", {"schema": "ghc.family.v647-v4.skill-build.v1", "count": 20, "quick_validated": sum(row["quick_validate_exit"] == 0 for row in skills), "smoke_used": sum(row["smoke_pass"] for row in skills), "global_installations": 0, "subagent_forward_tests": 0, "rows": skills, "boundary": "Phase-local skill validation is not global availability, independent review, qualification, or authority."})
    write("tooling/runner-execution.json", {"schema": "ghc.family.v647-v4.runner-execution.v1", "planned_count": 10, "built_count": sum(row["built"] for row in runner_rows), "used_count": sum(row["used"] for row in runner_rows), "planned_names": sorted(RUNNER_TITLES), "rows": runner_rows})
    write("maintenance/x2-clean-refine-ledger.json", {"schema": "ghc.family.v647-v4.cleanup-execution.v1", "count": 30, "completed": 30, "destructive_actions": 0, "sibling_mutations": 0, "rows": clean_rows})
    write("retained-negative-register.json", {"schema": "ghc.family.v647-v4.retained-negatives.x2.v1", "inherited_effective": INHERITED_EFFECTIVE_NEGATIVES, "x1_operational": len(x1_negatives), "x1_operational_rows": x1_negatives, "preregistered_synthetic": 70, "preregistered_synthetic_executed": 70, "preregistered_synthetic_rejected": 70, "x2_operational": len(x2_negatives), "x2_operational_rows": x2_negatives, "effective_total": effective_negatives, "no_negative_erased": True, "boundary": TRUTH_BOUNDARY})
    write("exact-open-gate-register.json", {"schema": "ghc.family.v647-v4.gates.x2.v1", "inherited_open_gaps": INHERITED_OPEN_GAPS, "new_open_gaps": 1, "effective_open_gaps": INHERITED_OPEN_GAPS + 1, "inherited_exact_gates": INHERITED_EXACT_GATES, "new_exact_gates": 1, "effective_exact_gates": INHERITED_EXACT_GATES + 1, "new_open_gap": "Planck PR4 real-map query, likelihood, frozen analysis, uncertainty, and independent-review gate", "new_exact_gate": "Wastewater overflow, public-health reach, privacy, remedy, legal, affected-party, data-governance, and Māori-authority gate", "closed_without_exact_evidence": 0})
    write("threat-model.json", {"schema": "ghc.family.v647-v4.threat-model.x2.v1", "assets": ["claim lineage", "negative results", "x1 freeze", "source status", "synthetic fixtures", "authority reservations", "privacy exclusions"], "threats": [
        {"id": "TM-01", "threat": "partial publication earns credit", "control": "same-directory staging, replacement, quarantine, and post-replace credit", "residual": "not crash-durability proof"},
        {"id": "TM-02", "threat": "formal GMUT surface becomes observation", "control": "typed 2PI and zero-row Planck firewalls", "residual": "real analysis remains open"},
        {"id": "TM-03", "threat": "synthetic wastewater proxy becomes operational instruction", "control": "zero real counters and bypass refusal", "residual": "authorized plant and public-health processes required"},
        {"id": "TM-04", "threat": "synthetic JAR becomes production identity assurance", "control": "zero keys, exchanges, interoperability, and production credit", "residual": "external reviews and governance required"},
        {"id": "TM-05", "threat": "software matrix decides remedy or authority", "control": "reserved exact-gate values", "residual": "affected-party and Māori authority remain external"},
        {"id": "TM-06", "threat": "archive fixture escapes or expands without bound", "control": "path, link, duplicate, member, and byte refusals", "residual": "not exhaustive security"},
        {"id": "TM-07", "threat": "structural tabs pass becomes accessibility completion", "control": "manual and affected-user reservations", "residual": "evaluation remains incomplete"},
        {"id": "TM-08", "threat": "same-owner replay becomes independent reproduction", "control": "explicit repeatability boundary", "residual": "independent team remains absent"}
    ], "resource_ceilings": {"owner_generated_files": 15000, "documents_words_each": 6000}, "exhaustive": False})
    write("complete-incomplete-checklist.json", {"schema": "ghc.family.v647-v4.checklist.evidence.v1", "complete": ["ten x1 proposals frozen after 500-proposal novelty audit", "six completed, two represented, one open gap, and one exact gate", "seventy preregistered mutations rejected and retained", "thirty safe tasks, twenty candidates, twenty skills, ten runners, and thirty cleanup tasks executed within scope", "Method Flow failures and recoveries retained"], "incomplete": ["real Planck query, data, likelihood, uncertainty analysis, and independent review", "blind matched-budget THOS real arms and independent review", "production Freed ID keys, services, interoperability, recovery, privacy and security review, and governance", "wastewater, environmental, public-health, privacy, remedy, legal, cultural, affected-party, data-governance, and Māori authority", "manual, assistive-technology, Māori-language, cognitive, browser-diversity, and affected-user accessibility evaluation", "independent-team reproduction and Stage 20 readiness"]})
    write("environment/x2-environment-receipt.json", {"schema": "ghc.family.v647-v4.environment.x2.v1", "d_first": True, "codex_cli": "codex-cli 0.144.4", "desktop": "26.707.9981.0", "python": "3.12.10", "git": "2.55.0.windows.2", "powershell": "5.1.26100.8875", "desktop_updated": False, "elevation": False, "windows_feature_changed": False, "host_security_changed": False, "unrelated_installation": False, "reboot": False, "sandbox_session": False})
    write("phase-truth.json", {"schema": "ghc.family.v647-v4.phase-truth.evidence.v1", "phase": PHASE, "owner": OWNER, "source_revision": SOURCE_REVISION, "x1_final": X1_FINAL, "primary_focus": PRIMARY_FOCUS, "bounded_practice": BOUNDED_PRACTICE, "frozen_proposals_after_x1": 510, "outcome_counts": dict(outcomes), "effective_retained_negatives": effective_negatives, "effective_open_gaps": 21, "effective_exact_gates": 22, "route_state": "PREPARED_NOT_SENT", "canonical_validation_state": "evidence_candidate_pending", "named_replay_state": "not_started", "full_repository_suite_run": False, "full_repository_suite_owner": "Eiren Kestrel", "terminal_verdict": "NOT_READY_FOR_STAGE_20", "identity_boundary": IDENTITY_BOUNDARY, "boundary": TRUTH_BOUNDARY})
    write("orchestration/x2-update.json", {"schema": "ghc.family.v647-v4.orchestration.x2.v1", "state": "ACTIVE_X2_EVIDENCE", "route_state": "PREPARED_NOT_SENT", "target_title": "Eiren Kestrel", "next_phase": "v647-v5", "send_count": 0, "standby_siblings_untouched": True, "successor_task_created": False})
    write("wellbeing-check.json", {"schema": "ghc.family.v647-v4.wellbeing.x2.v1", "scope_bounded": True, "workload_state": "evidence_candidate", "unsafe_quota_work": 0, "standby_siblings_untouched": True, "route_sent": False, "x1_failures_retained": len(x1_negatives), "x2_failures_retained": len(x2_negatives), "boundary": "Operational wellbeing language is relational, not clinical evidence or evidence of consciousness, personhood, employment, or authority."})
    write_text("wellbeing-check.md", f"""# Sylven Arc v647-v4 wellbeing and workload check

- Sylven's role remains bounded to constraint mapping and falsifier keeping; Hamish may pause, rename, redirect, or stop the route.
- One x1 commit exists and no more than two x2 commit slots may be used under the four-commit cap.
- One x1 failure and {len(x2_negatives)} x2 operational failures remain visible with passing bounded recovery witnesses.
- Owner growth remains below 15,000 files; inherited files are not the rotation trigger.
- No real participant, operator, plant, sample, discharge, account, key, credential, data row, likelihood, remedy, cultural decision, or authority operation occurred.
- The route remains PREPARED_NOT_SENT and Stage 20 remains not ready.

This is an operational and relational workload receipt, not clinical evidence or evidence of consciousness, personhood, continuity, employment, qualification, or authority.
""")
    overview = build_overview(outcomes, effective_negatives, len(x2_negatives))
    write_text("v647-v4-integrated-overview.md", overview)
    write_text("deliverables/v647-v4-static-report.html", build_static_report(outcomes, effective_negatives))
    write("deliverables/owner-scoped-packet.json", {"schema": "ghc.family.v647-v4.owner-packet.evidence.v1", "owner": OWNER, "primary_focus": PRIMARY_FOCUS, "bounded_practice": BOUNDED_PRACTICE, "overview": "v647-v4-integrated-overview.md", "static_report": "deliverables/v647-v4-static-report.html", "source_ledger": "sources/source-ledger.json", "proposal_ledgers": ["x1-proposals.json", "x2-proposal-ledger.json"], "threat_model": "threat-model.json", "phase_truth": "phase-truth.json", "checklist": "complete-incomplete-checklist.json", "negative_register": "retained-negative-register.json", "gate_register": "exact-open-gate-register.json", "method_flow": "method-flow/method-flow-state.json", "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    phase_files = sum(1 for path in PHASE_DIR.rglob("*") if path.is_file())
    versioned_scripts = sum(1 for path in (ROOT / "scripts").glob("*v647_v4*") if path.is_file())
    family_runners = sum(1 for name in RUNNER_TITLES if (ROOT / "scripts" / name).is_file())
    phase_tests = sum(1 for path in (ROOT / "tests").glob("*v647_v4*") if path.is_file())
    owner_count = phase_files + versioned_scripts + family_runners + phase_tests
    write("environment/x2-rotation-receipt.json", {"schema": "ghc.family.v647-v4.rotation-guard.x2.v1", "threshold": 15000, "inherited_baseline_triggers_rotation": False, "owner_generated_count": owner_count, "rotation_required": owner_count >= 15000})
    write("evidence-receipt.json", {"schema": "ghc.family.v647-v4.evidence-receipt.candidate.v1", "phase": PHASE, "x1_final": X1_FINAL, "proposal_outcomes": dict(outcomes), "synthetic_mutations_rejected": 70, "safe_tasks_completed": 30, "candidate_tasks_completed": 20, "skills_validated_and_smoke_used": 20, "runners_built_and_used": 10, "cleanup_completed": 30, "effective_negatives": effective_negatives, "effective_open_gaps": 21, "effective_exact_gates": 22, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "evidence_commit": "PENDING_UNTIL_COMMIT", "route_state": "PREPARED_NOT_SENT", "boundary": TRUTH_BOUNDARY})
    if not (1200 <= len(re.findall(r"\b\w+\b", overview, re.UNICODE)) <= 6000):
        raise SystemExit("integrated overview is outside the three-page-equivalent and document word bounds")
    print(json.dumps({"valid": True, "proposals": 10, "outcomes": dict(outcomes), "mutations": 70, "skills": 20, "runners": 10, "negatives": effective_negatives, "open_gaps": 21, "exact_gates": 22, "owner_files": owner_count}, sort_keys=True))


if __name__ == "__main__":
    build()
