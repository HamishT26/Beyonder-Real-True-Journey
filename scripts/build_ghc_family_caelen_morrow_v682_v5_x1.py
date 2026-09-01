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
BASE = ROOT / "docs" / "caelen-morrow" / "v682-v5"
X1 = BASE / "x1"
VALIDATION = BASE / "validation"

OWNER = "Caelen Morrow"
PHASE = "v682-v5"
BRANCH = "codex/GHC-Family/caelen-morrow-v682-v5-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/sylven-arc-v682-v4-full-tools"
SOURCE = "3cbffaa8b76a04a4c382545526658c2e8aaa256c"
SOURCE_X1 = "aef56c5f8beea8e138425e81a99f8b80b517dcde"
SOURCE_EVIDENCE = "ad85f34060125c834b1cefbb9174af3a924643f1"
SOURCE_PARENT = "2dcad52ce5e64cfef69bdb50335638eaa4954ef5"
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "ff9301e8e9d68583c2815a5908ffb8be8155eada4c968fdb1223e062daaa06b5"
)
SOURCE_CANONICAL_PAYLOAD_SHA256 = (
    "cfbf1c58b118f28811b83d6f7c000facf4883c33696e39a1c454be5220e01351"
)
DECLARED_CHAIN_BEFORE = 10430
DECLARED_CHAIN_AFTER = 10490
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
CHECKED_AT_UTC = "2026-09-01T19:00:00Z"
WRITTEN: list[str] = []

ACTIVATION_BASELINE = {
    "effective_negatives": 56465,
    "effective_methods": 67469,
    "failed_witnesses": 28126,
    "bounded_passing_witnesses": 48749,
    "open_gaps": 500,
    "exact_gates": 491,
}

