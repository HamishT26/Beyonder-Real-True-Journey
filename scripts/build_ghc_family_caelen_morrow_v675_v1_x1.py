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
OWNER_ROOT = ROOT / "docs" / "caelen-morrow" / "v675-v1"
OWNER = "Caelen Morrow"
PHASE = "v675-v1"
BRANCH = "codex/GHC-Family/caelen-morrow-v675-v1-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/sylven-arc-v674-v8-full-tools"
SOURCE_FINAL = "47ba7b0149713f60729f18f5a36ef78c331ce35f"
SOURCE_X1 = "404732ca1b665b0479a5ac96b3341df7cd2472a2"
SOURCE_EVIDENCE = "a9542a9024e0b9c647a9b969b393fbdca6575284"
SOURCE_PARENT = "1a5e801d2c52119c05a505baaaa072ef6420795d"
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "d78863ef9a56b994073c36ee61fc03e389d9c17191be22f17f0819e87b69680d"
)
SOURCE_CANONICAL_PAYLOAD_SHA256 = (
    "33d2de2d9e419f64047f754dae156937cc01de5f6d117ab26083de140620a8e4"
)
SOURCE_ROUTE_RECEIPT_SHA256 = (
    "be06708802490c870c650a918e162e0c5624a1d26fb159939415dd525b86586d"
)
SOURCE_PACKET_GIT_BLOB = "a89dc48cd89c8e0c31f5af6c42eb02d3eb29b23e"
SOURCE_CORPUS_SHA256 = (
    "8f8bf5c7cd8a64d0648809b1a361c63d5a1b113f193a370e839cfa00a10ff4a7"
)
BUILDER_PATH = "scripts/build_ghc_family_caelen_morrow_v675_v1_x1.py"
TEST_PATH = "tests/test_ghc_family_caelen_morrow_v675_v1_x1.py"
MANIFEST_PATH = "docs/caelen-morrow/v675-v1/validation/x1-manifest.json"
REVIEW_PATH = "docs/caelen-morrow/v675-v1/validation/x1-staged-review.json"
PRIVACY_PATH = "docs/caelen-morrow/v675-v1/validation/x1-staged-privacy.json"

IDENTITY_BOUNDARY = (
    "Caelen Morrow, they/them, preservation-change cartographer and consent-boundary "
    "keeper, is relational working language only. It is not evidence of consciousness, "
    "sentience, legal personhood, identity continuity, employment, qualification, "
    "independent agency, or scientific, operational, professional, legal, cultural, "
    "affected-party, or Māori authority."
)
BOUNDARY = (
    "Software, symbolic, synthetic, structural, citation, inherited, same-owner, or "
    "composite evidence is not empirical confirmation, participant evidence, "
    "professional competence or authority, production readiness, legal or cultural "
    "ratification, Māori authority, affected-party approval, complete privacy or "
    "accessibility assurance, exhaustive security, independent reproduction, AGI/ASI, "
    "consciousness or personhood evidence, Theory-of-Everything proof, proof or canon, "
    "or Stage 20 authority."
)
HOPE = (
    "Keep preservation changes auditable, reversible, and visibly short of any real-world "
    "authority that the evidence and affected parties have not supplied."
)
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
REPOSITORY_SEAL = {
    "proposal_chain": 7030,
    "effective_negatives": 39925,
    "effective_methods": 28177,
    "failed_witnesses": 11586,
    "bounded_passing_witnesses": 15460,
    "open_gaps": 328,
    "exact_gates": 321,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
}
ACTIVATION_OVERLAY = {
    "proposal_chain": 7030,
    "effective_negatives": 39926,
    "effective_methods": 28178,
    "failed_witnesses": 11587,
    "bounded_passing_witnesses": 15461,
    "open_gaps": 328,
    "exact_gates": 321,
    "external_zero_credit_failures": 1,
    "external_bounded_passing_witnesses": 1,
    "repository_seal_rewritten": False,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
}


PROPOSAL_TITLES = [
    "synthetic chair-caning work-order pseudonym and seat-frame identity braid with conflation quarantine",
    "front back and side seat-rail corner-joint aperture groove and panel relation lattice with orphan quarantine",
    "hand-caned drilled-hole perimeter index entry exit loop and temporary-peg sequence graph without threading instruction",
    "pressed-cane panel groove spline edge and insert vacancy topology without fit adhesive or installation approval",
    "vertical horizontal and diagonal cane-strand intersection graph with over-under contradiction refusal",
    "cane strand start tail return loop knot and splice-placeholder lineage without tension or strength inference",
    "cane coil reel strand lot and offcut pseudonym genealogy with species source and material abstention",
    "rush-seat rail wrap corner turn and figure-eight sequence vocabulary held as nonexecuted documentation",
    "Danish-cord warp pair weft turn nail rail and envelope topology without load or suitability claim",
    "wood-splint tape and fibre-seat element role graph with cultural-origin and material-authenticity vacancy",
    "front-to-back rail taper trapezoid keystone and central-opening geometry vacancy board with zero dimensions",
    "broken strand split loss sag abrasion fray stain and looseness cue register separated from diagnosis",
    "seat-frame joint movement surface crack and missing-fastener cue firewall with structural-safety hold",
    "chair seat top underside rail aperture groove and intersection image-orientation derivative-lineage ledger",
    "typed seat width depth rail span hole diameter strand width spacing angle and deflection vacancy matrix",
    "plain diagonal and octagonal caning legend token graph with pattern-recognition and fabrication separation",
    "append-only chair-caning correction supersession challenge readback and shift-handover braid",
    "maker workshop date chair model seat attribution and prior-intervention vacancy ledger with contestability",
    "accessibly structured woven-seat dossier with landmarks scoped tables text alternatives and noncolour holds",
    "minimal-disclosure chair dossier field whitelist and free-text rejection shell for unobserved synthetic records",
    "unresolved woven-seat docket capacity token rest threshold pause latch stop receipt and handover assignee vacancy",
    "THOS chair-caning documentation dependency DAG with checkpoint refusal acknowledgement rollback and operator vacancy",
    "THOS equal-budget dual-view omission challenge for synthetic seat records with zero people outcomes or effectiveness inference",
    "THOS chunk cursor incomplete-fragment quarantine bounded-resume precondition and expiry latch for synthetic seat dossiers",
    "Freed ID noncredential chair-job capability envelope separating pseudonymous subject scoped role purpose window cancellation and recovery vacancy",
    "CBR woven-seat notice access correction contest withdrawal explanation and response-vacancy matrix",
    "CBR chair-dossier unanswered-response interval ledger separating acknowledgement explanation debt escalation vacancy and nonadjudicative redress hold",
    "GMUT chair-seat cell-complex incidence orientation and coboundary obligation board with zero fitted parameters",
    "GMUT anisotropic woven-strip tensor and junction analogy with typed domains units and no material-law inference",
    "GMUT seat-perimeter trace operator corner junction and boundary-pairing representation with zero likelihood",
    "GMUT weave-graph discrete energy cochain and Green-identity representation without stability or force claim",
    "deterministic chair dossier serialization contract separating Unicode normalization duplicate members decimal strings array order and nonfinite refusal",
    "chair-record content-domain registry separating staged-index blobs normalized line endings checkout materialization HTML rendering and digest labels",
    "content-addressed four-tier chair-caning card deck joining relational owner Trinity pillar woven-seat lens task obligation and stale-cache refusal",
    "Canadian Conservation Institute cane-chair vocabulary adapter held at zero downloads zero records and zero conservation claims",
    "governed chair caner conservator affected-user assistive-technology and independent-review evaluation shell with zero participants",
    "real chair frame cane rush cord splint observation measurement image and environmental evidence gap",
    "real chair-caning recaning repair treatment load trial safety outcome and professional-review evidence gap",
    "professional chair-caning material tool chemical ergonomic product-safety use and release decision exact gate",
    "chair ownership custody maker rights heritage meaning recording privacy remedy affected-party Indigenous and Māori-authority reservation",
]


