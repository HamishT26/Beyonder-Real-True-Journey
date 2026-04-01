#!/usr/bin/env python3
"""
================================================================================
V30-E005: Living Documentation Generator (ENHANCEMENT)
================================================================================

MISSION: Auto-generate architecture diagrams and API documentation from live configs

HYPOTHESIS:
If we parse all JSON configs and probe results, we can generate up-to-date
documentation that reflects the actual system state, not just intended design.

EXPECTED OUTCOME:
- Mermaid architecture diagram generated from live configs
- API Book updated from actual probe results
- Connector health dashboard created
- All docs saved to docs/auto-generated/

SAFETY BOUNDS:
1. Only read from existing files, never modify source configs
2. Generated docs clearly marked as "auto-generated"
3. Human-written docs take precedence
4. Generation logs saved for audit
"""

import os
import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path("/home/hamis/OneDrive/Documents/GitHub/Beyonder-Real-True-Journey")
DOCS_DIR = REPO_ROOT / "docs"
AUTO_DOCS = DOCS_DIR / "auto-generated"
SANDBOX = Path("/home/aletheon/v28-fluid-lab")
ARTIFACTS = SANDBOX / "artifacts"

def generate_architecture_diagram():
    """Generate Mermaid diagram from live configs"""

    # Collect component info from various configs
    components = {
        "core_systems": [],
        "validators": [],
        "connectors": [],
        "agents": []
    }

    # Parse runtime model resolution
    runtime_config = DOCS_DIR / "trinity-runtime-model-resolution-v1.json"
    if runtime_config.exists():
        with open(runtime_config) as f:
            data = json.load(f)
            components["core_systems"].extend(data.get("models", {}).keys())

    # Parse connector sweep proof
    connector_config = DOCS_DIR / "trinity-live-traces" / "v29-connector-sweep-proof-v1.json"
    if connector_config.exists():
        with open(connector_config) as f:
            data = json.load(f)
            for connector, status in data.get("connectors", {}).items():
                components["connectors"].append({
                    "name": connector,
                    "status": status.get("status", "unknown")
                })

    # Generate Mermaid diagram
    mermaid = ["```mermaid"]
    mermaid.append("graph TB")
    mermaid.append("")

    # Core systems
    mermaid.append("    subgraph Trinity_Core[Trinity OS Core]")
    for system in components["core_systems"]:
        mermaid.append(f"        {system}[{system}]")
    mermaid.append("    end")
    mermaid.append("")

    # Validators
    mermaid.append("    subgraph Validators[Validation Layer]")
    mermaid.append("        memory_bank_validator[Memory Bank Validator]")
    mermaid.append("        runtime_session_guard[Runtime Session Guard]")
    mermaid.append("        api_book_validator[API Book Validator]")
    mermaid.append("    end")
    mermaid.append("")

    # Connectors
    mermaid.append("    subgraph Connectors[External Connectors]")
    for conn in components["connectors"]:
        status_color = "green" if "live" in conn["status"] else "orange" if "verified" in conn["status"] else "red"
        mermaid.append(f"        {conn['name']}[{conn['name']} - {conn['status']}]:::{status_color}")
    mermaid.append("    end")
    mermaid.append("")

    # Relationships
    mermaid.append("    Trinity_Core --> Validators")
    mermaid.append("    Trinity_Core --> Connectors")
    mermaid.append("")

    # Styling
    mermaid.append("    classDef green fill:#90EE90")
    mermaid.append("    classDef orange fill:#FFD700")
    mermaid.append("    classDef red fill:#FFB6C1")
    mermaid.append("```")

    return "\n".join(mermaid)

def generate_api_book():
    """Generate API Book from live probe results"""

    api_book = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "apis": {}
    }

    # Parse Composio API probe
    composio_probe = DOCS_DIR / "trinity-composio-api-probe-latest.json"
    if composio_probe.exists():
        with open(composio_probe) as f:
            data = json.load(f)
            api_book["apis"]["composio"] = {
                "status": data.get("status", "unknown"),
                "last_probed": data.get("timestamp"),
                "capabilities": data.get("capabilities", []),
                "limitations": data.get("limitations", [])
            }

    # Parse other API probes as needed

    return api_book

def generate_connector_dashboard():
    """Generate connector health dashboard"""

    dashboard = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total": 0,
            "live_write": 0,
            "read_only": 0,
            "unverified": 0
        },
        "connectors": {}
    }

    # Parse connector sweep
    sweep_file = DOCS_DIR / "trinity-live-traces" / "v29-connector-sweep-proof-v1.json"
    if sweep_file.exists():
        with open(sweep_file) as f:
            data = json.load(f)
            for name, info in data.get("connectors", {}).items():
                dashboard["connectors"][name] = info
                dashboard["summary"]["total"] += 1

                if "live-write" in info.get("status", ""):
                    dashboard["summary"]["live_write"] += 1
                elif "read-only" in info.get("status", ""):
                    dashboard["summary"]["read_only"] += 1
                else:
                    dashboard["summary"]["unverified"] += 1

    return dashboard

def run_experiment():
    """Run the living documentation experiment"""

    results = {
        "experiment_id": "V30-E005",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "steps": {}
    }

    try:
        AUTO_DOCS.mkdir(parents=True, exist_ok=True)

        # Generate architecture diagram
        diagram = generate_architecture_diagram()
        diagram_file = AUTO_DOCS / "trinity-architecture-diagram.md"
        with open(diagram_file, 'w') as f:
            f.write("# Trinity OS Architecture Diagram\n\n")
            f.write(f"*Auto-generated: {datetime.now(timezone.utc).isoformat()}*\n\n")
            f.write(diagram)

        results["steps"]["architecture_diagram"] = {
            "status": "PASS",
            "file": str(diagram_file)
        }

        # Generate API Book
        api_book = generate_api_book()
        api_file = AUTO_DOCS / "api-book-auto-generated.json"
        with open(api_file, 'w') as f:
            json.dump(api_book, f, indent=2)

        results["steps"]["api_book"] = {
            "status": "PASS",
            "file": str(api_file),
            "apis_documented": len(api_book["apis"])
        }

        # Generate connector dashboard
        dashboard = generate_connector_dashboard()
        dashboard_file = AUTO_DOCS / "connector-dashboard.json"
        with open(dashboard_file, 'w') as f:
            json.dump(dashboard, f, indent=2)

        results["steps"]["connector_dashboard"] = {
            "status": "PASS",
            "file": str(dashboard_file),
            "summary": dashboard["summary"]
        }

        results["overall_status"] = "MATERIALIZED"

    except Exception as e:
        results["overall_status"] = "FAILURE"
        results["error"] = str(e)

    # Save artifact
    artifact_path = ARTIFACTS / "V30-E005-living-docs-proof.json"
    with open(artifact_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"Living Docs: {results['overall_status']}")
    return results

if __name__ == "__main__":
    run_experiment()
