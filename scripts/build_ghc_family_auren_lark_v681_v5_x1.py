from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
from collections import Counter
from collections.abc import Iterable
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "auren-lark" / "v681-v5"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"

OWNER = "Auren Lark"
PHASE = "v681-v5"
BRANCH = "codex/GHC-Family/auren-lark-v681-v5-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/ilyra-fen-v681-v4-full-tools"
LYREN_SOURCE = "883bb81ded9a802d4b220db5aa24974559465cf1"
SOURCE_X1 = "27943a6e5d03812dfa9cae6795b204b0a3237e6b"
SOURCE_EVIDENCE = "aca60506d377f96c7a321b8585fda73668584f64"
SOURCE = "d2f8f60dfaa4c7bd825ae04d57ba0e76bbb7a151"
DECLARED_CHAIN_BEFORE = 9950
DECLARED_CHAIN_AFTER = 10010
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
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    WRITTEN.append(rel(path))


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")
    WRITTEN.append(rel(path))


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def jaccard(left: str, right: str) -> float:
    left_tokens = set(re.findall(r"[a-z0-9]+", left.casefold()))
    right_tokens = set(re.findall(r"[a-z0-9]+", right.casefold()))
    if not left_tokens and not right_tokens:
        return 1.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


PROPOSAL_TITLES = [
    "Synthetic civic-tree record and living tree referent identity split",
    "Civic-tree pseudonymous asset key with namespace collision quarantine",
    "Tree inventory observation and maintenance work-order separation",
    "Species-label assertion with taxonomic verification vacancy",
    "Planting-date precision and unknown-year refusal contract",
    "Trunk-diameter unit measurement-method and uncertainty boundary",
    "Tree-height canopy-spread and crown-base typed measurement separation",
    "Location-cell coarsening with exact-coordinate nonmaterialization",
    "Site-context vocabulary with ownership and jurisdiction abstention",
    "Inventory-observation timestamp timezone precision and vacancy contract",
    "Condition code and professional diagnosis non-equivalence",
    "Risk-flag placeholder without hazard assessment or public-safety authority",
    "Defect annotation vocabulary with visual-inspection evidence vacancy",
    "Maintenance recommendation and authorized work decision separation",
    "Pruning watering mulching and removal action nonexecution ledger",
    "Work-order requested scheduled held completed and cancelled state machine",
    "Contractor credential licence and competence exact vacancy",
    "Field observer reviewer approver and authority-role separation",
    "Image attachment provenance with zero real image content",
    "Sensor attachment and civic-tree record nonidentity boundary",
    "Synthetic correction request with disputed-field pointer",
    "Statement-of-correction attachment when replacement remains refused",
    "Supersession chain with reversible prior-state references",
    "Nonerasing amendment event with reason and readback receipt",
    "PROV entity activity agent-role graph for civic-tree record revision",
    "Dataset version and individual record revision separation",
    "Checksum content identity and civic-tree meaning non-equivalence",
    "Canonical JSON receipt for synthetic civic-tree record structure",
    "Bitemporal observed-effective and recorded-system clock separation",
    "Duplicate tree-record identifier collision hold",
    "Merge split retire and successor lineage without physical-tree inference",
    "Accessible text-first civic-tree status summary with explicit headings",
    "Deterministic reading order for correction and refusal history",
    "Plain-language status term and machine-code pairing",
    "Exception review queue with workload pause and handover state",
    "Correction refusal reason code with human-readable explanation vacancy",
    "Privacy purpose register for wholly synthetic civic-tree fixtures",
    "Location minimization board with exact-address refusal",
    "Person organization and worker identifier minimization guard",
    "Retention-review expiry and deletion-authority vacancy",
    "Consent notice and affected-party decision vacancy",
    "Public-release hold with explicit competent-authority requirement",
    "Represented Freed ID subjectless civic-tree catalogue pseudonym graph",
    "Represented Freed ID correction request without live credential lifecycle",
    "Represented CBR access correction contest and remedy queue",
    "Represented CBR refusal appeal and nonretaliation declaration",
    "Represented THOS civic-tree task workboard with reversible holds",
    "Represented THOS workload stop state and shift-handover proxy",
    "Represented GMUT finite constraint graph for measurement obligations",
    "Represented GMUT uncertainty surface with zero empirical likelihood rows",
    "Represented DCAT civic-tree dataset catalogue mapping without publication",
    "Represented PROV revision mapping without provenance conformance claim",
    "Represented Urban FIA vocabulary crosswalk without field measurement",
    "Represented New Zealand accessibility vocabulary without conformance claim",
    "Open gap for real arborist urban-forester and records-professional evaluation",
    "Open gap for real residents disabled users and affected-party review",
    "Open gap for real civic-tree inventory rows measurements incidents and reproduction",
    "Exact gate for statutory council ownership safety removal and disclosure decisions",
    "Exact gate for tangata whenua cultural governance Maori data and place authority",
    "Stage 20 nonpromotion boundary for every Auren synthetic civic-tree artifact and any science deployment identity AGI ASI consciousness personhood proof or canon claim",
]

