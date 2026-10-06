"""Selected Codex layer inspection and proposals. No configuration write path."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import stat
import sys
import tomllib

LIMIT = 1_048_576
ALLOWLIST = {'tui.alternate_screen': ('auto', 'always', 'never'),
             'tui.animations': bool, 'hide_agent_reasoning': bool}

class Issue(ValueError):
    pass

def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise Issue('duplicate-json-key')
        result[key] = value
    return result

def read_local(filename, suffix):
    if not isinstance(filename, str) or len(filename) > 4096 or any(ord(c) < 32 for c in filename):
        raise Issue('invalid-path')
    p = Path(filename)
    if not p.is_absolute() or filename.startswith(('\\\\', '//')) or p.suffix.lower() != suffix:
        raise Issue('invalid-local-file')
    try:
        for part in (p, *p.parents):
            s = part.lstat()
            if stat.S_ISLNK(s.st_mode) or getattr(s, 'st_file_attributes', 0) & 0x400:
                raise Issue('linked-path')
        s = p.stat()
        if not stat.S_ISREG(s.st_mode) or s.st_nlink != 1 or s.st_size > LIMIT:
            raise Issue('unsupported-file')
        with p.open('rb') as stream:
            data = stream.read(LIMIT + 1)
        if len(data) > LIMIT:
            raise Issue('oversized-file')
        after = p.stat()
        if (s.st_ino, s.st_size, s.st_mtime_ns) != (after.st_ino, after.st_size, after.st_mtime_ns):
            raise Issue('source-changed-during-read')
        return data, str(p.resolve())
    except Issue:
        raise
    except OSError:
        raise Issue('file-unavailable') from None

def valid_value(key, value):
    rule = ALLOWLIST[key]
    return type(value) is bool if rule is bool else type(value) is str and value in rule

def selected_values(data):
    result = {}
    for key in ALLOWLIST:
        obj = data
        for name in key.split('.'):
            if not isinstance(obj, dict) or name not in obj:
                break
            obj = obj[name]
        else:
            result[key] = {'valid': valid_value(key, obj), 'value': obj if valid_value(key, obj) else None}
    return result

def inspect(spec):
    if not isinstance(spec, dict) or type(spec.get('schemaVersion')) is not int or spec['schemaVersion'] != 1:
        raise Issue('invalid-spec-schema')
    layers = spec.get('layers')
    if not isinstance(layers, list) or not 1 <= len(layers) <= 8:
        raise Issue('invalid-layer-count')
    names, paths, rows, winners = set(), set(), [], {}
    for layer in layers:
        if not isinstance(layer, dict) or set(layer) != {'name', 'path', 'active'}:
            raise Issue('invalid-layer-shape')
        name = layer['name']
        if not isinstance(name, str) or not re.fullmatch(r'[a-z][a-z0-9-]{0,39}', name) or name in names or type(layer['active']) is not bool:
            raise Issue('invalid-or-duplicate-layer')
        names.add(name)
        row = {'name': name, 'activeDeclared': layer['active'], 'status': 'unavailable'}
        try:
            raw, resolved = read_local(layer['path'], '.toml')
            path_key = resolved.casefold() if sys.platform == 'win32' else resolved
            if path_key in paths:
                raise Issue('duplicate-layer-path')
            paths.add(path_key)
            try:
                data = tomllib.loads(raw.decode('utf-8-sig'))
            except (ValueError, UnicodeError):
                raise Issue('malformed-toml') from None
            values = selected_values(data)
            row.update(status='observed', path=resolved, sha256=hashlib.sha256(raw).hexdigest(), values=values)
            if layer['active']:
                for key, value in values.items():
                    winners[key] = {'layer': name, **value}
        except Issue as error:
            if str(error) == 'duplicate-layer-path':
                raise
            row['reason'] = str(error)
        rows.append(row)
    return {'schema': 'ghc.nexus.config-inspection.v1', 'scope': 'selected-layers-only',
            'applicability': 'caller-declared; host policy, project trust and invocation overrides not measured',
            'layers': rows, 'selectedWinners': winners, 'configurationWritten': False}

def propose(spec, target, expected, settings):
    report = inspect(spec)
    if not isinstance(expected, str) or not re.fullmatch('[0-9a-f]{64}', expected):
        raise Issue('invalid-expected-hash')
    changes = {}
    for setting in settings:
        if not isinstance(setting, str) or len(setting) > 160 or '=' not in setting:
            raise Issue('invalid-setting')
        key, text = setting.split('=', 1)
        if key not in ALLOWLIST or key in changes:
            raise Issue('unsupported-or-duplicate-key')
        try:
            value = json.loads(text)
        except ValueError:
            raise Issue('invalid-setting-value') from None
        if not valid_value(key, value):
            raise Issue('invalid-setting-value')
        changes[key] = value
    if not changes:
        raise Issue('empty-proposal')
    selected = next((r for r in report['layers'] if r['name'] == target), None)
    if selected is None:
        raise Issue('unknown-target')
    result = {'schema': 'ghc.nexus.config-proposal.v1', 'status': 'held', 'target': target,
              'configurationWritten': False, 'scope': report['scope'], 'applicability': report['applicability']}
    if any(r['status'] != 'observed' for r in report['layers']):
        return result | {'reason': 'selected-layer-unavailable'}
    if any(not value['valid'] for r in report['layers'] if r['activeDeclared'] for value in r['values'].values()):
        return result | {'reason': 'invalid-allowlisted-source-value'}
    if not selected['activeDeclared']:
        return result | {'reason': 'target-not-declared-active'}
    if selected['sha256'] != expected:
        return result | {'reason': 'source-hash-conflict', 'observedSha256': selected['sha256']}
    target_index = report['layers'].index(selected)
    conflicts = [{'key': key, 'higherLayer': r['name']} for key in changes
                 for r in report['layers'][target_index+1:] if r['activeDeclared'] and key in r['values']]
    result.update(path=selected['path'], expectedSha256=expected,
                  changes=[{'key': k, 'before': selected['values'].get(k, {}).get('value'), 'after': v} for k,v in changes.items()],
                  conflicts=conflicts,
                  backup={'requiredBeforeWrite': True, 'expectedSha256': expected,
                          'storage': 'private D-drive bank outside plugin/release exports; full config may contain secrets'},
                  rollback={'precondition': 'current bytes equal the recorded post-change hash; preserve later edits otherwise',
                            'action': 'restore the private original, parse TOML and verify its original digest'},
                  applied=False)
    result['status'] = 'conflict' if conflicts else 'ready-for-review'
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['inspect', 'propose'])
    parser.add_argument('--spec', required=True)
    parser.add_argument('--target')
    parser.add_argument('--expected-sha256')
    parser.add_argument('--set', action='append', default=[], dest='settings')
    args = parser.parse_args()
    try:
        raw, _ = read_local(args.spec, '.json')
        try:
            spec = json.loads(raw, object_pairs_hook=unique)
        except (ValueError, UnicodeError):
            raise Issue('invalid-spec-json') from None
        result = inspect(spec) if args.operation == 'inspect' else propose(spec, args.target, args.expected_sha256, args.settings)
        print(json.dumps(result, ensure_ascii=True))
        return 0 if result.get('status') in (None, 'ready-for-review') else 2
    except Issue as error:
        print(json.dumps({'status': 'refused', 'reason': str(error), 'configurationWritten': False}))
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
