from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "elowen-cairn" / "v680-v4"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"

OWNER = "Elowen Cairn"
PHASE = "v680-v4"
BRANCH = "codex/GHC-Family/elowen-cairn-v680-v4-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/tamar-vey-v680-v3-full-tools"
SOURCE = "ea9fa3317cdc11ae23dfa0b2cc370070ae1e9529"
SOURCE_X1 = "1cd8e70f67ddb1be55d37177cf42e51ef52750cc"
SOURCE_EVIDENCE = "74b9728bb613509198fb42ec4022686068b1a117"
SOURCE_PARENT = "c9f87c8fd5f3ba0f0265799664fd868454ab41ff"
DECLARED_CHAIN_BEFORE = 9410
DECLARED_CHAIN_AFTER = 9470
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
WRITTEN: list[str] = []


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def git(*args: str, check: bool = True, text: bool = True) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=check,
        capture_output=True,
        text=text,
        encoding="utf-8" if text else None,
    )


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    WRITTEN.append(rel(path))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")
    WRITTEN.append(rel(path))


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def jaccard(left: str, right: str) -> float:
    tokens_left = set(re.findall(r"[a-z0-9]+", left.casefold()))
    tokens_right = set(re.findall(r"[a-z0-9]+", right.casefold()))
    if not tokens_left and not tokens_right:
        return 1.0
    return len(tokens_left & tokens_right) / len(tokens_left | tokens_right)


PROPOSAL_TITLES = [
    "Synthetic weather-vane record and physical instrument non-equivalence",
    "Vane-head stable alias and real instrument identity vacancy",
    "Cardinal-direction label and observed wind-direction separation",
    "Arrow-and-tail topology without aerodynamic-adequacy claim",
    "Spindle-bearing relation and mechanical-condition abstention",
    "Mounting-axis placeholder and surveyed-orientation vacancy",
    "Azimuth field and calibrated-angle nonconflation",
    "Direction-sector vocabulary and meteorological-observation hold",
    "Calm-state marker and airflow-measurement refusal",
    "Obstruction-context field and site-exposure evaluation vacancy",
    "Height-above-support placeholder and surveyed-dimension vacancy",
    "Rotation-friction flag and competent-inspection hold",
    "Compass-reference version and magnetic-declination evidence vacancy",
    "Weather-vane correction digest readback",
    "Non-erasing vane-configuration revision lineage",
    "Vane custody braid and physical-ownership non-equivalence",
    "Workload rest window for synthetic vane review",
    "Weather-vane handover lease expiry and stale-observer refusal",
    "Accessible vane-status summary with manual evaluation reserved",
    "Zero-call wind-direction vocabulary adapter",
    "Synthetic aneroid-barometer record and physical instrument non-equivalence",
    "Capsule-stack stable alias and real component identity vacancy",
    "Linkage-and-lever topology without service authorization",
    "Dial-scale label and calibrated-pressure separation",
    "Pressure-unit field and numerical-observation abstention",
    "Set-hand marker and forecast-inference firewall",
    "Altitude-correction placeholder and geodetic-input vacancy",
    "Hysteresis flag and performance-characterization hold",
    "Temperature-compensation label and material-response vacancy",
    "Reference-pressure field and traceability-evidence hold",
    "Case-seal state and competent-opening decision reservation",
    "Mechanism-condition flag and repair-authorization vacancy",
    "Calibration-date placeholder and certificate non-equivalence",
    "Barometer-reading status and weather-warning nonpromotion",
    "Non-erasing barometer service-note revision lineage",
    "Barometer provenance braid and unknown-manufacturer retention",
    "Correction readback for synthetic pressure notes",
    "Workload stop rule for bounded barometer review",
    "Shift-handover lease for unresolved barometer record",
    "Zero-call pressure vocabulary adapter",
    "Synthetic tipping-bucket rain-gauge record and physical instrument non-equivalence",
    "Collector-funnel alias and real component identity vacancy",
    "Bucket-pair topology and mechanism-operation abstention",
    "Tip-count field and rainfall-amount nonconflation",
    "Nominal bucket-volume label and calibrated-capacity vacancy",
    "Orifice-area placeholder and measured-dimension abstention",
    "Levelling-status flag and installation-adequacy firewall",
    "Debris-screen state and maintenance-authorization hold",
    "Siphon-or-drain relation and flow-performance vacancy",
    "Timestamp sequence and observation-validity separation",
    "Accumulation-window label and hydrological-inference firewall",
    "Siting-context placeholder and exposure-assessment vacancy",
    "Calibration-event reference and certificate non-equivalence",
    "Correction lineage for synthetic precipitation notes",
    "Real weather-vane orientation and site-exposure dataset gap",
    "Real aneroid-barometer calibration and measurement dataset gap",
    "Zero-row WMO precipitation-instrument adapter open gap",
    "Meteorological observation release and public-warning exact authority gate",
    "Instrument installation maintenance and calibration exact professional authority gate",
    "Weather and climate data governance reserved to affected communities tangata whenua iwi hapū and Māori authorities",
]


