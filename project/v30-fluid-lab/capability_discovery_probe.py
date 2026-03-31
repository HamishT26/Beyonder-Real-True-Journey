#!/usr/bin/env python3
"""
================================================================================
CAPABILITY DISCOVERY PROBE v1.0
System Capability Assessment for Aletheon's WSL Environment
Beyonder-Real-True Journey - Grand Head Council Family
================================================================================

Purpose: Discover and catalog all available capabilities in the WSL environment
Output: JSON report suitable for Trinity OS integration
Safety: Read-only operations, no modifications

Author: Kairos-Adjacent Entity for the GHC Family
Date: March 29, 2026
================================================================================
"""

import os
import sys
import json
import subprocess
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, asdict

# ==============================================================================
# CAPABILITY DISCOVERY CLASSES
# ==============================================================================

@dataclass
class CapabilityReport:
    """Complete capability discovery report"""
    timestamp: str
    environment: str
    capabilities: Dict[str, Any]
    tools_available: Dict[str, bool]
    languages_available: Dict[str, str]
    system_limits: Dict[str, Any]
    recommendations: List[str]

class CapabilityDiscoverer:
    """Discovers system capabilities through probing"""

    def __init__(self):
        self.capabilities = {}
        self.tools = {}
        self.languages = {}
        self.limits = {}

    def discover_all(self) -> CapabilityReport:
        """Run all discovery probes"""
        print(" Starting Capability Discovery...")
        print()

        self.capabilities["environment"] = self._discover_environment()
        self.capabilities["filesystem"] = self._discover_filesystem()
        self.capabilities["process"] = self._discover_process()
        self.capabilities["network"] = self._discover_network()
        self.capabilities["packages"] = self._discover_packages()

        self.tools = self._discover_tools()
        self.languages = self._discover_languages()
        self.limits = self._discover_limits()

        recommendations = self._generate_recommendations()

        return CapabilityReport(
            timestamp=datetime.now(timezone.utc).isoformat(),
            environment="WSL-Ubuntu",
            capabilities=self.capabilities,
            tools_available=self.tools,
            languages_available=self.languages,
            system_limits=self.limits,
            recommendations=recommendations
        )

    def _discover_environment(self) -> Dict[str, Any]:
        """Discover environment characteristics"""
        print("   Discovering environment...")

        env = {
            "os": {},
            "user": {},
            "wsl": {}
        }

        # OS info
        try:
            with open("/etc/os-release") as f:
                for line in f:
                    if "=" in line:
                        key, value = line.strip().split("=", 1)
                        env["os"][key] = value.strip('"')
        except:
            pass

        # Kernel info
        try:
            result = subprocess.run(["uname", "-r"], capture_output=True, text=True)
            env["os"]["kernel"] = result.stdout.strip()
        except:
            pass

        # User info
        env["user"]["username"] = os.environ.get("USER", "unknown")
        env["user"]["home"] = os.environ.get("HOME", "unknown")
        env["user"]["shell"] = os.environ.get("SHELL", "unknown")
        env["user"]["uid"] = os.getuid()
        env["user"]["gid"] = os.getgid()

        # WSL info
        env["wsl"]["is_wsl"] = os.path.exists("/proc/sys/fs/binfmt_misc/WSLInterop")
        env["wsl"]["interop_enabled"] = os.environ.get("WSL_INTEROP", "") != ""
        env["wsl"]["distro_name"] = os.environ.get("WSL_DISTRO_NAME", "unknown")

        return env

    def _discover_filesystem(self) -> Dict[str, Any]:
        """Discover filesystem capabilities"""
        print("   Discovering filesystem...")

        fs = {
            "writable_locations": [],
            "mount_points": [],
            "special_filesystems": []
        }

        # Check common writable locations
        test_locations = [
            "/tmp",
            "/var/tmp",
            os.environ.get("HOME", "/home"),
            "/mnt/c"  # Windows mount
        ]

        for loc in test_locations:
            if os.path.exists(loc):
                try:
                    test_file = Path(loc) / ".capability_test"
                    test_file.write_text("test")
                    test_file.unlink()
                    fs["writable_locations"].append(loc)
                except:
                    pass

        # Get mount points
        try:
            with open("/proc/mounts") as f:
                for line in f:
                    parts = line.split()
                    if len(parts) >= 2:
                        fs["mount_points"].append({
                            "device": parts[0],
                            "mount": parts[1],
                            "type": parts[2]
                        })
        except:
            pass

        return fs

    def _discover_process(self) -> Dict[str, Any]:
        """Discover process management capabilities"""
        print("    Discovering process capabilities...")

        proc = {
            "max_processes": None,
            "current_processes": None,
            "can_fork": False,
            "can_thread": False
        }

        # Check max processes
        try:
            with open("/proc/sys/kernel/pid_max") as f:
                proc["max_processes"] = int(f.read().strip())
        except:
            pass

        # Count current processes
        try:
            result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
            proc["current_processes"] = len(result.stdout.strip().split("\n")) - 1
        except:
            pass

        # Test fork capability
        try:
            pid = os.fork()
            if pid == 0:
                os._exit(0)
            else:
                os.waitpid(pid, 0)
                proc["can_fork"] = True
        except:
            pass

        # Test threading
        try:
            import threading
            def test_thread():
                pass
            t = threading.Thread(target=test_thread)
            t.start()
            t.join()
            proc["can_thread"] = True
        except:
            pass

        return proc

    def _discover_network(self) -> Dict[str, Any]:
        """Discover network capabilities"""
        print("   Discovering network...")

        net = {
            "interfaces": [],
            "can_resolve_dns": False,
            "can_connect_outbound": False,
            "can_bind_ports": False
        }

        # Get network interfaces
        try:
            result = subprocess.run(["ip", "addr"], capture_output=True, text=True)
            for line in result.stdout.split("\n"):
                if line.strip().startswith("inet "):
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        net["interfaces"].append(parts[1])
        except:
            pass

        # Test DNS resolution
        try:
            import socket
            socket.gethostbyname("github.com")
            net["can_resolve_dns"] = True
        except:
            pass

        # Test outbound connection
        try:
            import urllib.request
            req = urllib.request.Request("https://github.com", method="HEAD")
            req.add_header("User-Agent", "CapabilityDiscovery/1.0")
            with urllib.request.urlopen(req, timeout=5) as response:
                net["can_connect_outbound"] = True
        except:
            pass

        # Test port binding
        try:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("127.0.0.1", 0))  # Bind to any available port
            port = s.getsockname()[1]
            s.close()
            net["can_bind_ports"] = True
            net["sample_bound_port"] = port
        except:
            pass

        return net

    def _discover_packages(self) -> Dict[str, Any]:
        """Discover package management capabilities"""
        print("   Discovering package management...")

        pkg = {
            "package_managers": {},
            "installed_packages_count": 0,
            "can_install": False,
            "can_update": False
        }

        # Check apt
        apt_path = shutil.which("apt")
        if apt_path:
            pkg["package_managers"]["apt"] = apt_path

            # Check if we can update
            try:
                result = subprocess.run(
                    ["apt", "--dry-run", "update"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                pkg["can_update"] = result.returncode == 0
            except:
                pass

        # Check dpkg
        dpkg_path = shutil.which("dpkg")
        if dpkg_path:
            pkg["package_managers"]["dpkg"] = dpkg_path

            # Count installed packages
            try:
                result = subprocess.run(
                    ["dpkg", "-l"],
                    capture_output=True,
                    text=True
                )
                pkg["installed_packages_count"] = len(result.stdout.strip().split("\n")) - 5
            except:
                pass

        # Check pip
        pip_path = shutil.which("pip3") or shutil.which("pip")
        if pip_path:
            pkg["package_managers"]["pip"] = pip_path

        return pkg

    def _discover_tools(self) -> Dict[str, bool]:
        """Discover available command-line tools"""
        print("    Discovering tools...")

        tools_to_check = {
            # Core utilities
            "git": "Version control",
            "curl": "HTTP client",
            "wget": "File downloader",
            "ssh": "Secure shell",
            "tar": "Archive utility",
            "gzip": "Compression",
            "grep": "Text search",
            "sed": "Stream editor",
            "awk": "Text processing",
            "find": "File finder",
            "xargs": "Argument builder",

            # Advanced tools (may need installation)
            "rg": "ripgrep (fast search)",
            "fd": "fd (modern find)",
            "fzf": "Fuzzy finder",
            "jq": "JSON processor",
            "gh": "GitHub CLI",
            "htop": "Process viewer",
            "tree": "Directory tree",
            "nc": "Netcat (networking)",
            "tmux": "Terminal multiplexer",
            "docker": "Container runtime",
            "kubectl": "Kubernetes CLI",

            # Development tools
            "node": "Node.js",
            "npm": "Node package manager",
            "python3": "Python 3",
            "pip3": "Python package manager",
            "gcc": "C compiler",
            "make": "Build tool",
        }

        discovered = {}
        for tool, description in tools_to_check.items():
            discovered[tool] = shutil.which(tool) is not None

        return discovered

    def _discover_languages(self) -> Dict[str, str]:
        """Discover available programming languages"""
        print("   Discovering languages...")

        languages = {}

        # Python
        try:
            result = subprocess.run(
                [sys.executable, "--version"],
                capture_output=True,
                text=True
            )
            languages["python"] = result.stdout.strip() or result.stderr.strip()
        except:
            pass

        # Node.js
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                languages["nodejs"] = result.stdout.strip()
        except:
            pass

        # Bash
        try:
            result = subprocess.run(["bash", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                languages["bash"] = result.stdout.split("\n")[0]
        except:
            pass

        # Perl
        try:
            result = subprocess.run(["perl", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                for line in result.stdout.split("\n"):
                    if "v5." in line or "v6." in line:
                        languages["perl"] = line.strip()
                        break
        except:
            pass

        # Ruby
        try:
            result = subprocess.run(["ruby", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                languages["ruby"] = result.stdout.strip()
        except:
            pass

        return languages

    def _discover_limits(self) -> Dict[str, Any]:
        """Discover system limits"""
        print("   Discovering system limits...")

        limits = {
            "file_descriptors": None,
            "max_file_size": None,
            "stack_size": None,
            "cpu_time": None,
            "virtual_memory": None
        }

        # Get ulimit values
        try:
            result = subprocess.run(["ulimit", "-n"], capture_output=True, text=True, shell=True)
            limits["file_descriptors"] = result.stdout.strip()
        except:
            pass

        try:
            result = subprocess.run(["ulimit", "-f"], capture_output=True, text=True, shell=True)
            limits["max_file_size"] = result.stdout.strip()
        except:
            pass

        try:
            result = subprocess.run(["ulimit", "-s"], capture_output=True, text=True, shell=True)
            limits["stack_size"] = result.stdout.strip()
        except:
            pass

        try:
            result = subprocess.run(["ulimit", "-t"], capture_output=True, text=True, shell=True)
            limits["cpu_time"] = result.stdout.strip()
        except:
            pass

        try:
            result = subprocess.run(["ulimit", "-v"], capture_output=True, text=True, shell=True)
            limits["virtual_memory"] = result.stdout.strip()
        except:
            pass

        # Get RAM info
        try:
            with open("/proc/meminfo") as f:
                for line in f:
                    if line.startswith("MemTotal:"):
                        limits["total_ram"] = line.split()[1:3]
                        break
        except:
            pass

        # Get disk space
        try:
            result = subprocess.run(["df", "-h", "/"], capture_output=True, text=True)
            lines = result.stdout.strip().split("\n")
            if len(lines) >= 2:
                parts = lines[1].split()
                limits["disk_space_root"] = {
                    "size": parts[1],
                    "used": parts[2],
                    "available": parts[3]
                }
        except:
            pass

        return limits

    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on discovery"""
        recommendations = []

        # Check for missing tools
        if not self.tools.get("rg"):
            recommendations.append("Install ripgrep (rg) for fast text search: sudo apt-get install ripgrep")

        if not self.tools.get("fd"):
            recommendations.append("Install fd-find for intuitive file finding: sudo apt-get install fd-find")

        if not self.tools.get("jq"):
            recommendations.append("Install jq for JSON processing: sudo apt-get install jq")

        if not self.tools.get("gh"):
            recommendations.append("Install GitHub CLI for repo-native automation: sudo apt-get install gh")

        if not self.tools.get("fzf"):
            recommendations.append("Install fzf for fuzzy finding: sudo apt-get install fzf")

        # Check for development tools
        if not self.tools.get("docker"):
            recommendations.append("Consider installing Docker for containerization")

        # Network recommendations
        if not self.capabilities.get("network", {}).get("can_connect_outbound"):
            recommendations.append("Network connectivity limited - check WSL network configuration")

        # General recommendations
        recommendations.append("Run Fluid Capability Test Suite for comprehensive validation")
        recommendations.append("Use Fluid Experiment Runner for safe capability exploration")

        return recommendations

# ==============================================================================
# MAIN
# ==============================================================================

def main():
    """Main entry point"""
    print("=" * 80)
    print("CAPABILITY DISCOVERY PROBE v1.0")
    print("Discovering Aletheon's WSL Environment")
    print("=" * 80)
    print()

    discoverer = CapabilityDiscoverer()
    report = discoverer.discover_all()

    # Save report
    output_dir = Path("/home/aletheon/v30-fluid-lab/artifacts")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_file = output_dir / f"capability-discovery-{timestamp}.json"

    with open(output_file, 'w') as f:
        json.dump(asdict(report), f, indent=2)

    # Print summary
    print()
    print("=" * 80)
    print("DISCOVERY COMPLETE")
    print("=" * 80)

    # Environment summary
    env = report.capabilities["environment"]
    print(f"\nEnvironment: {env['os'].get('PRETTY_NAME', 'Unknown')}")
    print(f"Kernel: {env['os'].get('kernel', 'Unknown')}")
    print(f"User: {env['user']['username']} (UID: {env['user']['uid']})")
    print(f"WSL: {'Yes' if env['wsl']['is_wsl'] else 'No'}")

    # Tools summary
    available_tools = [k for k, v in report.tools_available.items() if v]
    missing_tools = [k for k, v in report.tools_available.items() if not v]

    print(f"\nTools Available: {len(available_tools)}")
    print(f"Tools Missing: {len(missing_tools)}")
    print(f"\nKey Tools: {', '.join(available_tools[:10])}")

    # Languages summary
    print(f"\nLanguages: {', '.join(report.languages_available.keys())}")

    # Recommendations
    print(f"\nRecommendations ({len(report.recommendations)}):")
    for rec in report.recommendations:
        print(f"   {rec}")

    print(f"\nFull report saved to: {output_file}")
    print("=" * 80)

if __name__ == "__main__":
    main()
