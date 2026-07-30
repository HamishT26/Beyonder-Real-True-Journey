#!/usr/bin/env python3
"""Run Tamar Vey v656-v1 bounded contract group 3: chemical capacity, replenishment, carry-over, exhaustion, reuse budget, threshold, uncertainty, hold, and potency refusal, vessel, lid, label, funnel, measure, dedicated use, rinse, cross-contamination quarantine, and safety-decision refusal, light leak, safelight source, distance, duration, material class, test reservation, fault hold, and optical-measurement refusal."""

from ghc_family_v656_v1_core import group_main


if __name__ == "__main__":
    group_main(3, "ghc_family_darkroom_capacity_waste_reserve")
