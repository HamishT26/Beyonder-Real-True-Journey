#!/usr/bin/env python3
"""Family-current bounded runner for Expose synthetic turnout, route, conflict, detection unknown, lock, cancellation, release hold, and no-safety-claim relations.."""

from ghc_family_v661_v2_runtime import cli

if __name__ == "__main__":
    cli("model-railway-turnout-route-dependency")
