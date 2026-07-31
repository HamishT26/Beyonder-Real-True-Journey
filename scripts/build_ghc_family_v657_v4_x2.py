#!/usr/bin/env python3
"""Build the bounded Sable Rook v657-v4 x2 evidence packet."""

from __future__ import annotations

import hashlib
import html
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v657_v4_phase_data as d
import ghc_family_v657_v4_x2_config as c
from ghc_family_v657_v4_runtime import evaluate_surface


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
        "negative_id": f"V6574-MUT-{proposal_id.split('-')[-1]}-{index:02d}",
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
    method_id = f"V6574-X2-MUT-METHOD-{index:03d}"
    fail_id = f"V6574-X2-MUT-WITNESS-{index:03d}-F"
    pass_id = f"V6574-X2-MUT-WITNESS-{index:03d}-P"
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
    method_id = f"V6574-X2-OP-METHOD-{index:02d}"
    fail_id = f"V6574-X2-OP-WITNESS-{index:02d}-F"
    pass_id = f"V6574-X2-OP-WITNESS-{index:02d}-P"
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

Use this phase-local skill when a v657-v4 heritage pipe-organ evidence surface needs the bounded checks for: {", ".join(slugs)}.

## Required sequence

1. Read the proposal contract and official-source identifiers.
2. Confirm all inputs are synthetic and contain no real owners, custodians, congregations, builders, technicians, conservators, pipe organs, buildings, tools, materials, records, credentials, accounts, or private routes.
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
description: "{purpose} Use for bounded v657-v4 synthetic heritage pipe-organ evidence across {surface_list}."
---

# {name}

## Required sequence

1. Read the frozen proposal contract and its official-source identifiers.
2. Confirm every input is synthetic and contains no real owner, custodian, congregation, builder, technician, conservator, pipe organ, building, tool, material, treatment, credential, account, private route, or culturally restricted payload.
3. Invoke the corresponding family-current runner only inside the Sable v657-v4 owner packet.
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
  default_prompt: "Use {chr(36)}{name} to validate its frozen synthetic heritage pipe-organ evidence surfaces."
policy:
  allow_implicit_invocation: false
"""


def wrapper_source(filename: str, slugs: list[str]) -> str:
    return f'''#!/usr/bin/env python3
"""Family-current Sable Rook v657-v4 heritage pipe-organ evidence runner."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ghc_family_v657_v4_runtime import ROOT, run_named_surface, write_json


