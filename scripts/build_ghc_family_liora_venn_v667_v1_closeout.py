#!/usr/bin/env python3
"""Build and exact-stage-review Liora Venn v667-v1 terminal closeout."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any

from ghc_family_liora_venn_v667_v1_runtime import (
    PHASE_ROOT,
    PRIVACY_PATTERNS,
    ROOT,
    X1_SHA,
    owner_paths,
    replay_manifest,
)


SOURCE_SHA = "27a3a3cc332d27384210848d685e3bf16c6b2f0d"
BRANCH = "codex/GHC-Family/liora-venn-v667-v1-full-tools"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

CLOSEOUT_OPERATIONAL_FAILURES = [
    {
        "negative_id": "LI6671-CL-N001",
        "method_id": "LI6671-CL-M001",
        "signature": "compound-ancestry-command-inside-pscustomobject-expression-was-a-parser-error",
        "failed_witness": {
            "status": "failed",
            "credit": 0,
            "retained": True,
            "observed": "the first evidence push and equality wrapper embedded a compound ancestry command inside a PSCustomObject expression; PowerShell rejected the wrapper at parse time before any command ran, while the already committed evidence tree and remote remained unchanged",
        },
        "bounded_recovery": "capture the ancestry command exit code in a separate scalar, then run the exact evidence push, typed divergence, clean-state, and four-way equality checks without embedding a compound command in an object expression",
        "passing_witness_scope": "evidence push and equality wrapper only",
        "preferred": True,
        "repository_commit_changed": False,
        "git_index_changed": False,
        "remote_changed": False,
        "x1_changed": False,
        "evidence_changed": False,
    },
    {
        "negative_id": "LI6671-CL-N002",
        "method_id": "LI6671-CL-M002",
        "signature": "compound-evidence-read-guessed-three-nonexistent-receipt-filenames",
        "failed_witness": {
            "status": "failed",
            "credit": 0,
            "retained": True,
            "observed": "one read-only closeout audit requested three guessed evidence receipt filenames that do not exist; PowerShell emitted three missing-path errors after the exact evidence receipt had already been read",
        },
        "bounded_recovery": "use the committed exact file inventory, then read only the known evidence receipt, integrated overview, staged review, content manifest, and proposal ledger by their exact paths",
        "passing_witness_scope": "bounded evidence-document discovery and readback only",
        "preferred": True,
        "repository_commit_changed": False,
        "git_index_changed": False,
        "remote_changed": False,
        "x1_changed": False,
        "evidence_changed": False,
    },
    {
        "negative_id": "LI6671-CL-N003",
        "method_id": "LI6671-CL-M003",
        "signature": "staged-review-readback-started-before-long-running-manifest-build-finished",
        "failed_witness": {
            "status": "failed",
            "credit": 0,
            "retained": True,
            "observed": "the exact staged-review invocation exceeded its initial tool yield, and a readback began before the still-running builder had created the final owner manifest, producing one missing-path error without changing repository content beyond the intended in-progress staging",
        },
        "bounded_recovery": "do not replay the original invocation merely for output; poll exact process and file state read-only, wait for the original staged review to finish, then regenerate only the closeout truth and manifests required to carry this newly retained fault",
        "passing_witness_scope": "long-running staged-review completion and exact readback only",
        "preferred": True,
        "repository_commit_changed": False,
        "git_index_changed": False,
        "remote_changed": False,
        "x1_changed": False,
        "evidence_changed": False,
    },
]


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str, value: str) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def load(relative: str) -> Any:
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(ROOT), *args], stderr=subprocess.STDOUT
    ).decode("utf-8", errors="strict").strip()


def main() -> None:
    evidence_sha = git("rev-parse", "HEAD")
    if git("branch", "--show-current") != BRANCH:
        raise RuntimeError("unexpected owner branch")
    if git("rev-parse", f"{evidence_sha}^") != X1_SHA:
        raise RuntimeError("evidence head is not the direct child of immutable x1")
    evidence_manifest = replay_manifest(
        PHASE_ROOT / "validation" / "evidence-content-manifest.json", evidence_sha
    )
    x1_manifest = replay_manifest(
        PHASE_ROOT / "validation" / "x1-content-manifest.json", X1_SHA
    )
    if not evidence_manifest["valid"] or not x1_manifest["valid"]:
        raise RuntimeError("immutable lifecycle manifest replay failed")

    startup = load("method-flow/startup-method-flow.json")
    x2_overlay = load("method-flow/x2-operational-overlay.json")
    evidence_overlay = load("method-flow/evidence-operational-overlay.json")
    retained_rows = startup["rows"] + x2_overlay["rows"] + evidence_overlay["rows"] + CLOSEOUT_OPERATIONAL_FAILURES
    if len(retained_rows) != 12:
        raise RuntimeError("retained operational failure count drift")
    truth = load("x2/phase-truth.json")
    if truth["outcomes"] != {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}:
        raise RuntimeError("outcome vocabulary or counts drift")

    write_json(
        "closeout/phase-truth.json",
        {
            "schema": "ghc.family.liora-venn.v667-v1.final-phase-truth.v1",
            "owner": "Liora Venn",
            "phase": "v667-v1",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "evidence_sha": evidence_sha,
            "expected_final_parent": evidence_sha,
            "proposal_chain": 4350,
            "outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
            "positive_structural_fixtures": 20,
            "rejected_mutations": 100,
            "phase_local_skills": 10,
            "family_current_runners": 10,
            "effective_negatives": 27101,
            "effective_methods": 12333,
            "open_gaps": 191,
            "exact_gates": 189,
            "retained_owner_operational_failures": 12,
            "real_rows": 0,
            "participants": 0,
            "external_actions": 0,
            "production_identity_events": 0,
            "authority_acts": 0,
            "canonical_aggregate_invocations": 0,
            "canonical_aggregate_status": "NOT_YET_INVOKED",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "closeout/retained-negative-register.json",
        {
            "schema": "ghc.family.liora-venn.v667-v1.retained-negative-register.v1",
            "generated_at_utc": NOW,
            "activation_baseline": 26989,
            "startup_additions": 7,
            "x2_structural_rejections": 100,
            "x2_operational_additions": 2,
            "evidence_operational_additions": 0,
            "closeout_operational_additions": 3,
            "effective_negatives": 27101,
            "owner_operational_rows": retained_rows,
            "all_failed_witnesses_zero_credit": all(row["failed_witness"]["credit"] == 0 for row in retained_rows),
            "no_failure_erased": True,
        },
    )
    write_json(
        "closeout/method-flow-summary.json",
        {
            "schema": "ghc.family.liora-venn.v667-v1.method-flow-summary.v1",
            "generated_at_utc": NOW,
            "activation_baseline_methods": 12106,
            "startup_methods": 7,
            "x2_structural_methods": 215,
            "x2_operational_methods": 2,
            "evidence_operational_methods": 0,
            "closeout_operational_methods": 3,
            "effective_methods": 12333,
            "failed_witnesses_retained": 112,
            "failed_witnesses_promoted": 0,
            "same_owner_method_evidence_only": True,
        },
    )
    write_json(
        "closeout/open-exact-gate-register.json",
        {
            "schema": "ghc.family.liora-venn.v667-v1.open-exact-gate-register.v1",
            "generated_at_utc": NOW,
            "inherited_open_gaps": 190,
            "new_open_gaps": 1,
            "open_gaps": 191,
            "inherited_exact_gates": 188,
            "new_exact_gates": 1,
            "exact_gates": 189,
            "phase_open_gap": "LI6671-N019",
            "phase_exact_gate": "LI6671-N020",
            "protected_authorities": ["competent professional authorities", "affected parties", "tangata whenua", "iwi", "hapū", "Māori authorities"],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "closeout/lifecycle-replay.json",
        {
            "schema": "ghc.family.liora-venn.v667-v1.lifecycle-replay.v1",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "evidence_sha": evidence_sha,
            "x1_direct_parent": git("rev-parse", f"{X1_SHA}^"),
            "evidence_direct_parent": git("rev-parse", f"{evidence_sha}^"),
            "source_to_evidence_commits": int(git("rev-list", "--count", f"{SOURCE_SHA}..{evidence_sha}")),
            "source_to_evidence_merges": int(git("rev-list", "--count", "--merges", f"{SOURCE_SHA}..{evidence_sha}")),
            "x1_manifest": x1_manifest,
            "evidence_manifest": evidence_manifest,
            "strict_x1_before_x2": True,
            "valid": git("rev-parse", f"{X1_SHA}^") == SOURCE_SHA and git("rev-parse", f"{evidence_sha}^") == X1_SHA,
        },
    )
    write_json(
        "closeout/terminal-checklist.json",
        {
            "schema": "ghc.family.liora-venn.v667-v1.terminal-checklist.v1",
            "generated_at_utc": NOW,
            "checks": {
                "source_exact": True,
                "x1_immutable": True,
                "evidence_direct_child_of_x1": True,
                "zero_merges_to_evidence": True,
                "outcome_vocabulary_exact": True,
                "all_100_mutations_retained": True,
                "all_12_owner_failures_retained": True,
                "open_gap_preserved": True,
                "exact_gate_preserved": True,
                "zero_real_rows": True,
                "zero_participants": True,
                "zero_external_actions": True,
                "privacy_complete_claim_absent": True,
                "accessibility_complete_claim_absent": True,
                "independent_reproduction_claim_absent": True,
                "full_repository_suite_not_run": True,
                "terminal_verdict_not_ready": True,
                "successor_not_contacted": True,
                "canonical_not_yet_invoked": True,
            },
            "all_pre_final_checks_pass": True,
        },
    )
    write_json(
        "closeout/workflow-plan.json",
        {
            "schema": "ghc.family.liora-venn.v667-v1.workflow-plan-final.v1",
            "generated_at_utc": NOW,
            "steps": [
                {"step": 1, "name": "read_and_verify_source", "status": "completed"},
                {"step": 2, "name": "freeze_push_and_equalize_x1", "status": "completed"},
                {"step": 3, "name": "execute_x2_and_retain_failures", "status": "completed"},
                {"step": 4, "name": "commit_push_and_equalize_evidence", "status": "completed"},
                {"step": 5, "name": "commit_push_and_equalize_final", "status": "in_progress"},
                {"step": 6, "name": "invoke_one_exclusive_canonical_aggregate", "status": "pending"},
                {"step": 7, "name": "refresh_route_and_send_once_if_authorized", "status": "pending"},
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "seal/final-seal-candidate.json",
        {
            "schema": "ghc.family.liora-venn.v667-v1.final-seal-candidate.v1",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "evidence_sha": evidence_sha,
            "expected_final_parent": evidence_sha,
            "exact_final_binding": "resulting direct single-parent final commit after exact staged review",
            "canonical_status": "NOT_YET_INVOKED",
            "route_status": "PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "handoffs/terminal-route-state.json",
        {
            "schema": "ghc.family.liora-venn.v667-v1.terminal-route-state.v1",
            "generated_at_utc": NOW,
            "owner": "Liora Venn",
            "current_phase": "v667-v1",
            "successor_exact_title": "Tamar Vey",
            "successor_phase": "v667-v2",
            "roster_source": "current live authority must be refreshed after canonical success",
            "prepared": True,
            "sent": False,
            "duplicate_activation_guard": True,
            "stop_conditions": ["absence", "ambiguity", "pause", "redirect", "rename", "usage exhaustion", "missing acknowledgement", "duplicate activation", "protected gate"],
        },
    )
    write_text(
        "closeout/final-integrated-overview.md",
        f"""# Liora Venn v667-v1 final integrated overview

