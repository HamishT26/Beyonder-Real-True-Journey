#!/usr/bin/env python3
"""Family-current bounded runner for Check synthetic sheet lots, trays, carriers, trial strips, splits, merges, substitutions, orphans, and handling refusal.."""

from ghc_family_v661_v4_runtime import cli

if __name__ == "__main__":
    cli("paper-sheet-lot-topology")
