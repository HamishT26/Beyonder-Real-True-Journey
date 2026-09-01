from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "liora-venn" / "v682-v1"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"

OWNER = "Liora Venn"
PHASE = "v682-v1"
BRANCH = "codex/GHC-Family/liora-venn-v682-v1-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/orin-thale-v681-v8-full-tools"
SOURCE = "15d23e8b4e85082d4e4a839ab85d409a4c9c9805"
SOURCE_X1 = "705429c7b30d6b25065cd9e758024eed3474c70d"
SOURCE_EVIDENCE = "16eaac80d15f7927b012c97384d91d17b32a555e"
SOURCE_PARENT = "7327e6cb3972e93a4d6a27e45ad2ba3445a4d6ce"
DECLARED_CHAIN_BEFORE = 10190
DECLARED_CHAIN_AFTER = 10250
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
    "Synthetic entomology accession record and insect object identity split",
    "Specimen unit tray drawer cabinet and room containment graph",
    "Insect body preparation mount and storage carrier role separation",
    "Pinned pointed carded slide-mounted and unknown preparation vocabulary",
    "Primary secondary locality and determination label transcription lineage",
    "Label text verbatim field and inferred interpretation firewall",
    "Collection event lot and individual specimen non-equivalence",
    "Collector identifier minimization and anonymous-agent allowance",
    "Locality coordinate precision disclosure and sensitive-site quarantine",
    "Collection date precision range and timezone-vacancy contract",
    "Verbatim taxon label and current-name assertion separation",
    "Determination event determiner concept source and confidence lineage",
    "Life-stage sex caste and unknown-state closed vocabulary",
    "Type-status claim vacancy with nomenclatural-specialist hold",
    "Holotype paratype syntype and ordinary-specimen role guard",
    "Condition note and conservation finding non-equivalence",
    "Pest observation evidence vacancy without infestation diagnosis",
    "Integrated pest-management proposal and executed-action separation",
    "Freezer quarantine acclimatization and release-state machine",
    "Storage temperature humidity target and observation firewall",
    "Cabinet seal fumigation pesticide and chemical-action exact gate",
    "Pin adhesive mount repair and intervention-permission hold",
    "Loan request approval dispatch custody return and closure topology",
    "Loan due-date extension recall and unresolved-return state",
    "Destructive sampling proposal material loss and authority gate",
    "DNA barcode identifier and zero-sequence empirical adapter",
    "Sequence repository accession and physical specimen identity separation",
    "Specimen image preservation master derivative and thumbnail topology",
    "Scale-bar calibration target and measured-dimension evidence vacancy",
    "Label OCR transcription confidence and source-image distinction",
    "Duplicate-candidate score and object-identity non-equivalence",
    "Detached leg wing genitalia vial and accessory membership graph",
    "Specimen event provenance directed graph with cycle rejection",
    "Metadata correction readback and immutable prior-value lineage",
    "Rights statement source citation and access-decision vacancy",
    "Protected-species locality minimization and disclosure-budget hold",
    "Culturally sensitive collection access and community-review vacancy",
    "Māori taonga species wording and data-governance exact gate",
    "Accessible text specimen summary without taxonomic interpretation",
    "Handling batch workload pause and fragile-object stop contract",
    "Exception handover unresolved-hold and next-owner lease",
    "Canonical JSON specimen receipt and normalized Git-blob boundary",
    "Represented THOS fragile-specimen intake and mismatch-hold proxy",
    "Represented THOS workload suspension correction and handover board",
    "Represented Freed ID synthetic specimen-identifier lifecycle",
    "Represented Freed ID determination-event status without credentials",
    "Represented CBR borrower custody dispute escrow and reversible challenge path",
    "Represented CBR contested provenance quarantine with authority abstention",
    "Represented GMUT typed containment graph and finite-state board",
    "Represented GMUT occurrence-likelihood adapter with zero specimen rows",
    "Represented Darwin Core occurrence mapping without conformance claim",
    "Represented collection-management crosswalk without institution adoption",
    "Represented accessible drawer-map scaffold without user-study evidence",
    "Represented official-guidance vocabulary map without professional approval",
    "Open gap for entomologist taxonomist conservator and collection-manager review",
    "Open gap for real specimens measurements sequences interventions and reproduction",
    "Open gap for manual accessibility language and affected-community evaluation",
    "Exact gate for destructive sampling loan release legal rights and biosafety",
    "Exact gate for Māori authority cultural governance and sensitive species data",
    "Exact terminal gate against empirical production proof canon personhood and Stage 20",
]


