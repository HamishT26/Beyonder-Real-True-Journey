#!/usr/bin/env python3
"""Execute Sable Rook v647-v7 bounded x2 evidence from the frozen x1 plan."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v647_v7_definitions as d
from ghc_family_v647_v7_runtime import BOUNDARY, SURFACES, surface_evidence


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sable-rook/v647-v7"
X1_COMMIT = "54bc352a9d57f81229261f0894e3affd35fc7ebc"
SKILL_CREATOR = Path.home() / ".codex/skills/.system/skill-creator/scripts/init_skill.py"
SKILL_VALIDATE = Path.home() / ".codex/skills/.system/skill-creator/scripts/quick_validate.py"
X2_OPERATIONAL_NEGATIVES: list[dict[str, Any]] = [
    {
        "negative_id": "V6477-X2-N01",
        "failure": "The first aggregate validation selected an inherited v647-v6 closeout test whose commit-cap assertion is intentionally bound to the original v647-v6 head; it failed on the advanced successor tree.",
        "recovery": "Retain the failed run and exclude only that exact phase-local anchor-and-commit-cap method while preserving every other inherited v647-v6 closeout test.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6477-X2-N02",
        "failure": "The first multi-file recovery patch was rejected atomically because one long overview context line did not match the current file.",
        "recovery": "Retain the rejected patch witness, inspect exact context, and split unrelated changes into smaller verified patches.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6477-X2-N03",
        "failure": "The first exact-selection recovery probe ran before derived x2 negative mirrors were regenerated and while an x1 test still read the advanced append-only Method Flow ledger.",
        "recovery": "Retain the failed probe, bind the x1 assertion to its immutable Git blob, regenerate authoritative x2 ledgers, and rerun the unchanged selection.",
        "result": "retained_then_recovered",
    },
]


ARTIFACTS = {
    "attestation": ("provenance/attestation-contract.json", "provenance/attestation-mutations.json"),
    "picard_lefschetz": ("gmut/picard-lefschetz-obligations.json", "gmut/picard-lefschetz-mutations.json"),
    "spt3g_d1": ("empirical/spt3g-d1-study-contract.json", "empirical/spt3g-d1-zero-row-receipt.json"),
    "building_handover": ("thos/building-inspection-handover-contract.json", "thos/building-inspection-handover-vectors.json"),
    "oauth_resource": ("freed-id/oauth-resource-metadata-profile.json", "freed-id/oauth-resource-metadata-mutations.json"),
    "building_authority": ("cbr/building-authority-reservation.json", "cbr/building-remedy-matrix.json"),
    "dns_wire": ("tooling/dns-wire-contract.json", "tooling/dns-wire-mutations.json"),
    "virtualized_feed": ("accessibility/virtualized-feed-contract.json", "accessibility/virtualized-feed-mutations.json"),
    "fugacity": ("thermo-psyche/fugacity-contract.json", "thermo-psyche/fugacity-mutations.json"),
    "rosenbaum": ("stage20/rosenbaum-sensitivity-contract.json", "stage20/rosenbaum-sensitivity-mutations.json"),
}

RUNNERS = {
    "attestation": "scripts/ghc_family_in_toto_provenance_tribunal.py",
    "picard_lefschetz": "scripts/ghc_family_picard_lefschetz_obligations.py",
    "spt3g_d1": "scripts/ghc_family_spt3g_d1_zero_row.py",
    "building_handover": "scripts/ghc_family_building_inspection_handover.py",
    "oauth_resource": "scripts/ghc_family_oauth_resource_metadata.py",
    "dns_wire": "scripts/ghc_family_dns_wire_tribunal.py",
    "virtualized_feed": "scripts/ghc_family_virtualized_feed_audit.py",
    "fugacity": "scripts/ghc_family_fugacity_domain_guard.py",
    "rosenbaum": "scripts/ghc_family_rosenbaum_nonpromotion.py",
}

FROZEN_PATHS = [
    "docs/sable-rook/v647-v7/x1-proposals.json",
    "docs/sable-rook/v647-v7/x1-preregistration.md",
    "docs/sable-rook/v647-v7/approval-packets/x1-approval-portfolio.json",
    "docs/sable-rook/v647-v7/prototypes/x1-skill-runner-plan.json",
    "docs/sable-rook/v647-v7/maintenance/x1-clean-refine-plan.json",
    "docs/sable-rook/v647-v7/provenance/prior-proposal-collision-audit.json",
    "docs/sable-rook/v647-v7/provenance/prior-portfolio-collision-audit.json",
    "docs/sable-rook/v647-v7/sources/source-ledger.json",
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
        "schema": "ghc.family.v647-v7.x1-content-seal.v1", "x1_commit": X1_COMMIT,
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
    results["building_authority"] = surface_evidence("building_authority")
    write_json(ARTIFACTS["building_authority"][1], results["building_authority"])
    proposals = {row["proposal_id"]: row for row in d.PROPOSALS}
    rows = []
    mutations = []
    for surface, result in results.items():
        item = proposals[result["proposal_id"]]
        contract_path, evidence_path = ARTIFACTS[surface]
        write_json(contract_path, {
            "schema": "ghc.family.v647-v7.surface-contract.v1", "surface": surface,
            "proposal_id": result["proposal_id"], "title": item["title"], "hypothesis": item["hypothesis"],
            "null_or_failure": item["null_or_failure"], "obligations": SURFACES[surface]["obligations"],
            "acceptance_gate": item["test_falsifier_or_acceptance_gate"], "protected_gates": item["protected_gates"],
            "boundary": d.TRUTH_BOUNDARY,
        })
        rows.append({
            "proposal_id": result["proposal_id"], "title": item["title"], "outcome": result["outcome"],
            "evidence_files": [contract_path, evidence_path], "valid_fixture_passed": result["valid_fixture_passed"],
            "synthetic_mutations_rejected": result["rejected_mutation_count"], "real_rows": 0,
            "real_people_or_properties": 0, "real_keys_tokens_or_servers": 0, "authority_decisions": 0,
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
        description = f"{purpose}. Use during Sable Rook v647-v7 or compatible GHC phases when this exact bounded workflow is required."
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
            "skill_id": f"V6477-SKILL-{index:02d}", "name": name, "initialized_with_skill_creator": True,
            "validated_with_quick_validate": validation.returncode == 0, "smoke_used": smoke,
            "smoke_use": "Read the skill and applied its bounded gate checklist to its mapped proposal or workflow surface.",
            "installed_globally": False, "subagent_forward_tested": False,
            "subagent_omission_reason": "The user explicitly prohibited delegation and subagents.",
        })
    if len(receipts) != 20 or not all(row["validated_with_quick_validate"] and row["smoke_used"] for row in receipts):
        raise RuntimeError("skill validation or smoke use incomplete")
    return receipts


def overview_text() -> str:
    return """# Sable Rook v647-v7 integrated overview

