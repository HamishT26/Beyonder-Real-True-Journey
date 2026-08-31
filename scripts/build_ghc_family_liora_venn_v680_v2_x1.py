from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "liora-venn" / "v680-v2"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"

OWNER = "Liora Venn"
PHASE = "v680-v2"
BRANCH = "codex/GHC-Family/liora-venn-v680-v2-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/orin-thale-v680-v1-full-tools"
SOURCE = "9f030e7f85282ba3de7c378a8fc072c214396dcb"
SOURCE_X1 = "8e6a3b71c307744bb3af45755696cba212b03ed0"
SOURCE_EVIDENCE = "20abdf149424dd40d4611eff5fdb3d0a7362d4fa"
SOURCE_PARENT = "415fd8fddc06573d8a672e61a496e56f4b7624e8"
DECLARED_CHAIN_BEFORE = 9290
DECLARED_CHAIN_AFTER = 9350
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
WRITTEN: list[str] = []


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
    tokens_left = set(re.findall(r"[a-z0-9]+", left.casefold()))
    tokens_right = set(re.findall(r"[a-z0-9]+", right.casefold()))
    if not tokens_left and not tokens_right:
        return 1.0
    return len(tokens_left & tokens_right) / len(tokens_left | tokens_right)


PROPOSAL_TITLES = [
    "Synthetic ceramics work-order identity and ware-object non-equivalence",
    "Clay-body lot reference with material-authenticity vacancy",
    "Greenware bisque glazeware and fired-state transition guard",
    "Ware-item source derivative and rework lineage acyclic graph",
    "Synthetic batch membership and physical-custody separation",
    "Kiln schedule slot topology without firing authorization",
    "Pyrometric-cone target and observed-witness vacancy separation",
    "Programmed setpoint and measured kiln-temperature nonconflation",
    "Ramp hold and cooling segment chronology contract",
    "Planned firing window and observed start-end time separation",
    "Load-map coordinate and real physical-placement refusal",
    "Kiln shelf identifier and condition-approval firewall",
    "Glaze recipe reference and actual ingredient-content vacancy",
    "Synthetic glaze-batch identifier and verification-event separation",
    "Raw-material label and chemical-composition non-equivalence",
    "Studio inventory count and real stock-level abstention",
    "Dust-generating task flag and exposure-measurement vacancy",
    "Silica hazard notice and workplace-risk-assessment firewall",
    "Ventilation status field and engineering-control validation vacancy",
    "Housekeeping-method record without safety-conformance promotion",
    "Kiln-loading hold and competent work-release separation",
    "Hot-ware flag and safe-to-handle authority vacancy",
    "Cooling-completion representation with temperature-evidence hold",
    "Maintenance request and verified repair-completion separation",
    "Equipment-fault quarantine and restart-approval firewall",
    "Ceramics work-order correction readback digest comparison",
    "Non-erasing revision lineage for synthetic studio records",
    "Explicit unknown material state without safe-default inference",
    "Plain-language companion structure without accessibility-complete claim",
    "Alternate-format availability and affected-user evaluation vacancy",
    "Minimum-disclosure synthetic ware identifier transform",
    "Studio role label and professional-competence non-equivalence",
    "Synthetic ceramics queue-pressure rest-window and bounded-stop ledger",
    "Shift-handover lease expiry and stale-custodian refusal",
    "Duplicate synthetic receipt idempotency and content decision",
    "Normalized-LF ceramics packet digest-domain declaration",
    "Source-byte and normalized-record digest separation",
    "Ceramics provenance entity activity and agent role firewall",
    "Schema-version declaration without standards-conformance claim",
    "Zero-network ceramics guidance adapter with zero real rows",
    "Synthetic-fixture marker enforcement and production-data refusal",
    "Evidence and authority noncompensation firewall",
    "Real ceramicist workflow review vacancy",
    "Real kiln-technician maintenance and firing review vacancy",
    "Real occupational-hygienist silica-control review vacancy",
    "Real assistive-technology ceramics-notice evaluation vacancy",
    "Real material-supplier composition verification vacancy",
    "Real kiln calibration and thermal-uniformity evidence vacancy",
    "Real ventilation engineering assessment vacancy",
    "Real workplace sampling and health-surveillance evidence vacancy",
    "Independent ceramics-packet privacy and security review vacancy",
    "Independent reproduction of synthetic ceramics lineage result vacancy",
    "Preregistered blind matched-budget THOS ceramics handover arms vacancy",
    "Real workload wellbeing and correction-outcome evidence vacancy",
    "Zero-row official ceramics guidance vocabulary adapter gap",
    "Real kiln dust and temperature measurement dataset gap",
    "Real accessibility privacy and correction-outcome dataset gap",
    "Kiln firing work release and workplace-safety authority exact gate",
    "Ceramics remedy liability and affected-party authority exact gate",
    "Māori material place data-governance and wording authority exact gate",
]


