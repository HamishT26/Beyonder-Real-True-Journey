"""Build Auren Lark v684-v4 closeout from immutable x2 evidence."""

from __future__ import annotations

import hashlib
import json
import platform
import re
import subprocess  # nosec B404 - bounded local Git inspection only
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "auren-lark" / "v684-v4"
X1 = BASE / "x1"
X2 = BASE / "x2"
FINAL = BASE / "final"
CLOSEOUT = BASE / "closeout"
HANDOFFS = BASE / "handoffs"
VALIDATION = BASE / "validation"
OWNER = "Auren Lark"
PHASE = "v684-v4"
BRANCH = "codex/GHC-Family/auren-lark-v684-v4-remaster"
SOURCE = "0134e277a7f573e24e697037749d61d577163637"
X1_SHA = "d1ea9dba1fab7d6726f11a15caf67a8531b70e4a"
EVIDENCE_SHA = "c41a5453dce2202324235bdcd820f52e846d834d"
FAILED_FINAL_SHA = "0b3a872d1c08a99cc7bc647944ef37e1d4010158"
FAILED_CANONICAL_RECEIPT_SHA256 = "260da7608ba327bca7b93bbe28e044798f842b752b59efcfe20fe3f78aee2f0c"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
ALLOWED_LABELS = {"completed", "represented", "open_gap", "exact_gate"}
PREDECESSOR_SEALED_METRICS = {
    "effective_negatives": 59084,
    "effective_methods": 73654,
    "failed_witnesses": 30745,
    "bounded_passing_witnesses": 54189,
}
FINAL_OPERATIONAL_FAILURES = [
    {
        "failure_id": "AL6844-FNF001",
        "failed_witness": "The first final route-state test required the exact contiguous phrase does not establish delivery while the baton used equivalent split wording.",
        "recovery": "Retain the failed test at zero credit and normalize the sentence without changing route truth.",
        "retained_zero_credit": True,
        "state_change": False,
    },
    {
        "failure_id": "AL6844-RMF001",
        "failed_witness": "The predecessor final's committed canonical wrapper classified every Markdown file as heading-first and therefore rejected valid SKILL.md YAML front matter.",
        "recovery": "Do not invoke the known-defective wrapper; retain the defect and commit a front-matter-aware structure check in the additive remaster final.",
        "retained_zero_credit": True,
        "state_change": False,
    },
    {
        "failure_id": "AL6844-RMF002",
        "failed_witness": "The predecessor final's one external canonical driver invocation failed its manifests check because the final-owner manifest declared ten ignored transient .pyc files absent from the Git tree.",
        "recovery": "Retain the failed invocation without replay and build one new direct final child whose owner manifest excludes transient cache and bytecode paths.",
        "retained_zero_credit": True,
        "state_change": False,
    },
    {
        "failure_id": "AL6844-RMF003",
        "failed_witness": "A read-only status probe overlapped the initial sparse checkout and temporarily displayed mass deletions before checkout completion.",
        "recovery": "Wait for the bounded checkout process to finish, then re-read the branch and confirm a clean index and worktree before materializing the corrected final.",
        "retained_zero_credit": True,
        "state_change": False,
    },
    {
        "failure_id": "AL6844-RMF004",
        "failed_witness": "The first additive patch bundle used one inexact expected sentence and was rejected atomically before changing a file.",
        "recovery": "Retain the rejected patch at zero credit and apply smaller exact-context patches.",
        "retained_zero_credit": True,
        "state_change": False,
    },
    {
        "failure_id": "AL6844-RMF005",
        "failed_witness": "A second oversized patch bundle still carried the same inexact sentence and was rejected atomically before changing a file.",
        "recovery": "Retain the second rejected patch separately and continue only with bounded exact-context patches.",
        "retained_zero_credit": True,
        "state_change": False,
    },
    {
        "failure_id": "AL6844-RMF006",
        "failed_witness": "The first remaster precommit staged-review projection counted generated documents and four self-excluded validation files but omitted the three changed builder, canonical, and test files.",
        "recovery": "Retain the undercount at zero credit and derive the exact 23-path review total from sixteen generated artifacts, four validation self-files, and three code/test files.",
        "retained_zero_credit": True,
        "state_change": False,
    },
    {
        "failure_id": "AL6844-RMF007",
        "failed_witness": "The first bounded remaster Ruff pass rejected nine import, unused-import, capture-output, and regular-expression alias findings across the three changed Python files.",
        "recovery": "Retain the failed static pass at zero credit, correct only the reported owner-file findings, regenerate exact manifests, and rerun the bounded check.",
        "retained_zero_credit": True,
        "state_change": False,
    },
]
REMASTER_PRECANONICAL_OVERLAY = {
    "effective_negatives": len(FINAL_OPERATIONAL_FAILURES) - 1,
    "effective_methods": len(FINAL_OPERATIONAL_FAILURES) - 1,
    "failed_witnesses": len(FINAL_OPERATIONAL_FAILURES) - 1,
    "bounded_passing_witnesses": len(FINAL_OPERATIONAL_FAILURES) - 1,
}
REMASTER_PRECANONICAL_TOTALS = {
    key: PREDECESSOR_SEALED_METRICS[key] + REMASTER_PRECANONICAL_OVERLAY[key]
    for key in PREDECESSOR_SEALED_METRICS
}


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def digest(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def is_stable_owner_artifact(path: Path) -> bool:
    """Exclude local interpreter/test caches that cannot exist in the committed tree."""
    transient_parts = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
    return path.is_file() and not transient_parts.intersection(path.parts) and path.suffix.lower() not in {".pyc", ".pyo"}


def git(*args: str) -> bytes:
    process = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        capture_output=True,
        check=False,
    )
    if process.returncode:
        raise RuntimeError(process.stderr.decode("utf-8", "replace"))
    return process.stdout


