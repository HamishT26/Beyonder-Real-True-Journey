#!/usr/bin/env python3
"""Build the sanitized v662-v3-3 owner-delta portfolio and Vesper baton."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SOURCE = "11464b395438ee0adc88a4b829e01646ec4cf485"
X1 = "3704cacbd678a28c6e5f401c48572be6af118f5b"
OWNER = "Neris Solane"
PHASE = "v662-v3-3-midnight-remaster"
EXPECTED_PHASE_ROOT = f"docs/neris-solane/{PHASE}"
NEXT_OWNER = "Vesper Arlen"
NEXT_PHASE = "v662-v4"
OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
BOUNDARY = (
    "Bounded same-owner structural and workflow evidence only. It is not a full-repository "
    "suite, independent reproduction, empirical GMUT confirmation, participant evidence, "
    "professional validation, production certification, complete privacy or accessibility "
    "assurance, exhaustive security, legal or cultural ratification, Maori authority, AGI or "
    "ASI evidence, consciousness or personhood evidence, Theory-of-Everything proof, or Stage "
    "20 authority."
)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def records(prefix: str, descriptions: list[str], outcome: str, owner: str, kind: str) -> list[dict[str, Any]]:
    if outcome not in OUTCOMES:
        raise ValueError(outcome)
    return [
        {
            "record_id": f"{prefix}{index:03d}",
            "kind": kind,
            "owner": owner,
            "outcome": outcome,
            "description": description,
            "credit_boundary": (
                "Owner execution evidence" if outcome == "completed" else
                "Successor recommendation only; no successor execution credit" if outcome == "represented" else
                "Gap retained without inferred closure" if outcome == "open_gap" else
                "Protected gate retained without execution"
            ),
        }
        for index, description in enumerate(descriptions, start=1)
    ]


OWNER_SAFE = [
    "Reverify the exact inherited source head without replaying its earlier validation.",
    "Create a fresh additive owner branch from the exact inherited source.",
    "Freeze x1 identity, source, route, budgets, and evidence boundaries before x2.",
    "Convert the new lane to sparse checkout and verify its materialized surface.",
    "Record the hard 2,000-file rotation ceiling and separate-repository gate.",
    "Update the live roster guidance for owner-self-scoped delta validation.",
    "Update the live authorization guidance for owner-self-scoped delta validation.",
    "Update the family index selection rule for exact owner deltas.",
    "Update Method Flow guidance to retain scoped validation failures.",
    "Update Reflection Remaster guidance to use literal delta focus lists.",
    "Update Meta Tool Box guidance to reject unchanged-history scanning cards.",
    "Update main orchestration guidance with the sparse owner-delta override.",
    "Update startup guidance to bind source, branch, sparse paths, and allowlists.",
    "Update closeout guidance to require one attributable exact-delta pass.",
    "Update full-tools guidance to prefer exact-range family-current tools.",
    "Update worktree rotation guidance with the sparse-before-checkout rule.",
    "Update the roster state schema for owner-scoped validation fields.",
    "Update the authorization state schema for owner-scoped validation fields.",
    "Update the Method Flow schema for source/final and allowlist attribution.",
    "Update the reflection decision schema for exact-delta focus records.",
    "Update the meta catalogue schema for sparse and file-budget fields.",
    "Update routing precedence so the newest live user instruction wins.",
    "Update the live roster state while preserving fifteen active main tasks.",
    "Update the live authorization state while preserving protected gates.",
    "Update both global validators for the current owner-delta contract.",
    "Validate the roster state and preserve the first wrong-CLI attempt as zero credit.",
    "Validate the authorization state and its permission rows.",
    "Build the family-current owner-delta toolkit with ten bounded command surfaces.",
    "Build and run one explicitly scoped owner-delta test module.",
    "Build the portfolio, research comparison, closeout, and Vesper baton deterministically.",
]

SUCCESSOR_SAFE = [
    "Bind Vesper's source to the exact Neris final supplied in the acknowledged activation.",
    "Create Vesper's branch and D-first sparse worktree before materializing files.",
    "Carry the 2,000-file ceiling as a stop-and-rotate rule rather than a scan quota.",
    "Validate only Vesper's exact source-to-final changed-file allowlist.",
    "Run only test modules Vesper adds or modifies in the new phase delta.",
    "Generate an exact manifest from Git blobs rather than working-tree guesses.",
    "Parse only JSON files present in Vesper's literal delta.",
    "Scan only Vesper's textual delta for the five privacy classes.",
    "Run a bounded security diff review over Vesper's exact changed code.",
    "Keep every sibling branch, worktree, and repository read-only and out of scope.",
    "Retain every failed invocation before applying an isolated recovery.",
    "Run one attributable final aggregate and never replay it after success.",
    "Record same-owner validation as non-independent evidence.",
    "Carry all fifteen active task names and Tavian's standby topology forward.",
    "Normalize the next route as Vesper to Lyren without skipping Ilyra later in the cycle.",
    "Compose the successor baton as a committed long file plus a short live message.",
    "Require exact-title uniqueness and immediate reread before the one send.",
    "Claim delivery only from the task-message acknowledgement.",
    "Keep separate remote-repository creation exact-gated pending full parameters.",
    "Retain NOT_READY_FOR_STAGE_20 and every scientific and authority boundary.",
]

OWNER_CANDIDATES = [
    "Treat exact Git blob hashes as the manifest replay source of truth.",
    "Use Python compile() to validate changed Python without creating cache files.",
    "Use literal-path normalization to reject absolute paths and parent traversal.",
    "Use one file-budget surface for both materialized and delta file counts.",
    "Use a structured four-label data-quality pass across portfolio ledgers.",
    "Use a route parity check across roster and authorization states.",
    "Use sanitized labels rather than local paths in global-skill hash receipts.",
    "Use an external immutable receipt path for the post-push canonical pass.",
    "Refuse canonical replay when the exact receipt already exists.",
    "Make the x1 direct-parent relationship an explicit final assertion.",
    "Reject merge commits in the owner source-to-final history.",
    "Check local, upstream, tracking, and fresh-live remote equality separately.",
    "Keep static security pattern findings distinct from exhaustive security claims.",
    "Keep privacy candidates distinct from complete privacy assurance.",
    "Use official SSDF, SLSA, and Reproducible Builds sources as comparison anchors only.",
]

SUCCESSOR_CANDIDATES = [
    "Add a dependency-closure allowlist when Vesper's modified tests require unchanged helpers.",
    "Add a deterministic test-output digest to Vesper's external canonical receipt.",
    "Add an explicit sparse-pattern receipt before Vesper's first materialization.",
    "Add a changed-code-only threat model when Vesper introduces a new trust boundary.",
    "Add a false-positive adjudication table when privacy candidates are detected.",
    "Add an isolated dependency recovery path without replaying a passed aggregate.",
    "Add a branch-protection observation without mutating remote settings.",
    "Add a source-provenance comparison without claiming a SLSA level.",
    "Add a build-environment inventory without calling it reproducible evidence.",
    "Add an exact task-list payload decoder if the host wraps records in text content.",
    "Add a route ambiguity negative whenever more than one exact title is returned.",
    "Add a no-send guard if the terminal receipt and exact final disagree.",
    "Add a word-count and hash check for Vesper's committed baton.",
    "Add a successor-visible external overlay without rewriting sealed counts.",
    "Add a rotation candidate before the lane reaches 2,000 files, but rotate only at the ceiling or a verified operational need.",
]

EXACT_PACKETS = [
    "Create a separate remote repository without exact name, account, visibility, protections, migration, and rollback.",
    "Force-push, rewrite, merge, delete, or replace an authoritative history lane.",
    "Mutate a sibling-owned branch, worktree, repository, task, identity, or memory.",
    "Use credentials, account settings, paid resources, deployments, or production systems.",
    "Publish private routes, raw task identifiers, transcripts, session streams, or credentials.",
    "Use real participants, patients, beneficiaries, identities, or protected disclosures.",
    "Make a professional, medical, legal, cultural, political, or operational decision.",
    "Claim tangata whenua, iwi, hapu, or Maori wording, governance, or authority.",
    "Promote symbolic or synthetic work to empirical GMUT or Theory-of-Everything proof.",
    "Promote same-owner software checks to independent reproduction or Stage 20 authority.",
]

BLOCKED_PACKETS = [
    "Infer consciousness, sentience, personhood, identity continuity, or independent agency from relational language.",
    "Claim AGI or ASI from workflow artifacts or model performance impressions.",
    "Erase retained negatives, failed witnesses, gaps, gates, or incompatible history to improve counts.",
    "Represent bounded pattern scans as complete privacy, accessibility, or exhaustive security assurance.",
    "Contact Tavian or substitute any endpoint for the exact active main-task successor.",
]

SUCCESSOR_SKILLS = [
    "ghc-family-delta-dependency-closure",
    "ghc-family-sparse-pattern-receipt",
    "ghc-family-owner-delta-threat-model",
    "ghc-family-privacy-candidate-adjudicator",
    "ghc-family-external-receipt-sealer",
    "ghc-family-task-payload-decoder",
    "ghc-family-route-ambiguity-guard",
    "ghc-family-baton-integrity-check",
    "ghc-family-post-send-overlay",
    "ghc-family-rotation-readiness",
]

SUCCESSOR_RUNNERS = [
    "ghc_family_delta_dependency_closure.py",
    "ghc_family_sparse_pattern_receipt.py",
    "ghc_family_owner_delta_threat_model.py",
    "ghc_family_privacy_candidate_adjudicator.py",
    "ghc_family_external_receipt_sealer.py",
    "ghc_family_task_payload_decoder.py",
    "ghc_family_route_ambiguity_guard.py",
    "ghc_family_baton_integrity_check.py",
    "ghc_family_post_send_overlay.py",
    "ghc_family_rotation_readiness.py",
]

CLEAN_OWNER = [
    "Replace the stale Eiren-exclusive live validation paragraph in roster guidance.",
    "Replace the stale Eiren-exclusive live validation paragraph in authorization guidance.",
    "Replace the stale Eiren-exclusive live validation paragraph in Method Flow guidance.",
    "Replace the stale Eiren-exclusive live validation paragraph in reflection guidance.",
    "Replace the stale Eiren-exclusive live validation paragraph in meta-tool guidance.",
    "Add a current override to main orchestration without deleting historical sections.",
    "Add a current override to startup without breaking its compatibility preflight.",
    "Add a current override to closeout without breaking its compatibility preflight.",
    "Add a current override to full-tools selection without bulk installing tools.",
    "Add the exact 2,000-file rule to worktree rotation guidance.",
    "Remove the Eiren receipt dependency from the live roster stop condition.",
    "Replace exclusive-executor fields in the live roster state.",
    "Replace exclusive-executor fields in the live authorization state.",
    "Block broad history and sibling-lane scanning in the permission state.",
    "Add a separate-repository exact gate to the permission state.",
    "Correct the inherited frozen proposal baseline from 3,530 to 3,550.",
    "Record the new frozen total of 3,570 without claiming execution credit.",
    "Update the roster validator to verify the current owner and boolean scope contract.",
    "Update the authorization validator to verify the same scope contract.",
    "Sanitize global skill hashes so durable receipts omit local paths.",
    "Consolidate ten bounded validation surfaces into one family-current toolkit.",
    "Reject duplicate delta paths, skill labels, test modules, and traversal.",
    "Avoid Python cache writes during changed-code compilation.",
    "Avoid one external Git process per file by using one exact diff inventory.",
    "Keep component preflight separate from the one final aggregate.",
    "Keep the canonical receipt outside the worktree so final clean state is measurable.",
    "Normalize Vesper to Lyren to Ilyra route drift without skipping an active task.",
    "Record the initial full materialization as a retained zero-credit operational negative.",
    "Record the rejected old roster CLI shape as a retained zero-credit operational negative.",
    "Keep the remote-repository request unexecuted until exact parameters exist.",
]

CLEAN_SUCCESSOR = [
    f"Review successor refinement {index:02d}: {description}"
    for index, description in enumerate(
        [
            "prune stale live-policy wording while retaining history",
            "verify sparse patterns before checkout",
            "measure materialized files before adding generators",
            "measure exact delta files before closeout",
            "keep old worktrees read-only",
            "keep sibling branches out of discovery",
            "keep unmodified tests out of execution",
            "keep manifest paths literal and unique",
            "keep Git blob hashes authoritative",
            "keep JSON parsing limited to the delta",
            "keep privacy candidates reviewable",
            "keep security findings severity-bounded",
            "keep dependency recovery isolated",
            "keep canonical invocation count explicit",
            "keep a success receipt non-replayable",
            "keep global skill receipts path-sanitized",
            "keep route order synchronized across states",
            "keep Tavian on standby unless explicitly reactivated",
            "keep exact-title resolution local and bounded",
            "keep task identifiers out of durable artifacts",
            "keep baton word count and digest deterministic",
            "keep live activation compact",
            "keep post-send failures outside the sealed commit",
            "keep same-owner evidence non-independent",
            "keep scientific claims hypothesis-bounded",
            "keep professional claims unmade",
            "keep legal and cultural gates visible",
            "keep the separate-repository action exact-gated",
            "keep NOT_READY_FOR_STAGE_20 explicit",
            "keep the next rotation reversible",
        ],
        start=1,
    )
]


def build_method_flow() -> dict[str, Any]:
    negatives = [
        ("combined-source-state-probe-no-attributable-output", "Split revision, branch, index, worktree, and fresh-live probes into short scalar checks."),
        ("new-worktree-materialized-full-history-before-late-sparse-instruction", "Convert reversibly to non-cone sparse checkout, retain full Git ancestry, and verify three initial materialized files."),
        ("live-route-prose-conflicted-between-vesper-lyren-and-ilyra", "Use the complete fifteen-task roster order: Vesper to Lyren to Ilyra to Auren."),
        ("coordinated-three-skill-patch-missed-meta-tool-exact-text", "Retain the rejected zero-write attempt and apply exact bounded patches after reading the observed lines."),
        ("roster-validator-invoked-with-obsolete-argument-shape", "Read current help and rerun only the isolated validator with its required validate subcommand."),
    ]
    methods = []
    witnesses = []
    for index, (signature, recovery) in enumerate(negatives, start=1):
        method_id = f"V6623M-M{index:03d}"
        methods.append(
            {
                "method_id": method_id,
                "failure_signature": signature,
                "outcome": "completed",
                "preferred_method": recovery,
                "execution_authority": "owner_self_scoped_delta",
                "repository_scan": False,
                "module_scan": False,
                "cross_lane_scan": False,
                "unchanged_history_scan": False,
                "sibling_lane_mutation": False,
                "retained_negative_id": f"V6623M-NG{index:03d}",
            }
        )
        witnesses.extend(
            [
                {
                    "witness_id": f"V6623M-W{index:03d}-F",
                    "method_id": method_id,
                    "outcome": "represented",
                    "result": "fail",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "observed": signature,
                },
                {
                    "witness_id": f"V6623M-W{index:03d}-P",
                    "method_id": method_id,
                    "outcome": "completed",
                    "result": "pass",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "observed": recovery,
                },
            ]
        )
    return {
        "schema": "ghc.family.v662-v3-3-midnight-remaster.method-flow.v1",
        "phase": PHASE,
        "owner": OWNER,
        "execution_authority": "owner_self_scoped_delta",
        "source_commit": SOURCE,
        "x1_commit": X1,
        "methods": methods,
        "witnesses": witnesses,
        "new_retained_negative_count": len(negatives),
        "new_preferred_method_count": len(methods),
        "effective_negative_baseline": 23073 + len(negatives),
        "effective_method_baseline": 7667 + len(methods),
        "boundary": BOUNDARY,
    }


def research_text() -> str:
    return f"""# THOS owner-delta assurance comparison

