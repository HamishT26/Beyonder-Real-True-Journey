"""Exclusive exact-final owner-scoped canonical latch for Lyren v683-v2."""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import sys

import scripts.ghc_family_eiren_kestrel_v682_v6_canonical as template
from scripts.build_ghc_family_lyren_moss_v683_v2_final import map_repo_path


BRANCH = "codex/GHC-Family/lyren-moss-v683-v2-full-tools"
SOURCE = "484d44fb8875bf8129143c99e5340d2e2044fbd2"
X1 = "57dcd8a0e6e5a43f87d6f1a5a0d79d2d68b66d8b"
EVIDENCE = "d0240efd7c7369e1468882d62bebddce32cf8b85"


def map_arg(value: str) -> str:
    value = map_repo_path(value)
    return value.replace(
        "tests.test_ghc_family_eiren_kestrel_v682_v6_final",
        "tests.test_ghc_family_lyren_moss_v683_v2_final",
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
        payload["owner"] = "Lyren Moss"
        payload["phase"] = "v683-v2"
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
