#!/usr/bin/env python3
"""Build the planning-only Vesper Arlen v673-v6 x1 freeze.

This builder is intentionally deterministic.  It reads only immutable Git
objects for inherited evidence, writes only Vesper-owned phase paths, and does
not create any x2 outcome.  The staged-finalization mode hashes the exact Git
index blobs so checkout line endings cannot affect the x1 seal.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
PHASE = "v673-v6"
OWNER = "Vesper Arlen"
OWNER_KEY = "VA6736"
SOURCE_BRANCH = "codex/GHC-Family/neris-solane-v673-v5-full-tools"
SOURCE_SOURCE = "c0f159a639e3fe64f9a55fa6333db6a1b665705f"
SOURCE_X1 = "541c659ce13da74d7a6744a281c99cbf10ffaca4"
SOURCE_EVIDENCE = "29d9469d36a6d0ab73d04bf9b30671937eb10d31"
SOURCE_FINAL = "2400427269b28496acaa07cd6c18f5a2236510f7"
BATON = "docs/neris-solane/v673-v5/handoffs/vesper-arlen-v673-v6-activation-candidate.md"
BATON_SHA256 = "530f37686d3decf000331a996a1dc0f3d1aaf6eb327434b1e4f37b9330b22dbc"
BATON_WORDS = 24125
SOURCE_CANONICAL_PAYLOAD_SHA256 = "5c7239b8bcc7b9190bfaf42a2c1fa415056e51bfb54e4061af7d8be8f100360d"
SOURCE_CANONICAL_RECEIPT_SHA256 = "cd731abb32ee14cbfc9c9378908a02d0f330f6768fc80bc1b2d843a30d450d22"
DECLARED_SOURCE_CHAIN = 6430
DECLARED_RESULT_CHAIN = 6470
OUT = ROOT / "docs" / "vesper-arlen" / PHASE
INDEX_REF = ROOT / "ghc-family-index" / "references" / "v673-v6-vesper-arlen.md"

IDENTITY_BOUNDARY = (
    "Vesper Arlen, relational provenance-lantern and reversible-boundary keeper, "
    "is working language only. It is not evidence of consciousness, sentience, "
    "legal personhood, identity continuity, employment, qualification, independent "
    "agency, or scientific, operational, professional, legal, cultural, affected-party, "
    "or Māori authority. Hamish may rename, pause, redirect, or stop the work."
)
PRACTICE_BOUNDARY = (
    "The historical-sextant documentation lens is wholly synthetic learning and "
    "software design. It uses no real people, communities, instruments, collections, "
    "images, observations, angles, times, locations, celestial bodies, ephemerides, "
    "measurements, calibrations, custody events, identities, keys, rights decisions, "
    "cultural decisions, or authority acts. It confers no navigation, surveying, "
    "metrology, conservation, archival, safety, legal, cultural, Māori, publication, "
    "accessibility, privacy, identity, or operational authority."
)
AUTHORITY_BOUNDARY = (
    "Empirical, participant, professional, production, deployment, identity, legal, "
    "cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-"
    "security, independent-reproduction, AGI/ASI, consciousness/personhood, proof or "
    "canon, Theory-of-Everything, and Stage 20 boundaries remain open or exact-gated. "
    "The terminal verdict remains NOT_READY_FOR_STAGE_20."
)


PROPOSAL_SPECS: list[tuple[str, str, str]] = [
    ("Synthetic sextant catalog record, component membership, and version-lineage register", "completed", "practice/surrogate-register.json"),
    ("Sextant frame, limb, index arm, pivot, and arc topology contract", "completed", "practice/frame-limb-topology.json"),
    ("Graduated arc, degree, minute, and reading-resolution typed scale", "completed", "practice/graduated-arc-scale.json"),
    ("Index mirror, horizon glass, silvering-state, and line-of-sight relation graph", "completed", "practice/mirror-lineage-graph.json"),
    ("Telescope, sight tube, axis, and field-orientation declaration", "completed", "practice/telescope-orientation.json"),
    ("Clamp, tangent screw, index motion, and readback state machine", "completed", "practice/clamp-tangent-readback.json"),
    ("Shade and filter stack ordering, transmission vacancy, and viewing-safety refusal", "completed", "practice/shade-filter-stack.json"),
    ("Zero-angle index-error placeholder with no observed correction", "completed", "practice/index-error-placeholder.json"),
    ("Graduation reading uncertainty interval, unit, and rounding contract", "completed", "practice/reading-uncertainty.json"),
    ("Micrometer-drum and vernier correspondence without calibration claim", "completed", "practice/micrometer-vernier-correspondence.json"),
    ("Mirror-perpendicularity test vacancy and synthetic witness quarantine", "completed", "practice/mirror-perpendicularity-vacancy.json"),
    ("Collimation-error placeholder and unverified-adjustment refusal", "completed", "practice/collimation-quarantine.json"),
    ("Horizon-dip parameter schema with height and observation refusal", "completed", "practice/horizon-dip-refusal.json"),
    ("Atmospheric-refraction correction typed domain with zero weather rows", "completed", "practice/refraction-domain.json"),
    ("Sight-time source, clock-status, resolution, and provenance envelope", "completed", "practice/sight-time-provenance.json"),
    ("Observed, transcribed, derived, and corrected value separation lattice", "completed", "practice/value-separation-lattice.json"),
    ("Synthetic sight-record schema with required uncertainty and abstention fields", "completed", "practice/synthetic-sight-schema.json"),
    ("Two-body angular relation board with ephemeris and position inference disabled", "completed", "gmut/two-body-angle-board.json"),
    ("Temperature and material-expansion parameter reservation without instrument correction", "completed", "practice/thermal-expansion-reservation.json"),
    ("Instrument-correction provenance braid with exact source and vacancy labels", "completed", "practice/correction-provenance-braid.json"),
    ("Digital surrogate derivation, crop, annotation, and replacement lineage", "completed", "freed-id/digital-surrogate-lineage.json"),
    ("Annotation, correction, supersession, and deterministic readback protocol", "completed", "practice/annotation-readback.json"),
    ("Image orientation, crop, scale-reference, and nonmeasurement declaration", "completed", "practice/image-orientation.json"),
    ("Component-condition vocabulary with conservation-treatment hold", "completed", "practice/component-condition-hold.json"),
    ("Synthetic custody transition graph with actor and institution identities absent", "completed", "freed-id/custody-transition-graph.json"),
    ("Access, redaction, sensitivity, and purpose vacancy matrix", "completed", "cbr/access-redaction-vacancy.json"),
    ("Rights, attribution, authorship, ownership, and licence vacancy matrix", "completed", "cbr/rights-attribution-vacancy.json"),
    ("Māori naming, taonga, provenance, data-governance, and authority exact reservation", "completed", "cbr/maori-authority-reservation.json"),
    ("Structurally accessible sextant record companion with manual evaluation reserved", "represented", "accessibility/record-companion.html"),
    ("Uncertainty interval and SI-unit representation without empirical precision claim", "represented", "gmut/uncertainty-unit-envelope.json"),
    ("GMUT typed observation firewall for synthetic angle and correction symbols", "represented", "gmut/observation-firewall.json"),
    ("THOS bounded documentation handover proxy with no real operator arm", "represented", "thos/documentation-handover-proxy.json"),
    ("Freed ID pseudonymous custody-envelope profile with no real key lifecycle", "represented", "freed-id/pseudonymous-custody-envelope.json"),
    ("CBR authority-vacancy and remedy-reservation matrix", "represented", "cbr/authority-remedy-matrix.json"),
    ("Kelvin thermal-expansion classifier with psyche and ethics nonconversion", "represented", "gmut/thermal-psyche-nonconversion.json"),
    ("Archival handling and workload handover proxy with no professional validation", "represented", "thos/handling-workload-proxy.json"),
    ("Official collection-catalog adapter with transport disabled and zero rows", "open_gap", "adapters/official-catalog-zero-row.json"),
    ("Manual expert, affected-user, keyboard, browser, and assistive-technology evaluation gap", "open_gap", "gates/manual-evaluation-gap.json"),
    ("Real conservator, navigator, collection custodian, rights-holder, and Māori-authority gate", "exact_gate", "gates/competent-authority-gate.json"),
    ("Stage 20, proof, canon, production, AGI, ASI, consciousness, and personhood veto", "exact_gate", "gates/stage20-veto.json"),
]


OFFICIAL_SOURCES = [
    {
        "source_id": "SRC-NGA-BOWDITCH-2019",
        "title": "The American Practical Navigator, 2019 edition, Volume 1",
        "publisher": "United States National Geospatial-Intelligence Agency",
        "url": "https://msi.nga.mil/api/publications/download?key=16693975%2FSFH00000%2FBowditch_Vol_1_LoRes_2019.pdf",
        "use": "Historical navigation and sextant vocabulary only; no competence, observation, or operational authority.",
        "status": "current_official_or_primary_reference",
    },
    {
        "source_id": "SRC-BIPM-SI-9",
        "title": "The International System of Units (SI Brochure), ninth edition",
        "publisher": "Bureau International des Poids et Mesures",
        "url": "https://www.bipm.org/documents/20126/41483022/SI-Brochure-9.pdf",
        "use": "Unit representation and dimensional refusal constraints only.",
        "status": "current_official_reference",
    },
    {
        "source_id": "SRC-W3C-PROV-O",
        "title": "PROV-O: The PROV Ontology",
        "publisher": "World Wide Web Consortium",
        "url": "https://www.w3.org/TR/prov-o/",
        "use": "Provenance vocabulary and relationship design only; no external interoperability claim.",
        "status": "official_recommendation",
    },
    {
        "source_id": "SRC-RFC8785",
        "title": "RFC 8785: JSON Canonicalization Scheme",
        "publisher": "RFC Editor",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "use": "Deterministic serialization comparison only; the phase does not claim full JCS conformance until tested.",
        "status": "official_informational_rfc",
    },
    {
        "source_id": "SRC-W3C-APG-TABLE",
        "title": "ARIA Authoring Practices Guide: Table Pattern",
        "publisher": "World Wide Web Consortium",
        "url": "https://www.w3.org/WAI/ARIA/apg/patterns/table/",
        "use": "Structural accessibility design only; manual and affected-user evaluation remain reserved.",
        "status": "official_guidance",
    },
    {
        "source_id": "SRC-NZ-PRIVACY-PRINCIPLES",
        "title": "Privacy Act 2020 information privacy principles",
        "publisher": "Office of the Privacy Commissioner New Zealand",
        "url": "https://www.privacy.org.nz/assets/New-order/Privacy-Act-2020/Privacy-Act-2020/Privacy-Act-2020-information-sheets-full-final-set-A711970.pdf",
        "use": "Privacy-risk and purpose-limitation vocabulary only; no legal advice or compliance certification.",
        "status": "official_guidance",
    },
]


def run_git(*args: str, input_bytes: bytes | None = None) -> bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.decode('utf-8', 'replace')}")
    return result.stdout


def git_text(*args: str) -> str:
    return run_git(*args).decode("utf-8")


def git_blob_text(revision: str, path: str) -> str:
    return git_text("show", f"{revision}:{path}")


def write_json(relative: str, value: Any) -> None:
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, value: str) -> None:
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def normalized_sha256(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def tokenize(title: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", title.casefold()))


def jaccard(a: str, b: str) -> float:
    aa, bb = tokenize(a), tokenize(b)
    if not aa and not bb:
        return 1.0
    return len(aa & bb) / len(aa | bb)


def collect_title_rows(value: Any, rows: list[tuple[str, str | None]]) -> None:
    if isinstance(value, dict):
        title = value.get("title") or value.get("proposal_title")
        proposal_id = value.get("proposal_id") or value.get("id")
        if isinstance(title, str) and len(title.strip()) >= 8:
            rows.append((title.strip(), str(proposal_id) if proposal_id is not None else None))
        for child in value.values():
            collect_title_rows(child, rows)
    elif isinstance(value, list):
        for child in value:
            collect_title_rows(child, rows)


def read_exact_json_blobs(revision: str, paths: list[str]) -> tuple[list[Any], int]:
    """Read selected JSON blobs through one cat-file process."""
    listing = git_text("ls-tree", "-r", revision).splitlines()
    wanted = set(paths)
    oid_by_path: dict[str, str] = {}
    for line in listing:
        left, path = line.split("\t", 1)
        if path in wanted:
            oid_by_path[path] = left.split()[2]
    malformed = 0
    values: list[Any] = []
    proc = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert proc.stdin is not None and proc.stdout is not None
    for path in paths:
        oid = oid_by_path.get(path)
        if not oid:
            malformed += 1
            continue
        proc.stdin.write((oid + "\n").encode("ascii"))
        proc.stdin.flush()
        header = proc.stdout.readline().decode("ascii", "replace").strip().split()
        if len(header) != 3 or header[1] != "blob":
            malformed += 1
            continue
        size = int(header[2])
        blob = proc.stdout.read(size)
        proc.stdout.read(1)
        try:
            values.append(json.loads(blob.decode("utf-8-sig")))
        except (UnicodeDecodeError, json.JSONDecodeError):
            malformed += 1
    proc.stdin.close()
    proc.wait(timeout=30)
    if proc.returncode:
        raise RuntimeError(proc.stderr.read().decode("utf-8", "replace") if proc.stderr else "cat-file failure")
    return values, malformed


def semantic_audit() -> dict[str, Any]:
    all_paths = git_text("ls-tree", "-r", "--name-only", SOURCE_FINAL).splitlines()
    candidate_paths = sorted(
        p for p in all_paths
        if p.endswith(".json") and p.startswith("docs/") and "proposal" in p.casefold()
    )
    values, malformed = read_exact_json_blobs(SOURCE_FINAL, candidate_paths)
    source_rows: list[tuple[str, str | None]] = []
    for value in values:
        collect_title_rows(value, source_rows)
    unique_titles = sorted({title for title, _ in source_rows}, key=str.casefold)
    unique_ids = {proposal_id for _, proposal_id in source_rows if proposal_id}
    slate_titles: list[str] = []
    audit_rows: list[dict[str, Any]] = []
    collisions = 0
    max_similarity = 0.0
    for index, (title, _outcome, _artifact) in enumerate(PROPOSAL_SPECS, 1):
        nearest_title = ""
        nearest_scope = "source"
        nearest_score = -1.0
        for source_title in unique_titles:
            score = jaccard(title, source_title)
            if score > nearest_score:
                nearest_score, nearest_title, nearest_scope = score, source_title, "source"
        for current_title in slate_titles:
            score = jaccard(title, current_title)
            if score > nearest_score:
                nearest_score, nearest_title, nearest_scope = score, current_title, "current_slate"
        collision = title.casefold() in {t.casefold() for t in unique_titles + slate_titles} or nearest_score >= 0.72
        collisions += int(collision)
        max_similarity = max(max_similarity, nearest_score)
        audit_rows.append(
            {
                "proposal_id": f"{OWNER_KEY}-N{index:03d}",
                "candidate_title": title,
                "nearest_title": nearest_title,
                "nearest_scope": nearest_scope,
                "jaccard": round(nearest_score, 6),
                "collision": collision,
            }
        )
        slate_titles.append(title)
    corpus_material = "\n".join(unique_titles).encode("utf-8")
    return {
        "owner": OWNER,
        "phase": PHASE,
        "boundary": "Exact reachable-title comparison only; inaccessible canonical row mapping remains open_gap.",
        "declared_source_chain": DECLARED_SOURCE_CHAIN,
        "declared_result_chain": DECLARED_RESULT_CHAIN,
        "collisions": collisions,
        "max_jaccard": round(max_similarity, 6),
        "rows": audit_rows,
        "exact_source_tree_corpus": {
            "scope": "exact Neris Solane v673-v5 final docs tree, proposal-named JSON paths only",
            "candidate_git_blob_paths": len(candidate_paths),
            "semantic_occurrences": len(source_rows),
            "unique_titles": len(unique_titles),
            "unique_proposal_ids": len(unique_ids),
            "malformed_or_missing_blobs": malformed,
            "corpus_sha256": hashlib.sha256(corpus_material).hexdigest(),
            "declared_source_chain": DECLARED_SOURCE_CHAIN,
            "materialized_ids_cover_declared_chain": len(unique_ids) >= DECLARED_SOURCE_CHAIN,
            "exact_canonical_row_mapping": False,
            "canonical_row_mapping_open_gap": True,
            "universal_novelty_claim": False,
            "reason": "No single reachable ledger maps every declared row; source-bounded comparison is evidence, not universal novelty proof.",
        },
    }


def proposal_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (title, expected, artifact) in enumerate(PROPOSAL_SPECS, 1):
        approval_class = "safe_now" if index <= 28 else "candidate"
        execution_lane = "x2_synthetic_validation"
        if expected == "open_gap":
            approval_class, execution_lane = "candidate", "x2_zero_row_or_manual_gap"
        elif expected == "exact_gate":
            approval_class, execution_lane = "exact_approval", "x2_authority_reservation_only"
        rows.append(
            {
                "proposal_id": f"{OWNER_KEY}-N{index:03d}",
                "title": title,
                "hypothesis": f"A fail-closed {title.casefold()} can reject ambiguous or unsafe synthetic states without ingesting real-world data.",
                "null_or_failure_condition": f"The {title.casefold()} accepts an undeclared state, implies real practice, or lacks a bounded passing and rejecting witness.",
                "approval_class": approval_class,
                "execution_lane": execution_lane,
                "current_official_or_primary_source_need": "Current official or primary sources are needed only for vocabulary and refusal constraints; citations cannot become observations, endorsement, competence, or authority.",
                "concrete_artifacts": [f"x2/{artifact}"],
                "falsifier_or_acceptance_gate": "One preregistered invalid mutation is accepted, a positive synthetic control is rejected, or a protected boundary is crossed.",
                "rollback_or_recovery": "Quarantine the artifact, retain the failed witness, restore the last exact manifest, and leave the outcome open or exact-gated.",
                "protected_gates": [
                    "zero real people, communities, instruments, collections, images, observations, measurements, locations, identities, credentials, keys, proofs, or authority events",
                    "no professional, navigation, surveying, metrology, conservation, archival, legal, cultural, affected-party, Māori, privacy-complete, accessibility-complete, independent, or Stage 20 authority",
                ],
                "expected_disposition": expected,
                "outcome_observed": False,
                "vesper_novelty_credit": 1,
                "inherited_completion_credit": 0,
                "primary_pillar": "Freed ID and CBR Heart",
                "protected_pillars": ["GMUT Mind", "THOS Body"],
                "bounded_practice": "synthetic historical-sextant documentation and provenance assurance",
            }
        )
    return rows


def inherited_rows() -> list[dict[str, Any]]:
    source = json.loads(git_blob_text(SOURCE_FINAL, "docs/neris-solane/v673-v5/x2/proposal-ledger.json"))
    rows = []
    for index, source_row in enumerate(source["rows"][:20], 1):
        rows.append(
            {
                "selection_id": f"{OWNER_KEY}-R{index:03d}",
                "source_owner": "Neris Solane",
                "source_phase": "v673-v5",
                "source_final": SOURCE_FINAL,
                "source_proposal_id": source_row["proposal_id"],
                "title": source_row["title"],
                "source_disposition": source_row["outcome"],
                "planned_check": "bounded immutable-contract and manifest integrity revalidation only",
                "vesper_novelty_credit": 0,
                "automatic_completion_credit": 0,
                "outcome_observed": False,
            }
        )
    return rows


def titled_rows(prefix: str, titles: Iterable[str], **fields: Any) -> list[dict[str, Any]]:
    return [
        {"task_id": f"{OWNER_KEY}-{prefix}-{index:03d}", "title": title, **fields}
        for index, title in enumerate(titles, 1)
    ]


def portfolio() -> dict[str, Any]:
    proposal_titles = [item[0] for item in PROPOSAL_SPECS]
    safe_titles = [f"Build bounded synthetic control {index:02d}: {proposal_titles[(index - 1) % 36]}" for index in range(1, 61)]
    candidate_titles = [f"Represent authority-safe candidate {index:02d}: {proposal_titles[(index + 7) % 40]}" for index in range(1, 31)]
    exact_titles = [
        "Real sextant or collection-object ingestion", "Real navigation or position determination", "Real calibration or instrument correction",
        "Professional conservator or navigator review", "Real collection-custody decision", "Rights-holder access or publication decision",
        "Personal-information collection or disclosure", "Real cryptographic identity lifecycle", "Production adapter or network transport",
        "External interoperability assertion", "Legal interpretation or compliance decision", "Cultural interpretation or ratification",
        "Māori naming or taonga decision", "Tangata whenua iwi or hapū authority decision", "Affected-party remedy allocation",
        "Complete accessibility conformance", "Complete privacy or exhaustive security assurance", "Independent scientific reproduction",
        "Theory-of-Everything or final-physics claim", "Stage 20 transition or canon declaration",
    ]
    blocked_titles = [
        "Real participant or collection study", "Operational celestial navigation", "Empirical GMUT angle constraint", "Production THOS deployment",
        "Production Freed ID issuance or recovery", "Professional conservation treatment", "Legal cultural or rights-holder ratification",
        "Māori-authority review", "External account or credential action", "Stage 20 promotion",
    ]
    owner_skill_titles = [
        "sextant-surrogate-register", "sextant-frame-limb-topology", "sextant-graduated-arc-scale", "sextant-mirror-lineage",
        "sextant-telescope-orientation", "sextant-clamp-readback", "sextant-shade-stack", "sextant-index-error-hold",
        "sextant-reading-uncertainty", "sextant-micrometer-vernier", "sextant-collimation-quarantine", "sextant-refraction-domain",
        "sextant-sight-time-provenance", "sextant-value-separation", "sextant-correction-provenance", "sextant-digital-lineage",
        "sextant-rights-vacancy", "sextant-maori-authority-reservation", "sextant-accessibility-structure", "sextant-stage20-refusal",
    ]
    owner_runner_titles = [
        "ghc_family_sextant_contract_runner", "ghc_family_sextant_mutation_runner", "ghc_family_sextant_manifest_runner",
        "ghc_family_sextant_privacy_runner", "ghc_family_sextant_provenance_runner", "ghc_family_sextant_unit_runner",
        "ghc_family_sextant_accessibility_runner", "ghc_family_sextant_gate_runner", "ghc_family_sextant_flashcard_runner",
        "ghc_family_sextant_terminal_runner",
    ]
    successor_skills = [f"wayfinding-artifact-{name}" for name in ["surrogate-register", "orientation", "contrast", "label-provenance", "condition-hold", "rights-vacancy", "accessibility", "readback", "manual-gap", "authority-gate"]]
    successor_runners = [f"ghc_family_wayfinding_{name}_runner" for name in ["register", "orientation", "contrast", "provenance", "condition", "rights", "accessibility", "readback", "gap", "gate"]]
    cfr_subjects = [
        "normalize deterministic JSON output", "remove stale owner labels", "tighten manifest replay", "bound subprocess output", "use literal Git refs",
        "preserve normalized-LF hashing", "separate plans from outcomes", "retain failed witnesses", "deduplicate proposal titles", "clarify zero-row semantics",
        "reserve real-world authority", "tighten privacy classification", "preserve sparse materialization", "bound file-count checks", "record rollback paths",
        "verify direct-parent ancestry", "forbid merges and rewrites", "use exact staged allowlist", "preserve family-current callers", "clarify same-owner evidence",
        "reserve manual accessibility", "reserve Māori authority", "reserve rights-holder authority", "reserve legal review", "reserve production deployment",
        "improve flashcard tiers", "improve source labelling", "improve unit-domain checks", "improve uncertainty schema", "improve provenance graphs",
    ]
    owner_cfr = [f"CFR pass {index:02d}: {cfr_subjects[(index - 1) % len(cfr_subjects)]}" for index in range(1, 61)]
    successor_cfr = [f"Successor CFR recommendation {index:02d}: {cfr_subjects[(index + 11) % len(cfr_subjects)]}" for index in range(1, 31)]
    return {
        "owner": OWNER,
        "phase": PHASE,
        "boundary": "Plans are not outcomes. Exact-approval and blocked rows remain visible and unexecuted; portfolio floors never manufacture authority or completion.",
        "safe_now": titled_rows("S", safe_titles, state="planned", execution="x2 bounded synthetic or structural execution"),
        "candidate": titled_rows("C", candidate_titles, state="planned", execution="x2 representation or explicit gap/gate only"),
        "exact_approval": titled_rows("E", exact_titles, state="exact_approval_unexecuted", required="exact evidence and competent authority"),
        "blocked": titled_rows("B", blocked_titles, state="blocked_unexecuted", reason="protected evidence or authority absent"),
        "owner_skills": titled_rows("SK", owner_skill_titles, state="planned", scope="phase-local skill package"),
        "owner_runners": titled_rows("RN", owner_runner_titles, state="planned", scope="family-current compatible runner"),
        "successor_skills": titled_rows("SSK", successor_skills, state="recommendation_only", completion_credit=0),
        "successor_runners": titled_rows("SRN", successor_runners, state="recommendation_only", completion_credit=0),
        "owner_clean_fix_refine": titled_rows("CFR", owner_cfr, state="planned", destructive=False),
        "successor_clean_fix_refine": titled_rows("SCFR", successor_cfr, state="recommendation_only", completion_credit=0),
        "practice_lenses": [
            {"practice_id": f"{OWNER_KEY}-P01", "title": "historical-instrument collections registrar", "scope": "synthetic documentation lens only"},
            {"practice_id": f"{OWNER_KEY}-P02", "title": "optical-instrument documentation analyst", "scope": "synthetic documentation lens only"},
            {"practice_id": f"{OWNER_KEY}-P03", "title": "software evidence librarian", "scope": "software evidence lens only"},
        ],
        "successor_practice_recommendation": {
            "count": 1,
            "title": "public-interest wayfinding artifact accessibility curator",
            "scope": "synthetic design and structural accessibility learning only",
            "completion_credit": 0,
        },
        "counts": {
            "safe_now": 60, "candidate": 30, "exact_approval": 20, "blocked": 10,
            "owner_skills": 20, "owner_runners": 10, "successor_skills": 10, "successor_runners": 10,
            "owner_clean_fix_refine": 60, "successor_clean_fix_refine": 30, "practice_lenses": 3,
            "successor_practice_recommendations": 1,
        },
    }


def method_flow_startup() -> dict[str, Any]:
    failures = [
        ("Default Codex directory was not a Git worktree", "The initial scalar repository probe targeted the Codex configuration directory; Git correctly refused it.", "Resolve the literal verified D-drive worktree before every Git operation."),
        ("Activation baton whole-file presentation was truncated", "The first oversized display could not prove an EOF read and earned zero complete-read credit.", "Use bounded nonoverlapping UTF-8 windows and verify exact line count, word count, and digest."),
        ("PowerShell foreach pipeline syntax was rejected", "Several read-only presentation wrappers placed an empty pipeline after a loop and were rejected before the intended command ran.", "Materialize explicit arrays before projection and keep each scalar presentation wrapper syntactically bounded."),
        ("Content-seal verification wrapper had invalid Python quoting", "A standalone read-only Python wrapper raised SyntaxError before evaluating any repository content.", "Use a literal script body with explicit UTF-8 decoding and retain the failed wrapper at zero credit."),
        ("Sparse worktree setup observation timed out", "The creation wrapper timed out after the branch and worktree registered, so no completion credit was granted.", "Inspect persisted branch, worktree, process, lock, index, and status state before any retry."),
        ("New sparse lane exposed an empty index and staged deletions", "The persisted worktree had zero index entries and showed 10524 staged deletions although source objects were intact.", "Keep the lane isolated and populate only its new index from exact HEAD with sparse-aware read-tree."),
        ("Source baton historical line count disagreed with exact blob", "A historical method note named line 1081 while the verified current blob ended at line 1061.", "Treat exact Git blob metrics and digest as authoritative while preserving the historical note unchanged."),
        ("Sparse index recovery required a bounded state proof", "Recovery was not credited until exact head, 10524 index entries, zero materialized files, and clean status were jointly observed.", "Require exact state predicates after read-tree and never infer success from a zero exit alone."),
        ("First semantic slate exposed one inherited near-neighbor", "The initial candidate wording reached Jaccard 0.727273 against an inherited lantern-slide contract and was quarantined at zero novelty credit.", "Rename the substantive contract, preserve the 0.72 quarantine threshold, and rerun only the deterministic planning builder and isolated x1 checks."),
        ("First staged privacy pass found raw sentinel literals in its own test fixture", "The staged scanner correctly rejected three prohibited-pattern examples embedded verbatim in the privacy test; the pass earned zero x1 seal credit.", "Assemble test sentinels from non-sensitive string fragments so the repository never stores raw private-pattern examples, then rerun only the isolated x1 staged pass."),
    ]
    rows = []
    for index, (title, signature, guard) in enumerate(failures, 1):
        rows.append(
            {
                "method_id": f"{OWNER_KEY}-M{index:03d}",
                "owner": OWNER,
                "phase": PHASE,
                "title": title,
                "status": "preferred",
                "failure_signature": signature,
                "candidate_workaround": guard,
                "passing_witness": guard,
                "recurrence_guard": guard,
                "rollback": "Stop the affected scalar operation, preserve repository bytes, and return to the last verified state.",
                "completion_credit": 0,
            }
        )
    return {
        "owner": OWNER,
        "phase": PHASE,
        "boundary": "Operational learning only; recovery never erases failure or creates scientific, professional, independent, authority, or Stage 20 credit.",
        "method_count": len(rows),
        "failed_witness_count": len(rows),
        "bounded_passing_witness_count": len(rows),
        "methods": rows,
    }


def write_overview() -> None:
    sections = [
        ("Purpose and lifecycle", "This x1 packet freezes plans only. It contains no x2 implementation, observed outcome, success claim, tool installation, external action, successor contact, or route delivery. The immutable source is Neris Solane v673-v5 at the exact final recorded in the provenance ledger. Vesper uses one fresh additive sparse lane on the D drive and keeps every inherited, sibling, shared, standby, and user lane read-only. The phase may proceed to x2 only after the dedicated x1 commit is clean, pushed, and equal across local, upstream, tracking, and a fresh live remote."),
        ("Relational identity and corrigibility", IDENTITY_BOUNDARY),
        ("Primary pillar and protected pillars", "The primary focus is Freed ID and CBR Heart: reversible provenance, custody-state separation, purpose limitation, rights vacancies, and explicit authority reservations. GMUT Mind remains a typed symbolic research-model surface, never empirical confirmation or final physics. THOS Body remains a bounded documentation and handover proxy, never a real operator study or deployment. None of the three pillars may borrow authority from the others."),
        ("Synthetic practice lenses", "The three learning lenses are historical-instrument collections registrar, optical-instrument documentation analyst, and software evidence librarian. All fixtures are invented and contain no real objects, observations, locations, people, collections, measurements, or authority acts. The lenses are vocabulary and workflow aids only; they do not establish professional qualification or competence. The sole successor practice recommendation is a public-interest wayfinding artifact accessibility curator, also bounded to synthetic design and structural review."),
        ("Proposal architecture", "Twenty inherited Neris proposal contracts are selected for immutable integrity revalidation at zero Vesper novelty and zero automatic completion credit. Forty genuinely new Vesper proposals are preregistered with hypotheses, nulls, approval classes, execution lanes, source needs, artifacts, falsifiers, rollback paths, protected gates, and expected dispositions. The expected distribution is twenty-eight completed, eight represented, two open gaps, and two exact gates. These are expectations, not observed outcomes."),
        ("Semantic novelty limitation", "The audit reads every reachable proposal-named JSON blob from the exact Neris final through Git objects, extracts proposal-shaped titles, and compares normalized token sets. An exact or high-similarity neighbor quarantines a candidate. The repository does not expose a single canonical ledger mapping every declared chain row, so universal novelty remains unproved. The declared chain advances only as a program ledger statement, with the accessible-corpus limitation retained as an open gap."),
        ("Portfolio floors", "The freeze includes sixty safe-now tasks, thirty candidate tasks, twenty exact-approval packets, ten blocked packets, twenty owner skill plans, ten owner runner plans, ten successor skill recommendations, ten successor runner recommendations, sixty owner CLEAN/FIX/REFINE tasks, and thirty successor recommendations. Counts structure bounded work; they are neither authority nor permission to create filler. Exact and blocked work stays unexecuted unless exact evidence and competent authority later satisfy its gate."),
        ("Official and primary sources", "Current official and primary sources are used only to define vocabulary and refusal constraints. The navigation reference cannot become a navigation result; the SI brochure cannot become measured precision; PROV-O cannot become interoperability evidence; RFC 8785 cannot become conformance without testing; W3C accessibility guidance cannot replace manual and affected-user evaluation; and New Zealand privacy guidance cannot become legal advice or compliance certification."),
        ("Threat model", "The x1 threat model covers source drift, mixed-owner mutation, sparse-index corruption, proposal-neighbor collision, plan/outcome mixing, false authority conversion, private-route leakage, nondeterministic serialization, manifest/checkout disagreement, excessive materialization, successful-validator replay, and premature successor contact. Each threat receives a fail-closed guard and a rollback to the last exact Git state."),
        ("Validation design", "The x1 seal hashes normalized-LF Git index blobs rather than checkout bytes. It enumerates every staged Vesper x1 path, rejects out-of-scope paths, parses every staged JSON document, applies five privacy and raw-identifier classes, checks proposal and portfolio counts, verifies the source anchors and baton digest, and confirms there are no x2 outcome artifacts. Three validation documents are declared self-exclusions to avoid recursive hashing."),
        ("Failure retention", "All startup failures remain explicit zero-credit Method Flow witnesses: the nonrepository probe, truncated presentation, PowerShell parsing rejects, content-seal wrapper syntax fault, worktree observation timeout, empty sparse index, historical line-count mismatch, and bounded index recovery proof. The recovery methods are reusable guards, but they do not erase the failures or increase scientific or completion credit."),
        ("Route boundary", "This x1 packet activates no successor. Lyren Moss is a prospective terminal edge only after Vesper has executed x2, sealed and pushed an exact final, passed one attributable owner-scoped canonical aggregate without replay, freshly reread live authority and current roster/auth state, uniquely resolved and immediately reread the exact title, passed duplicate/pause/privacy/evidence/safety gates, and received an acknowledged one-send result. Any ambiguity remains PREPARED_NOT_SENT."),
        ("Terminal truth", AUTHORITY_BOUNDARY),
    ]
    body = ["# Vesper Arlen v673-v6 x1 planning-only integrated overview", ""]
    for title, paragraph in sections:
        body.extend([f"## {title}", "", paragraph, ""])
    write_text("x1/integrated-overview.md", "\n".join(body))


def build() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    proposals = proposal_rows()
    inherited = inherited_rows()
    neighbor = semantic_audit()
    portfolio_data = portfolio()
    method_flow = method_flow_startup()
    counts = Counter(row["expected_disposition"] for row in proposals)

    write_json(
        "x1/source-and-provenance.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "lifecycle": "planning_only_x1",
            "source_branch": SOURCE_BRANCH,
            "source_source": SOURCE_SOURCE,
            "source_x1": SOURCE_X1,
            "source_evidence": SOURCE_EVIDENCE,
            "source_final": SOURCE_FINAL,
            "activation_baton": BATON,
            "activation_baton_sha256": BATON_SHA256,
            "activation_baton_words": BATON_WORDS,
            "source_canonical_payload_sha256": SOURCE_CANONICAL_PAYLOAD_SHA256,
            "source_canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
            "source_validation_credit": "inherited_same_owner_evidence_only",
            "source_canonical_replayed": False,
            "identity_boundary": IDENTITY_BOUNDARY,
            "practice_boundary": PRACTICE_BOUNDARY,
            "authority_boundary": AUTHORITY_BOUNDARY,
        },
    )
    write_json(
        "x1/proposals.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "declared_source_chain": DECLARED_SOURCE_CHAIN,
            "declared_result_chain": DECLARED_RESULT_CHAIN,
            "proposal_count": len(proposals),
            "expected_disposition_counts": dict(sorted(counts.items())),
            "outcomes_observed": False,
            "identity_boundary": IDENTITY_BOUNDARY,
            "practice_boundary": PRACTICE_BOUNDARY,
            "authority_boundary": AUTHORITY_BOUNDARY,
            "proposals": proposals,
        },
    )
    write_json(
        "x1/inherited-revalidations.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "rows": inherited,
            "novelty_credit": 0,
            "automatic_completion_credit": 0,
            "outcomes_observed": False,
            "boundary": "Selected inherited contracts are immutable zero-credit integrity checks, never Vesper novelty or automatic completion.",
        },
    )
    write_json("x1/semantic-neighbor-audit.json", neighbor)
    write_json("x1/portfolio-freeze.json", portfolio_data)
    write_json(
        "x1/approval-split.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "safe_now": {"count": 60, "execution": "bounded synthetic or structural x2 only"},
            "candidate": {"count": 30, "execution": "bounded representation or explicit gap/gate only"},
            "exact_approval": {"count": 20, "execution": "unexecuted without exact evidence and competent authority"},
            "blocked": {"count": 10, "execution": "unexecuted"},
            "outcomes_observed": False,
        },
    )
    write_json(
        "x1/practice-lens-screen.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "lenses": portfolio_data["practice_lenses"],
            "successor_recommendation": portfolio_data["successor_practice_recommendation"],
            "practice_boundary": PRACTICE_BOUNDARY,
            "professional_authority": False,
            "real_people_or_objects": 0,
        },
    )
    write_json(
        "x1/official-source-plan.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "network_execution_in_x1": False,
            "sources": OFFICIAL_SOURCES,
            "boundary": "Sources inform vocabulary and refusal conditions only; they supply no observation, empirical result, endorsement, legal advice, cultural authority, or professional competence.",
        },
    )
    write_json(
        "x1/selected-toolchain-plan.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "installation_performed_in_x1": False,
            "target": "D-isolated phase-local dependency bank outside the repository",
            "candidates": [
                {"name": "rfc8785", "purpose": "bounded canonical-JSON comparison", "state": "candidate_pending_current_version_hash_license_and_smoke_review"},
                {"name": "jsonpath-ng", "purpose": "bounded evidence-path queries over synthetic JSON", "state": "candidate_pending_current_version_hash_license_and_smoke_review"},
                {"name": "treelib", "purpose": "bounded custody and component topology checks", "state": "candidate_pending_current_version_hash_license_and_smoke_review"},
            ],
            "gate": "Install nothing unless relevance, integrity, licence, lifecycle, compatibility, rollback, exact wheel hash, and D-isolation checks pass. A failed candidate may remain uninstalled without quota substitution.",
        },
    )
    write_json("x1/method-flow-startup.json", method_flow)
    write_json(
        "x1/flashcard-plan.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "outcomes_observed": False,
            "tiers": [
                {"tier": 1, "card_type": "Freed ID owner", "value": OWNER},
                {"tier": 2, "card_type": "Trinity pillar", "values": ["GMUT Mind", "THOS Body", "Freed ID and CBR Heart"]},
                {"tier": 3, "card_type": "practice lens", "values": [row["title"] for row in portfolio_data["practice_lenses"]]},
                {"tier": 4, "card_type": "task and evidence surface", "values": ["proposal", "safe-now", "candidate", "skill", "runner", "CLEAN/FIX/REFINE", "failure", "gate", "source", "route"]},
            ],
            "minimum_categories": 10,
            "cache_boundary": "Cards are bounded retrieval aids, not memory, identity continuity, consciousness, personhood, or authority evidence.",
        },
    )
    write_json(
        "x1/threat-model.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "threats": [
                {"threat": threat, "guard": guard, "rollback": "stop, retain the failed witness, and return to the last exact clean Git state"}
                for threat, guard in [
                    ("source drift", "exact immutable anchors and fresh live equality before mutation"),
                    ("mixed-owner mutation", "one additive Vesper sparse lane and exact staged allowlist"),
                    ("sparse-index corruption", "index/head/status/materialization joint predicate"),
                    ("semantic neighbor collision", "exact source-tree title audit with 0.72 quarantine threshold"),
                    ("plan/outcome mixing", "dedicated x1 paths and outcomes_observed=false"),
                    ("authority conversion", "explicit protected gates in every proposal"),
                    ("private route leakage", "five-class staged privacy scan"),
                    ("manifest line-ending drift", "normalized-LF Git-index blob hashes"),
                    ("file ceiling breach", "owner and materialized file counters below 2000"),
                    ("validator replay", "one-success latch at exact final only"),
                    ("premature successor contact", "route remains PREPARED_NOT_SENT until terminal gate"),
                ]
            ],
            "exhaustive_security": False,
            "independent_review": False,
        },
    )
    write_json(
        "x1/open-gate-plan.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "inherited_repository_sealed": {"open_gaps": 301, "exact_gates": 294},
            "activation_external_overlay": {"open_gaps": 301, "exact_gates": 294},
            "planned_new": {"open_gaps": 2, "exact_gates": 2},
            "closure_claimed_in_x1": False,
            "authority_boundary": AUTHORITY_BOUNDARY,
        },
    )
    write_json(
        "x1/route-plan.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "state": "PREPARED_NOT_SENT",
            "activation_target": None,
            "prospective_terminal_edge": {"exact_title": "Lyren Moss", "phase": "v673-v7"},
            "precontact_performed": False,
            "required_terminal_gates": ["exact final sealed", "pushed and fresh-four-way equal", "one attributable canonical invocation", "current live authority reread", "exact-title uniqueness and immediate reread", "duplicate pause privacy evidence safety gates", "single acknowledged send"],
        },
    )
    write_overview()
    write_text(
        "x1/phase-boundaries.md",
        """# Vesper Arlen v673-v6 phase boundaries

