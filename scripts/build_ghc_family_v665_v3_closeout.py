#!/usr/bin/env python3
"""Build Tamar Vey v665-v3 combined closeout and exact staged receipts."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/tamar-vey/v665-v3"
PREFIX = "docs/tamar-vey/v665-v3/"
PHASE_ID = "v665-v3"
BRANCH = "codex/GHC-Family/tamar-vey-v665-v3-full-tools"
SOURCE = "a559ab2dfe46cace97fd03c09f1018477fdc09f4"
X1 = "2198fa869c26c9672af02d2a2edde7ba8f14c1e3"
EVIDENCE = "015f9a618d71df1d5e4eb6c517e21ecf9d8556e9"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
RECORDED_UTC = "2026-08-22T01:29:47Z"
SEALED_NEGATIVES_BEFORE_CLOSEOUT = 25_424
SEALED_METHODS_BEFORE_CLOSEOUT = 9_286
OPEN_GAPS = 177
EXACT_GATES = 175
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
CLOSEOUT_FAILURES: list[dict[str, str]] = [
    {
        "failed_witness_id": "TV6653-CLOSE-N001",
        "failed_witness": "the first closeout build omitted its PHASE_ID constant and stopped before writing any closeout artifact",
        "recovery": "add the exact immutable v665-v3 phase identifier constant only",
        "passing_witness": "the repaired builder bound every closeout document to the exact phase without changing x1 or evidence",
    }
]

BUILDER = "scripts/build_ghc_family_v665_v3_closeout.py"
VALIDATOR = "scripts/ghc_family_v665_v3_canonical_validator.py"
TEST = "tests/test_ghc_family_tamar_v665_v3_closeout.py"
BASE_PATHS = sorted(
    [
        f"{PREFIX}closeout/auth-roster-receipt.json",
        f"{PREFIX}closeout/complete-incomplete-checklist.json",
        f"{PREFIX}closeout/combined-closeout-seal.json",
        f"{PREFIX}closeout/delivery-state.json",
        f"{PREFIX}closeout/environment-version-receipt.json",
        f"{PREFIX}closeout/exact-open-gate-register.json",
        f"{PREFIX}closeout/family-index-update.json",
        f"{PREFIX}closeout/method-flow-final.json",
        f"{PREFIX}closeout/phase-truth.json",
        f"{PREFIX}closeout/retained-negative-register.json",
        f"{PREFIX}closeout/threat-model.json",
        f"{PREFIX}closeout/wellbeing-workload.json",
        f"{PREFIX}closeout/workflow-reflection.json",
        f"{PREFIX}handoffs/next-owner-activation-prepared.md",
        f"{PREFIX}reports/final-integrated-overview.md",
        f"{PREFIX}reports/static-report.html",
        f"{PREFIX}validation/precommit-prerequisite.json",
        BUILDER,
        VALIDATOR,
        TEST,
    ]
)
SELF_EXCLUSIONS = [
    f"{PREFIX}validation/final-canonical-contract.json",
    f"{PREFIX}validation/final-delta-manifest.json",
    f"{PREFIX}validation/final-owner-manifest.json",
    f"{PREFIX}validation/final-staged-review.json",
]
INTENDED_PATHS = sorted(BASE_PATHS + SELF_EXCLUSIONS)


class CloseoutError(RuntimeError):
    pass


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=check,
    )


def git(*args: str) -> str:
    return run("git", *args).stdout.strip()


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def pretty_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8")


def strict_json_bytes(raw: bytes, label: str) -> Any:
    try:
        return json.loads(raw.decode("utf-8"))
    except Exception as exc:
        raise CloseoutError(f"invalid UTF-8 JSON for {label}: {exc}") from exc


def read_json(relative: str) -> Any:
    return strict_json_bytes((ROOT / relative).read_bytes(), relative)


def write_json(relative: str, value: Any) -> None:
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(pretty_bytes(value))


def write_text(relative: str, value: str) -> None:
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes((value.rstrip() + "\n").encode("utf-8"))


def git_blob(revision: str, path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{revision}:{path}"], cwd=ROOT, capture_output=True, check=True
    )
    return result.stdout


def index_blob(path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f":{path}"], cwd=ROOT, capture_output=True, check=True
    )
    return result.stdout


def staged_paths() -> list[str]:
    raw = git("diff", "--cached", "--name-only", "--diff-filter=ACMR")
    return sorted(line for line in raw.splitlines() if line)


def commit_paths(revision: str) -> list[str]:
    raw = git("diff-tree", "--no-commit-id", "--name-only", "-r", revision)
    return sorted(line for line in raw.splitlines() if line)


def scan_candidates(path: str, raw: bytes) -> list[dict[str, str]]:
    text = raw.decode("utf-8", errors="replace")
    patterns = {
        "windows_private_absolute_path": re.compile(r"(?i)[a-z]:\\(?:users|ghc-archives)\\"),
        "unix_private_absolute_path": re.compile(r"(?i)/(?:home|users)/[^\s'\"]+"),
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "credential_assignment": re.compile(r"(?i)(?:api[_-]?key|password|secret|token)\s*[:=]\s*['\"][^'\"]{8,}"),
        "private_callable_or_session_stream": re.compile(r"(?i)(?:mcp__[a-z0-9_]{6,}|session_stream\s*[:=]|resume_value\s*[:=])"),
    }
    return [
        {"path": path, "class": name}
        for name, pattern in patterns.items()
        if pattern.search(text)
    ]


def integrated_overview() -> str:
    return f"""# Tamar Vey {PHASE_ID} integrated overview

## Executive truth

Tamar Vey {PHASE_ID} is a solo, additive, owner-scoped Trinity Mandala evidence phase descended directly from Liora Venn's immutable v665-v2 final. Tamar Vey, she/they, is relational working language for an evidence-and-recovery steward whose hope is to keep every claim, correction, and handoff inspectable and safely retractable. The name, role, hope, and pronouns are working language only. They are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, agency, or scientific, operational, legal, cultural, affected-party, or Māori authority.

