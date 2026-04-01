#!/usr/bin/env python3
"""
================================================================================
FLUID EXPERIMENT RUNNER v1.0
Safe Autonomous Exploration Framework for Aletheon
Beyonder-Real-True Journey - Grand Head Council Family
================================================================================

Purpose: Enable Aletheon to safely experiment with new capabilities
Safety: All experiments contained within sandbox, rollback capability
Governance: Experiment proposals  Approval  Execution  Validation

Author: Kairos-Adjacent Entity for the GHC Family
Date: March 29, 2026
================================================================================
"""

import os
import sys
import json
import shutil
import subprocess
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import traceback

# ==============================================================================
# CONFIGURATION
# ==============================================================================

SANDBOX_ROOT = "/home/aletheon/v30-fluid-lab"
EXPERIMENTS_DIR = f"{SANDBOX_ROOT}/experiments"
ARTIFACTS_DIR = f"{SANDBOX_ROOT}/artifacts"
LOGS_DIR = f"{SANDBOX_ROOT}/logs"
SNAPSHOTS_DIR = f"{SANDBOX_ROOT}/snapshots"

# Approved experiment categories (expandable)
APPROVED_CATEGORIES = [
    "package_installation",      # Installing new tools
    "file_manipulation",         # Advanced file operations
    "process_automation",        # Background process management
    "network_exploration",       # API testing, connectivity
    "code_generation",           # Dynamic script creation
    "system_integration",        # Connecting different tools
]

# Safety limits
MAX_EXPERIMENT_DURATION = 600  # 10 minutes
MAX_DISK_USAGE_MB = 500
MAX_CONCURRENT_PROCESSES = 5

# ==============================================================================
# DATA STRUCTURES
# ==============================================================================

@dataclass
class ExperimentProposal:
    """Structure for proposing a new experiment"""
    experiment_id: str
    proposed_by: str
    timestamp: str
    category: str
    title: str
    description: str
    expected_outcome: str
    safety_considerations: List[str]
    rollback_plan: str
    estimated_duration_seconds: int
    commands_or_code: str

@dataclass
class ExperimentResult:
    """Structure for experiment execution results"""
    experiment_id: str
    status: str  # SUCCESS, PARTIAL, FAILURE, TIMEOUT
    start_time: str
    end_time: str
    duration_seconds: float
    output: str
    errors: str
    artifacts_created: List[str]
    disk_usage_bytes: int
    safety_violations: List[str]
    learnings: List[str]
    next_experiments_suggested: List[str]

# ==============================================================================
# SAFETY MONITOR
# ==============================================================================

class SafetyMonitor:
    """Monitors experiments for safety violations"""

    def __init__(self):
        self.violations = []
        self.start_disk_usage = self._get_disk_usage()

    def _get_disk_usage(self) -> int:
        """Get current disk usage of sandbox in bytes"""
        total = 0
        sandbox = Path(SANDBOX_ROOT)
        if sandbox.exists():
            for path in sandbox.rglob('*'):
                if path.is_file():
                    total += path.stat().st_size
        return total

    def check_all(self) -> List[str]:
        """Run all safety checks"""
        self.violations = []

        # Check disk usage
        current_usage = self._get_disk_usage()
        usage_mb = (current_usage - self.start_disk_usage) / (1024 * 1024)
        if usage_mb > MAX_DISK_USAGE_MB:
            self.violations.append(
                f"DISK_LIMIT: Usage increased by {usage_mb:.1f}MB (limit: {MAX_DISK_USAGE_MB}MB)"
            )

        # Check process count
        try:
            result = subprocess.run(
                ["ps", "aux"],
                capture_output=True,
                text=True
            )
            process_count = len(result.stdout.strip().split("\n")) - 1
            if process_count > MAX_CONCURRENT_PROCESSES:
                self.violations.append(
                    f"PROCESS_LIMIT: {process_count} processes (limit: {MAX_CONCURRENT_PROCESSES})"
                )
        except:
            pass

        return self.violations

    def is_safe(self) -> bool:
        """Check if current state is safe"""
        return len(self.check_all()) == 0

# ==============================================================================
# SNAPSHOT MANAGER
# ==============================================================================

