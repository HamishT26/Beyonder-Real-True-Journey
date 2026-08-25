"""Shared constants and deterministic helpers for Sylven Arc v669-v3.

This module is owner-local phase tooling.  It models only synthetic documentation
contracts and never performs a network call or a real ceramics, identity, safety,
professional, legal, cultural, or authority action.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable


OWNER = "Sylven Arc"
PHASE = "v669-v3"
PREFIX = "SA6693"
SOURCE_FINAL = "9c5b88ccde33130663859a3ffcb97188fa63efd7"
SOURCE_BRANCH = "codex/GHC-Family/elowen-cairn-v669-v2-full-tools"
SOURCE_CHAIN_DECLARED = 4990
SOURCE_RECOVERED = 1380
SOURCE_UNRECOVERED = 3570
ACCESSIBLE_WITH_ELOWEN = 1420
CHAIN_AFTER = 5030
OWNER_ROOT = Path("docs/sylven-arc/v669-v3")

INHERITED_BASELINES = {
    "effective_negatives": 30727,
    "methods": 16832,
    "failed_witnesses": 2548,
    "passing_witnesses": 3624,
    "open_gaps": 227,
    "exact_gates": 222,
}

SEALED_ELOWEN_COUNTS = {
    "effective_negatives": 30720,
    "methods": 16826,
    "failed_witnesses": 2541,
    "passing_witnesses": 3618,
    "open_gaps": 227,
    "exact_gates": 222,
}

PROTECTED_GATES = [
    "real_people_or_participants",
    "real_ceramics_kilns_materials_tools_or_workplaces",
    "real_measurements_observations_firings_or_safety_actions",
    "professional_ceramics_conservation_or_engineering_decision",
    "workplace_environmental_product_or_fire_safety_release",
    "live_identity_keys_proofs_or_lifecycle",
    "privacy_complete_or_accessibility_complete_claim",
    "ownership_custody_authorship_legal_or_remedy_decision",
    "cultural_interpretation_traditional_knowledge_or_affected_party_legitimacy",
    "Maori_wording_concepts_data_governance_or_authority",
    "empirical_GMUT_final_physics_or_Theory_of_Everything_claim",
    "THOS_operational_effectiveness_AGI_or_ASI_claim",
    "consciousness_personhood_or_identity_continuity_claim",
    "independent_reproduction_production_deployment_or_Stage_20_claim",
]

ROLLBACK = (
    "Retain the failed fixture at zero credit; stop the smallest owner-local "
    "control; preserve immutable history, negatives, gaps, and gates; remove "
    "only generated owner-local artifacts if required; rerun only the failed "
    "dependency before any broader validation."
)

# (slug, title, subject, expected disposition, approval class, source needs)
PROPOSAL_SPECS = [
    ("batch-identity", "synthetic studio-ceramics batch object sample vessel and fragment identity lattice with conflation refusal", "batch and object identity", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("vessel-topology", "ceramic vessel rim neck shoulder body foot handle lid and attachment topology with absent-part vacancies", "vessel topology", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("clay-body-vacancy", "clay-body composition plasticity shrinkage and provenance claim vacancy without material inference", "clay-body claim vacancy", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("forming-state", "forming-method state register separating declared handbuilding wheel casting and unknown states from practice claims", "forming-method state", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("greenware-state", "greenware wet leather-hard bone-dry and unknown state vocabulary with no handling prescription", "greenware state vocabulary", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("kiln-load-topology", "kiln-load shelf level zone position adjacency and clearance topology with zero physical loading action", "kiln-load topology", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("kiln-furniture-vacancy", "kiln shelf post setter and support identity vacancies with no equipment fitness claim", "kiln-furniture identity", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("schedule-separation", "firing schedule setpoint observation estimate and missing-value separation with no operational instruction", "schedule versus observation separation", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("ramp-hold-graph", "ramp hold cool segment dependency graph with typed duration and temperature vacancies", "ramp-hold event graph", "completed", "safe_now", ["NIST-SI-CURRENT-PRIMARY-SOURCE-NEEDED"]),
    ("atmosphere-vacancy", "oxidation reduction neutral and unknown kiln-atmosphere claim vacancy without combustion inference", "kiln-atmosphere claim vacancy", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("cone-witness-vacancy", "pyrometric-cone identifier placement observation and interpretation vacancies without heatwork conclusion", "cone-witness record vacancy", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("thermocouple-provenance", "thermocouple channel location calibration and reading provenance lattice with no sensor-validity claim", "thermocouple provenance", "completed", "safe_now", ["NIST-TEMPERATURE-CURRENT-PRIMARY-SOURCE-NEEDED"]),
    ("energy-fuel-vacancy", "electric gas wood and unknown firing-energy source vacancy without efficiency or emissions inference", "energy and fuel claim vacancy", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("glaze-material-firewall", "glaze and colorant ingredient assertion firewall with unknown composition and hazard holds", "glaze material assertion firewall", "completed", "safe_now", ["NIOSH-SILICA-CURRENT-PRIMARY-SOURCE-NEEDED"]),
    ("recipe-hash-domain", "synthetic glaze-recipe canonical hash domain separating aliases versions units and withheld values", "glaze recipe hash domain", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("surface-layer-graph", "slip engobe underglaze glaze oxide and unknown surface-layer graph with treatment abstention", "surface-layer graph", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("test-tile-linkage", "test-tile batch recipe firing and observation linkage contract with zero transfer to production ware", "test-tile linkage", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("defect-cue-nondiagnosis", "blister pinhole crawling shivering crazing and unknown cue vocabulary with diagnostic refusal", "surface cue non-diagnosis", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("shape-cue-vocabulary", "crack warp slump dunting and unknown shape-cue register with no cause or remedy inference", "shape cue vocabulary", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("dimension-mass-units", "dimension wall-thickness mass and capacity record with typed SI units uncertainty and vacancies", "dimension and mass unit profile", "completed", "safe_now", ["NIST-SI-CURRENT-PRIMARY-SOURCE-NEEDED"]),
    ("tool-identity-vacancy", "wheel kiln mixer extruder slab-roller and hand-tool identity vacancies with no fitness claim", "studio-tool identity vacancy", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("action-hold-state", "inspect document quarantine release and refuse action-state machine with every real action held", "action-hold state machine", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("correction-docket", "append-only ceramics record correction docket with supersession fork readback and rollback", "correction docket", "completed", "safe_now", ["W3C-PROV-CURRENT-PRIMARY-SOURCE-NEEDED"]),
    ("custody-location", "synthetic object batch shelf box and location custody graph with ownership and title refusal", "custody-location graph", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("workload-handover", "studio-documentation workload limit stop-state recovery note and shift-handover contract", "workload and handover", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("hazard-stop", "dust heat fumes sharp-edge lifting electrical and fire hazard stop register without safety release", "hazard-stop register", "completed", "safe_now", ["NIOSH-SILICA-CURRENT-PRIMARY-SOURCE-NEEDED"]),
    ("accessible-table", "structurally accessible ceramics dossier table with headers plain-language summaries and manual review reservation", "accessible dossier structure", "completed", "safe_now", ["W3C-WCAG-CURRENT-PRIMARY-SOURCE-NEEDED"]),
    ("alias-budget", "bounded object batch recipe and tool pseudonym alias budget with raw-identifier exclusion", "pseudonym alias budget", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("source-firewall", "ceramics source assertion firewall separating citation vocabulary from observation evidence and authority", "source assertion firewall", "represented", "candidate", ["CURRENT-PRIMARY-SOURCE-REVIEW-REQUIRED"]),
    ("issue-escrow", "ceramics discrepancy issue escrow with severity uncertainty owner vacancy and nonclosure rule", "issue escrow", "represented", "candidate", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("thos-dependency", "THOS ceramics documentation dependency DAG with zero-participant proxy and no effectiveness inference", "THOS dependency proxy", "represented", "candidate", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("freed-id-envelope", "Freed ID zero-key ceramics batch envelope with issuer holder proof and lifecycle vacancies", "Freed ID zero-key envelope", "represented", "candidate", ["W3C-DID-CURRENT-PRIMARY-SOURCE-NEEDED"]),
    ("cbr-challenge", "CBR ceramics challenge correction access remedy and appeal ladder with decision authority vacant", "CBR challenge ladder", "represented", "candidate", ["AFFECTED-PARTY-AUTHORITY-REQUIRED"]),
    ("gmut-heat-board", "GMUT kiln heat-flow boundary source sink unit and falsification obligation board with zero fitted coefficients", "GMUT heat-flow obligation board", "represented", "candidate", ["CURRENT-PEER-REVIEWED-PHYSICS-SOURCES-REQUIRED"]),
    ("gmut-phase-nonconversion", "GMUT ceramic phase-change analogy register with explicit nonconversion to material law or empirical confirmation", "GMUT phase-change nonconversion", "represented", "candidate", ["CURRENT-PEER-REVIEWED-MATERIAL-SOURCES-REQUIRED"]),
    ("cross-pillar-nonconversion", "cross-pillar ceramics analogy firewall preventing GMUT THOS Freed ID and CBR evidence conversion", "cross-pillar nonconversion", "represented", "candidate", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("museum-zero-call", "official museum ceramics collection adapter contract held at zero calls zero downloads and zero rows", "official collection zero-call adapter", "open_gap", "candidate", ["CURRENT-OFFICIAL-MUSEUM-API-SOURCE-REQUIRED"]),
    ("human-evaluation-gap", "ceramics dossier manual browser assistive-technology cognitive and affected-user evaluation gap", "human evaluation gap", "open_gap", "candidate", ["REAL-GOVERNED-HUMAN-EVALUATION-REQUIRED"]),
    ("ceramics-authority-gate", "ceramics craft conservation safety ownership cultural affected-party and Maori authority exact gate", "ceramics authority boundary", "exact_gate", "exact_approval", ["EXACT-ACTION-SPECIFIC-AUTHORITY-REQUIRED"]),
    ("stage20-nonpromotion", "terminal nonpromotion contract preserving NOT_READY_FOR_STAGE_20 across all synthetic ceramics evidence", "Stage 20 nonpromotion", "exact_gate", "exact_approval", ["EXACT-STAGE20-EVIDENCE-AND-AUTHORITY-REQUIRED"]),
]

SAFE_TITLES = [
    "freeze proposal contracts and accessible corpus boundary",
    "emit deterministic proposal shards",
    "validate exact title collision absence",
    "compute bounded token-Jaccard neighbors",
    "freeze source-status ledger",
    "freeze owner-local threat model",
    "freeze strict x1-before-x2 lifecycle",
    "freeze four-label outcome plan",
    "freeze retained-negative inheritance",
    "freeze Method Flow ingestion plan",
    "build synthetic batch identity control",
    "build synthetic vessel topology control",
    "build synthetic kiln-load topology control",
    "build schedule-observation separation control",
    "build glaze assertion firewall control",
    "build correction docket control",
    "build custody-location control",
    "build workload handover control",
    "build hazard-stop control",
    "build accessibility structure control",
    "build flashcard tier projection",
    "execute positive fixture controls",
    "execute preregistered rejecting mutations",
    "retain failures at zero completion credit",
    "smoke-use phase-local skills",
    "smoke-use family-current runners",
    "emit exact owner and delta manifests",
    "scan five privacy and raw-identifier classes",
    "emit three-page-equivalent integrated overview",
    "preserve terminal NOT_READY_FOR_STAGE_20 verdict",
]

CANDIDATE_TITLES = [
    "evaluate current primary-source vocabulary without importing authority",
    "evaluate zero-call museum adapter schema",
    "evaluate typed SI unit boundary",
    "evaluate W3C provenance vocabulary boundary",
    "evaluate WCAG structural projection without completeness claim",
    "evaluate zero-key Freed ID envelope",
    "evaluate THOS dependency proxy nonpromotion",
    "evaluate GMUT heat-flow obligation board",
    "evaluate GMUT phase-change analogy nonconversion",
    "evaluate CBR challenge ladder without remedy decision",
    "evaluate traditional-knowledge abstention field",
    "evaluate Maori-authority reservation field",
    "evaluate affected-user evaluation reservation",
    "evaluate professional decision refusal",
    "evaluate dependency-corrected validation recovery",
]

SKILL_TITLES = [
    "ghc-family-ceramics-batch-identity",
    "ghc-family-ceramics-vessel-topology",
    "ghc-family-ceramics-kiln-load-topology",
    "ghc-family-ceramics-schedule-separation",
    "ghc-family-ceramics-glaze-assertion-firewall",
    "ghc-family-ceramics-correction-docket",
    "ghc-family-ceramics-custody-location",
    "ghc-family-ceramics-hazard-stop",
    "ghc-family-ceramics-accessible-dossier",
    "ghc-family-ceramics-workload-handover",
]

RUNNER_TITLES = [
    "ghc_family_ceramics_batch_identity",
    "ghc_family_ceramics_vessel_topology",
    "ghc_family_ceramics_kiln_load_topology",
    "ghc_family_ceramics_schedule_separation",
    "ghc_family_ceramics_glaze_assertion_firewall",
    "ghc_family_ceramics_correction_docket",
    "ghc_family_ceramics_custody_location",
    "ghc_family_ceramics_hazard_stop",
    "ghc_family_ceramics_accessible_dossier",
    "ghc_family_ceramics_workload_handover",
]

REFINE_TITLES = [
    "normalize family-current runner names",
    "retain owner and version provenance",
    "separate source vocabulary from evidence",
    "separate setpoints from observations",
    "separate cues from diagnoses",
    "separate custody from ownership",
    "separate identity aliases from real identifiers",
    "separate structural accessibility from completeness",
    "separate analogies from scientific evidence",
    "separate proxy protocols from operational effectiveness",
    "add explicit zero-network-call counters",
    "add explicit zero-real-person counters",
    "add explicit zero-real-object counters",
    "add explicit zero-measurement counters",
    "add explicit zero-professional-action counters",
    "add exact rollback fields",
    "add smallest-dependency retry fields",
    "add immutable failure witnesses",
    "add bounded passing witnesses",
    "add stale-label review",
    "add exact Git-blob manifest review",
    "add five-class privacy scan contract",
    "add bounded changed-Python review",
    "add document word ceiling check",
    "add owner file ceiling check",
    "add clean-state and divergence gates",
    "add single-parent zero-merge gates",
    "add successor duplicate guard plan",
    "add no-standby-contact route gate",
    "add Stage 20 nonpromotion guard",
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
    proc = subprocess.run(
        ["git", "-C", str(repo), "show", f"{commit}:{relpath}"],
        check=True,
        capture_output=True,
    )
    return json.loads(proc.stdout.decode("utf-8"))


def inherited_title_corpus(repo: Path) -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    audit_path = "docs/elowen-cairn/v669-v2/x1/semantic-novelty-audit.json"
    audit = git_blob_json(repo, SOURCE_FINAL, audit_path)
    rows: list[dict[str, str]] = []
    sources: list[dict[str, Any]] = []
    for source in audit["source_shards"]:
        payload = git_blob_json(repo, SOURCE_FINAL, source["path"])
        rows.extend({"proposal_id": str(r["proposal_id"]), "title": str(r["title"])} for r in payload["rows"])
        sources.append(source)
    for index in range(1, 9):
        rel = f"docs/elowen-cairn/v669-v2/x1/proposal-freeze-shards/proposals-{index:02d}.json"
        payload = git_blob_json(repo, SOURCE_FINAL, rel)
        raw = subprocess.run(
            ["git", "-C", str(repo), "show", f"{SOURCE_FINAL}:{rel}"],
            check=True,
            capture_output=True,
        ).stdout
        rows.extend({"proposal_id": str(r["proposal_id"]), "title": str(r["title"])} for r in payload["rows"])
        sources.append({"path": rel, "rows": len(payload["rows"]), "sha256": sha256_bytes(raw)})
    deduped = {r["proposal_id"]: r for r in rows}
    return list(deduped.values()), sources


def proposal_rows(corpus: Iterable[dict[str, str]]) -> list[dict[str, Any]]:
    inherited = list(corpus)
    rows: list[dict[str, Any]] = []
    current_titles: list[dict[str, str]] = []
    for index, (slug, title, subject, disposition, approval, sources) in enumerate(PROPOSAL_SPECS, 1):
        proposal_id = f"{PREFIX}-N{index:03d}"
        comparison = inherited + current_titles
        ranked = sorted(
            ({"proposal_id": item["proposal_id"], "title": item["title"], "score": round(jaccard(title, item["title"]), 6)} for item in comparison),
            key=lambda item: (-item["score"], item["proposal_id"]),
        )
        rows.append(
            {
                "approval_class": approval,
                "concrete_artifacts": [
                    f"docs/sylven-arc/v669-v3/x2/proposals/{proposal_id.lower()}-{slug}.json",
                    f"docs/sylven-arc/v669-v3/x2/cards/{proposal_id.lower()}-{slug}.json",
                ],
                "execution_lane": "x2_owner_local_bounded_control" if disposition in {"completed", "represented"} else "held_gap_or_gate",
                "expected_disposition": disposition,
                "falsifier_or_acceptance_gate": (
                    "One bounded synthetic positive contract is accepted, four preregistered invalid mutations are rejected, "
                    "and all real people, objects, rows, measurements, external actions, and authority actions remain zero."
                    if disposition in {"completed", "represented"}
                    else "Remain open or exact-gated until the named evidence and authority requirements are complete."
                ),
                "hypothesis": f"A wholly synthetic zero-person {subject} contract can preserve typed states, vacancies, refusal conditions, and rollback without real-world action or protected claim.",
                "negative_fixtures": [
                    {"mutation_id": f"{proposal_id}-M{m:02d}", "kind": kind, "expected": "reject"}
                    for m, kind in enumerate(
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
        current_titles.append({"proposal_id": proposal_id, "title": title})
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
    root = repo / OWNER_ROOT
    entries: list[dict[str, Any]] = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        rel = path.relative_to(repo).as_posix()
        if rel in exclusions:
            continue
        data = path.read_bytes()
        entries.append({"path": rel, "bytes": len(data), "sha256": sha256_bytes(data)})
    for path in sorted((repo / "scripts").glob("*sylven_arc_v669_v3*.py")):
        rel = path.relative_to(repo).as_posix()
        if rel not in exclusions:
            data = path.read_bytes()
            entries.append({"path": rel, "bytes": len(data), "sha256": sha256_bytes(data)})
    for path in sorted((repo / "scripts").glob("ghc_family_ceramics_*.py")):
        rel = path.relative_to(repo).as_posix()
        if rel not in exclusions:
            data = path.read_bytes()
            entries.append({"path": rel, "bytes": len(data), "sha256": sha256_bytes(data)})
    for path in sorted((repo / "tests").glob("*sylven_arc_v669_v3*.py")):
        rel = path.relative_to(repo).as_posix()
        if rel not in exclusions:
            data = path.read_bytes()
            entries.append({"path": rel, "bytes": len(data), "sha256": sha256_bytes(data)})
    return sorted(entries, key=lambda item: item["path"])


def validate_synthetic_contract(payload: dict[str, Any], expected_slug: str) -> dict[str, Any]:
    """Validate one owner-local synthetic contract without external action."""

    failures: list[str] = []
    if payload.get("semantic_slug") != expected_slug:
        failures.append("semantic_slug_mismatch")
    if payload.get("synthetic_only") is not True:
        failures.append("synthetic_only_required")
    zero = payload.get("zero_counters", {})
    required_zero = [
        "real_people",
        "real_objects",
        "real_measurements",
        "network_calls",
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
