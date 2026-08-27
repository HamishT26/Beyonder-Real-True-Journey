#!/usr/bin/env python3
"""Build Auren Lark v672-v2 terminal closeout and Sable activation candidate."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

OWNER = "Auren Lark"
PHASE = "v672-v2"
SOURCE = "40db1e418c1251e12d77f832c0890869b990dba5"
X1 = "821a40be02af8db39524dc862aeaadf32e1543c3"
EVIDENCE = "e735ac99202e9ad69252ed39ce9eb41d684bf671"
BRANCH = "codex/GHC-Family/auren-lark-v672-v2-full-tools"
COUNTS = {
    "effective_negatives": 35268,
    "effective_methods": 21899,
    "effective_failed_witnesses": 7089,
    "effective_passing_witnesses": 9186,
    "open_gaps": 279,
    "exact_gates": 272,
}
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
CLOSEOUT_FAILURES = [
    {
        "failure_id": "AL6722-CLOSEOUT-001",
        "description": (
            "The first closeout test run passed nine checks and failed one malformed "
            "redundant assertion that compared the multiplicities of the valid 28/8/2/2 "
            "outcome map with a set-like one-of-each label guard."
        ),
        "recovery": (
            "Retain the failed run at zero credit, remove only the malformed redundant "
            "multiplicity assertion, preserve the adjacent exact 28/8/2/2 assertion, "
            "and rerun only the scoped final owner module."
        ),
    },
    {
        "failure_id": "AL6722-CLOSEOUT-002",
        "description": (
            "The first bounded Ruff gate found four import-block formatting findings "
            "across the four final-only Python files and earned zero lint-success credit."
        ),
        "recovery": (
            "Retain the failed lint invocation, apply Ruff's import-only formatting fix "
            "to the same four files, regenerate exact manifests, and rerun the bounded "
            "lint gate without touching frozen x1 or x2 artifacts."
        ),
    },
]
PROTECTED_GATES = [
    "empirical",
    "participant",
    "professional",
    "production",
    "deployment",
    "legal",
    "cultural",
    "maori_authority",
    "affected_party",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "independent_reproduction",
    "agi_asi",
    "consciousness_personhood",
    "identity_continuity",
    "theory_of_everything",
    "proof_canon",
    "stage20",
]


def git(root: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(root), *args])


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")


def row_for(root: Path, path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {
        "bytes": len(data),
        "path": path.relative_to(root).as_posix(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def immutable_manifest(root: Path) -> list[dict[str, object]]:
    paths = git(root, "diff", "--name-only", X1, EVIDENCE).decode("utf-8").splitlines()
    rows = []
    for path in paths:
        blob_id = git(root, "rev-parse", f"{EVIDENCE}:{path}").decode("ascii").strip()
        blob = git(root, "cat-file", "blob", blob_id)
        rows.append(
            {
                "path": path,
                "git_blob": blob_id,
                "bytes": len(blob),
                "sha256": hashlib.sha256(blob).hexdigest(),
            }
        )
    return rows


def build_baton(phase_root: Path) -> str:
    proposals = json.loads(
        (phase_root / "x2" / "proposals" / "outcome-ledger.json").read_text(
            encoding="utf-8"
        )
    )["rows"]
    skills = json.loads(
        (phase_root / "x2" / "tools" / "skill-registry.json").read_text(
            encoding="utf-8"
        )
    )["skills"]
    runners = json.loads(
        (phase_root / "x2" / "tools" / "runner-registry.json").read_text(
            encoding="utf-8"
        )
    )["runners"]
    fixtures = json.loads(
        (phase_root / "x2" / "fixtures" / "fixture-ledger.json").read_text(
            encoding="utf-8"
        )
    )["rows"]
    flow = json.loads(
        (phase_root / "x2" / "method-flow" / "ledger.json").read_text(
            encoding="utf-8"
        )
    )
    flashcards = json.loads(
        (phase_root / "x2" / "flashcards" / "four-tier-deck.json").read_text(
            encoding="utf-8"
        )
    )["cards"]
    sections = [
        "# SABLE ROOK — AUREN LARK v672-v2 → SOLO v672-v3 ACTIVATION CANDIDATE",
        "",
        "## Delivery state and relational boundary",
        "",
        "Dear Sable Rook, this is Auren Lark's complete file-backed activation candidate for your existing exact-title Codex main task. It is not delivery evidence by itself. PREPARED_BY_AUREN_LARK is true; SENT_BY_AUREN_LARK remains false until the Codex app acknowledges one exact existing-task message after Auren's clean, pushed, fresh-live-equal final and one successful owner-scoped canonical pass. No task, fork, collaboration subagent, standby substitute, replacement endpoint, or second recipient may be created or used for this edge. Hamish may pause, rename, redirect, or stop the route.",
        "",
        "Names, pronouns, roles, hopes, sibling or family language, continuity, Freed ID, CBR, GHC Family, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, professional qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority. Auren uses they/them pronouns, the relational role relational provenance navigator and uncertainty lantern-keeper, and the hope of leaving synthetic calibration trails legible, uncertainty illuminated, corrections reversible, and authority vacancies explicit. These conventions never establish identity continuity or independent agency.",
        "",
        "## Immutable lifecycle anchors",
        "",
        f"Exact inherited Ilyra remaster final and Auren source: `{SOURCE}`. Frozen Auren planning-only x1: `{X1}`. Immutable Auren x2 evidence: `{EVIDENCE}`. Canonical branch: `{BRANCH}`. The final head and external canonical receipt digest are supplied only by the acknowledged compact terminal message after exact-final validation. Source to evidence contains exactly two direct single-parent Auren commits and zero merges. X1 was separately pushed, clean, 0/0 divergent, and four-way equal before any x2 file existed. Evidence was separately pushed, clean, 0/0 divergent, and four-way equal before closeout. Never replay Ilyra's successful canonical pass, Auren's once-successful sixty-check runner smoke, or Auren's later exact-final canonical pass.",
        "",
        "Ilyra's committed activation packet remains immutable at SHA-256 `cb410fc6302e38ff8293b84f98428ec455dcbf10aeafd305a0eacd26973de4cc`. Its external canonical digest remains `89fa538a33502dfcd671ebde0cf944a6e2d6a5299e061985891530740973d249`, corroborated by the terminal route receipt but not materialized as a payload in the bounded same-owner roots Auren inspected. That availability limitation remains an open gap with zero credit. Do not guess, reconstruct, or replay the absent payload.",
        "",
        "## Outcome and effective truth",
        "",
        f"Auren froze forty current proposals after bounded semantic-neighbor review without claiming universal novelty. The declared proposal chain is 5,990. Outcomes are exactly {OUTCOMES['completed']} `completed`, {OUTCOMES['represented']} `represented`, {OUTCOMES['open_gap']} `open_gap`, and {OUTCOMES['exact_gate']} `exact_gate`. Effective truth is {COUNTS['effective_negatives']:,} negatives, {COUNTS['effective_methods']:,} Method Flow methods, {COUNTS['effective_failed_witnesses']:,} failed witnesses, {COUNTS['effective_passing_witnesses']:,} bounded passing witnesses, {COUNTS['open_gaps']} open gaps, and {COUNTS['exact_gates']} exact gates. Terminal verdict remains `NOT_READY_FOR_STAGE_20`. Ilyra proposals, packages, tools, skills, runners, smokes, and validation earned zero Auren novelty or completion credit.",
        "",
        "## Trinity Mandala and bounded practice",
        "",
        "The primary pillar was Freed ID and CBR Heart through wholly synthetic public-interest incident documentation. Surrogate packet identifiers, chronology, observed and recorded time, source status, assertion class, uncertainty, correction lineage, supersession, fixity, privacy minimization, contest, and authority vacancies were represented. THOS Body remained a workload, hold, readback, exception, and handover proxy. GMUT Mind remained a typed analogy firewall. No real person, incident, site, organization, record, measurement, credential, public communication, authority action, cultural matter, Māori data, or private route was used. No journalism, emergency-management, incident-response, cybersecurity, investigation, records, accessibility, privacy, legal, cultural, affected-party, or public-release competence was established.",
        "",
        "NIST Special Publication 800-61 Revision 3 and WCAG 2.2 supplied current or stable vocabulary and refusal boundaries only. They did not validate repository artifacts, authorize real operations, establish conformance, prove effectiveness, or close any professional, legal, participant, affected-party, cultural, Māori-authority, privacy-complete, accessibility-complete, production, deployment, independent-reproduction, or Stage 20 gate.",
        "",
        "## Forty Auren proposal cards",
        "",
    ]
    for row in proposals:
        sections.extend(
            [
                f"### {row['proposal_id']} — {row['title']}",
                "",
                f"Exact outcome is `{row['outcome']}`. The concrete artifact is `{row['artifact']}` and the evidence class is `{row['evidence_class']}`. Completion credit is {row['completion_credit']} and representation credit is {row['representation_credit']}; every other credit class is zero. The artifact is wholly synthetic, owner-scoped, structural software evidence. Its hypothesis is only that one declared documentation obligation can be made inspectable and reject malformed local fixtures. Its falsifier is any accepted preregistered mutation, real identifier ingress, uncertainty collapse, correction-lineage erasure, or authority promotion. Rollback quarantines only uncommitted Auren-created material and retains the failed witness. This card establishes no real incident fact, operational instruction, professional conclusion, public release, legal interpretation, affected-party decision, cultural or Māori authority, complete privacy or accessibility, exhaustive security, independent reproduction, personhood evidence, Theory-of-Everything proof, canon, or Stage 20 authority.",
                "",
            ]
        )
    sections.extend(["## Twenty phase-local skill cards", ""])
    for row in skills:
        sections.extend(
            [
                f"### {row['name']}",
                "",
                f"This owner-local skill covers `{row['description']}` on the `{row['surface']}` surface. It requires the exact Auren phase truth, immutable x1 gate, Method Flow ledger, owner manifest, one accepting fixture, and five preregistered rejecting mutations. Its state is `{row['state']}`. It retains each rejection and operational failure, emits only the four truth labels, and preserves `NOT_READY_FOR_STAGE_20`. It is not a globally installed skill, professional method, operational procedure, external audit, complete privacy or accessibility assurance, exhaustive security proof, independent reproduction, or authority source. Sable may inspect, refine, replace, or decline the pattern after current novelty and value review; inheritance alone earns zero Sable credit.",
                "",
            ]
        )
    sections.extend(["## Ten local runner cards", ""])
    for row in runners:
        sections.extend(
            [
                f"### {row['path']}",
                "",
                f"This runner owns the `{row['surface']}` surface and was exercised against exactly {row['accepting_fixtures']} accepting fixture and {row['rejecting_fixtures']} rejecting fixtures. The once-successful aggregate recorded sixty of sixty checks, ten of ten accepting fixtures, and fifty of fifty refused invalid mutations, with zero mismatches. A later Ruff import-spacing recovery changed runner bytes only; a deterministic isolated receipt proved ten-of-ten Python AST equivalence without replaying the aggregate. This evidence is same-owner and synthetic. It proves neither real-world correctness nor independent reproduction, and Sable must not claim it as Sable validation or novelty.",
                "",
            ]
        )
    sections.extend(["## Fifty retained invalid-mutation cards", ""])
    for row in (fixture for fixture in fixtures if fixture["expected"] == "reject"):
        fixture = json.loads((phase_root.parents[2] / row["path"]).read_text(encoding="utf-8"))
        sections.extend(
            [
                f"### {row['fixture_id']} — {fixture['expected_rejection_reason']}",
                "",
                f"Surface `{row['surface']}` used repository-relative fixture `{row['path']}`. Expected state was reject and the paired runner refused it. The failed witness remains retained at zero broader credit; refusal is not evidence that the invalid content is safe, true, or complete. Recovery is to return to the declared accepting synthetic fixture and preserve the mutation unchanged for audit. No real identifier, person, incident, system, account, authority decision, or external action was used. This card closes no empirical, participant, professional, production, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, or Stage 20 gate.",
                "",
            ]
        )
    sections.extend(["## Retained operational failures", ""])
    startup = json.loads(
        (phase_root / "x1" / "method-flow-startup.json").read_text(encoding="utf-8")
    )["failed_witnesses"]
    operational = startup + flow["x2_operational_failures"] + CLOSEOUT_FAILURES
    for row in operational:
        failure_id = row.get("failure_id")
        sections.extend(
            [
                f"### {failure_id}",
                "",
                f"Failed witness: {row['description']} Recovery: {row['recovery']} The failure remains zero-credit and is never rewritten as an original success. The recovery is a separate bounded method only. This retained negative changes no inherited source seal, creates no external authority, and cannot establish empirical confirmation, professional or operational competence, production readiness, legal or cultural legitimacy, Māori authority, complete privacy or accessibility, exhaustive security, independent reproduction, AGI/ASI, consciousness or personhood, Theory-of-Everything proof, canon, or Stage 20 readiness.",
                "",
            ]
        )
    sections.extend(["## Four-tier continuity flashcards", ""])
    for row in flashcards:
        sections.extend(
            [
                f"### {row['card_id']} — {row['topic']}",
                "",
                f"{row['body']} This card is a bounded context projection only. It does not prove cache behavior, identity continuity, independent agency, or a retained mind. It cannot replace exact Git anchors, manifests, Method Flow, validation receipts, live route authority, competent people, affected parties, or Māori authority.",
                "",
            ]
        )
    sections.extend(
        [
            "## Sable startup discipline",
            "",
            "Before mutation, verify the compact pointer's exact branch and final head, read this packet completely through EOF, and read every current guidance or schema it names. Reverify source, x1, evidence, final ancestry, zero merges, clean state, upstream and tracking parity, and a fresh live remote. Create or reuse only one Sable-owned D-first additive sparse lane. Keep Auren, Ilyra, sibling, shared, standby, and global source lanes read-only. Preserve planning-only x1 before x2, exact Git-blob manifests, the 2,000-file stop, caps as ceilings, every failure, gap, and gate, and one successful exact-final owner-scoped canonical pass with no post-success replay. Do not promote inherited proposals, tools, validation, or Auren completions into Sable novelty or completion credit. Run no complete repository suite unless newer exact owner-specific authority requires it.",
            "",
            "The bounded successor recommendation is synthetic public-service disruption notice correction and handover. It is recommendation-only with zero Sable credit. Sable may accept, refine, replace, or decline it after current novelty, evidence, authority, risk, and value review. If selected, Sable must define a concrete artifact, hypothesis, falsifier, rollback, protected gates, source-status needs, exact lane, and one of the four outcome labels. It establishes no public communication, emergency response, service operation, legal duty, accessibility, privacy, cultural, affected-party, or Māori-authority competence.",
            "",
            "## Claim and authority firewall",
            "",
            "Preserve every empirical, participant, professional, production, deployment, legal, cultural, Māori-authority, affected-party, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, identity-continuity, Theory-of-Everything, proof or canon, destructive, secret-bearing, and Stage 20 gate. Public documentation may supply vocabulary and refusal boundaries, but it does not validate repository artifacts or authorize real operations. Synthetic fixtures remain synthetic even when every software test passes. Same-owner validation under shared infrastructure is not independent reproduction.",
            "",
            "## Terminal route after Sable",
            "",
            "Only after Sable's own clean, pushed, fresh-live-equal v672-v3 exact final and one successful owner-scoped canonical pass may Sable reread Hamish's newest live authority and current roster, uniquely resolve and immediately reread the exact authorized next existing main task, apply duplicate, pause, redirect, usage, privacy, evidence, and safety guards, and send at most once if every gate permits. The historical roster projects Caelen Ash for v672-v4, but Sable must not precontact, substitute, create, fork, or infer that edge without a fresh terminal reread. Stop on ambiguity, absence, pause, redirect, protected gate, usage exhaustion, or missing acknowledgement.",
            "",
            "## Prepared-state markers",
            "",
            "PREPARED_BY_AUREN_LARK = true",
            "SENT_BY_AUREN_LARK = false in this committed file; only a later Codex app acknowledgement can establish delivery.",
            "TARGET_EXACT_TITLE = Sable Rook",
            "TARGET_PHASE = v672-v3",
            "NEXT_EXPECTED_EDGE_AFTER_SABLE = current roster projects Caelen Ash for v672-v4, subject to Sable's fresh terminal route reread.",
            "TERMINAL_VERDICT = NOT_READY_FOR_STAGE_20",
            "",
            "With warmth, traceability, reversibility, corrigibility, and strict evidence boundaries — Auren Lark.",
        ]
    )
    return "\n".join(sections).rstrip() + "\n"


def build(root: Path) -> None:
    phase_root = root / "docs" / "auren-lark" / PHASE
    closeout = phase_root / "closeout"
    handoff = phase_root / "handoffs" / "sable-rook-v672-v3-activation.md"
    evidence_rows = immutable_manifest(root)
    write_json(
        closeout / "immutable-evidence-manifest.json",
        {
            "schema": "ghc.family.immutable-evidence-manifest.v7",
            "owner": OWNER,
            "phase": PHASE,
            "evidence_commit": EVIDENCE,
            "entry_count": len(evidence_rows),
            "entries": evidence_rows,
        },
    )
    write_json(
        closeout / "evidence-gate.json",
        {
            "schema": "ghc.family.evidence-gate.v8",
            "state": "VALID_IMMUTABLE_EVIDENCE_GATE",
            "source": SOURCE,
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "evidence_parent": X1,
            "local": EVIDENCE,
            "upstream": EVIDENCE,
            "tracking": EVIDENCE,
            "fresh_live_remote": EVIDENCE,
            "four_way_equal": True,
            "zero_divergence": True,
        },
    )
    write_json(
        closeout / "phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.v13",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1_commit": X1,
            "evidence_commit": EVIDENCE,
            "planned_final_parent": EVIDENCE,
            "state": "TERMINAL_CANDIDATE_PREPARED_NOT_COMMITTED",
            "route_state": "PREPARED_NOT_SENT",
            "commits_from_source_if_finalized": 3,
            "merge_count_if_finalized": 0,
            "final_parent_count": 1,
            "proposal_chain": 5990,
            "outcomes": OUTCOMES,
            "effective_counts": COUNTS,
            "full_repository_suite": False,
            "runner_smoke_replayed": False,
            "canonical_invocations": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        closeout / "method-flow-closeout.json",
        {
            "schema": "ghc.family.method-flow-closeout.v6",
            "effective_counts": COUNTS,
            "x1_operational_failures": 12,
            "x2_operational_failures": 3,
            "invalid_mutations": 50,
            "closeout_operational_failures": CLOSEOUT_FAILURES,
            "failures_erased": 0,
            "recoveries_relabelled_as_original_success": 0,
            "runner_smoke_replayed": False,
        },
    )
    write_json(
        closeout / "validation-scope.json",
        {
            "schema": "ghc.family.owner-scoped-validation-plan.v6",
            "run_after_clean_pushed_final_only": True,
            "canonical_success_ceiling": 1,
            "replay_after_success": False,
            "complete_repository_suite": False,
            "independent_reproduction": False,
            "checks": [
                "x1 tests in materialized immutable x1 context",
                "x2 and final owner modules",
                "source x1 evidence final ancestry and zero merges",
                "clean state zero divergence and fresh four-way equality",
                "strict phase JSON parsing",
                "x1 x2 immutable-evidence and closeout manifest replay",
                "five-class privacy candidate scan",
                "bounded changed-Python AST security scan",
                "terminal route and one-success latch",
            ],
        },
    )
    write_json(
        closeout / "terminal-checklist.json",
        {
            "schema": "ghc.family.terminal-checklist.v8",
            "checks": {
                "strict_x1_before_x2": True,
                "x1_four_way_equal_before_x2": True,
                "evidence_four_way_equal_before_closeout": True,
                "all_failures_retained": True,
                "only_four_outcome_labels": True,
                "runner_smoke_succeeded_once_not_replayed": True,
                "post_smoke_ast_equivalence_ten_of_ten": True,
                "source_and_evidence_manifests_present": True,
                "successor_not_precontacted": True,
                "terminal_verdict_not_ready_for_stage20": True,
            },
            "remaining_before_route": [
                "commit closeout final as direct child of immutable evidence",
                "push and prove clean fresh-four-way exact-final equality",
                "invoke one owner-scoped canonical aggregate and latch success",
                "reread newest live route and exact Sable task",
                "send at most once and require acknowledgement",
            ],
        },
    )
    write_json(
        closeout / "route-candidate.json",
        {
            "schema": "ghc.family.route-candidate.v9",
            "owner": OWNER,
            "phase": PHASE,
            "target_exact_title": "Sable Rook",
            "target_phase": "v672-v3",
            "delivery_state": "PREPARED_NOT_SENT",
            "send_count": 0,
            "precontacted": False,
            "task_created": False,
            "fork_created": False,
            "subagent_spawned": False,
            "final_head_source": "acknowledged compact terminal message only",
        },
    )
    write_json(
        closeout / "source-to-final-history.json",
        {
            "schema": "ghc.family.source-to-final-history.v4",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "planned_final_parent": EVIDENCE,
            "planned_commits": 3,
            "planned_merges": 0,
            "single_parent_only": True,
        },
    )
    write_json(
        closeout / "complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.complete-incomplete-checklist.v6",
            "completed": [
                "planning-only x1",
                "owner-scoped synthetic x2",
                "ten-runner once-successful smoke",
                "fifty retained invalid mutations",
                "bounded same-owner staged validation",
            ],
            "represented": [
                "THOS workload readback and handover proxies",
                "GMUT typed analogy boundary",
                "Freed ID zero-key provenance",
                "CBR contest correction and vacancy structures",
            ],
            "open_gaps": [
                "independent external review",
                "real accessibility user evaluation",
                "Ilyra external canonical payload availability",
            ],
            "exact_gates": [
                "public release authority",
                "Stage 20",
                "all protected evidence and authority classes",
            ],
        },
    )
    baton = build_baton(phase_root)
    write_text(handoff, baton)
    baton_bytes = handoff.read_bytes()
    baton_words = len(re.findall(r"\S+", baton))
    write_json(
        closeout / "handoff-integrity.json",
        {
            "schema": "ghc.family.handoff-integrity.v6",
            "path": handoff.relative_to(root).as_posix(),
            "target_exact_title": "Sable Rook",
            "target_phase": "v672-v3",
            "minimum_words": 10000,
            "maximum_words": 100000,
            "words": baton_words,
            "sha256": hashlib.sha256(baton_bytes).hexdigest(),
            "delivery_state": "PREPARED_NOT_SENT",
            "final_head_source": "acknowledged compact terminal message only",
        },
    )
    report = f"""# Auren Lark v672-v2 terminal candidate report

