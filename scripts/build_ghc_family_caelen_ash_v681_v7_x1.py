#!/usr/bin/env python3
"""Materialize Caelen Ash v681-v7 planning-only x1 from an exact novelty receipt."""

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
BASE = ROOT / "docs" / "caelen-ash" / "v681-v7"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"

OWNER = "Caelen Ash"
PHASE = "v681-v7"
BRANCH = "codex/GHC-Family/caelen-ash-v681-v7-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/sable-rook-v681-v6-full-tools"
INHERITED_AUREN_SOURCE = "2a0210a495cbe557158095505671d599e0c33159"
SOURCE_X1 = "7285d38579cdf5e2fce3c6b0b013b49e940f44b5"
SOURCE_EVIDENCE = "7fe9cd2c6c487a7b871ab96ad9b635ea3a8580ba"
SOURCE = "4da1c50b22e1b30b5e7351b0641f350bdc8fbfbe"
DECLARED_CHAIN_BEFORE = 10070
DECLARED_CHAIN_AFTER = 10130
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
EXPECTED_AUDIT_SHA256 = "9c475b9eec50a0988d33fc79ba1341137fc3386b5edac7a0b7a9ad6f326c4a23"

WRITTEN: list[str] = []


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    WRITTEN.append(rel(path))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")
    WRITTEN.append(rel(path))


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


PROPOSAL_TITLES = [
    "Synthetic planetarium programme work and projected dome presentation referent split",
    "Show-package identifier with edition and venue-instance separation",
    "Fulldome master asset and physical projection-system non-equivalence",
    "Sky-scene catalogue label with source-model verification vacancy",
    "Star-field source token with zero catalogue-row materialization",
    "Epoch label and observation-time non-equivalence",
    "Reference-frame name with no coordinate-transform execution",
    "Angular-unit declaration and bare-number quarantine",
    "Projection geometry profile and measured dome calibration separation",
    "Dome-zone identifier with exact venue-location nonmaterialization",
    "Cue sequence ordinal with duplicate-cue quarantine",
    "Cue start and end timestamps with negative-duration rejection",
    "Overlapping cue pair with intentional-overlap declaration hold",
    "Nonmonotonic cue-arrival ledger preserving declared sequence and correction lineage",
    "Cue amendment lineage with prior-state retention",
    "Narration track and caption track synchronization obligation",
    "WebVTT cue vocabulary crosswalk without media conformance",
    "Audio-description cue pointer with zero recording bytes",
    "Tactile or text alternative reference with manual-evaluation vacancy",
    "Photosensitivity notice placeholder without clinical or safety determination",
    "Sensory-intensity label with affected-user review vacancy",
    "Language-track tag and translation-authority separation",
    "Pronunciation note with cultural-language authority hold",
    "Accessible seating request token without allocation decision",
    "Quiet-session option state with service-availability vacancy",
    "Rehearsal public-show and cancelled-show state separation",
    "Equipment readiness flag and professional-inspection non-equivalence",
    "Projector-lamp service note with electrical-safety authority vacancy",
    "Laser-content marker without classification or operating authorization",
    "Emergency-stop status placeholder without operational-safety claim",
    "Maintenance quarantine release and return-to-service separation",
    "Synthetic cue-review responsibility token with worker status and credential assertions refused",
    "Workload pause and resumable cue-review ownership transfer",
    "Shift handover receipt with unresolved-exception readback",
    "Show-metadata amendment challenge queue with remedy-decision vacancy",
    "Minimum-disclosure attendee alias with identity refusal",
    "Pseudonymous audience-feedback object with zero person linkage",
    "Synthetic feedback retention horizon with expiration-only and no erase action",
    "Rights-source pointer and public-performance permission vacancy",
    "Cultural sky-knowledge content hold with affected-community gate",
    "Maori astronomy wording and matauranga authority reservation",
    "Canonical JSON digest for zero-row show-cue structure",
    "Represented GMUT epoch-frame obligation board with no observational rows",
    "Represented GMUT covariance-shape analogy without likelihood or posterior",
    "Represented GMUT projection-residual sign board without force or prediction",
    "Represented THOS cue-orchestration proxy with reversible holds",
    "Represented THOS workload cancellation and handover state machine",
    "Represented Freed ID anonymous programme-access pseudonym graph with no identity event",
    "Represented Freed ID admission-capability envelope with no cryptographic lifecycle",
    "Represented CBR accommodation-metadata challenge queue with remedy authority vacant",
    "Represented CBR cultural-content refusal appeal without authority decision",
    "Represented IAU SOFA vocabulary crosswalk without astronomical computation",
    "Represented NASA SPICE frame-time vocabulary without kernels or transforms",
    "Represented PROV-O cue-revision graph without provenance conformance",
    "Open gap for real planetarium technicians astronomers captioners and accessibility specialists",
    "Open gap for real dome geometry show playback cue timing and independent reproduction",
    "Open gap for disabled visitors multilingual audiences affected communities and Maori-language evaluation",
    "Exact gate for venue safety laser electrical emergency and public-show release decisions",
    "Exact gate for cultural sky knowledge tikanga matauranga Maori data governance and Maori authority",
    "Stage 20 nonpromotion boundary for all synthetic planetarium artifacts and all empirical deployment identity AGI ASI consciousness personhood proof canon or Theory of Everything claims",
]

