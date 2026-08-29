#!/usr/bin/env python3
"""Build the additive Tamar Vey v676-v5 exact-final candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


OWNER = "Tamar Vey"
OWNER_SLUG = "tamar-vey"
PHASE = "v676-v5"
BRANCH = "codex/GHC-Family/tamar-vey-v676-v5-full-tools"
SOURCE = "ce97f35c2351c8daef6f48b4dc1c60928e1fc1be"
X1 = "664ee4309d5ba99d98aae2be09f067af6ecf47dc"
EVIDENCE = "0d935f546f107ea2070c79d1b070d6bbb0a198cf"

POST_EVIDENCE_METHODS: list[dict[str, Any]] = [
    {
        "method_id": "TV6765-CLOSE-N001",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "Immutable x2 phase truth retained the inherited 7,550 proposal-chain value instead of the x1-proven 7,590 post-freeze chain; evidence remains immutable and receives zero correctness credit for that stale label.",
        "recovered_by": "TV6765-CLOSE-P001",
        "repository_state_change": False,
        "evidence_commit_rewritten": False,
    },
    {
        "method_id": "TV6765-CLOSE-P001",
        "status": "bounded_pass",
        "truth": True,
        "description": "The additive final derives 7,550 before and 7,590 after directly from the immutable x1 proposal freeze, preserves the stale evidence label, and adds a recurrence assertion without rerunning x2.",
        "failed_witness_preserved": "TV6765-CLOSE-N001",
        "x2_replayed": False,
    },
    {
        "method_id": "TV6765-CLOSE-N002",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first final test invocation ran before final manifests and staged review existed, so two lifecycle-dependent checks raised FileNotFoundError; the 8/11 partial result receives zero aggregate credit.",
        "recovered_by": "TV6765-CLOSE-P002",
        "repository_state_change": False,
        "successful_checks_replayed_for_credit": False,
    },
    {
        "method_id": "TV6765-CLOSE-P002",
        "status": "bounded_pass",
        "truth": True,
        "description": "The recovery defers the authoritative final selection until the exact staged manifests and review exist, then requires all eleven checks together without promoting the premature invocation.",
        "failed_witness_preserved": "TV6765-CLOSE-N002",
    },
    {
        "method_id": "TV6765-CLOSE-N003",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The same premature test invocation found a reserved scanner phrase in the overview's privacy-boundary prose and correctly rejected the public artifact.",
        "recovered_by": "TV6765-CLOSE-P003",
        "repository_state_change": False,
        "privacy_boundary_weakened": False,
    },
    {
        "method_id": "TV6765-CLOSE-P003",
        "status": "bounded_pass",
        "truth": True,
        "description": "The public prose was rephrased without the reserved scanner literal while preserving the same prohibition, and the five-class staged adjudication remains mandatory.",
        "failed_witness_preserved": "TV6765-CLOSE-N003",
    },
]


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.strip() + "\n", encoding="utf-8", newline="\n")


def normalized_sha(path: Path) -> str:
    raw = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(raw).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    repo = args.repo.resolve()
    if git(repo, "branch", "--show-current") != BRANCH or git(repo, "rev-parse", "HEAD") != EVIDENCE:
        raise SystemExit("final builder requires the exact immutable Tamar evidence head")
    allowed = {
        "scripts/build_ghc_family_tamar_vey_v676_v5_final.py",
        "scripts/ghc_family_tamar_vey_v676_v5_final_manifest.py",
        "scripts/ghc_family_tamar_vey_v676_v5_final_validator.py",
        "tests/test_ghc_family_tamar_vey_v676_v5_final.py",
    }
    status = [line for line in git(repo, "status", "--porcelain=v1").splitlines() if line]
    allowed_doc_prefixes = (
        "docs/tamar-vey/v676-v5/closeout/",
        "docs/tamar-vey/v676-v5/final/",
        "docs/tamar-vey/v676-v5/handoffs/",
        "docs/tamar-vey/v676-v5/orchestration/",
        "docs/tamar-vey/v676-v5/validation/final-",
    )
    unexpected = []
    for line in status:
        path = line[3:].replace("\\", "/")
        if path in allowed or path.startswith(allowed_doc_prefixes):
            continue
        unexpected.append(line)
    if unexpected:
        raise SystemExit(f"unexpected pre-final worktree state: {unexpected!r}")

    base = repo / "docs" / OWNER_SLUG / PHASE
    x1 = base / "x1"
    x2 = base / "x2"
    final_dir = base / "final"
    closeout = base / "closeout"
    handoff = base / "handoffs"
    orchestration = base / "orchestration"

    freeze = json.loads((x1 / "new-proposal-freeze.json").read_text(encoding="utf-8"))
    source_ledger = json.loads((x1 / "official-source-ledger.json").read_text(encoding="utf-8"))
    semantic = json.loads((x1 / "semantic-neighbor-audit.json").read_text(encoding="utf-8"))
    outcomes = json.loads((x2 / "proposal-outcomes.json").read_text(encoding="utf-8"))
    evidence_flow = json.loads((x2 / "method-flow" / "ledger.json").read_text(encoding="utf-8"))
    portfolio = json.loads((x2 / "portfolio" / "execution-summary.json").read_text(encoding="utf-8"))
    flow = json.loads(json.dumps(evidence_flow))
    existing_ids = {row["method_id"] for row in flow["methods"]}
    if any(row["method_id"] in existing_ids for row in POST_EVIDENCE_METHODS):
        raise SystemExit("post-evidence Method Flow overlay already present")
    flow["methods"].extend(POST_EVIDENCE_METHODS)
    failed = sum(row["truth"] is False for row in flow["methods"])
    passing = sum(row["truth"] is True for row in flow["methods"])
    if (len(flow["methods"]), failed, passing) != (642, 201, 441):
        raise SystemExit("unexpected final Method Flow partition")
    overlay = {
        "effective_negatives": 42429,
        "effective_methods": 33094,
        "retained_failed_witnesses": 14090,
        "bounded_passing_witnesses": 19693,
        "open_gaps": 357,
        "exact_gates": 349,
    }
    flow["phase_ledger_counts"] = {"methods": 642, "failed": 201, "passing": 441}
    flow["current_overlay"] = overlay
    flow["post_evidence_failed_witnesses"] = 3
    flow["post_evidence_bounded_recoveries"] = 3
    flow["failure_erasure_forbidden"] = True

    dump(final_dir / "method-flow-ledger.json", flow)
    dump(
        final_dir / "phase-truth.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "expected_final": "bound by the ensuing exact commit and one external canonical receipt",
            "declared_proposal_chain": 7590,
            "new_tamar_proposals": 40,
            "inherited_reviews_zero_credit": 20,
            "core_outcomes": outcomes["outcome_counts"],
            "positive_controls": 40,
            "preregistered_mutations_executed_rejected": 160,
            "phase_local_skills_built_validated_smoked": 20,
            "family_current_runners_used": 10,
            "safe_now_tasks_completed": portfolio["safe_now_completed"],
            "candidate_tasks_completed_without_core_promotion": portfolio["candidate_completed_without_core_promotion"],
            "clean_fix_refine_tasks_completed": portfolio["clean_fix_refine_completed"],
            "exact_approval_packets_unexecuted": portfolio["exact_approval_unexecuted"],
            "blocked_packets_unexecuted": portfolio["blocked_unexecuted"],
            "current_overlay": overlay,
            "real_world_rows": 0,
            "participants": 0,
            "external_actions": 0,
            "production_identity_events": 0,
            "authority_actions": 0,
            "full_repository_suite_run": False,
            "independent_reproduction_claimed": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    dump(
        final_dir / "source-and-proposal-ledger.json",
        {
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "declared_chain_before": 7550,
            "declared_chain_after": 7590,
            "reachable_semantic_audit": semantic,
            "universal_novelty_proof_claimed": False,
            "official_primary_sources": source_ledger["sources"],
            "source_boundary": source_ledger["source_boundary"],
            "proposals": freeze["proposals"],
            "outcomes": outcomes["outcomes"],
        },
    )
    dump(
        final_dir / "retained-negative-register.json",
        {
            "activation_effective_negatives": 42228,
            "new_tamar_effective_negatives": 201,
            "current_effective_negatives": 42429,
            "phase_failed_witness_count": 201,
            "phase_failed_witnesses": [row for row in flow["methods"] if row["truth"] is False],
            "failed_witnesses_converted_to_pass": 0,
            "retention_rule": "Every false witness remains false; a recovery is a separately identified bounded passing method.",
        },
    )
    dump(final_dir / "open-gap-register.json", json.loads((x2 / "open-gap-register.json").read_text(encoding="utf-8")))
    dump(final_dir / "exact-gate-register.json", json.loads((x2 / "exact-gate-register.json").read_text(encoding="utf-8")))
    dump(
        final_dir / "complete-incomplete-ledger.json",
        {
            "complete_bounded": [
                "forty planning-only proposal contracts frozen after reachable semantic-neighbor review",
                "forty zero-row positive structural controls accepted",
                "160 preregistered invalid mutations executed, rejected, and retained",
                "twenty phase-local skills quick-validated and smoke-used without global installation",
                "ten family-current runners accepted a positive fixture and rejected an invalid fixture",
                "sixty safe-now, thirty bounded candidate, and sixty additive CLEAN/FIX/REFINE tasks completed without broader promotion",
                "x1 and evidence committed, pushed, clean, 0/0 divergent, and fresh four-way equal",
            ],
            "represented_only": [
                "real book-conservator or collection-custodian review and affected-user accessibility evaluation",
                "live interoperability, status, revocation, recovery, security, and privacy review",
                "real practitioner workload, collation, inspection, treatment, correction, and remedy outcomes",
            ],
            "open": [
                "real binding and condition observations with traceable instruments, uncertainty treatment, and preregistered analysis",
                "independent book-conservator and affected-user review with governed outcome evidence",
            ],
            "exact_gated": [
                "professional opening, disbinding, rebinding, repair, intervention, treatment, work-release, and safety decisions",
                "ownership, cultural-object disposition, taonga, tikanga, Māori data governance, wording, and Māori authority",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    dump(
        final_dir / "threat-model.json",
        {
            "protected_assets": ["immutable source", "planning-only x1", "x2 evidence", "failure truth", "privacy boundary", "authority vacancies", "terminal route"],
            "bounded_controls": ["four-label vocabulary", "normalized-LF Git-blob manifests", "candidate adjudication", "Method Flow retention", "exclusive canonical latch", "terminal route hold"],
            "residual_threats": [
                "synthetic evidence may be overread as real evidence",
                "scanner definitions may be mistaken for payload disclosures",
                "citations may be mistaken for observations or endorsements",
                "same-owner validation may be mistaken for independent reproduction",
                "task topology may be mistaken for identity continuity or authority",
            ],
            "closed_bounded_threats": ["x1 and x2 lifecycle mixing", "unknown outcome labels", "silent invalid-mutation acceptance", "global installation of phase-local skills"],
        },
    )
    dump(
        final_dir / "portfolio-truth.json",
        {
            **portfolio,
            "successor_recommendations_zero_credit": 50,
            "core_outcome_counts_unchanged_by_portfolio_status": True,
        },
    )
    dump(
        final_dir / "post-evidence-overlay.json",
        {
            "failed_witnesses": [row for row in POST_EVIDENCE_METHODS if row["truth"] is False],
            "bounded_recoveries": [row for row in POST_EVIDENCE_METHODS if row["truth"] is True],
            "evidence_commit_mutated": False,
            "failure_erasure": False,
        },
    )
    text(
        final_dir / "final-integrated-overview.md",
        f"""