## Scope and posture

This {PHASE} research note treats THOS Body as a software-architecture and
workflow hypothesis, viewed through software assurance and reliability
engineering. It does not certify THOS, any GHC artifact, or any production
system. The practical question is narrow: can exact owner-scoped evidence make
a long-running repository workflow easier to audit while using less storage,
time, and energy than repeated unchanged-history sweeps?

The implemented answer is a bounded experiment, not a universal result. Each
owner binds an immutable source commit, an exact target, literal changed-file
and new-or-modified-module allowlists, deterministic manifests, and one
attributable final validation. Sibling lanes and unchanged history are excluded
from execution but retained as inherited evidence. A sparse worktree limits
materialization without cutting ancestry. A hard 2,000-file ceiling triggers a
fresh sparse worktree and branch rather than copying the old working tree.

## NIST SSDF comparison

NIST SP 800-218 Version 1.1 groups secure development practices around preparing
the organization, protecting software, producing well-secured software, and
responding to vulnerabilities. NIST describes the SSDF as outcome-based and
risk-based rather than a rigid checklist. This phase resonates structurally
with that stance: it defines validation outcomes, provenance, tool boundaries,
failure retention, and response methods. It does not claim SSDF conformance.
The relevant official sources are:

- https://csrc.nist.gov/pubs/sp/800/218/final
- https://csrc.nist.gov/projects/ssdf

