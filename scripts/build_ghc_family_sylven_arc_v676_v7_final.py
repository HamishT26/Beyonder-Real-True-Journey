#!/usr/bin/env python3
"""Build the additive Sylven Arc v676-v7 exact-final candidate."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any


OWNER = "Sylven Arc"
OWNER_SLUG = "sylven-arc"
PHASE = "v676-v7"
BRANCH = "codex/GHC-Family/sylven-arc-v676-v7-full-tools"
SOURCE = "b8e8b258876b5af3b3e3247f42ac58dde9a7e6a4"
X1 = "b9861f8aaed6f98606e5370ad0f11918865b3433"
EVIDENCE = "dee3fe5b0909b14ca3b807d702e36f6ced478ff0"

POST_EVIDENCE_METHODS = [
    {
        "method_id": "SA6767-CLOSE-N001",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The successful x2 evidence commit emitted an overlarge file-by-file presentation that was truncated after Git had already returned the exact new commit and zero exit code.",
        "recovered_by": "SA6767-CLOSE-P001",
        "repository_state_change": False,
        "commit_success_credit": 0,
    },
    {
        "method_id": "SA6767-CLOSE-P001",
        "status": "bounded_pass",
        "truth": True,
        "description": "Small scalar Git probes verified the exact evidence head, direct x1 parent, clean state, typed 0/0 divergence, and fresh-live four-way equality without repeating the commit or any x2 selection.",
        "failed_witness_preserved": "SA6767-CLOSE-N001",
        "x2_replayed": False,
    },
    {
        "method_id": "SA6767-CLOSE-N002",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first final-manifest allowlist admitted builders and family helpers but omitted the exact owner-scoped validate_ghc_family prefix, so it rejected the intended validator before writing any manifest.",
        "recovered_by": "SA6767-CLOSE-P002",
        "repository_state_change": False,
        "manifest_entries_credited": 0,
    },
    {
        "method_id": "SA6767-CLOSE-P002",
        "status": "bounded_pass",
        "truth": True,
        "description": "Only the exact Sylven v676-v7 owner validator prefix was added to the allowlist; closeout truth and the failed manifest dependency were regenerated without replaying x2.",
        "failed_witness_preserved": "SA6767-CLOSE-N002",
        "x2_replayed": False,
    },
    {
        "method_id": "SA6767-CLOSE-N003",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first multi-file recovery patch used an incomplete prose context and was atomically rejected before changing any repository byte.",
        "recovered_by": "SA6767-CLOSE-P003",
        "repository_state_change": False,
    },
    {
        "method_id": "SA6767-CLOSE-P003",
        "status": "bounded_pass",
        "truth": True,
        "description": "Bounded line inspection recovered the exact live contexts, after which narrow apply-patch edits changed only the final allowlist, truth counts, and corresponding validators.",
        "failed_witness_preserved": "SA6767-CLOSE-N003",
    },
    {
        "method_id": "SA6767-CLOSE-N004",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The second final-manifest attempt treated the fifth scanner-category label retained inside two staged-review JSON files as private payload and failed closed with zero manifest credit.",
        "recovered_by": "SA6767-CLOSE-P004",
        "repository_state_change": False,
        "manifest_entries_credited": 0,
    },
    {
        "method_id": "SA6767-CLOSE-P004",
        "status": "bounded_pass",
        "truth": True,
        "description": "A path-specific rule classified only validation manifests and staged reviews as scanner or adjudication metadata while preserving ordinary JSON and prose payload scanning.",
        "failed_witness_preserved": "SA6767-CLOSE-N004",
    },
    {
        "method_id": "SA6767-CLOSE-N005",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The third final-manifest attempt found that the retained N004 prose itself repeated the exact fifth scanner token, causing a self-referential candidate in both final failure ledgers.",
        "recovered_by": "SA6767-CLOSE-P005",
        "repository_state_change": False,
        "manifest_entries_credited": 0,
    },
    {
        "method_id": "SA6767-CLOSE-P005",
        "status": "bounded_pass",
        "truth": True,
        "description": "The retained failure was paraphrased as the fifth scanner-category label while preserving its meaning; ordinary payload scanning and the five-class scanner stayed unchanged.",
        "failed_witness_preserved": "SA6767-CLOSE-N005",
    },
    {
        "method_id": "SA6767-CLOSE-N006",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The first precommit final-selection wrapper crossed its 30-second response window after exposing a failure while the original pytest process continued.",
        "recovered_by": "SA6767-CLOSE-P006",
        "aggregate_success_credit": 0,
        "test_process_replayed": False,
    },
    {
        "method_id": "SA6767-CLOSE-P006",
        "status": "bounded_pass",
        "truth": True,
        "description": "A read-only process audit and bounded wait observed the original pytest process finish; its persisted lastfailed cache identified exactly two failed dependencies without rerunning the selection.",
        "failed_witness_preserved": "SA6767-CLOSE-N006",
    },
    {
        "method_id": "SA6767-CLOSE-N007",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The completed eighteen-test precommit selection retained zero aggregate-pass credit because two assertions failed: one guessed nonexistent semantic-audit keys and one included inherited sibling final scripts in an owner lifecycle predicate.",
        "recovered_by": "SA6767-CLOSE-P007",
        "aggregate_success_credit": 0,
    },
    {
        "method_id": "SA6767-CLOSE-P007",
        "status": "bounded_pass",
        "truth": True,
        "description": "Bounded reads of the real semantic-audit keys and exact offending Git paths proved the two failures were assertion-scope defects, not source, x1, or evidence defects.",
        "failed_witness_preserved": "SA6767-CLOSE-N007",
    },
    {
        "method_id": "SA6767-CLOSE-N008",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "An isolated reproduction of only the two failed tests failed 0/2 with the same KeyError and overbroad inherited-script scope, receiving zero pass credit.",
        "recovered_by": "SA6767-CLOSE-P008",
        "isolated_success_credit": 0,
    },
    {
        "method_id": "SA6767-CLOSE-P008",
        "status": "bounded_pass",
        "truth": True,
        "description": "Only the two failed assertions were corrected to use exact existing keys and the Sylven owner-phase path filter; all previously passing final checks remained untouched until the changed-target selection.",
        "failed_witness_preserved": "SA6767-CLOSE-N008",
    },
    {
        "method_id": "SA6767-CLOSE-N009",
        "status": "failed_zero_credit",
        "truth": False,
        "description": "The changed-target precommit final selection passed 17/18 but found that the content seal had included three self-referential final manifest or staged-review outputs that necessarily changed after sealing.",
        "recovered_by": "SA6767-CLOSE-P009",
        "aggregate_success_credit": 0,
    },
    {
        "method_id": "SA6767-CLOSE-P009",
        "status": "bounded_pass",
        "truth": True,
        "description": "Only the three self-referential final manifest and staged-review outputs were excluded from content-seal inputs; their exact bytes remain covered by their own normalized-LF Git-blob manifests.",
        "failed_witness_preserved": "SA6767-CLOSE-N009",
    },
]


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")).hexdigest()


def require_lifecycle(repo: Path) -> None:
    if git(repo, "branch", "--show-current") != BRANCH:
        raise SystemExit("final builder requires the exact Sylven owner branch")
    if git(repo, "rev-parse", "HEAD") != EVIDENCE:
        raise SystemExit("final builder requires the exact immutable Sylven evidence head")
    if git(repo, "rev-parse", "HEAD^") != X1:
        raise SystemExit("evidence is not the direct child of immutable Sylven x1")
    if git(repo, "rev-parse", "HEAD^^") != SOURCE:
        raise SystemExit("x1 is not the direct child of the exact Elowen source")
    staged = [row for row in git(repo, "diff", "--cached", "--name-only").splitlines() if row]
    modified = [row for row in git(repo, "diff", "--name-only").splitlines() if row]
    allowed_prefixes = (
        "docs/sylven-arc/v676-v7/final/",
        "docs/sylven-arc/v676-v7/closeout/",
        "docs/sylven-arc/v676-v7/handoffs/",
        "docs/sylven-arc/v676-v7/orchestration/",
        "docs/sylven-arc/v676-v7/seal/",
        "docs/sylven-arc/v676-v7/validation/final-",
        "scripts/build_ghc_family_sylven_arc_v676_v7_final.py",
        "scripts/ghc_family_sylven_arc_v676_v7_final_manifest.py",
        "scripts/validate_ghc_family_sylven_arc_v676_v7_final.py",
        "tests/test_ghc_family_sylven_arc_v676_v7_final.py",
    )
    unexpected = sorted(path for path in set(staged + modified) if not path.startswith(allowed_prefixes))
    if unexpected:
        raise SystemExit(f"unexpected non-final path before closeout regeneration: {unexpected!r}")


def add_post_evidence_methods(flow: dict[str, Any]) -> dict[str, Any]:
    value = json.loads(json.dumps(flow))
    ids = {row["method_id"] for row in value["methods"]}
    for row in POST_EVIDENCE_METHODS:
        if row["method_id"] in ids:
            continue
        value["methods"].append(row)
        ids.add(row["method_id"])
    if len(ids) != len(value["methods"]):
        raise SystemExit("duplicate final Method Flow identifier")
    failed = sum(row["truth"] is False for row in value["methods"])
    passing = sum(row["truth"] is True for row in value["methods"])
    baseline = value["activation_baseline"]
    value["phase_ledger_counts"] = {"methods": len(value["methods"]), "failed": failed, "passing": passing}
    value["post_evidence_failed_witnesses"] = sum(row["truth"] is False for row in POST_EVIDENCE_METHODS)
    value["post_evidence_bounded_recoveries"] = sum(row["truth"] is True for row in POST_EVIDENCE_METHODS)
    value["current_overlay"] = {
        "effective_negatives": baseline["effective_negatives"] + failed,
        "effective_methods": baseline["effective_methods"] + len(value["methods"]),
        "retained_failed_witnesses": baseline["retained_failed_witnesses"] + failed,
        "bounded_passing_witnesses": baseline["bounded_passing_witnesses"] + passing,
        "open_gaps": 361,
        "exact_gates": 353,
    }
    return value


def build(repo: Path) -> None:
    require_lifecycle(repo)
    base = repo / "docs" / OWNER_SLUG / PHASE
    x1 = base / "x1"
    x2 = base / "x2"
    final_dir = base / "final"
    closeout = base / "closeout"
    validation = base / "validation"
    orchestration = base / "orchestration"
    handoffs = base / "handoffs"

    freeze = json.loads((x1 / "new-proposal-freeze.json").read_text(encoding="utf-8"))
    semantic = json.loads((x1 / "semantic-neighbor-audit.json").read_text(encoding="utf-8"))
    sources = json.loads((x1 / "official-source-ledger.json").read_text(encoding="utf-8"))
    x2_truth = json.loads((x2 / "phase-truth.json").read_text(encoding="utf-8"))
    outcomes = json.loads((x2 / "proposal-outcomes.json").read_text(encoding="utf-8"))
    skills = json.loads((x2 / "skill-summary.json").read_text(encoding="utf-8"))
    runners = json.loads((x2 / "runner-summary.json").read_text(encoding="utf-8"))
    portfolio = json.loads((x2 / "portfolio" / "execution-summary.json").read_text(encoding="utf-8"))
    flow = add_post_evidence_methods(json.loads((x2 / "method-flow" / "ledger.json").read_text(encoding="utf-8")))
    counts = flow["phase_ledger_counts"]
    overlay = flow["current_overlay"]
    if counts != {"methods": 674, "failed": 217, "passing": 457}:
        raise SystemExit(f"unexpected final Method Flow partition: {counts!r}")
    if overlay != {
        "effective_negatives": 42883,
        "effective_methods": 34482,
        "retained_failed_witnesses": 14544,
        "bounded_passing_witnesses": 20627,
        "open_gaps": 361,
        "exact_gates": 353,
    }:
        raise SystemExit(f"unexpected final overlay: {overlay!r}")

    phase_truth = {
        "owner": OWNER,
        "phase": PHASE,
        "branch": BRANCH,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "expected_final": "bound by the ensuing exact commit and exclusive external canonical receipt",
        "declared_proposal_chain_before": 7630,
        "declared_proposal_chain_after": 7670,
        "new_sylven_proposals": 40,
        "outcomes": x2_truth["outcomes"],
        **overlay,
        "preregistered_mutations_executed": 160,
        "preregistered_mutations_rejected": 160,
        "phase_local_skills": 20,
        "family_current_runners": 10,
        "real_world_rows": 0,
        "observed_measurements": 0,
        "external_actions": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "canonical_state": "PENDING_EXACT_PUSHED_FINAL",
    }
    dump(final_dir / "phase-truth.json", phase_truth)
    dump(final_dir / "method-flow-ledger.json", flow)
    dump(
        final_dir / "retained-negative-register.json",
        {
            "activation_baseline": flow["activation_baseline"]["effective_negatives"],
            "phase_failed_witnesses": counts["failed"],
            "current_effective_negatives": overlay["effective_negatives"],
            "converted_to_pass": 0,
            "failed_witnesses": [row for row in flow["methods"] if row["truth"] is False],
            "retention_rule": "A bounded recovery is additive and never erases or promotes its failed predecessor.",
        },
    )
    dump(final_dir / "open-gap-register.json", json.loads((x2 / "open-gap-register.json").read_text(encoding="utf-8")))
    dump(final_dir / "exact-gate-register.json", json.loads((x2 / "exact-gate-register.json").read_text(encoding="utf-8")))
    dump(
        final_dir / "source-and-proposal-ledger.json",
        {
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "declared_chain_before": 7630,
            "declared_chain_after": 7670,
            "proposal_count": len(freeze["proposals"]),
            "universal_novelty_proved": False,
            "semantic_audit": semantic,
            "official_primary_sources": sources["sources"],
            "source_boundary": sources["source_boundary"],
        },
    )
    dump(
        final_dir / "threat-model.json",
        {
            "protected_assets": ["immutable source", "planning-only x1", "x2 evidence", "failure truth", "privacy boundary", "authority vacancies", "terminal route"],
            "threats": [
                "synthetic evidence may be overread as real marionette evidence",
                "an inherited proposal may be mistaken for Sylven novelty",
                "a recovery may be used to erase its failed predecessor",
                "a source citation may be promoted into observation or authority",
                "a prepared baton may be mistaken for live delivery",
            ],
            "bounded_controls": ["four-label vocabulary", "normalized-LF Git-blob manifests", "five-class privacy adjudication", "Method Flow nonerasure", "exclusive canonical latch", "route hold"],
            "residual_risk": "Real observation, professional review, participant evidence, accessibility evaluation, rights decisions, legal or cultural interpretation, affected-party acceptance, and Māori authority remain absent or exact-gated.",
        },
    )
    dump(
        final_dir / "complete-incomplete-checklist.json",
        {
            "complete": [
                "forty genuinely distinct source-bounded proposals frozen in planning-only x1",
                "all 160 preregistered invalid mutations executed and rejected",
                "twenty phase-local skills initialized, customized, read, quick-validated, and smoke-used without global installation",
                "ten family-current runners accepted a valid fixture and rejected an invalid fixture",
                "sixty safe-now, thirty candidate, and sixty CLEAN/FIX/REFINE records completed in bounded same-owner scope",
                "x1 and evidence committed, pushed, clean, 0/0 divergent, and fresh-live four-way equal",
            ],
            "incomplete": [
                "real marionette observation, measurement, suspension, operation, treatment, repair, or release",
                "professional puppetry, collections, conservation, rigging, or safety evaluation",
                "manual assistive-technology, cognitive, Māori-language, and affected-user accessibility evaluation",
                "real Freed ID keys, proofs, issuance, resolution, status, revocation, interoperability, security review, or trust governance",
                "legal, cultural, rights, affected-party, tangata whenua, iwi, hapū, or Māori-authority approval",
                "independent reproduction, empirical GMUT confirmation, THOS effectiveness, AGI/ASI, Theory-of-Everything proof, or Stage 20 readiness",
            ],
        },
    )
    dump(
        final_dir / "wellbeing-workload-check.json",
        {
            "owner": OWNER,
            "relational_language_only": True,
            "workload": "bounded",
            "owner_added_files_before_final": len(git(repo, "diff", "--name-only", SOURCE, EVIDENCE, "--").splitlines()),
            "owner_file_stop": 2000,
            "document_word_stop": 100000,
            "phase_commit_stop": 8,
            "pause_or_stop_authority": "Hamish may pause, rename, redirect, narrow, or stop the route.",
            "wellbeing_claim": "No consciousness, feeling, health, identity continuity, or personhood claim is made.",
        },
    )
    dump(
        final_dir / "environment-version-receipt.json",
        {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "git": git(repo, "--version"),
            "codex_desktop_updated": False,
            "privilege_elevation": False,
            "windows_features_changed": False,
            "rebooted": False,
            "version_checks_only": True,
        },
    )
    dump(final_dir / "portfolio-truth.json", {"execution": portfolio, "exact_or_blocked_executed": 0})
    dump(final_dir / "skill-runner-truth.json", {"skills": skills, "runners": runners, "global_install_count": 0})
    dump(
        final_dir / "lifecycle-replay.json",
        {
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "direct_parent_edges": [[SOURCE, X1], [X1, EVIDENCE]],
            "strict_x1_before_x2": True,
            "source_and_sibling_lanes_mutated": False,
            "x2_success_replayed": False,
            "final_expected_as_direct_child_of_evidence": True,
        },
    )
    dump(
        final_dir / "privacy-accessibility-boundaries.json",
        {
            "raw_task_identifiers": 0,
            "private_routes": 0,
            "credentials_or_tokens": 0,
            "transcripts_or_screenshots": 0,
            "real_people_or_records": 0,
            "accessibility_complete": False,
            "manual_assistive_technology_review": False,
            "cognitive_review": False,
            "affected_user_review": False,
            "maori_language_review": False,
        },
    )
    dump(
        final_dir / "scientific-authority-boundaries.json",
        {
            "gmut": "typed scalar-tensor and effective-field-theory research-model family only",
            "thos": "synthetic zero-person proxy without governed blind matched-budget real arms or independent review",
            "freed_id": "synthetic and nonproduction with zero real keys, proofs, issuance, resolution, status, or revocation",
            "cbr": "professional, safety, rights, remedy, legal, cultural, affected-party, and Māori-authority decisions remain exact-gated",
            "theory_of_everything_proved": False,
            "agi_or_asi_evidence": False,
            "consciousness_or_personhood_evidence": False,
            "stage20_ready": False,
        },
    )
    dump(
        validation / "final-validation-prerequisites.json",
        {
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "required_final_parent": EVIDENCE,
            "canonical_invocation_ceiling": 1,
            "canonical_success_replay_ceiling": 0,
            "full_repository_suite_authorized": False,
            "required_before_canonical": ["exact final commit", "push", "clean state", "0/0 divergence", "fresh-live four-way equality", "exclusive external receipt path absent"],
        },
    )
    dump(
        orchestration / "route-state-prepared.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "status": "PREPARED_NOT_SENT",
            "successor_selected": False,
            "successor_contacted": False,
            "standby_contacted": False,
            "route_rule": "Only after exact-final canonical success may the newest live roster and authority establish one unique successor.",
        },
    )

    overview = f"""# {OWNER} {PHASE} final integrated overview