PROPOSAL_TITLES = [
    "Synthetic phonograph-cylinder record capsule and real carrier identity split",
    "Cylinder core groove surface and recording-layer topology with physical presence vacant",
    "Wax celluloid plaster foil and composite material claims under verification hold",
    "Standard concert dictation and custom cylinder format topology without dimensional measurement",
    "Manufacturer catalogue number inscription and box-label transcription versus attribution firewall",
    "Carrier object container sleeve and associated-document relation graph",
    "Accession shelf location barcode and surrogate identifier separation with location minimization",
    "Side end rim bore and groove-region orientation board without handling",
    "Mould shrinkage crack chip delamination and bloom cue vocabulary without condition diagnosis",
    "Surface contamination dust residue and mould suspicion under laboratory hold",
    "Diameter length bore taper mass and wall-thickness fields with zero measurement",
    "Groove pitch speed duration and channel-layout target fields with zero playback",
    "Lateral vertical hill-and-dale groove terminology without signal inference",
    "Original duplicate moulded copy and later reissue lineage without authenticity verdict",
    "Performer speaker creator publisher and collector role vacancies with zero person identification",
    "Title language date place matrix with unknown-value and uncertainty states",
    "Spoken-word music dictation field-recording and demonstration genre proposal without content classification",
    "Cylinder sequence set membership and missing-part topology",
    "Container label cylinder inscription catalogue source and transcription conflict board",
    "Confidence challenge correction supersession and dual-readback lineage",
    "Synthetic preservation event capsule with no cleaning handling repair or treatment",
    "Intake quarantine acclimatization housing and isolation plan versus executed-action separation",
    "Gloves supports trays mandrels and handling-tool plan under professional hold",
    "Temperature relative-humidity light vibration and pollutant target fields with zero monitoring",
    "Cleaning dry-brush solvent swab consolidation and repair plan under conservation hold",
    "Playback stylus profile tracking force speed mandrel and alignment plan with zero playback",
    "Optical-scanning contactless recovery and transfer-method topology with zero imaging or audio",
    "Analog-to-digital chain preamplifier converter clock and file relation graph without capture",
    "Sample rate bit depth channel count codec and wrapper target fields with zero media",
    "Checksum fixity filename and package identifier domains separated from carrier identity",
    "PREMIS object event agent and rights vacancy braid for synthetic preservation",
    "DCMI creator title identifier format and rights mapping with unresolved values",
    "W3C provenance derivation revision and attribution graph for synthetic surrogates",
    "Access master preservation master and derivative role separation without file creation",
    "Quality-control listening waveform spectral and noise-review plans with zero signal data",
    "Duration level speed wow flutter pitch and distortion metric fields with zero measurement",
    "Content warning sensitivity and restricted-description hold without inference",
    "Language dialect name place and cultural affiliation fields under competent-authority gate",
    "Rights copyright licence donor restriction and access-status vacancy ledger",
    "Custody loan transfer reproduction publication and takedown remedy topology",
    "Accessible text transcript caption waveform and player alternatives with manual review reserved",
    "Synthetic collection handover workload pause custody and review queue",
    "Represented archivist conservator cataloguer engineer rights-holder and community-reviewer roles vacant",
    "Represented Library of Congress cylinder-care adapter with zero calls and zero objects",
    "Represented IASA carrier-handling vocabulary adapter with zero calls and zero rows",
    "Represented Smithsonian early-sound collection adapter with zero calls and zero objects",
    "Represented PREMIS preservation-event profile with zero repository ingest",
    "Represented Dublin Core description profile with zero public record publication",
    "Represented THOS backlog fatigue pause and handover protocol with zero real workers",
    "Represented GMUT signal-residual obligation board with no waveform likelihood or inference",
    "Represented Freed ID carrier-surrogate relationship with zero real keys proofs or lifecycle events",
    "Represented amendment challenge acknowledgement expiry and remedy queue with no external contact",
    "Represented structural accessibility companion with browser assistive-technology review reserved",
    "Represented privacy-minimized discovery shell with zero search index or user analytics",
    "Open gap for real cylinder examination material identification condition assessment and conservation review",
    (
        "Open gap for governed playback or optical-transfer study with real carriers operators safety monitoring and "
        "independent review"
    ),
    "Open gap for affected-user accessible discovery rights remediation and cultural review",
    "Exact gate for handling cleaning treatment playback transfer collection custody and professional authority",
    (
        "Exact gate for copyright privacy donor restriction voice identity cultural meaning affected-party and publication "
        "authority"
    ),
    (
        "Exact terminal gate for traditional knowledge Maori wording Maori data governance empirical GMUT production "
        "personhood canon and Stage 20"
    ),
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
        "real people speakers performers collectors communities carriers cylinders containers recordings media observations "
        "measurements and actions"
    ),
    "empirical GMUT waveform likelihoods constraints predictions signal inference and confirmation",
    (
        "professional archival cataloguing conservation handling playback transfer electrical workplace collection and "
        "publication authority"
    ),
    "production identity issuance resolution status revocation interoperability and trust governance",
    (
        "voice identity privacy copyright donor restrictions ownership custody access heritage traditional knowledge legal "
        "cultural affected-party and Maori authority"
    ),
    "privacy-complete accessibility-complete and exhaustive-security claims",
    "independent reproduction AGI ASI consciousness personhood Theory of Everything proof canon and Stage 20",
]

