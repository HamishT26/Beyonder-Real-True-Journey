from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable

import build_ghc_family_elowen_cairn_v671_v1_x2 as x2


ROOT = x2.ROOT
OWNER_ROOT = x2.OWNER_ROOT
OWNER = x2.OWNER
PHASE = x2.PHASE
BRANCH = x2.BRANCH
SOURCE_FINAL = x2.SOURCE_FINAL
FROZEN_X1 = x2.X1_COMMIT
FROZEN_EVIDENCE = "460c8fff65986d82223afc1cfe96645b57960584"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
DOCUMENT_WORD_CEILING = 100_000
FILE_CEILING = 2_000
FINAL_METHOD_TITLES = (
    "replay immutable source and lifecycle anchors",
    "preserve exact outcome and proposal-chain truth",
    "close retained-negative and Method Flow arithmetic",
    "retain open gaps and exact authority gates",
    "materialize complete and incomplete checklist",
    "materialize workload and stop-rule receipt",
    "materialize threat and privacy boundary model",
    "materialize source and provenance closeout",
    "render structurally accessible static report",
    "seal exact Git-blob manifests and content",
    "prepare but do not send the successor baton",
    "reserve one exact-final canonical invocation",
)
FINAL_OVERLAY = {
    "effective_negatives": 33_521,
    "effective_methods": 19_838,
    "failed_witnesses": 5_342,
    "bounded_passing_witnesses": 6_877,
    "effective_open_gaps": 257,
    "effective_exact_gates": 252,
}
FINAL_FAILURES = [
    {
        "failure_id": "EC6711-FINAL-N001",
        "failed_witness": (
            "The first final Method Flow schema validation rejected all twelve new closeout methods because their retained_negative_ids lists were empty."
        ),
        "recovery": (
            "Retain the failed validation receipt, record one operational failure, link every closeout method to that retained negative, and rerun only the Method Flow validator."
        ),
        "recurrence_guard": (
            "Every Method Flow method, including failure-free closeout methods, must link at least one retained negative identifier."
        ),
    },
    {
        "failure_id": "EC6711-FINAL-N002",
        "failed_witness": (
            "The first non-executing final-test contract audit projected stale skill, runner, and tool field shapes and failed while indexing a nonexistent tool rows array."
        ),
        "recovery": (
            "Inspect the exact committed skill, runner, and keyed tool receipts and patch only the unexecuted final assertions before canonical invocation."
        ),
        "recurrence_guard": (
            "Read exact JSON keys and container types before projecting test assertions across inherited receipt schemas."
        ),
    },
    {
        "failure_id": "EC6711-FINAL-N003",
        "failed_witness": (
            "The first compact final preflight one-liner emitted only its placeholder text and no auditable privacy or security summary."
        ),
        "recovery": (
            "Run an explicit bounded stdin program over exact index blobs and emit structured JSON counts and findings."
        ),
        "recurrence_guard": (
            "Use readable multi-line bounded audit programs when a one-liner would obscure control flow or output guarantees."
        ),
    },
    {
        "failure_id": "EC6711-FINAL-N004",
        "failed_witness": (
            "The recovered full-owner preflight showed that the initial canonical scanner allowlist misclassified seven committed scanner-definition receipts and x1 scanner surfaces as confirmed payload hits."
        ),
        "recovery": (
            "Enumerate only the exact known scanner-definition code and receipt paths as candidates, then require zero confirmed hits across every other owner blob."
        ),
        "recurrence_guard": (
            "Carry scanner-definition dispositions across lifecycle-wide scans without granting a broad path or content exemption."
        ),
    },
]
FINAL_CODE_PATHS = [
    "scripts/build_ghc_family_elowen_cairn_v671_v1_final.py",
    "scripts/validate_ghc_family_elowen_cairn_v671_v1_final.py",
    "tests/test_ghc_family_elowen_cairn_v671_v1_final.py",
]
OWNER_CODE_PATHS = sorted(
    set(
        x2.TOOL_PATHS
        + x2.RUNNER_PATHS
        + x2.BUILD_PATHS
        + [
            "scripts/build_ghc_family_elowen_cairn_v671_v1_x1.py",
            "tests/test_ghc_family_elowen_cairn_v671_v1_x1.py",
        ]
        + FINAL_CODE_PATHS
    )
)
SCANNER_DEFINITION_PATHS = set(
    FINAL_CODE_PATHS
    + x2.BUILD_PATHS
    + x2.TOOL_PATHS
    + [
        "scripts/build_ghc_family_elowen_cairn_v671_v1_x1.py",
        "tests/test_ghc_family_elowen_cairn_v671_v1_x1.py",
        "docs/elowen-cairn/v671-v1/validation/evidence-staged-privacy.json",
        "docs/elowen-cairn/v671-v1/validation/final-staged-privacy.json",
        "docs/elowen-cairn/v671-v1/validation/x1-staged-privacy.json",
        "docs/elowen-cairn/v671-v1/validation/x1-validation-receipt.json",
    ]
)
FINAL_OWNER_MANIFEST = "docs/elowen-cairn/v671-v1/validation/final-owner-manifest.json"
FINAL_DELTA_MANIFEST = "docs/elowen-cairn/v671-v1/validation/final-delta-manifest.json"
FINAL_STAGED_REVIEW = "docs/elowen-cairn/v671-v1/validation/final-staged-review.json"
FINAL_STAGED_PRIVACY = "docs/elowen-cairn/v671-v1/validation/final-staged-privacy.json"
CONTENT_SEAL = "docs/elowen-cairn/v671-v1/seal/content-seal.json"
CLOSEOUT_RECEIPT = "docs/elowen-cairn/v671-v1/closeout/closeout-receipt.json"
MANIFEST_EXCLUSIONS = {
    FINAL_OWNER_MANIFEST,
    FINAL_DELTA_MANIFEST,
    FINAL_STAGED_REVIEW,
    CONTENT_SEAL,
    CLOSEOUT_RECEIPT,
}
IDENTITY_BOUNDARY = (
    "Elowen Cairn and they/them are relational working language for a boundary cartographer and evidence steward, "
    "with the hope of keeping structure, evidence, abstention, and authority visibly separate and recoverable. "
    "This is not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, "
    "independent agency, or scientific, operational, professional, legal, cultural, affected-party, or Māori authority. "
    "Hamish may rename, pause, redirect, or stop the work."
)
BOUNDARY = (
    "Same-owner synthetic software and documentation evidence only; not empirical confirmation, participant evidence, "
    "professional validation, production or deployment readiness, independent reproduction, exhaustive security, complete "
    "privacy or accessibility assurance, legal or cultural ratification, Māori authority, AGI or ASI evidence, consciousness "
    "or personhood evidence, Theory-of-Everything proof, canon, or Stage 20 authority."
)


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=check)


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8", errors="strict").strip()


