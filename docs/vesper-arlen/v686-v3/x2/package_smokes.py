"""Exercise the three Vesper v686-v3 D-isolated package additions."""

from __future__ import annotations

import argparse
import configparser
import hashlib
import importlib.metadata
import json
from pathlib import Path

import immutables
import tomlkit
from configupdater import ConfigUpdater


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    checks: list[dict] = []

    text = "# retained note\n[service]\nport = 8000\n"
    document = tomlkit.parse(text)
    document["service"]["port"] = 8100
    rendered = tomlkit.dumps(document)
    checks.append({"name": "tomlkit_style_edit", "pass": "# retained note" in rendered and "port = 8100" in rendered, "observed": rendered, "rejected": False})
    checks.append({"name": "tomlkit_typed_value", "pass": document["service"]["port"] == 8100 and type(document["service"]["port"].unwrap()) is int, "observed": document["service"]["port"].unwrap(), "rejected": False})
    try:
        tomlkit.parse("a = 1\na = 2\n")
        duplicate_toml = False
        toml_error = "not_rejected"
    except Exception as exc:  # library-specific parse exception is the evidence
        duplicate_toml = True
        toml_error = type(exc).__name__
    checks.append({"name": "tomlkit_duplicate_key_refusal", "pass": duplicate_toml, "observed": toml_error, "rejected": True, "success_credit": 0})

    base = immutables.Map({"mode": "base", "count": 1})
    derived = base.set("mode", "review").set("approved", False)
    checks.append({"name": "immutables_prior_retained", "pass": dict(base) == {"mode": "base", "count": 1}, "observed": dict(base), "rejected": False})
    checks.append({"name": "immutables_derived_snapshot", "pass": dict(derived) == {"mode": "review", "count": 1, "approved": False}, "observed": dict(derived), "rejected": False})
    try:
        base.delete("missing")
        missing_delete = False
        map_error = "not_rejected"
    except KeyError as exc:
        missing_delete = True
        map_error = type(exc).__name__
    checks.append({"name": "immutables_missing_delete_refusal", "pass": missing_delete and dict(base) == {"mode": "base", "count": 1}, "observed": map_error, "rejected": True, "success_credit": 0})

    ini = "# retained note\n[service]\nPort = 8000\n"
    updater = ConfigUpdater()
    updater.optionxform = str
    updater.read_string(ini)
    updater["service"]["Port"].value = "9000"
    updated = str(updater)
    checks.append({"name": "configupdater_comment_case", "pass": "# retained note" in updated and "Port = 9000" in updated, "observed": updated, "rejected": False})
    checks.append({"name": "configupdater_single_target", "pass": list(updater.sections()) == ["service"] and list(updater["service"].keys()) == ["Port"], "observed": {"sections": list(updater.sections()), "keys": list(updater["service"].keys())}, "rejected": False})
    try:
        duplicate = ConfigUpdater()
        duplicate.read_string("[service]\nPort = 1\nPort = 2\n")
        duplicate_ini = False
        ini_error = "not_rejected"
    except (configparser.DuplicateOptionError, ValueError) as exc:
        duplicate_ini = True
        ini_error = type(exc).__name__
    checks.append({"name": "configupdater_duplicate_option_refusal", "pass": duplicate_ini, "observed": ini_error, "rejected": True, "success_credit": 0})

    packages = sorted(
        (distribution.metadata["Name"], distribution.version)
        for distribution in importlib.metadata.distributions()
        if distribution.metadata["Name"].lower() in {"tomlkit", "immutables", "configupdater"}
    )
    payload = {
        "schema": "ghc.family.package-smokes.v686.v3",
        "owner": "Vesper Arlen",
        "phase": "v686-v3",
        "packages": packages,
        "checks": checks,
        "check_count": len(checks),
        "rejected_adversaries": sum(bool(check.get("rejected")) for check in checks),
        "pass": len(checks) == 9 and all(check["pass"] for check in checks),
        "same_owner_only": True,
        "independent_reproduction": False,
        "boundary": "Package smokes are local synthetic software evidence, not exhaustive security, production certification, legal review, professional validation, or Stage 20 authority.",
    }
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("xb") as handle:
        handle.write(encoded)
    print(json.dumps({"pass": payload["pass"], "checks": len(checks), "rejected": payload["rejected_adversaries"], "sha256": hashlib.sha256(encoded).hexdigest()}))
    return 0 if payload["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
