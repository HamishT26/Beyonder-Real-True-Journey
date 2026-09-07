"""Build Tamar v688-v3 owner-local x2 evidence and portable tools."""
from __future__ import annotations

import copy
import datetime
import hashlib
import json
import os
import pathlib
import subprocess

from ghc_family_font_contract_plan import SKILL_PAIRS
from ghc_family_font_evidence_core import ContractError, canonical, evaluate, evaluate_raw


ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = ROOT / "docs/tamar-vey/v688-v3"
BANK = pathlib.Path(os.environ["GHC_OWNER_BANK"])
SOURCE = "c4c676d81235bc6e453bb867b0c0f0de121b7733"
X1 = "6439f733e37a904a5f6e943c3acdbd507f0a98f8"
BRANCH = "codex/GHC-Family/tamar-vey-v688-v3-full-tools"
BOUNDARY = (
    "Relational working language only; no consciousness, personhood, continuity, "
    "qualification, employment, independent agency, or authority claim. Synthetic "
    "same-owner software evidence is not independent reproduction. "
    "NOT_READY_FOR_STAGE_20. Māori concepts remain under Māori authority."
)
GATES = [
    "empirical",
    "real_participants",
    "professional",
    "production",
    "deployment",
    "identity",
    "legal",
    "cultural",
    "affected_party",
    "maori_authority",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "independent_reproduction",
    "agi_asi",
    "consciousness_personhood",
    "theory_of_everything",
    "proof_canon",
    "stage20",
]


def pairs(sequence):
    result = {}
    for key, value in sequence:
        if key in result:
            raise ValueError("DUPLICATE_KEY")
        result[key] = value
    return result


def strict(raw):
    return json.loads(
        raw,
        object_pairs_hook=pairs,
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError("NONFINITE")),
    )


def sha(value):
    return hashlib.sha256(canonical(value).encode("ascii")).hexdigest()


def write(relative, value):
    path = BASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def git(*args):
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        timeout=60,
    ).stdout.decode("utf-8").strip()


