#!/usr/bin/env python3
"""Run Orin Thale v655-v7 bounded contract group 8: typed effective stress, pore pressure, strength parameters, sign, units, domain, and prediction firewall, typed consolidation diffusion, drainage, time, coefficient, boundary, initial state, units, and settlement refusal, slope mechanism, strength model, pore pressure, load, geometry, uncertainty, and stability-prediction refusal."""

from ghc_family_v655_v7_core import group_main


if __name__ == "__main__":
    group_main(8, "ghc_family_gmut_geomechanics_firewall")
