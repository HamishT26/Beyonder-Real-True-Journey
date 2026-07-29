#!/usr/bin/env python3
"""Run Vesper v655-v1 bounded contract group 2: SPICE kernel provenance and load-order boundary, FITS celestial header and world-coordinate boundary, dome geometry and fiducial survey proxy."""

from ghc_family_v655_v1_core import group_main


if __name__ == "__main__":
    group_main(2, "ghc_family_astronomical_timescale_normalizer")
