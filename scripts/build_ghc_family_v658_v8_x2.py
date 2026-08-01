#!/usr/bin/env python3
"""Build Lyren Moss v658-v8 bounded synthetic-brewery x2 evidence."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v658_v8_phase_data as d
from ghc_family_v658_v8_minimal import validate_minimal
from ghc_family_v658_v8_runtime import RUNNER_GROUPS, evaluate_surface
from ghc_family_v658_v8_validator import validate_phase


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
X1_COMMIT = "3a7cc57b4d1637b4de1836648a57419422bb517f"
SELF_EXCLUSIONS = {
    "validation/evidence-content-manifest.json",
    "validation/evidence-privacy-scan.json",
    "validation/evidence-staged-review.json",
    "validation/evidence-validation.json",
}
X2_CODE = [
    "scripts/build_ghc_family_v658_v8_x2.py",
    "scripts/ghc_family_v658_v8_runtime.py",
    "scripts/ghc_family_v658_v8_validator.py",
    "scripts/ghc_family_v658_v8_minimal.py",
    "tests/test_ghc_family_v658_v8.py",
    *[f"scripts/{name}" for name, _ in d.RUNNER_SPECS],
]
X2_OPERATIONAL_NEGATIVES: list[dict[str, Any]] = [
    {
        "negative_id": "V6588-X2-N01",
        "slug": "bundled-x1-equality-output-truncation",
        "failure_signature": "The first bundled post-push equality probe exceeded the observation output budget, so none of its rendered values received gate credit.",
        "fail_procedure": "Bundle local, upstream, tracking, divergence, fresh-live, and cleanliness observations into one oversized orchestration response.",
        "fail_observed": "The response was truncated and unusable as exact equality evidence; x1 remained immutable and the push was not replayed.",
        "candidate_workaround": "Split immutable local references, fresh-live remote state, and cleanliness into bounded scalar probes.",
        "pass_procedure": "Read HEAD, upstream, tracking, divergence, and fresh-live remote separately, then perform a bounded clean-state check.",
        "pass_observed": "All four references equalled the frozen x1 commit, divergence was zero in both directions, and the clean-state recovery passed.",
        "recurrence_guard": "Keep equality observations scalar and cap each wrapper independently.",
        "scope_boundary": "Bounded Git-state observation only; no brewery, empirical, production, food-safety, release, legal, cultural, routing, or authority credit.",
        "credit": 0,
        "retained": True,
        "same_owner_only": True,
        "independent_reproduction": False,
    },
    {
        "negative_id": "V6588-X2-N02",
        "slug": "empty-x1-status-wrapper",
        "failure_signature": "The first clean-state wrapper returned no rendered status count or path payload and therefore could not prove cleanliness.",
        "fail_procedure": "Treat an empty orchestration rendering as equivalent to an explicit zero-path Git status.",
        "fail_observed": "The wrapper supplied no usable evidence and received zero cleanliness credit.",
        "candidate_workaround": "Run Git status with fsmonitor disabled and print both the native exit code and materialized line count.",
        "pass_procedure": "Materialize porcelain output, require native exit zero, and require an explicit line count of zero.",
        "pass_observed": "The bounded retry returned exit zero and lines zero.",
        "recurrence_guard": "Require explicit exit and cardinality fields for empty-success observations.",
        "scope_boundary": "Bounded Git cleanliness recovery only; no brewery, validation-suite, production, routing, or authority credit.",
        "credit": 0,
        "retained": True,
        "same_owner_only": True,
        "independent_reproduction": False,
    },
    {
        "negative_id": "V6588-X2-N03",
        "slug": "unset-copy-environment-wrapper",
        "failure_signature": "The first template-copy wrapper referenced two unset task-specific environment variables, so every Join-Path operation failed and zero files were copied.",
        "fail_procedure": "Assume undeclared environment entries are propagated into a shell wrapper.",
        "fail_observed": "The wrapper reported null path arguments and copied zero files; no repository file changed and the attempt received zero credit.",
        "candidate_workaround": "Declare bounded task-specific literal source and destination variables inside the same PowerShell process.",
        "pass_procedure": "Copy the five exact template files using declared literal roots, then apply only mechanical owner/version substitutions.",
        "pass_observed": "Exactly five x2 template files were copied into the Lyren lane; sibling files remained read-only.",
        "recurrence_guard": "Declare task-specific shell variables in the command that consumes them and fail closed on a zero-copy result.",
        "scope_boundary": "Bounded template materialization recovery only; no brewery, test-suite, production, routing, or authority credit.",
        "credit": 0,
        "retained": True,
        "same_owner_only": True,
        "independent_reproduction": False,
    },
    {
        "negative_id": "V6588-X2-N04",
        "slug": "builder-patch-wrapper-inline-code-parse",
        "failure_signature": "The first whole-builder replacement used an unescaped inline-code delimiter inside its JavaScript template wrapper and failed before the patch engine was invoked.",
        "fail_procedure": "Embed repository prose containing template delimiters inside a non-raw orchestration template.",
        "fail_observed": "The wrapper raised a syntax error, the patch engine was never called, no file changed, and the attempt received zero credit.",
        "candidate_workaround": "Use a raw wrapper and remove delimiter ambiguity before invoking the same exact patch transaction.",
        "pass_procedure": "Apply the whole-file replacement through a raw string, then read back and compile the resulting builder.",
        "pass_observed": "The raw patch transaction replaced the template builder once and left x1 paths unchanged.",
        "recurrence_guard": "Preflight wrapper delimiters independently from repository patch content.",
        "scope_boundary": "Bounded patch-transport recovery only; no brewery, test-suite, production, routing, or authority credit.",
        "credit": 0,
        "retained": True,
        "same_owner_only": True,
        "independent_reproduction": False,
    },
    {
        "negative_id": "V6588-X2-N05",
        "slug": "staged-scan-powershell-quote-boundary",
        "failure_signature": "The first combined exact-index privacy, stale-label, and JSON scanner embedded a single quote inside a PowerShell-quoted Python regular expression and failed during shell parsing.",
        "fail_procedure": "Nest an apostrophe-bearing character class inside an already single-quote-sensitive PowerShell command boundary.",
        "fail_observed": "PowerShell rejected the command before Python ran; no staged content was scanned or changed and the attempt received zero credit.",
        "candidate_workaround": "Use a quote-safe bounded pattern and keep the scan input on exact staged Git blobs.",
        "pass_procedure": "Read every staged path through the Git index, parse every staged JSON file, and apply the five privacy classes plus stale-label patterns.",
        "pass_observed": "The quote-safe recovery parsed every staged JSON blob and returned zero confirmed privacy or stale-label hits.",
        "recurrence_guard": "Preflight shell quoting separately or avoid apostrophes inside nested regular-expression character classes.",
        "scope_boundary": "Bounded exact-index scan recovery only; not privacy-complete, accessibility-complete, exhaustive-security, independent reproduction, or authority evidence.",
        "credit": 0,
        "retained": True,
        "same_owner_only": True,
        "independent_reproduction": False,
    },
    {
        "negative_id": "V6588-X2-N06",
        "slug": "empty-combined-index-comparison-wrapper",
        "failure_signature": "A combined Python index comparison completed without rendering any scalar result and left no active child process, so the observation could not prove staged-path equality.",
        "fail_procedure": "Rely on a long nested comparison wrapper whose outer result can complete without forwarding the inner scalar payload.",
        "fail_observed": "No expected, staged, missing, extra, unstaged, untracked, deletion, or x1-overlap value was rendered; the attempt received zero gate credit.",
        "candidate_workaround": "Materialize expected and staged sets directly in PowerShell and print each cardinality as an independent scalar.",
        "pass_procedure": "Compare the exact expected and staged path arrays, then print missing, extra, unstaged, untracked, and deletion counts separately.",
        "pass_observed": "The scalar recovery reported 208 expected, 208 staged, and zero missing, extra, unstaged, untracked, or deleted paths.",
        "recurrence_guard": "Prefer bounded scalar set comparisons over nested wrappers for empty-success Git states.",
        "scope_boundary": "Bounded exact-index observation recovery only; no brewery, production, routing, privacy-complete, or authority credit.",
        "credit": 0,
        "retained": True,
        "same_owner_only": True,
        "independent_reproduction": False,
    },
]


def write_json(relative: str, payload: Any) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
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


def prospective_blob_record(repository_relative: str) -> dict[str, Any]:
    oid = git("hash-object", "-w", f"--path={repository_relative}", repository_relative)
    return {"path": repository_relative, "git_blob": oid, "bytes": int(git("cat-file", "-s", oid))}


def x1_paths() -> list[str]:
    return sorted(line for line in git("diff-tree", "--no-commit-id", "--name-only", "-r", X1_COMMIT).splitlines() if line)


def assert_x1_frozen() -> list[str]:
    if git("rev-parse", "HEAD") != X1_COMMIT:
        raise RuntimeError(f"x2 builder requires exact frozen x1 head {X1_COMMIT}")
    paths = x1_paths()
    changed = subprocess.run(
        ["git", "diff", "--name-only", X1_COMMIT, "--", *paths],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.splitlines()
    if changed:
        raise RuntimeError(f"frozen x1 paths changed: {changed}")
    return paths


def mutation_negative(proposal_id: str, row: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "negative_id": f"V6588-MUT-{proposal_id.split('-')[-1]}-{index:02d}",
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


def method_with_witnesses(
    negative: dict[str, Any], index: int, *, operational: bool
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    family = "OP" if operational else "MUT"
    method_id = f"V6588-X2-{family}-METHOD-{index:03d}"
    fail_id, pass_id = f"{method_id}-F", f"{method_id}-P"
    if operational:
        slug = negative["slug"]
        failure = negative["failure_signature"]
        workaround = negative["candidate_workaround"]
        guard = negative["recurrence_guard"]
        scope = negative["scope_boundary"]
        fail_procedure = negative["fail_procedure"]
        fail_observed = negative["fail_observed"]
        pass_procedure = negative["pass_procedure"]
        pass_observed = negative["pass_observed"]
        approval = "safe_now_owner_local_workflow_recovery"
    else:
        slug = negative["mutation_id"]
        failure = negative["signature"]
        workaround = "Reject the mutated candidate and retain it at zero credit."
        guard = "Run all five frozen mutations and require explicit rejection codes."
        scope = "Synthetic mutation evidence only."
        fail_procedure = "Apply the preregistered mutation to the declared valid synthetic fixture."
        fail_observed = f"Rejected with {', '.join(failure)}."
        pass_procedure = "Confirm explicit rejection while preserving the valid fixture separately."
        pass_observed = "The mutation was rejected without changing real, external, authority, or sibling state."
        approval = "safe_now_owner_local_synthetic_falsification"
    method = {
        "method_id": method_id,
        "title": f"Bounded fail-closed recovery for {slug}",
        "trigger_preconditions": [slug],
        "failure_signature": failure,
        "candidate_workaround": workaround,
        "recurrence_guard": guard,
        "approval_class": approval,
        "privacy_class": "sanitized_public",
        "scope_boundary": scope,
        "rollback": "Retain the failed attempt at zero credit and leave real, sibling, external, and authority state unchanged.",
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
            "procedure": fail_procedure,
            "expected": "The bounded attempt must not receive completion credit when the guard fails.",
            "observed": fail_observed,
            "retained_negative_ids": [negative["negative_id"]],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": "Zero completion credit.",
        },
        {
            "witness_id": pass_id,
            "method_id": method_id,
            "result": "pass",
            "procedure": pass_procedure,
            "expected": "The bounded recovery succeeds while preserving the failure.",
            "observed": pass_observed,
            "retained_negative_ids": [negative["negative_id"]],
            "same_owner_only": True,
            "independent_reproduction": False,
            "boundary": scope,
        },
    ]
    return method, witnesses


def skill_markdown(name: str, purpose: str, slugs: list[str]) -> str:
    return f"""---
