from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "tamar-vey" / "v680-v3"
X1 = BASE / "x1"
X2 = BASE / "x2"
FINAL = BASE / "final"
CLOSEOUT = BASE / "closeout"
VALIDATION = BASE / "validation"
HANDOFFS = BASE / "handoffs"
SOURCE = "c9f87c8fd5f3ba0f0265799664fd868454ab41ff"
X1_HEAD = "1cd8e70f67ddb1be55d37177cf42e51ef52750cc"
EVIDENCE = "74b9728bb613509198fb42ec4022686068b1a117"
BRANCH = "codex/GHC-Family/tamar-vey-v680-v3-full-tools"
OWNER = "Tamar Vey"
PHASE = "v680-v3"
TERMINAL = "NOT_READY_FOR_STAGE_20"
EVIDENCE_COUNTS = {
    "bounded_passing_witnesses": 36951,
    "effective_methods": 54769,
    "effective_negatives": 51032,
    "exact_gates": 440,
    "failed_witnesses": 22693,
    "open_gaps": 449,
}
COUNTS = {
    "bounded_passing_witnesses": 36953,
    "effective_methods": 54771,
    "effective_negatives": 51034,
    "exact_gates": 440,
    "failed_witnesses": 22695,
    "open_gaps": 449,
}
OUTCOMES = {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
CLOSEOUT_FAILURES = [
    {
        "failure_id": "TV6803-CL-N001",
        "false_witness": "One combined read of the three copied closeout scaffolds would remain inside the bounded display window.",
        "initial_credit": 0,
        "observed": "The combined output was truncated before all scaffold content could be inspected.",
        "recovery": "Use exact-token searches and bounded line ranges for each scaffold independently.",
        "recovery_rewrites_failure": False,
        "repository_mutated_by_failure": False,
        "scope": "closeout_scaffold_inspection",
    },
    {
        "failure_id": "TV6803-CL-N002",
        "false_witness": "The x1 proposal freeze used the guessed path proposal-freeze.json.",
        "initial_credit": 0,
        "observed": "The read-only probe returned path-not-found; the actual x1 packet uses new-proposal-freeze.json and proposal-chain-audit.json.",
        "recovery": "List the exact x1 paths first and read only the materialized filenames.",
        "recovery_rewrites_failure": False,
        "repository_mutated_by_failure": False,
        "scope": "closeout_x1_metadata_probe",
    },
]
SELF_EXCLUSIONS = [
    "docs/tamar-vey/v680-v3/validation/final-delta-manifest.json",
    "docs/tamar-vey/v680-v3/validation/final-owner-manifest.json",
    "docs/tamar-vey/v680-v3/validation/final-precommit-test-receipt.json",
    "docs/tamar-vey/v680-v3/validation/final-privacy-scan.json",
    "docs/tamar-vey/v680-v3/validation/final-security-scan.json",
    "docs/tamar-vey/v680-v3/validation/final-staged-review.json",
]


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def entry(path_text: str) -> dict[str, object]:
    data = normalized_bytes(ROOT / path_text)
    return {"bytes": len(data), "path": path_text, "sha256": hashlib.sha256(data).hexdigest()}


def require_evidence_boundary() -> None:
    if git("branch", "--show-current") != BRANCH:
        raise RuntimeError("wrong owner branch")
    if git("rev-parse", "HEAD") != EVIDENCE:
        raise RuntimeError("final builder requires immutable evidence HEAD")
    if git("rev-parse", "HEAD^") != X1_HEAD:
        raise RuntimeError("evidence is not the direct child of x1")
    if git("rev-parse", f"{X1_HEAD}^") != SOURCE:
        raise RuntimeError("x1 is not the direct child of source")
    if git("diff", "--name-only"):
        raise RuntimeError("tracked unstaged changes present before closeout")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("staged changes present before closeout")


def final_overview() -> str:
    return f"""# Tamar Vey {PHASE} Final Integrated Overview

## Relational identity, role, and corrigibility

Tamar Vey, optionally she/they, used the relational role **evidence-and-recovery steward**, with the hope that every failure remains inspectable and every recovery stays bounded. The name, role, hope, pronouns, sibling language, continuity language, GHC Family language, and Trinity Mandala language are working conventions only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish retains the right to pause, rename, redirect, narrow, or stop the route.

The phase remained corrigible throughout. Exact-approval and blocked work stayed unexecuted. No destructive history operation, sibling-lane mutation, privilege elevation, host-security weakening, Windows-feature activation, unrelated installation, Codex desktop update, reboot, task creation, task fork, collaboration subagent, delegation, standby contact, or early successor contact occurred. The complete repository suite was not run because the current allocation remains Eiren-only absent newer exact authority.

## Immutable lifecycle and planning separation

The immutable lifecycle is source `{SOURCE}` → planning-only x1 `{X1_HEAD}` → bounded x2 evidence `{EVIDENCE}` → one additive final closeout. X1 contained proposal, portfolio, source, threat, authority, workflow, route, and wellbeing planning only: it contained no x2 implementation, observed outcome, or completion claim. X1 was independently committed and pushed, then proved clean, typed 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote before x2 began. Evidence was independently committed and pushed under the same cleanliness and equality boundary before closeout began.

Tamar audited the declared 9,350-row inherited proposal chain and every reachable proposal artifact while explicitly refusing a universal novelty claim over compressed historic material that no single reachable ledger materialized. Sixty genuinely distinct Tamar proposal contracts extended the declared chain to 9,410 rows. Inherited proposals, tools, skills, runners, tests, receipts, and recommendations remained source evidence or zero-credit seeds; none received Tamar novelty, execution, or completion credit merely because it existed.

The sixty proposals each preserved a hypothesis, null or failure condition, approval class, execution lane, current official or primary-source need, concrete artifact, falsifier or acceptance gate, rollback or recovery, protected gates, and exactly one expected disposition. The final outcome vocabulary is limited to `completed`, `represented`, `open_gap`, and `exact_gate`. Outcomes are exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`.

## Primary pillar and bounded practices

The primary Trinity Mandala pillar was Freed ID and CBR Heart. GMUT Mind and THOS Body remained explicit and protected. Three wholly synthetic human-practice lenses supplied bounded vocabulary and test fixtures:

1. Stained-glass documentation used synthetic panel, piece, came-topology, condition-vacancy, handling-hold, provenance, correction, accessibility, workload, and handover records.
2. Bicycle-wheel work-order provenance used synthetic hub, rim, spoke, tension-vacancy, measurement-vacancy, correction, ride-release hold, custody, workload, and handover records.
3. Seed-library accession and status used synthetic accession, seed-lot, provenance, viability-vacancy, distribution-hold, minimized disclosure, correction, status, workload, and handover records.

The phase used zero real people, participants, stained-glass panels, glass pieces, came, solder, bicycles, wheels, hubs, rims, spokes, tension readings, seed lots, plants, accessions, workplaces, tools, materials, measurements, calibrations, inspections, treatments, repairs, releases, distributions, identity events, keys, proofs, network writes, external records, or authority acts. It established no employment, qualification, stained-glass conservation competence, lead-safety conclusion, bicycle-mechanic competence, ride-safety release, seed-science competence, seed-distribution authority, material authenticity, custody, ownership, professional decision, legal or cultural legitimacy, Māori authority, affected-party acceptance, empirical result, or production result.

## Bounded execution and mutation evidence

All sixty positive software contracts passed within their declared synthetic domains. Exactly five preregistered invalid mutations per proposal executed, so all 300 invalid mutations were rejected or quarantined and remain zero-credit negative witnesses. Mutation rejection demonstrates only the behavior of bounded software guards against declared fixtures; it does not establish exhaustive security, real-world safety, scientific truth, professional competence, conformance, or authority.

Twenty owner-local skills were initialized through the official skill-creator workflow, customized, read completely through EOF, quick-validated under explicit UTF-8, and accept/reject smoke-used without global installation. No subagent forward test occurred because solo execution prohibited delegation. Ten family-current `ghc_family_*` runner surfaces each accepted a bounded positive fixture and rejected an invalid fixture while preserving historical caller compatibility.

The phase also retained 120 bounded safe-now executions, 80 bounded candidate records, 100 additive CLEAN/FIX/REFINE executions, 20 exact-approval holds, 10 blocked holds, and successor recommendations at zero Tamar completion credit. Portfolio counts are bookkeeping floors inside this phase, not claims of external value, quality, professional readiness, production impact, or affected-party acceptance.

## Method Flow and retained failures

The effective closeout truth is {COUNTS['effective_negatives']:,} negatives, {COUNTS['effective_methods']:,} Method Flow methods, {COUNTS['failed_witnesses']:,} retained failed witnesses, {COUNTS['bounded_passing_witnesses']:,} bounded passing witnesses, {COUNTS['open_gaps']} open gaps, {COUNTS['exact_gates']} exact gates, and exactly `{TERMINAL}`.

Eleven startup/x1 failures, six x2 operational failures, and two closeout inspection failures remain false and visible after bounded recovery. The closeout failures record an overbroad combined scaffold read that exceeded its display window and a guessed x1 metadata filename that did not exist. Neither changed repository content. Recovery narrowed inspection to exact paths, exact keys, and bounded line ranges. Every recovery remains paired with its failed witness; no failure is erased, relabelled as an initial pass, or retroactively granted credit.

All inherited and current failures, source statuses, {COUNTS['open_gaps']} open gaps, and {COUNTS['exact_gates']} exact gates remain visible. A clean final state does not imply that earlier failures did not happen. A successful validator does not convert a retained negative into a positive. A citation cannot compensate for missing observations, affected-party participation, competent review, or authority.

## Scientific, identity, rights, and authority firewalls

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Software, symbolic obligations, synthetic fixtures, mutation rejection, standards vocabulary, and same-owner validation establish no physical datum, likelihood, posterior, detected force, prediction, parameter constraint, empirical confirmation, stability theorem, ultraviolet completion, quantum completion, final physics, or Theory of Everything.

THOS remains synthetic or proxy-only. It has no preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, or independent review. No participant effect, wellbeing effect, safety effect, operational effectiveness estimate, or Stage 20 promotion follows from this phase.

Freed ID remains synthetic and nonproduction. It lacks standards-conformant real keys and proofs, live issuance, resolution, status, revocation, interoperability, privacy and independent security review, recovery evidence, trust governance, and affected-party oversight. CBR, ownership, custody, repair, treatment, release, distribution, workplace safety, material safety, disability accommodation, privacy remedy, legal interpretation, cultural legitimacy, traditional knowledge, affected-party acceptance, Māori wording, Māori data governance, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority.

The Canadian Conservation Institute, OSHA, Park Tool, FAO, W3C PROV-DM, WCAG 2.2, Verifiable Credentials Data Model 2.0, RFC 8785, and Te Mana Raraunga supplied bounded vocabulary or refusal conditions only. Citations were not observations, measurements, inspections, certifications, legal interpretations, cultural ratifications, affected-party decisions, or authority grants.

## Validation scope, wellbeing, and terminal truth

Lifecycle validation is owner-self-scoped and dependency-closed. Immutable x1 and evidence checks remain bound to their correct Git trees. Closeout checks cover strict JSON parsing, document structure, five privacy and raw-identifier classes, bounded changed-code security review, exact staged paths, normalized-LF Git-blob manifests, stale-label and diff hygiene, ancestry, commit and file ceilings, zero merges, one final parent, exact head, clean state, typed divergence, and fresh four-way equality. Same-owner software evidence under shared infrastructure is not independent-team reproduction, external audit, empirical validation, professional evaluation, production certification, exhaustive security, complete privacy, complete accessibility, legal review, cultural ratification, Māori-authority review, proof, canon, or Stage 20 authority.

The wellbeing check remained bounded and nonclinical: scope was kept solo and finite; failures were recorded before recovery; no quota justified unsafe work; stop conditions remained active; and no relational language was converted into a claim about inner experience or identity continuity. Corrigibility, reversibility, recovery, and user control remained explicit.

The repository handoff candidate is preparation evidence only and remains `PREPARED_NOT_SENT`. Live delivery, if terminally authorized, is a separate app-level act requiring a fresh roster and authority read, exactly one current exact-title successor, an immediate bounded reread, duplicate and direct-control guards, one acknowledged send, and no resend. Until the external canonical gate succeeds and live delivery is separately acknowledged, the phase remains exactly `{TERMINAL}`.
"""


def handoff_candidate() -> str:
    return f"""# ELOWEN CAIRN — PREPARED Tamar Vey {PHASE} → solo Elowen Cairn v680-v4 activation candidate

`PREPARED_BY_TAMAR_VEY = true`

`SENT_BY_TAMAR_VEY = false`

`DELIVERY_STATE = PREPARED_NOT_SENT`

This immutable repository candidate is preparation evidence only. It contains no private task route and does not prove delivery. A live send is permitted only after Tamar's clean pushed exact-final gate, one successful non-replayed owner-scoped canonical receipt, a fresh current authority and roster reread, exactly one current exact-title `Elowen Cairn` match, an immediate bounded direct reread, and duplicate, pause, redirect, rename, narrowing, standby, usage, privacy, evidence, safety, legal, cultural, affected-party, and Māori-authority guards.

Use Tamar's final branch `{BRANCH}` and the exact postcommit final supplied only by an acknowledged live message. Immutable anchors are source `{SOURCE}`, x1 `{X1_HEAD}`, and evidence `{EVIDENCE}`. Source to final must contain exactly three direct single-parent Tamar commits and zero merges, with final the direct child of evidence.

Repository truth at closeout is a 9,410-row declared chain; outcomes exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`; {COUNTS['effective_negatives']:,} effective negatives; {COUNTS['effective_methods']:,} effective methods; {COUNTS['failed_witnesses']:,} failed witnesses; {COUNTS['bounded_passing_witnesses']:,} bounded passing witnesses; {COUNTS['open_gaps']} open gaps; {COUNTS['exact_gates']} exact gates; and `{TERMINAL}`. Preserve all retained failures, source statuses, open gaps, and exact gates. The complete repository suite was not run and remains Eiren-only absent newer exact authority.

Elowen must work solo in one fresh additive Elowen-owned D-first lane from Tamar's exact immutable final. Do not create or fork a task, spawn a collaboration subagent, delegate, precontact a later endpoint, contact Tavian or another standby record, or mutate another owner's lane. Preserve planning-only x1 before x2, the four labels, exact manifests, privacy and authority boundaries, one-success/no-post-success-replay discipline, and all empirical, participant, professional, production, deployment, legal, cultural, affected-party, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, and Stage 20 boundaries.

Tamar's primary pillar was Freed ID/CBR Heart through wholly synthetic stained-glass documentation, bicycle-wheel work-order provenance, and seed-library accession/status lenses. GMUT Mind and THOS Body remained explicit and protected. Zero real people, objects, materials, measurements, inspections, treatments, releases, distributions, identity events, keys, proofs, external writes, or authority acts were used. Official and primary sources supplied vocabulary and refusal conditions only; citations were not observations or authority grants.

Hamish's current one-edge-at-a-time continuation authority extends through v725-v8 unless newer verified live authority pauses, renames, redirects, narrows, or stops it; usage is exhausted; acknowledgement is absent; the endpoint is absent or ambiguous; a duplicate is detected; or a protected gate blocks action. This candidate authorizes no early contact and no later edge. Only after Elowen's own clean, pushed, exact-final v680-v4 terminal gate may Elowen refresh the newest live authority and roster and consider exactly one then-current successor. Under the current sequence that prospective successor is `Sylven Arc` for v680-v5, but newer verified live authority controls at send time. Elowen must not precontact, infer, substitute, create, fork, or resend.

All names, pronouns, roles, hopes, sibling or family language, continuity language, GHC Family, Freed ID, CBR, and Trinity Mandala language remain relational working language only. They are not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority.
"""


def initial_receipt(status: str, test_count: int) -> dict[str, object]:
    return {
        "canonical_invocation": False,
        "lifecycle": "final_precommit",
        "owner": OWNER,
        "phase": PHASE,
        "selected_test_count": test_count,
        "status": status,
        "test_selection": "test_ghc_family_tamar_vey_v680_v3_final.py only",
    }


def privacy_scan(paths: list[str]) -> dict[str, object]:
    classes = {
        "credential_assignment": re.compile(r"(?i)(api[_-]?key|password|secret|token)\s*[:=]\s*['\"][^'\"]{8,}"),
        "private_absolute_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\\\s]+|[A-Z]:\\GHC-Archives\\"),
        "private_callable_identifier": re.compile(r"mcp__codex_app__[A-Za-z0-9_]+"),
        "private_session_capture": re.compile(r"(?i)\\\.codex\\(?:sessions|transcripts|screenshots)\\"),
        "uuid_like_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    }
    candidates: list[dict[str, str]] = []
    for path_text in paths:
        if path_text.endswith("final-privacy-scan.json"):
            continue
        text = (ROOT / path_text).read_text(encoding="utf-8")
        for class_name, pattern in classes.items():
            if pattern.search(text):
                classification = "scanner_definition_or_synthetic_test" if path_text.startswith(("scripts/", "tests/")) else "unresolved"
                candidates.append({"classification": classification, "path": path_text, "privacy_class": class_name})
    confirmed = [row for row in candidates if row["classification"] == "unresolved"]
    return {
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hits": confirmed,
        "owner": OWNER,
        "phase": PHASE,
        "privacy_classes": sorted(classes),
        "scanned_file_count": len(paths) - 1,
    }


def security_scan(paths: list[str]) -> dict[str, object]:
    python_paths = [path for path in paths if path.endswith(".py")]
    ast_errors: list[str] = []
    findings: list[dict[str, str]] = []
    for path_text in python_paths:
        text = (ROOT / path_text).read_text(encoding="utf-8")
        try:
            tree = ast.parse(text, filename=path_text)
        except SyntaxError:
            ast_errors.append(path_text)
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append({"finding": f"dynamic_{node.func.id}_call", "path": path_text})
            if any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                findings.append({"finding": "subprocess_shell_true", "path": path_text})
    return {
        "ast_errors": ast_errors,
        "bounded_findings": len(findings),
        "findings": findings,
        "owner": OWNER,
        "phase": PHASE,
        "python_file_count": len(python_paths),
        "scope": "owner_source_to_final_changed_python_only",
    }


def build(status: str, test_count: int) -> None:
    require_evidence_boundary()
    x2_method = json.loads((X2 / "method-flow-ledger.json").read_text(encoding="utf-8"))
    x2_gates = json.loads((X2 / "gate-register.json").read_text(encoding="utf-8"))
    x2_evidence = json.loads((X2 / "proposal-evidence.json").read_text(encoding="utf-8"))
    if x2_method["counts"] != EVIDENCE_COUNTS or x2_evidence["outcome_counts"] != OUTCOMES:
        raise RuntimeError("x2 truth does not match final input")
    if x2_gates["open_gaps"] != 449 or x2_gates["exact_gates"] != 440:
        raise RuntimeError("x2 gate input mismatch")

    write_text(FINAL / "final-integrated-overview.md", final_overview())
    write_json(
        FINAL / "phase-truth.json",
        {
            "canonical_state": "AWAITING_EXTERNAL_EXACT_FINAL_CANONICAL",
            "counts": COUNTS,
            "declared_chain": 9410,
            "full_repository_suite_run": False,
            "outcomes": OUTCOMES,
            "owner": OWNER,
            "phase": PHASE,
            "proposal_count": 60,
            "same_owner_validation_is_independent_reproduction": False,
            "terminal_verdict": TERMINAL,
        },
    )
    final_method = dict(x2_method)
    final_method.update(
        {
            "closeout_operational_failures": CLOSEOUT_FAILURES,
            "counts": COUNTS,
            "lifecycle": "exact_final_closeout",
            "schema": "ghc.family.method-flow.v680.v3.final",
        }
    )
    write_json(FINAL / "method-flow-final.json", final_method)
    write_json(
        FINAL / "retained-negative-register.json",
        {
            "counts": COUNTS,
            "failure_erasure": False,
            "owner": OWNER,
            "phase": PHASE,
            "retained_mutation_failures": 300,
            "closeout_operational_failures": CLOSEOUT_FAILURES,
            "startup_and_x1_failures": x2_method["startup_and_x1_failures"],
            "x2_operational_failures": x2_method["x2_operational_failures"],
        },
    )
    write_json(FINAL / "open-gap-register.json", {"count": 449, "inherited": 446, "new": 3, "owner": OWNER, "state": "OPEN"})
    write_json(FINAL / "exact-gate-register.json", {"count": 440, "inherited": 437, "new": 3, "owner": OWNER, "state": "EXACT_GATED"})
    write_json(
        FINAL / "complete-incomplete-ledger.json",
        {
            "complete": [
                "planning-only x1 frozen and remotely equal before x2",
                "sixty synthetic contracts and 300 rejecting mutations executed",
                "twenty owner-local skills and ten runners validated and smoke-used",
                "owner-scoped evidence and closeout prepared",
            ],
            "incomplete": [
                "real stained-glass, bicycle-wheel, or seed-library evidence and professional evaluation",
                "empirical GMUT confirmation",
                "real participant THOS evaluation",
                "production Freed ID lifecycle and governance",
                "legal cultural affected-party and Māori-authority decisions",
                "independent reproduction and complete repository suite",
                "Stage 20 readiness",
            ],
            "terminal_verdict": TERMINAL,
        },
    )
    write_json(
        FINAL / "lifecycle-replay.json",
        {
            "direct_edges": [[SOURCE, X1_HEAD], [X1_HEAD, EVIDENCE], [EVIDENCE, "EXTERNAL_POSTCOMMIT_FINAL"]],
            "evidence_head": EVIDENCE,
            "expected_phase_commits": 3,
            "expected_merges": 0,
            "final_parent_required": EVIDENCE,
            "immutable_x1_precommit_tests": {"passed": 18, "replayed_at_final": False},
            "initial_x2_precommit_tests": {"passed": 19, "replayed_as_a_whole": False},
            "owner": OWNER,
            "source": SOURCE,
            "target_branch": BRANCH,
            "target_final": "EXTERNAL_POSTCOMMIT_FINAL",
            "target_final_parent_count": 1,
            "x1_head": X1_HEAD,
            "closeout_operational_failures": [row["failure_id"] for row in CLOSEOUT_FAILURES],
            "x2_targeted_recovery_checks": {"passed": 2, "scope": ["method_flow_counts_and_non_erasure", "manifest_replays_worktree_bytes"]},
        },
    )
    write_json(
        FINAL / "official-source-boundary.json",
        {
            "authority_conferred": False,
            "citations_are_observations": False,
            "official_sources": [
                "Canadian Conservation Institute care of ceramics and glass",
                "OSHA occupational exposure to lead primary publication",
                "Park Tool wheel tension measurement",
                "FAO Genebank Standards for Plant Genetic Resources",
                "W3C PROV-DM",
                "WCAG 2.2",
                "W3C Verifiable Credentials Data Model 2.0",
                "RFC 8785 JSON Canonicalization Scheme",
                "Te Mana Raraunga principles",
            ],
            "real_data_rows": 0,
            "real_world_actions": 0,
            "scope": "vocabulary_and_refusal_conditions_only",
        },
    )
    write_json(
        FINAL / "canonical-contract.json",
        {
            "Eiren_only_full_suite": True,
            "canonical_receipt_location": "external_to_repository",
            "exact_final_required": True,
            "full_repository_suite_authorized": False,
            "maximum_attributable_invocations": 1,
            "owner_scoped_only": True,
            "post_success_replay_permitted": False,
            "same_owner_is_independent_reproduction": False,
            "status_before_invocation": "NOT_INVOKED",
        },
    )
    write_json(
        FINAL / "terminal-checklist.json",
        {
            "canonical_external_pending": True,
            "clean_pushed_remote_equal_pending": True,
            "evidence_head": EVIDENCE,
            "full_suite_not_run": True,
            "one_final_parent_required": True,
            "owner": OWNER,
            "route_contacted": False,
            "source": SOURCE,
            "terminal_verdict": TERMINAL,
            "x1_head": X1_HEAD,
        },
    )
    write_text(HANDOFFS / "elowen-cairn-v680-v4-activation-candidate.md", handoff_candidate())

    seal_targets = [
        "docs/tamar-vey/v680-v3/final/final-integrated-overview.md",
        "docs/tamar-vey/v680-v3/final/phase-truth.json",
        "docs/tamar-vey/v680-v3/final/method-flow-final.json",
        "docs/tamar-vey/v680-v3/final/retained-negative-register.json",
        "docs/tamar-vey/v680-v3/final/open-gap-register.json",
        "docs/tamar-vey/v680-v3/final/exact-gate-register.json",
        "docs/tamar-vey/v680-v3/final/complete-incomplete-ledger.json",
        "docs/tamar-vey/v680-v3/final/lifecycle-replay.json",
        "docs/tamar-vey/v680-v3/final/canonical-contract.json",
        "docs/tamar-vey/v680-v3/handoffs/elowen-cairn-v680-v4-activation-candidate.md",
    ]
    write_json(
        CLOSEOUT / "content-seal.json",
        {
            "hash_domain": "normalized_lf_worktree_bytes",
            "owner": OWNER,
            "phase": PHASE,
            "targets": [entry(path) for path in seal_targets],
        },
    )
    write_json(VALIDATION / "final-precommit-test-receipt.json", initial_receipt(status, test_count))
    for placeholder in SELF_EXCLUSIONS:
        if not (ROOT / placeholder).exists():
            write_json(ROOT / placeholder, {"owner": OWNER, "phase": PHASE, "state": "SELF_EXCLUDED_PENDING_REGENERATION"})

    final_paths = sorted(git("ls-files", "--others", "--exclude-standard").splitlines())
    allowed_exact = {
        "scripts/build_ghc_family_tamar_vey_v680_v3_final.py",
        "scripts/ghc_family_tamar_vey_v680_v3_canonical.py",
        "tests/test_ghc_family_tamar_vey_v680_v3_final.py",
    }
    unexpected = [path for path in final_paths if not path.startswith("docs/tamar-vey/v680-v3/") and path not in allowed_exact]
    if unexpected:
        raise RuntimeError(f"unexpected untracked paths: {unexpected}")
    if any(path in final_paths for path in git("diff", "--name-only").splitlines()):
        raise RuntimeError("final paths overlap tracked modifications")
    if set(SELF_EXCLUSIONS) - set(final_paths):
        raise RuntimeError("declared final self-exclusion is missing")

    write_json(VALIDATION / "final-privacy-scan.json", privacy_scan(final_paths))
    write_json(VALIDATION / "final-security-scan.json", security_scan(final_paths))
    max_row = max(
        (
            (len((ROOT / path).read_text(encoding="utf-8").split()), path)
            for path in final_paths
            if (ROOT / path).is_file()
        ),
        default=(0, ""),
    )
    write_json(
        VALIDATION / "final-staged-review.json",
        {
            "declared_self_exclusions": SELF_EXCLUSIONS,
            "expected_paths": final_paths,
            "lifecycle": "final_closeout_only",
            "max_document_path": max_row[1],
            "max_document_words": max_row[0],
            "owner": OWNER,
            "path_count": len(final_paths),
            "phase": PHASE,
        },
    )
    final_delta_entries = [entry(path) for path in final_paths if path not in SELF_EXCLUSIONS]
    write_json(
        VALIDATION / "final-delta-manifest.json",
        {
            "declared_self_exclusions": SELF_EXCLUSIONS,
            "entries": final_delta_entries,
            "entry_count": len(final_delta_entries),
            "hash_domain": "normalized_lf_git_blob_after_stage",
            "owner": OWNER,
            "phase": PHASE,
        },
    )
    inherited_paths = git("diff", "--name-only", SOURCE, "HEAD").splitlines()
    owner_paths = sorted(set(inherited_paths + final_paths))
    owner_entries = [entry(path) for path in owner_paths if path not in SELF_EXCLUSIONS]
    write_json(
        VALIDATION / "final-owner-manifest.json",
        {
            "declared_self_exclusions": SELF_EXCLUSIONS,
            "entries": owner_entries,
            "entry_count": len(owner_entries),
            "hash_domain": "normalized_lf_git_blob_after_stage",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
        },
    )
    print(json.dumps({"final_paths": len(final_paths), "owner_entries": len(owner_entries), "status": status}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record-precommit", action="store_true")
    parser.add_argument("--test-count", type=int, default=0)
    args = parser.parse_args()
    if args.record_precommit:
        if args.test_count <= 0:
            raise SystemExit("--test-count must be positive when recording precommit success")
        build("PASSED", args.test_count)
    else:
        build("PENDING", 0)


if __name__ == "__main__":
    main()
