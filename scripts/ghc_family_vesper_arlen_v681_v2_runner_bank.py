from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "vesper-arlen" / "v681-v2"
RECEIPT = BASE / "x2" / "runner-smoke-receipts.json"
RUNNER_COUNT = 10


def runner_path(index: int) -> Path:
    return ROOT / "scripts" / f"ghc_family_vesper_v681_v2_lens_runner_{index:02d}.py"


def runner_source(index: int) -> str:
    return f'''from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "vesper-arlen" / "v681-v2" / "x2"


def main() -> None:
    phase = json.loads((BASE / "phase-truth.json").read_text(encoding="utf-8"))
    positives = json.loads((BASE / "positive-controls.json").read_text(encoding="utf-8"))
    mutations = json.loads((BASE / "mutation-results.json").read_text(encoding="utf-8"))
    assert phase["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert positives["accepted"] == 60
    assert mutations["rejected"] == 300
    print(json.dumps({{"runner": "ghc_family_vesper_v681_v2_lens_runner_{index:02d}", "positive_controls": 60, "rejected_mutations": 300, "real_rows": 0, "external_actions": 0}}))


if __name__ == "__main__":
    main()
'''


def materialize() -> list[str]:
    paths = []
    for index in range(1, RUNNER_COUNT + 1):
        path = runner_path(index)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(runner_source(index), encoding="utf-8", newline="\n")
        paths.append(path.relative_to(ROOT).as_posix())
    return paths


def smoke() -> None:
    if RECEIPT.exists():
        raise RuntimeError("runner smoke receipt already exists; successful smoke must not be replayed")
    rows = []
    for index in range(1, RUNNER_COUNT + 1):
        path = runner_path(index)
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
                "owner": "Vesper Arlen",
                "passed": len(rows),
                "phase": "v681-v2",
                "receipts": rows,
                "replayed_after_success": False,
                "schema": "ghc.family.runner-smoke.v681.v2.x2",
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
        print(json.dumps({"paths": len(materialize()), "runners": RUNNER_COUNT}))
    else:
        smoke()
        print(json.dumps({"passed": RUNNER_COUNT, "receipt": RECEIPT.relative_to(ROOT).as_posix()}))


if __name__ == "__main__":
    main()
