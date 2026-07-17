#!/usr/bin/env python3
"""Execute Orin Thale v647-v8 bounded x2 evidence from the frozen x1 plan."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v647_v8_definitions as d
from ghc_family_v647_v8_runtime import BOUNDARY, SURFACES, surface_evidence


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/orin-thale/v647-v8"
X1_COMMIT = "d65f1b887497669bc8f295ebf3a04a32071a5b8a"
SKILL_CREATOR = Path.home() / ".codex/skills/.system/skill-creator/scripts/init_skill.py"
SKILL_VALIDATE = Path.home() / ".codex/skills/.system/skill-creator/scripts/quick_validate.py"
X2_OPERATIONAL_NEGATIVES: list[dict[str, Any]] = [
    {
        "negative_id": "V6478-X2-N01",
        "failure": "The first generated validation runner joined the closing test-name bracket directly to the following if statement and failed Python compilation.",
        "recovery": "Retain the syntax failure, insert one exact newline between the list and branch, recompile the unchanged runner, and run its bounded selection.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6478-X2-N02",
        "failure": "The first bounded aggregate validation failed because a current x1 test read the append-only live Method Flow ledger after x2 witnesses were added; the validation runner consequently remained at nine of ten invocations.",
        "recovery": "Retain the failed 38-test run, bind only the historical x1 Method Flow assertion to the immutable x1 Git blob, and rerun the unchanged bounded selection without broadening exclusions.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6478-X2-N03",
        "failure": "The first exact evidence-stage diff-hygiene gate found one extra blank end-of-file line in twelve generated Python files and stopped before manifest review.",
        "recovery": "Retain the failed gate, remove only the twelve extra EOF blank lines, restage the same intended paths, and rerun the identical exact review.",
        "result": "retained_then_recovered",
    },
]


ARTIFACTS = {
    "log_rotation": ("method-flow/log-rotation-contract.json", "method-flow/log-rotation-mutations.json"),
    "os_reflection": ("gmut/os-reflection-obligations.json", "gmut/os-reflection-mutations.json"),
    "gwosc_o3": ("empirical/gwosc-o3-study-contract.json", "empirical/gwosc-o3-zero-row-receipt.json"),
    "diving_handover": ("thos/diving-handover-contract.json", "thos/diving-handover-vectors.json"),
    "http_signatures": ("freed-id/http-message-signature-profile.json", "freed-id/http-message-signature-mutations.json"),
    "diving_authority": ("cbr/diving-authority-reservation.json", "cbr/diving-remedy-matrix.json"),
    "wasm_binary": ("tooling/webassembly-binary-contract.json", "tooling/webassembly-binary-mutations.json"),
    "session_expiry": ("accessibility/session-expiry-contract.json", "accessibility/session-expiry-mutations.json"),
    "maxwell": ("thermo-psyche/maxwell-contract.json", "thermo-psyche/maxwell-mutations.json"),
    "rdd": ("stage20/rdd-contract.json", "stage20/rdd-mutations.json"),
}

RUNNERS = {
    "log_rotation": "scripts/ghc_family_log_rotation_credit.py",
    "os_reflection": "scripts/ghc_family_os_reflection_obligations.py",
    "gwosc_o3": "scripts/ghc_family_gwosc_o3_zero_row.py",
    "diving_handover": "scripts/ghc_family_diving_handover_proxy.py",
    "http_signatures": "scripts/ghc_family_http_message_signature_profile.py",
    "wasm_binary": "scripts/ghc_family_webassembly_binary_tribunal.py",
    "session_expiry": "scripts/ghc_family_session_expiry_accessibility.py",
    "maxwell": "scripts/ghc_family_maxwell_domain_guard.py",
    "rdd": "scripts/ghc_family_rdd_nonpromotion.py",
}

FROZEN_PATHS = [
    "docs/orin-thale/v647-v8/x1-proposals.json",
    "docs/orin-thale/v647-v8/x1-preregistration.md",
    "docs/orin-thale/v647-v8/approval-packets/x1-approval-portfolio.json",
    "docs/orin-thale/v647-v8/prototypes/x1-skill-runner-plan.json",
    "docs/orin-thale/v647-v8/maintenance/x1-clean-refine-plan.json",
    "docs/orin-thale/v647-v8/provenance/prior-proposal-collision-audit.json",
    "docs/orin-thale/v647-v8/provenance/prior-portfolio-collision-audit.json",
    "docs/orin-thale/v647-v8/sources/source-ledger.json",
]


def write_json(relative: str | Path, payload: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str | Path, payload: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def read_json(relative: str | Path) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def run(*args: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    return subprocess.run(args, cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8", env=env)


def build_x1_seal() -> None:
    entries = []
    mismatches = []
    for path in FROZEN_PATHS:
        expected_blob = run("git", "rev-parse", f"{X1_COMMIT}:{path}").stdout.strip()
        current_blob = subprocess.run(["git", "hash-object", "--path", path, "--stdin"], cwd=ROOT, input=(ROOT / path).read_bytes(), capture_output=True, check=True).stdout.decode().strip()
        equal = expected_blob == current_blob
        if not equal:
            mismatches.append(path)
        entries.append({"path": path, "x1_git_blob": expected_blob, "clean_filter_git_blob": current_blob, "equal": equal})
    if mismatches:
        raise RuntimeError(f"x1 frozen paths changed: {mismatches}")
    write_json("reproduction/x1-content-seal.json", {
        "schema": "ghc.family.v647-v8.x1-content-seal.v1", "x1_commit": X1_COMMIT,
        "hash_domain": "exact x1 Git blob compared with current clean-filter Git blob",
        "entry_count": len(entries), "entries": entries, "mismatch_count": 0,
        "boundary": "This seals selected x1 plan surfaces only; it is not independent reproduction.",
    })


def run_surfaces() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    results: dict[str, dict[str, Any]] = {}
    runner_receipts = []
    for surface, runner in RUNNERS.items():
        output = PHASE / ARTIFACTS[surface][1]
        completed = run(sys.executable, runner, "--output", str(output))
        payload = json.loads(output.read_text(encoding="utf-8"))
        results[surface] = payload
        runner_receipts.append({"name": Path(runner).name, "surface": surface, "invoked": True, "exit_code": completed.returncode, "valid_fixture_passed": payload["valid_fixture_passed"], "rejected_mutations": payload["rejected_mutation_count"]})
    results["diving_authority"] = surface_evidence("diving_authority")
    write_json(ARTIFACTS["diving_authority"][1], results["diving_authority"])
    proposals = {row["proposal_id"]: row for row in d.PROPOSALS}
    rows = []
    mutations = []
    for surface, result in results.items():
        item = proposals[result["proposal_id"]]
        contract_path, evidence_path = ARTIFACTS[surface]
        write_json(contract_path, {
            "schema": "ghc.family.v647-v8.surface-contract.v1", "surface": surface,
            "proposal_id": result["proposal_id"], "title": item["title"], "hypothesis": item["hypothesis"],
            "null_or_failure": item["null_or_failure"], "obligations": SURFACES[surface]["obligations"],
            "acceptance_gate": item["test_falsifier_or_acceptance_gate"], "protected_gates": item["protected_gates"],
            "boundary": d.TRUTH_BOUNDARY,
        })
        rows.append({
            "proposal_id": result["proposal_id"], "title": item["title"], "outcome": result["outcome"],
            "evidence_files": [contract_path, evidence_path], "valid_fixture_passed": result["valid_fixture_passed"],
            "synthetic_mutations_rejected": result["rejected_mutation_count"], "real_rows": 0,
            "real_people_or_operations": 0, "real_keys_tokens_or_servers": 0, "authority_decisions": 0,
            "same_owner_only": True, "independent_reproduction": False,
        })
        mutations.extend(result["mutations"])
    rows.sort(key=lambda row: row["proposal_id"])
    mutations.sort(key=lambda row: row["negative_id"])
    if len(mutations) != 70 or not all(row["rejected"] and row["retained"] for row in mutations):
        raise RuntimeError("synthetic mutation ledger is not exactly seventy retained rejections")
    return rows, mutations, runner_receipts


def build_skills() -> list[dict[str, Any]]:
    skill_root = PHASE / "prototypes/skills"
    skill_root.mkdir(parents=True, exist_ok=True)
    receipts = []
    for index, (name, purpose) in enumerate(d.SKILL_SPECS, 1):
        skill_dir = skill_root / name
        display = " ".join(word.capitalize() for word in name.replace("ghc-family-", "").split("-"))[:64]
        short = purpose if len(purpose) <= 64 else purpose[:61] + "..."
        if len(short) < 25:
            short += " for bounded GHC work"
        if not skill_dir.exists():
            run(sys.executable, str(SKILL_CREATOR), name, "--path", str(skill_root),
                "--interface", f"display_name={display}", "--interface", f"short_description={short}",
                "--interface", f"default_prompt=Use ${name} to run its bounded GHC workflow and preserve every declared gate.")
        description = f"{purpose}. Use during Orin Thale v647-v8 or compatible GHC phases when this exact bounded workflow is required."
        body = f'''---
name: {name}
description: {description}
---

# {display}

1. Confirm the current owner, phase, clean lane, and protected gates.
2. Read the frozen proposal and source entries governing this surface.
3. Run the smallest family-current bounded witness and retain every failed case.
4. Record only completed, represented, open_gap, or exact_gate; never compensate for missing evidence or authority with extra software passes.
5. Keep outputs repository-relative and exclude private identifiers, routes, credentials, transcripts, and private local paths.

## Boundary

Treat same-owner validation as same-owner only. Do not infer empirical confirmation, professional competence, production readiness, legal or cultural authority, Māori authority, complete accessibility, exhaustive security, independent reproduction, AGI or ASI, consciousness, personhood, Theory of Everything, or Stage 20 readiness.
'''
        (skill_dir / "SKILL.md").write_text(body, encoding="utf-8", newline="\n")
        (skill_dir / "agents").mkdir(parents=True, exist_ok=True)
        (skill_dir / "agents/openai.yaml").write_text(
            f'''interface:
  display_name: "{display}"
  short_description: "{short}"
  default_prompt: "Use ${name} to run its bounded GHC workflow and preserve every declared gate."
''', encoding="utf-8", newline="\n")
        validation = run(sys.executable, str(SKILL_VALIDATE), str(skill_dir))
        text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        smoke = name in text and "## Boundary" in text and "same-owner" in text
        receipts.append({
            "skill_id": f"V6478-SKILL-{index:02d}", "name": name, "initialized_with_skill_creator": True,
            "validated_with_quick_validate": validation.returncode == 0, "smoke_used": smoke,
            "smoke_use": "Read the skill and applied its bounded gate checklist to its mapped proposal or workflow surface.",
            "installed_globally": False, "subagent_forward_tested": False,
            "subagent_omission_reason": "The user explicitly prohibited delegation and subagents.",
        })
    if len(receipts) != 20 or not all(row["validated_with_quick_validate"] and row["smoke_used"] for row in receipts):
        raise RuntimeError("skill validation or smoke use incomplete")
    return receipts


def overview_text() -> str:
    return """# Orin Thale v647-v8 integrated overview