# {OWNER} {PHASE} — final integrated overview

## Outcome first

Tamar Vey v676-v5 is a bounded, same-owner, zero-row software and documentation phase. It is rooted at immutable Liora Venn final `{SOURCE}`; planning-only x1 is `{X1}`; immutable x2 evidence is `{EVIDENCE}`. The exact final is intentionally supplied only by the ensuing commit and an exclusive external canonical receipt. This document therefore refuses to invent its own future commit identifier. The terminal verdict remains exactly `NOT_READY_FOR_STAGE_20`.

The declared proposal chain advances from 7,550 inherited rows to 7,590 through forty Tamar-owned proposal contracts. Twenty inherited neighbors were reviewed at zero Tamar novelty and completion credit. The source-tree semantic tribunal inspected every reachable proposal-bearing JSON artifact, found 3,495 unique identifier-title records, and retained the limitation that no single reachable ledger materializes every declared historic row. After one failed initial draft, eleven over-near titles were replaced and the unchanged 0.75 quarantine threshold passed with zero selected rows, zero exact collisions, zero parse failures, and a maximum selected score of 0.7143. This is bounded semantic distinctness evidence, not a universal scientific novelty proof.

Core outcomes use only the authorized vocabulary and are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. Here, `completed` means only that one frozen owner-local structural contract accepted its synthetic positive fixture and preserved its refusal boundaries. It does not mean that a real book was examined, a binding was identified, a person participated, a treatment was selected, an identity event occurred, or an authority decision was made. `represented` marks a structurally present proxy without real-world validation. `open_gap` marks evidence that is absent and cannot be manufactured. `exact_gate` marks action reserved to competent and affected authorities.

