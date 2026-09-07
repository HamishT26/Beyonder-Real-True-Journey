"""One bounded OSV snapshot for the three exact pinned package versions."""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import pathlib
import urllib.request


PACKAGES = [("fonttools", "4.64.0"), ("uharfbuzz", "0.56.1"), ("unicodedata2", "17.0.1")]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()
    rows = []
    for name, version in PACKAGES:
        body = json.dumps({"package": {"name": name, "ecosystem": "PyPI"}, "version": version}).encode("utf-8")
        request = urllib.request.Request(
            "https://api.osv.dev/v1/query",
            data=body,
            headers={"Content-Type": "application/json", "User-Agent": "ghc-family-bounded-package-audit/1"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=25) as response:
            payload = json.loads(response.read().decode("utf-8"))
        vulnerabilities = [
            {"id": row.get("id"), "aliases": row.get("aliases", []), "summary": row.get("summary")}
            for row in payload.get("vulns", [])
        ]
        rows.append({"name": name, "version": version, "known_advisories": vulnerabilities, "known_advisory_count": len(vulnerabilities)})
    value = {
        "schema": "ghc.family.font-package-audit.v1",
        "source": "OSV v1 query API plus x1 official PyPI yanked metadata",
        "queried_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "rows": rows,
        "known_advisories": sum(row["known_advisory_count"] for row in rows),
        "independent_security_review": "open_gap",
        "exhaustive_security": False,
        "future_security_assurance": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"packages": 3, "known_advisories": value["known_advisories"], "output_sha256": hashlib.sha256(args.output.read_bytes()).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
