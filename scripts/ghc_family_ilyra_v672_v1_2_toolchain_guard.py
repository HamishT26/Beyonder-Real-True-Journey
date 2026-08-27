from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


def run_process(command: list[str], cwd: Path, stdin: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        input=stdin,
        capture_output=True,
        check=False,
        encoding="utf-8",
        errors="replace",
    )


def run_smokes(node_root: Path) -> dict[str, Any]:
    node = "node"
    biome = node_root / "node_modules" / ".bin" / "biome.cmd"
    if not biome.exists():
        raise FileNotFoundError(biome)

    formatted = run_process(
        [str(biome), "format", "--stdin-file-path", "fixture.json"],
        node_root,
        '{"owner":"Ilyra Fen","count":2}\n',
    )
    malformed = run_process(
        [str(biome), "check", "--stdin-file-path", "fixture.json"],
        node_root,
        '{"owner":',
    )

    program = r"""
const Ajv = require('ajv');
const YAML = require('yaml');
const stable = require('json-stable-stringify');
const semver = require('semver');
const ajv = new Ajv();
const validate = ajv.compile({type:'object', required:['count'], properties:{count:{type:'integer', minimum:1}}, additionalProperties:false});
const valid = validate({count:2});
const invalid = validate({count:0});
const yamlValue = YAML.parse('owner: Ilyra Fen\ncount: 2\n');
const duplicateDoc = YAML.parseDocument('owner: first\nowner: second\n', {uniqueKeys:true});
const stableValue = stable({z:1,a:2});
const semverValid = semver.satisfies('2.5.10', '>=2.0.0 <3.0.0');
const semverReject = !semver.valid('2.5');
console.log(JSON.stringify({
  ajv:{positive:valid === true, rejecting:invalid === false},
  yaml:{positive:yamlValue.owner === 'Ilyra Fen' && yamlValue.count === 2, rejecting:duplicateDoc.errors.length > 0},
  stable:{positive:stableValue === '{"a":2,"z":1}', rejecting:stable({z:1,a:3}) !== stableValue},
  semver:{positive:semverValid === true, rejecting:semverReject === true}
}));
"""
    libraries = run_process([node, "-e", program], node_root)
    library_results: dict[str, dict[str, bool]] = {}
    if libraries.returncode == 0:
        library_results = json.loads(libraries.stdout)

    results: dict[str, Any] = {
        "@biomejs/biome": {
            "positive": formatted.returncode == 0 and "Ilyra Fen" in formatted.stdout,
            "rejecting": malformed.returncode != 0,
            "boundary": "stdin-only synthetic JSON formatting and rejection",
        },
        "ajv": {**library_results.get("ajv", {}), "boundary": "one synthetic JSON Schema"},
        "yaml": {**library_results.get("yaml", {}), "boundary": "synthetic YAML parse and duplicate-key refusal"},
        "json-stable-stringify": {**library_results.get("stable", {}), "boundary": "deterministic in-memory serialization"},
        "semver": {**library_results.get("semver", {}), "boundary": "schema-tool version range only"},
    }
    passed = all(row.get("positive") is True and row.get("rejecting") is True for row in results.values())
    return {
        "schema": "ghc.family.ilyra.node-tool-smoke.v1",
        "passed": passed,
        "direct_surfaces": 5,
        "results": results,
        "diagnostics": {
            "biome_positive_exit": formatted.returncode,
            "biome_rejecting_exit": malformed.returncode,
            "library_exit": libraries.returncode,
            "library_stderr": libraries.stderr[-1000:],
        },
        "external_actions": 0,
        "production_result": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--node-root", type=Path, required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_smokes(args.node_root.resolve())
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("PASS" if result["passed"] else "FAIL")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