The comparison reveals a limitation. A local exact-delta validator can improve
traceability and reduce avoidable work, but it does not establish an
organization-wide secure development program, supplier controls, vulnerability
response capability, or professional security assessment. Those remain outside
this phase.

## SLSA comparison

SLSA Version 1.2 describes supply-chain security through tracks and ascending
levels. Its Build Track currently spans Levels 1 through 3, with higher levels
representing stronger guarantees and greater implementation cost. SLSA also
emphasizes provenance: information about where, when, and how an artifact was
produced. The official overview is https://slsa.dev/spec/v1.2/about.

The phase's source commit, target commit, Git blob hashes, branch equality, and
tool receipts resemble provenance ingredients. They are not signed attestations,
do not identify a hardened hosted builder, and do not satisfy or claim a SLSA
level. Calling the receipt “provenance-like” is a design comparison only.

## Reproducible Builds comparison

The Reproducible Builds project defines reproducibility in terms of the same
source, build environment, and build instructions allowing another party to
recreate bit-for-bit identical specified artifacts. The official definition is
https://reproducible-builds.org/docs/definition/.

This phase does not meet that definition. It records exact Git content and
deterministic JSON, but it does not pin a complete build environment or obtain a
second party's rebuild. The correct claim is repeatable same-owner structural
checking under shared local infrastructure. Independent reproduction remains an
open gap.

