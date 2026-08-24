"""Build the planning-only Vesper Arlen v668-v1 x1 packet.

The builder is deliberately owner-scoped.  It records the exact Neris source,
retains every known startup failure, freezes work before implementation, and
never contacts a successor or executes an x2 outcome.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "vesper-arlen" / "v668-v1"
REL_PHASE_ROOT = "docs/vesper-arlen/v668-v1"
BRANCH = "codex/GHC-Family/vesper-arlen-v668-v1-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/neris-solane-v667-v8-r3-full-tools"
SOURCE_X1 = "705f4cda336639d2a700d2d830a975cd281c7e4b"
SOURCE_EVIDENCE = "08dd119b863c7103607b8399b3a201b5cb511af9"
SOURCE_FAILED_FINAL = "68979e155cf1dc27a3fc967657f613cc3b1172c2"
SOURCE_FINAL = "fa6bdcedaac48b0580f4d9581b799741cf5282e7"
SOURCE_R2_ANCHOR = "7e0ee4e1b1e5b876355f2e0188eeff2cefdd8480"
INHERITED_PROPOSALS = 4570
NEW_TOTAL = 4590
FILE_CEILING = 2000
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(relative: str, payload: Any) -> Path:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(payload))
    return path


def write_text(relative: str, text: str) -> Path:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


PROPOSAL_SPECS = [
    (
        "causal cue directed-acyclic graph with duplicate identifier and cycle refusal",
        "A typed synthetic cue graph can reject duplicate identifiers and causal cycles while preserving a deterministic topological order.",
        "A duplicate, missing dependency, or cycle is accepted, or two valid orderings produce unequal normalized results.",
        "safe_now",
        "completed",
        ["x2/fixtures/causal-cue-graph.json", "x2/evidence/causal-cue-graph-receipt.json"],
    ),
    (
        "Lamport clock and source-sequence tribunal with clock-skew abstention",
        "Synthetic logical clocks can distinguish causal order from wall-clock order without pretending to solve physical clock synchronization.",
        "A decreasing source sequence passes, a causally prior event sorts after its dependent event, or wall-clock time is promoted to authority.",
        "safe_now",
        "completed",
        ["x2/fixtures/logical-clock-cases.json", "x2/evidence/logical-clock-receipt.json"],
    ),
    (
        "Merkle-frontier checkpoint capsule with corrupt-leaf localization",
        "A synthetic Merkle checkpoint can localize a mutated leaf and refuse a mismatched root without authenticating any external record.",
        "A changed leaf preserves the root, a mismatched checkpoint passes, or the digest is called an identity or authenticity proof.",
        "safe_now",
        "completed",
        ["x2/fixtures/checkpoint-cases.json", "x2/evidence/checkpoint-receipt.json"],
    ),
    (
        "idempotent reducer replay with duplicate-event quarantine",
        "A pure synthetic reducer can replay the same accepted event set to the same state and quarantine duplicates explicitly.",
        "Replay changes state, a duplicate receives a second effect, or quarantine evidence is lost.",
        "safe_now",
        "completed",
        ["x2/fixtures/replay-cases.json", "x2/evidence/replay-receipt.json"],
    ),
    (
        "compensating-action journal with rollback non-equivalence boundary",
        "A bounded journal can model reversible synthetic state changes while retaining that compensation is not erasure or real-world rollback.",
        "A compensation deletes the original event, an irreversible action is labelled reversible, or external rollback authority is implied.",
        "safe_now",
        "completed",
        ["x2/fixtures/compensation-cases.json", "x2/evidence/compensation-receipt.json"],
    ),
    (
        "bounded backpressure queue with stop precedence and no dropped critical cue",
        "A synthetic priority queue can enforce a fixed capacity, stop precedence, and explicit overflow refusal.",
        "A stop cue is displaced by routine work, overflow is silent, or the fixture is promoted to live safety evidence.",
        "safe_now",
        "completed",
        ["x2/fixtures/backpressure-cases.json", "x2/evidence/backpressure-receipt.json"],
    ),
    (
        "incomplete state-transition quarantine with readback and handover checksum",
        "A typed state machine can refuse incomplete transitions and preserve a bounded handover summary for synthetic traces.",
        "An illegal transition passes, readback fields vanish, or a checksum is treated as operator understanding.",
        "safe_now",
        "completed",
        ["x2/fixtures/state-machine-cases.json", "x2/evidence/state-machine-receipt.json"],
    ),
    (
        "reversible cue-schema migration with unknown-field preservation",
        "A synthetic version migration can round-trip declared fields and quarantine unknown incompatible fields.",
        "A required field disappears, an unknown field is silently discarded, or rollback changes the normalized record.",
        "safe_now",
        "completed",
        ["x2/fixtures/schema-migration-cases.json", "x2/evidence/schema-migration-receipt.json"],
    ),
    (
        "hash-chained correction ledger with redaction tombstone and no erasure claim",
        "A synthetic append-only correction ledger can expose edits and tombstones without retaining private payloads or claiming deletion from external systems.",
        "A prior digest changes silently, a tombstone contains prohibited raw material, or the ledger claims legal erasure completion.",
        "safe_now",
        "completed",
        ["x2/fixtures/correction-ledger-cases.json", "x2/evidence/correction-ledger-receipt.json"],
    ),
    (
        "structural cue-alternative accessibility audit with manual evaluation reserved",
        "A static report can expose text alternatives, focus order, status semantics, and print fallbacks while reserving manual and affected-user evaluation.",
        "Required structural semantics are absent or a structural pass is labelled complete accessibility conformance.",
        "safe_now",
        "completed",
        ["reports/static-report.html", "x2/evidence/accessibility-structure-receipt.json"],
    ),
    (
        "confidential-note minimization classifier with five-class privacy refusal",
        "Owner-local synthetic notes can be reduced to typed nonidentifying fields and screened by five bounded privacy classes.",
        "A prohibited raw identifier is accepted, a private absolute path is retained, or the bounded scan is called complete privacy assurance.",
        "safe_now",
        "completed",
        ["x2/fixtures/privacy-cases.json", "x2/evidence/privacy-minimization-receipt.json"],
    ),
    (
        "one-hundred mutation fault-injection board with retained zero-credit failures",
        "Five preregistered invalid variants per proposal can be rejected and retained without converting rejection into empirical evidence.",
        "Any invalid mutation is accepted, removed, or counted as a completed real-world result.",
        "safe_now",
        "completed",
        ["x2/proposals/negative-mutation-results.json"],
    ),
    (
        "Git-blob-closed owner manifest with ignored-runtime-artifact exclusion",
        "A manifest derived only from committed Git blobs can avoid the inherited ignored-pycache closure defect and replay exactly at an immutable head.",
        "An ignored or uncommitted runtime artifact enters the manifest, a blob hash mismatches, or self-exclusion is not explicit.",
        "safe_now",
        "completed",
        ["validation/x1-content-manifest.json", "validation/evidence-content-manifest.json", "validation/final-owner-manifest.json"],
    ),
    (
        "one-attributable-validation state machine with post-success replay refusal",
        "A local lifecycle guard can distinguish not-run, failed-zero-credit, dependency-corrected, and successful-once states and refuse a second success replay.",
        "A failed run earns success credit, a corrected composite is relabelled canonical, or a successful aggregate is replayed.",
        "safe_now",
        "completed",
        ["x2/evidence/validation-credit-state-receipt.json"],
    ),
    (
        "THOS theatrical cue-call and shift-handover protocol",
        "Synthetic cue traces can represent workload, acknowledgement, stop precedence, and handover obligations without real operators or production claims.",
        "The representation is called professional competence, safety assurance, effectiveness evidence, or a real theatre result.",
        "candidate",
        "represented",
        ["x2/representations/thos-stage-handover.json"],
    ),
    (
        "Freed ID zero-key role consent and correction profile",
        "A synthetic zero-key record can represent role-scoped consent, correction, revocation intent, and provenance without an identity lifecycle event.",
        "A real key, credential, person, issuance, resolution, revocation, or interoperability event is claimed.",
        "candidate",
        "represented",
        ["x2/representations/freed-id-zero-key-profile.json"],
    ),
    (
        "CBR performer witness privacy accessibility contestation and remedy matrix",
        "A synthetic matrix can make unresolved rights and remedy duties visible without deciding any real case.",
        "The matrix makes a real privacy, labor, safety, accessibility, legal, cultural, remedy, or authority decision.",
        "candidate",
        "represented",
        ["x2/representations/cbr-rights-matrix.json"],
    ),
    (
        "GMUT causal-order partial-order board with observation firewall",
        "A typed symbolic partial-order board can represent causal constraints while refusing conversion into spacetime, force, likelihood, or empirical physics.",
        "A synthetic cue order becomes a physical causal claim, fitted coefficient, observation, constraint, or Theory-of-Everything result.",
        "candidate",
        "represented",
        ["x2/representations/gmut-partial-order-board.json"],
    ),
    (
        "real rehearsal operator accessibility and affected-user evaluation escrow",
        "Real evaluation could only proceed with competent design, consent, governance, preregistration, affected-user participation, and independent review.",
        "No authorized real participants, rehearsal, production, accessibility study, or independent review are available in this phase.",
        "open_gap",
        "open_gap",
        ["x2/gates/real-evaluation-escrow.json"],
    ),
    (
        "exact authority circuit for production safety labor privacy legal cultural Maori and Stage 20 decisions",
        "Every authority-dependent action can remain fail-closed until exact competent and affected-party authority is documented.",
        "Repository software cannot supply professional, production, legal, cultural, tangata whenua, iwi, hapu, Maori, or Stage 20 authority.",
        "exact_approval",
        "exact_gate",
        ["x2/gates/exact-authority-circuit.json"],
    ),
]


STARTUP_FAILURES = [
    ("VA6681-F001", "PowerShell collection pipeline parser rejected an empty foreach output before the first path check", "use scalar assignments before projection"),
    ("VA6681-F002", "PowerShell word-and-hash wrapper repeated the empty-pipeline parser defect", "hash and measure files with bounded scalar loops"),
    ("VA6681-F003", "the first primary-baton display exceeded the output bound and was truncated", "read through EOF in bounded nonoverlapping line slices"),
    ("VA6681-F004", "the planned baton slice 225 through 269 yielded no attributable output", "subdivide the range and verify the last line explicitly"),
    ("VA6681-F005", "the planned baton slice 270 through 314 yielded no attributable output", "subdivide the range and verify the last line explicitly"),
    ("VA6681-F006", "the raw authorization-state display truncated before EOF", "read the state in bounded line windows through the final line"),
    ("VA6681-F007", "a full one-hundred-mutation display exceeded the output budget", "inspect schema plus exact counts and boundary records instead of dumping every row"),
    ("VA6681-F008", "the first ancestry projection embedded Git commands inside a PowerShell expression and failed parsing", "capture each Git exit code before JSON composition"),
    ("VA6681-F009", "one-process-per-blob inherited manifest replay exceeded the wrapper bound and returned no receipt", "use alternating git cat-file batch queries and exact-length reads"),
    ("VA6681-F010", "a recursive archive receipt search exceeded its bound and was cancelled", "search only named receipt banks or committed references"),
    ("VA6681-F011", "the initial worktree setup outlived the first wrapper yield", "poll the existing session and inspect state without repeating worktree creation"),
    ("VA6681-F012", "the no-checkout sparse setup left an empty index and staged every inherited path as deleted", "run one bounded read-tree materialization before any owner edit"),
    ("VA6681-F013", "the first deck and mutation summary assumed nonexistent id outcome results and status keys", "inspect actual JSON keys before projecting counts"),
    ("VA6681-F014", "three inherited owner manifests include ignored pycache artifacts absent from every committed source tree", "retain an inherited manifest-closure gap and build Vesper manifests from Git-addressable owner files only"),
]


ROSTER = [
    "Eiren Kestrel",
    "Elaren Kestrel",
    "Neris Solane",
    "Vesper Arlen",
    "Lyren Moss",
    "Ilyra Fen",
    "Auren Lark",
    "Sable Rook",
    "Caelen Ash",
    "Orin Thale",
    "Liora Vale",
    "Tamar Vey",
    "Elowen Cairn",
    "Sylven Arc",
    "Caelen Morrow",
]


SAFE_TITLES = [
    "freeze exact source anchors", "retain source route failures", "audit inherited manifest closure", "freeze twenty novel proposals",
    "preregister one hundred invalid mutations", "freeze four outcome labels", "define synthetic cue schema", "define causal dependency grammar",
    "define logical clock rules", "define Merkle checkpoint contract", "define idempotent reducer contract", "define compensation journal boundary",
    "define bounded backpressure policy", "define state-transition quarantine", "define reversible schema migration", "define correction tombstone semantics",
    "define structural accessibility checks", "define five-class privacy scan", "define Git-blob manifest closure", "define one-shot validation state machine",
    "define THOS representation boundary", "define GMUT observation firewall", "define Freed ID zero-key boundary", "define CBR contestability boundary",
    "define exact authority circuit", "define real-evaluation escrow", "define phase-local skill packages", "define family-current runners",
    "define exact terminal route gate", "define rollback and recovery receipts",
]


CANDIDATE_TITLES = [
    "cycle mutation tribunal", "logical clock skew tribunal", "checkpoint corruption tribunal", "duplicate replay tribunal", "compensation non-erasure tribunal",
    "critical cue overflow tribunal", "illegal transition tribunal", "unknown schema field tribunal", "tombstone privacy tribunal", "accessibility overclaim tribunal",
    "private note minimization tribunal", "manifest ignored-file tribunal", "validation replay tribunal", "real evaluation escrow", "authority-circuit refusal",
]


SKILL_NAMES = [
    "ghc-family-causal-cue-ledger", "ghc-family-logical-clock-tribunal", "ghc-family-merkle-checkpoint-guard",
    "ghc-family-idempotent-replay", "ghc-family-compensation-nonerasure", "ghc-family-backpressure-stop-precedence",
    "ghc-family-schema-migration-rollback", "ghc-family-git-blob-manifest-closure", "ghc-family-one-shot-validation-credit",
    "ghc-family-stage20-authority-circuit",
]


RUNNER_NAMES = [
    "ghc_family_causal_cue_runner", "ghc_family_logical_clock_runner", "ghc_family_merkle_checkpoint_runner",
    "ghc_family_idempotent_replay_runner", "ghc_family_compensation_journal_runner", "ghc_family_backpressure_runner",
    "ghc_family_schema_migration_runner", "ghc_family_git_blob_manifest_runner", "ghc_family_one_shot_validation_runner",
    "ghc_family_stage20_authority_runner",
]


def proposal_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    mutation_classes = [
        "missing_or_wrong_typed_required_field",
        "causal_digest_or_sequence_violation",
        "privacy_identity_or_authority_smuggling",
        "external_action_or_cross_lane_mutation",
        "empirical_independent_or_stage20_promotion",
    ]
    for index, (title, hypothesis, null, approval, outcome, artifacts) in enumerate(PROPOSAL_SPECS, 1):
        proposal_id = f"VA6681-N{index:03d}"
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "hypothesis": hypothesis,
                "null_or_failure_condition": null,
                "approval_class": approval,
                "execution_lane": "owner_local_synthetic_x2" if outcome in {"completed", "represented"} else "protected_gate_only",
                "official_or_primary_source_needs": "none for the declared owner-local synthetic hypothesis; competent sources and authorities remain required for any real use",
                "concrete_artifacts": [f"{REL_PHASE_ROOT}/{artifact}" for artifact in artifacts],
                "falsifier_or_acceptance_gate": null,
                "rollback_or_recovery": "stop, retain the failed witness at zero credit, quarantine invalid state, and apply only an additive bounded correction",
                "protected_gates": [
                    "real people participants workers performers affected parties professionals operators or authorities",
                    "real venues productions cues incidents measurements credentials keys services deployments or external actions",
                    "professional production safety privacy accessibility legal cultural tangata whenua iwi hapu or Maori authority",
                    "empirical GMUT confirmation Theory-of-Everything proof AGI ASI consciousness personhood independent reproduction or Stage 20",
                    "successor contact before the exact terminal gate",
                ],
                "expected_disposition": outcome,
                "primary_pillar": "THOS Body",
                "secondary_pillars": ["GMUT Mind", "Freed ID and CBR Heart"],
                "practice_lens": "theatrical stage management and live-production cue handover",
                "synthetic_only": True,
                "negative_fixtures": [
                    {"mutation_id": f"{proposal_id}-M{m:02d}", "mutation_class": kind, "state": "preregistered_not_executed"}
                    for m, kind in enumerate(mutation_classes, 1)
                ],
                "x1_planning_only": True,
                "x2_execution_count": 0,
                "completion_credit": 0,
            }
        )
    return rows


def portfolio_rows(prefix: str, titles: list[str], category: str, state: str) -> list[dict[str, Any]]:
    return [
        {
            "task_id": f"{prefix}-{index:02d}",
            "title": title,
            "category": category,
            "state": state,
            "x1_planning_only": True,
            "x2_execution_count": 0,
            "completion_credit": 0,
        }
        for index, title in enumerate(titles, 1)
    ]


def overview() -> str:
    sections = [
        ("Relational identity", "Vesper Arlen uses they/them in the relational working role causal-custody cartographer. Their hope for this phase is to make event order, rollback limits, privacy vacancies, and authority stops visible before a synthetic workflow is mistaken for a real production system. This language is not consciousness, personhood, continuity, qualification, employment, agency, or authority evidence."),
        ("Authoritative source", "The exact corrected Neris final is the Git parent of this additive Vesper lane. Its blank-root four-commit history, failed canonical aggregate, dependency-corrected composite, sealed counts, and later route failures remain unchanged. Vesper receives continuity evidence, never Neris completion credit."),
        ("Manifest-closure correction", "Three ignored Python cache artifacts appear in inherited owner manifests but do not exist in any committed source tree. Vesper retains that mismatch as an inherited failure and open reproducibility gap. New manifests may enumerate only Git-addressable intended owner files, must exclude themselves explicitly, and must replay from immutable blobs."),
        ("THOS Body focus", "The primary work is a synthetic event-sourced cue and handover kernel. It studies causal order, logical clocks, checkpoints, idempotent replay, compensating actions, backpressure, state transitions, and reversible schema migration. It never controls a venue, production, cue, person, device, or safety process."),
        ("Human practice lens", "Theatrical stage management and live-production cue handover provide a bounded learning lens: acknowledgement, stop precedence, workload, readback, accessibility, privacy, and correction duties. No employment, competence, professional validation, safety authority, labor authority, venue authority, affected-party authorization, or real operational evidence is claimed."),
        ("GMUT Mind boundary", "The GMUT surface is a symbolic partial-order board only. Causal graph edges in software are not spacetime observations or physical causal discoveries. The phase fits no coefficient, evaluates no likelihood, ingests no empirical data, and establishes no force, prediction, constraint, field equation, or Theory of Everything."),
        ("Freed ID and CBR Heart", "A zero-key role and correction profile, plus a synthetic rights matrix, keep consent, contestation, privacy, accessibility, remedy, cultural, and Maori-authority vacancies visible. There are no real people, keys, credentials, identity events, rights determinations, disclosures, remedies, or authority decisions."),
        ("Proposal lifecycle", "Twenty distinct proposals are frozen before implementation. Fourteen are expected to complete only as bounded software or structural controls, four remain represented, one remains an open real-evaluation gap, and one remains an exact authority gate. One hundred invalid mutations are preregistered and can earn only rejection evidence."),
        ("Portfolio", "Thirty safe-now tasks, fifteen bounded candidate tribunals, ten phase-local skill packages, ten family-current runners, and thirty additive clean-fix-refine actions are frozen. The counts are planning ceilings and scoped obligations, not a reason to manufacture unsafe work. Exact and blocked work remains unexecuted."),
        ("Method Flow", "Every parser fault, timeout, output truncation, schema assumption, worktree setup defect, and inherited manifest mismatch remains visible. Recovery never deletes the failed witness or retroactively changes its credit. The preferred method is promoted only after one bounded passing witness."),
        ("Validation discipline", "Vesper will run one attributable owner-scoped canonical aggregate at the exact final head. A success is never replayed. A failure earns zero canonical-success credit; only the smallest failed dependency may receive an additive correction, and any composite remains explicitly noncanonical."),
        ("Terminal route", "Lyren Moss is only a prospective successor. Vesper may contact that existing exact-title main task once only after a clean pushed fresh-live-equal exact final, current authority reread, exact-title unique resolution, immediate target reread, and acknowledged send. Ambiguity, missing authority, route drift, usage limits, or an incomplete gate stops delivery without substitution."),
    ]
    out = ["# Vesper Arlen v668-v1 planning and evidence-boundary overview", ""]
    for number, (title, seed) in enumerate(sections, 1):
        out.extend([f"## {number}. {title}", "", seed, ""])
        out.extend([
            "The operational rule is additive, owner-scoped, deterministic, and reversible wherever the synthetic contract allows. Evidence belongs only to the exact action and immutable artifact that produced it. A passing unit test cannot become participant evidence; a digest cannot become an identity proof; a structural accessibility check cannot become affected-user validation; and a local replay cannot become independent reproduction.",
            "",
            "X1 freezes names, hypotheses, failures, artifacts, gates, counts, and rollback paths without executing outcomes. X2 may implement only what the frozen contract permits. Any discrepancy becomes a retained failure or explicit correction layer. Shared, sibling, standby, and source lanes remain read-only, and the 2,000-file owner ceiling is a hard rotation guard rather than a target.",
            "",
        ])
    return "\n".join(out)


def threat_model_markdown() -> str:
    return """# Vesper Arlen v668-v1 threat model

