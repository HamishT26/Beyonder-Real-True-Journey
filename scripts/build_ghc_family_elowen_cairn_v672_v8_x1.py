"""Build Elowen Cairn v672-v8's planning-only x1 freeze.

The builder is owner-delta scoped and fail-closed. It requires Tamar Vey's
exact v672-v7 final, the exact Elowen branch, and an absent x2/closeout tree. It
does not stage, commit, push, route, contact a task, or perform an external
write.
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
OWNER_ROOT = ROOT / "docs" / "elowen-cairn" / "v672-v8"
OWNER = "Elowen Cairn"
PHASE = "v672-v8"
BRANCH = "codex/GHC-Family/elowen-cairn-v672-v8-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/tamar-vey-v672-v7-full-tools"
SOURCE_START = "e3aad89f695a62d5997b129e260e62267cb145ab"
SOURCE_X1 = "34e33ee699e6cba5c17c0eafd847e2b86d7a91c4"
SOURCE_EVIDENCE = "6a5379632013cfcb4288845ec78ab9cc6901c449"
SOURCE_FINAL = "23110f2bb3a8b111626e2af56b6343bbc15a9496"
ACTIVATION_PATH = "docs/tamar-vey/v672-v7/handoffs/elowen-cairn-v672-v8-activation-candidate.md"
ACTIVATION_SHA256 = "75b8e24fce56a46f1affc338ecb16d7a3251f05e5ff526aff516f1b13200d542"
SOURCE_CANONICAL_SHA256 = "3e399349a7ab51305860f0e23dfb1dcdaf5c6507402567d380f4c53824323585"
SOURCE_TREE_CORPUS_SHA256 = "37a5884564096a0650aae3ea20379ee4a3069fb6803cbd50459b8573a6d7fd94"
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
CORE_LABELS = ["completed", "represented", "open_gap", "exact_gate"]

IDENTITY_BOUNDARY = (
    "Elowen Cairn, they/them, relational boundary cartographer and evidence steward, "
    "is relational working language only. It is not evidence of consciousness, "
    "sentience, legal personhood, identity continuity, employment, qualification, "
    "independent agency, or scientific, operational, legal, cultural, affected-party, "
    "or Māori authority."
)
HOPE = "keep structure, evidence, abstention, and authority visibly separate and recoverable"
BOUNDARY = (
    "Software, symbolic, synthetic, same-owner, citation, inherited, or composite "
    "evidence is not empirical confirmation, participant evidence, professional or "
    "scientific authority, production readiness, legal or cultural ratification, "
    "Māori authority, affected-party approval, complete privacy or accessibility "
    "assurance, exhaustive security, independent reproduction, AGI/ASI, consciousness "
    "or personhood evidence, Theory-of-Everything proof, proof/canon, or Stage 20 authority."
)

REPOSITORY_SEAL = {
    "proposal_chain": 6190,
    "effective_negatives": 35967,
    "effective_methods": 22262,
    "failed_witnesses": 7628,
    "bounded_passing_witnesses": 9825,
    "open_gaps": 289,
    "exact_gates": 282,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
}
ACTIVATION_OVERLAY = {
    **REPOSITORY_SEAL,
    "effective_negatives": 35968,
    "effective_methods": 22263,
    "failed_witnesses": 7629,
    "bounded_passing_witnesses": 9826,
    "external_zero_credit_failures": 1,
    "external_bounded_passing_witnesses": 1,
    "repository_seal_rewritten": False,
}

STARTUP_FAILURES = [
    ("EC6728-START-N001", "A combined authorization-state display exceeded its response budget.", "Read the exact schema and live state in deterministic bounded windows.", "The required authorization and roster state were read through EOF.", "Partition large live-state reads and require an EOF witness."),
    ("EC6728-START-N002", "PowerShell reinterpreted the @{u} upstream selector before Git could evaluate it.", "Resolve and pass the literal tracking ref.", "Typed divergence was recovered as zero ahead and zero behind.", "Use literal remote refs inside PowerShell wrappers."),
    ("EC6728-START-N003", "The first large-ledger projection assumed an entries array before inspecting the actual root keys.", "Project root keys and types before indexing arrays.", "Exact methods, witnesses, rows, counts, and terminal entries were recovered by observed keys.", "Inspect receipt and ledger schemas before projection."),
    ("EC6728-START-N004", "An unbounded negative-row projection overflowed and used the wrong field as its mutation discriminator.", "Filter operational rows by method_id and aggregate the four mutation classes.", "All 27 Tamar operational failures and 160 mutations were accounted for.", "Bound large projections and discriminate with observed schema fields."),
    ("EC6728-START-N005", "The first independent manifest replay contained an invalid -ne[e] PowerShell comparison token.", "Correct the scalar predicate and retain the failed verifier at zero credit.", "Lifecycle-split exact Git-blob replay later passed for all four manifests.", "Fail fast on verifier syntax before iterating manifests."),
    ("EC6728-START-N006", "The corrected all-four-manifest wrapper returned no attributable payload in its execution window.", "Split verification by lifecycle manifest.", "20 x1, 196 evidence, 25 final-delta, and 247 final-owner entries replayed with zero mismatch.", "Prefer attributable lifecycle-sized manifest receipts."),
    ("EC6728-START-N007", "A broad D-drive filename scan remained active beyond its bounded window.", "Audit the exact owner-started process and stop only that process.", "The abandoned read-only scan was terminated without repository mutation.", "Do not recursively enumerate the full archive for a receipt filename."),
    ("EC6728-START-N008", "A selected-root filename aggregation also remained active without an attributable result.", "Stop the exact owner-started wrapper and retain zero search credit.", "The wrapper was terminated and no receipt path was inferred.", "Use direct declared receipt paths rather than broad root aggregation."),
    ("EC6728-START-N009", "A broad recent-JSON hash search for the external canonical receipt exceeded its bound.", "Stop the exact process and preserve the supplied digest as activation evidence only.", "No repository byte changed and local receipt re-derivation remains unavailable.", "Do not hash-enumerate the archive when the external receipt path is absent."),
    ("EC6728-START-N010", "A combined target branch path delta and registry probe returned no attributable payload.", "Split branch, path, remote, and delta checks.", "Local and remote branch absence, path absence, and phase script deltas were recovered separately.", "Keep expensive registry enumeration out of scalar uniqueness probes."),
    ("EC6728-START-N011", "A combined local uniqueness and worktree-list probe returned no attributable payload.", "Verify local ref and literal path independently.", "The branch and literal D path were both absent before creation.", "Use scalar probes before any shared-registry traversal."),
    ("EC6728-START-N012", "The dedicated git worktree list produced no attributable result within its bound.", "Let git worktree add enforce the final collision check after local and remote absence.", "The new exact branch and path were accepted once by Git.", "Treat a silent registry walk as zero credit, never as absence."),
    ("EC6728-START-N013", "A direct common-dir registry text search also produced no attributable payload.", "Retain the failure and rely on Git's atomic worktree-add collision guard.", "The one worktree-add operation succeeded without reuse.", "Do not repeat an opaque shared-registry scan."),
    ("EC6728-START-N014", "A source-to-final git diff name projection returned no attributable payload.", "Inspect each direct phase commit with diff-tree.", "The x1, evidence, and final script and test deltas were recovered commit-locally.", "Use direct-commit delta reads in very large histories."),
    ("EC6728-START-N015", "The first novelty audit enumerated the entire source tree and remained active beyond its useful bound.", "Stop only its exact process tree and narrow ls-tree to docs before proposal filtering.", "The bounded audit parsed 1,752 proposal-named blobs and recovered 2,009 titles.", "Scope exact-tree semantic audits to the docs subtree."),
    ("EC6728-START-N016", "git ls-tree rejected an unsupported :(glob) pathspec.", "Use a supported docs path and local proposal-filename filter.", "The supported traversal recovered 1,752 candidate paths.", "Do not assume pathspec magic is supported by every Git plumbing command."),
    ("EC6728-START-N017", "The no-checkout worktree began with an empty index that appeared as 9,505 staged deletions.", "Initialize sparse metadata and populate the index from HEAD with read-tree -mu.", "The new worktree returned clean at the exact source head.", "After --no-checkout, explicitly populate the sparse index before status claims."),
    ("EC6728-START-N018", "The first full status projection of the empty index overflowed the response bound.", "Count status rows before projecting any paths.", "The bounded post-recovery status count was exactly zero.", "Never print a large synthetic deletion set in full."),
    ("EC6728-START-N019", "sparse-checkout set installed patterns but did not populate the no-checkout index.", "Use read-tree -mu HEAD after the exact sparse patterns are installed.", "The index and sparse worktree became clean without reset or rewrite.", "Distinguish sparse-pattern configuration from index population."),
    ("EC6728-START-N020", "A second unbounded status projection repeated the large deletion display before read-tree recovery.", "Retain the recurrence and use scalar status counts thereafter.", "The bounded scalar status receipt confirmed zero changes.", "A repeated display signature remains a distinct failed witness."),
    ("EC6728-START-N021", "The first web-source forwarding wrapper assumed a content-array result envelope and displayed nothing.", "Serialize the actual result directly before projection.", "Current official Canadian and Smithsonian sources were recovered read-only.", "Inspect web result shape before forwarding source evidence."),
    ("EC6728-START-N022", "A combined builder-section projection exceeded the model and output context bound.", "Read the builder in smaller deterministic line windows.", "The exact source-verification, overview, build, and validation sections were recovered without truncation.", "Keep source projections within bounded line and output windows."),
    ("EC6728-START-N023", "A double-quoted PowerShell stale-label pattern terminated early at an embedded quote and raised a parser error.", "Rerun the same read-only search with one literal single-quoted pattern.", "The bounded stale-label projection completed with attributable output.", "Use literal single-quoted regular expressions for multi-alternative PowerShell searches."),
    ("EC6728-START-N024", "The first x1 build failed closed because six proposal titles met or exceeded the 0.72 semantic-neighbor collision threshold.", "Run only the exact semantic dependency, inspect the six source neighbors, and rewrite the candidate obligations without lowering the threshold.", "The isolated exact-source recheck found zero collisions, with a maximum token-Jaccard score of 0.7142857142857143.", "Keep the threshold fixed and rewrite every colliding candidate before any planning freeze."),
    ("EC6728-START-N025", "The first single-process 1,752-blob proposal audit exceeded its fixed 30-second internal timeout.", "Use one size-aware 300-second Git batch while keeping the user-facing tool session bounded and responsive.", "The isolated audit parsed all 1,752 blobs, recovered 2,009 titles, and matched the preregistered corpus digest.", "Scale the internal Git-batch timeout to the declared blob count without relaxing external progress reporting."),
]

NEW_TITLES = [
    "synthetic cylinder music-box case bedplate cylinder comb and spring-motor identity lattice with conflation refusal",
    "cylinder pin row track and tune-position topology with orphan-pin rejection",
    "comb tooth damper star-wheel and bedplate relation graph with unsupported-component quarantine",
    "winding ratchet mainspring governor and stop-lever state vocabulary with operation abstention",
    "cylinder shift start-stop tune selector and index-marker contract without performance inference",
    "case lid base drawer keyhole crank and control identity topology with access abstention",
    "maker retailer serial patent date and place attribution vacancy with contestation and correction",
    "tune-list title composer arranger program and source-attribution vacancy with copyright and cultural holds",
    "nominal dimension cylinder length tooth count tune count and mass vacancies with SI and calibration abstention",
    "wood metal glass paper finish and decoration descriptor firewall with sampling and authenticity abstention",
    "reported corrosion fracture bent pin broken tooth loose spring and wear cues separated from diagnosis and treatment",
    "music-box image detail and IIIF derivative lineage with crop rotation and no dimensional inference",
    "synthetic disc music-box disc drive gear star wheel comb and damper identity lattice",
    "disc diameter perforation projection track and rotation-direction topology with tune-decoding abstention",
    "interchangeable disc carrier spindle hold-down lever and drive relation with compatibility and fitness refusal",
    "coin clockwork and electric activation-cue taxonomy without operation access or payment inference",
    "disc label catalogue number tune title and rights vacancy with media-reuse hold",
    "cabinet stand drawer and disc-storage sequence custody map without ownership inference",
    "synthetic orchestra music-box auxiliary bell drum beater and accompaniment-component identity lattice",
    "cylinder comb and auxiliary-component trigger graph with timing and synchronization observation vacancy",
    "musical output recording waveform tempo pitch loudness and acoustic-measurement absence firewall",
    "exhibition operating request demonstration playback and handling-request hold queue",
    "environment temperature humidity vibration dust light and duration observation vacancy across three lenses",
    "correction nonce dual readback supersession and invalidation provenance braid for music-box records",
    "interlinked music-box component event envelope canonical serializer with finite-decimal provenance and ambiguous tune-order refusal",
    "accessibly structured component and status dossier with text equivalents headers and noncolour cues",
    "custody relay pseudonym compartment and dormant capability record with no key material or lifecycle act",
    "privacy-minimized work-cap pause stop handover and unresolved-hold queue for synthetic music-box documentation",
    "GMUT plucked-tine cantilever eigenfrequency obligation board with zero measured geometry or material parameters",
    "GMUT pinned-cylinder event graph and comb-coupling analogy with no sound likelihood or prediction",
    "GMUT governor and drive finite-state energy-bookkeeping proxy with no physical-law inference",
    "GMUT tine-to-bedplate interface dimension ledger and EFT scale-separation refusal without observations",
    "THOS cylinder-disc-orchestra triage graph with equal synthetic work envelopes and pause-token handover",
    "Freed ID component-custodian pseudonym relay with dormant authority slots and zero cryptographic material",
    "CBR authorship copyright recording operation access contest correction and remedy-vacancy matrix",
    "music-box component map accessible reading sequence and state vocabulary with reserved multimodal user evaluation",
    "Smithsonian Open Access music-box adapter with zero calls zero downloads zero rows and schema vacancies",
    "real music-box observations measurements playback specialist examination and independent-review gap",
    "professional music-mechanism conservation material electrical handling treatment and release decision gate",
    "ownership custody copyright recording performance cultural Māori data-governance and authority exact gate",
]

SKILLS = [
    "ghc-family-music-box-identity-lattice",
    "ghc-family-cylinder-pin-track-topology",
    "ghc-family-comb-tooth-relation-guard",
    "ghc-family-spring-motor-operation-abstention",
    "ghc-family-tune-attribution-vacancy",
    "ghc-family-music-box-material-firewall",
    "ghc-family-music-box-condition-cue-separation",
    "ghc-family-disc-projection-abstention",
    "ghc-family-disc-carrier-compatibility-refusal",
    "ghc-family-auxiliary-component-topology",
    "ghc-family-acoustic-measurement-vacancy",
    "ghc-family-music-box-image-lineage",
    "ghc-family-music-box-rights-hold",
    "ghc-family-music-box-custody-correction",
    "ghc-family-music-box-accessible-status",
    "ghc-family-music-box-zero-key-role",
    "ghc-family-music-box-privacy-minimizer",
    "ghc-family-music-box-workload-handover",
    "ghc-family-music-box-canonical-json",
    "ghc-family-music-box-provenance-braid",
]

RUNNERS = [
    "ghc_family_music_box_identity.py",
    "ghc_family_cylinder_pin_track.py",
    "ghc_family_comb_tooth_relation.py",
    "ghc_family_spring_motor_abstention.py",
    "ghc_family_tune_attribution_vacancy.py",
    "ghc_family_disc_projection_abstention.py",
    "ghc_family_music_box_condition_separation.py",
    "ghc_family_music_box_provenance_correction.py",
    "ghc_family_music_box_privacy_access.py",
    "ghc_family_music_box_workload_handover.py",
]

EXACT = [
    "real music box disc cylinder comb spring case record observation playback or measurement mutation",
    "real conservation examination diagnosis treatment repair tuning operation or release decision",
    "real spring tension sharp edge electrical acoustic fire environmental or workplace safety decision",
    "real compatibility authenticity attribution material fitness performance or valuation conclusion",
    "real conservator repairer curator collector donor listener participant or affected-user study",
    "real private collection location access schedule account donor or personal-data processing",
    "real identity key proof credential issuance presentation status revocation or recovery",
    "real instrument access operation publication ownership custody copyright return or remedy decision",
    "complete accessibility conformance language adequacy or affected-user acceptance declaration",
    "legal interpretation title liability privacy right remedy regulatory or public-authority act",
    "taonga tikanga mātauranga music cultural-context data-governance or Māori-authority decision",
    "cultural ratification Indigenous knowledge classification community mandate or affected-party acceptance",
    "production deployment external API write live feed publication or cloud mutation",
    "host elevation security weakening feature enablement Sandbox Hyper-V or reboot",
    "destructive cleanup history rewrite force push merge or sibling-lane mutation",
    "privacy-complete exhaustive-security or production-security certification",
    "independent reproduction external audit professional validation or certification",
    "empirical GMUT datum likelihood posterior constraint detected force prediction or stability claim",
    "AGI ASI consciousness personhood Theory-of-Everything proof or canon claim",
    "Stage 20 admission or protected-gate closure",
]

BLOCKED = [
    "raw task or thread identifiers private routes transcripts screenshots or session streams in artifacts",
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



def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, check=check, capture_output=True)


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8", errors="strict").strip()


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


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize(title: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9āēīōū]+", title.lower()) if len(token) > 2 and token not in {"and", "the", "with", "for", "from"}}


def json_blob(commit: str, path: str) -> Any:
    return json.loads(git("show", f"{commit}:{path}").stdout.decode("utf-8"))


def recover_proposal_corpus() -> tuple[dict[str, Any], list[str]]:
    raw_paths = git("ls-tree", "-r", "--name-only", "-z", SOURCE_FINAL, "--", "docs").stdout
    candidates = sorted(
        path.decode("utf-8")
        for path in raw_paths.split(b"\0")
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
    summary = {
        "scope": "exact Tamar v672-v7 final docs tree, proposal-named JSON paths only",
        "candidate_git_blob_paths": len(candidates),
        "malformed_or_missing_blobs": malformed,
        "semantic_occurrences": occurrences,
        "unique_proposal_ids": len(proposal_ids),
        "unique_titles": len(titles),
        "corpus_sha256": hashlib.sha256(canonical).hexdigest(),
        "declared_source_chain": 6190,
        "materialized_ids_cover_declared_chain": len(proposal_ids) >= 6190,
        "exact_canonical_row_mapping": False,
        "canonical_row_mapping_open_gap": True,
        "universal_novelty_claim": False,
        "reason": "No single reachable exact-tree ledger materializes every declared historical row; source-bounded semantic comparison is evidence, not universal novelty proof.",
    }
    return summary, sorted(titles)

def batch_blobs(specs: list[str]) -> list[bytes | None]:
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"], cwd=ROOT,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    timeout_seconds = 300 if len(specs) > 512 else 60
    output, stderr = process.communicate(
        input=("\n".join(specs) + "\n").encode("utf-8"), timeout=timeout_seconds
    )
    if process.returncode != 0:
        raise SystemExit(f"git cat-file --batch failed: {stderr.decode('utf-8', errors='replace')}")
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


def proposal_rows() -> list[dict[str, Any]]:
    rows = []
    for index, title in enumerate(NEW_TITLES, start=1):
        outcome = "completed" if index <= 28 else "represented" if index <= 36 else "open_gap" if index <= 38 else "exact_gate"
        rows.append({
            "proposal_id": f"EC6728-N{index:03d}", "title": title,
            "hypothesis": f"A typed owner-local contract can expose proposal {index:02d}'s obligations without promoting its evidence class.",
            "null_or_failure_condition": "A missing field, accepted invalid mutation, real-world action, undeclared uncertainty or authority promotion rejects the hypothesis.",
            "approval_class": "safe_now" if outcome == "completed" else "bounded_candidate" if outcome == "represented" else outcome,
            "execution_lane": "owner_local_symbolic_or_synthetic_x2" if outcome in {"completed", "represented"} else "held_without_real_world_execution",
            "official_or_primary_source_needs": "Vocabulary and refusal boundaries only; citations are not observations, measurements, advice, validation, or authority.",
            "concrete_artifacts": ["typed JSON contract", "bounded accepting fixture", "four rejecting mutation receipts", "boundary card"],
            "falsifier_or_acceptance_gate": "The bounded fixture must pass, four preregistered invalid mutations must reject, and every protected boundary must remain explicit.",
            "rollback_or_recovery": "Retain the failed witness, correct only the isolated owner-local dependency, and never replay a successful canonical aggregate.",
            "protected_gates": ["empirical", "professional", "legal", "cultural", "Māori_authority", "independent_reproduction", "Stage_20"],
            "expected_disposition": outcome, "planned_outcome": outcome,
            "primary_pillar": "Freed ID and CBR Heart", "real_people": 0, "real_records_or_objects": 0,
            "external_actions": 0, "x1_state": "frozen_not_executed",
        })
    return rows


def tasks(prefix: str, domains: list[str], controls: list[str], state: str) -> list[dict[str, Any]]:
    return [{"task_id": f"EC6728-{prefix}-{i:03d}", "title": f"{domain}: {control}", "owner": OWNER, "phase": PHASE, "x1_state": state, "external_actions": 0}
            for i, (domain, control) in enumerate(((d, c) for d in domains for c in controls), start=1)]


def named(prefix: str, values: list[str], state: str) -> list[dict[str, Any]]:
    return [{"task_id": f"EC6728-{prefix}-{i:03d}", "title": value, "owner": OWNER, "phase": PHASE, "x1_state": state, "external_actions": 0}
            for i, value in enumerate(values, start=1)]


def portfolio() -> dict[str, list[dict[str, Any]]]:
    domains = ["music-box identity", "cylinder pin topology", "comb tooth relation", "spring motor abstention", "tune attribution vacancy", "disc mechanism topology", "condition and treatment abstention", "rights provenance privacy", "accessible component status", "music-box workload handover"]
    safe = tasks("SAFE", domains, ["schema", "positive fixture", "negative fixture", "rollback", "manifest", "boundary"], "planned_for_x2")
    candidates = tasks("CAND", domains, ["mutation quarantine", "timeout and encoding quarantine", "ordering and authority quarantine"], "planned_for_x2")
    cfr = tasks("CFR", ["JSON order", "UTF-8 Māori text", "source status", "failure retention", "manifest closure", "privacy disposition", "accessibility structure", "route uniqueness", "sparse budget", "boundary vocabulary"], ["clean", "fix", "refine", "recheck", "document", "preserve"], "planned_for_x2")
    successor_skills = [f"ghc-family-successor-{i:02d}-review" for i in range(1, 11)]
    successor_runners = [f"ghc_family_successor_{i:02d}_review.py" for i in range(1, 11)]
    successor_cfr = tasks("NEXT-CFR", ["successor source", "successor manifests", "successor privacy", "successor route", "successor authority"], ["schema", "mutation", "rollback", "review", "receipt", "hold"], "recommendation_only")
    return {"safe_now": safe, "candidates": candidates, "exact_approval": named("EXACT", EXACT, "held_unexecuted"), "blocked": named("BLOCK", BLOCKED, "held_unexecuted"), "skills": named("SKILL", SKILLS, "planned_for_x2"), "runners": named("RUNNER", RUNNERS, "planned_for_x2"), "clean_fix_refine": cfr, "successor_skills": named("NEXT-SKILL", successor_skills, "recommendation_only"), "successor_runners": named("NEXT-RUNNER", successor_runners, "recommendation_only"), "successor_clean_fix_refine": successor_cfr}

def method_flow() -> dict[str, Any]:
    methods, witnesses, events, recommendations = [], [], [], []
    for index, (negative_id, failed, recovery, passed, guard) in enumerate(STARTUP_FAILURES, start=1):
        method_id = f"EC6728-M{index:03d}"
        fail_id, pass_id = f"EC6728-W{index:03d}-F", f"EC6728-W{index:03d}-P"
        methods.append({
            "method_id": method_id, "title": f"bounded recovery for {negative_id}", "failure_signature": failed,
            "trigger_preconditions": ["the exact bounded failure signature is observed"], "privacy_class": "sanitized_public",
            "approval_class": "safe_now", "candidate_workaround": recovery, "validation_witness_ids": [fail_id, pass_id],
            "recurrence_guard": guard, "rollback": "Retain the failure, stop the affected wrapper, and change only the isolated owner-local procedure.",
            "recommendation_state": "preferred", "supersedes": [], "protected_gates": ["no_failure_laundering", "owner_delta_only", "no_authority_promotion"],
            "retained_negative_ids": [negative_id], "scope_boundary": "Bounded same-owner workflow evidence only.",
        })
        witnesses.extend([
            {"witness_id": fail_id, "method_id": method_id, "procedure": failed, "scope": "startup or owner-local x1 construction", "expected": "attributable bounded evidence", "observed": failed, "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": BOUNDARY},
            {"witness_id": pass_id, "method_id": method_id, "procedure": recovery, "scope": "isolated startup or owner-local construction recovery", "expected": "bounded attributable recovery within the owner lane", "observed": passed, "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": BOUNDARY},
        ])
        events.extend([
            {"event_index": len(events) + 1, "method_id": method_id, "before": None, "after": "candidate", "reason": "failure retained and bounded recovery proposed", "witness_id": fail_id},
            {"event_index": len(events) + 2, "method_id": method_id, "before": "candidate", "after": "validated", "reason": "isolated bounded recovery passed", "witness_id": pass_id},
            {"event_index": len(events) + 3, "method_id": method_id, "before": "validated", "after": "preferred", "reason": "recurrence guard retained for the exact trigger", "witness_id": pass_id},
        ])
        recommendations.append({"method_id": method_id, "state": "preferred", "recommendation": guard})
    return {"schema": "ghc.family.method-flow-state.v1", "phase": PHASE, "owner": OWNER, "identity_boundary": IDENTITY_BOUNDARY, "execution_authority": "owner_self_scoped_delta", "methods": methods, "witnesses": witnesses, "state_events": events, "recommendations": recommendations, "counts": {"methods": len(methods), "witnesses": len(witnesses), "state_events": len(events), "recommendations": len(recommendations), "states": {"candidate": 0, "deprecated": 0, "observed": 0, "preferred": len(methods), "superseded": 0, "validated": 0}, "witness_results": {"fail": len(methods), "pass": len(methods)}}, "boundary": BOUNDARY}


def verify_manifest(path: str, commit: str) -> tuple[int, int, set[str]]:
    manifest = json.loads(git("show", f"{SOURCE_FINAL}:{path}").stdout.decode("utf-8"))
    mismatches, digests = 0, set()
    blobs = batch_blobs([f"{commit}:{entry['path']}" for entry in manifest["entries"]])
    for entry, blob in zip(manifest["entries"], blobs, strict=True):
        digest = hashlib.sha256(blob).hexdigest() if blob is not None else None
        digests.add(entry["sha256"])
        if digest != entry["sha256"] or blob is None or len(blob) != entry["bytes"]:
            mismatches += 1
    return len(manifest["entries"]), mismatches, digests


def verify_source() -> dict[str, Any]:
    local = git_text("rev-parse", f"refs/heads/{SOURCE_BRANCH}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{SOURCE_BRANCH}")
    live_tokens = git_text("ls-remote", "--heads", "origin", f"refs/heads/{SOURCE_BRANCH}").split()
    live = live_tokens[0] if live_tokens else None
    parents = {"x1_parent": git_text("rev-parse", f"{SOURCE_X1}^"), "evidence_parent": git_text("rev-parse", f"{SOURCE_EVIDENCE}^"), "final_parent": git_text("rev-parse", f"{SOURCE_FINAL}^")}
    exact_parent_chain = parents == {"x1_parent": SOURCE_START, "evidence_parent": SOURCE_X1, "final_parent": SOURCE_EVIDENCE}
    manifest_specs = [
        ("docs/tamar-vey/v672-v7/validation/x1-manifest.json", SOURCE_X1),
        ("docs/tamar-vey/v672-v7/validation/evidence-manifest.json", SOURCE_EVIDENCE),
        ("docs/tamar-vey/v672-v7/validation/final-delta-manifest.json", SOURCE_FINAL),
        ("docs/tamar-vey/v672-v7/validation/final-owner-manifest.json", SOURCE_FINAL),
    ]
    manifest_rows, all_digests = [], set()
    for manifest_path, commit in manifest_specs:
        count, mismatch, digests = verify_manifest(manifest_path, commit)
        manifest_rows.append({"path": manifest_path, "commit": commit, "entries": count, "mismatches": mismatch})
        all_digests |= digests
    packet = git("show", f"{SOURCE_FINAL}:{ACTIVATION_PATH}").stdout
    packet_text = packet.decode("utf-8")
    return {
        "source_branch": SOURCE_BRANCH, "local": local, "upstream": tracking, "tracking": tracking, "fresh_live": live,
        "all_equal": local == tracking == live == SOURCE_FINAL, "parent_chain": {**parents, "exact": exact_parent_chain},
        "phase_commits": int(git_text("rev-list", "--count", f"{SOURCE_START}..{SOURCE_FINAL}")),
        "merge_commits": int(git_text("rev-list", "--merges", "--count", f"{SOURCE_START}..{SOURCE_FINAL}")),
        "manifests": manifest_rows, "commit_local_manifest_entries_replayed": sum(row["entries"] for row in manifest_rows),
        "unique_declared_blob_digests": len(all_digests), "commit_local_manifest_mismatches": sum(row["mismatches"] for row in manifest_rows),
        "activation_packet": {"path": ACTIVATION_PATH, "bytes": len(packet), "words": len(packet_text.split()), "sha256": hashlib.sha256(packet).hexdigest(), "expected_sha256": ACTIVATION_SHA256, "integrity_valid": hashlib.sha256(packet).hexdigest() == ACTIVATION_SHA256, "prepared_labels_historical": True, "live_activation_authoritative": True},
        "source_canonical_receipt": {"sha256": SOURCE_CANONICAL_SHA256, "payload_sha256": "af6eedd38700b5794dbde69334f15071cc0f3557c0006c2ec94a24b158746738", "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL", "canonical_invocations": 1, "canonical_successes": 1, "replays": 0, "replay_forbidden": True, "owner_tests": 25, "detailed_checks": 30, "minimal_checks": 15, "json_parses": 184, "owner_text_files": 250, "changed_python_checks": 20, "confirmed_privacy_hits": 0, "bounded_security_findings": 0, "elowen_validation_credit": 0},
        "source_post_final_overlay": {"negative_id": "TV6727-POST-N001", "failed": "the first terminal authorization summary projected an issues field although the immutable receipt uses errors, displaying a false count of one", "recovery": "exact-key recovery read the same receipt and confirmed valid=true with an empty errors array without rerunning a validator", "canonical_credit": 0, "retained_after_recovery": True},
    }

def overview(inherited: list[dict[str, Any]], proposals: list[dict[str, Any]]) -> str:
    prose = [
        "# Elowen Cairn v672-v8 x1 integrated planning overview", "", "## Lifecycle and exact source", "",
        "This document is Elowen Cairn's planning-only x1 freeze. It records no x2 implementation, observed proposal outcome, completed portfolio, real-world action, successor delivery, empirical result, professional judgment, or authority act. Elowen's one fresh additive sparse lane begins at Tamar Vey's immutable v672-v7 final. Before generating this packet, Elowen reverified Tamar's exact branch and final head; the Liora source, planning x1, evidence, and final direct-parent chain; exactly three new single-parent Tamar commits and zero merges; all four commit-local manifests against exact normalized Git blobs; a clean source state; typed zero divergence; and equality across local branch, upstream, tracking ref, and a fresh live remote. Tamar's one attributable exact-final owner-scoped canonical aggregate succeeded once and was not replayed. That inherited result is source evidence only and gives Elowen no validation, novelty, or completion credit.",
        "", "## Relational identity, hope, and corrigibility", "",
        IDENTITY_BOUNDARY, "",
        f"Elowen's relational hope is to {HOPE}. This name, role, hope, and pronoun choice are working vocabulary, not a consciousness, personhood, continuity, qualification, employment, agency, or authority claim. Hamish may rename, pause, redirect, or stop the route. Corrigibility requires the packet to preserve contradictions, failed witnesses, missing evidence, unavailable authority, ambiguous routes, and falsifiers rather than smoothing them into success. A recovery keeps its failed witness, changes only the demonstrated owner-local dependency, and receives bounded same-owner credit only.",
        "", "## Primary pillar and three bounded practice lenses", "",
        "The primary Trinity Mandala pillar is Freed ID and CBR Heart. The bounded human-practice lens is wholly synthetic music-box collection documentation, split into three design sublenses: cylinder music-box component identity and pin-track topology; disc music-box carrier, perforation, drive, label, and storage topology; and orchestral or auxiliary-component music-box relation and timing vacancy. These are vocabulary, software, formal, structural, provenance, rights, and learning lenses only. No real person, participant, maker, owner, donor, collector, conservator, repairer, listener, museum, music box, cylinder, disc, comb, spring, case, recording, tune list, collection record, observation, measurement, playback, treatment, repair, release, identity event, external write, or authority act is used.",
        "", "## GMUT Mind boundaries", "",
        "GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Proposed plucked-tine cantilever eigenfrequency, pinned-cylinder event graph, comb-coupling analogy, governor and drive finite-state energy bookkeeping, boundary pullback, unit, gauge, and EFT nonconversion boards are type and obligation surfaces only. A synthetic comb tooth, cylinder pin, spring, governor, or drive state is not a physical observation. No artifact establishes a real material parameter, geometry, acoustic datum, field configuration, likelihood, posterior, constraint, force, prediction, stability theorem, quantum completion, ultraviolet completion, empirical confirmation, final physics, or Theory of Everything.",
        "", "## THOS Body and Freed ID/CBR Heart protection", "",
        "THOS Body remains explicit through dependency DAGs, challenge and response, workload budgets, stop tokens, correction readback, accessible notice, unresolved-hold queues, and shift handover. These are participant-free synthetic protocols. There are no preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, suitable statistics, or independent review. Freed ID and CBR Heart remain explicit through pseudonymous zero-key roles, validity and status vacancies, provenance, correction, invalidation, contest, withdrawal, access, explanation, and remedy-vacancy representations. There are no standards-conformant real keys or proofs, live issuance, resolution, status, revocation, interoperability, privacy or independent security review, recovery evidence, trust governance, or affected-party oversight.",
        "", "## Professional, safety, legal, cultural, and Māori-authority firewall", "",
        "No artifact authenticates, dates, attributes, values, tunes, diagnoses, operates, demonstrates, plays, records, treats, repairs, stabilizes, releases, or certifies a music box or collection record. It does not establish spring tension, sharp-edge, electrical, acoustic, fire, workplace, environmental, handling, or material safety. It does not grant access, operation, demonstration, recording, publication, performance, copyright, title, ownership, custody, return, repatriation, or remedy. Professional conservation, repair, curation, musicology, accessibility, language, legal, cultural, Indigenous-knowledge, affected-party, and public-authority decisions remain absent. Māori wording, taonga or mātauranga treatment, musical or cultural context, Māori data governance, and Māori authority remain exact-gated to competent and affected authorities, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority.",
        "", "## Source-bounded novelty and honest uncertainty", "",
        "The inherited repository declares a 6,190-row frozen proposal chain, but no single reachable exact-tree ledger materializes every declared historical row. Elowen therefore refuses a universal novelty claim. A bounded exact-source docs-tree audit parsed 1,752 proposal-named JSON blobs, recovered 7,318 proposal occurrences, 2,135 proposal identifiers, and 2,009 unique titles, and compared all forty candidate titles against every recovered title using the unchanged 0.72 token-Jaccard collision threshold. Exact-term review found no title using music box, cylinder music box, disc music box, mechanical music, comb tooth, or musical instrument. Pipe-organ work was rejected because windchest terms were already represented; bellfounding was rejected after one reachable hit. Zero threshold collisions supports bounded distinctness in reachable evidence; it is not exhaustive semantic proof over compressed or unavailable history.",
        "", "## Forty proposal contracts and falsification", "",
        f"Forty genuinely distinct Elowen proposal contracts are frozen with exactly one expected disposition each: {OUTCOMES}. Every row names a hypothesis, null or failure condition, approval class, execution lane, official or primary-source need, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, and expected disposition. The first twenty-eight are eligible only for bounded owner-local completed outcomes. The next eight are represented because their formal or synthetic surfaces cannot supply real-world evidence. Two remain open gaps for a zero-call Smithsonian Open Access adapter and for real observations, measurements, playback, specialist examination, and independent review. Two remain exact gates for professional conservation, repair, material, electrical, handling, treatment, and release decisions and for ownership, custody, copyright, recording, performance, cultural, Māori data-governance, and authority decisions. Four invalid mutations per proposal are preregistered for 160 required rejections in x2.",
        "", "## Retained failures and Method Flow", "",
        f"{len(STARTUP_FAILURES)} Elowen startup or x1-construction failures are retained at zero initial-pass credit. They include response-budget overflows, PowerShell selector and comparison faults, guessed receipt shapes, opaque bounded wrappers, overbroad archive and source-tree searches, unsupported pathspecs, no-checkout sparse-index surprises, repeated status overflows, a web result-envelope assumption, and an oversized builder projection. Each has one failed witness, one bounded recovery witness, a recurrence guard, a rollback boundary, and an append-only Method Flow transition to preferred only after its own passing witness. Tamar's post-final receipt-key projection failure is carried separately in the activation overlay, and Tamar's repository-sealed totals are never rewritten.",
        "", "## Portfolios, local skills, runners, and successor seeds", "",
        "The x1 portfolio freezes sixty safe-now tasks, thirty bounded candidates, twenty exact-approval packets, ten blocked packets, twenty owner-local skill ideas, ten family-current runner ideas, sixty additive CLEAN/FIX/REFINE tasks, ten successor skill recommendations, ten successor runner recommendations, and thirty successor CLEAN/FIX/REFINE recommendations. Inherited artifacts and successor recommendations receive zero Elowen novelty or completion credit. The ordinary phase target of three substantive tools is subordinate to evidence and relevance and is never a quota. X2 may materialize only owner-local files below the 2,000-file stop. Skills may be initialized through the official creator workflow, customized, completely read, quick-validated, and accepting/rejecting smoke-used locally; they are not globally installed. Family-current ghc_family_* and build_ghc_family_* compatibility remains protected.",
        "", "## Sources and zero-row discipline", "",
        "Current official or primary pages from the Canadian Conservation Institute, the Smithsonian Institution, W3C, the RFC Editor, and NIST supply vocabulary and refusal conditions only. The source work makes no dataset or API request, downloads no collection row or media item, ingests no observation, and performs no third-party write. Canadian guidance supplies high-level musical-instrument care boundaries; one Smithsonian object record supplies bounded cylinder-music-box vocabulary; Smithsonian Open Access developer guidance defines only a possible zero-call adapter surface. Those sources increase the need for abstention: a citation is not an object examination, measurement, playback, diagnosis, treatment instruction, safety release, cultural mandate, consent, legal conclusion, or authority grant.",
        "", "## Privacy, accessibility, and security", "",
        "Five privacy classes cover raw task or thread identifiers, private absolute paths, private routes or callable details, credential assignments, and transcripts or session streams. Scanner definitions and synthetic test strings are candidates requiring exact-file adjudication; other hits fail closed. Condition-map structure will include headings, table headers, text equivalents, non-colour cues, status language, focus-order obligations, and supersession. Structural checks do not establish complete accessibility. Manual keyboard, browser, assistive-technology, cognitive, language, security-usability, Māori-language, and affected-user evaluation remain reserved. Bounded changed-code compilation, AST review, mutation rejection, and privacy scanning are not exhaustive security or complete privacy assurance.",
        "", "## Strict x1-before-x2 and terminal validation hold", "",
        "This x1 must remain planning-only. It is staged from an exact owner allowlist, tested with its dependency-closed current suite, parsed as JSON, checked for Method Flow structure, scanned across five privacy classes, reviewed for stale labels and diff hygiene, and sealed in a normalized-LF exact staged Git-blob manifest. It must then be committed, pushed, clean, typed zero divergent, and equal across local, upstream, tracking, and fresh live remote before any x2 file or observed outcome exists. Later, only after a clean pushed final, Elowen may invoke at most one attributable exact-final owner-scoped canonical aggregate. A success is never replayed; a failure remains zero canonical-success credit and any narrow dependency correction must be separately named.",
        "", "## Route hold", "",
        "No task has been created or forked, no collaboration subagent has been spawned, no standby record has been contacted, and no prospective successor has been precontacted. The successor field is intentionally unresolved in x1. Only after Elowen's own clean, pushed, fresh-live-equal exact final and one successful non-replayed canonical aggregate may the newest live authority and roster be refreshed, the current registry bounded, exactly one authorized title locally required and immediately reread, duplicate and pause guards applied, and one sanitized existing-task message sent if every gate permits. Absence, ambiguity, pause, redirect, rename, standby state, usage exhaustion, duplicate activation, missing acknowledgement, privacy risk, or any protected gate stops the route.",
        "", "## Twenty inherited selections with zero Elowen credit", "",
    ]
    prose.extend(f"- {row['source_proposal_id']}: {row['source_title']} — inherited integrity evidence only." for row in inherited)
    prose.extend(["", "## Forty frozen Elowen proposals", ""])
    prose.extend(f"- {row['proposal_id']} [{row['planned_outcome']}]: {row['title']}." for row in proposals)
    prose.extend(["", "## Terminal truth", "", BOUNDARY, "", "NOT_READY_FOR_STAGE_20."])
    return "\n".join(prose)

def build() -> None:
    head, branch = git_text("rev-parse", "HEAD"), git_text("branch", "--show-current")
    if head != SOURCE_FINAL or branch != BRANCH:
        raise SystemExit(f"x1 requires {BRANCH} at {SOURCE_FINAL}; found {branch} at {head}")
    if any((OWNER_ROOT / name).exists() for name in ("x2", "closeout", "final", "seal")):
        raise SystemExit("x1 refuses a lane containing x2 or closeout material")
    source_rows = json_blob(SOURCE_FINAL, "docs/tamar-vey/v672-v7/closeout/proposal-ledger-final.json")["rows"]
    if len(source_rows) != 40:
        raise SystemExit("source proposal ledger must contain forty Tamar rows")
    inherited = [
        {
            "selection_id": f"EC6728-I{i:03d}", "source_owner": "Tamar Vey", "source_phase": "v672-v7",
            "source_proposal_id": row["proposal_id"], "source_title": row["title"], "source_outcome": row["observed_outcome"],
            "source_row_sha256": hashlib.sha256(json.dumps(row, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
            "integrity_revalidated": True, "elowen_novelty_credit": 0, "elowen_completion_credit": 0,
            "state": "inherited_evidence_only",
        }
        for i, row in enumerate(source_rows[:20], start=1)
    ]
    proposals = proposal_rows()
    if len(proposals) != 40 or len({row["title"] for row in proposals}) != 40 or Counter(row["planned_outcome"] for row in proposals) != Counter(OUTCOMES):
        raise SystemExit("proposal count, uniqueness, or distribution drifted")
    corpus_summary, source_titles = recover_proposal_corpus()
    if corpus_summary["malformed_or_missing_blobs"] or corpus_summary["corpus_sha256"] != SOURCE_TREE_CORPUS_SHA256:
        raise SystemExit("exact source-tree proposal corpus drifted or contained malformed blobs")
    if corpus_summary["candidate_git_blob_paths"] != 1752 or corpus_summary["semantic_occurrences"] != 7318 or corpus_summary["unique_proposal_ids"] != 2135 or corpus_summary["unique_titles"] != 2009:
        raise SystemExit(f"source-tree proposal audit count drift: {corpus_summary}")
    if not {row["title"] for row in source_rows} <= set(source_titles):
        raise SystemExit("source outcome titles are not all represented in the exact-tree audit")
    neighbors, max_score = [], 0.0
    for row in proposals:
        left, best_title, best_score = normalize(row["title"]), None, 0.0
        for source_title in source_titles:
            right = normalize(source_title)
            score = len(left & right) / max(1, len(left | right))
            if score > best_score:
                best_title, best_score = source_title, score
        max_score = max(max_score, best_score)
        neighbors.append({"proposal_id": row["proposal_id"], "source_title": best_title, "jaccard": round(best_score, 6), "collision": best_score >= 0.72})
    if any(row["collision"] for row in neighbors):
        raise SystemExit("semantic neighbor collision requires proposal rewrite")
    frozen_portfolio = portfolio()
    counts = {key: len(value) for key, value in frozen_portfolio.items()}
    expected = {"safe_now": 60, "candidates": 30, "exact_approval": 20, "blocked": 10, "skills": 20, "runners": 10, "clean_fix_refine": 60, "successor_skills": 10, "successor_runners": 10, "successor_clean_fix_refine": 30}
    if counts != expected:
        raise SystemExit(f"portfolio count drift: {counts}")
    source = verify_source()
    if not source["all_equal"] or not source["parent_chain"]["exact"] or source["phase_commits"] != 3 or source["merge_commits"] != 0 or source["commit_local_manifest_mismatches"] != 0 or not source["activation_packet"]["integrity_valid"]:
        raise SystemExit("immutable source verification failed")
    x1_overlay = {
        **ACTIVATION_OVERLAY,
        "effective_negatives": ACTIVATION_OVERLAY["effective_negatives"] + len(STARTUP_FAILURES),
        "effective_methods": ACTIVATION_OVERLAY["effective_methods"] + len(STARTUP_FAILURES),
        "failed_witnesses": ACTIVATION_OVERLAY["failed_witnesses"] + len(STARTUP_FAILURES),
        "bounded_passing_witnesses": ACTIVATION_OVERLAY["bounded_passing_witnesses"] + len(STARTUP_FAILURES),
        "elowen_startup_failures": len(STARTUP_FAILURES),
        "repository_seal_rewritten": False,
    }
    write_json("x1/activation-intake.json", {"schema": "ghc.family.activation-intake.v5", "owner": OWNER, "phase": PHASE, "source_verification": source, "task_creation_count": 0, "fork_count": 0, "subagent_count": 0, "standby_contact_count": 0})
    write_json("x1/identity-and-boundary.json", {"schema": "ghc.family.identity-boundary.v4", "owner": OWNER, "phase": PHASE, "pronouns": "they/them", "relational_role": "relational boundary cartographer and evidence steward", "relational_hope": HOPE, "identity_boundary": IDENTITY_BOUNDARY, "corrigibility": "Hamish may rename, pause, redirect, or stop the route."})
    write_json("x1/source-count-overlay.json", {"schema": "ghc.family.source-count-overlay.v5", "repository_sealed": REPOSITORY_SEAL, "live_activation_overlay": ACTIVATION_OVERLAY, "elowen_x1_overlay": x1_overlay})
    write_json("x1/inherited-proposal-revalidation.json", {"schema": "ghc.family.inherited-proposal-revalidation.v5", "owner": OWNER, "phase": PHASE, "selected": 20, "novelty_credit": 0, "completion_credit": 0, "rows": inherited})
    write_json("x1/semantic-neighbor-audit.json", {"schema": "ghc.family.semantic-neighbor-audit.v6", "owner": OWNER, "phase": PHASE, "exact_source_tree_corpus": corpus_summary, "source_tamar_titles_verified": 40, "reachable_unique_titles": len(source_titles), "declared_source_chain": 6190, "new_titles": 40, "max_jaccard": round(max_score, 6), "collision_threshold": 0.72, "collisions": 0, "rows": neighbors, "candidate_practice_exact_hits": {"music_box": 0, "cylinder_music_box": 0, "disc_music_box": 0, "mechanical_music": 0, "comb_tooth": 0, "musical_instrument": 0}, "rejected_materially_represented_practices": ["pipe organ and windchest", "bellfounding", "stained and leaded glass", "dry-stone construction", "ornamental plaster", "mechanical calculators", "upholstery", "calligraphy"], "universal_novelty_claim": False, "canonical_row_mapping_open_gap": True})
    write_json("x1/new-proposal-freeze.json", {"schema": "ghc.family.new-proposal-freeze.v6", "owner": OWNER, "phase": PHASE, "proposal_chain_before": 6190, "proposal_chain_after_if_evidence_frozen": 6230, "outcomes": OUTCOMES, "planned_invalid_mutations_per_proposal": 4, "planned_invalid_mutations": 160, "rows": proposals})
    write_json("x1/portfolio-freeze.json", {"schema": "ghc.family.remastered-portfolio-freeze.v6", "owner": OWNER, "phase": PHASE, "rows": frozen_portfolio, "counts": counts, "ordinary_phase_new_tool_target": 3, "ordinary_phase_tool_target_is_subordinate": True, "bounded_practice_lenses": ["synthetic cylinder music-box documentation with case, bedplate, cylinder, pin-track, comb, spring-motor, tune-attribution, condition-cue, provenance, privacy, and treatment abstention", "synthetic disc music-box documentation with disc, perforation, carrier, spindle, drive, label, storage, rights, compatibility, and operation abstention", "synthetic orchestra or auxiliary-component music-box documentation with bell, drum, beater, relation, timing, acoustic-measurement vacancy, accessibility, workload, and handover"], "successor_practice_recommendation": "synthetic hand-cranked optical-toy documentation with component identity, sequence vacancy, correction, accessibility, workload, and handover; recommendation only for the terminally authorized successor", "successor_practice_recommendation_count": 1, "inherited_portfolio_completion_credit": 0, "successor_recommendation_completion_credit": 0, "filler_prohibited": True})
    write_json("x1/source-ledger.json", {"schema": "ghc.family.public-source-ledger.v6", "owner": OWNER, "phase": PHASE, "retrieved_nz_date": "2026-08-28", "sources": [
        {"title": "Musical instruments", "publisher": "Canadian Conservation Institute", "url": "https://www.canada.ca/en/conservation-institute/services/care-objects/musical-instruments.html", "status": "current_official_page_checked_2026-08-28", "use": "high-level musical-instrument care, handling, environment, and professional-conservation boundaries only"},
        {"title": "Orchestra Cylinder Music Box", "publisher": "Smithsonian National Museum of American History", "url": "https://americanhistory.si.edu/collections/object/nmah_605774", "status": "current_official_object_page_checked_2026-08-28", "use": "bounded cylinder-music-box and auxiliary-component vocabulary only; not a downloaded or ingested collection row"},
        {"title": "Smithsonian Open Access Developer Tools", "publisher": "Smithsonian Institution", "url": "https://www.si.edu/openaccess/devtools", "status": "current_official_page_checked_2026-08-28", "use": "zero-call adapter provenance and request-schema vacancy only"},
        {"title": "PROV-O: The PROV Ontology", "publisher": "World Wide Web Consortium", "url": "https://www.w3.org/TR/prov-o/", "status": "stable_primary_standard", "use": "entity, activity, derivation, invalidation, and provenance vocabulary only"},
        {"title": "Web Content Accessibility Guidelines 2.2", "publisher": "World Wide Web Consortium", "url": "https://www.w3.org/TR/WCAG22/", "status": "current_primary_recommendation", "use": "structural accessibility vocabulary and manual-evaluation reservation"},
        {"title": "Verifiable Credentials Data Model v2.0", "publisher": "World Wide Web Consortium", "url": "https://www.w3.org/TR/vc-data-model-2.0/", "status": "current_primary_recommendation", "use": "credential vocabulary for a zero-key nonproduction representation only"},
        {"title": "RFC 8785: JSON Canonicalization Scheme", "publisher": "RFC Editor", "url": "https://www.rfc-editor.org/rfc/rfc8785", "status": "stable_primary_standard", "use": "canonical JSON ordering and numeric-domain refusal vocabulary only"},
        {"title": "The International System of Units (SI), NIST SP 330", "publisher": "National Institute of Standards and Technology", "url": "https://www.nist.gov/pml/special-publication-330", "status": "current_official_edition_page_checked_2026-08-28", "use": "unit and dimensional vocabulary with measurement and calibration vacancies"},
    ], "read_only_source_page_checks": 8, "failed_projection_attempts": 1, "api_calls": 0, "dataset_or_media_downloads": 0, "real_rows": 0, "external_writes": 0, "boundary": "Sources supply vocabulary and refusal conditions only; they are not observations, measurements, playback, professional advice, treatment instructions, safety release, legal interpretation, cultural legitimacy, consent, Māori authority, or Stage 20 evidence."})
    write_json("x1/threat-model.json", {"schema": "ghc.family.threat-model.v6", "owner": OWNER, "phase": PHASE, "assets": ["immutable source lineage", "planning-only x1 separation", "four truth labels", "retained failures", "synthetic-only fixtures", "authority vacancies", "route uniqueness"], "risks": [
        {"risk": "source or manifest drift", "control": "exact commits, normalized Git-blob replay, content-seal replay, and fresh live equality"},
        {"risk": "universal novelty overclaim", "control": "source-tree proposal-title comparison plus explicit unavailable canonical-row mapping gap"},
        {"risk": "condition or operation cue promoted into diagnosis treatment release playback or safety", "control": "zero-object fixtures, typed vacancies, and professional exact gates"},
        {"risk": "comb spring governor geometry or acoustic analogy promoted into physical evidence", "control": "analogy labels, zero measurements, unit vacancies, and GMUT observation firewall"},
        {"risk": "collection or tune vocabulary promoted into authorship copyright title access cultural or Indigenous authority", "control": "legal, affected-party, Māori, and competent-authority exact gates"},
        {"risk": "failure laundering", "control": "append-only Method Flow with paired failed and bounded passing witnesses"},
        {"risk": "private route identifier or precise-location leak", "control": "five-class exact-owner candidate adjudication and location minimization"},
        {"risk": "accessibility overclaim", "control": "structural-only checks with manual, language, assistive-technology, and affected-user evaluation reserved"},
        {"risk": "duplicate successor send", "control": "terminal live authority, exact-title reread, duplicate guard, acknowledgement, and no-resend"},
    ], "not_exhaustive_security": True})
    write_json("x1/method-flow-startup.json", method_flow())
    write_json("x1/workflow-plan.json", {"schema": "ghc.family.workflow-plan.v5", "owner": OWNER, "phase": PHASE, "steps": [{"step": "activation guidance and source verification", "state": "completed_read_only"}, {"step": "planning-only x1 freeze", "state": "in_progress_until_pushed_equal"}, {"step": "bounded x2 execution", "state": "blocked_by_x1_terminal_gate"}, {"step": "combined closeout and seal", "state": "pending"}, {"step": "one owner-scoped canonical aggregate", "state": "pending_not_invoked"}, {"step": "successor route", "state": "unresolved_until_terminal_live_authority"}], "commit_ceiling": 8, "planned_phase_commits": 3, "x1_commit_ceiling": 5, "x2_commit_ceiling": 5, "materialized_file_guard": 2000, "canonical_invocation_budget": 1, "canonical_success_budget": 1, "post_success_replay": False})
    write_json("x1/phase-truth.json", {"schema": "ghc.family.phase-truth.x1.v6", "owner": OWNER, "phase": PHASE, "primary_pillar": "Freed ID and CBR Heart", "protected_pillars": ["GMUT Mind", "THOS Body"], "bounded_practice_lens_count": 3, "proposal_rows": {"inherited_zero_credit": 20, "new": 40}, "expected_outcomes": OUTCOMES, "core_truth_labels": CORE_LABELS, "proposal_chain": {"before": 6190, "after_if_frozen": 6230}, "universal_novelty_claim": False, "canonical_row_mapping_open_gap": True, "startup_operational_failures": len(STARTUP_FAILURES), "x1_completion_credit": 0, "x2_execution_started": False, "real_people": 0, "real_objects_or_sites": 0, "real_world_actions": 0, "external_writes": 0, "identity_boundary": IDENTITY_BOUNDARY, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("x1/route-plan.json", {"schema": "ghc.family.route-plan.v5", "owner": OWNER, "phase": PHASE, "prospective_recipient_exact_title": None, "prospective_phase": None, "delivery_state": "UNRESOLVED_UNTIL_TERMINAL_LIVE_REFRESH", "successor_contact_count": 0, "task_creation_count": 0, "substitute_endpoint_count": 0, "standby_contact_count": 0, "required_gate": "clean pushed exact final, attributable terminal validation, newest live authority and roster, unique exact-title reread, duplicate guard, and acknowledged one-send"})
    text = overview(inherited, proposals)
    write_text("x1/integrated-overview.md", text)
    write_json("x1/build-receipt.json", {"schema": "ghc.family.x1-build-receipt.v6", "owner": OWNER, "phase": PHASE, "source_head": head, "branch": branch, "inherited_rows": 20, "new_rows": 40, "portfolio_counts": counts, "overview_words": len(text.split()), "read_only_source_page_checks": 8, "source_projection_failures": 1, "external_writes": 0, "x2_materialized": False})
    print(json.dumps({"owner": OWNER, "phase": PHASE, "new": 40, "outcomes": OUTCOMES, "portfolio": counts, "startup_failures": len(STARTUP_FAILURES), "overview_words": len(text.split()), "corpus": corpus_summary}, sort_keys=True))


def staged_paths() -> list[str]:
    return [line for line in git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if line]


def staged_review() -> None:
    paths = staged_paths()
    exact = {
        "scripts/build_ghc_family_elowen_cairn_v672_v8_x1.py",
        "tests/test_ghc_family_elowen_cairn_v672_v8_x1.py",
        "docs/elowen-cairn/v672-v8/validation/x1-method-flow-validation.json",
        "docs/elowen-cairn/v672-v8/validation/x1-validation-receipt.json",
        "docs/elowen-cairn/v672-v8/validation/x1-staged-privacy.json",
        "docs/elowen-cairn/v672-v8/validation/x1-staged-review.json",
        "docs/elowen-cairn/v672-v8/validation/x1-manifest.json",
    }
    out = [path for path in paths if not (path.startswith("docs/elowen-cairn/v672-v8/x1/") or path in exact)]
    mixed = [path for path in paths if any(part in path for part in ("/x2/", "/closeout/", "/final/", "/seal/")) or path.endswith(("_x2.py", "_final.py"))]
    payload = {"schema": "ghc.family.staged-review.v5", "owner": OWNER, "phase": PHASE, "lifecycle": "x1", "staged_before_self": paths, "staged_count_before_self": len(paths), "out_of_scope": out, "mixed_lifecycle": mixed, "valid": not out and not mixed}
    write_json("validation/x1-staged-review.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def manifest_from_index() -> None:
    exclusions = ["docs/elowen-cairn/v672-v8/validation/x1-manifest.json", "docs/elowen-cairn/v672-v8/validation/x1-staged-review.json"]
    entries = []
    for path in staged_paths():
        if path in exclusions:
            continue
        blob = git("show", f":{path}").stdout
        entries.append({"path": path, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})
    entries.sort(key=lambda row: row["path"])
    write_json("validation/x1-manifest.json", {"schema": "ghc.family.git-blob-manifest.v5", "domain": "x1 exact staged Git blobs before two declared self files", "hash_domain": "normalized_lf_exact_git_blob", "owner": OWNER, "phase": PHASE, "source_final": SOURCE_FINAL, "entry_count": len(entries), "entries": entries, "self_exclusions": exclusions})


def validation_receipt() -> None:
    json_paths = sorted((OWNER_ROOT / "x1").rglob("*.json"))
    text_paths = sorted(path for path in (OWNER_ROOT / "x1").rglob("*") if path.is_file())
    json_issues = []
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            json_issues.append({"path": path.relative_to(ROOT).as_posix(), "issue": type(exc).__name__})
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_route_or_callable": re.compile(r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"),
        "transcript_or_session_stream": re.compile(r"(?i)\b(?:session_stream|private_transcript|private_conversation_dump)\b"),
    }
    candidates = []
    for path in text_paths:
        text = path.read_text(encoding="utf-8")
        for label, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"path": path.relative_to(ROOT).as_posix(), "pattern_class": label})
    python_paths = [ROOT / "scripts" / "build_ghc_family_elowen_cairn_v672_v8_x1.py", ROOT / "tests" / "test_ghc_family_elowen_cairn_v672_v8_x1.py"]
    compile_issues = []
    for path in python_paths:
        try:
            compile(path.read_text(encoding="utf-8"), path.name, "exec")
        except SyntaxError as exc:
            compile_issues.append({"path": path.relative_to(ROOT).as_posix(), "issue": str(exc)})
    diff = git("diff", "--cached", "--check", check=False)
    materialized_files = len([path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts])
    payload = {
        "schema": "ghc.family.x1-validation-receipt.v1", "owner": OWNER, "phase": PHASE,
        "json_documents": len(json_paths), "json_issues": json_issues,
        "text_files": len(text_paths), "privacy_pattern_classes": sorted(patterns),
        "privacy_candidates": candidates, "confirmed_privacy_hits": 0 if not candidates else None,
        "python_compiles": len(python_paths), "python_compile_issues": compile_issues,
        "staged_paths_before_receipt": len(staged_paths()), "diff_hygiene_exit": diff.returncode,
        "diff_hygiene_output": diff.stdout.decode("utf-8", errors="replace"),
        "materialized_files": materialized_files, "file_guard": 2000,
        "x2_absent": not (OWNER_ROOT / "x2").exists(),
        "valid": not json_issues and not candidates and not compile_issues and diff.returncode == 0 and materialized_files < 2000 and not (OWNER_ROOT / "x2").exists(),
        "boundary": BOUNDARY,
    }
    write_json("validation/x1-validation-receipt.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def staged_privacy() -> None:
    self_path = "docs/elowen-cairn/v672-v8/validation/x1-staged-privacy.json"
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_route_or_callable": re.compile(r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"),
        "transcript_or_session_stream": re.compile(r"(?i)\b(?:session_stream|private_transcript|private_conversation_dump)\b"),
    }
    candidates = []
    scanned = 0
    for path in staged_paths():
        if path == self_path or Path(path).suffix.lower() not in {".py", ".json", ".md", ".txt", ".html"}:
            continue
        blob = git("show", f":{path}").stdout
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            candidates.append({"path": path, "pattern_class": "non_utf8_text", "disposition": "confirmed_payload_hit"})
            continue
        scanned += 1
        for label, pattern in patterns.items():
            if pattern.search(text):
                scanner_surface = path in {
                    "scripts/build_ghc_family_elowen_cairn_v672_v8_x1.py",
                    "tests/test_ghc_family_elowen_cairn_v672_v8_x1.py",
                }
                candidates.append({"path": path, "pattern_class": label, "disposition": "scanner_definition_or_unit_test" if scanner_surface else "confirmed_payload_hit"})
    confirmed = [row for row in candidates if row["disposition"] == "confirmed_payload_hit"]
    payload = {"schema": "ghc.family.staged-privacy-scan.v2", "owner": OWNER, "phase": PHASE, "lifecycle": "x1", "hash_domain": "exact_staged_git_blob", "pattern_classes": sorted(patterns), "scanned_text_files": scanned, "candidates": candidates, "confirmed_hits": confirmed, "confirmed_hit_count": len(confirmed), "self_exclusions": [self_path], "valid": not confirmed, "boundary": "Scanner definitions and unit-test strings are candidates, never payload hits; every other match fails closed."}
    write_json("validation/x1-staged-privacy.json", payload)
    if confirmed:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staged-review", action="store_true")
    parser.add_argument("--manifest-from-index", action="store_true")
    parser.add_argument("--validation-receipt", action="store_true")
    parser.add_argument("--staged-privacy", action="store_true")
    args = parser.parse_args()
    if args.staged_review:
        staged_review()
    elif args.manifest_from_index:
        manifest_from_index()
    elif args.validation_receipt:
        validation_receipt()
    elif args.staged_privacy:
        staged_privacy()
    else:
        build()


if __name__ == "__main__":
    main()
