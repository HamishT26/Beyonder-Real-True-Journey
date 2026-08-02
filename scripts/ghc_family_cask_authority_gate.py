#!/usr/bin/env python3
"""Run the bounded Elowen synthetic cask-authority gate."""

from ghc_family_v659_v8_runtime import surface_cli


if __name__ == "__main__":
    surface_cli("cask-authority-ratification-gate")
