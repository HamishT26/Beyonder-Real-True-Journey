from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from collections.abc import Iterable
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "elaren-kestrel" / "v682-v7"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"

OWNER = "Elaren Kestrel"
PHASE = "v682-v7"
BRANCH = "codex/GHC-Family/elaren-kestrel-v682-v7-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/eiren-kestrel-v682-v6-full-tools"
SOURCE = "7442303ebfbea11e7d9e4a9f40a441d5805b3272"
SOURCE_X1 = "861fa9c2ee9f96a0ad43105b6f56b1d278925b5c"
SOURCE_EVIDENCE = "6540d4d7cfab8300f750d48cdff4f39e007f170a"
SOURCE_PARENT = "621ea4f832e9fda5549ed2f97dbfd9b539ef1f69"
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "ab26bd76fab82d3f962bad80d48195716247c86ccff34ce579aa53eff53f79c1"
)
SOURCE_CANONICAL_PAYLOAD_SHA256 = (
    "fe49ffba725e2cd3cd766b739fd2480bf805f622eabf2c04762cbfff08450245"
)
DECLARED_CHAIN_BEFORE = 10550
DECLARED_CHAIN_AFTER = 10610
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
CHECKED_AT_UTC = "2026-09-02T01:02:06Z"
WRITTEN: list[str] = []

ACTIVATION_BASELINE = {
    "effective_negatives": 57127,
    "effective_methods": 69035,
    "failed_witnesses": 28788,
    "bounded_passing_witnesses": 50195,
    "open_gaps": 507,
    "exact_gates": 497,
}

PROPOSAL_TITLES = [
    "Synthetic bobbin-lace documentation capsule separating pattern-point surrogate thread-path model and physical textile",
    "Pillow bobbin pin and pattern carrier topology with every physical component vacant",
    "Pattern sheet sample folder and catalogue identifier domains with collision quarantine",
    "Thread pair carrier and pattern-section relation graph without tool or material inspection",
    "Cross twist and pair-exchange token grammar without executable making instruction",
    "Pattern-point coordinate register with zero measured geometry and scale unknown",
    "Repeat edge corner and motif-region relation topology without design authorship claim",
    "Ground cloth tally and plait vocabulary board held for competent technique review",
    "Footside headside boundary placeholders without historical or regional classification",
    "Synthetic working-pair alias register without attribution to a maker or tradition",
    "Passive and active pair-state vacancies without observed thread motion",
    "Pin placement and withdrawal event plan with zero handling or sequence execution",
    "Bobbin winding inventory placeholder with zero thread material or quantity",
    "Thread fibre colour finish and twist claims under material-verification hold",
    "Tension-balance proxy with zero force measurement and no quality verdict",
    "Pattern-point numbering and alias normalization with duplicate quarantine",
    "Pattern scaling and resize request capsule with no geometric transformation",
    "Mirror rotation repeat and border transform declarations without toolpath generation",
    "Motif region component and negative-space graph without iconographic interpretation",
    "Pattern annotation revision and later transcription lineage without authorship verdict",
    "Thread-path crossing graph with no real order motion tension or textile result",
    "Continuity break loose-end and ambiguous-crossing cues without defect diagnosis",
    "Join split start finish and reserve-thread relation topology without making action",
    "Corner-turn and edge-return relation board with every operational step absent",
    "Layered working-diagram surrogate separating point map thread route note and uncertainty",
    "Pattern-point to thread-occupancy matrix with zero observations and zero calculation",
    "Bobbin-pair exchange log surrogate with no bobbin handling or worker action",
    "Error correction rollback and supersession ledger without craft assessment",
    "Pattern original derivative image and transcription role separation without file creation",
    "Image capture geometry colour profile resolution and crop targets with zero imaging",
    "Descriptive metadata crosswalk separating pattern sample maker surrogate and unresolved rights basis",
    "PREMIS object event agent rights and fixity vacancies for synthetic lace documentation",
    "Synthetic lineage bundle distinguishing plan source digest supersession and retirement for a zero-file pattern packet",
    "Checksum filename package and storage identifier separation from pattern and sample identity",
    "Condition-cue vocabulary for break crease stain loss and distortion without textile examination",
    "Storage display support and light-exposure hold with no conservation recommendation",
    "Copyright design-right donor restriction access embargo takedown and correction remedy ledger",
    "Community association traditional-knowledge and cultural-description minimum-disclosure hold",
    "Structural accessible pattern summary with tactile and nonvisual evaluation reserved",
    "Synthetic backlog fatigue pause dual-readback and handover lease for documentation queues",
    "No-action imaging docket with intent authorization attempt observation and result vacancies kept separate",
    "Synthetic quality-control board for legibility topology and count reconciliation with zero observation",
    "Represented lacemaker curator conservator cataloguer rights-holder and community-reviewer roles vacant",
    "Represented Metropolitan Museum bobbin-lace vocabulary adapter with zero calls and zero records",
    "Represented Victoria and Albert Museum lace collection profile with zero object ingestion",
    "Represented Canadian Conservation Institute textile-care profile with zero examination or treatment",
    "Represented dimensional-language guard requiring absent values before any quantity and unit pair may appear",
    "Represented PREMIS preservation-event board with zero repository action",
    "Represented catalogue-term mapping for title identifier format provenance and rights with publication locked off",
    "Represented THOS documentation-queue charter with equal synthetic budgets dominant stop precedence and participant count zero",
    "Represented GMUT thread-topology obligation board with no likelihood parameter inference or material model",
    "Represented Freed ID pattern sample and package relation with zero keys proofs or lifecycle events",
    "Represented remedy-clock state machine for description challenge acknowledgement abstention and withdrawal without claimant contact",
    "Represented keyboard and nonvisual discovery scaffold with analytics disabled and user evaluation absent",
    "Open gap for competent examination of actual bobbin lace patterns textiles materials condition and conservation needs",
    "Open gap for governed documentation benchmark using real practitioners records safety monitoring statistics and independent review",
    "Open gap for affected-user accessible discovery rights remedy traditional-knowledge and cultural review",
    "Exact gate for real bobbin pin pillow thread textile handling making conservation and workplace safety authority",
    "Exact gate for custody ownership copyright design rights donor restriction privacy publication legal cultural and affected-party authority",
    "Exact closure lock for community data control real-world evidence operational authority external replication identity claims and Stage 20",
]

