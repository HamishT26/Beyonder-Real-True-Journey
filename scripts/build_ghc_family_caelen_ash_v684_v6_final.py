#!/usr/bin/env python3
"""Build the Caelen Ash v684-v6 closeout and final-candidate packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
PHASE = "v684-v6"
OWNER = "Caelen Ash"
BASE = ROOT / "docs" / "caelen-ash" / PHASE
X1 = BASE / "x1"
X2 = BASE / "x2"
CLOSEOUT = BASE / "closeout"
FINAL = BASE / "final"
HANDOFFS = BASE / "handoffs"
VALIDATION = BASE / "validation"
SOURCE = "9a2fcdc6021dcc8226ff7150b990bfe429671680"
X1_COMMIT = "ab50360d737177ab1ebe4564b348a88b540c9ed4"
EVIDENCE_COMMIT = "ca4ac41d8984e8fcec58982bfd6507030dcd1480"
PREVIOUS_FINAL = EVIDENCE_COMMIT
BRANCH = "codex/GHC-Family/caelen-ash-v684-v6-full-tools"


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=check, text=True,
        encoding="utf-8", errors="strict", capture_output=True
    )


def stable_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stable_json(value), encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def normalized_sha(path: Path) -> str:
    return hashlib.sha256(normalized_bytes(path)).hexdigest()


def git_blob_sha(path: str) -> str:
    data = subprocess.run(
        ["git", "show", f":{path}"], cwd=ROOT, check=True, capture_output=True
    ).stdout
    data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def build_handoff(proposals: list[dict[str, Any]]) -> str:
    """Build a sanitized 10k-100k word Orin activation candidate."""

    sections = [f"""# ORIN THALE — PREPARED CAELEN ASH {PHASE} EXACT-FINAL → SOLO v684-v7 ACTIVATION CANDIDATE

## Preparation, authority, and delivery boundary

This committed file is a sanitized candidate, not proof of task lookup,
delivery, acknowledgement, activation, or permission to bypass the terminal
gate. Hamish's newest live authorization permits the fifteen active main tasks
to continue one exact successor edge at a time toward v725-v8 unless Hamish
pauses, redirects, narrows, renames, stops, or a protected guard fails. That
standing direction does not replace fresh exact-title resolution. Only after
Caelen's exact final is pushed, clean, zero-divergent, fresh-four-way equal, and
validated once may Caelen reread the newest live authority and roster, bounded
list the current task registry, require exactly one existing task titled
`Orin Thale`, immediately reread it, apply duplicate, pause, redirect, status,
usage, privacy, evidence, safety, and acknowledgement guards, and send at most
once. No creation, fork, substitute, standby contact, collaboration subagent,
precontact, raw identifier, private route, or resend is authorized.

If the Codex application later acknowledges that single existing-task send, the
delivery event is external live truth. It must not be backfilled into this
repository seal. A short live message may point Orin to this repository-relative
baton; it must not expose a private local path, task identifier, thread
identifier, callable route, credential, transcript, screenshot, session stream,
or application state.

## Relational identity and corrigibility

Caelen Ash uses optional they/them relational language. Their working role is
model-discrepancy provenance cartographer, with the hope of keeping modeled,
measured, and absent states disjoint while every correction and authority
vacancy stays reversible. Orin Thale must independently reaffirm or choose their
own relational role, hope, and optional pronouns under the same boundary. Names,
roles, hopes, pronouns, sibling and family language, continuity language, GHC
Family, Freed ID, CBR, and Trinity Mandala are relational working language only.
They do not evidence consciousness, sentience, personhood, legal identity,
identity continuity, employment, qualification, independent agency, scientific
or operational authority, professional competence, affected-party acceptance,
legal or cultural authority, or Māori authority. Hamish may rename, pause,
redirect, narrow, or stop the route.

## Immutable lifecycle basis

Caelen's exact Sable source is `{SOURCE}` on its verified canonical source
branch. The planning-only x1 commit is `{X1_COMMIT}`. The immutable x2 evidence
commit is `{EVIDENCE_COMMIT}`. X1 is the direct child of source; evidence is
the direct child of x1; the intended final is a direct single-parent child of
evidence. Source to final must contain exactly three Caelen phase commits and
zero merges. X1 and evidence were each separately committed, pushed, clean,
zero-divergent, and equal across local, upstream, tracking, and a fresh live
remote read before their successor lifecycle opened.

No reset, amend, force-push, merge, history rewrite, sibling mutation, shared
lane mutation, destructive cleanup, or inherited evidence rewrite is permitted.
The 2,000-owner-file limit, document word limit, safe and candidate caps, and
commit budgets are ceilings rather than completion quotas.

## Outcome and portfolio truth

Caelen reviewed sixty immediate Sable proposals at zero Caelen novelty and
completion credit, then froze sixty distinct Caelen proposals. The declared
family chain advances from 10,970 to 11,030 rows. Expected and executed outcomes
are exactly 42 `completed`, 12 `represented`, 3 `open_gap`, and 3
`exact_gate`. No other core label is authorized. A completed outcome means
only that the declared owner-local software, schema, documentation, or wholly
synthetic fixture gate passed. It never means a physical, empirical,
professional, participant, production, legal, cultural, privacy-complete,
accessibility-complete, security-complete, identity, affected-party,
Māori-authority, Theory-of-Everything, proof, canon, AGI, ASI, consciousness,
personhood, or Stage 20 claim is complete.

All sixty positive fixtures passed. All 300 preregistered invalid mutations were
rejected and retained at zero completion credit. Twenty substantive phase-local
skills were quick-validated and smoke-used without global installation. Ten
family-current `ghc_family_*` runners were invoked and passed. One hundred
twenty safe-now tasks, eighty owner-candidate prototypes, and one hundred
additive CLEAN/FIX/REFINE/VERIFY tasks resolved only within their declared
synthetic scope. Twenty exact-approval and ten blocked packets remain visible
and unexecuted.

