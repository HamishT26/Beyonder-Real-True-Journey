#!/usr/bin/env python3
"""Family-current bounded runner for Validate bounded MARC 255 and 034 scale, projection, coordinate, provenance, malformed-input, and refusal fixtures.."""

from ghc_family_v661_v7_runtime import cli

if __name__ == "__main__":
    cli("ogc-records-zero-row-map-adapter")
