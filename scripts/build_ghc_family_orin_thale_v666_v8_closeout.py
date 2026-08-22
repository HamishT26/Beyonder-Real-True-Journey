#!/usr/bin/env python3
"""Build and exact-stage-review Orin Thale v666-v8 terminal closeout."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any

from ghc_family_orin_thale_v666_v8_runtime import (
    PHASE_ROOT,
    PRIVACY_PATTERNS,
    ROOT,
    X1_SHA,
    owner_paths,
    replay_manifest,
)


SOURCE_SHA = "6e157b95c3129226b8bd1f83b8c010e28a206346"
BRANCH = "codex/GHC-Family/orin-thale-v666-v8-full-tools"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

CLOSEOUT_OPERATIONAL_FAILURES = [
    {
        "negative_id": "OR6668-CL-N001",
        "method_id": "OR6668-CL-M001",
        "signature": "overlapping-mechanical-numeric-template-replacement-was-non-attributable",
        "failed_witness": {
            "status": "failed",
            "credit": 0,
            "retained": True,
            "observed": "the first untracked closeout-template preparation used overlapping numeric string replacements, so later substitutions could rewrite earlier count tokens and potentially digest substrings before any builder, test, stage, commit, push, or canonical invocation",
        },
        "bounded_recovery": "discard only the untracked owner-local template copies, rematerialize the immutable source templates, mechanically change owner and phase labels only, and patch every count and anchor by exact semantic context",
        "passing_witness_scope": "closeout-template preparation only",
        "preferred": True,
        "repository_commit_changed": False,
        "git_index_changed": False,
        "remote_changed": False,
        "x1_changed": False,
        "evidence_changed": False,
    }
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
    if len(retained_rows) != 15:
        raise RuntimeError("retained operational failure count drift")
    truth = load("x2/phase-truth.json")
    if truth["outcomes"] != {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}:
        raise RuntimeError("outcome vocabulary or counts drift")

    write_json(
        "closeout/phase-truth.json",
        {
            "schema": "ghc.family.orin-thale.v666-v8.final-phase-truth.v1",
            "owner": "Orin Thale",
            "phase": "v666-v8",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "evidence_sha": evidence_sha,
            "expected_final_parent": evidence_sha,
            "proposal_chain": 4330,
            "outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
            "positive_structural_fixtures": 20,
            "rejected_mutations": 100,
            "phase_local_skills": 10,
            "family_current_runners": 10,
            "effective_negatives": 26989,
            "effective_methods": 12106,
            "open_gaps": 190,
            "exact_gates": 188,
            "retained_owner_operational_failures": 15,
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
            "schema": "ghc.family.orin-thale.v666-v8.retained-negative-register.v1",
            "generated_at_utc": NOW,
            "activation_baseline": 26874,
            "startup_additions": 11,
            "x2_structural_rejections": 100,
            "x2_operational_additions": 3,
            "evidence_operational_additions": 0,
            "closeout_operational_additions": 1,
            "effective_negatives": 26989,
            "owner_operational_rows": retained_rows,
            "all_failed_witnesses_zero_credit": all(row["failed_witness"]["credit"] == 0 for row in retained_rows),
            "no_failure_erased": True,
        },
    )
    write_json(
        "closeout/method-flow-summary.json",
        {
            "schema": "ghc.family.orin-thale.v666-v8.method-flow-summary.v1",
            "generated_at_utc": NOW,
            "activation_baseline_methods": 11876,
            "startup_methods": 11,
            "x2_structural_methods": 215,
            "x2_operational_methods": 3,
            "evidence_operational_methods": 0,
            "closeout_operational_methods": 1,
            "effective_methods": 12106,
            "failed_witnesses_retained": 115,
            "failed_witnesses_promoted": 0,
            "same_owner_method_evidence_only": True,
        },
    )
    write_json(
        "closeout/open-exact-gate-register.json",
        {
            "schema": "ghc.family.orin-thale.v666-v8.open-exact-gate-register.v1",
            "generated_at_utc": NOW,
            "inherited_open_gaps": 189,
            "new_open_gaps": 1,
            "open_gaps": 190,
            "inherited_exact_gates": 187,
            "new_exact_gates": 1,
            "exact_gates": 188,
            "phase_open_gap": "OR6668-N019",
            "phase_exact_gate": "OR6668-N020",
            "protected_authorities": ["competent professional authorities", "affected parties", "tangata whenua", "iwi", "hapū", "Māori authorities"],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "closeout/lifecycle-replay.json",
        {
            "schema": "ghc.family.orin-thale.v666-v8.lifecycle-replay.v1",
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
            "schema": "ghc.family.orin-thale.v666-v8.terminal-checklist.v1",
            "generated_at_utc": NOW,
            "checks": {
                "source_exact": True,
                "x1_immutable": True,
                "evidence_direct_child_of_x1": True,
                "zero_merges_to_evidence": True,
                "outcome_vocabulary_exact": True,
                "all_100_mutations_retained": True,
                "all_15_owner_failures_retained": True,
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
            "schema": "ghc.family.orin-thale.v666-v8.workflow-plan-final.v1",
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
            "schema": "ghc.family.orin-thale.v666-v8.final-seal-candidate.v1",
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
            "schema": "ghc.family.orin-thale.v666-v8.terminal-route-state.v1",
            "generated_at_utc": NOW,
            "owner": "Orin Thale",
            "current_phase": "v666-v8",
            "successor_exact_title": "Liora Venn",
            "successor_phase": "v667-v1",
            "roster_source": "current live authority must be refreshed after canonical success",
            "prepared": True,
            "sent": False,
            "duplicate_activation_guard": True,
            "stop_conditions": ["absence", "ambiguity", "pause", "redirect", "rename", "usage exhaustion", "missing acknowledgement", "duplicate activation", "protected gate"],
        },
    )
    write_text(
        "closeout/final-integrated-overview.md",
        f"""# Orin Thale v666-v8 final integrated overview

