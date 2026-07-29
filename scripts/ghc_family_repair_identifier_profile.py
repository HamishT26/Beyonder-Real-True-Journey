#!/usr/bin/env python3
"""Run Lyren v655-v2 bounded contract group 9: fail-closed repair queue and workload governor, repair asset identifier and referent separation, repair decision provenance, correction, and remedy hold."""

from ghc_family_v655_v2_core import group_main


if __name__ == "__main__":
    group_main(9, "ghc_family_repair_identifier_profile")