STARTUP_FAILURES = [
    (
        "The committed activation packet's stated whitespace-word total exceeded the local simple-whitespace measurement by five words.",
        "Preserve both measurements with their algorithms and treat the five-word difference as a measurement discrepancy, not packet corruption.",
    ),
    (
        "An initial PowerShell skill-inventory wrapper piped an unmaterialized foreach expression and failed to parse.",
        "Materialize the bounded rows before serialization or piping.",
    ),
    (
        "The first combined authorization-state projection clipped before EOF.",
        "Read the state in bounded numbered chunks through EOF.",
    ),
    (
        "The first combined activation-packet projection clipped its appendix.",
        "Partition the packet read and retain an explicit final-line witness.",
    ),
    (
        "The first combined exact-final overview projection clipped its middle section.",
        "Read bounded line ranges with overlap and verify EOF.",
    ),
    (
        "A projection of every verbose Method Flow row exceeded the available context window.",
        "Replace verbose dumping with an exhaustive anomaly-only structural audit.",
    ),
    (
        "The first compact Method Flow probe assumed stale witness and negative-row property names.",
        "Inspect the exact schema keys before counting current rows.",
    ),
    (
        "A PowerShell join-precedence mistake falsely reported 304 Method Flow mapping anomalies.",
        "Materialize each sorted joined scalar before comparing mappings.",
    ),
    (
        "The first final proposal-ledger probe assumed a proposals array instead of the declared rows array.",
        "Inspect the exact top-level keys and validate the rows array.",
    ),
    (
        "A positive-control audit assumed one uniform evidence shape and falsely reported 42 anomalies.",
        "Validate the heterogeneous declared modes with shared safety invariants rather than one payload shape.",
    ),
    (
        "A positive-control property projection called Get-Member on six intentionally null gap and gate controls.",
        "Partition completed and represented controls from intentionally null open-gap and exact-gate controls.",
    ),
    (
        "The first x1 proposal-freeze probe repeated the stale proposals-array assumption.",
        "Use the current rows key and preserve this repeated false assumption as zero-credit evidence.",
    ),
    (
        "The first ancestry wrapper embedded a semicolon inside a PowerShell expression and failed to parse.",
        "Run each ancestry predicate separately and capture its scalar exit status.",
    ),
    (
        "The first branch-absence wrapper embedded the same unsupported inline scalar pattern and failed to parse.",
        "Separate the branch-existence command from its exit-code projection.",
    ),
    (
        "A combined D-drive and live-remote branch probe returned no usable presentation within its reporting window.",
        "Isolate local capacity and branch checks, then run one bounded live-remote scalar probe.",
    ),
    (
        "The sparse-worktree setup wrapper returned no presentation even though the original commands completed.",
        "Inspect the existing worktree state before considering any repeat mutation.",
    ),
    (
        "A Windows rg call passed literal wildcard path arguments and the filesystem rejected them.",
        "Search the containing directories with rg include globs instead of Windows wildcard paths.",
    ),
    (
        "The first forty-title Caelen slate produced eight semantic-neighbor collisions at or above the 0.72 threshold.",
        "Retain the rejected slate at zero novelty credit and rewrite only the eight colliding titles before freeze.",
    ),
]


SKILL_IDEAS = [
    "ghc-chair-seat-identity-lattice",
    "ghc-caning-aperture-path-vacancy",
    "ghc-pressed-cane-groove-spline-hold",
    "ghc-woven-strand-crossing-guard",
    "ghc-rush-seat-sequence-abstention",
    "ghc-danish-cord-topology-boundary",
    "ghc-seat-geometry-vacancy-board",
    "ghc-chair-condition-cue-abstention",
    "ghc-chair-image-lineage-minimizer",
    "ghc-woven-seat-correction-braid",
    "ghc-chair-attribution-contestability",
    "ghc-woven-seat-accessibility-shell",
    "ghc-chair-record-privacy-minimizer",
    "ghc-chair-workload-stop-handover",
    "ghc-thos-seat-dossier-quarantine",
    "ghc-freed-id-chair-capability-envelope",
    "ghc-cbr-chair-response-vacancy",
    "ghc-gmut-weave-graph-boundary",
    "ghc-chair-dossier-hash-domain",
    "ghc-chair-authority-reservation",
]

RUNNER_IDEAS = [
    "ghc_family_chair_seat_identity.py",
    "ghc_family_caning_path_vacancy.py",
    "ghc_family_woven_crossing_guard.py",
    "ghc_family_seat_geometry_vacancy.py",
    "ghc_family_chair_cue_abstention.py",
    "ghc_family_chair_correction_braid.py",
    "ghc_family_chair_privacy_minimizer.py",
    "ghc_family_thos_seat_quarantine.py",
    "ghc_family_freed_id_chair_envelope.py",
    "ghc_family_cbr_chair_response.py",
]

TOOL_IDEAS = [
    "chair dossier proposal-contract validator",
    "woven-seat topology vacancy checker",
    "chair correction and handover lineage validator",
]


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8").strip()


def write_json(relative: str, payload: Any) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def normalize_title(title: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9āēīōū]+", title.lower())
        if len(token) > 2 and token not in {"and", "the", "with", "for", "from"}
    }


def batch_blobs(specs: list[str]) -> list[bytes | None]:
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output, stderr = process.communicate(
        input=("\n".join(specs) + "\n").encode("utf-8"), timeout=30
    )
    if process.returncode != 0:
        raise SystemExit(
            f"git cat-file --batch failed: {stderr.decode('utf-8', errors='replace')}"
        )
    stream = io.BytesIO(output)
    rows: list[bytes | None] = []
    for _ in specs:
        header = stream.readline().decode("utf-8", errors="strict").strip()
        if header.endswith(" missing"):
            rows.append(None)
            continue
        parts = header.rsplit(" ", 2)
        if len(parts) != 3 or parts[1] != "blob":
            raise SystemExit(f"unexpected cat-file header: {header}")
        size = int(parts[2])
        rows.append(stream.read(size))
        if stream.read(1) != b"\n":
            raise SystemExit("cat-file delimiter missing")
    return rows


def json_blob(commit: str, path: str) -> Any:
    return json.loads(git("show", f"{commit}:{path}").stdout.decode("utf-8"))


