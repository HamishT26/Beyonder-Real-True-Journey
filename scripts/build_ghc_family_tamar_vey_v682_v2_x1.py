from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "tamar-vey" / "v682-v2"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"

OWNER = "Tamar Vey"
PHASE = "v682-v2"
BRANCH = "codex/GHC-Family/tamar-vey-v682-v2-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/liora-venn-v682-v1-full-tools"
SOURCE = "34536c2bb4c9fefb04cc0b571839e9ba54b3c497"
SOURCE_X1 = "d538a40de6b9dcdba6a35ffc99fd6848b09dbbbe"
SOURCE_EVIDENCE = "638943335e1485663b500eb1d2b2847cfeba5d59"
SOURCE_PARENT = "15d23e8b4e85082d4e4a839ab85d409a4c9c9805"
SOURCE_CANONICAL_RECEIPT_SHA256 = "93f799cd8ea41f317b06a7eeb839847d4cd4645ec1fd6b5a1bac860528d36c2c"
DECLARED_CHAIN_BEFORE = 10250
DECLARED_CHAIN_AFTER = 10310
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
CHECKED_AT_UTC = "2026-09-01T13:52:16Z"
WRITTEN: list[str] = []

ACTIVATION_BASELINE = {
    "effective_negatives": 55489,
    "effective_methods": 65141,
    "failed_witnesses": 27150,
    "bounded_passing_witnesses": 46603,
    "open_gaps": 491,
    "exact_gates": 482,
}

PROPOSAL_TITLES = [
    "Synthetic basketry work capsule and surrogate basket identity split",
    "Basket base wall rim handle lid and attachment topology with orphan quarantine",
    "Coiled twined plaited woven and unknown construction vocabulary without identification",
    "Splint rod cane fibre bark grass and unknown material vacancy ledger",
    "Basket orientation load-bearing zone and support-point proposal separated from observation",
    "Basket container tray ring support and shelf-location graph with zero storage action",
    "Shape deformation break abrasion loss and unknown cue register without condition diagnosis",
    "Maker seller donor custodian and cataloguer role vacancies with minimized identifiers",
    "Basket pattern colour motif and decoration description separated from cultural interpretation",
    "Basket dimension target unit precision uncertainty and zero-observation firewall",
    "Basket image view scale crop derivative and rights lineage",
    "Basket handling plan stop-work fragile-object hold and no-release state",
    "Basket pest mould moisture and contamination cue vacancy without diagnosis",
    "Basket cleaning reshaping consolidation and material-use plan under intervention hold",
    "Represented basket correction challenge supersession and dual-readback provenance braid",
    "Represented accessible basket summary with noncolour status and manual evaluation reserve",
    "Represented basket workload batch ceiling pause and next-shift handover queue",
    "Represented basket provenance custody ownership access and return topology with unresolved rights",
    "Synthetic lapidary work capsule and surrogate stone identity split",
    "Rough preform cabochon faceted carving and unknown form vocabulary without classification",
    "Slab blank dop fixture wheel lap belt and enclosure component topology",
    "Mineral gem trade-name treatment and composition assertion firewall",
    "Colour transparency lustre hardness cleavage and inclusion cue vocabulary without identification",
    "Cut plan orientation facet index angle and symmetry target graph with zero measurement",
    "Abrasive grit coolant lubricant compound and unknown material vacancy ledger",
    "Wheel guard splash shield ventilation and energy-isolation state with no work release",
    "Cutting grinding sanding polishing and cleaning plan versus executed-action separation",
    "Lapidary dimension target unit tolerance uncertainty and calibration vacancy",
    "Weight mass density and specific-gravity target without measurement or inference",
    "Heat fracture chip dust splash noise and electrical cue board without safety decision",
    "Stone material provenance supplier batch custody and substitution-challenge lineage",
    "Lapidary image lighting scale colour-reference and derivative provenance",
    "Represented synthetic treatment disclosure and unsigned certificate vacancy without authenticity claim",
    "Represented lapidary correction challenge reclassification and immutable prior-value lineage",
    "Represented accessible lapidary job summary with affected-user evaluation reserve",
    "Represented lapidary workload pause unresolved hold and shift-handover lease",
    "Synthetic sundial documentation capsule and surrogate instrument identity split",
    "Gnomon style dial plate hour-line noon-line and mounting topology",
    "Horizontal vertical equatorial polar and unknown dial-form vocabulary without classification",
    "Apparent solar mean solar standard civil and UTC time-scale separation",
    "Local meridian longitude zone offset daylight rule and location-vacancy firewall",
    "Latitude declination hour angle shadow and equation-of-time symbol table with unit checks",
    "Target dial geometry measured geometry and observational evidence separation",
    "Dial-line computation plan input-domain precision uncertainty and no-calibration claim",
    "Shadow point interval occlusion reflection refraction and weather-vacancy board",
    "Dial orientation level alignment mounting and site-suitability proposal versus action separation",
    "Sundial material finish corrosion crack and legibility cue register without condition finding",
    "Dial engraving inscription language translation and interpretation provenance",
    "Sundial diagram photograph scan transcription scale and derivative lineage",
    "Sundial correction challenge supersession and recalculation readback braid",
    "Represented accessible dial explanation with text alternatives and manual evaluation reserve",
    "Represented maintenance intervention cleaning repair and release exact-hold structure",
    "Represented daylight workload glare heat weather pause and handover queue",
    "Represented GMUT celestial-coordinate proxy with zero observation or physical inference",
    "Open gap for basketmaker conservator materials accessibility and affected-community evaluation",
    "Open gap for lapidary professional real materials machine safety measurements and independent review",
    "Open gap for sundial designer real site solar observations accessibility and independent review",
    "Exact gate for basket ownership cultural meaning traditional knowledge taonga Māori data and affected-party authority",
    "Exact gate for lapidary material authenticity mining provenance workplace release legal rights and environmental authority",
    "Exact terminal gate for sundial site installation heritage land cultural interpretation empirical GMUT production canon personhood and Stage 20",
]

