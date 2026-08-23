#!/usr/bin/env python3
"""One-shot, D-first bounded smoke tribunal for Eiren v667-v6-r2 tools.

The script never uploads, publishes, installs, or edits the repository.  Its
fixtures and receipts live under the phase's disposable D-first temp root.
An initial run exercises every direct tool once.  If a tool fails because the
tribunal itself needs correction, ``--recover NAME`` reruns only that failed
dependency and leaves all passing witnesses untouched.
"""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import subprocess
import sys
import traceback
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
DRIVE_ROOT = Path(ROOT.anchor)
ENV_ROOT = DRIVE_ROOT / "GHC-Archives" / "global-tools" / "python" / "eiren-kestrel-v667-v6-r2"
TEMP_ROOT = DRIVE_ROOT / "GHC-Archives" / "phase-temp" / "eiren-kestrel-v667-v6-r2"
SMOKE_ROOT = TEMP_ROOT / "tool-smoke"
PYTHON = ENV_ROOT / "Scripts" / "python.exe"
SCRIPTS = ENV_ROOT / "Scripts"

TOOLS = (
    "validate-pyproject",
    "pyproject-fmt",
    "deptry",
    "vulture",
    "radon",
    "xenon",
    "codespell",
    "yamllint",
    "toml-sort",
    "pip-licenses",
    "cyclonedx-bom",
    "check-manifest",
    "twine",
)

DIST_NAMES = {
    "validate-pyproject": "validate-pyproject",
    "pyproject-fmt": "pyproject-fmt",
    "deptry": "deptry",
    "vulture": "vulture",
    "radon": "radon",
    "xenon": "xenon",
    "codespell": "codespell",
    "yamllint": "yamllint",
    "toml-sort": "toml-sort",
    "pip-licenses": "pip-licenses",
    "cyclonedx-bom": "cyclonedx-bom",
    "check-manifest": "check-manifest",
    "twine": "twine",
}

EXECUTABLES = {
    "validate-pyproject": "validate-pyproject.exe",
    "pyproject-fmt": "pyproject-fmt.exe",
    "deptry": "deptry.exe",
    "vulture": "vulture.exe",
    "radon": "radon.exe",
    "xenon": "xenon.exe",
    "codespell": "codespell.exe",
    "yamllint": "yamllint.exe",
    "toml-sort": "toml-sort.exe",
    "pip-licenses": "pip-licenses.exe",
    "cyclonedx-bom": "cyclonedx-py.exe",
    "check-manifest": "check-manifest.exe",
    "twine": "twine.exe",
}


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def sanitize(value: str) -> str:
    replacements = (
        (str(SMOKE_ROOT), "<D_SMOKE_ROOT>"),
        (str(TEMP_ROOT), "<D_PHASE_TEMP>"),
        (str(ENV_ROOT), "<D_TOOL_ENV>"),
        (str(DRIVE_ROOT), "<D_ROOT>"),
    )
    for source, replacement in replacements:
        value = value.replace(source, replacement).replace(source.replace("\\", "/"), replacement)
    return value[-8000:]