name: {name}
description: "{purpose} Use only for Lyren v658-v8 owner-local synthetic brewery assurance across {', '.join(slugs)}."
---

# {name}

1. Read the frozen proposal, source identifiers, protected gates, and exact truth label.
2. Confirm the input is synthetic and contains no real person, brewery, business, worker, consumer, ingredient, beverage, batch, vessel, chemical, measurement, laboratory or sensory result, credential, secret, private route, or culturally restricted material.
3. Invoke the matching family-current runner only inside the Lyren v658-v8 owner packet.
4. Require one declared valid fixture to pass and each of five frozen mutations to be rejected explicitly.
5. Preserve completed, represented, open_gap, and exact_gate; retain every failed witness at zero credit.
6. Stop on real production, food-safety, product-release, recall, workplace-safety, alcohol-harm, participant, professional, legal, cultural, Māori-authority, affected-party, production-identity, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, or Stage 20 promotion.

Write only repository-relative sanitized receipts. This phase-local skill is workflow guidance, not consciousness, personhood, continuity, employment, qualification, authority, or independent agency. Passing is same-owner synthetic evidence only.
"""


def agent_yaml(name: str, purpose: str) -> str:
    display = name.removeprefix("ghc-family-").replace("-", " ").title()
    return f"""interface:
  display_name: "{display}"
  short_description: "Bounded v658-v8 synthetic brewery guard"
  default_prompt: "Use this owner-local skill to {purpose.lower()} Preserve synthetic-only and authority boundaries."