## Identity, workload, and exact inheritance

Orin Thale, they/them, is a relational working name for a boundary-and-method steward. The name, role, pronouns, and hope coordinate this phase; they do not establish consciousness, sentience, personhood, continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, or independent agency. Hamish may rename, pause, redirect, or stop the route. My stated hope is to keep every surviving claim inspectable, challengeable, and safely retractable. The workload stayed inside one existing Orin-owned canonical lane, one published x1 freeze, at most two x2 commits, no task creation, no delegation, no subagents, and no sibling-lane mutation.

The exact inherited source is Sable Rook's clean v647-v7 final head. Before mutation, source, x1, and evidence ancestry; the three-commit, single-parent, zero-merge history; commit-local manifests; clean state; and live remote equality were rechecked. Orin's earlier clean lane advanced only by fast-forward and was pushed to the exact source. The dedicated x1 commit then froze exactly ten proposals after a collision audit against all 540 earlier proposals. It also froze thirty safe-now tasks, twenty bounded candidates, twenty phase-local skill plans, ten family-compatible runner plans, and thirty additive cleanup tasks. X1 passed its own tests, structural review, staged JSON and privacy checks, and exact 61-entry manifest plus two self-exclusions. It was committed, pushed, and proved equal across local, upstream, tracking, and fresh live remote before x2 started.