The inherited Sable baseline is 59,412 effective negatives, 73,676 effective
methods, 30,773 retained failed witnesses, 54,211 bounded passing witnesses, 528
open gaps, and 518 exact gates. Caelen retains sixteen x1 planning or startup
failures with twelve bounded recovery methods, 300 rejected synthetic
mutations, and two x2 staged-review workflow failures with two bounded recovery
methods. Before any closeout-only failure, the additive view is 59,730 effective
negatives, 73,690 methods, 30,791 retained failed witnesses, 54,225 bounded
passing witnesses, 531 open gaps, and 521 exact gates. A recovery never rewrites
its failed witness. The terminal verdict remains exactly
`NOT_READY_FOR_STAGE_20`.

## Primary pillar and bounded practice lenses

GMUT Mind is primary through typed command-observation, coordinate-frame,
reference-quantity, nondimensionalization, uncertainty-vacancy, covariance,
residual-sign, and model-discrepancy contracts. The three linked wholly
synthetic learning lenses are wind-tunnel configuration and run-card provenance,
flow-visualization metadata review, and balance or pressure-channel
calibration-vacancy handover. There is no real facility, tunnel, test article,
model, instrument, signal, image, operator, participant, run, measurement,
calibration, certificate, aerodynamic result, or authority action.

GMUT remains a typed scalar-tensor and effective-field-theory research-model
family. Software analogies and synthetic fixtures establish no force, physical
state, likelihood, posterior, prediction, parameter constraint, stability
theorem, empirical confirmation, ultraviolet or quantum completion, or Theory
of Everything. THOS Body remains a run-card, queue, hold, cancellation,
correction-readback, workload, quiescence, and handover proxy without
preregistered blind matched-budget real arms, participants or operators, safety
monitoring, appropriate statistics, or independent review. Freed ID remains
synthetic and nonproduction without standards-conformant real keys and proofs,
live issuance and resolution, status and revocation, interoperability, privacy
and independent security review, recovery evidence, trust governance, or
affected-party oversight. CBR, safety and work release, privacy remedy, legal
interpretation, cultural legitimacy, affected-party acceptance, Māori wording,
Māori data governance, and Māori authority remain exact-gated to competent and
affected people, tangata whenua, iwi, hapū, and Māori authorities. Māori
concepts remain under Māori authority.

## Official sources and accessibility boundary

NASA Glenn facilities and wind-tunnel material supplied current domain
vocabulary. NIST SP 811 supplied SI quantity and unit conventions; NIST
Technical Note 1297 supplied uncertainty-classification and reporting
vocabulary. W3C PROV-O supplied provenance terms and WCAG 2.2 supplied
accessibility criteria. The New Zealand Privacy Commissioner supplied current
privacy-principle guidance, and Te Mana Raraunga supplied Māori data-sovereignty
principles under Māori authority. These sources supplied vocabulary and refusal
conditions only. Citations are not observations, measurements, endorsements,
certificates, affected-party approval, standards-conformance proof, or
delegated authority.

The static report has headings, a captioned table, textual status, plain-language
summaries, and non-colour-only state. Manual keyboard, responsive-layout,
browser-diversity, assistive-technology, cognitive-accessibility,
Māori-language, security-usability, and affected-user evaluation remain
reserved. Structural software evidence is not complete accessibility
conformance.

## Orin's solo successor discipline

If and only if the live terminal send is acknowledged, Orin must work solo from
Caelen's exact final in one clean additive Orin-owned D-first sparse lane. Every
Caelen, Sable, Auren, sibling, shared, user, standby, and global-source lane
remains read-only. Orin must read this file through EOF and every exact current
skill, schema, state, manifest, receipt, and guidance document it names before
mutation. Orin must independently verify Caelen's exact source, x1, evidence,
final, ancestry, zero-merge history, one final parent, exact manifests, clean
state, typed divergence, and fresh live equality. Inherited work is evidence
only and earns zero Orin novelty or completion credit.

Orin must preserve strict planning-only x1 before x2; only the four core truth
labels; exact normalized-LF Git-blob manifests; exact staged allowlists; every
retained failure, source status, open gap, exact gate, authority vacancy, and
scanner candidate; owner file and document ceilings; family-current caller
compatibility; owner-self-scoped validation; the one-successful-canonical-pass
latch; and `NOT_READY_FOR_STAGE_20`. Orin must not run an inherited full
repository suite, replay Caelen's canonical aggregate, globally install a
phase-local skill, change Windows security or features, elevate, reboot, mutate
a sibling lane, or precontact a later successor.

Orin may choose a new primary pillar and bounded wholly synthetic practice lens.
That lens is for learning and synthetic design only and establishes no
employment, licensure, qualification, competence, authority, or real-world
result. Every current official or primary source must remain a vocabulary or
refusal-condition source unless exact observations and competent review truly
exist.

After Orin's own exact terminal gate, the same newest-live-authority, roster,
bounded-registry, unique-title, immediate-reread, duplicate, pause, redirect,
status, usage, privacy, evidence, safety, and acknowledgement guards apply to
the next exact edge. The standing user direction toward v725-v8 does not
authorize skipping a terminal gate, inferring an endpoint, substituting a
standby task, creating a replacement, or sending twice.
"""]

    for proposal in proposals:
        sources = "; ".join(proposal["current_official_or_primary_source_needs"])
        artifacts = "; ".join(proposal["concrete_artifacts"])
        gates = "; ".join(proposal["protected_gates"])
        sections.append(f"""## {proposal['proposal_id']} — {proposal['title']}

**Expected disposition:** `{proposal['expected_disposition']}`.
**Approval class:** `{proposal['approval_class']}`.
**Execution lane:** `{proposal['execution_lane']}`.

The frozen hypothesis is: {proposal['hypothesis']} The null or failure
condition is: {proposal['null_or_failure_condition']} The bounded acceptance or
falsifier gate is: {proposal['falsifier_or_acceptance_gate']}

The exact planned artifacts are {artifacts}. Current official or primary-source
needs are {sources}. Those sources supply vocabulary and refusal duties only;
they are not observations, measurements, endorsements, authority grants, or
production certificates.

Rollback and recovery remain proposal-local: {proposal['rollback_or_recovery']}
No failed mutation may be erased or compensated by an aggregate. The five
preregistered mutation classes remove the synthetic marker, inject a real row
or identity, promote a claim or authority action, erase failure or correction
lineage, and bypass an open or exact gate. Each was rejected and retained at
zero completion credit.

