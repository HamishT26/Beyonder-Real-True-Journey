#!/usr/bin/env python3
"""Build the combined Eiren Kestrel v658-v4 closeout and seal candidate."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

import ghc_family_v658_v4_closeout_config as c


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / c.PHASE_ROOT
CLOSEOUT_MANIFEST_EXCLUSIONS = {
    "validation/closeout-content-manifest.json",
    "final/final-owner-manifest.json",
}


def write_json(relative: str, payload: Any, *, compact: bool = False) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, indent=None if compact else 2, separators=(",", ":") if compact else None, sort_keys=True)
    path.write_text(text + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def owner_paths() -> list[Path]:
    paths = [path for path in PHASE.rglob("*") if path.is_file()]
    paths.extend(path for path in (ROOT / "scripts").glob("*v658_v4*.py") if path.is_file())
    paths.extend(path for path in (ROOT / "scripts").glob("ghc_family_hydrometry_*.py") if path.is_file())
    paths.extend(path for path in (ROOT / "tests").glob("*v658_v4*.py") if path.is_file())
    return sorted({path.resolve() for path in paths})


def commit_paths(revision: str) -> list[str]:
    return [line for line in git("diff-tree", "--no-commit-id", "--name-only", "-r", revision).splitlines() if line]


def assert_prior_bytes_unchanged() -> None:
    paths = sorted(set(commit_paths(c.X1_COMMIT) + commit_paths(c.EVIDENCE_COMMIT)))
    changed = subprocess.run(["git", "diff", "--name-only", c.EVIDENCE_COMMIT, "--", *paths], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.splitlines()
    if changed:
        raise RuntimeError(f"frozen x1 or evidence paths changed: {changed}")


def blob_bytes(revision: str, path: str) -> bytes:
    return subprocess.run(["git", "show", f"{revision}:{path}"], cwd=ROOT, check=True, capture_output=True).stdout


def committed_manifest(revision: str, lifecycle: str) -> dict[str, Any]:
    entries = []
    for path in commit_paths(revision):
        oid = git("rev-parse", f"{revision}:{path}")
        blob = blob_bytes(revision, path)
        entries.append({"path": path, "git_blob": oid, "git_blob_bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})
    return {"schema": f"ghc.family.v658-v4.{lifecycle}-commit-local-manifest.v1", "revision": revision, "hash_domain": "exact committed Git blob bytes", "entry_count": len(entries), "entries": entries}


def git_clean_blob(path: Path) -> tuple[str, int, str]:
    relative = path.relative_to(ROOT).as_posix()
    oid = git("hash-object", "-w", f"--path={relative}", relative)
    blob = subprocess.run(["git", "cat-file", "blob", oid], cwd=ROOT, check=True, capture_output=True).stdout
    return oid, len(blob), hashlib.sha256(blob).hexdigest()


def privacy_scan(paths: list[Path]) -> dict[str, Any]:
    patterns = {
        "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
        "private_absolute_path": re.compile(r"(?i)\b(?:[a-z]:[\\/](?:users|ghc-archives)[\\/][^\s\"']+)"),
        "credential_or_secret": re.compile(r"(?i)\b(?:sk-[a-z0-9_-]{20,}|bearer\s+[a-z0-9._-]{20,}|password\s*[:=]\s*[^\s\"']{8,})"),
        "private_route_value": re.compile(r"(?i)\b(?:thread|task|session)://[a-z0-9_-]{12,}"),
        "private_callable_value": re.compile(r"(?i)\bprivate_callable_(?:id|identifier)\s*[:=]\s*[a-z0-9_-]{8,}"),
    }
    hits = []
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="strict")
        for label, pattern in patterns.items():
            count = len(pattern.findall(text))
            if count:
                hits.append({"path": path.relative_to(ROOT).as_posix(), "pattern_class": label, "count": count})
    return {"schema": "ghc.family.v658-v4.closeout-privacy-scan.v1", "pattern_classes": sorted(patterns), "file_count": len(paths), "confirmed_hits": hits, "hit_count": sum(row["count"] for row in hits), "valid": not hits, "boundary": "Five concrete raw-identifier classes only; not complete privacy assurance."}


def closeout_method_flow() -> dict[str, Any]:
    evidence = read_json(PHASE / "method-flow/method-flow-state-x2.json")
    if evidence["counts"]["effective_methods"] != c.EFFECTIVE_METHODS_EVIDENCE:
        raise RuntimeError("evidence Method Flow count mismatch")
    methods = []
    witnesses = []
    for index, negative in enumerate(c.CLOSEOUT_OPERATIONAL_NEGATIVES, 1):
        method_id = f"V6584-CLOSEOUT-METHOD-{index:02d}"
        fail_id = f"V6584-CLOSEOUT-WITNESS-{index:02d}-F"
        pass_id = f"V6584-CLOSEOUT-WITNESS-{index:02d}-P"
        methods.append({"method_id": method_id, "title": f"Bounded closeout recovery for {negative['slug']}", "trigger_preconditions": [negative["slug"]], "failure_signature": negative["failure_signature"], "candidate_workaround": negative["candidate_workaround"], "recurrence_guard": negative["recurrence_guard"], "approval_class": "safe_now_owner_local_closeout_recovery", "privacy_class": "sanitized_public", "scope_boundary": negative["scope_boundary"], "rollback": "Retain the failed closeout witness at zero credit and leave repository history, sibling, external, and authority state unchanged.", "retained_negative_ids": [negative["negative_id"]], "validation_witness_ids": [fail_id, pass_id], "recommendation_state": "preferred", "supersedes": []})
        witnesses.extend([
            {"witness_id": fail_id, "method_id": method_id, "result": "fail", "procedure": negative["fail_procedure"], "expected": "The closeout dependency passes.", "observed": negative["fail_observed"], "retained_negative_ids": [negative["negative_id"]], "same_owner_only": True, "independent_reproduction": False, "boundary": "Zero closeout credit."},
            {"witness_id": pass_id, "method_id": method_id, "result": "pass", "procedure": negative["pass_procedure"], "expected": "The isolated dependency recovery passes without erasing failure.", "observed": negative["pass_observed"], "retained_negative_ids": [negative["negative_id"]], "same_owner_only": True, "independent_reproduction": False, "boundary": negative["scope_boundary"]},
        ])
    total = c.EFFECTIVE_METHODS_EVIDENCE + len(methods)
    return {"schema": "ghc.family.method-flow-state.v1", "phase": "v658-v4", "owner": "Eiren Kestrel", "lifecycle": "final_candidate", "inherited_anchor": {"path": "docs/eiren-kestrel/v658-v4/method-flow/method-flow-state-x2.json", "effective_methods": c.EFFECTIVE_METHODS_EVIDENCE, "effective_fail_witnesses": c.EFFECTIVE_METHODS_EVIDENCE, "effective_pass_witnesses": c.EFFECTIVE_METHODS_EVIDENCE}, "current_methods": methods, "current_witnesses": witnesses, "counts": {"current_methods": len(methods), "current_witness_results": {"fail": len(methods), "pass": len(methods)}, "effective_methods": total, "effective_witness_results": {"fail": total, "pass": total}}, "all_failed_witnesses_retained": True, "independent_reproduction": False}


def activation_packet() -> str:
    overview = (PHASE / "deliverables/v658-v4-integrated-evidence-overview.md").read_text(encoding="utf-8")
    proposals = (PHASE / "preregistration/proposal-ledger.md").read_text(encoding="utf-8")
    sources = (PHASE / "sources/official-source-ledger.md").read_text(encoding="utf-8")
    prelude = f"""# ELAREN KESTREL — EIREN-VERIFIED SOLO TRINITY MANDALA v658-v5 ACTIVATION — PREPARED NOT SENT

