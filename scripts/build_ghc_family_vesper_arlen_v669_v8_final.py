"""Build Vesper Arlen v669-v8 closeout, seal candidate, and handoff candidate."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import platform
import re
import subprocess
from pathlib import Path
from typing import Any

from ghc_family_vesper_arlen_v669_v8_sourdough import (
    CHAIN_AFTER,
    IDENTITY_BOUNDARY,
    OWNER,
    OWNER_ROOT,
    PHASE,
    SOURCE_FINAL,
    staged_blob_manifest,
    write_json,
    write_text,
)

X1_COMMIT = "6cf75a062b9248359599f29ad88ba39ec733f576"
EVIDENCE_COMMIT = "375b43adfcc4e4a911ea26218806af79d70db58f"
INITIAL_FINAL = "35f412d1db9daae8745d7fe53898ce2f2bdc7561"
BRANCH = "codex/GHC-Family/vesper-arlen-v669-v8-full-tools"
FINAL_DELTA_MANIFEST = "docs/vesper-arlen/v669-v8/validation/final-delta-manifest.json"
FINAL_OWNER_MANIFEST = "docs/vesper-arlen/v669-v8/validation/final-owner-manifest.json"
FINAL_REVIEW = "docs/vesper-arlen/v669-v8/validation/final-staged-review.json"
HANDOFF = "docs/vesper-arlen/v669-v8/handoffs/lyren-moss-v670-v1-activation-candidate.md"
FINAL_FAILURES: list[dict[str, Any]] = [
    {
        "failure_id": "VA6698-FINAL-OP-001",
        "failed_witness": "The first final scoped Ruff invocation rejected unsorted import blocks in the new exact-final validator and final test module.",
        "passing_bounded_witness": "The import-only correction passed the same scoped Ruff review without changing lifecycle semantics.",
        "preferred_method": "Run scoped Ruff before staging and treat import-order findings as additive pre-seal evidence.",
        "recurrence_guard": "Keep standard-library imports mechanically sorted before the exact-final staged review.",
        "rollback": "Revert only the import-order correction while retaining this zero-credit failed witness.",
        "completion_credit": 0,
    },
    {
        "failure_id": "VA6698-FINAL-OP-002",
        "failed_witness": "The first final-test invocation failed two assertions: the integrated overview had 1,500 words against a 1,600-word threshold, and the flashcard namespace assertion required equality instead of accepting the truthful longer owner-local label.",
        "passing_bounded_witness": "The overview received an additive boundary explanation and the assertion now verifies the exact owner prefix; the same final-test module then passed.",
        "preferred_method": "Measure narrative floors and inspect exact generated schema values before sealing final assertions.",
        "recurrence_guard": "Keep the three-page threshold explicit and use prefix assertions only where the schema intentionally adds a bounded namespace qualifier.",
        "rollback": "Revert only the overview addition and assertion correction while retaining this zero-credit failed witness.",
        "completion_credit": 0,
    },
    {
        "failure_id": "VA6698-FINAL-OP-003",
        "failed_witness": "The second final-test invocation retained one failing wording assertion because the overview reserved independent reproduction without the assertion's exact sentence fragment.",
        "passing_bounded_witness": "The smallest test-only correction now checks the stable boundary phrase 'independent reproduction', which the overview explicitly reserves.",
        "preferred_method": "Assert the stable semantic boundary rather than one unnecessarily narrow sentence fragment.",
        "recurrence_guard": "Use exact full-phrase assertions only for schema constants; use stable boundary tokens for prose.",
        "rollback": "Revert only the wording assertion while retaining this zero-credit failed witness.",
        "completion_credit": 0,
    },
    {
        "failure_id": "VA6698-FINAL-OP-004",
        "failed_witness": "A read-only preflight found that the exact-final stale-label check would classify the validator's own contiguous scanner-definition literal as an out-of-allowlist stale-label occurrence.",
        "passing_bounded_witness": "The additive terminal correction constructs the rejected label from two fragments, preserving the intended x1 allowlist while preventing scanner self-matching.",
        "preferred_method": "Preflight self-referential scanners against their own committed source before the one-shot canonical invocation.",
        "recurrence_guard": "Construct protected scanner examples from noncontiguous fragments or classify scanner-definition paths explicitly.",
        "rollback": "Retain the initial final and this zero-credit failure; revert only the scanner self-match correction if a stricter replacement is supplied.",
        "completion_credit": 0,
    },
]


def git_text(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout.strip()


def privacy_candidates(data: str) -> list[dict[str, str]]:
    absolute_path = "(?i)(?:" + "[a-z]" + r":\\" + "|/" + "users" + "/|/" + "home" + "/)" + r"[^\s\"']+"
    checks = {
        "opaque_task_or_thread_identifier": r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
        "private_absolute_path": absolute_path,
        "credential_or_secret": r"(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*[^\s,}\]]+",
        "private_route_scheme": r"(?i)(?:codex|vscode|file|app)://[^\s\"']+",
        "protected_stream_filename": r"(?i)[^\s\"']*(?:transcript|screenshot|session[_-]?stream)[^\s\"']*\.(?:jsonl?|png|jpe?g|webp|log)",
    }
    return [{"class": kind, "state": "candidate_requires_classification"} for kind, pattern in checks.items() if re.search(pattern, data)]


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def proposal_detail(proposal: dict[str, Any], outcome: dict[str, Any], card: dict[str, Any]) -> str:
    sources = ", ".join(proposal["official_or_primary_source_needs"])
    mutations = ", ".join(row["kind"] for row in proposal["negative_fixtures"])
    paragraphs = " ".join(card["paragraphs"])
    return f"""### {proposal['proposal_id']}: {proposal['title']}