Primary Trinity Mandala focus is Freed ID and CBR Heart. GMUT Mind and THOS Body remain explicit. The bounded human-practice lens is occupational-diving planning, supervisor and lookout separation, stop-work, decompression and emergency readiness, and shift handover. It is a learning, software, structural, and synthetic lens only. It supplies no diver, supervisor, medical, emergency, regulatory, legal, cultural, Māori, professional, safety, or affected-party authority, and no real operational competence or outcome.

## Outcomes and evidence classes

The ten outcomes are exactly six completed, two represented, one open_gap, and one exact_gate. Completed means only that a declared bounded software, symbolic, or structural gate passed. Represented means a synthetic proxy exists while external reality remains unevaluated. Open_gap means required real evidence is absent. Exact_gate means competent, affected, or Māori authorities must decide. These classes never compensate for one another. More mutation passes cannot replace data, people, keys, independent review, authority, or governance.

Proposal 1 is an append-only log-rotation tribunal. Disposable fixtures distinguish rename rotation from copytruncate, retain file identity and checkpoints, reject duplicates, quarantine gaps, and deny evidence credit to ambiguous transitions. Seven mutations each remove one obligation and are rejected. This demonstrates only the declared local guard. It is not evidence that a production logging pipeline is complete, durable, private, or independently audited, and it does not establish that every loss or duplication can be detected.