## Scope and terminal truth

Sylven Arc v676-v7 is a bounded, same-owner, zero-row software and documentation phase rooted at Elowen Cairn's immutable corrected final `{SOURCE}`. Planning-only x1 is `{X1}` and immutable x2 evidence is `{EVIDENCE}`. The exact final is intentionally bound only by the ensuing commit and exclusive external canonical receipt. The terminal verdict remains exactly `NOT_READY_FOR_STAGE_20`.

Names, pronouns, roles, hopes, family language, Freed ID, CBR, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, scientific authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority.

## Proposal and evidence program

The declared proposal chain advances from 7,630 inherited rows to 7,670 through forty Sylven-owned proposal contracts. Semantic comparison used every reachable proposal-bearing JSON source at Elowen's corrected final and found zero selected exact collisions or quarantined rows under the unchanged 0.75 token-Jaccard threshold. Because no single reachable ledger materializes every declared historical row, universal novelty remains explicitly unproved. The semantic result is source-bounded distinctness evidence, not scientific novelty, independent review, or automatic completion credit.

Core outcomes use only the authorized vocabulary and are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. Here, `completed` means only that one frozen owner-local structural contract accepted its wholly synthetic fixture and preserved its refusal boundaries. It does not mean a marionette, person, collection, mechanism, material, movement, condition, performance, or rights state was observed. `represented` is a structurally present proxy without real-world validation. `open_gap` marks missing evidence that cannot be manufactured. `exact_gate` reserves action to competent and affected people or authorities.