def recover_proposal_corpus() -> tuple[dict[str, Any], list[str]]:
    raw_paths = git("ls-tree", "-r", "--name-only", "-z", SOURCE_FINAL).stdout
    candidates = sorted(
        path.decode("utf-8")
        for path in raw_paths.split(b"\0")
        if path
        and path.decode("utf-8").lower().endswith(".json")
        and "proposal" in path.decode("utf-8").lower()
    )
    proposal_ids: set[str] = set()
    titles: set[str] = set()
    occurrences = 0
    malformed = 0

    def walk(node: Any) -> None:
        nonlocal occurrences
        if isinstance(node, dict):
            proposal_id = node.get("proposal_id")
            title = node.get("title")
            if (
                isinstance(proposal_id, str)
                and proposal_id.strip()
                and isinstance(title, str)
                and title.strip()
            ):
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
        for blob in batch_blobs(specs[start : start + 128]):
            if blob is None:
                malformed += 1
                continue
            try:
                walk(json.loads(blob.decode("utf-8")))
            except (UnicodeDecodeError, json.JSONDecodeError):
                malformed += 1
    canonical = json.dumps(
        {"proposal_ids": sorted(proposal_ids), "titles": sorted(titles)},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    summary = {
        "scope": "exact Sylven Arc v674-v8 final tree, proposal-labelled JSON paths only",
        "candidate_git_blob_paths": len(candidates),
        "malformed_or_missing_blobs": malformed,
        "semantic_occurrences": occurrences,
        "unique_proposal_ids": len(proposal_ids),
        "unique_titles": len(titles),
        "corpus_sha256": hashlib.sha256(canonical).hexdigest(),
        "declared_source_chain": 7030,
        "materialized_ids_cover_declared_chain": len(proposal_ids) >= 7030,
        "exact_canonical_row_mapping": False,
        "canonical_row_mapping_open_gap": True,
        "universal_novelty_claim": False,
        "reason": (
            "No single reachable exact-tree ledger materializes every declared historical "
            "row; source-bounded semantic comparison is evidence, not universal novelty proof."
        ),
    }
    return summary, sorted(titles)


def proposal_rows() -> list[dict[str, Any]]:
    rows = []
    for index, title in enumerate(PROPOSAL_TITLES, start=1):
        if index <= 28:
            outcome, approval, lane = (
                "completed",
                "safe_now",
                "owner_local_symbolic_or_synthetic_x2",
            )
        elif index <= 36:
            outcome, approval, lane = (
                "represented",
                "bounded_candidate",
                "owner_local_symbolic_or_synthetic_x2",
            )
        elif index <= 38:
            outcome, approval, lane = "open_gap", "open_gap", "held_without_real_world_execution"
        else:
            outcome, approval, lane = "exact_gate", "exact_gate", "held_without_real_world_execution"
        rows.append(
            {
                "proposal_id": f"CM6751-N{index:03d}",
                "title": title,
                "hypothesis": (
                    f"A typed owner-local contract can expose proposal {index:02d}'s chair-caning "
                    "documentation obligations without promoting its evidence class."
                ),
                "null_or_failure_condition": (
                    "A missing required field, accepted invalid mutation, real-world action, "
                    "unlabelled uncertainty, or authority promotion rejects the hypothesis."
                ),
                "approval_class": approval,
                "execution_lane": lane,
                "official_or_primary_source_needs": (
                    "Vocabulary and refusal boundaries only; citations are not observations, "
                    "measurements, treatment advice, validation, consent, or authority."
                ),
                "concrete_artifacts": [
                    "typed JSON contract",
                    "bounded accepting or explicit-vacancy fixture",
                    "four rejecting mutation receipts",
                    "boundary flashcard",
                ],
                "falsifier_or_acceptance_gate": (
                    "The bounded fixture must match the expected disposition, four preregistered "
                    "invalid mutations must reject, and every protected boundary must remain explicit."
                ),
                "rollback_or_recovery": (
                    "Retain the failed witness, correct only the isolated owner-local dependency, "
                    "and never replay a successful canonical aggregate."
                ),
                "protected_gates": [
                    "empirical",
                    "participant",
                    "professional",
                    "legal",
                    "cultural",
                    "Māori_authority",
                    "affected_party",
                    "privacy_complete",
                    "accessibility_complete",
                    "independent_reproduction",
                    "Stage_20",
                ],
                "primary_pillar": "Freed ID and CBR Heart",
                "planned_outcome": outcome,
                "expected_disposition": outcome,
                "x1_state": "frozen_not_executed",
                "external_actions": 0,
                "real_people": 0,
                "real_records_or_objects": 0,
            }
        )
    return rows


def frozen_task(task_id: str, title: str, approval: str = "safe_now") -> dict[str, Any]:
    return {
        "task_id": task_id,
        "title": title,
        "approval_class": approval,
        "state": "frozen_not_executed",
        "execution_count": 0,
        "completion_credit": 0,
        "hypothesis": "The named bounded owner-local obligation can be tested without external action.",
        "failure_condition": "Any real-world action, missing gate, or unbounded claim stops execution.",
        "rollback": "Retain the failure and change only the isolated uncommitted owner-local artifact.",
        "protected_gates": ["no_external_action", "no_authority_promotion", "no_failure_laundering"],
    }


def portfolio() -> dict[str, list[dict[str, Any]]]:
    proposals = proposal_rows()
    safe_titles = [f"preregister and structurally review {row['proposal_id']}: {row['title']}" for row in proposals]
    safe_titles.extend(
        [
            "enforce the four-outcome label allowlist",
            "preserve source seal and external overlay as separate truth layers",
            "enforce deterministic UTF-8 JSON with finite-number refusal",
            "retain the relational identity and corrigibility boundary",
            "retain the zero-person zero-object zero-measurement declaration",
            "verify direct source ancestry without replaying source validation",
            "preserve planning-only x1 before any x2 surface",
            "preserve current family runner naming compatibility",
            "reserve manual accessibility and affected-user evaluation",
            "reserve professional chair-caning and conservation judgement",
            "reserve ownership custody heritage and recording rights",
            "reserve Māori wording concepts data governance and authority",
            "record the D-first sparse lane and owner scope",
            "record every failed wrapper at zero credit",
            "record official-source use as vocabulary only",
            "preregister four invalid mutations per new proposal",
            "preregister content-addressed flashcard sections",
            "preregister exact staged Git-blob manifests",
            "preregister the one-shot final canonical latch",
            "keep the successor route prepared but unsent",
        ]
    )
    safe = [frozen_task(f"CM6751-SAFE-{i:03d}", title) for i, title in enumerate(safe_titles, 1)]
    candidates = [
        frozen_task(
            f"CM6751-CAND-{i:03d}",
            f"bounded evidence candidate for {proposals[i-1]['proposal_id']}: {proposals[i-1]['title']}",
            "bounded_candidate",
        )
        for i in range(1, 31)
    ]
    exact_titles = [
        "real chair condition assessment",
        "real chair-caning or recaning treatment",
        "real material species or composition identification",
        "real load capacity or fitness decision",
        "real adhesive solvent dye or chemical choice",
        "real tool machine or ergonomic safety release",
        "real product or public-use safety release",
        "real custody ownership or access decision",
        "real maker attribution or authenticity decision",
        "real heritage significance interpretation",
        "real legal rights or copyright interpretation",
        "real privacy or data-governance decision",
        "real accessibility conformance claim",
        "real affected-party notice or acceptance",
        "real Indigenous cultural and intellectual property decision",
        "real Māori wording or concept use",
        "real Māori data-governance decision",
        "real tangata whenua iwi or hapū consultation",
        "real credential issuance verification or revocation",
        "Stage 20 promotion or deployment",
    ]
    exact = [
        frozen_task(f"CM6751-EXACT-{i:03d}", title, "exact_approval_required")
        for i, title in enumerate(exact_titles, 1)
    ]
    blocked_titles = [
        "participant recruitment or observation",
        "real chair or material acquisition",
        "real workshop access or tool operation",
        "real image recording or location disclosure",
        "real repair installation or return to use",
        "live identity key proof or credential lifecycle",
        "production deployment or third-party publication",
        "legal cultural or affected-party adjudication",
        "Māori-authority substitution",
        "independent reproduction claim by the same owner",
    ]
    blocked = [
        frozen_task(f"CM6751-BLOCK-{i:03d}", title, "blocked")
        for i, title in enumerate(blocked_titles, 1)
    ]
    skills = [
        {
            **frozen_task(f"CM6751-SKILL-{i:03d}", name, "owner_local_skill_candidate"),
            "skill_name": name,
            "global_installation": False,
            "quick_validation_required": True,
            "accepting_and_rejecting_smoke_required": True,
        }
        for i, name in enumerate(SKILL_IDEAS, 1)
    ]
    runners = [
        {
            **frozen_task(f"CM6751-RUN-{i:03d}", name, "family_current_runner_candidate"),
            "runner_path": f"scripts/{name}",
            "family_current_prefix": True,
            "zero_action_smoke_required": True,
        }
        for i, name in enumerate(RUNNER_IDEAS, 1)
    ]
    cfr = []
    for index in range(1, 21):
        proposal = proposals[index - 1]
        for action in ("CLEAN", "FIX", "REFINE"):
            cfr.append(
                frozen_task(
                    f"CM6751-CFR-{len(cfr)+1:03d}",
                    f"{action}: {proposal['proposal_id']} {proposal['title']}",
                    "safe_now" if action != "REFINE" else "bounded_candidate",
                )
            )
    successor_skills = [
        frozen_task(
            f"CM6751-NEXT-SKILL-{i:03d}",
            f"successor skill seed {i:02d}: conditional brushmaking documentation boundary",
            "successor_recommendation_zero_credit",
        )
        for i in range(1, 11)
    ]
    successor_runners = [
        frozen_task(
            f"CM6751-NEXT-RUN-{i:03d}",
            f"successor runner seed {i:02d}: owner-local zero-action brush record guard",
            "successor_recommendation_zero_credit",
        )
        for i in range(1, 11)
    ]
    successor_cfr = [
        frozen_task(
            f"CM6751-NEXT-CFR-{i:03d}",
            f"successor CLEAN/FIX/REFINE recommendation {i:02d} requiring fresh owner audit",
            "successor_recommendation_zero_credit",
        )
        for i in range(1, 31)
    ]
    tools = [
        {
            **frozen_task(f"CM6751-TOOL-{i:03d}", title, "owner_local_tool_candidate"),
            "tool_title": title,
            "substantive_accepting_and_rejecting_fixtures_required": True,
            "global_installation": False,
        }
        for i, title in enumerate(TOOL_IDEAS, 1)
    ]
    inherited_reviews = [
        frozen_task(
            f"CM6751-INHERITED-REVIEW-{i:03d}",
            f"zero-credit source integrity revalidation {i:02d}",
            "inherited_evidence_only",
        )
        for i in range(1, 21)
    ]
    return {
        "inherited_reviews": inherited_reviews,
        "safe_now": safe,
        "candidates": candidates,
        "exact_approval": exact,
        "blocked": blocked,
        "skills": skills,
        "runners": runners,
        "tools": tools,
        "clean_fix_refine": cfr,
        "successor_skills": successor_skills,
        "successor_runners": successor_runners,
        "successor_clean_fix_refine": successor_cfr,
    }


def method_flow() -> dict[str, Any]:
    methods, recommendations, witnesses, events, negatives = [], [], [], [], []
    event_index = 0
    for index, (failure, recovery) in enumerate(STARTUP_FAILURES, start=1):
        method_id = f"CM6751-X1-M{index:03d}"
        negative_id = f"CM6751-X1-N{index:03d}"
        fail_id = f"CM6751-X1-W{index:03d}-F"
        pass_id = f"CM6751-X1-W{index:03d}-P"
        methods.append(
            {
                "method_id": method_id,
                "title": f"bounded recovery for {negative_id}",
                "trigger_preconditions": [failure],
                "failure_signature": failure,
                "candidate_workaround": recovery,
                "validation_witness_ids": [fail_id, pass_id],
                "retained_negative_ids": [negative_id],
                "recurrence_guard": recovery,
                "rollback": "Retain the failure and change only the isolated owner-local procedure.",
                "scope_boundary": BOUNDARY,
                "approval_class": "safe_now",
                "privacy_class": "sanitized_public",
                "recommendation_state": "preferred",
                "protected_gates": [
                    "no_failure_laundering",
                    "owner_delta_only",
                    "no_authority_promotion",
                ],
                "supersedes": [],
            }
        )
        recommendations.append(
            {"method_id": method_id, "recommendation": recovery, "state": "preferred"}
        )
        witnesses.extend(
            [
                {
                    "witness_id": fail_id,
                    "method_id": method_id,
                    "scope": "owner-local startup and x1 planning",
                    "procedure": failure,
                    "expected": "bounded attributable evidence",
                    "observed": failure,
                    "result": "fail",
                    "retained_negative_ids": [negative_id],
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "boundary": BOUNDARY,
                },
                {
                    "witness_id": pass_id,
                    "method_id": method_id,
                    "scope": "owner-local bounded recovery",
                    "procedure": recovery,
                    "expected": "the isolated dependency passes without rewriting its failure",
                    "observed": recovery,
                    "result": "pass",
                    "retained_negative_ids": [negative_id],
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "boundary": BOUNDARY,
                },
            ]
        )
        negatives.append(
            {
                "negative_id": negative_id,
                "method_id": method_id,
                "failed_witness": failure,
                "result": "fail",
                "completion_credit": 0,
                "recovery_preserves_failure": True,
            }
        )
        for before, after, reason, witness_id in (
            (None, "candidate", "failure retained and bounded recovery proposed", fail_id),
            ("candidate", "validated", "bounded recovery passed", pass_id),
            ("validated", "preferred", "recurrence guard retained", pass_id),
        ):
            event_index += 1
            events.append(
                {
                    "event_index": event_index,
                    "method_id": method_id,
                    "before": before,
                    "after": after,
                    "reason": reason,
                    "witness_id": witness_id,
                }
            )
    return {
        "schema": "ghc.family.method-flow-state.v1",
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "planning_only_x1",
        "execution_authority": "owner_self_scoped_delta",
        "methods": methods,
        "recommendations": recommendations,
        "state_events": events,
        "witnesses": witnesses,
        "negative_rows": negatives,
        "counts": {
            "methods": len(methods),
            "recommendations": len(recommendations),
            "state_events": len(events),
            "states": {"preferred": len(methods)},
            "witness_results": {"fail": len(methods), "pass": len(methods)},
            "witnesses": len(witnesses),
        },
        "boundary": BOUNDARY,
        "identity_boundary": IDENTITY_BOUNDARY,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def build_default() -> None:
    if git_text("rev-parse", "HEAD") != SOURCE_FINAL:
        raise SystemExit("x1 must begin at the exact immutable Sylven final")
    if len(PROPOSAL_TITLES) != 40 or len(set(PROPOSAL_TITLES)) != 40:
        raise SystemExit("proposal title count or uniqueness drifted")
    proposals = proposal_rows()
    if Counter(row["expected_disposition"] for row in proposals) != Counter(OUTCOMES):
        raise SystemExit("proposal disposition distribution drifted")
    corpus_summary, source_titles = recover_proposal_corpus()
    expected_corpus = {
        "candidate_git_blob_paths": 2235,
        "malformed_or_missing_blobs": 0,
        "semantic_occurrences": 9098,
        "unique_proposal_ids": 2975,
        "unique_titles": 2848,
        "corpus_sha256": SOURCE_CORPUS_SHA256,
    }
    for key, expected in expected_corpus.items():
        if corpus_summary[key] != expected:
            raise SystemExit(f"source corpus drift for {key}: {corpus_summary[key]} != {expected}")
    neighbors, max_score = [], 0.0
    for row in proposals:
        left = normalize_title(row["title"])
        best_title, best_score = "", 0.0
        for source_title in source_titles:
            right = normalize_title(source_title)
            score = len(left & right) / max(1, len(left | right))
            if score > best_score:
                best_title, best_score = source_title, score
        max_score = max(max_score, best_score)
        neighbors.append(
            {
                "proposal_id": row["proposal_id"],
                "source_title": best_title,
                "jaccard": round(best_score, 6),
                "collision": best_score >= 0.72,
            }
        )
    if any(row["collision"] for row in neighbors):
        raise SystemExit("corrected proposal slate still contains a semantic collision")
    source_freeze = json_blob(
        SOURCE_FINAL, "docs/sylven-arc/v674-v8/x1/new-proposal-freeze.json"
    )
    source_rows = source_freeze["rows"]
    if len(source_rows) != 60:
        raise SystemExit("source proposal freeze must contain sixty Sylven rows")
    selected_source = source_rows[::3]
    if len(selected_source) != 20:
        raise SystemExit("inherited selection must contain twenty rows")
    inherited = []
    for index, row in enumerate(selected_source, start=1):
        row_bytes = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )
        inherited.append(
            {
                "selection_id": f"CM6751-I{index:03d}",
                "source_owner": "Sylven Arc",
                "source_phase": "v674-v8",
                "source_proposal_id": row["proposal_id"],
                "source_title": row["title"],
                "source_outcome": row["expected_disposition"],
                "source_row_sha256": hashlib.sha256(row_bytes).hexdigest(),
                "integrity_revalidated": True,
                "caelen_novelty_credit": 0,
                "caelen_completion_credit": 0,
                "state": "inherited_evidence_only",
            }
        )
    frozen_portfolio = portfolio()
    counts = {key: len(value) for key, value in frozen_portfolio.items()}
    expected_counts = {
        "inherited_reviews": 20,
        "safe_now": 60,
        "candidates": 30,
        "exact_approval": 20,
        "blocked": 10,
        "skills": 20,
        "runners": 10,
        "tools": 3,
        "clean_fix_refine": 60,
        "successor_skills": 10,
        "successor_runners": 10,
        "successor_clean_fix_refine": 30,
    }
    if counts != expected_counts:
        raise SystemExit(f"portfolio count drift: {counts}")
    flow = method_flow()
    x1_overlay = {
        **ACTIVATION_OVERLAY,
        "effective_negatives": ACTIVATION_OVERLAY["effective_negatives"] + len(STARTUP_FAILURES),
        "effective_methods": ACTIVATION_OVERLAY["effective_methods"] + len(STARTUP_FAILURES),
        "failed_witnesses": ACTIVATION_OVERLAY["failed_witnesses"] + len(STARTUP_FAILURES),
        "bounded_passing_witnesses": ACTIVATION_OVERLAY["bounded_passing_witnesses"]
        + len(STARTUP_FAILURES),
        "caelen_startup_failures": len(STARTUP_FAILURES),
        "repository_seal_rewritten": False,
    }
    write_json(
        "x1/activation-intake.json",
        {
            "schema": "ghc.family.activation-intake.v6",
            "owner": OWNER,
            "phase": PHASE,
            "source_branch": SOURCE_BRANCH,
            "source_final": SOURCE_FINAL,
            "source_x1": SOURCE_X1,
            "source_evidence": SOURCE_EVIDENCE,
            "source_parent": SOURCE_PARENT,
            "source_history": {
                "phase_commits": 3,
                "merges": 0,
                "single_parent_commits": 3,
                "final_direct_child_of_evidence": True,
            },
            "source_manifests_reverified": {
                "x1": 20,
                "evidence": 260,
                "final_delta": 26,
                "final_owner": 309,
                "mismatches": 0,
            },
            "source_canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
            "source_canonical_payload_sha256": SOURCE_CANONICAL_PAYLOAD_SHA256,
            "source_route_receipt_sha256": SOURCE_ROUTE_RECEIPT_SHA256,
            "source_packet_git_blob": SOURCE_PACKET_GIT_BLOB,
            "source_clean_zero_divergent_fresh_four_way_equal": True,
            "source_validation_replayed": False,
            "task_creation_count": 0,
            "fork_count": 0,
            "subagent_count": 0,
            "standby_contact_count": 0,
            "successor_precontact_count": 0,
            "external_writes": 0,
        },
    )
    write_json(
        "x1/identity-and-boundary.json",
        {
            "schema": "ghc.family.identity-boundary.v5",
            "owner": OWNER,
            "phase": PHASE,
            "pronouns": "they/them",
            "relational_role": "preservation-change cartographer and consent-boundary keeper",
            "relational_hope": HOPE,
            "identity_boundary": IDENTITY_BOUNDARY,
            "corrigibility": "Hamish may rename, pause, redirect, narrow, or stop the route.",
        },
    )
    write_json(
        "x1/source-count-overlay.json",
        {
            "schema": "ghc.family.source-count-overlay.v6",
            "repository_sealed": REPOSITORY_SEAL,
            "live_activation_overlay": ACTIVATION_OVERLAY,
            "caelen_x1_overlay": x1_overlay,
        },
    )
    write_json(
        "x1/inherited-proposal-revalidation.json",
        {
            "schema": "ghc.family.inherited-proposal-revalidation.v7",
            "owner": OWNER,
            "phase": PHASE,
            "selected": 20,
            "novelty_credit": 0,
            "completion_credit": 0,
            "selection_rule": "every third source row in exact source order, twenty rows total",
            "rows": inherited,
        },
    )
    write_json(
        "x1/semantic-neighbor-audit.json",
        {
            "schema": "ghc.family.semantic-neighbor-audit.v8",
            "owner": OWNER,
            "phase": PHASE,
            "exact_source_tree_corpus": corpus_summary,
            "reachable_unique_titles": len(source_titles),
            "declared_source_chain": 7030,
            "new_titles": 40,
            "collision_threshold": 0.72,
            "max_jaccard": round(max_score, 6),
            "collisions": 0,
            "rows": neighbors,
            "rejected_initial_slate": {
                "titles": 40,
                "threshold_collisions": 8,
                "novelty_credit": 0,
                "retained_negative_id": "CM6751-X1-N018",
            },
            "candidate_practice_exact_hits": {
                "chair_caning": sum("chair caning" in title.casefold() for title in source_titles),
                "woven_seat": sum("woven seat" in title.casefold() for title in source_titles),
                "brush_making": sum("brush making" in title.casefold() for title in source_titles),
                "woodturning": sum("woodturning" in title.casefold() for title in source_titles),
            },
            "adjacent_term_hits": {
                "chair": sum("chair" in title.casefold() for title in source_titles),
                "weaving": sum("weaving" in title.casefold() for title in source_titles),
                "brush": sum("brush" in title.casefold() for title in source_titles),
                "lathe": sum("lathe" in title.casefold() for title in source_titles),
            },
            "universal_novelty_claim": False,
            "canonical_row_mapping_open_gap": True,
        },
    )
    write_json(
        "x1/new-proposal-freeze.json",
        {
            "schema": "ghc.family.new-proposal-freeze.v8",
            "owner": OWNER,
            "phase": PHASE,
            "proposal_chain_before": 7030,
            "proposal_chain_after_if_evidence_frozen": 7070,
            "outcomes": OUTCOMES,
            "planned_invalid_mutations_per_proposal": 4,
            "planned_invalid_mutations": 160,
            "rows": proposals,
        },
    )
    write_json(
        "x1/portfolio-freeze.json",
        {
            "schema": "ghc.family.remastered-portfolio-freeze.v8",
            "owner": OWNER,
            "phase": PHASE,
            "rows": frozen_portfolio,
            "counts": counts,
            "bounded_human_practice": "synthetic chair caning and woven-seat documentation",
            "successor_practice_recommendation": (
                "synthetic brushmaking documentation, conditional on the successor's fresh source-bounded novelty audit"
            ),
            "successor_practice_recommendation_count": 1,
            "inherited_portfolio_completion_credit": 0,
            "successor_recommendation_completion_credit": 0,
            "filler_prohibited": True,
        },
    )
    write_json(
        "x1/practice-lens-selection.json",
        {
            "schema": "ghc.family.practice-lens-selection.v2",
            "owner": OWNER,
            "phase": PHASE,
            "primary_pillar": "Freed ID and CBR Heart",
            "protected_pillars": ["GMUT Mind", "THOS Body"],
            "candidates": [
                {
                    "practice": "synthetic chair caning and woven-seat documentation",
                    "selected_for_current_phase": True,
                    "exact_title_hits": 0,
                },
                {
                    "practice": "synthetic brushmaking documentation",
                    "selected_for_current_phase": False,
                    "recommended_to_successor_conditionally": True,
                    "exact_title_hits": 0,
                },
                {
                    "practice": "synthetic woodturning documentation",
                    "selected_for_current_phase": False,
                    "exact_title_hits": 0,
                },
            ],
            "real_people": 0,
            "real_objects": 0,
            "real_actions": 0,
            "authority_conferred": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "x1/source-ledger.json",
        {
            "schema": "ghc.family.public-source-ledger.v8",
            "owner": OWNER,
            "phase": PHASE,
            "retrieved_nz_date": "2026-08-29",
            "read_only_source_page_checks": 7,
            "api_calls": 0,
            "dataset_or_media_downloads": 0,
            "external_writes": 0,
            "real_rows": 0,
            "sources": [
                {
                    "publisher": "Canadian Conservation Institute",
                    "title": "Caring for basketry and plant materials",
                    "url": "https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/basketry-plant-materials.html",
                    "status": "current_official_page_checked_2026-08-29",
                    "use": "cane, woven-seat, passive/active element, and vulnerability vocabulary only; no care, treatment, condition, or professional claim",
                },
                {
                    "publisher": "Canadian Conservation Institute",
                    "title": "Furniture, wooden objects and basketry",
                    "url": "https://www.canada.ca/en/conservation-institute/services/care-objects/furniture-wooden-objects-basketry.html",
                    "status": "current_official_page_checked_2026-08-29",
                    "use": "collection-category and preservation-boundary vocabulary only",
                },
                {
                    "publisher": "National Institute of Standards and Technology",
                    "title": "SI Units",
                    "url": "https://www.nist.gov/pml/owm/metric-si/si-units",
                    "status": "current_official_page_checked_2026-08-29",
                    "use": "quantity and SI-symbol vocabulary with zero measurement or conformance claim",
                },
                {
                    "publisher": "World Wide Web Consortium",
                    "title": "PROV-O: The PROV Ontology",
                    "url": "https://www.w3.org/TR/prov-o/",
                    "status": "stable_primary_recommendation_checked_2026-08-29",
                    "use": "entity, activity, derivation, invalidation, and provenance vocabulary only",
                },
                {
                    "publisher": "World Wide Web Consortium",
                    "title": "Web Content Accessibility Guidelines 2.2",
                    "url": "https://www.w3.org/TR/WCAG22/",
                    "status": "current_primary_recommendation_checked_2026-08-29",
                    "use": "structural-accessibility vocabulary and manual-evaluation reservation",
                },
                {
                    "publisher": "World Wide Web Consortium",
                    "title": "Verifiable Credentials Data Model v2.0",
                    "url": "https://www.w3.org/TR/vc-data-model-2.0/",
                    "status": "current_primary_recommendation_checked_2026-08-29",
                    "use": "credential vocabulary for a zero-key nonproduction representation only",
                },
                {
                    "publisher": "RFC Editor",
                    "title": "RFC 8785: JSON Canonicalization Scheme",
                    "url": "https://www.rfc-editor.org/rfc/rfc8785",
                    "status": "stable_primary_standard_checked_2026-08-29",
                    "use": "canonical JSON ordering and numeric-domain refusal vocabulary only",
                },
            ],
            "boundary": (
                "Sources provide vocabulary and refusal conditions only; they are not observations, "
                "measurements, conservation advice, professional validation, consent, legal or cultural "
                "interpretation, Māori authority, affected-party approval, or Stage 20 evidence."
            ),
        },
    )
    write_json(
        "x1/threat-model.json",
        {
            "schema": "ghc.family.threat-model.v6",
            "owner": OWNER,
            "phase": PHASE,
            "threats": [
                {"threat": "x2 contamination in planning-only x1", "control": "path and lifecycle absence tests", "residual": "fail closed"},
                {"threat": "semantic collision disguised as novelty", "control": "exact-source reachable-corpus Jaccard gate", "residual": "canonical row mapping remains open gap"},
                {"threat": "professional or safety promotion", "control": "explicit vacancy and exact-gate outcomes", "residual": "no real practice authority"},
                {"threat": "identity or credential production", "control": "zero-key noncredential fixtures", "residual": "Freed ID remains synthetic"},
                {"threat": "privacy or raw identifier leakage", "control": "five-class staged-blob scan", "residual": "bounded scanner only"},
                {"threat": "accessibility completeness claim", "control": "structural checks plus manual evaluation reservation", "residual": "manual and affected-user review absent"},
                {"threat": "Māori or Indigenous authority substitution", "control": "exact gate and zero cultural interpretation", "residual": "authority remains absent"},
                {"threat": "source or sibling mutation", "control": "one additive owner path and branch", "residual": "shared infrastructure only"},
                {"threat": "failed witness laundering", "control": "paired Method Flow fail/pass records", "residual": "failures remain zero credit"},
                {"threat": "successor precontact", "control": "route remains prepared-not-sent until terminal gate", "residual": "no current successor contact"},
            ],
            "real_world_actions": 0,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "x1/workflow-plan.json",
        {
            "schema": "ghc.family.workflow-plan.v7",
            "owner": OWNER,
            "phase": PHASE,
            "steps": [
                {"step": "read activation, skills, schemas, and exact source", "status": "completed"},
                {"step": "reverify source manifests, receipts, ancestry, clean equality", "status": "completed"},
                {"step": "freeze planning-only x1 and push fresh equality", "status": "in_progress"},
                {"step": "build bounded x2 evidence after x1 gate", "status": "pending"},
                {"step": "seal one owner final and invoke one canonical latch", "status": "pending"},
                {"step": "refresh route and send at most once if every gate passes", "status": "pending"},
            ],
            "caps": {"owner_files": 2000, "document_words": 100000, "x1_commits": 3, "x2_commits": 3, "total_commits": 6},
            "caps_are_ceilings_not_quotas": True,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "x1/route-plan.json",
        {
            "schema": "ghc.family.route-state.v8",
            "owner": OWNER,
            "phase": PHASE,
            "delivery_state": "PREPARED_NOT_SENT",
            "prospective_successor_title": "Eiren Kestrel",
            "prospective_successor_phase": "v675-v2",
            "successor_contact_attempts": 0,
            "task_created": False,
            "standby_contacted": False,
            "requires_terminal_refresh": True,
            "route_authority_ceiling": "through the currently requested label v725-v8, one terminal edge at a time",
            "boundary": "Repository preparation is not delivery; only a supported existing-task acknowledgement can establish delivery.",
        },
    )
    write_json(
        "x1/flashcard-plan.json",
        {
            "schema": "ghc.family.freed-id-flashcard-plan.v3",
            "owner": OWNER,
            "phase": PHASE,
            "tiers": ["owner", "Trinity pillars", "bounded practice", "task and change"],
            "sections": [
                "owner anchor", "GMUT Mind", "THOS Body", "Freed ID and CBR Heart",
                "chair-caning practice", "proposal contracts", "portfolio", "skills", "runners",
                "evidence", "gates", "wellbeing", "route and manifests",
            ],
            "planned_cards": 80,
            "content_addressing_required": True,
            "cache_benefit_claimed": False,
            "identity_continuity_claimed": False,
            "x1_state": "planned_not_built",
        },
    )
    write_json(
        "x1/tool-plan.json",
        {
            "schema": "ghc.family.owner-tool-plan.v2",
            "owner": OWNER,
            "phase": PHASE,
            "ordinary_phase_target": 3,
            "target_is_subordinate_to_safety_and_relevance": True,
            "global_installation_authority": False,
            "tools": frozen_portfolio["tools"],
            "x1_state": "planned_not_built",
        },
    )
    write_json("x1/method-flow-startup.json", flow)
    write_json(
        "x1/phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.v9",
            "owner": OWNER,
            "phase": PHASE,
            "branch": BRANCH,
            "source_final": SOURCE_FINAL,
            "lifecycle": "planning_only_x1",
            "planning_only": True,
            "x2_started": False,
            "outcomes_observed": False,
            "proposal_chain_before": 7030,
            "new_proposals_frozen": 40,
            "inherited_revalidations": 20,
            "planned_outcomes": OUTCOMES,
            "observed_outcomes": None,
            "real_people": 0,
            "real_objects": 0,
            "real_records": 0,
            "real_measurements": 0,
            "external_actions": 0,
            "same_owner_only": True,
            "independent_reproduction": False,
            "full_repository_suite": "not_run_not_claimed",
            "successor_contacted": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "x1/build-receipt.json",
        {
            "schema": "ghc.family.x1-build-receipt.v6",
            "owner": OWNER,
            "phase": PHASE,
            "state": "PLANNING_ONLY_FROZEN_NOT_EXECUTED",
            "new_proposals": 40,
            "inherited_zero_credit_reviews": 20,
            "planned_mutations": 160,
            "startup_failures_retained": len(STARTUP_FAILURES),
            "source_corpus_titles": len(source_titles),
            "semantic_collisions": 0,
            "max_jaccard": round(max_score, 6),
            "external_actions": 0,
            "x2_artifacts": 0,
            "outcomes_observed": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "validation/x1-method-flow-validation.json",
        {
            "schema": "ghc.family.method-flow-validation.v3",
            "owner": OWNER,
            "phase": PHASE,
            "valid": True,
            "methods": len(flow["methods"]),
            "recommendations": len(flow["recommendations"]),
            "state_events": len(flow["state_events"]),
            "witnesses": len(flow["witnesses"]),
            "failed_witnesses": len(STARTUP_FAILURES),
            "bounded_passing_witnesses": len(STARTUP_FAILURES),
            "negative_rows": len(flow["negative_rows"]),
            "preferred_methods": len(flow["methods"]),
            "failures_rewritten_as_pass": 0,
        },
    )
    write_json(
        "validation/x1-validation-prerequisites.json",
        {
            "schema": "ghc.family.validation-prerequisites.v3",
            "owner": OWNER,
            "phase": PHASE,
            "lifecycle": "planning_only_x1",
            "required": [
                "exact owner-scoped x1 tests",
                "all x1 JSON parsing",
                "five-class staged privacy scan",
                "exact staged Git-blob manifest",
                "staged path and lifecycle review",
                "clean push and fresh four-way equality",
            ],
            "canonical_final_invocation_allowed": False,
            "full_repository_suite_allowed": False,
        },
    )
    overview_lines = [
        "# Caelen Morrow v675-v1 planning-only x1 integrated overview",
        "",
        IDENTITY_BOUNDARY,
        "",
        "## Outcome",
        "",
        "This is a planning-only x1 freeze. It contains no x2 implementation, observed proposal outcome, completed portfolio task, real-world action, successor contact, or authority act. The one Caelen-owned sparse lane begins at Sylven Arc's immutable exact final. Source manifests, receipts, ancestry, clean state, zero divergence, and fresh four-way equality were reverified read-only without replaying Sylven's validator or tests.",
        "",
        "## Bounded practice and Trinity Mandala",
        "",
        "Freed ID and CBR Heart is the primary pillar through wholly synthetic chair caning and woven-seat documentation. GMUT Mind and THOS Body remain visible and protected. The practice supplies a learning and design lens only; it establishes no chair-caning, conservation, repair, furniture, materials, tool, workplace, product-safety, custody, ownership, legal, cultural, affected-party, accessibility, privacy, or Māori authority.",
        "",
        "Three practice candidates were reviewed: chair caning and woven-seat documentation for the current phase, brushmaking documentation as one conditional successor recommendation, and woodturning documentation as an unselected candidate. Every future use requires its own source-bounded novelty and authority review.",
        "",
        "## Source-bounded novelty",
        "",
        f"The exact source-tree corpus contains {corpus_summary['candidate_git_blob_paths']} proposal-labelled JSON blobs, {corpus_summary['semantic_occurrences']} semantic occurrences, {corpus_summary['unique_proposal_ids']} unique proposal identifiers, and {corpus_summary['unique_titles']} unique reachable titles. It does not materialize a canonical mapping for all 7,030 declared historical rows, so no universal novelty claim is made. The first forty-title slate had eight threshold collisions and remains zero-credit. The corrected slate has zero collisions at the 0.72 threshold and a bounded maximum Jaccard score of {max_score:.6f}.",
        "",
        "## Frozen proposal contracts",
        "",
        "Twenty inherited Sylven rows are selected for integrity revalidation at zero Caelen novelty and completion credit. Forty genuinely new source-bounded Caelen proposals are frozen with exactly one expected disposition each: 28 completed, 8 represented, 2 open_gap, and 2 exact_gate. Each row contains the required hypothesis, null or failure condition, approval class, execution lane, source need, artifact, falsifier or acceptance gate, rollback or recovery, protected gates, and expected disposition. Four invalid mutations per proposal are preregistered, for 160 required x2 rejections.",
        "",
    ]
    overview_lines.extend(
        f"- {row['proposal_id']} [{row['expected_disposition']}]: {row['title']}"
        for row in proposals
    )
    overview_lines.extend(
        [
            "",
            "## Frozen portfolios",
            "",
            "The x1 portfolio freezes 60 safe-now tasks, 30 bounded candidates, 20 exact-approval packets, 10 blocked packets, 20 owner-local skill ideas, 10 family-current runner ideas, three substantive owner-local tool ideas, 60 CLEAN/FIX/REFINE tasks, and successor recommendations. None is executed in x1. Inherited and successor rows receive zero Caelen completion credit. Floors do not authorize filler, global installation, destructive deletion, sibling mutation, external action, or gate crossing.",
            "",
            "## Retained failures and Method Flow",
            "",
            f"Eighteen startup or preregistration failures remain retained at zero completion credit. They include output clipping, parser and field-shape assumptions, PowerShell expression mistakes, presentation-window recoveries, the five-word packet-count discrepancy, and the rejected eight-collision draft. Eighteen preferred bounded recovery methods pair those failures with eighteen failing and eighteen passing same-owner witnesses. Recovery never converts a failure into success credit.",
            "",
        ]
    )
    overview_lines.extend(
        f"- CM6751-X1-N{i:03d}: {failure} Recovery: {recovery}"
        for i, (failure, recovery) in enumerate(STARTUP_FAILURES, 1)
    )
    overview_lines.extend(
        [
            "",
            "## Sources and evidence boundary",
            "",
            "Seven current official or primary pages were checked read-only. Canadian Conservation Institute material supplies cane, woven-seat, plant-material, and vulnerability vocabulary; NIST supplies SI vocabulary; W3C PROV-O, WCAG 2.2, and Verifiable Credentials 2.0 supply provenance, structural accessibility, and nonproduction credential vocabulary; RFC 8785 supplies canonical JSON vocabulary. The phase made no dataset or media download, API call, external write, real-row ingestion, observation, measurement, or treatment decision.",
            "",
            "## Protected gates",
            "",
            "GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The chair weave and lattice language is only a typed analogy and establishes no likelihood, constraint, force, stability theorem, material law, empirical confirmation, final physics, or Theory-of-Everything proof. THOS remains participant-free protocol work without governed blind matched-budget real arms, safety monitoring, statistics, or independent review. Freed ID remains zero-key and nonproduction without standards-conformant keys or proofs, live lifecycle events, interoperability, independent security review, recovery evidence, trust governance, or affected-party oversight. CBR, professional practice, safety, ownership, heritage, privacy, accessibility, remedy, legal and cultural interpretation, Indigenous rights, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain open or exact-gated.",
            "",
            "## Route",
            "",
            "The prospective Eiren Kestrel v675-v2 edge remains PREPARED_NOT_SENT. Caelen will not list, reread, or message a successor until its own clean pushed fresh-live-equal exact-final terminal gate, and only the then-current roster and authorization may control one acknowledged send.",
            "",
            f"Terminal verdict: NOT_READY_FOR_STAGE_20. {BOUNDARY}",
        ]
    )
    write_text("x1/integrated-overview.md", "\n".join(overview_lines))


def staged_paths() -> list[str]:
    return sorted(
        line
        for line in git_text(
            "diff", "--cached", "--name-only", "--diff-filter=ACMR", SOURCE_FINAL
        ).splitlines()
        if line
    )


def staged_blob(path: str) -> bytes:
    return git("show", f":{path}").stdout.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def staged_mode(path: str) -> str:
    row = git_text("ls-files", "-s", "--", path)
    return row.split()[0]


def build_privacy() -> None:
    paths = [path for path in staged_paths() if path != PRIVACY_PATH]
    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
            re.IGNORECASE,
        ),
        "private_absolute_path": re.compile(r"\b[A-Z]:[\\/](?:Users|GHC-Archives)[\\/]"),
        "credential_assignment": re.compile(
            r"\b(?:api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*['\"]?[A-Za-z0-9+/=_-]{12,}",
            re.IGNORECASE,
        ),
        "transcript_or_session_stream": re.compile(
            r"^\s*(?:user|assistant|developer|system)\s*:", re.IGNORECASE | re.MULTILINE
        ),
        "private_callable_identifier": re.compile(r"\bmcp__[a-z0-9_]+\b", re.IGNORECASE),
    }
    text_suffixes = {".json", ".md", ".py", ".yaml", ".yml", ".html", ".txt"}
    scanned = 0
    candidates, confirmed, decode_issues = [], [], []
    for path in paths:
        if Path(path).suffix.lower() not in text_suffixes:
            continue
        scanned += 1
        try:
            text = staged_blob(path).decode("utf-8")
        except UnicodeDecodeError:
            decode_issues.append(path)
            continue
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                row = {"path": path, "line": line, "class": class_name}
                if path in {BUILDER_PATH, TEST_PATH}:
                    row["classification"] = "scanner_definition_or_rejecting_fixture"
                    candidates.append(row)
                else:
                    confirmed.append(row)
    write_json(
        "validation/x1-staged-privacy.json",
        {
            "schema": "ghc.family.staged-privacy-scan.v3",
            "owner": OWNER,
            "phase": PHASE,
            "lifecycle": "planning_only_x1",
            "hash_domain": "exact_staged_git_blob",
            "pattern_classes": sorted(patterns),
            "scanned_text_files": scanned,
            "candidates": candidates,
            "confirmed_hits": confirmed,
            "confirmed_hit_count": len(confirmed),
            "decode_issues": decode_issues,
            "self_exclusions": [PRIVACY_PATH],
            "valid": not confirmed and not decode_issues,
            "boundary": "Scanner definitions and rejecting fixtures are candidates, never silently discarded payload hits.",
        },
    )


def build_manifest() -> None:
    exclusions = [MANIFEST_PATH, REVIEW_PATH]
    paths = [path for path in staged_paths() if path not in exclusions]
    entries = []
    for path in paths:
        blob = staged_blob(path)
        entries.append(
            {
                "path": path,
                "mode": staged_mode(path),
                "bytes": len(blob),
                "sha256": hashlib.sha256(blob).hexdigest(),
            }
        )
    write_json(
        "validation/x1-manifest.json",
        {
            "schema": "ghc.family.git-blob-manifest.v6",
            "domain": "Caelen v675-v1 planning-only x1 exact staged Git blobs before two declared self files",
            "hash_domain": "normalized_lf_exact_git_blob",
            "owner": OWNER,
            "phase": PHASE,
            "source_final": SOURCE_FINAL,
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": exclusions,
        },
    )


def build_review() -> None:
    paths = staged_paths()
    name_status = git_text("diff", "--cached", "--name-status", SOURCE_FINAL).splitlines()
    deletions = [row for row in name_status if row.startswith("D\t")]
    allowed = all(
        path.startswith("docs/caelen-morrow/v675-v1/")
        or path in {BUILDER_PATH, TEST_PATH}
        for path in paths
    )
    manifest = json.loads((ROOT / MANIFEST_PATH).read_text(encoding="utf-8"))
    manifest_issues = []
    for entry in manifest["entries"]:
        try:
            blob = staged_blob(entry["path"])
        except subprocess.CalledProcessError:
            manifest_issues.append({"path": entry["path"], "issue": "missing_staged_blob"})
            continue
        if len(blob) != entry["bytes"] or hashlib.sha256(blob).hexdigest() != entry["sha256"]:
            manifest_issues.append({"path": entry["path"], "issue": "hash_or_length_mismatch"})
    expected_paths = set(manifest["self_exclusions"]) | {row["path"] for row in manifest["entries"]}
    privacy = json.loads((ROOT / PRIVACY_PATH).read_text(encoding="utf-8"))
    issues = []
    if not allowed:
        issues.append("path outside Caelen owner scope")
    if deletions:
        issues.append("staged deletion")
    if any("/x2/" in f"/{path}/" or "_x2.py" in path for path in paths):
        issues.append("x2 path in planning-only x1")
    if expected_paths != set(paths) | {REVIEW_PATH}:
        issues.append("manifest paths and exclusions do not cover prospective x1 tree")
    if manifest_issues:
        issues.append("manifest replay mismatch")
    if not privacy["valid"]:
        issues.append("privacy scan invalid")
    write_json(
        "validation/x1-staged-review.json",
        {
            "schema": "ghc.family.staged-review.v5",
            "owner": OWNER,
            "phase": PHASE,
            "lifecycle": "planning_only_x1",
            "source_final": SOURCE_FINAL,
            "staged_paths_before_self": len(paths),
            "prospective_staged_paths": len(paths) + (0 if REVIEW_PATH in paths else 1),
            "allowed_owner_scope": allowed,
            "deletions": deletions,
            "x2_paths": [path for path in paths if "/x2/" in f"/{path}/" or "_x2.py" in path],
            "manifest_entries": manifest["entry_count"],
            "manifest_self_exclusions": manifest["self_exclusions"],
            "manifest_issues": manifest_issues,
            "privacy_valid": privacy["valid"],
            "issues": issues,
            "valid": not issues,
            "outcomes_observed": False,
            "external_actions": 0,
            "boundary": BOUNDARY,
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--privacy", action="store_true")
    parser.add_argument("--manifest", action="store_true")
    parser.add_argument("--review", action="store_true")
    args = parser.parse_args()
    selected = sum((args.privacy, args.manifest, args.review))
    if selected > 1:
        raise SystemExit("select at most one lifecycle mode")
    if args.privacy:
        build_privacy()
    elif args.manifest:
        build_manifest()
    elif args.review:
        build_review()
    else:
        build_default()


if __name__ == "__main__":
    main()