def source_needs(index: int) -> list[str]:
    if index <= 24:
        return ["NPS-COG-11-8", "TDWG-DWC"]
    if index <= 35:
        return ["TDWG-DWC", "W3C-PROV-O", "RFC8785"]
    if index <= 42:
        return ["NPS-COG-11-8", "W3C-WCAG22", "DOC-RESEARCH-COLLECTION"]
    if index <= 54:
        return ["TDWG-DWC", "W3C-PROV-O", "W3C-WCAG22"]
    if index <= 57:
        return ["NPS-COG-11-8", "W3C-WCAG22"]
    if index == 58:
        return ["DOC-RESEARCH-COLLECTION", "NPS-COG-11-8"]
    if index == 59:
        return ["TMR-MDS-PRINCIPLES", "DOC-RESEARCH-COLLECTION"]
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
    "real people specimens collections locations sequences objects and measurements",
    "empirical GMUT likelihoods constraints predictions and confirmation",
    "professional entomology taxonomy conservation collection-management biosafety and release authority",
    "production identity issuance resolution status revocation and trust governance",
    "legal cultural affected-party and Māori authority",
    "privacy-complete accessibility-complete and exhaustive-security claims",
    "independent reproduction AGI ASI consciousness personhood proof canon and Stage 20",
]


