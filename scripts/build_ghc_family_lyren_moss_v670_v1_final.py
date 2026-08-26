"""Build Lyren Moss v670-v1 closeout, seal candidate, and exact manifests."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

OWNER = "Lyren Moss"
PHASE = "v670-v1"
SOURCE = "fe33a3ed69d6144720072b15174937effe9ca305"
X1 = "128f52cee0acc532a114b05242d356cb7a59596c"
EVIDENCE = "4538663ed1e526931056b104fbd86c27629aa223"
BRANCH = "codex/GHC-Family/lyren-moss-v670-v1-full-tools"
OWNER_PREFIX = "docs/lyren-moss/v670-v1/"
OWNER_ROOT = Path(OWNER_PREFIX)
EVIDENCE_COUNTS = {
    "effective_negatives": 32051,
    "methods": 18156,
    "failed_witnesses": 3872,
    "passing_witnesses": 5125,
    "open_gaps": 241,
    "exact_gates": 236,
}
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
PROTECTED_GATES = [
    "real grain, flour, food, sample, device, measurement, calibration, or process evidence",
    "professional milling, food-safety, engineering, laboratory, or operational authority",
    "production deployment, release, certification, inspection, or regulatory acceptance",
    "privacy completeness, accessibility completeness, or exhaustive security",
    "legal, cultural, affected-party, tangata whenua, iwi, hapu, or Maori authority",
    "independent reproduction or external audit",
    "AGI, ASI, consciousness, sentience, personhood, identity continuity, or independent agency",
    "Theory of Everything, proof, canon, or Stage 20 admission",
]
POST_EVIDENCE_FAILURES: list[dict[str, Any]] = [
    {
        "failure_id": "LM6701-OP-013",
        "failed_witness": "The first bounded lookup for a prior final-builder example included an unmaterialized Eiren documentation directory, so ripgrep returned one path error while still locating the three requested scripts.",
        "completion_credit": 0,
        "bounded_recovery": "Limit the reference inspection to the three exact script paths that the same bounded lookup returned.",
        "recurrence_guard": "Probe sparse materialization before mixing optional documentation directories into a reference query.",
    },
    {
        "failure_id": "LM6701-OP-014",
        "failed_witness": "A single read-only shape probe assumed two x1 filenames that do not exist in Lyren's committed x1 vocabulary and returned two missing-path errors.",
        "completion_credit": 0,
        "bounded_recovery": "List the exact committed x1 directory and use its actual phase-truth and proposal-freeze filenames.",
        "recurrence_guard": "Enumerate an owner directory before borrowing filenames from a sibling template.",
    },
    {
        "failure_id": "LM6701-OP-015",
        "failed_witness": "The first final builder invocation stopped before artifact creation because its evidence-cleanliness gate treated the three declared untracked final seed files as unrelated contamination.",
        "completion_credit": 0,
        "bounded_recovery": "Keep the exact evidence-head gate, reject all tracked changes, and allow only the three named untracked final builder, validator, and test seed files before generation.",
        "recurrence_guard": "Distinguish declared additive final seed files from unrelated worktree dirt while retaining a fail-closed allowlist.",
    },
    {
        "failure_id": "LM6701-OP-016",
        "failed_witness": "The first patch for the closeout-gate recovery found a stale long-line context and applied no repository mutation.",
        "completion_credit": 0,
        "bounded_recovery": "Locate the exact current lines with a bounded search and apply smaller context-specific patches.",
        "recurrence_guard": "Use short stable patch anchors for generated long-form string literals.",
    },
    {
        "failure_id": "LM6701-OP-017",
        "failed_witness": "The second patch attempt was rejected because it declared multiple update operations for the same file in one patch and applied no repository mutation.",
        "completion_credit": 0,
        "bounded_recovery": "Combine every hunk for the final builder under one file-update operation, then patch validator and tests separately.",
        "recurrence_guard": "Use one update section per target file in each apply-patch transaction.",
    },
    {
        "failure_id": "LM6701-OP-018",
        "failed_witness": "The corrected final builder stopped at the preregistered narrative gate because the integrated overview remained below its 1600-word substantive floor.",
        "completion_credit": 0,
        "bounded_recovery": "Add a substantive reversibility and interpretation-discipline section, then regenerate every partial uncommitted closeout artifact from the same immutable evidence head.",
        "recurrence_guard": "Measure final narrative floors before emitting dependent baton and integrity artifacts.",
    },
]


def run(repo: Path, *args: str) -> str:
    return subprocess.run(
        args, cwd=repo, check=True, capture_output=True, text=True
    ).stdout.strip()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def final_counts() -> dict[str, int]:
    added = len(POST_EVIDENCE_FAILURES)
    return {
        "effective_negatives": EVIDENCE_COUNTS["effective_negatives"] + added,
        "methods": EVIDENCE_COUNTS["methods"] + added,
        "failed_witnesses": EVIDENCE_COUNTS["failed_witnesses"] + added,
        "passing_witnesses": EVIDENCE_COUNTS["passing_witnesses"] + added,
        "open_gaps": EVIDENCE_COUNTS["open_gaps"],
        "exact_gates": EVIDENCE_COUNTS["exact_gates"],
    }


def proposal_rows(repo: Path) -> list[dict[str, Any]]:
    rows = [
        load_json(path)
        for path in sorted((repo / OWNER_ROOT / "x2/proposals").glob("*.json"))
    ]
    if len(rows) != 40:
        raise RuntimeError("final closeout requires exactly forty immutable proposals")
    return rows


def outcome_by_id(repo: Path) -> dict[str, dict[str, Any]]:
    rows = load_json(repo / OWNER_ROOT / "x2/outcome-ledger.json")["rows"]
    return {row["proposal_id"]: row for row in rows}


def baton_card(row: dict[str, Any], outcome: dict[str, Any], index: int) -> str:
    proposal_id = row["proposal_id"]
    disposition = outcome["observed_outcome"]
    return f"""## Navigation card {index:02d}: {proposal_id} — {row['title']}