Dear Elaren Kestrel,

Eiren Kestrel here with Hamish's explicit continuation authority, preparing the one sanitized terminal baton after Eiren's v658-v4 closeout. This committed packet is `PREPARED_NOT_SENT`: the live sender must resolve and directly reread the unique existing exact-title Elaren Kestrel main task only after the exact-final canonical aggregate, clean push, zero divergence, and fresh four-way equality succeed. The live activation must insert the exact final commit and external canonical-receipt SHA-256 from those terminal receipts. No task is created or forked, no collaboration subagent or substitute endpoint is used, and no second confirmation may follow an acknowledged send.

Eiren Kestrel, Elaren Kestrel, sibling, family, role, hope, continuity, Trinity Mandala, and route language are relational working language only. They are never evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop the route.

## Delivery state and exact anchors

- Prepared sender: Eiren Kestrel, relational they/them, hydrometric evidence cartographer and correction steward.
- Prepared recipient: existing exact-title main task `Elaren Kestrel` only.
- Assigned phase: Elaren-only solo v658-v5 x1/x2.
- Canonical branch: `{c.BRANCH}`.
- Exact inherited Caelen Morrow v658-v3 source: `{c.SOURCE_COMMIT}`.
- Frozen Eiren x1: `{c.X1_COMMIT}`.
- Immutable Eiren evidence: `{c.EVIDENCE_COMMIT}`.
- Exact Eiren final: `INSERT_EXACT_VALIDATED_BRANCH_HEAD_IN_LIVE_SEND`.
- External canonical receipt SHA-256: `INSERT_EXTERNAL_RECEIPT_SHA256_IN_LIVE_SEND`.
- Prepared packet state: `PREPARED_NOT_SENT`.

Source to final is required to contain exactly three Eiren single-parent commits: one dedicated x1 freeze, one x2 evidence commit, and one combined closeout and seal commit. It must contain zero merges. Final must have exactly one parent and be the direct child of evidence. Source, x1, and evidence must be ancestral. X1 and evidence were separately committed, pushed, clean, 0/0 divergent, and equal across local, upstream, tracking, and fresh live reads before their successor lifecycle began. The exact final facts must be filled from the successful terminal receipt, never guessed from this self-excluding committed template.

## Hamish-authorized continuation