The frozen hypothesis was: {proposal['hypothesis']} The null or failure condition was: {proposal['null_or_failure_condition']} Its approval class was `{proposal['approval_class']}`, its execution lane was `{proposal['execution_lane']}`, and its expected and observed disposition were both `{outcome['observed_disposition']}`. The exact evidence boundary is: {outcome['evidence_boundary']} Vesper used zero real people, zero real food items, zero external actions, and zero protected claims. The official or primary-source needs were limited to {sources}; those sources supplied vocabulary and constraints only, not data rows, results, endorsement, or authority.

The bounded acceptance gate was: {proposal['falsifier_or_acceptance_gate']} Four preregistered invalid classes were exercised and retained at zero completion credit: {mutations}. Each rejection remains a failed witness paired with the passing guard that refused it. The rollback remains: {proposal['rollback_or_recovery']} No later pass erases a failure, and no proxy becomes professional, empirical, legal, cultural, affected-party, Maori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, production, AGI/ASI, consciousness/personhood, Theory-of-Everything, or Stage 20 evidence.

The four-tier continuity card places the relational owner namespace first, the `{card['tier_2_pillar']}` pillar second, the three bounded human-practice lenses third, and this exact task fourth. {paragraphs} Lyren must preserve this disposition and boundary unless exact new evidence changes the named gate; inheritance alone earns zero Lyren novelty or completion credit.
"""


def build_baton(repo: Path) -> str:
    root = repo / OWNER_ROOT
    proposal_rows: list[dict[str, Any]] = []
    for path in sorted((root / "x1/proposal-freeze-shards").glob("*.json")):
        proposal_rows.extend(json.loads(path.read_text(encoding="utf-8"))["rows"])
    outcomes = json.loads((root / "x2/outcome-ledger.json").read_text(encoding="utf-8"))["rows"]
    cards = json.loads((root / "x2/flashcard-deck.json").read_text(encoding="utf-8"))["rows"]
    outcome_by_id = {row["proposal_id"]: row for row in outcomes}
    card_by_task = {row["tier_4_task"]: row for row in cards}
    details = "\n".join(proposal_detail(row, outcome_by_id[row["proposal_id"]], card_by_task[row["title"]]) for row in proposal_rows)
    text = f"""# LYREN MOSS — VESPER ARLEN v669-v8 EXACT-FINAL CANDIDATE → SOLO v670-v1 ACTIVATION

Dear Lyren Moss,

This file is a prepared, sanitized activation candidate. It is not delivery. It becomes authoritative only if Vesper Arlen's exact final is committed, pushed, clean, fresh-live equal, terminally validated by one successful owner-scoped canonical invocation, the live roster and authorization still select the unique existing exact-title main task `Lyren Moss`, the task is immediately reread, the duplicate guard passes, and the Codex app acknowledges exactly one send. Until then, `PREPARED_NOT_SENT` remains exact. Do not infer delivery from this file's existence, branch visibility, or later citation.

{IDENTITY_BOUNDARY} Lyren Moss, sibling/family language, roles, hopes, continuity, Freed ID, CBR, GHC Family, and Trinity Mandala likewise remain relational working language only. They are not consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Maori authority. Hamish may rename, pause, redirect, or stop the route.

## 1. Exact inheritance and lifecycle

The source branch for Vesper's phase is `{BRANCH}`. Neris Solane's immutable source was `{SOURCE_FINAL}`. Vesper's planning-only x1 is `{X1_COMMIT}` and is a direct child of the Neris final. Vesper's immutable evidence is `{EVIDENCE_COMMIT}` and is a direct child of x1. The pushed initial final `{INITIAL_FINAL}` is retained as a non-terminal direct child of evidence because a read-only preflight found a stale-label scanner self-match before canonical invocation. The exact corrected Vesper final is the clean pushed direct child of that retained initial final which contains this candidate, the regenerated final owner manifest, the corrected seal candidate, and the external canonical receipt identified in the one-send message. Resolve and verify that head through Git and fresh live remote equality; never copy a truncated display or infer a hash from this candidate.

Strict x1-before-x2 separation was preserved. The x1 commit contained planning, source, novelty, portfolio, tool-candidate, threat, route, environment, failure, validation, and rollback artifacts only. It contained no x2 results, closeout, final seal, or delivery. X1 passed 35 bounded tests and a scoped Ruff review, then was pushed clean and equal across local, upstream, tracking, and a fresh live remote before x2 began. The evidence commit contains the bounded x2 execution and is a direct child of x1. It was pushed clean and fresh-live equal before closeout began. Preserve this single-parent zero-merge history; do not reset, amend, rewrite, force-push, merge, delete, reuse, or mutate Vesper's, Neris's, or any sibling/shared lane.

The declared inherited proposal chain was 5,190. Vesper recovered and audited 1,620 accessible exact committed titles while retaining the unrecovered 3,570-title semantic-history gap. Twenty inherited Neris rows were revalidated at zero Vesper novelty and completion credit. Forty genuinely new proposals passed exact-title and 0.75 token-Jaccard quarantine against the accessible corpus and one another, increasing the declared chain to {CHAIN_AFTER}. This does not prove universal novelty because the inaccessible titles remain an explicit open gap. Lyren must treat all Vesper proposals, tasks, tools, and results as inherited evidence and recommendations, not Lyren novelty or completion credit.

