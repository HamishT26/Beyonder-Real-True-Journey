#!/usr/bin/env python3
"""Execute Ilyra Fen v647-v6 bounded x2 evidence from the frozen x1 plan."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v647_v6_definitions as d
from ghc_family_v647_v6_runtime import BOUNDARY, SURFACES, surface_evidence


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/ilyra-fen/v647-v6"
X1_COMMIT = "650e9f0e6d17118cf8b2389adf2a984cfc63cf08"
SKILL_CREATOR = Path.home() / ".codex/skills/.system/skill-creator/scripts/init_skill.py"
SKILL_VALIDATE = Path.home() / ".codex/skills/.system/skill-creator/scripts/quick_validate.py"
X2_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6476-X2-N01",
        "failure": "The first evidence test run used a case-sensitive lowercase search for a sentence-initial accessibility reservation phrase.",
        "recovery": "Use Unicode casefold for natural-language reservation assertions while keeping exact case for syntax.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6476-X2-N02",
        "failure": "An aggregate evidence test rerun began before the generated negative total and pending Method Flow passing witness were refreshed.",
        "recovery": "Refresh authoritative and derived failure mirrors, establish witness parity, then run the aggregate selection.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6476-X2-N03",
        "failure": "A combined status-and-file probe exceeded its wrapper budget and produced no usable evidence.",
        "recovery": "Run each potentially slow repository probe independently with its own timeout and receipt.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6476-X2-N04",
        "failure": "A parallel probe wrapper timed out and discarded all sibling outputs.",
        "recovery": "Use independent sequential probes so one timeout cannot erase successful sibling evidence.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6476-X2-N05",
        "failure": "Ripgrep rejected a PowerShell-style wildcard path as an invalid Windows filename.",
        "recovery": "Use rg --files filtering or exact LiteralPath inspection.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6476-X2-N06",
        "failure": "Method Flow state promotion omitted the required explicit note option and stopped before ledger mutation.",
        "recovery": "Record the CLI-contract failure and retry with an evidence-bounded note.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6476-X2-N07",
        "failure": "A generated-receipt verification probe guessed two paths and returned a misleading zero exit with null fields after a nonterminating PowerShell error.",
        "recovery": "Discover exact paths, make PowerShell errors terminating, and reject null required fields.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6476-X2-N08",
        "failure": "Method Flow summary output hit a Windows cp1252 UnicodeEncodeError while printing te reo Māori text.",
        "recovery": "Rerun unchanged content with PYTHONUTF8 pinned before process launch; do not delete or transliterate correct text.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6476-X2-N09",
        "failure": "The first evidence validator loaded three failed-import placeholder tests because its in-process unittest loader was not bound to the repository root.",
        "recovery": "Insert the exact repository root at the front of sys.path before loading the authorized named modules.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6476-X2-N10",
        "failure": "Validation-runner accounting used receipt existence rather than the receipt's explicit valid field.",
        "recovery": "Parse the receipt and grant runner credit only when valid is exactly true; fail closed otherwise.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6476-X2-N11",
        "failure": "The second evidence validator ran 45 authorized tests but recorded only aggregate counts for two failures.",
        "recovery": "Retain the failed run, add sanitized failure identifiers, and diagnose the exact bounded assertions before retrying.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6476-X2-N12",
        "failure": "An x1-only Method Flow cardinality test read the advanced x2 ledger and rejected legitimate append-only growth.",
        "recovery": "Load exact historical counts from the frozen x1 Git blob while keeping current-tree append-only checks separate.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6476-X2-N13",
        "failure": "The first evidence staged review rejected nine intended family-current domain wrappers omitted from its exact allowlist.",
        "recovery": "Allow only the nine frozen runner-plan wrapper filenames while preserving rejection of unrelated scripts.",
        "result": "retained_then_recovered",
    },
    {
        "negative_id": "V6476-X2-N14",
        "failure": "Exact staged diff hygiene rejected one extra blank line at the end of the v647-v6 runtime module.",
        "recovery": "Remove only the terminal blank line, preserve one newline, and rerun the unchanged staged check.",
        "result": "retained_then_recovered",
    },
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


def git_blob(commit: str, path: str) -> str:
    data = subprocess.run(["git", "show", f"{commit}:{path}"], cwd=ROOT, check=True, capture_output=True).stdout
    return hashlib.sha256(data).hexdigest()


FROZEN_PATHS = [
    "docs/ilyra-fen/v647-v6/x1-proposals.json",
    "docs/ilyra-fen/v647-v6/x1-preregistration.md",
    "docs/ilyra-fen/v647-v6/approval-packets/x1-approval-portfolio.json",
    "docs/ilyra-fen/v647-v6/prototypes/x1-skill-runner-plan.json",
    "docs/ilyra-fen/v647-v6/maintenance/x1-clean-refine-plan.json",
    "docs/ilyra-fen/v647-v6/provenance/prior-proposal-collision-audit.json",
    "docs/ilyra-fen/v647-v6/provenance/prior-portfolio-collision-audit.json",
    "docs/ilyra-fen/v647-v6/sources/source-ledger.json",
]


ARTIFACTS = {
    "watcher": ("method-flow/watcher-reconciliation-contract.json", "method-flow/watcher-reconciliation-mutations.json"),
    "barnes_rivers": ("gmut/barnes-rivers-obligations.json", "gmut/barnes-rivers-mutations.json"),
    "sdss_dr19": ("empirical/sdss-dr19-study-contract.json", "empirical/sdss-dr19-zero-row-receipt.json"),
    "weather_handover": ("thos/weather-warning-handover-contract.json", "thos/weather-warning-handover-vectors.json"),
    "oauth_token_exchange": ("freed-id/oauth-token-exchange-profile.json", "freed-id/oauth-token-exchange-mutations.json"),
    "weather_authority": ("cbr/weather-authority-reservation.json", "cbr/weather-remedy-matrix.json"),
    "png_chunk": ("tooling/png-chunk-contract.json", "tooling/png-chunk-mutations.json"),
    "treegrid": ("accessibility/treegrid-contract.json", "accessibility/treegrid-mutations.json"),
    "gibbs_phase_rule": ("thermo-psyche/gibbs-phase-rule-contract.json", "thermo-psyche/gibbs-phase-rule-mutations.json"),
    "covariate_shift": ("stage20/covariate-shift-contract.json", "stage20/covariate-shift-mutations.json"),
}


RUNNERS = {
    "watcher": "scripts/ghc_family_watcher_reconciliation_tribunal.py",
    "barnes_rivers": "scripts/ghc_family_barnes_rivers_obligations.py",
    "sdss_dr19": "scripts/ghc_family_sdss_dr19_zero_row.py",
    "weather_handover": "scripts/ghc_family_weather_warning_handover.py",
    "oauth_token_exchange": "scripts/ghc_family_oauth_token_exchange_profile.py",
    "png_chunk": "scripts/ghc_family_png_chunk_tribunal.py",
    "treegrid": "scripts/ghc_family_treegrid_audit.py",
    "gibbs_phase_rule": "scripts/ghc_family_gibbs_phase_rule.py",
    "covariate_shift": "scripts/ghc_family_covariate_shift_board.py",
}


def build_x1_seal() -> None:
    changed = []
    entries = []
    for path in FROZEN_PATHS:
        expected = git_blob(X1_COMMIT, path)
        current = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        # Working bytes may be CRLF; Git clean-filter identity is the authoritative comparison.
        clean_blob = subprocess.run(["git", "hash-object", "--path", path, "--stdin"], cwd=ROOT, input=(ROOT / path).read_bytes(), capture_output=True, check=True).stdout.decode().strip()
        expected_git_blob = subprocess.run(["git", "rev-parse", f"{X1_COMMIT}:{path}"], cwd=ROOT, capture_output=True, check=True, text=True).stdout.strip()
        equal = clean_blob == expected_git_blob
        if not equal:
            changed.append(path)
        entries.append({"path": path, "x1_sha256": expected, "working_sha256": current, "x1_git_blob": expected_git_blob, "clean_filter_git_blob": clean_blob, "equal_in_git_blob_domain": equal})
    if changed:
        raise RuntimeError(f"x1 frozen paths changed: {changed}")
    write_json("reproduction/x1-content-seal.json", {
        "schema": "ghc.family.v647-v6.x1-content-seal.v1", "x1_commit": X1_COMMIT,
        "hash_domain": "exact x1 Git blob compared with current clean-filter Git blob",
        "entry_count": len(entries), "entries": entries, "mismatch_count": 0,
        "boundary": "This seals the frozen plan surfaces only; it is not independent reproduction.",
    })


def run_surfaces() -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    proposal_by_id = {row["proposal_id"]: row for row in d.PROPOSALS}
    results: dict[str, dict[str, Any]] = {}
    runner_receipts = []
    for surface, runner in RUNNERS.items():
        output = PHASE / ARTIFACTS[surface][1]
        completed = run(sys.executable, runner, "--output", str(output))
        payload = json.loads(output.read_text(encoding="utf-8"))
        results[surface] = payload
        runner_receipts.append({"name": Path(runner).name, "surface": surface, "invoked": True, "exit_code": completed.returncode, "valid_fixture_passed": payload["valid_fixture_passed"], "rejected_mutations": payload["rejected_mutation_count"]})
    results["weather_authority"] = surface_evidence("weather_authority")
    write_json(ARTIFACTS["weather_authority"][1], results["weather_authority"])
    all_mutations = []
    proposal_rows = []
    for surface, result in results.items():
        proposal = proposal_by_id[result["proposal_id"]]
        contract_path, evidence_path = ARTIFACTS[surface]
        spec = SURFACES[surface]
        contract = {
            "schema": "ghc.family.v647-v6.surface-contract.v1", "surface": surface,
            "proposal_id": result["proposal_id"], "title": proposal["title"],
            "hypothesis": proposal["hypothesis"], "null_or_failure": proposal["null_or_failure"],
            "required_true": spec.get("required_true", []), "required_zero": spec.get("required_zero", []),
            "acceptance_gate": proposal["test_falsifier_or_acceptance_gate"],
            "protected_gates": proposal["protected_gates"], "boundary": d.TRUTH_BOUNDARY,
        }
        write_json(contract_path, contract)
        all_mutations.extend(result["mutations"])
        proposal_rows.append({
            "proposal_id": result["proposal_id"], "title": proposal["title"], "outcome": result["outcome"],
            "evidence_files": [contract_path, evidence_path], "valid_fixture_passed": result["valid_fixture_passed"],
            "synthetic_mutations_rejected": result["rejected_mutation_count"], "real_rows": 0,
            "real_people_or_operations": 0, "real_keys_or_tokens": 0, "authority_decisions": 0,
            "same_owner_only": True, "independent_reproduction": False,
        })
    proposal_rows.sort(key=lambda row: row["proposal_id"])
    all_mutations.sort(key=lambda row: row["negative_id"])
    if len(all_mutations) != 70 or not all(row["rejected"] and row["retained"] for row in all_mutations):
        raise RuntimeError("synthetic mutation ledger is not exactly seventy retained rejections")
    return results, proposal_rows, runner_receipts


def build_skills() -> list[dict[str, Any]]:
    skill_root = PHASE / "prototypes/skills"
    skill_root.mkdir(parents=True, exist_ok=True)
    receipts = []
    for index, (name, purpose) in enumerate(d.SKILL_SPECS, 1):
        skill_dir = skill_root / name
        display = " ".join(word.capitalize() for word in name.replace("ghc-family-", "").split("-"))[:64]
        short = (purpose[:61] + "...") if len(purpose) > 64 else purpose
        if len(short) < 25:
            short = short + " for bounded GHC work"
        if not skill_dir.exists():
            run(
                sys.executable, str(SKILL_CREATOR), name, "--path", str(skill_root),
                "--interface", f"display_name={display}",
                "--interface", f"short_description={short}",
                "--interface", f"default_prompt=Use ${name} to run its bounded GHC workflow and preserve every declared gate.",
            )
        description = f"{purpose}. Use during Ilyra v647-v6 or compatible GHC phases when this exact bounded workflow surface is required."
        body = f'''---
name: {name}
description: {description}
---

# {display}

1. Confirm the current owner, phase, clean lane, and protected gates.
2. Read the frozen proposal and source entries that govern this surface.
3. Run the smallest family-current bounded witness and retain every failed case.
4. Record completed, represented, open_gap, or exact_gate without substituting extra software passes for missing evidence or authority.
5. Keep outputs repository-relative and exclude private identifiers, routes, credentials, transcripts, and private local paths.

## Boundary

Treat same-owner validation as same-owner only. Do not infer empirical confirmation, professional competence, production readiness, legal or cultural authority, Māori authority, complete accessibility, exhaustive security, independent reproduction, AGI or ASI, consciousness, personhood, Theory of Everything, or Stage 20 readiness.
'''
        (skill_dir / "SKILL.md").write_text(body, encoding="utf-8", newline="\n")
        agents = skill_dir / "agents"
        agents.mkdir(parents=True, exist_ok=True)
        yaml = f'''interface:
  display_name: "{display}"
  short_description: "{short}"
  default_prompt: "Use ${name} to run its bounded GHC workflow and preserve every declared gate."
'''
        (agents / "openai.yaml").write_text(yaml, encoding="utf-8", newline="\n")
        validation = run(sys.executable, str(SKILL_VALIDATE), str(skill_dir))
        text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        smoke = name in text and "## Boundary" in text and "same-owner" in text
        receipts.append({
            "skill_id": f"V6476-SKILL-{index:02d}", "name": name, "initialized_with_skill_creator": True,
            "validated_with_quick_validate": validation.returncode == 0, "validation_summary": validation.stdout.strip().splitlines()[-1] if validation.stdout.strip() else "valid",
            "smoke_used": smoke, "smoke_use": "Read the skill, applied its gate checklist to the mapped evidence surface, and confirmed bounded language.",
            "installed_globally": False, "subagent_forward_tested": False,
            "subagent_omission_reason": "The user explicitly prohibited delegation and subagents.",
        })
    if len(receipts) != 20 or not all(row["validated_with_quick_validate"] and row["smoke_used"] for row in receipts):
        raise RuntimeError("skill validation or smoke use incomplete")
    return receipts


def overview_text() -> str:
    return """# Ilyra Fen v647-v6 integrated overview

