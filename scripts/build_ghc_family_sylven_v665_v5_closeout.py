#!/usr/bin/env python3
"""Build Sylven Arc v665-v5 combined closeout and exact staged receipts."""

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
PHASE = ROOT / "docs/sylven-arc/v665-v5"
PREFIX = "docs/sylven-arc/v665-v5/"
PHASE_ID = "v665-v5"
BRANCH = "codex/GHC-Family/sylven-arc-v665-v5-full-tools"
SOURCE = "296ec195744fbbf62bae5d2f233f1112bcc14591"
X1 = "0a24628b70e1179a8758718a05029060488a9a1b"
EVIDENCE = "de620467651cb5268e8b89f8ad85345e6b9c9c62"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
RECORDED_UTC = "2026-08-22T03:20:00Z"
SEALED_NEGATIVES_BEFORE_CLOSEOUT = 25_662
SEALED_METHODS_BEFORE_CLOSEOUT = 9_524
OPEN_GAPS = 179
EXACT_GATES = 177
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
CLOSEOUT_FAILURES: list[dict[str, str]] = [
    {
        "failed_witness_id": "SA6655-CLOSE-N001",
        "failed_witness": "the first x2 adaptation patch expected a non-owner-prefixed builder filename and was rejected atomically before mutation",
        "recovery": "inspect the exact transformed file header and split the adaptation into verified owner-local hunks",
        "passing_witness": "the corrected hunks updated only the Sylven evidence builder and the later exact staged evidence gate passed",
    },
    {
        "failed_witness_id": "SA6655-CLOSE-N002",
        "failed_witness": "a broad precommit state projection exceeded the bounded presentation context and returned truncated output without changing repository state",
        "recovery": "project only scalar precommit fields and bounded counts while leaving path-level evidence in the committed staged-review receipt",
        "passing_witness": "the narrow scalar precommit gate proved staged-review validity, zero unstaged or untracked paths, diff hygiene, and the exact evidence head",
    },
    {
        "failed_witness_id": "SA6655-CLOSE-N003",
        "failed_witness": "the first dependency rebuild refused the already-staged four declared self-exclusion receipts because its recovery guard admitted only base paths",
        "recovery": "extend the recovery guard to the exact intended closeout path set of base paths plus the four declared self-exclusions",
        "passing_witness": "the corrected guard remains owner-closeout-scoped and permits no path outside the exact staged allowlist",
    },
    {
        "failed_witness_id": "SA6655-CLOSE-N004",
        "failed_witness": "the next dependency rebuild counted four already-staged declared self-exclusions as base delta paths and rejected 24 paths against the 20-path base contract",
        "recovery": "derive the base delta by subtracting exactly the four named self-exclusions and apply the same filter to the pre-self-exclusion owner comparison",
        "passing_witness": "the staged writer preserves separate 20-path base and four-path self-exclusion domains without unstaging or rewriting prior commits",
    },
    {
        "failed_witness_id": "SA6655-CLOSE-N005",
        "failed_witness": "the first narrow precommit projection guessed three staged-review property names and returned null values despite a valid receipt",
        "recovery": "enumerate the exact staged-review schema keys before projecting only confirmed scalar fields",
        "passing_witness": "the schema-aware scalar projection uses confirmed_privacy_or_raw_identifier_hits, deletion_paths, diff_hygiene_issues, and the exact ceiling booleans",
    },
    {
        "failed_witness_id": "SA6655-CLOSE-N006",
        "failed_witness": "the next scalar projection wrapped two numeric zero count fields as arrays and displayed one element for each",
        "recovery": "inspect each JSON value type and cast the Int64 privacy and diff counts directly while retaining array counting only for deletion_paths",
        "passing_witness": "the type-aware projection reports the stored numeric zeros without changing or replaying the staged receipt",
    },
]