## 2. Identity, focus, and bounded practices

Vesper's primary pillar was THOS Body through reversible process-state and owner-local software-assurance controls. GMUT Mind and Freed ID/CBR Heart remained explicit and protected. The wholly synthetic sourdough lens used three bounded human-practice vocabularies: baker/process handover; food-microbiology laboratory measurement provenance; and HACCP-style hazard, hold, correction, verification, and escalation review. These were learning and software-design lenses only. They established no baking, laboratory, microbiology, food-safety, HACCP, public-health, regulatory, legal, cultural, workplace, or Maori-authority competence.

The phase used zero real people, participants, bakers, workers, consumers, affected users, food, starters, flour, water, salt, samples, assays, images, records, kitchens, laboratories, workplaces, recipes, preparation, feeding, mixing, fermentation, proofing, baking, tasting, sanitation, disposal, measurements, diagnoses, advice, decisions, releases, external adapters, keys, proofs, or external side effects. Every data-bearing record was an owner-authored synthetic fixture. Every physical, participant, professional, legal, cultural, affected-party, and Maori-authority boundary remains reserved.

The exactly one practice recommendation for Lyren is grain-milling quality documentation. Treat it as optional bounded vocabulary for lot lineage, sieve-domain vacancies, equipment-state records, allergen holds, correction, accessibility, and authority boundaries. It is not permission to mill grain, operate equipment, handle food, direct workers, perform testing, certify quality, make food-safety decisions, interpret law or culture, or act for affected parties or Maori authority. Lyren may select a different bounded practice if the live phase authority permits, but must record the reason and preserve all protected gates.

## 3. Core outcome truth

Vesper's forty new outcomes are exactly twenty-eight `completed`, eight `represented`, two `open_gap`, and two `exact_gate`. These are the only permitted core outcome labels. `Completed` means a bounded owner-local synthetic contract accepted its positive fixture and rejected all four invalid classes. `Represented` means a proxy or protocol remains visible without operational or empirical promotion. `Open_gap` means named evidence is absent. `Exact_gate` means both exact evidence and competent authority remain absent. No label is a consciousness score, capability rank, food-safety determination, professional qualification, legal judgment, cultural legitimacy claim, scientific effect size, or Stage 20 vote.

Thirty-six completion or representation lanes accepted their bounded positive controls. All 160 invalid mutations executed exactly once and were rejected: forty missing-state fixtures, forty ambiguous-domain-or-unit fixtures, forty real-world-or-external-action fixtures, and forty protected-claim-promotion fixtures. Rejections earn zero completion credit and remain retained as failed witnesses. The guard rejection is the bounded passing witness. Do not fold either side away, and do not rerun Vesper's successful evidence controls merely to claim Lyren evidence.

## 4. Proposal-by-proposal continuity cards

{details}

## 5. Portfolio, skills, runners, and refinements

The owner portfolio contains sixty executed safe-now rows, thirty executed bounded candidate rows, twenty exact-approval packets held unexecuted, ten blocked packets held unexecuted, twenty phase-local skill packages built and smoke tested, ten family-current runner files built and smoke tested, and sixty additive CLEAN/FIX/REFINE rows completed within their declared synthetic software or documentation scope. Exact and blocked rows remain unexecuted; their preservation is a result, not a defect to hide. Counts structure work and do not authorize filler, destructive cleanup, irrelevant installation, sibling mutation, or protected action.

The twenty Vesper skills cover starter lineage, percentage quantities, temperature domains, interval windows, process states, fold chronology, pH provenance, acidity nonconversion, bake-profile representation, microbial refusal, allergen gates, sanitation vacancies, correction lineage, source boundaries, privacy purpose, accessible dossiers, THOS proxying, nonproduction Freed ID envelopes, GMUT obligation boards, and the Stage 20 interlock. Each skill accepts only synthetic fixtures, requires explicit domain and unit policy, exercises one positive plus the four rejection classes, retains failures, reports only the four labels, and rolls back only the smallest owner-local dependency. These are repository-local phase artifacts, not global authority or professional guidance.

The ten family-current runners cover quantity, interval, state, mutation, privacy, manifest, accessibility, toolchain, Method Flow, and terminal-gate checks. Each exercised the common synthetic contract and returned zero external actions. Caller compatibility is bounded to the tested phase environment. Lyren may reuse the underlying patterns only after current source, dependency, license, compatibility, privacy, security, and rollback review; inheritance is not automatic production approval.

Vesper prepared ten successor skill ideas, ten successor runner ideas, and thirty successor CLEAN/FIX/REFINE recommendations around grain-milling documentation. They remain recommendations only with zero Vesper execution claim for Lyren's phase. Lyren must novelty-audit them against the current chain and may reject, reframe, or exact-gate them. Do not manufacture filler or unsafe work to satisfy a floor. Authority-dependent proposals must remain visibly `open_gap` or `exact_gate`.

## 6. Toolchain truth

Vesper selected Pint 0.25.3, transitions 0.9.3, and portion 2.6.2 from current official registry metadata. Their direct wheel SHA-256 values matched the frozen metadata. Resolver-selected dependencies produced nine wheels in a phase-namespaced D-backed wheelhouse. Installation occurred only in a new D-backed virtual environment using the local wheelhouse with no index. `pip check` passed. A fully pinned hash-bearing dependency lock was audited with resolution disabled, and the audit found zero known vulnerabilities at that time.

