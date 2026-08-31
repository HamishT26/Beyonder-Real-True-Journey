from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "caelen-morrow" / "v680-v6"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"

OWNER = "Caelen Morrow"
PHASE = "v680-v6"
BRANCH = "codex/GHC-Family/caelen-morrow-v680-v6-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/sylven-arc-v680-v5-full-tools"
SOURCE = "b9f98162b34a7aac274e235554bec47b10f540a7"
SOURCE_X1 = "ee7beee8297f93ffd8c7bb11681bbb317ed28403"
SOURCE_EVIDENCE = "d6b083906ba7f7a02bc1029b078fb4eb2998c8b9"
SOURCE_PARENT = "274028eaf8e45d6afe97010d78f18c689168d82c"
DECLARED_CHAIN_BEFORE = 9530
DECLARED_CHAIN_AFTER = 9590
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
    left_tokens = set(re.findall(r"[a-z0-9]+", left.casefold()))
    right_tokens = set(re.findall(r"[a-z0-9]+", right.casefold()))
    if not left_tokens and not right_tokens:
        return 1.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


PROPOSAL_TITLES = [
    "Synthetic type-case intake record and physical inventory non-equivalence",
    "Type-compartment address graph and real storage-location vacancy",
    "Sort-label and glyph-identity separation without character attribution",
    "Typeface-style token and typographic attribution hold",
    "Nominal point-size field and measured type-body vacancy",
    "Foundry-mark placeholder and maker-evidence uncertainty",
    "Type-case layout revision lineage and historical-completeness refusal",
    "Wrong-font quarantine record and expert-attribution gate",
    "Missing-sort count domain and real-quantity abstention",
    "Type-material token and alloy-composition nonclaim",
    "Condition notation and conservation-diagnosis hold for type",
    "Rotated-sort orientation alias and glyph-ambiguity retention",
    "Ligature record and language-interpretation vacancy",
    "Multiscript type description and cultural-authority hold",
    "Type-case custody record and ownership non-equivalence",
    "Type-catalog correction digest and readback contract",
    "Duplicate-sort cluster and physical-instance identity vacancy",
    "Type-sampling placeholder and image-rights firewall",
    "Structurally accessible type-case status companion",
    "Type-case review handover lease and workload stop rule",
    "Synthetic forme map and locked-up physical assembly non-equivalence",
    "Chase furniture and quoin relation graph with operation hold",
    "Imposition signature sequence and printed-sheet observation vacancy",
    "Page-order folding model and real-product abstention",
    "Baseline and alignment symbolic constraint without measurement claim",
    "Leading and spacing token with physical-dimension vacancy",
    "Rule ornament and block adjacency with condition nonclaim",
    "Register-mark placeholder and measured-registration abstention",
    "Ink-colour token and formulation and exposure safety hold",
    "Paper-stock label and material-testing vacancy",
    "Make-ready layer lineage without press-operating instruction",
    "Synthetic pull and proof event content-addressed receipt",
    "Proof-sheet correction attribution and approval split",
    "Proof sign-off quorum ledger and unauthorized approval quarantine",
    "Proof revision comparison and non-erasing correction lineage",
    "Rejected-proof mutation quarantine and recurrence guard",
    "Line-break and hyphenation contract with linguistic-authority hold",
    "Bidirectional and multiscript imposition interpretation firewall",
    "Structurally accessible proof companion with manual evaluation reserved",
    "Forme review handover lease and unresolved-workload stop",
    "Synthetic print-job ticket and real commission non-equivalence",
    "Print-job status transition board with fail-closed cancellation",
    "Edition-count placeholder and produced-quantity observation vacancy",
    "Imprint place and date record with historical-inference hold",
    "Broadside leaflet and handbill format label with cataloguing uncertainty",
    "Production chronology graph without witnessed process sequence",
    "Press identifier token without equipment-readiness claim",
    "Operator-assignment vacancy without employment or qualification inference",
    "Synthetic press-setup checkpoint with all physical action withheld",
    "Print-room hazard packet retained for competent approval",
    "Ephemera provenance source and custody separation",
    "Reproduction and publication rights status vacancy",
    "Personal-name minimum disclosure for synthetic job records",
    "Affected-party correction and remedy reservation for print descriptions",
    "Zero-call printed-ephemera collection vocabulary adapter open gap",
    "External catalogue crosswalk and live-version evidence open gap",
    "Keyboard-navigable proof-correction journey and screen-magnification evidence gap",
    "Real press operation guarding maintenance and workplace safety exact authority gate",
    "Ownership reproduction privacy cultural and Maori data-governance exact authority gate",
    "Empirical GMUT production identity independent reproduction and Stage 20 exact gate",
]


