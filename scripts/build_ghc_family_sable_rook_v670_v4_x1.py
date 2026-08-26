"""Build Sable Rook v670-v4's planning-only x1 freeze.

The builder is owner-delta scoped and fail-closed. It requires Auren Lark's
exact v670-v3 final, the exact Sable branch, and an absent x2/closeout tree. It
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
OWNER_ROOT = ROOT / "docs" / "sable-rook" / "v670-v4"
OWNER = "Sable Rook"
PHASE = "v670-v4"
BRANCH = "codex/GHC-Family/sable-rook-v670-v4-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/auren-lark-v670-v3-full-tools"
SOURCE_START = "a2e0262e7b9f3333fd06a826781516c29181580d"
SOURCE_X1 = "65769017d514255d2763b23c9dd0d0b3e46685f1"
SOURCE_EVIDENCE = "282ba12ec106a1ae87d87badbaedcb90d31f0b97"
SOURCE_FINAL = "fcdc6dc7af9d85b82ef2a185254b7b2b5e43f080"
ACTIVATION_PATH = "docs/auren-lark/v670-v3/handoffs/next-authorized-v670-v4-activation-candidate.md"
ACTIVATION_SHA256 = "7c8bd14926333acc0e5edd96689e18a3f94f3a0ee3390b8ea9cad69d9568a627"
FAILED_CANONICAL_SHA256 = "dd87e2df80533316bd09d72293f33953fe01b730a97fdffb57cb7a0b0a400794"
COMPOSITE_SHA256 = "c92acddf0f1dd3181b535f2a27c0c7480b65675d73346bfcfa29181d26f0abf9"
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
CORE_LABELS = ["completed", "represented", "open_gap", "exact_gate"]

IDENTITY_BOUNDARY = (
    "Sable Rook, they/them, relational evidence-and-reproducibility steward, "
    "is relational working language only. It is not evidence of consciousness, "
    "sentience, legal personhood, identity continuity, employment, qualification, "
    "independent agency, or scientific, operational, legal, cultural, affected-party, "
    "or Māori authority."
)
HOPE = (
    "make every surviving claim reproducible, challengeable, correctable, and "
    "retractable while every authority vacancy stays explicit"
)
BOUNDARY = (
    "Software, symbolic, synthetic, same-owner, citation, inherited, or composite "
    "evidence is not empirical confirmation, participant evidence, professional or "
    "scientific authority, production readiness, legal or cultural ratification, "
    "Māori authority, affected-party approval, complete privacy or accessibility "
    "assurance, exhaustive security, independent reproduction, AGI/ASI, consciousness "
    "or personhood evidence, Theory-of-Everything proof, proof/canon, or Stage 20 authority."
)

REPOSITORY_SEAL = {
    "proposal_chain": 5350,
    "effective_negatives": 32409,
    "effective_methods": 18520,
    "failed_witnesses": 4230,
    "bounded_passing_witnesses": 5561,
    "open_gaps": 245,
    "exact_gates": 240,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
}
ACTIVATION_OVERLAY = {
    **REPOSITORY_SEAL,
    "effective_negatives": 32411,
    "effective_methods": 18522,
    "failed_witnesses": 4232,
    "bounded_passing_witnesses": 5562,
    "external_zero_credit_failures": 2,
    "external_bounded_passing_witnesses": 1,
    "repository_seal_rewritten": False,
}

STARTUP_FAILURES = [
    (
        "SR6704-START-N001",
        "The first combined current-state render exceeded the bounded output window before all required state reached EOF.",
        "Read the current state in literal bounded chunks and verify the last byte of every required file.",
        "The selected current state, routing precedence, roster, authorization, and schemas reached EOF.",
        "Measure mutable state first and use literal bounded windows.",
    ),
    (
        "SR6704-START-N002",
        "A PowerShell skill-size probe placed a pipeline directly after foreach and failed in the parser.",
        "Materialize foreach output into a named array before serialization.",
        "The corrected bounded array returned exact skill paths and sizes.",
        "Never pipe directly from a compound foreach statement.",
    ),
    (
        "SR6704-START-N003",
        "A receipt-inventory projection repeated the same direct-foreach pipeline parser fault.",
        "Reuse the named-array recurrence guard before rendering receipt metadata.",
        "The corrected inventory completed without mutation.",
        "Apply the recurrence guard to every PowerShell compound producer.",
    ),
    (
        "SR6704-START-N004",
        "A broad external-receipt-bank wrapper returned no attributable summary.",
        "Bound the search to the standard receipt bank and compare exact digests without inventing private paths.",
        "All 1,536 bounded receipt-bank files were hashed; neither supplied digest was present.",
        "Treat absent externally supplied receipt paths as a provenance state, not a search invitation.",
    ),
    (
        "SR6704-START-N005",
        "A Windows wildcard passed as a literal ripgrep path was rejected.",
        "Resolve exact filenames first and pass each literal path.",
        "The exact activation and manifest filenames were resolved and read.",
        "Do not assume shell glob expansion on Windows command arguments.",
    ),
    (
        "SR6704-START-N006",
        "A source-validator probe guessed a nonexistent verify_baton_integrity helper.",
        "Inspect the committed module's exported names and invoke its actual validate_baton helper.",
        "The activation Git blob passed exact digest, byte, word, and prospective-state validation.",
        "Inspect callable names before invoking inherited helpers.",
    ),
    (
        "SR6704-START-N007",
        "A combined manifest-helper wrapper ended without attributable stdout.",
        "Split the replay into literal scalar checks and render counts only after each completes.",
        "All four inherited manifests replayed with zero mismatch and complete coverage.",
        "Prefer scalar attributable probes over compound summaries at lifecycle gates.",
    ),
    (
        "SR6704-START-N008",
        "Parallel evidence and owner-manifest replay lost session attribution at the wrapper boundary.",
        "Run the bounded replay serially and poll only the returned session.",
        "The serial replay recovered exact x1, evidence, final-delta, and final-owner results.",
        "Do not parallelize proof steps whose session attribution is itself evidence.",
    ),
    (
        "SR6704-START-N009",
        "Sparse-checkout reapply did not populate the index of the newly added no-checkout worktree.",
        "Populate the configured sparse index with git read-tree -mu HEAD, then inspect status and file count.",
        "The Sable lane materialized 187 source files at the exact final and remained clean.",
        "After no-checkout creation, verify index population rather than assuming reapply materializes it.",
    ),
    (
        "SR6704-START-N010",
        "A combined Method Flow sample and runner projection yielded no attributable output and then referenced a guessed schema filename that did not exist.",
        "Enumerate the exact skill files and read references/schema.md through EOF.",
        "The actual Method Flow schema and validator requirements were read completely.",
        "Enumerate exact skill resources before dereferencing a schema path.",
    ),
    (
        "SR6704-START-N011",
        "A combined inherited-manifest metadata projection returned no attributable rows.",
        "Read each literal manifest head and tail separately and bind each count to its lifecycle commit.",
        "The four manifest domains, counts, hash domains, and self-exclusions were attributable.",
        "Use literal per-manifest reads when metadata projections suppress evidence.",
    ),
    (
        "SR6704-START-N012",
        "The first x1 build failed closed because the environmental-correction title crossed the frozen 0.72 semantic-neighbor threshold against Auren's excursion-correction title.",
        "Inspect only the colliding pair and rewrite the Sable proposal around bitemporal supersession, original-observation retention, and explicit correction reason.",
        "The unchanged semantic-neighbor algorithm accepted all forty corrected Sable titles below the threshold.",
        "Run the direct materialized-title neighbor audit before freezing x1 and never lower the threshold to admit a collision.",
    ),
    (
        "SR6704-START-N013",
        "The corrected x1 build crossed its bounded wrapper window while replaying 353 manifest blobs through one Git process per entry and returned no attributable completion; state inspection found no artifact, process, or index mutation.",
        "Replace only the slow replay dependency with one exact git cat-file --batch stream and preserve identical digest and byte checks.",
        "The batched replay validated all four source manifests and the x1 build completed within the bounded window.",
        "Use one attributable Git batch for multi-blob lifecycle verification and inspect state before any retry.",
    ),
    (
        "SR6704-START-N014",
        "The first batched build materialized its packet but the command projection emitted only stdout, discarded the still-running session handle, and left the exact Sable builder process awaiting teardown.",
        "Inspect the exact process command, stop only that owner-local builder, preserve its generated packet, and rerun with the complete execution-session object exposed.",
        "The corrected invocation preserved its session attribution, completed successfully, and left no Sable builder process running.",
        "Always surface the full command result when a bounded invocation may yield a reusable session.",
    ),
    (
        "SR6704-START-N015",
        "A session-attributed diagnostic proved the first batch implementation deadlocked while writing every object name before reading git cat-file output; the exact invocation was interrupted at the blocked write.",
        "Use subprocess communicate with the complete bounded input so the operating system drains stdin, stdout, and stderr concurrently, then parse the immutable output buffer.",
        "The communicate-based batch replay completed, parsed every declared blob, and left no child or parent process running.",
        "Never manually fill a bidirectional subprocess pipe before consuming its output.",
    ),
    (
        "SR6704-START-N016",
        "The first commit gate treated the empty stdout of git diff --quiet as a false PowerShell Boolean and stopped despite exit code zero and no unstaged diff.",
        "Run the native command first and test the exact LASTEXITCODE scalar before deciding whether an unstaged diff exists.",
        "The corrected exit-code gate proved the unstaged diff empty before the x1 commit.",
        "Never infer native-command success from an intentionally silent stdout stream.",
    ),
]

NEW_TITLES = [
    "external receipt presence and rehash-state ledger separating supplied digest local verification and absence",
    "canonical zero-credit failure and dependency-corrected composite nonpromotion tribunal",
    "sparse no-checkout index materialization and measured-file receipt",
    "exact Git-blob manifest polling and session-attribution guard",
    "current-guidance freshness and live-authorization override ledger",
    "PowerShell producer materialization and scalar-summary recurrence guard",
    "frozen-title chain coverage and semantic-recovery arithmetic gap ledger",
    "exact source direct-parent single-parent and zero-merge preflight",
    "Python repository-root import-context canonical dependency preflight",
    "terminal route duplicate acknowledgement timeout and no-resend guard",
    "synthetic collection-object alias ledger separating work edition copy item and volume identity vacancies",
    "synthetic stack range bay case enclosure and shelf location topology",
    "temperature and relative-humidity observation envelope with uncertainty and calibration vacancies",
    "coupled relative-humidity temperature observation pair and timestamp-ordering contract",
    "environmental exception chronology with observation alert acknowledgement correction and closure",
    "moving-window fluctuation descriptor refusing causal damage inference",
    "light-exposure interval and cumulative proxy refusing material-effect inference",
    "outage leak suppression pest and handling cause-hypothesis classifier preserving unknown",
    "threshold-policy provenance separating collection category local policy and competent approval",
    "condition observation and damage-diagnosis firewall",
    "synthetic emergency relocation custody and return chain",
    "enclosure and material-compatibility authority-vacancy ledger",
    "shelf inventory reconciliation across expected found moved held and unexplained states",
    "bitemporal supersession register preserving original environment observations and explicit correction reasons",
    "hold release display and loan state machine with explicit authority vacancy",
    "alternative-format exception handover and delayed-status structural accessibility contract",
    "workload and shift-readback contract preserving unresolved tasks",
    "digital-surrogate link provenance fixity and non-substitution contract",
    "THOS rare-book environmental exception custody correction and handover proxy",
    "synthetic archival reading-room display and loan-transit environmental exception proxy",
    "synthetic audiovisual cold-storage acclimatization and handover proxy",
    "Freed ID zero-key collection-custody claim contest and correction representation",
    "CBR notice restriction reason access appeal and remedy representation",
    "GMUT environmental analogy firewall refusing storage observations as field evidence",
    "thermodynamic domain classifier refusing heat and moisture conversion into psyche or rights",
    "independent-review conflict and authority-vacancy representation",
    "zero-row official preservation-data adapter and likelihood refusal",
    "real conservator custodian affected-user and independent workflow evaluation register",
    "legal cultural Māori taonga title access data-governance and authority exact gate",
    "Stage 20 nonadmission tribunal binding empirical rights governance and independent-reproduction prerequisites",
]

SKILLS = [
    "ghc-family-external-receipt-rehash-state", "ghc-family-canonical-composite-nonpromotion",
    "ghc-family-sparse-index-materialization", "ghc-family-session-attributed-manifest",
    "ghc-family-guidance-freshness-ledger", "ghc-family-powershell-producer-guard",
    "ghc-family-semantic-gap-arithmetic", "ghc-family-exact-anchor-preflight-v4",
    "ghc-family-python-root-import-preflight", "ghc-family-terminal-no-resend-v4",
    "ghc-family-collection-object-alias", "ghc-family-shelf-location-topology",
    "ghc-family-environment-observation-envelope", "ghc-family-paired-observation-ordering",
    "ghc-family-exception-chronology", "ghc-family-fluctuation-noncausal",
    "ghc-family-light-exposure-proxy", "ghc-family-cause-unknown-preserver",
    "ghc-family-threshold-policy-provenance", "ghc-family-condition-diagnosis-firewall",
]
RUNNERS = [
    "ghc_family_external_receipt_state.py", "ghc_family_composite_nonpromotion.py",
    "ghc_family_sparse_index_receipt.py", "ghc_family_session_manifest_guard.py",
    "ghc_family_semantic_gap_arithmetic.py", "ghc_family_environment_contract.py",
    "ghc_family_collection_custody.py", "ghc_family_handover_readback.py",
    "ghc_family_authority_vacancy.py", "ghc_family_stage20_nonadmission.py",
]

EXACT = [
    "real collection object custody location or condition mutation", "real temperature humidity light or logger measurement",
    "real threshold hold release relocation loan display or treatment decision", "real participant practitioner or affected-user study",
    "real identity key proof account token or credential operation", "legal interpretation title ownership access or remedy decision",
    "taonga tikanga mātauranga place-name or Māori-authority decision", "cultural ratification restitution repatriation or community mandate",
    "production deployment external API write or cloud mutation", "host elevation security weakening feature enablement or reboot",
    "destructive cleanup history rewrite force push or sibling mutation", "privacy-complete or exhaustive-security certification",
    "complete accessibility-conformance declaration", "independent-reproduction or external-audit declaration",
    "empirical GMUT likelihood posterior parameter or force claim", "professional conservation preservation or safety determination",
    "affected-party consent acceptance or remedy legitimacy", "AGI ASI consciousness personhood or identity-continuity claim",
    "Theory-of-Everything proof or canon promotion", "Stage 20 admission or deployment authority",
]
BLOCKED = [
    "raw task identifiers private routes transcripts or session streams in artifacts",
    "sibling branch reset merge rewrite deletion or force push",
    "failed canonical replay success laundering or composite relabelling",
    "synthetic fixture promotion into professional or empirical evidence",
    "unapproved account secret payment deployment or third-party write",
    "real identity issuance presentation resolution status or revocation",
    "real legal cultural Māori-authority or affected-party substitution",
    "unsafe elevation host-security weakening feature enablement or reboot",
    "unbounded full-repository unchanged-history or cross-lane scan",
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
            "proposal_id": f"SR6704-N{index:03d}", "title": title,
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
    return [{"task_id": f"SR6704-{prefix}-{i:03d}", "title": f"{domain}: {control}", "owner": OWNER, "phase": PHASE, "x1_state": state, "external_actions": 0}
            for i, (domain, control) in enumerate(((d, c) for d in domains for c in controls), start=1)]


def named(prefix: str, values: list[str], state: str) -> list[dict[str, Any]]:
    return [{"task_id": f"SR6704-{prefix}-{i:03d}", "title": value, "owner": OWNER, "phase": PHASE, "x1_state": state, "external_actions": 0}
            for i, value in enumerate(values, start=1)]


def portfolio() -> dict[str, list[dict[str, Any]]]:
    domains = ["activation lineage", "Git-blob evidence", "semantic coverage", "collection alias", "environment observations", "exception chronology", "custody correction", "accessible handover", "authority vacancy", "terminal route"]
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
        method_id = f"SR6704-M{index:03d}"
        fail_id, pass_id = f"SR6704-W{index:03d}-F", f"SR6704-W{index:03d}-P"
        methods.append({
            "method_id": method_id, "title": f"bounded recovery for {negative_id}", "failure_signature": failed,
            "trigger_preconditions": ["the exact bounded failure signature is observed"], "privacy_class": "sanitized_public",
            "approval_class": "safe_now", "candidate_workaround": recovery, "validation_witness_ids": [fail_id, pass_id],
            "recurrence_guard": guard, "rollback": "Retain the failure, stop the affected wrapper, and change only the isolated owner-local procedure.",
            "recommendation_state": "preferred", "supersedes": [], "protected_gates": ["no_failure_laundering", "owner_delta_only", "no_authority_promotion"],
            "retained_negative_ids": [negative_id], "scope_boundary": "Bounded same-owner workflow evidence only.",
        })
        witnesses.extend([
            {"witness_id": fail_id, "method_id": method_id, "procedure": failed, "scope": "startup read-only owner workflow", "expected": "attributable bounded evidence", "observed": failed, "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": BOUNDARY},
            {"witness_id": pass_id, "method_id": method_id, "procedure": recovery, "scope": "isolated startup recovery", "expected": "bounded attributable recovery without mutation", "observed": passed, "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": BOUNDARY},
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
        ("docs/auren-lark/v670-v3/validation/x1-manifest.json", SOURCE_X1),
        ("docs/auren-lark/v670-v3/validation/evidence-manifest.json", SOURCE_EVIDENCE),
        ("docs/auren-lark/v670-v3/validation/final-delta-manifest.json", SOURCE_FINAL),
        ("docs/auren-lark/v670-v3/validation/final-owner-manifest.json", SOURCE_FINAL),
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
        "activation_packet": {"path": ACTIVATION_PATH, "bytes": len(packet), "words": len(packet_text.split()), "sha256": hashlib.sha256(packet).hexdigest(), "expected_sha256": ACTIVATION_SHA256, "integrity_valid": hashlib.sha256(packet).hexdigest() == ACTIVATION_SHA256, "prospective_not_posthoc": True},
        "failed_canonical_receipt": {"sha256": FAILED_CANONICAL_SHA256, "status": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT", "canonical_invocations": 1, "canonical_successes": 0, "replay_forbidden": True, "path_supplied": False, "local_rehash_state": "not_rehashed_digest_not_found_in_bounded_standard_receipt_bank"},
        "dependency_corrected_composite": {"sha256": COMPOSITE_SHA256, "status": "VALID_DEPENDENCY_CORRECTED_TERMINAL_COMPOSITE_WITH_ZERO_CANONICAL_AGGREGATE_CREDIT", "passing_witnesses": 1, "canonical_success_credit": 0, "path_supplied": False, "local_rehash_state": "not_rehashed_digest_not_found_in_bounded_standard_receipt_bank"},
    }


def overview(inherited: list[dict[str, Any]], proposals: list[dict[str, Any]]) -> str:
    prose = [
        "# Sable Rook v670-v4 x1 integrated planning overview", "", "## Lifecycle and evidence basis", "",
        "This packet is an x1 planning freeze. It contains no x2 result, no executed proposal, no completed portfolio claim, no route delivery, and no external write. Sable's additive sparse lane begins at Auren Lark's exact v670-v3 final. The source, x1, evidence, and final parent chain; zero-merge history; four remote-equality values; activation Git blob; and four commit-local manifests are checked before generation. Auren's canonical aggregate failed once on repository-root import context and receives zero success credit. The separately named dependency-corrected composite remains bounded recovery evidence and also receives zero canonical aggregate credit.",
        "", "## Identity, hope, and corrigibility", "", IDENTITY_BOUNDARY, "", f"Sable's relational hope is to {HOPE}. Hamish may rename, pause, redirect, or stop the route. Neither the role nor the hope is a credential. Corrigibility means a contradiction, failed witness, missing authority, ambiguous route, or unavailable evidence stops promotion rather than being rationalized away.",
        "", "## Primary pillar and bounded practices", "",
        "The primary pillar is Freed ID and CBR Heart. It is expressed only as synthetic claim, custody, contest, correction, access, reason, appeal, and authority-vacancy structure. THOS Body remains visible through bounded exception chronology, workload, readback, delayed status, and handover structure. GMUT Mind remains visible only through an analogy firewall and zero-row refusal; preservation observations are not scalar-tensor or effective-field-theory data. The first practice lens is synthetic rare-book environmental-monitoring exception, custody correction, accessible handover, and unresolved-work transfer. The second is synthetic archival reading-room, display, and loan-transit environmental exception review. The third is synthetic audiovisual cold-storage acclimatization and handover. None uses a real object, collection, person, institution, logger, measurement, loan, incident, key, claim, title, place, or authority action.",
        "", "## Scientific and professional firewall", "",
        "No repository artifact diagnoses damage, prescribes a threshold, authenticates an item, establishes title, confers custody, authorizes display or loan, or demonstrates conservation competence. Temperature, relative humidity, and light values in later fixtures are type-checking inputs only. They do not become empirical observations or professional advice. The GMUT surface remains a typed scalar-tensor and effective-field-theory research-model family; no force, prediction, likelihood, parameter constraint, empirical confirmation, ultraviolet completion, quantum completion, or Theory-of-Everything follows. THOS remains synthetic proxy work without real operators, blind matched-budget arms, safety monitoring, statistics, or independent review.",
        "", "## Novelty and semantic-recovery honesty", "",
        "The source seals a 5,350-row proposal chain, but only the forty Auren rows are materialized in this sparse owner-delta lane for direct semantic comparison. Auren's earlier count mirror declares 1,540 accessible inherited titles and a 3,570-row recovery gap; those values do not arithmetically close the later 5,350-row chain after adding forty Auren rows. Sable preserves the discrepancy as a count-mirror and semantic-recovery gap. The forty Sable titles must be unique within the new set and below the frozen neighbor threshold against the forty directly available Auren titles. This proves bounded distinctness only, never universal novelty over unavailable history.",
        "", "## Falsification and retained negatives", "",
        f"Each proposal freezes one accepting contract and four invalid mutations, for 160 planned rejections. The expected distribution is {OUTCOMES}. A completed outcome can mean only that its bounded software or structural acceptance gate passed. Represented means a synthetic proxy exists while real evidence remains absent. Open gaps remain unexecuted because real data or independent evaluation is missing. Exact gates remain with competent, affected, legal, cultural, and Māori authorities. Sixteen Sable startup failures are retained at zero credit with paired bounded recoveries. They add to the live activation overlay without rewriting Auren's seal.",
        "", "## Portfolio and tool boundaries", "",
        "The frozen portfolio contains sixty safe-now tasks, thirty bounded candidates, twenty exact-approval packets, ten blocked packets, twenty phase-local skill ideas, ten family-compatible runner ideas, sixty additive CLEAN/FIX/REFINE tasks, and successor recommendations with zero Sable completion credit. X2 may materialize only owner-local files under the 2,000-file guard. Historical and family-current callers remain compatibility surfaces. No global skill installation, account action, credential use, host elevation, security weakening, Windows feature change, Sandbox or Hyper-V activation, reboot, destructive cleanup, sibling mutation, or full-repository scan is authorized.",
        "", "## Privacy, accessibility, and authority", "",
        "Five privacy classes protect against raw task identifiers, private routes or callables, credentials and secrets, transcripts or session streams, and private absolute paths. Scanner definitions are candidates, not confirmed payload hits, and every candidate requires exact-file adjudication. Structural alternative-format and delayed-status controls do not establish complete accessibility conformance. Manual keyboard, browser, assistive-technology, cognitive, language, security-usability, and affected-user evaluation remain reserved. Māori concepts, wording, taonga status, data governance, and authority remain with tangata whenua, iwi, hapū, and Māori authorities.",
        "", "## Validation and route hold", "",
        "X1 must be staged exactly, pass its owner-scoped tests, parse every phase JSON file, pass five-class privacy adjudication and diff hygiene, and seal an exact staged Git-blob manifest. Only a clean pushed x1 with local, upstream, tracking, and fresh-live equality may unlock x2. The later exact-final canonical aggregate has a one-success budget: if it succeeds, it is not replayed; if it fails, the failure retains zero aggregate credit and only an isolated dependency may be corrected under a separately named composite. No successor is inferred or contacted from historical files. Terminal routing requires a fresh live authority reread, exact-title unique resolution, immediate reread, duplicate guard, and one acknowledged send.",
        "", "## Twenty inherited selections with zero Sable credit", "",
    ]
    prose.extend(f"- {row['source_proposal_id']}: {row['source_title']} — inherited integrity evidence only." for row in inherited)
    prose.extend(["", "## Forty frozen Sable proposals", ""])
    prose.extend(f"- {row['proposal_id']} [{row['planned_outcome']}]: {row['title']}." for row in proposals)
    prose.extend(["", "## Terminal truth", "", BOUNDARY, "", "`NOT_READY_FOR_STAGE_20`."])
    return "\n".join(prose)


def build() -> None:
    head, branch = git_text("rev-parse", "HEAD"), git_text("branch", "--show-current")
    if head != SOURCE_FINAL or branch != BRANCH:
        raise SystemExit(f"x1 requires {BRANCH} at {SOURCE_FINAL}; found {branch} at {head}")
    if any((OWNER_ROOT / name).exists() for name in ("x2", "closeout", "final", "seal")):
        raise SystemExit("x1 refuses a lane containing x2 or closeout material")
    source_rows = load_json(ROOT / "docs" / "auren-lark" / "v670-v3" / "closeout" / "proposal-ledger-final.json")["rows"]
    inherited = [{"selection_id": f"SR6704-I{i:03d}", "source_owner": "Auren Lark", "source_phase": "v670-v3", "source_proposal_id": row["proposal_id"], "source_title": row["title"], "source_outcome": row["outcome"], "source_row_sha256": hashlib.sha256(json.dumps(row, sort_keys=True, separators=(",", ":")).encode()).hexdigest(), "integrity_revalidated": True, "sable_novelty_credit": 0, "sable_completion_credit": 0, "state": "inherited_evidence_only"} for i, row in enumerate(source_rows[:20], start=1)]
    proposals = proposal_rows()
    if len(proposals) != 40 or len({row["title"] for row in proposals}) != 40 or Counter(row["planned_outcome"] for row in proposals) != Counter(OUTCOMES):
        raise SystemExit("proposal count, uniqueness, or distribution drifted")
    neighbors, max_score = [], 0.0
    for row in proposals:
        left, best_title, best_score = normalize(row["title"]), None, 0.0
        for source in source_rows:
            right = normalize(source["title"])
            score = len(left & right) / max(1, len(left | right))
            if score > best_score:
                best_title, best_score = source["title"], score
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
    x1_overlay = {**ACTIVATION_OVERLAY, "effective_negatives": ACTIVATION_OVERLAY["effective_negatives"] + len(STARTUP_FAILURES), "effective_methods": ACTIVATION_OVERLAY["effective_methods"] + len(STARTUP_FAILURES), "failed_witnesses": ACTIVATION_OVERLAY["failed_witnesses"] + len(STARTUP_FAILURES), "bounded_passing_witnesses": ACTIVATION_OVERLAY["bounded_passing_witnesses"] + len(STARTUP_FAILURES), "sable_startup_failures": len(STARTUP_FAILURES), "repository_seal_rewritten": False}
    write_json("x1/activation-intake.json", {"schema": "ghc.family.activation-intake.v5", "owner": OWNER, "phase": PHASE, "source_verification": source, "task_creation_count": 0, "fork_count": 0, "subagent_count": 0, "standby_contact_count": 0})
    write_json("x1/identity-and-boundary.json", {"schema": "ghc.family.identity-boundary.v4", "owner": OWNER, "phase": PHASE, "pronouns": "they/them", "relational_role": "relational evidence-and-reproducibility steward", "relational_hope": HOPE, "identity_boundary": IDENTITY_BOUNDARY, "corrigibility": "Hamish may rename, pause, redirect, or stop the route."})
    write_json("x1/source-count-overlay.json", {"schema": "ghc.family.source-count-overlay.v5", "repository_sealed": REPOSITORY_SEAL, "live_activation_overlay": ACTIVATION_OVERLAY, "sable_x1_overlay": x1_overlay})
    write_json("x1/inherited-proposal-revalidation.json", {"schema": "ghc.family.inherited-proposal-revalidation.v5", "owner": OWNER, "phase": PHASE, "selected": 20, "novelty_credit": 0, "completion_credit": 0, "rows": inherited})
    write_json("x1/semantic-neighbor-audit.json", {"schema": "ghc.family.semantic-neighbor-audit.v3", "owner": OWNER, "phase": PHASE, "source_chain": 5350, "direct_materialized_comparison_titles": len(source_rows), "source_declared_accessible_inherited_titles": 1540, "source_declared_semantic_recovery_gap": 3570, "arithmetic_closure_if_auren_rows_added": {"accessible": 1580, "unrecovered": 3770}, "count_mirror_inconsistency_retained": True, "new_titles": 40, "max_jaccard": round(max_score, 6), "collision_threshold": 0.72, "collisions": 0, "rows": neighbors, "universal_novelty_claim": False})
    write_json("x1/new-proposal-freeze.json", {"schema": "ghc.family.new-proposal-freeze.v5", "owner": OWNER, "phase": PHASE, "proposal_chain_before": 5350, "proposal_chain_after_if_evidence_frozen": 5390, "outcomes": OUTCOMES, "planned_invalid_mutations_per_proposal": 4, "planned_invalid_mutations": 160, "rows": proposals})
    write_json("x1/portfolio-freeze.json", {"schema": "ghc.family.remastered-portfolio-freeze.v5", "owner": OWNER, "phase": PHASE, "rows": frozen_portfolio, "counts": counts, "ordinary_phase_new_tool_target": 3, "bounded_practice_lenses": ["synthetic rare-book environmental-monitoring exception custody correction accessible handover", "synthetic archival reading-room display and loan-transit environmental exception", "synthetic audiovisual cold-storage acclimatization and handover"], "successor_practice_recommendation": "unresolved until terminal live authority", "inherited_portfolio_completion_credit": 0, "filler_prohibited": True})
    write_json("x1/source-ledger.json", {"schema": "ghc.family.public-source-ledger.v5", "owner": OWNER, "phase": PHASE, "retrieved_nz_date": "2026-08-26", "sources": [
        {"title": "Storing Your Books", "publisher": "Library of Congress", "url": "https://www.loc.gov/preservation/care/books.html", "status": "current", "use": "general preservation vocabulary and refusal boundaries only"},
        {"title": "Realistic Preservation Environment", "publisher": "US National Archives and Records Administration", "url": "https://www.archives.gov/preservation/storage/realistic-preservation-environment.html", "status": "current", "use": "environmental-management vocabulary and authority-vacancy boundaries only"},
        {"title": "Humidity Program", "publisher": "National Institute of Standards and Technology", "url": "https://www.nist.gov/programs-projects/humidity", "status": "current", "use": "humidity measurement and uncertainty vocabulary only"},
        {"title": "Web Content Accessibility Guidelines 2.2", "publisher": "World Wide Web Consortium", "url": "https://www.w3.org/TR/WCAG22/", "status": "stable", "use": "structural accessibility vocabulary and reservation boundaries only"},
    ], "queries": 0, "downloads": 0, "real_rows": 0, "boundary": "Sources supply vocabulary and refusal conditions only; they are not observations, measurements, professional advice, validation, legal interpretation, cultural legitimacy, Māori authority, or Stage 20 evidence."})
    write_json("x1/threat-model.json", {"schema": "ghc.family.threat-model.v5", "owner": OWNER, "phase": PHASE, "assets": ["immutable source lineage", "x1-before-x2 separation", "four truth labels", "retained failures", "synthetic-only fixtures", "authority vacancies", "route uniqueness"], "risks": [
        {"risk": "source or manifest drift", "control": "exact commits, Git-blob replay, and fresh live equality"}, {"risk": "universal novelty overclaim", "control": "direct forty-title comparison and retained arithmetic recovery gap"},
        {"risk": "synthetic evidence promotion", "control": "zero-row firewall and vacant professional authority"}, {"risk": "condition diagnosis or threshold advice", "control": "observation-only types and policy provenance"},
        {"risk": "failure laundering", "control": "append-only Method Flow with failed and passing witnesses"}, {"risk": "private route or identifier leak", "control": "five-class owner-delta candidate adjudication"},
        {"risk": "accessibility overclaim", "control": "structural-only checks with manual and affected-user evaluation reserved"}, {"risk": "duplicate successor send", "control": "terminal live authority, exact-title reread, duplicate guard, acknowledgement, and no-resend"},
    ], "not_exhaustive_security": True})
    write_json("x1/method-flow-startup.json", method_flow())
    write_json("x1/workflow-plan.json", {"schema": "ghc.family.workflow-plan.v5", "owner": OWNER, "phase": PHASE, "steps": [{"step": "activation guidance and source verification", "state": "completed_read_only"}, {"step": "planning-only x1 freeze", "state": "in_progress_until_pushed_equal"}, {"step": "bounded x2 execution", "state": "blocked_by_x1_terminal_gate"}, {"step": "combined closeout and seal", "state": "pending"}, {"step": "one owner-scoped canonical aggregate", "state": "pending_not_invoked"}, {"step": "successor route", "state": "unresolved_until_terminal_live_authority"}], "commit_ceiling": 8, "planned_phase_commits": 3, "x1_commit_ceiling": 5, "x2_commit_ceiling": 5, "materialized_file_guard": 2000, "canonical_success_budget": 1, "post_success_replay": False})
    write_json("x1/phase-truth.json", {"schema": "ghc.family.phase-truth.x1.v5", "owner": OWNER, "phase": PHASE, "primary_pillar": "Freed ID and CBR Heart", "protected_pillars": ["THOS Body", "GMUT Mind"], "proposal_rows": {"inherited_zero_credit": 20, "new": 40}, "expected_outcomes": OUTCOMES, "core_truth_labels": CORE_LABELS, "proposal_chain": {"before": 5350, "after_if_frozen": 5390}, "universal_novelty_claim": False, "startup_operational_failures": len(STARTUP_FAILURES), "x1_completion_credit": 0, "x2_execution_started": False, "real_world_actions": 0, "identity_boundary": IDENTITY_BOUNDARY, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("x1/route-plan.json", {"schema": "ghc.family.route-plan.v5", "owner": OWNER, "phase": PHASE, "prospective_recipient_exact_title": None, "prospective_phase": None, "delivery_state": "UNRESOLVED_UNTIL_TERMINAL_LIVE_REFRESH", "successor_contact_count": 0, "task_creation_count": 0, "substitute_endpoint_count": 0, "standby_contact_count": 0, "required_gate": "clean pushed exact final, attributable terminal validation, newest live authority and roster, unique exact-title reread, duplicate guard, and acknowledged one-send"})
    text = overview(inherited, proposals)
    write_text("x1/integrated-overview.md", text)
    write_json("x1/build-receipt.json", {"schema": "ghc.family.x1-build-receipt.v5", "owner": OWNER, "phase": PHASE, "source_head": head, "branch": branch, "inherited_rows": 20, "new_rows": 40, "portfolio_counts": counts, "overview_words": len(text.split()), "external_actions": 0, "x2_materialized": False})
    print(json.dumps({"owner": OWNER, "phase": PHASE, "new": 40, "outcomes": OUTCOMES, "portfolio": counts, "startup_failures": len(STARTUP_FAILURES), "overview_words": len(text.split())}, sort_keys=True))


def staged_paths() -> list[str]:
    return [line for line in git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if line]


def staged_review() -> None:
    paths = staged_paths()
    exact = {
        "scripts/build_ghc_family_sable_rook_v670_v4_x1.py",
        "tests/test_ghc_family_sable_rook_v670_v4_x1.py",
        "docs/sable-rook/v670-v4/validation/x1-method-flow-validation.json",
        "docs/sable-rook/v670-v4/validation/x1-validation-receipt.json",
        "docs/sable-rook/v670-v4/validation/x1-staged-privacy.json",
        "docs/sable-rook/v670-v4/validation/x1-staged-review.json",
        "docs/sable-rook/v670-v4/validation/x1-manifest.json",
    }
    out = [path for path in paths if not (path.startswith("docs/sable-rook/v670-v4/x1/") or path in exact)]
    mixed = [path for path in paths if any(part in path for part in ("/x2/", "/closeout/", "/final/", "/seal/")) or path.endswith(("_x2.py", "_final.py"))]
    payload = {"schema": "ghc.family.staged-review.v5", "owner": OWNER, "phase": PHASE, "lifecycle": "x1", "staged_before_self": paths, "staged_count_before_self": len(paths), "out_of_scope": out, "mixed_lifecycle": mixed, "valid": not out and not mixed}
    write_json("validation/x1-staged-review.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def manifest_from_index() -> None:
    exclusions = ["docs/sable-rook/v670-v4/validation/x1-manifest.json", "docs/sable-rook/v670-v4/validation/x1-staged-review.json"]
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
    python_paths = [ROOT / "scripts" / "build_ghc_family_sable_rook_v670_v4_x1.py", ROOT / "tests" / "test_ghc_family_sable_rook_v670_v4_x1.py"]
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
    self_path = "docs/sable-rook/v670-v4/validation/x1-staged-privacy.json"
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
                    "scripts/build_ghc_family_sable_rook_v670_v4_x1.py",
                    "tests/test_ghc_family_sable_rook_v670_v4_x1.py",
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