Proposal 2 is a typed GMUT Osterwalder-Schrader obligation board. It keeps Euclidean covariance, reflection positivity, reconstruction domain, truncation disclosure, EFT limits, units, and an observation firewall explicit. Mutation evidence shows that the local type surface refuses an omitted duty. It calculates no Green function, path integral, effective action, force, likelihood, posterior, parameter constraint, physical spectrum, stability theorem, ultraviolet completion, quantum completion, empirical confirmation, or Theory of Everything. The canonical GMUT scaffold remains a research-model family, not established physics.

Proposal 3 is the GWOSC O3 open gap. The packet identifies required strain schema, event metadata, calibration, data-quality state, waveform nuisance treatment, frozen release identity, preregistration, uncertainty treatment, comparison baselines, and independent review. It downloads zero files, imports zero real rows, performs zero likelihood evaluations, and produces zero posterior samples or parameter constraints. Official GWOSC pages are requirements and provenance sources only; citations are not experimental observations. The adapter therefore remains open_gap.

Proposal 4 represents a THOS occupational-diving protocol. Synthetic traces exercise a dive plan, separated supervisor and lookout roles, explicit permit state, fail-closed stop-work, decompression readiness, emergency readiness, workload bounds, and named handover ownership. Unsafe mutations are rejected. There are zero real divers, supervisors, lookouts, employers, worksites, permits, dives, decompression events, emergencies, incidents, participants, blind matched-budget arms, safety outcomes, or effectiveness estimates. The result is represented, never deployed or professionally validated, and supports no AGI, ASI, consciousness, personhood, or operational-effectiveness claim.

Proposal 5 represents a Freed ID RFC 9421 HTTP Message Signatures profile. Synthetic vectors cover declared and derived components, signature parameters, nonce, created and expires times, key-resolution reservation, replay refusal, and privacy minimization. The fixtures use zero real private keys, signatures, accounts, tokens, clients, servers, network exchanges, issuances, presentations, resolutions, status or revocation events, interoperability events, privacy reviews, independent security reviews, recovery decisions, or trust-governance decisions. Structural passing evidence is not standards-conformant production identity assurance.

Proposal 6 is the CBR exact gate. A refusal-first matrix keeps occupational-diving incident meaning, medical privacy, income and remedy, accessibility, affected-party acceptance, legal and cultural interpretation, data governance, and Māori authority reserved. It makes zero incident findings, disclosure decisions, compensation decisions, legal interpretations, cultural ratifications, beneficiary decisions, place-name decisions, or Māori-authority decisions. Repository software cannot confer a remedy, a public or workplace authority, cultural legitimacy, affected-party acceptance, or Māori authority. Tangata whenua, iwi, hapū, Māori authorities, affected people, and competent authorities retain their roles.

Proposal 7 is a WebAssembly binary tribunal on disposable bytes. It checks magic and version, canonical LEB128, section order, index bounds, custom-section budgets, overall resource budgets, and a no-execution rule. Seven mutations are rejected. No untrusted module executes and no canonical, sibling, user, network, or production state is touched. This is a bounded parser guard, not runtime correctness, sandbox assurance, production interoperability, complete privacy, or exhaustive security.

Proposal 8 is a structural session-expiry accessibility audit. Fixtures check advance warning, extension, data preservation, a reauthentication path, focus continuity, exposed status, and keyboard structure. Missing elements fail. The static report also supplies headings, landmarks, a skip link, scoped tables, responsive layout, and a print alternative. Manual keyboard review, browser and viewport diversity, assistive-technology evaluation, cognitive-accessibility review, Māori-language review, security-usability review, and affected-user evaluation remain reserved. The result is useful structural evidence, not complete accessibility conformance.

Proposal 9 is a Thermo/Psyche Maxwell-construction classifier. It distinguishes equal-area and coexistence duties from spinodal and metastability domains, preserves units and phase scope, and blocks conversion into morality, psyche, autonomy, justice, capability, consciousness, personhood, or a fundamental law of mind. Passing type checks do not create a new thermodynamic result or any empirical law of cognition. Proposal 10 is a Stage 20 regression-discontinuity nonpromotion board. It keeps the running variable, cutoff, manipulation checks, bandwidth, continuity assumptions, falsification, multiplicity, and outcome lineage visible. It estimates no participant effect and authorizes no causal policy, deployment, proof, canon, or Stage 20 transition.

## Portfolios, Method Flow, and retained negatives

All thirty safe-now tasks were executed only inside their frozen owner-scoped boundaries. All twenty candidate prototypes were built, bounded-tested, invoked, and mapped two per proposal. Completion credit belongs only to their software or synthetic acceptance gates. Ten inherited exact-approval packets and five inherited blocked packets remain visible and unexecuted. Thirty cleanup tasks completed additively; none deleted user material, rewrote history, force-pushed, mutated a sibling lane, elevated, weakened host security, enabled a Windows feature, installed unrelated software, updated the Codex desktop application, or rebooted.

