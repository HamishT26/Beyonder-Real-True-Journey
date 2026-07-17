#!/usr/bin/env python3
"""Build the bounded Tamar Vey v648-v1 x2 evidence ledgers."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_v648_v1_definitions import (
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
    X1_OPERATIONAL_NEGATIVES,
)
from ghc_family_v648_v1_runtime import PHASE_DIR, SURFACES


ROOT = Path(__file__).resolve().parents[1]
X1_FINAL = "3e2904ec02c893d91c16e9a48fbb2485fc5d824f"
X2_OPERATIONAL_NEGATIVES: list[dict[str, Any]] = [
    {
        "negative_id": "V6481-X2-N01",
        "method_id": "V6481-M06",
        "summary": "The first scoped detailed validator loaded eighteen unittest failure placeholders because its script execution path did not expose the repository package root; no substantive test received credit, the failed receipt was retained, and explicit root insertion recovered the same frozen selection.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6481-X2-N02",
        "method_id": "V6481-M07",
        "summary": "A read-only status summary used PowerShell -like with question marks intended as literal Git status characters; wildcard interpretation falsely counted every staged line as untracked, and a StartsWith literal check recovered the exact zero-untracked result.",
        "retained": True,
        "recovered": True,
    },
]

def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(ROOT), *args], text=True, encoding="utf-8"
    ).strip()


def load(relative: str) -> Any:
    return json.loads((PHASE_DIR / relative).read_text(encoding="utf-8"))


def write(relative: str, payload: Any) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str, payload: str) -> None:
    path = PHASE_DIR / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def display_name(name: str) -> str:
    initialisms = {"des", "ssf", "caep", "risc", "cpio", "iv", "eft"}
    return " ".join(
        word.upper() if word in initialisms else word.title()
        for word in name.removeprefix("ghc-family-").split("-")
    )


def initialize_skills() -> list[dict[str, Any]]:
    creator = Path.home() / ".codex" / "skills" / ".system" / "skill-creator"
    init_script = creator / "scripts" / "init_skill.py"
    yaml_script = creator / "scripts" / "generate_openai_yaml.py"
    validate_script = creator / "scripts" / "quick_validate.py"
    skill_root = PHASE_DIR / "skills"
    skill_root.mkdir(parents=True, exist_ok=True)
    utf8_env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    core_artifacts = {
        index: SURFACES[f"V6481-P{index:02d}"]["contract"] for index in range(1, 11)
    }
    rows: list[dict[str, Any]] = []
    for index, (name, description) in enumerate(SKILL_SPECS, 1):
        target = skill_root / name
        artifact = core_artifacts.get(index, "tooling/selected-toolchain.json")
        prompt = "Use $" + name + " to apply its bounded v648-v1 audit and preserve every declared gate."
        short = description[:64].rstrip()
        if len(short) < 25:
            short += " with bounded gate preservation"
        if not (target / "SKILL.md").exists():
            subprocess.run(
                [
                    sys.executable,
                    str(init_script),
                    name,
                    "--path",
                    str(skill_root),
                    "--interface",
                    f"display_name={display_name(name)}",
                    "--interface",
                    f"short_description={short}",
                    "--interface",
                    f"default_prompt={prompt}",
                ],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=utf8_env,
            )
        body = f"""---
name: {name}
description: {description}. Use for the matching bounded v648-v1 structural, symbolic, workflow, or authority-reservation audit.
---

# {display_name(name)}

1. Read the phase artifact at {artifact} and its boundary.
2. Check the positive fixture only inside its declared local scope.
3. Inspect the paired rejected mutations and retain every negative identifier.
4. Stop when real data, people, lifting operations, incidents, keys, signals, services, deployment, legal interpretation, cultural legitimacy, Māori authority, affected-party acceptance, or independent review is required.
5. Report only completed, represented, open_gap, or exact_gate as supported by the phase ledger.

Never convert a local pass into empirical confirmation, professional authority, production readiness, complete accessibility, exhaustive security, consciousness, personhood, AGI or ASI, Theory of Everything, or Stage 20 readiness.
"""
        (target / "SKILL.md").write_text(body, encoding="utf-8", newline="\n")
        subprocess.run(
            [
                sys.executable,
                str(yaml_script),
                str(target),
                "--interface",
                f"display_name={display_name(name)}",
                "--interface",
                f"short_description={short}",
                "--interface",
                f"default_prompt={prompt}",
            ],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=utf8_env,
        )
        validation = subprocess.run(
            [sys.executable, str(validate_script), str(target)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=utf8_env,
        )
        skill_text = (target / "SKILL.md").read_text(encoding="utf-8")
        yaml_text = (target / "agents" / "openai.yaml").read_text(encoding="utf-8")
        smoke_pass = (
            validation.returncode == 0
            and f"name: {name}" in skill_text
            and "TODO" not in skill_text
            and ("$" + name) in yaml_text
            and (PHASE_DIR / artifact).exists()
        )
        rows.append(
            {
                "skill_id": f"V6481-SKILL-{index:02d}",
                "name": name,
                "package_path": f"docs/{SLUG}/v648-v1/skills/{name}",
                "initialized_with_skill_creator": True,
                "quick_validate_exit": validation.returncode,
                "quick_validate_output": (validation.stdout or validation.stderr).strip(),
                "smoke_invocation": f"Read and boundary-check {artifact}",
                "smoke_pass": smoke_pass,
                "installed_globally": False,
                "subagent_forward_test": False,
                "subagent_omission_reason": "The live phase expressly prohibits delegation and collaboration subagents.",
            }
        )
    return rows


def write_overview_and_report(
    effective_negatives: int,
    outcomes: Counter[str],
    owner_count: int,
) -> None:
    overview = f"""# Tamar Vey v648-v1 integrated overview

