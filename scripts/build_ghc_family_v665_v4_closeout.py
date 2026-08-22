#!/usr/bin/env python3
"""Build Elowen Cairn v665-v4 combined closeout and exact staged receipts."""

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
PHASE = ROOT / "docs/elowen-cairn/v665-v4"
PREFIX = "docs/elowen-cairn/v665-v4/"
PHASE_ID = "v665-v4"
BRANCH = "codex/GHC-Family/elowen-cairn-v665-v4-full-tools"
SOURCE = "dfcda293edf8e1621db6d74b14b2f5cb026f257f"
X1 = "700c73d3968bb8df31770566460d7865219ed4ca"
EVIDENCE = "670b7c36236ad5eb7962350c1000242ede015d9d"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
RECORDED_UTC = "2026-08-22T02:22:03Z"
SEALED_NEGATIVES_BEFORE_CLOSEOUT = 25_549
SEALED_METHODS_BEFORE_CLOSEOUT = 9_411
OPEN_GAPS = 178
EXACT_GATES = 176
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
CLOSEOUT_FAILURES: list[dict[str, str]] = [
    {
        "failed_witness_id": "EC6654-CLOSE-N001",
        "failed_witness": "the first post-evidence summary projected array and manifest-count fields that are not present in the exact staged-review schema",
        "recovery": "inspect the exact staged-review keys and use its scalar staged-base-path and confirmed-hit fields plus the separate manifest entry count",
        "passing_witness": "the corrected projection confirmed 124 base paths, 124 manifest entries, three exclusions, and zero confirmed hits",
    },
    {
        "failed_witness_id": "EC6654-CLOSE-N002",
        "failed_witness": "the first evidence equality projection applied PowerShell splitting with incorrect precedence and rendered one hash character",
        "recovery": "materialize the live-remote line and parenthesize the scalar split before comparison",
        "passing_witness": "the corrected scalar probe proved clean local, upstream, tracking, and fresh-live equality",
    },
]