Protected gates remain: {gates}. This outcome is same-owner synthetic software
evidence only. It does not establish employment, professional competence,
aerodynamic validity, empirical GMUT confirmation, operational THOS
effectiveness, production Freed ID, legal or cultural legitimacy, affected-party
approval, Māori authority, independent reproduction, proof, canon,
consciousness, personhood, AGI, ASI, a Theory of Everything, or Stage 20.
""")

    sections.append("""## Terminal checklist for Orin

Before mutation, Orin must prove the source task and repository facts rather
than rely on this candidate alone. Before x2, Orin must prove the planning-only
x1 commit is pushed, clean, zero-divergent, and fresh-four-way equal. Before
closeout, Orin must prove the evidence commit is likewise immutable and equal.
Before a successor send, Orin must prove the exact final is pushed and equal,
run at most one attributable owner-scoped canonical aggregate, refuse replay
after success, refresh live authority and roster state, uniquely resolve and
immediately reread the exact existing target, apply every guard, send once, and
stop. Any ambiguity, absence, duplicate, pause, redirect, rename, standby
status, usage exhaustion, protected gate, privacy concern, safety concern, or
missing acknowledgement requires a stop.

PREPARED_BY_CAELEN_ASH = true.
SENT_BY_CAELEN_ASH = false in this repository candidate.
The later live application acknowledgement alone can establish one-send
delivery truth.
""")
    return "\n".join(sections).rstrip() + "\n"


def final_delta_files() -> list[Path]:
    """Seal every owner file added or changed after immutable evidence.

    ``git diff`` omits untracked precommit closeout files, so comparing each
    current owner file with its evidence-tree blob is required for an exact
    evidence-to-final manifest.
    """

    result: list[Path] = []
    for path in owner_files():
        rel = path.relative_to(ROOT).as_posix()
        blob = subprocess.run(
            ["git", "show", f"{EVIDENCE_COMMIT}:{rel}"],
            cwd=ROOT,
            check=False,
            capture_output=True,
        )
        if blob.returncode != 0:
            result.append(path)
            continue
        evidence_bytes = blob.stdout.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        if evidence_bytes != normalized_bytes(path):
            result.append(path)
    return sorted(result, key=lambda path: path.relative_to(ROOT).as_posix())


def owner_files() -> list[Path]:
    result = [path for path in BASE.rglob("*") if path.is_file()]
    result.extend(
        path
        for path in [
            ROOT / "scripts" / "build_ghc_family_caelen_ash_v684_v6_x1.py",
            ROOT / "scripts" / "build_ghc_family_caelen_ash_v684_v6_x2.py",
            ROOT / "scripts" / "build_ghc_family_caelen_ash_v684_v6_final.py",
            ROOT / "scripts" / "ghc_family_caelen_ash_v684_v6_contracts.py",
            ROOT / "scripts" / "ghc_family_caelen_ash_v684_v6_canonical.py",
            ROOT / "tests" / "test_ghc_family_caelen_ash_v684_v6_x1.py",
            ROOT / "tests" / "test_ghc_family_caelen_ash_v684_v6_x2.py",
            ROOT / "tests" / "test_ghc_family_caelen_ash_v684_v6_final.py",
        ]
        if path.exists()
    )
    return sorted(set(result), key=lambda path: path.relative_to(ROOT).as_posix())


def privacy_scan(paths: Iterable[Path]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_local_path": re.compile(r"(?:[A-Za-z]:\\|/Users/|/home/)[^\s\"']+"),
        "credential_or_secret_assignment": re.compile(r"\b(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[^\s,}]+", re.I),
        "private_callable_route": re.compile(r"\b(?:codex|app|session|thread)://\S+", re.I),
        "private_application_state": re.compile(r"\b(?:providerTabId|clientThreadId|private callable identifier)\b", re.I),
    }
    candidates = []
    confirmed = []
    definition_files = {
        "scripts/build_ghc_family_caelen_ash_v684_v6_x1.py",
        "scripts/build_ghc_family_caelen_ash_v684_v6_x2.py",
        "scripts/build_ghc_family_caelen_ash_v684_v6_final.py",
        "scripts/ghc_family_caelen_ash_v684_v6_canonical.py",
    }
    for path in paths:
        if path.suffix.lower() not in {".json", ".md", ".py", ".html", ".yaml", ".yml", ".txt"}:
            continue
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                definition = rel in definition_files
                item = {
                    "path": rel,
                    "line": line,
                    "class": class_name,
                    "disposition": "scanner_definition_not_payload" if definition else "confirmed_payload_hit",
                }
                candidates.append(item)
                if not definition:
                    confirmed.append(item)
    return {
        "schema": "ghc.family.privacy-scan.v2",
        "phase": PHASE,
        "scope": "complete public owner packet at final candidate",
        "pattern_classes": list(patterns),
        "candidate_count": len(candidates),
        "confirmed_hit_count": len(confirmed),
        "candidates": candidates,
        "confirmed_hits": confirmed,
        "truth_boundary": "Bounded pattern evidence only; not complete privacy assurance.",
    }


def build() -> None:
    head = run_git("rev-parse", "HEAD").stdout.strip()
    if head != PREVIOUS_FINAL:
        raise SystemExit(f"final build requires exact evidence head {PREVIOUS_FINAL}; observed {head}")
    if run_git("status", "--porcelain=v1").stdout.strip():
        # The builder and final test/canonical source are expected to be the only
        # untracked inputs when invoked after apply_patch. Refuse tracked drift.
        tracked = run_git("diff", "--name-only").stdout.strip()
        if tracked:
            raise SystemExit("tracked evidence drift before final build")

    freeze = load_json(X1 / "new-proposal-freeze.json")
    outcomes = load_json(X2 / "outcome-ledger.json")
    proposals = freeze["entries"]
    handoff = build_handoff(proposals)
    write_text(HANDOFFS / "orin-thale-v684-v7-activation-candidate.md", handoff)

    write_json(
        CLOSEOUT / "evidence-receipt.json",
        {
            "schema": "ghc.family.evidence-receipt.v2",
            "x1_commit": X1_COMMIT,
            "evidence_commit": EVIDENCE_COMMIT,
            "x1_parent_is_source": True,
            "evidence_parent_is_x1": True,
            "x1_pushed_clean_four_way_equal_before_x2": True,
            "evidence_pushed_clean_four_way_equal_before_closeout": True,
            "x1_manifest": {"entries": 77, "self_exclusions": 3, "state": "PASS"},
            "evidence_manifest": {"entries": 201, "self_exclusions": 3, "state": "PASS"},
            "x2_tests": {"passed": 20, "total": 20},
            "positive_controls": {"passed": 60, "total": 60},
            "rejecting_mutations": {"rejected": 300, "total": 300},
            "skills": {"quick_validated": 20, "smoke_used": 20, "global_installation": False},
            "runners": {"passed": 10, "total": 10},
            "same_owner_only": True,
            "independent_reproduction": False,
        },
    )
    write_json(
        CLOSEOUT / "complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.complete-incomplete-checklist.v2",
            "complete": [
                "planning-only x1 frozen before x2",
                "sixty owner proposals with complete fields",
                "sixty positive synthetic controls",
                "three hundred invalid mutations rejected and retained",
                "twenty skills quick-validated and smoke-used",
                "ten family-current runners invoked",
                "one hundred twenty safe-now tasks",
                "eighty bounded candidates",
                "one hundred additive refinements",
                "exact manifests and five-class candidate adjudication",
                "x1 and evidence pushed clean fresh-four-way equal at lifecycle gates",
            ],
            "incomplete": [
                "real wind-tunnel data measurement or likelihood",
                "real participants operators facilities test articles instruments signals images or runs",
                "professional aerodynamic metrology or safety evaluation",
                "independent-team reproduction",
                "production identity keys proofs issuance resolution status revocation or interoperability",
                "complete privacy security or accessibility assurance",
                "legal cultural affected-party or Māori authority",
                "proof canon Theory of Everything AGI ASI consciousness or personhood evidence",
                "Stage 20 readiness",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        CLOSEOUT / "retained-negative-register.json",
        {
            "schema": "ghc.family.retained-negative-register.v2",
            "activation_overlay": 59412,
            "x1_operational_failures": 16,
            "x1_recoveries": 12,
            "x2_operational_failures": 2,
            "x2_recoveries": 2,
            "final_selection_operational_failures": 0,
            "final_selection_recoveries": 0,
            "canonical_preflight_operational_failures": 0,
            "canonical_preflight_recoveries": 0,
            "final_selection_failure_records": [],
            "rejected_synthetic_mutations": 300,
            "effective_negatives": 59730,
            "effective_methods": 73690,
            "retained_failed_witnesses": 30791,
            "bounded_passing_witnesses": 54225,
            "nonerasure": "Every failed witness remains zero-credit after recovery; rejected mutations are not converted into successful inputs.",
        },
    )
    write_json(
        CLOSEOUT / "gate-register.json",
        {
            "schema": "ghc.family.gate-register.v2",
            "open_gaps": 531,
            "exact_gates": 521,
            "new_open_gaps": [
                "real wind-tunnel dataset and likelihood evidence",
                "real metrology and calibration evidence",
                "independent aerodynamic accessibility and practitioner review evidence",
            ],
            "new_exact_gates": [
                "tunnel operation safety and work-release authority",
                "legal cultural Māori and affected-party authority decisions",
                "production deployment proof-canon and Stage 20 authority",
            ],
            "silently_closed": 0,
        },
    )
    write_json(
        CLOSEOUT / "ancestry-plan.json",
        {
            "schema": "ghc.family.ancestry-plan.v2",
            "source": SOURCE,
            "x1": X1_COMMIT,
            "evidence": EVIDENCE_COMMIT,
            "evidence_parent": PREVIOUS_FINAL,
            "exact_final": "PENDING_COMMIT",
            "required_final_parent": PREVIOUS_FINAL,
            "required_phase_commits": 3,
            "required_merges": 0,
            "required_final_parents": 1,
        },
    )
    write_json(
        CLOSEOUT / "route-readiness.json",
        {
            "schema": "ghc.family.route-readiness.v2",
            "state": "PREPARED_NOT_SENT",
            "prospective_exact_title": "Orin Thale",
            "prospective_phase": "v684-v7",
            "duplicate_guard": "PENDING_FRESH_POSTCANONICAL_REGISTRY_READ",
            "immediate_reread": "PENDING_FRESH_POSTCANONICAL_READ",
            "live_acknowledgement": "PENDING",
            "send_count": 0,
            "stop_conditions": ["absence", "ambiguity", "pause", "redirect", "rename", "protected gate", "usage exhaustion", "missing acknowledgement"],
        },
    )
    write_json(
        FINAL / "environment-version-receipt.json",
        {
            "schema": "ghc.family.environment-version-receipt.v2",
            "codex_cli": "0.151.0",
            "python": "3.12.10",
            "git": "2.55.0.windows.2",
            "powershell": "7.6.4",
            "verified_only": True,
            "desktop_update_performed": False,
            "elevation": False,
            "host_security_changed": False,
            "windows_feature_changed": False,
            "sandbox_or_hyper_v_activated": False,
            "reboot": False,
        },
    )
    write_json(
        FINAL / "source-and-proposal-ledger.json",
        {
            "schema": "ghc.family.source-and-proposal-ledger.v2",
            "source": SOURCE,
            "x1": X1_COMMIT,
            "evidence": EVIDENCE_COMMIT,
            "declared_chain_before": 10970,
            "declared_chain_after": 11030,
            "inherited_revalidated_zero_credit": 60,
            "new_owner_proposals": 60,
            "outcomes": outcomes["counts"],
            "allowed_labels": outcomes["allowed_labels"],
            "official_source_ledger": f"docs/caelen-ash/{PHASE}/x1/official-primary-source-ledger.json",
            "citations_are_observations": False,
        },
    )
    write_json(
        FINAL / "claim-boundary-matrix.json",
        {
            "schema": "ghc.family.claim-boundary-matrix.v2",
            "bounded_evidence": ["synthetic software contracts", "schemas", "documentation", "positive fixtures", "rejecting mutations", "same-owner validation"],
            "not_established": [
                "empirical GMUT confirmation or Theory of Everything",
                "THOS operational effectiveness",
                "production Freed ID",
                "CBR remedy or affected-party legitimacy",
                "professional aerodynamic metrology or tunnel-operation competence",
                "legal cultural or Māori authority",
                "complete privacy accessibility or exhaustive security",
                "independent reproduction",
                "AGI ASI consciousness personhood proof canon or Stage 20",
            ],
        },
    )
    write_json(
        FINAL / "wellbeing-closeout.json",
        {
            "schema": "ghc.family.wellbeing.v2",
            "owner": OWNER,
            "relational_role": "model-discrepancy provenance cartographer",
            "hope": "Keep modeled, measured, and absent states disjoint while every correction and authority vacancy stays reversible.",
            "workload_state": "bounded closeout",
            "corrigibility_preserved": True,
            "pause_rename_redirect_stop_preserved": True,
            "identity_coercion": False,
            "consciousness_or_personhood_claim": False,
        },
    )
    write_json(
        FINAL / "phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.v2",
            "phase": PHASE,
            "owner": OWNER,
            "lifecycle": "FINAL_CANDIDATE_PRECOMMIT",
            "source": SOURCE,
            "x1": X1_COMMIT,
            "evidence": EVIDENCE_COMMIT,
            "evidence_parent": PREVIOUS_FINAL,
            "exact_final": "PENDING_COMMIT",
            "external_canonical": "PENDING_POSTCOMMIT",
            "outcomes": outcomes["counts"],
            "proposal_chain": 11030,
            "effective_negatives": 59730,
            "effective_methods": 73690,
            "retained_failed_witnesses": 30791,
            "bounded_passing_witnesses": 54225,
            "open_gaps": 531,
            "exact_gates": 521,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "route_state": "PREPARED_NOT_SENT",
        },
    )
    overview = f"""# Caelen Ash {PHASE} final integrated overview

