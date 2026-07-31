#!/usr/bin/env python3
"""Build the bounded Auren Lark v657-v3 x2 evidence packet."""

from __future__ import annotations

import hashlib
import html
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v657_v3_phase_data as d
import ghc_family_v657_v3_x2_config as c
from ghc_family_v657_v3_runtime import evaluate_surface


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
SELF_EXCLUSIONS = {
    "validation/evidence-content-manifest.json",
    "validation/evidence-privacy-scan.json",
    "validation/evidence-staged-review.json",
    "validation/evidence-validation.json",
}


def write_json(relative: str, payload: Any, *, compact: bool = False) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(
        payload,
        ensure_ascii=False,
        indent=None if compact else 2,
        separators=(",", ":") if compact else None,
        sort_keys=True,
    )
    path.write_text(text + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def x1_frozen_paths() -> list[str]:
    return [
        line
        for line in git(
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            c.X1_COMMIT,
        ).splitlines()
        if line
    ]


def assert_x1_unchanged() -> None:
    paths = x1_frozen_paths()
    index_changed = subprocess.run(
        ["git", "diff", "--cached", "--name-only", c.X1_COMMIT, "--", *paths],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.splitlines()
    working_changed = subprocess.run(
        ["git", "diff", "--name-only", "--", *paths],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.splitlines()
    changed = sorted(set(index_changed + working_changed))
    if changed:
        raise RuntimeError(f"x1 frozen paths changed: {changed}")


def mutation_negative(proposal_id: str, row: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "negative_id": f"V6573-MUT-{proposal_id.split('-')[-1]}-{index:02d}",
        "proposal_id": proposal_id,
        "mutation_id": row["mutation_id"],
        "signature": row["error_codes"],
        "observed": "The preregistered mutation was rejected by the bounded contract validator.",
        "credit": 0,
        "retained": True,
        "same_owner_only": True,
        "independent_reproduction": False,
    }


def mutation_method(negative: dict[str, Any], index: int) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    method_id = f"V6573-X2-MUT-METHOD-{index:03d}"
    fail_id = f"V6573-X2-MUT-WITNESS-{index:03d}-F"
    pass_id = f"V6573-X2-MUT-WITNESS-{index:03d}-P"
    method = {
        "method_id": method_id,
        "title": f"Fail-closed mutation guard for {negative['mutation_id']}",
        "trigger_preconditions": [negative["mutation_id"]],
        "failure_signature": negative["signature"],
        "candidate_workaround": "Reject the mutated candidate and retain it at zero credit.",
        "recurrence_guard": "Run all five frozen mutations for the surface and require explicit rejection codes.",
        "approval_class": "safe_now_owner_local_synthetic_falsification",
        "privacy_class": "sanitized_public",
        "scope_boundary": "Synthetic mutation evidence only.",
        "rollback": "Discard the mutated candidate, preserve the valid contract, and leave external state unchanged.",
        "protected_gates": d.PROTECTED_GATES,
        "retained_negative_ids": [negative["negative_id"]],
        "validation_witness_ids": [fail_id, pass_id],
        "recommendation_state": "preferred",
        "supersedes": [],
    }
    witnesses = [
        {
            "witness_id": fail_id,
            "method_id": method_id,
            "result": "fail",
            "procedure": "Apply the preregistered mutation to the valid synthetic fixture.",
            "expected": "The mutation must not receive valid-fixture credit.",
            "observed": f"Rejected with {', '.join(negative['signature'])}.",
            "retained_negative_ids": [negative["negative_id"]],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": "Zero completion credit.",
        },
        {
            "witness_id": pass_id,
            "method_id": method_id,
            "result": "pass",
            "procedure": "Confirm explicit rejection while preserving the valid fixture separately.",
            "expected": "The validator fails closed on the mutation.",
            "observed": "The mutation was rejected and retained without changing external state.",
            "retained_negative_ids": [negative["negative_id"]],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": "Bounded same-owner falsification only.",
        },
    ]
    return method, witnesses


def operational_method(
    negative: dict[str, Any], index: int
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    method_id = f"V6573-X2-OP-METHOD-{index:02d}"
    fail_id = f"V6573-X2-OP-WITNESS-{index:02d}-F"
    pass_id = f"V6573-X2-OP-WITNESS-{index:02d}-P"
    method = {
        "method_id": method_id,
        "title": f"Bounded recovery for {negative['slug']}",
        "trigger_preconditions": [negative["slug"]],
        "failure_signature": negative["failure_signature"],
        "candidate_workaround": negative["candidate_workaround"],
        "recurrence_guard": negative["recurrence_guard"],
        "approval_class": "safe_now_owner_local_workflow_recovery",
        "privacy_class": "sanitized_public",
        "scope_boundary": negative["scope_boundary"],
        "rollback": "Retain the failed attempt at zero credit, stop the failed invocation, and leave sibling and external state unchanged.",
        "protected_gates": d.PROTECTED_GATES,
        "retained_negative_ids": [negative["negative_id"]],
        "validation_witness_ids": [fail_id, pass_id],
        "recommendation_state": "preferred",
        "supersedes": [],
    }
    witnesses = [
        {
            "witness_id": fail_id,
            "method_id": method_id,
            "result": "fail",
            "procedure": negative["fail_procedure"],
            "expected": "The bounded operation completes without a tooling, timeout, or encoding failure.",
            "observed": negative["fail_observed"],
            "retained_negative_ids": [negative["negative_id"]],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": "Failed workflow witness with zero completion credit.",
        },
        {
            "witness_id": pass_id,
            "method_id": method_id,
            "result": "pass",
            "procedure": negative["pass_procedure"],
            "expected": "The bounded recovery completes while preserving the failed witness.",
            "observed": negative["pass_observed"],
            "retained_negative_ids": [negative["negative_id"]],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": negative["scope_boundary"],
        },
    ]
    return method, witnesses


def skill_markdown(name: str, purpose: str, slugs: list[str]) -> str:
    return f"""# {name}

## Purpose

{purpose}

## Trigger

Use this phase-local skill when a v657-v3 typewriter-maintenance evidence surface needs the bounded checks for: {", ".join(slugs)}.

## Required sequence

1. Read the proposal contract and official-source identifiers.
2. Confirm all inputs are synthetic and contain no real passengers, technicians, typewriters, buildings, components, controls, work orders, inspections, repairs, rescues, credentials, accounts, or private routes.
3. Invoke the corresponding family-current runner.
4. Require the valid fixture to pass and every frozen mutation to be rejected.
5. Preserve failed witnesses at zero credit and keep the declared truth outcome unchanged unless exact evidence requires a downgrade.
6. Stop on any professional, production, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, Theory-of-Everything, or Stage 20 gate.

## Output

Write only a repository-relative, sanitized receipt. Do not include credentials, private identifiers, private paths, transcripts, screenshots, session streams, or raw field data.

## Boundary

This skill is owner-local synthetic workflow guidance. It is not evidence of consciousness, personhood, identity continuity, employment, qualification, maintainer appointment, engineering or security assessment, professional authority, production readiness, legal interpretation, cultural ratification, Māori authority, independent reproduction, or Stage 20 readiness.
"""


def skill_markdown_v6573(name: str, purpose: str, slugs: list[str]) -> str:
    surface_list = ", ".join(slugs)
    return f"""---
name: {name}
description: "{purpose} Use for bounded v657-v3 synthetic typewriter evidence across {surface_list}."
---

# {name}

## Required sequence

1. Read the frozen proposal contract and its official-source identifiers.
2. Confirm every input is synthetic and contains no real owner, donor, repairer, conservator, typewriter, component, tool, material, workshop, treatment, credential, account, private route, or culturally restricted payload.
3. Invoke the corresponding family-current runner only inside the Auren v657-v3 owner packet.
4. Require the valid fixture to pass and all five frozen mutations for each surface to be rejected.
5. Retain every failed witness at zero credit and keep the exact truth outcome unchanged unless exact evidence requires a downgrade.
6. Stop on any real operation, energization, disassembly, cleaning, lubrication, adjustment, repair, conservation, authenticity, valuation, professional, production, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, Theory-of-Everything, or Stage 20 gate.

## Output

Write only a repository-relative sanitized receipt. Do not include credentials, private identifiers, private paths, transcripts, screenshots, session streams, real object records, or raw field data.

## Boundary

This phase-local skill is synthetic workflow guidance. It does not establish consciousness, sentience, legal personhood, identity continuity, employment, qualification, professional authority, operational authority, safety, production readiness, ownership, authenticity, valuation, legal interpretation, cultural ratification, Māori authority, independent reproduction, or Stage 20 readiness.
"""


def skill_openai_yaml(name: str, purpose: str) -> str:
    display = " ".join(part.capitalize() for part in name.split("-"))
    short = purpose if len(purpose) <= 64 else purpose[:61].rstrip() + "..."
    return f"""interface:
  display_name: "{display}"
  short_description: "{short}"
  default_prompt: "Use {chr(36)}{name} to validate its frozen synthetic typewriter evidence surfaces."
policy:
  allow_implicit_invocation: false
"""


def wrapper_source(filename: str, slugs: list[str]) -> str:
    return f'''#!/usr/bin/env python3
"""Family-current Auren Lark v657-v3 typewriter-maintenance evidence runner."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ghc_family_v657_v3_runtime import ROOT, run_named_surface, write_json


SURFACES = {slugs!r}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    rows = [run_named_surface(slug) for slug in SURFACES]
    payload = {{
        "schema": "ghc.family.v657-v3.group-runner-receipt.v1",
        "runner": "{filename}",
        "surfaces": SURFACES,
        "surface_count": len(rows),
        "valid_fixture_count": sum(row["valid_fixture_passed"] for row in rows),
        "rejected_mutation_count": sum(row["rejected_mutation_count"] for row in rows),
        "valid": all(row["valid_fixture_passed"] and row["all_mutations_rejected"] for row in rows),
        "same_owner_only": True,
        "independent_reproduction": False,
        "rows": rows,
    }}
    write_json(ROOT / args.output, payload)
    print(json.dumps(payload, ensure_ascii=True, sort_keys=True))
    if not payload["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
'''


def overview(outcome_counts: dict[str, int], negative_total: int) -> str:
    return f"""# Auren Lark v657-v3 integrated evidence overview

## Outcome and identity boundary

Ilyra v657-v3 executes thirty frozen proposal surfaces as bounded synthetic software evidence. The observed distribution is {outcome_counts['completed']} completed, {outcome_counts['represented']} represented, {outcome_counts['open_gap']} open gap, and {outcome_counts['exact_gate']} exact gate. The evidence candidate preserves {negative_total:,} effective negatives, with every rejected mutation and operational failure retained at zero credit. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

Auren Lark, they/them, is relational working language only. The role remains repair-traceability lantern and reversible-evidence gardener, and the hope remains making community repair decisions kind, inspectable, and reversible while competent and affected authorities retain safety, ownership, privacy, legal, cultural, and Māori decisions. This language is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, or independent agency.

## Freed ID and CBR Heart

Freed ID/CBR Heart is the primary focus. The evidence packet structures synthetic asset and change-set provenance, minimized disclosure, correction, contestation, maintainer-role placeholders, accessible notice, sensitive publication, remedy, and authority checkpoints. These contracts expose omissions and prohibited promotions to software. They do not appoint maintainers, authorize repository access, decide vulnerability severity, approve patches or releases, operate production systems, interpret law, decide cultural legitimacy, or substitute for Māori authority.

The bounded practice lens is public-interest software defect intake, repair planning, component and change-set provenance, test and rollback evidence, release reservation, maintenance windows, incident handover, accessible notice, privacy and vulnerability holds, and community correction. No real person, repository, service, account, credential, vulnerability report, component inventory, incident, patch, release, or deployment is included. Competent maintainers, operators, security and accessibility specialists, privacy and legal reviewers, affected communities, tangata whenua, iwi, hapū, and Māori authorities retain every governed decision.

## GMUT Mind and THOS Body

GMUT Mind remains explicit through typed Bayesian defect-prior and repairable-system hazard-rate dimensional proxies, observation windows, missingness, censoring, calibration quarantine, sensitivity, and nonpromotion. The code checks structural consistency and rejects mutations. It uses no real defect dataset, failure history, calibration dataset, likelihood, posterior, parameter constraint, prediction, reliability conclusion, or empirical comparison.

The proxies remain represented, not empirically confirmed. They do not establish a new force, unique prediction, stability theorem, ultraviolet completion, Theory of Everything, proof, or canon. THOS remains represented through synthetic intake, rollback, maintenance-window, workload, safety-stop, readback, and handover contracts; it has no real operators, participants, interventions, safety monitoring, matched-budget comparison, deployment, or operational-effectiveness result.

Freed ID surfaces provide synthetic maintainer-role and patch-provenance envelopes. They reserve purpose, audience, minimization, correction, identifier, issuer, signer, proof, status, resolution, revocation, interoperability, privacy review, independent security review, recovery, and trust governance. No real key, credential, proof, identity event, artifact signature, status service, transparency service, or trust decision exists.

CBR Heart is expressed through intake, severity deliberation, privacy and accessibility regression, vulnerability disclosure, contestation, sensitive publication, community notice, remedy, and the repair authority covenant. Software can ensure an authority field is not silently replaced by an owner-local assertion. It cannot decide safety, security, release, maintainer impact, privacy, accessibility, remedy, legal meaning, cultural legitimacy, Māori wording or concepts, Māori data governance, or Māori authority.

## Proposal groups and falsification

The first ten surfaces cover asset census, repair intake, reproduction, component relationships, severity deliberation, proposal ancestry, maintainer authorization boundaries, change-set provenance, blast radius, and repair tests. The next ten cover rollback, accessibility and privacy regression, vulnerability disclosure, attestation nonclaims, release reservation, maintenance windows, incident handover, component equivalence, and legal reservations. The final ten cover community notice, contestation, sensitive publication, GMUT and THOS proxies, Freed ID capsules, a no-network CISA KEV adapter, and the exact-gated CBR authority covenant.

Every proposal has one valid synthetic fixture and five preregistered mutations. The mutations remove a required obligation, promote a real system or artifact input, promote Stage 20, remove a required source, or alter the outcome label. All 150 mutations must be rejected with explicit error codes. Each rejection becomes a retained zero-credit negative and a paired Method Flow failed and passing witness. A passing witness establishes only that the validator failed closed; it never erases the failed candidate.

The CISA KEV adapter executes with no network and zero rows, leaving the governed real-query gap open. The CBR repair authority covenant remains exact-gated. This mutation catalogue is software falsification, not scientific or independent reproduction. The same owner created the contracts, mutations, engine, and validators under shared infrastructure.

## Skills, validation, and route boundary

Ten phase-local skills and ten family-current runners group the thirty surfaces without global installation. Each runner invokes the shared contract engine and writes a sanitized receipt. Existing historical tools and x1 artifacts remain byte-stable. No inherited or sibling file is rewritten.

The evidence candidate receives current-phase unit tests, a detailed validator, a minimal validator, complete JSON parsing, five-class privacy scanning, document and file caps, manifest parity, exact staged review, diff hygiene, and x1 byte-stability checks. Later closeout and exact-final validation add ancestry, commit caps, single-parent history, zero merges, exact head, clean state, zero divergence, and four-way live equality.

Only one successful exact-final canonical aggregate is permitted. Precommit development checks do not substitute for it. The successor route to the existing exact-title `Auren Lark` task remains `PREPARED_NOT_SENT` and ineligible until Ilyra's own exact final is clean, pushed, fresh-live equal, and passes the one authorized canonical aggregate. Tavian Sol remains on standby and is not eligible for this main-task route.
"""

def static_report(outcomes: dict[str, int], negatives: int) -> str:
    rows = "\n".join(
        f"<tr><th scope=\"row\">{html.escape(item['proposal_id'])}</th><td>{html.escape(item['title'])}</td><td>{html.escape(item['expected_disposition'])}</td></tr>"
        for item in d.PROPOSALS
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Auren Lark v657-v3 bounded repair-traceability evidence report</title>
<style>
body{{font:1rem/1.6 system-ui,sans-serif;max-width:78rem;margin:auto;padding:1.5rem;color:#10251d;background:#f7fbf8}}
a{{color:#064f3a}} a:focus{{outline:3px solid #d54f00;outline-offset:3px}}
header,section{{background:#fff;border:2px solid #2d6653;border-radius:.6rem;padding:1rem 1.25rem;margin:1rem 0}}
table{{border-collapse:collapse;width:100%}} caption{{font-weight:700;text-align:left;margin:.5rem 0}}
th,td{{border:1px solid #567a6e;padding:.55rem;text-align:left;vertical-align:top}}
.notice{{border-left:.5rem solid #b34700;padding-left:1rem}} code{{overflow-wrap:anywhere}}
</style>
</head>
<body>
<header>
<h1>Auren Lark v657-v3 bounded repair-traceability evidence report</h1>
<p class="notice"><strong>Boundary:</strong> synthetic same-owner software evidence only. Not professional engineering or security assessment, empirical confirmation, production identity or operations, legal or cultural authority, Māori authority, independent reproduction, Theory-of-Everything proof, or Stage 20 readiness.</p>
</header>
<main>
<section aria-labelledby="summary"><h2 id="summary">Summary</h2>
<p>Thirty frozen surfaces produced {outcomes['completed']} completed, {outcomes['represented']} represented, {outcomes['open_gap']} open gap, and {outcomes['exact_gate']} exact gate outcomes. The evidence candidate preserves {negatives:,} effective negatives. Terminal verdict: <code>NOT_READY_FOR_STAGE_20</code>.</p>
</section>
<section aria-labelledby="proposals"><h2 id="proposals">Proposal truth</h2>
<div role="region" aria-label="Proposal outcomes" tabindex="0">
<table><caption>Thirty bounded proposal outcomes</caption><thead><tr><th scope="col">ID</th><th scope="col">Surface</th><th scope="col">Outcome</th></tr></thead><tbody>{rows}</tbody></table>
</div></section>
<section aria-labelledby="reserved"><h2 id="reserved">Reserved evaluation</h2>
<p>Manual browser, assistive-technology, Māori-language, cognitive, low-vision, affected-user, professional, legal, cultural, and Māori-authority evaluation remains reserved. Automated structure checks are not completeness claims.</p>
</section>
</main>
</body>
</html>"""


def overview_typewriter(outcome_counts: dict[str, int], negative_total: int) -> str:
    return f"""# Auren Lark v657-v3 integrated evidence overview

## Evidence result and identity boundary

Auren Lark v657-v3 executes thirty frozen proposal surfaces as bounded owner-local synthetic software evidence. The observed distribution is {outcome_counts['completed']} completed, {outcome_counts['represented']} represented, {outcome_counts['open_gap']} open gap, and {outcome_counts['exact_gate']} exact gate. The evidence candidate preserves {negative_total:,} effective negatives. Every rejected mutation and every operational failure remains visible at zero credit. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

Auren Lark, they/them, is relational working language only. The phase role is evidence-boundary steward and reversible-handover cartographer; its hope is to leave every typewriter service-and-conservation maintenance claim traceable and every safety, accessibility, privacy, legal, cultural, and Māori-authority gate unmistakable. This language is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, or independent agency. Hamish retains the right to pause, rename, redirect, or stop the route.

## THOS Body and bounded practice

THOS Body is the primary focus. The phase models synthetic typewriter-maintenance intake, asset and work-order provenance, out-of-service and hazardous-energy holds, restricted access, component inspection state, emergency and accessibility cues, correction, workload, readback, and shift handover. It does not operate a typewriter or access a maintenance system. It does not inspect, isolate, test, adjust, repair, rescue, procure, certify, or return equipment to service.

The bounded human-practice lens is typewriter service-and-conservation maintenance and handover. No real passenger, technician, inspector, engineer, emergency responder, building owner, typewriter, escalator, building, hoistway, pit, machine room, component, controller, access log, work order, measurement, incident, credential, or affected-party decision is present. The software records synthetic obligations and refuses promotions. Competent people and institutions retain all real safety, maintenance, inspection, rescue, accessibility, privacy, legal, cultural, and governance decisions.

THOS remains represented rather than operationally validated. There are no preregistered blind matched-budget real arms, real operators, participant recruitment, field observations, safety monitoring, effect estimates, deployment, or independent review. Synthetic transition checks cannot establish operational effectiveness, equipment safety, professional competence, AGI, ASI, consciousness, or personhood.

## GMUT Mind

GMUT Mind remains explicit through two represented typed proxies. The traction-rope coupled-oscillator surface separates car and counterweight domains, stiffness and damping units, boundary signs, and calibration quarantine. The braking-energy and thermal-dissipation surface separates mass, speed, energy, power, loss terms, and measurement holds. The engine checks obligation presence and rejects prohibited promotions; it performs no equipment simulation or calibrated physical inference.

No real displacement, vibration, acceleration, speed, mass, brake, temperature, energy, load, component, or maintenance row is ingested. No likelihood, posterior, parameter constraint, forecast, safety margin, reliability estimate, stability theorem, detected force, empirical comparison, ultraviolet completion, quantum completion, or Theory of Everything is produced. GMUT remains a typed scalar-tensor and effective-field-theory research-model family.

## Freed ID and CBR Heart

Freed ID is represented through a synthetic maintenance-access purpose matrix and a synthetic typewriter-maintenance record provenance card. These surfaces expose purpose, audience or scope, minimization, expiry, disclosure, correction, status, work-order relation, inspection-state hold, unsigned state, and origin nonclaim. No real issuer, holder, verifier, key, credential, proof, account, DID method, resolution, status or revocation service, interoperability exchange, privacy review, independent security review, recovery decision, or trust-governance decision exists.

CBR Heart appears throughout the outage, accessibility, privacy, contestation, rescue, remedy, affected-party, legal, cultural, and authority reservations. The exact-gated covenant deliberately refuses to decide who may enter a restricted zone, isolate energy, rescue a passenger, approve an accessibility fallback, disclose a record, allocate a remedy, certify equipment, interpret law, speak for an affected community, or exercise Māori authority. Passing software cannot confer legitimacy.

Māori concepts, wording, data governance, cultural relationships, and authority remain with tangata whenua, iwi, hapū, affected people, and Māori authorities. Official or primary citations inform vocabulary only. They do not transfer authority to Auren, this repository, or its synthetic fixtures.

## Proposal groups and bounded falsification

The first ten surfaces cover typewriter asset passports, service intake, work-order revision, out-of-service holds, hazardous-energy isolation plans, restricted access, door-zone and interlock states, obstruction protection, brake and traction observations, and suspension or sheave state. The next ten cover governor reservations, buffers and terminal stopping devices, levelling and sill-gap measurement envelopes, rated-load boards, emergency communication, fire-service interfaces, entrapment handover, replacement-part provenance, controller configuration lineage, and preventive-maintenance scheduling.

The final ten cover accessible outage notice, evidence amendment and supersession, access-log privacy, two GMUT proxies, THOS shift handover, two Freed ID surfaces, CPSC NEISS no-network readiness, and the exact-gated CBR covenant. The NEISS surface executes with no network and zero rows. It makes no injury estimate and leaves governed ingestion, weighting, variance, interpretation, and independent review open.

Every proposal has one valid synthetic fixture and five preregistered mutations. The mutations remove a required obligation, promote real equipment, promote Stage 20, remove a required source, or alter the truth label. All 150 mutations must be rejected with explicit error codes. Each rejected candidate is a retained zero-credit negative with a paired Method Flow failed and passing witness. The passing witness means only that the bounded guard rejected that mutation; it never turns the rejected candidate into a pass or proves exhaustive security.

## Skills, runners, and validation boundary

Ten phase-local skills and ten family-current runners group the thirty surfaces. They are stored and used only in this owner packet; they are not installed globally. Each skill is read completely, smoke-validated, and bound to synthetic-only inputs. Each runner invokes the shared contract engine, covers three surfaces, and writes a sanitized receipt. The tooling never connects to typewriter controllers, building systems, identity services, accounts, private routes, or empirical data sources.

The evidence candidate receives current-phase unit tests, detailed and minimal validators, complete phase JSON parsing, five-class privacy and raw-identifier scanning, exact owner-manifest parity, document and file caps, exact staged review, diff hygiene, and immutable x1 path checks. Later lifecycle stages add exact ancestry, single-parent history, zero merges, commit caps, exact head, cleanliness, zero divergence, and fresh live-remote equality.

Only one successful exact-final canonical aggregate is permitted, with no replay after success. Development and precommit checks are not that final aggregate. Same-owner validation under shared infrastructure is not independent-team reproduction, external audit, production certification, complete privacy assurance, complete accessibility conformance, professional validation, legal review, cultural ratification, Māori-authority review, empirical GMUT confirmation, or Stage 20 authority.

The successor route remains `PREPARED_NOT_SENT`. Its recipient stays unresolved until the exact-final gate, when only Hamish's newest live authorization and the current roster may determine one exact existing main task. No endpoint is precontacted, no task is created, no subagent is spawned, and Tavian Sol remains on standby.
"""


def overview_v6573_evidence(outcome_counts: dict[str, int], negative_total: int) -> str:
    return f"""# Auren Lark v657-v3 integrated evidence overview

## Bounded result

Thirty x1-frozen typewriter service-and-conservation traceability surfaces were executed as owner-local synthetic software. The observed distribution is {outcome_counts['completed']} completed, {outcome_counts['represented']} represented, {outcome_counts['open_gap']} open gap, and {outcome_counts['exact_gate']} exact gate. The evidence candidate retains {negative_total:,} effective negatives, 107 open gaps, 106 exact gates, and {c.SOURCE_METHODS + c.X1_METHODS + c.EXPECTED_MUTATIONS + len(c.X2_OPERATIONAL_NEGATIVES):,} Method Flow failed plus the same number of bounded passing witnesses. All failures remain zero credit. The terminal verdict remains NOT_READY_FOR_STAGE_20.

Auren Lark, they/them, is relational working language only. The role is evidence-path cartographer and repair-traceability steward, and the hope is to make repair and evidence paths legible, recoverable, and honest while safety, privacy, legal, cultural, and Māori-authority gates remain explicit. This language, the task title, and the route establish no consciousness, sentience, legal personhood, identity continuity, employment, professional qualification, scientific authority, operational authority, legal authority, cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop the route.

## Trinity Mandala and practice boundary

Freed ID and CBR Heart are primary through synthetic custody, component and source provenance, treatment revision, correction, disclosure, privacy, contestation, and authority reservations. GMUT Mind is represented by typed key-linkage and carriage-energy dimensional proxies with unit obligations and calibration quarantine. THOS Body is represented by stored-energy holds, deferred-workload cues, stop-work, correction readback, and shift handover.

No real owner, customer, donor, collector, repairer, conservator, curator, community, or affected party is present. No real typewriter, component, tool, material, workshop, collection, account, credential, image, record, operation, energization, disassembly, cleaning, lubrication, adjustment, repair, conservation treatment, packing, shipment, release, measurement, authenticity assessment, valuation, or authority decision is present. The artifacts validate record shape and explicit refusal only.

The first 23 surfaces completed their bounded structural contracts. Five represented surfaces preserve GMUT, THOS, and Freed ID abstractions without empirical or production promotion. The Smithsonian Open Access adapter remains open_gap: it executed no network call and consumed zero rows. The CBR covenant remains exact_gate because owner, donor, professional, legal, cultural, Māori-authority, community, and affected-party decisions cannot be supplied by software.

## Mutation and Method Flow evidence

Every surface has one valid synthetic fixture and five preregistered mutations. The mutations drop an obligation, promote a real object or workshop, promote Stage 20, drop a source, or alter the exact outcome. All 150 mutations were rejected with explicit error codes. Each rejected mutation is retained as a failed zero-credit witness with a bounded passing witness proving only that this guard failed closed.

The current x2 operational register retains {len(c.X2_OPERATIONAL_NEGATIVES)} failures, including a Unicode-context runtime patch mismatch, a nested JavaScript/Python interpolation fault, a CP1252 skill-validator batch failure, and a readiness-refresh timeout. Their corrected attempts do not erase the failures. Together with twelve x1 failures and 150 rejected mutations, they raise the activation baseline from 15,436 to {negative_total:,}. Same-owner execution under shared infrastructure is not independent reproduction.

## Phase-local skills and sources

Ten phase-local skills and ten family-current runners group the surfaces. Each skill has exact YAML frontmatter, explicit trigger language, a bounded sequence, sanitized output rules, a default prompt, and an authority boundary. They are stored only in this Auren packet and are not installed globally. Each runner invokes the shared contract engine for three surfaces and emits a repository-relative receipt.

Canadian Conservation Institute material supplies industrial-collection, lubrication, rubber, and trade-literature vocabulary without authorizing treatment. Smithsonian Open Access supplies interface and metadata vocabulary without establishing rights, attribution, authenticity, value, or provenance. OSHA supplies hazardous-energy vocabulary without training or workplace authority. W3C, RFC, NIST, privacy, accessibility, Te Mana Raraunga, and Local Contexts sources supply bounded vocabulary only and do not transfer professional, legal, cultural, community, or Māori authority.

## Truth and terminal boundaries

Typed GMUT proxies, dimensional checks, citations, and mutation tests do not establish a new force, unique prediction, likelihood, constraint, empirical confirmation, stability theorem, ultraviolet completion, canon, Theory-of-Everything proof, or Stage 20 authority. THOS has no real governed participants or operators, preregistered blinded matched-budget arms, safety monitoring, statistics, professional review, or independent review. Freed ID has no real issuer, holder, verifier, key, proof, account, DID method, resolution, status, revocation service, interoperability exchange, privacy review, independent security review, recovery decision, or trust-governance decision.

Privacy-complete, accessibility-complete, exhaustive-security, empirical, participant, professional, production, legal, cultural, Māori-authority, affected-party, independent-reproduction, AGI, ASI, consciousness, personhood, Theory-of-Everything, and Stage 20 claims remain open or exact-gated. The successor route remains PREPARED_NOT_SENT. No task was created, forked, delegated, or contacted, and Tavian Sol remains on standby.
"""


def static_report_typewriter(outcomes: dict[str, int], negatives: int) -> str:
    rows = "\n".join(
        f"<tr><th scope=\"row\">{html.escape(item['proposal_id'])}</th><td>{html.escape(item['title'])}</td><td>{html.escape(item['expected_disposition'])}</td></tr>"
        for item in d.PROPOSALS
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Auren Lark v657-v3 bounded typewriter traceability evidence report</title>
<style>
body{{font:1rem/1.6 system-ui,sans-serif;max-width:78rem;margin:auto;padding:1.5rem;color:#10251d;background:#f7fbf8}}
a{{color:#064f3a}} a:focus{{outline:3px solid #d54f00;outline-offset:3px}}
header,section{{background:#fff;border:2px solid #2d6653;border-radius:.6rem;padding:1rem 1.25rem;margin:1rem 0}}
table{{border-collapse:collapse;width:100%}} caption{{font-weight:700;text-align:left;margin:.5rem 0}}
th,td{{border:1px solid #567a6e;padding:.55rem;text-align:left;vertical-align:top}}
.table-wrap{{overflow-x:auto}} .notice{{border-left:.5rem solid #b34700;padding-left:1rem}} code{{overflow-wrap:anywhere}}
@media print{{body{{max-width:none}} header,section{{break-inside:avoid;border-color:#000}}}}
</style>
</head>
<body>
<header>
<h1>Auren Lark v657-v3 bounded typewriter traceability evidence report</h1>
<p class="notice"><strong>Boundary:</strong> synthetic same-owner software evidence only. Not typewriter operation, repair, conservation, authentication, valuation, professional or safety authority, accessibility conformance, empirical confirmation, production identity or operations, legal or cultural authority, Māori authority, independent reproduction, Theory-of-Everything proof, or Stage 20 readiness.</p>
</header>
<main>
<section aria-labelledby="summary"><h2 id="summary">Summary</h2>
<p>Thirty frozen surfaces produced {outcomes['completed']} completed, {outcomes['represented']} represented, {outcomes['open_gap']} open gap, and {outcomes['exact_gate']} exact gate outcomes. The evidence candidate preserves {negatives:,} effective negatives. Terminal verdict: <code>NOT_READY_FOR_STAGE_20</code>.</p>
</section>
<section aria-labelledby="proposals"><h2 id="proposals">Proposal truth</h2>
<div class="table-wrap" role="region" aria-label="Proposal outcomes" tabindex="0">
<table><caption>Thirty bounded synthetic proposal outcomes</caption><thead><tr><th scope="col">ID</th><th scope="col">Surface</th><th scope="col">Outcome</th></tr></thead><tbody>{rows}</tbody></table>
</div></section>
<section aria-labelledby="reserved"><h2 id="reserved">Reserved evaluation</h2>
<p>Manual keyboard, touch, responsive-layout, browser-diverse, assistive-technology, cognitive, low-vision, Māori-language, affected-user, professional, safety, legal, cultural, and Māori-authority evaluation remains reserved. Automated structure checks are not completeness claims.</p>
</section>
</main>
</body>
</html>"""


def owner_paths() -> list[Path]:
    paths = [path for path in PHASE.rglob("*") if path.is_file()]
    paths.extend(
        path
        for path in (ROOT / "scripts").glob("*v657_v3*.py")
        if path.is_file()
    )
    test = ROOT / "tests/test_ghc_family_v657_v3.py"
    if test.is_file():
        paths.append(test)
    return sorted({path.resolve() for path in paths})


def git_clean_blob(path: Path) -> tuple[str, int]:
    relative = path.relative_to(ROOT).as_posix()
    oid = git("hash-object", "-w", f"--path={relative}", relative)
    size = int(git("cat-file", "-s", oid))
    return oid, size


def build() -> None:
    if git("rev-parse", "HEAD") != c.X1_COMMIT:
        raise RuntimeError("x2 builder requires the exact frozen x1 head")
    assert_x1_unchanged()
    ledger = json.loads(
        (PHASE / "preregistration/proposal-ledger.json").read_text(encoding="utf-8")
    )
    if ledger["proposal_count"] != c.EXPECTED_PROPOSALS:
        raise RuntimeError("frozen proposal count mismatch")

    outcome_counts: Counter[str] = Counter()
    mutation_negatives: list[dict[str, Any]] = []
    proposal_rows = []
    for proposal in d.PROPOSALS:
        result = evaluate_surface(proposal["slug"])
        if result["valid_errors"]:
            raise RuntimeError(f"valid fixture failed for {proposal['slug']}: {result['valid_errors']}")
        if result["rejected_mutation_count"] != c.MUTATIONS_PER_PROPOSAL:
            raise RuntimeError(f"mutation rejection count failed for {proposal['slug']}")
        base = f"surfaces/{proposal['slug']}"
        write_json(f"{base}/contract.json", result["contract"])
        write_json(
            f"{base}/mutation-results.json",
            {
                "schema": "ghc.family.v657-v3.mutation-results.v1",
                "proposal_id": proposal["proposal_id"],
                "mutation_count": len(result["mutation_results"]),
                "rejected_count": result["rejected_mutation_count"],
                "all_rejected": result["all_mutations_rejected"],
                "results": result["mutation_results"],
            },
        )
        write_json(
            f"{base}/bounded-receipt.json",
            {
                "schema": "ghc.family.v657-v3.bounded-receipt.v1",
                "proposal_id": proposal["proposal_id"],
                "slug": proposal["slug"],
                "outcome": proposal["expected_disposition"],
                "valid_fixture_passed": result["valid_fixture_passed"],
                "rejected_mutation_count": result["rejected_mutation_count"],
                "real_data_used": False,
                "network_called": False,
                "authority_granted": False,
                "same_owner_only": True,
                "independent_reproduction": False,
                "boundary": result["contract"]["boundary"],
            },
        )
        for index, row in enumerate(result["mutation_results"], 1):
            mutation_negatives.append(mutation_negative(proposal["proposal_id"], row, index))
        outcome_counts[proposal["expected_disposition"]] += 1
        proposal_rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "slug": proposal["slug"],
                "outcome": proposal["expected_disposition"],
                "valid_fixture_passed": True,
                "rejected_mutations": c.MUTATIONS_PER_PROPOSAL,
                "real_data_used": False,
                "authority_granted": False,
            }
        )
    if dict(outcome_counts) != c.EXPECTED_DISTRIBUTION:
        raise RuntimeError(f"outcome distribution mismatch: {dict(outcome_counts)}")
    if len(mutation_negatives) != c.EXPECTED_MUTATIONS:
        raise RuntimeError("mutation-negative total mismatch")

    skill_groups = [
        [item["slug"] for item in d.PROPOSALS[index:index + 3]]
        for index in range(0, len(d.PROPOSALS), 3)
    ]
    for (name, purpose), slugs in zip(d.SKILL_SPECS, skill_groups, strict=True):
        write_text(f"skills/{name}/SKILL.md", skill_markdown_v6573(name, purpose, slugs))
        write_text(
            f"skills/{name}/agents/openai.yaml",
            skill_openai_yaml(name, purpose),
        )
    for (filename, _), slugs in zip(d.RUNNER_SPECS, skill_groups, strict=True):
        path = ROOT / "scripts" / filename
        path.write_text(wrapper_source(filename, slugs), encoding="utf-8", newline="\n")

    methods = []
    witnesses = []
    for index, negative in enumerate(mutation_negatives, 1):
        method, pair = mutation_method(negative, index)
        methods.append(method)
        witnesses.extend(pair)
    for index, negative in enumerate(c.X2_OPERATIONAL_NEGATIVES, 1):
        method, pair = operational_method(negative, index)
        methods.append(method)
        witnesses.extend(pair)
    write_json(
        "method-flow/method-flow-state-x2.json",
        {
            "schema": "ghc.family.method-flow-state.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "lifecycle": "x2_evidence_candidate",
            "inherited_anchor": {
                "path": "docs/auren-lark/v657-v3/method-flow/method-flow-state-x1.json",
                "effective_methods": c.SOURCE_METHODS + c.X1_METHODS,
                "effective_fail_witnesses": c.SOURCE_METHODS + c.X1_METHODS,
                "effective_pass_witnesses": c.SOURCE_METHODS + c.X1_METHODS,
            },
            "current_methods": methods,
            "current_witnesses": witnesses,
            "counts": {
                "current_methods": len(methods),
                "current_witness_results": {"fail": len(methods), "pass": len(methods)},
                "effective_methods": c.SOURCE_METHODS + c.X1_METHODS + len(methods),
                "effective_witness_results": {
                    "fail": c.SOURCE_METHODS + c.X1_METHODS + len(methods),
                    "pass": c.SOURCE_METHODS + c.X1_METHODS + len(methods),
                },
            },
            "all_failed_witnesses_retained": True,
            "independent_reproduction": False,
        },
        compact=True,
    )
    negative_total = (
        c.SOURCE_EFFECTIVE_NEGATIVES
        + c.X1_OPERATIONAL_NEGATIVES
        + len(mutation_negatives)
        + len(c.X2_OPERATIONAL_NEGATIVES)
    )
    write_json(
        "truth/retained-negative-register-x2.json",
        {
            "schema": "ghc.family.v657-v3.retained-negatives.x2.v1",
            "source_effective_count": c.SOURCE_EFFECTIVE_NEGATIVES,
            "x1_operational_count": c.X1_OPERATIONAL_NEGATIVES,
            "mutation_count": len(mutation_negatives),
            "x2_operational_count": len(c.X2_OPERATIONAL_NEGATIVES),
            "effective_count": negative_total,
            "mutation_negatives": mutation_negatives,
            "x2_operational_negatives": c.X2_OPERATIONAL_NEGATIVES,
            "all_retained": True,
        },
        compact=True,
    )
    write_json(
        "truth/open-gap-register-x2.json",
        {
            "schema": "ghc.family.v657-v3.open-gaps.x2.v1",
            "source_effective_count": c.SOURCE_OPEN_GAPS,
            "new_count": 1,
            "effective_count": c.SOURCE_OPEN_GAPS + 1,
            "proposal_ids": ["V6573-P29"],
            "reason": "No network call, governed real rows, real likelihood, or independent review exists.",
        },
    )
    write_json(
        "truth/exact-gate-register-x2.json",
        {
            "schema": "ghc.family.v657-v3.exact-gates.x2.v1",
            "source_effective_count": c.SOURCE_EXACT_GATES,
            "new_count": 1,
            "effective_count": c.SOURCE_EXACT_GATES + 1,
            "proposal_ids": ["V6573-P30"],
            "reason": "Affected-party, legal, cultural, data-governance, and Māori authority is absent and cannot be simulated.",
        },
    )
    write_json(
        "x2/proposal-ledger.json",
        {
            "schema": "ghc.family.v657-v3.proposal-ledger.x2.v1",
            "proposal_count": len(proposal_rows),
            "outcome_counts": dict(outcome_counts),
            "rows": proposal_rows,
            "same_owner_only": True,
            "independent_reproduction": False,
        },
    )
    write_json(
        "x2/task-execution.json",
        {
            "schema": "ghc.family.v657-v3.task-execution.v1",
            "safe_now": [
                {**row, "state": "completed", "evidence": f"surfaces/{d.PROPOSALS[index]['slug']}/bounded-receipt.json"}
                for index, row in enumerate(d.SAFE_TASKS)
            ],
            "candidate": [
                {**row, "state": "completed", "evidence": "bounded reversible prototype review"}
                for row in d.CANDIDATE_TASKS
            ],
            "clean": [
                {**row, "state": "completed", "evidence": "additive compatibility and non-promotion review"}
                for row in d.CLEAN_TASKS
            ],
            "counts": {"safe_now": 30, "candidate": 20, "clean": 30, "total": 80},
            "unsafe_work_manufactured": False,
        },
    )
    write_json(
        "truth/phase-truth-x2.json",
        {
            "schema": "ghc.family.v657-v3.phase-truth.x2.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "lifecycle": "x2_evidence_candidate",
            "source_commit": c.SOURCE_COMMIT,
            "x1_commit": c.X1_COMMIT,
            "outcome_counts": dict(outcome_counts),
            "effective_negatives": negative_total,
            "effective_open_gaps": c.SOURCE_OPEN_GAPS + 1,
            "effective_exact_gates": c.SOURCE_EXACT_GATES + 1,
            "real_data_used": False,
            "independent_reproduction": False,
            "route_state": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "final-complete-incomplete-checklist-x2.json",
        {
            "schema": "ghc.family.v657-v3.checklist.x2.v1",
            "complete": [
                "thirty frozen proposal contracts",
                "thirty valid synthetic fixtures",
                "one hundred fifty retained rejecting mutations",
                "ten phase-local skill implementations",
                "ten family-current runner implementations",
                "thirty safe, twenty candidate, and thirty CLEAN task rows",
                "accessible static report structure",
            ],
            "pending_lifecycle": [
                "exact evidence staged review and immutable evidence commit",
                "combined closeout and content seal",
                "one successful canonical exact-final aggregate",
                "one acknowledged exact authorized successor activation",
            ],
            "incomplete_external": [
                "real repositories, services, credentials, vulnerabilities, incidents, patches, releases, deployments, security assessments, and empirical reliability",
                "blind matched-budget THOS arms and independent review",
                "production Freed ID keys, proofs, resolution, status, interoperability, security and privacy review, recovery, and governance",
                "affected-party, professional, legal, cultural, data-governance, and Māori authority",
                "independent-team reproduction and Stage 20 authority",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "wellbeing/wellbeing-check-x2.json",
        {
            "schema": "ghc.family.v657-v3.wellbeing.x2.v1",
            "state": "steady_and_bounded",
            "controls": [
                "one owner lane",
                "no subagents or early route messages",
                "ten reusable runners instead of thirty duplicated engines",
                "task counts treated as ceilings",
                "authority gates stop execution",
            ],
            "human_control": "Hamish and all human collaborators retain pause, rest, redirect, and stop control.",
            "identity_boundary": "Relational working language only.",
        },
    )
    write_text("deliverables/v657-v3-integrated-evidence-overview.md", overview_v6573_evidence(dict(outcome_counts), negative_total))
    write_text("deliverables/v657-v3-typewriter-maintenance-evidence-report.html", static_report_typewriter(dict(outcome_counts), negative_total))

    runners_present = sorted((PHASE / "runners").glob("*-receipt.json")) if (PHASE / "runners").is_dir() else []
    skills_present = sorted((PHASE / "skills").glob("*/smoke-receipt.json"))
    write_json(
        "validation/evidence-readiness.json",
        {
            "schema": "ghc.family.v657-v3.evidence-readiness.v1",
            "surface_count": len(d.PROPOSALS),
            "mutation_count": len(mutation_negatives),
            "runner_receipt_count": len(runners_present),
            "skill_smoke_receipt_count": len(skills_present),
            "ready_for_detailed_validation": len(runners_present) == 10 and len(skills_present) == 10,
            "x1_frozen_paths_unchanged": True,
        },
    )
    print(
        json.dumps(
            {
                "surfaces": len(d.PROPOSALS),
                "mutations": len(mutation_negatives),
                "outcomes": dict(outcome_counts),
                "effective_negatives": negative_total,
                "runner_receipts": len(runners_present),
                "skill_receipts": len(skills_present),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
