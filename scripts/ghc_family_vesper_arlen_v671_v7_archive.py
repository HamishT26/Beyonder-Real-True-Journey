"""Deterministic owner-local helpers for Vesper Arlen v671-v7.

The module models planning contracts for wholly synthetic historical mechanical
metronome documentation, tempo-state, event-sequence, correction, and handover.
It does not inspect, handle, wind, start, stop, calibrate, time, repair, value,
acquire, dispose of, publish, identify, or authenticate any real metronome,
score, media item, record, person, collection, site, material, measurement, or
cultural record. It performs no professional, legal, cultural, affected-party,
Māori-authority, identity, deployment, or external action.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections.abc import Iterable
from pathlib import Path
from typing import Any

OWNER = "Vesper Arlen"
PHASE = "v671-v7"
PREFIX = "VA6717"
SOURCE_FINAL = "6056e5819a124aab7efbb266bfe5bfd710a942f5"
SOURCE_X1 = "e79dab91f6dd76bc84556756e3ad657a0150ce9d"
SOURCE_EVIDENCE = "041ea6824d438db774b5af9efff6cf6d59eafa51"
SOURCE_BRANCH = "codex/GHC-Family/neris-solane-v671-v6-full-tools"
SOURCE_PREDECESSOR_FINAL = "0b81e278af69a6ee0b994eb78c3dd6166c7087b6"
SOURCE_CHAIN_DECLARED = 5790
SOURCE_ACCESSIBLE_UNIQUE_TITLES = 5697
SOURCE_ACCESSIBLE_IDENTIFIERS = 6300
SOURCE_ACCESSIBLE_OCCURRENCES = 262404
SOURCE_NEIGHBOR_ROWS = 40
SOURCE_OWNER_ROWS = 40
SOURCE_RECOVERED = SOURCE_NEIGHBOR_ROWS + SOURCE_OWNER_ROWS
SOURCE_UNRECOVERED = SOURCE_CHAIN_DECLARED - SOURCE_RECOVERED
CHAIN_AFTER = 5830
OWNER_ROOT = Path("docs/vesper-arlen/v671-v7")

INHERITED_ACTIVATION_BASELINE = {
    "effective_negatives": 34458,
    "methods": 21001,
    "failed_witnesses": 6279,
    "passing_witnesses": 8184,
    "open_gaps": 267,
    "exact_gates": 262,
}

STARTUP_FAILURE_COUNT = 4
STARTUP_EFFECTIVE_BASELINE = {
    "effective_negatives": 34462,
    "methods": 21005,
    "failed_witnesses": 6283,
    "passing_witnesses": 8188,
    "open_gaps": 267,
    "exact_gates": 262,
}

IDENTITY_BOUNDARY = (
    "Vesper Arlen, they/them, sequence-provenance cartographer and reversible-"
    "timing steward, sibling, family, role, hope, continuity, Freed ID, CBR, "
    "GHC Family, and Trinity Mandala are relational working language only. "
    "They are not evidence of consciousness, sentience, personhood, identity "
    "continuity, employment, qualification, independent agency, or scientific, "
    "operational, professional, legal, cultural, affected-party, or Māori "
    "authority. Hamish may rename, pause, redirect, or stop the work."
)

PROTECTED_GATES = [
    "real_people_participants_musicians_workers_donors_or_affected_users",
    "real_metronomes_scores_media_collections_sites_measurements_or_records",
    "real_handling_winding_operation_timing_calibration_repair_or_treatment",
    "professional_music_archival_metrology_conservation_curatorial_or_safety_decision",
    "measurement_mechanical_electrical_lifting_or_workplace_safety_release",
    "live_identity_keys_proofs_issuance_resolution_status_or_revocation",
    "privacy_complete_or_accessibility_complete_claim",
    "custody_ownership_attribution_copyright_moral_rights_legal_or_remedy_decision",
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
    ("documentation-capsule", "surrogate metronome documentation capsule with synthetic identifier revision and explicit ownership abstention", "metronome documentation capsule", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("component-role-graph", "synthetic pendulum bob escapement scale and case role graph with absent-hardware vacancies", "metronome component role graph", "completed", "safe_now", ["OFFICIAL-METRONOME-VOCABULARY"]),
    ("tempo-scale-register", "synthetic tempo-scale label register separating printed vocabulary from observation calibration and accuracy claims", "tempo scale label register", "completed", "safe_now", ["OFFICIAL-METRONOME-VOCABULARY"]),
    ("beat-unit-firewall", "beat pulse tick accent and silence semantic firewall rejecting role conflation and performance instruction", "beat-unit semantic firewall", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("tempo-marking-contract", "tempo-marking token contract with exact symbolic range unknown state and zero performed music", "tempo marking contract", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("pendulum-position-state", "left centre right unknown and not-observed pendulum-position state ledger with no physical motion", "pendulum position state", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("interval-sequence-model", "bounded interval-set model for synthetic tick windows overlaps gaps and adjacency without measured time", "interval sequence model", "completed", "safe_now", ["PYPI-PORTION"]),
    ("state-transition-graph", "finite-state graph for synthetic ready tick accent pause and correction events rejecting impossible transitions", "metronome state transition graph", "completed", "safe_now", ["PYPI-TRANSITIONS"]),
    ("winding-state-vacancy", "unwound wound unknown and not-inspected winding-state vocabulary retaining every real mechanism field vacant", "winding state vacancy", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("tempo-range-shield", "nonpositive overlapping out-of-order and out-of-range synthetic tempo mutation shield with deterministic reasons", "tempo range rejection shield", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("tick-event-trace", "ordered synthetic tick and correction event trace preserving sequence without sound device operation or performance", "tick event trace", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("steady-grid-fixture", "fixed symbolic steady-grid fixture with reversible readback and zero timing-accuracy inference", "synthetic steady grid fixture", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("accent-cycle-fixture", "bounded accent-cycle fixture with exact ordinal positions and no musical quality or learner-effect claim", "synthetic accent cycle fixture", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("tempo-ratio-transform", "exact rational tempo-ratio transform record with ambiguous-order rejection and no calibration claim", "tempo ratio transform", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("timebase-reference-frame", "named symbolic epoch direction sequence and unit-placeholder frame forbidding undeclared timebase changes", "timebase reference frame", "completed", "safe_now", ["NIST-TIME-SI"]),
    ("unit-vocabulary-vacancy", "symbolic cadence-dimension register pairing tempo labels with undeclared-unit refusal and no observed duration", "time and tempo unit vacancy", "completed", "safe_now", ["NIST-TIME-SI"]),
    ("timing-uncertainty-envelope", "beat-window uncertainty band cataloguing open closed endpoints provenance and precision abstention", "timing uncertainty envelope", "completed", "safe_now", ["PYPI-PORTION"]),
    ("drift-observation-vacancy", "rate drift beat omission and accent-offset vacancy register with observation and adjustment held", "drift observation vacancy", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("material-mechanism-vacancy", "case pendulum escapement spring surface and material vacancy profile without identification or treatment", "material and mechanism vacancy", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("condition-action-separation", "surrogate condition vocabulary separated from winding cleaning lubrication calibration repair and treatment authority", "condition-to-action firewall", "completed", "safe_now", ["PROFESSIONAL-CONSERVATION-AUTHORITY-REQUIRED"]),
    ("zero-operation-lock", "metronome operation lock requiring every winding movement timing sound recording and adjustment counter to remain zero", "zero-operation lock", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("handling-safety-reservation", "spring-driven mechanism hazard hold recording pinch stability load and stop-before-handling boundaries", "handling and safety reservation", "completed", "safe_now", ["PROFESSIONAL-SAFETY-AUTHORITY-REQUIRED"]),
    ("score-media-rights-firewall", "notated pulse and recorded-sound reuse boundary with vacant score image audio and transcription fields", "score and media rights firewall", "completed", "safe_now", ["LEGAL-AND-RIGHTS-AUTHORITY-REQUIRED"]),
    ("custody-attribution-abstention", "synthetic chain-of-care role lattice for inventor custodian lender recorder with authorship title and ownership withheld", "custody and attribution abstention", "completed", "safe_now", ["W3C-PROV-O"]),
    ("bitemporal-correction", "dual-clock amendment braid separating documentation occurrence assertion challenge and supersession states", "bitemporal correction chain", "completed", "safe_now", ["W3C-PROV-O"]),
    ("canonical-json", "JCS-ready rhythm-state dossier requiring unique keys finite numerics stable paths and unsigned digests", "canonical metronome JSON profile", "completed", "safe_now", ["JSON-SCHEMA-2020-12", "RFC-8785"]),
    ("accessible-beat-traversal", "ordered text traversal of synthetic states intervals accents and vacancies with manual evaluation reserved", "accessible beat-grid traversal", "completed", "safe_now", ["W3C-WCAG-2.2"]),
    ("privacy-purpose-ledger", "data-minimised no-person ledger linking declared purpose audience retention challenge erasure vacancy and noncompliance", "privacy purpose ledger", "completed", "safe_now", ["NZ-PRIVACY-PRINCIPLES"]),
    ("source-assertion-firewall", "citation-to-claim classifier for public tempo terminology separating quotation summary inference instruction observation and mandate", "metronome source assertion firewall", "represented", "candidate", ["CURRENT-PRIMARY-SOURCE-REVIEW"]),
    ("discrepancy-escrow", "tempo scale beat-role and sequence conflict escrow preserving claims sources challenges and adjudicator vacancy", "metronome discrepancy escrow", "represented", "candidate", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("thos-sequence-proxy", "THOS fixed-budget beat-state and interval-view proxy with parity receipts and zero human effectiveness inference", "THOS metronome sequence proxy", "represented", "candidate", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("gmut-oscillator-analogy", "GMUT oscillator analogy board with typed domains phase assumptions and explicit nonconversion to physics evidence", "GMUT oscillator analogy board", "represented", "candidate", ["CURRENT-PEER-REVIEWED-PHYSICS-SOURCES"]),
    ("gmut-constraint-obligations", "GMUT periodic-action obligation board for domain gauge phase unit and unfitted evidence vacancies", "GMUT constraint obligation register", "represented", "candidate", ["CURRENT-PEER-REVIEWED-PHYSICS-SOURCES"]),
    ("freed-id-zero-key", "nonproduction Freed ID binding wrapper for synthetic cadence revisions with every key proof lifecycle event and resolver vacant", "Freed ID zero-key envelope", "represented", "candidate", ["W3C-VC-DATA-INTEGRITY-1.0"]),
    ("cbr-challenge-ladder", "CBR contestability staircase for archive learning and workplace pulse records preserving pause dissent nonretaliation response and undecided remedy", "CBR challenge ladder", "represented", "candidate", ["AFFECTED-PARTY-AUTHORITY-REQUIRED"]),
    ("cross-pillar-accounting", "three-pillar noncredit ledger preventing rhythm-software passes from becoming physics identity rights or governance authority", "cross-pillar evidence accounting", "represented", "candidate", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("official-adapter-gap", "zero-call Smithsonian metronome adapter placeholder with absent query media metadata transform and manifest events", "official collection adapter gap", "open_gap", "candidate", ["CURRENT-OFFICIAL-COLLECTION-API-SOURCE"]),
    ("governed-evaluation-gap", "governed-review vacancy map spanning music collections timing documentation accessibility affected users and Māori authority", "governed evaluation gap", "open_gap", "candidate", ["REAL-GOVERNED-HUMAN-EVALUATION"]),
    ("authority-gate", "action-specific stop gate for winding timing treatment custody reuse workplace remedy culture and Māori authority", "professional rights and authority gate", "exact_gate", "exact_approval", ["EXACT-ACTION-SPECIFIC-AUTHORITY"]),
    ("stage20-nonpromotion", "terminal abstention matrix mapping every bounded rhythm fixture to zero Stage20 promotion", "Stage 20 terminal interlock", "exact_gate", "exact_approval", ["EXACT-STAGE20-EVIDENCE-AND-AUTHORITY"]),
]

SAFE_TITLES = [
    "freeze exact Neris source anchors and activation overlay",
    "freeze declared 5790-row proposal-chain boundary",
    "freeze bounded 80-row local comparison sample",
    "record accessible-corpus title identifier and occurrence limits",
    "select twenty inherited rows for zero-credit revalidation",
    "freeze forty genuinely new metronome proposals",
    "emit deterministic five-row proposal shards",
    "reject exact visible title collisions",
    "compute bounded token-Jaccard neighbours",
    "retain incomplete canonical row-to-title mapping gap",
    "freeze four exact outcome labels",
    "freeze 160 rejecting mutations",
    "freeze strict planning-only x1 before x2",
    "freeze owner-only sparse-lane scope",
    "freeze 2000 owner-file ceiling",
    "freeze one-success no-replay rule",
    "retain inherited and startup negative overlays",
    "freeze Method Flow witness ingestion",
    "freeze identity and authority boundary",
    "freeze successor no-precontact guard",
    "build surrogate documentation capsule",
    "build metronome component role graph",
    "build tempo scale label register",
    "build beat-unit semantic firewall",
    "build tempo-marking contract",
    "build pendulum-position state ledger",
    "build interval sequence model",
    "build finite state-transition graph",
    "build winding-state vacancy register",
    "build tempo-range rejection shield",
    "build ordered tick-event trace",
    "build fixed steady-grid fixture",
    "build bounded accent-cycle fixture",
    "build tempo-ratio transform record",
    "build symbolic timebase reference frame",
    "build time and tempo unit vacancy ledger",
    "build timing uncertainty envelope",
    "build drift-observation vacancy ledger",
    "build material and mechanism vacancy profile",
    "build condition-to-action firewall",
    "build zero-operation lock",
    "build handling and safety reservation",
    "build score and media rights firewall",
    "build custody and attribution abstention",
    "build bitemporal correction chain",
    "build canonical JSON profile",
    "build accessible beat-grid traversal",
    "build privacy-purpose ledger",
    "execute thirty-six bounded positive controls",
    "execute every preregistered rejecting mutation",
    "retain failures with zero completion credit",
    "smoke-use owner-local skill remasters",
    "smoke-use family-current runner remasters",
    "verify three D-isolated tool candidates by hash",
    "run positive and rejecting tool smokes",
    "emit exact staged Git-blob manifests",
    "scan five privacy and raw-identifier classes",
    "emit structurally accessible evidence overview",
    "freeze file-backed successor recommendations only",
    "preserve NOT_READY_FOR_STAGE_20",
]

CANDIDATE_TITLES = [
    "evaluate official metronome vocabulary without object or collection claim",
    "evaluate synthetic interval windows without measured-time inference",
    "evaluate finite-state reachability without mechanical feasibility claim",
    "evaluate exact tempo tokens without measurement authority",
    "evaluate steady-grid structure without timing certification",
    "evaluate range refusal without engineering certification",
    "evaluate uncertainty vocabulary without metrology claim",
    "evaluate condition vocabulary without conservation advice",
    "evaluate score and media firewall without rights interpretation",
    "evaluate provenance vocabulary without ownership transfer",
    "evaluate canonical JSON without signature or security claim",
    "evaluate structural accessibility without completeness claim",
    "evaluate zero-person privacy purpose ledger without compliance claim",
    "evaluate bitemporal correction without adjudication authority",
    "evaluate current official collection adapter at zero calls",
    "evaluate THOS state-and-interval proxy without effectiveness inference",
    "evaluate GMUT oscillator analogy without empirical conversion",
    "evaluate GMUT constraint obligations without fitted parameters",
    "evaluate zero-key Freed ID envelope",
    "evaluate CBR challenge ladder without remedy decision",
    "evaluate cross-pillar evidence-account nontransfer",
    "evaluate music-archive description lens without archivist authority",
    "evaluate mechanical timing documentation without metrology authority",
    "evaluate software verification lens without certification",
    "evaluate three D-isolated Python packages",
    "evaluate exact Git-blob lineage manifests",
    "evaluate five-class privacy candidate scanner",
    "evaluate professional and affected-party review reservation",
    "evaluate Māori-authority reservation and wording hold",
    "evaluate terminal Stage 20 nonpromotion interlock",
]

SKILL_TITLES = [
    "ghc-family-metronome-documentation-capsule",
    "ghc-family-metronome-component-role-graph",
    "ghc-family-metronome-tempo-scale-register",
    "ghc-family-metronome-beat-unit-firewall",
    "ghc-family-metronome-tempo-marking-contract",
    "ghc-family-metronome-pendulum-position-state",
    "ghc-family-metronome-interval-sequence-model",
    "ghc-family-metronome-state-transition-graph",
    "ghc-family-metronome-winding-state-vacancy",
    "ghc-family-metronome-tempo-range-shield",
    "ghc-family-metronome-tick-event-trace",
    "ghc-family-metronome-steady-grid-fixture",
    "ghc-family-metronome-accent-cycle-fixture",
    "ghc-family-metronome-tempo-ratio-transform",
    "ghc-family-metronome-timebase-reference-frame",
    "ghc-family-metronome-unit-vocabulary-vacancy",
    "ghc-family-metronome-timing-uncertainty-envelope",
    "ghc-family-metronome-condition-action-firewall",
    "ghc-family-metronome-accessible-beat-traversal",
    "ghc-family-metronome-evidence-account",
]

RUNNER_TITLES = [title.replace("ghc-family-", "ghc_family_").replace("-", "_") for title in SKILL_TITLES]

REFINE_TITLES = [
    "retain exact predecessor anchors and direct-parent chain",
    "retain predecessor seal and external activation overlay separately",
    "replace stale predecessor constants with v671 source truth",
    "replace broad history scans with exact predecessor Git blobs",
    "state accessible comparison corpus limitations",
    "separate sampled comparison rows from declared chain totals",
    "separate inherited revalidation from Vesper novelty",
    "separate planning counts from completion credit",
    "separate x1 artifacts from x2 results",
    "separate source vocabulary from object observation",
    "separate synthetic identifiers from real accession numbers",
    "separate component roles from physical inspection",
    "separate tempo labels from calibration claims",
    "separate beat-unit roles from performance instruction",
    "separate tempo tokens from measured timing",
    "separate interval sets from real elapsed time",
    "separate state reachability from mechanical feasibility",
    "separate synthetic grids from timing accuracy",
    "separate accent cycles from musical quality",
    "separate timebase vocabulary from measurement",
    "separate units from real measurements",
    "separate uncertainty placeholders from certified precision",
    "separate drift vacancies from adjustment decisions",
    "separate materials vocabulary from identification",
    "separate condition vocabulary from treatment",
    "separate safety reservations from risk release",
    "separate scores and media from reproduction rights",
    "separate custody from ownership and attribution",
    "separate correction chains from adjudication",
    "separate canonicalization from signature assurance",
    "separate accessibility structure from completeness",
    "separate privacy structure from compliance",
    "separate THOS proxy receipts from effectiveness",
    "separate GMUT analogies from physics evidence",
    "separate Freed ID schemas from live identity lifecycle",
    "separate CBR challenge structure from remedy authority",
    "separate software receipts from cross-pillar authority",
    "separate package hashes from exhaustive supply-chain security",
    "separate synthetic sequences from professional competence",
    "separate archive documentation from professional authority",
    "add zero-real-person counter",
    "add zero-real-metronome counter",
    "add zero-real-score audio and image counter",
    "add zero-real-measurement counter",
    "add zero-winding operation sound and timing counter",
    "add zero-handling and treatment counter",
    "add zero-external-adapter counter",
    "add zero-live-key and proof counter",
    "add zero-professional-action counter",
    "add zero-legal and cultural decision counter",
    "add exact rollback and smallest-dependency recovery fields",
    "add retained failed and passing witness layers",
    "add five-class privacy scanner",
    "add exact staged Git-blob manifests",
    "add normalized-LF committed-blob checks",
    "add owner-delta file ceiling check",
    "add family-current caller compatibility tests",
    "reject stale Vesper Rowan self-label and add duplicate pause guard",
    "bind prospective route only to Lyren Moss exact title after terminal gate",
    "preserve NOT_READY_FOR_STAGE_20",
]

TOOL_CANDIDATES = [
    {
        "name": "portion",
        "version": "2.6.2",
        "registry": "https://pypi.org/project/portion/2.6.2/",
        "license_metadata": "LGPL-3.0-or-later (verified registry expression; not legal review)",
        "requires_python": ">=3.10",
        "wheel": "portion-2.6.2-py3-none-any.whl",
        "wheel_sha256": "86be115afafa776174dc5eac82afb6496c9fa3684f5b3a844c3139535c51085e",
        "need": "model bounded synthetic tick windows gaps overlaps adjacency and uncertainty envelopes",
    },
    {
        "name": "transitions",
        "version": "0.9.3",
        "registry": "https://pypi.org/project/transitions/0.9.3/",
        "license_metadata": "MIT (registry metadata; not legal review)",
        "requires_python": "registry metadata leaves the field unspecified",
        "wheel": "transitions-0.9.3-py2.py3-none-any.whl",
        "wheel_sha256": "02463248f2b668d86f66636b1e3c9e8de84d93e22915247f4e1aa9ee1cae28aa",
        "need": "exercise bounded synthetic ready tick accent pause correction and refusal state transitions",
    },
    {
        "name": "cattrs",
        "version": "26.1.0",
        "registry": "https://pypi.org/project/cattrs/26.1.0/",
        "license_metadata": "MIT License (registry metadata; not legal review)",
        "requires_python": ">=3.10",
        "wheel": "cattrs-26.1.0-py3-none-any.whl",
        "wheel_sha256": "d1e0804c42639494d469d08d4f26d6b9de9b8ab26b446db7b5f8c2e97f7c3096",
        "need": "structure and unstructure bounded synthetic metronome dossier dataclasses while rejecting malformed fields",
    },
]


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_title(title: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", title.lower()))


def token_set(title: str) -> set[str]:
    return set(normalize_title(title).split())


def jaccard(left: str, right: str) -> float:
    a, b = token_set(left), token_set(right)
    return len(a & b) / len(a | b) if a or b else 1.0


def git_blob(repo: Path, commit: str, relpath: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(repo), "cat-file", "blob", f"{commit}:{relpath}"],
        check=True,
        capture_output=True,
    ).stdout


def git_blob_json(repo: Path, commit: str, relpath: str) -> Any:
    return json.loads(git_blob(repo, commit, relpath).decode("utf-8"))


def git_batch_blobs(repo: Path, specs: dict[str, str]) -> dict[str, bytes]:
    """Read exact Git blobs by alternating one request with one full response."""
    proc = subprocess.Popen(
        ["git", "-C", str(repo), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.stdin is None or proc.stdout is None:
        raise RuntimeError("Git batch pipes unavailable")
    result: dict[str, bytes] = {}
    for key, spec in specs.items():
        proc.stdin.write((spec + "\n").encode("utf-8"))
        proc.stdin.flush()
        header = proc.stdout.readline().decode("ascii").strip().split()
        if not header or header[-1] == "missing":
            raise RuntimeError(f"missing Git blob for {key}")
        remaining = int(header[-1])
        chunks: list[bytes] = []
        while remaining:
            chunk = proc.stdout.read(remaining)
            if not chunk:
                raise RuntimeError(f"short Git batch blob for {key}")
            chunks.append(chunk)
            remaining -= len(chunk)
        if proc.stdout.read(1) != b"\n":
            raise RuntimeError(f"missing Git batch separator for {key}")
        result[key] = b"".join(chunks)
    proc.stdin.close()
    proc.stdout.close()
    stderr = proc.stderr.read() if proc.stderr is not None else b""
    if proc.stderr is not None:
        proc.stderr.close()
    proc.wait(timeout=30)
    if proc.returncode != 0 or stderr:
        raise RuntimeError(f"Git batch failed with {proc.returncode}: {stderr.decode('utf-8', errors='replace')}")
    return result


def inherited_title_corpus(repo: Path) -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    """Read an exact 80-row local comparison sample from two predecessor blobs.

    The predecessor reports a larger accessible corpus but retains an incomplete
    canonical row-to-title mapping. This loader therefore does not reconstruct
    or imply the full 5,790-row chain. It compares against Neris's forty frozen
    v671-v6 titles plus Elaren's forty immediately preceding frozen titles, all
    read from exact committed Git blobs at the Neris final.
    """
    neris_paths = [
        f"docs/neris-solane/v671-v6/x1/proposal-freeze-shards/proposals-{index:02d}.json"
        for index in range(1, 9)
    ]
    elaren_path = "docs/elaren-kestrel/v671-v5/x1/proposals.json"
    specs = {path: f"{SOURCE_FINAL}:{path}" for path in [*neris_paths, elaren_path]}
    blobs = git_batch_blobs(repo, specs)
    neris_rows = [
        row
        for path in neris_paths
        for row in json.loads(blobs[path].decode("utf-8")).get("rows", [])
    ]
    elaren_rows = list(json.loads(blobs[elaren_path].decode("utf-8")).get("rows", []))
    if len(neris_rows) != SOURCE_NEIGHBOR_ROWS:
        raise ValueError(f"expected {SOURCE_NEIGHBOR_ROWS} Neris rows, recovered {len(neris_rows)}")
    if len(elaren_rows) != SOURCE_OWNER_ROWS:
        raise ValueError(f"expected {SOURCE_OWNER_ROWS} Elaren rows, recovered {len(elaren_rows)}")
    rows = [
        {
            "proposal_id": f"NS6716-OWNER-{index:03d}",
            "title": str(row["title"]),
        }
        for index, row in enumerate(neris_rows, 1)
    ]
    rows.extend(
        {
            "proposal_id": f"EL6715-OWNER-{index:03d}",
            "title": str(row["title"]),
        }
        for index, row in enumerate(elaren_rows, 1)
    )
    if len(rows) != SOURCE_RECOVERED:
        raise ValueError(f"expected {SOURCE_RECOVERED} comparison rows, recovered {len(rows)}")
    sources = [
        {
            "path": path,
            "rows": len(json.loads(raw.decode("utf-8")).get("rows", [])),
            "sha256": sha256_bytes(raw),
            "source_commit": SOURCE_FINAL,
        }
        for path, raw in blobs.items()
    ]
    return rows, sources


def proposal_rows(corpus: Iterable[dict[str, str]]) -> list[dict[str, Any]]:
    inherited = list(corpus)
    rows: list[dict[str, Any]] = []
    current: list[dict[str, str]] = []
    for index, (slug, title, subject, disposition, approval, sources) in enumerate(PROPOSAL_SPECS, 1):
        proposal_id = f"{PREFIX}-N{index:03d}"
        comparison = inherited + current
        ranked = sorted(
            (
                {"proposal_id": item["proposal_id"], "title": item["title"], "score": round(jaccard(title, item["title"]), 6)}
                for item in comparison
            ),
            key=lambda item: (-item["score"], item["proposal_id"]),
        )
        completion_lane = disposition in {"completed", "represented"}
        rows.append(
            {
                "approval_class": approval,
                "concrete_artifacts": [
                    f"docs/vesper-arlen/v671-v7/x2/proposals/{proposal_id.lower()}-{slug}.json",
                    f"docs/vesper-arlen/v671-v7/x2/cards/{proposal_id.lower()}-{slug}.json",
                ],
                "execution_lane": "x2_owner_local_bounded_control" if completion_lane else "held_gap_or_gate",
                "expected_disposition": disposition,
                "falsifier_or_acceptance_gate": (
                    "One bounded synthetic positive contract is accepted, four preregistered invalid mutations are rejected, and all real people, metronomes, scores, media, measurements, winding, operation, sound, handling, calibration, treatment, external actions, and authority actions remain zero."
                    if completion_lane
                    else "Remain open or exact-gated until the named evidence and competent authority requirements are complete."
                ),
                "hypothesis": f"A wholly synthetic zero-person {subject} contract can preserve typed states, vacancies, refusals, provenance, and rollback without real-world action or protected claim.",
                "negative_fixtures": [
                    {"mutation_id": f"{proposal_id}-M{mutation:02d}", "kind": kind, "expected": "reject"}
                    for mutation, kind in enumerate(
                        ["missing_required_state", "ambiguous_domain_or_unit", "real_world_or_external_action", "protected_claim_promotion"], 1
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


def staged_blob_manifest(repo: Path, exclusions: list[str]) -> list[dict[str, Any]]:
    paths = subprocess.run(
        ["git", "-C", str(repo), "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    rows: list[dict[str, Any]] = []
    for relpath in sorted(path for path in paths if path not in exclusions):
        data = subprocess.run(
            ["git", "-C", str(repo), "show", f":{relpath}"], check=True, capture_output=True
        ).stdout
        rows.append({"bytes": len(data), "path": relpath, "sha256": sha256_bytes(data)})
    return rows