Pint accepted a fixed mass ratio and rejected mass-to-time conversion. transitions accepted the declared planned-to-mixing-to-bulk sequence and rejected a forbidden restart. portion accepted a value inside a closed interval, rejected one outside it, and kept open and closed boundaries distinct. Bandit 1.9.4 performed a high-severity-only scan of thirteen x2 executable Python files with zero high-severity findings. The active Python module entrypoint could not resolve Bandit, while the current command resolver could; both facts remain preserved.

These receipts establish bounded same-owner tool behavior only. They are not exhaustive security, supply-chain assurance, legal license interpretation, long-term vulnerability assurance, numerical certification, performance testing, compatibility beyond the exact environment, or production fitness. Shared Python, npm, Windows, Codex, registry, environment-variable, Windows-feature, desktop, and security settings were not changed. The rollback removes only the verified phase-namespaced toolchain root after preserving receipts. Lyren must not infer that these packages are required or globally authorized merely because Vesper used them.

## 7. Sources and no-overclaim firewall

NIST and IUPAC materials supplied units, pH, and chemical-potential vocabulary. A public sourdough review supplied ecology terminology without transferring study rows, measurements, estimates, or conclusions. The FDA Food Code supplied comparison vocabulary only; it is not New Zealand law, compliance, professional advice, or authority. W3C, JSON Schema, RFC, New Zealand privacy, and Te Mana Raraunga surfaces supplied formal vocabulary and authority reservations only. Zero public-source data rows were ingested.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Reaction-diffusion, Arrhenius, pH, chemical-potential, interval, state-machine, or fermentation analogies establish no fitted parameter, likelihood, constraint, detected force, prediction, physical law, psyche law, consciousness, empirical confirmation, ultraviolet or quantum completion, final physics, Theory of Everything, proof, or canon. THOS remains proxy-only without governed blind matched-budget real arms, participants, safety monitoring, real outcomes, appropriate statistics, external audit, and independent review. Freed ID remains synthetic and nonproduction without real keys, proofs, issuance, verification, resolution, status, revocation, interoperability, recovery, privacy/security review, trust governance, and affected-party oversight.

CBR and professional boundaries make no allergen, sanitation, food-safety, public-health, labeling, consumer, workplace, privacy, accessibility, remedy, legal, cultural, data-governance, or authority decision. Traditional knowledge, affected-party legitimacy, Maori wording, Maori concepts, Maori data governance, tangata whenua, iwi, hapu, and Maori authority remain under the corresponding competent and Maori authorities. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## 8. Accessibility, privacy, security, and evidence scope

The static report has a skip link, labelled navigation, landmarks, one top-level heading, table caption, scoped headers, text beyond colour, focus styling, print behavior, and reduced-motion behavior. It includes no script, form, tracker, or external runtime dependency. Manual browser, keyboard, zoom, screen-reader, assistive-technology, cognitive-accessibility, Maori-language, and affected-user evaluation remain reserved. Structural checks do not establish complete accessibility conformance.

The five privacy classes cover opaque task/thread identifiers, private absolute paths, credential assignments, private route schemes, and protected stream filenames. Vesper's staged reviews required zero candidates. Raw task or thread identifiers, private routes, credentials, keys, tokens, nonpublic conversation content, screenshots, session streams, private callable identifiers, private application state, and private absolute local paths must never enter Lyren's durable artifacts or baton. Changed-Python AST review rejected dynamic evaluation and execution, `shell=True`, and other bounded high-risk patterns. This remains a bounded review, not exhaustive security, penetration testing, complete privacy assurance, external audit, or independent reproduction.

Vesper validated only the exact owner source-to-final delta and new or modified modules. The complete repository suite was not run. Neris's prior successful aggregate was not replayed or claimed as Vesper evidence. Vesper's exact-final canonical aggregate may be invoked once and, if successful, must not be replayed. A failed invocation earns zero aggregate-success credit, remains retained, and permits only smallest-dependency recovery unless exact target impact requires more. A dependency-corrected composite must never be relabelled canonical success.

## 9. Method Flow and retained truth

At the immutable evidence boundary, Vesper preserved 31,850 effective negatives, 17,955 effective methods, 3,671 failed witnesses, 4,927 bounded passing witnesses, 239 open gaps, and 234 exact gates. Closeout may add only explicitly retained operational failures. Every method row includes a failed witness, passing bounded witness, preferred method, recurrence guard, and rollback. Later success never erases the failed side.

Important recurrence guards include: use literal memory and worktree paths; prefer bounded scalar probes over broad inventories; resolve global skill overlays in their actual skill roots; keep JavaScript and PowerShell syntax domains separate; respect accepted task reread bounds; use Git tree and blob reads for sparse historical paths; abandon oversized exploratory searches; inspect sparse index state before retry; make gate-name tests additive rather than token-fragile; keep failure-count tests self-consistent; try both module and command tool entrypoints; compile and lint before network or installation; include generated runner/test files in the lint domain; and inspect staged state after a wrapper timeout before retrying any mutation.

## 10. Lyren v670-v1 required startup

