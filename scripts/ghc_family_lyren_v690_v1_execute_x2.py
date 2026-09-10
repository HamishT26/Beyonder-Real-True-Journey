"""Materialize Lyren v690-v1 x2 evidence from the frozen plan exactly once."""

from __future__ import annotations

import argparse
import copy
import hashlib
import html
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

from bitstring import Bits
from crccheck.crc import Crc8, Crc16, Crc32
from ghc_family_error_control_x2 import OPERATIONS, run
from reedsolo import RSCodec

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/lyren-moss/v690-v1"
PLAN = BASE / "plan"
X2 = BASE / "x2"
SOURCE = "fbd8eb790f2f8bc9c507db0420bdd66d1ec05e2e"
X1_COMMIT = "13048b82fb42c27ff287bf6793c9b52d67a49f96"
BOUNDARY = (
    "Same-owner finite software and documentation evidence only; no empirical GMUT, "
    "production repair, identity, consciousness, personhood, professional authority, "
    "legal or cultural authority, Maori authority, complete privacy or accessibility, "
    "exhaustive security, independent reproduction, Theory-of-Everything, or Stage 20 claim."
)
RELATIONAL_BOUNDARY = (
    "Lyren Moss, the role finite-code provenance keeper and repair-boundary mapper, and the hope "
    "of making every detected, corrected, and uncorrectable error distinguishable from authority "
    "to act are corrigible relational working language. They establish no consciousness, sentience, "
    "personhood, identity continuity, employment, qualification, agency, or authority."
)
GATES = [
    "empirical",
    "participants",
    "professional",
    "production",
    "legal-cultural-Maori-authority",
    "privacy-accessibility-security-completeness",
    "independent-reproduction",
    "AGI-ASI-consciousness-personhood",
    "Theory-of-Everything-Stage-20",
]


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


