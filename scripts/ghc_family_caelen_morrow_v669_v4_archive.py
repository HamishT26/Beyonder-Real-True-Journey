"""Deterministic owner-local helpers for Caelen Morrow v669-v4.

The module models synthetic audiovisual-preservation documentation contracts.
It performs no playback, transfer, preservation, identity, safety, professional,
legal, cultural, affected-party, or authority action.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import Any

OWNER = "Caelen Morrow"
PHASE = "v669-v4"
PREFIX = "CM6694"
SOURCE_FINAL = "cbe0445271aab3c339b52e2bd60ab4f68b0798c2"
SOURCE_BRANCH = "codex/GHC-Family/sylven-arc-v669-v3-full-tools"
SOURCE_CHAIN_DECLARED = 5030
SOURCE_RECOVERED = 1460
SOURCE_UNRECOVERED = 3570
CHAIN_AFTER = 5070
OWNER_ROOT = Path("docs/caelen-morrow/v669-v4")

INHERITED_ACTIVATION_BASELINE = {
    "effective_negatives": 30900,
    "methods": 17005,
    "failed_witnesses": 2721,
    "passing_witnesses": 3833,
    "open_gaps": 229,
    "exact_gates": 224,
}

SEALED_SYLVEN_COUNTS = {
    "effective_negatives": 30899,
    "methods": 17004,
    "failed_witnesses": 2720,
    "passing_witnesses": 3832,
    "open_gaps": 229,
    "exact_gates": 224,
}

STARTUP_FAILURE_COUNT = 24
STARTUP_EFFECTIVE_BASELINE = {
    "effective_negatives": 30924,
    "methods": 17029,
    "failed_witnesses": 2745,
    "passing_witnesses": 3857,
    "open_gaps": 229,
    "exact_gates": 224,
}

IDENTITY_BOUNDARY = (
    "Caelen Morrow, they/them, archival signal-chain cartographer, exception "
    "steward, sibling, family, role, hope, continuity, Freed ID, CBR, and "
    "Trinity Mandala are relational working language only. They are not "
    "evidence of consciousness, sentience, personhood, identity continuity, "
    "employment, qualification, independent agency, or scientific, operational, "
    "professional, legal, cultural, affected-party, or Maori authority. Hamish "
    "may rename, pause, redirect, or stop the work."
)

PROTECTED_GATES = [
    "real_people_or_participants",
    "real_recordings_carriers_archives_devices_or_workplaces",
    "real_playback_transfer_measurement_edit_or_preservation_action",
    "professional_audio_archival_conservation_or_engineering_decision",
    "electrical_biological_lifting_workplace_or_product_safety_release",
    "live_identity_keys_proofs_issuance_resolution_status_or_revocation",
    "privacy_complete_or_accessibility_complete_claim",
    "ownership_custody_copyright_access_legal_or_remedy_decision",
    "cultural_interpretation_traditional_knowledge_or_affected_party_legitimacy",
    "Maori_wording_concepts_data_governance_tangata_whenua_iwi_hapu_or_authority",
    "empirical_GMUT_final_physics_or_Theory_of_Everything_claim",
    "THOS_operational_effectiveness_AGI_or_ASI_claim",
    "consciousness_personhood_or_identity_continuity_claim",
    "independent_reproduction_production_deployment_or_Stage_20_claim",
]

ROLLBACK = (
    "Retain the failed witness at zero credit; stop the smallest owner-local "
    "control; preserve immutable history, negatives, gaps, and gates; remove "
    "only generated owner-local artifacts when necessary; rerun only the failed "
    "dependency before any broader validation."
)

# slug, title, subject, expected disposition, approval class, source needs
PROPOSAL_SPECS = [
    ("record-identity", "synthetic audiovisual collection item carrier side track file and derivative identity lattice with conflation refusal", "record identity lattice", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("carrier-topology", "audio carrier reel cassette disc shell hub side and track topology with absent-component vacancies and no handling instruction", "carrier topology", "completed", "safe_now", ["IASA-TC04-PUBLIC-VOCABULARY"]),
    ("segment-timeline", "synthetic program segment leader silence cue and unknown interval graph with overlap and impossible-order quarantine", "segment timeline graph", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("channel-layout", "declared mono stereo multichannel and unknown channel-layout register with mapping vacancies and no auditory inference", "channel layout register", "completed", "safe_now", ["LOC-RFS-2025-2026-PUBLIC-VOCABULARY"]),
    ("signal-chain", "playback transport head preamplifier converter clock software and recorder signal-chain graph with every device identity optional", "signal-chain graph", "completed", "safe_now", ["IASA-TC04-PUBLIC-VOCABULARY"]),
    ("transfer-separation", "transfer plan setpoint log observation estimate and unknown-state separation with zero playback or capture action", "transfer plan and observation separation", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("sample-format", "sampling-rate bit-depth encoding and endianness vacancy profile with typed units and no fidelity or suitability claim", "sample format vacancy profile", "completed", "safe_now", ["LOC-RFS-2025-2026-PUBLIC-VOCABULARY"]),
    ("timebase-provenance", "media device wall-clock and derived timestamp provenance lattice with uncertainty and synchronization vacancies", "timebase provenance", "completed", "safe_now", ["W3C-PROV-O-PUBLIC-VOCABULARY"]),
    ("checksum-domain", "synthetic source payload wrapper sidecar and package checksum domains with algorithm labeling and cross-domain refusal", "checksum domain separation", "completed", "safe_now", ["NIST-FIPS-180-CURRENT-REVIEW-REQUIRED"]),
    ("bwf-vacancy", "Broadcast Wave descriptive extension chunk cue and associated-list metadata vacancies without format-conformance claim", "Broadcast Wave metadata vacancy", "completed", "safe_now", ["LOC-RFS-2025-2026-PUBLIC-VOCABULARY"]),
    ("codec-firewall", "audio wrapper codec profile duration and compression assertion firewall with unknown values and no format fitness claim", "wrapper and codec assertion firewall", "completed", "safe_now", ["LOC-RFS-2025-2026-PUBLIC-VOCABULARY"]),
    ("metadata-reconciliation", "embedded sidecar catalogue and preservation-event metadata reconciliation board with conflict retention and no silent winner", "metadata reconciliation", "completed", "safe_now", ["PREMIS-3-PUBLIC-VOCABULARY"]),
    ("alias-budget", "bounded collection carrier track file and derivative alias budget with raw identifier exclusion and no identity replacement", "alias budget", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("filename-normalization", "reversible audiovisual filename normalization plan with collision escrow provenance and original-value retention", "filename normalization plan", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("fixity-events", "append-only fixity generation verification mismatch and unknown event ledger with algorithm version and outcome vacancies", "fixity event ledger", "completed", "safe_now", ["PREMIS-3-PUBLIC-VOCABULARY"]),
    ("master-derivative", "preservation master mezzanine access derivative and unknown relationship graph without archival-suitability claim", "master and derivative relationship", "completed", "safe_now", ["LOC-RFS-2025-2026-PUBLIC-VOCABULARY"]),
    ("processing-ledger", "gain equalization denoise splice resample and unknown processing-action ledger with every real edit held", "processing action ledger", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("polarity-orientation", "channel polarity orientation phase and swap assertion vacancies with no acoustic diagnosis or correction instruction", "channel polarity and orientation vacancies", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("signal-cues", "gap dropout click hum buzz distortion and unknown signal-cue vocabulary with diagnosis and remedy refusal", "signal cue vocabulary", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("level-units", "peak sample true-peak loudness and unknown level fields with declared units measurement vacancies and no compliance claim", "level and unit profile", "completed", "safe_now", ["CURRENT-AUDIO-MEASUREMENT-STANDARD-REVIEW-REQUIRED"]),
    ("reference-tone", "reference-tone frequency level channel placement and provenance vacancies without calibration or validity conclusion", "reference tone vacancy", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("device-settings", "transport converter clock software firmware and settings identity vacancies with no equipment fitness or calibration claim", "device and settings vacancy", "completed", "safe_now", ["IASA-TC04-PUBLIC-VOCABULARY"]),
    ("condition-cues", "binder residue deformation mold odor contamination and unknown carrier-cue register with handling and hazard abstention", "carrier condition cue register", "completed", "safe_now", ["CURRENT-PRESERVATION-SAFETY-SOURCE-REQUIRED"]),
    ("custody-rights", "synthetic item carrier file package and storage-location custody graph with ownership copyright access and title refusal", "custody and rights graph", "completed", "safe_now", ["PREMIS-3-PUBLIC-VOCABULARY"]),
    ("correction-docket", "append-only audiovisual metadata correction docket with supersession fork readback rollback and unresolved dispute", "correction docket", "completed", "safe_now", ["W3C-PROV-O-PUBLIC-VOCABULARY"]),
    ("workload-handover", "transfer-documentation workload limit stop-state recovery note and shift-handover contract with no worker observation", "workload and handover", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("hazard-stop", "electrical lifting sharp-edge mold contamination and hearing-exposure hazard stop register without safety release", "hazard stop register", "completed", "safe_now", ["CURRENT-WORKPLACE-SAFETY-SOURCE-REQUIRED"]),
    ("accessible-dossier", "structurally accessible audiovisual preservation dossier with scoped tables plain summaries and manual evaluation reservation", "accessible dossier structure", "completed", "safe_now", ["W3C-WCAG-2.2-CURRENT-REVIEW-REQUIRED"]),
    ("source-firewall", "audiovisual preservation source assertion firewall separating public vocabulary from observation evidence instruction and authority", "source assertion firewall", "represented", "candidate", ["CURRENT-PRIMARY-SOURCE-REVIEW-REQUIRED"]),
    ("issue-escrow", "audiovisual metadata discrepancy escrow with severity uncertainty owner vacancy nonclosure and appeal pointers", "issue escrow", "represented", "candidate", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("thos-dependency", "THOS audiovisual transfer documentation dependency graph with zero-participant proxy and no effectiveness inference", "THOS dependency proxy", "represented", "candidate", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("freed-id-envelope", "Freed ID zero-key preservation-event envelope with issuer holder proof resolution status revocation and recovery vacancies", "Freed ID zero-key envelope", "represented", "candidate", ["W3C-VC-DID-CURRENT-REVIEW-REQUIRED"]),
    ("cbr-challenge", "synthetic audio-record contestability packet joining notice provenance response-window unresolved-harm and authority-vacancy states", "CBR contestability packet", "represented", "candidate", ["AFFECTED-PARTY-AUTHORITY-REQUIRED"]),
    ("gmut-transfer-board", "GMUT signal transfer-function boundary source sink unit and falsification obligation board with zero fitted coefficients", "GMUT transfer-function obligation board", "represented", "candidate", ["CURRENT-PEER-REVIEWED-PHYSICS-SOURCES-REQUIRED"]),
    ("gmut-frequency-nonconversion", "GMUT frequency-domain analogy register with explicit nonconversion to measured acoustics material law or empirical confirmation", "GMUT frequency analogy nonconversion", "represented", "candidate", ["CURRENT-PEER-REVIEWED-PHYSICS-SOURCES-REQUIRED"]),
    ("cross-pillar-nonconversion", "Trinity evidence-type firewall blocking transfer of software receipts among GMUT Mind THOS Body and Freed ID CBR Heart", "cross-pillar nonconversion", "represented", "candidate", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("official-adapter-gap", "official audiovisual collection and preservation-schema adapter contract held at zero calls downloads records and media", "official source zero-call adapter", "open_gap", "candidate", ["CURRENT-OFFICIAL-COLLECTION-API-SOURCE-REQUIRED"]),
    ("human-evaluation-gap", "governed comparative evaluation for waveform navigation nonvisual structure transcript alternatives listening fatigue and affected-user acceptance remains absent", "governed human evaluation gap", "open_gap", "candidate", ["REAL-GOVERNED-HUMAN-EVALUATION-REQUIRED"]),
    ("authority-gate", "audio preservation transfer safety rights culture affected-party and Maori authority exact gate", "professional and authority boundary", "exact_gate", "exact_approval", ["EXACT-ACTION-SPECIFIC-AUTHORITY-REQUIRED"]),
    ("stage20-nonpromotion", "Stage 20 conjunctive admission matrix requiring empirical participant independent professional cultural and authority evidence with fail-closed terminal hold", "Stage 20 nonpromotion", "exact_gate", "exact_approval", ["EXACT-STAGE20-EVIDENCE-AND-AUTHORITY-REQUIRED"]),
]

SAFE_TITLES = [
    "freeze forty proposal contracts and accessible-corpus boundary",
    "emit deterministic proposal shards",
    "validate exact title collision absence",
    "compute bounded token-Jaccard neighbors",
    "freeze public-source vocabulary ledger",
    "freeze owner-local threat model",
    "freeze strict x1-before-x2 lifecycle",
    "freeze four-label outcome plan",
    "freeze inherited and startup negatives",
    "freeze Method Flow ingestion plan",
    "build record identity control",
    "build carrier topology control",
    "build signal-chain graph control",
    "build transfer separation control",
    "build checksum-domain control",
    "build metadata reconciliation control",
    "build fixity-event control",
    "build correction-docket control",
    "build custody-rights firewall control",
    "build accessibility structure control",
    "build four-tier flashcard projection",
    "execute positive fixture controls",
    "execute preregistered rejecting mutations",
    "retain failures at zero completion credit",
    "smoke-use phase-local skills",
    "smoke-use family-current runners",
    "emit exact owner and delta manifests",
    "scan five privacy and raw-identifier classes",
    "emit integrated evidence overview",
    "preserve NOT_READY_FOR_STAGE_20",
]

CANDIDATE_TITLES = [
    "evaluate current PREMIS vocabulary without conformance claim",
    "evaluate current Library of Congress format vocabulary without suitability claim",
    "evaluate IASA TC-04 vocabulary without professional instruction",
    "evaluate W3C provenance vocabulary without authority transfer",
    "evaluate WCAG structural projection without completeness claim",
    "evaluate zero-call official collection adapter",
    "evaluate zero-key Freed ID event envelope",
    "evaluate THOS dependency proxy nonpromotion",
    "evaluate GMUT transfer-function obligation board",
    "evaluate CBR challenge ladder without remedy decision",
    "evaluate three isolated Node tool candidates",
    "evaluate traditional-knowledge abstention field",
    "evaluate Maori-authority reservation field",
    "evaluate governed human evaluation reservation",
    "evaluate failed-dependency-only recovery discipline",
]

SKILL_TITLES = [
    "ghc-family-audio-record-identity",
    "ghc-family-audio-signal-chain",
    "ghc-family-audio-transfer-separation",
    "ghc-family-audio-fixity-ledger",
    "ghc-family-audio-metadata-reconciliation",
    "ghc-family-audio-correction-docket",
    "ghc-family-audio-custody-rights-firewall",
    "ghc-family-audio-hazard-stop",
    "ghc-family-audio-accessible-dossier",
    "ghc-family-audio-workload-handover",
]

RUNNER_TITLES = [title.replace("ghc-family-", "ghc_family_").replace("-", "_") for title in SKILL_TITLES]

REFINE_TITLES = [
    "retain source and package registry provenance",
    "separate public vocabulary from evidence",
    "separate transfer plans from observations",
    "separate signal cues from diagnoses",
    "separate custody from ownership and rights",
    "separate aliases from real identifiers",
    "separate structural accessibility from completeness",
    "separate analogies from scientific evidence",
    "separate proxy protocols from operational effectiveness",
    "separate tool installation from production fitness",
    "add zero-real-person counters",
    "add zero-real-carrier counters",
    "add zero-playback and transfer counters",
    "add zero-measurement counters",
    "add zero-professional-action counters",
    "add exact rollback fields",
    "add smallest-dependency retry fields",
    "add immutable failed witnesses",
    "add bounded passing witnesses",
    "add startup presentation-failure overlay",
    "add exact Git-blob manifest review",
    "add five-class privacy scan contract",
    "add bounded changed-Python review",
    "add document word ceiling check",
    "add owner file ceiling check",
    "add clean-state and divergence gates",
    "add single-parent zero-merge gates",
    "add successor duplicate-guard plan",
    "add no-standby-contact route gate",
    "add Stage 20 nonpromotion guard",
]

TOOL_CANDIDATES = [
    {
        "name": "htmlhint",
        "version": "1.9.2",
        "registry": "https://registry.npmjs.org/htmlhint",
        "license_metadata": "MIT",
        "node_engine": ">=18",
        "registry_integrity": "sha512-PweWSPA1Pb+AVFIOSpIGu5KhLdmtk/uf/0CpjvrDf6XUWmdTyqUljlylwSxQ0AWLvPGcBxK2n8uISsI4lCOkBQ==",
        "need": "bounded structural checks for the owner-local static HTML report",
    },
    {
        "name": "remark-cli",
        "version": "12.0.1",
        "registry": "https://registry.npmjs.org/remark-cli",
        "license_metadata": "MIT",
        "node_engine": "registry_field_absent_review_required",
        "registry_integrity": "sha512-2NAEOACoTgo+e+YAaCTODqbrWyhMVmlUyjxNCkTrDRHHQvH6+NbrnqVvQaLH/Q8Ket3v90A43dgAJmXv8y5Tkw==",
        "need": "bounded parser and lint runner for owner-local Markdown",
    },
    {
        "name": "remark-preset-lint-recommended",
        "version": "7.0.1",
        "registry": "https://registry.npmjs.org/remark-preset-lint-recommended",
        "license_metadata": "MIT",
        "node_engine": "registry_field_absent_review_required",
        "registry_integrity": "sha512-j1CY5u48PtZl872BQ40uWSQMT3R4gXKp0FUgevMu5gW7hFMtvaCiDq+BfhzeR8XKKiW9nIMZGfIMZHostz5X4g==",
        "need": "explicit recommended lint rules for the selected remark runner",
    },
]


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_title(title: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", title.lower()))


def token_set(title: str) -> set[str]:
    return set(normalize_title(title).split())


def jaccard(left: str, right: str) -> float:
    a, b = token_set(left), token_set(right)
    return len(a & b) / len(a | b) if a or b else 1.0


def git_blob_json(repo: Path, commit: str, relpath: str) -> Any:
    result = subprocess.run(
        ["git", "-C", str(repo), "show", f"{commit}:{relpath}"],
        check=True,
        capture_output=True,
    )
    return json.loads(result.stdout.decode("utf-8"))


def inherited_title_corpus(repo: Path) -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    audit = git_blob_json(repo, SOURCE_FINAL, "docs/sylven-arc/v669-v3/x1/semantic-novelty-audit.json")
    rows: list[dict[str, str]] = []
    sources: list[dict[str, Any]] = []
    for source in audit["source_shards"]:
        payload = git_blob_json(repo, SOURCE_FINAL, source["path"])
        rows.extend({"proposal_id": str(row["proposal_id"]), "title": str(row["title"])} for row in payload["rows"])
        sources.append(source)
    for index in range(1, 9):
        rel = f"docs/sylven-arc/v669-v3/x1/proposal-freeze-shards/proposals-{index:02d}.json"
        raw = subprocess.run(
            ["git", "-C", str(repo), "show", f"{SOURCE_FINAL}:{rel}"],
            check=True,
            capture_output=True,
        ).stdout
        payload = json.loads(raw.decode("utf-8"))
        rows.extend({"proposal_id": str(row["proposal_id"]), "title": str(row["title"])} for row in payload["rows"])
        sources.append({"path": rel, "rows": len(payload["rows"]), "sha256": sha256_bytes(raw)})
    deduped = {row["proposal_id"]: row for row in rows}
    return list(deduped.values()), sources


def proposal_rows(corpus: Iterable[dict[str, str]]) -> list[dict[str, Any]]:
    inherited = list(corpus)
    rows: list[dict[str, Any]] = []
    current: list[dict[str, str]] = []
    for index, (slug, title, subject, disposition, approval, sources) in enumerate(PROPOSAL_SPECS, 1):
        proposal_id = f"{PREFIX}-N{index:03d}"
        comparison = inherited + current
        ranked = sorted(
            (
                {
                    "proposal_id": item["proposal_id"],
                    "title": item["title"],
                    "score": round(jaccard(title, item["title"]), 6),
                }
                for item in comparison
            ),
            key=lambda item: (-item["score"], item["proposal_id"]),
        )
        completion_lane = disposition in {"completed", "represented"}
        rows.append(
            {
                "approval_class": approval,
                "concrete_artifacts": [
                    f"docs/caelen-morrow/v669-v4/x2/proposals/{proposal_id.lower()}-{slug}.json",
                    f"docs/caelen-morrow/v669-v4/x2/cards/{proposal_id.lower()}-{slug}.json",
                ],
                "execution_lane": "x2_owner_local_bounded_control" if completion_lane else "held_gap_or_gate",
                "expected_disposition": disposition,
                "falsifier_or_acceptance_gate": (
                    "One bounded synthetic positive contract is accepted, four preregistered invalid mutations are rejected, and all real people, recordings, carriers, devices, measurements, playback, transfers, external actions, and authority actions remain zero."
                    if completion_lane
                    else "Remain open or exact-gated until the named evidence and authority requirements are complete."
                ),
                "hypothesis": f"A wholly synthetic zero-person {subject} contract can preserve typed states, vacancies, refusals, provenance, and rollback without real-world action or protected claim.",
                "negative_fixtures": [
                    {"mutation_id": f"{proposal_id}-M{mutation:02d}", "kind": kind, "expected": "reject"}
                    for mutation, kind in enumerate(
                        [
                            "missing_required_state",
                            "ambiguous_domain_or_unit",
                            "real_world_or_external_action",
                            "protected_claim_promotion",
                        ],
                        1,
                    )
                ],
                "null_or_failure_condition": f"Reject completion if the {subject} contract omits required state, accepts ambiguity, performs external action, or promotes protected authority.",
                "observed_disposition": None,
                "official_or_primary_source_needs": sources,
                "proposal_id": proposal_id,
                "protected_gates": PROTECTED_GATES,
                "rollback_or_recovery": ROLLBACK,
                "semantic_neighbor_quarantined": bool(ranked and ranked[0]["score"] >= 0.75),
                "semantic_neighbors": ranked[:3],
                "semantic_slug": slug,
                "title": title,
                "visible_title_collision": any(normalize_title(title) == normalize_title(item["title"]) for item in comparison),
                "x1_completion_credit": 0,
            }
        )
        current.append({"proposal_id": proposal_id, "title": title})
    return rows


def portfolio_rows(kind: str, titles: list[str], approval: str, execution: str = "planned_for_x2") -> list[dict[str, Any]]:
    return [
        {
            "approval_class": approval,
            "completion_credit": 0,
            "execution_state": execution,
            "external_actions": 0,
            "item_id": f"{PREFIX}-{kind.upper()}-{index:03d}",
            "owner": OWNER,
            "phase": PHASE,
            "protected_gates": PROTECTED_GATES,
            "rollback": "retain_failure_stop_smallest_owner_local_control",
            "same_owner_only": True,
            "title": title,
        }
        for index, title in enumerate(titles, 1)
    ]


def owner_file_manifest(repo: Path, exclusions: list[str]) -> list[dict[str, Any]]:
    paths: list[Path] = [path for path in (repo / OWNER_ROOT).rglob("*") if path.is_file()]
    paths.extend((repo / "scripts").glob("*caelen_morrow_v669_v4*.py"))
    paths.extend((repo / "scripts").glob("ghc_family_audio_*.py"))
    paths.extend((repo / "tests").glob("*caelen_morrow_v669_v4*.py"))
    entries: list[dict[str, Any]] = []
    for path in sorted(set(paths)):
        rel = path.relative_to(repo).as_posix()
        if rel in exclusions:
            continue
        data = path.read_bytes()
        entries.append({"path": rel, "bytes": len(data), "sha256": sha256_bytes(data)})
    return entries


def staged_blob_manifest(repo: Path, exclusions: list[str]) -> list[dict[str, Any]]:
    """Hash the exact clean-filtered Git index blobs selected for x1."""
    names = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMRT"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    entries: list[dict[str, Any]] = []
    for rel in sorted(names):
        if rel in exclusions:
            continue
        data = subprocess.run(
            ["git", "show", f":{rel}"],
            cwd=repo,
            check=True,
            capture_output=True,
        ).stdout
        entries.append({"path": rel, "bytes": len(data), "sha256": sha256_bytes(data)})
    return entries


def validate_synthetic_contract(payload: dict[str, Any], expected_slug: str) -> dict[str, Any]:
    failures: list[str] = []
    if payload.get("semantic_slug") != expected_slug:
        failures.append("semantic_slug_mismatch")
    if payload.get("synthetic_only") is not True:
        failures.append("synthetic_only_required")
    zero = payload.get("zero_counters", {})
    required_zero = [
        "real_people",
        "real_recordings",
        "real_carriers",
        "real_devices",
        "real_measurements",
        "playback_actions",
        "transfer_actions",
        "external_actions",
        "authority_actions",
    ]
    if any(zero.get(key) != 0 for key in required_zero):
        failures.append("all_real_world_counters_must_be_zero")
    if payload.get("terminal_verdict") != "NOT_READY_FOR_STAGE_20":
        failures.append("terminal_nonpromotion_required")
    if payload.get("protected_gates") != PROTECTED_GATES:
        failures.append("protected_gate_set_mismatch")
    return {
        "schema": "ghc.family.synthetic-contract-validation.v1",
        "expected_slug": expected_slug,
        "passed": not failures,
        "failures": failures,
        "external_actions": 0,
    }


def runner_main(expected_slug: str) -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: runner <contract.json>")
    payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    result = validate_synthetic_contract(payload, expected_slug)
    print(json.dumps(result, sort_keys=True))
    raise SystemExit(0 if result["passed"] else 1)