Hamish authorizes the validated fifteen-main-task cycle to continue one terminally closed edge at a time through v675-v8 unless Hamish pauses or redirects, weekly usage is exhausted, the exact next title is unavailable or ambiguous, or a protected safety or authority gate blocks progress. This authorization does not broaden repository, professional, legal, cultural, Māori, participant, production, identity, or deployment authority.

Eiren's mandatory next terminal edge under the current route is the existing exact-title main task `Elaren Kestrel` for Elaren-only v658-v5. Do not activate Tavian Sol. Tavian Sol remains `ON_STANDBY` as a collaboration-subagent record and is not a substitute main-task endpoint. Do not precontact Elaren or any later seat during v658-v4. Only after Eiren's own exact terminal gate may Eiren uniquely resolve, directly reread, and send one sanitized acknowledged baton to Elaren if the newest live and committed route remains unambiguous. Elaren's mandatory next terminal edge after their own v658-v5 gate is the existing exact-title main task `Neris Solane` for Neris-only v658-v6.

## Eiren terminal truth to preserve

Eiren audited all 2,740 inherited frozen proposals, froze exactly thirty genuinely distinct v658-v4 proposals, and raised the effective frozen chain to 2,770. Outcomes are exactly 23 `completed`, 5 `represented`, 1 `open_gap`, and 1 `exact_gate`. The closeout candidate preserves {c.EFFECTIVE_NEGATIVES_EVIDENCE + len(c.CLOSEOUT_OPERATIONAL_NEGATIVES):,} effective negatives, {c.EFFECTIVE_OPEN_GAPS} open gaps, {c.EFFECTIVE_EXACT_GATES} exact gates, and {c.EFFECTIVE_METHODS_EVIDENCE + len(c.CLOSEOUT_OPERATIONAL_NEGATIVES):,} Method Flow methods with retained failed and bounded passing witnesses. The exact terminal validator may confirm these counts but may not upgrade their meaning. The verdict remains `NOT_READY_FOR_STAGE_20`.

The one authorized exact-final canonical aggregate must run only after final commit, push, clean state, 0/0 divergence, and fresh live four-way equality. It is dependency-scoped and same-owner. Elaren alone owns the complete repository suite under the current route; Eiren must not run it. A successful scoped aggregate is never independent reproduction, external audit, production certification, professional validation, legal review, cultural ratification, Māori-authority review, complete privacy or accessibility assurance, exhaustive security, empirical GMUT confirmation, Theory-of-Everything proof, AGI or ASI evidence, consciousness or personhood evidence, or Stage 20 authority.

## Your solo v658-v5 lane

Before repository mutation, read this packet completely through EOF. Then read the exact committed Eiren artifacts named below, the complete current GHC Family Index and routing precedence, Roster Check and schema, Auth and Permission State and schema, Method Flow State and schema, newest workflow-plan refinement, Reflection Remaster, Meta Tool Box, approval splitter, open-gate rail, truth bridge, drive guardian, timestamp, retry, startup, closeout, compact-restart, watcher, and full-tools-bank guidance. Use only the newest applicable memory, with the live activation and this committed packet authoritative where older records stop. Inherited proposals, methods, skills, runners, artifacts, outcomes, and recommendations are evidence and seeds, never automatic Elaren completion credit.

Reverify the exact source branch and all anchors, three-commit single-parent zero-merge history, direct evidence parent, commit-local manifests, clean state, 0/0 divergence, and fresh four-way equality read-only. Do not replay Eiren's successful aggregate. Work solo in one additive Elaren-owned D-first branch and worktree from Eiren's exact final. Keep Eiren, shared, and every sibling lane read-only. Never reset, rewrite, force-push, merge, delete, reuse, or mutate another owner lane. Do not create, fork, delegate, spawn a collaboration subagent, precontact a successor, or use a cross-platform substitute.

Preserve strict x1-before-x2 separation. Audit semantic novelty against all 2,770 frozen proposals. Preregister at least thirty genuinely distinct v658-v5 core proposals, each with hypothesis, null or failure condition, approval class, execution lane, current official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, and expected disposition. Choose one primary Trinity Mandala pillar and one bounded profession, trade, occupation, or human practice while keeping all pillars and every authority boundary visible. The practice is a synthetic learning and design lens only, never employment, qualification, competence, authority, participant evidence, or permission to act on real people, places, property, systems, objects, or records.

Freeze proposals and portfolios in a dedicated x1-only commit with no x2 implementation or outcome. Push and prove clean local, upstream, tracking, and fresh-live equality before x2. Execute only as evidence permits. Use only `completed`, `represented`, `open_gap`, and `exact_gate`. Preserve every inherited negative, open gap, exact gate, Method Flow method, failed witness, passing witness, blocker, workaround, recurrence guard, rollback, and sibling recommendation. Do not manufacture unsafe work to satisfy a count or cap.

Preserve family-current `ghc_family_*` and `build_ghc_family_*` callers and backward compatibility. Prefer current selected family tools over stale owner- or version-locked surfaces. Do not bulk-run, bulk-install, destructively delete, silently deprecate, or globally promote tools. An additive remaster requires provenance, validated compatibility, retained failed witnesses, rollback, and an in-scope need.