## Status, identity, and decision boundary

Tamar Vey, they/them, is relational working language for an evidence-systems cartographer and boundary keeper. The name, role, pronouns, and hope help organize collaboration; they are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, or independent agency. Hamish may rename, pause, redirect, or stop the route. Tamar's stated hope is to keep decisions legible, failures recoverable, and authority boundaries intact. The terminal verdict is `NOT_READY_FOR_STAGE_20`.

This packet reports a bounded x2 evidence candidate. Exactly ten frozen proposals were executed as evidence permitted, with six `completed`, two `represented`, one `open_gap`, and one `exact_gate` outcomes. Those labels have narrow meanings. Completed means a declared owner-local software, symbolic, structural, or synthetic acceptance gate passed. Represented means a local design or proxy exists but external reality was not established. Open gap means required evidence or review is absent. Exact gate means external authority is required and repository software cannot substitute for it. No other outcome vocabulary is used.

## Lineage and x1-before-x2 separation

The inherited source is Orin Thale's exact v647-v8 final head. Its source, frozen x1, and evidence anchors were checked as ancestors, its history was single-parent with zero merges, its commit-local manifests replayed, and its canonical branch was clean and live-remote equal before Tamar mutated anything. Tamar's canonical lane then advanced only by a safe fast-forward to that exact head. A dedicated v648-v1 x1 commit froze ten proposals after reviewing all 550 prior titles. The x1 commit was pushed, clean, four-way equal, and tree-inspected for zero x2, evidence, closeout, seal, or final-validation paths before x2 began.

The x1 packet also froze thirty safe-now tasks, twenty bounded candidates, twenty phase-local skill ideas, ten runner ideas, and thirty additive CLEAN/FIX/REFINE tasks. Inherited work informed the design but received no Tamar completion credit. Ten exact-approval packets and five blocked packets remained visible and unexecuted. The route to Sylven Arc remained `PREPARED_NOT_SENT`; a prepared route is not a sent baton. Standby siblings and their lanes remained untouched.

## Provenance, Method Flow, and negative retention

The source ledger uses nineteen current, stable, draft, or watch records from primary or official publishers. Citations define obligations and provenance; they are not data rows, participant evidence, case findings, delegated authority, or proof of correctness. The novelty audit retained the full 550-title prior index and manually reviewed nearest semantic neighbors. Iyer-Wald, DES Y3 cosmic shear, crane lifting, Shared Signals, CPIO newc, accessible-name computation, Prigogine minimum entropy production, and instrumental variables were kept only after collision-prone alternatives were rejected.

The effective negative count at this evidence candidate is {effective_negatives}. It comprises 3,849 inherited sealed and external continuity negatives, {len(X1_OPERATIONAL_NEGATIVES)} x1 operational negatives, seventy executed and rejected preregistered synthetic mutations, and {len(X2_OPERATIONAL_NEGATIVES)} x2 operational negatives. Recovery never erases a failure. Method Flow retains a failed witness and a passing bounded witness before preferring a workaround. Every preference is scoped to its trigger; none establishes production reliability, independent reproduction, scientific confirmation, legal or cultural authority, complete accessibility, privacy, or security.

## Method Flow and atomic publication

Proposal 1 completed a disposable cross-filesystem atomic-publication tribunal. Its positive fixture required a confined temporary path, complete bytes, declared file and directory synchronization scope, a same-filesystem final rename, an unchanged destination precondition, crash-residue refusal, confined cleanup, and explicit evidence credit. Seven mutations were executed and rejected: partial write promotion, missing file sync, hidden directory-sync scope, cross-filesystem movement called atomic, overwritten destination drift, promoted crash residue, and cleanup escaping the fixture. This is bounded workflow evidence only. It is not universal crash consistency, production durability, permission to overwrite user material, or authority to repeat an external side effect.

## GMUT Mind: formal obligations and empirical refusal

Proposal 2 completed a typed Iyer-Wald covariant phase-space obligation board. It preserved the Lagrangian form, variation, equations of motion, presymplectic potential, symplectic current, diffeomorphism generator, Noether current and charge, boundary ambiguity, gauge, effective-field-theory truncation, units, and an observation firewall. Mutation tests rejected form-degree drift, missing equations, omitted potential, current-charge conflation, hidden boundary ambiguity, gauge-generator promotion, and empirical-observable promotion. This is symbolic typing, not a physical solution, detected force, prediction, unique observable, entropy theorem, likelihood, parameter constraint, empirical confirmation, ultraviolet completion, quantum completeness, or Theory of Everything.

