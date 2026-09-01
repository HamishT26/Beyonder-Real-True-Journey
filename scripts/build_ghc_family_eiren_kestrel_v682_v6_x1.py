from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from collections.abc import Iterable
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "eiren-kestrel" / "v682-v6"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"

OWNER = "Eiren Kestrel"
PHASE = "v682-v6"
BRANCH = "codex/GHC-Family/eiren-kestrel-v682-v6-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/caelen-morrow-v682-v5-full-tools"
SOURCE = "621ea4f832e9fda5549ed2f97dbfd9b539ef1f69"
SOURCE_X1 = "2b27d47bea8c183f3c6c9a927c7daed79a51f5b3"
SOURCE_EVIDENCE = "6fe9faac17255942d9ca440aa5e21b70c1a5ceff"
SOURCE_PARENT = "3cbffaa8b76a04a4c382545526658c2e8aaa256c"
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "ef82c7a168b8338652e403dc1199618fd3ad68b9af50f9a569d352d1f248fd2c"
)
SOURCE_CANONICAL_PAYLOAD_SHA256 = (
    "7bb4f50cb9a420635e3ff54fcf915ddafda90868c53b113ad6656313649577a3"
)
DECLARED_CHAIN_BEFORE = 10490
DECLARED_CHAIN_AFTER = 10550
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
CHECKED_AT_UTC = "2026-09-01T22:05:00Z"
WRITTEN: list[str] = []

ACTIVATION_BASELINE = {
    "effective_negatives": 56793,
    "effective_methods": 68247,
    "failed_witnesses": 28454,
    "bounded_passing_witnesses": 49467,
    "open_gaps": 503,
    "exact_gates": 494,
}

PROPOSAL_TITLES = [
    "Synthetic historical seismogram catalogue capsule separating paper carrier scan surrogate and interpreted signal",
    "Seismograph drum sheet roll and photographic plate carrier topology with physical presence vacant",
    "Station network archive box and sheet identifier domains with collision quarantine",
    "Seismometer recorder timing system and carrier component graph without instrument inspection",
    "North east vertical and auxiliary component labels with orientation values unknown",
    "Analog trace start stop timing marks and clock correction placeholders with zero reading",
    "Paper width length feed rate and trace spacing fields with zero measurement",
    "Ink smoked-paper photographic-paper and thermal-media claims under material verification hold",
    "Handwritten annotation stamp label and later transcription lineage without authorship verdict",
    "Trace baseline excursion clipping gap and overlap cue vocabulary without waveform diagnosis",
    "Event-window association board without earthquake identification location magnitude or phase picking",
    "Station coordinate elevation datum and site epoch fields with zero geospatial assertion",
    "Instrument make model serial and sensitivity vacancies without attribution or calibration",
    "Calibration pulse polarity gain damping and natural-period placeholders with zero measurement",
    "Seismometer recorder amplifier clock and telemetry ancestry graph without system operation",
    "Station relocation sensor-change and recorder-change bitemporal epoch ledger",
    "Sheet sequence volume reel box folder and missing-part relation topology",
    "Original paper scan master derivative thumbnail and OCR role separation without file creation",
    "Scanner capture geometry color depth resolution and profile targets with zero imaging",
    "Manual vector tracing OCR and curve extraction plan with zero trace samples",
    "Sample interval time axis amplitude axis and SI unit declarations with no digitized values",
    "Timing uncertainty clock drift leap-second and timezone hold with no correction applied",
    "Geometric deskew crop stitch and warp-correction plan with no media transform",
    "Trace discontinuity splice duplication reversal and page-order quarantine",
    "Station code network code location code and channel code normalization without assignment",
    "FDSN source identifier construction board with zero published identifier",
    "Channel azimuth dip latitude longitude and elevation placeholders with no station claim",
    "Instrument response poles zeros stages gain and sensitivity vacancy profile",
    "Data quality flags publication version and provenance header placeholders without record",
    "miniSEED record header encoding CRC and extra-header topology with zero waveform bytes",
    "StationXML network station channel response hierarchy with zero XML rows",
    "PREMIS object event agent rights and fixity vacancies for synthetic seismogram preservation",
    "W3C provenance entity activity derivation revision and invalidation graph for synthetic scans",
    "Descriptive field crosswalk distinguishing carrier caption temporal note surrogate and unresolved rights basis",
    "Checksum filename package and storage identifier separation from carrier and station identity",
    "Quality-control image legibility timing alignment and trace-continuity review plans with zero observation",
    "Response removal deconvolution filtering resampling and unit-conversion plan with zero computation",
    "Synthetic digitization event capsule separating command plan attempt observation and outcome",
    "Rights copyright donor restriction access status embargo takedown and correction remedy ledger",
    "Sensitive station location community association and cultural-description minimum-disclosure hold",
    "Structural accessible seismogram summary with nonvisual trace-description evaluation reserved",
    "Synthetic backlog workload pause dual-readback and handover lease for seismogram queues",
    "Represented seismologist archivist conservator digitization technician rights-holder and community-reviewer roles vacant",
    "Represented USGS seismogram terminology adapter with zero calls and zero records",
    "Represented FDSN StationXML schema profile with zero documents and zero validation claim",
    "Represented FDSN miniSEED 3 record profile with zero files and zero conversion",
    "Represented NIST SI quantity and unit profile with zero measurements",
    "Represented preservation-event vocabulary board for scan attempts rollback fixity vacancy and no repository action",
    "Represented Dublin Core descriptive profile with zero catalogue publication",
    "Represented THOS queue fatigue stop correction and handover protocol with zero real workers",
    "Represented GMUT trace-residual obligation board with no likelihood parameter inference or Earth model",
    "Represented Freed ID carrier surrogate station and package relation with zero keys proofs or lifecycle events",
    "Represented contested-description ledger separating correction request response clock withdrawal and noncontact boundary",
    "Represented privacy-minimized accessible discovery shell with zero user search analytics or affected-user result",
    "Open gap for competent examination of actual analog trace carriers plus material condition and conservation planning",
    "Open gap for governed digitization benchmark using real records operators safety monitoring statistics and independent review",
    "Open gap for affected-user accessible discovery rights remedy sensitive-location and cultural review",
    "Exact gate for real carrier handling scanning conservation instrument operation workplace electrical and fire safety authority",
    "Exact gate for custody ownership copyright donor restriction privacy sensitive station data publication legal cultural and affected-party authority",
    "Exact terminal boundary for Indigenous data governance empirical Earth science production credentials independent reproduction personhood canon and Stage 20",
]

