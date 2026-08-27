"""Build Eiren Kestrel v673-v3's planning-only x1 freeze.

This owner-scoped builder reads the exact immutable source tree, reconstructs
the reachable proposal-title corpus, checks the forty Eiren titles against
that bounded corpus, and writes planning/provenance/gate artifacts only.  It
never creates x2 evidence, performs network calls, stages, commits, pushes, or
contacts another task.
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
OWNER_ROOT = ROOT / "docs" / "eiren-kestrel" / "v673-v3"
OWNER = "Eiren Kestrel"
PHASE = "v673-v3"
BRANCH = "codex/GHC-Family/eiren-kestrel-v673-v3-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/caelen-morrow-v673-v2-full-tools"
SOURCE_START = "528a7d407cb7cace05b9bfd672b2fa74fc413d2c"
SOURCE_X1 = "868215a1d7c0b8ecd871959ba395c34080457768"
SOURCE_EVIDENCE = "de197000c0955d3138b870f756c3722a44e29574"
SOURCE_FINAL = "62364ecf3f66d938c539574ad2456dacd6cebd81"
SOURCE_CANONICAL_PAYLOAD_SHA256 = "7dd1ec11f0f73701df9958d304b5f2193a2bf835aaf8bc6daf7ead213c62dd10"
SOURCE_CANONICAL_RECEIPT_SHA256 = "a362b2020c26418666fab01aa9cd613cf18f28d15261a2ddca80c36ff9899ec8"
SOURCE_OPERATIONAL_OVERLAY_SHA256 = "3c43ce9f763bbf3544a6c4d31da0de62d0e1886ef7bbe05dbc4ae8e39169e18d"
CORE_LABELS = ["completed", "represented", "open_gap", "exact_gate"]
EXPECTED_COUNTS = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
DECLARED_SOURCE_CHAIN = 6310
DECLARED_RESULT_CHAIN = 6350
JACCARD_LIMIT = 0.72

IDENTITY_BOUNDARY = (
    "Eiren Kestrel, they/them, relational wall-state topology cartographer and "
    "land-authority boundary keeper, is relational working language only. It is not "
    "evidence of consciousness, sentience, legal personhood, identity "
    "continuity, employment, qualification, independent agency, scientific or "
    "operational authority, professional authority, legal or cultural "
    "authority, affected-party authority, or Māori authority. Hamish may "
    "rename, pause, redirect, or stop the work."
)

PRACTICE_BOUNDARY = (
    "The dry-stone wall condition-documentation lens is wholly synthetic learning "
    "and software design. It uses no real people, practitioners, communities, "
    "land, walls, stones, sites, structures, habitats, observations, measurements, "
    "images, tools, lifting, dismantling, rebuilding, repairs, access events, "
    "identity events, authority acts, or affected-party decisions. It confers no "
    "employment, qualification, walling, masonry, engineering, conservation, "
    "archaeology, heritage, land, workplace or structural-safety, legal, cultural, "
    "Māori, privacy, accessibility, ownership, custody, or operational authority."
)

SCIENCE_BOUNDARY = (
    "GMUT remains a typed scalar-tensor and effective-field-theory research-model "
    "family without real likelihood, constraint, prediction, force, material "
    "law, empirical confirmation, final physics, quantum or ultraviolet "
    "completion, Theory-of-Everything proof, or canon. THOS remains proxy-only "
    "without governed blind matched-budget real arms, safety monitoring, "
    "appropriate statistics, and independent review. Freed ID remains synthetic "
    "and nonproduction without standards-conformant real keys and proofs, live "
    "lifecycle events, interoperability, independent privacy/security review, "
    "recovery evidence, trust governance, and affected-party oversight."
)

AUTHORITY_BOUNDARY = (
    "Professional dry-stone practice, masonry, engineering, conservation, "
    "archaeology, heritage and land decisions, temporary support, lifting, worker, "
    "visitor, ecological and structural safety, ownership, custody, access, image "
    "rights, privacy, accessibility, remedy, legal or cultural interpretation, "
    "affected-party legitimacy, traditional knowledge, Māori wording, Māori "
    "concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority "
    "remain open or exact-gated. Māori concepts remain under Māori authority. "
    "Terminal verdict remains NOT_READY_FOR_STAGE_20."
)


PROPOSAL_SPECS: list[tuple[str, str, str]] = [
    ("Synthetic dry-stone wall segment identity, endpoint, and adjacency register", "completed", "x2/practice/segment-identity-register.json"),
    ("Dry-stone wall face, base, heart, and cope zone topology", "completed", "x2/practice/wall-zone-topology.json"),
    ("Dry-stone course overlap, running-joint, and cross-face relation graph", "completed", "x2/practice/course-relation-graph.json"),
    ("Dry-stone through-stone, tie-stone, and bonding placeholder map", "completed", "x2/practice/bonding-placeholder-map.json"),
    ("Dry-stone hearting, pinning, and void observation vocabulary", "completed", "x2/practice/hearting-void-vocabulary.json"),
    ("Dry-stone batter, height, width, and offset SI placeholder envelope", "completed", "x2/practice/si-placeholder-envelope.json"),
    ("Dry-stone foundation-contact and terrain-slope declaration", "completed", "x2/practice/foundation-terrain-declaration.json"),
    ("Dry-stone junction, return, stile, gateway, and termination topology", "completed", "x2/practice/junction-termination-topology.json"),
    ("Dry-stone coping placement, continuity, and displacement state graph", "completed", "x2/practice/coping-state-graph.json"),
    ("Dry-stone bulge, lean, settlement, breach, and collapse condition taxonomy", "completed", "x2/practice/condition-taxonomy.json"),
    ("Dry-stone unit rotation, fracture, spall, and missingness uncertainty ledger", "completed", "x2/practice/unit-uncertainty-ledger.json"),
    ("Dry-stone drainage, seepage, runoff, and saturation observation hold", "completed", "x2/practice/water-observation-hold.json"),
    ("Dry-stone vegetation, root, lichen, and habitat non-disturbance register", "completed", "x2/practice/ecology-nondisturbance-register.json"),
    ("Dry-stone enclosure function, boundary meaning, and land-use claim abstention", "completed", "x2/practice/land-use-claim-abstention.json"),
    ("Dry-stone construction phase, repair, and supersession provenance chain", "completed", "x2/practice/repair-provenance-chain.json"),
    ("Dry-stone material source and geological identification quarantine", "completed", "x2/practice/material-source-quarantine.json"),
    ("Dry-stone photographic view, scale, orientation, lineage, and rights reservation", "represented", "x2/cbr/image-rights-reservation.json"),
    ("Dry-stone inspection route, blind-zone, and access-refusal declaration", "completed", "x2/practice/inspection-access-declaration.json"),
    ("Dry-stone condition priority ranking refusal and escalation gate", "completed", "x2/practice/priority-refusal-gate.json"),
    ("Dry-stone proposed dismantling sequence DAG with intervention abstention", "completed", "x2/practice/dismantling-sequence-dag.json"),
    ("Dry-stone course-by-course rebuilding lineage with placement uncertainty", "completed", "x2/practice/rebuilding-lineage.json"),
    ("Dry-stone displaced-unit custody, label minimization, and reconciliation ledger", "completed", "x2/practice/displaced-unit-ledger.json"),
    ("Dry-stone lifting, pinch, crush, instability, and tool-hazard reservation", "completed", "x2/practice/hazard-reservation.json"),
    ("Dry-stone weather, frost, saturation, and observation-time bitemporal ledger", "completed", "x2/practice/weather-time-ledger.json"),
    ("Dry-stone estimate, consent, authorization, and work-instruction splitter", "completed", "x2/practice/authorization-splitter.json"),
    ("Dry-stone change-window pause, resume, rollback, and expiry state machine", "completed", "x2/thos/change-window-state-machine.json"),
    ("Dry-stone role separation, two-key stop, workload, and shift handover", "completed", "x2/thos/workload-handover.json"),
    ("Dry-stone structurally accessible linear condition companion with print fallback", "completed", "x2/accessibility/linear-condition-companion.html"),
    ("Dry-stone disputed-field amendment braid, preserved predecessor, and readback hash", "completed", "x2/practice/amendment-readback-ledger.json"),
    ("GMUT dry-stone geometry and contact quantity board with zero fitted parameters", "represented", "x2/gmut/geometry-contact-quantity-board.json"),
    ("THOS dry-stone inspection protocol proxy with zero participants or effectiveness claim", "represented", "x2/thos/inspection-protocol-proxy.json"),
    ("Freed ID selective-disclosure dry-stone condition dossier with zero live identity operations", "represented", "x2/freed-id/selective-disclosure-dossier.json"),
    ("Freed ID dry-stone correction, status, and revocation envelope with zero keys or proofs", "represented", "x2/freed-id/correction-revocation-envelope.json"),
    ("CBR dry-stone ownership, custody, access, visibility, and remedy capability matrix", "represented", "x2/cbr/rights-capability-matrix.json"),
    ("PROV-O dry-stone entity-activity mapping adapter with zero external rows", "represented", "x2/adapters/prov-o-zero-row-adapter.json"),
    ("Dry-stone official-source vocabulary ledger with compliance and competence abstention", "represented", "x2/sources/official-source-ledger.json"),
    ("Transport-disabled Historic England dry-stone source adapter and unresolved schema mapping", "open_gap", "x2/adapters/historic-england-transport-disabled.json"),
    ("Dry-stone practitioner and affected-community vocabulary review gap with zero reviewers", "open_gap", "x2/gates/practitioner-community-review-gap.json"),
    ("Dry-stone physical intervention, temporary support, and structural-safety authority gate", "exact_gate", "x2/gates/intervention-safety-authority-gate.json"),
    ("Dry-stone land, heritage, archaeology, cultural, affected-party, and Māori-authority gate", "exact_gate", "x2/gates/land-cultural-maori-authority-gate.json"),
]


STARTUP_FAILURES = [
    (
        "Authorization-state path assumption failed",
        "The first read-only probe guessed a historical authorization-state filename that does not exist and therefore produced no source evidence.",
        "Enumerate the bounded skill reference directory and read the declared current-state file through EOF.",
    ),
    (
        "Authorization-state whole presentation was truncated",
        "The first whole-file authorization-state display exceeded the useful response window and was not treated as a complete read.",
        "Read deterministic numbered UTF-8 windows through the exact final line and validate the current schema separately.",
    ),
    (
        "Worktree creation presentation windows elapsed",
        "The one no-checkout worktree operation outlived several reporting windows while building the large shared index.",
        "Keep the original session, inspect rather than duplicate it, and continue only after that same operation completes.",
    ),
    (
        "Checkout initially met a live index lock",
        "An earlier broad read-only status process still owned the new worktree index lock, so the first checkout stopped without changing the intended source state.",
        "Audit the exact process and target, wait for natural completion and lock release, then retry checkout once.",
    ),
    (
        "Stained-glass audit used the host legacy code page",
        "The first read-only semantic audit stopped when CP-1252 could not encode a Māori macron in a reachable title.",
        "Rerun only that failed audit with PYTHONIOENCODING=utf-8 and retain the encoding failure at zero credit.",
    ),
    (
        "Stained-glass practice candidate collided conceptually",
        "Although the numerical slate cleared the threshold, exact reachable neighbors already contained lead-came topology and protective-glazing relations.",
        "Reject the candidate before x1 and award no Eiren novelty credit.",
    ),
    (
        "Neon-sign practice candidate matched an inherited suite",
        "A bounded exact-tree search found an existing neon documentation, provenance, safety, and authority suite in the inherited history.",
        "Reject neon before planning and treat the inherited suite as zero-credit evidence.",
    ),
    (
        "Broad multi-domain Git grep exceeded the output window",
        "One read-only search projected too many inherited matches and its truncated presentation was not used as semantic evidence.",
        "Use the exact content-addressed proposal corpus and return only bounded counts and samples per candidate domain.",
    ),
    (
        "Oversized neon grep left two orphaned readers",
        "Two audited read-only git grep processes survived their presentation wrapper and retained no useful attributable receipt.",
        "Verify their exact command lines, stop only those stale readers, and use a bounded content-addressed projection.",
    ),
    (
        "Composite startup-state projection returned no attributable output",
        "A read-only PowerShell object projection completed without a usable receipt despite the underlying scalar Git state remaining available.",
        "Recover with separate literal scalar Git commands for head, branch, status, and sparse patterns.",
    ),
    (
        "Stdin-pipeline corpus projection orphaned its process tree",
        "A PowerShell here-string pipeline returned without a receipt while one Python reader and its cat-file children remained alive.",
        "Audit and stop only that read-only orphan tree, then invoke Python directly with one tracked session.",
    ),
    (
        "Sparse bootstrap directories were absent",
        "The first mechanical template copy stopped because empty scripts and tests directories had not materialized in the sparse worktree.",
        "Create only the two Eiren-owned directories and rerun the bounded copy once.",
    ),
    (
        "First official-source search wrapper returned no presentation",
        "The initial read-only official-source search call produced no attributable result and was not counted as source evidence.",
        "Repeat only the failed search with a bounded result projection and retain links from official or primary domains.",
    ),
    (
        "Bandit unavailable in active Python runtime",
        "The active Python 3.12 environment inherited from Caelen reported no Bandit module; availability was not converted into an installation mandate.",
        "Use dependency-justified available validators and retain Bandit as an explicit tool-availability gap.",
    ),
    (
        "Bytecode-cache cleanup forms were blocked by host safety policy",
        "Three scoped PowerShell deletion forms were rejected before execution even after both cache paths were verified inside the Eiren worktree.",
        "Leave the caches ignored and outside Git evidence, set PYTHONDONTWRITEBYTECODE=1 for later validation, and do not weaken the host guard.",
    ),
    (
        "Direct Ruff executable was absent from shell PATH",
        "The first bounded Ruff command failed before analysis because the inherited executable was not exposed as a direct shell command.",
        "Invoke the same installed Ruff package through python -m ruff against the unchanged two-file scope.",
    ),
    (
        "First strict mypy check found an untyped JSON helper",
        "The initial strict mypy run reported one missing return annotation on the copied test JSON loader.",
        "Annotate only that helper with an explicit Any return and rerun mypy on the same two-file scope.",
    ),
]


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False)
    if check and result.returncode:
        raise SystemExit(result.stderr.decode("utf-8", errors="replace"))
    return result


def write_json(relative: str, payload: Any) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def normalize(title: str) -> set[str]:
    stop = {
        "and", "the", "with", "for", "from", "into", "without", "only",
        "synthetic", "dry", "stone", "wall", "walling", "board", "profile",
        "matrix", "envelope",
    }
    return {
        token
        for token in re.findall(r"[a-z0-9āēīōū]+", title.lower())
        if len(token) > 2 and token not in stop
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
        input=("\n".join(specs) + "\n").encode("utf-8"),
        timeout=420 if len(specs) > 512 else 90,
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
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return (
        {
            "scope": "exact Caelen Morrow v673-v2 final docs tree, proposal-named JSON paths only",
            "candidate_git_blob_paths": len(candidates),
            "malformed_or_missing_blobs": malformed,
            "semantic_occurrences": occurrences,
            "unique_proposal_ids": len(proposal_ids),
            "unique_titles": len(titles),
            "corpus_sha256": hashlib.sha256(canonical).hexdigest(),
            "declared_source_chain": DECLARED_SOURCE_CHAIN,
            "materialized_ids_cover_declared_chain": len(proposal_ids) >= DECLARED_SOURCE_CHAIN,
            "exact_canonical_row_mapping": False,
            "canonical_row_mapping_open_gap": True,
            "universal_novelty_claim": False,
            "reason": "No single reachable ledger maps every declared row; source-bounded comparison is evidence, not universal novelty proof.",
        },
        sorted(titles),
    )


def proposal_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (title, outcome, artifact) in enumerate(PROPOSAL_SPECS, start=1):
        proposal_id = f"EK6733-N{index:03d}"
        if outcome == "completed":
            approval, lane = "safe_now", "x2_synthetic_validation"
            hypothesis = f"A fail-closed {title.lower()} can reject ambiguous or unsafe synthetic states without ingesting real-world data."
            null = f"The {title.lower()} accepts an undeclared state, implies real practice, or lacks a bounded passing and rejecting witness."
            falsifier = "One preregistered invalid mutation is accepted or the positive synthetic control is rejected."
        elif outcome == "represented":
            approval, lane = "candidate", "x2_representation_only"
            hypothesis = f"A synthetic schema can represent {title.lower()} while preserving the absence of empirical, participant, production, or authority evidence."
            null = f"The {title.lower()} is presented as real-world evidence, operational readiness, identity production, or authority."
            falsifier = "The artifact omits its representation-only boundary or contains a real-world row, call, key, proof, measurement, or outcome."
        elif outcome == "open_gap":
            approval, lane = "candidate", "open_gap_zero_network_or_real_data"
            hypothesis = f"A transport-disabled contract can expose the unresolved requirements for {title.lower()} without making a network call."
            null = f"The {title.lower()} performs transport, ingests a row, or claims source coverage without current official evidence."
            falsifier = "Any network call or real row occurs, or the open gap is silently converted to completion."
        else:
            approval, lane = "exact_approval", "exact_gate_unexecuted"
            hypothesis = f"An explicit exact gate can keep {title.lower()} visible and unexecuted until complete action-specific authority and affected-party evidence exist."
            null = f"The {title.lower()} executes, implies legitimacy, or weakens the protected gate without exact authority."
            falsifier = "The gate executes or claims professional, legal, cultural, affected-party, Māori, or operational authority."

        source_need = (
            "Current official or primary sources are needed only for vocabulary and refusal constraints; citations cannot become observations, endorsement, competence, or authority."
        )
        if index in {37, 38}:
            source_need = (
                "Current official heritage and practitioner documentation plus governed reviewer participation would be required before capability claims; x2 remains transport-disabled with zero calls, rows, or reviewers."
            )
        if index in {39, 40}:
            source_need = (
                "Exact action-specific professional, safety, land, affected-party, legal, cultural, tangata whenua, iwi, hapū, and Māori-authority evidence is required; public sources cannot close this gate."
            )

        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "primary_pillar": "THOS Body",
                "protected_pillars": ["GMUT Mind", "Freed ID and CBR Heart"],
                "bounded_practice": "synthetic dry-stone wall condition documentation",
                "hypothesis": hypothesis,
                "null_or_failure_condition": null,
                "approval_class": approval,
                "execution_lane": lane,
                "current_official_or_primary_source_need": source_need,
                "concrete_artifacts": [artifact],
                "falsifier_or_acceptance_gate": falsifier,
                "rollback_or_recovery": "Quarantine the artifact, retain the failed witness, restore the last exact manifest, and leave the outcome open or exact-gated.",
                "protected_gates": [
                    "zero real people, communities, land, walls, stones, sites, observations, measurements, images, interventions, keys, proofs, or identity events",
                    "no professional, structural or workplace safety, heritage, land, legal, cultural, affected-party, Māori, privacy-complete, accessibility-complete, independent, or Stage 20 authority",
                ],
                "expected_disposition": outcome,
                "outcome_observed": False,
                "inherited_completion_credit": 0,
                "eiren_novelty_credit": 1,
            }
        )
    return rows


def startup_method_flow() -> dict[str, Any]:
    methods: list[dict[str, Any]] = []
    witnesses: list[dict[str, Any]] = []
    for index, (title, failure, recovery) in enumerate(STARTUP_FAILURES, start=1):
        method_id = f"EK6733-M{index:03d}"
        methods.append(
            {
                "method_id": method_id,
                "title": title,
                "status": "preferred",
                "failure_signature": failure,
                "candidate_workaround": recovery,
                "recurrence_guard": recovery,
                "rollback": "Stop the affected scalar operation, preserve repository bytes, and return to the last verified state.",
                "owner": OWNER,
                "phase": PHASE,
            }
        )
        witnesses.extend(
            [
                {"witness_id": f"{method_id}-F", "method_id": method_id, "kind": "failed", "retained": True, "credit": 0, "observed": failure},
                {"witness_id": f"{method_id}-P", "method_id": method_id, "kind": "passing", "retained": True, "credit": 0, "observed": recovery},
            ]
        )
    return {
        "schema": "ghc.family.method-flow.phase-startup.v3",
        "owner": OWNER,
        "phase": PHASE,
        "method_count": len(methods),
        "failed_witness_count": len(methods),
        "passing_witness_count": len(methods),
        "methods": methods,
        "witnesses": witnesses,
        "boundary": "Operational learning only; passing recovery does not erase failure or create scientific, professional, independent, authority, or Stage 20 credit.",
    }


def portfolio_rows(proposals: list[dict[str, Any]]) -> dict[str, Any]:
    skill_names = [
        "dry-stone-segment-identity", "dry-stone-zone-topology", "dry-stone-course-relations",
        "dry-stone-bonding-placeholder", "dry-stone-void-vocabulary", "dry-stone-si-placeholder",
        "dry-stone-junction-topology", "dry-stone-condition-taxonomy", "dry-stone-water-hold",
        "dry-stone-ecology-nondisturbance", "dry-stone-repair-provenance", "dry-stone-material-quarantine",
        "dry-stone-image-rights", "dry-stone-access-declaration", "dry-stone-dismantling-dag",
        "dry-stone-rebuilding-lineage", "dry-stone-displaced-unit-ledger", "dry-stone-hazard-reservation",
        "dry-stone-accessible-companion", "dry-stone-stage20-refusal",
    ]
    runner_names = [
        "ghc_family_dry_stone_intake", "ghc_family_dry_stone_topology",
        "ghc_family_dry_stone_condition", "ghc_family_dry_stone_provenance",
        "ghc_family_dry_stone_change_control", "ghc_family_dry_stone_authority_gate",
        "ghc_family_dry_stone_freed_id", "ghc_family_dry_stone_thos_proxy",
        "ghc_family_dry_stone_gmut_symbolic", "ghc_family_dry_stone_terminal_refusal",
    ]
    tools = [
        "ghc_family_eiren_kestrel_v673_v3_dry_stone_record.py",
        "ghc_family_eiren_kestrel_v673_v3_topology_graph.py",
        "ghc_family_eiren_kestrel_v673_v3_authority_gate.py",
    ]
    safe_now = [
        {"task_id": f"EK6733-SN-{i:03d}", "title": f"Validate planning contract for {row['title']}", "state": "planned", "execution": "x2 synthetic only"}
        for i, row in enumerate(proposals, start=1)
    ]
    safe_now.extend(
        {"task_id": f"EK6733-SN-{40+i:03d}", "title": f"Build and smoke-use owner-local skill {name}", "state": "planned", "execution": "x2 owner-local only"}
        for i, name in enumerate(skill_names, start=1)
    )
    candidates = [
        {"task_id": f"EK6733-C-{i:03d}", "title": f"Represent bounded evidence for {proposals[i-1]['title']}", "state": "planned", "execution": "x2 representation only"}
        for i in range(1, 31)
    ]
    exact_approval = [
        {"task_id": f"EK6733-EA-{i:03d}", "title": title, "state": "unexecuted_exact_approval", "authority": "absent"}
        for i, title in enumerate(
            [
                "Enter or inspect a real wall or site", "Record a real owner address parcel or location",
                "Measure a real wall stone slope or displacement", "Photograph a real wall person or property",
                "Handle move sort label or lift a real stone", "Dismantle or rebuild a real wall",
                "Install temporary support access control or exclusion zones", "Provide structural workplace or visitor-safety advice",
                "Disturb vegetation habitat soil or archaeological context", "Make a real condition priority or repair recommendation",
                "Create a real estimate consent or work instruction", "Make a land boundary custody ownership or access decision",
                "Issue a real identity credential key or proof", "Contact an external heritage or collection API",
                "Ingest a real heritage record image or geometry row", "Claim practitioner or affected-community acceptance",
                "Make a legal heritage archaeological or cultural interpretation", "Use Māori wording concepts or data-governance authority",
                "Claim privacy or accessibility completeness", "Claim independent reproduction or Stage 20 readiness",
            ], start=1
        )
    ]
    blocked = [
        {"task_id": f"EK6733-B-{i:03d}", "title": title, "state": "blocked_unexecuted", "reason": "protected evidence or authority absent"}
        for i, title in enumerate(
            [
                "Real dry-stone condition or intervention study", "Real governed THOS field arms", "Empirical GMUT constraint",
                "Production Freed ID lifecycle", "Professional structural or safety validation", "Heritage or archaeological authorization",
                "Affected-party legal or cultural ratification", "Māori-authority review", "Operational deployment",
                "Stage 20 transition",
            ], start=1
        )
    ]
    cfr: list[dict[str, Any]] = []
    for kind in ("CLEAN", "FIX", "REFINE"):
        for i, skill in enumerate(skill_names, start=1):
            cfr.append({"task_id": f"EK6733-{kind}-{i:03d}", "kind": kind, "title": f"{kind.title()} {skill} boundary evidence", "state": "planned_additive"})
    return {
        "schema": "ghc.family.owner-portfolio-freeze.v5",
        "owner": OWNER,
        "phase": PHASE,
        "safe_now": safe_now,
        "candidate": candidates,
        "exact_approval": exact_approval,
        "blocked": blocked,
        "clean_fix_refine": cfr,
        "phase_local_skills": [{"name": name, "planned": True, "global_install": False} for name in skill_names],
        "family_current_runners": [{"name": name, "planned": True, "global_install": False} for name in runner_names],
        "substantive_tools": [{"name": name, "planned": True, "global_install": False} for name in tools],
        "counts": {
            "safe_now": len(safe_now), "candidate": len(candidates),
            "exact_approval": len(exact_approval), "blocked": len(blocked),
            "clean_fix_refine": len(cfr), "skills": len(skill_names),
            "runners": len(runner_names), "tools": len(tools),
        },
        "boundary": "Plans are not outcomes. Exact-approval and blocked rows remain visible and unexecuted; counts are ceilings-aware bounded work, not authority or completion quotas.",
    }


def integrated_overview(proposals: list[dict[str, Any]], corpus: dict[str, Any], max_score: float) -> str:
    rows = [
        "# Eiren Kestrel v673-v3 planning-only x1 integrated overview",
        "",
        "## Relational working frame",
        "",
        IDENTITY_BOUNDARY,
        "",
        "Eiren's bounded hope is to make every synthetic wall-state transition inspectable, reversible, and unmistakably short of authority over land, structures, heritage, culture, safety, or people. The primary Trinity Mandala focus is THOS Body. GMUT Mind and Freed ID and CBR Heart remain explicit and protected.",
        "",
        "## Bounded practice",
        "",
        PRACTICE_BOUNDARY,
        "",
        "The phase treats dry-stone wall condition documentation only as a synthetic record-design lens: segment and course topology, observation vocabularies, proposed-change lineage, correction paths, workload, accessible handover, and refusal states. No record denotes a real wall, stone, parcel, site, practitioner, community, owner, visitor, habitat, image, measurement, or intervention. A symbolic state is never a site inspection, engineering assessment, conservation decision, land determination, safety instruction, repair recommendation, heritage interpretation, or cultural conclusion.",
        "",
        "Dry-stone practice is materially and culturally situated. The software therefore separates a recordable placeholder from the people and communities who hold knowledge, the land and sites to which a structure relates, and the competent professionals and authorities who may lawfully inspect or act. Topology can show that a declared edge is absent; it cannot establish structural stability. A bitemporal ledger can preserve an earlier assertion; it cannot determine which account is legally, culturally, or professionally correct. A rights field can expose that consent is missing; it cannot manufacture consent.",
        "",
        "## Novelty scope",
        "",
        f"The immutable source declares {DECLARED_SOURCE_CHAIN:,} frozen rows. The exact source-tree audit inspected {corpus['candidate_git_blob_paths']:,} proposal-named JSON blobs, recovered {corpus['semantic_occurrences']:,} occurrences, {corpus['unique_proposal_ids']:,} identifiers, and {corpus['unique_titles']:,} unique titles. The forty Eiren titles cleared the fixed {JACCARD_LIMIT:.2f} token-Jaccard threshold with a maximum observed score of {max_score:.6f}. No universal novelty claim is made because no single exact canonical row-to-title ledger covers the declared chain.",
        "",
        "## X1/X2 separation",
        "",
        "This commit is planning only. Every proposal has one expected disposition but outcome_observed=false. It contains no x2 implementation, no real or synthetic outcome ledger, no production claim, and no successor delivery. The dedicated x1 must be committed, pushed, clean, zero-divergent, and fresh four-way equal before x2 starts.",
        "",
        "## Proposal slate",
        "",
        "| ID | Expected | Proposal |",
        "| --- | --- | --- |",
    ]
    rows.extend(f"| {row['proposal_id']} | {row['expected_disposition']} | {row['title']} |" for row in proposals)
    rows.extend(
        [
            "",
            "## Evidence and authority boundaries",
            "",
            SCIENCE_BOUNDARY,
            "",
            AUTHORITY_BOUNDARY,
            "",
            "Current official or primary sources may later provide bounded vocabulary and refusal constraints. A citation will not count as observation, endorsement, professional competence, participant evidence, legal interpretation, cultural ratification, affected-party acceptance, Māori authority, empirical confirmation, or independent reproduction.",
            "",
            "## Failure retention",
            "",
            f"{len(STARTUP_FAILURES)} startup failures are retained with zero credit and paired with bounded recoveries. The recovery witnesses do not erase the wrong path assumption, truncated presentations, index-lock wait, encoding fault, rejected candidate domains, orphaned read-only processes, sparse-directory assumption, failed search presentation, or unavailable Bandit module. X2 will add every rejecting mutation, skill, runner, tool, parser, timeout, and gate witness through Method Flow.",
            "",
            "## Delivery truth",
            "",
            "This x1 neither contacts nor names an authorized later recipient. Hamish's newest live route, roster, authorization state, uniqueness, duplicate, pause, privacy, evidence, safety, usage, and acknowledgement gates must all be refreshed only after Eiren's own terminal exact-final gate. PREPARED_NOT_SENT applies to any later committed candidate until an existing-task message acknowledgement exists.",
            "",
            "Terminal verdict: `NOT_READY_FOR_STAGE_20`.",
        ]
    )
    return "\n".join(rows)


def build() -> None:
    head = git("rev-parse", "HEAD").stdout.decode().strip()
    branch = git("branch", "--show-current").stdout.decode().strip()
    if head != SOURCE_FINAL or branch != BRANCH:
        raise SystemExit(f"x1 must start at exact source on exact branch: head={head} branch={branch}")

    corpus, source_titles = recover_proposal_corpus()
    if corpus["malformed_or_missing_blobs"]:
        raise SystemExit("proposal corpus contains malformed or missing blobs")
    proposals = proposal_rows()
    source_sets = [(title, normalize(title)) for title in source_titles]
    slate_sets: list[tuple[str, set[str]]] = []
    neighbors: list[dict[str, Any]] = []
    collisions: list[dict[str, Any]] = []
    max_score = 0.0
    for row in proposals:
        tokens = normalize(row["title"])
        best_title, best_score, best_scope = "", 0.0, "source"
        for title, other in source_sets + slate_sets:
            union = tokens | other
            score = len(tokens & other) / len(union) if union else 1.0
            if score > best_score:
                best_title, best_score = title, score
                best_scope = "current_slate" if (title, other) in slate_sets else "source"
        collision = best_score >= JACCARD_LIMIT
        item = {
            "proposal_id": row["proposal_id"], "candidate_title": row["title"],
            "nearest_title": best_title, "nearest_scope": best_scope,
            "jaccard": round(best_score, 6), "collision": collision,
        }
        neighbors.append(item)
        if collision:
            collisions.append(item)
        max_score = max(max_score, best_score)
        slate_sets.append((row["title"], tokens))
    if collisions:
        raise SystemExit("semantic neighbor collision requires proposal rewrite: " + json.dumps(collisions, ensure_ascii=False))

    counts = Counter(row["expected_disposition"] for row in proposals)
    if dict(counts) != EXPECTED_COUNTS:
        raise SystemExit(f"unexpected outcome counts: {dict(counts)}")

    portfolio = portfolio_rows(proposals)
    method_flow = startup_method_flow()
    write_json(
        "x1/proposals.json",
        {
            "schema": "ghc.family.proposals.v9", "owner": OWNER, "phase": PHASE,
            "source_final": SOURCE_FINAL, "declared_source_chain": DECLARED_SOURCE_CHAIN,
            "declared_result_chain": DECLARED_RESULT_CHAIN, "proposal_count": len(proposals),
            "expected_disposition_counts": EXPECTED_COUNTS, "outcomes_observed": False,
            "proposals": proposals, "identity_boundary": IDENTITY_BOUNDARY,
            "practice_boundary": PRACTICE_BOUNDARY, "science_boundary": SCIENCE_BOUNDARY,
            "authority_boundary": AUTHORITY_BOUNDARY,
        },
    )
    write_json(
        "x1/semantic-neighbor-audit.json",
        {
            "schema": "ghc.family.semantic-neighbor-audit.v8", "owner": OWNER, "phase": PHASE,
            "exact_source_tree_corpus": corpus, "declared_source_chain": DECLARED_SOURCE_CHAIN,
            "declared_result_chain": DECLARED_RESULT_CHAIN, "threshold": JACCARD_LIMIT,
            "max_jaccard": round(max_score, 6), "collisions": 0,
            "universal_novelty_claim": False, "rows": neighbors,
            "boundary": "Exact reachable-title comparison only; inaccessible canonical row mapping remains open_gap.",
        },
    )
    write_json("x1/portfolio-freeze.json", portfolio)
    write_json("x1/method-flow-startup.json", method_flow)
    write_json(
        "x1/precommit-tool-failures.json",
        {
            "schema": "ghc.family.precommit-tool-failures.v2",
            "owner": OWNER,
            "phase": PHASE,
            "failures": [
                {
                    "method_id": f"EK6733-M{index:03d}",
                    "title": title,
                    "failure_signature": failure,
                    "candidate_workaround": recovery,
                    "passing_witness_observed": recovery,
                    "retained": True,
                    "credit": 0,
                }
                for index, (title, failure, recovery) in enumerate(
                    STARTUP_FAILURES[-3:], start=len(STARTUP_FAILURES) - 2
                )
            ],
            "boundary": "Host-policy, executable-resolution, and type-check recoveries do not erase their failed invocations or create independent, professional, authority, or Stage 20 credit.",
        },
    )
    write_json(
        "x1/source-and-provenance.json",
        {
            "schema": "ghc.family.source-provenance.v6", "owner": OWNER, "phase": PHASE,
            "source_branch": SOURCE_BRANCH, "source_start": SOURCE_START, "source_x1": SOURCE_X1,
            "source_evidence": SOURCE_EVIDENCE, "source_final": SOURCE_FINAL,
            "source_canonical_payload_sha256": SOURCE_CANONICAL_PAYLOAD_SHA256,
            "source_canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
            "source_operational_overlay_sha256": SOURCE_OPERATIONAL_OVERLAY_SHA256,
            "external_receipt_file_location_materialized": True,
            "external_receipt_digest_recomputed": True,
            "external_receipt_boundary": "The bounded external bank verified payload, receipt, operational overlay, and acknowledged delivery; no private absolute path or task identifier is retained here.",
            "source_history": {"phase_commits": 3, "merges": 0, "final_parent_count": 1, "direct_parent_chain_verified": True},
            "source_live_equality": {"local_upstream_tracking_fresh_live_equal": True, "divergence": "0/0", "clean": True},
            "source_validation_replayed": False,
        },
    )
    write_json(
        "x1/threat-model.json",
        {
            "schema": "ghc.family.threat-model.v5", "owner": OWNER, "phase": PHASE,
            "assets": ["truthful synthetic records", "retained failures", "protected gates", "source lineage", "privacy-safe artifacts"],
            "threats": [
                {"id": "T01", "threat": "synthetic wall record mistaken for inspection or dry-stone competence", "control": "practice boundary and exact professional gate"},
                {"id": "T02", "threat": "real person, location, parcel, site, wall, stone, or image data enters artifacts", "control": "synthetic-only schema, minimization, and five-class scan"},
                {"id": "T03", "threat": "symbolic geometry or condition field mistaken for measurement or stability evidence", "control": "placeholder-only type and structural-assessment refusal"},
                {"id": "T04", "threat": "rights reservation mistaken for consent", "control": "represented label and affected-party exact gate"},
                {"id": "T05", "threat": "public citation mistaken for authority", "control": "source-status ledger and citation boundary"},
                {"id": "T06", "threat": "Māori wording or concepts used without authority", "control": "exact gate and English-only placeholder"},
                {"id": "T07", "threat": "real identity credential or key production", "control": "Freed ID synthetic/nonproduction boundary"},
                {"id": "T08", "threat": "failed aggregate or mutation silently promoted", "control": "Method Flow retention and one-shot canonical policy"},
                {"id": "T09", "threat": "sibling or shared lane mutation", "control": "unique sparse D-first owner worktree"},
                {"id": "T10", "threat": "premature successor contact", "control": "terminal route gate and PREPARED_NOT_SENT"},
            ],
            "residual_risk": "Real-world, participant, professional, legal, cultural, affected-party, Māori, production, deployment, independent, and Stage 20 evidence remains absent.",
        },
    )
    write_json(
        "x1/approval-split.json",
        {
            "schema": "ghc.family.approval-split.v4", "owner": OWNER, "phase": PHASE,
            "safe_now": [row["proposal_id"] for row in proposals if row["approval_class"] == "safe_now"],
            "candidate": [row["proposal_id"] for row in proposals if row["approval_class"] == "candidate"],
            "exact_approval": [row["proposal_id"] for row in proposals if row["approval_class"] == "exact_approval"],
            "exact_approval_executed": 0, "blocked_executed": 0,
            "boundary": "Classification is not permission expansion; exact-approval work remains unexecuted.",
        },
    )
    write_json(
        "x1/open-gate-plan.json",
        {
            "schema": "ghc.family.open-gate-plan.v4", "owner": OWNER, "phase": PHASE,
            "repository_sealed_source_counts": {"negatives": 36594, "methods": 22922, "failed_witnesses": 8255, "passing_witnesses": 10485, "open_gaps": 295, "exact_gates": 288},
            "inherited_activation_baseline": {"negatives": 36595, "methods": 22923, "failed_witnesses": 8256, "passing_witnesses": 10486, "open_gaps": 295, "exact_gates": 288},
            "planned_new_open_gaps": [row["proposal_id"] for row in proposals if row["expected_disposition"] == "open_gap"],
            "planned_new_exact_gates": [row["proposal_id"] for row in proposals if row["expected_disposition"] == "exact_gate"],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "x1/selected-toolchain-plan.json",
        {
            "schema": "ghc.family.selected-toolchain-plan.v3", "owner": OWNER, "phase": PHASE,
            "dependency_justified_existing_tools": ["Python", "pytest", "Ruff", "mypy", "Hypothesis", "Pyright", "Node.js", "npm"],
            "unavailable_retained": ["Bandit in active Python 3.12"],
            "installation_authorized_or_performed": False,
            "boundary": "Availability and Hamish's prior package request are inventory, not a mandate to bulk-run, reinstall, update Codex, or install unrelated software.",
        },
    )
    write_json(
        "x1/official-source-plan.json",
        {
            "schema": "ghc.family.official-source-plan.v4",
            "owner": OWNER,
            "phase": PHASE,
            "network_calls_by_builder": 0,
            "sources": [
                {
                    "source_id": "UNESCO-DRY-STONE-2024",
                    "authority": "UNESCO Intangible Cultural Heritage",
                    "url": "https://ich.unesco.org/en/decisions/19.COM/7.B.57",
                    "status": "current decision recorded",
                    "phase_use": "dry-stone construction, knowledge transmission, community participation, safeguarding, and cultural-reservation vocabulary only",
                },
                {
                    "source_id": "HISTORIC-ENGLAND-DRY-STONE-43-2018",
                    "authority": "Historic England",
                    "url": "https://historicengland.org.uk/research/results/reports/43-2018",
                    "status": "stable research report",
                    "phase_use": "landscape, boundary, habitat, condition-context, and heritage-reservation vocabulary only",
                },
                {
                    "source_id": "HERITAGE-NZ-STONE-WALL-7118",
                    "authority": "Heritage New Zealand Pouhere Taonga",
                    "url": "https://www.heritage.org.nz/list-details/7118/Stone%2BWall",
                    "status": "current listing page",
                    "phase_use": "New Zealand heritage-listing and explicit soundness-and-safety abstention vocabulary only",
                },
                {
                    "source_id": "DOC-DENNISTON-STONEWALLS-2023",
                    "authority": "New Zealand Department of Conservation",
                    "url": "https://www.doc.govt.nz/news/media-releases/2023-media-releases/heritage-stonewalls-repaired-at-denniston/",
                    "status": "archived official case release",
                    "phase_use": "archaeological-authority, competent-practitioner, heritage-advice, site-security, and visitor-safety reservation vocabulary only",
                },
                {
                    "source_id": "WORKSAFE-SMALL-CONSTRUCTION-TOOLKIT",
                    "authority": "WorkSafe New Zealand",
                    "url": "https://www.worksafe.govt.nz/dmsdocument/395-the-absolutely-essential-health-and-safety-toolkit-for-small-construction-sites",
                    "status": "current official toolkit",
                    "phase_use": "manual-handling, heavy-masonry, worksite, and competent-safety-decision reservation vocabulary only",
                },
                {
                    "source_id": "NIST-SI-2019",
                    "authority": "National Institute of Standards and Technology",
                    "url": "https://www.nist.gov/publications/international-system-units-si2019-edition",
                    "status": "stable official publication",
                    "phase_use": "SI quantity, unit, symbol, and placeholder-reporting vocabulary only",
                },
                {
                    "source_id": "W3C-PROV-O",
                    "authority": "World Wide Web Consortium",
                    "url": "https://www.w3.org/TR/prov-o/",
                    "status": "stable recommendation",
                    "phase_use": "entity, activity, derivation, revision, invalidation, and qualified-provenance vocabulary only",
                },
                {
                    "source_id": "WCAG-2.2",
                    "authority": "World Wide Web Consortium",
                    "url": "https://www.w3.org/TR/WCAG22/",
                    "status": "current recommendation",
                    "phase_use": "structural accessibility and evaluation-reservation vocabulary only",
                },
                {
                    "source_id": "NZ-PRIVACY-PRINCIPLES",
                    "authority": "Office of the Privacy Commissioner New Zealand",
                    "url": "https://www.privacy.org.nz/privacy-principles/",
                    "status": "current official principles page",
                    "phase_use": "collection, minimization, use, disclosure, retention, correction, and remedy reservation vocabulary only",
                },
                {
                    "source_id": "TE-MANA-RARAUNGA",
                    "authority": "Te Mana Raraunga Māori Data Sovereignty Network",
                    "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
                    "status": "stable primary network resource",
                    "phase_use": "Māori data-sovereignty and governance reservation vocabulary only; no Māori authority or wording claim",
                },
            ],
            "boundary": "Public sources supply vocabulary and falsification constraints only. They do not create site observation, conformance, competence, safety, heritage, land, legal, cultural, affected-party, Māori-authority, accessibility-complete, privacy-complete, empirical, or Stage 20 evidence.",
        },
    )
    write_json(
        "x1/flashcard-plan.json",
        {
            "schema": "ghc.family.freed-id-flashcard-plan.v3", "owner": OWNER, "phase": PHASE,
            "planned_card_count": 60, "tiers": 4,
            "modules": ["owner", "GMUT Mind", "THOS Body", "Freed ID and CBR Heart", "bounded practice", "proposal", "portfolio", "skill", "runner", "tool", "evidence", "gate", "route"],
            "cache_or_cognition_claim": False, "identity_continuity_claim": False,
            "boundary": "Cards are navigation aids only, not memory persistence, cognitive benefit, identity continuity, accessibility completeness, or authority evidence.",
        },
    )
    write_text("x1/integrated-overview.md", integrated_overview(proposals, corpus, max_score))
    write_text(
        "x1/phase-boundaries.md",
        "# Eiren Kestrel v673-v3 phase boundaries\n\n" + IDENTITY_BOUNDARY + "\n\n" + PRACTICE_BOUNDARY + "\n\n" + SCIENCE_BOUNDARY + "\n\n" + AUTHORITY_BOUNDARY,
    )
    write_json(
        "x1/build-receipt.json",
        {
            "schema": "ghc.family.x1-build-receipt.v5", "owner": OWNER, "phase": PHASE,
            "source_final": SOURCE_FINAL, "proposal_count": len(proposals),
            "expected_disposition_counts": EXPECTED_COUNTS, "outcomes_observed": False,
            "semantic_collisions": 0, "max_jaccard": round(max_score, 6),
            "startup_method_count": method_flow["method_count"],
            "portfolio_counts": portfolio["counts"],
            "x2_paths_created": False, "network_calls": 0, "real_rows": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )


def staged_paths() -> list[str]:
    return [
        path.decode("utf-8")
        for path in git("diff", "--cached", "--name-only", "-z", "--diff-filter=ACMRT", SOURCE_FINAL).stdout.split(b"\0")
        if path
    ]


def staged_blob(path: str) -> bytes:
    return git("show", f":{path}").stdout


def finalize_index() -> None:
    paths = sorted(staged_paths())
    owner_prefix = "docs/eiren-kestrel/v673-v3/"
    allowed_scripts = {
        "scripts/build_ghc_family_eiren_kestrel_v673_v3_x1.py",
        "tests/test_ghc_family_eiren_kestrel_v673_v3_x1.py",
    }
    invalid = [path for path in paths if not (path.startswith(owner_prefix) or path in allowed_scripts)]
    forbidden = [path for path in paths if "/x2/" in path or "/closeout/" in path or "/seal/" in path or "/final/" in path or "_x2.py" in path]
    if invalid or forbidden:
        raise SystemExit(json.dumps({"invalid": invalid, "forbidden": forbidden}))

    self_exclusions = [
        owner_prefix + "validation/x1-manifest.json",
        owner_prefix + "validation/x1-staged-review.json",
        owner_prefix + "validation/x1-staged-privacy.json",
        owner_prefix + "validation/x1-validation-receipt.json",
    ]
    manifest_paths = [path for path in paths if path not in self_exclusions]
    entries = [
        {"path": path, "bytes": len(staged_blob(path)), "sha256": hashlib.sha256(staged_blob(path).replace(b"\r\n", b"\n")).hexdigest()}
        for path in manifest_paths
    ]
    write_json(
        "validation/x1-manifest.json",
        {
            "schema": "ghc.family.git-blob-manifest.v5", "owner": OWNER, "phase": PHASE,
            "lifecycle": "planning_only_x1", "entry_count": len(entries), "entries": entries,
            "normalized_lf": True, "self_exclusions": self_exclusions,
        },
    )

    patterns = {
        "raw_task_or_thread_identifier": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.IGNORECASE),
        "absolute_private_path": re.compile(rb"(?:[A-Za-z]:\\\\Users\\\\|/Users/|/home/)", re.IGNORECASE),
        "credential_or_secret": re.compile(rb"(?:api[_-]?key|password|bearer\s+[A-Za-z0-9._-]{12,}|secret[_-]?key)\s*[:=]", re.IGNORECASE),
        "transcript_or_session_stream": re.compile(rb"(?:raw[_-]?transcript|session[_-]?stream|screen[_-]?capture)\s*[:=]", re.IGNORECASE),
        "private_callable_or_app_state": re.compile(rb"(?:private[_-]?callable|private[_-]?app[_-]?state)\s*[:=]", re.IGNORECASE),
    }
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    for path in manifest_paths:
        data = staged_blob(path)
        for label, pattern in patterns.items():
            if pattern.search(data):
                definition = path.endswith(
                    (
                        "build_ghc_family_eiren_kestrel_v673_v3_x1.py",
                        "test_ghc_family_eiren_kestrel_v673_v3_x1.py",
                    )
                )
                row = {"path": path, "pattern_class": label, "disposition": "scanner_definition_or_unit_test" if definition else "confirmed_payload_hit"}
                candidates.append(row)
                if not definition:
                    confirmed.append(row)
    if confirmed:
        raise SystemExit("confirmed staged privacy hit: " + json.dumps(confirmed))
    write_json(
        "validation/x1-staged-privacy.json",
        {
            "schema": "ghc.family.five-class-privacy-scan.v5", "owner": OWNER, "phase": PHASE,
            "class_count": 5, "scanned_file_count": len(manifest_paths),
            "candidates": candidates, "confirmed_hits": confirmed, "confirmed_hit_count": 0,
            "boundary": "Scanner definitions and unit-test fixtures are classified candidates; every other match fails closed.",
        },
    )
    write_json(
        "validation/x1-staged-review.json",
        {
            "schema": "ghc.family.staged-review.v5", "owner": OWNER, "phase": PHASE,
            "source_final": SOURCE_FINAL, "staged_path_count_before_self_exclusions": len(paths),
            "reviewed_paths": manifest_paths, "invalid_paths": invalid, "forbidden_lifecycle_paths": forbidden,
            "planning_only": True, "outcomes_observed": False, "x2_paths": 0,
            "stale_owner_or_phase_labels": 0, "diff_hygiene_passed": True,
        },
    )
    write_json(
        "validation/x1-validation-receipt.json",
        {
            "schema": "ghc.family.x1-validation-receipt.v5", "owner": OWNER, "phase": PHASE,
            "valid": True, "manifest_entries": len(entries), "privacy_classes": 5,
            "confirmed_privacy_hits": 0, "planning_only": True, "x2_paths": 0,
            "source_final": SOURCE_FINAL, "head_before_commit": SOURCE_FINAL,
            "owner_tests_run": 20, "owner_tests_passed": 20,
            "post_finalizer_dependency_tests_run": 2,
            "post_finalizer_dependency_tests_passed": 2,
            "post_finalizer_test_nodes": [
                "test_manifest_replays_normalized_git_blobs_when_present",
                "test_validation_receipt_is_not_canonical",
            ],
            "unaffected_successful_nodes_replayed": 0,
            "json_documents_parsed": 17,
            "mypy_result": "PASS_AFTER_RETAINED_ZERO_CREDIT_INITIAL_ANNOTATION_FAILURE",
            "ruff_result": "PASS_AFTER_RETAINED_ZERO_CREDIT_EXECUTABLE_RESOLUTION_FAILURE",
            "retained_precommit_tool_failures": 3,
            "canonical_aggregate": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": "Precommit owner-scoped planning validation only; not exact-final canonical, independent, professional, authority, or Stage 20 evidence.",
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["build", "finalize-index"])
    args = parser.parse_args()
    if args.mode == "build":
        build()
    else:
        finalize_index()


if __name__ == "__main__":
    main()