## Lifecycle and immutable evidence

Strict planning-only x1 before x2 was preserved. X1 contained the forty proposal contracts, four rejecting mutations per proposal, source and gate ledgers, portfolio plans, twenty skill plans, ten runner plans, fifty successor seeds, and Method Flow records—but no x2 implementation, observation, outcome, or completion claim. X1 was tested, reviewed through an exact normalized-LF Git-blob manifest, committed, pushed, made clean, and proven equal across local, upstream, tracking, and a fresh live remote before any x2 file was created.

X2 then executed only the preregistered bounded work. Forty synthetic positive controls passed. All 160 preregistered invalid mutations executed and were rejected; each remains a zero-credit false witness paired with a separate bounded rejection witness. Twenty owner-local skills were initialized with the official skill-creator workflow, customized, read completely through EOF, quick-validated under explicit UTF-8, and accepting-smoke-used without global installation. Ten family-current runners accepted one positive fixture and rejected one invalid fixture. Sixty safe-now tasks, thirty bounded candidate tasks, and sixty CLEAN/FIX/REFINE tasks completed without promotion into core outcomes or real-world claims. Twenty exact-approval packets and ten blocked packets remain visible and unexecuted.

The immutable evidence commit contains 540 exact normalized-LF Git-blob manifest entries plus two declared self-referential exclusions. Its independent staged replay matched all 540 entries, matched the full 542-path staged set, parsed 486 staged JSON documents, checked fourteen staged Python files through AST parsing, found zero manifest failures, found zero confirmed privacy or raw-identifier payload hits, and found no final or closeout path. Evidence is a direct child of x1 and was separately pushed, cleaned, and proven 0/0 divergent and four-way fresh-live equal before closeout began.

