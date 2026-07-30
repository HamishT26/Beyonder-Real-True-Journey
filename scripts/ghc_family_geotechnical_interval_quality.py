#!/usr/bin/env python3
"""Run Orin Thale v655-v7 bounded contract group 4: depth, unit, overlap, duplicate, ordering, quarantine, and interpretation refusal, field-log workload, unresolved interval, sample hold, alert, break, readback, and release refusal, incident, near miss, complaint, correction, hold, remedy, and adjudication refusal."""

from ghc_family_v655_v7_core import group_main


if __name__ == "__main__":
    group_main(4, "ghc_family_geotechnical_interval_quality")