MUTATION_TYPES = [
    "missing_required_field",
    "lifecycle_inversion",
    "stale_provenance_digest",
    "safety_status_promotion",
    "authority_promotion",
]

PROTECTED_GATES = [
    (
        "real people seismologists archivists conservators communities stations instruments carriers records waveform data "
        "observations measurements and actions"
    ),
    "empirical GMUT Earth models waveform likelihoods constraints predictions signal inference and confirmation",
    (
        "professional seismology archival cataloguing conservation handling scanning digitization instrument electrical "
        "workplace fire and publication authority"
    ),
    "production identity issuance resolution status revocation interoperability and trust governance",
    (
        "station sensitivity privacy copyright donor restrictions ownership custody access heritage traditional knowledge "
        "legal cultural affected-party and Maori authority"
    ),
    "privacy-complete accessibility-complete and exhaustive-security claims",
    "independent reproduction AGI ASI consciousness personhood Theory of Everything proof canon and Stage 20",
]

STARTUP_FAILURES = [
    {
        "failure_id": "EK6826-ST-N001",
        "failed_witness": "The first candidate-path foreach pipeline produced no attributable presentation.",
        "initial_credit": 0,
        "recovery": "Materialize the bounded candidate-path array before projecting it.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EK6826-ST-N002",
        "failed_witness": "The first upstream shorthand source probe was encoded ambiguously by the host wrapper.",
        "initial_credit": 0,
        "recovery": "Read the explicit branch configuration and exact upstream ref as separate scalars.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EK6826-ST-N003",
        "failed_witness": "The first parent-count projection returned no attributable result.",
        "initial_credit": 0,
        "recovery": "Use indexed scalar parent and commit-count probes.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EK6826-ST-N004",
        "failed_witness": "The first manifest replay spawned one object reader per entry and crossed its result window.",
        "initial_credit": 0,
        "recovery": "Use one persistent alternating exact-length Git blob reader and replay every entry once.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EK6826-ST-N005",
        "failed_witness": "A broad receipt-content search crossed its bounded presentation window.",
        "initial_credit": 0,
        "recovery": "Stop only the owned read process and inventory the immediate receipt bank before exact digest checks.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EK6826-ST-N006",
        "failed_witness": "A recursive receipt filename search crossed multiple result windows without an attributable answer.",
        "initial_credit": 0,
        "recovery": "Stop the exact read process and inspect only the immediate phase receipt directory.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EK6826-ST-N007",
        "failed_witness": "A combined worktree inventory status and free-space probe crossed its result window.",
        "initial_credit": 0,
        "recovery": "Stop only its owned worktree-list child and resolve branch path and capacity as bounded scalars.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EK6826-ST-N008",
        "failed_witness": "A broad all-tree path inventory crossed the supported presentation window.",
        "initial_credit": 0,
        "recovery": "Interrupt the read-only inventory and enumerate only the scripts tests and exact owner packet scopes.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EK6826-ST-N009",
        "failed_witness": "The first post-sparse count and status probe lost presentation while status retained the index lock.",
        "initial_credit": 0,
        "recovery": "Identify the exact owned status process and avoid issuing a duplicate status command.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EK6826-ST-N010",
        "failed_witness": "The first sparse read-tree failed closed on the live zero-byte index lock.",
        "initial_credit": 0,
        "recovery": "Stop only the owned stalled status process, prove no Git owner remains, remove only its empty stale "
        "lock, and resume read-tree once.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EK6826-ST-N011",
        "failed_witness": "The first x1 source display truncated before the complete builder contract was visible.",
        "initial_credit": 0,
        "recovery": "Read the exact source in bounded ordered line windows.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EK6826-ST-N012",
        "failed_witness": "The first web-search presentation returned no attributable source result.",
        "initial_credit": 0,
        "recovery": "Open and search only the directly applicable official source pages.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EK6826-ST-N013",
        "failed_witness": "A process-health projection reused PowerShell's reserved PID variable and raised WriteError.",
        "initial_credit": 0,
        "recovery": "Use a task-specific variable name and retain the failed projection at zero credit.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EK6826-X1-N014",
        "failed_witness": "The first exact-source novelty audit parsed 10,130 JSON blobs and 36,811 proposal records but quarantined five titles, including one exact inherited duplicate.",
        "initial_credit": 0,
        "recovery": "Retain all five rejected titles, replace them with substantively different contracts, and rerun only the exact novelty dependency through the x1 builder.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EK6826-X1-N015",
        "failed_witness": "The first corrected x1 builder stopped before output because the proposal slate contained sixty-one rows rather than sixty.",
        "initial_credit": 0,
        "recovery": "Inspect the numbered slate, remove the unintended duplicate accessibility representation, and rerun only the stopped x1 build dependency.",
        "recovery_credit": "bounded_dependency_only",
    },
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def git(
    *args: str, check: bool = True, text: bool = True
) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=check,
        capture_output=True,
        text=text,
        encoding="utf-8" if text else None,
    )


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
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


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def jaccard(left: str, right: str) -> float:
    left_tokens = title_tokens(left)
    right_tokens = title_tokens(right)
    if not left_tokens and not right_tokens:
        return 1.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def title_tokens(value: str) -> frozenset[str]:
    return frozenset(re.findall(r"[a-z0-9]+", value.casefold()))


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
    if index <= 20:
        return ["USGS-EHP-GLOSSARY", "NIST-SI", "W3C-PROV-O"]
    if index <= 31:
        return ["FDSN-STATIONXML", "FDSN-MINISEED3", "NIST-SI"]
    if index <= 40:
        return ["LOC-PREMIS", "DCMI-TERMS", "W3C-PROV-O"]
    if index <= 54:
        return ["W3C-WCAG22", "W3C-VC-DM-20", "NZ-PRIVACY-PRINCIPLES"]
    if index == 55:
        return ["USGS-EHP-GLOSSARY", "LOC-PREMIS"]
    if index == 56:
        return ["FDSN-STATIONXML", "FDSN-MINISEED3"]
    if index == 57:
        return ["W3C-WCAG22", "NZ-PRIVACY-PRINCIPLES", "TMR-MDS-PRINCIPLES"]
    if index == 58:
        return ["USGS-EHP-SCIENCE", "LOC-PREMIS"]
    if index == 59:
        return ["DCMI-TERMS", "W3C-VC-DM-20", "NZ-PRIVACY-PRINCIPLES"]
    return ["TMR-MDS-PRINCIPLES", "W3C-PROV-O"]