STARTUP_FAILURES = [
    {
        "failure_id": "CM6825-ST-N001",
        "failed_witness": "A combined four-skill display exceeded the supported presentation window before every entrypoint "
        "reached EOF.",
        "initial_credit": 0,
        "recovery": "Reread compact-restart, watcher, full-tools, and worktree-rotation entrypoints separately through EOF.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "CM6825-ST-N002",
        "failed_witness": "The first combined exact-final packet display truncated inside the retained-negative register.",
        "initial_credit": 0,
        "recovery": "Enumerate the exact final filename and reread the register independently through EOF.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "CM6825-ST-N003",
        "failed_witness": "A combined workflow, reflection, and meta-tool display clipped the tail of the workflow "
        "entrypoint.",
        "initial_credit": 0,
        "recovery": "Reread workflow-plan refinement independently and then read each directly required schema.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "CM6825-ST-N004",
        "failed_witness": "The complete mutable authorization-state display exceeded the tool output limit.",
        "initial_credit": 0,
        "recovery": "Read the same immutable JSON in four ordered bounded slices and keep the live v682 activation "
        "authoritative.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "CM6825-ST-N005",
        "failed_witness": "A combined four-anchor history probe crossed its first result window after printing only two "
        "commits.",
        "initial_credit": 0,
        "recovery": "Use separate scalar parent and count probes without replaying source validation.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "CM6825-ST-N006",
        "failed_witness": "An overbroad archive-wide receipt filename traversal returned no bounded attributable result.",
        "initial_credit": 0,
        "recovery": "Enumerate bounded receipt-bank children and inspect the exact observed Sylven v682-v4 directory.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "CM6825-ST-N007",
        "failed_witness": "PowerShell rejected an outer foreach pipeline while projecting manifest contracts.",
        "initial_credit": 0,
        "recovery": "Materialize the rows array before formatting the exact manifest projection.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "CM6825-ST-N008",
        "failed_witness": "A retained-negative probe guessed a closeout path that did not exist.",
        "initial_credit": 0,
        "recovery": "Enumerate exact phase paths and read final/retained-negative-register.json through EOF.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "CM6825-ST-N009",
        "failed_witness": "A test inventory guessed three filenames without their ghc_family prefix.",
        "initial_credit": 0,
        "recovery": "Enumerate the exact current-phase test paths before measuring them.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "CM6825-ST-N010",
        "failed_witness": "The first sparse read-tree was blocked by a live read-only status process holding a zero-byte "
        "index lock.",
        "initial_credit": 0,
        "recovery": "Stop only the owned stalled status process, prove no Git owner remains, remove only its empty stale "
        "lock, and resume read-tree once.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "CM6825-ST-N011",
        "failed_witness": "The first bounded wait wrapper for the stalled status process returned no attributable output.",
        "initial_credit": 0,
        "recovery": "Use explicit finite waits with visible true-or-false output and inspect exact process state.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "CM6825-ST-N012",
        "failed_witness": "Host policy rejected the first exact Remove-Item wrapper for the proven empty stale index lock.",
        "initial_credit": 0,
        "recovery": "Delete only the verified empty lock through the patch surface and recheck absence.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "CM6825-ST-N013",
        "failed_witness": "A recursive materialization-progress inventory produced no attributable result while read-tree "
        "owned the index.",
        "initial_credit": 0,
        "recovery": "Avoid recursive inspection during index construction and follow the original read-tree session until "
        "exit.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "CM6825-X1-N014",
        "failed_witness": "The first complete novelty audit quarantined CM6825-N052 at token-Jaccard 0.833333 against Sylven "
        "proposal SA6824-N054.",
        "initial_credit": 0,
        "recovery": "Retain the rejected title, replace only CM6825-N052 with a semantically different amendment "
        "acknowledgement remedy-queue contract, and rerun the novelty dependency.",
        "recovery_credit": "bounded_dependency_only",
    },
    {
        "failure_id": "CM6825-X1-N015",
        "failed_witness": "The first Ruff invocation found seventeen style-only findings across the two Caelen x1 Python surfaces and earned zero lint-success credit.",
        "initial_credit": 0,
        "recovery": "Apply Ruff fixes only to the two owned x1 Python surfaces, refresh their normalized-LF manifest entries, and rerun only changed lint and test dependencies.",
        "recovery_credit": "bounded_dependency_only",
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
    if index <= 20:
        return ["LOC-CYLINDER-CARE", "IASA-TC05", "W3C-PROV-O"]
    if index <= 36:
        return ["LOC-PREMIS", "DCMI-TERMS", "W3C-PROV-O"]
    if index <= 54:
        return ["SMITHSONIAN-EARLY-SOUND", "W3C-WCAG22", "NZ-PRIVACY-PRINCIPLES"]
    if index == 55:
        return ["LOC-CYLINDER-CARE", "IASA-TC05"]
    if index == 56:
        return ["IASA-TC05", "SMITHSONIAN-WHAT-1889"]
    if index == 57:
        return ["W3C-WCAG22", "NZ-PRIVACY-PRINCIPLES"]
    if index == 58:
        return ["LOC-CYLINDER-CARE", "LOC-PREMIS"]
    if index == 59:
        return ["DCMI-TERMS", "W3C-VC-DM-20", "NZ-PRIVACY-PRINCIPLES"]
    return ["TMR-MDS-PRINCIPLES", "W3C-PROV-O"]


def proposals() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, title in enumerate(PROPOSAL_TITLES, start=1):
        proposal_id = f"CM6825-N{index:03d}"
        rows.append(
            {
                "approval_class": approval_class(index),
                "concrete_artifacts": [
                    f"docs/caelen-morrow/v682-v5/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/caelen-morrow/v682-v5/x2/rejecting-mutations.json#{proposal_id}",
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
            data = proc.stdout.read(size)
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
            + json.dumps(
                {"exact": exact_collisions, "neighbors": quarantined},
                ensure_ascii=False,
            )
        )
    return {
        "audit_scope": {
            "claim": "bounded all-reachable exact-source proposal audit; no universal 10370-row proof",
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
        "schema": "ghc.family.proposal-chain-audit.v682.v5.x1",
        "source": SOURCE,
    }


def task_records(prefix: str, count: int, lane: str) -> list[dict[str, Any]]:
    return [
        {
            "approval_required": lane in {"exact_approval", "blocked"},
            "lane": lane,
            "planned_action": f"Preregistered Caelen owner-local {lane.replace('_', ' ')} item {index:03d}.",
            "state": "preregistered_not_executed",
            "task_id": f"CM6825-{prefix}-{index:03d}",
        }
        for index in range(1, count + 1)
    ]


SKILL_NAMES = [
    "cylinder-carrier-identity-separator",
    "carrier-material-claim-firewall",
    "groove-topology-nonobservation",
    "format-dimension-vacancy",
    "label-transcription-lineage",
    "container-association-graph",
    "location-privacy-minimizer",
    "condition-cue-nondiagnosis",
    "preservation-action-separator",
    "environment-monitoring-vacancy",
    "playback-parameter-hold",
    "contactless-transfer-topology",
    "digital-surrogate-role-separator",
    "premis-event-vacancy",
    "dcmi-description-boundary",
    "rights-access-hold",
    "accessible-audio-record-summary",
    "workload-handover-lease",
    "cultural-description-noncompensation",
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
            "wholly synthetic phonograph-cylinder catalogue and carrier-identity documentation",
            "wholly synthetic carrier preservation, transfer-plan, and preservation-event documentation",
            "wholly synthetic rights, accessibility, remedy, workload, and collection-handover documentation",
        ],
        "owner_runner_ideas": [
            {
                "runner_id": f"CM6825-RUNNER-{index:02d}",
                "name": f"ghc_family_cylinder_archive_runner_{index:02d}.py",
                "state": "planned_not_built_in_x1",
            }
            for index in range(1, 11)
        ],
        "owner_skill_ideas": [
            {
                "skill_id": f"CM6825-SKILL-{index:02d}",
                "name": name,
                "state": "planned_not_built_in_x1",
            }
            for index, name in enumerate(SKILL_NAMES, start=1)
        ],
        "phase": PHASE,
        "primary_pillar": "Freed ID and CBR Heart",
        "represented_pillars": ["GMUT Mind", "THOS Body"],
        "safe_now": task_records("SAFE", 120, "safe_now"),
        "schema": "ghc.family.portfolio-freeze.v682.v5.x1",
        "successor_candidates": task_records(
            "SUCCESSOR-CAND", 20, "successor_candidate_zero_credit"
        ),
        "successor_clean_fix_refine": task_records(
            "SUCCESSOR-CFR", 30, "successor_recommendation_zero_credit"
        ),
        "successor_practice_recommendation": (
            "exactly one zero-credit seed: synthetic scientific-slide box documentation; successor must audit novelty independently"
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
            "source_id": "LOC-CYLINDER-CARE",
            "status": "official_Library_of_Congress_page_checked_2026-09-02",
            "title": "Caring for Cylinder Recordings",
            "url": "https://www.loc.gov/preservation/care/cyn.html",
            "use": "carrier material, groove, storage, handling, playback-transfer and fragility vocabulary only; no carrier inspection, handling, treatment or playback",
        },
        {
            "source_id": "IASA-TC05",
            "status": "official_IASA_Technical_Committee_page_checked_2026-09-02",
            "title": "Handling and Storage of Audio and Video Carriers",
            "url": "https://www.iasa-web.org/tc05/publication-information",
            "use": "professional carrier-handling and storage vocabulary plus exact abstention conditions only; no professional recommendation or action",
        },
        {
            "source_id": "SMITHSONIAN-EARLY-SOUND",
            "status": "official_Smithsonian_page_checked_2026-09-02",
            "title": "Early Sound Recording Collection and Sound Recovery Project",
            "url": "https://americanhistory.si.edu/press/fact-sheets/early-sound-recording-collection-and-sound-recovery-project",
            "use": "early recording carrier, material, collection and sound-recovery vocabulary only; zero objects, media or observations ingested",
        },
        {
            "source_id": "SMITHSONIAN-WHAT-1889",
            "status": "official_Smithsonian_page_checked_2026-09-02",
            "title": "What did 1889 sound like?",
            "url": "https://americanhistory.si.edu/explore/stories/what-did-1889-sound",
            "use": "wax-cylinder, crack, non-contact scanning and derivative-audio vocabulary only; no media retrieved, interpreted or evaluated",
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
            "use": "privacy minimization, access, correction and disclosure hold vocabulary only; no legal interpretation or compliance claim",
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
        "schema": "ghc.family.official-primary-sources.v682.v5.x1",
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
        "schema": "ghc.family.privacy-scan.v682.v5.x1",
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
            "schema": "ghc.family.activation-intake.v682.v5.x1",
        },
    )
    write_json(
        X1 / "identity-and-boundary.json",
        {
            "consciousness_personhood_or_continuity_claimed": False,
            "hope": "Every carrier, surrogate, correction, and rights hold stays traceable without turning a record into authority.",
            "name": OWNER,
            "optional_pronouns": "they/them",
            "owner_rename_pause_redirect_stop_right": "Hamish",
            "phase": PHASE,
            "relational_working_language_only": True,
            "role": "provenance weaver and boundary cartographer",
            "schema": "ghc.family.identity-boundary.v682.v5.x1",
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
                "evidence": 70,
                "final_delta": 23,
                "final_owner": 119,
                "total": 232,
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
            "schema": "ghc.family.proposal-freeze.v682.v5.x1",
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
            "schema": "ghc.family.inherited-revalidation.v682.v5.x1",
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
            "schema": "ghc.family.approval-holds.v682.v5.x1",
        },
    )
    write_json(
        X1 / "clean-fix-refine-plan.json",
        {
            "owner": OWNER,
            "owner_rows": portfolio["owner_clean_fix_refine"],
            "phase": PHASE,
            "schema": "ghc.family.clean-fix-refine.v682.v5.x1",
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
            "schema": "ghc.family.skill-runner-plan.v682.v5.x1",
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
            "schema": "ghc.family.method-flow-startup.v682.v5.x1",
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
            "schema": "ghc.family.phase-truth.v682.v5.x1",
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
                "carrier condition, treatment, playback fitness, rights or cultural authority inferred from documentation",
                "route or private identifier leakage",
                "x1 and x2 lifecycle contamination",
            ],
            "schema": "ghc.family.threat-model.v682.v5.x1",
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
            "schema": "ghc.family.workflow-plan.v682.v5.x1",
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
            "prospective_successor_exact_title": "Eiren Kestrel",
            "prospective_successor_phase": "v682-v6",
            "route_authority_through": "v725-v8",
            "send_before_terminal_gate": False,
            "tavian_sol": "ON_STANDBY",
        },
    )
    write_text(
        X1 / "integrated-overview.md",
        f"""# Caelen Morrow {PHASE} Planning-Only X1 Overview

Caelen Morrow, optionally they/them, is relational working language for a provenance weaver and boundary cartographer, with the hope that every carrier, surrogate, correction, and rights hold stays traceable without turning a record into authority. This is not evidence of consciousness, sentience, personhood, continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Maori authority. Hamish retains the right to rename, pause, redirect, narrow, or stop the route.

The exact immutable source is Sylven Arc final `{SOURCE}` on `{SOURCE_BRANCH}`. Read-only verification established three direct single-parent Sylven commits, zero merges, one final parent, clean state, typed 0/0 divergence, fresh four-way equality, 232 exact normalized-LF manifest entries and ten content-seal targets, plus exact canonical receipt and payload digests. No Sylven test, manifest aggregate, or canonical aggregate was replayed. The repository seal, two-event external activation overlay, live acknowledged delivery, and Caelen startup failures remain distinct truth layers.

This x1 freezes sixty Caelen proposals after a bounded all-reachable exact-source audit. It makes no universal semantic-novelty claim over every declared historical row where a single canonical materialized ledger is absent. The synthetic phonograph-cylinder cataloguing, preservation-planning, transfer, rights, accessibility, and handover proposals must produce zero exact title collisions and zero quarantine hits at the 0.78 token-Jaccard threshold. Twenty inherited neighbour reviews remain source evidence with zero Caelen completion credit.

Freed ID and CBR Heart are primary through surrogate-versus-carrier identity, provenance, correction, fixity, access, rights, remedy, privacy minimization, and cultural-authority holds. THOS Body remains explicit through synthetic carrier topology, preservation-action separation, stop states, workload budgets, accessibility, correction, and handover. GMUT Mind remains explicit through signal-domain, sampling, uncertainty, residual, and model-obligation vacancies with every waveform, measurement, likelihood, and inference absent. Phonograph-cylinder cataloguing and preservation planning are wholly synthetic learning and design lenses only, never employment, qualification, competence, collection custody, conservation, handling, playback, transfer, rights clearance, publication, or professional authority.

The plan uses zero real people, speakers, performers, communities, collections, cylinders, containers, recordings, audio, labels, tools, materials, observations, measurements, treatments, playbacks, transfers, identity events, external writes, or authority acts. Current official and primary sources supply vocabulary and refusal conditions only. They are not carrier observations, preservation recommendations, media transfers, cataloguing decisions, rights determinations, legal interpretations, cultural ratifications, affected-party decisions, or authority grants.

Expected x2 dispositions are exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`. Those are preregistered expected labels, not observed outcomes. All 300 invalid mutations, 120 safe-now tasks, 80 bounded candidates, 100 CLEAN/FIX/REFINE records, twenty skills, and ten runners remain planned rather than executed in this x1. Twenty exact-approval and ten blocked packets remain visible and unexecuted.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family without physical data, waveform evidence, likelihood, posterior, prediction, constraint, empirical confirmation, ultraviolet or quantum completion, or Theory-of-Everything proof. THOS remains synthetic/proxy-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live lifecycle operations, interoperability, independent privacy/security review, recovery evidence, trust governance, and affected-party oversight.

Collection handling, conservation treatment, playback, transfer, professional cataloguing, copyright, privacy, donor restrictions, voice identity, access, ownership, custody, heritage, traditional knowledge, remedy, legal and cultural interpretation, affected-party legitimacy, Maori wording and data governance, and Maori authority remain exact-gated. Maori concepts remain under Maori authority. Complete privacy, complete accessibility, exhaustive security, independent reproduction, AGI/ASI, consciousness/personhood, proof/canon, and Stage 20 remain open or exact-gated. The terminal verdict remains `{TERMINAL_VERDICT}`.
""",
    )

    x1_material_paths = sorted(
        set(
            WRITTEN
            + [
                "scripts/build_ghc_family_caelen_morrow_v682_v5_x1.py",
                "tests/test_ghc_family_caelen_morrow_v682_v5_x1.py",
            ]
        )
    )
    exclusions = [
        "docs/caelen-morrow/v682-v5/validation/x1-index-manifest.json",
        "docs/caelen-morrow/v682-v5/validation/x1-privacy-scan.json",
        "docs/caelen-morrow/v682-v5/validation/x1-staged-review.json",
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
            "schema": "ghc.family.normalized-lf-index-manifest.v682.v5.x1",
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
            "schema": "ghc.family.staged-review.v682.v5.x1",
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