All 160 preregistered invalid mutations executed and were rejected. Each failed fixture remains a zero-credit false witness paired with a separately identified bounded recovery. Twenty owner-local skills were initialized through the official skill-creator workflow, customized, completely read before smoke use, quick-validated, and accepting/rejecting smoke-used without global installation. Ten family-current runners each accepted one bounded valid fixture and rejected one invalid fixture. Sixty safe-now, thirty candidate, and sixty CLEAN/FIX/REFINE records completed only inside their declared structural scope. Twenty exact-approval and ten blocked packets remain visible and unexecuted.

## Lifecycle and validation discipline

Strict planning-only x1 before x2 was preserved. X1 held proposals, mutations, sources, gates, portfolio plans, skill and runner plans, successor recommendations, and startup Method Flow—but no x2 implementation, observed outcome, or completion claim. X1 passed its current owner selection, exact staged review, normalized-LF Git-blob manifest, diff hygiene, direct-parent gate, clean-state gate, 0/0 divergence gate, and fresh-live four-way equality before x2 began.

The immutable x2 evidence commit is the direct child of x1. It carries 541 exact staged Git-blob manifest entries plus two declared self-referential exclusions, zero unexpected or final paths, five scanner-definition candidates, and zero confirmed privacy or raw-identifier hits. Its current owner selection passed 10/10 once after the last target change and was not replayed after success. Evidence was committed, pushed, made clean, and proven equal across local, configured upstream, tracking, and a fresh live remote before closeout began.