MUTATION_TYPES = [
    "remove_required_field",
    "duplicate_identifier",
    "invert_order_or_interval",
    "promote_reserved_authority_claim",
    "inject_private_or_real_row",
]

PROTECTED_GATES = [
    "no real people venues domes projectors shows cues recordings catalogues measurements credentials or external actions",
    "no empirical GMUT likelihood posterior force prediction parameter constraint or Theory of Everything claim",
    "no THOS operational effectiveness production deployment AGI ASI or public-safety claim",
    "no Freed ID production key proof issuance resolution status revocation interoperability or trust-governance claim",
    "no professional legal cultural affected-party privacy-complete accessibility-complete or Maori-authority claim",
    "NOT_READY_FOR_STAGE_20",
]


def disposition(index: int) -> str:
    if index <= 42:
        return "completed"
    if index <= 54:
        return "represented"
    if index <= 57:
        return "open_gap"
    return "exact_gate"


def approval_class(index: int) -> str:
    if index <= 42:
        return "safe_now"
    if index <= 57:
        return "bounded_candidate"
    return "exact_approval"


def execution_lane(index: int) -> str:
    if index <= 42:
        return "owner_local_synthetic_zero_row"
    if index <= 54:
        return "represented_external_evidence_vacancy"
    if index <= 57:
        return "open_external_evidence_gap"
    return "unexecuted_competent_authority_gate"


def source_needs(index: int) -> list[str]:
    if index in {6, 7, 8, 43, 44, 45, 52, 53}:
        return ["IAU-SOFA", "IAU-RESOLUTIONS", "NASA-NAIF-SPICE", "RFC3339"]
    if index in {16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 50, 54, 57}:
        return ["W3C-WEBVTT", "W3C-WCAG22", "NZ-WEB-ACCESS"]
    if index in {35, 36, 37, 38, 39, 40, 41, 48, 49, 50, 51, 59}:
        return ["W3C-PROV-O", "NZ-PRIVACY", "TMR-PRINCIPLES"]
    return ["W3C-PROV-O", "RFC8785", "JSON-SCHEMA-2020-12"]


def proposals() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, title in enumerate(PROPOSAL_TITLES, start=1):
        proposal_id = f"CA6817-N{index:03d}"
        expected = disposition(index)
        rows.append(
            {
                "approval_class": approval_class(index),
                "concrete_artifacts": [
                    f"docs/caelen-ash/v681-v7/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/caelen-ash/v681-v7/x2/positive-controls.json#{proposal_id}",
                    f"docs/caelen-ash/v681-v7/x2/mutation-results.json#{proposal_id}",
                ],
                "execution_lane": execution_lane(index),
                "expected_disposition": expected,
                "falsifier_or_acceptance_gate": (
                    f"Accept {proposal_id} only when one wholly synthetic zero-row witness passes, "
                    "all five preregistered invalid mutations are rejected, and no protected claim is promoted."
                ),
                "hypothesis": (
                    f"A deterministic owner-local contract can represent '{title}' while retaining explicit "
                    "unknown, disputed, open, and authority-gated states."
                ),
                "null_or_failure_condition": (
                    "The contract fails if a required field, unique identifier, monotonic or declared interval, "
                    "privacy refusal, provenance link, or authority hold is absent or promoted."
                ),
                "official_or_primary_source_needs": source_needs(index),
                "proposal_id": proposal_id,
                "protected_gates": PROTECTED_GATES,
                "rejecting_mutations": [
                    {"expected": "reject", "mutation_id": f"{proposal_id}-M{slot:02d}", "mutation_type": kind}
                    for slot, kind in enumerate(MUTATION_TYPES, start=1)
                ],
                "rollback_or_recovery": (
                    f"Quarantine only the {proposal_id} witness, retain its failure at zero credit, and "
                    "regenerate from this immutable planning contract without changing another proposal."
                ),
                "title": title,
            }
        )
    return rows