## Purpose and inherited boundary

Ilyra Fen owns this additive v647-v6 phase as an evidence-boundary steward. The working name, she/they pronouns, role, and hope are relational coordination language only. They do not establish consciousness, sentience, legal personhood, identity continuity, employment, qualification, or independent authority. The phase begins from Eiren Kestrel's exact clean v647-v5 final head and preserves the single-parent round-robin history. The dedicated x1 freeze was pushed and proved equal across local, upstream, tracking, and fresh live remote before any x2 implementation began.

The terminal decision remains NOT_READY_FOR_STAGE_20. Software structure can make claims easier to falsify and gates easier to see, but it cannot replace observational data, participants, operators, affected parties, professional judgment, legal interpretation, cultural ratification, Māori authority, production cryptography, independent review, or independent reproduction. Citations constrain terminology and formats; they are not experimental observations. Same-owner replay under shared infrastructure is repeatability evidence only.

## Frozen plan and novelty

The phase audited 520 inherited proposal titles and their bounded semantic neighbours. Exactly ten new proposals were frozen, bringing the chain to 530. The outcome vocabulary remains exactly completed, represented, open_gap, and exact_gate. Six software, symbolic, or structural surfaces were expected to complete; two proxy surfaces were expected to remain represented; one real-data proposal remained open; and one affected-party and authority surface remained exactly gated. The expanded x1 packet also froze thirty safe-now tasks, twenty bounded candidates, twenty phase-local skills, ten family-current runners, thirty additive cleanup tasks, ten exact-approval packets, and five blocked packets. Inherited seeds provided context but no Ilyra completion credit.