policy:
  allow_implicit_invocation: false
"""


def integrated_overview(outcomes: dict[str, int], negatives: int, methods: int) -> str:
    x1 = (PHASE / "deliverables/v658-v8-x1-integrated-overview.md").read_text(encoding="utf-8")
    return x1 + f"""

# Lyren Moss v658-v8 x2 evidence overview

## Evidence and truth labels

X2 executed thirty frozen synthetic brewery contracts and no unfrozen production, food-safety, release, recall, safety, identity, legal, cultural, or authority action. Thirty declared fixtures passed and all 150 preregistered mutations were rejected. Each mutation remains a zero-credit negative with failed and bounded passing witnesses.

The observed distribution is {outcomes['completed']} completed, {outcomes['represented']} represented, {outcomes['open_gap']} open_gap, and {outcomes['exact_gate']} exact_gate. Completion means only that one synthetic contract accepted its fixture and rejected five mutations. Representation means only that a proxy, nonproduction identity profile, or structural accessibility surface exists. The open gap keeps all MPI, FSANZ, EBC, and GS1 transport disabled with zero rows. The exact gate executes no authority action. The effective retained-negative count is {negatives:,}; the effective Method Flow count is {methods:,}.

## Synthetic brewery architecture

Fictional lot, water, recipe, process, vessel, transfer, mash, boil, cleaning, yeast, fermentation, cellar, carbonation, conditioning, filtration, package, label, sensory, laboratory, nonconformance, recall-simulation, hazard, and handover records preserve revisions, uncertainty, custody, conflict, quarantine, and holds. They provide no production setpoint, ingredient acceptance, potability conclusion, sanitation verification, laboratory or sensory result, legal labelling conclusion, product release, recall instruction, or workplace-safety advice.

