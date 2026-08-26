"""Deterministic owner-local helpers for Lyren Moss v671-v8.

The module models planning contracts for wholly synthetic hand-bound-book
collation, gathering-sequence, condition-documentation, correction, and
reversible handover. It does not inspect, handle, open, collate, paginate,
identify, sample, clean, repair, rebind, treat, value, acquire, dispose of,
publish, digitize, or authenticate any real book, binding, leaf, text, image,
record, person, collection, site, material, measurement, or cultural record.
It performs no professional, legal, cultural, affected-party, Māori-authority,
identity, deployment, or external action.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections.abc import Iterable
from pathlib import Path
from typing import Any

OWNER = "Lyren Moss"
PHASE = "v671-v8"
PREFIX = "LM6718"
SOURCE_FINAL = "98d77253f3882fefad7f65e68fd0135f9b6f3d71"
SOURCE_X1 = "d2ab0148e82725c680204d1d5a3fbf98544e57ea"
SOURCE_EVIDENCE = "c7b6801c309ba334bff8ce1a14d0cde0350221cb"
SOURCE_BRANCH = "codex/GHC-Family/vesper-arlen-v671-v7-full-tools"
SOURCE_PREDECESSOR_FINAL = "6056e5819a124aab7efbb266bfe5bfd710a942f5"
SOURCE_CHAIN_DECLARED = 5830
SOURCE_ACCESSIBLE_UNIQUE_TITLES = 5697
SOURCE_ACCESSIBLE_IDENTIFIERS = 6300
SOURCE_ACCESSIBLE_OCCURRENCES = 262404
SOURCE_NEIGHBOR_ROWS = 40
SOURCE_OWNER_ROWS = 40
SOURCE_RECOVERED = SOURCE_NEIGHBOR_ROWS + SOURCE_OWNER_ROWS
SOURCE_UNRECOVERED = SOURCE_CHAIN_DECLARED - SOURCE_RECOVERED
CHAIN_AFTER = 5870
OWNER_ROOT = Path("docs/lyren-moss/v671-v8")

INHERITED_ACTIVATION_BASELINE = {
    "effective_negatives": 34627,
    "methods": 21170,
    "failed_witnesses": 6448,
    "passing_witnesses": 8389,
    "open_gaps": 269,
    "exact_gates": 264,
}

STARTUP_FAILURE_COUNT = 16
STARTUP_EFFECTIVE_BASELINE = {
    "effective_negatives": 34643,
    "methods": 21186,
    "failed_witnesses": 6464,
    "passing_witnesses": 8405,
    "open_gaps": 269,
    "exact_gates": 264,
}

IDENTITY_BOUNDARY = (
    "Lyren Moss, they/them, collation-provenance cartographer and reversible-"
    "documentation steward, sibling, family, role, hope, continuity, Freed ID, CBR, "
    "GHC Family, and Trinity Mandala are relational working language only. "
    "They are not evidence of consciousness, sentience, personhood, identity "
    "continuity, employment, qualification, independent agency, or scientific, "
    "operational, professional, legal, cultural, affected-party, or Māori "
    "authority. Hamish may rename, pause, redirect, or stop the work."
)

PROTECTED_GATES = [
    "real_people_participants_readers_workers_donors_or_affected_users",
    "real_books_bindings_leaves_texts_images_collections_sites_measurements_or_records",
    "real_handling_opening_collation_pagination_sampling_rebinding_repair_or_treatment",
    "professional_bibliographical_archival_conservation_curatorial_or_safety_decision",
    "material_sampling_lifting_mould_biohazard_or_workplace_safety_release",
    "live_identity_keys_proofs_issuance_resolution_status_or_revocation",
    "privacy_complete_or_accessibility_complete_claim",
    "custody_ownership_attribution_copyright_moral_rights_reuse_legal_or_remedy_decision",
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
    ("documentation-capsule", "surrogate hand-bound-book documentation capsule with synthetic identifier revision and explicit ownership abstention", "book documentation capsule", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("gathering-role-graph", "synthetic cover board spine joint sewing support gathering and leaf role graph with absent-structure vacancies", "binding and gathering role graph", "completed", "safe_now", ["LOC-BOOK-PRESERVATION-GUIDE"]),
    ("collation-formula-register", "synthetic collation-formula token register separating descriptive notation from inspection and bibliographical authority", "collation formula register", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("leaf-page-folio-firewall", "leaf page folio opening recto and verso semantic firewall rejecting role conflation and pagination invention", "leaf and folio semantic firewall", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("signature-marking-contract", "signature-mark token contract with exact symbolic range unknown state and zero transcription of real marks", "signature marking contract", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("leaf-position-state", "front middle back recto verso unknown and not-observed leaf-position ledger with no physical opening", "leaf position state", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("section-sequence-model", "bounded interval-set model for synthetic gathering and leaf ranges overlaps gaps and adjacency without real collation", "section sequence model", "completed", "safe_now", ["PYPI-PORTION"]),
    ("binding-state-transition-graph", "finite-state graph for synthetic accession describe challenge correct and handover events rejecting impossible transitions", "binding documentation state graph", "completed", "safe_now", ["PYPI-TRANSITIONS"]),
    ("sewing-structure-vacancy", "unsupported supported unknown and not-inspected sewing-structure vocabulary retaining every real binding field vacant", "sewing structure vacancy", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("pagination-range-shield", "deterministic folio-range refusal table covering zero origins duplicate leaves reversed spans and impossible bounds", "pagination range rejection shield", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("collation-event-trace", "ordered synthetic gathering leaf and correction trace preserving sequence without book handling opening or transcription", "collation event trace", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("gathering-grid-fixture", "fixed symbolic gathering-grid fixture with reversible readback and zero bibliographical inference", "synthetic gathering grid fixture", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("catchword-cycle-fixture", "bounded catchword-position fixture with exact ordinal placeholders and no textual-authenticity or authorship claim", "synthetic catchword cycle fixture", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("collation-ratio-transform", "exact rational section-to-leaf transform record with ambiguous-order rejection and no physical-structure claim", "collation ratio transform", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("reading-order-reference-frame", "named symbolic front-to-back recto-verso sequence frame forbidding undeclared reading-order changes", "reading order reference frame", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("notation-vocabulary-vacancy", "symbolic collation-dimension register pairing formula labels with undeclared-notation refusal and no observed leaf count", "collation notation vacancy", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("condition-uncertainty-envelope", "leaf-and-joint condition uncertainty bands cataloguing bounded terms provenance and precision abstention", "book condition uncertainty envelope", "completed", "safe_now", ["PYPI-PORTION"]),
    ("deformation-observation-vacancy", "warping detachment abrasion and loss vacancy register with inspection severity and intervention held", "deformation observation vacancy", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("material-structure-vacancy", "paper parchment cloth leather board adhesive thread and media vacancy profile without identification or treatment", "material and structure vacancy", "completed", "safe_now", ["LOC-COLLECTIONS-CARE"]),
    ("condition-action-separation", "surrogate condition vocabulary separated from opening cleaning humidification consolidation repair rebinding and treatment authority", "condition-to-action firewall", "completed", "safe_now", ["PROFESSIONAL-CONSERVATION-AUTHORITY-REQUIRED"]),
    ("zero-treatment-lock", "book-treatment lock requiring every handling opening sampling cleaning repair rebinding digitization and disposal counter to remain zero", "zero-treatment lock", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("handling-safety-reservation", "fragile-binding hazard hold recording support load mould sharp-fastener and stop-before-handling boundaries", "handling and safety reservation", "completed", "safe_now", ["PROFESSIONAL-SAFETY-AUTHORITY-REQUIRED"]),
    ("text-image-rights-firewall", "printed manuscript annotation illustration and scan reuse boundary with every text image transcription and rights field vacant", "text and image rights firewall", "completed", "safe_now", ["LEGAL-AND-RIGHTS-AUTHORITY-REQUIRED"]),
    ("custody-attribution-abstention", "synthetic chain-of-care role lattice for maker author former custodian lender and recorder with ownership withheld", "custody and attribution abstention", "completed", "safe_now", ["W3C-PROV-O"]),
    ("bitemporal-correction", "versioned amendment braid with separate event-time assertion-time challenge withdrawal and supersession lanes", "bitemporal correction chain", "completed", "safe_now", ["W3C-PROV-O"]),
    ("canonical-json", "reproducible unsigned collation dossier with duplicate-member refusal nonfinite-number rejection fixed relative names and deterministic serialization", "canonical book-collation JSON profile", "completed", "safe_now", ["JSON-SCHEMA-2020-12", "RFC-8785"]),
    ("accessible-collation-traversal", "screen-reader-oriented linear narrative for placeholder gatherings leaf roles uncertainty and withheld fields with human testing reserved", "accessible collation traversal", "completed", "safe_now", ["W3C-WCAG-2.2"]),
    ("privacy-purpose-ledger", "zero-person purpose register with audience scope minimum retention challenge path deletion vacancy and explicit noncompliance state", "privacy purpose ledger", "completed", "safe_now", ["NZ-PRIVACY-PRINCIPLES"]),
    ("source-assertion-firewall", "evidence-use taxonomy keeps preservation citations in summary inference workflow-note observation and authority buckets", "book source assertion firewall", "represented", "candidate", ["CURRENT-PRIMARY-SOURCE-REVIEW"]),
    ("discrepancy-escrow", "gathering foliation condition and sequence conflict escrow preserving claims sources challenges and adjudicator vacancy", "collation discrepancy escrow", "represented", "candidate", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("thos-sequence-proxy", "bounded THOS comparison harness over gathering adjacency and document-state views with parity receipts barred from implying benefit for people", "THOS collation sequence proxy", "represented", "candidate", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("gmut-topology-analogy", "GMUT book-topology metaphor ledger types adjacency orientation and domain assumptions while barring conversion into physical evidence", "GMUT topology analogy board", "represented", "candidate", ["CURRENT-PEER-REVIEWED-PHYSICS-SOURCES"]),
    ("gmut-constraint-obligations", "GMUT section-connectivity obligation board for domain gauge orientation unit and unfitted evidence vacancies", "GMUT constraint obligation register", "represented", "candidate", ["CURRENT-PEER-REVIEWED-PHYSICS-SOURCES"]),
    ("freed-id-zero-key", "synthetic nonproduction Freed ID envelope for dossier versions with credentials proofs resolver calls issuance and revocation remaining empty", "Freed ID zero-key envelope", "represented", "candidate", ["W3C-VC-DATA-INTEGRITY-1.0"]),
    ("cbr-challenge-ladder", "CBR objection-and-review scaffold for reading-room records reserves stop disagreement non-retaliation response and remedy decisions", "CBR challenge ladder", "represented", "candidate", ["AFFECTED-PARTY-AUTHORITY-REQUIRED"]),
    ("cross-pillar-accounting", "evidence nontransfer firewall keeps collation tests from crediting GMUT identity infrastructure rights determinations or governance", "cross-pillar evidence accounting", "represented", "candidate", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("official-adapter-gap", "zero-call Library-of-Congress collection adapter placeholder with absent query media metadata transform and manifest events", "official collection adapter gap", "open_gap", "candidate", ["CURRENT-OFFICIAL-COLLECTION-API-SOURCE"]),
    ("governed-evaluation-gap", "governed-review vacancy map spanning rare-book description conservation documentation accessibility affected users and Māori authority", "governed evaluation gap", "open_gap", "candidate", ["REAL-GOVERNED-HUMAN-EVALUATION"]),
    ("authority-gate", "competent-authority interlock blocks book opening treatment custody reproduction workplace cultural and Māori-authority actions", "professional rights and authority gate", "exact_gate", "exact_approval", ["EXACT-ACTION-SPECIFIC-AUTHORITY"]),
    ("stage20-nonpromotion", "Stage 20 promotion remains barred by a terminal matrix covering every synthetic book-control outcome", "Stage 20 terminal interlock", "exact_gate", "exact_approval", ["EXACT-STAGE20-EVIDENCE-AND-AUTHORITY"]),
]

SAFE_TITLES = [
    "freeze exact Vesper source anchors and activation overlay",
    "freeze declared 5830-row proposal-chain boundary",
    "freeze bounded 80-row local comparison sample",
    "record accessible-corpus title identifier and occurrence limits",
    "select twenty inherited rows for zero-credit revalidation",
    "freeze forty genuinely new hand-bound-book proposals",
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
    "build binding and gathering role graph",
    "build collation-formula token register",
    "build leaf-page-folio semantic firewall",
    "build signature-marking contract",
    "build leaf-position state ledger",
    "build section sequence model",
    "build binding-documentation transition graph",
    "build sewing-structure vacancy register",
    "build pagination-range rejection shield",
    "build ordered collation-event trace",
    "build fixed gathering-grid fixture",
    "build bounded catchword-position fixture",
    "build collation-ratio transform record",
    "build reading-order reference frame",
    "build collation-notation vacancy ledger",
    "build book-condition uncertainty envelope",
    "build deformation-observation vacancy ledger",
    "build material and structure vacancy profile",
    "build condition-to-action firewall",
    "build zero-treatment lock",
    "build handling and safety reservation",
    "build text and image rights firewall",
    "build custody and attribution abstention",
    "build bitemporal correction chain",
    "build canonical JSON profile",
    "build accessible collation traversal",
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
    "evaluate official book-preservation vocabulary without object or collection claim",
    "evaluate synthetic gathering intervals without physical-collation inference",
    "evaluate documentation-state reachability without conservation-feasibility claim",
    "evaluate exact collation tokens without bibliographical authority",
    "evaluate gathering-grid structure without inspection certification",
    "evaluate pagination-range refusal without cataloguing certification",
    "evaluate uncertainty vocabulary without material-diagnosis claim",
    "evaluate condition vocabulary without conservation advice",
    "evaluate text and image firewall without rights interpretation",
    "evaluate provenance vocabulary without ownership transfer",
    "evaluate canonical JSON without signature or security claim",
    "evaluate structural accessibility without completeness claim",
    "evaluate zero-person privacy purpose ledger without compliance claim",
    "evaluate bitemporal correction without adjudication authority",
    "evaluate current official collection adapter at zero calls",
    "evaluate THOS state-and-interval proxy without effectiveness inference",
    "evaluate GMUT topology analogy without empirical conversion",
    "evaluate GMUT constraint obligations without fitted parameters",
    "evaluate zero-key Freed ID envelope",
    "evaluate CBR challenge ladder without remedy decision",
    "evaluate cross-pillar evidence-account nontransfer",
    "evaluate rare-book collation lens without bibliographer authority",
    "evaluate reversible conservation documentation without conservator authority",
    "evaluate software verification lens without certification",
    "evaluate three D-isolated Python packages",
    "evaluate exact Git-blob lineage manifests",
    "evaluate five-class privacy candidate scanner",
    "evaluate professional and affected-party review reservation",
    "evaluate Māori-authority reservation and wording hold",
    "evaluate terminal Stage 20 nonpromotion interlock",
]

SKILL_TITLES = [
    "ghc-family-book-documentation-capsule",
    "ghc-family-book-gathering-role-graph",
    "ghc-family-book-collation-formula-register",
    "ghc-family-book-leaf-folio-firewall",
    "ghc-family-book-signature-marking-contract",
    "ghc-family-book-leaf-position-state",
    "ghc-family-book-section-sequence-model",
    "ghc-family-book-binding-state-graph",
    "ghc-family-book-sewing-structure-vacancy",
    "ghc-family-book-pagination-range-shield",
    "ghc-family-book-collation-event-trace",
    "ghc-family-book-gathering-grid-fixture",
    "ghc-family-book-catchword-cycle-fixture",
    "ghc-family-book-collation-ratio-transform",
    "ghc-family-book-reading-order-reference-frame",
    "ghc-family-book-notation-vocabulary-vacancy",
    "ghc-family-book-condition-uncertainty-envelope",
    "ghc-family-book-condition-action-firewall",
    "ghc-family-book-accessible-collation-traversal",
    "ghc-family-book-evidence-account",
]

RUNNER_TITLES = [title.replace("ghc-family-", "ghc_family_").replace("-", "_") for title in SKILL_TITLES]

REFINE_TITLES = [
    "retain exact predecessor anchors and direct-parent chain",
    "retain predecessor seal and external activation overlay separately",
    "replace stale predecessor constants with v671 source truth",
    "replace broad history scans with exact predecessor Git blobs",
    "state accessible comparison corpus limitations",
    "separate sampled comparison rows from declared chain totals",
    "separate inherited revalidation from Lyren novelty",
    "separate planning counts from completion credit",
    "separate x1 artifacts from x2 results",
    "separate source vocabulary from object observation",
    "separate synthetic identifiers from real accession numbers",
    "separate binding component roles from physical inspection",
    "separate collation notation from bibliographical claims",
    "separate leaf-page-folio roles from pagination invention",
    "separate signature tokens from real mark transcription",
    "separate section intervals from real collation",
    "separate documentation-state reachability from conservation feasibility",
    "separate synthetic gathering grids from object structure truth",
    "separate catchword positions from textual authenticity",
    "separate reading-order vocabulary from inspection",
    "separate notation placeholders from observed leaf counts",
    "separate condition uncertainty from material diagnosis",
    "separate deformation vacancies from intervention decisions",
    "separate materials vocabulary from material identification",
    "separate condition vocabulary from treatment",
    "separate safety reservations from risk release",
    "separate text and images from reproduction rights",
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
    "separate synthetic collation sequences from professional competence",
    "separate rare-book documentation from professional authority",
    "add zero-real-person counter",
    "add zero-real-book binding leaf and collection counter",
    "add zero-real-text image and transcription counter",
    "add zero-real-measurement counter",
    "add zero-opening collation pagination and sampling counter",
    "add zero-handling repair rebinding and treatment counter",
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
    "bind prospective route only to Ilyra Fen exact title after terminal gate",
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
        "need": "model bounded synthetic gathering and leaf ranges gaps overlaps adjacency and condition uncertainty envelopes",
    },
    {
        "name": "transitions",
        "version": "0.9.3",
        "registry": "https://pypi.org/project/transitions/0.9.3/",
        "license_metadata": "MIT (registry metadata; not legal review)",
        "requires_python": "registry metadata leaves the field unspecified",
        "wheel": "transitions-0.9.3-py2.py3-none-any.whl",
        "wheel_sha256": "02463248f2b668d86f66636b1e3c9e8de84d93e22915247f4e1aa9ee1cae28aa",
        "need": "exercise bounded synthetic accession describe challenge correct handover and refusal state transitions",
    },
    {
        "name": "cattrs",
        "version": "26.1.0",
        "registry": "https://pypi.org/project/cattrs/26.1.0/",
        "license_metadata": "MIT License (registry metadata; not legal review)",
        "requires_python": ">=3.10",
        "wheel": "cattrs-26.1.0-py3-none-any.whl",
        "wheel_sha256": "d1e0804c42639494d469d08d4f26d6b9de9b8ab26b446db7b5f8c2e97f7c3096",
        "need": "structure and unstructure bounded synthetic book-collation dossier dataclasses while rejecting malformed fields",
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
    or imply the full 5,830-row chain. It compares against Vesper's forty frozen
    v671-v7 titles plus Neris's forty immediately preceding frozen titles, all
    read from exact committed Git blobs at the Vesper final.
    """
    vesper_paths = [
        f"docs/vesper-arlen/v671-v7/x1/proposal-freeze-shards/proposals-{index:02d}.json"
        for index in range(1, 9)
    ]
    neris_paths = [
        f"docs/neris-solane/v671-v6/x1/proposal-freeze-shards/proposals-{index:02d}.json"
        for index in range(1, 9)
    ]
    specs = {path: f"{SOURCE_FINAL}:{path}" for path in [*vesper_paths, *neris_paths]}
    blobs = git_batch_blobs(repo, specs)
    vesper_rows = [
        row
        for path in vesper_paths
        for row in json.loads(blobs[path].decode("utf-8")).get("rows", [])
    ]
    neris_rows = [
        row
        for path in neris_paths
        for row in json.loads(blobs[path].decode("utf-8")).get("rows", [])
    ]
    if len(vesper_rows) != SOURCE_NEIGHBOR_ROWS:
        raise ValueError(f"expected {SOURCE_NEIGHBOR_ROWS} Vesper rows, recovered {len(vesper_rows)}")
    if len(neris_rows) != SOURCE_OWNER_ROWS:
        raise ValueError(f"expected {SOURCE_OWNER_ROWS} Neris rows, recovered {len(neris_rows)}")
    rows = [
        {
            "proposal_id": f"VA6717-OWNER-{index:03d}",
            "title": str(row["title"]),
        }
        for index, row in enumerate(vesper_rows, 1)
    ]
    rows.extend(
        {
            "proposal_id": f"NS6716-OWNER-{index:03d}",
            "title": str(row["title"]),
        }
        for index, row in enumerate(neris_rows, 1)
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
                    f"docs/lyren-moss/v671-v8/x2/proposals/{proposal_id.lower()}-{slug}.json",
                    f"docs/lyren-moss/v671-v8/x2/cards/{proposal_id.lower()}-{slug}.json",
                ],
                "execution_lane": "x2_owner_local_bounded_control" if completion_lane else "held_gap_or_gate",
                "expected_disposition": disposition,
                "falsifier_or_acceptance_gate": (
                    "One bounded synthetic positive contract is accepted, four preregistered invalid mutations are rejected, and all real people, books, bindings, leaves, texts, images, measurements, opening, collation, pagination, sampling, handling, repair, rebinding, treatment, external actions, and authority actions remain zero."
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