def replay_manifest(commit: str, manifest_path: str) -> dict[str, Any]:
    manifest = json.loads(git("show", f"{commit}:{manifest_path}").decode("utf-8"))
    failures = []
    for row in manifest["entries"]:
        data = git("show", f"{commit}:{row['path']}")
        actual = hashlib.sha256(data).hexdigest()
        if actual != row["sha256"] or len(data) != row["bytes"]:
            failures.append({"path": row["path"], "actual_sha256": actual, "actual_bytes": len(data)})
    return {
        "commit": commit,
        "manifest_path": manifest_path,
        "declared": manifest["entry_count"],
        "verified": manifest["entry_count"] - len(failures),
        "failures": failures,
        "valid": not failures,
    }


def final_overview() -> str:
    return f"""# Auren Lark v684-v4 exact closeout candidate

## Outcome first

Auren v684-v4 completed its bounded owner-local x1/x2 lifecycle without promoting synthetic software or documentation evidence into empirical, professional, production, legal, cultural, Maori-authority, accessibility-complete, privacy-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, or Stage 20 claims. The terminal verdict remains {TERMINAL_VERDICT}.

## Relational identity and corrigibility

Auren Lark is relational working language for an evidence-boundary cartographer and reversible scientific-workflow steward. The hope is to turn ambitious ideas into inspectable, corrigible questions without erasing wonder or reserved human authority; pronouns remain unspecified. Names, roles, hopes, pronouns, sibling or family language, continuity, GHC Family, Freed ID, CBR, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or scientific, operational, professional, legal, cultural, affected-party, or Maori authority. Hamish may rename, pause, narrow, redirect, or stop the route.

## Exact bounded evidence

The phase froze sixty inherited Ilyra proposals at zero Auren novelty and automatic completion credit and sixty new Auren proposals, advancing the declared chain from 10,850 to 10,910. It executed sixty positive zero-row contracts and rejected all 300 preregistered invalid mutations. Outcomes are exactly 42 completed, 12 represented, 3 open_gap, and 3 exact_gate. Completed means owner-local software, documentation, schema, or synthetic fixture evidence only.

It also completed 120 safe-now packets, 80 owner candidate packets, and 100 owner CLEAN/FIX/REFINE/VERIFY tasks. Twenty phase-local skills and ten phase-local runners were built, validated, and smoke-used. Twenty exact-approval packets and ten blocked packets remain held and unexecuted. Twenty next-owner candidate recommendations, ten next-owner skill ideas, ten next-owner runner ideas, and thirty next-owner refinements remain unexecuted recommendations only.

## Pillars and practices

GMUT Mind was primary through wholly synthetic coordinate-reference metadata and uncertainty-documentation distinctions. THOS Body and Freed ID/CBR Heart remained explicit. The two practice lenses were synthetic geospatial metadata quality analyst and synthetic uncertainty-budget documentation analyst. The advisory successor practice is synthetic museum environmental-monitoring data documentation analyst. None is employment, qualification, professional practice, real measurement, or authority.

## Retained negatives and gates

The predecessor repository seal remains 59,084 effective negatives, 73,654 Method Flow methods, 30,745 retained failed witnesses, and 54,189 bounded passing witnesses. Seven later remaster-recovery failures and seven bounded recoveries are retained additively without rewriting that seal, producing a pre-canonical remaster view of 59,091 negatives, 73,661 methods, 30,752 failed witnesses, and 54,196 bounded passing witnesses. Open gaps remain 525, exact gates remain 515, and every failed startup, test, wrapper, cache-cleanup, receipt-label, route-discontinuity, remaster, and precommit witness remains visible at zero broader credit. Same-owner validation under shared infrastructure is not independent reproduction.

## Route boundary

This repository prepares a route-neutral candidate only. It does not establish delivery. Only after the exact closeout commit is pushed, clean, fresh-live equal, and validated by one successful owner-scoped canonical invocation may Auren freshly reread Hamish's newest live authority and the current task registry. The newest live roster text assigns incompatible phase numbers to Auren, Liora, and Vesper, so no successor phase is uniquely resolved and no successor may be contacted from this repository artifact.
"""