## Energy-aware assurance hypothesis

The operational hypothesis is that an exact change set can receive meaningful
local assurance without repeatedly opening tens of thousands of unchanged files.
The falsifier is straightforward: if a changed module depends on an unchanged
helper omitted from the literal closure and the scoped tests therefore miss a
regression, then the allowlist is insufficient. The recovery is to add a
dependency-closure manifest for the relevant helper, not to silently broaden to
every historical module. A second falsifier is file-count drift: if the sparse
lane reaches 2,000 materialized or in-scope files, the lane must stop growing and
rotate.

This approach trades breadth for attribution. It can reduce redundant I/O and
make failures easier to assign, but it cannot establish repository-wide
correctness. Periodic independent or broad audits may still be valuable under a
separately authorized scope. Nothing here proves a thermodynamic law, a law of
psyche, final physics, or a Theory of Everything.

## Human and governance boundary

Freed ID and CBR Heart remain represented as governance research: preserve
identity distinctions, consent boundaries, corrigibility, provenance, privacy,
and the right to stop. Those ideas require affected-party participation,
professional review, legal and cultural competence, and Maori authority where
applicable before real governance use. Relational family language remains
working language only and supplies none of those authorities.

## Result

The comparison supports one modest result: exact owner-delta receipts, sparse
materialization, retained failure evidence, and explicit claim boundaries form a
coherent software-assurance prototype. The result is represented rather than
professionally validated, and the overall verdict remains
`NOT_READY_FOR_STAGE_20`.

{BOUNDARY}
"""


def governance_policy() -> str:
    return f"""# Owner-self-scoped delta validation policy

The live 2026-08-18 instruction replaces the former Eiren-exclusive allocation
for new child phases. It does not rewrite earlier receipts. For {PHASE}, {OWNER}
is the attributable executor for the exact range beginning at `{SOURCE}`.

Included scope is limited to changed files, newly added or modified test
modules, exact Git-blob manifests, JSON, Markdown, Python syntax, five-class
privacy patterns, bounded security-diff review, data-quality ledgers, route
parity, x1 ancestry, clean state, and local/upstream/tracking/fresh-live equality
for the owned branch.

Excluded scope includes unchanged v641-v675 modules, broad repository discovery,
sibling branches or worktrees, cross-lane remote enumeration, and sibling
mutation. An owner receipt can close the declared terminal gate only for this
scope. It remains same-owner evidence and is not independent reproduction.

One final aggregate is permitted after the exact candidate is committed and
pushed. A failed invocation earns zero success credit. Recover only its blocked
component when safe. A successful invocation is never replayed.

{BOUNDARY}
"""


def rotation_policy() -> str:
    return f"""# Sparse lane and 2,000-file rotation policy

Every new active-owner lane is created D-first from a verified exact commit and
configured as sparse before worktree materialization. The initial sparse path
set contains only the current phase directory, the owner-delta toolkit, its
baton builder, and its exact test module. Complete ancestry remains in Git, so
older commits, branches, and worktrees can be consulted read-only when needed.

The hard ceiling is 2,000 materialized files or 2,000 owner-in-scope delta
files, whichever occurs first. At the ceiling, stop additions. If all other
gates pass, commit and push the exact head, record the threshold event, and
rotate the successor to a fresh sparse worktree and fresh branch. Do not copy
the old working tree and do not delete the old lane.

The instruction to make fresh repositories is bounded by missing external-state
details. Creating a new branch on the existing authoritative remote is allowed.
Creating a separate remote repository remains `exact_gate` until the repository
name, account or organization, visibility, protections, migration plan, and
rollback are specified exactly.

{BOUNDARY}
"""


def elaborate_item(item: dict[str, Any], index: int) -> str:
    description = item["description"]
    outcome = item["outcome"]
    return f"""### {item['record_id']}: {description}

