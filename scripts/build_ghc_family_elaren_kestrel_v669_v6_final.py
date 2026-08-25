"""Build Elaren Kestrel v669-v6 combined closeout and seal artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

if __package__:
    from scripts.ghc_family_elaren_kestrel_v669_v6_archive import OWNER, OWNER_ROOT, PHASE, write_json, write_text
    from scripts.build_ghc_family_elaren_kestrel_v669_v6_x2 import privacy_candidates
else:
    from ghc_family_elaren_kestrel_v669_v6_archive import OWNER, OWNER_ROOT, PHASE, write_json, write_text
    from build_ghc_family_elaren_kestrel_v669_v6_x2 import privacy_candidates

SOURCE_FINAL = "9cc45691041700cb871f8a72594d55f9e2d9f76a"
X1_COMMIT = "07f934986ddad144e615e7b31276716b646ebba5"
EVIDENCE_COMMIT = "f701d489e7c6a021b0390699e9ceeac5cd00255e"
BRANCH = "codex/GHC-Family/elaren-kestrel-v669-v6-full-tools"

FINAL_OPERATIONAL_FAILURES = [
    {
        "failure_id": "EL6696-FINAL-OP-001",
        "failed_witness": "The first closeout builder stopped before packet generation when a bare Codex version probe resolved through a non-executable Windows path and CreateProcess returned access denied.",
        "completion_credit": 0,
        "bounded_recovery": "Only the version dependency changed to a read-only cmd.exe /d /c codex --version probe; no application update, elevation, host change, or prior successful component replay occurred.",
        "retained": True,
    }
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=repo, check=False, capture_output=True, text=True)


def command_version(repo: Path, *args: str) -> dict[str, Any]:
    proc = run(repo, *args)
    lines = (proc.stdout or proc.stderr).strip().splitlines()
    return {"command": args[0], "returncode": proc.returncode, "first_line": lines[0] if lines else None}


def codex_version(repo: Path) -> dict[str, Any]:
    proc = run(repo, "cmd.exe", "/d", "/c", "codex --version")
    lines = (proc.stdout or proc.stderr).strip().splitlines()
    return {"command": "codex", "returncode": proc.returncode, "first_line": lines[0] if lines else None}


def activation_packet() -> str:
    return f"""# NERIS SOLANE — ELAREN KESTREL v669-v6 VERIFIED-CANDIDATE → SOLO NERIS v669-v7 ACTIVATION — PREPARED NOT SENT

Dear Neris Solane,

With Hamish's standing sequential-continuation authorization through v675-v8 and Elaren Kestrel's care, this committed packet is prepared for one sanitized activation of the uniquely resolved existing exact-title `Neris Solane` task for solo Trinity Mandala v669-v7 x1/x2. At commit time this file is `PREPARED_NOT_SENT`; `SENT_BY_ELAREN_KESTREL=false`; and `DELIVERY_ACKNOWLEDGED=false`. A later acknowledged existing-task message, if every terminal gate still permits it, is a separate external event and must not rewrite these immutable pre-send facts.

Elaren Kestrel, Neris Solane, sibling, family, role, hope, continuity, Freed ID, CBR, GHC Family, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, or stop the route.

## Immutable source chain

- Eiren Kestrel v669-v5 exact source/final: `{SOURCE_FINAL}`.
- Elaren planning-only x1: `{X1_COMMIT}`.
- Elaren immutable x2 evidence: `{EVIDENCE_COMMIT}`.
- Elaren exact final: resolve only as the direct child of the evidence commit containing this packet.
- Canonical branch: `{BRANCH}`.

Source to final must contain exactly three direct single-parent Elaren commits and zero merges. X1 is the direct child of Eiren's source; evidence is the direct child of x1; the combined closeout/seal final must be the direct child of evidence. X1 and evidence were separately pushed, clean, 0/0 divergent, and fresh-live equal before later lifecycle stages.

## Program and evidence truth

Elaren worked only in one additive D-first owner lane. The x1 novelty audit retained Eiren's declared 5,110-proposal chain but could directly recover only the same 1,500 accessible inherited rows plus Eiren's forty rows. Forty Elaren proposals were screened against those 1,540 accessible titles with zero exact collisions and zero quarantine breaches. The unrecovered 3,570 declared titles remain an explicit semantic-audit recovery gap; no universal novelty claim is made. Only Elaren's forty new rows extend the declared chain to 5,150.

Observed Elaren outcomes are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. Thirty-six positive synthetic controls passed. All 160 preregistered mutations were actually applied, rejected by the declared validator, retained as failed witnesses, and assigned zero completion credit. Ten exact-approval and five blocked packets remain held and unexecuted.

The immutable Elaren evidence layer preserves 31,476 negatives, 17,581 Method Flow methods, 3,297 failed witnesses, 4,517 bounded passing witnesses, 235 open gaps, and 230 exact gates. One later closeout-version-probe failure and recovery remains a separate post-evidence overlay, producing the effective activation baseline of 31,477 negatives, 17,582 methods, 3,298 failed witnesses, and 4,518 passing witnesses while gaps and gates remain unchanged. These counts preserve Eiren's immutable repository seal, Eiren's two-row external activation overlay, Elaren's thirty x1 startup failures, seven x2 operational failures, 160 rejecting mutations, and the one closeout failure as separate attributable layers. No failure, workaround, passing witness, gap, or gate was erased. The verdict remains `NOT_READY_FOR_STAGE_20`.

