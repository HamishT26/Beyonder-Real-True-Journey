#!/usr/bin/env python3
"""Family-current bounded runner for Preserve de-energised synthetic districts, feeders, returns, gaps, polarity, capacity unknowns, conflicts, and connection refusal.."""

from ghc_family_v661_v2_runtime import cli

if __name__ == "__main__":
    cli("model-railway-power-district-map")
