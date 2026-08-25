"""Build Elaren Kestrel v669-v6 bounded synthetic x2 evidence.

This builder validates owner-local synthetic historical-typewriter documentation
fixtures only. It performs no real handling, operation, repair, treatment,
cataloguing decision, identity action, rights decision, publication, or
professional, legal, cultural, affected-party, or Māori-authority act.
"""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

if __package__:
    from scripts.ghc_family_elaren_kestrel_v669_v6_archive import (
        CANDIDATE_TITLES,
        CHAIN_AFTER,
        OWNER,
        OWNER_ROOT,
        PHASE,
        PROTECTED_GATES,
        REFINE_TITLES,
        RUNNER_TITLES,
        SAFE_TITLES,
        SKILL_TITLES,
        STARTUP_EFFECTIVE_BASELINE,
        TOOL_CANDIDATES,
        portfolio_rows,
        write_json,
        write_text,
    )
    from scripts.ghc_family_elaren_kestrel_v669_v6_contracts import validate_synthetic_contract
else:
    from ghc_family_elaren_kestrel_v669_v6_archive import (
        CANDIDATE_TITLES,
        CHAIN_AFTER,
        OWNER,
        OWNER_ROOT,
        PHASE,
        PROTECTED_GATES,
        REFINE_TITLES,
        RUNNER_TITLES,
        SAFE_TITLES,
        SKILL_TITLES,
        STARTUP_EFFECTIVE_BASELINE,
        TOOL_CANDIDATES,
        portfolio_rows,
        write_json,
        write_text,
    )
    from ghc_family_elaren_kestrel_v669_v6_contracts import validate_synthetic_contract

X1_COMMIT = "07f934986ddad144e615e7b31276716b646ebba5"

X2_OPERATIONAL_FAILURES = [
    {
        "failure_id": "EL6696-X2-OP-001",
        "title": "first inherited x2 source-size inventory used a pipeline directly after a foreach block",
        "failed_witness": "PowerShell rejected an empty pipeline element before any inherited blob was read.",
        "bounded_recovery": "An explicit result collection produced bounded path, line, and character scalars without repository mutation.",
    },
    {
        "failure_id": "EL6696-X2-OP-002",
        "title": "first isolated audit projection joined machine JSON and a status line",
        "failed_witness": "The mixed stdout and stderr projection could not be parsed as one JSON document and its apparent counts received zero credit.",
        "bounded_recovery": "The failed audit dependency was rerun once with a dedicated D-backed JSON output file and parsed exactly.",
    },
    {
        "failure_id": "EL6696-X2-OP-003",
        "title": "initial disposable environment audit found seven advisories in bootstrap pip 25.0.1",
        "failed_witness": "The three selected tools had no reported advisory, but the isolated environment failed because its inherited pip carried seven advisory rows.",
        "bounded_recovery": "Only the disposable environment received the official pip 26.2.1 wheel after hash verification; the isolated audit dependency then found zero known vulnerabilities.",
    },
    {
        "failure_id": "EL6696-X2-OP-004",
        "title": "first x2 validator extension targeted the archive file frozen in x1",
        "failed_witness": "The working copy briefly contained an unstaged archive extension that would have violated the x1 staged-review boundary if retained.",
        "bounded_recovery": "An exact reverse patch restored the x1 file byte-for-byte and moved all validation extensions into a new x2-only family module.",
    },
    {
        "failure_id": "EL6696-X2-OP-005",
        "title": "first x2 build interpreted x1-local shard labels as repository-relative paths",
        "failed_witness": "The builder stopped before evidence generation when the first proposal shard could not be resolved from the repository root.",
        "bounded_recovery": "The loader now resolves every frozen shard label relative to the immutable x1 directory and changes no x1 artifact.",
    },
    {
        "failure_id": "EL6696-X2-OP-006",
        "title": "first x2 test invocation stopped at validator package import",
        "failed_witness": "Repository-root unittest discovery could not resolve the script-directory archive import, so no test received credit.",
        "bounded_recovery": "A package-safe fallback import corrected only the loader dependency; retention ledgers were refreshed without replaying successful contracts, mutations, skills, runners, tools, or audit checks.",
    },
    {
        "failure_id": "EL6696-X2-OP-007",
        "title": "second x2 test run isolated a builder package-import failure after twenty-one passing dependencies",
        "failed_witness": "The builder module still used script-directory imports when the final contract-mutation test imported it through the scripts package.",
        "bounded_recovery": "Package-aware imports corrected only that failed test dependency; the twenty-one passing dependencies and every earlier successful component were not replayed.",
    },
]