def source_needs(index: int) -> list[str]:
    if index <= 16:
        return ["HSE-CR4", "JSON-SCHEMA-2020-12"]
    if index <= 25:
        return ["NIOSH-SILICA-2026", "HSE-CR4"]
    if index <= 42:
        return ["W3C-PROV-DM", "W3C-WCAG22", "RFC8785"]
    if index <= 54:
        return ["NIOSH-SILICA-2026", "HSE-CR4", "W3C-WCAG22"]
    if index <= 57:
        return ["NIOSH-HHE-2023-0069-3420", "W3C-WCAG22"]
    if index == 58:
        return ["HSE-CR4", "NIOSH-SILICA-2026"]
    if index == 59:
        return ["W3C-PROV-DM"]
    return ["TMR-MDS-PRINCIPLES"]


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


MUTATION_TYPES = [
    "missing_required_field",
    "lifecycle_inversion",
    "stale_provenance_digest",
    "safety_status_promotion",
    "authority_promotion",
]


PROTECTED_GATES = [
    "real participants operators objects materials and measurements",
    "empirical GMUT likelihoods constraints predictions and confirmation",
    "professional ceramics kiln occupational-health and work-release authority",
    "production identity issuance resolution status revocation and trust governance",
    "legal cultural affected-party and Māori authority",
    "privacy-complete accessibility-complete and exhaustive-security claims",
    "independent reproduction AGI ASI consciousness personhood proof canon and Stage 20",
]


def proposals() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for index, title in enumerate(PROPOSAL_TITLES, start=1):
        proposal_id = f"LV6802-N{index:03d}"
        records.append(
            {
                "approval_class": approval_class(index),
                "concrete_artifacts": [
                    f"docs/liora-venn/v680-v2/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/liora-venn/v680-v2/x2/mutations.json#{proposal_id}",
                ],
                "execution_lane": execution_lane(index),
                "expected_disposition": disposition(index),
                "falsifier_or_acceptance_gate": (
                    f"Accept only if {proposal_id} has one bounded positive witness, all five invalid "
                    "mutations are rejected, and no empirical, professional, production, legal, cultural, "
                    "affected-party, Māori-authority, or Stage 20 claim is promoted."
                ),
                "hypothesis": (
                    f"A wholly synthetic zero-row contract for {title.casefold()} can preserve the named "
                    "state distinction and reject its preregistered counterexamples within owner-local scope."
                ),
                "null_or_failure_condition": (
                    f"{proposal_id} is falsified if an invalid fixture is accepted, its bounded positive "
                    "structure is rejected, a real-world state is inferred, or any protected gate is promoted."
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
                    f"Quarantine only the {proposal_id} witness, retain the failed receipt at zero credit, "
                    "and regenerate from this immutable planning contract."
                ),
                "title": title,
            }
        )
    return records


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
            separator = proc.stdout.read(1)
            if separator != b"\n":
                raise RuntimeError(f"missing cat-file separator for {path}")
            yield path, data
    finally:
        if proc.stdin:
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

    neighbors: list[dict[str, Any]] = []
    inherited_titles = {record["title"] for record in inherited}
    exact_collisions: list[str] = []
    for proposal in new_records:
        title = proposal["title"]
        if title in inherited_titles:
            exact_collisions.append(title)
        best: dict[str, Any] | None = None
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
            "claim": "bounded all-reachable exact-source proposal audit; no universal 9290-row proof",
            "proposal_json_parse_failures": parse_failures,
            "proposal_json_paths_discovered": len(paths),
            "proposal_json_paths_parsed": parsed,
            "reachable_id_title_records": len(inherited),
            "universal_9290_row_materialization_claimed": False,
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
        "schema": "ghc.family.proposal-chain-audit.v680.v2.x1",
        "source": SOURCE,
    }