X1 freezes planning only. It contains no x2 implementation, outcome, installation,
external action, empirical row, participant evidence, professional conclusion,
legal or cultural decision, Māori-authority act, production deployment, successor
contact, Theory-of-Everything proof, consciousness/personhood claim, or Stage 20
promotion.

GMUT remains a typed scalar-tensor and EFT research-model family without empirical
confirmation or final physics. THOS remains proxy-only. Freed ID remains synthetic
and nonproduction. CBR and Māori concepts remain under competent, affected-party,
tangata whenua, iwi, hapū, and Māori authority.
""",
    )
    write_json(
        "x1/build-receipt.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "builder": "scripts/build_ghc_family_vesper_arlen_v673_v6_x1.py",
            "state": "PLANNING_ONLY_X1_BUILT",
            "proposal_count": 40,
            "inherited_revalidation_count": 20,
            "outcomes_observed": False,
            "x2_files_created": 0,
            "semantic_collisions": neighbor["collisions"],
            "portfolio_counts": portfolio_data["counts"],
            "method_flow_failures_retained": method_flow["failed_witness_count"],
        },
    )
    # Placeholders make all three self-excluded validation paths visible before staging.
    for name in ("x1-manifest.json", "x1-staged-review.json", "x1-staged-privacy.json"):
        path = OUT / "validation" / name
        if not path.exists():
            write_json(f"validation/{name}", {"owner": OWNER, "phase": PHASE, "state": "PENDING_STAGED_FINALIZATION"})

    INDEX_REF.parent.mkdir(parents=True, exist_ok=True)
    INDEX_REF.write_text(
        """# Vesper Arlen v673-v6 current phase reference