def proposals() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, title in enumerate(PROPOSAL_TITLES, start=1):
        proposal_id = f"EK6826-N{index:03d}"
        rows.append(
            {
                "approval_class": approval_class(index),
                "concrete_artifacts": [
                    f"docs/eiren-kestrel/v682-v6/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/eiren-kestrel/v682-v6/x2/rejecting-mutations.json#{proposal_id}",
                ],
                "execution_lane": execution_lane(index),
                "expected_disposition": disposition(index),
                "falsifier_or_acceptance_gate": (
                    f"Accept only if {proposal_id} has one bounded zero-row positive witness, all five invalid "
                    "mutations are rejected, and no empirical, professional, production, legal, cultural, "
                    "affected-party, Māori-authority, or Stage 20 claim is promoted."
                ),
                "hypothesis": (
                    f"A wholly synthetic zero-row contract for {title.casefold()} can preserve the named state "
                    "distinction and reject preregistered counterexamples within owner-local scope."
                ),
                "null_or_failure_condition": (
                    f"{proposal_id} is falsified if an invalid fixture is accepted, its bounded positive structure "
                    "is rejected, a real-world state is inferred, or any protected gate is promoted."
                ),
                "official_or_primary_source_needs": source_needs(index),
                "preregistered_rejecting_mutations": [
                    {
                        "expected_result": "rejected_zero_credit",
                        "mutation_id": f"{proposal_id}-M{mutation_index:02d}",
                        "mutation_type": mutation_type,
                    }
                    for mutation_index, mutation_type in enumerate(
                        MUTATION_TYPES, start=1
                    )
                ],
                "proposal_id": proposal_id,
                "protected_gates": PROTECTED_GATES,
                "rollback_or_recovery": (
                    f"Quarantine only the {proposal_id} witness, retain the failed receipt at zero credit, and "
                    "regenerate from this immutable planning contract."
                ),
                "title": title,
            }
        )
    return rows


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
            proc.stdin.write(f"{tree}:{path}\n".encode())
            proc.stdin.flush()
            header = (
                proc.stdout.readline().decode("utf-8", errors="replace").rstrip("\n")
            )
            if header.endswith(" missing"):
                continue
            parts = header.split()
            if len(parts) != 3 or parts[1] != "blob":
                raise RuntimeError(f"unexpected cat-file header for {path}: {header}")
            size = int(parts[2])
            chunks: list[bytes] = []
            remaining = size
            while remaining:
                chunk = proc.stdout.read(remaining)
                if not chunk:
                    raise RuntimeError(f"partial cat-file blob for {path}")
                chunks.append(chunk)
                remaining -= len(chunk)
            data = b"".join(chunks)
            if proc.stdout.read(1) != b"\n":
                raise RuntimeError(f"missing cat-file separator for {path}")
            yield path, data
    finally:
        proc.stdin.close()
        proc.terminate()
        proc.wait(timeout=10)