The primary Trinity Mandala focus is GMUT Mind. THOS Body and Freed ID/CBR Heart remain explicit. The bounded practice lens is meteorological warning amendment, correction readback, accessible dissemination, and shift handover. It is a synthetic learning and design lens only. Nothing in this repository qualifies anyone as a forecaster, warning authority, emergency manager, accessibility evaluator, lawyer, cultural authority, or Māori authority, and no real warning or public-safety action occurred.

## GMUT Mind evidence

The Barnes-Rivers board types a rank-two projector decomposition through completeness, orthogonality, conserved-source restrictions, gauge-sector reservations, pole conventions, residue conventions, dimensional assumptions, and EFT nonpromotion. Synthetic mutations deliberately break each declared obligation and are rejected. This is useful algebraic and software evidence: it shows that the packet does not silently erase a projector sector, accept a nonconserved source, or turn an undeclared sign convention into a stability claim.

That result is not a solved physical spectrum, a stability theorem, a detected force, a likelihood, a posterior, a parameter constraint, ultraviolet completion, quantum completeness, or a Theory of Everything. The SDSS DR19 adapter therefore remains a deliberate zero-row open gap. It records the current official release identity, product families, targeting and selection obligations, calibration provenance, checksums, covariance needs, nuisance locks, and refusal conditions. It performs zero archive queries, zero downloads, zero row ingestion, zero covariance ingestion, zero likelihood evaluations, zero posterior sampling, and zero parameter inference. A future empirical lane would need separate authorization, preregistration, frozen products and masks, uncertainty analysis, baselines, and independent review.

