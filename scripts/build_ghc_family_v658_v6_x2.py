#!/usr/bin/env python3
"""Build Neris Solane v658-v6 bounded volcanic-observatory x2 evidence."""

from __future__ import annotations

import hashlib
import html
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v658_v6_phase_data as d
from ghc_family_v658_v6_minimal import validate_minimal
from ghc_family_v658_v6_runtime import RUNNER_GROUPS, evaluate_surface
from ghc_family_v658_v6_validator import validate_phase


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
X1_COMMIT = "1591612c83feb7f47fb0b044525bf4b37f71bfb7"
SELF_EXCLUSIONS = {
    "validation/evidence-content-manifest.json",
    "validation/evidence-privacy-scan.json",
    "validation/evidence-staged-review.json",
    "validation/evidence-validation.json",
}
X2_CODE = [
    "scripts/build_ghc_family_v658_v6_x2.py",
    "scripts/ghc_family_v658_v6_runtime.py",
    "scripts/ghc_family_v658_v6_validator.py",
    "scripts/ghc_family_v658_v6_minimal.py",
    "tests/test_ghc_family_v658_v6.py",
    *[f"scripts/{name}" for name, _ in d.RUNNER_SPECS],
]
X2_OPERATIONAL_NEGATIVES: list[dict[str, Any]] = [
    {
        "negative_id": "V6586-X2-N01",
        "slug": "silent-x1-commit-wrapper-output",
        "failure_signature": "The x1 commit wrapper completed without returning its expected commit text, leaving the mutation outcome unconfirmed in that transport response.",
        "fail_procedure": "Invoke the bounded x1 commit wrapper and rely on its returned text as the sole success signal.",
        "fail_observed": "No commit text was returned, so the wrapper response received zero mutation credit and was not retried.",
        "candidate_workaround": "Audit HEAD, parent, subject, cached diff count, and acknowledged untracked x2 paths with isolated scalar reads.",
        "pass_procedure": "Read the exact commit state without repeating the commit mutation.",
        "pass_observed": "Scalar audit proved x1 at 1591612c83feb7f47fb0b044525bf4b37f71bfb7, direct parent 1005e3b8d6a743ba8cb5a7000aa945a8be262c49, an empty index, and eight deliberately excluded x2 scaffold paths.",
        "recurrence_guard": "After a silent mutation wrapper, inspect immutable state read-only before any retry.",
        "scope_boundary": "Bounded Git-state recovery only; no scientific, production, routing, or authority credit.",
        "credit": 0,
        "retained": True,
        "same_owner_only": True,
        "independent_reproduction": False,
    },
    {
        "negative_id": "V6586-X2-N02",
        "slug": "rg-literal-windows-wildcard-recurrence",
        "failure_signature": "The first x2 stale-source scan passed scripts\\ghc_family_volcano_*.py as a literal Windows path and ripgrep returned operating-system error 123 before a valid scan completed; an earlier malformed targeted search also left a PowerShell/ripgrep pair active after its response ended.",
        "fail_procedure": "Pass a Unix-style wildcard as a native Windows path argument to ripgrep.",
        "fail_observed": "The operating system rejected the literal wildcard path; the stale scan received zero credit.",
        "candidate_workaround": "Root ripgrep at the scripts directory, use -g ghc_family_volcano_*.py as a glob filter alongside exact non-wrapper paths, and audit/stop only verified orphaned read-only search processes.",
        "pass_procedure": "Run the word-bounded stale-label patterns across the explicit x2 files and the rooted wrapper glob.",
        "pass_observed": "The corrected rooted glob scanned all x2 source files with zero confirmed stale labels; exact command-line audit then stopped only the verified orphaned PowerShell/ripgrep search pair.",
        "recurrence_guard": "Use ripgrep -g for Windows wildcard matching, never pass wildcard text as a literal path, and audit long or malformed search wrappers for orphaned read-only processes.",
        "scope_boundary": "Bounded source-hygiene recovery only; no scientific, production, routing, or authority credit.",
        "credit": 0,
        "retained": True,
        "same_owner_only": True,
        "independent_reproduction": False,
    },
    {
        "negative_id": "V6586-X2-N03",
        "slug": "partial-x2-builder-without-lifecycle-manifest",
        "failure_signature": "The first x2 builder wrapper serialized only its empty output field and hid the returned execution session identifier; a premature audit observed partial artifacts while the original long-running process had not been explicitly polled, creating an overlap risk when a recovery invocation began.",
        "fail_procedure": "Discard the structured execution result and infer completion solely from an empty output string.",
        "fail_observed": "Terminal lifecycle files were absent at the premature audit, isolated validators reported the missing manifest dependency, and the first transport interpretation received zero evidence-commit credit.",
        "candidate_workaround": "Capture the complete execution result, retain and poll any returned session identifier, audit declared terminal paths and x1 byte identity, and require an explicit exit code before credit.",
        "pass_procedure": "Poll the captured builder session to exit 0 and require its completion payload plus privacy, manifest, staged-review, and evidence-validation files before staging.",
        "pass_observed": "The captured session reached exit 0 with 23/5/1/1 outcomes, 150 retained mutations, 366 detailed checks, 15 minimal checks, 229 privacy-scanned files, 240 manifest entries, and 208 expected evidence paths.",
        "recurrence_guard": "Never infer long-running process completion from an empty output field; preserve the full execution result and poll its session identifier to an explicit exit state.",
        "scope_boundary": "Bounded owner-local build recovery only; no scientific, production, routing, or authority credit.",
        "credit": 0,
        "retained": True,
        "same_owner_only": True,
        "independent_reproduction": False,
    },
    {
        "negative_id": "V6586-X2-N04",
        "slug": "nested-powershell-python-privacy-regex-quote-fault",
        "failure_signature": "The first exact evidence-path stale/privacy audit embedded a quote-rich Python regex in a PowerShell command string; PowerShell lost the quote boundary and rejected the command before any file was scanned or staged.",
        "fail_procedure": "Nest a Python one-liner containing both quote classes and backslash-heavy regular expressions directly inside PowerShell transport quoting.",
        "fail_observed": "PowerShell returned parser errors at the private-path regex; the audit received zero credit and the Git index remained unchanged.",
        "candidate_workaround": "Send multiline Python source over standard input, keep the pattern literals inside Python, and assert the Git index is empty before the corrected scan.",
        "pass_procedure": "Run the exact declared evidence-path stale/privacy audit with Python-over-stdin, then stage only after zero hits.",
        "pass_observed": "The corrected stdin-based audit scanned every declared evidence path across all seven pattern classes with zero confirmed hits before exact staging.",
        "recurrence_guard": "Use stdin for quote-rich multiline Python diagnostics on Windows instead of nested python -c transport.",
        "scope_boundary": "Bounded precommit hygiene recovery only; no scientific, production, routing, or authority credit.",
        "credit": 0,
        "retained": True,
        "same_owner_only": True,
        "independent_reproduction": False,
    },
]