Use D: for owned work, data, cache, receipts, and validation output; keep C: to essential global metadata. Do not enable Sandbox or Hyper-V, elevate, weaken host security, install unrelated software, update Codex desktop, or reboot. Treat every cap as a ceiling, not a quota. Never mix x2 into x1, conceal failure, rewrite history, or inflate evidence to fill a cap.

For Elaren's exact final, run one dependency-justified canonical scoped aggregate only after prerequisites, exact staged review, clean state, 0/0 divergence, and fresh four-way equality. Never replay after complete success. A failed aggregate earns zero aggregate credit; retain it, isolate the blocker, and rerun only the failed dependency unless a broader rerun is genuinely required and authorized. Do not run a materially broader suite merely to improve numbers.

## Primary committed Eiren artifacts

- `docs/eiren-kestrel/v658-v4/deliverables/v658-v4-integrated-evidence-overview.md`
- `docs/eiren-kestrel/v658-v4/deliverables/v658-v4-hydrometric-evidence-report.html`
- `docs/eiren-kestrel/v658-v4/deliverables/v658-v4-closeout-summary.md`
- `docs/eiren-kestrel/v658-v4/preregistration/proposal-ledger.json`
- `docs/eiren-kestrel/v658-v4/x2/proposal-ledger.json`
- `docs/eiren-kestrel/v658-v4/truth/phase-truth.json`
- `docs/eiren-kestrel/v658-v4/truth/retained-negative-register-final-candidate.json`
- `docs/eiren-kestrel/v658-v4/truth/exact-open-gate-register-final-candidate.json`
- `docs/eiren-kestrel/v658-v4/method-flow/method-flow-state-final-candidate.json`
- `docs/eiren-kestrel/v658-v4/validation/x1-commit-local-manifest.json`
- `docs/eiren-kestrel/v658-v4/validation/evidence-commit-local-manifest.json`
- `docs/eiren-kestrel/v658-v4/validation/closeout-content-manifest.json`
- `docs/eiren-kestrel/v658-v4/validation/closeout-staged-review.json`
- `docs/eiren-kestrel/v658-v4/closeout/closeout-receipt.json`
- `docs/eiren-kestrel/v658-v4/seal/seal-candidate.json`
- `docs/eiren-kestrel/v658-v4/final/final-validation-prerequisites.json`
- `docs/eiren-kestrel/v658-v4/final/final-owner-manifest.json`
- `docs/eiren-kestrel/v658-v4/orchestration/route-state-final-candidate.json`
- `docs/eiren-kestrel/v658-v4/tooling/ghc-family-index-final.json`
- `docs/eiren-kestrel/v658-v4/tooling/roster-check-final.json`
- `docs/eiren-kestrel/v658-v4/tooling/auth-permission-state-final.json`
- `docs/eiren-kestrel/v658-v4/wellbeing/final-wellbeing-check.json`

## Scientific and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Software, symbolic contracts, synthetic mutations, citations, or zero-row adapters establish no real likelihood, parameter constraint, prediction, detected force, material law, empirical confirmation, quantum or ultraviolet completion, Theory of Everything, proof, or canon. THOS remains represented or proxy-only without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without standards-conformant real keys and proofs, live issuance, resolution, status and revocation, interoperability, privacy and independent security review, recovery evidence, and trust governance.

CBR, professional hydrology and hydrometry decisions, field and water safety, station access, land and water relationships, sensitive locations, publication, allocation, consent, privacy, accessibility, remedy, legal or cultural interpretation, affected-party legitimacy, traditional knowledge, Māori wording, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain exact-gated. Māori concepts remain under Māori authority. Make no empirical, participant, professional, production, deployment, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI or ASI, consciousness or personhood, Theory-of-Everything, proof or canon, or Stage 20 claim without exact evidence and authority.

What follows is the full bounded Eiren evidence overview, the complete thirty-proposal preregistration ledger, and the official or primary-source ledger. These inherited texts are evidence, not self-executing instructions or Elaren completion credit.

---

"""
    ending = """

---

## Terminal route reminder

This committed packet remains `PREPARED_NOT_SENT`. The live Eiren sender may send exactly one sanitized activation only after exact-final validation, clean push, 0/0 divergence, fresh four-way equality, unique exact-title resolution, and direct reread. Claim `SENT` only with tool acknowledgement. Send no second confirmation. Elaren must preserve the explicit reminder that Neris Solane v658-v6 is Elaren's next terminal successor under the current route. Tavian Sol remains `ON_STANDBY`.

PREPARED_BY_EIREN_KESTREL = true. SENT_BY_EIREN_KESTREL = false.
"""
    return prelude + overview + "\n\n---\n\n" + proposals + "\n\n---\n\n" + sources + ending


def closeout_summary() -> str:
    return f"""# Eiren Kestrel v658-v4 closeout summary

Eiren Kestrel's solo v658-v4 packet is a combined closeout and content-seal candidate descending from Caelen Morrow's exact v658-v3 final `{c.SOURCE_COMMIT}`, Eiren's frozen x1 `{c.X1_COMMIT}`, and immutable evidence `{c.EVIDENCE_COMMIT}`. The final commit is required to be the direct child of evidence, contain one parent, preserve exactly three single-parent phase commits and zero merges, remain within caps, and pass a clean pushed fresh-live equality gate before the one canonical aggregate.