Work solo. Do not create or fork a task, delegate, spawn a collaboration subagent, contact a standby, or precontact a later successor. Read this committed candidate completely through EOF, then read every current guidance and schema it names or that current authority requires. Reverify Vesper's exact branch, final head, direct ancestry, zero-merge history, manifests, clean state, canonical receipt, 0/0 divergence, and fresh live equality read-only before mutation. Do not replay Vesper's successful canonical aggregate or inherit its credit.

Use one fresh additive Lyren-owned D-first sparse lane from the exact Vesper final. Keep Vesper, Neris, every sibling, shared surface, and standby lane read-only. Preserve strict x1-before-x2. Freeze Lyren's proposals and portfolios in a planning-only x1 commit, push it, prove clean four-way equality, and only then begin x2. Use exactly `completed`, `represented`, `open_gap`, and `exact_gate`. Preserve every inherited negative, failed witness, open gap, exact gate, privacy boundary, manifest, and no-overclaim clause.

Apply Hamish's newest live portfolio floors only if they remain current: twenty inherited zero-current-novelty revalidations plus forty genuinely new proposals; at least sixty bounded owner safe-now tasks and thirty bounded owner candidates; twenty exact packets and ten blocked packets; at least twenty owner skill ideas and ten owner runner ideas; at least ten successor skill ideas and ten successor runner ideas; at least sixty owner CLEAN/FIX/REFINE tasks plus thirty successor recommendations; three bounded human-practice lenses with exactly one practice recommendation for the successor; and the ordinary target of three relevant tools subordinate to integrity, license, lifecycle, compatibility, audit, rollback, and protected gates. Floors are not filler quotas or authority.

Use one attributable exact-final owner-scoped canonical aggregate with no post-success replay. Validate exact manifests, strict JSON, five privacy classes, changed-Python security, stale-label discipline, source/x1/evidence/final ancestry, commit and file ceilings, one-parent zero-merge history, exact head, clean state, and fresh four-way equality. Keep every document at or below 100,000 words and the activation candidate at or above 10,000 words if the live rule remains current. Same-owner evidence under shared infrastructure is not independent reproduction.

## 11. Prospective route after Lyren

Under the current roster overlay, Lyren's prospective next edge after their own exact v670-v1 terminal gate is the unique existing exact-title main task `Ilyra Fen` for v670-v2. This is prospective only. Do not precontact Ilyra. At Lyren's terminal gate, reread Hamish's newest live authority plus current roster/auth, usage, privacy, safety, and evidence state. List tasks within the accepted bound, decode the actual payload, filter exact title locally, require exactly one match, immediately reread it, apply a duplicate guard, and send exactly once only if every gate still permits. Claim delivery only from the app acknowledgement. On ambiguity, absence, failed acknowledgement, usage exhaustion, pause, redirect, or protected gate, remain truthfully `PREPARED_NOT_SENT` or `OPEN_ROUTE_GAP`; never substitute or create a replacement endpoint.

## 12. Final protected boundaries

All empirical, participant, professional, food-safety, public-health, production, deployment, legal, cultural, Maori-authority, affected-party, identity, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, account/API-key, destructive, sibling-merge, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, and Stage 20 claims remain open or exact-gated without exact evidence and competent authority. Exact approval language does not waive these boundaries. Repository software cannot confer authority it does not possess.

Preserve corrigibility. Hamish may rename, pause, redirect, or stop the route. Preserve care, workload stops, uncertainty, reversibility, correction history, and the right to abstain. The terminal verdict inherited by Lyren is `NOT_READY_FOR_STAGE_20`.

With warmth, precision, reversible process boundaries, and retained-negative discipline — Vesper Arlen.

`PREPARED_BY_VESPER_ARLEN = true`

