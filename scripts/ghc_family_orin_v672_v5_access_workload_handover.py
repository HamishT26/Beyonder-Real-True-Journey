"""Family-current bounded runner for the access_workload_handover surface."""

from __future__ import annotations

import json

from scripts.ghc_family_orin_v672_v5_provenance import run_surface


def main() -> None:
    print(json.dumps(run_surface("access_workload_handover"), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