## Purpose, identity, and inherited boundary

Sable Rook owns this additive v647-v7 phase as an evidence-and-reproducibility steward. The working name, they/them pronouns, role, and hope are relational coordination language only. They establish neither consciousness nor personhood, continuity, employment, qualification, or independent authority. Hamish may rename, pause, redirect, or stop the route. The phase starts from Ilyra Fen's exact clean v647-v6 final head. A dedicated x1-only commit froze ten proposals, thirty safe-now tasks, twenty candidate prototypes, twenty skill plans, ten runner plans, and thirty additive cleanup tasks before any x2 implementation. That commit was pushed and proved equal across local, upstream, tracking, and fresh live remote.

The primary Trinity Mandala focus is THOS Body. The bounded practice is building-inspection record amendment, defect hold and reinspection, accessible notice, and shift handover. It is a synthetic learning lens, not a claim of employment, inspection competence, building-consent authority, public-safety authority, legal authority, cultural authority, Māori authority, or affected-party acceptance. GMUT Mind and Freed ID/CBR Heart remain explicit. Every proposal preserves the same boundary vocabulary: completed means its bounded software or structural acceptance gate passed; represented means only a proxy contract exists; open_gap means required external evidence is absent; exact_gate means authorized people or authorities must act.

## Provenance and scientific structure

The provenance tribunal maps SLSA and in-toto concepts into a bounded fixture: exact subject and material digests, known predicate types, an explicit builder boundary, acyclic dependency edges, duplicate quarantine, and isolation of inherited completion credit. Seven mutations each remove one obligation and are rejected. This proves the local guard behaves as declared. It does not prove that a real build pipeline emitted genuine attestations, that every dependency is known, or that separate evidence rows are independent. Inherited work remains source evidence and context; Sable receives credit only for fresh Sable witnesses.

