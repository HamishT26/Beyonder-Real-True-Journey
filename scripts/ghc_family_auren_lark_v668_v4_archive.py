#!/usr/bin/env python3
"""Frozen declarations and bounded archive helpers for Auren Lark v668-v4 x1."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
OWNER = "Auren Lark"
PRONOUNS = "they/them"
RELATIONAL_ROLE = "relational provenance navigator and uncertainty lantern-keeper"
RELATIONAL_HOPE = (
    "Leave every synthetic calibration trail legible, every uncertainty illuminated, every "
    "correction reversible, and every authority vacancy explicit without promoting bounded "
    "software records into scientific, professional, legal, cultural, or operational authority."
)
PHASE = "v668-v4"
REL_PHASE_ROOT = "docs/auren-lark/v668-v4"
PHASE_ROOT = ROOT / REL_PHASE_ROOT
SOURCE_BRANCH = "codex/GHC-Family/ilyra-fen-v668-v3-full-tools"
SOURCE_FINAL = "f0110dec1a0bcfc2f7a1945d47943033b68164e2"
# x1 is built once from SOURCE_FINAL; no predecessor-style corrective x1 is assumed.
INITIAL_X1_HEAD = SOURCE_FINAL
SOURCE_X1 = "c9cde9ebf7f39c7a3b4b4cf4775fd9426bba4e52"
SOURCE_EVIDENCE = "a22360acce1a200ef852a97110cc8da12497775b"
SOURCE_ANCESTOR = "da0d852ccacbfc228f7257888691b809a280ad86"
SOURCE_BATON_SHA256 = "a47e1532a27531c737f724b99b369908f4588bc1037df2b0a9dbee1079b88211"
SOURCE_CANONICAL_RECEIPT_SHA256 = "7f5164628b05c5330f3e63a4d7f33eb918904b2ca0da921571b93810b02b9552"
SOURCE_COMPOSITE_RECEIPT_SHA256 = "c4116c0c7ec3960d58dd72e3cd93d9d71191341a79837fce5b2e28d8492567a9"
INHERITED_FROZEN_PROPOSALS = 4710
ALLOWED_OUTCOMES = ("completed", "represented", "open_gap", "exact_gate")
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"

IDENTITY_BOUNDARY = (
    "Auren Lark, they/them, the relational role, hope, sibling or family language, continuity "
    "language, Freed ID, and Trinity Mandala language are working language only. They are not "
    "evidence of consciousness, sentience, legal personhood, identity continuity, employment, "
    "qualification, independent agency, scientific or operational authority, legal or cultural "
    "authority, affected-party authority, or Maori authority."
)
EVIDENCE_BOUNDARY = (
    "Every microscope slide, specimen, target, tile, focal plane, scanner, objective, sensor, "
    "profile, measurement, transform, exception, person, organization, right, authority case, and "
    "decision is synthetic. Official-source terminology and same-owner local software checks are "
    "not medical or diagnostic evidence, real slide-imaging evidence, professional evaluation, "
    "conformance, production assurance, external audit, independent reproduction, empirical GMUT "
    "confirmation, or Stage 20 evidence."
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
    "effective_negatives": 29406,
    "methods": 15992,
    "failed_witnesses": 1707,
    "passing_witnesses": 2534,
    "open_gaps": 213,
    "exact_gates": 208,
    "boundary": (
        "Ilyra's repository seal remains 29399 negatives, 15985 methods, 1700 failed and "
        "2533 passing witnesses; seven terminal overlay witnesses remain external and additive."
    ),
}
STARTUP_FAILURE_COUNT = 22
X1_OVERLAY = {
    "effective_negatives": ACTIVATION_OVERLAY["effective_negatives"] + STARTUP_FAILURE_COUNT,
    "methods": ACTIVATION_OVERLAY["methods"] + STARTUP_FAILURE_COUNT,
    "failed_witnesses": ACTIVATION_OVERLAY["failed_witnesses"] + STARTUP_FAILURE_COUNT,
    "passing_witnesses": ACTIVATION_OVERLAY["passing_witnesses"] + STARTUP_FAILURE_COUNT,
    "open_gaps": ACTIVATION_OVERLAY["open_gaps"],
    "exact_gates": ACTIVATION_OVERLAY["exact_gates"],
}

PRIMARY_PILLAR = "THOS Body"
PRACTICES = (
    "microscope-slide digitization calibration custodian lineage review",
    "imaging technician focus-stack exception review",
    "quality coordinator tile-correction readback and shift handover",
)
SUCCESSOR_PRACTICE_RECOMMENDATION = (
    "withheld pending the terminal live-authority reread; no successor practice is inferred in x1"
)

SOURCE_LEDGER = [
    {
        "source_id": "SRC-DICOM-WSI",
        "title": "DICOM Whole Slide Imaging",
        "url": "https://dicom.nema.org/dicom/dicomwsi/index.html",
        "status": "official DICOM explanatory page inspected 2026-08-25",
        "use": "tile, pyramid, focal-plane, local Z-context, optical-path, and coordinate vocabulary only",
        "credit_boundary": "zero medical, diagnostic, conformance, professional, or operational credit",
    },
    {
        "source_id": "SRC-DICOM-PROTOCOL",
        "title": "DICOM CID 8131 Pathology Imaging Protocol",
        "url": "https://dicom.nema.org/medical/dicom/current/output/chtml/part16/sect_cid_8131.html",
        "status": "official current DICOM PS3.16 2026b page inspected 2026-08-25",
        "use": "slide-microscopy and whole-slide-imaging protocol labels only",
        "credit_boundary": "no pathology workflow, protocol compliance, diagnosis, or clinical claim",
    },
    {
        "source_id": "SRC-OME-TIFF",
        "title": "OME-TIFF specification",
        "url": "https://ome-model.readthedocs.io/en/latest/ome-tiff/specification.html",
        "status": "official OME Data Model documentation inspected 2026-08-25",
        "use": "image-plane, dimensional-order, metadata, and pyramidal sub-resolution vocabulary only",
        "credit_boundary": "no OME-TIFF conformance, interoperability, image-quality, or production claim",
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
        "source_id": "SRC-PREMIS",
        "title": "PREMIS Preservation Metadata Maintenance Activity",
        "url": "https://www.loc.gov/standards/premis/",
        "status": "Library of Congress maintenance page; status checked 2026-08-25",
        "use": "synthetic object, event, agent-role, and rights-vacancy projection only",
        "credit_boundary": "no real collection event, right, or preservation outcome",
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
    ("synthetic microscope-slide coordinate-frame and tile-grid contract with out-of-bounds refusal", "completed", "slide-tile-contract"),
    ("synthetic calibration-slide identity, lot, target-region, and acquisition-session lineage ledger", "completed", "calibration-slide-lineage"),
    ("quarantine clock for synthetic calibration-slide use: lot status, evidence vacancy, expiry instant, and no validity inference", "completed", "calibration-quarantine-clock"),
    ("microscope objective, illumination, filter, sensor, and stage optical-path fingerprint", "completed", "slide-optical-path"),
    ("exact-rational pixel-spacing and total-matrix dimension tribunal without decimal substitution", "completed", "rational-pixel-spacing"),
    ("stage-to-slide affine transform tribunal with handedness, determinant, and condition bounds", "completed", "stage-slide-transform"),
    ("reversible tile-registration graph retaining source coordinates, inverse mappings, and overlap provenance", "completed", "tile-registration-graph"),
    ("nominal focal-plane Z-offset ledger with local-context warning and absolute-depth refusal", "completed", "z-offset-ledger"),
    ("focus-stack plane-count, Z-order, spacing, duplicate, and missing-plane tribunal", "completed", "focus-stack-tribunal"),
    ("tiled matrix row-column coverage, gap, overlap, duplicate, and sparse-region detector", "completed", "tile-coverage-detector"),
    ("synthetic channel clipping and declared dynamic-range headroom tribunal", "completed", "channel-headroom"),
    ("illumination flatness proxy map with sampled-region denominator and diagnosis abstention", "completed", "illumination-flatness-proxy"),
    ("optical channel routing ledger separating detector band, lookup transform, path identity, and display profile", "completed", "optical-channel-routing"),
    ("color-management attachment ledger for slide tiles: profile hash, declared revision, intent, and replacement edge", "completed", "color-attachment-ledger"),
    ("full-resolution plane, pyramid level, thumbnail, and access derivative distinction board", "completed", "pyramid-distinction"),
    ("reference-capture dependency graph for illumination blanks, dark frames, flat fields, calibration planes, expiry, and replacement", "completed", "reference-capture-graph"),
    ("blur, fold, debris, bubble, and stitch cue-mask provenance with diagnosis refusal", "completed", "slide-cue-mask"),
    ("focus-measure grid with declared tiles, plane candidates, metric version, and denominator", "completed", "focus-measure-grid"),
    ("synthetic stage-micrometer residual report with units, uncertainty, and no conformance promotion", "completed", "stage-micrometer-residual"),
    ("raw tile, focal stack, full-resolution plane, pyramid, and access-copy lineage graph", "completed", "slide-derivative-lineage"),
    ("per-tile digest, focal-plane Merkle root, checkpoint, and resume-integrity ledger", "completed", "tile-integrity-ledger"),
    ("tile-focus hold and correction graph with addressed patch, superseding edge, contest record, and dual readback", "completed", "focus-correction-graph"),
    ("synthetic release-hold council with two vacant reviewer slots and explicit zero-approval result", "completed", "release-hold-council"),
    ("bounded tile-focus review queue with pause budget, stop token, discrepancy echo, owner vacancy, and handover", "completed", "focus-review-queue"),
    ("keyboard-readable focus exception report: caption, header scope, textual state, linear order, and printable fallback", "completed", "accessible-focus-report"),
    ("data-minimizing pseudonymous equipment, calibration slide, session, plane, and tile identifier contract", "completed", "slide-pseudonyms"),
    ("tile-specific focus-exception neighborhood expansion with bounded radius and no blanket slide status", "completed", "focus-neighborhood"),
    ("GMUT analogy docket for synthetic slide-focus transfer terms, nuisance symbols, units, and no-observation firewall", "completed", "gmut-slide-obligations"),
    ("microscope digitization calibration custodian practice lens with zero competence inference", "represented", "custodian-practice"),
    ("imaging technician focus-stack exception review practice lens with zero professional-result credit", "represented", "focus-review-practice"),
    ("quality coordinator tile-correction readback and shift-handover practice lens with no operational authority", "represented", "quality-practice"),
    ("Freed ID zero-key equipment, session, slide, plane, tile, correction, and challenge graph", "represented", "freed-id-slide-graph"),
    ("CBR slide-data matrix for privacy, access, remedy, contestability, cultural-care, and decision-right vacancies", "represented", "cbr-slide-vacancies"),
    ("synthetic THOS workboard for tile-focus holds, bounded retries, stop tokens, readback, and handover", "represented", "thos-focus-workboard"),
    ("symbolic focus-transfer vocabulary map with explicit GMUT analogy-only and zero physical-observation credit", "represented", "gmut-analogy-map"),
    ("nonconversion ledger for heat-and-drift metaphors: no mind, agency, justice, value, or physical inference", "represented", "thermo-nonconversion"),
    ("representative real microscope-slide, scanner, objective, specimen, and interoperability evaluation", "open_gap", "external-slide-gap"),
    ("external human review vacancy for scanner practice, assistive access, language, cultural care, and affected-party judgment", "open_gap", "human-review-gap"),
    ("competent-custodian gate for synthetic slide/specimen disclosure, retention, return, cultural care, and release decisions", "exact_gate", "custodian-authority-gate"),
    ("Stage-20 promotion veto grid: slide observations, external reproduction, safety review, rights decision, and authority receipts remain non-substitutable", "exact_gate", "stage20-veto-grid"),
]

SKILL_NAMES = [
    "ghc-family-slide-coordinate-tile-contract",
    "ghc-family-slide-session-lineage",
    "ghc-family-slide-calibration-quarantine",
    "ghc-family-slide-optical-path-fingerprint",
    "ghc-family-slide-rational-pixel-spacing",
    "ghc-family-slide-affine-transform-tribunal",
    "ghc-family-slide-reversible-registration",
    "ghc-family-slide-z-offset-ledger",
    "ghc-family-slide-focus-stack-tribunal",
    "ghc-family-slide-tile-coverage-detector",
    "ghc-family-slide-dynamic-range-headroom",
    "ghc-family-slide-illumination-flatness-proxy",
    "ghc-family-slide-channel-routing",
    "ghc-family-slide-color-attachment-ledger",
    "ghc-family-slide-pyramid-distinction",
    "ghc-family-slide-reference-capture-graph",
    "ghc-family-slide-cue-mask-provenance",
    "ghc-family-slide-focus-measure-grid",
    "ghc-family-slide-lineage-graph",
    "ghc-family-slide-authority-vacancy-firewall",
]

RUNNER_NAMES = [
    "ghc_family_slide_tile_contract_runner",
    "ghc_family_slide_session_lineage_runner",
    "ghc_family_slide_optical_path_runner",
    "ghc_family_slide_registration_runner",
    "ghc_family_slide_z_plane_runner",
    "ghc_family_slide_tile_coverage_runner",
    "ghc_family_slide_color_attachment_runner",
    "ghc_family_slide_focus_measure_runner",
    "ghc_family_slide_correction_runner",
    "ghc_family_slide_authority_firewall_runner",
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
            "selection_id": f"AL6684-INHERITED-{index + 1:02d}",
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
        "slide-tile-contract": ["SRC-DICOM-WSI", "SRC-OME-TIFF"],
        "calibration-slide-lineage": ["SRC-PROV-DM", "SRC-PREMIS"],
        "calibration-quarantine-clock": ["SRC-PROV-DM"],
        "slide-optical-path": ["SRC-DICOM-WSI"],
        "rational-pixel-spacing": ["SRC-DICOM-WSI"],
        "z-offset-ledger": ["SRC-DICOM-WSI"],
        "focus-stack-tribunal": ["SRC-DICOM-WSI", "SRC-OME-TIFF"],
        "tile-coverage-detector": ["SRC-DICOM-WSI"],
        "pyramid-distinction": ["SRC-DICOM-WSI", "SRC-OME-TIFF"],
        "accessible-focus-report": ["SRC-WCAG22"],
        "slide-derivative-lineage": ["SRC-PREMIS", "SRC-PROV-DM"],
        "freed-id-slide-graph": ["SRC-PROV-DM", "SRC-PREMIS"],
        "cbr-slide-vacancies": ["SRC-PROV-DM"],
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
        proposal_id = f"AL6684-N{index:03d}"
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
                f"A bounded Auren-local {slug} control can preserve declared calibration custody, "
                "failure, and abstention states without promoting absent evidence or authority."
            ),
            "null_or_failure_condition": (
                f"The {slug} control accepts an invalid fixture, loses a retained state, rewrites "
                "source truth, or implies a protected professional, scientific, identity, or authority claim."
            ),
            "approval_class": approval,
            "execution_lane": "owner-local synthetic and structural x2 lane; external actions and real material zero",
            "official_or_primary_source_needs": source_map.get(slug, ["SRC-DICOM-WSI", "SRC-PROV-DM"]),
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
        raise ValueError("x1 must begin at the exact Ilyra final")
    if git("branch", "--show-current") != "codex/GHC-Family/auren-lark-v668-v4-full-tools":
        raise ValueError("unexpected Auren branch")
    allowed_x1_code = {
        "scripts/ghc_family_auren_lark_v668_v4_archive.py",
        "scripts/build_ghc_family_auren_lark_v668_v4_x1.py",
        "tests/test_ghc_family_auren_lark_v668_v4_x1.py",
    }
    status_lines = run_git("status", "--porcelain", "--untracked-files=all").stdout.splitlines()
    unexpected = []
    for line in status_lines:
        path = line[3:].strip().replace("\\", "/")
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        allowed_partial_x1 = (
            path.startswith("docs/auren-lark/v668-v4/x1/")
            or path.startswith("docs/auren-lark/v668-v4/method-flow/")
            or path.startswith("docs/auren-lark/v668-v4/validation/")
        )
        if path not in allowed_x1_code and not allowed_partial_x1:
            unexpected.append(line)
    if unexpected:
        raise ValueError(f"x1 builder found unexpected pre-freeze changes: {unexpected}")
    forbidden = [PHASE_ROOT / "x2", PHASE_ROOT / "evidence", PHASE_ROOT / "final", PHASE_ROOT / "closeout", PHASE_ROOT / "seal"]
    if any(path.exists() for path in forbidden):
        raise ValueError("x2 or closeout material exists before x1 freeze")
    script_names = git("ls-files", "--others", "--cached", "--", "scripts", "tests").splitlines()
    if any("auren_lark_v668_v4_x2" in name or "auren_lark_v668_v4_final" in name for name in script_names):
        raise ValueError("x2 or final implementation exists before x1 freeze")
