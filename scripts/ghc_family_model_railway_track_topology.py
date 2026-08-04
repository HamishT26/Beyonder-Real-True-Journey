#!/usr/bin/env python3
"""Family-current bounded runner for Check synthetic modules, track, turnouts, crossings, connectors, adjacency, orphans, loops, gauge conflicts, and construction refusal.."""

from ghc_family_v661_v2_runtime import cli

if __name__ == "__main__":
    cli("model-railway-track-topology")