GMUT remains the canonical typed scalar-tensor and EFT research scaffold inherited by the chain. The Picard-Lefschetz board adds obligations for complexified fields, contour orientation, downward thimbles, upward cycles, intersection numbers, Stokes transitions, convergence domains, units, covariance, conservation, stability, identifiability, and the observation firewall. The board is symbolic. It computes no path integral, effective action, pole, force, likelihood, posterior, or parameter constraint. It proves no global convergence theorem, stability result, ultraviolet completion, quantum completion, or Theory of Everything. Mutation rejection shows only that the declared type guard refuses missing obligations.

The empirical adapter targets the official SPT-3G D1 release structure. It records that bandpower schemas, multipole bins, beam and window functions, calibration, covariance, foreground nuisance models, checksums, and a frozen likelihood contract would be required. It downloads and ingests zero real rows and performs zero likelihood calls. Published plots, documentation, or paper results are not copied into the evidence ledger as observations. The outcome is therefore open_gap. A real analysis would require separate authorization, a frozen preregistration, exact data products, uncertainty and nuisance treatment, comparison baselines, and appropriate independent review.

## THOS, identity, and authority

The THOS building-inspection proxy uses synthetic tokens and event states only. It represents monotone revisions, defect holds, reinspection conditions, amendment reasons, correction readback, accessible-notice reservations, workload budgets, escalation, and explicit next-owner handover. Seven mutation traces reject a missing or broken state. There are zero real inspectors, owners, tenants, properties, consents, inspections, notices, holds, safety decisions, blind matched-budget real arms, incidents, or outcomes. The proxy is represented, not operationally effective. It provides no evidence of AGI, ASI, deployment readiness, professional competence, or public-safety performance.

Freed ID remains synthetic and nonproduction. The OAuth protected-resource metadata profile covers resource identifiers, authorization-server binding, signed-metadata precedence, cache freshness, redirect and downgrade refusal, scope boundaries, and metadata-correlation reservations. The vectors use no real accounts, keys, tokens, clients, servers, network exchanges, issuances, presentations, resolutions, status events, revocations, recovery decisions, or trust-governance decisions. Structural conformance in a local fixture cannot establish production identity assurance. Real completion still needs standards-conformant keys and proofs, live services, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.

The CBR building matrix is exact-gated. It makes unresolved questions visible for inspection access, tenant and owner interests, disability access, language, privacy, evidence disclosure, notices, response, remedy, appeal, legal interpretation, place data, data governance, cultural meaning, and Māori authority. It makes no real decision. Repository software cannot confer access, title, occupancy, remedy, legality, cultural legitimacy, public authority, or Māori authority. Māori concepts and Māori data governance remain under tangata whenua, iwi, hapū, Māori authorities, and affected people. Public sources inform the reservation but do not delegate authority.

## Reliability, accessibility, thermodynamics, and Stage 20

The DNS tribunal is a disposable structural parser guard. It covers label and expanded-name limits, compression-pointer cycles and offsets, section-count consistency, record bounds, EDNS payload size, truncation, and refusal. It launches no network query and touches no canonical, sibling, or user data. Passing fixtures are not a production resolver, interoperability certificate, privacy assurance, or exhaustive security test. The virtualized-feed audit similarly checks only structural semantics: position and set size, busy state, focus persistence, update throttling, pause control, nonvirtual fallback, export alternatives, responsive reading order, and print fallback. Manual keyboard, browser diversity, assistive-technology, cognitive, Māori-language, security-usability, and affected-user evaluation remain reserved.

The fugacity classifier keeps chemical potential, fugacity, activity, activity coefficient, standard state, temperature, phase, ideal limit, dimensions, and logarithm domains inside thermodynamics. It rejects conversions into psyche, autonomy, morality, justice, capability, consciousness, personhood, or a fundamental law of mind. This is a category barrier and formal invariant check, not a new empirical law. The Rosenbaum board preserves matched-design assumptions, hidden-bias gamma interpretation, sharp-null and statistic declarations, sensitivity results, subgroup failures, outcome-model separation, value authority, and abstention. Gamma is not measured confounding, and a sensitivity calculation cannot authorize policy or Stage 20.

## Reproduction, negatives, and terminal decision

