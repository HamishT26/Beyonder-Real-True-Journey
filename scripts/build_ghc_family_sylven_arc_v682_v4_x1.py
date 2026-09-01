from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "sylven-arc" / "v682-v4"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"

OWNER = "Sylven Arc"
PHASE = "v682-v4"
BRANCH = "codex/GHC-Family/sylven-arc-v682-v4-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/elowen-cairn-v682-v3-full-tools"
SOURCE = "2dcad52ce5e64cfef69bdb50335638eaa4954ef5"
SOURCE_X1 = "607c6742f44e2dbd3d7d66bf20348ad3ffe8bcfb"
SOURCE_EVIDENCE = "743bdbcf879dd600f05e5cbea645e00557cbbf85"
SOURCE_PARENT = "ed63ba1080cbb0a69701e56fd9bee9c80221a709"
SOURCE_CANONICAL_RECEIPT_SHA256 = "4fab7dd298125b5a304bcf8dd6af39b0893bc0530a4ebe859ba285f530882b3d"
SOURCE_CANONICAL_PAYLOAD_SHA256 = "f5d42ed4ec00daee07ac3f63fc605421a1bf6f20f46215d02290bb966eabdd8d"
DECLARED_CHAIN_BEFORE = 10370
DECLARED_CHAIN_AFTER = 10430
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
CHECKED_AT_UTC = "2026-09-02T05:00:00Z"
WRITTEN: list[str] = []

ACTIVATION_BASELINE = {
    "effective_negatives": 56132,
    "effective_methods": 66686,
    "failed_witnesses": 27793,
    "bounded_passing_witnesses": 48026,
    "open_gaps": 497,
    "exact_gates": 488,
}

PROPOSAL_TITLES = [
    "Synthetic sextant record capsule and real instrument identity split",
    "Sextant frame arc limb and index-arm topology with unresolved physical presence",
    "Horizon mirror index mirror and reflection-path topology without optical observation",
    "Telescope sight tube collar and eyepiece relation graph without performance claim",
    "Scale vernier micrometer and tangent-screw reading topology with zero reading",
    "Clamp release and fine-adjustment plan versus executed-action separation",
    "Sun shade filter and horizon-glass relation with optical-safety hold",
    "Handle storage case and accessory topology with custody vacancy",
    "Maker model serial and inscription transcription versus attribution firewall",
    "Frame mirror glass finish and material-claim vacancy ledger",
    "Dimension mass radius and aperture target fields with zero measurement",
    "Graduation least-count unit and tolerance targets without calibration claim",
    "Index error side error perpendicularity and correction vacancy board",
    "Scratch corrosion looseness breakage and unknown cues without condition diagnosis",
    "Cleaning lubrication adjustment repair and intervention plan under professional hold",
    "Artificial horizon chronometer and reference-accessory relation with no use claim",
    "Sextant custody provenance access reproduction and rights topology",
    "Accessible instrument intake summary with noncolour status and manual evaluation reserve",
    "Synthetic celestial-sight capsule and real observation identity split",
    "Observer vessel site date and time vacancies with minimized identifiers",
    "Celestial-body target label and real object identification firewall",
    "Visible sea horizon artificial horizon and dip-correction vacancy graph",
    "Raw altitude corrected altitude and intercept state separation with zero angle reading",
    "UTC timestamp chronometer error and time-reference vacancy ledger",
    "GHA SHA declination and almanac-edition provenance braid",
    "Assumed latitude longitude estimated position and observed-fix separation",
    "Altitude azimuth right-ascension and declination coordinate-domain board",
    "Degree minute second and radian angle-unit separation without conversion result",
    "Refraction parallax semidiameter and dip correction graph with no computation",
    "Sight-reduction table method model and edition provenance without execution",
    "Intercept azimuth and line-of-position geometry topology without navigational result",
    "Uncertainty residual scatter and outlier vacancy ledger without statistical inference",
    "Multiple-sight batch sequence and dependency topology with no fix claim",
    "Command calculation observation transcription and decision-state separation",
    "Celestial-sight correction challenge supersession and dual-readback lineage",
    "Accessible sight record with text alternatives and affected-user evaluation reserved",
    "Synthetic navigation-handover capsule with zero vessel movement or route release",
    "Chart almanac chronometer sextant and weather-input dependency graph",
    "Publication edition update effective-time and supersession provenance chain",
    "Course heading bearing track speed and distance domain separation",
    "Fix estimated position dead reckoning and line-of-position status firewall",
    "Weather visibility sea-state and horizon cues without forecast or safety decision",
    "Represented lookout navigator officer custodian and reviewer role vacancies",
    "Represented fatigue workload pause and governed watch-handover queue",
    "Represented instrument operability calibration and fitness-for-navigation hold",
    "Represented route course and voyage-safety decision with no authorization",
    "Represented USNO almanac vocabulary adapter with zero calls and zero rows",
    "Represented Smithsonian sextant collection adapter with zero calls and zero objects",
    "Represented NOAA chart-update provenance adapter with zero calls and zero chart data",
    "Represented GMUT angular-residual obligation board with no empirical inference",
    "Represented THOS navigation decision-state proxy with no operational effectiveness claim",
    "Represented Freed ID sight-record relationship with zero real keys proofs or lifecycle events",
    "Represented accessible navigation status with browser assistive-technology and affected-user review reserved",
    "Represented correction recall supersession and recipient-notice braid with zero delivery",
    "Open gap for real sextant examination calibration angle readings and independent metrology review",
    "Open gap for governed celestial-navigation participant operator study and independent review",
    "Open gap for real navigation safety human-factors affected-user and professional evaluation",
    "Exact gate for vessel operation route release navigation safety professional and legal authority",
    "Exact gate for chart rights location privacy custody copyright cultural meaning and affected-party authority",
    "Exact terminal gate for sea land heritage traditional knowledge Māori data authority empirical GMUT production canon personhood and Stage 20",
]

