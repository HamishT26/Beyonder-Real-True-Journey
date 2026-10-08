"""Audit or explicitly repair only deprecated Guardian thread_context assignments.

Never emits configuration contents. Unsupported syntax stays unchanged. This is
a selected-file repair, not a background watcher or an App reload mechanism.
"""
import argparse
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import tempfile
import tomllib

from config_menu import Issue, read_local, deprecated_paths


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def parse(raw):
    try:
        return tomllib.loads(raw.decode('utf-8-sig'))
    except (ValueError, UnicodeError):
        raise Issue('malformed-toml') from None


def equivalent(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(equivalent(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(equivalent(x, y) for x, y in zip(a, b))
    if isinstance(a, float) and math.isnan(a):
        return math.isnan(b)
    return a == b


def sole_path(data):
    keys = []
    while isinstance(data, dict) and len(data) == 1:
        name, data = next(iter(data.items()))
        keys.append(name)
    return keys if data is True else None


def normalize_removed_containers(data, paths):
    result = copy.deepcopy(data)
    for target in paths:
        for length in range(len(target) - 1, 0, -1):
            parent = result
            for key in target[:length-1]:
                if not isinstance(parent, dict) or key not in parent:
                    parent = None
                    break
                parent = parent[key]
            if isinstance(parent, dict) and parent.get(target[length-1]) == {}:
                del parent[target[length-1]]
    return result


def remove_deprecated(raw):
    before = parse(raw)
    paths = deprecated_paths(before)
    if not paths:
        return raw, []
    expected = copy.deepcopy(before)
    for target in paths:
        node = expected
        for key in target[:-1]:
            node = node[key]
        del node[target[-1]]
    text = raw.decode('utf-8-sig')
    table = []
    kept = []
    targets = {tuple(p) for p in paths}
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        if stripped.startswith('['):
            try:
                parsed = tomllib.loads(stripped + '\n__ghc_guard_marker__=true\n')
                marker = sole_path(parsed)
                table = marker[:-1] if marker and marker[-1] == '__ghc_guard_marker__' else None
            except ValueError:
                table = None
        removed = False
        if table is not None and '=' in line and not stripped.startswith('#'):
            key = line.split('=', 1)[0].strip()
            try:
                local = sole_path(tomllib.loads(key + '=true'))
            except ValueError:
                local = None
            if local and tuple([*table, *local]) in targets:
                removed = True
        if not removed:
            kept.append(line)
    result = ''.join(kept).encode('utf-8')
    if raw.startswith(b'\xef\xbb\xbf'):
        result = b'\xef\xbb\xbf' + result
    # This also rejects accidental matches inside multiline strings, inline
    # tables and any rewrite that changes a value outside the exact allowlist.
    try:
        after = parse(result)
    except Issue:
        raise Issue('unsupported-assignment-syntax') from None
    if deprecated_paths(after) or not equivalent(
            normalize_removed_containers(after, paths), normalize_removed_containers(expected, paths)):
        raise Issue('unsupported-assignment-syntax')
    return result, paths


def audit(filename):
    raw, resolved = read_local(filename, '.toml')
    paths = deprecated_paths(parse(raw))
    return {'schema': 'ghc.nexus.config-guard.v1', 'path': resolved,
            'sha256': digest(raw), 'status': 'deprecated-found' if paths else 'clean',
            'deprecatedKeys': paths, 'configurationWritten': False,
            'scope': 'selected-file; running-client state not measured'}


def backup_directory(value, target):
    directory = Path(value)
    if not directory.is_absolute() or str(value).startswith(('\\\\', '//')):
        raise Issue('invalid-backup-directory')
    try:
        for part in (directory, *directory.parents):
            s = part.lstat()
            if stat.S_ISLNK(s.st_mode) or getattr(s, 'st_file_attributes', 0) & 0x400:
                raise Issue('linked-backup-directory')
        if not directory.is_dir() or directory.resolve() == target.parent.resolve():
            raise Issue('separate-private-backup-required')
    except OSError:
        raise Issue('backup-directory-unavailable') from None
    return directory


def repair(filename, expected, backup, execute=False):
    if not isinstance(expected, str) or not re.fullmatch('[0-9a-f]{64}', expected):
        raise Issue('invalid-expected-hash')
    raw, resolved = read_local(filename, '.toml')
    if digest(raw) != expected:
        raise Issue('source-hash-conflict')
    revised, paths = remove_deprecated(raw)
    result = {'schema': 'ghc.nexus.config-guard.v1', 'path': resolved,
              'beforeSha256': expected, 'afterSha256': digest(revised),
              'deprecatedKeys': paths, 'configurationWritten': False,
              'status': 'ready' if paths else 'clean',
              'otherParsedSettingsUnchanged': True}
    if not execute or not paths:
        return result
    target = Path(resolved)
    directory = backup_directory(backup, target)
    original_mode = stat.S_IMODE(target.stat().st_mode)
    destination = directory / ('guardian-config-' + expected + '.toml')
    try:
        with destination.open('xb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
    except FileExistsError:
        saved, _ = read_local(str(destination), '.toml')
        if saved != raw:
            raise Issue('backup-conflict') from None
    os.chmod(destination, stat.S_IRUSR | stat.S_IWUSR)
    saved, _ = read_local(str(destination), '.toml')
    if saved != raw:
        raise Issue('backup-readback-failed')
    temporary = None
    mutated = False
    try:
        fd, temporary = tempfile.mkstemp(prefix='.ghc-config-', suffix='.tmp', dir=target.parent)
        with os.fdopen(fd, 'wb') as stream:
            stream.write(revised)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, original_mode)
        current, current_path = read_local(filename, '.toml')
        if current != raw or current_path != resolved:
            raise Issue('source-changed-before-write')
        os.replace(temporary, target)
        mutated = True
        temporary = None
        actual, _ = read_local(filename, '.toml')
        if actual != revised:
            raise Issue('post-write-conflict')
    except (Issue, OSError) as error:
        error.configuration_written = mutated
        raise
    finally:
        if temporary is not None:
            os.unlink(temporary)
    return result | {'status': 'repaired', 'configurationWritten': True,
                     'backupPath': str(destination), 'backupSha256': expected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['audit', 'repair'])
    parser.add_argument('--file', required=True)
    parser.add_argument('--expected-sha256')
    parser.add_argument('--backup-dir')
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    try:
        if args.operation == 'audit' and (args.execute or args.expected_sha256 or args.backup_dir):
            raise Issue('unsupported-audit-option')
        if args.execute and not args.backup_dir:
            raise Issue('private-backup-directory-required')
        result = audit(args.file) if args.operation == 'audit' else repair(
            args.file, args.expected_sha256, args.backup_dir, args.execute)
        print(json.dumps(result, ensure_ascii=True))
        return 0
    except (Issue, OSError, TypeError) as error:
        reason = str(error) if isinstance(error, Issue) else 'file-operation-failed'
        print(json.dumps({'status': 'refused', 'reason': reason,
                          'configurationWritten': getattr(error, 'configuration_written', False)}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