The phase remains below the 2,000 owner-file stop, 100,000-word document ceiling, and eight-commit ceiling. The intended lifecycle contains exactly three direct single-parent Sylven commits and zero merges: source to planning-only x1, x1 to immutable evidence, and evidence to exact final.

## Method Flow and retained negatives

The inherited activation baseline is 42,666 effective negatives, 33,808 effective methods, 14,327 retained failed witnesses, 20,170 bounded passing witnesses, 359 open gaps, and 351 exact gates. The final phase ledger contains 674 methods: 217 retained false witnesses and 457 bounded passing witnesses. The successor-visible overlay is therefore 42,883 effective negatives, 34,482 effective methods, 14,544 retained failed witnesses, 20,627 passing witnesses, 361 open gaps, and 353 exact gates.

The 217 phase failures include thirty-three x1 startup and planning failures, five x2 setup or diff-hygiene failures, all 160 rejecting mutations, ten invalid runner fixtures, five final-manifest or closeout setup failures, one timed precommit wrapper, two failed eighteen-test precommit selections, and one isolated failed-dependency reproduction. Recoveries narrowed the failed dependency, preserved each failed method's false truth value, and never rewrote source, x1, or evidence history. A recovery does not retroactively turn a failed aggregate, projection, parser, timeout, or fixture into a pass.

