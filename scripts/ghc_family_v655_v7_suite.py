#!/usr/bin/env python3
"""Run all thirty bounded Orin Thale v655-v7 contracts."""

from ghc_family_v655_v7_core import suite_main


if __name__ == "__main__":
    suite_main("ghc_family_v655_v7_suite")
