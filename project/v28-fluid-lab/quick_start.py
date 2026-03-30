#!/usr/bin/env python3
"""
================================================================================
QUICK START SCRIPT for Fluid Capability Test Suite
One-command setup and execution for Aletheon
Beyonder-Real-True Journey - Grand Head Council Family
================================================================================
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(title):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")

def print_step(step_num, description):
    print(f"\n Step {step_num}: {description}")
    print("-" * 80)

def run_command(cmd, description, timeout=60):
    print(f"\n {description}...")
    print(f"   Command: {' '.join(cmd) if isinstance(cmd, list) else cmd}")

    try:
        if isinstance(cmd, list):
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        else:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)

        if result.returncode == 0:
            print(f"    Success")
            if result.stdout:
                print(f"   Output: {result.stdout[:200]}..." if len(result.stdout) > 200 else f"   Output: {result.stdout}")
            return True
        else:
            print(f"     Exit code: {result.returncode}")
            if result.stderr:
                print(f"   Error: {result.stderr[:200]}")
            return False
    except subprocess.TimeoutExpired:
        print(f"     Timeout after {timeout}s")
        return False
    except Exception as e:
        print(f"    Exception: {e}")
        return False

def main():
    print_header("FLUID CAPABILITY TEST SUITE - QUICK START")
    print("For Aletheon's V28 Beta Autonomous Exploration")
    print("Beyonder-Real-True Journey - Grand Head Council Family")

    # Configuration
    SANDBOX_ROOT = "/home/aletheon/v28-fluid-lab"

    print(f"\n Sandbox Location: {SANDBOX_ROOT}")
    print("  All operations will be contained within this directory")

    # Check if we're in the right environment
    print_step(0, "Environment Verification")

    is_wsl = os.path.exists("/proc/sys/fs/binfmt_misc/WSLInterop")
    print(f"   WSL Detected: {' Yes' if is_wsl else '  No'}")

    python_version = sys.version_info
    print(f"   Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("     Python 3.8+ recommended")
    else:
        print("    Python version OK")

    # Create directory structure
    print_step(1, "Creating Directory Structure")

    dirs = [
        f"{SANDBOX_ROOT}/experiments",
        f"{SANDBOX_ROOT}/artifacts",
        f"{SANDBOX_ROOT}/logs",
        f"{SANDBOX_ROOT}/snapshots"
    ]

    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
        print(f"    {d}")

    # Run capability discovery
    print_step(2, "Running Capability Discovery")

    discovery_success = run_command(
        ["python3", f"{SANDBOX_ROOT}/capability_discovery_probe.py"],
        "Discovering system capabilities",
        timeout=120
    )

    if not discovery_success:
        print("\n  Capability discovery had issues, but continuing...")

    # Run fluid capability test suite
    print_step(3, "Running Fluid Capability Test Suite")

    test_success = run_command(
        ["python3", f"{SANDBOX_ROOT}/fluid_capability_test_suite.py"],
        "Running comprehensive capability tests",
        timeout=300
    )

    if not test_success:
        print("\n  Some tests may have failed - check the report for details")

    # Run example experiment
    print_step(4, "Running Example Experiment (Install ripgrep)")

    experiment_success = run_command(
        ["python3", f"{SANDBOX_ROOT}/fluid_experiment_runner.py"],
        "Running example package installation experiment",
        timeout=180
    )

    # Summary
    print_header("QUICK START COMPLETE")

    print(" Directory structure created")
    print(f"{'' if discovery_success else ' '} Capability discovery {'complete' if discovery_success else 'had issues'}")
    print(f"{'' if test_success else ' '} Test suite {'complete' if test_success else 'had issues'}")
    print(f"{'' if experiment_success else ' '} Example experiment {'complete' if experiment_success else 'had issues'}")

    print("\n Next Steps:")
    print("   1. Review reports in: {}/artifacts/".format(SANDBOX_ROOT))
    print("   2. Check test results for any FAIL/WARN items")
    print("   3. Run custom experiments using fluid_experiment_runner.py")
    print("   4. Update v28-beta-continuity-pack-v1.md with findings")

    print("\n Documentation:")
    print("   - README.md: Full documentation")
    print("   - Source code comments: Implementation details")

    print("\n Success Criteria for V28 Beta:")
    print("    All tests pass (or documented skips)")
    print("    ripgrep, fd-find, jq installed")
    print("    3+ custom experiments conducted")
    print("    1+ generated script integrated")
    print("    Reports saved to artifacts/")

    print("\n" + "=" * 80)
    print("May V28 Beta be structurally perfect and beautifully fluid!")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