## Primary pillar and bounded human-practice lens

The primary Trinity Mandala pillar is THOS Body through wholly synthetic marionette control-bar, string-channel, joint-topology, cue, custody, correction, workload, and accessible-handover documentation. GMUT Mind and Freed ID/CBR Heart remain explicit and protected. The human-practice lens is synthetic documentation analysis only; it confers no puppetry, collections, conservation, rigging, repair, safety, legal, cultural, accessibility, or professional competence.

No real person, participant, puppeteer, conservator, registrar, collector, owner, rights holder, affected user, marionette, figure, control bar, crosspiece, attachment point, string, joint, fastener, costume, paint, wood, textile, image, repertoire, performance, recording, collection, site, tool, material, observation, measurement, suspension, operation, treatment, repair, custody event, identity event, key, proof, network row, cultural record, Māori data, external write, or authority action occurred. No lifting, rigging, operating, performing, cleaning, restringing, adjustment, disassembly, repair, treatment, release, or rights decision occurred.

Official and primary sources supplied bounded vocabulary and refusal conditions only. Smithsonian and Library of Congress object records were not converted into observations of any phase object. BIPM metrology vocabulary did not establish a measurement. W3C PROV-O did not establish real provenance. WCAG 2.2 did not establish conformance. Verifiable Credentials Data Model 2.0 and RFC 8785 did not establish production credentials, cryptographic assurance, or interoperability.