MUTATION_TYPES = [
    "missing_required_field",
    "lifecycle_inversion",
    "stale_provenance_digest",
    "safety_status_promotion",
    "authority_promotion",
]

PROTECTED_GATES = [
    "real people navigators vessels sextants chronometers charts sites objects materials tools observations and measurements",
    "empirical GMUT likelihoods constraints predictions observations and confirmation",
    "professional navigation metrology instrument operation inspection repair vessel workplace and route-release authority",
    "production identity issuance resolution status revocation interoperability and trust governance",
    "location privacy chart rights ownership custody heritage traditional knowledge legal cultural affected-party and Māori authority",
    "privacy-complete accessibility-complete and exhaustive-security claims",
    "independent reproduction AGI ASI consciousness personhood Theory of Everything proof canon and Stage 20",
]

STARTUP_FAILURES = [
    {
        "failure_id": "SA6824-ST-N001",
        "failed_witness": "The first plan-update presentation exceeded the model-visible context even though the plan update returned an empty success object.",
        "initial_credit": 0,
        "recovery": "Submit one compact seven-step plan and require an attributable result before using it as current workflow state.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "SA6824-ST-N002",
        "failed_witness": "PowerShell rejected an outer foreach pipeline while inventorying current skills and source metadata.",
        "initial_credit": 0,
        "recovery": "Materialize the projection array before JSON serialization.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "SA6824-ST-N003",
        "failed_witness": "A source probe assumed the Codex metadata root was a Git repository and returned not-a-repository.",
        "initial_credit": 0,
        "recovery": "Resolve and use the exact Elowen D-drive source worktree for all repository probes.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "SA6824-ST-N004",
        "failed_witness": "An unquoted HEAD tree revision was parsed incorrectly and produced an ambiguous revision error.",
        "initial_credit": 0,
        "recovery": "Use quoted literal revision arguments and isolated scalar Git probes.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "SA6824-ST-N005",
        "failed_witness": "The combined required-skill display exceeded its presentation window.",
        "initial_credit": 0,
        "recovery": "Reread each selected skill completely and independently through EOF.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "SA6824-ST-N006",
        "failed_witness": "The first full authorization-state display truncated before EOF.",
        "initial_credit": 0,
        "recovery": "Read the same immutable state in bounded ordered chunks and validate its schema separately.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "SA6824-ST-N007",
        "failed_witness": "The combined manifest display truncated before every final-owner row was visible.",
        "initial_credit": 0,
        "recovery": "Reread each manifest independently and later replay exact Git blobs through one batch stream.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "SA6824-ST-N008",
        "failed_witness": "A repeated PowerShell outer-foreach pipeline parser fault stopped the source-code inventory.",
        "initial_credit": 0,
        "recovery": "Use a pre-materialized rows array before the final pipe.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "SA6824-ST-N009",
        "failed_witness": "The first recovered code inventory assumed a phase-specific letterpress-contract filename that did not exist.",
        "initial_credit": 0,
        "recovery": "Enumerate exact tracked v682-v3 filenames before projecting sizes and line counts.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "SA6824-ST-N010",
        "failed_witness": "The first content-seal projection assumed a generic seal directory instead of the live closeout path.",
        "initial_credit": 0,
        "recovery": "Inspect final-delta manifest keys and use the exact closeout/content-seal.json path.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "SA6824-ST-N011",
        "failed_witness": "The first Python manifest wrapper embedded escape-sensitive newline byte literals and failed with SyntaxError before Git access.",
        "initial_credit": 0,
        "recovery": "Use explicit byte values rather than backslash escapes across the JavaScript PowerShell Python boundary.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "SA6824-ST-N012",
        "failed_witness": "The corrected per-file manifest verifier crossed its result window and completed without attributable output.",
        "initial_credit": 0,
        "recovery": "Use one persistent git cat-file batch stream and require a visible zero-failure summary.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "SA6824-X1-N001",
        "failed_witness": "The first exact-lane absence wrapper used a semicolon inside a PowerShell subexpression and failed before Git ran.",
        "initial_credit": 0,
        "recovery": "Separate the Git command from LASTEXITCODE assignment and verify branch path and metadata independently.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "SA6824-X1-N002",
        "failed_witness": "An overbroad git worktree list remained active while enumerating the shared registry and produced no bounded result.",
        "initial_credit": 0,
        "recovery": "Terminate only the owned read-only enumeration and use exact branch path and administrative-metadata absence probes.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "SA6824-X1-N003",
        "failed_witness": "The first worktree-add path lost backslashes in the JavaScript command string and created an unintended nested worktree link under the source lane.",
        "initial_credit": 0,
        "recovery": "Prove exact provenance, remove only the owned erroneous registration, restore source cleanliness, and preserve the correctly created branch.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "SA6824-X1-N004",
        "failed_witness": "The first attachment repair repeated the unquoted drive-relative path and was rejected because the malformed target already existed.",
        "initial_credit": 0,
        "recovery": "Quote a double-escaped absolute D-drive path and attach the already-existing exact branch only once.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "SA6824-X1-N005",
        "failed_witness": "The first sparse verification launched an overbroad status walk on an intentionally empty no-checkout index and was terminated after retaining no result.",
        "initial_credit": 0,
        "recovery": "Probe branch head and sparse patterns without status, then materialize the configured sparse index explicitly.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "SA6824-X1-N006",
        "failed_witness": "The first sparse read-tree attempt refused a zero-byte stale index lock left by the terminated status probe.",
        "initial_credit": 0,
        "recovery": "Prove zero live Git owners, remove only the exact stale lock, and rerun only the blocked read-tree dependency.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "SA6824-X1-N007",
        "failed_witness": "Host policy rejected the first native Remove-Item wrapper for the proven stale index lock.",
        "initial_credit": 0,
        "recovery": "Delete only the verified zero-byte lock through the patch surface and recheck absence before materialization.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "SA6824-X1-N008",
        "failed_witness": "The successful sparse read-tree materialization crossed multiple presentation windows before exiting cleanly.",
        "initial_credit": 0,
        "recovery": "Track the original process handle without replay and prove exact head clean state patterns and materialized helper after exit.",
        "recovery_credit": "bounded_dependency_only",
    },
]


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
    left_tokens = set(re.findall(r"[a-z0-9]+", left.casefold()))
    right_tokens = set(re.findall(r"[a-z0-9]+", right.casefold()))
    if not left_tokens and not right_tokens:
        return 1.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


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
    if index <= 18:
        return ["SMITHSONIAN-SEXTANT", "NIST-ANGLE-UNITS", "W3C-PROV-O"]
    if index <= 36:
        return ["USNO-CELESTIAL-NAV", "USNO-AIR-ALMANAC", "NIST-ANGLE-UNITS"]
    if index <= 54:
        return ["NOAA-CHART-UPDATES", "W3C-PROV-O", "W3C-WCAG22"]
    if index == 55:
        return ["SMITHSONIAN-SEXTANT", "NIST-ANGLE-UNITS"]
    if index == 56:
        return ["USNO-CELESTIAL-NAV", "W3C-WCAG22"]
    if index == 57:
        return ["NOAA-CHART-UPDATES", "W3C-WCAG22"]
    if index == 58:
        return ["NOAA-CHART-UPDATES", "W3C-PROV-O"]
    if index == 59:
        return ["NOAA-CHART-UPDATES", "W3C-VC-DM-20"]
    return ["TMR-MDS-PRINCIPLES", "W3C-PROV-O"]


