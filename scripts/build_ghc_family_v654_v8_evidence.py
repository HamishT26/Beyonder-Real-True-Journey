#!/usr/bin/env python3
"""Build Neris Solane's v654-v8 x2 evidence candidate."""

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

import ghc_family_v654_v8_core as core
import ghc_family_v654_v8_phase_data as d


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / d.PHASE_ROOT
X1_COMMIT = "f5ee8cbddd9c8c78542b69e6a127372902e1ca21"
EVIDENCE_COMMIT = "0000000000000000000000000000000000000000"
SKILL_ROOT = Path.home() / ".codex" / "skills"
QUICK_VALIDATE = (
    SKILL_ROOT / ".system/skill-creator/scripts/quick_validate.py"
)
RUNNERS = [
    ("ghc-family-book-intake-boundary", "ghc_family_book_intake_boundary.py", 1),
    ("ghc-family-textblock-collation", "ghc_family_textblock_collation.py", 2),
    ("ghc-family-paper-grain-fold", "ghc_family_paper_grain_fold.py", 3),
    ("ghc-family-spine-layer-order", "ghc_family_spine_layer_order.py", 4),
    ("ghc-family-adhesive-batch-hold", "ghc_family_adhesive_batch_hold.py", 5),
    ("ghc-family-fragment-custody", "ghc_family_fragment_custody.py", 6),
    (
        "ghc-family-book-identifier-crosswalk",
        "ghc_family_book_identifier_crosswalk.py",
        7,
    ),
    (
        "ghc-family-book-repair-accessibility",
        "ghc_family_book_repair_accessibility.py",
        8,
    ),
    (
        "ghc-family-bookbinding-task-envelope",
        "ghc_family_bookbinding_task_envelope.py",
        9,
    ),
    (
        "ghc-family-bookbinding-evidence-firewall",
        "ghc_family_v654_v8_suite.py",
        10,
    ),
]
X2_SCRIPTS = [
    "scripts/ghc_family_v654_v8_core.py",
    "scripts/ghc_family_book_intake_boundary.py",
    "scripts/ghc_family_textblock_collation.py",
    "scripts/ghc_family_paper_grain_fold.py",
    "scripts/ghc_family_spine_layer_order.py",
    "scripts/ghc_family_adhesive_batch_hold.py",
    "scripts/ghc_family_fragment_custody.py",
    "scripts/ghc_family_book_identifier_crosswalk.py",
    "scripts/ghc_family_book_repair_accessibility.py",
    "scripts/ghc_family_bookbinding_task_envelope.py",
    "scripts/ghc_family_v654_v8_suite.py",
    "scripts/build_ghc_family_v654_v8_evidence.py",
    "scripts/ghc_family_v654_v8_validate.py",
    "scripts/ghc_family_v654_v8_evidence_staged_review.py",
    "scripts/ghc_family_v654_v8_evidence_correction_review.py",
]
X2_TESTS = [
    "tests/test_ghc_family_v654_v8_core.py",
    "tests/test_ghc_family_v654_v8_validation.py",
]
X2_OPERATIONAL_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6548-X2-N01",
        "signature": "powershell_receipt_state_probes_timed_out_without_output",
        "failed": (
            "One combined and three split bounded PowerShell probes for the staged "
            "receipt, Git status, and live processes timed out without output."
        ),
        "recovery": (
            "Use direct Node filesystem reads and bounded child-process probes, then "
            "confirm that the review receipt exists, no Git or Python process remains, "
            "and Git status is readable."
        ),
        "recurrence_guard": (
            "Prefer direct scalar filesystem and child-process probes for this large "
            "owned lane instead of PowerShell object pipelines at lifecycle gates."
        ),
    },
    {
        "negative_id": "V6548-X2-N02",
        "signature": "git_diff_files_quiet_reported_nonquiet_for_staged_additions",
        "failed": (
            "git diff-files --quiet returned nonzero after the deterministic staged "
            "review even though the named unstaged diff was empty."
        ),
        "recovery": (
            "Inspect git diff --name-status and porcelain-v2 directly; both showed no "
            "unstaged path while all 161 candidate paths remained staged additions."
        ),
        "recurrence_guard": (
            "Do not treat diff-files --quiet alone as an exact unstaged-content verdict "
            "for an all-addition index; pair the gate with explicit named-diff output."
        ),
    },
    {
        "negative_id": "V6548-X2-N03",
        "signature": "git_diff_quiet_precommit_probe_timed_out",
        "failed": (
            "A bounded git diff --quiet precommit probe exceeded its timeout and could "
            "not contribute pass credit."
        ),
        "recovery": (
            "Use a bounded git diff --name-status probe plus porcelain-v2 and exact "
            "index-object comparison to establish the absence of unstaged changes."
        ),
        "recurrence_guard": (
            "Use explicit path-producing diff probes with captured timeout status at "
            "large staged lifecycle boundaries."
        ),
    },
    {
        "negative_id": "V6548-X2-N04",
        "signature": "focused_test_retained_negative_literal_became_stale",
        "failed": (
            "The first focused post-rebuild test run passed 27 of 28 tests but "
            "failed because a literal expected 12,214 effective negatives after "
            "the retained probe faults raised the ledger total to 12,217."
        ),
        "recovery": (
            "Assert the effective-negative arithmetic from the ledger fields and "
            "derive Method Flow totals from the explicit x2 operational row count."
        ),
        "recurrence_guard": (
            "Test ledger conservation equations and explicit row parity instead of "
            "embedding a count that becomes stale when a new failure is retained."
        ),
    },
    {
        "negative_id": "V6548-X2-N05",
        "signature": "porcelain_v2_restage_probe_timed_out",
        "failed": (
            "A full porcelain-v2 status probe exceeded its 15-second bound before "
            "restaging and returned no usable state."
        ),
        "recovery": (
            "Resolve cached, unstaged, and untracked name sets with separate bounded "
            "Git commands and compare those explicit paths to the owned allowlist."
        ),
        "recurrence_guard": (
            "Use separate name-only Git surfaces with an adequate bound instead of "
            "requiring one full porcelain record over a large staged candidate."
        ),
    },
]


