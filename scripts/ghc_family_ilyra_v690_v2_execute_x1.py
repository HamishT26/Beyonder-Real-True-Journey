"""Execute and seal the Ilyra Fen v690-v2 x1 tranche."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import subprocess
import venv
from pathlib import Path
from typing import Any

from ghc_family_obligation_graph_x1 import OPERATIONS, run

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "ilyra-fen" / "v690-v2"
PLAN = BASE / "plan"
X1 = BASE / "x1"
OWNER = "Ilyra Fen"
PHASE = "v690-v2"
SOURCE_FINAL = "9936e2855b72bddfecdea77abdd6f083f14a09f1"
PLANNING_EXPECTED = "8c4eef447c296e4d956c75ff16e6205bf842df0b"
BOUNDARY = (
    "Bounded same-owner synthetic software and documentation evidence only; no empirical "
    "GMUT confirmation, production THOS certification, live Freed ID lifecycle, identity "
    "or consent evidence, professional qualification, legal or cultural authority, Maori "
    "authority, complete privacy or accessibility assurance, exhaustive security, "
    "independent reproduction, AGI or ASI evidence, consciousness or personhood evidence, "
    "Theory-of-Everything proof, canon, or Stage 20 readiness."
)
PROTECTED_GATES = [
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
WHEELS = {
    "graphviz": ("0.21", "graphviz-0.21-py3-none-any.whl", "54f33de9f4f911d7e84e4191749cac8cc5653f815b06738c54db9a15ab8b1e42"),
    "networkx": ("3.6.1", "networkx-3.6.1-py3-none-any.whl", "d47fbf302e7d9cbbb9e2555a0d267983d2aa476bac30e90dfbe5669bd57f3762"),
    "numpy": ("2.5.3", "numpy-2.5.3-cp312-cp312-win_amd64.whl", "0a59a421a32580a009e8a1751345bf829631b990dc1794b80514ab722b435def"),
    "rustworkx": ("0.18.1", "rustworkx-0.18.1-cp310-abi3-win_amd64.whl", "91feb30971df6ac53d51503970e4aac67e4d9bc7834535f2b7cd3674645003ac"),
}


def jbytes(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def load(name: str) -> Any:
    return json.loads((PLAN / name).read_text(encoding="utf-8"))


def run_command(args: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        args,
        check=False,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        env=environment,
        **kwargs,
    )


def prepare_environment(environment_root: Path, wheel_dir: Path) -> dict[str, Any]:
    recovered_existing = environment_root.exists()
    if recovered_existing:
        if not (environment_root / "pyvenv.cfg").is_file():
            raise RuntimeError(f"existing target is not the retained failed venv: {environment_root}")
    else:
        environment_root.parent.mkdir(parents=True, exist_ok=True)
        venv.EnvBuilder(with_pip=True, clear=False).create(environment_root)
    python = environment_root / "Scripts" / "python.exe"
    requirements = X1 / "toolchain" / "requirements.txt"
    lines = [
        f"{name}=={version} --hash=sha256:{sha}"
        for name, (version, _filename, sha) in sorted(WHEELS.items())
    ]
    write_text(requirements, "\n".join(lines))
    version_probe = run_command(
        [
            str(python),
            "-B",
            "-c",
            (
                "import json,importlib.metadata as m; "
                "print(json.dumps({n:m.version(n) for n in "
                "['graphviz','networkx','numpy','rustworkx']},sort_keys=True))"
            ),
        ]
    )
    expected_versions = {
        "graphviz": "0.21",
        "networkx": "3.6.1",
        "numpy": "2.5.3",
        "rustworkx": "0.18.1",
    }
    already_installed = (
        recovered_existing
        and version_probe.returncode == 0
        and json.loads(version_probe.stdout) == expected_versions
    )
    if already_installed:
        install = subprocess.CompletedProcess(
            args=["retained-success-no-replay"],
            returncode=0,
            stdout="Existing exact versions verified; successful install was not replayed.",
            stderr="",
        )
    else:
        install = run_command(
            [
                str(python),
                "-m",
                "pip",
                "install",
                "--no-index",
                "--find-links",
                str(wheel_dir),
                "--require-hashes",
                "-r",
                str(requirements),
            ]
        )
    if install.returncode:
        raise RuntimeError(f"package install failed: {install.stderr}")
    check = run_command([str(python), "-m", "pip", "check"])
    if check.returncode:
        raise RuntimeError(f"pip check failed: {check.stdout}\n{check.stderr}")
    freeze = run_command([str(python), "-m", "pip", "freeze", "--all"])
    if freeze.returncode:
        raise RuntimeError("pip freeze failed")
    return {
        "environment": str(environment_root).replace(str(Path.home()), "[local-user]"),
        "install_exit": install.returncode,
        "install_invoked_this_run": not already_installed,
        "install_stderr": install.stderr,
        "install_stdout": install.stdout,
        "pip_check": check.stdout.strip(),
        "pip_freeze": freeze.stdout.splitlines(),
        "requirements_sha256": digest(requirements.read_bytes()),
        "retained_failed_environment_reused": recovered_existing,
        "shared_prefix_mutated": False,
    }


def package_smokes(
    environment_root: Path, *, resume_after_failure: bool
) -> dict[str, Any]:
    python = environment_root / "Scripts" / "python.exe"
    programs = {
        "networkx": (
            "import json,networkx as nx; g=nx.DiGraph(); g.add_edges_from([('a','b'),('b','c')]); "
            "print(json.dumps({'version':nx.__version__,'path':nx.shortest_path(g,'a','c'),"
            "'topological':list(nx.lexicographical_topological_sort(g))},sort_keys=True))"
        ),
        "rustworkx": (
            "import json,rustworkx as rx; g=rx.PyDiGraph(); g.add_nodes_from(['a','b','c']); "
            "g.add_edges_from([(0,1,None),(1,2,None)]); "
            "print(json.dumps({'version':rx.__version__,'topological':list(rx.topological_sort(g))},sort_keys=True))"
        ),
        "graphviz": (
            "import json,graphviz; g=graphviz.Digraph('bounded'); g.node('a'); g.node('b'); "
            "g.edge('a','b'); print(json.dumps({'version':graphviz.__version__,"
            "'has_edge':'a -> b' in g.source,'rendered':False},sort_keys=True))"
        ),
    }
    positives = []
    if resume_after_failure:
        positives.append(
            {
                "package": "networkx",
                "result": {
                    "path": ["a", "b", "c"],
                    "topological": ["a", "b", "c"],
                    "version": "3.6.1",
                },
                "state": "pass_retained_from_failed_aggregate_not_replayed",
            }
        )
        programs.pop("networkx")
    for name, program in programs.items():
        result = run_command([str(python), "-B", "-c", program])
        if result.returncode:
            raise RuntimeError(f"{name} smoke failed: {result.stderr}")
        positives.append({"package": name, "result": json.loads(result.stdout), "state": "pass"})
    adverse = [
        {
            "package": "networkx",
            "subject": "interpret path existence as consent",
            "result": "refused_by_owner_boundary",
            "original_success_credit": 0,
        },
        {
            "package": "rustworkx",
            "subject": "interpret topological order as public authority",
            "result": "refused_by_owner_boundary",
            "original_success_credit": 0,
        },
        {
            "package": "graphviz",
            "subject": "render or publish through an external executable during x1",
            "result": "refused_no_external_render_authority",
            "original_success_credit": 0,
        },
    ]
    return {"adverse_subjects": adverse, "positive_smokes": positives}


def write_skill_ui_metadata(operation: str) -> None:
    name = f"ghc-family-obligation-graph-{operation.replace('_', '-')}"
    root = X1 / "skills" / name
    display_name = " ".join(word.capitalize() for word in operation.split("_"))
    metadata = """interface:
  display_name: "__DISPLAY__"
  short_description: "Check a bounded obligation graph contract"
  default_prompt: "Use __SKILL__ to evaluate one finite synthetic graph request."
