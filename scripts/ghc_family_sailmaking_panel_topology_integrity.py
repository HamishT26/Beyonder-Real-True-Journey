#!/usr/bin/env python3
"""Run Elowen Cairn v656-v2 bounded contract group 2: cloth roll, lot, material class, weave direction, finish, width, defect, substitution, and material-property refusal, warp, fill, bias, radial, crosscut, load-path annotation, conflict, confidence, and strength-inference refusal, seam allowance, overlap, stitch row, turnback, edge finish, length, tolerance, dependency, and machine-instruction refusal."""

from ghc_family_v656_v2_core import group_main


if __name__ == "__main__":
    group_main(2, "ghc_family_sailmaking_panel_topology_integrity")