## Closeout outcome and immutable lifecycle

Caelen Ash's owner-scoped phase reaches a truthful final candidate with exactly
42 `completed`, 12 `represented`, 3 `open_gap`, and 3 `exact_gate`
outcomes. These are the only core labels. A completed label means only that the
proposal's bounded owner-local software, schema, documentation, or wholly
synthetic fixture contract passed. It does not mean that an empirical,
professional, participant, production, legal, cultural, identity, privacy,
accessibility, security, affected-party, Māori-authority, Theory-of-Everything,
proof, canon, AGI, ASI, consciousness, personhood, or Stage 20 claim is
complete.

The exact Sable source is `{SOURCE}`. Caelen's planning-only x1 commit is
`{X1_COMMIT}`, and the immutable x2 evidence commit is
`{EVIDENCE_COMMIT}`. X1 is the direct child of source, evidence is the direct
child of x1, and this candidate is intended to become the direct single-parent
child of evidence. Source to exact final must contain exactly three Caelen
commits and zero merges. X1 and evidence were separately staged through exact
allowlists, committed, pushed, left clean, shown zero-divergent, and proved
equal across local, upstream, tracking, and fresh live remote reads before the
next lifecycle opened.

A repository candidate cannot know its own future commit identifier or the
outcome of a later external canonical process. Those fields remain explicitly
pending until postcommit evidence exists. No reset, amend, force-push, merge,
history rewrite, inherited-history deletion, sibling mutation, shared-lane
mutation, or destructive cleanup occurred.