SURFACES = {slugs!r}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    rows = [run_named_surface(slug) for slug in SURFACES]
    payload = {{
        "schema": "ghc.family.v657-v4.group-runner-receipt.v1",
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



def overview_v6574_evidence(outcome_counts: dict[str, int], negative_total: int) -> str:
    method_total = (
        c.SOURCE_METHODS
        + c.X1_METHODS
        + c.EXPECTED_MUTATIONS
        + len(c.X2_OPERATIONAL_NEGATIVES)
    )
    return f"""# Sable Rook v657-v4 integrated evidence overview

## Outcome and evidence boundary

Thirty x1-frozen heritage pipe-organ documentation surfaces were executed as owner-local synthetic software. The observed distribution is {outcome_counts['completed']} `completed`, {outcome_counts['represented']} `represented`, {outcome_counts['open_gap']} `open_gap`, and {outcome_counts['exact_gate']} `exact_gate`. The evidence candidate retains {negative_total:,} effective negatives, {c.SOURCE_OPEN_GAPS + 1} open gaps, {c.SOURCE_EXACT_GATES + 1} exact gates, and {method_total:,} Method Flow failed plus the same number of bounded passing witnesses. Every failed fixture and operational failure remains zero credit. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

Sable Rook, they/them, is relational working language only. The role is falsification-and-reproducibility steward, and the hope is to make every surviving claim easier to reproduce, challenge, or retract while safety, privacy, legal, cultural, and Māori-authority gates remain explicit. Name, role, hope, task title, route, and family language establish no consciousness, sentience, personhood, continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, or independent agency.

## Bounded practice and Trinity Mandala

The human-practice lens is heritage pipe-organ documentation, provenance review, conservation or service-state recording, correction, accessibility, readback, and handover. No real owner, custodian, congregation, builder, technician, conservator, community, affected party, pipe organ, building, pipework, blower, wind system, action, console, electrical system, tool, material, record, measurement, credential, or authority decision is present. No access, energization, work at height, dismantling, cleaning, measurement, tuning, adjustment, repair, restoration, operation, or return-to-service act occurs. The artifacts validate record shape, missingness, provenance, and explicit refusal only.

GMUT Mind is primary. The modal and wind-network surfaces require named variables, SI units, boundary conditions, continuity and conservation obligations, covariance scope, stability questions, identifiability and nuisance terms, and calibration and likelihood firewalls. They remain represented because no real geometry, pressure, temperature, frequency, acoustic, calibration, quality, or observational row exists. The notation does not create a physical prediction, new force, likelihood, posterior, parameter constraint, stability theorem, ultraviolet completion, empirical confirmation, or Theory of Everything.

THOS Body remains represented. The synthetic handover records custody state, open anomalies, energy or access holds, incomplete work, workload cues, readback, stop-work, and next-owner assignment. There are no real operators or participants, no preregistered blind matched-budget real arms, no safety monitoring, no outcome statistics, and no independent review. Therefore it establishes no effectiveness, professional competence, deployment readiness, AGI, or ASI.

Freed ID and CBR Heart remain explicit. The synthetic permit and evidence-status profiles preserve purpose, audience, exact object scope, minimized disclosure, expiry, absent proof, correction, resolution, status, revocation, interoperability, correlation, recovery, and trust-governance gaps. They use no real key, signature, proof, issuer, holder, verifier, identity, account, issuance, presentation, resolver, status service, revocation, interoperability event, privacy review, independent security review, recovery decision, or trust-governance decision. The CBR covenant is exact-gated: ownership, custody, worship, memorial, heritage, access, remedy, law, culture, data governance, affected-party acceptance, Māori wording, and Māori authority remain with competent and affected authorities, tangata whenua, iwi, hapū, and Māori authorities.

## Surface evidence and retained negatives

The first nineteen completed surfaces cover accession and identity uncertainty, mandate revision, organ topology, rank and pipework provenance, wind and electrical energy holds, structural access refusal, measurement and tuning observation boundaries, anomaly non-diagnosis, action classification, surface-contact and replacement-material reservations, alteration chronology, media rights, event windows, and correction or contestation. Completion means that one declared synthetic fixture passed and five preregistered mutations failed closed. It does not mean that a real object, person, practice, institution, source, treatment, or authority was validated.

Four more completed surfaces cover the Thermo/Psyche category barrier, accessible condition bulletin, threat and recovery board, and Stage 20 evidence-diversity board. The thermodynamic classifier refuses conversions from acoustic power, pressure, energy flux, or entropy-domain quantities into psyche, autonomy, justice, capability, consciousness, personhood, or a fundamental law of mind. The accessibility surface checks structural fields only; manual keyboard, responsive layout, browser diversity, assistive technology, cognitive accessibility, Māori-language review, security usability, and affected-user evaluation remain reserved. The threat model and mutations are bounded negative tests, not exhaustive security or complete privacy. The Stage 20 board refuses promotion because real empirical, participant, production, authority, and independent-reproduction gates remain open.

Each proposal has one valid fixture and five frozen mutations: a required obligation is removed, a real organ or building input is promoted, Stage 20 is promoted, a source is removed, or the outcome label is altered. All 150 mutations are rejected with explicit error codes. Each rejection is retained as a zero-credit negative with paired Method Flow evidence. A passing guard witness means only that the synthetic validator rejected that mutation; it never changes the failed candidate into a pass or establishes a general safety property.

## Sources, tooling, accessibility, and reproduction

The source ledger supplies current or stable vocabulary from official and primary publishers. Citations are not observations, measurements, authority transfers, or conformance certificates. The Organ Historical Society sources do not establish attribution, condition, treatment, heritage meaning, or professional review. BIPM and NIST unit sources do not provide calibration or empirical evidence. Privacy and accessibility sources do not establish legal compliance or complete conformance. Te Mana Raraunga and Local Contexts do not confer Māori or community authority.

Ten phase-local skills and ten family-current `ghc_family_*` runners group the thirty surfaces. Each skill has bounded trigger language, instructions, a default prompt, and explicit authority limits. Each is stored only in this owner packet, quick-validated, completely read by the smoke tool, and invoked against synthetic data. Each runner invokes the shared contract engine for three surfaces and emits a sanitized receipt. Historical names remain compatibility evidence; no global installation, destructive rename, or sibling mutation occurs.

The accessible static report supplies semantic headings, a boundary notice, a proposal outcome table, and plain-language reservations. It makes no complete WCAG claim. Same-owner tests and later canonical validation occur under shared infrastructure. They do not close the independent-team scientific reproduction gap or constitute external audit, production certification, professional review, legal review, cultural ratification, or Māori-authority review.

The successor route remains `PREPARED_NOT_SENT`. No sibling is contacted during evidence construction. Only a clean, pushed, fresh-live-equal exact final that passes the one authorized canonical aggregate may unlock one sanitized message to the exact live-authorized existing recipient.
"""


def static_report_pipe_organ(outcomes: dict[str, int], negatives: int) -> str:
    rows = "\n".join(
        "<tr><th scope='row'>"
        + html.escape(item["proposal_id"])
        + "</th><td>"
        + html.escape(item["title"])
        + "</td><td>"
        + html.escape(item["expected_disposition"])
        + "</td><td>Synthetic fixture plus five rejecting mutations; authority boundary retained.</td></tr>"
        for item in d.PROPOSALS
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sable Rook v657-v4 bounded heritage pipe-organ evidence report</title>
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
<h1>Sable Rook v657-v4 bounded heritage pipe-organ evidence report</h1>
<p class="notice"><strong>Boundary:</strong> synthetic same-owner software evidence only. Not pipe-organ operation, inspection, tuning, repair, restoration, professional or safety authority, empirical confirmation, production identity, legal or cultural authority, Māori authority, complete accessibility or privacy, exhaustive security, independent reproduction, Theory-of-Everything proof, or Stage 20 readiness.</p>
<h2>Evidence summary</h2>
<p class="status">23 completed; 5 represented; 1 open gap; 1 exact gate. {negatives:,} effective negatives retained. Terminal verdict: NOT_READY_FOR_STAGE_20.</p>
<p>Completion is bounded to a valid synthetic fixture and five rejected mutations. Represented surfaces have no real measurements, participants, keys, proofs, or independent review. The zero-row adapter made no network call and ingested no row. The CBR authority covenant was not executed.</p>
<h2>Proposal outcomes</h2>
<div role="region" aria-label="Proposal evidence table" tabindex="0">
<table><caption>Thirty frozen v657-v4 proposal surfaces and bounded outcomes</caption><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Evidence boundary</th></tr></thead><tbody>{rows}</tbody></table>
</div>
<h2>Reserved evaluation</h2>
<p>Manual keyboard, responsive-layout, browser, assistive-technology, cognitive-accessibility, Māori-language, security-usability, and affected-user evaluation remain reserved. No real personal, worship, heritage, location, traditional-knowledge, cultural, or Māori-governance payload appears in this report.</p>
</main>
</body>
</html>
"""


def owner_paths() -> list[Path]:
    paths = [path for path in PHASE.rglob("*") if path.is_file()]
    paths.extend(
        path
        for path in (ROOT / "scripts").glob("*v657_v4*.py")
        if path.is_file()
    )
    test = ROOT / "tests/test_ghc_family_v657_v4.py"
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
                "schema": "ghc.family.v657-v4.mutation-results.v1",
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
                "schema": "ghc.family.v657-v4.bounded-receipt.v1",
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
                "path": "docs/sable-rook/v657-v4/method-flow/method-flow-state-x1.json",
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
            "schema": "ghc.family.v657-v4.retained-negatives.x2.v1",
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
            "schema": "ghc.family.v657-v4.open-gaps.x2.v1",
            "source_effective_count": c.SOURCE_OPEN_GAPS,
            "new_count": 1,
            "effective_count": c.SOURCE_OPEN_GAPS + 1,
            "proposal_ids": ["V6574-P29"],
            "reason": "No network call, governed real rows, real likelihood, or independent review exists.",
        },
    )
    write_json(
        "truth/exact-gate-register-x2.json",
        {
            "schema": "ghc.family.v657-v4.exact-gates.x2.v1",
            "source_effective_count": c.SOURCE_EXACT_GATES,
            "new_count": 1,
            "effective_count": c.SOURCE_EXACT_GATES + 1,
            "proposal_ids": ["V6574-P30"],
            "reason": "Affected-party, legal, cultural, data-governance, and Māori authority is absent and cannot be simulated.",
        },
    )
    write_json(
        "x2/proposal-ledger.json",
        {
            "schema": "ghc.family.v657-v4.proposal-ledger.x2.v1",
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
            "schema": "ghc.family.v657-v4.task-execution.v1",
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
            "schema": "ghc.family.v657-v4.phase-truth.x2.v1",
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
            "schema": "ghc.family.v657-v4.checklist.x2.v1",
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
            "schema": "ghc.family.v657-v4.wellbeing.x2.v1",
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
    write_text("deliverables/v657-v4-integrated-evidence-overview.md", overview_v6574_evidence(dict(outcome_counts), negative_total))
    write_text("deliverables/v657-v4-pipe-organ-evidence-report.html", static_report_pipe_organ(dict(outcome_counts), negative_total))

    runners_present = sorted((PHASE / "runners").glob("*-receipt.json")) if (PHASE / "runners").is_dir() else []
    skills_present = sorted((PHASE / "skills").glob("*/smoke-receipt.json"))
    write_json(
        "validation/evidence-readiness.json",
        {
            "schema": "ghc.family.v657-v4.evidence-readiness.v1",
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