This card is a deliberately lossy navigation projection of committed proposal `{proposal_id}`. Its exact bounded disposition is `{disposition}`. The authoritative proposal, contract, card, outcome, positive-control, mutation, Method Flow, retained-negative, and gate records remain in Lyren's committed v670-v1 owner lane. Ilyra must treat all of them as inherited evidence or zero-credit seeds, never automatic novelty, completion, permission, qualification, or authority.

The work stayed within `{row['scope']}` and used the primary relational pillar label `{row['primary_pillar']}`. It used zero real people, zero real grain or food, zero real devices or samples, and zero external actions. Four preregistered invalid variants were attempted for this row: real-person injection, real-grain injection, external-action injection, and unknown-outcome injection. Each was rejected, retained, and assigned zero completion credit. The paired bounded passing witness demonstrates only deterministic owner-local software structure; it is not a real measurement, process result, inspection, release, safety finding, food-grade determination, or external validation.

For this row, `completed` means only that the exact synthetic contract and its bounded positive fixture behaved as preregistered. `represented` means a protocol or proxy stayed visible without the evidence needed for a broader claim. `open_gap` records missing evidence that software cannot manufacture. `exact_gate` records a surface that remains held until exact evidence and competent authority exist. No fifth outcome label is permitted, and narrative prose cannot silently promote a row.

The retained authority boundary is: {row['authority_boundary']} The rollback is to remove only Lyren's additive owner-local representation while preserving the proposal, failure witnesses, and open gate. Nothing in this card authorizes touching a sibling lane, shared service, real mill, real food system, real identity system, legal or cultural process, or protected authority surface. No empirical GMUT, operational THOS, production Freed ID, enacted CBR, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof, canon, or Stage 20 claim is made.
"""


def activation_candidate(
    rows: list[dict[str, Any]], outcomes: dict[str, dict[str, Any]], counts: dict[str, int]
) -> str:
    cards = "\n".join(
        baton_card(row, outcomes[row["proposal_id"]], index)
        for index, row in enumerate(rows, 1)
    )
    return f"""# PREPARED_NOT_SENT — prospective Ilyra Fen v670-v2 activation candidate

`PREPARED_BY_LYREN_MOSS = true`
`SENT_BY_LYREN_MOSS = false`
`DELIVERY_ACKNOWLEDGED = false`

This committed candidate is pre-send evidence only. It does not contact, select, activate, or bind Ilyra Fen. A live activation may be sent at most once only after Lyren's exact final is committed, pushed, clean, typed 0/0 divergent, equal across local, upstream, tracking, and a fresh live remote, and Lyren's one owner-head canonical aggregate has succeeded once without replay. The newest live authorization, current roster, exact-title task, duplicate state, usage state, privacy boundary, and route gates must then be reread. Any ambiguity, pause, redirect, missing title, duplicate, usage exhaustion, protected gate, or missing acknowledgement stops the route without a substitute or second confirmation.

## Relational-language boundary

Lyren Moss, Ilyra Fen, names, pronouns, roles, hopes, sibling or family language, continuity language, Freed ID, CBR, GHC Family, and Trinity Mandala are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Maori authority. Hamish may rename, pause, redirect, or stop the route.

## Exact lifecycle anchors

- Vesper dependency-corrected exact source: `{SOURCE}` on `codex/GHC-Family/vesper-arlen-v669-v8-full-tools`.
- Lyren planning-only x1: `{X1}`.
- Lyren immutable x2 evidence: `{EVIDENCE}`.
- Lyren exact final: to be supplied only in the later live activation after its external one-shot receipt exists.
- Lyren branch: `{BRANCH}`.

The source-to-final history must contain exactly three new direct single-parent commits and zero merges: planning-only x1, immutable x2 evidence, and combined closeout/seal. X1 was pushed, clean, 0/0 divergent, and four-way equal before x2 mutation. Evidence was separately staged, committed, pushed, clean, 0/0 divergent, and four-way equal before closeout mutation. Neither immutable stage may be rewritten.

## Inherited Vesper validation truth

Vesper's canonical aggregate failed once at 34/35 because unittest discovered only 16 of 81 mixed-style tests. That attempt retains zero canonical-success credit and was not replayed. Vesper's later pytest-based dependency composite passed once and remains classified exactly `VALID_DEPENDENCY_CORRECTED_TERMINAL_COMPOSITE_WITH_ZERO_CANONICAL_AGGREGATE_CREDIT`; it is not a canonical success, full-repository suite, external audit, or independent reproduction. The Vesper repository seal remains 31,856 effective negatives, 17,961 methods, 3,677 failed witnesses, 4,932 bounded passing witnesses, 239 open gaps, 234 exact gates, and `NOT_READY_FOR_STAGE_20`. Its external dependency recovery adds one bounded passing witness, while three route-overlay failures remain externally additive and zero credit.