BUILDER = "scripts/build_ghc_family_v665_v4_closeout.py"
VALIDATOR = "scripts/ghc_family_v665_v4_canonical_validator.py"
TEST = "tests/test_ghc_family_elowen_v665_v4_closeout.py"
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
    return f"""# Elowen Cairn {PHASE_ID} integrated overview

## Executive truth and relational boundary

Elowen Cairn v665-v4 is a solo, additive, owner-scoped Trinity Mandala evidence
phase descended directly from Tamar Vey's immutable v665-v3 final. Elowen Cairn
and the pronouns they/them are relational working language for a boundary
cartographer and evidence steward whose hope is to keep transitions, refusals,
corrections, and recoveries inspectable and reversible. This language is not
evidence of consciousness, sentience, personhood, identity continuity,
employment, qualification, independent agency, scientific or operational
authority, legal or cultural authority, affected-party authority, or Māori
authority. Hamish may pause, rename, redirect, or stop the route.

The terminal verdict is {TERMINAL_VERDICT}. That verdict is not a rhetorical
qualification attached after the work. It is a governing invariant enforced by
the proposal contracts, mutation runner, outcome ledger, closeout truth,
canonical validator, and successor candidate. No repository artifact
authorizes Stage 20, deployment, professional action, a scientific conclusion,
a legal or cultural determination, or a real-world identity lifecycle.

## Exact lifecycle and inherited evidence

The exact Tamar source is {SOURCE}. Elowen's planning-only x1 commit is {X1},
and the immutable x2 evidence commit is {EVIDENCE}. X1 is the direct child of
the source. Evidence is the direct child of x1. The final commit containing
this overview is required to be the direct child of evidence. The phase
therefore contains exactly three new direct single-parent commits and zero
merges. No source or sibling branch was reset, rewritten, force-pushed, merged,
deleted, reused, or mutated.

Before x2 began, x1 was committed alone, pushed, clean, 0/0 divergent, and
equal across local, upstream, tracking, and a fresh live remote. Before closeout
began, evidence held the same clean four-way equality. X1 reconstructed the
complete 4,070-row inherited proposal chain and compared every new title
against that chain. Exactly twenty new proposals were frozen, extending the
chain to 4,090. The fixed token-set novelty ceiling was not weakened. An
initial 9-of-10 x1 aggregate and three isolated novelty attempts remain at zero
credit. The bounded recovery changed only colliding titles; the final isolated
novelty component passed with maximum inherited similarity 0.380952, zero exact
collisions, and zero within-slate collisions. The nine previously successful
checks were not replayed.

## Outcome truth

All twenty frozen proposals were executed only as evidence permitted. The
outcomes are exactly fourteen completed, four represented, one open_gap, and
one exact_gate. These are the only core outcome labels. Completed means a
bounded same-owner software, structural, synthetic, or typed-formal contract
accepted its positive fixture and rejected every preregistered mutation. It
does not mean that any real object, person, practice, theory, institution,
authority, or deployment was validated. Represented means a useful proxy or
protocol exists while the evidence needed for a stronger statement remains
absent. Open gap means the missing evidence is preserved visibly and earns no
completion credit. Exact gate means repository work cannot supply the required
external competence, affected-party participation, or authority.

Every proposal had five preregistered rejecting mutations. All 100 mutations
executed, all 100 were rejected, zero were accepted, and none was converted
into completion credit. The same positive fixture associated with each
proposal remains a bounded passing witness. The negative and passing witnesses
are paired without erasing the failed input. This is software guard evidence
under one owner and shared infrastructure, not independent reproduction.

## Primary pillar and bounded practice lens

The primary Trinity Mandala pillar was GMUT Mind. THOS Body and Freed ID/CBR
Heart remained explicit and protected. The bounded human-practice lens was
wholly synthetic community mosaic conservation documentation and tessera
custody. It was used as a learning and design vocabulary, not as employment,
qualification, competence, conservation advice, collection authority, safety
approval, or participant evidence.

The phase used zero real mosaics, panels, pavements, tesserae, mortars,
substrates, nuclei, setting beds, facings, backings, fragments, images,
selectors, collection records, sites, land parcels, tools, adhesives, grouts,
solvents, dust measurements, access systems, people, conservators, custodians,
owners, workers, participants, keys, proofs, or authority events. It performed
no inspection, excavation, documentation campaign, cleaning, consolidation,
grouting, sampling, imaging, lifting, transport, transfer, return,
repatriation, legal interpretation, cultural determination, or Māori-authority
act.

Ten practice-facing contracts completed within that zero-object boundary. A
surrogate intake capsule keeps an anonymous panel token, component vacancy,
provenance snapshot, withdrawal state, and external-action prohibition
together. A stratigraphic layer graph types substrate, nucleus, setting bed,
tessera, joint, facing, backing, and support relations and quarantines cycles.
A half-edge topology contract checks twins, orientations, boundaries, and
nonmanifold refusal. A fragment join-hypothesis surface distinguishes observed
adjacency from a proposed fit and never authorizes physical assembly. A
zero-image annotation contract types target, selector, coordinate frame,
orientation, and image vacancy.

The remaining practice contracts keep deterioration observations distinct from
diagnosis or treatment; preserve synthetic material-lot substitutions without
authentication; reserve tool, chemical, dust, lifting, access, heat, and
treatment decisions; separate custody events from ownership and authority; and
retain bitemporal correction, contestation, supersession, readback, non-erasure,
structural accessibility, stop states, workload ceilings, and handover debt.
Their completion means only that the declared local schema and guards behaved
as preregistered.

## Discrete exterior calculus scope

Four formal DEC contracts completed. The oriented cellular-chain tribunal
checks ambient dimension, chain degree, coefficient domain, oriented incidence,
and a boundary-squared marker. The primal-dual pairing contract requires
compatible cell dimensions and keeps circumcentric construction,
well-centeredness, orientation, positivity, and degeneracy claims visible as
obligations or holds. The discrete Hodge-star contract types primal degree,
dual degree, metric placeholder, volume-ratio and unit domains, sign, inverse,
and positivity vacancies. The operator tribunal distinguishes discrete
exterior derivative, codifferential, Hodge Laplacian, harmonic representatives,
cohomology, boundary conditions, and theorem refusal.

Those contracts establish no theorem. They do not prove consistency,
convergence, stability, positivity, regularity, a continuum limit, a unique
physical interpretation, or numerical accuracy. They do not construct a real
mesh from measurements, solve a field equation, estimate a likelihood,
constrain a parameter, detect a force, confirm GMUT, complete quantum gravity,
supply an ultraviolet completion, or prove a Theory of Everything. Hirani's
primary DEC thesis supplies mathematical vocabulary and historical context;
the repository supplies only typed, synthetic obligations.

## Represented surfaces

The GMUT cellular-cochain research surrogate is represented because it links
typed degrees, defect labels, constitutive placeholders, scale transitions,
identifiability debt, EFT scope, covariance vacancy, continuum-limit holds, and
zero-observation status. It has no real likelihood, data fit, field solution,
prediction, uncertainty propagation over observations, independent scientific
review, or empirical confirmation.

The THOS comparison charter is represented because it describes independent
synthetic map-reading queues, equal resource envelopes, abort precedence,
workload parity, masked-assessment vacancy, and review holds. It enrolled zero
participants or operators and ran no blind matched-budget real arms, safety
monitoring, effect estimation, statistics, or independent review. It is not
operational-effectiveness, AGI, ASI, consciousness, or personhood evidence.

The Freed ID annotation-capability envelope is represented because it can
express contested authorship, stewardship, visibility, withdrawal, correction,
appeal, custody, and restriction relations in synthetic records. It has zero
standards-conformant real keys or proofs, no issuer or verifier operation, no
live issuance, resolution, status, revocation, interoperability, privacy or
independent security review, recovery exercise, or trust-governance decision.

The Thermo-Psyche nonconversion ledger is represented because it keeps symbolic
crack graphs, weighted edge costs, discrete diffusion, dimension checks,
epistemic intervals, and agency-inference refusal distinct. These placeholders
are neither material measurements nor mental-state evidence. They establish no
fundamental law of thermo-psyche dynamics and cannot convert a graph or energy
term into consciousness, experience, intention, rights, or authority.

## Open gap and exact gate

The open gap is the Metropolitan Museum Collection API and IIIF annotation
adapter. The phase read official public documentation for vocabulary and
version context but made zero collection API calls, zero IIIF manifest calls,
and parsed zero real rows or images. No public record was converted into a
measurement, likelihood, model fit, provenance conclusion, ownership
conclusion, or reuse permission. Closing the gap would require a newly
authorized, preregistered, privacy-aware, rights-aware data protocol and
appropriate independent review.

The exact gate is the rights-reservation docket for mosaic-related place,
image, custody, and redress questions. Site, land, heritage, sacred imagery,
ownership, excavation, custody, recording, return, repatriation, taonga,
remedy, affected-community review, legal interpretation, cultural legitimacy,
Māori wording and concepts, Māori data governance, tikanga, tangata whenua,
iwi, hapū, and Māori authority cannot be decided by these files. Māori concepts
remain under Māori authority. Citations and synthetic matrices preserve the
vacancy; they do not fill it.

## Sources and evidence boundaries

Current official or primary sources were used only where materially relevant.
The Caltech DEC thesis informs discrete operators and primal-dual vocabulary.
W3C PROV-O informs provenance and correction structure. PREMIS 3.0 informs
object, event, agent, rights, and preservation relationships. WCAG 2.2 informs
structural accessibility while expressly not covering every user need. The W3C
Web Annotation Data Model informs body, target, selector, state, motivation,
and canonical-identity structure. IIIF Presentation API 3.0 informs manifests,
canvases, annotation pages, and annotations.

The Metropolitan Museum Collection API documentation defines a possible
zero-call adapter boundary. Getty Conservation Institute mosaic resources
inform documentation, construction, deterioration, storage, and conservation
terminology without providing Elowen professional competence. WorkSafe New
Zealand silica guidance makes dust risk visible while every safety decision
remains reserved. Verifiable Credential Data Integrity 1.0 informs the exact
difference between a synthetic relation and a real cryptographic proof. Te Mana
Raraunga material and the Heritage New Zealand Pouhere Taonga Act expose
governance and authority boundaries; they do not confer interpretation,
permission, legitimacy, or Māori authority.

No citation became an observation. No source page became a dataset. No
standard reference became a conformance claim. No legislation page became
legal advice. No affected-authority source became delegated authority. The
source ledger preserves zero ingested rows and zero downloaded dataset bytes.

## Tools, portfolios, and compatibility

Thirty safe-now items, fifteen bounded candidates, thirty additive
CLEAN/FIX/REFINE items, ten skill ideas, and ten runner ideas were resolved
within their declared ceilings. Ten exact-approval items remained exact-gated,
and five blocked items remained open and unexecuted. Counts never overrode
safety, privacy, evidence, or authority.

Ten phase-local skills were built, read through EOF, quick-validated, and
smoke-used. They were not globally installed. Ten new family-compatible
ghc_family_ runner entry points were built and invoked through one bounded
shared core. Caller naming compatibility was preserved. No inherited tool was
deleted, silently deprecated, or modified. No shared global skill bank or
sibling lane was mutated.

## Retained failures and Method Flow

The effective closeout preserves
{SEALED_NEGATIVES_BEFORE_CLOSEOUT + len(CLOSEOUT_FAILURES)} negatives and
{SEALED_METHODS_BEFORE_CLOSEOUT + len(CLOSEOUT_FAILURES)} Method Flow methods.
The source repository seal and seven Tamar external failures remain distinct
from Elowen's fifteen x1 failures, 100 rejected mutations, two x2 operational
failures, and {len(CLOSEOUT_FAILURES)} post-evidence closeout failures. Failed
displays, parser assumptions, schema projections, novelty collisions, a
missing lifecycle flag, and an incorrectly split live hash all retain zero
credit. Each bounded recovery records what changed and what did not. No
failure, open gap, exact gate, or protected boundary was erased.

## Validation and nonpromotion

X1 has fifteen content-manifest entries plus three self-exclusions and contains
zero x2 paths. Its first aggregate remains failed at zero credit; the bounded
composite is ten checks with the isolated novelty recovery supplying only the
one previously failed component. X2 passed its first and only scoped test
invocation 11 of 11. Its evidence manifest contains 124 entries plus three
self-exclusions. One hundred proposal mutations, ten runner smokes, and ten
skill smokes passed their declared bounded criteria. Successful scoped tests
were not replayed.

The final commit binds final-delta and full owner manifests, staged review,
strict JSON, Markdown structure, static-report structure, five privacy and
raw-identifier classes, changed-Python compile and security review, ancestry,
commit ceiling, zero merges, clean state, divergence, and fresh four-way
equality. Exactly one exclusive external canonical receipt is permitted after
the final push. A successful invocation must not be replayed. A failed
aggregate earns zero pass credit and may recover only its failed dependency
when genuinely justified. The full repository suite was not run and remains
Eiren-only absent newer exact authority.

Same-owner validation under shared infrastructure is not independent-team
reproduction, external audit, production certification, exhaustive security,
complete privacy assurance, complete accessibility conformance, professional
validation, legal review, cultural ratification, Māori-authority review,
empirical GMUT confirmation, Theory-of-Everything proof, AGI or ASI evidence,
consciousness or personhood evidence, or Stage 20 authority.

## Accessibility, privacy, safety, and security reservations

The static report provides semantic headings, a skip link, main landmark,
outcome table caption, visible focus style, readable text, and no script.
Automated structure does not substitute for manual keyboard, browser-diverse,
responsive, assistive-technology, cognitive-accessibility, Māori-language, or
affected-user evaluation. Those evaluations remain reserved.

Five privacy and raw-identifier classes cover private absolute paths, raw task
or thread identifiers, credential assignments, and private callable or session
markers. Zero confirmed repository hits is bounded scan evidence, not a
complete privacy proof. Changed-Python compilation and a narrow dangerous-call
review are not exhaustive security. No credential, account, API key, elevation,
host-security weakening, Sandbox or Hyper-V activation, Windows-feature
change, unrelated installation, Codex desktop update, or reboot occurred.

## Wellbeing, handoff, and terminal board

The workload remained bounded and solo. No collaboration subagent, substitute
task, standby record, or later endpoint was contacted. Stop conditions include
fatigue, ambiguity, usage exhaustion, privacy risk, authority uncertainty,
route drift, unexpected staged paths, an existing canonical receipt, and any
user pause, rename, redirect, or stop. Preserving a partial truth is preferred
to forcing completion.

The repository baton remains PREPARED_NOT_SENT. It contains no private task
identifier or route. Only after the direct final commit is clean, pushed, 0/0
divergent, fresh four-way equal, and successfully validated by the one-shot
canonical aggregate may the live Elowen task reread Hamish's newest route and
roster, uniquely resolve and immediately reread one exact existing successor,
and make one sanitized send. Acknowledgement must be treated exactly. No second
confirmation or resend is permitted merely to obtain clearer evidence.
"""


