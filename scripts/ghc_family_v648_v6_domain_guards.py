#!/usr/bin/env python3
"""Family-current bounded v648-v6 runner."""

from ghc_family_v648_v6_runtime import cli_for


if __name__ == "__main__":
    cli_for(["V6486-P09","V6486-P10"], "ghc_family_v648_v6_domain_guards.py")
