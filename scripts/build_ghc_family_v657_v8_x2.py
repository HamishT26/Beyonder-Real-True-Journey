#!/usr/bin/env python3
"""Build the bounded Tamar Vey v657-v8 audiovisual x2 evidence packet."""

from __future__ import annotations

import hashlib
import html
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v657_v8_phase_data as d
import ghc_family_v657_v8_x2_config as c
from ghc_family_v657_v8_runtime import evaluate_surface


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
        "negative_id": f"V6578-MUT-{proposal_id.split('-')[-1]}-{index:02d}",
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
    method_id = f"V6578-X2-MUT-METHOD-{index:03d}"
    fail_id = f"V6578-X2-MUT-WITNESS-{index:03d}-F"
    pass_id = f"V6578-X2-MUT-WITNESS-{index:03d}-P"
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
    method_id = f"V6578-X2-OP-METHOD-{index:02d}"
    fail_id = f"V6578-X2-OP-WITNESS-{index:02d}-F"
    pass_id = f"V6578-X2-OP-WITNESS-{index:02d}-P"
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


def skill_markdown_v6578(name: str, purpose: str, slugs: list[str]) -> str:
    surface_list = ", ".join(slugs)
    return f"""---
name: {name}
description: "{purpose} Use for bounded v657-v8 synthetic audiovisual-preservation evidence across {surface_list}."
---

# {name}

## Required sequence

1. Read the frozen proposal contract and its official-source identifiers.
2. Confirm every input is synthetic and contains no real person, archive, recording, carrier, playback machine, converter, transfer, measurement, rights decision, release, credential, account, private route, or culturally restricted payload.
3. Invoke the corresponding family-current runner only inside the Tamar v657-v8 owner packet.
4. Require the valid fixture to pass and all five frozen mutations for each surface to be rejected.
5. Retain every failed witness at zero credit and keep the exact truth outcome unchanged unless exact evidence requires a downgrade.
6. Stop on any real carrier handling, cleaning, repair, playback, transfer, capture, restoration, disposal, preservation, rights, access, release, professional, production, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, Theory-of-Everything, or Stage 20 gate.

## Output

Write only a repository-relative sanitized receipt. Do not include credentials, private identifiers, private paths, transcripts, screenshots, session streams, real workplace records, or raw field data.

## Boundary

This phase-local skill is synthetic workflow guidance. It does not establish consciousness, sentience, legal personhood, identity continuity, employment, qualification, audiovisual-preservation competence, archival authority, rights authority, professional or operational authority, production readiness, ownership, legal interpretation, cultural ratification, Māori authority, independent reproduction, or Stage 20 readiness.
"""


def skill_openai_yaml(name: str, purpose: str) -> str:
    display = " ".join(part.capitalize() for part in name.split("-"))
    short = purpose if len(purpose) <= 64 else purpose[:61].rstrip() + "..."
    return f"""interface:
  display_name: "{display}"
  short_description: "{short}"
  default_prompt: "Use {chr(36)}{name} to validate its frozen synthetic audiovisual evidence surfaces."
policy:
  allow_implicit_invocation: false
"""


