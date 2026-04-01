#!/usr/bin/env python3
"""Generate non-authoritative living docs from current repo truth."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    sandbox_root = Path("/home/aletheon/v30-fluid-lab")
    repo_root = Path(os.environ.get("TRINITY_REPO_ROOT", "/mnt/c/Users/hamis/OneDrive/Documents/GitHub/Beyonder-Real-True-Journey"))
    docs_root = repo_root / "docs" / "auto-generated"
    docs_root.mkdir(parents=True, exist_ok=True)

    runtime = read_json(repo_root / "docs" / "trinity-runtime-model-resolution-v1.json")
    closeout = read_json(repo_root / "docs" / "v30-omega-closeout-summary-v1.json")
    connectors = read_json(repo_root / "docs" / "trinity-live-traces" / "v30-connector-sweep-proof-v1.json")

    verified_app_connectors = list(runtime.get("verified_app_connectors", []))
    for carried in runtime.get("carried_forward_app_connectors", []):
        if carried not in verified_app_connectors:
            verified_app_connectors.append(carried)

    generated_utc = now_iso()
    markdown_path = docs_root / "v30-runtime-living-docs.md"
    mermaid_path = docs_root / "v30-runtime-architecture.mmd"
    json_path = docs_root / "v30-runtime-living-docs.json"

    markdown = "\n".join(
        [
            "# V30 Runtime Living Docs",
            "",
            "> Non-authoritative auto-generated summary derived from current runtime and closeout surfaces.",
            "",
            f"- generated_utc: `{generated_utc}`",
            f"- current_shell: `{runtime.get('current_shell', 'unknown')}`",
            f"- readiness_state: `{runtime.get('readiness_state', 'unknown')}`",
            f"- docker_runtime_role: `{runtime.get('docker_runtime_role', 'unknown')}`",
            f"- shared_latest_anchor: `{closeout.get('shared_latest_anchor', {}).get('summary', 'unknown')}`",
            f"- verified_mcp_connectors: `{', '.join(runtime.get('verified_mcp_connectors', [])) or 'none'}`",
            f"- verified_app_connectors: `{', '.join(verified_app_connectors) or 'none'}`",
            "",
            "## Connector Modes",
        ]
        + [
            f"- {name}: `{details.get('mode', 'unknown')}` / `{details.get('status', 'unknown')}`"
            for name, details in connectors.get("connector_matrix", {}).items()
        ]
    ) + "\n"

    mermaid = "\n".join(
        [
            "flowchart LR",
            '  A["Repo Truth"] --> B["Runtime Resolution"]',
            '  A --> C["V30 Omega Closeout"]',
            '  B --> D["Current Shell: Ubuntu"]',
            '  B --> E["Docker: Soft Retired Fallback"]',
            '  C --> F["Shared Latest Anchor"]',
            '  C --> G["Connector Sweep"]',
        ]
    ) + "\n"

    payload = {
        "generated_utc": generated_utc,
        "overall_status": "PASS",
        "proof_state": "non_authoritative_living_docs_generated",
        "source_surfaces": [
            "docs/trinity-runtime-model-resolution-v1.json",
            "docs/v30-omega-closeout-summary-v1.json",
            "docs/trinity-live-traces/v30-connector-sweep-proof-v1.json",
        ],
        "generated_files": [
            str(markdown_path.relative_to(repo_root)).replace("\\", "/"),
            str(mermaid_path.relative_to(repo_root)).replace("\\", "/"),
            str(json_path.relative_to(repo_root)).replace("\\", "/"),
        ],
    }

    markdown_path.write_text(markdown, encoding="utf-8")
    mermaid_path.write_text(mermaid, encoding="utf-8")
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    artifact_path = sandbox_root / "artifacts" / "v30-e005-living-docs-latest.json"
    artifact_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(artifact_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