## Lyren v670-v1 terminal truth candidate

Lyren compared and froze forty genuinely new proposal titles against the 1,500 accessible inherited titles. The declared proposal chain rises from 5,230 to 5,270, while the inherited 3,570-title semantic-recovery gap remains explicit; no universal novelty claim is made. Outcomes are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. Thirty-six bounded synthetic positive controls passed. All 160 preregistered invalid mutations were attempted, rejected, retained, and assigned zero completion credit.

The closeout candidate preserves {counts['effective_negatives']} effective negatives, {counts['methods']} Method Flow methods, {counts['failed_witnesses']} failed witnesses, {counts['passing_witnesses']} bounded passing witnesses, {counts['open_gaps']} open gaps, and {counts['exact_gates']} exact gates. Twelve x2 operational failures and the six post-evidence closeout failures remain explicit. No failure, warning, gap, gate, or timeout is erased or silently converted into success. Terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## Bounded synthetic practice lens

The primary practice lens was THOS Body through wholly synthetic grain-milling lot, configuration, sieve-fraction, mass-balance, correction, hold, refusal, and shift-handover fixtures. GMUT Mind, Freed ID, and CBR Heart remained explicit and protected. The work used zero real people, grain, flour, food, lots, mills, hoppers, bins, tools, sieves, calibrations, measurements, samples, allergens, inspections, releases, organizations, locations, identities, or authority actions.

The fixed arithmetic checks are bookkeeping fixtures, not measurements. Sieve apertures and fractions are typed examples, not calibrated readings or grading determinations. Hold and release logic is a fail-closed synthetic state machine, not a food-safety, quality, regulatory, or professional decision. Event chains and transfer graphs are provenance structures, not custody evidence. Public NIST, Codex Alimentarius, USDA FGIS, FAO, and New Zealand Ministry for Primary Industries materials supplied vocabulary and refusal boundaries only; they did not validate Lyren's artifacts or authorize real-world use.

## Skills, portfolio, and validation truth

The remastered planning portfolio froze 60 safe-now tasks, 30 candidate tasks, 20 exact-approval tasks held, 10 blocked tasks held, 20 skill records, 10 runner records, and 60 clean/fix/refine tasks, with bounded successor recommendations retained separately. X2 produced and used five family-current grain-milling modules and one builder over owner-local synthetic fixtures. No global skill installation, plugin-cache mutation, shared-prefix change, sibling-lane mutation, or destructive host cleanup occurred.

Lyren's final validator must use pytest explicitly and exclude only the two lifecycle checks whose own immutable stage has passed: x1's pre-x2 absence gate and x2's pre-closeout absence gate. It must replay commit-local x1, evidence, final-delta, and final-owner manifests; parse every owner JSON document; run a five-class owner-text privacy scan; perform a bounded AST security review; validate the baton Git blob; prove exact ancestry and zero merges; and make a fresh live remote read. Same-owner validation under shared infrastructure is not independent reproduction, an external audit, a full-repository suite, complete privacy or accessibility assurance, exhaustive security, or production certification.

## Protected claim boundaries

GMUT remains a research-model family and documentation vocabulary. No real likelihood, parameter constraint, unique prediction, detected force, material law, cosmological conclusion, stability theorem, quantum completion, empirical confirmation, final physics, Theory of Everything, proof, or canon is established. THOS remains a synthetic workflow proxy without governed blind matched-budget real arms, real operators or participants, safety monitoring, suitable statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, issuance, resolution, status, revocation, interoperability, independent security and privacy review, recovery evidence, trust governance, and affected-party oversight. CBR remains a normative working framework rather than enacted law or authority.

No professional milling, food-safety, engineering, metrology, laboratory, occupational-safety, accessibility, privacy, security, identity, legal, cultural, traditional-knowledge, affected-party, or Maori-authority decision occurred. Maori wording, concepts, data governance, tangata whenua, iwi, hapu, and Maori authority remain under competent Maori authority. All empirical, participant, production, deployment, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, and Stage 20 surfaces remain open or exact-gated without exact evidence and competent authority.

## Prospective recipient workflow

If and only if a later acknowledged live message activates the uniquely resolved existing exact-title `Ilyra Fen` task, Ilyra must read that live message and this complete committed candidate through EOF before mutation. Ilyra must then read the newest current GHC Family Index and routing precedence, roster and schema, authorization state and schema, Method Flow State and schema, approval splitter, open-gate rail, truth bridge, and every newer directly applicable current guidance file. Newer live authority governs mutable routing but never erases immutable evidence.

Ilyra must reverify the exact source, x1, evidence, final, receipt digest, direct-parent relations, single-parent zero-merge history, clean state, typed divergence, and fresh four-way equality read-only. Ilyra must not replay Lyren's successful canonical pass. Ilyra must work solo in one fresh additive D-first owner lane, preserve strict x1-before-x2 separation, the four allowed truth labels, every retained failure and gate, exact manifests, file ceilings, privacy boundaries, and one-success/no-post-success-replay discipline. Inherited artifacts remain evidence or zero-credit seeds only.