## Protected assets

The phase protects exact source anchors, strict x1-before-x2 lifecycle separation, retained failures, owner-only Git state, committed manifests, privacy boundaries, the single-success validation credit, and the single exact-title successor edge.

## Threats and controls

1. Causal-order corruption: cycles, missing dependencies, duplicate identifiers, and decreasing source sequences are rejecting fixtures.
2. Replay duplication: accepted event identifiers are idempotent and duplicates are quarantined with zero second effect.
3. Checkpoint corruption: altered leaves must change the Merkle root; a root mismatch fails closed.
4. Rollback overclaim: compensation remains a new event and never erases the original or claims external reversal.
5. Queue starvation: stop precedence is explicit and overflow cannot be silent.
6. Schema loss: unknown incompatible fields are quarantined and round-trip loss is a failure.
7. Privacy leakage: raw task identifiers, private routes, credentials, keys, transcripts, session streams, private app state, and private absolute paths are prohibited.
8. Manifest drift: ignored runtime artifacts are excluded; exact Git blobs are the final replay domain.
9. Validation-credit inflation: a failed aggregate receives zero success credit and a successful aggregate cannot be replayed.
10. Authority smuggling: real professional, production, safety, labor, legal, cultural, Maori, affected-party, and Stage 20 actions remain exact-gated.