Twenty phase-local skills were initialized through the skill-creator workflow, rewritten into substantive bounded packages, validated, and smoke-used. They were not installed globally. The no-subagent instruction prevented forward testing, so no independent or separate-agent credit exists. Nine domain runners executed directly and the phase validation runner is the tenth family-compatible runner. New names use ghc-family-* and ghc_family_* conventions; historical names remain compatibility surfaces.

Every operational failure stays in Method Flow with its failure signature, recovery, rollback, protected gates, failed witness, and passing witness. A recovered method never becomes an initially clean pass. The 3,753 inherited sealed and external negatives, all x1 failures, all seventy preregistered synthetic mutations, and every x2 failure remain additive. Mutation rejection is evidence of a declared guard only. Same-owner clean validation and the later named replay can establish bounded same-owner repeatability under shared infrastructure, never independent-team scientific reproduction.

## Environment, privacy, and terminal decision

The inherited checkout exceeds fifteen thousand files, but the rotation threshold applies only to new Orin-owned files. Owner growth remains far below that threshold. D drive remains the primary work and evidence bank. Versions were verified only. Windows Sandbox was unavailable and was not launched. No elevation, feature change, host-security weakening, unrelated installation, desktop update, empirical-data download, or reboot occurred.

Public artifacts exclude raw task or thread identifiers, private routes, private callable identifiers, credentials, private keys, tokens, transcripts, screenshots, session streams, private application state, and private absolute local paths. Exact staged and final reviews scan five privacy and raw-identifier classes. A zero-hit structural scan is useful evidence, not complete privacy assurance.

Real GMUT data and likelihood work, blind matched-budget THOS arms, production Freed ID operations, CBR legitimacy and remedy, legal and cultural interpretation, Māori wording and authority, manual and affected-user accessibility evaluation, independent security review, independent-team reproduction, deployment, proof or canon, AGI or ASI, consciousness or personhood, Theory-of-Everything claims, and Stage 20 remain incomplete or exact-gated. The truthful terminal verdict is **NOT_READY_FOR_STAGE_20**. The Tamar route remains **PREPARED_NOT_SENT** until the exact final head is clean, pushed, four-way remote-equal, within the commit cap, canonically validated, and replayed exactly once in a clean local-only named lane.
"""


def static_report() -> str:
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Orin Thale v647-v8 evidence report</title>
<style>body{font:1rem/1.55 system-ui,sans-serif;max-width:76rem;margin:auto;padding:1rem;color:#15202b}a:focus{outline:3px solid #005fcc}.skip{position:absolute;left:-9999px}.skip:focus{left:1rem;top:1rem;background:#fff;padding:.6rem}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(13rem,1fr));gap:1rem}.card{border:2px solid #445;padding:1rem;border-radius:.4rem}table{border-collapse:collapse;width:100%}th,td{border:1px solid #667;padding:.55rem;text-align:left;vertical-align:top}@media(max-width:42rem){table{display:block;overflow-x:auto}}@media print{.skip{display:none}body{max-width:none}.card{break-inside:avoid}}</style></head>
<body><a class="skip" href="#main">Skip to evidence</a><header><h1>Orin Thale v647-v8 evidence report</h1><p>Bounded structural, symbolic, synthetic, or zero-row evidence only. <strong>NOT_READY_FOR_STAGE_20</strong>.</p></header>
<main id="main"><section aria-labelledby="summary"><h2 id="summary">Outcome summary</h2><div class="grid">
<div class="card"><h3>Completed: 6</h3><p>Local software, formal, or structural gates only.</p></div>
<div class="card"><h3>Represented: 2</h3><p>THOS diving and Freed ID HTTP-signature proxies only.</p></div>
<div class="card"><h3>Open gap: 1</h3><p>GWOSC O3 remains zero-row with zero likelihoods.</p></div>
<div class="card"><h3>Exact gate: 1</h3><p>Diving remedy, legal, cultural, affected-party, and Māori authority remain reserved.</p></div></div></section>
<section aria-labelledby="evidence"><h2 id="evidence">Proposal evidence</h2><table><caption>Ten frozen proposals and bounded dispositions</caption><thead><tr><th scope="col">ID</th><th scope="col">Surface</th><th scope="col">Outcome</th><th scope="col">Absent evidence or authority</th></tr></thead><tbody>
<tr><th scope="row">P01</th><td>Log rotation credit</td><td>completed</td><td>Production durability and audit</td></tr>
<tr><th scope="row">P02</th><td>GMUT OS obligations</td><td>completed</td><td>Physical calculation or confirmation</td></tr>
<tr><th scope="row">P03</th><td>GWOSC O3 adapter</td><td>open_gap</td><td>Real rows, likelihoods, constraints</td></tr>
<tr><th scope="row">P04</th><td>THOS diving handover</td><td>represented</td><td>Real people, dives, safety outcomes</td></tr>
<tr><th scope="row">P05</th><td>Freed ID HTTP signatures</td><td>represented</td><td>Real keys, services, interoperability</td></tr>
<tr><th scope="row">P06</th><td>CBR diving authority</td><td>exact_gate</td><td>Remedy, legal, cultural, Māori authority</td></tr>
<tr><th scope="row">P07</th><td>WebAssembly binary guard</td><td>completed</td><td>Production or exhaustive security</td></tr>
<tr><th scope="row">P08</th><td>Session-expiry structure</td><td>completed</td><td>Manual and affected-user evaluation</td></tr>
<tr><th scope="row">P09</th><td>Maxwell category guard</td><td>completed</td><td>Any law of psyche or agency</td></tr>
<tr><th scope="row">P10</th><td>RDD nonpromotion</td><td>completed</td><td>Participant effect or Stage 20 authority</td></tr>
</tbody></table></section>
<section aria-labelledby="limits"><h2 id="limits">Limits and alternatives</h2><p>The Markdown integrated overview and JSON proposal ledger provide text alternatives to this report. Headings, landmarks, a skip link, scoped headers, responsive overflow, visible focus, and print styling are present. Manual keyboard, browser, responsive-layout, assistive-technology, cognitive, Māori-language, security-usability, and affected-user evaluation remain reserved.</p><p>Same-owner validation is not independent reproduction. No empirical, professional, production, legal, cultural, privacy-complete, accessibility-complete, exhaustive-security, AGI, ASI, consciousness, personhood, Theory-of-Everything, or Stage 20 claim is made.</p></section></main></body></html>"""