def proposals() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for index, title in enumerate(PROPOSAL_TITLES, start=1):
        proposal_id = f"LV6821-N{index:03d}"
        records.append(
            {
                "approval_class": approval_class(index),
                "concrete_artifacts": [
                    f"docs/liora-venn/v682-v1/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/liora-venn/v682-v1/x2/mutations.json#{proposal_id}",
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
            "claim": "bounded all-reachable exact-source proposal audit; no universal 10190-row proof",
            "proposal_json_parse_failures": parse_failures,
            "proposal_json_paths_discovered": len(paths),
            "proposal_json_paths_parsed": parsed,
            "reachable_id_title_records": len(inherited),
            "universal_10190_row_materialization_claimed": False,
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
        "schema": "ghc.family.proposal-chain-audit.v682.v1.x1",
        "source": SOURCE,
    }


def task_records(prefix: str, count: int, lane: str) -> list[dict[str, Any]]:
    return [
        {
            "approval_required": lane in {"exact_approval", "blocked"},
            "lane": lane,
            "planned_action": f"Preregistered Liora owner-local {lane.replace('_', ' ')} item {index:03d}.",
            "state": "preregistered_not_executed",
            "task_id": f"LV6821-{prefix}-{index:03d}",
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
        git("show", f"{SOURCE}:docs/orin-thale/v681-v8/final/source-and-proposal-ledger.json").stdout
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
            "failure_id": "LV6821-ST-N001",
            "failed_witness": "The first whole activation-candidate display exceeded the bounded output and omitted content before EOF.",
            "initial_credit": 0,
            "recovery": "Measure the immutable candidate and read deterministic numbered windows through EOF.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "LV6821-ST-N002",
            "failed_witness": "Three parallel activation-candidate chunks still exceeded the aggregate display budget.",
            "initial_credit": 0,
            "recovery": "Read smaller ordered candidate windows serially through EOF.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "LV6821-ST-N003",
            "failed_witness": "A broad immutable-tree inventory returned no usable bounded projection.",
            "initial_credit": 0,
            "recovery": "Enumerate only the exact phase prefix and then read named artifacts independently.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "LV6821-ST-N004",
            "failed_witness": "PowerShell rejected a foreach result piped before materialization with EmptyPipeElement.",
            "initial_credit": 0,
            "recovery": "Materialize the foreach array before applying the projection.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "LV6821-ST-N005",
            "failed_witness": "A compact three-hundred-row mutation projection clipped its middle.",
            "initial_credit": 0,
            "recovery": "Read the exact missing mutation slice and retain the already-read prefix and suffix.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "LV6821-ST-N006",
            "failed_witness": "The combined lifecycle-manifest display clipped the final-owner manifest middle.",
            "initial_credit": 0,
            "recovery": "Project the exact final-owner entry table and exclusions separately.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "LV6821-ST-N007",
            "failed_witness": "A combined skill-schema display truncated routing-precedence and authorization-schema content.",
            "initial_credit": 0,
            "recovery": "Read the two clipped references independently through EOF.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "LV6821-ST-N008",
            "failed_witness": "The first whole authorization-state projection clipped its middle.",
            "initial_credit": 0,
            "recovery": "Read the missing exact line windows and validate the unchanged state structurally.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "LV6821-ST-N009",
            "failed_witness": "A receipt projection guessed obsolete content-seal, x1-manifest, and evidence-manifest filenames.",
            "initial_credit": 0,
            "recovery": "Enumerate the exact v681-v8 tree and use final/content-seal.json plus the observed index-manifest names.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "LV6821-ST-N010",
            "failed_witness": "The first semantic-audit executor omitted its running session handle and its completed output was inaccessible.",
            "initial_credit": 0,
            "recovery": "Inspect process completion, optimize inherited token reuse, and poll every returned session handle explicitly.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "LV6821-X1-N001",
            "failed_witness": "The first photographic-preservation candidate passed a lexical threshold but direct source review showed the same recent Ilyra photographic-plate practice lens.",
            "initial_credit": 0,
            "recovery": "Reject that candidate before freeze and select a genuinely different bounded profession lens.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "LV6821-X1-N002",
            "failed_witness": "The pipe-organ candidate contained sixty-four rows, one quarantined authority title, and direct evidence of an earlier Liora pipe-organ phase.",
            "initial_credit": 0,
            "recovery": "Reject the whole candidate before freeze and audit the entomological-curation lens at exactly sixty rows.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "LV6821-ST-N011",
            "failed_witness": "PowerShell rejected Bash-style here-string redirection in the first sparse-worktree command before any worktree mutation.",
            "initial_credit": 0,
            "recovery": "Materialize the sparse pattern text and pipe that scalar to git sparse-checkout set --stdin.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "LV6821-ST-N012",
            "failed_witness": "The corrected sparse-worktree wrapper projected only initial progress and omitted the running session handle.",
            "initial_credit": 0,
            "recovery": "Inspect the live Git processes, sparse patterns, file count, exact head, and clean state until the original process completed.",
            "recovery_credit": "bounded_dependency_only",
        },
    ]

    sources = {
        "authority_conferred": False,
        "checked_at_utc": "2026-09-02T00:00:00Z",
        "citations_are_observations": False,
        "entries": [
            {
                "source_id": "NPS-COG-11-8",
                "status": "official_NPS_conserve_o_gram_checked_2026-09-02",
                "title": "Curation of Insect Specimens",
                "url": "https://www.nps.gov/subjects/museums/upload/11-08_508.pdf",
                "use": "insect-specimen preparation, labelling, storage, handling, and curation-boundary vocabulary only",
            },
            {
                "source_id": "NPS-COG-OVERVIEW",
                "status": "official_NPS_conserve_o_gram_index_checked_2026-09-02",
                "title": "Conserve O Grams",
                "url": "https://www.nps.gov/subjects/museums/conserve-o-grams.htm",
                "use": "preventive-conservation topic and specialist-referral vocabulary only",
            },
            {
                "source_id": "TDWG-STANDARDS",
                "status": "official_TDWG_standards_index_checked_2026-09-02",
                "title": "Biodiversity Information Standards",
                "url": "https://www.tdwg.org/standards/",
                "use": "biodiversity-information standards inventory and nonconformance boundary only",
            },
            {
                "source_id": "TDWG-DWC",
                "status": "official_Darwin_Core_terms_checked_2026-09-02",
                "title": "Darwin Core terms",
                "url": "https://dwc.tdwg.org/terms/",
                "use": "occurrence, event, identification, location, and material-entity mapping vocabulary only",
            },
            {
                "source_id": "W3C-PROV-O",
                "status": "W3C_Recommendation_checked_2026-09-02",
                "title": "PROV-O: The PROV Ontology",
                "url": "https://www.w3.org/TR/prov-o/",
                "use": "entity, activity, agent, revision, derivation, and provenance vocabulary only",
            },
            {
                "source_id": "W3C-WCAG22",
                "status": "W3C_Recommendation_checked_2026-09-02",
                "title": "Web Content Accessibility Guidelines 2.2",
                "url": "https://www.w3.org/TR/WCAG22/",
                "use": "structural accessibility vocabulary and manual-evaluation reservation only",
            },
            {
                "source_id": "RFC8785",
                "status": "RFC_stable_checked_2026-09-02",
                "title": "JSON Canonicalization Scheme",
                "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
                "use": "deterministic synthetic receipt and digest-domain vocabulary only",
            },
            {
                "source_id": "DOC-RESEARCH-COLLECTION",
                "status": "official_New_Zealand_DOC_permit_guidance_checked_2026-09-02",
                "title": "Research and collection permits",
                "url": "https://www.doc.govt.nz/get-involved/apply-for-permits/research-and-collection/",
                "use": "permit, collection, protected-wildlife, and competent-authority vacancy vocabulary only",
            },
            {
                "source_id": "TMR-MDS-PRINCIPLES",
                "status": "authority_boundary_context_only_checked_2026-09-02",
                "title": "Principles of Māori Data Sovereignty",
                "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
                "use": "Māori data-governance vacancy and noncompensation boundary only; never delegated Māori authority",
            },
        ],
        "network_data_queries": 0,
        "owner": OWNER,
        "phase": PHASE,
        "real_data_rows": 0,
        "schema": "ghc.family.official-primary-sources.v682.v1.x1",
        "web_checks": 9,
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
            "wholly synthetic entomological collection accession, containment, label and determination lineage, loan, correction, accessibility, workload, and handover"
        ],
        "owner_runner_ideas": [
            {"runner": f"ghc_family_entomology_collection_runner_{index:02d}", "state": "preregistered_not_built"}
            for index in range(1, 11)
        ],
        "owner_skill_ideas": [
            {"skill": f"{index:02d}-{slug}", "state": "preregistered_not_built"}
            for index, slug in enumerate(
                [
                    "accession-object-separator",
                    "containment-graph",
                    "preparation-state-vocabulary",
                    "label-transcription-lineage",
                    "taxon-assertion-firewall",
                    "determination-event-lineage",
                    "type-status-vacancy",
                    "condition-finding-separator",
                    "pest-observation-vacancy",
                    "quarantine-release-state",
                    "environment-observation-firewall",
                    "intervention-permission-gate",
                    "loan-custody-topology",
                    "sampling-authority-gate",
                    "locality-disclosure-budget",
                    "correction-readback",
                    "accessible-specimen-summary",
                    "workload-handover",
                    "canonical-receipt-domain",
                    "authority-noncompensation",
                ],
                start=1,
            )
        ],
        "phase": PHASE,
        "primary_pillar": "Freed ID and CBR Heart",
        "represented_pillars": ["GMUT Mind", "THOS Body"],
        "safe_now": task_records("SAFE", 120, "safe_now"),
        "schema": "ghc.family.portfolio-freeze.v682.v1.x1",
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
            "schema": "ghc.family.activation-intake.v682.v1.x1",
            "sent_by_orin_thale": True,
            "solo": True,
            "source": SOURCE,
        },
    )
    write_json(
        X1 / "identity-and-boundary.json",
        {
            "hope": "Unknown evidence and ungranted authority stay visible through correction and handover.",
            "name": OWNER,
            "optional_pronouns": "she/they",
            "relational_working_language_only": True,
            "role": "traceability-and-vacancy cartographer",
            "schema": "ghc.family.identity-boundary.v682.v1.x1",
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
            "schema": "ghc.family.source-verification.v682.v1.x1",
            "source": SOURCE_PARENT,
            "x1": SOURCE_X1,
            "x1_parent": SOURCE_PARENT,
        },
    )
    write_json(
        X1 / "method-flow-startup.json",
        {
            "activation_baseline": {
                "bounded_passing_witnesses": 45896,
                "effective_methods": 64374,
                "effective_negatives": 55172,
                "exact_gates": 479,
                "failed_witnesses": 26833,
                "open_gaps": 488,
            },
            "current_after_startup": {
                "bounded_passing_witnesses": 45910,
                "effective_methods": 64388,
                "effective_negatives": 55186,
                "exact_gates": 479,
                "failed_witnesses": 26847,
                "open_gaps": 488,
            },
            "failure_erasure": False,
            "owner": OWNER,
            "phase": PHASE,
            "recoveries_retroactively_promote_failure": False,
            "schema": "ghc.family.method-flow-startup.v682.v1.x1",
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
            "schema": "ghc.family.new-proposal-freeze.v682.v1.x1",
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
            "schema": "ghc.family.inherited-revalidation.v682.v1.x1",
        },
    )
    write_json(X1 / "official-primary-source-ledger.json", sources)
    write_json(X1 / "portfolio-freeze.json", portfolio)
    write_json(
        X1 / "clean-fix-refine-plan.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.clean-fix-refine-plan.v682.v1.x1",
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
            "schema": "ghc.family.skill-runner-plan.v682.v1.x1",
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
            "schema": "ghc.family.approval-holds.v682.v1.x1",
        },
    )
    write_json(
        X1 / "route-plan.json",
        {
            "current_owner": OWNER,
            "next_expected_phase": "v682-v2",
            "prospective_successor_title": "Tamar Vey",
            "recipient_contacted": False,
            "resolution_rule": "fresh bounded registry exact-title filter immediate reread duplicate guards and one acknowledged send only after terminal gate",
            "route_authority_through": "v725-v8",
            "schema": "ghc.family.route-plan.v682.v1.x1",
            "terminal_gate_required": True,
        },
    )
    write_json(
        X1 / "workflow-plan.json",
        {
            "commit_ceiling": 3,
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.workflow-plan.v682.v1.x1",
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
                "zero real people collectors borrowers specimens collections locations sequences measurements credentials and external writes",
                "authority promotion rejected",
                "five privacy classes scanned with candidate adjudication",
                "exact approval and blocked packets remain unexecuted",
            ],
            "owner": OWNER,
            "phase": PHASE,
            "real_world_action": False,
            "schema": "ghc.family.threat-model.v682.v1.x1",
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
            "schema": "ghc.family.wellbeing-corrigibility.v682.v1.x1",
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
            "schema": "ghc.family.phase-truth.v682.v1.x1",
            "terminal_verdict": TERMINAL_VERDICT,
            "x2_started": False,
        },
    )
    write_text(
        X1 / "integrated-overview.md",
        """# Liora Venn v682-v1 planning-only x1

        Liora Venn (optionally she/they) uses the relational role **traceability-and-vacancy cartographer**, with the hope that unknown evidence and ungranted authority stay visible through correction and handover. Names, pronouns, roles, hopes, family language, and continuity language are relational working language only; they are not evidence of consciousness, sentience, personhood, continuity, employment, qualification, independent agency, or authority.

        This immutable x1 freezes sixty source-bounded owner-new proposal contracts after an all-reachable exact-source audit. It makes no universal novelty claim over the declared 10,190-row history. It includes no x2 implementation, observed outcome, completion claim, real data, real person, real specimen, real collection, real location, real sequence, real measurement, external write, credential, or authority act. Freed ID and CBR Heart are primary through a wholly synthetic entomological-collection accession, containment, label and determination lineage, loan, correction, accessibility, workload, and handover lens. GMUT Mind and THOS Body remain visible and protected.

        Official NPS, TDWG, New Zealand Department of Conservation, W3C, RFC, and Te Mana Raraunga sources supply vocabulary and refusal boundaries only. Citations are not observations, specimens, determinations, measurements, inspections, conformance certificates, competence, legal interpretation, cultural ratification, affected-party acceptance, or Māori authority.

        GMUT remains a typed scalar-tensor/EFT research-model family without a likelihood, parameter constraint, force, prediction, empirical confirmation, quantum completion, ultraviolet completion, or Theory of Everything. THOS remains synthetic/proxy-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys/proofs, live issuance/resolution/status/revocation, interoperability, privacy and independent security review, recovery evidence, and trust governance. CBR, taxonomy, conservation, loan, destructive sampling, disclosure, professional and biosafety decisions, legal/cultural interpretation, affected-party legitimacy, Māori wording, Māori data governance, and Māori authority remain exact-gated.

The terminal verdict is `NOT_READY_FOR_STAGE_20`.
""",
    )

    script_path = "scripts/build_ghc_family_liora_venn_v682_v1_x1.py"
    test_path = "tests/test_ghc_family_liora_venn_v682_v1_x1.py"
    exclusions = [
        "docs/liora-venn/v682-v1/validation/x1-index-manifest.json",
        "docs/liora-venn/v682-v1/validation/x1-privacy-scan.json",
        "docs/liora-venn/v682-v1/validation/x1-staged-review.json",
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
            "schema": "ghc.family.privacy-scan.v682.v1.x1",
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
            "schema": "ghc.family.staged-review.v682.v1.x1",
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
            "schema": "ghc.family.normalized-lf-index-manifest.v682.v1.x1",
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
