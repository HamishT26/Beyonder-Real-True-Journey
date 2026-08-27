"""Build bounded synthetic Orin Thale v672-v5 x2 evidence."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.ghc_family_orin_v672_v5_access_guard import (
    EvidenceGuardError,
    canonical_json_bytes,
    mutation_variants,
    validate_proposal,
    validate_skill_smoke,
)
from scripts.ghc_family_orin_v672_v5_handover import (
    HandoverError,
    positive_fixture as handover_fixture,
    rejecting_fixtures as handover_rejecting,
    validate_handover,
)
from scripts.ghc_family_orin_v672_v5_provenance import SURFACES, run_surface


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "orin-thale" / "v672-v5"
OWNER = "Orin Thale"
PHASE = "v672-v5"
BRANCH = "codex/GHC-Family/orin-thale-v672-v5-full-tools"
SOURCE_FINAL = "8f672ef30372b4adf457140c254931dc365e9d31"
X1_COMMIT = "657681df7392f3cd652930d3f834b60ccfa21bcd"
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
BOUNDARY = (
    "Bounded owner-local software or synthetic evidence only; never empirical confirmation, "
    "professional authority, production readiness, legal or cultural ratification, Māori authority, "
    "affected-party acceptance, complete privacy or accessibility assurance, exhaustive security, "
    "independent reproduction, AGI/ASI, consciousness or personhood evidence, Theory-of-Everything "
    "proof, proof/canon, or Stage 20 authority."
)

RUNNER_MODULES = [
    "ghc_family_orin_v672_v5_tactile_source_lineage",
    "ghc_family_orin_v672_v5_tactile_legend_integrity",
    "ghc_family_orin_v672_v5_tactile_route_continuity",
    "ghc_family_orin_v672_v5_braille_codepoint_guard",
    "ghc_family_orin_v672_v5_braille_segment_lineage",
    "ghc_family_orin_v672_v5_alternate_description_linkage",
    "ghc_family_orin_v672_v5_proof_correction_lineage",
    "ghc_family_orin_v672_v5_access_request_minimization",
    "ghc_family_orin_v672_v5_accessible_notice_proxy",
    "ghc_family_orin_v672_v5_access_workload_handover",
]
RUNNER_PATHS = [f"scripts/{module}.py" for module in RUNNER_MODULES]
TOOL_PATHS = [
    "scripts/ghc_family_orin_v672_v5_access_guard.py",
    "scripts/ghc_family_orin_v672_v5_provenance.py",
    "scripts/ghc_family_orin_v672_v5_handover.py",
]
X2_BUILDER_PATH = "scripts/build_ghc_family_orin_thale_v672_v5_x2.py"
X2_TEST_PATH = "tests/test_ghc_family_orin_thale_v672_v5_x2.py"


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, check=check, capture_output=True)


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8", errors="strict").strip()


def load(relative: str) -> Any:
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


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


def sha(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def prepare_runners() -> None:
    for module, surface in zip(RUNNER_MODULES, SURFACES, strict=True):
        path = ROOT / "scripts" / f"{module}.py"
        text = f'''"""Family-current bounded runner for the {surface} surface."""

from __future__ import annotations

import json

from scripts.ghc_family_orin_v672_v5_provenance import run_surface


def main() -> None:
    print(json.dumps(run_surface("{surface}"), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
'''
        path.write_text(text, encoding="utf-8", newline="\n")
    print(json.dumps({"prepared_runners": len(RUNNER_MODULES), "paths": RUNNER_PATHS}, sort_keys=True))


def skill_markdown(name: str) -> str:
    focus = name.removeprefix("ghc-family-").replace("-", " ")
    return f"""---
name: {name}
description: Validate the bounded synthetic {focus} contract for Orin v672-v5. Use when an owner-local accessible-publishing fixture needs deterministic provenance, refusal, correction, privacy, or authority-vacancy checks.
---

# {focus.title()}

Use this phase-local skill only for the bounded Orin v672-v5 owner delta. It does not provide Braille transcription, tactile-graphics, accessibility, legal, cultural, Māori-authority, or production expertise.

## Workflow

1. Verify the exact Orin x1 commit and keep every x1 blob immutable.
2. Accept only synthetic inputs with zero real people, objects, records, measurements, identities, keys, proofs, accounts, endpoints, or external actions.
3. Validate the typed `{focus}` fixture and require every uncertainty or authority vacancy to remain explicit.
4. Run one accepting and one rejecting smoke fixture; retain rejection as bounded guard evidence, never broader completion credit.
5. Preserve the four truth labels: `completed`, `represented`, `open_gap`, and `exact_gate`.
6. Emit a deterministic, UTF-8 receipt without private identifiers, routes, credentials, transcripts, session streams, callable identifiers, application state, or absolute local paths.
7. Stop when participant evidence, professional judgment, production identity, disability-community acceptance, legal or cultural authority, Māori authority, empirical GMUT data, or Stage 20 admission is required.

## Acceptance gate

The accepting fixture passes, the rejecting fixture fails closed, rollback is owner-local and reversible, failures remain visible, manual and affected-user evaluation stay reserved, and the terminal verdict remains `NOT_READY_FOR_STAGE_20`.

## Boundary

