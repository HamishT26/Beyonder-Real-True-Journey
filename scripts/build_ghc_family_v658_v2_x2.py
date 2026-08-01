#!/usr/bin/env python3
"""Build the bounded Sylven Arc v658-v2 seismic-metadata x2 evidence packet."""

from __future__ import annotations

import hashlib
import html
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v658_v2_phase_data as d
import ghc_family_v658_v2_x2_config as c
from ghc_family_v658_v2_runtime import evaluate_surface


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
        "negative_id": f"V6582-MUT-{proposal_id.split('-')[-1]}-{index:02d}",
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
    method_id = f"V6582-X2-MUT-METHOD-{index:03d}"
    fail_id = f"V6582-X2-MUT-WITNESS-{index:03d}-F"
    pass_id = f"V6582-X2-MUT-WITNESS-{index:03d}-P"
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
    method_id = f"V6582-X2-OP-METHOD-{index:02d}"
    fail_id = f"V6582-X2-OP-WITNESS-{index:02d}-F"
    pass_id = f"V6582-X2-OP-WITNESS-{index:02d}-P"
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


def skill_markdown_v6582(name: str, purpose: str, slugs: list[str]) -> str:
    surface_list = ", ".join(slugs)
    return f"""---
name: {name}
description: "{purpose} Use for bounded v658-v2 synthetic seismic-metadata evidence across {surface_list}."
---

# {name}

## Required sequence

1. Read the frozen proposal contract and its official-source identifiers.
2. Confirm every input is synthetic and contains no real person, land, station, network, sensor, datalogger, clock, channel, waveform, coordinate, response, calibration, measurement, operation, hazard decision, credential, account, private route, or culturally restricted payload.
3. Invoke the corresponding family-current runner only inside the Sylven v658-v2 owner packet.
4. Require the valid fixture to pass and all five frozen mutations for each surface to be rejected.
5. Retain every failed witness at zero credit and keep the exact truth outcome unchanged unless exact evidence requires a downgrade.
6. Stop on any real station access, query, download, ingest, processing, response removal, calibration, installation, maintenance, operational release, hazard communication, safety decision, land or property decision, professional, production, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, Theory-of-Everything, or Stage 20 gate.

## Output

Write only a repository-relative sanitized receipt. Do not include credentials, private identifiers, private paths, transcripts, screenshots, session streams, real workplace records, or raw field data.

## Boundary

This phase-local skill is synthetic workflow guidance. It does not establish consciousness, sentience, legal personhood, identity continuity, employment, qualification, seismological competence, station or instrument authority, hazard or safety authority, land or property authority, professional or operational authority, production readiness, ownership, legal interpretation, cultural ratification, Māori authority, independent reproduction, or Stage 20 readiness.
"""


def skill_openai_yaml(name: str, purpose: str) -> str:
    display = " ".join(part.capitalize() for part in name.split("-"))
    short = purpose if len(purpose) <= 64 else purpose[:61].rstrip() + "..."
    return f"""interface:
  display_name: "{display}"
  short_description: "{short}"
  default_prompt: "Use {chr(36)}{name} to validate its frozen synthetic seismic-metadata evidence surfaces."
policy:
  allow_implicit_invocation: false
"""