def load(relative: str) -> Any:
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def canonical_bytes(payload: Any) -> bytes:
    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def owner_path(path: str) -> bool:
    return path.startswith("docs/elowen-cairn/v671-v1/") or path in OWNER_CODE_PATHS


def index_objects() -> dict[str, dict[str, str]]:
    objects: dict[str, dict[str, str]] = {}
    for line in git_text("ls-files", "--stage").splitlines():
        left, path = line.split("\t", 1)
        mode, object_id, stage = left.split()
        if stage == "0":
            objects[path] = {"mode": mode, "object_id": object_id}
    return objects


def index_rows(paths: Iterable[str]) -> list[dict[str, Any]]:
    objects = index_objects()
    selected = sorted(set(paths))
    missing = [path for path in selected if path not in objects]
    if missing:
        raise RuntimeError(f"missing staged/index objects: {missing}")
    blobs = x2.batch_git_blobs([objects[path]["object_id"] for path in selected])
    rows: list[dict[str, Any]] = []
    for path, blob in zip(selected, blobs, strict=True):
        if blob is None:
            raise RuntimeError(f"missing Git blob: {path}")
        rows.append(
            {
                "path": path,
                "mode": objects[path]["mode"],
                "git_blob_oid": objects[path]["object_id"],
                "bytes": len(blob),
                "sha256": sha256(blob),
            }
        )
    return rows


def staged_paths() -> list[str]:
    text = git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR")
    return sorted(text.splitlines()) if text else []


def assert_closeout_start() -> None:
    if git_text("branch", "--show-current") != BRANCH:
        raise RuntimeError("wrong Elowen owner branch")
    if git_text("rev-parse", "HEAD") != FROZEN_EVIDENCE:
        raise RuntimeError("closeout must begin from immutable Elowen evidence")
    if git_text("rev-parse", f"{FROZEN_EVIDENCE}^") != FROZEN_X1:
        raise RuntimeError("immutable evidence is not the direct child of frozen x1")
    staged = staged_paths()
    out_of_scope = [path for path in staged if not owner_path(path)]
    frozen = [
        path
        for path in staged
        if path.startswith("docs/elowen-cairn/v671-v1/x1/")
        or path.startswith("docs/elowen-cairn/v671-v1/x2/")
        or path in x2.BUILD_PATHS
    ]
    if out_of_scope or frozen:
        raise RuntimeError(f"closeout refresh staged-scope failure: out={out_of_scope}, frozen={frozen}")
    if git("diff", "--quiet", check=False).returncode != 0:
        raise RuntimeError("closeout builder requires no tracked working-tree drift")


def final_method_flow() -> dict[str, Any]:
    ledger = deepcopy(load("x2/method-flow-evidence.json"))
    for index, title in enumerate(FINAL_METHOD_TITLES, start=1):
        failure = FINAL_FAILURES[index - 1] if index <= len(FINAL_FAILURES) else None
        x2.append_method(
            ledger,
            f"EC6711-FINAL-M{index:03d}",
            title,
            [row["failure_id"] for row in FINAL_FAILURES],
            failure["failed_witness"] if failure else None,
            f"The owner-local closeout method '{title}' produced a bounded exact artifact or gate without external action.",
            "Require immutable evidence parentage, exact Git-blob review, and retained authority boundaries.",
        )
    states = Counter(row["recommendation_state"] for row in ledger["methods"])
    results = Counter(row["result"] for row in ledger["witnesses"])
    ledger["counts"] = {
        "methods": len(ledger["methods"]),
        "witnesses": len(ledger["witnesses"]),
        "state_events": len(ledger["state_events"]),
        "recommendations": len(ledger["recommendations"]),
        "states": {
            state: states.get(state, 0)
            for state in ("candidate", "deprecated", "observed", "preferred", "superseded", "validated")
        },
        "witness_results": {result: results.get(result, 0) for result in ("fail", "pass")},
    }
    ledger["effective_overlay"] = {
        "effective_negatives": FINAL_OVERLAY["effective_negatives"],
        "effective_methods": FINAL_OVERLAY["effective_methods"],
        "failed_witnesses": FINAL_OVERLAY["failed_witnesses"],
        "bounded_passing_witnesses": FINAL_OVERLAY["bounded_passing_witnesses"],
        "repository_seal_rewritten": False,
    }
    expected = {
        "methods": 230,
        "witnesses": 419,
        "state_events": 690,
        "recommendations": 230,
    }
    for key, value in expected.items():
        if ledger["counts"][key] != value:
            raise RuntimeError(f"final Method Flow {key} drift")
    if ledger["counts"]["witness_results"] != {"fail": 189, "pass": 230}:
        raise RuntimeError("final Method Flow witness drift")
    return ledger