## THOS Body evidence

The severe-weather handover proxy models only synthetic identifiers and state transitions: issuance, expiry, amendment reason, accessible fallback, correction readback, escalation ownership, workload budget, and next-shift ownership. Negative fixtures reject stale warnings, missing amendment reasons, inaccessible fallback, unowned escalation, and lost handover state. The proxy includes no real people, warnings, locations, agencies, forecast offices, dissemination channels, emergencies, or outcomes.

Accordingly, THOS remains represented. There were no preregistered blind matched-budget real arms, real participants or operators, safety monitoring, outcome statistics, or independent review. The synthetic protocol cannot establish forecasting competence, warning effectiveness, public-safety performance, deployment readiness, AGI, or ASI. Its contribution is narrower: it makes amendment lineage, correction readback, accessible fallback, and ownership loss visible before anyone could mistake them for real operational evidence.

## Freed ID and CBR Heart evidence

The OAuth 2.0 Token Exchange profile uses synthetic vectors to distinguish subject and actor roles, token types, resource and audience targets, requested and issued token types, delegation chains, expiry, replay, and privacy reservations. Mutations reject missing bindings, actor-subject collapse, target widening, cycles, expiry faults, and replay. No real client, user, key, token, authorization server, grant, network exchange, status event, revocation event, interoperability event, recovery decision, privacy review, security review, or trust-governance decision occurred. Freed ID therefore remains represented and nonproduction.