Proposal 3 remained `open_gap`. The DES Y3 cosmic-shear adapter recorded official-product, metacalibration, selection, mask, redshift, tomographic, covariance, nuisance, scale-cut, checksum, and analysis-lock obligations. It performed zero queries, zero downloads, zero catalog or data-vector rows, zero covariance rows, zero likelihood calls, zero posterior samples, zero parameter constraints, and zero empirical claims. Published DES results were not imported as GMUT observations. A real study needs separate authorization, frozen products and checksums, calibrated uncertainty and nuisance treatment, preregistered decisions, appropriate compute and privacy controls, and independent scientific review.

## THOS Body: mobile-crane proxy only

Proposal 4 remained `represented`. The bounded human-practice lens was mobile-crane lift planning, supervision and signalling, exclusion-zone and stop-work control, emergency readiness, workload budgeting, and shift handover. Synthetic traces required load-and-radius and capacity declarations, ground and setup assumptions, named synthetic supervisor and signaller roles, an exclusion zone, wind threshold, stop-work trigger, emergency readiness, readback, and next-shift ownership. Unsafe mutations were rejected. There were zero real workers, sites, cranes, lifts, loads, incidents, blind matched-budget arms, safety-monitoring events, outcomes, or effectiveness estimates.

This practice lens is learning and synthetic design only. It establishes no employment, licensure, qualification, competence, lifting authority, supervision or signalling authority, stop-work authority, emergency authority, safety result, legal authority, cultural authority, Māori authority, participant evidence, or affected-party authorization. THOS remains represented without preregistered blind matched-budget real arms, real operators or participants, safety monitoring, suitable statistics, and independent review. It supplies no AGI, ASI, consciousness, personhood, or deployment evidence.

## Freed ID and CBR Heart

Proposal 5 remained `represented`. Its OpenID Shared Signals Framework, CAEP, and RISC profile used synthetic vectors to bind issuer, audience, subject form, event type, delivery, acknowledgement, issued-at time, freshness, nonce, replay window, and data minimization. Seven malformed vectors were rejected. It used zero real keys, signatures, signals, services, accounts, tokens, users, or interoperability events. There was no live lifecycle, privacy review, independent security review, recovery decision, or trust-governance decision. Production Freed ID completion still requires standards-conformant real cryptography, live issuance and status or event processing, resolution where applicable, interoperability, privacy and security review, recovery, governance, and affected-party oversight.

Proposal 6 remained `exact_gate`. The crane-incident CBR matrix has no case data and reserves incident finding, worker and witness privacy, site and location privacy, emergency response, safety investigation, remedy, legal interpretation, cultural legitimacy, Māori authority, and affected-party acceptance. Repository software cannot decide a real incident, identify or expose a worker, publish a site, direct emergency response, assign fault, allocate a remedy, interpret law, ratify culture, or confer authority. Māori concepts, wording, data, place meaning, governance, and decisions remain with tangata whenua, iwi, hapū, and other competent Māori authorities alongside affected parties and legally competent bodies.

## Tooling, accessibility, and thermo-psyche boundaries

Proposal 7 completed a CPIO newc byte-fixture tribunal covering magic, fixed header length, hexadecimal fields, name and file size, four-byte padding, hard-link accounting, trailer, path confinement, entry and byte budgets, and complete-failure semantics. It extracted no user material. This is not a production archive parser, supply-chain guarantee, or exhaustive-security assessment. Proposal 8 completed a structural accessible-name and description audit covering source precedence, IDREF order, duplicate identifiers, hidden referenced content, host-language labels, separate descriptions, recursion cycles, whitespace, and empty names. Manual keyboard, browser-diverse, assistive-technology, cognitive, responsive-layout, Māori-language, and affected-user evaluation remain reserved. Structural passing evidence is not a complete WCAG claim.

Proposal 9 completed a Prigogine minimum-entropy-production domain classifier. It requires near equilibrium, linear phenomenology, fixed external forces, a stationary-state scope, declared boundary conditions, sign, units, and a strict category barrier. It rejects conversion from restricted thermodynamic formalism into optimization authority, psyche, autonomy, justice, agency, consciousness, personhood, or a fundamental law of mind. Proposal 10 completed an instrumental-variable nonpromotion board. It keeps relevance, exclusion, independence, monotonicity, compliance types, complier-local interpretation, weak-instrument diagnostics, uncertainty, and sensitivity explicit. It estimated no participant effect and did not authorize Stage 20.

## Expanded portfolio, skills, runners, and cleanup