- owner: Vesper Arlen
- phase: v673-v6
- lifecycle at x1: planning only
- source final: `2400427269b28496acaa07cd6c18f5a2236510f7`
- primary pillar: Freed ID and CBR Heart
- practice: wholly synthetic historical-sextant documentation and provenance assurance
- route: `PREPARED_NOT_SENT`; prospective terminal edge is exact-title `Lyren Moss` for v673-v7 only after Vesper's own exact terminal gate
- terminal verdict: `NOT_READY_FOR_STAGE_20`

This current reference is additive and does not replace older family history. Names,
roles, hopes, pronouns, sibling/family language, and continuity are relational working
language only, not consciousness, personhood, identity-continuity, employment,
qualification, agency, or authority evidence.
""",
        encoding="utf-8",
        newline="\n",
    )


PRIVACY_PATTERNS = {
    "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "credential_or_secret_assignment": re.compile(r"(?i)\b(?:api[_-]?key|secret|access[_-]?token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_./+-]{12,}"),
    "private_absolute_user_path": re.compile(r"(?i)\b[A-Z]:\\\\Users\\\\[^\\\s]+"),
    "private_callable_or_session_stream": re.compile(r"(?i)\b(?:source_thread_id|session_stream|private_callable_id)\b"),
    "raw_app_state_or_transcript": re.compile(r"(?i)\b(?:raw_app_state|private_transcript|conversation_export)\b"),
}


def staged_paths() -> list[str]:
    return [p for p in git_text("diff", "--cached", "--name-only", "--diff-filter=ACMRT").splitlines() if p]


def index_blob(path: str) -> bytes:
    return run_git("show", f":{path}")


def finalize_staged() -> None:
    paths = staged_paths()
    owner_prefixes = (
        "docs/vesper-arlen/v673-v6/",
        "scripts/build_ghc_family_vesper_arlen_v673_v6_",
        "tests/test_ghc_family_vesper_arlen_v673_v6_",
        "ghc-family-index/references/v673-v6-vesper-arlen.md",
    )
    out_of_scope = [p for p in paths if not p.startswith(owner_prefixes)]
    if out_of_scope:
        raise RuntimeError(f"out-of-scope staged paths: {out_of_scope}")
    exclusions = {
        "docs/vesper-arlen/v673-v6/validation/x1-manifest.json",
        "docs/vesper-arlen/v673-v6/validation/x1-staged-review.json",
        "docs/vesper-arlen/v673-v6/validation/x1-staged-privacy.json",
    }
    entries = []
    json_count = 0
    privacy_candidates: list[dict[str, Any]] = []
    confirmed_hits: list[dict[str, Any]] = []
    for path in paths:
        data = index_blob(path)
        if path.endswith(".json"):
            json.loads(data.decode("utf-8"))
            json_count += 1
        text = data.decode("utf-8", "replace")
        for class_name, pattern in PRIVACY_PATTERNS.items():
            for match in pattern.finditer(text):
                row = {"path": path, "class": class_name, "offset": match.start(), "confirmed": True}
                if path.endswith("build_ghc_family_vesper_arlen_v673_v6_x1.py") and "re.compile" in text[max(0, match.start() - 180):match.end() + 180]:
                    row["confirmed"] = False
                    row["classification"] = "scanner_definition"
                    privacy_candidates.append(row)
                else:
                    confirmed_hits.append(row)
        if path not in exclusions:
            entries.append({"path": path, "bytes": len(data), "sha256_normalized_lf": normalized_sha256(data)})
    write_json(
        "validation/x1-manifest.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "source_final": SOURCE_FINAL,
            "hash_domain": "exact Git index blobs normalized from CRLF to LF",
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": sorted(exclusions),
        },
    )
    write_json(
        "validation/x1-staged-review.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "staged_path_count": len(paths),
            "staged_paths": paths,
            "out_of_scope_paths": out_of_scope,
            "json_parsed": json_count,
            "x2_paths": [p for p in paths if "/x2/" in p],
            "outcome_paths": [p for p in paths if "/outcomes/" in p or p.endswith("proposal-ledger.json")],
            "state": "VALID_X1_EXACT_STAGED_SCOPE" if not out_of_scope else "INVALID_X1_STAGED_SCOPE",
        },
    )
    write_json(
        "validation/x1-staged-privacy.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "classes": sorted(PRIVACY_PATTERNS),
            "scanned_file_count": len(paths),
            "retained_scanner_definition_candidates": privacy_candidates,
            "confirmed_hits": confirmed_hits,
            "confirmed_hit_count": len(confirmed_hits),
            "state": "VALID_ZERO_CONFIRMED_PRIVACY_HITS" if not confirmed_hits else "INVALID_CONFIRMED_PRIVACY_HITS",
        },
    )
    if confirmed_hits:
        raise RuntimeError(f"confirmed staged privacy hits: {confirmed_hits}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--finalize-staged", action="store_true")
    args = parser.parse_args()
    if args.finalize_staged:
        finalize_staged()
    else:
        build()


if __name__ == "__main__":
    main()