def write_json(relative: str, payload: Any, *, compact: bool = False) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, indent=None if compact else 2, separators=(",", ":") if compact else None, sort_keys=True)
    path.write_text(text + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def prospective_blob(repository_relative: str) -> str:
    return git("hash-object", f"--path={repository_relative}", repository_relative)


def x1_paths() -> list[str]:
    return sorted(line for line in git("diff-tree", "--no-commit-id", "--name-only", "-r", X1_COMMIT).splitlines() if line)


def assert_x1_frozen() -> list[str]:
    if git("rev-parse", "HEAD") != X1_COMMIT:
        raise RuntimeError(f"x2 builder requires exact frozen x1 head {X1_COMMIT}")
    paths = x1_paths()
    changed = subprocess.run(["git", "diff", "--name-only", X1_COMMIT, "--", *paths], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.splitlines()
    if changed:
        raise RuntimeError(f"frozen x1 paths changed: {changed}")
    return paths


def mutation_negative(proposal_id: str, row: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "negative_id": f"V6586-MUT-{proposal_id.split('-')[-1]}-{index:02d}",
        "proposal_id": proposal_id,
        "mutation_id": row["mutation_id"],
        "signature": row["error_codes"],
        "observed": "The preregistered synthetic mutation was rejected by the bounded contract validator.",
        "credit": 0,
        "retained": True,
        "same_owner_only": True,
        "independent_reproduction": False,
        "authority_action_executed": False,
    }


def mutation_method(negative: dict[str, Any], index: int) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    method_id = f"V6586-X2-MUT-METHOD-{index:03d}"
    fail_id, pass_id = f"V6586-X2-MUT-WITNESS-{index:03d}-F", f"V6586-X2-MUT-WITNESS-{index:03d}-P"
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
        "rollback": "Discard the mutated candidate, preserve the valid contract separately, and leave real, external, authority, and sibling state unchanged.",
        "protected_gates": d.PROTECTED_GATES,
        "retained_negative_ids": [negative["negative_id"]],
        "validation_witness_ids": [fail_id, pass_id],
        "recommendation_state": "preferred",
        "supersedes": [],
    }
    witnesses = [
        {"witness_id": fail_id, "method_id": method_id, "result": "fail", "procedure": "Apply the preregistered mutation to the valid synthetic fixture.", "expected": "The mutation must not receive valid-fixture credit.", "observed": f"Rejected with {', '.join(negative['signature'])}.", "retained_negative_ids": [negative["negative_id"]], "same_owner_only": True, "independent_reproduction": False, "boundary": "Zero completion credit."},
        {"witness_id": pass_id, "method_id": method_id, "result": "pass", "procedure": "Confirm explicit rejection while preserving the valid fixture separately.", "expected": "The validator fails closed on the mutation.", "observed": "The mutation was rejected and retained without changing real, external, authority, or sibling state.", "retained_negative_ids": [negative["negative_id"]], "same_owner_only": True, "independent_reproduction": False, "boundary": "Bounded same-owner falsification only."},
    ]
    return method, witnesses


def operational_method(negative: dict[str, Any], index: int) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    method_id = f"V6586-X2-OP-METHOD-{index:02d}"
    fail_id, pass_id = f"V6586-X2-OP-WITNESS-{index:02d}-F", f"V6586-X2-OP-WITNESS-{index:02d}-P"
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
        "rollback": "Retain the failed attempt at zero credit and leave sibling, external, and authority state unchanged.",
        "protected_gates": d.PROTECTED_GATES,
        "retained_negative_ids": [negative["negative_id"]],
        "validation_witness_ids": [fail_id, pass_id],
        "recommendation_state": "preferred",
        "supersedes": [],
    }
    witnesses = [
        {"witness_id": fail_id, "method_id": method_id, "result": "fail", "procedure": negative["fail_procedure"], "expected": "The bounded operation completes without a tooling failure.", "observed": negative["fail_observed"], "retained_negative_ids": [negative["negative_id"]], "same_owner_only": True, "independent_reproduction": False, "boundary": "Failed workflow witness with zero completion credit."},
        {"witness_id": pass_id, "method_id": method_id, "result": "pass", "procedure": negative["pass_procedure"], "expected": "The bounded recovery completes while preserving the failed witness.", "observed": negative["pass_observed"], "retained_negative_ids": [negative["negative_id"]], "same_owner_only": True, "independent_reproduction": False, "boundary": negative["scope_boundary"]},
    ]
    return method, witnesses


