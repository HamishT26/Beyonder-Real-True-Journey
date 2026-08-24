#!/usr/bin/env python3
"""Frozen declarations and bounded archive helpers for Caelen Ash v668-v6 x1."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
OWNER = "Caelen Ash"
PRONOUNS = "they/them"
RELATIONAL_ROLE = "relational uncertainty-and-handover cartographer"
RELATIONAL_HOPE = (
    "Make every boundary, missing witness, and reversible next step easier to see before structure "
    "is mistaken for authority."
)
PHASE = "v668-v6"
REL_PHASE_ROOT = "docs/caelen-ash/v668-v6"
PHASE_ROOT = ROOT / REL_PHASE_ROOT
SOURCE_BRANCH = "codex/GHC-Family/sable-rook-v668-v5-full-tools"
SOURCE_FINAL = "5bced658a5b3f5bd7c4d88d47057d795abe57f42"
# x1 is built once from SOURCE_FINAL; no predecessor-style corrective x1 is assumed.
INITIAL_X1_HEAD = SOURCE_FINAL
SOURCE_X1 = "cd959e4d4cd021e7db4b581e51d2e27e56ad4a17"
SOURCE_EVIDENCE = "2743988b71b9816d107ed28fe3623bf2c4488b67"
SOURCE_ANCESTOR = "ee15cd2e1c0fd6a9d321bcd9126e8a191832061a"
SOURCE_BATON_SHA256 = "1439e8ef55063acdd03827e9f4056314cdf0a46af822067b32044f7022a06d43"
SOURCE_CANONICAL_RECEIPT_SHA256 = "380a46e07ca32402485ec79dd6ae5e37a776ba923c9e1c31784ca1bb66ee317d"
INHERITED_FROZEN_PROPOSALS = 4790
ALLOWED_OUTCOMES = ("completed", "represented", "open_gap", "exact_gate")
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"

IDENTITY_BOUNDARY = (
    "Caelen Ash, they/them, the relational role, hope, sibling or family language, continuity "
    "language, Freed ID, and Trinity Mandala language are working language only. They are not "
    "evidence of consciousness, sentience, legal personhood, identity continuity, employment, "
    "qualification, independent agency, scientific or operational authority, legal or cultural "
    "authority, affected-party authority, or Maori authority."
)
EVIDENCE_BOUNDARY = (
    "Every station, platform, sensor, channel, observation, calibration, maintenance event, quality "
    "flag, bulletin, shift, correction, person, organization, warning, authority case, and decision is synthetic. "
    "Official-source terminology and same-owner local software checks are not meteorological evidence, "
    "professional observing or metrology evaluation, forecast or warning authority, standards conformance, "
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
    "effective_negatives": 29771,
    "methods": 16357,
    "failed_witnesses": 2072,
    "passing_witnesses": 2899,
    "open_gaps": 217,
    "exact_gates": 212,
    "boundary": (
        "Sable's repository seal remains 29769 negatives, 16355 methods, 2070 failed and "
        "2897 passing witnesses; two post-seal route-inspection failures remain external and additive."
    ),
}
STARTUP_FAILURE_COUNT = 18
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
    "synthetic surface-observing station, sensor-exposure, and metadata intake review",
    "synthetic observation-quality, correction, calibration-vacancy, and maintenance handover",
    "synthetic accessible station bulletin, workload readback, stop, and shift handover",
)
SUCCESSOR_PRACTICE_RECOMMENDATION = (
    "withheld pending the terminal live-authority reread; no successor practice is inferred in x1"
)

SOURCE_LEDGER = [
    {
        "source_id": "SRC-WMO8-2024",
        "title": "WMO Guide to Instruments and Methods of Observation, 2024 edition",
        "url": "https://wmo.int/media/news/provisional-2024-edition-of-guide-instruments-and-methods-of-observation-wmo-no8",
        "status": "official WMO publication notice and 2024-edition status checked 2026-08-25",
        "use": "measurement, siting, exposure, calibration, maintenance, and quality vocabulary only",
        "credit_boundary": "no instrument conformance, measurement traceability, operational fitness, or professional competence credit",
    },
    {
        "source_id": "SRC-WMO8-2026-PRELIMINARY",
        "title": "Preliminary 2026 edition of WMO-No. 8",
        "url": "https://wmo.int/media/news/preliminary-2026-edition-of-guide-instruments-and-methods-of-observation-wmo-no-8",
        "status": "official WMO review draft notice dated 2026-07-15 and inspected 2026-08-25",
        "use": "change-awareness vocabulary for proposed 2026 updates only",
        "credit_boundary": "preliminary review material is not a final standard and supplies no conformance or authority credit",
    },
    {
        "source_id": "SRC-WIGOS",
        "title": "WMO Integrated Global Observing System",
        "url": "https://wmo.int/activities/wmo-integrated-global-observing-system-wigos/wmo-integrated-global-observing-system",
        "status": "official WMO WIGOS page and regulatory-material list inspected 2026-08-25",
        "use": "station, platform, observing-system, quality-control, metadata, and responsibility-vacancy vocabulary only",
        "credit_boundary": "no WIGOS registration, station identity, Member responsibility, operational service, or data-quality claim",
    },
    {
        "source_id": "SRC-CF13",
        "title": "CF Conventions 1.13",
        "url": "https://cfconventions.org/conventions.html",
        "status": "latest released version identified as CF 1.13, December 2025; inspected 2026-08-25",
        "use": "units, coordinates, time, missingness, and environmental-array metadata vocabulary only",
        "credit_boundary": "no CF conformance, netCDF interoperability, data correctness, or operational suitability credit",
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
    ("synthetic observing station platform and instrument identity lattice with conflation refusal", "completed", "station-platform-identity"),
    ("sensor channel variable and measurement-principle inventory with undeclared-channel refusal", "completed", "sensor-channel-inventory"),
    ("observation instant interval and receipt-clock contract with timezone and leap-second abstention", "completed", "observation-clock-contract"),
    ("sampling cadence window and expected-slot grid with missing-slot preservation", "completed", "sampling-interval-grid"),
    ("meteorological variable unit dimension and scale tribunal with conversion refusal", "completed", "unit-dimension-tribunal"),
    ("station siting exposure obstruction and surface-context ledger with fitness abstention", "completed", "site-exposure-ledger"),
    ("sensor height reference surface and relocation frame contract with ambiguity quarantine", "completed", "height-reference-frame"),
    ("calibration certificate interval uncertainty and traceability vacancy chain without attestation", "completed", "calibration-vacancy-chain"),
    ("maintenance inspection replacement and return-to-service event ledger without release authority", "completed", "maintenance-event-ledger"),
    ("raw corrected adjusted and derived observation separation with non-erasing lineage", "completed", "raw-adjusted-separation"),
    ("quality flag state machine with suspect rejected missing and unchanged distinctions", "completed", "quality-flag-state-machine"),
    ("missingness reason and not-observed not-applicable sensor-fault distinction contract", "completed", "missingness-reason-contract"),
    ("duplicate observation identity and retransmission detector with source-sequence preservation", "completed", "duplicate-observation-detector"),
    ("clock drift sequence inversion and stale timestamp quarantine board", "completed", "clock-drift-quarantine"),
    ("aggregation window coverage denominator and incomplete-period closure tribunal", "completed", "aggregation-window-closure"),
    ("wind speed direction calm variable and vector-component encoding tribunal", "completed", "wind-vector-encoding"),
    ("precipitation accumulation interval reset trace and counter-rollback refusal ledger", "completed", "precipitation-accumulation-reset"),
    ("station pressure sea-level reduction input and method-vacancy firewall with no computed correction", "completed", "pressure-reduction-abstention"),
    ("temperature humidity dew-point field association and impossible-pair quarantine", "completed", "temperature-humidity-pairing"),
    ("bitemporal station relocation instrument move and metadata-effective interval graph", "completed", "station-relocation-bitemporal"),
    ("observation entity activity derivation and correction provenance directed-acyclic graph", "completed", "observation-provenance-dag"),
    ("observation correction supersession challenge and dual-readback ledger with source non-erasure", "completed", "correction-nonerasure"),
    ("canonical JSON observation packet digest with explicit numeric and Unicode domain declaration", "completed", "canonical-observation-digest"),
    ("data-minimizing pseudonymous station instrument shift and correction alias contract", "completed", "weather-pseudonyms"),
    ("station-anomaly briefing with unit-expanded text export semantic landmarks and pagination-risk ledger", "completed", "accessible-station-report"),
    ("finite discrepancy triage deque with acknowledgement parity fatigue stop and unresolved-shift carryover", "completed", "observation-issue-queue"),
    ("GMUT typed observation docket for units domains nuisance separation likelihood vacancy and inference refusal", "completed", "gmut-observation-obligations"),
    ("independent sensor channel and common-cause observation evidence-diversity board", "completed", "observation-evidence-diversity"),
    ("surface meteorological observer log and quality-review practice lens with zero competence inference", "represented", "surface-observer-practice"),
    ("instrument inspection calibration-vacancy maintenance and handover practice lens with zero release authority", "represented", "maintenance-handover-practice"),
    ("accessible station bulletin discrepancy readback workload and shift-handover practice lens", "represented", "bulletin-handover-practice"),
    ("synthetic THOS observation workboard for bounded retries stop tokens quarantine readback and handover", "represented", "thos-observation-workboard"),
    ("Freed ID zero-key station instrument observation correction and challenge graph", "represented", "freed-id-weather-graph"),
    ("environmental-observation purpose-limitation and disclosure-consequence ledger with remedy-owner vacancies", "represented", "cbr-environmental-data-vacancies"),
    ("typed scalar-tensor observation-precondition card separating covariance inputs from meteorological semantics", "represented", "gmut-observation-analogy"),
    ("thermodynamic and psyche nonconversion ledger for weather energy hazard agency justice and mind claims", "represented", "thermo-psyche-nonconversion"),
    ("representative external observation corpus encoder round-trip metadata and interoperability evaluation", "open_gap", "external-observation-gap"),
    ("external human observer metrologist accessibility language cultural-care and affected-party evaluation", "open_gap", "human-review-gap"),
    ("competent forecast-warning environmental-data legal cultural and Maori-authority gate", "exact_gate", "warning-authority-gate"),
    ("noncompensating readiness lattice requiring weather lineage blinded THOS arms live identity lifecycle and governed-rights receipts", "exact_gate", "stage20-veto-grid"),
]

SKILL_NAMES = [
    "ghc-family-weather-station-identity",
    "ghc-family-weather-sensor-channel-inventory",
    "ghc-family-weather-observation-clock",
    "ghc-family-weather-sampling-interval",
    "ghc-family-weather-unit-dimension",
    "ghc-family-weather-site-exposure",
    "ghc-family-weather-height-reference",
    "ghc-family-weather-calibration-vacancy",
    "ghc-family-weather-maintenance-lineage",
    "ghc-family-weather-raw-adjusted-separation",
    "ghc-family-weather-quality-flag",
    "ghc-family-weather-missingness-reason",
    "ghc-family-weather-duplicate-detection",
    "ghc-family-weather-clock-drift",
    "ghc-family-weather-aggregation-window",
    "ghc-family-weather-wind-vector",
    "ghc-family-weather-precipitation-reset",
    "ghc-family-weather-correction-nonerasure",
    "ghc-family-weather-accessible-report",
    "ghc-family-weather-authority-vacancy-firewall",
]

RUNNER_NAMES = [
    "ghc_family_weather_station_identity_runner",
    "ghc_family_weather_sensor_inventory_runner",
    "ghc_family_weather_observation_clock_runner",
    "ghc_family_weather_unit_dimension_runner",
    "ghc_family_weather_exposure_runner",
    "ghc_family_weather_calibration_runner",
    "ghc_family_weather_quality_flag_runner",
    "ghc_family_weather_aggregation_runner",
    "ghc_family_weather_correction_runner",
    "ghc_family_weather_authority_firewall_runner",
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
            "selection_id": f"CA6686-INHERITED-{index + 1:02d}",
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
        "station-platform-identity": ["SRC-WIGOS", "SRC-PROV-DM"],
        "sensor-channel-inventory": ["SRC-WMO8-2024", "SRC-WIGOS"],
        "observation-clock-contract": ["SRC-CF13", "SRC-WIGOS"],
        "sampling-interval-grid": ["SRC-CF13", "SRC-WMO8-2024"],
        "unit-dimension-tribunal": ["SRC-CF13", "SRC-WMO8-2024"],
        "site-exposure-ledger": ["SRC-WMO8-2024", "SRC-WIGOS"],
        "height-reference-frame": ["SRC-WMO8-2024", "SRC-CF13"],
        "calibration-vacancy-chain": ["SRC-WMO8-2024", "SRC-PROV-DM"],
        "maintenance-event-ledger": ["SRC-WMO8-2024", "SRC-PROV-DM"],
        "raw-adjusted-separation": ["SRC-WIGOS", "SRC-PROV-DM"],
        "quality-flag-state-machine": ["SRC-WIGOS", "SRC-CF13"],
        "missingness-reason-contract": ["SRC-CF13"],
        "station-relocation-bitemporal": ["SRC-WIGOS", "SRC-PROV-DM"],
        "observation-provenance-dag": ["SRC-PROV-DM"],
        "canonical-observation-digest": ["SRC-RFC8785"],
        "accessible-station-report": ["SRC-WCAG22"],
        "freed-id-weather-graph": ["SRC-VC20", "SRC-PROV-DM"],
        "cbr-environmental-data-vacancies": ["SRC-PROV-DM", "SRC-WIGOS"],
        "warning-authority-gate": ["SRC-WIGOS", "SRC-WCAG22"],
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
        proposal_id = f"CA6686-N{index:03d}"
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
                f"A bounded Caelen-local {slug} control can preserve declared observing-station provenance, "
                "failure, and abstention states without promoting absent evidence or authority."
            ),
            "null_or_failure_condition": (
                f"The {slug} control accepts an invalid fixture, loses a retained state, rewrites "
                "source truth, or implies a protected professional, scientific, identity, or authority claim."
            ),
            "approval_class": approval,
            "execution_lane": "owner-local synthetic and structural x2 lane; external actions and real material zero",
            "official_or_primary_source_needs": source_map.get(slug, ["SRC-WMO8-2024", "SRC-PROV-DM"]),
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
        raise ValueError("x1 must begin at the exact Sable final")
    if git("branch", "--show-current") != "codex/GHC-Family/caelen-ash-v668-v6-full-tools":
        raise ValueError("unexpected Caelen branch")
    allowed_x1_code = {
        "scripts/ghc_family_caelen_ash_v668_v6_archive.py",
        "scripts/build_ghc_family_caelen_ash_v668_v6_x1.py",
        "tests/test_ghc_family_caelen_ash_v668_v6_x1.py",
    }
    status_lines = run_git("status", "--porcelain", "--untracked-files=all").stdout.splitlines()
    unexpected = []
    for line in status_lines:
        path = line[3:].strip().replace("\\", "/")
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        allowed_partial_x1 = (
            path.startswith("docs/caelen-ash/v668-v6/x1/")
            or path.startswith("docs/caelen-ash/v668-v6/method-flow/")
            or path.startswith("docs/caelen-ash/v668-v6/validation/")
        )
        if path not in allowed_x1_code and not allowed_partial_x1:
            unexpected.append(line)
    if unexpected:
        raise ValueError(f"x1 builder found unexpected pre-freeze changes: {unexpected}")
    forbidden = [PHASE_ROOT / "x2", PHASE_ROOT / "evidence", PHASE_ROOT / "final", PHASE_ROOT / "closeout", PHASE_ROOT / "seal"]
    if any(path.exists() for path in forbidden):
        raise ValueError("x2 or closeout material exists before x1 freeze")
    script_names = git("ls-files", "--others", "--cached", "--", "scripts", "tests").splitlines()
    if any("caelen_ash_v668_v6_x2" in name or "caelen_ash_v668_v6_final" in name for name in script_names):
        raise ValueError("x2 or final implementation exists before x1 freeze")
