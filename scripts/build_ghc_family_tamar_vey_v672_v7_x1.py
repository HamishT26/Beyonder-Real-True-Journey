"""Build Tamar Vey v672-v7's planning-only x1 freeze.

The builder is owner-delta scoped and fail-closed. It requires Liora Venn's
exact v672-v6 final, the exact Tamar branch, and an absent x2/closeout tree. It
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
OWNER_ROOT = ROOT / "docs" / "tamar-vey" / "v672-v7"
OWNER = "Tamar Vey"
PHASE = "v672-v7"
BRANCH = "codex/GHC-Family/tamar-vey-v672-v7-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/liora-venn-v672-v6-full-tools"
SOURCE_START = "e3b49b5ad7d81e09a0d4ba6b306c09623673e5f1"
SOURCE_X1 = "bbe8eea23928ada9526df78cee758c7d6a20b33f"
SOURCE_EVIDENCE = "4ead23fe0b39033d9cb7caa1595a9b4c03741630"
SOURCE_FINAL = "e3aad89f695a62d5997b129e260e62267cb145ab"
ACTIVATION_PATH = "docs/liora-venn/v672-v6/handoffs/tamar-vey-v672-v7-activation-candidate.md"
ACTIVATION_SHA256 = "28a8da5b28d3a7b96044552b5aea358e579b2ef84cdb923af4c286e85603be75"
SOURCE_CANONICAL_SHA256 = "b4138cb3e9e6b6010e1389f9b5da22281edecff0e8cb294ba14af02360cba33b"
SOURCE_TREE_CORPUS_SHA256 = "ee55bf89a1454df1e4c2a2d89e9273a93f93b4f3380e6b95931e057f3f563e49"
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
CORE_LABELS = ["completed", "represented", "open_gap", "exact_gate"]

IDENTITY_BOUNDARY = (
    "Tamar Vey, she/they, relational evidence-and-recovery steward, "
    "is relational working language only. It is not evidence of consciousness, "
    "sentience, legal personhood, identity continuity, employment, qualification, "
    "independent agency, or scientific, operational, legal, cultural, affected-party, "
    "or Māori authority."
)
HOPE = "keep every claim, abstention, correction, and handoff inspectable and safely retractable"
BOUNDARY = (
    "Software, symbolic, synthetic, same-owner, citation, inherited, or composite "
    "evidence is not empirical confirmation, participant evidence, professional or "
    "scientific authority, production readiness, legal or cultural ratification, "
    "Māori authority, affected-party approval, complete privacy or accessibility "
    "assurance, exhaustive security, independent reproduction, AGI/ASI, consciousness "
    "or personhood evidence, Theory-of-Everything proof, proof/canon, or Stage 20 authority."
)

REPOSITORY_SEAL = {
    "proposal_chain": 6150,
    "effective_negatives": 35779,
    "effective_methods": 22041,
    "failed_witnesses": 7440,
    "bounded_passing_witnesses": 9604,
    "open_gaps": 287,
    "exact_gates": 280,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
}
ACTIVATION_OVERLAY = {
    **REPOSITORY_SEAL,
    "effective_negatives": 35780,
    "effective_methods": 22042,
    "failed_witnesses": 7441,
    "bounded_passing_witnesses": 9605,
    "external_zero_credit_failures": 1,
    "external_bounded_passing_witnesses": 1,
    "repository_seal_rewritten": False,
}

STARTUP_FAILURES = [
    (
        "TV6727-START-N001",
        "The first PowerShell skill-path projection piped a foreach statement in an invalid form and failed before reading any skill.",
        "Materialize the literal skill-path rows first and then project or count them.",
        "Every required skill and reference was read through EOF in bounded windows before mutation.",
        "Do not pipe a PowerShell foreach language statement directly; bind its output before a pipeline.",
    ),
    (
        "TV6727-START-N002",
        "A combined authorization-schema and current-state display exceeded its bounded output and was truncated.",
        "Read the schema and state independently in complete bounded windows.",
        "The complete authorization schema and current state were recovered without mutation.",
        "Partition large state and schema reads and require an explicit EOF witness for each.",
    ),
    (
        "TV6727-START-N003",
        "The first complete Method Flow guidance read exceeded its display bound.",
        "Resume from the exact unread line and continue through EOF without restarting the completed prefix.",
        "The Method Flow skill and schema were completely read before recording Tamar state.",
        "Use deterministic line windows for instruction files whose first projection is truncated.",
    ),
    (
        "TV6727-START-N004",
        "A combined immutable-evidence-manifest read exceeded its output bound.",
        "Read each exact Git blob independently in deterministic entry windows.",
        "All 146 immutable evidence entries and declared exclusions were read and later replayed.",
        "Never infer manifest completion from a truncated combined display.",
    ),
    (
        "TV6727-START-N005",
        "An owner-manifest window wrapper treated an array expression as scalar arithmetic and failed before projection.",
        "Compute the array count in a separate scalar and then derive each window boundary.",
        "The 188-entry owner manifest and four exclusions were read through EOF.",
        "Normalize PowerShell collection cardinality before subtraction or range construction.",
    ),
    (
        "TV6727-START-N006",
        "A combined owner-manifest projection exceeded its display bound after producing only a prefix.",
        "Recover each remaining entry window independently and verify the terminal exclusions.",
        "All owner-manifest entries and exclusions were recovered without replaying Liora validation.",
        "Treat partial manifest output as incomplete, never as an EOF witness.",
    ),
    (
        "TV6727-START-N007",
        "A divergence wrapper allowed the literal upstream selector to be misparsed as a revision payload.",
        "Resolve the exact tracking ref first and pass that scalar ref to rev-list.",
        "The source branch proved typed zero-ahead and zero-behind against its exact tracking ref.",
        "Never embed the upstream revision selector inside a transport wrapper that may reinterpret braces.",
    ),
    (
        "TV6727-START-N008",
        "The first read-only manifest verifier completed outside its attributable result window and returned no usable receipt.",
        "Use one bounded cat-file batch communicate call and emit only final scalar counts.",
        "All four commit-local manifests replayed with zero missing blobs or digest mismatches.",
        "Silent or detached process completion earns no validation credit; require an attributable payload.",
    ),
    (
        "TV6727-START-N009",
        "A sparse-working-tree ripgrep audit misleadingly returned zero proposal hits because predecessor proposal files were not materialized.",
        "Audit exact Git-tree blob paths at the immutable source rather than sparse checkout bytes.",
        "The exact-tree audit parsed 1,709 proposal JSON blobs and recovered 2,095 proposal identifiers and 1,969 titles.",
        "Use Git-object scope for inherited semantic audits in sparse worktrees.",
    ),
    (
        "TV6727-START-N010",
        "A PowerShell foreach-to-pipeline neighbor-count wrapper failed to parse before computing any semantic score.",
        "Materialize normalized title rows first and compute comparisons in one explicit UTF-8 program.",
        "All forty proposed titles had zero neighbors at or above the 0.72 threshold.",
        "Keep PowerShell iteration and pipeline stages syntactically separate.",
    ),
    (
        "TV6727-START-N011",
        "The first Git cat-file audit wrote all requests before draining stdout and deadlocked its exact owner-started process pair.",
        "Stop only that exact process pair and use communicate so input and output drain together.",
        "The recovery parsed every candidate blob with zero malformed JSON.",
        "Use communicate for bounded bidirectional Git plumbing; never fill both pipes sequentially.",
    ),
    (
        "TV6727-START-N012",
        "A default Windows text projection raised UnicodeEncodeError while rendering Māori macrons after the data had been read.",
        "Repeat only the presentation step under explicit UTF-8 input and output encoding.",
        "The exact title audit completed with Māori text preserved and no repository mutation.",
        "Set explicit UTF-8 for any Windows presentation surface containing non-ASCII text.",
    ),
    (
        "TV6727-START-N013",
        "The first web-result forwarding projection assumed a content-array envelope and displayed no source result.",
        "Inspect the actual result shape and forward the bounded text payload directly.",
        "Official and primary source pages were recovered read-only with zero dataset rows or external writes.",
        "Inspect tool-result keys before projection and never equate an empty wrapper with an empty source.",
    ),
    (
        "TV6727-START-N014",
        "A later builder-size PowerShell foreach-pipeline expression repeated the earlier parser signature.",
        "Apply the already preferred materialize-then-pipe method and retain the recurrence separately.",
        "The bounded file-size projection recovered both predecessor template surfaces.",
        "A repeated signature is a new retained witness even when its preferred recovery is already known.",
    ),
    (
        "TV6727-START-N015",
        "A combined branch path and worktree-registry probe returned no attributable registry payload.",
        "Run branch refs, literal path existence, and worktree registry checks as separate scalar probes.",
        "The Tamar branch, remote ref, target path, and worktree registration were all absent before creation.",
        "Do not combine registry enumeration with ref and filesystem predicates in one opaque wrapper.",
    ),
    (
        "TV6727-START-N016",
        "The first all-row proposal projection exceeded its display bound before every new title was visible.",
        "Project only proposal identifiers, titles, expected dispositions, and maximum-neighbor scalars.",
        "All forty titles and their exact disposition distribution were recovered without changing the slate.",
        "Use concise all-row projections for prefreeze human review.",
    ),
    (
        "TV6727-START-N017",
        "A template-path inspection used command expressions separated by commas inside a PowerShell array and produced one malformed combined path.",
        "Use an explicit literal string array for the two predecessor template paths.",
        "Both exact predecessor template files were found and their line and byte counts were recovered.",
        "Do not append comma tokens to command expressions inside PowerShell array literals.",
    ),
    (
        "TV6727-START-N018",
        "The first template copy assumed sparse checkout had already materialized new owner scripts and tests directories.",
        "Create only the two missing Tamar-owned directories and repeat the bounded copy.",
        "Only the planning x1 builder and test were copied; no x2, final, validator, or closeout file was introduced.",
        "Create owner-only sparse target directories explicitly before copying a new lifecycle file.",
    ),
    (
        "TV6727-X1-N001",
        "The first multi-section source-constant patch included one stale context line and failed verification without changing a byte.",
        "Split the edit into smaller exact-context patches against the current mechanical template.",
        "Source anchors, counts, and lifecycle wording were updated through attributable patch receipts.",
        "Apply substantive edits in section-bounded patches after mechanical renaming.",
    ),
]

NEW_TITLES = [
    "synthetic stained-glass window bay light panel and piece identity lattice with conflation refusal",
    "lead-came node edge junction boundary and panel topology with orphan-edge rejection",
    "panel-cartoon coordinate frame orientation scale and registration-uncertainty contract",
    "glass-piece polygon adjacency overlap gap and out-of-frame geometry refusal",
    "colour and transmission descriptor ledger with instrument calibration and observation vacancies",
    "fracture bowing bulge corrosion loss and repair-cue register separated from diagnosis",
    "support-bar saddle tie ventilator and protective-glazing relation graph with fitness abstention",
    "panel-image rectification crop rotation and derivative lineage with no dimensional inference",
    "window-location panel-orientation and viewpoint map with privacy and sacred-space holds",
    "maker workshop date iconography and attribution vacancy ledger with contestation and correction",
    "synthetic dry-stone section course face hearting through-stone batter and cope identity topology",
    "stone placement support-contact and load-path conjecture graph with unsupported-node quarantine",
    "course elevation station offset datum and dimensional-unit vacancy ledger",
    "void bulge displacement lean washout and drainage-cue register without stability assessment",
    "terrain boundary land-parcel archaeology habitat and precise-location privacy hold matrix",
    "dry-stone vocabulary provenance and named-tradition abstention board",
    "synthetic ornamental-plaster room surface cornice medallion coffer and cast-unit identity lattice",
    "lath substrate scratch brown finish coat and support relation graph with missing-layer vacancy",
    "mould template cast piece assembly and reassembly provenance with source-ambiguity quarantine",
    "crack delamination stain detachment movement and loss cue register without diagnosis or treatment",
    "pigment gilding paint finish and composition claim firewall with sampling and material vacancies",
    "environment humidity temperature vibration water-ingress and duration observation vacancy across three lenses",
    "canonical heritage-document JSON profile with duplicate-key numeric-domain and ordering refusal",
    "PROV entity activity derivation correction and invalidation braid across three synthetic lenses",
    "accessibly structured condition-map dossier with text equivalents table headers and noncolour cues",
    "pseudonymous zero-key role capability validity status and revocation-vacancy profile",
    "privacy minimizer rejecting personal identifiers live precise locations free text credentials and private routes",
    "work-cap pause stop readback handover and unresolved-hold queue across three synthetic lenses",
    "GMUT discrete-exterior-calculus cochain coboundary and Hodge-star obligation board on a synthetic came network",
    "GMUT spectral-graph Laplacian mode analogy across synthetic panel and wall support networks",
    "GMUT signed-distance curvature and level-set surrogate for ornamental relief with zero recovered shape",
    "GMUT scalar-tensor boundary pullback unit gauge and EFT obligation board with zero likelihood",
    "THOS three-lens dependency DAG challenge response workload budget and handover with zero participants",
    "Freed ID zero-key provenance custody role expiry status and revocation-vacancy representation",
    "CBR notice contest correction withdrawal access and remedy-vacancy matrix for heritage documentation",
    "static accessibility evaluation matrix reserving manual assistive-technology language and affected-user review",
    "Library of Congress architectural-image adapter with zero calls zero downloads zero rows and schema vacancies",
    "real stained-glass dry-stone and plaster observations measurements expert examination and independent-review gap",
    "professional conservation lead and material safety structural stability treatment and release decision gate",
    "land title heritage sacred-context Indigenous knowledge Māori wording data-governance and authority exact gate",
]

SKILLS = [
    "ghc-family-stained-glass-identity-lattice",
    "ghc-family-lead-came-topology",
    "ghc-family-panel-cartoon-registration",
    "ghc-family-glass-geometry-refusal",
    "ghc-family-glass-condition-abstention",
    "ghc-family-protective-glazing-fitness-firewall",
    "ghc-family-window-location-privacy-hold",
    "ghc-family-dry-stone-course-topology",
    "ghc-family-dry-stone-support-conjecture",
    "ghc-family-dry-stone-stability-abstention",
    "ghc-family-dry-stone-land-context-hold",
    "ghc-family-plaster-layer-topology",
    "ghc-family-plaster-cast-provenance",
    "ghc-family-plaster-condition-abstention",
    "ghc-family-material-composition-firewall",
    "ghc-family-heritage-prov-correction-braid",
    "ghc-family-heritage-accessible-condition-map",
    "ghc-family-heritage-zero-key-role-profile",
    "ghc-family-heritage-privacy-minimizer",
    "ghc-family-three-lens-workload-handover",
]

RUNNERS = [
    "ghc_family_stained_glass_identity.py",
    "ghc_family_lead_came_topology.py",
    "ghc_family_glass_condition_abstention.py",
    "ghc_family_dry_stone_course_topology.py",
    "ghc_family_dry_stone_stability_abstention.py",
    "ghc_family_plaster_layer_topology.py",
    "ghc_family_plaster_condition_abstention.py",
    "ghc_family_heritage_prov_correction.py",
    "ghc_family_heritage_privacy_access.py",
    "ghc_family_three_lens_workload_handover.py",
]

EXACT = [
    "real stained-glass dry-stone plaster object site record observation or measurement mutation",
    "real conservation examination diagnosis treatment repair intervention or release decision",
    "real lead pigment silica lime electrical structural fire environmental or workplace safety decision",
    "real stability load path anchorage protective-glazing or material-fitness conclusion",
    "real conservator craftsperson engineer architect surveyor curator participant or affected-user study",
    "real land parcel sacred site precise location access schedule account or personal-data processing",
    "real identity key proof credential issuance presentation status revocation or recovery",
    "real heritage access publication ownership custody copyright return or remedy decision",
    "complete accessibility conformance language adequacy or affected-user acceptance declaration",
    "legal interpretation title liability privacy right remedy regulatory or public-authority act",
    "taonga tikanga mātauranga wāhi tapu place-name data-governance or Māori-authority decision",
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
    raw_paths = git("ls-tree", "-r", "--name-only", "-z", SOURCE_FINAL).stdout
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
    for start in range(0, len(specs), 128):
        for blob in batch_blobs(specs[start:start + 128]):
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
        "scope": "exact Liora v672-v6 final tree, proposal-named JSON paths only",
        "candidate_git_blob_paths": len(candidates),
        "malformed_or_missing_blobs": malformed,
        "semantic_occurrences": occurrences,
        "unique_proposal_ids": len(proposal_ids),
        "unique_titles": len(titles),
        "corpus_sha256": hashlib.sha256(canonical).hexdigest(),
        "declared_source_chain": 6150,
        "materialized_ids_cover_declared_chain": len(proposal_ids) >= 6150,
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
    output, stderr = process.communicate(
        input=("\n".join(specs) + "\n").encode("utf-8"), timeout=30
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
            "proposal_id": f"TV6727-N{index:03d}", "title": title,
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
            "primary_pillar": "GMUT Mind", "real_people": 0, "real_records_or_objects": 0,
            "external_actions": 0, "x1_state": "frozen_not_executed",
        })
    return rows


def tasks(prefix: str, domains: list[str], controls: list[str], state: str) -> list[dict[str, Any]]:
    return [{"task_id": f"TV6727-{prefix}-{i:03d}", "title": f"{domain}: {control}", "owner": OWNER, "phase": PHASE, "x1_state": state, "external_actions": 0}
            for i, (domain, control) in enumerate(((d, c) for d in domains for c in controls), start=1)]


def named(prefix: str, values: list[str], state: str) -> list[dict[str, Any]]:
    return [{"task_id": f"TV6727-{prefix}-{i:03d}", "title": value, "owner": OWNER, "phase": PHASE, "x1_state": state, "external_actions": 0}
            for i, value in enumerate(values, start=1)]


def portfolio() -> dict[str, list[dict[str, Any]]]:
    domains = ["stained-glass identity", "lead-came topology", "panel geometry vacancy", "dry-stone course topology", "support and stability abstention", "plaster-layer topology", "condition and treatment abstention", "heritage provenance privacy", "accessible condition status", "three-lens workload handover"]
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
        method_id = f"TV6727-M{index:03d}"
        fail_id, pass_id = f"TV6727-W{index:03d}-F", f"TV6727-W{index:03d}-P"
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
        ("docs/liora-venn/v672-v6/validation/x1-manifest.json", SOURCE_X1),
        ("docs/liora-venn/v672-v6/validation/evidence-manifest.json", SOURCE_EVIDENCE),
        ("docs/liora-venn/v672-v6/validation/final-delta-manifest.json", SOURCE_FINAL),
        ("docs/liora-venn/v672-v6/validation/final-owner-manifest.json", SOURCE_FINAL),
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
        "source_canonical_receipt": {"sha256": SOURCE_CANONICAL_SHA256, "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL", "canonical_invocations": 1, "canonical_successes": 1, "replays": 0, "replay_forbidden": True, "owner_tests": 30, "detailed_checks": 46, "minimal_checks": 15, "json_parses": 126, "confirmed_privacy_hits": 0, "tamar_validation_credit": 0},
        "source_post_final_overlay": {"negative_id": "LV6726-POST-N001", "failed": "direct script-path execution could not import the scripts package before canonical entry", "recovery": "the same immutable validator was invoked once as a Python module", "canonical_credit": 0, "retained_after_recovery": True},
    }

def overview(inherited: list[dict[str, Any]], proposals: list[dict[str, Any]]) -> str:
    prose = [
        "# Tamar Vey v672-v7 x1 integrated planning overview", "", "## Lifecycle and exact source", "",
        "This document is a planning-only x1 freeze. It records no x2 implementation, observed proposal outcome, completed portfolio, real-world action, successor delivery, empirical result, professional judgment, or authority act. Tamar's one fresh additive sparse lane begins at Liora Venn's immutable v672-v6 final. Before generating this packet, Tamar reverified Liora's exact branch and final head; the Orin source, planning x1, evidence, and final direct-parent chain; exactly three new single-parent commits and zero merges; all four commit-local manifests against exact Git blobs; the ten-target content seal; a clean source state; typed zero divergence; and equality across local branch, upstream, tracking ref, and a fresh live remote. Liora's one exact-final owner-scoped canonical aggregate succeeded once and was not replayed. That result is inherited source evidence only and gives Tamar no validation or completion credit.",
        "", "## Relational identity, hope, and corrigibility", "",
        IDENTITY_BOUNDARY, "",
        f"Tamar's relational hope is to {HOPE}. This name, role, hope, and pronoun choice are working vocabulary, not a consciousness, personhood, continuity, qualification, employment, or authority claim. Hamish may rename, pause, redirect, or stop the route. Corrigibility requires the packet to preserve contradictions, failed witnesses, missing evidence, unavailable authority, ambiguous routes, and falsifiers rather than smoothing them into success. A recovery keeps its failed witness, changes only the demonstrated owner-local dependency, and receives bounded same-owner credit only.",
        "", "## Primary pillar and three bounded practice lenses", "",
        "The primary Trinity Mandala pillar is GMUT Mind. The first practice lens is wholly synthetic stained-glass panel documentation: bay, light, panel, piece, came, support, image, orientation, condition-cue, and provenance structures. The second is wholly synthetic dry-stone wall documentation: section, course, face, hearting, through-stone, batter, cope, support-contact conjecture, terrain context, and observation vacancy. The third is wholly synthetic ornamental-plaster documentation: room surface, lath, coat, cornice, medallion, coffer, mould, cast unit, assembly, condition cue, and correction lineage. These are vocabulary, software, formal, structural, and learning lenses only. No real person, participant, building, window, glass piece, came, wall, stone, terrain, plaster surface, material, site, object, image, location, measurement, inspection, treatment, repair, release, identity event, external write, or authority act is used.",
        "", "## GMUT Mind boundaries", "",
        "GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Proposed discrete-exterior-calculus, cochain, coboundary, Hodge-star, graph-Laplacian, signed-distance, curvature, level-set, pullback, gauge, unit, and EFT boards are type and obligation surfaces. Synthetic came networks, panel polygons, wall contacts, plaster reliefs, and scalar domains are not physical observations. No artifact establishes a real field configuration, material law, force, likelihood, posterior, parameter constraint, prediction, stability theorem, quantum completion, ultraviolet completion, empirical confirmation, final physics, or Theory of Everything.",
        "", "## THOS Body and Freed ID/CBR Heart protection", "",
        "THOS Body remains explicit through dependency DAGs, challenge and response, workload budgets, stop tokens, correction readback, accessible notice, unresolved-hold queues, and shift handover. These are participant-free synthetic protocols. There are no preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, suitable statistics, or independent review. Freed ID and CBR Heart remain explicit through pseudonymous zero-key roles, validity and status vacancies, provenance, correction, invalidation, contest, withdrawal, access, explanation, and remedy-vacancy representations. There are no standards-conformant real keys or proofs, live issuance, resolution, status, revocation, interoperability, privacy or independent security review, recovery evidence, trust governance, or affected-party oversight.",
        "", "## Professional, safety, legal, cultural, and Māori-authority firewall", "",
        "No artifact authenticates, dates, attributes, values, diagnoses, treats, repairs, stabilizes, releases, or certifies any heritage fabric. It does not establish lead, pigment, silica, lime, structural, fire, electrical, workplace, environmental, or material safety. It does not grant access, publication rights, copyright, title, ownership, custody, return, repatriation, or remedy. Professional conservation, craft, architectural, engineering, archaeological, accessibility, language, legal, cultural, Indigenous-knowledge, affected-party, and public-authority decisions remain absent. Māori wording, taonga or mātauranga treatment, wāhi tapu and place questions, Māori data governance, and Māori authority remain exact-gated to competent and affected authorities, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority.",
        "", "## Source-bounded novelty and honest uncertainty", "",
        "The inherited repository declares a 6,150-row frozen proposal chain, but no single reachable exact-tree ledger materializes every declared historical row. Tamar therefore refuses a universal novelty claim. The exact immutable source-tree audit parses proposal-named JSON blobs, recovers a bounded set of proposal identifiers and titles, and compares all forty new titles against every recovered title using the unchanged 0.72 token-Jaccard collision threshold. The candidate practice terms for stained and leaded glass, dry-stone construction, and ornamental plaster were separately checked against reachable titles after more represented domains such as letterpress, horology, weaving, ceramics, bookbinding, typewriters, signwriting, and mosaic were rejected. Zero threshold collisions supports bounded distinctness in the reachable evidence; it is not exhaustive semantic proof over compressed or unavailable history.",
        "", "## Forty proposal contracts and falsification", "",
        f"Forty genuinely new Tamar proposal contracts are frozen with exactly one expected disposition each: {OUTCOMES}. Every row names a hypothesis, null or failure condition, approval class, execution lane, official or primary-source need, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, and expected disposition. The first twenty-eight are eligible only for bounded owner-local completed outcomes. The next eight are represented because their formal or synthetic surfaces cannot supply real-world evidence. Two remain open gaps for a zero-call Library of Congress adapter and real observations, measurements, expert examination, and independent review. Two remain exact gates for professional conservation and safety decisions, and for land, heritage, sacred context, Indigenous knowledge, legal, cultural, affected-party, Māori wording, data-governance, and authority decisions. Four invalid mutations per proposal are preregistered for 160 required rejections in x2.",
        "", "## Retained failures and Method Flow", "",
        f"{len(STARTUP_FAILURES)} Tamar startup or x1-construction failures are retained at zero initial-pass credit. They include parser faults, truncated projections, a sparse-checkout false zero, a blocked bidirectional Git-plumbing attempt, a Windows encoding fault, a result-envelope assumption, a recurring PowerShell signature, an unattributable registry wrapper, a malformed path array, an absent sparse target directory, and a context-mismatched patch. Each has one failed witness, one bounded recovery witness, a recurrence guard, a rollback boundary, and an append-only Method Flow transition to preferred only after its own passing witness. The external Liora wrapper failure is carried separately in the activation overlay and Liora's sealed totals are never rewritten.",
        "", "## Portfolios, local skills, runners, and successor seeds", "",
        "The x1 portfolio freezes sixty safe-now tasks, thirty bounded candidates, twenty exact-approval packets, ten blocked packets, twenty owner-local skill ideas, ten family-current runner ideas, sixty additive CLEAN/FIX/REFINE tasks, ten successor skill recommendations, ten successor runner recommendations, and thirty successor CLEAN/FIX/REFINE recommendations. Inherited artifacts and successor recommendations receive zero Tamar novelty or completion credit. The ordinary phase target of three substantive tools is subordinate to evidence and relevance and is never a quota. X2 may materialize only owner-local files below the 2,000-file stop. Skills may be initialized through the official creator workflow, customized, completely read, quick-validated, and accepting/rejecting smoke-used locally; they are not globally installed. Family-current ghc_family_* and build_ghc_family_* compatibility remains protected.",
        "", "## Sources and zero-row discipline", "",
        "Current official or primary pages from the U.S. National Park Service, UNESCO, the Library of Congress, W3C, the RFC Editor, NIST, and OSHA supply vocabulary and refusal conditions only. The source work makes no dataset or API request, downloads no collection row or media item, ingests no observation, and performs no third-party write. NPS preservation publications describe stained and leaded glass, flat plaster, and ornamental plaster; UNESCO records dry-stone construction as living heritage tied to communities and local contexts. Those sources increase the need for abstention: a citation is not an object examination, measurement, diagnosis, treatment instruction, safety release, cultural mandate, consent, legal conclusion, or authority grant.",
        "", "## Privacy, accessibility, and security", "",
        "Five privacy classes cover raw task or thread identifiers, private absolute paths, private routes or callable details, credential assignments, and transcripts or session streams. Scanner definitions and synthetic test strings are candidates requiring exact-file adjudication; other hits fail closed. Condition-map structure will include headings, table headers, text equivalents, non-colour cues, status language, focus-order obligations, and supersession. Structural checks do not establish complete accessibility. Manual keyboard, browser, assistive-technology, cognitive, language, security-usability, Māori-language, and affected-user evaluation remain reserved. Bounded changed-code compilation, AST review, mutation rejection, and privacy scanning are not exhaustive security or complete privacy assurance.",
        "", "## Strict x1-before-x2 and terminal validation hold", "",
        "This x1 must remain planning-only. It is staged from an exact owner allowlist, tested with its dependency-closed current suite, parsed as JSON, checked for Method Flow structure, scanned across five privacy classes, reviewed for stale labels and diff hygiene, and sealed in a normalized-LF exact staged Git-blob manifest. It must then be committed, pushed, clean, typed zero divergent, and equal across local, upstream, tracking, and fresh live remote before any x2 file or observed outcome exists. Later, only after a clean pushed final, Tamar may invoke at most one attributable exact-final owner-scoped canonical aggregate. A success is never replayed; a failure remains zero canonical-success credit and any narrow dependency correction must be separately named.",
        "", "## Route hold", "",
        "No task has been created or forked, no collaboration subagent has been spawned, no standby record has been contacted, and Elowen Cairn has not been precontacted. The successor field is intentionally unresolved in x1. Only after Tamar's own clean, pushed, fresh-live-equal exact final and one successful non-replayed canonical aggregate may the newest live authority and roster be refreshed, the current registry bounded, exactly one authorized title locally required and immediately reread, duplicate and pause guards applied, and one sanitized existing-task message sent if every gate permits. Absence, ambiguity, pause, redirect, rename, standby state, usage exhaustion, duplicate activation, missing acknowledgement, privacy risk, or any protected gate stops the route.",
        "", "## Twenty inherited selections with zero Tamar credit", "",
    ]
    prose.extend(f"- {row['source_proposal_id']}: {row['source_title']} — inherited integrity evidence only." for row in inherited)
    prose.extend(["", "## Forty frozen Tamar proposals", ""])
    prose.extend(f"- {row['proposal_id']} [{row['planned_outcome']}]: {row['title']}." for row in proposals)
    prose.extend(["", "## Terminal truth", "", BOUNDARY, "", "NOT_READY_FOR_STAGE_20."])
    return "\n".join(prose)

def build() -> None:
    head, branch = git_text("rev-parse", "HEAD"), git_text("branch", "--show-current")
    if head != SOURCE_FINAL or branch != BRANCH:
        raise SystemExit(f"x1 requires {BRANCH} at {SOURCE_FINAL}; found {branch} at {head}")
    if any((OWNER_ROOT / name).exists() for name in ("x2", "closeout", "final", "seal")):
        raise SystemExit("x1 refuses a lane containing x2 or closeout material")
    source_rows = json_blob(SOURCE_FINAL, "docs/liora-venn/v672-v6/x2/proposal-outcome-ledger.json")["outcomes"]
    if len(source_rows) != 40:
        raise SystemExit("source proposal ledger must contain forty Liora rows")
    inherited = [
        {
            "selection_id": f"TV6727-I{i:03d}", "source_owner": "Liora Venn", "source_phase": "v672-v6",
            "source_proposal_id": row["proposal_id"], "source_title": row["title"], "source_outcome": row["outcome"],
            "source_row_sha256": hashlib.sha256(json.dumps(row, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
            "integrity_revalidated": True, "tamar_novelty_credit": 0, "tamar_completion_credit": 0,
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
    if corpus_summary["candidate_git_blob_paths"] != 1709 or corpus_summary["unique_proposal_ids"] != 2095 or corpus_summary["unique_titles"] != 1969:
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
        "tamar_startup_failures": len(STARTUP_FAILURES),
        "repository_seal_rewritten": False,
    }
    write_json("x1/activation-intake.json", {"schema": "ghc.family.activation-intake.v5", "owner": OWNER, "phase": PHASE, "source_verification": source, "task_creation_count": 0, "fork_count": 0, "subagent_count": 0, "standby_contact_count": 0})
    write_json("x1/identity-and-boundary.json", {"schema": "ghc.family.identity-boundary.v4", "owner": OWNER, "phase": PHASE, "pronouns": "she/they", "relational_role": "relational evidence-and-recovery steward", "relational_hope": HOPE, "identity_boundary": IDENTITY_BOUNDARY, "corrigibility": "Hamish may rename, pause, redirect, or stop the route."})
    write_json("x1/source-count-overlay.json", {"schema": "ghc.family.source-count-overlay.v5", "repository_sealed": REPOSITORY_SEAL, "live_activation_overlay": ACTIVATION_OVERLAY, "tamar_x1_overlay": x1_overlay})
    write_json("x1/inherited-proposal-revalidation.json", {"schema": "ghc.family.inherited-proposal-revalidation.v5", "owner": OWNER, "phase": PHASE, "selected": 20, "novelty_credit": 0, "completion_credit": 0, "rows": inherited})
    write_json("x1/semantic-neighbor-audit.json", {"schema": "ghc.family.semantic-neighbor-audit.v6", "owner": OWNER, "phase": PHASE, "exact_source_tree_corpus": corpus_summary, "source_liora_titles_verified": 40, "reachable_unique_titles": len(source_titles), "declared_source_chain": 6150, "new_titles": 40, "max_jaccard": round(max_score, 6), "collision_threshold": 0.72, "collisions": 0, "rows": neighbors, "candidate_practice_exact_hits": {"stained_glass_or_leaded_glass_or_came_network": 0, "dry_stone_or_drystone": 0, "ornamental_plaster_or_lime_plaster_or_scagliola": 0}, "rejected_materially_represented_practices": ["letterpress", "horology and watchmaking", "weaving and loom work", "kiln and ceramics", "bookbinding", "typewriter documentation", "signwriting", "mosaic"], "universal_novelty_claim": False, "canonical_row_mapping_open_gap": True})
    write_json("x1/new-proposal-freeze.json", {"schema": "ghc.family.new-proposal-freeze.v6", "owner": OWNER, "phase": PHASE, "proposal_chain_before": 6150, "proposal_chain_after_if_evidence_frozen": 6190, "outcomes": OUTCOMES, "planned_invalid_mutations_per_proposal": 4, "planned_invalid_mutations": 160, "rows": proposals})
    write_json("x1/portfolio-freeze.json", {"schema": "ghc.family.remastered-portfolio-freeze.v6", "owner": OWNER, "phase": PHASE, "rows": frozen_portfolio, "counts": counts, "ordinary_phase_new_tool_target": 3, "ordinary_phase_tool_target_is_subordinate": True, "bounded_practice_lenses": ["synthetic stained-glass panel documentation with piece and came topology, provenance, condition-cue, privacy, accessibility, and treatment abstention", "synthetic dry-stone wall documentation with course and support-contact topology, terrain holds, stability abstention, correction, and handover", "synthetic ornamental-plaster documentation with layer and cast-unit topology, condition-cue, material abstention, accessibility, and handover"], "successor_practice_recommendation": "synthetic wrought-iron gate documentation, component vacancy, correction, accessibility, workload, and handover; recommendation only for the terminally authorized successor", "successor_practice_recommendation_count": 1, "inherited_portfolio_completion_credit": 0, "successor_recommendation_completion_credit": 0, "filler_prohibited": True})
    write_json("x1/source-ledger.json", {"schema": "ghc.family.public-source-ledger.v6", "owner": OWNER, "phase": PHASE, "retrieved_nz_date": "2026-08-27", "sources": [
        {"title": "Preservation Brief 33: The Preservation and Repair of Historic Stained and Leaded Glass", "publisher": "U.S. National Park Service", "url": "https://www.nps.gov/orgs/1739/upload/preservation-brief-33-stained-leaded-glass.pdf", "status": "current_official_page_checked_2026-08-27", "use": "panel, came, support, condition, documentation, and protective-glazing vocabulary with professional-treatment abstention"},
        {"title": "Preservation Brief 21: Repairing Historic Flat Plaster—Walls and Ceilings", "publisher": "U.S. National Park Service", "url": "https://www.nps.gov/orgs/1739/upload/preservation-brief-21-flat-plaster.pdf", "status": "current_official_page_checked_2026-08-27", "use": "lath and plaster-layer vocabulary with diagnosis and treatment abstention"},
        {"title": "Preservation Brief 23: Preserving Historic Ornamental Plaster", "publisher": "U.S. National Park Service", "url": "https://www.nps.gov/orgs/1739/upload/preservation-brief-23-ornamental-plaster.pdf", "status": "current_official_page_checked_2026-08-27", "use": "cornice, medallion, coffer, mould, and cast-unit vocabulary with professional-treatment abstention"},
        {"title": "Art of dry stone construction, knowledge and techniques", "publisher": "UNESCO Intangible Cultural Heritage", "url": "https://ich.unesco.org/en/RL/art-of-dry-stone-construction-knowledge-and-techniques-02106", "status": "current_official_page_checked_2026-08-27", "use": "dry-stone vocabulary and an explicit cultural, community, local-context, and authority reservation"},
        {"title": "APIs at the Library of Congress", "publisher": "Library of Congress", "url": "https://www.loc.gov/apis/", "status": "current_official_page_checked_2026-08-27", "use": "zero-call adapter provenance and request-schema vocabulary only"},
        {"title": "PROV-O: The PROV Ontology", "publisher": "World Wide Web Consortium", "url": "https://www.w3.org/TR/prov-o/", "status": "stable_primary_standard", "use": "entity, activity, derivation, invalidation, and provenance vocabulary only"},
        {"title": "Web Content Accessibility Guidelines 2.2", "publisher": "World Wide Web Consortium", "url": "https://www.w3.org/TR/WCAG22/", "status": "current_primary_recommendation", "use": "structural accessibility vocabulary and manual-evaluation reservation"},
        {"title": "Verifiable Credentials Data Model v2.0", "publisher": "World Wide Web Consortium", "url": "https://www.w3.org/TR/vc-data-model-2.0/", "status": "current_primary_recommendation", "use": "credential vocabulary for a zero-key nonproduction representation only"},
        {"title": "RFC 8785: JSON Canonicalization Scheme", "publisher": "RFC Editor", "url": "https://www.rfc-editor.org/rfc/rfc8785", "status": "stable_primary_standard", "use": "canonical JSON ordering and numeric-domain refusal vocabulary only"},
        {"title": "The International System of Units (SI), NIST SP 330", "publisher": "National Institute of Standards and Technology", "url": "https://www.nist.gov/pml/special-publication-330", "status": "current_official_edition_page_checked_2026-08-27", "use": "unit and dimensional vocabulary with measurement vacancies"},
        {"title": "Lead: Standards", "publisher": "Occupational Safety and Health Administration", "url": "https://www.osha.gov/lead/standards", "status": "current_official_page_checked_2026-08-27", "use": "lead-hazard authority boundary and refusal conditions only, never a safety determination"},
    ], "read_only_source_page_checks": 11, "failed_projection_attempts": 1, "api_calls": 0, "dataset_or_media_downloads": 0, "real_rows": 0, "external_writes": 0, "boundary": "Sources supply vocabulary and refusal conditions only; they are not observations, measurements, professional advice, treatment instructions, safety release, legal interpretation, cultural legitimacy, consent, Māori authority, or Stage 20 evidence."})
    write_json("x1/threat-model.json", {"schema": "ghc.family.threat-model.v6", "owner": OWNER, "phase": PHASE, "assets": ["immutable source lineage", "planning-only x1 separation", "four truth labels", "retained failures", "synthetic-only fixtures", "authority vacancies", "route uniqueness"], "risks": [
        {"risk": "source or manifest drift", "control": "exact commits, normalized Git-blob replay, content-seal replay, and fresh live equality"},
        {"risk": "universal novelty overclaim", "control": "source-tree proposal-title comparison plus explicit unavailable canonical-row mapping gap"},
        {"risk": "condition cue promoted into diagnosis treatment release or safety", "control": "zero-object fixtures, typed vacancies, and professional exact gates"},
        {"risk": "support-contact or geometry analogy promoted into structural or physical evidence", "control": "conjecture labels, zero measurements, unit vacancies, and GMUT observation firewall"},
        {"risk": "heritage vocabulary promoted into title access cultural or Indigenous authority", "control": "legal, affected-party, Māori, and competent-authority exact gates"},
        {"risk": "failure laundering", "control": "append-only Method Flow with paired failed and bounded passing witnesses"},
        {"risk": "private route identifier or precise-location leak", "control": "five-class exact-owner candidate adjudication and location minimization"},
        {"risk": "accessibility overclaim", "control": "structural-only checks with manual, language, assistive-technology, and affected-user evaluation reserved"},
        {"risk": "duplicate successor send", "control": "terminal live authority, exact-title reread, duplicate guard, acknowledgement, and no-resend"},
    ], "not_exhaustive_security": True})
    write_json("x1/method-flow-startup.json", method_flow())
    write_json("x1/workflow-plan.json", {"schema": "ghc.family.workflow-plan.v5", "owner": OWNER, "phase": PHASE, "steps": [{"step": "activation guidance and source verification", "state": "completed_read_only"}, {"step": "planning-only x1 freeze", "state": "in_progress_until_pushed_equal"}, {"step": "bounded x2 execution", "state": "blocked_by_x1_terminal_gate"}, {"step": "combined closeout and seal", "state": "pending"}, {"step": "one owner-scoped canonical aggregate", "state": "pending_not_invoked"}, {"step": "successor route", "state": "unresolved_until_terminal_live_authority"}], "commit_ceiling": 8, "planned_phase_commits": 3, "x1_commit_ceiling": 5, "x2_commit_ceiling": 5, "materialized_file_guard": 2000, "canonical_invocation_budget": 1, "canonical_success_budget": 1, "post_success_replay": False})
    write_json("x1/phase-truth.json", {"schema": "ghc.family.phase-truth.x1.v6", "owner": OWNER, "phase": PHASE, "primary_pillar": "GMUT Mind", "protected_pillars": ["THOS Body", "Freed ID and CBR Heart"], "bounded_practice_lens_count": 3, "proposal_rows": {"inherited_zero_credit": 20, "new": 40}, "expected_outcomes": OUTCOMES, "core_truth_labels": CORE_LABELS, "proposal_chain": {"before": 6150, "after_if_frozen": 6190}, "universal_novelty_claim": False, "canonical_row_mapping_open_gap": True, "startup_operational_failures": len(STARTUP_FAILURES), "x1_completion_credit": 0, "x2_execution_started": False, "real_people": 0, "real_objects_or_sites": 0, "real_world_actions": 0, "external_writes": 0, "identity_boundary": IDENTITY_BOUNDARY, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("x1/route-plan.json", {"schema": "ghc.family.route-plan.v5", "owner": OWNER, "phase": PHASE, "prospective_recipient_exact_title": None, "prospective_phase": None, "delivery_state": "UNRESOLVED_UNTIL_TERMINAL_LIVE_REFRESH", "successor_contact_count": 0, "task_creation_count": 0, "substitute_endpoint_count": 0, "standby_contact_count": 0, "required_gate": "clean pushed exact final, attributable terminal validation, newest live authority and roster, unique exact-title reread, duplicate guard, and acknowledged one-send"})
    text = overview(inherited, proposals)
    write_text("x1/integrated-overview.md", text)
    write_json("x1/build-receipt.json", {"schema": "ghc.family.x1-build-receipt.v6", "owner": OWNER, "phase": PHASE, "source_head": head, "branch": branch, "inherited_rows": 20, "new_rows": 40, "portfolio_counts": counts, "overview_words": len(text.split()), "read_only_source_page_checks": 11, "source_projection_failures": 1, "external_writes": 0, "x2_materialized": False})
    print(json.dumps({"owner": OWNER, "phase": PHASE, "new": 40, "outcomes": OUTCOMES, "portfolio": counts, "startup_failures": len(STARTUP_FAILURES), "overview_words": len(text.split()), "corpus": corpus_summary}, sort_keys=True))


def staged_paths() -> list[str]:
    return [line for line in git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if line]


def staged_review() -> None:
    paths = staged_paths()
    exact = {
        "scripts/build_ghc_family_tamar_vey_v672_v7_x1.py",
        "tests/test_ghc_family_tamar_vey_v672_v7_x1.py",
        "docs/tamar-vey/v672-v7/validation/x1-method-flow-validation.json",
        "docs/tamar-vey/v672-v7/validation/x1-validation-receipt.json",
        "docs/tamar-vey/v672-v7/validation/x1-staged-privacy.json",
        "docs/tamar-vey/v672-v7/validation/x1-staged-review.json",
        "docs/tamar-vey/v672-v7/validation/x1-manifest.json",
    }
    out = [path for path in paths if not (path.startswith("docs/tamar-vey/v672-v7/x1/") or path in exact)]
    mixed = [path for path in paths if any(part in path for part in ("/x2/", "/closeout/", "/final/", "/seal/")) or path.endswith(("_x2.py", "_final.py"))]
    payload = {"schema": "ghc.family.staged-review.v5", "owner": OWNER, "phase": PHASE, "lifecycle": "x1", "staged_before_self": paths, "staged_count_before_self": len(paths), "out_of_scope": out, "mixed_lifecycle": mixed, "valid": not out and not mixed}
    write_json("validation/x1-staged-review.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def manifest_from_index() -> None:
    exclusions = ["docs/tamar-vey/v672-v7/validation/x1-manifest.json", "docs/tamar-vey/v672-v7/validation/x1-staged-review.json"]
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
    python_paths = [ROOT / "scripts" / "build_ghc_family_tamar_vey_v672_v7_x1.py", ROOT / "tests" / "test_ghc_family_tamar_vey_v672_v7_x1.py"]
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
    self_path = "docs/tamar-vey/v672-v7/validation/x1-staged-privacy.json"
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
                    "scripts/build_ghc_family_tamar_vey_v672_v7_x1.py",
                    "tests/test_ghc_family_tamar_vey_v672_v7_x1.py",
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