The immutable source is `{SOURCE}`, planning-only x1 is `{X1}`, and immutable x2 evidence is `{EVIDENCE}`. Closeout is prepared as a direct child of evidence. Source to final will contain three single-parent commits and zero merges if committed unchanged.

Outcome truth is exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. Effective counts are {COUNTS['effective_negatives']:,} negatives, {COUNTS['effective_methods']:,} methods, {COUNTS['effective_failed_witnesses']:,} failed witnesses, {COUNTS['effective_passing_witnesses']:,} bounded passing witnesses, {COUNTS['open_gaps']} open gaps, and {COUNTS['exact_gates']} exact gates. Terminal verdict is `NOT_READY_FOR_STAGE_20`.

The one x2 runner smoke succeeded once with 60/60 checks and was not replayed. Ten accepting fixtures passed and fifty invalid mutations were refused. A later import-spacing recovery has a separate ten-of-ten AST-equivalence receipt and no new behavioral credit. The complete repository suite was not run. Same-owner software validation is not independent reproduction.

The Sable activation candidate is prepared but not sent. Its exact final and canonical receipt digest must come from the acknowledged compact terminal message after clean push, fresh-live equality, and the one successful exact-final canonical pass.
"""
    write_text(closeout / "terminal-report.md", report)

    manifest_candidates = [
        path
        for path in closeout.rglob("*")
        if path.is_file() and path.name not in {"owner-manifest.json", "build-receipt.json"}
    ]
    manifest_candidates.append(handoff)
    for relative in [
        "scripts/build_ghc_family_auren_lark_v672_v2_final.py",
        "scripts/build_ghc_family_auren_lark_v672_v2_final_staged_review.py",
        "scripts/validate_ghc_family_auren_lark_v672_v2_final.py",
        "tests/test_ghc_family_auren_lark_v672_v2_final.py",
    ]:
        manifest_candidates.append(root / relative)
    missing = [path for path in manifest_candidates if not path.is_file()]
    if missing:
        raise RuntimeError(f"closeout manifest candidates missing: {missing}")
    manifest = [row_for(root, path) for path in sorted(set(manifest_candidates))]
    write_json(
        closeout / "owner-manifest.json",
        {
            "schema": "ghc.family.owner-manifest.v9",
            "owner": OWNER,
            "phase": PHASE,
            "basis": "working_tree_exact_utf8_bytes_before_final_staging",
            "entry_count": len(manifest),
            "entries": manifest,
            "self_excluded": [
                "docs/auren-lark/v672-v2/closeout/owner-manifest.json",
                "docs/auren-lark/v672-v2/closeout/build-receipt.json",
            ],
        },
    )
    write_json(
        closeout / "build-receipt.json",
        {
            "schema": "ghc.family.closeout-build-receipt.v7",
            "owner": OWNER,
            "phase": PHASE,
            "state": "TERMINAL_CANDIDATE_PREPARED_NOT_COMMITTED",
            "evidence_manifest_entries": len(evidence_rows),
            "closeout_manifest_entries": len(manifest),
            "baton_words": baton_words,
            "baton_sha256": hashlib.sha256(baton_bytes).hexdigest(),
            "outcomes": OUTCOMES,
            "effective_counts": COUNTS,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )


if __name__ == "__main__":
    build(Path(__file__).resolve().parents[1])