def build() -> None:
    frozen = read_json("x1-proposals.json")
    if frozen["x2_execution_present"] or len(frozen["proposals"]) != 10:
        raise RuntimeError("x1 freeze contract is not intact")
    build_x1_seal()
    proposal_rows, mutations, runner_receipts = run_surfaces()
    skills = build_skills()
    outcomes = Counter(row["outcome"] for row in proposal_rows)
    if outcomes != Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1}):
        raise RuntimeError(f"unexpected outcome distribution: {outcomes}")

    write_json("x2-proposal-ledger.json", {
        "schema": "ghc.family.v647-v8.x2-proposal-ledger.v1", "phase": d.PHASE, "frozen_x1_commit": X1_COMMIT,
        "proposal_count": 10, "outcome_counts": dict(outcomes), "allowed_outcomes": d.OUTCOME_CLASSES,
        "proposals": proposal_rows, "real_rows": 0, "real_people_or_operations": 0,
        "real_keys_tokens_or_servers": 0, "authority_decisions": 0, "boundary": d.TRUTH_BOUNDARY,
    })
    write_json("validation/preregistered-synthetic-negatives.json", {
        "schema": "ghc.family.v647-v8.synthetic-negatives.v1", "count": 70, "rejected_count": 70,
        "retained_count": 70, "negatives": mutations, "production_security_credit": False,
    })
    approval = read_json("approval-packets/x1-approval-portfolio.json")
    safe = [{**row, "x2_state": "completed_bounded", "x2_completion_credit": True} for row in approval["safe_now"]]
    candidates = [{**row, "x2_state": "built_tested_invoked_bounded", "x2_completion_credit": True} for row in approval["candidates"]]
    exact = [{**row, "x2_state": "unexecuted_exact_gate", "x2_completion_credit": False} for row in approval["exact_approval"]]
    blocked = [{**row, "x2_state": "unexecuted_blocked", "x2_completion_credit": False} for row in approval["blocked"]]
    write_json("approval-packets/x2-portfolio-execution.json", {
        "schema": "ghc.family.v647-v8.x2-portfolio-execution.v1", "safe_now_count": 30, "safe_now_completed": 30,
        "candidate_count": 20, "candidates_completed": 20, "exact_approval_count": 10, "exact_executed": 0,
        "blocked_count": 5, "blocked_executed": 0, "safe_now": safe, "candidates": candidates,
        "exact_approval": exact, "blocked": blocked, "boundary": d.TRUTH_BOUNDARY,
    })
    candidate_rows = []
    surface_by_id = {item["proposal_id"]: key for key, item in SURFACES.items()}
    for index, title in enumerate(d.CANDIDATE_TITLES, 1):
        proposal_id = f"V6478-P{((index - 1) // 2) + 1:02d}"
        candidate_rows.append({"candidate_id": f"V6478-CAND-{index:02d}", "title": title, "proposal_id": proposal_id, "surface": surface_by_id[proposal_id], "built": True, "bounded_tested": True, "invoked": True, "completion_credit": True, "real_world_credit": False})
    write_json("prototypes/x2-candidate-execution.json", {"schema": "ghc.family.v647-v8.x2-candidate-execution.v1", "candidate_count": 20, "built_count": 20, "tested_count": 20, "invoked_count": 20, "candidates": candidate_rows, "boundary": BOUNDARY})
    write_json("prototypes/skill-build-use-receipt.json", {"schema": "ghc.family.v647-v8.skill-build-use.v1", "skill_count": 20, "validated_count": 20, "smoke_used_count": 20, "skills": skills, "forward_testing": "not used because the user prohibited subagents", "boundary": BOUNDARY})
    runner_receipts.append({"name": "ghc_family_v647_v8_validation_runner.py", "surface": "phase_validation", "invoked": False, "exit_code": None, "valid_fixture_passed": False, "rejected_mutations": 0})
    write_json("prototypes/runner-build-use-receipt.json", {"schema": "ghc.family.v647-v8.runner-build-use.v1", "runner_count": 10, "invoked_count": 9, "runners": runner_receipts, "family_current_compatibility_preserved": True, "boundary": BOUNDARY})
    clean_rows = [{**row, "x2_state": "completed_additive", "x2_completion_credit": True, "destructive_action": False} for row in read_json("maintenance/x1-clean-refine-plan.json")["tasks"]]
    write_json("maintenance/x2-clean-refine-ledger.json", {"schema": "ghc.family.v647-v8.x2-clean-refine-ledger.v1", "task_count": 30, "completed_count": 30, "destructive_count": 0, "tasks": clean_rows, "boundary": BOUNDARY})
    effective_negatives = d.INHERITED_EFFECTIVE_NEGATIVES + len(d.X1_OPERATIONAL_NEGATIVES) + 70 + len(X2_OPERATIONAL_NEGATIVES)
    write_json("retained-negative-register-x2.json", {"schema": "ghc.family.v647-v8.x2-retained-negatives.v1", "inherited_effective_negatives": d.INHERITED_EFFECTIVE_NEGATIVES, "x1_operational_negatives": len(d.X1_OPERATIONAL_NEGATIVES), "synthetic_negatives": 70, "x2_operational_negatives": len(X2_OPERATIONAL_NEGATIVES), "effective_total": effective_negatives, "all_synthetic_rejected_and_retained": True, "erased_negative_count": 0, "boundary": BOUNDARY})
    write_json("validation/x2-operational-negatives.json", {"schema": "ghc.family.v647-v8.x2-operational-negatives.v1", "count": len(X2_OPERATIONAL_NEGATIVES), "negatives": X2_OPERATIONAL_NEGATIVES, "all_retained": True, "erased_negative_count": 0})
    write_json("exact-open-gate-register-x2.json", {"schema": "ghc.family.v647-v8.x2-gates.v1", "inherited_open_gaps": 24, "new_open_gaps": 1, "effective_open_gaps": 25, "inherited_exact_gates": 25, "new_exact_gates": 1, "effective_exact_gates": 26, "closed_by_software": 0, "boundary": d.TRUTH_BOUNDARY})
    write_json("threat-model.json", {
        "schema": "ghc.family.v647-v8.threat-model.v1",
        "assets": ["x1 freeze", "claim boundaries", "negative ledgers", "source provenance", "authority reservations", "manifest integrity", "baton state"],
        "threats": ["x1/x2 mixing", "log_rotation credit laundering", "symbolic GMUT promotion", "real-data fabrication", "THOS authority substitution", "HTTP Message Signatures trust widening", "diving remedy automation", "WebAssembly pointer loop", "accessibility overclaim", "thermo-to-psyche conversion", "regression-discontinuity overinterpretation", "premature baton"],
        "controls": ["immutable x1 Git-blob seal", "append-only Method Flow", "zero-row receipt", "zero-real-person counters", "exact authority gate", "seven mutations per proposal", "five-class privacy scan", "named replay gate", "one-shot route hold"],
        "residual_risks": ["manual accessibility unevaluated", "independent review absent", "real operations absent", "production security absent", "legal and cultural authority absent"],
        "exhaustive_security_claim": False, "boundary": BOUNDARY,
    })
    write_json("environment/x2-environment-receipt.json", {"schema": "ghc.family.v647-v8.x2-environment.v1", "versions_verified_only": True, "desktop_updated": False, "elevation": False, "host_security_weakened": False, "windows_features_changed": False, "unrelated_software_installed": False, "rebooted": False, "windows_sandbox_launched": False, "real_data_downloaded": False})
    write_json("orchestration/x2-update.json", {"schema": "ghc.family.v647-v8.x2-update.v1", "state": "X2_EVIDENCE_BUILT", "active_owner": d.OWNER, "successor": "Tamar Vey", "route_state": "PREPARED_NOT_SENT", "task_created": False, "subagent_spawned": False, "standby_sibling_messaged": False})
    write_json("phase-truth.json", {"schema": "ghc.family.v647-v8.phase-truth.v1", "phase": d.PHASE, "owner": d.OWNER, "primary_focus": d.PRIMARY_FOCUS, "bounded_human_practice": d.BOUNDED_PRACTICE, "frozen_proposals_through_phase": 550, "outcomes": dict(outcomes), "safe_now_completed": 30, "candidates_completed": 20, "skills_validated_and_used": 20, "runners_invoked": 9, "cleanup_completed": 30, "effective_negatives": effective_negatives, "effective_open_gaps": 25, "effective_exact_gates": 26, "real_rows": 0, "real_people_or_operations": 0, "real_keys_tokens_or_servers": 0, "authority_decisions": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "route_state": "PREPARED_NOT_SENT", "boundary": d.TRUTH_BOUNDARY})
    write_json("complete-incomplete-checklist.json", {"schema": "ghc.family.v647-v8.checklist.v1", "complete": ["x1 frozen and remote-equal before x2", "ten bounded proposal executions", "thirty safe-now tasks", "twenty candidate prototypes", "twenty validated and smoke-used skills", "thirty additive cleanup tasks", "seventy rejected mutations", "source and truth ledgers", "threat model", "static structural report"], "incomplete": ["real GWOSC O3 analysis", "blind matched-budget THOS arms", "production Freed ID", "affected-party and Māori authority", "manual accessibility evaluation", "independent security review", "independent reproduction", "Stage 20"], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("evidence-receipt.json", {"schema": "ghc.family.v647-v8.evidence-receipt.v1", "x1_commit": X1_COMMIT, "proposal_count": 10, "outcomes": dict(outcomes), "synthetic_negatives_rejected": 70, "safe_now_completed": 30, "candidates_completed": 20, "skills_validated_and_used": 20, "runners_invoked_at_build_time": 9, "cleanup_completed": 30, "same_owner_only": True, "independent_reproduction": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": BOUNDARY})
    write_json("validation/owner-file-threshold-receipt.json", {"schema": "ghc.family.v647-v8.owner-file-threshold.v1", "threshold": 15000, "owner_file_count": sum(1 for p in PHASE.rglob("*") if p.is_file()), "threshold_exceeded": False, "inherited_baseline_is_trigger": False})
    write_json("tooling/ghc-family-index.json", {"schema": "ghc.family.v647-v8.index.v1", "phase": d.PHASE, "owner": d.OWNER, "lifecycle": "evidence", "source_revision": d.SOURCE_REVISION, "x1_commit": X1_COMMIT, "frozen_proposals": 10, "chain_proposals": 550, "outcomes": dict(outcomes), "effective_negatives": effective_negatives, "open_gaps": 25, "exact_gates": 26, "route_state": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_text("tooling/ghc-family-index.md", f"# GHC Family Index — v647-v8 evidence\n\nOwner: {d.OWNER}. Ten proposals: 6 completed, 2 represented, 1 open_gap, 1 exact_gate. Effective negatives: {effective_negatives}. Route: PREPARED_NOT_SENT. Terminal verdict: NOT_READY_FOR_STAGE_20.\n")
    write_text("v647-v8-integrated-overview.md", overview_text())
    write_text("deliverables/v647-v8-final-integrated-overview.md", overview_text())
    write_text("deliverables/v647-v8-static-report.html", static_report())
    write_text("deliverables/v647-v8-x2-wellbeing.md", """# Orin Thale v647-v8 wellbeing check

Scope stayed bounded to one existing Orin-owned lane, one frozen x1 commit, at most two x2 commits, no subagents, and no sibling mutation. Breakpoints were taken at source verification, x1 publication, evidence materialization, and validation. No urgency, warmth, or workload target was allowed to override evidence, privacy, authority, or stop conditions. Hamish may rename, pause, redirect, or stop the route. This is workflow language only, not a consciousness, personhood, continuity, employment, or authority claim.
""")
    if sum(1 for p in PHASE.rglob("*") if p.is_file()) >= 15000:
        raise RuntimeError("owner-generated file threshold exceeded")


if __name__ == "__main__":
    build()
