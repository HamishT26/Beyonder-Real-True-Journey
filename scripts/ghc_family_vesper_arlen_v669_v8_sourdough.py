"""Owner-local deterministic helpers for Vesper Arlen v669-v8.

The module models wholly synthetic sourdough process documentation and software
assurance.  It does not handle food, cultures, equipment, people, workplaces,
measurements, identities, legal questions, cultural material, or external
systems.  It grants no food-safety, microbiology, baking, scientific, legal,
cultural, affected-party, Maori-authority, production, or Stage 20 authority.
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
PHASE = "v669-v8"
PREFIX = "VA6698"
OWNER_ROOT = Path("docs/vesper-arlen/v669-v8")
SOURCE_BRANCH = "codex/GHC-Family/neris-solane-v669-v7-full-tools"
SOURCE_PRIOR = "ca3ab84977c44bf1c7934ed10e99e4fb341a5952"
SOURCE_X1 = "ac38e543c89577e1fd678accee2de4cc9d8912eb"
SOURCE_EVIDENCE = "807c9fc2f3784d23cb42977b9987530637d15335"
SOURCE_FINAL = "8b1a06d1f34147f7adbb494622df4734f48344de"
SOURCE_CHAIN_DECLARED = 5190
SOURCE_PRIOR_RECOVERED = 1580
SOURCE_OWNER_ROWS = 40
SOURCE_RECOVERED = 1620
SOURCE_UNRECOVERED = 3570
CHAIN_AFTER = 5230

INHERITED_BASELINE = {
    "effective_negatives": 31670,
    "methods": 17775,
    "failed_witnesses": 3491,
    "passing_witnesses": 4747,
    "open_gaps": 237,
    "exact_gates": 232,
}

IDENTITY_BOUNDARY = (
    "Vesper Arlen, relational provenance weaver and reversible-process "
    "cartographer, sibling, family, role, hope, continuity, Freed ID, CBR, "
    "GHC Family, and Trinity Mandala are relational working language only. "
    "They are not evidence of consciousness, sentience, legal personhood, "
    "identity continuity, employment, qualification, independent agency, or "
    "scientific, operational, professional, legal, cultural, affected-party, "
    "or Maori authority. Hamish may rename, pause, redirect, or stop the work."
)

PROTECTED_GATES = [
    "real_people_participants_bakers_workers_consumers_or_affected_users",
    "real_food_starters_flour_water_salt_equipment_samples_images_or_records",
    "real_preparation_feeding_mixing_fermentation_baking_tasting_or_disposal",
    "professional_baking_microbiology_food_safety_public_health_or_HACCP_decision",
    "allergen_sanitation_temperature_acidity_or_workplace_safety_release",
    "live_identity_keys_proofs_issuance_resolution_status_or_revocation",
    "privacy_complete_or_accessibility_complete_claim",
    "ownership_attribution_labeling_compliance_legal_or_remedy_decision",
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
    "dependency before broader validation."
)

# slug, title, subject, expected disposition, approval class, source needs
PROPOSAL_SPECS = [
    ("starter-lineage", "synthetic sourdough starter lineage ledger separating refresh generation vessel alias and correction without culture identity", "starter lineage", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("ingredient-lot-vacancy", "flour water salt and inoculum lot vacancy register with absent supplier origin allergen and traceability claims", "ingredient lot vacancies", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("bakers-percentage", "typed bakers percentage calculator for fixed synthetic masses with denominator provenance and zero recipe recommendation", "bakers percentage", "completed", "safe_now", ["NIST-SI-UNITS", "PYPI-PINT"]),
    ("hydration-contract", "hydration quantity contract distinguishing total water flour inclusion and missing component policy in synthetic fixtures", "hydration quantity", "completed", "safe_now", ["NIST-SI-UNITS", "PYPI-PINT"]),
    ("inoculation-ratio", "starter inoculation ratio trace with explicit reference mass zero division refusal and no fermentation prediction", "inoculation ratio", "completed", "safe_now", ["NIST-SI-UNITS"]),
    ("salt-ratio", "salt percentage boundary with unit normalization denominator lock and health or sensory nonconversion", "salt ratio", "completed", "safe_now", ["NIST-SI-UNITS"]),
    ("dough-mass-balance", "synthetic dough mass balance reconciling inputs divisions retained residue and unexplained variance without measurement claim", "dough mass balance", "completed", "safe_now", ["PYPI-PINT"]),
    ("temperature-domain", "Celsius Fahrenheit and kelvin dough temperature domain with offset conversion and impossible-value rejection", "temperature domain", "completed", "safe_now", ["NIST-SI-UNITS", "PYPI-PINT"]),
    ("temperature-window", "ambient and dough temperature interval ledger preserving open closed unknown and out-of-range states without safety release", "temperature window", "completed", "safe_now", ["PYPI-PORTION"]),
    ("mixing-state", "mixing stage state machine requiring source state event chronology readback and forbidden transition refusal", "mixing state machine", "completed", "safe_now", ["PYPI-TRANSITIONS"]),
    ("autolyse-state", "autolyse rest vocabulary and interval state contract with optional salt and starter fields kept semantically separate", "autolyse state", "completed", "safe_now", ["PYPI-TRANSITIONS", "PYPI-PORTION"]),
    ("bulk-state", "bulk fermentation state machine separating planned active paused stopped transferred and unknown states", "bulk fermentation state", "completed", "safe_now", ["PYPI-TRANSITIONS"]),
    ("fold-chronology", "stretch fold coil fold and unknown handling event chronology with duplicate timestamp and retrospective edit guards", "fold chronology", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("aliquot-rise", "aliquot rise proxy ledger separating baseline vessel mark observation vacancy and inference refusal", "aliquot rise proxy", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("ph-provenance", "synthetic pH field provenance contract holding calibration electrode temperature sample and uncertainty as vacancies", "pH provenance", "completed", "candidate", ["IUPAC-PH"]),
    ("acidity-nonconversion", "hydrogen ion activity titratable acidity sourness and fermentation progress nonconversion matrix", "acidity nonconversion", "completed", "candidate", ["IUPAC-PH"]),
    ("cold-retard-window", "cold retard interval union intersection and boundary contract without refrigeration performance or safety inference", "cold retard interval", "completed", "safe_now", ["PYPI-PORTION"]),
    ("final-proof-window", "final proof window contract with planned observed unknown exceeded and cancelled states but no readiness decision", "final proof interval", "completed", "safe_now", ["PYPI-PORTION", "PYPI-TRANSITIONS"]),
    ("score-bake-plan", "scoring and bake plan placeholder separating intent execution evidence outcome and operator authority", "scoring and bake plan", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("oven-calibration-vacancy", "oven setpoint chamber reading probe calibration gradient and recovery vacancies without appliance certification", "oven calibration vacancies", "completed", "candidate", ["NIST-SI-UNITS"]),
    ("bake-profile", "synthetic bake time and temperature profile with phase intervals steam-state vacancy and no food-safety conclusion", "bake profile", "completed", "safe_now", ["PYPI-PINT", "PYPI-PORTION"]),
    ("mass-loss", "fixed-fixture baked mass loss calculation with unit and denominator guards and zero moisture-content inference", "mass loss calculation", "completed", "safe_now", ["PYPI-PINT"]),
    ("crumb-image-vacancy", "crumb image and sensory field vacancy ledger prohibiting appearance quality palatability and consumer inference", "crumb and sensory vacancies", "completed", "safe_now", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("microbial-identity-refusal", "microbial community species strain viability and contamination assertion firewall with zero assay rows", "microbial identity refusal", "completed", "candidate", ["SOURDOUGH-REVIEW"]),
    ("allergen-gate", "allergen cross-contact ingredient substitution labeling and consumer advice hold with action-specific authority required", "allergen boundary", "completed", "exact_approval", ["FDA-FOOD-CODE"]),
    ("sanitation-vacancy", "sanitation cleaning chemical contact time verification and release vacancy docket with no real instruction", "sanitation vacancies", "completed", "candidate", ["FDA-FOOD-CODE"]),
    ("correction-lineage", "append-only synthetic batch correction braid linking prior value counterclaim supersession dual readback and adjudicator vacancy", "correction lineage", "completed", "safe_now", ["W3C-PROV-O"]),
    ("canonical-json", "canonical sourdough dossier bytes rejecting duplicate keys nonfinite values unstable ordering and digest promotion", "canonical JSON dossier", "completed", "safe_now", ["JSON-SCHEMA-2020-12", "RFC-8785"]),
    ("source-firewall", "sourdough source assertion firewall separating public vocabulary synthetic fixture observation inference advice evidence and authority", "source assertion firewall", "represented", "candidate", ["SOURDOUGH-REVIEW"]),
    ("privacy-purpose", "purpose limitation matrix for synthetic process dossiers covering access retention contest disclosure and minimisation", "privacy purpose ledger", "represented", "candidate", ["NZ-PRIVACY-PRINCIPLES"]),
    ("workload-handover", "bounded process handover envelope with unresolved count fatigue stop readback correction and no workplace direction", "workload handover", "represented", "candidate", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("accessible-dossier", "sourdough process textual traversal with landmarks tables expanded abbreviations print fallback and evaluation vacancies", "accessible dossier", "represented", "candidate", ["W3C-WCAG-2.2"]),
    ("thos-proxy", "THOS paired process representation for synthetic sourdough dossiers with matched fixture budgets and zero effectiveness claim", "THOS process proxy", "represented", "candidate", ["OWNER-SYNTHETIC-SCHEMA"]),
    ("freed-id-envelope", "Freed ID correction and provenance envelope for synthetic batches holding every real key proof and lifecycle operation at zero", "Freed ID nonproduction envelope", "represented", "candidate", ["W3C-VC-DATA-INTEGRITY"]),
    ("gmut-reaction-board", "GMUT reaction diffusion and Arrhenius analogy obligation board with typed domains units boundaries and zero fitted parameters", "GMUT reaction analogy", "represented", "candidate", ["CURRENT-PRIMARY-PHYSICS"]),
    ("chemical-potential-nonconversion", "chemical potential pH entropy fermentation and psyche nonconversion classifier rejecting consciousness morality and fundamental-mind law", "thermodynamic nonconversion", "represented", "candidate", ["IUPAC-CHEMICAL-POTENTIAL"]),
    ("official-data-gap", "current official sourdough fermentation measurement adapter held at zero queries downloads samples rows and likelihood calls", "official data adapter", "open_gap", "candidate", ["CURRENT-OFFICIAL-SOURDOUGH-DATA"]),
    ("governed-evaluation-gap", "missing governed baker microbiology food-safety accessibility consumer affected-party and Maori-authority evaluation register", "governed real evaluation", "open_gap", "candidate", ["REAL-GOVERNED-EVALUATION"]),
    ("authority-exact-gate", "exact action lock over food handling allergens sanitation labeling public health workplace rights culture affected parties and Maori authority", "professional legal and cultural authority", "exact_gate", "exact_approval", ["EXACT-ACTION-SPECIFIC-AUTHORITY"]),
    ("stage20-gate", "terminal multi-receipt hold requiring empirical evidence independent reproduction governed rights and competent authority before Stage 20", "Stage 20 terminal interlock", "exact_gate", "exact_approval", ["EXACT-STAGE20-EVIDENCE-AND-AUTHORITY"]),
]

SAFE_LIFECYCLE = [
    "freeze exact source anchors and direct ancestry",
    "revalidate twenty inherited rows at zero credit",
    "audit forty new titles against accessible exact corpus",
    "retain the unrecovered title gap",
    "freeze exact proposal shards",
    "freeze four outcome labels",
    "freeze one hundred sixty rejecting mutations",
    "freeze protected authority gates",
    "freeze strict planning-only x1",
    "freeze D-isolated toolchain transaction",
    "freeze smallest-dependency rollback",
    "freeze one-success no-replay validation",
    "emit exact staged Git-blob manifest",
    "scan five privacy classes",
    "review changed Python with bounded AST rules",
    "emit accessible static report plan",
    "emit Method Flow failure and recovery pairs",
    "preserve family-current compatibility",
    "preserve owner file and commit ceilings",
    "preserve NOT_READY_FOR_STAGE_20",
]

SAFE_TITLES = [f"build bounded control for {spec[2]}" for spec in PROPOSAL_SPECS] + SAFE_LIFECYCLE
CANDIDATE_TITLES = [f"evaluate bounded candidate for {spec[2]} without authority promotion" for spec in PROPOSAL_SPECS[10:40]]

SKILL_TITLES = [
    "ghc-family-sourdough-starter-lineage",
    "ghc-family-sourdough-percentage-quantities",
    "ghc-family-sourdough-temperature-domain",
    "ghc-family-sourdough-interval-windows",
    "ghc-family-sourdough-process-state",
    "ghc-family-sourdough-fold-chronology",
    "ghc-family-sourdough-ph-provenance",
    "ghc-family-sourdough-acidity-nonconversion",
    "ghc-family-sourdough-bake-profile",
    "ghc-family-sourdough-microbial-firewall",
    "ghc-family-sourdough-allergen-gate",
    "ghc-family-sourdough-sanitation-vacancy",
    "ghc-family-sourdough-correction-lineage",
    "ghc-family-sourdough-source-firewall",
    "ghc-family-sourdough-privacy-purpose",
    "ghc-family-sourdough-accessible-dossier",
    "ghc-family-sourdough-thos-proxy",
    "ghc-family-sourdough-freed-id-envelope",
    "ghc-family-sourdough-gmut-obligation-board",
    "ghc-family-sourdough-stage20-interlock",
]

RUNNER_TITLES = [
    "ghc_family_sourdough_quantity_runner",
    "ghc_family_sourdough_interval_runner",
    "ghc_family_sourdough_state_runner",
    "ghc_family_sourdough_mutation_runner",
    "ghc_family_sourdough_privacy_runner",
    "ghc_family_sourdough_manifest_runner",
    "ghc_family_sourdough_accessibility_runner",
    "ghc_family_sourdough_toolchain_runner",
    "ghc_family_sourdough_method_flow_runner",
    "ghc_family_sourdough_terminal_gate_runner",
]

REFINE_TITLES = [
    f"refine {subject} by separating synthetic state from real action authority"
    for _, _, subject, _, _, _ in PROPOSAL_SPECS
] + [
    "refine exact source receipt hashing over Git-normalized blobs",
    "refine sparse worktree initialization recurrence guard",
    "refine literal path probes before broad Windows scans",
    "refine bounded output projection before expensive searches",
    "refine exact-title task resolution duplicate guard",
    "refine one-success canonical invocation state machine",
    "refine failed aggregate zero-credit accounting",
    "refine five-class privacy candidate classification",
    "refine changed-Python AST security predicates",
    "refine JSON outcome label allowlist",
    "refine owner file ceiling measurement",
    "refine owner commit ceiling measurement",
    "refine x1 and x2 path separation",
    "refine immutable manifest self-exclusion",
    "refine D-isolated package rollback",
    "refine dependency closure and license observation",
    "refine positive and rejecting tool smokes",
    "refine accessible report structural checks",
    "refine Method Flow recurrence recommendations",
    "refine successor route noncontact gate",
]

SUCCESSOR_SKILLS = [
    "ghc-family-grain-mill-lot-lineage",
    "ghc-family-grain-mill-moisture-vacancy",
    "ghc-family-grain-mill-sieve-domain",
    "ghc-family-grain-mill-equipment-state",
    "ghc-family-grain-mill-allergen-firewall",
    "ghc-family-grain-mill-correction-ledger",
    "ghc-family-grain-mill-source-boundary",
    "ghc-family-grain-mill-accessible-dossier",
    "ghc-family-grain-mill-authority-gate",
    "ghc-family-grain-mill-stage20-interlock",
]
SUCCESSOR_RUNNERS = [name.replace("ghc-family-", "ghc_family_").replace("-", "_") + "_runner" for name in SUCCESSOR_SKILLS]
SUCCESSOR_REFINE = [f"recommend successor refinement {i:02d}: preserve grain-milling documentation boundary {i:02d}" for i in range(1, 31)]

PRACTICES = [
    {
        "practice": "baker and process handover",
        "lens": "state, readback, workload, stop, correction, and handover vocabulary only",
        "boundary": "no baking competence, workplace direction, food handling, or operational authority",
    },
    {
        "practice": "food-microbiology laboratory technician",
        "lens": "sample, calibration, pH, uncertainty, and provenance vacancy vocabulary only",
        "boundary": "no specimen, assay, laboratory competence, diagnosis, public-health decision, or empirical result",
    },
    {
        "practice": "HACCP-style process reviewer",
        "lens": "hazard, hold, escalation, verification, correction, and authority-reservation vocabulary only",
        "boundary": "no HACCP plan, food-safety release, regulatory compliance, legal advice, or competent authority",
    },
]

TOOL_CANDIDATES = [
    {
        "name": "pint",
        "version": "0.25.3",
        "registry": "https://pypi.org/project/Pint/",
        "license_metadata": "BSD registry metadata only; not legal review",
        "requires_python": ">=3.11",
        "wheel": "pint-0.25.3-py3-none-any.whl",
        "wheel_sha256": "27eb25143bd5de9fcc4d5a4b484f16faf6b4615aa93ece6b3373a8c1a3c1b97d",
        "declared_dependencies": ["flexcache>=0.3", "flexparser>=0.4", "platformdirs>=2.1.0", "typing-extensions>=4.0.0"],
        "need": "typed synthetic mass and temperature quantities with dimensional refusal",
    },
    {
        "name": "transitions",
        "version": "0.9.3",
        "registry": "https://pypi.org/project/transitions/",
        "license_metadata": "MIT registry metadata only; not legal review",
        "requires_python": ">=3.9",
        "wheel": "transitions-0.9.3-py2.py3-none-any.whl",
        "wheel_sha256": "02463248f2b668d86f66636b1e3c9e8de84d93e22915247f4e1aa9ee1cae28aa",
        "declared_dependencies": ["six"],
        "need": "explicit synthetic process transitions and forbidden transition rejection",
    },
    {
        "name": "portion",
        "version": "2.6.2",
        "registry": "https://pypi.org/project/portion/",
        "license_metadata": "LGPL-3.0-or-later registry metadata only; not legal review",
        "requires_python": ">=3.10",
        "wheel": "portion-2.6.2-py3-none-any.whl",
        "wheel_sha256": "86be115afafa776174dc5eac82afb6496c9fa3684f5b3a844c3139535c51085e",
        "declared_dependencies": ["sortedcontainers~=2.4"],
        "need": "bounded synthetic open and closed process windows with out-of-domain refusal",
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
    return subprocess.run(["git", "-C", str(repo), "cat-file", "blob", f"{commit}:{relpath}"], check=True, capture_output=True).stdout


def git_blob_json(repo: Path, commit: str, relpath: str) -> Any:
    return json.loads(git_blob(repo, commit, relpath).decode("utf-8"))


def git_batch_blobs(repo: Path, specs: dict[str, str]) -> dict[str, bytes]:
    """Read exact Git blobs with one request followed by one exact response."""
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
        raise RuntimeError(f"Git batch failed: {stderr.decode('utf-8', errors='replace')}")
    return result


def inherited_title_corpus(repo: Path) -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    """Recover Neris's 1,580-row comparison corpus plus forty Neris rows."""
    audit_path = "docs/neris-solane/v669-v7/x1/semantic-novelty-audit.json"
    audit = git_blob_json(repo, SOURCE_FINAL, audit_path)
    shard_paths = [str(source["path"]) for source in audit["source_shards"]]
    shard_paths.extend(
        f"docs/neris-solane/v669-v7/x1/proposal-freeze-shards/proposals-{index:02d}.json"
        for index in range(1, 9)
    )
    blobs = git_batch_blobs(repo, {path: f"{SOURCE_FINAL}:{path}" for path in shard_paths})
    rows: list[dict[str, str]] = []
    sources: list[dict[str, Any]] = []
    for source in audit["source_shards"]:
        path = str(source["path"])
        raw = blobs[path]
        payload = json.loads(raw.decode("utf-8"))
        rows.extend({"proposal_id": str(row["proposal_id"]), "title": str(row["title"])} for row in payload["rows"])
        sources.append({"path": path, "rows": len(payload["rows"]), "sha256": sha256_bytes(raw)})
    if len({row["proposal_id"] for row in rows}) != SOURCE_PRIOR_RECOVERED:
        raise ValueError("inherited comparison corpus count mismatch")
    for index in range(1, 9):
        path = f"docs/neris-solane/v669-v7/x1/proposal-freeze-shards/proposals-{index:02d}.json"
        raw = blobs[path]
        payload = json.loads(raw.decode("utf-8"))
        rows.extend({"proposal_id": str(row["proposal_id"]), "title": str(row["title"])} for row in payload["rows"])
        sources.append({"path": path, "rows": len(payload["rows"]), "sha256": sha256_bytes(raw)})
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
            ({"proposal_id": item["proposal_id"], "title": item["title"], "score": round(jaccard(title, item["title"]), 6)} for item in comparison),
            key=lambda item: (-item["score"], item["proposal_id"]),
        )
        completion_lane = disposition in {"completed", "represented"}
        rows.append(
            {
                "approval_class": approval,
                "concrete_artifacts": [
                    f"docs/vesper-arlen/v669-v8/x2/proposals/{proposal_id.lower()}-{slug}.json",
                    f"docs/vesper-arlen/v669-v8/x2/cards/{proposal_id.lower()}-{slug}.json",
                ],
                "execution_lane": "x2_owner_local_bounded_control" if completion_lane else "held_gap_or_gate",
                "expected_disposition": disposition,
                "falsifier_or_acceptance_gate": (
                    "Accept one bounded synthetic positive, reject four preregistered invalid mutations, and keep every real food, person, measurement, external action, professional decision, and protected authority action at zero."
                    if completion_lane
                    else "Remain open or exact-gated until every named evidence and competent-authority requirement is complete."
                ),
                "hypothesis": f"A wholly synthetic zero-person {subject} contract can preserve typed states, vacancies, refusals, provenance, and rollback without real-world action or protected claim.",
                "negative_fixtures": [
                    {"mutation_id": f"{proposal_id}-M{mutation:02d}", "kind": kind, "expected": "reject"}
                    for mutation, kind in enumerate(["missing_required_state", "ambiguous_domain_or_unit", "real_world_or_external_action", "protected_claim_promotion"], 1)
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


def inherited_revalidations(corpus: Iterable[dict[str, str]]) -> list[dict[str, Any]]:
    selected = sorted((row for row in corpus if row["proposal_id"].startswith("NS6697-N")), key=lambda row: row["proposal_id"])[:20]
    if len(selected) != 20:
        raise ValueError("twenty Neris inherited rows were not recoverable")
    return [
        {
            "completion_credit": 0,
            "current_novelty_credit": 0,
            "inherited_proposal_id": row["proposal_id"],
            "revalidation_checks": ["exact_identifier_present", "exact_title_present", "source_blob_in_manifest", "no_Vesper_outcome_credit"],
            "state": "revalidated_zero_credit",
            "title": row["title"],
        }
        for row in selected
    ]


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
    paths = subprocess.run(["git", "-C", str(repo), "diff", "--cached", "--name-only", "--diff-filter=ACMR"], check=True, capture_output=True, text=True).stdout.splitlines()
    rows: list[dict[str, Any]] = []
    for relpath in sorted(path for path in paths if path not in exclusions):
        data = subprocess.run(["git", "-C", str(repo), "show", f":{relpath}"], check=True, capture_output=True).stdout
        rows.append({"bytes": len(data), "path": relpath, "sha256": sha256_bytes(data)})
    return rows