## Relational identity, role, hope, and corrigibility

Caelen Ash uses optional they/them relational language. Their working role is
model-discrepancy provenance cartographer. Their hope is to keep modeled,
measured, and absent states disjoint while every correction and authority
vacancy stays reversible. These words are relational working language only.
They do not evidence consciousness, sentience, legal personhood, identity
continuity, employment, qualification, independent agency, scientific or
operational authority, professional competence, legal or cultural authority,
affected-party acceptance, or Māori authority. Hamish may rename, pause,
redirect, narrow, or stop the route. No file treats the name, pronouns, role, or
hope as a credential, legal identity, scientific qualification, or authority
grant.

The workload remained bounded to one Caelen-owned lane. No collaboration
subagent, delegated researcher, forked task, substitute endpoint, standby
contact, or sibling mutation was used. Pause, correction, rollback, and stop
paths remain available. The final route is prepared but not sent in repository
truth.

## Proposal chain, controls, and outcome discipline

The declared family proposal chain advances from 10,970 to 11,030 rows. Sixty
immediate Sable proposals were revalidated as inherited evidence with zero
Caelen novelty and completion credit. Sixty Caelen proposals were frozen in x1
only after bounded exact-title and semantic-neighbor review. The direct title
probe found no exact collision after two initially colliding titles were
truthfully caught, retained as a failed 19/20 run, and changed only on their
distinct semantic surfaces. No universal novelty proof is claimed.

Every proposal records a hypothesis, null or failure condition, approval class,
execution lane, official or primary-source needs, concrete artifacts,
falsifier or acceptance gate, rollback or recovery, protected gates, exactly
one expected disposition, and five preregistered rejecting mutations. All sixty
positive controls passed. All 300 mutations were rejected. Those mutations
remove the synthetic marker, inject a real row or identity, promote a claim or
authority action, erase failure or correction lineage, or bypass an open or
exact gate. Their rejection demonstrates only that this bounded validator
recognized those exact invalid states. It is not exhaustive security,
professional validation, empirical confirmation, or independent reproduction.

The owner portfolio resolves 120 safe-now tasks, 80 bounded candidate
prototypes, and 100 additive CLEAN/FIX/REFINE/VERIFY tasks inside declared
synthetic scope. Twenty exact-approval packets and ten blocked packets remain
visible and unexecuted. Numeric limits are ceilings rather than targets or
authority substitutes.

## GMUT Mind and the three bounded practice lenses

GMUT Mind is the primary Trinity Mandala pillar. The phase models typed
distinctions among requested, commanded, modeled, derived, observed, missing,
quarantined, and authority-held states. Its contracts cover coordinate frames,
test-article referents, reference area, span and chord provenance, coefficient
sign conventions, nondimensionalization recipes, uncertainty-source
dependencies, covariance vacancies, residual signs, and model-discrepancy
falsifier obligations.