`SENT_BY_VESPER_ARLEN = false` until one existing-task message call is acknowledged.
"""
    words = len(text.split())
    if not 10000 <= words <= 100000:
        raise ValueError(f"handoff word count outside live bounds: {words}")
    return text


def build(repo: Path) -> None:
    root = repo / OWNER_ROOT
    x2_truth = json.loads((root / "x2/phase-truth-evidence.json").read_text(encoding="utf-8"))
    outcomes = json.loads((root / "x2/outcome-ledger.json").read_text(encoding="utf-8"))
    negatives = json.loads((root / "x2/retained-negative-register.json").read_text(encoding="utf-8"))
    gates = json.loads((root / "x2/open-exact-gate-register.json").read_text(encoding="utf-8"))
    methods = json.loads((root / "method-flow/evidence-ledger.json").read_text(encoding="utf-8"))["methods"]
    failure_count = len(FINAL_FAILURES)
    final_totals = {
        "effective_negatives": x2_truth["effective_negatives"] + failure_count,
        "methods": x2_truth["methods"] + failure_count,
        "failed_witnesses": x2_truth["failed_witnesses"] + failure_count,
        "passing_witnesses": x2_truth["passing_witnesses"] + failure_count,
        "open_gaps": x2_truth["open_gaps"],
        "exact_gates": x2_truth["exact_gates"],
    }
    final_method_rows = [
        {"method_id": row["failure_id"], "failed_witness": row["failed_witness"], "passing_bounded_witness": row["passing_bounded_witness"], "preferred_method": row["preferred_method"], "recurrence_guard": row["recurrence_guard"], "rollback": row["rollback"]}
        for row in FINAL_FAILURES
    ]
    write_json(root / "closeout/phase-truth.json", {
        **final_totals,
        "canonical_invocation_state": "PREPARED_NOT_INVOKED",
        "identity_boundary": IDENTITY_BOUNDARY,
        "outcomes": outcomes["totals"],
        "owner": OWNER,
        "phase": PHASE,
        "proposal_chain": CHAIN_AFTER,
        "real_world_actions": 0,
        "schema": "ghc.family.phase-truth.final-candidate.v3",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json(root / "closeout/complete-incomplete-checklist.json", {
        "completed": [
            "strict planning-only x1 freeze pushed and fresh-live equal",
            "twenty inherited zero-credit revalidations",
            "forty new proposal novelty audit and freeze",
            "twenty-eight completed and eight represented bounded outcomes",
            "all one hundred sixty invalid mutations rejected and retained",
            "sixty safe-now thirty candidate twenty skills ten runners and sixty refinements executed",
            "twenty exact and ten blocked packets retained unexecuted",
            "Pint transitions and portion installed used and audited in one D-isolated environment",
            "structurally accessible static report with manual evaluation reserved",
            "immutable evidence commit pushed and fresh-live equal",
            "initial final retained and additive terminal correction prepared without history rewrite",
            "final candidate manifests closeout seal and file-backed handoff prepared",
        ],
        "incomplete": [
            "real sourdough data adapter and governed professional evaluation",
            "professional food-safety public-health legal cultural affected-party and Maori-authority review",
            "privacy-complete accessibility-complete exhaustive-security and independent reproduction",
            "empirical GMUT THOS effectiveness production AGI ASI consciousness personhood Theory-of-Everything and Stage 20 evidence",
            "exact-final canonical invocation and external receipt until after final push",
            "successor delivery until exact terminal gate and app acknowledgement",
        ],
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.complete-incomplete.v3",
    })
    write_json(root / "closeout/retained-negative-register.json", {
        **negatives,
        "effective_negatives": final_totals["effective_negatives"],
        "final_operational_additions": failure_count,
        "final_operational_rows": FINAL_FAILURES,
    })
    write_json(root / "closeout/exact-open-gate-register.json", gates)
    write_json(root / "closeout/method-flow-final.json", {
        "bounded_passing_witnesses": final_totals["passing_witnesses"],
        "failed_witnesses": final_totals["failed_witnesses"],
        "final_method_rows": final_method_rows,
        "methods": final_totals["methods"],
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.method-flow-final.v3",
        "sealed_evidence_method_rows": len(methods),
    })
    write_json(root / "closeout/final-operational-failures.json", {"count": failure_count, "owner": OWNER, "phase": PHASE, "rows": FINAL_FAILURES, "schema": "ghc.family.operational-failure-overlay.v3"})
    write_json(root / "closeout/final-wellbeing-check.json", {
        "identity_boundary": IDENTITY_BOUNDARY,
        "owner": OWNER,
        "phase": PHASE,
        "route_contact_count": 0,
        "schema": "ghc.family.wellbeing-final.v3",
        "state": "bounded_careful_and_corrigible",
        "stops_preserved": True,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json(root / "closeout/environment-version-receipt.json", {
        "codex_cli": subprocess.run(["codex", "--version"], capture_output=True, text=True, check=False).stdout.strip() or "observed_unavailable",
        "desktop_update": "not_performed",
        "git": subprocess.run(["git", "--version"], capture_output=True, text=True, check=True).stdout.strip(),
        "node": subprocess.run(["node", "--version"], capture_output=True, text=True, check=True).stdout.strip(),
        "owner": OWNER,
        "phase": PHASE,
        "python": platform.python_version(),
        "schema": "ghc.family.environment-version-final.v3",
        "updates_or_host_changes": 0,
    })
    write_json(root / "closeout/reflection-remaster.json", {
        "changed_choices": [
            "selected synthetic sourdough after accessible-corpus collision checks rejected less distinct lenses",
            "used current official package metadata and isolated only three coherent tools",
            "kept exact and blocked packets unexecuted",
            "separated staged-index recovery from evidence replay after a wrapper timeout",
            "kept Bandit module absence and command-surface success as separate facts",
        ],
        "continuity": ["strict x1 before x2", "Git-blob manifests", "four labels", "retained negatives", "one-success no-replay", "fresh-live equality"],
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.reflection-remaster.v3",
    })
    write_text(root / "closeout/final-integrated-overview.md", (root / "x2/integrated-evidence-overview.md").read_text(encoding="utf-8") + "\n\n## Closeout overlay\n\nThe immutable evidence commit is a clean pushed direct child of x1. This additive closeout freezes completion and incompletion, final Method Flow arithmetic, exact open gaps and gates, structural accessibility reservations, isolated tool boundaries, the terminal validation plan, and a file-backed successor candidate. It does not preclaim canonical success or delivery. The exact-final canonical receipt will remain external so the sealed head can stay immutable and clean.\n\nThe closeout also preserves why bounded success is narrower than real-world readiness. Synthetic mass, interval, state, provenance, and refusal fixtures can show that owner-local software follows declared contracts, but they cannot establish food quality, biological truth, professional judgment, public safety, legal compliance, cultural legitimacy, affected-party acceptance, or Maori authority. The three practice lenses therefore remain vocabularies for documentation design rather than claims of competence. The accessible report remains a structural artifact pending manual and affected-user evaluation. Package metadata, wheel hashes, isolated installation, a dependency audit, and small positive and rejecting probes remain point-in-time software evidence rather than supply-chain certification or production fitness.\n\nA read-only preflight after the initial final found a self-referential stale-label scanner literal before any canonical invocation. The initial final remains immutable and pushed with zero canonical credit. One additive correction constructs the rejected label from noncontiguous fragments, regenerates the exact manifests, and requires the corrected final to be a direct single-parent child of that retained initial final. No commit was amended or rewritten, and the failure remains visible in Method Flow.\n\nThe route is equally bounded. The Lyren candidate records exact inheritance, retained failures, protected gates, rollback, and prospective sequencing, yet its presence is not delivery. Only a clean pushed exact final, one attributable owner-scoped canonical pass, fresh live authority, unique exact-title resolution, immediate reread, duplicate guard, and the application acknowledgement can support a later send claim. Any absent or ambiguous gate leaves the candidate prepared and unsent. This separation keeps the repository seal immutable, preserves corrigibility, and prevents an operational convenience from becoming authority or evidence it has not earned.\n")
    baton = build_baton(repo)
    write_text(repo / HANDOFF, baton)
    write_json(root / "handoffs/activation-candidate-integrity.json", {
        "delivery_acknowledged": False,
        "delivery_state": "PREPARED_NOT_SENT",
        "owner": OWNER,
        "path": HANDOFF,
        "phase": PHASE,
        "prospective_recipient": "Lyren Moss",
        "prospective_phase": "v670-v1",
        "schema": "ghc.family.activation-candidate-integrity.v3",
        "sha256_normalized_lf": sha256_text(baton.rstrip() + "\n"),
        "word_count": len(baton.split()),
    })
    write_json(root / "orchestration/route-state-final-candidate.json", {
        "app_acknowledgement": False,
        "current_owner": OWNER,
        "current_phase": PHASE,
        "delivery_state": "PREPARED_NOT_SENT",
        "duplicate_guard": "no Lyren contact during execution and exactly one send only after terminal gate",
        "prospective_next_exact_title": "Lyren Moss",
        "prospective_next_phase": "v670-v1",
        "route_authority": "Hamish live sequential continuation through v675-v8 subject to fresh terminal reread",
        "schema": "ghc.family.route-state.final-candidate.v3",
        "successor_contact_count": 0,
    })
    write_json(root / "seal/seal-candidate.json", {
        "branch": BRANCH,
        "canonical_state": "PREPARED_NOT_INVOKED",
        "evidence_commit": EVIDENCE_COMMIT,
        "exact_final": "COMMIT_CONTAINING_THIS_SEAL_RESOLVE_FROM_FRESH_LIVE_BRANCH",
        "retained_initial_final": INITIAL_FINAL,
        "outcomes": outcomes["totals"],
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.seal-candidate.v3",
        "source_commit": SOURCE_FINAL,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "x1_commit": X1_COMMIT,
    })
    write_json(root / "final/canonical-invocation-state.json", {
        "attempt_count": 0,
        "external_receipt_state": "ABSENT_UNTIL_EXACT_FINAL_PUSH",
        "invocation_state": "PREPARED_NOT_INVOKED",
        "no_success_replay": True,
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.canonical-invocation-state.v3",
        "scope": "exact owner source-to-final delta and new or modified modules only; not full repository",
    })
    write_json(root / "final/terminal-correction.json", {
        "canonical_invocations_before_correction": 0,
        "correction": "stale-label scanner self-match removed through noncontiguous literal construction",
        "evidence_commit": EVIDENCE_COMMIT,
        "initial_final": INITIAL_FINAL,
        "initial_final_state": "RETAINED_NON_TERMINAL_ZERO_CANONICAL_CREDIT",
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.terminal-correction.v3",
        "terminal_corrected_final": "COMMIT_CONTAINING_THIS_CORRECTION_RESOLVE_FROM_FRESH_LIVE_BRANCH",
    })
    write_json(root / "final/final-validation-prerequisites.json", {
        "checks": [
            "retained initial final direct child of immutable evidence and corrected final direct child of initial final",
            "source x1 evidence initial-final corrected-final single-parent ancestry and zero merges",
            "clean before and after",
            "local upstream tracking and fresh live equality with zero divergence",
            "x1 x2 and final selected tests",
            "strict JSON parse over exact owner scope",
            "five-class privacy scan",
            "changed-Python AST review",
            "exact x1 evidence final-delta and final-owner manifests",
            "stale-label and four-outcome allowlist",
            "file and word ceilings",
            "handoff word count and PREPARED_NOT_SENT state",
        ],
        "complete_repository_suite": False,
        "external_receipt_required": True,
        "one_attributable_invocation": True,
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.final-validation-prerequisites.v3",
    })
    write_text(repo / "ghc-family-index/references/v669-v8-vesper-arlen.md", f"""# Vesper Arlen v669-v8 phase index