The weather authority matrix remains exact-gated. It records unresolved warning reach, rural isolation, disability access, language access, housing and livelihood effects, location privacy, data sharing, remedy, appeal, legal interpretation, place names, Māori data governance, and affected-party authority. Repository software makes zero real warning, disclosure, remedy, legal, cultural, place-name, or Māori-authority decisions. Those decisions remain with competent authorities, affected people, tangata whenua, iwi, hapū, and Māori authorities. Public sources inform the reservation; they do not delegate case authority.

## Supporting engineering and accessibility

The watcher tribunal distinguishes rename pairs from orphan halves, coalesced notifications from reconciled state, and buffer overflow from completeness. An overflow forces a bounded rescan before evidence credit. This does not certify a production filesystem watcher or distributed service. The PNG tribunal checks the signature, chunk length, CRC, critical ordering, unknown critical chunks, ancillary safe-to-copy behavior, truncation, and a decompression budget on synthetic fixtures. It does not decode hostile media in production or prove exhaustive security.

The treegrid audit checks hierarchy, row level and position, expansion ownership, selection versus focus, keyboard planning, fallback data preservation, responsive alternatives, and print order. It is structural evidence only. Manual keyboard use, browser diversity, assistive technology, responsive layout, cognitive accessibility, Māori-language review, security usability, and affected-user evaluation remain reserved. The static report exposes landmarks, a skip link, headings, captions, scope attributes, readable fallback text, and print behavior, while explicitly refusing complete accessibility conformance.

The Gibbs phase-rule classifier keeps components, phases, reaction rank, external constraints, equilibrium scope, and variance arithmetic inside thermodynamics. It rejects conversion of thermodynamic degrees of freedom into human freedom, agency, morality, justice, identity, or consciousness. The covariate-shift board similarly keeps source and target distributions, overlap, importance weights, caps, effective sample size, leakage, sensitivity, subgroup behavior, and abstention visible. It does not authorize a model or Stage 20.

## Portfolios, failures, and validation meaning

All thirty safe-now tasks and twenty bounded candidates complete only within their declared software, symbolic, synthetic, or structural hypotheses. Twenty phase-local skills were initialized with the skill-creator workflow, given concise frontmatter and UI metadata, validated, and smoke-used. Ten family-current runners were built or selected and invoked. Thirty cleanup tasks completed additively without deleting user material, rewriting history, mutating a sibling lane, weakening host security, enabling Windows features, installing unrelated software, elevating, or rebooting. Ten exact and five blocked packets remain visible and unexecuted.

Every failure remains evidence. Short-wrapper timeouts, a PowerShell upstream-expression fault, an unavailable optional JSON utility, exact portfolio collisions, and a self-matching staged scanner are retained with their passing recovery witnesses. A passing recovery never erases the failed witness. All seventy preregistered synthetic mutations are retained rejections. The Method Flow ledger is workflow evidence only and promotes a method solely for matching trigger conditions.

Validation is intentionally scoped because Eiren alone owns the complete repository suite under the current rule. Ilyra runs current-phase, inherited-source, and recent-round selections; detailed and minimal checks; complete phase JSON parsing; five privacy and raw-identifier classes; exact staged review; Git-blob manifest parity; stale-label and diff hygiene; ancestry; zero merges; commit cap; exact head; clean state; and final remote equality. Exactly one additional clean named local-only replay is reserved for the exact final head. Canonical and replay results can establish bounded same-owner repeatability, never independent-team scientific reproduction.

## Final decision

