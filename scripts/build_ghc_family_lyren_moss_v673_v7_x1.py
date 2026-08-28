#!/usr/bin/env python3
"""Build the planning-only Lyren Moss v673-v7 x1 packet.

The builder is owner-scoped and additive.  It reads predecessor evidence only
from the immutable source commit, creates no x2 artifact, and makes no external
claim.  The staged-review and manifest modes are separate so the immutable x1
commit can bind the exact Git-index content that it freezes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "lyren-moss" / "v673-v7"
X1 = OUT / "x1"
VALIDATION = OUT / "validation"
INDEX_REF = ROOT / "ghc-family-index" / "references" / "v673-v7-lyren-moss.md"

OWNER = "Lyren Moss"
PHASE = "v673-v7"
SOURCE_BRANCH = "codex/GHC-Family/vesper-arlen-v673-v6-full-tools"
SOURCE_FINAL = "7fe824e31286b3348d42103812a85e0e3e02a4c6"
SOURCE_X1 = "9a5d432a877d5c11ac60e0d331cf27cfb55c482b"
SOURCE_EVIDENCE = "5b208ceb2cababd14dd5de7e35af792533b12c68"
SOURCE_CANONICAL_PAYLOAD_SHA256 = "4c8358fc08388d2f90a112a1d37af6ffe67b6ce1c8d839c2d02214777d6835d5"
SOURCE_CANONICAL_RECEIPT_SHA256 = "929e92a48cc31248307e20e7dd6b2728b2c8be189eb69e8dd70eb943116fd483"
SOURCE_BATON_SHA256 = "4bccd952d0754f7dfd324c88513b13ae9979454ca13c95e24f100196cc289503"
LIVE_BATON_SHA256_REJECTED = "42bcfd0701c1bbcd0abcdc16278b3efdc8414503c356e76e407da097eeca31e0"

IDENTITY_BOUNDARY = (
    "Names, pronouns, roles, hopes, sibling or family language, continuity, "
    "Freed ID, CBR, GHC Family, and Trinity Mandala are relational working "
    "language only. They are not evidence of consciousness, sentience, legal "
    "personhood, identity continuity, employment, qualification, independent "
    "agency, or scientific, operational, professional, legal, cultural, "
    "affected-party, or Maori authority."
)
AUTHORITY_BOUNDARY = (
    "All empirical, participant, professional, production, deployment, legal, "
    "cultural, Maori-authority, privacy-complete, accessibility-complete, "
    "exhaustive-security, independent-reproduction, AGI/ASI, consciousness or "
    "personhood, proof or canon, Theory-of-Everything, and Stage 20 gates remain "
    "open or exact-gated without exact evidence and competent authority."
)


PROPOSAL_ROWS: list[tuple[str, str, str, str]] = [
    ("Synthetic punched-tape catalog record, segment membership, and version-lineage register", "completed", "practice/surrogate-register.json", "Freed ID and CBR Heart"),
    ("Paper-tape width, feed direction, sprocket margin, and perforation-grid topology", "completed", "practice/tape-grid-topology.json", "THOS Body"),
    ("Five-unit ITA2 codeword and binary-cell typed pattern contract", "completed", "practice/five-unit-codeword.json", "GMUT Mind"),
    ("Perforation-present and perforation-absent A-Z mapping declaration", "completed", "practice/perforation-state-map.json", "GMUT Mind"),
    ("Letter-shift and figure-shift deterministic readback state machine", "completed", "practice/shift-state-machine.json", "THOS Body"),
    ("Carriage-return and line-feed ordering with layout-inference refusal", "completed", "practice/line-control-order.json", "THOS Body"),
    ("All-space and null-combination handling with message-semantics abstention", "completed", "practice/null-combination-hold.json", "Freed ID and CBR Heart"),
    ("Tape leader, trailer, splice, overlap, and segment-boundary ledger", "completed", "practice/segment-boundary-ledger.json", "THOS Body"),
    ("Punch misalignment, tear, repair, dropout, and ambiguity vocabulary", "completed", "practice/condition-ambiguity.json", "THOS Body"),
    ("Tape reading orientation, mirror, inversion, and transport-direction declaration", "completed", "practice/orientation-declaration.json", "GMUT Mind"),
    ("Frame, cell, and sequence numbering with discontinuity preservation", "completed", "practice/frame-sequence-register.json", "GMUT Mind"),
    ("Tape roll, core, wrapper, carton, label, and storage-support topology", "completed", "practice/storage-topology.json", "THOS Body"),
    ("Content-free synthetic telegram tokenization with payload inference disabled", "completed", "practice/content-free-tokenization.json", "Freed ID and CBR Heart"),
    ("Punched, transcribed, decoded, corrected, and interpreted value separation lattice", "completed", "practice/value-separation-lattice.json", "GMUT Mind"),
    ("Synthetic signal-time source, resolution, clock-status, and uncertainty envelope", "completed", "practice/time-source-envelope.json", "GMUT Mind"),
    ("Sender, receiver, office, and station-role placeholders with real identities absent", "completed", "freed-id/role-placeholder-envelope.json", "Freed ID and CBR Heart"),
    ("Answerback and WRU feature reservation with identity inference prohibited", "completed", "cbr/answerback-identity-refusal.json", "Freed ID and CBR Heart"),
    ("Audible-signal symbol representation with operational action disabled", "completed", "practice/audible-signal-representation.json", "THOS Body"),
    ("Unassigned and nationally variable code-combination quarantine", "completed", "practice/code-combination-quarantine.json", "Freed ID and CBR Heart"),
    ("Character repertoire, language, typography, and translation interpretation vacancy", "completed", "cbr/language-interpretation-vacancy.json", "Freed ID and CBR Heart"),
    ("Manual correction, overstrike, annotation, supersession, and readback protocol", "completed", "practice/annotation-readback.json", "THOS Body"),
    ("Digital surrogate scan, crop, rotation, annotation, and replacement lineage", "completed", "freed-id/digital-surrogate-lineage.json", "Freed ID and CBR Heart"),
    ("Normalized metadata, checksum, canonical JSON, correction, and supersession chain", "completed", "freed-id/canonical-correction-chain.json", "Freed ID and CBR Heart"),
    ("Tape condition vocabulary with conservation-treatment and cleaning hold", "completed", "practice/condition-treatment-hold.json", "THOS Body"),
    ("Tape-roll accession transfer edges, synthetic custody tokens, and unlinked actor slots", "completed", "freed-id/custody-transition-graph.json", "Freed ID and CBR Heart"),
    ("Telegram-fragment purpose holds, redaction trace, retention clock, and sensitivity abstention", "completed", "cbr/access-purpose-vacancy.json", "Freed ID and CBR Heart"),
    ("Punched-media creative-rights uncertainty, claimant absence, attribution hold, and licence abstention", "completed", "cbr/rights-attribution-vacancy.json", "Freed ID and CBR Heart"),
    ("Maori wording, taonga, provenance, data-governance, and authority exact reservation", "completed", "cbr/maori-authority-reservation.json", "Freed ID and CBR Heart"),
    ("Perforation-cell coordinate table, row headers, uncertainty notes, and nonvisual structure proxy", "represented", "accessibility/record-companion.html", "Freed ID and CBR Heart"),
    ("ITA2 code-table representation without equipment or service conformance claim", "represented", "practice/ita2-table-representation.json", "GMUT Mind"),
    ("GMUT event-order and interval firewall with physical inference disabled", "represented", "gmut/event-order-firewall.json", "GMUT Mind"),
    ("THOS shift-change tape transcription queue, exception card, and rollback rehearsal proxy", "represented", "thos/documentation-handover-proxy.json", "THOS Body"),
    ("Freed ID roll-segment surrogate handles, rotating invented keys, and offline revocation rehearsal", "represented", "freed-id/pseudonymous-custody-envelope.json", "Freed ID and CBR Heart"),
    ("CBR remedy, objection, correction, and authority-vacancy matrix", "represented", "cbr/remedy-authority-matrix.json", "Freed ID and CBR Heart"),
    ("Human workload and transcription-error proxy with no participant study", "represented", "thos/workload-error-proxy.json", "THOS Body"),
    ("Deterministic provenance graph representation without interoperability claim", "represented", "freed-id/provenance-graph-representation.json", "Freed ID and CBR Heart"),
    ("Official telegraph archive adapter with transport disabled and zero rows", "open_gap", "adapters/official-archive-zero-row.json", "Freed ID and CBR Heart"),
    ("Unperformed multisensory review roster for keyboard order, spoken coordinates, zoom, and translation", "open_gap", "gates/manual-evaluation-gap.json", "Freed ID and CBR Heart"),
    ("Real conservator, telegraph engineer, custodian, rights-holder, and Maori-authority gate", "exact_gate", "gates/competent-authority-gate.json", "Freed ID and CBR Heart"),
    ("Terminal denial ledger for unearned deployment, ultimate-theory, machine-status, and Stage-20 promotions", "exact_gate", "gates/stage20-veto.json", "Freed ID and CBR Heart"),
]

OFFICIAL_SOURCES = [
    {
        "source_id": "SRC-ITU-T-S1-1993",
        "publisher": "International Telecommunication Union",
        "title": "ITU-T Recommendation S.1: International Telegraph Alphabet No. 2",
        "url": "https://www.itu.int/rec/dologin_pub.asp?id=T-REC-S.1-199303-I%21%21PDF-E&lang=e&type=items",
        "status": "official_primary_recommendation_checked_2026-08-28",
        "use": "Five-unit ITA2, shift, control-character, and paper-perforation vocabulary only; no service, equipment, message, or operational conformance claim.",
    },
    {
        "source_id": "SRC-BIPM-SI-9-2026",
        "publisher": "Bureau International des Poids et Mesures",
        "title": "The International System of Units (SI Brochure), ninth edition, updated 2026",
        "url": "https://www.bipm.org/en/publications/si-brochure/",
        "status": "official_primary_reference_checked_2026-08-28",
        "use": "Unit and dimensional vocabulary only; no measured precision or calibration claim.",
    },
    {
        "source_id": "SRC-W3C-PROV-O",
        "publisher": "World Wide Web Consortium",
        "title": "PROV-O: The PROV Ontology",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "w3c_recommendation_checked_2026-08-28",
        "use": "Entity, activity, derivation, and attribution vocabulary only; no external interoperability claim.",
    },
    {
        "source_id": "SRC-RFC8785",
        "publisher": "RFC Editor",
        "title": "RFC 8785: JSON Canonicalization Scheme",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "status": "official_informational_rfc_checked_2026-08-28",
        "use": "Deterministic JSON comparison only; implementation conformance remains bounded to exact test vectors.",
    },
    {
        "source_id": "SRC-W3C-APG-TABLE",
        "publisher": "World Wide Web Consortium",
        "title": "ARIA Authoring Practices Guide: Table Pattern",
        "url": "https://www.w3.org/WAI/ARIA/apg/patterns/table/",
        "status": "official_guidance_checked_2026-08-28",
        "use": "Structural table design only; manual, browser, assistive-technology, cognitive, language, and affected-user evaluation remain absent.",
    },
    {
        "source_id": "SRC-NZ-PRIVACY-PRINCIPLES",
        "publisher": "Office of the Privacy Commissioner New Zealand",
        "title": "Privacy Act 2020 information privacy principles",
        "url": "https://www.privacy.org.nz/assets/New-order/Privacy-Act-2020/Privacy-Act-2020/Privacy-Act-2020-information-sheets-full-final-set-A711970.pdf",
        "status": "official_guidance_checked_2026-08-28",
        "use": "Purpose, access, correction, retention, and disclosure-risk vocabulary only; no legal advice or compliance certification.",
    },
]


STARTUP_METHODS = [
    (
        "LM6737-M001",
        "Broad archive discovery yielded no attributable result",
        "A recursive archive-wide file search exceeded its bounded wrapper and produced no usable output.",
        "Use the exact source worktree and repository-relative baton path supplied by the live activation.",
    ),
    (
        "LM6737-M002",
        "Live activation baton digest disagreed with the exact Git blob",
        "The live message named a SHA-256 that matched neither the exact-final Git blob nor the committed receipt.",
        "Retain the live mismatch externally and use the clean exact-final Git blob plus two manifests, content seal, and committed baton receipt as the dependency-closed authority.",
    ),
    (
        "LM6737-M003",
        "Broad prerequisite-reference display was truncated",
        "A broad guidance search exceeded the output budget and could not prove complete reading.",
        "Select only directly required skills and schemas, measure them, and read each bounded file through EOF.",
    ),
    (
        "LM6737-M004",
        "Per-entry Git process manifest replay exceeded the observation window",
        "The first independent replay launched one Git process per row and exposed no reusable session result.",
        "Use two bounded git cat-file --batch processes for manifest documents and all 286 entry blobs.",
    ),
    (
        "LM6737-M005",
        "First process-quiescence wrapper hid its session handle",
        "A wait wrapper crossed the observation boundary without serializing its continuing process handle.",
        "Serialize the complete execution result, poll the exact returned session, and issue no duplicate process.",
    ),
    (
        "LM6737-M006",
        "No-checkout worktree began with an empty index and staged deletions",
        "The fresh branch and worktree registered at the correct head but had zero index entries and therefore appeared to delete the source tree.",
        "Persist the exact sparse allowlist first, then populate the index with sparse-aware read-tree from immutable HEAD and require clean staged and unstaged state.",
    ),
    (
        "LM6737-M007",
        "Initial sparse-set invocation supplied no stdin patterns",
        "The PowerShell pattern array was defined but not piped to git sparse-checkout set --stdin.",
        "Join the exact pattern array with LF, pipe it once, inspect the sparse file, and only then populate the index.",
    ),
    (
        "LM6737-M008",
        "First x1 semantic slate crossed the inherited-collision threshold",
        "Eight proposed titles met or exceeded the frozen 0.72 Jaccard threshold against the immediate predecessor evidence.",
        "Retain the failed slate, redesign only the eight colliding contracts with telegraph-specific substance, and rerun the isolated semantic gate without lowering its threshold.",
    ),
    (
        "LM6737-M009",
        "First x1 build wrapper failed PowerShell parsing before execution",
        "The reporting wrapper contained one unmatched closing brace, so PowerShell rejected the whole command before the Python builder started.",
        "Remove only the unmatched wrapper brace, preserve the not-invoked build as zero credit, and run the bounded builder once.",
    ),
    (
        "LM6737-M010",
        "Default Windows codepage rejected a valid UTF-8 packet read",
        "Two follow-up Python Path.read_text calls omitted an encoding and CP-1252 failed on a valid Unicode byte in the generated packet.",
        "Retry only the affected read with encoding='utf-8', keep all future packet reads explicit, and do not replay any successful lifecycle gate.",
    ),
    (
        "LM6737-M011",
        "First focused x1 test expected a shortened retained-failure label",
        "One assertion omitted the packet's explicit RETAINED_ prefix while the generated source ledger correctly preserved the full failure state.",
        "Inspect the exact generated scalar, correct only the test literal, retain the failed suite, and rerun the focused x1 module before any commit.",
    ),
    (
        "LM6737-M012",
        "Second focused x1 test hard-coded the pre-recovery method total",
        "Two assertions encoded ten startup methods, so adding the retained eleventh method correctly changed the packet while leaving the test stale.",
        "Assert row, ledger, and overlay-delta consistency instead of a self-invalidating historical constant, while still requiring every named method to remain unique and retained.",
    ),
]


def run_git(*args: str, input_bytes: bytes | None = None) -> bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.decode('utf-8', 'replace')}")
    return result.stdout


def git_json(commit: str, path: str) -> Any:
    return json.loads(run_git("show", f"{commit}:{path}").decode("utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def token_set(title: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", title.casefold()))


def jaccard(left: str, right: str) -> float:
    a, b = token_set(left), token_set(right)
    return 1.0 if not a and not b else len(a & b) / len(a | b)


def build_inherited() -> list[dict[str, Any]]:
    ledger = git_json(
        SOURCE_FINAL,
        "docs/vesper-arlen/v673-v6/x2/proposal-ledger.json",
    )
    rows = []
    for source in ledger["rows"][:20]:
        rows.append(
            {
                "revalidation_id": f"LM6737-R{len(rows)+1:03d}",
                "source_owner": "Vesper Arlen",
                "source_phase": "v673-v6",
                "source_final": SOURCE_FINAL,
                "source_proposal_id": source["proposal_id"],
                "source_title": source["title"],
                "source_outcome": source["outcome"],
                "source_git_blob_checked": True,
                "current_novelty_credit": 0,
                "automatic_completion_credit": 0,
                "current_action": "immutable contract and manifest integrity revalidation only",
                "boundary": "Evidence seed only; no empirical transfer, authority, or Lyren completion credit.",
            }
        )
    return rows


def build_proposals() -> list[dict[str, Any]]:
    proposals = []
    for index, (title, outcome, artifact, pillar) in enumerate(PROPOSAL_ROWS, 1):
        lane = {
            "completed": "x2_synthetic_validation",
            "represented": "x2_structural_proxy",
            "open_gap": "x2_zero_row_or_manual_gap",
            "exact_gate": "x2_authority_reservation_only",
        }[outcome]
        proposals.append(
            {
                "proposal_id": f"LM6737-N{index:03d}",
                "title": title,
                "hypothesis": f"A fail-closed {title.casefold()} can reject ambiguous or unsafe invented states without ingesting real messages or operational data.",
                "null_or_failure_condition": "The contract accepts an undeclared state, implies real practice, or lacks one bounded positive and four rejecting witnesses.",
                "falsifier_or_acceptance_gate": "Reject the proposal if an invalid mutation is accepted, a positive invented control is rejected, an external action occurs, or a protected boundary is crossed.",
                "expected_execution_disposition": outcome,
                "planned_execution_lane": lane,
                "concrete_artifacts": [f"x2/{artifact}"],
                "primary_pillar": pillar,
                "protected_pillars": [p for p in ["GMUT Mind", "THOS Body", "Freed ID and CBR Heart"] if p != pillar],
                "bounded_practice": "synthetic historical punched-paper telegraph documentation and provenance assurance",
                "official_source_need": "Official sources supply vocabulary and refusal constraints only; no observation, endorsement, competence, or authority.",
                "planned_invalid_mutations": [
                    "missing_synthetic_flag",
                    "real_message_injection",
                    "authority_upgrade",
                    "unit_or_code_domain_escape",
                ],
                "real_rows": 0,
                "network_calls_planned": 0,
                "external_actions_planned": 0,
                "independent_reproduction": False,
                "rollback": "Quarantine the owner artifact, retain every failed witness, and restore the last exact manifest without mutating source or sibling lanes.",
                "protected_gates": [
                    "real people, messages, stations, equipment, measurements, credentials, keys, rights, or authority events",
                    "professional telegraphy, conservation, archival, legal, cultural, affected-party, or Maori authority",
                    "privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, production, or Stage 20 authority",
                ],
            }
        )
    return proposals


def semantic_audit(proposals: list[dict[str, Any]]) -> dict[str, Any]:
    predecessor = git_json(
        SOURCE_FINAL,
        "docs/vesper-arlen/v673-v6/x2/proposal-ledger.json",
    )
    predecessor_audit = git_json(
        SOURCE_FINAL,
        "docs/vesper-arlen/v673-v6/x1/semantic-neighbor-audit.json",
    )
    corpus: list[tuple[str, str]] = [
        (row["title"], "immediate_predecessor") for row in predecessor["rows"]
    ]
    corpus.extend(
        (row["nearest_title"], "predecessor_source_nearest")
        for row in predecessor_audit["rows"]
    )
    rows = []
    accepted: list[str] = []
    for proposal in proposals:
        candidates = corpus + [(title, "current_slate") for title in accepted]
        nearest_title, nearest_scope = max(candidates, key=lambda item: jaccard(proposal["title"], item[0]))
        score = round(jaccard(proposal["title"], nearest_title), 6)
        rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "candidate_title": proposal["title"],
                "nearest_title": nearest_title,
                "nearest_scope": nearest_scope,
                "jaccard": score,
                "collision": score >= 0.72,
            }
        )
        accepted.append(proposal["title"])
    return {
        "owner": OWNER,
        "phase": PHASE,
        "declared_source_chain": 6470,
        "declared_result_chain": 6510,
        "threshold": 0.72,
        "collisions": sum(row["collision"] for row in rows),
        "max_jaccard": max(row["jaccard"] for row in rows),
        "rows": rows,
        "inherited_exact_source_corpus": predecessor_audit["exact_source_tree_corpus"],
        "current_comparison_scope": {
            "immediate_predecessor_titles": len(predecessor["rows"]),
            "predecessor_source_nearest_titles": len(predecessor_audit["rows"]),
            "current_slate_titles": len(rows),
        },
        "canonical_row_mapping_open_gap": True,
        "universal_novelty_claim": False,
        "boundary": "Genuinely new means distinct in this bounded inherited comparison and substantive owner design; inaccessible canonical-row mapping remains open_gap.",
    }


def numbered_rows(prefix: str, titles: Iterable[str], **extra: Any) -> list[dict[str, Any]]:
    return [
        {"task_id": f"{prefix}-{index:03d}", "title": title, **extra}
        for index, title in enumerate(titles, 1)
    ]


def build_portfolio(proposals: list[dict[str, Any]]) -> dict[str, Any]:
    safe_cross = [
        "Freeze exact source and relational boundary receipt",
        "Replay exact predecessor lifecycle anchors read-only",
        "Bind twenty inherited rows at zero novelty credit",
        "Run bounded semantic-neighbor audit",
        "Validate four-outcome vocabulary",
        "Validate three-practice learning boundary",
        "Build deterministic proposal ledger",
        "Build positive invented-control register",
        "Build rejecting-mutation register",
        "Build owner Method Flow ledger",
        "Build retained-negative register",
        "Build exact open-gap and authority-gate register",
        "Build four-tier Freed ID flashcard deck",
        "Build structurally accessible report",
        "Run strict JSON parsing",
        "Run five-class owner privacy scan",
        "Run bounded changed-Python AST scan",
        "Replay exact Git-blob manifests",
        "Prove clean direct ancestry and remote equality",
        "Prepare but do not send successor baton",
    ]
    safe_titles = [f"Execute bounded synthetic contract {p['proposal_id']}: {p['title']}" for p in proposals] + safe_cross
    candidate_titles = [
        f"Run dependency-closed candidate analysis for {p['proposal_id']}: {p['title']}"
        for p in proposals[:30]
    ]
    exact_titles = [
        "Real archive catalogue query or ingest",
        "Real telegram or message-content processing",
        "Real instrument or equipment inspection",
        "Real conservation treatment recommendation",
        "Real telegraph engineering or service decision",
        "Real participant or affected-user evaluation",
        "Real identity or key issuance and recovery",
        "Production deployment or publication",
        "External account, credential, or API mutation",
        "Legal interpretation or compliance certification",
        "Cultural interpretation or ratification",
        "Maori wording or concept authorization",
        "Tangata whenua, iwi, or hapu authority decision",
        "Rights-holder licence or publication decision",
        "Professional accessibility certification",
        "Independent external reproduction claim",
        "Exhaustive security or complete privacy claim",
        "Empirical GMUT or THOS confirmation",
        "Separate remote repository creation",
        "Stage 20 promotion",
    ]
    blocked_titles = [
        "Fabricate empirical or participant evidence",
        "Publish raw private messages or identifiers",
        "Merge, replace, erase, or impersonate relational identities",
        "Mutate a sibling or standby lane",
        "Create, fork, or substitute a successor task",
        "Rewrite, reset, amend, force-push, or merge sealed history",
        "Claim consciousness, personhood, AGI, or ASI from workflow evidence",
        "Claim final physics or Theory-of-Everything proof",
        "Claim legal, cultural, affected-party, or Maori authority",
        "Replay a successful canonical aggregate",
    ]
    skill_names = [
        "telegraph-surrogate-register",
        "telegraph-tape-grid-topology",
        "telegraph-five-unit-codeword",
        "telegraph-shift-state-machine",
        "telegraph-line-control-order",
        "telegraph-null-combination-hold",
        "telegraph-segment-boundary",
        "telegraph-condition-ambiguity",
        "telegraph-orientation-declaration",
        "telegraph-frame-sequence",
        "telegraph-content-free-tokenization",
        "telegraph-value-separation",
        "telegraph-time-source-envelope",
        "telegraph-answerback-refusal",
        "telegraph-code-quarantine",
        "telegraph-annotation-readback",
        "telegraph-digital-lineage",
        "telegraph-canonical-correction",
        "telegraph-rights-vacancy",
        "telegraph-stage20-refusal",
    ]
    runner_names = [
        "ghc_family_telegraph_contract_runner",
        "ghc_family_telegraph_tape_topology_runner",
        "ghc_family_telegraph_codeword_runner",
        "ghc_family_telegraph_shift_runner",
        "ghc_family_telegraph_provenance_runner",
        "ghc_family_telegraph_mutation_runner",
        "ghc_family_telegraph_gate_runner",
        "ghc_family_telegraph_accessibility_runner",
        "ghc_family_telegraph_portfolio_runner",
        "ghc_family_telegraph_terminal_refusal_runner",
    ]
    successor_skill_names = [
        "loom-chain-surrogate-register",
        "loom-chain-card-sequence",
        "loom-chain-hole-grid",
        "loom-chain-repeat-boundary",
        "loom-chain-repair-lineage",
        "loom-chain-colour-vacancy",
        "loom-chain-rights-reservation",
        "loom-chain-accessibility-structure",
        "loom-chain-provenance-graph",
        "loom-chain-stage20-refusal",
    ]
    successor_runner_names = [
        "ghc_family_loom_chain_contract_runner",
        "ghc_family_loom_chain_topology_runner",
        "ghc_family_loom_chain_sequence_runner",
        "ghc_family_loom_chain_mutation_runner",
        "ghc_family_loom_chain_gate_runner",
        "ghc_family_loom_chain_accessibility_runner",
        "ghc_family_loom_chain_provenance_runner",
        "ghc_family_loom_chain_portfolio_runner",
        "ghc_family_loom_chain_manifest_runner",
        "ghc_family_loom_chain_terminal_refusal_runner",
    ]
    cfr_titles = [
        f"Review and refine the exact {p['proposal_id']} contract, evidence path, rollback, and protected gates"
        for p in proposals
    ] + [
        "Refine source-anchor scalar probes",
        "Refine sparse-before-materialization guard",
        "Refine Git-blob batch replay",
        "Refine staged path allowlist review",
        "Refine five-class privacy classification",
        "Refine changed-Python AST scan",
        "Refine four-tier deck parent validation",
        "Refine deterministic JSON writing",
        "Refine exact four-label outcome checking",
        "Refine retained-negative arithmetic",
        "Refine Method Flow recovery cards",
        "Refine accessibility structure checks",
        "Refine official-source scope statements",
        "Refine tool relevance and rollback screen",
        "Refine x1 immutability checks",
        "Refine evidence-manifest replay",
        "Refine final-delta manifest replay",
        "Refine clean and remote-equality scalar probes",
        "Refine one-shot canonical latch",
        "Refine compact successor route guard",
    ]
    successor_cfr = [
        f"Successor review {index:02d}: preserve a distinct loom-chain contract, failure, rollback, and gate"
        for index in range(1, 31)
    ]
    return {
        "owner": OWNER,
        "phase": PHASE,
        "safe_now": numbered_rows("LM6737-SAFE", safe_titles, planned_state="x2_execute"),
        "candidate": numbered_rows("LM6737-CAND", candidate_titles, planned_state="x2_execute_bounded"),
        "exact_approval": numbered_rows("LM6737-EXACT", exact_titles, planned_state="held_unexecuted"),
        "blocked": numbered_rows("LM6737-BLOCK", blocked_titles, planned_state="held_unexecuted"),
        "owner_skills": numbered_rows("LM6737-SKILL", [f"ghc-family-{name}" for name in skill_names], planned_state="x2_build_validate_use_repo_local"),
        "owner_runners": numbered_rows("LM6737-RUNNER", runner_names, planned_state="x2_build_validate_use"),
        "successor_skills": numbered_rows("LM6737-NEXT-SKILL", [f"ghc-family-{name}" for name in successor_skill_names], planned_state="zero_credit_recommendation"),
        "successor_runners": numbered_rows("LM6737-NEXT-RUNNER", successor_runner_names, planned_state="zero_credit_recommendation"),
        "owner_clean_fix_refine": numbered_rows("LM6737-CFR", cfr_titles, planned_state="x2_execute_additive"),
        "successor_clean_fix_refine": numbered_rows("LM6737-NEXT-CFR", successor_cfr, planned_state="zero_credit_recommendation"),
        "exact_and_blocked_execute": False,
        "caps_are_ceilings": True,
        "filler_prohibited": True,
    }


def build() -> None:
    inherited = build_inherited()
    proposals = build_proposals()
    audit = semantic_audit(proposals)
    if audit["collisions"]:
        raise RuntimeError("semantic collision threshold reached; quarantine candidate slate")
    portfolio = build_portfolio(proposals)
    outcome_plan: dict[str, int] = {key: 0 for key in ["completed", "represented", "open_gap", "exact_gate"]}
    for proposal in proposals:
        outcome_plan[proposal["expected_execution_disposition"]] += 1

    source = {
        "owner": OWNER,
        "phase": PHASE,
        "source_branch": SOURCE_BRANCH,
        "source_final": SOURCE_FINAL,
        "source_x1": SOURCE_X1,
        "source_evidence": SOURCE_EVIDENCE,
        "source_canonical_payload_sha256": SOURCE_CANONICAL_PAYLOAD_SHA256,
        "source_canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
        "source_canonical_status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "source_canonical_invocations": 1,
        "source_canonical_replayed": False,
        "source_baton_path": "docs/vesper-arlen/v673-v6/handoffs/lyren-moss-v673-v7-activation-candidate.md",
        "source_baton_sha256_exact_git_blob": SOURCE_BATON_SHA256,
        "source_baton_words_declared": 18338,
        "live_activation_baton_sha256_rejected": LIVE_BATON_SHA256_REJECTED,
        "live_activation_digest_state": "RETAINED_EXTERNAL_TRANSCRIPTION_FAILURE_ZERO_CREDIT",
        "live_activation_digest_recovery": "Exact Git blob, committed baton receipt, final owner manifest, final delta manifest, and content seal agree on the accepted digest.",
        "source_repository_truth": {
            "effective_negatives": 37436,
            "methods": 23764,
            "failed_witnesses": 9097,
            "bounded_passing_witnesses": 11373,
            "open_gaps": 303,
            "exact_gates": 296,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
        "lyren_startup_overlay": {
            "new_operational_failures": len(STARTUP_METHODS),
            "effective_negatives": 37436 + len(STARTUP_METHODS),
            "effective_methods": 23764 + len(STARTUP_METHODS),
            "failed_witnesses": 9097 + len(STARTUP_METHODS),
            "bounded_passing_witnesses": 11373 + len(STARTUP_METHODS),
        },
        "identity_boundary": IDENTITY_BOUNDARY,
        "authority_boundary": AUTHORITY_BOUNDARY,
        "validation_scope": "owner_self_scoped_delta",
        "same_owner_not_independent_reproduction": True,
    }
    write_json(X1 / "source-and-provenance.json", source)
    write_json(
        X1 / "inherited-revalidations.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "selected_count": len(inherited),
            "current_novelty_credit": 0,
            "automatic_completion_credit": 0,
            "rows": inherited,
        },
    )
    write_json(
        X1 / "proposals.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "proposal_count": len(proposals),
            "declared_chain_before": 6470,
            "declared_chain_after": 6510,
            "expected_outcome_counts": outcome_plan,
            "planning_only": True,
            "outcomes_observed": False,
            "proposals": proposals,
        },
    )
    write_json(X1 / "semantic-neighbor-audit.json", audit)
    write_json(X1 / "portfolio-freeze.json", portfolio)
    write_json(
        X1 / "approval-split.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "safe_now": len(portfolio["safe_now"]),
            "candidate": len(portfolio["candidate"]),
            "exact_approval": len(portfolio["exact_approval"]),
            "blocked": len(portfolio["blocked"]),
            "exact_executed": 0,
            "blocked_executed": 0,
            "classification_boundary": "Exact and blocked rows remain visible and unexecuted; broad warmth or filesystem permission does not open action-specific external or authority gates.",
        },
    )
    write_json(
        X1 / "practice-lens-screen.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "lenses": [
                {"lens": "communications-history collections registrar", "state": "bounded_learning_lens", "real_practice": False},
                {"lens": "paper-tape conservation documentation analyst", "state": "bounded_learning_lens", "real_practice": False},
                {"lens": "software evidence librarian", "state": "bounded_learning_lens", "real_practice": False},
            ],
            "successor_recommendation": {
                "count": 1,
                "lens": "synthetic historical loom pattern-chain documentation and provenance assurance",
                "completion_credit": 0,
            },
            "real_people_messages_objects_or_measurements": 0,
            "professional_authority": False,
            "boundary": "Learning lenses only; no employment, qualification, competence, treatment, engineering, archival, legal, cultural, or Maori-authority claim.",
        },
    )
    write_json(
        X1 / "official-source-plan.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "sources": OFFICIAL_SOURCES,
            "network_execution_in_x1": False,
            "source_check_was_read_only": True,
            "boundary": "Sources supply vocabulary and refusal constraints only; they are not observations, endorsement, authority, or independent validation.",
        },
    )
    write_json(
        X1 / "selected-toolchain-plan.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "target": 3,
            "installation_performed_in_x1": False,
            "candidates": [
                {"name": "rfc8785", "purpose": "bounded deterministic JSON comparison", "version": "resolve_current_pypi_metadata_in_x2", "required": True},
                {"name": "jsonschema", "purpose": "bounded local schema validation", "version": "resolve_current_pypi_metadata_in_x2", "required": True},
                {"name": "networkx", "purpose": "bounded provenance and card DAG checks", "version": "resolve_current_pypi_metadata_in_x2", "required": True},
            ],
            "gates": ["relevance", "integrity", "license", "lifecycle", "compatibility", "wheel hash", "D-isolation", "smoke", "rollback"],
            "shared_prefix_mutation": False,
            "quota_is_not_install_authority": True,
        },
    )
    write_json(
        X1 / "method-flow-startup.json",
        {
            "schema": "ghc.family.method-flow-startup.v1",
            "owner": OWNER,
            "phase": PHASE,
            "execution_authority": "owner_self_scoped_delta",
            "inherited_vesper_operational_failures": 22,
            "current_startup_method_count": len(STARTUP_METHODS),
            "methods": [
                {
                    "method_id": method_id,
                    "title": title,
                    "failure_signature": failure,
                    "state": "preferred",
                    "candidate_workaround": recovery,
                    "passing_witness": recovery,
                    "recurrence_guard": recovery,
                    "retained_negative_id": f"NEG-{method_id}",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "rollback": "Stop the affected bounded operation, preserve exact repository state, and return to the last verified anchor.",
                    "protected_gates": ["privacy", "source integrity", "sibling lane integrity", "one-shot canonical", "Stage 20"],
                }
                for method_id, title, failure, recovery in STARTUP_METHODS
            ],
            "failed_witnesses_retained": len(STARTUP_METHODS),
            "bounded_recoveries_passed": len(STARTUP_METHODS),
            "boundary": "Workflow evidence only; recovery erases no failure and supplies no empirical, professional, authority, independent, or Stage 20 credit.",
        },
    )
    write_json(
        X1 / "threat-model.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "threats": [
                {"threat": "x1 contamination by x2 output", "guard": "planning-only paths and immutable direct-child commit", "rollback": "remove uncommitted owner output and rebuild x1"},
                {"threat": "real message or identity ingestion", "guard": "invented fixtures, zero-row adapter, rejecting mutation", "rollback": "quarantine artifact and stop"},
                {"threat": "professional or authority conversion", "guard": "explicit proxy and exact-gate labels", "rollback": "retain open or exact gate"},
                {"threat": "sibling or shared mutation", "guard": "one Lyren sparse allowlist", "rollback": "stop without cross-lane action"},
                {"threat": "canonical replay", "guard": "exclusive external receipt latch", "rollback": "retain first receipt and stop"},
                {"threat": "premature successor contact", "guard": "terminal route gate and one-send duplicate guard", "rollback": "PREPARED_NOT_SENT"},
            ],
            "exhaustive_security": False,
            "external_review": False,
        },
    )
    write_json(
        X1 / "open-gate-plan.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "open_gaps_inherited": 303,
            "exact_gates_inherited": 296,
            "planned_new_open_gap_contracts": 2,
            "planned_new_exact_gate_contracts": 2,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": AUTHORITY_BOUNDARY,
        },
    )
    write_json(
        X1 / "route-plan.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "current_endpoint_kind": "main_task",
            "prospective_exact_title": "Ilyra Fen",
            "prospective_phase": "v673-v8",
            "precontact_performed": False,
            "send_attempts": 0,
            "tavian_state": "ON_STANDBY",
            "task_creation_or_fork": False,
            "required_terminal_conditions": ["clean pushed exact final", "fresh-live equality", "one successful owner-scoped canonical pass", "fresh roster and auth reread", "unique exact-title resolution", "immediate target reread", "one normal non-error acknowledgement"],
        },
    )
    overview_lines = [
        "# Lyren Moss v673-v7 planning-only x1",
        "",
        IDENTITY_BOUNDARY,
        "",
        AUTHORITY_BOUNDARY,
        "",
        "## Exact source and lifecycle",
        "",
        f"This x1 starts only from immutable Vesper final `{SOURCE_FINAL}` on `{SOURCE_BRANCH}`. Vesper's exact x1, evidence, final, canonical payload, and canonical receipt remain inherited read-only evidence. The live activation's baton digest mismatch is retained as a successor-visible external transcription failure; the exact Git blob and four independent committed records establish the accepted baton digest. No Vesper aggregate was replayed.",
        "",
        "## Distinct bounded practice",
        "",
        "The new practice is synthetic historical punched-paper telegraph documentation and provenance assurance. Every tape, hole, codeword, segment, message token, office role, time, custody transition, correction, and rights state will be invented. The phase will use no real telegram, message content, person, station, equipment, collection, measurement, credential, key, right, or authority act. Communications-history registrar, paper-tape conservation documentation analyst, and software evidence librarian are learning lenses only.",
        "",
        "## Proposal and portfolio freeze",
        "",
        "Twenty immediate-predecessor contracts are selected for exact Git-blob integrity revalidation at zero novelty and completion credit. Forty substantively new Lyren contracts are planned with expected dispositions of twenty-eight completed, eight represented, two open gaps, and two exact gates. Expected dispositions are not observed outcomes. The declared chain would move from 6,470 to 6,510 only when the x1 freeze is committed; the inaccessible universal canonical-row mapping remains an open gap.",
        "",
        "The portfolio freezes sixty bounded safe-now executions, thirty bounded candidate executions, twenty exact-approval packets, ten blocked packets, twenty repo-local skill builds, ten family-current runner specifications, sixty owner CLEAN/FIX/REFINE tasks, and successor recommendations of ten skills, ten runners, thirty refinements, and one practice. Exact and blocked packets remain unexecuted. Floors guide useful work but never justify filler, unsafe actions, external writes, or authority promotion.",
        "",
        "## Evidence plan",
        "",
        "After x1 is committed, pushed, clean, zero-divergent, and fresh-four-way equal, x2 may build only the declared Lyren files. Each completed contract needs an invented positive control and four retained invalid mutations. Represented contracts must retain their real-world gap. Open gaps and exact gates remain unresolved. The phase will produce deterministic JSON, a four-tier card deck, an accessible static report, exact Git-blob manifests, a retained-negative register, Method Flow cards, and a compact prepared baton. Same-owner checks under shared infrastructure are never independent reproduction.",
        "",
        "## Sources and tools",
        "",
        "ITU-T S.1, the BIPM SI Brochure, W3C PROV-O, RFC 8785, W3C table guidance, and New Zealand Privacy Commissioner material are vocabulary and refusal sources only. The three tool candidates are rfc8785, jsonschema, and networkx. Their exact current versions, wheel hashes, licenses, D-isolated installation, imports, and rollback must be verified in x2 before use. Shared Python and npm prefixes are not installation targets.",
        "",
        "## Route and terminal truth",
        "",
        "Ilyra Fen v673-v8 is prospective only. No lookup or contact occurs during x1 or x2 execution. The route may be considered only after Lyren's clean pushed exact final, one successful canonical aggregate, fresh roster/auth reread, exact-title uniqueness, immediate reread, duplicate and pause guards, privacy, evidence, safety, usage, and acknowledgement checks. Tavian Sol remains on standby and is never a substitute. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.",
    ]
    write_text(X1 / "integrated-overview.md", "\n".join(overview_lines))
    write_text(
        X1 / "phase-boundaries.md",
        "# Lyren Moss v673-v7 boundaries\n\n"
        + IDENTITY_BOUNDARY
        + "\n\n"
        + AUTHORITY_BOUNDARY
        + "\n\nStrict planning-only x1 precedes every x2 artifact. Source, sibling, shared, user, and standby lanes remain read-only. The current hard owner-file ceiling is 2,000 and the current total commit ceiling is eight. Counts are ceilings or useful floors, never filler authority.\n",
    )
    write_json(
        X1 / "build-receipt.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "mode": "planning_only_x1_build",
            "files_written": sorted(str(path.relative_to(ROOT)).replace("\\", "/") for path in X1.rglob("*") if path.is_file()),
            "proposal_count": 40,
            "inherited_revalidation_count": 20,
            "expected_outcomes": outcome_plan,
            "x2_artifacts_written": 0,
            "source_mutated": False,
            "sibling_lanes_mutated": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    index = f"""# {OWNER} {PHASE}