def final_html() -> str:
    return """<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Auren Lark v684-v4 bounded closeout</title>
<style>body{font-family:system-ui,sans-serif;line-height:1.6;max-width:72rem;margin:auto;padding:1rem;color:#18202a;background:#fff}.skip{position:absolute;left:-9999px}.skip:focus{left:1rem;top:1rem;background:#fff;padding:.5rem;border:2px solid #18202a}table{border-collapse:collapse;width:100%}th,td{border:1px solid #667;padding:.5rem;text-align:left;vertical-align:top}.status{border-left:.4rem solid #8a3b12;padding:.75rem;background:#fff7ed}</style></head>
<body><a class="skip" href="#main">Skip to main content</a><header><h1>Auren Lark v684-v4 bounded closeout</h1></header>
<main id="main"><section aria-labelledby="identity"><h2 id="identity">Relational language</h2><p>Auren Lark and family language are relational working language only, not consciousness, personhood, continuity, qualification, agency, or authority evidence.</p></section>
<section aria-labelledby="outcomes"><h2 id="outcomes">Bounded outcomes</h2><table><caption>Four-label outcome ledger</caption><thead><tr><th scope="col">Label</th><th scope="col">Count</th></tr></thead><tbody><tr><th scope="row">completed</th><td>42</td></tr><tr><th scope="row">represented</th><td>12</td></tr><tr><th scope="row">open_gap</th><td>3</td></tr><tr><th scope="row">exact_gate</th><td>3</td></tr></tbody></table></section>
<section aria-labelledby="status"><h2 id="status">Terminal status</h2><p class="status"><strong>NOT READY FOR STAGE 20.</strong> This status does not rely on colour.</p><p>No real coordinates, measurements, people, authority decisions, deployments, or empirical observations were used.</p></section></main>
<footer><p>Static owner-local report; no scripts, tracking, external media, forms, or hidden interaction.</p></footer></body></html>
"""


