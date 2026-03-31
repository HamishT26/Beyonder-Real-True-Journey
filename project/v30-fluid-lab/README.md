# V30 Fluid Lab

Repo-tracked V30 runtime bundle for bounded Ubuntu-side experimentation.

Runtime sandbox note:
- The live WSL sandbox is `/home/aletheon/v30-fluid-lab/`.
- This repo copy is the tracked source bundle.
- The preserved external contributor prototype bundle lives separately at
  `project/v30-experiment-proposals-source/`.

## Overview

This bundle keeps V30 experiments split across two lanes:

- controller-run proofs for connector/materialization work such as Gmail,
  Hugging Face, and Composio
- sandbox-run proofs for local autonomy, bounded self-healing, kairotic
  integration, and living-doc generation

The runtime sandbox keeps snapshots, rollback data, temporary outputs, and
experiment logs inside WSL. Only summarized proof artifacts and clearly marked
non-authoritative docs should come back into the repo.

## Layout

```text
/home/aletheon/v30-fluid-lab/
|-- experiments/
|-- artifacts/
|-- logs/
|-- snapshots/
|-- capability_discovery_probe.py
|-- fluid_capability_test_suite.py
|-- fluid_experiment_runner.py
|-- quick_start.py
`-- v30_experiment_orchestrator.py
```

## Quick Start

1. Run `python3 capability_discovery_probe.py`.
2. Run `python3 fluid_capability_test_suite.py`.
3. Run `python3 v30_experiment_orchestrator.py --list`.
4. Run `python3 v30_experiment_orchestrator.py --local-only`.

## Local Experiments

The local V30 lane focuses on:

- a bounded Ubuntu autonomy proof
- bounded self-healing observations and sandbox temp cleanup
- kairotic proof generation using the existing repo surface
- non-authoritative living docs generated from current repo truth

## Controller-Run Experiments

The Gmail and Hugging Face experiments are preserved in the bundle for lineage,
but they are expected to receive controller/session proof inputs rather than be
blindly executed inside WSL.

## Safety

- Every experiment stays inside the sandbox or on explicitly named repo paths.
- Snapshots are taken before risky local experiments.
- Rollback is used on safety violations.
- Standard and deep suite defaults stay offline-safe unless an explicit V30
  bridge turns on a live lane.