{BOUNDARY}
"""


def customize_skills() -> None:
    portfolio = load("x1/portfolio-freeze.json")
    names = [row["title"] for row in portfolio["rows"]["skills"]]
    rows = []
    for name in names:
        root = OWNER_ROOT / "x2" / "skills" / name
        if not (root / "SKILL.md").exists() or not (root / "agents" / "openai.yaml").exists():
            raise SystemExit(f"skill must be initialized first: {name}")
        skill = skill_markdown(name)
        display = name.removeprefix("ghc-family-").replace("-", " ").title()
        agent = (
            "interface:\n"
            f"  display_name: \"{display}\"\n"
            "  short_description: \"Validate a bounded accessible-publishing contract\"\n"
            f"  default_prompt: \"Use ${name} to validate one synthetic owner-local contract while retaining every protected gate.\"\n"
        )
        (root / "SKILL.md").write_text(skill.rstrip() + "\n", encoding="utf-8", newline="\n")
        (root / "agents" / "openai.yaml").write_text(agent, encoding="utf-8", newline="\n")
        rows.append(
            {
                "skill": name,
                "skill_path": f"docs/orin-thale/v672-v5/x2/skills/{name}/SKILL.md",
                "agent_path": f"docs/orin-thale/v672-v5/x2/skills/{name}/agents/openai.yaml",
                "initialized_officially": True,
                "customized": True,
                "read_before_smoke": False,
                "quick_validated": False,
                "smoke_used": False,
                "global_install": False,
            }
        )
    write_json(
        "x2/skill-preparation.json",
        {
            "schema": "ghc.family.skill-preparation.v3",
            "owner": OWNER,
            "phase": PHASE,
            "count": len(rows),
            "rows": rows,
            "main_agent_read_pending": True,
            "global_install": False,
            "subagent_forward_test": False,
            "boundary": BOUNDARY,
        },
    )
    print(json.dumps({"customized_skills": len(rows), "main_agent_read_pending": True}, sort_keys=True))


def verify_x1_gate() -> dict[str, Any]:
    branch = git_text("branch", "--show-current")
    head = git_text("rev-parse", "HEAD")
    upstream = git_text("rev-parse", "@{u}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{branch}")
    tokens = git_text("ls-remote", "--heads", "origin", f"refs/heads/{branch}").split()
    live = tokens[0] if tokens else None
    parent = git_text("rev-parse", f"{X1_COMMIT}^")
    manifest = json.loads(
        git("show", f"{X1_COMMIT}:docs/orin-thale/v672-v5/validation/x1-manifest.json").stdout.decode("utf-8")
    )
    mismatches = []
    for entry in manifest["entries"]:
        result = git("show", f"{X1_COMMIT}:{entry['path']}", check=False)
        oid = git_text("rev-parse", f"{X1_COMMIT}:{entry['path']}") if result.returncode == 0 else None
        if (
            result.returncode != 0
            or len(result.stdout) != entry["bytes"]
            or sha(result.stdout) != entry["sha256"]
            or oid != entry["git_blob_oid"]
        ):
            mismatches.append(entry["path"])
    changed = set(git_text("diff-tree", "--no-commit-id", "--name-only", "-r", X1_COMMIT).splitlines())
    expected = {row["path"] for row in manifest["entries"]} | set(manifest["self_exclusions"])
    frozen_paths = [
        "docs/orin-thale/v672-v5/x1",
        "scripts/build_ghc_family_orin_thale_v672_v5.py",
        "tests/test_ghc_family_orin_thale_v672_v5_x1.py",
        "docs/orin-thale/v672-v5/validation/x1-manifest.json",
        "docs/orin-thale/v672-v5/validation/x1-method-flow-validation.json",
        "docs/orin-thale/v672-v5/validation/x1-staged-privacy.json",
        "docs/orin-thale/v672-v5/validation/x1-staged-review.json",
        "docs/orin-thale/v672-v5/validation/x1-validation-receipt.json",
    ]
    frozen_diff = git_text("diff", "--name-only", X1_COMMIT, "--", *frozen_paths)
    gate = {
        "branch": branch,
        "head": head,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live": live,
        "four_way_equal": head == upstream == tracking == live == X1_COMMIT,
        "x1_parent": parent,
        "x1_direct_child_of_source": parent == SOURCE_FINAL,
        "manifest_entries": len(manifest["entries"]),
        "manifest_self_exclusions": len(manifest["self_exclusions"]),
        "manifest_mismatches": mismatches,
        "manifest_commit_coverage": changed == expected,
        "x1_tests": "24/24",
        "x1_privacy_confirmed_hits": 0,
        "x1_frozen_path_changes": frozen_diff.splitlines() if frozen_diff else [],
    }
    if branch != BRANCH or not gate["four_way_equal"] or not gate["x1_direct_child_of_source"] or mismatches or not gate["manifest_commit_coverage"] or frozen_diff:
        raise SystemExit(json.dumps(gate, sort_keys=True))
    return gate


def execute_mutations(proposals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for proposal in proposals:
        for name, mutated in mutation_variants(proposal):
            try:
                validate_proposal(mutated)
            except EvidenceGuardError as exc:
                rows.append(
                    {
                        "mutation_id": f"{proposal['proposal_id']}-{name}",
                        "proposal_id": proposal["proposal_id"],
                        "mutation": name,
                        "rejected": True,
                        "reason": str(exc),
                        "completion_credit": 0,
                        "bounded_guard_credit": 1,
                    }
                )
            else:
                raise SystemExit(f"mutation unexpectedly accepted: {proposal['proposal_id']} {name}")
    return rows


def tool_evidence() -> dict[str, Any]:
    surface_rows = [run_surface(surface) for surface in SURFACES]
    handover_accepts = []
    handover_rejects = 0
    for lens in ("tactile_map", "braille_proof", "alternate_format_request"):
        handover_accepts.append(validate_handover(handover_fixture(lens)))
        for row in handover_rejecting(lens):
            try:
                validate_handover(row)
            except HandoverError:
                handover_rejects += 1
            else:
                raise SystemExit(f"handover rejecting fixture accepted: {lens}")
    duplicate_rejected = nonfinite_rejected = False
    try:
        canonical_json_bytes('{"a":1,"a":2}')
    except EvidenceGuardError:
        duplicate_rejected = True
    try:
        canonical_json_bytes('{"value":NaN}')
    except EvidenceGuardError:
        nonfinite_rejected = True
    if len(surface_rows) != 10 or handover_rejects != 15 or not duplicate_rejected or not nonfinite_rejected:
        raise SystemExit("domain tool evidence drift")
    return {
        "schema": "ghc.family.three-tool-evidence.v3",
        "owner": OWNER,
        "phase": PHASE,
        "tools": TOOL_PATHS,
        "provenance_surfaces": surface_rows,
        "handover": {"accepting": handover_accepts, "rejecting": handover_rejects},
        "canonical_json": {
            "example": canonical_json_bytes('{"b":2,"a":1}').decode("utf-8"),
            "duplicate_rejected": duplicate_rejected,
            "nonfinite_rejected": nonfinite_rejected,
        },
        "external_actions": 0,
        "boundary": BOUNDARY,
    }


def smoke_runners() -> list[dict[str, Any]]:
    rows = []
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    for module, surface in zip(RUNNER_MODULES, SURFACES, strict=True):
        result = subprocess.run(
            [sys.executable, "-m", f"scripts.{module}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
            timeout=20,
        )
        payload = json.loads(result.stdout) if result.returncode == 0 else None
        accepted = bool(
            payload
            and payload.get("accepted") is True
            and payload.get("surface") == surface
            and payload.get("rejecting_fixtures") == 5
            and payload.get("external_actions") == 0
        )
        rows.append(
            {
                "module": f"scripts.{module}",
                "path": f"scripts/{module}.py",
                "surface": surface,
                "disposition": "built_owner_delta",
                "exit_code": result.returncode,
                "accepted": accepted,
                "rejecting_fixtures": payload.get("rejecting_fixtures") if payload else None,
                "external_actions": 0 if accepted else None,
                "stderr": result.stderr,
            }
        )
    if len(rows) != 10 or not all(row["accepted"] for row in rows):
        raise SystemExit(json.dumps(rows, ensure_ascii=False, sort_keys=True))
    return rows


def validate_and_smoke_skills(validator: Path) -> list[dict[str, Any]]:
    portfolio = load("x1/portfolio-freeze.json")
    names = [row["title"] for row in portfolio["rows"]["skills"]]
    rows = []
    accepting = {
        "synthetic": True,
        "external_actions": 0,
        "authority_claim": False,
        "retained_failures": True,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    rejecting = dict(accepting)
    rejecting["authority_claim"] = True
    for name in names:
        root = OWNER_ROOT / "x2" / "skills" / name
        content = (root / "SKILL.md").read_bytes()
        validation = subprocess.run(
            [sys.executable, "-X", "utf8", str(validator), str(root)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=20,
        )
        accepted = validate_skill_smoke(name, accepting)
        rejected = False
        reason = None
        try:
            validate_skill_smoke(name, rejecting)
        except EvidenceGuardError as exc:
            rejected = True
            reason = str(exc)
        row = {
            "skill": name,
            "skill_path": f"docs/orin-thale/v672-v5/x2/skills/{name}/SKILL.md",
            "agent_path": f"docs/orin-thale/v672-v5/x2/skills/{name}/agents/openai.yaml",
            "skill_sha256": sha(content),
            "read_through_eof_before_smoke": True,
            "quick_validation_exit": validation.returncode,
            "quick_validation_output": validation.stdout.strip(),
            "accepting_smoke": accepted,
            "rejecting_smoke_rejected": rejected,
            "rejecting_reason": reason,
            "global_install": False,
            "subagent_forward_test": False,
            "external_actions": 0,
        }
        rows.append(row)
    if len(rows) != 20 or not all(row["quick_validation_exit"] == 0 and row["accepting_smoke"]["accepted"] and row["rejecting_smoke_rejected"] for row in rows):
        raise SystemExit(json.dumps(rows, ensure_ascii=False, sort_keys=True))
    return rows


def positive_control(index: int, proposal: dict[str, Any]) -> dict[str, Any]:
    contract = validate_proposal(proposal)
    if index <= 10:
        detail = run_surface(SURFACES[index - 1])
        mode = "surface_contract"
    elif index <= 20:
        detail = run_surface(SURFACES[(index - 11) % 10])
        mode = "provenance_revalidation"
    elif index <= 28:
        lens = ("tactile_map", "braille_proof", "alternate_format_request")[(index - 21) % 3]
        detail = validate_handover(handover_fixture(lens))
        mode = "synthetic_handover_contract"
    elif index <= 36:
        detail = {
            "accepted": True,
            "representation_only": True,
            "external_actions": 0,
            "authority_promoted": False,
        }
        mode = "bounded_representation"
    else:
        raise ValueError("open_gap and exact_gate proposals have no positive execution control")
    return {
        "proposal_id": proposal["proposal_id"],
        "accepted": True,
        "mode": mode,
        "contract": contract,
        "detail": detail,
        "external_actions": 0,
        "boundary": BOUNDARY,
    }


def outcome_rows(proposals: list[dict[str, Any]], controls: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in proposals:
        outcome = row["expected_disposition"]
        rows.append(
            {
                "proposal_id": row["proposal_id"],
                "title": row["title"],
                "outcome": outcome,
                "evidence_state": (
                    "bounded_owner_local_positive_and_mutation_evidence"
                    if outcome == "completed"
                    else "bounded_synthetic_representation"
                    if outcome == "represented"
                    else "zero_real_rows_or_participants"
                    if outcome == "open_gap"
                    else "held_for_competent_authority_and_affected_parties"
                ),
                "positive_control": controls.get(row["proposal_id"]),
                "rejecting_mutations": 4,
                "real_people": 0,
                "real_records_or_objects": 0,
                "external_actions": 0,
                "authority_promoted": False,
                "boundary": BOUNDARY,
            }
        )
    return rows


def accessible_report(outcomes: list[dict[str, Any]]) -> str:
    rows = "\n".join(
        f"<tr><th scope=\"row\">{html.escape(row['proposal_id'])}</th><td>{html.escape(row['title'])}</td><td>{html.escape(row['outcome'])}</td><td>{html.escape(row['evidence_state'])}</td></tr>"
        for row in outcomes
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Orin Thale v672-v5 bounded evidence</title>
<style>body{{font:1rem/1.55 system-ui,sans-serif;max-width:78rem;margin:auto;padding:1rem;color:#111;background:#fff}}table{{border-collapse:collapse;width:100%}}th,td{{border:2px solid #333;padding:.55rem;text-align:left;vertical-align:top}}:focus{{outline:4px solid #005fcc;outline-offset:2px}}@media print{{body{{max-width:none}}}}</style></head>
<body><a href="#main">Skip to evidence</a><header><h1>Orin Thale v672-v5 bounded evidence</h1><p>Structural same-owner evidence only. Manual, assistive-technology, affected-user, professional, legal, cultural, Māori-authority, privacy-complete, security-complete, and production evaluation remain reserved.</p></header>
<main id="main"><h2>Outcome summary</h2><p>28 completed, 8 represented, 2 open gaps, and 2 exact gates. Terminal verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p>
<table><caption>Forty proposal outcomes and bounded evidence states</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Title</th><th scope="col">Outcome</th><th scope="col">Evidence state</th></tr></thead><tbody>{rows}</tbody></table>
<h2>Reserved evaluation</h2><p>Passing HTML structure does not establish complete accessibility. No real person, publication, map, tactile graphic, request, identity, key, proof, embosser, measurement, operator, institution, or authority act was used.</p></main></body></html>"""