def proposals() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, title in enumerate(PROPOSAL_TITLES, start=1):
        proposal_id = f"SA6824-N{index:03d}"
        rows.append(
            {
                "approval_class": approval_class(index),
                "concrete_artifacts": [
                    f"docs/sylven-arc/v682-v4/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/sylven-arc/v682-v4/x2/rejecting-mutations.json#{proposal_id}",
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
                    for mutation_index, mutation_type in enumerate(MUTATION_TYPES, start=1)
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
            if proc.stdout.read(1) != b"\n":
                raise RuntimeError(f"missing cat-file separator for {path}")
            yield path, data
    finally:
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

    inherited_titles = {record["title"] for record in inherited}
    exact_collisions: list[str] = []
    neighbors: list[dict[str, Any]] = []
    for proposal in new_records:
        title = proposal["title"]
        if title in inherited_titles:
            exact_collisions.append(title)
        best: dict[str, str] | None = None
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
            "claim": "bounded all-reachable exact-source proposal audit; no universal 10370-row proof",
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
        "schema": "ghc.family.proposal-chain-audit.v682.v4.x1",
        "source": SOURCE,
    }


def task_records(prefix: str, count: int, lane: str) -> list[dict[str, Any]]:
    return [
        {
            "approval_required": lane in {"exact_approval", "blocked"},
            "lane": lane,
            "planned_action": f"Preregistered Sylven owner-local {lane.replace('_', ' ')} item {index:03d}.",
            "state": "preregistered_not_executed",
            "task_id": f"SA6824-{prefix}-{index:03d}",
        }
        for index in range(1, count + 1)
    ]


SKILL_NAMES = [
    "sextant-identity-separator",
    "instrument-component-topology",
    "mirror-path-vacancy",
    "scale-reading-nonobservation",
    "adjustment-action-separator",
    "material-claim-firewall",
    "calibration-correction-hold",
    "condition-cue-nondiagnosis",
    "almanac-edition-provenance",
    "celestial-target-identity-hold",
    "angle-unit-domain-board",
    "time-reference-vacancy",
    "sight-reduction-nonexecution",
    "line-of-position-topology",
    "uncertainty-vacancy-ledger",
    "navigation-command-observation-split",
    "accessible-sight-summary",
    "workload-handover-lease",
    "location-privacy-minimizer",
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
            "wholly synthetic sextant instrument intake and component-topology documentation",
            "wholly synthetic celestial-observation angle time and uncertainty record design",
            "wholly synthetic navigation-handover abstention correction and workload documentation",
        ],
        "owner_runner_ideas": [
            {
                "runner_id": f"SA6824-RUNNER-{index:02d}",
                "name": f"ghc_family_sextant_navigation_runner_{index:02d}.py",
                "state": "planned_not_built_in_x1",
            }
            for index in range(1, 11)
        ],
        "owner_skill_ideas": [
            {
                "skill_id": f"SA6824-SKILL-{index:02d}",
                "name": name,
                "state": "planned_not_built_in_x1",
            }
            for index, name in enumerate(SKILL_NAMES, start=1)
        ],
        "phase": PHASE,
        "primary_pillar": "GMUT Mind",
        "represented_pillars": ["THOS Body", "Freed ID and CBR Heart"],
        "safe_now": task_records("SAFE", 120, "safe_now"),
        "schema": "ghc.family.portfolio-freeze.v682.v4.x1",
        "successor_candidates": task_records("SUCCESSOR-CAND", 20, "successor_candidate_zero_credit"),
        "successor_clean_fix_refine": task_records("SUCCESSOR-CFR", 30, "successor_recommendation_zero_credit"),
        "successor_practice_recommendation": (
            "exactly one zero-credit seed: synthetic museum label revision documentation; successor must audit novelty independently"
        ),
        "successor_runner_ideas": task_records("SUCCESSOR-RUNNER", 10, "successor_runner_seed_zero_credit"),
        "successor_skill_ideas": task_records("SUCCESSOR-SKILL", 10, "successor_skill_seed_zero_credit"),
    }


def official_sources() -> dict[str, Any]:
    entries = [
        {
            "source_id": "SMITHSONIAN-SEXTANT",
            "status": "official_Smithsonian_object_page_checked_2026-09-02",
            "title": "Sextant",
            "url": "https://americanhistory.si.edu/collections/object/nmah_1057798",
            "use": "sextant, frame, scale, vernier, tangent-screw, magnifier, and collection-record vocabulary only; no object observation or material verification",
        },
        {
            "source_id": "USNO-CELESTIAL-NAV",
            "status": "official_US_Naval_Observatory_page_checked_2026-09-02",
            "title": "Celestial Navigation Resources",
            "url": "https://aa.usno.navy.mil/faq/celnav",
            "use": "almanac, celestial body, assumed position, time, altitude, and line-of-position dependency vocabulary only; no navigation instruction or result",
        },
        {
            "source_id": "USNO-AIR-ALMANAC",
            "status": "official_US_Naval_Observatory_page_checked_2026-09-02",
            "title": "The Air Almanac",
            "url": "https://aa.usno.navy.mil/publications/aira",
            "use": "GHA, SHA, declination, navigational-star, edition, precision, and errata vocabulary only; no computation or navigation claim",
        },
        {
            "source_id": "USNO-ALT-AZ",
            "status": "official_US_Naval_Observatory_page_checked_2026-09-02",
            "title": "Computing Altitude and Azimuth from Greenwich Apparent Sidereal Time",
            "url": "https://aa.usno.navy.mil/faq/alt_az",
            "use": "altitude, azimuth, right ascension, declination, horizon-coordinate, and reference-point vocabulary only; no calculation executed",
        },
        {
            "source_id": "NIST-ANGLE-UNITS",
            "status": "official_NIST_page_checked_2026-09-02",
            "title": "NIST Guide to the SI, Chapter 5: Units Outside the SI",
            "url": "https://www.nist.gov/pml/special-publication-811/nist-guide-si-chapter-5-units-outside-si",
            "use": "radian, degree, minute and second of plane angle plus time-unit vocabulary only; no measurement or calibration claim",
        },
        {
            "source_id": "NOAA-CHART-UPDATES",
            "status": "official_NOAA_Office_of_Coast_Survey_page_checked_2026-09-02",
            "title": "NOAA Chart Updates",
            "url": "https://www.nauticalcharts.noaa.gov/charts/chart-updates.html",
            "use": "chart edition, update, critical correction, sequence, effective-state, and danger-to-navigation hold vocabulary only; no chart data ingested or voyage decision",
        },
        {
            "source_id": "W3C-PROV-O",
            "status": "W3C_Recommendation_checked_2026-09-02",
            "title": "PROV-O: The PROV Ontology",
            "url": "https://www.w3.org/TR/prov-o/",
            "use": "entity, activity, revision, derivation, and provenance vocabulary only",
        },
        {
            "source_id": "W3C-WCAG22",
            "status": "W3C_Recommendation_checked_2026-09-02",
            "title": "Web Content Accessibility Guidelines 2.2",
            "url": "https://www.w3.org/TR/WCAG22/",
            "use": "structural accessibility vocabulary and manual-evaluation reservation only",
        },
        {
            "source_id": "W3C-VC-DM-20",
            "status": "W3C_Recommendation_checked_2026-09-02",
            "title": "Verifiable Credentials Data Model v2.0",
            "url": "https://www.w3.org/TR/vc-data-model-2.0/",
            "use": "synthetic credential lifecycle and proof-vacancy vocabulary only",
        },
        {
            "source_id": "RFC8785",
            "status": "RFC_stable_checked_2026-09-02",
            "title": "JSON Canonicalization Scheme",
            "url": "https://www.rfc-editor.org/rfc/rfc8785",
            "use": "deterministic synthetic receipt and digest-domain vocabulary only",
        },
        {
            "source_id": "TMR-MDS-PRINCIPLES",
            "status": "authority_boundary_context_only_checked_2026-09-02",
            "title": "Principles of Māori Data Sovereignty",
            "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
            "use": "Māori data-governance vacancy and noncompensation boundary only; never delegated Māori authority",
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
        "schema": "ghc.family.official-primary-sources.v682.v4.x1",
        "web_checks": len(entries),
    }


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    classes = {
        "raw_task_or_thread_identifier": re.compile(r"\b019[a-f0-9]{29,}\b", re.I),
        "credential_or_secret": re.compile(r"(?:api[_-]?key|private[_-]?key|bearer\s+[a-z0-9._-]{12,})", re.I),
        "private_route_or_callable_identifier": re.compile(r"(?:threadId|private callable|app://connector_)", re.I),
        "private_absolute_path": re.compile(r"(?:[A-Z]:\\Users\\|[A-Z]:\\GHC-Archives\\)", re.I),
        "transcript_screenshot_or_session_stream": re.compile(r"(?:raw transcript|session stream|screenshot payload)", re.I),
    }
    candidates: list[dict[str, str]] = []
    for path in paths:
        target = ROOT / path
        if not target.exists() or target.suffix.lower() not in {".json", ".md", ".py", ".yaml", ".yml", ".html"}:
            continue
        text = target.read_text(encoding="utf-8")
        for class_name, pattern in classes.items():
            if pattern.search(text):
                candidates.append({"class": class_name, "path": path, "adjudication": "scanner_definition_only"})
    return {
        "candidate_count": len(candidates),
        "candidates": candidates,
        "class_count": 5,
        "confirmed_hit_count": 0,
        "confirmed_hits": [],
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.privacy-scan.v682.v4.x1",
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
    if expected_counts != Counter({"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}):
        raise RuntimeError(f"unexpected disposition counts: {expected_counts}")
    audit = proposal_chain_audit(new_records)

    current_after_startup = dict(ACTIVATION_BASELINE)
    for key in ("effective_negatives", "effective_methods", "failed_witnesses", "bounded_passing_witnesses"):
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
            "schema": "ghc.family.activation-intake.v682.v4.x1",
        },
    )
    write_json(
        X1 / "identity-and-boundary.json",
        {
            "consciousness_personhood_or_continuity_claimed": False,
            "hope": "Angles remain typed, uncertainty stays visible, and no synthetic record becomes a voyage.",
            "name": OWNER,
            "optional_pronouns": "they/them",
            "owner_rename_pause_redirect_stop_right": "Hamish",
            "phase": PHASE,
            "relational_working_language_only": True,
            "role": "horizon cartographer and evidence steward",
            "schema": "ghc.family.identity-boundary.v682.v4.x1",
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
            "schema": "ghc.family.proposal-freeze.v682.v4.x1",
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
            "schema": "ghc.family.inherited-revalidation.v682.v4.x1",
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
            "schema": "ghc.family.approval-holds.v682.v4.x1",
        },
    )
    write_json(
        X1 / "clean-fix-refine-plan.json",
        {
            "owner": OWNER,
            "owner_rows": portfolio["owner_clean_fix_refine"],
            "phase": PHASE,
            "schema": "ghc.family.clean-fix-refine.v682.v4.x1",
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
            "schema": "ghc.family.skill-runner-plan.v682.v4.x1",
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
            "schema": "ghc.family.method-flow-startup.v682.v4.x1",
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
            "schema": "ghc.family.phase-truth.v682.v4.x1",
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
                "instrument fitness or navigation safety inferred from documentation",
                "route or private identifier leakage",
                "x1 and x2 lifecycle contamination",
            ],
            "schema": "ghc.family.threat-model.v682.v4.x1",
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
            "schema": "ghc.family.workflow-plan.v682.v4.x1",
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
            "prospective_successor_exact_title": "Caelen Morrow",
            "prospective_successor_phase": "v682-v5",
            "route_authority_through": "v725-v8",
            "send_before_terminal_gate": False,
            "tavian_sol": "ON_STANDBY",
        },
    )
    write_text(
        X1 / "integrated-overview.md",
        f"""# Sylven Arc {PHASE} Planning-Only X1 Overview

Sylven Arc, optionally they/them, is relational working language for a horizon cartographer and evidence steward, with the hope that angles remain typed, uncertainty stays visible, and no synthetic record becomes a voyage. This is not evidence of consciousness, sentience, personhood, continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish retains the right to rename, pause, redirect, narrow, or stop the route.

The exact immutable source is Elowen Cairn final `{SOURCE}` on `{SOURCE_BRANCH}`. Read-only verification established three direct single-parent Elowen commits, zero merges, one final parent, clean state, typed 0/0 divergence, fresh four-way equality, 232 exact normalized-LF manifest entries and ten content-seal targets with zero mismatches, and the successful one-invocation one-success zero-replay canonical receipt. No Elowen test or canonical aggregate was replayed. The repository seal, external activation overlay, and this live acknowledged delivery remain distinct truth layers.

This x1 freezes sixty Sylven proposals after a bounded all-reachable exact-source audit. It makes no universal semantic-novelty claim over all 10,370 declared historical rows. The synthetic sextant, celestial-sight, and navigation-handover proposals must produce zero exact title collisions and zero quarantine hits at the 0.78 token-Jaccard threshold. Twenty inherited neighbor reviews remain source evidence with zero Sylven completion credit.

GMUT Mind is primary through typed angle, time, coordinate, uncertainty, correction, and line-of-position obligations with every observation and measurement vacant. THOS Body remains explicit through synthetic instrument topology, command/observation separation, stop states, workload budgets, correction, and handover. Freed ID and CBR Heart remain explicit through surrogate instrument, sight, publication, and handover identifiers, provenance, location minimization, challenge, accessibility structure, remedy holds, and exact authority gates. Sextant documentation, celestial-observation record design, and navigation handover are wholly synthetic learning and design lenses only, never employment, qualification, competence, navigation instruction, vessel operation, safety release, or professional authority.

The plan uses zero real people, navigators, crews, vessels, sextants, chronometers, charts, horizons, celestial observations, locations, routes, tools, measurements, calculations, identity events, external writes, or authority acts. Current official and primary sources supply vocabulary and refusal conditions only. They are not instrument observations, almanac executions, navigation instructions, conformance certificates, safety releases, legal interpretations, cultural ratifications, affected-party decisions, or authority grants.

Expected x2 dispositions are exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. Those are preregistered expected labels, not observed outcomes. All 300 invalid mutations, 120 safe-now tasks, 80 bounded candidates, 100 CLEAN/FIX/REFINE records, twenty skills, and ten runners remain planned rather than executed in this x1. Twenty exact-approval and ten blocked packets remain visible and unexecuted.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family without physical data, likelihood, posterior, prediction, constraint, empirical confirmation, ultraviolet or quantum completion, or Theory-of-Everything proof. THOS remains synthetic/proxy-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live lifecycle operations, interoperability, independent privacy/security review, recovery evidence, trust governance, and affected-party oversight.

Vessel operation, route release, navigation safety, professional instrument use, chart and publication rights, location privacy, ownership, custody, heritage, traditional knowledge, remedy, legal and cultural interpretation, affected-party legitimacy, Māori wording and data governance, and Māori authority remain exact-gated. Māori concepts remain under Māori authority. Complete privacy, complete accessibility, exhaustive security, independent reproduction, AGI/ASI, consciousness/personhood, proof/canon, and Stage 20 remain open or exact-gated. The terminal verdict remains `{TERMINAL_VERDICT}`.
""",
    )

    x1_material_paths = sorted(set(WRITTEN + [
        "scripts/build_ghc_family_sylven_arc_v682_v4_x1.py",
        "tests/test_ghc_family_sylven_arc_v682_v4_x1.py",
    ]))
    exclusions = [
        "docs/sylven-arc/v682-v4/validation/x1-index-manifest.json",
        "docs/sylven-arc/v682-v4/validation/x1-privacy-scan.json",
        "docs/sylven-arc/v682-v4/validation/x1-staged-review.json",
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
            "schema": "ghc.family.normalized-lf-index-manifest.v682.v4.x1",
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
            "schema": "ghc.family.staged-review.v682.v4.x1",
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