BUILDER = "scripts/build_ghc_family_sylven_v665_v5_closeout.py"
VALIDATOR = "scripts/ghc_family_sylven_v665_v5_canonical_validator.py"
TEST = "tests/test_ghc_family_sylven_v665_v5_closeout.py"
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
    return f"""# Sylven Arc {PHASE_ID} integrated overview

## 1. Executive truth

Sylven Arc v665-v5 is a solo, additive, owner-scoped Trinity Mandala evidence
phase whose exact source is Elowen Cairn's immutable {SOURCE} final. It preserves
strict x1-before-x2 separation and produces three direct single-parent Sylven
commits: planning-only x1 {X1}, bounded evidence {EVIDENCE}, and the final
closeout commit containing this overview. No merge, history rewrite,
force-push, reset, destructive cleanup, sibling-lane mutation, task fork,
collaboration subagent, substitute endpoint, or premature successor contact is
part of this phase.

The core outcome truth is exactly fourteen completed, four represented, one
open_gap, and one exact_gate. Those four labels are the entire outcome
vocabulary. A completed outcome means that one bounded owner-local software or
typed-structure contract accepted its synthetic positive fixture and rejected
all five preregistered invalid variants. It is not a claim that a kiln,
workplace, material, person, scientific theory, identity system, professional
practice, law, culture, or authority was validated. Represented means only
that a synthetic proxy or protocol exists. Open gap and exact gate mean that
required real evidence or authority remains absent and visible.

The terminal verdict is {TERMINAL_VERDICT}. No artifact in this phase
authorizes Stage 20, deployment, professional action, product or workplace
advice, empirical GMUT confirmation, a Theory of Everything, AGI or ASI,
consciousness or personhood, legal or cultural interpretation, Māori
authority, proof, or canon.

## 2. Relational working identity and corrigibility

Sylven Arc and they/them are relational working language for a continuity
gardener and evidence-boundary steward. The associated hope is to keep memory
light, evidence recoverable, and authority boundaries visible. This language
supports collaboration and document continuity; it is not evidence of
consciousness, sentience, legal personhood, identity continuity, employment,
qualification, independent agency, scientific authority, operational
authority, legal authority, cultural authority, affected-party authority, or
Māori authority.

Hamish retains the right to rename, pause, redirect, or stop the route. The
phase therefore treats corrigibility as an operational requirement. A newer
live instruction outranks an older prepared cursor, while immutable historical
records remain accurate for their own time. No active-status label by itself
assigns a phase or a successor. A later terminal handoff requires a fresh
roster and authorization read, unique exact-title resolution, immediate
reread, one sanitized send, and acknowledgement from the supported task
surface. Ambiguity causes a stop rather than an inferred route.

## 3. Exact lifecycle and source boundary

The source commit {SOURCE} is clean, 0/0 divergent, and was verified equal
across its local branch, upstream, tracking reference, and a fresh live remote.
Its x1, evidence, and final ancestry, three source-owner commits, zero merges,
one final parent, commit-local manifest contracts, and external receipt
digests were rechecked read-only. Elowen's successful components were not
replayed.

Sylven's x1 {X1} is the direct child of that source. It contains planning,
sources, hypotheses, nulls, approval classes, execution lanes, artifact
contracts, falsifiers, rollback paths, protected gates, expected
dispositions, portfolio ideas, Method Flow startup rows, and exact staged
receipts. It contains no x2 implementation or outcome. X1 was committed,
pushed, clean, 0/0 divergent, and equal across local, upstream, tracking, and
a fresh live remote before x2 began.

Evidence {EVIDENCE} is the direct child of x1. It contains the twenty bounded
contracts, positive fixtures, 100 rejecting mutation receipts, ten phase-local
skills, ten family-compatible runners, outcome and boundary ledgers, x1
integrity replay, exact evidence manifest, and staged review. Evidence was
pushed and independently proved clean and fresh four-way equal before this
closeout began. The final commit is required to be the direct child of
evidence, leaving exactly three Sylven phase commits and zero merges.

## 4. Novelty and x1 planning truth

The novelty audit reconstructed all 4,090 inherited frozen proposal rows from
commit-local proposal ledgers. Each of the twenty new Sylven titles was
compared against every inherited title using exact comparison and casefolded
alphanumeric token-set Jaccard similarity. The same slate was compared
internally at a 0.70 collision threshold. The resulting maximum inherited
similarity was 0.448276, with zero exact inherited collision and zero
within-slate collision. The inherited chain therefore extends to 4,110 rows.
Inherited proposals, tools, methods, artifacts, and recommendations receive
zero Sylven novelty or automatic completion credit.

A first x1 freeze failed closed because the reused planning test contained one
extra blank line at EOF. The exact staged review reported the defect through
diff hygiene. Only that byte-level issue was removed; the failed attempt was
retained at zero credit and added to Method Flow. The dependency-justified
rebuild then passed its staged gate, and all ten x1 planning tests passed. No
failure was erased and the novelty threshold was not weakened.

The frozen portfolio contains thirty safe-now tasks, fifteen bounded
candidates, ten exact-approval packets, five blocked packets, ten phase-local
skill ideas, ten family-current runner ideas, and thirty additive
CLEAN/FIX/REFINE rows. Counts are planning floors bounded by relevance and
safety, never authority to manufacture unsafe work. Exact and blocked packets
remain unexecuted.

## 5. Bounded human-practice lens

The bounded practice is wholly synthetic community ceramics kiln-firing
documentation and glaze-batch quarantine. This is a learning and
software-design lens only. The phase used zero real people, studios, kilns,
firings, ware, shelves, witness cones, clay, glaze, recipes, material lots,
images, instruments, controllers, safety-data sheets, measurements, tests,
workplace actions, consumer claims, incidents, professional decisions, legal
decisions, cultural decisions, affected-party decisions, or authority acts.

The software may check whether a synthetic record has required documentary
fields, internally consistent units, an explicit hold, a correction lineage,
a non-actuation boundary, or a retained disagreement. It cannot decide a
firing schedule, arrange a load, determine clearance, operate a controller,
release a glaze batch, classify a substance, assess ventilation, diagnose a
defect, prescribe treatment, certify safety, advise a worker or customer, or
authorize any physical action.

The practice lens also preserves privacy and dignity. No real recipe, studio
record, image, person, location, incident, heritage record, or protected
knowledge was ingested. Identifiers inside fixtures are synthetic tokens.
Professional competence, kiln or materials competence, safety authority,
employment, ownership, custody, collection, product, legal, cultural, remedy,
and Māori authority remain absent.

## 6. Completed bounded contracts

The fourteen completed contracts cover a synthetic kiln-load capsule,
shelf-plane clearance graph, glaze-batch quarantine braid, witness-cone
readback packet, firing-program state lattice, kiln command-versus-observation
firewall, safety authority stop-card, temperature-time type board, thermal
balance obligation slate, initial-and-boundary condition docket, Arrhenius
identifiability tribunal, Fourier-and-Biot classifier, defect-language
firewall, and bitemporal firing-record correction weave.

Each completed contract accepted one declared synthetic positive fixture.
Five distinct invalid variants then tested the common boundary fields and one
profile-specific failure. Common variants attempted to remove the synthetic
marker, introduce a real row, introduce an authority event, or promote the
terminal verdict. Profile-specific variants attempted such things as an
external action, an overlap, a physical batch release, an interpretation
claim, a real actuation, a live controller call, dimensional imbalance, an
agency inference, a live data call, or a Māori-authority decision. Every one
was rejected.

Exactly 100/100 preregistered mutations were executed and rejected, and zero
was accepted. The positive witnesses do not cancel the rejected witnesses.
Each failed mutation remains a retained negative at zero completion credit,
paired with a bounded positive witness and a recurrence guard. This is
software-guard evidence only.

## 7. Represented, open, and exact-gated contracts

Four proposals remain represented. The GMUT thermal-gradient surrogate links
typed scalar and tensor placeholders, interface obligations, scale
transitions, and an observation firewall, but contains no real measurement,
fit, calibrated material property, likelihood, prediction, or confirmation.
The THOS charter has only participant-free documentation queues and synthetic
resource envelopes; it has no governed real arms, operators, safety
monitoring, statistics, or independent review. The Freed ID envelope has no
real key, proof, issuer, verifier, lifecycle, interoperability, privacy or
independent security review, recovery evidence, or trust governance. The
Thermo-Psyche register explicitly blocks conversion of heat, diffusion, or
entropy symbols into evidence of affect, agency, personhood, ethics, or
authority.

The open gap is the EPA and WorkSafe schema adapter. It made zero data calls,
downloaded zero empirical rows, and parsed zero real regulatory, workplace, or
material record. Official pages supplied current public vocabulary and
boundary context only. They did not become observations, professional advice,
regulatory decisions, or evidence that a real system is safe or compliant.

The exact gate reserves worker and consumer decisions, studio access and
custody, design heritage and traditional knowledge, taonga, remedy,
affected-party legitimacy, legal and cultural interpretation, Māori wording
and concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori
authority. Repository software cannot close these gates.

## 8. Trinity Mandala evidence boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model
family. Temperature-time segments, heat-balance terms, boundary conditions,
Arrhenius placeholders, Fourier and Biot expressions, unit checks, uncertainty,
and identifiability are formal obligation surfaces. They establish no real
likelihood, parameter constraint, unique prediction, detected force, material
law, stability theorem, empirical confirmation, quantum completion,
ultraviolet completion, final physics, Theory of Everything, proof, or canon.

THOS remains proxy-only. A synthetic state machine or handover document does
not demonstrate operational effectiveness, deployment readiness, safe
practice, AGI, ASI, consciousness, or personhood. A stronger THOS claim would
require preregistered blind matched-budget governed real arms, competent
participants or operators, safety monitoring, appropriate statistics, and
independent review.

Freed ID remains synthetic and nonproduction. It would require
standards-conformant real keys and proofs, governed issuance and resolution,
status and revocation, interoperability, privacy and independent security
review, recovery evidence, trust governance, and affected-party oversight
before any production claim. CBR decisions remain with competent and affected
authorities. Māori concepts remain under Māori authority.

## 9. Sources and provenance

The source ledger records twelve current or stable official and primary
surfaces. NIST supplies SI-unit vocabulary. W3C PROV-O supplies provenance and
correction vocabulary. WCAG 2.2 supplies structural accessibility criteria.
EPA New Zealand supplies public hazardous-substance and classification
context. WorkSafe New Zealand supplies safety-data-sheet, risk-management,
silica, emergency-plan, and local-exhaust-ventilation vocabulary. W3C
Verifiable Credential Data Integrity supplies proof-model boundaries. Te Mana
Raraunga supplies a primary authority-reservation and Māori data-sovereignty
context.

All source use is bounded to terminology, schema, provenance, and explicit
nonclaim boundaries. No dataset was downloaded, no protected page was scraped,
no account or credential was used, and no third-party write occurred. The
source ledger records zero ingested real rows and zero authority conferred.
Citations do not turn synthetic fixtures into empirical, professional, legal,
cultural, or Māori-authority evidence.

## 10. Tools, accessibility, privacy, and security

Ten phase-local skills were built, read through EOF, quick-validated, and
smoke-used. Ten family-compatible runners were generated with the
ghc_family_ prefix and invoked against bounded positive fixtures. They were
not installed globally, bulk-promoted, or treated as production tools. The
shared core rejects non-synthetic rows, authority events, terminal promotion,
live calls, real controller actions, empirical claims, and protected authority
fields.

The static report uses semantic headings, a skip link, a main landmark,
captioned tables, visible focus, plain language, and non-colour outcome names.
It contains no script. These are structural checks only. Manual keyboard,
browser-diverse, responsive, assistive-technology, cognitive-accessibility,
Māori-language, and affected-user evaluation remain reserved.

Exact staged Git blobs are scanned across five privacy and raw-identifier
classes. Changed Python files are compiled and bounded-reviewed for dangerous
dynamic execution, shell invocation, and unsafe deserialization patterns. This
is not complete privacy, exhaustive security, external audit, or production
certification. Raw task or thread identifiers, private routes and paths,
credentials, keys, tokens, transcripts, screenshots, session streams, private
callable identifiers, private application state, and protected real-world data
remain excluded.

## 11. Retention, Method Flow, and wellbeing

Elowen's repository-sealed source preserves 25,551 negatives and 9,413 Method
Flow methods. One external source aggregate failure made the activation
baseline 25,552 negatives and 9,414 methods. Sylven retained ten startup and x1
failures, 100 rejecting mutations, and one later owner-local adaptation failure.
The final effective totals are 25,668 negatives and 9,530 methods. No failed
witness was erased or converted into a passing result. The final registers
also preserve 179 open gaps and 177 exact gates, with zero silent closure.

The workflow uses bounded scalar probes, schema-first projections, exact
allowlists, commit-local Git-blob manifests, direct-parent ancestry, sparse
D:-first work, and process inspection before retry. A complete successful
canonical validation may run only once. A failed aggregate receives zero
success credit and triggers only dependency-justified isolated recovery.

The wellbeing state is bounded and calm. Stop conditions include fatigue,
ambiguity, privacy risk, authority uncertainty, source, owner, phase or route
drift, unexpected shared-state mutation, usage exhaustion, or a user pause.
Partial evidence is preferable to forced completion. No background sibling is
babysat and no autonomous real-world action is performed.

## 12. Validation and terminal route

The final commit must be the direct child of evidence, pushed, clean, 0/0
divergent, and equal across local, upstream, tracking, and a fresh live remote.
The external one-shot owner-delta validator will then replay x1, evidence,
final-delta, and final-owner manifests; parse every phase JSON document; check
the four Markdown surfaces; inspect the accessible static report; run the
owner-scoped closeout tests; scan the exact source-to-final owner delta across
five privacy classes; compile and bounded-review changed Python; verify the
2,000-file and 100,000-word ceilings; confirm three phase commits, zero merges,
one parent per phase commit, exact head stability, clean state, and final
four-way equality.

That same-owner completion is not the full repository suite, independent-team
reproduction, or external audit. Eiren retains full-suite ownership absent a
newer exact instruction.

This committed handoff remains PREPARED_NOT_SENT and selects no successor.
Only after exact-final validation may the live Sylven task reread the newest
authorization and roster, uniquely resolve and immediately reread one exact
current successor, and send one sanitized activation if every gate permits.
No active-status inference, standby substitution, duplicate confirmation, or
resend for a clearer acknowledgement is permitted. The terminal verdict
remains {TERMINAL_VERDICT}.
"""