MUTATION_TYPES = [
    "missing_required_field",
    "lifecycle_inversion",
    "stale_provenance_digest",
    "safety_status_promotion",
    "authority_promotion",
]

PROTECTED_GATES = [
    "real people baskets stones sundials sites objects materials tools machines and measurements",
    "empirical GMUT likelihoods constraints predictions observations and confirmation",
    "professional basketry conservation lapidary mineralogy sundial design workplace safety and release authority",
    "production identity issuance resolution status revocation interoperability and trust governance",
    "ownership heritage traditional knowledge legal cultural affected-party and Māori authority",
    "privacy-complete accessibility-complete and exhaustive-security claims",
    "independent reproduction AGI ASI consciousness personhood Theory of Everything proof canon and Stage 20",
]

STARTUP_FAILURES = [
    {
        "failure_id": "TV6822-ST-N001",
        "failed_witness": "The first memory-registry probe assumed MEMORY.md lived directly under the Codex home and failed on the absent path.",
        "initial_credit": 0,
        "recovery": "Use the configured memories/MEMORY.md registry and retain the failed path assumption.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "TV6822-ST-N002",
        "failed_witness": "A combined authorization schema and current-state display clipped the current-state middle.",
        "initial_credit": 0,
        "recovery": "Read the current-state document in bounded ordered windows through EOF and preserve the clipped display.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "TV6822-ST-N003",
        "failed_witness": "PowerShell rejected a roster foreach result piped before materialization with EmptyPipeElement.",
        "initial_credit": 0,
        "recovery": "Materialize the roster projection array before JSON serialization.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "TV6822-ST-N004",
        "failed_witness": "The first Truth Bridge read exceeded the aggregate context window before an attributable EOF witness.",
        "initial_credit": 0,
        "recovery": "Measure the exact file and read its sixty-one lines through EOF in one bounded projection.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "TV6822-ST-N005",
        "failed_witness": "A Method Flow summary projection accidentally forwarded the full mutation and positive arrays and clipped its display.",
        "initial_credit": 0,
        "recovery": "Project only counts, uniqueness, boundary booleans, and first and last witnesses from the unchanged parsed ledger.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "TV6822-ST-N006",
        "failed_witness": "A combined branch path and worktree-list absence probe outlived its display window and exposed no session handle.",
        "initial_credit": 0,
        "recovery": "Inspect the attributable Git process to completion, prove the path remained absent, then use separate local and live-remote branch scalars.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "TV6822-X1-N001",
        "failed_witness": "The first multi-pattern Git grep novelty probe returned no bounded attributable payload.",
        "initial_credit": 0,
        "recovery": "Use one exact-source cat-file batch, retain its session handle, and project only bounded proposal-title matches.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "TV6822-X1-N002",
        "failed_witness": "The first combined official-source web search returned no attributable result.",
        "initial_credit": 0,
        "recovery": "Query official domains narrowly and use the resulting pages only for vocabulary and refusal conditions.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "TV6822-X1-N003",
        "failed_witness": "A broad spelling audit forwarded repeated generated proposal content and clipped its display.",
        "initial_credit": 0,
        "recovery": "Inspect only the builder definitions, correct the relational wording there, and regenerate every derived artifact and hash.",
        "recovery_credit": "bounded_dependency_only",
    },
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def git(*args: str, check: bool = True, text: bool = True) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=check,
        capture_output=True,
        text=text,
        encoding="utf-8" if text else None,
    )


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    WRITTEN.append(rel(path))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")
    WRITTEN.append(rel(path))


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def jaccard(left: str, right: str) -> float:
    left_tokens = set(re.findall(r"[a-z0-9]+", left.casefold()))
    right_tokens = set(re.findall(r"[a-z0-9]+", right.casefold()))
    if not left_tokens and not right_tokens:
        return 1.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def disposition(index: int) -> str:
    if index <= 42:
        return "completed"
    if index <= 54:
        return "represented"
    if index <= 57:
        return "open_gap"
    return "exact_gate"


