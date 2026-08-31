from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "tamar-vey" / "v680-v3"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"

OWNER = "Tamar Vey"
PHASE = "v680-v3"
BRANCH = "codex/GHC-Family/tamar-vey-v680-v3-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/liora-venn-v680-v2-full-tools"
SOURCE = "c9f87c8fd5f3ba0f0265799664fd868454ab41ff"
SOURCE_X1 = "04b3248d8fc62d7f81303eec1d452d6078586db3"
SOURCE_EVIDENCE = "26db158bb8574ab2996ef87bae3ed8e89c2ce9e9"
SOURCE_PARENT = "9f030e7f85282ba3de7c378a8fc072c214396dcb"
DECLARED_CHAIN_BEFORE = 9350
DECLARED_CHAIN_AFTER = 9410
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
    "Synthetic stained-glass panel record and physical panel non-equivalence",
    "Glass-piece stable alias and real object identity vacancy",
    "Lead-came segment topology without fabrication authorization",
    "Copper-foil seam graph and soldered-joint evidence separation",
    "Cartoon-pattern revision lineage and cut-piece derivation contract",
    "Panel light-path geometry proxy without optical measurement",
    "Glass-colour descriptor and spectral-measurement nonconflation",
    "Came-channel width field and calibrated-dimension vacancy",
    "Support-bar placement plan and structural-adequacy firewall",
    "Border-came sequence and installed-edge refusal",
    "Synthetic solder-lot reference and alloy-composition vacancy",
    "Lead-handling hazard notice and exposure-assessment firewall",
    "Fume-extraction status field and engineering-control validation vacancy",
    "Flux-label reference and chemical-content abstention",
    "Panel-condition flag and conservation-treatment authority hold",
    "Packing-orientation record and real handling-release separation",
    "Glass-break quarantine and competent repair-decision vacancy",
    "Stained-glass work-order correction digest readback",
    "Non-erasing panel revision and custody lineage",
    "Stained-glass handover lease expiry and stale-custodian refusal",
    "Synthetic bicycle-wheel work-order and physical wheel non-equivalence",
    "Hub-shell alias and real component identity vacancy",
    "Rim-model label and manufacturer-specification evidence hold",
    "Spoke-count topology and installed-spoke inventory separation",
    "Lacing-pattern graph and assembly-authorization firewall",
    "Drive-side and non-drive-side role partition without measurement",
    "Wheel-dish target field and observed-centering vacancy",
    "Lateral-runout proxy and calibrated-indicator nonconflation",
    "Radial-runout proxy and physical-roundness abstention",
    "Spoke-tension target and tensiometer-reading separation",
    "Relative-tension vector and certified wheel-fitness firewall",
    "Nipple-turn placeholder and adjustment-authorization hold",
    "Rim-damage flag and competent replace-or-repair decision vacancy",
    "Brake-surface state and ride-release exact reservation",
    "Wheel custody chain and bicycle ownership non-equivalence",
    "Component-provenance braid and unknown-origin retention",
    "Correction readback for synthetic wheel-truing notes",
    "Wheel work-queue rest window and bounded-stop ledger",
    "Shift-handover lease for an unfinished wheel record",
    "Zero-call wheel-tension adapter with no instrument rows",
    "Synthetic seed-library accession and biological material non-equivalence",
    "Seed-packet alias and taxonomic-identity vacancy",
    "Declared cultivar label and varietal-authenticity firewall",
    "Accession acquisition event and ownership-right separation",
    "Donor-role label and affected-party consent vacancy",
    "Packet-lot membership and physical-custody nonconflation",
    "Quantity field and real inventory-count abstention",
    "Storage-location code and environmental-measurement vacancy",
    "Germination field and viability-test evidence hold",
    "Regeneration-plan status and planting-authorization firewall",
    "Distribution request and release-eligibility separation",
    "Quarantine flag and biosecurity-decision exact reservation",
    "Provenance derivation graph for synthetic seed-packet records",
    "Non-erasing correction lineage for seed-accession metadata",
    "Real stained-glass condition and lead-exposure dataset gap",
    "Real bicycle-wheel measurement and ride-safety review gap",
    "Zero-row FAO seed-vocabulary adapter open gap",
    "Seed distribution ownership and benefit-sharing exact authority gate",
    "Stained-glass lead-work safety and treatment exact authority gate",
    "Seed-library cultural governance reserved to tangata whenua iwi hapū and Māori authorities",
]