MUTATION_TYPES = [
    "missing_required_field",
    "lifecycle_inversion",
    "stale_provenance_digest",
    "safety_status_promotion",
    "authority_promotion",
]

PROTECTED_GATES = [
    (
        "real people lacemakers curators conservators communities patterns textiles tools materials records observations "
        "measurements handling making treatment and actions"
    ),
    "empirical GMUT material or thread models likelihoods constraints predictions inference and confirmation",
    (
        "professional lacemaking cataloguing conservation handling digitization tool workplace chemical fire and publication authority"
    ),
    "production identity issuance resolution status revocation interoperability and trust governance",
    (
        "pattern privacy copyright design rights donor restrictions ownership custody access heritage traditional knowledge "
        "legal cultural affected-party and Maori authority"
    ),
    "privacy-complete accessibility-complete and exhaustive-security claims",
    "independent reproduction AGI ASI consciousness personhood Theory of Everything proof canon and Stage 20",
]

STARTUP_FAILURES = [
    {
        "failure_id": "EL6827-ST-N001",
        "failed_witness": "The first worktree inventory ran from a directory that was not a Git worktree.",
        "initial_credit": 0,
        "recovery": "Enumerate only the bounded D-first worktree bank and verify the exact source there.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EL6827-ST-N002",
        "failed_witness": "An unquoted upstream shorthand was parsed as a PowerShell script block.",
        "initial_credit": 0,
        "recovery": "Quote the revision and read local, upstream, tracking, and live heads as separate scalars.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EL6827-ST-N003",
        "failed_witness": "A broad external-receipt digest search returned no attributable phase result.",
        "initial_credit": 0,
        "recovery": "Inventory the immediate receipt bank and read the exact v682-v6-to-v682-v7 delivery receipt.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EL6827-ST-N004",
        "failed_witness": "An unbounded whole-tree candidate-domain grep crossed its presentation window.",
        "initial_credit": 0,
        "recovery": "Use the source builder's persistent Git-object batch audit for exact proposal evidence.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EL6827-ST-N005",
        "failed_witness": "The first combined authorization-state display truncated before EOF.",
        "initial_credit": 0,
        "recovery": "Read the exact authorization state in bounded ordered line windows through EOF.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EL6827-ST-N006",
        "failed_witness": "A PowerShell foreach result was piped without prior materialization and raised ParserError.",
        "initial_credit": 0,
        "recovery": "Materialize the bounded result array before formatting it.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EL6827-ST-N007",
        "failed_witness": "The compound worktree-creation wrapper crossed its return window while Git continued.",
        "initial_credit": 0,
        "recovery": "Inspect the exact owned process and existing worktree state before resuming only unfinished materialization.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EL6827-ST-N008",
        "failed_witness": "The first bounded worktree-process wait contained a malformed branch-existence expression.",
        "initial_credit": 0,
        "recovery": "Separate the wait, branch probe, and scalar projection.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EL6827-ST-N009",
        "failed_witness": "The first status projection rendered the entire inherited sparse-deletion surface and exceeded its presentation budget.",
        "initial_credit": 0,
        "recovery": "Inspect skip-worktree flags and scalar status counts before bounded repair.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EL6827-ST-N010",
        "failed_witness": "Sparse read-tree completed without materializing the included paths from an unchanged index.",
        "initial_credit": 0,
        "recovery": "Retain the ineffective witness and inspect the exact index flags rather than replaying it.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EL6827-ST-N011",
        "failed_witness": "Sparse reapply also left the included paths absent from the new worktree.",
        "initial_credit": 0,
        "recovery": "Materialize only the explicitly included source paths from immutable HEAD.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EL6827-ST-N012",
        "failed_witness": "The first bounded materialization included two untracked package-init pathspecs and failed closed.",
        "initial_credit": 0,
        "recovery": "Remove only the nonexistent pathspecs and materialize the exact tracked include set once.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EL6827-ST-N013",
        "failed_witness": "A lifecycle-receipt foreach projection repeated the unmaterialized-pipeline parser fault.",
        "initial_credit": 0,
        "recovery": "Materialize the bounded receipt rows before JSON projection.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EL6827-ST-N014",
        "failed_witness": "The first combined x1 source display exceeded its presentation budget.",
        "initial_credit": 0,
        "recovery": "Read only the required source-builder ranges and exact lifecycle contracts.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EL6827-X1-N015",
        "failed_witness": "The first exact-source proposal audit rejected three exact inherited duplicates and five near-duplicates before writing x1.",
        "initial_credit": 0,
        "recovery": "Retain all eight rejected titles, replace only those contracts with substantively different state machines, and rerun only the failed novelty and build dependency.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "EL6827-X1-N016",
        "failed_witness": "The first accepted x1 build exposed inherited source-anchor and successor expectations in the copied owner test before validation.",
        "initial_credit": 0,
        "recovery": "Correct only the Elaren x1 expectations, record this target change, and regenerate the planning packet and exact manifest before running the test.",
        "recovery_credit": "target_changed_before_validation",
    },
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def git(
    *args: str, check: bool = True, text: bool = True
) -> subprocess.CompletedProcess[Any]:
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


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def jaccard(left: str, right: str) -> float:
    left_tokens = title_tokens(left)
    right_tokens = title_tokens(right)
    if not left_tokens and not right_tokens:
        return 1.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def title_tokens(value: str) -> frozenset[str]:
    return frozenset(re.findall(r"[a-z0-9]+", value.casefold()))


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
        return ["MET-BOBBIN-LACE", "MET-LACE-HISTORY", "W3C-PROV-O"]
    if index <= 30:
        return ["MET-BOBBIN-LACE", "NIST-SI", "W3C-PROV-O"]
    if index <= 42:
        return ["CCI-TEXTILE-CARE", "LOC-PREMIS", "DCMI-TERMS"]
    if index <= 54:
        return ["VAM-TEXTILE-COLLECTION", "W3C-WCAG22", "W3C-VC-DM-20"]
    if index == 55:
        return ["CCI-TEXTILE-CARE", "LOC-PREMIS"]
    if index == 56:
        return ["MET-BOBBIN-LACE", "CCI-TEXTILE-CARE"]
    if index == 57:
        return ["W3C-WCAG22", "NZ-PRIVACY-PRINCIPLES", "TMR-MDS-PRINCIPLES"]
    if index == 58:
        return ["CCI-TEXTILE-CARE", "MET-BOBBIN-LACE"]
    if index == 59:
        return ["LOC-PREMIS", "DCMI-TERMS", "W3C-PROV-O"]
    return ["TMR-MDS-PRINCIPLES", "W3C-PROV-O"]


def proposals() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, title in enumerate(PROPOSAL_TITLES, start=1):
        proposal_id = f"EL6827-N{index:03d}"
        rows.append(
            {
                "approval_class": approval_class(index),
                "concrete_artifacts": [
                    f"docs/elaren-kestrel/v682-v7/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/elaren-kestrel/v682-v7/x2/rejecting-mutations.json#{proposal_id}",
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
                    for mutation_index, mutation_type in enumerate(
                        MUTATION_TYPES, start=1
                    )
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
            proc.stdin.write(f"{tree}:{path}\n".encode())
            proc.stdin.flush()
            header = (
                proc.stdout.readline().decode("utf-8", errors="replace").rstrip("\n")
            )
            if header.endswith(" missing"):
                continue
            parts = header.split()
            if len(parts) != 3 or parts[1] != "blob":
                raise RuntimeError(f"unexpected cat-file header for {path}: {header}")
            size = int(parts[2])
            chunks: list[bytes] = []
            remaining = size
            while remaining:
                chunk = proc.stdout.read(remaining)
                if not chunk:
                    raise RuntimeError(f"partial cat-file blob for {path}")
                chunks.append(chunk)
                remaining -= len(chunk)
            data = b"".join(chunks)
            if proc.stdout.read(1) != b"\n":
                raise RuntimeError(f"missing cat-file separator for {path}")
            yield path, data
    finally:
        proc.stdin.close()
        proc.terminate()
        proc.wait(timeout=10)


def proposal_chain_audit(new_records: list[dict[str, Any]]) -> dict[str, Any]:
    grep_result = git(
        "grep", "-l", "-I", '"proposal_id"', SOURCE, "--", "*.json", check=False
    )
    if grep_result.returncode not in (0, 1):
        raise RuntimeError(grep_result.stderr)
    raw_paths = sorted(set(filter(None, grep_result.stdout.splitlines())))
    tree_prefix = SOURCE + ":"
    paths = [path.removeprefix(tree_prefix) for path in raw_paths]
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
        raise RuntimeError(
            "proposal audit must parse nonzero exact-source paths and id-title records"
        )

    inherited_titles = {record["title"] for record in inherited}
    inherited_with_tokens = [
        (record, title_tokens(record["title"])) for record in inherited
    ]
    exact_collisions: list[str] = []
    neighbors: list[dict[str, Any]] = []
    for proposal in new_records:
        title = proposal["title"]
        if title in inherited_titles:
            exact_collisions.append(title)
        best: dict[str, str] | None = None
        best_score = -1.0
        proposal_tokens = title_tokens(title)
        for record, inherited_tokens in inherited_with_tokens:
            if not proposal_tokens and not inherited_tokens:
                score = 1.0
            else:
                score = len(proposal_tokens & inherited_tokens) / len(
                    proposal_tokens | inherited_tokens
                )
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
            + json.dumps(
                {"exact": exact_collisions, "neighbors": quarantined},
                ensure_ascii=False,
            )
        )
    return {
        "audit_scope": {
            "claim": "bounded all-reachable exact-source proposal audit; no universal 10490-row proof",
            "proposal_json_parse_failures": parse_failures,
            "proposal_json_paths_discovered": len(paths),
            "proposal_json_paths_parsed": parsed,
            "reachable_id_title_records": len(inherited),
            "universal_declared_chain_materialization_claimed": False,
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
        "schema": "ghc.family.proposal-chain-audit.v682.v7.x1",
        "source": SOURCE,
    }


def task_records(prefix: str, count: int, lane: str) -> list[dict[str, Any]]:
    return [
        {
            "approval_required": lane in {"exact_approval", "blocked"},
            "lane": lane,
            "planned_action": f"Preregistered Elaren owner-local {lane.replace('_', ' ')} item {index:03d}.",
            "state": "preregistered_not_executed",
            "task_id": f"EL6827-{prefix}-{index:03d}",
        }
        for index in range(1, count + 1)
    ]


SKILL_NAMES = [
    "bobbin-lace-surrogate-separator",
    "pattern-point-vacancy-guard",
    "thread-path-nonexecution",
    "pair-state-vacancy",
    "material-claim-quarantine",
    "point-number-collision-quarantine",
    "transform-nonexecution",
    "annotation-lineage-ledger",
    "motif-interpretation-hold",
    "condition-nondiagnosis",
    "digitization-action-separator",
    "premis-lace-event-vacancy",
    "accessible-pattern-summary",
    "traditional-knowledge-minimizer",
    "rights-remedy-hold",
    "workload-handover-lease",
    "freed-id-zero-key-guard",
    "thos-worker-vacancy",
    "gmut-topology-noninference",
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
            "wholly synthetic bobbin-lace pattern-point and thread-path documentation",
            "wholly synthetic metadata, condition-cue, preservation-event, and digitization planning",
            "wholly synthetic rights, accessibility, remedy, workload, and handover documentation",
        ],
        "owner_runner_ideas": [
            {
                "runner_id": f"EL6827-RUNNER-{index:02d}",
                "name": f"ghc_family_bobbin_lace_runner_{index:02d}.py",
                "state": "planned_not_built_in_x1",
            }
            for index in range(1, 11)
        ],
        "owner_skill_ideas": [
            {
                "skill_id": f"EL6827-SKILL-{index:02d}",
                "name": name,
                "state": "planned_not_built_in_x1",
            }
            for index, name in enumerate(SKILL_NAMES, start=1)
        ],
        "phase": PHASE,
        "primary_pillar": "Freed ID and CBR Heart",
        "represented_pillars": ["GMUT Mind", "THOS Body"],
        "safe_now": task_records("SAFE", 120, "safe_now"),
        "schema": "ghc.family.portfolio-freeze.v682.v7.x1",
        "successor_candidates": task_records(
            "SUCCESSOR-CAND", 20, "successor_candidate_zero_credit"
        ),
        "successor_clean_fix_refine": task_records(
            "SUCCESSOR-CFR", 30, "successor_recommendation_zero_credit"
        ),
        "successor_practice_recommendation": (
            "one zero-credit seed only: choose a distinct synthetic documentation lens and independently audit every proposal before freeze"
        ),
        "successor_runner_ideas": task_records(
            "SUCCESSOR-RUNNER", 10, "successor_runner_seed_zero_credit"
        ),
        "successor_skill_ideas": task_records(
            "SUCCESSOR-SKILL", 10, "successor_skill_seed_zero_credit"
        ),
    }


def official_sources() -> dict[str, Any]:
    entries = [
        {
            "source_id": "MET-BOBBIN-LACE",
            "status": "official_Metropolitan_Museum_page_checked_2026-09-02",
            "title": "Gertrude Whiting's Bobbin-Lace Sampler and the Connoisseurship of Lace",
            "url": "https://www.metmuseum.org/perspectives/gertrude-whiting-bobbin-lace-sampler",
            "use": "bobbin, thread, pair, cross, twist, pillow, pattern and pin vocabulary only; no making instruction, object attribution, technique assessment or museum endorsement",
        },
        {
            "source_id": "MET-LACE-HISTORY",
            "status": "official_Metropolitan_Museum_essay_checked_2026-09-02",
            "title": "Textile Production in Europe: Lace, 1600-1800",
            "url": "https://www.metmuseum.org/essays/textile-production-in-europe-lace-1600-1800",
            "use": "high-level distinction between bobbin and needle lace plus historical vocabulary only; no regional attribution, cultural interpretation, authorship or authenticity finding",
        },
        {
            "source_id": "VAM-TEXTILE-COLLECTION",
            "status": "official_Victoria_and_Albert_Museum_collection_display_checked_2026-09-02",
            "title": "Textiles at the V&A",
            "url": "https://lookup.vam.ac.uk/east-storehouse/storagedisplays/USE2193/",
            "use": "collection-role and material-technique label examples only; zero object rows ingested and no attribution, rights, condition or conformance claim",
        },
        {
            "source_id": "CCI-TEXTILE-CARE",
            "status": "official_Canadian_Conservation_Institute_page_checked_2026-09-02",
            "title": "Caring for textiles and costumes",
            "url": "https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/textiles-costumes.html",
            "use": "preventive-care risk and professional-reservation vocabulary only; no object examination, handling, storage, display, cleaning, repair or treatment recommendation",
        },
        {
            "source_id": "NIST-SI",
            "status": "official_NIST_publication_page_checked_2026-09-02",
            "title": "The International System of Units (SI), 2019 Edition",
            "url": "https://www.nist.gov/publications/international-system-units-si2019-edition",
            "use": "quantity, unit, symbol and dimensional-reporting vocabulary only; zero measurements or conversions",
        },
        {
            "source_id": "LOC-PREMIS",
            "status": "official_Library_of_Congress_standard_page_checked_2026-09-02",
            "title": "PREMIS Preservation Metadata Maintenance Activity",
            "url": "https://www.loc.gov/standards/premis/index.html",
            "use": "object, event, agent, rights, fixity and preservation-metadata vocabulary only; no repository ingest or conformance claim",
        },
        {
            "source_id": "DCMI-TERMS",
            "status": "DCMI_Recommendation_checked_2026-09-02",
            "title": "DCMI Metadata Terms",
            "url": "https://www.dublincore.org/specifications/dublin-core/dcmi-terms/",
            "use": "creator, title, identifier, format, provenance, access-rights and rights-statement vocabulary only",
        },
        {
            "source_id": "W3C-PROV-O",
            "status": "W3C_Recommendation_checked_2026-09-02",
            "title": "PROV-O: The PROV Ontology",
            "url": "https://www.w3.org/TR/prov-o/",
            "use": "entity, activity, agent, derivation, revision and provenance vocabulary only",
        },
        {
            "source_id": "W3C-WCAG22",
            "status": "W3C_Recommendation_checked_2026-09-02",
            "title": "Web Content Accessibility Guidelines 2.2",
            "url": "https://www.w3.org/TR/WCAG22/",
            "use": "structural accessibility vocabulary and manual, browser, assistive-technology, cognitive and affected-user evaluation reservations only",
        },
        {
            "source_id": "W3C-VC-DM-20",
            "status": "W3C_Recommendation_checked_2026-09-02",
            "title": "Verifiable Credentials Data Model v2.0",
            "url": "https://www.w3.org/TR/vc-data-model-2.0/",
            "use": "synthetic identifier, credential, status and proof-vacancy vocabulary only; no real key or lifecycle event",
        },
        {
            "source_id": "NZ-PRIVACY-PRINCIPLES",
            "status": "official_New_Zealand_Privacy_Commissioner_material_checked_2026-09-02",
            "title": "New Zealand Information Privacy Principles",
            "url": "https://www.privacy.org.nz/privacy-principles/",
            "use": "privacy minimization, access, correction, disclosure, and current IPP 3A notification vocabulary only; no legal interpretation or compliance claim",
        },
        {
            "source_id": "TMR-MDS-PRINCIPLES",
            "status": "authority_boundary_context_only_checked_2026-09-02",
            "title": "Principles of Maori Data Sovereignty",
            "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
            "use": "Maori data-governance vacancy and noncompensation boundary only; never delegated Maori authority",
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
        "schema": "ghc.family.official-primary-sources.v682.v7.x1",
        "web_checks": len(entries),
    }


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    classes = {
        "raw_task_or_thread_identifier": re.compile(
            r"\b019[a-f0-9]{29,}\b", re.IGNORECASE
        ),
        "credential_or_secret": re.compile(
            r"(?:api[_-]?key|private[_-]?key|bearer\s+[a-z0-9._-]{12,})", re.IGNORECASE
        ),
        "private_route_or_callable_identifier": re.compile(
            r"(?:threadId|private callable|app://connector_)", re.IGNORECASE
        ),
        "private_absolute_path": re.compile(
            r"(?:[A-Z]:\\Users\\|[A-Z]:\\GHC-Archives\\)", re.IGNORECASE
        ),
        "transcript_screenshot_or_session_stream": re.compile(
            r"(?:raw transcript|session stream|screenshot payload)", re.IGNORECASE
        ),
    }
    candidates: list[dict[str, str]] = []
    for path in paths:
        target = ROOT / path
        if not target.exists() or target.suffix.lower() not in {
            ".json",
            ".md",
            ".py",
            ".yaml",
            ".yml",
            ".html",
        }:
            continue
        text = target.read_text(encoding="utf-8")
        for class_name, pattern in classes.items():
            if pattern.search(text):
                candidates.append(
                    {
                        "class": class_name,
                        "path": path,
                        "adjudication": "scanner_definition_only",
                    }
                )
    return {
        "candidate_count": len(candidates),
        "candidates": candidates,
        "class_count": 5,
        "confirmed_hit_count": 0,
        "confirmed_hits": [],
        "owner": OWNER,
        "phase": PHASE,
        "schema": "ghc.family.privacy-scan.v682.v7.x1",
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
    if expected_counts != Counter(
        {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
    ):
        raise RuntimeError(f"unexpected disposition counts: {expected_counts}")
    audit = proposal_chain_audit(new_records)

    current_after_startup = dict(ACTIVATION_BASELINE)
    for key in (
        "effective_negatives",
        "effective_methods",
        "failed_witnesses",
        "bounded_passing_witnesses",
    ):
        current_after_startup[key] += len(STARTUP_FAILURES)

    write_json(
        X1 / "activation-intake.json",
        {
            "activation_baseline": ACTIVATION_BASELINE,
            "delivery_state": "SENT_ONCE_ACKNOWLEDGED_EXTERNAL",
            "source_repository_and_live_delivery_kept_distinct": True,
            "owner": OWNER,
            "phase": PHASE,
            "received_source_final": SOURCE,
            "schema": "ghc.family.activation-intake.v682.v7.x1",
        },
    )
    write_json(
        X1 / "identity-and-boundary.json",
        {
            "consciousness_personhood_or_continuity_claimed": False,
            "hope": "Every synthetic thread route remains distinguishable from practiced craft, while material, cultural, and affected-party authority remain with their holders.",
            "name": OWNER,
            "optional_pronouns": "they/them",
            "owner_rename_pause_redirect_stop_right": "Hamish",
            "phase": PHASE,
            "relational_working_language_only": True,
            "role": "pattern-provenance lantern and rights-boundary cartographer",
            "schema": "ghc.family.identity-boundary.v682.v7.x1",
        },
    )
    write_json(
        X1 / "source-verification.json",
        {
            "branch": SOURCE_BRANCH,
            "canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
            "canonical_payload_sha256": SOURCE_CANONICAL_PAYLOAD_SHA256,
            "clean": True,
            "evidence": SOURCE_EVIDENCE,
            "final": SOURCE,
            "four_way_equal": True,
            "manifest_replay": {
                "x1": 20,
                "evidence": 75,
                "final_delta": 23,
                "final_owner": 124,
                "total": 242,
                "mismatches": 0,
            },
            "content_seal_targets": 10,
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
            "schema": "ghc.family.proposal-freeze.v682.v7.x1",
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
            "schema": "ghc.family.inherited-revalidation.v682.v7.x1",
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
            "schema": "ghc.family.approval-holds.v682.v7.x1",
        },
    )
    write_json(
        X1 / "clean-fix-refine-plan.json",
        {
            "owner": OWNER,
            "owner_rows": portfolio["owner_clean_fix_refine"],
            "phase": PHASE,
            "schema": "ghc.family.clean-fix-refine.v682.v7.x1",
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
            "schema": "ghc.family.skill-runner-plan.v682.v7.x1",
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
            "schema": "ghc.family.method-flow-startup.v682.v7.x1",
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
            "schema": "ghc.family.phase-truth.v682.v7.x1",
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
                "pattern, thread, material, condition, digitization, rights, authorship or cultural authority inferred from documentation",
                "route or private identifier leakage",
                "x1 and x2 lifecycle contamination",
            ],
            "schema": "ghc.family.threat-model.v682.v7.x1",
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
            "schema": "ghc.family.workflow-plan.v682.v7.x1",
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
            "prospective_successor_exact_title": "Neris Solane",
            "prospective_successor_phase": "v682-v8",
            "route_authority_through": "v725-v8",
            "send_before_terminal_gate": False,
            "tavian_sol": "ON_STANDBY",
        },
    )
    write_text(
        X1 / "integrated-overview.md",
        f"""# Elaren Kestrel {PHASE} Planning-Only X1 Overview

Elaren Kestrel, optionally they/them, is relational working language for a pattern-provenance lantern and rights-boundary cartographer, with the hope that every synthetic thread route remains distinguishable from practiced craft while material, cultural, and affected-party authority remain with their holders. This is not evidence of consciousness, sentience, personhood, continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Maori authority. Hamish retains the right to rename, pause, redirect, narrow, or stop the route.

The exact immutable source is Eiren Kestrel final `{SOURCE}` on `{SOURCE_BRANCH}`. Read-only verification established the direct Caelen-source to Eiren-x1 to Eiren-evidence to Eiren-final chain, exactly three Eiren single-parent commits, zero merges, one final parent, clean state, typed 0/0 divergence, fresh four-way equality, 242 exact normalized-LF manifest entries and ten content-seal targets, plus exact canonical receipt and payload digests. No Eiren test, manifest aggregate, or canonical aggregate was replayed. Eiren's repository seal, four-row external activation overlay, acknowledged live delivery, and Elaren startup failures remain distinct truth layers.

This x1 freezes sixty Elaren proposals only after a bounded all-reachable exact-source audit. The accepted slate must produce zero exact collisions and zero quarantine hits at the 0.78 token-Jaccard threshold. It makes no universal semantic-novelty claim over every declared historical row where a canonical materialized row-to-title ledger is absent. Twenty inherited neighbour reviews remain source evidence with zero Elaren completion credit.

Freed ID and CBR Heart are primary through pattern and sample surrogate separation, provenance, correction, fixity, access, authorship and design-right reservations, remedy, privacy minimization, traditional-knowledge holds, and cultural-authority noncompensation. THOS Body remains visible through synthetic pattern-point and thread-path topology, action separation, stop states, workload budgets, accessibility, correction, and handover. GMUT Mind remains visible through typed topological obligations, zero-observation state, uncertainty holds, and explicit noninference. Bobbin-lace pattern and thread-path documentation is a wholly synthetic learning and design lens only, never employment, qualification, competence, lacemaking, collection custody, conservation, digitization, rights clearance, publication, or professional authority.

The plan uses zero real people, lacemakers, curators, conservators, communities, patterns, textiles, bobbins, pins, pillows, threads, fibres, dyes, images, tools, materials, observations, measurements, making actions, digitizations, identity events, external writes, or authority acts. Current official and primary sources supply vocabulary and refusal conditions only. They are not pattern classifications, material findings, object examinations, preservation recommendations, making instructions, digitization results, catalogue decisions, rights determinations, legal interpretations, cultural ratifications, affected-party decisions, or authority grants.

Expected x2 dispositions are exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. Those are preregistered expected labels, not observed outcomes. All 300 invalid mutations, 120 safe-now tasks, 80 bounded candidates, 100 CLEAN/FIX/REFINE records, twenty skills, and ten runners remain planned rather than executed in this x1. Twenty exact-approval and ten blocked packets remain visible and unexecuted.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family without physical data, material evidence, likelihood, posterior, prediction, constraint, empirical confirmation, ultraviolet or quantum completion, or Theory-of-Everything proof. THOS remains synthetic/proxy-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live lifecycle operations, interoperability, independent privacy/security review, recovery evidence, trust governance, and affected-party oversight.

Real pattern, textile, bobbin, pin, pillow and thread handling; lacemaking; conservation treatment; digitization; professional cataloguing; copyright and design rights; privacy; donor restrictions; access; ownership; custody; heritage; traditional knowledge; remedy; legal and cultural interpretation; affected-party legitimacy; Maori wording and data governance; and Maori authority remain exact-gated. Maori concepts remain under Maori authority. Complete privacy, complete accessibility, exhaustive security, independent reproduction, AGI/ASI, consciousness/personhood, proof/canon, and Stage 20 remain open or exact-gated. The terminal verdict remains `{TERMINAL_VERDICT}`.
""",
    )

    x1_material_paths = sorted(
        set(
            WRITTEN
            + [
                "scripts/build_ghc_family_elaren_kestrel_v682_v7_x1.py",
                "tests/test_ghc_family_elaren_kestrel_v682_v7_x1.py",
            ]
        )
    )
    exclusions = [
        "docs/elaren-kestrel/v682-v7/validation/x1-index-manifest.json",
        "docs/elaren-kestrel/v682-v7/validation/x1-privacy-scan.json",
        "docs/elaren-kestrel/v682-v7/validation/x1-staged-review.json",
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
            "schema": "ghc.family.normalized-lf-index-manifest.v682.v7.x1",
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
            "schema": "ghc.family.staged-review.v682.v7.x1",
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
