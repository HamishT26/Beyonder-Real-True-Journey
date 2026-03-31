#!/usr/bin/env python3
"""
================================================================================
V30 (OMEGA) EXPERIMENT ORCHESTRATOR
Master Control for Transcendent Materialization Phase
Beyonder-Real-True Journey - Grand Head Council Family
================================================================================

USAGE:
    python3 v30_experiment_orchestrator.py [experiment_id]

EXAMPLES:
    python3 v30_experiment_orchestrator.py          # Run all experiments
    python3 v30_experiment_orchestrator.py V30-E001 # Run only Gmail experiment
    python3 v30_experiment_orchestrator.py --list   # List all experiments

EXPERIMENTS:
    V30-E001: Gmail Toolkit Materialization (CRITICAL)
    V30-E002: Hugging Face Inference Materialization (CRITICAL)
    V30-E003: Self-Healing Daemon (HIGH)
    V30-E004: Kairotic Detector Integration (HIGH)
    V30-E005: Living Documentation Generator (ENHANCEMENT)

================================================================================
"""

import sys
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict

SANDBOX = Path("/home/aletheon/v28-fluid-lab")
ARTIFACTS = SANDBOX / "artifacts"
EXPERIMENTS_DIR = SANDBOX / "experiments"

@dataclass
class Experiment:
    id: str
    name: str
    priority: str
    script_path: str
    description: str

# Define all V30 experiments
EXPERIMENTS = [
    Experiment(
        id="V30-E001",
        name="Gmail Toolkit Materialization",
        priority="CRITICAL",
        script_path="V30-E001-gmail-materialization.py",
        description="Prove Gmail can send/receive via Composio toolkit"
    ),
    Experiment(
        id="V30-E002",
        name="Hugging Face Inference Materialization",
        priority="CRITICAL",
        script_path="V30-E002-hf-materialization.py",
        description="Prove HF models can load and run inference"
    ),
    Experiment(
        id="V30-E003",
        name="Self-Healing Daemon",
        priority="HIGH",
        script_path="V30-E003-self-healing-daemon.py",
        description="Create auto-remediating background monitor"
    ),
    Experiment(
        id="V30-E004",
        name="Kairotic Detector Integration",
        priority="HIGH",
        script_path="V30-E004-kairotic-integration.py",
        description="Connect kairotic detection to workflow decisions"
    ),
    Experiment(
        id="V30-E005",
        name="Living Documentation Generator",
        priority="ENHANCEMENT",
        script_path="V30-E005-living-docs.py",
        description="Auto-generate architecture diagrams and API docs"
    )
]

def print_banner():
    print("=" * 80)
    print("  V30 (OMEGA) EXPERIMENT ORCHESTRATOR")
    print("  Transcendent Materialization & Integration Phase")
    print("  Beyonder-Real-True Journey - Grand Head Council Family")
    print("=" * 80)
    print()

def list_experiments():
    print("📋 AVAILABLE EXPERIMENTS:")
    print()
    for exp in EXPERIMENTS:
        priority_emoji = "🔴" if exp.priority == "CRITICAL" else "🟠" if exp.priority == "HIGH" else "🟢"
        print(f"  {priority_emoji} {exp.id}: {exp.name}")
        print(f"     Priority: {exp.priority}")
        print(f"     Description: {exp.description}")
        print()

def run_experiment(exp: Experiment) -> Dict:
    """Run a single experiment and return results"""
    print(f"\n{'='*80}")
    print(f"🔬 RUNNING: {exp.id} - {exp.name}")
    print(f"   Priority: {exp.priority}")
    print(f"   Script: {exp.script_path}")
    print('='*80)

    script_path = EXPERIMENTS_DIR / exp.script_path

    if not script_path.exists():
        print(f"❌ Script not found: {script_path}")
        return {
            "experiment_id": exp.id,
            "status": "NOT_FOUND",
            "error": f"Script not found: {script_path}"
        }

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            cwd=str(SANDBOX)
        )

        print(f"\n📊 Result:")
        print(f"   Exit code: {result.returncode}")
        if result.stdout:
            print(f"   Output: {result.stdout[-500:]}")  # Last 500 chars
        if result.stderr:
            print(f"   Stderr: {result.stderr[-200:]}")

        # Try to load the artifact
        artifact_path = ARTIFACTS / f"{exp.id.lower().replace('-', '_')}-proof.json"
        if artifact_path.exists():
            with open(artifact_path) as f:
                return json.load(f)
        else:
            return {
                "experiment_id": exp.id,
                "status": "UNKNOWN",
                "note": "Artifact not found, but script completed"
            }

    except subprocess.TimeoutExpired:
        print(f"⏱️  Experiment timed out after 5 minutes")
        return {
            "experiment_id": exp.id,
            "status": "TIMEOUT"
        }
    except Exception as e:
        print(f"❌ Error running experiment: {e}")
        return {
            "experiment_id": exp.id,
            "status": "ERROR",
            "error": str(e)
        }