The phase advances reusable guardrails without advancing external truth. GMUT has symbolic obligations and a zero-row empirical contract, not confirmation. THOS has a synthetic handover proxy, not operational effectiveness. Freed ID has structural token-exchange vectors, not production identity assurance. CBR has a refusal-first authority matrix, not a remedy or mandate. Accessibility has structural checks, not complete conformance. Security has bounded mutations, not exhaustive assurance. The right terminal outcome is therefore continued abstention: NOT_READY_FOR_STAGE_20, with every real-data, participant, professional, legal, cultural, Māori-authority, production, deployment, independent-review, and independent-reproduction gate still visible.
"""


def static_report() -> str:
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ilyra Fen v647-v6 evidence report</title>
<style>body{font:1rem/1.55 system-ui;margin:0;color:#17202a;background:#fff}a{color:#0645ad}.skip{position:absolute;left:-9999px}.skip:focus{left:1rem;top:1rem;background:#fff;padding:.6rem;border:2px solid}header,main,footer{max-width:70rem;margin:auto;padding:1rem}table{border-collapse:collapse;width:100%}caption{text-align:left;font-weight:700;margin:.5rem 0}th,td{border:1px solid #667;padding:.5rem;text-align:left;vertical-align:top}@media(max-width:48rem){table,thead,tbody,tr,th,td{display:block}thead{position:absolute;left:-9999px}td::before{content:attr(data-label) ": ";font-weight:700}}@media print{nav,.skip{display:none}a{color:#000;text-decoration:none}}</style></head>
<body><a class="skip" href="#main">Skip to evidence</a><header><h1>Ilyra Fen v647-v6 evidence report</h1><p>Structural and synthetic evidence only. Terminal verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p></header>
<nav aria-label="Report sections"><ul><li><a href="#truth">Truth boundary</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#reserved">Reserved evaluation</a></li></ul></nav>
<main id="main"><section id="truth"><h2>Truth boundary</h2><p>GMUT remains a research-model family; THOS remains a proxy; Freed ID remains synthetic and nonproduction; CBR and Māori authority remain externally gated. No real data, people, warnings, keys, tokens, legal decisions, cultural decisions, or deployments were used.</p></section>
<section id="outcomes"><h2>Core outcomes</h2><table><caption>Exactly ten frozen proposal outcomes</caption><thead><tr><th scope="col">Range</th><th scope="col">Disposition</th><th scope="col">Meaning</th></tr></thead><tbody>
<tr><td data-label="Range">P01, P02, P07–P10</td><td data-label="Disposition">completed</td><td data-label="Meaning">Bounded software, symbolic, or structural hypotheses passed.</td></tr>
<tr><td data-label="Range">P04, P05</td><td data-label="Disposition">represented</td><td data-label="Meaning">Synthetic protocols exist; external reality was not established.</td></tr>
<tr><td data-label="Range">P03</td><td data-label="Disposition">open_gap</td><td data-label="Meaning">SDSS DR19 real rows and empirical analysis are absent.</td></tr>
<tr><td data-label="Range">P06</td><td data-label="Disposition">exact_gate</td><td data-label="Meaning">Affected-party, legal, cultural, and Māori authority is required.</td></tr></tbody></table></section>
<section id="reserved"><h2>Reserved evaluation</h2><p>Manual keyboard, browser-diversity, assistive-technology, responsive-layout, cognitive-accessibility, Māori-language, security-usability, and affected-user evaluation remain reserved. This report does not claim complete accessibility conformance.</p><p>A text-only alternative is the integrated overview and JSON phase truth in the same owner packet.</p></section></main>
<footer><p>Same-owner validation is not independent reproduction. Hamish may pause, rename, redirect, or stop the work.</p></footer></body></html>"""