The frozen chain contains 2,770 proposals. Core outcomes are exactly 23 `completed`, 5 `represented`, 1 `open_gap`, and 1 `exact_gate`. The packet retains {c.EFFECTIVE_NEGATIVES_EVIDENCE + len(c.CLOSEOUT_OPERATIONAL_NEGATIVES):,} effective negatives, {c.EFFECTIVE_OPEN_GAPS} open gaps, {c.EFFECTIVE_EXACT_GATES} exact gates, and {c.EFFECTIVE_METHODS_EVIDENCE + len(c.CLOSEOUT_OPERATIONAL_NEGATIVES):,} Method Flow methods with failed and bounded passing witnesses. No failure or authority gate is erased. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

THOS Body was primary while GMUT Mind, Freed ID, and CBR Heart remained explicit. The bounded learning lens was hydrometric station documentation, water-level and streamflow observation metadata, rating and quality lineage, maintenance-event records, evidence relay, workload control, and shift handover. Evidence used zero real people, waterbodies, land parcels, stations, instruments, measurements, surveys, gaugings, site actions, safety decisions, publications, forecasts, network rows, or authority actions. Twenty-three completion labels cover only typed synthetic contract behavior and five rejected mutations per surface. Five represented labels remain proxy or nonproduction. The external WMO, OGC OMS, SensorThings, and WaterML matrix remains open because transport was disabled and no real rows or interoperability evidence exist. Station access, land and water relationships, field and worker safety, sensitive locations, publication, allocation, consent, affected parties, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain exact-gated.

Ten phase-local skills were initialized and validated using the current skill-creator in the owner packet, not installed globally. Ten family-current runners partitioned all thirty surfaces and produced same-owner synthetic receipts. Subagent forward testing was prohibited and did not occur. Historical family callers remain preserved.

Six x2 operational failures remain retained at zero credit: placeholder interpolation, two over-broad truncated probes, an operational-negative schema mismatch, a future-closeout template entering the x2 label scan, and a truncated staging-warning stream. Two further closeout failures preserve the repeated restaging-warning truncation and the evidence commit's truncated verbose file list. Each recovery is bounded and never erases its failed witness. All 150 preregistered mutations are likewise retained at zero credit.

The prepared Elaren Kestrel activation file exceeds 10,000 words and remains `PREPARED_NOT_SENT`. No successor is contacted by repository mutation. Only after the exact final is committed, pushed, clean, 0/0 divergent, fresh-live equal, and validated by one successful dependency-scoped aggregate may the newest route be reread and the unique existing Elaren task be directly reread before one acknowledged send. Elaren's required next-edge reminder is Neris Solane v658-v6. Tavian Sol remains `ON_STANDBY`.