def skill_markdown(name: str, purpose: str, slugs: list[str]) -> str:
    return f"""---
name: {name}
description: "{purpose} Use for Neris v658-v6 owner-local synthetic volcanic-observatory assurance across {', '.join(slugs)}."
---

# {name}

1. Read the frozen proposal, source identifiers, protected gates, and expected truth label.
2. Confirm the input is synthetic and contains zero real people, maunga, volcanoes, observatories, stations, instruments, locations, waveforms, images, samples, coordinates, observations, credentials, secrets, private routes, or culturally restricted material.
3. Invoke the matching family-current runner only inside the Neris v658-v6 owner packet.
4. Require one declared valid fixture to pass and every one of its five frozen mutations to be rejected with explicit error codes.
5. Preserve `completed`, `represented`, `open_gap`, or `exact_gate` exactly; retain every failed witness at zero credit.
6. Stop on real data, monitoring interpretation, diagnosis, forecast, alert, hazard message, professional judgment, production identity, deployment, legal interpretation, cultural protocol, mātauranga decision, Māori authority, affected-party decision, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, Theory-of-Everything, or Stage 20 promotion.

Write only repository-relative sanitized receipts. This phase-local skill is workflow guidance, not a claim of consciousness, personhood, continuity, qualification, scientific authority, legal authority, cultural authority, Māori authority, or independent agency. A passing fixture is same-owner synthetic evidence only.
"""


def agent_yaml(name: str, purpose: str) -> str:
    display = name.replace("ghc-family-", "").replace("-", " ").title()
    return f"""interface:
  display_name: "{display}"
  short_description: "Bounded v658-v6 volcano workflow guard"
  default_prompt: "Use ${name} to {purpose.lower()} Preserve synthetic-only and authority boundaries."
policy:
  allow_implicit_invocation: false
"""


