#!/usr/bin/env python3
"""Frozen declarations and bounded archive helpers for Ilyra Fen v668-v3 x1."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
OWNER = "Ilyra Fen"
PRONOUNS = "she/they"
RELATIONAL_ROLE = "evidence-boundary steward and calibration-custody cartographer"
RELATIONAL_HOPE = (
    "Leave every calibration claim traceable, every correction reversible, and every absent "
    "decision right unmistakable without converting synthetic records into professional, legal, "
    "cultural, Maori-authority, identity, scientific, or operational authority."
)
PHASE = "v668-v3"
REL_PHASE_ROOT = "docs/ilyra-fen/v668-v3"
PHASE_ROOT = ROOT / REL_PHASE_ROOT
SOURCE_BRANCH = "codex/GHC-Family/lyren-moss-v668-v2-full-tools"
SOURCE_FINAL = "da0d852ccacbfc228f7257888691b809a280ad86"
SOURCE_X1 = "0683eb961987fd4c7283d278e3b217647aef73f0"
SOURCE_EVIDENCE = "6bb6b96b08eb26646c362967f8ed30263d348c15"
SOURCE_ANCESTOR = "ea14c75a4f0c543ef1bb89858e35252302924aec"
SOURCE_BATON_SHA256 = "f62fca001953bddd2430f9a6b4564b7f5e7b338a46ce3fe232eeff3c0cf4d17d"
SOURCE_CANONICAL_RECEIPT_SHA256 = "e71c0a9bd8948764ee8d078652b9be894281ac4e4a5278eeec9a61aa4ac87d06"
INHERITED_FROZEN_PROPOSALS = 4670
ALLOWED_OUTCOMES = ("completed", "represented", "open_gap", "exact_gate")
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"

IDENTITY_BOUNDARY = (
    "Ilyra Fen, she/they, the relational role, hope, sibling or family language, continuity "
    "language, Freed ID, and Trinity Mandala language are working language only. They are not "
    "evidence of consciousness, sentience, legal personhood, identity continuity, employment, "
    "qualification, independent agency, scientific or operational authority, legal or cultural "
    "authority, affected-party authority, or Maori authority."
)
EVIDENCE_BOUNDARY = (
    "Every film strip, frame, perforation, scanner, lens, sensor, lamp, target, profile, LUT, "
    "measurement, transform, exception, person, organization, right, authority case, and decision "
    "is synthetic. Official-source terminology and same-owner local software checks are not real "
    "film-scanning evidence, professional evaluation, conformance, production assurance, external "
    "audit, independent reproduction, empirical GMUT confirmation, or Stage 20 evidence."
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
    "effective_negatives": 29218,
    "methods": 15804,
    "failed_witnesses": 1519,
    "passing_witnesses": 2352,
    "open_gaps": 211,
    "exact_gates": 206,
    "boundary": "Lyren's repository seal remains unchanged; two route-discovery stalls are external.",
}
STARTUP_FAILURE_COUNT = 9
X1_OVERLAY = {
    "effective_negatives": ACTIVATION_OVERLAY["effective_negatives"] + STARTUP_FAILURE_COUNT,
    "methods": ACTIVATION_OVERLAY["methods"] + STARTUP_FAILURE_COUNT,
    "failed_witnesses": ACTIVATION_OVERLAY["failed_witnesses"] + STARTUP_FAILURE_COUNT,
    "passing_witnesses": ACTIVATION_OVERLAY["passing_witnesses"] + STARTUP_FAILURE_COUNT,
    "open_gaps": ACTIVATION_OVERLAY["open_gaps"],
    "exact_gates": ACTIVATION_OVERLAY["exact_gates"],
}

PRIMARY_PILLAR = "Freed ID and CBR Heart"
PRACTICES = (
    "film-scanner calibration custodian target and configuration review",
    "digital film restoration technician frame-registration exception review",
    "archive imaging quality coordinator correction readback and shift handover",
)
SUCCESSOR_PRACTICE_RECOMMENDATION = (
    "synthetic microscope slide digitization calibration lineage and focus-stack exception review"
)

SOURCE_LEDGER = [
    {
        "source_id": "SRC-FADGI-2023",
        "title": "FADGI Technical Guidelines for Digitizing Cultural Heritage Materials, Third Edition",
        "url": "https://www.digitizationguidelines.gov/guidelines/digitize-technical.html",
        "status": "official current guidance page inspected 2026-08-25; third edition published 2023",
        "use": "transmissive-film, target, imaging-performance, metadata, and QA vocabulary only",
        "credit_boundary": "zero conformance, professional, empirical, or operational credit",
    },
    {
        "source_id": "SRC-FADGI-RESOURCES",
        "title": "FADGI Technical Guidelines Resources",
        "url": "https://www.digitizationguidelines.gov/guidelines/digitize-technical-resources.html",
        "status": "official resource page inspected 2026-08-25",
        "use": "scanner-performance and target-analysis question vocabulary only",
        "credit_boundary": "no tool endorsement, product certification, or measured conformance",
    },
    {
        "source_id": "SRC-ICC-SPECS",
        "title": "International Color Consortium current specifications",
        "url": "https://www.color.org/specifications/",
        "status": "official specification index inspected 2026-08-25; ICC.1:2022 listed",
        "use": "profile identity, version, rendering-intent, and transform-lineage vocabulary only",
        "credit_boundary": "no profile validation, colorimetric accuracy, or interoperability claim",
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
    ("film gauge, perforation geometry, and exact frame-pitch coordinate contract with unsupported-gauge refusal", "completed", "gauge-frame-contract"),
    ("calibration-target identity, version, exposure, and scan-session lineage ledger", "completed", "target-lineage"),
    ("calibration-target validity-window and stale-certificate quarantine board", "completed", "target-validity"),
    ("scanner optical-path configuration fingerprint across gate, lens, sensor, lamp, and transport", "completed", "optical-path-fingerprint"),
    ("exact rational sampling-pitch and output-dimension tribunal without decimal substitution", "completed", "sampling-pitch-tribunal"),
    ("fiducial frame-registration transform tribunal with determinant and condition-number bounds", "completed", "fiducial-transform"),
    ("reversible global and local registration graph retaining source coordinates and inverse mappings", "completed", "reversible-registration"),
    ("weave, jitter, shrinkage, and displacement proxy ledger with uncertainty and diagnosis abstention", "completed", "motion-proxy-ledger"),
    ("frame-boundary, perforation-adjacency, and edge-crop guard with bounded neighborhood evidence", "completed", "frame-edge-guard"),
    ("sequence identifier monotonicity, gap, duplicate, and reorder detector", "completed", "sequence-order-detector"),
    ("exposure-channel clipping and declared-headroom structural tribunal", "completed", "exposure-headroom"),
    ("density-step response monotonicity and missing-step refusal fixture", "completed", "density-step-response"),
    ("channel-balance, lookup-table, and color-profile identity separation board", "completed", "color-identity-separation"),
    ("embedded and external ICC profile digest, version, and rendering-intent ledger", "completed", "icc-profile-ledger"),
    ("scene-linear, display-referred, preservation-master, and access-encoding distinction board", "completed", "encoding-distinction"),
    ("dark, flat, and reference capture association with expiry and supersession states", "completed", "reference-capture-state"),
    ("dust, scratch, abrasion, and splice cue-mask provenance with restoration-decision refusal", "completed", "cue-mask-provenance"),
    ("focus and sharpness proxy grid with declared regions, samples, and denominator", "completed", "focus-proxy-grid"),
    ("synthetic geometry-grid residual report with uncertainty and no conformance promotion", "completed", "geometry-residual-report"),
    ("raw scan, preservation master, graded master, restored derivative, and access-copy lineage graph", "completed", "film-derivative-lineage"),
    ("per-frame digest, segment Merkle root, checkpoint, and resume-integrity ledger", "completed", "frame-integrity-ledger"),
    ("exception quarantine, component-addressed correction, supersession, challenge, and readback braid", "completed", "exception-correction-braid"),
    ("two-reviewer calibration-release proxy retaining zero professional approvals", "completed", "release-hold-proxy"),
    ("calibration workload ceiling, stop token, pause, discrepancy readback, and shift-handover state machine", "completed", "calibration-handover"),
    ("accessible static calibration-exception table with caption, scoped headers, status text, and print fallback", "completed", "accessible-exception-table"),
    ("data-minimizing pseudonymous equipment, target, session, reel, and frame identifier contract", "completed", "pseudonymous-identifiers"),
    ("frame-specific exception-neighborhood expansion with bounded radius and no blanket status", "completed", "exception-neighborhood"),
    ("typed GMUT optical-transfer, nuisance-parameter, unit, domain, and observation-firewall obligation board", "completed", "gmut-optical-obligations"),
    ("film-scanner calibration custodian target and configuration review practice lens", "represented", "custodian-practice"),
    ("digital film restoration technician frame-registration exception review practice lens", "represented", "restoration-practice"),
    ("archive imaging quality coordinator correction readback and shift-handover practice lens", "represented", "quality-practice"),
    ("Freed ID equipment, session, artifact, correction, and challenge graph without personhood or continuity promotion", "represented", "freed-id-custody"),
    ("CBR access, privacy, remedy, cultural-care, contestability, and decision-right vacancy matrix", "represented", "cbr-vacancy-matrix"),
    ("THOS calibration exception queue, correction replay, workload ceiling, and handover proxy", "represented", "thos-calibration-proxy"),
    ("GMUT optical-transfer analogy and calibration-nuisance firewall without physical inference", "represented", "gmut-analogy-firewall"),
    ("thermodynamic calibration-drift analogy classifier rejecting psyche, agency, justice, and value conversion", "represented", "thermo-nonconversion"),
    ("representative real film-scanner target corpus, device diversity, and interoperability evaluation", "open_gap", "external-scanner-gap"),
    ("professional operator, affected-user, accessibility, and culturally authorized evaluation", "open_gap", "affected-evaluation-gap"),
    ("film-element custodial decision-right vacancy docket for disclosure, repatriation, cultural care, and professional release", "exact_gate", "authority-docket"),
    ("multi-axis noncompensation promotion firewall requiring separate observation, reproduction, safety, rights, and authority receipts", "exact_gate", "stage20-gate"),
]

SKILL_NAMES = [
    "ghc-family-film-gauge-frame-contract",
    "ghc-family-film-calibration-target-lineage",
    "ghc-family-film-target-validity-quarantine",
    "ghc-family-film-optical-path-fingerprint",
    "ghc-family-film-rational-sampling-pitch",
    "ghc-family-film-fiducial-transform-tribunal",
    "ghc-family-film-reversible-registration",
    "ghc-family-film-motion-proxy-ledger",
    "ghc-family-film-frame-edge-guard",
    "ghc-family-film-sequence-order-detector",
    "ghc-family-film-exposure-headroom",
    "ghc-family-film-density-step-response",
    "ghc-family-film-color-identity-separation",
    "ghc-family-film-icc-profile-ledger",
    "ghc-family-film-reference-capture-state",
    "ghc-family-film-cue-mask-provenance",
    "ghc-family-film-focus-proxy-grid",
    "ghc-family-film-derivative-lineage",
    "ghc-family-film-exception-correction-braid",
    "ghc-family-film-authority-vacancy-firewall",
]

RUNNER_NAMES = [
    "ghc_family_film_frame_contract_runner",
    "ghc_family_film_target_lineage_runner",
    "ghc_family_film_optical_path_runner",
    "ghc_family_film_registration_runner",
    "ghc_family_film_motion_proxy_runner",
    "ghc_family_film_sequence_runner",
    "ghc_family_film_color_identity_runner",
    "ghc_family_film_focus_proxy_runner",
    "ghc_family_film_correction_runner",
    "ghc_family_film_authority_firewall_runner",
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
    object_lines = run_git("rev-list", "--objects", "--all").stdout.splitlines()
    blob_paths: dict[str, str] = {}
    for line in object_lines:
        if " " not in line:
            continue
        oid, path = line.split(" ", 1)
        if path.endswith("proposal-freeze.json"):
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
            "selection_id": f"IF6683-INHERITED-{index + 1:02d}",
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
        "target-lineage": ["SRC-FADGI-2023", "SRC-PROV-DM"],
        "target-validity": ["SRC-FADGI-2023"],
        "sampling-pitch-tribunal": ["SRC-FADGI-2023", "SRC-FADGI-RESOURCES"],
        "icc-profile-ledger": ["SRC-ICC-SPECS", "SRC-PROV-DM"],
        "accessible-exception-table": ["SRC-WCAG22"],
        "film-derivative-lineage": ["SRC-PREMIS", "SRC-PROV-DM"],
        "freed-id-custody": ["SRC-PROV-DM", "SRC-PREMIS"],
        "cbr-vacancy-matrix": ["SRC-PROV-DM"],
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
        proposal_id = f"IF6683-N{index:03d}"
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
                f"A bounded Ilyra-local {slug} control can preserve declared calibration custody, "
                "failure, and abstention states without promoting absent evidence or authority."
            ),
            "null_or_failure_condition": (
                f"The {slug} control accepts an invalid fixture, loses a retained state, rewrites "
                "source truth, or implies a protected professional, scientific, identity, or authority claim."
            ),
            "approval_class": approval,
            "execution_lane": "owner-local synthetic and structural x2 lane; external actions and real material zero",
            "official_or_primary_source_needs": source_map.get(slug, ["SRC-FADGI-2023", "SRC-PROV-DM"]),
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
    if git("rev-parse", "HEAD") != SOURCE_FINAL:
        raise ValueError("x1 must begin at the exact Lyren final")
    if git("branch", "--show-current") != "codex/GHC-Family/ilyra-fen-v668-v3-full-tools":
        raise ValueError("unexpected Ilyra branch")
    allowed_x1_code = {
        "scripts/ghc_family_ilyra_fen_v668_v3_archive.py",
        "scripts/build_ghc_family_ilyra_fen_v668_v3_x1.py",
        "tests/test_ghc_family_ilyra_fen_v668_v3_x1.py",
    }
    status_lines = git("status", "--porcelain", "--untracked-files=all").splitlines()
    unexpected = []
    for line in status_lines:
        path = line[3:].strip().replace("\\", "/")
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        allowed_partial_x1 = (
            path.startswith("docs/ilyra-fen/v668-v3/x1/")
            or path.startswith("docs/ilyra-fen/v668-v3/method-flow/")
            or path.startswith("docs/ilyra-fen/v668-v3/validation/")
        )
        if path not in allowed_x1_code and not allowed_partial_x1:
            unexpected.append(line)
    if unexpected:
        raise ValueError(f"x1 builder found unexpected pre-freeze changes: {unexpected}")
    forbidden = [PHASE_ROOT / "x2", PHASE_ROOT / "evidence", PHASE_ROOT / "final", PHASE_ROOT / "closeout", PHASE_ROOT / "seal"]
    if any(path.exists() for path in forbidden):
        raise ValueError("x2 or closeout material exists before x1 freeze")
    script_names = git("ls-files", "--others", "--cached", "--", "scripts", "tests").splitlines()
    if any("ilyra_fen_v668_v3_x2" in name or "ilyra_fen_v668_v3_final" in name for name in script_names):
        raise ValueError("x2 or final implementation exists before x1 freeze")