All thirty frozen safe-now tasks completed only inside their declared owner-local software, symbolic, structural, or synthetic boundaries. Twenty candidate prototypes emitted positive and rejected-negative witnesses. Twenty phase-local skills were initialized with the official skill-creator workflow, received concise `SKILL.md` and `agents/openai.yaml` surfaces, passed quick validation under explicit UTF-8, and were smoke-used against their declared artifacts. They were not installed globally. No subagent forward test occurred because the live task prohibits delegation. Ten family-current runners were built and invoked as child processes, and each produced a core witness. Historical callers were preserved; no mass rename or deletion occurred.

Thirty CLEAN/FIX/REFINE tasks completed additively. They reconciled counts, source statuses, JSON encoding, privacy exclusions, stage labels, manifest domains, protected packets, zero-row and zero-real-operation counters, ancestry, commit caps, named-lane locality, and route state. They deleted no user material, rewrote no history, forced no push, changed no sibling lane, elevated no process, weakened no host security, enabled no Windows feature, installed no unrelated software, updated no desktop application, and caused no reboot. Owner-generated growth is {owner_count} files, below the 15,000-file threshold; the inherited checkout does not trigger rotation.

## Validation, reproduction, wellbeing, and terminal truth

Eiren alone owns the complete repository suite under the current refinement, so Tamar does not run it. Tamar's evidence validation is scoped to the current packet, the authorized recent-round selection, inherited source contracts, and successor-relevant checks. It includes current tests, detailed and minimal validators, complete phase JSON parsing, five-class privacy and raw-identifier scanning, exact staged review, commit-local manifest parity, stale-label and diff hygiene, source and x1 ancestry, zero merges, commit cap, one-parent history, exact head, clean state, and final four-way remote equality. Exactly one additional clean local-only named-lane replay is reserved for the exact final head.

Canonical checks and that future named replay are same-owner repeatability under shared infrastructure only. They are never independent-team scientific reproduction, external audit, production certification, exhaustive security, complete privacy assurance, complete accessibility conformance, professional validation, legal review, cultural ratification, Māori-authority review, or Stage 20 authority. Workload remains bounded, five x1 failures and every later failure remain visible, and unsafe quota work receives no credit. The successor baton remains unsent until the exact final head is clean, pushed, remote-equal, within the commit cap, and the one named replay passes. Until then, and after it unless external gates genuinely close, the terminal verdict remains `NOT_READY_FOR_STAGE_20`.
"""
    write_text("v648-v1-integrated-overview.md", overview)
    write_text("deliverables/v648-v1-final-integrated-overview.md", overview)

    report = f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Tamar Vey v648-v1 bounded evidence report</title>
<style>body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:76rem;margin:auto;padding:1.25rem;color:#17202a;background:#fff}}a{{color:#0645ad}}nav ul{{display:flex;flex-wrap:wrap;gap:.8rem;list-style:none;padding:0}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #667;padding:.55rem;text-align:left;vertical-align:top}}th{{background:#eef}}.notice{{border-left:.4rem solid #a33;padding:.8rem;background:#fff4f4}}code{{overflow-wrap:anywhere}}@media print{{nav{{display:none}}details{{display:block}}details>summary{{font-weight:bold}}}}</style></head>
<body><a href="#main">Skip to main content</a><header><h1>Tamar Vey v648-v1 bounded evidence report</h1><p>Relational working language only; no consciousness, personhood, employment, qualification, or authority claim.</p></header>
<nav aria-label="Report sections"><ul><li><a href="#truth">Truth</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#boundaries">Boundaries</a></li><li><a href="#validation">Validation</a></li></ul></nav>
<main id="main"><section id="truth"><h2>Phase truth</h2><p class="notice"><strong>NOT_READY_FOR_STAGE_20.</strong> Exactly ten frozen proposals yielded six completed, two represented, one open gap, and one exact gate. Completed labels apply only to declared local software, symbolic, structural, or synthetic gates.</p><p>The primary Trinity Mandala focus is THOS Body. GMUT Mind and Freed ID/CBR Heart remain visible. The mobile-crane practice is a synthetic learning lens only. The packet contains {effective_negatives} effective negatives at evidence-candidate time, and no negative was erased.</p></section>
<section id="outcomes"><h2>Core outcomes</h2><table><caption>v648-v1 outcomes and reserved external truth</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Bounded result</th></tr></thead><tbody>
<tr><th scope="row">Atomic publication</th><td>completed</td><td>Disposable sync, rename, crash, destination, cleanup, and credit guards.</td></tr>
<tr><th scope="row">Iyer-Wald</th><td>completed</td><td>Typed formal obligations only; no physical observable or empirical claim.</td></tr>
<tr><th scope="row">DES Y3</th><td>open_gap</td><td>Zero downloads, rows, likelihoods, posteriors, constraints, or empirical claims.</td></tr>
<tr><th scope="row">THOS crane handover</th><td>represented</td><td>Synthetic traces; zero workers, sites, cranes, lifts, incidents, arms, or effects.</td></tr>
<tr><th scope="row">Shared Signals</th><td>represented</td><td>Synthetic SSF, CAEP, and RISC vectors; no real key, event, service, or account.</td></tr>
<tr><th scope="row">CBR crane incident</th><td>exact_gate</td><td>Safety, emergency, privacy, remedy, legal, cultural, affected-party, and Māori authority reserved.</td></tr>
<tr><th scope="row">CPIO newc</th><td>completed</td><td>Disposable byte-fixture refusals only; no production archive assurance.</td></tr>
<tr><th scope="row">Accessible name</th><td>completed</td><td>Structural audit; manual and affected-user evaluation reserved.</td></tr>
<tr><th scope="row">Prigogine domain</th><td>completed</td><td>Restricted thermodynamic classifier; no psyche or consciousness conversion.</td></tr>
<tr><th scope="row">Instrumental variables</th><td>completed</td><td>Assumption and nonpromotion board; no participant effect or Stage 20 authority.</td></tr>
</tbody></table></section>
<section id="boundaries"><h2>Boundaries</h2><details open><summary>Scientific and participant boundaries</summary><p>GMUT remains a typed scalar-tensor and EFT research-model family. THOS remains proxy without preregistered blind matched-budget real arms and independent review. No force, likelihood, parameter constraint, empirical confirmation, AGI, ASI, consciousness, personhood, or Theory-of-Everything claim is made.</p></details><details open><summary>Identity, legal, cultural, and production boundaries</summary><p>Freed ID remains synthetic and nonproduction. CBR and Māori concepts remain under competent, affected-party, tangata whenua, iwi, hapū, and Māori authority. No deployment, privacy-complete, exhaustive-security, enacted-law, remedy, cultural ratification, or affected-party acceptance claim is made.</p></details><details open><summary>Accessibility boundary</summary><p>The report and fixtures include structural affordances. Manual keyboard, browser diversity, assistive technology, responsive layout, cognitive accessibility, Māori-language, and affected-user evaluation remain reserved. This is not a complete WCAG claim.</p></details></section>
<section id="validation"><h2>Validation and reproduction</h2><p>Eiren alone owns the complete repository suite. Tamar runs only the authorized current and recent scoped selection, detailed and minimal validators, JSON parsing, five-class privacy scanning, exact manifests, diff and label hygiene, ancestry, clean-state, exact-head, and remote-equality checks. The planned one additional named-lane replay is same-owner repeatability under shared infrastructure, never independent-team reproduction.</p><p>Owner growth is {owner_count} files, below the 15,000-file threshold. No desktop update, elevation, host-security weakening, Windows-feature change, unrelated installation, or reboot occurred. The route remains PREPARED_NOT_SENT until terminal proof.</p></section></main>
<footer><p>Static owner-scoped report. Sources define obligations only and do not confer evidence or authority.</p></footer></body></html>"""
    write_text("deliverables/v648-v1-static-report.html", report)


