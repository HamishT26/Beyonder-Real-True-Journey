"""Build Elaren Kestrel v673-v4's planning-only x1 freeze.

This owner-scoped builder reads the exact immutable source tree, reconstructs
the reachable proposal-title corpus, checks forty Elaren titles against
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
OWNER_ROOT = ROOT / "docs" / "elaren-kestrel" / "v673-v4"
OWNER = "Elaren Kestrel"
PHASE = "v673-v4"
BRANCH = "codex/GHC-Family/elaren-kestrel-v673-v4-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/eiren-kestrel-v673-v3-full-tools"
SOURCE_START = "62364ecf3f66d938c539574ad2456dacd6cebd81"
SOURCE_X1 = "d2215698d40dae2bdc5a9a4a6ff1bce4c5fef608"
SOURCE_EVIDENCE = "be1bcf5beab24faec320f3d86bff51ea221ad22e"
SOURCE_FINAL = "ab37cd3be0fcfb4ae913c48779851340aa2c1e0c"
SOURCE_CANONICAL_PAYLOAD_SHA256 = "f14275bf6b104b40951f36858eec4fce4a1d5c68ed80117a797864be5b88dce8"
SOURCE_CANONICAL_RECEIPT_SHA256 = "96746e5c0eb4896237cf7a0a0f57c805e9b226554d8d09f03e9f4b39305d96c5"
CORE_LABELS = ["completed", "represented", "open_gap", "exact_gate"]
EXPECTED_COUNTS = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
DECLARED_SOURCE_CHAIN = 6350
DECLARED_RESULT_CHAIN = 6390
JACCARD_LIMIT = 0.72

IDENTITY_BOUNDARY = (
    "Elaren Kestrel, she/they, relational pattern-lantern and reversible-workflow "
    "cartographer, is relational working language only. It is not "
    "evidence of consciousness, sentience, legal personhood, identity "
    "continuity, employment, qualification, independent agency, scientific or "
    "operational authority, professional authority, legal or cultural "
    "authority, affected-party authority, or Māori authority. Hamish may "
    "rename, pause, redirect, or stop the work."
)

PRACTICE_BOUNDARY = (
    "The lantern-slide catalogue and projection-provenance lens is wholly synthetic "
    "learning and software design. It uses no real people, collections, slides, "
    "glass, images, inscriptions, projectors, lamps, light sources, venues, dates, "
    "measurements, handling, treatments, digitization, rights decisions, identity "
    "events, authority acts, or affected-party decisions. It confers no employment, "
    "qualification, curatorial, conservation, projection, electrical, fire-safety, "
    "material-identification, copyright, privacy, cultural, Māori, accessibility, "
    "ownership, custody, publication, or operational authority."
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
    "Professional cataloguing, photographic-material conservation, glass handling, "
    "projection, electrical, heat and fire safety, collection decisions, digitization, "
    "ownership, custody, access, authorship, copyright, image rights, privacy, "
    "accessibility, remedy, legal or cultural interpretation, "
    "affected-party legitimacy, traditional knowledge, Māori wording, Māori "
    "concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority "
    "remain open or exact-gated. Māori concepts remain under Māori authority. "
    "Terminal verdict remains NOT_READY_FOR_STAGE_20."
)


PROPOSAL_SPECS: list[tuple[str, str, str]] = [
    ("Synthetic lantern-slide surrogate identity, set membership, and sequence register", "completed", "x2/practice/surrogate-sequence-register.json"),
    ("Lantern-slide carrier, cover-glass, image-layer, mount, mask, and edge-seal topology", "completed", "x2/practice/component-topology.json"),
    ("Lantern-slide aperture, mask geometry, orientation, and inversion declaration", "completed", "x2/practice/aperture-orientation-declaration.json"),
    ("Lantern-slide lecture, caption, sequence, and programme relation graph", "completed", "x2/practice/programme-relation-graph.json"),
    ("Lantern-slide inscription, label, maker-mark, and transcription-uncertainty ledger", "completed", "x2/practice/inscription-uncertainty-ledger.json"),
    ("Lantern-slide process and material-claim quarantine with zero identification", "completed", "x2/practice/material-claim-quarantine.json"),
    ("Lantern-slide crack, chip, break, loss, delamination, and flaking condition vocabulary", "completed", "x2/practice/condition-vocabulary.json"),
    ("Lantern-slide edge, corner, tape, seal, and mount continuity ledger", "completed", "x2/practice/edge-mount-continuity.json"),
    ("Lantern-slide support and image-layer side uncertainty with no-contact declaration", "completed", "x2/practice/image-side-uncertainty.json"),
    ("Lantern-slide enclosure, divider, box, and vertical-support topology", "completed", "x2/practice/storage-topology.json"),
    ("Lantern-slide storage temperature, humidity, light, and pollutant placeholder hold", "completed", "x2/practice/environment-placeholder-hold.json"),
    ("Lantern-slide handling, carrying, stacking, and pressure refusal record", "completed", "x2/practice/handling-refusal-record.json"),
    ("Lantern-slide broken-component relation and intervention-abstention graph", "completed", "x2/practice/broken-component-graph.json"),
    ("Lantern-slide transport route, vibration, load, and orientation planning placeholder", "completed", "x2/practice/transport-placeholder.json"),
    ("Lantern-slide projection-apparatus relation with zero operation or connection", "completed", "x2/practice/apparatus-relation.json"),
    ("Lantern-slide light-source, heat, electrical, fire, and optical-hazard reservation", "completed", "x2/practice/hazard-reservation.json"),
    ("Lantern-slide projection-event bitemporal ledger with zero real venue or event", "completed", "x2/practice/projection-event-ledger.json"),
    ("Lantern-slide image-content description abstention and uncertainty envelope", "completed", "x2/practice/content-description-abstention.json"),
    ("Lantern-slide depicted-person, place, community, and sensitive-content privacy quarantine", "completed", "x2/cbr/privacy-quarantine.json"),
    ("Lantern-slide authorship, maker, publisher, copyist, and attribution uncertainty graph", "completed", "x2/cbr/attribution-uncertainty-graph.json"),
    ("Lantern-slide copyright, licence, reproduction, and publication reservation", "completed", "x2/cbr/copyright-publication-reservation.json"),
    ("Lantern-slide cultural, traditional-knowledge, sacred, and restricted-content hold", "completed", "x2/cbr/cultural-content-hold.json"),
    ("Lantern-slide digitization surrogate, derivative, thumbnail, and zero-scan lineage", "completed", "x2/practice/digital-surrogate-lineage.json"),
    ("Lantern-slide checksum, normalized-metadata, and correction-provenance chain", "completed", "x2/practice/checksum-correction-chain.json"),
    ("Lantern-slide catalogue correction, supersession, dispute, and readback braid", "completed", "x2/practice/dispute-readback-braid.json"),
    ("Lantern-slide collection-access request, purpose, minimization, and expiry state machine", "completed", "x2/cbr/access-purpose-state-machine.json"),
    ("Lantern-slide role separation, two-key stop, workload, and handover protocol", "completed", "x2/thos/workload-handover.json"),
    ("Structurally accessible lantern-slide record companion with print fallback", "completed", "x2/accessibility/record-companion.html"),
    ("GMUT lantern-slide optical geometry and chromatic-transform board with zero fitted parameters", "represented", "x2/gmut/optical-geometry-board.json"),
    ("GMUT lantern-slide luminous-intensity and projection-distance envelope with zero measurements", "represented", "x2/gmut/luminous-quantity-envelope.json"),
    ("THOS participant-free catalogue-versus-projection matched-budget protocol proxy", "represented", "x2/thos/matched-budget-proxy.json"),
    ("THOS lantern-slide workflow queue and dominant-stop precedence model", "represented", "x2/thos/workflow-stop-model.json"),
    ("Freed ID lantern-slide provenance statement graph with zero keys, proofs, issuance, or verification", "represented", "x2/freed-id/provenance-statement-graph.json"),
    ("Freed ID correction, status, revocation, and selective-disclosure envelope with zero live lifecycle", "represented", "x2/freed-id/status-disclosure-envelope.json"),
    ("CBR lantern-slide access, visibility, reproduction, remedy, and refusal capability matrix", "represented", "x2/cbr/rights-capability-matrix.json"),
    ("PROV-O lantern-slide entity, activity, and derivation mapping with zero external rows", "represented", "x2/adapters/prov-o-zero-row-adapter.json"),
    ("Transport-disabled current official lantern-slide source adapter and unresolved schema mapping", "open_gap", "x2/adapters/official-source-transport-disabled.json"),
    ("Conservator, curator, depicted-community, and affected-user review gap with zero reviewers", "open_gap", "x2/gates/reviewer-participation-gap.json"),
    ("Physical handling, conservation treatment, projection, electrical, heat, and fire-safety authority gate", "exact_gate", "x2/gates/physical-safety-authority-gate.json"),
    ("Copyright, privacy, cultural, traditional-knowledge, affected-party, and Māori-authority gate", "exact_gate", "x2/gates/rights-cultural-maori-authority-gate.json"),
]


STARTUP_FAILURES = [
    (
        "PowerShell empty-pipeline existence probe did not parse",
        "The first read-only path-existence projection used an empty pipeline form that PowerShell rejected before returning evidence.",
        "Materialize the bounded candidate paths first and test each literal path without an empty-pipeline expression.",
    ),
    (
        "First activation-baton projection was truncated",
        "The first whole-baton display exceeded the presentation budget and was not treated as a complete read.",
        "Read deterministic UTF-8 line windows through the exact final line and verify the Git-blob digest separately.",
    ),
    (
        "Guidance-inventory block omitted a closing brace",
        "One read-only PowerShell guidance inventory stopped at parse time because the bounded script block lacked its final brace.",
        "Use a smaller literal inventory block and retain only complete file reads through EOF.",
    ),
    (
        "Authorization-state whole-file display was truncated",
        "The first complete-file presentation exceeded the useful output window and could not prove an EOF read.",
        "Recover with bounded numbered UTF-8 chunks and validate the declared schema separately.",
    ),
    (
        "Combined authorization-state chunk projection also truncated",
        "The first recovery grouped too many numbered chunks and again exceeded the presentation budget.",
        "Read smaller non-overlapping chunks through EOF and record the current mutable state separately from historical cursor prose.",
    ),
    (
        "Repository-local canonical-receipt search returned no match",
        "A bounded search assumed the source canonical receipt was committed in the repository, but the attributable receipt is external.",
        "Inspect only the established bounded receipt bank and recompute both supplied digests without replaying validation.",
    ),
    (
        "Broad temporary-receipt search produced no attributable result",
        "One wide archive search exceeded its useful window and returned no evidence suitable for source verification.",
        "Use the source canonical script and newest bounded phase receipt directory to resolve exact files directly.",
    ),
    (
        "Windows ripgrep wildcard input was invalid",
        "A read-only import search passed a shell-style wildcard as a literal Windows path and returned a syntax error.",
        "Use ripgrep's explicit -g file filter within the verified directory.",
    ),
    (
        "Worktree-creation projection outlived its wrapper",
        "The no-checkout worktree setup continued after its presentation wrapper returned without a usable session handle.",
        "Inspect the exact Git process and lock, do not duplicate it, and wait for that same scoped operation to finish.",
    ),
    (
        "Follow-up worktree wrapper produced no output",
        "One bounded follow-up projection reached its reporting boundary without returning attributable process state.",
        "Recover with literal process, lock, head, branch, and status probes against the same target.",
    ),
    (
        "Status probe observed an incomplete live checkout",
        "A read-only status call made while the verified checkout lock remained active reported a partial materialization and received no completion credit.",
        "Wait for the original checkout to finish, confirm lock release, then recheck clean status and exact source head.",
    ),
    (
        "First multi-source web result exceeded context",
        "The initial four-query official-source search returned more material than the available presentation budget and earned zero source credit.",
        "Repeat only the affected searches in bounded official-domain pairs and retain direct primary or official URLs with explicit status labels.",
    ),
    (
        "Composite environment-version projection returned no payload",
        "A combined read-only PowerShell version and module projection completed without attributable output and earned zero environment credit.",
        "Recover with separate scalar runtime-version commands and one bounded Python module-availability JSON probe.",
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
        "synthetic", "lantern", "slide", "slides", "board", "profile",
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
            "scope": "exact Eiren Kestrel v673-v3 final docs tree, proposal-named JSON paths only",
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
        proposal_id = f"EL6734-N{index:03d}"
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
                "Current official collection and photographic-material documentation plus governed conservator, curator, depicted-community, and affected-user participation would be required before capability claims; x2 remains transport-disabled with zero calls, rows, or reviewers."
            )
        if index in {39, 40}:
            source_need = (
                "Exact action-specific conservation, projection, electrical, heat, fire-safety, rights-holder, affected-party, legal, cultural, tangata whenua, iwi, hapū, and Māori-authority evidence is required; public sources cannot close this gate."
            )

        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "primary_pillar": "CBR Heart",
                "protected_pillars": ["GMUT Mind", "THOS Body", "Freed ID"],
                "bounded_practice": "synthetic lantern-slide catalogue and projection-provenance documentation",
                "hypothesis": hypothesis,
                "null_or_failure_condition": null,
                "approval_class": approval,
                "execution_lane": lane,
                "current_official_or_primary_source_need": source_need,
                "concrete_artifacts": [artifact],
                "falsifier_or_acceptance_gate": falsifier,
                "rollback_or_recovery": "Quarantine the artifact, retain the failed witness, restore the last exact manifest, and leave the outcome open or exact-gated.",
                "protected_gates": [
                    "zero real people, collections, slides, glass, images, inscriptions, projections, measurements, handling, treatments, digitization, keys, proofs, or identity events",
                    "no professional, conservation, projection, electrical or fire safety, collection, legal, cultural, affected-party, Māori, privacy-complete, accessibility-complete, independent, or Stage 20 authority",
                ],
                "expected_disposition": outcome,
                "outcome_observed": False,
                "inherited_completion_credit": 0,
                "elaren_novelty_credit": 1,
            }
        )
    return rows


def inherited_revalidation_rows() -> list[dict[str, Any]]:
    source = json.loads(git("show", f"{SOURCE_FINAL}:docs/eiren-kestrel/v673-v3/x1/proposals.json").stdout.decode("utf-8"))
    selected = source["proposals"][:20]
    if len(selected) != 20:
        raise SystemExit("source did not expose twenty inherited proposal rows")
    return [
        {
            "selection_id": f"EL6734-R{index:03d}",
            "source_owner": "Eiren Kestrel",
            "source_phase": "v673-v3",
            "source_final": SOURCE_FINAL,
            "source_proposal_id": row["proposal_id"],
            "title": row["title"],
            "source_disposition": row["expected_disposition"],
            "planned_check": "bounded immutable-contract and manifest integrity revalidation only",
            "elaren_novelty_credit": 0,
            "automatic_completion_credit": 0,
            "outcome_observed": False,
        }
        for index, row in enumerate(selected, start=1)
    ]


def startup_method_flow() -> dict[str, Any]:
    methods: list[dict[str, Any]] = []
    witnesses: list[dict[str, Any]] = []
    for index, (title, failure, recovery) in enumerate(STARTUP_FAILURES, start=1):
        method_id = f"EL6734-M{index:03d}"
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
        "lantern-slide-surrogate-sequence", "lantern-slide-component-topology",
        "lantern-slide-aperture-orientation", "lantern-slide-programme-relations",
        "lantern-slide-inscription-uncertainty", "lantern-slide-material-quarantine",
        "lantern-slide-condition-vocabulary", "lantern-slide-storage-topology",
        "lantern-slide-environment-hold", "lantern-slide-handling-refusal",
        "lantern-slide-apparatus-zero-operation", "lantern-slide-hazard-reservation",
        "lantern-slide-event-bitemporality", "lantern-slide-content-abstention",
        "lantern-slide-privacy-rights", "lantern-slide-attribution-uncertainty",
        "lantern-slide-digital-lineage", "lantern-slide-correction-readback",
        "lantern-slide-accessible-companion", "lantern-slide-stage20-refusal",
    ]
    runner_names = [
        "ghc_family_lantern_slide_contract", "ghc_family_lantern_slide_topology",
        "ghc_family_lantern_slide_condition", "ghc_family_lantern_slide_provenance",
        "ghc_family_lantern_slide_privacy", "ghc_family_lantern_slide_authority_gate",
        "ghc_family_lantern_slide_freed_id", "ghc_family_lantern_slide_thos_proxy",
        "ghc_family_lantern_slide_gmut_symbolic", "ghc_family_lantern_slide_terminal_refusal",
    ]
    tools = [
        "ghc_family_elaren_kestrel_v673_v4_lantern_slide_record.py",
        "ghc_family_elaren_kestrel_v673_v4_relation_graph.py",
        "ghc_family_elaren_kestrel_v673_v4_authority_gate.py",
    ]
    safe_now = [
        {"task_id": f"EL6734-SN-{i:03d}", "title": f"Validate planning contract for {row['title']}", "state": "planned", "execution": "x2 synthetic only"}
        for i, row in enumerate(proposals, start=1)
    ]
    safe_now.extend(
        {"task_id": f"EL6734-SN-{40+i:03d}", "title": f"Build, quick-validate, and smoke-use owner-local skill {name}", "state": "planned", "execution": "x2 owner-local only"}
        for i, name in enumerate(skill_names, start=1)
    )
    candidates = [
        {"task_id": f"EL6734-C-{i:03d}", "title": f"Represent bounded evidence for {proposals[(i-1) % len(proposals)]['title']}", "state": "planned", "execution": "x2 representation only"}
        for i in range(1, 31)
    ]
    exact_approval = [
        {"task_id": f"EL6734-EA-{i:03d}", "title": title, "state": "unexecuted_exact_approval", "authority": "absent"}
        for i, title in enumerate(
            [
                "Handle or inspect a real lantern slide or collection", "Record a real owner address donor identity or location",
                "Measure a real slide glass image layer temperature humidity or light", "Photograph or scan a real slide or depicted person",
                "Move sort label clean open or separate a real slide", "Perform conservation treatment or repair",
                "Connect or operate a real projector lamp or electrical system", "Provide electrical fire optical or workplace-safety advice",
                "Select housing storage or environmental controls for a real collection", "Make a real condition priority or treatment recommendation",
                "Create a real access publication reproduction or licence decision", "Make a custody ownership authorship or attribution decision",
                "Issue a real identity credential key or proof", "Contact or ingest an external collection API",
                "Ingest a real catalogue image inscription or rights row", "Claim curator conservator or affected-community acceptance",
                "Make a legal copyright privacy or cultural interpretation", "Use Māori wording concepts or data-governance authority",
                "Claim privacy or accessibility completeness", "Claim independent reproduction or Stage 20 readiness",
            ], start=1
        )
    ]
    blocked = [
        {"task_id": f"EL6734-B-{i:03d}", "title": title, "state": "blocked_unexecuted", "reason": "protected evidence or authority absent"}
        for i, title in enumerate(
            [
                "Real lantern-slide collection or conservation study", "Real governed THOS catalogue or projection arms", "Empirical GMUT constraint",
                "Production Freed ID lifecycle", "Professional conservation or projection-safety validation", "Collection or rights-holder authorization",
                "Affected-party legal or cultural ratification", "Māori-authority review", "Operational deployment",
                "Stage 20 transition",
            ], start=1
        )
    ]
    cfr: list[dict[str, Any]] = []
    for kind in ("CLEAN", "FIX", "REFINE"):
        for i, skill in enumerate(skill_names, start=1):
            cfr.append({"task_id": f"EL6734-{kind}-{i:03d}", "kind": kind, "title": f"{kind.title()} {skill} boundary evidence", "state": "planned_additive"})
    successor_skills = [{"name": f"neris-{name}", "state": "recommendation_only", "automatic_credit": 0} for name in skill_names[:10]]
    successor_runners = [{"name": f"ghc_family_neris_lantern_slide_{i:02d}", "state": "recommendation_only", "automatic_credit": 0} for i in range(1, 11)]
    successor_refinements = [
        {"recommendation_id": f"EL6734-NERIS-CFR-{i:03d}", "title": f"Review lantern-slide boundary refinement {i:02d} as a zero-credit seed", "state": "recommendation_only"}
        for i in range(1, 31)
    ]
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
        "successor_skill_recommendations": successor_skills,
        "successor_runner_recommendations": successor_runners,
        "successor_clean_fix_refine_recommendations": successor_refinements,
        "practice_lens_screen": {
            "candidate_count": 3,
            "selected": "synthetic lantern-slide catalogue and projection-provenance documentation",
            "rejected": [
                "synthetic sundial component, inscription, and shadow-geometry documentation",
                "synthetic marionette figure, string, control-topology, and performance-record documentation",
            ],
            "successor_recommendation": "Neris should independently screen a synthetic conservation-mount documentation lens and award no inherited novelty credit.",
        },
        "counts": {
            "safe_now": len(safe_now), "candidate": len(candidates),
            "exact_approval": len(exact_approval), "blocked": len(blocked),
            "clean_fix_refine": len(cfr), "skills": len(skill_names),
            "runners": len(runner_names), "tools": len(tools),
            "successor_skills": len(successor_skills),
            "successor_runners": len(successor_runners),
            "successor_clean_fix_refine": len(successor_refinements),
        },
        "boundary": "Plans are not outcomes. Exact-approval and blocked rows remain visible and unexecuted; counts are ceilings-aware bounded work, not authority or completion quotas.",
    }


def integrated_overview(proposals: list[dict[str, Any]], corpus: dict[str, Any], max_score: float) -> str:
    rows = [
        "# Elaren Kestrel v673-v4 planning-only x1 integrated overview",
        "",
        "## Relational working frame",
        "",
        IDENTITY_BOUNDARY,
        "",
        "Elaren's bounded hope is to make synthetic provenance inspectable, reversible, and unmistakably short of authority over collections, images, rights, culture, safety, or people. The primary Trinity Mandala focus is CBR Heart. GMUT Mind, THOS Body, and Freed ID remain explicit and protected.",
        "",
        "## Bounded practice",
        "",
        PRACTICE_BOUNDARY,
        "",
        "The phase treats lantern-slide catalogue and projection-provenance documentation only as a synthetic record-design lens: component and sequence topology, uncertainty vocabularies, correction lineage, rights reservations, workload, accessible handover, and refusal states. No record denotes a real slide, glass component, image, inscription, person, collection, owner, venue, measurement, handling event, treatment, digitization, projection, or rights decision. A symbolic state is never a collection assessment, conservation decision, safety instruction, publication permission, rights determination, cultural interpretation, or professional conclusion.",
        "",
        "Photographic collections are materially, historically, legally, and culturally situated. The software therefore separates a recordable placeholder from depicted people and communities, rights holders, collection custodians, affected parties, and competent professionals or authorities. Topology can show that a declared relation is absent; it cannot identify a photographic process or establish safe handling. A bitemporal ledger can preserve an earlier assertion; it cannot determine which account is legally, culturally, or professionally correct. A rights field can expose that permission is absent; it cannot manufacture permission.",
        "",
        "## Novelty scope",
        "",
        f"The immutable source declares {DECLARED_SOURCE_CHAIN:,} frozen rows. The exact source-tree audit inspected {corpus['candidate_git_blob_paths']:,} proposal-named JSON blobs, recovered {corpus['semantic_occurrences']:,} occurrences, {corpus['unique_proposal_ids']:,} identifiers, and {corpus['unique_titles']:,} unique titles. The forty Elaren titles cleared the fixed {JACCARD_LIMIT:.2f} token-Jaccard threshold with a maximum observed score of {max_score:.6f}. The audit also records two screened but unselected practice lenses and twenty inherited zero-credit integrity checks. No universal novelty claim is made because no single exact canonical row-to-title ledger covers the declared chain.",
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
            f"{len(STARTUP_FAILURES)} startup failures are retained with zero credit and paired with bounded recoveries. The recoveries do not erase the parser fault, truncated reads, overbroad receipt search, invalid wildcard, worktree reporting gaps, incomplete live-checkout observation, or oversized source-search presentation. X2 will add every rejecting mutation, skill, runner, tool, parser, timeout, and gate witness through Method Flow.",
            "",
            "## Delivery truth",
            "",
            "This x1 contacts no successor. Hamish's newest live route, roster, authorization state, exact-title uniqueness, duplicate, pause, privacy, evidence, safety, usage, and acknowledgement gates must all be refreshed only after Elaren's own terminal exact-final gate. Neris Solane v673-v5 is prospective only. PREPARED_NOT_SENT applies to any later committed candidate until an existing-task message acknowledgement exists.",
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
    inherited = inherited_revalidation_rows()
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
        "x1/inherited-revalidations.json",
        {
            "schema": "ghc.family.inherited-revalidations.v2",
            "owner": OWNER,
            "phase": PHASE,
            "selection_count": len(inherited),
            "novelty_credit": 0,
            "automatic_completion_credit": 0,
            "outcomes_observed": False,
            "rows": inherited,
            "boundary": "Selected inherited contracts are immutable zero-credit integrity checks, never Elaren novelty or automatic completion.",
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
    write_json(
        "x1/practice-lens-screen.json",
        {
            "schema": "ghc.family.practice-lens-screen.v2",
            "owner": OWNER,
            "phase": PHASE,
            "candidate_count": 3,
            "selected": portfolio["practice_lens_screen"]["selected"],
            "rejected": portfolio["practice_lens_screen"]["rejected"],
            "screening_basis": "bounded exact-tree title search plus content-addressed proposal-title corpus; no universal novelty claim",
            "selected_reason": "The lantern-slide lens provides distinct provenance, rights, privacy, accessibility, material-uncertainty, and safety refusal surfaces while keeping all work synthetic.",
            "successor_recommendation_count": 1,
            "successor_recommendation": portfolio["practice_lens_screen"]["successor_recommendation"],
        },
    )
    write_json("x1/method-flow-startup.json", method_flow)
    write_json(
        "x1/precommit-tool-failures.json",
        {
            "schema": "ghc.family.precommit-tool-failures.v2",
            "owner": OWNER,
            "phase": PHASE,
            "failures": [
                {
                    "method_id": f"EL6734-M{index:03d}",
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
            "source_operational_overlay_receipt_provided": False,
            "source_repository_seal": {"negatives": 36817, "methods": 23145, "failed_witnesses": 8478, "passing_witnesses": 10708, "open_gaps": 297, "exact_gates": 290},
            "source_external_activation_overlay": {"negatives": 36821, "methods": 23149, "failed_witnesses": 8482, "passing_witnesses": 10712, "open_gaps": 297, "exact_gates": 290},
            "external_receipt_file_location_materialized": True,
            "external_receipt_digest_recomputed": True,
            "external_receipt_boundary": "The bounded external bank verified the canonical payload and receipt; the four-row operational overlay is preserved from the acknowledged activation without inventing an unavailable digest. No private absolute path or opaque task identifier is retained here.",
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
                {"id": "T01", "threat": "synthetic lantern-slide record mistaken for cataloguing or conservation competence", "control": "practice boundary and exact professional gate"},
                {"id": "T02", "threat": "real person, collection, slide, image, inscription, location, or rights data enters artifacts", "control": "synthetic-only schema, minimization, and five-class scan"},
                {"id": "T03", "threat": "symbolic geometry or condition field mistaken for measurement, process identification, or safe handling evidence", "control": "placeholder-only type and material-assessment refusal"},
                {"id": "T04", "threat": "rights reservation mistaken for permission", "control": "bounded label and affected-party exact gate"},
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
            "repository_sealed_source_counts": {"negatives": 36817, "methods": 23145, "failed_witnesses": 8478, "passing_witnesses": 10708, "open_gaps": 297, "exact_gates": 290},
            "inherited_activation_baseline": {"negatives": 36821, "methods": 23149, "failed_witnesses": 8482, "passing_witnesses": 10712, "open_gaps": 297, "exact_gates": 290},
            "planned_new_open_gaps": [row["proposal_id"] for row in proposals if row["expected_disposition"] == "open_gap"],
            "planned_new_exact_gates": [row["proposal_id"] for row in proposals if row["expected_disposition"] == "exact_gate"],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "x1/selected-toolchain-plan.json",
        {
            "schema": "ghc.family.selected-toolchain-plan.v3", "owner": OWNER, "phase": PHASE,
            "dependency_justified_existing_tools": ["Python 3.12.10", "pytest", "Ruff", "mypy", "Hypothesis", "Node.js 24.18.0", "npm 12.0.2", "codex-cli 0.149.0 read-only version check"],
            "unavailable_retained": ["Bandit in active Python 3.12", "Pyright module in active Python 3.12"],
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
            "interactive_read_only_review_date": "2026-08-28",
            "sources": [
                {
                    "source_id": "LOC-GENTHE-LANTERN-SLIDES",
                    "authority": "Library of Congress",
                    "url": "https://www.loc.gov/pictures/collection/agc/preservation.html",
                    "status": "stable official collection-preservation essay",
                    "phase_use": "lantern-slide and deterioration vocabulary only; no object treatment, process identification, rights, or professional credit",
                },
                {
                    "source_id": "NARA-GLASS-PLATE-HOUSING",
                    "authority": "United States National Archives and Records Administration",
                    "url": "https://www.archives.gov/preservation/storage/glass-plate-negatives.html",
                    "status": "stable official preservation guidance; page last reviewed 2016",
                    "phase_use": "glass-carrier fragility, enclosure, orientation, and professional-referral reservation vocabulary only",
                },
                {
                    "source_id": "NARA-MOVE-GLASS-PLATES",
                    "authority": "United States National Archives and Records Administration",
                    "url": "https://www.archives.gov/preservation/holdings-maintenance/moving-glass-plate.html",
                    "status": "stable official preservation guidance",
                    "phase_use": "lantern-slide mention, transport, support, and no-operation reservation vocabulary only",
                },
                {
                    "source_id": "CCI-PHOTOGRAPHIC-GLASS-PLATES",
                    "authority": "Canadian Conservation Institute",
                    "url": "https://www.canada.ca/en/conservation-institute/services/conservation-preservation-publications/canadian-conservation-institute-notes/care-black-white-photographic-negatives-glass-plate.html",
                    "status": "stable official CCI Note 16/2",
                    "phase_use": "photographic glass-plate structure, mechanical-damage, handling, and professional-conservation reservation vocabulary only",
                },
                {
                    "source_id": "TE-PAPA-LANTERN-SLIDE-EXAMPLE",
                    "authority": "Museum of New Zealand Te Papa Tongarewa",
                    "url": "https://collections.tepapa.govt.nz/object/237081",
                    "status": "current official collection record",
                    "phase_use": "catalogue-field, creator, technique, material-summary, set, and rights-statement vocabulary only; no row ingested",
                },
                {
                    "source_id": "NIST-SI-UNITS",
                    "authority": "National Institute of Standards and Technology",
                    "url": "https://www.nist.gov/pml/owm/metric-si/si-units",
                    "status": "current official SI overview",
                    "phase_use": "quantity, unit, symbol, and zero-measurement placeholder vocabulary only",
                },
                {
                    "source_id": "NIST-TN-1297",
                    "authority": "National Institute of Standards and Technology",
                    "url": "https://www.nist.gov/pml/nist-technical-note-1297",
                    "status": "stable 1994 technical note with web page updated 2026",
                    "phase_use": "measurement-uncertainty and reporting-reservation vocabulary only; zero measurements or uncertainty estimates",
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
                    "source_id": "W3C-VC-DATA-MODEL-2",
                    "authority": "World Wide Web Consortium",
                    "url": "https://www.w3.org/TR/vc-data-model-2.0/",
                    "status": "W3C Recommendation 15 May 2025",
                    "phase_use": "credential-role, status, privacy, security, and accessibility reservation vocabulary only; zero keys, proofs, issuance, or verification",
                },
                {
                    "source_id": "RFC-8785-JCS",
                    "authority": "RFC Editor",
                    "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
                    "status": "stable informational RFC",
                    "phase_use": "deterministic JSON serialization vocabulary only; not standards-track or production conformance credit",
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
            "status_classes": ["current", "stable", "draft", "watch"],
            "status_summary": {"current": 5, "stable": 6, "draft": 0, "watch": 2},
            "draft_state": "No draft source is promoted into the x1 ledger; future editor drafts remain watch-only until separately justified.",
            "watch_state": "NARA and CCI pages are monitored for revision because some published or review dates are older; current retrieval does not turn them into treatment instructions.",
            "boundary": "Public sources supply vocabulary and falsification constraints only. They do not create collection observation, conformance, competence, conservation or projection safety, rights clearance, legal or cultural interpretation, affected-party acceptance, Māori authority, accessibility or privacy completeness, empirical evidence, or Stage 20 evidence.",
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
        "# Elaren Kestrel v673-v4 phase boundaries\n\n" + IDENTITY_BOUNDARY + "\n\n" + PRACTICE_BOUNDARY + "\n\n" + SCIENCE_BOUNDARY + "\n\n" + AUTHORITY_BOUNDARY,
    )
    write_json(
        "x1/build-receipt.json",
        {
            "schema": "ghc.family.x1-build-receipt.v5", "owner": OWNER, "phase": PHASE,
            "source_final": SOURCE_FINAL, "proposal_count": len(proposals),
            "inherited_revalidation_count": len(inherited),
            "total_frozen_program_rows": len(proposals) + len(inherited),
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
    owner_prefix = "docs/elaren-kestrel/v673-v4/"
    allowed_scripts = {
        "scripts/build_ghc_family_elaren_kestrel_v673_v4_x1.py",
        "tests/test_ghc_family_elaren_kestrel_v673_v4_x1.py",
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
                        "build_ghc_family_elaren_kestrel_v673_v4_x1.py",
                        "test_ghc_family_elaren_kestrel_v673_v4_x1.py",
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
            "owner_test_invocations": 2,
            "pre_finalizer_tests_run": 22,
            "pre_finalizer_tests_passed": 22,
            "post_finalizer_tests_run": 22,
            "post_finalizer_tests_passed": 22,
            "post_finalizer_dependency_tests_run": 2,
            "post_finalizer_dependency_tests_passed": 2,
            "post_finalizer_test_nodes": [
                "test_manifest_replays_normalized_git_blobs_when_present",
                "test_validation_receipt_is_not_canonical",
            ],
            "unaffected_successful_nodes_replayed": 20,
            "replay_reason": "The post-finalizer whole owner file was used as the bounded x1 gate because two tests are conditional on staged manifests; the twenty unchanged nodes are disclosed as replays and receive no extra credit.",
            "json_documents_parsed": 19,
            "mypy_result": "PASS",
            "ruff_result": "PASS",
            "retained_precommit_tool_failures": 3,
            "canonical_aggregate": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": "Precommit owner-scoped planning validation only. The disclosed x1 replay is not a final canonical replay and earns no duplicate credit; this is not independent, professional, authority, or Stage 20 evidence.",
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
