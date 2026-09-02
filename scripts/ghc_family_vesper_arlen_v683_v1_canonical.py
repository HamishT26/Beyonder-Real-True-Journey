"""Exclusive exact-final owner-scoped canonical latch for Vesper v683-v1."""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import sys

import scripts.ghc_family_eiren_kestrel_v682_v6_canonical as template
from scripts.build_ghc_family_vesper_arlen_v683_v1_final import map_repo_path

BRANCH = "codex/GHC-Family/vesper-arlen-v683-v1-full-tools"
SOURCE = "22c32b5ec50af2f59f221b18bfbe468f0b6bd1e7"
X1 = "2981dcc774afce801973f8e3a9e6643b5e22dcee"
EVIDENCE = "40177e37035c377b5cb7d8d6d5c66f8de54ddbd0"


def map_arg(value: str) -> str:
    value = map_repo_path(value)
    return value.replace(
        "tests.test_ghc_family_eiren_kestrel_v682_v6_final",
        "tests.test_ghc_family_vesper_arlen_v683_v1_final",
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
        payload["owner"] = "Vesper Arlen"
        payload["phase"] = "v683-v1"
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
                    "checks_passed": sum(1 for value in payload["checks"].values() if value),
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