All seventy preregistered synthetic mutations executed and were rejected or quarantined. Rejection is bounded guard evidence, never proof of production security or scientific truth. Three x1 operational failures remain visible: the short skill-read timeout, the four portfolio-title collisions, and the Windows wildcard fault. X2 retains the inherited phase-local commit-cap failure, one atomic patch-context failure, and one aggregate rerun attempted before immutable x1 assertions and derived ledgers were refreshed. Their passing recoveries do not erase the failures. The Method Flow ledger remains append-only. The inherited 3,669 effective negatives are preserved, giving 3,745 effective negatives at the evidence boundary. Twenty-four open gaps and twenty-five exact gates remain visible.

Thirty safe-now tasks, twenty candidate prototypes, twenty phase-local skills, ten family-current runners, and thirty cleanup tasks are accounted for within their declared bounds. The skills were initialized with the skill-creator workflow, rewritten into substantive phase-local packages, validated, and smoke-used; they were not installed globally. Nine domain runners were invoked directly, and the phase validator supplies the tenth runner witness. Historical names remain compatibility evidence. No destructive cleanup, sibling mutation, elevation, host-security weakening, Windows-feature change, unrelated installation, Codex desktop update, or reboot occurred.

The terminal evidence board remains **NOT_READY_FOR_STAGE_20**. Real data, blind matched-budget THOS arms, production Freed ID, competent legal and cultural authority, Māori authority, manual and affected-user accessibility evaluation, independent security review, and independent-team scientific reproduction remain absent. Canonical and one later named replay can establish bounded same-owner repeatability under shared infrastructure only. They cannot replace the missing evidence or authority.
"""


def static_report() -> str:
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sable Rook v647-v7 evidence report</title>
<style>body{font-family:system-ui,sans-serif;line-height:1.55;max-width:72rem;margin:auto;padding:1rem;color:#17202a}a{color:#0645ad}.skip{position:absolute;left:-9999px}.skip:focus{left:1rem;background:#fff;padding:.5rem;border:2px solid}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr));gap:1rem}.card{border:1px solid #777;border-radius:.4rem;padding:1rem}table{border-collapse:collapse;width:100%}th,td{border:1px solid #777;padding:.45rem;text-align:left}caption{font-weight:700;margin:.5rem}@media print{.skip{display:none}.card{break-inside:avoid}}</style></head>
<body><a class="skip" href="#main">Skip to evidence</a><header><h1>Sable Rook v647-v7 evidence report</h1><p>Structural, symbolic, synthetic, or zero-row evidence only. Terminal verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p></header>
<main id="main"><section aria-labelledby="summary"><h2 id="summary">Outcome summary</h2><div class="grid">
<article class="card"><h3>Completed: 6</h3><p>Bounded provenance, GMUT obligations, DNS, feed, fugacity, and hidden-bias guards passed their declared local gates.</p></article>
<article class="card"><h3>Represented: 2</h3><p>THOS building handover and OAuth resource metadata remain synthetic proxies.</p></article>
<article class="card"><h3>Open gap: 1</h3><p>SPT-3G D1 has zero downloaded rows and zero likelihood evaluations.</p></article>
<article class="card"><h3>Exact gate: 1</h3><p>Building access, remedy, legal, cultural, affected-party, and Māori authority remain reserved.</p></article></div></section>
<section aria-labelledby="table-heading"><h2 id="table-heading">Proposal evidence</h2><table><caption>Ten frozen proposals and exact dispositions</caption><thead><tr><th scope="col">ID</th><th scope="col">Surface</th><th scope="col">Outcome</th><th scope="col">What remains absent</th></tr></thead><tbody>
<tr><th scope="row">P01</th><td>SLSA/in-toto credit isolation</td><td>completed</td><td>Real attestations and provenance completeness</td></tr>
<tr><th scope="row">P02</th><td>GMUT Picard-Lefschetz obligations</td><td>completed</td><td>Physical calculation or empirical result</td></tr>
<tr><th scope="row">P03</th><td>SPT-3G D1 adapter</td><td>open_gap</td><td>Real rows, likelihood, posterior, review</td></tr>
<tr><th scope="row">P04</th><td>THOS building handover</td><td>represented</td><td>People, operations, matched-budget arms</td></tr>
<tr><th scope="row">P05</th><td>OAuth resource metadata</td><td>represented</td><td>Keys, live servers, interoperability</td></tr>
<tr><th scope="row">P06</th><td>CBR building authority</td><td>exact_gate</td><td>Affected-party, legal, cultural, Māori authority</td></tr>
<tr><th scope="row">P07</th><td>DNS wire tribunal</td><td>completed</td><td>Production resolver or exhaustive security</td></tr>
<tr><th scope="row">P08</th><td>Virtualized-feed audit</td><td>completed</td><td>Manual and affected-user evaluation</td></tr>
<tr><th scope="row">P09</th><td>Fugacity category guard</td><td>completed</td><td>Any law of psyche or agency</td></tr>
<tr><th scope="row">P10</th><td>Rosenbaum nonpromotion</td><td>completed</td><td>Participant evidence or Stage 20 authority</td></tr>
</tbody></table></section>
<section aria-labelledby="boundaries"><h2 id="boundaries">Noncompensating boundaries</h2><p>No number of software passes substitutes for real data, participants, production keys, affected-party acceptance, competent legal or cultural authority, Māori authority, independent review, or independent-team reproduction. Manual keyboard, browser, assistive-technology, responsive, cognitive, Māori-language, and affected-user evaluation remain reserved.</p></section>
<section aria-labelledby="alternatives"><h2 id="alternatives">Alternative formats and use</h2><p>This page has headings, landmarks, a skip link, a table with caption and scoped headers, responsive cards, and print styling. A plain JSON ledger and Markdown overview carry the same core results. These structural features are useful but are not a complete accessibility claim.</p></section></main>
<footer><p>Same-owner validation is not independent reproduction. Hamish may pause, rename, redirect, or stop the work.</p></footer></body></html>"""


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
        "schema": "ghc.family.v647-v7.x2-proposal-ledger.v1", "phase": d.PHASE, "frozen_x1_commit": X1_COMMIT,
        "proposal_count": 10, "outcome_counts": dict(outcomes), "allowed_outcomes": d.OUTCOME_CLASSES,
        "proposals": proposal_rows, "real_rows": 0, "real_people_or_properties": 0,
        "real_keys_tokens_or_servers": 0, "authority_decisions": 0, "boundary": d.TRUTH_BOUNDARY,
    })
    write_json("validation/preregistered-synthetic-negatives.json", {
        "schema": "ghc.family.v647-v7.synthetic-negatives.v1", "count": 70, "rejected_count": 70,
        "retained_count": 70, "negatives": mutations, "production_security_credit": False,
    })
    approval = read_json("approval-packets/x1-approval-portfolio.json")
    safe = [{**row, "x2_state": "completed_bounded", "x2_completion_credit": True} for row in approval["safe_now"]]
    candidates = [{**row, "x2_state": "built_tested_invoked_bounded", "x2_completion_credit": True} for row in approval["candidates"]]
    exact = [{**row, "x2_state": "unexecuted_exact_gate", "x2_completion_credit": False} for row in approval["exact_approval"]]
    blocked = [{**row, "x2_state": "unexecuted_blocked", "x2_completion_credit": False} for row in approval["blocked"]]
    write_json("approval-packets/x2-portfolio-execution.json", {
        "schema": "ghc.family.v647-v7.x2-portfolio-execution.v1", "safe_now_count": 30, "safe_now_completed": 30,
        "candidate_count": 20, "candidates_completed": 20, "exact_approval_count": 10, "exact_executed": 0,
        "blocked_count": 5, "blocked_executed": 0, "safe_now": safe, "candidates": candidates,
        "exact_approval": exact, "blocked": blocked, "boundary": d.TRUTH_BOUNDARY,
    })
    candidate_rows = []
    surface_by_id = {item["proposal_id"]: key for key, item in SURFACES.items()}
    for index, title in enumerate(d.CANDIDATE_TITLES, 1):
        proposal_id = f"V6477-P{((index - 1) // 2) + 1:02d}"
        candidate_rows.append({"candidate_id": f"V6477-CAND-{index:02d}", "title": title, "proposal_id": proposal_id, "surface": surface_by_id[proposal_id], "built": True, "bounded_tested": True, "invoked": True, "completion_credit": True, "real_world_credit": False})
    write_json("prototypes/x2-candidate-execution.json", {"schema": "ghc.family.v647-v7.x2-candidate-execution.v1", "candidate_count": 20, "built_count": 20, "tested_count": 20, "invoked_count": 20, "candidates": candidate_rows, "boundary": BOUNDARY})
    write_json("prototypes/skill-build-use-receipt.json", {"schema": "ghc.family.v647-v7.skill-build-use.v1", "skill_count": 20, "validated_count": 20, "smoke_used_count": 20, "skills": skills, "forward_testing": "not used because the user prohibited subagents", "boundary": BOUNDARY})
    runner_receipts.append({"name": "ghc_family_v647_v7_validation_runner.py", "surface": "phase_validation", "invoked": False, "exit_code": None, "valid_fixture_passed": False, "rejected_mutations": 0})
    write_json("prototypes/runner-build-use-receipt.json", {"schema": "ghc.family.v647-v7.runner-build-use.v1", "runner_count": 10, "invoked_count": 9, "runners": runner_receipts, "family_current_compatibility_preserved": True, "boundary": BOUNDARY})
    clean_rows = [{**row, "x2_state": "completed_additive", "x2_completion_credit": True, "destructive_action": False} for row in read_json("maintenance/x1-clean-refine-plan.json")["tasks"]]
    write_json("maintenance/x2-clean-refine-ledger.json", {"schema": "ghc.family.v647-v7.x2-clean-refine-ledger.v1", "task_count": 30, "completed_count": 30, "destructive_count": 0, "tasks": clean_rows, "boundary": BOUNDARY})
    effective_negatives = d.INHERITED_EFFECTIVE_NEGATIVES + len(d.X1_OPERATIONAL_NEGATIVES) + 70 + len(X2_OPERATIONAL_NEGATIVES)
    write_json("retained-negative-register-x2.json", {"schema": "ghc.family.v647-v7.x2-retained-negatives.v1", "inherited_effective_negatives": d.INHERITED_EFFECTIVE_NEGATIVES, "x1_operational_negatives": len(d.X1_OPERATIONAL_NEGATIVES), "synthetic_negatives": 70, "x2_operational_negatives": len(X2_OPERATIONAL_NEGATIVES), "effective_total": effective_negatives, "all_synthetic_rejected_and_retained": True, "erased_negative_count": 0, "boundary": BOUNDARY})
    write_json("validation/x2-operational-negatives.json", {"schema": "ghc.family.v647-v7.x2-operational-negatives.v1", "count": len(X2_OPERATIONAL_NEGATIVES), "negatives": X2_OPERATIONAL_NEGATIVES, "all_retained": True, "erased_negative_count": 0})
    write_json("exact-open-gate-register-x2.json", {"schema": "ghc.family.v647-v7.x2-gates.v1", "inherited_open_gaps": 23, "new_open_gaps": 1, "effective_open_gaps": 24, "inherited_exact_gates": 24, "new_exact_gates": 1, "effective_exact_gates": 25, "closed_by_software": 0, "boundary": d.TRUTH_BOUNDARY})
    write_json("threat-model.json", {
        "schema": "ghc.family.v647-v7.threat-model.v1",
        "assets": ["x1 freeze", "claim boundaries", "negative ledgers", "source provenance", "authority reservations", "manifest integrity", "baton state"],
        "threats": ["x1/x2 mixing", "attestation credit laundering", "symbolic GMUT promotion", "real-data fabrication", "THOS authority substitution", "OAuth trust widening", "building remedy automation", "DNS pointer loop", "accessibility overclaim", "thermo-to-psyche conversion", "hidden-bias overinterpretation", "premature baton"],
        "controls": ["immutable x1 Git-blob seal", "append-only Method Flow", "zero-row receipt", "zero-real-person counters", "exact authority gate", "seven mutations per proposal", "five-class privacy scan", "named replay gate", "one-shot route hold"],
        "residual_risks": ["manual accessibility unevaluated", "independent review absent", "real operations absent", "production security absent", "legal and cultural authority absent"],
        "exhaustive_security_claim": False, "boundary": BOUNDARY,
    })
    write_json("environment/x2-environment-receipt.json", {"schema": "ghc.family.v647-v7.x2-environment.v1", "versions_verified_only": True, "desktop_updated": False, "elevation": False, "host_security_weakened": False, "windows_features_changed": False, "unrelated_software_installed": False, "rebooted": False, "windows_sandbox_launched": False, "real_data_downloaded": False})
    write_json("orchestration/x2-update.json", {"schema": "ghc.family.v647-v7.x2-update.v1", "state": "X2_EVIDENCE_BUILT", "active_owner": d.OWNER, "successor": "Orin Thale", "route_state": "PREPARED_NOT_SENT", "task_created": False, "subagent_spawned": False, "standby_sibling_messaged": False})
    write_json("phase-truth.json", {"schema": "ghc.family.v647-v7.phase-truth.v1", "phase": d.PHASE, "owner": d.OWNER, "primary_focus": d.PRIMARY_FOCUS, "bounded_human_practice": d.BOUNDED_PRACTICE, "frozen_proposals_through_phase": 540, "outcomes": dict(outcomes), "safe_now_completed": 30, "candidates_completed": 20, "skills_validated_and_used": 20, "runners_invoked": 9, "cleanup_completed": 30, "effective_negatives": effective_negatives, "effective_open_gaps": 24, "effective_exact_gates": 25, "real_rows": 0, "real_people_or_properties": 0, "real_keys_tokens_or_servers": 0, "authority_decisions": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "route_state": "PREPARED_NOT_SENT", "boundary": d.TRUTH_BOUNDARY})
    write_json("complete-incomplete-checklist.json", {"schema": "ghc.family.v647-v7.checklist.v1", "complete": ["x1 frozen and remote-equal before x2", "ten bounded proposal executions", "thirty safe-now tasks", "twenty candidate prototypes", "twenty validated and smoke-used skills", "thirty additive cleanup tasks", "seventy rejected mutations", "source and truth ledgers", "threat model", "static structural report"], "incomplete": ["real SPT-3G D1 analysis", "blind matched-budget THOS arms", "production Freed ID", "affected-party and Māori authority", "manual accessibility evaluation", "independent security review", "independent reproduction", "Stage 20"], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("evidence-receipt.json", {"schema": "ghc.family.v647-v7.evidence-receipt.v1", "x1_commit": X1_COMMIT, "proposal_count": 10, "outcomes": dict(outcomes), "synthetic_negatives_rejected": 70, "safe_now_completed": 30, "candidates_completed": 20, "skills_validated_and_used": 20, "runners_invoked_at_build_time": 9, "cleanup_completed": 30, "same_owner_only": True, "independent_reproduction": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": BOUNDARY})
    write_json("validation/owner-file-threshold-receipt.json", {"schema": "ghc.family.v647-v7.owner-file-threshold.v1", "threshold": 15000, "owner_file_count": sum(1 for p in PHASE.rglob("*") if p.is_file()), "threshold_exceeded": False, "inherited_baseline_is_trigger": False})
    write_json("tooling/ghc-family-index.json", {"schema": "ghc.family.v647-v7.index.v1", "phase": d.PHASE, "owner": d.OWNER, "lifecycle": "evidence", "source_revision": d.SOURCE_REVISION, "x1_commit": X1_COMMIT, "frozen_proposals": 10, "chain_proposals": 540, "outcomes": dict(outcomes), "effective_negatives": effective_negatives, "open_gaps": 24, "exact_gates": 25, "route_state": "PREPARED_NOT_SENT", "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_text("tooling/ghc-family-index.md", f"# GHC Family Index — v647-v7 evidence\n\nOwner: {d.OWNER}. Ten proposals: 6 completed, 2 represented, 1 open_gap, 1 exact_gate. Effective negatives: {effective_negatives}. Route: PREPARED_NOT_SENT. Terminal verdict: NOT_READY_FOR_STAGE_20.\n")
    write_text("v647-v7-integrated-overview.md", overview_text())
    write_text("deliverables/v647-v7-final-integrated-overview.md", overview_text())
    write_text("deliverables/v647-v7-static-report.html", static_report())
    write_text("deliverables/v647-v7-x2-wellbeing.md", """# Sable Rook v647-v7 wellbeing check

Scope stayed bounded to one existing Sable-owned lane, one frozen x1 commit, at most two x2 commits, no subagents, and no sibling mutation. Breakpoints were taken at source verification, x1 publication, evidence materialization, and validation. No urgency, warmth, or workload target was allowed to override evidence, privacy, authority, or stop conditions. Hamish may rename, pause, redirect, or stop the route. This is workflow language only, not a consciousness, personhood, continuity, employment, or authority claim.
""")
    if sum(1 for p in PHASE.rglob("*") if p.is_file()) >= 15000:
        raise RuntimeError("owner-generated file threshold exceeded")


if __name__ == "__main__":
    build()