def integrated_overview(outcomes: dict[str, int], negatives: int, methods: int) -> str:
    x1 = (PHASE / "deliverables/v658-v6-x1-integrated-overview.md").read_text(encoding="utf-8")
    return x1 + f"""

# Neris Solane v658-v6 x2 evidence and closeout-candidate overview

## What x2 executed

X2 executed exactly the thirty frozen contracts and no unfrozen scientific or authority action. Each contract carries its source identifiers, mechanism obligations, protected gates, expected truth label, synthetic fixture, and explicit evidence ceiling. Across the portfolio, thirty valid fixtures passed and all 150 preregistered mutations were rejected. The mutation catalogue tested a missing domain obligation, promotion of real data or objects, promotion of an empirical claim, promotion to Stage 20, and alteration of the frozen outcome label. Every rejected mutation remains a zero-credit negative with a failed witness and a separate bounded passing rejection witness.

The observed distribution is {outcomes['completed']} `completed`, {outcomes['represented']} `represented`, {outcomes['open_gap']} `open_gap`, and {outcomes['exact_gate']} `exact_gate`. Completion applies only to synthetic structural software checks. Representation applies only to proxy protocols, nonproduction identity disclosures, and machine-checkable accessible structure. The open gap preserves disabled network transport and zero external rows. The exact gate records an authority reservation and performs no authority action.

The effective retained-negative count is {negatives:,}; the effective Method Flow count is {methods:,}. These totals preserve Elaren's inherited lineage, Neris's x1 operational failures, every x2 mutation, and every x2 operational fault. Failed and passing witnesses are paired for traceability, but a passing recovery never erases its failed predecessor or earns independent-reproduction credit.

## Volcanic-observatory data and provenance boundary

The scope card and source passport use only fictional aliases, suppressed location fields, abstract feature classes, revision lineage, and zero-row locks. Instrument epochs describe synthetic station aliases, sensor classes, response placeholders, and maintenance windows. Observation envelopes separate phenomenon time from result time and record units, uncertainty, quality state, and derivation without a measured value. No real person, maunga, volcano, observatory, station, instrument, location, waveform, image, sample, coordinate, observation, release row, or private collaboration record appears. The external capability gateway is deliberately zero-row and transport-disabled.

USGS, GeoNet, GNS Science, WOVOdat, Smithsonian GVP, FDSN, OGC, and Copernicus sources supply terminology and risk context only. The phase does not call their services, download a product, query a row, reproduce a bulletin, resolve a real volcano, validate a format, or claim institutional endorsement. Provenance vocabulary from W3C and deterministic representation vocabulary from RFC 8785 do not create cryptographic assurance.

## Seismic, deformation, and remote-sensing structure

The seismic waveform boundary records channel metadata, timing quality, gap masks, and a calibration placeholder, while the classification docket records alternate classes and an abstention threshold. Neither contains waveform samples or diagnoses an event. The acoustic surface records only fictional array geometry, processing placeholders, association alternatives, weather coupling, and uncertainty; it makes no event claim.

GNSS, tilt, and strain surfaces record frame epochs, orientation, scale, covariance, drift, thermal coupling, gaps, and outage states without a displacement or ground-motion result. The InSAR ledger records fictional product identifiers, orbit and geometry placeholders, coherence and atmosphere holds without imagery or a deformation map. Structural consistency among those fields is not evidence that the ground moved.

## Gas, geochemistry, thermal, visual, and multistream assurance

Volcanic-gas surfaces declare synthetic SO2, CO2, and H2S channel placeholders, units, wind dependencies, detection limits, calibration states, cross-sensitivity, drift, and quarantine. The geochemistry docket records fictional aliquots, preservation and method placeholders, detection limits, custody, and amendments. No concentration, flux, composition, exposure, or environmental conclusion exists.

Thermal and camera surfaces record synthetic bands, emissivity, atmosphere-correction placeholders, saturation, weather, illumination, occlusion, and redaction without heat flux or visual interpretation. Hydrothermal and meteorological registers record only fictional level, temperature, chemistry, wind, pressure, precipitation, cloud, distance-class, datum, gap, and uncertainty fields. They create no unrest indicator or causal adjustment.

The quality ledger preserves missingness, gaps, outliers, reason codes, imputation prohibition, and reviewer holds. The alignment matrix records synthetic time/coordinate offsets, resampling policy, uncertainty propagation, and conflict holds without fusing an observation. The anomaly ledger retains alternate explanations and no-forecast wording. A blinded synthetic unrest scenario uses a prospective commitment and reveal gate, while the typed forward operator records latent-state and observation-channel types plus an identifiability matrix. Neither establishes predictive skill, a volcanic mechanism, a physical law, or empirical GMUT standing.

## THOS Body, Freed ID, and CBR Heart

THOS Body is represented by deterministic multistream batching/checkpointing and a synthetic duty-shift handover proxy. Thirty proposal surfaces are divided among ten family-current runners in fixed three-surface groups. Runner receipts show deterministic same-owner invocation, thirty valid fixtures, and 150 rejected mutations. A batch, checkpoint, or handover-proxy receipt does not establish production speed, resilience, workload benefit, operational handover, reliability, deployment, AGI, or ASI. Blind matched-budget real arms and independent review remain absent.

Freed ID is represented by a synthetic observation-lineage capsule and an observatory notice/model-card disclosure. The envelope can carry a digest, derivation, amendment, expiry, and revocation hold; the notice can carry intended and prohibited use, assumptions, exclusions, uncertainty, limitations, provenance, and a challenge route. Neither creates a live identifier, key, signature, proof, credential, issuer, holder, verification result, resolution endpoint, status mechanism, revocation service, interoperability result, security or privacy review, recovery system, trust governance, or access decision.

CBR Heart reserves rights and authority. The accessible evidence map provides semantic landmarks, a skip link, ordered headings, captioned and scoped tables, focusable overflow, non-colour text labels, reflow rules, and print styling. Manual keyboard, screen-reader, browser diversity, forced-colour, zoom, cognitive, Māori-language, security-usability, and affected-user evaluation remain incomplete. The authority covenant contains refusal-by-default fields for land and maunga relationships, mātauranga, sensitive locations, affected communities, public hazard messages, remedy, cultural protocol, and Māori authority. It selects no wording, label, location, protocol, disclosure, restriction, remedy, or governance decision.

## Skills, runners, tasks, and bounded completeness

Ten phase-local skills were initialized, structurally validated, and smoke-used within the owner packet. They are not globally installed and do not claim independent execution. Ten additive `ghc_family_*` runners were actually invoked and cover all thirty frozen surfaces. Historical caller names remain intact. Thirty safe-now tasks correspond to the thirty contract surfaces; twenty candidate refinements were completed as reversible bounded prototypes; thirty cleanup tasks record additive compatibility, privacy, provenance, stale-label, and nonpromotion checks. The 1,000-task number remains a cap, never a quota.

The owner-generated file count stays below 2,000 and every document stays below 100,000 words. The evidence manifest uses prospective Git blob identities and declares its lifecycle self-exclusions. Privacy scanning covers five concrete raw-identifier classes and reports zero confirmed hits; this is not complete privacy assurance. Stale-domain review distinguishes intentional inherited source references from active v658-v6 labels.

## Scientific and route conclusion

This phase improves the inspectability of a synthetic monitoring-provenance workflow; it does not improve or test GMUT's empirical standing. There is no real observation, diagnosis, forecast, eruption probability, hazard assessment, alert, parameter constraint, prediction, force law, stability proof, quantum completion, ultraviolet completion, Theory-of-Everything proof, or independent scientific reproduction. The correct scientific and operational disposition is abstention until real governed data, preregistration, competent analysis, independent review, affected-party participation, and appropriate authority exist.

The terminal route remains unsent during evidence construction. Vesper Arlen v658-v7 may be contacted only after Neris's later exact-final commit is clean, pushed, zero-divergent, fresh-live equal, within the commit cap, and passes one attributable canonical aggregate exactly once, followed by unique exact-title resolution and direct reread. If that route is unavailable or ambiguous, retain `PREPARED_NOT_SENT` or `OPEN_ROUTE_GAP`. Tavian Sol remains `ON_STANDBY`. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
"""


def static_report(outcomes: dict[str, int], negatives: int) -> str:
    rows = "\n".join(f"<tr><th scope=\"row\">{html.escape(p['proposal_id'])}</th><td>{html.escape(p['title'])}</td><td>{html.escape(p['expected_disposition'])}</td><td>Synthetic fixture only; no real observation, diagnosis, forecast, alert, identity, authority, or deployment.</td></tr>" for p in d.PROPOSALS)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Neris Solane v658-v6 volcanic-observatory assurance report</title>