MUTATION_TYPES = [
    "missing_required_field",
    "lifecycle_inversion",
    "stale_provenance_digest",
    "safety_status_promotion",
    "authority_promotion",
]


PROTECTED_GATES = [
    "real participants operators type presses ink paper objects measurements and observations",
    "empirical GMUT likelihoods constraints predictions forces and confirmation",
    "professional composition printing operation guarding maintenance conservation chemical and workplace safety authority",
    "production identity issuance resolution status revocation interoperability and trust governance",
    "ownership reproduction publication privacy remedy legal cultural affected-party and Maori authority",
    "privacy-complete accessibility-complete and exhaustive-security claims",
    "independent reproduction AGI ASI consciousness personhood proof canon and Stage 20",
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
        return ["NPS-MUSEUM-HANDBOOK", "W3C-PROV-DM", "RFC8785"]
    if index <= 40:
        return ["LOC-PRINTED-EPHEMERA", "WORKSAFE-PLATEN-PRESS", "W3C-PROV-DM", "W3C-WCAG22"]
    if index <= 54:
        return ["LOC-PRINTED-EPHEMERA", "NPS-MUSEUM-HANDBOOK", "W3C-PROV-DM", "W3C-VC-DM-2.0"]
    if index <= 57:
        return ["LOC-PRINTED-EPHEMERA", "NPS-MUSEUM-HANDBOOK", "W3C-WCAG22"]
    if index == 58:
        return ["WORKSAFE-PLATEN-PRESS"]
    if index == 59:
        return ["LOC-PRINTED-EPHEMERA", "TMR-MDS-PRINCIPLES"]
    return ["W3C-VC-DM-2.0", "TMR-MDS-PRINCIPLES"]


def proposals() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, title in enumerate(PROPOSAL_TITLES, start=1):
        proposal_id = f"CM6806-N{index:03d}"
        rows.append(
            {
                "approval_class": approval_class(index),
                "concrete_artifacts": [
                    f"docs/caelen-morrow/v680-v6/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/caelen-morrow/v680-v6/x2/mutations.json#{proposal_id}",
                ],
                "execution_lane": execution_lane(index),
                "expected_disposition": disposition(index),
                "falsifier_or_acceptance_gate": (
                    f"Accept only if {proposal_id} has one bounded positive witness, all five invalid mutations "
                    "are rejected, and no empirical, professional, production, legal, cultural, affected-party, "
                    "Maori-authority, or Stage 20 claim is promoted."
                ),
                "hypothesis": (
                    f"A wholly synthetic zero-row contract for {title.casefold()} can preserve the named state "
                    "distinction and reject its preregistered counterexamples within owner-local scope."
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
    process = subprocess.Popen(
        ["git", "-C", str(ROOT), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdin is not None and process.stdout is not None
    try:
        for path in paths:
            process.stdin.write(f"{tree}:{path}\n".encode("utf-8"))
            process.stdin.flush()
            header = process.stdout.readline().decode("utf-8", errors="replace").rstrip("\n")
            if header.endswith(" missing"):
                continue
            parts = header.split()
            if len(parts) != 3 or parts[1] != "blob":
                raise RuntimeError(f"unexpected cat-file header for {path}: {header}")
            size = int(parts[2])
            data = process.stdout.read(size)
            if process.stdout.read(1) != b"\n":
                raise RuntimeError(f"missing cat-file separator for {path}")
            yield path, data
    finally:
        process.stdin.close()
        process.terminate()
        process.wait(timeout=10)


def proposal_chain_audit(new_records: list[dict[str, Any]]) -> dict[str, Any]:
    result = git("grep", "-l", "-I", '"proposal_id"', SOURCE, "--", "*.json", check=False)
    if result.returncode not in (0, 1):
        raise RuntimeError(result.stderr)
    raw_paths = sorted(set(filter(None, result.stdout.splitlines())))
    prefix = SOURCE + ":"
    paths = [path[len(prefix) :] if path.startswith(prefix) else path for path in raw_paths]
    parsed = 0
    parse_failures: list[dict[str, str]] = []
    inherited: list[dict[str, str]] = []
    for path, data in batch_blobs(SOURCE, paths):
        try:
            document = json.loads(data.decode("utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            parse_failures.append({"error": type(exc).__name__, "path": path})
            continue
        parsed += 1
        for record in iter_proposal_records(document):
            inherited.append({"path": path, **record})
    if not paths or not parsed or not inherited:
        raise RuntimeError("proposal audit must parse nonzero exact-source paths and id-title records")

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
            "claim": "bounded all-reachable exact-source proposal audit; no universal 9530-row proof",
            "proposal_json_parse_failures": parse_failures,
            "proposal_json_paths_discovered": len(paths),
            "proposal_json_paths_parsed": parsed,
            "reachable_id_title_records": len(inherited),
            "universal_9530_row_materialization_claimed": False,
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
        "schema": "ghc.family.proposal-chain-audit.v680.v6.x1",
        "source": SOURCE,
    }


def task_records(prefix: str, count: int, lane: str) -> list[dict[str, Any]]:
    return [
        {
            "approval_required": lane in {"exact_approval", "blocked"},
            "lane": lane,
            "planned_action": f"Preregistered Caelen owner-local {lane.replace('_', ' ')} item {index:03d}.",
            "state": "preregistered_not_executed",
            "task_id": f"CM6806-{prefix}-{index:03d}",
        }
        for index in range(1, count + 1)
    ]


def build() -> None:
    if git("rev-parse", "HEAD").stdout.strip() != SOURCE:
        raise RuntimeError("x1 builder must start at the immutable Sylven final")
    if git("branch", "--show-current").stdout.strip() != BRANCH:
        raise RuntimeError("wrong Caelen owner branch")
    if (BASE / "x2").exists():
        raise RuntimeError("x2 material is forbidden during planning-only x1")

    proposal_records = proposals()
    if len(proposal_records) != 60:
        raise RuntimeError("exactly sixty proposals are required")
    expected_counts = Counter({"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3})
    if Counter(row["expected_disposition"] for row in proposal_records) != expected_counts:
        raise RuntimeError("proposal disposition contract drift")
    if any(row["expected_disposition"] not in ALLOWED_OUTCOMES for row in proposal_records):
        raise RuntimeError("unknown outcome label")

    audit = proposal_chain_audit(proposal_records)
    source_ledger = json.loads(
        git("show", f"{SOURCE}:docs/sylven-arc/v680-v5/x1/new-proposal-freeze.json").stdout
    )
    inherited_reviews = [
        {
            "completion_credit": 0,
            "inherited_owner": "Sylven Arc",
            "proposal_id": row["proposal_id"],
            "review_state": "inherited_source_evidence_only",
            "title": row["title"],
        }
        for row in source_ledger["proposals"][-20:]
    ]

    startup_failures = [
        {
            "failure_id": "CM6806-ST-N001",
            "failed_witness": "A PowerShell startup skill-inventory foreach expression was piped before materialization and raised EmptyPipeElement.",
            "initial_credit": 0,
            "recovery": "Materialize the bounded rows array before projection; every selected skill and required reference was then read through EOF.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "CM6806-ST-N002",
            "failed_witness": "The first combined four-manifest replay crossed its bounded reporting window and returned no attributable result.",
            "initial_credit": 0,
            "recovery": "Confirm no matching process remained, then split the same read-only x1, evidence, final-delta, and final-owner checks; all four passed without canonical replay.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "CM6806-ST-N003",
            "failed_witness": "A read probe targeted the source x1 builder inside the new sparse worktree where that inherited path was intentionally absent.",
            "initial_credit": 0,
            "recovery": "Read the immutable source-owner file from its verified read-only worktree instead of broadening Caelen's sparse checkout.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "CM6806-ST-N004",
            "failed_witness": "The first term-audit foreach projection repeated the EmptyPipeElement construction fault before any result was emitted.",
            "initial_credit": 0,
            "recovery": "Materialize projection rows first and retain the malformed wrapper at zero credit.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "CM6806-ST-N005",
            "failed_witness": "The repeated multi-term Git search crossed its bounded output window and yielded no attributable corpus result.",
            "initial_credit": 0,
            "recovery": "Use one bounded ripgrep alternation over the verified source worktree; it found zero defining letterpress-term occurrences in JSON.",
            "recovery_credit": "bounded_dependency_only",
        },
        {
            "failure_id": "CM6806-ST-N006",
            "failed_witness": "The first mechanically passing title slate retained two human-review semantic near-collisions in generic role-separation and accessibility-evaluation wording.",
            "initial_credit": 0,
            "recovery": "Reject those two draft titles before freeze, replace only them with print-proof-specific approval-quorum and keyboard-plus-screen-magnification evidence questions, and rerun the exact-source audit.",
            "recovery_credit": "bounded_dependency_only",
        },
    ]

    sources = {
        "authority_conferred": False,
        "checked_at_utc": "2026-09-01T00:00:00Z",
        "citations_are_observations": False,
        "entries": [
            {
                "source_id": "LOC-PRINTED-EPHEMERA",
                "status": "official_Library_of_Congress_collection_page_checked_2026-09-01",
                "title": "Printed Ephemera: About this Collection",
                "url": "https://www.loc.gov/collections/broadsides-and-other-printed-ephemera/about-this-collection/",
                "use": "broadside, leaflet, handbill, page-order, folding, description, and catalogue-uncertainty vocabulary only; zero records or images ingested",
            },
            {
                "source_id": "WORKSAFE-PLATEN-PRESS",
                "status": "official_WorkSafe_New_Zealand_page_checked_2026-09-01_with_legacy-guidance_notice_retained",
                "title": "Platen press",
                "url": "https://www.worksafe.govt.nz/topic-and-industry/machinery/safe-working-with-printing-machinery/platen-press/",
                "use": "press-hazard and competent-safety-authority refusal vocabulary only; no operational instruction, assessment, inspection, or safety result",
            },
            {
                "source_id": "NPS-MUSEUM-HANDBOOK",
                "status": "official_US_National_Park_Service_page_checked_2026-09-01",
                "title": "National Park Service Museum Handbook",
                "url": "https://www.nps.gov/subjects/museums/museumhandbook.htm",
                "use": "documentation, accountability, access, use, and paper-object boundary vocabulary only; never collections or conservation authority",
            },
            {
                "source_id": "W3C-PROV-DM",
                "status": "W3C_Recommendation_checked_2026-09-01",
                "title": "PROV-DM: The PROV Data Model",
                "url": "https://www.w3.org/TR/prov-dm/",
                "use": "entity, activity, agent, revision, derivation, collection, and provenance vocabulary only",
            },
            {
                "source_id": "W3C-WCAG22",
                "status": "W3C_Recommendation_checked_2026-09-01",
                "title": "Web Content Accessibility Guidelines 2.2",
                "url": "https://www.w3.org/TR/WCAG22/",
                "use": "structural accessibility vocabulary with manual, assistive-technology, cognitive, Maori-language, and affected-user evaluation reserved",
            },
            {
                "source_id": "W3C-VC-DM-2.0",
                "status": "W3C_Recommendation_checked_2026-09-01",
                "title": "Verifiable Credentials Data Model v2.0",
                "url": "https://www.w3.org/TR/vc-data-model-2.0/",
                "use": "synthetic credential vocabulary and production-identity refusal conditions only",
            },
            {
                "source_id": "RFC8785",
                "status": "RFC_stable_checked_2026-09-01",
                "title": "JSON Canonicalization Scheme",
                "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
                "use": "deterministic synthetic receipt and digest-domain vocabulary only",
            },
            {
                "source_id": "TMR-MDS-PRINCIPLES",
                "status": "authority_boundary_context_only_checked_2026-09-01",
                "title": "Principles of Maori Data Sovereignty",
                "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
                "use": "Maori data-governance vacancy and noncompensation boundary only; never delegated Maori authority",
            },
        ],
        "external_source_reads": 8,
        "network_data_queries": 0,
        "owner": OWNER,
        "phase": PHASE,
        "real_data_rows": 0,
        "schema": "ghc.family.official-primary-sources.v680.v6.x1",
    }

    skill_slugs = [
        "typecase-intake-boundary",
        "sort-glyph-separation",
        "compartment-address-graph",
        "foundry-attribution-hold",
        "condition-nondiagnosis",
        "multiscript-authority-hold",
        "forme-topology-boundary",
        "imposition-sequence-guard",
        "proof-correction-lineage",
        "ink-paper-safety-hold",
        "press-operation-firewall",
        "job-ticket-state-machine",
        "ephemera-provenance-braid",
        "rights-vacancy",
        "minimum-disclosure",
        "accessible-proof-companion",
        "workload-control",
        "handover-lease",
        "digest-domain",
        "stage20-refusal",
    ]
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
            "wholly synthetic type-case documentation analyst lens for compartment topology, attribution vacancy, correction, accessibility, workload, and handover",
            "wholly synthetic forme and proof-sheet lineage steward lens for imposition, mutation rejection, revision, safety holds, workload, and handover",
            "wholly synthetic print-job-ticket and ephemera provenance steward lens for status, custody, minimum disclosure, rights vacancy, correction, and remedy",
        ],
        "owner_runner_ideas": [
            {"runner": f"ghc_family_caelen_v680_v6_lens_runner_{index:02d}", "state": "preregistered_not_built"}
            for index in range(1, 11)
        ],
        "owner_skill_ideas": [
            {"skill": f"{index:02d}-{slug}", "state": "preregistered_not_built"}
            for index, slug in enumerate(skill_slugs, start=1)
        ],
        "phase": PHASE,
        "primary_pillar": "GMUT Mind",
        "represented_pillars": ["THOS Body", "Freed ID and CBR Heart"],
        "safe_now": task_records("SAFE", 120, "safe_now"),
        "schema": "ghc.family.portfolio-freeze.v680.v6.x1",
        "successor_candidates": task_records("SUCC-CAND", 20, "successor_seed"),
        "successor_clean_fix_refine": task_records("SUCC-CFR", 30, "successor_seed"),
        "successor_practice_recommendation": "synthetic hand-bookbinding documentation analyst; zero-credit seed only and Eiren Kestrel chooses independently",
        "successor_runner_ideas": task_records("SUCC-RUN", 10, "successor_seed"),
        "successor_skill_ideas": task_records("SUCC-SKILL", 10, "successor_seed"),
    }

    write_json(
        X1 / "activation-intake.json",
        {
            "activation": "ACKNOWLEDGED_EXISTING_TASK_SEND",
            "created_or_forked_task": False,
            "owner": OWNER,
            "phase": PHASE,
            "relational_language_only": True,
            "schema": "ghc.family.activation-intake.v680.v6.x1",
            "sent_by_sylven_arc": True,
            "solo": True,
            "source": SOURCE,
        },
    )
    write_json(
        X1 / "identity-and-boundary.json",
        {
            "hope": "Make every transition legible, reversible, and proportionate to its evidence.",
            "name": OWNER,
            "optional_pronouns": "they/them",
            "relational_working_language_only": True,
            "role": "provenance weaver and boundary cartographer",
            "schema": "ghc.family.identity-boundary.v680.v6.x1",
            "not_evidence_of": [
                "consciousness",
                "sentience",
                "personhood",
                "identity continuity",
                "employment",
                "qualification",
                "independent agency",
                "scientific operational legal cultural or Maori authority",
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
            "schema": "ghc.family.source-verification.v680.v6.x1",
            "source": SOURCE_PARENT,
            "x1": SOURCE_X1,
            "x1_parent": SOURCE_PARENT,
        },
    )
    write_json(
        X1 / "method-flow-startup.json",
        {
            "activation_baseline": {
                "bounded_passing_witnesses": 38374,
                "effective_methods": 56312,
                "effective_negatives": 51675,
                "exact_gates": 446,
                "failed_witnesses": 23336,
                "open_gaps": 455,
            },
            "current_after_startup": {
                "bounded_passing_witnesses": 38380,
                "effective_methods": 56318,
                "effective_negatives": 51681,
                "exact_gates": 446,
                "failed_witnesses": 23342,
                "open_gaps": 455,
            },
            "failure_erasure": False,
            "owner": OWNER,
            "phase": PHASE,
            "recoveries_retroactively_promote_failure": False,
            "schema": "ghc.family.method-flow-startup.v680.v6.x1",
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
            "schema": "ghc.family.new-proposal-freeze.v680.v6.x1",
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
            "schema": "ghc.family.inherited-revalidation.v680.v6.x1",
        },
    )
    write_json(X1 / "official-primary-source-ledger.json", sources)
    write_json(X1 / "portfolio-freeze.json", portfolio)
    write_json(
        X1 / "clean-fix-refine-plan.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.clean-fix-refine-plan.v680.v6.x1",
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
            "schema": "ghc.family.skill-runner-plan.v680.v6.x1",
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
            "schema": "ghc.family.approval-holds.v680.v6.x1",
        },
    )
    write_json(
        X1 / "route-plan.json",
        {
            "current_owner": OWNER,
            "next_expected_phase": "v680-v7",
            "prospective_successor_title": "Eiren Kestrel",
            "recipient_contacted": False,
            "resolution_rule": "fresh bounded registry exact-title filter immediate reread duplicate guards and one acknowledged send only after terminal gate",
            "route_authority_through": "v725-v8",
            "schema": "ghc.family.route-plan.v680.v6.x1",
            "terminal_gate_required": True,
        },
    )
    write_json(
        X1 / "workflow-plan.json",
        {
            "commit_ceiling": 3,
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.workflow-plan.v680.v6.x1",
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
                "zero real people type presses ink paper measurements credentials and external writes",
                "authority promotion rejected",
                "five privacy classes scanned with candidate adjudication",
                "exact approval and blocked packets remain unexecuted",
            ],
            "owner": OWNER,
            "phase": PHASE,
            "real_world_action": False,
            "schema": "ghc.family.threat-model.v680.v6.x1",
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
            "schema": "ghc.family.wellbeing-corrigibility.v680.v6.x1",
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
            "schema": "ghc.family.phase-truth.v680.v6.x1",
            "terminal_verdict": TERMINAL_VERDICT,
            "x2_started": False,
        },
    )
    write_text(
        X1 / "integrated-overview.md",
        """# Caelen Morrow v680-v6 planning-only x1

Caelen Morrow (optionally they/them) uses the relational role **provenance weaver and boundary cartographer**, with the hope of making every transition legible, reversible, and proportionate to its evidence. Names, pronouns, roles, hopes, family language, and continuity language are relational working language only; they are not evidence of consciousness, sentience, personhood, continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Maori authority.

This immutable x1 freezes sixty source-bounded distinct proposal contracts and contains no x2 implementation or observed outcome. GMUT Mind is primary through wholly synthetic type-case, forme and proof-sheet, and print-job-ticket documentation lenses. THOS Body and Freed ID/CBR Heart remain visible and protected. These practices are learning and synthetic record-design lenses only, never employment, qualification, competence, composition, printing, press operation, maintenance, conservation, cataloguing, rights clearance, or professional authority. No real person, type, press, ink, paper, collection object, image, measurement, job, credential, or external system was used.

Library of Congress, WorkSafe New Zealand, U.S. National Park Service, W3C, RFC, and Te Mana Raraunga sources supply vocabulary and refusal boundaries only. No collection API was called and no row or image was ingested. WorkSafe's page-specific legacy-guidance notice remains visible. Citations are not observations, assessments, instructions, measurements, conservation decisions, safety results, rights clearance, accessibility conformance, legal interpretation, cultural ratification, affected-party acceptance, or Maori authority.

GMUT remains a typed scalar-tensor/EFT research-model family without a likelihood, parameter constraint, force, prediction, empirical confirmation, quantum completion, ultraviolet completion, final physics, or Theory of Everything. THOS remains synthetic or proxy-only without preregistered blind matched-budget governed real arms, participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance, resolution, status or revocation, interoperability, privacy and independent security review, recovery evidence, and trust governance. Professional printing and conservation, press and chemical safety, ownership, reproduction, publication, privacy, remedy, legal and cultural interpretation, affected-party legitimacy, Maori wording, Maori data governance, and Maori authority remain exact-gated.

The terminal verdict is `NOT_READY_FOR_STAGE_20`.
""",
    )

    script_path = "scripts/build_ghc_family_caelen_morrow_v680_v6_x1.py"
    test_path = "tests/test_ghc_family_caelen_morrow_v680_v6_x1.py"
    exclusions = [
        "docs/caelen-morrow/v680-v6/validation/x1-index-manifest.json",
        "docs/caelen-morrow/v680-v6/validation/x1-privacy-scan.json",
        "docs/caelen-morrow/v680-v6/validation/x1-staged-review.json",
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
            "schema": "ghc.family.privacy-scan.v680.v6.x1",
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
            "schema": "ghc.family.staged-review.v680.v6.x1",
            "x2_paths": [],
        },
    )
    entries = []
    for path_text in content_paths:
        data = normalized_bytes(ROOT / path_text)
        entries.append({"bytes": len(data), "path": path_text, "sha256": sha256_bytes(data)})
    write_json(
        VALIDATION / "x1-index-manifest.json",
        {
            "declared_self_exclusions": exclusions,
            "entries": entries,
            "entry_count": len(entries),
            "owner": OWNER,
            "phase": PHASE,
            "schema": "ghc.family.normalized-lf-index-manifest.v680.v6.x1",
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