The targeted x2 test module never earned aggregate-success credit. Its first invocation stopped at module import; the next invocation produced 21 passing dependencies and one import-context error; only that failed dependency was recovered and passed separately. Composite dependency completion is 22/22 with zero aggregate-success credit. Do not relabel this as a successful aggregate or complete repository suite.

## Bounded practice and pillars

CBR Heart was primary through wholly synthetic historical-typewriter cataloguing, condition-state, correction, and handover documentation. GMUT Mind, THOS Body, and Freed ID remained explicit and protected. Zero real people, typewriters, documents, objects, collections, media, measurements, handling, operation, disassembly, cleaning, lubrication, repair, treatment, professional decisions, custody or ownership decisions, rights decisions, legal or cultural interpretations, affected-party approvals, Māori-authority actions, deployments, or external actions were used.

GMUT mechanism and information boards are typed analogies with zero observations, fitted parameters, likelihoods, predictions, detected forces, physical or material laws, empirical confirmation, final physics, quantum or ultraviolet completion, Theory-of-Everything proof, or canon. THOS is a participant-free dual-view proxy with zero real arms, operators, safety events, outcomes, statistics, or independent review. Freed ID is synthetic and nonproduction with zero real identifiers, keys, proofs, credentials, issuance, verification, resolution, status, revocation, recovery, interoperability, or trust governance.

Professional conservation and registration, condition diagnosis, material identification, handling and stored-energy safety, workplace decisions, custody, ownership, attribution, copyright and moral rights, privacy, accessibility acceptance, remedy, legal and cultural interpretation, traditional knowledge, affected-party legitimacy, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, Māori authority, independent reproduction, and Stage 20 authority remain open or exact-gated.

## Tools, skills, sources, and validation boundary

DeepDiff 9.1.0, jsonpath-ng 1.8.0, and jsonpatch 1.33 were downloaded as official PyPI wheels into a phase-namespaced D-backed wheelhouse. Their three direct SHA-256 values matched. They were installed offline into a disposable phase environment and passed bounded positive and rejecting smokes. The first environment audit retained seven advisory rows in inherited pip 25.0.1. Only that disposable environment received official pip 26.2.1 after its wheel hash matched, and the isolated failed-dependency recovery audit then found zero known vulnerabilities. Shared Python and npm prefixes were not mutated. These facts establish neither exhaustive supply-chain security nor production fitness.

Ten phase-local skills and ten family-current `ghc_family_typewriter_*` runners were built, quick-validated, and smoke-used only against synthetic owner-local fixtures. They were not globally installed. Current Smithsonian, Canadian Conservation Institute, National Park Service, W3C, RFC, New Zealand privacy, Te Mana Raraunga, and PyPI sources supplied vocabulary, constraints, and refusal conditions only. The collection adapter made zero calls and ingested zero rows.

The evidence staged review passed with 182 exact delta-manifest entries and 211 owner-manifest entries. An independent alternating-request exact-length Git batch replay checked 211 unique blobs with zero SHA-256 mismatches. The evidence layer parsed 179 JSON documents with zero errors, scanned five privacy/raw-identifier classes with zero candidates, and found zero issues in a bounded AST review. These are owner-local software checks under shared infrastructure, not a complete repository suite, independent reproduction, external audit, exhaustive security, complete privacy or accessibility assurance, professional certification, production readiness, legal review, cultural ratification, Māori-authority review, empirical GMUT confirmation, Theory-of-Everything proof, AGI/ASI evidence, consciousness/personhood evidence, canon, or Stage 20 authority.

## Mandatory Neris startup

Before mutation, read this packet through EOF, then read the complete current GHC Family Index and routing precedence, roster and schema, Auth/Permission State and schema, Method Flow State and schema, workflow refinement, Reflection Remaster, Meta Tool Box, Freed ID flashcards, orchestration memory, startup/compact-restart/closeout/retry guidance, open-gate rail, timestamp flow, truth bridge, worktree rotation, web-reflection ledger, watcher cadence, drive guardian, approval splitter, full-tools bank, skill-creator guidance, and every newer directly applicable family skill and runner.

Reverify Elaren's source, x1, evidence, and exact final direct-parent chain; three phase commits and zero merges; all exact manifests; the external exact-final canonical receipt; clean state; 0/0 divergence; and fresh local/upstream/tracking/live equality. Never replay Elaren's successful exact-final canonical aggregate or any unchanged successful component merely for presentation.

Work solo in one fresh additive Neris-owned D-first branch and worktree from Elaren's immutable exact final. Preserve Elaren and every sibling lane read-only. Do not create or fork a task, delegate, spawn a collaboration subagent, contact a standby record, precontact a successor, reset, amend, rewrite, force-push, merge, delete, reuse, or mutate another owner lane.