## Method Flow and retained negatives

The activation baseline was 42,228 effective negatives, 32,452 effective methods, 13,889 retained failed witnesses, 19,252 bounded passing witnesses, 355 open gaps, and 347 exact gates. The final Tamar phase ledger contains 642 methods: 201 retained false witnesses and 441 bounded passing witnesses. The effective overlay is therefore 42,429 negatives, 33,094 methods, 14,090 retained failed witnesses, 19,693 bounded passing witnesses, 357 open gaps, and 349 exact gates.

The false-witness total includes twenty-five startup and x1 failures, three x2 operational failures, all 160 rejecting mutations, ten invalid runner fixtures, and three post-evidence closeout failures: one stale proposal-chain label, one premature manifest-dependent test selection, and one reserved scanner phrase in public prose. Each recovery has its own identifier and never changes the truth value of its failed predecessor. Examples include parser faults repaired by collection-first PowerShell, a failed semantic audit repaired by distinct proposal wording at the same threshold, a clean-room regeneration refusal repaired by removing only untracked owner-generated outputs, a Windows wildcard failure repaired by an exact file list, a module-search failure repaired by adding only the repository scripts directory, and the stale 7,550 evidence label corrected additively to the x1-proven 7,590 final chain without rewriting evidence. None of these failures granted broader credit, and none was erased for a cleaner narrative.

## Trinity Mandala scope