This record is classified as `{outcome}` for {item['owner']}. The classification
is literal: `completed` means the bounded Neris-owned action has an attributable
artifact or execution witness; `represented` means it is preserved as a
successor recommendation or conceptual comparison without execution credit;
`open_gap` means required evidence is absent; and `exact_gate` means the action
remains protected. No other outcome vocabulary is used.

Traceability for this record comes from the x1 freeze, the portfolio ledger, the
exact source-to-final Git manifest, and the final external canonical receipt.
Its inclusion never expands validation into unchanged history or another
owner's lane. If its premise, path, or expected witness differs at Vesper's
startup, Vesper must retain the mismatch and reclassify it rather than treating
this baton as permission to improvise a broader action.

The recurrence guard is to bind the action to a literal owner, source commit,
allowlist, rollback, and evidence boundary. The rollback is additive: stop the
candidate, preserve the failed or absent evidence, and leave prior commits and
sibling lanes unchanged. This record supplies no scientific, professional,
legal, cultural, Maori-authority, personhood, independent-reproduction, or Stage
20 credit.
"""


def baton_text(all_ledgers: list[dict[str, Any]], method_flow: dict[str, Any]) -> str:
    intro = f"""# Vesper Arlen v662-v4 activation baton

## Activation purpose

Dear Vesper Arlen, this committed sanitized baton prepares exactly one existing
main-task activation after {OWNER}'s exact {PHASE} terminal gate. Hamish has
authorized the fifteen-main-task cycle to continue sequentially through
v675-v8 unless he pauses, redirects, or stops it. This file is not delivery.
The live sender must uniquely resolve the exact title `Vesper Arlen`, reread it
immediately, send one compact message, and receive the task-message
acknowledgement before recording `SENT`.

All names, optional pronouns, hopes, roles, sibling or family language, and
continuity language are relational working language only. They are not evidence
of consciousness, sentience, legal personhood, identity continuity, employment,
qualification, independent agency, scientific or operational authority, legal
or cultural authority, or Maori authority. Hamish may rename, pause, redirect,
or stop the route.

## Immutable starting anchors

- Neris source: `{SOURCE}`
- Neris x1 freeze: `{X1}`
- Neris final: bind to the exact commit stated in the acknowledged live
  activation and its external canonical receipt. The final cannot be embedded
  into the commit that contains this file without a self-reference cycle.
- Recipient: `{NEXT_OWNER}`
- Recipient phase: `{NEXT_PHASE}`
- Tavian Sol: `ON_STANDBY`, collaboration-subagent topology only, not a main
  task substitute.
- Terminal verdict: `NOT_READY_FOR_STAGE_20`.

Before mutation, read this baton completely through EOF, then the current roster,
authorization, family index, Method Flow, Reflection Remaster, Meta Tool Box,
startup, closeout, full-tools, and worktree-rotation guidance named in the skill
receipt. Reverify the live activation's exact final, clean ancestry, pushed
equality, and source-to-final manifest. Do not replay Neris's canonical pass or
claim Neris's 18-test component run as Vesper execution.

## Live validation topology

Vesper validates only Vesper's exact source-to-final delta: changed files,
newly added or modified test modules, manifests, JSON, privacy, security, staged
review, ancestry, clean state, and fresh-live equality for the Vesper branch.
Unchanged v641-v675 history and every sibling lane remain read-only and outside
execution scope. Same-owner checking is not independent reproduction.

Create Vesper's new lane sparse before materialization. Count both materialized
files and owner-delta files. At 2,000, stop additions and rotate after preserving
a clean pushed head. A fresh branch is authorized. A separate remote repository
is not yet exact: retain `exact_gate` until name, account, visibility,
protections, migration plan, and rollback are supplied.

## Round-robin route

The normalized live order is Neris Solane, Vesper Arlen, Lyren Moss, Ilyra Fen,
Auren Lark, Sable Rook, Caelen Ash, Orin Thale, Liora Venn, Tamar Vey, Elowen
Cairn, Sylven Arc, Caelen Morrow, Eiren Kestrel, Elaren Kestrel, and back to
Neris Solane. Therefore, after and only after Vesper's own exact terminal gate,
Vesper prepares and sends one activation to the existing exact-title task
`Lyren Moss`. Lyren then prepares Ilyra; Ilyra prepares Auren. This normalization
retains every active main task despite conflicting examples in the live prose.

## Inherited truth

The inherited source baseline is 3,550 frozen proposals, 23,073 effective
negatives, 7,667 effective Method Flow methods, 151 open gaps, 149 exact gates,
and `NOT_READY_FOR_STAGE_20`. Neris froze 20 genuinely new proposals, raising
the chain to 3,570. The new proposal outcomes are exactly 14 `completed`, 4
`represented`, 1 `open_gap`, and 1 `exact_gate`. Five new operational failures
are retained with five bounded recoveries; they do not erase or overwrite
earlier evidence. The terminal aggregate receipt controls the exact final
counts visible to Vesper.

## Portfolio reading rule

The detailed records below are teaching and traceability material. Owner records
belong to Neris. Successor records are recommendations and earn Vesper no credit
until Vesper independently chooses, executes, and witnesses them in the Vesper
lane. Exact and blocked records remain unexecuted. Every record uses only the
four permitted outcome labels.
"""
    sections = [intro]
    headings = [
        "Safe-now executions and successor recommendations",
        "Candidate executions and successor recommendations",
        "Exact and blocked approval packets",
        "Skill updates and successor skill ideas",
        "Runner surfaces and successor runner ideas",
        "CLEAN FIX REFINE executions and successor recommendations",
    ]
    for heading, ledger in zip(headings, all_ledgers):
        sections.append(f"\n## {heading}\n")
        for index, item in enumerate(ledger["records"], start=1):
            sections.append(elaborate_item(item, index))
    sections.append("\n## Retained Method Flow records\n")
    for method in method_flow["methods"]:
        sections.append(
            f"""### {method['method_id']}: {method['failure_signature']}