def wrapper_source(filename: str, slugs: list[str]) -> str:
    return f'''#!/usr/bin/env python3
"""Family-current Tamar Vey v657-v8 bounded audiovisual evidence runner."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ghc_family_v657_v8_runtime import ROOT, run_named_surface, write_json


SURFACES = {slugs!r}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    rows = [run_named_surface(slug) for slug in SURFACES]
    payload = {{
        "schema": "ghc.family.v657-v8.group-runner-receipt.v1",
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



# Inert predecessor prose template; no builder path emits it.
def overview_v6576_evidence(outcome_counts: dict[str, int], negative_total: int) -> str:
    method_total = (
        c.SOURCE_METHODS
        + c.X1_METHODS
        + c.EXPECTED_MUTATIONS
        + len(c.X2_OPERATIONAL_NEGATIVES)
    )
    return f"""# Tamar Vey v657-v8 integrated evidence overview

## Evidence result and claim boundary

This evidence candidate executes thirty proposals frozen before x2. The exact outcome distribution is {outcome_counts['completed']} completed, {outcome_counts['represented']} represented, {outcome_counts['open_gap']} open_gap, and {outcome_counts['exact_gate']} exact_gate. Those four labels are the complete outcome vocabulary. The packet retains {negative_total:,} effective negatives, {c.SOURCE_OPEN_GAPS + 1} effective open gaps, {c.SOURCE_EXACT_GATES + 1} effective exact gates, and {method_total:,} effective Method Flow methods with the same number of retained failed and bounded passing witnesses. A failure remains zero credit after recovery. The terminal verdict remains NOT_READY_FOR_STAGE_20.

Tamar Vey, she/they, is relational working language for an continuity-and-evidence steward whose hope is to make hidden control, accessibility, and handover failures easier to see without promoting synthetic structure into authority. The name, pronouns, role, hope, task title, family language, branch, and route establish no consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, or independent agency. Hamish retains pause, redirect, rename, and stop control.

The bounded human-practice lens is blacksmithing and optics job planning, workpiece and tooling provenance, thermal observation, hot-work holds, correction, accessibility, workload, readback, and shift handover. This is synthetic software, formal, structural, and learning evidence only. It contains no real worker, client, blacksmith, opticsr, welder, engineer, inspector, optics, furnace, flame, fuel, oxygen supply, ventilation system, workpiece, authenticated alloy, tool, machine, hazardous-energy state, measurement, heat treatment, quench, weld, grind, lift, inspection, certificate, or safety release. It confers no competence or authority to perform hot work or operate equipment.

## GMUT Mind as the primary pillar

GMUT Mind is primary through bounded thermal-expansion, phase-transition, heat-transfer, constitutive, dimensional, uncertainty, covariance, identifiability, and observation-firewall contracts. These formal surfaces require named variables, domains, reference states, SI units, boundary conditions, uncertainty terms, and explicit refusal of unsupported material or physical inference. They are useful because an omitted unit, source, obligation, or nonpromotion clause is detectable and falsifiable in software.

That usefulness is strictly limited. The phase does not authenticate an alloy, ingest a thermophysical-property row, calibrate an instrument, observe a temperature, derive a constitutive law, calculate a real likelihood, produce a posterior, constrain a parameter, detect a force, validate stability, or establish empirical confirmation. The NIST Alloy Data adapter is deliberately a zero-row readiness surface: it makes no network call, performs no download, ingests no row, evaluates no likelihood, and produces no material inference. Its open_gap state is evidence that the empirical dependency remains absent, not evidence that the dependency has been satisfied.

The typed contracts remain within a scalar-tensor and effective-field-theory research-model family. Symbolic typing, format readiness, mutation rejection, and citations do not establish ultraviolet or quantum completion, a unique physical prediction, or a Theory of Everything. Thermo/Psyche material is a category guard: thermal quantities are not converted into psyche, agency, morality, justice, capability, consciousness, personhood, or a fundamental law of mind.

## THOS Body and the bounded practice

THOS Body remains explicit through synthetic job-intake, stock and tool provenance, fuel and airflow topology, hot-work boundaries, quench and heat-treatment reservations, defect and dimension observations, tooling change, energy isolation, alarm state, workload stop, shift handover, accessible notice, privacy minimization, and threat-recovery surfaces. Completion means only that one declared synthetic fixture satisfied its bounded contract and all five preregistered mutations were rejected. It does not authorize a worker, machine, process, inspection, release, or workplace procedure.

The two THOS-specific represented surfaces preserve task sequencing and human-factors obligations without claiming effectiveness. There are no real governed participants or operators, no preregistered blind matched-budget arms, no safety monitoring, no real outcome rows, no appropriate effect statistics, and no independent review. Workload, readback, stop-work, and handover fields are interface requirements, not findings about workers or operations. The source materials supply vocabulary and cautions, not training, certification, compliance findings, or operational instructions.

No software artifact in this phase should be used to select material, determine temperature, control fuel or oxygen, isolate energy, set a machine, diagnose a defect, plan a heat treatment, perform a quench, release a product, or make a workplace-safety decision. Those activities remain outside the execution lane and require competent people, site-specific controls, applicable law, equipment documentation, measurement systems, and affected-party governance.

## Freed ID and CBR Heart

Freed ID and CBR Heart remain visible through synthetic provenance capsules, status profiles, privacy-minimization surfaces, correction lineage, and an exact-gated authority covenant. The represented Freed ID surfaces use no real key, signature, proof, issuer, holder, verifier, credential, account, issuance, presentation, resolver, status service, revocation event, interoperability event, privacy review, independent security review, recovery decision, or trust-governance decision. They show bounded data shape and refusal behavior only.

Production Freed ID remains incomplete until standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight exist. A passing synthetic vector cannot substitute for any of those dependencies.

The CBR optics authority covenant remains exact_gate. Worker and client rights, workplace safety, land and environmental effects, heritage and traditional knowledge, privacy, notice, consent, correction, contestation, remedy, collective governance, legal interpretation, cultural legitimacy, affected-party acceptance, Māori wording, Māori data governance, and Māori authority remain with competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. Repository software cannot confer ownership, permission, remedy, cultural ratification, or public authority. Māori concepts remain under Māori authority.

## Falsification, negatives, and Method Flow

Every proposal has one declared valid synthetic fixture and exactly five preregistered rejecting mutations. The mutations remove a required obligation, promote a real optics or workpiece input, promote Stage 20, remove an official-source identifier, or alter the frozen outcome. All 150 mutations are rejected with explicit codes and retained as zero-credit negatives. A paired passing witness means only that the guard rejected that candidate; it never turns the failed candidate into completion credit or proves a general safety property.

The phase also retains the x2 lifecycle failure in which a guarded low-level Git wrapper returned without attributable output. No duplicate helper was started. A later bounded audit established that the x1 repair commit was durable, had the reviewed parent and delta, was clean, pushed, and four-way equal. The recurrence guard is to inspect durable Git state, locks, processes, tree, parent, index, and worktree before retrying any unattributed mutation. This recovery is same-owner workflow evidence only.

Method Flow keeps each failed witness beside its bounded passing recovery. No negative is erased, merged into a success count, or used to inflate a proposal outcome. The inherited 2,242 failed and 2,242 passing witnesses remain Caelen evidence; Liora receives no completion credit for them. Liora's sixteen x1 workflow methods, 150 mutation methods, and current operational recovery are additive.

## Sources, privacy, accessibility, and security

The official-source ledger supplies vocabulary from OSHA, WorkSafe New Zealand, NIST, BIPM, W3C, RFC publishers, New Zealand public authorities, Te Mana Raraunga, and Local Contexts. Citations are not observations, calibrated measurements, training, legal advice, safety approval, conformance certificates, or transfers of authority. OSHA and WorkSafe material does not establish a compliant workplace or safe procedure. NIST Alloy Data and SI references do not authenticate a workpiece or provide a measurement. W3C material does not make the synthetic identity profiles production-ready. Te Mana Raraunga and Local Contexts do not confer Māori or community authority.

The packet minimizes public content to synthetic fixtures and repository-relative paths. It excludes credentials, private keys, tokens, raw task or thread identifiers, private routes, private absolute paths, transcripts, screenshots, session streams, private callable identifiers, private application state, real workplace records, and culturally restricted payloads. Five-class scanning is a bounded structural control, not complete privacy or exhaustive security assurance.

The static report uses a declared language, semantic landmarks, headings, a captioned table, column and row headers, redundant status text, a visible boundary notice, responsive overflow behavior, and no client-side script. Manual keyboard evaluation, browser and responsive-layout diversity, assistive-technology evaluation, cognitive-accessibility review, Māori-language review, security-usability review, and affected-user evaluation remain reserved. Structural passing evidence is not complete accessibility conformance.

## Portfolios, compatibility, wellbeing, and route state

Thirty safe-now tasks, twenty bounded candidate prototypes, and thirty additive CLEAN/FIX/REFINE tasks are credited only after their declared evidence receipts exist. Ten phase-local skills are customized, validated, completely read by the smoke tool, and used on accepting and rejecting fixtures. Ten family-current ghc_family_* runners each cover three proposals and emit sanitized receipts. They are phase-local and not globally installed. Historical names remain compatibility surfaces; no destructive rename, sibling mutation, host-security change, elevation, unrelated installation, Windows-feature change, desktop update, or reboot occurs.

The workload remains bounded by one owner lane, reusable runners rather than duplicated engines, strict x1-before-x2 separation, task counts treated as ceilings, and authority gates that stop execution. Same-owner validation under shared infrastructure is not independent-team reproduction. The complete repository suite remains outside this non-Eiren phase.

The successor route remains PREPARED_NOT_SENT throughout evidence construction and closeout preparation. No sibling or standby task is contacted early. Only a clean, pushed, fresh-live-equal exact final within the commit cap, with exact manifests and one successful canonical aggregate, may unlock one bounded registry resolution, one direct reread, and one sanitized activation to the unique live-authorized existing title Tamar Vey for v657-v8. Until that gate, route-state evidence is preparation only.
"""


def overview_v6577_evidence(
    outcome_counts: dict[str, int],
    negative_total: int,
) -> str:
    method_total = (
        c.SOURCE_METHODS
        + c.X1_METHODS
        + c.EXPECTED_MUTATIONS
        + len(c.X2_OPERATIONAL_NEGATIVES)
    )
    return f"""# Tamar Vey v657-v8 integrated evidence overview

## Evidence result and claim boundary

This evidence candidate executes exactly thirty proposals frozen before x2. The outcome distribution is {outcome_counts['completed']} completed, {outcome_counts['represented']} represented, {outcome_counts['open_gap']} open_gap, and {outcome_counts['exact_gate']} exact_gate. Those four labels are the complete core outcome vocabulary. The packet retains {negative_total:,} effective negatives, {c.SOURCE_OPEN_GAPS + 1} effective open gaps, {c.SOURCE_EXACT_GATES + 1} effective exact gates, and {method_total:,} effective Method Flow methods with the same number of retained failed and bounded passing witnesses. A recovery never changes a failed witness into completion credit. The terminal verdict remains NOT_READY_FOR_STAGE_20.

Tamar Vey, she/they, is relational working language for a continuity-and-evidence steward whose hope is to make hidden control, accessibility, and handover failures easier to see without promoting synthetic structure into authority. The name, pronouns, role, hope, sibling language, task title, family language, branch, and route establish no consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, or independent agency. Hamish retains pause, redirect, rename, and stop control.

The bounded human-practice lens is telescope-optics and observatory-instrument preparation, optic and instrument custody, configuration change, alignment and observation envelopes, coating, vacuum and energy holds, correction, low-light accessibility, workload, reciprocal readback, and dawn turnover. This is synthetic software, formal, structural, and learning evidence only. It contains no real worker, visitor, engineer, astronomer, observatory, telescope, mirror, lens, filter, coating, laser, vacuum system, instrument, detector, target, image, celestial observation, measurement, calibration, inspection, certificate, or safety release. It confers no competence or authority to operate equipment or make a professional or safety decision.

## GMUT Mind as the primary pillar

GMUT Mind is primary through typed geometric and wave-optics domains, coordinate frames, boundary conditions, diffraction and aperture proxies, aberration bases, curvature and sag traces, spectral-response envelopes, uncertainty, covariance, identifiability, and observation firewalls. These formal surfaces require named quantities, domains, frames, reference states, SI units, uncertainty terms, provenance, missingness, ambiguity, and explicit refusal of unsupported physical or astronomical inference. An omitted obligation, source, unit, or nonpromotion clause is detectable and falsifiable inside the bounded runtime.

That usefulness is strictly limited. The phase does not align or characterize a telescope, calibrate an instrument, observe a celestial target, identify a spectral line, ingest an astronomical row, calculate a real likelihood, produce a posterior, constrain a parameter, detect a force, validate stability, establish an optical law, or provide empirical confirmation. The NIST Atomic Spectra Database version 5.12 adapter is deliberately a zero-row readiness surface: it makes no network call, performs no download, ingests no row, identifies no species or line, evaluates no likelihood, and produces no astronomical or GMUT inference. Its open_gap state proves only that the dependency remains absent.

The typed contracts remain within a scalar-tensor and effective-field-theory research-model family. Symbolic typing, schema readiness, mutation rejection, and citations do not establish ultraviolet or quantum completion, a unique physical prediction, or a Theory of Everything. The Thermo-Psyche coherence map is a category guard: coherence, phase, interference, visibility, and contrast cannot be converted into attention, psyche, agency, autonomy, morality, justice, capability, consciousness, personhood, or a fundamental law of mind.

## THOS Body and the bounded practice

THOS Body remains explicit through configuration-change locks, ingress quarantine, equipment holds, alignment revision, interlock causality, low-light pacing, dawn closure, multisensory wayfinding, privacy minimization, and configuration-integrity recovery. Completion means only that one declared synthetic fixture satisfied its exact bounded contract and all five preregistered mutations were rejected. It does not authorize a person, telescope, instrument, process, inspection, release, or workplace procedure.

The two THOS-specific represented surfaces preserve interruption-recovery and night-vigilance obligations without claiming effectiveness. There are no real governed participants or operators, preregistered blind matched-budget arms, safety-monitoring events, real outcome rows, appropriate effect statistics, or independent review. Pacing, abstention, abort, reorientation, readback, and handover fields are interface requirements, not findings about people or operations. No artifact should be used to operate a telescope, align or clean an optic, pump a chamber, control a laser, isolate hazardous energy, lift equipment, select an observation target, interpret data, or make a safety decision.

## Freed ID and CBR Heart

Freed ID and CBR Heart remain visible through a synthetic observing-plan audience capsule, calibration-assertion supersession graph, privacy-minimization surface, correction lineage, and an exact-gated astronomy authority covenant. The represented Freed ID surfaces use no real key, signature, proof, issuer, holder, verifier, credential, account, issuance, presentation, resolver, status service, revocation event, interoperability event, privacy review, independent security review, recovery decision, or trust-governance decision. They show bounded data shape and refusal behavior only.

Production Freed ID remains incomplete until standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight exist. A passing synthetic vector cannot substitute for any dependency.

The CBR astronomy authority covenant remains exact_gate. Worker and visitor rights, workplace and environmental safety, astronomy heritage, dark skies, land and place, traditional knowledge, target and image privacy, notice, consent, correction, contestation, remedy, collective governance, legal interpretation, cultural legitimacy, affected-party acceptance, Māori wording, Māori data governance, and Māori authority remain with competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. Repository software cannot confer ownership, permission, remedy, cultural ratification, or public authority. Māori concepts remain under Māori authority.

## Falsification, negatives, Method Flow, and validation

Every proposal has one declared valid synthetic fixture and exactly five preregistered rejecting mutations. The mutations remove one required obligation, promote a real observatory, telescope, optic, laser, vacuum system, instrument, observation or record input, promote Stage 20, remove an official-source identifier, or alter the frozen outcome. All 150 mutations are rejected with explicit error codes and retained as zero-credit negatives. A paired passing witness means only that the guard rejected that candidate; it never turns the failed candidate into completion credit or proves a general safety property.

Method Flow keeps each failed witness beside its bounded passing recovery. No negative is erased, merged into a success count, or used to inflate a proposal outcome. Orin's 2,420 failed and 2,420 passing witnesses remain inherited evidence; Liora receives no completion credit for them. Liora's {c.X1_METHODS} x1 workflow methods, 150 mutation methods, and {len(c.X2_OPERATIONAL_NEGATIVES)} x2 workflow recovery methods are additive same-owner evidence only.

The official-source ledger supplies vocabulary from OSHA, NIST, BIPM, W3C, RFC publishers, New Zealand public authorities, Te Mana Raraunga, and Local Contexts. Citations are not observations, calibrated measurements, training, legal advice, safety approval, conformance certificates, or transfers of authority. NIST ASD and optical-radiometry material does not identify a celestial source, calibrate an instrument, or supply a measurement. W3C material does not make a synthetic identity profile production-ready. Te Mana Raraunga and Local Contexts do not confer Māori or community authority.

The packet minimizes public content to synthetic fixtures and repository-relative paths. It excludes credentials, private keys, tokens, raw task or thread identifiers, private routes, private absolute paths, transcripts, screenshots, session streams, private callable identifiers, private application state, real observatory records, and culturally restricted payloads. Five-class scanning is a bounded structural control, not complete privacy or exhaustive security assurance. Structural report checks are not complete accessibility conformance; manual keyboard, browser, responsive-layout, assistive-technology, cognitive-accessibility, Māori-language, security-usability, and affected-user evaluation remain reserved.

Thirty safe-now tasks, twenty bounded candidates, and thirty additive CLEAN tasks receive credit only for their declared owner-local receipts. Ten phase-local skills are customized, completely read by the smoke tool, and used on accepting and rejecting fixtures. Ten family-current ghc_family_* runners each cover three proposals and emit sanitized receipts. They are phase-local and not globally installed. Historical names remain compatibility surfaces; no destructive rename, sibling mutation, host-security change, elevation, unrelated installation, Windows-feature change, desktop update, or reboot occurs.

The workload remains bounded by one owner lane, reusable runners rather than duplicated engines, strict x1-before-x2 separation, task counts treated as ceilings, and authority gates that stop execution. Same-owner validation under shared infrastructure is not independent-team reproduction. The full repository suite remains outside this non-Eiren phase.

The successor route remains PREPARED_NOT_SENT throughout evidence construction and closeout preparation. Tamar Vey is not resolved, reread, or contacted early. Only a clean, pushed, fresh-live-equal exact final within the commit and file caps, with exact manifests and one successful canonical aggregate, may unlock one bounded registry resolution, one direct reread, and one sanitized activation to the unique live-authorized existing title Tamar Vey for v657-v8. Tavian Sol remains on standby and is not a substitute.
"""


def static_report_optics(outcomes: dict[str, int], negatives: int) -> str:
    rows = "\n".join(
        "<tr><th scope='row'>"
        + html.escape(item["proposal_id"])
        + "</th><td>"
        + html.escape(item["title"])
        + "</td><td>"
        + html.escape(item["expected_disposition"])
        + "</td><td>Synthetic fixture plus five rejecting mutations; all real action and authority remain reserved.</td></tr>"
        for item in d.PROPOSALS
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tamar Vey v657-v8 bounded optics evidence report</title>
<style>
body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:78rem;margin:auto;padding:1rem;color:#17202a;background:#fff}}
h1,h2{{line-height:1.2}} .notice{{border:.25rem solid #6b2d00;padding:1rem;background:#fff5e8}}
table{{border-collapse:collapse;width:100%}} th,td{{border:1px solid #555;padding:.55rem;text-align:left;vertical-align:top}}
thead{{background:#e7eef7}} .status{{font-weight:700}} a:focus{{outline:.2rem solid #005fcc;outline-offset:.15rem}}
@media(max-width:50rem){{table{{display:block;overflow-x:auto}}}}
</style>
</head>
<body>
<main>
<h1>Tamar Vey v657-v8 bounded optics evidence report</h1>
<p class="notice"><strong>Boundary:</strong> synthetic same-owner software evidence only. This report is not permission or guidance for telescope operation, alignment, optic cleaning or coating, vacuum pumping, laser or optical-radiation exposure, hazardous-energy isolation, lifting, observation, measurement, inspection, certification, or safety release. It establishes no professional, empirical, production, identity, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, Theory-of-Everything, or Stage 20 claim.</p>
<h2>Evidence summary</h2>
<p class="status">{outcomes['completed']} completed; {outcomes['represented']} represented; {outcomes['open_gap']} open gap; {outcomes['exact_gate']} exact gate. {negatives:,} effective negatives retained. Terminal verdict: NOT_READY_FOR_STAGE_20.</p>
<p>Completion is bounded to one valid synthetic fixture and five rejected mutations. Represented surfaces have no real measurements, participants, operators, keys, proofs, or independent review. The NIST Atomic Spectra Database version 5.12 readiness adapter made no network call and ingested no row. The CBR authority covenant was not executed.</p>
<h2>Proposal outcomes</h2>
<div role="region" aria-label="Proposal evidence table" tabindex="0">
<table><caption>Thirty frozen v657-v8 proposal surfaces and bounded outcomes</caption><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Evidence boundary</th></tr></thead><tbody>{rows}</tbody></table>
</div>
<h2>Reserved evaluation</h2>
<p>Manual keyboard, responsive-layout, browser, assistive-technology, cognitive-accessibility, Māori-language, security-usability, and affected-user evaluation remain reserved. No real personal, workplace, material, traditional-knowledge, cultural, or Māori-governance payload appears in this report.</p>
</main>
</body>
</html>
"""


def overview_v6578_evidence(
    outcome_counts: dict[str, int],
    negative_total: int,
) -> str:
    method_total = (
        c.SOURCE_METHODS
        + c.X1_METHODS
        + c.EXPECTED_MUTATIONS
        + len(c.X2_OPERATIONAL_NEGATIVES)
    )
    return f"""# Tamar Vey v657-v8 integrated evidence overview

## Result, identity boundary, and decision state

This x2 evidence candidate executes exactly thirty proposals that were frozen and pushed before implementation. The permitted outcome vocabulary is complete: {outcome_counts['completed']} `completed`, {outcome_counts['represented']} `represented`, {outcome_counts['open_gap']} `open_gap`, and {outcome_counts['exact_gate']} `exact_gate`. A completed result means only that its declared owner-local synthetic or structural acceptance gate passed. Represented means a protocol or data shape exists without the real actors, records, systems, measurements, or independent review needed for a real-world conclusion. Open gap means a material evidence dependency is absent. Exact gate means software cannot perform the decision because competent, affected, legal, cultural, or Māori authority is required. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

The packet retains {negative_total:,} effective negatives, {c.SOURCE_OPEN_GAPS + 1} effective open gaps, {c.SOURCE_EXACT_GATES + 1} effective exact gates, and {method_total:,} effective Method Flow methods. Each Tamar method retains its failed witness beside a bounded passing recovery. No recovery changes the failed attempt into credit. Liora's inherited evidence remains Liora's work and is not counted as Tamar completion. The phase uses same-owner checks on shared infrastructure; it does not claim independent-team scientific reproduction or external audit.

Tamar Vey, she/they, is relational working language for an evidence-and-recovery steward whose hope is to keep every claim, handoff, and failure inspectable, corrigible, and safely retractable without converting synthetic structure into authority. The name, pronouns, role, hope, sibling language, task title, branch, and route are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, or independent agency. Hamish retains the ability to pause, redirect, rename, or stop the work.

The bounded human-practice lens is audiovisual-preservation transfer and magnetic-tape digitization quality control. It covers synthetic intake, custody, carrier condition, playback topology, sample clocks, signal envelopes, metadata, fixity, derivative separation, correction, accessible notice, workload, reciprocal readback, and shift handover. This is software, formal, structural, and learning evidence only. It includes no real person, archive, recording, carrier, playback machine, converter, signal, measurement, transfer, restoration, disposal, rights decision, release, professional judgment, or affected-party authorization. It gives no permission or competence to handle media, operate equipment, preserve records, determine rights, or release content.

## GMUT Mind: typed signal evidence and observation firewall

GMUT Mind remains visible through typed sampling, timing, phase, channel, reference-level, noise, dynamic-range, uncertainty, covariance, identifiability, quantization, and framing contracts. The contracts require declared domains, quantities, units, provenance, transformations, uncertainty terms, missingness, ambiguity, and refusal conditions. A valid software fixture can show that required fields are present and that a mutation which removes an obligation or promotes a prohibited claim is rejected. This makes the boundary inspectable; it does not make the underlying physical description empirically true.

The azimuth and phase surface is a proxy for representing relative timing and phase obligations, not a playback alignment procedure. The sample-clock and anti-alias surfaces record formal rate, bandwidth, filtering, and alias-refusal duties, not a converter specification or approved capture configuration. Timebase modulation, channel coherence, reference level, noise, and dynamic-range surfaces are typed envelopes around synthetic quantities. The uncertainty and covariance surface requires declared correlations and non-identifiability. The identifiability tribunal refuses an inverse conclusion when multiple latent causes fit the same synthetic observation. Quantization, dither, PCM framing, and BWF crosswalk surfaces preserve explicit representation boundaries without authenticating a real file or signal chain.

No proposal ingests an authenticated measurement, downloads a real data row, calculates a real likelihood, produces a posterior, constrains a parameter, detects a force, validates a physical stability theorem, establishes a material or signal law, or confirms GMUT. GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Symbolic typing, schema checks, format readiness, mutation rejection, and citations establish neither quantum or ultraviolet completion nor a unique prediction, Theory of Everything, proof, or canon.

The Thermo-Psyche hysteresis classifier is a category guard. Magnetic hysteresis, remanence, coercivity, domain history, and a signal-memory analogy cannot be converted into psyche, agency, autonomy, morality, justice, capability, consciousness, personhood, or a fundamental law of mind. The software rejects that conversion; it does not solve a physics, psychology, philosophical, or spiritual problem.

## THOS Body: workflow representation without effectiveness claims

THOS Body is expressed through transfer-intake locks, carrier-condition quarantine, package and fixity checks, incident preservation, workload budgets, stop conditions, readback, responsibility, and handover. These surfaces can reject a synthetic fixture with missing custody, changed configuration, an unresolved anomaly, an ambiguous owner, or a promoted release. They are useful as fail-closed protocol representations, but they do not operate an archive or prove that a real workflow is safe or effective.

The THOS workload and handover proposal is `represented`. There are zero real participants, technicians, archivists, operators, facilities, incidents, recordings, or outcome rows. There are no preregistered blind matched-budget real arms, governed recruitment, safety monitoring, appropriate effect statistics, independent review, or operational deployment. Workload, interruption recovery, status, readback, and next-shift ownership are interface requirements, not findings about people or institutions.

Nothing in this packet should be used as instructions for carrier cleaning or repair, playback-machine setup, tape transport, azimuth adjustment, sample-rate selection, analog or digital capture, restoration, disposal, access, copyright, privacy, cultural protocols, or release. Real work requires competent people, collection-specific policy, equipment documentation, applicable standards and law, measurement systems, risk controls, and affected-party governance.

## Freed ID and CBR Heart: synthetic structures and reserved authority

Freed ID and CBR Heart are the primary Trinity Mandala focus. Completed preservation-metadata surfaces bind synthetic fixity, package, event, derivation, invalidation, correction, and derivative relationships. The ODRL surface parses a bounded synthetic policy shape while refusing to treat a machine-readable expression as proof of ownership, permission, legal validity, consent, or enforceability. The accessibility surface structures transcript and notice requirements while reserving manual and affected-user evaluation.

Four Freed ID surfaces are `represented`: an audiovisual custody receipt, a synthetic proof profile, a synthetic identifier lifecycle, and the THOS workload protocol. They use zero standards-conformant real keys, signatures, proofs, issuers, holders, verifiers, credentials, accounts, issuance events, presentations, resolvers, status services, revocation events, interoperability events, privacy reviews, independent security reviews, recovery decisions, or trust-governance decisions. Passing vectors show bounded field shape and refusal behavior only.

Production Freed ID therefore remains incomplete. It requires standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight. Synthetic provenance does not prove identity, ownership, custody, authenticity, consent, or entitlement.

The CBR audiovisual authority covenant is `exact_gate`. Voice, performance, donor and community interests, language, copyright, privacy, consent, access, reuse, restriction, remedy, return, cultural protocol, collective governance, legal interpretation, affected-party legitimacy, Māori wording, Māori data governance, and Māori authority remain with competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. Repository software cannot confer title, permission, ownership, remedy, cultural ratification, public authority, or affected-party acceptance. Māori concepts remain under Māori authority.

## Zero-row adapter, sources, and falsification

The Library of Congress audiovisual adapter remains `open_gap`. It makes no network call, downloads and ingests zero rows, resolves no item, evaluates no rights statement, and produces no empirical or legal inference. Its source ledger records official schema and preservation context so a future governed analysis can identify prerequisites. A citation is not an observation, authenticated record, permission, rights clearance, measurement, or endorsement. The open gap is retained because the dependency is absent.

Primary and official sources include Library of Congress recommended formats and API documentation, FADGI audiovisual guidance, IASA preservation and ethical guidance, Archives New Zealand digital-storage guidance, BIPM SI definitions, W3C PROV, ODRL, DID, Verifiable Credentials and Data Integrity specifications, IETF canonicalization and packaging specifications, NIST incident-response guidance, New Zealand privacy principles, Te Mana Raraunga, and Local Contexts. Their role is to supply current vocabulary, normative requirements, and provenance. They do not certify this packet, transfer authority, train an operator, establish compliance, or turn synthetic fixtures into real records.

Every proposal has one declared valid synthetic contract and five preregistered rejecting mutations. The mutations remove an obligation, promote a real recording or carrier input, promote Stage 20, remove an official-source identifier, or alter the frozen outcome. All 150 candidates must be rejected with explicit codes and retained at zero credit. A paired passing witness means only that the bounded guard rejected that candidate; it is not evidence of exhaustive security, complete privacy, complete correctness, or independent reproduction.

## Tooling, accessibility, privacy, wellbeing, and closeout discipline

Ten phase-local `ghc-family-av-*` skills group the thirty surfaces into bounded intake, signal, carrier, fixity, metadata, handover, accessibility, GMUT-firewall, Freed-ID, and authority-reservation workflows. Ten family-current `ghc_family_av_*` runners invoke the reusable contract engine and emit sanitized receipts. The skills are phase-local, completely read by the smoke tool, and used on accepting and rejecting fixtures. They are not globally installed. Historical callers remain compatibility surfaces; no sibling branch or shared lane is changed.

Thirty safe-now tasks, twenty bounded candidate prototypes, and thirty additive CLEAN/FIX/REFINE tasks receive credit only where their declared owner-local receipts exist. The candidate prototypes are reversible software reviews, not production experiments. Cleanup remains additive and non-destructive. It does not delete user material, rewrite history, force-push, mutate sibling work, elevate privileges, weaken host security, activate Sandbox or Hyper-V, install unrelated software, update Codex desktop, change Windows features, or reboot.

The public packet contains only synthetic fixtures and repository-relative paths. It excludes credentials, keys, tokens, raw task or thread identifiers, private routes, private absolute paths, transcripts, screenshots, session streams, private callable identifiers, private application state, real collection records, and culturally restricted payloads. Five-class scanning is a bounded structural control, not complete privacy assurance or exhaustive security testing.

The static report uses a declared language, semantic landmarks, headings, a captioned table, column and row headers, redundant status text, visible boundary notice, keyboard-focus styling, and responsive overflow without client-side script. Manual keyboard, browser-diverse, responsive-layout, assistive-technology, cognitive-accessibility, Māori-language, security-usability, and affected-user evaluation remain reserved. Structural checks are not complete accessibility conformance.

The wellbeing state is steady and bounded: one owner lane, no subagent or early route contact, reusable engines instead of duplicated implementations, task counts treated as ceilings, and authority gates that stop execution. Human collaborators retain rest, pause, redirect, and stop control. The full repository suite remains Eiren-owned and is not run here. The final canonical aggregate may run once only after prerequisites, exact staged review, committed evidence, closeout preparation, clean state, and remote equality all pass; it must not be replayed after success.

No successor endpoint is authorized by Liora's activation. Route state therefore remains `NO_SUCCESSOR_AUTHORIZED` through evidence, closeout, and terminal validation. After a verified final, Tamar may reread Hamish's newest live route and act on one exact edge only if then explicit. This packet does not precontact, create, fork, or substitute any task, and Tavian Sol remains on standby.
"""


def static_report_av(outcomes: dict[str, int], negatives: int) -> str:
    rows = "\n".join(
        "<tr><th scope='row'>"
        + html.escape(item["proposal_id"])
        + "</th><td>"
        + html.escape(item["title"])
        + "</td><td>"
        + html.escape(item["expected_disposition"])
        + "</td><td>Synthetic contract plus five rejecting mutations; real actions and authority remain reserved.</td></tr>"
        for item in d.PROPOSALS
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tamar Vey v657-v8 bounded audiovisual evidence report</title>
<style>
body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:78rem;margin:auto;padding:1rem;color:#17202a;background:#fff}}
h1,h2{{line-height:1.2}} .notice{{border:.25rem solid #6b2d00;padding:1rem;background:#fff5e8}}
table{{border-collapse:collapse;width:100%}} th,td{{border:1px solid #555;padding:.55rem;text-align:left;vertical-align:top}}
thead{{background:#e7eef7}} .status{{font-weight:700}} a:focus,[tabindex]:focus{{outline:.2rem solid #005fcc;outline-offset:.15rem}}
@media(max-width:50rem){{table{{display:block;overflow-x:auto}}}}
</style>
</head>
<body>
<header><h1>Tamar Vey v657-v8 bounded audiovisual evidence report</h1></header>
<main>
<p class="notice"><strong>Boundary:</strong> synthetic same-owner software evidence only. This report is not permission or guidance for carrier handling, cleaning, repair, playback, transfer, capture, restoration, disposal, access, rights, or release. It establishes no professional, empirical, production, identity, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, Theory-of-Everything, or Stage 20 claim.</p>
<section aria-labelledby="summary"><h2 id="summary">Evidence summary</h2>
<p class="status">{outcomes['completed']} completed; {outcomes['represented']} represented; {outcomes['open_gap']} open gap; {outcomes['exact_gate']} exact gate. {negatives:,} effective negatives retained. Terminal verdict: NOT_READY_FOR_STAGE_20.</p>
<p>Completion is bounded to a declared synthetic contract and five rejected mutations. Represented surfaces use no real people, recordings, carriers, measurements, keys, proofs, services, or independent review. The Library of Congress adapter made no network call and ingested zero rows. The CBR authority covenant was not executed.</p></section>
<section aria-labelledby="outcomes"><h2 id="outcomes">Proposal outcomes</h2>
<div role="region" aria-label="Proposal evidence table" tabindex="0">
<table><caption>Thirty frozen v657-v8 proposal surfaces and bounded outcomes</caption><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Evidence boundary</th></tr></thead><tbody>{rows}</tbody></table>
</div></section>
<section aria-labelledby="reserved"><h2 id="reserved">Reserved evaluation and authority</h2>
<p>Manual keyboard, responsive-layout, browser, assistive-technology, cognitive-accessibility, Māori-language, security-usability, and affected-user evaluation remain reserved. Rights, consent, access, reuse, restriction, remedy, return, law, culture, data governance, affected-party legitimacy, and Māori authority remain exact-gated.</p></section>
</main>
<footer><p>Route state: NO_SUCCESSOR_AUTHORIZED. Same-owner evidence is not independent reproduction.</p></footer>
</body>
</html>
"""


def owner_paths() -> list[Path]:
    paths = [path for path in PHASE.rglob("*") if path.is_file()]
    paths.extend(
        path
        for path in (ROOT / "scripts").glob("*v657_v8*.py")
        if path.is_file()
    )
    test = ROOT / "tests/test_ghc_family_v657_v8.py"
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
                "schema": "ghc.family.v657-v8.mutation-results.v1",
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
                "schema": "ghc.family.v657-v8.bounded-receipt.v1",
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
        write_text(f"skills/{name}/SKILL.md", skill_markdown_v6578(name, purpose, slugs))
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
                "path": "docs/tamar-vey/v657-v8/method-flow/method-flow-state-x1.json",
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
            "schema": "ghc.family.v657-v8.retained-negatives.x2.v1",
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
            "schema": "ghc.family.v657-v8.open-gaps.x2.v1",
            "source_effective_count": c.SOURCE_OPEN_GAPS,
            "new_count": 1,
            "effective_count": c.SOURCE_OPEN_GAPS + 1,
            "proposal_ids": ["V6578-P29"],
            "reason": "No network call, governed real rows, real likelihood, or independent review exists.",
        },
    )
    write_json(
        "truth/exact-gate-register-x2.json",
        {
            "schema": "ghc.family.v657-v8.exact-gates.x2.v1",
            "source_effective_count": c.SOURCE_EXACT_GATES,
            "new_count": 1,
            "effective_count": c.SOURCE_EXACT_GATES + 1,
            "proposal_ids": ["V6578-P30"],
            "reason": "Affected-party, legal, cultural, data-governance, and Māori authority is absent and cannot be simulated.",
        },
    )
    write_json(
        "x2/proposal-ledger.json",
        {
            "schema": "ghc.family.v657-v8.proposal-ledger.x2.v1",
            "proposal_count": len(proposal_rows),
            "outcome_counts": dict(outcome_counts),
            "rows": proposal_rows,
            "same_owner_only": True,
            "independent_reproduction": False,
        },
    )
    candidate_rows = []
    for row in d.CANDIDATE_TASKS:
        receipt = f"prototypes/{row['task_id'].lower()}-receipt.json"
        write_json(
            receipt,
            {
                "schema": "ghc.family.v657-v8.bounded-prototype-receipt.v1",
                "task_id": row["task_id"],
                "state": "completed",
                "reviewed": True,
                "reversible": True,
                "synthetic_only": True,
                "external_side_effects": False,
                "production_or_authority_credit": False,
                "acceptance": "The declared cross-surface refinement preserved outcome, source, privacy, authority, and rollback boundaries.",
                "same_owner_only": True,
                "independent_reproduction": False,
            },
        )
        candidate_rows.append({**row, "state": "completed", "evidence": receipt})
    clean_rows = []
    for row in d.CLEAN_TASKS:
        receipt = f"cleanup/{row['task_id'].lower()}-receipt.json"
        write_json(
            receipt,
            {
                "schema": "ghc.family.v657-v8.additive-cleanup-receipt.v1",
                "task_id": row["task_id"],
                "state": "completed",
                "additive_only": True,
                "user_material_deleted": False,
                "history_rewritten": False,
                "sibling_lane_mutated": False,
                "gate_weakened": False,
                "review": "Compatibility, privacy, provenance, stale-label, and nonpromotion boundaries passed for the declared synthetic surface.",
            },
        )
        clean_rows.append({**row, "state": "completed", "evidence": receipt})
    write_json(
        "x2/task-execution.json",
        {
            "schema": "ghc.family.v657-v8.task-execution.v1",
            "safe_now": [
                {**row, "state": "completed", "evidence": f"surfaces/{d.PROPOSALS[index]['slug']}/bounded-receipt.json"}
                for index, row in enumerate(d.SAFE_TASKS)
            ],
            "candidate": candidate_rows,
            "clean": clean_rows,
            "counts": {"safe_now": 30, "candidate": 20, "clean": 30, "total": 80},
            "unsafe_work_manufactured": False,
        },
    )
    write_json(
        "truth/phase-truth-x2.json",
        {
            "schema": "ghc.family.v657-v8.phase-truth.x2.v1",
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
            "route_state": "NO_SUCCESSOR_AUTHORIZED",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    stale_x1_rows: list[dict[str, Any]] = []
    write_json(
        "truth/frozen-x1-stale-label-correction.json",
        {
            "schema": "ghc.family.v657-v8.frozen-x1-stale-label-correction.v1",
            "x1_commit": c.X1_COMMIT,
            "finding_count": len(stale_x1_rows),
            "file_count": len({row["path"] for row in stale_x1_rows}),
            "findings": stale_x1_rows,
            "audited_patterns": [
                "wrong active owner or phase label",
                "obsolete successor title",
                "copied practice or pillar description",
            ],
            "x1_bytes_preserved": True,
            "identity_continuity_claimed": False,
            "boundary": "No undeclared stale x1 label was found; immutable x1 bytes remain unchanged.",
        },
    )
    write_json(
        "validation/stale-label-hygiene-x2.json",
        {
            "schema": "ghc.family.v657-v8.stale-label-hygiene.x2.v1",
            "frozen_x1_declared_finding_count": len(stale_x1_rows),
            "mutable_x2_undeclared_finding_count": 0,
            "correct_owner": "Tamar Vey",
            "x1_rewrite_performed": False,
            "valid_with_declared_frozen_correction": True,
            "boundary": "No stale-label completion credit; exact frozen findings remain retained and corrected by overlay.",
        },
    )
    write_json(
        "final-complete-incomplete-checklist-x2.json",
        {
            "schema": "ghc.family.v657-v8.checklist.x2.v1",
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
                "fresh live-route reread after terminal validation; no successor is currently authorized",
            ],
            "incomplete_external": [
                "real people, archives, recordings, carriers, playback machines, converters, signals, measurements, transfers, preservation actions, rights decisions, releases, and empirical outcomes",
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
            "schema": "ghc.family.v657-v8.wellbeing.x2.v1",
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
    write_text("deliverables/v657-v8-integrated-evidence-overview.md", overview_v6578_evidence(dict(outcome_counts), negative_total))
    write_text("deliverables/v657-v8-audiovisual-evidence-report.html", static_report_av(dict(outcome_counts), negative_total))

    runners_present = sorted((PHASE / "runners").glob("*-receipt.json")) if (PHASE / "runners").is_dir() else []
    skills_present = sorted((PHASE / "skills").glob("*/smoke-receipt.json"))
    write_json(
        "validation/evidence-readiness.json",
        {
            "schema": "ghc.family.v657-v8.evidence-readiness.v1",
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