def approval_class(index: int) -> str:
    if index <= 42:
        return "safe_now"
    if index <= 57:
        return "bounded_candidate"
    return "exact_approval"


def execution_lane(index: int) -> str:
    if index <= 42:
        return "owner_local_synthetic_zero_row"
    if index <= 54:
        return "represented_external_evidence_vacancy"
    if index <= 57:
        return "open_external_evidence_gap"
    return "unexecuted_competent_authority_gate"


def source_needs(index: int) -> list[str]:
    if index <= 18:
        return ["NPS-COG-05-01", "W3C-PROV-O", "W3C-WCAG22"]
    if index <= 36:
        return ["OSHA-1910-212", "OSHA-CPL-2022-01", "W3C-PROV-O"]
    if index <= 54:
        return ["NIST-SOLAR-TIME", "NIST-SP559R1", "W3C-PROV-O"]
    if index == 55:
        return ["NPS-COG-05-01", "W3C-WCAG22"]
    if index == 56:
        return ["OSHA-1910-212", "OSHA-CPL-2022-01"]
    if index == 57:
        return ["NIST-SOLAR-TIME", "W3C-WCAG22"]
    if index == 58:
        return ["TMR-MDS-PRINCIPLES", "W3C-PROV-O"]
    if index == 59:
        return ["OSHA-1910-212", "W3C-PROV-O"]
    return ["NIST-SOLAR-TIME", "TMR-MDS-PRINCIPLES"]


def proposals() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, title in enumerate(PROPOSAL_TITLES, start=1):
        proposal_id = f"TV6822-N{index:03d}"
        rows.append(
            {
                "approval_class": approval_class(index),
                "concrete_artifacts": [
                    f"docs/tamar-vey/v682-v2/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/tamar-vey/v682-v2/x2/mutations.json#{proposal_id}",
                ],
                "execution_lane": execution_lane(index),
                "expected_disposition": disposition(index),
                "falsifier_or_acceptance_gate": (
                    f"Accept only if {proposal_id} has one bounded zero-row positive witness, all five invalid "
                    "mutations are rejected, and no empirical, professional, production, legal, cultural, "
                    "affected-party, Māori-authority, or Stage 20 claim is promoted."
                ),
                "hypothesis": (
                    f"A wholly synthetic zero-row contract for {title.casefold()} can preserve the named state "
                    "distinction and reject preregistered counterexamples within owner-local scope."
                ),
                "null_or_failure_condition": (
                    f"{proposal_id} is falsified if an invalid fixture is accepted, its bounded positive structure "
                    "is rejected, a real-world state is inferred, or any protected gate is promoted."
                ),
                "official_or_primary_source_needs": source_needs(index),
                "preregistered_rejecting_mutations": [
                    {
                        "expected_result": "rejected_zero_credit",
                        "mutation_id": f"{proposal_id}-M{mutation_index:02d}",
                        "mutation_type": mutation_type,
                    }
                    for mutation_index, mutation_type in enumerate(MUTATION_TYPES, start=1)
                ],
                "proposal_id": proposal_id,
                "protected_gates": PROTECTED_GATES,
                "rollback_or_recovery": (
                    f"Quarantine only the {proposal_id} witness, retain the failed receipt at zero credit, and "
                    "regenerate from this immutable planning contract."
                ),
                "title": title,
            }
        )
    return rows