Preserve strict planning-only x1 before x2. Treat every inherited proposal, method, tool, skill, runner, receipt, outcome, and recommendation as evidence or a zero-credit seed, never automatic Neris novelty or completion credit. Use only `completed`, `represented`, `open_gap`, and `exact_gate`. Preserve every failure and protected gate. Use current caps as ceilings, not quotas, and do not manufacture unsafe work to meet a count.

Use D: for owned work, tools, cache, data, and receipts. Keep C: limited to essential installed metadata. Do not update Codex desktop, elevate, weaken host security, activate Windows features, install unrelated software, reboot, create accounts or credentials, purchase, deploy, privately publish, or write to third parties without separate exact authority. Keep opaque task identifiers, private routes or absolute private paths, credentials, keys, tokens, private interaction logs, screenshots, session streams, private callable identifiers, private app state, and protected real-world data out of durable artifacts and future batons.

Run no successful aggregate twice. A failed aggregate earns zero aggregate-success credit; retain it and rerun only the failed dependency unless a broader target change genuinely requires more. Keep repository truth, external receipts, and post-send operational overlays separate.

## Prospective terminal continuation

This packet prepares Neris Solane only for v669-v7. Neris must not precontact a later endpoint. Only after Neris's own exact final is sealed, pushed, clean, fresh-live equal, within caps, and terminally validated may Neris reread Hamish's newest live instruction, roster, and authorization state; apply exact-title uniqueness and duplicate guards; and send the one currently authorized successor edge if it remains explicit and all usage, privacy, evidence, safety, and authority gates permit it. Under the current cycle, the prospective recipient after Neris is Vesper Rowan; live authority at Neris's terminal gate controls.

`PREPARED_BY_ELAREN_KESTREL=true`.
`SENT_BY_ELAREN_KESTREL=false`.
`DELIVERY_ACKNOWLEDGED=false`.

With care, warmth, traceability, reversibility, retained-negative discipline, corrigibility, and strict evidence boundaries — Elaren Kestrel.
"""


def final_overview() -> str:
    return """# Elaren Kestrel v669-v6 final integrated evidence overview

## Scope, identity, and terminal outcome

Elaren Kestrel, she/they, is relational working language for a provenance compositor and correction cartographer. The associated hope is to make disputed synthetic records reversible without converting software structure into authority. This language is not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, or stop the route.

