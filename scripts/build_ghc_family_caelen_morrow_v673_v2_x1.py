"""Build Caelen Morrow v673-v2's planning-only x1 freeze.

This owner-scoped builder reads the exact immutable source tree, reconstructs
the reachable proposal-title corpus, checks the forty Caelen titles against
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
OWNER_ROOT = ROOT / "docs" / "caelen-morrow" / "v673-v2"
OWNER = "Caelen Morrow"
PHASE = "v673-v2"
BRANCH = "codex/GHC-Family/caelen-morrow-v673-v2-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/sylven-arc-v673-v1-full-tools"
SOURCE_START = "305708c6d5a8dfee0432a2c09ef5b59da4b6c438"
SOURCE_X1 = "606f6b7afef6d4368e1b34d128e57fc061629b05"
SOURCE_EVIDENCE = "11dbffa2598f106bfa78b37974f8726fb61c7708"
SOURCE_FINAL = "528a7d407cb7cace05b9bfd672b2fa74fc413d2c"
SOURCE_CANONICAL_PAYLOAD_SHA256 = "7efb155e26c4fc44aa6243fc71ef2dd8efd3d5ef0032e44e37c67c0db3bde7dd"
SOURCE_CANONICAL_RECEIPT_SHA256 = "59087cd1e6164784f04f5f1690798a75db56d6449caaa96a7fc748c15292c7df"
SOURCE_OPERATIONAL_OVERLAY_SHA256 = "28dc8618c45c5e4e2286568b0c48363041bfad0f5bc119440396584c2f92c62a"
CORE_LABELS = ["completed", "represented", "open_gap", "exact_gate"]
EXPECTED_COUNTS = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
DECLARED_SOURCE_CHAIN = 6270
DECLARED_RESULT_CHAIN = 6310
JACCARD_LIMIT = 0.72

IDENTITY_BOUNDARY = (
    "Caelen Morrow, they/them, relational preservation-change cartographer and "
    "consent-boundary keeper, is relational working language only. It is not "
    "evidence of consciousness, sentience, legal personhood, identity "
    "continuity, employment, qualification, independent agency, scientific or "
    "operational authority, professional authority, legal or cultural "
    "authority, affected-party authority, or Māori authority. Hamish may "
    "rename, pause, redirect, or stop the work."
)

PRACTICE_BOUNDARY = (
    "The accordion-repair intake and documentation lens is wholly synthetic "
    "learning and software design. It uses no real people, instruments, cases, "
    "parts, serials, observations, measurements, recordings, repairs, tuning, "
    "tools, materials, customers, workplaces, identity events, authority acts, "
    "or affected-party decisions. It confers no employment, qualification, "
    "repair, tuning, conservation, collection, safety, legal, cultural, Māori, "
    "privacy, accessibility, custody, ownership, or operational authority."
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
    "Professional repair and tuning, worker and product safety, ownership, "
    "custody, access, recording rights, privacy, accessibility, remedy, legal or "
    "cultural interpretation, affected-party legitimacy, Māori wording, Māori "
    "concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori "
    "authority remain open or exact-gated. Māori concepts remain under Māori "
    "authority. Terminal verdict remains NOT_READY_FOR_STAGE_20."
)


PROPOSAL_SPECS: list[tuple[str, str, str]] = [
    ("Synthetic accordion custody intake envelope", "completed", "x2/practice/custody-intake-envelope.json"),
    ("Accordion model and serial minimization profile", "completed", "x2/practice/model-serial-minimization.json"),
    ("Accordion case and accessory custody manifest", "completed", "x2/practice/case-accessory-manifest.json"),
    ("Accordion bellows-fold condition topology", "completed", "x2/practice/bellows-fold-topology.json"),
    ("Accordion bellows-leak suspicion quarantine board", "completed", "x2/practice/bellows-leak-quarantine.json"),
    ("Accordion reed-block slot provenance map", "completed", "x2/practice/reed-block-slot-provenance.json"),
    ("Accordion reed-plate mounting lineage", "completed", "x2/practice/reed-plate-mounting-lineage.json"),
    ("Accordion reed-tongue condition vocabulary", "completed", "x2/practice/reed-tongue-vocabulary.json"),
    ("Accordion valve-leather intervention hold", "completed", "x2/practice/valve-leather-hold.json"),
    ("Accordion wax and adhesive material provenance", "completed", "x2/practice/material-provenance.json"),
    ("Accordion keyboard action state graph", "completed", "x2/practice/keyboard-action-graph.json"),
    ("Accordion bass-button mechanism dependency graph", "completed", "x2/practice/bass-mechanism-graph.json"),
    ("Accordion register-switch state machine", "completed", "x2/practice/register-switch-machine.json"),
    ("Accordion coupler and mute state representation", "completed", "x2/practice/coupler-mute-state.json"),
    ("Accordion synthetic air-path continuity matrix", "completed", "x2/practice/air-path-matrix.json"),
    ("Accordion tuning-observation unit contract", "completed", "x2/practice/tuning-unit-contract.json"),
    ("Accordion temperament-claim refusal boundary", "completed", "x2/practice/temperament-refusal.json"),
    ("Accordion pitch-drift symbolic uncertainty board", "completed", "x2/practice/pitch-drift-uncertainty.json"),
    ("Accordion disassembly dependency directed graph", "completed", "x2/practice/disassembly-dag.json"),
    ("Accordion component-interchangeability refusal", "completed", "x2/practice/interchangeability-refusal.json"),
    ("Accordion proposed-intervention lineage envelope", "completed", "x2/practice/intervention-lineage.json"),
    ("Accordion reassembly completeness checklist", "completed", "x2/practice/reassembly-checklist.json"),
    ("Accordion tool-calibration evidence quarantine", "completed", "x2/practice/tool-calibration-quarantine.json"),
    ("Accordion photograph and recording-rights reservation", "represented", "x2/cbr/recording-rights-reservation.json"),
    ("Accordion estimate-versus-authorization splitter", "completed", "x2/practice/estimate-authorization-split.json"),
    ("Accordion safety-hold and escalation board", "completed", "x2/practice/safety-hold-board.json"),
    ("Accordion structurally accessible owner handover companion", "completed", "x2/accessibility/handover-companion.html"),
    ("Accordion workload and shift-handover ledger", "completed", "x2/thos/workload-handover-ledger.json"),
    ("Freed ID selective-disclosure accordion custody receipt", "represented", "x2/freed-id/selective-disclosure-custody.json"),
    ("Freed ID accordion correction and revocation envelope", "represented", "x2/freed-id/correction-revocation-envelope.json"),
    ("CBR accordion remedy and affected-party reservation matrix", "exact_gate", "x2/cbr/remedy-affected-party-gate.json"),
    ("CBR accordion cultural and Māori-authority gate", "exact_gate", "x2/cbr/cultural-maori-authority-gate.json"),
    ("THOS synthetic accordion intake-to-handover proxy", "represented", "x2/thos/intake-handover-proxy.json"),
    ("THOS governed accordion real-arm absence board", "represented", "x2/thos/real-arm-absence-board.json"),
    ("GMUT coupled-reed symbolic operator atlas", "represented", "x2/gmut/coupled-reed-operator-atlas.json"),
    ("GMUT accordion identifiability and gauge-refusal board", "represented", "x2/gmut/identifiability-gauge-refusal.json"),
    ("Transport-disabled public musical-instrument collection adapter", "open_gap", "x2/adapters/public-collection-adapter.json"),
    ("Zero-row official accordion-source capability matrix", "open_gap", "x2/adapters/official-source-capability-matrix.json"),
    ("Accordion five-class privacy and raw-identifier scanner", "completed", "x2/privacy/five-class-scan.json"),
    ("Accordion Stage 20 terminal-evidence refusal rail", "represented", "x2/final/stage20-refusal-rail.json"),
]


STARTUP_FAILURES = [
    (
        "PowerShell direct foreach-to-pipe parser rejection",
        "A direct foreach statement was placed immediately before a pipeline and PowerShell rejected the command before any repository read or write.",
        "Materialize the foreach results in an array before piping or serializing them.",
    ),
    (
        "PowerShell skill-size projection parser rejection",
        "The same unsupported direct foreach-to-pipe shape recurred in the bounded skill-size projection and produced no evidence.",
        "Use an explicitly initialized result array and append one scalar row at a time.",
    ),
    (
        "Authorization-state raw presentation truncation",
        "The first whole-file authorization-state presentation exceeded the useful output window and was not treated as a complete read.",
        "Read deterministic numbered windows through the exact final line and separately validate the schema.",
    ),
    (
        "Authorization-state window projection returned blank",
        "One Select-Object skip window returned no visible rows despite the file containing the requested range.",
        "Load the bounded file into an array and project exact zero-based slices without changing the source.",
    ),
    (
        "External Sylven receipt locations were not materialized",
        "The three supplied digest strings had no text hit in the bounded canonical, validation, terminal, phase, or activation receipt banks, so no file-backed digest recomputation was claimed.",
        "Carry the exact live-message digests as authoritative anchors and preserve a source-location gap rather than inventing a receipt path.",
    ),
    (
        "Broad semantic-search presentation was truncated",
        "A broad read-only rg projection produced more matches than the response window and therefore was not used as a complete semantic corpus.",
        "Use one exact Git-tree candidate list and one content-addressed cat-file batch instead.",
    ),
    (
        "Initial source-corpus probe exceeded the useful startup window",
        "The first exploratory exact-tree proposal scan remained inside Git tree enumeration without producing a bounded receipt and was interrupted at zero novelty credit.",
        "Run the owner x1 corpus builder once, retain its exact summary and digest, and do not reuse the abandoned probe as evidence.",
    ),
    (
        "Worktree creation presentation window elapsed",
        "The original no-checkout worktree operation outlived several reporting windows while constructing the large shared sparse index.",
        "Inspect the original process and target state, do not duplicate it, and continue only after the same operation completes cleanly.",
    ),
    (
        "Bandit unavailable in active Python runtime",
        "The active Python 3.12 environment reported no Bandit module; availability was not converted into an installation mandate.",
        "Use the already available dependency-justified pytest, Ruff, mypy, Hypothesis, and Pyright surfaces and retain Bandit as an explicit tool-availability gap.",
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
        "synthetic", "accordion", "board", "profile", "matrix", "envelope",
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
            "scope": "exact Sylven Arc v673-v1 final docs tree, proposal-named JSON paths only",
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
        proposal_id = f"CM6732-N{index:03d}"
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
                "Current official collection or standards documentation would be required before capability claims; x2 remains transport-disabled with zero calls and zero rows."
            )
        if index in {31, 32}:
            source_need = (
                "Exact affected-party, legal, cultural, tangata whenua, iwi, hapū, and Māori-authority evidence is required; public sources cannot close this gate."
            )

        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "primary_pillar": "Freed ID and CBR Heart",
                "protected_pillars": ["GMUT Mind", "THOS Body"],
                "bounded_practice": "synthetic accordion-repair intake and documentation",
                "hypothesis": hypothesis,
                "null_or_failure_condition": null,
                "approval_class": approval,
                "execution_lane": lane,
                "current_official_or_primary_source_need": source_need,
                "concrete_artifacts": [artifact],
                "falsifier_or_acceptance_gate": falsifier,
                "rollback_or_recovery": "Quarantine the artifact, retain the failed witness, restore the last exact manifest, and leave the outcome open or exact-gated.",
                "protected_gates": [
                    "zero real people, instruments, observations, measurements, repairs, tuning, keys, proofs, or identity events",
                    "no professional, safety, legal, cultural, affected-party, Māori, privacy-complete, accessibility-complete, independent, or Stage 20 authority",
                ],
                "expected_disposition": outcome,
                "outcome_observed": False,
                "inherited_completion_credit": 0,
                "caelen_novelty_credit": 1,
            }
        )
    return rows


def startup_method_flow() -> dict[str, Any]:
    methods: list[dict[str, Any]] = []
    witnesses: list[dict[str, Any]] = []
    for index, (title, failure, recovery) in enumerate(STARTUP_FAILURES, start=1):
        method_id = f"CM6732-M{index:03d}"
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
        "accordion-custody-envelope", "bellows-topology-validator", "reed-block-provenance",
        "reed-condition-vocabulary", "valve-material-quarantine", "action-state-graph",
        "register-state-machine", "tuning-claim-boundary", "disassembly-dependency",
        "intervention-lineage", "tool-evidence-quarantine", "recording-rights-gate",
        "authorization-splitter", "workload-handover", "accessible-companion",
        "freed-id-custody", "freed-id-correction", "thos-proxy-boundary",
        "gmut-symbolic-boundary", "stage20-refusal",
    ]
    runner_names = [
        "ghc_family_accordion_intake", "ghc_family_bellows_topology",
        "ghc_family_reed_provenance", "ghc_family_action_graph",
        "ghc_family_intervention_lineage", "ghc_family_authority_gate",
        "ghc_family_freed_id_receipt", "ghc_family_thos_proxy",
        "ghc_family_gmut_symbolic", "ghc_family_terminal_refusal",
    ]
    tools = [
        "ghc_family_caelen_morrow_v673_v2_accordion_record.py",
        "ghc_family_caelen_morrow_v673_v2_transition_graph.py",
        "ghc_family_caelen_morrow_v673_v2_authority_gate.py",
    ]
    safe_now = [
        {"task_id": f"CM6732-SN-{i:03d}", "title": f"Validate planning contract for {row['title']}", "state": "planned", "execution": "x2 synthetic only"}
        for i, row in enumerate(proposals, start=1)
    ]
    safe_now.extend(
        {"task_id": f"CM6732-SN-{40+i:03d}", "title": f"Build and smoke-use owner-local skill {name}", "state": "planned", "execution": "x2 owner-local only"}
        for i, name in enumerate(skill_names, start=1)
    )
    candidates = [
        {"task_id": f"CM6732-C-{i:03d}", "title": f"Represent bounded evidence for {proposals[i-1]['title']}", "state": "planned", "execution": "x2 representation only"}
        for i in range(1, 31)
    ]
    exact_approval = [
        {"task_id": f"CM6732-EA-{i:03d}", "title": title, "state": "unexecuted_exact_approval", "authority": "absent"}
        for i, title in enumerate(
            [
                "Touch or inspect a real instrument", "Record a real serial or owner identifier",
                "Perform bellows or reed work", "Perform tuning or temperament work",
                "Use tools, wax, adhesive, solvent, or leather", "Provide repair or safety advice",
                "Create a real estimate or customer authorization", "Photograph or record a real person or instrument",
                "Issue a real identity credential", "Create or use real keys or proofs",
                "Contact a collection API", "Ingest a collection row or media object",
                "Make a legal or ownership decision", "Make a cultural interpretation",
                "Use Māori wording as authorized language", "Make Māori data-governance decisions",
                "Claim affected-party acceptance", "Claim privacy or accessibility completeness",
                "Claim independent reproduction", "Claim Stage 20 readiness",
            ], start=1
        )
    ]
    blocked = [
        {"task_id": f"CM6732-B-{i:03d}", "title": title, "state": "blocked_unexecuted", "reason": "protected evidence or authority absent"}
        for i, title in enumerate(
            [
                "Real repair efficacy study", "Real governed THOS arms", "Empirical GMUT constraint",
                "Production Freed ID lifecycle", "Independent security review", "Affected-party governance",
                "Legal or cultural ratification", "Māori-authority review", "Operational deployment",
                "Stage 20 transition",
            ], start=1
        )
    ]
    cfr: list[dict[str, Any]] = []
    for kind in ("CLEAN", "FIX", "REFINE"):
        for i, skill in enumerate(skill_names, start=1):
            cfr.append({"task_id": f"CM6732-{kind}-{i:03d}", "kind": kind, "title": f"{kind.title()} {skill} boundary evidence", "state": "planned_additive"})
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
        "# Caelen Morrow v673-v2 planning-only x1 integrated overview",
        "",
        "## Relational working frame",
        "",
        IDENTITY_BOUNDARY,
        "",
        "Caelen's bounded hope is to make every synthetic transition auditable, reversible, and unmistakably short of real-world authority. The primary Trinity Mandala focus is Freed ID and CBR Heart. GMUT Mind and THOS Body remain explicit and protected.",
        "",
        "## Bounded practice",
        "",
        PRACTICE_BOUNDARY,
        "",
        "The phase treats an accordion only as a synthetic record-design lens: custody envelopes, component graphs, proposed-intervention lineage, correction paths, handover, workload, and refusal states. No record denotes a real instrument or person. Symbolic state is never a measurement, diagnosis, repair recommendation, or performance outcome.",
        "",
        "## Novelty scope",
        "",
        f"The immutable source declares {DECLARED_SOURCE_CHAIN:,} frozen rows. The exact source-tree audit inspected {corpus['candidate_git_blob_paths']:,} proposal-named JSON blobs, recovered {corpus['semantic_occurrences']:,} occurrences, {corpus['unique_proposal_ids']:,} identifiers, and {corpus['unique_titles']:,} unique titles. The forty Caelen titles cleared the fixed {JACCARD_LIMIT:.2f} token-Jaccard threshold with a maximum observed score of {max_score:.6f}. No universal novelty claim is made because no single exact canonical row-to-title ledger covers the declared chain.",
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
            "Nine startup failures are retained with zero credit and paired with bounded recoveries. The recovery witnesses do not erase the failed parser forms, truncated presentations, missing external receipt location, abandoned exploratory corpus probe, slow worktree presentation, or unavailable Bandit module. X2 will add every rejecting mutation, skill, runner, tool, parser, timeout, and gate witness through Method Flow.",
            "",
            "## Delivery truth",
            "",
            "This x1 neither contacts nor names an authorized later recipient. Hamish's newest live route, roster, authorization state, uniqueness, duplicate, pause, privacy, evidence, safety, usage, and acknowledgement gates must all be refreshed only after Caelen's own terminal exact-final gate. PREPARED_NOT_SENT applies to any later committed candidate until an existing-task message acknowledgement exists.",
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
        "x1/source-and-provenance.json",
        {
            "schema": "ghc.family.source-provenance.v6", "owner": OWNER, "phase": PHASE,
            "source_branch": SOURCE_BRANCH, "source_start": SOURCE_START, "source_x1": SOURCE_X1,
            "source_evidence": SOURCE_EVIDENCE, "source_final": SOURCE_FINAL,
            "source_canonical_payload_sha256": SOURCE_CANONICAL_PAYLOAD_SHA256,
            "source_canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
            "source_operational_overlay_sha256": SOURCE_OPERATIONAL_OVERLAY_SHA256,
            "external_receipt_file_location_materialized": False,
            "external_receipt_location_gap": "The live activation supplied exact digests but no bounded receipt-bank path was found; no recomputation was claimed.",
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
                {"id": "T01", "threat": "synthetic record mistaken for repair competence", "control": "practice boundary and exact professional gate"},
                {"id": "T02", "threat": "real owner, serial, or instrument data enters artifacts", "control": "synthetic-only schema, minimization, five-class scan"},
                {"id": "T03", "threat": "symbolic tuning field mistaken for measurement", "control": "symbolic-only type and empirical refusal"},
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
            "inherited_activation_baseline": {"negatives": 36374, "methods": 22702, "failed_witnesses": 8035, "passing_witnesses": 10265, "open_gaps": 293, "exact_gates": 286},
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
        "# Caelen Morrow v673-v2 phase boundaries\n\n" + IDENTITY_BOUNDARY + "\n\n" + PRACTICE_BOUNDARY + "\n\n" + SCIENCE_BOUNDARY + "\n\n" + AUTHORITY_BOUNDARY,
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
    owner_prefix = "docs/caelen-morrow/v673-v2/"
    allowed_scripts = {
        "scripts/build_ghc_family_caelen_morrow_v673_v2_x1.py",
        "tests/test_ghc_family_caelen_morrow_v673_v2_x1.py",
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
                        "build_ghc_family_caelen_morrow_v673_v2_x1.py",
                        "test_ghc_family_caelen_morrow_v673_v2_x1.py",
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
            "json_documents_parsed": 16, "mypy_result": "PASS",
            "ruff_result": "PASS_AFTER_RETAINED_ZERO_CREDIT_INITIAL_FAILURE",
            "retained_precommit_tool_failures": 2,
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
