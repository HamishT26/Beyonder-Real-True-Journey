"""Exclusive exact-final owner-scoped canonical latch for Neris v682-v8."""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import sys

import scripts.ghc_family_eiren_kestrel_v682_v6_canonical as template
from scripts.build_ghc_family_elaren_kestrel_v682_v7_final import (
    map_repo_path as elaren_map_repo_path,
)
from scripts.build_ghc_family_neris_solane_v682_v8_final import map_repo_path

BRANCH = "codex/GHC-Family/neris-solane-v682-v8-full-tools"
SOURCE = "938162611d2ce944ddcddf64834bd93e045e3c49"
X1 = "d1a3bb0fc1964608478dcc1bc9b236183617ef8a"
EVIDENCE = "6b64714a680ecebdb39785bccbe13c50e87fbd18"


def map_arg(value: str) -> str:
    value = map_repo_path(elaren_map_repo_path(value))
    return value.replace(
        "tests.test_ghc_family_eiren_kestrel_v682_v6_final",
        "tests.test_ghc_family_neris_solane_v682_v8_final",
    )


def main() -> int:
    template.BRANCH = BRANCH
    template.REMOTE_REF = f"refs/heads/{BRANCH}"
    template.SOURCE = SOURCE
    template.X1 = X1
    template.EVIDENCE = EVIDENCE
    original_run = template.run

    def mapped_run(args: list[str], **kwargs):
        return original_run([map_arg(item) for item in args], **kwargs)

    template.run = mapped_run
    capture = io.StringIO()
    with contextlib.redirect_stdout(capture):
        result = template.main()

    receipt_arg = sys.argv[sys.argv.index("--receipt") + 1]
    receipt = template.Path(receipt_arg).resolve()
    if receipt.exists():
        payload = json.loads(receipt.read_text(encoding="utf-8"))
        payload["owner"] = "Neris Solane"
        payload["phase"] = "v682-v8"
        payload_without_digest = {
            key: value for key, value in payload.items() if key != "payload_sha256"
        }
        payload_bytes = json.dumps(
            payload_without_digest,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        payload["payload_sha256"] = hashlib.sha256(payload_bytes).hexdigest()
        receipt.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        print(
            json.dumps(
                {
                    "checks_passed": sum(
                        1 for value in payload["checks"].values() if value
                    ),
                    "checks_total": len(payload["checks"]),
                    "head": payload["head"],
                    "payload_sha256": payload["payload_sha256"],
                    "status": payload["status"],
                },
                separators=(",", ":"),
            )
        )
    else:
        print(capture.getvalue().strip())
    return result


if __name__ == "__main__":
    raise SystemExit(main())