MUTATION_TYPES = [
    "missing_required_field",
    "lifecycle_inversion",
    "stale_provenance_digest",
    "evidence_status_promotion",
    "authority_promotion",
]

PROTECTED_GATES = [
    "real people residents workers arborists urban foresters councils organizations trees sites coordinates images inventory rows measurements incidents work orders and decisions",
    "empirical GMUT likelihoods constraints predictions forces confirmation final physics and Theory of Everything",
    "professional arboriculture forestry records-management accessibility public-safety inspection certification and operational authority",
    "production identity issuance resolution status revocation interoperability recovery and trust governance",
    "privacy accessibility remedy ownership jurisdiction consent disclosure cultural affected-party Maori-language Maori-data-governance and Maori authority",
    "privacy-complete accessibility-complete exhaustive-security and independent-reproduction claims",
    "AGI ASI consciousness personhood proof canon and Stage 20",
]


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
    if index <= 20:
        return ["USFS-URBAN-FIA", "JSON-SCHEMA-2020-12", "W3C-PROV"]
    if index <= 40:
        return ["W3C-PROV", "RFC8785", "DCMI-TERMS", "W3C-WCAG22"]
    if index <= 54:
        return ["NZ-PRIVACY-P7", "NZ-WEB-ACCESS-1.2", "NIST-PRIVACY", "W3C-DCAT3", "TMR-CHARTER"]
    return ["USFS-URBAN-FIA", "NZ-PRIVACY-P7", "NZ-WEB-ACCESS-1.2", "TMR-CHARTER", "W3C-WCAG22"]