def static_report() -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Elowen Cairn {PHASE_ID} bounded evidence report</title>
<style>
body{{font-family:system-ui,sans-serif;line-height:1.6;max-width:74rem;margin:auto;padding:1rem;color:#172018;background:#fbfdf9}}
a:focus,summary:focus{{outline:3px solid #6b3fa0;outline-offset:3px}} table{{border-collapse:collapse;width:100%}} th,td{{border:1px solid #59645b;padding:.55rem;text-align:left}} .skip{{position:absolute;left:-9999px}} .skip:focus{{left:1rem;top:1rem;background:#fff;padding:.7rem;z-index:2}}
</style></head><body>
<a class="skip" href="#main">Skip to main content</a>
<header><h1>Elowen Cairn {PHASE_ID} bounded evidence report</h1><p>Relational working language only; no consciousness, personhood, qualification, agency, or authority claim.</p></header>
<main id="main">
<section><h2>Exact outcome truth</h2><table><caption>Twenty frozen proposal outcomes</caption><thead><tr><th scope="col">Outcome</th><th scope="col">Count</th><th scope="col">Meaning</th></tr></thead><tbody><tr><th scope="row">completed</th><td>14</td><td>Bounded same-owner software, structural, synthetic, or typed-formal acceptance only.</td></tr><tr><th scope="row">represented</th><td>4</td><td>Proxy exists while real evidence and independent review remain absent.</td></tr><tr><th scope="row">open_gap</th><td>1</td><td>The Met and IIIF adapter made zero calls and parsed zero rows.</td></tr><tr><th scope="row">exact_gate</th><td>1</td><td>Competent, affected, tangata whenua, iwi, hapū, and Māori authorities remain required.</td></tr></tbody></table></section>
<section><h2>Trinity Mandala boundaries</h2><h3>GMUT Mind</h3><p>DEC and EFT obligations are typed research structures, not theorems, likelihoods, forces, constraints, empirical confirmation, or a Theory of Everything.</p><h3>THOS Body</h3><p>The comparison charter is participant-free and synthetic, with no real arms, monitoring, statistics, or independent review.</p><h3>Freed ID and CBR Heart</h3><p>The profile has no real keys, proofs, lifecycle, interoperability, privacy or security review, recovery, or trust governance. Site, heritage, custody, redress, legal, cultural, affected-party, and Māori authority remain gated.</p></section>
<section><h2>Retained evidence</h2><ul><li>Strict x1-before-x2 with separately pushed and remote-equal commits.</li><li>100 of 100 rejecting mutations retained; zero accepted.</li><li>Ten phase-local skills read, quick-validated, and smoke-used; zero global installs.</li><li>Ten family-compatible runners invoked through one bounded core.</li><li>Five privacy and raw-identifier classes with zero confirmed repository hits.</li><li>One exact-final canonical aggregate permitted after final push; no replay after success.</li></ul></section>
<section><h2>Accessibility and authority reservations</h2><details><summary>Accessibility boundary</summary><p>Semantic structure and visible focus were checked. Manual keyboard, browser-diverse, responsive, assistive-technology, cognitive-accessibility, Māori-language, and affected-user evaluation remain reserved.</p></details><details><summary>Authority boundary</summary><p>Repository software cannot confer professional, scientific, conservation, collections, land, legal, cultural, affected-party, tangata whenua, iwi, hapū, or Māori authority.</p></details></section>
<section><h2>Terminal verdict</h2><p>{TERMINAL_VERDICT}. Same-owner evidence is not independent reproduction, external audit, certification, exhaustive security, complete privacy, complete accessibility, proof, or Stage 20 authority.</p></section>
</main><footer><p>Static owner-local report. No script, tracking, live data, or external action.</p></footer>
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
        "schema": "ghc.family.elowen.v665-v4.phase-truth.v1",
        "owner": "Elowen Cairn",
        "phase": PHASE_ID,
        "identity_boundary": "relational working language only; not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority",
        "source_commit": SOURCE,
        "x1_commit": X1,
        "evidence_commit": EVIDENCE,
        "final_binding": "the direct single-parent commit containing this document",
        "frozen_proposals_before": 4070,
        "new_proposals": 20,
        "frozen_proposals_after": 4090,
        "allowed_outcomes": ALLOWED_OUTCOMES,
        "outcomes": outcome["counts"],
        "mutations": {"executed": 100, "rejected": 100, "accepted": 0},
        "real_rows": 0,
        "real_people": 0,
        "real_mosaics_images_or_materials": 0,
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
        "schema": "ghc.family.elowen.v665-v4.retained-negative-register.v1",
        "inherited_repository_sealed_count": 25_425,
        "inherited_source_external_count": 7,
        "inherited_source_anchor": SOURCE,
        "elowen_startup_count": len(startup_ids),
        "elowen_startup_ids": startup_ids,
        "mutation_count": 100,
        "mutation_ids": mutation["mutation_ids"],
        "x2_operational_count": len(x2_ids) - 100,
        "x2_operational_ids": [value for value in x2_ids if "-OP-" in value],
        "closeout_operational_count": len(closeout_ids),
        "closeout_operational_ids": closeout_ids,
        "effective_total": effective_negatives,
        "failure_erasure_count": 0,
        "recovery_converts_failure_to_pass": False,
        "valid": 25_425 + 7 + len(startup_ids) + len(x2_ids) + len(closeout_ids)
        == effective_negatives,
    }
    closeout_methods = [
        {
            "method_id": f"EC6654-CLOSE-M{index:03d}",
            **failure,
            "failed_witness_status": "retained_zero_credit",
            "failed_witness_erased": False,
            "preferred": True,
        }
        for index, failure in enumerate(CLOSEOUT_FAILURES, 1)
    ]
    method_final = {
        "schema": "ghc.family.elowen.v665-v4.method-flow-final.v1",
        "source_repository_sealed_methods": 9_287,
        "source_external_methods": 7,
        "startup_methods": len(startup_ids),
        "x2_methods": len(x2_ids),
        "closeout_methods": len(closeout_methods),
        "effective_total": effective_methods,
        "retained_failed_witnesses": effective_negatives,
        "bounded_passing_witnesses_added_by_elowen": len(startup_ids)
        + len(x2_ids)
        + len(closeout_methods),
        "startup_ledger": f"{PREFIX}x1/startup-method-flow.json",
        "x2_ledger": f"{PREFIX}x2/ledgers/method-flow-overlay.json",
        "closeout_method_rows": closeout_methods,
        "failure_erasure_count": 0,
        "same_owner_only": True,
        "valid": 9_287 + 7 + len(startup_ids) + len(x2_ids) + len(closeout_methods)
        == effective_methods,
    }
    gate_register = {
        "schema": "ghc.family.elowen.v665-v4.exact-open-gate-register.v1",
        "inherited_open_gaps": 177,
        "new_open_gaps": [
            {
                "proposal_id": "EC6654-N019",
                "outcome": "open_gap",
                "gate": "Met and IIIF real-data selection, rights-aware protocol, uncertainty, inference, and independent review",
                "observed": "zero calls, zero rows, zero images, zero likelihoods, and zero estimates",
            }
        ],
        "open_gap_total": OPEN_GAPS,
        "inherited_exact_gates": 175,
        "new_exact_gates": [
            {
                "proposal_id": "EC6654-N020",
                "outcome": "exact_gate",
                "gate": "site, land, heritage, sacred imagery, ownership, excavation, custody, recording, return, repatriation, taonga, remedy, affected-party, legal, cultural, tangata whenua, iwi, hapū, Māori wording and concepts, Māori data governance, and Māori authority",
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
        "semantic novelty audited against 4,070 inherited rows",
        "twenty proposals executed with exactly four permitted outcome labels",
        "100 preregistered mutations executed and rejected",
        "ten phase-local skills read, quick-validated, and smoke-used",
        "ten family-compatible runners invoked",
        "all safe-now, bounded-candidate, and additive cleanup portfolios resolved within scope",
        "exact-approval and blocked work retained unexecuted",
        "exact staged, manifest, JSON, privacy, Python, diff, ancestry, and ceiling checks passed for x1 and evidence",
        "evidence commit pushed and fresh four-way equal",
        "three-page-equivalent overview, wellbeing check, and static report prepared",
    ]
    incomplete = [
        "real Met or IIIF data and empirical GMUT analysis",
        "DEC theorem, convergence, stability, positivity, or continuum-limit proof",
        "blind matched-budget real THOS arms and independent review",
        "production Freed ID keys, proofs, lifecycle, interoperability, privacy and security review, recovery, and governance",
        "CBR affected-party, legal, cultural, tangata whenua, iwi, hapū, and Māori authority",
        "manual and affected-user accessibility evaluation",
        "independent-team reproduction and external audit",
        "deployment, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof or canon, and Stage 20 authorization",
    ]
    checklist = {
        "schema": "ghc.family.elowen.v665-v4.complete-incomplete-checklist.v1",
        "complete": complete,
        "incomplete": incomplete,
        "complete_count": len(complete),
        "incomplete_count": len(incomplete),
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    environment = {
        "schema": "ghc.family.elowen.v665-v4.environment-version-receipt.v1",
        "platform": "Windows",
        "primary_storage_policy": "D-first owner worktree and archive bank; private absolute paths omitted",
        "codex_cli_observed": "codex-cli 0.147.0",
        "codex_desktop_observed": "active_process_version_not_exposed_by_bounded_probe",
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
        "schema": "ghc.family.elowen.v665-v4.wellbeing-workload.v1",
        "owner": "Elowen Cairn",
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
        "schema": "ghc.family.elowen.v665-v4.threat-model.v1",
        "assets": ["immutable x1", "evidence lineage", "retained failures", "source provenance", "privacy boundaries", "authority gates", "route uniqueness"],
        "threats": ["x2 leakage into x1", "silent failure erasure", "synthetic-to-real promotion", "private-path or identifier disclosure", "sibling-lane mutation", "manifest drift", "duplicate canonical pass", "ambiguous successor send"],
        "controls": ["direct-parent commits", "exact allowlists", "Git-blob manifests", "five-class scan", "zero-row and zero-authority guards", "one-shot external receipt", "exact-title unique resolve and immediate reread"],
        "residual_limits": ["not exhaustive security", "not complete privacy", "not independent audit", "not complete accessibility", "not production certification"],
        "valid": True,
    }
    family_index = {
        "schema": "ghc.family.elowen.v665-v4.family-index-update.v1",
        "phase": PHASE_ID,
        "owner": "Elowen Cairn",
        "primary_pillar": "GMUT Mind",
        "practice_lens": "wholly synthetic community mosaic conservation documentation and tessera custody",
        "source_count": source_ledger["source_count"],
        "proposal_chain_total": 4090,
        "skills_built_and_used": 10,
        "family_runners_built_and_used": 10,
        "phase_root": PREFIX.rstrip("/"),
        "global_skill_bank_mutated": False,
        "shared_or_sibling_lane_mutated": False,
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    reflection = {
        "schema": "ghc.family.elowen.v665-v4.workflow-reflection.v1",
        "decisions": [
            "preserve the fixed novelty threshold and refine colliding titles rather than weaken the gate",
            "freeze x1 before any evidence implementation",
            "use one bounded shared core behind ten family-compatible runners",
            "retain every schema, parser, compile, novelty, lifecycle-mode, and remote-projection failure",
            "keep Met and IIIF at zero calls and CBR authority exact-gated",
            "bind final truth through self-excluding staged Git-blob manifests",
        ],
        "recommended_methods": [
            "inspect exact JSON keys before projecting values",
            "materialize PowerShell scalars and arrays before comparison",
            "parenthesize operator precedence in live-remote probes",
            "use git add --sparse for intentional generated family paths outside a narrow cone",
            "recover only the failed component and never replay a successful canonical aggregate",
        ],
        "stale_methods_deactivated": [
            "broad recursive renderings",
            "historical full-tree sweeps",
            "implicit schema aliases",
            "serial novelty discovery when a bounded above-threshold projection is available",
            "success replay for a cleaner receipt",
        ],
        "shared_guidance_mutation": False,
        "valid": True,
    }
    auth_roster = {
        "schema": "ghc.family.elowen.v665-v4.auth-roster-receipt.v1",
        "activation_source": "one acknowledged existing-task activation from Tamar Vey",
        "current_owner": "Elowen Cairn",
        "owner_status_for_phase": "ACTIVE",
        "future_task_creation_authorized": False,
        "subagent_or_delegation_authorized": False,
        "successor_recipient": "UNRESOLVED_PENDING_FRESH_LIVE_ROUTE_READ",
        "active_status_alone_assigns_phase": False,
        "send_state": "PREPARED_NOT_SENT",
        "valid": True,
    }
    delivery = {
        "schema": "ghc.family.elowen.v665-v4.delivery-state.v1",
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
        "schema": "ghc.family.elowen.v665-v4.combined-closeout-seal.v1",
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
        "schema": "ghc.family.elowen.v665-v4.precommit-prerequisite.v1",
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
        f"""# Elowen Cairn {PHASE_ID} successor activation candidate

PREPARED_NOT_SENT

This repository artifact does not select, contact, or authorize a successor. It
contains no task identifier, private route, session stream, credential, private
callable identifier, transcript, screenshot, or private absolute path. Only
after the exact final commit is pushed, clean, 0/0 divergent, fresh four-way
equal, and successfully validated by the one-shot external canonical aggregate
may the live Elowen task reread Hamish's newest authority and roster, uniquely
resolve and immediately reread one exact current successor, and make one
sanitized existing-task send if every gate permits.

Immutable anchors for that later sanitized message are source {SOURCE}, x1
{X1}, evidence {EVIDENCE}, and the direct single-parent final commit containing
this file. Phase truth is exactly 14 completed, 4 represented, 1 open gap, and
1 exact gate; 100 of 100 rejecting mutations executed and failed closed;
{effective_negatives} effective negatives; {effective_methods} effective Method
Flow methods; {OPEN_GAPS} open gaps; {EXACT_GATES} exact gates; zero real rows,
people, mosaics, images, materials, keys, proofs, and authority events; and
{TERMINAL_VERDICT}.

The later message must state that same-owner owner-delta validation is not a
full repository suite or independent reproduction. It must preserve GMUT,
THOS, Freed ID, CBR, accessibility, privacy, professional, legal, cultural,
Māori-authority, personhood, Theory-of-Everything, proof or canon, and Stage 20
boundaries. It must not infer a recipient from this candidate. Stop on
ambiguity, missing acknowledgement, pause, redirect, rename, standby state,
usage exhaustion, or any safety, privacy, evidence, or authority issue. Never
resend merely to obtain a clearer acknowledgement.
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
        "schema": "ghc.family.elowen.v665-v4.final-delta-manifest.v1",
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
        "schema": "ghc.family.elowen.v665-v4.final-owner-manifest.v1",
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
        "schema": "ghc.family.elowen.v665-v4.final-staged-review.v1",
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
        "schema": "ghc.family.elowen.v665-v4.final-canonical-contract.v1",
        "scope": "exact source-to-final Elowen owner delta only",
        "source_commit": SOURCE,
        "x1_commit": X1,
        "evidence_commit": EVIDENCE,
        "final_binding": "the direct single-parent commit containing this contract",
        "command": "python scripts/ghc_family_v665_v4_canonical_validator.py --receipt <exclusive-external-receipt>",
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