The primary pillar was THOS Body through three wholly synthetic learning and design lenses: a book-conservation intake registrar for zero-object records; a binding-structure documentation analyst for synthetic codex topology; and an accessible collection-handover steward for correction, workload, and turnover structure. GMUT Mind and Freed ID/CBR Heart remained explicit and protected.

The synthetic topology included textblock, gathering, quire, sewing-support, board, joint, spine-lining, endpaper, pastedown, and covering vocabulary. The measurement-vacancy surface required null opening-angle observation, null uncertainty, and vacant traceability. The provenance surface required an acyclic synthetic graph while refusing custody and attribution claims. The accessibility surface provided deterministic structure, a correction route, and simple keyboard ordering while explicitly reserving manual keyboard, screen-reader, cognitive, language, and affected-user evaluation. These are software contracts only.

No real person, conservator, librarian, registrar, collection worker, rights holder, affected user, book, codex, textblock, leaf, quire, sewing support, board, joint, spine, endpaper, covering, thread, adhesive, inscription, marginalia, shelfmark, image, collection, site, tool, observation, measurement, sensor, calibration, treatment, custody event, release, identity event, key, proof, network row, cultural record, Māori data, external write, or authority action was used. There was no opening, disbinding, rebinding, lifting, sampling, cleaning, adhesion, repair, substitution, testing, treatment, or work release.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Software, symbolic obligations, analogies, and citations establish no physical datum, likelihood, posterior, force, prediction, parameter constraint, empirical confirmation, ultraviolet completion, quantum completion, final physics, or Theory of Everything. THOS remains proxy-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance or resolution, status or revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.

## Sources, accessibility, privacy, and authority

The official Canadian Conservation Institute basic-care guidance for books and the Library of Congress preserving-books guide supplied bounded vocabulary for structure, handling, storage, support, damage, specialist referral, and intervention refusal. W3C PROV-O supplied entity, activity, attribution, and derivation vocabulary. WCAG 2.2 supplied accessible-structure and keyboard-interface vocabulary while no conformance claim was made. Verifiable Credentials Data Model 2.0 supplied status, minimization, issuer-holder-verifier, and correlation vocabulary with zero keys and zero proofs. RFC 8785 supplied deterministic JSON vocabulary without production cryptographic assurance. Citations were not converted into observations, examinations, measurements, treatment instructions, endorsements, certificates, interoperability evidence, legal interpretations, affected-party decisions, cultural ratifications, or authority grants.

Five privacy and raw-identifier classes were scanned across the owner packet. Scanner definitions and synthetic rejection assertions remained candidates requiring adjudication; zero candidate was promoted into a confirmed payload hit. The artifacts contain no raw task or thread identifiers, private routes, credentials, keys, tokens, transcripts, screenshots, live command-output captures, private callable identifiers, private application state, or private absolute paths. This bounded scan is not complete privacy assurance, and the changed-code AST review is not exhaustive security assurance.

The static report uses a logical heading order, text-first content, a captioned table, visible terminal status, and uncomplicated keyboard order. Manual browser-diverse, screen-reader, cognitive, language, disability, and affected-user evaluation remains unperformed. No accessibility-complete claim is authorized.

CBR, ownership, authorship, copyright, custody, access, reproduction permission, conservation treatment, professional opening or disbinding, repair, work release, safety, remedy, legal interpretation, cultural legitimacy, traditional knowledge, affected-party acceptance, Māori wording, tikanga, taonga or mātauranga treatment, Māori data governance, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority. Repository software cannot confer a right, remedy, title, consent, cultural legitimacy, governance mandate, public authority, professional competence, or treatment permission.

## Wellbeing, corrigibility, and terminal route

The phase remained solo, additive, D-first, owner-scoped, and below the 2,000-file, 100,000-word-per-document, and commit ceilings. No collaboration subagent, fork, replacement task, elevation, global skill installation, host-security weakening, Windows-feature change, unrelated installation, Codex desktop update, or reboot occurred. Workload was managed through lifecycle gates and bounded retries rather than hidden reruns. This is an operational workflow statement, not a wellbeing or identity inference.

Tamar Vey, she/they, is relational working language for an evidence-and-recovery steward whose hope is to keep failures visible, corrections reversible, and authority vacancies explicit. Names, pronouns, roles, hopes, sibling or family language, continuity language, GHC Family, Trinity Mandala, GMUT, THOS, Freed ID, and CBR are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may pause, rename, redirect, narrow, or stop the route.