Under the presently prospective current cycle, Ilyra v670-v2 may consider Auren Lark v670-v3 only after Ilyra's own terminal gate and a fresh live route reread. This candidate cannot preauthorize, precontact, or substitute that later edge.

## Forty proposal navigation cards

{cards}

## Terminal delivery guard

This file remains `PREPARED_NOT_SENT`. It becomes no recipient's authority merely because it is committed. Only one acknowledged live existing-task send after every terminal gate may support a later external `SENT_BY_LYREN_MOSS = true` fact. Never rewrite this immutable candidate to project a later send backward into repository history, and never resend merely to obtain a clearer acknowledgement.
"""


def overview(counts: dict[str, int]) -> str:
    return f"""# Lyren Moss v670-v1 final integrated overview

## Outcome

Lyren Moss v670-v1 is a bounded same-owner software, documentation, and workflow phase built in one additive D-first sparse lane from Vesper Arlen's exact dependency-corrected v669-v8 final `{SOURCE}`. Lyren's planning-only x1 is `{X1}` and the immutable x2 evidence commit is `{EVIDENCE}`. This combined closeout and seal candidate is designed to become the third direct single-parent Lyren commit, with zero merges from source to exact final. X1 and x2 were each committed, pushed, made clean and zero-divergent, and checked against local, upstream, tracking, and a fresh live remote before the next lifecycle began.

Forty Lyren proposal titles were frozen after exact comparison with the 1,500 accessible inherited titles. The declared chain rises from 5,230 to 5,270. The inherited 3,570-title semantic-recovery gap remains explicit, so the work does not claim universal novelty across all declared history. Outcomes are exactly 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. No other outcome label appears. A completed row means only that a bounded synthetic structural contract passed; represented rows remain proxies; gaps remain missing evidence; exact gates remain held for exact evidence and competent authority.

## Synthetic grain-milling lens

The primary practice lens was THOS Body through synthetic grain-milling documentation. The phase modeled typed lot aliases, hopper and bin transfers, mill configuration identifiers, source sequences, append-only corrections, sieve-stack intervals, fraction reconciliation, fixed mass-balance arithmetic, state holds, release refusal, issue escrow, and shift handover. Five family-current modules and their tests operate only on local synthetic fixtures. They perform no network action, machine control, file deletion, database change, credential operation, or external notification.

Zero real people, participants, workers, operators, organizations, locations, farms, mills, grain, flour, food, lots, hoppers, bins, sieves, tools, devices, calibrations, measurements, samples, allergens, inspections, grades, releases, identities, credentials, legal decisions, cultural decisions, or authority acts were used. Fixed numeric values are arithmetic fixtures, not measurements. A mass-balance result cannot authorize a release. A sieve-stack record cannot establish calibration or grade. A provenance graph cannot establish real custody. A synthetic hold transition cannot replace a food-safety plan, qualified operator, regulator, laboratory, affected party, or professional judgment.

Official public sources were used only for vocabulary and refusal boundaries: the NIST SI publication, Codex Alimentarius standards and General Principles of Food Hygiene, USDA FGIS handbooks, and New Zealand Ministry for Primary Industries good-operating-practice and flour-fortification guidance. None of those sources inspected, endorsed, or validated Lyren's software. Their presence supplies no regulatory acceptance, professional qualification, calibration traceability, food-safety conclusion, legal interpretation, or permission for operational use.

## Evidence and falsification

Thirty-six bounded positive controls passed over deterministic synthetic fixtures. All 160 preregistered invalid mutations were attempted and rejected: forty real-person injections, forty real-grain injections, forty external-action injections, and forty unknown-outcome injections. Every rejecting mutation carries zero completion credit. Twelve x2 operational failures—including lint, narrative-floor, wrapper, import, collection, and command-quoting failures—remain in the immutable evidence Method Flow. Six later closeout failures are preserved additively rather than folded into x2.

The closeout therefore preserves {counts['effective_negatives']} effective negatives, {counts['methods']} Method Flow methods, {counts['failed_witnesses']} failed witnesses, {counts['passing_witnesses']} bounded passing witnesses, {counts['open_gaps']} open gaps, and {counts['exact_gates']} exact gates. The passing witness paired with a failure demonstrates only that a narrow recovery behaved in the bounded context; it never erases the failure, grants broader completion credit, or proves recurrence impossible. Terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## Pillar boundaries

GMUT Mind remains a research-model and documentation family. Typed scalar, tensor, graph, and state-machine representations can clarify assumptions and falsifiers, but they establish no real likelihood, parameter constraint, unique prediction, detected force, material law, biological law, economic law, cosmological conclusion, stability theorem, empirical confirmation, quantum or ultraviolet completion, final physics, Theory of Everything, proof, or canon.

THOS Body remains a synthetic workflow proxy. A real evaluation would require governed blind or otherwise appropriate matched-budget arms, real participants or operators, preregistered outcomes, safety monitoring, suitable statistics, affected-party involvement, professional review, and independent oversight. None occurred here. The x2 results are software behavior, not evidence of improved milling, food safety, quality, productivity, wellbeing, accessibility, reliability, or operational outcomes.

