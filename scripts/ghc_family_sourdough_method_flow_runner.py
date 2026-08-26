"""Family-current bounded method_flow runner for Vesper v669-v8."""

from __future__ import annotations

import json

from ghc_family_sourdough_contracts import runner_entry


def main() -> None:
    print(json.dumps(runner_entry("method_flow"), sort_keys=True))


if __name__ == "__main__":
    main()