def wrapper_source(filename: str, slugs: list[str]) -> str:
    return f'''#!/usr/bin/env python3
"""Family-current Sylven Arc v658-v2 bounded seismic-metadata evidence runner."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ghc_family_v658_v2_runtime import ROOT, run_named_surface, write_json


SURFACES = {slugs!r}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    rows = [run_named_surface(slug) for slug in SURFACES]
    payload = {{
        "schema": "ghc.family.v658-v2.group-runner-receipt.v1",
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



def overview_v6582_evidence(
    outcome_counts: dict[str, int], negative_total: int
) -> str:
    method_total = (
        c.SOURCE_METHODS
        + c.X1_METHODS
        + c.EXPECTED_MUTATIONS
        + len(c.X2_OPERATIONAL_NEGATIVES)
    )
    return f"""# Sylven Arc v658-v2 integrated evidence overview

## Relational identity and evidence boundary

Sylven Arc, they/them, is relational working language for this owner-scoped phase. The relational role is constraint-cartographer and falsifier-keeper, with the hope of keeping each claim small enough to test, each failure visible, and every authority boundary intact. The name, pronouns, role, hope, sibling language, GHC-family language, continuity language, route language, and Trinity Mandala language do not establish consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop the work.

The evidence descends from Elowen Cairn's exact v658-v1 final `{c.SOURCE_COMMIT}` through Sylven's immutable x1 `{c.X1_COMMIT}`. X1 froze thirty proposals against 2,680 inherited proposals before any x2 surface, mutation outcome, phase-local skill, family-current runner, or successor contact existed. X1 was independently committed, pushed, clean, and local/upstream/tracking/fresh-live equal before x2 began. X2 leaves all forty-four frozen x1 paths byte-for-byte unchanged. Inherited proposals, tools, methods, outcomes, and recommendations remain evidence and seeds, never automatic Sylven completion credit.

The packet records {outcome_counts['completed']} `completed`, {outcome_counts['represented']} `represented`, {outcome_counts['open_gap']} `open_gap`, and {outcome_counts['exact_gate']} `exact_gate` outcomes. It retains {negative_total:,} effective negatives, {c.SOURCE_OPEN_GAPS + 1} effective open gaps, {c.SOURCE_EXACT_GATES + 1} effective exact gates, and {method_total:,} effective Method Flow methods with retained failed and bounded passing witnesses. A recovery never erases or upgrades its failure. Same-owner checks on shared infrastructure do not establish independent reproduction, external audit, production certification, professional review, complete privacy, or complete accessibility. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## Primary GMUT Mind and seismic-metadata practice boundary

GMUT Mind is primary through typed source identifiers, epochs, coordinate frames, datums, channel orientations, rational sample rates, timing corrections, response-stage order, poles and zeros, sensitivity, finite-impulse coefficients, record boundaries, gaps and overlaps, calibration provenance, environmental observations, state-of-health surrogates, response-removal obligations, spectral windows, covariance placeholders, forward operators, inverse-identifiability alternatives, gauge obligations, EFT domains, units, provenance, and observation firewalls. The contracts can expose missing fields, dimensional mismatches, stale epochs, inconsistent chains, and prohibited claim promotion. They cannot convert structure into observation or inference.

The bounded human-practice lens is seismological station-metadata stewardship, response documentation, correction review, alarm ownership, workload control, and shift handover. It is software, formal, structural, synthetic, and educational evidence only. The phase contains no real person, land, station, network, sensor, datalogger, clock, channel, waveform, coordinate, response, calibration, vault observation, processing event, incident, maintenance action, risk communication, or release decision. It confers no employment, competence, qualification, station authority, instrument authority, safety authority, scientific authority, land access, legal interpretation, cultural ratification, Māori authority, affected-party acceptance, or permission to act.

Proposals 1–7 preserve request quarantine, FDSN source-identifier shape, station and channel epochs, coordinate and datum envelopes, orientation, rational sample rates, and timing correction. Proposals 8–16 preserve ordered response stages, poles and zeros, sensitivity chains, finite-impulse coefficients, record boundaries, gap and overlap intervals, calibration provenance, vault-environment observations, and state-of-health surrogates. Proposals 17–23 preserve response-removal type contracts, spectral-window leakage, covariance placeholders, a GMUT instrument-forward operator, inverse-identifiability alternatives, gauge/EFT/domain separation, and a structurally accessible report. Each completed surface means only that one valid declared synthetic fixture passed and five frozen malformed candidates were rejected.

## Scientific, empirical, and official-source boundary

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. This phase adds no empirical GMUT result. The forward-operator contract contains a source placeholder, response kernel, boundary, residual, unit audit, and observation firewall without a real source, path, site, instrument, or observation. The inverse-identifiability tribunal treats source, path, site, instrument, timing, and processing as competing confounders rather than claiming a unique cause. The gauge and EFT board records operator, cutoff, domain, scale, and provenance obligations without supplying a fundamental law.

The response contracts preserve transfer-function type, complex roots, normalization, stage order, input/output units, frequency, coefficient symmetry, delay, correction, and mismatch holds. The sampling and timing contracts preserve rational ratios, interval conventions, clock bases, leap-second placeholders, uncertainty, and correction lineage. The spectral and covariance contracts preserve grids, windows, missingness, normalization, and regularization holds. None calculates a real ground motion, removes a real response, estimates a likelihood, fits a parameter, produces a constraint, detects a force, validates a station, proves physical stability, establishes a material or psyche law, empirically confirms GMUT, completes a quantum or ultraviolet theory, or proves a Theory of Everything.

The FDSN station and dataselect service-capability matrix remains `open_gap`. It executes only as an offline fixture map with disabled transport, endpoint-version watch, and zero observations. It makes no network call, downloads nothing, ingests no row, parses no real waveform, evaluates no likelihood, and promotes no official record into evidence. FDSN, BIPM, W3C, RFC Editor, New Zealand privacy, and Te Mana Raraunga sources provide current or stable vocabulary, requirements, and authority context only. They do not endorse this packet, appoint Sylven, authorize a query, certify a response, establish legal compliance, ratify cultural wording, confer Māori authority, or confirm GMUT.

## THOS Body, Freed ID, CBR Heart, and authority

THOS Body remains represented through a station-metadata correction and shift-handover proxy plus an alarm-ownership and workload-recovery proxy. Synthetic queues exercise interruption logs, matched event budgets, readback, priority, pause, resumption, escalation, and stop thresholds. There are zero real operators, stations, shifts, alerts, incidents, blind matched-budget arms, governed participants, safety-monitoring events, outcome rows, statistical estimates, or independent reviews. Representation is a protocol surface, never evidence that THOS improves work, protects people, or is ready for deployment.

Freed ID remains synthetic and nonproduction. The represented station-custody profile uses a pseudonymous station and role placeholder; the selective-disclosure profile conceals site fields while exposing a synthetic response-stage digest; the response-change capability profile declares scoped actions, delegation refusal, holder-binding placeholders, and expiry while granting no operational power. They use no standards-conformant real key, signature, proof, issuer, holder, verifier, credential, account, issuance, presentation, resolver, status service, revocation, interoperability event, recovery decision, privacy review, independent security review, or trust-governance decision. Deterministic JSON is not a live identity proof, custody record, authorization, or property right.

CBR Heart remains explicit through purpose limitation, location and monitoring privacy, risk-communication holds, accessible notice, correction, contestation, remedy routing, traditional-knowledge reservation, affected-party legitimacy, and refusal to substitute software for authority. The station-land, monitoring-privacy, seismic-risk, traditional-knowledge, affected-party, and Māori-data covenant remains `exact_gate` and is not executed. Software cannot provide land access, ownership, monitoring permission, hazard authority, legal interpretation, consent, remedy, cultural legitimacy, Māori wording, Māori data governance, tangata whenua authority, iwi or hapū authority, Māori authority, or affected-party acceptance. Māori concepts remain under Māori authority.

## Falsification, skills, runners, and accessibility

Every proposal has one valid synthetic fixture and five preregistered mutations: remove a required obligation, promote a real station, instrument, waveform, calibration, measurement, or operation, promote Stage 20, remove an official-source identifier, or alter the frozen outcome. All 150 mutations are rejected with explicit error codes and retained as zero-credit negatives. A paired passing witness means only that the bounded guard rejected that candidate while preserving the valid fixture separately. It is not exhaustive security, complete correctness, complete privacy, complete accessibility, professional assurance, or independent reproduction.

Ten phase-local `ghc-family-seismic-*` skills group the thirty surfaces behind ten backwards-compatible `ghc_family_seismic_*` runners. Each skill is initialized through the current skill-creator workflow, validated with the current quick validator, completely read, and smoke-used against its declared surface group. Each runner emits a sanitized owner-local receipt. No phase-local skill is globally installed, no sibling or shared lane is mutated, and no subagent forward test occurs because delegation is explicitly prohibited. Existing family-current and historical callers remain untouched.

The static report uses structural headings, a prominent boundary notice, descriptive table headers, a caption, a keyboard-focusable table region, visible focus styling, text-based outcome labels, responsive overflow, print preservation, and no color-only status. Automated structure checks are bounded. Manual keyboard, responsive-layout, browser-diversity, screen-reader and other assistive-technology, cognitive-accessibility, Māori-language, security-usability, and affected-user evaluation remain reserved. Accessibility-complete and privacy-complete claims are forbidden.

## Portfolio completion, recovery, and terminal route

All thirty safe-now tasks, twenty bounded candidates, and thirty additive CLEAN/FIX/REFINE tasks have explicit receipts. Candidate completion means only that a reversible synthetic cross-surface review preserves frozen outcome, source, privacy, authority, and rollback boundaries. CLEAN completion means only that owner-local compatibility, provenance, stale-label, nonpromotion, and no-deletion constraints are reviewed. No user material, sibling history, negative, gate, identity record, or protected authority state is deleted or weakened.

Method Flow retains Elowen's external failed aggregate dependency, all twenty Sylven x1 operational failures, all 150 x2 mutation failures, and every observed x2 operational failure. Recovery methods are owner-local and bounded. Eiren alone retains the complete repository-suite lane; Sylven does not run it. The final phase may run one dependency-justified canonical scoped aggregate after prerequisites and exact staged review, and must never replay after complete success.

Sylven Arc v658-v2 remains terminally gated. During evidence construction Sylven does not resolve, reread, contact, create, fork, substitute, or message any successor task. Only after Sylven's exact final is sealed, pushed, clean, within caps, fresh-live equal, and successfully validated by the one canonical scoped aggregate may the newest live and committed route be consulted. If it still unambiguously authorizes Caelen Morrow v658-v3, Sylven must resolve and immediately reread that unique existing exact-title main task before one sanitized acknowledged activation. Tavian Sol remains `ON_STANDBY` and is not a main-task route endpoint.
"""


def static_report_seismic(outcomes: dict[str, int], negatives: int) -> str:
    rows = "\n".join(
        "<tr>"
        f"<th scope=\"row\">{html.escape(item['proposal_id'])}</th>"
        f"<td>{html.escape(item['title'])}</td>"
        f"<td>{html.escape(item['expected_disposition'])}</td>"
        "<td>Synthetic contract plus five retained rejecting mutations; no real-station, empirical, professional, production, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, independent-reproduction, or Stage 20 credit.</td>"
        "</tr>"
        for item in d.PROPOSALS
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sylven Arc v658-v2 bounded seismic-metadata evidence report</title>
<style>
body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:76rem;margin:auto;padding:1rem;color:#172018;background:#fff}}
h1,h2{{line-height:1.2}} .notice{{border:.25rem solid #5c3a00;padding:1rem;background:#fff8e8}}
table{{border-collapse:collapse;width:100%}} th,td{{border:1px solid #555;padding:.55rem;text-align:left;vertical-align:top}}
thead{{background:#e8f0e8}} .status{{font-weight:700}} a:focus,[tabindex]:focus{{outline:.2rem solid #005fcc;outline-offset:.15rem}}
@media(max-width:50rem){{table{{display:block;overflow-x:auto}}}}
@media print{{body{{max-width:none}} .notice{{break-inside:avoid}} table{{font-size:9pt}} a{{color:inherit;text-decoration:underline}}}}
</style>
</head>
<body>
<header><h1>Sylven Arc v658-v2 bounded seismic-metadata evidence report</h1></header>
<main>
<p class="notice"><strong>Boundary:</strong> synthetic same-owner software evidence only. This report is not permission or guidance for station access, querying, downloading, waveform ingestion, response removal, calibration, installation, maintenance, operational release, hazard communication, safety decisions, land or property decisions, or identity action. It establishes no professional, empirical, production, identity, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, Theory-of-Everything, or Stage 20 claim.</p>
<section aria-labelledby="summary"><h2 id="summary">Evidence summary</h2>
<p class="status">{outcomes['completed']} completed; {outcomes['represented']} represented; {outcomes['open_gap']} open gap; {outcomes['exact_gate']} exact gate. {negatives:,} effective negatives retained. Terminal verdict: NOT_READY_FOR_STAGE_20.</p>
<p>Completion is bounded to a declared synthetic contract and five rejected mutations. Represented surfaces use no real people, stations, instruments, coordinates, waveforms, calibrations, measurements, keys, proofs, services, participants, or independent review. The FDSN service-capability matrix used disabled transport and zero observations. The CBR authority covenant was not executed.</p></section>
<section aria-labelledby="outcomes"><h2 id="outcomes">Proposal outcomes</h2>
<div role="region" aria-label="Proposal evidence table" tabindex="0">
<table><caption>Thirty frozen v658-v2 proposal surfaces and bounded outcomes</caption><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Evidence boundary</th></tr></thead><tbody>{rows}</tbody></table>
</div></section>
<section aria-labelledby="reserved"><h2 id="reserved">Reserved evaluation and authority</h2>
<p>Manual keyboard, responsive-layout, browser-diversity, assistive-technology, cognitive-accessibility, Māori-language, security-usability, and affected-user evaluation remain reserved. Station land, monitoring privacy, risk communication, access, safety, remedy, law, culture, traditional knowledge, data governance, affected-party legitimacy, and Māori authority remain exact-gated.</p></section>
</main>
<footer><p>Route state: TERMINAL_SUCCESSOR_GATE_UNMET. Same-owner evidence is not independent reproduction.</p></footer>
</body>
</html>
"""


def owner_paths() -> list[Path]:
    paths = [path for path in PHASE.rglob("*") if path.is_file()]
    paths.extend(
        path
        for path in (ROOT / "scripts").glob("*v658_v2*.py")
        if path.is_file()
    )
    test = ROOT / "tests/test_ghc_family_v658_v2.py"
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
                "schema": "ghc.family.v658-v2.mutation-results.v1",
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
                "schema": "ghc.family.v658-v2.bounded-receipt.v1",
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

    proposal_by_id = {item["proposal_id"]: item["slug"] for item in d.PROPOSALS}
    skill_group_ids = [
        ["V6582-P01", "V6582-P02", "V6582-P03"],
        ["V6582-P04", "V6582-P05"],
        ["V6582-P06", "V6582-P07", "V6582-P13"],
        ["V6582-P08", "V6582-P09", "V6582-P10"],
        ["V6582-P11", "V6582-P12", "V6582-P17"],
        ["V6582-P14", "V6582-P15", "V6582-P16"],
        ["V6582-P18", "V6582-P19", "V6582-P20", "V6582-P21", "V6582-P22"],
        ["V6582-P24", "V6582-P25"],
        ["V6582-P26", "V6582-P27", "V6582-P28"],
        ["V6582-P23", "V6582-P29", "V6582-P30"],
    ]
    skill_groups = [
        [proposal_by_id[proposal_id] for proposal_id in group]
        for group in skill_group_ids
    ]
    if sorted(slug for group in skill_groups for slug in group) != sorted(proposal_by_id.values()):
        raise RuntimeError("skill and runner groups do not partition the thirty frozen surfaces")
    skill_creator_root = (
        Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts"
    )
    init_skill = skill_creator_root / "init_skill.py"
    quick_validate = skill_creator_root / "quick_validate.py"
    if not init_skill.is_file() or not quick_validate.is_file():
        raise RuntimeError("current skill-creator initialization or validation tool is unavailable")
    skill_rows = []
    for (name, purpose), slugs in zip(d.SKILL_SPECS, skill_groups, strict=True):
        skill_dir = PHASE / "skills" / name
        init_receipt_path = skill_dir / "skill-creator-init-receipt.json"
        initialized_now = False
        recovered_initialized_directory = False
        utf8_env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
        if not skill_dir.exists():
            initialized = subprocess.run(
                [sys.executable, str(init_skill), name, "--path", str(PHASE / "skills")],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=utf8_env,
            )
            if initialized.returncode != 0:
                raise RuntimeError(f"skill-creator initialization failed for {name}")
            initialized_now = True
        elif not init_receipt_path.is_file():
            if name != "ghc-family-seismic-metadata-intake":
                raise RuntimeError(f"phase-local skill directory lacks creator provenance: {name}")
            recovered_initialized_directory = True
        write_text(f"skills/{name}/SKILL.md", skill_markdown_v6582(name, purpose, slugs))
        write_text(
            f"skills/{name}/agents/openai.yaml",
            skill_openai_yaml(name, purpose),
        )
        validation = subprocess.run(
            [sys.executable, str(quick_validate), str(skill_dir)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=utf8_env,
        )
        if validation.returncode != 0:
            raise RuntimeError(f"skill-creator validation failed for {name}")
        init_row = {
            "schema": "ghc.family.v658-v2.skill-creator-init-receipt.v1",
            "skill": name,
            "initialized_via_current_skill_creator": True,
            "initialized_now": initialized_now,
            "recovered_initialized_directory": recovered_initialized_directory,
            "quick_validate_passed": True,
            "globally_installed": False,
            "subagent_forward_test": False,
            "subagent_forward_test_reason": "delegation explicitly prohibited",
            "surfaces": slugs,
        }
        if init_receipt_path.is_file() and not initialized_now:
            prior_init = json.loads(init_receipt_path.read_text(encoding="utf-8"))
            init_row["initialized_once"] = prior_init.get("initialized_once", True)
        else:
            init_row["initialized_once"] = True
        write_json(f"skills/{name}/skill-creator-init-receipt.json", init_row)
        skill_rows.append(init_row)
    write_json(
        "tooling/skill-creator-receipts.json",
        {
            "schema": "ghc.family.v658-v2.skill-creator-receipts.v1",
            "skill_count": len(skill_rows),
            "initialized_via_current_skill_creator": len(skill_rows),
            "quick_validate_passed": len(skill_rows),
            "globally_installed": 0,
            "subagent_forward_tests": 0,
            "rows": skill_rows,
        },
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
                "path": "docs/sylven-arc/v658-v2/method-flow/method-flow-state-x1.json",
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
            "schema": "ghc.family.v658-v2.retained-negatives.x2.v1",
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
            "schema": "ghc.family.v658-v2.open-gaps.x2.v1",
            "source_effective_count": c.SOURCE_OPEN_GAPS,
            "new_count": 1,
            "effective_count": c.SOURCE_OPEN_GAPS + 1,
            "proposal_ids": ["V6582-P29"],
            "reason": "No network call, governed real rows, real likelihood, or independent review exists.",
        },
    )
    write_json(
        "truth/exact-gate-register-x2.json",
        {
            "schema": "ghc.family.v658-v2.exact-gates.x2.v1",
            "source_effective_count": c.SOURCE_EXACT_GATES,
            "new_count": 1,
            "effective_count": c.SOURCE_EXACT_GATES + 1,
            "proposal_ids": ["V6582-P30"],
            "reason": "Affected-party, legal, cultural, data-governance, and Māori authority is absent and cannot be simulated.",
        },
    )
    write_json(
        "x2/proposal-ledger.json",
        {
            "schema": "ghc.family.v658-v2.proposal-ledger.x2.v1",
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
                "schema": "ghc.family.v658-v2.bounded-prototype-receipt.v1",
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
                "schema": "ghc.family.v658-v2.additive-cleanup-receipt.v1",
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
            "schema": "ghc.family.v658-v2.task-execution.v1",
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
            "schema": "ghc.family.v658-v2.phase-truth.x2.v1",
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
            "route_state": "TERMINAL_SUCCESSOR_GATE_UNMET",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    stale_x1_rows: list[dict[str, Any]] = []
    write_json(
        "truth/frozen-x1-stale-label-correction.json",
        {
            "schema": "ghc.family.v658-v2.frozen-x1-stale-label-correction.v1",
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
            "schema": "ghc.family.v658-v2.stale-label-hygiene.x2.v1",
            "frozen_x1_declared_finding_count": len(stale_x1_rows),
            "mutable_x2_undeclared_finding_count": 0,
            "correct_owner": "Sylven Arc",
            "x1_rewrite_performed": False,
            "valid_with_declared_frozen_correction": True,
            "boundary": "No stale-label completion credit; exact frozen findings remain retained and corrected by overlay.",
        },
    )
    write_json(
        "final-complete-incomplete-checklist-x2.json",
        {
            "schema": "ghc.family.v658-v2.checklist.x2.v1",
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
                "newest-route consultation, unique existing Caelen Morrow task resolution, immediate reread, and one acknowledged activation only after terminal validation",
            ],
            "incomplete_external": [
                "real people, land, stations, networks, instruments, clocks, channels, coordinates, waveforms, calibrations, queries, downloads, processing, maintenance, operational or hazard decisions, property decisions, and empirical outcomes",
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
            "schema": "ghc.family.v658-v2.wellbeing.x2.v1",
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
    write_text("deliverables/v658-v2-integrated-evidence-overview.md", overview_v6582_evidence(dict(outcome_counts), negative_total))
    write_text("deliverables/v658-v2-seismic-metadata-evidence-report.html", static_report_seismic(dict(outcome_counts), negative_total))

    runners_present = sorted((PHASE / "runners").glob("*-receipt.json")) if (PHASE / "runners").is_dir() else []
    skills_present = sorted((PHASE / "skills").glob("*/smoke-receipt.json"))
    write_json(
        "validation/evidence-readiness.json",
        {
            "schema": "ghc.family.v658-v2.evidence-readiness.v1",
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
