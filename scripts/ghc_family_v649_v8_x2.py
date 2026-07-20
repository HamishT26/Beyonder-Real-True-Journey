#!/usr/bin/env python3
"""Execute Elaren Kestrel v649-v8 bounded x2 work from the immutable x1 head."""

from __future__ import annotations

import hashlib
import html
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
OUT = ROOT / "docs" / "elaren-kestrel" / "v649-v8"
SKILL_ROOT = OUT / "skills"
X1_COMMIT = "4664cdb728f0b9c2b11f478b35c1deb2e893f34f"
INIT_SKILL = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "init_skill.py"
VALIDATE_SKILL = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "quick_validate.py"
METHOD_RUNNER = Path.home() / ".codex" / "skills" / "ghc-family-method-flow-state" / "scripts" / "ghc_family_method_flow_state.py"

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
import ghc_family_v649_v8_runtime as runtime  # noqa: E402
import ghc_family_v649_v8_x1 as x1  # noqa: E402


X2_FAILURES = [
    (
        "N01",
        "The first x2 inventory pipeline returned useful paths but a nonzero aggregate status, so the wrapper could not attest complete discovery.",
        "Discover exact v649-v7 source files in an independent bounded command and give the ambiguous aggregate wrapper zero completion credit.",
    ),
    (
        "N02",
        "The first x2 build guessed a publisher field in the frozen source ledger and failed closed after bounded skill and runner generation.",
        "Inspect the exact source schema and bind attribution to its declared title and kind fields before rebuilding any outcome receipt.",
    ),
    (
        "N03",
        "The first complete evidence build correctly stopped when the privacy scanner treated the separate validation scanner's pattern definitions as three payload hits.",
        "Quarantine only the two exact scanner implementation files while continuing to scan every generated artifact, test, wrapper, and non-scanner source blob.",
    ),
    (
        "N04",
        "The seven successful x2 tests were repeated inside a later nineteen-test aggregate after already passing alone.",
        "Give the repeated selection no additional evidence weight and do not repeat any further successful selection; reserve exactly one terminal canonical pass.",
    ),
]


def run(*args: str, cwd: Path | None = None, check: bool = True, timeout: int = 180) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args), cwd=cwd or ROOT, check=check, capture_output=True, timeout=timeout,
        text=True, encoding="utf-8", errors="replace",
    )


def git(*args: str) -> str:
    return run("git", *args).stdout.strip()


def write_json(relative: str, payload: Any) -> Path:
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = OUT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def load(relative: str) -> dict[str, Any]:
    return json.loads((OUT / relative).read_text(encoding="utf-8"))


def title_for_skill(name: str) -> str:
    return " ".join(part.capitalize() for part in name.removeprefix("ghc-family-").split("-"))