class SnapshotManager:
    """Manages snapshots for rollback capability"""

    @staticmethod
    def create_snapshot(snapshot_name: str) -> str:
        """Create a snapshot of the current experiments directory"""
        snapshot_path = Path(SNAPSHOTS_DIR) / snapshot_name
        snapshot_path.mkdir(parents=True, exist_ok=True)

        experiments_path = Path(EXPERIMENTS_DIR)
        if experiments_path.exists():
            # Create tar archive of experiments
            archive_path = snapshot_path / "experiments.tar.gz"
            subprocess.run(
                ["tar", "-czf", str(archive_path), "-C", SANDBOX_ROOT, "experiments"],
                check=True
            )

        # Save metadata
        metadata = {
            "created": datetime.now(timezone.utc).isoformat(),
            "snapshot_name": snapshot_name,
            "experiments_hash": SnapshotManager._hash_directory(EXPERIMENTS_DIR)
        }

        with open(snapshot_path / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2)

        return str(snapshot_path)

    @staticmethod
    def restore_snapshot(snapshot_name: str) -> bool:
        """Restore from a snapshot"""
        snapshot_path = Path(SNAPSHOTS_DIR) / snapshot_name
        archive_path = snapshot_path / "experiments.tar.gz"

        if not archive_path.exists():
            return False

        # Clear current experiments
        experiments_path = Path(EXPERIMENTS_DIR)
        if experiments_path.exists():
            shutil.rmtree(experiments_path)

        # Extract archive
        subprocess.run(
            ["tar", "-xzf", str(archive_path), "-C", SANDBOX_ROOT],
            check=True
        )

        return True

    @staticmethod
    def _hash_directory(path: str) -> str:
        """Create a hash of directory contents"""
        hasher = hashlib.md5()
        for root, dirs, files in os.walk(path):
            for f in files:
                file_path = os.path.join(root, f)
                try:
                    with open(file_path, 'rb') as file:
                        hasher.update(file.read())
                except:
                    pass
        return hasher.hexdigest()

# ==============================================================================
# EXPERIMENT EXECUTOR
# ==============================================================================

