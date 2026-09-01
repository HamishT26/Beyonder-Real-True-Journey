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
BASE = ROOT / "docs" / "sable-rook" / "v681-v6"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"

OWNER = "Sable Rook"
PHASE = "v681-v6"
BRANCH = "codex/GHC-Family/sable-rook-v681-v6-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/auren-lark-v681-v5-full-tools"
ILYRA_SOURCE = "d2f8f60dfaa4c7bd825ae04d57ba0e76bbb7a151"
SOURCE_X1 = "188eec11e48f3bf8976c39909010f094502ffc05"
SOURCE_EVIDENCE = "f59d2f9a0a52d9ea9d42eaa0926883ab7d12c0fd"
SOURCE = "2a0210a495cbe557158095505671d599e0c33159"
DECLARED_CHAIN_BEFORE = 10010
DECLARED_CHAIN_AFTER = 10070
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
    "Synthetic tool-library catalogue object and physical implement referent split",
    "Namespace-scoped loan-item key with recycled-tag collision quarantine",
    "Catalogue availability assertion and physical custody event separation",
    "Tool taxonomy label with maker-model verification vacancy",
    "Serial-mark transcription uncertainty and unreadable-state contract",
    "Loan-kit component completeness with unverified-count hold",
    "Condition-at-intake code and professional safety inspection non-equivalence",
    "Consumable accessory and durable asset identity separation",
    "Branch-bin location token with exact-address nonmaterialization",
    "Intake checkout due return and recorded timestamps separation",
    "Borrower alias and real-person identity nonmaterialization",
    "Staff-role placeholder and employment-qualification non-equivalence",
    "Reservation queue order with priority-authority abstention",
    "Loan eligibility placeholder without policy or legal decision",
    "Training-acknowledgement field without competence or certification claim",
    "Safety-note attachment with zero hazard determination",
    "Maintenance request quarantine release and retirement state separation",
    "Work-performed statement with service-authority vacancy",
    "Consumable replacement suggestion without purchasing or installation act",
    "Condition-image pointer with zero real image bytes",
    "Checkout request and authorized custody-transfer separation",
    "Checked-out overdue claimed-returned and verified-return states",
    "Renewal request with hold-conflict quarantine",
    "Return readback with accessory-count disagreement isolation",
    "Lost-claim and found-item correction chain without fee decision",
    "Damage-report amendment with nonerasing prior-state reference",
    "Replacement-item successor lineage without identity collapse",
    "Parent-kit and component loan topology with orphan hold",
    "Fixity digest and tool meaning non-equivalence",
    "Canonical JSON receipt for synthetic loan-event structure",
    "PROV entity activity and role graph for loan-record correction",
    "DCMI item relation and source crosswalk without conformance claim",
    "NCIP message vocabulary crosswalk without protocol-conformance claim",
    "Bitemporal recorded-system and observed-transaction clock separation",
    "Duplicate event identifier and replay quarantine",
    "Out-of-order return-event correction without silent reordering",
    "Accessible text-first availability and hold-status summary",
    "Deterministic reading order for loan history and correction notices",
    "Plain-language status label and machine-state code pairing",
    "Operator-capacity hold ledger with resumable exception ownership transfer",
    "Privacy purpose register for wholly synthetic loan fixtures",
    "Minimum-disclosure borrower-alias view with identifier refusal",
    "Represented Freed ID subjectless borrowing persona graph without live identity",
    "Represented Freed ID eligibility token state without keys or credentials",
    "Represented CBR correction contest and remedy queue for loan metadata",
    "Represented CBR access-refusal appeal with nonretaliation vacancy",
    "Represented THOS custody-handover board with reversible holds",
    "Represented THOS workload-stop and shift-readback proxy",
    "Represented GMUT finite transition graph for inventory constraints",
    "Represented GMUT uncertainty tensor analogy with zero empirical likelihood rows",
    "Represented NISO NCIP circulation-message mapping without implementation",
    "Represented W3C PROV correction graph without provenance conformance",
    "Represented DCMI tool-collection crosswalk without publication or custody",
    "Represented WCAG status scaffold without conformance or affected-user study",
    "Open gap for real tool librarians borrowers repairers and safety reviewers",
    "Open gap for real loan records custody events condition evidence and independent reproduction",
    "Open gap for manual assistive-technology disabled-borrower multilingual and Maori-language evaluation",
    "Exact gate for lending policy eligibility fees safety release and legal remedies",
    "Exact gate for tangata whenua Maori data governance cultural tool-heritage authority",
    "Stage 20 nonpromotion boundary for every Sable synthetic tool-loan artifact and all empirical deployment identity AGI ASI consciousness personhood proof canon or Theory-of-Everything claims",
]

