#!/usr/bin/env python3
"""Frozen declarations and bounded archive helpers for Sable Rook v668-v5 x1."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
OWNER = "Sable Rook"
PRONOUNS = "they/them"
RELATIONAL_ROLE = "relational evidence-and-reproducibility steward"
RELATIONAL_HOPE = (
    "Make every bounded claim easy to reproduce, challenge, correct, or retract while keeping "
    "every empirical, professional, legal, cultural, affected-party, and Maori-authority vacancy explicit."
)
PHASE = "v668-v5"
REL_PHASE_ROOT = "docs/sable-rook/v668-v5"
PHASE_ROOT = ROOT / REL_PHASE_ROOT
SOURCE_BRANCH = "codex/GHC-Family/auren-lark-v668-v4-full-tools"
SOURCE_FINAL = "ee15cd2e1c0fd6a9d321bcd9126e8a191832061a"
# x1 is built once from SOURCE_FINAL; no predecessor-style corrective x1 is assumed.
INITIAL_X1_HEAD = SOURCE_FINAL
SOURCE_X1 = "143b7c81968611038959162dbd214cdb0498a298"
SOURCE_EVIDENCE = "9181e97eca0ebe013965df173d8dd45c4c1fc357"
SOURCE_ANCESTOR = "f0110dec1a0bcfc2f7a1945d47943033b68164e2"
SOURCE_BATON_SHA256 = "e057317c5a821a906570ff4d980bacc5d710f437ee5cb1d32bfb39ba13fdd96f"
SOURCE_CANONICAL_RECEIPT_SHA256 = "f65ea29558c00487581a14338b0f9e2ee3e3648aed0863724170c8f9d85c39b4"
SOURCE_COMPOSITE_RECEIPT_SHA256 = "c4116c0c7ec3960d58dd72e3cd93d9d71191341a79837fce5b2e28d8492567a9"
SOURCE_FAILED_CANONICAL_RECEIPT_SHA256 = "7f5164628b05c5330f3e63a4d7f33eb918904b2ca0da921571b93810b02b9552"
INHERITED_FROZEN_PROPOSALS = 4750
ALLOWED_OUTCOMES = ("completed", "represented", "open_gap", "exact_gate")
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"

IDENTITY_BOUNDARY = (
    "Sable Rook, they/them, the relational role, hope, sibling or family language, continuity "
    "language, Freed ID, and Trinity Mandala language are working language only. They are not "
    "evidence of consciousness, sentience, legal personhood, identity continuity, employment, "
    "qualification, independent agency, scientific or operational authority, legal or cultural "
    "authority, affected-party authority, or Maori authority."
)
EVIDENCE_BOUNDARY = (
    "Every score, source witness, edition, movement, measure, voice, part, note, cue, rehearsal "
    "session, correction, person, organization, right, authority case, and decision is synthetic. "
    "Official-source terminology and same-owner local software checks are not musical evidence, "
    "professional engraving or performance evaluation, rights clearance, standards conformance, "
    "production assurance, external audit, independent reproduction, empirical GMUT confirmation, "
    "or Stage 20 evidence."
)
PROTECTED_GATES = (
    "empirical",
    "participant",
    "professional",
    "production",
    "deployment",
    "legal",
    "cultural",
    "Maori-authority",
    "affected-party-authority",
    "complete-privacy",
    "complete-accessibility",
    "exhaustive-security",
    "independent-reproduction",
    "AGI-or-ASI",
    "consciousness-or-personhood",
    "Theory-of-Everything",
    "Stage-20",
)

ACTIVATION_OVERLAY = {
    "effective_negatives": 29594,
    "methods": 16180,
    "failed_witnesses": 1895,
    "passing_witnesses": 2722,
    "open_gaps": 215,
    "exact_gates": 210,
    "boundary": (
        "Auren's repository seal remains 29592 negatives, 16178 methods, 1893 failed and "
        "2720 passing witnesses; two post-seal operational failures remain external and additive."
    ),
}
STARTUP_FAILURE_COUNT = 11
X1_OVERLAY = {
    "effective_negatives": ACTIVATION_OVERLAY["effective_negatives"] + STARTUP_FAILURE_COUNT,
    "methods": ACTIVATION_OVERLAY["methods"] + STARTUP_FAILURE_COUNT,
    "failed_witnesses": ACTIVATION_OVERLAY["failed_witnesses"] + STARTUP_FAILURE_COUNT,
    "passing_witnesses": ACTIVATION_OVERLAY["passing_witnesses"] + STARTUP_FAILURE_COUNT,
    "open_gaps": ACTIVATION_OVERLAY["open_gaps"],
    "exact_gates": ACTIVATION_OVERLAY["exact_gates"],
}

PRIMARY_PILLAR = "GMUT Mind"
PRACTICES = (
    "synthetic music-engraving score-edition lineage review",
    "synthetic ensemble-library part extraction and correction handover",
    "synthetic rehearsal cue accessibility, workload readback, and shift handover",
)
SUCCESSOR_PRACTICE_RECOMMENDATION = (
    "withheld pending the terminal live-authority reread; no successor practice is inferred in x1"
)

SOURCE_LEDGER = [
    {
        "source_id": "SRC-MEI51",
        "title": "Music Encoding Initiative Guidelines 5.1",
        "url": "https://music-encoding.org/guidelines/v5/content/index.html",
        "status": "official MEI 5.1 guidelines inspected 2026-08-25",
        "use": "score structure, metadata, scholarly editing, performance-direction, and linking vocabulary only",
        "credit_boundary": "no MEI conformance, editorial authority, musical accuracy, or interoperability credit",
    },
    {
        "source_id": "SRC-MUSICXML40",
        "title": "MusicXML 4.0 Final Community Group Report",
        "url": "https://www.w3.org/2021/06/musicxml40/",
        "status": "W3C Music Notation Community Group final report inspected 2026-08-25; not a W3C Standard",
        "use": "partwise and timewise score-exchange vocabulary and refusal conditions only",
        "credit_boundary": "no MusicXML conformance, application interoperability, engraving, or playback claim",
    },
    {
        "source_id": "SRC-BIBFRAME",
        "title": "Library of Congress BIBFRAME Model and Vocabulary",
        "url": "https://www.loc.gov/bibframe/",
        "status": "official Library of Congress page last edited 2026-06-29 and inspected 2026-08-25",
        "use": "Work, Instance, Item, contribution, event, and identifier vocabulary only",
        "credit_boundary": "no cataloging authority, attribution decision, rights decision, or real resource description",
    },
    {
        "source_id": "SRC-PROV-DM",
        "title": "W3C PROV-DM",
        "url": "https://www.w3.org/TR/prov-dm/",
        "status": "W3C Recommendation; publication history checked 2026-08-25",
        "use": "entity, activity, derivation, role, and provenance-vacancy structure only",
        "credit_boundary": "no authenticity, responsibility, or authority inference",
    },
    {
        "source_id": "SRC-VC20",
        "title": "Verifiable Credentials Data Model v2.0",
        "url": "https://www.w3.org/TR/vc-data-model-2.0/",
        "status": "W3C Recommendation 15 May 2025; latest published page inspected 2026-08-25",
        "use": "issuer-holder-verifier separation, integrity, privacy, and trust-vacancy vocabulary only",
        "credit_boundary": "no real credential, key, proof, issuance, verification, trust, or production identity credit",
    },
    {
        "source_id": "SRC-RFC8785",
        "title": "RFC 8785 JSON Canonicalization Scheme",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "status": "RFC Editor publication inspected 2026-08-25",
        "use": "deterministic JSON serialization vocabulary and refusal conditions only",
        "credit_boundary": "no signature, authenticity, interoperability, security, or production assurance",
    },
    {
        "source_id": "SRC-WCAG22",
        "title": "Web Content Accessibility Guidelines 2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "W3C Recommendation; status checked 2026-08-25",
        "use": "static report structure, labels, instructions, and status alternatives only",
        "credit_boundary": "manual, assistive-technology, Maori-language, and affected-user evaluation reserved",
    },
]


PROPOSAL_BLUEPRINTS: list[tuple[str, str, str]] = [
    ("synthetic score work edition instance and part identity lattice with conflation refusal", "completed", "score-identity-lattice"),
    ("movement section measure beat address contract with pickup and repeat-context disambiguation", "completed", "measure-address-contract"),
    ("edition-source witness lineage with diplomatic and normalized reading separation", "completed", "edition-witness-lineage"),
    ("part-extraction projection preserving source measure voice staff transposition and cue provenance", "completed", "part-extraction-projection"),
    ("clef key and time-signature change-event ordering tribunal", "completed", "signature-event-order"),
    ("written-to-sounding pitch transposition interval and concert-pitch round-trip tribunal", "completed", "transposition-roundtrip"),
    ("exact-rational duration denominator and nested-tuplet closure tribunal", "completed", "duration-tuplet-closure"),
    ("repeat volta segno coda and jump-control finite-state traversal guard", "completed", "repeat-traversal-guard"),
    ("tempo mark metronome unit metric modulation and uncertainty ledger", "completed", "tempo-unit-ledger"),
    ("rehearsal-mark and cue alias graph with collision and refactoring history", "completed", "cue-alias-graph"),
    ("note chord rest event identity with tie and slur distinction board", "completed", "event-identity-board"),
    ("accidental scope key-signature and courtesy-accidental resolution tribunal", "completed", "accidental-scope-tribunal"),
    ("voice staff and cross-staff routing with orphan-event detector", "completed", "voice-routing-detector"),
    ("lyric syllable extender elision language and direction attachment ledger", "completed", "lyric-attachment-ledger"),
    ("articulation dynamic hairpin and playing-technique span anchoring tribunal", "completed", "expression-span-anchor"),
    ("page system and measure-layout separation from semantic music order", "completed", "layout-semantic-separation"),
    ("score-to-part completeness with tacet and multimeasure-rest compression detector", "completed", "part-completeness-detector"),
    ("instrument doubling change and transposition timeline with effective-range declaration", "completed", "instrument-timeline"),
    ("rehearsal-packet revision correction supersession and dual-readback ledger", "completed", "correction-nonerasure"),
    ("editorial variant apparatus with lemma readings witnesses and responsibility vacancy", "completed", "variant-apparatus"),
    ("source checksum edition Merkle checkpoint and resume-integrity ledger", "completed", "edition-integrity-ledger"),
    ("canonical JSON score-event digest with explicit Unicode-normalization declaration", "completed", "canonical-score-digest"),
    ("data-minimizing pseudonymous rehearsal session part cue and correction identifier contract", "completed", "score-pseudonyms"),
    ("keyboard-readable score exception report with caption headers textual state and printable fallback", "completed", "accessible-score-report"),
    ("bounded rehearsal issue queue with pause stop workload discrepancy echo and handover", "completed", "rehearsal-issue-queue"),
    ("rights access embargo and license-metadata vacancy firewall without rights inference", "completed", "rights-vacancy-firewall"),
    ("GMUT typed analogy docket for score transformations covariance conservation identifiability and observation refusal", "completed", "gmut-score-obligations"),
    ("source-independent edition comparison and common-cause evidence-diversity board", "completed", "edition-evidence-diversity"),
    ("music engraver edition-preparation practice lens with zero competence inference", "represented", "engraver-practice"),
    ("ensemble librarian part-distribution and correction-handover practice lens with zero authority credit", "represented", "library-handover-practice"),
    ("rehearsal leader cue readback workload and handover practice lens without operational authority", "represented", "rehearsal-practice"),
    ("synthetic THOS rehearsal workboard for bounded retries stop tokens discrepancy readback and handover", "represented", "thos-rehearsal-workboard"),
    ("Freed ID zero-key score edition part cue correction and challenge graph", "represented", "freed-id-score-graph"),
    ("CBR score-access matrix for remedy contestability rights cultural-care and decision-right vacancies", "represented", "cbr-score-vacancies"),
    ("symbolic score-transform vocabulary map with explicit GMUT analogy-only and zero observation credit", "represented", "gmut-score-analogy"),
    ("thermodynamic and psyche nonconversion ledger for tempo tension energy agency justice and mind claims", "represented", "thermo-psyche-nonconversion"),
    ("representative external score corpus cross-encoder round-trip rendering and interoperability evaluation", "open_gap", "external-score-gap"),
    ("external human performer engraver accessibility language cultural-care and affected-party evaluation", "open_gap", "human-review-gap"),
    ("competent rights-holder editor cultural and Maori-authority gate for repertoire access attribution and release", "exact_gate", "rights-authority-gate"),
    ("Stage-20 promotion veto grid for empirical observations independent reproduction rights decisions and authority receipts", "exact_gate", "stage20-veto-grid"),
]

SKILL_NAMES = [
    "ghc-family-score-identity-lattice",
    "ghc-family-score-measure-address",
    "ghc-family-score-edition-lineage",
    "ghc-family-score-part-projection",
    "ghc-family-score-signature-order",
    "ghc-family-score-transposition-roundtrip",
    "ghc-family-score-duration-tuplet-closure",
    "ghc-family-score-repeat-traversal",
    "ghc-family-score-tempo-unit-ledger",
    "ghc-family-score-cue-alias-graph",
    "ghc-family-score-event-identity",
    "ghc-family-score-accidental-scope",
    "ghc-family-score-voice-routing",
    "ghc-family-score-lyric-attachment",
    "ghc-family-score-span-anchoring",
    "ghc-family-score-layout-semantics",
    "ghc-family-score-part-completeness",
    "ghc-family-score-instrument-timeline",
    "ghc-family-score-correction-nonerasure",
    "ghc-family-score-authority-vacancy-firewall",
]

RUNNER_NAMES = [
    "ghc_family_score_identity_runner",
    "ghc_family_score_measure_address_runner",
    "ghc_family_score_edition_lineage_runner",
    "ghc_family_score_part_projection_runner",
    "ghc_family_score_transposition_runner",
    "ghc_family_score_duration_runner",
    "ghc_family_score_repeat_runner",
    "ghc_family_score_tempo_runner",
    "ghc_family_score_correction_runner",
    "ghc_family_score_authority_firewall_runner",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def write_json(relative: str, value: Any) -> Path:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json_bytes(value))
    return path


def write_text(relative: str, text: str) -> Path:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8"))
    return path


def run_git(*args: str, check: bool = True, binary: bool = False) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=check,
        capture_output=True,
        text=not binary,
        encoding=None if binary else "utf-8",
        errors=None if binary else "replace",
    )


def git(*args: str) -> str:
    return run_git(*args).stdout.strip()


def normalize_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.casefold()).strip()


def title_tokens(title: str) -> set[str]:
    return {token for token in normalize_title(title).split() if len(token) > 2}


def jaccard(left: str, right: str) -> float:
    a, b = title_tokens(left), title_tokens(right)
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b) if a | b else 0.0


def visible_proposal_inventory() -> tuple[dict[str, Any], dict[str, dict[str, str]]]:
    # Exact-source reachability excludes unrelated newer refs while retaining historical blobs.
    object_lines = run_git("rev-list", "--objects", SOURCE_FINAL, "--").stdout.splitlines()
    blob_paths: dict[str, str] = {}
    for line in object_lines:
        if " " not in line:
            continue
        oid, path = line.split(" ", 1)
        if path.endswith("proposal-freeze.json") or (
            "/proposal-freeze-shards/" in path and path.endswith(".json")
        ):
            blob_paths.setdefault(oid, path)
    records: list[dict[str, str]] = []
    parse_failures: list[dict[str, str]] = []
    for oid, source_path in sorted(blob_paths.items()):
        payload = run_git("cat-file", "blob", oid, binary=True).stdout
        try:
            document = json.loads(payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            parse_failures.append({"blob": oid, "source_path": source_path, "error_class": type(exc).__name__})
            continue
        for key in ("new_proposals", "proposals", "selected_inherited"):
            if source_path.startswith(f"{REL_PHASE_ROOT}/"):
                continue
            rows = document.get(key, [])
            if not isinstance(rows, list):
                continue
            for row in rows:
                if not isinstance(row, dict):
                    continue
                proposal_id = str(row.get("proposal_id") or row.get("id") or "")
                title = str(row.get("title") or row.get("proposal") or "")
                if proposal_id or title:
                    records.append({
                        "proposal_id": proposal_id,
                        "title": title,
                        "normalized_title": normalize_title(title),
                        "source_path": source_path,
                    })
    unique_by_id = {row["proposal_id"]: row for row in records if row["proposal_id"]}
    unique_by_title = {row["normalized_title"]: row for row in records if row["normalized_title"]}
    selectable = sorted(unique_by_id.values(), key=lambda row: (row["proposal_id"], row["normalized_title"]))
    if len(selectable) < 20:
        raise ValueError("fewer than twenty attributable inherited proposals are visible")
    selected: list[dict[str, Any]] = []
    for index in range(20):
        position = min(len(selectable) - 1, int((index + 0.5) * len(selectable) / 20))
        row = selectable[position]
        selected.append({
            "selection_id": f"SR6685-INHERITED-{index + 1:02d}",
            "proposal_id": row["proposal_id"],
            "title": row["title"],
            "source_path": row["source_path"],
            "novelty_credit": 0,
            "completion_credit": 0,
            "disposition": "selected_for_zero_credit_semantic_neighbor_review",
        })
    audit = {
        "declared_inherited_chain_count": INHERITED_FROZEN_PROPOSALS,
        "freeze_blob_count": len(blob_paths),
        "row_record_count": len(records),
        "unique_id_count": len(unique_by_id),
        "unique_visible_title_count": len(unique_by_title),
        "normalized_visible_title_sha256": sha256_bytes("\n".join(sorted(unique_by_title)).encode("utf-8")),
        "parse_failures": parse_failures,
        "selected_inherited": selected,
        "selected_count": 20,
        "selected_novelty_credit": 0,
        "selected_completion_credit": 0,
        "compressed_title_gap_count_minimum": max(0, INHERITED_FROZEN_PROPOSALS - len(unique_by_id)),
        "coverage_state": "VISIBLE_ROWS_AND_NEIGHBORS_AUDITED_COMPRESSED_OLDER_TITLES_REMAIN_OPEN_GAP",
        "boundary": "Visible titles can falsify a novelty claim; unavailable compressed titles cannot confirm one.",
    }
    return audit, unique_by_title


def proposal_rows(visible_titles: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    source_map = {
        "score-identity-lattice": ["SRC-BIBFRAME", "SRC-MEI51"],
        "measure-address-contract": ["SRC-MEI51", "SRC-MUSICXML40"],
        "edition-witness-lineage": ["SRC-MEI51", "SRC-PROV-DM"],
        "part-extraction-projection": ["SRC-MEI51", "SRC-MUSICXML40"],
        "signature-event-order": ["SRC-MEI51", "SRC-MUSICXML40"],
        "transposition-roundtrip": ["SRC-MEI51", "SRC-MUSICXML40"],
        "duration-tuplet-closure": ["SRC-MEI51", "SRC-MUSICXML40"],
        "repeat-traversal-guard": ["SRC-MEI51", "SRC-MUSICXML40"],
        "tempo-unit-ledger": ["SRC-MEI51"],
        "edition-integrity-ledger": ["SRC-PROV-DM", "SRC-RFC8785"],
        "canonical-score-digest": ["SRC-RFC8785"],
        "accessible-score-report": ["SRC-WCAG22"],
        "freed-id-score-graph": ["SRC-VC20", "SRC-PROV-DM"],
        "cbr-score-vacancies": ["SRC-PROV-DM", "SRC-BIBFRAME"],
        "rights-vacancy-firewall": ["SRC-BIBFRAME", "SRC-PROV-DM"],
    }
    visible_rows = list(visible_titles.values())
    result: list[dict[str, Any]] = []
    mutation_classes = (
        "missing_required_field",
        "wrong_type_or_domain",
        "forbidden_claim_promotion",
        "boundary_order_or_authority_bypass",
    )
    for index, (title, outcome, slug) in enumerate(PROPOSAL_BLUEPRINTS, 1):
        proposal_id = f"SR6685-N{index:03d}"
        neighbors = sorted(
            (
                {"proposal_id": row["proposal_id"], "title": row["title"], "similarity": round(jaccard(title, row["title"]), 6)}
                for row in visible_rows
            ),
            key=lambda row: (-row["similarity"], row["proposal_id"], row["title"]),
        )[:3]
        approval = "safe_now" if outcome == "completed" else "candidate"
        if outcome == "exact_gate":
            approval = "exact_approval"
        result.append({
            "proposal_id": proposal_id,
            "title": title,
            "semantic_slug": slug,
            "hypothesis": (
                f"A bounded Sable-local {slug} control can preserve declared score-edition provenance, "
                "failure, and abstention states without promoting absent evidence or authority."
            ),
            "null_or_failure_condition": (
                f"The {slug} control accepts an invalid fixture, loses a retained state, rewrites "
                "source truth, or implies a protected professional, scientific, identity, or authority claim."
            ),
            "approval_class": approval,
            "execution_lane": "owner-local synthetic and structural x2 lane; external actions and real material zero",
            "official_or_primary_source_needs": source_map.get(slug, ["SRC-MEI51", "SRC-PROV-DM"]),
            "concrete_artifacts": [
                f"x2/proposals/{proposal_id.casefold()}-{slug}.json",
                f"x2/cards/{proposal_id.casefold()}.json",
            ],
            "falsifier_or_acceptance_gate": (
                "The positive fixture must preserve its exact bounded state; all four preregistered "
                "mutations must be rejected; every protected claim remains false or gated."
            ),
            "rollback_or_recovery": (
                "Quarantine the owner-local artifact, retain the failed witness at zero credit, and "
                "correct only the smallest attributable dependency before a bounded retry."
            ),
            "protected_gates": list(PROTECTED_GATES),
            "expected_disposition": outcome,
            "x1_planning_only": True,
            "x2_execution_count": 0,
            "normalized_title": normalize_title(title),
            "visible_title_collision": normalize_title(title) in visible_titles,
            "semantic_neighbors": neighbors,
            "semantic_neighbor_quarantine_threshold": 0.75,
            "semantic_neighbor_quarantined": bool(neighbors and neighbors[0]["similarity"] >= 0.75),
            "negative_fixtures": [
                {
                    "mutation_id": f"{proposal_id}-M{offset:02d}",
                    "mutation_class": mutation_class,
                    "state": "preregistered_not_executed",
                    "credit": 0,
                }
                for offset, mutation_class in enumerate(mutation_classes, 1)
            ],
        })
    return result


def portfolio_rows(prefix: str, titles: list[str], category: str, state: str = "planned_for_x2") -> list[dict[str, Any]]:
    return [
        {
            "task_id": f"{prefix}-{index:02d}",
            "title": title,
            "category": category,
            "state": state,
            "completion_credit": 0,
            "x1_planning_only": True,
            "x2_execution_count": 0,
            "scope": "bounded owner-local synthetic or structural control; destructive cleanup and authority substitution excluded",
        }
        for index, title in enumerate(titles, 1)
    ]


def phase_owner_files() -> list[Path]:
    if not PHASE_ROOT.exists():
        return []
    return sorted(path for path in PHASE_ROOT.rglob("*") if path.is_file())


def manifest_rows(paths: Iterable[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(set(paths)):
        worktree_data = path.read_bytes()
        relative = path.relative_to(ROOT).as_posix()
        hashed = subprocess.run(
            ["git", "-C", str(ROOT), "hash-object", "-w", f"--path={relative}", "--stdin"],
            input=worktree_data,
            check=True,
            capture_output=True,
        )
        oid = hashed.stdout.decode("ascii").strip()
        data = run_git("cat-file", "blob", oid, binary=True).stdout
        rows.append({
            "path": relative,
            "git_blob_oid": oid,
            "sha256": sha256_bytes(data),
            "bytes": len(data),
            "canonical_domain": "git_blob_bytes_after_clean_filter_before_commit",
        })
    return rows


def word_count(path: Path) -> int:
    return len(re.findall(r"\b\w+[\w'-]*\b", path.read_text(encoding="utf-8")))


def assert_source_and_x1_only() -> None:
    head = git("rev-parse", "HEAD")
    if head != SOURCE_FINAL:
        raise ValueError("x1 must begin at the exact Auren final")
    if git("branch", "--show-current") != "codex/GHC-Family/sable-rook-v668-v5-full-tools":
        raise ValueError("unexpected Sable branch")
    allowed_x1_code = {
        "scripts/ghc_family_sable_rook_v668_v5_archive.py",
        "scripts/build_ghc_family_sable_rook_v668_v5_x1.py",
        "tests/test_ghc_family_sable_rook_v668_v5_x1.py",
    }
    status_lines = run_git("status", "--porcelain", "--untracked-files=all").stdout.splitlines()
    unexpected = []
    for line in status_lines:
        path = line[3:].strip().replace("\\", "/")
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        allowed_partial_x1 = (
            path.startswith("docs/sable-rook/v668-v5/x1/")
            or path.startswith("docs/sable-rook/v668-v5/method-flow/")
            or path.startswith("docs/sable-rook/v668-v5/validation/")
        )
        if path not in allowed_x1_code and not allowed_partial_x1:
            unexpected.append(line)
    if unexpected:
        raise ValueError(f"x1 builder found unexpected pre-freeze changes: {unexpected}")
    forbidden = [PHASE_ROOT / "x2", PHASE_ROOT / "evidence", PHASE_ROOT / "final", PHASE_ROOT / "closeout", PHASE_ROOT / "seal"]
    if any(path.exists() for path in forbidden):
        raise ValueError("x2 or closeout material exists before x1 freeze")
    script_names = git("ls-files", "--others", "--cached", "--", "scripts", "tests").splitlines()
    if any("sable_rook_v668_v5_x2" in name or "sable_rook_v668_v5_final" in name for name in script_names):
        raise ValueError("x2 or final implementation exists before x1 freeze")
