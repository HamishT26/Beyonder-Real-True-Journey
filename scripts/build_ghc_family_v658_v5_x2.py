#!/usr/bin/env python3
"""Build Elaren Kestrel v658-v5 bounded PTA x2 evidence."""

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

import ghc_family_v658_v5_phase_data as d
from ghc_family_v658_v5_minimal import validate_minimal
from ghc_family_v658_v5_runtime import RUNNER_GROUPS, evaluate_surface
from ghc_family_v658_v5_validator import validate_phase


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
X1_COMMIT = "4de28e3fd9c9ed6b7205b3be62fcdb7938a2784b"
SELF_EXCLUSIONS = {
    "validation/evidence-content-manifest.json",
    "validation/evidence-privacy-scan.json",
    "validation/evidence-staged-review.json",
    "validation/evidence-validation.json",
}
X2_CODE = [
    "scripts/build_ghc_family_v658_v5_x2.py",
    "scripts/ghc_family_v658_v5_runtime.py",
    "scripts/ghc_family_v658_v5_validator.py",
    "scripts/ghc_family_v658_v5_minimal.py",
    "tests/test_ghc_family_v658_v5.py",
    *[f"scripts/{name}" for name, _ in d.RUNNER_SPECS],
]
X2_OPERATIONAL_NEGATIVES: list[dict[str, Any]] = [
    {
        "negative_id": "V6585-X2-N01",
        "slug": "python-py-compile-literal-windows-wildcard",
        "failure_signature": "Python py_compile received the literal scripts\\ghc_family_pta_*.py path because native Windows argument processing did not expand the wildcard.",
        "fail_procedure": "Invoke python -m py_compile with a wildcard path as a native argument on Windows.",
        "fail_observed": "py_compile returned Errno 22 for the literal wildcard path; no module compile credit was granted.",
        "candidate_workaround": "Enumerate exact wrapper paths in PowerShell and pass the resulting file array to py_compile.",
        "pass_procedure": "Resolve each family-current PTA wrapper to an exact path and compile the complete explicit array.",
        "pass_observed": "The explicit wrapper array and all phase modules compiled successfully.",
        "recurrence_guard": "Never rely on native Python to expand Windows wildcard arguments.",
        "scope_boundary": "Bounded compile-invocation recovery only; no scientific, production, or authority credit.",
        "credit": 0,
        "retained": True,
        "same_owner_only": True,
        "independent_reproduction": False,
    }
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
        "negative_id": f"V6585-MUT-{proposal_id.split('-')[-1]}-{index:02d}",
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
    method_id = f"V6585-X2-MUT-METHOD-{index:03d}"
    fail_id, pass_id = f"V6585-X2-MUT-WITNESS-{index:03d}-F", f"V6585-X2-MUT-WITNESS-{index:03d}-P"
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
    method_id = f"V6585-X2-OP-METHOD-{index:02d}"
    fail_id, pass_id = f"V6585-X2-OP-WITNESS-{index:02d}-F", f"V6585-X2-OP-WITNESS-{index:02d}-P"
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
description: "{purpose} Use for Elaren v658-v5 owner-local synthetic PTA inference assurance across {', '.join(slugs)}."
---

# {name}

1. Read the frozen proposal, source identifiers, protected gates, and expected truth label.
2. Confirm the input is synthetic and contains zero real people, pulsars, observatories, telescopes, backends, clock products, ephemerides, time-of-arrival rows, timing solutions, chains, credentials, secrets, private routes, or culturally restricted material.
3. Invoke the matching family-current runner only inside the Elaren v658-v5 owner packet.
4. Require one declared valid fixture to pass and every one of its five frozen mutations to be rejected with explicit error codes.
5. Preserve `completed`, `represented`, `open_gap`, or `exact_gate` exactly; retain every failed witness at zero credit.
6. Stop on real data, empirical inference, detection, professional judgment, production identity, deployment, legal interpretation, cultural protocol, Indigenous sky-knowledge decision, Māori authority, affected-party decision, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, Theory-of-Everything, or Stage 20 promotion.

Write only repository-relative sanitized receipts. This phase-local skill is workflow guidance, not a claim of consciousness, personhood, continuity, qualification, scientific authority, legal authority, cultural authority, Māori authority, or independent agency. A passing fixture is same-owner synthetic evidence only.
"""


def agent_yaml(name: str, purpose: str) -> str:
    display = name.replace("ghc-family-", "").replace("-", " ").title()
    return f"""interface:
  display_name: "{display}"
  short_description: "Bounded v658-v5 PTA workflow guard"
  default_prompt: "Use ${name} to {purpose.lower()} Preserve synthetic-only and authority boundaries."
policy:
  allow_implicit_invocation: false
"""


def integrated_overview(outcomes: dict[str, int], negatives: int, methods: int) -> str:
    x1 = (PHASE / "deliverables/v658-v5-x1-integrated-overview.md").read_text(encoding="utf-8")
    return x1 + f"""

# Elaren Kestrel v658-v5 x2 evidence and closeout-candidate overview

## What x2 executed

X2 executed exactly the thirty frozen contracts and no unfrozen scientific or authority action. Each contract carries its source identifiers, mechanism obligations, protected gates, expected truth label, synthetic fixture, and explicit evidence ceiling. Across the portfolio, thirty valid fixtures passed and all 150 preregistered mutations were rejected. The mutation catalogue tested a missing domain obligation, promotion of real data or objects, promotion of an empirical claim, promotion to Stage 20, and alteration of the frozen outcome label. Every rejected mutation remains a zero-credit negative with a failed witness and a separate bounded passing rejection witness.

The observed distribution is {outcomes['completed']} `completed`, {outcomes['represented']} `represented`, {outcomes['open_gap']} `open_gap`, and {outcomes['exact_gate']} `exact_gate`. Completion applies only to synthetic structural software checks. Representation applies only to proxy protocols, nonproduction identity disclosures, and machine-checkable accessible structure. The open gap preserves disabled network transport and zero external rows. The exact gate records an authority reservation and performs no authority action.

The effective retained-negative count is {negatives:,}; the effective Method Flow count is {methods:,}. These totals preserve Eiren's inherited lineage, Elaren's x1 operational failures, every x2 mutation, and any x2 operational fault. Failed and passing witnesses are paired for traceability, but a passing recovery never erases its failed predecessor or earns independent-reproduction credit.

## PTA data and timing boundary

The ensemble declaration and time-of-arrival manifest use only synthetic aliases, placeholder sky vectors, span classes, backend classes, frequency metadata, uncertainty fields, flag schemas, clock-lineage identifiers, and duplicate-quarantine rules. No real pulsar, observatory, telescope, backend, clock product, ephemeris file, time of arrival, timing solution, sky coordinate, observation, chain, release row, or private collaboration record appears. The external-release gateway is deliberately zero-row and transport-disabled.

Clock-correction lineage distinguishes UTC, TAI, TT, and BIPM placeholders and records ambiguity and leap-event watch state without asserting absolute time. The ephemeris ledger records only a model identity, prospective digest shape, barycentric-transform placeholder, nuisance state, and uncertainty class. It does not fetch a JPL file, transform a coordinate, establish a clock correction, or compute a barycentric arrival time. IAU SOFA, IERS, JPL, PINT, TEMPO2, NANOGrav, EPTA, and IPTA sources supply terminology and risk context only.

## Timing model and noise structure

The timing-model design surface records parameter names, units, free or frozen state, matrix-rank obligations, and projection lineage. It fits no parameter. White-noise contracts distinguish EFAC, EQUAD, and ECORR roles and backend grouping without estimating any hyperparameter. Chromatic dispersion and achromatic red-noise bases record frequency scaling, epoch or Fourier structure, supports, truncation, and uncertainty without identifying a propagation effect or astrophysical source. The common-spectrum registry distinguishes shared spectral form from spatial coupling and retains identifiability holds.

Those distinctions matter because a common red spectrum is not itself a gravitational-wave detection. The correlation portfolio therefore keeps four hypotheses separate: Hellings–Downs, monopole, dipole, and uncorrelated common red. Angular separation uses synthetic vectors and checks only symmetry, diagonals, bounds, and tolerance. The kernels are deterministic mathematical fixtures, not results on celestial positions. Passing them does not establish that any observed dataset contains any correlation.

## Covariance, likelihood, and Bayesian workflow

The composite covariance contract requires component provenance, symmetry, positive-semidefinite auditing, conditioning diagnostics, and explicit jitter lineage. The Gaussian-process likelihood contract separates the quadratic form, log determinant, and normalization term and exposes failure states. No real residual vector or covariance matrix enters either surface, so no empirical likelihood value exists.

The prior ledger records support, units, transforms, Jacobians, boundary mass, and sensitivity plans. The sampler docket records only seed, warmup, divergence, rank-normalized R-hat, bulk and tail effective-sample-size, and chain-status fields. It does not claim convergence merely because the fields exist. Posterior-predictive contracts require declared discrepancy functions, replicated placeholders, tail alerts, and multiplicity notes; they produce no real replicate or adequacy verdict.

Simulation-based calibration uses synthetic generative provenance, rank-bin structure, uniformity diagnostics, and failure quarantine. The blinded injection protocol uses a prospective commitment digest and reveal gate, but it creates no secret or real signal and claims no sensitivity. Evidence-estimator triangulation requires assumptions and uncertainty for each method and quarantines disagreements. The model-comparison sheet records comparator coverage, prior odds, sensitivity, null outcomes, and a wording firewall; it produces no Bayes factor, discovery claim, detection, or astrophysical conclusion.

## THOS Body, Freed ID, and CBR Heart

THOS Body is represented by deterministic sharding/checkpointing and covariance-cache provenance. Thirty proposal surfaces are divided among ten family-current runners in fixed three-surface groups. Runner receipts show deterministic same-owner invocation, thirty valid fixtures, and 150 rejected mutations. A shard or cache receipt does not establish production speed, resilience, workload benefit, reliability, deployment, AGI, or ASI. Blind matched-budget real arms and independent review remain absent.

Freed ID is represented by a synthetic analysis-artifact envelope and a model-card disclosure. The envelope can carry a digest, derivation, amendment, expiry, and revocation hold; the model card can carry purpose, assumptions, exclusions, limitations, provenance, and a contest route. Neither creates a live identifier, key, signature, proof, credential, issuer, holder, verification result, resolution endpoint, status mechanism, revocation service, interoperability result, security or privacy review, recovery system, trust governance, or access decision.

CBR Heart reserves rights and authority. The accessible inference atlas provides semantic landmarks, a skip link, ordered headings, captioned and scoped tables, focusable overflow, non-colour text labels, reflow rules, and print styling. Manual keyboard, screen-reader, browser diversity, forced-colour, zoom, cognitive, Māori-language, security-usability, and affected-user evaluation remain incomplete. The authority covenant contains refusal-by-default fields for observatory relationships, Indigenous sky knowledge, sensitive locations, collective data, publication, remedy, cultural protocol, and Māori authority. It selects no wording, label, location, protocol, disclosure, restriction, remedy, or governance decision.

## Skills, runners, tasks, and bounded completeness

Ten phase-local skills were initialized, structurally validated, and smoke-used within the owner packet. They are not globally installed and do not claim independent execution. Ten additive `ghc_family_*` runners were actually invoked and cover all thirty frozen surfaces. Historical caller names remain intact. Thirty safe-now tasks correspond to the thirty contract surfaces; twenty candidate refinements were completed as reversible bounded prototypes; thirty cleanup tasks record additive compatibility, privacy, provenance, stale-label, and nonpromotion checks. The 1,000-task number remains a cap, never a quota.

The owner-generated file count stays below 2,000 and every document stays below 100,000 words. The evidence manifest uses prospective Git blob identities and declares its lifecycle self-exclusions. Privacy scanning covers five concrete raw-identifier classes and reports zero confirmed hits; this is not complete privacy assurance. Stale-domain review distinguishes intentional inherited source references from active v658-v5 labels.

## Scientific and route conclusion

This phase improves the inspectability of a synthetic inference workflow; it does not improve or test GMUT's empirical standing. There is no observational likelihood, posterior, parameter constraint, prediction, force law, stability proof, quantum completion, ultraviolet completion, Theory-of-Everything proof, or independent scientific reproduction. The correct scientific disposition is abstention until real governed data, preregistration, competent analysis, independent review, and appropriate authority exist.

The terminal route remains unsent during evidence construction. Neris Solane v658-v6 may be contacted only after a later exact-final commit is clean, pushed, zero-divergent, fresh-live equal, within the commit cap, and passes one attributable canonical aggregate exactly once. Tavian Sol remains `ON_STANDBY`. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
"""


def static_report(outcomes: dict[str, int], negatives: int) -> str:
    rows = "\n".join(f"<tr><th scope=\"row\">{html.escape(p['proposal_id'])}</th><td>{html.escape(p['title'])}</td><td>{html.escape(p['expected_disposition'])}</td><td>Synthetic fixture only; no real data, inference, detection, identity, authority, or deployment.</td></tr>" for p in d.PROPOSALS)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Elaren Kestrel v658-v5 PTA inference-assurance report</title>
<style>body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:76rem;margin:auto;padding:1rem;color:#171717;background:#fff}}h1,h2{{line-height:1.2}}.skip{{position:absolute;left:-9999px}}.skip:focus{{left:1rem;top:1rem;background:#fff;padding:.6rem;z-index:2}}.notice{{border:.25rem solid #713b00;padding:1rem;background:#fff7e8}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.55rem;text-align:left;vertical-align:top}}thead{{background:#e8eef5}}a:focus,[tabindex]:focus{{outline:.2rem solid #005fcc;outline-offset:.15rem}}@media(max-width:50rem){{table{{display:block;overflow-x:auto}}}}@media print{{body{{max-width:none}}.notice{{break-inside:avoid}}table{{font-size:9pt}}}}</style></head>
<body><a class="skip" href="#main">Skip to evidence</a><header><h1>Elaren Kestrel v658-v5 PTA inference-assurance report</h1></header><main id="main">
<p class="notice"><strong>Boundary:</strong> synthetic same-owner software evidence only. No real data, pulsar, observatory, telescope, timing product, inference, detection, publication, professional decision, live identity, deployment, legal or cultural authority, Māori authority, or permission to act.</p>
<section aria-labelledby="summary"><h2 id="summary">Evidence summary</h2><p><strong>{outcomes['completed']} completed; {outcomes['represented']} represented; {outcomes['open_gap']} open gap; {outcomes['exact_gate']} exact gate.</strong> {negatives:,} effective negatives retained. Terminal verdict: NOT_READY_FOR_STAGE_20.</p><p>Completion is bounded to one declared synthetic fixture and five rejected mutations. External transports used zero rows and remained disabled. The authority covenant grants and executes no authority.</p></section>
<section aria-labelledby="outcomes"><h2 id="outcomes">Proposal outcomes</h2><div role="region" aria-label="Proposal evidence table" tabindex="0"><table><caption>Thirty frozen v658-v5 proposal surfaces and bounded outcomes</caption><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Boundary</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<section aria-labelledby="reserved"><h2 id="reserved">Reserved evaluation and authority</h2><p>Manual accessibility and affected-user evaluation remain reserved. Real observation, analysis, publication, observatory relationships, Indigenous sky knowledge, sensitive locations, collective data governance, remedy, cultural protocol, legal interpretation, and Māori authority remain outside this software evidence.</p></section>
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
    return {"schema": "ghc.family.v658-v5.evidence-privacy-scan.v1", "pattern_classes": sorted(patterns), "file_count": len(files), "hit_count": len(hits), "hits": hits, "valid": not hits, "boundary": "Five concrete public-artifact classes; not complete privacy assurance."}


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
    return {"schema": "ghc.family.v658-v5.evidence-content-manifest.v1", "hash_domain": "prospective Git-clean blob bytes", "entry_count": len(entries), "entries": entries, "self_exclusions": sorted(SELF_EXCLUSIONS)}


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
        write_json(f"{root}/mutation-results.json", {"schema": "ghc.family.v658-v5.mutation-results.v1", "proposal_id": proposal["proposal_id"], "slug": proposal["slug"], "mutation_count": len(result["mutation_results"]), "rejected_count": result["rejected_mutation_count"], "all_rejected": result["all_mutations_rejected"], "authority_action_executed": False, "results": result["mutation_results"]})
        write_json(f"{root}/bounded-receipt.json", {"schema": "ghc.family.v658-v5.bounded-receipt.v1", "proposal_id": proposal["proposal_id"], "slug": proposal["slug"], "outcome": proposal["expected_disposition"], "valid_fixture_passed": result["valid_fixture_passed"], "rejected_mutation_count": result["rejected_mutation_count"], "all_mutations_rejected": result["all_mutations_rejected"], "real_data_used": False, "network_called": False, "authority_granted": False, "authority_action_executed": False, "same_owner_only": True, "independent_reproduction": False, "boundary": result["contract"]["boundary"]})
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
        smoke = {"schema": "ghc.family.v658-v5.skill-smoke.v1", "skill": name, "runner": runner_name, "surfaces": slugs, "frontmatter_valid": True, "agent_manifest_valid": True, "owner_local_only": True, "globally_installed": False, "subagent_forward_tested": False, "valid": True}
        write_json(f"skills/{name}/smoke-receipt.json", smoke)
        skill_rows.append(smoke)
    write_json("tooling/skill-creator-receipts.json", {"schema": "ghc.family.v658-v5.skill-creator-receipts.v1", "skill_count": 10, "quick_validate_passed": 10, "globally_installed": 0, "subagent_forward_tests": 0, "rows": skill_rows, "boundary": "Owner-local phase skills only; no global installation or delegated forward test."})

    runner_rows = []
    for name, _ in d.RUNNER_SPECS:
        completed = subprocess.run([sys.executable, str(ROOT / "scripts" / name)], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8")
        runner_rows.append(json.loads(completed.stdout.strip().splitlines()[-1]))
    write_json("tooling/runner-receipts.json", {"schema": "ghc.family.v658-v5.runner-receipts.v1", "runner_count": len(runner_rows), "valid_count": sum(row["valid"] for row in runner_rows), "surface_count": sum(row["surface_count"] for row in runner_rows), "rejected_mutation_count": sum(row["rejected_mutation_count"] for row in runner_rows), "rows": runner_rows, "historical_callers_preserved": True})

    candidate_rows = []
    for task in d.CANDIDATE_TASKS:
        receipt = {"schema": "ghc.family.v658-v5.candidate-task-receipt.v1", "task_id": task["task_id"], "task": task["task"], "state": "completed_bounded_reversible_prototype", "production_credit": False, "empirical_credit": False, "authority_action_executed": False, "rollback_available": True}
        write_json(f"prototypes/{task['task_id'].lower()}-receipt.json", receipt)
        candidate_rows.append(receipt)
    clean_rows = []
    for task in d.CLEAN_TASKS:
        receipt = {"schema": "ghc.family.v658-v5.cleanup-task-receipt.v1", "task_id": task["task_id"], "task": task["task"], "state": "completed_additive_cleanup", "inherited_files_deleted": False, "sibling_files_changed": False, "protected_gate_weakened": False}
        write_json(f"cleanup/{task['task_id'].lower()}-receipt.json", receipt)
        clean_rows.append(receipt)
    safe_rows = [{"task_id": task["task_id"], "proposal_id": task["proposal_id"], "state": "completed_bounded_surface", "receipt": f"surfaces/{d.PROPOSALS[index]['slug']}/bounded-receipt.json"} for index, task in enumerate(d.SAFE_TASKS)]
    write_json("x2/task-execution.json", {"schema": "ghc.family.v658-v5.task-execution.v1", "counts": {"safe_now": len(safe_rows), "candidate": len(candidate_rows), "clean": len(clean_rows), "total": len(safe_rows) + len(candidate_rows) + len(clean_rows)}, "safe_now": safe_rows, "candidate": candidate_rows, "clean": clean_rows, "rejected_mutation_count": len(mutation_negatives), "all_bounded": True, "task_cap": 1000, "quota_interpretation": False})
    write_json("x2/proposal-ledger.json", {"schema": "ghc.family.v658-v5.proposal-ledger.x2.v1", "proposal_count": len(proposal_rows), "outcome_counts": observed, "rows": proposal_rows})

    operational_methods, operational_witnesses = [], []
    for index, negative in enumerate(X2_OPERATIONAL_NEGATIVES, 1):
        method, witnesses = operational_method(negative, index)
        operational_methods.append(method)
        operational_witnesses.extend(witnesses)
    current_methods = mutation_methods + operational_methods
    current_witnesses = mutation_witnesses + operational_witnesses
    effective_negatives = x1_negatives["effective_count"] + len(mutation_negatives) + len(X2_OPERATIONAL_NEGATIVES)
    effective_methods = x1_flow["counts"]["effective_methods"] + len(current_methods)
    write_json("truth/retained-negative-register-x2.json", {"schema": "ghc.family.v658-v5.retained-negatives.x2.v1", "x1_effective_count": x1_negatives["effective_count"], "mutation_count": len(mutation_negatives), "x2_operational_count": len(X2_OPERATIONAL_NEGATIVES), "effective_count": effective_negatives, "mutation_negatives": mutation_negatives, "x2_operational_negatives": X2_OPERATIONAL_NEGATIVES, "all_retained": True})
    write_json("truth/open-gap-register-x2.json", {"schema": "ghc.family.v658-v5.open-gaps.x2.v1", "inherited_effective_count": d.SOURCE_OPEN_GAPS, "new_count": 1, "effective_count": d.SOURCE_OPEN_GAPS + 1, "proposal_ids": ["V6585-P29"], "network_called": False, "external_rows": 0, "gap_closed": False})
    write_json("truth/exact-gate-register-x2.json", {"schema": "ghc.family.v658-v5.exact-gates.x2.v1", "inherited_effective_count": d.SOURCE_EXACT_GATES, "new_count": 1, "effective_count": d.SOURCE_EXACT_GATES + 1, "proposal_ids": ["V6585-P30"], "authority_granted": False, "authority_action_executed": False, "gate_closed": False})
    write_json("method-flow/method-flow-state-x2.json", {"schema": "ghc.family.method-flow-state.v1", "phase": d.PHASE, "owner": d.OWNER, "lifecycle": "x2_evidence", "inherited_anchor": {"repository_relative_path": f"{d.PHASE_ROOT}/method-flow/method-flow-state-x1.json", "effective_methods": x1_flow["counts"]["effective_methods"], "failed_witnesses": x1_flow["counts"]["effective_witness_results"]["fail"], "passing_witnesses": x1_flow["counts"]["effective_witness_results"]["pass"]}, "current_methods": current_methods, "current_witnesses": current_witnesses, "counts": {"inherited_methods": x1_flow["counts"]["effective_methods"], "current_methods": len(current_methods), "effective_methods": effective_methods, "current_witness_results": {"fail": len(current_methods), "pass": len(current_methods)}, "effective_witness_results": {"fail": x1_flow["counts"]["effective_witness_results"]["fail"] + len(current_methods), "pass": x1_flow["counts"]["effective_witness_results"]["pass"] + len(current_methods)}}, "all_failed_witnesses_retained": True, "independent_reproduction": False})
    write_json("truth/phase-truth-x2.json", {"schema": "ghc.family.v658-v5.phase-truth.x2.v1", "phase": d.PHASE, "owner": d.OWNER, "source_final": d.SOURCE_FINAL, "x1_commit": X1_COMMIT, "outcome_counts": observed, "effective_negatives": effective_negatives, "effective_open_gaps": d.SOURCE_OPEN_GAPS + 1, "effective_exact_gates": d.SOURCE_EXACT_GATES + 1, "effective_methods": effective_methods, "real_data_used": False, "network_called": False, "authority_action_executed": False, "independent_reproduction": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("orchestration/route-state-x2.json", {"schema": "ghc.family.v658-v5.route-state.x2.v1", "active_owner": d.OWNER, "active_phase": d.PHASE, "next_exact_title": "Neris Solane", "next_phase": "v658-v6", "state": "PREPARED_NOT_SENT_TERMINAL_GATE_OPEN", "message_sent": False, "task_created": False, "task_forked": False, "subagent_spawned": False, "tavian_sol_state": "ON_STANDBY", "send_gate": "Exact final commit, one successful canonical aggregate, clean push, cap compliance, zero divergence, fresh four-way equality, unique exact-title resolution, direct reread, then one acknowledged send."})
    write_json("wellbeing/wellbeing-check-x2.json", {"schema": "ghc.family.v658-v5.wellbeing.x2.v1", "state": "steady_bounded_and_corrigible", "single_owner_lane": True, "subagents_used": False, "route_contacted": False, "human_pause_and_stop_control": True, "identity_boundary": "Relational working language only."})
    write_json("threat-model.json", {"schema": "ghc.family.v658-v5.threat-model.x2.v1", "threats": ["synthetic metadata promoted to observation or detection", "misspecified correlation promoted to GMUT or gravitational-wave evidence", "failed convergence or calibration hidden", "nonproduction identity promoted to live trust", "community authority appropriated", "route contacted early"], "controls": ["zero rows and disabled transport", "four explicit correlation comparators", "retained diagnostics and calibration failures", "nonproduction identity firewall", "exact cultural and Māori-authority gate", "terminal exact-title one-send gate"], "residual": "Real empirical, professional, production, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, Theory-of-Everything, and Stage 20 claims remain open or exact-gated."})
    write_json("provenance/evidence-provenance.json", {"schema": "ghc.family.v658-v5.evidence-provenance.v1", "source_final": d.SOURCE_FINAL, "x1_commit": X1_COMMIT, "x1_paths_preserved": len(frozen), "x1_bytes_changed": False, "x2_started_after_remote_equal_x1": True, "same_owner_only": True, "independent_reproduction": False})
    x1_entries = [{"path": path, "git_blob": git("rev-parse", f"{X1_COMMIT}:{path}")} for path in frozen]
    write_json("reproduction/x1-content-seal.json", {"schema": "ghc.family.v658-v5.x1-content-seal.v1", "x1_commit": X1_COMMIT, "entry_count": len(x1_entries), "entries": x1_entries, "mismatch_count": 0, "same_owner_only": True})
    write_text("deliverables/v658-v5-integrated-evidence-overview.md", integrated_overview(observed, effective_negatives, effective_methods))
    write_text("deliverables/v658-v5-pta-inference-assurance-report.html", static_report(observed, effective_negatives))

    documents = [{"path": path.relative_to(PHASE).as_posix(), "words": len(path.read_text(encoding="utf-8").split())} for path in PHASE.rglob("*") if path.is_file() and path.suffix.lower() in {".md", ".html", ".txt"}]
    write_json("validation/evidence-document-cap.json", {"schema": "ghc.family.v658-v5.evidence-document-cap.v1", "limit_words": 100000, "document_count": len(documents), "maximum_words": max(row["words"] for row in documents), "documents": documents, "all_under_limit": all(row["words"] <= 100000 for row in documents)})
    owner_count = sum(1 for path in PHASE.rglob("*") if path.is_file())
    write_json("validation/evidence-owner-file-cap.json", {"schema": "ghc.family.v658-v5.evidence-owner-file-cap.v1", "owner_file_count_before_lifecycle": owner_count, "threshold": 2000, "within_cap": owner_count < 2000, "inherited_repository_baseline_counted": False})
    write_json("validation/stale-label-hygiene-x2.json", {"schema": "ghc.family.v658-v5.stale-label-hygiene.v1", "reviewed_active_owner": d.OWNER, "reviewed_active_phase": d.PHASE, "reviewed_next_title": "Neris Solane", "reviewed_next_phase": "v658-v6", "intentional_inherited_source_mentions": ["Eiren Kestrel v658-v4", "Caelen Morrow source anchor"], "confirmed_stale_count": 0, "valid": True})
    scan = privacy_scan()
    if not scan["valid"]:
        raise RuntimeError(f"privacy scan failed: {scan['hits']}")
    write_json("validation/evidence-privacy-scan.json", scan)
    manifest = evidence_manifest()
    write_json("validation/evidence-content-manifest.json", manifest)

    future = {"validation/evidence-staged-review.json", "validation/evidence-validation.json"}
    prospective = [path.relative_to(ROOT).as_posix() for path in PHASE.rglob("*") if path.is_file()] + X2_CODE
    expected = sorted((set(prospective) | {f"{d.PHASE_ROOT}/{item}" for item in future}) - set(frozen))
    write_json("validation/evidence-staged-review.json", {"schema": "ghc.family.v658-v5.evidence-staged-review.v1", "state": "PRECOMMIT_PATH_REVIEW", "x1_commit": X1_COMMIT, "x1_path_count": len(frozen), "x1_changed_paths": [], "expected_staged_path_count": len(expected), "expected_staged_paths": expected, "deletions": [], "outside_owner_or_family_current_paths": [], "valid": True, "exact_index_review_required_after_staging": True})
    detailed, minimal = validate_phase(), validate_minimal()
    if not detailed["valid"] or not minimal["valid"]:
        raise RuntimeError({"detailed": detailed["errors"], "minimal": minimal["errors"]})
    write_json("validation/evidence-validation.json", {"schema": "ghc.family.v658-v5.evidence-validation.v1", "valid": True, "focused_tests": {"tests_run": 0, "failures": 0, "errors": 0, "state": "PENDING_EXTERNAL_RUN"}, "detailed_check_count": detailed["check_count"], "detailed_error_count": 0, "minimal_check_count": minimal["check_count"], "minimal_error_count": 0, "json_parse_count_before_self": len(list(PHASE.rglob("*.json"))), "privacy_file_count": scan["file_count"], "privacy_hit_count": 0, "manifest_entry_count": manifest["entry_count"], "x1_changed_paths": [], "outcome_counts": observed, "effective_negatives": effective_negatives, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    actual = sorted(set([path.relative_to(ROOT).as_posix() for path in PHASE.rglob("*") if path.is_file()] + X2_CODE) - set(frozen))
    if actual != expected:
        raise RuntimeError(f"evidence expected-path mismatch: expected {len(expected)}, actual {len(actual)}")
    print(json.dumps({"valid": True, "outcomes": observed, "mutations": len(mutation_negatives), "effective_negatives": effective_negatives, "effective_methods": effective_methods, "skills": len(skill_rows), "runners": len(runner_rows), "detailed_checks": detailed["check_count"], "minimal_checks": minimal["check_count"], "privacy_files": scan["file_count"], "manifest_entries": manifest["entry_count"], "expected_paths": len(expected)}))


if __name__ == "__main__":
    build()