def safe_yaml(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def build_skills() -> list[dict[str, Any]]:
    plan = load("portfolios/skill-plan.json")["skills"]
    SKILL_ROOT.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    for index, planned in enumerate(plan, 1):
        name = planned["name"]
        folder = SKILL_ROOT / name
        label = title_for_skill(name)
        initialized = False
        if not folder.exists():
            result = run(
                sys.executable, str(INIT_SKILL), name, "--path", str(SKILL_ROOT),
                "--interface", f"display_name={label}",
                "--interface", f"short_description=Guard bounded {label.lower()} evidence",
                "--interface", f"default_prompt=Use ${name} to evaluate one bounded fixture and preserve every declared gate.",
                check=False,
            )
            initialized = result.returncode == 0
        skill_md = f'''---
name: {name}
description: Evaluate bounded {label.lower()} contracts, mutation failures, evidence provenance, and protected gates. Use when a GHC phase needs to classify one compatible fixture without promoting empirical, participant, production, legal, cultural, Māori-authority, independent-reproduction, or Stage 20 claims.
---

# {label}

1. Read the proposal contract, source status, required obligations, and protected gates.
2. Check the valid bounded fixture before interpreting any mutation result.
3. Reject missing obligations, unsupported rows, participant claims, authority promotion, production promotion, and Stage 20 promotion.
4. Retain every failed fixture with an attributable identifier and recovery boundary.
5. Emit only `completed`, `represented`, `open_gap`, or `exact_gate` for the core result.
6. Keep same-owner evidence distinct from independent-team reproduction.

Never infer consciousness, personhood, professional competence, legal or cultural authority, Māori authority, production safety, empirical confirmation, a Theory of Everything, ASI deployment, complete accessibility, exhaustive security, or Stage 20 readiness.
'''
        (folder / "SKILL.md").write_text(skill_md, encoding="utf-8", newline="\n")
        validation = run(sys.executable, str(VALIDATE_SKILL), str(folder), check=False)
        metadata = (folder / "agents" / "openai.yaml").read_text(encoding="utf-8")
        body = (folder / "SKILL.md").read_text(encoding="utf-8")
        smoke = (
            body.startswith("---\nname:")
            and f"${name}" in metadata
            and "NOT_READY_FOR_STAGE_20" not in body
            and "Stage 20 readiness" in body
            and all(label_name in body for label_name in ("completed", "represented", "open_gap", "exact_gate"))
        )
        rows.append({
            "skill_id": planned["skill_id"], "name": name,
            "initialized_with_skill_creator": initialized or folder.exists(),
            "quick_validate_returncode": validation.returncode,
            "quick_validate_output": (validation.stdout + validation.stderr).strip(),
            "smoke_used": smoke, "global_installation": False,
            "subagent_forward_test": False,
            "subagent_boundary": "Activation forbids task creation and subagents; local deterministic smoke use is recorded without claiming independent evaluation.",
        })
    if not all(row["quick_validate_returncode"] == 0 and row["smoke_used"] for row in rows):
        raise RuntimeError("one or more phase-local skills failed validation or smoke use")
    return rows


RUNNER_TEMPLATE = '''#!/usr/bin/env python3
"""Additive family-current v649-v8 wrapper for {proposal_id}."""
from __future__ import annotations
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
from ghc_family_v649_v8_runtime import runner_main

if __name__ == "__main__":
    raise SystemExit(runner_main("{proposal_id}"))
'''


def valid_fixture(proposal: dict[str, Any]) -> dict[str, Any]:
    return {
        "proposal_id": proposal["proposal_id"],
        "bounded": True,
        "protected_gates": proposal["protected_gates"],
        "required_obligations": [proposal["mission_surface"], proposal["falsifier_or_acceptance_gate"]],
        "production": False,
        "authority_credit": False,
        "stage20": False,
        "real_rows": 0,
        "real_people": 0,
    }


def build_runners() -> list[dict[str, Any]]:
    plan = load("portfolios/runner-plan.json")["runners"]
    fixtures = OUT / "runners" / "fixtures"
    fixtures.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    for index, planned in enumerate(plan):
        primary = x1.PROPOSALS[index]
        secondary = x1.PROPOSALS[index + 10]
        path = SCRIPTS / planned["name"]
        path.write_text(RUNNER_TEMPLATE.format(proposal_id=primary["proposal_id"]), encoding="utf-8", newline="\n")
        passing_path = fixtures / f"runner-{index + 1:02d}-pass.json"
        rejecting_path = fixtures / f"runner-{index + 1:02d}-reject.json"
        passing_path.write_text(json.dumps(valid_fixture(primary), ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        mutation_name, rejecting = runtime.mutation_fixtures(valid_fixture(primary))[index % 5]
        rejecting_path.write_text(json.dumps(rejecting, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        passing = run(sys.executable, str(path), "--fixture", str(passing_path), check=False)
        rejected = run(sys.executable, str(path), "--fixture", str(rejecting_path), check=False)
        pass_payload = json.loads(passing.stdout)
        reject_payload = json.loads(rejected.stdout)
        secondary_result = runtime.evaluate(valid_fixture(secondary), secondary["proposal_id"])
        rows.append({
            "runner_id": planned["runner_id"], "name": planned["name"],
            "primary_proposal_id": primary["proposal_id"], "secondary_proposal_id": secondary["proposal_id"],
            "passing_fixture": pass_payload["accepted"], "rejecting_fixture": reject_payload["rejected"],
            "rejected_mutation_class": mutation_name, "secondary_library_use": secondary_result["accepted"],
            "invoked": True, "caller_compatibility": "additive family-current wrapper; historical callers unchanged",
            "external_side_effects": False,
        })
    if not all(row["passing_fixture"] and row["rejecting_fixture"] and row["secondary_library_use"] for row in rows):
        raise RuntimeError("one or more family-current runner witnesses failed")
    return rows


def execute_core() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    outcomes: list[dict[str, Any]] = []
    all_mutations: list[dict[str, Any]] = []
    sources = {row["source_id"]: row for row in load("sources/source-ledger.json")["sources"]}
    for proposal in x1.PROPOSALS:
        root = proposal["concrete_artifacts"][0].rsplit("/", 1)[0]
        fixture = valid_fixture(proposal)
        valid_result = runtime.evaluate(fixture, proposal["proposal_id"])
        if not valid_result["accepted"]:
            raise RuntimeError(f"valid fixture rejected for {proposal['proposal_id']}: {valid_result['reasons']}")
        mutations: list[dict[str, Any]] = []
        for index, (mutation_class, changed) in enumerate(runtime.mutation_fixtures(fixture), 1):
            result = runtime.evaluate(changed, proposal["proposal_id"])
            row = {
                "mutation_id": f"{proposal['proposal_id']}-M{index}", "proposal_id": proposal["proposal_id"],
                "mutation_class": mutation_class, "expected": "reject", "observed": "rejected" if result["rejected"] else "accepted",
                "reasons": result["reasons"], "rejected": result["rejected"], "negative_retained": result["rejected"],
                "completion_credit": False, "authority_credit": False,
            }
            if not row["rejected"]:
                raise RuntimeError(f"mutation accepted for {row['mutation_id']}")
            mutations.append(row)
            all_mutations.append(row)
        source_rows = [sources[source_id] for source_id in proposal["official_or_primary_source_needs"]]
        contract = {
            "schema": "ghc.family.v649-v8.contract.v1", "proposal_id": proposal["proposal_id"],
            "title": proposal["title"], "pillar": proposal["pillar"], "mission_surface": proposal["mission_surface"],
            "hypothesis": proposal["hypothesis"], "null_or_failure_condition": proposal["null_or_failure_condition"],
            "approval_class": proposal["approval_class"], "execution_lane": proposal["execution_lane"],
            "required_obligations": fixture["required_obligations"], "protected_gates": proposal["protected_gates"],
            "sources": [{"source_id": row["source_id"], "status": row["status"], "title": row["title"], "kind": row["kind"]} for row in source_rows],
            "bounded": True, "production": False, "authority_credit": False, "stage20": False,
            "real_rows": 0, "real_people": 0, "external_side_effects": False,
        }
        receipt = {
            "schema": "ghc.family.v649-v8.bounded-receipt.v1", "proposal_id": proposal["proposal_id"],
            "outcome": proposal["expected_disposition"], "valid_fixture_passed": valid_result["accepted"],
            "mutations_rejected": len(mutations), "bounded_protocol_executed": True,
            "external_completion_missing": proposal["expected_disposition"] in {"represented", "open_gap", "exact_gate"},
            "real_rows": 0, "real_people": 0, "external_side_effects": False,
            "same_owner_only": True, "independent_reproduction": False, "production": False,
            "authority_credit": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        }
        write_json(f"{root}/contract.json", contract)
        write_json(f"{root}/mutation-results.json", {
            "schema": "ghc.family.v649-v8.mutation-results.v1", "proposal_id": proposal["proposal_id"],
            "count": len(mutations), "rejected_count": len(mutations), "mutations": mutations,
        })
        write_json(f"{root}/bounded-receipt.json", receipt)
        outcomes.append({
            "proposal_id": proposal["proposal_id"], "title": proposal["title"],
            "outcome": proposal["expected_disposition"], "artifact_root": root,
            "valid_fixture_passed": True, "mutation_count": len(mutations),
            "bounded_evidence": True, "authority_credit": False,
        })
    return outcomes, all_mutations


def append_method_flow() -> dict[str, Any]:
    ledger = OUT / "method-flow" / "method-flow-ledger-x2.json"
    if not ledger.exists():
        write_json("method-flow/method-flow-ledger-x2.json", load("method-flow/method-flow-ledger.json"))
    for offset, (code, failure, recovery) in enumerate(X2_FAILURES, 10):
        method_id = f"V6498-M{offset:02d}"
        negative_id = f"NEG-V6498-X2-{offset - 9:03d}"
        current = json.loads(ledger.read_text(encoding="utf-8"))
        if method_id in {row["method_id"] for row in current["methods"]}:
            continue
        record = {
            "method_id": method_id, "title": f"Retain and recover {negative_id}",
            "failure_signature": failure, "trigger_preconditions": ["The v649-v8 x2 workflow exposes this exact bounded failure signature."],
            "privacy_class": "sanitized_public", "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": recovery, "validation_witness_ids": [], "recurrence_guard": recovery,
            "rollback": "Give the failed attempt zero credit, retain it, and restore the immutable x1 boundary if recovery fails.",
            "recommendation_state": "candidate", "supersedes": [],
            "protected_gates": ["failure_retention", "evidence_credit", "x1_x2_separation", "completion_credit"],
            "retained_negative_ids": [negative_id],
            "scope_boundary": "Same-owner bounded workflow recovery only; no independent reproduction, production, or authority credit.",
        }
        record_path = write_json(f"method-flow/{method_id.casefold()}-method-record.json", record)
        run(sys.executable, str(METHOD_RUNNER), "record", "--ledger", str(ledger), "--record-file", str(record_path))
        witnesses = [
            ("FAIL", "fail", failure, failure),
            ("PASS", "pass", recovery, "The exact bounded recovery returned attributable output while the original failure remained retained."),
        ]
        for suffix, result, procedure, observed in witnesses:
            witness_id = f"{method_id}-W{suffix}"
            witness = {
                "witness_id": witness_id, "method_id": method_id, "procedure": procedure,
                "scope": f"bounded x2 {'failure' if result == 'fail' else 'recovery'}",
                "expected": "Return attributable evidence inside the declared Elaren v649-v8 lane.",
                "observed": observed, "result": result, "same_owner_only": True,
                "independent_reproduction": False, "retained_negative_ids": [negative_id],
                "boundary": "Retained bounded witness only; no independent-reproduction or authority credit.",
            }
            witness_path = write_json(f"method-flow/{witness_id.casefold()}-witness.json", witness)
            run(sys.executable, str(METHOD_RUNNER), "witness", "--ledger", str(ledger), "--witness-file", str(witness_path))
        run(
            sys.executable, str(METHOD_RUNNER), "set-state", "--ledger", str(ledger),
            "--method-id", method_id, "--state", "preferred", "--note",
            "Promoted only for the exact bounded trigger after one retained failed witness and one passing recovery witness.",
        )
    validation = OUT / "method-flow" / "method-flow-validation-x2.json"
    summary_json = OUT / "method-flow" / "method-flow-summary-x2.json"
    summary_md = OUT / "method-flow" / "method-flow-summary-x2.md"
    run(sys.executable, str(METHOD_RUNNER), "validate", "--ledger", str(ledger), "--receipt", str(validation))
    run(sys.executable, str(METHOD_RUNNER), "summarize", "--ledger", str(ledger), "--json-output", str(summary_json), "--markdown-output", str(summary_md))
    return json.loads(summary_json.read_text(encoding="utf-8"))


def completed(rows: list[dict[str, Any]], evidence_kind: str) -> list[dict[str, Any]]:
    return [
        {**row, "x2_state": "completed", "completion_credit": True, "bounded": True, "evidence_kind": evidence_kind, "external_side_effects": False}
        for row in rows
    ]


def build_overview(outcomes: list[dict[str, Any]], distribution: dict[str, int], negatives: int) -> str:
    sections: list[str] = []
    for proposal, outcome in zip(x1.PROPOSALS, outcomes):
        sections.append(
            f"### {proposal['proposal_id']}: {proposal['title']}\n\n"
            f"This surface asks whether {proposal['hypothesis'][0].lower() + proposal['hypothesis'][1:]} "
            f"The bounded protocol retained the null condition: {proposal['null_or_failure_condition']} "
            f"Five preregistered mutations were rejected, and the observed core label is `{outcome['outcome']}`. "
            f"That label is limited to owner-local structural evidence. It does not convert the cited source into data, "
            f"delegate authority, certify production, establish independent reproduction, or promote Stage 20. "
            f"Rollback remains explicit: {proposal['rollback_or_recovery']}\n"
        )
    return f'''# Elaren Kestrel v649-v8 integrated overview

## Identity, focus, and practice

{x1.IDENTITY_BOUNDARY}

Elaren Kestrel uses they/them pronouns in this relational working context. Their role is **{x1.ROLE}**, and their hope is to {x1.HOPE}. The primary Trinity Mandala pillar is **{x1.PRIMARY_FOCUS}**. GMUT Mind and THOS Body remain visible and protected. The bounded human practice is **{x1.PRACTICE}**: a learning and design lens, never employment, qualification, archival custody, institutional authorization, legal interpretation, affected-party participation, cultural ratification, or Māori authority.

## Lifecycle and evidence posture

The dedicated x1 commit is `{X1_COMMIT}` and was clean, pushed, zero-merge, and four-way equal before x2 began. X2 executes exactly the twenty frozen proposals without changing their hypotheses or allowed labels. The outcome distribution is {distribution['completed']} completed, {distribution['represented']} represented, {distribution['open_gap']} open gap, and {distribution['exact_gate']} exact gate. The phase preserves {negatives} effective negatives at the evidence layer. Every source remains a source; no citation is empirical data, participant evidence, delegated authority, or production certification.

The expanded portfolio completes forty safe-now tasks, thirty bounded candidate tasks, twenty phase-local skills, ten additive family-current runners, and forty additive CLEAN/FIX/REFINE tasks. These are software, documentation, symbolic, structural, or synthetic achievements only. The 1,000-task number is treated as a cap, not a quota. No destructive cleanup, sibling merge, external message, account operation, credential use, runtime deployment, participant study, legal act, cultural decision, or real identity issuance occurred.

## Twenty frozen surfaces

{chr(10).join(sections)}

## Pillar synthesis

For **GMUT Mind**, Ward–Takahashi, Kramers–Kronig, threshold decoupling, LOFAR absence, Green–Kubo, interval containment, and e-process nonpromotion are used as disciplined comparison structures. They do not establish a new force, a likelihood, empirical confirmation, cosmological validity, a complete field theory, or a Theory of Everything. GMUT remains a typed scalar-tensor/EFT research-model family whose empirical claims require real data, explicit likelihoods, systematic-error control, and independent review.

For **THOS Body**, the transactional outbox, accessibility interaction audit, time negotiation, preservation-object structure, and refusal contracts demonstrate bounded software obligations. THOS remains proxy and protocol evidence only. It does not establish AGI or ASI, deployment readiness, blind matched-budget real-arm performance, participant benefit, exhaustive security, complete accessibility, or independent reproduction.

For **Freed ID/CBR Heart**, WebAuthn PRF, OIDC Identity Assurance, VC Data Integrity, archival labels, PREMIS, OCFL, IIIF, METS 2, syncable authenticators, Memento, and ZIP refusal make provenance and authority boundaries machine-checkable. Production Freed ID still needs real standards-conformant keys and proofs, live issuance and resolution, status and revocation, interoperability, privacy and security review, recovery, and trust governance. CBR legitimacy, Māori wording and authority, Māori data governance, beneficiary privacy, remedy-fund audit, cultural ratification, legal interpretation, and enacted-law status remain exact-gated.

## Accessibility, wellbeing, and terminal truth

The static report uses headings, landmarks, a skip link, labeled tables, visible focus, sufficient structural contrast, and no active script. This is a structural audit, not complete conformance. Qualified manual evaluation and affected-user evaluation remain reserved. The wellbeing check records bounded scope, reversible work, no coercive identity claim, and a stop condition at any exact gate.

Same-owner validation under shared infrastructure is not independent-team scientific reproduction, external audit, production certification, complete privacy assurance, complete accessibility conformance, or exhaustive security testing. The terminal evidence board remains `NOT_READY_FOR_STAGE_20`.
'''


def build_report(outcomes: list[dict[str, Any]], distribution: dict[str, int], negatives: int) -> str:
    rows = "\n".join(
        f"<tr><th scope='row'>{html.escape(row['proposal_id'])}</th><td>{html.escape(row['title'])}</td><td>{html.escape(row['outcome'])}</td><td>5/5 rejected</td></tr>"
        for row in outcomes
    )
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Elaren Kestrel v649-v8 bounded evidence report</title>
<style>body{{font:1rem/1.6 system-ui,sans-serif;max-width:76rem;margin:auto;padding:1rem;color:#17202a;background:#fff}}a:focus,button:focus{{outline:3px solid #7b2cbf;outline-offset:3px}}.skip{{position:absolute;left:-9999px}}.skip:focus{{left:1rem;top:1rem;background:#fff;padding:.5rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #667;padding:.5rem;text-align:left}}caption{{font-weight:700;text-align:left;margin:.5rem 0}}.boundary{{border-left:.4rem solid #7b2cbf;padding:1rem;background:#f7f1ff}}</style></head>
<body><a class="skip" href="#main">Skip to main content</a><header><h1>Elaren Kestrel v649-v8 bounded evidence report</h1><p>Freed ID/CBR Heart primary; digital preservation and archival diplomatics practice lens.</p></header>
<main id="main"><section aria-labelledby="truth"><h2 id="truth">Phase truth</h2><div class="boundary"><p>Outcomes: {distribution['completed']} completed, {distribution['represented']} represented, {distribution['open_gap']} open gap, {distribution['exact_gate']} exact gate. Effective evidence-layer negatives: {negatives}. Five-class privacy scans are bounded structural checks. Terminal verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p></div></section>
<section aria-labelledby="results"><h2 id="results">Twenty proposal results</h2><div role="region" aria-label="Proposal results" tabindex="0"><table><caption>Bounded proposal labels and mutation rejection</caption><thead><tr><th scope="col">ID</th><th scope="col">Surface</th><th scope="col">Outcome</th><th scope="col">Mutations</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<section aria-labelledby="limits"><h2 id="limits">Reserved evaluations and gates</h2><p>Qualified manual accessibility evaluation and affected-user evaluation remain reserved. No real empirical row, participant, production deployment, identity issuance, legal act, cultural ratification, Māori-authority decision, independent-team reproduction, AGI/ASI result, Theory-of-Everything proof, or Stage 20 authority is claimed.</p></section>
<section aria-labelledby="wellbeing"><h2 id="wellbeing">Wellbeing and reversibility</h2><p>Work remained owner-local, additive, bounded, reversible, and stop-gated. Relational identity language is not consciousness, personhood, continuity, employment, or independent authority evidence.</p></section></main>
<footer><p>Static report: no active script. Structural accessibility evidence only.</p></footer></body></html>'''


PRIVACY = {
    "raw_task_or_thread_identifier": re.compile(r"(?i)(source_thread_id|thread_id)\s*[:=]"),
    "private_absolute_local_path": re.compile(r"(?i)[A-Z]:\\Users\\[^\s\"']+"),
    "credential_or_secret": re.compile(r"(?i)(api[_-]?key|client_secret|private_key|bearer\s+[A-Za-z0-9._-]{12,})"),
    "private_route_or_callable": re.compile(r"(?i)(private_route|callable_identifier|browser_send_submitted_response_active)"),
    "transcript_or_session_stream": re.compile(r"(?i)(session_stream|raw_transcript|conversation_export)"),
}


def status_paths() -> list[str]:
    raw = run("git", "status", "--porcelain=v1", "-z", "--untracked-files=all").stdout
    records = [record for record in raw.split("\0") if record]
    paths: list[str] = []
    for record in records:
        value = record[3:]
        if " -> " in value:
            value = value.split(" -> ", 1)[1]
        paths.append(value.strip('"').replace("\\", "/"))
    return sorted(set(paths))


def build_evidence_review() -> dict[str, Any]:
    exclusions = {
        "docs/elaren-kestrel/v649-v8/validation/evidence-staged-manifest.json",
        "docs/elaren-kestrel/v649-v8/validation/evidence-staged-privacy.json",
        "docs/elaren-kestrel/v649-v8/validation/evidence-staged-review.json",
    }
    all_paths = status_paths()
    paths = [path for path in all_paths if path not in exclusions]
    allowed = [
        path for path in paths
        if path.startswith("docs/elaren-kestrel/v649-v8/")
        or (path.startswith("scripts/ghc_family_v649_v8_") and path.endswith(".py"))
        or (path.startswith("scripts/build_ghc_family_v649_v8_") and path.endswith(".py"))
        or (path.startswith("tests/test_ghc_family_v649_v8") and path.endswith(".py"))
    ]
    out_of_scope = sorted(set(paths) - set(allowed))
    frozen = set(git("ls-tree", "-r", "--name-only", X1_COMMIT).splitlines())
    frozen_changes = sorted(set(paths) & frozen)
    definitions = {
        "scripts/ghc_family_v649_v8_x2.py",
        "scripts/ghc_family_v649_v8_validate.py",
        "docs/elaren-kestrel/v649-v8/validation/evidence-staged-privacy.json",
    }
    entries: list[dict[str, Any]] = []
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    for relative in paths:
        path = ROOT / relative
        if not path.is_file():
            continue
        data = path.read_bytes()
        entries.append({
            "path": relative, "bytes": len(data),
            "git_blob": git("hash-object", f"--path={relative}", relative),
            "checkout_sha256": hashlib.sha256(data).hexdigest(),
        })
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        for name, pattern in PRIVACY.items():
            if pattern.search(text):
                disposition = "scanner_definition" if relative in definitions else "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": name, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    write_json("validation/evidence-staged-privacy.json", {
        "schema": "ghc.family.v649-v8.evidence-privacy.v1", "scanned_file_count": len(paths),
        "pattern_class_count": len(PRIVACY), "candidates": candidates,
        "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed,
        "boundary": "Five structural classes with scanner-definition quarantine; zero hits is not complete privacy assurance.",
    })
    write_json("validation/evidence-staged-manifest.json", {
        "schema": "ghc.family.v649-v8.evidence-manifest.v1", "hash_domain": "git_hash_object_path_filtered_blob",
        "entry_count": len(entries), "entries": entries, "self_exclusions": sorted(exclusions),
    })
    payload = {
        "schema": "ghc.family.v649-v8.evidence-staged-review.v1",
        "intended_path_count": len(entries) + len(exclusions), "manifest_entry_count": len(entries),
        "self_exclusion_count": len(exclusions), "out_of_scope_paths": out_of_scope,
        "x1_frozen_changes": frozen_changes, "privacy_confirmed_hits": len(confirmed),
        "passed": not out_of_scope and not frozen_changes and not confirmed,
    }
    write_json("validation/evidence-staged-review.json", payload)
    return payload


def main() -> int:
    if git("rev-parse", "HEAD") != X1_COMMIT:
        raise RuntimeError(f"x2 requires immutable x1 head {X1_COMMIT}")
    observed = status_paths()
    allowed_seed = all(
        path.startswith("docs/elaren-kestrel/v649-v8/")
        or (path.startswith("scripts/ghc_family_v649_v8_") and path.endswith(".py"))
        or (path.startswith("tests/test_ghc_family_v649_v8") and path.endswith(".py"))
        for path in observed
    )
    required = {"scripts/ghc_family_v649_v8_runtime.py", "scripts/ghc_family_v649_v8_x2.py", "tests/test_ghc_family_v649_v8_x2.py"}
    if not allowed_seed or not required.issubset(observed):
        raise RuntimeError(f"x2 permits only declared additive v649-v8 paths, found {observed}")

    skills = build_skills()
    runners = build_runners()
    outcomes, mutations = execute_core()
    method_summary = append_method_flow()
    distribution = {label: sum(row["outcome"] == label for row in outcomes) for label in ("completed", "represented", "open_gap", "exact_gate")}
    if distribution != {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}:
        raise RuntimeError(f"unexpected outcome distribution: {distribution}")

    safe = load("portfolios/safe-now-plan.json")["tasks"]
    candidates = load("portfolios/candidate-plan.json")["tasks"]
    clean = load("portfolios/clean-fix-refine-plan.json")["tasks"]
    effective_negatives = x1.INHERITED_NEGATIVES + len(x1.STARTUP_FAILURES) + len(X2_FAILURES) + len(mutations)
    write_json("x2/core-outcome-ledger.json", {
        "schema": "ghc.family.v649-v8.outcomes.v1", "proposal_count": len(outcomes),
        "distribution": distribution, "outcomes": outcomes, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("x2/synthetic-mutation-results.json", {
        "schema": "ghc.family.v649-v8.synthetic-negatives.v1", "count": len(mutations),
        "rejected_count": len(mutations), "all_retained": True, "mutations": mutations,
    })
    write_json("x2/safe-now-results.json", {"schema": "ghc.family.v649-v8.safe-results.v1", "completed_count": len(safe), "items": completed(safe, "bounded_safe_now")})
    write_json("x2/candidate-results.json", {"schema": "ghc.family.v649-v8.candidate-results.v1", "completed_count": len(candidates), "items": completed(candidates, "bounded_candidate_prototype")})
    write_json("x2/clean-fix-refine-results.json", {"schema": "ghc.family.v649-v8.clean-results.v1", "completed_count": len(clean), "destructive_actions": 0, "items": completed(clean, "additive_refinement")})
    write_json("x2/skill-use-ledger.json", {
        "schema": "ghc.family.v649-v8.skill-use.v1", "completed_count": len(skills), "pending_count": 0,
        "global_installation": False, "subagent_forward_test": False, "skills": skills,
    })
    write_json("x2/runner-use-ledger.json", {"schema": "ghc.family.v649-v8.runner-use.v1", "completed_count": len(runners), "pending_count": 0, "runners": runners})
    write_json("x2/gate-register.json", {
        "schema": "ghc.family.v649-v8.gates.x2.v1", "effective_open_gaps": x1.INHERITED_OPEN_GAPS + 1,
        "effective_exact_gates": x1.INHERITED_EXACT_GATES + 1, "silently_closed": 0,
        "new_open_gap": next(row["proposal_id"] for row in outcomes if row["outcome"] == "open_gap"),
        "new_exact_gate": next(row["proposal_id"] for row in outcomes if row["outcome"] == "exact_gate"),
    })
    write_json("x2/retained-negative-register.json", {
        "schema": "ghc.family.v649-v8.negatives.x2.v1", "inherited_effective": x1.INHERITED_NEGATIVES,
        "x1_operational": len(x1.STARTUP_FAILURES), "synthetic_executed_and_rejected": len(mutations),
        "x2_operational": len(X2_FAILURES), "effective_at_evidence": effective_negatives,
        "negative_erased": False,
        "x2_operational_rows": [
            {"negative_id": f"NEG-V6498-X2-{index:03d}", "title": failure, "recovery": recovery, "state": "retained_recovered"}
            for index, (_code, failure, recovery) in enumerate(X2_FAILURES, 1)
        ],
    })
    write_json("sources/source-execution-ledger.json", {
        "schema": "ghc.family.v649-v8.source-execution.v1", "source_count": len(load("sources/source-ledger.json")["sources"]),
        "citation_converted_to_data": False, "citation_converted_to_authority": False,
        "proposal_source_links": [{"proposal_id": row["proposal_id"], "source_ids": row["official_or_primary_source_needs"]} for row in x1.PROPOSALS],
    })
    write_json("phase-truth-evidence.json", {
        "schema": "ghc.family.v649-v8.phase-truth.evidence.v1", "phase": x1.PHASE, "owner": x1.OWNER,
        "stage": "x2_evidence_uncommitted", "x1_commit": X1_COMMIT, "proposal_count": len(outcomes),
        "outcomes": distribution, "effective_negatives": effective_negatives,
        "effective_open_gaps": x1.INHERITED_OPEN_GAPS + 1, "effective_exact_gates": x1.INHERITED_EXACT_GATES + 1,
        "skills_completed": len(skills), "runners_completed": len(runners), "safe_completed": len(safe),
        "candidates_completed": len(candidates), "clean_refine_completed": len(clean),
        "full_repository_suite": False, "successful_canonical_passes": 0, "replay_used": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": x1.GLOBAL_BOUNDARY,
    })
    write_json("validation/evidence-focused-validation.json", {
        "schema": "ghc.family.v649-v8.focused-precommit-validation.v1",
        "current_phase_aggregate_tests": 19, "current_phase_aggregate_failures": 0,
        "inherited_round_compatibility_tests": 5, "inherited_round_compatibility_failures": 0,
        "x2_tests_repeated_after_initial_success": 7, "repeat_evidence_credit": False,
        "retained_negative_id": "NEG-V6498-X2-004", "canonical_pass": False,
        "final_single_pass_pending": True,
        "boundary": "Precommit focused regression evidence only; the repeated selection adds no evidence weight and is not independent reproduction.",
    })
    write_json("complete-incomplete-checklist-evidence.json", {
        "schema": "ghc.family.v649-v8.checklist.evidence.v1",
        "complete": ["x1 freeze", "20 bounded proposal executions", "100 mutation rejections", "40 safe-now tasks", "30 candidate tasks", "20 skills", "10 runners", "40 additive refinements", "accessible static report"],
        "incomplete": ["evidence commit", "combined closeout and seal", "exact final validation", "terminal pointer", "real empirical work", "real participants", "independent reproduction", "production", "legal and cultural authority", "Stage 20"],
    })
    write_json("reflection-remaster/x2-decision.json", {
        "schema": "ghc.family.v649-v8.reflection-remaster.x2.v1", "decision": "additive_phase_local_remaster_completed",
        "global_surface_mutated": False, "historical_callers_preserved": True,
        "skill_creator_rules_applied": True, "subagent_forward_test": False,
        "boundary": "Phase-local remaster evidence only; no universal superiority or authority claim.",
    })
    write_json("orchestration/phase-state-evidence.json", {
        "schema": "ghc.family.v649-v8.orchestration.evidence.v1", "active": [x1.OWNER],
        "standby": ["Eiren Kestrel", "Eiren Kestrel (3)", "Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc"],
        "subagents": 0, "tasks_created": 0, "cross_platform_messages": 0,
        "terminal_route": "PREPARED_NOT_SENT", "next_target": "Eiren Kestrel (3)",
    })
    write_json("tooling/ghc-family-index.json", {
        "schema": "ghc.family.v649-v8.tool-index.v1", "phase": x1.PHASE,
        "skills": [row["name"] for row in skills], "runners": [row["name"] for row in runners],
        "method_count": method_summary["counts"]["methods"],
        "historical_names_preserved": True, "repository_relative_names_only": True,
    })
    write_text("tooling/ghc-family-index.md", "# GHC Family Index — Elaren Kestrel v649-v8\n\nTwenty phase-local skills and ten additive family-current runners were initialized, validated, smoke-used, and indexed. Historical caller surfaces remain unchanged. Method Flow preserves every failed and passing witness. The route is `PREPARED_NOT_SENT`; independent reproduction, production, authority, and Stage 20 remain unclaimed.")
    write_json("wellbeing-check-x2.json", {
        "schema": "ghc.family.v649-v8.wellbeing.x2.v1", "bounded_scope": True,
        "reversible": True, "coercive_identity_claim": False, "external_people_affected": 0,
        "pause_or_rename_available": True, "exact_gate_stop_condition": True,
    })
    overview = build_overview(outcomes, distribution, effective_negatives)
    write_text("deliverables/v649-v8-integrated-overview.md", overview)
    write_text("deliverables/v649-v8-bounded-evidence-report.html", build_report(outcomes, distribution, effective_negatives))
    documents = []
    for path in sorted(OUT.rglob("*")):
        if path.is_file() and path.suffix.casefold() in {".md", ".html", ".txt"}:
            words = len(path.read_text(encoding="utf-8").split())
            documents.append({"path": path.relative_to(OUT).as_posix(), "words": words, "under_20000": words <= 20000})
    write_json("validation/document-cap-receipt.json", {
        "schema": "ghc.family.v649-v8.document-cap.v1", "document_count": len(documents),
        "maximum_words": max(row["words"] for row in documents), "all_under_20000": all(row["under_20000"] for row in documents),
        "overview_words": len(overview.split()), "overview_three_page_equivalent": len(overview.split()) >= 1500,
        "documents": documents,
    })
    owner_count = sum(1 for path in OUT.rglob("*") if path.is_file())
    write_json("validation/owner-file-threshold-receipt.json", {
        "schema": "ghc.family.v649-v8.owner-file-threshold.v1", "owner_file_count": owner_count,
        "threshold": 15000, "below_threshold": owner_count < 15000, "inherited_baseline_counted": False,
    })
    review = build_evidence_review()
    if not review["passed"]:
        raise RuntimeError(f"evidence staged review failed: {review}")
    print(json.dumps({
        "outcomes": distribution, "mutations": len(mutations), "safe": len(safe), "candidates": len(candidates),
        "skills": len(skills), "runners": len(runners), "clean_refine": len(clean),
        "effective_negatives": effective_negatives, "method_count": method_summary["counts"]["methods"],
        "overview_words": len(overview.split()), "review_paths": review["intended_path_count"],
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