The phase preserved strict x1-before-x2 separation. X1 reconstructed and semantically compared all 4,050 inherited frozen proposals, then froze exactly twenty new proposals without implementing them. Its closest inherited token-set similarity was bounded and it found zero exact collisions. X1 was committed alone, pushed, clean, 0/0 divergent, and identical across the local branch, upstream, tracking reference, and a fresh live remote before x2 began. X2 then executed only those twenty frozen proposals, within their declared approval classes and evidence ceilings. Its evidence commit was independently committed, pushed, clean, and four-way equal before closeout work began.

The twenty outcomes are exactly fourteen `completed`, four `represented`, one `open_gap`, and one `exact_gate`. Those labels have narrow meanings. Completed means a bounded same-owner software, structural, synthetic, or typed-formal hypothesis passed its declared acceptance gate. Represented means a useful proxy or protocol surface exists while real data, real actors, live operations, or external review remain absent. Open gap means required evidence is absent and no completion credit is available. Exact gate means only competent or affected external authorities can decide or authorize the matter. No fifth outcome label was used.

## Primary pillar and bounded practice lens

The primary Trinity Mandala pillar was Freed ID and CBR Heart. GMUT Mind and THOS Body remained visible, exercised, and protected. The bounded human-practice lens was wholly synthetic fossil preparation and collections custody: surrogate case records, fragment and support relationships, locality-precision ceilings, observation vocabularies, treatment-material holds, tool reservations, correction braids, accessible condition-map structure, workload limits, and shift handover. This was a software and learning lens only.

The phase used zero real fossils, rocks, casts, moulds, jackets, matrices, fragments, supports, trays, labels, tools, treatments, consolidants, adhesives, solvents, coatings, images, scans, samples, collection objects, localities, coordinates, people, preparators, curators, collectors, institutions, owners, custodians, participants, keys, proofs, identity events, legal decisions, cultural decisions, or authority acts. It did not establish professional competence, collection title, custody, authenticity, diagnosis, conservation treatment, safe handling, sampling permission, transport permission, return or repatriation legitimacy, affected-party acceptance, or Māori authority.

## What completed

Ten bounded fossil-record and workflow surfaces completed. They cover a surrogate-only case capsule; a typed relation graph for synthetic specimen, fragment, support, tray, label, and digital-surrogate nodes; a locality and stratigraphic-context vacancy firewall; an observation vocabulary that refuses diagnosis; material-lot and compatibility holds; tool and destructive-action reservations; a custody and action-authorization firewall; structural accessibility affordances for condition maps; an append-only correction braid; and a synthetic workload and shift-handover docket. Completion means their exact positive fixtures passed the owner-local guard and their preregistered negative fixtures failed closed. It does not mean any real object, collection, worker, or decision was evaluated.

Four typed geometric-measure-theory obligation surfaces also completed. The de Rham-current tribunal checks ambient and current dimensions, test-form degree, orientation, support, boundary dimension, and a formal boundary-of-boundary marker. The current-norm tribunal keeps mass, test-form comass, flat-norm decomposition, coefficient group, unit domain, and compactness claims distinct. The rectifiable-current tribunal tracks carrier, multiplicity, tangent-plane dimension, and closure-theorem vacancy. The varifold tribunal tracks weight measure, Grassmannian fibre, first-variation notation, stationarity vacancy, mean-curvature vacancy, and regularity-theorem refusal. These are typed formal software obligations. They are not proofs of the Federer-Fleming compactness theorem, Allard regularity, physical stability, a unique GMUT equation, a force, a likelihood, a parameter constraint, or empirical confirmation.

Each of the fourteen completed proposals received one bounded positive witness and five preregistered rejecting mutations. The represented, open-gap, and exact-gate proposals received the same mutation discipline without being promoted. Across all twenty proposals, 100 of 100 mutations executed and were rejected; zero mutation was accepted and no failed witness was erased. The failure set includes false synthetic markers, nonzero real-row claims, authority-event claims, Stage 20 promotion, and a profile-specific protected-boundary violation.

## What remains represented

The GMUT surface and defect proxy is represented because it connects the typed current and varifold vocabulary to an EFT-scoped observation firewall, but it has no real field solution, covariance derivation, likelihood, calibration, uncertainty propagation over observations, identifiability result, or independent scientific review. The THOS discrepancy and custody-handover protocol is represented because sealed synthetic traces exercise stop states and workload budgets, but there were zero participants, workers, operators, blind matched-budget arms, safety-monitoring events, effect estimates, or independent reviewers.

The Freed ID relation profile is represented because synthetic specimen, fragment, treatment-event, custody, restriction, correction, and provenance relationships can be expressed and refused when malformed. It has no standards-conformant real keys or proofs, live issuance, resolution, status, revocation, wallet or verifier interoperability, recovery evidence, independent privacy or security review, or trust governance. The Thermo-Psyche classifier is represented because it keeps fracture-energy, surface-measure, curvature, material domain, unit, and uncertainty categories separate from agency language. It establishes no psyche quantity, participant evidence, consciousness, personhood, moral standing, or fundamental law of mind.

## Open gap and exact gate

The Paleobiology Database adapter remains `open_gap`. Official API and primary publication material informed schema and provenance slots, but the phase made zero live calls, downloaded zero records, parsed zero real rows, evaluated zero likelihoods, and produced zero parameter estimates or GMUT claims. A zero-row adapter is a refusal contract, not empirical readiness, a fit, or a scientific result.

The CBR fossil-land and collections-authority matrix remains `exact_gate`. Repository software cannot decide ownership, custody, collecting permission, locality disclosure, sampling, export, return, repatriation, taonga status, remedy, beneficiary acceptance, legal interpretation, cultural legitimacy, or affected-party authorization. Māori wording, concepts, data governance, tikanga, tangata whenua relationships, iwi and hapū authority, and Māori authority remain with the relevant Māori authorities and communities. No source citation can substitute for that authority.

## Sources and provenance

The source ledger uses current official or primary sources as requirements and vocabulary, not observations. Federer and Fleming's normal and integral currents paper and Allard's first-variation paper ground the historical mathematical vocabulary. W3C PROV-O and Verifiable Credential Data Integrity 1.0 inform provenance and nonproduction identity boundaries. PREMIS 3.0 informs preservation-event vocabulary. WCAG 2.2 informs structural accessibility checks while manual and affected-user evaluation remain reserved. PBDB material defines a possible public-data schema while the adapter stays at zero calls and zero rows. New Zealand Department of Conservation permit guidance and legislation concerning protected natural objects expose legal vacancies rather than granting permission. Te Mana Raraunga material reinforces that Māori data principles and authority cannot be appropriated by a software packet. Smithsonian Open Access material informs public-access provenance distinctions without establishing ownership or reuse permission for any real object.