def invoke(tool: str, args: list[str], cwd: Path | None = None, timeout: int = 120) -> dict[str, object]:
    executable = SCRIPTS / EXECUTABLES[tool]
    completed = subprocess.run(
        [str(executable), *args],
        cwd=str(cwd or SMOKE_ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=timeout,
    )
    return {
        "tool": tool,
        "argv": [EXECUTABLES[tool], *[sanitize(arg) for arg in args]],
        "cwd": "<D_SMOKE_ROOT>",
        "exit_code": completed.returncode,
        "stdout": sanitize(completed.stdout.decode("utf-8", errors="replace")),
        "stderr": sanitize(completed.stderr.decode("utf-8", errors="replace")),
    }


def invoke_python(args: list[str], cwd: Path, timeout: int = 120) -> dict[str, object]:
    completed = subprocess.run(
        [str(PYTHON), *args],
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=timeout,
    )
    return {
        "tool": "python",
        "argv": ["python.exe", *[sanitize(arg) for arg in args]],
        "cwd": "<D_SMOKE_ROOT>",
        "exit_code": completed.returncode,
        "stdout": sanitize(completed.stdout.decode("utf-8", errors="replace")),
        "stderr": sanitize(completed.stderr.decode("utf-8", errors="replace")),
    }


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def smoke_validate_pyproject(root: Path) -> dict[str, object]:
    good = root / "good.toml"
    bad = root / "bad.toml"
    write_text(good, """
[build-system]
requires = ["setuptools>=77"]
build-backend = "setuptools.build_meta"

[project]
name = "bounded-smoke"
version = "0.0.0"
requires-python = ">=3.11"
""")
    write_text(bad, """
[project]
name = "Not A Valid Distribution Name!"
version = "not-a-version"
""")
    negative = invoke("validate-pyproject", [str(bad)], root)
    positive = invoke("validate-pyproject", [str(good)], root)
    require(negative["exit_code"] != 0, "invalid pyproject was accepted")
    require(positive["exit_code"] == 0, "valid pyproject was rejected")
    return {"negative": negative, "positive": positive}


def smoke_pyproject_fmt(root: Path) -> dict[str, object]:
    path = root / "pyproject.toml"
    write_text(path, """
[project]
version="0.0.0"
name="bounded-fmt"
requires-python=">=3.11"
""")
    common = ["--no-generate-python-version-classifiers", str(path)]
    negative = invoke("pyproject-fmt", ["--check", *common], root)
    formatted = invoke("pyproject-fmt", common, root)
    positive = invoke("pyproject-fmt", ["--check", *common], root)
    require(negative["exit_code"] != 0, "unformatted pyproject was accepted")
    # pyproject-fmt deliberately returns 1 when it changes a file, including in
    # write mode; the second check must then return 0 to prove idempotence.
    require(formatted["exit_code"] == 1 and positive["exit_code"] == 0, "format/idempotence check failed")
    return {"negative": negative, "format": formatted, "positive": positive}


def smoke_deptry(root: Path) -> dict[str, object]:
    source = root / "src" / "bounded_deptry" / "__init__.py"
    config = root / "pyproject.toml"
    write_text(source, "import requests\nVALUE = requests.__version__")
    write_text(config, """
[project]
name = "bounded-deptry"
version = "0.0.0"
dependencies = []
""")
    negative = invoke("deptry", [str(root / "src"), "--config", str(config), "--no-ansi"], root)
    write_text(config, """
[project]
name = "bounded-deptry"
version = "0.0.0"
dependencies = ["requests==2.34.2"]
""")
    positive = invoke("deptry", [str(root / "src"), "--config", str(config), "--no-ansi"], root)
    require(negative["exit_code"] != 0, "undeclared import was accepted")
    require(positive["exit_code"] == 0, "declared import was rejected")
    return {"negative": negative, "positive": positive}


def smoke_vulture(root: Path) -> dict[str, object]:
    path = root / "sample.py"
    write_text(path, "def unused_value():\n    return 1")
    negative = invoke("vulture", [str(path), "--min-confidence", "60"], root)
    write_text(path, "def used_value():\n    return 1\n\nif __name__ == '__main__':\n    print(used_value())")
    positive = invoke("vulture", [str(path), "--min-confidence", "60"], root)
    require(negative["exit_code"] != 0, "unused function was accepted")
    require(positive["exit_code"] == 0, "used function was rejected")
    return {"negative": negative, "positive": positive}


def smoke_radon(root: Path) -> dict[str, object]:
    path = root / "sample.py"
    write_text(path, "def bounded(value: int) -> int:\n    if value > 0:\n        return value\n    return 0")
    cc = invoke("radon", ["cc", "-s", "-a", str(path)], root)
    mi = invoke("radon", ["mi", "-s", str(path)], root)
    require(cc["exit_code"] == 0 and "Average complexity" in str(cc["stdout"]), "complexity report failed")
    require(mi["exit_code"] == 0 and str(path.name) in str(mi["stdout"]), "maintainability report failed")
    return {"complexity": cc, "maintainability": mi}


def smoke_xenon(root: Path) -> dict[str, object]:
    path = root / "sample.py"
    write_text(path, """
def complex_value(a, b, c, d, e, f, g, h):
    total = 0
    if a: total += 1
    if b: total += 1
    if c: total += 1
    if d: total += 1
    if e: total += 1
    if f: total += 1
    if g: total += 1
    if h: total += 1
    return total
""")
    negative = invoke("xenon", ["-b", "A", "-m", "A", "-a", "A", str(path)], root)
    write_text(path, "def simple_value(value):\n    return value + 1")
    positive = invoke("xenon", ["-b", "A", "-m", "A", "-a", "A", str(path)], root)
    require(negative["exit_code"] != 0, "complexity threshold did not reject fixture")
    require(positive["exit_code"] == 0, "simple fixture failed complexity threshold")
    return {"negative": negative, "positive": positive}


def smoke_codespell(root: Path) -> dict[str, object]:
    path = root / "words.txt"
    write_text(path, "teh bounded witness")
    negative = invoke("codespell", ["--disable-colors", str(path)], root)
    write_text(path, "the bounded witness")
    positive = invoke("codespell", ["--disable-colors", str(path)], root)
    require(negative["exit_code"] != 0, "known typo was accepted")
    require(positive["exit_code"] == 0, "corrected text was rejected")
    return {"negative": negative, "positive": positive}


def smoke_yamllint(root: Path) -> dict[str, object]:
    path = root / "sample.yaml"
    write_text(path, "key: one\nkey: two")
    negative = invoke("yamllint", ["-f", "parsable", str(path)], root)
    write_text(path, "key: value\nitems:\n  - one")
    positive = invoke("yamllint", ["-f", "parsable", str(path)], root)
    require(negative["exit_code"] != 0, "duplicate YAML key was accepted")
    require(positive["exit_code"] == 0, "valid YAML was rejected")
    return {"negative": negative, "positive": positive}


def smoke_toml_sort(root: Path) -> dict[str, object]:
    path = root / "sample.toml"
    write_text(path, """
[tool.z]
b = 2
a = 1

[tool.a]
z = 3
""")
    common = ["--sort-table-keys", str(path)]
    negative = invoke("toml-sort", ["--check", *common], root)
    sorted_run = invoke("toml-sort", ["--in-place", *common], root)
    positive = invoke("toml-sort", ["--check", *common], root)
    require(negative["exit_code"] != 0, "unsorted TOML was accepted")
    require(sorted_run["exit_code"] == 0 and positive["exit_code"] == 0, "sort/idempotence check failed")
    return {"negative": negative, "sort": sorted_run, "positive": positive}


def smoke_pip_licenses(root: Path) -> dict[str, object]:
    output = root / "licenses.json"
    result = invoke("pip-licenses", ["--format", "json", "--output-file", str(output)], root)
    require(result["exit_code"] == 0 and output.is_file(), "license inventory failed")
    payload = json.loads(output.read_text(encoding="utf-8-sig"))
    require(isinstance(payload, list) and len(payload) >= 13, "license inventory was incomplete")
    return {"positive": result, "package_count": len(payload), "output": "licenses.json"}


def smoke_cyclonedx(root: Path) -> dict[str, object]:
    output = root / "sbom.json"
    result = invoke(
        "cyclonedx-bom",
        ["environment", str(PYTHON), "--output-reproducible", "--output-format", "JSON", "--output-file", str(output), "--validate"],
        root,
    )
    require(result["exit_code"] == 0 and output.is_file(), "SBOM generation failed")
    payload = json.loads(output.read_text(encoding="utf-8"))
    require(payload.get("bomFormat") == "CycloneDX" and len(payload.get("components", [])) >= 13, "SBOM was incomplete")
    return {"positive": result, "component_count": len(payload["components"]), "output": "sbom.json"}


def smoke_check_manifest(root: Path) -> dict[str, object]:
    project = root / "project"
    write_text(project / "pyproject.toml", """
[build-system]
requires = ["setuptools>=77"]
build-backend = "setuptools.build_meta"

[project]
name = "bounded-manifest"
version = "0.0.0"
readme = "README.md"
""")
    write_text(project / "README.md", "# Bounded manifest")
    write_text(project / "src" / "bounded_manifest" / "__init__.py", "VALUE = 1")
    write_text(project / "docs" / "guide.md", "# Tracked guide")
    subprocess.run(["git", "init", "-q", str(project)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    subprocess.run(["git", "-C", str(project), "add", "."], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    common = ["--no-build-isolation", "--python", str(PYTHON), str(project)]
    negative = invoke("check-manifest", common, root)
    write_text(project / "MANIFEST.in", "include docs/guide.md")
    subprocess.run(["git", "-C", str(project), "add", "MANIFEST.in"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    positive = invoke("check-manifest", common, root)
    require(negative["exit_code"] != 0, "missing manifest declaration was accepted")
    require(positive["exit_code"] == 0, "complete manifest was rejected")
    return {"negative": negative, "positive": positive}


def smoke_twine(root: Path) -> dict[str, object]:
    project = root / "project"
    dist = root / "dist"
    write_text(project / "pyproject.toml", """
[build-system]
requires = ["setuptools>=77"]
build-backend = "setuptools.build_meta"

[project]
name = "bounded-twine"
version = "0.0.0"
description = "A disposable local metadata fixture"
readme = "README.md"
requires-python = ">=3.11"
license = "MIT"
""")
    write_text(project / "README.md", "# Bounded Twine\n\nLocal smoke fixture only.")
    write_text(project / "src" / "bounded_twine" / "__init__.py", "VALUE = 1")
    built = invoke_python(["-m", "build", "--sdist", "--no-isolation", "--outdir", str(dist), str(project)], root)
    require(built["exit_code"] == 0, "local sdist build failed")
    artifact = next(dist.glob("*.tar.gz"), None)
    require(artifact is not None, "local sdist was not created")
    bad = root / "not-a-distribution.txt"
    write_text(bad, "not a distribution")
    negative = invoke("twine", ["check", str(bad)], root)
    positive = invoke("twine", ["check", str(artifact)], root)
    require(negative["exit_code"] != 0, "non-distribution was accepted")
    require(positive["exit_code"] == 0, "valid local sdist metadata was rejected")
    return {"build": built, "negative": negative, "positive": positive, "upload_count": 0}


SMOKES: dict[str, Callable[[Path], dict[str, object]]] = {
    "validate-pyproject": smoke_validate_pyproject,
    "pyproject-fmt": smoke_pyproject_fmt,
    "deptry": smoke_deptry,
    "vulture": smoke_vulture,
    "radon": smoke_radon,
    "xenon": smoke_xenon,
    "codespell": smoke_codespell,
    "yamllint": smoke_yamllint,
    "toml-sort": smoke_toml_sort,
    "pip-licenses": smoke_pip_licenses,
    "cyclonedx-bom": smoke_cyclonedx,
    "check-manifest": smoke_check_manifest,
    "twine": smoke_twine,
}


def execute(tool: str, mode: str) -> dict[str, object]:
    fixture = SMOKE_ROOT / ("initial" if mode == "initial" else "recovery") / tool
    fixture.mkdir(parents=True, exist_ok=False)
    try:
        details = SMOKES[tool](fixture)
        return {
            "tool": tool,
            "distribution": DIST_NAMES[tool],
            "version": importlib.metadata.version(DIST_NAMES[tool]),
            "status": "PASS",
            "bounded_use_completed": True,
            "real_world_action_count": 0,
            "upload_count": 0,
            "details": details,
        }
    except Exception as exc:  # retained verbatim only in external sanitized receipt
        return {
            "tool": tool,
            "distribution": DIST_NAMES[tool],
            "version": importlib.metadata.version(DIST_NAMES[tool]),
            "status": "FAIL",
            "bounded_use_completed": False,
            "real_world_action_count": 0,
            "upload_count": 0,
            "error": sanitize(f"{type(exc).__name__}: {exc}"),
            "traceback": sanitize(traceback.format_exc()),
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--recover", choices=TOOLS)
    args = parser.parse_args()
    SMOKE_ROOT.mkdir(parents=True, exist_ok=True)
    if args.recover:
        initial_path = SMOKE_ROOT / "tool-smoke-initial.json"
        if not initial_path.is_file():
            raise RuntimeError("initial receipt missing")
        initial = json.loads(initial_path.read_text(encoding="utf-8"))
        prior = next(row for row in initial["results"] if row["tool"] == args.recover)
        if prior["status"] != "FAIL":
            raise RuntimeError("recovery is allowed only for a failed initial dependency")
        receipt_path = SMOKE_ROOT / f"tool-smoke-recovery-{args.recover}.json"
        if receipt_path.exists():
            raise RuntimeError("recovery already attempted; no replay allowed")
        result = execute(args.recover, "recovery")
        receipt = {
            "schema": "ghc-family-bounded-tool-smoke-recovery-v1",
            "mode": "isolated_dependency_recovery",
            "tool": args.recover,
            "invocation_count": 1,
            "replayed_passing_components": 0,
            "result": result,
        }
        write_json(receipt_path, receipt)
        print(json.dumps({"tool": args.recover, "status": result["status"]}, sort_keys=True))
        return 0 if result["status"] == "PASS" else 1

    receipt_path = SMOKE_ROOT / "tool-smoke-initial.json"
    if receipt_path.exists():
        raise RuntimeError("initial tool smoke already invoked; no replay allowed")
    results = [execute(tool, "initial") for tool in TOOLS]
    passed = sum(row["status"] == "PASS" for row in results)
    receipt = {
        "schema": "ghc-family-bounded-tool-smoke-initial-v1",
        "mode": "initial_thirteen_tool_component_tribunal",
        "invocation_count": 1,
        "replayed": False,
        "tool_count": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "results": results,
    }
    write_json(receipt_path, receipt)
    print(json.dumps({"failed": len(results) - passed, "passed": passed, "tool_count": len(results)}, sort_keys=True))
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
