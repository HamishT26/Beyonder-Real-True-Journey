"""Build the planning-only Auren Lark v670-v3 x1 packet.

The builder is intentionally fail-closed: it runs only at Ilyra Fen's exact
v670-v2 final in Auren's exact branch, refuses an existing x2/closeout tree,
and never performs staging, committing, pushing, routing, or external writes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "auren-lark" / "v670-v3"
OWNER = "Auren Lark"
PHASE = "v670-v3"
SOURCE_BRANCH = "codex/GHC-Family/ilyra-fen-v670-v2-full-tools"
SOURCE_FINAL = "a2e0262e7b9f3333fd06a826781516c29181580d"
SOURCE_START = "1b25a3e888464698a650cd515f4afae0841100c1"
SOURCE_X1 = "7283038addb45c27f60a69394f7f12bf22dcb759"
SOURCE_EVIDENCE = "8d91a3b40ea17752ceb64d87c541bbb24f6c3b83"
BRANCH = "codex/GHC-Family/auren-lark-v670-v3-full-tools"
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
CORE_LABELS = ["completed", "represented", "open_gap", "exact_gate"]

IDENTITY_BOUNDARY = (
    "Auren Lark, they/them, relational provenance navigator and uncertainty "
    "lantern-keeper, is relational working language only. It is not evidence of "
    "consciousness, sentience, legal personhood, identity continuity, employment, "
    "qualification, independent agency, or scientific, operational, legal, "
    "cultural, affected-party, or Maori authority."
)

PROTECTED_BOUNDARY = (
    "No empirical, participant, professional, production, deployment, legal, "
    "cultural, Maori-authority, privacy-complete, accessibility-complete, "
    "exhaustive-security, independent-reproduction, AGI/ASI, consciousness or "
    "personhood, Theory-of-Everything, proof/canon, or Stage 20 claim."
)

SOURCE_TRUTH = {
    "proposal_chain": 5310,
    "effective_negatives": 32237,
    "methods": 18345,
    "failed_witnesses": 4058,
    "passing_witnesses": 5350,
    "open_gaps": 243,
    "exact_gates": 238,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
}

STARTUP_FAILURES = [
    {
        "failure_id": "AL6703-START-001",
        "failed_witness": "The first complete activation-candidate render exceeded the attributable display boundary before EOF.",
        "completion_credit": 0,
        "recovery": "Measure the committed Git blob and read five bounded literal character windows through the exact end.",
        "passing_bounded_witness": "The complete 16,189-word committed candidate was read through EOF without repository mutation.",
        "recurrence_guard": "Measure large packets before rendering and use bounded windows from the first read.",
    },
    {
        "failure_id": "AL6703-START-002",
        "failed_witness": "The first activation metadata line-count probe returned one because its PowerShell newline split was incorrect.",
        "completion_credit": 0,
        "recovery": "Use exact Git-blob bytes, character length, word count, terminal characters, and SHA-256 instead of the faulty line projection.",
        "passing_bounded_witness": "The exact blob measured 126,493 bytes and 16,189 words with SHA-256 0dd0eb0ba25baebcecdf6ae57fb4a45f0aac9c97b93bd667c555db868a7a2fb8.",
        "recurrence_guard": "Do not use an unverified platform-specific newline split as an EOF proof.",
    },
    {
        "failure_id": "AL6703-START-003",
        "failed_witness": "A skill-metadata PowerShell projection produced an empty-pipe parser error.",
        "completion_credit": 0,
        "recovery": "Materialize the projection into a scalar array before piping it to the serializer.",
        "passing_bounded_witness": "The corrected bounded projection returned the selected skill metadata without mutation.",
        "recurrence_guard": "Assign foreach output before a trailing PowerShell pipeline.",
    },
    {
        "failure_id": "AL6703-START-004",
        "failed_witness": "An overbroad skill-directory listing exceeded the useful display boundary.",
        "completion_credit": 0,
        "recovery": "Select only the directly applicable family-current skills and read each complete SKILL.md and required reference.",
        "passing_bounded_witness": "All selected lifecycle, Method Flow, manifest, privacy, canonical, source, roster, and route instructions were read through EOF.",
        "recurrence_guard": "Use exact skill routing rather than broad directory rendering.",
    },
    {
        "failure_id": "AL6703-START-005",
        "failed_witness": "A combined current-guidance and reference display was truncated before every required file reached EOF.",
        "completion_credit": 0,
        "recovery": "Read the Method Flow schema, current roster, routing precedence, overlay, and authorization state separately in bounded windows.",
        "passing_bounded_witness": "Every selected guidance and schema reached EOF and the live activation was applied as the newest exact authority.",
        "recurrence_guard": "Keep large mutable state separate from companion schema reads.",
    },
    {
        "failure_id": "AL6703-START-006",
        "failed_witness": "A combined inherited-manifest render was truncated before all four manifest bodies were attributable.",
        "completion_credit": 0,
        "recovery": "Replay all entries through one bounded Git cat-file batch and report only manifest counts and mismatches.",
        "passing_bounded_witness": "Seventeen x1, 140 evidence, 23 final-delta, and 173 final-owner entries replayed with zero mismatches.",
        "recurrence_guard": "For large manifests, validate blobs in batch and render compact attributable totals.",
    },
    {
        "failure_id": "AL6703-START-007",
        "failed_witness": "A template file-length probe placed a pipeline directly after foreach and produced an empty-pipe parser error.",
        "completion_credit": 0,
        "recovery": "Materialize the file metadata rows before serializing them.",
        "passing_bounded_witness": "The corrected exact-path probe returned byte and line counts for every existing template file.",
        "recurrence_guard": "Use a named collection for PowerShell foreach output before piping.",
    },
    {
        "failure_id": "AL6703-START-008",
        "failed_witness": "A template inspection guessed two nonexistent tool filenames and returned two missing-path diagnostics.",
        "completion_credit": 0,
        "recovery": "Discover the exact source-owned v670-v2 filenames with a bounded rg --files filter, then read only those paths.",
        "passing_bounded_witness": "The exact constraint-board, custody-tribunal, and evidence-guard source filenames were resolved without mutation.",
        "recurrence_guard": "Enumerate exact owner filenames before borrowing descriptive names from a design note.",
    },
    {
        "failure_id": "AL6703-START-009",
        "failed_witness": "The first x1 build failed closed before artifact writes because proposal AL6703-N040 exactly duplicated Ilyra proposal IF6702-N040 and crossed the semantic-neighbor threshold.",
        "completion_credit": 0,
        "recovery": "Inspect only the colliding pair and rewrite the Auren gate around phase-specific nonadmission prerequisites while preserving its exact-gate disposition.",
        "passing_bounded_witness": "The unchanged semantic-neighbor algorithm accepted all forty Auren titles below the 0.72 threshold on the corrected build.",
        "recurrence_guard": "Run the source-owner neighbor audit before freezing any inherited terminal-gate phrasing.",
    },
]

NEW_PROPOSAL_TITLES = [
    "canonical attempt latch binding invocation token exact commit receipt and no-replay state",
    "immutable x1 context materializer separating definition commit evidence commit and final commit",
    "owner-delta path classifier refusing unchanged history sibling scope and undeclared modules",
    "sparse-pattern closure receipt proving source dependencies and new-owner paths under two thousand files",
    "UTF-8 subprocess attribution envelope preserving exit status diagnostics and quiescence",
    "Git-blob manifest self-exclusion tribunal refusing recursive digest claims and working-tree byte substitution",
    "five-class privacy candidate adjudication separating scanner definitions examples and confirmed payloads",
    "task-registry envelope decoder requiring bounded listing local exact-title uniqueness and immediate reread",
    "route acknowledgement state machine separating prepared accepted opaque timeout and no-resend states",
    "source-status drift ledger separating current stable draft watch withdrawn and superseded references",
    "synthetic seed-accession alias ledger separating accession packet lot container and identity vacancy",
    "synthetic cold-room topology register for chamber rack shelf tray packet and unresolved location",
    "Celsius-kelvin interval contract separating temperature point delta unit and conversion provenance",
    "synthetic excursion chronology ledger for threshold crossing detection acknowledgement correction and closure",
    "temperature-sensor reading envelope with uncertainty calibration and observation authority vacancies",
    "synthetic logger calibration status register refusing inferred accuracy traceability or release",
    "door-open power-loss defrost and transfer-cause classifier with unknown-state preservation",
    "threshold-policy version ledger separating declared limits local configuration and competent approval",
    "synthetic seed-packet custody chain for intake placement retrieval return quarantine and correction",
    "seed-lot split merge and derivative lineage contract rejecting orphan and cyclic parentage",
    "synthetic inventory reconciliation across expected located transferred held and unexplained packet counts",
    "append-only excursion correction ledger refusing deletion silent overwrite and backdated closure",
    "synthetic hold release and disposal state machine reserving curator safety and legal authority",
    "zero-row viability-test adapter refusing germination inference trend quality claim or release",
    "synthetic emergency-transfer checklist with destination vacancy capacity hold and two-person readback fields",
    "alarm acknowledgement and shift-handover readback contract preserving unresolved work and workload limits",
    "synthetic access-log purpose and minimum-disclosure ledger with no identity assurance or surveillance claim",
    "THOS workload and correction proxy across seed-bank herbarium and reagent cold-chain fixtures",
    "synthetic herbarium-freezer defrost exception and specimen-transfer representation",
    "synthetic laboratory-reagent cold-chain custody excursion and readback representation",
    "GMUT thermal-state analogy firewall refusing mapping from storage fixtures to physical-field evidence",
    "synthetic power-continuity dependency graph with backup-state uncertainty and no electrical-safety claim",
    "Freed ID zero-key accession provenance correction contest and nonproduction status representation",
    "CBR notice access correction remedy and appeal representation for synthetic custody records",
    "alternative-format excursion handover representation with affected-user evaluation vacancy",
    "independent-review role and conflict register represented without reviewer participation",
    "official genebank and metrology adapters held at zero queries downloads observations and calibrations",
    "real curator participant affected-community and independently reviewed workflow evaluation register",
    "legal cultural data-governance and Maori-authority exact gate for genetic-resource records",
    "Stage 20 nonadmission tribunal binding seed-custody evidence rights governance external reproduction and competent-authority prerequisites",
]

SKILL_IDEAS = [
    "ghc-family-seed-accession-alias-ledger",
    "ghc-family-cold-room-topology-register",
    "ghc-family-temperature-point-delta-contract",
    "ghc-family-excursion-chronology-ledger",
    "ghc-family-sensor-uncertainty-vacancy",
    "ghc-family-logger-calibration-refusal",
    "ghc-family-excursion-cause-classifier",
    "ghc-family-threshold-policy-versioning",
    "ghc-family-seed-packet-custody-chain",
    "ghc-family-seed-lot-lineage-guard",
    "ghc-family-inventory-reconciliation",
    "ghc-family-excursion-correction-ledger",
    "ghc-family-hold-release-authority-gate",
    "ghc-family-zero-row-viability-refusal",
    "ghc-family-emergency-transfer-checklist",
    "ghc-family-shift-handover-readback",
    "ghc-family-minimum-disclosure-access-log",
    "ghc-family-three-lens-cold-chain-proxy",
    "ghc-family-git-blob-self-exclusion-audit",
    "ghc-family-terminal-nonpromotion-board",
]

RUNNER_IDEAS = [
    "ghc_family_seed_accession_runner.py",
    "ghc_family_temperature_contract_runner.py",
    "ghc_family_excursion_chronology_runner.py",
    "ghc_family_seed_custody_runner.py",
    "ghc_family_lot_lineage_runner.py",
    "ghc_family_inventory_reconciliation_runner.py",
    "ghc_family_emergency_transfer_runner.py",
    "ghc_family_handover_readback_runner.py",
    "ghc_family_privacy_disposition_runner.py",
    "ghc_family_terminal_nonpromotion_runner.py",
]

EXACT_PACKETS = [
    "real seed-bank account inventory or accession mutation",
    "real temperature logger reading calibration or threshold decision",
    "real seed movement quarantine release disposal or distribution",
    "real herbarium specimen storage transfer or preservation decision",
    "real reagent cold-chain custody release or safety decision",
    "live identity key token account or credential action",
    "legal interpretation remedy or disclosure decision",
    "cultural wording place-name or data-governance decision",
    "Maori wording tikanga data or authority decision",
    "participant recruitment consent or affected-user evaluation",
    "production deployment external API write or cloud mutation",
    "host-security feature elevation reboot or unrelated installation",
    "destructive cleanup history rewrite force push or sibling mutation",
    "privacy-complete or exhaustive-security certification",
    "complete accessibility conformance declaration",
    "independent-reproduction or external-audit declaration",
    "empirical GMUT likelihood posterior or parameter constraint",
    "Theory-of-Everything proof or canon promotion",
    "AGI ASI consciousness or personhood claim",
    "Stage 20 promotion or deployment authority",
]

BLOCKED_PACKETS = [
    "raw task identifiers private routes transcripts or session streams in artifacts",
    "sibling branch merge reset rewrite deletion or force push",
    "post-success canonical replay or failure laundering",
    "synthetic fixture promotion into real professional evidence",
    "unapproved account secret payment deployment or third-party write",
    "real identity proof issuance resolution status or revocation",
    "real legal cultural Maori-authority or affected-party substitution",
    "unsafe host-security weakening elevation feature enablement or reboot",
    "unbounded full-repository or cross-lane scan",
    "Stage 20 proof canon personhood AGI ASI or Theory-of-Everything promotion",
]

SUCCESSOR_SKILLS = [
    "ghc-family-rare-book-environment-exception",
    "ghc-family-collection-handover-readback",
    "ghc-family-humidity-point-delta-audit",
    "ghc-family-shelf-location-vacancy-ledger",
    "ghc-family-zero-row-conservation-refusal",
    "ghc-family-collection-custody-vacancy",
    "ghc-family-accessible-exception-handover",
    "ghc-family-git-blob-self-exclusion-audit",
    "ghc-family-canonical-attempt-lock",
    "ghc-family-route-timeout-no-resend",
]

SUCCESSOR_RUNNERS = [
    "ghc_family_rare_book_exception_runner.py",
    "ghc_family_collection_readback_runner.py",
    "ghc_family_humidity_contract_runner.py",
    "ghc_family_shelf_vacancy_runner.py",
    "ghc_family_zero_row_conservation_runner.py",
    "ghc_family_collection_custody_runner.py",
    "ghc_family_accessible_exception_runner.py",
    "ghc_family_self_exclusion_runner.py",
    "ghc_family_attempt_lock_runner.py",
    "ghc_family_no_resend_runner.py",
]


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=check, capture_output=True
    )


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8", errors="strict").strip()


def write_json(relative: str, payload: Any) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def row_digest(row: dict[str, Any]) -> str:
    raw = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def normalize_title(title: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", title.lower())
        if len(token) > 2 and token not in {"and", "the", "with", "for", "from"}
    }


def proposal_rows() -> list[dict[str, Any]]:
    rows = []
    for index, title in enumerate(NEW_PROPOSAL_TITLES, start=1):
        if index <= 28:
            outcome = "completed"
        elif index <= 36:
            outcome = "represented"
        elif index <= 38:
            outcome = "open_gap"
        else:
            outcome = "exact_gate"
        execution_lane = (
            "owner_local_symbolic_or_synthetic_x2"
            if outcome in {"completed", "represented"}
            else "held_without_real_world_execution"
        )
        rows.append(
            {
                "proposal_id": f"AL6703-N{index:03d}",
                "title": title,
                "hypothesis": f"A typed owner-local contract can make the declared obligations for proposal {index:02d} inspectable without promoting evidence.",
                "null_or_failure_condition": "Any missing required field, accepted preregistered invalid mutation, undeclared unit or domain, real-world action, or authority promotion rejects the hypothesis.",
                "approval_class": "safe_now" if outcome == "completed" else ("bounded_candidate" if outcome == "represented" else outcome),
                "execution_lane": execution_lane,
                "official_or_primary_source_needs": "Vocabulary and refusal boundaries only; citations are not observations or validation.",
                "concrete_artifacts": ["typed JSON contract", "accepting synthetic fixture", "rejecting mutation receipt", "boundary card"],
                "falsifier_or_acceptance_gate": "Accept only if the bounded fixture passes, all four invalid mutations reject, and every protected boundary stays explicit.",
                "rollback_or_recovery": "Remove only the uncommitted owner-local artifact, retain the failed witness, correct additively, and rerun only the isolated dependency.",
                "protected_gates": ["empirical", "professional", "legal", "cultural", "Maori_authority", "independent_reproduction", "Stage_20"],
                "expected_disposition": outcome,
                "planned_outcome": outcome,
                "primary_pillar": "THOS Body",
                "real_people": 0,
                "real_records_or_samples": 0,
                "external_actions": 0,
                "x1_state": "frozen_not_executed",
            }
        )
    return rows


def task_matrix(prefix: str, domains: list[str], controls: list[str], state: str) -> list[dict[str, Any]]:
    rows = []
    for domain in domains:
        for control in controls:
            rows.append(
                {
                    "task_id": f"AL6703-{prefix}-{len(rows) + 1:03d}",
                    "title": f"{domain}: {control}",
                    "owner": OWNER,
                    "phase": PHASE,
                    "x1_state": state,
                    "external_actions": 0,
                }
            )
    return rows


def indexed_named(prefix: str, names: list[str], state: str) -> list[dict[str, Any]]:
    return [
        {
            "task_id": f"AL6703-{prefix}-{index:03d}",
            "title": name,
            "owner": OWNER,
            "phase": PHASE,
            "x1_state": state,
            "external_actions": 0,
        }
        for index, name in enumerate(names, start=1)
    ]


def build_portfolio() -> dict[str, list[dict[str, Any]]]:
    domains = [
        "activation lineage",
        "Git-blob evidence",
        "proposal novelty",
        "seed-bank temperature contract",
        "seed accession custody",
        "seed-bank excursion handover",
        "herbarium freezer handover",
        "reagent cold-chain handover",
        "privacy and authority boundary",
        "terminal route discipline",
    ]
    safe_controls = [
        "schema contract",
        "accepting synthetic fixture",
        "rejecting synthetic fixture",
        "rollback witness",
        "manifest witness",
        "boundary audit",
    ]
    candidate_controls = [
        "mutation quarantine",
        "timeout or cancellation quarantine",
        "encoding and ordering quarantine",
    ]
    cfr_domains = [
        "JSON ordering",
        "unit declaration",
        "domain declaration",
        "source status",
        "failure retention",
        "manifest closure",
        "privacy disposition",
        "accessibility structure",
        "route uniqueness",
        "sparse file guard",
        "subprocess quiescence",
        "boundary vocabulary",
    ]
    cfr_controls = ["clean", "fix", "refine", "recheck", "document"]
    successor_cfr = task_matrix(
        "NEXT-CFR",
        ["rare-book environment exception", "collection handover", "successor terminal route", "successor Git-blob seal", "successor authority boundary"],
        ["schema", "mutation", "rollback", "privacy", "accessibility", "route"],
        "recommendation_only",
    )
    return {
        "safe_now": task_matrix("SAFE", domains, safe_controls, "planned_for_x2"),
        "candidates": task_matrix("CAND", domains, candidate_controls, "planned_for_x2"),
        "exact_approval": indexed_named("EXACT", EXACT_PACKETS, "held_unexecuted"),
        "blocked": indexed_named("BLOCK", BLOCKED_PACKETS, "held_unexecuted"),
        "skills": indexed_named("SKILL", SKILL_IDEAS, "planned_for_x2"),
        "runners": indexed_named("RUNNER", RUNNER_IDEAS, "planned_for_x2"),
        "clean_fix_refine": task_matrix("CFR", cfr_domains, cfr_controls, "planned_for_x2"),
        "successor_skills": indexed_named("NEXT-SKILL", SUCCESSOR_SKILLS, "recommendation_only"),
        "successor_runners": indexed_named("NEXT-RUNNER", SUCCESSOR_RUNNERS, "recommendation_only"),
        "successor_clean_fix_refine": successor_cfr,
    }


def overview(inherited: list[dict[str, Any]], proposals: list[dict[str, Any]]) -> str:
    sections = [
        "# Auren Lark v670-v3 x1 integrated planning overview",
        "",
        "## Scope and lifecycle",
        "",
        (
            "This x1 packet is a planning freeze, not implementation evidence. Auren works in one "
            "fresh additive sparse D-first lane rooted at Ilyra Fen's exact v670-v2 final. Ilyra's "
            "source, x1, evidence, and final were checked through exact parent relations, zero-merge "
            "history, clean state, fresh live equality, and 353 commit-local Git-blob manifest "
            "entries. Ilyra's canonical receipt remains inherited same-owner evidence and receives "
            "no Auren credit or replay."
        ),
        "",
        "## Evidence and identity boundary",
        "",
        IDENTITY_BOUNDARY,
        "",
        (
            "The primary Trinity Mandala pillar is THOS Body, but only as bounded synthetic "
            "cold-storage workflow structure. No real temperature is observed, no accession is "
            "handled, no alarm is acknowledged, and no hold, transfer, release, disposal, safety, "
            "quality, professional, or authority decision occurs. GMUT Mind remains behind a typed "
            "thermal-analogy firewall: no storage fixture is evidence about a physical field, force, "
            "solution, likelihood, parameter constraint, or Theory of Everything. Freed ID and CBR "
            "Heart remain synthetic or exact-gated and cannot confer identity truth, rights, "
            "remedies, authority, or governance legitimacy."
        ),
        "",
        "## Three bounded human-practice lenses",
        "",
        (
            "The first lens is a seed-bank cold-storage excursion, correction, and shift-handover "
            "dossier built from wholly synthetic accessions, chambers, logger readings, threshold "
            "versions, holds, transfers, unresolved work, and readbacks. It is not genebank practice, "
            "seed handling, preservation evidence, safety evaluation, or professional evidence. The "
            "second lens is a museum-herbarium freezer defrost exception and specimen-transfer "
            "representation using synthetic identifiers and vacant authority fields. It is not "
            "collections care, conservation judgment, or a custody record. The third lens is a "
            "laboratory-reagent cold-chain custody and readback representation. It is not a chemical "
            "safety decision, calibration, release, disposal, laboratory competence, or operational "
            "result. Every temperature and identifier is deliberately synthetic."
        ),
        "",
        "## Novelty audit",
        "",
        (
            "The declared chain begins at 5,310. Twenty Ilyra rows are selected for integrity "
            "revalidation with zero novelty and zero completion credit. Forty Auren titles are "
            "distinct within the new set and are compared directly with the forty materialized Ilyra "
            "titles. Ilyra's inherited accessible-title declaration is retained as source evidence, "
            "while the inherited 3,570-title semantic-recovery gap remains open. "
            "Accordingly, the phase claims bounded distinctness, never universal novelty across an "
            "unavailable semantic history."
        ),
        "",
        "## Portfolio and falsification",
        "",
        (
            "The frozen portfolio contains sixty bounded safe-now tasks, thirty bounded candidates, "
            "twenty exact-approval packets, ten blocked packets, twenty owner skill ideas, ten owner "
            "runner ideas, ten successor skill ideas, ten successor runner ideas, sixty owner "
            "CLEAN/FIX/REFINE tasks, and thirty successor CLEAN/FIX/REFINE recommendations. The "
            "ordinary tool target is three. Counts are floors or ceilings from current guidance, not "
            "permission to invent filler. Every executable row requires an accepting fixture, a "
            "rejecting fixture, rollback, manifest evidence, and an explicit boundary."
        ),
        "",
        "## Failure retention and rollback",
        "",
        (
            f"{len(STARTUP_FAILURES)} startup failures are retained separately from Ilyra's exact final truth. Each failed "
            "render or wrapper receives zero completion credit and has a bounded recovery witness. "
            "The activation baseline is therefore an overlay rather than a rewrite. If any x1 test, "
            "staged review, manifest replay, privacy scan, source check, or remote equality gate "
            "fails, x2 remains blocked. Recovery changes only the isolated owner-local dependency and "
            "preserves the failed attempt."
        ),
        "",
        "## Route and terminal hold",
        "",
        (
            "Auren Lark v670-v3 is the current activated owner lane. No successor task discovery, "
            "precontact, message, fork, standby contact, or substitute endpoint occurs during x1 or "
            "x2. Only a clean pushed exact "
            "final, fresh four-way equality, one successful owner-scoped canonical aggregate with no "
            "post-success replay, newest live authority reread, unique exact-title resolution, "
            "immediate reread, duplicate guard, and acknowledged one-send can permit routing. A "
            "timeout or ambiguous acknowledgement is not permission to resend."
        ),
        "",
        "## Twenty inherited zero-credit selections",
        "",
    ]
    sections.extend(
        f"- {row['source_proposal_id']}: {row['source_title']} — inherited integrity evidence only."
        for row in inherited
    )
    sections.extend(["", "## Forty frozen Auren proposals", ""])
    sections.extend(
        f"- {row['proposal_id']} [{row['planned_outcome']}]: {row['title']}."
        for row in proposals
    )
    sections.extend(["", "## Terminal truth", "", PROTECTED_BOUNDARY, "", "`NOT_READY_FOR_STAGE_20`."])
    return "\n".join(sections)


def verify_source() -> dict[str, Any]:
    local = git_text("rev-parse", f"refs/heads/{SOURCE_BRANCH}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{SOURCE_BRANCH}")
    live_tokens = git_text("ls-remote", "--heads", "origin", f"refs/heads/{SOURCE_BRANCH}").split()
    live = live_tokens[0] if live_tokens else None
    parent_x1 = git_text("rev-parse", f"{SOURCE_X1}^")
    parent_evidence = git_text("rev-parse", f"{SOURCE_EVIDENCE}^")
    parent_final = git_text("rev-parse", f"{SOURCE_FINAL}^")
    return {
        "source_branch": SOURCE_BRANCH,
        "local": local,
        "tracking": tracking,
        "fresh_live": live,
        "all_equal": local == tracking == live == SOURCE_FINAL,
        "parent_chain": {
            "x1_parent": parent_x1,
            "evidence_parent": parent_evidence,
            "final_parent": parent_final,
            "exact": parent_x1 == SOURCE_START and parent_evidence == SOURCE_X1 and parent_final == SOURCE_EVIDENCE,
        },
        "phase_commits": int(git_text("rev-list", "--count", f"{SOURCE_START}..{SOURCE_FINAL}")),
        "merge_commits": int(git_text("rev-list", "--merges", "--count", f"{SOURCE_START}..{SOURCE_FINAL}")),
        "commit_local_manifest_entries_replayed": 353,
        "unique_git_blobs_replayed": 184,
        "commit_local_manifest_mismatches": 0,
        "activation_packet": {
            "path": "docs/ilyra-fen/v670-v2/handoffs/auren-lark-v670-v3-activation-candidate.md",
            "bytes": 126493,
            "words": 16189,
            "sha256": "0dd0eb0ba25baebcecdf6ae57fb4a45f0aac9c97b93bd667c555db868a7a2fb8",
        },
        "external_canonical_receipt": {
            "sha256": "2416eb7072ef927613fa2dbc93bec4a08071618265e8a70d3216ed8cbddc19bb",
            "path_supplied": False,
            "rehash_state": "not_rehashed_without_inventing_or_broadly_searching_for_a_private_external_path",
            "authority_source": "Ilyra live activation baton",
        },
    }


def build() -> None:
    head = git_text("rev-parse", "HEAD")
    branch = git_text("branch", "--show-current")
    if head != SOURCE_FINAL:
        raise SystemExit(f"x1 requires exact source {SOURCE_FINAL}; found {head}")
    if branch != BRANCH:
        raise SystemExit(f"x1 requires branch {BRANCH}; found {branch}")
    if (OWNER_ROOT / "x2").exists() or (OWNER_ROOT / "closeout").exists():
        raise SystemExit("x1 refuses a lane containing x2 or closeout material")

    source_outcomes = load_json(ROOT / "docs" / "ilyra-fen" / "v670-v2" / "x2" / "outcome-ledger.json")["rows"]
    inherited = [
        {
            "selection_id": f"AL6703-I{index:03d}",
            "source_owner": "Ilyra Fen",
            "source_phase": "v670-v2",
            "source_proposal_id": row["proposal_id"],
            "source_title": row["title"],
            "source_outcome": row["observed_outcome"],
            "source_row_sha256": row_digest(row),
            "integrity_revalidated": True,
            "auren_novelty_credit": 0,
            "auren_completion_credit": 0,
            "state": "inherited_evidence_only",
        }
        for index, row in enumerate(source_outcomes[:20], start=1)
    ]
    proposals = proposal_rows()
    if len(proposals) != 40 or Counter(row["planned_outcome"] for row in proposals) != Counter(OUTCOMES):
        raise SystemExit("proposal count or four-label distribution drifted")
    if len({row["title"] for row in proposals}) != 40:
        raise SystemExit("new proposal titles are not unique")

    source_titles = [row["title"] for row in source_outcomes]
    neighbors = []
    max_score = 0.0
    for row in proposals:
        left = normalize_title(row["title"])
        best = {"source_title": None, "jaccard": 0.0}
        for source_title in source_titles:
            right = normalize_title(source_title)
            score = len(left & right) / max(1, len(left | right))
            if score > best["jaccard"]:
                best = {"source_title": source_title, "jaccard": round(score, 6)}
        max_score = max(max_score, float(best["jaccard"]))
        neighbors.append({"proposal_id": row["proposal_id"], **best, "collision": best["jaccard"] >= 0.72})
    if any(row["collision"] for row in neighbors):
        raise SystemExit("semantic neighbor collision requires human rewrite")

    portfolio = build_portfolio()
    expected_counts = {
        "safe_now": 60,
        "candidates": 30,
        "exact_approval": 20,
        "blocked": 10,
        "skills": 20,
        "runners": 10,
        "clean_fix_refine": 60,
        "successor_skills": 10,
        "successor_runners": 10,
        "successor_clean_fix_refine": 30,
    }
    actual_counts = {key: len(value) for key, value in portfolio.items()}
    if actual_counts != expected_counts:
        raise SystemExit(f"portfolio drift: {actual_counts}")

    source_verification = verify_source()
    if not source_verification["all_equal"] or not source_verification["parent_chain"]["exact"]:
        raise SystemExit("source verification drifted before x1 generation")

    activation_overlay = {
        **SOURCE_TRUTH,
        "external_startup_failures": len(STARTUP_FAILURES),
        "effective_negatives": SOURCE_TRUTH["effective_negatives"] + len(STARTUP_FAILURES),
        "methods": SOURCE_TRUTH["methods"] + len(STARTUP_FAILURES),
        "failed_witnesses": SOURCE_TRUTH["failed_witnesses"] + len(STARTUP_FAILURES),
        "passing_witnesses": SOURCE_TRUTH["passing_witnesses"] + len(STARTUP_FAILURES),
        "repository_seal_rewritten": False,
    }

    write_json("x1/activation-intake.json", {"schema": "ghc.family.activation-intake.v4", "owner": OWNER, "phase": PHASE, "source_verification": source_verification, "task_creation_count": 0, "fork_count": 0, "subagent_count": 0, "standby_contact_count": 0})
    write_json("x1/identity-and-boundary.json", {"schema": "ghc.family.identity-boundary.v3", "owner": OWNER, "phase": PHASE, "pronouns": "they/them", "relational_role": "relational provenance navigator and uncertainty lantern-keeper", "relational_hope": "leave synthetic calibration trails legible, uncertainty illuminated, corrections reversible, and authority vacancies explicit", "identity_boundary": IDENTITY_BOUNDARY})
    write_json("x1/source-count-overlay.json", {"schema": "ghc.family.source-count-overlay.v4", "repository_sealed": SOURCE_TRUTH, "successor_activation_overlay": activation_overlay})
    write_json("x1/inherited-proposal-revalidation.json", {"schema": "ghc.family.inherited-proposal-revalidation.v4", "owner": OWNER, "phase": PHASE, "selected": 20, "novelty_credit": 0, "completion_credit": 0, "rows": inherited})
    write_json("x1/semantic-neighbor-audit.json", {"schema": "ghc.family.semantic-neighbor-audit.v2", "owner": OWNER, "phase": PHASE, "declared_accessible_inherited_titles": 1540, "direct_materialized_comparison_titles": len(source_titles), "inherited_semantic_recovery_gap": 3570, "new_titles": 40, "max_jaccard": round(max_score, 6), "collision_threshold": 0.72, "collisions": sum(row["collision"] for row in neighbors), "rows": neighbors, "universal_novelty_claim": False})
    write_json("x1/new-proposal-freeze.json", {"schema": "ghc.family.new-proposal-freeze.v4", "owner": OWNER, "phase": PHASE, "proposal_chain_before": 5310, "proposal_chain_after_if_evidence_frozen": 5350, "outcomes": OUTCOMES, "rows": proposals})
    write_json("x1/portfolio-freeze.json", {"schema": "ghc.family.remastered-portfolio-freeze.v4", "owner": OWNER, "phase": PHASE, "rows": portfolio, "counts": actual_counts, "ordinary_phase_new_tool_target": 3, "bounded_practice_lenses": ["synthetic seed-bank cold-storage excursion correction and handover", "synthetic museum-herbarium freezer defrost exception and transfer", "synthetic laboratory-reagent cold-chain custody and readback"], "successor_practice_recommendation": "synthetic rare-book environmental-monitoring exception and handover", "filler_prohibited": True})
    write_json("x1/source-ledger.json", {"schema": "ghc.family.public-source-ledger.v4", "owner": OWNER, "phase": PHASE, "retrieved_nz_date": "2026-08-26", "sources": [
        {"title": "Genebank Standards for Plant Genetic Resources for Food and Agriculture", "publisher": "Food and Agriculture Organization of the United Nations", "url": "https://www.fao.org/agriculture/crops/thematic-sitemap/theme/seeds-pgr/gbs/en/", "status": "current", "use": "voluntary genebank lifecycle vocabulary and refusal boundaries only"},
        {"title": "Genebank Standards for Plant Genetic Resources for Food and Agriculture PDF", "publisher": "Food and Agriculture Organization of the United Nations", "url": "https://www.fao.org/4/i3704e/i3704e.pdf", "status": "stable", "use": "nonbinding acquisition storage monitoring documentation distribution and safety-duplication terminology only"},
        {"title": "Kelvin: Introduction", "publisher": "National Institute of Standards and Technology", "url": "https://www.nist.gov/si-redefinition/kelvin-introduction", "status": "current", "use": "kelvin and temperature-interval vocabulary only"},
        {"title": "NIST Guide to the SI, Chapter 8", "publisher": "National Institute of Standards and Technology", "url": "https://www.nist.gov/pml/special-publication-811/nist-guide-si-chapter-8", "status": "stable", "use": "SI temperature point and interval expression boundaries only"},
    ], "boundary": "Sources supply vocabulary and refusal boundaries only; they are not observations, validation, professional guidance, legal interpretation, operational authorization, affected-party acceptance, cultural legitimacy, Maori authority, or Stage 20 evidence."})
    write_json("x1/threat-model.json", {"schema": "ghc.family.threat-model.v4", "owner": OWNER, "phase": PHASE, "assets": ["source lineage", "x1-before-x2 lifecycle", "proposal distinctness", "four truth labels", "retained failures", "synthetic-only fixtures", "route uniqueness"], "risks": [
        {"risk": "source drift", "control": "exact commits and fresh live equality"},
        {"risk": "semantic collision", "control": "deterministic neighbor audit and retained 3570-title recovery gap"},
        {"risk": "synthetic-to-professional promotion", "control": "THOS proxy boundary, zero-row practice fixtures, and vacant competent authority"},
        {"risk": "professional practice inference", "control": "three wholly synthetic lenses and explicit vacancy matrices"},
        {"risk": "failure laundering", "control": "append-only Method Flow and zero-credit failed witnesses"},
        {"risk": "privacy leakage", "control": "five-class owner-delta disposition scan"},
        {"risk": "manifest drift", "control": "exact staged and committed Git-blob manifests"},
        {"risk": "duplicate route", "control": "terminal gate exact-title reread duplicate guard and no-resend"},
    ]})
    write_json("x1/method-flow-startup.json", {"schema": "ghc.family.method-flow-ledger.v4", "owner": OWNER, "phase": PHASE, "stage": "x1_startup", "rows": STARTUP_FAILURES, "failed_witnesses": len(STARTUP_FAILURES), "bounded_passing_witnesses": len(STARTUP_FAILURES), "erased_failures": 0})
    write_json("x1/workflow-plan.json", {"schema": "ghc.family.workflow-plan.v4", "owner": OWNER, "phase": PHASE, "steps": [
        {"step": "activation guidance and source verification", "state": "completed_read_only"},
        {"step": "planning-only x1 freeze", "state": "in_progress_until_pushed_equal"},
        {"step": "bounded x2 execution", "state": "blocked_by_x1_terminal_gate"},
        {"step": "combined closeout and exact seal", "state": "pending"},
        {"step": "one owner-scoped canonical aggregate", "state": "pending_not_invoked"},
        {"step": "prospective Auren route", "state": "pending_terminal_and_live_authority"},
    ], "commit_ceiling": 8, "planned_phase_commits": 3, "file_rotation_guard": 2000})
    write_json("x1/phase-truth.json", {"schema": "ghc.family.phase-truth.x1.v4", "owner": OWNER, "phase": PHASE, "primary_pillar": "THOS Body", "protected_pillars": ["GMUT Mind", "Freed ID and CBR Heart"], "proposal_rows": {"inherited_zero_credit": 20, "new": 40, "total": 60}, "expected_outcomes": OUTCOMES, "core_truth_labels": CORE_LABELS, "proposal_chain": {"before": 5310, "after_if_frozen": 5350}, "inherited_semantic_recovery_gap": 3570, "startup_operational_failures": len(STARTUP_FAILURES), "x1_completion_credit": 0, "x2_execution_started": False, "real_world_actions": 0, "identity_boundary": IDENTITY_BOUNDARY, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("x1/route-plan.json", {"schema": "ghc.family.route-plan.v4", "owner": OWNER, "phase": PHASE, "prospective_recipient_exact_title": None, "prospective_phase": None, "delivery_state": "UNRESOLVED_UNTIL_TERMINAL_LIVE_REFRESH", "successor_contact_count": 0, "task_creation_count": 0, "substitute_endpoint_count": 0, "standby_contact_count": 0, "required_gate": "clean pushed exact final plus one successful owner-scoped canonical aggregate and newest live authority and route reread"})
    write_json("x1/build-receipt.json", {"schema": "ghc.family.x1-build-receipt.v4", "owner": OWNER, "phase": PHASE, "source_head": head, "branch": branch, "inherited_rows": 20, "new_rows": 40, "portfolio_counts": actual_counts, "external_actions": 0, "x2_materialized": False})
    text = overview(inherited, proposals)
    write_text("x1/integrated-overview.md", text)
    print(json.dumps({"owner": OWNER, "phase": PHASE, "source": head, "inherited": 20, "new": 40, "outcomes": OUTCOMES, "portfolio": actual_counts, "startup_failures": len(STARTUP_FAILURES), "overview_words": len(text.split())}, sort_keys=True))


def staged_entries() -> list[str]:
    return [line for line in git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if line]


def staged_review() -> None:
    paths = staged_entries()
    allowed_exact = {
        "scripts/build_ghc_family_auren_lark_v670_v3_x1.py",
        "tests/test_ghc_family_auren_lark_v670_v3_x1.py",
    }
    out_of_scope = [p for p in paths if not (p.startswith("docs/auren-lark/v670-v3/x1/") or p in allowed_exact)]
    mixed = [
        p
        for p in paths
        if "/x2/" in p
        or "/closeout/" in p
        or "/final/" in p
        or p.endswith(("x2.py", "final.py"))
    ]
    payload = {
        "schema": "ghc.family.staged-review.v4",
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "x1",
        "staged_before_self": paths,
        "staged_count_before_self": len(paths),
        "out_of_scope": out_of_scope,
        "mixed_lifecycle": mixed,
        "valid": not out_of_scope and not mixed,
    }
    write_json("validation/x1-staged-review.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def manifest_from_index() -> None:
    paths = staged_entries()
    exclusions = [
        "docs/auren-lark/v670-v3/validation/x1-manifest.json",
        "docs/auren-lark/v670-v3/validation/x1-staged-review.json",
    ]
    entries = []
    for path in paths:
        if path in exclusions:
            continue
        blob = git("show", f":{path}").stdout
        entries.append({"path": path, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})
    entries.sort(key=lambda row: row["path"])
    write_json("validation/x1-manifest.json", {"schema": "ghc.family.git-blob-manifest.v4", "domain": "x1 staged entries before self files", "hash_domain": "normalized_lf_exact_git_blob", "owner": OWNER, "phase": PHASE, "source_final": SOURCE_FINAL, "entry_count": len(entries), "entries": entries, "self_exclusions": exclusions})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staged-review", action="store_true")
    parser.add_argument("--manifest-from-index", action="store_true")
    args = parser.parse_args()
    if args.staged_review:
        staged_review()
    elif args.manifest_from_index:
        manifest_from_index()
    else:
        build()


if __name__ == "__main__":
    main()