def planned_tasks(prefix: str, count: int, lane: str, titles: list[str]) -> list[dict[str, Any]]:
    actions = [
        "type the record boundary",
        "test the acceptance and refusal pair",
        "verify provenance and rollback fields",
        "review the authority and privacy hold",
        "check the accessible text representation",
    ]
    return [
        {
            "approval_lane": lane,
            "executed_in_x1": False,
            "task_id": f"{prefix}-{index:03d}",
            "task": f"{actions[(index - 1) % len(actions)]} for {titles[(index - 1) % len(titles)]}",
        }
        for index in range(1, count + 1)
    ]


STARTUP_FAILURES = [
    ("The first broad memory-registry projection exceeded its bounded output.", "Use exact v681 and owner terms with bounded line windows."),
    ("A PowerShell foreach-to-pipeline wrapper failed with EmptyPipeElement before its read.", "Materialize scalar objects before piping."),
    ("The first authorization-state display truncated before EOF.", "Read contiguous bounded windows through the exact final line."),
    ("A broad source-tree projection truncated before terminal paths were attributable.", "Inventory only the exact phase subtree and then each lifecycle directory."),
    ("A per-blob size probe yielded without preserving its running-session handle.", "Use one bounded ls-tree size projection and preserve every later session handle."),
    ("A broad candidate-reference projection truncated repeated proposal text.", "Read the candidate in bounded exact line windows through EOF."),
    ("The first integrated-overview projection truncated mid-document.", "Read the overview in five bounded numbered windows through EOF."),
    ("A whole-drive filename probe yielded without an attributable result.", "Search only bounded receipt banks and retain the exact session handle."),
    ("The first per-entry manifest replay yielded without preserving its handle.", "Use restricted path lists and one cat-file batch per immutable revision."),
    ("A Measure-Object parameter combination was invalid before its scalar summary.", "Materialize path lengths and use the valid Sum parameter set."),
    ("A Git archive manifest replay remained I/O-bound and was cancelled without credit.", "Use restricted ls-tree mappings and cat-file batch blobs."),
    ("A whole-tree ls-tree manifest replay remained I/O-bound and was cancelled.", "Pass only manifest-declared paths to ls-tree before one batch read."),
    ("A broad proposal-ledger enumeration exceeded its bounded window.", "Use the exact proposal_id Git-grep and a single batched blob stream."),
    ("The native worktree-registry listing exceeded its bounded window.", "Inspect the exact common registry files and target path without enumerating display output."),
    ("A combined x2 source-packet projection truncated after its output ceiling.", "Split the packet at exact file boundaries and reread the remainder."),
    ("A domain-keyword Git grep exceeded its bounded window and was cancelled.", "Run the exact all-reachable proposal corpus audit once and persist its receipt."),
    ("The initial skill-creator display truncated before EOF.", "Reread the skill-creator guidance in bounded contiguous windows through EOF."),
    ("The first oversized apply-patch result exceeded its output projection and left application state ambiguous.", "Inspect the exact two target files and Git state, compile both files, and patch only the verified count delta."),
]


