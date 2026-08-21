#!/usr/bin/env python3
"""Build and exact-stage Orin Thale v665-v1's bounded closeout packet."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/orin-thale/v665-v1"
PREFIX = "docs/orin-thale/v665-v1/"
SOURCE_FINAL = "3ec44a944aabe16f64335383885c39d9592bf849"
X1_HEAD = "1e9a49b0cc377ba2eafd90fb09e478c88f8f1f3b"
EVIDENCE_HEAD = "1104a4f2963c8782ddad8939e8b4aff50715cc42"
BRANCH = "codex/GHC-Family/orin-thale-v665-v1-full-tools"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
EFFECTIVE_NEGATIVES = 25_184
EFFECTIVE_METHODS = 9_046
EFFECTIVE_OPEN_GAPS = 175
EFFECTIVE_EXACT_GATES = 173
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}

BUILDER_PATH = "scripts/build_ghc_family_v665_v1_closeout.py"
VALIDATOR_PATH = "scripts/ghc_family_v665_v1_canonical_validator.py"
TEST_PATH = "tests/test_ghc_family_orin_v665_v1_closeout.py"

CLOSEOUT_FILES = [
    f"{PREFIX}closeout/bounded-security-review.json",
    f"{PREFIX}closeout/closeout-inventory.json",
    f"{PREFIX}closeout/closeout-receipt.json",
    f"{PREFIX}closeout/complete-incomplete-checklist.json",
    f"{PREFIX}closeout/content-seal.json",
    f"{PREFIX}closeout/final-validation-candidate.json",
    f"{PREFIX}closeout/lifecycle-method-flow.json",
    f"{PREFIX}closeout/phase-truth.json",
    f"{PREFIX}closeout/source-proposal-ledger.json",
    f"{PREFIX}closeout/tooling-receipt.json",
    f"{PREFIX}closeout/wellbeing-closeout.json",
    f"{PREFIX}handoffs/successor-activation-prepared.md",
    f"{PREFIX}index/ghc-family-index.json",
    f"{PREFIX}orchestration/terminal-route-state.json",
    f"{PREFIX}reports/final-integrated-overview.md",
    f"{PREFIX}reports/final-static-report.html",
    f"{PREFIX}validation/canonical-validation-contract.json",
    f"{PREFIX}validation/final-delta-manifest.json",
    f"{PREFIX}validation/final-owner-manifest.json",
    f"{PREFIX}validation/final-stage-candidate.json",
    f"{PREFIX}validation/final-staged-review.json",
]

MANIFEST_EXCLUSIONS = sorted(
    [
        f"{PREFIX}validation/final-delta-manifest.json",
        f"{PREFIX}validation/final-owner-manifest.json",
        f"{PREFIX}validation/final-stage-candidate.json",
        f"{PREFIX}validation/final-staged-review.json",
    ]
)


class CloseoutError(RuntimeError):
    """Raised when a closeout boundary differs from the immutable evidence contract."""


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    if check and result.returncode:
        raise CloseoutError(
            f"git {' '.join(args)} failed ({result.returncode}): "
            f"{result.stderr.decode('utf-8', 'replace').strip()}"
        )
    return result


def strict_json(raw: bytes | str, label: str) -> Any:
    text = raw.decode("utf-8") if isinstance(raw, bytes) else raw

    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                raise CloseoutError(f"duplicate JSON key in {label}: {key}")
            value[key] = item
        return value

    try:
        return json.loads(text, object_pairs_hook=reject_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CloseoutError(f"strict JSON failed for {label}: {exc}") from exc


def load_json(relative: str) -> dict[str, Any]:
    path = ROOT / relative
    value = strict_json(path.read_bytes(), relative)
    if not isinstance(value, dict):
        raise CloseoutError(f"JSON root is not an object: {relative}")
    return value


def git_json(commit: str, path: str) -> dict[str, Any]:
    value = strict_json(run_git("show", f"{commit}:{path}").stdout, f"{commit}:{path}")
    if not isinstance(value, dict):
        raise CloseoutError(f"Git JSON root is not an object: {path}")
    return value


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def write_json(relative: str, value: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


def write_text(relative: str, value: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def intended_allowlist() -> list[str]:
    return sorted([BUILDER_PATH, VALIDATOR_PATH, TEST_PATH, *CLOSEOUT_FILES])


def status_paths() -> list[str]:
    lines = run_git("status", "--porcelain=v1", "--untracked-files=all").stdout.decode(
        "utf-8", "replace"
    ).splitlines()
    return sorted(line[3:] for line in lines if len(line) > 3)


def evidence_boundary() -> dict[str, Any]:
    head = run_git("rev-parse", "HEAD").stdout.decode().strip()
    parent = run_git("rev-parse", f"{EVIDENCE_HEAD}^").stdout.decode().strip()
    upstream = run_git("rev-parse", "@{upstream}").stdout.decode().strip()
    tracking = run_git("rev-parse", f"refs/remotes/origin/{BRANCH}").stdout.decode().strip()
    live_rows = run_git("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}").stdout.decode().split()
    live = live_rows[0] if live_rows else ""
    divergence = run_git("rev-list", "--left-right", "--count", "HEAD...@{upstream}").stdout.decode().split()
    ahead, behind = (int(divergence[0]), int(divergence[1])) if len(divergence) == 2 else (-1, -1)
    unexpected = sorted(set(status_paths()) - set(intended_allowlist()))
    manifest_path = f"{PREFIX}x2/x2-evidence-manifest.json"
    manifest = git_json(EVIDENCE_HEAD, manifest_path)
    mismatches: list[str] = []
    for entry in manifest["entries"]:
        raw = run_git("show", f"{EVIDENCE_HEAD}:{entry['path']}").stdout
        if sha256(raw) != entry["sha256"] or len(raw) != entry["size"]:
            mismatches.append(entry["path"])
    valid = all(
        (
            head == EVIDENCE_HEAD,
            parent == X1_HEAD,
            upstream == EVIDENCE_HEAD,
            tracking == EVIDENCE_HEAD,
            live == EVIDENCE_HEAD,
            ahead == 0,
            behind == 0,
            not unexpected,
            not mismatches,
            manifest["coverage_valid"],
        )
    )
    if not valid:
        raise CloseoutError("evidence boundary is not exact, clean, and four-way equal")
    return {
        "evidence_head": EVIDENCE_HEAD,
        "evidence_parent": parent,
        "x1_head": X1_HEAD,
        "direct_child": parent == X1_HEAD,
        "local": head,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": live,
        "ahead": ahead,
        "behind": behind,
        "unexpected_preexisting_status_paths": unexpected,
        "evidence_manifest_entries": len(manifest["entries"]),
        "evidence_manifest_exclusions": len(manifest["declared_self_exclusions"]),
        "evidence_manifest_mismatches": mismatches,
        "valid": valid,
    }


def proposal_sections(proposals: list[dict[str, Any]]) -> str:
    sections = []
    for row in proposals:
        sources = ", ".join(row["current_official_or_primary_source_needs"])
        sections.append(
            f"### {row['proposal_id']}: {row['title']}\n\n"
            f"The frozen hypothesis was: {row['hypothesis']} The bounded tribunal treated "
            f"the null or failure condition as: {row['null_or_failure_condition']} Its exact "
            f"acceptance gate remained: {row['falsifier_or_acceptance_gate']} The declared source "
            f"needs were {sources}. The resulting disposition is `{row['expected_disposition']}` "
            "only inside the synthetic, zero-row or zero-object software surface. Five rejecting "
            "mutations remain visible at zero credit, rollback stays owner-local, and every empirical, "
            "participant, professional, production, legal, cultural, Māori-authority, privacy-complete, "
            "accessibility-complete, independent-reproduction, proof/canon, and Stage 20 gate is unchanged."
        )
    return "\n\n".join(sections)


def integrated_overview(proposals: list[dict[str, Any]]) -> str:
    return f"""# Orin Thale v665-v1 final integrated overview