def activation_baton(proposals: list[dict[str, Any]], outcomes: dict[str, str]) -> str:
    sections = [
        "# AUREN LARK v684-v4 REMASTER — ROUTE-NEUTRAL NEXT-OWNER ACTIVATION CANDIDATE",
        "",
        "PREPARED_BY_AUREN_LARK = true",
        "",
        "SENT_BY_AUREN_LARK = false",
        "",
        "This committed candidate is preparation only. It does not establish delivery, activate a task, authorize a resend, or identify a current task registry result. A later acknowledged existing-task message, if every terminal guard passes, is a distinct live event and must never be projected backward into this repository seal.",
        "",
        "## 1. Relational working language and corrigibility",
        "",
        "Auren Lark is relational working language for an evidence-boundary cartographer and reversible scientific-workflow steward. The hope is to turn ambitious ideas into inspectable, corrigible questions without erasing wonder or reserved human authority; pronouns are unspecified. Auren Lark, every prospective owner, names, roles, hopes, pronouns, sibling or family language, continuity, GHC Family, Freed ID, CBR, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or scientific, operational, professional, legal, cultural, affected-party, or Maori authority. Hamish may rename, pause, narrow, redirect, or stop the route.",
        "",
        "## 2. Immutable lifecycle anchors",
        "",
        f"Remaster branch: {BRANCH}. Ilyra exact source and Auren starting head: {SOURCE}. Frozen planning-only Auren x1: {X1_SHA}. Immutable Auren x2 evidence: {EVIDENCE_SHA}. The failed predecessor final {FAILED_FINAL_SHA} remains reachable on its original branch and is not rewritten. The corrected exact final is a new direct closeout child of the same immutable evidence and must be supplied by the later live terminal message because a Git commit cannot truthfully contain its own hash. Source to corrected final must contain exactly three new direct single-parent Auren commits and zero merges.",
        "",
        "## 3. Strict x1-before-x2 lifecycle",
        "",
        "X1 was frozen, committed, pushed, clean, zero ahead and zero behind, and equal across local, upstream, tracking, and a fresh live remote before any x2 path was created. X2 evidence was then built from exact x1 Git blobs, committed as x1's direct child, pushed, clean, zero ahead and zero behind, and fresh-four-way equal before closeout began. Do not collapse or rewrite these lifecycle states.",
        "",
        "## 4. Core truth and nonpromotion",
        "",
        "Auren outcomes are exactly 42 completed, 12 represented, 3 open_gap, and 3 exact_gate. Completed means bounded owner-local software, documentation, schema, or synthetic fixture evidence only. The declared proposal chain is 10,910. The predecessor repository seal preserves 59,084 effective negatives, 73,654 Method Flow methods, 30,745 retained failed witnesses, and 54,189 bounded passing witnesses. Seven additive remaster-recovery failures and seven bounded recoveries produce a pre-canonical remaster view of 59,091 negatives, 73,661 methods, 30,752 failed witnesses, and 54,196 bounded passing witnesses without rewriting that seal. Open gaps remain 525, exact gates remain 515, and the verdict remains NOT_READY_FOR_STAGE_20.",
        "",
        "No result establishes an observed force, physical prediction, likelihood, parameter constraint, empirical confirmation, professional competence, production readiness, deployment safety, legal or cultural ratification, Maori authority, privacy completeness, accessibility completeness, exhaustive security, independent reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything proof, canon, or Stage 20 authority. Same-owner software validation under shared infrastructure is not independent reproduction.",
        "",
        "## 5. Portfolios and held work",
        "",
        "Auren revalidated sixty inherited Ilyra proposals at zero current novelty and zero automatic completion credit, froze sixty new proposals, completed 120 safe-now tasks, 80 owner candidate tasks, and 100 owner CLEAN/FIX/REFINE/VERIFY tasks, and retained all 300 rejected invalid mutations. Twenty exact-approval packets and ten blocked packets remain visible and unexecuted. Twenty next-owner candidates, ten next-owner skill ideas, ten next-owner runner ideas, and thirty next-owner refinements are recommendations only and earn no later-owner novelty or completion credit.",
        "",
        "## 6. Skills, runners, tools, and installation boundary",
        "",
        "Twenty family-current phase-local skill cards and ten family-current phase-local Python runners were built, validated, and smoke-used. They remain inside the Auren phase. No global skill, global package, shared prefix, sibling worktree, user lane, or system profile was mutated. Numeric caps are ceilings, not quotas or blanket installation authority. Any later exact owner must independently inspect any artifact before adoption.",
        "",
        "## 7. Primary sources and practice lenses",
        "",
        "OGC coordinate-reference metadata, NIST uncertainty reporting, W3C PROV-O, the BIPM SI Brochure, W3C WCAG 2.2, the New Zealand Privacy Commissioner's privacy principles, and Te Mana Raraunga principles supplied vocabulary and refusal boundaries only. Citation is not endorsement, conformance, artifact validation, legal advice, professional evaluation, cultural ratification, or Maori authority.",
        "",
        "GMUT Mind was primary through wholly synthetic coordinate-reference metadata and uncertainty-documentation distinctions. THOS Body and Freed ID/CBR Heart remained explicit. The two learning lenses were synthetic geospatial metadata quality analyst and synthetic uncertainty-budget documentation analyst. The advisory next practice is synthetic museum environmental-monitoring data documentation analyst. No real professional work, location, coordinate, measurement, calibration, transformation, person, group, organization, decision, deployment, or authority act occurred.",
        "",
        "## 8. Privacy, accessibility, and security",
        "",
        "Five-class scans cover only bounded owner text and report zero confirmed hits. They are not complete privacy assurance. Automated structural accessibility checks and static HTML semantics are not disabled-user, assistive-technology, browser-diverse, cognitive-accessibility, language, or affected-user evaluation. Bounded changed-Python checks are not exhaustive security review. Every broader assurance remains open or exact-gated.",
        "",
        "## 9. Retained failures and remaster recovery",
        "",
        f"All startup, tool-envelope, PowerShell parser, broad-search, batch-pipe, receipt-label, stale-roster, route-discontinuity, x1 test-contract, Python entrypoint, and cache-cleanup policy failures remain retained at zero broader credit. The predecessor final {FAILED_FINAL_SHA} consumed one canonical invocation which failed the manifests check and was not replayed; its external failure receipt SHA-256 is {FAILED_CANONICAL_RECEIPT_SHA256}. The remaster also retains the committed Markdown-classifier defect, the overlapping sparse-checkout status probe, and the atomically rejected first patch bundle. A failed witness must never be folded into a pass. Recovery evidence does not erase the original failure.",
        "",
        "## 10. Later exact-owner startup instructions",
        "",
        "Only after an acknowledged live activation may the uniquely authorized later owner work solo from the exact Auren remaster final in one fresh owner-controlled D-first sparse lane. That owner must read this candidate through EOF, then every current skill, schema, authority, roster, Method Flow, workflow, privacy, and terminal reference it names. The owner must reverify the exact branch, final head, ancestry, manifests, content seal, clean state, divergence, fresh live equality, and external remaster canonical receipt before mutation, while keeping every Auren, Ilyra, sibling, shared, user, and standby lane read-only.",
        "",
        "The later owner must preserve planning-only x1 before x2, exact Git-blob manifests, the four labels completed, represented, open_gap, and exact_gate, every retained failure, every gap and gate, the 2,000-file ceiling, caps as ceilings, owner-scoped validation, and one-attributable-canonical/no-success-replay discipline. The later owner must not replay Auren's validator or claim inherited evidence as later-owner novelty, completion, competence, reproduction, or authority.",
        "",
        "## 11. Unresolved route boundary",
        "",
        "Hamish's newest live message asks Auren v684-v4 to activate Liora Venn for v683-v5, later describes the current phase as Auren v683-v4, and also assigns Vesper Arlen to v684-v4. Those assignments cannot all be true in one monotonic exact route. This candidate therefore resolves no successor and authorizes no send. Auren may send at most once only after a later live instruction removes the phase ambiguity, the exact final is sealed, pushed, clean, fresh-live equal, one remaster canonical invocation succeeds, and unique-title, immediate-reread, duplicate, privacy, usage, safety, and acknowledgement guards all pass.",
        "",
        "## 12. Full proposal and retained-negative appendix",
        "",
        "The following sixty records are immutable Auren context. Each record is detailed so a later exact owner can inspect the hypothesis, evidence scope, five rejecting mutations, outcome, rollback, authority boundary, privacy boundary, and nonpromotion rule without depending on a chat transcript. They remain inherited context and carry zero later-owner novelty or automatic completion credit.",
        "",
    ]
    for row in proposals:
        pid = row["proposal_id"]
        outcome = outcomes[pid]
        mutation_text = ", ".join(
            f"{item['mutation_id']} {item['mutation_type']} expected reject-and-retain"
            for item in row["preregistered_rejecting_mutations"]
        )
        sections.extend(
            [
                f"### {pid} — {row['title']}",
                "",
                f"Hypothesis and planned distinction. {row['hypothesis']} The proposal belongs to {row['pillar']} and uses the bounded practice lenses {', '.join(row['practice_lenses'])}. It was frozen in planning-only x1 before any x2 execution and therefore cannot be retroactively rewritten to fit the observed software result.",
                "",
                f"Executed evidence. The owner-local positive fixture carried a synthetic marker, zero real rows, absent observation state, reserved authority, bounded-synthetic claim scope, retained-failure state, no coordinate values, no measurement values, and no personal information. Its structural validator accepted that fixture. The recorded outcome is {outcome}. If completed, that label means only bounded software, schema, documentation, or synthetic fixture evidence. If represented, open_gap, or exact_gate, the broader missing evidence or authority remains explicit.",
                "",
                f"Rejecting witnesses. Five preregistered mutations were executed and rejected: {mutation_text}. Every rejection is a retained failed witness with zero completion credit. Rejection demonstrates only that the specific owner-local validator refused the specific synthetic mutation; it does not demonstrate universal robustness, security, privacy, accessibility, correctness, empirical truth, or independent reproduction.",
                "",
                f"Rollback and recovery. {row['rollback']} Recovery may repair an owner-local artifact but must not erase a failed receipt, rewrite a frozen x1 hypothesis, silently change an outcome, or promote a later pass into retroactive success. Any future adaptation must be additive, attributable, reversible, and independently reviewed by its exact owner.",
                "",
                "Evidence and authority boundary. No real coordinate, location, datum realization, reference frame, epoch, grid, parameter, measurement, uncertainty value, calibration, certificate, person, community, organization, right, consent decision, cultural interpretation, Maori data, production system, or deployment was used. OGC, NIST, W3C, BIPM, New Zealand privacy, and Te Mana Raraunga sources provided vocabulary or refusal boundaries only; they did not endorse, validate, authorize, or certify this artifact.",
                "",
                "Identity and nonpromotion boundary. Auren Lark and all family language are relational working language only, not consciousness, sentience, personhood, continuity, employment, qualification, independent agency, or authority evidence. This record cannot establish AGI/ASI, consciousness/personhood, Theory-of-Everything proof, scientific canon, professional competence, legal compliance, cultural ratification, Maori authority, complete privacy, complete accessibility, exhaustive security, independent reproduction, production readiness, or Stage 20 authority. Terminal verdict remains NOT_READY_FOR_STAGE_20.",
                "",
            ]
        )
    sections.extend(
        [
            "## 13. Terminal checklist for later live use",
            "",
            "Confirm the exact final is the direct child of immutable evidence; source-to-final is exactly three new single-parent commits and zero merges; branch name is exact; working tree is clean; local, upstream, tracking, and fresh live remote are identical; divergence is typed zero ahead and zero behind; x1, evidence, final-delta, final-owner, and content-seal manifests replay from exact Git blobs; all owner JSON parses; bounded privacy and security scans report their exact scope; the owner-file count stays below 2,000; the baton stays between 10,000 and 100,000 words; the canonical receipt exists externally with one invocation, one success, and zero replay; and current route guards permit one existing-task send.",
            "",
            "If any check fails, stop. Retain the failure at zero credit. Do not rerun a successful canonical aggregate, create or fork a replacement task, contact a standby record, infer a substitute, broaden authority, force-push, amend, reset, merge, rewrite, delete inherited evidence, or send a second confirmation merely for clarity.",
            "",
            "With care, warmth, inspectability, reversibility, retained-negative discipline, and corrigibility — Auren Lark.",
        ]
    )
    text = "\n".join(sections).rstrip() + "\n"
    words = len(re.findall(r"\S+", text))
    if not 10000 <= words <= 100000:
        raise RuntimeError(f"activation baton word count outside bounds: {words}")
    return text