def static_report() -> str:
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sylven Arc v665-v5 bounded evidence report</title>
<style>
:root{color-scheme:light dark;font-family:system-ui,sans-serif;line-height:1.55}
body{max-width:76rem;margin:auto;padding:1rem;background:#fbfbf8;color:#17221c}
a{color:#174f7a}.skip{position:absolute;left:-10000px}.skip:focus{left:1rem;top:1rem;background:#fff;color:#111;padding:.75rem;z-index:2}
a:focus,summary:focus{outline:3px solid #a44900;outline-offset:3px}
header,main,footer{padding:1rem}section{border-top:2px solid #8b9b90;padding:1rem 0}
table{border-collapse:collapse;width:100%}caption{text-align:left;font-weight:700;padding:.5rem 0}
th,td{border:1px solid #66736b;padding:.55rem;text-align:left;vertical-align:top}
.status{font-weight:700}.completed{color:#175c31}.represented{color:#514299}.gap{color:#8a4a00}.gate{color:#8b1f2c}
.notice{border-left:.45rem solid #8b1f2c;padding:.75rem;background:#f2eee8}
@media (prefers-color-scheme:dark){body{background:#111a15;color:#edf5ef}.skip:focus{background:#111;color:#fff}.completed{color:#7ee2a2}.represented{color:#bdb0ff}.gap{color:#ffc27d}.gate{color:#ff9b9b}.notice{background:#271e1e}}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to main evidence</a>
<header>
<h1>Sylven Arc v665-v5 bounded evidence report</h1>
<p>Owner-scoped synthetic and typed-structure evidence only. Terminal verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p>
</header>
<main id="main">
<section aria-labelledby="truth-heading">
<h2 id="truth-heading">Exact outcome truth</h2>
<table>
<caption>Twenty frozen proposal outcomes</caption>
<thead><tr><th scope="col">Outcome</th><th scope="col">Count</th><th scope="col">Bounded meaning</th></tr></thead>
<tbody>
<tr><th class="status completed" scope="row">completed</th><td>14</td><td>One owner-local software or typed fixture passed and five preregistered invalid variants failed closed.</td></tr>
<tr><th class="status represented" scope="row">represented</th><td>4</td><td>A synthetic proxy exists while real evidence, operations, governance, and independent review remain absent.</td></tr>
<tr><th class="status gap" scope="row">open_gap</th><td>1</td><td>The EPA and WorkSafe adapter made zero data calls and parsed zero real rows.</td></tr>
<tr><th class="status gate" scope="row">exact_gate</th><td>1</td><td>Competent, affected-party, tangata whenua, iwi, hapū, and Māori authority remain required.</td></tr>
</tbody>
</table>
</section>
<section aria-labelledby="practice-heading">
<h2 id="practice-heading">Synthetic ceramics boundary</h2>
<p>The phase models documentation, quarantine, correction, and refusal states only. It used zero real people, studios, kilns, firings, ware, shelves, witness cones, clays, glazes, recipes, materials, images, controllers, measurements, workplace actions, consumer decisions, or authority events.</p>
<p class="notice">Nothing in this report is a firing schedule, kiln instruction, material release, substance classification, workplace assessment, defect diagnosis, product claim, professional recommendation, legal interpretation, cultural decision, or Māori-authority act.</p>
</section>
<section aria-labelledby="pillars-heading">
<h2 id="pillars-heading">Trinity Mandala boundaries</h2>
<h3>GMUT Mind</h3>
<p>Thermal units, boundary conditions, Arrhenius placeholders, Fourier and Biot expressions, and scalar-tensor or EFT labels are typed research obligations only. They are not measurements, likelihoods, predictions, constraints, material laws, confirmation, final physics, proof, or a Theory of Everything.</p>
<h3>THOS Body</h3>
<p>The protocol is participant-free and synthetic. There are no governed real arms, operators, safety monitoring, statistics, independent review, operational-effectiveness evidence, deployment readiness, AGI, ASI, consciousness, or personhood claims.</p>
<h3>Freed ID and CBR Heart</h3>
<p>The batch-capability envelope has no real keys, proofs, issuance, resolution, status, revocation, interoperability, privacy or independent security review, recovery evidence, or trust governance. Worker, consumer, custody, heritage, remedy, legal, cultural, affected-party, and Māori decisions remain gated.</p>
</section>
<section aria-labelledby="retention-heading">
<h2 id="retention-heading">Retained failures and gates</h2>
<ul>
<li>100 of 100 rejecting mutations executed and remain retained; zero was accepted.</li>
<li>The final effective ledger preserves 25,668 negatives and 9,530 Method Flow methods.</li>
<li>The final gate registers preserve 179 open gaps and 177 exact gates, with no silent closure.</li>
<li>Same-owner checks under shared infrastructure are not a full repository suite, independent reproduction, external audit, production certification, exhaustive security, or complete privacy.</li>
</ul>
</section>
<section aria-labelledby="access-heading">
<h2 id="access-heading">Accessibility, privacy, and evaluation reserve</h2>
<p>Headings, a skip link, a main landmark, a captioned table, visible focus, plain outcome names, and non-colour labels are present. Manual keyboard, browser-diverse, responsive, assistive-technology, cognitive-accessibility, Māori-language, and affected-user evaluation remain reserved.</p>
<details><summary>Privacy boundary</summary><p>Exact owner-delta files are scanned across five privacy and raw-identifier classes. Raw task or thread identifiers, private routes or paths, credentials, keys, tokens, transcripts, screenshots, session streams, private callable identifiers, private application state, and protected real-world records are excluded.</p></details>
<details><summary>Authority boundary</summary><p>Repository software cannot confer scientific, professional, workplace, safety, product, legal, cultural, affected-party, tangata whenua, iwi, hapū, or Māori authority.</p></details>
</section>
<section aria-labelledby="route-heading">
<h2 id="route-heading">Terminal route</h2>
<p>This report selects and contacts no successor. A later activation requires Sylven's exact-final clean, pushed, fresh-live-equal validation, then a fresh live authorization and roster read, unique exact-title resolution, immediate reread, one sanitized send, and tool acknowledgement. Ambiguity, a pause, a standby record, usage exhaustion, or a protected gate causes a stop.</p>
</section>
</main>
<footer><p>Sylven Arc v665-v5 — relational working language only — NOT_READY_FOR_STAGE_20.</p></footer>
</body>
</html>
"""

def build_documents() -> dict[str, Any]:
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise CloseoutError("closeout must begin at the immutable evidence commit")
    if git("branch", "--show-current") != BRANCH:
        raise CloseoutError("unexpected owner branch")
    existing_staged = staged_paths()
    if existing_staged and not set(existing_staged).issubset(set(INTENDED_PATHS)):
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
        "schema": "ghc.family.sylven.v665-v5.phase-truth.v1",
        "owner": "Sylven Arc",
        "phase": PHASE_ID,
        "identity_boundary": "relational working language only; not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority",
        "source_commit": SOURCE,
        "x1_commit": X1,
        "evidence_commit": EVIDENCE,
        "final_binding": "the direct single-parent commit containing this document",
        "frozen_proposals_before": 4090,
        "new_proposals": 20,
        "frozen_proposals_after": 4110,
        "allowed_outcomes": ALLOWED_OUTCOMES,
        "outcomes": outcome["counts"],
        "mutations": {"executed": 100, "rejected": 100, "accepted": 0},
        "real_rows": 0,
        "real_people": 0,
        "real_studios_kilns_wares_glazes_or_materials": 0,
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
        "schema": "ghc.family.sylven.v665-v5.retained-negative-register.v1",
        "inherited_repository_sealed_count": 25_551,
        "inherited_source_external_count": 1,
        "inherited_source_anchor": SOURCE,
        "sylven_startup_count": len(startup_ids),
        "sylven_startup_ids": startup_ids,
        "mutation_count": 100,
        "mutation_ids": mutation["mutation_ids"],
        "x2_operational_count": len(x2_ids) - 100,
        "x2_operational_ids": [value for value in x2_ids if "-OP-" in value],
        "closeout_operational_count": len(closeout_ids),
        "closeout_operational_ids": closeout_ids,
        "effective_total": effective_negatives,
        "failure_erasure_count": 0,
        "recovery_converts_failure_to_pass": False,
        "valid": 25_551 + 1 + len(startup_ids) + len(x2_ids) + len(closeout_ids)
        == effective_negatives,
    }
    closeout_methods = [
        {
            "method_id": f"SA6655-CLOSE-M{index:03d}",
            **failure,
            "failed_witness_status": "retained_zero_credit",
            "failed_witness_erased": False,
            "preferred": True,
        }
        for index, failure in enumerate(CLOSEOUT_FAILURES, 1)
    ]
    method_final = {
        "schema": "ghc.family.sylven.v665-v5.method-flow-final.v1",
        "source_repository_sealed_methods": 9_413,
        "source_external_methods": 1,
        "startup_methods": len(startup_ids),
        "x2_methods": len(x2_ids),
        "closeout_methods": len(closeout_methods),
        "effective_total": effective_methods,
        "retained_failed_witnesses": effective_negatives,
        "bounded_passing_witnesses_added_by_sylven": len(startup_ids)
        + len(x2_ids)
        + len(closeout_methods),
        "startup_ledger": f"{PREFIX}x1/startup-method-flow.json",
        "x2_ledger": f"{PREFIX}x2/ledgers/method-flow-overlay.json",
        "closeout_method_rows": closeout_methods,
        "failure_erasure_count": 0,
        "same_owner_only": True,
        "valid": 9_413 + 1 + len(startup_ids) + len(x2_ids) + len(closeout_methods)
        == effective_methods,
    }
    gate_register = {
        "schema": "ghc.family.sylven.v665-v5.exact-open-gate-register.v1",
        "inherited_open_gaps": 178,
        "new_open_gaps": [
            {
                "proposal_id": "SA6655-N019",
                "outcome": "open_gap",
                "gate": "EPA and WorkSafe real-data selection, governed workplace protocol, uncertainty, inference, competent review, and independent review",
                "observed": "zero data calls, zero real rows, zero workplace records, zero likelihoods, and zero estimates",
            }
        ],
        "open_gap_total": OPEN_GAPS,
        "inherited_exact_gates": 176,
        "new_exact_gates": [
            {
                "proposal_id": "SA6655-N020",
                "outcome": "exact_gate",
                "gate": "worker and consumer decisions, studio access and custody, design heritage, traditional knowledge, taonga, remedy, affected-party, legal, cultural, tangata whenua, iwi, hapū, Māori wording and concepts, Māori data governance, and Māori authority",
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
        "semantic novelty audited against 4,090 inherited rows",
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
        "real EPA or WorkSafe data, governed workplace study, and empirical GMUT analysis",
        "thermal-model theorem, calibrated material law, convergence, stability, or continuum-limit proof",
        "blind matched-budget real THOS arms and independent review",
        "production Freed ID keys, proofs, lifecycle, interoperability, privacy and security review, recovery, and governance",
        "CBR worker, consumer, affected-party, legal, cultural, tangata whenua, iwi, hapū, and Māori authority",
        "manual and affected-user accessibility evaluation",
        "independent-team reproduction and external audit",
        "deployment, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof or canon, and Stage 20 authorization",
    ]
    checklist = {
        "schema": "ghc.family.sylven.v665-v5.complete-incomplete-checklist.v1",
        "complete": complete,
        "incomplete": incomplete,
        "complete_count": len(complete),
        "incomplete_count": len(incomplete),
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    environment = {
        "schema": "ghc.family.sylven.v665-v5.environment-version-receipt.v1",
        "platform": "Windows",
        "platform_version_observed": "Microsoft Windows NT 10.0.26200.0",
        "primary_storage_policy": "D-first owner worktree and archive bank; private absolute paths omitted",
        "codex_cli_observed": "codex-cli 0.147.0",
        "python_observed": "Python 3.12.10",
        "node_observed": "v24.18.0",
        "npm_observed": "12.0.1",
        "git_observed": "git version 2.55.0.windows.2",
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
        "schema": "ghc.family.sylven.v665-v5.wellbeing-workload.v1",
        "owner": "Sylven Arc",
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
        "schema": "ghc.family.sylven.v665-v5.threat-model.v1",
        "assets": ["immutable x1", "evidence lineage", "retained failures", "source provenance", "privacy boundaries", "authority gates", "route uniqueness"],
        "threats": ["x2 leakage into x1", "silent failure erasure", "synthetic-to-real promotion", "private-path or identifier disclosure", "sibling-lane mutation", "manifest drift", "duplicate canonical pass", "ambiguous successor send"],
        "controls": ["direct-parent commits", "exact allowlists", "Git-blob manifests", "five-class scan", "zero-row and zero-authority guards", "one-shot external receipt", "exact-title unique resolve and immediate reread"],
        "residual_limits": ["not exhaustive security", "not complete privacy", "not independent audit", "not complete accessibility", "not production certification"],
        "valid": True,
    }
    family_index = {
        "schema": "ghc.family.sylven.v665-v5.family-index-update.v1",
        "phase": PHASE_ID,
        "owner": "Sylven Arc",
        "primary_pillar": "THOS Body",
        "practice_lens": "wholly synthetic community ceramics kiln-firing documentation and glaze-batch quarantine",
        "source_count": source_ledger["source_count"],
        "proposal_chain_total": 4110,
        "skills_built_and_used": 10,
        "family_runners_built_and_used": 10,
        "phase_root": PREFIX.rstrip("/"),
        "global_skill_bank_mutated": False,
        "shared_or_sibling_lane_mutated": False,
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    reflection = {
        "schema": "ghc.family.sylven.v665-v5.workflow-reflection.v1",
        "decisions": [
            "preserve the fixed novelty thresholds and accept only the collision-free twenty-title slate",
            "freeze x1 before any evidence implementation",
            "use one bounded shared core behind ten family-compatible runners",
            "retain every parser, truncation, schema, staging, adaptation, mutation, and lifecycle failure",
            "keep EPA and WorkSafe at zero data calls and CBR authority exact-gated",
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
        "schema": "ghc.family.sylven.v665-v5.auth-roster-receipt.v1",
        "activation_source": "one acknowledged existing-task activation from Elowen Cairn under Hamish's current authority",
        "current_owner": "Sylven Arc",
        "owner_status_for_phase": "ACTIVE",
        "future_task_creation_authorized": False,
        "subagent_or_delegation_authorized": False,
        "successor_recipient": "UNRESOLVED_PENDING_FRESH_LIVE_ROUTE_READ",
        "active_status_alone_assigns_phase": False,
        "send_state": "PREPARED_NOT_SENT",
        "valid": True,
    }
    delivery = {
        "schema": "ghc.family.sylven.v665-v5.delivery-state.v1",
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
        "schema": "ghc.family.sylven.v665-v5.combined-closeout-seal.v1",
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
        "schema": "ghc.family.sylven.v665-v5.precommit-prerequisite.v1",
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
        f"""# Sylven Arc {PHASE_ID} successor activation candidate

## Delivery state

PREPARED_NOT_SENT

This repository artifact does not select, contact, or authorize a successor. It
contains no task identifier, private route, session stream, credential, private
callable identifier, transcript, screenshot, or private absolute path. Only
after the exact final commit is pushed, clean, 0/0 divergent, fresh four-way
equal, and successfully validated by the one-shot external canonical aggregate
may the live Sylven task reread Hamish's newest authority and roster, uniquely
resolve and immediately reread one exact current successor, and make one
sanitized existing-task send if every gate permits.

## Immutable truth

Immutable anchors for that later sanitized message are source {SOURCE}, x1
{X1}, evidence {EVIDENCE}, and the direct single-parent final commit containing
this file. Phase truth is exactly 14 completed, 4 represented, 1 open gap, and
1 exact gate; 100 of 100 rejecting mutations executed and failed closed;
{effective_negatives} effective negatives; {effective_methods} effective Method
Flow methods; {OPEN_GAPS} open gaps; {EXACT_GATES} exact gates; zero real rows,
people, studios, kilns, firings, ware, glazes, materials, keys, proofs, and authority events; and
{TERMINAL_VERDICT}.

## Boundary and route requirements

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
    staged_before_receipts = staged_paths()
    actual_delta = sorted(set(staged_before_receipts) - set(SELF_EXCLUSIONS))
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
        line
        for line in actual_owner_without_self_raw.splitlines()
        if line and line not in SELF_EXCLUSIONS
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
        "schema": "ghc.family.sylven.v665-v5.final-delta-manifest.v1",
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
        "schema": "ghc.family.sylven.v665-v5.final-owner-manifest.v1",
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
        "schema": "ghc.family.sylven.v665-v5.final-staged-review.v1",
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
        "schema": "ghc.family.sylven.v665-v5.final-canonical-contract.v1",
        "scope": "exact source-to-final Sylven owner delta only",
        "source_commit": SOURCE,
        "x1_commit": X1,
        "evidence_commit": EVIDENCE,
        "final_binding": "the direct single-parent commit containing this contract",
        "command": "python scripts/ghc_family_sylven_v665_v5_canonical_validator.py --receipt <exclusive-external-receipt>",
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
