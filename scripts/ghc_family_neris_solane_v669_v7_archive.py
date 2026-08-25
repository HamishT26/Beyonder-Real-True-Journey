"""Deterministic owner-local helpers for Neris Solane v669-v7.

The module models planning contracts for wholly synthetic historical slide-rule
cataloguing, scale-state, computation-trace, correction, and handover
documentation. It does not inspect, handle, operate, calculate with, clean,
repair, value, acquire, dispose of, publish, identify, or authenticate any real
slide rule, manual, record, person, collection, site, material, measurement, or
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
PHASE = "v669-v7"
PREFIX = "NS6697"
SOURCE_FINAL = "ca3ab84977c44bf1c7934ed10e99e4fb341a5952"
SOURCE_X1 = "07f934986ddad144e615e7b31276716b646ebba5"
SOURCE_EVIDENCE = "f701d489e7c6a021b0390699e9ceeac5cd00255e"
SOURCE_BRANCH = "codex/GHC-Family/elaren-kestrel-v669-v6-full-tools"
SOURCE_CHAIN_DECLARED = 5150
SOURCE_PRIOR_RECOVERED = 1540
SOURCE_OWNER_ROWS = 40
SOURCE_RECOVERED = SOURCE_PRIOR_RECOVERED + SOURCE_OWNER_ROWS
SOURCE_UNRECOVERED = 3570
CHAIN_AFTER = 5190
OWNER_ROOT = Path("docs/neris-solane/v669-v7")

INHERITED_ACTIVATION_BASELINE = {
    "effective_negatives": 31483,
    "methods": 17588,
    "failed_witnesses": 3304,
    "passing_witnesses": 4524,
    "open_gaps": 235,
    "exact_gates": 230,
}

STARTUP_FAILURE_COUNT = 23
STARTUP_EFFECTIVE_BASELINE = {
    "effective_negatives": 31506,
    "methods": 17611,
    "failed_witnesses": 3327,
    "passing_witnesses": 4547,
    "open_gaps": 235,
    "exact_gates": 230,
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
    "real_slide_rules_manuals_collections_sites_images_measurements_or_records",
    "real_handling_operation_calculation_cleaning_repair_or_treatment",
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
    ("instrument-identity", "surrogate historical slide rule accession instrument maker model form and serial-assertion identity lattice with conflation refusal", "slide rule identity lattice", "completed", "safe_now", ["SMITHSONIAN-SLIDE-RULE-RESOURCES"]),
    ("form-family-taxonomy", "linear circular cylindrical spiral and special-purpose slide rule form-family register with completeness abstention", "slide rule form-family taxonomy", "completed", "safe_now", ["SMITHSONIAN-SLIDE-RULE-RESOURCES"]),
    ("body-slide-cursor-topology", "slide rule stock slide groove cursor frame hairline end-brace and scale-face topology with missing-part vacancies", "slide rule component topology", "completed", "safe_now", ["SMITHSONIAN-SLIDE-RULE-OBJECT"]),
    ("scale-code-register", "A B C D CI DI K L S T and unknown slide rule scale-code register separating literal inscription function hypothesis and authority", "scale-code assertion register", "completed", "safe_now", ["SMITHSONIAN-SLIDE-RULE-RESOURCES"]),
    ("index-alignment-vacancy", "left right and folded index alignment vacancy ledger with zero inspection adjustment calibration or accuracy claim", "index alignment vacancy", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("scale-domain-direction", "increasing decreasing reciprocal logarithmic trigonometric and unknown scale-domain direction register without operational inference", "scale domain and direction register", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("logarithmic-spacing-representation", "synthetic logarithmic spacing coordinate representation with declared base domain transform and zero physical measurement", "logarithmic spacing representation", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA", "PYPI-PINT"]),
    ("cursor-parallax-vacancy", "cursor hairline width offset parallax readability and alignment vacancies without observation measurement calibration or repair", "cursor and parallax vacancy register", "completed", "safe_now", ["SMITHSONIAN-SLIDE-RULE-OBJECT"]),
    ("decimal-placement-abstention", "synthetic mantissa trace separating scale reading decimal placement order-of-magnitude estimate and correctness abstention", "decimal placement abstention trace", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("significant-figure-boundary", "slide rule significant-figure interval rounding uncertainty and precision boundary with no real result or accuracy certification", "significant-figure boundary", "completed", "safe_now", ["PYPI-UNCERTAINTIES", "PYPI-PORTION"]),
    ("multiplication-trace", "synthetic C and D scale multiplication alignment readback trace with fixed fixture values and no instruction or competence claim", "multiplication trace fixture", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("division-trace", "surrogate quotient audit using numerator denominator and reversed C-to-D relations with instruction and competence held", "division trace fixture", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("root-scale-trace", "synthetic A B C D and K square cube and root relation trace with domain holds and zero empirical measurement", "root-scale relation trace", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("reciprocal-scale-trace", "synthetic CI and DI reciprocal relation trace with nonzero-domain gate and no operational instruction", "reciprocal scale trace", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("trigonometric-scale-vacancy", "S T ST and unknown angular-scale designation vacancy with unit-domain guard and zero surveying navigation or engineering use", "trigonometric scale vacancy", "completed", "safe_now", ["NIST-SI-UNITS", "PYPI-PINT"]),
    ("log-log-scale-vacancy", "LL scale family base range sign direction and exponential-relation vacancies without model identification or real calculation", "log-log scale vacancy", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("gauge-mark-legend", "gauge mark constant reference symbol and special-purpose legend separating inscription hypothesis source and verified function", "gauge mark legend", "completed", "safe_now", ["SMITHSONIAN-SLIDE-RULE-RESOURCES"]),
    ("mixed-material-vacancy", "slide rule wood bamboo plastic aluminium paper glass ink paint and unknown composite material vacancy ledger without identification", "mixed-material vacancy ledger", "completed", "safe_now", ["CCI-INDUSTRIAL-COLLECTIONS"]),
    ("surface-engraving-condition", "engraved printed laminated inked anodized painted and cursor-surface condition vocabulary with treatment abstention", "surface and engraving condition vocabulary", "completed", "safe_now", ["CCI-INDUSTRIAL-COLLECTIONS"]),
    ("observation-treatment-separation", "condition-to-action firewall for surrogate scale faces keeping observation referral authorization treatment and outcome disjoint", "observation and treatment separation", "completed", "safe_now", ["CCI-INDUSTRIAL-COLLECTIONS"]),
    ("treatment-hold", "cleaning lubrication cursor adjustment scale realignment refinishing and parts replacement docket with every physical action held", "treatment and maintenance hold", "completed", "safe_now", ["CCI-HANDLING-HERITAGE-OBJECTS"]),
    ("manual-content-rights-firewall", "slide rule manual table example annotation scan transcription and reuse ledger excluding real content identities and rights conclusions", "manual content and rights firewall", "completed", "safe_now", ["SMITHSONIAN-TERMS-AND-METADATA", "NZ-PRIVACY-PRINCIPLES"]),
    ("custody-attribution-abstention", "provenance braid for surrogate instrument associations quarantining maker retail stewardship possession title and ownership conclusions", "custody and attribution abstention", "completed", "safe_now", ["W3C-PROV-O"]),
    ("correction-challenge-ledger", "append-only dispute braid for surrogate scale records linking prior assertion counterclaim supersession dual readback and adjudicator vacancy", "correction and challenge ledger", "completed", "safe_now", ["W3C-PROV-O"]),
    ("workload-handover", "bounded solo documentation envelope with card budget fatigue stop unresolved count correction readback and explicit handover", "workload and handover control", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("canonical-json", "canonical byte profile for surrogate scale dossiers rejecting duplicates nonfinite numeric domains unsorted fields normalization drift and digest promotion", "canonical dossier JSON profile", "completed", "safe_now", ["JSON-SCHEMA-2020-12", "RFC-8785"]),
    ("accessible-dossier", "slide rule form-to-scale textual traversal companion with ordered landmarks expanded abbreviations printable errors and evaluation vacancies", "accessible slide rule traversal companion", "completed", "safe_now", ["W3C-WCAG-2.2"]),
    ("privacy-purpose-ledger", "purpose-limitation matrix for surrogate instrument records covering access retention contest disclosure and minimisation without compliance inference", "privacy purpose ledger", "completed", "safe_now", ["NZ-PRIVACY-PRINCIPLES"]),
    ("source-assertion-firewall", "slide rule source firewall separating public museum vocabulary inscription observation inference instruction evidence and authority", "slide rule source assertion firewall", "represented", "candidate", ["CURRENT-PRIMARY-SOURCE-REVIEW"]),
    ("issue-escrow", "scale-code inscription conflict braid joining literal readings catalogue assertions source dates correction custody and unresolved function", "slide rule inscription conflict braid", "represented", "candidate", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("thos-dual-view-proxy", "THOS paired-representation ablation for surrogate scale dossiers using matched budgets and no participants outcomes or effectiveness inference", "THOS slide rule documentation proxy", "represented", "candidate", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("freed-id-claim-graph", "Freed ID claim envelope for surrogate instrument provenance holding every cryptographic lifecycle and trust operation at zero", "Freed ID nonproduction claim graph", "represented", "candidate", ["W3C-VC-DATA-INTEGRITY-1.0"]),
    ("cbr-learning-workplace-challenge", "CBR challenge protocol for synthetic learning records with nonretaliation harm pause response clock remedy vacancy and no adjudication", "CBR learning and workplace challenge ladder", "represented", "candidate", ["AFFECTED-PARTY-AUTHORITY-REQUIRED"]),
    ("gmut-logarithmic-obligations", "GMUT logarithmic-map analogy obligation board with typed domain dimensions covariance boundary conditions and zero fitted parameters", "GMUT logarithmic mapping analogy board", "represented", "candidate", ["CURRENT-PEER-REVIEWED-PHYSICS-SOURCES"]),
    ("gmut-dimensional-nonconversion", "GMUT scale and dimensional-analysis analogy with explicit nonconversion to force law prediction measurement or confirmation", "GMUT dimensional analogy nonconversion", "represented", "candidate", ["CURRENT-PEER-REVIEWED-PHYSICS-SOURCES"]),
    ("cross-pillar-nonconversion", "nontransfer accounting matrix assigning surrogate slide-rule software receipts zero balance in GMUT THOS Freed ID and CBR authority accounts", "cross-pillar evidence-account routing", "represented", "candidate", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("official-adapter-gap", "official museum slide rule vocabulary adapter held at zero calls downloads objects images records or manifests", "official collection zero-call adapter", "open_gap", "candidate", ["CURRENT-OFFICIAL-COLLECTION-API-SOURCE"]),
    ("governed-evaluation-gap", "missing governed review register spanning metrology museum documentation conservation accessibility affected parties and Māori authority", "governed slide rule evaluation gap", "open_gap", "candidate", ["REAL-GOVERNED-HUMAN-EVALUATION"]),
    ("authority-gate", "exact action lock over slide-rule metrology conservation custody rights workplace culture affected parties and Māori authority", "professional rights and authority boundary", "exact_gate", "exact_approval", ["EXACT-ACTION-SPECIFIC-AUTHORITY"]),
    ("stage20-nonpromotion", "terminal four-receipt hold requiring instrument evidence independent reproduction governed rights and competent authority before any Stage 20 state", "Stage 20 four-key terminal interlock", "exact_gate", "exact_approval", ["EXACT-STAGE20-EVIDENCE-AND-AUTHORITY"]),
]

SAFE_TITLES = [
    "freeze forty new proposal contracts and accessible-corpus boundary",
    "emit deterministic proposal shards",
    "validate exact title collision absence",
    "compute bounded token-Jaccard neighbours",
    "freeze official-source vocabulary ledger",
    "freeze slide rule authority threat model",
    "freeze strict planning-only x1 before x2",
    "freeze four-label outcome plan",
    "retain inherited and startup negatives",
    "freeze Method Flow ingestion plan",
    "build surrogate instrument identity control",
    "build slide rule form and component topology controls",
    "build scale-code assertion register",
    "build index alignment and direction vacancy controls",
    "build logarithmic spacing representation control",
    "build decimal-placement and significant-figure holds",
    "build fixed synthetic computation-trace controls",
    "build observation and treatment separation",
    "build manual content and rights firewall",
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
    "evaluate current Smithsonian slide rule vocabulary without collection claim",
    "evaluate CCI industrial-object vocabulary without treatment advice",
    "evaluate NIST unit vocabulary without measurement authority",
    "evaluate W3C provenance vocabulary without authority transfer",
    "evaluate WCAG structure without completeness claim",
    "evaluate zero-call official collection adapter",
    "evaluate zero-key Freed ID slide rule envelope",
    "evaluate THOS dual-view proxy nonpromotion",
    "evaluate GMUT logarithmic-map obligation board",
    "evaluate CBR learning and workplace challenge without remedy decision",
    "evaluate three isolated Python tool candidates",
    "evaluate manual and reproduction rights abstention",
    "evaluate traditional-knowledge abstention field",
    "evaluate Māori-authority reservation field",
    "evaluate governed human and affected-user reservation",
]

SKILL_TITLES = [
    "ghc-family-slide-rule-instrument-identity",
    "ghc-family-slide-rule-form-topology",
    "ghc-family-slide-rule-scale-code-register",
    "ghc-family-slide-rule-index-alignment",
    "ghc-family-slide-rule-domain-direction",
    "ghc-family-slide-rule-logarithmic-spacing",
    "ghc-family-slide-rule-cursor-parallax-vacancy",
    "ghc-family-slide-rule-decimal-placement-abstention",
    "ghc-family-slide-rule-significant-figure-boundary",
    "ghc-family-slide-rule-computation-trace-firewall",
]

RUNNER_TITLES = [title.replace("ghc-family-", "ghc_family_").replace("-", "_") for title in SKILL_TITLES]

REFINE_TITLES = [
    "retain exact source and package registry provenance",
    "separate public vocabulary from observation and instruction",
    "separate catalogue identity from real serial numbers and ownership",
    "separate form topology from metrological function claims",
    "separate scale codes from verified function",
    "separate logarithmic coordinates from physical measurement",
    "separate synthetic arithmetic traces from instruction and competence",
    "separate decimal placement and significant figures from certified correctness and accuracy",
    "separate condition cues from treatment decisions",
    "separate custody from ownership and attribution",
    "separate manual metadata from reproduction rights",
    "separate calculation placeholders from private content",
    "separate structural accessibility from completeness",
    "separate scientific analogy from empirical evidence",
    "separate proxy protocols from operational effectiveness",
    "separate tool installation from production fitness",
    "add zero-real-person instrument manual media and adapter counters",
    "add zero-handling operation calculation and treatment counters",
    "add zero-professional-action counters",
    "add exact rollback fields",
    "add smallest-dependency retry fields",
    "add immutable failed witnesses",
    "add bounded passing witnesses",
    "add startup failure overlay",
    "add exact Git-blob manifest review",
    "add five-class privacy scan contract",
    "add bounded changed-Python review",
    "add owner materialized-file ceiling check",
    "add successor duplicate-guard plan",
    "add Stage 20 nonpromotion guard",
]

TOOL_CANDIDATES = [
    {
        "name": "pint",
        "version": "0.25.3",
        "registry": "https://pypi.org/project/Pint/0.25.3/",
        "license_metadata": "BSD (registry metadata; not legal review)",
        "requires_python": ">=3.11",
        "wheel": "pint-0.25.3-py3-none-any.whl",
        "wheel_sha256": "27eb25143bd5de9fcc4d5a4b484f16faf6b4615aa93ece6b3373a8c1a3c1b97d",
        "need": "reject unit-domain mismatches in bounded synthetic scale records",
    },
    {
        "name": "portion",
        "version": "2.6.2",
        "registry": "https://pypi.org/project/portion/2.6.2/",
        "license_metadata": "LGPL-3.0-or-later (registry metadata; not legal review)",
        "requires_python": ">=3.10",
        "wheel": "portion-2.6.2-py3-none-any.whl",
        "wheel_sha256": "86be115afafa776174dc5eac82afb6496c9fa3684f5b3a844c3139535c51085e",
        "need": "model bounded open and closed synthetic scale intervals and reject out-of-domain values",
    },
    {
        "name": "uncertainties",
        "version": "3.2.3",
        "registry": "https://pypi.org/project/uncertainties/3.2.3/",
        "license_metadata": "Revised BSD (registry metadata; not legal review)",
        "requires_python": ">=3.8",
        "wheel": "uncertainties-3.2.3-py3-none-any.whl",
        "wheel_sha256": "313353900d8f88b283c9bad81e7d2b2d3d4bcc330cbace35403faaed7e78890a",
        "need": "represent bounded synthetic nominal values and uncertainty without claiming real measurements",
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
    """Recover Elaren's 1,540-row accessible corpus plus Elaren's 40 rows."""
    audit_path = "docs/elaren-kestrel/v669-v6/x1/semantic-novelty-audit.json"
    audit = git_blob_json(repo, SOURCE_FINAL, audit_path)
    rows: list[dict[str, str]] = []
    sources: list[dict[str, Any]] = []
    shard_paths = [str(source["path"]) for source in audit["source_shards"]]
    shard_paths.extend(
        f"docs/elaren-kestrel/v669-v6/x1/proposal-freeze-shards/proposals-{index:02d}.json"
        for index in range(1, 9)
    )
    blobs = git_batch_blobs(repo, {path: f"{SOURCE_FINAL}:{path}" for path in shard_paths})
    for source in audit["source_shards"]:
        raw = blobs[str(source["path"])]
        payload = json.loads(raw.decode("utf-8"))
        rows.extend({"proposal_id": str(row["proposal_id"]), "title": str(row["title"])} for row in payload["rows"])
        sources.append({"path": source["path"], "rows": len(payload["rows"]), "sha256": sha256_bytes(raw)})
    prior = {row["proposal_id"]: row for row in rows}
    if len(prior) != SOURCE_PRIOR_RECOVERED:
        raise ValueError(f"expected {SOURCE_PRIOR_RECOVERED} prior rows, recovered {len(prior)}")
    for index in range(1, 9):
        rel = f"docs/elaren-kestrel/v669-v6/x1/proposal-freeze-shards/proposals-{index:02d}.json"
        raw = blobs[rel]
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
                    f"docs/neris-solane/v669-v7/x2/proposals/{proposal_id.lower()}-{slug}.json",
                    f"docs/neris-solane/v669-v7/x2/cards/{proposal_id.lower()}-{slug}.json",
                ],
                "execution_lane": "x2_owner_local_bounded_control" if completion_lane else "held_gap_or_gate",
                "expected_disposition": disposition,
                "falsifier_or_acceptance_gate": (
                    "One bounded synthetic positive contract is accepted, four preregistered invalid mutations are rejected, and all real people, slide rules, manuals, records, media, measurements, handling, operation, calculation, treatment, external actions, and authority actions remain zero."
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
