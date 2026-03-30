# Fluid Capability Test Suite v1.0

Bounded repo-tracked source bundle for Aletheon's V28 beta fluid-lab work.

Runtime sandbox note:
- The live WSL sandbox remains `/home/aletheon/v28-fluid-lab/`.
- This repo copy is the tracked source bundle and reporting surface.

## Overview

This suite is a safe, sandboxed framework for capability discovery, validation, and small experiments. It is intended to:

- catalog available tools and language/runtime support
- run a bounded capability test suite
- provide a safe experiment runner with rollback support
- emit JSON reports that can be integrated into Trinity OS validation workflows

## Layout

```text
/home/aletheon/v28-fluid-lab/
|-- experiments/
|-- artifacts/
|-- logs/
|-- snapshots/
|-- capability_discovery_probe.py
|-- fluid_capability_test_suite.py
|-- fluid_experiment_runner.py
`-- quick_start.py
```

The runtime sandbox keeps snapshots, rollback data, and experiment logs inside WSL. Only summarized reports should come back into the repo.

## Quick Start

1. Run `python3 capability_discovery_probe.py`.
2. Run `python3 fluid_capability_test_suite.py`.
3. Run `python3 fluid_experiment_runner.py`.

## Custom Experiments

The runner supports safe, bounded experiments for:

- package installation
- file manipulation
- process automation
- network exploration
- code generation
- system integration

## Safety

- Every experiment should stay inside the sandbox root.
- Snapshots should be taken before risky experiments.
- Rollback should be used when safety limits are violated.

## Success Criteria

- Discovery completes with a useful capability report.
- The test suite runs and records PASS/WARN/FAIL results.
- At least one bounded experiment can be run safely and summarized.
- The repo continues to track only the bundle and summary outputs.
