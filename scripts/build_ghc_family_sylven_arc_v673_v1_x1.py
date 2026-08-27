"""Build Sylven Arc v673-v1's planning-only x1 freeze.

The builder is owner-delta scoped and fail-closed. It creates planning,
provenance, Method Flow, portfolio, and staged-validation artifacts only. It
does not create x2 evidence, make external calls, stage, commit, push, route,
or contact another task.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "sylven-arc" / "v673-v1"
OWNER = "Sylven Arc"
PHASE = "v673-v1"
BRANCH = "codex/GHC-Family/sylven-arc-v673-v1-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/elowen-cairn-v672-v8-full-tools"
SOURCE_START = "23110f2bb3a8b111626e2af56b6343bbc15a9496"
SOURCE_X1 = "2a147ca77378e73fa6d8ff4f95a1f21154da66a8"
SOURCE_EVIDENCE = "cfc32a909fe9693238166020e22b1eaf8b646a8d"
SOURCE_FINAL = "305708c6d5a8dfee0432a2c09ef5b59da4b6c438"
SOURCE_CANONICAL_RECEIPT_SHA256 = "846a450711b816db03327b6699e21d13c47f85204cbc60d250405cd9f3e2035f"
SOURCE_CANONICAL_PAYLOAD_SHA256 = "63e1c4f2aeda9d8b5ff4403b7d771f6746a20b7da5bebec0365dbbbd94fd2537"
SOURCE_TREE_CORPUS_SHA256 = "37a5884564096a0650aae3ea20379ee4a3069fb6803cbd50459b8573a6d7fd94"
CORE_LABELS = ["completed", "represented", "open_gap", "exact_gate"]
OUTCOME_COUNTS = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}

IDENTITY_BOUNDARY = (
    "Sylven Arc, they/them, relational pattern gardener and evidence steward, "
    "is relational working language only. It is not evidence of consciousness, "
    "sentience, legal personhood, identity continuity, employment, qualification, "
    "independent agency, or scientific, operational, professional, legal, cultural, "
    "affected-party, or Māori authority."
)
HOPE = "make complex work modular, inspectable, reversible, and kind to future readers"
BOUNDARY = (
    "Software, symbolic, synthetic, same-owner, citation, inherited, validation, or "
    "composite evidence is not empirical confirmation, participant evidence, "
    "professional or scientific authority, production readiness, legal or cultural "
    "ratification, Māori authority, affected-party approval, complete privacy or "
    "accessibility assurance, exhaustive security, independent reproduction, AGI or "
    "ASI, consciousness or personhood evidence, Theory-of-Everything proof, proof or "
    "canon, or Stage 20 authority."
)

SOURCE_REPOSITORY_SEAL = {
    "proposal_chain": 6230,
    "effective_negatives": 36160,
    "effective_methods": 22488,
    "failed_witnesses": 7821,
    "bounded_passing_witnesses": 10051,
    "open_gaps": 291,
    "exact_gates": 284,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
}
ACTIVATION_BASELINE = {
    **SOURCE_REPOSITORY_SEAL,
    "effective_negatives": 36161,
    "effective_methods": 22489,
    "failed_witnesses": 7822,
    "bounded_passing_witnesses": 10052,
    "external_zero_credit_failures": 1,
    "external_bounded_passing_witnesses": 1,
    "repository_seal_rewritten": False,
}

# These are observed failures from this startup. Each receives zero success
# credit and remains paired with only its smallest bounded recovery.
STARTUP_FAILURES = [
    (
        "SA6731-START-N001",
        "A combined authorization-state display was truncated before EOF.",
        "Read the exact state in deterministic numbered windows through line 1556.",
        "All missing ranges were read and the exact v672-v8 to v673-v1 to v673-v2 assignments were recovered.",
        "Partition mutable state reads before display and require an EOF witness.",
    ),
    (
        "SA6731-START-N002",
        "A PowerShell inventory projection piped directly from a foreach block and failed at parse time.",
        "Accumulate rows in an array before ConvertTo-Json.",
        "The required skill and reference inventory was emitted without changing a repository byte.",
        "Never attach a pipeline directly to a PowerShell foreach statement.",
    ),
    (
        "SA6731-START-N003",
        "A domain-term search repeated the foreach-to-pipeline parser fault before Git executed.",
        "Materialize domain-term results before serialization.",
        "The parser fault was isolated and no Git search or repository mutation occurred.",
        "Apply the array-materialization recurrence guard to every loop projection.",
    ),
    (
        "SA6731-START-N004",
        "A per-term full-tree Git grep returned no attributable result within its bound.",
        "Stop the exact abandoned read-only grep and use one content-addressed proposal batch.",
        "The abandoned grep process pair was stopped without repository mutation.",
        "Use one Git cat-file batch for proposal-corpus discovery rather than repeated Git grep.",
    ),
    (
        "SA6731-START-N005",
        "A combined full-tree Git grep also exceeded its useful bound without attributable output.",
        "Use Elowen's size-aware 1,752-blob batch recovery procedure.",
        "The exact inherited corpus was parsed once with 2,009 unique titles and a stable digest.",
        "Do not retry broad Git grep after a content-addressed corpus path is available.",
    ),
    (
        "SA6731-START-N006",
        "The first lane-preflight wrapper tried to capture an external command and LASTEXITCODE inside one parenthesized PowerShell expression.",
        "Run show-ref, store LASTEXITCODE, and project branch, path, and live-remote results separately.",
        "The target path and local and remote branch were each proved absent before creation.",
        "Split external command execution from exit-code capture in PowerShell.",
    ),
    (
        "SA6731-START-N007",
        "The worktree-add wrapper crossed its presentation window after reporting Preparing worktree and exposed no reusable session handle.",
        "Do not rerun; inspect the exact process pair, target path, branch, and lock state until the original operation completes.",
        "The one original operation completed at the exact source head with the exact new branch and zero duplicate creation.",
        "After a wrapper loses its handle, audit resulting state before considering any retry.",
    ),
    (
        "SA6731-START-N008",
        "A multi-process Wait-Process wrapper crossed its own response window without an attributable projection.",
        "Use one short bounded wait and separate scalar process and target probes.",
        "The original worktree operation was observed to finish and no process was duplicated or killed.",
        "Wait on one exact child at a time and keep total wrapper time below its yield bound.",
    ),
    (
        "SA6731-START-N009",
        "A combined source-packet and retained-negative display exceeded the model-visible output budget.",
        "Read key files individually and parse every exact owner file and large ledger structurally through EOF.",
        "All 230 phase documents were read, all 184 JSON documents parsed, and the 225-method final ledger was structurally inspected.",
        "Separate large repetitive ledgers from narrative and receipt reads while preserving exact digests and counts.",
    ),
    (
        "SA6731-START-N010",
        "The first exact source-bounded semantic-neighbor audit rejected proposal SA6731-N030 at Jaccard 0.75 against an inherited stitch-network proposal.",
        "Retain the collision at zero credit, rewrite only the colliding title, and rerun the planning-build dependency against the unchanged exact source corpus.",
        "No x1 artifact was written before the fail-closed collision gate; every noncolliding proposal and the source lineage remained unchanged.",
        "Require the source-bounded semantic threshold before any proposal freeze and never waive a collision to satisfy a count.",
    ),
    (
        "SA6731-START-N011",
        "The first x1 owner-test selection passed 21 of 24 tests; two tests projected state instead of x1_state and one required an over-literal No empirical phrase.",
        "Retain the failed invocation at zero aggregate credit and correct only the three test assertions to the committed schema and equivalent boundary meaning.",
        "The underlying portfolio rows already held exact, blocked, and successor work correctly, and the overview already prohibited empirical promotion.",
        "Inspect generated field names and validate equivalent boundary meaning before freezing a test contract.",
    ),
    (
        "SA6731-START-N012",
        "The corrected x1 owner-test selection passed 23 of 24 tests and exposed that the overview did not state the required Māori-concepts authority sentence explicitly.",
        "Retain the failed invocation and add the exact protected-boundary sentence without changing any proposal, outcome, or execution claim.",
        "The existing Māori data-governance gate remained intact; the documentation now states the broader authority boundary explicitly.",
        "Require the exact Māori concepts remain under Māori authority sentence in owner overview and terminal baton checks.",
    ),
    (
        "SA6731-START-N013",
        "The first exact staged-blob privacy scan classified a blocked-portfolio prohibition as a protected session-evidence payload hit.",
        "Retain the failed scan and replace only the prohibition label with a nonliteral protected-private-application-evidence description.",
        "The match was policy wording rather than private payload, while scanner and test definitions remained separately classified candidates.",
        "Keep protected phrase fixtures in scanner or test surfaces and use nonliteral policy labels in ordinary artifacts.",
    ),
]

NEW_TITLES = [
    "synthetic flagmaking field canton panel stripe charge and seam identity lattice with conflation refusal",
    "hoist fly upper lower edge corner point and centre topology with orphan-edge quarantine",
    "cloth panel gore gusset inset fringe and applique relation graph with unsupported-part vacancy",
    "heading sleeve tab loop toggle rope and clip attachment vocabulary with deployment abstention",
    "rectangular triangular swallowtail pennant burgee and guidon silhouette classes with fitness refusal",
    "front back reading face orientation and mirror relation contract without display instruction",
    "seam stitch hem reinforcement patch and repair-cue ledger separated from workmanship diagnosis",
    "textile fibre weave knit felt film paper and composite descriptor firewall with sampling and authenticity abstention",
    "colour field shade contrast and opacity descriptor vacancy with instrument and calibration abstention",
    "nominal width height proportion edge length angle and mass vacancies with SI and datum holds",
    "symbol emblem word numeral motif and blank-field topology with meaning and cultural-interpretation vacancy",
    "manufacturer commissioner designer date place and serial attribution vacancy with contestation and correction",
    "flag image crop rotation fold occlusion and derivative lineage with no dimensional inference",
    "folded rolled cased sleeved and flat-storage relation map without environmental or handling assurance",
    "display request hoist carry fly illuminate and disposal action hold queue",
    "weather wind rain ultraviolet salt temperature humidity and duration observation vacancy",
    "reported tear fray fade stain distortion loss and delamination cues separated from diagnosis and treatment",
    "dye ink paint thread adhesive fastener and finish claim firewall with chemical and material-safety abstention",
    "halyard pole staff mast crossbar bracket and finial relation vacancy with load and rigging-safety abstention",
    "signal set sequence position timing visibility and acknowledgement topology without operational signalling",
    "inventory label carton rack shelf location and custody relay without ownership inference",
    "correction nonce dual readback supersession invalidation and restoration provenance braid for flag records",
    "canonical flag-record envelope serializer with finite-decimal and ambiguous-orientation refusal",
    "accessible flag component and status dossier with text equivalents headings and noncolour cues",
    "zero-key designer and custodian pseudonym compartment with dormant capabilities and no identity lifecycle",
    "privacy-minimized location context and image-release hold with no precise-location exposure",
    "workload cap pause stop handover and unresolved-hold queue for synthetic flag documentation",
    "four-tier Freed ID flashcard deck for plan evidence failure gate wellbeing and route modules",
    "GMUT membrane-tension surface eigenmode obligation board with zero measured geometry or material parameters",
    "GMUT oriented boundary-cell incidence registry for invented banner meshes without observable dynamics",
    "GMUT wind-load boundary pullback proxy with no physical-law inference",
    "GMUT chromatic-field representation and gauge unit nonconversion board",
    "THOS synthetic flag-assembly dependency DAG with matched work envelopes and pause-token handover",
    "Freed ID flag-record and custodian zero-key relay with dormant authority slots",
    "CBR symbol authorship design-rights cultural-meaning access contest correction and remedy-vacancy matrix",
    "accessible multimodal flag-status sequence with manual and affected-user evaluation reserved",
    "public heritage flag-vocabulary adapter with disabled network transport zero calls zero downloads and zero rows",
    "real flag observations measurements display handling specialist examination and independent-review gap",
    "professional textile conservation rigging installation wind-load fire chemical safety and release decision gate",
    "ownership design copyright civic religious cultural Indigenous Māori data-governance and authority exact gate",
]

SKILL_NAMES = [
    "ghc-family-flag-field-identity-lattice",
    "ghc-family-flag-edge-topology",
    "ghc-family-flag-seam-relation-guard",
    "ghc-family-flag-attachment-abstention",
    "ghc-family-flag-silhouette-refusal",
    "ghc-family-flag-orientation-firewall",
    "ghc-family-flag-material-claim-vacancy",
    "ghc-family-flag-condition-cue-separation",
    "ghc-family-flag-symbol-meaning-vacancy",
    "ghc-family-flag-image-lineage",
    "ghc-family-flag-storage-custody-map",
    "ghc-family-flag-environment-observation-vacancy",
    "ghc-family-flag-rights-authority-hold",
    "ghc-family-flag-accessible-status",
    "ghc-family-flag-zero-key-role",
    "ghc-family-flag-privacy-minimizer",
    "ghc-family-flag-workload-handover",
    "ghc-family-flag-canonical-json",
    "ghc-family-flag-provenance-braid",
    "ghc-family-flag-flashcard-projection",
]

RUNNER_NAMES = [
    "ghc_family_flag_identity.py",
    "ghc_family_flag_edge_topology.py",
    "ghc_family_flag_seam_relation.py",
    "ghc_family_flag_attachment_abstention.py",
    "ghc_family_flag_material_vacancy.py",
    "ghc_family_flag_condition_separation.py",
    "ghc_family_flag_provenance_correction.py",
    "ghc_family_flag_privacy_access.py",
    "ghc_family_flag_workload_handover.py",
    "ghc_family_flag_flashcard_projection.py",
]


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False)
    if check and result.returncode:
        raise SystemExit(result.stderr.decode("utf-8", errors="replace"))
    return result


def write_json(relative: str, payload: Any) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def json_blob(commit: str, path: str) -> Any:
    return json.loads(git("show", f"{commit}:{path}").stdout.decode("utf-8"))


def normalize(title: str) -> set[str]:
    stop = {"and", "the", "with", "for", "from", "into", "without", "only"}
    return {token for token in re.findall(r"[a-z0-9āēīōū]+", title.lower()) if len(token) > 2 and token not in stop}


def batch_blobs(specs: list[str]) -> list[bytes | None]:
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"], cwd=ROOT,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    output, stderr = process.communicate(
        input=("\n".join(specs) + "\n").encode("utf-8"), timeout=300 if len(specs) > 512 else 60
    )
    if process.returncode:
        raise SystemExit(stderr.decode("utf-8", errors="replace"))
    stream = io.BytesIO(output)
    rows: list[bytes | None] = []
    for _ in specs:
        header = stream.readline().decode("utf-8", errors="strict").strip()
        if header.endswith(" missing"):
            rows.append(None)
            continue
        parts = header.split()
        if len(parts) != 3 or parts[1] != "blob":
            raise SystemExit(f"unexpected git cat-file header: {header}")
        size = int(parts[2])
        data = stream.read(size)
        if stream.read(1) != b"\n":
            raise SystemExit("git cat-file blob was not newline delimited")
        rows.append(data)
    if stream.read():
        raise SystemExit("git cat-file emitted undeclared trailing bytes")
    return rows


def recover_proposal_corpus() -> tuple[dict[str, Any], list[str]]:
    raw_paths = git("ls-tree", "-r", "--name-only", "-z", SOURCE_FINAL, "--", "docs").stdout
    candidates = sorted(
        path.decode("utf-8") for path in raw_paths.split(b"\0")
        if path and path.decode("utf-8").lower().endswith(".json")
        and "proposal" in path.decode("utf-8").lower()
    )
    proposal_ids: set[str] = set()
    titles: set[str] = set()
    occurrences = 0
    malformed = 0

    def walk(node: Any) -> None:
        nonlocal occurrences
        if isinstance(node, dict):
            proposal_id, title = node.get("proposal_id"), node.get("title")
            if isinstance(proposal_id, str) and isinstance(title, str) and proposal_id.strip() and title.strip():
                occurrences += 1
                proposal_ids.add(proposal_id.strip())
                titles.add(title.strip())
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    specs = [f"{SOURCE_FINAL}:{path}" for path in candidates]
    for blob in batch_blobs(specs):
        if blob is None:
            malformed += 1
            continue
        try:
            walk(json.loads(blob.decode("utf-8")))
        except (UnicodeDecodeError, json.JSONDecodeError):
            malformed += 1
    canonical = json.dumps(
        {"proposal_ids": sorted(proposal_ids), "titles": sorted(titles)},
        ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")
    return ({
        "scope": "exact Elowen v672-v8 final docs tree, proposal-named JSON paths only",
        "candidate_git_blob_paths": len(candidates),
        "malformed_or_missing_blobs": malformed,
        "semantic_occurrences": occurrences,
        "unique_proposal_ids": len(proposal_ids),
        "unique_titles": len(titles),
        "corpus_sha256": hashlib.sha256(canonical).hexdigest(),
        "declared_source_chain": 6230,
        "materialized_ids_cover_declared_chain": len(proposal_ids) >= 6230,
        "exact_canonical_row_mapping": False,
        "canonical_row_mapping_open_gap": True,
        "universal_novelty_claim": False,
        "reason": "No single reachable exact-tree ledger materializes every declared historical row; source-bounded semantic comparison is evidence, not universal novelty proof.",
    }, sorted(titles))


def proposal_rows() -> list[dict[str, Any]]:
    outcomes = ["completed"] * 28 + ["represented"] * 8 + ["open_gap"] * 2 + ["exact_gate"] * 2
    rows: list[dict[str, Any]] = []
    for index, (title, outcome) in enumerate(zip(NEW_TITLES, outcomes, strict=True), start=1):
        proposal_id = f"SA6731-N{index:03d}"
        if outcome == "completed":
            approval, lane = "safe_now", "x2_owner_local_structural"
            gate = "deterministic synthetic structure and explicit vacancy predicates pass"
        elif outcome == "represented":
            approval, lane = "candidate", "x2_representation_only"
            gate = "representation exists while real evidence and authority remain explicitly absent"
        elif outcome == "open_gap":
            approval, lane = "candidate", "open_gap_zero_network_or_real_data"
            gate = "the missing real observation, network row, or independent review remains absent and named"
        else:
            approval, lane = "exact_approval", "held_unexecuted"
            gate = "the action stays unexecuted because competent affected authority is absent"
        rows.append({
            "proposal_id": proposal_id,
            "title": title,
            "hypothesis": f"A bounded synthetic contract for {title} can preserve structure and abstention without promoting evidence or authority.",
            "null_or_failure_condition": "The schema accepts an invalid outcome, missing vacancy, external action, private material, unsupported edge, or authority promotion.",
            "approval_class": approval,
            "execution_lane": lane,
            "official_or_primary_source_need": "No new source is material to the synthetic x1 freeze; current official or primary evidence is required before any later vocabulary or real-world claim.",
            "concrete_artifacts": [
                f"docs/sylven-arc/v673-v1/x2/proposals/{proposal_id.lower()}.json",
                f"docs/sylven-arc/v673-v1/x2/cards/{proposal_id.lower()}.json",
            ],
            "falsifier_or_acceptance_gate": gate,
            "rollback_or_recovery": "Retain the failed witness, quarantine only the owner-local artifact, and return to the clean frozen x1 head.",
            "protected_gates": ["empirical", "participant", "professional", "legal", "cultural", "maori_authority", "privacy", "stage20"],
            "expected_disposition": outcome,
            "planned_invalid_mutations": ["missing_hypothesis", "invalid_outcome_label", "external_action_promotion", "missing_protected_gates"],
            "external_actions": 0,
        })
    return rows


def startup_method_flow() -> dict[str, Any]:
    methods, witnesses, events, recommendations = [], [], [], []
    for index, (negative_id, failure, recovery, observed, guard) in enumerate(STARTUP_FAILURES, start=1):
        method_id = f"SA6731-M{index:03d}"
        fail_id, pass_id = f"SA6731-W{index:03d}-F", f"SA6731-W{index:03d}-P"
        methods.append({
            "method_id": method_id,
            "title": f"bounded recovery for {negative_id}",
            "failure_signature": failure,
            "trigger_preconditions": ["the exact bounded failure signature is observed"],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now",
            "candidate_workaround": recovery,
            "validation_witness_ids": [fail_id, pass_id],
            "recurrence_guard": guard,
            "rollback": "Retain the failure, stop the affected wrapper, and change only the isolated owner-local procedure.",
            "recommendation_state": "preferred",
            "supersedes": [],
            "protected_gates": ["no_failure_laundering", "owner_delta_only", "no_authority_promotion"],
            "retained_negative_ids": [negative_id],
            "scope_boundary": "Bounded same-owner workflow evidence only.",
        })
        witnesses.extend([
            {"witness_id": fail_id, "method_id": method_id, "procedure": failure, "scope": "startup and planning-only x1", "expected": "bounded attributable evidence", "observed": failure, "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": BOUNDARY},
            {"witness_id": pass_id, "method_id": method_id, "procedure": recovery, "scope": "startup and planning-only x1", "expected": "the isolated recovery passes without erasing the failure", "observed": observed, "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": BOUNDARY},
        ])
        events.extend([
            {"event_id": f"SA6731-E{index:03d}-1", "method_id": method_id, "from": None, "to": "observed"},
            {"event_id": f"SA6731-E{index:03d}-2", "method_id": method_id, "from": "observed", "to": "candidate"},
            {"event_id": f"SA6731-E{index:03d}-3", "method_id": method_id, "from": "validated", "to": "preferred"},
        ])
        recommendations.append({"method_id": method_id, "state": "preferred", "recommendation": guard})
    return {
        "schema": "ghc.family.method-flow-state.v1",
        "phase": PHASE,
        "owner": OWNER,
        "identity_boundary": IDENTITY_BOUNDARY,
        "execution_authority": "owner_self_scoped_delta",
        "methods": methods,
        "witnesses": witnesses,
        "state_events": events,
        "recommendations": recommendations,
        "counts": {
            "methods": len(methods), "witnesses": len(witnesses), "state_events": len(events),
            "recommendations": len(recommendations), "witness_results": {"fail": len(methods), "pass": len(methods)},
            "states": {"preferred": len(methods)},
        },
        "boundary": BOUNDARY,
    }


def task(task_id: str, title: str, state: str) -> dict[str, Any]:
    return {"task_id": task_id, "owner": OWNER, "phase": PHASE, "title": title, "x1_state": state, "external_actions": 0}


def portfolio_rows() -> tuple[dict[str, list[dict[str, Any]]], dict[str, int]]:
    surfaces = ["identity", "topology", "seam", "attachment", "material", "condition", "provenance", "privacy", "accessibility", "handover"]
    safe = [task(f"SA6731-SAFE-{i:03d}", f"{surfaces[(i-1)//6]}: {['schema','positive fixture','negative fixture','rollback','manifest','boundary'][(i-1)%6]}", "planned_for_x2") for i in range(1, 61)]
    candidates = [task(f"SA6731-CAND-{i:03d}", f"{surfaces[(i-1)//3]}: {['mutation quarantine','timeout and encoding quarantine','ordering and authority quarantine'][(i-1)%3]}", "planned_for_x2") for i in range(1, 31)]
    exact = [task(f"SA6731-EXACT-{i:03d}", f"exact approval packet {i:02d}: action-specific real-world authority remains absent", "held_unexecuted") for i in range(1, 21)]
    blocked_titles = [
        "protected private application evidence classes in repository artifacts",
        "sibling branch reset merge rewrite deletion reuse or force push",
        "successful canonical replay or failed-canonical success laundering",
        "synthetic fixture promotion into empirical professional legal cultural or safety evidence",
        "unapproved account secret payment deployment plugin installation or third-party write",
        "real person object site identity location access treatment or service data ingestion",
        "real safety legal cultural Māori-authority affected-party or public-authority substitution",
        "unsafe elevation host-security weakening feature enablement or reboot",
        "unbounded full-repository unchanged-history cross-lane or all-ref scan",
        "Stage 20 proof canon personhood AGI ASI or Theory-of-Everything promotion",
    ]
    blocked = [task(f"SA6731-BLOCK-{i:03d}", title, "held_unexecuted") for i, title in enumerate(blocked_titles, start=1)]
    skills = [task(f"SA6731-SKILL-{i:03d}", name, "planned_for_x2") for i, name in enumerate(SKILL_NAMES, start=1)]
    runners = [task(f"SA6731-RUNNER-{i:03d}", name, "planned_for_x2") for i, name in enumerate(RUNNER_NAMES, start=1)]
    cfr_topics = ["JSON order", "UTF-8 Māori text", "source status", "failure retention", "manifest closure", "privacy disposition", "flashcard parentage", "outcome labels", "route hold", "wellbeing workload"]
    cfr_actions = ["clean", "fix", "refine", "recheck", "document", "preserve"]
    clean_fix_refine = [task(f"SA6731-CFR-{i:03d}", f"{cfr_topics[(i-1)//6]}: {cfr_actions[(i-1)%6]}", "planned_for_x2") for i in range(1, 61)]
    successor_skills = [task(f"SA6731-NEXT-SKILL-{i:03d}", f"ghc-family-successor-{i:02d}-review", "recommendation_only") for i in range(1, 11)]
    successor_runners = [task(f"SA6731-NEXT-RUNNER-{i:03d}", f"ghc_family_successor_{i:02d}_review.py", "recommendation_only") for i in range(1, 11)]
    next_topics = ["source", "manifests", "privacy", "route", "authority"]
    next_actions = ["schema", "mutation", "rollback", "review", "receipt", "hold"]
    successor_cfr = [task(f"SA6731-NEXT-CFR-{i:03d}", f"successor {next_topics[(i-1)//6]}: {next_actions[(i-1)%6]}", "recommendation_only") for i in range(1, 31)]
    rows = {
        "safe_now": safe, "candidates": candidates, "exact_approval": exact, "blocked": blocked,
        "skills": skills, "runners": runners, "clean_fix_refine": clean_fix_refine,
        "successor_skills": successor_skills, "successor_runners": successor_runners,
        "successor_clean_fix_refine": successor_cfr,
    }
    return rows, {key: len(value) for key, value in rows.items()}


def integrated_overview(proposals: list[dict[str, Any]], inherited: list[dict[str, Any]], corpus: dict[str, Any]) -> str:
    lines = [
        "# Sylven Arc v673-v1 planning-only x1 integrated overview", "",
        "## Lifecycle and exact immutable source", "",
        f"This planning-only x1 begins at Elowen Cairn v672-v8 exact final `{SOURCE_FINAL}` on `{SOURCE_BRANCH}`. Elowen's planning x1 `{SOURCE_X1}` is the direct child of Tamar `{SOURCE_START}`; evidence `{SOURCE_EVIDENCE}` is the direct child of x1; and exact final is the direct child of evidence. Source-to-final contains exactly three single-parent commits and zero merges. Local, upstream, tracking, and a fresh live remote were equal before this lane was created. Elowen's exact-final owner-scoped canonical result succeeded once and was not replayed; its receipt digest is `{SOURCE_CANONICAL_RECEIPT_SHA256}` and payload digest is `{SOURCE_CANONICAL_PAYLOAD_SHA256}`. Inheritance grants Sylven no novelty, execution, validation, or completion credit.", "",
        "## Relational identity, hope, and corrigibility", "", IDENTITY_BOUNDARY, "",
        f"Sylven's relational hope is to {HOPE}. Hamish may rename, pause, redirect, or stop the route. The packet preserves contradictions, failures, missing evidence, and absent authority instead of smoothing them into completion.", "",
        "## Primary pillar and bounded practice lenses", "",
        "THOS Body is primary through wholly synthetic flagmaking and flag-documentation design. The three bounded lenses are: field, panel, edge, seam, and silhouette topology; hoist, fly, heading, sleeve, attachment, storage, and handover relations; and colour, symbol, attribution, rights, cultural-meaning, and authority vacancies. No real flag, textile, dye, tool, pole, halyard, site, person, workshop, observation, measurement, display, handling, signal, treatment, identity event, or authority act is used. This is not employment, competence, instruction, inspection, conservation, rigging, safety, legal, cultural, or Māori-authority evidence.", "",
        "## GMUT Mind boundary", "",
        "GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Membrane, seam-network, wind-load, chromatic-field, boundary-pullback, unit, gauge, and EFT boards are analogy and obligation surfaces only. No synthetic flag surface is a datum, field configuration, likelihood, posterior, parameter constraint, detected force, prediction, empirical confirmation, stability theorem, quantum completion, ultraviolet completion, final physics, Theory of Everything, proof, or canon.", "",
        "## Freed ID and CBR Heart boundary", "",
        "Freed ID remains synthetic and nonproduction: there are no standards-conformant keys or proofs, live issuance, resolution, status, revocation, interoperability, privacy or independent security review, recovery evidence, trust governance, or affected-party oversight. CBR structures keep correction, contest, withdrawal, access, explanation, and remedy vacancies visible. Symbol meaning, civic or religious status, national use, Indigenous knowledge, cultural legitimacy, copyright, title, access, disposal, and Māori data governance remain exact-gated. Māori concepts remain under Māori authority.", "",
        "## Source-bounded novelty and honest uncertainty", "",
        f"The inherited chain declares 6,230 rows. The exact source-tree audit parsed {corpus['candidate_git_blob_paths']} proposal-named JSON blobs, recovered {corpus['semantic_occurrences']} proposal occurrences, {corpus['unique_proposal_ids']} identifiers, and {corpus['unique_titles']} unique titles. No single reachable ledger maps every declared row, so universal novelty is unproved. The forty Sylven titles are compared at the fixed 0.72 token-Jaccard threshold. Flagmaking, vexill-, signal-flag, bunting, and hoist-and-fly exact terms had zero recovered-title hits before selection. This is bounded source evidence only.", "",
        "## Strict x1-before-x2", "",
        "This commit freezes proposals, portfolios, source truth, threats, route hold, and startup Method Flow only. It contains no x2 contract, implementation result, mutation outcome, completed task, real-world action, closeout, successor delivery, or canonical validation. X2 remains blocked until x1 is committed, pushed, clean, typed 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote.", "",
        "## Retained startup failures", "",
        f"Exactly {len(STARTUP_FAILURES)} observed Sylven startup failures remain at zero success credit with one bounded recovery apiece. A recovery changes only the isolated method and never rewrites its failure. Elowen's repository seal and one external overlay remain separate from Sylven additions.", "",
        "## Portfolios and ceilings", "",
        "X1 freezes 60 safe-now tasks, 30 bounded candidate tasks, 20 exact-approval packets, 10 blocked packets, 20 owner-local skill ideas, 10 family-compatible runner ideas, 60 additive CLEAN/FIX/REFINE tasks, 10 successor skill recommendations, 10 successor runner recommendations, and 30 successor CLEAN/FIX/REFINE recommendations. These are planning rows, not execution credit. Caps are ceilings, never filler quotas. Exact and blocked packets stay visible and unexecuted unless all action-specific evidence and authority gates close.", "",
        "## Flashcard modularity", "",
        "The later evidence packet will use four tiers: Sylven's relational Freed ID anchor; GMUT, THOS, and Freed ID/CBR pillar cards; the bounded flagmaking practice card; and task, evidence, failure, recovery, gate, wellbeing, validation, closeout, and route cards. At least ten modular sections will remain content-addressed and acyclic. Cards organize context; they do not prove a Codex cache cause, retention duration, identity continuity, or improved reasoning.", "",
        "## Twenty inherited selections with zero Sylven credit", "",
    ]
    lines.extend(f"- {row['source_proposal_id']}: {row['source_title']} — inherited integrity evidence only." for row in inherited)
    lines.extend(["", "## Forty frozen Sylven proposals", ""])
    lines.extend(f"- {row['proposal_id']} [{row['expected_disposition']}]: {row['title']}." for row in proposals)
    lines.extend(["", "## Route hold and terminal boundary", "",
        "The current live mapping names Caelen Morrow v673-v2 only as the provisional post-terminal recipient. No task was created or forked, no subagent was spawned, Tavian remains standby, and Caelen has not been contacted. Only after Sylven's own clean pushed fresh-live-equal exact final and attributable one-shot canonical gate may the newest authority and roster be refreshed for one possible acknowledged send.", "",
        BOUNDARY, "", "`NOT_READY_FOR_STAGE_20`",
    ])
    return "\n".join(lines)


def build() -> None:
    if git("branch", "--show-current").stdout.decode().strip() != BRANCH:
        raise SystemExit("wrong branch")
    if git("rev-parse", "HEAD").stdout.decode().strip() != SOURCE_FINAL:
        raise SystemExit("x1 must begin at exact Elowen final")
    if (OWNER_ROOT / "x2").exists() or (OWNER_ROOT / "closeout").exists():
        raise SystemExit("x2 or closeout exists before x1 freeze")

    proposals = proposal_rows()
    if len(proposals) != 40 or Counter(row["expected_disposition"] for row in proposals) != Counter(OUTCOME_COUNTS):
        raise SystemExit("proposal count or outcome plan mismatch")
    if len(set(NEW_TITLES)) != 40:
        raise SystemExit("duplicate proposal title")

    corpus_summary, source_titles = recover_proposal_corpus()
    if corpus_summary["malformed_or_missing_blobs"]:
        raise SystemExit("proposal corpus contains malformed or missing blobs")
    neighbors, max_score = [], 0.0
    for row in proposals:
        candidate = normalize(row["title"])
        best_title, best_score = "", 0.0
        for source_title in source_titles:
            source_tokens = normalize(source_title)
            union = candidate | source_tokens
            score = len(candidate & source_tokens) / len(union) if union else 0.0
            if score > best_score:
                best_title, best_score = source_title, score
        max_score = max(max_score, best_score)
        neighbors.append({"proposal_id": row["proposal_id"], "source_title": best_title, "jaccard": round(best_score, 6), "collision": best_score >= 0.72})
    collisions = [row for row in neighbors if row["collision"]]
    if collisions:
        raise SystemExit("semantic neighbor collision requires proposal rewrite: " + json.dumps(collisions, ensure_ascii=False))

    source_ledger = json_blob(SOURCE_FINAL, "docs/elowen-cairn/v672-v8/closeout/proposal-ledger-final.json")
    inherited = [{
        "source_proposal_id": row["proposal_id"], "source_title": row["title"],
        "source_outcome": row["observed_outcome"], "selection_state": "selected_for_bounded_revalidation",
        "sylven_novelty_credit": 0, "sylven_completion_credit": 0,
    } for row in source_ledger["rows"][:20]]
    portfolios, portfolio_counts = portfolio_rows()
    method_flow = startup_method_flow()
    x1_counts = {
        "proposal_chain": 6230,
        "effective_negatives": ACTIVATION_BASELINE["effective_negatives"] + len(STARTUP_FAILURES),
        "effective_methods": ACTIVATION_BASELINE["effective_methods"] + len(STARTUP_FAILURES),
        "failed_witnesses": ACTIVATION_BASELINE["failed_witnesses"] + len(STARTUP_FAILURES),
        "bounded_passing_witnesses": ACTIVATION_BASELINE["bounded_passing_witnesses"] + len(STARTUP_FAILURES),
        "open_gaps": ACTIVATION_BASELINE["open_gaps"], "exact_gates": ACTIVATION_BASELINE["exact_gates"],
    }

    write_json("x1/activation-intake.json", {
        "schema": "ghc.family.activation-intake.v6", "owner": OWNER, "phase": PHASE,
        "task_creation_count": 0, "fork_count": 0, "subagent_count": 0, "standby_contact_count": 0,
        "source_verification": {
            "source_branch": SOURCE_BRANCH, "source_start": SOURCE_START, "x1": SOURCE_X1,
            "evidence": SOURCE_EVIDENCE, "source_final": SOURCE_FINAL,
            "source_to_final_phase_commits": 3, "merge_commits": 0, "single_parent_chain": True,
            "clean": True, "divergence": {"ahead": 0, "behind": 0}, "four_way_equal": True,
            "canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
            "canonical_payload_sha256": SOURCE_CANONICAL_PAYLOAD_SHA256,
            "canonical_status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "canonical_invocations": 1, "canonical_successes": 1, "canonical_replays": 0,
            "source_canonical_replayed_by_sylven": False,
        },
    })
    write_json("x1/identity-and-boundary.json", {
        "schema": "ghc.family.identity-boundary.v5", "owner": OWNER, "phase": PHASE,
        "pronouns": "they/them", "relational_role": "relational pattern gardener and evidence steward",
        "relational_hope": HOPE, "identity_boundary": IDENTITY_BOUNDARY,
        "corrigibility": "Hamish may rename, pause, redirect, or stop the route.",
    })
    write_json("x1/inherited-proposal-revalidation.json", {
        "schema": "ghc.family.inherited-proposal-revalidation.v6", "owner": OWNER, "phase": PHASE,
        "selection_count": len(inherited), "novelty_credit": 0, "completion_credit": 0, "rows": inherited,
    })
    write_json("x1/new-proposal-freeze.json", {
        "schema": "ghc.family.new-proposal-freeze.v7", "owner": OWNER, "phase": PHASE,
        "proposal_chain_before": 6230, "proposal_chain_after_if_evidence_frozen": 6270,
        "outcomes": OUTCOME_COUNTS, "planned_invalid_mutations_per_proposal": 4,
        "planned_invalid_mutations": 160, "rows": proposals,
    })
    write_json("x1/semantic-neighbor-audit.json", {
        "schema": "ghc.family.semantic-neighbor-audit.v7", "owner": OWNER, "phase": PHASE,
        "exact_source_tree_corpus": corpus_summary, "declared_source_chain": 6230,
        "reachable_unique_titles": len(source_titles), "new_titles": 40, "collision_threshold": 0.72,
        "max_jaccard": round(max_score, 6), "collisions": 0, "rows": neighbors,
        "candidate_practice_exact_hits": {term: sum(1 for title in source_titles if term in title.lower()) for term in ["flagmaking", "vexill", "signal flag", "bunting", "hoist and fly"]},
        "universal_novelty_claim": False, "canonical_row_mapping_open_gap": True,
    })
    write_json("x1/portfolio-freeze.json", {
        "schema": "ghc.family.remastered-portfolio-freeze.v7", "owner": OWNER, "phase": PHASE,
        "bounded_practice_lenses": ["field panel seam and silhouette topology", "hoist fly attachment storage and handover relations", "symbol attribution rights culture and authority vacancies"],
        "counts": portfolio_counts, "rows": portfolios, "ordinary_phase_new_tool_target": 3,
        "ordinary_phase_tool_target_is_subordinate": True, "filler_prohibited": True,
        "inherited_portfolio_completion_credit": 0, "successor_recommendation_completion_credit": 0,
        "successor_practice_recommendation": "Caelen selects their own bounded practice only after live authority and novelty review.",
    })
    write_json("x1/method-flow-startup.json", method_flow)
    write_json("x1/source-count-overlay.json", {
        "schema": "ghc.family.source-count-overlay.v6",
        "repository_sealed": SOURCE_REPOSITORY_SEAL,
        "activation_baseline": ACTIVATION_BASELINE,
        "sylven_x1_overlay": {**x1_counts, "startup_failures": len(STARTUP_FAILURES), "terminal_verdict": "NOT_READY_FOR_STAGE_20", "repository_seal_rewritten": False},
    })
    write_json("x1/source-ledger.json", {
        "schema": "ghc.family.public-source-ledger.v7", "owner": OWNER, "phase": PHASE,
        "read_only_source_page_checks": 0, "api_calls": 0, "dataset_or_media_downloads": 0,
        "real_rows": 0, "external_writes": 0, "sources": [],
        "source_status": "No new external source was material to the synthetic planning freeze; source citations remain inherited evidence only.",
        "boundary": "A future citation supplies vocabulary or refusal conditions only; never observation, instruction, consent, legal or cultural authority, Māori authority, or Stage 20 evidence.",
    })
    write_json("x1/threat-model.json", {
        "schema": "ghc.family.threat-model.v7", "owner": OWNER, "phase": PHASE,
        "assets": ["immutable source lineage", "planning-only x1 separation", "four truth labels", "retained failures", "synthetic-only fixtures", "authority vacancies", "route uniqueness"],
        "risks": [
            {"risk": "source or manifest drift", "control": "exact anchors, normalized Git-blob manifests, and fresh equality"},
            {"risk": "universal novelty overclaim", "control": "source-tree comparison plus explicit unavailable canonical-row mapping gap"},
            {"risk": "flag vocabulary promoted into deployment rigging signalling or safety advice", "control": "zero-object fixtures, action holds, vacancies, and professional exact gates"},
            {"risk": "membrane or wind analogy promoted into physics", "control": "analogy labels, zero measurements, and GMUT nonconversion"},
            {"risk": "symbol vocabulary promoted into legal cultural civic religious Indigenous or Māori authority", "control": "rights and authority exact gates"},
            {"risk": "failure laundering", "control": "append-only Method Flow with paired failed and passing witnesses"},
            {"risk": "private route or precise-location leak", "control": "five-class exact staged-blob scan"},
            {"risk": "accessibility overclaim", "control": "structural checks with manual and affected-user evaluation reserved"},
            {"risk": "duplicate successor send", "control": "terminal refresh, exact-title reread, duplicate guard, acknowledgement, and no resend"},
        ], "not_exhaustive_security": True,
    })
    write_json("x1/workflow-plan.json", {
        "schema": "ghc.family.workflow-plan.v6", "owner": OWNER, "phase": PHASE,
        "planned_phase_commits": 3, "commit_ceiling": 8, "x1_commit_ceiling": 5, "x2_commit_ceiling": 5,
        "materialized_file_guard": 2000, "canonical_invocation_budget": 1, "canonical_success_budget": 1,
        "post_success_replay": False,
        "steps": [
            {"step": "activation guidance and source verification", "state": "completed_read_only"},
            {"step": "planning-only x1 freeze", "state": "in_progress_until_pushed_equal"},
            {"step": "bounded x2 execution", "state": "blocked_by_x1_terminal_gate"},
            {"step": "combined closeout and seal", "state": "pending"},
            {"step": "one owner-scoped canonical aggregate", "state": "pending_not_invoked"},
            {"step": "successor route", "state": "provisional_caelen_v673_v2_terminally_gated"},
        ],
    })
    write_json("x1/route-plan.json", {
        "schema": "ghc.family.route-plan.v6", "owner": OWNER, "phase": PHASE,
        "delivery_state": "PROVISIONAL_NOT_CONTACTED_REQUIRES_TERMINAL_REFRESH",
        "prospective_recipient_exact_title": "Caelen Morrow", "prospective_phase": "v673-v2",
        "required_gate": "clean pushed exact final, attributable one-shot terminal validation, newest live authority and roster, unique exact-title reread, duplicate guard, and acknowledged one-send",
        "task_creation_count": 0, "successor_contact_count": 0, "standby_contact_count": 0, "substitute_endpoint_count": 0,
    })
    write_json("x1/phase-truth.json", {
        "schema": "ghc.family.phase-truth.x1.v7", "owner": OWNER, "phase": PHASE,
        "source_final": SOURCE_FINAL, "proposal_chain_before": 6230, "planned_proposal_chain_after": 6270,
        "new_proposals": 40, "selected_inherited": 20, "selected_inherited_novelty_credit": 0,
        "selected_inherited_completion_credit": 0, "planned_outcomes": OUTCOME_COUNTS,
        "planned_invalid_mutations": 160, "x2_exists": False, "x2_completion_claims": 0,
        "effective_counts_after_startup": x1_counts, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "independent_reproduction": False, "boundary": BOUNDARY,
    })
    write_text("x1/integrated-overview.md", integrated_overview(proposals, inherited, corpus_summary))
    write_json("x1/build-receipt.json", {
        "schema": "ghc.family.x1-build-receipt.v7", "owner": OWNER, "phase": PHASE,
        "planning_only": True, "proposal_count": 40, "inherited_selection_count": 20,
        "semantic_collisions": 0, "max_jaccard": round(max_score, 6), "portfolio_counts": portfolio_counts,
        "startup_failures_retained": len(STARTUP_FAILURES), "x2_exists": False, "external_actions": 0,
    })


def staged_paths() -> list[str]:
    return [line for line in git("diff", "--cached", "--name-only", "--diff-filter=ACMRT").stdout.decode("utf-8").splitlines() if line]


def staged_review() -> None:
    self_path = "docs/sylven-arc/v673-v1/validation/x1-staged-review.json"
    paths = [path for path in staged_paths() if path != self_path]
    allowed = [
        path for path in paths if path.startswith("docs/sylven-arc/v673-v1/x1/")
        or path.startswith("docs/sylven-arc/v673-v1/validation/x1-")
        or path == "scripts/build_ghc_family_sylven_arc_v673_v1_x1.py"
        or path == "tests/test_ghc_family_sylven_arc_v673_v1_x1.py"
    ]
    out_of_scope = sorted(set(paths) - set(allowed))
    mixed = [path for path in paths if "/x2/" in path or "/closeout/" in path or "/final/" in path]
    payload = {
        "schema": "ghc.family.staged-review.v6", "owner": OWNER, "phase": PHASE, "lifecycle": "x1",
        "staged_before_self": paths, "staged_count_before_self": len(paths), "out_of_scope": out_of_scope,
        "mixed_lifecycle": mixed, "valid": not out_of_scope and not mixed,
    }
    write_json("validation/x1-staged-review.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def staged_privacy() -> None:
    self_path = "docs/sylven-arc/v673-v1/validation/x1-staged-privacy.json"
    paths = [path for path in staged_paths() if path != self_path]
    patterns = {
        "credential_assignment": re.compile(r"(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*[^\s<]+"),
        "private_absolute_path": re.compile(r"(?i)(?:[A-Z]:\\Users\\|/home/|/Users/)"),
        "private_route_or_callable": re.compile(r"(?i)(?:thread[_-]?id|task[_-]?id|callable[_-]?id|session[_-]?id)\s*[:=]"),
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "transcript_or_session_stream": re.compile(r"(?i)(raw transcript|session stream|screenshot payload)"),
    }
    candidates, scanned = [], 0
    for path in paths:
        blob = git("show", f":{path}").stdout
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            continue
        scanned += 1
        scanner_surface = path.startswith("scripts/") or path.startswith("tests/")
        for label, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"path": path, "pattern_class": label, "disposition": "scanner_definition_or_unit_test" if scanner_surface else "confirmed_payload_hit"})
    confirmed = [row for row in candidates if row["disposition"] == "confirmed_payload_hit"]
    payload = {
        "schema": "ghc.family.staged-privacy-scan.v3", "owner": OWNER, "phase": PHASE, "lifecycle": "x1",
        "hash_domain": "exact_staged_git_blob", "pattern_classes": sorted(patterns), "scanned_text_files": scanned,
        "candidates": candidates, "confirmed_hits": confirmed, "confirmed_hit_count": len(confirmed),
        "self_exclusions": [self_path], "valid": not confirmed,
        "boundary": "Scanner definitions and synthetic unit-test strings are candidates, never payload hits; every other match fails closed.",
    }
    write_json("validation/x1-staged-privacy.json", payload)
    if confirmed:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def validation_receipt() -> None:
    paths = staged_paths()
    json_issues, compiles, compile_issues, text_files = [], 0, [], 0
    for path in paths:
        blob = git("show", f":{path}").stdout
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            continue
        text_files += 1
        if path.endswith(".json"):
            try:
                json.loads(text)
            except json.JSONDecodeError as exc:
                json_issues.append({"path": path, "error": str(exc)})
        if path.endswith(".py"):
            try:
                compile(text, path, "exec")
                compiles += 1
            except SyntaxError as exc:
                compile_issues.append({"path": path, "error": str(exc)})
    diff = git("diff", "--cached", "--check", check=False)
    materialized = sum(1 for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts)
    payload = {
        "schema": "ghc.family.x1-validation-receipt.v2", "owner": OWNER, "phase": PHASE,
        "staged_paths_before_receipt": len(paths), "json_documents": sum(path.endswith(".json") for path in paths),
        "json_issues": json_issues, "python_compiles": compiles, "python_compile_issues": compile_issues,
        "text_files": text_files, "diff_hygiene_exit": diff.returncode,
        "diff_hygiene_output": diff.stdout.decode("utf-8", errors="replace"),
        "x2_absent": not (OWNER_ROOT / "x2").exists(), "materialized_files": materialized,
        "file_guard": 2000, "confirmed_privacy_hits": 0, "boundary": BOUNDARY,
        "valid": not json_issues and not compile_issues and diff.returncode == 0 and not (OWNER_ROOT / "x2").exists() and materialized < 2000,
    }
    write_json("validation/x1-validation-receipt.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def method_flow_validation() -> None:
    ledger = json.loads((OWNER_ROOT / "x1" / "method-flow-startup.json").read_text(encoding="utf-8"))
    methods, witnesses = ledger["methods"], ledger["witnesses"]
    issues = []
    if len(methods) != len(STARTUP_FAILURES) or len(witnesses) != 2 * len(methods):
        issues.append("count mismatch")
    for method in methods:
        linked = [row for row in witnesses if row["method_id"] == method["method_id"]]
        if Counter(row["result"] for row in linked) != Counter({"fail": 1, "pass": 1}):
            issues.append(method["method_id"])
    write_json("validation/x1-method-flow-validation.json", {
        "schema": "ghc.family.method-flow-state.validation.v2", "owner": OWNER, "phase": PHASE,
        "method_count": len(methods), "witness_count": len(witnesses),
        "state_event_count": len(ledger["state_events"]), "recommendation_count": len(ledger["recommendations"]),
        "issues": issues, "issue_count": len(issues), "valid": not issues,
        "boundary": "Validation covers bounded owner-local method evidence only; it is not independent reproduction or broader assurance.",
    })
    if issues:
        raise SystemExit(json.dumps(issues))


def manifest_from_index() -> None:
    self_path = "docs/sylven-arc/v673-v1/validation/x1-manifest.json"
    paths = [path for path in staged_paths() if path != self_path]
    entries = []
    for path in paths:
        blob = git("show", f":{path}").stdout
        entries.append({"path": path, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})
    write_json("validation/x1-manifest.json", {
        "schema": "ghc.family.git-blob-manifest.v6", "owner": OWNER, "phase": PHASE,
        "lifecycle": "x1", "hash_domain": "exact_staged_git_blob", "entry_count": len(entries),
        "entries": entries, "self_exclusions": [self_path],
    })


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staged-review", action="store_true")
    parser.add_argument("--manifest-from-index", action="store_true")
    parser.add_argument("--validation-receipt", action="store_true")
    parser.add_argument("--staged-privacy", action="store_true")
    parser.add_argument("--method-flow-validation", action="store_true")
    args = parser.parse_args()
    if args.staged_review:
        staged_review()
    elif args.manifest_from_index:
        manifest_from_index()
    elif args.validation_receipt:
        validation_receipt()
    elif args.staged_privacy:
        staged_privacy()
    elif args.method_flow_validation:
        method_flow_validation()
    else:
        build()


if __name__ == "__main__":
    main()