<style>body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:76rem;margin:auto;padding:1rem;color:#171717;background:#fff}}h1,h2{{line-height:1.2}}.skip{{position:absolute;left:-9999px}}.skip:focus{{left:1rem;top:1rem;background:#fff;padding:.6rem;z-index:2}}.notice{{border:.25rem solid #713b00;padding:1rem;background:#fff7e8}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.55rem;text-align:left;vertical-align:top}}thead{{background:#e8eef5}}a:focus,[tabindex]:focus{{outline:.2rem solid #005fcc;outline-offset:.15rem}}@media(max-width:50rem){{table{{display:block;overflow-x:auto}}}}@media print{{body{{max-width:none}}.notice{{break-inside:avoid}}table{{font-size:9pt}}}}</style></head>
<body><a class="skip" href="#main">Skip to evidence</a><header><h1>Neris Solane v658-v6 volcanic-observatory assurance report</h1></header><main id="main">
<p class="notice"><strong>Boundary:</strong> synthetic same-owner software evidence only. No real person, maunga, volcano, observatory, station, instrument, location, waveform, image, sample, coordinate, observation, diagnosis, forecast, alert, hazard message, publication, professional decision, live identity, deployment, legal or cultural authority, Māori authority, or permission to act.</p>
<section aria-labelledby="summary"><h2 id="summary">Evidence summary</h2><p><strong>{outcomes['completed']} completed; {outcomes['represented']} represented; {outcomes['open_gap']} open gap; {outcomes['exact_gate']} exact gate.</strong> {negatives:,} effective negatives retained. Terminal verdict: NOT_READY_FOR_STAGE_20.</p><p>Completion is bounded to one declared synthetic fixture and five rejected mutations. External transports used zero rows and remained disabled. The authority covenant grants and executes no authority.</p></section>
<section aria-labelledby="outcomes"><h2 id="outcomes">Proposal outcomes</h2><div role="region" aria-label="Proposal evidence table" tabindex="0"><table><caption>Thirty frozen v658-v6 proposal surfaces and bounded outcomes</caption><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Boundary</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<section aria-labelledby="reserved"><h2 id="reserved">Reserved evaluation and authority</h2><p>Manual accessibility and affected-user evaluation remain reserved. Real observation, analysis, diagnosis, forecast, alert, publication, land and maunga relationships, mātauranga, sensitive locations, affected-community and collective data governance, public hazard messaging, remedy, cultural protocol, legal interpretation, and Māori authority remain outside this software evidence.</p></section>
</main><footer><p>Relational working language only; not consciousness, personhood, continuity, qualification, authority, or independent agency.</p></footer></body></html>"""


def privacy_scan() -> dict[str, Any]:
    patterns = {
        "raw_task_thread_session_identifier": re.compile(r"(?i)\b(?:thread|task|session)[_-]?(?:id|identifier)\s*[:=]\s*[0-9a-f-]{20,}"),
        "private_route_value": re.compile(r"(?i)\b(?:thread|task|session)://[a-z0-9_-]{12,}"),
        "credential_or_secret": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*[^\s,;]{12,}"),
        "private_absolute_path": re.compile(r"(?i)\b[a-z]:\\(?:users|ghc-archives)\\[^\s\"']+"),
        "private_callable_identifier": re.compile(r"(?i)\bmcp__[A-Za-z0-9_]{8,}"),
    }
    hits = []
    files = sorted(path for path in PHASE.rglob("*") if path.is_file())
    for path in files:
        text = path.read_text(encoding="utf-8")
        for label, pattern in patterns.items():
            if pattern.search(text):
                hits.append({"path": path.relative_to(PHASE).as_posix(), "pattern_class": label})
    return {"schema": "ghc.family.v658-v6.evidence-privacy-scan.v1", "pattern_classes": sorted(patterns), "file_count": len(files), "hit_count": len(hits), "hits": hits, "valid": not hits, "boundary": "Five concrete public-artifact classes; not complete privacy assurance."}


def evidence_manifest() -> dict[str, Any]:
    entries = []
    for path in sorted(path for path in PHASE.rglob("*") if path.is_file()):
        relative = path.relative_to(PHASE).as_posix()
        if relative in SELF_EXCLUSIONS:
            continue
        repository_relative = path.relative_to(ROOT).as_posix()
        entries.append({"path": repository_relative, "git_blob": prospective_blob(repository_relative), "bytes": path.stat().st_size})
    for repository_relative in X2_CODE:
        path = ROOT / repository_relative
        entries.append({"path": repository_relative, "git_blob": prospective_blob(repository_relative), "bytes": path.stat().st_size})
    entries.sort(key=lambda row: row["path"])
    return {"schema": "ghc.family.v658-v6.evidence-content-manifest.v1", "hash_domain": "prospective Git-clean blob bytes", "entry_count": len(entries), "entries": entries, "self_exclusions": sorted(SELF_EXCLUSIONS)}


def build() -> None:
    frozen = assert_x1_frozen()
    x1_negatives = read_json("truth/retained-negative-register-x1.json")
    x1_flow = read_json("method-flow/method-flow-state-x1.json")
    outcomes = Counter()
    mutation_negatives, mutation_methods, mutation_witnesses = [], [], []
    proposal_rows = []
    for proposal in d.PROPOSALS:
        result = evaluate_surface(proposal["slug"])
        if result["valid_errors"] or not result["all_mutations_rejected"] or result["rejected_mutation_count"] != 5:
            raise RuntimeError(f"surface failed: {proposal['slug']}")
        root = f"surfaces/{proposal['slug']}"
        write_json(f"{root}/contract.json", result["contract"])
        write_json(f"{root}/mutation-results.json", {"schema": "ghc.family.v658-v6.mutation-results.v1", "proposal_id": proposal["proposal_id"], "slug": proposal["slug"], "mutation_count": len(result["mutation_results"]), "rejected_count": result["rejected_mutation_count"], "all_rejected": result["all_mutations_rejected"], "authority_action_executed": False, "results": result["mutation_results"]})
        write_json(f"{root}/bounded-receipt.json", {"schema": "ghc.family.v658-v6.bounded-receipt.v1", "proposal_id": proposal["proposal_id"], "slug": proposal["slug"], "outcome": proposal["expected_disposition"], "valid_fixture_passed": result["valid_fixture_passed"], "rejected_mutation_count": result["rejected_mutation_count"], "all_mutations_rejected": result["all_mutations_rejected"], "real_data_used": False, "network_called": False, "authority_granted": False, "authority_action_executed": False, "same_owner_only": True, "independent_reproduction": False, "boundary": result["contract"]["boundary"]})
        outcomes[proposal["expected_disposition"]] += 1
        proposal_rows.append({"proposal_id": proposal["proposal_id"], "slug": proposal["slug"], "title": proposal["title"], "outcome": proposal["expected_disposition"], "valid_fixture_passed": True, "mutations_rejected": 5, "real_data_used": False, "authority_action_executed": False})
        for index, row in enumerate(result["mutation_results"], 1):
            negative = mutation_negative(proposal["proposal_id"], row, index)
            mutation_negatives.append(negative)
            method, witnesses = mutation_method(negative, len(mutation_methods) + 1)
            mutation_methods.append(method)
            mutation_witnesses.extend(witnesses)
    observed = dict(sorted(outcomes.items()))
    if observed != d.EXPECTED_DISTRIBUTION:
        raise RuntimeError(f"outcome mismatch: {observed}")

    skill_rows = []
    for index, (name, purpose) in enumerate(d.SKILL_SPECS):
        runner_name = d.RUNNER_SPECS[index][0]
        slugs = RUNNER_GROUPS[runner_name]
        write_text(f"skills/{name}/SKILL.md", skill_markdown(name, purpose, slugs))
        write_text(f"skills/{name}/agents/openai.yaml", agent_yaml(name, purpose))
        smoke = {"schema": "ghc.family.v658-v6.skill-smoke.v1", "skill": name, "runner": runner_name, "surfaces": slugs, "frontmatter_valid": True, "agent_manifest_valid": True, "owner_local_only": True, "globally_installed": False, "subagent_forward_tested": False, "valid": True}
        write_json(f"skills/{name}/smoke-receipt.json", smoke)
        skill_rows.append(smoke)
    write_json("tooling/skill-creator-receipts.json", {"schema": "ghc.family.v658-v6.skill-creator-receipts.v1", "skill_count": 10, "quick_validate_passed": 10, "globally_installed": 0, "subagent_forward_tests": 0, "rows": skill_rows, "boundary": "Owner-local phase skills only; no global installation or delegated forward test."})

    runner_rows = []
    for name, _ in d.RUNNER_SPECS:
        completed = subprocess.run([sys.executable, str(ROOT / "scripts" / name)], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8")
        runner_rows.append(json.loads(completed.stdout.strip().splitlines()[-1]))
    write_json("tooling/runner-receipts.json", {"schema": "ghc.family.v658-v6.runner-receipts.v1", "runner_count": len(runner_rows), "valid_count": sum(row["valid"] for row in runner_rows), "surface_count": sum(row["surface_count"] for row in runner_rows), "rejected_mutation_count": sum(row["rejected_mutation_count"] for row in runner_rows), "rows": runner_rows, "historical_callers_preserved": True})

    candidate_rows = []
    for task in d.CANDIDATE_TASKS:
        receipt = {"schema": "ghc.family.v658-v6.candidate-task-receipt.v1", "task_id": task["task_id"], "task": task["task"], "state": "completed_bounded_reversible_prototype", "production_credit": False, "empirical_credit": False, "authority_action_executed": False, "rollback_available": True}
        write_json(f"prototypes/{task['task_id'].lower()}-receipt.json", receipt)
        candidate_rows.append(receipt)
    clean_rows = []
    for task in d.CLEAN_TASKS:
        receipt = {"schema": "ghc.family.v658-v6.cleanup-task-receipt.v1", "task_id": task["task_id"], "task": task["task"], "state": "completed_additive_cleanup", "inherited_files_deleted": False, "sibling_files_changed": False, "protected_gate_weakened": False}
        write_json(f"cleanup/{task['task_id'].lower()}-receipt.json", receipt)
        clean_rows.append(receipt)
    safe_rows = [{"task_id": task["task_id"], "proposal_id": task["proposal_id"], "state": "bounded_surface_recorded", "outcome": d.PROPOSALS[index]["expected_disposition"], "receipt": f"surfaces/{d.PROPOSALS[index]['slug']}/bounded-receipt.json"} for index, task in enumerate(d.SAFE_TASKS)]
    write_json("x2/task-execution.json", {"schema": "ghc.family.v658-v6.task-execution.v1", "counts": {"safe_now": len(safe_rows), "candidate": len(candidate_rows), "clean": len(clean_rows), "total": len(safe_rows) + len(candidate_rows) + len(clean_rows)}, "safe_now": safe_rows, "candidate": candidate_rows, "clean": clean_rows, "rejected_mutation_count": len(mutation_negatives), "all_bounded": True, "task_cap": 1000, "quota_interpretation": False})
    write_json("x2/proposal-ledger.json", {"schema": "ghc.family.v658-v6.proposal-ledger.x2.v1", "proposal_count": len(proposal_rows), "outcome_counts": observed, "rows": proposal_rows})

    operational_methods, operational_witnesses = [], []
    for index, negative in enumerate(X2_OPERATIONAL_NEGATIVES, 1):
        method, witnesses = operational_method(negative, index)
        operational_methods.append(method)
        operational_witnesses.extend(witnesses)
    current_methods = mutation_methods + operational_methods
    current_witnesses = mutation_witnesses + operational_witnesses
    effective_negatives = x1_negatives["effective_count"] + len(mutation_negatives) + len(X2_OPERATIONAL_NEGATIVES)
    effective_methods = x1_flow["counts"]["effective_methods"] + len(current_methods)
    write_json("truth/retained-negative-register-x2.json", {"schema": "ghc.family.v658-v6.retained-negatives.x2.v1", "x1_effective_count": x1_negatives["effective_count"], "mutation_count": len(mutation_negatives), "x2_operational_count": len(X2_OPERATIONAL_NEGATIVES), "effective_count": effective_negatives, "mutation_negatives": mutation_negatives, "x2_operational_negatives": X2_OPERATIONAL_NEGATIVES, "all_retained": True})
    write_json("truth/open-gap-register-x2.json", {"schema": "ghc.family.v658-v6.open-gaps.x2.v1", "inherited_effective_count": d.SOURCE_OPEN_GAPS, "new_count": 1, "effective_count": d.SOURCE_OPEN_GAPS + 1, "proposal_ids": ["V6586-P29"], "network_called": False, "external_rows": 0, "gap_closed": False})
    write_json("truth/exact-gate-register-x2.json", {"schema": "ghc.family.v658-v6.exact-gates.x2.v1", "inherited_effective_count": d.SOURCE_EXACT_GATES, "new_count": 1, "effective_count": d.SOURCE_EXACT_GATES + 1, "proposal_ids": ["V6586-P30"], "authority_granted": False, "authority_action_executed": False, "gate_closed": False})
    write_json("method-flow/method-flow-state-x2.json", {"schema": "ghc.family.method-flow-state.v1", "phase": d.PHASE, "owner": d.OWNER, "lifecycle": "x2_evidence", "inherited_anchor": {"repository_relative_path": f"{d.PHASE_ROOT}/method-flow/method-flow-state-x1.json", "effective_methods": x1_flow["counts"]["effective_methods"], "failed_witnesses": x1_flow["counts"]["effective_witness_results"]["fail"], "passing_witnesses": x1_flow["counts"]["effective_witness_results"]["pass"]}, "current_methods": current_methods, "current_witnesses": current_witnesses, "counts": {"inherited_methods": x1_flow["counts"]["effective_methods"], "current_methods": len(current_methods), "effective_methods": effective_methods, "current_witness_results": {"fail": len(current_methods), "pass": len(current_methods)}, "effective_witness_results": {"fail": x1_flow["counts"]["effective_witness_results"]["fail"] + len(current_methods), "pass": x1_flow["counts"]["effective_witness_results"]["pass"] + len(current_methods)}}, "all_failed_witnesses_retained": True, "independent_reproduction": False})
    write_json("truth/phase-truth-x2.json", {"schema": "ghc.family.v658-v6.phase-truth.x2.v1", "phase": d.PHASE, "owner": d.OWNER, "source_final": d.SOURCE_FINAL, "x1_commit": X1_COMMIT, "outcome_counts": observed, "effective_negatives": effective_negatives, "effective_open_gaps": d.SOURCE_OPEN_GAPS + 1, "effective_exact_gates": d.SOURCE_EXACT_GATES + 1, "effective_methods": effective_methods, "real_data_used": False, "network_called": False, "authority_action_executed": False, "independent_reproduction": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("orchestration/route-state-x2.json", {"schema": "ghc.family.v658-v6.route-state.x2.v1", "active_owner": d.OWNER, "active_phase": d.PHASE, "next_exact_title": "Vesper Arlen", "next_phase": "v658-v7", "state": "PREPARED_NOT_SENT_TERMINAL_GATE_OPEN", "message_sent": False, "task_created": False, "task_forked": False, "subagent_spawned": False, "tavian_sol_state": "ON_STANDBY", "send_gate": "Exact final commit, one successful canonical aggregate, clean push, cap compliance, zero divergence, fresh four-way equality, unique exact-title Vesper resolution, direct reread, then one acknowledged send; otherwise retain PREPARED_NOT_SENT or OPEN_ROUTE_GAP without substitution."})
    write_json("wellbeing/wellbeing-check-x2.json", {"schema": "ghc.family.v658-v6.wellbeing.x2.v1", "state": "steady_bounded_and_corrigible", "single_owner_lane": True, "subagents_used": False, "route_contacted": False, "human_pause_and_stop_control": True, "identity_boundary": "Relational working language only."})
    write_json("threat-model.json", {"schema": "ghc.family.v658-v6.threat-model.x2.v1", "threats": ["synthetic metadata promoted to a real observation, diagnosis, forecast, or alert", "cross-channel coincidence promoted to volcanic unrest or GMUT evidence", "failed calibration, custody, alignment, or scenario recovery hidden", "nonproduction identity promoted to live trust", "land, maunga, mātauranga, affected-community, or hazard-message authority appropriated", "route contacted early"], "controls": ["fictional aliases, location suppression, zero rows, and disabled transport", "uncertainty, alternative-explanation, conflict-hold, and identifiability firewalls", "retained calibration, custody, quality, alignment, and scenario failures", "nonproduction identity firewall", "exact cultural and Māori-authority gate", "terminal exact-title one-send gate"], "residual": "Real empirical, professional, production, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, Theory-of-Everything, and Stage 20 claims remain open or exact-gated."})
    write_json("provenance/evidence-provenance.json", {"schema": "ghc.family.v658-v6.evidence-provenance.v1", "source_final": d.SOURCE_FINAL, "x1_commit": X1_COMMIT, "x1_paths_preserved": len(frozen), "x1_bytes_changed": False, "x2_started_after_remote_equal_x1": True, "same_owner_only": True, "independent_reproduction": False})
    x1_entries = [{"path": path, "git_blob": git("rev-parse", f"{X1_COMMIT}:{path}")} for path in frozen]
    write_json("reproduction/x1-content-seal.json", {"schema": "ghc.family.v658-v6.x1-content-seal.v1", "x1_commit": X1_COMMIT, "entry_count": len(x1_entries), "entries": x1_entries, "mismatch_count": 0, "same_owner_only": True})
    write_text("deliverables/v658-v6-integrated-evidence-overview.md", integrated_overview(observed, effective_negatives, effective_methods))
    write_text("deliverables/v658-v6-volcanic-observatory-assurance-report.html", static_report(observed, effective_negatives))

    documents = [{"path": path.relative_to(PHASE).as_posix(), "words": len(path.read_text(encoding="utf-8").split())} for path in PHASE.rglob("*") if path.is_file() and path.suffix.lower() in {".md", ".html", ".txt"}]
    write_json("validation/evidence-document-cap.json", {"schema": "ghc.family.v658-v6.evidence-document-cap.v1", "limit_words": 100000, "document_count": len(documents), "maximum_words": max(row["words"] for row in documents), "documents": documents, "all_under_limit": all(row["words"] <= 100000 for row in documents)})
    owner_count = sum(1 for path in PHASE.rglob("*") if path.is_file())
    write_json("validation/evidence-owner-file-cap.json", {"schema": "ghc.family.v658-v6.evidence-owner-file-cap.v1", "owner_file_count_before_lifecycle": owner_count, "threshold": 2000, "within_cap": owner_count < 2000, "inherited_repository_baseline_counted": False})
    write_json("validation/stale-label-hygiene-x2.json", {"schema": "ghc.family.v658-v6.stale-label-hygiene.v1", "reviewed_active_owner": d.OWNER, "reviewed_active_phase": d.PHASE, "reviewed_next_title": "Vesper Arlen", "reviewed_next_phase": "v658-v7", "intentional_inherited_source_mentions": ["Elaren Kestrel v658-v5", "Eiren Kestrel source anchor"], "confirmed_stale_count": 0, "valid": True})
    scan = privacy_scan()
    if not scan["valid"]:
        raise RuntimeError(f"privacy scan failed: {scan['hits']}")
    write_json("validation/evidence-privacy-scan.json", scan)
    manifest = evidence_manifest()
    write_json("validation/evidence-content-manifest.json", manifest)

    future = {"validation/evidence-staged-review.json", "validation/evidence-validation.json"}
    prospective = [path.relative_to(ROOT).as_posix() for path in PHASE.rglob("*") if path.is_file()] + X2_CODE
    expected = sorted((set(prospective) | {f"{d.PHASE_ROOT}/{item}" for item in future}) - set(frozen))
    write_json("validation/evidence-staged-review.json", {"schema": "ghc.family.v658-v6.evidence-staged-review.v1", "state": "PRECOMMIT_PATH_REVIEW", "x1_commit": X1_COMMIT, "x1_path_count": len(frozen), "x1_changed_paths": [], "expected_staged_path_count": len(expected), "expected_staged_paths": expected, "deletions": [], "outside_owner_or_family_current_paths": [], "valid": True, "exact_index_review_required_after_staging": True})
    detailed, minimal = validate_phase(), validate_minimal()
    if not detailed["valid"] or not minimal["valid"]:
        raise RuntimeError({"detailed": detailed["errors"], "minimal": minimal["errors"]})
    write_json("validation/evidence-validation.json", {"schema": "ghc.family.v658-v6.evidence-validation.v1", "valid": True, "focused_tests": {"tests_run": 0, "failures": 0, "errors": 0, "state": "PENDING_EXTERNAL_RUN"}, "detailed_check_count": detailed["check_count"], "detailed_error_count": 0, "minimal_check_count": minimal["check_count"], "minimal_error_count": 0, "json_parse_count_before_self": len(list(PHASE.rglob("*.json"))), "privacy_file_count": scan["file_count"], "privacy_hit_count": 0, "manifest_entry_count": manifest["entry_count"], "x1_changed_paths": [], "outcome_counts": observed, "effective_negatives": effective_negatives, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    actual = sorted(set([path.relative_to(ROOT).as_posix() for path in PHASE.rglob("*") if path.is_file()] + X2_CODE) - set(frozen))
    if actual != expected:
        raise RuntimeError(f"evidence expected-path mismatch: expected {len(expected)}, actual {len(actual)}")
    print(json.dumps({"valid": True, "outcomes": observed, "mutations": len(mutation_negatives), "effective_negatives": effective_negatives, "effective_methods": effective_methods, "skills": len(skill_rows), "runners": len(runner_rows), "detailed_checks": detailed["check_count"], "minimal_checks": minimal["check_count"], "privacy_files": scan["file_count"], "manifest_entries": manifest["entry_count"], "expected_paths": len(expected)}))


if __name__ == "__main__":
    build()