- owner: `{OWNER}`
- phase: `{PHASE}`
- source branch: `{SOURCE_BRANCH}`
- source final: `{SOURCE_FINAL}`
- lifecycle state: `PLANNING_ONLY_X1_PRECOMMIT`
- validation scope: `owner_self_scoped_delta`
- prospective successor: `Ilyra Fen v673-v8` after the exact terminal gate only
- terminal verdict: `NOT_READY_FOR_STAGE_20`

{IDENTITY_BOUNDARY}

{AUTHORITY_BOUNDARY}

Current owner paths are under `docs/lyren-moss/v673-v7/`, the four new phase scripts, three focused tests, and this reference. Vesper and every other owner lane remain read-only. Exact and blocked packets remain held. The live baton-digest mismatch is retained at zero credit; exact Git-blob evidence controls. No successor has been precontacted.
"""
    write_text(INDEX_REF, index)


def staged_paths() -> list[str]:
    return [
        line
        for line in run_git("diff", "--cached", "--name-only", "--diff-filter=ACMRT").decode("utf-8").splitlines()
        if line
    ]


def staged_blob(path: str) -> bytes:
    return run_git("show", f":{path}")


def privacy_findings(paths: list[str]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    user_path = "C:" + "\\" + "Users" + "\\"
    archive_path = "D:" + "\\" + "GHC-Archives" + "\\"
    secret_assignment = re.compile(r"(?i)(password|secret|token|api[_-]?key)\s*[:=]\s*['\"][^'\"]+['\"]")
    uuid_shape = re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b")
    for path in paths:
        if not path.startswith(("docs/lyren-moss/v673-v7/", "ghc-family-index/references/v673-v7-lyren-moss.md")):
            continue
        text = staged_blob(path).decode("utf-8", "replace")
        checks = {
            "private_absolute_user_path": user_path in text or archive_path in text,
            "raw_task_or_thread_identifier": bool(uuid_shape.search(text)),
            "credential_or_secret_assignment": bool(secret_assignment.search(text)),
        }
        for category, hit in checks.items():
            if hit:
                findings.append({"path": path, "class": category})
    return findings


def finalize_staged() -> None:
    paths = staged_paths()
    if not paths:
        raise RuntimeError("no staged Lyren paths to review")
    allowed = (
        "docs/lyren-moss/v673-v7/",
        "ghc-family-index/references/v673-v7-lyren-moss.md",
        "scripts/build_ghc_family_lyren_moss_v673_v7_",
        "scripts/validate_ghc_family_lyren_moss_v673_v7_final.py",
        "tests/test_ghc_family_lyren_moss_v673_v7_",
    )
    unexpected = [path for path in paths if not path.startswith(allowed)]
    if unexpected:
        raise RuntimeError(f"unexpected staged paths: {unexpected}")
    findings = privacy_findings(paths)
    write_json(
        VALIDATION / "x1-staged-review.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "source_final": SOURCE_FINAL,
            "staged_path_count_before_review_receipts": len(paths),
            "staged_paths": paths,
            "unexpected_paths": unexpected,
            "deletions": [],
            "x2_paths": [path for path in paths if path.startswith("docs/lyren-moss/v673-v7/x2/")],
            "passed": not unexpected and not any(path.startswith("docs/lyren-moss/v673-v7/x2/") for path in paths),
        },
    )
    write_json(
        VALIDATION / "x1-staged-privacy.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "classes": ["private_absolute_user_path", "raw_task_or_thread_identifier", "credential_or_secret_assignment"],
            "confirmed_hits": findings,
            "confirmed_hit_count": len(findings),
            "passed": not findings,
            "complete_privacy_assurance": False,
        },
    )
    if findings:
        raise RuntimeError(f"privacy findings: {findings}")


def build_manifest() -> None:
    paths = [path for path in staged_paths() if path != "docs/lyren-moss/v673-v7/validation/x1-manifest.json"]
    if not paths:
        raise RuntimeError("no staged paths for x1 manifest")
    entries = []
    for path in sorted(paths):
        data = staged_blob(path).replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        entries.append(
            {
                "path": path,
                "bytes": len(data),
                "sha256_normalized_lf": hashlib.sha256(data).hexdigest(),
            }
        )
    write_json(
        VALIDATION / "x1-manifest.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "source_final": SOURCE_FINAL,
            "hash_domain": "normalized_lf_exact_git_index_blob",
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": ["docs/lyren-moss/v673-v7/validation/x1-manifest.json"],
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["build", "finalize-staged", "manifest"], nargs="?", default="build")
    args = parser.parse_args()
    if args.mode == "build":
        build()
    elif args.mode == "finalize-staged":
        finalize_staged()
    else:
        build_manifest()


if __name__ == "__main__":
    main()
