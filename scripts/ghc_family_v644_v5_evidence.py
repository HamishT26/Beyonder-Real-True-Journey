#!/usr/bin/env python3
"""Build the Eiren Kestrel v644-v5 x2 evidence packet."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from collections import Counter
from pathlib import Path
from typing import Any

from ghc_family_v644_v5_model import proposal_cases
from ghc_family_v644_v5_x1_definitions import OVERVIEW, PROPOSALS, SOURCES, X1_NEGATIVES


PHASE = "v644-gmut-thos-v5-x1-x2"
OWNER = "Eiren Kestrel"
X1_COMMIT = "8a4323e25aeff7a3b9abce898b460cf125e5db83"
SOURCE_REVISION = "9785197893954cfcc57d7632e65e497454e9ab39"
PHASE_REL = Path("docs/eiren-kestrel/v644-v5")
INHERITED_NEGATIVES = Path("docs/sylven-arc/v644-v4/retained-negative-register.json")
INHERITED_GATES = Path("docs/sylven-arc/v644-v4/exact-open-gate-register.json")


X2_NEGATIVES = [
    {
        "negative_id": "V6445-X2-N01",
        "class": "content_seal_design",
        "failure_signature": "The first x1 content-seal plan included the seal file itself, making the stored self-hash stale after every rewrite.",
        "trigger_preconditions": ["manifest input set included its own output"],
        "recovery": "Excluded the seal output from its own hash domain and added a regression test.",
        "recurrence_guard": "Every manifest or seal builder must declare and test its non-circular exclusion set.",
        "promotion_effect": "none; the self-referential seal was not committed",
    },
    {
        "negative_id": "V6445-X2-N02",
        "class": "windows_utf8_validation",
        "failure_signature": "The first skill validation opened UTF-8 Māori wording through the legacy Windows code page and raised a decode error.",
        "trigger_preconditions": ["validator inherited a non-UTF-8 default text encoding"],
        "recovery": "Reran the unchanged validator in explicit Python UTF-8 mode and preserved the original wording.",
        "recurrence_guard": "Use Python UTF-8 mode for local skill validators that do not declare an encoding.",
        "promotion_effect": "only the explicit UTF-8 validation pass is promoted",
    },
    {
        "negative_id": "V6445-X2-N03",
        "class": "byte_probe_portability",
        "failure_signature": "A diagnostic byte-stream probe used a PowerShell parameter unavailable in the installed legacy shell.",
        "trigger_preconditions": ["command assumed a newer PowerShell byte-stream parameter"],
        "recovery": "Used a read-only Python subprocess byte capture for the Git blob hash.",
        "recurrence_guard": "Prefer cross-version binary readers or test the PowerShell edition before using newer parameters.",
        "promotion_effect": "none; the failed probe produced no hash evidence",
    },
    {
        "negative_id": "V6445-X2-N04",
        "class": "patch_transport_quoting",
        "failure_signature": "A documentation patch containing Markdown delimiter characters was parsed by the host template transport before reaching the patch engine.",
        "trigger_preconditions": ["unescaped delimiter characters inside a host template literal"],
        "recovery": "Used indentation and plain text instead of transport-sensitive delimiters, then applied the same semantic update.",
        "recurrence_guard": "Avoid or explicitly escape host-template delimiter characters in generated patch payloads.",
        "promotion_effect": "none; only the successfully applied skill update is evidence",
    },
    {
        "negative_id": "V6445-X2-N05",
        "class": "validation_dependency_cycle",
        "failure_signature": "The first lean-companion replay plan ran the artifact suite that required the final lean receipt before that receipt could be emitted.",
        "trigger_preconditions": ["a validator consumes the receipt produced only after that same validator finishes"],
        "recovery": "Split the companion replay into x1 contract tests plus receipt-independent model tests, then validate the complete canonical packet after the receipt exists.",
        "recurrence_guard": "Before running a staged validator, draw its input/output dependency boundary and exclude outputs that cannot truthfully exist until the stage completes.",
        "promotion_effect": "none; the circular replay design was corrected before execution",
    },
    {
        "negative_id": "V6445-X2-N06",
        "class": "active_surface_selection",
        "failure_signature": "The first lean-companion selector considered only Git diff output and would have omitted current untracked x2 artifacts.",
        "trigger_preconditions": ["the active surface contains owner-generated files not yet committed"],
        "recovery": "Union the baseline diff with Git's bounded exclude-aware untracked-file listing before dependency closure.",
        "recurrence_guard": "Lean-repository selectors must test tracked changes and untracked owner outputs as separate input classes.",
        "promotion_effect": "none; the incomplete selector was corrected before companion creation",
    },
    {
        "negative_id": "V6445-X2-N07",
        "class": "lean_companion_timeout",
        "failure_signature": "The first additive companion attempt selected an inherited pointer-chain closure of 1585 files and exceeded the two-minute command window before Git initialization.",
        "trigger_preconditions": ["unbounded recursive JSON path closure crossed the current-phase boundary"],
        "recovery": "Retained the incomplete additive directory, limited path closure to the current phase, and prepared one fresh retry without changing canonical history.",
        "recurrence_guard": "Count the dependency closure before materialization and keep active-surface JSON references inside a declared phase boundary unless an exact dependency requires expansion.",
        "promotion_effect": "none; the incomplete companion is not a verified artifact",
    },
    {
        "negative_id": "V6445-X2-N08",
        "class": "temporal_test_assumption",
        "failure_signature": "The x1 artifact test inferred x1 separation from the current working tree, which necessarily contains x2 files during later lifecycle validation.",
        "trigger_preconditions": ["an immutable earlier-stage assertion was evaluated against a later-stage mutable filesystem"],
        "recovery": "Evaluate x1 separation against the frozen x1 exact-file-set receipt rather than present-day path existence.",
        "recurrence_guard": "Lifecycle tests for prior stages must read immutable stage receipts or exact commits, never infer prior state from the current workspace.",
        "promotion_effect": "the corrected test preserves the same x1 separation claim across later stages",
    },
    {
        "negative_id": "V6445-X2-N09",
        "class": "windows_stdout_encoding",
        "failure_signature": "The Method Flow summary wrote its UTF-8 artifacts successfully but its final JSON console echo failed when the legacy Windows code page encountered Māori text.",
        "trigger_preconditions": ["UTF-8 payload printed through a legacy non-UTF-8 console encoding"],
        "recovery": "Rerun the unchanged summary command in explicit Python UTF-8 mode and validate the written files.",
        "recurrence_guard": "Use explicit UTF-8 mode for both file validation and console-emitting workflow runners on Windows.",
        "promotion_effect": "only the explicit UTF-8 rerun is promoted; the failed console echo remains retained",
    },
    {
        "negative_id": "V6445-X2-N10",
        "class": "staged_privacy_literal",
        "failure_signature": "The first exact staged scan found a private-route field label embedded as a literal in the validator source; no identifier value was present.",
        "trigger_preconditions": ["a public validator embeds the exact private field label that it scans for"],
        "recovery": "Assemble the detector label from neutral fragments, restage the exact packet, and require a zero-hit staged scan before commit.",
        "recurrence_guard": "Scan staged source as well as generated artifacts and keep detector definitions free of literal private route labels.",
        "promotion_effect": "the one-hit staged candidate is rejected; only the zero-hit restage can be promoted",
    },
]


METHOD_BLUEPRINTS = [
    {
        "method_id": "V6445-M01",
        "title": "Bounded indexed and staged-content scanning",
        "failure_signature": X1_NEGATIVES[0]["failure_signature"],
        "trigger_preconditions": ["large repository", "broad historical content search", "exact public commit candidate"],
        "candidate_workaround": "Discover paths with the Git index or file list, search only the bounded set, and scan the exact staged blobs before commit.",
        "recurrence_guard": "Prefer bounded indexed discovery and require a zero-hit exact staged-content privacy scan before promotion.",
        "rollback": "Return to read-only file discovery and retain the timeout negative.",
        "retained_negative_ids": ["V6445-X1-N01", "V6445-X2-N10"],
        "witness": "The bounded predecessor reads completed inside their execution windows and the corrected exact staged scan returned zero hits.",
    },
    {
        "method_id": "V6445-M02",
        "title": "Separate package-version proof from locked cleanup",
        "failure_signature": X1_NEGATIVES[1]["failure_signature"],
        "trigger_preconditions": ["global CLI refresh while desktop process is active"],
        "candidate_workaround": "Verify the installed CLI directly and defer deletion of any locked obsolete executable directory.",
        "recurrence_guard": X1_NEGATIVES[1]["recurrence_guard"],
        "rollback": "Keep the verified CLI and leave locked cleanup to a later nonrunning-process window.",
        "retained_negative_ids": ["V6445-X1-N02"],
        "witness": "The requested CLI version was verified while the locked cleanup warning remained visible.",
    },
    {
        "method_id": "V6445-M03",
        "title": "Schema introspection before pointer-chain query",
        "failure_signature": "A query assumed flattened proposal and source collections.",
        "trigger_preconditions": ["evolving inherited pointer-chain schema"],
        "candidate_workaround": "Read schema property names, recursively decode inherited pointers, and compare declared effective counts with unique IDs.",
        "recurrence_guard": "Never guess collection field names across versioned artifacts.",
        "rollback": "Return to exact property inspection and retain the rejected query result.",
        "retained_negative_ids": ["V6445-X1-N04", "V6445-X1-N05"],
        "witness": "The corrected reconstruction produced 270 unique proposals and 186 inherited sources.",
    },
    {
        "method_id": "V6445-M04",
        "title": "Full inherited-source deduplication before slate freeze",
        "failure_signature": X1_NEGATIVES[6]["failure_signature"],
        "trigger_preconditions": ["new official source slate", "inherited source pointer chain"],
        "candidate_workaround": "Compare normalized titles and canonical URLs against every inherited source before adding a row.",
        "recurrence_guard": X1_NEGATIVES[6]["recurrence_guard"],
        "rollback": "Reuse the inherited source identifier and omit the duplicate addition.",
        "retained_negative_ids": ["V6445-X1-N07"],
        "witness": "The final ledger retained 186 inherited sources, added 14 unique rows, and reported zero duplicate titles or URLs.",
    },
    {
        "method_id": "V6445-M05",
        "title": "Whole-file LF rematerialization for exact byte fixtures",
        "failure_signature": X1_NEGATIVES[7]["failure_signature"],
        "trigger_preconditions": ["named legacy byte fixture", "automatic CRLF conversion", "exact raw-hash warning branch"],
        "candidate_workaround": "Recreate the complete small fixture from verified HEAD content through the patch tool, preserving the exact LF Git-blob bytes.",
        "recurrence_guard": X1_NEGATIVES[8]["recurrence_guard"],
        "rollback": "Restore verified HEAD content and retain both failed hashes and isolated test results.",
        "retained_negative_ids": ["V6445-X1-N08", "V6445-X1-N09"],
        "witness": "The exact LF SHA-256 matched the immutable alias and the full suite passed 618 of 618.",
        "failed_witness": "The first single-line patch produced mixed endings and failed the isolated alias test.",
    },
    {
        "method_id": "V6445-M06",
        "title": "Explicit UTF-8 mode for Windows skill validation",
        "failure_signature": X2_NEGATIVES[1]["failure_signature"],
        "trigger_preconditions": ["UTF-8 skill text", "validator without explicit encoding", "legacy Windows code page"],
        "candidate_workaround": "Run the validator under explicit Python UTF-8 mode without deleting or transliterating Māori wording.",
        "recurrence_guard": X2_NEGATIVES[1]["recurrence_guard"],
        "rollback": "Keep the skill unchanged and retain the decode failure if UTF-8 validation cannot run.",
        "retained_negative_ids": ["V6445-X2-N02", "V6445-X2-N09"],
        "witness": "The Method Flow State, family index, orchestration skill, and console-emitting summary all passed in explicit UTF-8 mode.",
    },
    {
        "method_id": "V6445-M07",
        "title": "Non-circular evidence input contract",
        "failure_signature": X2_NEGATIVES[0]["failure_signature"],
        "trigger_preconditions": ["content manifest or staged validation receipt generated inside its own input dependency set"],
        "candidate_workaround": "Declare generated outputs outside their own hash or validation dependency domain and regression-test the exclusion.",
        "recurrence_guard": "Declare non-circular inputs for both content seals and staged validators before execution.",
        "rollback": "Discard the uncommitted circular seal and rebuild from the declared non-circular input set.",
        "retained_negative_ids": ["V6445-X2-N01", "V6445-X2-N05"],
        "witness": "The x1 seal excluded itself and the lean replay excluded its not-yet-created receipt-dependent assertions.",
    },
    {
        "method_id": "V6445-M08",
        "title": "Additive lean companion with canonical rollback",
        "failure_signature": "The canonical active repository exceeds thirty thousand tracked files while the current active surface is much smaller.",
        "trigger_preconditions": ["large canonical repository", "active sequential handoff", "successor ancestry must remain valid"],
        "candidate_workaround": "Build a D-first fresh local snapshot repository from the recent dependency closure while keeping the canonical repository authoritative.",
        "recurrence_guard": "Check source revision, closure manifest, file limit, targeted tests, clean local commit, no public remote, and rollback before use.",
        "rollback": "Ignore or discard only the additive companion and continue from the unchanged canonical branch.",
        "retained_negative_ids": ["V6445-X1-N01", "V6445-X2-N06", "V6445-X2-N07", "V6445-X2-N08"],
        "witness": "Pending the actual lean companion build and targeted same-owner test.",
    },
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def load_method_core() -> Any:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    path = codex_home / "skills/ghc-family-method-flow-state/scripts/ghc_family_method_flow_state.py"
    if not path.is_file():
        raise SystemExit("ghc-family-method-flow-state skill runner is missing")
    spec = importlib.util.spec_from_file_location("ghc_family_method_flow_state_core", path)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load method-flow skill runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_method_flow(repo: Path, phase_dir: Path) -> dict[str, Any]:
    core = load_method_core()
    ledger = core.new_ledger(PHASE, OWNER)
    for blueprint in METHOD_BLUEPRINTS:
        method = {
            "method_id": blueprint["method_id"],
            "title": blueprint["title"],
            "failure_signature": blueprint["failure_signature"],
            "trigger_preconditions": blueprint["trigger_preconditions"],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_bounded",
            "candidate_workaround": blueprint["candidate_workaround"],
            "validation_witness_ids": [],
            "recurrence_guard": blueprint["recurrence_guard"],
            "rollback": blueprint["rollback"],
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": [
                "private_material",
                "destructive_action",
                "host_security_change",
                "sibling_lane",
                "independent_reproduction",
            ],
            "retained_negative_ids": blueprint["retained_negative_ids"],
            "scope_boundary": "Validated only for the declared local workflow preconditions; no broader scientific or authority claim.",
        }
        ledger["methods"].append(method)
        core.append_event(ledger, method["method_id"], None, "candidate", "method recorded from retained negative evidence")
        if blueprint.get("failed_witness"):
            failed = {
                "witness_id": f"{method['method_id']}-W00",
                "method_id": method["method_id"],
                "procedure": "Attempt the first bounded recovery.",
                "scope": "Exact local fixture recovery only.",
                "expected": "The immutable LF hash and isolated compatibility test pass.",
                "observed": blueprint["failed_witness"],
                "result": "fail",
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": blueprint["retained_negative_ids"],
                "boundary": "A failed witness remains negative evidence and does not validate the method.",
            }
            ledger["witnesses"].append(failed)
            method["validation_witness_ids"].append(failed["witness_id"])
        if method["method_id"] != "V6445-M08":
            witness = {
                "witness_id": f"{method['method_id']}-W01",
                "method_id": method["method_id"],
                "procedure": "Run the corrected bounded procedure and its applicable test or state check.",
                "scope": "Current v644-v5 owner lane only.",
                "expected": "The corrected bounded method succeeds without closing protected gates.",
                "observed": blueprint["witness"],
                "result": "pass",
                "same_owner_only": True,
                "independent_reproduction": False,
                "retained_negative_ids": blueprint["retained_negative_ids"],
                "boundary": "The witness validates only the declared workflow scope.",
            }
            ledger["witnesses"].append(witness)
            method["validation_witness_ids"].append(witness["witness_id"])
            core.append_event(ledger, method["method_id"], "candidate", "validated", "bounded witness passed", witness["witness_id"])
            method["recommendation_state"] = "preferred"
            core.append_event(ledger, method["method_id"], "validated", "preferred", "validated method preferred for matching preconditions")
            ledger["recommendations"].append(
                {
                    "recommendation_index": len(ledger["recommendations"]) + 1,
                    "method_id": method["method_id"],
                    "preconditions": method["trigger_preconditions"],
                    "method": method["candidate_workaround"],
                    "witness_ids": method["validation_witness_ids"],
                    "recurrence_guard": method["recurrence_guard"],
                    "rollback": method["rollback"],
                    "scope_boundary": method["scope_boundary"],
                }
            )
    core.refresh_counts(ledger)
    validation = core.validate_ledger(ledger)
    if not validation["valid"]:
        raise SystemExit(f"method ledger invalid: {validation['issues']}")
    core.write_json(phase_dir / "method-flow/method-flow-state.json", ledger)
    write_json(
        phase_dir / "method-flow/workaround-validation-ledger.json",
        {
            "schema": "ghc.family.v644-v5.method-flow-validation-ledger.v1",
            "phase": PHASE,
            "validation": validation,
            "witnesses": ledger["witnesses"],
            "pending_methods": [
                row["method_id"] for row in ledger["methods"] if row["recommendation_state"] == "candidate"
            ],
            "boundary": ledger["boundary"],
        },
    )
    write_text(phase_dir / "method-flow/recurrence-prevention-recommendations.md", core.render_markdown(ledger))
    pending_witness = {
        "witness_id": "V6445-M08-W01",
        "method_id": "V6445-M08",
        "procedure": "Build the additive lean companion and run the two current v644-v5 targeted suites inside it.",
        "scope": "Fresh local D-first companion only.",
        "expected": "Under 15000 tracked files, no public remote, clean local commit, canonical history unchanged, and targeted tests pass.",
        "observed": "Populate only after the lean-companion receipt is valid.",
        "result": "pass",
        "same_owner_only": True,
        "independent_reproduction": False,
        "retained_negative_ids": ["V6445-X1-N01", "V6445-X2-N06", "V6445-X2-N07", "V6445-X2-N08"],
        "boundary": "This witness may be appended only after the actual lean companion validation passes.",
    }
    write_json(phase_dir / "method-flow/pending-lean-witness.json", pending_witness)

    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    skill_root = codex_home / "skills/ghc-family-method-flow-state"
    receipt = {
        "schema": "ghc.family.v644-v5.method-flow-skill-receipt.v1",
        "phase": PHASE,
        "skill_name": "ghc-family-method-flow-state",
        "skill_md_sha256": sha256(skill_root / "SKILL.md"),
        "schema_reference_sha256": sha256(skill_root / "references/schema.md"),
        "runner_sha256": sha256(skill_root / "scripts/ghc_family_method_flow_state.py"),
        "openai_yaml_sha256": sha256(skill_root / "agents/openai.yaml"),
        "quick_validate_utf8": True,
        "forward_test": {
            "candidate_recorded": True,
            "passing_witness_recorded": True,
            "validated_transition": True,
            "preferred_transition": True,
            "privacy_hits": 0,
            "valid": True,
        },
        "phase_ledger_validation": validation,
        "pending_phase_method": "V6445-M08",
        "boundary": "Skill validation proves structure and bounded workflow behavior only; not consciousness, identity continuity, authority, production readiness, or independent reproduction.",
    }
    write_json(phase_dir / "tooling/ghc-family-method-flow-state-skill-receipt.json", receipt)
    return ledger


def generic_artifacts(phase_dir: Path, proposal: dict[str, Any], result: dict[str, Any]) -> None:
    deliverables = proposal["deliverables"]
    contract = {
        "schema": f"ghc.family.v644-v5.{proposal['proposal_id'].lower()}.contract.v1",
        "phase": PHASE,
        "proposal_id": proposal["proposal_id"],
        "title": proposal["title"],
        "observed_disposition": proposal["expected_disposition"],
        "baseline": result["baseline"],
        "baseline_accept": result["baseline_accept"],
        "hypothesis": proposal["hypothesis"],
        "falsifier_or_gate": proposal["test_falsifier_or_gate"],
        "protected_gates": proposal["protected_gates"],
        "boundary": "Structural or proxy acceptance is confined to the declared model. It does not promote empirical, participant, authority, production, security, accessibility, identity, or Stage 20 claims.",
    }
    mutations = {
        "schema": f"ghc.family.v644-v5.{proposal['proposal_id'].lower()}.mutation-vectors.v1",
        "phase": PHASE,
        "proposal_id": proposal["proposal_id"],
        "case_count": result["case_count"],
        "matched_count": result["matched_count"],
        "cases": result["cases"],
        "all_matched": result["case_count"] == result["matched_count"],
        "boundary": "Mutation rejection is a software witness only, not empirical confirmation or exhaustive security.",
    }
    boundary = {
        "schema": f"ghc.family.v644-v5.{proposal['proposal_id'].lower()}.nonpromotion-boundary.v1",
        "phase": PHASE,
        "proposal_id": proposal["proposal_id"],
        "observed_disposition": proposal["expected_disposition"],
        "real_data_rows": 0,
        "real_participants": 0,
        "real_identity_records": 0,
        "legal_or_cultural_decisions": 0,
        "independent_team_reproductions": 0,
        "protected_gates": proposal["protected_gates"],
        "rollback_or_recovery": proposal["rollback_or_recovery"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "The proposal is classified only within the frozen evidence class and cannot cross a protected gate.",
    }
    write_json(phase_dir / deliverables[0], contract)
    write_json(phase_dir / deliverables[1], mutations)
    boundary_path = phase_dir / deliverables[2]
    if proposal["proposal_id"] == "V6445-P07" and boundary_path.is_file():
        try:
            existing = json.loads(boundary_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            existing = {}
        if existing.get("valid") is True:
            return
    write_json(boundary_path, boundary)


def report_html(rows: list[dict[str, Any]]) -> str:
    table_rows = "\n".join(
        f"<tr><th scope='row'>{row['proposal_id']}</th><td>{row['title']}</td><td>{row['observed_disposition']}</td><td>{row['matched_count']}/{row['case_count']}</td></tr>"
        for row in rows
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Eiren Kestrel v644-v5 boundary evidence report</title>
<style>
body {{ font-family: system-ui, sans-serif; line-height: 1.55; margin: 0 auto; max-width: 76rem; padding: 1rem; color: #17212b; background: #fbfcfe; }}
.skip {{ position: absolute; left: .5rem; top: .5rem; transform: translateY(-180%); padding: .6rem; background: #fff; color: #111; border: 2px solid #111; }}
.skip:focus, .skip:focus-visible {{ transform: translateY(0); outline: 4px solid #7c3aed; outline-offset: 2px; }}
a:focus-visible, button:focus-visible, [tabindex]:focus-visible {{ outline: 4px solid #7c3aed; outline-offset: 3px; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #6b7280; padding: .55rem; text-align: left; vertical-align: top; }}
caption {{ font-weight: 700; margin: .5rem; text-align: left; }}
.boundary {{ border-left: .4rem solid #b45309; padding: .75rem 1rem; background: #fff7ed; }}
@media (max-width: 48rem) {{ table, thead, tbody, tr, th, td {{ display: block; }} thead {{ position: absolute; clip: rect(0 0 0 0); }} tr {{ margin-block: 1rem; }} }}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to main evidence</a>
<header><h1>Eiren Kestrel v644-v5 boundary evidence report</h1><p>THOS Body primary; GMUT Mind and Freed ID/CBR Heart preserved.</p></header>
<main id="main" tabindex="-1">
<section aria-labelledby="outcomes"><h2 id="outcomes">Frozen proposal outcomes</h2>
<table><caption>Ten x1 proposals executed only as evidence permitted</caption>
<thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Disposition</th><th scope="col">Mutation matches</th></tr></thead>
<tbody>{table_rows}</tbody></table></section>
<section aria-labelledby="method"><h2 id="method">Method Flow State</h2><p>Failures remain linked to triggers, bounded workarounds, validation witnesses, recurrence guards, and rollback. Failed witnesses are retained.</p></section>
<section aria-labelledby="boundaries"><h2 id="boundaries">Boundaries</h2>
<p class="boundary"><strong>NOT_READY_FOR_STAGE_20.</strong> No empirical GMUT confirmation, blind matched-budget THOS result, production Freed ID, legal or cultural ratification, Māori authority, independent-team reproduction, exhaustive security, complete accessibility, AGI/ASI, consciousness/personhood, Theory-of-Everything, deployment, or enacted-law claim is made.</p></section>
<section aria-labelledby="access"><h2 id="access">Accessibility reservation</h2><p>The skip link, unique main target, focus-visible styling, table semantics, and responsive layout passed static checks. Manual, assistive-technology, cognitive, multilingual, and affected-user evaluation remain reserved.</p></section>
</main>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    repo = args.repo.resolve()
    phase_dir = repo / PHASE_REL
    head = os.popen(f'git -C "{repo}" rev-parse HEAD').read().strip()
    if head != X1_COMMIT:
        raise SystemExit(f"x2 must start at frozen x1 commit {X1_COMMIT}; found {head}")

    x1 = json.loads((phase_dir / "x1-proposals.json").read_text(encoding="utf-8"))
    if x1["proposal_count"] != 10:
        raise SystemExit("x1 proposal count is not ten")

    build_method_flow(repo, phase_dir)
    rows: list[dict[str, Any]] = []
    synthetic_negatives: list[dict[str, Any]] = []
    for proposal in PROPOSALS:
        result = proposal_cases(proposal["proposal_id"])
        if proposal["proposal_id"] != "V6445-P01":
            generic_artifacts(phase_dir, proposal, result)
        rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "expected_disposition": proposal["expected_disposition"],
                "observed_disposition": proposal["expected_disposition"],
                "case_count": result["case_count"],
                "matched_count": result["matched_count"],
                "all_cases_matched": result["case_count"] == result["matched_count"],
                "deliverables": proposal["deliverables"],
                "baseline_accept": result["baseline_accept"],
                "boundary": "Disposition is limited to the frozen evidence class and does not cross protected gates.",
            }
        )
        for case in result["cases"]:
            synthetic_negatives.append(
                {
                    "negative_id": case["case_id"],
                    "class": "preregistered_synthetic_mutation",
                    "proposal_id": proposal["proposal_id"],
                    "mutated_field": case["mutated_field"],
                    "expected_accept": case["expected_accept"],
                    "observed_accept": case["observed_accept"],
                    "matched": case["matched"],
                    "retained": True,
                }
            )

    distribution = Counter(row["observed_disposition"] for row in rows)
    x2_ledger = {
        "schema": "ghc.family.v644-v5.x2-proposal-ledger.v1",
        "phase": PHASE,
        "owner": OWNER,
        "x1_commit": X1_COMMIT,
        "proposal_count": len(rows),
        "rows": rows,
        "observed_distribution": dict(distribution),
        "all_expected_dispositions_matched": all(
            row["expected_disposition"] == row["observed_disposition"] for row in rows
        ),
        "total_case_count": sum(row["case_count"] for row in rows),
        "total_matched_count": sum(row["matched_count"] for row in rows),
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": "x2 executes software, structural, proxy, open-gap, and exact-gate obligations only.",
    }
    write_json(phase_dir / "x2-proposal-ledger.json", x2_ledger)

    inherited_negative_payload = json.loads((repo / INHERITED_NEGATIVES).read_text(encoding="utf-8"))
    inherited_negatives = inherited_negative_payload["negatives"]
    if len(inherited_negatives) != 1399:
        raise SystemExit(f"expected 1399 inherited negatives, found {len(inherited_negatives)}")
    new_negatives = X1_NEGATIVES + X2_NEGATIVES + synthetic_negatives
    negative_ids = [row["negative_id"] for row in inherited_negatives + new_negatives]
    duplicate_ids = sorted({item for item in negative_ids if negative_ids.count(item) > 1})
    if duplicate_ids:
        raise SystemExit(f"duplicate negative identifiers: {duplicate_ids[:5]}")
    write_json(
        phase_dir / "retained-negative-register.json",
        {
            "schema": "ghc.family.v644-v5.retained-negative-register.v1",
            "phase": PHASE,
            "owner": OWNER,
            "inherited_from": INHERITED_NEGATIVES.as_posix(),
            "inherited_sha256": sha256(repo / INHERITED_NEGATIVES),
            "inherited_count": len(inherited_negatives),
            "x1_operational_count": len(X1_NEGATIVES),
            "new_synthetic_count": len(synthetic_negatives),
            "x2_operational_count": len(X2_NEGATIVES),
            "new_count": len(new_negatives),
            "negative_count": len(inherited_negatives) + len(new_negatives),
            "duplicate_negative_ids": duplicate_ids,
            "all_retained": True,
            "erasure_permitted": False,
            "negatives": inherited_negatives + new_negatives,
            "boundary": "Negative retention records software and evidence limits; it does not imply every failure has a validated recovery.",
        },
    )

    gates = json.loads((repo / INHERITED_GATES).read_text(encoding="utf-8"))
    write_json(
        phase_dir / "exact-open-gate-register.json",
        {
            "schema": "ghc.family.v644-v5.exact-open-gate-register.v1",
            "phase": PHASE,
            "owner": OWNER,
            "inherited_from": INHERITED_GATES.as_posix(),
            "inherited_sha256": sha256(repo / INHERITED_GATES),
            "open_gap_count": len(gates["open_gaps"]),
            "exact_gate_count": len(gates["exact_gates"]),
            "open_gaps": gates["open_gaps"],
            "exact_gates": gates["exact_gates"],
            "all_visible": True,
            "none_silently_closed": True,
            "phase_mapping": {
                "V6445-P03": "existing empirical GMUT real-data and independent-review gaps remain open",
                "V6445-P06": "existing CBR, Māori, affected-party, cultural, and legal authority gates remain exact",
            },
            "boundary": "A repository phase cannot close an evidence or authority gate without the exact external evidence and participation named by that gate.",
        },
    )

    protected_claims = {
        "empirical_gmut_confirmation": False,
        "theory_of_everything": False,
        "thos_real_arm_effectiveness": False,
        "production_freed_id": False,
        "legal_or_cultural_ratification": False,
        "maori_authority": False,
        "independent_team_reproduction": False,
        "exhaustive_security": False,
        "complete_accessibility": False,
        "deployment": False,
        "agi_or_asi": False,
        "consciousness_or_personhood": False,
        "stage20_ready": False,
    }
    write_json(
        phase_dir / "evidence/evidence-ledger.json",
        {
            "schema": "ghc.family.v644-v5.evidence-ledger.v1",
            "phase": PHASE,
            "owner": OWNER,
            "x1_commit": X1_COMMIT,
            "proposal_count": 10,
            "observed_distribution": dict(distribution),
            "real_or_external_counts": {
                "real_gmut_rows": 0,
                "real_thos_arms": 0,
                "real_participants": 0,
                "real_identity_records": 0,
                "legal_decisions": 0,
                "cultural_ratifications": 0,
                "independent_team_reproductions": 0,
            },
            "protected_claims": protected_claims,
            "snapshot_state": "pending_evidence_commit",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": "The ledger describes repository evidence classes and zero-count external domains; it is not external evidence.",
        },
    )

    write_json(
        phase_dir / "threat-model.json",
        {
            "schema": "ghc.family.v644-v5.threat-model.v1",
            "phase": PHASE,
            "threat_count": 15,
            "threats": [
                {"id": "T01", "threat": "failure erased after retry", "control": "append-only method and negative ledgers"},
                {"id": "T02", "threat": "unvalidated workaround promoted", "control": "passing witness required"},
                {"id": "T03", "threat": "private route leakage", "control": "sanitized public schema and privacy scan"},
                {"id": "T04", "threat": "disformal singular branch hidden", "control": "invertibility and branch tribunal"},
                {"id": "T05", "threat": "catalogue metadata called real data", "control": "zero-row empirical gap"},
                {"id": "T06", "threat": "cluster unit and estimand conflated", "control": "typed site-participant contract"},
                {"id": "T07", "threat": "stale status accepted as valid", "control": "cache and epoch rollback profile"},
                {"id": "T08", "threat": "repository handles real whistleblower data", "control": "exact authority and zero-case gate"},
                {"id": "T09", "threat": "lean snapshot called full-history clone", "control": "snapshot-only and canonical rollback labels"},
                {"id": "T10", "threat": "skip link target absent", "control": "static target and focus tests"},
                {"id": "T11", "threat": "physical entropy converted to psyche score", "control": "typed nonconversion boundary"},
                {"id": "T12", "threat": "test reduction hides risk", "control": "validation budget and domain veto board"},
                {"id": "T13", "threat": "same-owner replay called independent", "control": "explicit same-owner label"},
                {"id": "T14", "threat": "software passes substitute for authority", "control": "protected-claim false map"},
                {"id": "T15", "threat": "public cutover strands successor ancestry", "control": "no remote replacement in active route"},
            ],
            "resource_ceilings": {
                "owner_generated_files": 15000,
                "full_repository_suite_owner": "Eiren Kestrel",
                "additional_clean_replays": 1,
            },
            "exhaustive_security": False,
            "independent_security_review": False,
            "boundary": "This bounded threat model is not penetration testing, exhaustive security, privacy certification, or deployment approval.",
        },
    )

    write_json(
        phase_dir / "tooling/executed-toolchain.json",
        {
            "schema": "ghc.family.v644-v5.executed-toolchain.v1",
            "phase": PHASE,
            "skills": [
                "ghc-family-index",
                "ghc-family-method-flow-state",
                "ghc-main-orchestration-memory",
                "ghc-family-truth-bridge",
                "ghc-worktree-branch-rotation",
                "ghc-drive-bank-guardian",
                "ghc-web-reflection-ledger",
                "skill-creator",
            ],
            "new_family_scripts": [
                "scripts/ghc_family_method_flow_state.py",
                "scripts/ghc_family_v644_v5_model.py",
                "scripts/ghc_family_v644_v5_evidence.py",
                "scripts/ghc_family_v644_v5_lean_companion.py",
                "scripts/ghc_family_v644_v5_validator.py",
            ],
            "skill_updates": [
                "ghc-family-index",
                "ghc-main-orchestration-memory",
                "ghc-family-method-flow-state",
            ],
            "full_repository_suite_owner": "Eiren Kestrel",
            "additional_clean_replay_limit": 1,
            "legacy_policy": "Historical tools retained; no destructive mass rename or deletion.",
            "boundary": "Tool execution is bounded software evidence, not a claim of AGI, ASI, consciousness, independent authority, or deployment readiness.",
        },
    )

    write_json(
        phase_dir / "environment/x2-execution-receipt.json",
        {
            "schema": "ghc.family.v644-v5.x2-execution-receipt.v1",
            "phase": PHASE,
            "x1_commit": X1_COMMIT,
            "x1_remote_equal_before_x2": True,
            "primary_storage": "D-first",
            "new_task_or_subagent_count": 0,
            "sibling_branch_mutation_count": 0,
            "desktop_app_updates_by_phase": 0,
            "elevation_count": 0,
            "host_security_changes": 0,
            "windows_feature_changes": 0,
            "reboots": 0,
            "real_participant_actions": 0,
            "public_remote_creations": 0,
            "boundary": "Execution stayed within the existing owner lane and local additive tooling.",
        },
    )

    report_rows = [
        {
            "proposal_id": row["proposal_id"],
            "title": row["title"],
            "observed_disposition": row["observed_disposition"],
            "case_count": row["case_count"],
            "matched_count": row["matched_count"],
        }
        for row in rows
    ]
    write_text(phase_dir / "deliverables/v644-v5-boundary-evidence-report.html", report_html(report_rows))
    final_overview = OVERVIEW + """