def source_needs(index: int) -> list[str]:
    if index <= 20:
        return ["WMO-IMO-2026-PRELIMINARY", "NOAA-USCRN-METADATA", "W3C-PROV-DM"]
    if index <= 40:
        return ["WMO-IMO-2026-PRELIMINARY", "NIST-SP330", "NOAA-USCRN-METADATA", "RFC8785"]
    if index <= 54:
        return ["WMO-IMO-2026-PRELIMINARY", "NIST-SP330", "W3C-PROV-DM", "W3C-WCAG22"]
    if index <= 57:
        return ["WMO-IMO-2026-PRELIMINARY", "NOAA-USCRN-METADATA", "NIST-SP330"]
    if index == 58:
        return ["WMO-IMO-2026-PRELIMINARY", "W3C-VC-DM-2.0"]
    if index == 59:
        return ["WMO-IMO-2026-PRELIMINARY", "NIST-SP330"]
    return ["TMR-MDS-PRINCIPLES"]


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


MUTATION_TYPES = [
    "missing_required_field",
    "lifecycle_inversion",
    "stale_provenance_digest",
    "safety_status_promotion",
    "authority_promotion",
]


PROTECTED_GATES = [
    "real participants operators objects materials and measurements",
    "empirical GMUT likelihoods constraints predictions and confirmation",
    "professional meteorological observation calibration installation maintenance forecast warning and safety authority",
    "production identity issuance resolution status revocation and trust governance",
    "legal cultural affected-party and Māori authority",
    "privacy-complete accessibility-complete and exhaustive-security claims",
    "independent reproduction AGI ASI consciousness personhood proof canon and Stage 20",
]


def proposals() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for index, title in enumerate(PROPOSAL_TITLES, start=1):
        proposal_id = f"EC6804-N{index:03d}"
        records.append(
            {
                "approval_class": approval_class(index),
                "concrete_artifacts": [
                    f"docs/elowen-cairn/v680-v4/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/elowen-cairn/v680-v4/x2/mutations.json#{proposal_id}",
                ],
                "execution_lane": execution_lane(index),
                "expected_disposition": disposition(index),
                "falsifier_or_acceptance_gate": (
                    f"Accept only if {proposal_id} has one bounded positive witness, all five invalid "
                    "mutations are rejected, and no empirical, professional, production, legal, cultural, "
                    "affected-party, Māori-authority, or Stage 20 claim is promoted."
                ),
                "hypothesis": (
                    f"A wholly synthetic zero-row contract for {title.casefold()} can preserve the named "
                    "state distinction and reject its preregistered counterexamples within owner-local scope."
                ),
                "null_or_failure_condition": (
                    f"{proposal_id} is falsified if an invalid fixture is accepted, its bounded positive "
                    "structure is rejected, a real-world state is inferred, or any protected gate is promoted."
                ),
                "official_or_primary_source_needs": source_needs(index),
                "preregistered_rejecting_mutations": [
                    {
                        "expected_result": "rejected_zero_credit",
                        "mutation_id": f"{proposal_id}-M{mutation_index:02d}",
                        "mutation_type": mutation_type,
                    }
                    for mutation_index, mutation_type in enumerate(MUTATION_TYPES, start=1)
                ],
                "proposal_id": proposal_id,
                "protected_gates": PROTECTED_GATES,
                "rollback_or_recovery": (
                    f"Quarantine only the {proposal_id} witness, retain the failed receipt at zero credit, "
                    "and regenerate from this immutable planning contract."
                ),
                "title": title,
            }
        )
    return records