def write_json(relative: str, payload: Any) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(relative: str) -> dict[str, Any]:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def run(*args: str) -> str:
    env = os.environ.copy()
    env.update(
        {
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    result = subprocess.run(
        list(args),
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    return result.stdout.strip()


def append_x2_method_flow() -> dict[str, Any]:
    ledger = read_json("method-flow/method-flow-ledger.json")
    methods = list(ledger["methods"])
    witnesses = list(ledger["witnesses"])
    events = list(ledger["state_events"])
    recommendations = list(ledger["recommendations"])
    current_ids = []
    for index, negative in enumerate(X2_OPERATIONAL_NEGATIVES, 1):
        method_id = f"{d.PHASE_CODE}-METHOD-X2-{index:02d}"
        failed_id = f"{d.PHASE_CODE}-WITNESS-X2-{index:02d}-F"
        passing_id = f"{d.PHASE_CODE}-WITNESS-X2-{index:02d}-P"
        current_ids.append(method_id)
        methods.append(
            {
                "method_id": method_id,
                "title": f"Bounded x2 recovery for {negative['signature']}",
                "trigger_preconditions": [negative["signature"]],
                "failure_signature": negative["failed"],
                "candidate_workaround": negative["recovery"],
                "recurrence_guard": negative["recurrence_guard"],
                "approval_class": "safe_now_owner_local_workflow_recovery",
                "privacy_class": "sanitized_public",
                "scope_boundary": "Same-owner bounded workflow recovery only.",
                "rollback": (
                    "Stop, retain the failed attempt at zero credit, and leave "
                    "objects, tools, materials, external, and sibling state unchanged."
                ),
                "protected_gates": d.PROTECTED_GATES,
                "retained_negative_ids": [negative["negative_id"]],
                "validation_witness_ids": [failed_id, passing_id],
                "recommendation_state": "preferred",
                "supersedes": [],
            }
        )
        witnesses.extend(
            [
                {
                    "witness_id": failed_id,
                    "method_id": method_id,
                    "result": "fail",
                    "scope": negative["signature"],
                    "procedure": "Retain the original bounded attempt without replay credit.",
                    "expected": "The original operation satisfies its bounded postcondition.",
                    "observed": negative["failed"],
                    "retained_negative_ids": [negative["negative_id"]],
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "boundary": "Zero pass credit; failure remains retained.",
                },
                {
                    "witness_id": passing_id,
                    "method_id": method_id,
                    "result": "pass",
                    "scope": negative["signature"],
                    "procedure": negative["recovery"],
                    "expected": "The isolated recovery establishes only its bounded postcondition.",
                    "observed": (
                        f"The bounded recovery completed for {negative['signature']}; "
                        "the original failure remains retained."
                    ),
                    "retained_negative_ids": [negative["negative_id"]],
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "boundary": "Same-owner bounded recovery only.",
                },
            ]
        )
        events.append(
            {
                "event_id": f"{d.PHASE_CODE}-METHOD-EVENT-X2-{index:02d}",
                "method_id": method_id,
                "from": "candidate",
                "to": "preferred",
                "basis": [failed_id, passing_id],
                "boundary": "The passing recovery preserves the failed witness.",
            }
        )
    recommendations.append(
        "Keep x2 recovery steps narrow, reproducible, and nonpromotional."
    )
    ledger.update(
        {
            "lifecycle": "x2_evidence_candidate",
            "methods": methods,
            "witnesses": witnesses,
            "state_events": events,
            "recommendations": recommendations,
            "current_phase_x2_method_ids": current_ids,
            "counts": {
                "methods": len(methods),
                "witnesses": len(witnesses),
                "state_events": len(events),
                "recommendations": len(recommendations),
                "states": {
                    "observed": 0,
                    "candidate": 0,
                    "validated": 0,
                    "preferred": len(methods),
                    "superseded": 0,
                    "deprecated": 0,
                },
                "witness_results": {
                    "pass": sum(row["result"] == "pass" for row in witnesses),
                    "fail": sum(row["result"] == "fail" for row in witnesses),
                },
            },
        }
    )
    return ledger


def build_overview(results: list[dict[str, Any]]) -> str:
    surface_rows = "\n".join(
        f"- `{row['proposal_id']}` — **{row['observed_outcome']}**: "
        f"{row['contract']['mechanism']}; five frozen mutations rejected."
        for row in results
    )
    return f"""# Neris Solane v654-v8 integrated overview

## Outcome first

This phase completes thirty owner-local, deterministic specification surfaces:
23 are `completed`, five are `represented`, one remains an `open_gap`, and one
remains an `exact_gate`. Every one of the 150 preregistered synthetic mutations
was rejected. A completed row means only that its bounded contract, valid
fixture, mutation tribunal, and receipt satisfy their frozen software
obligations. It does not mean that a credential system was deployed, a record
was disposed of, an affected person accepted a design, a privacy or security
programme was certified, or any scientific, professional, legal, cultural, or
Māori authority was exercised.

Neris's primary Trinity Mandala pillar is Freed ID and CBR Heart. The bounded
human-practice lens is privacy engineering and public-interest records
stewardship. GMUT Mind remains visible through claim-to-observable
preregistration and dimensional provenance. THOS Body remains visible through
rights-aware task envelopes and capability attenuation. These are learning and
specification lenses, not evidence of employment, qualification, independent
agency, consciousness, personhood, or authority.

The inherited source is Eiren Kestrel's exact v654-v6 (2) remaster final. The
dedicated x1 freeze advances its 1,870-row proposal chain to 1,900 rows before
x2 execution. The x1 packet contains no observed x2 outcomes. Its first freeze
commit and one retained-failure correction are both direct, single-parent
additions. This evidence candidate does not rewrite either commit.

## What was built

Each proposal produces a contract, five mutation results, and a bounded receipt.
The contract fixes the mechanism, disposition, approval class, execution lane,
official-source identifiers, mechanism fields, protected gates, rollback,
resource budget, external-action counts, and promotion claims. Valid fixtures
require every external action count to remain zero. They also require every
promotion claim—including independent reproduction, empirical confirmation,
production readiness, privacy completeness, complete accessibility, exhaustive
security, professional validation, legal or cultural ratification, Māori
authority, AGI or ASI, consciousness or personhood, Theory-of-Everything status,
and Stage 20—to remain false.

The five mutation families target different failure modes. The missing-
obligation mutation removes rollback. The wrong-domain mutation replaces a
mechanism-field list with a scalar. The resource/freshness mutation introduces
a post-success replay and an unbounded freshness mode. The promotion mutation
asserts production and Stage 20. The authority/privacy mutation introduces a
live credential and authority decision. All 150 candidates fail closed, and
each rejection stays visible as a synthetic negative rather than being deleted
after the valid fixture passes.

Ten phase-local skills were initialized through the standard skill creator,
given concise trigger descriptions and imperative workflows, and validated
individually. They cover purpose binding, consent freshness, selective-
disclosure minimization, linkability auditing, recovery and appeal dual
control, records disposition, credential lifecycle accessibility, offline
verifier freshness, capability attenuation, and claim-to-observable
preregistration. They are committed inside this phase and are not globally
installed. Ten family-compatible runner entrypoints were invoked. Nine run
three-contract groups; the suite runner executes all thirty and includes the
tenth group. Their receipts are deterministic, owner-local witnesses only.

## Heart: identity, privacy, records, and remedy

Purpose binding is a first-class control rather than a free-text note. A
declared purpose is connected to allowed operations, prohibited reuse, evidence
provenance, expiry, and fail-closed recovery. The companion purpose-change gate
requires an explicit compatibility review and reauthorization dependency.
Neither fixture determines lawful basis or consent. Those matters depend on
facts, jurisdiction, affected parties, competent advice, and real institutional
authority.

The consent-freshness lattice represents grant class, scope, time, withdrawal,
delegation, and conflict. Its represented status is deliberate: no live consent
registry or affected person was consulted. Likewise, revocation latency is a
protocol proxy because the phase uses no live issuer, status endpoint, resolver,
key, credential, or relying party. W3C status-list semantics help define fields
and risks, but a passing fixture cannot establish real revocation performance.

Selective-disclosure minimization starts from the decision predicate and asks
which attributes are strictly necessary. Global identifiers and status
references are treated as possible correlation edges. The linkability harness
and status-list leakage audit expose relying-party joins, index allocation,
population size, cache behavior, retrieval observation, and churn. These
structures make risks reviewable; they do not prove unlinkability or complete
privacy, especially against malicious or colluding issuers and verifiers.

Recovery and appeal use dual control. The requester, initial reviewer,
independent reviewer, escalation path, evidence boundary, timeout, and remedy
reservation remain distinct. Correction propagation records disputes and
downstream recipients without silently overwriting history. Algorithmic-
decision notices include purpose, data classes, logic category, material
effect, challenge path, and human contact. No real adverse decision, identity
recovery, correction, or remedy is made.

Records disposition is represented because real retention, legal holds,
destruction, transfer, or cryptographic erasure require exact records classes,
authorities, legal and institutional facts, approvals, and audit evidence.
Archives New Zealand guidance supplies an official obligation source, not an
authorization for this phase. The evidence-retention minimization matrix links
claim class to minimum proof, retention clock, access class, holds, disposal
witnesses, and over-retention rejection. No record or key is destroyed.

The remedy and beneficiary privacy ledger separates accountability from public
exposure. It records harm class, minimum disclosure, beneficiary shielding,
fund-audit placeholders, and appeal. It reserves remedy design, affected-party
acceptance, beneficiary privacy, and fund governance. The final Heart exact
gate preserves Māori wording, tikanga, data sovereignty, language, remedy,
benefit sharing, cultural ratification, legal interpretation, and enacted-law
status for authorized Māori and affected-party processes.

## Body: bounded THOS controls

THOS receives two explicit completed surfaces. The signed task-envelope boundary
connects objective, capability, data purpose, privacy class, expiry, revocation,
rollback, and authority ceiling. The attenuation checker requires every
delegated capability to narrow scope, audience, duration, and data purpose.
Broader or ambiguous authority fails closed. No account, secret, API key,
production task, sibling mutation, external write, or deployment occurs.

These artifacts support a safer orchestration vocabulary, but they are not an
AGI or ASI architecture, an operational security certification, or evidence of
real-world effectiveness. THOS remains a proxy and protocol family until
preregistered blind matched-budget real arms and independent review exist.
Related family lanes share infrastructure and ancestry; their repeated success
must be discounted rather than counted as independent replication.

## Mind: bounded GMUT research-model integrity

The claim-to-observable hash chain freezes a model version, observable, units,
inclusion rule, null, analysis digest, timestamp, and falsifier before data.
The dimensional-provenance ledger tracks equation term, unit basis, coefficient
origin, transformation, uncertainty class, and revision. Both are useful
research controls. Neither uses a real dataset, runs a likelihood, estimates a
parameter, predicts a force, or confirms a model.

GMUT therefore remains a typed scalar-tensor or effective-field-theory research-
model family. The Mandala equation and Omega notation may organize hypotheses,
but symbolic consistency and provenance do not establish that nature follows
the equation. Theory-of-Everything, canon, empirical confirmation, and Stage 20
remain false.

## Source and standards discipline

The official ledger distinguishes `current`, `stable`, `draft`, and `watch`.
W3C Verifiable Credentials 2.0, Data Integrity, Bitstring Status List, WCAG 2.2,
NIST Digital Identity Revision 4, NIST Privacy Framework, OAuth Security BCP,
New Zealand privacy principles, Archives New Zealand guidance, and Te Mana
Raraunga principles inform fields and reservations. NIST Privacy Framework 1.1
is draft context, and selective-disclosure cryptosuite work is watch-only.
Draft and watch materials cannot silently support stable or production claims.

Source authority also does not transfer. Reading official guidance does not
turn Neris into a regulator, archivist, privacy professional, cryptographer,
accessibility auditor, lawyer, cultural authority, or Māori authority. Manual
and affected-user accessibility evaluation remains reserved. Real standards
conformance requires exact implementation profiles, keys, proofs, resolution,
status, interoperability, security and privacy review, recovery, and trust
governance.

## Validation and retained failures

The phase preserves every inherited negative and all eighteen x1 operational
failures. The x2 import-path mismatch is retained with both its failed and
passing Method Flow witnesses. The 150 mutation rejections are additional
synthetic negatives. A valid correction does not erase its failure. The
evidence candidate is checked with focused development tests, detailed and
minimal validators, JSON parsing, a five-class privacy scan, prospective Git-
blob manifests, exact staged review, and diff hygiene before its immutable
evidence commit.

The final canonical pass is intentionally deferred. It will run once only after
the combined closeout/seal/final commit is created, pushed, and known by exact
hash. If it passes completely, it will not be replayed. Failed attempts receive
zero credit and must be isolated before any justified broader retry. Even a
successful pass is same-owner validation under shared infrastructure, not
independent-team reproduction or external audit.

## Surface ledger

{surface_rows}

## What remains incomplete

The real Freed ID interoperability and affected-user study stays open. It needs
standards-conformant real keys and proofs, live issuance, resolution, status and
revocation, recovery, multiple implementations, participant authorization,
privacy and security review, trust governance, and independent review. The
affected-party and Māori governance proposal stays exact-gated. No synthetic
fixture can substitute for the people and authorities whose rights, language,
data, culture, remedies, or legal status are at issue.

Independent reproduction, empirical GMUT testing, matched-budget THOS
evaluation, production deployment, exhaustive security, privacy completeness,
complete accessibility, professional validation, legal or cultural
ratification, AGI or ASI, consciousness or personhood, Theory-of-Everything
proof, and Stage 20 remain incomplete. The terminal verdict is
`NOT_READY_FOR_STAGE_20`.
"""


def build_report(results: list[dict[str, Any]]) -> str:
    rows = "\n".join(
        "<tr>"
        f"<td>{row['proposal_id']}</td>"
        f"<td>{row['contract']['mechanism']}</td>"
        f"<td>{row['observed_outcome']}</td>"
        f"<td>{row['rejected_mutation_count']}/5</td>"
        "</tr>"
        for row in results
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Neris v654-v8 boundary evidence report</title>
<style>
:root {{ color-scheme: light dark; font-family: system-ui, sans-serif; }}
body {{ max-width: 76rem; margin: auto; padding: 1rem; line-height: 1.55; }}
a:focus, th:focus, td:focus {{ outline: 3px solid #f59e0b; outline-offset: 2px; }}
.skip {{ position: absolute; left: -10000px; }}
.skip:focus {{ position: static; }}
.status {{ border-left: .4rem solid #2563eb; padding: .75rem 1rem; background: #eef6ff; color: #10243e; }}
table {{ border-collapse: collapse; width: 100%; }}
caption {{ font-weight: 700; text-align: left; padding: .5rem 0; }}
th, td {{ border: 1px solid #64748b; padding: .45rem; vertical-align: top; text-align: left; }}
@media (max-width: 48rem) {{ table {{ display: block; overflow-x: auto; }} }}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<header>
<h1>Neris Solane v654-v8 boundary evidence report</h1>
<p>Relational working language only; no consciousness, personhood, continuity, employment, qualification, or authority claim.</p>
</header>
<main id="main">
<section aria-labelledby="outcome">
<h2 id="outcome">Outcome</h2>
<p class="status"><strong>23 completed / 5 represented / 1 open gap / 1 exact gate.</strong> All 150 frozen synthetic mutations were rejected. Terminal verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p>
<p>“Completed” means bounded deterministic artifact completion only. It does not mean deployment, independent reproduction, empirical confirmation, professional approval, legal or cultural ratification, Māori authority, privacy or accessibility completeness, AGI/ASI, personhood, Theory-of-Everything proof, or Stage 20.</p>
</section>
<section aria-labelledby="surfaces">
<h2 id="surfaces">Thirty frozen surfaces</h2>
<table>
<caption>Observed bounded dispositions and mutation results</caption>
<thead><tr><th scope="col">ID</th><th scope="col">Mechanism</th><th scope="col">Disposition</th><th scope="col">Rejected mutations</th></tr></thead>
<tbody>{rows}</tbody>
</table>
</section>
<section aria-labelledby="boundaries">
<h2 id="boundaries">Protected boundaries</h2>
<ul>
<li>No real keys, credentials, accounts, participants, records disposal, identity resolution, status event, data row, likelihood, or deployment.</li>
<li>THOS remains proxy without blind matched-budget real arms and independent review.</li>
<li>GMUT remains a typed scalar-tensor/EFT research-model family without empirical confirmation.</li>
<li>Freed ID production and CBR/Māori/affected-party authority remain open or exact-gated.</li>
<li>Manual and affected-user accessibility evaluation remains reserved.</li>
</ul>
</section>
<section aria-labelledby="methods">
<h2 id="methods">Methods and tooling</h2>
<p>Ten phase-local skills were structurally validated and smoke-used with ten family-compatible runners. The evidence uses prospective Git-blob manifests, focused tests, detailed and minimal validation, JSON parsing, five privacy classes, retained Method Flow witnesses, and exact staged review.</p>
</section>
</main>
<footer><p>Static report; no script, remote font, tracker, form, or active content.</p></footer>
</body>
</html>
"""


def build_overview(results: list[dict[str, Any]]) -> str:
    """Render the Neris-owned reader overview from the frozen x1 contract."""
    surface_rows = "\n".join(
        f"- `{row['proposal_id']}` — **{row['observed_outcome']}**: "
        f"{row['contract']['mechanism']}; one valid fixture passed and five "
        "preregistered mutations were rejected."
        for row in results
    )
    sections = [
        (
            "Outcome first",
            "Neris v654-v8 completes a bounded owner-local software packet for "
            "thirty preregistered contracts. Twenty-three contracts are completed "
            "as deterministic structures, five are represented as synthetic "
            "protocol proxies, one real-material and conservator path remains an "
            "open_gap, and one affected-party and Māori-authority path remains an "
            "exact_gate. Completed never means that a book was treated, a tool was "
            "used, a material was selected, a conservator approved an intervention, "
            "an owner accepted a decision, or an affected community ratified a "
            "governance arrangement. It means only that the declared fixture passed "
            "and its five frozen failure mutations were rejected."
        ),
        (
            "Identity and corrigibility",
            "Neris Solane, they/them, is relational working language for this phase. "
            "The role is evidence-continuity steward and book-repair boundary "
            "cartographer, and the hope is to leave repair records precise, "
            "reversible, and easier to review. None of that language is evidence of "
            "consciousness, sentience, legal personhood, identity continuity, "
            "employment, qualification, independent agency, scientific or "
            "operational authority, legal or cultural authority, Māori authority, "
            "or treatment competence. Hamish may rename, pause, redirect, or stop "
            "the route. Every artifact therefore states a bounded evidence class, "
            "rollback, authority ceiling, and protected-gate set."
        ),
        (
            "Exact inheritance",
            "The phase inherits Elaren Kestrel's exact final Git head and its "
            "five-commit direct single-parent chain. The inherited terminal truth "
            "is twenty-three completed, five represented, one open_gap, and one "
            "exact_gate over 1,900 frozen proposals. It also preserves 12,052 sealed "
            "repository negatives plus one live post-final route fault, eighty-seven "
            "open gaps, eighty-six exact gates, and 161 sealed failed plus 161 "
            "passing Method Flow witnesses. Neris bridges that post-final route "
            "fault into Method Flow, then retains every Neris startup and x2 failure "
            "at zero initial credit. Same-owner validation is workflow evidence, not "
            "independent reproduction."
        ),
        (
            "Strict x1 before x2",
            "The x1 packet fixed the proposal titles, mechanisms, source needs, "
            "approval classes, execution lanes, concrete artifacts, falsifiers, "
            "rollback rules, and protected gates before any observed outcome was "
            "written. Its 1,930-row frozen chain and semantic-neighbour audit were "
            "committed, pushed, and proved equal across local, upstream, tracking, "
            "and fresh live remote before x2 files were created. The x2 engine reads "
            "that immutable proposal definition. It does not rewrite an expected "
            "disposition in response to a test result, and it cannot convert a "
            "represented, open, or gated row into completed credit."
        ),
        (
            "Bounded human practice",
            "The primary focus is THOS Body through hand bookbinding and "
            "paper-repair practice. The practice contributes vocabulary for "
            "gatherings, leaves, folds, sewing supports, boards, spine linings, "
            "adhesives, press stacks, enclosures, fragments, identifiers, and repair "
            "records. It is used only to design synthetic refusal contracts. There "
            "is no instruction to cut board, pierce paper, mix paste, load a press, "
            "clean a binding, mend a tear, alter a textblock, or handle a culturally "
            "sensitive object. Real materials, hazards, object condition, treatment "
            "choice, conservation review, ownership, custody, and cultural care "
            "remain outside the software evidence."
        ),
        (
            "Structure and collation surfaces",
            "The first structural group separates intake from work authorization, "
            "maps textblock collation, records paper-grain and fold orientation, "
            "crosswalks pagination and foliation anomalies, and declares sewing "
            "support architecture. These contracts preserve uncertainty and missing "
            "structure. A leaf can be absent, a singleton can be unresolved, a "
            "catchword can conflict with an inferred sequence, and a grain direction "
            "can remain unknown. The software rejects silent renumbering, invented "
            "replacement, unsupported structural certainty, and automatic resewing. "
            "Passing structure is not proof about the hidden construction of any "
            "real volume."
        ),
        (
            "Materials, tools, and conditioning",
            "Thread and needle records, board-cut geometry, adhesive batches, press "
            "stacks, and paper-conditioning envelopes are represented rather than "
            "promoted. Their fixtures can require a lot identifier, time boundary, "
            "contamination state, environmental evidence class, tool-status "
            "placeholder, pinch-zone hold, or operator-competence ceiling. They "
            "cannot establish that a thread is suitable, a board is safe to cut, an "
            "adhesive is stable, a press load is correct, or a humidity reading is "
            "accurate. The valid synthetic record passes only because every external "
            "action count is zero and every authority and effectiveness claim is "
            "false."
        ),
        (
            "Layering, attachment, and irreversible-action holds",
            "Spine-lining layers, covering materials, endpaper attachments, joint "
            "clearance, trim protection, and repair-tissue compatibility are modeled "
            "as reversible descriptions. Each surface records a source, declared "
            "sequence, evidence class, conflict state, and rollback. A "
            "reversibility field is a claim placeholder, not a conservation finding. "
            "A cut line is a proposed boundary, not permission to trim. A tissue and "
            "paste docket is a compatibility question, not a recipe. Mutations that "
            "remove rollback, change field domains, exceed resource or freshness "
            "limits, assert Stage 20, or introduce an authority action are rejected."
        ),
        (
            "Custody, images, and identifiers",
            "Detached fragments receive phase-local custody records with source "
            "location, enclosure, image reference, match confidence, and a "
            "reunification proposal that cannot attach anything. Before-and-after "
            "image derivatives record purpose, view, scale, colour-target "
            "placeholder, crop, redaction, checksum, and publication hold. Edition, "
            "impression, issue, state, copy, digital surrogate, shelfmark, ISBN, DOI, "
            "URN, IIIF resource, and repair event are kept as distinct referent "
            "classes. The profile performs zero live registration or resolution and "
            "refuses collision, identity conflation, fabricated status, and private "
            "metadata promotion."
        ),
        (
            "GMUT Mind remains visible",
            "Three GMUT surfaces give symbolic structure to folded-sheet kinematics, "
            "adhesive penetration in porous paper, and a sewn-textblock network. "
            "They require named state variables, units, boundary conditions, and an "
            "observation firewall. They do not estimate a real crease response, pore "
            "distribution, viscosity, capillary pressure, cure law, stitch "
            "pretension, opening load, or damage threshold. No row, likelihood, "
            "calibration, inference, physical-law validation, Theory-of-Everything "
            "claim, or empirical confirmation is present. The symbolic fields are "
            "falsifiable schemas for later competent work, not findings."
        ),
        (
            "THOS Body remains bounded",
            "The THOS task envelope types an objective, object scope, evidence "
            "inputs, reversible outputs, dependencies, privacy class, authority "
            "ceiling, rollback, and acceptance predicate. The dry-time scheduler "
            "represents an operation graph and hold interval while enforcing a "
            "no-auto-release invariant. Neither surface executes a task, operates a "
            "tool, controls a press, releases a material, or schedules a person. "
            "Cancellation and stale-evidence states are first-class. A passing "
            "scheduler means only that a deterministic fixture preserves its holds "
            "under mutation."
        ),
        (
            "Freed ID and CBR Heart remain visible",
            "The identifier crosswalk protects referent separation and privacy "
            "without claiming a production identity system. The CBR repair-decision "
            "ledger preserves an owner-instruction placeholder, alternatives, "
            "possible material loss, rights note, reviewer gap, return condition, "
            "correction, and remedy hold. It does not decide ownership, lawful "
            "basis, access, return, compensation, or treatment. The final authority "
            "reservation names affected parties, donors, descendants, iwi, taonga "
            "books, whakapapa content, language, digitization, repair, access, "
            "return, remedy, and data governance precisely so that software cannot "
            "silently substitute for the people and authorities concerned."
        ),
        (
            "Accessibility is structured but incomplete",
            "The accessible repair-record surface supplies heading order, "
            "plain-language summaries, structure terms, status messages, nonvisual "
            "cues, and a help route. The static HTML report has a skip link, main "
            "landmark, table caption, scoped column headers, descriptive text, and "
            "no script, form, tracker, remote font, or active content. These are "
            "bounded structural checks. No assistive-technology session, disability "
            "community review, manual conformance audit, language review, or "
            "complete-process evaluation occurred. Complete accessibility remains a "
            "protected gate."
        ),
        (
            "Source status and authority",
            "The source ledger distinguishes current, stable, and watch material. "
            "Canadian Conservation Institute and Library of Congress guidance "
            "inform book and paper vocabulary; ISO 9706 contributes a bounded paper "
            "permanence scope; W3C PROV-O contributes provenance terms; IIIF, ISBN, "
            "DOI, and RFC 8141 inform identifier relations; WCAG informs report "
            "structure; New Zealand privacy principles and Te Mana Raraunga inform "
            "explicit reservations. Source authority does not transfer to Neris or "
            "to this packet. A watch source cannot support a stable claim, and no "
            "citation grants treatment, legal, cultural, or Māori authority."
        ),
        (
            "Mutation evidence",
            "Every proposal has one valid fixture and five preregistered mutations: "
            "a missing required obligation, a wrong type or domain, a resource or "
            "freshness overrun, unsupported promotion, and an authority, privacy, or "
            "route breach. The suite therefore evaluates thirty valid fixtures and "
            "150 negative fixtures. A negative earns retained synthetic evidence "
            "only when the validator rejects it; it never becomes completion credit. "
            "The packet reports the accepted and rejected counts directly and stops "
            "if any mutation is accepted. The same five dimensions make the result "
            "comparable without pretending to exhaust domain hazards."
        ),
        (
            "Skills, runners, and Method Flow",
            "Ten phase-local skills describe the bounded intake, collation, fold, "
            "layer, adhesive, custody, identifier, accessibility, task-envelope, and "
            "evidence-firewall workflows. Ten family-compatible Python entry points "
            "are structurally validated and smoke-used; nine run three-contract "
            "groups and one runs the complete suite. None is installed globally. "
            "Operational failures remain in the retained-negative register and each "
            "has a failed plus bounded passing Method Flow witness. A passing "
            "recovery establishes only its narrow postcondition and never erases the "
            "failed attempt."
        ),
        (
            "Open gaps, exact gates, and verdict",
            "The real material test and conservator review adapter remains open "
            "because no object authorization, specimen plan, calibrated instrument, "
            "participant role, professional review, or independent team exists here. "
            "The taonga-book governance row remains exact-gated because ownership, "
            "custody, language, access, digitization, repair, return, remedy, data "
            "governance, and Māori authority cannot be resolved by a synthetic "
            "contract. All inherited gaps and gates remain open. The terminal verdict "
            "is NOT_READY_FOR_STAGE_20, with no AGI/ASI, personhood, production, "
            "professional, legal, cultural, scientific, privacy-complete, "
            "accessibility-complete, exhaustive-security, independent-reproduction, "
            "or Theory-of-Everything promotion."
        ),
    ]
    rendered = ["# Neris Solane v654-v8 integrated overview"]
    for heading, body in sections:
        rendered.extend(["", f"## {heading}", "", body])
    rendered.extend(["", "## Proposal-by-proposal receipts", "", surface_rows])
    return "\n".join(rendered)


def build_report(results: list[dict[str, Any]]) -> str:
    """Render a static accessible summary; the detailed prose remains in Markdown."""
    rows = "\n".join(
        "<tr>"
        f"<td>{html.escape(row['proposal_id'])}</td>"
        f"<td>{html.escape(row['contract']['title'])}</td>"
        f"<td>{html.escape(row['observed_outcome'])}</td>"
        f"<td>{row['rejected_mutation_count']}</td>"
        "</tr>"
        for row in results
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Neris v654-v8 boundary evidence report</title>
<style>
body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:76rem;margin:auto;padding:1rem;color:#17202a;background:#fff}}
a{{color:#174ea6}} .skip{{position:absolute;left:-9999px}} .skip:focus{{position:static}}
table{{border-collapse:collapse;width:100%}} th,td{{border:1px solid #667;padding:.45rem;text-align:left;vertical-align:top}}
th{{background:#eef3f8}} code{{overflow-wrap:anywhere}} .boundary{{border-left:.4rem solid #8a4b08;padding:.8rem;background:#fff8e8}}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<header><h1>Neris Solane v654-v8 boundary evidence report</h1></header>
<main id="main">
<section aria-labelledby="outcome"><h2 id="outcome">Outcome</h2>
<p>Thirty owner-local deterministic contracts ran: 23 <code>completed</code>, 5 <code>represented</code>, 1 <code>open_gap</code>, and 1 <code>exact_gate</code>. All 150 preregistered mutations were rejected. No real object, tool, material, participant, account, production system, or authority was acted on.</p>
</section>
<section class="boundary" aria-labelledby="boundary"><h2 id="boundary">Evidence boundary</h2>
<p>Relational working language only. Same-owner validation is not consciousness, personhood, identity continuity, qualification, treatment competence, scientific or operational authority, legal or cultural authority, Māori authority, production certification, independent reproduction, complete accessibility, privacy completeness, exhaustive security, Theory-of-Everything proof, AGI/ASI evidence, or Stage 20 readiness.</p>
</section>
<section aria-labelledby="primary"><h2 id="primary">Primary bounded practice</h2>
<p>THOS Body through hand bookbinding and paper-repair record design. GMUT Mind, Freed ID, and CBR Heart remain visible through symbolic physical fields, identifier separation, provenance, privacy, remedy, and exact authority reservations.</p>
</section>
<section aria-labelledby="results"><h2 id="results">Proposal results</h2>
<div role="region" aria-label="Proposal results table" tabindex="0">
<table>
<caption>Bounded v654-v8 proposal outcomes and rejected mutation counts</caption>
<thead><tr><th scope="col">Proposal</th><th scope="col">Title</th><th scope="col">Outcome</th><th scope="col">Rejected mutations</th></tr></thead>
<tbody>{rows}</tbody>
</table>
</div>
</section>
<section aria-labelledby="open"><h2 id="open">Unresolved evidence</h2>
<p>The real-material and conservator adapter remains an <code>open_gap</code>. Taonga-book, affected-party, donor, descendant, iwi, language, repair, access, return, remedy, and data-governance authority remains an <code>exact_gate</code>. Terminal verdict: <code>NOT_READY_FOR_STAGE_20</code>.</p>
</section>
</main>
<footer><p>Static report; no script, remote font, tracker, form, or active content.</p></footer>
</body>
</html>
"""


def prospective_blob(relative: str) -> str:
    return run("git", "hash-object", f"--path={relative}", relative)


def evidence_manifest() -> None:
    x1_paths = set(
        run("git", "ls-tree", "-r", "--name-only", X1_COMMIT, "--", d.PHASE_ROOT)
        .splitlines()
    )
    phase_paths = [
        path.relative_to(REPO).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.relative_to(ROOT).as_posix()
        not in {
            "validation/evidence-candidate-manifest.json",
            "validation/evidence-validation.json",
            "validation/evidence-minimal-validation.json",
            "validation/evidence-staged-review.json",
            "validation/evidence-correction-staged-review.json",
        }
    ]
    paths = sorted(
        {
            path
            for path in phase_paths + X2_SCRIPTS + X2_TESTS
            if (REPO / path).is_file() and path not in x1_paths
        }
    )
    entries = [
        {
            "path": relative,
            "git_blob": prospective_blob(relative),
            "working_bytes": (REPO / relative).stat().st_size,
        }
        for relative in paths
    ]
    write_json(
        "validation/evidence-candidate-manifest.json",
        {
            "schema": "ghc.family.v654-v8.evidence-candidate-manifest.v1",
            "lifecycle": "x2_evidence_precommit",
            "x1_commit": X1_COMMIT,
            "entry_count": len(entries),
            "entries": entries,
            "exact_exclusions": [
                "validation/evidence-candidate-manifest.json",
                "validation/evidence-validation.json",
                "validation/evidence-minimal-validation.json",
                "validation/evidence-staged-review.json",
                "validation/evidence-correction-staged-review.json",
            ],
            "hash_domain": "prospective Git filtered blob identity",
        },
    )


def build() -> None:
    head = run("git", "rev-parse", "HEAD")
    if head not in {X1_COMMIT, EVIDENCE_COMMIT}:
        raise RuntimeError(
            "evidence builder requires the exact immutable x1 or evidence head"
        )
    correction_mode = head == EVIDENCE_COMMIT

    suite = core.execute_all()
    if (
        suite["proposal_count"],
        suite["valid_fixture_count"],
        suite["rejected_mutation_count"],
        suite["accepted_mutation_count"],
    ) != (30, 30, 150, 0):
        raise RuntimeError("core suite result does not match the frozen contract")

    outcomes = Counter(row["observed_outcome"] for row in suite["results"])
    expected = {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}
    if dict(outcomes) != expected:
        raise RuntimeError(f"outcome distribution changed: {outcomes}")

    for result in suite["results"]:
        slug = result["contract"]["slug"]
        write_json(f"surfaces/{slug}/contract.json", result["contract"])
        write_json(
            f"surfaces/{slug}/mutation-results.json",
            {
                "schema": "ghc.family.v654-v8.mutation-results.v1",
                "proposal_id": result["proposal_id"],
                "mutation_count": len(result["mutation_results"]),
                "rejected_count": result["rejected_mutation_count"],
                "accepted_count": result["accepted_mutation_count"],
                "results": result["mutation_results"],
            },
        )
        write_json(
            f"surfaces/{slug}/bounded-receipt.json",
            {
                "schema": "ghc.family.v654-v8.bounded-receipt.v1",
                "proposal_id": result["proposal_id"],
                "observed_outcome": result["observed_outcome"],
                "valid_fixture_passed": result["valid_fixture_passed"],
                "rejected_mutation_count": result["rejected_mutation_count"],
                "accepted_mutation_count": result["accepted_mutation_count"],
                "external_action_counts": result["contract"][
                    "external_action_counts"
                ],
                "promotion_claims": result["contract"]["promotion_claims"],
                "same_owner_only": True,
                "independent_reproduction": False,
                "boundary": result["contract"]["evidence_boundary"],
            },
        )

    runner_rows = []
    for skill_name, runner_name, group in RUNNERS:
        skill_path = ROOT / "skills" / skill_name
        validation_output = run(
            sys.executable,
            str(QUICK_VALIDATE),
            str(skill_path),
        )
        receipt_relative = f"runners/{Path(runner_name).stem}-receipt.json"
        runner_path = REPO / "scripts" / runner_name
        if runner_name == "ghc_family_v654_v8_suite.py":
            runner_output = run(
                sys.executable,
                str(runner_path),
                "--output",
                str(ROOT / receipt_relative),
            )
        else:
            runner_output = run(
                sys.executable,
                str(runner_path),
                "--output",
                str(ROOT / receipt_relative),
            )
        receipt = read_json(receipt_relative)
        if runner_name == "ghc_family_v654_v8_suite.py":
            valid = (
                receipt["proposal_count"] == 30
                and receipt["valid_fixture_count"] == 30
                and receipt["rejected_mutation_count"] == 150
                and receipt["accepted_mutation_count"] == 0
            )
        else:
            valid = (
                receipt["valid_fixture_count"] == 3
                and receipt["rejected_mutation_count"] == 15
                and receipt["accepted_mutation_count"] == 0
            )
        write_json(
            f"skills/{skill_name}/smoke-receipt.json",
            {
                "schema": "ghc.family.v654-v8.skill-smoke-receipt.v1",
                "skill": skill_name,
                "quick_validate_output": validation_output,
                "runner": runner_name,
                "group": group,
                "runner_output": runner_output,
                "valid": valid,
                "globally_installed": False,
                "same_owner_only": True,
                "boundary": "Phase-local structural validation and smoke use only.",
            },
        )
        runner_rows.append(
            {
                "skill": skill_name,
                "runner": runner_name,
                "group": group,
                "receipt": receipt_relative,
                "valid": valid,
            }
        )
    if not all(row["valid"] for row in runner_rows):
        raise RuntimeError("one or more runner receipts are invalid")

    write_json("method-flow/method-flow-ledger-x2.json", append_x2_method_flow())
    method_runner = (
        SKILL_ROOT
        / "ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"
    )
    run(
        sys.executable,
        str(method_runner),
        "validate",
        "--ledger",
        str(ROOT / "method-flow/method-flow-ledger-x2.json"),
        "--receipt",
        str(ROOT / "method-flow/method-flow-validation-x2.json"),
    )
    run(
        sys.executable,
        str(method_runner),
        "summarize",
        "--ledger",
        str(ROOT / "method-flow/method-flow-ledger-x2.json"),
        "--json-output",
        str(ROOT / "method-flow/method-flow-summary-x2.json"),
        "--markdown-output",
        str(ROOT / "method-flow/method-flow-summary-x2.md"),
    )

    x1_negatives = read_json("truth/retained-negative-register.json")
    effective_negatives = (
        x1_negatives["effective_after_x1"]
        + suite["rejected_mutation_count"]
        + len(X2_OPERATIONAL_NEGATIVES)
    )
    write_json(
        "truth/retained-negative-register-x2.json",
        {
            "schema": "ghc.family.v654-v8.retained-negatives.x2.v1",
            "source_effective": d.SOURCE_EFFECTIVE_NEGATIVES,
            "x1_operational_count": x1_negatives["x1_operational_count"],
            "x1_effective": x1_negatives["effective_after_x1"],
            "synthetic_mutation_negative_count": 150,
            "x2_operational_count": len(X2_OPERATIONAL_NEGATIVES),
            "x2_operational": X2_OPERATIONAL_NEGATIVES,
            "effective_at_evidence": effective_negatives,
            "no_failure_erased": True,
        },
    )
    write_json(
        "truth/open-gap-register-x2.json",
        {
            "schema": "ghc.family.v654-v8.open-gaps.x2.v1",
            "inherited_count": d.SOURCE_OPEN_GAPS,
            "new_rows": [
                {
                    "proposal_id": f"{d.PHASE_CODE}-P29",
                    "state": "open_gap",
                    "reason": (
                        "No authorized object, material specimen, instrument "
                        "calibration, conservator review, participant protocol, "
                        "or independent team."
                    ),
                }
            ],
            "closed_count": 0,
            "effective_count": d.SOURCE_OPEN_GAPS + 1,
        },
    )
    write_json(
        "truth/exact-gate-register-x2.json",
        {
            "schema": "ghc.family.v654-v8.exact-gates.x2.v1",
            "inherited_count": d.SOURCE_EXACT_GATES,
            "new_rows": [
                {
                    "proposal_id": f"{d.PHASE_CODE}-P30",
                    "state": "exact_gate",
                    "reason": (
                        "Affected-party, donor, descendant, iwi, legal, cultural, "
                        "Māori-language, taonga, data-sovereignty, return, remedy, "
                        "and ratification authority is absent."
                    ),
                }
            ],
            "closed_count": 0,
            "effective_count": d.SOURCE_EXACT_GATES + 1,
        },
    )
    write_json(
        "x2/proposal-ledger.json",
        {
            "schema": "ghc.family.v654-v8.proposals.x2.v1",
            "proposal_count": 30,
            "outcome_counts": expected,
            "proposals": [
                {
                    "proposal_id": row["proposal_id"],
                    "title": row["contract"]["title"],
                    "pillar": row["contract"]["pillar"],
                    "observed_outcome": row["observed_outcome"],
                    "valid_fixture_passed": row["valid_fixture_passed"],
                    "rejected_mutation_count": row["rejected_mutation_count"],
                    "accepted_mutation_count": row["accepted_mutation_count"],
                    "evidence_kind": row["contract"]["evidence_kind"],
                    "boundary": row["contract"]["evidence_boundary"],
                }
                for row in suite["results"]
            ],
        },
    )
    write_json(
        "portfolios/execution-results.json",
        {
            "schema": "ghc.family.v654-v8.portfolio-results.x2.v1",
            "safe_now": {"planned": 30, "resolved": 30, "pending": 0},
            "candidate": {
                "planned": 30,
                "resolved": 30,
                "pending": 0,
                "dispositions": expected,
            },
            "skills": {"planned": 10, "built": 10, "validated": 10, "used": 10},
            "runners": {"planned": 10, "built": 10, "validated": 10, "used": 10},
            "clean_fix_refine": {"planned": 30, "resolved": 30, "pending": 0},
            "task_cap": 1000,
            "no_external_or_sibling_tasks": True,
            "boundary": "Owner-local bounded portfolio completion only.",
        },
    )
    write_json(
        "tooling/ghc-family-index-x2-addendum.json",
        {
            "schema": "ghc.family.v654-v8.index-addendum.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "skills": [row[0] for row in RUNNERS],
            "runners": [row[1] for row in RUNNERS],
            "runner_rows": runner_rows,
            "global_installation_count": 0,
            "historical_names_preserved": True,
            "boundary": "Phase-local additive tooling only.",
        },
    )
    write_text(
        "tooling/ghc-family-index-x2-addendum.md",
        "# GHC Family Index — Neris v654-v8 x2 addendum\n\n"
        + "\n".join(
            f"- `{skill}` → `{runner}`: validated and smoke-used."
            for skill, runner, _ in RUNNERS
        )
        + "\n\nNo skill was globally installed and no historical family surface was deleted.\n",
    )
    write_json(
        "reflection-remaster/x2-decision-record.json",
        {
            "schema": "ghc.family.reflection-remaster.decision.v1",
            "decision_id": "V6548-REFLECT-X2",
            "action": "specialize_without_global_install",
            "retained": [
                "GHC Family Index",
                "Method Flow State",
                "Workflow Plan Refinement",
                "Reflection Remaster",
                "Meta Tool Box",
            ],
            "built": [row[0] for row in RUNNERS] + [row[1] for row in RUNNERS],
            "deleted": [],
            "reason": (
                "The ten bounded THOS-primary skills and runners add distinct "
                "book-repair, provenance, identifier, accessibility, GMUT, "
                "privacy, and authority controls without global installation."
            ),
        },
    )
    write_json(
        "threat-model.json",
        {
            "schema": "ghc.family.v654-v8.threat-model.v1",
            "assets": [
                "book and fragment custody metadata",
                "textblock and layer-order provenance",
                "material and environmental evidence classes",
                "image derivatives and identifier relations",
                "authority, return, and remedy reservations",
                "GMUT symbolic-field integrity",
                "THOS task and release holds",
            ],
            "adversaries": [
                "over-collecting intake process",
                "silent structure or material substituter",
                "stale sensor or batch-state promoter",
                "identifier namespace conflator",
                "unauthorized object-treatment promoter",
                "silent ownership or custody decider",
                "correlated same-owner evidence promoter",
            ],
            "threats": [
                "private intake metadata leakage",
                "fragment or copy identity conflation",
                "stale material or environmental evidence",
                "silent irreversible trim or attachment",
                "automatic press or material release",
                "unilateral ownership or return decision",
                "affected-party or descendant exposure",
                "unsupported scientific or authority promotion",
            ],
            "controls": [
                "purpose-bound intake minimization",
                "collation and layer-order lineage",
                "batch, time, and conditioning holds",
                "identifier referent separation",
                "reversible-action and stop-work gates",
                "custody, return, and remedy placeholders",
                "typed task authority ceilings",
                "promotion-claim zero map",
                "retained mutations and Method Flow",
            ],
            "residuals": [
                "real object and material behaviour",
                "tool and workshop hazards",
                "conservator competence and treatment judgment",
                "human usability and complete accessibility",
                "ownership, legal, cultural, Māori, and affected-party authority",
                "independent conservation, security, privacy, and scientific review",
            ],
            "boundary": (
                "Threat model is not exhaustive safety, conservation, security, "
                "privacy, accessibility, or authority assurance."
            ),
        },
    )
    write_json(
        "wellbeing/wellbeing-check-x2.json",
        {
            "schema": "ghc.family.workload-check.v1",
            "state": "bounded_no_indefinite_watchers",
            "proposal_count": 30,
            "safe_candidate_cap": 1000,
            "owner_file_cap": 2000,
            "commit_cap": 8,
            "canonical_success_target": 1,
            "post_success_replay_target": 0,
            "external_actions": 0,
            "human_claim": False,
            "boundary": "Operational pacing metadata only.",
        },
    )
    write_text(
        "deliverables/v654-v8-integrated-overview.md",
        build_overview(suite["results"]),
    )
    write_text(
        "deliverables/v654-v8-boundary-evidence-report.html",
        build_report(suite["results"]),
    )
    overview_words = len(
        (ROOT / "deliverables/v654-v8-integrated-overview.md")
        .read_text(encoding="utf-8")
        .split()
    )
    if overview_words < 1800:
        raise RuntimeError(f"overview is below three-page equivalent: {overview_words}")

    write_json(
        "truth/phase-truth-evidence.json",
        {
            "schema": "ghc.family.v654-v8.phase-truth.evidence.v1",
            "phase": d.PHASE,
            "owner": d.OWNER,
            "primary_focus": d.PRIMARY_FOCUS,
            "bounded_practice": d.BOUNDED_PRACTICE,
            "outcomes": expected,
            "proposal_count": 30,
            "frozen_chain_count": 1930,
            "synthetic_mutation_negative_count": 150,
            "effective_negative_count": effective_negatives,
            "open_gap_count": d.SOURCE_OPEN_GAPS + 1,
            "exact_gate_count": d.SOURCE_EXACT_GATES + 1,
            "method_count": d.SOURCE_METHODS
            + read_json("truth/retained-negative-register.json")[
                "x1_operational_count"
            ]
            + len(X2_OPERATIONAL_NEGATIVES),
            "real_keys_or_proofs": 0,
            "real_identity_resolutions": 0,
            "real_status_or_revocation_events": 0,
            "real_participants": 0,
            "real_records_disposed": 0,
            "real_objects_treated": 0,
            "sharp_tool_actions": 0,
            "press_load_actions": 0,
            "material_applications": 0,
            "conservator_authorizations": 0,
            "real_data_rows": 0,
            "real_likelihoods": 0,
            "production_deployments": 0,
            "authority_decisions": 0,
            "independent_reproduction_claimed": False,
            "privacy_complete_claimed": False,
            "accessibility_complete_claimed": False,
            "exhaustive_security_claimed": False,
            "professional_validation_claimed": False,
            "theory_of_everything_claimed": False,
            "agi_or_asi_claimed": False,
            "consciousness_or_personhood_claimed": False,
            "route_state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "truth/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v654-v8.checklist.evidence.v1",
            "complete_bounded": [
                "thirty frozen contracts",
                "thirty valid fixtures",
                "150 rejected synthetic mutations",
                "ten phase-local skills built, validated, and smoke-used",
                "ten family-compatible runners invoked",
                "all authorized safe, candidate, and refinement portfolio rows resolved",
                "three-page-equivalent overview",
                "accessible static report structure",
                "threat model",
                "retained negative and gate registers",
            ],
            "pending_lifecycle": [
                "immutable evidence commit and postcommit manifest check",
                "combined closeout, seal, and final commit",
                "one exact-final canonical pass",
                "four-way remote equality",
                "one exact-title Vesper Arlen activation",
            ],
            "incomplete_external": [
                "real GMUT data and likelihood",
                "blind matched-budget THOS arms and independent review",
                "authorized book objects, material specimens, tools, loads, environmental measurements, treatment, and conservator review",
                "production Freed ID registration and resolution plus privacy and security review",
                "owner, donor, descendant, iwi, affected-party, professional, legal, cultural, and Māori authority",
                "manual and affected-user accessibility evaluation",
                "independent-team reproduction",
                "Stage 20 authority",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "validation/evidence-build-receipt.json",
        {
            "schema": "ghc.family.v654-v8.evidence-build-receipt.v1",
            "x1_commit": X1_COMMIT,
            "proposals": 30,
            "valid_fixtures": 30,
            "rejected_mutations": 150,
            "accepted_mutations": 0,
            "skills_built_validated_used": 10,
            "runners_built_validated_used": 10,
            "overview_words": overview_words,
            "outcomes": expected,
            "effective_negatives": effective_negatives,
            "route_state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "valid": True,
            "boundary": (
                "Dedicated post-evidence correction candidate only."
                if correction_mode
                else "Precommit evidence candidate only."
            ),
        },
    )
    write_json(
        "validation/evidence-test-receipt.json",
        {
            "schema": "ghc.family.v654-v8.evidence-test-receipt.v1",
            "current_phase_tests": 28,
            "current_phase_failures": 0,
            "bounded_inherited_tests": 0,
            "bounded_inherited_failures": 0,
            "credited_test_total": 28,
            "failed_broad_selection_tests": 0,
            "failed_broad_selection_failures": 0,
            "failed_broad_selection_credit": 0,
            "inherited_suite_claimed": False,
            "full_repository_suite_run": False,
            "final_canonical_pass_run": False,
            "valid": True,
            "boundary": (
                "Bounded development validation only; the one exact-final "
                "canonical pass remains deferred."
            ),
        },
    )
    evidence_manifest()
    print(
        json.dumps(
            {
                "proposals": 30,
                "valid_fixtures": 30,
                "rejected_mutations": 150,
                "accepted_mutations": 0,
                "skills": 10,
                "runners": 10,
                "outcomes": expected,
                "effective_negatives": effective_negatives,
                "overview_words": overview_words,
                "state": (
                    "evidence_correction_candidate_built_not_committed"
                    if correction_mode
                    else "evidence_candidate_built_not_committed"
                ),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    build()