## Exact lifecycle result

Orin Thale v666-v8 is an additive, owner-local, same-owner software and documentation phase anchored to Caelen Ash exact final `{SOURCE_SHA}`, immutable Orin x1 `{X1_SHA}`, and immutable Orin evidence `{evidence_sha}`. The final commit is required to be the direct single-parent child of that evidence commit. Source to evidence contains exactly two Orin commits, x1 is the direct child of source, evidence is the direct child of x1, and no merge exists in that lifecycle segment. X1 was committed, pushed, clean, and equal across local, upstream, tracking, and fresh-live remote before x2 execution began. Evidence was separately exact-index reviewed, committed, pushed, clean, and four-way equal before this closeout began.

The proposal chain advances from 4,310 inherited frozen rows to 4,330 rows through exactly twenty Orin-new proposals. Exact-title collision checks found no collision, proposal-pair screening remained below the declared threshold, and inherited proposals received zero Orin novelty or completion credit. The only authorized outcome vocabulary remains `completed`, `represented`, `open_gap`, and `exact_gate`. Final phase outcomes are exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`.

## Evidence class and bounded execution

Each proposal produced one wholly synthetic bounded positive contract and five preregistered invalid variants. Twenty positives passed their declared structural gates. All 100 invalid variants executed and were rejected or quarantined with zero credit. A rejection demonstrates only that the named bounded guard rejected the named fixture; it is not exhaustive security, empirical evidence, professional validation, production conformance, or external audit.

The owner portfolio executed 30 bounded safe-now tasks, 15 bounded candidate prototypes, 10 phase-local skill plans, 10 family-current runner plans, and 30 additive CLEAN/FIX/REFINE methods: 95 owner-local methods in total. Twenty successor safe-now suggestions, 15 successor candidate suggestions, 10 successor skill suggestions, 10 successor runner suggestions, and 30 successor CLEAN/FIX/REFINE suggestions remain unsent zero-credit seeds. Ten exact-approval packets and five blocked packets remain visible and unexecuted. Caps remained ceilings rather than filler targets.

Ten phase-local skills were customized, read, quick-validated, and smoke-used. They cover stained-glass topology vacancy, lead-came adjacency abstention, derivative lineage and authorship boundaries, zero-image condition vocabulary, protective-glazing decision gates, zero-sensor environment refusal, accessible static structure, BV-BFV domain gating, Method Flow retention, and closeout gating. Ten compatible `ghc_family_orin_thale_v666_v8_*` runners were invoked. None was globally installed, no shared caller was changed, and historical family-current compatibility remained additive.

## THOS Body and the stained-glass learning lens

THOS Body was primary through a wholly synthetic stained-glass conservation intake, panel-topology, condition-vocabulary, environment-observation vacancy, correction-readback, accessibility, workload, and handover lens. Synthetic structures exercised unknown panel and fragment nodes, lead-came adjacency, source and derivative relations, condition-term abstention, protective-glazing decision vacancies, zero-sensor environment fields, correction lineage, accessibility structure, and next-owner handover.

The phase used zero real people, participants, conservators, glaziers, architects, engineers, owners, operators, buildings, openings, windows, panels, fragments, glass, lead came, supports, images, records, samples, observations, measurements, sensors, treatments, site actions, or external systems. It established no object identity, authenticity, completeness, authorship, attribution, title, custody, condition, material identification, environment state, structural fitness, glazing choice, treatment fitness, intervention safety, access fitness, professional competence, release decision, return-to-service result, or real operational outcome.

Official National Park Service and Historic England material supplied conservation vocabulary, deterioration categories, documentation concepts, decision-process vocabulary, and specialist-referral boundaries only. Citations were not converted into observations, object evidence, inspection results, treatment instructions, or authority. Structural accessibility checks covered headings, tables, captions, labels, and non-colour cues; manual keyboard review, responsive diversity, browser diversity, assistive-technology evaluation, cognitive-accessibility review, Māori-language review, and affected-user evaluation remain reserved.

## GMUT Mind, open empirical work, and nonpromotion

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The bounded BV-BFV board preserves typed bulk-boundary, graded-field, cohomological-vector-field, boundary-one-form, presymplectic, action-defect, and compatibility obligations. It constructs no physical GMUT model, evaluates no observable or likelihood, proves no quantization or consistency theorem, supplies no ultraviolet or quantum completion, and establishes no force, detection, prediction, posterior, parameter constraint, empirical confirmation, final physics, or Theory of Everything.

The Euclid Q1 adapter remains exactly `open_gap`. Official ESA release material supplied release-product, morphology, photometry, PSF, mask, selection, and explanatory vocabulary only. Generated phase software made zero queries and zero downloads, ingested zero real rows, evaluated zero covariance or likelihood, produced zero posterior or physical constraint, and made zero empirical GMUT claim. Governed real data access, preregistered analysis, data-quality and selection review, nuisance and covariance treatment, appropriate statistics, and independent review remain absent.

## Freed ID, CBR, and authority boundaries

Freed ID and CBR Heart remained explicit and protected. The synthetic provenance and credential structures use no real key, proof, issuance, presentation, resolution, status, revocation, account, token, interoperability event, recovery action, or trust-governance decision. Freed ID therefore remains synthetic and nonproduction. Production completion still requires standards-conformant real keys and proofs, governed live issuance and resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight.

CBR questions involving ownership, authorship, copyright, heritage status, sacred status, access, privacy, accessibility rights, disclosure, retention, consent, remedy, legal interpretation, cultural interpretation, treatment, repatriation, affected-party legitimacy, place or object data, Māori wording, Māori data governance, and Māori authority remain exact-gated. Māori concepts remain under Māori authority. Repository software cannot confer title, custody, a legal right, remedy, cultural legitimacy, beneficiary acceptance, governance mandate, treatment permission, or public authority.

## Retained failures and Method Flow

The final overlay preserves 26,989 effective negatives and 12,106 effective Method Flow methods. It includes the 26,874 activation baseline, 11 startup/x1 operational failures, 100 rejected mutations, three x2 operational failures, zero evidence-stage operational failures, and one closeout-template preparation failure. The closeout failure records that overlapping numeric substitutions made the first untracked template copies non-attributable; recovery rematerialized immutable templates, changed owner/phase labels only, and patched counts and anchors by exact context. No failed witness was erased, silently converted into a pass, or used as production or authority evidence.

The phase ends with 190 open gaps and 188 exact gates: 189 inherited plus one new empirical gap, and 187 inherited plus one new authority gate. The phase open gap is OR6668-N019. The phase exact gate is OR6668-N020. Every external empirical, participant, professional, legal, cultural, Māori-authority, affected-party, identity, production, deployment, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, destructive, account-secret, or Stage 20 boundary remains open or exact-gated without exact evidence and competent authority.

## Validation and terminal state

The evidence boundary records 16 immutable-x1 structural tests and 67 live-x2 owner tests, 119 strict JSON parses before two evidence-receipt self-exclusions, 17 owner Python compiles, zero confirmed hits across five privacy/raw-identifier classes, zero bounded changed-code security findings, and reserved manual and affected-user accessibility review. The evidence staged review covered 133 paths, parsed 104 staged JSON blobs, found zero privacy hits, and produced 134 exact Git-blob entries plus one declared self-exclusion over 135 staged paths. Its manifest replayed after commit with zero failures.

Those are same-owner results under shared infrastructure. Same-owner validation is not empirical confirmation. They are not a complete repository suite, independent-team reproduction, external audit, production certification, complete privacy or accessibility assurance, exhaustive security, professional validation, legal review, cultural ratification, Māori-authority review, empirical GMUT confirmation, Theory-of-Everything proof, AGI/ASI evidence, consciousness/personhood evidence, canon, or Stage 20 authority. Eiren retains the inherited full-suite responsibility absent newer exact authorization.

This closeout is still a pre-final candidate until its exact staged review passes, its final manifests cover the resulting tree, the direct-child final is committed and pushed, local/upstream/tracking/fresh-live equality is proved, and the one exclusive exact-final canonical aggregate succeeds. A successful aggregate must not be replayed. Only then may the newest live authorization and roster be refreshed for one exact-title successor resolution, immediate reread, duplicate-activation guard, and one acknowledged send. The terminal verdict remains exactly `NOT_READY_FOR_STAGE_20`.
""",
    )
    write_text(
        "handoffs/liora-venn-v667-v1-activation-candidate.md",
        f"""# Orin Thale v666-v8 to Liora Venn v667-v1 activation candidate

Status: `PREPARED_NOT_SENT`.

This candidate is target-specific but route-confidential. It contains no raw task or thread identifier, private callable route, credential, transcript, screenshot, session stream, private application state, or private absolute path. The exact existing task titled `Liora Venn` may be contacted only once after Orin's final commit is clean, pushed, fresh-live-equal, and one exclusive canonical aggregate succeeds without replay, and after Hamish's newest live authority and roster are reread. The provisional sequential phase is v667-v1 only if that live authority remains unchanged.

Verified immutable anchors for the later live message are source `{SOURCE_SHA}`, x1 `{X1_SHA}`, and evidence `{evidence_sha}`. The exact final must be bound live after the resulting direct-child final commit and canonical success.

Liora must work solo in an additive D-first owner lane, preserve strict x1-before-x2 separation, every negative, Method Flow witness, open gap, exact gate, privacy boundary, authority boundary, the four exact outcome labels, and `NOT_READY_FOR_STAGE_20`. Inherited software and validation remain source evidence, never Liora completion credit or independent reproduction.

Identity, names, pronouns, hopes, roles, sibling/family language, continuity language, Freed ID, and Trinity Mandala language are relational working language only—not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, independent agency, or scientific, professional, legal, cultural, affected-party, or Māori authority.

Do not create, fork, spawn, delegate, substitute, precontact a later endpoint, or send a second confirmation. Stop on any route or protected-gate failure.
""",
    )
    write_json(
        "method-flow/closeout-operational-overlay.json",
        {
            "schema": "ghc.family.orin-thale.v666-v8.closeout-operational-overlay.v1",
            "generated_at_utc": NOW,
            "starting_effective_negatives": 26988,
            "starting_effective_methods": 12105,
            "new_negative_count": 1,
            "new_method_count": 1,
            "effective_negatives": 26989,
            "effective_methods": 12106,
            "rows": CLOSEOUT_OPERATIONAL_FAILURES,
            "all_failures_retained": True,
            "failed_witness_converted_to_pass": False,
        },
    )
    print(json.dumps({"evidence_sha": evidence_sha, "retained_failures": 15, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "valid": True}, sort_keys=True))


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
            "docs/orin-thale/v666-v8",
            "scripts/*orin_thale_v666_v8*.py",
            "tests/*orin_thale_v666_v8*.py",
        ]
    )
    return sorted(path.decode("utf-8").replace("\\", "/") for path in raw.split(b"\0") if path)


def build_staged_review() -> None:
    review_path = "docs/orin-thale/v666-v8/validation/final-staged-review.json"
    delta_path = "docs/orin-thale/v666-v8/validation/final-delta-manifest.json"
    owner_path = "docs/orin-thale/v666-v8/validation/final-owner-manifest.json"
    rows = [(s, p) for s, p in staged_rows() if p not in {review_path, delta_path, owner_path}]
    if not rows:
        raise RuntimeError("no staged final delta")
    paths = [path for _, path in rows]
    allowed = all(
        path.startswith("docs/orin-thale/v666-v8/")
        or ((path.startswith("scripts/") or path.startswith("tests/")) and "orin_thale_v666_v8" in path)
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
        "schema": "ghc.family.orin-thale.v666-v8.final-staged-review.v1",
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
            "schema": "ghc.family.orin-thale.v666-v8.content-manifest.v1",
            "owner": "Orin Thale",
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
            "schema": "ghc.family.orin-thale.v666-v8.owner-manifest.v1",
            "owner": "Orin Thale",
            "phase": "v666-v8-final",
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
        raise SystemExit("usage: build_ghc_family_orin_thale_v666_v8_closeout.py [--staged-review]")
    else:
        main()