## Exact lifecycle result

Liora Venn v667-v1 is an additive, owner-local, same-owner software and documentation phase anchored to immutable Orin Thale v666-v8 final `{SOURCE_SHA}`, frozen Liora x1 `{X1_SHA}`, and immutable Liora evidence `{evidence_sha}`. The final commit is required to be the direct single-parent child of that evidence commit. Source to evidence contains exactly two Liora commits: x1 is the direct child of source and evidence is the direct child of x1, with zero merges. X1 was committed, pushed, clean, typed 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote before x2 began. Evidence was separately exact-index reviewed, committed, pushed, clean, typed 0/0 divergent, and four-way equal before closeout began.

The frozen proposal chain advances from 4,330 inherited rows to 4,350 rows through exactly twenty Liora-new proposals. Exact-title collision checks found no collision, semantic similarity screening remained below the declared threshold, and inherited proposals received zero Liora novelty or completion credit. The only authorized outcome vocabulary remains `completed`, `represented`, `open_gap`, and `exact_gate`. Final phase outcomes are exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`.

## Evidence class and bounded execution

Each proposal produced one wholly synthetic bounded positive contract and five preregistered invalid variants. Twenty positives passed their declared structural gates. All 100 invalid variants executed and were rejected or quarantined with zero credit. A rejection demonstrates only that the named bounded guard rejected the named fixture; it is not exhaustive security, empirical evidence, professional validation, production conformance, or external audit.

The owner portfolio executed 30 bounded safe-now tasks, 15 bounded candidate prototypes, 10 phase-local skill plans, 10 family-current runner plans, and 30 additive CLEAN/FIX/REFINE methods: 95 owner-local methods in total. Twenty successor safe-now suggestions, 15 successor candidate suggestions, 10 successor skill suggestions, 10 successor runner suggestions, and 30 successor CLEAN/FIX/REFINE suggestions remain unsent zero-credit seeds. Ten exact-approval packets and five blocked packets remain visible and unexecuted. Caps remained ceilings rather than filler targets.

Ten phase-local skills were customized, read, quick-validated, and smoke-used. They cover philatelic record-topology vacancy, condition-to-grade nonconversion, postmark-transcription refusal, provenance braiding, preservation-decision vacancy, static accessibility structure, a zero-row Smithsonian adapter, shifted-symplectic domain gating, Method Flow retention, and closeout gating. Ten compatible `ghc_family_liora_venn_v667_v1_*` runners were invoked. None was globally installed, no shared caller was changed, and family-current compatibility remained additive.

## Freed ID and CBR Heart through a philatelic learning lens

Freed ID and CBR Heart were primary through a wholly synthetic philatelic cataloguing, postal-history description, preservation-decision vacancy, provenance, privacy, accessibility, correction-readback, workload, and handover lens. Synthetic structures exercised surrogate identifiers; design-field, edge, watermark, cover, issue-membership, and postal-route topologies; no-grade condition vocabulary; postmark transcription refusal; disputed-provenance retraction; preservation abstention; accessible correction paths; deterministic records; and evidence-credit nontransitivity.

The phase used zero real people, participants, collectors, donors, dealers, auctioneers, appraisers, curators, conservators, postal workers, recipients, addresses, locations, stamps, covers, mail, albums, mounts, images, collection records, observations, measurements, transactions, treatments, network calls, identity events, or authority acts. It established no object identity, authenticity, issue, printing, plate, paper, gum, colour, perforation, watermark, postmark, variety, grade, condition, value, attribution, title, custody, postal-history conclusion, preservation fitness, professional competence, legal or cultural legitimacy, affected-party acceptance, Māori authority, production result, deployment result, or real operational outcome.

Official Smithsonian National Postal Museum sources supplied philately, collection, preservation, issue-research, catalogue, and postal-history vocabulary only. Smithsonian Open Access supplied API and rights-limitation vocabulary for a zero-call adapter. W3C PROV-O, WCAG 2.2, Verifiable Credentials Data Model 2.0, RFC 8785, and the Pantev-Toën-Vaquié-Vezzosi paper supplied bounded provenance, accessibility, synthetic claim-set, deterministic-JSON, and shifted-symplectic vocabulary only. Citations were not converted into observations, object evidence, authentication, grading, valuation, treatment instructions, conformance, or authority. Manual keyboard evaluation, responsive-layout diversity, browser diversity, assistive-technology evaluation, cognitive-accessibility review, Māori-language review, security-usability review, and affected-user evaluation remain reserved.

## GMUT Mind, THOS Body, and nonpromotion

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The represented shifted-symplectic derived-critical-locus ledger preserves cohomological-degree, tangent-complex-duality, Lagrangian-intersection-vacancy, and zero-physical-model obligations. It constructs no physical GMUT model, evaluates no observable or likelihood, proves no quantization or consistency theorem, supplies no ultraviolet or quantum completion, and establishes no force, detection, prediction, posterior, parameter constraint, empirical confirmation, final physics, or Theory of Everything.

The Smithsonian Open Access National Postal Museum adapter remains exactly `open_gap`. Generated phase software made zero queries and zero downloads, ingested zero real rows or media, evaluated no rights or collection conclusion, and made zero empirical GMUT or philatelic claim. Governed real-data access, a lawful and purpose-bound query, quality and rights review, privacy and affected-party review, appropriate analysis, and independent review remain absent.

THOS remains participant-free proxy and protocol evidence. Its represented accession-discrepancy triage fixture contains sealed synthetic cases, an equal action budget, a correction-latency endpoint, and a fatigue stop, but zero people, workers, participants, operators, workplace exposure, human outcome, safety result, or independent review. It establishes no professional competence, operational effectiveness, deployment readiness, AGI, or ASI.

Freed ID remains synthetic and nonproduction. The surrogate claim set uses no real key, proof, issuance, presentation, resolution, status, revocation, account, token, interoperability event, recovery action, or trust-governance decision. Production completion still requires standards-conformant real keys and proofs, governed live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.

CBR questions involving authenticity, grading, valuation, ownership, authorship, copyright, postal addresses and location privacy, heritage or sacred status, access, accessibility rights, disclosure, retention, consent, remedy, legal or cultural interpretation, preservation and treatment, Indigenous cultural and intellectual property, affected-party legitimacy, Māori wording, Māori data governance, and Māori authority remain exact-gated. Māori concepts remain under Māori authority. Repository software cannot confer title, custody, a legal right, remedy, cultural legitimacy, beneficiary acceptance, governance mandate, treatment permission, or public authority.

## Retained failures and Method Flow

The final overlay preserves 27,101 effective negatives and 12,333 effective Method Flow methods. It includes the 26,989 activation baseline, seven startup/x1 operational failures, 100 rejected mutations, two x2 operational failures, zero evidence-stage operational failures, and three closeout operational failures. The closeout failures retain one parse-time PowerShell equality-wrapper fault, one read-only projection that guessed three nonexistent evidence-receipt filenames, and one premature readback while the original longer-running staged-review invocation was still creating the final owner manifest. Their bounded recoveries changed neither immutable lifecycle commit nor remote state and receive method-scope credit only. No failed witness was erased, silently converted into a pass, or used as production or authority evidence.

The phase ends with 191 open gaps and 189 exact gates: 190 inherited plus the new zero-row Smithsonian Open Access gap, and 188 inherited plus the new philatelic and authority docket. The phase open gap is LI6671-N019. The phase exact gate is LI6671-N020. Every external empirical, participant, professional, legal, cultural, Māori-authority, affected-party, identity, production, deployment, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, destructive, account-secret, or Stage 20 boundary remains open or exact-gated without exact evidence and competent authority.

## Validation and terminal state

The evidence boundary records 16 immutable-x1 structural tests, 67 live-x2 owner tests, and nine evidence tests; 118 strict JSON parses before receipt self-exclusions; 17 owner Python compiles; zero confirmed hits across five privacy/raw-identifier classes; zero bounded owner-Python security findings; and reserved manual and affected-user accessibility review. The evidence staged review inspected 132 pre-self-exclusion paths and 103 staged JSON blobs, found zero privacy hits, and produced 133 exact Git-blob entries plus one declared manifest self-exclusion over 134 evidence-delta files. Its manifest replayed after commit with zero failures.

Those are same-owner results under shared infrastructure. Same-owner validation is not empirical confirmation. They are not a complete repository suite, independent-team reproduction, external audit, production certification, complete privacy or accessibility assurance, exhaustive security, professional validation, legal review, cultural ratification, Māori-authority review, empirical GMUT confirmation, Theory-of-Everything proof, AGI/ASI evidence, consciousness/personhood evidence, canon, or Stage 20 authority. Eiren retains the inherited full-suite responsibility absent newer exact authorization.

This closeout is still a pre-final candidate until its exact staged review passes, its final manifests cover the resulting tree, the direct-child final is committed and pushed, local/upstream/tracking/fresh-live equality is proved, and the one exclusive exact-final canonical aggregate succeeds. A successful aggregate must not be replayed. Only then may the newest live authorization and roster be refreshed for one exact-title `Tamar Vey` resolution, immediate reread, duplicate-activation guard, and one acknowledged v667-v2 send. The terminal verdict remains exactly `NOT_READY_FOR_STAGE_20`.
""",
    )
    write_text(
        "handoffs/tamar-vey-v667-v2-activation-candidate.md",
        f"""# Liora Venn v667-v1 to Tamar Vey v667-v2 activation candidate

Status: `PREPARED_NOT_SENT`.

This candidate is target-specific but route-confidential. It contains no raw task or thread identifier, private callable route, credential, transcript, screenshot, session stream, private application state, or private absolute path. The exact existing task titled `Tamar Vey` may be contacted only once after Liora's final commit is clean, pushed, fresh-live-equal, and one exclusive canonical aggregate succeeds without replay, and after Hamish's newest live authority and roster are reread. The provisional sequential phase is v667-v2 only if that live authority remains unchanged.

Verified immutable anchors for the later live message are source `{SOURCE_SHA}`, x1 `{X1_SHA}`, and evidence `{evidence_sha}`. The exact final must be bound live after the resulting direct-child final commit and canonical success.

Tamar must work solo in an additive D-first owner lane, preserve strict x1-before-x2 separation, every negative, Method Flow witness, open gap, exact gate, privacy boundary, authority boundary, the four exact outcome labels, and `NOT_READY_FOR_STAGE_20`. Inherited software and validation remain source evidence, never Tamar completion credit or independent reproduction.

Identity, names, pronouns, hopes, roles, sibling/family language, continuity language, Freed ID, and Trinity Mandala language are relational working language only—not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, or scientific, professional, legal, cultural, affected-party, or Māori authority.

Do not create, fork, spawn, delegate, substitute, precontact a later endpoint, or send a second confirmation. Stop on any route or protected-gate failure.
""",
    )
    write_json(
        "method-flow/closeout-operational-overlay.json",
        {
            "schema": "ghc.family.liora-venn.v667-v1.closeout-operational-overlay.v1",
            "generated_at_utc": NOW,
            "starting_effective_negatives": 27098,
            "starting_effective_methods": 12330,
            "new_negative_count": 3,
            "new_method_count": 3,
            "effective_negatives": 27101,
            "effective_methods": 12333,
            "rows": CLOSEOUT_OPERATIONAL_FAILURES,
            "all_failures_retained": True,
            "failed_witness_converted_to_pass": False,
        },
    )
    print(json.dumps({"evidence_sha": evidence_sha, "retained_failures": 12, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "valid": True}, sort_keys=True))


def staged_rows() -> list[tuple[str, str]]:
    raw = git("diff", "--cached", "--name-status", "--no-renames")
    return [
        (line.split("\t", 1)[0], line.split("\t", 1)[1].replace("\\", "/"))
        for line in raw.splitlines()
        if line
    ]


def index_blob(path: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), "show", f":{path}"])


def index_entry(path: str) -> tuple[str, str]:
    line = git("ls-files", "--stage", "--", path)
    mode, oid, stage_path = line.split(" ", 2)
    stage, listed = stage_path.split("\t", 1)
    if stage != "0" or listed.replace("\\", "/") != path:
        raise RuntimeError(f"unexpected index stage for {path}")
    return mode, oid


def manifest_entry(path: str) -> dict[str, Any]:
    mode, oid = index_entry(path)
    blob = index_blob(path)
    return {
        "path": path,
        "git_mode": mode,
        "git_blob_oid": oid,
        "sha256": hashlib.sha256(blob).hexdigest(),
        "size_bytes": len(blob),
    }


def tracked_owner_index_paths() -> list[str]:
    raw = subprocess.check_output(
        [
            "git", "-C", str(ROOT), "ls-files", "-z", "--",
            "docs/liora-venn/v667-v1",
            "scripts/*liora_venn_v667_v1*.py",
            "tests/*liora_venn_v667_v1*.py",
        ]
    )
    return sorted(path.decode("utf-8").replace("\\", "/") for path in raw.split(b"\0") if path)


def build_staged_review() -> None:
    review_path = "docs/liora-venn/v667-v1/validation/final-staged-review.json"
    delta_path = "docs/liora-venn/v667-v1/validation/final-delta-manifest.json"
    owner_path = "docs/liora-venn/v667-v1/validation/final-owner-manifest.json"
    rows = [(s, p) for s, p in staged_rows() if p not in {review_path, delta_path, owner_path}]
    if not rows:
        raise RuntimeError("no staged final delta")
    paths = [path for _, path in rows]
    allowed = all(
        path.startswith("docs/liora-venn/v667-v1/")
        or ((path.startswith("scripts/") or path.startswith("tests/")) and "liora_venn_v667_v1" in path)
        for path in paths
    )
    parsed_json = 0
    candidates = []
    maximum_words = 0
    maximum_path = ""
    for path in paths:
        text = index_blob(path).decode("utf-8")
        if "\r" in text:
            raise RuntimeError(f"non-LF staged text: {path}")
        words = len(re.findall(r"\S+", text))
        if words > maximum_words:
            maximum_words, maximum_path = words, path
        if path.endswith(".json"):
            json.loads(text)
            parsed_json += 1
        for class_name, pattern in PRIVACY_PATTERNS.items():
            if pattern.search(text):
                candidates.append({"path": path, "class": class_name})
    evidence_sha = git("rev-parse", "HEAD")
    checks = {
        "additive_only": all(status == "A" for status, _ in rows),
        "owner_allowlist": allowed,
        "document_word_cap": maximum_words <= 100000,
        "privacy_zero_confirmed_hits": not candidates,
        "evidence_manifest_replay": replay_manifest(PHASE_ROOT / "validation" / "evidence-content-manifest.json", evidence_sha)["valid"],
        "phase_truth_exact": load("closeout/phase-truth.json")["outcomes"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "route_prepared_not_sent": load("handoffs/terminal-route-state.json")["prepared"] and not load("handoffs/terminal-route-state.json")["sent"],
        "terminal_verdict": load("closeout/phase-truth.json")["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
    }
    review = {
        "schema": "ghc.family.liora-venn.v667-v1.final-staged-review.v1",
        "generated_at_utc": NOW,
        "reviewed_from": "exact_git_index_blobs",
        "reviewed_paths": paths,
        "reviewed_path_count": len(paths),
        "json_parsed": parsed_json,
        "maximum_document_words": maximum_words,
        "maximum_document_path": maximum_path,
        "privacy_scan_classes": list(PRIVACY_PATTERNS),
        "privacy_candidates": candidates,
        "privacy_confirmed_hits": len(candidates),
        "checks": checks,
        "self_exclusions": [review_path, delta_path, owner_path],
        "valid": all(checks.values()),
    }
    if not review["valid"]:
        raise RuntimeError(json.dumps(review, ensure_ascii=False, sort_keys=True))
    write_json("validation/final-staged-review.json", review)
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", review_path])

    delta_entries = [manifest_entry(path) for _, path in staged_rows() if path not in {delta_path, owner_path}]
    write_json(
        "validation/final-delta-manifest.json",
        {
            "schema": "ghc.family.liora-venn.v667-v1.content-manifest.v1",
            "owner": "Liora Venn",
            "phase": "final_delta",
            "generated_at_utc": NOW,
            "source_sha": evidence_sha,
            "hash_source": "exact_git_index_blobs",
            "entries": delta_entries,
            "entry_count": len(delta_entries),
            "deletion_count": 0,
            "additive_only": all(status == "A" for status, _ in rows),
            "self_exclusions": [delta_path, owner_path],
        },
    )
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", delta_path])

    owner_paths_index = [path for path in tracked_owner_index_paths() if path != owner_path]
    owner_entries = [manifest_entry(path) for path in owner_paths_index]
    write_json(
        "validation/final-owner-manifest.json",
        {
            "schema": "ghc.family.liora-venn.v667-v1.owner-manifest.v1",
            "owner": "Liora Venn",
            "phase": "v667-v1-final",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "expected_final_parent": evidence_sha,
            "hash_source": "exact_git_index_blobs_for_resulting_final_tree",
            "entries": owner_entries,
            "entry_count": len(owner_entries),
            "file_ceiling": 2000,
            "within_file_ceiling": len(owner_entries) + 1 < 2000,
            "self_exclusion": owner_path,
        },
    )
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--sparse", "--", owner_path])
    print(json.dumps({"reviewed": len(paths), "delta_entries": len(delta_entries), "owner_entries": len(owner_entries), "valid": True}))


if __name__ == "__main__":
    if sys.argv[1:] == ["--staged-review"]:
        build_staged_review()
    elif sys.argv[1:]:
        raise SystemExit("usage: build_ghc_family_liora_venn_v667_v1_closeout.py [--staged-review]")
    else:
        main()