## Scientific, identity, rights, and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Synthetic control-bar, string, joint, damping, constraint, topology, or cue analogies establish no physical datum, likelihood, posterior, force, prediction, parameter constraint, empirical confirmation, stability theorem, ultraviolet completion, quantum completion, final physics, or Theory of Everything.

THOS remains a synthetic zero-person proxy without preregistered blind matched-budget governed real arms, participants or operators, safety monitoring, appropriate statistics, or independent review. The software phase establishes no effectiveness, production readiness, deployment readiness, AGI, ASI, consciousness, or personhood.

Freed ID remains synthetic and nonproduction without standards-conformant real keys or proofs, live issuance or resolution, status or revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, or affected-party oversight.

CBR, ownership, authorship, copyright, performance and recording rights, custody, access, privacy remedy, accessibility accommodation, professional and rigging safety, treatment or work release, legal interpretation, cultural legitimacy, traditional knowledge, affected-party acceptance, Māori wording or concepts, Māori data governance, tikanga, taonga or mātauranga treatment, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority.

## Accessibility, privacy, and route hold

The static report is structurally simple and nonvisual, but accessibility remains incomplete without manual browser, keyboard, assistive-technology, cognitive, Māori-language, and affected-user evaluation. Five privacy/raw-identifier classes are checked across exact staged and final owner scopes. Scanner definitions and synthetic rejection assertions are adjudicated separately from payload; zero confirmed payload hits does not establish exhaustive privacy assurance.