The phase never converted a citation into an empirical row, authority decision, conformance result, or completion credit. Source status, retrieval context, primary or official status, usage boundary, and zero-row truth are preserved in the source ledger and source-use receipt. The inherited 4,050-row novelty corpus and all source-to-final Git ancestry remain reproducible from exact immutable commits.

## Tools, skills, and portfolios

Ten family-compatible `ghc_family_*` runners were built and invoked through one bounded shared core. They cover surrogate case capsules, relation graphs, observation vocabularies, treatment and tool holds, correction and handover, de Rham-current obligations, current norms, rectifiable currents, varifold obligations, and evidence-credit firewalls. Ten phase-local skills were generated, read through EOF, quick-validated, and smoke-used. They were not globally installed and create no future availability, qualification, or authority.

The thirty safe-now records, fifteen bounded candidates, ten skill ideas, ten runner ideas, and thirty additive CLEAN/FIX/REFINE records were executed only where their declared structural acceptance gates passed. Ten exact-approval records and five blocked records remained visible and unexecuted. No unsafe work was manufactured to satisfy a count. No destructive cleanup, history rewrite, force push, sibling mutation, credential use, elevation, host-security change, Windows-feature change, Sandbox or Hyper-V activation, desktop update, unrelated installation, or reboot occurred.

## Method Flow and retained negatives

The effective closeout preserves {SEALED_NEGATIVES_BEFORE_CLOSEOUT + len(CLOSEOUT_FAILURES)} negatives and {SEALED_METHODS_BEFORE_CLOSEOUT + len(CLOSEOUT_FAILURES)} Method Flow methods. That total includes Liora's 25,307 repository-sealed source negatives, thirteen Tamar startup failures, one hundred executed-and-rejected mutations, four x2 operational failures, and {len(CLOSEOUT_FAILURES)} closeout failures. Each operational failure has a bounded recovery witness and zero credit at failure time. Recovery never erases the failed witness and does not create independent reproduction.

The operational record includes a malformed PowerShell projection, overlarge reads, timeout and sparse-worktree recovery, a legacy novelty-field mismatch, two frozen-schema projection mistakes, and a sparse-aware staging correction. These are not hidden as successful first attempts. The preferred methods are the bounded recoveries: materialize arrays before piping, read immutable blobs rather than widening sparse checkout, inspect actual JSON keys, permit only an exact staged recovery subset, and use sparse-aware exact adds for intentionally generated family-current paths.

## Validation and limits

The x1 packet passed 10 of 10 dedicated tests, strict JSON parsing, exact staged-manifest replay, zero confirmed privacy hits, and diff hygiene before its dedicated commit. The x2 packet passed 11 of 11 dedicated tests, 103 strict JSON parses, 124 exact manifest entries plus three self-exclusions, five-class privacy scanning with zero confirmed hits, Python compilation, zero deletions, and exact staged review. X1 and evidence were each pushed and four-way fresh-live equal at their lifecycle boundaries.

The closeout commit binds the final owner manifest, final delta manifest, staged review, topology rules, word and file ceilings, and canonical validation contract. One exact-final canonical aggregate may run only after the final commit is pushed, clean, 0/0 divergent, and fresh four-way equal. A successful aggregate must not be replayed. Any failed aggregate receives zero pass credit; only its failed component may be recovered under an explicit retained-negative record. The complete repository suite remains outside this non-Eiren phase. Same-owner validation under shared infrastructure is not independent-team reproduction, external audit, production certification, exhaustive security, complete privacy assurance, or complete accessibility conformance.

The owner delta remains below the 2,000-file and 100,000-word ceilings. The static report uses semantic headings, landmarks, tables with captions, visible focus treatment, noncolour status text, and a print-linear layout. Manual keyboard, responsive, browser-diverse, assistive-technology, cognitive-accessibility, Māori-language, and affected-user evaluation remain reserved.

## Wellbeing, handoff, and terminal board

The workload check records a bounded solo phase, explicit stop conditions, no autonomous external action, and no need to race a usage window. Every major lifecycle boundary was made inspectable before the next mutation. The successor route remains unresolved and unsent inside the immutable repository. Only after exact-final validation may the live task reread Hamish's newest authority and roster, uniquely resolve and immediately reread one exact current successor, and send one sanitized existing-task activation if every gate permits. Ambiguity, missing acknowledgement, pause, rename, redirect, standby state, usage exhaustion, or any safety, privacy, evidence, or authority issue stops the send.