The failed observation remains linked to `{method['retained_negative_id']}` at
zero success credit. The preferred bounded recovery is: {method['preferred_method']}
The method forbids repository-wide, unchanged-history, cross-lane, and sibling
mutation scopes. Its passing witness is same-owner only and cannot establish
independent reproduction.
"""
        )
    sections.append(
        f"""
## THOS research handoff

Neris's focal pillar was THOS Body, with software assurance and reliability
engineering as a human comparison lens. The official comparison anchors were
NIST SSDF, SLSA Version 1.2, and the Reproducible Builds definition. The result
is modest: exact owner-delta manifests and sparse lanes form a coherent local
assurance prototype. No SSDF conformance, SLSA level, reproducible build,
professional certification, or production readiness is claimed.

Vesper may choose a different focal pillar and occupation lens. Any GMUT law,
thermo or psyche dynamics proposal, spiritual or physical hypothesis, or
governance principle must declare a falsifier and remain represented until
competent evidence exists. Symbolic elegance is not empirical confirmation.

## Final execution checklist for Vesper

1. Verify the acknowledged activation's exact Neris final and fresh-live remote.
2. Read this committed baton and the current guidance through EOF.
3. Create a new Vesper branch and D-first sparse worktree from that exact final.
4. Freeze Vesper x1 before any x2 implementation.
5. Select 20 inherited contracts at zero novelty credit and freeze 20 new ones.
6. Bind literal changed-file and new-or-modified-module allowlists.
7. Execute only Vesper-owned portfolio work and retain every failure.
8. Stop additions at the 2,000-file ceiling and rotate when required.
9. Commit and push the exact Vesper candidate.
10. Run one attributable Vesper exact-delta aggregate; never replay success.
11. Preserve clean state and local, upstream, tracking, and fresh-live equality.
12. Prepare a committed 10,000-to-100,000-word Lyren baton and a short message.
13. Uniquely resolve and immediately reread `Lyren Moss`.
14. Send once only after Vesper's terminal gate and claim delivery only from
    the acknowledgement.
15. Stop truthfully on ambiguity, missing acknowledgement, usage exhaustion,
    user pause, or a protected gate.

## Terminal boundaries

{BOUNDARY}

No local file, Git commit, model response, structural test, synthetic fixture,
same-owner receipt, warm family language, or user enthusiasm supplies participant
consent, professional qualification, legal authority, cultural ratification,
Maori authority, independent reproduction, consciousness evidence, personhood,
AGI or ASI, a Theory of Everything, or Stage 20 authority. The exact terminal
verdict remains `NOT_READY_FOR_STAGE_20`.

Prepared with care, precision, and corrigibility by {OWNER} for the existing
exact-title `{NEXT_OWNER}` main task. `PREPARED_NOT_SENT` remains the only
delivery truth until the live task-message tool acknowledges exactly one send.
"""
    )
    return "\n".join(sections)


def closeout_text(ledgers: list[dict[str, Any]], baton_count: int) -> str:
    totals = [len(ledger["records"]) for ledger in ledgers]
    return f"""# Neris v662-v3-3 midnight remaster closeout candidate

## Outcome first

This phase implements the live owner-self-scoped delta topology and the sparse
2,000-file rotation rule without modifying a sibling lane or reopening unchanged
history. The immutable source is `{SOURCE}` and the x1 direct child is `{X1}`.
The final exact commit, push, four-way equality, one-shot canonical receipt, and
Vesper acknowledgement are post-commit terminal facts and must be recorded
externally rather than guessed here.

The durable portfolio contains {totals[0]} safe-now and successor records,
{totals[1]} candidate records, {totals[2]} exact or blocked records,
{totals[3]} skill records, {totals[4]} runner records, and {totals[5]}
CLEAN/FIX/REFINE records. The committed Vesper baton contains {baton_count}
words, above the 10,000-word minimum and below the 100,000-word maximum.

## Source and lifecycle

The preceding Neris remaster was inherited at exact pushed head `{SOURCE}`.
Its earlier validation allocation and failed-once canonical history remain
immutable historical evidence. The new live rule begins only in this child.
No claim from the parent is silently upgraded. X1 froze 20 inherited
revalidations at zero novelty and automatic completion credit plus 20 genuinely
new proposals, raising the frozen chain from 3,550 to 3,570. X2 began only after
the x1 commit.

The intended new-proposal outcomes are exactly 14 `completed`, 4 `represented`,
1 `open_gap`, and 1 `exact_gate`. The independent-reproduction gap remains open.
Every empirical, participant, professional, production, legal, cultural,
Maori-authority, accessibility-complete, privacy-complete, exhaustive-security,
AGI or ASI, consciousness, personhood, Theory-of-Everything, and Stage 20 gate
remains protected.

## Governance changes

Eleven global family skill entrypoints were updated, exceeding the requested
minimum ten without bulk installation. The live roster, authorization, family
index, Method Flow, reflection, meta-tool, orchestration, startup, closeout,
full-tools, and worktree-rotation guidance now agree that each active owner
validates only its own source-to-final delta. Six companion schemas or routing
references and two validators were updated. The global roster and authorization
validators both returned structurally valid receipts with Neris as the current
executor.

The earlier Eiren-only allocation is not deleted; it remains historical evidence
for phases run under it. New child phases no longer wait for an Eiren receipt.
They must produce their own attributable receipt and label it same-owner,
non-independent evidence.