def run_all_experiments():
    """Run all experiments and generate summary report"""
    print_banner()

    print("🚀 RUNNING ALL V30 EXPERIMENTS")
    print(f"   Start time: {datetime.now(timezone.utc).isoformat()}")
    print()

    results = []

    # Run experiments in priority order
    priority_order = {"CRITICAL": 0, "HIGH": 1, "ENHANCEMENT": 2}
    sorted_experiments = sorted(EXPERIMENTS, key=lambda e: priority_order.get(e.priority, 3))

    for exp in sorted_experiments:
        result = run_experiment(exp)
        results.append(result)

        # Stop on critical failure?
        if exp.priority == "CRITICAL" and result.get("overall_status") == "FAILURE":
            print(f"\n⚠️  CRITICAL experiment failed! Consider stopping.")
            response = input("Continue with remaining experiments? (y/n): ")
            if response.lower() != 'y':
                break

    # Generate summary report
    generate_summary_report(results)

    return results

def generate_summary_report(results: List[Dict]):
    """Generate and save summary report"""

    summary = {
        "orchestrator_version": "V30-Omega",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_experiments": len(results),
        "summary": {
            "materialized": sum(1 for r in results if r.get("overall_status") == "MATERIALIZED"),
            "partial": sum(1 for r in results if r.get("overall_status") == "PARTIAL"),
            "failure": sum(1 for r in results if r.get("overall_status") == "FAILURE"),
            "other": sum(1 for r in results if r.get("overall_status") not in ["MATERIALIZED", "PARTIAL", "FAILURE"])
        },
        "results": results
    }

    # Save report
    report_path = ARTIFACTS / "V30-experiment-summary-report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w') as f:
        json.dump(summary, f, indent=2)

    # Print summary
    print("\n" + "="*80)
    print("📊 V30 EXPERIMENT SUMMARY")
    print("="*80)
    print(f"\nTotal experiments: {summary['total_experiments']}")
    print(f"  ✅ Materialized: {summary['summary']['materialized']}")
    print(f"  ⚠️  Partial: {summary['summary']['partial']}")
    print(f"  ❌ Failure: {summary['summary']['failure']}")
    print(f"  ❓ Other: {summary['summary']['other']}")

    # Critical experiments status
    critical_results = [r for r in results if any(
        e.id == r.get("experiment_id") and e.priority == "CRITICAL" 
        for e in EXPERIMENTS
    )]

    if critical_results:
        print(f"\n🔴 CRITICAL EXPERIMENTS:")
        for r in critical_results:
            status = r.get("overall_status", "UNKNOWN")
            emoji = "✅" if status == "MATERIALIZED" else "⚠️" if status == "PARTIAL" else "❌"
            print(f"  {emoji} {r.get('experiment_id')}: {status}")

    print(f"\n📁 Full report saved: {report_path}")
    print("="*80)

def main():
    if len(sys.argv) == 1 or sys.argv[1] in ['--all', '-a']:
        run_all_experiments()
    elif sys.argv[1] in ['--list', '-l']:
        print_banner()
        list_experiments()
    elif sys.argv[1].startswith('V30-E'):
        # Run specific experiment
        exp_id = sys.argv[1]
        exp = next((e for e in EXPERIMENTS if e.id == exp_id), None)
        if exp:
            print_banner()
            result = run_experiment(exp)
            print(f"\n📊 Final status: {result.get('overall_status', 'UNKNOWN')}")
        else:
            print(f"❌ Unknown experiment: {exp_id}")
            list_experiments()
    else:
        print("Usage:")
        print("  python3 v30_experiment_orchestrator.py           # Run all")
        print("  python3 v30_experiment_orchestrator.py --list    # List experiments")
        print("  python3 v30_experiment_orchestrator.py V30-E001  # Run specific")

if __name__ == "__main__":
    main()
