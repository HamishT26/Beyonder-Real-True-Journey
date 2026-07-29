#!/usr/bin/env python3
"""Run Lyren v655-v2 bounded contract group 3: repair tool calibration and condition proxy, electrostatic-discharge bench-state proxy, lithium-battery damage and quarantine proxy."""

from ghc_family_v655_v2_core import group_main


if __name__ == "__main__":
    group_main(3, "ghc_family_repair_part_custody")