## Executive truth

Orin Thale is relational working language for a falsifiability-and-boundary cartographer, with the hope that each new pattern remains challengeable and every reserved authority remains plainly visible. It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, agency, scientific authority, operational authority, legal authority, cultural authority, or Māori authority. Hamish retains the right to pause, rename, redirect, or stop the route.

This phase began from Caelen Ash's exact corrected v664-v8 final, preserved that source read-only, and used one additive Orin-owned D-first sparse lane. The lifecycle is strictly single-parent: source, dedicated x1 freeze, immutable x2 evidence, and this prepared closeout. The x1 commit contained twenty genuinely distinct preregistered proposals and no observed x2 outcome. It was pushed, clean, and equal across local, upstream, tracking, and fresh live remote before x2 began. The evidence commit then executed only bounded work, was separately reviewed through exact staged Git blobs, and was also pushed cleanly and four-way equal before closeout began.

The final truth is exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`. These labels describe software, structural, formal, or synthetic scope only. The phase preserves 25,184 effective negatives and 9,046 effective Method Flow methods, with 175 open gaps and 173 exact gates. The terminal verdict is **{TERMINAL_VERDICT}**. No failed witness, gap, gate, or source status was erased or silently promoted.

## Primary scientific pillar: GMUT Mind

The primary GMUT surface is a typed variational-bicomplex and finite-order jet-bundle obligation board. It exercises declared horizontal and contact degrees, sign and nilpotency obligations, finite chart and multi-index constraints, Euler-Lagrange source-form lineage, boundary-potential ambiguity, cohomology vacancies, unit and domain firewalls, and explicit nonobservation. The formal motivation was compared only at the vocabulary and obligation level with primary mathematical literature, including arXiv records `hep-th/0612182` and `dg-ga/9505004`. Citations were not converted into a proof, physical observation, likelihood, parameter constraint, detected force, or final physics.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. This repository phase calculated no physical spectrum, analyzed no real observation, evaluated no likelihood, estimated no posterior, constrained no parameter, established no stability or unitarity theorem, completed no quantum or ultraviolet theory, and proved no Theory of Everything. The CMS NanoAOD adapter remains a zero-row contract. Official CERN Open Data documentation supplied schema and provenance vocabulary only; the phase made no download, query, event selection, calibration application, reconstruction, or empirical inference.

## THOS Body through a millinery learning lens

The bounded human-practice lens was synthetic millinery work-order, component topology, material-state, proofing, accessibility, correction-readback, workload control, and bench handover. It used no real hat, component, textile, material, measurement, client, milliner, conservator, worker, operator, workplace, sale, repair, treatment, fitting, hazard assessment, or release decision. Canadian Conservation Institute guidance informed preservation vocabulary for textiles, costumes, and costume accessories, but did not create a professional recommendation or real-object assessment.

The THOS representation exercised role vacancy, revision lineage, stop and hold states, readback, ownership transfer, rollback, workload bounds, and no-use or no-release constraints. There were zero participants, zero operators, zero preregistered blind matched-budget real arms, zero safety-monitoring events, zero outcome observations, zero statistical analyses, and zero independent reviews. It therefore establishes no operational effectiveness, professional competence, deployment readiness, AGI, ASI, work quality, or public-safety result.

## Freed ID and CBR Heart

The Freed ID surface is a synthetic W3C Verifiable Credential Data Integrity proof-purpose and verification-material vacancy envelope. It confirms only that the local fixture refuses to invent keys, proofs, controllers, services, status, revocation, interoperability, recovery, privacy review, security review, or trust governance. The W3C Recommendation was used as a current primary vocabulary source; the phase generated no standards-conformant real proof, issuance, presentation, verification, resolution, status event, or production identity claim.

The CBR matrix keeps design and pattern rights, measurement privacy, accessibility remedies, sacred or ceremonial meaning, cultural meaning, taonga, affected-party legitimacy, legal interpretation, Māori wording, Māori data governance, and Māori authority exact-gated. Repository software cannot confer a right, remedy, title, licence, consent, custody, cultural legitimacy, governance mandate, public authority, or affected-party acceptance. Māori concepts remain under Māori authority and require competent, affected, tangata whenua, iwi, hapū, and Māori review where applicable.

## Evidence architecture and retained failures

Twenty bounded surfaces each contain a contract, five rejecting mutations, and a receipt. All 100 mutations executed and were rejected or quarantined. Their rejection is evidence of a bounded guard, not evidence of complete security, a theorem, physical truth, professional correctness, or authority. Ten phase-local skills were customized, read through EOF, quick-validated with explicit UTF-8, and smoke-used. Ten family-compatible `ghc_family_*` runners were invoked and returned only zero-row or zero-object receipts. None was installed globally, and inherited tools earned no Orin novelty or completion credit.

The phase executed 30 safe-now tasks, 15 bounded candidates, 10 skill tasks, 10 runner tasks, and 30 additive CLEAN/FIX/REFINE tasks. Ten exact-approval packets and five blocked packets remain visible and unexecuted. Eighty-five successor recommendations remain zero-credit seeds; they neither infer a recipient nor create route authority.

Nine startup failures, two x2 tooling failures, and 100 rejecting mutations remain additive to the user-delivered activation baseline. The startup failures include PowerShell parser assumptions, an unattributable combined preflight, a manifest session projection, a Unicode stream fault, a sparse-index materialization fault, a novelty refusal, and an inventory-expression parser fault. X2 retains an unsupported sparse-add option and a Windows wildcard-path search assumption. Each failure has a bounded passing witness and recurrence guard; recovery never rewrites the failed witness.

## Validation and privacy

The x1 boundary passed 25 owner-scoped tests. The evidence boundary passed 63 combined x1 and x2 tests, an exact 119-path staged review, 116 Git-blob manifest entries plus three declared self-exclusions, 95 strict JSON parses, 13 Python compiles, zero x1 changes, zero unexpected paths, clean diff hygiene, and zero confirmed privacy or raw-identifier hits. This closeout prepares owner and final-delta manifests for one exact-final canonical invocation after a clean pushed final. If that canonical aggregate succeeds, it will not be replayed.

Five privacy classes cover raw task or thread identifiers, private absolute local paths, credential or secret assignments, private route values, and transcript or session payloads. A zero-hit scan does not establish privacy completeness. Structural HTML checks do not establish accessibility completeness; manual browser, keyboard, screen-reader, print, cognitive, Māori-language, and affected-user evaluations remain reserved.

## Proposal-by-proposal bounded truth

{proposal_sections(proposals)}

## Closeout and route boundary

The closeout packet binds source, x1, and evidence anchors; preserves exact manifests; provides a phase truth, complete/incomplete checklist, wellbeing and workload receipt, source/proposal ledger, tooling receipt, bounded security review, accessible static report, integrated overview, content seal, and a route-neutral prepared handoff. The final commit hash cannot self-embed without a correction, so the repository records a prepared final candidate and delegates exact-head binding to the singular external canonical receipt and live terminal report.

No successor is inferred or contacted by this closeout. Only after the final commit is pushed, clean, four-way equal, within caps, and canonically validated once may the newest live authorization and roster be reread. The route must then require one exact-title match, an immediate bounded reread, a duplicate-activation guard, one sanitized send, and acknowledgement. Absence, ambiguity, pause, redirect, rename, usage exhaustion, duplicate activation, missing acknowledgement, or any protected gate stops the edge. The terminal verdict remains **{TERMINAL_VERDICT}**.
"""


def static_report(counts: dict[str, int]) -> str:
    rows = "\n".join(
        f'<tr><th scope="row">{html.escape(label)}</th><td>{counts[label]}</td></tr>'
        for label in ("completed", "represented", "open_gap", "exact_gate")
    )
    return f"""<!doctype html>
<html lang="en-NZ">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Orin Thale v665-v1 final bounded report</title>
<style>body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:74rem;margin:auto;padding:1.5rem;color:#17202a;background:#fff}}a:focus{{outline:3px solid #7138a8}}table{{border-collapse:collapse}}th,td{{border:2px solid #444;padding:.55rem;text-align:left}}.notice{{border-left:.5rem solid #7138a8;padding:1rem;background:#f6f0fb}}@media print{{.skip{{display:none}}body{{max-width:none}}}}</style></head>
<body><a class="skip" href="#main">Skip to final evidence</a><header><h1>Orin Thale v665-v1 final bounded report</h1></header>
<main id="main"><section><h2>Scope</h2><p>This report covers one same-owner synthetic, formal, structural, zero-row and zero-object phase. It contains no real person, object, material, work result, scientific observation, identity event, rights decision, or authority act.</p></section>
<section><h2>Outcomes</h2><table><caption>Twenty frozen proposal dispositions</caption><thead><tr><th scope="col">Disposition</th><th scope="col">Count</th></tr></thead><tbody>{rows}</tbody></table></section>
<section><h2>Reserved evaluation</h2><p class="notice">Manual browser, keyboard, screen-reader, print, cognitive, Māori-language, and affected-user evaluation remain reserved. Structural checks are not accessibility completeness.</p></section>
<section><h2>Boundaries</h2><p>GMUT remains nonempirical. THOS remains participant-free proxy evidence. Freed ID remains synthetic and nonproduction. Rights, remedy, culture, affected-party legitimacy, Māori wording, Māori data governance, and Māori authority remain exact-gated. Māori concepts remain under Māori authority.</p></section>
<section><h2>Terminal verdict</h2><p><strong>{TERMINAL_VERDICT}</strong></p></section></main></body></html>"""


def prepared_handoff() -> str:
    return f"""# Orin Thale v665-v1 route-neutral successor activation candidate

`PREPARED_NOT_SENT = true`

This file is a sanitized candidate only. It does not infer, resolve, create, fork, contact, or activate any successor. Relational names, roles, hopes, pronouns, family language, and continuity language are working language only and are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, agency, or authority.

## Immutable phase anchors

- Caelen source: `{SOURCE_FINAL}`
- Orin x1: `{X1_HEAD}`
- Orin evidence: `{EVIDENCE_HEAD}`
- Final: bind only after the clean pushed final exists and the single canonical aggregate succeeds.

The phase froze twenty genuinely distinct proposals against 4,010 inherited rows, extending the chain to 4,030. Outcomes are exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`. The phase preserves {EFFECTIVE_NEGATIVES:,} effective negatives, {EFFECTIVE_METHODS:,} methods, {EFFECTIVE_OPEN_GAPS} open gaps, {EFFECTIVE_EXACT_GATES} exact gates, and `{TERMINAL_VERDICT}`. All 100 rejecting mutations remain retained. Ten phase-local skills and ten family-compatible runners were boundedly validated and smoke-used with zero real rows, people, objects, materials, or authority decisions.