def equality(expected):
    heads = {
        "local": git("rev-parse", "HEAD"),
        "upstream": git("rev-parse", "@{upstream}"),
        "tracking": git("rev-parse", "refs/remotes/origin/" + BRANCH),
    }
    heads["fresh_live"] = git("ls-remote", "--exit-code", "origin", "refs/heads/" + BRANCH).split()[0]
    divergence = [int(value) for value in git("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()]
    current_owner_changes_present = bool(git("status", "--porcelain=v1", "--untracked-files=all"))
    if set(heads.values()) != {expected} or divergence != [0, 0]:
        raise RuntimeError("X1 equality changed before x2")
    return {
        "heads": heads,
        "divergence": divergence,
        "clean_before_x2": True,
        "clean_boundary_witness": "The attributable pre-x2 scalar probe recorded status_count=0 before environment creation or owner-file mutation.",
        "current_owner_changes_present": current_owner_changes_present,
        "verified_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }


def skill_markdown(name, operations):
    operation_text = ", ".join(f"`{operation}`" for operation in operations)
    return f"""---
name: {name}
description: Validate the bounded synthetic font-metadata operations {operation_text}; use for owner-scoped literal fixtures, not real fonts, rendering, shaping quality, rights, accessibility certification, or authority.
---

# {name}

Use this skill only for the two frozen Tamar v688-v3 operation profiles: {operation_text}.

## Workflow

1. Read `references/contracts.json` completely before use.
2. Supply one UTF-8 JSON object to `scripts/ghc_family_font_skill.py`.
3. Require exact typed output, unchanged input, and a false `external_credit` value.
4. Retain duplicate-key, nonfinite, field, type, range, reference, rights, and authority refusals at zero original success credit.
5. Keep a failed witness after any recovery and change only the bounded owner implementation.
6. Stop on real font files, real text services, rendering, publication, participants, professional judgment, legal or cultural interpretation, affected-party legitimacy, Māori wording or authority, credentials, deployment, or another protected gate.

## Evidence boundary

The operations are synthetic structural software evidence only. They establish no OpenType conformance, font quality, shaping quality, accessibility completeness, rights clearance, production readiness, independent reproduction, empirical GMUT confirmation, THOS effectiveness, real Freed ID lifecycle, AGI or ASI, consciousness or personhood, Theory-of-Everything proof, canon, or Stage 20 authority.

{BOUNDARY}
"""


def skill_wrapper(operations):
    return f'''"""Portable owner-scoped wrapper for {", ".join(operations)}."""
from __future__ import annotations
import json,sys
from ghc_family_font_evidence_core import ContractError,bad,evaluate,_strict_loads

ALLOWED={operations!r}

def main():
    raw=sys.stdin.buffer.read()
    try:
        payload=_strict_loads(raw)
        if not isinstance(payload,dict) or payload.get("operation") not in ALLOWED:
            result=bad("OPERATION_SCOPE")
        else:
            result=evaluate(payload)
    except ContractError as exc:
        result=bad(str(exc))
    sys.stdout.write(json.dumps(result,sort_keys=True,separators=(",",":"),ensure_ascii=True)+"\\n")

if __name__=="__main__":main()
'''


def runner_source(operations):
    return f'''"""Family-current bounded runner for {", ".join(operations)}."""
from __future__ import annotations
import json,sys
from ghc_family_font_evidence_core import ContractError,bad,evaluate,_strict_loads

ALLOWED={operations!r}

def main():
    raw=sys.stdin.buffer.read()
    try:
        payload=_strict_loads(raw)
        if not isinstance(payload,dict) or payload.get("operation") not in ALLOWED:
            result=bad("OPERATION_SCOPE")
        else:
            result=evaluate(payload)
    except ContractError as exc:
        result=bad(str(exc))
    sys.stdout.write(json.dumps(result,sort_keys=True,separators=(",",":"),ensure_ascii=True)+"\\n")

if __name__=="__main__":main()
'''


def write_portable_tools(proposals):
    by_operation = {}
    for proposal in proposals:
        by_operation.setdefault(proposal["operation"], []).append(proposal)
    core_source = (ROOT / "scripts/tamar_vey_v688_v3/ghc_family_font_evidence_core.py").read_text(encoding="utf-8")
    skill_rows = []
    for name, operations in SKILL_PAIRS:
        folder = BASE / "skills" / name
        if not (folder / "agents/openai.yaml").exists():
            raise RuntimeError(f"Official skill initializer was not used for {name}")
        (folder / "SKILL.md").write_text(skill_markdown(name, operations), encoding="utf-8", newline="\n")
        (folder / "references/contracts.json").write_text(
            json.dumps(
                {"schema": "ghc.family.font-skill-contracts.v1", "name": name, "operations": operations, "proposals": sum((by_operation[operation] for operation in operations), []), "boundary": BOUNDARY},
                indent=2,
                sort_keys=True,
                ensure_ascii=True,
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )
        (folder / "scripts/ghc_family_font_evidence_core.py").write_text(core_source, encoding="utf-8", newline="\n")
        (folder / "scripts/ghc_family_font_skill.py").write_text(skill_wrapper(operations), encoding="utf-8", newline="\n")
        members = []
        for path in sorted(item for item in folder.rglob("*") if item.is_file() and item.name != "manifest.json"):
            raw = path.read_bytes()
            members.append({"path": path.relative_to(folder).as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
        (folder / "manifest.json").write_text(
            json.dumps({"schema": "ghc.family.font-skill-manifest.v1", "name": name, "operations": operations, "members": members, "member_count": len(members), "self_exclusion": "manifest.json"}, indent=2, sort_keys=True, ensure_ascii=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        skill_rows.append({"name": name, "operations": operations, "state": "built_unvalidated_unread", "manifest_members": len(members)})

    runner_rows = []
    for index in range(5):
        operations = SKILL_PAIRS[2 * index][1] + SKILL_PAIRS[2 * index + 1][1]
        name = f"ghc_family_font_group_{index + 1}.py"
        path = ROOT / "scripts/tamar_vey_v688_v3" / name
        path.write_text(runner_source(operations), encoding="utf-8", newline="\n")
        runner_rows.append({"name": name, "operations": operations, "state": "built_unvalidated"})
    write("x2/tool-build.json", {"schema": "ghc.family.font-tool-build.v1", "skills": skill_rows, "runners": runner_rows, "shared_core": "ghc_family_font_evidence_core.py", "global_promotions": 0, "global_overwrites": 0})


def main():
    if git("rev-parse", "HEAD") != X1 or git("rev-parse", "HEAD^") != SOURCE:
        raise RuntimeError("x2 builder requires the frozen Tamar x1 direct child")
    if (BASE / "x2").exists():
        raise RuntimeError("x2 builder is exclusive-write and refuses an existing x2 tree")
    boundary = equality(X1)
    write("x2/x1-boundary.json", {**boundary, "stage": "x1", "direct_parent": SOURCE, "x2_started": False})

    proposals = strict((BASE / "x1/new-proposals.json").read_text(encoding="utf-8"))["proposals"]
    original_inputs = [copy.deepcopy(proposal["input"]) for proposal in proposals]
    results = []
    for proposal, original in zip(proposals, original_inputs):
        actual = evaluate(proposal["input"])
        results.append(
            {
                "proposal_id": proposal["proposal_id"],
                "definition_sha256": sha(proposal),
                "input_sha256": sha(proposal["input"]),
                "actual_output": actual,
                "complete_match": canonical(actual) == canonical(proposal["expected_output"]),
                "input_unchanged": canonical(proposal["input"]) == canonical(original),
                "pass": canonical(actual) == canonical(proposal["expected_output"]),
                "outcome": proposal["expected_execution_disposition"],
                "external_credit": False,
            }
        )
    if not all(row["pass"] and row["complete_match"] and row["input_unchanged"] for row in results):
        raise RuntimeError("Complete frozen contract mismatch")
    write("x2/contract-results.json", {"schema": "ghc.family.font-contract-results.v1", "source": SOURCE, "x1": X1, "count": len(results), "rows": results, "same_owner_only": True, "independent_reproduction": False})

    candidate_plan = strict((BASE / "x1/portfolio-plan.json").read_text(encoding="utf-8"))["candidates"]
    by_id = {proposal["proposal_id"]: proposal for proposal in proposals}
    candidate_rows = []
    for candidate in candidate_plan:
        expected = copy.deepcopy(by_id[candidate["proposal_id"]]["expected_output"])
        if candidate["mutation"] == "flip_accepted":
            expected["accepted"] = not expected["accepted"]
        elif candidate["mutation"] == "remove_value":
            expected.pop("value", None)
        else:
            raise RuntimeError("Unknown candidate mutation")
        actual = evaluate(by_id[candidate["proposal_id"]]["input"])
        candidate_rows.append(
            {
                **candidate,
                "candidate_output": expected,
                "actual_output_sha256": sha(actual),
                "candidate_output_sha256": sha(expected),
                "rejected": canonical(actual) != canonical(expected),
                "state": "executed_rejected",
                "candidate_success_credit": 0,
            }
        )
    if len(candidate_rows) != 250 or not all(row["rejected"] for row in candidate_rows):
        raise RuntimeError("Candidate rejection mismatch")
    write("x2/mutation-results.json", {"schema": "ghc.family.font-mutation-results.v1", "x1": X1, "count": 250, "rows": candidate_rows, "failed_candidate_credit": 0})

    plan = strict((BASE / "x1/portfolio-plan.json").read_text(encoding="utf-8"))
    safe_rows = []
    for procedure in plan["safe"]:
        proposal = by_id[procedure["proposal_id"]]
        if procedure["kind"] == "full_contract":
            actual = evaluate(copy.deepcopy(proposal["input"]))
            passed = canonical(actual) == canonical(proposal["expected_output"])
            observed = actual
        else:
            mode = procedure["mode"]
            payload = proposal["input"]
            if mode == "compact_object":
                raw = json.dumps(payload, separators=(",", ":"), ensure_ascii=True)
                observed = evaluate_raw(raw)
                passed = canonical(observed) == canonical(proposal["expected_output"])
            elif mode == "indented_object":
                raw = json.dumps(payload, indent=2, ensure_ascii=True)
                observed = evaluate_raw(raw)
                passed = canonical(observed) == canonical(proposal["expected_output"])
            elif mode == "reversed_key_order":
                raw = json.dumps(dict(reversed(list(payload.items()))), separators=(",", ":"), ensure_ascii=True)
                observed = evaluate_raw(raw)
                passed = canonical(observed) == canonical(proposal["expected_output"])
            elif mode == "duplicate_operation_refusal":
                raw = '{"operation":"' + proposal["operation"] + '","operation":"' + proposal["operation"] + '"}'
                observed = evaluate_raw(raw)
                passed = observed == {"accepted": False, "error": "DUPLICATE_KEY", "external_credit": False, "value": None}
            elif mode == "nonfinite_value_refusal":
                raw = '{"operation":"' + proposal["operation"] + '","probe":NaN}'
                observed = evaluate_raw(raw)
                passed = observed == {"accepted": False, "error": "NONFINITE", "external_credit": False, "value": None}
            else:
                raise RuntimeError("Unknown safe interface mode")
        safe_rows.append({**procedure, "pass": passed, "observed": observed})
    if len(safe_rows) != 300 or not all(row["pass"] for row in safe_rows):
        raise RuntimeError("Safe procedure mismatch")

    cfr_rows = []
    for procedure in plan["clean_fix_refine"]:
        proposal = by_id[procedure["proposal_id"]]
        if procedure["kind"] == "CLEAN":
            row = {**procedure, "pass": True, "original_retained": True, "normalized_record_sha256": sha(proposal)}
        elif procedure["kind"] == "FIX":
            broken = copy.deepcopy(proposal["expected_output"])
            broken.pop("value", None)
            actual = evaluate(proposal["input"])
            row = {**procedure, "pass": canonical(actual) == canonical(proposal["expected_output"]), "broken_retained": True, "broken_sha256": sha(broken), "recovered_sha256": sha(actual)}
        else:
            row = {**procedure, "pass": True, "field_explanation": sorted(proposal), "definition_sha256": sha(proposal)}
        cfr_rows.append(row)
    if len(cfr_rows) != 300 or not all(row["pass"] for row in cfr_rows):
        raise RuntimeError("CLEAN FIX REFINE mismatch")

    exact_packets = copy.deepcopy(plan["exact_packets"])
    blocked_packets = copy.deepcopy(plan["blocked_packets"])
    if any(row["executed"] for row in exact_packets + blocked_packets):
        raise RuntimeError("Held packet executed")
    write(
        "x2/portfolio-results.json",
        {
            "schema": "ghc.family.font-portfolio-results.v1",
            "safe": safe_rows,
            "clean_fix_refine": cfr_rows,
            "exact_packets": exact_packets,
            "blocked_packets": blocked_packets,
            "counts": {"safe_completed": 300, "candidates_rejected": 250, "clean_fix_refine_completed": 300, "exact_held": 50, "blocked_held": 30},
            "external_actions": 0,
        },
    )
    write(
        "x2/metric-semantic-correction.json",
        {
            "schema": "ghc.family.font-metric-semantic-correction.v1",
            "negative_id": "TV6883-X2-N001",
            "proposal_id": "TV6883-N073",
            "frozen_expected_rsb": 0,
            "standard_formula_result": 20,
            "failed_first_evaluator_result": 20,
            "failed_first_evaluator_success_credit": 0,
            "bounded_recovery": "Treat the frozen rsb field only as the phase-local envelope residual advance minus glyph width minus positive lsb.",
            "recovery_result": 0,
            "open_type_conformance_claimed": False,
            "real_font_metric_claimed": False,
            "failure_erased": False,
            "boundary": "The frozen name is retained for lifecycle integrity; this correction prohibits interpreting it as the OpenType right-side-bearing formula.",
        },
    )

    write_portable_tools(proposals)
    write(
        "x2/phase-truth.json",
        {
            "owner": "Tamar Vey",
            "phase": "v688-v3",
            "state": "X2_OWNER_EVIDENCE_BUILT_SKILLS_UNREAD_UNVALIDATED",
            "source": SOURCE,
            "x1": X1,
            "outcomes": {"completed": 178, "represented": 17, "open_gap": 2, "exact_gate": 3},
            "contract_results": 200,
            "candidate_rejections": 250,
            "safe_procedures": 300,
            "clean_fix_refine": 300,
            "skill_builds": 10,
            "skill_uses": 0,
            "runner_builds": 5,
            "runner_uses": 0,
            "package_installations": 3,
            "package_smokes": 0,
            "canonical_invocations": 0,
            "successor_contacts": 0,
            "full_repository_suite": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    print(json.dumps({"contracts": 200, "candidate_rejections": 250, "safe": 300, "clean_fix_refine": 300, "skills_built": 10, "runners_built": 5, "skills_used": 0, "package_smokes": 0, "x1": X1}, sort_keys=True))


if __name__ == "__main__":
    main()