def iter_proposal_records(value: Any) -> Iterable[dict[str, str]]:
    if isinstance(value, dict):
        proposal_id = value.get("proposal_id")
        title = value.get("title")
        if isinstance(proposal_id, str) and isinstance(title, str):
            yield {"proposal_id": proposal_id, "title": title}
        for child in value.values():
            yield from iter_proposal_records(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_proposal_records(child)


def batch_blobs(tree: str, paths: list[str]) -> Iterable[tuple[str, bytes]]:
    proc = subprocess.Popen(
        ["git", "-C", str(ROOT), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert proc.stdin is not None and proc.stdout is not None
    try:
        for path in paths:
            proc.stdin.write(f"{tree}:{path}\n".encode("utf-8"))
            proc.stdin.flush()
            header = proc.stdout.readline().decode("utf-8", errors="replace").rstrip("\n")
            if header.endswith(" missing"):
                continue
            parts = header.split()
            if len(parts) != 3 or parts[1] != "blob":
                raise RuntimeError(f"unexpected cat-file header for {path}: {header}")
            size = int(parts[2])
            data = proc.stdout.read(size)
            if proc.stdout.read(1) != b"\n":
                raise RuntimeError(f"missing cat-file separator for {path}")
            yield path, data
    finally:
        proc.stdin.close()
        proc.terminate()
        proc.wait(timeout=10)


def proposal_chain_audit(new_records: list[dict[str, Any]]) -> dict[str, Any]:
    grep_result = git("grep", "-l", "-I", '"proposal_id"', SOURCE, "--", "*.json", check=False)
    if grep_result.returncode not in (0, 1):
        raise RuntimeError(grep_result.stderr)
    raw_paths = sorted(set(filter(None, grep_result.stdout.splitlines())))
    tree_prefix = SOURCE + ":"
    paths = [path[len(tree_prefix) :] if path.startswith(tree_prefix) else path for path in raw_paths]
    parsed = 0
    parse_failures: list[dict[str, str]] = []
    inherited: list[dict[str, str]] = []
    for path, data in batch_blobs(SOURCE, paths):
        try:
            document = json.loads(data.decode("utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            parse_failures.append({"path": path, "error": type(exc).__name__})
            continue
        parsed += 1
        for record in iter_proposal_records(document):
            inherited.append({"path": path, **record})
    if not paths or parsed == 0 or not inherited:
        raise RuntimeError("proposal audit must parse nonzero exact-source paths and id-title records")

    inherited_titles = {record["title"] for record in inherited}
    exact_collisions: list[str] = []
    neighbors: list[dict[str, Any]] = []
    for proposal in new_records:
        title = proposal["title"]
        if title in inherited_titles:
            exact_collisions.append(title)
        best: dict[str, str] | None = None
        best_score = -1.0
        for record in inherited:
            score = jaccard(title, record["title"])
            if score > best_score:
                best_score = score
                best = record
        neighbors.append(
            {
                "best_inherited_neighbor": best,
                "proposal_id": proposal["proposal_id"],
                "quarantined": best_score >= 0.78,
                "title": title,
                "token_jaccard": round(best_score, 6),
            }
        )
    quarantined = [row for row in neighbors if row["quarantined"]]
    if exact_collisions or quarantined:
        raise RuntimeError(
            "proposal novelty quarantine required: "
            + json.dumps({"exact": exact_collisions, "neighbors": quarantined}, ensure_ascii=False)
        )
    return {
        "audit_scope": {
            "claim": "bounded all-reachable exact-source proposal audit; no universal 10250-row proof",
            "proposal_json_parse_failures": parse_failures,
            "proposal_json_paths_discovered": len(paths),
            "proposal_json_paths_parsed": parsed,
            "reachable_id_title_records": len(inherited),
            "universal_10250_row_materialization_claimed": False,
        },
        "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
        "declared_chain_before": DECLARED_CHAIN_BEFORE,
        "exact_title_collisions": exact_collisions,
        "maximum_neighbor_score": max(row["token_jaccard"] for row in neighbors),
        "neighbor_reviews": neighbors,
        "new_proposal_count": len(new_records),
        "owner": OWNER,
        "phase": PHASE,
        "quarantine_threshold_token_jaccard": 0.78,
        "quarantined_neighbors": quarantined,
        "schema": "ghc.family.proposal-chain-audit.v682.v2.x1",
        "source": SOURCE,
    }


def task_records(prefix: str, count: int, lane: str) -> list[dict[str, Any]]:
    return [
        {
            "approval_required": lane in {"exact_approval", "blocked"},
            "lane": lane,
            "planned_action": f"Preregistered Tamar owner-local {lane.replace('_', ' ')} item {index:03d}.",
            "state": "preregistered_not_executed",
            "task_id": f"TV6822-{prefix}-{index:03d}",
        }
        for index in range(1, count + 1)
    ]


SKILL_NAMES = [
    "basket-object-identity-separator",
    "basket-component-topology",
    "construction-vocabulary-firewall",
    "basket-material-claim-vacancy",
    "support-observation-separator",
    "cultural-meaning-authority-gate",
    "stone-object-identity-separator",
    "lapidary-component-topology",
    "mineral-assertion-firewall",
    "facet-target-unit-board",
    "abrasive-material-vacancy",
    "machine-release-hold",
    "dust-hazard-nondecision",
    "sundial-identity-separator",
    "time-scale-firewall",
    "dial-geometry-symbol-board",
    "solar-observation-vacancy",
    "accessible-status-summary",
    "correction-readback",
    "authority-noncompensation",
]


def portfolio_freeze() -> dict[str, Any]:
    return {
        "blocked": task_records("BLOCK", 10, "blocked"),
        "caps_are_ceilings": True,
        "commit_cap": 3,
        "document_word_cap": 100000,
        "exact_approval": task_records("EXACT", 20, "exact_approval"),
        "materialized_file_stop": 2000,
        "owner": OWNER,
        "owner_candidates": task_records("CAND", 80, "bounded_candidate"),
        "owner_clean_fix_refine": task_records("CFR", 100, "clean_fix_refine"),
        "owner_practice_lenses": [
            "wholly synthetic basketry documentation and collection-support planning",
            "wholly synthetic lapidary work-order and material-claim vacancy planning",
            "wholly synthetic sundial documentation and solar-time symbol modelling",
        ],
        "owner_runner_ideas": [
            {
                "runner_id": f"TV6822-RUNNER-{index:02d}",
                "name": f"ghc_family_basketry_lapidary_sundial_runner_{index:02d}.py",
                "state": "planned_not_built_in_x1",
            }
            for index in range(1, 11)
        ],
        "owner_skill_ideas": [
            {
                "skill_id": f"TV6822-SKILL-{index:02d}",
                "name": name,
                "state": "planned_not_built_in_x1",
            }
            for index, name in enumerate(SKILL_NAMES, start=1)
        ],
        "phase": PHASE,
        "primary_pillar": "GMUT Mind",
        "represented_pillars": ["THOS Body", "Freed ID and CBR Heart"],
        "safe_now": task_records("SAFE", 120, "safe_now"),
        "schema": "ghc.family.portfolio-freeze.v682.v2.x1",
        "successor_candidates": task_records("SUCCESSOR-CAND", 20, "successor_candidate_zero_credit"),
        "successor_clean_fix_refine": task_records("SUCCESSOR-CFR", 30, "successor_recommendation_zero_credit"),
        "successor_practice_recommendation": (
            "exactly one zero-credit seed: synthetic glass-engraving documentation; successor must audit novelty independently"
        ),
        "successor_runner_ideas": task_records("SUCCESSOR-RUNNER", 10, "successor_runner_seed_zero_credit"),
        "successor_skill_ideas": task_records("SUCCESSOR-SKILL", 10, "successor_skill_seed_zero_credit"),
    }


def official_sources() -> dict[str, Any]:
    entries = [
        {
            "source_id": "NPS-COG-05-01",
            "status": "official_NPS_source_checked_2026-09-02",
            "title": "Storage Supports for Basket Collections",
            "url": "https://www.nps.gov/subjects/museums/upload/05-01_508.pdf",
            "use": "basket-support, handling-vacancy, and professional-referral vocabulary only",
        },
        {
            "source_id": "OSHA-1910-212",
            "status": "official_OSHA_current_standard_checked_2026-09-02",
            "title": "General requirements for all machines",
            "url": "https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.212",
            "use": "machine-guarding and stop-state vocabulary only; no workplace release or legal interpretation",
        },
        {
            "source_id": "OSHA-CPL-2022-01",
            "status": "official_OSHA_source_checked_2026-09-02",
            "title": "Regional Emphasis Program on Silica in Cut Stone and Slab Handling",
            "url": "https://www.osha.gov/sites/default/files/enforcement/directives/CPL_2022-01.pdf",
            "use": "stone-dust hazard-vacancy and professional-review boundary only",
        },
        {
            "source_id": "NIST-SOLAR-TIME",
            "status": "official_NIST_page_checked_2026-09-02",
            "title": "Time and Frequency from A to Z: Solar Time",
            "url": "https://www.nist.gov/pml/time-and-frequency-division/popular-links/time-frequency-z/time-and-frequency-z-s-so",
            "use": "apparent-solar, mean-solar, local-noon, and equation-of-time vocabulary only",
        },
        {
            "source_id": "NIST-SP559R1",
            "status": "official_NIST_publication_checked_2026-09-02",
            "title": "Time and Frequency Users Manual",
            "url": "https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication559r1.pdf",
            "use": "solar-time and sundial distinction vocabulary only; no calibration or observation claim",
        },
        {
            "source_id": "W3C-PROV-O",
            "status": "W3C_Recommendation_checked_2026-09-02",
            "title": "PROV-O: The PROV Ontology",
            "url": "https://www.w3.org/TR/prov-o/",
            "use": "entity, activity, revision, derivation, and provenance vocabulary only",
        },
        {
            "source_id": "W3C-WCAG22",
            "status": "W3C_Recommendation_checked_2026-09-02",
            "title": "Web Content Accessibility Guidelines 2.2",
            "url": "https://www.w3.org/TR/WCAG22/",
            "use": "structural accessibility vocabulary and manual-evaluation reservation only",
        },
        {
            "source_id": "W3C-VC-DM-20",
            "status": "W3C_Recommendation_checked_2026-09-02",
            "title": "Verifiable Credentials Data Model v2.0",
            "url": "https://www.w3.org/TR/vc-data-model-2.0/",
            "use": "synthetic credential lifecycle and proof-vacancy vocabulary only",
        },
        {
            "source_id": "RFC8785",
            "status": "RFC_stable_checked_2026-09-02",
            "title": "JSON Canonicalization Scheme",
            "url": "https://www.rfc-editor.org/rfc/rfc8785",
            "use": "deterministic synthetic receipt and digest-domain vocabulary only",
        },
        {
            "source_id": "TMR-MDS-PRINCIPLES",
            "status": "authority_boundary_context_only_checked_2026-09-02",
            "title": "Principles of Māori Data Sovereignty",
            "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
            "use": "Māori data-governance vacancy and noncompensation boundary only; never delegated Māori authority",
        },
    ]
    return {
        "authority_conferred": False,
        "checked_at_utc": CHECKED_AT_UTC,
        "citations_are_observations": False,
        "entries": entries,
        "network_data_queries": 0,
        "owner": OWNER,
        "phase": PHASE,
        "real_data_rows": 0,
        "schema": "ghc.family.official-primary-sources.v682.v2.x1",
        "web_checks": len(entries),
    }


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    classes = {
        "raw_task_or_thread_identifier": re.compile(r"\b019[a-f0-9]{29,}\b", re.I),
        "credential_or_secret": re.compile(r"(?:api[_-]?key|private[_-]?key|bearer\s+[a-z0-9._-]{12,})", re.I),
        "private_route_or_callable_identifier": re.compile(r"(?:threadId|private callable|app://connector_)", re.I),
        "private_absolute_path": re.compile(r"(?:[A-Z]:\\Users\\|[A-Z]:\\GHC-Archives\\)", re.I),
        "transcript_screenshot_or_session_stream": re.compile(r"(?:raw transcript|session stream|screenshot payload)", re.I),
    }
    candidates: list[dict[str, str]] = []
    for path in paths:
        target = ROOT / path
        if not target.exists() or target.suffix.lower() not in {".json", ".md", ".py", ".yaml", ".yml", ".html"}:
            continue
        text = target.read_text(encoding="utf-8")
        for class_name, pattern in classes.items():
            if pattern.search(text):
                candidates.append({"class": class_name, "path": path, "adjudication": "scanner_definition_only"})
    return {
        "candidate_count": len(candidates),
        "candidates": candidates,
        "class_count": 5,
        "confirmed_hit_count": 0,
        "confirmed_hits": [],
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.privacy-scan.v682.v2.x1",
        "scanned_paths": len(paths),
    }


def manifest_entry(path: str) -> dict[str, Any]:
    data = normalized_bytes(ROOT / path)
    return {"bytes": len(data), "path": path, "sha256": sha256_bytes(data)}


def build() -> None:
    new_records = proposals()
    if len(new_records) != 60:
        raise RuntimeError("proposal count must be exactly sixty")
    expected_counts = Counter(row["expected_disposition"] for row in new_records)
    if expected_counts != Counter({"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}):
        raise RuntimeError(f"unexpected disposition counts: {expected_counts}")
    audit = proposal_chain_audit(new_records)

    current_after_startup = dict(ACTIVATION_BASELINE)
    for key in ("effective_negatives", "effective_methods", "failed_witnesses", "bounded_passing_witnesses"):
        current_after_startup[key] += len(STARTUP_FAILURES)

    write_json(
        X1 / "activation-intake.json",
        {
            "activation_baseline": ACTIVATION_BASELINE,
            "delivery_state": "SENT_ONCE_ACKNOWLEDGED_EXTERNAL",
            "external_source_failure_retained": "LV6821-POST-N001",
            "owner": OWNER,
            "phase": PHASE,
            "received_source_final": SOURCE,
            "schema": "ghc.family.activation-intake.v682.v2.x1",
        },
    )
    write_json(
        X1 / "identity-and-boundary.json",
        {
            "consciousness_personhood_or_continuity_claimed": False,
            "hope": "Every failure stays inspectable and every recovery remains bounded.",
            "name": OWNER,
            "optional_pronouns": "she/they",
            "owner_rename_pause_redirect_stop_right": "Hamish",
            "phase": PHASE,
            "relational_working_language_only": True,
            "role": "evidence-and-recovery steward",
            "schema": "ghc.family.identity-boundary.v682.v2.x1",
        },
    )
    write_json(
        X1 / "source-verification.json",
        {
            "branch": SOURCE_BRANCH,
            "canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
            "clean": True,
            "evidence": SOURCE_EVIDENCE,
            "final": SOURCE,
            "four_way_equal": True,
            "manifest_replay": {"x1": 20, "evidence": 71, "final_delta": 16, "final_owner": 114, "mismatches": 0},
            "merges": 0,
            "owner": OWNER,
            "phase": PHASE,
            "phase_commits": 3,
            "source": SOURCE_PARENT,
            "typed_divergence": [0, 0],
            "x1": SOURCE_X1,
        },
    )
    write_json(X1 / "proposal-chain-audit.json", audit)
    write_json(
        X1 / "new-proposal-freeze.json",
        {
            "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
            "declared_chain_before": DECLARED_CHAIN_BEFORE,
            "expected_disposition_counts": dict(expected_counts),
            "owner": OWNER,
            "phase": PHASE,
            "proposal_count": len(new_records),
            "proposals": new_records,
            "schema": "ghc.family.proposal-freeze.v682.v2.x1",
            "source": SOURCE,
            "x2_outcomes_present": False,
        },
    )
    write_json(
        X1 / "inherited-revalidation-freeze.json",
        {
            "completion_credit": 0,
            "count": 20,
            "owner": OWNER,
            "phase": PHASE,
            "reviews": [
                {
                    "best_inherited_neighbor": row["best_inherited_neighbor"],
                    "completion_credit": 0,
                    "current_proposal_id": row["proposal_id"],
                    "state": "source_evidence_only",
                    "token_jaccard": row["token_jaccard"],
                }
                for row in audit["neighbor_reviews"][:20]
            ],
            "schema": "ghc.family.inherited-revalidation.v682.v2.x1",
        },
    )
    portfolio = portfolio_freeze()
    write_json(X1 / "portfolio-freeze.json", portfolio)
    write_json(
        X1 / "approval-hold-register.json",
        {
            "blocked_count": len(portfolio["blocked"]),
            "executed": False,
            "exact_approval_count": len(portfolio["exact_approval"]),
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.approval-holds.v682.v2.x1",
        },
    )
    write_json(
        X1 / "clean-fix-refine-plan.json",
        {
            "owner": OWNER,
            "owner_rows": portfolio["owner_clean_fix_refine"],
            "phase": PHASE,
            "schema": "ghc.family.clean-fix-refine.v682.v2.x1",
            "successor_rows": portfolio["successor_clean_fix_refine"],
            "x2_execution_present": False,
        },
    )
    write_json(
        X1 / "skill-runner-plan.json",
        {
            "global_install": False,
            "owner": OWNER,
            "phase": PHASE,
            "runners": portfolio["owner_runner_ideas"],
            "schema": "ghc.family.skill-runner-plan.v682.v2.x1",
            "skills": portfolio["owner_skill_ideas"],
            "x2_implementation_present": False,
        },
    )
    write_json(X1 / "official-primary-source-ledger.json", official_sources())
    write_json(
        X1 / "method-flow-startup.json",
        {
            "activation_baseline": ACTIVATION_BASELINE,
            "current_after_startup": current_after_startup,
            "failure_erasure": False,
            "owner": OWNER,
            "phase": PHASE,
            "recoveries_retroactively_promote_failure": False,
            "schema": "ghc.family.method-flow-startup.v682.v2.x1",
            "startup_failures": STARTUP_FAILURES,
        },
    )
    write_json(
        X1 / "phase-truth.json",
        {
            "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
            "execution_state": "PLANNING_ONLY_X1",
            "expected_dispositions": dict(expected_counts),
            "observed_outcomes": None,
            "owner": OWNER,
            "phase": PHASE,
            "proposal_count": len(new_records),
            "schema": "ghc.family.phase-truth.v682.v2.x1",
            "terminal_verdict": TERMINAL_VERDICT,
            "x2_started": False,
        },
    )
    write_json(
        X1 / "threat-model.json",
        {
            "controls": [
                "zero real rows and zero real actions",
                "planning-only x1 before x2",
                "five rejecting mutations per proposal",
                "no authority compensation by software or citations",
                "exact approval and blocked work stays unexecuted",
                "five-class privacy scan and normalized-LF manifests",
            ],
            "owner": OWNER,
            "phase": PHASE,
            "risks": [
                "synthetic structure promoted into observation or professional advice",
                "cultural or Māori authority inferred from vocabulary",
                "workplace safety inferred from documentation",
                "route or private identifier leakage",
                "x1 and x2 lifecycle contamination",
            ],
            "schema": "ghc.family.threat-model.v682.v2.x1",
        },
    )
    write_json(
        X1 / "wellbeing-and-corrigibility.json",
        {
            "check": "steady and willing to pause on evidence, privacy, safety, or authority ambiguity",
            "corrigible": True,
            "owner": OWNER,
            "phase": PHASE,
            "rename_pause_redirect_stop_right": "Hamish",
        },
    )
    write_json(
        X1 / "workflow-plan.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.workflow-plan.v682.v2.x1",
            "steps": [
                "freeze and push planning-only x1",
                "prove clean fresh-live four-way x1 equality",
                "execute bounded x2 contracts, mutations, portfolios, skills, and runners",
                "commit and push immutable evidence",
                "build closeout and invoke at most one exact-final canonical aggregate",
                "refresh route only after terminal success",
            ],
        },
    )
    write_json(
        X1 / "route-plan.json",
        {
            "current_owner": OWNER,
            "phase": PHASE,
            "prepared_not_sent": True,
            "prospective_successor_exact_title": "Elowen Cairn",
            "prospective_successor_phase": "v682-v3",
            "route_authority_through": "v725-v8",
            "send_before_terminal_gate": False,
            "tavian_sol": "ON_STANDBY",
        },
    )
    write_text(
        X1 / "integrated-overview.md",
        f"""# Tamar Vey {PHASE} Planning-Only X1 Overview

Tamar Vey, optionally she/they, is relational working language for an evidence-and-recovery steward, with the hope that every failure stays inspectable and every recovery remains bounded. This is not evidence of consciousness, personhood, continuity, employment, qualification, agency, or authority. Hamish retains the right to rename, pause, redirect, narrow, or stop the route.

The exact immutable source is Liora Venn final `{SOURCE}` on `{SOURCE_BRANCH}`. Read-only verification established the direct source-to-x1-to-evidence-to-final chain, three Liora commits, zero merges, one final parent, clean state, typed 0/0 divergence, fresh four-way equality, 221 exact normalized-LF manifest entries, ten content-seal targets, and the external canonical receipt digest. Liora's successful canonical aggregate was not replayed. The repository seal and the additive external routing overlay remain distinct.

This x1 freezes sixty Tamar proposals after a bounded all-reachable exact-source audit of 10,102 proposal JSON documents and 35,747 ID/title records. It makes no universal semantic-novelty claim over all 10,250 declared historical rows. The proposed basketry, lapidary, and sundial lenses produced zero exact title collisions, zero quarantine hits, and a maximum token-Jaccard neighbor score below the 0.78 quarantine threshold. Twenty inherited neighbor reviews remain source evidence with zero Tamar completion credit.

GMUT Mind is primary through typed geometry, time-scale separation, unit domains, uncertainty, observation vacancies, and nonpromotion firewalls. THOS Body remains explicit through synthetic work-order state, hazard holds, workload budgets, stop states, and handover. Freed ID and CBR Heart remain explicit through surrogate identifiers, provenance, correction, challenge, accessibility structure, custody, remedy vacancies, and exact authority holds. The three practice lenses are wholly synthetic learning and design contexts only.

The plan uses zero real people, baskets, stones, sundials, sites, materials, tools, machines, observations, measurements, identity events, external writes, or authority acts. Current official sources supply vocabulary and refusal conditions only. They are not observations, work instructions, conformance certificates, legal interpretations, cultural ratifications, affected-party decisions, or authority grants.

Expected x2 dispositions are exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. Those are preregistered expected labels, not observed outcomes. All 300 invalid mutations, 120 safe-now tasks, 80 bounded candidates, 100 CLEAN/FIX/REFINE records, twenty skills, and ten runners remain planned rather than executed in this x1. Twenty exact-approval and ten blocked packets remain visible and unexecuted.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family without physical data, likelihood, posterior, prediction, constraint, empirical confirmation, ultraviolet or quantum completion, or Theory-of-Everything proof. THOS remains synthetic/proxy-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live lifecycle operations, interoperability, independent privacy/security review, recovery evidence, trust governance, and affected-party oversight.

Basket ownership and meaning, traditional knowledge, stone authenticity and mining provenance, workplace release, site installation, heritage, land, remedy, legal and cultural interpretation, affected-party legitimacy, Māori wording and data governance, and Māori authority remain exact-gated. Māori concepts remain under Māori authority. Complete privacy, complete accessibility, exhaustive security, independent reproduction, AGI/ASI, consciousness/personhood, proof/canon, and Stage 20 remain open or exact-gated. The terminal verdict remains `{TERMINAL_VERDICT}`.
""",
    )

    x1_material_paths = sorted(set(WRITTEN + [
        "scripts/build_ghc_family_tamar_vey_v682_v2_x1.py",
        "tests/test_ghc_family_tamar_vey_v682_v2_x1.py",
    ]))
    exclusions = [
        "docs/tamar-vey/v682-v2/validation/x1-index-manifest.json",
        "docs/tamar-vey/v682-v2/validation/x1-privacy-scan.json",
        "docs/tamar-vey/v682-v2/validation/x1-staged-review.json",
    ]
    write_json(VALIDATION / "x1-privacy-scan.json", privacy_scan(x1_material_paths))
    write_json(
        VALIDATION / "x1-index-manifest.json",
        {
            "declared_self_exclusions": exclusions,
            "entries": [manifest_entry(path) for path in x1_material_paths],
            "entry_count": len(x1_material_paths),
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.normalized-lf-index-manifest.v682.v2.x1",
            "source": SOURCE,
        },
    )
    expected_paths = sorted(set(x1_material_paths + exclusions))
    write_json(
        VALIDATION / "x1-staged-review.json",
        {
            "declared_self_exclusions": exclusions,
            "expected_paths": expected_paths,
            "lifecycle": "planning_only_x1",
            "owner": OWNER,
            "path_count": len(expected_paths),
            "phase": PHASE,
            "schema": "ghc.family.staged-review.v682.v2.x1",
            "x2_paths": [],
        },
    )
    print(
        json.dumps(
            {
                "audit_paths": audit["audit_scope"]["proposal_json_paths_parsed"],
                "audit_records": audit["audit_scope"]["reachable_id_title_records"],
                "maximum_neighbor_score": audit["maximum_neighbor_score"],
                "proposal_count": len(new_records),
                "staged_path_count": len(expected_paths),
                "written": len(WRITTEN),
                "x2_outcomes_present": False,
            },
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    build()