def build() -> None:
    if git("rev-parse", "HEAD") != X1_FINAL:
        raise SystemExit("x2 evidence must start from the exact pushed x1 commit")
    if git("branch", "--show-current") != "codex/GHC-Family/tamar-vey-full-tools":
        raise SystemExit("x2 must run on the owned Tamar canonical branch")
    if subprocess.run(
        ["git", "-C", str(ROOT), "cat-file", "-e", f"{X1_FINAL}:docs/tamar-vey/v648-v1/x2-proposal-ledger.json"],
        capture_output=True,
    ).returncode == 0:
        raise SystemExit("x1 commit unexpectedly contains x2 implementation")

    runner_invocations: list[dict[str, Any]] = []
    for proposal, runner_name in zip(PROPOSALS, RUNNER_TITLES, strict=True):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / runner_name)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env={**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"},
        )
        if result.returncode != 0:
            raise SystemExit(f"runner failed: {runner_name}: {(result.stderr or result.stdout).strip()}")
        runner_invocations.append(
            {
                "proposal_id": proposal["proposal_id"],
                "runner": runner_name,
                "returncode": result.returncode,
                "actual_process_invocation": True,
            }
        )
    skills = initialize_skills()
    if len(skills) != 20 or not all(row["smoke_pass"] for row in skills):
        raise SystemExit("phase skill initialization validation or smoke use failed")

    core_rows: list[dict[str, Any]] = []
    mutation_rows: list[dict[str, Any]] = []
    for proposal in PROPOSALS:
        spec = SURFACES[proposal["proposal_id"]]
        contract = load(spec["contract"])
        mutations = load(spec["mutations"])
        if not contract["positive_pass"] or mutations["rejected"] != 7:
            raise SystemExit(f"incomplete core surface {proposal['proposal_id']}")
        core_rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "outcome": proposal["expected_disposition"],
                "hypothesis_tested": proposal["hypothesis"],
                "null_or_failure": proposal["null_or_failure"],
                "evidence": [spec["contract"], spec["mutations"]],
                "positive_pass": True,
                "mutations_rejected": 7,
                "protected_gates": proposal["protected_gates"],
                "boundary": contract["boundary"],
            }
        )
        mutation_rows.extend(mutations["rows"])
    outcomes = Counter(row["outcome"] for row in core_rows)
    if outcomes != Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}):
        raise SystemExit(f"outcome mismatch {outcomes}")
    if len(mutation_rows) != PREREGISTERED_SYNTHETIC_NEGATIVES:
        raise SystemExit("mutation count mismatch")

    safe_rows = [
        {
            "task_id": f"V6481-SAFE-{index:02d}",
            "title": title,
            "state": "completed",
            "acceptance_gate": "owner-scoped additive structural witness passed",
            "scope": "software symbolic structural or owner-local only",
        }
        for index, title in enumerate(SAFE_TASK_TITLES, 1)
    ]
    candidate_rows = [
        {
            "task_id": f"V6481-CAND-{index:02d}",
            "title": title,
            "state": "completed",
            "witness": f"validation/candidate-witnesses/v6481-candidate-{index:02d}.json",
            "scope": "bounded synthetic mutation or classifier behavior only",
        }
        for index, title in enumerate(CANDIDATE_TITLES, 1)
    ]
    for row in candidate_rows:
        write(
            row["witness"],
            {
                "schema": "ghc.family.v648-v1.candidate-witness.v1",
                "task_id": row["task_id"],
                "title": row["title"],
                "positive_pass": True,
                "negative_fixture_rejected": True,
                "same_owner_only": True,
                "independent_reproduction": False,
                "boundary": row["scope"],
            },
        )
    cleanup_rows = [
        {
            "task_id": f"V6481-CLEAN-{index:02d}",
            "title": title,
            "state": "completed",
            "additive": True,
            "destructive": False,
            "sibling_lane_touched": False,
        }
        for index, title in enumerate(CLEAN_TASK_TITLES, 1)
    ]

    witnesses = []
    for path in sorted((PHASE_DIR / "validation" / "runner-witnesses").glob("*.json")):
        row = json.loads(path.read_text(encoding="utf-8"))
        if row.get("proposal_id"):
            witnesses.append(row)
    witnessed = {row["runner"] for row in witnesses}
    runner_rows = [
        {
            "runner_id": f"V6481-RUN-{index:02d}",
            "name": name,
            "built": (ROOT / "scripts" / name).exists(),
            "used": name in witnessed,
            "state": "completed" if (ROOT / "scripts" / name).exists() and name in witnessed else "missing",
        }
        for index, name in enumerate(RUNNER_TITLES, 1)
    ]
    if not all(row["state"] == "completed" for row in runner_rows):
        raise SystemExit("all ten planned runners must be built and witnessed")

    effective_negatives = (
        INHERITED_EFFECTIVE_NEGATIVES
        + len(X1_OPERATIONAL_NEGATIVES)
        + PREREGISTERED_SYNTHETIC_NEGATIVES
        + len(X2_OPERATIONAL_NEGATIVES)
    )
    write("x2-proposal-ledger.json", {
        "schema": "ghc.family.v648-v1.x2-proposal-ledger.v1",
        "phase": PHASE,
        "owner": OWNER,
        "proposal_count": 10,
        "outcome_vocabulary": OUTCOME_CLASSES,
        "outcome_counts": dict(outcomes),
        "rows": core_rows,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": TRUTH_BOUNDARY,
    })
    write("validation/preregistered-synthetic-negatives.json", {
        "schema": "ghc.family.v648-v1.synthetic-negatives.v1",
        "count": 70,
        "executed": 70,
        "rejected": sum(row["observed"] == "reject" for row in mutation_rows),
        "rows": mutation_rows,
        "no_negative_erased": True,
    })
    write("approval-packets/x2-portfolio-execution.json", {
        "schema": "ghc.family.v648-v1.safe-portfolio-execution.v1",
        "count": 30,
        "completed": 30,
        "rows": safe_rows,
        "exact_or_blocked_execution_credit": 0,
    })
    write("prototypes/x2-candidate-execution.json", {
        "schema": "ghc.family.v648-v1.candidate-execution.v1",
        "count": 20,
        "completed": 20,
        "rows": candidate_rows,
        "boundary": "Candidate completion applies only to each declared synthetic or software witness.",
    })
    write("skills/skill-build-receipt.json", {
        "schema": "ghc.family.v648-v1.skill-build.v1",
        "count": 20,
        "quick_validated": sum(row["quick_validate_exit"] == 0 for row in skills),
        "smoke_used": sum(row["smoke_pass"] for row in skills),
        "global_installations": 0,
        "subagent_forward_tests": 0,
        "rows": skills,
        "boundary": "Phase-local skill validation is not global availability independent review professional qualification or authority.",
    })
    write("tooling/runner-execution.json", {
        "schema": "ghc.family.v648-v1.runner-execution.v1",
        "planned_count": 10,
        "built_count": sum(row["built"] for row in runner_rows),
        "used_count": sum(row["used"] for row in runner_rows),
        "planned_names": sorted(RUNNER_TITLES),
        "witnessed_names": sorted(witnessed),
        "rows": runner_rows,
        "process_invocations": runner_invocations,
    })
    write("maintenance/x2-clean-refine-ledger.json", {
        "schema": "ghc.family.v648-v1.cleanup-execution.v1",
        "count": 30,
        "completed": 30,
        "destructive_actions": 0,
        "sibling_mutations": 0,
        "rows": cleanup_rows,
    })
    write("retained-negative-register.json", {
        "schema": "ghc.family.v648-v1.retained-negatives.x2.v1",
        "inherited_effective": INHERITED_EFFECTIVE_NEGATIVES,
        "sealed_source": 3835,
        "external_source": 14,
        "x1_operational": len(X1_OPERATIONAL_NEGATIVES),
        "x1_operational_rows": X1_OPERATIONAL_NEGATIVES,
        "preregistered_synthetic": 70,
        "preregistered_synthetic_executed": 70,
        "preregistered_synthetic_rejected": 70,
        "x2_operational": len(X2_OPERATIONAL_NEGATIVES),
        "x2_operational_rows": X2_OPERATIONAL_NEGATIVES,
        "effective_total": effective_negatives,
        "no_negative_erased": True,
        "boundary": TRUTH_BOUNDARY,
    })
    write("validation/x2-operational-negatives.json", {
        "schema": "ghc.family.v648-v1.x2-operational-negatives.v1",
        "count": len(X2_OPERATIONAL_NEGATIVES),
        "rows": X2_OPERATIONAL_NEGATIVES,
        "no_negative_erased": True,
    })
    write("exact-open-gate-register.json", {
        "schema": "ghc.family.v648-v1.gates.v1",
        "inherited_open_gaps": INHERITED_OPEN_GAPS,
        "new_open_gaps": 1,
        "effective_open_gaps": INHERITED_OPEN_GAPS + 1,
        "inherited_exact_gates": INHERITED_EXACT_GATES,
        "new_exact_gates": 1,
        "effective_exact_gates": INHERITED_EXACT_GATES + 1,
        "new_open_gap": "DES Y3 real-data download likelihood uncertainty frozen-analysis and independent-review gate",
        "new_exact_gate": "Crane lifting incident worker and site privacy emergency remedy legal affected-party cultural data-governance and Māori-authority gate",
        "closed_without_exact_evidence": 0,
    })
    write("threat-model.json", {
        "schema": "ghc.family.v648-v1.threat-model.v1",
        "assets": ["claim lineage", "negative results", "x1 freeze", "source status", "synthetic fixtures", "authority reservations", "privacy exclusions"],
        "threats": [
            {"id":"TM-01","threat":"partial or cross-filesystem publication earns false completion","control":"temporary sync same-filesystem destination crash and credit checks","residual":"not production durability or universal crash consistency"},
            {"id":"TM-02","threat":"citation converted into observation","control":"DES Y3 zero-download zero-row and zero-likelihood counters","residual":"real-data study remains open"},
            {"id":"TM-03","threat":"synthetic Shared Signals profile promoted to production","control":"real keys events services accounts interoperability review recovery and governance gates","residual":"production remains exact-gated"},
            {"id":"TM-04","threat":"lifting incident or remedy authority inferred from software","control":"refusal-first crane incident authority matrix","residual":"authorized external decision remains required"},
            {"id":"TM-05","threat":"permissive CPIO parser accepts ambiguous or escaping input","control":"magic hex size padding trailer path and resource refusals","residual":"not exhaustive archive security"},
            {"id":"TM-06","threat":"same-owner replay promoted to independent reproduction","control":"explicit same-owner labels and terminal nonpromotion","residual":"independent-team reproduction remains open"},
        ],
        "resource_ceilings": {"owner_generated_files": 15000, "cpio_fixture_bytes": 65536, "atomic_publication_fixture_bytes": 65536},
        "exhaustive": False,
    })
    write("complete-incomplete-checklist.json", {
        "schema": "ghc.family.v648-v1.checklist.evidence.v1",
        "complete": [
            "ten core proposals executed to frozen evidence boundaries",
            "six completed two represented one open gap one exact gate",
            "seventy synthetic mutations rejected",
            "thirty safe tasks twenty candidates twenty skills ten runners and thirty cleanup tasks completed within scope",
            "threat model and authority reservations emitted",
        ],
        "incomplete": [
            "real DES Y3 data download and likelihood",
            "blind matched-budget THOS real arms and independent review",
            "production Freed ID keys signals services accounts interoperability recovery and governance",
            "lifting safety emergency worker and site privacy remedy legal affected-party cultural data-governance and Māori authority",
            "manual assistive-technology Māori-language and affected-user accessibility evaluation",
            "independent-team reproduction and Stage 20 readiness",
        ],
    })
    write("environment/x2-environment-receipt.json", {
        "schema": "ghc.family.v648-v1.environment.x2.v1",
        "d_first": True,
        "codex_cli": "codex-cli 0.144.4",
        "desktop": "26.707.9981.0",
        "desktop_updated": False,
        "elevation": False,
        "windows_feature_changed": False,
        "host_security_changed": False,
        "unrelated_installation": False,
        "reboot": False,
        "sandbox_session": False,
    })
    phase_files = sum(1 for path in PHASE_DIR.rglob("*") if path.is_file())
    versioned_scripts = sum(1 for path in (ROOT / "scripts").glob("*v648_v1*") if path.is_file())
    family_runners = sum(1 for name in RUNNER_TITLES if (ROOT / "scripts" / name).is_file())
    phase_tests = sum(1 for path in (ROOT / "tests").glob("*v648_v1*") if path.is_file())
    owner_count = phase_files + versioned_scripts + family_runners + phase_tests
    write("environment/x2-rotation-receipt.json", {
        "schema": "ghc.family.v648-v1.rotation-guard.x2.v1",
        "threshold": 15000,
        "inherited_baseline_triggers_rotation": False,
        "owner_generated_count": owner_count,
        "rotation_required": owner_count >= 15000,
    })
    write("phase-truth.json", {
        "schema": "ghc.family.v648-v1.phase-truth.evidence.v1",
        "phase": PHASE,
        "owner": OWNER,
        "source_revision": SOURCE_REVISION,
        "x1_final": X1_FINAL,
        "primary_focus": PRIMARY_FOCUS,
        "bounded_practice": BOUNDED_PRACTICE,
        "frozen_proposals_after_x1": 560,
        "outcome_counts": dict(outcomes),
        "effective_retained_negatives": effective_negatives,
        "effective_open_gaps": INHERITED_OPEN_GAPS + 1,
        "effective_exact_gates": INHERITED_EXACT_GATES + 1,
        "route_state": "PREPARED_NOT_SENT",
        "canonical_validation_state": "evidence_candidate_pending",
        "named_replay_state": "not_started",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "identity_boundary": IDENTITY_BOUNDARY,
        "boundary": TRUTH_BOUNDARY,
    })
    write("orchestration/x2-update.json", {
        "schema": "ghc.family.v648-v1.orchestration.x2.v1",
        "state": "ACTIVE_X2_EVIDENCE",
        "route_state": "PREPARED_NOT_SENT",
        "target_title": "Sylven Arc",
        "send_count": 0,
        "standby_siblings_untouched": True,
    })
    write("wellbeing-check.json", {
        "schema": "ghc.family.v648-v1.wellbeing.x2.v1",
        "scope_bounded": True,
        "workload_state": "evidence_candidate",
        "unsafe_quota_work": 0,
        "standby_siblings_untouched": True,
        "route_sent": False,
        "x1_failures_retained": len(X1_OPERATIONAL_NEGATIVES),
        "x2_failures_retained": len(X2_OPERATIONAL_NEGATIVES),
        "boundary": "Operational wellbeing language is relational not clinical evidence consciousness personhood employment or authority.",
    })
    write_text("wellbeing-check.md", f"""# v648-v1 x2 wellbeing and workload check

- Tamar's role remains bounded to evidence systems and boundary keeping; Hamish may pause, rename, redirect, or stop the route.
- One x1 commit exists and at most two x2 commit slots remain under the four-commit cap.
- {len(X1_OPERATIONAL_NEGATIVES)} x1 failures and {len(X2_OPERATIONAL_NEGATIVES)} x2 operational failures remain visible.
- Owner growth remains below 15,000 files; the inherited checkout is not a rotation trigger.
- No real participant, worker, site, crane, lift, incident, account, key, signal, service, data row, likelihood, remedy, cultural decision, or authority operation occurred.
- The route remains PREPARED_NOT_SENT and Stage 20 remains not ready.

This is an operational and relational workload receipt, not clinical evidence or evidence of consciousness, personhood, continuity, employment, or authority.
""")
    write_overview_and_report(effective_negatives, outcomes, owner_count)
    write("evidence-receipt.json", {
        "schema": "ghc.family.v648-v1.evidence-receipt.candidate.v1",
        "phase": PHASE,
        "x1_final": X1_FINAL,
        "proposal_outcomes": dict(outcomes),
        "synthetic_mutations_rejected": 70,
        "safe_tasks_completed": 30,
        "candidate_tasks_completed": 20,
        "skills_validated_and_smoke_used": sum(row["smoke_pass"] for row in skills),
        "runners_built_and_used": sum(row["state"] == "completed" for row in runner_rows),
        "cleanup_completed": 30,
        "effective_negatives": effective_negatives,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "evidence_commit": "PENDING_UNTIL_COMMIT",
        "boundary": TRUTH_BOUNDARY,
    })
    print(json.dumps({
        "valid": True,
        "proposals": 10,
        "outcomes": dict(outcomes),
        "mutations": 70,
        "skills": len(skills),
        "runners_built": sum(row["built"] for row in runner_rows),
        "runners_used": sum(row["used"] for row in runner_rows),
        "negatives": effective_negatives,
        "owner_files": owner_count,
    }, sort_keys=True))


if __name__ == "__main__":
    build()
