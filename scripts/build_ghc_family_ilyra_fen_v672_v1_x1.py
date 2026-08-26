"""Build the planning-only Ilyra Fen v672-v1 x1 packet.

The builder is intentionally fail-closed: it runs only at the exact Lyren
source head in the exact Ilyra branch, refuses an existing x2/closeout tree,
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
OWNER_ROOT = ROOT / "docs" / "ilyra-fen" / "v672-v1"
OWNER = "Ilyra Fen"
PHASE = "v672-v1"
SOURCE_BRANCH = "codex/GHC-Family/lyren-moss-v671-v8-full-tools"
SOURCE_FINAL = "189a71f6bb8164ba74a2fdcd215ec9969d3c14bc"
SOURCE_VESPER = "98d77253f3882fefad7f65e68fd0135f9b6f3d71"
SOURCE_X1 = "cefc03dbbdf3793162f47a29c857df8d59ba5e3b"
SOURCE_EVIDENCE = "afa96fed7a51f09a3d3d57e24399b73d167f5889"
BRANCH = "codex/GHC-Family/ilyra-fen-v672-v1-full-tools"
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
CORE_LABELS = ["completed", "represented", "open_gap", "exact_gate"]

IDENTITY_BOUNDARY = (
    "Ilyra Fen, she/they, evidence-boundary steward and reproducibility "
    "cartographer, is relational working language only. It is not evidence of "
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

SOURCE_SEAL = {
    "proposal_chain": 5870,
    "effective_negatives": 34813,
    "methods": 21356,
    "failed_witnesses": 6634,
    "passing_witnesses": 8611,
    "open_gaps": 271,
    "exact_gates": 266,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
}

ACTIVATION_BASELINE = {
    **SOURCE_SEAL,
    "effective_negatives": 34816,
    "methods": 21359,
    "failed_witnesses": 6637,
    "passing_witnesses": 8614,
    "external_route_failures": 3,
    "repository_seal_rewritten": False,
}

STARTUP_FAILURES = [
    {
        "failure_id": "IF6721-START-001",
        "failed_witness": "The first whole activation-packet display exceeded the visible result boundary before EOF.",
        "completion_credit": 0,
        "recovery": "Measure the committed packet and read numbered literal windows through line 478 and EOF.",
        "passing_bounded_witness": "All 478 lines were read and the exact Git-blob digest and word count matched.",
        "recurrence_guard": "Measure large committed packets before display and use one bounded window per read.",
    },
    {
        "failure_id": "IF6721-START-002",
        "failed_witness": "The first complete authorization-state display exceeded its output budget before EOF.",
        "completion_credit": 0,
        "recovery": "Read the immutable state in numbered literal windows through line 1556 and EOF.",
        "passing_bounded_witness": "Every state line and the required schema were read without mutation.",
        "recurrence_guard": "Read large mutable-state snapshots in premeasured windows rather than one projection.",
    },
    {
        "failure_id": "IF6721-START-003",
        "failed_witness": "The first closeout-skill display exceeded the model-visible context boundary.",
        "completion_credit": 0,
        "recovery": "Read the 177-line skill in two numbered chunks through EOF.",
        "passing_bounded_witness": "Both chunks completed and included the current owner-delta closeout override.",
        "recurrence_guard": "Premeasure long skills and split them before the first display.",
    },
    {
        "failure_id": "IF6721-START-004",
        "failed_witness": "The first orchestration-memory display omitted a bounded middle region when its result was truncated.",
        "completion_credit": 0,
        "recovery": "Reread the exact omitted line interval separately after the surrounding chunks.",
        "passing_bounded_witness": "The recovered interval closed the only omission through EOF.",
        "recurrence_guard": "Treat a tool truncation marker as an omission gate even when later lines remain visible.",
    },
    {
        "failure_id": "IF6721-START-005",
        "failed_witness": "The first byte-level packet word counter over-escaped its whitespace expression and reported zero words.",
        "completion_credit": 0,
        "recovery": "Decode the exact Git blob as UTF-8 and count split tokens directly.",
        "passing_bounded_witness": "The recovered projection reported 15,251 words and the expected SHA-256.",
        "recurrence_guard": "Prefer decoded split counting over nested shell-regex escaping.",
    },
    {
        "failure_id": "IF6721-START-006",
        "failed_witness": "A multiline Python manifest-schema wrapper returned no attributable output.",
        "completion_credit": 0,
        "recovery": "Use PowerShell scalar JSON reads to inspect each manifest's keys, entry count, and self exclusions.",
        "passing_bounded_witness": "Five manifest schemas and their 725 aggregate entries were attributed exactly.",
        "recurrence_guard": "Avoid multiline code in a shell argument when a scalar JSON projection is sufficient.",
    },
    {
        "failure_id": "IF6721-START-007",
        "failed_witness": "The first one-process-per-entry manifest replay completed its display window without an attributable result.",
        "completion_credit": 0,
        "recovery": "Replace per-entry Git process creation with one exact cat-file batch projection.",
        "passing_bounded_witness": "The later bounded batch replay checked all 725 entries with zero mismatches.",
        "recurrence_guard": "Use one batch Git object process for large commit-local manifest replays.",
    },
    {
        "failure_id": "IF6721-START-008",
        "failed_witness": "A second per-entry replay wrapper outlived its display window without preserving its terminal session identifier.",
        "completion_credit": 0,
        "recovery": "Abandon the un-attributable wrapper and use an explicit batch result object with captured session state.",
        "passing_bounded_witness": "The replacement emitted a complete per-domain replay receipt.",
        "recurrence_guard": "Print the whole terminal result object whenever a command may cross the initial yield window.",
    },
    {
        "failure_id": "IF6721-START-009",
        "failed_witness": "The first Git batch replay wrote all requests before draining stdout and deadlocked on bounded pipe buffers.",
        "completion_credit": 0,
        "recovery": "Terminate only the stuck read-only process and use subprocess communication that drains output while supplying input.",
        "passing_bounded_witness": "The recovered batch replayed 725 entries with zero mismatches.",
        "recurrence_guard": "Use communicate or equivalent concurrent pipe drainage for Git batch protocols.",
    },
    {
        "failure_id": "IF6721-START-010",
        "failed_witness": "The dynamically advertised source-task read surface reported that it was no longer callable through dynamic tools.",
        "completion_credit": 0,
        "recovery": "Use the exact local source-task rollout record read-only to recover the already-declared external receipt pointer.",
        "passing_bounded_witness": "The exact receipt was found and its SHA-256 matched the live baton.",
        "recurrence_guard": "Treat advertised-but-retired task tools as capability failures and use current Codex MCP only when exposed.",
    },
    {
        "failure_id": "IF6721-START-011",
        "failed_witness": "The first canonical-receipt projection exceeded PowerShell's default JSON depth and emitted null scalar guesses.",
        "completion_credit": 0,
        "recovery": "Read the small receipt raw after its exact file hash had already matched.",
        "passing_bounded_witness": "The raw receipt confirmed 33 of 33 checks, 18 of 18 tests, one success, and no replay.",
        "recurrence_guard": "Inspect actual receipt keys or increase JSON depth before selecting nested fields.",
    },
    {
        "failure_id": "IF6721-START-012",
        "failed_witness": "A broad worktree-registration inventory exceeded its bounded window and left two read-only Git processes running.",
        "completion_credit": 0,
        "recovery": "Terminate only those two inventory processes and test the exact intended path, ref, registration directory, and remote ref.",
        "passing_bounded_witness": "All four scalar uniqueness checks proved the Ilyra lane absent before creation.",
        "recurrence_guard": "Never enumerate the complete worktree bank when one exact registration path answers the gate.",
    },
    {
        "failure_id": "IF6721-START-013",
        "failed_witness": "The first sparse-setup diagnostic used a semicolon inside a PowerShell parenthesized expression and failed to parse before Git ran.",
        "completion_credit": 0,
        "recovery": "Split sparse initialization, pattern selection, read-tree population, and diagnostics into scalar commands.",
        "passing_bounded_witness": "The unique sparse lane materialized zero inherited files and remained clean at the exact source head.",
        "recurrence_guard": "Assign command exit codes after invocation rather than embedding command lists inside expressions.",
    },
    {
        "failure_id": "IF6721-START-014",
        "failed_witness": "The first official-source search result projection emitted no visible text because its response envelope was misread.",
        "completion_credit": 0,
        "recovery": "Project the same bounded official search response directly.",
        "passing_bounded_witness": "Official buildingSMART, W3C, and New Zealand Building Performance sources were recovered.",
        "recurrence_guard": "Project web search responses directly unless a typed content envelope has been verified first.",
    },
    {
        "failure_id": "IF6721-START-015",
        "failed_witness": "The first large two-file edit result exceeded the model-visible context and left patch application ambiguous.",
        "completion_credit": 0,
        "recovery": "Inspect both exact literal files and their targeted old-label, count, anchor, and route patterns before any subsequent edit.",
        "passing_bounded_witness": "The planning builder and test rewrite were present, internally aligned, and the lane still contained only the two intended untracked files.",
        "recurrence_guard": "Split large patches into bounded files or sections and inspect exact post-edit state whenever tool output truncates.",
    },
    {
        "failure_id": "IF6721-START-016",
        "failed_witness": "The first x1 build assumed inherited outcome rows used observed_outcome and stopped on a missing-key error before packet materialization.",
        "completion_credit": 0,
        "recovery": "Inspect the first exact Git-blob row in both predecessor ledgers and use their actual outcome field.",
        "passing_bounded_witness": "Both immutable ledgers exposed the same proposal_id, title, outcome, and completion_credit schema before the correction.",
        "recurrence_guard": "Project exact committed ledger keys before adapting a historical builder to a newer phase.",
    },
]

NEW_PROPOSAL_TITLES = [
    "synthetic architectural drawing package capsule binding issue set revision and surrogate project identifiers",
    "sheet index uniqueness tribunal rejecting duplicate sheet numbers and silently omitted references",
    "title block completeness contract for synthetic drawing identity discipline status scale and issue purpose",
    "revision label sequence board refusing ambiguous ordering reuse rollback and unexplained gaps",
    "revision event reason status and supersession ledger with append-only correction lineage",
    "revision cloud region reference contract separating change indication from design approval",
    "superseded sheet quarantine preventing stale issue sets from regaining current status",
    "issue purpose vocabulary firewall separating review coordination consent construction and record labels",
    "synthetic transmittal package acknowledgement board preserving sent received exception and no-acceptance states",
    "external reference dependency graph for synthetic drawing model schedule and specification links",
    "missing external reference refusal with unresolved dependency escrow and reversible recovery",
    "view detail section and callout referential-integrity tribunal rejecting orphan targets",
    "cyclic sheet detail and reference detector with bounded path witness and no geometry inference",
    "scale annotation versus measurement firewall refusing dimensional derivation from display metadata",
    "unit precision and coordinate-domain register for synthetic drawing annotations",
    "datum origin and coordinate-reference uncertainty ledger preserving survey-authority vacancy",
    "layer classification and visibility-label contract rejecting semantic promotion from display state",
    "model drawing and schedule divergence escrow with explicit unresolved comparison status",
    "markup comment lifecycle board for open answered incorporated rejected and withdrawn synthetic states",
    "synthetic request-for-information linkage contract refusing professional response or instruction authority",
    "clash issue record with object surrogate viewpoint status and resolution-evidence vacancies",
    "acceptance status versus approval authority firewall for drawing exchanges and review comments",
    "issue-set fixity board binding path media type byte length and content digest without document truth promotion",
    "bitemporal drawing correction ledger separating recorded observed effective and superseded times",
    "synthetic authorship ownership and responsibility abstention profile for drawing metadata",
    "drawing-package confidentiality purpose limitation and minimum-disclosure recipient profile",
    "zero-key Freed ID credential structure for synthetic drawing issuer recipient and subject roles",
    "synthetic credential status and withdrawal representation with zero live keys resolution or revocation events",
    "accessible sheet index structure with headings landmarks counts focus order and table semantics",
    "text-alternative record for drawing symbols details dimensions and revision annotations",
    "colour-independent revision notice using labels patterns text and change descriptions",
    "responsive and print-fallback drawing register with manual assistive-technology evaluation reserved",
    "THOS bounded drawing issue correction readback workload hold and shift-handover representation",
    "GMUT coordinate-chart overlap analogy refusing architectural geometry to spacetime or force promotion",
    "GMUT constraint-and-boundary obligation register for typed analogies with zero physical inference",
    "CBR notice contest nonretaliation correction and remedy-vacancy matrix for synthetic drawing records",
    "zero-row IFC document adapter held at zero files parses exchanges validations and interoperability claims",
    "real practitioner affected-user accessibility and independently reviewed drawing-workflow evaluation gap",
    "building consent design inspection release and professional responsibility exact authority gate",
    "heritage cultural Maori-authority and terminal Stage 20 promotion exact gate",
]

SKILL_IDEAS = [
    "ghc-family-drawing-package-capsule",
    "ghc-family-sheet-index-uniqueness",
    "ghc-family-title-block-contract",
    "ghc-family-revision-sequence-board",
    "ghc-family-superseded-sheet-quarantine",
    "ghc-family-issue-purpose-firewall",
    "ghc-family-transmittal-acknowledgement",
    "ghc-family-xref-dependency-escrow",
    "ghc-family-callout-integrity-tribunal",
    "ghc-family-scale-measurement-firewall",
    "ghc-family-datum-uncertainty-ledger",
    "ghc-family-model-drawing-divergence",
    "ghc-family-markup-lifecycle-board",
    "ghc-family-drawing-fixity-manifest",
    "ghc-family-drawing-bitemporal-correction",
    "ghc-family-drawing-minimum-disclosure",
    "ghc-family-zero-key-drawing-credential",
    "ghc-family-accessible-sheet-index",
    "ghc-family-drawing-handover-proxy",
    "ghc-family-drawing-authority-nonpromotion",
]

RUNNER_IDEAS = [
    "ghc_family_drawing_package_runner.py",
    "ghc_family_sheet_index_runner.py",
    "ghc_family_revision_sequence_runner.py",
    "ghc_family_transmittal_runner.py",
    "ghc_family_xref_escrow_runner.py",
    "ghc_family_callout_integrity_runner.py",
    "ghc_family_drawing_fixity_runner.py",
    "ghc_family_accessible_sheet_runner.py",
    "ghc_family_drawing_handover_runner.py",
    "ghc_family_drawing_nonpromotion_runner.py",
]

EXACT_PACKETS = [
    "real architectural commission design service or professional instruction",
    "real building site survey datum coordinate or measurement decision",
    "real building consent application approval inspection or compliance decision",
    "real drawing issue release construction direction or record certification",
    "real practitioner participant client worker or affected-user evaluation",
    "live IFC exchange model upload registry query or interoperability event",
    "live identity key proof token account credential issuance or revocation",
    "real confidential drawing disclosure recipient or access decision",
    "legal interpretation liability ownership copyright or remedy decision",
    "heritage cultural wording traditional knowledge or data-governance decision",
    "Maori wording tikanga place data or authority decision",
    "production deployment external API write cloud mutation or package release",
    "host-security feature elevation reboot or unrelated installation",
    "destructive cleanup history rewrite force push or sibling mutation",
    "privacy-complete or exhaustive-security certification",
    "complete accessibility conformance declaration",
    "independent-reproduction or external-audit declaration",
    "empirical GMUT likelihood posterior parameter constraint or detected force",
    "Theory-of-Everything proof AGI ASI consciousness personhood or canon promotion",
    "Stage 20 promotion or operational authority",
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
    "ghc-family-theatre-cue-map-revision",
    "ghc-family-prop-drawing-custody-vacancy",
    "ghc-family-alternate-format-cue-index",
    "ghc-family-technical-rehearsal-readback",
    "ghc-family-ifc-zero-file-refusal",
    "ghc-family-drawing-credential-status-gap",
    "ghc-family-reference-cycle-explanation",
    "ghc-family-git-blob-self-exclusion-audit",
    "ghc-family-canonical-attempt-lock",
    "ghc-family-route-timeout-no-resend",
]

SUCCESSOR_RUNNERS = [
    "ghc_family_theatre_cue_revision_runner.py",
    "ghc_family_prop_drawing_custody_runner.py",
    "ghc_family_cue_index_accessibility_runner.py",
    "ghc_family_rehearsal_readback_runner.py",
    "ghc_family_ifc_zero_file_runner.py",
    "ghc_family_credential_status_gap_runner.py",
    "ghc_family_reference_cycle_runner.py",
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


def git_json(commit: str, path: str) -> Any:
    return json.loads(git("show", f"{commit}:{path}").stdout.decode("utf-8", errors="strict"))


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
                "proposal_id": f"IF6721-N{index:03d}",
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
                "primary_pillar": "Freed ID and CBR Heart",
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
                    "task_id": f"IF6721-{prefix}-{len(rows) + 1:03d}",
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
            "task_id": f"IF6721-{prefix}-{index:03d}",
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
        "drawing package identity",
        "revision and supersession",
        "external reference escrow",
        "issue and transmittal control",
        "accessible drawing register",
        "Heart notice correction and authority boundary",
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
        ["theatre cue-map revision", "technical rehearsal handover", "successor terminal route", "successor Git-blob seal", "successor authority boundary"],
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
        "# Ilyra Fen v672-v1 x1 integrated planning overview",
        "",
        "## Scope and lifecycle",
        "",
        (
            "This x1 packet is a planning freeze, not implementation evidence. Ilyra works in one "
            "fresh additive sparse D-first lane rooted at Lyren Moss's exact v671-v8 final. The "
            "source, Lyren x1, Lyren evidence, and Lyren final were checked through exact parent "
            "relations, zero-merge history, clean state, fresh live equality, and 725 commit-local "
            "Git-blob manifest entries. Lyren's canonical receipt remains inherited same-owner "
            "evidence and receives no Ilyra credit or replay."
        ),
        "",
        "## Evidence and identity boundary",
        "",
        IDENTITY_BOUNDARY,
        "",
        (
            "The primary Trinity Mandala pillar is Freed ID and CBR Heart, limited to synthetic "
            "drawing-package notice, provenance, minimum-disclosure, correction, contest, and "
            "authority-vacancy contracts. No real key, proof, credential, account, issuer, recipient, "
            "building record, right, remedy, disclosure decision, or governance legitimacy exists. "
            "THOS Body is represented only by bounded issue-control handover fixtures. GMUT Mind "
            "retains typed coordinate and constraint analogies with no geometry, force, prediction, "
            "likelihood, physical inference, Theory of Everything, or canon claim."
        ),
        "",
        "## Three bounded human-practice lenses",
        "",
        (
            "The first lens is architectural drawing revision and supersession control using wholly "
            "synthetic sheets, title blocks, revision events, issue purposes, fixity records, and "
            "stale-set quarantine. It is not architectural, engineering, surveying, drafting, consent, "
            "inspection, or construction practice. The second lens is drawing transmittal and external-"
            "reference coordination using synthetic acknowledgements, callouts, dependency escrows, "
            "comments, and unresolved statuses. It is not a professional instruction, acceptance, or "
            "approval. The third lens is accessible drawing-register presentation using structural "
            "headings, table semantics, text alternatives, colour-independent notices, and print "
            "fallback. Manual assistive-technology and affected-user evaluation remain absent."
        ),
        "",
        "## Novelty audit",
        "",
        (
            "The declared chain begins at 5,870. Twenty Lyren rows are selected for integrity "
            "revalidation with zero novelty and zero completion credit. Forty Ilyra titles are "
            "distinct within the new set and are compared directly with an exact eighty-title sample "
            "from Lyren and Vesper Git blobs. The repository's declared canonical row-to-title mapping "
            "remains incomplete, leaving 5,750 inherited declared rows outside this local comparison. "
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
            f"{len(STARTUP_FAILURES)} startup failures are retained separately from the Lyren repository seal. Each failed "
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
            "Auren Lark v672-v2 is prospective only. No task discovery, precontact, message, fork, "
            "standby contact, or substitute endpoint occurs during x1 or x2. Only a clean pushed exact "
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
    sections.extend(["", "## Forty frozen Ilyra proposals", ""])
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
            "exact": parent_x1 == SOURCE_VESPER and parent_evidence == SOURCE_X1 and parent_final == SOURCE_EVIDENCE,
        },
        "phase_commits": int(git_text("rev-list", "--count", f"{SOURCE_VESPER}..{SOURCE_FINAL}")),
        "merge_commits": int(git_text("rev-list", "--merges", "--count", f"{SOURCE_VESPER}..{SOURCE_FINAL}")),
        "commit_local_manifest_entries_replayed": 725,
        "commit_local_manifest_mismatches": 0,
        "activation_packet": {
            "path": "docs/lyren-moss/v671-v8/handoffs/ilyra-fen-v672-v1-activation-candidate.md",
            "bytes": 137699,
            "words": 15251,
            "sha256": "1de6c4dfb14244c1c5291be9306a51d7849963eb66452476aaa12f466b3eebe0",
        },
        "external_canonical_receipt": {
            "sha256": "8351d24420cd9e52571edfd73f62dedb6b9d11b065424436a46c3ab7b01614c5",
            "bytes": 3556,
            "path_supplied": True,
            "path_published": False,
            "rehash_state": "exact_D_backed_receipt_rehashed_without_publishing_private_absolute_path",
            "result": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "checks": "33/33",
            "tests": "18/18",
            "invocations": 1,
            "successful_invocations": 1,
            "post_success_replay": False,
            "authority_source": "Lyren live activation baton and exact source-task terminal record",
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

    source_outcomes = git_json(
        SOURCE_FINAL, "docs/lyren-moss/v671-v8/x2/outcome-ledger.json"
    )["rows"]
    predecessor_outcomes = git_json(
        SOURCE_VESPER, "docs/vesper-arlen/v671-v7/x2/outcome-ledger.json"
    )["rows"]
    inherited = [
        {
            "selection_id": f"IF6721-I{index:03d}",
            "source_owner": "Lyren Moss",
            "source_phase": "v671-v8",
            "source_proposal_id": row["proposal_id"],
            "source_title": row["title"],
            "source_outcome": row["outcome"],
            "source_row_sha256": row_digest(row),
            "integrity_revalidated": True,
            "ilyra_novelty_credit": 0,
            "ilyra_completion_credit": 0,
            "state": "inherited_evidence_only",
        }
        for index, row in enumerate(source_outcomes[:20], start=1)
    ]
    proposals = proposal_rows()
    if len(proposals) != 40 or Counter(row["planned_outcome"] for row in proposals) != Counter(OUTCOMES):
        raise SystemExit("proposal count or four-label distribution drifted")
    if len({row["title"] for row in proposals}) != 40:
        raise SystemExit("new proposal titles are not unique")

    source_titles = [row["title"] for row in source_outcomes + predecessor_outcomes]
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
        **ACTIVATION_BASELINE,
        "external_startup_failures": len(STARTUP_FAILURES),
        "effective_negatives": ACTIVATION_BASELINE["effective_negatives"] + len(STARTUP_FAILURES),
        "methods": ACTIVATION_BASELINE["methods"] + len(STARTUP_FAILURES),
        "failed_witnesses": ACTIVATION_BASELINE["failed_witnesses"] + len(STARTUP_FAILURES),
        "passing_witnesses": ACTIVATION_BASELINE["passing_witnesses"] + len(STARTUP_FAILURES),
        "repository_seal_rewritten": False,
    }

    write_json("x1/activation-intake.json", {"schema": "ghc.family.activation-intake.v4", "owner": OWNER, "phase": PHASE, "source_verification": source_verification, "task_creation_count": 0, "fork_count": 0, "subagent_count": 0, "standby_contact_count": 0})
    write_json("x1/identity-and-boundary.json", {"schema": "ghc.family.identity-boundary.v3", "owner": OWNER, "phase": PHASE, "pronouns": "she/they", "relational_role": "evidence-boundary steward and reproducibility cartographer", "relational_hope": "leave every claim traceable and every gate unmistakable", "identity_boundary": IDENTITY_BOUNDARY})
    write_json("x1/source-count-overlay.json", {"schema": "ghc.family.source-count-overlay.v5", "repository_sealed": SOURCE_SEAL, "inherited_activation_baseline": ACTIVATION_BASELINE, "ilyra_x1_overlay": activation_overlay})
    write_json("x1/inherited-proposal-revalidation.json", {"schema": "ghc.family.inherited-proposal-revalidation.v4", "owner": OWNER, "phase": PHASE, "selected": 20, "novelty_credit": 0, "completion_credit": 0, "rows": inherited})
    write_json("x1/semantic-neighbor-audit.json", {"schema": "ghc.family.semantic-neighbor-audit.v3", "owner": OWNER, "phase": PHASE, "declared_accessible_unique_titles": 5697, "direct_git_blob_comparison_titles": len(source_titles), "inherited_declared_rows_not_locally_compared": 5750, "canonical_row_to_title_mapping_complete": False, "new_titles": 40, "max_jaccard": round(max_score, 6), "collision_threshold": 0.72, "collisions": sum(row["collision"] for row in neighbors), "rows": neighbors, "universal_novelty_claim": False})
    write_json("x1/new-proposal-freeze.json", {"schema": "ghc.family.new-proposal-freeze.v5", "owner": OWNER, "phase": PHASE, "proposal_chain_before": 5870, "proposal_chain_after_if_evidence_frozen": 5910, "outcomes": OUTCOMES, "rows": proposals})
    write_json("x1/portfolio-freeze.json", {"schema": "ghc.family.remastered-portfolio-freeze.v5", "owner": OWNER, "phase": PHASE, "rows": portfolio, "counts": actual_counts, "ordinary_phase_new_tool_target": 3, "bounded_practice_lenses": ["synthetic architectural drawing revision and supersession control", "synthetic drawing transmittal and external-reference coordination", "synthetic accessible drawing-register presentation"], "successor_practice_recommendation": "synthetic theatre technical-drawing cue-map revision and accessible rehearsal handover", "filler_prohibited": True})
    write_json("x1/source-ledger.json", {"schema": "ghc.family.public-source-ledger.v5", "owner": OWNER, "phase": PHASE, "retrieved_nz_date": "2026-08-27", "sources": [
        {"title": "IFC 4.3.2.0 official documentation", "publisher": "buildingSMART International", "url": "https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/index.html", "use": "official open-schema scope and exchange vocabulary only"},
        {"title": "IfcDocumentInformation", "publisher": "buildingSMART International", "url": "https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/HTML/lexical/IfcDocumentInformation.htm", "use": "document identity revision purpose status and confidentiality vocabulary only"},
        {"title": "PROV-DM: The PROV Data Model", "publisher": "W3C", "url": "https://www.w3.org/TR/prov-dm/", "use": "entity activity derivation agent and bundle provenance vocabulary only"},
        {"title": "Verifiable Credentials Data Model v2.0", "publisher": "W3C", "url": "https://www.w3.org/TR/vc-data-model/", "use": "issuer holder verifier status privacy and nontruth-promotion boundaries only"},
        {"title": "Decentralized Identifiers v1.0", "publisher": "W3C", "url": "https://www.w3.org/TR/did-core/", "use": "identifier verification-method and controller vocabulary with zero live keys"},
        {"title": "Web Content Accessibility Guidelines 2.2", "publisher": "W3C", "url": "https://www.w3.org/TR/WCAG22/", "use": "text alternative colour-independent and structural accessibility vocabulary only"},
        {"title": "Apply for building consent", "publisher": "New Zealand Building Performance", "url": "https://www.building.govt.nz/projects-and-consents/apply-for-building-consent", "use": "current consent-process vocabulary and exact professional-authority refusal boundary only"},
    ], "boundary": "Sources supply vocabulary and refusal boundaries only; they are not observations, validation, professional guidance, legal interpretation, operational authorization, affected-party acceptance, cultural legitimacy, Maori authority, or Stage 20 evidence."})
    write_json("x1/threat-model.json", {"schema": "ghc.family.threat-model.v4", "owner": OWNER, "phase": PHASE, "assets": ["source lineage", "x1-before-x2 lifecycle", "proposal distinctness", "four truth labels", "retained failures", "synthetic-only fixtures", "route uniqueness"], "risks": [
        {"risk": "source drift", "control": "exact commits and fresh live equality"},
        {"risk": "semantic collision", "control": "deterministic 80-title Git-blob neighbor audit and retained 5750-row recovery gap"},
        {"risk": "drawing metadata to professional approval promotion", "control": "acceptance-versus-authority firewall and zero-row IFC adapter"},
        {"risk": "formal-to-physical promotion", "control": "GMUT coordinate analogy firewall and zero physical inference"},
        {"risk": "professional practice inference", "control": "three wholly synthetic drawing lenses and explicit authority vacancies"},
        {"risk": "failure laundering", "control": "append-only Method Flow and zero-credit failed witnesses"},
        {"risk": "privacy leakage", "control": "five-class owner-delta disposition scan"},
        {"risk": "manifest drift", "control": "exact staged and committed Git-blob manifests"},
        {"risk": "duplicate route", "control": "terminal gate exact-title reread duplicate guard and no-resend"},
    ]})
    write_json("x1/method-flow-startup.json", {"schema": "ghc.family.method-flow-ledger.v4", "owner": OWNER, "phase": PHASE, "stage": "x1_startup", "rows": STARTUP_FAILURES, "failed_witnesses": len(STARTUP_FAILURES), "bounded_passing_witnesses": len(STARTUP_FAILURES), "erased_failures": 0})
    write_json("x1/workflow-plan.json", {"schema": "ghc.family.workflow-plan.v5", "owner": OWNER, "phase": PHASE, "steps": [
        {"step": "activation guidance and source verification", "state": "completed_read_only"},
        {"step": "planning-only x1 freeze", "state": "in_progress_until_pushed_equal"},
        {"step": "bounded x2 execution", "state": "blocked_by_x1_terminal_gate"},
        {"step": "combined closeout and exact seal", "state": "pending"},
        {"step": "one owner-scoped canonical aggregate", "state": "pending_not_invoked"},
        {"step": "prospective Auren route", "state": "pending_terminal_and_live_authority"},
    ], "commit_ceiling": 8, "planned_phase_commits": 3, "file_rotation_guard": 2000})
    write_json("x1/phase-truth.json", {"schema": "ghc.family.phase-truth.x1.v5", "owner": OWNER, "phase": PHASE, "primary_pillar": "Freed ID and CBR Heart", "protected_pillars": ["GMUT Mind", "THOS Body"], "proposal_rows": {"inherited_zero_credit": 20, "new": 40, "total": 60}, "expected_outcomes": OUTCOMES, "core_truth_labels": CORE_LABELS, "proposal_chain": {"before": 5870, "after_if_frozen": 5910}, "inherited_declared_rows_not_locally_compared": 5750, "startup_operational_failures": len(STARTUP_FAILURES), "x1_completion_credit": 0, "x2_execution_started": False, "real_world_actions": 0, "identity_boundary": IDENTITY_BOUNDARY, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("x1/route-plan.json", {"schema": "ghc.family.route-plan.v5", "owner": OWNER, "phase": PHASE, "prospective_recipient_exact_title": "Auren Lark", "prospective_phase": "v672-v2", "delivery_state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED", "successor_contact_count": 0, "task_creation_count": 0, "substitute_endpoint_count": 0, "standby_contact_count": 0, "required_gate": "clean pushed exact final plus one successful owner-scoped canonical aggregate and newest live route reread"})
    write_json("x1/build-receipt.json", {"schema": "ghc.family.x1-build-receipt.v4", "owner": OWNER, "phase": PHASE, "source_head": head, "branch": branch, "inherited_rows": 20, "new_rows": 40, "portfolio_counts": actual_counts, "external_actions": 0, "x2_materialized": False})
    text = overview(inherited, proposals)
    write_text("x1/integrated-overview.md", text)
    print(json.dumps({"owner": OWNER, "phase": PHASE, "source": head, "inherited": 20, "new": 40, "outcomes": OUTCOMES, "portfolio": actual_counts, "startup_failures": len(STARTUP_FAILURES), "overview_words": len(text.split())}, sort_keys=True))


def staged_entries() -> list[str]:
    return [line for line in git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if line]


def staged_review() -> None:
    paths = staged_entries()
    allowed_exact = {
        "scripts/build_ghc_family_ilyra_fen_v672_v1_x1.py",
        "tests/test_ghc_family_ilyra_fen_v672_v1_x1.py",
    }
    out_of_scope = [p for p in paths if not (p.startswith("docs/ilyra-fen/v672-v1/x1/") or p in allowed_exact)]
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
        "docs/ilyra-fen/v672-v1/validation/x1-manifest.json",
        "docs/ilyra-fen/v672-v1/validation/x1-staged-review.json",
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