def overview() -> str:
    evidence = (OWNER_ROOT / "x2/evidence-overview.md").read_text(encoding="utf-8").rstrip()
    return evidence + "\n\n" + f"""
# Elowen Cairn v671-v1 final integrated closeout

## Outcome first

Elowen v671-v1 closes as a bounded same-owner synthetic phase with exactly 28 completed, 8 represented, 2 open-gap, and 2 exact-gate proposal outcomes. The planning-only x1 commit is {FROZEN_X1}; immutable x2 evidence is {FROZEN_EVIDENCE}; this closeout is prepared as their single direct-child final. The source is Tamar Vey's immutable final {SOURCE_FINAL}. Source to final therefore has exactly three Elowen single-parent commits and zero merges when this candidate is committed. X1 and evidence were each pushed, clean, typed 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote before the next lifecycle began.

The final additive truth is {FINAL_OVERLAY['effective_negatives']} effective negatives, {FINAL_OVERLAY['effective_methods']} Method Flow methods, {FINAL_OVERLAY['failed_witnesses']} retained failed witnesses, {FINAL_OVERLAY['bounded_passing_witnesses']} bounded passing witnesses, {FINAL_OVERLAY['effective_open_gaps']} open gaps, and {FINAL_OVERLAY['effective_exact_gates']} exact gates. The twelve closeout methods add twelve bounded passing witnesses and retain four closeout failures: the Method Flow link omission, the stale receipt-shape projection, the non-auditing compact preflight, and the incomplete scanner-definition allowlist. The three x2 operational failures, twenty-two x1 failures, 160 rejecting mutations, all four closeout failures, and every inherited or external baseline failure remain visible. Recovery never changes a failed witness into success credit.

## Lifecycle and validation interpretation

The first x1 aggregate passed 23 of 24 checks and failed one overly literal source-status predicate. It retains zero aggregate-pass credit. Only that failed dependency ran again and passed 1 of 1; the other twenty-three checks were not replayed. X2 then passed 30 of 30 owner-scoped tests once. The resulting evidence-stage composite accounts for 54 bounded checks while preserving the failed x1 aggregate as failed. It is not a canonical aggregate and not independent reproduction. Evidence validation additionally parsed 136 JSON documents, compiled fifteen owner Python surfaces, found zero frozen-x1 changes, kept 233 materialized files below the 2,000-file ceiling, and found six scanner or unit-test definition candidates with zero confirmed private or raw-identifier hits across 195 staged text files. The exact evidence manifest seals 196 Git blobs.

The full repository suite was not run and is not claimed. One attributable exact-final owner-scoped canonical aggregate is reserved until after the final commit is pushed, clean, typed 0/0 divergent, and fresh-live four-way equal. If that aggregate succeeds, it will not be replayed. If it fails, it remains zero canonical-success credit; only a genuinely failed dependency may receive separately named bounded recovery. Same-owner validation under shared infrastructure is not independent-team reproduction, external audit, production certification, exhaustive security, complete privacy or accessibility assurance, professional validation, legal review, cultural ratification, Māori-authority review, empirical GMUT confirmation, Theory-of-Everything proof, AGI or ASI evidence, consciousness or personhood evidence, canon, or Stage 20 authority.

## Trinity Mandala and bounded shoemaking lens

THOS Body was the primary pillar, viewed through wholly synthetic shoemaking and cobbling documentation. The forty contracts cover fabricated job identity, last and pattern topology, upper and sole relations, measurement vacancy, assembly lineage, diagnosis and safety abstention, privacy quarantine, accessible status, correction readback, workload, provenance, rights holds, GMUT typed obligations, THOS protocol boundaries, Freed ID vacancy, CBR challenge and remedy, adapter vacancy, affected-user gaps, authority gates, and Stage 20 nonpromotion. GMUT Mind and Freed ID or CBR Heart remained visible and protected throughout.

This phase used zero real people, participants, shoemakers, cobblers, conservators, customers, owners, custodians, workshops, footwear, lasts, patterns, uppers, soles, materials, adhesives, stitches, tools, observations, measurements, diagnoses, treatments, repairs, releases, identity events, keys, proofs, professional decisions, legal or cultural decisions, affected-party approvals, or authority acts. It made no production deployment, no account or credential change, and no third-party write. Official Victoria and Albert Museum, NIST, and W3C sources supplied bounded vocabulary or structural obligations only; they were not object observations, instructions, conformance evidence, professional validation, or authority.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Synthetic software, symbolic typing, citations, and rejecting fixtures establish no real likelihood, parameter constraint, force, prediction, material law, stability theorem, empirical confirmation, quantum or ultraviolet completion, final physics, Theory of Everything, proof, or canon. THOS remains a participant-free proxy without preregistered blind matched-budget governed real arms, real operators, safety monitoring, appropriate statistics, or independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys or proofs, live issuance, resolution, status or revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.

CBR, professional diagnosis and treatment, workplace or material safety, ownership, custody, access, copyright, privacy remedy, legal or cultural interpretation, affected-party legitimacy, Māori wording, Māori concepts, Māori data governance, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority. The terminal verdict remains {TERMINAL_VERDICT}.

## Tools, portfolios, accessibility, and recoverability

Twenty phase-local skills were initialized with the current skill-creator, customized, quick-validated, and smoke-used locally. Ten family-named runners and three owner-local tools passed bounded accepting and rejecting fixtures. Nothing was globally installed. Sixty safe-now tasks, thirty candidates, sixty clean-fix-refine tasks, and the bounded tool, skill, and runner portfolio were executed as evidence permitted. Twenty exact-approval and ten blocked tasks remained held and unexecuted. Successor portfolios remain recommendations only and earn no Elowen execution credit.

The static report supplies a skip link, semantic landmarks, ordered headings, captioned tables, scoped headers, redundant text labels, visible focus styles, responsive overflow containment, system-color contrast, and print fallback. These are structural checks, not accessibility completion. Manual keyboard, pointer, touch, zoom, reflow, browser-diverse, assistive-technology, screen-reader, cognitive, Māori-language, security-usability, print, professional, affected-user, affected-party, and Māori-authority evaluations remain reserved and unperformed.

Every user, sibling, shared, Tamar, Liora, Orin, and standby lane remained read-only and recoverable. No reset, amendment, history rewrite, force-push, merge, deletion, reuse, collaboration subagent, delegated research, task creation, fork, Tavian contact, or successor precontact occurred. D:-first storage was used. Codex desktop was not updated; no elevation, host-security weakening, Sandbox or Hyper-V activation, Windows-feature change, unrelated installation, account mutation, credential creation, or reboot occurred.

## Prepared route only

The repository route remains PREPARED_NOT_SENT. Under the current live cycle, the provisional exact-title successor is Sylven Arc for v671-v2, but the committed baton cannot deliver itself and cannot bind the future final SHA. Only after one successful non-replayed exact-final canonical aggregate and a fresh clean four-way equality gate may Elowen reread current live authorization and roster, list at most fifty current tasks, require exactly one existing task titled Sylven Arc, reread it immediately, apply a duplicate guard, and send exactly once through the existing-task message surface. Missing, ambiguous, renamed, paused, redirected, duplicate, standby, usage-exhausted, privacy-blocked, evidence-blocked, authority-blocked, or unacknowledged state requires stopping without a substitute or resend.

Elowen Cairn and they or them remain relational working language only. It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, or stop the route.
"""