def source_needs(index: int) -> list[str]:
    if index <= 20:
        return ["CCI-CARE-CERAMICS-GLASS", "OSHA-LEAD", "W3C-PROV-DM"]
    if index <= 40:
        return ["PARKTOOL-WHEEL-TENSION", "W3C-PROV-DM", "RFC8785"]
    if index <= 54:
        return ["FAO-GENEBANK-STANDARDS", "W3C-VC-DM-2.0", "W3C-WCAG22"]
    if index <= 57:
        return ["CCI-CARE-CERAMICS-GLASS", "PARKTOOL-WHEEL-TENSION", "FAO-GENEBANK-STANDARDS"]
    if index == 58:
        return ["FAO-GENEBANK-STANDARDS", "W3C-VC-DM-2.0"]
    if index == 59:
        return ["CCI-CARE-CERAMICS-GLASS", "OSHA-LEAD"]
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
    "professional stained-glass bicycle seed-library safety treatment release and biosecurity authority",
    "production identity issuance resolution status revocation and trust governance",
    "legal cultural affected-party and Māori authority",
    "privacy-complete accessibility-complete and exhaustive-security claims",
    "independent reproduction AGI ASI consciousness personhood proof canon and Stage 20",
]


def proposals() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for index, title in enumerate(PROPOSAL_TITLES, start=1):
        proposal_id = f"TV6803-N{index:03d}"
        records.append(
            {
                "approval_class": approval_class(index),
                "concrete_artifacts": [
                    f"docs/tamar-vey/v680-v3/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/tamar-vey/v680-v3/x2/mutations.json#{proposal_id}",
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
            "claim": "bounded all-reachable exact-source proposal audit; no universal 9350-row proof",
            "proposal_json_parse_failures": parse_failures,
            "proposal_json_paths_discovered": len(paths),
            "proposal_json_paths_parsed": parsed,
            "reachable_id_title_records": len(inherited),
            "universal_9350_row_materialization_claimed": False,
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
        "schema": "ghc.family.proposal-chain-audit.v680.v3.x1",
        "source": SOURCE,
    }


def task_records(prefix: str, count: int, lane: str) -> list[dict[str, Any]]:
    return [
        {
            "approval_required": lane in {"exact_approval", "blocked"},
            "lane": lane,
            "planned_action": f"Preregistered Tamar owner-local {lane.replace('_', ' ')} item {index:03d}.",
            "state": "preregistered_not_executed",
            "task_id": f"TV6803-{prefix}-{index:03d}",
        }
        for index in range(1, count + 1)
    ]


def build() -> None:
    if git("rev-parse", "HEAD").stdout.strip() != SOURCE:
        raise RuntimeError("x1 builder must start at the immutable Liora final")
    if git("branch", "--show-current").stdout.strip() != BRANCH:
        raise RuntimeError("wrong Tamar owner branch")
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
        git("show", f"{SOURCE}:docs/liora-venn/v680-v2/x1/new-proposal-freeze.json").stdout
    )
    inherited_reviews = [
        {
            "completion_credit": 0,
            "inherited_owner": "Liora Venn",
            "proposal_id": row["proposal_id"],
            "review_state": "inherited_source_evidence_only",
            "title": row["title"],
        }
        for row in source_ledger["proposals"][-20:]
    ]

    startup_failures = [
        {
            "failure_id": "TV6803-ST-N001",
            "failed_witness": "The first combined Method Flow display exceeded its bounded output window.",
            "initial_credit": 0,
            "recovery": "Parse the full 149-kilobyte JSON locally and project only exact keys, counts, and method identifiers.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "TV6803-ST-N002",
            "failed_witness": "A PowerShell foreach result was piped before materialization and the parser rejected the expression.",
            "initial_credit": 0,
            "recovery": "Materialize the foreach array before applying the projection.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "TV6803-ST-N003",
            "failed_witness": "The full authorization current-state display exceeded its bounded output window.",
            "initial_credit": 0,
            "recovery": "Read the same exact file in bounded numbered chunks through EOF.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "TV6803-ST-N004",
            "failed_witness": "The first canonical-receipt projection assumed a checks property map and returned a false all-check result.",
            "initial_credit": 0,
            "recovery": "Inspect the receipt's actual keys, then project the real detailed, minimal, and test fields.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "TV6803-ST-N005",
            "failed_witness": "The absent Tamar remote branch returned no rows and the preflight wrapper called Trim on null.",
            "initial_credit": 0,
            "recovery": "Materialize zero returned rows explicitly and preserve absence as the expected branch-creation precondition.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "TV6803-ST-N006",
            "failed_witness": "The authorized worktree creation crossed its display boundary and the wrapper omitted the running session handle.",
            "initial_credit": 0,
            "recovery": "Do not rerun the mutation; inspect exact Git processes, locks, and the eventual registered worktree until quiescent.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "TV6803-ST-N007",
            "failed_witness": "A Wait-Process already-gone result collapsed into the wrapper's timeout catch.",
            "initial_credit": 0,
            "recovery": "Verify an exact zero process count and inspect the created branch and worktree directly.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "TV6803-ST-N008",
            "failed_witness": "The first worktree-registration comparison treated Git forward slashes and Windows backslashes as different paths.",
            "initial_credit": 0,
            "recovery": "Normalize only path separators and compare the exact registered absolute path.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "TV6803-X1-N001",
            "failed_witness": "The first planning-only materialization quarantined proposal 060 because its title had token Jaccard 0.833333 against an inherited Māori-authority title.",
            "initial_credit": 0,
            "recovery": "Change only proposal 060's title to a seed-library cultural-governance reservation with distinct wording, then rerun the complete bounded novelty audit.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "TV6803-X1-N002",
            "failed_witness": "The first staged-manifest replay diagnostic escaped CR and LF byte literals as textual backslash sequences and falsely reported two-byte mismatches in the builder and test.",
            "initial_credit": 0,
            "recovery": "Use actual CR and LF byte constants on one literal path per invocation; worktree and staged Git-blob bytes then matched exactly.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "TV6803-X1-N003",
            "failed_witness": "The first bounded byte-difference recovery had an unterminated Python string literal and exited before inspecting either file.",
            "initial_credit": 0,
            "recovery": "Remove the nested executable string and inspect one literal path per invocation with a short direct expression.",
            "recovery_credit": "bounded_dependency_only",
        },
    ]

    sources = {
        "authority_conferred": False,
        "checked_at_utc": "2026-08-31T00:00:00Z",
        "citations_are_observations": False,
        "entries": [
            {
                "source_id": "CCI-CARE-CERAMICS-GLASS",
                "status": "official_Canadian_Conservation_Institute_page_checked_2026-08-31",
                "title": "The Care and Preservation of Ceramics and Glass",
                "url": "https://www.canada.ca/en/conservation-institute/services/conservation-preservation-publications/canadian-conservation-institute-notes/care-ceramics-glass.html",
                "use": "glass condition, handling, storage, and professional-treatment vacancy vocabulary only",
            },
            {
                "source_id": "OSHA-LEAD",
                "status": "official_OSHA_lead_standard_primary_publication_checked_2026-08-31",
                "title": "Occupational Exposure to Lead",
                "url": "https://www.osha.gov/sites/default/files/laws-regs/federalregister/1978-11-14.pdf",
                "use": "lead-exposure and competent workplace-control refusal boundaries only; no exposure data ingested",
            },
            {
                "source_id": "PARKTOOL-WHEEL-TENSION",
                "status": "official_manufacturer_repair_vocabulary_page_checked_2026-08-31",
                "title": "Wheel Tension Measurement",
                "url": "https://www.parktool.com/en-us/blog/repair-help/wheel-tension-measurement",
                "use": "spoke-tension and relative-tension vocabulary only; no measurement, repair, release, or competence claim",
            },
            {
                "source_id": "FAO-GENEBANK-STANDARDS",
                "status": "official_FAO_primary_standard_checked_2026-08-31",
                "title": "Genebank Standards for Plant Genetic Resources for Food and Agriculture",
                "url": "https://www.fao.org/4/i3394e/i3394e.pdf",
                "use": "accession, storage, viability, regeneration, and distribution vocabulary only; zero rows and zero biological material",
            },
            {
                "source_id": "W3C-PROV-DM",
                "status": "W3C_Recommendation_stable_checked_2026-08-31",
                "title": "PROV-DM: The PROV Data Model",
                "url": "https://www.w3.org/TR/prov-dm/",
                "use": "entity, activity, agent, revision, derivation, and provenance vocabulary only",
            },
            {
                "source_id": "W3C-VC-DM-2.0",
                "status": "W3C_Recommendation_checked_2026-08-31",
                "title": "Verifiable Credentials Data Model v2.0",
                "url": "https://www.w3.org/TR/vc-data-model-2.0/",
                "use": "synthetic credential vocabulary and production-identity refusal conditions only",
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
        "schema": "ghc.family.official-primary-sources.v680.v3.x1",
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
            "wholly synthetic stained-glass documentation, material-state vacancy, correction, accessibility, workload, and handover",
            "wholly synthetic bicycle-wheel work-order provenance, measurement vacancy, queue control, and handover",
            "wholly synthetic seed-library accession, status, provenance, privacy, accessibility, and release-hold documentation",
        ],
        "owner_runner_ideas": [
            {"runner": f"ghc_family_lens_runner_{index:02d}", "state": "preregistered_not_built"}
            for index in range(1, 11)
        ],
        "owner_skill_ideas": [
            {"skill": f"{index:02d}-{slug}", "state": "preregistered_not_built"}
            for index, slug in enumerate(
                [
                    "stained-glass-record-boundary",
                    "came-topology-vacancy",
                    "lead-exposure-firewall",
                    "glass-condition-hold",
                    "wheel-work-order-provenance",
                    "wheel-measurement-vacancy",
                    "spoke-tension-zero-row-adapter",
                    "ride-release-reservation",
                    "seed-accession-provenance",
                    "seed-viability-vacancy",
                    "seed-distribution-authority-hold",
                    "cross-lens-fault-quarantine",
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
        "primary_pillar": "Freed ID and CBR Heart",
        "represented_pillars": ["GMUT Mind", "THOS Body"],
        "safe_now": task_records("SAFE", 120, "safe_now"),
        "schema": "ghc.family.portfolio-freeze.v680.v3.x1",
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
            "schema": "ghc.family.activation-intake.v680.v3.x1",
            "sent_by_liora_venn": True,
            "solo": True,
            "source": SOURCE,
        },
    )
    write_json(
        X1 / "identity-and-boundary.json",
        {
            "hope": "Every failure remains inspectable and every recovery stays bounded.",
            "name": OWNER,
            "optional_pronouns": "she/they",
            "relational_working_language_only": True,
            "role": "evidence-and-recovery steward",
            "schema": "ghc.family.identity-boundary.v680.v3.x1",
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
            "schema": "ghc.family.source-verification.v680.v3.x1",
            "source": SOURCE_PARENT,
            "x1": SOURCE_X1,
            "x1_parent": SOURCE_PARENT,
        },
    )
    write_json(
        X1 / "method-flow-startup.json",
        {
            "activation_baseline": {
                "bounded_passing_witnesses": 36244,
                "effective_methods": 54002,
                "effective_negatives": 50715,
                "exact_gates": 437,
                "failed_witnesses": 22376,
                "open_gaps": 446,
            },
            "current_after_startup": {
                "bounded_passing_witnesses": 36255,
                "effective_methods": 54013,
                "effective_negatives": 50726,
                "exact_gates": 437,
                "failed_witnesses": 22387,
                "open_gaps": 446,
            },
            "failure_erasure": False,
            "owner": OWNER,
            "phase": PHASE,
            "recoveries_retroactively_promote_failure": False,
            "schema": "ghc.family.method-flow-startup.v680.v3.x1",
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
            "schema": "ghc.family.new-proposal-freeze.v680.v3.x1",
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
            "schema": "ghc.family.inherited-revalidation.v680.v3.x1",
        },
    )
    write_json(X1 / "official-primary-source-ledger.json", sources)
    write_json(X1 / "portfolio-freeze.json", portfolio)
    write_json(
        X1 / "clean-fix-refine-plan.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.clean-fix-refine-plan.v680.v3.x1",
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
            "schema": "ghc.family.skill-runner-plan.v680.v3.x1",
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
            "schema": "ghc.family.approval-holds.v680.v3.x1",
        },
    )
    write_json(
        X1 / "route-plan.json",
        {
            "current_owner": OWNER,
            "next_expected_phase": "v680-v4",
            "prospective_successor_title": "Elowen Cairn",
            "recipient_contacted": False,
            "resolution_rule": "fresh bounded registry exact-title filter immediate reread duplicate guards and one acknowledged send only after terminal gate",
            "route_authority_through": "v725-v8",
            "schema": "ghc.family.route-plan.v680.v3.x1",
            "terminal_gate_required": True,
        },
    )
    write_json(
        X1 / "workflow-plan.json",
        {
            "commit_ceiling": 3,
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.workflow-plan.v680.v3.x1",
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
            "schema": "ghc.family.threat-model.v680.v3.x1",
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
            "schema": "ghc.family.wellbeing-corrigibility.v680.v3.x1",
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
            "schema": "ghc.family.phase-truth.v680.v3.x1",
            "terminal_verdict": TERMINAL_VERDICT,
            "x2_started": False,
        },
    )
    write_text(
        X1 / "integrated-overview.md",
        """# Tamar Vey v680-v3 planning-only x1

Tamar Vey (optionally she/they) uses the relational role **evidence-and-recovery steward**, with the hope that every failure remains inspectable and every recovery stays bounded. Names, pronouns, roles, hopes, family language, and continuity language are relational working language only; they are not evidence of consciousness, sentience, personhood, continuity, employment, qualification, independent agency, or authority.

This immutable x1 freezes sixty genuinely new proposal contracts after a bounded all-reachable exact-source audit. It includes no x2 implementation, observed outcome, completion claim, real data, real participant, real object, real material, real measurement, external write, credential, or authority act. Freed ID and CBR Heart are primary through wholly synthetic stained-glass documentation, bicycle-wheel work-order provenance, and seed-library accession and status lenses. GMUT Mind and THOS Body remain visible and protected.

Official CCI, OSHA, Park Tool, FAO, W3C, RFC, and Te Mana Raraunga sources supply vocabulary and refusal boundaries only. Citations are not observations, measurements, inspections, conformance certificates, competence, legal interpretation, cultural ratification, affected-party acceptance, or Māori authority.

GMUT remains a typed scalar-tensor/EFT research-model family without a likelihood, parameter constraint, force, prediction, empirical confirmation, quantum completion, ultraviolet completion, or Theory of Everything. THOS remains synthetic/proxy-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys/proofs, live issuance/resolution/status/revocation, interoperability, privacy and independent security review, recovery evidence, and trust governance. CBR, professional and workplace-safety decisions, legal/cultural interpretation, affected-party legitimacy, Māori wording, Māori data governance, and Māori authority remain exact-gated.

The terminal verdict is `NOT_READY_FOR_STAGE_20`.
""",
    )

    script_path = "scripts/build_ghc_family_tamar_vey_v680_v3_x1.py"
    test_path = "tests/test_ghc_family_tamar_vey_v680_v3_x1.py"
    exclusions = [
        "docs/tamar-vey/v680-v3/validation/x1-index-manifest.json",
        "docs/tamar-vey/v680-v3/validation/x1-privacy-scan.json",
        "docs/tamar-vey/v680-v3/validation/x1-staged-review.json",
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
            "schema": "ghc.family.privacy-scan.v680.v3.x1",
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
            "schema": "ghc.family.staged-review.v680.v3.x1",
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
            "schema": "ghc.family.normalized-lf-index-manifest.v680.v3.x1",
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