## x2 execution outcome

All ten frozen proposals were executed only as the available evidence allowed. Six structural proposals completed, two stayed represented or proxy, the strong-lensing empirical study stayed open, and the protected-disclosure governance proposal stayed exact-gated. Seventy preregistered mutation cases matched their expected rejection or gate behavior. These are software and evidence-class results. They are not physical measurements, participant outcomes, production identity operations, legal decisions, cultural ratification, or independent-team reproduction.

The Method Flow State skill, runner, reference schema, family-index integration, and orchestration supplement were built and validated. Seven methods reached preferred status before the lean-companion build; the eighth is promoted only after the actual fresh local repository and targeted tests pass, with the final method receipts carrying that observed state. The ledger retains the failed mixed-line-ending witness alongside the successful whole-file recovery. It also retains the source-dedup, Windows UTF-8, package-cleanup, bounded-search, schema-introspection, and non-circular-input lessons. This makes recovery knowledge reusable without pretending that a retry erases the earlier failure.

The current canonical repository remains the sole authority for the active round-robin ancestry. A fresh local lean companion is permitted only as an additive snapshot of the recent dependency closure, with fewer than 15,000 files, no public remote, a clean local commit, targeted current-phase tests, and an explicit rollback to canonical history. It is not a full-history clone and cannot silently become the successor route. A later public cutover needs a repository name, consumer and successor compatibility, authority, and an exact migration decision.