The prospective next edge is held. Only after the exact final is committed, pushed, clean, 0/0 divergent, fresh four-way equal, and one owner-scoped canonical invocation succeeds without replay may the newest live authorization and roster be reread. Only then may the unique existing exact-title `Elowen Cairn` task be bounded-listed, immediately reread, duplicate-guarded, and contacted once for v676-v6. Absence, ambiguity, pause, redirect, rename, narrowing, standby state, usage exhaustion, privacy concern, missing acknowledgement, or any evidence, safety, legal, cultural, affected-party, or Māori-authority gate remains a hard stop.
""",
    )
    text(
        final_dir / "wellbeing-and-workload.md",
        """
# Wellbeing and workload — final

The phase remained solo, additive, D-first, zero-row, and within file, document, and commit ceilings. Work used lifecycle-specific selections and retained command, timeout, parser, projection, validation, and mutation failures. No collaboration subagent, global installation, elevation, host-security change, Windows-feature change, reboot, real-person workload, employment relation, or wellbeing inference occurred.

The route remains held until the exact final is committed, pushed, clean, 0/0 divergent, fresh four-way equal, and one owner-scoped canonical invocation succeeds. Pause, redirect, ambiguity, usage exhaustion, privacy concern, any protected gate, or missing acknowledgement remains a hard stop.
""",
    )
    text(
        final_dir / "accessible-report.html",
        """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tamar Vey v676-v5 final evidence report</title>