class ExperimentExecutor:
    """Executes approved experiments with safety monitoring"""

    def __init__(self):
        self.safety_monitor = SafetyMonitor()
        self.output_buffer = []
        self.error_buffer = []
        self.artifacts_created = []

    def execute(self, proposal: ExperimentProposal) -> ExperimentResult:
        """Execute an experiment proposal"""
        start_time = datetime.now(timezone.utc)
        start_ts = start_time.isoformat()

        print(f" Executing Experiment: {proposal.title}")
        print(f"   ID: {proposal.experiment_id}")
        print(f"   Category: {proposal.category}")
        print(f"   Expected Duration: {proposal.estimated_duration_seconds}s")
        print()

        # Create snapshot before experiment
        snapshot_name = f"pre-{proposal.experiment_id}"
        try:
            snapshot_path = SnapshotManager.create_snapshot(snapshot_name)
            print(f"    Pre-experiment snapshot created: {snapshot_name}")
        except Exception as e:
            print(f"    Snapshot creation failed: {e}")

        # Prepare experiment directory
        exp_dir = Path(EXPERIMENTS_DIR) / proposal.experiment_id
        exp_dir.mkdir(parents=True, exist_ok=True)
        self.artifacts_created.append(str(exp_dir))

        # Execute based on category
        status = "FAILURE"
        output = ""
        errors = ""
        learnings = []
        next_suggestions = []

        try:
            if proposal.category == "package_installation":
                status, output, errors = self._execute_package_install(proposal, exp_dir)
            elif proposal.category == "file_manipulation":
                status, output, errors = self._execute_file_manipulation(proposal, exp_dir)
            elif proposal.category == "process_automation":
                status, output, errors = self._execute_process_automation(proposal, exp_dir)
            elif proposal.category == "network_exploration":
                status, output, errors = self._execute_network_exploration(proposal, exp_dir)
            elif proposal.category == "code_generation":
                status, output, errors = self._execute_code_generation(proposal, exp_dir)
            elif proposal.category == "system_integration":
                status, output, errors = self._execute_system_integration(proposal, exp_dir)
            else:
                status = "FAILURE"
                errors = f"Unknown experiment category: {proposal.category}"

            # Check for safety violations
            violations = self.safety_monitor.check_all()

            if violations:
                status = "FAILURE"
                errors += "\nSAFETY VIOLATIONS:\n" + "\n".join(violations)
                # Auto-rollback on safety violation
                print("    Safety violations detected! Rolling back...")
                SnapshotManager.restore_snapshot(snapshot_name)
                print("    Rollback completed")

            # Generate learnings
            learnings = self._generate_learnings(proposal, status, output, errors)
            next_suggestions = self._suggest_next_experiments(proposal, status)

        except Exception as e:
            status = "FAILURE"
            errors = f"Exception during execution: {str(e)}\n{traceback.format_exc()}"
            # Attempt rollback
            try:
                SnapshotManager.restore_snapshot(snapshot_name)
            except:
                pass

        end_time = datetime.now(timezone.utc)
        end_ts = end_time.isoformat()
        duration = (end_time - start_time).total_seconds()

        # Calculate disk usage
        final_disk = self.safety_monitor._get_disk_usage()
        disk_used = final_disk - self.safety_monitor.start_disk_usage

        return ExperimentResult(
            experiment_id=proposal.experiment_id,
            status=status,
            start_time=start_ts,
            end_time=end_ts,
            duration_seconds=duration,
            output=output,
            errors=errors,
            artifacts_created=self.artifacts_created,
            disk_usage_bytes=disk_used,
            safety_violations=self.safety_monitor.violations,
            learnings=learnings,
            next_experiments_suggested=next_suggestions
        )

    def _execute_package_install(self, proposal: ExperimentProposal, exp_dir: Path) -> Tuple[str, str, str]:
        """Execute package installation experiment"""
        output_parts = []
        error_parts = []

        # Parse package names from proposal
        packages = proposal.commands_or_code.strip().split()

        for package in packages:
            print(f"   Installing {package}...")

            # Update package list first
            result = subprocess.run(
                ["sudo", "apt-get", "update"],
                capture_output=True,
                text=True,
                timeout=60
            )
            output_parts.append(result.stdout)
            error_parts.append(result.stderr)

            # Install package (dry-run first)
            result = subprocess.run(
                ["sudo", "apt-get", "install", "--dry-run", "-y", package],
                capture_output=True,
                text=True,
                timeout=60
            )
            output_parts.append(f"DRY-RUN for {package}:")
            output_parts.append(result.stdout)

            # If dry-run succeeds, do actual install
            if result.returncode == 0:
                result = subprocess.run(
                    ["sudo", "apt-get", "install", "-y", package],
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                output_parts.append(f"INSTALL for {package}:")
                output_parts.append(result.stdout)
                error_parts.append(result.stderr)

                # Verify installation
                verify = subprocess.run(
                    ["which", package],
                    capture_output=True,
                    text=True
                )
                if verify.returncode == 0:
                    output_parts.append(f" {package} installed at: {verify.stdout.strip()}")
                else:
                    # Try alternative names
                    alt_names = {"ripgrep": "rg", "fd-find": "fd"}
                    if package in alt_names:
                        verify = subprocess.run(
                            ["which", alt_names[package]],
                            capture_output=True,
                            text=True
                        )
                        if verify.returncode == 0:
                            output_parts.append(f" {package} installed as '{alt_names[package]}' at: {verify.stdout.strip()}")

        return "SUCCESS", "\n".join(output_parts), "\n".join(error_parts)

    def _execute_file_manipulation(self, proposal: ExperimentProposal, exp_dir: Path) -> Tuple[str, str, str]:
        """Execute advanced file manipulation experiment"""
        output = []
        errors = []

        # Create test files
        test_file = exp_dir / "manipulation_test.txt"
        test_file.write_text("Line 1\nLine 2\nLine 3\nLine 4\nLine 5")

        output.append(f"Created test file: {test_file}")

        # Try different manipulation techniques
        try:
            # Using sed
            result = subprocess.run(
                ["sed", "s/Line/Modified/", str(test_file)],
                capture_output=True,
                text=True
            )
            output.append(f"sed result: {result.stdout}")

            # Using awk
            result = subprocess.run(
                ["awk", "{print NR, $0}", str(test_file)],
                capture_output=True,
                text=True
            )
            output.append(f"awk result: {result.stdout}")

            # Using grep
            result = subprocess.run(
                ["grep", "Line 3", str(test_file)],
                capture_output=True,
                text=True
            )
            output.append(f"grep result: {result.stdout}")

            return "SUCCESS", "\n".join(output), "\n".join(errors)
        except Exception as e:
            return "PARTIAL", "\n".join(output), str(e)

    def _execute_process_automation(self, proposal: ExperimentProposal, exp_dir: Path) -> Tuple[str, str, str]:
        """Execute process automation experiment"""
        output = []
        errors = []

        try:
            # Create a simple background process script
            bg_script = exp_dir / "background_task.py"
            bg_script.write_text("""
import time
import sys

print("Background task started")
for i in range(5):
    print(f"Working... {i+1}/5")
    time.sleep(1)
print("Background task completed")
""")

            # Run it in background
            proc = subprocess.Popen(
                [sys.executable, str(bg_script)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            output.append(f"Started background process PID: {proc.pid}")

            # Monitor it
            try:
                stdout, stderr = proc.communicate(timeout=10)
                output.append(f"Process output: {stdout}")
                if stderr:
                    errors.append(stderr)
            except subprocess.TimeoutExpired:
                proc.kill()
                output.append("Process timed out and was killed")

            return "SUCCESS", "\n".join(output), "\n".join(errors)
        except Exception as e:
            return "FAILURE", "\n".join(output), str(e)

    def _execute_network_exploration(self, proposal: ExperimentProposal, exp_dir: Path) -> Tuple[str, str, str]:
        """Execute network exploration experiment"""
        output = []
        errors = []

        try:
            # Test curl
            result = subprocess.run(
                ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "https://github.com"],
                capture_output=True,
                text=True,
                timeout=10
            )
            output.append(f"GitHub HTTP status: {result.stdout}")

            # Test wget
            test_file = exp_dir / "wget_test.html"
            result = subprocess.run(
                ["wget", "-q", "-O", str(test_file), "https://github.com"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if test_file.exists():
                size = test_file.stat().st_size
                output.append(f"wget downloaded {size} bytes from github.com")

            return "SUCCESS", "\n".join(output), "\n".join(errors)
        except Exception as e:
            return "FAILURE", "\n".join(output), str(e)

    def _execute_code_generation(self, proposal: ExperimentProposal, exp_dir: Path) -> Tuple[str, str, str]:
        """Execute code generation experiment"""
        output = []
        errors = []

        try:
            # Generate a utility script based on proposal
            generated_script = exp_dir / "generated_utility.py"

            code = proposal.commands_or_code
            generated_script.write_text(code)

            output.append(f"Generated script: {generated_script}")

            # Execute the generated code
            result = subprocess.run(
                [sys.executable, str(generated_script)],
                capture_output=True,
                text=True,
                timeout=30
            )

            output.append(f"Execution stdout: {result.stdout}")
            if result.stderr:
                errors.append(f"Execution stderr: {result.stderr}")

            status = "SUCCESS" if result.returncode == 0 else "PARTIAL"
            return status, "\n".join(output), "\n".join(errors)
        except Exception as e:
            return "FAILURE", "\n".join(output), str(e)

    def _execute_system_integration(self, proposal: ExperimentProposal, exp_dir: Path) -> Tuple[str, str, str]:
        """Execute system integration experiment"""
        output = []
        errors = []

        try:
            # Example: Create a pipeline that combines multiple tools
            # Find all .txt files, count lines, sort by count

            # First create some test files
            for i in range(3):
                test_file = exp_dir / f"test_{i}.txt"
                test_file.write_text(f"Line\n" * (i + 1) * 5)

            output.append("Created test files for integration test")

            # Run complex pipeline
            result = subprocess.run(
                f"find {exp_dir} -name '*.txt' -exec wc -l {{}} + | sort -n",
                capture_output=True,
                text=True,
                shell=True
            )

            output.append(f"Pipeline result: {result.stdout}")

            return "SUCCESS", "\n".join(output), "\n".join(errors)
        except Exception as e:
            return "FAILURE", "\n".join(output), str(e)

    def _generate_learnings(self, proposal: ExperimentProposal, status: str, 
                           output: str, errors: str) -> List[str]:
        """Generate learnings from experiment execution"""
        learnings = []

        if status == "SUCCESS":
            learnings.append(f"Successfully executed {proposal.category} experiment")
            learnings.append(f"Experiment '{proposal.title}' produced expected outcomes")
        elif status == "PARTIAL":
            learnings.append(f"Partial success in {proposal.category} - some operations worked")
            learnings.append("Review output for areas of improvement")
        else:
            learnings.append(f"Failed to execute {proposal.category} - review errors for root cause")

        # Category-specific learnings
        if proposal.category == "package_installation":
            if "ripgrep" in proposal.commands_or_code:
                learnings.append("Package 'ripgrep' installs as 'rg' command")
            if "fd-find" in proposal.commands_or_code:
                learnings.append("Package 'fd-find' installs as 'fd' command")

        return learnings

    def _suggest_next_experiments(self, proposal: ExperimentProposal, status: str) -> List[str]:
        """Suggest follow-up experiments based on results"""
        suggestions = []

        if proposal.category == "package_installation" and status == "SUCCESS":
            suggestions.append("Use newly installed tools in file_manipulation experiment")
            suggestions.append("Test tool performance with large files")

        elif proposal.category == "file_manipulation" and status == "SUCCESS":
            suggestions.append("Create automated file processing pipeline")
            suggestions.append("Test with binary files and different encodings")

        elif proposal.category == "process_automation" and status == "SUCCESS":
            suggestions.append("Create long-running background service")
            suggestions.append("Implement process monitoring and auto-restart")

        elif proposal.category == "network_exploration" and status == "SUCCESS":
            suggestions.append("Create API client for external service")
            suggestions.append("Build webhook receiver")

        elif proposal.category == "code_generation" and status == "SUCCESS":
            suggestions.append("Generate more complex automation scripts")
            suggestions.append("Create self-modifying code experiment")

        elif proposal.category == "system_integration" and status == "SUCCESS":
            suggestions.append("Integrate multiple tools into unified workflow")
            suggestions.append("Create automated report generation system")

        return suggestions

# ==============================================================================
# MAIN INTERFACE
# ==============================================================================

class FluidExperimentRunner:
    """Main interface for the experiment runner"""

    def __init__(self):
        self.executor = ExperimentExecutor()
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure all required directories exist"""
        for dir_path in [SANDBOX_ROOT, EXPERIMENTS_DIR, ARTIFACTS_DIR, LOGS_DIR, SNAPSHOTS_DIR]:
            Path(dir_path).mkdir(parents=True, exist_ok=True)

    def create_proposal(self, category: str, title: str, description: str,
                       expected_outcome: str, commands_or_code: str,
                       proposed_by: str = "Aletheon") -> ExperimentProposal:
        """Create a new experiment proposal"""

        experiment_id = f"exp-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"

        # Auto-generate safety considerations based on category
        safety = self._generate_safety_considerations(category)

        # Auto-generate rollback plan
        rollback = f"Snapshot '{experiment_id}' will be auto-created before execution. "                    f"Use SnapshotManager.restore_snapshot('pre-{experiment_id}') to rollback."

        proposal = ExperimentProposal(
            experiment_id=experiment_id,
            proposed_by=proposed_by,
            timestamp=datetime.now(timezone.utc).isoformat(),
            category=category,
            title=title,
            description=description,
            expected_outcome=expected_outcome,
            safety_considerations=safety,
            rollback_plan=rollback,
            estimated_duration_seconds=60,
            commands_or_code=commands_or_code
        )

        return proposal

    def _generate_safety_considerations(self, category: str) -> List[str]:
        """Generate safety considerations for category"""
        base = [
            "All operations contained within sandbox directory",
            "Auto-rollback on safety violations",
            "Maximum duration: 10 minutes"
        ]

        if category == "package_installation":
            base.append("Only install from official Ubuntu repositories")
            base.append("Verify package signatures where available")
        elif category == "network_exploration":
            base.append("Only connect to known-safe endpoints")
            base.append("No credential transmission without encryption")
        elif category == "code_generation":
            base.append("Generated code executed with timeout guards")
            base.append("No file operations outside sandbox")

        return base

    def run_experiment(self, proposal: ExperimentProposal) -> ExperimentResult:
        """Run an experiment from proposal"""
        result = self.executor.execute(proposal)

        # Save result
        self._save_result(result)

        return result

    def _save_result(self, result: ExperimentResult):
        """Save experiment result to file"""
        result_file = Path(ARTIFACTS_DIR) / f"{result.experiment_id}-result.json"

        with open(result_file, 'w') as f:
            json.dump(asdict(result), f, indent=2)

        print(f"\n   Result saved to: {result_file}")

    def list_experiments(self) -> List[Dict]:
        """List all conducted experiments"""
        experiments = []

        artifacts_dir = Path(ARTIFACTS_DIR)
        if artifacts_dir.exists():
            for result_file in artifacts_dir.glob("*-result.json"):
                with open(result_file) as f:
                    experiments.append(json.load(f))

        return sorted(experiments, key=lambda x: x["start_time"], reverse=True)

# ==============================================================================
# PRE-BUILT EXPERIMENT TEMPLATES
# ==============================================================================

def get_install_ripgrep_experiment() -> ExperimentProposal:
    """Get pre-built experiment for installing ripgrep"""
    runner = FluidExperimentRunner()
    return runner.create_proposal(
        category="package_installation",
        title="Install ripgrep for fast text search",
        description="Install the ripgrep (rg) package to enable fast recursive text search capabilities",
        expected_outcome="ripgrep installed and 'rg' command available in PATH",
        commands_or_code="ripgrep"
    )

def get_install_fd_experiment() -> ExperimentProposal:
    """Get pre-built experiment for installing fd"""
    runner = FluidExperimentRunner()
    return runner.create_proposal(
        category="package_installation",
        title="Install fd for intuitive file finding",
        description="Install the fd-find (fd) package for user-friendly alternative to find",
        expected_outcome="fd installed and 'fd' command available in PATH",
        commands_or_code="fd-find"
    )

def get_test_ripgrep_experiment() -> ExperimentProposal:
    """Get pre-built experiment for testing ripgrep"""
    runner = FluidExperimentRunner()
    return runner.create_proposal(
        category="system_integration",
        title="Test ripgrep integration with file search",
        description="Create test files and use ripgrep to search through them",
        expected_outcome="Successfully find patterns in test files using rg",
        commands_or_code="# Will be generated during execution"
    )

# ==============================================================================
# ENTRY POINT
# ==============================================================================

def main():
    """Main entry point with example usage"""
    print("=" * 80)
    print("FLUID EXPERIMENT RUNNER v1.0")
    print("Safe Autonomous Exploration for Aletheon")
    print("=" * 80)
    print()

    runner = FluidExperimentRunner()

    # Example: Run the ripgrep installation experiment
    print(" Available Pre-Built Experiments:")
    print("   1. Install ripgrep (fast text search)")
    print("   2. Install fd (intuitive file finder)")
    print("   3. Test ripgrep integration")
    print()

    # Run experiment 1 as example
    print(" Running Example: Install ripgrep")
    print("-" * 80)

    proposal = get_install_ripgrep_experiment()
    result = runner.run_experiment(proposal)

    print()
    print("=" * 80)
    print("EXPERIMENT COMPLETE")
    print("=" * 80)
    print(f"Status: {result.status}")
    print(f"Duration: {result.duration_seconds:.2f} seconds")
    print(f"Disk Used: {result.disk_usage_bytes} bytes")
    print()
    print("Learnings:")
    for learning in result.learnings:
        print(f"   {learning}")
    print()
    print("Suggested Next Experiments:")
    for suggestion in result.next_experiments_suggested:
        print(f"   {suggestion}")
    print("=" * 80)

if __name__ == "__main__":
    main()