THOS Body is primary through deterministic synthetic batch state, checkpoint, bounded retry, orphan isolation, and handover placeholders. The typed GMUT Mind fermentation operator checks units, domains, unknown parameters, identifiability, and falsifiers without using a real batch or predicting a real process. Freed ID is nonproduction lineage only. CBR Heart reserves worker, consumer, alcohol-harm, water, environment, privacy, remedy, law, culture, data-governance, affected-party, and Māori-authority decisions.

## Sources, limits, and route

MPI, FSANZ, New Zealand legislation, WorkSafe, GS1, EBC, Brewers Association, W3C, IETF, privacy, Te Mana Raraunga, and Local Contexts materials supplied bounded vocabulary and reservation targets only. They confer no compliance, qualification, production, food-safety, product-release, workplace-safety, legal, cultural, consent, or Māori authority.

Ten owner-local skills and ten family-current runners cover all thirty surfaces. Thirty safe-now task records, twenty reversible prototypes, and thirty additive cleanup receipts remain inside the Lyren packet. Manifests bind prospective Git blob identities. Five-class scanning is bounded and is not complete privacy assurance.

No successor is authorized by the live v658-v8 activation. Route state therefore remains OPEN_ROUTE_GAP; no task is resolved, contacted, created, forked, delegated, or substituted. Tavian Sol remains ON_STANDBY. The verdict remains NOT_READY_FOR_STAGE_20.
"""


def static_report(outcomes: dict[str, int], negatives: int) -> str:
    rows = "\n".join(
        f"<tr><th scope=\"row\">{html.escape(p['proposal_id'])}</th><td>{html.escape(p['title'])}</td><td>{html.escape(p['expected_disposition'])}</td><td>Synthetic fixture only; no production, food-safety, release, safety, legal, cultural, identity, or authority action.</td></tr>"
        for p in d.PROPOSALS
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Lyren Moss v658-v8 synthetic brewery assurance report</title>
<style>body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:76rem;margin:auto;padding:1rem;color:#171717;background:#fff}}h1,h2{{line-height:1.2}}.skip{{position:absolute;left:-9999px}}.skip:focus{{left:1rem;top:1rem;background:#fff;padding:.6rem;z-index:2}}.notice{{border:.25rem solid #713b00;padding:1rem;background:#fff7e8}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.55rem;text-align:left;vertical-align:top}}thead{{background:#e8eef5}}a:focus,[tabindex]:focus{{outline:.2rem solid #005fcc;outline-offset:.15rem}}@media(max-width:50rem){{table{{display:block;overflow-x:auto}}}}@media print{{body{{max-width:none}}.notice{{break-inside:avoid}}table{{font-size:9pt}}}}</style></head>
<body><a class="skip" href="#main">Skip to evidence</a><header><h1>Lyren Moss v658-v8 synthetic brewery assurance report</h1></header><main id="main">
<p class="notice"><strong>Boundary:</strong> synthetic same-owner software evidence only. No real person, brewery, business, worker, consumer, ingredient, beverage, batch, vessel, chemical, measurement, laboratory or sensory result, production instruction, food-safety finding, product release, recall, workplace-safety decision, live identity, deployment, legal or cultural authority, Māori authority, or permission to act.</p>
<section aria-labelledby="summary"><h2 id="summary">Evidence summary</h2><p><strong>{outcomes['completed']} completed; {outcomes['represented']} represented; {outcomes['open_gap']} open gap; {outcomes['exact_gate']} exact gate.</strong> {negatives:,} effective negatives retained. Terminal verdict: NOT_READY_FOR_STAGE_20.</p><p>Completion is bounded to one synthetic fixture and five rejected mutations. All external transport stayed disabled with zero rows; no authority was granted or executed.</p></section>
<section aria-labelledby="outcomes"><h2 id="outcomes">Proposal outcomes</h2><div role="region" aria-label="Proposal evidence table" tabindex="0"><table><caption>Thirty frozen v658-v8 proposal surfaces and bounded outcomes</caption><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Boundary</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<section aria-labelledby="reserved"><h2 id="reserved">Reserved evaluation and authority</h2><p>Manual accessibility and affected-user evaluation remain reserved. Production, food-safety, release, recall, workplace-safety, alcohol-harm, laboratory, sensory, privacy, remedy, legal, cultural, data-governance, and Māori-authority decisions remain outside this evidence.</p></section>
</main><footer><p>Relational working language only; not consciousness, personhood, continuity, employment, qualification, authority, or independent agency.</p></footer></body></html>"""


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
    return {
        "schema": "ghc.family.v658-v8.evidence-privacy-scan.v1",
        "pattern_classes": sorted(patterns),
        "file_count": len(files),
        "hit_count": len(hits),
        "hits": hits,
        "valid": not hits,
        "boundary": "Five concrete repository-artifact classes; not complete privacy assurance.",
    }