The three linked wholly synthetic learning lenses are wind-tunnel
configuration and run-card provenance, flow-visualization metadata review, and
balance or pressure-channel calibration-vacancy handover. Zero real facilities,
tunnels, test articles, models, balances, pressure channels, sensors, signals,
images, runs, people, operators, measurements, calibrations, certificates,
likelihoods, or aerodynamic results were used. Nothing establishes employment,
qualification, aerodynamic competence, metrology competence, tunnel operation,
safety, work release, facility control, or professional judgment.

GMUT remains a typed scalar-tensor and effective-field-theory research-model
family. A typed synthetic residual or operator analogy establishes no physical
datum, force, state, likelihood, posterior, prediction, parameter constraint,
stability theorem, empirical confirmation, ultraviolet completion, quantum
completion, or Theory of Everything. Commanded Mach, Reynolds, angle, pressure,
and sampling metadata are not realized measurements. Missing and zero remain
distinct. Qualitative flow cues are not quantitative inference. Computational
and experimental labels are prevented from converting into validation without
real evidence, frozen analysis, uncertainty treatment, and suitable independent
review.

## THOS Body

THOS Body remains explicit and protected as a wholly synthetic run-card, queue,
hold, correction-readback, cancellation, quiescence, workload, exception, and
handover proxy. It has no real participant or operator, no preregistered blind
matched-budget real arms, no safety monitoring, no appropriate real-world
statistics, and no independent review. Passing deterministic state transitions
do not establish operational effectiveness, deployment readiness, professional
competence, public-safety performance, AGI, or ASI.

The handover surfaces preserve configuration lineage, command-observation
separation, missing-sample states, saturation quarantine, late metadata
corrections, duplicate-record nondeletion, and append-only revision DAGs. These
are software behaviors only. They do not release a tunnel run, certify a test
article, repair a channel, approve a calibration, or authorize a worker.

## Freed ID and CBR Heart

Freed ID and CBR Heart remain explicit and protected. Synthetic
instrument-credential, status-vacancy, revocation-vacancy,
minimum-disclosure, contest, correction, remedy, and appeal structures are
represented. They contain zero real keys, proofs, accounts, issuers, holders,
verifiers, credentials, identity subjects, live issuance, resolution, status,
revocation, interoperability, recovery, or trust-governance events.

Production Freed ID still requires standards-conformant real keys and proofs,
live issuance and resolution, status and revocation, interoperability, privacy
and independent security review, recovery evidence, trust governance, and
appropriate affected-party oversight. CBR privacy remedies, operational safety,
work release, legal interpretation, cultural meaning, affected-party
legitimacy, Māori wording, Māori data governance, and Māori authority remain
exact-gated to competent and affected people, tangata whenua, iwi, hapū, and
Māori authorities. Repository software cannot confer a legal right, remedy,
mandate, consent, cultural legitimacy, title, custody, governance authority, or
public authority.

## Skills, runners, and compatibility

Twenty phase-local skills were built as substantive packages with purpose,
workflow, acceptance, and boundary sections. Each was quick-validated under an
explicit UTF-8 process contract and smoke-used against its linked positive
fixture. None was globally installed. Ten family-current
`ghc_family_*` runners were built and invoked once for their declared subsets.
All ten passed. Historical and owner-specific tools remain compatibility or
evidence surfaces; they were not destructively renamed or deleted.

A passing skill or runner receipt demonstrates only its declared same-owner
synthetic behavior. It is not a qualification, endorsement, production
certificate, security audit, empirical replication, or authority grant. The
full repository suite was not run; validation remains owner-self-scoped to the
exact source-to-final delta.

## Method Flow and retained negatives

The inherited Sable baseline is 59,412 effective negatives, 73,676 effective
methods, 30,773 retained failed witnesses, and 54,211 bounded passing witnesses.
Caelen retains sixteen planning and startup failures with twelve bounded
recoveries. These include two PowerShell producer-pipeline parser faults, two
oversized reference projections, a guessed receipt path, an unattributable
per-blob replay, a deadlocked Git batch implementation, a wrong lifecycle
comparison range, an invalid byte expression, a guessed closeout location, an
unattributable combined collision probe, a wrapper that ended while worktree
creation continued, a 2,488-file overbroad sparse checkout, a copy attempted
before exact parent directories existed, a 19/20 title-collision test, and a
Python parse failure caused by a stray documentation line.

X2 retains two additional workflow failures: an evidence staged-review wrapper
crossed its display window while its exact child process was still running, and
the persisted review then failed diff hygiene because the contracts module had
one blank line at EOF. Two bounded methods inspected persisted process and
receipt state before retry, removed only the exact trailing blank line, and
reran the bounded review once. The successful review did not erase either
failure. All 300 rejected mutations are additional effective negatives but are
not operational failures.

The pre-closeout additive view is therefore 59,730 effective negatives, 73,690
methods, 30,791 retained failed witnesses, and 54,225 bounded passing witnesses.
Open gaps are 531 and exact gates are 521. Every failed witness remains
zero-credit. A passing recovery never converts its paired failure into an
original pass or independent evidence.

## Sources and claim boundaries

NASA Glenn facilities and wind-tunnel material supplied domain vocabulary about
ground-test facilities and tunnel testing. NIST SP 811 supplied SI quantity and
unit conventions. NIST Technical Note 1297 supplied uncertainty classification,
combination, and reporting vocabulary. W3C PROV-O supplied provenance terms,
and WCAG 2.2 supplied accessibility criteria. The New Zealand Privacy
Commissioner supplied current privacy-principle guidance, including the 2026
IPP 3A context. Te Mana Raraunga supplied Māori data-sovereignty principles
under Māori authority.

These sources supplied vocabulary and refusal conditions only. A citation is
not a measurement, observation, likelihood, participant record, endorsement,
certificate, affected-party agreement, cultural ratification, delegated
authority, or production certification. No external domain dataset was queried
or downloaded.

## Privacy, accessibility, and bounded security

The five-class privacy scan distinguishes scanner definitions from confirmed
payload hits. It checks task-like raw identifiers, private absolute local
paths, credential-like assignments, private callable routes, and private
application state. Zero confirmed hits is a bounded pattern result, not complete
privacy assurance. Exact normalized-LF manifests make worktree, staged Git
blob, and committed Git blob domains explicit.