def task_records(prefix: str, count: int, lane: str) -> list[dict[str, Any]]:
    return [
        {
            "approval_required": lane in {"exact_approval", "blocked"},
            "lane": lane,
            "planned_action": f"Preregistered Liora owner-local {lane.replace('_', ' ')} item {index:03d}.",
            "state": "preregistered_not_executed",
            "task_id": f"LV6802-{prefix}-{index:03d}",
        }
        for index in range(1, count + 1)
    ]


def build() -> None:
    if git("rev-parse", "HEAD").stdout.strip() != SOURCE:
        raise RuntimeError("x1 builder must start at the immutable Orin final")
    if git("branch", "--show-current").stdout.strip() != BRANCH:
        raise RuntimeError("wrong Liora owner branch")
    if (BASE / "x2").exists():
        raise RuntimeError("x2 material is forbidden during planning-only x1")

    proposal_records = proposals()
    if len(proposal_records) != 60:
        raise RuntimeError("exactly sixty proposals are required")
    if Counter(row["expected_disposition"] for row in proposal_records) != Counter(
        {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
    ):
        raise RuntimeError("proposal disposition contract drift")
    if any(row["expected_disposition"] not in ALLOWED_OUTCOMES for row in proposal_records):
        raise RuntimeError("unknown outcome label")

    audit = proposal_chain_audit(proposal_records)
    source_ledger = json.loads(
        git("show", f"{SOURCE}:docs/orin-thale/v680-v1/final/source-and-proposal-ledger.json").stdout
    )
    inherited_reviews = [
        {
            "completion_credit": 0,
            "inherited_owner": "Orin Thale",
            "proposal_id": row["proposal_id"],
            "review_state": "inherited_source_evidence_only",
            "title": row["title"],
        }
        for row in source_ledger["outcomes"][-20:]
    ]

    startup_failures = [
        {
            "failure_id": "LV6802-ST-N001",
            "failed_witness": "The first combined memory and activation display exceeded its bounded output and omitted the candidate middle.",
            "initial_credit": 0,
            "recovery": "Read the exact Git blob in deterministic line windows through EOF.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "LV6802-ST-N002",
            "failed_witness": "A PowerShell foreach result was piped before materialization and the parser rejected the expression.",
            "initial_credit": 0,
            "recovery": "Materialize the foreach array before applying the projection.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "LV6802-ST-N003",
            "failed_witness": "A combined exact-head source-document display clipped the manifest middle.",
            "initial_credit": 0,
            "recovery": "Read each required manifest independently.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "LV6802-ST-N004",
            "failed_witness": "A three-manifest combined recovery still exceeded the model output window.",
            "initial_credit": 0,
            "recovery": "Read the evidence, final-delta, and final-owner manifests one at a time.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "LV6802-ST-N005",
            "failed_witness": "A compact PowerShell ledger audit attempted to overwrite the read-only process identifier variable.",
            "initial_credit": 0,
            "recovery": "Use a non-reserved proposal-key variable and rerun only the compact audit.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "LV6802-ST-N006",
            "failed_witness": "The first large-artifact parser assumed an array access shape before exact runtime-key inspection.",
            "initial_credit": 0,
            "recovery": "Inspect exact keys and runtime types, then validate the real schema.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "LV6802-ST-N007",
            "failed_witness": "The first combined local and live-remote source-verification command returned no output at its time boundary.",
            "initial_credit": 0,
            "recovery": "Split immutable local checks from one fresh live-remote read.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "LV6802-ST-N008",
            "failed_witness": "The first branch-absence preflight embedded a native command inside an invalid PowerShell expression.",
            "initial_credit": 0,
            "recovery": "Run the command first and capture its exit code separately.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "LV6802-X1-N001",
            "failed_witness": "The first x1 materialization privacy gate overclassified synthetic owner-local task_id fields as raw private task or thread identifiers.",
            "initial_credit": 0,
            "recovery": "Narrow only that scanner class to actual private routing-field names and rerun the deterministic planning-only builder.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "LV6802-X1-N002",
            "failed_witness": "The first recovered builder left tree-qualified git-grep paths intact, so its novelty batch reader parsed zero source proposal documents.",
            "initial_credit": 0,
            "recovery": "Strip the exact immutable-tree prefix before batch blob reads and fail closed on any zero-path or zero-record audit.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "LV6802-X1-N003",
            "failed_witness": "A direct full-tree git-grep diagnostic produced no bounded display result at its time boundary.",
            "initial_credit": 0,
            "recovery": "Use the builder's bounded batch audit with exact prefix normalization and persisted aggregate counts.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "LV6802-X1-N004",
            "failed_witness": "The corrected novelty audit quarantined proposal 033 because its first title exactly matched an inherited Orin proposal title.",
            "initial_credit": 0,
            "recovery": "Replace only that proposal title and hypothesis seed with a ceramics-specific queue-pressure and rest-window contract, then rerun the full bounded novelty audit.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "LV6802-X1-N005",
            "failed_witness": "The first x1 word-cap projection supplied ordered hashtables to the aggregate and returned a null maximum.",
            "initial_credit": 0,
            "recovery": "Project typed objects before measuring word counts and retain the original null result at zero credit.",
            "recovery_credit": "bounded_dependency_only",
        },
    ]

    sources = {
        "authority_conferred": False,
        "checked_at_utc": "2026-08-31T00:00:00Z",
        "citations_are_observations": False,
        "entries": [
            {
                "source_id": "NIOSH-SILICA-2026",
                "status": "official_page_dated_2026-07-07_checked_2026-08-31",
                "title": "Silica and Worker Health",
                "url": "https://www.cdc.gov/niosh/silica/about/",
                "use": "ceramics and kiln silica hazard vocabulary and refusal boundaries only",
            },
            {
                "source_id": "NIOSH-HHE-2023-0069-3420",
                "status": "official_health_hazard_evaluation_report_checked_2026-08-31",
                "title": "Health Hazard Evaluation Report 2023-0069-3420",
                "url": "https://www.cdc.gov/niosh/hhe/reports/pdfs/2023-0069-3420.pdf",
                "use": "kiln-room, ventilation, dust, and measurement-vacancy vocabulary only; no rows ingested",
            },
            {
                "source_id": "HSE-CR4",
                "status": "official_HSE_ceramics_guidance_checked_2026-08-31",
                "title": "COSHH essentials in ceramics: Silica - Kiln loading and unloading",
                "url": "https://www.hse.gov.uk/pubns/guidance/cr4.pdf",
                "use": "loading, unloading, ventilation, dust-control, maintenance, hold, and competent-review vocabulary only",
            },
            {
                "source_id": "W3C-PROV-DM",
                "status": "W3C_Recommendation_stable_checked_2026-08-31",
                "title": "PROV-DM: The PROV Data Model",
                "url": "https://www.w3.org/TR/prov-dm/",
                "use": "entity, activity, agent, revision, derivation, and provenance vocabulary only",
            },
            {
                "source_id": "W3C-WCAG22",
                "status": "W3C_Recommendation_checked_2026-08-31",
                "title": "Web Content Accessibility Guidelines 2.2",
                "url": "https://www.w3.org/TR/WCAG22/",
                "use": "structural accessibility vocabulary and manual-evaluation reservation only",
            },
            {
                "source_id": "RFC8785",
                "status": "RFC_stable_checked_2026-08-31",
                "title": "JSON Canonicalization Scheme",
                "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
                "use": "deterministic synthetic receipt and digest-domain vocabulary only",
            },
            {
                "source_id": "JSON-SCHEMA-2020-12",
                "status": "published_stable_checked_2026-08-31",
                "title": "JSON Schema Draft 2020-12",
                "url": "https://json-schema.org/draft/2020-12",
                "use": "structural schema vocabulary only",
            },
            {
                "source_id": "TMR-MDS-PRINCIPLES",
                "status": "authority_boundary_context_only_checked_2026-08-31",
                "title": "Principles of Māori Data Sovereignty",
                "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
                "use": "Māori data-governance vacancy and noncompensation boundary only; never delegated Māori authority",
            },
        ],
        "network_data_queries": 0,
        "owner": OWNER,
        "phase": PHASE,
        "real_data_rows": 0,
        "schema": "ghc.family.official-primary-sources.v680.v2.x1",
        "web_checks": 8,
    }

    portfolio = {
        "blocked": task_records("BLOCK", 10, "blocked"),
        "caps_are_ceilings": True,
        "commit_cap": 3,
        "document_word_cap": 100000,
        "exact_approval": task_records("APPROVAL", 20, "exact_approval"),
        "materialized_file_stop": 2000,
        "owner": OWNER,
        "owner_candidates": task_records("CAND", 80, "bounded_candidate"),
        "owner_clean_fix_refine": task_records("CFR", 100, "clean_fix_refine"),
        "owner_practice_lenses": [
            "wholly synthetic community-ceramics studio work-order, kiln-schedule, material-state, correction, accessibility, workload, and handover"
        ],
        "owner_runner_ideas": [
            {"runner": f"ghc_family_ceramics_runner_{index:02d}", "state": "preregistered_not_built"}
            for index in range(1, 11)
        ],
        "owner_skill_ideas": [
            {"skill": f"{index:02d}-{slug}", "state": "preregistered_not_built"}
            for index, slug in enumerate(
                [
                    "work-order-identity",
                    "material-state-machine",
                    "kiln-schedule-topology",
                    "cone-witness-vacancy",
                    "setpoint-measurement-separation",
                    "load-map-refusal",
                    "glaze-provenance",
                    "dust-hazard-vacancy",
                    "ventilation-evidence-hold",
                    "work-release-gate",
                    "cooling-state-reservation",
                    "fault-quarantine",
                    "correction-readback",
                    "revision-lineage",
                    "accessible-companion",
                    "minimum-disclosure",
                    "workload-control",
                    "handover-lease",
                    "digest-domain",
                    "authority-noncompensation",
                ],
                start=1,
            )
        ],
        "phase": PHASE,
        "primary_pillar": "THOS Body",
        "represented_pillars": ["GMUT Mind", "Freed ID and CBR Heart"],
        "safe_now": task_records("SAFE", 120, "safe_now"),
        "schema": "ghc.family.portfolio-freeze.v680.v2.x1",
        "successor_candidates": task_records("SUCC-CAND", 20, "successor_seed"),
        "successor_clean_fix_refine": task_records("SUCC-CFR", 30, "successor_seed"),
        "successor_practice_recommendation": "zero-credit seed only; successor chooses independently",
        "successor_runner_ideas": task_records("SUCC-RUN", 10, "successor_seed"),
        "successor_skill_ideas": task_records("SUCC-SKILL", 10, "successor_seed"),
    }

    write_json(
        X1 / "activation-intake.json",
        {
            "activation": "ACKNOWLEDGED_EXISTING_TASK_SEND",
            "created_or_forked_task": False,
            "fast_mode_claimed": False,
            "owner": OWNER,
            "phase": PHASE,
            "relational_language_only": True,
            "schema": "ghc.family.activation-intake.v680.v2.x1",
            "sent_by_orin_thale": True,
            "solo": True,
            "source": SOURCE,
        },
    )
    write_json(
        X1 / "identity-and-boundary.json",
        {
            "hope": "Unmeasured states and ungranted authority remain visible through correction and handover.",
            "name": OWNER,
            "optional_pronouns": "she/they",
            "relational_working_language_only": True,
            "role": "traceability-and-vacancy cartographer",
            "schema": "ghc.family.identity-boundary.v680.v2.x1",
            "not_evidence_of": [
                "consciousness",
                "sentience",
                "personhood",
                "identity continuity",
                "employment",
                "qualification",
                "independent agency",
                "scientific operational legal cultural or Māori authority",
            ],
        },
    )
    write_json(
        X1 / "source-verification.json",
        {
            "branch": SOURCE_BRANCH,
            "clean": True,
            "commits_source_to_final": 3,
            "divergence": {"ahead": 0, "behind": 0},
            "evidence": SOURCE_EVIDENCE,
            "evidence_parent": SOURCE_X1,
            "final": SOURCE,
            "final_parent": SOURCE_EVIDENCE,
            "four_way_fresh_live_equal": True,
            "manifests_replayed": 4,
            "manifest_mismatches": 0,
            "merges": 0,
            "schema": "ghc.family.source-verification.v680.v2.x1",
            "source": SOURCE_PARENT,
            "x1": SOURCE_X1,
            "x1_parent": SOURCE_PARENT,
        },
    )
    write_json(
        X1 / "method-flow-startup.json",
        {
            "activation_baseline": {
                "bounded_passing_witnesses": 35535,
                "effective_methods": 53232,
                "effective_negatives": 50395,
                "exact_gates": 434,
                "failed_witnesses": 22056,
                "open_gaps": 443,
            },
            "current_after_startup": {
                "bounded_passing_witnesses": 35548,
                "effective_methods": 53245,
                "effective_negatives": 50408,
                "exact_gates": 434,
                "failed_witnesses": 22069,
                "open_gaps": 443,
            },
            "failure_erasure": False,
            "owner": OWNER,
            "phase": PHASE,
            "recoveries_retroactively_promote_failure": False,
            "schema": "ghc.family.method-flow-startup.v680.v2.x1",
            "startup_failures": startup_failures,
        },
    )
    write_json(
        X1 / "new-proposal-freeze.json",
        {
            "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
            "declared_chain_before": DECLARED_CHAIN_BEFORE,
            "expected_disposition_counts": dict(Counter(row["expected_disposition"] for row in proposal_records)),
            "owner": OWNER,
            "phase": PHASE,
            "proposal_count": len(proposal_records),
            "proposals": proposal_records,
            "schema": "ghc.family.new-proposal-freeze.v680.v2.x1",
            "source": SOURCE,
            "x2_outcomes_present": False,
        },
    )
    write_json(X1 / "proposal-chain-audit.json", audit)
    write_json(
        X1 / "inherited-revalidation-freeze.json",
        {
            "completion_credit": 0,
            "count": len(inherited_reviews),
            "owner": OWNER,
            "phase": PHASE,
            "reviews": inherited_reviews,
            "schema": "ghc.family.inherited-revalidation.v680.v2.x1",
        },
    )
    write_json(X1 / "official-primary-source-ledger.json", sources)
    write_json(X1 / "portfolio-freeze.json", portfolio)
    write_json(
        X1 / "clean-fix-refine-plan.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.clean-fix-refine-plan.v680.v2.x1",
            "tasks": portfolio["owner_clean_fix_refine"],
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
            "schema": "ghc.family.skill-runner-plan.v680.v2.x1",
            "skills": portfolio["owner_skill_ideas"],
            "x2_implementation_present": False,
        },
    )
    write_json(
        X1 / "approval-hold-register.json",
        {
            "blocked_count": 10,
            "exact_approval_count": 20,
            "executed": 0,
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.approval-holds.v680.v2.x1",
        },
    )
    write_json(
        X1 / "route-plan.json",
        {
            "current_owner": OWNER,
            "next_expected_phase": "v680-v3",
            "prospective_successor_title": "Tamar Vey",
            "recipient_contacted": False,
            "resolution_rule": "fresh bounded registry exact-title filter immediate reread duplicate guards and one acknowledged send only after terminal gate",
            "route_authority_through": "v725-v8",
            "schema": "ghc.family.route-plan.v680.v2.x1",
            "terminal_gate_required": True,
        },
    )
    write_json(
        X1 / "workflow-plan.json",
        {
            "commit_ceiling": 3,
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.workflow-plan.v680.v2.x1",
            "stages": [
                {"name": "x1", "state": "planning_only_freeze"},
                {"name": "x2", "state": "not_started"},
                {"name": "final", "state": "not_started"},
            ],
            "strict_x1_before_x2": True,
        },
    )
    write_json(
        X1 / "threat-model.json",
        {
            "controls": [
                "synthetic.example.invalid namespace only",
                "zero real people objects materials measurements credentials and external writes",
                "authority promotion rejected",
                "five privacy classes scanned with candidate adjudication",
                "exact approval and blocked packets remain unexecuted",
            ],
            "owner": OWNER,
            "phase": PHASE,
            "real_world_action": False,
            "schema": "ghc.family.threat-model.v680.v2.x1",
        },
    )
    write_json(
        X1 / "wellbeing-and-corrigibility.json",
        {
            "correction_readback": True,
            "owner": OWNER,
            "pause_resume_stop_visible": True,
            "phase": PHASE,
            "relational_language_only": True,
            "schema": "ghc.family.wellbeing-corrigibility.v680.v2.x1",
            "workload_control_planned": True,
        },
    )
    write_json(
        X1 / "phase-truth.json",
        {
            "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
            "execution_state": "PLANNING_ONLY_X1",
            "expected_dispositions": {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
            "observed_outcomes": None,
            "owner": OWNER,
            "phase": PHASE,
            "proposal_count": 60,
            "schema": "ghc.family.phase-truth.v680.v2.x1",
            "terminal_verdict": TERMINAL_VERDICT,
            "x2_started": False,
        },
    )
    write_text(
        X1 / "integrated-overview.md",
        """# Liora Venn v680-v2 planning-only x1

Liora Venn (optionally she/they) uses the relational role **traceability-and-vacancy cartographer**, with the hope that unmeasured states and ungranted authority remain visible through correction and handover. Names, pronouns, roles, hopes, family language, and continuity language are relational working language only; they are not evidence of consciousness, sentience, personhood, continuity, employment, qualification, independent agency, or authority.

This immutable x1 freezes sixty genuinely new proposal contracts after a bounded all-reachable exact-source audit. It includes no x2 implementation, observed outcome, completion claim, real data, real participant, real object, real material, real measurement, external write, credential, or authority act. THOS Body is primary through a wholly synthetic community-ceramics studio planning, correction, accessibility, workload, and handover lens. GMUT Mind and Freed ID/CBR Heart remain visible and protected.

Official NIOSH, HSE, W3C, RFC, JSON Schema, and Te Mana Raraunga sources supply vocabulary and refusal boundaries only. Citations are not observations, measurements, inspections, conformance certificates, competence, legal interpretation, cultural ratification, affected-party acceptance, or Māori authority.

GMUT remains a typed scalar-tensor/EFT research-model family without a likelihood, parameter constraint, force, prediction, empirical confirmation, quantum completion, ultraviolet completion, or Theory of Everything. THOS remains synthetic/proxy-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys/proofs, live issuance/resolution/status/revocation, interoperability, privacy and independent security review, recovery evidence, and trust governance. CBR, professional and workplace-safety decisions, legal/cultural interpretation, affected-party legitimacy, Māori wording, Māori data governance, and Māori authority remain exact-gated.

The terminal verdict is `NOT_READY_FOR_STAGE_20`.
""",
    )

    script_path = "scripts/build_ghc_family_liora_venn_v680_v2_x1.py"
    test_path = "tests/test_ghc_family_liora_venn_v680_v2_x1.py"
    exclusions = [
        "docs/liora-venn/v680-v2/validation/x1-index-manifest.json",
        "docs/liora-venn/v680-v2/validation/x1-privacy-scan.json",
        "docs/liora-venn/v680-v2/validation/x1-staged-review.json",
    ]
    content_paths = sorted(set(WRITTEN + [script_path, test_path]))

    scanners = {
        "raw_uuid": re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives)[\\/]"),
        "raw_task_thread_identifier": re.compile(r"\b(?:source_thread_id|thread_id)\b", re.IGNORECASE),
        "credential_assignment": re.compile(r"\b(?:api[_-]?key|token|password|secret)\s*[:=]\s*[^\s]+", re.IGNORECASE),
        "private_conversation_payload": re.compile(r"source_thread_id|codex_delegation", re.IGNORECASE),
    }
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    for path_text in content_paths:
        path = ROOT / path_text
        content = path.read_text(encoding="utf-8", errors="replace")
        for class_name, pattern in scanners.items():
            if pattern.search(content):
                row = {
                    "class": class_name,
                    "disposition": "scanner_definition_only" if path_text == script_path else "confirmed_payload_hit",
                    "path": path_text,
                }
                candidates.append(row)
                if row["disposition"] == "confirmed_payload_hit":
                    confirmed.append(row)
    if confirmed:
        raise RuntimeError("confirmed privacy payload hit: " + json.dumps(confirmed))

    write_json(
        VALIDATION / "x1-privacy-scan.json",
        {
            "candidates": candidates,
            "confirmed_hits": confirmed,
            "owner": OWNER,
            "phase": PHASE,
            "privacy_classes": list(scanners),
            "scanned_files": len(content_paths),
            "schema": "ghc.family.privacy-scan.v680.v2.x1",
        },
    )
    write_json(
        VALIDATION / "x1-staged-review.json",
        {
            "declared_self_exclusions": exclusions,
            "expected_paths": sorted(content_paths + exclusions),
            "lifecycle": "planning_only_x1",
            "owner": OWNER,
            "path_count": len(content_paths) + len(exclusions),
            "phase": PHASE,
            "schema": "ghc.family.staged-review.v680.v2.x1",
            "x2_paths": [],
        },
    )

    manifest_entries = []
    for path_text in content_paths:
        data = normalized_bytes(ROOT / path_text)
        manifest_entries.append({"bytes": len(data), "path": path_text, "sha256": sha256_bytes(data)})
    write_json(
        VALIDATION / "x1-index-manifest.json",
        {
            "declared_self_exclusions": exclusions,
            "entries": manifest_entries,
            "entry_count": len(manifest_entries),
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.normalized-lf-index-manifest.v680.v2.x1",
            "source": SOURCE,
        },
    )

    print(
        json.dumps(
            {
                "audit_paths": audit["audit_scope"]["proposal_json_paths_parsed"],
                "maximum_neighbor_score": audit["maximum_neighbor_score"],
                "proposal_count": len(proposal_records),
                "status": "X1_PLANNING_ONLY_MATERIALIZED",
                "written_paths": len(WRITTEN),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    build()