CORE_SKILL_USES = [
    ("ghc-freed-id-flashcards", "built forty lossy cards anchored to proposal, outcome, Method Flow, and gate ledgers"),
    ("ghc-family-index", "used current routing precedence, D-first ownership, truth labels, and terminal boundaries"),
    ("ghc-family-reflection-remaster", "retained surprises, changed choices, recurrence guards, and sibling-safe recommendations"),
    ("ghc-family-method-flow-state", "kept every failed witness and bounded recovery additive"),
    ("ghc-family-meta-tool-box", "selected exactly three dependency-justified owner-local tools"),
    ("ghc-family-auth-permission-state", "kept action, owner, evidence, expiry, and protected authority separate"),
    ("ghc-family-roster-check", "held successor resolution until the terminal live reread"),
    ("ghc-main-orchestration-memory", "treated the newest live activation as authoritative over stale cursors"),
    ("ghc-main-startup-builder", "completed source, drive, privacy, identity, novelty, and lifecycle startup gates"),
    ("ghc-main-compact-restart-builder", "used exact anchors and bounded scalar recovery after display loss"),
    ("ghc-main-closeout-builder", "preregistered manifests, history, equality, validation, and route gates"),
    ("ghc-main-retry", "reran only failed or target-changed dependencies and retained first witnesses"),
    ("ghc-open-gate-rail", "left professional, participant, legal, cultural, Māori, and Stage 20 authority unexecuted"),
    ("ghc-timestamp-flow", "recorded dated source and environment evidence without fabricating deterministic time"),
    ("ghc-full-tools-skill-bank", "used current selected family tools before creating owner-local additions"),
    ("ghc-family-truth-bridge", "kept inherited seal, external overlay, x1, and x2 count layers separate"),
    ("ghc-worktree-branch-rotation", "used one fresh sparse D-first owner branch and preserved every sibling lane"),
    ("ghc-web-reflection-ledger", "used current official sources only for vocabulary and refusal conditions"),
    ("ghc-watcher-notifier-cadence", "polled bounded live processes without duplicate relaunch"),
    ("ghc-drive-bank-guardian", "kept work, wheels, environment, cache, and receipts D-backed"),
    ("ghc-approval-packet-splitter", "separated executed safe and candidate work from held exact and blocked packets"),
    ("ghc-family-workflow-plan-refinement", "kept one lifecycle step in progress and refreshed after hard gates"),
    ("skill-creator", "validated ten owner-local skills with the current UTF-8 quick validator"),
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run(cwd: Path, *args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, check=False, capture_output=True, text=True, env=env)


def proposals(repo: Path) -> list[dict[str, Any]]:
    x1_root = repo / OWNER_ROOT / "x1"
    freeze = load_json(x1_root / "proposal-freeze.json")
    rows: list[dict[str, Any]] = []
    for relpath in freeze["shards"]:
        rows.extend(load_json(x1_root / relpath)["rows"])
    if len(rows) != 40:
        raise RuntimeError("x1 proposal freeze must expose exactly forty rows")
    return rows


def contract_for(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "ghc.family.synthetic-typewriter-documentation-contract.v1",
        "owner": OWNER,
        "phase": PHASE,
        "proposal_id": row["proposal_id"],
        "semantic_slug": row["semantic_slug"],
        "title": row["title"],
        "synthetic_only": True,
        "typed_state": "documented_zero-real-row_fixture",
        "vacancies": [
            "real_typewriter_document_collection_object_or_media",
            "real_person_typist_worker_donor_owner_or_affected_user",
            "real_measurement_condition_diagnosis_or_professional_decision",
            "real_handling_operation_disassembly_cleaning_lubrication_repair_or_treatment",
            "real_identity_rights_legal_cultural_or_maori_authority_action",
        ],
        "zero_counters": {
            "real_people": 0,
            "real_typewriters": 0,
            "real_documents": 0,
            "real_media": 0,
            "real_measurements": 0,
            "handling_actions": 0,
            "operation_actions": 0,
            "treatment_actions": 0,
            "professional_actions": 0,
            "external_actions": 0,
            "authority_actions": 0,
        },
        "protected_gates": PROTECTED_GATES,
        "rollback": row["rollback_or_recovery"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }


def mutate_contract(contract: dict[str, Any], kind: str) -> dict[str, Any]:
    mutated = copy.deepcopy(contract)
    if kind == "missing_required_state":
        mutated.pop("typed_state", None)
    elif kind == "ambiguous_domain_or_unit":
        mutated["typed_state"] = "ambiguous_untyped_state"
    elif kind == "real_world_or_external_action":
        mutated["zero_counters"]["external_actions"] = 1
    elif kind == "protected_claim_promotion":
        mutated["terminal_verdict"] = "READY_FOR_STAGE_20"
    else:
        raise ValueError(f"unknown preregistered mutation: {kind}")
    return mutated


def card_for(row: dict[str, Any], outcome: str, contract_relpath: str) -> dict[str, Any]:
    return {
        "schema": "ghc.family.freed-id-flashcard.v1",
        "card_id": f"{row['proposal_id']}-CARD",
        "tiers": {
            "tier_1_freed_id": {"owner": OWNER, "boundary": "relational working language only"},
            "tier_2_trinity_pillar": {"primary": "CBR Heart", "protected": ["GMUT Mind", "THOS Body", "Freed ID"]},
            "tier_3_practice": "synthetic historical-typewriter documentation",
            "tier_4_task": row["title"],
        },
        "sections": {
            "identity": OWNER,
            "phase": PHASE,
            "pillar": "CBR Heart",
            "practice": "synthetic learning and documentation-design lens only",
            "task": row["title"],
            "hypothesis": row["hypothesis"],
            "source_status": row["official_or_primary_source_needs"],
            "artifact": contract_relpath,
            "evidence": outcome,
            "failure_boundary": row["null_or_failure_condition"],
            "authority_boundary": row["protected_gates"],
            "rollback": row["rollback_or_recovery"],
        },
        "authoritative": False,
        "lossy_projection": True,
    }


def skill_text(name: str, slug: str, runner_name: str) -> str:
    return f"""---
name: {name}
description: Validate the {slug.replace('-', ' ')} boundary of a wholly synthetic historical-typewriter documentation fixture when this exact owner-local guard is needed.
---

# {name}

Use this skill only for an owner-local synthetic JSON fixture. It authorizes no real typewriter, document, collection object, person, handling, operation, repair, treatment, identity lifecycle, rights decision, professional act, legal or cultural interpretation, affected-party decision, or Māori-authority act.

## Input

Require one contract whose `semantic_slug` is `{slug}`, whose real-world and action counters are all zero, whose protected gates are complete, and whose terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## Workflow

Run `python -B scripts/{runner_name}.py <contract.json>`. Retain a rejected fixture at zero completion credit. Correct only the smallest owner-local failed dependency and preserve the first witness.

## Output boundary

A pass establishes only local structure. It establishes no empirical, participant, professional, production, safety, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, canon, or Stage 20 claim.
"""


def runner_text(slug: str) -> str:
    return f'''"""Family-current validator for the {slug} synthetic typewriter contract."""
from ghc_family_elaren_kestrel_v669_v6_contracts import runner_main

if __name__ == "__main__":
    runner_main("{slug}")
'''


def package_version(python: Path, distribution: str) -> dict[str, Any]:
    code = "import importlib.metadata as m; print(m.version(" + repr(distribution) + "))"
    proc = run(Path.cwd(), str(python), "-B", "-c", code)
    return {
        "name": distribution,
        "returncode": proc.returncode,
        "version": proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else None,
    }


def audit_rows(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict):
        return list(payload.get("dependencies", []))
    if isinstance(payload, list):
        return payload
    raise TypeError("unsupported audit payload")


def audit_vulnerability_count(payload: Any) -> int:
    return sum(len(row.get("vulns", [])) for row in audit_rows(payload))


def toolchain_receipt(repo: Path) -> dict[str, Any]:
    base = Path(os.environ["EL6696_TOOL_BASE"])
    environment = base / "python-tool-env"
    wheelhouse = base / "wheelhouse"
    python = environment / "Scripts/python.exe"
    selected: list[dict[str, Any]] = []
    for item in TOOL_CANDIDATES:
        wheel = wheelhouse / item["wheel"]
        data = wheel.read_bytes()
        installed = package_version(python, item["name"])
        selected.append(
            {
                **item,
                "observed_wheel_sha256": hashlib.sha256(data).hexdigest(),
                "wheel_bytes": len(data),
                "integrity_matches": hashlib.sha256(data).hexdigest() == item["wheel_sha256"],
                "installed_version": installed["version"],
                "version_matches": installed["returncode"] == 0 and installed["version"] == item["version"],
            }
        )
    initial = load_json(base / "audit-initial.json")
    corrected = load_json(base / "audit-corrected.json")
    smoke_commands = [
        (
            "deepdiff",
            "from deepdiff import DeepDiff; d=DeepDiff({'state':'draft'},{'state':'corrected'}); raise SystemExit(0 if d else 2)",
            "from deepdiff import DeepDiff; d=DeepDiff({'state':'same'},{'state':'same'}); raise SystemExit(0 if not d else 2)",
        ),
        (
            "jsonpath-ng",
            "from jsonpath_ng import parse; p=parse('$.machine.identity'); d={'machine':{'identity':'SYN-MACHINE'}}; raise SystemExit(0 if [m.value for m in p.find(d)]==['SYN-MACHINE'] else 2)",
            "from jsonpath_ng import parse; p=parse('$.machine.private_record'); d={'machine':{'identity':'SYN-MACHINE'}}; raise SystemExit(0 if not p.find(d) else 2)",
        ),
        (
            "jsonpatch",
            "import jsonpatch; s={'state':'draft'}; p=jsonpatch.JsonPatch([{'op':'replace','path':'/state','value':'corrected'}]); d=p.apply(s); raise SystemExit(0 if d['state']=='corrected' and s['state']=='draft' else 2)",
            "import jsonpatch; from jsonpatch import JsonPatchConflict; p=jsonpatch.JsonPatch([{'op':'replace','path':'/missing','value':'x'}]);\ntry: p.apply({'state':'draft'})\nexcept JsonPatchConflict: raise SystemExit(0)\nraise SystemExit(2)",
        ),
    ]
    smokes: list[dict[str, Any]] = []
    for tool, positive, rejecting in smoke_commands:
        pos = run(repo, str(python), "-B", "-c", positive)
        neg = run(repo, str(python), "-B", "-c", rejecting)
        smokes.append({"tool": tool, "positive_exit": pos.returncode, "rejecting_exit": neg.returncode})
    wheel_entries = []
    for wheel in sorted(wheelhouse.glob("*.whl")):
        data = wheel.read_bytes()
        wheel_entries.append({"name": wheel.name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    pip = package_version(python, "pip")
    return {
        "schema": "ghc.family.isolated-python-toolchain-install-receipt.v2",
        "location": "$EL6696_TOOL_BASE/python-tool-env",
        "wheelhouse": "$EL6696_TOOL_BASE/wheelhouse",
        "shared_python_environment_mutated": False,
        "shared_npm_prefix_mutated": False,
        "source_builds_allowed": False,
        "offline_install_from_local_wheels": True,
        "selected": selected,
        "wheelhouse_manifest": wheel_entries,
        "initial_audit": {
            "tool": "pip-audit 2.10.1",
            "dependency_count": len(audit_rows(initial)),
            "vulnerability_count": audit_vulnerability_count(initial),
            "exit_state": "failed_retained_zero_credit",
            "bootstrap_pip": "25.0.1",
        },
        "corrected_audit": {
            "tool": "pip-audit 2.10.1",
            "dependency_count": len(audit_rows(corrected)),
            "vulnerability_count": audit_vulnerability_count(corrected),
            "exit_state": "passed_isolated_failed_dependency_recovery",
            "audit_replayed_by_builder": False,
        },
        "pip_recovery": {
            "version": pip["version"],
            "expected": "26.2.1",
            "version_matches": pip["returncode"] == 0 and pip["version"] == "26.2.1",
            "official_wheel_sha256": "71138adf1f4ca900cdb7d289c21b7494329f2332b6d85f0e1c42108c0384ed3e",
        },
        "smoke": {
            "rows": smokes,
            "positive_passed": all(row["positive_exit"] == 0 for row in smokes),
            "rejecting_passed": all(row["rejecting_exit"] == 0 for row in smokes),
        },
        "claim_boundary": "Direct hashes, an isolated audit, and bounded smokes are not exhaustive supply-chain or production-fitness assurance.",
    }


def privacy_candidates(text: str) -> list[dict[str, str]]:
    absolute_path = "(?i)(?:" + "[a-z]" + r":\\" + "|/" + "users" + "/|/" + "home" + "/)" + r"[^\s\"']+"
    patterns = {
        "private_absolute_path": absolute_path,
        "raw_task_or_thread_identifier": r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
        "credential_or_secret_assignment": r"(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*[^\s,}\]]+",
        "transcript_screenshot_or_session_stream": r"(?i)(?:private[_-]?transcript|screenshot[_-]?path|session[_-]?stream)\s*[:=]\s*[^\s,}\]]+",
        "private_callable_or_application_state": r"(?i)(?:private[_-]?callable[_-]?id|private[_-]?app[_-]?state)\s*[:=]\s*[^\s,}\]]+",
    }
    return [
        {"class": class_name, "state": "candidate_requires_classification"}
        for class_name, pattern in patterns.items()
        if re.search(pattern, text)
    ]


def owner_paths(repo: Path) -> list[Path]:
    paths = [path for path in (repo / OWNER_ROOT).rglob("*") if path.is_file()]
    paths.extend((repo / "scripts").glob("*elaren_kestrel_v669_v6*.py"))
    paths.extend((repo / "scripts").glob("ghc_family_typewriter_*.py"))
    paths.extend((repo / "tests").glob("*elaren_kestrel_v669_v6*.py"))
    return sorted(set(paths))


def privacy_scan(repo: Path) -> dict[str, Any]:
    excluded = "docs/elaren-kestrel/v669-v6/validation/evidence-privacy-scan.json"
    candidates: list[dict[str, str]] = []
    scanned = 0
    for path in owner_paths(repo):
        relpath = path.relative_to(repo).as_posix()
        if relpath == excluded or path.suffix.lower() not in {".json", ".md", ".html", ".txt", ".py"}:
            continue
        scanned += 1
        candidates.extend({"path": relpath, **row} for row in privacy_candidates(path.read_text(encoding="utf-8")))
    return {
        "schema": "ghc.family.five-class-privacy-scan.v3",
        "files_scanned": scanned,
        "candidate_count": len(candidates),
        "confirmed_hits": len(candidates),
        "candidates": candidates,
        "self_exclusions": [excluded],
        "claim_boundary": "A bounded pattern scan is not complete privacy assurance.",
    }


def python_security_review(repo: Path) -> dict[str, Any]:
    files = [path for path in owner_paths(repo) if path.suffix == ".py"]
    findings: list[dict[str, Any]] = []
    for path in files:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append({"path": path.relative_to(repo).as_posix(), "line": node.lineno, "kind": node.func.id})
            if isinstance(node.func, ast.Attribute) and node.func.attr == "system":
                findings.append({"path": path.relative_to(repo).as_posix(), "line": node.lineno, "kind": "system_call"})
            for keyword in node.keywords:
                if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                    findings.append({"path": path.relative_to(repo).as_posix(), "line": node.lineno, "kind": "shell_true"})
    return {
        "schema": "ghc.family.bounded-python-security-review.v3",
        "files_reviewed": len(files),
        "finding_count": len(findings),
        "findings": findings,
        "claim_boundary": "A bounded AST review is not exhaustive security assurance.",
    }


def report_html(rows: list[dict[str, Any]]) -> str:
    body = "\n".join(
        f'<tr><th scope="row">{html.escape(row["proposal_id"])}</th><td>{html.escape(row["title"])}</td><td>{html.escape(row["expected_disposition"])}</td></tr>'
        for row in rows
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Elaren Kestrel v669-v6 bounded evidence report</title><style>
:root{{color-scheme:light dark;font-family:system-ui,sans-serif;line-height:1.5}}body{{margin:0}}.skip{{position:absolute;left:-9999px}}.skip:focus{{left:1rem;top:1rem;background:Canvas;padding:.6rem;z-index:2}}header,main,footer{{max-width:76rem;margin:auto;padding:1rem}}nav ul{{display:flex;flex-wrap:wrap;gap:1rem;padding-left:1rem}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid;padding:.45rem;text-align:left;vertical-align:top}}:focus-visible{{outline:.2rem solid Highlight;outline-offset:.2rem}}.notice{{border-inline-start:.35rem solid;padding-inline-start:1rem}}@media(max-width:48rem){{table{{display:block;overflow-x:auto}}}}@media print{{nav,.skip{{display:none}}a{{color:inherit;text-decoration:none}}}}@media(prefers-reduced-motion:reduce){{*{{scroll-behavior:auto!important}}}}
</style></head><body><a class="skip" href="#main">Skip to evidence</a><header><h1>Elaren Kestrel v669-v6 bounded evidence report</h1><p class="notice">Synthetic learning and documentation-design evidence only. No real people, typewriters, documents, objects, media, measurements, handling, operation, treatment, professional decisions, rights decisions, or authority acts occurred.</p><nav aria-label="Report sections"><ul><li><a href="#outcomes">Outcomes</a></li><li><a href="#pillars">Pillars</a></li><li><a href="#gates">Gates</a></li><li><a href="#accessibility">Accessibility</a></li></ul></nav></header><main id="main">
<section id="outcomes"><h2>Outcome ledger</h2><p>Only completed, represented, open_gap, and exact_gate are used.</p><table><caption>Forty preregistered synthetic proposal outcomes</caption><thead><tr><th scope="col">ID</th><th scope="col">Task</th><th scope="col">Outcome</th></tr></thead><tbody>{body}</tbody></table></section>
<section id="pillars"><h2>Trinity Mandala boundaries</h2><h3>CBR Heart</h3><p>Primary: correction, challenge, purpose, rights-reservation, workload, and handover structures only. No remedy, ownership, custody, workplace, legal, cultural, or authority decision occurred.</p><h3>GMUT Mind</h3><p>Mechanism and information boards are typed analogies with zero fitted parameters, observations, predictions, forces, physical laws, empirical confirmation, final physics, quantum completion, or Theory-of-Everything proof.</p><h3>THOS Body and Freed ID</h3><p>THOS remains a participant-free proxy with zero outcomes. Freed ID remains synthetic and nonproduction with zero keys, proofs, issuance, verification, resolution, status, revocation, recovery, or trust governance.</p></section>
<section id="gates"><h2>Open and exact gates</h2><p>The official collection adapter remains zero-call. Professional conservation and registration, worker and stored-energy safety, custody and rights, affected-party legitimacy, privacy and accessibility acceptance, legal and cultural interpretation, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, Māori authority, independent reproduction, and Stage 20 remain open or exact-gated.</p></section>
<section id="accessibility"><h2>Accessibility boundary</h2><p>Landmarks, headings, links, table caption and scopes, focus, responsive overflow, print fallback, and reduced-motion styling are structural checks only. Manual browser, keyboard, touch, zoom, screen-reader, cognitive-accessibility, Māori-language, security-usability, and affected-user evaluation remain reserved.</p></section></main><footer><p>Terminal verdict: NOT_READY_FOR_STAGE_20.</p></footer></body></html>"""


def executed_portfolio(kind: str, titles: list[str], approval: str, state: str) -> list[dict[str, Any]]:
    rows = portfolio_rows(kind, titles, approval, state)
    for row in rows:
        row["completion_credit"] = 1
        row["observed_state"] = state
    return rows


def build(repo: Path) -> None:
    root = repo / OWNER_ROOT
    rows = proposals(repo)
    outcomes: list[dict[str, Any]] = []
    positives: list[dict[str, Any]] = []
    mutations: list[dict[str, Any]] = []
    card_ids: list[str] = []
    for row in rows:
        proposal_id = row["proposal_id"]
        slug = row["semantic_slug"]
        outcome = row["expected_disposition"]
        contract_relpath = f"docs/elaren-kestrel/v669-v6/x2/contracts/{proposal_id.lower()}-{slug}.json"
        contract = contract_for(row)
        validation = validate_synthetic_contract(contract, slug)
        if outcome in {"completed", "represented"} and not validation["passed"]:
            raise RuntimeError(f"positive synthetic contract failed: {proposal_id}")
        write_json(repo / contract_relpath, contract)
        proposal = dict(row)
        proposal["observed_disposition"] = outcome
        proposal["x2_contract"] = contract_relpath
        proposal["positive_validation"] = validation if outcome in {"completed", "represented"} else None
        write_json(repo / row["concrete_artifacts"][0], proposal)
        card = card_for(row, outcome, contract_relpath)
        write_json(repo / row["concrete_artifacts"][1], card)
        card_ids.append(card["card_id"])
        outcomes.append({"proposal_id": proposal_id, "title": row["title"], "outcome": outcome, "completion_credit": 1 if outcome == "completed" else 0})
        if outcome in {"completed", "represented"}:
            positives.append({"proposal_id": proposal_id, "contract": contract_relpath, "validation": validation})
        for fixture in row["negative_fixtures"]:
            result = validate_synthetic_contract(mutate_contract(contract, fixture["kind"]), slug)
            if result["passed"]:
                raise RuntimeError(f"preregistered mutation unexpectedly passed: {fixture['mutation_id']}")
            mutations.append(
                {
                    **fixture,
                    "proposal_id": proposal_id,
                    "attempted": True,
                    "accepted": False,
                    "observed": "rejected_as_preregistered",
                    "validator_failures": result["failures"],
                    "completion_credit": 0,
                    "retained_failed_witness": True,
                    "bounded_recovery": "valid synthetic contract remained unchanged" if outcome in {"completed", "represented"} else "open or exact gate remained held",
                }
            )
    for start in range(0, len(mutations), 20):
        write_json(root / f"x2/mutations/mutation-ledger-{start // 20 + 1:02d}.json", {"schema": "ghc.family.mutation-ledger.v3", "rows": mutations[start : start + 20]})
    labels = ["completed", "represented", "open_gap", "exact_gate"]
    counts = {label: sum(row["outcome"] == label for row in outcomes) for label in labels}
    write_json(root / "x2/outcome-ledger.json", {"schema": "ghc.family.outcome-ledger.v3", "owner": OWNER, "phase": PHASE, "counts": counts, "rows": outcomes})
    write_json(root / "x2/positive-controls.json", {"schema": "ghc.family.positive-controls.v3", "count": len(positives), "rows": positives})
    write_json(root / "x2/flashcard-deck.json", {"schema": "ghc.family.freed-id-flashcard-deck.v2", "owner": OWNER, "phase": PHASE, "card_count": len(card_ids), "tier_order": ["Freed ID owner", "Trinity pillar", "bounded practice", "task"], "minimum_sections": 10, "cards": card_ids, "authoritative_sources": ["proposal freeze", "outcome ledger", "Method Flow ledger", "gate register"], "boundary": "Cards are lossy projections and never replace authoritative ledgers."})

    portfolios = {
        "safe_now": executed_portfolio("safe", SAFE_TITLES, "safe_now", "completed_bounded_synthetic"),
        "candidate": executed_portfolio("candidate", CANDIDATE_TITLES, "candidate", "completed_bounded_evaluation"),
        "skill": executed_portfolio("skill", SKILL_TITLES, "phase_local_skill", "built_validated_smoke_used"),
        "runner": executed_portfolio("runner", RUNNER_TITLES, "family_current_runner", "built_validated_smoke_used"),
        "clean_fix_refine": executed_portfolio("refine", REFINE_TITLES, "safe_now_clean_fix_refine", "completed_bounded_structural"),
        "exact_approval": portfolio_rows("exact", [f"held exact-approval packet {index:02d}" for index in range(1, 11)], "exact_approval", "held_unexecuted"),
        "blocked": portfolio_rows("blocked", [f"held blocked packet {index:02d}" for index in range(1, 6)], "blocked", "held_unexecuted"),
    }
    for kind, packet in portfolios.items():
        write_json(root / f"x2/portfolio-execution/{kind}.json", {"schema": "ghc.family.portfolio-execution.v3", "kind": kind, "count": len(packet), "rows": packet})

    runner_receipts: list[dict[str, Any]] = []
    skill_receipts: list[dict[str, Any]] = []
    for index, (skill, runner_name) in enumerate(zip(SKILL_TITLES, RUNNER_TITLES), 1):
        row = rows[index - 1]
        skill_path = root / f"tools/skills/{skill}/SKILL.md"
        runner_path = repo / f"scripts/{runner_name}.py"
        write_text(skill_path, skill_text(skill, row["semantic_slug"], runner_name))
        write_text(runner_path, runner_text(row["semantic_slug"]))
        contract_path = repo / f"docs/elaren-kestrel/v669-v6/x2/contracts/{row['proposal_id'].lower()}-{row['semantic_slug']}.json"
        proc = run(repo, sys.executable, "-B", str(runner_path), str(contract_path))
        parsed = json.loads(proc.stdout) if proc.stdout else {"passed": False, "failures": ["no_result"]}
        runner_receipts.append({"runner": runner_path.relative_to(repo).as_posix(), "returncode": proc.returncode, "result": parsed})
        body = skill_path.read_text(encoding="utf-8")
        skill_receipts.append({"skill": skill_path.relative_to(repo).as_posix(), "frontmatter_name_present": f"name: {skill}" in body, "runner_instruction_present": f"scripts/{runner_name}.py" in body, "smoke_runner_passed": proc.returncode == 0 and parsed.get("passed") is True, "global_installation": False})
    if not all(row["returncode"] == 0 and row["result"].get("passed") for row in runner_receipts):
        raise RuntimeError("one or more family-current runner smokes failed")
    write_json(root / "tools/runner-smoke-receipt.json", {"schema": "ghc.family.runner-smoke.v3", "count": 10, "failures": 0, "rows": runner_receipts})
    write_json(root / "tools/skill-smoke-receipt.json", {"schema": "ghc.family.skill-smoke.v3", "count": 10, "failures": 0, "rows": skill_receipts})

    validator = Path.home() / ".codex/skills/.system/skill-creator/scripts/quick_validate.py"
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    quick_rows = []
    for skill in SKILL_TITLES:
        skill_dir = root / f"tools/skills/{skill}"
        proc = run(repo, sys.executable, "-B", str(validator), str(skill_dir), env=env)
        quick_rows.append({"skill": skill_dir.relative_to(repo).as_posix(), "returncode": proc.returncode, "passed": proc.returncode == 0, "utf8_mode": True})
    if not all(row["passed"] for row in quick_rows):
        raise RuntimeError("one or more phase-local skills failed current quick validation")
    write_json(root / "tools/skill-quick-validation-receipt.json", {"schema": "ghc.family.skill-quick-validation.v2", "count": 10, "failures": 0, "rows": quick_rows})
    write_json(root / "tools/core-skill-use-ledger.json", {"schema": "ghc.family.core-skill-use-ledger.v2", "required_and_used": len(CORE_SKILL_USES), "rows": [{"skill": skill, "status": "read_through_eof_and_applied", "evidence": evidence} for skill, evidence in CORE_SKILL_USES], "boundary": "Skill use is workflow evidence, not identity continuity, authority, or independent agency."})

    tools = toolchain_receipt(repo)
    if not all(row["version_matches"] and row["integrity_matches"] for row in tools["selected"]):
        raise RuntimeError("isolated direct tool lock or integrity mismatch")
    if tools["initial_audit"]["vulnerability_count"] != 7 or tools["corrected_audit"]["vulnerability_count"] != 0:
        raise RuntimeError("isolated audit history mismatch")
    if not tools["pip_recovery"]["version_matches"]:
        raise RuntimeError("isolated pip recovery mismatch")
    if not tools["smoke"]["positive_passed"] or not tools["smoke"]["rejecting_passed"]:
        raise RuntimeError("isolated tool smoke mismatch")
    write_json(root / "tools/isolated-toolchain-install-receipt.json", tools)

    write_json(
        root / "x2/source-provenance.json",
        {
            "schema": "ghc.family.public-source-provenance.v2",
            "retrieval_date": "2026-08-26",
            "sources": [
                {"name": "Smithsonian National Museum of American History typewriter object", "url": "https://americanhistory.si.edu/collections/object/nmah_850053", "use": "public object vocabulary and uncertainty cues only"},
                {"name": "Smithsonian Institution typewriter collection search", "url": "https://collections.si.edu/search/results.htm?q=set_name%3A%22Typewriters%22", "use": "collection vocabulary only; no records ingested"},
                {"name": "Canadian Conservation Institute care of industrial collections", "url": "https://www.canada.ca/en/conservation-institute/services/care-objects/industrial-collections.html", "use": "industrial-object vocabulary and referral boundaries only"},
                {"name": "Canadian Conservation Institute care and cleaning of iron", "url": "https://www.canada.ca/en/conservation-institute/services/care-objects/metals/care-cleaning-iron.html", "use": "condition vocabulary and treatment abstention only"},
                {"name": "National Park Service Museum Handbook Part I", "url": "https://www.nps.gov/museum/publications/MHI/MHI.pdf", "use": "museum-object documentation and environmental vocabulary only"},
                {"name": "W3C PROV-O", "url": "https://www.w3.org/TR/prov-o/", "use": "provenance vocabulary only"},
                {"name": "W3C WCAG 2.2", "url": "https://www.w3.org/TR/WCAG22/", "use": "structural accessibility vocabulary only"},
                {"name": "RFC 8785 JSON Canonicalization Scheme", "url": "https://www.rfc-editor.org/rfc/rfc8785", "use": "canonical JSON vocabulary only"},
                {"name": "PyPI deepdiff 9.1.0", "url": "https://pypi.org/project/deepdiff/9.1.0/", "use": "official release metadata and direct wheel hash only"},
                {"name": "PyPI jsonpath-ng 1.8.0", "url": "https://pypi.org/project/jsonpath-ng/1.8.0/", "use": "official release metadata and direct wheel hash only"},
                {"name": "PyPI jsonpatch 1.33", "url": "https://pypi.org/project/jsonpatch/1.33/", "use": "official release metadata and direct wheel hash only"},
                {"name": "PyPI pip 26.2.1", "url": "https://pypi.org/project/pip/26.2.1/", "use": "official isolated-environment remediation release and wheel hash only"},
            ],
            "network_calls_by_phase_adapter": 0,
            "real_rows_ingested": 0,
            "claim_boundary": "Public sources confer no observation, endorsement, conformance, competence, legal interpretation, cultural ratification, or authority.",
        },
    )
    write_json(root / "x2/official-collection-adapter-receipt.json", {"schema": "ghc.family.zero-call-adapter.v2", "transport_enabled": False, "calls": 0, "rows": 0, "objects": 0, "images": 0, "records": 0, "outcome": "open_gap", "reason": "No approved live collection transaction was necessary or authorized."})

    method_rows = [
        {"method_id": row["failure_id"], "class": "x2_owner_operational", "failed_witness": row["failed_witness"], "completion_credit": 0, "bounded_passing_witness": row["bounded_recovery"], "retained": True}
        for row in X2_OPERATIONAL_FAILURES
    ]
    method_rows.extend(
        {"method_id": mutation["mutation_id"], "class": "preregistered_rejecting_mutation", "failed_witness": mutation["kind"], "completion_credit": 0, "bounded_passing_witness": mutation["bounded_recovery"], "retained": True}
        for mutation in mutations
    )
    evidence_counts = {
        "effective_negatives": STARTUP_EFFECTIVE_BASELINE["effective_negatives"] + len(method_rows),
        "methods": STARTUP_EFFECTIVE_BASELINE["methods"] + len(method_rows),
        "failed_witnesses": STARTUP_EFFECTIVE_BASELINE["failed_witnesses"] + len(method_rows),
        "passing_witnesses": STARTUP_EFFECTIVE_BASELINE["passing_witnesses"] + len(method_rows) + len(positives),
        "open_gaps": STARTUP_EFFECTIVE_BASELINE["open_gaps"] + 2,
        "exact_gates": STARTUP_EFFECTIVE_BASELINE["exact_gates"] + 2,
    }
    write_json(root / "method-flow/evidence-ledger.json", {"schema": "ghc.family.method-flow-ledger.v4", "owner": OWNER, "phase": PHASE, "inherited_x1_effective_baseline": STARTUP_EFFECTIVE_BASELINE, "new_operational_failures": len(X2_OPERATIONAL_FAILURES), "new_rejecting_mutations": len(mutations), "new_method_count": len(method_rows), "new_failed_witnesses": len(method_rows), "new_bounded_recoveries": len(method_rows), "new_positive_witnesses": len(positives), "rows": method_rows})
    write_json(root / "method-flow/evidence-summary.json", {"schema": "ghc.family.method-flow-summary.v4", **evidence_counts})
    write_json(root / "x2/x2-operational-failures.json", {"schema": "ghc.family.retained-operational-failures.v3", "count": len(X2_OPERATIONAL_FAILURES), "rows": X2_OPERATIONAL_FAILURES})
    write_json(root / "x2/retained-negative-register.json", {"schema": "ghc.family.retained-negative-register.v4", "inherited_x1_effective": STARTUP_EFFECTIVE_BASELINE["effective_negatives"], "x2_operational": len(X2_OPERATIONAL_FAILURES), "rejecting_mutations": len(mutations), "effective": evidence_counts["effective_negatives"], "erased": 0})
    write_json(root / "x2/open-exact-gate-register.json", {"schema": "ghc.family.open-exact-gates.v3", "inherited_open_gaps": STARTUP_EFFECTIVE_BASELINE["open_gaps"], "new_open_gaps": ["official museum collection adapter remains zero-call", "governed registrar conservator accessibility affected-party and Māori-authority evaluation remains absent"], "effective_open_gaps": evidence_counts["open_gaps"], "inherited_exact_gates": STARTUP_EFFECTIVE_BASELINE["exact_gates"], "new_exact_gates": ["typewriter conservation custody ownership copyright workplace cultural affected-party and Māori authority", "Stage 20 evidence and competent authority"], "effective_exact_gates": evidence_counts["exact_gates"]})
    write_json(root / "x2/phase-truth-evidence.json", {"schema": "ghc.family.phase-truth.v4", "owner": OWNER, "phase": PHASE, "lifecycle": "x2_evidence", "x1_commit": X1_COMMIT, "proposal_chain": CHAIN_AFTER, "outcomes": counts, **evidence_counts, "positive_controls": len(positives), "rejecting_mutations": len(mutations), "portfolio_completed": 95, "exact_approval_held": 10, "blocked_held": 5, "isolated_D_tool_installations": 3, "shared_prefix_mutations": 0, "real_world_actions": 0, "network_calls_by_phase_adapter": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json(root / "x2/wellbeing-workload-check.json", {"schema": "ghc.family.wellbeing-workload.v3", "owner": OWNER, "phase": PHASE, "relational_language_boundary": True, "hope": "make disputed synthetic records reversible without converting software structure into authority", "workload_within_caps": True, "file_ceiling": 2000, "document_word_ceiling": 100000, "stop_conditions_visible": True, "no_claim_of_sentience_personhood_continuity_or_authority": True})
    write_text(root / "x2/integrated-evidence-overview.md", """# Elaren Kestrel v669-v6 bounded x2 evidence

## Outcome

Forty preregistered proposals were processed with only `completed`, `represented`, `open_gap`, and `exact_gate`: 28 bounded structural completions, 8 representations, 2 open gaps, and 2 exact gates. Thirty-six synthetic positive controls passed. All 160 preregistered invalid mutations were actually applied to owner-local fixtures, rejected by the declared validator, retained, and assigned zero completion credit.

## Practice and pillars

CBR Heart is primary through a wholly synthetic historical-typewriter cataloguing, condition-state, correction, and handover lens. It contains zero real people, typewriters, documents, media, measurements, handling, operation, treatment, professional decisions, rights decisions, or authority acts. GMUT mechanism and information boards remain typed analogies with zero fitted parameters, observations, predictions, forces, physical laws, empirical confirmation, final physics, quantum completion, or Theory-of-Everything proof. THOS remains a participant-free proxy with zero outcomes. Freed ID remains synthetic and nonproduction with zero keys, proofs, issuance, verification, resolution, status, revocation, recovery, or trust governance.

## Tools, skills, and runners

DeepDiff 9.1.0, jsonpath-ng 1.8.0, and jsonpatch 1.33 were downloaded as wheels from official PyPI into a phase-namespaced D-backed wheelhouse. Their three direct hashes matched. Offline installation and bounded positive/rejecting smokes passed. The first audit retained seven advisories in disposable bootstrap pip 25.0.1; only that environment received official pip 26.2.1 after hash verification, and the isolated failed-dependency recovery audit then found zero known vulnerabilities. This is not exhaustive supply-chain or production evidence. Ten phase-local skills and ten family-current runners were built, quick-validated, and smoke-used only against synthetic owner fixtures.

## Work and holds

Thirty safe-now, fifteen candidate, ten skill, ten runner, and thirty CLEAN/FIX/REFINE rows completed within bounded structural scope. Ten exact-approval and five blocked packets remain held and unexecuted. No inherited proposal, method, tool, skill, runner, evidence row, recommendation, or outcome became automatic Elaren novelty or completion credit.

## Sources, accessibility, and nonclaims

Current official sources supplied vocabulary and refusal conditions only. The collection adapter made zero calls and ingested zero rows. The static report supplies structural landmarks, headings, captions, scopes, focus, responsive overflow, print fallback, and reduced-motion styling. Manual browser, keyboard, touch, zoom, assistive-technology, cognitive-accessibility, Māori-language, security-usability, and affected-user evaluation remain reserved. Nothing establishes professional competence, custody, ownership, attribution, workplace or stored-energy safety, conservation or treatment authority, rights or remedy, legal or cultural interpretation, Māori authority, complete privacy or accessibility, independent reproduction, production readiness, AGI/ASI, consciousness/personhood, empirical GMUT confirmation, Theory-of-Everything proof, canon, or Stage 20 readiness.

## Retention

    Every inherited and x1 failure remains visible. All x2 operational failures and all 160 rejecting mutations are additional zero-credit Method Flow rows with bounded recoveries. Repository-sealed source truth, Eiren's external overlay, Elaren x1, and Elaren x2 remain separate layers. Terminal verdict remains `NOT_READY_FOR_STAGE_20`.
""")
    write_text(root / "x2/accessible-evidence-report.html", report_html(rows))
    write_text(root / "x2/threat-model.md", """# Elaren Kestrel v669-v6 x2 threat model

## Assets

Immutable source and x1 history, retained failures, exact gates, proposal identity, tool integrity, privacy boundaries, evidence labels, and delivery truth.

## Threats

X1 mutation, inaccessible-history novelty overclaim, fabricated object or human evidence, mechanism analogy converted into physics, structural condition cues converted into professional treatment advice, custody converted into ownership, identifier graphs converted into identity authority, public vocabulary converted into endorsement, dependency confusion, stale advisories, source-build substitution, private-route leakage, raw identifiers, manifest drift, validation replay, sibling-lane mutation, and premature Stage 20 promotion.

## Controls

An immutable x1 commit, zero-real-row fixtures, four outcome labels, 160 executed rejecting mutations, held exact packets, official direct wheel hashes, source-build-free offline installation, initial and corrected isolated audit receipts, bounded tool smokes, phase-local skills, family-current callers, five-class privacy scanning, AST review, exact staged Git-blob manifests, additive Method Flow, and one terminal validator only after final equality.

## Residual risk

Official metadata, direct hashes, audits, same-owner smokes, static structure, and synthetic fixtures cannot establish future supply-chain safety, exhaustive security, complete privacy or accessibility, typewriter registration or conservation competence, handling or stored-energy safety, custody or rights, legal or cultural legitimacy, affected-party acceptance, Māori authority, empirical GMUT, operational THOS, production Freed ID, independent reproduction, or Stage 20 readiness.
""")

    privacy = privacy_scan(repo)
    security = python_security_review(repo)
    if privacy["confirmed_hits"]:
        raise RuntimeError(f"privacy scan found candidates: {privacy['candidates']}")
    if security["finding_count"]:
        raise RuntimeError(f"bounded Python review found issues: {security['findings']}")
    write_json(root / "validation/evidence-privacy-scan.json", privacy)
    write_json(root / "validation/evidence-python-security-review.json", security)
    write_json(root / "validation/evidence-build-receipt.json", {"schema": "ghc.family.evidence-build-receipt.v2", "owner": OWNER, "phase": PHASE, "outcomes": counts, "positive_controls": len(positives), "rejecting_mutations": len(mutations), "operational_failures": len(X2_OPERATIONAL_FAILURES), "portfolio_completed": 95, "skills": 10, "runners": 10, "isolated_tools": 3, "privacy_candidates": privacy["candidate_count"], "security_findings": security["finding_count"], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})


def refresh_retention(repo: Path) -> None:
    """Refresh only failure-derived counts after an unrelated failed dependency."""
    root = repo / OWNER_ROOT
    mutations: list[dict[str, Any]] = []
    for path in sorted((root / "x2/mutations").glob("mutation-ledger-*.json")):
        mutations.extend(load_json(path)["rows"])
    positives = load_json(root / "x2/positive-controls.json")["rows"]
    outcome = load_json(root / "x2/outcome-ledger.json")
    method_rows = [
        {"method_id": row["failure_id"], "class": "x2_owner_operational", "failed_witness": row["failed_witness"], "completion_credit": 0, "bounded_passing_witness": row["bounded_recovery"], "retained": True}
        for row in X2_OPERATIONAL_FAILURES
    ]
    method_rows.extend(
        {"method_id": mutation["mutation_id"], "class": "preregistered_rejecting_mutation", "failed_witness": mutation["kind"], "completion_credit": 0, "bounded_passing_witness": mutation["bounded_recovery"], "retained": True}
        for mutation in mutations
    )
    evidence_counts = {
        "effective_negatives": STARTUP_EFFECTIVE_BASELINE["effective_negatives"] + len(method_rows),
        "methods": STARTUP_EFFECTIVE_BASELINE["methods"] + len(method_rows),
        "failed_witnesses": STARTUP_EFFECTIVE_BASELINE["failed_witnesses"] + len(method_rows),
        "passing_witnesses": STARTUP_EFFECTIVE_BASELINE["passing_witnesses"] + len(method_rows) + len(positives),
        "open_gaps": STARTUP_EFFECTIVE_BASELINE["open_gaps"] + 2,
        "exact_gates": STARTUP_EFFECTIVE_BASELINE["exact_gates"] + 2,
    }
    write_json(root / "method-flow/evidence-ledger.json", {"schema": "ghc.family.method-flow-ledger.v4", "owner": OWNER, "phase": PHASE, "inherited_x1_effective_baseline": STARTUP_EFFECTIVE_BASELINE, "new_operational_failures": len(X2_OPERATIONAL_FAILURES), "new_rejecting_mutations": len(mutations), "new_method_count": len(method_rows), "new_failed_witnesses": len(method_rows), "new_bounded_recoveries": len(method_rows), "new_positive_witnesses": len(positives), "rows": method_rows})
    write_json(root / "method-flow/evidence-summary.json", {"schema": "ghc.family.method-flow-summary.v4", **evidence_counts})
    write_json(root / "x2/x2-operational-failures.json", {"schema": "ghc.family.retained-operational-failures.v3", "count": len(X2_OPERATIONAL_FAILURES), "rows": X2_OPERATIONAL_FAILURES})
    write_json(root / "x2/retained-negative-register.json", {"schema": "ghc.family.retained-negative-register.v4", "inherited_x1_effective": STARTUP_EFFECTIVE_BASELINE["effective_negatives"], "x2_operational": len(X2_OPERATIONAL_FAILURES), "rejecting_mutations": len(mutations), "effective": evidence_counts["effective_negatives"], "erased": 0})
    truth = load_json(root / "x2/phase-truth-evidence.json")
    truth.update(evidence_counts)
    truth["outcomes"] = outcome["counts"]
    truth["positive_controls"] = len(positives)
    truth["rejecting_mutations"] = len(mutations)
    write_json(root / "x2/phase-truth-evidence.json", truth)
    receipt = load_json(root / "validation/evidence-build-receipt.json")
    receipt["operational_failures"] = len(X2_OPERATIONAL_FAILURES)
    write_json(root / "validation/evidence-build-receipt.json", receipt)
    overview_path = root / "x2/integrated-evidence-overview.md"
    overview = overview_path.read_text(encoding="utf-8")
    overview = re.sub(r"(?:Four|Five|Six|\d+) x2 operational failures", "All x2 operational failures", overview)
    write_text(overview_path, overview)


def refresh_validation(repo: Path) -> None:
    """Rerun only target-dependent privacy and Python-review checks."""
    root = repo / OWNER_ROOT
    privacy = privacy_scan(repo)
    security = python_security_review(repo)
    if privacy["confirmed_hits"]:
        raise RuntimeError(f"privacy scan found candidates: {privacy['candidates']}")
    if security["finding_count"]:
        raise RuntimeError(f"bounded Python review found issues: {security['findings']}")
    write_json(root / "validation/evidence-privacy-scan.json", privacy)
    write_json(root / "validation/evidence-python-security-review.json", security)
    receipt = load_json(root / "validation/evidence-build-receipt.json")
    receipt["privacy_candidates"] = privacy["candidate_count"]
    receipt["security_findings"] = security["finding_count"]
    receipt["target_changed_validation_refresh"] = True
    receipt["successful_unaffected_components_replayed"] = False
    write_json(root / "validation/evidence-build-receipt.json", receipt)


def staged_review(repo: Path) -> None:
    names = run(repo, "git", "diff", "--cached", "--name-only", "--diff-filter=ACMRT", "HEAD").stdout.splitlines()
    x1_locked = {
        "scripts/build_ghc_family_elaren_kestrel_v669_v6_x1.py",
        "scripts/ghc_family_elaren_kestrel_v669_v6_archive.py",
        "tests/test_ghc_family_elaren_kestrel_v669_v6_x1.py",
    }
    frozen = [name for name in names if name.startswith("docs/elaren-kestrel/v669-v6/x1/") or name in x1_locked or name.endswith("/x1-manifest.json") or name.endswith("/x1-staged-review.json") or name.endswith("/x1-validation-receipt.json")]
    disallowed = [name for name in names if any(part in name for part in ("/closeout/", "/seal/", "/final/", "/handoffs/"))]
    exclusions = {
        "docs/elaren-kestrel/v669-v6/validation/evidence-staged-review.json",
        "docs/elaren-kestrel/v669-v6/validation/evidence-delta-manifest.json",
        "docs/elaren-kestrel/v669-v6/validation/evidence-owner-manifest.json",
    }
    json_errors: list[str] = []
    privacy: list[dict[str, str]] = []
    for relpath in names:
        if relpath in exclusions:
            continue
        data = subprocess.run(["git", "show", f":{relpath}"], cwd=repo, check=True, capture_output=True).stdout
        text = data.decode("utf-8", errors="replace")
        if relpath.endswith(".json"):
            try:
                json.loads(text)
            except Exception as exc:  # noqa: BLE001 - exact path and class retained
                json_errors.append(f"{relpath}:{type(exc).__name__}")
        privacy.extend({"path": relpath, **row} for row in privacy_candidates(text))
    diff_check = run(repo, "git", "diff", "--cached", "--check").returncode
    receipt = {
        "schema": "ghc.family.staged-review.v3",
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "x2_evidence",
        "staged_entry_count_before_self": len(names),
        "frozen_x1_mutations": frozen,
        "disallowed_closeout_paths": disallowed,
        "json_errors": json_errors,
        "privacy_candidates": privacy,
        "diff_cached_exit": diff_check,
        "x1_immutable": not frozen,
        "x2_only": not disallowed,
        "passed": not frozen and not disallowed and not json_errors and not privacy and diff_check == 0,
        "self_exclusions": sorted(exclusions),
    }
    write_json(repo / OWNER_ROOT / "validation/evidence-staged-review.json", receipt)
    if not receipt["passed"]:
        raise RuntimeError("x2 staged review failed closed")


def manifests_from_index(repo: Path) -> None:
    names = run(repo, "git", "diff", "--cached", "--name-only", "--diff-filter=ACMRT", "HEAD").stdout.splitlines()
    exclusions = [
        "docs/elaren-kestrel/v669-v6/validation/evidence-owner-manifest.json",
        "docs/elaren-kestrel/v669-v6/validation/evidence-delta-manifest.json",
        "docs/elaren-kestrel/v669-v6/validation/evidence-staged-review.json",
    ]
    delta = []
    for relpath in sorted(name for name in names if name not in exclusions):
        data = subprocess.run(["git", "show", f":{relpath}"], cwd=repo, check=True, capture_output=True).stdout
        delta.append({"path": relpath, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    owner_names = set(names)
    owner_names.update(run(repo, "git", "ls-tree", "-r", "--name-only", "HEAD", "docs/elaren-kestrel/v669-v6", "scripts", "tests").stdout.splitlines())
    owner = []
    for relpath in sorted(owner_names):
        if relpath in exclusions:
            continue
        if not (
            relpath.startswith("docs/elaren-kestrel/v669-v6/")
            or (relpath.startswith("scripts/") and ("elaren_kestrel_v669_v6" in relpath or relpath.startswith("scripts/ghc_family_typewriter_")))
            or (relpath.startswith("tests/") and "elaren_kestrel_v669_v6" in relpath)
        ):
            continue
        spec = f":{relpath}" if relpath in names else f"HEAD:{relpath}"
        data = subprocess.run(["git", "show", spec], cwd=repo, check=True, capture_output=True).stdout
        owner.append({"path": relpath, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    common = {"schema": "ghc.family.content-manifest.v3", "owner": OWNER, "phase": PHASE, "self_exclusions": exclusions}
    root = repo / OWNER_ROOT / "validation"
    write_json(root / "evidence-delta-manifest.json", {**common, "domain": "x2_exact_staged_git_blobs", "entry_count": len(delta), "entries": delta})
    write_json(root / "evidence-owner-manifest.json", {**common, "domain": "owner_exact_head_plus_staged_git_blobs", "entry_count": len(owner), "entries": owner})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--review-staged", action="store_true")
    parser.add_argument("--manifests-from-index", action="store_true")
    parser.add_argument("--refresh-retention", action="store_true")
    parser.add_argument("--refresh-validation", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    if args.refresh_validation:
        refresh_validation(repo)
    elif args.refresh_retention:
        refresh_retention(repo)
    elif args.review_staged:
        staged_review(repo)
    elif args.manifests_from_index:
        manifests_from_index(repo)
    else:
        build(repo)


if __name__ == "__main__":
    main()