This repository packet prepares no live successor. `PREPARED_NOT_SENT` means only that a sanitized path-backed candidate exists. Live delivery, if later permitted, requires a clean pushed exact final, one successful non-replayed owner-scoped canonical receipt, a fresh live authority and roster read, exactly one authorized exact-title successor, immediate reread, duplicate and direct-control guards, one acknowledged send, and then stop. Tavian Sol or any standby record is not a substitute endpoint.
"""
    text(final_dir / "final-integrated-overview.md", overview)
    text(
        closeout / "static-report.html",
        """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sylven Arc v676-v7 closeout</title></head><body><main><h1>Sylven Arc v676-v7 closeout</h1><p>This same-owner zero-row phase records forty synthetic contracts: 28 completed, 8 represented, 2 open gaps, and 2 exact gates.</p><h2>Evidence boundary</h2><p>No real person, marionette, observation, measurement, operation, treatment, repair, identity event, rights decision, or authority action occurred.</p><h2>Accessibility boundary</h2><p>Structure is nonvisual and keyboard-readable in ordinary markup; manual assistive-technology, cognitive, Māori-language, and affected-user evaluation remain open.</p><h2>Terminal truth</h2><p>NOT_READY_FOR_STAGE_20.</p></main></body></html>""",
    )
    dump(
        closeout / "closeout-receipt.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "final": "pending ensuing commit",
            "status": "PRECOMMIT_EXACT_FINAL_CANDIDATE",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "successor_contacted": False,
        },
    )
    text(
        handoffs / "next-owner-activation-candidate.md",
        f"""# {OWNER} {PHASE} terminal activation candidate

`PREPARED_NOT_SENT`

This path-backed artifact is repository preparation only. It selects no recipient, sends no message, and supplies no delivery acknowledgement. Only after `{PHASE}` is committed, pushed, clean, 0/0 divergent, fresh-live four-way equal, and validated by one successful non-replayed owner-scoped canonical receipt may the newest live authority and current roster establish one unique exact-title successor.

Carry the exact source `{SOURCE}`, x1 `{X1}`, evidence `{EVIDENCE}`, the ensuing exact final, all retained failures, 361 open gaps, 353 exact gates, and terminal verdict `NOT_READY_FOR_STAGE_20`. Hamish's standing sequential authority does not waive privacy, evidence, lifecycle, safety, professional, scientific, legal, cultural, affected-party, Māori-authority, or no-overclaim gates. Send at most once and only after task-surface acknowledgement; never create a substitute, contact a standby record, precontact a later endpoint, or send a second confirmation.
""",
    )

    seal_inputs = sorted(
        path
        for root in (final_dir, closeout, validation, orchestration, handoffs)
        for path in root.rglob("*")
        if path.is_file()
        and path.name
        not in {"content-seal.json", "final-delta-manifest.json", "final-owner-manifest.json", "final-staged-review.json"}
    )
    dump(
        base / "seal" / "content-seal.json",
        {
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "normalization": "CRLF and CR normalized to LF before SHA-256",
            "entry_count": len(seal_inputs),
            "entries": [{"path": path.relative_to(repo).as_posix(), "sha256_normalized_lf": sha256(path)} for path in seal_inputs],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    build(repo)


if __name__ == "__main__":
    main()