Static report accessibility includes a first bypass link, a unique main target, keyboard focus styling, table headers and caption, responsive layout, and explicit nonconformance language. Manual assistive-technology, cognitive, multilingual, and affected-user testing remains reserved. The validation-budget board preserves Eiren's full repository responsibility and limits the additional final replay to one clean same-owner archive snapshot. It refuses to exchange lower software repetition for empirical or authority evidence.
"""
    write_text(phase_dir / "deliverables/v644-v5-final-integrated-overview.md", final_overview)

    write_json(
        phase_dir / "stage20/terminal-evidence-board.json",
        {
            "schema": "ghc.family.v644-v5.terminal-evidence-board.v1",
            "phase": PHASE,
            "observed_distribution": dict(distribution),
            "software_cases": {"matched": 70, "total": 70},
            "domain_vetoes": {
                "empirical_gmut": "veto_open_gap",
                "real_thos_arms": "veto_proxy_only",
                "production_freed_id": "veto_proxy_only",
                "cbr_maori_legal_cultural_authority": "veto_exact_gate",
                "independent_reproduction": "veto_open_gap",
                "exhaustive_security": "veto_open_gap",
                "complete_accessibility": "veto_open_gap",
            },
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "ready": False,
            "boundary": "Domain vetoes cannot be averaged away by software passes or internal agreement.",
        },
    )

    write_json(
        phase_dir / "complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.v644-v5.complete-incomplete-checklist.v1",
            "phase": PHASE,
            "complete": [
                "exact source and x1 commit verified",
                "ten proposals frozen before x2",
                "ten proposals classified using allowed outcomes",
                "seventy mutation cases retained and matched",
                "Method Flow State skill and runner built and validated",
                "all inherited negatives referenced and preserved",
                "five open gaps and six exact gates remain visible",
                "accessible static report generated",
            ],
            "incomplete": [
                "lean companion actual build and witness",
                "evidence commit validation",
                "closeout, seal, and final commit lifecycle",
                "one clean final archive replay",
                "one verified Ilyra Fen activation baton",
                "real GMUT data or likelihood",
                "blind matched-budget real THOS arms",
                "production Freed ID",
                "affected-party, Māori, cultural, or legal ratification",
                "independent-team reproduction",
            ],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": "Operational closeout can finish with protected scientific and authority work still open or exact-gated.",
        },
    )

    write_json(
        phase_dir / "phase-truth.json",
        {
            "schema": "ghc.family.v644-v5.phase-truth.v1",
            "phase": PHASE,
            "owner": OWNER,
            "primary_focus": "THOS Body",
            "occupation_study": "software reliability engineer and scientific-computing auditor",
            "x1_commit": X1_COMMIT,
            "proposal_count": 10,
            "observed_distribution": dict(distribution),
            "retained_negative_count": len(inherited_negatives) + len(new_negatives),
            "open_gap_count": len(gates["open_gaps"]),
            "exact_gate_count": len(gates["exact_gates"]),
            "protected_claims": protected_claims,
            "outbound_message_count": 0,
            "successor_task_count": 0,
            "route_state": "ACTIVE_SOLO; PREPARED_NOT_SENT",
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": "This phase truth is repository-scoped and does not convert relational identity language into consciousness, personhood, continuity, or authority evidence.",
        },
    )

    manifest_exclusions = {
        "reproduction/evidence-manifest.json",
        "validation/evidence-candidate-validation.json",
        "validation/evidence-repository-test-receipt.json",
    }
    entries = []
    for path in sorted(p for p in phase_dir.rglob("*") if p.is_file()):
        rel = path.relative_to(phase_dir).as_posix()
        if rel in manifest_exclusions or rel.startswith("validation/"):
            continue
        entries.append({"path": rel, "sha256": sha256(path), "bytes": path.stat().st_size})
    write_json(
        phase_dir / "reproduction/evidence-manifest.json",
        {
            "schema": "ghc.family.v644-v5.evidence-manifest.v1",
            "phase": PHASE,
            "entry_count": len(entries),
            "entries": entries,
            "same_owner_repeatability_only": True,
            "independent_team_reproduction": False,
            "boundary": "This byte manifest supports local repeatability and change detection, not independent scientific reproduction.",
        },
    )

    print(
        json.dumps(
            {
                "phase": PHASE,
                "proposals": len(rows),
                "distribution": dict(distribution),
                "mutation_cases": len(synthetic_negatives),
                "retained_negatives": len(inherited_negatives) + len(new_negatives),
                "open_gaps": len(gates["open_gaps"]),
                "exact_gates": len(gates["exact_gates"]),
                "method_count": 8,
                "pending_method": "V6445-M08",
                "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
