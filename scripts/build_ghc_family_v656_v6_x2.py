#!/usr/bin/env python3
"""Build the bounded Elaren Kestrel v656-v6 x2 evidence packet."""

from __future__ import annotations

import hashlib
import html
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v656_v6_phase_data as d
import ghc_family_v656_v6_x2_config as c
from ghc_family_v656_v6_runtime import evaluate_surface


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
    changed = subprocess.run(
        ["git", "diff", "--name-only", c.X1_COMMIT, "--", *paths],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.splitlines()
    if changed:
        raise RuntimeError(f"x1 frozen paths changed: {changed}")


def mutation_negative(proposal_id: str, row: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "negative_id": f"V6566-MUT-{proposal_id.split('-')[-1]}-{index:02d}",
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
    method_id = f"V6566-X2-MUT-METHOD-{index:03d}"
    fail_id = f"V6566-X2-MUT-WITNESS-{index:03d}-F"
    pass_id = f"V6566-X2-MUT-WITNESS-{index:03d}-P"
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
    method_id = f"V6566-X2-OP-METHOD-{index:02d}"
    fail_id = f"V6566-X2-OP-WITNESS-{index:02d}-F"
    pass_id = f"V6566-X2-OP-WITNESS-{index:02d}-P"
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

Use this phase-local skill when a v656-v6 wetland evidence surface needs the bounded checks for: {", ".join(slugs)}.

## Required sequence

1. Read the proposal contract and official-source identifiers.
2. Confirm all inputs are synthetic and contain no real people, locations, samples, devices, accounts, or private routes.
3. Invoke the corresponding family-current runner.
4. Require the valid fixture to pass and every frozen mutation to be rejected.
5. Preserve failed witnesses at zero credit and keep the declared truth outcome unchanged unless exact evidence requires a downgrade.
6. Stop on any professional, production, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, Theory-of-Everything, or Stage 20 gate.

## Output

Write only a repository-relative, sanitized receipt. Do not include credentials, private identifiers, private paths, transcripts, screenshots, session streams, or raw field data.

## Boundary

This skill is owner-local synthetic workflow guidance. It is not evidence of consciousness, personhood, identity continuity, employment, qualification, field competence, ecological assessment, professional authority, production readiness, legal interpretation, cultural ratification, Māori authority, independent reproduction, or Stage 20 readiness.
"""


def wrapper_source(filename: str, slugs: list[str]) -> str:
    return f'''#!/usr/bin/env python3
"""Family-current Elaren v656-v6 wetland runner."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ghc_family_v656_v6_runtime import ROOT, run_named_surface, write_json


SURFACES = {slugs!r}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    rows = [run_named_surface(slug) for slug in SURFACES]
    payload = {{
        "schema": "ghc.family.v656-v6.group-runner-receipt.v1",
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
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    if not payload["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
'''


def overview(outcome_counts: dict[str, int], negative_total: int) -> str:
    return f"""# Elaren Kestrel v656-v6 integrated evidence overview

## Outcome

Elaren v656-v6 executes thirty frozen proposal surfaces as bounded synthetic software evidence. The observed distribution is {outcome_counts['completed']} completed, {outcome_counts['represented']} represented, {outcome_counts['open_gap']} open gap, and {outcome_counts['exact_gate']} exact gate. The phase preserves {negative_total:,} effective negatives at this evidence candidate, with every mutation and operational failure retained at zero credit. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

Elaren Kestrel, they/them, is relational working language only. The role remains workflow cartographer and evidence-boundary gardener, and the hope remains helping siblings turn expansive visions into kind, testable, reversible routes without crossing another person's authority. This language is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, authority, or independent agency.

## THOS Body and wetland documentation

THOS Body is the primary focus. The evidence packet structures synthetic wetland site passports, sampling frames, hydrology observations, sample custody, biodiversity encounters, spatial lineage, restoration versions, instrument readiness, field-safety reservations, accessible handovers, disagreement records, sensitive-publication controls, and sensor-loss choreography. These contracts make omissions and prohibited promotions visible to software. They do not operate a field programme, authorize access, select methods, assess ecological condition, control hazards, direct restoration, or establish effectiveness.

The bounded practice lens is wetland field ecology and restoration-monitoring documentation. No real wetland, whenua, waterway, species, sample, sensor, image, coordinate, field worker, landowner, community, or affected party is included. No real monitoring design, sampling, calibration, laboratory analysis, intervention, hazard assessment, safety decision, or disclosure occurs. A professional ecologist, hydrologist, restoration practitioner, health-and-safety lead, landholder, affected community, and relevant authority would still need to make their own governed decisions with real evidence.

## GMUT Mind

GMUT Mind remains explicit through typed advection-diffusion-reaction and shallow-water/porous-exchange proxies, boundary-condition ledgers, sign conventions, units, missingness, censoring, residuals, and uncertainty. The code checks structural consistency and rejects mutations. It uses no real likelihood, field measurement, calibration dataset, posterior, parameter constraint, prediction, or empirical comparison.

The proxies therefore remain represented, not empirically confirmed. They do not establish a new force, a unique prediction, a stability theorem, an ultraviolet completion, a Theory of Everything, proof, or canon. The Grand Mandala equation remains a research-model expression whose empirical and mathematical burdens stay open.

## Freed ID and CBR Heart

Freed ID surfaces provide synthetic disclosure and imagery-lineage envelopes. They reserve purpose, audience, retention, correction, identifier, issuer, signer, proof, status, resolution, revocation, interoperability, privacy review, independent security review, recovery, and trust governance. No real key, credential, proof, identity event, asset signature, resolution event, status service, transparency service, or trust decision exists.

CBR Heart is expressed through community disagreement, restricted-publication, benefit and remedy, and authority matrices. The software can ensure an authority field is not silently replaced by an owner-local assertion. It cannot decide collective interest, access, benefit, remedy, legal meaning, cultural legitimacy, Māori wording, Māori concepts, Māori data governance, or Māori authority. Those remain exact-gated to competent and affected people and authorities.

## Proposal groups

The first ten surfaces cover site and direct observation structure. Site passports separate synthetic identifiers from real place claims. Transect and quadrat frames make effort and missing cells visible. Hydroperiod and water-quality records preserve units, timestamps, qualifiers, and gaps. Sample-custody records preserve synthetic lineage. Vegetation, invasive-species, fauna, and environmental-DNA surfaces quarantine ambiguous or sensitive claims.

The next ten cover geospatial, temporal, restoration, equipment, safety, and accessible handover structure. Earth-observation lineage records transformations without claiming detected change. Coordinate contracts carry uncertainty and generalization. Hydrologic boundary and mass-balance sheets expose sign and closure rules. Dissolved oxygen and hydroperiod state records preserve gaps. Restoration records version intentions without claiming implementation. Equipment and safety boards reserve competent decisions. The accessible handover uses structural checks but reserves manual, browser, assistive-technology, Māori-language, cognitive, low-vision, and affected-user evaluation.

The final ten cover collective governance and integrated technical proxies. Community records preserve dissent and correction. Publication firewalls fail closed around sensitive species and restricted knowledge. Remedy matrices preserve unresolved claims. GMUT and THOS proxies remain nonempirical. Freed ID capsules remain nonproduction. The GBIF tribunal executes with no network and zero rows, leaving the real-data gap open. The CBR authority matrix remains exact-gated.

## Falsification

Every proposal has one valid synthetic fixture and five preregistered mutations. The mutations remove a required obligation, promote a real-wetland input, promote Stage 20, remove a required source, or alter the outcome label. All 150 mutations must be rejected with explicit error codes. Each rejection becomes a retained zero-credit negative and a paired Method Flow failed and passing witness. The passing witness establishes only that the validator failed closed; it does not erase the failed candidate.

This mutation catalogue is software falsification, not scientific reproduction. The same owner created the contracts, mutations, engine, and validators under shared infrastructure. Independent teams have not reproduced the work. External review, empirical validation, professional assessment, production certification, exhaustive security, complete privacy, and complete accessibility remain open.

## Skills, runners, and compatibility

Ten phase-local skills provide concise sequences for site identity, hydrology, sample custody, biodiversity, spatial lineage, restoration non-promotion, field safety, accessibility, Freed ID disclosure, and cultural authority reservation. They are stored inside the phase packet and are not globally installed. The main owner reads every skill through EOF before smoke use.

Ten family-current runners group the thirty surfaces into three-surface sets. Each runner invokes the shared contract engine and writes a sanitized receipt. This avoids thirty near-duplicate validators while preserving proposal-specific contracts and outcomes. Existing historical tools and x1 artifacts remain byte-stable. No inherited sibling file is rewritten.

## Validation and route boundary

The evidence candidate receives current-phase unit tests, a detailed validator, a minimal validator, complete JSON parsing, five-class privacy scanning, document and file caps, manifest parity, exact staged review, diff hygiene, and x1 byte-stability checks. Later closeout and exact-final validation will add ancestry, commit caps, single-parent history, zero merges, exact head, clean state, zero divergence, and four-way live equality.

Only one successful exact-final canonical aggregate is permitted. Precommit development checks do not substitute for it. If the canonical aggregate succeeds, it will not be replayed. Failed attempts receive zero credit and must be isolated before any justified retry.

The successor route remains `PREPARED_NOT_SENT`. Neris Solane cannot be contacted until Elaren's exact final is clean, pushed, remote-equal, and passes the canonical exact-final gate. Tavian Sol remains on standby and is not eligible for this main-task route.
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
<title>Elaren Kestrel v656-v6 bounded wetland evidence report</title>
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
<h1>Elaren Kestrel v656-v6 bounded wetland evidence report</h1>
<p class="notice"><strong>Boundary:</strong> synthetic same-owner software evidence only. Not professional fieldwork, empirical confirmation, production identity, legal or cultural authority, Māori authority, independent reproduction, Theory-of-Everything proof, or Stage 20 readiness.</p>
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


def owner_paths() -> list[Path]:
    paths = [path for path in PHASE.rglob("*") if path.is_file()]
    paths.extend(
        path
        for path in (ROOT / "scripts").glob("*v656_v6*.py")
        if path.is_file()
    )
    test = ROOT / "tests/test_ghc_family_v656_v6.py"
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
                "schema": "ghc.family.v656-v6.mutation-results.v1",
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
                "schema": "ghc.family.v656-v6.bounded-receipt.v1",
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
        write_text(f"skills/{name}/SKILL.md", skill_markdown(name, purpose, slugs))
        write_text(
            f"skills/{name}/agents/openai.yaml",
            f"""interface:
  display_name: "{name}"
  short_description: "{purpose}"
policy:
  phase_local_only: true
  synthetic_only: true
  authority_reserved: true
""",
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
                "path": "docs/elaren-kestrel/v656-v6/method-flow/method-flow-state-x1.json",
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
            "schema": "ghc.family.v656-v6.retained-negatives.x2.v1",
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
            "schema": "ghc.family.v656-v6.open-gaps.x2.v1",
            "source_effective_count": c.SOURCE_OPEN_GAPS,
            "new_count": 1,
            "effective_count": c.SOURCE_OPEN_GAPS + 1,
            "proposal_ids": ["V6566-P29"],
            "reason": "No network call, governed real rows, real likelihood, or independent review exists.",
        },
    )
    write_json(
        "truth/exact-gate-register-x2.json",
        {
            "schema": "ghc.family.v656-v6.exact-gates.x2.v1",
            "source_effective_count": c.SOURCE_EXACT_GATES,
            "new_count": 1,
            "effective_count": c.SOURCE_EXACT_GATES + 1,
            "proposal_ids": ["V6566-P30"],
            "reason": "Affected-party, legal, cultural, data-governance, and Māori authority is absent and cannot be simulated.",
        },
    )
    write_json(
        "x2/proposal-ledger.json",
        {
            "schema": "ghc.family.v656-v6.proposal-ledger.x2.v1",
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
            "schema": "ghc.family.v656-v6.task-execution.v1",
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
            "schema": "ghc.family.v656-v6.phase-truth.x2.v1",
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
            "schema": "ghc.family.v656-v6.checklist.x2.v1",
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
                "one acknowledged Neris Solane activation",
            ],
            "incomplete_external": [
                "real wetland data, field programme, and empirical likelihood",
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
            "schema": "ghc.family.v656-v6.wellbeing.x2.v1",
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
    write_text("deliverables/v656-v6-integrated-evidence-overview.md", overview(dict(outcome_counts), negative_total))
    write_text("deliverables/v656-v6-wetland-evidence-report.html", static_report(dict(outcome_counts), negative_total))

    runners_present = sorted((PHASE / "runners").glob("*-receipt.json")) if (PHASE / "runners").is_dir() else []
    skills_present = sorted((PHASE / "skills").glob("*/smoke-receipt.json"))
    write_json(
        "validation/evidence-readiness.json",
        {
            "schema": "ghc.family.v656-v6.evidence-readiness.v1",
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