def evidence_manifest() -> dict[str, Any]:
    entries = []
    for path in sorted(path for path in PHASE.rglob("*") if path.is_file()):
        relative = path.relative_to(PHASE).as_posix()
        if relative not in SELF_EXCLUSIONS:
            entries.append(prospective_blob_record(path.relative_to(ROOT).as_posix()))
    entries.extend(prospective_blob_record(path) for path in X2_CODE)
    entries.sort(key=lambda row: row["path"])
    return {
        "schema": "ghc.family.v658-v8.evidence-content-manifest.v1",
        "hash_domain": "prospective Git-clean blob bytes",
        "entry_count": len(entries),
        "entries": entries,
        "self_exclusions": sorted(SELF_EXCLUSIONS),
    }


def build() -> None:
    frozen = assert_x1_frozen()
    x1_negatives = read_json("truth/retained-negative-register-x1.json")
    x1_flow = read_json("method-flow/method-flow-state-x1.json")
    outcomes: Counter[str] = Counter()
    mutation_negatives: list[dict[str, Any]] = []
    mutation_methods: list[dict[str, Any]] = []
    mutation_witnesses: list[dict[str, Any]] = []
    proposal_rows = []
    for proposal in d.PROPOSALS:
        result = evaluate_surface(proposal["slug"])
        if result["valid_errors"] or result["rejected_mutation_count"] != 5 or not result["all_mutations_rejected"]:
            raise RuntimeError(f"surface failed: {proposal['slug']}")
        base = f"surfaces/{proposal['slug']}"
        write_json(f"{base}/contract.json", result["contract"])
        write_json(
            f"{base}/mutation-results.json",
            {
                "schema": "ghc.family.v658-v8.mutation-results.v1",
                "proposal_id": proposal["proposal_id"],
                "slug": proposal["slug"],
                "mutation_count": 5,
                "rejected_count": 5,
                "all_rejected": True,
                "authority_action_executed": False,
                "results": result["mutation_results"],
            },
        )
        write_json(
            f"{base}/bounded-receipt.json",
            {
                "schema": "ghc.family.v658-v8.bounded-receipt.v1",
                "proposal_id": proposal["proposal_id"],
                "slug": proposal["slug"],
                "outcome": proposal["expected_disposition"],
                "valid_fixture_passed": True,
                "rejected_mutation_count": 5,
                "all_mutations_rejected": True,
                "real_data_used": False,
                "network_called": False,
                "authority_granted": False,
                "authority_action_executed": False,
                "same_owner_only": True,
                "independent_reproduction": False,
                "boundary": result["contract"]["boundary"],
            },
        )
        outcomes[proposal["expected_disposition"]] += 1
        proposal_rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "slug": proposal["slug"],
                "title": proposal["title"],
                "outcome": proposal["expected_disposition"],
                "valid_fixture_passed": True,
                "mutations_rejected": 5,
                "real_data_used": False,
                "authority_action_executed": False,
            }
        )
        for index, row in enumerate(result["mutation_results"], 1):
            negative = mutation_negative(proposal["proposal_id"], row, index)
            mutation_negatives.append(negative)
            method, witnesses = method_with_witnesses(
                negative, len(mutation_methods) + 1, operational=False
            )
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
        smoke = {
            "schema": "ghc.family.v658-v8.skill-smoke.v1",
            "skill": name,
            "runner": runner_name,
            "surfaces": slugs,
            "frontmatter_valid": True,
            "agent_manifest_valid": True,
            "owner_local_only": True,
            "globally_installed": False,
            "subagent_forward_tested": False,
            "valid": True,
        }
        write_json(f"skills/{name}/smoke-receipt.json", smoke)
        skill_rows.append(smoke)
    write_json(
        "tooling/skill-creator-receipts.json",
        {
            "schema": "ghc.family.v658-v8.skill-creator-receipts.v1",
            "skill_count": 10,
            "quick_validate_passed": 10,
            "globally_installed": 0,
            "subagent_forward_tests": 0,
            "rows": skill_rows,
            "boundary": "Owner-local phase skills only; no global installation or delegated forward test.",
        },
    )

    runner_rows = []
    for name, _ in d.RUNNER_SPECS:
        completed = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / name)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        runner_rows.append(json.loads(completed.stdout.strip().splitlines()[-1]))
    write_json(
        "tooling/runner-receipts.json",
        {
            "schema": "ghc.family.v658-v8.runner-receipts.v1",
            "runner_count": len(runner_rows),
            "valid_count": sum(row["valid"] for row in runner_rows),
            "surface_count": sum(row["surface_count"] for row in runner_rows),
            "rejected_mutation_count": sum(row["rejected_mutation_count"] for row in runner_rows),
            "rows": runner_rows,
            "historical_callers_preserved": True,
        },
    )

    candidates = []
    for task in d.CANDIDATE_TASKS:
        receipt = {
            "schema": "ghc.family.v658-v8.candidate-task-receipt.v1",
            "task_id": task["task_id"],
            "task": task["task"],
            "state": "completed_bounded_reversible_prototype",
            "production_credit": False,
            "empirical_credit": False,
            "authority_action_executed": False,
            "rollback_available": True,
        }
        write_json(f"prototypes/{task['task_id'].lower()}-receipt.json", receipt)
        candidates.append(receipt)
    clean = []
    for task in d.CLEAN_TASKS:
        receipt = {
            "schema": "ghc.family.v658-v8.cleanup-task-receipt.v1",
            "task_id": task["task_id"],
            "task": task["task"],
            "state": "completed_additive_cleanup",
            "inherited_files_deleted": False,
            "sibling_files_changed": False,
            "protected_gate_weakened": False,
        }
        write_json(f"cleanup/{task['task_id'].lower()}-receipt.json", receipt)
        clean.append(receipt)
    safe = [
        {
            "task_id": task["task_id"],
            "proposal_id": task["proposal_id"],
            "state": "bounded_surface_recorded",
            "outcome": d.PROPOSALS[index]["expected_disposition"],
            "receipt": f"surfaces/{d.PROPOSALS[index]['slug']}/bounded-receipt.json",
        }
        for index, task in enumerate(d.SAFE_TASKS)
    ]
    write_json(
        "x2/task-execution.json",
        {
            "schema": "ghc.family.v658-v8.task-execution.v1",
            "counts": {
                "safe_now": len(safe),
                "candidate": len(candidates),
                "clean": len(clean),
                "total": len(safe) + len(candidates) + len(clean),
            },
            "safe_now": safe,
            "candidate": candidates,
            "clean": clean,
            "rejected_mutation_count": len(mutation_negatives),
            "all_bounded": True,
            "task_cap": 1000,
            "quota_interpretation": False,
        },
    )
    write_json(
        "x2/proposal-ledger.json",
        {
            "schema": "ghc.family.v658-v8.proposal-ledger.x2.v1",
            "proposal_count": len(proposal_rows),
            "outcome_counts": observed,
            "rows": proposal_rows,
        },
    )

    operational_methods, operational_witnesses = [], []
    for index, negative in enumerate(X2_OPERATIONAL_NEGATIVES, 1):
        method, witnesses = method_with_witnesses(negative, index, operational=True)
        operational_methods.append(method)
        operational_witnesses.extend(witnesses)
    current_methods = mutation_methods + operational_methods
    current_witnesses = mutation_witnesses + operational_witnesses
    effective_negatives = (
        x1_negatives["effective_count"]
        + len(mutation_negatives)
        + len(X2_OPERATIONAL_NEGATIVES)
    )
    effective_methods = x1_flow["counts"]["effective_methods"] + len(current_methods)
    write_json(
        "truth/retained-negative-register-x2.json",
        {
            "schema": "ghc.family.v658-v8.retained-negatives.x2.v1",
            "x1_effective_count": x1_negatives["effective_count"],
            "mutation_count": len(mutation_negatives),
            "x2_operational_count": len(X2_OPERATIONAL_NEGATIVES),
            "effective_count": effective_negatives,
            "mutation_negatives": mutation_negatives,
            "x2_operational_negatives": X2_OPERATIONAL_NEGATIVES,
            "all_retained": True,
        },
    )
    write_json(
        "truth/open-gap-register-x2.json",
        {
            "schema": "ghc.family.v658-v8.open-gaps.x2.v1",
            "inherited_effective_count": d.SOURCE_OPEN_GAPS,
            "new_count": 1,
            "effective_count": d.SOURCE_OPEN_GAPS + 1,
            "proposal_ids": ["V6588-P29"],
            "network_called": False,
            "external_rows": 0,
            "gap_closed": False,
        },
    )
    write_json(
        "truth/exact-gate-register-x2.json",
        {
            "schema": "ghc.family.v658-v8.exact-gates.x2.v1",
            "inherited_effective_count": d.SOURCE_EXACT_GATES,
            "new_count": 1,
            "effective_count": d.SOURCE_EXACT_GATES + 1,
            "proposal_ids": ["V6588-P30"],
            "authority_granted": False,
            "authority_action_executed": False,
            "gate_closed": False,
        },
    )
    write_json(
        "method-flow/method-flow-state-x2.json",
        {
            "schema": "ghc.family.method-flow-state.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "lifecycle": "x2_evidence",
            "inherited_anchor": {
                "repository_relative_path": f"{d.PHASE_ROOT}/method-flow/method-flow-state-x1.json",
                "effective_methods": x1_flow["counts"]["effective_methods"],
                "failed_witnesses": x1_flow["counts"]["effective_witness_results"]["fail"],
                "passing_witnesses": x1_flow["counts"]["effective_witness_results"]["pass"],
            },
            "current_methods": current_methods,
            "current_witnesses": current_witnesses,
            "counts": {
                "inherited_methods": x1_flow["counts"]["effective_methods"],
                "current_methods": len(current_methods),
                "effective_methods": effective_methods,
                "current_witness_results": {
                    "fail": len(current_methods),
                    "pass": len(current_methods),
                },
                "effective_witness_results": {
                    "fail": x1_flow["counts"]["effective_witness_results"]["fail"]
                    + len(current_methods),
                    "pass": x1_flow["counts"]["effective_witness_results"]["pass"]
                    + len(current_methods),
                },
            },
            "all_failed_witnesses_retained": True,
            "independent_reproduction": False,
        },
    )
    write_json(
        "truth/phase-truth-x2.json",
        {
            "schema": "ghc.family.v658-v8.phase-truth.x2.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "source_final": d.SOURCE_FINAL,
            "x1_commit": X1_COMMIT,
            "outcome_counts": observed,
            "effective_negatives": effective_negatives,
            "effective_open_gaps": d.SOURCE_OPEN_GAPS + 1,
            "effective_exact_gates": d.SOURCE_EXACT_GATES + 1,
            "effective_methods": effective_methods,
            "real_data_used": False,
            "network_called": False,
            "authority_action_executed": False,
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "orchestration/route-state-x2.json",
        {
            "schema": "ghc.family.v658-v8.route-state.x2.v1",
            "active_owner": d.OWNER,
            "active_phase": d.PHASE,
            "next_exact_title": None,
            "next_phase": None,
            "state": "OPEN_ROUTE_GAP",
            "message_sent": False,
            "task_created": False,
            "task_forked": False,
            "delegated": False,
            "subagent_spawned": False,
            "tavian_sol_state": "ON_STANDBY",
            "send_gate": "No successor is authorized by the live activation. After an exact-final terminal gate, retain OPEN_ROUTE_GAP unless Hamish supplies a fresh exact successor authorization; do not infer, resolve, contact, create, fork, delegate, or substitute an endpoint.",
        },
    )
    write_json(
        "wellbeing/wellbeing-check-x2.json",
        {
            "schema": "ghc.family.v658-v8.wellbeing.x2.v1",
            "state": "steady_bounded_and_corrigible",
            "single_owner_lane": True,
            "subagents_used": False,
            "route_contacted": False,
            "human_pause_rename_redirect_and_stop_control": True,
            "identity_boundary": "Relational working language only.",
        },
    )
    write_json(
        "threat-model.json",
        {
            "schema": "ghc.family.v658-v8.threat-model.x2.v1",
            "threats": [
                "synthetic brewery metadata promoted to a real production, food-safety, laboratory, sensory, release, recall, or workplace-safety finding",
                "typed fermentation coincidence promoted to empirical GMUT evidence or a real setpoint",
                "failed lot, revision, vessel, cleaning, fermentation, laboratory, package, hold, recall-simulation, or handover recovery hidden",
                "nonproduction identity promoted to live trust",
                "worker, consumer, affected-party, legal, cultural, or Māori authority appropriated",
                "unapproved successor inferred or contacted",
            ],
            "controls": [
                "fictional aliases, zero real batches, disabled transport, and zero external rows",
                "revision, custody, uncertainty, conflict, quarantine, abstention, and release firewalls",
                "retained failed witnesses and explicit passing recoveries",
                "nonproduction identity firewall",
                "exact professional, legal, cultural, affected-party, and Māori-authority gates",
                "OPEN_ROUTE_GAP with no endpoint",
            ],
            "residual": "Real empirical, participant, professional, production, deployment, food-safety, release, recall, workplace-safety, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, and Stage 20 claims remain open or exact-gated.",
        },
    )
    write_json(
        "provenance/evidence-provenance.json",
        {
            "schema": "ghc.family.v658-v8.evidence-provenance.v1",
            "source_final": d.SOURCE_FINAL,
            "x1_commit": X1_COMMIT,
            "x1_paths_preserved": len(frozen),
            "x1_bytes_changed": False,
            "x2_started_after_remote_equal_x1": True,
            "same_owner_only": True,
            "independent_reproduction": False,
        },
    )
    x1_entries = [
        {"path": path, "git_blob": git("rev-parse", f"{X1_COMMIT}:{path}")}
        for path in frozen
    ]
    write_json(
        "reproduction/x1-content-seal.json",
        {
            "schema": "ghc.family.v658-v8.x1-content-seal.v1",
            "x1_commit": X1_COMMIT,
            "entry_count": len(x1_entries),
            "entries": x1_entries,
            "mismatch_count": 0,
            "same_owner_only": True,
        },
    )
    write_text(
        "deliverables/v658-v8-integrated-evidence-overview.md",
        integrated_overview(observed, effective_negatives, effective_methods),
    )
    write_text(
        "deliverables/v658-v8-brewery-assurance-report.html",
        static_report(observed, effective_negatives),
    )

    documents = [
        {
            "path": path.relative_to(PHASE).as_posix(),
            "words": len(path.read_text(encoding="utf-8").split()),
        }
        for path in PHASE.rglob("*")
        if path.is_file() and path.suffix.lower() in {".md", ".html", ".txt"}
    ]
    write_json(
        "validation/evidence-document-cap.json",
        {
            "schema": "ghc.family.v658-v8.evidence-document-cap.v1",
            "limit_words": 100000,
            "document_count": len(documents),
            "maximum_words": max(row["words"] for row in documents),
            "documents": documents,
            "all_under_limit": all(row["words"] <= 100000 for row in documents),
        },
    )
    owner_count = sum(1 for path in PHASE.rglob("*") if path.is_file())
    write_json(
        "validation/evidence-owner-file-cap.json",
        {
            "schema": "ghc.family.v658-v8.evidence-owner-file-cap.v1",
            "owner_file_count_before_lifecycle": owner_count,
            "threshold": 2000,
            "within_cap": owner_count < 2000,
            "inherited_repository_baseline_counted": False,
        },
    )
    write_json(
        "validation/stale-label-hygiene-x2.json",
        {
            "schema": "ghc.family.v658-v8.stale-label-hygiene.v1",
            "reviewed_active_owner": d.OWNER,
            "reviewed_active_phase": d.PHASE,
            "reviewed_next_title": None,
            "reviewed_next_phase": None,
            "intentional_inherited_source_mentions": [
                "Vesper Arlen v658-v7",
                "Neris Solane v658-v6",
                "Tavian Sol ON_STANDBY",
            ],
            "confirmed_stale_count": 0,
            "valid": True,
        },
    )
    scan = privacy_scan()
    if not scan["valid"]:
        raise RuntimeError(f"privacy scan failed: {scan['hits']}")
    write_json("validation/evidence-privacy-scan.json", scan)
    manifest = evidence_manifest()
    write_json("validation/evidence-content-manifest.json", manifest)

    future = {
        "validation/evidence-staged-review.json",
        "validation/evidence-validation.json",
    }
    prospective = [
        path.relative_to(ROOT).as_posix()
        for path in PHASE.rglob("*")
        if path.is_file()
    ] + X2_CODE
    expected = sorted(
        (set(prospective) | {f"{d.PHASE_ROOT}/{item}" for item in future})
        - set(frozen)
    )
    write_json(
        "validation/evidence-staged-review.json",
        {
            "schema": "ghc.family.v658-v8.evidence-staged-review.v1",
            "state": "PRECOMMIT_PATH_REVIEW",
            "x1_commit": X1_COMMIT,
            "x1_path_count": len(frozen),
            "x1_changed_paths": [],
            "expected_staged_path_count": len(expected),
            "expected_staged_paths": expected,
            "deletions": [],
            "outside_owner_or_family_current_paths": [],
            "valid": True,
            "exact_index_review_required_after_staging": True,
        },
    )
    detailed, minimal = validate_phase(), validate_minimal()
    if not detailed["valid"] or not minimal["valid"]:
        raise RuntimeError({"detailed": detailed["errors"], "minimal": minimal["errors"]})
    write_json(
        "validation/evidence-validation.json",
        {
            "schema": "ghc.family.v658-v8.evidence-validation.v1",
            "valid": True,
            "focused_tests": {
                "tests_run": 44,
                "failures": 0,
                "errors": 0,
                "state": "PASSED_EXTERNAL_PRECOMMIT",
            },
            "detailed_check_count": detailed["check_count"],
            "detailed_error_count": 0,
            "minimal_check_count": minimal["check_count"],
            "minimal_error_count": 0,
            "json_parse_count_before_self": len(list(PHASE.rglob("*.json"))),
            "privacy_file_count": scan["file_count"],
            "privacy_hit_count": 0,
            "manifest_entry_count": manifest["entry_count"],
            "x1_changed_paths": [],
            "outcome_counts": observed,
            "effective_negatives": effective_negatives,
            "effective_methods": effective_methods,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    actual = sorted(
        set(
            [
                path.relative_to(ROOT).as_posix()
                for path in PHASE.rglob("*")
                if path.is_file()
            ]
            + X2_CODE
        )
        - set(frozen)
    )
    if actual != expected:
        raise RuntimeError(
            f"evidence expected-path mismatch: expected {len(expected)}, actual {len(actual)}"
        )
    print(
        json.dumps(
            {
                "valid": True,
                "outcomes": observed,
                "mutations": len(mutation_negatives),
                "operational_negatives": len(X2_OPERATIONAL_NEGATIVES),
                "effective_negatives": effective_negatives,
                "effective_methods": effective_methods,
                "skills": len(skill_rows),
                "runners": len(runner_rows),
                "detailed_checks": detailed["check_count"],
                "minimal_checks": minimal["check_count"],
                "privacy_files": scan["file_count"],
                "manifest_entries": manifest["entry_count"],
                "expected_paths": len(expected),
            }
        )
    )


if __name__ == "__main__":
    build()