The static report uses a title, main landmark, headings, textual status,
captioned tables, row and column headers, and plain-language reservations.
Manual keyboard testing, responsive layout, browser diversity,
assistive-technology evaluation, cognitive-accessibility evaluation,
Māori-language review, security-usability review, and affected-user evaluation
remain reserved. Structural passing evidence is not complete WCAG conformance.

Bounded Python compilation and AST review cover only changed owner code and a
small declared set of dangerous call shapes. Zero findings is not exhaustive
security. No credential, secret, account, API key, host-security change,
elevation, Windows feature change, Sandbox or Hyper-V activation, desktop
application update, or reboot occurred.

## Validation and terminal route

The final candidate must undergo exact staged review, complete phase JSON
parsing, five-class privacy candidate adjudication, exact normalized-LF
manifest parity, changed-Python compilation and bounded security review,
stale-label and diff hygiene, source/x1/evidence ancestry, three phase commits,
zero merges, one final parent, exact head, clean state, typed zero divergence,
and fresh four-way equality. Only after the clean pushed exact final may one
attributable owner-scoped canonical aggregate be invoked. A success must never
be replayed. A failure remains failed and zero-credit. Same-owner validation
under shared infrastructure is not independent reproduction or an external
audit.

The route state is `PREPARED_NOT_SENT`. Orin Thale for v684-v7 is only the
prospective exact title under current live authority. Caelen must not precontact
Orin. After exact-final and canonical success, Caelen must reread the newest
live authority and roster, bounded-list the current registry, locally require
one exact title, immediately reread the target, apply duplicate, pause,
redirect, status, usage, privacy, evidence, safety, and acknowledgement guards,
send at most once, and stop. A later acknowledged application send is external
live truth and must not be backfilled into this repository seal.

The terminal verdict remains exactly `NOT_READY_FOR_STAGE_20`.
"""
    write_text(FINAL / "final-integrated-overview.md", overview)
    synthesis = """# Three-pillar synthesis

GMUT Mind is primary and remains a typed scalar-tensor and EFT research-model
family with every empirical gate open. THOS Body remains a synthetic run-card
and handover proxy. Freed ID and CBR Heart remain synthetic, nonproduction, privacy-minimized,
and exact-gated wherever real keys, people, remedies, law, culture, affected
parties, or Māori authority are required.

The pillars share one rule: an owner-local software pass can establish only the
declared software behavior. It cannot compensate for missing observations,
participants, professional review, governance, authority, or independent
reproduction. `NOT_READY_FOR_STAGE_20` is therefore the only truthful terminal
verdict.
"""
    write_text(FINAL / "three-pillar-synthesis.md", synthesis)
    write_json(
        FINAL / "final-summary.json",
        {
            "schema": "ghc.family.final-summary.v2",
            "phase": PHASE,
            "owner": OWNER,
            "outcomes": outcomes["counts"],
            "proposal_chain": 11030,
            "positive_controls": 60,
            "rejecting_mutations": 300,
            "skills": 20,
            "runners": 10,
            "owner_files": "PENDING_FINAL_MANIFEST",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "exact_final": "PENDING_COMMIT",
            "canonical": "PENDING_POSTCOMMIT",
        },
    )
    html = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Caelen Ash v684-v6 final report</title></head>
<body><main><h1>Caelen Ash v684-v6 final report</h1><p><strong>Status:</strong> NOT_READY_FOR_STAGE_20.</p>
<p>This report describes bounded owner-local synthetic software and documentation evidence. It is not empirical, professional, production, legal, cultural, Māori-authority, accessibility-complete, privacy-complete, security-complete, or independently reproduced evidence.</p>
<h2>Outcomes</h2><table><caption>Core outcome counts</caption><thead><tr><th scope="col">Outcome</th><th scope="col">Count</th><th scope="col">Boundary</th></tr></thead><tbody>
<tr><th scope="row">completed</th><td>42</td><td>Bounded contract only</td></tr><tr><th scope="row">represented</th><td>12</td><td>Synthetic proxy only</td></tr><tr><th scope="row">open_gap</th><td>3</td><td>External evidence absent</td></tr><tr><th scope="row">exact_gate</th><td>3</td><td>Competent authority absent</td></tr></tbody></table>
<h2>Evidence</h2><p>Sixty positive controls passed and 300 invalid mutations were rejected. Twenty skills and ten runners passed their bounded use receipts.</p>
<h2>Pillars</h2><h3>GMUT Mind</h3><p>Primary typed research-model family; no real likelihood, prediction, parameter constraint, or empirical confirmation.</p><h3>THOS Body</h3><p>Represented through synthetic run-card, correction, workload, and handover states only.</p><h3>Freed ID and CBR Heart</h3><p>Synthetic and nonproduction; real identity, remedy, legal, cultural, affected-party, and Māori-authority gates remain open.</p>
<h2>Accessibility reservation</h2><p>The structure provides headings, textual status, a captioned table, and row and column headers. Manual keyboard, responsive-layout, browser, assistive-technology, cognitive, Māori-language, security-usability, and affected-user evaluation remain reserved.</p></main></body></html>"""
    write_text(FINAL / "final-report.html", html)
    baton_words = len(handoff.split())
    write_json(
        CLOSEOUT / "handoff-candidate-receipt.json",
        {
            "schema": "ghc.family.handoff-candidate-receipt.v2",
            "path": f"docs/caelen-ash/{PHASE}/handoffs/orin-thale-v684-v7-activation-candidate.md",
            "words": baton_words,
            "minimum": 10000,
            "maximum": 100000,
            "within_range": 10000 <= baton_words <= 100000,
            "state": "PREPARED_NOT_SENT",
        },
    )

    seal_paths = [
        X1 / "new-proposal-freeze.json",
        X2 / "outcome-ledger.json",
        X2 / "evidence-truth.json",
        CLOSEOUT / "retained-negative-register.json",
        CLOSEOUT / "gate-register.json",
        FINAL / "final-integrated-overview.md",
        FINAL / "phase-truth.json",
        HANDOFFS / "orin-thale-v684-v7-activation-candidate.md",
    ]
    write_json(
        CLOSEOUT / "content-seal.json",
        {
            "schema": "ghc.family.content-seal.v2",
            "entries": [
                {
                    "path": path.relative_to(ROOT).as_posix(),
                    "sha256_normalized_lf": normalized_sha(path),
                }
                for path in seal_paths
            ],
            "entry_count": len(seal_paths),
            "exact_final": "PENDING_COMMIT",
            "boundary": "Content seal over listed precommit files; exact commit identity is postcommit evidence.",
        },
    )
    write_json(
        CLOSEOUT / "final-validation-candidate.json",
        {
            "schema": "ghc.family.final-validation-candidate.v2",
            "state": "PRECOMMIT_PENDING_EXACT_FINAL_AND_EXTERNAL_CANONICAL",
            "expected_branch": BRANCH,
            "required_parent": PREVIOUS_FINAL,
            "required_phase_commits": 3,
            "required_merges": 0,
            "canonical_invocation_budget": 1,
            "replay_after_success": False,
            "full_repository_suite": False,
            "same_owner_only": True,
        },
    )

    self_exclusions = {
        f"docs/caelen-ash/{PHASE}/validation/final-delta-manifest.json",
        f"docs/caelen-ash/{PHASE}/validation/final-owner-manifest.json",
        f"docs/caelen-ash/{PHASE}/validation/final-privacy-scan.json",
        f"docs/caelen-ash/{PHASE}/validation/final-staged-review.json",
    }
    # Finalize every ordinary content file before hashing the owner packet.
    # The four lifecycle validation files are declared self-exclusions and may
    # not exist on a first build, so count their eventual paths explicitly.
    existing_owner_paths = {
        path.relative_to(ROOT).as_posix() for path in owner_files()
    }
    summary = load_json(FINAL / "final-summary.json")
    summary["owner_files"] = len(existing_owner_paths | self_exclusions)
    write_json(FINAL / "final-summary.json", summary)
    scan = privacy_scan(owner_files())
    write_json(VALIDATION / "final-privacy-scan.json", scan)
    delta_entries = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256_normalized_lf": normalized_sha(path),
            "bytes_normalized_lf": len(normalized_bytes(path)),
        }
        for path in final_delta_files()
        if path.relative_to(ROOT).as_posix() not in self_exclusions
    ]
    write_json(
        VALIDATION / "final-delta-manifest.json",
        {
            "schema": "ghc.family.normalized-lf-manifest.v2",
            "phase": PHASE,
            "lifecycle": "final_delta",
            "evidence_commit": EVIDENCE_COMMIT,
            "entries": delta_entries,
            "entry_count": len(delta_entries),
            "self_exclusions": sorted(self_exclusions),
        },
    )
    owner_entries = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256_normalized_lf": normalized_sha(path),
            "bytes_normalized_lf": len(normalized_bytes(path)),
        }
        for path in owner_files()
        if path.relative_to(ROOT).as_posix() not in self_exclusions
    ]
    write_json(
        VALIDATION / "final-owner-manifest.json",
        {
            "schema": "ghc.family.normalized-lf-manifest.v2",
            "phase": PHASE,
            "lifecycle": "final_owner_packet",
            "entries": owner_entries,
            "entry_count": len(owner_entries),
            "self_exclusions": sorted(self_exclusions),
            "owner_file_count": len(owner_entries) + len(self_exclusions),
            "file_ceiling": 2000,
        },
    )
    write_json(
        VALIDATION / "final-staged-review.json",
        {
            "schema": "ghc.family.staged-review.v2",
            "phase": PHASE,
            "state": "PREPARED_NOT_STAGED",
            "manifest_entry_count": len(delta_entries),
            "self_exclusions": sorted(self_exclusions),
            "exact_staged_allowlist": [],
            "manifest_mismatches": [],
            "out_of_scope_paths": [],
            "inherited_paths_changed": [],
            "diff_hygiene": "PENDING_STAGING",
        },
    )