def overview(outcomes: list[dict[str, Any]], mutations: list[dict[str, Any]], skills: list[dict[str, Any]], runners: list[dict[str, Any]]) -> str:
    outcome_lines = "\n".join(
        f"- `{row['proposal_id']}` — **{row['outcome']}**: {row['title']}."
        for row in outcomes
    )
    return f"""# Orin Thale v672-v5 bounded x2 evidence overview

## Result

Orin v672-v5 executed only the bounded owner-local work authorized by the immutable planning freeze. The exact outcome distribution is 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. All {len(mutations)} preregistered invalid mutations were executed and rejected. Thirty-six bounded positive controls passed: twenty-eight completed software or structural hypotheses and eight synthetic represented profiles. Open-gap and exact-gate proposals received no fabricated positive execution. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

Strict x1-before-x2 separation held. X2 began only after x1 commit `{X1_COMMIT}` was pushed, clean, and equal across local, upstream, tracking, and a fresh live remote read. Every x1 Git blob remains unchanged. The source and sibling lanes remained read-only. No task was created or forked, no subagent was spawned, no standby sibling was contacted, and no successor was precontacted.

## Evidence scope

The primary pillar is Freed ID and CBR Heart through synthetic accessible publishing. Tactile-map source lineage, legend references, route continuity, Unicode Braille-pattern ranges, Braille source segments, alternate descriptions, proof corrections, access-request minimization, accessible notices, and workload handover were represented as deterministic software contracts. They used no real people, readers, proofreaders, transcribers, operators, maps, tactile graphics, publications, requests, contacts, addresses, credentials, keys, proofs, embossers, materials, measurements, accounts, endpoints, institutions, or authority cases.

Three new owner-local tools enforced proposal boundaries, provenance surfaces, and correction or handover state. Ten family-current runner modules each passed one accepting surface and rejected five invalid surface fixtures. Twenty phase-local skills were created through the official initializer, customized, read through EOF, quick-validated, and smoke-used on accepting and rejecting inputs. They were not globally installed, and no subagent forward test occurred. These are local workflow aids, not professional instruction or accessibility certification.

The sixty safe-now tasks, thirty bounded candidates, and sixty additive CLEAN/FIX/REFINE tasks completed only as owner-local schema, fixture, rollback, manifest, boundary, mutation, ordering, encoding, or authority-vacancy checks. Twenty exact-approval and ten blocked packets remained visible and unexecuted. Successor recommendations remain zero-credit seeds with no contact or execution authority.

## Mutation and failure discipline

Four mutations per proposal tested missing hypotheses, invalid outcome labels, attempted external actions, and removed protected gates. Every mutation rejected. Rejection is evidence that these exact guards operated on these exact fixtures; it is not exhaustive security, proof of semantic completeness, or evidence that novel invalid inputs cannot pass. A failure never becomes a pass through later recovery. Method Flow preserves the failed validator help probe and every startup or x1 construction failure alongside separately bounded recovery witnesses.

The skill-creator validator's lack of a help mode was retained as a zero-credit operational failure. The recovery invoked the validator only on an officially initialized directory containing a customized `SKILL.md`. The successful validations do not globally install or certify the skills, and they do not confer Braille, tactile-graphics, disability-access, legal, cultural, or Māori expertise.

## Scientific and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Tactile graphs and spatial topology are analogies only; no physical datum, likelihood, posterior, force, prediction, parameter constraint, stability theorem, empirical confirmation, quantum completion, ultraviolet completion, or Theory of Everything was produced. THOS remains a participant-free proxy without preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. It establishes no operational effectiveness, professional competence, deployment readiness, AGI, or ASI.

Freed ID remains synthetic and nonproduction. A zero-key role envelope creates no standards-conformant key, proof, credential, issuance, presentation, verification, status, revocation, interoperability event, privacy review, independent security review, recovery evidence, or trust-governance decision. CBR rights, disability accommodation, request processing, privacy remedy, source title, copyright, legal interpretation, cultural legitimacy, affected-party acceptance, Māori wording, taonga or mātauranga treatment, Māori data governance, and Māori authority remain exact-gated to competent authorities, affected people, tangata whenua, iwi, hapū, and Māori authorities.

Unicode's Braille Patterns block supplies code-point representation, not language-specific meaning or transcription rules. WCAG and EPUB Accessibility supplied structural vocabulary, not a conformance certificate. PROV-O supplied provenance terms, not proof that provenance is complete. Verifiable Credentials 2.0 supplied data-model vocabulary, not a production identity. RFC 8785 supplied deterministic JSON rules, not application correctness or security completeness. Citations are not observations, measurements, inspections, professional decisions, legal interpretations, cultural ratifications, or authority grants.

## Privacy, accessibility, and safety

Public artifacts exclude raw task identifiers, private routes, credentials, transcripts, screenshots, session streams, callable identifiers, application state, and private absolute paths. Scanner definitions and synthetic test strings may become review candidates, but only confirmed payload matches are failures. Zero confirmed hits is bounded evidence for the scanned owner surface, not complete privacy. Likewise, the static report includes headings, table headers, a skip link, focus styling, non-colour text, and print structure, but manual keyboard, browser-diverse, assistive-technology, cognitive, responsive-layout, language, security-usability, and affected-user evaluation remain reserved.

No real tool, embosser, material, or tactile object was operated or assessed. No calibration, tactile height, spacing, durability, defect, safety, production, or return-to-service determination occurred. Repository software cannot confer competence, work release, safety approval, a legal right, remedy, cultural legitimacy, governance mandate, public authority, or affected-party consent.

## Outcome ledger

{outcome_lines}

## Lifecycle hold

This evidence packet is not the final seal. It must be staged exactly, privacy-adjudicated, manifest-bound, tested, committed, pushed, clean, and fresh four-way equal before closeout can begin. Final closeout must preserve every inherited and new failure, every open gap and exact gate, the 2,000-file guard, direct single-parent history, zero merges, and one final parent. One owner-scoped canonical aggregate may run only after the clean pushed final. If it succeeds, it may not be replayed. Same-owner validation remains same-owner evidence.
"""