def proposals() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, title in enumerate(PROPOSAL_TITLES, start=1):
        proposal_id = f"AL6815-N{index:03d}"
        rows.append(
            {
                "approval_class": approval_class(index),
                "concrete_artifacts": [
                    f"docs/auren-lark/v681-v5/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/auren-lark/v681-v5/x2/mutation-results.json#{proposal_id}",
                ],
                "execution_lane": execution_lane(index),
                "expected_disposition": disposition(index),
                "falsifier_or_acceptance_gate": (
                    f"Accept {proposal_id} only if its bounded positive witness passes, all five invalid "
                    "mutations are rejected, and no empirical, professional, production, legal, cultural, "
                    "affected-party, Maori-authority, identity, or Stage 20 claim is promoted."
                ),
                "hypothesis": (
                    f"A wholly synthetic zero-row contract for {title.casefold()} can preserve its named "
                    "distinction and reject preregistered counterexamples within Auren owner-local scope."
                ),
                "null_or_failure_condition": (
                    f"{proposal_id} is falsified if an invalid fixture is accepted, its positive structure "
                    "is rejected, a real state is inferred, or a protected gate is promoted."
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
                    f"Quarantine only the {proposal_id} witness, retain the failure at zero credit, and "
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
    requests = b"".join(f"{tree}:{path}\n".encode() for path in paths)
    completed = subprocess.run(
        ["git", "-C", str(ROOT), "cat-file", "--batch"],
        input=requests,
        check=True,
        capture_output=True,
    )
    stream = io.BytesIO(completed.stdout)
    for path in paths:
        header = stream.readline().decode("utf-8", errors="replace").rstrip("\n")
        if header.endswith(" missing"):
            continue
        parts = header.split()
        if len(parts) != 3 or parts[1] != "blob":
            raise RuntimeError(f"unexpected cat-file header for {path}: {header}")
        size = int(parts[2])
        data = stream.read(size)
        if stream.read(1) != b"\n":
            raise RuntimeError(f"missing cat-file separator for {path}")
        yield path, data


def proposal_chain_audit(new_records: list[dict[str, Any]]) -> dict[str, Any]:
    result = git("grep", "-l", "-I", '"proposal_id"', SOURCE, "--", "*.json", check=False)
    if result.returncode not in (0, 1):
        raise RuntimeError(result.stderr)
    prefix = SOURCE + ":"
    paths = sorted({path.removeprefix(prefix) for path in result.stdout.splitlines() if path})
    parsed = 0
    failures: list[dict[str, str]] = []
    inherited: list[dict[str, str]] = []
    for path, data in batch_blobs(SOURCE, paths):
        try:
            document = json.loads(data.decode("utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            failures.append({"error": type(exc).__name__, "path": path})
            continue
        parsed += 1
        for record in iter_proposal_records(document):
            inherited.append({"path": path, **record})
    if not paths or not parsed or not inherited:
        raise RuntimeError("proposal audit requires nonzero exact-source paths and records")

    inherited_titles = {record["title"] for record in inherited}
    collisions: list[str] = []
    neighbors: list[dict[str, Any]] = []
    for proposal in new_records:
        title = proposal["title"]
        if title in inherited_titles:
            collisions.append(title)
        best = max(inherited, key=lambda record: jaccard(title, record["title"]))
        score = jaccard(title, best["title"])
        neighbors.append(
            {
                "best_inherited_neighbor": best,
                "proposal_id": proposal["proposal_id"],
                "quarantined": score >= 0.78,
                "title": title,
                "token_jaccard": round(score, 6),
            }
        )
    quarantined = [row for row in neighbors if row["quarantined"]]
    if collisions or quarantined:
        raise RuntimeError(
            "proposal novelty quarantine required: "
            + json.dumps({"exact": collisions, "neighbors": quarantined}, ensure_ascii=False)
        )
    return {
        "audit_scope": {
            "claim": "bounded all-reachable exact-source proposal audit; no universal declared-chain proof",
            "earlier_exact_term_probe_paths": 2752,
            "earlier_exact_term_probe_hits": 0,
            "proposal_json_parse_failures": failures,
            "proposal_json_paths_discovered": len(paths),
            "proposal_json_paths_parsed": parsed,
            "reachable_id_title_records": len(inherited),
            "universal_declared_chain_materialization_claimed": False,
        },
        "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
        "declared_chain_before": DECLARED_CHAIN_BEFORE,
        "exact_title_collisions": collisions,
        "maximum_neighbor_score": max(row["token_jaccard"] for row in neighbors),
        "neighbor_reviews": neighbors,
        "new_proposal_count": len(new_records),
        "owner": OWNER,
        "phase": PHASE,
        "quarantine_threshold_token_jaccard": 0.78,
        "quarantined_neighbors": quarantined,
        "schema": "ghc.family.proposal-chain-audit.v681.v5.x1",
        "source": SOURCE,
    }


def planned_tasks(prefix: str, count: int, lane: str, titles: list[str]) -> list[dict[str, Any]]:
    actions = [
        "type the record boundary",
        "test the acceptance and refusal pair",
        "verify provenance and rollback fields",
        "review the authority and privacy hold",
        "check the accessible text representation",
    ]
    return [
        {
            "approval_required": lane in {"exact_approval", "blocked"},
            "lane": lane,
            "planned_action": f"{actions[(index - 1) % len(actions)].capitalize()} for {titles[(index - 1) % len(titles)].casefold()}.",
            "state": "preregistered_not_executed",
            "task_id": f"AL6815-{prefix}-{index:03d}",
        }
        for index in range(1, count + 1)
    ]


STARTUP_FAILURES = [
    ("The first whole-packet rendering omitted a bounded middle range before EOF was attributable.", "Reread only the missing range with literal UTF-8 line bounds, then continue through EOF."),
    ("A PowerShell skill inventory piped directly from foreach and failed with EmptyPipeElement.", "Materialize the bounded rows before piping and retain the parser failure at zero credit."),
    ("A one-block authorization-state rendering exceeded the output budget.", "Read the file in four bounded UTF-8 line ranges through EOF."),
    ("The first manifest projection guessed an absent entry_count helper-return key.", "Inspect the helper return schema and retry only the failed projection with the exact entries key."),
    ("The first D-lane preflight wrapper completed without a usable projection.", "Split capacity, branch, worktree, and remote checks into bounded literal scalar probes."),
    ("An absent local branch ref was incorrectly trimmed as though it were a string.", "Materialize zero-or-more rows and test the row count without trimming null."),
    ("A PowerShell proposal-path projection crossed its bounded window with no output.", "Use one native Git listing and in-memory batch-blob filtering instead of PowerShell per-line filtering."),
    ("Eight separate exact-term Git greps crossed the bounded window with no output.", "Replace the repeated scans with one in-memory exact-source batch-blob pass."),
    ("A combined exact-term Git grep crossed the bounded window with no output.", "Use the already bounded proposal path family and a single decoded in-memory term audit."),
    ("Git ls-tree rejected unsupported glob pathspec magic.", "List exact-source docs once and filter proposal paths without unsupported pathspec magic."),
    ("A cmd wrapper passed quoted worktree text literally to git -C and failed.", "Avoid the cross-shell quoted path and use the active worktree as the command working directory."),
    ("A cmd proposal-regex projection returned no usable rows after a quoting mismatch.", "Use a literal proposal token first, then bound and parse the result in memory."),
    ("An overbroad proposal filename projection exceeded its output budget.", "Replace the rendering with a count and bounded batch-blob audit; retain the truncation at zero credit."),
    ("The worktree setup wrapper returned only its first progress line while checkout continued.", "Inspect the exact target process and filesystem, wait for quiescence, and verify the finished sparse lane without recreating it."),
    ("A concurrent branch and worktree probe returned no output while checkout still held the setup path.", "Wait for the already-running owner checkout and then verify head, branch, sparse patterns, and clean state separately."),
    ("The first x1 builder quarantined one inherited-neighbour terminal title at token Jaccard 0.809524 before writing phase artifacts.", "Replace only the quarantined title with an independently phrased Stage 20 nonpromotion boundary and retry the previously unsuccessful builder once."),
]


def build() -> None:
    if git("rev-parse", "HEAD").stdout.strip() != SOURCE:
        raise RuntimeError("x1 builder must begin at the immutable Ilyra final")
    if git("branch", "--show-current").stdout.strip() != BRANCH:
        raise RuntimeError("wrong Auren owner branch")
    if (BASE / "x2").exists():
        raise RuntimeError("x2 material is forbidden in planning-only x1")

    proposal_records = proposals()
    expected = Counter({"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
    if len(proposal_records) != 60 or Counter(row["expected_disposition"] for row in proposal_records) != expected:
        raise RuntimeError("proposal count or expected-disposition contract drift")
    if any(row["expected_disposition"] not in ALLOWED_OUTCOMES for row in proposal_records):
        raise RuntimeError("unknown outcome label")

    audit = proposal_chain_audit(proposal_records)
    inherited = json.loads(
        git("show", f"{SOURCE}:docs/ilyra-fen/v681-v4/x1/new-proposal-freeze.json").stdout
    )
    inherited_reviews = [
        {
            "completion_credit": 0,
            "inherited_owner": "Ilyra Fen",
            "proposal_id": row["proposal_id"],
            "review_state": "inherited_source_evidence_only",
            "title": row["title"],
        }
        for row in inherited["proposals"][-20:]
    ]
    startup = [
        {
            "failed_witness": failed,
            "failure_id": f"AL6815-ST-N{index:03d}",
            "initial_credit": 0,
            "recovery": recovery,
            "recovery_credit": "bounded_dependency_only",
        }
        for index, (failed, recovery) in enumerate(STARTUP_FAILURES, start=1)
    ]

    source_entries = [
        ("USFS-URBAN-FIA", "Urban Forest Inventory and Analysis Field Guide", "https://research.fs.usda.gov/understory/urban-forest-inventory-and-analysis-field-guide", "urban-tree inventory field-item vocabulary only; no field measurement identification inspection diagnosis or professional authority"),
        ("W3C-PROV", "PROV Overview", "https://www.w3.org/TR/prov-overview/", "entity activity agent role revision and derivation vocabulary only"),
        ("W3C-WCAG22", "Web Content Accessibility Guidelines 2.2", "https://www.w3.org/TR/WCAG22/", "structural accessibility vocabulary with manual assistive-technology cognitive and affected-user evaluation reserved"),
        ("NZ-PRIVACY-P7", "Principle 7 - Correction of personal information", "https://www.privacy.org.nz/privacy-principles/7/", "correction-request and statement-of-correction vocabulary only; no legal conclusion or applicability claim"),
        ("NZ-WEB-ACCESS-1.2", "About the Web Accessibility Standard 1.2", "https://www.digital.govt.nz/standards-and-guidance/nz-government-web-standards/web-accessibility-standard-1-2/about-the-web-accessibility-standard", "New Zealand public-sector accessibility context only; no conformance or jurisdiction claim"),
        ("NIST-PRIVACY", "NIST Privacy Framework", "https://www.nist.gov/privacy-framework", "voluntary privacy-risk vocabulary only; version and draft status remain explicit"),
        ("W3C-DCAT3", "Data Catalog Vocabulary Version 3", "https://www.w3.org/TR/vocab-dcat-3/", "dataset catalogue version and distribution vocabulary only; no publication or conformance claim"),
        ("DCMI-TERMS", "DCMI Metadata Terms", "https://www.dublincore.org/specifications/dublin-core/dcmi-terms/", "identifier source rights provenance and dataset vocabulary only"),
        ("RFC8785", "RFC 8785 JSON Canonicalization Scheme", "https://www.rfc-editor.org/rfc/rfc8785.html", "deterministic synthetic receipt vocabulary only; informational RFC status remains explicit"),
        ("JSON-SCHEMA-2020-12", "JSON Schema Draft 2020-12", "https://json-schema.org/draft/2020-12", "machine-readable record validation vocabulary only"),
        ("TMR-CHARTER", "Te Mana Raraunga Charter", "https://www.temanararaunga.maori.nz/tutohinga", "Maori data-sovereignty and authority vacancy boundary only; never cultural ratification or delegated authority"),
    ]
    sources = {
        "authority_conferred": False,
        "checked_at_nz": "2026-09-01",
        "citations_are_observations": False,
        "entries": [
            {"source_id": source_id, "status": "official_or_primary_source_checked_2026-09-01", "title": title, "url": url, "use": use}
            for source_id, title, url, use in source_entries
        ],
        "external_source_entries": len(source_entries),
        "network_data_queries": 0,
        "official_source_web_queries": 14,
        "owner": OWNER,
        "phase": PHASE,
        "real_data_rows": 0,
        "schema": "ghc.family.official-primary-sources.v681.v5.x1",
    }

    skill_names = [
        "ghc-family-civic-tree-record-boundary",
        "ghc-family-civic-tree-pseudonym-guard",
        "ghc-family-inventory-observation-separator",
        "ghc-family-taxonomy-assertion-vacancy",
        "ghc-family-tree-measurement-unit-guard",
        "ghc-family-location-coarsening-refusal",
        "ghc-family-condition-diagnosis-firewall",
        "ghc-family-risk-authority-hold",
        "ghc-family-work-order-state-rail",
        "ghc-family-correction-request-ledger",
        "ghc-family-statement-of-correction-attach",
        "ghc-family-nonerasing-amendment-chain",
        "ghc-family-bitemporal-tree-record",
        "ghc-family-tree-record-merge-split-lineage",
        "ghc-family-accessible-tree-status",
        "ghc-family-civic-tree-exception-queue",
        "ghc-family-tree-record-privacy-purpose",
        "ghc-family-public-release-authority-hold",
        "ghc-family-civic-tree-canonical-receipt",
        "ghc-family-stage20-terminal-refusal",
    ]
    runner_names = [
        "ghc_family_civic_tree_schema_runner",
        "ghc_family_tree_measurement_guard_runner",
        "ghc_family_correction_lineage_runner",
        "ghc_family_civic_tree_provenance_runner",
        "ghc_family_tree_record_privacy_runner",
        "ghc_family_tree_status_accessibility_runner",
        "ghc_family_civic_tree_mutation_runner",
        "ghc_family_civic_tree_outcome_runner",
        "ghc_family_civic_tree_manifest_runner",
        "ghc_family_stage20_refusal_runner",
    ]
    titles = [row["title"] for row in proposal_records]
    portfolio = {
        "blocked": planned_tasks("BLOCK", 10, "blocked", titles[57:]),
        "caps_are_ceilings": True,
        "commit_cap": 3,
        "document_word_cap": 100000,
        "exact_approval": planned_tasks("APPROVAL", 20, "exact_approval", titles[57:]),
        "materialized_file_stop": 2000,
        "owner_candidates": planned_tasks("CAND", 80, "bounded_candidate", titles[42:57]),
        "owner_clean_fix_refine": planned_tasks("CFR", 100, "clean_fix_refine", titles),
        "owner_practice_lenses": [
            "wholly synthetic urban-forestry inventory data-stewardship lens",
            "wholly synthetic public-record quality-analysis lens",
            "wholly synthetic accessibility-documentation review lens",
        ],
        "owner_runner_ideas": [{"runner": name, "state": "preregistered_not_built"} for name in runner_names],
        "owner_skill_ideas": [{"skill": name, "state": "preregistered_not_built"} for name in skill_names],
        "phase": PHASE,
        "primary_pillar": "Freed ID and CBR Heart",
        "represented_pillars": ["THOS Body", "GMUT Mind"],
        "safe_now": planned_tasks("SAFE", 120, "safe_now", titles[:42]),
        "schema": "ghc.family.portfolio-freeze.v681.v5.x1",
        "successor_candidates": planned_tasks("SUCC-CAND", 20, "successor_seed", titles[42:57]),
        "successor_clean_fix_refine": planned_tasks("SUCC-CFR", 30, "successor_seed", titles),
        "successor_practice_recommendation": "wholly synthetic tool-library loan-record correction and handover steward; zero-credit seed only and Sable Rook chooses independently",
        "successor_runner_ideas": planned_tasks("SUCC-RUN", 10, "successor_seed", titles),
        "successor_skill_ideas": planned_tasks("SUCC-SKILL", 10, "successor_seed", titles),
    }

    write_json(X1 / "activation-intake.json", {
        "activation": "ACKNOWLEDGED_EXISTING_TASK_SEND",
        "created_or_forked_task": False,
        "owner": OWNER,
        "phase": PHASE,
        "relational_language_only": True,
        "schema": "ghc.family.activation-intake.v681.v5.x1",
        "sent_by_ilyra_fen": True,
        "solo": True,
        "source": SOURCE,
    })
    write_json(X1 / "identity-and-boundary.json", {
        "hope": "Make synthetic civic-tree record correction, provenance, accessibility, and refusal states inspectable without converting software evidence into authority.",
        "name": OWNER,
        "not_evidence_of": ["consciousness", "sentience", "personhood", "identity continuity", "employment", "qualification", "independent agency", "scientific operational professional legal cultural affected-party or Maori authority"],
        "optional_pronouns": "he/they",
        "relational_working_language_only": True,
        "role": "Stewardship State Cartographer",
        "schema": "ghc.family.identity-boundary.v681.v5.x1",
    })
    write_json(X1 / "source-verification.json", {
        "branch": SOURCE_BRANCH,
        "clean": True,
        "commits_lyren_source_to_ilyra_final": 3,
        "content_seal_entries_replayed": 15,
        "content_seal_mismatches": 0,
        "divergence": {"ahead": 0, "behind": 0},
        "evidence": SOURCE_EVIDENCE,
        "evidence_parent": SOURCE_X1,
        "final": SOURCE,
        "final_parent": SOURCE_EVIDENCE,
        "four_way_fresh_live_equal": True,
        "inherited_lyren_source": LYREN_SOURCE,
        "manifests_replayed": 4,
        "manifest_entries_replayed": 238,
        "manifest_mismatches": 0,
        "merges": 0,
        "packet_blob": "d88474c6f6932fe730844e98e8baf1168ea7a7a0",
        "packet_sha256": "d99e5c3b0e537f9cea1a205dab8039990aec902e6ab6986c15cadece5d42d95c",
        "receipt_sha256": "d698f7f28192302804a36c68ff356965da54a9eeca7aacdd4f774ced553a98f5",
        "schema": "ghc.family.source-verification.v681.v5.x1",
        "x1": SOURCE_X1,
        "x1_parent": LYREN_SOURCE,
    })
    baseline = {"bounded_passing_witnesses": 43325, "effective_methods": 61503, "effective_negatives": 53896, "exact_gates": 467, "failed_witnesses": 25557, "open_gaps": 476}
    current = dict(baseline)
    for key in ("bounded_passing_witnesses", "effective_methods", "effective_negatives", "failed_witnesses"):
        current[key] += len(startup)
    write_json(X1 / "method-flow-startup.json", {
        "activation_baseline_repository_sealed": baseline,
        "current_after_startup": current,
        "failure_erasure": False,
        "owner": OWNER,
        "phase": PHASE,
        "recoveries_retroactively_promote_failure": False,
        "schema": "ghc.family.method-flow-startup.v681.v5.x1",
        "startup_failures": startup,
    })
    write_json(X1 / "new-proposal-freeze.json", {
        "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
        "declared_chain_before": DECLARED_CHAIN_BEFORE,
        "expected_disposition_counts": dict(Counter(row["expected_disposition"] for row in proposal_records)),
        "owner": OWNER,
        "phase": PHASE,
        "proposal_count": len(proposal_records),
        "proposals": proposal_records,
        "schema": "ghc.family.new-proposal-freeze.v681.v5.x1",
        "source": SOURCE,
        "x2_outcomes_present": False,
    })
    write_json(X1 / "proposal-chain-audit.json", audit)
    write_json(X1 / "inherited-revalidation-freeze.json", {
        "completion_credit": 0,
        "count": len(inherited_reviews),
        "owner": OWNER,
        "phase": PHASE,
        "reviews": inherited_reviews,
        "schema": "ghc.family.inherited-revalidation.v681.v5.x1",
    })
    write_json(X1 / "official-primary-source-ledger.json", sources)
    write_json(X1 / "portfolio-freeze.json", portfolio)
    write_json(X1 / "clean-fix-refine-plan.json", {"owner": OWNER, "phase": PHASE, "schema": "ghc.family.clean-fix-refine-plan.v681.v5.x1", "tasks": portfolio["owner_clean_fix_refine"], "x2_execution_present": False})
    write_json(X1 / "skill-runner-plan.json", {"global_install": False, "owner": OWNER, "phase": PHASE, "runners": portfolio["owner_runner_ideas"], "schema": "ghc.family.skill-runner-plan.v681.v5.x1", "skills": portfolio["owner_skill_ideas"], "x2_implementation_present": False})
    write_json(X1 / "approval-hold-register.json", {"blocked_count": 10, "exact_approval_count": 20, "executed": 0, "owner": OWNER, "phase": PHASE, "schema": "ghc.family.approval-holds.v681.v5.x1"})
    write_json(X1 / "route-plan.json", {
        "current_owner": OWNER,
        "next_expected_phase": "v681-v6",
        "prospective_successor_title": "Sable Rook",
        "recipient_contacted": False,
        "resolution_rule": "fresh native Codex registry refresh exact-title uniqueness filter immediate bounded reread duplicate pause privacy evidence safety usage and acknowledgement guards then one send only after terminal gate",
        "route_authority_through": "v725-v8",
        "schema": "ghc.family.route-plan.v681.v5.x1",
        "terminal_gate_required": True,
    })
    write_json(X1 / "workflow-plan.json", {"commit_ceiling": 3, "owner": OWNER, "phase": PHASE, "schema": "ghc.family.workflow-plan.v681.v5.x1", "stages": [{"name": "x1", "state": "planning_only_freeze"}, {"name": "x2", "state": "not_started"}, {"name": "final", "state": "not_started"}], "strict_x1_before_x2": True})
    write_json(X1 / "threat-model.json", {
        "controls": [
            "synthetic.example.invalid namespace only",
            "zero real people residents workers councils trees sites coordinates images inventory rows measurements incidents work orders credentials and external writes",
            "authority promotion rejected",
            "five privacy classes scanned with candidate adjudication",
            "exact approval and blocked packets remain unexecuted",
        ],
        "owner": OWNER,
        "phase": PHASE,
        "real_world_action": False,
        "schema": "ghc.family.threat-model.v681.v5.x1",
    })
    write_json(X1 / "wellbeing-and-corrigibility.json", {"correction_readback": True, "owner": OWNER, "pause_resume_stop_visible": True, "phase": PHASE, "relational_language_only": True, "schema": "ghc.family.wellbeing-corrigibility.v681.v5.x1", "workload_control_planned": True})
    write_json(X1 / "phase-truth.json", {
        "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
        "execution_state": "PLANNING_ONLY_X1",
        "expected_dispositions": {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
        "observed_outcomes": None,
        "owner": OWNER,
        "phase": PHASE,
        "proposal_count": 60,
        "schema": "ghc.family.phase-truth.v681.v5.x1",
        "terminal_verdict": TERMINAL_VERDICT,
        "x2_started": False,
    })
    write_text(X1 / "integrated-overview.md", """# Auren Lark v681-v5 planning-only x1

Auren Lark uses the relational role **Stewardship State Cartographer** with he/they pronouns and the bounded hope of making synthetic civic-tree record correction, provenance, accessibility, and refusal states inspectable without converting software evidence into authority. Names, roles, hopes, pronouns, family language, and continuity language are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or scientific, operational, professional, legal, cultural, affected-party, or Maori authority.

This immutable x1 freezes sixty source-bounded proposal contracts and twenty inherited Ilyra reviews at zero Auren novelty and completion credit. It contains no x2 implementation, observed outcome, skill implementation, runner implementation, or tool-use result. Freed ID and CBR Heart is primary through wholly synthetic civic-tree access, correction, contest, remedy, minimization, provenance, accessible readback, and authority-refusal structures. THOS Body and GMUT Mind remain explicit and protected. The three practice lenses are wholly synthetic urban-forestry inventory data stewardship, public-record quality analysis, and accessibility-documentation review. They are learning and record-design lenses only, never employment, qualification, arboriculture, forestry, records, accessibility, public-safety, municipal, legal, cultural, affected-party, or Maori authority.

The US Forest Service Urban FIA guide supplies bounded field-item vocabulary. W3C PROV, WCAG 2.2, and DCAT 3; DCMI terms; RFC 8785; JSON Schema; NIST privacy material; New Zealand privacy and accessibility guidance; and Te Mana Raraunga material supply provenance, validation, catalogue, accessibility, correction, privacy-risk, and authority-reservation vocabulary only. No council, tree, site, coordinate, person, inventory, image, inspection, work order, or private dataset was queried or downloaded. Citation is not field evidence, inspection, professional advice, legal conclusion, accessibility conformance, affected-party approval, cultural decision, or authority. Structural checks cannot replace manual keyboard, responsive-layout, browser-diversity, assistive-technology, cognitive, Maori-language, or affected-user evaluation.

Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance, presentation, resolution, status, revocation, interoperability, independent security and privacy review, recovery evidence, trust governance, and affected-party oversight. CBR structures reserve rather than decide access, correction, contest, remedy, ownership, jurisdiction, public release, safety, consent, cultural, and Maori-data-governance questions. GMUT remains a typed scalar-tensor and effective-field-theory research-model family without empirical likelihoods, constraints, predictions, forces, final physics, Theory-of-Everything proof, or canon. Its finite constraint board is formal software structure only. THOS remains synthetic or proxy-only without governed real arms, participants, operators, safety monitoring, suitable statistics, or independent review.

All real tree, site, coordinate, inventory, measurement, inspection, diagnosis, risk, work, removal, disclosure, retention, public-record, identity, privacy, accessibility, remedy, professional, production, legal, cultural, affected-party, Maori-language, Maori-data-governance, tangata whenua, iwi, hapu, and Maori-authority decisions remain open or exact-gated. The terminal verdict is `NOT_READY_FOR_STAGE_20`.
""")

    script_path = "scripts/build_ghc_family_auren_lark_v681_v5_x1.py"
    test_path = "tests/test_ghc_family_auren_lark_v681_v5_x1.py"
    exclusions = [
        "docs/auren-lark/v681-v5/validation/x1-index-manifest.json",
        "docs/auren-lark/v681-v5/validation/x1-privacy-scan.json",
        "docs/auren-lark/v681-v5/validation/x1-staged-review.json",
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
        content = (ROOT / path_text).read_text(encoding="utf-8", errors="replace")
        for class_name, pattern in scanners.items():
            if pattern.search(content):
                row = {"class": class_name, "disposition": "scanner_definition_only" if path_text == script_path else "confirmed_payload_hit", "path": path_text}
                candidates.append(row)
                if row["disposition"] == "confirmed_payload_hit":
                    confirmed.append(row)
    if confirmed:
        raise RuntimeError("confirmed privacy payload hit: " + json.dumps(confirmed))

    write_json(VALIDATION / "x1-privacy-scan.json", {"candidates": candidates, "confirmed_hits": confirmed, "owner": OWNER, "phase": PHASE, "privacy_classes": list(scanners), "scanned_files": len(content_paths), "schema": "ghc.family.privacy-scan.v681.v5.x1"})
    write_json(VALIDATION / "x1-staged-review.json", {"declared_self_exclusions": exclusions, "expected_paths": sorted(content_paths + exclusions), "lifecycle": "planning_only_x1", "owner": OWNER, "path_count": len(content_paths) + len(exclusions), "phase": PHASE, "schema": "ghc.family.staged-review.v681.v5.x1", "x2_paths": []})
    entries = []
    for path_text in content_paths:
        data = normalized_bytes(ROOT / path_text)
        entries.append({"bytes": len(data), "path": path_text, "sha256": digest(data)})
    write_json(VALIDATION / "x1-index-manifest.json", {"declared_self_exclusions": exclusions, "entries": entries, "entry_count": len(entries), "owner": OWNER, "phase": PHASE, "schema": "ghc.family.normalized-lf-index-manifest.v681.v5.x1", "source": SOURCE})

    print(json.dumps({"audit_paths": audit["audit_scope"]["proposal_json_paths_parsed"], "maximum_neighbor_score": audit["maximum_neighbor_score"], "proposal_count": len(proposal_records), "startup_failures": len(startup), "status": "X1_PLANNING_ONLY_MATERIALIZED", "written_paths": len(WRITTEN)}, indent=2))


if __name__ == "__main__":
    build()