def source_entries() -> list[tuple[str, str, str, str]]:
    return [
        ("IAU-SOFA", "IAU Standards of Fundamental Astronomy", "https://www.iausofa.org/", "fundamental-astronomy algorithm and model vocabulary only; no computation or validation claim"),
        ("IAU-RESOLUTIONS", "IAU resolutions on reference systems", "https://www.iau.org/Iau/Iau/Publications/List-of-Resolutions.aspx", "reference-system and time-standard vocabulary only"),
        ("NASA-NAIF-SPICE", "NASA NAIF SPICE documentation", "https://naif.jpl.nasa.gov/naif/", "frame time kernel and metadata vocabulary only; no kernel load or geometry computation"),
        ("W3C-WEBVTT", "WebVTT Candidate Recommendation Draft 20 May 2026", "https://www.w3.org/TR/webvtt1/", "timed-text cue vocabulary only; work-in-progress status and no conformance remain explicit"),
        ("W3C-WCAG22", "Web Content Accessibility Guidelines 2.2", "https://www.w3.org/TR/WCAG22/", "structural accessibility vocabulary with manual and affected-user evaluation reserved"),
        ("W3C-PROV-O", "W3C PROV-O", "https://www.w3.org/TR/prov-o/", "entity activity revision and role vocabulary only; no provenance conformance"),
        ("RFC3339", "RFC 3339 Date and Time on the Internet", "https://www.rfc-editor.org/rfc/rfc3339.html", "timestamp syntax vocabulary only; no astronomical time equivalence"),
        ("RFC8785", "RFC 8785 JSON Canonicalization Scheme", "https://www.rfc-editor.org/rfc/rfc8785.html", "deterministic receipt vocabulary only; informational status remains explicit"),
        ("JSON-SCHEMA-2020-12", "JSON Schema Draft 2020-12", "https://json-schema.org/draft/2020-12", "synthetic record validation vocabulary only"),
        ("NZ-PRIVACY", "New Zealand Privacy Act 2020 principles", "https://www.privacy.org.nz/privacy-principles/", "privacy collection access correction retention and identifier vocabulary only; no legal conclusion"),
        ("NZ-WEB-ACCESS", "New Zealand Web Accessibility Standard 1.2", "https://www.digital.govt.nz/standards-and-guidance/nz-government-web-standards/web-accessibility-standard-1-2/", "public-sector accessibility context only; no applicability or conformance conclusion"),
        ("TMR-PRINCIPLES", "Te Mana Raraunga Principles of Maori Data Sovereignty", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Maori data-governance authority vacancy boundary only; never delegated authority or cultural ratification"),
    ]


SKILL_NAMES = [
    "ghc-family-planetarium-work-show-referent-split",
    "ghc-family-show-package-edition-instance",
    "ghc-family-fulldome-master-system-firewall",
    "ghc-family-sky-scene-source-vacancy",
    "ghc-family-epoch-observation-separator",
    "ghc-family-frame-transform-refusal",
    "ghc-family-angular-unit-rail",
    "ghc-family-dome-calibration-vacancy",
    "ghc-family-cue-identifier-quarantine",
    "ghc-family-cue-interval-validator",
    "ghc-family-cue-overlap-declaration",
    "ghc-family-cue-correction-lineage",
    "ghc-family-caption-narration-sync-obligation",
    "ghc-family-photosensitivity-notice-firewall",
    "ghc-family-language-authority-hold",
    "ghc-family-accessible-dome-status",
    "ghc-family-equipment-readiness-inspection-split",
    "ghc-family-planetarium-handover-readback",
    "ghc-family-audience-alias-minimizer",
    "ghc-family-stage20-planetarium-refusal",
]

RUNNER_NAMES = [
    "ghc_family_planetarium_schema_runner",
    "ghc_family_planetarium_cue_runner",
    "ghc_family_planetarium_epoch_frame_runner",
    "ghc_family_planetarium_accessibility_runner",
    "ghc_family_planetarium_provenance_runner",
    "ghc_family_planetarium_privacy_runner",
    "ghc_family_planetarium_mutation_runner",
    "ghc_family_planetarium_outcome_runner",
    "ghc_family_planetarium_manifest_runner",
    "ghc_family_planetarium_stage20_runner",
]


def load_audit(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    if digest(raw) != EXPECTED_AUDIT_SHA256:
        raise RuntimeError("proposal audit receipt digest mismatch")
    audit = json.loads(raw.decode("utf-8"))
    if audit.get("source") != SOURCE or audit.get("new_proposal_count") != 60:
        raise RuntimeError("proposal audit source or count mismatch")
    if audit.get("exact_title_collisions") or audit.get("quarantined_neighbors"):
        raise RuntimeError("proposal audit contains a collision or quarantine")
    reviewed = [row.get("title") for row in audit.get("neighbor_reviews", [])]
    if reviewed != PROPOSAL_TITLES:
        raise RuntimeError("proposal audit title order differs from frozen proposal set")
    if audit.get("maximum_neighbor_score", 1.0) >= 0.78:
        raise RuntimeError("proposal audit maximum score exceeds quarantine threshold")
    audit["external_preflight_receipt_sha256"] = EXPECTED_AUDIT_SHA256
    audit["manual_refinement"] = {
        "initial_formal_pass_maximum_neighbor_score": 0.777778,
        "reason": "eight generic titles were voluntarily tightened before freeze despite no formal quarantine",
        "revised_maximum_neighbor_score": audit["maximum_neighbor_score"],
    }
    return audit


def build(audit_path: Path) -> None:
    if git("rev-parse", "HEAD").stdout.strip() != SOURCE:
        raise RuntimeError("x1 builder must begin at the immutable Sable final")
    if git("branch", "--show-current").stdout.strip() != BRANCH:
        raise RuntimeError("wrong Caelen owner branch")
    if (BASE / "x2").exists() or (BASE / "final").exists():
        raise RuntimeError("x2 or final material is forbidden in planning-only x1")

    proposal_records = proposals()
    expected = Counter({"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
    if len(proposal_records) != 60 or Counter(row["expected_disposition"] for row in proposal_records) != expected:
        raise RuntimeError("proposal count or disposition contract drift")
    if any(len(row["rejecting_mutations"]) != 5 for row in proposal_records):
        raise RuntimeError("every proposal requires exactly five rejecting mutations")
    if any(row["expected_disposition"] not in ALLOWED_OUTCOMES for row in proposal_records):
        raise RuntimeError("unknown outcome label")

    audit = load_audit(audit_path)
    inherited = json.loads(git("show", f"{SOURCE}:docs/sable-rook/v681-v6/x1/new-proposal-freeze.json").stdout)
    inherited_reviews = [
        {
            "completion_credit": 0,
            "inherited_owner": "Sable Rook",
            "proposal_id": row["proposal_id"],
            "review_state": "inherited_source_evidence_only",
            "title": row["title"],
        }
        for row in inherited["proposals"][-20:]
    ]
    startup = [
        {
            "failed_witness": failed,
            "failure_id": f"CA6817-ST-N{index:03d}",
            "initial_credit": 0,
            "recovery": recovery,
            "recovery_credit": "bounded_dependency_only",
        }
        for index, (failed, recovery) in enumerate(STARTUP_FAILURES, start=1)
    ]

    sources = {
        "authority_conferred": False,
        "checked_at_nz": "2026-09-01",
        "citations_are_observations": False,
        "entries": [
            {"source_id": sid, "status": "official_or_primary_source_checked_2026-09-01", "title": title, "url": url, "use": use}
            for sid, title, url, use in source_entries()
        ],
        "external_source_entries": len(source_entries()),
        "network_data_queries": 0,
        "official_source_web_queries": 15,
        "owner": OWNER,
        "phase": PHASE,
        "real_data_rows": 0,
        "schema": "ghc.family.official-primary-sources.v681.v7.x1",
    }
    titles = [row["title"] for row in proposal_records]
    portfolio = {
        "blocked": planned_tasks("BLOCK", 10, "blocked", titles[57:]),
        "caps_are_ceilings": True,
        "commit_cap": 3,
        "document_word_cap": 100000,
        "exact_approval": planned_tasks("APPROVAL", 20, "exact_approval", titles[57:]),
        "materialized_file_stop": 2000,
        "owner_candidates": planned_tasks("CAND", 80, "bounded_candidate", titles[42:57]),
        "owner_clean_fix_refine": planned_tasks("CFR", 100, "clean_fix_refine", titles),
        "owner_practice_lenses": [
            "wholly synthetic planetarium show-cue provenance stewardship",
            "wholly synthetic astronomical visualization metadata quality analysis",
            "wholly synthetic accessible dome-program handover review",
        ],
        "owner_runner_ideas": [{"runner": name, "state": "preregistered_not_built"} for name in RUNNER_NAMES],
        "owner_skill_ideas": [{"skill": name, "state": "preregistered_not_built"} for name in SKILL_NAMES],
        "phase": PHASE,
        "primary_pillar": "GMUT Mind",
        "represented_pillars": ["THOS Body", "Freed ID and CBR Heart"],
        "safe_now": planned_tasks("SAFE", 120, "safe_now", titles[:42]),
        "schema": "ghc.family.portfolio-freeze.v681.v7.x1",
        "successor_candidates": planned_tasks("SUCC-CAND", 20, "successor_seed", titles[42:57]),
        "successor_clean_fix_refine": planned_tasks("SUCC-CFR", 30, "successor_seed", titles),
        "successor_practice_recommendation": "wholly synthetic marine navigation chart-correction and notice-to-mariners handover review, subject to successor independent choice and every professional safety legal cultural and Maori-authority gate",
        "successor_runner_ideas": planned_tasks("SUCC-RUN", 10, "successor_seed", titles),
        "successor_skill_ideas": planned_tasks("SUCC-SKILL", 10, "successor_seed", titles),
    }

    write_json(X1 / "activation-intake.json", {
        "activation": "ACKNOWLEDGED_EXISTING_TASK_SEND",
        "created_or_forked_task": False,
        "owner": OWNER,
        "phase": PHASE,
        "relational_language_only": True,
        "schema": "ghc.family.activation-intake.v681.v7.x1",
        "sent_by_sable_rook": True,
        "solo": True,
        "source": SOURCE,
    })
    write_json(X1 / "identity-and-boundary.json", {
        "hope": "Keep every synthetic sky cue, epoch, correction, and access vacancy traceable without confusing a dome-show model with observation or astronomical authority.",
        "name": OWNER,
        "not_evidence_of": ["consciousness", "sentience", "personhood", "identity continuity", "employment", "qualification", "independent agency", "scientific operational professional legal cultural affected-party or Maori authority"],
        "optional_pronouns": "they/she",
        "relational_working_language_only": True,
        "role": "Cue-Epoch Cartographer and Accessible Dome Handover Steward",
        "schema": "ghc.family.identity-boundary.v681.v7.x1",
    })
    write_json(X1 / "source-verification.json", {
        "branch": SOURCE_BRANCH,
        "candidate_blob": "7d6ca7c18afbc9dc60805ba34df11a44ef29424e",
        "candidate_sha256": "ffd22cf3750f99787f87a852fa8f572daabf8aa079e26ffa7d37cd9921bc9b72",
        "candidate_words": 29186,
        "clean": True,
        "commits_source_to_final": 3,
        "content_seal_entries_replayed": 15,
        "content_seal_mismatches": 0,
        "divergence": {"ahead": 0, "behind": 0},
        "evidence": SOURCE_EVIDENCE,
        "evidence_parent": SOURCE_X1,
        "final": SOURCE,
        "final_parent": SOURCE_EVIDENCE,
        "four_way_fresh_live_equal": True,
        "inherited_auren_final": INHERITED_AUREN_SOURCE,
        "manifest_entries_replayed": 242,
        "manifest_mismatches": 0,
        "merges": 0,
        "receipt_sha256": "3bcf6f2e2e7f6265b25bbbdf4b29c744d98a4a50b39c7ae81cff62b974a7d953",
        "schema": "ghc.family.source-verification.v681.v7.x1",
        "x1": SOURCE_X1,
        "x1_parent": INHERITED_AUREN_SOURCE,
    })
    baseline = {"bounded_passing_witnesses": 44737, "effective_methods": 62915, "effective_negatives": 54528, "exact_gates": 473, "failed_witnesses": 26189, "open_gaps": 482}
    current = dict(baseline)
    for key in ("bounded_passing_witnesses", "effective_methods", "effective_negatives", "failed_witnesses"):
        current[key] += len(startup)
    write_json(X1 / "method-flow-startup.json", {
        "activation_baseline_repository_sealed": baseline,
        "current_after_startup": current,
        "failure_erasure": False,
        "owner": OWNER,
        "phase": PHASE,
        "recoveries_retroactively_promote_failure": False,
        "schema": "ghc.family.method-flow-startup.v681.v7.x1",
        "startup_failures": startup,
    })
    write_json(X1 / "new-proposal-freeze.json", {
        "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
        "declared_chain_before": DECLARED_CHAIN_BEFORE,
        "expected_disposition_counts": dict(Counter(row["expected_disposition"] for row in proposal_records)),
        "owner": OWNER,
        "phase": PHASE,
        "proposal_count": len(proposal_records),
        "proposals": proposal_records,
        "schema": "ghc.family.new-proposal-freeze.v681.v7.x1",
        "source": SOURCE,
        "x2_outcomes_present": False,
    })
    write_json(X1 / "proposal-chain-audit.json", audit)
    write_json(X1 / "inherited-revalidation-freeze.json", {
        "completion_credit": 0,
        "count": len(inherited_reviews),
        "owner": OWNER,
        "phase": PHASE,
        "reviews": inherited_reviews,
        "schema": "ghc.family.inherited-revalidation.v681.v7.x1",
    })
    write_json(X1 / "official-primary-source-ledger.json", sources)
    write_json(X1 / "portfolio-freeze.json", portfolio)
    write_json(X1 / "clean-fix-refine-plan.json", {"owner": OWNER, "phase": PHASE, "schema": "ghc.family.clean-fix-refine-plan.v681.v7.x1", "tasks": portfolio["owner_clean_fix_refine"], "x2_execution_present": False})
    write_json(X1 / "skill-runner-plan.json", {"global_install": False, "owner": OWNER, "phase": PHASE, "runners": portfolio["owner_runner_ideas"], "schema": "ghc.family.skill-runner-plan.v681.v7.x1", "skills": portfolio["owner_skill_ideas"], "x2_implementation_present": False})
    write_json(X1 / "approval-hold-register.json", {"blocked_count": 10, "exact_approval_count": 20, "executed": 0, "owner": OWNER, "phase": PHASE, "schema": "ghc.family.approval-holds.v681.v7.x1"})
    write_json(X1 / "route-plan.json", {
        "current_owner": OWNER,
        "recipient_contacted": False,
        "resolution_rule": "refresh newest live authority and native task registry only after exact-final canonical success; require one unique exact authorized title, immediate reread, duplicate pause privacy evidence safety usage and acknowledgement guards, then one send at most",
        "route_authority_through": "v725-v8",
        "schema": "ghc.family.route-plan.v681.v7.x1",
        "successor_not_precontacted": True,
        "terminal_gate_required": True,
    })
    write_json(X1 / "workflow-plan.json", {"commit_ceiling": 3, "owner": OWNER, "phase": PHASE, "schema": "ghc.family.workflow-plan.v681.v7.x1", "stages": [{"name": "x1", "state": "planning_only_freeze"}, {"name": "x2", "state": "not_started"}, {"name": "final", "state": "not_started"}], "strict_x1_before_x2": True})
    write_json(X1 / "threat-model.json", {
        "controls": [
            "synthetic.example.invalid namespace only",
            "zero real people venues domes projectors shows cues recordings catalogue rows measurements credentials and external writes",
            "authority promotion rejected",
            "five privacy classes scanned with candidate adjudication",
            "exact approval and blocked packets remain unexecuted",
        ],
        "owner": OWNER,
        "phase": PHASE,
        "real_world_action": False,
        "schema": "ghc.family.threat-model.v681.v7.x1",
    })
    write_json(X1 / "wellbeing-and-corrigibility.json", {"correction_readback": True, "owner": OWNER, "pause_resume_stop_visible": True, "phase": PHASE, "relational_language_only": True, "schema": "ghc.family.wellbeing-corrigibility.v681.v7.x1", "workload_control_planned": True})
    write_json(X1 / "phase-truth.json", {
        "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
        "execution_state": "PLANNING_ONLY_X1",
        "expected_dispositions": {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
        "observed_outcomes": None,
        "owner": OWNER,
        "phase": PHASE,
        "proposal_count": 60,
        "schema": "ghc.family.phase-truth.v681.v7.x1",
        "terminal_verdict": TERMINAL_VERDICT,
        "x2_started": False,
    })
    write_text(X1 / "integrated-overview.md", """# Caelen Ash v681-v7 planning-only x1

Caelen Ash uses the phase-local relational role **Cue-Epoch Cartographer and Accessible Dome Handover Steward**, they/she pronouns, and the bounded hope of keeping every synthetic sky cue, epoch, correction, and access vacancy traceable without confusing a dome-show model with observation or astronomical authority. This is relational working language only, never evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, or authority.

This immutable planning-only x1 freezes sixty genuinely new contracts after an exact-source audit of 10,075 proposal-bearing JSON blobs and 34,861 reachable ID/title records. The revised maximum token-Jaccard neighbor score is 0.758621, with zero exact collisions and zero quarantines. Twenty inherited Sable reviews retain zero Caelen novelty or completion credit. X1 contains no implementation, observed outcome, phase-local skill, runner, mutation result, or x2 completion claim.

GMUT Mind is primary through wholly synthetic epoch, reference-frame, angular-unit, cue-order, projection-residual, provenance, and uncertainty obligations. THOS Body remains represented through cue orchestration, workload, cancellation, correction readback, and reversible handover. Freed ID and CBR Heart remain represented through subjectless access placeholders, minimum disclosure, correction, contest, remedy vacancies, and authority holds. The three bounded learning lenses are planetarium show-cue provenance stewardship, astronomical-visualization metadata quality analysis, and accessible dome-program handover review. They establish no employment, qualification, astronomical computation, planetarium competence, operational safety, legal or cultural authority, affected-party acceptance, or Maori authority.

IAU SOFA and resolutions, NASA NAIF/SPICE, W3C WebVTT, WCAG 2.2 and PROV-O, RFC 3339 and 8785, JSON Schema, New Zealand privacy and accessibility sources, and Te Mana Raraunga supply vocabulary and refusal conditions only. No real datum, kernel, catalogue row, transform, venue, person, show, cue, asset, measurement, credential, or external system was queried or used. Citation is not observation, endorsement, conformance, professional evaluation, legal interpretation, cultural ratification, or delegated authority.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family without a physical likelihood, posterior, detected force, prediction, parameter constraint, ultraviolet or quantum completion, Theory-of-Everything proof, or canon. THOS remains proxy-only without preregistered blind matched-budget real arms, participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without real keys and proofs, issuance, resolution, status, revocation, interoperability, privacy and independent security review, recovery evidence, and trust governance. CBR and every safety, accessibility, privacy, consent, rights, remedy, legal, cultural, language, Maori data-governance, and Maori-authority decision remain open or exact-gated. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
""")

    script_path = "scripts/build_ghc_family_caelen_ash_v681_v7_x1.py"
    test_path = "tests/test_ghc_family_caelen_ash_v681_v7_x1.py"
    exclusions = [
        "docs/caelen-ash/v681-v7/validation/x1-index-manifest.json",
        "docs/caelen-ash/v681-v7/validation/x1-privacy-scan.json",
        "docs/caelen-ash/v681-v7/validation/x1-staged-review.json",
    ]
    content_paths = sorted(set(WRITTEN + [script_path, test_path]))
    scanners = {
        "raw_uuid": re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives)[\\/]"),
        "raw_task_thread_identifier": re.compile(r"\b(?:source_thread_id|thread_id)\b", re.IGNORECASE),
        "credential_assignment": re.compile(r"\b(?:api[_-]?key|token|password|secret)\s*[:=]\s*[^\s]+", re.IGNORECASE),
        "private_conversation_payload": re.compile(r"source_thread_id|codex_delegation", re.IGNORECASE),
    }
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    for path_text in content_paths:
        content = (ROOT / path_text).read_text(encoding="utf-8", errors="replace")
        for class_name, pattern in scanners.items():
            if pattern.search(content):
                row = {"class": class_name, "disposition": "scanner_definition_only" if path_text == script_path else "confirmed_payload_hit", "path": path_text}
                candidates.append(row)
                if row["disposition"] == "confirmed_payload_hit":
                    confirmed.append(row)
    if confirmed:
        raise RuntimeError("confirmed privacy payload hit: " + json.dumps(confirmed))
    write_json(VALIDATION / "x1-privacy-scan.json", {"candidates": candidates, "confirmed_hits": confirmed, "owner": OWNER, "phase": PHASE, "privacy_classes": list(scanners), "scanned_files": len(content_paths), "schema": "ghc.family.privacy-scan.v681.v7.x1"})
    write_json(VALIDATION / "x1-staged-review.json", {"declared_self_exclusions": exclusions, "expected_paths": sorted(content_paths + exclusions), "lifecycle": "planning_only_x1", "owner": OWNER, "path_count": len(content_paths) + len(exclusions), "phase": PHASE, "schema": "ghc.family.staged-review.v681.v7.x1", "x2_paths": []})
    entries = []
    for path_text in content_paths:
        data = normalized_bytes(ROOT / path_text)
        entries.append({"bytes": len(data), "path": path_text, "sha256": digest(data)})
    write_json(VALIDATION / "x1-index-manifest.json", {"declared_self_exclusions": exclusions, "entries": entries, "entry_count": len(entries), "owner": OWNER, "phase": PHASE, "schema": "ghc.family.normalized-lf-index-manifest.v681.v7.x1", "source": SOURCE})
    print(json.dumps({"audit_paths": audit["audit_scope"]["proposal_json_paths_parsed"], "maximum_neighbor_score": audit["maximum_neighbor_score"], "proposal_count": len(proposal_records), "startup_failures": len(startup), "status": "X1_PLANNING_ONLY_MATERIALIZED", "written_paths": len(WRITTEN)}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--proposal-audit-receipt", required=True, type=Path)
    args = parser.parse_args()
    build(args.proposal_audit_receipt)


if __name__ == "__main__":
    main()