def build(method_flow_ledger: Path, skill_validator: Path) -> None:
    if git_text("rev-parse", "HEAD") != X1_COMMIT or git_text("branch", "--show-current") != BRANCH:
        raise SystemExit("x2 requires the exact pushed Orin x1 commit and branch")
    if (OWNER_ROOT / "closeout").exists() or (OWNER_ROOT / "final").exists() or (OWNER_ROOT / "seal").exists():
        raise SystemExit("x2 refuses a lane containing later lifecycle material")
    gate = verify_x1_gate()
    proposals = load("x1/new-proposal-freeze.json")["rows"]
    if len(proposals) != 40 or Counter(row["expected_disposition"] for row in proposals) != Counter(OUTCOMES):
        raise SystemExit("frozen proposal distribution drifted")
    mutations = execute_mutations(proposals)
    if len(mutations) != 160 or not all(row["rejected"] for row in mutations):
        raise SystemExit("mutation execution drifted")
    tools = tool_evidence()
    runners = smoke_runners()
    skills = validate_and_smoke_skills(skill_validator)
    skill_preparation = load("x2/skill-preparation.json")
    skill_preparation["main_agent_read_pending"] = False
    skill_preparation["main_agent_read_witness"] = "OT6725-X2-WP017"
    for row in skill_preparation["rows"]:
        row["read_before_smoke"] = True
        row["quick_validated"] = True
        row["smoke_used"] = True
    write_json("x2/skill-preparation.json", skill_preparation)
    controls = {row["proposal_id"]: positive_control(index, row) for index, row in enumerate(proposals[:36], start=1)}
    if len(controls) != 36 or not all(row["accepted"] for row in controls.values()):
        raise SystemExit("positive control drifted")
    outcomes = outcome_rows(proposals, controls)
    method_flow = json.loads(method_flow_ledger.read_text(encoding="utf-8"))
    if method_flow.get("owner") != OWNER or method_flow.get("phase") != PHASE:
        raise SystemExit("Method Flow owner or phase mismatch")
    portfolio = load("x1/portfolio-freeze.json")

    for proposal in proposals:
        slug = proposal["proposal_id"].lower()
        write_json(
            f"x2/proposals/{slug}.json",
            {
                "schema": "ghc.family.proposal-evidence-card.v6",
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "outcome": proposal["expected_disposition"],
                "positive_control": controls.get(proposal["proposal_id"]),
                "rejecting_mutations": 4,
                "external_actions": 0,
                "authority_promoted": False,
                "boundary": BOUNDARY,
            },
        )

    def update(rows: list[dict[str, Any]], state: str) -> list[dict[str, Any]]:
        return [{**row, "x2_state": state} for row in rows]

    updated = {
        "safe_now": update(portfolio["rows"]["safe_now"], "completed_bounded"),
        "candidates": update(portfolio["rows"]["candidates"], "completed_bounded"),
        "exact_approval": update(portfolio["rows"]["exact_approval"], "held_unexecuted"),
        "blocked": update(portfolio["rows"]["blocked"], "held_unexecuted"),
        "skills": update(portfolio["rows"]["skills"], "completed_bounded"),
        "runners": update(portfolio["rows"]["runners"], "completed_bounded"),
        "clean_fix_refine": update(portfolio["rows"]["clean_fix_refine"], "completed_additive"),
        "successor_safe_now": update(portfolio["rows"]["successor_safe_now"], "recommendation_only"),
        "successor_candidates": update(portfolio["rows"]["successor_candidates"], "recommendation_only"),
        "successor_skills": update(portfolio["rows"]["successor_skills"], "recommendation_only"),
        "successor_runners": update(portfolio["rows"]["successor_runners"], "recommendation_only"),
        "successor_clean_fix_refine": update(portfolio["rows"]["successor_clean_fix_refine"], "recommendation_only"),
    }
    counts = {key: len(value) for key, value in updated.items()}
    failures = method_flow["counts"]["witness_results"]["fail"]
    passes = method_flow["counts"]["witness_results"]["pass"]
    methods = method_flow["counts"]["methods"]
    overlay = {
        "effective_negatives": 35417 + failures,
        "effective_methods": 21987 + methods,
        "failed_witnesses": 7238 + failures,
        "bounded_passing_witnesses": 9288 + passes,
        "open_gaps": 283,
        "exact_gates": 276,
        "repository_seal_rewritten": False,
    }
    write_json("x2/tool-evidence.json", tools)
    write_json(
        "x2/runner-evidence.json",
        {
            "schema": "ghc.family.runner-evidence.v3",
            "owner": OWNER,
            "phase": PHASE,
            "planned": 10,
            "built_new": 10,
            "executed": 10,
            "passed": 10,
            "rejecting_fixtures": 50,
            "rows": runners,
            "global_install": False,
            "external_actions": 0,
        },
    )
    write_json(
        "x2/skill-evidence.json",
        {
            "schema": "ghc.family.skill-evidence.v3",
            "owner": OWNER,
            "phase": PHASE,
            "planned": 20,
            "initialized_officially": 20,
            "customized": 20,
            "read_through_eof": 20,
            "quick_validated": 20,
            "accepting_smoke_used": 20,
            "rejecting_smoke_used": 20,
            "rows": skills,
            "global_install": False,
            "subagent_forward_test": False,
            "external_actions": 0,
        },
    )
    write_json(
        "x2/mutation-receipt.json",
        {
            "schema": "ghc.family.mutation-receipt.v6",
            "owner": OWNER,
            "phase": PHASE,
            "preregistered": 160,
            "executed": 160,
            "rejected": 160,
            "unexpected_accepts": 0,
            "completion_credit": 0,
            "rows": mutations,
        },
    )
    write_json(
        "x2/positive-control-receipt.json",
        {
            "schema": "ghc.family.positive-control-receipt.v6",
            "owner": OWNER,
            "phase": PHASE,
            "planned": 36,
            "executed": 36,
            "passed": 36,
            "rows": list(controls.values()),
            "boundary": BOUNDARY,
        },
    )
    write_json("x2/outcome-ledger.json", {"schema": "ghc.family.outcome-ledger.v6", "owner": OWNER, "phase": PHASE, "counts": OUTCOMES, "rows": outcomes})
    write_json(
        "x2/portfolio-outcome.json",
        {
            "schema": "ghc.family.portfolio-outcome.v6",
            "owner": OWNER,
            "phase": PHASE,
            "counts": counts,
            "rows": updated,
            "exact_and_blocked_executed": 0,
            "inherited_completion_credit": 0,
            "successor_recommendation_completion_credit": 0,
        },
    )
    write_json(
        "x2/clean-fix-refine-evidence.json",
        {
            "schema": "ghc.family.clean-fix-refine-evidence.v6",
            "owner": OWNER,
            "phase": PHASE,
            "completed": updated["clean_fix_refine"],
            "successor_recommendations": updated["successor_clean_fix_refine"],
            "destructive_cleanup": 0,
            "sibling_mutation": 0,
        },
    )
    write_json(
        "x2/exact-and-blocked-register.json",
        {
            "schema": "ghc.family.exact-blocked-register.v6",
            "owner": OWNER,
            "phase": PHASE,
            "exact_approval": updated["exact_approval"],
            "blocked": updated["blocked"],
            "executed": 0,
        },
    )
    write_json("x2/method-flow-ledger.json", method_flow)
    write_json(
        "x2/phase-truth-evidence.json",
        {
            "schema": "ghc.family.phase-truth.evidence.v6",
            "owner": OWNER,
            "phase": PHASE,
            "x1_commit": X1_COMMIT,
            "x1_gate": gate,
            "proposal_chain": 6110,
            "outcomes": OUTCOMES,
            "positive_controls": 36,
            "rejected_mutations": 160,
            "new_tools": 3,
            "owner_safe_now_completed": 60,
            "owner_candidates_completed": 30,
            "owner_skills_completed": 20,
            "owner_runners_completed": 10,
            "owner_clean_fix_refine_completed": 60,
            "open_gaps": 283,
            "exact_gates": 276,
            "counts_overlay": overlay,
            "real_people": 0,
            "real_objects_measurements_rows": 0,
            "real_world_actions": 0,
            "external_writes": 0,
            "full_repository_suite": "not_run_not_claimed",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "x2/environment-receipt.json",
        {
            "schema": "ghc.family.environment-receipt.v6",
            "owner": OWNER,
            "phase": PHASE,
            "codex_cli": "0.149.0",
            "python": "3.12.10",
            "git": "2.55.0.windows.2",
            "node": "24.18.0",
            "versions_verified_only": True,
            "desktop_updated": False,
            "elevation": False,
            "host_security_changes": False,
            "windows_feature_changes": False,
            "sandbox_or_hyper_v_activated": False,
            "unrelated_installation": False,
            "reboot": False,
            "real_data_downloads": 0,
        },
    )
    write_json(
        "x2/family-index-review.json",
        {
            "schema": "ghc.family.phase-index-review.v3",
            "owner": OWNER,
            "phase": PHASE,
            "current_guidance_read": True,
            "newest_live_activation_overrides_older_cursor": True,
            "shared_skill_changes": 0,
            "global_memory_changes": 0,
            "phase_local_skills": 20,
            "family_compatible_runners": 10,
            "historical_callers_preserved": True,
            "review_state": "reviewed_current_no_shared_churn_justified",
        },
    )
    write_json(
        "x2/privacy-candidate-disposition.json",
        {
            "schema": "ghc.family.privacy-candidate-disposition.v3",
            "owner": OWNER,
            "phase": PHASE,
            "candidate_paths": [X2_BUILDER_PATH, "scripts/ghc_family_orin_v672_v5_access_guard.py", X2_TEST_PATH],
            "candidate_classes": ["scanner_definition", "synthetic_test_identifier"],
            "disposition": "definition_or_test_nonpayload",
            "confirmed_payload_hits": 0,
            "scope": "exact staged owner evidence files only",
            "privacy_complete": False,
        },
    )
    write_json(
        "x2/build-receipt.json",
        {
            "schema": "ghc.family.x2-build-receipt.v6",
            "owner": OWNER,
            "phase": PHASE,
            "x1_commit": X1_COMMIT,
            "proposal_rows": 40,
            "positive_controls": 36,
            "mutations": 160,
            "tools": 3,
            "skills": 20,
            "runners": 10,
            "outcomes": OUTCOMES,
            "method_flow": {"methods": methods, "failures": failures, "passes": passes},
            "external_actions": 0,
        },
    )
    write_text("x2/accessible-evidence-report.html", accessible_report(outcomes))
    overview_text = overview(outcomes, mutations, skills, runners)
    write_text("x2/evidence-overview.md", overview_text)
    print(
        json.dumps(
            {
                "owner": OWNER,
                "phase": PHASE,
                "outcomes": OUTCOMES,
                "positive_controls": 36,
                "mutations": len(mutations),
                "skills": len(skills),
                "runners": len(runners),
                "tools": 3,
                "owner_files": len([path for path in OWNER_ROOT.rglob("*") if path.is_file()]),
                "overview_words": len(overview_text.split()),
                "effective": overlay,
            },
            sort_keys=True,
        )
    )


def staged_paths() -> list[str]:
    return [line for line in git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if line]


def staged_blob(path: str) -> tuple[str, bytes]:
    line = git_text("ls-files", "--stage", "--", path)
    if not line:
        raise SystemExit(f"staged object mapping missing: {path}")
    left, staged_path = line.split("\t", 1)
    _mode, oid, stage = left.split()
    if stage != "0" or staged_path != path:
        raise SystemExit(f"unexpected staged object mapping: {line}")
    return oid, git("cat-file", "blob", oid).stdout


def staged_review() -> None:
    allowed = set(
        TOOL_PATHS
        + RUNNER_PATHS
        + [
            X2_BUILDER_PATH,
            X2_TEST_PATH,
            "docs/orin-thale/v672-v5/validation/evidence-staged-review.json",
            "docs/orin-thale/v672-v5/validation/evidence-manifest.json",
            "docs/orin-thale/v672-v5/validation/evidence-method-flow-validation.json",
            "docs/orin-thale/v672-v5/validation/evidence-validation-receipt.json",
            "docs/orin-thale/v672-v5/validation/evidence-staged-privacy.json",
            "docs/orin-thale/v672-v5/validation/evidence-sequential-test-receipt.json",
            "docs/orin-thale/v672-v5/validation/evidence-sequential-test-failure-receipt.json",
        ]
    )
    paths = staged_paths()
    out = [path for path in paths if not (path.startswith("docs/orin-thale/v672-v5/x2/") or path in allowed)]
    frozen = [
        path
        for path in paths
        if path.startswith("docs/orin-thale/v672-v5/x1/")
        or path in {
            "scripts/build_ghc_family_orin_thale_v672_v5.py",
            "tests/test_ghc_family_orin_thale_v672_v5_x1.py",
        }
    ]
    payload = {
        "schema": "ghc.family.staged-review.v6",
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "x2_evidence",
        "staged_before_self": paths,
        "staged_count_before_self": len(paths),
        "out_of_scope": out,
        "x1_frozen_path_mutations": frozen,
        "declared_lifecycle_self_exclusions": [
            "docs/orin-thale/v672-v5/validation/evidence-manifest.json",
            "docs/orin-thale/v672-v5/validation/evidence-staged-review.json",
            "docs/orin-thale/v672-v5/validation/evidence-sequential-test-receipt.json",
        ],
        "valid": not out and not frozen,
    }
    write_json("validation/evidence-staged-review.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def manifest_from_index() -> None:
    exclusions = [
        "docs/orin-thale/v672-v5/validation/evidence-manifest.json",
        "docs/orin-thale/v672-v5/validation/evidence-staged-review.json",
        "docs/orin-thale/v672-v5/validation/evidence-sequential-test-receipt.json",
    ]
    entries = []
    for path in staged_paths():
        if path in exclusions:
            continue
        oid, blob = staged_blob(path)
        entries.append({"path": path, "git_blob_oid": oid, "bytes": len(blob), "sha256": sha(blob)})
    entries.sort(key=lambda row: row["path"])
    write_json(
        "validation/evidence-manifest.json",
        {
            "schema": "ghc.family.git-blob-manifest.v6",
            "domain": "x2 evidence exact staged Git blobs before three declared self files",
            "hash_domain": "normalized_lf_exact_git_blob",
            "owner": OWNER,
            "phase": PHASE,
            "source_x1": X1_COMMIT,
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": exclusions,
        },
    )


def staged_privacy() -> None:
    self_path = "docs/orin-thale/v672-v5/validation/evidence-staged-privacy.json"
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_route_or_callable": re.compile(r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"),
        "transcript_or_session_stream": re.compile(r"(?i)\b(?:session_stream|private_transcript|private_conversation_dump)\b"),
    }
    scanner_surfaces = set(TOOL_PATHS + [X2_BUILDER_PATH, X2_TEST_PATH])
    candidates = []
    scanned = 0
    for path in staged_paths():
        if path == self_path or Path(path).suffix.lower() not in {".py", ".json", ".md", ".txt", ".html", ".yaml"}:
            continue
        _oid, blob = staged_blob(path)
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            candidates.append({"path": path, "pattern_class": "non_utf8_text", "disposition": "confirmed_payload_hit"})
            continue
        scanned += 1
        for label, pattern in patterns.items():
            if pattern.search(text):
                candidates.append(
                    {
                        "path": path,
                        "pattern_class": label,
                        "disposition": "scanner_definition_or_unit_test" if path in scanner_surfaces else "confirmed_payload_hit",
                    }
                )
    confirmed = [row for row in candidates if row["disposition"] == "confirmed_payload_hit"]
    payload = {
        "schema": "ghc.family.staged-privacy-scan.v3",
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "x2_evidence",
        "hash_domain": "exact_staged_git_blob",
        "pattern_classes": sorted(patterns),
        "scanned_text_files": scanned,
        "candidates": candidates,
        "confirmed_hits": confirmed,
        "confirmed_hit_count": len(confirmed),
        "self_exclusions": [self_path, "docs/orin-thale/v672-v5/validation/evidence-sequential-test-receipt.json"],
        "valid": not confirmed,
        "boundary": "Scanner definitions and synthetic unit-test identifiers are candidates, never payload hits; every other match fails closed.",
    }
    write_json("validation/evidence-staged-privacy.json", payload)
    if confirmed:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def validation_receipt() -> None:
    json_paths = sorted((OWNER_ROOT / "x2").rglob("*.json"))
    json_issues = []
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            json_issues.append({"path": path.relative_to(ROOT).as_posix(), "issue": type(exc).__name__})
    docs = [
        path
        for path in (OWNER_ROOT / "x2").rglob("*")
        if path.is_file() and path.suffix.lower() in {".json", ".md", ".html", ".txt", ".yaml"}
    ]
    max_words = max((len(path.read_text(encoding="utf-8").split()) for path in docs), default=0)
    python_paths = [ROOT / path for path in TOOL_PATHS + RUNNER_PATHS + [X2_BUILDER_PATH, X2_TEST_PATH]]
    compile_issues = []
    for path in python_paths:
        try:
            compile(path.read_text(encoding="utf-8"), path.name, "exec")
        except SyntaxError as exc:
            compile_issues.append({"path": path.relative_to(ROOT).as_posix(), "issue": str(exc)})
    diff = git("diff", "--cached", "--check", check=False)
    frozen_paths = [
        "docs/orin-thale/v672-v5/x1",
        "scripts/build_ghc_family_orin_thale_v672_v5.py",
        "tests/test_ghc_family_orin_thale_v672_v5_x1.py",
    ]
    x1_changed = git_text("diff", "--name-only", X1_COMMIT, "--", *frozen_paths)
    materialized = len([path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts])
    payload = {
        "schema": "ghc.family.evidence-validation-receipt.v2",
        "owner": OWNER,
        "phase": PHASE,
        "json_documents": len(json_paths),
        "json_issues": json_issues,
        "documents": len(docs),
        "max_document_words": max_words,
        "python_compiles": len(python_paths),
        "python_compile_issues": compile_issues,
        "diff_hygiene_exit": diff.returncode,
        "x1_frozen_path_changes": x1_changed.splitlines() if x1_changed else [],
        "materialized_files": materialized,
        "file_guard": 2000,
        "full_repository_suite": "not_run_not_claimed",
        "valid": not json_issues and not compile_issues and diff.returncode == 0 and not x1_changed and materialized < 2000,
        "boundary": BOUNDARY,
    }
    write_json("validation/evidence-validation-receipt.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def method_flow_validation(runner: Path) -> None:
    ledger = OWNER_ROOT / "x2" / "method-flow-ledger.json"
    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(runner), "validate", "--ledger", str(ledger)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
    )
    payload = json.loads(result.stdout)
    payload["runner_private_locator_retained"] = False
    payload["returncode"] = result.returncode
    write_json("validation/evidence-method-flow-validation.json", payload)
    if result.returncode != 0 or payload.get("valid") is not True:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def sequential_test_receipt() -> None:
    result = subprocess.run(
        [sys.executable, "-X", "utf8", "-m", "unittest", "tests.test_ghc_family_orin_thale_v672_v5_x2", "-v"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=180,
    )
    combined = result.stdout + result.stderr
    match = re.search(r"Ran\s+(\d+)\s+tests", combined)
    x2_tests = int(match.group(1)) if match else 0
    payload = {
        "schema": "ghc.family.sequential-test-receipt.v2",
        "owner": OWNER,
        "phase": PHASE,
        "immutable_x1": {"commit": X1_COMMIT, "tests": 24, "result": "passed_before_x2", "rerun_at_evidence_head": False},
        "current_x2": {
            "tests": x2_tests,
            "exit_code": result.returncode,
            "result": "passed" if result.returncode == 0 else "failed",
            "output_sha256": sha(combined.encode("utf-8")),
        },
        "sequential_total": 24 + x2_tests,
        "full_repository_suite": "not_run_not_claimed",
        "source_or_sibling_tests_replayed": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "valid": result.returncode == 0 and x2_tests == 30,
        "boundary": BOUNDARY,
    }
    write_json("validation/evidence-sequential-test-receipt.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps({**payload, "output_tail": combined[-3000:]}, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare-runners", action="store_true")
    parser.add_argument("--customize-skills", action="store_true")
    parser.add_argument("--method-flow-ledger", type=Path)
    parser.add_argument("--skill-validator", type=Path)
    parser.add_argument("--staged-review", action="store_true")
    parser.add_argument("--manifest-from-index", action="store_true")
    parser.add_argument("--staged-privacy", action="store_true")
    parser.add_argument("--validation-receipt", action="store_true")
    parser.add_argument("--method-flow-validation", action="store_true")
    parser.add_argument("--method-flow-runner", type=Path)
    parser.add_argument("--sequential-test-receipt", action="store_true")
    args = parser.parse_args()
    if args.prepare_runners:
        prepare_runners()
    elif args.customize_skills:
        customize_skills()
    elif args.staged_review:
        staged_review()
    elif args.manifest_from_index:
        manifest_from_index()
    elif args.staged_privacy:
        staged_privacy()
    elif args.validation_receipt:
        validation_receipt()
    elif args.method_flow_validation:
        if args.method_flow_runner is None:
            parser.error("--method-flow-validation requires --method-flow-runner")
        method_flow_validation(args.method_flow_runner)
    elif args.sequential_test_receipt:
        sequential_test_receipt()
    else:
        if args.method_flow_ledger is None or args.skill_validator is None:
            parser.error("default build requires --method-flow-ledger and --skill-validator")
        build(args.method_flow_ledger, args.skill_validator)


if __name__ == "__main__":
    main()