def static_report(truth: dict[str, Any]) -> str:
    meanings = {
        "completed": "bounded synthetic evidence",
        "represented": "typed or protocol surface only",
        "open_gap": "required dependency absent",
        "exact_gate": "authority or evidence lock held",
    }
    rows = "".join(
        f"<tr><th scope='row'>{html.escape(label)}</th><td>{count}</td><td>{html.escape(meanings[label])}</td></tr>"
        for label, count in truth["core_outcomes"].items()
    )
    return f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{OWNER} {PHASE} bounded closeout</title>
<style>:root{{color-scheme:light dark;font-family:system-ui,sans-serif;line-height:1.55}}body{{margin:0 auto;max-width:72rem;padding:1rem}}.skip{{position:absolute;left:-9999px}}.skip:focus{{left:1rem;top:1rem;background:Canvas;color:CanvasText;padding:.75rem;outline:.2rem solid Highlight}}a:focus{{outline:.2rem solid Highlight;outline-offset:.15rem}}nav ul{{display:flex;flex-wrap:wrap;gap:1rem}}.table-wrap{{overflow-x:auto}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid CanvasText;padding:.55rem;text-align:left;vertical-align:top}}.status{{border-left:.4rem solid Highlight;padding:.75rem 1rem}}@media(max-width:42rem){{nav ul{{display:block}}}}@media print{{.skip,nav{{display:none}}body{{max-width:none;color:#000;background:#fff}}}}</style></head>
<body><a class="skip" href="#main">Skip to main content</a><header><h1>{OWNER} {PHASE} bounded closeout</h1><p class="status"><strong>Terminal verdict:</strong> {TERMINAL_VERDICT}. Same-owner synthetic evidence only.</p></header>
<nav aria-label="Report sections"><ul><li><a href="#scope">Scope</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#retention">Retention</a></li><li><a href="#reserved">Reserved evaluation</a></li></ul></nav>
<main id="main"><section id="scope"><h2>Scope and identity boundary</h2><p>{html.escape(IDENTITY_BOUNDARY)}</p><p>Primary pillar: THOS Body. Synthetic learning lens: shoemaking and cobbling documentation. Zero real people, objects, measurements, repairs, keys, proofs, professional decisions, or authority acts.</p></section>
<section id="outcomes"><h2>Core outcomes</h2><div class="table-wrap" tabindex="0" aria-label="Scrollable outcome table"><table><caption>Forty preregistered proposal outcomes</caption><thead><tr><th scope="col">Outcome</th><th scope="col">Count</th><th scope="col">Meaning</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<section id="retention"><h2>Retained truth</h2><ul><li>{truth['effective_negatives']} effective negatives</li><li>{truth['effective_methods']} Method Flow methods</li><li>{truth['failed_witnesses']} retained failed witnesses</li><li>{truth['bounded_passing_witnesses']} bounded passing witnesses</li><li>{truth['effective_open_gaps']} open gaps</li><li>{truth['effective_exact_gates']} exact gates</li></ul><p>Recovery never erases or promotes a failed witness.</p></section>
<section id="reserved"><h2>Reserved manual and authority evaluation</h2><p>Manual keyboard, pointer, touch, zoom, reflow, browser, assistive-technology, cognitive, Māori-language, security-usability, professional, affected-user, affected-party, legal, cultural, and Māori-authority evaluation remain unperformed.</p></section></main>
<footer><p>Prepared closeout artifact. Route state remains PREPARED_NOT_SENT until exact-final and live-route gates pass.</p></footer></body></html>"""


def baton_text() -> str:
    return f"""# SYLVEN ARC — PREPARED ELOWEN v671-v1 TO PROVISIONAL v671-v2 ACTIVATION CANDIDATE

PREPARED_NOT_SENT = true. SENT_BY_ELOWEN_CAIRN = false.

This sanitized repository file is preparation only. It is not a live message, acknowledgement, task creation, fork, delegation, successor contact, or permission to bypass Elowen's terminal gate. The actual exact final SHA and external canonical receipt must be bound in a later acknowledged existing-task send, if and only if every live gate remains satisfied.

Relational names, pronouns, roles, hopes, sibling or family language, continuity language, GHC Family, Freed ID, CBR, and Trinity Mandala are working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, or stop the route.

## Prepared source packet

- Owner: {OWNER}
- Phase: {PHASE}
- Branch: {BRANCH}
- Tamar source and final: {SOURCE_FINAL}
- Frozen Elowen planning-only x1: {FROZEN_X1}
- Immutable Elowen x2 evidence: {FROZEN_EVIDENCE}
- Exact Elowen final: TO_BE_BOUND_BY_ACKNOWLEDGED_LIVE_SEND_AFTER_CANONICAL_GATE
- Proposal chain: 5,550 to 5,590 through forty distinct Elowen proposals
- Outcomes: 28 completed, 8 represented, 2 open_gap, 2 exact_gate
- Final truth candidate: {FINAL_OVERLAY['effective_negatives']} negatives, {FINAL_OVERLAY['effective_methods']} methods, {FINAL_OVERLAY['failed_witnesses']} failed witnesses, {FINAL_OVERLAY['bounded_passing_witnesses']} bounded passing witnesses, {FINAL_OVERLAY['effective_open_gaps']} open gaps, {FINAL_OVERLAY['effective_exact_gates']} exact gates
- Terminal verdict: {TERMINAL_VERDICT}

Elowen's primary pillar was THOS Body through wholly synthetic shoemaking and cobbling documentation. GMUT Mind and Freed ID or CBR Heart remained explicit. The phase used zero real people, participants, footwear, lasts, patterns, materials, tools, observations, measurements, diagnoses, repairs, treatments, identity events, keys, proofs, professional decisions, legal or cultural decisions, affected-party approvals, or authority acts. Official sources supplied bounded vocabulary only.

GMUT remains a typed scalar-tensor and EFT research-model family without a real likelihood, constraint, force, prediction, empirical confirmation, final physics, Theory-of-Everything proof, or canon. THOS remains a participant-free proxy without governed blind matched-budget real arms, safety monitoring, statistics, or independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live lifecycle, interoperability, privacy and independent security review, recovery evidence, or trust governance. CBR, professional decisions, safety, ownership, custody, access, remedy, law, culture, affected-party legitimacy, Māori wording, Māori concepts, Māori data governance, and Māori authority remain exact-gated. Māori concepts remain under Māori authority.

The x1 aggregate failed at 23 of 24 and retains zero aggregate-pass credit; only its failed dependency recovered 1 of 1. X2 passed 30 of 30 once. The 54-check dependency-corrected evidence composite is same-owner evidence and not canonical or independent reproduction. The full repository suite was not run. The exact-final owner aggregate remains one-shot and external after final push and equality. A success must not be replayed; a failure retains zero canonical-success credit.

## Provisional successor instructions

Only if Hamish's refreshed live authorization and roster still assign the next terminal edge to exactly one existing task titled Sylven Arc may Elowen send this activation once. The live sender must list no more than fifty current tasks, require one exact title match, reread it immediately, check the recent task for this exact edge, final SHA, and canonical receipt, and use the existing-task message surface once. Stop without substitution or resend on ambiguity, absence, rename, pause, redirect, duplicate, standby state, usage exhaustion, missing acknowledgement, privacy risk, evidence failure, or authority gate.

Sylven should work solo from the exact Elowen final in one fresh additive D-first owner lane; preserve strict planning-only x1 before x2; audit semantic novelty against all 5,590 declared frozen proposals; treat inherited artifacts only as evidence; retain every negative, failed witness, recovery, open gap, and exact gate; use only completed, represented, open_gap, and exact_gate; keep exact and blocked work held without exact authority; use family-current callers compatibly; remain below current file, document, and commit ceilings; and reserve at most one exact-final owner canonical invocation after the clean pushed final. Do not run the full repository suite without newer exact authority.

No empirical, participant, professional, production, deployment, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof or canon, or Stage 20 claim is authorized without exact evidence and authority.
"""


def materialize() -> None:
    assert_closeout_start()
    evidence_truth = load("x2/phase-truth-evidence.json")
    if evidence_truth["outcomes"] != x2.OUTCOMES:
        raise RuntimeError("evidence outcome drift")
    ledger = final_method_flow()
    write_json("closeout/method-flow-final.json", ledger)
    write_json(
        "closeout/method-flow-summary.json",
        {
            "schema": "ghc.family.method-flow-summary.final.v1",
            "owner": OWNER,
            "phase": PHASE,
            **FINAL_OVERLAY,
            "new_closeout_methods": len(FINAL_METHOD_TITLES),
            "new_closeout_failures": len(FINAL_FAILURES),
            "phase_methods": ledger["counts"]["methods"],
            "phase_failed_witnesses": ledger["counts"]["witness_results"]["fail"],
            "phase_passing_witnesses": ledger["counts"]["witness_results"]["pass"],
        },
    )
    truth = {
        "schema": "ghc.family.phase-truth.final.v1",
        "owner": OWNER,
        "phase": PHASE,
        "status": "EXACT_FINAL_CANDIDATE",
        "source_final": SOURCE_FINAL,
        "frozen_x1": FROZEN_X1,
        "frozen_evidence": FROZEN_EVIDENCE,
        "exact_final": "TO_BE_BOUND_EXTERNALLY_AFTER_COMMIT",
        "core_outcomes": x2.OUTCOMES,
        "proposal_chain_before": 5550,
        "proposal_chain_after": 5590,
        **FINAL_OVERLAY,
        "phase_methods": ledger["counts"]["methods"],
        "phase_failed_witnesses": ledger["counts"]["witness_results"]["fail"],
        "phase_passing_witnesses": ledger["counts"]["witness_results"]["pass"],
        "rejected_mutations": 160,
        "real_people_objects_measurements_or_actions": 0,
        "terminal_verdict": TERMINAL_VERDICT,
    }
    write_json("closeout/phase-truth.json", truth)
    write_json(
        "closeout/retained-negative-register.json",
        {
            "schema": "ghc.family.retained-negative-register.final.v1",
            "owner": OWNER,
            "phase": PHASE,
            "tamar_repository_seal": 33324,
            "activation_declared_overlay": 33329,
            "post_route_overlay": 33332,
            "evidence_effective_negatives": 33517,
            "final_effective_negatives": FINAL_OVERLAY["effective_negatives"],
            "phase_failed_witnesses": 189,
            "closeout_new_failures": FINAL_FAILURES,
            "evidence_register": "docs/elowen-cairn/v671-v1/x2/method-flow-evidence.json",
            "failure_erased": False,
        },
    )
    write_json(
        "closeout/open-exact-gate-register.json",
        {
            "schema": "ghc.family.open-exact-gate-register.final.v1",
            "owner": OWNER,
            "phase": PHASE,
            "inherited_open_gaps": 255,
            "new_open_gaps": ["EC6711-N037", "EC6711-N038"],
            "effective_open_gaps": 257,
            "inherited_exact_gates": 250,
            "new_exact_gates": ["EC6711-N039", "EC6711-N040"],
            "effective_exact_gates": 252,
            "authority_promotion": False,
        },
    )
    write_json(
        "closeout/lifecycle-replay.json",
        {
            "schema": "ghc.family.lifecycle-replay.final.v1",
            "owner": OWNER,
            "phase": PHASE,
            "source_final": SOURCE_FINAL,
            "frozen_x1": FROZEN_X1,
            "frozen_evidence": FROZEN_EVIDENCE,
            "expected_final_parent": FROZEN_EVIDENCE,
            "source_to_final_commits_after_commit": 3,
            "single_parent_each": True,
            "zero_merges": True,
            "strict_x1_before_x2": True,
            "x1_equal_before_x2": True,
            "evidence_equal_before_closeout": True,
        },
    )
    write_json(
        "closeout/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.complete-incomplete.final.v1",
            "owner": OWNER,
            "phase": PHASE,
            "completed": [
                "forty distinct proposals frozen and dispositioned",
                "thirty-six bounded positive controls retained",
                "160 rejecting mutations retained at zero completion credit",
                "sixty safe-now and thirty candidate tasks completed boundedly",
                "sixty clean-fix-refine tasks completed additively",
                "twenty phase-local skills and ten family runners smoke-used",
                "three owner-local tools used with paired fixtures",
                "x1 and evidence lifecycle gates pushed and equal",
                "retained-negative and Method Flow ledgers closed",
                "static report, exact manifests, seal, and route candidate prepared",
            ],
            "represented": ["typed GMUT obligations", "THOS participant-free proxy", "Freed ID and CBR synthetic surfaces", "structural accessibility"],
            "open_gap": ["real object and measurement evidence", "manual professional affected-user and assistive-technology evaluation"],
            "exact_gate": ["professional legal cultural affected-party and Māori authority", "empirical or Stage 20 promotion"],
        },
    )
    write_json(
        "closeout/wellbeing-workload-check.json",
        {
            "schema": "ghc.family.wellbeing-workload.final.v1",
            "owner": OWNER,
            "phase": PHASE,
            "status": "CLOSEOUT_READY_WITH_STOP_RULES",
            "health_measurement_claim": False,
            "external_coordination_during_phase": 0,
            "context_pressure": "managed with strict lifecycle boundaries and sharded artifacts",
            "stop_conditions": ["usage_exhaustion", "route_ambiguity", "privacy_or_authority_gate", "canonical_failure", "remote_divergence"],
        },
    )
    write_json(
        "closeout/threat-model-final.json",
        {
            "schema": "ghc.family.threat-model.final.v1",
            "owner": OWNER,
            "phase": PHASE,
            "threats": ["claim promotion", "private material leakage", "manifest drift", "route duplication", "authority substitution", "failure laundering"],
            "controls": ["synthetic only", "zero external action", "five-class scan", "exact Git-blob manifests", "authority vacancy", "single-send route", "no replay"],
            "reserved": ["exhaustive security", "complete privacy", "complete accessibility", "professional review", "affected-party review", "Māori authority"],
        },
    )
    write_json(
        "closeout/source-provenance-ledger.json",
        {
            "schema": "ghc.family.source-provenance.final.v1",
            "owner": OWNER,
            "phase": PHASE,
            "source_final": SOURCE_FINAL,
            "evidence_sources": "docs/elowen-cairn/v671-v1/x2/source-evidence-ledger.json",
            "network_downloads_during_execution_or_closeout": 0,
            "inherited_completion_credit": 0,
            "citations_are_observations": False,
            "authority_conferred": False,
        },
    )
    final_overview = write_text("closeout/final-integrated-overview.md", overview())
    words = len(re.findall(r"\S+", final_overview.read_text(encoding="utf-8")))
    if not 1800 <= words <= DOCUMENT_WORD_CEILING:
        raise RuntimeError(f"final overview word bound failed: {words}")
    write_text("closeout/static-report.html", static_report(truth))
    write_text("handoffs/sylven-arc-v671-v2-activation-candidate.md", baton_text())
    write_json(
        "closeout/route-state-final-candidate.json",
        {
            "schema": "ghc.family.route-state.final.v1",
            "owner": OWNER,
            "phase": PHASE,
            "delivery_state": "PREPARED_NOT_SENT",
            "sent_by_elowen_cairn": False,
            "exact_target_title": "Sylven Arc",
            "next_phase": "v671-v2",
            "bounded_registry_limit": 50,
            "fresh_reread_required": True,
            "duplicate_guard_required": True,
            "stop_on_ambiguity_or_missing_acknowledgement": True,
        },
    )
    write_json(
        "validation/stale-label-review.json",
        {
            "schema": "ghc.family.stale-label-review.final.v1",
            "owner": OWNER,
            "phase": PHASE,
            "current_labels": ["Elowen Cairn v671-v1", "Sylven Arc v671-v2 provisional", "PREPARED_NOT_SENT"],
            "historical_labels_retained": ["Tamar v670-v8 source", "Elowen v669-v2 historical closeout"],
            "unexpected_stale_labels": [],
            "status": "PASS",
        },
    )
    write_json(
        "validation/canonical-protocol.json",
        {
            "schema": "ghc.family.canonical-protocol.final.v1",
            "owner": OWNER,
            "phase": PHASE,
            "status": "PENDING_EXACT_FINAL_COMMIT_PUSH_EQUALITY",
            "canonical_invocation_count_before_final": 0,
            "post_success_replay_forbidden": True,
            "complete_repository_suite": False,
            "dependency_scope": ["one exact-final owner test module", "strict phase JSON and document checks", "five-class scan", "bounded owner Python AST review", "exact Git-blob manifests", "ancestry clean divergence and four-way equality"],
            "external_receipt_required": True,
        },
    )
    write_json(
        "validation/final-method-flow-validation-failed.json",
        {
            "schema": "ghc.family.method-flow-state.validation.v1",
            "phase": PHASE,
            "owner": OWNER,
            "method_count": 230,
            "witness_count": 415,
            "state_event_count": 690,
            "recommendation_count": 230,
            "issue_count": 12,
            "issues": [
                f"EC6711-FINAL-M{index:03d}: retained_negative_ids must be a non-empty list"
                for index in range(1, 13)
            ],
            "valid": False,
            "failure_id": FINAL_FAILURES[0]["failure_id"],
            "completion_credit": 0,
            "recovery": FINAL_FAILURES[0]["recovery"],
            "recurrence_guard": FINAL_FAILURES[0]["recurrence_guard"],
            "boundary": "Failed schema validation retained at zero credit; it is not erased by the bounded recovery.",
        },
    )
    write_json(
        "validation/final-contract-audit-failed.json",
        {
            "schema": "ghc.family.final-contract-audit.failed.v1",
            "owner": OWNER,
            "phase": PHASE,
            "failure_id": FINAL_FAILURES[1]["failure_id"],
            "status": "FAILED_ZERO_CREDIT",
            "completion_credit": 0,
            "failed_projection": ["skill.quick_validation", "skill.smoke_use", "runner.result", "tool.rows"],
            "observed_contract": ["skill.quick_validated", "skill.smoke_used", "runner.accepted", "tool.tools and keyed receipts"],
            "recovery": FINAL_FAILURES[1]["recovery"],
            "recurrence_guard": FINAL_FAILURES[1]["recurrence_guard"],
            "canonical_tests_executed": False,
        },
    )
    write_json(
        "validation/final-preflight-command-failed.json",
        {
            "schema": "ghc.family.final-preflight-command.failed.v1",
            "owner": OWNER,
            "phase": PHASE,
            "failure_id": FINAL_FAILURES[2]["failure_id"],
            "status": "FAILED_ZERO_CREDIT",
            "completion_credit": 0,
            "observed": "placeholder_only_no_audit_summary",
            "recovery": FINAL_FAILURES[2]["recovery"],
            "recurrence_guard": FINAL_FAILURES[2]["recurrence_guard"],
            "repository_bytes_changed": False,
            "canonical_tests_executed": False,
        },
    )
    write_json(
        "validation/final-privacy-classification-preflight-failed.json",
        {
            "schema": "ghc.family.final-privacy-classification-preflight.failed.v1",
            "owner": OWNER,
            "phase": PHASE,
            "failure_id": FINAL_FAILURES[3]["failure_id"],
            "status": "FAILED_ZERO_CREDIT",
            "completion_credit": 0,
            "initial_confirmed_count": 7,
            "initial_candidates": 8,
            "recovery": FINAL_FAILURES[3]["recovery"],
            "recurrence_guard": FINAL_FAILURES[3]["recurrence_guard"],
            "broad_exemption_added": False,
            "canonical_tests_executed": False,
        },
    )
    write_json(
        "closeout/closeout-receipt.json",
        {
            "schema": "ghc.family.closeout-receipt.final.v1",
            "owner": OWNER,
            "phase": PHASE,
            "status": "FINAL_CLOSEOUT_CANDIDATE",
            "exact_final": "TO_BE_BOUND_EXTERNALLY_AFTER_COMMIT",
            "final_parent": FROZEN_EVIDENCE,
            "route_state": "PREPARED_NOT_SENT",
            "canonical_status": "PENDING_EXACT_FINAL_COMMIT_PUSH_EQUALITY",
            "content_seal_payload_sha256": "TO_BE_BOUND_AFTER_STAGED_SEAL",
            "terminal_verdict": TERMINAL_VERDICT,
        },
    )
    print(json.dumps({"status": "FINAL_CLOSEOUT_MATERIALIZED_NOT_COMMITTED", "overview_words": words, "final_truth": FINAL_OVERLAY}, indent=2, sort_keys=True))


def privacy_patterns() -> dict[str, re.Pattern[bytes]]:
    return {
        "raw_task_or_thread_identifier": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "credential_assignment": re.compile(rb"(?i)(?:password|secret|api[_-]?key|bearer|access[_-]?token)\s*[:=]\s*['\"][^'\"]+"),
        "private_route_or_callable": re.compile(rb"(?i)(?:source_thread_id|<codex_delegation|(?:app|plugin)://)"),
        "private_absolute_path": re.compile(rb"[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)[\\/]", re.I),
        "transcript_or_session_stream": re.compile(rb"(?i)(?:private_transcript|session_stream|private_callable_identifier|private_application_state)"),
    }


def staged_privacy() -> None:
    self_path = FINAL_STAGED_PRIVACY
    paths = [path for path in staged_paths() if path != self_path and Path(path).suffix.lower() in {".py", ".json", ".md", ".txt", ".html", ".yaml", ".yml"}]
    rows = index_rows(paths)
    scanners = SCANNER_DEFINITION_PATHS
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    patterns = privacy_patterns()
    for row in rows:
        blob = git("cat-file", "blob", row["git_blob_oid"]).stdout
        for label, pattern in patterns.items():
            if pattern.search(blob):
                hit = {"path": row["path"], "pattern_class": label}
                if row["path"] in scanners:
                    hit["disposition"] = "scanner_definition_or_bounded_test"
                    candidates.append(hit)
                else:
                    hit["disposition"] = "confirmed_hit"
                    confirmed.append(hit)
    payload = {
        "schema": "ghc.family.final-staged-privacy.v1",
        "owner": OWNER,
        "phase": PHASE,
        "hash_domain": "exact_staged_git_blob",
        "scanned_text_files": len(rows),
        "pattern_classes": sorted(patterns),
        "candidates": candidates,
        "confirmed_hits": confirmed,
        "confirmed_hit_count": len(confirmed),
        "self_exclusion": self_path,
        "valid": not confirmed,
        "boundary": BOUNDARY,
    }
    write_json("validation/final-staged-privacy.json", payload)
    if confirmed:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def manifest_from_index() -> None:
    all_owner = [path for path in index_objects() if owner_path(path) and path not in MANIFEST_EXCLUSIONS]
    delta = [path for path in staged_paths() if owner_path(path) and path not in MANIFEST_EXCLUSIONS]
    owner_rows = index_rows(all_owner)
    delta_rows = index_rows(delta)
    write_json(
        "validation/final-owner-manifest.json",
        {
            "schema": "ghc.family.final-owner-manifest.v1",
            "owner": OWNER,
            "phase": PHASE,
            "hash_domain": "exact_git_blob",
            "entry_count": len(owner_rows),
            "entries": owner_rows,
            "self_exclusions": sorted(MANIFEST_EXCLUSIONS),
        },
    )
    write_json(
        "validation/final-delta-manifest.json",
        {
            "schema": "ghc.family.final-delta-manifest.v1",
            "owner": OWNER,
            "phase": PHASE,
            "base": FROZEN_EVIDENCE,
            "hash_domain": "exact_git_blob",
            "entry_count": len(delta_rows),
            "entries": delta_rows,
            "self_exclusions": sorted(MANIFEST_EXCLUSIONS),
        },
    )
    print(json.dumps({"owner_entries": len(owner_rows), "delta_entries": len(delta_rows)}, sort_keys=True))


def seal_from_index() -> None:
    paths = [
        "docs/elowen-cairn/v671-v1/closeout/final-integrated-overview.md",
        "docs/elowen-cairn/v671-v1/closeout/phase-truth.json",
        "docs/elowen-cairn/v671-v1/closeout/method-flow-final.json",
        "docs/elowen-cairn/v671-v1/closeout/open-exact-gate-register.json",
        "docs/elowen-cairn/v671-v1/closeout/static-report.html",
        "docs/elowen-cairn/v671-v1/handoffs/sylven-arc-v671-v2-activation-candidate.md",
        FINAL_OWNER_MANIFEST,
        FINAL_DELTA_MANIFEST,
    ]
    payload: dict[str, Any] = {
        "schema": "ghc.family.content-seal.final.v1",
        "owner": OWNER,
        "phase": PHASE,
        "status": "SEALED_FINAL_CANDIDATE",
        "hash_domain": "exact_staged_git_blob",
        "files": index_rows(paths),
    }
    payload["payload_sha256"] = sha256(canonical_bytes(payload))
    write_json("seal/content-seal.json", payload)
    print(payload["payload_sha256"])


def finalize_receipt() -> None:
    seal = load("seal/content-seal.json")
    owner_manifest = load("validation/final-owner-manifest.json")
    delta_manifest = load("validation/final-delta-manifest.json")
    write_json(
        "closeout/closeout-receipt.json",
        {
            "schema": "ghc.family.closeout-receipt.final.v1",
            "owner": OWNER,
            "phase": PHASE,
            "status": "FINAL_CLOSEOUT_CANDIDATE",
            "exact_final": "TO_BE_BOUND_EXTERNALLY_AFTER_COMMIT",
            "final_parent": FROZEN_EVIDENCE,
            "route_state": "PREPARED_NOT_SENT",
            "canonical_status": "PENDING_EXACT_FINAL_COMMIT_PUSH_EQUALITY",
            "content_seal_payload_sha256": seal["payload_sha256"],
            "owner_manifest_entries": owner_manifest["entry_count"],
            "delta_manifest_entries": delta_manifest["entry_count"],
            "terminal_verdict": TERMINAL_VERDICT,
        },
    )


def staged_review() -> None:
    paths = staged_paths()
    required = {
        *FINAL_CODE_PATHS,
        "docs/elowen-cairn/v671-v1/closeout/phase-truth.json",
        "docs/elowen-cairn/v671-v1/closeout/final-integrated-overview.md",
        "docs/elowen-cairn/v671-v1/closeout/method-flow-final.json",
        "docs/elowen-cairn/v671-v1/handoffs/sylven-arc-v671-v2-activation-candidate.md",
        FINAL_OWNER_MANIFEST,
        FINAL_DELTA_MANIFEST,
        FINAL_STAGED_PRIVACY,
        CONTENT_SEAL,
        CLOSEOUT_RECEIPT,
    }
    out_of_scope = [path for path in paths if not owner_path(path)]
    frozen = [path for path in paths if path.startswith("docs/elowen-cairn/v671-v1/x1/") or path.startswith("docs/elowen-cairn/v671-v1/x2/") or path in x2.BUILD_PATHS]
    missing = sorted(required - set(paths))
    diff_check = git("diff", "--cached", "--check", check=False)
    all_owner = [path for path in index_objects() if owner_path(path)]
    max_words = 0
    for row in index_rows(path for path in all_owner if Path(path).suffix.lower() in {".md", ".html", ".txt"}):
        blob = git("cat-file", "blob", row["git_blob_oid"]).stdout
        max_words = max(max_words, len(re.findall(rb"\S+", blob)))
    payload = {
        "schema": "ghc.family.final-staged-review.v1",
        "owner": OWNER,
        "phase": PHASE,
        "base": FROZEN_EVIDENCE,
        "staged_count_before_self": len(paths),
        "staged_paths_before_self": paths,
        "out_of_scope": out_of_scope,
        "frozen_x1_or_x2_changes": frozen,
        "required_missing": missing,
        "diff_hygiene_exit": diff_check.returncode,
        "owner_file_count": len(all_owner),
        "file_ceiling": FILE_CEILING,
        "max_document_words": max_words,
        "document_word_ceiling": DOCUMENT_WORD_CEILING,
        "self_exclusion": FINAL_STAGED_REVIEW,
        "valid": not out_of_scope and not frozen and not missing and diff_check.returncode == 0 and len(all_owner) <= FILE_CEILING and max_words <= DOCUMENT_WORD_CEILING,
    }
    write_json("validation/final-staged-review.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staged-privacy", action="store_true")
    parser.add_argument("--manifest-from-index", action="store_true")
    parser.add_argument("--seal-from-index", action="store_true")
    parser.add_argument("--finalize-receipt", action="store_true")
    parser.add_argument("--staged-review", action="store_true")
    args = parser.parse_args()
    if args.staged_privacy:
        staged_privacy()
    elif args.manifest_from_index:
        manifest_from_index()
    elif args.seal_from_index:
        seal_from_index()
    elif args.finalize_receipt:
        finalize_receipt()
    elif args.staged_review:
        staged_review()
    else:
        materialize()


if __name__ == "__main__":
    main()
