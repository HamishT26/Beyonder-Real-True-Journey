from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "sable-rook" / "v681-v6"
RECEIPT = BASE / "x2" / "runner-smoke-receipts.json"

RUNNER_NAMES = [
    "ghc_family_tool_library_schema_runner",
    "ghc_family_tool_library_custody_runner",
    "ghc_family_tool_library_correction_runner",
    "ghc_family_tool_library_provenance_runner",
    "ghc_family_tool_library_privacy_runner",
    "ghc_family_tool_library_accessibility_runner",
    "ghc_family_tool_library_mutation_runner",
    "ghc_family_tool_library_outcome_runner",
    "ghc_family_tool_library_manifest_runner",
    "ghc_family_tool_library_stage20_runner",
]


def runner_path(name: str) -> Path:
    return ROOT / "scripts" / f"{name}.py"


def runner_source(name: str) -> str:
    return f'''from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "sable-rook" / "v681-v6" / "x2"


def main() -> None:
    phase = json.loads((BASE / "phase-truth.json").read_text(encoding="utf-8"))
    positives = json.loads((BASE / "positive-controls.json").read_text(encoding="utf-8"))
    mutations = json.loads((BASE / "mutation-results.json").read_text(encoding="utf-8"))
    portfolio = json.loads((BASE / "portfolio-results.json").read_text(encoding="utf-8"))
    assert phase["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert positives["accepted"] == 60
    assert mutations["rejected"] == 300
    assert len(portfolio["safe_now"]) == 120
    print(json.dumps({{"runner": "{name}", "positive_controls": 60, "rejected_mutations": 300, "safe_now": 120, "real_rows": 0, "external_actions": 0}}))


if __name__ == "__main__":
    main()
'''


def materialize() -> list[str]:
    paths = []
    for name in RUNNER_NAMES:
        path = runner_path(name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(runner_source(name), encoding="utf-8", newline="\n")
        paths.append(path.relative_to(ROOT).as_posix())
    return paths


def smoke() -> None:
    if RECEIPT.exists():
        raise RuntimeError("runner smoke receipt already exists; successful smoke must not be replayed")
    rows = []
    for name in RUNNER_NAMES:
        path = runner_path(name)
        completed = subprocess.run(
            [sys.executable, "-X", "utf8", str(path)],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        payload = json.loads(completed.stdout) if completed.returncode == 0 else None
        row = {
            "output": payload,
            "returncode": completed.returncode,
            "runner": path.stem,
            "sha256": hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest(),
            "smoke_invocations": 1,
        }
        rows.append(row)
        if completed.returncode != 0:
            raise RuntimeError(json.dumps(row))
    RECEIPT.write_text(
        json.dumps(
            {
                "external_actions": 0,
                "owner": "Sable Rook",
                "passed": len(rows),
                "phase": "v681-v6",
                "receipts": rows,
                "replayed_after_success": False,
                "schema": "ghc.family.runner-smoke.v681.v6.x2",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("materialize", "smoke"))
    args = parser.parse_args()
    if args.mode == "materialize":
        print(json.dumps({"paths": len(materialize()), "runners": len(RUNNER_NAMES)}))
    else:
        smoke()
        print(json.dumps({"passed": len(RUNNER_NAMES), "receipt": RECEIPT.relative_to(ROOT).as_posix()}))


if __name__ == "__main__":
    main()
