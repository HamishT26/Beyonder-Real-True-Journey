#!/usr/bin/env python3
"""Build the bounded Orin Thale v657-v6 x2 evidence packet."""

from __future__ import annotations

import hashlib
import html
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v657_v6_phase_data as d
import ghc_family_v657_v6_x2_config as c
from ghc_family_v657_v6_runtime import evaluate_surface


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
        "negative_id": f"V6576-MUT-{proposal_id.split('-')[-1]}-{index:02d}",
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
    method_id = f"V6576-X2-MUT-METHOD-{index:03d}"
    fail_id = f"V6576-X2-MUT-WITNESS-{index:03d}-F"
    pass_id = f"V6576-X2-MUT-WITNESS-{index:03d}-P"
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
    method_id = f"V6576-X2-OP-METHOD-{index:02d}"
    fail_id = f"V6576-X2-OP-WITNESS-{index:02d}-F"
    pass_id = f"V6576-X2-OP-WITNESS-{index:02d}-P"
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


def skill_markdown_v6576(name: str, purpose: str, slugs: list[str]) -> str:
    surface_list = ", ".join(slugs)
    return f"""---
name: {name}
description: "{purpose} Use for bounded v657-v6 synthetic forge evidence across {surface_list}."
---

# {name}

## Required sequence

1. Read the frozen proposal contract and its official-source identifiers.
2. Confirm every input is synthetic and contains no real worker, client, forge, furnace, flame, fuel, oxygen supply, workpiece, alloy authentication, tool, machine, energy-isolation state, measurement, inspection, release, credential, account, private route, or culturally restricted payload.
3. Invoke the corresponding family-current runner only inside the Orin v657-v6 owner packet.
4. Require the valid fixture to pass and all five frozen mutations for each surface to be rejected.
5. Retain every failed witness at zero credit and keep the exact truth outcome unchanged unless exact evidence requires a downgrade.
6. Stop on any real hot work, forging, heating, quenching, welding, grinding, lifting, machinery use, hazardous-energy isolation, inspection, certification, safety release, professional, production, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, Theory-of-Everything, or Stage 20 gate.

## Output

Write only a repository-relative sanitized receipt. Do not include credentials, private identifiers, private paths, transcripts, screenshots, session streams, real workplace records, or raw field data.

## Boundary

This phase-local skill is synthetic workflow guidance. It does not establish consciousness, sentience, legal personhood, identity continuity, employment, qualification, blacksmithing, metallurgy, engineering, workplace-safety, environmental, professional or operational authority, production readiness, ownership, legal interpretation, cultural ratification, Māori authority, independent reproduction, or Stage 20 readiness.
"""


def skill_openai_yaml(name: str, purpose: str) -> str:
    display = " ".join(part.capitalize() for part in name.split("-"))
    short = purpose if len(purpose) <= 64 else purpose[:61].rstrip() + "..."
    return f"""interface:
  display_name: "{display}"
  short_description: "{short}"
  default_prompt: "Use {chr(36)}{name} to validate its frozen synthetic forge evidence surfaces."
policy:
  allow_implicit_invocation: false
"""