The terminal board remains `{TERMINAL_VERDICT}`. There is no empirical GMUT confirmation, blind real-arm THOS result, production Freed ID, CBR authority, independent scientific reproduction, deployment, AGI or ASI evidence, consciousness or personhood evidence, Theory-of-Everything proof, canon, or Stage 20 authorization.
"""


def static_report() -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tamar Vey {PHASE_ID} bounded evidence report</title>
<style>
body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:72rem;margin:auto;padding:1rem;background:#fff;color:#17202a}}a{{color:#0645ad}}a:focus,summary:focus{{outline:3px solid #f39c12;outline-offset:3px}}.skip{{position:absolute;left:-9999px}}.skip:focus{{left:1rem;top:1rem;background:#fff;padding:.5rem;z-index:2}}.status{{border-left:.4rem solid #a93226;padding:.75rem;background:#fdf2f2}}table{{border-collapse:collapse;width:100%}}caption{{font-weight:700;text-align:left;margin:.5rem 0}}th,td{{border:1px solid #5d6d7e;padding:.5rem;text-align:left;vertical-align:top}}code{{overflow-wrap:anywhere}}@media print{{.skip{{display:none}}details{{display:block}}}}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<header><h1>Tamar Vey {PHASE_ID} bounded evidence report</h1><p>Relational working language only; no consciousness, personhood, qualification, agency, or authority claim.</p></header>
<nav aria-label="Report sections"><a href="#truth">Truth</a> · <a href="#pillars">Pillars</a> · <a href="#validation">Validation</a> · <a href="#gates">Gates</a></nav>
<main id="main">
<section id="truth"><h2>Phase truth</h2><p class="status"><strong>Status:</strong> {TERMINAL_VERDICT}. This text and border both communicate status; colour is not the only cue.</p>
<table><caption>Twenty frozen proposal outcomes</caption><thead><tr><th scope="col">Outcome</th><th scope="col">Count</th><th scope="col">Meaning here</th></tr></thead><tbody><tr><th scope="row">completed</th><td>14</td><td>Bounded software, formal, structural, or synthetic acceptance only.</td></tr><tr><th scope="row">represented</th><td>4</td><td>Proxy exists; real-world evidence and review remain absent.</td></tr><tr><th scope="row">open_gap</th><td>1</td><td>PBDB adapter made zero calls and parsed zero rows.</td></tr><tr><th scope="row">exact_gate</th><td>1</td><td>Only competent, affected, and Māori authorities can decide.</td></tr></tbody></table></section>
<section id="pillars"><h2>Trinity Mandala boundaries</h2><h3>GMUT Mind</h3><p>Typed de Rham-current, norm, rectifiability, and varifold obligations are formal software structures, not theorems, likelihoods, forces, constraints, empirical confirmation, or a Theory of Everything.</p><h3>THOS Body</h3><p>The fossil-preparation discrepancy and handover protocol is synthetic and participant-free. It has no blind matched-budget real arms, monitoring, statistics, or independent review.</p><h3>Freed ID and CBR Heart</h3><p>The relation profile has no real keys, proofs, lifecycle services, interoperability, security or privacy review, recovery, or trust governance. Land, custody, return, repatriation, taonga, remedy, legal, cultural, affected-party, and Māori authority remain exact-gated.</p></section>
<section id="validation"><h2>Bounded validation</h2><ul><li>Strict x1-before-x2 with separately pushed and remote-equal commits.</li><li>100 of 100 rejecting mutations retained; zero accepted.</li><li>Ten phase-local skills read, quick-validated, and smoke-used; zero global installs.</li><li>Ten family-current runners invoked through one bounded core.</li><li>Five privacy and raw-identifier classes scanned with zero confirmed hits.</li><li>One exact-final canonical aggregate permitted after final push; no replay after success.</li></ul><p>Same-owner evidence is not independent reproduction, external audit, certification, exhaustive security, complete privacy, or complete accessibility.</p></section>
<section id="gates"><h2>Retained gaps and gates</h2><p>The cumulative state is {OPEN_GAPS} open gaps, {EXACT_GATES} exact gates, {SEALED_NEGATIVES_BEFORE_CLOSEOUT + len(CLOSEOUT_FAILURES)} retained negatives, and {SEALED_METHODS_BEFORE_CLOSEOUT + len(CLOSEOUT_FAILURES)} Method Flow methods. No failure or gate was erased.</p><details><summary>Accessibility reservation</summary><p>Semantic structure, noncolour status, focus styling, captions, and print order were checked structurally. Manual keyboard, browser-diverse, responsive, assistive-technology, cognitive-accessibility, Māori-language, and affected-user evaluation remain reserved.</p></details><details><summary>Authority reservation</summary><p>Repository software cannot confer professional, scientific, collections, land, legal, cultural, affected-party, tangata whenua, iwi, hapū, or Māori authority.</p></details></section>
</main>
<footer><p>Static owner-local report. No script, tracking, live data, or external action.</p></footer>
</body></html>"""