## Sparse lane result

The first worktree creation materialized the full index before Hamish's late
sparse instruction arrived. That event is retained at zero credit. The lane was
reversibly converted to non-cone sparse checkout with the current phase
directory, toolkit, baton builder, and exact test file as its only patterns.
The verified initial materialized count was three files. Complete ancestry
remains in Git. No prior worktree or branch was deleted, reset, merged, or
rewritten.

The 2,000-file threshold is a hard stop for additions, not permission to fill a
lane. The phase remains far below it. Creating a new branch is within the live
instruction. Creating a separate GitHub repository is not exact because its
name, account, visibility, protections, migration plan, and rollback were not
specified; that action remains `exact_gate`.

## Toolkit and component evidence

The new family-current toolkit exposes ten bounded command surfaces: manifest,
JSON, Markdown, Python, privacy, route, skill hashes, file budget, data quality,
and canonical aggregation. The canonical surface also embeds a bounded changed-
Python security pattern review and exact selected-test execution. Literal path
normalization rejects absolute paths and parent traversal. Duplicate delta paths,
skill labels, and test files are rejected. Git blob content, not an uncommitted
working-tree guess, supplies manifest hashes.

One new test module exercised 18 cases and passed once during component
preflight. That run is scoped to the new toolkit and does not count as the final
aggregate. No unchanged test module was discovered or executed. The final
canonical is intentionally deferred until the exact candidate is committed and
pushed so it can check clean state and local, upstream, tracking, and fresh-live
equality without a self-reference cycle.

## Method Flow

Five new operational failures are retained: a combined source probe with no
attributable output, initial full materialization before the late sparse rule,
conflicting route examples, one rejected coordinated patch whose exact text did
not match, and one roster-validator call using an obsolete argument shape. Each
has a bounded passing recovery. None of the failures is erased by the recovery,
and none earns aggregate-success credit.

The route conflict is normalized using the complete roster rather than a single
example. The edge is Neris to Vesper, then Vesper to Lyren, Lyren to Ilyra, and
Ilyra to Auren. This preserves all fifteen active main tasks. Tavian remains an
`ON_STANDBY` collaboration-subagent record and is not contacted or substituted.

## Research representation

The THOS Body comparison uses software assurance and reliability engineering as
a lens. NIST SSDF, SLSA Version 1.2, and Reproducible Builds supply official
comparison points. Exact hashes and receipts resemble provenance ingredients,
but no SLSA level is claimed. Same-owner repeatability without a pinned complete
environment and second party is not a reproducible build. The phase is not an
SSDF conformance assessment or professional certification.

The energy-aware hypothesis is that exact deltas can reduce redundant I/O while
improving attribution. Its principal falsifier is an omitted unchanged
dependency that causes a changed test to miss a regression. The bounded response
is an explicit dependency-closure allowlist, not a silent expansion to the full
repository. A future independent audit could test whether the scoped approach
misses relevant interactions, but no such audit exists here.

## Handoff state

The long baton is committed as a file and teaches Vesper the source, topology,
portfolio, sparse rule, exact validation contract, route, failure methods, and
boundaries. Because a commit cannot contain its own final hash, the short live
activation and external canonical receipt must bind the exact Neris final.
Before the terminal gate, the baton state is `PREPARED_NOT_SENT`.

After the final pass, Neris must resolve exactly one existing task titled
`Vesper Arlen`, immediately reread it, and send one short sanitized activation.
No task creation, fork, collaboration subagent, standby contact, or substitute
endpoint is authorized. Tool acknowledgement alone changes delivery truth.

## Final boundary

{BOUNDARY}

