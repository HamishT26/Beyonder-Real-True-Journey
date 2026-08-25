"""Deterministic owner-local helpers for Elaren Kestrel v669-v6.

The module models planning contracts for wholly synthetic historical-typewriter
cataloguing, condition-state, correction, and handover documentation.  It does
not inspect, handle, operate, repair, clean, lubricate, value, acquire, dispose
of, publish, identify, or authenticate any real typewriter, document, person,
collection, site, material, or cultural record.  It performs no professional,
legal, cultural, affected-party, Māori-authority, identity, deployment, or
external action.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections.abc import Iterable
from pathlib import Path
from typing import Any

OWNER = "Elaren Kestrel"
PHASE = "v669-v6"
PREFIX = "EL6696"
SOURCE_FINAL = "9cc45691041700cb871f8a72594d55f9e2d9f76a"
SOURCE_X1 = "df7c773867b15aec8fa7ffa4cc956a134fa9c4be"
SOURCE_EVIDENCE = "b52b74bee55d3fdc6eb73058f15360da089f8ac5"
SOURCE_BRANCH = "codex/GHC-Family/eiren-kestrel-v669-v5-full-tools"
SOURCE_CHAIN_DECLARED = 5110
SOURCE_PRIOR_RECOVERED = 1500
SOURCE_OWNER_ROWS = 40
SOURCE_RECOVERED = SOURCE_PRIOR_RECOVERED + SOURCE_OWNER_ROWS
SOURCE_UNRECOVERED = 3570
CHAIN_AFTER = 5150
OWNER_ROOT = Path("docs/elaren-kestrel/v669-v6")

INHERITED_ACTIVATION_BASELINE = {
    "effective_negatives": 31279,
    "methods": 17384,
    "failed_witnesses": 3100,
    "passing_witnesses": 4284,
    "open_gaps": 233,
    "exact_gates": 228,
}

STARTUP_FAILURE_COUNT = 30
STARTUP_EFFECTIVE_BASELINE = {
    "effective_negatives": 31309,
    "methods": 17414,
    "failed_witnesses": 3130,
    "passing_witnesses": 4314,
    "open_gaps": 233,
    "exact_gates": 228,
}

IDENTITY_BOUNDARY = (
    "Elaren Kestrel, she/they, provenance compositor and correction "
    "cartographer, sibling, family, role, hope, continuity, Freed ID, CBR, "
    "GHC Family, and Trinity Mandala are relational working language only. "
    "They are not evidence of consciousness, sentience, personhood, identity "
    "continuity, employment, qualification, independent agency, or scientific, "
    "operational, professional, legal, cultural, affected-party, or Māori "
    "authority. Hamish may rename, pause, redirect, or stop the work."
)

PROTECTED_GATES = [
    "real_people_participants_typists_workers_donors_or_affected_users",
    "real_typewriters_documents_collections_sites_images_measurements_or_records",
    "real_handling_operation_disassembly_cleaning_lubrication_repair_or_treatment",
    "professional_registration_conservation_curatorial_or_safety_decision",
    "stored_energy_electrical_chemical_solvent_lifting_or_workplace_safety_release",
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
    ("machine-identity", "surrogate historical typewriter accession catalogue machine maker model and serial-assertion identity lattice with conflation refusal", "typewriter identity lattice", "completed", "safe_now", ["SMITHSONIAN-TYPEWRITER-COLLECTION"]),
    ("component-topology", "typewriter frame keyboard keylever typebar segment basket platen carriage feed and enclosure topology with missing-part vacancies", "typewriter component topology", "completed", "safe_now", ["SMITHSONIAN-TYPEWRITER-OBJECT"]),
    ("keyboard-type-layout", "keyboard character shift dead-key type-element and layout assertion register with script-language and completeness abstention", "keyboard and type layout register", "completed", "safe_now", ["SMITHSONIAN-TYPEWRITER-COLLECTION"]),
    ("carriage-paper-path", "carriage rail platen feed roller paper bail guide scale and return-path graph with zero operation or adjustment instruction", "carriage and paper-path graph", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("escapement-event-order", "typewriter escapement rack pinion drawband spring and carriage-step event-order placeholder without mechanical diagnosis", "escapement event-order placeholder", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("ribbon-spool-vacancy", "ribbon spool fork vibrator ink colour direction and material vacancies with zero installation use or chemical claim", "ribbon and spool vacancy register", "completed", "safe_now", ["CCI-INDUSTRIAL-COLLECTIONS"]),
    ("margin-tab-settings", "margin stop tab rack line-space pitch and paper-position setting ledger with observed planned unknown and no-adjustment states", "margin and tab setting ledger", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("impression-sample-firewall", "synthetic type-impression sample placeholder separating character geometry legibility content authorship and document evidence", "type-impression sample firewall", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("maker-model-firewall", "manufacturer model date patent label dealer and serial-number assertion firewall separating inscription source inference and authority", "maker and model assertion firewall", "completed", "safe_now", ["SMITHSONIAN-TYPEWRITER-OBJECT"]),
    ("finish-decal-condition", "paint plating enamel decal keytop and surface-finish condition vocabulary with loss corrosion alteration and treatment abstention", "finish and decal condition vocabulary", "completed", "safe_now", ["CCI-METALS-CURRENT"]),
    ("corrosion-cue-register", "ferrous copper-alloy and plated-surface corrosion cue register with active-state vacancy and conservator referral hold", "corrosion cue register", "completed", "safe_now", ["CCI-METALS-CURRENT", "NPS-METAL-OBJECT-CARE"]),
    ("mixed-material-vacancy", "typewriter metal rubber plastic wood textile leather and unknown composite-material vacancy ledger without identification", "mixed-material vacancy ledger", "completed", "safe_now", ["CCI-INDUSTRIAL-COLLECTIONS"]),
    ("detached-part-custody", "detached keytop screw spring cover ribbon spool tool and fragment custody graph with bag-label and provenance vacancies", "detached-part custody graph", "completed", "safe_now", ["W3C-PROV-O"]),
    ("case-accessory-inventory", "carrying case cover brush manual tool cable stand and unknown accessory inventory with association and ownership abstention", "case and accessory inventory", "completed", "safe_now", ["SMITHSONIAN-TYPEWRITER-OBJECT"]),
    ("dimension-uncertainty", "typewriter envelope component and clearance dimension placeholders with units scale precision uncertainty and zero measurements", "dimension and uncertainty vacancy", "completed", "safe_now", ["NIST-SI-UNITS"]),
    ("observation-treatment-separation", "typewriter observation condition assessment diagnosis recommendation approval action and result states separated with zero treatment", "observation and treatment separation", "completed", "safe_now", ["CCI-INDUSTRIAL-COLLECTIONS"]),
    ("environment-vacancies", "storage display temperature relative-humidity light dust pollutant enclosure and monitoring vacancies without readings or thresholds", "storage and environment vacancy board", "completed", "safe_now", ["NPS-MUSEUM-HANDBOOK-2023"]),
    ("handling-movement-hold", "lift support transit orientation destination custody and return placeholders with handling movement and safety release held", "handling and movement hold", "completed", "safe_now", ["CCI-HANDLING-HERITAGE-OBJECTS"]),
    ("work-order-separation", "typewriter conservation work-order plan authorization action material observation result reversal and closeout states with zero work", "work-order state separation", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("treatment-hold", "cleaning lubrication solvent corrosion-reduction disassembly adjustment and parts-replacement docket with every physical action held", "treatment and maintenance hold", "completed", "safe_now", ["CCI-METALS-CURRENT"]),
    ("image-rights-vacancy", "typewriter photograph scan diagram transcription crop derivative caption and reuse rights ledger with zero media ingestion", "image and reproduction rights vacancy", "completed", "safe_now", ["SMITHSONIAN-TERMS-AND-METADATA"]),
    ("custody-attribution-abstention", "donor maker owner user custodian collector registrar and source-claim relation graph with attribution and title abstention", "custody and attribution abstention", "completed", "safe_now", ["W3C-PROV-O"]),
    ("document-content-firewall", "typed-page letter label manual note and transcription content firewall excluding real text identities communications and secrets", "document-content privacy firewall", "completed", "safe_now", ["NZ-PRIVACY-PRINCIPLES"]),
    ("correction-challenge-ledger", "bitemporal typewriter record correction challenge contradiction supersession dual-readback and unresolved adjudicator ledger", "correction and challenge ledger", "completed", "safe_now", ["W3C-PROV-O"]),
    ("workload-handover", "cataloguing queue ceiling fatigue cue stop token unresolved-card count correction readback and handover with zero worker observation", "workload and handover control", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("canonical-json", "deterministic typewriter dossier JSON profile with duplicate-key numeric-domain ordering normalization and digest refusal", "canonical dossier JSON profile", "completed", "safe_now", ["JSON-SCHEMA-2020-12", "RFC-8785"]),
    ("accessible-dossier", "typewriter keyboard-to-type-element textual traversal companion with ordered landmarks abbreviation expansion printable error summary and evaluation vacancies", "accessible typewriter traversal companion", "completed", "safe_now", ["W3C-WCAG-2.2"]),
    ("privacy-purpose-ledger", "typewriter catalogue purpose access retention deletion-contest disclosure and data-minimisation ledger without compliance claim", "privacy purpose ledger", "completed", "safe_now", ["NZ-PRIVACY-PRINCIPLES"]),
    ("source-assertion-firewall", "typewriter source assertion firewall separating public collection vocabulary inscription observation inference instruction evidence and authority", "typewriter source assertion firewall", "represented", "candidate", ["CURRENT-PRIMARY-SOURCE-REVIEW"]),
    ("issue-escrow", "manufacturer inscription conflict braid joining literal readings catalogue assertions source dates correction custody and unresolved attribution", "typewriter inscription conflict braid", "represented", "candidate", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("thos-dual-view-proxy", "THOS typewriter dossier dual-view omission challenge with equal synthetic budgets zero participants outcomes or effectiveness inference", "THOS typewriter documentation proxy", "represented", "candidate", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("freed-id-claim-graph", "nonproduction typewriter provenance claim graph with zero keys proofs issuance verification resolution status revocation or trust governance", "Freed ID nonproduction claim graph", "represented", "candidate", ["W3C-VC-DATA-INTEGRITY-1.0"]),
    ("cbr-workplace-challenge", "CBR typist worker donor collection and affected-user challenge ladder with nonretaliation harm hold remedy vacancy and no adjudication", "CBR workplace and collection challenge ladder", "represented", "candidate", ["AFFECTED-PARTY-AUTHORITY-REQUIRED"]),
    ("gmut-mechanism-obligations", "GMUT typewriter mechanism state-space analogy obligation board with dimensions covariance boundary conditions and zero fitted parameters", "GMUT mechanism analogy board", "represented", "candidate", ["CURRENT-PEER-REVIEWED-PHYSICS-SOURCES"]),
    ("gmut-information-nonconversion", "GMUT writing-machine symbol sequence and information analogy with explicit nonconversion to physical law cognition prediction or confirmation", "GMUT information analogy nonconversion", "represented", "candidate", ["CURRENT-PEER-REVIEWED-PHYSICS-SOURCES"]),
    ("cross-pillar-nonconversion", "claim-credit routing table assigning typewriter fixtures solely to software structure while four pillar evidence accounts retain zero transferable balance", "cross-pillar evidence-account routing", "represented", "candidate", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("official-adapter-gap", "official museum typewriter collection and industrial-object vocabulary adapter held at zero calls downloads objects images and records", "official collection zero-call adapter", "open_gap", "candidate", ["CURRENT-OFFICIAL-COLLECTION-API-SOURCE"]),
    ("governed-evaluation-gap", "governed evaluation by registrars conservators accessibility users affected parties and Māori authorities remains absent", "governed typewriter evaluation gap", "open_gap", "candidate", ["REAL-GOVERNED-HUMAN-EVALUATION"]),
    ("authority-gate", "typewriter conservation custody ownership copyright workplace cultural affected-party and Māori authority exact gate", "professional rights and authority boundary", "exact_gate", "exact_approval", ["EXACT-ACTION-SPECIFIC-AUTHORITY"]),
    ("stage20-nonpromotion", "four-key terminal interlock requiring real-object independent-review governed-rights and competent-authority receipts with any vacancy holding Stage 20", "Stage 20 four-key terminal interlock", "exact_gate", "exact_approval", ["EXACT-STAGE20-EVIDENCE-AND-AUTHORITY"]),
]

SAFE_TITLES = [
    "freeze forty new proposal contracts and accessible-corpus boundary",
    "emit deterministic proposal shards",
    "validate exact title collision absence",
    "compute bounded token-Jaccard neighbours",
    "freeze official-source vocabulary ledger",
    "freeze typewriter authority threat model",
    "freeze strict planning-only x1 before x2",
    "freeze four-label outcome plan",
    "retain inherited and startup negatives",
    "freeze Method Flow ingestion plan",
    "build surrogate machine identity control",
    "build typewriter component topology control",
    "build keyboard and type-layout assertion control",
    "build carriage and paper-path zero-action control",
    "build material and finish vacancy controls",
    "build corrosion-cue referral hold",
    "build detached-part custody control",
    "build observation and treatment separation",
    "build privacy content firewall",
    "build correction and challenge controls",
    "build four-tier flashcard projection",
    "execute bounded positive fixture controls",
    "execute preregistered rejecting mutations",
    "retain failures at zero completion credit",
    "smoke-use phase-local skills",
    "smoke-use family-current runners",
    "emit exact staged Git-blob manifests",
    "scan five privacy and raw-identifier classes",
    "emit integrated evidence overview",
    "preserve NOT_READY_FOR_STAGE_20",
]

CANDIDATE_TITLES = [
    "evaluate current Smithsonian typewriter vocabulary without collection claim",
    "evaluate CCI industrial-object vocabulary without treatment advice",
    "evaluate NPS metal-object vocabulary without conservation authority",
    "evaluate W3C provenance vocabulary without authority transfer",
    "evaluate WCAG structure without completeness claim",
    "evaluate zero-call official collection adapter",
    "evaluate zero-key Freed ID typewriter envelope",
    "evaluate THOS dual-view proxy nonpromotion",
    "evaluate GMUT mechanism obligation board",
    "evaluate CBR workplace challenge without remedy decision",
    "evaluate three isolated Python tool candidates",
    "evaluate image and reproduction rights abstention",
    "evaluate traditional-knowledge abstention field",
    "evaluate Māori-authority reservation field",
    "evaluate governed human and affected-user reservation",
]

SKILL_TITLES = [
    "ghc-family-typewriter-machine-identity",
    "ghc-family-typewriter-component-topology",
    "ghc-family-typewriter-observation-separation",
    "ghc-family-typewriter-material-vacancy",
    "ghc-family-typewriter-custody-firewall",
    "ghc-family-typewriter-treatment-hold",
    "ghc-family-typewriter-correction-ledger",
    "ghc-family-typewriter-rights-firewall",
    "ghc-family-typewriter-accessible-dossier",
    "ghc-family-typewriter-workload-handover",
]

RUNNER_TITLES = [title.replace("ghc-family-", "ghc_family_").replace("-", "_") for title in SKILL_TITLES]

REFINE_TITLES = [
    "retain exact source and package registry provenance",
    "separate public vocabulary from observation and instruction",
    "separate catalogue identity from real serial numbers",
    "separate component topology from mechanical diagnosis",
    "separate condition cues from treatment decisions",
    "separate settings records from operation instructions",
    "separate custody from ownership and attribution",
    "separate image metadata from reproduction rights",
    "separate document placeholders from private content",
    "separate structural accessibility from completeness",
    "separate scientific analogy from empirical evidence",
    "separate proxy protocols from operational effectiveness",
    "separate tool installation from production fitness",
    "add zero-real-person counters",
    "add zero-real-object document media and adapter counters",
    "add zero-handling operation and treatment counters",
    "add zero-professional-action counters",
    "add exact rollback fields",
    "add smallest-dependency retry fields",
    "add immutable failed witnesses",
    "add bounded passing witnesses",
    "add startup failure overlay",
    "add exact Git-blob manifest review",
    "add five-class privacy scan contract",
    "add bounded changed-Python review",
    "add owner file ceiling check",
    "add clean-state and divergence gates",
    "add single-parent zero-merge gates",
    "add successor duplicate-guard plan",
    "add Stage 20 nonpromotion guard",
]

TOOL_CANDIDATES = [
    {
        "name": "deepdiff",
        "version": "9.1.0",
        "registry": "https://pypi.org/project/deepdiff/9.1.0/",
        "license_metadata": "MIT (registry metadata; not legal review)",
        "requires_python": ">=3.10",
        "wheel": "deepdiff-9.1.0-py3-none-any.whl",
        "wheel_sha256": "80c0460e1993b04f6f0ca79abf25548b129fd218478c4ebb08f80560f5d10610",
        "need": "compare bounded synthetic dossier corrections without mutating the source record",
    },
    {
        "name": "jsonpath-ng",
        "version": "1.8.0",
        "registry": "https://pypi.org/project/jsonpath-ng/1.8.0/",
        "license_metadata": "Apache-2.0 (registry classifiers; not legal review)",
        "requires_python": "project page states CPython 3.10+",
        "wheel": "jsonpath_ng-1.8.0-py3-none-any.whl",
        "wheel_sha256": "b8dde192f8af58d646fc031fac9c99fe4d00326afc4148f1f043c601a8cfe138",
        "need": "query declared synthetic dossier paths and prove missing-field quarantine",
    },
    {
        "name": "jsonpatch",
        "version": "1.33",
        "registry": "https://pypi.org/project/jsonpatch/1.33/",
        "license_metadata": "Modified BSD (registry metadata; not legal review)",
        "requires_python": ">=2.7 excluding Python 3.0 through 3.6",
        "wheel": "jsonpatch-1.33-py2.py3-none-any.whl",
        "wheel_sha256": "0ae28c0cd062bbd8b8ecc26d7d164fbbea9652a1a3693f3b956c1eae5145dade",
        "need": "represent reversible RFC 6902 correction patches over synthetic records",
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


def inherited_title_corpus(repo: Path) -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    """Recover the same 1,500-row corpus Eiren used plus Eiren's 40 rows."""
    audit_path = "docs/eiren-kestrel/v669-v5/x1/semantic-novelty-audit.json"
    audit = git_blob_json(repo, SOURCE_FINAL, audit_path)
    rows: list[dict[str, str]] = []
    sources: list[dict[str, Any]] = []
    for source in audit["source_shards"]:
        raw = git_blob(repo, SOURCE_FINAL, source["path"])
        payload = json.loads(raw.decode("utf-8"))
        rows.extend({"proposal_id": str(row["proposal_id"]), "title": str(row["title"])} for row in payload["rows"])
        sources.append({"path": source["path"], "rows": len(payload["rows"]), "sha256": sha256_bytes(raw)})
    prior = {row["proposal_id"]: row for row in rows}
    if len(prior) != SOURCE_PRIOR_RECOVERED:
        raise ValueError(f"expected {SOURCE_PRIOR_RECOVERED} prior rows, recovered {len(prior)}")
    for index in range(1, 9):
        rel = f"docs/eiren-kestrel/v669-v5/x1/proposal-freeze-shards/proposals-{index:02d}.json"
        raw = git_blob(repo, SOURCE_FINAL, rel)
        payload = json.loads(raw.decode("utf-8"))
        rows.extend({"proposal_id": str(row["proposal_id"]), "title": str(row["title"])} for row in payload["rows"])
        sources.append({"path": rel, "rows": len(payload["rows"]), "sha256": sha256_bytes(raw)})
    deduped = {row["proposal_id"]: row for row in rows}
    if len(deduped) != SOURCE_RECOVERED:
        raise ValueError(f"expected {SOURCE_RECOVERED} accessible rows, recovered {len(deduped)}")
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
                    f"docs/elaren-kestrel/v669-v6/x2/proposals/{proposal_id.lower()}-{slug}.json",
                    f"docs/elaren-kestrel/v669-v6/x2/cards/{proposal_id.lower()}-{slug}.json",
                ],
                "execution_lane": "x2_owner_local_bounded_control" if completion_lane else "held_gap_or_gate",
                "expected_disposition": disposition,
                "falsifier_or_acceptance_gate": (
                    "One bounded synthetic positive contract is accepted, four preregistered invalid mutations are rejected, and all real people, typewriters, documents, objects, media, measurements, handling, operation, treatment, external actions, and authority actions remain zero."
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