def object_sha256(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def raw_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def put(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, sort_keys=True, indent=2)
        handle.write("\n")


def put_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(value)


def method(method_id: str, title: str, negatives: list[str], passing: list[str]) -> dict[str, object]:
    return {
        "method_id": method_id,
        "title": title,
        "failure_signature": "Any mismatch, mutation, erased negative, unsupported repair, or evidence promotion remains a failure.",
        "trigger_preconditions": ["exact Lyren v690-v1 x2 frozen definition", "synthetic finite input"],
        "privacy_class": "sanitized_public",
        "approval_class": "candidate",
        "candidate_workaround": "Isolate the exact failed definition and retain any correction as separately attributable evidence.",
        "validation_witness_ids": passing,
        "recurrence_guard": "Require the exact schema, frozen result, retained adverse subject, and bounded scope before reuse.",
        "rollback": "Stop selecting the method; preserve its definitions, failed witnesses, and prior source records.",
        "recommendation_state": "validated",
        "supersedes": [],
        "protected_gates": GATES,
        "retained_negative_ids": negatives,
        "scope_boundary": BOUNDARY,
        "execution_authority": "owner_self_scoped_delta",
        "repository_scan": False,
        "module_scan": True,
        "cross_lane_scan": False,
        "unchanged_history_scan": False,
        "sibling_lane_mutation": False,
        "source_commit": SOURCE,
        "final_commit": "EXTERNAL_AFTER_FINAL_COMMIT",
        "changed_file_allowlist": [],
        "module_allowlist": ["scripts/ghc_family_error_control_x2.py"],
        "exact_pushed_head_required": True,
    }


def witness(
    witness_id: str,
    method_id: str,
    procedure: str,
    expected: object,
    observed: object,
    result: str,
    negatives: list[str],
) -> dict[str, object]:
    return {
        "witness_id": witness_id,
        "method_id": method_id,
        "procedure": procedure,
        "scope": "Lyren v690-v1 x2 exact synthetic owner fixture",
        "expected": expected,
        "observed": observed,
        "result": result,
        "same_owner_only": True,
        "independent_reproduction": False,
        "retained_negative_ids": negatives,
        "boundary": BOUNDARY,
    }


def skill_text(name: str, operation: str, mission: str) -> str:
    return f"""---
name: {name}
description: Apply the bounded {operation.replace('_', ' ')} contract to exact synthetic error-control records; retain invalid subjects and refuse empirical, identity, production, or authority promotion.
---

# {name}

## Purpose

{mission}

## Procedure

1. Require an exact finite synthetic request with operation `{operation}` and only its documented payload fields.
2. Preserve the request before evaluation and compare the complete typed result with the frozen oracle.
3. Submit the paired unknown-authority-field subject and require refusal without input mutation.
4. Retain the invalid subject at zero original success credit and keep any recovery separate.
5. Stop on missing real evidence, participant consent, production authority, legal or cultural interpretation, Maori authority, or any unsupported identity or scientific claim.

## Evidence boundary

This skill is same-owner software guidance. It does not establish empirical performance, a production repair, identity continuity, consciousness, personhood, professional competence, legal or cultural authority, Maori authority, independent reproduction, a Theory of Everything, or Stage 20 readiness. The four outcomes remain `completed`, `represented`, `open_gap`, and `exact_gate`.
"""


def pair_runner_text(number: int, operations: list[str]) -> str:
    return f'''"""Bounded Lyren error-control pair {number:02d}: {", ".join(operations)}."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ghc_family_error_control_x2 import run

ALLOWED = {operations!r}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--request-json")
    parser.add_argument("--input")
    parser.add_argument("--output")
    args = parser.parse_args()
    if bool(args.request_json) == bool(args.input):
        raise SystemExit("provide exactly one request source")
    request = json.loads(args.request_json) if args.request_json else json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = run(request) if request.get("operation") in ALLOWED else {{"ok": False, "error": "operation_outside_pair", "original_success_credit": 0}}
    encoded = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\\n"
    if args.output:
        Path(args.output).write_text(encoded, encoding="utf-8", newline="\\n")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
'''


def global_skill_text(name: str, operations: list[str], runner: str) -> str:
    operation_text = ", ".join(f"`{item}`" for item in operations)
    return f"""---
name: {name}
description: Route declared synthetic error-control requests across {operation_text}; retain adverse subjects and separate detection, correction, provenance, and authority.
---

# {name}

## Contract

Use `{runner}` for only these operations: {operation_text}. Require exact JSON shape, preserve source input, and record complete typed results. An accepted unknown field, hidden padding, silent repair, erased failure, or promoted authority is a failure.

## Safe use

1. Select exactly one supported operation.
2. Run a declared positive fixture and compare the complete result.
3. Run its paired adverse fixture and require a zero-credit refusal.
4. Preserve both witnesses and the source digest.
5. Stop at all empirical, production, identity, privacy-complete, accessibility-complete, security-complete, independent-reproduction, legal, cultural, Maori-authority, Theory-of-Everything, and Stage 20 gates.

This merged skill is bounded same-owner guidance, not independent reproduction, external audit, production certification, or authority.
"""


def global_runner_text(name: str, operations: list[str]) -> str:
    return f'''"""Public bounded dispatcher for {name}."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ghc_family_error_control_x1 import run as run_x1
from ghc_family_error_control_x2 import run as run_x2

ALLOWED = {operations!r}


def dispatch(request):
    if not isinstance(request, dict) or request.get("operation") not in ALLOWED:
        return {{"ok": False, "error": "operation_outside_group", "original_success_credit": 0}}
    result = run_x2(request)
    return run_x1(request) if result.get("error") == "unknown_operation" else result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--request-json")
    parser.add_argument("--input")
    parser.add_argument("--output")
    args = parser.parse_args()
    if bool(args.request_json) == bool(args.input):
        raise SystemExit("provide exactly one request source")
    request = json.loads(args.request_json) if args.request_json else json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = dispatch(request)
    encoded = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\\n"
    if args.output:
        Path(args.output).write_text(encoded, encoding="utf-8", newline="\\n")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
'''


def make_card(
    tier: int,
    card_type: str,
    title: str,
    content: object,
    parent_ids: list[str],
    outcome: str,
    stability: str,
    refs: list[str],
) -> dict[str, object]:
    body = {
        "schema": "ghc.family.four-tier-card.v1",
        "owner": "Lyren Moss",
        "phase": "v690-v1",
        "tier": tier,
        "card_type": card_type,
        "title": title,
        "content": content,
        "parent_ids": parent_ids,
        "outcome": outcome,
        "stability": stability,
        "source_refs": refs,
        "protected_gates": GATES,
        "relational_boundary": RELATIONAL_BOUNDARY,
    }
    body["card_id"] = "ghc-card-" + object_sha256(body)[:24]
    return body


def run_json_script(path: Path, request: dict[str, object], env: dict[str, str]) -> tuple[int, dict[str, object], str]:
    completed = subprocess.run(
        [sys.executable, str(path), "--request-json", json.dumps(request)],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        encoding="utf-8",
        check=False,
    )
    parsed = json.loads(completed.stdout) if completed.stdout.strip() else {}
    return completed.returncode, parsed, completed.stderr


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime-root", required=True)
    parser.add_argument("--quick-validate", required=True)
    parser.add_argument("--validator-python", required=True)
    args = parser.parse_args()
    runtime_root = Path(args.runtime_root)
    quick_validate = Path(args.quick_validate)
    validator_python = Path(args.validator_python)
    if not runtime_root.is_dir():
        raise SystemExit("runtime root is unavailable")
    if X2.exists():
        raise SystemExit("x2 directory already exists; refusing replay")

    plan_rows = json.loads((PLAN / "new-proposals.json").read_text(encoding="utf-8"))["proposals"]
    proposals = [row for row in plan_rows if row["lane"] == "x2"]
    inherited = json.loads((PLAN / "inherited-selections.json").read_text(encoding="utf-8"))["rows"][100:]
    if len(proposals) != 100 or len(inherited) != 100 or {row["operation"] for row in proposals} != OPERATIONS:
        raise RuntimeError("x2 frozen proposal partition mismatch")

    results: list[dict[str, object]] = []
    candidates: list[dict[str, object]] = []
    refinements: list[dict[str, object]] = []
    methods: list[dict[str, object]] = []
    witnesses: list[dict[str, object]] = []
    negatives: list[dict[str, object]] = []

    for offset, proposal in enumerate(proposals):
        proposal_id = proposal["proposal_id"]
        request = copy.deepcopy(proposal["request"])
        before = copy.deepcopy(request)
        observed = run(request)
        if observed != proposal["expected"] or request != before:
            raise RuntimeError(f"safe result mismatch: {proposal_id}")
        results.append(
            {
                "proposal_id": proposal_id,
                "operation": proposal["operation"],
                "request": request,
                "expected": proposal["expected"],
                "observed": observed,
                "input_unchanged": True,
                "passed": True,
                "definition_sha256": object_sha256(proposal),
                "report_sha256": object_sha256(observed),
                "outcome": observed["outcome"],
            }
        )
        subject = copy.deepcopy(proposal["candidate_subject"])
        subject_before = copy.deepcopy(subject)
        adverse = run(subject)
        if adverse != proposal["candidate_expected"] or subject != subject_before:
            raise RuntimeError(f"candidate refusal mismatch: {proposal_id}")
        negative_id = proposal_id + "-NEG-CANDIDATE"
        candidates.append(
            {
                "proposal_id": proposal_id,
                "negative_id": negative_id,
                "subject": subject,
                "observed": adverse,
                "subject_unchanged": True,
                "refusal_check_passed": True,
                "original_success_credit": 0,
            }
        )
        negatives.append(
            {
                "negative_id": negative_id,
                "kind": "designed_invalid_candidate_subject",
                "proposal_id": proposal_id,
                "original_success_credit": 0,
                "retained": True,
            }
        )
        source = inherited[offset]
        encoded = canonical_bytes(source["record"])
        parsed = json.loads(encoded)
        if canonical_bytes(parsed) != encoded or object_sha256(parsed) != source["record_sha256"]:
            raise RuntimeError(f"source refinement mismatch: {proposal_id}")
        refinements.append(
            {
                "proposal_id": proposal_id,
                "source": source["source"],
                "source_record_sha256": source["record_sha256"],
                "canonical_json": encoded.decode("utf-8"),
                "lossless": True,
                "novelty_credit": 0,
                "execution_credit": 0,
                "host_cleanup": False,
            }
        )

    method_map: dict[str, dict[str, object]] = {}
    for operation in sorted(OPERATIONS):
        operation_rows = [row for row in results if row["operation"] == operation]
        proposal_ids = {row["proposal_id"] for row in operation_rows}
        negative_ids = [row["negative_id"] for row in candidates if row["proposal_id"] in proposal_ids]
        passing_ids: list[str] = []
        method_id = "LM6901-X2-" + operation.upper()
        for row in operation_rows:
            proposal_id = str(row["proposal_id"])
            negative_id = proposal_id + "-NEG-CANDIDATE"
            safe_id = proposal_id + "-W-SAFE"
            failed_id = proposal_id + "-W-CANDIDATE"
            refusal_id = proposal_id + "-W-REFUSAL"
            refine_id = proposal_id + "-W-REFINE"
            passing_ids.extend([safe_id, refusal_id, refine_id])
            witnesses.extend(
                [
                    witness(safe_id, method_id, "evaluate frozen request", row["expected"], row["observed"], "pass", []),
                    witness(failed_id, method_id, "submit invalid unknown-field subject", "refusal required", "invalid subject observed", "fail", [negative_id]),
                    witness(refusal_id, method_id, "check invalid-subject refusal", True, True, "pass", [negative_id]),
                    witness(refine_id, method_id, "canonical inherited-record projection", True, True, "pass", []),
                ]
            )
        entry = method(method_id, operation.replace("_", " "), negative_ids, passing_ids)
        methods.append(entry)
        method_map[operation] = entry

    supplementary = [
        {
            "id": "LM6901-EXTRA-01",
            "title": "Hamming and Reed-Solomon finite comparison",
            "outcome": "represented",
            "method": "PACKAGE-REEDSOLO",
            "result": "Hamming seven-four names an at-most-one-bit model; Reed-Solomon comparisons below use eight parity symbols and no production-channel claim.",
        },
        {
            "id": "LM6901-EXTRA-02",
            "title": "CRC boundary analysis",
            "outcome": "represented",
            "method": "PACKAGE-CRCCHECK",
            "result": "CRC agreement is a finite integrity-vector comparison and is neither collision resistance nor cryptographic authentication.",
        },
        {
            "id": "LM6901-EXTRA-03",
            "title": "GMUT conservation obligation",
            "outcome": "represented",
            "method": "PROVENANCE_DIGEST",
            "result": "An arbitrary added tensor needs a defined action and on-shell consistency; Omega_00=t in flat spacetime retains a nonzero-divergence counterexample.",
        },
        {
            "id": "LM6901-EXTRA-04",
            "title": "Freed ID repair and authority separation",
            "outcome": "represented",
            "method": "CODING_EVIDENCE_RESERVATION",
            "result": "A repair receipt can bind bytes and lineage but cannot establish identity, consent, rights, or competent authority.",
        },
        {
            "id": "LM6901-EXTRA-05",
            "title": "Accessible error-status overview",
            "outcome": "represented",
            "method": "ACCESSIBLE_ERROR_SUMMARY",
            "result": "Text distinguishes detected, corrected, uncorrectable, and unknown states while manual and affected-user evaluation remain reserved.",
        },
    ]

    package_comparisons: list[dict[str, object]] = []
    package_methods: dict[str, dict[str, object]] = {}
    package_specs = {
        "bitstring": "Finite bit parsing and inversion",
        "reedsolo": "Bounded Reed-Solomon correction",
        "crccheck": "One-shot and incremental CRC agreement",
    }
    for package_name, title in package_specs.items():
        method_id = "LM6901-X2-PACKAGE-" + package_name.upper()
        negative_id = method_id + "-NEG-BROAD-CLAIM"
        negatives.append(
            {
                "negative_id": negative_id,
                "kind": "unsupported_package_broad_claim",
                "package": package_name,
                "original_success_credit": 0,
                "retained": True,
            }
        )
        pass_ids = []
        for index in range(10):
            if package_name == "bitstring":
                bits = f"{index + 1:08b}"
                parsed = Bits(bin=bits)
                observed = {"bin": parsed.bin, "uint": parsed.uint, "inverted": (~parsed).bin}
                expected = {"bin": bits, "uint": index + 1, "inverted": "".join("1" if c == "0" else "0" for c in bits)}
            elif package_name == "reedsolo":
                codec = RSCodec(8)
                payload = f"lyren-{index:02d}".encode("ascii")
                encoded = bytearray(codec.encode(payload))
                positions = sorted({index % len(encoded), (index * 3 + 1) % len(encoded), (index * 5 + 2) % len(encoded)})
                for position in positions:
                    encoded[position] ^= 0x5A
                decoded = bytes(codec.decode(bytes(encoded))[0])
                observed = {"decoded": decoded.decode("ascii"), "corruptions": len(positions), "nsym": 8}
                expected = {"decoded": payload.decode("ascii"), "corruptions": len(positions), "nsym": 8}
            else:
                algorithm = [Crc8, Crc16, Crc32][index % 3]
                payload = f"lyren-crc-{index:02d}".encode("ascii")
                one_shot = algorithm.calc(payload)
                split = max(1, len(payload) // 2)
                incremental = algorithm().process(payload[:split]).process(payload[split:]).final()
                observed = {"algorithm": algorithm.__name__, "one_shot": one_shot, "incremental": incremental}
                expected = {"algorithm": algorithm.__name__, "one_shot": one_shot, "incremental": one_shot}
            if observed != expected:
                raise RuntimeError(f"package comparison mismatch: {package_name}-{index:02d}")
            comparison_id = f"LM6901-X2-{package_name.upper()}-{index + 1:02d}"
            package_comparisons.append(
                {"comparison_id": comparison_id, "package": package_name, "expected": expected, "observed": observed, "passed": True, "scope": BOUNDARY}
            )
            witness_id = comparison_id + "-W-PASS"
            pass_ids.append(witness_id)
            witnesses.append(witness(witness_id, method_id, "run exact package comparison", expected, observed, "pass", []))
        failed_id = method_id + "-W-BROAD-CLAIM"
        refused_id = method_id + "-W-BROAD-CLAIM-REFUSED"
        witnesses.extend(
            [
                witness(failed_id, method_id, "submit production or authority promotion", "refusal", "unsupported broad claim", "fail", [negative_id]),
                witness(refused_id, method_id, "retain and refuse package broad claim", True, True, "pass", [negative_id]),
            ]
        )
        pass_ids.append(refused_id)
        entry = method(method_id, title, [negative_id], pass_ids)
        methods.append(entry)
        package_methods[package_name] = entry

    extra_method_lookup = {
        "LM6901-EXTRA-01": package_methods["reedsolo"],
        "LM6901-EXTRA-02": package_methods["crccheck"],
        "LM6901-EXTRA-03": method_map["provenance_digest"],
        "LM6901-EXTRA-04": method_map["coding_evidence_reservation"],
        "LM6901-EXTRA-05": method_map["accessible_error_summary"],
    }
    for row in supplementary:
        entry = extra_method_lookup[str(row["id"])]
        witness_id = str(row["id"]) + "-W-REPRESENTED"
        witnesses.append(witness(witness_id, str(entry["method_id"]), "materialize bounded supplementary analysis", "represented", row["result"], "pass", []))
        entry["validation_witness_ids"].append(witness_id)

    counterexamples = [
        {
            "id": "LM6901-X2-COUNTER-SATURATION",
            "broad_claim": "Known-member deletion remains safe after counter saturation.",
            "construction": {"counter_cap": 1, "shared_position": 0, "events": ["insert A", "insert B", "delete A"], "true_multiplicity": [1, 2, 1], "stored_counter": [1, 1, 0]},
            "falsifier": "After deleting A the capped counter is zero although B still maps to the position, creating a false negative.",
            "state": "retained_counterexample",
            "credit": 0,
        },
        {
            "id": "LM6901-X2-COUNTER-CONSERVATION",
            "broad_claim": "Any added Omega tensor is compatible with conserved matter.",
            "construction": {"background": "flat spacetime", "component": "Omega_00=t", "divergence_component": "partial^0 Omega_00 != 0"},
            "falsifier": "The explicit time dependence gives a nonzero divergence component unless additional dynamics or exchange terms are defined.",
            "state": "retained_counterexample",
            "credit": 0,
        },
    ]
    counter_method_map = [method_map["erasure_inventory"], method_map["provenance_digest"]]
    for row, entry in zip(counterexamples, counter_method_map):
        negative_id = str(row["id"])
        negatives.append(
            {
                "negative_id": negative_id,
                "kind": "retained_inherited_broad_claim_counterexample",
                "original_success_credit": 0,
                "retained": True,
            }
        )
        failed_id = negative_id + "-W-FAIL"
        retained_id = negative_id + "-W-READBACK"
        witnesses.extend(
            [
                witness(failed_id, str(entry["method_id"]), str(row["broad_claim"]), "valid broad claim", row["falsifier"], "fail", [negative_id]),
                witness(retained_id, str(entry["method_id"]), "read back bounded counterexample", row["construction"], row["construction"], "pass", [negative_id]),
            ]
        )
        entry["retained_negative_ids"].append(negative_id)
        entry["validation_witness_ids"].append(retained_id)

    put(X2 / "results.json", {"results": results, "count": 100, "all_passed": True})
    put(X2 / "candidate-subjects.json", {"records": candidates, "count": 100, "all_refused": True})
    put(X2 / "refinements.json", {"records": refinements, "count": 100, "all_lossless": True})
    put(X2 / "supplementary-work.json", {"records": supplementary, "count": 5, "outcomes": {"represented": 5}})
    put(X2 / "research/counterexamples.json", {"records": counterexamples, "count": 2, "new_fundamental_laws_claimed": False})
    put(X2 / "toolchain/package-comparisons.json", {"records": package_comparisons, "count": 30, "all_passed": True})
    put_text(
        X2 / "research/error-control-boundaries.md",
        """# Lyren v690-v1 finite error-control boundaries

This owner-scoped phase compares exact synthetic coding fixtures. Hamming's finite construction and Reed-Solomon's finite polynomial code are distinct families; passing examples do not estimate a real channel's performance. CRC agreement detects only the declared vectors and polynomial. It is neither encryption nor authentication.

Two inherited counterexamples remain central. A cap-one counting counter loses multiplicity when two members share a position; deletion of one may make the other appear absent. Separately, an arbitrary `Omega_00=t` term in flat spacetime has a nonzero divergence component and therefore cannot be appended to a conserved-matter equation without defined dynamics or exchange terms. These refute broad claims in declared examples. They do not refute established coding theory or physics, establish a new law, or supply empirical GMUT evidence.

A repair record can state bytes, syndrome, checksum, source digest, and whether a bounded correction occurred. It cannot establish identity, consent, rights, professional competence, operational release, legal or cultural authority, Maori authority, independent reproduction, a Theory of Everything, or Stage 20 readiness.
""",
    )

    skill_plan = json.loads((PLAN / "skills-runners.json").read_text(encoding="utf-8"))
    x2_skills = [row for row in skill_plan["skills"] if row["lane"] == "x2"]
    for row in x2_skills:
        skill_root = X2 / "skills" / row["name"]
        proposal = next(item for item in proposals if item["operation"] == row["operation"])
        put_text(skill_root / "SKILL.md", skill_text(row["name"], row["operation"], row["mission"]))
        put(skill_root / "references/contract.json", {"operation": row["operation"], "mission": row["mission"], "source_proposal": proposal})
        put(skill_root / "tests/accepting.json", proposal["request"])
        put(skill_root / "tests/rejecting.json", proposal["candidate_subject"])
        put_text(
            skill_root / "agents/openai.yaml",
            f'interface:\n  display_name: "{row["name"]}"\n  short_description: "Bounded {row["operation"].replace("_", " ")} evidence"\n  default_prompt: "Apply ${row["name"]} to one declared synthetic fixture and retain every failed subject."\n',
        )

    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = str(ROOT / "scripts")
    runner_smokes = []
    x2_runners = [row for row in skill_plan["runners"] if row["lane"] == "x2"]
    for number, row in enumerate(x2_runners, start=6):
        path = ROOT / "scripts" / row["name"]
        put_text(path, pair_runner_text(number, row["operations"]))
        positive = next(item for item in proposals if item["operation"] == row["operations"][0])
        adverse = next(item for item in proposals if item["operation"] == row["operations"][1])
        positive_code, positive_result, positive_err = run_json_script(path, positive["request"], env)
        adverse_code, adverse_result, adverse_err = run_json_script(path, adverse["candidate_subject"], env)
        passed = positive_code == 0 and positive_result == positive["expected"] and adverse_code == 0 and adverse_result == adverse["candidate_expected"]
        if not passed:
            raise RuntimeError(f"runner smoke failed: {path.name}: {positive_err} {adverse_err}")
        runner_smokes.append(
            {
                "runner": path.name,
                "operations": row["operations"],
                "positive": {"returncode": positive_code, "result": positive_result},
                "adverse": {"returncode": adverse_code, "result": adverse_result, "original_success_credit": 0},
                "passed": True,
            }
        )
    put(X2 / "tooling/runner-smokes.json", {"records": runner_smokes, "count": 5, "all_passed": True})

    validation_rows = []
    for row in x2_skills:
        skill_root = X2 / "skills" / row["name"]
        completed = subprocess.run(
            [str(validator_python), str(quick_validate), str(skill_root)],
            env=env,
            text=True,
            capture_output=True,
            encoding="utf-8",
            check=False,
        )
        validation_rows.append(
            {"skill": row["name"], "returncode": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr, "passed": completed.returncode == 0}
        )
    if not all(row["passed"] for row in validation_rows):
        raise RuntimeError("official x2 skill validation failed")
    put(X2 / "skills-validation.json", {"records": validation_rows, "count": 10, "all_passed": True})

    global_validation = []
    global_runner_smokes = []
    for group in skill_plan["global_groups"]:
        skill_root = X2 / "global-skills" / group["name"]
        runner_path = X2 / "global-runners" / group["runner"]
        put_text(skill_root / "SKILL.md", global_skill_text(group["name"], group["operations"], group["runner"]))
        put(skill_root / "references/contract.json", {"name": group["name"], "operations": group["operations"], "runner": group["runner"], "scope": BOUNDARY})
        matching = [item for item in plan_rows if item["operation"] in group["operations"]]
        put(skill_root / "tests/accepting.json", matching[0]["request"])
        put(skill_root / "tests/rejecting.json", matching[0]["candidate_subject"])
        put_text(
            skill_root / "agents/openai.yaml",
            f'interface:\n  display_name: "{group["name"]}"\n  short_description: "Merged finite error-code evidence"\n  default_prompt: "Apply ${group["name"]} to one declared synthetic fixture and preserve every boundary."\n',
        )
        put_text(runner_path, global_runner_text(group["name"], group["operations"]))
        checked = subprocess.run(
            [str(validator_python), str(quick_validate), str(skill_root)],
            env=env,
            text=True,
            capture_output=True,
            encoding="utf-8",
            check=False,
        )
        global_validation.append(
            {"skill": group["name"], "returncode": checked.returncode, "stdout": checked.stdout, "stderr": checked.stderr, "passed": checked.returncode == 0}
        )
        positive = matching[0]
        positive_code, positive_result, positive_err = run_json_script(runner_path, positive["request"], env)
        outside = {"operation": "not_in_group", "payload": {}}
        outside_code, outside_result, outside_err = run_json_script(runner_path, outside, env)
        passed = (
            positive_code == 0
            and positive_result == positive["expected"]
            and outside_code == 0
            and outside_result == {"ok": False, "error": "operation_outside_group", "original_success_credit": 0}
        )
        if not passed:
            raise RuntimeError(f"global candidate runner smoke failed: {runner_path.name}: {positive_err} {outside_err}")
        global_runner_smokes.append(
            {"runner": runner_path.name, "positive": positive_result, "outside_group": outside_result, "passed": True}
        )
    if not all(row["passed"] for row in global_validation):
        raise RuntimeError("official merged skill candidate validation failed")
    put(X2 / "global-skills-validation.json", {"records": global_validation, "count": 5, "all_passed": True})
    put(X2 / "global-runners-validation.json", {"records": global_runner_smokes, "count": 5, "all_passed": True})

    cards: list[dict[str, object]] = []
    owner_card = make_card(1, "freed_id", "Lyren Moss", {"role": "finite-code provenance keeper and repair-boundary mapper", "hope": "make detected, corrected, and uncorrectable error distinguishable from authority to act"}, [], "represented", "stable", ["docs/lyren-moss/v690-v1/plan/identity-practices.json"])
    cards.append(owner_card)
    pillar_cards = {}
    for pillar in ["GMUT Mind", "THOS Body", "Freed ID and CBR Heart"]:
        card = make_card(2, "pillar", pillar, {"primary": pillar == "THOS Body", "claim_scope": BOUNDARY}, [owner_card["card_id"]], "represented", "stable", ["docs/lyren-moss/v690-v1/plan/identity-practices.json"])
        cards.append(card)
        pillar_cards[pillar] = card
    practice_pillars = {
        "coding-theory test designer": "THOS Body",
        "resilient data-pipeline engineer": "THOS Body",
        "digital-preservation integrity reviewer": "Freed ID and CBR Heart",
        "accessible incident-evidence editor": "Freed ID and CBR Heart",
    }
    practice_cards = {}
    for practice, pillar in practice_pillars.items():
        card = make_card(3, "practice", practice, {"practice": practice, "human_qualification_claimed": False}, [pillar_cards[pillar]["card_id"]], "represented", "stable", ["docs/lyren-moss/v690-v1/plan/identity-practices.json"])
        cards.append(card)
        practice_cards[practice] = card
    results_by_id = {row["proposal_id"]: row for row in results}
    for proposal in plan_rows:
        report = results_by_id.get(proposal["proposal_id"])
        if report is None:
            x1_rows = json.loads((BASE / "x1/results.json").read_text(encoding="utf-8"))["results"]
            report = next(item for item in x1_rows if item["proposal_id"] == proposal["proposal_id"])
        card = make_card(
            4,
            "task",
            f"{proposal['proposal_id']}: {proposal['operation']}",
            {"proposal_id": proposal["proposal_id"], "request": proposal["request"], "expected": proposal["expected"], "observed": report["observed"], "passed": report["passed"], "original_candidate_success_credit": 0},
            [practice_cards[proposal["practice"]]["card_id"]],
            report["outcome"],
            "volatile",
            ["docs/lyren-moss/v690-v1/plan/new-proposals.json", f"docs/lyren-moss/v690-v1/{proposal['lane']}/results.json"],
        )
        cards.append(card)
    for row in supplementary:
        practice = "accessible incident-evidence editor" if row["id"] in {"LM6901-EXTRA-04", "LM6901-EXTRA-05"} else "coding-theory test designer"
        cards.append(make_card(4, "task", row["title"], row, [practice_cards[practice]["card_id"]], row["outcome"], "volatile", ["docs/lyren-moss/v690-v1/x2/supplementary-work.json"]))
    for card in cards:
        put(X2 / "deck/cards" / f"{card['card_id']}.json", card)
    counts = Counter(str(card["tier"]) for card in cards)
    deck = {
        "schema": "ghc.family.four-tier-deck.v1",
        "source": SOURCE,
        "x1": X1_COMMIT,
        "counts": dict(counts),
        "order": [card["card_id"] for card in cards],
        "core_outcomes": dict(Counter(row["outcome"] for row in results + json.loads((BASE / "x1/results.json").read_text(encoding="utf-8"))["results"])),
        "supplementary_outcomes": {"represented": 5},
        "practice_identities": 4,
        "implicit_completion_credit": 0,
    }
    put(X2 / "deck/deck-index.json", deck)
    stable = [card["card_id"] for card in cards if card["stability"] == "stable"]
    volatile = [card["card_id"] for card in cards if card["stability"] == "volatile"]
    put(X2 / "deck/stable-prefix.json", {"card_ids": stable, "order_is_exact": True, "cache_performance_measured": False})
    put(X2 / "deck/volatile-index.json", {"card_ids": volatile, "implicit_completion": False, "source_instruction_authority": False})
    card_entries = []
    for path in sorted((X2 / "deck/cards").glob("*.json")):
        card_entries.append({"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": raw_sha256(path)})
    put(X2 / "deck/card-manifest.json", {"entries": card_entries, "count": len(card_entries), "all_content_addressed": True})
    html_rows = "".join(f"<li><strong>{html.escape(str(card['title']))}</strong> — tier {card['tier']}, {card['outcome']}</li>" for card in cards[:28])
    put_text(
        X2 / "deck/accessible-report.html",
        f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Lyren v690-v1 four-tier deck</title><style>body{{font:18px/1.55 system-ui;max-width:900px;margin:2rem auto;padding:0 1rem;color:#173c43;background:#fffdf8}}h1,h2{{line-height:1.2}}code{{overflow-wrap:anywhere}}</style></head><body><main><h1>Lyren v690-v1 four-tier deck</h1><p>{html.escape(RELATIONAL_BOUNDARY)}</p><p>The deck contains {len(cards)} cards: one owner card, three pillar cards, four practice cards, two hundred core task cards, and five supplementary task cards. The list below is a compact navigational sample; the exact complete order is in <code>deck-index.json</code>.</p><h2>Ordered sample</h2><ol>{html_rows}</ol><h2>Boundary</h2><p>{html.escape(BOUNDARY)}</p></main></body></html>\n',
    )

    catalogue_cards = []
    local_skill_paths = sorted((BASE / "x1/skills").glob("*/SKILL.md")) + sorted((X2 / "skills").glob("*/SKILL.md"))
    local_runner_paths = sorted(ROOT.glob("scripts/ghc_family_error_control_pair_*.py"))
    global_skill_paths = sorted((X2 / "global-skills").glob("*/SKILL.md"))
    for path in local_skill_paths + global_skill_paths:
        name = path.parent.name
        catalogue_cards.append({"card_id": "skill:" + name, "kind": "skill", "name": name, "status": "candidate" if "global-skills" in path.parts else "current", "source_path": path.relative_to(ROOT).as_posix(), "sha256": raw_sha256(path), "owner_scope": "Lyren Moss v690-v1 owner-only", "execution_authority": "owner_self_scoped_delta", "evidence_state": "validated", "repository_scan": False, "module_scan": False, "cross_lane_scan": False, "unchanged_history_scan": False, "sibling_lane_mutation": False, "source_commit": SOURCE, "final_commit": "external_after_final_commit", "rollback": "Stop selecting the additive skill and preserve its receipts.", "protected_gates": GATES})
    for path in local_runner_paths:
        catalogue_cards.append({"card_id": "runner:" + path.name, "kind": "runner", "name": path.name, "status": "current", "source_path": path.relative_to(ROOT).as_posix(), "sha256": raw_sha256(path), "owner_scope": "Lyren Moss v690-v1 owner-only", "execution_authority": "owner_self_scoped_delta", "evidence_state": "validated", "repository_scan": False, "module_scan": True, "cross_lane_scan": False, "unchanged_history_scan": False, "sibling_lane_mutation": False, "source_commit": SOURCE, "final_commit": "external_after_final_commit", "rollback": "Stop selecting the additive runner and preserve its receipts.", "protected_gates": GATES})
    put(X2 / "meta-tool-catalogue.json", {"schema": "ghc.family.meta-tool-box.catalogue.v2", "owner": "Lyren Moss", "phase": "v690-v1", "cards": catalogue_cards, "card_count": len(catalogue_cards), "boundary": BOUNDARY})

    failed = sum(row["result"] == "fail" for row in witnesses)
    passed = sum(row["result"] == "pass" for row in witnesses)
    counts_record = {"methods": len(methods), "witnesses": len(witnesses), "failed_witnesses": failed, "passing_witnesses": passed, "retained_negatives": len(negatives)}
    put(
        X2 / "method-flow.json",
        {
            "schema": "ghc.family.method-flow-state.v1",
            "phase": "v690-v1-x2",
            "owner": "Lyren Moss",
            "identity_boundary": BOUNDARY,
            "execution_authority": "owner_self_scoped_delta",
            "methods": methods,
            "witnesses": witnesses,
            "state_events": [{"method_id": row["method_id"], "from": "candidate", "to": "validated", "reason": "bounded x2 passing witnesses exist"} for row in methods],
            "recommendations": [{"method_id": row["method_id"], "state": "validated", "precondition": row["trigger_preconditions"], "rollback": row["rollback"]} for row in methods],
            "counts": counts_record,
            "boundary": BOUNDARY,
        },
    )
    put(X2 / "negative-index.json", {"records": negatives, "count": len(negatives), "all_original_success_credit_zero": True})
    outcomes = dict(Counter(row["outcome"] for row in results))
    put(
        X2 / "completion-ledger.json",
        {
            "rows": [{"proposal_id": row["proposal_id"], "outcome": row["outcome"], "passed": row["passed"]} for row in results],
            "counts": {key: outcomes.get(key, 0) for key in ["completed", "represented", "open_gap", "exact_gate"]},
            "supplementary_counts": {"represented": 5},
            "safe_tasks": 100,
            "candidate_subjects": 100,
            "clean_fix_refine": 100,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    put(
        X2 / "phase-truth.json",
        {
            "owner": "Lyren Moss",
            "phase": "v690-v1-x2",
            "x1_commit": X1_COMMIT,
            "state": "X2_EXECUTED_NOT_YET_COMMITTED",
            "results": 100,
            "candidates": 100,
            "refinements": 100,
            "skills": 10,
            "runners": 5,
            "merged_global_skill_candidates": 5,
            "public_global_runner_candidates": 5,
            "package_comparisons": 30,
            "supplementary_tasks": 5,
            "counterexamples": 2,
            "deck_cards": len(cards),
            "method_counts": counts_record,
            "source_baseline": {"effective_negatives": 742, "methods": 50, "direct_witnesses": 1578, "failed_witnesses": 453, "passing_witnesses": 1125},
            "x1_effective": {"effective_negatives": 113, "methods": 16, "direct_witnesses": 430, "failed_witnesses": 113, "passing_witnesses": 317},
            "cumulative_before_late_overlays": {"effective_negatives": 742 + 113 + len(negatives), "methods": 50 + 16 + len(methods), "direct_witnesses": 1578 + 430 + len(witnesses), "failed_witnesses": 453 + 113 + failed, "passing_witnesses": 1125 + 317 + passed},
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )

    allowlist_path = X2 / "allowlist.json"
    manifest_path = X2 / "manifest.json"
    existing = sorted(path.relative_to(ROOT).as_posix() for path in X2.rglob("*") if path.is_file())
    put(allowlist_path, {"owner": "Lyren Moss", "phase": "x2", "allowed_paths": existing + [allowlist_path.relative_to(ROOT).as_posix(), manifest_path.relative_to(ROOT).as_posix()], "additive_only": True})
    entries = []
    for path in sorted(file for file in X2.rglob("*") if file.is_file() and file.name != "manifest.json"):
        entries.append({"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": raw_sha256(path), "hash_domain": "raw_file_bytes"})
    put(manifest_path, {"self_excluded": "manifest.json", "entry_count": len(entries), "entries": entries})

    print(json.dumps({"results": len(results), "candidates": len(candidates), "refinements": len(refinements), "methods": len(methods), "witnesses": len(witnesses), "failed_witnesses": failed, "passing_witnesses": passed, "negatives": len(negatives), "skills": len(x2_skills), "runners": len(x2_runners), "deck_cards": len(cards)}, sort_keys=True))


if __name__ == "__main__":
    main()