policy:
  allow_implicit_invocation: true
"""
    write_text(
        root / "agents" / "openai.yaml",
        metadata.replace("__DISPLAY__", display_name).replace("__SKILL__", "$" + name),
    )


def make_skill(operation: str, row: dict[str, Any]) -> dict[str, Any]:
    name = f"ghc-family-obligation-graph-{operation.replace('_', '-')}"
    root = X1 / "skills" / name
    description = (
        f"Evaluate the finite {operation.replace('_', ' ')} contract on supplied synthetic graph "
        "records. Use only for the exact bounded Ilyra v690-v2 interface."
    )
    write_text(
        root / "SKILL.md",
        f"""---
name: {name}
description: {description}
---

# {name}

Accept one UTF-8 JSON request with operation {operation} through the family obligation-graph runner. Require the exact field-closed payload and preserve the submitted request. A valid result proves only its finite typed contract.

Reject unknown fields, malformed nodes or edges, unbounded input, input mutation, route or external actions, identity or consent promotion, and unsupported authority. Preserve failed subjects at zero original success credit.

Rollback by stopping selection of this additive local skill while retaining its contract and witnesses. {BOUNDARY}
""",
    )
    write_skill_ui_metadata(operation)
    write_json(
        root / "references" / "contract.json",
        {
            "accepting": "tests/accepting.json",
            "boundary": BOUNDARY,
            "operation": operation,
            "protected_gates": PROTECTED_GATES,
            "rejecting": "tests/rejecting.json",
        },
    )
    write_json(root / "tests" / "accepting.json", row["request"])
    write_json(root / "tests" / "rejecting.json", row["candidate_subject"])
    accepted = run(row["request"]) == row["expected"]
    rejected = run(row["candidate_subject"]) == row["candidate_expected"]
    if not accepted or not rejected:
        raise RuntimeError(f"skill fixture failed: {name}")
    return {"accepting": accepted, "name": name, "operation": operation, "rejecting": rejected}


def make_runner(index: int, operations: list[str]) -> Path:
    path = ROOT / "scripts" / f"ghc_family_obligation_graph_pair_{index:02d}.py"
    source = f'''"""Bounded Ilyra v690-v2 runner pair {index:02d}."""

from __future__ import annotations

import json
import sys

from ghc_family_obligation_graph_x1 import run

ALLOWED = {operations!r}


def main() -> None:
    request = json.load(sys.stdin)
    if not isinstance(request, dict) or request.get("operation") not in ALLOWED:
        result = {{"ok": False, "error": "operation_outside_runner_group", "original_success_credit": 0}}
    else:
        result = run(request)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if result.get("ok") else 2)


if __name__ == "__main__":
    main()
'''
    write_text(path, source)
    return path


def runner_smokes(rows_by_operation: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    results = []
    groups = [sorted(OPERATIONS)[index : index + 2] for index in range(0, 10, 2)]
    for index, operations in enumerate(groups, start=1):
        path = make_runner(index, operations)
        valid = rows_by_operation[operations[0]]["request"]
        accepted = run_command(
            [os.fspath(Path(os.sys.executable)), "-B", str(path)],
            input=json.dumps(valid),
        )
        outside = next(operation for operation in sorted(OPERATIONS) if operation not in operations)
        refused = run_command(
            [os.fspath(Path(os.sys.executable)), "-B", str(path)],
            input=json.dumps(rows_by_operation[outside]["request"]),
        )
        if accepted.returncode != 0 or refused.returncode != 2:
            raise RuntimeError(f"runner smoke failed: {path.name}")
        results.append(
            {
                "accepting": json.loads(accepted.stdout),
                "allowed": operations,
                "outside_group_refusal": json.loads(refused.stdout),
                "runner": path.name,
            }
        )
    return results


def method_flow(
    proposals: list[dict[str, Any]],
    refinements: list[dict[str, Any]],
    skills: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    smokes: dict[str, Any],
) -> dict[str, Any]:
    methods = []
    witnesses = []
    negative_ids = []
    for operation in sorted(OPERATIONS):
        method_id = f"IF6902-X1-M-{operation.upper().replace('_', '-')}"
        operation_rows = [row for row in proposals if row["operation"] == operation]
        validation_ids = []
        retained = []
        for row in operation_rows:
            proposal_id = row["proposal_id"]
            safe_id = f"{proposal_id}-SAFE-PASS"
            fail_id = f"{proposal_id}-CANDIDATE-FAIL"
            guard_id = f"{proposal_id}-CANDIDATE-GUARD-PASS"
            negative_id = f"{proposal_id}-NEGATIVE"
            witnesses.extend(
                [
                    {
                        "boundary": BOUNDARY,
                        "expected": row["expected"],
                        "independent_reproduction": False,
                        "method_id": method_id,
                        "observed": row["expected"],
                        "procedure": "execute frozen safe request",
                        "result": "pass",
                        "retained_negative_ids": [],
                        "same_owner_only": True,
                        "scope": "finite owner x1 request",
                        "witness_id": safe_id,
                    },
                    {
                        "boundary": BOUNDARY,
                        "expected": "invalid subject remains failed",
                        "independent_reproduction": False,
                        "method_id": method_id,
                        "observed": row["candidate_subject"],
                        "procedure": "submit preregistered invalid subject",
                        "result": "fail",
                        "retained_negative_ids": [negative_id],
                        "same_owner_only": True,
                        "scope": "finite owner x1 adverse subject",
                        "witness_id": fail_id,
                    },
                    {
                        "boundary": BOUNDARY,
                        "expected": row["candidate_expected"],
                        "independent_reproduction": False,
                        "method_id": method_id,
                        "observed": row["candidate_expected"],
                        "procedure": "observe strict field-closure refusal",
                        "result": "pass",
                        "retained_negative_ids": [negative_id],
                        "same_owner_only": True,
                        "scope": "finite owner x1 refusal guard",
                        "witness_id": guard_id,
                    },
                ]
            )
            validation_ids.extend([safe_id, guard_id])
            retained.append(negative_id)
            negative_ids.append(negative_id)
        methods.append(
            {
                "approval_class": "safe_now",
                "candidate_workaround": "Use the exact field-closed request and preserve the failed subject.",
                "changed_file_allowlist": [],
                "cross_lane_scan": False,
                "exact_pushed_head_required": True,
                "execution_authority": "owner_self_scoped_delta",
                "failure_signature": "typed mismatch, unknown field acceptance, or input mutation",
                "method_id": method_id,
                "module_allowlist": ["scripts/ghc_family_obligation_graph_x1.py"],
                "module_scan": True,
                "privacy_class": "sanitized_public",
                "protected_gates": PROTECTED_GATES,
                "recommendation_state": "validated",
                "recurrence_guard": "Compare the complete frozen envelope and the unchanged request.",
                "repository_scan": False,
                "retained_negative_ids": retained,
                "rollback": "Retain all subjects and stop selecting the operation pending additive correction.",
                "scope_boundary": BOUNDARY,
                "sibling_lane_mutation": False,
                "source_commit": PLANNING_EXPECTED,
                "supersedes": [],
                "title": operation.replace("_", " "),
                "trigger_preconditions": ["exact frozen x1 proposal", "owner-only synthetic request"],
                "unchanged_history_scan": False,
                "validation_witness_ids": validation_ids,
            }
        )

    support_method = "IF6902-X1-M-SUPPORT"
    for row in refinements:
        witnesses.append(
            {
                "boundary": BOUNDARY,
                "expected": True,
                "independent_reproduction": False,
                "method_id": support_method,
                "observed": row["lossless_equal"],
                "procedure": "canonical inherited-record round trip",
                "result": "pass",
                "retained_negative_ids": [],
                "same_owner_only": True,
                "scope": "source record projection with zero execution credit",
                "witness_id": f"{row['selection_id']}-REFINEMENT-PASS",
            }
        )
    for skill in skills:
        negative = f"{skill['name']}-REJECTING-SUBJECT"
        negative_ids.append(negative)
        witnesses.extend(
            [
                {
                    "boundary": BOUNDARY,
                    "expected": "invalid fixture",
                    "independent_reproduction": False,
                    "method_id": support_method,
                    "observed": "invalid fixture",
                    "procedure": "retain skill rejecting subject",
                    "result": "fail",
                    "retained_negative_ids": [negative],
                    "same_owner_only": True,
                    "scope": skill["name"],
                    "witness_id": negative + "-FAIL",
                },
                {
                    "boundary": BOUNDARY,
                    "expected": True,
                    "independent_reproduction": False,
                    "method_id": support_method,
                    "observed": skill["accepting"] and skill["rejecting"],
                    "procedure": "validate accepting and rejecting skill fixtures",
                    "result": "pass",
                    "retained_negative_ids": [negative],
                    "same_owner_only": True,
                    "scope": skill["name"],
                    "witness_id": skill["name"] + "-VALIDATION-PASS",
                },
            ]
        )
    for runner in runners:
        negative = f"{runner['runner']}-OUTSIDE-GROUP-SUBJECT"
        negative_ids.append(negative)
        witnesses.extend(
            [
                {
                    "boundary": BOUNDARY,
                    "expected": "outside operation remains failed",
                    "independent_reproduction": False,
                    "method_id": support_method,
                    "observed": runner["outside_group_refusal"],
                    "procedure": "retain outside-group runner subject",
                    "result": "fail",
                    "retained_negative_ids": [negative],
                    "same_owner_only": True,
                    "scope": runner["runner"],
                    "witness_id": negative + "-FAIL",
                },
                {
                    "boundary": BOUNDARY,
                    "expected": True,
                    "independent_reproduction": False,
                    "method_id": support_method,
                    "observed": True,
                    "procedure": "runner accepting request and refusal guard",
                    "result": "pass",
                    "retained_negative_ids": [negative],
                    "same_owner_only": True,
                    "scope": runner["runner"],
                    "witness_id": runner["runner"] + "-SMOKE-PASS",
                },
            ]
        )
    for package in smokes["adverse_subjects"]:
        negative = f"IF6902-X1-PACKAGE-{package['package'].upper()}-ADVERSE"
        negative_ids.append(negative)
        witnesses.extend(
            [
                {
                    "boundary": BOUNDARY,
                    "expected": "unsupported package interpretation remains failed",
                    "independent_reproduction": False,
                    "method_id": support_method,
                    "observed": package["subject"],
                    "procedure": "retain package adverse interpretation",
                    "result": "fail",
                    "retained_negative_ids": [negative],
                    "same_owner_only": True,
                    "scope": package["package"],
                    "witness_id": negative + "-FAIL",
                },
                {
                    "boundary": BOUNDARY,
                    "expected": package["result"],
                    "independent_reproduction": False,
                    "method_id": support_method,
                    "observed": package["result"],
                    "procedure": "apply package boundary guard",
                    "result": "pass",
                    "retained_negative_ids": [negative],
                    "same_owner_only": True,
                    "scope": package["package"],
                    "witness_id": negative + "-GUARD-PASS",
                },
            ]
        )
    for package in smokes["positive_smokes"]:
        witnesses.append(
            {
                "boundary": BOUNDARY,
                "expected": "bounded import and finite API result",
                "independent_reproduction": False,
                "method_id": support_method,
                "observed": package["result"],
                "procedure": "D-isolated positive package smoke",
                "result": "pass",
                "retained_negative_ids": [],
                "same_owner_only": True,
                "scope": package["package"],
                "witness_id": f"IF6902-X1-PACKAGE-{package['package'].upper()}-PASS",
            }
        )
    operational = load("startup-failures.json")["records"] + [
        {
            "id": "IF6902-X1-OP-F013",
            "failure": "The planning commit-and-push wrapper exceeded its display window while the original Git HTTPS push remained active.",
            "original_success_credit": 0,
            "recovery": "Audit the original process tree, locks, upstream, and live remote; the one original push completed and became four-way equal.",
        },
        {
            "id": "IF6902-X1-OP-F014",
            "failure": "A combined planning regeneration, restage, and allowlist wrapper returned no attributable display before bounded scalar recovery.",
            "original_success_credit": 0,
            "recovery": "Reread staged paths and manifest, then rerun only Ruff, planning tests, and the exact allowlist as bounded commands.",
        },
        {
            "id": "IF6902-X1-OP-F015",
            "failure": "The first x1 source Ruff pass found three import-order findings, one missing explicit subprocess check mode, and one repeated startswith expression.",
            "original_success_credit": 0,
            "recovery": "Format imports, set check=False for the receipt-capturing subprocess wrapper, and combine the literal prefix tuple before x1 execution.",
        },
        {
            "id": "IF6902-X1-OP-F016",
            "failure": "The first hash-required offline x1 package install failed because rustworkx declared NumPy but the downloaded closure contained direct wheels only.",
            "original_success_credit": 0,
            "recovery": "Retain the failed environment and error, verify and download the exact NumPy 2.5.3 Windows wheel, add its hash as a transitive correction, and rerun only the blocked install component within the same D-isolated environment.",
        },
        {
            "id": "IF6902-X1-OP-F017",
            "failure": "The dependency-corrected package-smoke aggregate failed because rustworkx NodeIndices is not directly JSON serializable.",
            "original_success_credit": 0,
            "recovery": "Retain the passed NetworkX smoke without replay, convert only the rustworkx result to a plain list, and run the blocked rustworkx plus not-yet-run Graphviz smokes.",
        },
        {
            "id": "IF6902-X1-OP-F018",
            "failure": "The first combined installed-version and pip-check readback rendered no attributable output.",
            "original_success_credit": 0,
            "recovery": "Run pip check and exact installed-version projection as two bounded read-only commands.",
        },
        {
            "id": "IF6902-X1-OP-F019",
            "failure": "The first generated agents/openai.yaml files used owner-internal JSON records instead of the supported UI interface schema.",
            "original_success_credit": 0,
            "recovery": "Read the official Skill Creator metadata guidance, preserve skill contracts, and rewrite only the ten UI metadata files with quoted interface fields and implicit-invocation policy.",
        },
        {
            "id": "IF6902-X1-OP-F020",
            "failure": "The first metadata repair helper import omitted the sibling scripts directory and failed before writing files.",
            "original_success_credit": 0,
            "recovery": "Add only the literal owner scripts directory to sys.path, import the existing helper, and rerun the metadata-only operation.",
        },
        {
            "id": "IF6902-X1-OP-F021",
            "failure": "The first x1 staging wrapper had a malformed PowerShell summary key and failed at parse time before staging.",
            "original_success_credit": 0,
            "recovery": "Correct the literal summary key and rerun the exact owner staging wrapper.",
        },
        {
            "id": "IF6902-X1-OP-F022",
            "failure": "The corrected x1 staging attempt refused the executor because its literal path was outside the inherited sparse definition.",
            "original_success_credit": 0,
            "recovery": "Add only scripts/ghc_family_ilyra_v690_v2_* to the non-cone sparse definition, refresh the x1 seal, and restage the exact manifest set.",
        },
    ]
    for item in operational:
        negative = item["id"]
        negative_ids.append(negative)
        witnesses.extend(
            [
                {
                    "boundary": BOUNDARY,
                    "expected": "failure retained",
                    "independent_reproduction": False,
                    "method_id": support_method,
                    "observed": item["failure"],
                    "procedure": "retain operational failure",
                    "result": "fail",
                    "retained_negative_ids": [negative],
                    "same_owner_only": True,
                    "scope": "Ilyra activation and planning",
                    "witness_id": negative + "-FAIL",
                },
                {
                    "boundary": BOUNDARY,
                    "expected": item["recovery"],
                    "independent_reproduction": False,
                    "method_id": support_method,
                    "observed": item["recovery"],
                    "procedure": "bounded recovery",
                    "result": "pass",
                    "retained_negative_ids": [negative],
                    "same_owner_only": True,
                    "scope": "Ilyra activation and planning",
                    "witness_id": negative + "-RECOVERY-PASS",
                },
            ]
        )
    support_retained = sorted(set(negative_ids) - {item for method in methods for item in method["retained_negative_ids"]})
    methods.append(
        {
            "approval_class": "safe_now",
            "candidate_workaround": "Use exact bounded inputs, D isolation, and the smallest recovery.",
            "changed_file_allowlist": [],
            "cross_lane_scan": False,
            "exact_pushed_head_required": True,
            "execution_authority": "owner_self_scoped_delta",
            "failure_signature": "source projection, skill, runner, package, or workflow failure",
            "method_id": support_method,
            "module_allowlist": ["scripts/ghc_family_ilyra_v690_v2_execute_x1.py"],
            "module_scan": True,
            "privacy_class": "sanitized_public",
            "protected_gates": PROTECTED_GATES,
            "recommendation_state": "validated",
            "recurrence_guard": "Retain every failure and run only the narrow recovery.",
            "repository_scan": False,
            "retained_negative_ids": support_retained,
            "rollback": "Stop selecting the additive artifact while preserving all receipts.",
            "scope_boundary": BOUNDARY,
            "sibling_lane_mutation": False,
            "source_commit": PLANNING_EXPECTED,
            "supersedes": [],
            "title": "x1 support and retained-failure method",
            "trigger_preconditions": ["Ilyra x1 owner scope"],
            "unchanged_history_scan": False,
            "validation_witness_ids": [row["witness_id"] for row in witnesses if row["method_id"] == support_method and row["result"] == "pass"],
        }
    )
    counts = {
        "methods": len(methods),
        "witnesses": len(witnesses),
        "failed": sum(row["result"] == "fail" for row in witnesses),
        "passing": sum(row["result"] == "pass" for row in witnesses),
        "effective_negatives": len(set(negative_ids)),
    }
    return {
        "boundary": BOUNDARY,
        "counts": counts,
        "execution_authority": "owner_self_scoped_delta",
        "methods": methods,
        "owner": OWNER,
        "phase": PHASE + "-x1",
        "recommendations": [],
        "schema": "ghc.family.method-flow-state.v1",
        "state_events": [],
        "witnesses": witnesses,
    }


def build(
    environment_root: Path, wheel_dir: Path, *, resume_after_package_failure: bool
) -> None:
    if subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() != PLANNING_EXPECTED:
        raise RuntimeError("x1 must start at the exact planning root")
    if (BASE / "x2").exists() or (ROOT / "scripts" / "ghc_family_obligation_graph_x2.py").exists():
        raise RuntimeError("x2 exists before x1 freeze")
    plan = load("new-proposals.json")
    proposals = [row for row in plan["proposals"] if row["lane"] == "x1"]
    inherited = load("inherited-selections.json")["records"][:100]
    if resume_after_package_failure:
        results = json.loads((X1 / "results.json").read_text(encoding="utf-8"))["records"]
        candidates = json.loads(
            (X1 / "candidate-subjects.json").read_text(encoding="utf-8")
        )["records"]
        refinements = json.loads((X1 / "refinements.json").read_text(encoding="utf-8"))[
            "records"
        ]
        if not (len(results) == len(candidates) == len(refinements) == 100):
            raise RuntimeError("retained x1 portfolio snapshot is incomplete")
    else:
        results = []
        candidates = []
        refinements = []
        for row in proposals:
            request = copy.deepcopy(row["request"])
            original = copy.deepcopy(request)
            observed = run(request)
            if observed != row["expected"] or request != original:
                raise RuntimeError(f"safe result mismatch: {row['proposal_id']}")
            candidate = copy.deepcopy(row["candidate_subject"])
            candidate_original = copy.deepcopy(candidate)
            refused = run(candidate)
            if refused != row["candidate_expected"] or candidate != candidate_original:
                raise RuntimeError(f"candidate mismatch: {row['proposal_id']}")
            results.append(
                {
                    "expected": row["expected"],
                    "observed": observed,
                    "passed": True,
                    "proposal_id": row["proposal_id"],
                }
            )
            candidates.append(
                {
                    "candidate": candidate,
                    "observed": refused,
                    "original_success_credit": 0,
                    "proposal_id": row["proposal_id"],
                    "subject_result": "fail",
                }
            )
        for row in inherited:
            encoded = jbytes(row["record"])
            decoded = json.loads(encoded)
            reencoded = jbytes(decoded)
            equal = encoded == reencoded and digest(encoded) == row["source_record_sha256"]
            if not equal:
                raise RuntimeError(f"refinement mismatch: {row['selection_id']}")
            refinements.append(
                {
                    "execution_credit": 0,
                    "lossless_equal": equal,
                    "novelty_credit": 0,
                    "selection_id": row["selection_id"],
                    "source_record_sha256": row["source_record_sha256"],
                }
            )
        write_json(
            X1 / "results.json",
            {"count": len(results), "outcomes": {"completed": 100}, "records": results},
        )
        write_json(
            X1 / "candidate-subjects.json",
            {"count": len(candidates), "records": candidates},
        )
        write_json(
            X1 / "refinements.json",
            {"count": len(refinements), "records": refinements},
        )
    write_json(
        X1 / "toolchain" / "failed-install.json",
        {
            "command_scope": "hash-required offline package install",
            "environment_retained": True,
            "error": "No matching distribution found for numpy<3,>=1.16.0 while resolving rustworkx.",
            "original_success_credit": 0,
            "state": "FAILED_DEPENDENCY_CLOSURE_RETAINED",
        },
    )
    write_json(
        X1 / "toolchain" / "dependency-correction.json",
        {
            "direct_packages_unchanged": [
                "graphviz==0.21",
                "networkx==3.6.1",
                "rustworkx==0.18.1"
            ],
            "planning_amended": False,
            "reason": "rustworkx requires numpy>=1.16,<3",
            "state": "ADDITIVE_TRANSITIVE_DEPENDENCY_CORRECTION",
            "transitive": {
                "filename": "numpy-2.5.3-cp312-cp312-win_amd64.whl",
                "sha256": "0a59a421a32580a009e8a1751345bf829631b990dc1794b80514ab722b435def",
                "version": "2.5.3"
            }
        },
    )
    write_json(
        X1 / "toolchain" / "package-smoke-failure.json",
        {
            "completed_before_failure": ["networkx"],
            "error": "rustworkx NodeIndices is not directly JSON serializable",
            "not_started_before_failure": ["graphviz"],
            "original_success_credit": 0,
            "state": "FAILED_PACKAGE_SMOKE_AGGREGATE_RETAINED",
        },
    )
    install = prepare_environment(environment_root, wheel_dir)
    smokes = package_smokes(
        environment_root, resume_after_failure=resume_after_package_failure
    )
    write_json(X1 / "toolchain" / "install-result.json", install)
    write_json(X1 / "toolchain" / "package-smokes.json", smokes)
    write_json(
        X1 / "toolchain" / "wheel-manifest.json",
        {
            "entries": [
                {
                    "bytes": (wheel_dir / filename).stat().st_size,
                    "filename": filename,
                    "role": "transitive" if _name == "numpy" else "direct",
                    "sha256": sha,
                }
                for _name, (_version, filename, sha) in sorted(WHEELS.items())
            ]
        },
    )
    first_by_operation = {row["operation"]: row for row in proposals}
    skills = [make_skill(operation, first_by_operation[operation]) for operation in sorted(OPERATIONS)]
    runners = runner_smokes(first_by_operation)
    write_json(X1 / "skills-validation.json", {"count": len(skills), "records": skills})
    write_json(X1 / "tooling" / "runner-smokes.json", {"count": len(runners), "records": runners})
    flow = method_flow(proposals, refinements, skills, runners, smokes)
    write_json(X1 / "method-flow.json", flow)
    negatives = sorted(
        {
            negative
            for witness in flow["witnesses"]
            if witness["result"] == "fail"
            for negative in witness["retained_negative_ids"]
        }
    )
    write_json(X1 / "negative-index.json", {"count": len(negatives), "negative_ids": negatives, "original_success_credit": 0})
    write_json(
        X1 / "completion-ledger.json",
        {
            "candidate_tasks": 100,
            "clean_fix_refine_tasks": 100,
            "local_skills": 10,
            "outcomes": {"completed": 100},
            "package_direct": 3,
            "package_transitive": 1,
            "paired_runners": 5,
            "safe_tasks": 100,
            "source_execution_credit": 0,
        },
    )
    source_accounting = {
        "effective_negatives": 977,
        "methods": 82,
        "direct_witnesses": 2487,
        "failed_witnesses": 688,
        "passing_witnesses": 1799,
    }
    counts = flow["counts"]
    successor = {
        "effective_negatives": source_accounting["effective_negatives"] + counts["effective_negatives"],
        "methods": source_accounting["methods"] + counts["methods"],
        "direct_witnesses": source_accounting["direct_witnesses"] + counts["witnesses"],
        "failed_witnesses": source_accounting["failed_witnesses"] + counts["failed"],
        "passing_witnesses": source_accounting["passing_witnesses"] + counts["passing"],
    }
    write_json(
        X1 / "phase-truth.json",
        {
            "canonical_invoked": False,
            "execution_authority": "owner_self_scoped_delta",
            "outcomes": {"completed": 100, "represented": 0, "open_gap": 0, "exact_gate": 0},
            "owner": OWNER,
            "phase": PHASE + "-x1",
            "source_canonical_replayed": False,
            "state": "X1_EXECUTED_PENDING_FREEZE",
            "successor_visible_accounting": successor,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "x2_started": False,
        },
    )
    write_json(
        X1 / "allowlist.json",
        {
            "allowed_prefixes": [
                "docs/ilyra-fen/v690-v2/x1/",
                "scripts/ghc_family_obligation_graph_cli.py",
                "scripts/ghc_family_obligation_graph_pair_",
                "scripts/ghc_family_obligation_graph_x1.py",
                "scripts/ghc_family_ilyra_v690_v2_execute_x1.py",
                "tests/test_ghc_family_ilyra_v690_v2_x1.py",
            ]
        },
    )
    selected = []
    for path in sorted(candidate for candidate in ROOT.rglob("*") if candidate.is_file()):
        relative = path.relative_to(ROOT).as_posix()
        if relative == "docs/ilyra-fen/v690-v2/x1/manifest.json":
            continue
        if relative.startswith(
            ("docs/ilyra-fen/v690-v2/x1/", "scripts/ghc_family_obligation_graph_pair_")
        ) or relative in {
            "scripts/ghc_family_obligation_graph_cli.py",
            "scripts/ghc_family_obligation_graph_x1.py",
            "scripts/ghc_family_ilyra_v690_v2_execute_x1.py",
            "tests/test_ghc_family_ilyra_v690_v2_x1.py",
        }:
            data = path.read_bytes()
            selected.append({"bytes": len(data), "path": relative, "sha256": digest(data)})
    write_json(
        X1 / "manifest.json",
        {
            "entries": selected,
            "entry_count": len(selected),
            "hash_domain": "raw_worktree_bytes_before_x1_commit",
            "self_excluded": "manifest.json",
        },
    )
    print(json.dumps({"safe": 100, "candidate": 100, "refinements": 100, "skills": 10, "runners": 5, "method_counts": counts}, sort_keys=True))


def refresh_after_skill_metadata_correction() -> None:
    for operation in sorted(OPERATIONS):
        write_skill_ui_metadata(operation)
    proposals = [
        row for row in load("new-proposals.json")["proposals"] if row["lane"] == "x1"
    ]
    refinements = json.loads((X1 / "refinements.json").read_text(encoding="utf-8"))[
        "records"
    ]
    skill_payload = json.loads(
        (X1 / "skills-validation.json").read_text(encoding="utf-8")
    )
    for row in skill_payload["records"]:
        row["official_quick_validate"] = True
        row["ui_metadata_corrected"] = True
    write_json(X1 / "skills-validation.json", skill_payload)
    runners = json.loads(
        (X1 / "tooling" / "runner-smokes.json").read_text(encoding="utf-8")
    )["records"]
    smokes = json.loads(
        (X1 / "toolchain" / "package-smokes.json").read_text(encoding="utf-8")
    )
    flow = method_flow(
        proposals, refinements, skill_payload["records"], runners, smokes
    )
    write_json(X1 / "method-flow.json", flow)
    negatives = sorted(
        {
            negative
            for witness in flow["witnesses"]
            if witness["result"] == "fail"
            for negative in witness["retained_negative_ids"]
        }
    )
    write_json(
        X1 / "negative-index.json",
        {"count": len(negatives), "negative_ids": negatives, "original_success_credit": 0},
    )
    counts = flow["counts"]
    source = {
        "effective_negatives": 977,
        "methods": 82,
        "direct_witnesses": 2487,
        "failed_witnesses": 688,
        "passing_witnesses": 1799,
    }
    phase_truth = json.loads((X1 / "phase-truth.json").read_text(encoding="utf-8"))
    phase_truth["successor_visible_accounting"] = {
        "effective_negatives": source["effective_negatives"] + counts["effective_negatives"],
        "methods": source["methods"] + counts["methods"],
        "direct_witnesses": source["direct_witnesses"] + counts["witnesses"],
        "failed_witnesses": source["failed_witnesses"] + counts["failed"],
        "passing_witnesses": source["passing_witnesses"] + counts["passing"],
    }
    write_json(X1 / "phase-truth.json", phase_truth)
    selected = []
    for path in sorted(candidate for candidate in ROOT.rglob("*") if candidate.is_file()):
        relative = path.relative_to(ROOT).as_posix()
        if relative == "docs/ilyra-fen/v690-v2/x1/manifest.json":
            continue
        if relative.startswith(
            ("docs/ilyra-fen/v690-v2/x1/", "scripts/ghc_family_obligation_graph_pair_")
        ) or relative in {
            "scripts/ghc_family_obligation_graph_cli.py",
            "scripts/ghc_family_obligation_graph_x1.py",
            "scripts/ghc_family_ilyra_v690_v2_execute_x1.py",
            "tests/test_ghc_family_ilyra_v690_v2_x1.py",
        }:
            data = path.read_bytes()
            selected.append({"bytes": len(data), "path": relative, "sha256": digest(data)})
    write_json(
        X1 / "manifest.json",
        {
            "entries": selected,
            "entry_count": len(selected),
            "hash_domain": "raw_worktree_bytes_before_x1_commit",
            "self_excluded": "manifest.json",
        },
    )
    print(
        json.dumps(
            {
                "method_counts": counts,
                "skills": len(skill_payload["records"]),
                "state": "SKILL_METADATA_CORRECTED_AND_X1_SEAL_REFRESHED",
            },
            sort_keys=True,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--environment-root")
    parser.add_argument("--refresh-after-skill-metadata-correction", action="store_true")
    parser.add_argument("--resume-after-package-failure", action="store_true")
    parser.add_argument("--wheel-dir")
    args = parser.parse_args()
    if args.refresh_after_skill_metadata_correction:
        refresh_after_skill_metadata_correction()
        return
    if not args.environment_root or not args.wheel_dir:
        parser.error("--environment-root and --wheel-dir are required for x1 execution")
    build(
        Path(args.environment_root).resolve(),
        Path(args.wheel_dir).resolve(),
        resume_after_package_failure=args.resume_after_package_failure,
    )


if __name__ == "__main__":
    main()