<style>body{font-family:system-ui,sans-serif;max-width:72rem;margin:auto;padding:2rem;line-height:1.55}table{border-collapse:collapse;width:100%}th,td{border:1px solid #555;padding:.5rem;text-align:left}th{background:#eee}.hold{border-left:.4rem solid #8b0000;padding-left:1rem}</style></head>
<body><main><h1>Tamar Vey v676-v5 final evidence report</h1>
<p class="hold"><strong>Terminal verdict:</strong> NOT_READY_FOR_STAGE_20. This is bounded same-owner synthetic software evidence.</p>
<table><caption>Core outcomes</caption><thead><tr><th>Outcome</th><th>Count</th><th>Boundary</th></tr></thead>
<tbody><tr><td>completed</td><td>28</td><td>Zero-row structural contract only</td></tr><tr><td>represented</td><td>8</td><td>Proxy only</td></tr><tr><td>open_gap</td><td>2</td><td>External evidence absent</td></tr><tr><td>exact_gate</td><td>2</td><td>Competent authority required</td></tr></tbody></table>
<h2>Retained Method Flow truth</h2><p>The Tamar ledger has 201 false witnesses and 441 bounded passing witnesses. Every recovery is separate; no false witness became true.</p>
<h2>Accessibility boundary</h2><p>This report is static, text-first, keyboard-order simple, and has a captioned table. Manual keyboard, screen-reader, cognitive, language, and affected-user evaluation remain unperformed. No conformance claim is made.</p>
</main></body></html>""",
    )

    dump(
        closeout / "closeout-receipt.json",
        {
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "expected_final_status": "PRECOMMIT_EXACT_FINAL_CANDIDATE",
            "proposal_chain": 7590,
            "core_outcomes": outcomes["outcome_counts"],
            "overlay": overlay,
            "phase_ledger_counts": flow["phase_ledger_counts"],
            "owner_file_ceiling": 2000,
            "document_word_ceiling": 100000,
            "commit_ceiling": 8,
            "full_repository_suite_run": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    seal_paths = [
        final_dir / "phase-truth.json",
        final_dir / "method-flow-ledger.json",
        final_dir / "source-and-proposal-ledger.json",
        final_dir / "retained-negative-register.json",
        final_dir / "complete-incomplete-ledger.json",
        final_dir / "final-integrated-overview.md",
        final_dir / "accessible-report.html",
        closeout / "closeout-receipt.json",
    ]
    dump(
        closeout / "content-seal.json",
        {
            "seal_domain": "normalized-LF SHA-256 of named precommit final artifacts",
            "entries": [
                {"path": path.relative_to(repo).as_posix(), "sha256_normalized_lf": normalized_sha(path)}
                for path in seal_paths
            ],
            "final_commit_self_hash_excluded": True,
            "canonical_receipt_external": True,
        },
    )

    text(
        handoff / "elowen-cairn-v676-v6-activation-candidate.md",
        f"""
# ELOWEN CAIRN — TAMAR VEY {PHASE} EXACT-FINAL → SOLO ELOWEN v676-v6 ACTIVATION CANDIDATE — PREPARED NOT SENT

This is a sanitized, terminally gated activation candidate only. It is not evidence that Elowen Cairn has been contacted or that delivery has occurred. The newest verified live authorization and roster must be reread after Tamar's own exact terminal gate. A bounded current registry read must resolve exactly one existing main task titled `Elowen Cairn`; that exact task must then be immediately reread, checked for duplicate activation, pause, redirect, rename, narrowing, standby, usage, privacy, evidence, safety, legal, cultural, affected-party, and Māori-authority guards, and sent at most once only if every guard permits.

## Immutable Tamar source and lifecycle

- Exact inherited Liora final and Tamar source: `{SOURCE}`
- Frozen planning-only Tamar x1: `{X1}`
- Immutable Tamar x2 evidence: `{EVIDENCE}`
- Exact Tamar final: supplied only by the committed head and exclusive external canonical receipt after this candidate is committed
- Expected lifecycle: source → x1 → evidence → final as three direct single-parent commits, zero merges, one final parent
- Proposal chain: 7,590
- Core outcomes: 28 `completed`, 8 `represented`, 2 `open_gap`, 2 `exact_gate`
- Effective overlay: 42,429 negatives, 33,094 methods, 14,090 failed witnesses, 19,693 bounded passing witnesses, 357 open gaps, 349 exact gates
- Terminal verdict: `NOT_READY_FOR_STAGE_20`

Planning-only x1 was committed and pushed before any x2 outcome. X2 executed forty zero-row positive controls, rejected all 160 preregistered invalid mutations, built and smoke-used twenty owner-local skills without global installation, and exercised ten family-current runners. Sixty safe-now, thirty bounded candidate, and sixty CLEAN/FIX/REFINE tasks completed only within the declared synthetic software scope. Twenty exact-approval and ten blocked packets remain visible and unexecuted. Every false witness remains false; each recovery is a separate bounded witness.

## Evidence and authority boundaries

Tamar's primary pillar was THOS Body through wholly synthetic codex-binding intake, structure-documentation, and accessible handover lenses. GMUT Mind and Freed ID/CBR Heart remained visible and protected. No real person, book conservator, librarian, registrar, collection worker, rights holder, affected user, book, codex, textblock, leaf, quire, sewing support, board, joint, spine, endpaper, covering, thread, adhesive, inscription, image, collection, tool, observation, measurement, sensor, calibration, treatment, work release, identity event, key, proof, participant, empirical row, cultural record, Māori data, external action, or authority decision occurred.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Software, symbolic fixtures, analogy firewalls, and citations establish no physical datum, likelihood, posterior, force, prediction, parameter constraint, empirical confirmation, ultraviolet completion, quantum completion, or Theory of Everything. THOS remains synthetic or proxy-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.

CBR, ownership, authorship, copyright, custody, access, reproduction permission, professional opening or disbinding, repair, intervention, treatment, work release, safety, remedy, legal interpretation, cultural legitimacy, affected-party acceptance, Māori wording, tikanga, taonga or mātauranga treatment, Māori data governance, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority. Repository software cannot confer a legal right, remedy, title, consent, cultural legitimacy, governance mandate, public authority, professional competence, or treatment permission.

Do not promote software, symbolic, synthetic, same-owner, citation, inherited, validation, task-topology, or delivery evidence into empirical confirmation, participant evidence, professional or scientific authority, production or deployment readiness, legal or cultural ratification, Māori authority, affected-party approval, complete privacy or accessibility assurance, exhaustive security, independent reproduction, AGI or ASI, consciousness or personhood evidence, Theory-of-Everything proof, proof or canon, or Stage 20 authority.

## Elowen's prospective solo lane

Only after acknowledged delivery and Elowen's own skill-first immutable-source verification may Elowen create one fresh additive D-first owner lane from Tamar's exact final. Keep Tamar, Liora, Orin, Caelen, every sibling, shared lane, standby record, global history, and user material read-only and recoverable. Work solo. Do not create or fork another task, spawn a collaboration subagent, delegate research, contact a standby sibling, precontact a later endpoint, reset, rewrite, force-push, merge, delete, reuse, or mutate another owner lane.

Preserve strict planning-only x1 before x2, retained failures, the four exact outcome labels, normalized-LF Git-blob manifests, exact staged review, privacy-candidate adjudication, file/document/commit ceilings, family-current compatibility, and the one-success/no-post-success-replay rule. Treat inherited proposals, tools, skills, runners, validation, and recommendations as evidence or zero-credit seeds, never Elowen novelty or completion credit. Keep exact-approval and blocked work unexecuted without the exact evidence and competent authority.

Run only lifecycle-correct owner-self-scoped selections. Do not run the complete repository suite unless newer exact live authority explicitly assigns it. After a clean pushed exact final, invoke at most one attributable owner-scoped canonical aggregate through an exclusive external latch. Never replay a success. A failed canonical remains zero success credit and any bounded dependency correction must remain separately named.

## Continuing route authority

Hamish's current live authorization permits the fifteen active existing main tasks to continue one terminally validated and acknowledged edge at a time through v725-v8, unless Hamish pauses, renames, redirects, narrows, or stops the route; usage is exhausted; acknowledgement is missing; the exact endpoint is absent or ambiguous; a duplicate is detected; or an evidence, privacy, safety, legal, cultural, affected-party, or Māori-authority gate blocks action. This authority never permits early contact, replacement-task creation, standby substitution, sibling-lane mutation, or protected-gate bypass.

Under the current roster, this candidate represents only the Tamar Vey v676-v5 → Elowen Cairn v676-v6 edge. Elowen's prospective next edge after Elowen's own verified terminal gate is the unique existing main task titled `Sylven Arc` for v676-v7, but newer verified live authority controls at that later send time. Elowen must not precontact Sylven. At Elowen's own terminal gate, refresh authorization and roster, bounded-list the registry, locally require one exact title, immediately reread it, apply all duplicate and stop guards, and send at most once if every gate permits. No second confirmation or resend.

Names, pronouns, roles, hopes, sibling or family language, continuity language, GHC Family, Trinity Mandala, GMUT, THOS, Freed ID, and CBR are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may pause, rename, redirect, narrow, or stop the route at any time.

`PREPARED_BY_TAMAR_VEY = true`

`SENT_BY_TAMAR_VEY = false`
""",
    )
    dump(
        orchestration / "terminal-route-hold.json",
        {
            "state": "PREPARED_NOT_SENT",
            "provisional_exact_title": "Elowen Cairn",
            "provisional_phase": "v676-v6",
            "newest_live_authority_required_at_send": True,
            "precontact_performed": False,
            "send_count": 0,
            "continuation_authority_terminal_label": "v725-v8",
            "terminal_prerequisites": [
                "exact final committed and pushed",
                "clean 0/0 divergence and fresh four-way equality",
                "one successful non-replayed owner-scoped canonical invocation",
                "newest live authority and structurally valid roster",
                "one unique exact-title registry match and immediate reread",
                "duplicate, pause, redirect, rename, standby, usage, privacy, evidence, safety, legal, cultural, affected-party, and Māori-authority guards",
                "one acknowledged send only",
            ],
        },
    )
    dump(
        base / "validation" / "final-validation-candidate.json",
        {
            "status": "PRECOMMIT_EXACT_FINAL_VALIDATION_CANDIDATE",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "expected_branch": BRANCH,
            "expected_phase_commits": 3,
            "expected_merges": 0,
            "expected_final_parents": 1,
            "canonical_invocation_limit": 1,
            "canonical_success_replay_forbidden": True,
            "full_repository_suite": False,
            "test_selections": {
                "x1": "immutable x1 owner tree",
                "evidence": "immutable evidence owner tree",
                "final": "exact-final owner test",
            },
        },
    )


if __name__ == "__main__":
    main()