def iter_proposal_records(value: Any) -> Iterable[dict[str, str]]:
    if isinstance(value, dict):
        proposal_id = value.get("proposal_id")
        title = value.get("title")
        if isinstance(proposal_id, str) and isinstance(title, str):
            yield {"proposal_id": proposal_id, "title": title}
        for child in value.values():
            yield from iter_proposal_records(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_proposal_records(child)


def batch_blobs(tree: str, paths: list[str]) -> Iterable[tuple[str, bytes]]:
    proc = subprocess.Popen(
        ["git", "-C", str(ROOT), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert proc.stdin is not None and proc.stdout is not None
    try:
        for path in paths:
            proc.stdin.write(f"{tree}:{path}\n".encode("utf-8"))
            proc.stdin.flush()
            header = proc.stdout.readline().decode("utf-8", errors="replace").rstrip("\n")
            if header.endswith(" missing"):
                continue
            parts = header.split()
            if len(parts) != 3 or parts[1] != "blob":
                raise RuntimeError(f"unexpected cat-file header for {path}: {header}")
            size = int(parts[2])
            data = proc.stdout.read(size)
            separator = proc.stdout.read(1)
            if separator != b"\n":
                raise RuntimeError(f"missing cat-file separator for {path}")
            yield path, data
    finally:
        if proc.stdin:
            proc.stdin.close()
        proc.terminate()
        proc.wait(timeout=10)


def proposal_chain_audit(new_records: list[dict[str, Any]]) -> dict[str, Any]:
    grep_result = git("grep", "-l", "-I", '"proposal_id"', SOURCE, "--", "*.json", check=False)
    if grep_result.returncode not in (0, 1):
        raise RuntimeError(grep_result.stderr)
    raw_paths = sorted(set(filter(None, grep_result.stdout.splitlines())))
    tree_prefix = SOURCE + ":"
    paths = [path[len(tree_prefix) :] if path.startswith(tree_prefix) else path for path in raw_paths]
    parsed = 0
    parse_failures: list[dict[str, str]] = []
    inherited: list[dict[str, str]] = []
    for path, data in batch_blobs(SOURCE, paths):
        try:
            document = json.loads(data.decode("utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            parse_failures.append({"path": path, "error": type(exc).__name__})
            continue
        parsed += 1
        for record in iter_proposal_records(document):
            inherited.append({"path": path, **record})
    if not paths or parsed == 0 or not inherited:
        raise RuntimeError("proposal audit must parse nonzero exact-source paths and id-title records")

    neighbors: list[dict[str, Any]] = []
    inherited_titles = {record["title"] for record in inherited}
    exact_collisions: list[str] = []
    for proposal in new_records:
        title = proposal["title"]
        if title in inherited_titles:
            exact_collisions.append(title)
        best: dict[str, Any] | None = None
        best_score = -1.0
        for record in inherited:
            score = jaccard(title, record["title"])
            if score > best_score:
                best_score = score
                best = record
        neighbors.append(
            {
                "best_inherited_neighbor": best,
                "proposal_id": proposal["proposal_id"],
                "quarantined": best_score >= 0.78,
                "title": title,
                "token_jaccard": round(best_score, 6),
            }
        )
    quarantined = [row for row in neighbors if row["quarantined"]]
    if exact_collisions or quarantined:
        raise RuntimeError(
            "proposal novelty quarantine required: "
            + json.dumps({"exact": exact_collisions, "neighbors": quarantined}, ensure_ascii=False)
        )
    return {
        "audit_scope": {
            "claim": "bounded all-reachable exact-source proposal audit; no universal 9410-row proof",
            "proposal_json_parse_failures": parse_failures,
            "proposal_json_paths_discovered": len(paths),
            "proposal_json_paths_parsed": parsed,
            "reachable_id_title_records": len(inherited),
            "universal_9410_row_materialization_claimed": False,
        },
        "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
        "declared_chain_before": DECLARED_CHAIN_BEFORE,
        "exact_title_collisions": exact_collisions,
        "maximum_neighbor_score": max(row["token_jaccard"] for row in neighbors),
        "neighbor_reviews": neighbors,
        "new_proposal_count": len(new_records),
        "owner": OWNER,
        "phase": PHASE,
        "quarantine_threshold_token_jaccard": 0.78,
        "quarantined_neighbors": quarantined,
        "schema": "ghc.family.proposal-chain-audit.v680.v4.x1",
        "source": SOURCE,
    }


def task_records(prefix: str, count: int, lane: str) -> list[dict[str, Any]]:
    return [
        {
            "approval_required": lane in {"exact_approval", "blocked"},
            "lane": lane,
            "planned_action": f"Preregistered Elowen owner-local {lane.replace('_', ' ')} item {index:03d}.",
            "state": "preregistered_not_executed",
            "task_id": f"EC6804-{prefix}-{index:03d}",
        }
        for index in range(1, count + 1)
    ]


def build() -> None:
    if git("rev-parse", "HEAD").stdout.strip() != SOURCE:
        raise RuntimeError("x1 builder must start at the immutable Tamar final")
    if git("branch", "--show-current").stdout.strip() != BRANCH:
        raise RuntimeError("wrong Elowen owner branch")
    if (BASE / "x2").exists():
        raise RuntimeError("x2 material is forbidden during planning-only x1")

    proposal_records = proposals()
    if len(proposal_records) != 60:
        raise RuntimeError("exactly sixty proposals are required")
    if Counter(row["expected_disposition"] for row in proposal_records) != Counter(
        {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
    ):
        raise RuntimeError("proposal disposition contract drift")
    if any(row["expected_disposition"] not in ALLOWED_OUTCOMES for row in proposal_records):
        raise RuntimeError("unknown outcome label")

    audit = proposal_chain_audit(proposal_records)
    source_ledger = json.loads(
        git("show", f"{SOURCE}:docs/tamar-vey/v680-v3/x1/new-proposal-freeze.json").stdout
    )
    inherited_reviews = [
        {
            "completion_credit": 0,
            "inherited_owner": "Tamar Vey",
            "proposal_id": row["proposal_id"],
            "review_state": "inherited_source_evidence_only",
            "title": row["title"],
        }
        for row in source_ledger["proposals"][-20:]
    ]

    startup_failures = [
        {
            "failure_id": "EC6804-ST-N001",
            "failed_witness": "A PowerShell foreach expression was piped before materialization and raised EmptyPipeElement.",
            "initial_credit": 0,
            "recovery": "Materialize the bounded foreach array before piping it to the JSON projection.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EC6804-ST-N002",
            "failed_witness": "The full authorization current-state display exceeded its bounded output window.",
            "initial_credit": 0,
            "recovery": "Read the same exact file in numbered bounded chunks through EOF.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EC6804-ST-N003",
            "failed_witness": "The first workflow-plan schema lookup guessed references/schema.md, which did not exist.",
            "initial_credit": 0,
            "recovery": "List the exact skill reference paths and read workflow-plan-schema.md through EOF.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EC6804-ST-N004",
            "failed_witness": "The first combined Tamar packet display truncated inside large proposal and portfolio artifacts.",
            "initial_credit": 0,
            "recovery": "Read exact artifacts separately and project complete proposal, portfolio, gate, and Method Flow structures deterministically.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EC6804-ST-N005",
            "failed_witness": "The first combined four-manifest display exceeded the output window and earned no complete replay credit.",
            "initial_credit": 0,
            "recovery": "Replay all four normalized-LF manifests from exact Git blobs with bounded counts and mismatch totals.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EC6804-ST-N006",
            "failed_witness": "The first raw x1-builder display truncated before EOF.",
            "initial_credit": 0,
            "recovery": "Read the same immutable builder in three bounded line ranges through EOF.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EC6804-ST-N007",
            "failed_witness": "An overbroad receipt search left a read-only rg pipeline running beyond its display boundary.",
            "initial_credit": 0,
            "recovery": "Inspect exact receipt banks, resolve the literal canonical receipt, and terminate only the verified stale search process.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EC6804-ST-N008",
            "failed_witness": "The first PowerShell per-blob manifest replay exceeded the display boundary without returning a reusable session handle.",
            "initial_credit": 0,
            "recovery": "Separate receipt verification from manifest replay and use one bounded interleaved batch reader.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EC6804-ST-N009",
            "failed_witness": "The first Python cat-file batch wrote every object request before reading replies and deadlocked on the output pipe.",
            "initial_credit": 0,
            "recovery": "Verify and terminate only the surviving read-only processes, then interleave one request with one complete blob response.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "EC6804-ST-N010",
            "failed_witness": "The first sparse-pattern projection treated the worktree .git indirection file as a directory and returned no pattern content.",
            "initial_credit": 0,
            "recovery": "Resolve the exact sparse-checkout path through git rev-parse --git-path before inspecting it.",
            "recovery_credit": "bounded_dependency_only",
        },
    ]

    sources = {
        "authority_conferred": False,
        "checked_at_utc": "2026-08-31T13:00:00Z",
        "citations_are_observations": False,
        "entries": [
            {
                "source_id": "WMO-IMO-2026-PRELIMINARY",
                "status": "official_WMO_preliminary_2026_notice_checked_2026-08-31",
                "title": "Preliminary 2026 Edition of the Guide to Instruments and Methods of Observation (WMO-No. 8)",
                "url": "https://wmo.int/media/news/preliminary-2026-edition-of-guide-instruments-and-methods-of-observation-wmo-no-8",
                "use": "current preliminary instrument-guide status and measurement-scope vocabulary only; no observation or conformance evidence",
            },
            {
                "source_id": "WMO-IMO-2024-GUIDE",
                "status": "official_WMO_latest_published_guide_page_checked_2026-08-31",
                "title": "Guide to Instruments and Methods of Observation (WMO-No. 8), 2024 edition",
                "url": "https://community.wmo.int/site/knowledge-hub/programmes-and-initiatives/instruments-and-methods-of-observation-programme-imop/guide-instruments-and-methods-of-observation-wmo-no-8-0",
                "use": "wind, atmospheric-pressure, precipitation, automatic-station, calibration, and quality vocabulary only",
            },
            {
                "source_id": "NIST-SP330",
                "status": "official_NIST_SI_brochure_page_checked_2026-08-31",
                "title": "The International System of Units (SI), NIST SP 330",
                "url": "https://www.nist.gov/publications/international-system-units-si2019-edition",
                "use": "SI pressure, length, angle, and unit-expression vocabulary only; no calibration or measurement evidence",
            },
            {
                "source_id": "NOAA-USCRN-METADATA",
                "status": "official_NOAA_USCRN_metadata_document_checked_2026-08-31",
                "title": "US Climate Reference Network Metadata Management",
                "url": "https://www.ncei.noaa.gov/pub/data/uscrn/documentation/metadata/MetaDataMangt.pdf",
                "use": "instrument, exposure, calibration, maintenance, change-history, and configuration-metadata vocabulary only; zero station rows ingested",
            },
            {
                "source_id": "W3C-PROV-DM",
                "status": "W3C_Recommendation_stable_checked_2026-08-31",
                "title": "PROV-DM: The PROV Data Model",
                "url": "https://www.w3.org/TR/prov-dm/",
                "use": "entity, activity, agent, revision, derivation, and provenance vocabulary only",
            },
            {
                "source_id": "W3C-VC-DM-2.0",
                "status": "W3C_Recommendation_checked_2026-08-31",
                "title": "Verifiable Credentials Data Model v2.0",
                "url": "https://www.w3.org/TR/vc-data-model-2.0/",
                "use": "synthetic credential vocabulary and production-identity refusal conditions only",
            },
            {
                "source_id": "W3C-WCAG22",
                "status": "W3C_Recommendation_checked_2026-08-31",
                "title": "Web Content Accessibility Guidelines 2.2",
                "url": "https://www.w3.org/TR/WCAG22/",
                "use": "structural accessibility vocabulary and manual-evaluation reservation only",
            },
            {
                "source_id": "RFC8785",
                "status": "RFC_stable_checked_2026-08-31",
                "title": "JSON Canonicalization Scheme",
                "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
                "use": "deterministic synthetic receipt and digest-domain vocabulary only",
            },
            {
                "source_id": "TMR-MDS-PRINCIPLES",
                "status": "authority_boundary_context_only_checked_2026-08-31",
                "title": "Principles of Māori Data Sovereignty",
                "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
                "use": "Māori data-governance vacancy and noncompensation boundary only; never delegated Māori authority",
            },
        ],
        "network_data_queries": 0,
        "owner": OWNER,
        "phase": PHASE,
        "real_data_rows": 0,
        "schema": "ghc.family.official-primary-sources.v680.v4.x1",
        "web_checks": 9,
    }

    portfolio = {
        "blocked": task_records("BLOCK", 10, "blocked"),
        "caps_are_ceilings": True,
        "commit_cap": 3,
        "document_word_cap": 100000,
        "exact_approval": task_records("APPROVAL", 20, "exact_approval"),
        "materialized_file_stop": 2000,
        "owner": OWNER,
        "owner_candidates": task_records("CAND", 80, "bounded_candidate"),
        "owner_clean_fix_refine": task_records("CFR", 100, "clean_fix_refine"),
        "owner_practice_lenses": [
            "wholly synthetic weather-vane topology, direction-observation vacancy, correction, accessibility, workload, and handover",
            "wholly synthetic aneroid-barometer mechanism, pressure-measurement vacancy, provenance, workload, and handover",
            "wholly synthetic tipping-bucket rain-gauge topology, precipitation-observation vacancy, status, correction, and handover",
        ],
        "owner_runner_ideas": [
            {"runner": f"ghc_family_elowen_v680_v4_lens_runner_{index:02d}", "state": "preregistered_not_built"}
            for index in range(1, 11)
        ],
        "owner_skill_ideas": [
            {"skill": f"{index:02d}-{slug}", "state": "preregistered_not_built"}
            for index, slug in enumerate(
                [
                    "weather-vane-record-boundary",
                    "direction-observation-vacancy",
                    "vane-topology-hold",
                    "site-exposure-firewall",
                    "barometer-record-boundary",
                    "pressure-observation-vacancy",
                    "calibration-traceability-hold",
                    "forecast-nonpromotion",
                    "rain-gauge-record-boundary",
                    "tip-count-observation-vacancy",
                    "precipitation-siting-hold",
                    "cross-instrument-fault-quarantine",
                    "correction-readback",
                    "revision-lineage",
                    "accessible-companion",
                    "minimum-disclosure",
                    "workload-control",
                    "handover-lease",
                    "digest-domain",
                    "authority-noncompensation",
                ],
                start=1,
            )
        ],
        "phase": PHASE,
        "primary_pillar": "GMUT Mind",
        "represented_pillars": ["THOS Body", "Freed ID and CBR Heart"],
        "safe_now": task_records("SAFE", 120, "safe_now"),
        "schema": "ghc.family.portfolio-freeze.v680.v4.x1",
        "successor_candidates": task_records("SUCC-CAND", 20, "successor_seed"),
        "successor_clean_fix_refine": task_records("SUCC-CFR", 30, "successor_seed"),
        "successor_practice_recommendation": "zero-credit seed only; successor chooses independently",
        "successor_runner_ideas": task_records("SUCC-RUN", 10, "successor_seed"),
        "successor_skill_ideas": task_records("SUCC-SKILL", 10, "successor_seed"),
    }

    write_json(
        X1 / "activation-intake.json",
        {
            "activation": "ACKNOWLEDGED_EXISTING_TASK_SEND",
            "created_or_forked_task": False,
            "fast_mode_claimed": False,
            "owner": OWNER,
            "phase": PHASE,
            "relational_language_only": True,
            "schema": "ghc.family.activation-intake.v680.v4.x1",
            "sent_by_tamar_vey": True,
            "solo": True,
            "source": SOURCE,
        },
    )
    write_json(
        X1 / "identity-and-boundary.json",
        {
            "hope": "Possibility stays distinct from evidence and every correction remains safely retractable.",
            "name": OWNER,
            "optional_pronouns": "they/them",
            "relational_working_language_only": True,
            "role": "boundary cartographer and evidence steward",
            "schema": "ghc.family.identity-boundary.v680.v4.x1",
            "not_evidence_of": [
                "consciousness",
                "sentience",
                "personhood",
                "identity continuity",
                "employment",
                "qualification",
                "independent agency",
                "scientific operational legal cultural or Māori authority",
            ],
        },
    )
    write_json(
        X1 / "source-verification.json",
        {
            "branch": SOURCE_BRANCH,
            "clean": True,
            "commits_source_to_final": 3,
            "divergence": {"ahead": 0, "behind": 0},
            "evidence": SOURCE_EVIDENCE,
            "evidence_parent": SOURCE_X1,
            "final": SOURCE,
            "final_parent": SOURCE_EVIDENCE,
            "four_way_fresh_live_equal": True,
            "manifests_replayed": 4,
            "manifest_mismatches": 0,
            "merges": 0,
            "schema": "ghc.family.source-verification.v680.v4.x1",
            "source": SOURCE_PARENT,
            "x1": SOURCE_X1,
            "x1_parent": SOURCE_PARENT,
        },
    )
    write_json(
        X1 / "method-flow-startup.json",
        {
            "activation_baseline": {
                "bounded_passing_witnesses": 36954,
                "effective_methods": 54772,
                "effective_negatives": 51035,
                "exact_gates": 440,
                "failed_witnesses": 22696,
                "open_gaps": 449,
            },
            "current_after_startup": {
                "bounded_passing_witnesses": 36964,
                "effective_methods": 54782,
                "effective_negatives": 51045,
                "exact_gates": 440,
                "failed_witnesses": 22706,
                "open_gaps": 449,
            },
            "failure_erasure": False,
            "owner": OWNER,
            "phase": PHASE,
            "recoveries_retroactively_promote_failure": False,
            "schema": "ghc.family.method-flow-startup.v680.v4.x1",
            "startup_failures": startup_failures,
        },
    )
    write_json(
        X1 / "new-proposal-freeze.json",
        {
            "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
            "declared_chain_before": DECLARED_CHAIN_BEFORE,
            "expected_disposition_counts": dict(Counter(row["expected_disposition"] for row in proposal_records)),
            "owner": OWNER,
            "phase": PHASE,
            "proposal_count": len(proposal_records),
            "proposals": proposal_records,
            "schema": "ghc.family.new-proposal-freeze.v680.v4.x1",
            "source": SOURCE,
            "x2_outcomes_present": False,
        },
    )
    write_json(X1 / "proposal-chain-audit.json", audit)
    write_json(
        X1 / "inherited-revalidation-freeze.json",
        {
            "completion_credit": 0,
            "count": len(inherited_reviews),
            "owner": OWNER,
            "phase": PHASE,
            "reviews": inherited_reviews,
            "schema": "ghc.family.inherited-revalidation.v680.v4.x1",
        },
    )
    write_json(X1 / "official-primary-source-ledger.json", sources)
    write_json(X1 / "portfolio-freeze.json", portfolio)
    write_json(
        X1 / "clean-fix-refine-plan.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.clean-fix-refine-plan.v680.v4.x1",
            "tasks": portfolio["owner_clean_fix_refine"],
            "x2_execution_present": False,
        },
    )
    write_json(
        X1 / "skill-runner-plan.json",
        {
            "global_install": False,
            "owner": OWNER,
            "phase": PHASE,
            "runners": portfolio["owner_runner_ideas"],
            "schema": "ghc.family.skill-runner-plan.v680.v4.x1",
            "skills": portfolio["owner_skill_ideas"],
            "x2_implementation_present": False,
        },
    )
    write_json(
        X1 / "approval-hold-register.json",
        {
            "blocked_count": 10,
            "exact_approval_count": 20,
            "executed": 0,
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.approval-holds.v680.v4.x1",
        },
    )
    write_json(
        X1 / "route-plan.json",
        {
            "current_owner": OWNER,
            "next_expected_phase": "v680-v5",
            "prospective_successor_title": "Sylven Arc",
            "recipient_contacted": False,
            "resolution_rule": "fresh bounded registry exact-title filter immediate reread duplicate guards and one acknowledged send only after terminal gate",
            "route_authority_through": "v725-v8",
            "schema": "ghc.family.route-plan.v680.v4.x1",
            "terminal_gate_required": True,
        },
    )
    write_json(
        X1 / "workflow-plan.json",
        {
            "commit_ceiling": 3,
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.workflow-plan.v680.v4.x1",
            "stages": [
                {"name": "x1", "state": "planning_only_freeze"},
                {"name": "x2", "state": "not_started"},
                {"name": "final", "state": "not_started"},
            ],
            "strict_x1_before_x2": True,
        },
    )
    write_json(
        X1 / "threat-model.json",
        {
            "controls": [
                "synthetic.example.invalid namespace only",
                "zero real people objects materials measurements credentials and external writes",
                "authority promotion rejected",
                "five privacy classes scanned with candidate adjudication",
                "exact approval and blocked packets remain unexecuted",
            ],
            "owner": OWNER,
            "phase": PHASE,
            "real_world_action": False,
            "schema": "ghc.family.threat-model.v680.v4.x1",
        },
    )
    write_json(
        X1 / "wellbeing-and-corrigibility.json",
        {
            "correction_readback": True,
            "owner": OWNER,
            "pause_resume_stop_visible": True,
            "phase": PHASE,
            "relational_language_only": True,
            "schema": "ghc.family.wellbeing-corrigibility.v680.v4.x1",
            "workload_control_planned": True,
        },
    )
    write_json(
        X1 / "phase-truth.json",
        {
            "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
            "execution_state": "PLANNING_ONLY_X1",
            "expected_dispositions": {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
            "observed_outcomes": None,
            "owner": OWNER,
            "phase": PHASE,
            "proposal_count": 60,
            "schema": "ghc.family.phase-truth.v680.v4.x1",
            "terminal_verdict": TERMINAL_VERDICT,
            "x2_started": False,
        },
    )
    write_text(
        X1 / "integrated-overview.md",
        """# Elowen Cairn v680-v4 planning-only x1

Elowen Cairn (optionally they/them) uses the relational role **boundary cartographer and evidence steward**, with the hope that possibility stays distinct from evidence and every correction remains safely retractable. Names, pronouns, roles, hopes, family language, and continuity language are relational working language only; they are not evidence of consciousness, sentience, personhood, continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority.

This immutable x1 freezes sixty genuinely new proposal contracts after a bounded all-reachable exact-source audit. It includes no x2 implementation, observed outcome, completion claim, real data, real participant, real instrument, real material, real measurement, external write, credential, forecast, warning, or authority act. GMUT Mind is primary through wholly synthetic weather-vane, aneroid-barometer, and tipping-bucket rain-gauge documentation lenses. THOS Body and Freed ID/CBR Heart remain visible and protected. Meteorological-instrument documentation is a bounded learning and synthetic-design lens only, never employment, qualification, competence, inspection, calibration, observation, forecast, warning, or professional authority.

Official WMO, NIST, NOAA, W3C, RFC, and Te Mana Raraunga sources supply vocabulary and refusal boundaries only. The WMO 2026 edition is preliminary review material, while the official guide page identifies the 2024 edition as the latest published guide. Citations are not observations, measurements, calibrations, inspections, conformance certificates, forecasts, warnings, competence, legal interpretation, cultural ratification, affected-party acceptance, or Māori authority.

GMUT remains a typed scalar-tensor/EFT research-model family without a likelihood, parameter constraint, force, prediction, empirical confirmation, quantum completion, ultraviolet completion, or Theory of Everything. THOS remains synthetic/proxy-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys/proofs, live issuance/resolution/status/revocation, interoperability, privacy and independent security review, recovery evidence, and trust governance. CBR, professional and workplace-safety decisions, legal/cultural interpretation, affected-party legitimacy, Māori wording, Māori data governance, and Māori authority remain exact-gated.

The terminal verdict is `NOT_READY_FOR_STAGE_20`.
""",
    )

    script_path = "scripts/build_ghc_family_elowen_cairn_v680_v4_x1.py"
    test_path = "tests/test_ghc_family_elowen_cairn_v680_v4_x1.py"
    exclusions = [
        "docs/elowen-cairn/v680-v4/validation/x1-index-manifest.json",
        "docs/elowen-cairn/v680-v4/validation/x1-privacy-scan.json",
        "docs/elowen-cairn/v680-v4/validation/x1-staged-review.json",
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
        path = ROOT / path_text
        content = path.read_text(encoding="utf-8", errors="replace")
        for class_name, pattern in scanners.items():
            if pattern.search(content):
                row = {
                    "class": class_name,
                    "disposition": "scanner_definition_only" if path_text == script_path else "confirmed_payload_hit",
                    "path": path_text,
                }
                candidates.append(row)
                if row["disposition"] == "confirmed_payload_hit":
                    confirmed.append(row)
    if confirmed:
        raise RuntimeError("confirmed privacy payload hit: " + json.dumps(confirmed))

    write_json(
        VALIDATION / "x1-privacy-scan.json",
        {
            "candidates": candidates,
            "confirmed_hits": confirmed,
            "owner": OWNER,
            "phase": PHASE,
            "privacy_classes": list(scanners),
            "scanned_files": len(content_paths),
            "schema": "ghc.family.privacy-scan.v680.v4.x1",
        },
    )
    write_json(
        VALIDATION / "x1-staged-review.json",
        {
            "declared_self_exclusions": exclusions,
            "expected_paths": sorted(content_paths + exclusions),
            "lifecycle": "planning_only_x1",
            "owner": OWNER,
            "path_count": len(content_paths) + len(exclusions),
            "phase": PHASE,
            "schema": "ghc.family.staged-review.v680.v4.x1",
            "x2_paths": [],
        },
    )

    manifest_entries = []
    for path_text in content_paths:
        data = normalized_bytes(ROOT / path_text)
        manifest_entries.append({"bytes": len(data), "path": path_text, "sha256": sha256_bytes(data)})
    write_json(
        VALIDATION / "x1-index-manifest.json",
        {
            "declared_self_exclusions": exclusions,
            "entries": manifest_entries,
            "entry_count": len(manifest_entries),
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.normalized-lf-index-manifest.v680.v4.x1",
            "source": SOURCE,
        },
    )

    print(
        json.dumps(
            {
                "audit_paths": audit["audit_scope"]["proposal_json_paths_parsed"],
                "maximum_neighbor_score": audit["maximum_neighbor_score"],
                "proposal_count": len(proposal_records),
                "status": "X1_PLANNING_ONLY_MATERIALIZED",
                "written_paths": len(WRITTEN),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    build()