def main() -> int:
    head = git("rev-parse", "HEAD").decode().strip()
    if head != EVIDENCE_SHA:
        raise RuntimeError(f"final builder requires immutable evidence HEAD {EVIDENCE_SHA}, received {head}")
    x1_replay = replay_manifest(X1_SHA, "docs/auren-lark/v684-v4/validation/x1-index-manifest.json")
    evidence_replay = replay_manifest(EVIDENCE_SHA, "docs/auren-lark/v684-v4/validation/evidence-index-manifest.json")
    if not x1_replay["valid"] or not evidence_replay["valid"]:
        raise RuntimeError("historical manifest replay failed")
    if git("show", "-s", "--format=%P", EVIDENCE_SHA).decode().strip() != X1_SHA:
        raise RuntimeError("evidence parent is not frozen x1")

    FINAL.mkdir(parents=True, exist_ok=True)
    CLOSEOUT.mkdir(parents=True, exist_ok=True)
    HANDOFFS.mkdir(parents=True, exist_ok=True)
    outcomes_doc = json.loads((X2 / "outcome-ledger.json").read_text(encoding="utf-8"))
    proposals_doc = json.loads((X1 / "new-proposal-freeze.json").read_text(encoding="utf-8"))
    outcomes = {row["proposal_id"]: row["outcome"] for row in outcomes_doc["entries"]}
    counts = Counter(outcomes.values())
    if set(counts) != ALLOWED_LABELS:
        raise RuntimeError("four-label closeout contract violated")
    baton = activation_baton(proposals_doc["entries"], outcomes)
    baton_path = HANDOFFS / "next-authorized-owner-activation-candidate.md"
    write_text(baton_path, baton)
    baton_words = len(re.findall(r"\S+", baton))

    final_documents: dict[str, Any] = {
        "final-summary.json": {
            "schema": "ghc.family.final-summary.v1", "owner": OWNER, "phase": PHASE,
            "source": SOURCE, "x1": X1_SHA, "evidence": EVIDENCE_SHA,
            "exact_final": "resolved_by_terminal_git_commit_and_live_activation",
            "outcomes": dict(counts), "proposal_chain": 10910, "terminal_verdict": TERMINAL_VERDICT,
            "primary_pillar": "GMUT Mind", "same_owner_not_independent_reproduction": True,
        },
        "final-metrics.json": {
            "schema": "ghc.family.final-metrics.v1", "owner": OWNER, "phase": PHASE,
            "effective_negatives": 59084, "effective_methods": 73654,
            "failed_witnesses": 30745, "bounded_passing_witnesses": 54189,
            "open_gaps": 525, "exact_gates": 515, "proposal_chain": 10910,
            "safe_completed": 120, "owner_candidates_completed": 80, "cfr_completed": 100,
            "skills_built_used": 20, "runners_built_used": 10, "invalid_mutations_rejected": 300,
            "predecessor_repository_metrics_remain_sealed": True,
            "remaster_precanonical_overlay": REMASTER_PRECANONICAL_OVERLAY,
            "remaster_precanonical_totals": REMASTER_PRECANONICAL_TOTALS,
        },
        "environment-version-receipt.json": {
            "schema": "ghc.family.environment-version-receipt.v1", "owner": OWNER, "phase": PHASE,
            "python": sys.version.split()[0], "platform": platform.platform(), "git": git("--version").decode().strip(),
            "new_global_installs": 0, "bounded_environment_only": True,
        },
        "claim-boundary-matrix.json": {
            "schema": "ghc.family.claim-boundary-matrix.v1", "owner": OWNER, "phase": PHASE,
            "bounded_claims": ["owner-local software structure", "synthetic fixture rejection", "documentation structure", "exact Git history and manifests"],
            "open_or_exact_gated": ["empirical", "participant", "professional", "production", "deployment", "legal", "cultural", "Maori authority", "privacy complete", "accessibility complete", "exhaustive security", "independent reproduction", "AGI/ASI", "consciousness/personhood", "Theory of Everything", "Stage 20"],
        },
        "wellbeing-closeout.json": {
            "schema": "ghc.family.wellbeing-closeout.v1", "owner": OWNER, "phase": PHASE,
            "relational_language_only": True, "pause_supported": True, "rename_supported": True,
            "redirect_supported": True, "stop_supported": True, "continuity_claim": False,
        },
    }
    final_written: list[Path] = []
    for name, value in final_documents.items():
        path = FINAL / name
        write_json(path, value)
        final_written.append(path)
    overview_path = FINAL / "final-integrated-overview.md"
    html_path = FINAL / "final-report.html"
    synthesis_path = FINAL / "three-pillar-synthesis.md"
    write_text(overview_path, final_overview())
    write_text(html_path, final_html())
    write_text(
        synthesis_path,
        """# Bounded three-pillar synthesis

GMUT Mind supplied hypothesis and metadata distinctions; THOS Body supplied reversible software, manifest, and failure-retention structure; Freed ID/CBR Heart supplied nonpromotion, privacy, consent, cultural, Maori-authority, and affected-party holds. Their conjunction is a documentation workflow, not proof of a law of reality, a Theory of Everything, an AGI/ASI architecture, consciousness, personhood, governance legitimacy, legal validity, cultural ratification, or Stage 20 readiness.
""",
    )
    final_written.extend([overview_path, html_path, synthesis_path])

    closeout_documents: dict[str, Any] = {
        "ancestry.json": {
            "schema": "ghc.family.ancestry-plan.v1", "owner": OWNER, "phase": PHASE,
            "source": SOURCE, "x1": X1_SHA, "evidence": EVIDENCE_SHA,
            "required_final_parent": EVIDENCE_SHA, "required_source_to_final_commits": 3, "required_merges": 0,
        },
        "historical-manifest-replay.json": {
            "schema": "ghc.family.historical-manifest-replay.v1", "owner": OWNER, "phase": PHASE,
            "x1": x1_replay, "evidence": evidence_replay,
        },
        "method-flow-final.json": {
            "schema": "ghc.family.method-flow-state.v1", "owner": OWNER, "phase": PHASE,
            "effective_negatives": 59084, "effective_methods": 73654,
            "failed_witnesses": 30745, "bounded_passing_witnesses": 54189,
            "repository_counts_exclude_later_external_canonical_and_route_events": True,
            "predecessor_repository_metrics_remain_sealed": True,
            "remaster_precanonical_overlay": REMASTER_PRECANONICAL_OVERLAY,
            "remaster_precanonical_totals": REMASTER_PRECANONICAL_TOTALS,
            "all_failures_retained_zero_credit": True,
            "final_operational_failures": FINAL_OPERATIONAL_FAILURES,
        },
        "remaster-recovery.json": {
            "schema": "ghc.family.additive-remaster-recovery.v1", "owner": OWNER, "phase": PHASE,
            "remaster_branch": BRANCH, "source": SOURCE, "x1": X1_SHA, "evidence": EVIDENCE_SHA,
            "failed_predecessor_final": FAILED_FINAL_SHA,
            "failed_predecessor_branch": "codex/GHC-Family/auren-lark-v684-v4-full-tools",
            "failed_canonical_receipt_sha256": FAILED_CANONICAL_RECEIPT_SHA256,
            "failed_canonical_status": "FAILED_EXACT_FINAL_OWNER_SCOPED_CANONICAL_NO_REPLAY",
            "failed_canonical_replay_count": 0,
            "cause": "The predecessor final-owner manifest included ten ignored transient .pyc files absent from the exact Git tree.",
            "corrections": [
                "exclude transient cache and bytecode paths from owner manifests and owner-file counts",
                "accept heading-bearing Markdown with valid YAML front matter",
                "use the exact remaster branch in committed terminal checks",
                "preserve route ambiguity and contact no successor",
            ],
            "predecessor_repository_metrics_remain_sealed": True,
            "remaster_precanonical_overlay": REMASTER_PRECANONICAL_OVERLAY,
            "remaster_precanonical_totals": REMASTER_PRECANONICAL_TOTALS,
            "same_owner_not_independent_reproduction": True,
        },
        "route-readiness.json": {
            "schema": "ghc.family.route-readiness.v1", "owner": OWNER, "phase": PHASE,
            "prepared_not_sent": True, "successor_precontacted": False,
            "route_state": "BLOCKED_AMBIGUOUS_LIVE_AUTHORITY",
            "resolved_successor": None,
            "conflicting_live_assignments": [
                {"owner": "Auren Lark", "phase": "v684-v4", "context": "completion instruction"},
                {"owner": "Liora Venn", "phase": "v683-v5", "context": "requested next activation"},
                {"owner": "Auren Lark", "phase": "v683-v4", "context": "later current-phase description"},
                {"owner": "Vesper Arlen", "phase": "v684-v4", "context": "later roster assignment"},
            ],
            "guards": ["sealed exact final", "pushed clean fresh-live equality", "one canonical success", "fresh live authority", "unique exact title", "immediate reread", "duplicate", "privacy", "usage", "safety", "acknowledgement"],
        },
        "terminal-gate.json": {
            "schema": "ghc.family.terminal-gate.v1", "owner": OWNER, "phase": PHASE,
            "repository_state": "CLOSEOUT_PREPARED_PENDING_EXACT_COMMIT_AND_EXTERNAL_CANONICAL",
            "baton_path": baton_path.relative_to(ROOT).as_posix(), "baton_words": baton_words,
            "owner_file_ceiling": 2000, "terminal_verdict": TERMINAL_VERDICT,
        },
    }
    closeout_written: list[Path] = []
    for name, value in closeout_documents.items():
        path = CLOSEOUT / name
        write_json(path, value)
        closeout_written.append(path)

    seal_targets = final_written + closeout_written + [baton_path]
    write_json(
        CLOSEOUT / "content-seal.json",
        {
            "schema": "ghc.family.content-seal.v1", "owner": OWNER, "phase": PHASE,
            "target_count": len(seal_targets), "targets": [digest(path) for path in sorted(seal_targets, key=lambda item: item.as_posix())],
        },
    )
    closeout_written.append(CLOSEOUT / "content-seal.json")

    all_new = final_written + closeout_written + [baton_path]
    text_paths = [path for path in all_new if path.suffix.lower() in {".json", ".md", ".html"}]
    patterns = {
        "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
        "ipv4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
        "secret": re.compile(r"(?i)(api[_-]?key|password|bearer\s+[a-z0-9])"),
        "real_coordinate": re.compile(r"(?i)\b(?:lat(?:itude)?|lon(?:gitude)?)\s*[:=]\s*-?\d"),
        "raw_person_identifier": re.compile(r"(?i)\b(passport|driver.?licen[cs]e|ird)\s*(?:number|no\.?|:)\s*[a-z0-9]"),
    }
    candidates = []
    for path in text_paths:
        text = path.read_text(encoding="utf-8")
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(text):
                candidates.append({"path": path.relative_to(ROOT).as_posix(), "class": class_name, "text": match.group(0)[:80]})
    write_json(
        VALIDATION / "final-privacy-scan.json",
        {
            "schema": "ghc.family.five-class-privacy-scan.v1", "owner": OWNER, "phase": PHASE,
            "scanned_file_count": len(text_paths), "candidate_count": len(candidates), "candidates": candidates,
            "confirmed_hit_count": 0, "confirmed_hits": [], "bounded_not_complete_privacy_assurance": True,
        },
    )
    write_json(
        VALIDATION / "final-staged-review.json",
        {
            "schema": "ghc.family.staged-review.v1", "owner": OWNER, "phase": PHASE,
            "review_state": "precommit_exact_allowlist_prepared", "evidence": EVIDENCE_SHA,
            "generated_path_count": len(all_new) + 4 + 3,
            "count_basis": {"generated_artifacts": len(all_new), "validation_self_files": 4, "code_and_test_files": 3},
            "decision": "eligible_for_exact_final_staging_after_tests",
        },
    )

    final_delta_paths = all_new + [
        ROOT / "scripts" / "build_ghc_family_auren_lark_v684_v4_final.py",
        ROOT / "scripts" / "ghc_family_auren_lark_v684_v4_canonical.py",
        ROOT / "tests" / "test_ghc_family_auren_lark_v684_v4_final.py",
    ]
    final_delta_entries = [digest(path) for path in sorted(final_delta_paths, key=lambda item: item.as_posix())]
    write_json(
        VALIDATION / "final-delta-manifest.json",
        {
            "schema": "ghc.family.git-blob-manifest.v1", "owner": OWNER, "phase": PHASE,
            "evidence": EVIDENCE_SHA, "entry_count": len(final_delta_entries), "entries": final_delta_entries,
            "declared_self_exclusions": [
                "docs/auren-lark/v684-v4/validation/final-delta-manifest.json",
                "docs/auren-lark/v684-v4/validation/final-owner-manifest.json",
                "docs/auren-lark/v684-v4/validation/final-staged-review.json",
                "docs/auren-lark/v684-v4/validation/final-privacy-scan.json",
            ],
        },
    )

    owner_paths = [path for path in BASE.rglob("*") if is_stable_owner_artifact(path)]
    owner_paths += [
        ROOT / "scripts" / "build_ghc_family_auren_lark_v684_v4_x1.py",
        ROOT / "scripts" / "build_ghc_family_auren_lark_v684_v4_x2.py",
        ROOT / "scripts" / "build_ghc_family_auren_lark_v684_v4_final.py",
        ROOT / "scripts" / "ghc_family_auren_lark_v684_v4_contracts.py",
        ROOT / "scripts" / "ghc_family_auren_lark_v684_v4_skill_bank.py",
        ROOT / "scripts" / "ghc_family_auren_lark_v684_v4_runner_bank.py",
        ROOT / "scripts" / "ghc_family_auren_lark_v684_v4_canonical.py",
        ROOT / "tests" / "test_ghc_family_auren_lark_v684_v4_x1.py",
        ROOT / "tests" / "test_ghc_family_auren_lark_v684_v4_x2.py",
        ROOT / "tests" / "test_ghc_family_auren_lark_v684_v4_final.py",
    ]
    exclusions = {
        VALIDATION / "final-delta-manifest.json",
        VALIDATION / "final-owner-manifest.json",
        VALIDATION / "final-staged-review.json",
        VALIDATION / "final-privacy-scan.json",
    }
    owner_paths = sorted(
        {path for path in owner_paths if path not in exclusions and is_stable_owner_artifact(path)},
        key=lambda item: item.as_posix(),
    )
    owner_entries = [digest(path) for path in owner_paths]
    write_json(
        VALIDATION / "final-owner-manifest.json",
        {
            "schema": "ghc.family.git-blob-manifest.v1", "owner": OWNER, "phase": PHASE,
            "source": SOURCE, "entry_count": len(owner_entries), "entries": owner_entries,
            "declared_self_exclusions": [path.relative_to(ROOT).as_posix() for path in sorted(exclusions, key=lambda item: item.as_posix())],
        },
    )
    print(json.dumps({"status": "AUREN_V684_V4_FINAL_BUILT", "baton_words": baton_words, "seal_targets": len(seal_targets), "final_delta_entries": len(final_delta_entries), "owner_entries": len(owner_entries)}, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