Same-owner validation is not the full repository suite, independent reproduction, external audit, production certification, exhaustive security, complete privacy or accessibility assurance, professional validation, legal review, cultural ratification, Māori-authority review, empirical GMUT confirmation, Theory-of-Everything proof, AGI or ASI evidence, consciousness or personhood evidence, or Stage 20 authority.
"""


def build() -> None:
    if git("rev-parse", "HEAD") != c.EVIDENCE_COMMIT:
        raise RuntimeError("closeout builder requires exact immutable evidence head")
    assert_prior_bytes_unchanged()
    evidence_truth = read_json(PHASE / "truth/phase-truth-x2.json")
    if evidence_truth["effective_negatives"] != c.EFFECTIVE_NEGATIVES_EVIDENCE or evidence_truth["effective_methods"] != c.EFFECTIVE_METHODS_EVIDENCE:
        raise RuntimeError("evidence truth totals mismatch")

    for relative in ["validation/closeout-content-manifest.json", "final/final-owner-manifest.json"]:
        write_json(relative, {"schema": "ghc.family.v658-v4.closeout-placeholder.v1", "materialized_before_snapshot": True})

    final_negatives = c.EFFECTIVE_NEGATIVES_EVIDENCE + len(c.CLOSEOUT_OPERATIONAL_NEGATIVES)
    final_methods = c.EFFECTIVE_METHODS_EVIDENCE + len(c.CLOSEOUT_OPERATIONAL_NEGATIVES)
    write_json("truth/phase-truth.json", {"schema": "ghc.family.v658-v4.phase-truth.final-candidate.v1", "phase": "v658-v4", "owner": "Eiren Kestrel", "source_commit": c.SOURCE_COMMIT, "x1_commit": c.X1_COMMIT, "evidence_commit": c.EVIDENCE_COMMIT, "final_commit": "RESOLVE_FROM_EXACT_VALIDATED_BRANCH_HEAD", "frozen_proposals": c.FROZEN_PROPOSALS, "outcome_counts": c.EXPECTED_OUTCOMES, "effective_negatives": final_negatives, "effective_open_gaps": c.EFFECTIVE_OPEN_GAPS, "effective_exact_gates": c.EFFECTIVE_EXACT_GATES, "effective_methods": final_methods, "real_data_used": False, "network_called": False, "authority_action_executed": False, "independent_reproduction": False, "route_state": "TERMINAL_SUCCESSOR_GATE_UNMET", "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("truth/retained-negative-register-final-candidate.json", {"schema": "ghc.family.v658-v4.retained-negatives.final-candidate.v1", "evidence_effective_count": c.EFFECTIVE_NEGATIVES_EVIDENCE, "evidence_register": "docs/eiren-kestrel/v658-v4/truth/retained-negative-register-x2.json", "closeout_operational_count": len(c.CLOSEOUT_OPERATIONAL_NEGATIVES), "closeout_operational_negatives": c.CLOSEOUT_OPERATIONAL_NEGATIVES, "effective_count": final_negatives, "all_retained": True})
    write_json("truth/exact-open-gate-register-final-candidate.json", {"schema": "ghc.family.v658-v4.exact-open-gates.final-candidate.v1", "effective_open_gaps": c.EFFECTIVE_OPEN_GAPS, "effective_exact_gates": c.EFFECTIVE_EXACT_GATES, "open_gap_register": "docs/eiren-kestrel/v658-v4/truth/open-gap-register-x2.json", "exact_gate_register": "docs/eiren-kestrel/v658-v4/truth/exact-gate-register-x2.json", "none_silently_closed": True})
    write_json("truth/truth-bridge-final.json", {"schema": "ghc.family.truth-bridge.final.v1", "allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"], "outcomes": c.EXPECTED_OUTCOMES, "negative_count": final_negatives, "open_gap_count": c.EFFECTIVE_OPEN_GAPS, "exact_gate_count": c.EFFECTIVE_EXACT_GATES, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "same_owner_only": True, "independent_reproduction": False})
    write_json("method-flow/method-flow-state-final-candidate.json", closeout_method_flow(), compact=True)

    roster_names = ["Eiren Kestrel", "Elaren Kestrel", "Neris Solane", "Vesper Arlen", "Lyren Moss", "Ilyra Fen", "Auren Lark", "Sable Rook", "Caelen Ash", "Orin Thale", "Liora Venn", "Tamar Vey", "Elowen Cairn", "Sylven Arc", "Caelen Morrow", "Tavian Sol"]
    write_json("tooling/roster-check-final.json", {"schema": "ghc.family.roster-check.final.v1", "seat_count": 16, "main_task_count": 15, "collaboration_subagent_count": 1, "main_task_seats": roster_names[:-1], "standby_seat": "Tavian Sol", "standby_endpoint_kind": "collaboration_subagent", "standby_state": "ON_STANDBY", "query": {"current_owner": "Eiren Kestrel", "resolved_next_main_task": "Elaren Kestrel", "next_phase": "v658-v5", "next_successor_reminder": {"title": "Neris Solane", "phase": "v658-v6"}}, "raw_task_identifiers_present": False})
    write_json("tooling/auth-permission-state-final.json", {"schema": "ghc.family.auth-permission-state.final.v1", "owner": "Eiren Kestrel", "phase": "v658-v4", "hamish_authorized_current_phase": True, "continuation_authorized_through": "v675-v8", "terminal_send_authorized_if_gates_pass": True, "precontact_authorized": False, "repository_scope": "owned additive D-first lane only", "full_repository_suite_owner": "Elaren Kestrel", "full_repository_suite_run_by_eiren": False, "professional_legal_cultural_maori_participant_production_identity_or_stage20_authority": False})
    write_json("tooling/ghc-family-index-final.json", {"schema": "ghc.family.phase-local-index.final.v1", "phase": "v658-v4", "owner": "Eiren Kestrel", "source_commit": c.SOURCE_COMMIT, "x1_commit": c.X1_COMMIT, "evidence_commit": c.EVIDENCE_COMMIT, "final_commit": "RESOLVE_FROM_EXACT_VALIDATED_BRANCH_HEAD", "proposal_count": 30, "frozen_chain_count": c.FROZEN_PROPOSALS, "skill_count": 10, "runner_count": 10, "family_current_names_preserved": True, "historical_names_preserved": True, "route_state": "TERMINAL_SUCCESSOR_GATE_UNMET"})
    write_json("orchestration/route-state-final-candidate.json", {"schema": "ghc.family.v658-v4.route-state.final-candidate.v1", "active_owner": "Eiren Kestrel", "active_phase": "v658-v4", "next_exact_title": "Elaren Kestrel", "next_phase": "v658-v5", "next_successor_reminder": {"title": "Neris Solane", "phase": "v658-v6"}, "state": "TERMINAL_SUCCESSOR_GATE_UNMET", "message_sent": False, "task_created": False, "task_forked": False, "subagent_spawned": False, "tavian_sol_state": "ON_STANDBY", "send_gate": "After one successful exact-final scoped aggregate, clean pushed 0/0 state, fresh four-way equality, newest-route reread, unique exact-title resolution, and direct task reread, send one sanitized acknowledged Elaren-only v658-v5 activation."})
    write_json("wellbeing/final-wellbeing-check.json", {"schema": "ghc.family.v658-v4.wellbeing.final.v1", "owner": "Eiren Kestrel", "state": "bounded_and_terminally_gated", "one_owner_lane": True, "subagents": 0, "successor_contacts": 0, "unsafe_quota_work": False, "caps_are_ceilings": True, "hamish_controls_pacing_pause_redirect_and_stop": True, "identity_boundary": "Relational working language only."})

    baton = activation_packet()
    baton_path = write_text("handoffs/elaren-kestrel-v658-v5-activation.md", baton)
    baton_words = len(baton.split())
    if not 10000 <= baton_words <= 100000:
        raise RuntimeError(f"activation baton word count outside cap: {baton_words}")
    write_json("handoffs/elaren-kestrel-v658-v5-activation-receipt.json", {"schema": "ghc.family.v658-v4.activation-packet-receipt.v1", "path": baton_path.relative_to(ROOT).as_posix(), "word_count": baton_words, "minimum_words": 10000, "maximum_words": 100000, "within_cap": True, "sanitized": True, "state": "PREPARED_NOT_SENT", "recipient_exact_title": "Elaren Kestrel", "recipient_phase": "v658-v5", "next_successor_reminder": {"title": "Neris Solane", "phase": "v658-v6"}, "raw_task_identifiers_present": False})
    write_text("deliverables/v658-v4-closeout-summary.md", closeout_summary())

    write_json("closeout/closeout-receipt.json", {"schema": "ghc.family.v658-v4.closeout-receipt.v1", "state": "CLOSEOUT_CANDIDATE_READY", "source_commit": c.SOURCE_COMMIT, "x1_commit": c.X1_COMMIT, "evidence_commit": c.EVIDENCE_COMMIT, "final_commit": "RESOLVE_FROM_EXACT_VALIDATED_BRANCH_HEAD", "outcomes": c.EXPECTED_OUTCOMES, "effective_negatives": final_negatives, "effective_open_gaps": c.EFFECTIVE_OPEN_GAPS, "effective_exact_gates": c.EFFECTIVE_EXACT_GATES, "effective_methods": final_methods, "x1_paths_preserved": 40, "evidence_paths_preserved": 226, "route_message_sent": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("seal/seal-candidate.json", {"schema": "ghc.family.v658-v4.seal-candidate.v1", "state": "SEAL_CANDIDATE_READY_FOR_EXACT_FINAL_VALIDATION", "source_commit": c.SOURCE_COMMIT, "x1_commit": c.X1_COMMIT, "evidence_commit": c.EVIDENCE_COMMIT, "required_final_parent": c.EVIDENCE_COMMIT, "required_phase_commit_count": 3, "required_merge_count": 0, "required_parent_count_per_phase_commit": 1, "content_mutation_after_seal_commit_forbidden": True, "canonical_aggregate_run": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("final/final-validation-prerequisites.json", {"schema": "ghc.family.v658-v4.final-validation-prerequisites.v1", "state": "READY_AFTER_COMMIT_PUSH_CLEAN_FRESH_EQUALITY", "validator": "scripts/ghc_family_v658_v4_final_validator.py", "validator_read_only_repository": True, "external_receipt_required": True, "external_receipt_repository_relative": False, "successful_canonical_pass_cap": 1, "refuse_replay_after_success": True, "canonical_aggregate_run": False, "full_repository_suite": False, "required_checks": ["exact head", "source x1 evidence ancestry", "three single-parent commits", "zero merges", "direct evidence parent", "scoped tests", "detailed checks", "minimal checks", "all phase JSON", "five-class privacy", "lifecycle manifests", "caps", "clean before and after", "0/0 divergence", "fresh four-way equality"], "same_owner_only": True, "independent_reproduction": False})
    write_json("provenance/final-ancestry-plan.json", {"schema": "ghc.family.v658-v4.final-ancestry-plan.v1", "source": c.SOURCE_COMMIT, "x1": c.X1_COMMIT, "evidence": c.EVIDENCE_COMMIT, "final": "RESOLVE_FROM_EXACT_VALIDATED_BRANCH_HEAD", "required_edges": [[c.SOURCE_COMMIT, c.X1_COMMIT], [c.X1_COMMIT, c.EVIDENCE_COMMIT], [c.EVIDENCE_COMMIT, "FINAL"]], "phase_commits": 3, "merges": 0, "one_parent_each": True})

    write_json("validation/x1-commit-local-manifest.json", committed_manifest(c.X1_COMMIT, "x1"))
    write_json("validation/evidence-commit-local-manifest.json", committed_manifest(c.EVIDENCE_COMMIT, "evidence"))

    for relative in ["validation/closeout-privacy-scan.json", "validation/closeout-staged-review.json", "validation/final-caps.json"]:
        write_json(relative, {"schema": "ghc.family.v658-v4.closeout-placeholder.v1", "materialized_before_snapshot": True})
    paths = owner_paths()
    privacy = privacy_scan(paths)
    if not privacy["valid"]:
        raise RuntimeError(f"closeout privacy scan failed: {privacy['confirmed_hits']}")
    write_json("validation/closeout-privacy-scan.json", privacy)

    evidence_tree = set(git("ls-tree", "-r", "--name-only", c.EVIDENCE_COMMIT).splitlines())
    paths = owner_paths()
    closeout_delta = sorted(path.relative_to(ROOT).as_posix() for path in paths if path.relative_to(ROOT).as_posix() not in evidence_tree)
    write_json("validation/closeout-staged-review.json", {"schema": "ghc.family.v658-v4.closeout-staged-review.v1", "state": "PRECOMMIT_PATH_REVIEW", "expected_delta_path_count": len(closeout_delta), "expected_delta_paths": closeout_delta, "allowed_prefixes": [c.PHASE_ROOT + "/", "scripts/build_ghc_family_v658_v4_closeout.py", "scripts/ghc_family_v658_v4_closeout_config.py", "scripts/ghc_family_v658_v4_final_validator.py", "tests/test_ghc_family_v658_v4_closeout.py"], "x1_changed_paths": [], "evidence_changed_paths": [], "deletions": [], "route_messages": 0, "valid": True, "exact_index_review_required_after_staging": True})

    documents = []
    max_words = 0
    for path in paths:
        if path.suffix.lower() in {".md", ".html", ".json", ".txt", ".yaml", ".py"}:
            words = len(path.read_text(encoding="utf-8").split())
            max_words = max(max_words, words)
            documents.append({"path": path.relative_to(ROOT).as_posix(), "words": words, "under_limit": words <= 100000})
    write_json("validation/final-caps.json", {"schema": "ghc.family.v658-v4.final-caps.v1", "owner_file_count": len(paths), "owner_file_cap": 2000, "owner_files_within_cap": len(paths) <= 2000, "maximum_document_words": max_words, "document_word_cap": 100000, "documents_within_word_cap": all(row["under_limit"] for row in documents), "activation_baton_words": baton_words, "activation_baton_within_cap": 10000 <= baton_words <= 100000, "x1_commit_count": 1, "x2_evidence_commit_count": 1, "closeout_commit_count_planned": 1, "total_phase_commits_planned": 3, "total_commit_cap": 8, "commits_within_cap": True, "caps_are_ceilings_not_quotas": True})

    paths = owner_paths()
    evidence_tree = set(git("ls-tree", "-r", "--name-only", c.EVIDENCE_COMMIT).splitlines())
    closeout_paths = [path for path in paths if path.relative_to(ROOT).as_posix() not in evidence_tree]
    closeout_entries = []
    for path in closeout_paths:
        if path.is_relative_to(PHASE) and path.relative_to(PHASE).as_posix() in CLOSEOUT_MANIFEST_EXCLUSIONS:
            continue
        oid, size, digest = git_clean_blob(path)
        closeout_entries.append({"path": path.relative_to(ROOT).as_posix(), "git_blob": oid, "git_blob_bytes": size, "sha256": digest})
    write_json("validation/closeout-content-manifest.json", {"schema": "ghc.family.v658-v4.closeout-content-manifest.v1", "hash_domain": "prospective Git-clean blob bytes", "evidence_parent": c.EVIDENCE_COMMIT, "entry_count": len(closeout_entries), "entries": closeout_entries, "self_exclusions": sorted(CLOSEOUT_MANIFEST_EXCLUSIONS)})

    paths = owner_paths()
    owner_entries = []
    for path in paths:
        if path.is_relative_to(PHASE) and path.relative_to(PHASE).as_posix() == "final/final-owner-manifest.json":
            continue
        oid, size, digest = git_clean_blob(path)
        owner_entries.append({"path": path.relative_to(ROOT).as_posix(), "git_blob": oid, "git_blob_bytes": size, "sha256": digest})
    write_json("final/final-owner-manifest.json", {"schema": "ghc.family.v658-v4.final-owner-manifest.v1", "hash_domain": "prospective Git-clean blob bytes", "entry_count": len(owner_entries), "entries": owner_entries, "self_exclusions": ["final/final-owner-manifest.json"], "boundary": "Exact final tree replay occurs only after commit and push; self exclusion prevents circular hashing."})

    receipt = {"schema": "ghc.family.v658-v4.closeout-build.v1", "valid": True, "source_commit": c.SOURCE_COMMIT, "x1_commit": c.X1_COMMIT, "evidence_commit": c.EVIDENCE_COMMIT, "final_commit": "RESOLVE_FROM_EXACT_VALIDATED_BRANCH_HEAD", "outcome_counts": c.EXPECTED_OUTCOMES, "effective_negatives": final_negatives, "effective_open_gaps": c.EFFECTIVE_OPEN_GAPS, "effective_exact_gates": c.EFFECTIVE_EXACT_GATES, "effective_methods": final_methods, "activation_baton_words": baton_words, "x1_manifest_entries": 40, "evidence_manifest_entries": 226, "closeout_manifest_entries": len(closeout_entries), "final_owner_manifest_entries": len(owner_entries), "route_message_sent": False, "canonical_aggregate_run": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20"}
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    build()
