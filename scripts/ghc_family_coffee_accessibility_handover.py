#!/usr/bin/env python3
"""Run a bounded Eiren Kestrel v656-v5 synthetic coffee-roasting contract group."""

from __future__ import annotations

import json

import ghc_family_v656_v5_phase_data as d
from ghc_family_v656_v5_core import run_proposals


INDICES = [18, 19, 20]


if __name__ == "__main__":
    print(json.dumps(run_proposals([d.PROPOSALS[i] for i in INDICES]), sort_keys=True))
