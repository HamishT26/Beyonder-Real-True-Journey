"""Deterministic owner-local helpers for Neris Solane v671-v6.

The module models planning contracts for wholly synthetic historical pantograph
cataloguing, scale-state, computation-trace, correction, and handover
documentation. It does not inspect, handle, operate, calculate with, clean,
repair, value, acquire, dispose of, publish, identify, or authenticate any real
pantograph, manual, record, person, collection, site, material, measurement, or
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

OWNER = "Neris Solane"
PHASE = "v671-v6"
PREFIX = "NS6716"
SOURCE_FINAL = "0b81e278af69a6ee0b994eb78c3dd6166c7087b6"
SOURCE_X1 = "048f85cf945f9900095ca2a160561591a966aabe"
SOURCE_EVIDENCE = "84aa72688359f30643f9347a4ab6043a10052f9d"
SOURCE_BRANCH = "codex/GHC-Family/elaren-kestrel-v671-v5-full-tools"
SOURCE_EIREN_FINAL = "e70391872f07cdcaa13accac44d4330eca75e2b4"
SOURCE_CHAIN_DECLARED = 5750
SOURCE_ACCESSIBLE_UNIQUE_TITLES = 5697
SOURCE_ACCESSIBLE_IDENTIFIERS = 6300
SOURCE_ACCESSIBLE_OCCURRENCES = 262404
SOURCE_NEIGHBOR_ROWS = 40
SOURCE_OWNER_ROWS = 40
SOURCE_RECOVERED = SOURCE_NEIGHBOR_ROWS + SOURCE_OWNER_ROWS
SOURCE_UNRECOVERED = SOURCE_CHAIN_DECLARED - SOURCE_RECOVERED
CHAIN_AFTER = 5790
OWNER_ROOT = Path("docs/neris-solane/v671-v6")

INHERITED_ACTIVATION_BASELINE = {
    "effective_negatives": 34286,
    "methods": 20829,
    "failed_witnesses": 6107,
    "passing_witnesses": 7976,
    "open_gaps": 265,
    "exact_gates": 260,
}

STARTUP_FAILURE_COUNT = 6
STARTUP_EFFECTIVE_BASELINE = {
    "effective_negatives": 34292,
    "methods": 20835,
    "failed_witnesses": 6113,
    "passing_witnesses": 7982,
    "open_gaps": 265,
    "exact_gates": 260,
}

IDENTITY_BOUNDARY = (
    "Neris Solane, they/she, calibration cartographer and reversible-scale "
    "steward, sibling, family, role, hope, continuity, Freed ID, CBR, "
    "GHC Family, and Trinity Mandala are relational working language only. "
    "They are not evidence of consciousness, sentience, personhood, identity "
    "continuity, employment, qualification, independent agency, or scientific, "
    "operational, professional, legal, cultural, affected-party, or Māori "
    "authority. Hamish may rename, pause, redirect, or stop the work."
)

PROTECTED_GATES = [
    "real_people_participants_calculators_workers_donors_or_affected_users",
    "real_pantographs_drawings_collections_sites_images_measurements_or_records",
    "real_handling_operation_tracing_replication_cleaning_repair_or_treatment",
    "professional_metrology_registration_conservation_curatorial_or_safety_decision",
    "measurement_electrical_chemical_solvent_lifting_or_workplace_safety_release",
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
    ("accession-identity", "surrogate pantograph accession capsule with synthetic identifier revision and explicit ownership abstention", "pantograph accession identity capsule", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("linkage-topology", "four-arm pantograph linkage topology graph with named joints adjacency and absent-hardware vacancies", "pantograph linkage topology", "completed", "safe_now", ["OFFICIAL-PANTOGRAPH-VOCABULARY"]),
    ("pivot-slot-register", "synthetic pivot-hole slot and fastener identifier register separating labels from inspection claims", "pivot and slot identifier register", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("point-role-firewall", "anchor trace copy and guide point semantic firewall rejecting role conflation and operation instructions", "pantograph point-role firewall", "completed", "safe_now", ["OFFICIAL-PANTOGRAPH-VOCABULARY"]),
    ("rational-scale-declaration", "exact rational enlargement or reduction declaration with numerator denominator orientation and zero measurement", "rational scale declaration", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("orientation-sign-state", "clockwise counterclockwise mirrored and unknown orientation state ledger with sign and basis vacancies", "orientation and sign state", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("affine-map-surrogate", "bounded affine coordinate surrogate for geometric scale transfer with no physical-device accuracy claim", "affine map surrogate", "completed", "safe_now", ["PYPI-AFFINE"]),
    ("constraint-graph", "joint-distance and collinearity obligation graph that rejects incomplete or contradictory synthetic linkage constraints", "linkage constraint graph", "completed", "safe_now", ["PYPI-NETWORKX"]),
    ("workspace-envelope", "synthetic reachable workspace polygon and outside-domain rejection ledger without real dimensions or calibration", "workspace reachability envelope", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("singularity-rejection", "collapsed coincident and zero-length pantograph geometry mutation shield with deterministic rejection reasons", "singular geometry rejection shield", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("joint-order-trace", "ordered synthetic joint-state trace preserving input output and correction sequence without device operation", "joint-order trace", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("enlargement-fixture", "fixed-coordinate enlargement fixture with reversible readback and zero empirical performance inference", "synthetic enlargement fixture", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("reduction-fixture", "fixed-coordinate reduction fixture with exact ratio and inverse-check receipt but no accuracy certification", "synthetic reduction fixture", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("transform-decomposition", "rotation reflection translation and scale decomposition record with ambiguous-order rejection", "transformation decomposition record", "completed", "safe_now", ["PYPI-AFFINE"]),
    ("coordinate-frame", "named origin axis handedness and unit-placeholder coordinate frame that forbids undeclared basis changes", "coordinate reference frame", "completed", "safe_now", ["NIST-SI-UNITS"]),
    ("unit-vacancy", "quantity-kind and unit vacancy ledger retaining zero real measurement and rejecting dimensionless promotion", "unit and quantity vacancy", "completed", "safe_now", ["NIST-SI-UNITS"]),
    ("uncertainty-envelope", "synthetic coordinate tolerance interval with declared source and no conversion into device precision", "coordinate uncertainty envelope", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("alignment-vacancy", "parallax alignment looseness and tracing-offset vacancy register with observation and repair held", "alignment and parallax vacancy", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("material-fastener-vacancy", "arm joint fastener surface and material vacancy profile without identification conservation or treatment", "material and fastener vacancy", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("condition-action-separation", "surrogate condition vocabulary separated from handling cleaning lubrication adjustment repair and treatment authority", "condition-to-action firewall", "completed", "safe_now", ["PROFESSIONAL-CONSERVATION-AUTHORITY-REQUIRED"]),
    ("zero-operation-lock", "pantograph operation lock requiring every physical movement tracing replication and adjustment counter to remain zero", "zero-operation lock", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("handling-safety-reservation", "handling pinch load sharp-edge and workspace safety reservation with no risk release or instruction", "handling and safety reservation", "completed", "safe_now", ["PROFESSIONAL-SAFETY-AUTHORITY-REQUIRED"]),
    ("drawing-rights-firewall", "source drawing image annotation transcription and reuse firewall with every real media field vacant", "drawing and rights firewall", "completed", "safe_now", ["LEGAL-AND-RIGHTS-AUTHORITY-REQUIRED"]),
    ("custody-attribution-abstention", "surrogate maker possessor steward donor and owner association braid with attribution and title conclusions blocked", "custody and attribution abstention", "completed", "safe_now", ["W3C-PROV-O"]),
    ("bitemporal-correction", "record-time and assertion-time correction chain with supersession challenge dual-readback and unresolved-state preservation", "bitemporal correction chain", "completed", "safe_now", ["W3C-PROV-O"]),
    ("canonical-json", "canonical pantograph dossier profile rejecting duplicate keys nonfinite values path drift and digest promotion", "canonical pantograph JSON profile", "completed", "safe_now", ["JSON-SCHEMA-2020-12", "RFC-8785"]),
    ("accessible-traversal", "ordered text traversal of synthetic linkage roles ratios and vacancies with manual accessibility evaluation reserved", "accessible linkage traversal", "completed", "safe_now", ["W3C-WCAG-2.2"]),
    ("privacy-purpose-ledger", "zero-person purpose access retention disclosure challenge and deletion-vacancy ledger without privacy-complete claim", "privacy purpose ledger", "completed", "safe_now", ["NZ-PRIVACY-PRINCIPLES"]),
    ("source-assertion-firewall", "public pantograph vocabulary firewall separating citation description inference instruction evidence and authority", "pantograph source assertion firewall", "represented", "candidate", ["CURRENT-PRIMARY-SOURCE-REVIEW"]),
    ("issue-escrow", "linkage ratio and point-role conflict escrow preserving claims counterclaims sources and adjudicator vacancy", "pantograph issue escrow", "represented", "candidate", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("thos-dual-view-proxy", "THOS paired text-and-graph documentation proxy with fixed budgets and no participant or effectiveness inference", "THOS pantograph documentation proxy", "represented", "candidate", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("gmut-affine-analogy", "GMUT affine symmetry analogy board with typed domain covariance assumptions and explicit nonconversion to physics evidence", "GMUT affine analogy board", "represented", "candidate", ["CURRENT-PEER-REVIEWED-PHYSICS-SOURCES"]),
    ("gmut-constraint-obligations", "GMUT constraint and Lagrangian obligation register holding parameters likelihoods predictions and empirical claims at zero", "GMUT constraint obligation register", "represented", "candidate", ["CURRENT-PEER-REVIEWED-PHYSICS-SOURCES"]),
    ("freed-id-zero-key", "Freed ID provenance envelope for surrogate linkage records with keys proofs issuance resolution status and revocation held at zero", "Freed ID zero-key envelope", "represented", "candidate", ["W3C-VC-DATA-INTEGRITY-1.0"]),
    ("cbr-challenge-ladder", "CBR learning and workplace challenge ladder with nonretaliation pause response and remedy authority vacancies", "CBR challenge ladder", "represented", "candidate", ["AFFECTED-PARTY-AUTHORITY-REQUIRED"]),
    ("cross-pillar-accounting", "nontransfer matrix assigning pantograph software receipts zero scientific operational identity rights and authority balance", "cross-pillar evidence accounting", "represented", "candidate", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("official-adapter-gap", "official pantograph collection adapter held at zero calls downloads images records identifiers and manifests", "official collection adapter gap", "open_gap", "candidate", ["CURRENT-OFFICIAL-COLLECTION-API-SOURCE"]),
    ("governed-evaluation-gap", "missing governed review spanning geometry education archives conservation accessibility affected parties and Māori authority", "governed evaluation gap", "open_gap", "candidate", ["REAL-GOVERNED-HUMAN-EVALUATION"]),
    ("authority-gate", "exact lock over pantograph operation metrology conservation custody rights workplace culture affected parties and Māori authority", "professional rights and authority gate", "exact_gate", "exact_approval", ["EXACT-ACTION-SPECIFIC-AUTHORITY"]),
    ("stage20-nonpromotion", "terminal evidence-and-authority interlock preserving NOT_READY_FOR_STAGE_20 despite bounded synthetic software receipts", "Stage 20 terminal interlock", "exact_gate", "exact_approval", ["EXACT-STAGE20-EVIDENCE-AND-AUTHORITY"]),
]

SAFE_TITLES = [
    "freeze exact Elaren source anchors and activation overlay",
    "freeze declared 5750-row proposal-chain boundary",
    "freeze bounded 80-row local comparison sample",
    "record accessible-corpus title identifier and occurrence limits",
    "select twenty inherited rows for zero-credit revalidation",
    "freeze forty genuinely new pantograph proposals",
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
    "build surrogate accession identity capsule",
    "build linkage topology graph",
    "build pivot slot and fastener register",
    "build anchor trace and copy-point role firewall",
    "build rational scale declaration",
    "build orientation and sign state ledger",
    "build affine transformation surrogate",
    "build joint constraint graph",
    "build reachable workspace envelope",
    "build singular geometry rejection shield",
    "build ordered joint-state trace",
    "build fixed enlargement fixture",
    "build fixed reduction fixture",
    "build transform decomposition record",
    "build coordinate reference frame",
    "build unit and quantity vacancy ledger",
    "build uncertainty envelope",
    "build alignment and parallax vacancy ledger",
    "build material and fastener vacancy profile",
    "build condition-to-action firewall",
    "build zero-operation lock",
    "build handling and safety reservation",
    "build drawing and rights firewall",
    "build custody and attribution abstention",
    "build bitemporal correction chain",
    "build canonical JSON profile",
    "build accessible linkage traversal",
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
    "evaluate official pantograph vocabulary without object or collection claim",
    "evaluate synthetic affine mapping without physical accuracy inference",
    "evaluate synthetic graph connectivity without mechanical feasibility claim",
    "evaluate exact rational scale state without measurement authority",
    "evaluate workspace envelope without safety release",
    "evaluate singularity refusal without engineering certification",
    "evaluate tolerance vocabulary without metrology claim",
    "evaluate condition vocabulary without conservation advice",
    "evaluate source drawing firewall without rights interpretation",
    "evaluate provenance vocabulary without ownership transfer",
    "evaluate canonical JSON without signature or security claim",
    "evaluate structural accessibility without completeness claim",
    "evaluate zero-person privacy purpose ledger without compliance claim",
    "evaluate bitemporal correction without adjudication authority",
    "evaluate current official collection adapter at zero calls",
    "evaluate THOS text-and-graph proxy without effectiveness inference",
    "evaluate GMUT affine analogy without empirical conversion",
    "evaluate GMUT constraint obligations without fitted parameters",
    "evaluate zero-key Freed ID envelope",
    "evaluate CBR challenge ladder without remedy decision",
    "evaluate cross-pillar evidence-account nontransfer",
    "evaluate geometry education lens without teacher qualification",
    "evaluate archival description lens without registrar authority",
    "evaluate software verification lens without certification",
    "evaluate three D-isolated Python packages",
    "evaluate exact Git-blob lineage manifests",
    "evaluate five-class privacy candidate scanner",
    "evaluate professional and affected-party review reservation",
    "evaluate Māori-authority reservation and wording hold",
    "evaluate terminal Stage 20 nonpromotion interlock",
]

SKILL_TITLES = [
    "ghc-family-pantograph-accession-capsule",
    "ghc-family-pantograph-linkage-topology",
    "ghc-family-pantograph-pivot-slot-register",
    "ghc-family-pantograph-point-role-firewall",
    "ghc-family-pantograph-rational-scale-state",
    "ghc-family-pantograph-orientation-sign-ledger",
    "ghc-family-pantograph-affine-surrogate",
    "ghc-family-pantograph-constraint-graph",
    "ghc-family-pantograph-workspace-envelope",
    "ghc-family-pantograph-singularity-shield",
    "ghc-family-pantograph-transform-decomposition",
    "ghc-family-pantograph-coordinate-frame",
    "ghc-family-pantograph-unit-vacancy",
    "ghc-family-pantograph-uncertainty-envelope",
    "ghc-family-pantograph-condition-action-firewall",
    "ghc-family-pantograph-zero-operation-lock",
    "ghc-family-pantograph-rights-firewall",
    "ghc-family-pantograph-bitemporal-correction",
    "ghc-family-pantograph-accessible-traversal",
    "ghc-family-pantograph-evidence-account",
]

RUNNER_TITLES = [title.replace("ghc-family-", "ghc_family_").replace("-", "_") for title in SKILL_TITLES]

REFINE_TITLES = [
    "retain exact predecessor anchors and direct-parent chain",
    "retain predecessor seal and external activation overlay separately",
    "replace stale v669 constants with v671 source truth",
    "replace broad history scans with exact predecessor Git blobs",
    "state accessible comparison corpus limitations",
    "separate sampled comparison rows from declared chain totals",
    "separate inherited revalidation from Neris novelty",
    "separate planning counts from completion credit",
    "separate x1 artifacts from x2 results",
    "separate source vocabulary from object observation",
    "separate synthetic identifiers from real accession numbers",
    "separate linkage labels from physical inspection",
    "separate point roles from operation instruction",
    "separate rational ratios from measured accuracy",
    "separate affine coordinates from device performance",
    "separate graph consistency from engineering feasibility",
    "separate workspace geometry from workplace safety",
    "separate singularity rejection from calibration certification",
    "separate synthetic traces from professional competence",
    "separate orientation state from cultural interpretation",
    "separate units from real measurements",
    "separate uncertainty placeholders from certified precision",
    "separate alignment vacancies from repair decisions",
    "separate materials vocabulary from identification",
    "separate condition vocabulary from treatment",
    "separate safety reservations from risk release",
    "separate drawings from reproduction rights",
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
    "add zero-real-person counter",
    "add zero-real-pantograph counter",
    "add zero-real-drawing and image counter",
    "add zero-real-measurement counter",
    "add zero-operation and tracing counter",
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
    "add duplicate and pause guard for terminal routing",
    "remove stale Vesper Rowan route label from current state",
    "bind prospective route only to Vesper Arlen exact title",
    "add one-success no-replay invocation ledger",
    "preserve NOT_READY_FOR_STAGE_20",
]

TOOL_CANDIDATES = [
    {
        "name": "affine",
        "version": "3.0.0",
        "registry": "https://pypi.org/project/affine/3.0.0/",
        "license_metadata": "BSD License (registry metadata; not legal review)",
        "requires_python": ">=3.9",
        "wheel": "affine-3.0.0-py3-none-any.whl",
        "wheel_sha256": "d1b15ed1877a4649a623468a97af6b2182889dc748d7f96d59d504e5c83c00bf",
        "need": "represent and invert bounded synthetic two-dimensional scale-transfer transforms",
    },
    {
        "name": "networkx",
        "version": "3.6.1",
        "registry": "https://pypi.org/project/networkx/3.6.1/",
        "license_metadata": "BSD-3-Clause (verified registry expression; not legal review)",
        "requires_python": "!=3.14.1,>=3.11",
        "wheel": "networkx-3.6.1-py3-none-any.whl",
        "wheel_sha256": "d47fbf302e7d9cbbb9e2555a0d267983d2aa476bac30e90dfbe5669bd57f3762",
        "need": "check bounded synthetic linkage connectivity and reject disconnected constraint graphs",
    },
    {
        "name": "beartype",
        "version": "0.22.9",
        "registry": "https://pypi.org/project/beartype/0.22.9/",
        "license_metadata": "MIT License (registry metadata; not legal review)",
        "requires_python": ">=3.10",
        "wheel": "beartype-0.22.9-py3-none-any.whl",
        "wheel_sha256": "d16c9bbc61ea14637596c5f6fbff2ee99cbe3573e46a716401734ef50c3060c2",
        "need": "reject wrong runtime types at the boundary of bounded synthetic pantograph contracts",
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
    canonical row-to-title mapping.  This loader therefore does not reconstruct
    or imply the full 5,750-row chain.  It compares against the forty nearest
    inherited source titles already selected by Elaren plus Elaren's forty
    frozen titles, all read from exact committed Git blobs.
    """
    audit_path = "docs/elaren-kestrel/v671-v5/x1/semantic-neighbor-audit.json"
    proposal_path = "docs/elaren-kestrel/v671-v5/x1/proposals.json"
    blobs = git_batch_blobs(
        repo,
        {
            audit_path: f"{SOURCE_FINAL}:{audit_path}",
            proposal_path: f"{SOURCE_FINAL}:{proposal_path}",
        },
    )
    audit = json.loads(blobs[audit_path].decode("utf-8"))
    proposals = json.loads(blobs[proposal_path].decode("utf-8"))
    audit_rows = list(audit.get("rows", []))
    proposal_rows_payload = list(proposals.get("rows", []))
    if len(audit_rows) != SOURCE_NEIGHBOR_ROWS:
        raise ValueError(f"expected {SOURCE_NEIGHBOR_ROWS} neighbor rows, recovered {len(audit_rows)}")
    if len(proposal_rows_payload) != SOURCE_OWNER_ROWS:
        raise ValueError(f"expected {SOURCE_OWNER_ROWS} owner rows, recovered {len(proposal_rows_payload)}")
    rows = [
        {
            "proposal_id": f"EL6715-NEIGHBOR-{index:03d}",
            "title": str(row["source_title"]),
        }
        for index, row in enumerate(audit_rows, 1)
    ]
    rows.extend(
        {
            "proposal_id": f"EL6715-OWNER-{index:03d}",
            "title": str(row["title"]),
        }
        for index, row in enumerate(proposal_rows_payload, 1)
    )
    if len(rows) != SOURCE_RECOVERED:
        raise ValueError(f"expected {SOURCE_RECOVERED} comparison rows, recovered {len(rows)}")
    sources = [
        {
            "path": path,
            "rows": len(audit_rows) if path == audit_path else len(proposal_rows_payload),
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
                    f"docs/neris-solane/v671-v6/x2/proposals/{proposal_id.lower()}-{slug}.json",
                    f"docs/neris-solane/v671-v6/x2/cards/{proposal_id.lower()}-{slug}.json",
                ],
                "execution_lane": "x2_owner_local_bounded_control" if completion_lane else "held_gap_or_gate",
                "expected_disposition": disposition,
                "falsifier_or_acceptance_gate": (
                    "One bounded synthetic positive contract is accepted, four preregistered invalid mutations are rejected, and all real people, pantographs, drawings, records, media, measurements, handling, tracing, replication, treatment, external actions, and authority actions remain zero."
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