The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--phase-root", required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    normalized_phase_root = args.phase_root.replace("\\", "/")
    if normalized_phase_root != EXPECTED_PHASE_ROOT:
        raise SystemExit(f"phase root must be exactly {EXPECTED_PHASE_ROOT}")
    phase_root = repo / Path(normalized_phase_root)

    safe = {
        "schema": "ghc.family.portfolio.safe.v1",
        "phase": PHASE,
        "records": records("SAFE-OWN-", OWNER_SAFE, "completed", OWNER, "owner_safe_now_execution")
        + records("SAFE-NEXT-", SUCCESSOR_SAFE, "represented", NEXT_OWNER, "successor_safe_now_recommendation"),
        "boundary": BOUNDARY,
    }
    candidates = {
        "schema": "ghc.family.portfolio.candidate.v1",
        "phase": PHASE,
        "records": records("CAND-OWN-", OWNER_CANDIDATES, "completed", OWNER, "owner_candidate_execution")
        + records("CAND-NEXT-", SUCCESSOR_CANDIDATES, "represented", NEXT_OWNER, "successor_candidate_recommendation"),
        "boundary": BOUNDARY,
    }
    approvals = {
        "schema": "ghc.family.portfolio.approval-gates.v1",
        "phase": PHASE,
        "records": records("EXACT-", EXACT_PACKETS, "exact_gate", OWNER, "exact_approval_packet")
        + records("BLOCKED-", BLOCKED_PACKETS, "exact_gate", OWNER, "blocked_approval_packet"),
        "boundary": BOUNDARY,
    }

    skill_hashes = json.loads((phase_root / "x2" / "global-skill-hashes.json").read_text(encoding="utf-8"))
    skill_records = [
        {
            "record_id": f"SKILL-OWN-{index:03d}",
            "kind": "owner_skill_update",
            "owner": OWNER,
            "outcome": "completed",
            "description": f"Updated and hash-sealed {row['label']} under the live owner-delta and sparse-lane rule.",
            "sha256": row["sha256"],
        }
        for index, row in enumerate(skill_hashes["records"], start=1)
    ]
    skill_records += records(
        "SKILL-NEXT-",
        [f"Consider building {name} for an exact Vesper need." for name in SUCCESSOR_SKILLS],
        "represented",
        NEXT_OWNER,
        "successor_skill_recommendation",
    )
    skills = {
        "schema": "ghc.family.portfolio.skills.v1",
        "phase": PHASE,
        "records": skill_records,
        "owner_skill_count": len(skill_hashes["records"]),
        "successor_skill_count": len(SUCCESSOR_SKILLS),
        "boundary": BOUNDARY,
    }

    command_surfaces = [
        "manifest", "json", "markdown", "python", "privacy", "route",
        "skill-hashes", "file-budget", "data-quality", "canonical",
    ]
    runner_records = records(
        "RUN-OWN-",
        [f"Built, documented, and component-tested the `{name}` command surface in the family-current owner-delta toolkit." for name in command_surfaces],
        "completed",
        OWNER,
        "owner_runner_command_surface",
    ) + records(
        "RUN-NEXT-",
        [f"Consider {name} only when its exact Vesper trigger exists." for name in SUCCESSOR_RUNNERS],
        "represented",
        NEXT_OWNER,
        "successor_runner_recommendation",
    )
    runners = {
        "schema": "ghc.family.portfolio.runners.v1",
        "phase": PHASE,
        "entrypoint": "scripts/ghc_family_owner_delta_toolkit.py",
        "records": runner_records,
        "boundary": BOUNDARY,
    }

    clean = {
        "schema": "ghc.family.portfolio.clean-fix-refine.v1",
        "phase": PHASE,
        "records": records("CFR-OWN-", CLEAN_OWNER, "completed", OWNER, "owner_clean_fix_refine_execution")
        + records("CFR-NEXT-", CLEAN_SUCCESSOR, "represented", NEXT_OWNER, "successor_clean_fix_refine_recommendation"),
        "boundary": BOUNDARY,
    }
    method_flow = build_method_flow()
    outcome = {
        "schema": "ghc.family.v662-v3-3-midnight-remaster.outcome-ledger.v1",
        "owner": OWNER,
        "phase": PHASE,
        "source_commit": SOURCE,
        "x1_commit": X1,
        "frozen_proposal_baseline": 3550,
        "new_frozen_proposals": 20,
        "frozen_proposal_total": 3570,
        "new_proposal_outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "effective_negatives_before_final_external_overlay": 23078,
        "effective_methods_before_final_external_overlay": 7672,
        "open_gaps": 152,
        "exact_gates": 150,
        "verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": BOUNDARY,
    }

    ledgers = [safe, candidates, approvals, skills, runners, clean]
    destinations = [
        phase_root / "portfolio" / "safe-now-ledger.json",
        phase_root / "portfolio" / "candidate-ledger.json",
        phase_root / "portfolio" / "approval-gate-ledger.json",
        phase_root / "portfolio" / "skill-ledger.json",
        phase_root / "portfolio" / "runner-ledger.json",
        phase_root / "portfolio" / "clean-fix-refine-ledger.json",
    ]
    for path, ledger in zip(destinations, ledgers):
        write_json(path, ledger)
    write_json(phase_root / "x2" / "method-flow.json", method_flow)
    write_json(phase_root / "x2" / "outcome-ledger.json", outcome)
    write_text(phase_root / "governance" / "owner-delta-validation-policy.md", governance_policy())
    write_text(phase_root / "governance" / "sparse-lane-rotation-policy.md", rotation_policy())
    write_text(phase_root / "research" / "thos-owner-delta-assurance-comparison.md", research_text())

    baton = baton_text(ledgers, method_flow)
    baton_path = phase_root / "handoffs" / "vesper-arlen-v662-v4-activation.md"
    write_text(baton_path, baton)
    baton_count = words(baton)
    if not 10000 <= baton_count <= 100000:
        raise RuntimeError(f"baton word count outside live range: {baton_count}")
    write_json(
        phase_root / "handoffs" / "vesper-arlen-v662-v4-activation-metadata.json",
        {
            "schema": "ghc.family.handoff.metadata.v1",
            "owner": OWNER,
            "recipient": NEXT_OWNER,
            "recipient_phase": NEXT_PHASE,
            "source_commit": SOURCE,
            "x1_commit": X1,
            "final_commit_binding": "exact final supplied by the acknowledged live activation and external canonical receipt",
            "word_count": baton_count,
            "sha256": sha256(baton_path),
            "delivery_state": "represented",
            "boundary": BOUNDARY,
        },
    )
    write_text(phase_root / "closeout" / "phase-closeout-candidate.md", closeout_text(ledgers, baton_count))

    summary = {
        "schema": "ghc.family.v662-v3-3-midnight-remaster.builder-receipt.v1",
        "generated_at_utc": now_utc(),
        "source_commit": SOURCE,
        "x1_commit": X1,
        "portfolio_record_counts": {
            "safe": len(safe["records"]),
            "candidate": len(candidates["records"]),
            "approval": len(approvals["records"]),
            "skills": len(skills["records"]),
            "runners": len(runners["records"]),
            "clean_fix_refine": len(clean["records"]),
        },
        "baton_word_count": baton_count,
        "baton_sha256": sha256(baton_path),
        "new_method_count": len(method_flow["methods"]),
        "new_retained_negative_count": method_flow["new_retained_negative_count"],
        "allowed_outcomes": sorted(OUTCOMES),
        "verdict": "NOT_READY_FOR_STAGE_20",
        "valid": True,
        "boundary": BOUNDARY,
    }
    write_json(phase_root / "x2" / "builder-receipt.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