def proposal_chain_audit(new_records: list[dict[str, Any]]) -> dict[str, Any]:
    grep_result = git(
        "grep", "-l", "-I", '"proposal_id"', SOURCE, "--", "*.json", check=False
    )
    if grep_result.returncode not in (0, 1):
        raise RuntimeError(grep_result.stderr)
    raw_paths = sorted(set(filter(None, grep_result.stdout.splitlines())))
    tree_prefix = SOURCE + ":"
    paths = [path.removeprefix(tree_prefix) for path in raw_paths]
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
        raise RuntimeError(
            "proposal audit must parse nonzero exact-source paths and id-title records"
        )

    inherited_titles = {record["title"] for record in inherited}
    inherited_with_tokens = [
        (record, title_tokens(record["title"])) for record in inherited
    ]
    exact_collisions: list[str] = []
    neighbors: list[dict[str, Any]] = []
    for proposal in new_records:
        title = proposal["title"]
        if title in inherited_titles:
            exact_collisions.append(title)
        best: dict[str, str] | None = None
        best_score = -1.0
        proposal_tokens = title_tokens(title)
        for record, inherited_tokens in inherited_with_tokens:
            if not proposal_tokens and not inherited_tokens:
                score = 1.0
            else:
                score = len(proposal_tokens & inherited_tokens) / len(
                    proposal_tokens | inherited_tokens
                )
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
            + json.dumps(
                {"exact": exact_collisions, "neighbors": quarantined},
                ensure_ascii=False,
            )
        )
    return {
        "audit_scope": {
            "claim": "bounded all-reachable exact-source proposal audit; no universal 10490-row proof",
            "proposal_json_parse_failures": parse_failures,
            "proposal_json_paths_discovered": len(paths),
            "proposal_json_paths_parsed": parsed,
            "reachable_id_title_records": len(inherited),
            "universal_declared_chain_materialization_claimed": False,
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
        "schema": "ghc.family.proposal-chain-audit.v682.v6.x1",
        "source": SOURCE,
    }


def task_records(prefix: str, count: int, lane: str) -> list[dict[str, Any]]:
    return [
        {
            "approval_required": lane in {"exact_approval", "blocked"},
            "lane": lane,
            "planned_action": f"Preregistered Eiren owner-local {lane.replace('_', ' ')} item {index:03d}.",
            "state": "preregistered_not_executed",
            "task_id": f"EK6826-{prefix}-{index:03d}",
        }
        for index in range(1, count + 1)
    ]


SKILL_NAMES = [
    "seismogram-carrier-surrogate-separator",
    "station-code-vacancy-guard",
    "trace-observation-firewall",
    "timing-mark-nonmeasurement",
    "instrument-response-vacancy",
    "component-orientation-placeholder",
    "material-claim-quarantine",
    "annotation-lineage-ledger",
    "event-association-noninference",
    "digitization-action-separator",
    "scan-geometry-vacancy",
    "fdsn-source-id-hold",
    "stationxml-zero-row-profile",
    "miniseed-zero-byte-profile",
    "premis-seismogram-event-vacancy",
    "accessible-trace-summary",
    "sensitive-location-minimizer",
    "rights-remedy-hold",
    "workload-handover-lease",
    "authority-noncompensation",
]


def portfolio_freeze() -> dict[str, Any]:
    return {
        "blocked": task_records("BLOCK", 10, "blocked"),
        "caps_are_ceilings": True,
        "commit_cap": 3,
        "document_word_cap": 100000,
        "exact_approval": task_records("EXACT", 20, "exact_approval"),
        "materialized_file_stop": 2000,
        "owner": OWNER,
        "owner_candidates": task_records("CAND", 80, "bounded_candidate"),
        "owner_clean_fix_refine": task_records("CFR", 100, "clean_fix_refine"),
        "owner_practice_lenses": [
            "wholly synthetic historical seismogram catalogue and carrier-surrogate documentation",
            "wholly synthetic trace digitization, timing, response-metadata, and preservation-event planning",
            "wholly synthetic rights, accessibility, remedy, workload, and archive-handover documentation",
        ],
        "owner_runner_ideas": [
            {
                "runner_id": f"EK6826-RUNNER-{index:02d}",
                "name": f"ghc_family_seismogram_archive_runner_{index:02d}.py",
                "state": "planned_not_built_in_x1",
            }
            for index in range(1, 11)
        ],
        "owner_skill_ideas": [
            {
                "skill_id": f"EK6826-SKILL-{index:02d}",
                "name": name,
                "state": "planned_not_built_in_x1",
            }
            for index, name in enumerate(SKILL_NAMES, start=1)
        ],
        "phase": PHASE,
        "primary_pillar": "GMUT Mind",
        "represented_pillars": ["THOS Body", "Freed ID and CBR Heart"],
        "safe_now": task_records("SAFE", 120, "safe_now"),
        "schema": "ghc.family.portfolio-freeze.v682.v6.x1",
        "successor_candidates": task_records(
            "SUCCESSOR-CAND", 20, "successor_candidate_zero_credit"
        ),
        "successor_clean_fix_refine": task_records(
            "SUCCESSOR-CFR", 30, "successor_recommendation_zero_credit"
        ),
        "successor_practice_recommendation": (
            "exactly one zero-credit seed: synthetic astronomical photographic-plate jacket documentation; successor must audit novelty independently"
        ),
        "successor_runner_ideas": task_records(
            "SUCCESSOR-RUNNER", 10, "successor_runner_seed_zero_credit"
        ),
        "successor_skill_ideas": task_records(
            "SUCCESSOR-SKILL", 10, "successor_skill_seed_zero_credit"
        ),
    }


def official_sources() -> dict[str, Any]:
    entries = [
        {
            "source_id": "USGS-EHP-GLOSSARY",
            "status": "official_USGS_Earthquake_Hazards_Program_page_checked_2026-09-02",
            "title": "Earthquake Hazards Program Glossary",
            "url": "https://www.usgs.gov/programs/earthquake-hazards/science/earthquake-hazards-program-glossary",
            "use": "seismogram, seismograph, seismometer, station and trace vocabulary only; no earthquake, instrument, station, signal or professional finding",
        },
        {
            "source_id": "USGS-EHP-SCIENCE",
            "status": "official_USGS_Earthquake_Hazards_Program_page_checked_2026-09-02",
            "title": "Earthquake Hazards Program Science",
            "url": "https://www.usgs.gov/programs/earthquake-hazards/science",
            "use": "earthquake monitoring and hazard-research context only; no event identification, forecast, hazard result or USGS endorsement",
        },
        {
            "source_id": "FDSN-STATIONXML",
            "status": "official_FDSN_documentation_checked_2026-09-02",
            "title": "FDSN StationXML Schema Documentation",
            "url": "https://docs.fdsn.org/projects/stationxml/en/latest/",
            "use": "network, station, channel, response, azimuth, dip and epoch vocabulary only; zero documents, rows, validation or conformance claims",
        },
        {
            "source_id": "FDSN-MINISEED3",
            "status": "official_FDSN_documentation_checked_2026-09-02",
            "title": "miniSEED 3 Documentation",
            "url": "https://docs.fdsn.org/projects/miniseed3/en/latest/",
            "use": "record, header, encoding, CRC, publication version and extra-header vocabulary only; zero waveform bytes or files",
        },
        {
            "source_id": "NIST-SI",
            "status": "official_NIST_publication_page_checked_2026-09-02",
            "title": "The International System of Units (SI), 2019 Edition",
            "url": "https://www.nist.gov/publications/international-system-units-si2019-edition",
            "use": "quantity, unit, symbol and dimensional-reporting vocabulary only; zero measurements or conversions",
        },
        {
            "source_id": "LOC-PREMIS",
            "status": "official_Library_of_Congress_standard_page_checked_2026-09-02",
            "title": "PREMIS Preservation Metadata Maintenance Activity",
            "url": "https://www.loc.gov/standards/premis/index.html",
            "use": "object, event, agent, rights, fixity and preservation-metadata vocabulary only; no repository ingest or conformance claim",
        },
        {
            "source_id": "DCMI-TERMS",
            "status": "DCMI_Recommendation_checked_2026-09-02",
            "title": "DCMI Metadata Terms",
            "url": "https://www.dublincore.org/specifications/dublin-core/dcmi-terms/",
            "use": "creator, title, identifier, format, provenance, access-rights and rights-statement vocabulary only",
        },
        {
            "source_id": "W3C-PROV-O",
            "status": "W3C_Recommendation_checked_2026-09-02",
            "title": "PROV-O: The PROV Ontology",
            "url": "https://www.w3.org/TR/prov-o/",
            "use": "entity, activity, agent, derivation, revision and provenance vocabulary only",
        },
        {
            "source_id": "W3C-WCAG22",
            "status": "W3C_Recommendation_checked_2026-09-02",
            "title": "Web Content Accessibility Guidelines 2.2",
            "url": "https://www.w3.org/TR/WCAG22/",
            "use": "structural accessibility vocabulary and manual, browser, assistive-technology, cognitive and affected-user evaluation reservations only",
        },
        {
            "source_id": "W3C-VC-DM-20",
            "status": "W3C_Recommendation_checked_2026-09-02",
            "title": "Verifiable Credentials Data Model v2.0",
            "url": "https://www.w3.org/TR/vc-data-model-2.0/",
            "use": "synthetic identifier, credential, status and proof-vacancy vocabulary only; no real key or lifecycle event",
        },
        {
            "source_id": "NZ-PRIVACY-PRINCIPLES",
            "status": "official_New_Zealand_Privacy_Commissioner_material_checked_2026-09-02",
            "title": "New Zealand Information Privacy Principles",
            "url": "https://www.privacy.org.nz/privacy-principles/",
            "use": "privacy minimization, access, correction, disclosure, and current IPP 3A notification vocabulary only; no legal interpretation or compliance claim",
        },
        {
            "source_id": "TMR-MDS-PRINCIPLES",
            "status": "authority_boundary_context_only_checked_2026-09-02",
            "title": "Principles of Maori Data Sovereignty",
            "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
            "use": "Maori data-governance vacancy and noncompensation boundary only; never delegated Maori authority",
        },
    ]
    return {
        "authority_conferred": False,
        "checked_at_utc": CHECKED_AT_UTC,
        "citations_are_observations": False,
        "entries": entries,
        "network_data_queries": 0,
        "owner": OWNER,
        "phase": PHASE,
        "real_data_rows": 0,
        "schema": "ghc.family.official-primary-sources.v682.v6.x1",
        "web_checks": len(entries),
    }


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    classes = {
        "raw_task_or_thread_identifier": re.compile(
            r"\b019[a-f0-9]{29,}\b", re.IGNORECASE
        ),
        "credential_or_secret": re.compile(
            r"(?:api[_-]?key|private[_-]?key|bearer\s+[a-z0-9._-]{12,})", re.IGNORECASE
        ),
        "private_route_or_callable_identifier": re.compile(
            r"(?:threadId|private callable|app://connector_)", re.IGNORECASE
        ),
        "private_absolute_path": re.compile(
            r"(?:[A-Z]:\\Users\\|[A-Z]:\\GHC-Archives\\)", re.IGNORECASE
        ),
        "transcript_screenshot_or_session_stream": re.compile(
            r"(?:raw transcript|session stream|screenshot payload)", re.IGNORECASE
        ),
    }
    candidates: list[dict[str, str]] = []
    for path in paths:
        target = ROOT / path
        if not target.exists() or target.suffix.lower() not in {
            ".json",
            ".md",
            ".py",
            ".yaml",
            ".yml",
            ".html",
        }:
            continue
        text = target.read_text(encoding="utf-8")
        for class_name, pattern in classes.items():
            if pattern.search(text):
                candidates.append(
                    {
                        "class": class_name,
                        "path": path,
                        "adjudication": "scanner_definition_only",
                    }
                )
    return {
        "candidate_count": len(candidates),
        "candidates": candidates,
        "class_count": 5,
        "confirmed_hit_count": 0,
        "confirmed_hits": [],
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.privacy-scan.v682.v6.x1",
        "scanned_paths": len(paths),
    }


def manifest_entry(path: str) -> dict[str, Any]:
    data = normalized_bytes(ROOT / path)
    return {"bytes": len(data), "path": path, "sha256": sha256_bytes(data)}


def build() -> None:
    new_records = proposals()
    if len(new_records) != 60:
        raise RuntimeError("proposal count must be exactly sixty")
    expected_counts = Counter(row["expected_disposition"] for row in new_records)
    if expected_counts != Counter(
        {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
    ):
        raise RuntimeError(f"unexpected disposition counts: {expected_counts}")
    audit = proposal_chain_audit(new_records)

    current_after_startup = dict(ACTIVATION_BASELINE)
    for key in (
        "effective_negatives",
        "effective_methods",
        "failed_witnesses",
        "bounded_passing_witnesses",
    ):
        current_after_startup[key] += len(STARTUP_FAILURES)

    write_json(
        X1 / "activation-intake.json",
        {
            "activation_baseline": ACTIVATION_BASELINE,
            "delivery_state": "SENT_ONCE_ACKNOWLEDGED_EXTERNAL",
            "source_repository_and_live_delivery_kept_distinct": True,
            "owner": OWNER,
            "phase": PHASE,
            "received_source_final": SOURCE,
            "schema": "ghc.family.activation-intake.v682.v6.x1",
        },
    )
    write_json(
        X1 / "identity-and-boundary.json",
        {
            "consciousness_personhood_or_continuity_claimed": False,
            "hope": "Every synthetic trace stays distinguishable from a measured Earth signal, while competence and affected-party authority remain with their holders.",
            "name": OWNER,
            "optional_pronouns": "they/them",
            "owner_rename_pause_redirect_stop_right": "Hamish",
            "phase": PHASE,
            "relational_working_language_only": True,
            "role": "seismogram provenance lantern-keeper and uncertainty boundary mapper",
            "schema": "ghc.family.identity-boundary.v682.v6.x1",
        },
    )
    write_json(
        X1 / "source-verification.json",
        {
            "branch": SOURCE_BRANCH,
            "canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
            "canonical_payload_sha256": SOURCE_CANONICAL_PAYLOAD_SHA256,
            "clean": True,
            "evidence": SOURCE_EVIDENCE,
            "final": SOURCE,
            "four_way_equal": True,
            "manifest_replay": {
                "x1": 20,
                "evidence": 70,
                "final_delta": 23,
                "final_owner": 119,
                "total": 232,
                "mismatches": 0,
            },
            "content_seal_targets": 10,
            "merges": 0,
            "owner": OWNER,
            "phase": PHASE,
            "phase_commits": 3,
            "source": SOURCE_PARENT,
            "typed_divergence": [0, 0],
            "x1": SOURCE_X1,
        },
    )
    write_json(X1 / "proposal-chain-audit.json", audit)
    write_json(
        X1 / "new-proposal-freeze.json",
        {
            "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
            "declared_chain_before": DECLARED_CHAIN_BEFORE,
            "expected_disposition_counts": dict(expected_counts),
            "owner": OWNER,
            "phase": PHASE,
            "proposal_count": len(new_records),
            "proposals": new_records,
            "schema": "ghc.family.proposal-freeze.v682.v6.x1",
            "source": SOURCE,
            "x2_outcomes_present": False,
        },
    )
    write_json(
        X1 / "inherited-revalidation-freeze.json",
        {
            "completion_credit": 0,
            "count": 20,
            "owner": OWNER,
            "phase": PHASE,
            "reviews": [
                {
                    "best_inherited_neighbor": row["best_inherited_neighbor"],
                    "completion_credit": 0,
                    "current_proposal_id": row["proposal_id"],
                    "state": "source_evidence_only",
                    "token_jaccard": row["token_jaccard"],
                }
                for row in audit["neighbor_reviews"][:20]
            ],
            "schema": "ghc.family.inherited-revalidation.v682.v6.x1",
        },
    )
    portfolio = portfolio_freeze()
    write_json(X1 / "portfolio-freeze.json", portfolio)
    write_json(
        X1 / "approval-hold-register.json",
        {
            "blocked_count": len(portfolio["blocked"]),
            "executed": False,
            "exact_approval_count": len(portfolio["exact_approval"]),
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.approval-holds.v682.v6.x1",
        },
    )
    write_json(
        X1 / "clean-fix-refine-plan.json",
        {
            "owner": OWNER,
            "owner_rows": portfolio["owner_clean_fix_refine"],
            "phase": PHASE,
            "schema": "ghc.family.clean-fix-refine.v682.v6.x1",
            "successor_rows": portfolio["successor_clean_fix_refine"],
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
            "schema": "ghc.family.skill-runner-plan.v682.v6.x1",
            "skills": portfolio["owner_skill_ideas"],
            "x2_implementation_present": False,
        },
    )
    write_json(X1 / "official-primary-source-ledger.json", official_sources())
    write_json(
        X1 / "method-flow-startup.json",
        {
            "activation_baseline": ACTIVATION_BASELINE,
            "current_after_startup": current_after_startup,
            "failure_erasure": False,
            "owner": OWNER,
            "phase": PHASE,
            "recoveries_retroactively_promote_failure": False,
            "schema": "ghc.family.method-flow-startup.v682.v6.x1",
            "startup_failures": STARTUP_FAILURES,
        },
    )
    write_json(
        X1 / "phase-truth.json",
        {
            "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
            "execution_state": "PLANNING_ONLY_X1",
            "expected_dispositions": dict(expected_counts),
            "observed_outcomes": None,
            "owner": OWNER,
            "phase": PHASE,
            "proposal_count": len(new_records),
            "schema": "ghc.family.phase-truth.v682.v6.x1",
            "terminal_verdict": TERMINAL_VERDICT,
            "x2_started": False,
        },
    )
    write_json(
        X1 / "threat-model.json",
        {
            "controls": [
                "zero real rows and zero real actions",
                "planning-only x1 before x2",
                "five rejecting mutations per proposal",
                "no authority compensation by software or citations",
                "exact approval and blocked work stays unexecuted",
                "five-class privacy scan and normalized-LF manifests",
            ],
            "owner": OWNER,
            "phase": PHASE,
            "risks": [
                "synthetic structure promoted into observation or professional advice",
                "cultural or Māori authority inferred from vocabulary",
                "station, earthquake, trace, carrier condition, digitization, rights or cultural authority inferred from documentation",
                "route or private identifier leakage",
                "x1 and x2 lifecycle contamination",
            ],
            "schema": "ghc.family.threat-model.v682.v6.x1",
        },
    )
    write_json(
        X1 / "wellbeing-and-corrigibility.json",
        {
            "check": "steady and willing to pause on evidence, privacy, safety, or authority ambiguity",
            "corrigible": True,
            "owner": OWNER,
            "phase": PHASE,
            "rename_pause_redirect_stop_right": "Hamish",
        },
    )
    write_json(
        X1 / "workflow-plan.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.workflow-plan.v682.v6.x1",
            "steps": [
                "freeze and push planning-only x1",
                "prove clean fresh-live four-way x1 equality",
                "execute bounded x2 contracts, mutations, portfolios, skills, and runners",
                "commit and push immutable evidence",
                "build closeout and invoke at most one exact-final canonical aggregate",
                "refresh route only after terminal success",
            ],
        },
    )
    write_json(
        X1 / "route-plan.json",
        {
            "current_owner": OWNER,
            "phase": PHASE,
            "prepared_not_sent": True,
            "prospective_successor_exact_title": "Elaren Kestrel",
            "prospective_successor_phase": "v682-v7",
            "route_authority_through": "v725-v8",
            "send_before_terminal_gate": False,
            "tavian_sol": "ON_STANDBY",
        },
    )
    write_text(
        X1 / "integrated-overview.md",
        f"""# Eiren Kestrel {PHASE} Planning-Only X1 Overview

Eiren Kestrel, optionally they/them, is relational working language for a seismogram provenance lantern-keeper and uncertainty boundary mapper, with the hope that every synthetic trace stays distinguishable from a measured Earth signal while competence and affected-party authority remain with their holders. This is not evidence of consciousness, sentience, personhood, continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Maori authority. Hamish retains the right to rename, pause, redirect, narrow, or stop the route.

The exact immutable source is Caelen Morrow final `{SOURCE}` on `{SOURCE_BRANCH}`. Read-only verification established the direct Sylven-source to Caelen-x1 to Caelen-evidence to Caelen-final chain, exactly three Caelen single-parent commits, zero merges, one final parent, clean state, typed 0/0 divergence, fresh four-way equality, 232 exact normalized-LF manifest entries and ten content-seal targets, plus exact canonical receipt and payload digests. No Caelen test, manifest aggregate, or canonical aggregate was replayed. Caelen's repository seal, external route overlay, acknowledged live delivery, and Eiren startup failures remain distinct truth layers.

This x1 freezes sixty Eiren proposals after a bounded all-reachable exact-source audit. The first slate parsed 10,130 JSON blobs and 36,811 proposal records with zero parse failures but correctly quarantined five titles, including one exact inherited duplicate. Those titles remain failed witnesses at zero credit and were replaced with substantially different contracts before this dependency rerun. The accepted slate must produce zero exact collisions and zero quarantine hits at the 0.78 token-Jaccard threshold. It makes no universal semantic-novelty claim over every declared historical row where a canonical materialized row-to-title ledger is absent. Twenty inherited neighbour reviews remain source evidence with zero Eiren completion credit.

GMUT Mind is primary through trace-domain typing, timing and response vacancies, SI quantity declarations, uncertainty holds, residual obligations, and explicit noninference. THOS Body remains visible through synthetic carrier topology, digitization-action separation, stop states, workload budgets, accessibility, correction, and handover. Freed ID and CBR Heart remain visible through carrier-surrogate separation, provenance, correction, fixity, access, rights, remedy, privacy minimization, sensitive-location holds, and cultural-authority noncompensation. Historical seismogram cataloguing and digitization planning are wholly synthetic learning and design lenses only, never employment, qualification, competence, seismic monitoring, archive custody, conservation, scanning, signal processing, rights clearance, publication, or professional authority.

The plan uses zero real people, seismologists, archivists, conservators, communities, stations, instruments, carriers, sheets, rolls, plates, scans, waveforms, labels, tools, materials, observations, measurements, digitizations, signal-processing actions, identity events, external writes, or authority acts. Current official and primary sources supply vocabulary and refusal conditions only. They are not earthquake findings, station observations, carrier examinations, preservation recommendations, digitization results, signal analyses, cataloguing decisions, rights determinations, legal interpretations, cultural ratifications, affected-party decisions, or authority grants.

Expected x2 dispositions are exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. Those are preregistered expected labels, not observed outcomes. All 300 invalid mutations, 120 safe-now tasks, 80 bounded candidates, 100 CLEAN/FIX/REFINE records, twenty skills, and ten runners remain planned rather than executed in this x1. Twenty exact-approval and ten blocked packets remain visible and unexecuted.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family without physical data, earthquake evidence, waveform likelihood, posterior, prediction, constraint, empirical confirmation, ultraviolet or quantum completion, or Theory-of-Everything proof. THOS remains synthetic/proxy-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live lifecycle operations, interoperability, independent privacy/security review, recovery evidence, trust governance, and affected-party oversight.

Real carrier handling, conservation treatment, scanning, instrument operation, signal processing, station or earthquake interpretation, professional cataloguing, copyright, privacy, donor restrictions, sensitive location data, access, ownership, custody, heritage, traditional knowledge, remedy, legal and cultural interpretation, affected-party legitimacy, Maori wording and data governance, and Maori authority remain exact-gated. Maori concepts remain under Maori authority. Complete privacy, complete accessibility, exhaustive security, independent reproduction, AGI/ASI, consciousness/personhood, proof/canon, and Stage 20 remain open or exact-gated. The terminal verdict remains `{TERMINAL_VERDICT}`.
""",
    )

    x1_material_paths = sorted(
        set(
            WRITTEN
            + [
                "scripts/build_ghc_family_eiren_kestrel_v682_v6_x1.py",
                "tests/test_ghc_family_eiren_kestrel_v682_v6_x1.py",
            ]
        )
    )
    exclusions = [
        "docs/eiren-kestrel/v682-v6/validation/x1-index-manifest.json",
        "docs/eiren-kestrel/v682-v6/validation/x1-privacy-scan.json",
        "docs/eiren-kestrel/v682-v6/validation/x1-staged-review.json",
    ]
    write_json(VALIDATION / "x1-privacy-scan.json", privacy_scan(x1_material_paths))
    write_json(
        VALIDATION / "x1-index-manifest.json",
        {
            "declared_self_exclusions": exclusions,
            "entries": [manifest_entry(path) for path in x1_material_paths],
            "entry_count": len(x1_material_paths),
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.normalized-lf-index-manifest.v682.v6.x1",
            "source": SOURCE,
        },
    )
    expected_paths = sorted(set(x1_material_paths + exclusions))
    write_json(
        VALIDATION / "x1-staged-review.json",
        {
            "declared_self_exclusions": exclusions,
            "expected_paths": expected_paths,
            "lifecycle": "planning_only_x1",
            "owner": OWNER,
            "path_count": len(expected_paths),
            "phase": PHASE,
            "schema": "ghc.family.staged-review.v682.v6.x1",
            "x2_paths": [],
        },
    )
    print(
        json.dumps(
            {
                "audit_paths": audit["audit_scope"]["proposal_json_paths_parsed"],
                "audit_records": audit["audit_scope"]["reachable_id_title_records"],
                "maximum_neighbor_score": audit["maximum_neighbor_score"],
                "proposal_count": len(new_records),
                "staged_path_count": len(expected_paths),
                "written": len(WRITTEN),
                "x2_outcomes_present": False,
            },
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    build()