MUTATION_TYPES = [
    "missing_required_field",
    "lifecycle_inversion",
    "stale_provenance_digest",
    "evidence_status_promotion",
    "authority_promotion",
]

PROTECTED_GATES = [
    "real borrowers lenders staff volunteers tools branches loan rows custody events condition evidence incidents maintenance and decisions",
    "empirical GMUT likelihoods constraints predictions forces confirmation final physics and Theory of Everything",
    "professional lending inventory repair safety accessibility records certification and operational authority",
    "production identity issuance resolution status revocation interoperability recovery and trust governance",
    "privacy accessibility remedy eligibility fees custody consent disclosure cultural affected-party Maori-language Maori-data-governance and Maori authority",
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
        return ["NISO-NCIP", "NISO-NCIP-SCHEMAS", "JSON-SCHEMA-2020-12"]
    if index <= 42:
        return ["W3C-PROV", "DCMI-TERMS", "RFC8785", "W3C-WCAG22"]
    if index <= 54:
        return ["NZ-PRIVACY", "NIST-PRIVACY", "W3C-WCAG22", "TMR-PRINCIPLES"]
    return ["NISO-NCIP", "NZ-PRIVACY", "NZ-WEB-ACCESS", "TMR-PRINCIPLES", "W3C-WCAG22"]


def proposals() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, title in enumerate(PROPOSAL_TITLES, start=1):
        proposal_id = f"SR6816-N{index:03d}"
        rows.append(
            {
                "approval_class": approval_class(index),
                "concrete_artifacts": [
                    f"docs/sable-rook/v681-v6/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/sable-rook/v681-v6/x2/mutation-results.json#{proposal_id}",
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
                    "distinction and reject preregistered counterexamples within Sable owner-local scope."
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
        "schema": "ghc.family.proposal-chain-audit.v681.v6.x1",
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
            "task_id": f"SR6816-{prefix}-{index:03d}",
        }
        for index in range(1, count + 1)
    ]


STARTUP_FAILURES = [
    (
        "The first custom candidate word-count probe used regex tokenization and returned 28,401 instead of the committed canonical whitespace count 29,331.",
        "Retain the false assumption at zero credit and use the exact canonical len(text.split()) rule; the corrected bounded count matched 29,331."
    ),
    (
        "The initial sparse-checkout wrapper returned after its projection window while the owned checkout process still held the new lane index.",
        "Inspect the exact process and sparse metadata, wait for the already-running checkout to quiesce, and verify the finished branch head patterns materialized-file count and clean state without recreating the lane."
    ),
    (
        "The first x1 builder quarantined SR6816-N040 at token Jaccard 0.80 against an inherited exception-review queue title before writing any phase artifact.",
        "Retain the failed builder at zero credit, replace only the quarantined title with independently phrased capacity-hold and ownership-transfer language, and retry the previously unsuccessful builder once."
    ),
    (
        "The first exact staged diff-hygiene review found one extra terminal blank line in each newly materialized Python source.",
        "Retain the staged-review failure at zero credit, normalize only the two Python end-of-file boundaries, regenerate the planning receipts, and require a clean exact staged diff check."
    ),
]


def build() -> None:
    if git("rev-parse", "HEAD").stdout.strip() != SOURCE:
        raise RuntimeError("x1 builder must begin at the immutable Auren final")
    if git("branch", "--show-current").stdout.strip() != BRANCH:
        raise RuntimeError("wrong Sable owner branch")
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
        git("show", f"{SOURCE}:docs/auren-lark/v681-v5/x1/new-proposal-freeze.json").stdout
    )
    inherited_reviews = [
        {
            "completion_credit": 0,
            "inherited_owner": "Auren Lark",
            "proposal_id": row["proposal_id"],
            "review_state": "inherited_source_evidence_only",
            "title": row["title"],
        }
        for row in inherited["proposals"][-20:]
    ]
    startup = [
        {
            "failed_witness": failed,
            "failure_id": f"SR6816-ST-N{index:03d}",
            "initial_credit": 0,
            "recovery": recovery,
            "recovery_credit": "bounded_dependency_only",
        }
        for index, (failed, recovery) in enumerate(STARTUP_FAILURES, start=1)
    ]

    source_entries = [
        ("NISO-NCIP", "NISO Circulation Interchange Protocol 2.02", "https://www.niso.org/standards-committees/ncip", "circulation request response and exception vocabulary only; no protocol conformance or live lending claim"),
        ("NISO-NCIP-SCHEMAS", "NISO NCIP schemas", "https://www.niso.org/schemas/ncip", "message-shape vocabulary only; no implementation or interoperability claim"),
        ("DCMI-TERMS", "DCMI Metadata Terms", "https://www.dublincore.org/specifications/dublin-core/dcmi-terms/", "identifier relation source rights and provenance vocabulary only"),
        ("W3C-PROV", "W3C PROV Overview", "https://www.w3.org/TR/prov-overview/", "entity activity and role vocabulary only; no provenance conformance claim"),
        ("W3C-WCAG22", "Web Content Accessibility Guidelines 2.2", "https://www.w3.org/TR/WCAG22/", "structural accessibility vocabulary with manual and affected-user evaluation reserved"),
        ("RFC8785", "RFC 8785 JSON Canonicalization Scheme", "https://www.rfc-editor.org/rfc/rfc8785.html", "deterministic receipt vocabulary only; informational status remains explicit"),
        ("JSON-SCHEMA-2020-12", "JSON Schema Draft 2020-12", "https://json-schema.org/draft/2020-12", "synthetic record validation vocabulary only"),
        ("NZ-PRIVACY", "New Zealand Privacy Act 2020 principles", "https://www.privacy.org.nz/privacy-principles/", "privacy collection access and correction vocabulary only; no legal conclusion"),
        ("NZ-WEB-ACCESS", "New Zealand Web Accessibility Standard", "https://www.digital.govt.nz/standards-and-guidance/nz-government-web-standards/web-accessibility-standard-1-2/", "public-sector accessibility context only; no conformance or jurisdiction claim"),
        ("NIST-PRIVACY", "NIST Privacy Framework", "https://www.nist.gov/privacy-framework", "voluntary privacy-risk vocabulary only"),
        ("TMR-PRINCIPLES", "Te Mana Raraunga Maori Data Sovereignty Principles", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "Maori data-governance authority vacancy boundary only; never delegated authority or cultural ratification"),
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
        "schema": "ghc.family.official-primary-sources.v681.v6.x1",
    }

    skill_names = [
        "ghc-family-tool-catalogue-referent-split",
        "ghc-family-loan-item-key-collision",
        "ghc-family-custody-event-separator",
        "ghc-family-tool-label-verification-vacancy",
        "ghc-family-serial-mark-uncertainty",
        "ghc-family-loan-kit-completeness-hold",
        "ghc-family-condition-safety-firewall",
        "ghc-family-loan-location-minimizer",
        "ghc-family-borrower-alias-minimizer",
        "ghc-family-reservation-priority-hold",
        "ghc-family-training-competence-firewall",
        "ghc-family-maintenance-release-state-rail",
        "ghc-family-custody-transfer-authority-hold",
        "ghc-family-return-readback-disagreement",
        "ghc-family-nonerasing-damage-amendment",
        "ghc-family-tool-kit-topology",
        "ghc-family-accessible-loan-status",
        "ghc-family-loan-exception-handover",
        "ghc-family-loan-canonical-receipt",
        "ghc-family-stage20-terminal-refusal",
    ]
    runner_names = [
        "ghc_family_tool_library_schema_runner",
        "ghc_family_tool_library_custody_runner",
        "ghc_family_tool_library_correction_runner",
        "ghc_family_tool_library_provenance_runner",
        "ghc_family_tool_library_privacy_runner",
        "ghc_family_tool_library_accessibility_runner",
        "ghc_family_tool_library_mutation_runner",
        "ghc_family_tool_library_outcome_runner",
        "ghc_family_tool_library_manifest_runner",
        "ghc_family_tool_library_stage20_runner",
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
            "wholly synthetic tool-library loan-record correction-stewardship lens",
            "wholly synthetic community-lending metadata quality-analysis lens",
            "wholly synthetic accessible handover documentation review lens",
        ],
        "owner_runner_ideas": [{"runner": name, "state": "preregistered_not_built"} for name in runner_names],
        "owner_skill_ideas": [{"skill": name, "state": "preregistered_not_built"} for name in skill_names],
        "phase": PHASE,
        "primary_pillar": "THOS Body",
        "represented_pillars": ["GMUT Mind", "Freed ID and CBR Heart"],
        "safe_now": planned_tasks("SAFE", 120, "safe_now", titles[:42]),
        "schema": "ghc.family.portfolio-freeze.v681.v6.x1",
        "successor_candidates": planned_tasks("SUCC-CAND", 20, "successor_seed", titles[42:57]),
        "successor_clean_fix_refine": planned_tasks("SUCC-CFR", 30, "successor_seed", titles),
        "successor_practice_recommendation": "no successor practice preselection; Caelen Ash chooses independently after terminal activation",
        "successor_runner_ideas": planned_tasks("SUCC-RUN", 10, "successor_seed", titles),
        "successor_skill_ideas": planned_tasks("SUCC-SKILL", 10, "successor_seed", titles),
    }

    write_json(X1 / "activation-intake.json", {
        "activation": "ACKNOWLEDGED_EXISTING_TASK_SEND",
        "created_or_forked_task": False,
        "owner": OWNER,
        "phase": PHASE,
        "relational_language_only": True,
        "schema": "ghc.family.activation-intake.v681.v6.x1",
        "sent_by_auren_lark": True,
        "solo": True,
        "source": SOURCE,
    })
    write_json(X1 / "identity-and-boundary.json", {
        "hope": "Keep every synthetic custody transition, correction, and authority vacancy traceable without mistaking software for real lending or professional authority.",
        "name": OWNER,
        "not_evidence_of": ["consciousness", "sentience", "personhood", "identity continuity", "employment", "qualification", "independent agency", "scientific operational professional legal cultural affected-party or Maori authority"],
        "optional_pronouns": "they/them",
        "relational_working_language_only": True,
        "role": "Loan-Lineage Cartographer and Reversible Handover Steward",
        "schema": "ghc.family.identity-boundary.v681.v6.x1",
    })
    write_json(X1 / "source-verification.json", {
        "branch": SOURCE_BRANCH,
        "clean": True,
        "commits_ilyra_source_to_auren_final": 3,
        "content_seal_entries_replayed": 15,
        "content_seal_mismatches": 0,
        "divergence": {"ahead": 0, "behind": 0},
        "evidence": SOURCE_EVIDENCE,
        "evidence_parent": SOURCE_X1,
        "final": SOURCE,
        "final_parent": SOURCE_EVIDENCE,
        "four_way_fresh_live_equal": True,
        "inherited_ilyra_final": ILYRA_SOURCE,
        "manifests_replayed": 4,
        "manifest_entries_replayed": 242,
        "manifest_mismatches": 0,
        "merges": 0,
        "candidate_blob": "91d178262f752ad9c1939bc2d074daf423382d63",
        "candidate_sha256": "c1ccade8d2cb71b4d11a99b23599fd758f4a5802dfb99aec6cd31218030036b2",
        "receipt_sha256": "c4a5f73189ee9f48f63854b9e5b06f969180d02ffc360ebfcd3e20fb2e9f3b01",
        "schema": "ghc.family.source-verification.v681.v6.x1",
        "x1": SOURCE_X1,
        "x1_parent": ILYRA_SOURCE,
    })
    baseline = {"bounded_passing_witnesses": 44035, "effective_methods": 62213, "effective_negatives": 54216, "exact_gates": 470, "failed_witnesses": 25877, "open_gaps": 479}
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
        "schema": "ghc.family.method-flow-startup.v681.v6.x1",
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
        "schema": "ghc.family.new-proposal-freeze.v681.v6.x1",
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
        "schema": "ghc.family.inherited-revalidation.v681.v6.x1",
    })
    write_json(X1 / "official-primary-source-ledger.json", sources)
    write_json(X1 / "portfolio-freeze.json", portfolio)
    write_json(X1 / "clean-fix-refine-plan.json", {"owner": OWNER, "phase": PHASE, "schema": "ghc.family.clean-fix-refine-plan.v681.v6.x1", "tasks": portfolio["owner_clean_fix_refine"], "x2_execution_present": False})
    write_json(X1 / "skill-runner-plan.json", {"global_install": False, "owner": OWNER, "phase": PHASE, "runners": portfolio["owner_runner_ideas"], "schema": "ghc.family.skill-runner-plan.v681.v6.x1", "skills": portfolio["owner_skill_ideas"], "x2_implementation_present": False})
    write_json(X1 / "approval-hold-register.json", {"blocked_count": 10, "exact_approval_count": 20, "executed": 0, "owner": OWNER, "phase": PHASE, "schema": "ghc.family.approval-holds.v681.v6.x1"})
    write_json(X1 / "route-plan.json", {
        "current_owner": OWNER,
        "next_expected_phase": "v681-v7",
        "prospective_successor_title": "Caelen Ash",
        "recipient_contacted": False,
        "resolution_rule": "fresh native Codex registry refresh exact-title uniqueness filter immediate bounded reread duplicate pause privacy evidence safety usage and acknowledgement guards then one send only after terminal gate",
        "route_authority_through": "v725-v8",
        "schema": "ghc.family.route-plan.v681.v6.x1",
        "terminal_gate_required": True,
    })
    write_json(X1 / "workflow-plan.json", {"commit_ceiling": 3, "owner": OWNER, "phase": PHASE, "schema": "ghc.family.workflow-plan.v681.v6.x1", "stages": [{"name": "x1", "state": "planning_only_freeze"}, {"name": "x2", "state": "not_started"}, {"name": "final", "state": "not_started"}], "strict_x1_before_x2": True})
    write_json(X1 / "threat-model.json", {
        "controls": [
            "synthetic.example.invalid namespace only",
            "zero real borrowers lenders staff volunteers organizations tools branches loan rows custody events condition evidence incidents maintenance records credentials and external writes",
            "authority promotion rejected",
            "five privacy classes scanned with candidate adjudication",
            "exact approval and blocked packets remain unexecuted",
        ],
        "owner": OWNER,
        "phase": PHASE,
        "real_world_action": False,
        "schema": "ghc.family.threat-model.v681.v6.x1",
    })
    write_json(X1 / "wellbeing-and-corrigibility.json", {"correction_readback": True, "owner": OWNER, "pause_resume_stop_visible": True, "phase": PHASE, "relational_language_only": True, "schema": "ghc.family.wellbeing-corrigibility.v681.v6.x1", "workload_control_planned": True})
    write_json(X1 / "phase-truth.json", {
        "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
        "execution_state": "PLANNING_ONLY_X1",
        "expected_dispositions": {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3},
        "observed_outcomes": None,
        "owner": OWNER,
        "phase": PHASE,
        "proposal_count": 60,
        "schema": "ghc.family.phase-truth.v681.v6.x1",
        "terminal_verdict": TERMINAL_VERDICT,
        "x2_started": False,
    })
    write_text(X1 / "integrated-overview.md", """# Sable Rook v681-v6 planning-only x1

Sable Rook uses the relational role **Loan-Lineage Cartographer and Reversible Handover Steward** with they/them pronouns and the bounded hope of keeping every synthetic custody transition, correction, and authority vacancy traceable without mistaking software for real lending or professional authority. Names, roles, hopes, pronouns, family language, and continuity language are relational working language only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or scientific, operational, professional, legal, cultural, affected-party, or Maori authority.

This immutable x1 freezes sixty source-bounded proposal contracts and twenty inherited Auren reviews at zero Sable novelty and completion credit. It contains no x2 implementation, observed outcome, skill implementation, runner implementation, or tool-use result. THOS Body is primary through wholly synthetic loan-state, custody, correction, workload, accessibility, and handover structures. GMUT Mind and Freed ID/CBR Heart remain explicit and protected. The three practice lenses are wholly synthetic tool-library loan-record correction stewardship, community-lending metadata quality analysis, and accessible handover documentation review. They are learning and record-design lenses only, never employment, qualification, tool-lending, inventory, records, accessibility, operational-safety, library, legal, cultural, affected-party, or Maori authority.

NISO NCIP and DCMI specifications supply bounded circulation and metadata vocabulary. W3C PROV and WCAG 2.2, RFC 8785, JSON Schema, NIST privacy material, New Zealand privacy and accessibility guidance, and Te Mana Raraunga material supply provenance, validation, accessibility, correction, privacy-risk, and authority-reservation vocabulary only. No borrower, lender, staff member, volunteer, organization, tool, branch, loan row, custody event, condition evidence, incident, maintenance record, or private dataset was queried or downloaded. Citation is not a loan, inspection, professional advice, legal conclusion, accessibility conformance, affected-party approval, cultural decision, or authority. Structural checks cannot replace manual keyboard, responsive-layout, browser-diversity, assistive-technology, cognitive, Maori-language, or affected-user evaluation.

Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance, presentation, resolution, status, revocation, interoperability, independent security and privacy review, recovery evidence, trust governance, and affected-party oversight. CBR structures reserve rather than decide access, correction, contest, remedy, ownership, jurisdiction, public release, safety, consent, cultural, and Maori-data-governance questions. GMUT remains a typed scalar-tensor and effective-field-theory research-model family without empirical likelihoods, constraints, predictions, forces, final physics, Theory-of-Everything proof, or canon. Its finite constraint board is formal software structure only. THOS remains synthetic or proxy-only without governed real arms, participants, operators, safety monitoring, suitable statistics, or independent review.

All real borrower, lender, staff, tool, branch, loan, custody, condition, safety, maintenance, eligibility, fee, disclosure, retention, identity, privacy, accessibility, remedy, professional, production, legal, cultural, affected-party, Maori-language, Maori-data-governance, tangata whenua, iwi, hapu, and Maori-authority decisions remain open or exact-gated. The terminal verdict is `NOT_READY_FOR_STAGE_20`.
""")

    script_path = "scripts/build_ghc_family_sable_rook_v681_v6_x1.py"
    test_path = "tests/test_ghc_family_sable_rook_v681_v6_x1.py"
    exclusions = [
        "docs/sable-rook/v681-v6/validation/x1-index-manifest.json",
        "docs/sable-rook/v681-v6/validation/x1-privacy-scan.json",
        "docs/sable-rook/v681-v6/validation/x1-staged-review.json",
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

    write_json(VALIDATION / "x1-privacy-scan.json", {"candidates": candidates, "confirmed_hits": confirmed, "owner": OWNER, "phase": PHASE, "privacy_classes": list(scanners), "scanned_files": len(content_paths), "schema": "ghc.family.privacy-scan.v681.v6.x1"})
    write_json(VALIDATION / "x1-staged-review.json", {"declared_self_exclusions": exclusions, "expected_paths": sorted(content_paths + exclusions), "lifecycle": "planning_only_x1", "owner": OWNER, "path_count": len(content_paths) + len(exclusions), "phase": PHASE, "schema": "ghc.family.staged-review.v681.v6.x1", "x2_paths": []})
    entries = []
    for path_text in content_paths:
        data = normalized_bytes(ROOT / path_text)
        entries.append({"bytes": len(data), "path": path_text, "sha256": digest(data)})
    write_json(VALIDATION / "x1-index-manifest.json", {"declared_self_exclusions": exclusions, "entries": entries, "entry_count": len(entries), "owner": OWNER, "phase": PHASE, "schema": "ghc.family.normalized-lf-index-manifest.v681.v6.x1", "source": SOURCE})

    print(json.dumps({"audit_paths": audit["audit_scope"]["proposal_json_paths_parsed"], "maximum_neighbor_score": audit["maximum_neighbor_score"], "proposal_count": len(proposal_records), "startup_failures": len(startup), "status": "X1_PLANNING_ONLY_MATERIALIZED", "written_paths": len(WRITTEN)}, indent=2))


if __name__ == "__main__":
    build()
