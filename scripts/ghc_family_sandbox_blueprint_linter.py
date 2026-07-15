#!/usr/bin/env python3
"""Lint sanitized Windows Sandbox templates without launching a sandbox."""

from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path

TOKENS = {
    "__HOST_BOOTSTRAP__": r"C:\GHC\Bootstrap",
    "__HOST_INPUT__": r"C:\GHC\Input",
    "__HOST_OUTPUT__": r"C:\GHC\Output",
}


def lint(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    materialized = raw
    for token, value in TOKENS.items():
        materialized = materialized.replace(token, value)
    checks: dict[str, bool] = {"all_placeholders_resolved": "__HOST_" not in materialized}
    try:
        root = ET.fromstring(materialized)
    except ET.ParseError as exc:
        return {"template": path.name, "valid": False, "checks": checks, "error": str(exc)}
    checks["root_configuration"] = root.tag == "Configuration"
    checks["networking_disabled"] = (root.findtext("Networking") or "").casefold() == "disable"
    checks["vgpu_disabled"] = (root.findtext("VGpu") or "").casefold() == "disable"
    checks["clipboard_disabled"] = (root.findtext("ClipboardRedirection") or "").casefold() == "disable"
    folders = root.findall("./MappedFolders/MappedFolder")
    checks["three_mapped_folders"] = len(folders) == 3
    permissions = [(folder.findtext("SandboxFolder"), (folder.findtext("ReadOnly") or "").casefold()) for folder in folders]
    checks["bootstrap_read_only"] = (r"C:\GHC\Bootstrap", "true") in permissions
    checks["input_read_only"] = (r"C:\GHC\Input", "true") in permissions
    checks["output_only_writable"] = permissions.count((r"C:\GHC\Output", "false")) == 1 and sum(value == "false" for _, value in permissions) == 1
    command = root.findtext("./LogonCommand/Command") or ""
    checks["bounded_bootstrap_command"] = "ghc_family_sandbox_bootstrap.ps1" in command and "-NoProfile" in command
    checks["no_inline_network_installer"] = all(term not in command.casefold() for term in ("invoke-webrequest", "curl ", "wget ", "winget ", "choco "))
    return {"template": path.name, "valid": all(checks.values()), "checks": checks, "owner_label": path.stem.split(".")[0]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--templates", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    results = [lint(path) for path in sorted(args.templates.glob("*.wsb.in"))]
    receipt = {
        "schema": "ghc.family.windows-sandbox-blueprint-validation.v1", "template_count": len(results),
        "valid_count": sum(item["valid"] for item in results), "valid": len(results) == 6 and all(item["valid"] for item in results),
        "results": results,
        "boundary": "Template linting does not prove feature availability, sandbox launch, administrative context, package installation, host security, or independent review.",
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"templates": len(results), "valid": receipt["valid"]}, indent=2))
    if not receipt["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