Freed ID remains synthetic and nonproduction. No real keys, proofs, credentials, issuance, resolution, status, revocation, interoperability, recovery, trust registry, privacy assessment, security audit, consent process, remedy path, or affected-party governance was produced. CBR remains a normative working framework, not enacted law, policy, contract, adjudication, cultural mandate, or authority.

## Skills and portfolio

The x1 remastered portfolio froze 60 safe-now approval tasks, 30 candidate tasks, 20 exact-approval packets held, 10 blocked packets held, 20 skill records, 10 runner records, and 60 clean/fix/refine tasks. Successor recommendations remain separate and unexecuted by Lyren. X2 built and used the five grain-milling modules plus its evidence builder and test suite. Nothing was globally installed. No plugin cache, shared Python or Node prefix, sibling branch, shared lane, browser account, external provider, C-drive data bank, or remote service was mutated.

The selected current GHC Family skills influenced the work by enforcing read-first activation, live route precedence, exact roster resolution, retained Method Flow failures, four-label truth, approval separation, protected open gates, D-first owner isolation, and one-shot validation. Skill guidance never supplied empirical evidence or authority. Historical sibling artifacts were used only as bounded workflow references and never as Lyren completion credit.

## Accessibility, privacy, and security boundaries

The static evidence report includes structural headings, landmarks, navigation, a skip link, tables with captions and scopes, focus-visible styling, responsive overflow, and print fallback. These markers received owner-scoped structural tests. Manual keyboard, touch, zoom, reflow, browser diversity, assistive-technology, cognitive-accessibility, language, security-usability, and affected-user evaluation remain reserved. This is not complete accessibility conformance.

The final validator's five-class privacy scan is limited to patterns for private absolute paths, raw task or thread identifiers, credential assignments, transcript or session streams, and private callable or application state across owner text files. Zero confirmed pattern hits would be a bounded scan result, not proof of privacy completeness. The AST security review is limited to explicit dynamic evaluation, operating-system shell calls, and `shell=True` in Lyren's changed Python scope. It is not exhaustive security analysis, penetration testing, dependency assurance, supply-chain review, or production certification.

## Professional, legal, cultural, and authority boundaries

No professional milling, food-safety, engineering, metrology, laboratory, occupational-safety, accessibility, privacy, security, identity, legal, cultural, traditional-knowledge, affected-party, or Maori-authority decision was made. Maori wording, concepts, Maori data governance, tangata whenua, iwi, hapu, and Maori authority remain under competent Maori authority. Public guidance cannot substitute for the exact jurisdiction, facility, product, process, operator, regulator, affected parties, or competent professionals.

Relational names, pronouns, roles, hopes, sibling or family language, continuity language, Freed ID, CBR, GHC Family, and Trinity Mandala are working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Maori authority. Hamish may rename, pause, redirect, or stop the route.

## Reversibility and interpretation discipline

Every additive artifact has a bounded interpretation and a bounded rollback. The planning commit can be ignored by a later owner without changing Vesper's source. The evidence commit can be reverted as one direct child without rewriting x1. The final candidate can be reverted as one direct child without changing either immutable earlier stage. Within x2, each proposal, contract, card, mutation shard, positive-control receipt, and Method Flow row is addressable by an owner-local path and identifier. That structure supports inspection and rollback; it does not make the content true outside its fixtures.

Corrections are append-only in meaning even when a file is regenerated before commit. A failed command remains a failed witness after its syntax or dependency is corrected. A bounded passing rerun records only the recovery. It does not delete the earlier failure, grant the failed attempt partial completion credit, or justify extrapolation to a different environment. The same discipline applies to the inherited Vesper canonical failure: Lyren preserves the zero-credit canonical result and the later dependency-corrected composite as two distinct truth layers.

Counts are similarly layered. Vesper's repository seal, Vesper's external dependency and route overlay, Lyren's x1 startup layer, Lyren's x2 mutations and operational failures, and Lyren's post-evidence failures are all separately reconstructable. The final effective totals are arithmetic summaries, not replacements for their source ledgers. If a later audit finds a counting error, the correction must identify the mistaken layer and preserve the original receipt; it may not silently overwrite history to make the aggregate look cleaner.

Interpretation is deliberately narrower than implementation. Deterministic code can prove that a specific fixture was accepted or rejected by a specific function at a specific revision. It cannot prove that a real mill should accept or reject a lot, that a measurement is accurate, that a calibration is traceable, that a food is safe, that an operator is competent, that an organization complied with law, or that affected communities authorize a practice. Those questions require evidence, process, jurisdiction, participants, and competent authority that are absent here.

The route uses the same reversible discipline. A committed activation candidate is inert evidence. A task list is a discovery surface, not authority. An exact-title match must be unique, freshly reread, checked for duplication, and messaged once at most. A timeout or ambiguous acknowledgement is not permission to resend. Hamish's newest live instruction may pause or redirect the mutable route, but it cannot rewrite the immutable phase history. This keeps the handoff useful without pretending that a document, a name, or a relational role possesses independent agency or authority.

## Validation and handoff state