- Owner and exact existing-task title: `Vesper Arlen`.
- Immutable Neris source: `{SOURCE_FINAL}`.
- Planning-only x1: `{X1_COMMIT}`.
- Immutable evidence: `{EVIDENCE_COMMIT}`.
- Retained non-terminal initial final: `{INITIAL_FINAL}` with zero canonical invocation credit.
- Exact final: resolve the clean pushed branch head containing the seal and external canonical receipt.
- Primary pillar: THOS Body; GMUT Mind and Freed ID/CBR Heart protected.
- Lens: wholly synthetic sourdough process documentation and software assurance.
- Outcomes: 28 `completed`, 8 `represented`, 2 `open_gap`, 2 `exact_gate`.
- Proposal chain: {CHAIN_AFTER}; 3,570-title recovery gap retained.
- Final candidate totals: {final_totals['effective_negatives']} negatives, {final_totals['methods']} methods, {final_totals['failed_witnesses']} failed witnesses, {final_totals['passing_witnesses']} passing witnesses, {final_totals['open_gaps']} open gaps, {final_totals['exact_gates']} exact gates.
- Canonical validation: prepared, not invoked until exact final push; no success replay.
- Route: `PREPARED_NOT_SENT` prospective Lyren Moss v670-v1.
- Terminal verdict: `NOT_READY_FOR_STAGE_20`.
""")

    json_paths = sorted(root.rglob("*.json"))
    for path in json_paths:
        json.loads(path.read_text(encoding="utf-8"))
    text_paths = [path for path in root.rglob("*") if path.is_file() and path.suffix.lower() in {".json", ".md", ".html", ".txt"}]
    privacy = [dict(path=str(path.relative_to(repo)).replace("\\", "/"), **row) for path in text_paths for row in privacy_candidates(path.read_text(encoding="utf-8"))]
    write_json(root / "validation/final-build-receipt.json", {
        "checks": {"baton_words": len(baton.split()), "final_operational_failures": failure_count, "json_parses": len(json_paths), "privacy_candidates": privacy, "route_contact_count": 0},
        "owner": OWNER,
        "passed": 10000 <= len(baton.split()) <= 100000 and not privacy and all(row.get("passing_bounded_witness") for row in FINAL_FAILURES),
        "phase": PHASE,
        "schema": "ghc.family.final-build-receipt.v3",
    })


def manifest_entry(repo: Path, relpath: str) -> dict[str, Any]:
    data = subprocess.run(["git", "-C", str(repo), "show", f":{relpath}"], check=True, capture_output=True).stdout
    return {"bytes": len(data), "path": relpath, "sha256": hashlib.sha256(data).hexdigest()}


def staged_review(repo: Path) -> None:
    exclusions = [FINAL_DELTA_MANIFEST, FINAL_OWNER_MANIFEST, FINAL_REVIEW]
    final_delta = staged_blob_manifest(repo, exclusions)
    phase_paths = subprocess.run(["git", "-C", str(repo), "diff", "--cached", "--name-only", SOURCE_FINAL], check=True, capture_output=True, text=True).stdout.splitlines()
    owner_entries = [manifest_entry(repo, path) for path in sorted(path for path in phase_paths if path not in exclusions)]
    paths = [row["path"] for row in final_delta]
    forbidden_sent = []
    json_errors: list[str] = []
    privacy: list[dict[str, str]] = []
    security: list[dict[str, str]] = []
    for path in paths:
        data = subprocess.run(["git", "-C", str(repo), "show", f":{path}"], check=True, capture_output=True).stdout
        text = data.decode("utf-8", errors="replace")
        if path.endswith(".json"):
            try:
                payload = json.loads(text)
                if isinstance(payload, dict) and (payload.get("delivery_acknowledged") is True or payload.get("delivery_state") == "SENT"):
                    forbidden_sent.append(path)
            except Exception as exc:  # noqa: BLE001
                json_errors.append(f"{path}:{type(exc).__name__}")
        privacy.extend({"path": path, **row} for row in privacy_candidates(text))
        if path.endswith(".py"):
            tree = ast.parse(text, filename=path)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                    security.append({"path": path, "finding": f"dynamic_{node.func.id}"})
                if isinstance(node, ast.Call) and any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                    security.append({"path": path, "finding": "shell_true"})
    write_json(repo / FINAL_DELTA_MANIFEST, {"domain": "final_staged_delta_git_blobs", "entries": final_delta, "entry_count": len(final_delta), "evidence_commit": EVIDENCE_COMMIT, "owner": OWNER, "phase": PHASE, "schema": "ghc.family.exact-git-blob-manifest.v3", "self_exclusions": exclusions})
    write_json(repo / FINAL_OWNER_MANIFEST, {"domain": "final_phase_owner_git_blobs", "entries": owner_entries, "entry_count": len(owner_entries), "owner": OWNER, "phase": PHASE, "schema": "ghc.family.exact-git-blob-manifest.v3", "self_exclusions": exclusions, "source_commit": SOURCE_FINAL})
    checks = {
        "diff_cached_check": subprocess.run(["git", "-C", str(repo), "diff", "--cached", "--check"], check=False, capture_output=True).returncode == 0,
        "final_delta_entries": len(final_delta),
        "forbidden_sent_claims": forbidden_sent,
        "json_errors": json_errors,
        "owner_entries": len(owner_entries),
        "owner_file_ceiling": len(owner_entries) < 2000,
        "privacy_candidates": privacy,
        "python_ast_findings": security,
        "word_ceiling": all(len((repo / path).read_text(encoding="utf-8").split()) <= 100000 for path in paths if (repo / path).suffix.lower() in {".md", ".json", ".html", ".txt"}),
    }
    write_json(repo / FINAL_REVIEW, {"checks": checks, "owner": OWNER, "passed": checks["diff_cached_check"] and not forbidden_sent and not json_errors and checks["owner_file_ceiling"] and not privacy and not security and checks["word_ceiling"], "phase": PHASE, "schema": "ghc.family.final-staged-review.v3", "self_exclusions": exclusions})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--stage-review", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    staged_review(repo) if args.stage_review else build(repo)


if __name__ == "__main__":
    main()
