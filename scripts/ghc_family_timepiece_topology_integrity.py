#!/usr/bin/env python3
"""Run a bounded Caelen Morrow v656-v4 synthetic timepiece contract group."""

from __future__ import annotations

import json

import ghc_family_v656_v4_phase_data as d
from ghc_family_v656_v4_core import run_proposals


INDICES = [3, 4, 5]


if __name__ == "__main__":
    print(json.dumps(run_proposals([d.PROPOSALS[i] for i in INDICES]), sort_keys=True))
