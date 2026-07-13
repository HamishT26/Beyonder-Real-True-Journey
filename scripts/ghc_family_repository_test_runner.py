#!/usr/bin/env python3
"""Run unittest discovery with an explicit Windows temp ACL adapter.

Python 3.12 requests mode 0700 for ``tempfile.mkdtemp``. In this managed
Windows execution context, those children can become inaccessible to the
creating process. The optional adapter creates only ephemeral child
directories with the existing parent ACL. It does not change a parent ACL,
host security setting, Windows feature, test module, or repository fixture.
"""

from __future__ import annotations

import argparse
import errno
import json
import os
import secrets
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


def inherited_acl_mkdtemp(suffix: Any = None, prefix: Any = None, dir: Any = None) -> Any:
    """Create one unique temporary child using its existing parent ACL."""
    output_type = bytes if any(isinstance(value, bytes) for value in (suffix, prefix, dir) if value is not None) else str
    suffix = (b"" if output_type is bytes else "") if suffix is None else suffix
    prefix = (b"tmp" if output_type is bytes else "tmp") if prefix is None else prefix
    base = tempfile.gettempdir() if dir is None else dir
    if output_type is bytes:
        base = os.fsencode(base)
    for _ in range(10000):
        token: Any = secrets.token_hex(8)
        if output_type is bytes:
            token = token.encode("ascii")
        path = os.path.join(base, prefix + token + suffix)
        try:
            os.mkdir(path)
        except FileExistsError:
            continue
        return os.path.abspath(path)
    raise FileExistsError(errno.EEXIST, "no usable inherited-ACL temp directory name found")


def run(start: Path, pattern: str, use_windows_inherited_acl_temp: bool) -> unittest.result.TestResult:
    if use_windows_inherited_acl_temp:
        if os.name != "nt":
            raise SystemExit("--windows-inherited-acl-temp is Windows-only")
        tempfile.mkdtemp = inherited_acl_mkdtemp
    repository = start.parent
    if str(repository) not in sys.path:
        sys.path.insert(0, str(repository))
    suite = unittest.defaultTestLoader.discover(str(start), pattern=pattern)
    return unittest.TextTestRunner(verbosity=1).run(suite)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start-directory", type=Path, default=Path("tests"))
    parser.add_argument("--pattern", default="test_*.py")
    parser.add_argument("--windows-inherited-acl-temp", action="store_true")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    result = run(args.start_directory.resolve(), args.pattern, args.windows_inherited_acl_temp)
    receipt = {
        "schema": "ghc.family.repository-test-runner-console-receipt.v1",
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
        "windows_inherited_acl_temp": args.windows_inherited_acl_temp,
        "parent_acl_changed": False,
        "host_security_changed": False,
    }
    print(json.dumps(receipt, ensure_ascii=False))
    raise SystemExit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()