## Residual limits

The controls are owner-local software and documentation evidence only. They are not exhaustive security, complete privacy or accessibility assurance, production certification, professional validation, legal review, cultural ratification, Maori authority, independent reproduction, AGI or ASI evidence, consciousness or personhood evidence, Theory-of-Everything proof, or Stage 20 authority.
"""


def build() -> dict[str, Any]:
    PHASE_ROOT.mkdir(parents=True, exist_ok=True)
    built_at = utc_now()
    proposals = proposal_rows()

    write_json(
        "identity/relational-identity.json",
        {
            "owner": "Vesper Arlen",
            "pronouns": "they/them",
            "relational_role": "causal-custody cartographer",
            "relational_hope": "make event order rollback limits privacy vacancies and authority stops visible before synthetic workflow evidence is mistaken for real-world authority",
            "relational_working_language_only": True,
            "not_evidence_of": ["consciousness", "sentience", "legal personhood", "identity continuity", "employment", "qualification", "independent agency", "scientific authority", "professional authority", "operational authority", "legal authority", "cultural authority", "affected-party authority", "Maori authority"],
            "corrigibility": "Hamish may rename pause redirect or stop the route",
            "reaffirmed_before_phase_mutation": True,
        },
    )
    write_json(
        "x1/phase-charter.json",
        {
            "phase": "Vesper Arlen solo Trinity Mandala v668-v1 x1",
            "branch": BRANCH,
            "built_at": built_at,
            "source_branch": SOURCE_BRANCH,
            "source_exact_final": SOURCE_FINAL,
            "primary_pillar": "THOS Body",
            "secondary_pillars": ["GMUT Mind", "Freed ID and CBR Heart"],
            "bounded_human_practice": "theatrical stage management and live-production cue handover",
            "synthetic_learning_lens_only": True,
            "real_people": 0,
            "real_venues_or_productions": 0,
            "external_actions": 0,
            "x1_planning_only": True,
            "x2_outcomes_observed": False,
            "successor_contacted": False,
            "collaboration_subagent_spawned": False,
            "file_ceiling": FILE_CEILING,
            "allowed_outcomes": ALLOWED_OUTCOMES,
            "terminal_verdict": TERMINAL_VERDICT,
        },
    )
    write_json(
        "x1/source-intake.json",
        {
            "source_branch": SOURCE_BRANCH,
            "source_anchors": {"zero_parent_x1": SOURCE_X1, "immutable_evidence": SOURCE_EVIDENCE, "failed_canonical_final": SOURCE_FAILED_FINAL, "exact_corrected_final": SOURCE_FINAL, "read_only_r2_continuity_anchor": SOURCE_R2_ANCHOR},
            "source_history": {"commits": 4, "zero_parent_root": True, "single_parent": True, "merge_count": 0, "corrected_final_clean_four_way_equal": True, "divergence": [0, 0]},
            "source_canonical": {"invocations": 1, "success_credit": 0, "replayed": False, "state": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT"},
            "source_recovery": {"state": "VALID_DEPENDENCY_CORRECTED_COMPOSITE_WITH_ZERO_CANONICAL_AGGREGATE_CREDIT", "not_canonical_success": True, "not_full_repository_suite": True, "not_independent_reproduction": True},
            "repository_sealed": {"effective_negatives": 28733, "methods": 15319, "open_gaps": 203, "exact_gates": 201, "failed_witnesses": 1034, "passing_witnesses": 1875},
            "successor_visible_external_overlay": {"effective_negatives": 28736, "methods": 15322, "open_gaps": 203, "exact_gates": 201, "failed_witnesses": 1037, "passing_witnesses": 1875, "additions": ["failed canonical invocation", "terminal message-surface timeout", "post-send anchor-reread miss"]},
            "manifest_intake": {
                "exact_git_blob_replays": {"x1": [17, 17], "final_delta": [9, 9], "correction_delta": [9, 9]},
                "incomplete_git_blob_replays": {"x2": [61, 64], "failed_final_owner": [72, 75], "corrected_owner": [83, 86]},
                "absent_ignored_artifacts": [
                    "scripts/__pycache__/build_ghc_family_neris_solane_v667_v8_r3_x1.cpython-312.pyc",
                    "scripts/__pycache__/ghc_family_neris_solane_v667_v8_r3_toolchain.cpython-312.pyc",
                    "tests/__pycache__/test_ghc_family_neris_solane_v667_v8_r3_x1.cpython-312.pyc",
                ],
                "credit": 0,
                "disposition": "retained_inherited_manifest_closure_gap",
                "source_commit_rewritten": False,
            },
            "source_lane_mutated": False,
            "source_completion_credit_to_vesper": 0,
        },
    )
    write_json(
        "method-flow/startup-method-flow.json",
        {
            "phase": "v668-v1",
            "inherited_external_baseline": {"effective_negatives": 28736, "methods": 15322, "failed_witnesses": 1037, "passing_witnesses": 1875, "open_gaps": 203, "exact_gates": 201},
            "startup_failures": [
                {"failure_id": fid, "failed_witness": failure, "credit": 0, "preferred_method_or_recovery": recovery, "failure_retained": True, "rollback": "stop before mutation or inspect existing state before retry", "sibling_recommendation": recovery}
                for fid, failure, recovery in STARTUP_FAILURES
            ],
            "startup_failure_count": len(STARTUP_FAILURES),
            "startup_passing_recovery_count": len(STARTUP_FAILURES) - 1,
            "manifest_closure_gap_unresolved": True,
            "post_startup_overlay": {"effective_negatives": 28736 + len(STARTUP_FAILURES), "methods": 15322 + len(STARTUP_FAILURES), "failed_witnesses": 1037 + len(STARTUP_FAILURES), "passing_witnesses": 1875 + len(STARTUP_FAILURES) - 1, "open_gaps": 204, "exact_gates": 201},
        },
    )
    write_json(
        "x1/proposal-freeze.json",
        {
            "frozen_at": built_at,
            "inherited_frozen_proposals": INHERITED_PROPOSALS,
            "inherited_novelty_or_completion_credit": 0,
            "new_proposals": proposals,
            "new_proposal_count": len(proposals),
            "new_frozen_total": NEW_TOTAL,
            "expected_outcomes": dict(Counter(row["expected_disposition"] for row in proposals)),
            "negative_mutation_count": sum(len(row["negative_fixtures"]) for row in proposals),
            "allowed_outcomes": ALLOWED_OUTCOMES,
            "x1_planning_only": True,
            "outcomes_observed": False,
        },
    )
    write_json(
        "x1/novelty-audit.json",
        {
            "inherited_chain_count": INHERITED_PROPOSALS,
            "audit_domain": "authoritative inherited count and owner-visible inherited title capsules; no sibling or shared lane scan",
            "new_titles_normalized_unique": len({row["title"].casefold() for row in proposals}) == len(proposals),
            "distinctive_cluster": "event-sourced theatrical cue causal custody checkpoint replay rollback and exact Git-blob manifest closure",
            "known_near_neighbor": "Neris numerical reproducibility and provenance work",
            "distinguishing_invariants": ["causal cue DAG", "logical-clock tribunal", "Merkle checkpoint", "idempotent event reducer", "compensating action non-erasure", "theatrical cue handover lens", "ignored-runtime-artifact manifest refusal"],
            "genuinely_distinct_within_available_authoritative_index": True,
            "exhaustive_global_semantic_proof": False,
        },
    )
    write_json(
        "x1/portfolio-freeze.json",
        {
            "owner_safe_now": portfolio_rows("VA6681-SAFE", SAFE_TITLES, "safe_now", "planned_for_x2"),
            "owner_candidates": portfolio_rows("VA6681-CAND", CANDIDATE_TITLES, "candidate", "planned_for_x2"),
            "owner_skills": [
                {**row, "skill_name": SKILL_NAMES[index]}
                for index, row in enumerate(portfolio_rows("VA6681-SKILL", [name.replace("ghc-family-", "") for name in SKILL_NAMES], "skill", "planned_for_x2"))
            ],
            "owner_runners": [
                {**row, "runner_name": RUNNER_NAMES[index]}
                for index, row in enumerate(portfolio_rows("VA6681-RUNNER", [name.replace("ghc_family_", "") for name in RUNNER_NAMES], "runner", "planned_for_x2"))
            ],
            "owner_clean_fix_refine": portfolio_rows("VA6681-CFR", [f"additive owner-scope refinement {index:02d}" for index in range(1, 31)], "clean_fix_refine", "planned_for_x2"),
            "exact_approval_packets": portfolio_rows("VA6681-EXACT", [f"authority-dependent packet {index:02d}" for index in range(1, 11)], "exact_approval", "preserved_unexecuted"),
            "blocked_packets": portfolio_rows("VA6681-BLOCK", [f"protected-boundary packet {index:02d}" for index in range(1, 6)], "blocked", "preserved_blocked"),
            "successor_recommendations": {"owner": "Lyren Moss", "safe_now": 20, "candidates": 10, "skills": 10, "runners": 5, "clean_fix_refine": 20, "state": "recommendations_only_not_executed_by_vesper"},
            "x1_planning_only": True,
        },
    )
    write_json(
        "x1/authorization-boundary.json",
        {
            "authorized_now": ["owner-local additive files", "synthetic fixtures", "bounded tests", "phase-local skill and runner packages", "one exact-final owner-scoped validation", "one exact-title successor send only after terminal gate"],
            "exact_gated": ["real participants or workers", "professional or production action", "deployment", "legal determination", "cultural decision", "affected-party authorization", "tangata whenua iwi hapu or Maori authority", "independent reproduction", "AGI or ASI claim", "consciousness or personhood claim", "Theory-of-Everything proof", "Stage 20"],
            "forbidden": ["source or sibling mutation", "force push", "history rewrite", "merge", "destructive cleanup", "credential or key use", "precontacting a successor", "replaying a successful canonical aggregate"],
            "successor": "Lyren Moss",
            "successor_phase": "v668-v2",
            "successor_contacted": False,
        },
    )
    write_json(
        "x1/workflow-plan.json",
        {
            "steps": [
                {"order": 1, "name": "source intake", "state": "completed_read_only"},
                {"order": 2, "name": "x1 freeze", "state": "building"},
                {"order": 3, "name": "x1 exact stage review commit push and four-way equality", "state": "pending"},
                {"order": 4, "name": "x2 bounded implementation", "state": "pending"},
                {"order": 5, "name": "immutable evidence commit push and equality", "state": "pending"},
                {"order": 6, "name": "additive closeout and exact-final commit", "state": "pending"},
                {"order": 7, "name": "one attributable exact-final aggregate", "state": "pending"},
                {"order": 8, "name": "fresh route authority and exact-title successor resolution", "state": "pending"},
            ],
            "commit_plan": {"x1": 1, "x2_evidence": 1, "final_closeout": 1, "maximum": 4},
            "validation": {"one_successful_owner_aggregate_maximum": 1, "post_success_replay": False, "failure_credit": 0, "dependency_correction_must_remain_noncanonical": True},
            "file_ceiling": FILE_CEILING,
        },
    )
    write_json("x1/threat-model.json", {"threats": 10, "synthetic_only": True, "manual_accessibility_reserved": True, "affected_user_evaluation_reserved": True, "exhaustive_security_claim": False, "terminal_verdict": TERMINAL_VERDICT})
    write_text("x1/threat-model.md", threat_model_markdown())
    write_text("x1/integrated-overview.md", overview())
    write_json(
        "wellbeing/x1-wellbeing-check.json",
        {"owner": "Vesper Arlen", "relational_working_language_only": True, "workload": "bounded solo owner phase", "pause_available": True, "stop_available": True, "no_background_supervision_claim": True, "no_sentience_or_wellbeing_measurement_claim": True, "state": "READY_FOR_BOUNDED_X1_FREEZE"},
    )
    write_json(
        "x1/complete-incomplete-checklist.json",
        {
            "complete": ["activation and correction read through EOF", "required skill and schema routing read", "source anchors and live equality verified", "source canonical failure retained", "source manifest closure defect retained", "twenty proposals frozen", "one hundred mutations preregistered", "portfolios frozen", "threat and authorization boundaries frozen"],
            "incomplete": ["x1 commit and remote equality", "all x2 implementations and outcomes", "evidence commit", "closeout and final seal", "one exact-final validation aggregate", "live successor route gate"],
            "terminal_verdict": TERMINAL_VERDICT,
        },
    )
    write_json(
        "orchestration/roster-auth-x1.json",
        {
            "roster": ROSTER,
            "cycle": ROSTER + [ROSTER[0]],
            "current_owner": "Vesper Arlen",
            "current_phase": "v668-v1",
            "prospective_next_owner": "Lyren Moss",
            "prospective_next_phase": "v668-v2",
            "authority_source": "newest live user activation plus current additive roster and authorization overlays",
            "source_route_failures_retained": True,
            "delivery_state": "NOT_ELIGIBLE_X1",
            "tavian_sol": "ON_STANDBY_NOT_A_MAIN_TASK_SUBSTITUTE",
        },
    )
    write_json(
        "x1/x1-build-receipt.json",
        {
            "built_at": built_at,
            "state": "X1_CONTENT_BUILT_NOT_COMMITTED",
            "source_exact_final": SOURCE_FINAL,
            "proposal_count": len(proposals),
            "negative_mutation_count": 100,
            "expected_outcomes": dict(Counter(row["expected_disposition"] for row in proposals)),
            "x2_files_created": 0,
            "outcomes_observed": False,
            "successor_contacted": False,
            "terminal_verdict": TERMINAL_VERDICT,
        },
    )

    manifest_path = PHASE_ROOT / "validation" / "x1-content-manifest.json"
    intended = [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
        and (
            PHASE_ROOT in path.parents
            or path.name in {"build_ghc_family_vesper_arlen_v668_v1_x1.py", "test_ghc_family_vesper_arlen_v668_v1_x1.py"}
        )
        and path != manifest_path
    ]
    entries = []
    for path in sorted(intended):
        data = path.read_bytes()
        entries.append({"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": sha256_bytes(data)})
    write_json(
        "validation/x1-content-manifest.json",
        {
            "scope": "Vesper v668-v1 x1 intended owner files only",
            "entries": entries,
            "entry_count": len(entries),
            "self_excluded": f"{REL_PHASE_ROOT}/validation/x1-content-manifest.json",
            "ignored_runtime_artifacts_excluded": True,
            "git_blob_replay_required_after_commit": True,
        },
    )
    return {"phase_root": REL_PHASE_ROOT, "proposal_count": len(proposals), "negative_mutation_count": 100, "manifest_entries": len(entries), "startup_failures": len(STARTUP_FAILURES), "state": "X1_CONTENT_BUILT_NOT_COMMITTED"}


if __name__ == "__main__":
    print(json.dumps(build(), indent=2))