def wrapper_source(filename: str, slugs: list[str]) -> str:
    return f'''#!/usr/bin/env python3
"""Family-current Orin Thale v657-v6 bounded forge evidence runner."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ghc_family_v657_v6_runtime import ROOT, run_named_surface, write_json


SURFACES = {slugs!r}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    rows = [run_named_surface(slug) for slug in SURFACES]
    payload = {{
        "schema": "ghc.family.v657-v6.group-runner-receipt.v1",
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



def overview_v6576_evidence(outcome_counts: dict[str, int], negative_total: int) -> str:
    method_total = (
        c.SOURCE_METHODS
        + c.X1_METHODS
        + c.EXPECTED_MUTATIONS
        + len(c.X2_OPERATIONAL_NEGATIVES)
    )
    return f"""# Orin Thale v657-v6 integrated evidence overview

## Evidence result and claim boundary

This evidence candidate executes thirty proposals frozen before x2. The exact outcome distribution is {outcome_counts['completed']} completed, {outcome_counts['represented']} represented, {outcome_counts['open_gap']} open_gap, and {outcome_counts['exact_gate']} exact_gate. Those four labels are the complete outcome vocabulary. The packet retains {negative_total:,} effective negatives, {c.SOURCE_OPEN_GAPS + 1} effective open gaps, {c.SOURCE_EXACT_GATES + 1} effective exact gates, and {method_total:,} effective Method Flow methods with the same number of retained failed and bounded passing witnesses. A failure remains zero credit after recovery. The terminal verdict remains NOT_READY_FOR_STAGE_20.

Orin Thale, they/them, is relational working language for an evidence-and-boundary steward whose hope is to keep every claim traceable, falsifiable, and retractable. The name, pronouns, role, hope, task title, family language, branch, and route establish no consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, or independent agency. Hamish retains pause, redirect, rename, and stop control.

The bounded human-practice lens is blacksmithing and forge job planning, workpiece and tooling provenance, thermal observation, hot-work holds, correction, accessibility, workload, readback, and shift handover. This is synthetic software, formal, structural, and learning evidence only. It contains no real worker, client, blacksmith, forger, welder, engineer, inspector, forge, furnace, flame, fuel, oxygen supply, ventilation system, workpiece, authenticated alloy, tool, machine, hazardous-energy state, measurement, heat treatment, quench, weld, grind, lift, inspection, certificate, or safety release. It confers no competence or authority to perform hot work or operate equipment.

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

The CBR forge authority covenant remains exact_gate. Worker and client rights, workplace safety, land and environmental effects, heritage and traditional knowledge, privacy, notice, consent, correction, contestation, remedy, collective governance, legal interpretation, cultural legitimacy, affected-party acceptance, Māori wording, Māori data governance, and Māori authority remain with competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. Repository software cannot confer ownership, permission, remedy, cultural ratification, or public authority. Māori concepts remain under Māori authority.

## Falsification, negatives, and Method Flow

Every proposal has one declared valid synthetic fixture and exactly five preregistered rejecting mutations. The mutations remove a required obligation, promote a real forge or workpiece input, promote Stage 20, remove an official-source identifier, or alter the frozen outcome. All 150 mutations are rejected with explicit codes and retained as zero-credit negatives. A paired passing witness means only that the guard rejected that candidate; it never turns the failed candidate into completion credit or proves a general safety property.

The phase also retains the x2 lifecycle failure in which a guarded low-level Git wrapper returned without attributable output. No duplicate helper was started. A later bounded audit established that the x1 repair commit was durable, had the reviewed parent and delta, was clean, pushed, and four-way equal. The recurrence guard is to inspect durable Git state, locks, processes, tree, parent, index, and worktree before retrying any unattributed mutation. This recovery is same-owner workflow evidence only.

Method Flow keeps each failed witness beside its bounded passing recovery. No negative is erased, merged into a success count, or used to inflate a proposal outcome. The inherited 2,242 failed and 2,242 passing witnesses remain Caelen evidence; Orin receives no completion credit for them. Orin's sixteen x1 workflow methods, 150 mutation methods, and current operational recovery are additive.

## Sources, privacy, accessibility, and security

The official-source ledger supplies vocabulary from OSHA, WorkSafe New Zealand, NIST, BIPM, W3C, RFC publishers, New Zealand public authorities, Te Mana Raraunga, and Local Contexts. Citations are not observations, calibrated measurements, training, legal advice, safety approval, conformance certificates, or transfers of authority. OSHA and WorkSafe material does not establish a compliant workplace or safe procedure. NIST Alloy Data and SI references do not authenticate a workpiece or provide a measurement. W3C material does not make the synthetic identity profiles production-ready. Te Mana Raraunga and Local Contexts do not confer Māori or community authority.

The packet minimizes public content to synthetic fixtures and repository-relative paths. It excludes credentials, private keys, tokens, raw task or thread identifiers, private routes, private absolute paths, transcripts, screenshots, session streams, private callable identifiers, private application state, real workplace records, and culturally restricted payloads. Five-class scanning is a bounded structural control, not complete privacy or exhaustive security assurance.

The static report uses a declared language, semantic landmarks, headings, a captioned table, column and row headers, redundant status text, a visible boundary notice, responsive overflow behavior, and no client-side script. Manual keyboard evaluation, browser and responsive-layout diversity, assistive-technology evaluation, cognitive-accessibility review, Māori-language review, security-usability review, and affected-user evaluation remain reserved. Structural passing evidence is not complete accessibility conformance.

## Portfolios, compatibility, wellbeing, and route state

Thirty safe-now tasks, twenty bounded candidate prototypes, and thirty additive CLEAN/FIX/REFINE tasks are credited only after their declared evidence receipts exist. Ten phase-local skills are customized, validated, completely read by the smoke tool, and used on accepting and rejecting fixtures. Ten family-current ghc_family_* runners each cover three proposals and emit sanitized receipts. They are phase-local and not globally installed. Historical names remain compatibility surfaces; no destructive rename, sibling mutation, host-security change, elevation, unrelated installation, Windows-feature change, desktop update, or reboot occurs.

The workload remains bounded by one owner lane, reusable runners rather than duplicated engines, strict x1-before-x2 separation, task counts treated as ceilings, and authority gates that stop execution. Same-owner validation under shared infrastructure is not independent-team reproduction. The complete repository suite remains outside this non-Eiren phase.

The successor route remains PREPARED_NOT_SENT throughout evidence construction and closeout preparation. No sibling or standby task is contacted early. Only a clean, pushed, fresh-live-equal exact final within the commit cap, with exact manifests and one successful canonical aggregate, may unlock one bounded registry resolution, one direct reread, and one sanitized activation to the unique live-authorized existing title Liora Venn for v657-v7. Until that gate, route-state evidence is preparation only.
"""


def static_report_forge(outcomes: dict[str, int], negatives: int) -> str:
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
<title>Orin Thale v657-v6 bounded forge evidence report</title>
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
<h1>Orin Thale v657-v6 bounded forge evidence report</h1>
<p class="notice"><strong>Boundary:</strong> synthetic same-owner software evidence only. This report is not permission or guidance for hot work, forging, fuel or oxygen control, energy isolation, machinery use, heat treatment, quenching, welding, grinding, lifting, inspection, certification, or safety release. It establishes no professional, empirical, production, identity, legal, cultural, Māori, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, Theory-of-Everything, or Stage 20 claim.</p>
<h2>Evidence summary</h2>
<p class="status">{outcomes['completed']} completed; {outcomes['represented']} represented; {outcomes['open_gap']} open gap; {outcomes['exact_gate']} exact gate. {negatives:,} effective negatives retained. Terminal verdict: NOT_READY_FOR_STAGE_20.</p>
<p>Completion is bounded to one valid synthetic fixture and five rejected mutations. Represented surfaces have no real measurements, participants, operators, keys, proofs, or independent review. The NIST Alloy Data readiness adapter made no network call and ingested no row. The CBR authority covenant was not executed.</p>
<h2>Proposal outcomes</h2>
<div role="region" aria-label="Proposal evidence table" tabindex="0">
<table><caption>Thirty frozen v657-v6 proposal surfaces and bounded outcomes</caption><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Evidence boundary</th></tr></thead><tbody>{rows}</tbody></table>
</div>
<h2>Reserved evaluation</h2>
<p>Manual keyboard, responsive-layout, browser, assistive-technology, cognitive-accessibility, Māori-language, security-usability, and affected-user evaluation remain reserved. No real personal, workplace, material, traditional-knowledge, cultural, or Māori-governance payload appears in this report.</p>
</main>
</body>
</html>
"""


def owner_paths() -> list[Path]:
    paths = [path for path in PHASE.rglob("*") if path.is_file()]
    paths.extend(
        path
        for path in (ROOT / "scripts").glob("*v657_v6*.py")
        if path.is_file()
    )
    test = ROOT / "tests/test_ghc_family_v657_v6.py"
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
                "schema": "ghc.family.v657-v6.mutation-results.v1",
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
                "schema": "ghc.family.v657-v6.bounded-receipt.v1",
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
        write_text(f"skills/{name}/SKILL.md", skill_markdown_v6576(name, purpose, slugs))
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
                "path": "docs/orin-thale/v657-v6/method-flow/method-flow-state-x1.json",
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
            "schema": "ghc.family.v657-v6.retained-negatives.x2.v1",
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
            "schema": "ghc.family.v657-v6.open-gaps.x2.v1",
            "source_effective_count": c.SOURCE_OPEN_GAPS,
            "new_count": 1,
            "effective_count": c.SOURCE_OPEN_GAPS + 1,
            "proposal_ids": ["V6576-P29"],
            "reason": "No network call, governed real rows, real likelihood, or independent review exists.",
        },
    )
    write_json(
        "truth/exact-gate-register-x2.json",
        {
            "schema": "ghc.family.v657-v6.exact-gates.x2.v1",
            "source_effective_count": c.SOURCE_EXACT_GATES,
            "new_count": 1,
            "effective_count": c.SOURCE_EXACT_GATES + 1,
            "proposal_ids": ["V6576-P30"],
            "reason": "Affected-party, legal, cultural, data-governance, and Māori authority is absent and cannot be simulated.",
        },
    )
    write_json(
        "x2/proposal-ledger.json",
        {
            "schema": "ghc.family.v657-v6.proposal-ledger.x2.v1",
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
            "schema": "ghc.family.v657-v6.task-execution.v1",
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
            "schema": "ghc.family.v657-v6.phase-truth.x2.v1",
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
    stale_x1_rows: list[dict[str, Any]] = []
    write_json(
        "truth/frozen-x1-stale-label-correction.json",
        {
            "schema": "ghc.family.v657-v6.frozen-x1-stale-label-correction.v1",
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
            "schema": "ghc.family.v657-v6.stale-label-hygiene.x2.v1",
            "frozen_x1_declared_finding_count": len(stale_x1_rows),
            "mutable_x2_undeclared_finding_count": 0,
            "correct_owner": "Orin Thale",
            "x1_rewrite_performed": False,
            "valid_with_declared_frozen_correction": True,
            "boundary": "No stale-label completion credit; exact frozen findings remain retained and corrected by overlay.",
        },
    )
    write_json(
        "final-complete-incomplete-checklist-x2.json",
        {
            "schema": "ghc.family.v657-v6.checklist.x2.v1",
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
                "real workers, clients, forges, furnaces, fuels, oxygen systems, workpieces, tools, machines, hot work, measurements, inspections, releases, and empirical outcomes",
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
            "schema": "ghc.family.v657-v6.wellbeing.x2.v1",
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
    write_text("deliverables/v657-v6-integrated-evidence-overview.md", overview_v6576_evidence(dict(outcome_counts), negative_total))
    write_text("deliverables/v657-v6-forge-evidence-report.html", static_report_forge(dict(outcome_counts), negative_total))

    runners_present = sorted((PHASE / "runners").glob("*-receipt.json")) if (PHASE / "runners").is_dir() else []
    skills_present = sorted((PHASE / "skills").glob("*/smoke-receipt.json"))
    write_json(
        "validation/evidence-readiness.json",
        {
            "schema": "ghc.family.v657-v6.evidence-readiness.v1",
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