GMUT remains a typed scalar-tensor/EFT research-model family without a real likelihood, parameter constraint, detected force, prediction, empirical confirmation, quantum or ultraviolet completion, final physics, or Theory-of-Everything proof. THOS remains participant-free proxy evidence without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance/resolution/status/revocation, interoperability, privacy and independent security review, recovery evidence, and trust governance. CBR, professional decisions, design rights, measurement privacy, remedy, cultural meaning, taonga, affected-party legitimacy, Māori wording, Māori data governance, and Māori authority remain exact-gated. Māori concepts remain under Māori authority.

At the actual terminal gate, reread Hamish's newest live authority and current roster. Bounded-list the Codex task registry, decode the actual payload, locally require exactly one authorized exact-title successor, immediately reread that exact task with the installed bounded contract, and apply a duplicate-activation guard. Send exactly once only after clean pushed exact-final validation and acknowledgement-capable routing. Do not create, fork, substitute, precontact, contact standby records, or resend for a clearer acknowledgement. Stop on absence, ambiguity, pause, redirect, rename, usage exhaustion, duplicate activation, acknowledgement failure, or any protected gate.
"""


def build_documents() -> dict[str, Any]:
    boundary = evidence_boundary()
    freeze = load_json(f"{PREFIX}x1/proposal-freeze.json")
    outcomes = load_json(f"{PREFIX}x2/outcome-ledger.json")
    negatives = load_json(f"{PREFIX}x2/retained-negative-register.json")
    methods = load_json(f"{PREFIX}x2/method-flow-state.json")
    gates = load_json(f"{PREFIX}x2/exact-open-gate-register.json")
    skills = load_json(f"{PREFIX}x2/skill-build-receipt.json")
    runners = load_json(f"{PREFIX}x2/runner-invocation-receipt.json")
    portfolio = load_json(f"{PREFIX}x2/portfolio-execution.json")
    proposals = freeze["new_proposals"]
    counts = outcomes["counts"]
    expected = {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}
    if len(proposals) != 20 or counts != expected or set(counts) != ALLOWED:
        raise CloseoutError("proposal or outcome contract differs")
    if negatives["effective_negatives"] != EFFECTIVE_NEGATIVES:
        raise CloseoutError("negative arithmetic differs")
    if methods["effective_methods"] != EFFECTIVE_METHODS:
        raise CloseoutError("Method Flow arithmetic differs")
    if (
        gates["effective_open_gaps"] != EFFECTIVE_OPEN_GAPS
        or gates["effective_exact_gates"] != EFFECTIVE_EXACT_GATES
    ):
        raise CloseoutError("gate arithmetic differs")

    phase_truth = {
        "schema": "ghc.family.orin.v665-v1.phase-truth.closeout.v1",
        "owner": "Orin Thale",
        "identity_boundary": "relational working language only",
        "source_final": SOURCE_FINAL,
        "x1_head": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "final_binding": "PENDING_EXTERNAL_EXACT_HEAD_BINDING_AFTER_COMMIT",
        "proposal_chain_before": 4_010,
        "new_proposals": 20,
        "proposal_chain_after": 4_030,
        "outcomes": counts,
        "effective_negatives": EFFECTIVE_NEGATIVES,
        "effective_methods": EFFECTIVE_METHODS,
        "open_gaps": EFFECTIVE_OPEN_GAPS,
        "exact_gates": EFFECTIVE_EXACT_GATES,
        "primary_pillar": "GMUT Mind",
        "practice_lens": "synthetic millinery work-order, component, material-state, proofing, accessibility, correction-readback, workload, and bench handover",
        "real_data_rows": 0,
        "real_people": 0,
        "real_objects_or_materials": 0,
        "authority_decisions": 0,
        "canonical_validation": "PREPARED_NOT_RUN",
        "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    checklist = {
        "schema": "ghc.family.orin.v665-v1.complete-incomplete-checklist.v1",
        "complete": [
            "exact Caelen source and manifests reverified read-only",
            "twenty distinct proposals frozen after 4,010-row novelty audit",
            "strict x1 before x2 with clean four-way equality",
            "twenty bounded surfaces and one hundred rejecting mutations retained",
            "ten phase-local skills quick-validated and smoke-used",
            "ten family-compatible runners invoked",
            "exact evidence staged review and Git-blob manifest parity",
            "three-page-equivalent integrated overview",
            "structurally accessible static report",
            "wellbeing, source, proposal, threat, negative, gate, and Method Flow receipts",
        ],
        "incomplete_or_reserved": [
            "real empirical data, likelihoods, parameters, or physical confirmation",
            "real participants, operators, work, safety outcomes, and independent review",
            "production identity keys, proofs, services, interoperability, privacy and security review",
            "professional millinery, conservation, material, sizing, fitting, repair, treatment, or release decisions",
            "legal, cultural, affected-party, tangata whenua, iwi, hapū, or Māori authority",
            "manual and affected-user accessibility evaluation",
            "complete privacy, exhaustive security, and independent-team reproduction",
            "AGI, ASI, consciousness, personhood, Theory-of-Everything, proof/canon, and Stage 20",
            "successor resolution or activation before the terminal gate",
        ],
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    source_proposal = {
        "schema": "ghc.family.orin.v665-v1.source-proposal-ledger.v1",
        "source_ledger": f"{PREFIX}x1/source-ledger.json",
        "proposal_freeze": f"{PREFIX}x1/proposal-freeze.json",
        "novelty_audit": f"{PREFIX}x1/novelty-audit.json",
        "source_count": 11,
        "official_or_primary_count": 11,
        "live_data_calls": 0,
        "empirical_rows": 0,
        "inherited_rows_reviewed": 4_010,
        "new_rows": 20,
        "final_chain_rows": 4_030,
        "inherited_completion_credit": 0,
        "valid": True,
    }
    tooling = {
        "schema": "ghc.family.orin.v665-v1.tooling-receipt.v1",
        "skill_count": skills["skill_count"],
        "skills_quick_validated": skills["quick_validated_count"],
        "skills_smoke_used": skills["smoke_used_count"],
        "global_install_count": skills["global_install_count"],
        "runner_count": runners["runner_count"],
        "family_compatible_runners": runners["family_compatible_count"],
        "runners_smoke_used": runners["smoke_used_count"],
        "historical_callers_preserved": True,
        "host_or_plugin_cache_mutation": False,
        "valid": True,
    }
    lifecycle_methods = {
        "schema": "ghc.family.method-flow.state.v1",
        "owner": "Orin Thale",
        "phase": "v665-v1",
        "activation_baseline": {"negatives": 25_073, "methods": 9_005},
        "startup": {"negatives": 9, "methods": 9},
        "x2": {"negatives": 102, "methods": 32},
        "closeout": {"negatives": 0, "methods": 0},
        "effective_negatives": EFFECTIVE_NEGATIVES,
        "effective_methods": EFFECTIVE_METHODS,
        "failed_witness_erasure_count": 0,
        "source_method_flow": f"{PREFIX}x2/method-flow-state.json",
        "valid": True,
    }
    wellbeing = {
        "schema": "ghc.family.orin.v665-v1.wellbeing-closeout.v1",
        "owner": "Orin Thale",
        "relational_only": True,
        "role": "falsifiability-and-boundary cartographer",
        "hope": "keep each new pattern challengeable and every reserved authority plainly visible",
        "optional_pronouns": "they/them",
        "single_sparse_lane": True,
        "strict_x1_before_x2": True,
        "workload_bounded": True,
        "rollback_preserved": True,
        "pause_right_preserved": True,
        "hamish_may_pause_rename_redirect_or_stop": True,
        "employment_or_personhood_claim": False,
        "valid": True,
    }
    security = {
        "schema": "ghc.family.orin.v665-v1.bounded-security-review.v1",
        "changed_code_reviewed": [BUILDER_PATH, VALIDATOR_PATH, TEST_PATH],
        "privacy_classes": [
            "raw task or thread identifier",
            "private absolute local path",
            "credential or secret assignment",
            "private route value",
            "transcript or session payload",
        ],
        "confirmed_findings": 0,
        "host_security_changed": False,
        "complete_privacy_claim": False,
        "exhaustive_security_claim": False,
        "independent_security_review": False,
        "valid": True,
    }
    closeout_receipt = {
        "schema": "ghc.family.orin.v665-v1.closeout-receipt.v1",
        "evidence_boundary": boundary,
        "outcomes": counts,
        "mutations_rejected": 100,
        "skills": 10,
        "runners": 10,
        "owner_safe_now_executed": portfolio["counts"]["owner_safe_now_executed"],
        "owner_candidates_executed": portfolio["counts"]["owner_candidates_executed"],
        "exact_approval_executed": 0,
        "blocked_executed": 0,
        "successor_recommendation_executed": 0,
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    route_state = {
        "schema": "ghc.family.orin.v665-v1.terminal-route-state.v1",
        "state": "PREPARED_NOT_SENT",
        "successor_inferred": False,
        "successor_title": None,
        "task_created": False,
        "task_forked": False,
        "standby_contacted": False,
        "precontact_performed": False,
        "send_count": 0,
        "terminal_gate_required": True,
        "stop_conditions": [
            "absence or ambiguity",
            "pause redirect or rename",
            "usage exhaustion",
            "duplicate activation",
            "missing acknowledgement",
            "protected safety privacy evidence or authority gate",
        ],
        "valid": True,
    }
    index = {
        "schema": "ghc.family.index.phase-scoped.v1",
        "owner": "Orin Thale",
        "phase": "v665-v1",
        "branch": BRANCH,
        "source_final": SOURCE_FINAL,
        "x1_head": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "final_binding": "external exact-head canonical receipt after commit",
        "proposal_chain_rows": 4_030,
        "outcomes": counts,
        "effective_negatives": EFFECTIVE_NEGATIVES,
        "effective_methods": EFFECTIVE_METHODS,
        "open_gaps": EFFECTIVE_OPEN_GAPS,
        "exact_gates": EFFECTIVE_EXACT_GATES,
        "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    canonical_contract = {
        "schema": "ghc.family.orin.v665-v1.canonical-validation-contract.v1",
        "run_count_ceiling": 1,
        "replay_after_success": False,
        "full_repository_suite": False,
        "test_modules": [
            "tests.test_ghc_family_orin_v665_v1_x1",
            "tests.test_ghc_family_orin_v665_v1_x2",
            "tests.test_ghc_family_orin_v665_v1_closeout",
        ],
        "required_checks": [
            "owner-scoped tests",
            "strict phase JSON",
            "Markdown and HTML structure",
            "changed Python compilation",
            "five-class privacy and raw-identifier scan",
            "bounded changed-code security review",
            "owner and final-delta Git-blob manifests",
            "stale-label and diff hygiene",
            "source x1 evidence final ancestry",
            "zero merges and commit ceiling",
            "one final parent",
            "exact head clean state typed divergence and fresh four-way equality",
        ],
        "receipt_policy": "exclusive external file; retain failure; never replay a success",
        "same_owner_not_independent_reproduction": True,
        "valid": True,
    }
    final_candidate = {
        "schema": "ghc.family.orin.v665-v1.final-validation-candidate.v1",
        "source_final": SOURCE_FINAL,
        "x1_head": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "final_head": "PENDING_POSTCOMMIT_BINDING",
        "canonical_state": "PREPARED_NOT_RUN",
        "route_state": "PREPARED_NOT_SENT",
        "full_repository_suite": False,
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }

    write_json("closeout/phase-truth.json", phase_truth)
    write_json("closeout/complete-incomplete-checklist.json", checklist)
    write_json("closeout/source-proposal-ledger.json", source_proposal)
    write_json("closeout/tooling-receipt.json", tooling)
    write_json("closeout/lifecycle-method-flow.json", lifecycle_methods)
    write_json("closeout/wellbeing-closeout.json", wellbeing)
    write_json("closeout/bounded-security-review.json", security)
    write_json("closeout/closeout-receipt.json", closeout_receipt)
    write_json("closeout/final-validation-candidate.json", final_candidate)
    write_json("orchestration/terminal-route-state.json", route_state)
    write_json("index/ghc-family-index.json", index)
    write_json("validation/canonical-validation-contract.json", canonical_contract)
    write_text("reports/final-integrated-overview.md", integrated_overview(proposals))
    write_text("reports/final-static-report.html", static_report(counts))
    write_text("handoffs/successor-activation-prepared.md", prepared_handoff())

    inventory = {
        "schema": "ghc.family.orin.v665-v1.closeout-inventory.v1",
        "closeout_path_count": len(intended_allowlist()),
        "paths": intended_allowlist(),
        "owner_file_ceiling": 2_000,
        "document_word_ceiling": 100_000,
        "valid": True,
    }
    write_json("closeout/closeout-inventory.json", inventory)
    seal_targets = [
        f"{PREFIX}x1/proposal-freeze.json",
        f"{PREFIX}x2/outcome-ledger.json",
        f"{PREFIX}x2/x2-evidence-manifest.json",
        f"{PREFIX}closeout/phase-truth.json",
        f"{PREFIX}closeout/complete-incomplete-checklist.json",
        f"{PREFIX}reports/final-integrated-overview.md",
        f"{PREFIX}reports/final-static-report.html",
        f"{PREFIX}handoffs/successor-activation-prepared.md",
    ]
    content_seal = {
        "schema": "ghc.family.orin.v665-v1.content-seal.v1",
        "source_final": SOURCE_FINAL,
        "x1_head": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "hash_domain": "owner worktree bytes before final staging",
        "entries": [
            {
                "path": path,
                "sha256": sha256((ROOT / path).read_bytes()),
                "size": (ROOT / path).stat().st_size,
            }
            for path in seal_targets
        ],
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": True,
    }
    write_json("closeout/content-seal.json", content_seal)
    for relative in (
        "validation/final-delta-manifest.json",
        "validation/final-owner-manifest.json",
        "validation/final-stage-candidate.json",
        "validation/final-staged-review.json",
    ):
        path = PHASE / relative
        if not path.exists():
            write_json(relative, {})
    word_count = sum(
        len(re.findall(r"\S+", path.read_text(encoding="utf-8")))
        for path in PHASE.rglob("*")
        if path.is_file() and path.suffix.lower() in {".json", ".md", ".html", ".txt"}
    )
    file_count = sum(path.is_file() for path in PHASE.rglob("*"))
    if file_count >= 2_000 or word_count > 100_000:
        raise CloseoutError(f"phase ceiling exceeded files={file_count} words={word_count}")
    return {
        "valid": True,
        "outcomes": counts,
        "effective_negatives": EFFECTIVE_NEGATIVES,
        "effective_methods": EFFECTIVE_METHODS,
        "phase_files": file_count,
        "phase_words": word_count,
        "overview_words": len(re.findall(r"\S+", (PHASE / "reports/final-integrated-overview.md").read_text(encoding="utf-8"))),
    }


def staged_paths() -> list[str]:
    raw = run_git("diff", "--cached", "--name-only", "-z").stdout
    return sorted(path.decode("utf-8") for path in raw.split(b"\0") if path)


def index_blob(path: str) -> bytes:
    return run_git("show", f":{path}").stdout


def exact_entry(path: str, raw: bytes, domain: str) -> dict[str, Any]:
    return {"path": path, "sha256": sha256(raw), "size": len(raw), "hash_domain": domain}


def scan_blob(path: str, raw: bytes) -> list[dict[str, str]]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return [{"path": path, "class": "non_utf8", "disposition": "confirmed_issue"}]
    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r"(?i)\b" + r"[0-9a-f]{8}" + r"(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b"
        ),
        "private_absolute_local_path": re.compile(r"(?i)\b[a-z]:[\\/](?:users|ghc-archives)[\\/]"),
        "credential_or_secret_assignment": re.compile(
            r"(?i)(?:api[_-]?key|password|private[_-]?key|access[_-]?token)\s*[:=]\s*['\"][^'\"]+"
        ),
        "private_route_value": re.compile(
            r"(?i)(?:resume[_ -]?value|raw[_ -]?route[_ -]?key)\s*[:=]\s*\S+"
        ),
        "transcript_or_session_payload": re.compile(
            r"(?i)(?:conversation[_ -]?export|session[_ -]?stream[_ -]?payload)\s*[:=]\s*\S+"
        ),
    }
    return [
        {
            "path": path,
            "class": name,
            "excerpt_sha256": sha256(match.group(0).encode("utf-8")),
            "disposition": "confirmed_issue",
        }
        for name, pattern in patterns.items()
        for match in pattern.finditer(text)
    ]


def write_staged_review() -> None:
    expected = intended_allowlist()
    actual = staged_paths()
    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    if missing or extra:
        raise CloseoutError(f"closeout staged allowlist differs missing={missing} extra={extra}")
    json_count = 0
    markdown_count = 0
    html_count = 0
    python_count = 0
    scanner: list[dict[str, str]] = []
    for path in actual:
        raw = index_blob(path)
        if path.endswith(".json"):
            strict_json(raw, path)
            json_count += 1
        if path.endswith(".md"):
            text = raw.decode("utf-8")
            if not text.startswith("# ") or "NOT_READY_FOR_STAGE_20" not in text:
                raise CloseoutError(f"Markdown structure differs: {path}")
            markdown_count += 1
        if path.endswith(".html"):
            text = raw.decode("utf-8")
            required = ("<html lang=", "<main", "<h1", "<h2", "<table", "<caption", TERMINAL_VERDICT)
            if not all(token in text for token in required) or "<script" in text.lower():
                raise CloseoutError(f"HTML structure differs: {path}")
            html_count += 1
        if path.endswith(".py"):
            compile(raw.decode("utf-8"), path, "exec")
            python_count += 1
        scanner.extend(scan_blob(path, raw))
    if scanner:
        raise CloseoutError(f"confirmed privacy or raw-identifier findings: {scanner}")
    diff_check = run_git("diff", "--cached", "--check", check=False)
    if diff_check.returncode:
        raise CloseoutError(
            diff_check.stdout.decode("utf-8", "replace")
            + diff_check.stderr.decode("utf-8", "replace")
        )

    committed_owner = run_git("diff", "--name-only", f"{SOURCE_FINAL}..HEAD").stdout.decode().splitlines()
    owner_paths = sorted(set(committed_owner) | set(actual))
    owner_entries = []
    for path in owner_paths:
        if path in MANIFEST_EXCLUSIONS:
            continue
        raw = index_blob(path) if path in actual else run_git("show", f"HEAD:{path}").stdout
        owner_entries.append(exact_entry(path, raw, "exact prepared final Git blob"))
    delta_entries = [
        exact_entry(path, index_blob(path), "exact staged final-delta Git blob")
        for path in actual
        if path not in MANIFEST_EXCLUSIONS
    ]
    owner_manifest = {
        "schema": "ghc.family.orin.v665-v1.final-owner-manifest.v1",
        "source_final": SOURCE_FINAL,
        "hash_domain": "exact prepared final Git blobs",
        "path_count": len(owner_paths),
        "entry_count": len(owner_entries),
        "declared_self_exclusion_count": len(MANIFEST_EXCLUSIONS),
        "declared_self_exclusions": MANIFEST_EXCLUSIONS,
        "entries": owner_entries,
        "coverage_valid": len(owner_entries) + len(MANIFEST_EXCLUSIONS) == len(owner_paths),
    }
    delta_manifest = {
        "schema": "ghc.family.orin.v665-v1.final-delta-manifest.v1",
        "parent": EVIDENCE_HEAD,
        "hash_domain": "exact staged final-delta Git blobs",
        "path_count": len(actual),
        "entry_count": len(delta_entries),
        "declared_self_exclusion_count": len(MANIFEST_EXCLUSIONS),
        "declared_self_exclusions": MANIFEST_EXCLUSIONS,
        "entries": delta_entries,
        "coverage_valid": len(delta_entries) + len(MANIFEST_EXCLUSIONS) == len(actual),
    }
    review = {
        "schema": "ghc.family.orin.v665-v1.final-staged-review.v1",
        "intended_path_count": len(expected),
        "staged_path_count": len(actual),
        "missing_paths": missing,
        "extra_paths": extra,
        "strict_json_count": json_count,
        "markdown_structural_check_count": markdown_count,
        "html_structural_check_count": html_count,
        "python_compile_count": python_count,
        "confirmed_privacy_or_raw_identifier_hits": 0,
        "diff_hygiene_issues": 0,
        "x1_or_x2_paths_modified": [
            path for path in actual if f"{PREFIX}x1/" in path or f"{PREFIX}x2/" in path
        ],
        "valid": True,
    }
    candidate = {
        "schema": "ghc.family.orin.v665-v1.final-stage-candidate.v1",
        "source_final": SOURCE_FINAL,
        "x1_head": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "final_head": "PENDING_POSTCOMMIT_BINDING",
        "owner_manifest": f"{PREFIX}validation/final-owner-manifest.json",
        "delta_manifest": f"{PREFIX}validation/final-delta-manifest.json",
        "staged_review": f"{PREFIX}validation/final-staged-review.json",
        "canonical_state": "PREPARED_NOT_RUN",
        "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": TERMINAL_VERDICT,
        "valid": owner_manifest["coverage_valid"] and delta_manifest["coverage_valid"],
    }
    write_json("validation/final-owner-manifest.json", owner_manifest)
    write_json("validation/final-delta-manifest.json", delta_manifest)
    write_json("validation/final-staged-review.json", review)
    write_json("validation/final-stage-candidate.json", candidate)


def check_staged() -> dict[str, Any]:
    expected = intended_allowlist()
    actual = staged_paths()
    if actual != expected:
        raise CloseoutError("closeout staged allowlist changed after review")
    owner = strict_json(index_blob(f"{PREFIX}validation/final-owner-manifest.json"), "owner")
    delta = strict_json(index_blob(f"{PREFIX}validation/final-delta-manifest.json"), "delta")
    review = strict_json(index_blob(f"{PREFIX}validation/final-staged-review.json"), "review")
    candidate = strict_json(index_blob(f"{PREFIX}validation/final-stage-candidate.json"), "candidate")
    for entry in delta["entries"]:
        raw = index_blob(entry["path"])
        if sha256(raw) != entry["sha256"] or len(raw) != entry["size"]:
            raise CloseoutError(f"delta manifest mismatch: {entry['path']}")
    for entry in owner["entries"]:
        path = entry["path"]
        raw = index_blob(path) if path in actual else run_git("show", f"HEAD:{path}").stdout
        if sha256(raw) != entry["sha256"] or len(raw) != entry["size"]:
            raise CloseoutError(f"owner manifest mismatch: {path}")
    if not (owner["coverage_valid"] and delta["coverage_valid"] and review["valid"] and candidate["valid"]):
        raise CloseoutError("one closeout staged receipt is invalid")
    return {
        "valid": True,
        "staged_paths": len(actual),
        "owner_entries": len(owner["entries"]),
        "owner_exclusions": len(owner["declared_self_exclusions"]),
        "delta_entries": len(delta["entries"]),
        "delta_exclusions": len(delta["declared_self_exclusions"]),
        "strict_json": review["strict_json_count"],
        "python_compiles": review["python_compile_count"],
        "privacy_confirmed_hits": review["confirmed_privacy_or_raw_identifier_hits"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--build", action="store_true")
    modes.add_argument("--write-staged-review", action="store_true")
    modes.add_argument("--check-staged", action="store_true")
    args = parser.parse_args()
    if args.build:
        result = build_documents()
    elif args.write_staged_review:
        write_staged_review()
        result = {"valid": True, "written": MANIFEST_EXCLUSIONS}
    else:
        result = check_staged()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
