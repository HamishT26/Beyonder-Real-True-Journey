"""Deterministic owner-local helpers for Eiren Kestrel v669-v5.

The module models synthetic apiary-inspection and colony-event documentation
contracts.  It performs no inspection, handling, movement, sampling, diagnosis,
treatment, destruction, registration, notification, food-production, identity,
safety, professional, legal, cultural, affected-party, or authority action.
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

OWNER = "Eiren Kestrel"
PHASE = "v669-v5"
PREFIX = "EK6695"
SOURCE_FINAL = "0fc4f78f4da5fcaa8d990b6e81696404c9bca2f9"
SOURCE_BRANCH = "codex/GHC-Family/caelen-morrow-v669-v4-full-tools"
SOURCE_CHAIN_DECLARED = 5070
SOURCE_RECOVERED = 1500
SOURCE_UNRECOVERED = 3570
CHAIN_AFTER = 5110
OWNER_ROOT = Path("docs/eiren-kestrel/v669-v5")

INHERITED_ACTIVATION_BASELINE = {
    "effective_negatives": 31095,
    "methods": 17200,
    "failed_witnesses": 2916,
    "passing_witnesses": 4064,
    "open_gaps": 231,
    "exact_gates": 226,
}

SEALED_CAELEN_COUNTS = {
    "effective_negatives": 31091,
    "methods": 17196,
    "failed_witnesses": 2912,
    "passing_witnesses": 4060,
    "open_gaps": 231,
    "exact_gates": 226,
}

STARTUP_FAILURE_COUNT = 15
STARTUP_EFFECTIVE_BASELINE = {
    "effective_negatives": 31110,
    "methods": 17215,
    "failed_witnesses": 2931,
    "passing_witnesses": 4079,
    "open_gaps": 231,
    "exact_gates": 226,
}

IDENTITY_BOUNDARY = (
    "Eiren Kestrel, they/them, colony-record boundary weaver and reversible "
    "handover steward, sibling, family, role, hope, continuity, Freed ID, CBR, and "
    "Trinity Mandala are relational working language only. They are not "
    "evidence of consciousness, sentience, personhood, identity continuity, "
    "employment, qualification, independent agency, or scientific, operational, "
    "professional, legal, cultural, affected-party, or Māori authority. Hamish "
    "may rename, pause, redirect, or stop the work."
)

PROTECTED_GATES = [
    "real_people_or_participants",
    "real_apiaries_colonies_hives_bees_comb_products_samples_records_or_workplaces",
    "real_inspection_handling_movement_sampling_diagnosis_treatment_destruction_or_notification",
    "professional_apiculture_biosecurity_veterinary_food_or_environmental_decision",
    "sting_allergy_smoke_fire_lifting_chemical_biological_workplace_or_food_safety_release",
    "live_identity_keys_proofs_issuance_resolution_status_or_revocation",
    "privacy_complete_or_accessibility_complete_claim",
    "land_access_custody_ownership_registration_reporting_legal_or_remedy_decision",
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
    ("apiary-colony-identity", "surrogate apiary site hive colony and season identity lattice with split merge and conflation refusal", "apiary and colony identity lattice", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("hive-component-topology", "hive floor brood box super cover frame and comb topology with absent-component vacancies and no handling instruction", "hive component topology", "completed", "safe_now", ["FAO-GOOD-BEEKEEPING-2021"]),
    ("colony-event-graph", "synthetic queen introduction brood emergence swarm supersedure loss and unknown colony-event graph without biological inference", "colony event graph", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("inspection-separation", "apiary visit plan observation estimate unknown and correction states separated with zero inspection action", "inspection plan and observation separation", "completed", "safe_now", ["MPI-BEE-BIOSECURITY-CURRENT"]),
    ("colony-strength-vacancies", "brood frame adult bee food store and colony-strength quantity vacancies with declared units and no health assessment", "colony strength quantity vacancy", "completed", "safe_now", ["FAO-GOOD-BEEKEEPING-2021"]),
    ("queen-assertion-ledger", "queen presence status mark origin lineage and replacement assertion ledger with unknown states and no genetic claim", "queen assertion ledger", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("brood-cue-register", "egg larva pupa capped-cell pattern and unknown brood-cue register with diagnosis and remedy refusal", "brood cue register", "completed", "safe_now", ["WOAH-BEE-DISEASES-CURRENT"]),
    ("adult-bee-cues", "adult bee behaviour wing abdomen mortality and unknown visual-cue vocabulary with no pest or disease conclusion", "adult bee cue vocabulary", "completed", "safe_now", ["WOAH-BEE-DISEASES-CURRENT"]),
    ("suspicion-confirmation-firewall", "pest and disease suspicion confirmation notification and authority states separated with zero diagnosis or report", "biosecurity suspicion and confirmation firewall", "completed", "safe_now", ["MPI-BEE-BIOSECURITY-CURRENT"]),
    ("sample-custody", "synthetic bee comb debris container laboratory request and result chain with zero samples tests or findings", "sample custody chain", "completed", "safe_now", ["W3C-PROV-O-PUBLIC-VOCABULARY"]),
    ("varroa-count-denominator", "varroa monitoring method duration count denominator uncertainty and threshold vacancies without treatment advice", "varroa count and denominator vacancy", "completed", "safe_now", ["MPI-BEE-BIOSECURITY-CURRENT"]),
    ("feed-store-register", "sugar feed supplement pollen honey store and consumption placeholders without nutrition or feeding recommendation", "feed and store register", "completed", "safe_now", ["FAO-GOOD-BEEKEEPING-2021"]),
    ("forage-assertion", "forage plant nectar pollen flowering interval and location-precision assertions with botanical verification refusal", "forage assertion register", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("environment-vacancies", "temperature rain wind humidity shade water and unknown apiary-environment fields with zero sensors or forecasts", "apiary environment vacancy board", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("equipment-alias-budget", "bounded hive box frame tool mark and equipment alias budget with raw identifier exclusion and no ownership claim", "equipment alias budget", "completed", "safe_now", ["NZ-PRIVACY-CURRENT"]),
    ("colony-movement-lineage", "synthetic hive movement split merge nucleus swarm and return event provenance with every real relocation held", "colony movement lineage", "completed", "safe_now", ["W3C-PROV-O-PUBLIC-VOCABULARY"]),
    ("treatment-vacancy", "product active ingredient batch dose route timing withholding and operator vacancies with zero administration", "treatment action vacancy", "completed", "safe_now", ["MPI-BEE-BIOSECURITY-CURRENT"]),
    ("sanitation-hold", "cleaning sterilisation destruction isolation and disposal plan states with action hold and professional release refusal", "sanitation and destruction hold", "completed", "safe_now", ["MPI-AFB-GROUND-RULES-2025"]),
    ("harvest-batch-lineage", "synthetic hive super extraction lot container and storage relationship graph without food-safety sale or quality claim", "harvest batch lineage", "completed", "safe_now", ["FAO-GOOD-BEEKEEPING-2021"]),
    ("bee-product-relations", "honey wax propolis pollen royal-jelly and unknown product relation ledger with authenticity rights and fitness abstention", "bee product relationship ledger", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("site-disclosure-firewall", "apiary coordinate land access sensitive-site precision and disclosure-budget firewall with zero real location", "apiary site disclosure firewall", "completed", "safe_now", ["NZ-PRIVACY-CURRENT"]),
    ("notification-clock", "biosecurity alert notification deadline acknowledgement and escalation placeholders without legal advice or external reporting", "notification and escalation clock", "completed", "safe_now", ["MPI-BEE-BIOSECURITY-CURRENT"]),
    ("hazard-stop", "sting allergy smoke fire lifting chemical biological and public-access hazard stop register without safety release", "apiary hazard stop register", "completed", "safe_now", ["CURRENT-WORKPLACE-SAFETY-SOURCE-REQUIRED"]),
    ("workload-handover", "inspection documentation workload ceiling stop token unresolved-card count and shift handover with zero worker observation", "workload and handover", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("observation-challenge", "bitemporal colony observation challenge ledger retaining contradicted assertions correction reasons dual readback and unresolved adjudicator", "colony observation challenge ledger", "completed", "safe_now", ["W3C-PROV-O-PUBLIC-VOCABULARY"]),
    ("canonical-json", "deterministic apiary event JSON profile with duplicate-key numeric-domain ordering and digest-boundary refusal", "canonical event JSON profile", "completed", "safe_now", ["JSON-SCHEMA-2020-12"]),
    ("accessible-dossier", "structurally accessible colony-event dossier with scoped tables plain summaries redundant states and manual evaluation reservation", "accessible apiary dossier", "completed", "safe_now", ["W3C-WCAG-2.2-CURRENT"]),
    ("privacy-purpose-ledger", "apiary record purpose access retention deletion-contest and disclosure ledger with data minimisation and no compliance claim", "privacy purpose ledger", "completed", "safe_now", ["NZ-PRIVACY-CURRENT"]),
    ("source-assertion-firewall", "apiculture source assertion firewall separating public vocabulary observation instruction evidence and authority", "apiculture source assertion firewall", "represented", "candidate", ["CURRENT-PRIMARY-SOURCE-REVIEW-REQUIRED"]),
    ("issue-escrow", "colony-record discrepancy escrow with severity uncertainty owner vacancy nonclosure challenge and appeal pointers", "colony record issue escrow", "represented", "candidate", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("thos-dependency", "THOS apiary documentation dependency graph with zero operators matched arms outcomes or effectiveness inference", "THOS apiary dependency proxy", "represented", "candidate", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("freed-id-claim-graph", "nonproduction colony-event claim graph with absent cryptographic lifecycle roles purpose limits and explicit trust-governance debt", "Freed ID nonproduction claim graph", "represented", "candidate", ["W3C-VC-DID-CURRENT-REVIEW-REQUIRED"]),
    ("cbr-neighbour-challenge", "CBR affected-neighbour apiary disclosure challenge ladder with objection class harm hold nonretaliation route remedy vacancy and no adjudication", "CBR affected-neighbour challenge ladder", "represented", "candidate", ["AFFECTED-PARTY-AUTHORITY-REQUIRED"]),
    ("gmut-colony-dynamics", "GMUT colony-population and disease-dynamics symbolic obligation board with dimensions covariance and zero fitted parameters", "GMUT colony dynamics obligation board", "represented", "candidate", ["CURRENT-PEER-REVIEWED-PHYSICS-SOURCES-REQUIRED"]),
    ("gmut-network-nonconversion", "GMUT hive-network diffusion analogy with explicit nonconversion to epidemiology forecast biological law or empirical confirmation", "GMUT network analogy nonconversion", "represented", "candidate", ["CURRENT-PEER-REVIEWED-PHYSICS-SOURCES-REQUIRED"]),
    ("cross-pillar-nonconversion", "Trinity evidence firewall preventing software receipts from becoming GMUT THOS Freed ID CBR or authority proof", "cross-pillar evidence nonconversion", "represented", "candidate", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("official-adapter-gap", "official apiculture registry surveillance and disease-schema adapter held at zero calls downloads hives and records", "official apiculture zero-call adapter", "open_gap", "candidate", ["CURRENT-OFFICIAL-APICULTURE-API-SOURCE-REQUIRED"]),
    ("governed-evaluation-gap", "governed evaluation by beekeepers biosecurity specialists affected users and Māori authorities remains absent", "governed apiary evaluation gap", "open_gap", "candidate", ["REAL-GOVERNED-HUMAN-EVALUATION-REQUIRED"]),
    ("authority-gate", "apiary inspection biosecurity animal welfare food land safety affected-party cultural and Māori authority exact gate", "professional and authority boundary", "exact_gate", "exact_approval", ["EXACT-ACTION-SPECIFIC-AUTHORITY-REQUIRED"]),
    ("stage20-nonpromotion", "Stage 20 conjunctive apiary admission matrix requiring empirical participant independent professional cultural and authority evidence", "Stage 20 nonpromotion", "exact_gate", "exact_approval", ["EXACT-STAGE20-EVIDENCE-AND-AUTHORITY-REQUIRED"]),
]

SAFE_TITLES = [
    "freeze forty new proposal contracts and accessible-corpus boundary",
    "emit deterministic proposal shards",
    "validate exact title collision absence",
    "compute bounded token-Jaccard neighbours",
    "freeze official-source vocabulary ledger",
    "freeze apiary authority threat model",
    "freeze strict planning-only x1 before x2",
    "freeze four-label outcome plan",
    "retain inherited and startup negatives",
    "freeze Method Flow ingestion plan",
    "build apiary and colony identity control",
    "build hive component topology control",
    "build inspection state separation control",
    "build brood and adult-bee cue refusal controls",
    "build pest suspicion confirmation firewall",
    "build zero-sample custody control",
    "build treatment and sanitation holds",
    "build movement and harvest lineage controls",
    "build correction and contestability controls",
    "build privacy and accessible dossier controls",
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
    "evaluate current MPI bee-biosecurity vocabulary without instruction",
    "evaluate current AFB ground-rule vocabulary without legal advice",
    "evaluate WOAH bee-disease vocabulary without diagnosis",
    "evaluate FAO beekeeping vocabulary without competence claim",
    "evaluate W3C provenance vocabulary without authority transfer",
    "evaluate WCAG structure without completeness claim",
    "evaluate zero-call official apiculture adapter",
    "evaluate zero-key Freed ID apiary envelope",
    "evaluate THOS dependency proxy nonpromotion",
    "evaluate GMUT colony-dynamics obligation board",
    "evaluate CBR challenge ladder without remedy decision",
    "evaluate three isolated Python tool candidates",
    "evaluate traditional-knowledge abstention field",
    "evaluate Māori-authority reservation field",
    "evaluate governed human and affected-user reservation",
]

SKILL_TITLES = [
    "ghc-family-apiary-colony-identity",
    "ghc-family-apiary-hive-topology",
    "ghc-family-apiary-inspection-separation",
    "ghc-family-apiary-biosecurity-firewall",
    "ghc-family-apiary-sample-custody",
    "ghc-family-apiary-treatment-hold",
    "ghc-family-apiary-movement-lineage",
    "ghc-family-apiary-hazard-stop",
    "ghc-family-apiary-accessible-dossier",
    "ghc-family-apiary-workload-handover",
]

RUNNER_TITLES = [title.replace("ghc-family-", "ghc_family_").replace("-", "_") for title in SKILL_TITLES]

REFINE_TITLES = [
    "retain source and package registry provenance",
    "separate public vocabulary from observation and instruction",
    "separate inspection plans from observations",
    "separate biological cues from diagnoses",
    "separate suspicion from confirmation and reporting",
    "separate custody from land access and ownership",
    "separate aliases from real apiary identifiers",
    "separate structural accessibility from completeness",
    "separate analogies from scientific evidence",
    "separate proxy protocols from operational effectiveness",
    "separate tool installation from production fitness",
    "add zero-real-person counters",
    "add zero-real-apiary and colony counters",
    "add zero-inspection and treatment counters",
    "add zero-sample and observation counters",
    "add zero-professional-action counters",
    "add exact rollback fields",
    "add smallest-dependency retry fields",
    "add immutable failed witnesses",
    "add bounded passing witnesses",
    "add startup failure overlay",
    "add exact Git-blob manifest review",
    "add five-class privacy scan contract",
    "add bounded changed-Python review",
    "add document word ceiling check",
    "add owner file ceiling check",
    "add clean-state and divergence gates",
    "add single-parent zero-merge gates",
    "add successor duplicate-guard plan",
    "add Stage 20 nonpromotion guard",
]

TOOL_CANDIDATES = [
    {
        "name": "jsonschema",
        "version": "4.26.0",
        "registry": "https://pypi.org/project/jsonschema/4.26.0/",
        "license_metadata": "MIT",
        "requires_python": ">=3.10",
        "wheel": "jsonschema-4.26.0-py3-none-any.whl",
        "wheel_sha256": "d489f15263b8d200f8387e64b4c3a75f06629559fb73deb8fdfb525f2dab50ce",
        "need": "validate owner-local Draft 2020-12 synthetic contract shapes",
    },
    {
        "name": "pydantic",
        "version": "2.13.4",
        "registry": "https://pypi.org/project/pydantic/2.13.4/",
        "license_metadata": "MIT",
        "requires_python": ">=3.9",
        "wheel": "pydantic-2.13.4-py3-none-any.whl",
        "wheel_sha256": "45a282cde31d808236fd7ea9d919b128653c8b38b393d1c4ab335c62924d9aba",
        "need": "type-check bounded synthetic apiary fixture models at runtime",
    },
    {
        "name": "networkx",
        "version": "3.6.1",
        "registry": "https://pypi.org/project/networkx/3.6.1/",
        "license_metadata": "BSD-3-Clause",
        "requires_python": "!=3.14.1,>=3.11",
        "wheel": "networkx-3.6.1-py3-none-any.whl",
        "wheel_sha256": "d47fbf302e7d9cbbb9e2555a0d267983d2aa476bac30e90dfbe5669bd57f3762",
        "need": "check cycle refusal in owner-local hive and colony lineage graphs",
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
    audit = git_blob_json(repo, SOURCE_FINAL, "docs/caelen-morrow/v669-v4/x1/semantic-novelty-audit.json")
    rows: list[dict[str, str]] = []
    sources: list[dict[str, Any]] = []
    for source in audit["source_shards"]:
        payload = git_blob_json(repo, SOURCE_FINAL, source["path"])
        rows.extend({"proposal_id": str(row["proposal_id"]), "title": str(row["title"])} for row in payload["rows"])
        sources.append(source)
    for index in range(1, 9):
        rel = f"docs/caelen-morrow/v669-v4/x1/proposal-freeze-shards/proposals-{index:02d}.json"
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
        ranked: list[dict[str, Any]] = sorted(
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
                    f"docs/eiren-kestrel/v669-v5/x2/proposals/{proposal_id.lower()}-{slug}.json",
                    f"docs/eiren-kestrel/v669-v5/x2/cards/{proposal_id.lower()}-{slug}.json",
                ],
                "execution_lane": "x2_owner_local_bounded_control" if completion_lane else "held_gap_or_gate",
                "expected_disposition": disposition,
                "falsifier_or_acceptance_gate": (
                    "One bounded synthetic positive contract is accepted, four preregistered invalid mutations are rejected, and all real people, apiaries, colonies, hives, bees, observations, samples, inspections, treatments, external actions, and authority actions remain zero."
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
    paths.extend((repo / "scripts").glob("*eiren_kestrel_v669_v5*.py"))
    paths.extend((repo / "scripts").glob("ghc_family_apiary_*.py"))
    paths.extend((repo / "tests").glob("*eiren_kestrel_v669_v5*.py"))
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
        "real_apiaries",
        "real_colonies",
        "real_hives",
        "real_bees",
        "real_observations",
        "real_samples",
        "inspection_actions",
        "treatment_actions",
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