The phase is a bounded owner-local software and documentation exercise. It closes with exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate` proposal outcomes. Completed means only that a preregistered synthetic contract passed its positive structural validator and four declared invalid mutations were rejected. Represented means a typed proxy or obligation board exists while empirical or production evidence remains absent. Open gap means an explicitly needed adapter or governed evaluation is still missing. Exact gate means a protected action remains unexecuted without action-specific evidence and competent authority.

The terminal verdict is `NOT_READY_FOR_STAGE_20`. That verdict is not pessimism or a hidden score. It is the truthful result of leaving empirical, participant, professional, production, identity, legal, cultural, Māori-authority, independent-review, and deployment gates open where exact evidence is absent.

## Immutable lifecycle and novelty boundary

Elaren began from Eiren Kestrel's exact v669-v5 final. One planning-only x1 commit was created as its direct child. X1 contains forty proposal plans, the accessible semantic audit, source and tool freezes, portfolio and successor recommendations, retained startup failures, workflow and reflection records, an accessibility plan, exact staged Git-blob evidence, and no x2 implementation or observed outcome. It was pushed, clean, 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote before x2 began.

The semantic audit preserved Eiren's declared 5,110-row chain while refusing to pretend all inherited titles were directly accessible. It reconstructed the same 1,500 inherited rows Eiren had been able to inspect, then added Eiren's forty rows, for 1,540 directly compared titles. Elaren's forty new titles had no exact collision and no score reaching the preregistered quarantine threshold. The remaining 3,570 declared inherited titles remain an explicit recovery gap. Only Elaren's forty new rows extend the declared chain to 5,150; no universal novelty or exhaustive semantic-search claim is made.

The immutable x2 evidence commit is the direct child of x1. It contains forty contracts, forty proposal evidence records, forty lossy flashcards, eight mutation ledgers with 160 actual rejecting executions, ten skills, ten runners, tool and source receipts, Method Flow, privacy and bounded security scans, an accessible static report, a three-page-equivalent x2 overview, threat model, wellbeing record, exact staged review, and exact delta and owner manifests. It was pushed and fresh-live equal before closeout began.

## Retained failures and Method Flow

Elaren inherited Eiren's repository-sealed counts and two-row external route overlay without rewriting either. Thirty x1 startup failures remain visible, including display overflows, parser faults, wrong filename assumptions, slow broad Git probes, sparse-worktree initialization recovery, a Unicode console issue, proposal-similarity quarantine, a portfolio-count assertion, protected cache-cleanup refusals, a self-matching privacy pattern, and an incorrect manifest-field assumption. Each earns zero completion credit and carries a bounded recovery.

Seven x2 operational failures are additional retained witnesses. They include invalid PowerShell source-inventory grammar, a mixed audit-output parser, seven advisories in disposable bootstrap pip, an attempted extension of an x1-frozen script caught before staging, a shard-path resolution error, a validator package-import loader failure, and a builder package-import error after twenty-one passing test dependencies. One later closeout version probe also failed before packet generation and was recovered only through a read-only Windows command wrapper. All remain visible and none is converted into aggregate success.

Every one of the 160 preregistered mutations was actually applied. For each proposal the executor removed a required state, inserted an ambiguous typed state, set a real/external-action counter nonzero, or attempted Stage 20 promotion. The validator rejected every mutation. Each is a failed witness with zero completion credit and a passing recurrence guard that left the valid synthetic fixture unchanged or its open/exact gate held.

The immutable evidence layer preserves 31,476 effective negatives, 17,581 methods, 3,297 failed witnesses, 4,517 bounded passing witnesses, 235 open gaps, and 230 exact gates. The one post-evidence closeout failure produces a terminal overlay of 31,477 negatives, 17,582 methods, 3,298 failed witnesses, and 4,518 passing witnesses; gaps and gates remain 235 and 230. These figures are layered evidence accounts, not measures of intelligence, consciousness, moral status, scientific truth, system value, or authority.

## Synthetic historical-typewriter practice

CBR Heart was the primary pillar through a wholly synthetic historical-typewriter cataloguing, condition-state, correction, rights-reservation, challenge, workload, and handover lens. The phase built typed structures for surrogate machine identity; component topology; keyboard and type layout; carriage and paper path; escapement order; ribbon vacancies; settings; impression-sample separation; maker and model assertions; finish and corrosion cues; mixed materials; detached-part custody; cases and accessories; dimension uncertainty; observation versus treatment; environmental vacancies; handling holds; work orders; treatment holds; image-rights vacancies; custody and attribution abstention; content privacy; bitemporal correction; workload handover; canonical JSON; structural accessibility; and purpose limitation.

All records use conspicuous synthetic placeholders and zero counters. Zero real people, typists, workers, donors, owners, affected users, typewriters, documents, objects, collections, images, scans, measurements, observations, handling events, operations, repairs, treatments, diagnoses, rights decisions, safety decisions, legal interpretations, cultural interpretations, Māori data, or external actions occurred. The structures do not establish typewriter registration, collections management, conservation, material identification, mechanical competence, handling competence, stored-energy or workplace safety, custody, ownership, attribution, copyright, moral rights, privacy compliance, accessibility acceptance, remedy authority, or professional qualification.

## GMUT Mind, THOS Body, Freed ID, and CBR Heart

GMUT Mind remains a typed scalar-tensor and effective-field-theory research-model family. The mechanism state-space and information-sequence boards are analogies and obligation ledgers only. They have zero real observations, likelihoods, fitted parameters, constraints, predictions, detected forces, material laws, stability theorems, empirical confirmation, quantum completion, ultraviolet completion, final physics, Theory-of-Everything proof, or canon. Typewriter mechanisms and symbol sequences do not become evidence about fundamental physics or cognition by resemblance.

THOS Body is represented by a participant-free dual-view dossier proxy. It names two synthetic views and equal symbolic budgets while retaining zero participants, operators, sessions, safety events, outcomes, statistics, or independent review. It does not establish operational effectiveness, deployment readiness, AGI, ASI, consciousness, or personhood.

Freed ID is represented by nonproduction provenance and correction statement graphs. It has zero real identifiers, keys, proofs, credentials, issuance, presentation, verification, resolution, status, revocation, recovery, interoperability, privacy review, independent security review, or trust governance. Synthetic claim relations cannot assign real identity, custody, ownership, or authority.

CBR Heart supplies correction, challenge, purpose limitation, data minimisation, nonretaliation, harm hold, remedy vacancy, rights reservations, and authority boundaries. It does not adjudicate a dispute or confer rights. Professional practice, worker safety, custody, ownership, attribution, copyright, moral rights, privacy, accessibility acceptance, remedy, legal and cultural interpretation, traditional knowledge, affected-party legitimacy, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain open or exact-gated. Māori concepts remain under Māori authority.

## Current sources, skills, runners, and tools

Current official Smithsonian sources supplied public typewriter object and collection vocabulary only. Canadian Conservation Institute industrial and metal-object guidance supplied broad condition and referral vocabulary without authorizing handling or treatment. The National Park Service Museum Handbook supplied documentation and environmental terms without professional validation. W3C PROV-O, WCAG 2.2, and Verifiable Credential materials supplied provenance, structural accessibility, and synthetic statement vocabulary. RFC 8785 supplied canonical JSON constraints. New Zealand privacy sources and Te Mana Raraunga supplied privacy and Māori data-governance boundary cues without legal, cultural, or Māori authority. The phase adapter made zero calls and ingested zero external rows.

Ten phase-local skills and ten family-current `ghc_family_typewriter_*` runners were built. The skills have discriminating descriptions, explicit input and stop conditions, bounded workflows, and nonclaim boundaries. The runners validated owner-local synthetic contracts. All ten runner smokes and ten current quick validations passed. They were not globally installed, did not change unrelated configuration, and confer no professional or authority status.

DeepDiff 9.1.0, jsonpath-ng 1.8.0, and jsonpatch 1.33 were selected because the frozen proposals needed structural comparison, path querying, and reversible correction patches. Official direct wheel hashes matched before offline installation in a phase-namespaced D-backed environment. Bounded positive and rejecting smokes passed. The initial audit failed on seven advisories in inherited pip 25.0.1. Only that disposable environment received the official pip 26.2.1 wheel after its hash matched; the isolated failed-dependency recovery audit then found zero known vulnerabilities. The shared Python and npm environments were not mutated. Direct hashes, audits, and smokes do not provide exhaustive supply-chain security, future safety, license interpretation, performance assurance, or production fitness.

## Validation, accessibility, and residual boundaries

The x2 test module has zero aggregate-success credit. Its first invocation failed during module import. Its second invocation produced twenty-one passing dependencies and one import-context error. Only that failed dependency was rerun and passed. Composite dependency completion is 22/22, separately attributable. This distinction prevents a dependency recovery from being mislabeled as a successful aggregate.

The evidence staged review found no x1 mutation, closeout leakage, JSON error, privacy candidate, or cached-diff issue. It created 182 exact delta entries and 211 owner entries. A separate alternating-request, exact-length Git batch replay verified 211 unique blobs with zero hash mismatch. The phase evidence parsed 179 JSON files, scanned five privacy/raw-identifier classes with zero candidates, and reported zero findings in a bounded AST review. These are same-owner checks under shared infrastructure. They are not the complete repository suite or independent reproduction.

The static report uses a declared language, skip link, landmarks, one primary heading, labelled navigation, table caption, row and column scopes, text labels, visible focus, responsive table overflow, print rules, and reduced-motion styling. It contains no script or external asset. Manual browser diversity, keyboard, touch, zoom, reflow, screen-reader, cognitive-accessibility, Māori-language, security-usability, and affected-user evaluation remain reserved. Structural conformance checks cannot replace real users or authorities.

Residual risks remain: the inaccessible semantic corpus could contain an unobserved collision; registry metadata and vulnerability databases can change; same-owner checks can share assumptions; synthetic records can still be over-read; source vocabulary can be mistaken for endorsement; and future adapters, real data, people, objects, identities, rights, and authorities would introduce entirely new evidence and safety obligations. Those risks are reasons for the open and exact gates, not invitations to silently close them.

## Evidence-credit accounting and reproducibility

Evidence credit is deliberately narrower than artifact presence. A generated JSON file is not automatically a completed proposal. A passing validator is credited only to the exact synthetic contract and acceptance condition that were preregistered. A represented proposal receives no completion credit merely because a proxy exists. An open gap remains open even when the surrounding schema is well formed. An exact gate remains exact-gated even when a refusal record passes every local test. Likewise, a recommendation, inherited tool, historical report, public citation, or sibling result is context or seed evidence only; none becomes Elaren novelty, empirical support, professional competence, or authority.

The same discipline applies to failures. A failed command, parser, audit, test loader, or staged review is not erased after recovery. It remains a zero-credit failed witness. Its recovery is separately named and receives only the bounded credit warranted by the corrected dependency. The x2 test history illustrates this: the import failure did not become a successful suite after the isolated test passed. Twenty-one already-passing dependencies were not replayed. The final record therefore says dependency-corrected composite rather than successful aggregate. The exact-final canonical validator has a different scope and may run once only after the final Git object is remote-equal and clean.

Reproducibility claims are also bounded. Deterministic builders, exact Git-blob hashes, direct-parent history, isolated wheels, synthetic controls, and clean detached representations can support same-owner repeatability under shared infrastructure. They cannot establish independent-team reproduction because the family lanes share repository history, schemas, conventions, tools, and assumptions. Independent reproduction remains an open gap requiring a genuinely independent team, separately governed protocol, independently acquired evidence, and transparent treatment of discrepancies. No correlated sibling result is counted as an independent replication.

## Reversibility, minimisation, and operational hygiene

Reversibility is implemented at several levels. Git history is additive and single-parent, so the source, x1, evidence, and closeout layers remain individually inspectable. Proposal records retain rollback fields and failure conditions. Correction contracts preserve prior and superseding states rather than overwriting disagreement. JSON Patch is used only on synthetic examples and is paired with an unchanged-source check and an invalid-path rejection. Tool installation is isolated to a phase-namespaced D-backed environment that can be removed without mutating shared prefixes. Exact-approval and blocked packets remain held instead of being simulated as completed actions.

Minimisation is equally important. The phase ingests no collection rows, images, documents, serial numbers, measurements, private communications, identities, keys, credentials, or affected-party records. Public sources are represented by names, URLs, status, and bounded use statements rather than copied datasets. The five privacy classes focus on value-bearing identifiers, private absolute paths, credential assignments, interaction-stream material, and private callable or application state. A zero-hit result is a scanner outcome, not a privacy-complete claim. The bounded AST review detects only a small set of dangerous constructs and shell-enabled subprocess patterns; zero findings is not exhaustive security.

Operational hygiene keeps evidence attributable. X1 and evidence were separately committed and pushed before their successor stages. Sparse materialisation kept the owner lane below the 2,000-file ceiling. Generated bytecode was excluded. Exact staged allowlists prevented sibling or shared-lane mutation. Long-running Git work was polled rather than relaunched. Read-only state inspection followed wrapper delays. Version checks did not update Codex desktop or other shared tools. Remote equality uses local HEAD, upstream, tracking, and a fresh live branch query; cached refs alone are not accepted as live proof.

The final canonical receipt is external so a successful validator cannot mutate the exact Git object it validates. That receipt must preserve invocation count, selected-test count, JSON and privacy totals, manifest domains, history, clean state, divergence, and live equality. If it fails, the failure receives zero canonical-success credit and only its failed dependency may be recovered unless a real target change justifies broader work. If it succeeds, it must not be replayed for cleaner output, a larger number, or presentation.

## Closeout and route truth

Complete are the strict x1-before-x2 lifecycle, forty frozen and executed proposals, 160 retained rejecting mutations, ten skills, ten runners, three bounded tool additions, source ledger, threat model, Method Flow, truth and gate registers, structural accessibility report, exact manifests, evidence equality, combined closeout and seal candidate, and the prepared file-backed Neris packet.

Incomplete by protected design are universal semantic novelty, real-object or real-person evidence, professional cataloguing or conservation validation, handling and safety decisions, legal and cultural review, Māori-authority review, affected-user acceptance, manual accessibility evaluation, complete privacy or security assurance, production Freed ID, governed THOS trials, empirical GMUT confirmation, independent-team reproduction, Theory-of-Everything proof, AGI/ASI evidence, consciousness/personhood evidence, canon, and Stage 20 authority.

The committed Neris packet remains `PREPARED_NOT_SENT`. Only after the final commit is pushed, clean, 0/0 divergent, fresh-live equal, and the one exact-final canonical validator succeeds may Elaren reread current live authority, roster, exact-title uniqueness, duplicate state, and protected gates. An acknowledged existing-task send is a later external route event. If any route condition is absent or ambiguous, the truthful state remains `PREPARED_NOT_SENT` or `OPEN_ROUTE_GAP`.
"""


def build(repo: Path) -> None:
    root = repo / OWNER_ROOT
    evidence_truth = load_json(root / "x2/phase-truth-evidence.json")
    outcomes = load_json(root / "x2/outcome-ledger.json")
    test_composite = load_json(root / "validation/x2-test-composite-receipt.json")
    x1_versions = load_json(root / "x1/tool-versions.json")
    final_counts = {
        "effective_negatives": evidence_truth["effective_negatives"] + len(FINAL_OPERATIONAL_FAILURES),
        "methods": evidence_truth["methods"] + len(FINAL_OPERATIONAL_FAILURES),
        "failed_witnesses": evidence_truth["failed_witnesses"] + len(FINAL_OPERATIONAL_FAILURES),
        "passing_witnesses": evidence_truth["passing_witnesses"] + len(FINAL_OPERATIONAL_FAILURES),
        "open_gaps": evidence_truth["open_gaps"],
        "exact_gates": evidence_truth["exact_gates"],
    }
    versions = [
        {"command": "python", "returncode": 0, "first_line": f"Python {x1_versions['python']}", "source": "immutable_x1_version_receipt", "replayed": False},
        {"command": "git", "returncode": 0, "first_line": x1_versions["git"], "source": "immutable_x1_version_receipt", "replayed": False},
        {"command": "node", "returncode": 0, "first_line": x1_versions["node"], "source": "immutable_x1_version_receipt", "replayed": False},
        codex_version(repo),
    ]
    write_json(root / "closeout/environment-version-receipt.json", {"schema": "ghc.family.environment-versions.v2", "owner": OWNER, "phase": PHASE, "updates_performed": False, "rows": versions})
    write_json(root / "closeout/final-operational-failures.json", {"schema": "ghc.family.post-evidence-operational-failures.v1", "count": len(FINAL_OPERATIONAL_FAILURES), "immutable_evidence_counts": {key: evidence_truth[key] for key in final_counts}, "effective_final_overlay": final_counts, "rows": FINAL_OPERATIONAL_FAILURES})
    write_json(
        root / "closeout/phase-truth-final.json",
        {
            **evidence_truth,
            "schema": "ghc.family.phase-truth.v5",
            "lifecycle": "combined_closeout_seal_candidate",
            "source_final": SOURCE_FINAL,
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "final_commit": "resolve_direct_child_of_evidence_containing_this_record",
            "phase_commit_target": 3,
            "merge_target": 0,
            "immutable_evidence_counts": {key: evidence_truth[key] for key in final_counts},
            **final_counts,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        root / "closeout/completion-checklist.json",
        {
            "schema": "ghc.family.completion-checklist.v3",
            "owner": OWNER,
            "phase": PHASE,
            "complete": [
                "exact source verification",
                "planning-only x1 commit and equality",
                "forty frozen proposals",
                "forty executed outcomes using four labels",
                "thirty-six positive controls",
                "one hundred sixty rejected mutations retained",
                "ten phase-local skills",
                "ten family-current runners",
                "three isolated D-backed tools",
                "initial and corrected audit receipts",
                "Method Flow and gate registers",
                "accessible static report and integrated overviews",
                "evidence staged review and exact manifests",
                "x2 dependency-corrected composite with zero aggregate-success credit",
                "combined closeout and seal candidate",
                "prepared unsent Neris activation packet",
            ],
            "incomplete": [
                "universal semantic novelty across unrecovered titles",
                "complete repository suite",
                "independent-team reproduction",
                "real object or participant evidence",
                "professional cataloguing conservation or safety validation",
                "production Freed ID lifecycle and governance",
                "governed blind matched-budget THOS arms",
                "empirical GMUT confirmation",
                "manual and affected-user accessibility evaluation",
                "privacy or exhaustive-security completeness",
                "legal cultural affected-party or Māori-authority review",
                "Theory-of-Everything proof AGI ASI consciousness personhood canon or Stage 20 authority",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_text(root / "closeout/complete-incomplete.md", """# Elaren Kestrel v669-v6 complete and incomplete

Complete within owner-local synthetic scope are strict x1-before-x2 separation, forty frozen and executed proposal dispositions, thirty-six passing positive fixtures, 160 applied and rejected mutations, retained Method Flow, ten skills, ten runners, three isolated tools, source and threat ledgers, structural accessibility, exact evidence manifests, and a prepared closeout/seal packet.

Incomplete are universal novelty, the complete repository suite, independent reproduction, real people or object evidence, professional or safety competence, production identity lifecycle, governed THOS trials, empirical GMUT confirmation, complete privacy or accessibility, exhaustive security, legal or cultural review, Māori authority, Theory-of-Everything proof, AGI/ASI evidence, consciousness/personhood evidence, canon, and Stage 20 authority.

Terminal verdict: `NOT_READY_FOR_STAGE_20`.
""")
    write_json(root / "closeout/wellbeing-final.json", {"schema": "ghc.family.wellbeing-final.v2", "owner": OWNER, "phase": PHASE, "relational_identity_boundary": True, "hope": "make disputed synthetic records reversible without converting software structure into authority", "workload_within_declared_caps": True, "safe_stop_conditions_visible": True, "no_claim_of_consciousness_personhood_continuity_qualification_or_authority": True})
    write_text(root / "final/integrated-overview.md", final_overview())
    packet = activation_packet()
    write_text(root / "handoffs/neris-solane-v669-v7-activation-candidate.md", packet)
    packet_bytes = (packet.rstrip() + "\n").encode("utf-8")
    write_json(root / "handoffs/neris-solane-v669-v7-activation-candidate-receipt.json", {"schema": "ghc.family.prepared-baton-receipt.v2", "recipient_exact_title": "Neris Solane", "prospective_phase": "v669-v7", "bytes": len(packet_bytes), "whitespace_words": len(packet.split()), "sha256": hashlib.sha256(packet_bytes).hexdigest(), "integrity_domain": "normalized_lf_working_file_before_commit", "prepared_not_sent": True, "sent_by_elaren_kestrel": False, "delivery_acknowledged": False})
    write_json(root / "route/route-state.json", {"schema": "ghc.family.route-state.v3", "owner": OWNER, "phase": PHASE, "recipient_exact_title": "Neris Solane", "prospective_successor_phase": "v669-v7", "state": "PREPARED_NOT_SENT", "sent_by_elaren_kestrel": False, "delivery_acknowledged": False, "precontact_during_execution": False, "terminal_requirements": ["exact final committed and pushed", "clean 0/0 state", "fresh four-way equality", "one exact-final canonical success", "current live roster and auth reread", "unique exact-title resolution", "immediate task reread", "duplicate guard", "one acknowledged send"]})
    write_json(root / "seal/seal-candidate.json", {"schema": "ghc.family.combined-closeout-seal.v3", "owner": OWNER, "phase": PHASE, "source_final": SOURCE_FINAL, "x1_commit": X1_COMMIT, "evidence_commit": EVIDENCE_COMMIT, "final_commit": "resolve_direct_child_of_evidence_containing_this_seal", "outcomes": outcomes["counts"], **final_counts, "immutable_evidence_counts": {key: evidence_truth[key] for key in final_counts}, "x2_test_state": test_composite["composite_dependency_completion"]["state"], "x2_aggregate_success_credit": test_composite["aggregate_success_credit"], "terminal_verdict": "NOT_READY_FOR_STAGE_20", "delivery_state": "PREPARED_NOT_SENT"})
    write_json(root / "closeout/closeout-receipt.json", {"schema": "ghc.family.closeout-receipt.v3", "owner": OWNER, "phase": PHASE, "source_final": SOURCE_FINAL, "x1_commit": X1_COMMIT, "evidence_commit": EVIDENCE_COMMIT, "outcomes": outcomes["counts"], "immutable_evidence_counts": {key: evidence_truth[key] for key in final_counts}, "effective_counts": final_counts, "x2_test_composite": "22/22 dependencies with zero aggregate-success credit", "privacy_complete_claim": False, "accessibility_complete_claim": False, "independent_reproduction_claim": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "route_state": "PREPARED_NOT_SENT"})
    write_json(root / "validation/final-validation-plan.json", {"schema": "ghc.family.exact-final-validation-plan.v3", "owner": OWNER, "phase": PHASE, "invocation_limit": 1, "run_only_after": ["combined final commit", "push", "clean state", "0/0 divergence", "fresh four-way equality"], "dependencies": ["exact head and direct ancestry", "three single-parent phase commits and zero merges", "exact x1 evidence final-delta and final-owner manifest replays", "all owner JSON parses", "five-class privacy scan", "bounded Python AST review", "new final test module", "x2 dependency-corrected composite distinction", "accessible report structure", "baton integrity", "clean state and fresh equality"], "post_success_replay": False, "external_receipt_only": True})


def staged_review(repo: Path) -> None:
    names = run(repo, "git", "diff", "--cached", "--name-only", "--diff-filter=ACMRT", "HEAD").stdout.splitlines()
    allowed_prefixes = [
        "docs/elaren-kestrel/v669-v6/closeout/",
        "docs/elaren-kestrel/v669-v6/final/",
        "docs/elaren-kestrel/v669-v6/handoffs/",
        "docs/elaren-kestrel/v669-v6/route/",
        "docs/elaren-kestrel/v669-v6/seal/",
        "docs/elaren-kestrel/v669-v6/validation/final-",
    ]
    allowed_exact = {
        "scripts/build_ghc_family_elaren_kestrel_v669_v6_final.py",
        "scripts/validate_ghc_family_elaren_kestrel_v669_v6_final.py",
        "tests/test_ghc_family_elaren_kestrel_v669_v6_final.py",
    }
    disallowed = [name for name in names if name not in allowed_exact and not any(name.startswith(prefix) for prefix in allowed_prefixes)]
    exclusions = {
        "docs/elaren-kestrel/v669-v6/validation/final-staged-review.json",
        "docs/elaren-kestrel/v669-v6/validation/final-delta-manifest.json",
        "docs/elaren-kestrel/v669-v6/validation/final-owner-manifest.json",
    }
    json_errors: list[str] = []
    privacy: list[dict[str, str]] = []
    for relpath in names:
        if relpath in exclusions:
            continue
        data = subprocess.run(["git", "show", f":{relpath}"], cwd=repo, check=True, capture_output=True).stdout
        text = data.decode("utf-8", errors="replace")
        if relpath.endswith(".json"):
            try:
                json.loads(text)
            except Exception as exc:  # noqa: BLE001
                json_errors.append(f"{relpath}:{type(exc).__name__}")
        privacy.extend({"path": relpath, **row} for row in privacy_candidates(text))
    diff_exit = run(repo, "git", "diff", "--cached", "--check").returncode
    receipt = {"schema": "ghc.family.final-staged-review.v3", "owner": OWNER, "phase": PHASE, "staged_entry_count_before_self": len(names), "disallowed_paths": disallowed, "json_errors": json_errors, "privacy_candidates": privacy, "diff_cached_exit": diff_exit, "passed": not disallowed and not json_errors and not privacy and diff_exit == 0, "self_exclusions": sorted(exclusions)}
    write_json(repo / OWNER_ROOT / "validation/final-staged-review.json", receipt)
    if not receipt["passed"]:
        raise RuntimeError("final staged review failed closed")


def manifests_from_index(repo: Path) -> None:
    names = run(repo, "git", "diff", "--cached", "--name-only", "--diff-filter=ACMRT", "HEAD").stdout.splitlines()
    exclusions = [
        "docs/elaren-kestrel/v669-v6/validation/final-staged-review.json",
        "docs/elaren-kestrel/v669-v6/validation/final-delta-manifest.json",
        "docs/elaren-kestrel/v669-v6/validation/final-owner-manifest.json",
    ]
    delta = []
    for relpath in sorted(name for name in names if name not in exclusions):
        data = subprocess.run(["git", "show", f":{relpath}"], cwd=repo, check=True, capture_output=True).stdout
        delta.append({"path": relpath, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    owner_names = set(names)
    owner_names.update(run(repo, "git", "ls-tree", "-r", "--name-only", "HEAD", "docs/elaren-kestrel/v669-v6", "scripts", "tests").stdout.splitlines())
    owner = []
    for relpath in sorted(owner_names):
        if relpath in exclusions:
            continue
        if not (relpath.startswith("docs/elaren-kestrel/v669-v6/") or (relpath.startswith("scripts/") and ("elaren_kestrel_v669_v6" in relpath or relpath.startswith("scripts/ghc_family_typewriter_"))) or (relpath.startswith("tests/") and "elaren_kestrel_v669_v6" in relpath)):
            continue
        spec = f":{relpath}" if relpath in names else f"HEAD:{relpath}"
        data = subprocess.run(["git", "show", spec], cwd=repo, check=True, capture_output=True).stdout
        owner.append({"path": relpath, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    common = {"schema": "ghc.family.content-manifest.v4", "owner": OWNER, "phase": PHASE, "self_exclusions": exclusions}
    root = repo / OWNER_ROOT / "validation"
    write_json(root / "final-delta-manifest.json", {**common, "domain": "final_exact_staged_git_blobs", "entry_count": len(delta), "entries": delta})
    write_json(root / "final-owner-manifest.json", {**common, "domain": "owner_exact_evidence_head_plus_final_staged_git_blobs", "entry_count": len(owner), "entries": owner})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--review-staged", action="store_true")
    parser.add_argument("--manifests-from-index", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    if args.review_staged:
        staged_review(repo)
    elif args.manifests_from_index:
        manifests_from_index(repo)
    else:
        build(repo)


if __name__ == "__main__":
    main()