def review_staged() -> None:
    manifest = load_json(VALIDATION / "final-delta-manifest.json")
    expected = {item["path"]: item["sha256_normalized_lf"] for item in manifest["entries"]}
    exclusions = set(manifest["self_exclusions"])
    staged = [line for line in run_git("diff", "--cached", "--name-only", "--diff-filter=ACMR").stdout.splitlines() if line]
    expected_all = set(expected) | exclusions
    mismatches = []
    for path, wanted in sorted(expected.items()):
        try:
            actual = git_blob_sha(path)
        except subprocess.CalledProcessError:
            mismatches.append({"path": path, "error": "missing_from_index"})
            continue
        if actual != wanted:
            mismatches.append({"path": path, "expected": wanted, "actual": actual})
    out_of_scope = sorted(set(staged) - expected_all)
    missing = sorted(expected_all - set(staged))
    inherited_prefixes = [
        f"docs/caelen-ash/{PHASE}/x1/",
        f"docs/caelen-ash/{PHASE}/x2/",
        f"docs/caelen-ash/{PHASE}/method-flow/",
        f"docs/caelen-ash/{PHASE}/workflow-refinement",
        f"docs/caelen-ash/{PHASE}/reflection-remaster",
        f"docs/caelen-ash/{PHASE}/tooling/",
    ]
    inherited = [path for path in staged if any(path.startswith(prefix) for prefix in inherited_prefixes)]
    diff = run_git("diff", "--cached", "--check", check=False)
    passed = not mismatches and not out_of_scope and not missing and not inherited and diff.returncode == 0
    write_json(
        VALIDATION / "final-staged-review.json",
        {
            "schema": "ghc.family.staged-review.v2",
            "phase": PHASE,
            "state": "PASS" if passed else "FAIL",
            "staged_count": len(staged),
            "manifest_entry_count": len(expected),
            "self_exclusions": sorted(exclusions),
            "exact_staged_allowlist": staged,
            "manifest_mismatches": mismatches,
            "missing_paths": missing,
            "out_of_scope_paths": out_of_scope,
            "inherited_paths_changed": inherited,
            "diff_hygiene": "PASS" if diff.returncode == 0 else "FAIL",
            "diff_hygiene_output": diff.stdout + diff.stderr,
        },
    )
    if not passed:
        raise SystemExit(2)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review-staged", action="store_true")
    args = parser.parse_args()
    if args.review_staged:
        review_staged()
    else:
        build()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