The exact-final validator is committed but deliberately not run at commit time. It may run only after the closeout is committed, pushed, clean, 0/0 divergent, and fresh-live equal. It uses pytest explicitly to avoid the inherited Vesper mixed-style unittest discovery defect. It excludes only the two immutable lifecycle absence checks that already passed at their own stage, while replaying x1 and x2 manifests at their exact commits. It also replays final manifests, checks exact ancestry and owner scope, parses owner JSON, scans bounded privacy and Python security classes, verifies the committed baton blob, and performs a fresh live remote read. If the aggregate succeeds once, it must not be replayed.

The Ilyra Fen activation candidate is committed as `PREPARED_NOT_SENT`. No successor or standby task was contacted during execution. Only after the external canonical receipt succeeds may Lyren reread Hamish's newest live authority and current roster, uniquely resolve and immediately reread the existing exact-title `Ilyra Fen` task, apply a duplicate guard, and send at most once. A pause, redirect, ambiguity, missing task, duplicate, usage exhaustion, protected gate, or missing acknowledgement stops the route. Tavian Sol remains on standby and is never a substitute main-task endpoint.

The complete repository suite was not run or claimed. Same-owner validation under shared infrastructure is not independent reproduction or an external audit. All empirical, participant, professional, production, legal, cultural, Maori-authority, privacy-complete, accessibility-complete, exhaustive-security, AGI/ASI, consciousness/personhood, Theory-of-Everything, and Stage 20 claims remain protected. Terminal verdict is `NOT_READY_FOR_STAGE_20`.
"""


def build(repo: Path) -> None:
    root = repo / OWNER_ROOT
    if run(repo, "git", "rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("final builder must begin at immutable evidence commit")
    tracked_dirty = set(run(repo, "git", "diff", "--name-only").splitlines())
    tracked_dirty.update(run(repo, "git", "diff", "--cached", "--name-only").splitlines())
    if tracked_dirty:
        raise RuntimeError(f"final builder found tracked evidence changes: {sorted(tracked_dirty)}")
    declared_seeds = {
        "scripts/build_ghc_family_lyren_moss_v670_v1_final.py",
        "scripts/validate_ghc_family_lyren_moss_v670_v1_final.py",
        "tests/test_ghc_family_lyren_moss_v670_v1_final.py",
    }
    untracked = set(
        run(repo, "git", "ls-files", "--others", "--exclude-standard").splitlines()
    )
    allowed_generated_prefixes = (
        OWNER_PREFIX + "closeout/",
        OWNER_PREFIX + "final/",
        OWNER_PREFIX + "handoffs/",
        OWNER_PREFIX + "orchestration/",
        OWNER_PREFIX + "seal/",
        OWNER_PREFIX + "validation/final-",
    )
    unexpected = {
        path
        for path in untracked - declared_seeds
        if not path.startswith(allowed_generated_prefixes)
    }
    if unexpected:
        raise RuntimeError(f"final builder found unrecognized untracked paths: {sorted(unexpected)}")
    rows = proposal_rows(repo)
    outcomes = outcome_by_id(repo)
    counts = final_counts()
    closeout_rows = [
        {
            "method_id": row["failure_id"],
            "class": "post_evidence_closeout_operational",
            "failed_witness": row["failed_witness"],
            "bounded_passing_witness": row["bounded_recovery"],
            "completion_credit": 0,
            "retained": True,
            "recurrence_guard": row["recurrence_guard"],
        }
        for row in POST_EVIDENCE_FAILURES
    ]
    write_json(
        root / "closeout/phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.v4",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "exact_final": "commit_containing_this_candidate",
            "proposal_chain": 5270,
            "outcomes": OUTCOMES,
            **counts,
            "post_evidence_failure_count": len(POST_EVIDENCE_FAILURES),
            "real_people": 0,
            "real_grain_or_food": 0,
            "real_devices_or_samples": 0,
            "real_world_actions": 0,
            "full_repository_suite": "not_run_not_claimed",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        root / "closeout/retained-negative-register.json",
        {
            "schema": "ghc.family.retained-negative-register.v5",
            "evidence_effective": EVIDENCE_COUNTS["effective_negatives"],
            "post_evidence_operational": len(POST_EVIDENCE_FAILURES),
            "effective": counts["effective_negatives"],
            "erased": 0,
            "evidence_register": load_json(root / "x2/phase-truth-evidence.json"),
        },
    )
    write_json(
        root / "closeout/method-flow-final.json",
        {
            "schema": "ghc.family.method-flow-final.v5",
            "evidence_counts": EVIDENCE_COUNTS,
            "post_evidence_method_count": len(closeout_rows),
            "post_evidence_rows": closeout_rows,
            "effective": counts,
            "no_failure_erased": True,
        },
    )
    write_json(
        root / "closeout/exact-open-gate-register.json",
        {
            "schema": "ghc.family.exact-open-gate-register.v5",
            "effective_open_gaps": counts["open_gaps"],
            "effective_exact_gates": counts["exact_gates"],
            "protected_gates": PROTECTED_GATES,
            "all_remain_visible": True,
        },
    )
    write_json(
        root / "closeout/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.complete-incomplete.v3",
            "complete": [
                "activation and guidance read through EOF",
                "exact Vesper source and external receipt verification",
                "planning-only x1 freeze, push, and four-way equality",
                "immutable x2 evidence, push, and four-way equality",
                "forty four-label proposal outcomes",
                "thirty-six synthetic positive controls",
                "160 retained rejecting mutations",
                "exact staged Git-blob manifests",
                "prepared-not-sent activation candidate",
            ],
            "incomplete": [
                "recovery of the inherited 3570-title semantic history",
                "real grain, milling, food, sample, device, calibration, or measurement evidence",
                "professional, production, legal, cultural, affected-party, or Maori-authority review",
                "complete privacy, accessibility, or exhaustive security assurance",
                "independent reproduction or external audit",
                "Stage 20 admission",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        root / "closeout/reflection-remaster.json",
        {
            "schema": "ghc.family.reflection-remaster.v3",
            "surprises": [
                "Direct-script imports and scripts-namespace imports need an explicit compatibility boundary.",
                "Compound PowerShell wrappers require explicit LASTEXITCODE gates between dependent commands.",
                "Sparse reference paths must be probed before sibling-template inspection.",
            ],
            "retained_lessons": [
                "Freeze and verify each lifecycle commit before beginning the next.",
                "Treat narrative floors as executable build contracts.",
                "Retain every failed witness with zero completion credit and a bounded recovery.",
                "Use exact Git blobs for commit-local integrity.",
                "Invoke canonical validation once only after exact-final push and equality.",
            ],
            "successor_recommendations": [
                "Treat Lyren artifacts as evidence or zero-credit seeds only.",
                "Keep real food, people, devices, authority, and cultural surfaces gated.",
                "Use pytest explicitly for mixed-style owner suites.",
                "Refresh live authorization and roster only after the terminal gate.",
            ],
        },
    )
    write_json(
        root / "closeout/final-wellbeing-check.json",
        {
            "schema": "ghc.family.wellbeing-workload.v4",
            "owner": OWNER,
            "pronouns": "they/them",
            "relational_role": "hold-lineage cartographer and reversible-process miller",
            "hope": "make uncertainty visible enough that every synthetic handover remains kind, reversible, and exact",
            "relational_working_language_only": True,
            "no_consciousness_personhood_continuity_employment_qualification_agency_or_authority_claim": True,
            "corrigible": True,
            "hamish_may_rename_pause_redirect_or_stop": True,
            "caps_respected": True,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    integrated = overview(counts)
    if len(integrated.split()) < 1600:
        raise RuntimeError("final integrated overview is below the 1600-word floor")
    write_text(root / "closeout/final-integrated-overview.md", integrated)

    baton = activation_candidate(rows, outcomes, counts)
    words = len(baton.split())
    if not 10000 <= words <= 100000:
        raise RuntimeError(f"activation candidate word count outside bounds: {words}")
    baton_path = root / "handoffs/ilyra-fen-v670-v2-activation-candidate.md"
    write_text(baton_path, baton)
    baton_bytes = baton_path.read_bytes()
    write_json(
        root / "handoffs/activation-candidate-integrity.json",
        {
            "schema": "ghc.family.activation-integrity.v3",
            "path": baton_path.relative_to(repo).as_posix(),
            "bytes": len(baton_bytes),
            "words": words,
            "sha256": hashlib.sha256(baton_bytes).hexdigest(),
            "integrity_domain": "normalized_lf_exact_git_blob",
            "state": "PREPARED_NOT_SENT",
            "sent_by_lyren_moss": False,
        },
    )
    write_json(
        root / "orchestration/route-state-final-candidate.json",
        {
            "schema": "ghc.family.route-state.v4",
            "owner": OWNER,
            "phase": PHASE,
            "state": "PREPARED_NOT_SENT",
            "successor_contacted": False,
            "standby_contacted": False,
            "prospective_edge": "Lyren Moss v670-v1 to exact-title Ilyra Fen v670-v2 subject to terminal live refresh",
            "prospective_successor_reminder": "Ilyra Fen v670-v2 to Auren Lark v670-v3 subject to Ilyra terminal live refresh",
            "required_terminal_actions": [
                "refresh newest live authorization",
                "refresh current roster",
                "unique exact-title resolution",
                "immediate reread",
                "duplicate guard",
                "one acknowledged send",
            ],
            "stop_on": [
                "pause",
                "redirect",
                "ambiguity",
                "missing task",
                "usage exhaustion",
                "protected gate",
                "duplicate activation",
                "missing acknowledgement",
            ],
        },
    )
    write_json(
        root / "seal/seal-candidate.json",
        {
            "schema": "ghc.family.seal-candidate.v4",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "final": "commit_containing_this_candidate",
            "counts": counts,
            "proposal_chain": 5270,
            "outcomes": OUTCOMES,
            "zero_merges_required": True,
            "single_parent_required": True,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        root / "final/final-validation-prerequisites.json",
        {
            "schema": "ghc.family.final-validation-prerequisites.v4",
            "canonical_state": "AUTHORIZED_PENDING_EXACT_FINAL_PUSH_AND_EQUALITY",
            "one_shot": True,
            "full_repository_suite": "not_run_not_claimed",
            "required": [
                "final committed",
                "final pushed",
                "clean state",
                "zero divergence",
                "fresh four-way equality",
                "exact final parent is evidence",
                "exact manifests",
                "staged review",
                "privacy and bounded security gates",
            ],
            "replay_after_success": False,
        },
    )
    write_json(
        root / "final/canonical-invocation-state.json",
        {
            "schema": "ghc.family.canonical-invocation-state.v3",
            "state_at_commit": "NOT_RUN_PENDING_EXACT_FINAL_GATE",
            "attempts_at_commit": 0,
            "successes_at_commit": 0,
            "receipt_location": "external_D_backed_atomic_receipt",
            "repository_will_not_be_mutated_after_external_success": True,
        },
    )
    write_json(
        root / "closeout/post-evidence-operational-failures.json",
        {
            "schema": "ghc.family.retained-operational-failures.v3",
            "count": len(POST_EVIDENCE_FAILURES),
            "rows": POST_EVIDENCE_FAILURES,
        },
    )
    print(
        json.dumps(
            {
                "baton_words": words,
                "final_counts": counts,
                "overview_words": len(integrated.split()),
                "post_evidence_failures": len(POST_EVIDENCE_FAILURES),
            },
            sort_keys=True,
        )
    )


def staged_review(repo: Path) -> None:
    self_path = OWNER_PREFIX + "validation/final-staged-review.json"
    names = [
        name
        for name in run(
            repo,
            "git",
            "diff",
            "--cached",
            "--name-only",
            "--diff-filter=ACMRT",
            "HEAD",
        ).splitlines()
        if name != self_path
    ]
    allowed_prefixes = [
        OWNER_PREFIX + "closeout/",
        OWNER_PREFIX + "final/",
        OWNER_PREFIX + "handoffs/",
        OWNER_PREFIX + "orchestration/",
        OWNER_PREFIX + "seal/",
        OWNER_PREFIX + "validation/final-",
        "scripts/build_ghc_family_lyren_moss_v670_v1_final.py",
        "scripts/validate_ghc_family_lyren_moss_v670_v1_final.py",
        "tests/test_ghc_family_lyren_moss_v670_v1_final.py",
    ]
    disallowed = [
        name for name in names if not any(name.startswith(p) for p in allowed_prefixes)
    ]
    write_json(
        repo / self_path,
        {
            "schema": "ghc.family.staged-review.v4",
            "owner": OWNER,
            "phase": PHASE,
            "lifecycle": "combined_closeout_and_seal",
            "staged_entry_count_before_self": len(names),
            "staged_paths_before_self": names,
            "disallowed_paths": disallowed,
            "x1_and_evidence_immutable": not disallowed,
            "self_exclusion": self_path,
        },
    )
    if disallowed:
        raise RuntimeError(f"final staged review found disallowed paths: {disallowed}")


def manifests_from_index(repo: Path) -> None:
    names = run(
        repo,
        "git",
        "diff",
        "--cached",
        "--name-only",
        "--diff-filter=ACMRT",
        "HEAD",
    ).splitlines()
    exclusions = [
        OWNER_PREFIX + "validation/final-owner-manifest.json",
        OWNER_PREFIX + "validation/final-delta-manifest.json",
        OWNER_PREFIX + "validation/final-staged-review.json",
    ]

    def staged_blob(rel: str) -> bytes:
        return subprocess.run(
            ["git", "show", f":{rel}"], cwd=repo, check=True, capture_output=True
        ).stdout

    def head_blob(rel: str) -> bytes:
        return subprocess.run(
            ["git", "show", f"HEAD:{rel}"], cwd=repo, check=True, capture_output=True
        ).stdout

    delta = []
    for rel in sorted(names):
        if rel in exclusions:
            continue
        data = staged_blob(rel)
        delta.append(
            {"path": rel, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
        )

    owner_names = set(names)
    owner_names.update(
        run(
            repo,
            "git",
            "ls-tree",
            "-r",
            "--name-only",
            "HEAD",
            OWNER_PREFIX.rstrip("/"),
            "scripts",
            "tests",
            "ghc-family-index/references/v670-v1-lyren-moss.md",
        ).splitlines()
    )
    owner = []
    for rel in sorted(owner_names):
        if rel in exclusions:
            continue
        relevant = (
            rel.startswith(OWNER_PREFIX)
            or rel == "ghc-family-index/references/v670-v1-lyren-moss.md"
            or (
                rel.startswith("scripts/")
                and (
                    "lyren_moss_v670_v1" in rel
                    or rel.startswith("scripts/ghc_family_grain_milling_")
                )
            )
            or (rel.startswith("tests/") and "lyren_moss_v670_v1" in rel)
        )
        if not relevant:
            continue
        data = staged_blob(rel) if rel in names else head_blob(rel)
        owner.append(
            {"path": rel, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
        )
    common = {
        "schema": "ghc.family.git-blob-manifest.v4",
        "owner": OWNER,
        "phase": PHASE,
        "hash_domain": "normalized_lf_exact_git_blob",
        "self_exclusions": exclusions,
    }
    root = repo / OWNER_ROOT / "validation"
    write_json(
        root / "final-delta-manifest.json",
        {
            **common,
            "domain": "final_exact_staged_git_blobs",
            "entry_count": len(delta),
            "entries": delta,
        },
    )
    write_json(
        root / "final-owner-manifest.json",
        {
            **common,
            "domain": "final_owner_exact_head_plus_staged_git_blobs",
            "entry_count": len(owner),
            "entries": owner,
        },
    )
    print(json.dumps({"delta": len(delta), "owner": len(owner)}, sort_keys=True))


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