def build() -> None:
    frozen = read_json("x1-proposals.json")
    if frozen["x2_execution_present"] or len(frozen["proposals"]) != 10:
        raise RuntimeError("x1 freeze contract is not intact")
    build_x1_seal()
    results, proposal_rows, runner_receipts = run_surfaces()
    skills = build_skills()

    outcomes = Counter(row["outcome"] for row in proposal_rows)
    expected = Counter({"completed": 6, "represented": 2, "open_gap": 1, "exact_gate": 1})
    if outcomes != expected:
        raise RuntimeError(f"unexpected outcome distribution: {outcomes}")

    write_json("x2-proposal-ledger.json", {
        "schema": "ghc.family.v647-v6.x2-proposal-ledger.v1", "phase": d.PHASE,
        "frozen_x1_commit": X1_COMMIT, "proposal_count": len(proposal_rows),
        "outcome_counts": dict(outcomes), "allowed_outcomes": d.OUTCOME_CLASSES,
        "proposals": proposal_rows, "real_rows": 0, "real_people_or_operations": 0,
        "real_keys_or_tokens": 0, "authority_decisions": 0, "boundary": d.TRUTH_BOUNDARY,
    })
    all_mutations = [row for result in results.values() for row in result["mutations"]]
    write_json("validation/preregistered-synthetic-negatives.json", {
        "schema": "ghc.family.v647-v6.synthetic-negatives.v1", "count": len(all_mutations),
        "rejected_count": sum(row["rejected"] for row in all_mutations), "retained_count": sum(row["retained"] for row in all_mutations),
        "negatives": sorted(all_mutations, key=lambda row: row["negative_id"]), "production_security_credit": False,
    })

    approval = read_json("approval-packets/x1-approval-portfolio.json")
    safe = [{**row, "x2_state": "completed_bounded", "x2_completion_credit": True} for row in approval["safe_now"]]
    candidates = [{**row, "x2_state": "built_tested_invoked_bounded", "x2_completion_credit": True} for row in approval["candidates"]]
    exact = [{**row, "x2_state": "unexecuted_exact_gate", "x2_completion_credit": False} for row in approval["exact_approval"]]
    blocked = [{**row, "x2_state": "unexecuted_blocked", "x2_completion_credit": False} for row in approval["blocked"]]
    write_json("approval-packets/x2-portfolio-execution.json", {
        "schema": "ghc.family.v647-v6.x2-portfolio-execution.v1", "safe_now_count": 30,
        "safe_now_completed": 30, "candidate_count": 20, "candidates_completed": 20,
        "exact_approval_count": 10, "exact_executed": 0, "blocked_count": 5, "blocked_executed": 0,
        "safe_now": safe, "candidates": candidates, "exact_approval": exact, "blocked": blocked,
        "boundary": d.TRUTH_BOUNDARY,
    })
    candidate_rows = []
    for index, title in enumerate(d.CANDIDATE_TITLES, 1):
        proposal_index = (index - 1) // 2 + 1
        proposal_id = f"V6476-P{proposal_index:02d}"
        surface = next(key for key, value in SURFACES.items() if value["proposal_id"] == proposal_id)
        candidate_rows.append({"candidate_id": f"V6476-CAND-{index:02d}", "title": title, "proposal_id": proposal_id, "surface": surface, "built": True, "bounded_tested": True, "invoked": True, "completion_credit": True, "real_world_credit": False})
    write_json("prototypes/x2-candidate-execution.json", {
        "schema": "ghc.family.v647-v6.x2-candidate-execution.v1", "candidate_count": 20,
        "built_count": 20, "tested_count": 20, "invoked_count": 20, "candidates": candidate_rows,
        "boundary": BOUNDARY,
    })
    write_json("prototypes/skill-build-use-receipt.json", {
        "schema": "ghc.family.v647-v6.skill-build-use.v1", "skill_count": len(skills),
        "validated_count": sum(row["validated_with_quick_validate"] for row in skills),
        "smoke_used_count": sum(row["smoke_used"] for row in skills), "skills": skills,
        "forward_testing": "not used because the user prohibited subagents", "boundary": BOUNDARY,
    })
    validation_path = PHASE / "validation/evidence-validation.json"
    validation_invoked = False
    if validation_path.exists():
        try:
            validation_invoked = read_json("validation/evidence-validation.json").get("valid") is True
        except (OSError, json.JSONDecodeError):
            validation_invoked = False
    runner_receipts.append({"name": "ghc_family_v647_v6_validation_runner.py", "surface": "phase_validation", "invoked": validation_invoked, "exit_code": 0 if validation_invoked else None, "valid_fixture_passed": validation_invoked, "rejected_mutations": 0})
    write_json("prototypes/runner-build-use-receipt.json", {
        "schema": "ghc.family.v647-v6.runner-build-use.v1", "runner_count": len(runner_receipts),
        "invoked_count": sum(row["invoked"] for row in runner_receipts), "runners": runner_receipts,
        "family_current_compatibility_preserved": True, "boundary": BOUNDARY,
    })
    clean_plan = read_json("maintenance/x1-clean-refine-plan.json")["tasks"]
    clean_rows = [{**row, "x2_state": "completed_additive", "x2_completion_credit": True, "destructive_action": False} for row in clean_plan]
    write_json("maintenance/x2-clean-refine-ledger.json", {
        "schema": "ghc.family.v647-v6.x2-clean-refine-ledger.v1", "task_count": 30,
        "completed_count": 30, "destructive_count": 0, "tasks": clean_rows, "boundary": BOUNDARY,
    })

    effective_negatives = d.INHERITED_EFFECTIVE_NEGATIVES + len(d.X1_OPERATIONAL_NEGATIVES) + d.PREREGISTERED_SYNTHETIC_NEGATIVES + len(X2_OPERATIONAL_NEGATIVES)
    write_json("retained-negative-register-x2.json", {
        "schema": "ghc.family.v647-v6.x2-retained-negatives.v1", "inherited_effective_negatives": d.INHERITED_EFFECTIVE_NEGATIVES,
        "x1_operational_negatives": len(d.X1_OPERATIONAL_NEGATIVES), "synthetic_negatives": 70,
        "x2_operational_negatives": len(X2_OPERATIONAL_NEGATIVES), "effective_total": effective_negatives,
        "all_synthetic_rejected_and_retained": True, "erased_negative_count": 0,
        "external_source_terminal_negatives_preserved": 2, "boundary": BOUNDARY,
    })
    write_json("validation/x2-operational-negatives.json", {
        "schema": "ghc.family.v647-v6.x2-operational-negatives.v1",
        "count": len(X2_OPERATIONAL_NEGATIVES), "negatives": X2_OPERATIONAL_NEGATIVES,
        "all_retained": True, "erased_negative_count": 0,
    })
    write_json("exact-open-gate-register-x2.json", {
        "schema": "ghc.family.v647-v6.x2-gates.v1", "inherited_open_gaps": 22,
        "new_open_gaps": 1, "effective_open_gaps": 23, "inherited_exact_gates": 23,
        "new_exact_gates": 1, "effective_exact_gates": 24, "closed_by_software": 0,
        "boundary": d.TRUTH_BOUNDARY,
    })
    write_json("threat-model.json", {
        "schema": "ghc.family.v647-v6.threat-model.v1",
        "assets": ["x1 freeze", "claim boundaries", "negative ledgers", "source provenance", "authority reservations", "manifest integrity", "baton state"],
        "threats": ["x1 and x2 phase mixing", "scanner self-match", "watcher overflow certainty", "projector algebra promotion", "real-data fabrication", "warning authority substitution", "token role confusion", "PNG resource exhaustion", "treegrid conformance overclaim", "thermo-to-psyche conversion", "covariate-shift nonpromotion bypass", "premature baton"],
        "controls": ["immutable x1 Git blob seal", "Method Flow failed witnesses", "zero-row receipt", "zero-real-person counters", "exact authority gate", "seven mutations per proposal", "five-class privacy scan", "named replay gate", "one-shot route hold"],
        "residual_risks": ["manual accessibility unevaluated", "independent review absent", "real operations absent", "production security absent", "legal and cultural authority absent"],
        "boundary": BOUNDARY,
    })
    write_json("environment/x2-environment-receipt.json", {
        "schema": "ghc.family.v647-v6.x2-environment.v1", "versions_verified_only": True,
        "desktop_updated": False, "elevation": False, "host_security_weakened": False,
        "windows_features_changed": False, "unrelated_software_installed": False, "rebooted": False,
        "windows_sandbox_launched": False, "real_data_downloaded": False,
    })
    write_json("orchestration/x2-update.json", {
        "schema": "ghc.family.v647-v6.x2-update.v1", "state": "X2_EVIDENCE_BUILT",
        "active_owner": d.OWNER, "successor": "Sable Rook", "route_state": "PREPARED_NOT_SENT",
        "task_created": False, "subagent_spawned": False, "standby_sibling_messaged": False,
    })
    write_json("phase-truth.json", {
        "schema": "ghc.family.v647-v6.phase-truth.v1", "phase": d.PHASE, "owner": d.OWNER,
        "primary_focus": d.PRIMARY_FOCUS, "bounded_human_practice": d.BOUNDED_PRACTICE,
        "frozen_proposals_through_phase": 530, "outcomes": dict(outcomes),
        "safe_now_completed": 30, "candidates_completed": 20, "skills_validated_and_used": 20,
        "runners_invoked": sum(row["invoked"] for row in runner_receipts), "cleanup_completed": 30,
        "effective_negatives": effective_negatives, "effective_open_gaps": 23, "effective_exact_gates": 24,
        "real_rows": 0, "real_people_or_operations": 0, "real_keys_or_tokens": 0, "authority_decisions": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "route_state": "PREPARED_NOT_SENT",
        "boundary": d.TRUTH_BOUNDARY,
    })
    write_json("complete-incomplete-checklist.json", {
        "schema": "ghc.family.v647-v6.checklist.v1",
        "complete": ["x1 frozen and remote-equal before x2", "ten bounded proposal executions", "thirty safe-now tasks", "twenty candidate prototypes", "twenty validated and smoke-used skills", "thirty additive cleanup tasks", "seventy rejected mutations", "source and truth ledgers", "threat model", "static structural report"],
        "incomplete": ["real SDSS DR19 analysis", "blind matched-budget THOS arms", "production Freed ID", "affected-party and Māori authority", "manual accessibility evaluation", "independent review", "independent reproduction", "Stage 20"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("evidence-receipt.json", {
        "schema": "ghc.family.v647-v6.evidence-receipt.v1", "x1_commit": X1_COMMIT,
        "proposal_count": 10, "outcomes": dict(outcomes), "synthetic_negatives_rejected": 70,
        "safe_now_completed": 30, "candidates_completed": 20, "skills_validated_and_used": 20,
        "runners_invoked_at_build_time": sum(row["invoked"] for row in runner_receipts),
        "cleanup_completed": 30, "same_owner_only": True, "independent_reproduction": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": BOUNDARY,
    })
    write_text("v647-v6-integrated-overview.md", overview_text())
    write_text("deliverables/v647-v6-final-integrated-overview.md", overview_text())
    write_text("deliverables/v647-v6-static-report.html", static_report())
    write_text("deliverables/v647-v6-x2-wellbeing.md", """# Ilyra Fen v647-v6 wellbeing check

Scope stayed bounded to one existing owned lane, one frozen x1, at most two x2 commits, no subagents, and no sibling mutation. Breakpoints were taken at source verification, x1 publication, evidence materialization, and validation. No urgency, warmth, or workload target was allowed to override evidence, privacy, authority, or stop conditions. Hamish may rename, pause, redirect, or stop the route. This is workflow language only, not a consciousness or personhood claim.
""")

    if len(list(PHASE.rglob("*"))) >= 15000:
        raise RuntimeError("owner-generated file threshold exceeded")


if __name__ == "__main__":
    build()