def build_documents() -> dict[str, Any]:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise CloseoutError("closeout must begin at the immutable evidence commit")
    if git("branch", "--show-current") != BRANCH:
        raise CloseoutError("unexpected owner branch")
    existing_staged = staged_paths()
    if existing_staged and not set(existing_staged).issubset(set(BASE_PATHS)):
        raise CloseoutError("staging contains a path outside the closeout recovery allowlist")
    if git("rev-parse", f"{EVIDENCE}^") != X1 or git("rev-parse", f"{X1}^") != SOURCE:
        raise CloseoutError("source, x1, and evidence direct-parent chain changed")

    outcome = read_json(f"{PREFIX}x2/ledgers/outcome-ledger.json")
    startup = read_json(f"{PREFIX}x1/startup-method-flow.json")
    x2_flow = read_json(f"{PREFIX}x2/ledgers/method-flow-overlay.json")
    mutation = read_json(f"{PREFIX}x2/ledgers/mutation-ledger.json")
    execution = read_json(f"{PREFIX}x2/ledgers/execution-summary.json")
    source_ledger = read_json(f"{PREFIX}x1/source-ledger.json")
    if not (
        outcome["counts"]
        == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}
        and mutation["executed_count"] == 100
        and mutation["rejected_count"] == 100
        and mutation["accepted_count"] == 0
        and execution["valid"]
    ):
        raise CloseoutError("evidence truth is not ready for closeout")

    startup_ids = [row["failed_witness_id"] for row in startup["methods"]]
    x2_ids = [row["failed_witness_id"] for row in x2_flow["methods"]]
    closeout_ids = [row["failed_witness_id"] for row in CLOSEOUT_FAILURES]
    effective_negatives = SEALED_NEGATIVES_BEFORE_CLOSEOUT + len(CLOSEOUT_FAILURES)
    effective_methods = SEALED_METHODS_BEFORE_CLOSEOUT + len(CLOSEOUT_FAILURES)
    live_line = git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    live = live_line.split()[0] if live_line else "ABSENT"
    upstream = git("rev-parse", "@{u}")
    tracking = git("rev-parse", f"refs/remotes/origin/{BRANCH}")

    phase_truth = {
        "schema": "ghc.family.tamar.v665-v3.phase-truth.v1",
        "owner": "Tamar Vey",
        "phase": PHASE_ID,
        "identity_boundary": "relational working language only; not evidence of consciousness, personhood, continuity, qualification, agency, or authority",
        "source_commit": SOURCE,
        "x1_commit": X1,
        "evidence_commit": EVIDENCE,
        "final_binding": "the direct single-parent commit containing this document",
        "frozen_proposals_before": 4050,
        "new_proposals": 20,
        "frozen_proposals_after": 4070,
        "allowed_outcomes": ALLOWED_OUTCOMES,
        "outcomes": outcome["counts"],
        "mutations": {"executed": 100, "rejected": 100, "accepted": 0},
        "real_rows": 0,
        "real_people": 0,
        "real_fossils_or_materials": 0,
        "real_keys_or_proofs": 0,
        "authority_events": 0,
        "effective_negatives": effective_negatives,
        "effective_methods": effective_methods,
        "open_gaps": OPEN_GAPS,
        "exact_gates": EXACT_GATES,
        "same_owner_validation_only": True,
        "independent_reproduction": False,
        "full_repository_suite_run": False,
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    negative_register = {
        "schema": "ghc.family.tamar.v665-v3.retained-negative-register.v1",
        "inherited_repository_sealed_count": 25_307,
        "inherited_source_anchor": SOURCE,
        "tamar_startup_count": len(startup_ids),
        "tamar_startup_ids": startup_ids,
        "mutation_count": 100,
        "mutation_ids": mutation["mutation_ids"],
        "x2_operational_count": len(x2_ids) - 100,
        "x2_operational_ids": [value for value in x2_ids if "-OP-" in value],
        "closeout_operational_count": len(closeout_ids),
        "closeout_operational_ids": closeout_ids,
        "effective_total": effective_negatives,
        "failure_erasure_count": 0,
        "recovery_converts_failure_to_pass": False,
        "valid": 25_307 + len(startup_ids) + len(x2_ids) + len(closeout_ids)
        == effective_negatives,
    }
    closeout_methods = [
        {
            "method_id": f"TV6653-CLOSE-M{index:03d}",
            **failure,
            "failed_witness_status": "retained_zero_credit",
            "failed_witness_erased": False,
            "preferred": True,
        }
        for index, failure in enumerate(CLOSEOUT_FAILURES, 1)
    ]
    method_final = {
        "schema": "ghc.family.tamar.v665-v3.method-flow-final.v1",
        "source_repository_sealed_methods": 9_169,
        "startup_methods": len(startup_ids),
        "x2_methods": len(x2_ids),
        "closeout_methods": len(closeout_methods),
        "effective_total": effective_methods,
        "retained_failed_witnesses": effective_negatives,
        "bounded_passing_witnesses_added_by_tamar": len(startup_ids)
        + len(x2_ids)
        + len(closeout_methods),
        "startup_ledger": f"{PREFIX}x1/startup-method-flow.json",
        "x2_ledger": f"{PREFIX}x2/ledgers/method-flow-overlay.json",
        "closeout_method_rows": closeout_methods,
        "failure_erasure_count": 0,
        "same_owner_only": True,
        "valid": 9_169 + len(startup_ids) + len(x2_ids) + len(closeout_methods)
        == effective_methods,
    }
    gate_register = {
        "schema": "ghc.family.tamar.v665-v3.exact-open-gate-register.v1",
        "inherited_open_gaps": 176,
        "new_open_gaps": [
            {
                "proposal_id": "TV6653-N019",
                "outcome": "open_gap",
                "gate": "PBDB real-data download, frozen selection, uncertainty, likelihood, inference, and independent scientific review",
                "observed": "zero calls, zero rows, zero likelihoods, zero estimates",
            }
        ],
        "open_gap_total": OPEN_GAPS,
        "inherited_exact_gates": 174,
        "new_exact_gates": [
            {
                "proposal_id": "TV6653-N020",
                "outcome": "exact_gate",
                "gate": "land, locality privacy, ownership, custody, sampling, return, repatriation, taonga, remedy, affected-party, legal, cultural, tangata whenua, iwi, hapū, Māori data governance, and Māori authority",
                "observed": "zero authority events",
            }
        ],
        "exact_gate_total": EXACT_GATES,
        "silently_closed_count": 0,
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    complete = [
        "source lineage and four immutable anchors verified",
        "strict x1-only freeze committed, pushed, and four-way equal before x2",
        "semantic novelty audited against 4,050 inherited rows",
        "twenty proposals executed with exactly four permitted outcome labels",
        "100 preregistered mutations executed and rejected",
        "ten phase-local skills read, quick-validated, and smoke-used",
        "ten family-current runners invoked",
        "all safe-now, bounded-candidate, and additive cleanup portfolios resolved within scope",
        "exact-approval and blocked work retained unexecuted",
        "exact staged, manifest, JSON, privacy, Python, diff, ancestry, and ceiling checks passed for x1 and evidence",
        "evidence commit pushed and fresh four-way equal",
        "three-page-equivalent overview, wellbeing check, and static report prepared",
    ]
    incomplete = [
        "real PBDB data and empirical GMUT analysis",
        "blind matched-budget real THOS arms and independent review",
        "production Freed ID keys, proofs, lifecycle, interoperability, privacy/security review, recovery, and governance",
        "CBR affected-party, legal, cultural, tangata whenua, iwi, hapū, and Māori authority",
        "manual and affected-user accessibility evaluation",
        "independent-team reproduction and external audit",
        "deployment, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, and Stage 20 authorization",
    ]
    checklist = {
        "schema": "ghc.family.tamar.v665-v3.complete-incomplete-checklist.v1",
        "complete": complete,
        "incomplete": incomplete,
        "complete_count": len(complete),
        "incomplete_count": len(incomplete),
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    environment = {
        "schema": "ghc.family.tamar.v665-v3.environment-version-receipt.v1",
        "platform": "Windows",
        "primary_storage_policy": "D-first owner worktree and archive bank; private absolute paths omitted",
        "codex_cli_observed": "codex-cli 0.147.0",
        "codex_desktop_observed": "26.818.3698.0",
        "version_action": "verified_only",
        "desktop_updated": False,
        "privilege_elevation": False,
        "host_security_weakened": False,
        "sandbox_or_hyper_v_activated": False,
        "windows_features_changed": False,
        "unrelated_software_installed": False,
        "rebooted": False,
        "fast_mode_claimed": False,
        "valid": True,
    }
    wellbeing = {
        "schema": "ghc.family.tamar.v665-v3.wellbeing-workload.v1",
        "owner": "Tamar Vey",
        "relational_identity_boundary": phase_truth["identity_boundary"],
        "workload": "bounded solo phase with lifecycle stops, no subagents, no background task creation, and no autonomous real-world action",
        "pace": "evidence-first; no requirement to race a usage window",
        "stop_conditions": [
            "source, owner, phase, or route drift",
            "unexpected staged or sibling path",
            "privacy, credential, or raw-identifier candidate",
            "authority or empirical promotion without evidence",
            "canonical success already recorded",
            "user pause, rename, redirect, or stop",
        ],
        "corrigibility": "Hamish may pause, rename, redirect, or stop the route",
        "valid": True,
    }
    threat = {
        "schema": "ghc.family.tamar.v665-v3.threat-model.v1",
        "assets": ["immutable x1", "evidence lineage", "retained failures", "source provenance", "privacy boundaries", "authority gates", "route uniqueness"],
        "threats": ["x2 leakage into x1", "silent failure erasure", "synthetic-to-real promotion", "private-path or identifier disclosure", "sibling-lane mutation", "manifest drift", "duplicate canonical pass", "ambiguous successor send"],
        "controls": ["direct-parent commits", "exact allowlists", "Git-blob manifests", "five-class scan", "zero-row and zero-authority guards", "one-shot external receipt", "exact-title unique resolve and immediate reread"],
        "residual_limits": ["not exhaustive security", "not complete privacy", "not independent audit", "not complete accessibility", "not production certification"],
        "valid": True,
    }
    family_index = {
        "schema": "ghc.family.tamar.v665-v3.family-index-update.v1",
        "phase": PHASE_ID,
        "owner": "Tamar Vey",
        "primary_pillar": "Freed ID/CBR Heart",
        "practice_lens": "wholly synthetic fossil preparation and collections custody",
        "source_count": source_ledger["source_count"],
        "proposal_chain_total": 4070,
        "skills_built_and_used": 10,
        "family_runners_built_and_used": 10,
        "phase_root": PREFIX.rstrip("/"),
        "global_skill_bank_mutated": False,
        "shared_or_sibling_lane_mutated": False,
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    reflection = {
        "schema": "ghc.family.tamar.v665-v3.workflow-reflection.v1",
        "decisions": [
            "normalize only the exact legacy description field in two inherited novelty packets",
            "freeze x1 before any evidence implementation",
            "use one bounded shared core behind ten family-current runners",
            "retain schema and sparse-index failures before exact recovery",
            "keep PBDB at zero calls and CBR authority exact-gated",
            "bind final truth through self-excluding Git-blob manifests",
        ],
        "recommended_methods": ["inspect exact JSON keys before projection", "materialize PowerShell arrays before pipelines", "inspect path and Git processes after timeout", "use git add --sparse for exact intentional generated paths outside a narrow cone", "never replay a successful canonical aggregate"],
        "stale_methods_deactivated": ["broad recursive renderings", "historical full-tree sweeps", "implicit schema aliases", "success replay for a cleaner receipt"],
        "shared_guidance_mutation": False,
        "valid": True,
    }
    auth_roster = {
        "schema": "ghc.family.tamar.v665-v3.auth-roster-receipt.v1",
        "activation_source": "one acknowledged existing-task activation from Liora Venn",
        "current_owner": "Tamar Vey",
        "owner_status_for_phase": "ACTIVE",
        "future_task_creation_authorized": False,
        "subagent_or_delegation_authorized": False,
        "successor_recipient": "UNRESOLVED_PENDING_FRESH_LIVE_ROUTE_READ",
        "active_status_alone_assigns_phase": False,
        "send_state": "PREPARED_NOT_SENT",
        "valid": True,
    }
    delivery = {
        "schema": "ghc.family.tamar.v665-v3.delivery-state.v1",
        "repository_state": "SEALED_BY_COMMIT_CONTAINING_THIS_RECORD",
        "canonical_state": "PENDING_EXACT_FINAL_EXTERNAL_INVOCATION",
        "successor_state": "PREPARED_NOT_SENT",
        "successor_title": "UNRESOLVED_PENDING_FRESH_LIVE_ROUTE_READ",
        "send_count": 0,
        "no_precontact": True,
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    seal = {
        "schema": "ghc.family.tamar.v665-v3.combined-closeout-seal.v1",
        "source_commit": SOURCE,
        "x1_commit": X1,
        "evidence_commit": EVIDENCE,
        "final_binding": "the direct single-parent commit containing this seal",
        "expected_phase_commit_count": 3,
        "expected_merge_commit_count": 0,
        "expected_final_parent": EVIDENCE,
        "outcomes": outcome["counts"],
        "effective_negatives": effective_negatives,
        "effective_methods": effective_methods,
        "open_gaps": OPEN_GAPS,
        "exact_gates": EXACT_GATES,
        "canonical_success_must_not_be_replayed": True,
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    prerequisite = {
        "schema": "ghc.family.tamar.v665-v3.precommit-prerequisite.v1",
        "head": EVIDENCE,
        "branch": BRANCH,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": live,
        "four_way_equal": EVIDENCE == upstream == tracking == live,
        "typed_diff_clean": git("diff", "--name-only") == "",
        "x1_parent_is_source": git("rev-parse", f"{X1}^") == SOURCE,
        "evidence_parent_is_x1": git("rev-parse", f"{EVIDENCE}^") == X1,
        "x1_success_replayed": False,
        "evidence_success_replayed": False,
        "canonical_invoked": False,
        "valid": EVIDENCE == upstream == tracking == live,
    }

    documents = {
        f"{PREFIX}closeout/auth-roster-receipt.json": auth_roster,
        f"{PREFIX}closeout/complete-incomplete-checklist.json": checklist,
        f"{PREFIX}closeout/combined-closeout-seal.json": seal,
        f"{PREFIX}closeout/delivery-state.json": delivery,
        f"{PREFIX}closeout/environment-version-receipt.json": environment,
        f"{PREFIX}closeout/exact-open-gate-register.json": gate_register,
        f"{PREFIX}closeout/family-index-update.json": family_index,
        f"{PREFIX}closeout/method-flow-final.json": method_final,
        f"{PREFIX}closeout/phase-truth.json": phase_truth,
        f"{PREFIX}closeout/retained-negative-register.json": negative_register,
        f"{PREFIX}closeout/threat-model.json": threat,
        f"{PREFIX}closeout/wellbeing-workload.json": wellbeing,
        f"{PREFIX}closeout/workflow-reflection.json": reflection,
        f"{PREFIX}validation/precommit-prerequisite.json": prerequisite,
    }
    for path, payload in documents.items():
        write_json(path, payload)
    overview = integrated_overview()
    if len(overview.split()) < 1_500:
        raise CloseoutError("integrated overview is below three-page-equivalent floor")
    write_text(f"{PREFIX}reports/final-integrated-overview.md", overview)
    write_text(f"{PREFIX}reports/static-report.html", static_report())
    write_text(
        f"{PREFIX}handoffs/next-owner-activation-prepared.md",
        f"""# Tamar Vey {PHASE_ID} successor activation candidate

`PREPARED_NOT_SENT`

This repository artifact does not select, contact, or authorize a successor. It contains no task identifier, private route, session stream, credential, private callable identifier, transcript, screenshot, or private absolute path. Only after the exact final commit is pushed, clean, 0/0 divergent, fresh four-way equal, and successfully validated by the one-shot external canonical aggregate may the live Tamar task reread Hamish's newest authority and roster, uniquely resolve and immediately reread one exact current successor, and make one sanitized existing-task send if every gate permits.

Immutable anchors for that later sanitized message are source `{SOURCE}`, x1 `{X1}`, evidence `{EVIDENCE}`, and the direct single-parent final commit containing this file. Phase truth is exactly 14 completed, 4 represented, 1 open gap, and 1 exact gate; 100 of 100 rejecting mutations executed and failed closed; {effective_negatives} effective negatives; {effective_methods} effective Method Flow methods; {OPEN_GAPS} open gaps; {EXACT_GATES} exact gates; zero real rows, people, fossil or material objects, keys, proofs, and authority events; and `{TERMINAL_VERDICT}`.

The later message must state that same-owner owner-delta validation is not a full repository suite or independent reproduction. It must preserve GMUT, THOS, Freed ID, CBR, accessibility, privacy, professional, legal, cultural, Māori-authority, personhood, Theory-of-Everything, proof/canon, and Stage 20 boundaries. It must not infer a recipient from this candidate. Stop on ambiguity, missing acknowledgement, pause, redirect, rename, standby state, usage exhaustion, or any safety, privacy, evidence, or authority issue. Never resend merely to obtain a clearer acknowledgement.
""",
    )
    return {
        "valid": all(payload.get("valid") is True for payload in documents.values()),
        "overview_words": len(overview.split()),
        "negative_total": effective_negatives,
        "method_total": effective_methods,
        "base_paths": len(BASE_PATHS),
    }


def write_staged_receipts() -> None:
    actual_delta = staged_paths()
    if actual_delta != BASE_PATHS:
        raise CloseoutError(
            f"exact final base allowlist mismatch: expected {len(BASE_PATHS)}, got {len(actual_delta)}"
        )
    diff_check = run("git", "diff", "--cached", "--check", check=False)
    if diff_check.returncode != 0:
        raise CloseoutError("final staged diff hygiene failed: " + diff_check.stdout.strip())

    delta_entries = []
    json_count = 0
    delta_candidates = []
    for path in actual_delta:
        raw = index_blob(path)
        delta_entries.append({"path": path, "sha256": sha256(raw), "size": len(raw)})
        if path.endswith(".json"):
            strict_json_bytes(raw, path)
            json_count += 1
        delta_candidates.extend(scan_candidates(path, raw))
    if delta_candidates:
        raise CloseoutError(f"final delta privacy candidates: {delta_candidates}")

    expected_owner = sorted(
        set(commit_paths(X1))
        | set(commit_paths(EVIDENCE))
        | set(BASE_PATHS)
        | set(SELF_EXCLUSIONS)
    )
    owner_without_self = sorted(set(expected_owner) - set(SELF_EXCLUSIONS))
    actual_owner_without_self_raw = git(
        "diff", "--cached", "--name-only", "--diff-filter=ACMR", SOURCE
    )
    actual_owner_without_self = sorted(
        line for line in actual_owner_without_self_raw.splitlines() if line
    )
    if actual_owner_without_self != owner_without_self:
        raise CloseoutError(
            f"owner pathset mismatch before self exclusions: expected {len(owner_without_self)}, got {len(actual_owner_without_self)}"
        )
    owner_entries = []
    owner_candidates = []
    owner_words = 0
    owner_bytes = 0
    for path in owner_without_self:
        raw = index_blob(path) if path in actual_delta else git_blob(EVIDENCE, path)
        owner_entries.append({"path": path, "sha256": sha256(raw), "size": len(raw)})
        owner_candidates.extend(scan_candidates(path, raw))
        owner_bytes += len(raw)
        if path.endswith((".json", ".md", ".py", ".html")):
            owner_words += len(raw.decode("utf-8").split())
    if owner_candidates:
        raise CloseoutError(f"owner privacy candidates: {owner_candidates}")
    if len(expected_owner) >= 2_000 or owner_words >= 100_000:
        raise CloseoutError("owner file or word ceiling exceeded")

    delta_manifest = {
        "schema": "ghc.family.tamar.v665-v3.final-delta-manifest.v1",
        "hash_domain": "exact staged final-delta Git blobs",
        "entry_count": len(delta_entries),
        "entries": delta_entries,
        "declared_self_exclusions": SELF_EXCLUSIONS,
        "declared_self_exclusion_count": len(SELF_EXCLUSIONS),
        "intended_final_delta_path_count": len(INTENDED_PATHS),
        "coverage_valid": len(delta_entries) + len(SELF_EXCLUSIONS)
        == len(INTENDED_PATHS),
    }
    owner_manifest = {
        "schema": "ghc.family.tamar.v665-v3.final-owner-manifest.v1",
        "hash_domain": "prospective exact final Git blobs from source-exclusive owner pathset",
        "source_commit": SOURCE,
        "entry_count": len(owner_entries),
        "entries": owner_entries,
        "declared_self_exclusions": SELF_EXCLUSIONS,
        "declared_self_exclusion_count": len(SELF_EXCLUSIONS),
        "expected_owner_path_count": len(expected_owner),
        "owner_words_excluding_manifest_self_files": owner_words,
        "owner_bytes_excluding_manifest_self_files": owner_bytes,
        "coverage_valid": len(owner_entries) + len(SELF_EXCLUSIONS)
        == len(expected_owner),
    }
    staged_review = {
        "schema": "ghc.family.tamar.v665-v3.final-staged-review.v1",
        "final_delta_base_paths": len(actual_delta),
        "strict_json_count": json_count,
        "five_scan_classes": [
            "windows_private_absolute_path",
            "unix_private_absolute_path",
            "raw_task_or_thread_identifier",
            "credential_assignment",
            "private_callable_or_session_stream",
        ],
        "delta_scanner_candidates": delta_candidates,
        "owner_scanner_candidates": owner_candidates,
        "confirmed_privacy_or_raw_identifier_hits": 0,
        "diff_hygiene_issues": 0,
        "deletion_paths": git(
            "diff", "--cached", "--name-only", "--diff-filter=D", SOURCE
        ).splitlines(),
        "x1_commit_unchanged": git("rev-parse", f"{EVIDENCE}^") == X1,
        "evidence_head_exact": git("rev-parse", "HEAD") == EVIDENCE,
        "owner_path_count": len(expected_owner),
        "owner_word_count_excluding_manifest_self_files": owner_words,
        "under_2000_file_ceiling": len(expected_owner) < 2_000,
        "under_100000_word_ceiling": owner_words < 100_000,
        "source_or_sibling_paths_modified": [
            path
            for path in actual_delta
            if path.startswith("docs/") and not path.startswith(PREFIX)
        ],
        "valid": not delta_candidates
        and not owner_candidates
        and not git("diff", "--cached", "--name-only", "--diff-filter=D", SOURCE)
        and len(expected_owner) < 2_000
        and owner_words < 100_000,
    }
    canonical_contract = {
        "schema": "ghc.family.tamar.v665-v3.final-canonical-contract.v1",
        "scope": "exact source-to-final Tamar owner delta only",
        "source_commit": SOURCE,
        "x1_commit": X1,
        "evidence_commit": EVIDENCE,
        "final_binding": "the direct single-parent commit containing this contract",
        "command": "python scripts/ghc_family_v665_v3_canonical_validator.py --receipt <exclusive-external-receipt>",
        "invocation_limit": 1,
        "successful_invocation_must_not_be_replayed": True,
        "full_repository_suite": False,
        "independent_reproduction": False,
        "required": [
            "exact branch and final head",
            "direct three-commit single-parent zero-merge source-to-final chain",
            "clean before and after",
            "0/0 divergence and four-way fresh-live equality",
            "closeout owner tests",
            "strict JSON and Markdown structure",
            "Python compilation and bounded changed-code security review",
            "five-class privacy scan",
            "x1, evidence, final-delta, and final-owner manifest replay",
            "outcome, negative, method, gap, gate, file, word, and terminal truth",
        ],
        "expected_owner_path_count": len(expected_owner),
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": delta_manifest["coverage_valid"]
        and owner_manifest["coverage_valid"]
        and staged_review["valid"],
    }
    write_json(SELF_EXCLUSIONS[0], canonical_contract)
    write_json(SELF_EXCLUSIONS[1], delta_manifest)
    write_json(SELF_EXCLUSIONS[2], owner_manifest)
    write_json(SELF_EXCLUSIONS[3], staged_review)


def check_staged() -> dict[str, Any]:
    actual = staged_paths()
    if actual != INTENDED_PATHS:
        raise CloseoutError(
            f"final staged allowlist changed: expected {len(INTENDED_PATHS)}, got {len(actual)}"
        )
    delta = strict_json_bytes(index_blob(SELF_EXCLUSIONS[1]), "final delta manifest")
    owner = strict_json_bytes(index_blob(SELF_EXCLUSIONS[2]), "final owner manifest")
    review = strict_json_bytes(index_blob(SELF_EXCLUSIONS[3]), "final staged review")
    contract = strict_json_bytes(index_blob(SELF_EXCLUSIONS[0]), "canonical contract")
    mismatches = []
    for entry in delta["entries"]:
        raw = index_blob(entry["path"])
        if sha256(raw) != entry["sha256"] or len(raw) != entry["size"]:
            mismatches.append(entry["path"])
    owner_mismatches = []
    for entry in owner["entries"]:
        raw = index_blob(entry["path"]) if entry["path"] in BASE_PATHS else git_blob(EVIDENCE, entry["path"])
        if sha256(raw) != entry["sha256"] or len(raw) != entry["size"]:
            owner_mismatches.append(entry["path"])
    json_count = 0
    candidates = []
    for path in actual:
        raw = index_blob(path)
        if path.endswith(".json"):
            strict_json_bytes(raw, path)
            json_count += 1
        candidates.extend(scan_candidates(path, raw))
    diff_check = run("git", "diff", "--cached", "--check", check=False)
    if mismatches or owner_mismatches or candidates or diff_check.returncode != 0:
        raise CloseoutError(
            f"final staged audit failure: delta={mismatches}, owner={owner_mismatches}, candidates={candidates}, diff={diff_check.stdout.strip()}"
        )
    if not (
        delta["coverage_valid"]
        and owner["coverage_valid"]
        and review["valid"]
        and contract["valid"]
    ):
        raise CloseoutError("one final staged lifecycle receipt is invalid")
    return {
        "valid": True,
        "staged_paths": len(actual),
        "delta_manifest_entries": len(delta["entries"]),
        "owner_manifest_entries": len(owner["entries"]),
        "strict_json": json_count,
        "privacy_confirmed_hits": 0,
        "diff_hygiene_issues": 0,
    }


def prepare() -> dict[str, Any]:
    built = build_documents()
    run("git", "add", "--sparse", "--", *BASE_PATHS)
    write_staged_receipts()
    run("git", "add", "--sparse", "--", *SELF_EXCLUSIONS)
    return {**built, **check_staged()}


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--prepare", action="store_true")
    modes.add_argument("--check-staged", action="store_true")
    modes.add_argument("--list-paths", action="store_true")
    args = parser.parse_args()
    if args.prepare:
        result = prepare()
    elif args.check_staged:
        result = check_staged()
    else:
        result = {"base_paths": BASE_PATHS, "self_exclusions": SELF_EXCLUSIONS}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
