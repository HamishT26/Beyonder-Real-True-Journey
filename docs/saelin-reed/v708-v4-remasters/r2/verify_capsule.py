"""Verify selected capsule bytes without extracting or executing their contents."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import re


def pairs_unique(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError('duplicate decoded JSON key')
        value[key] = item
    return value


def nonfinite(value):
    raise ValueError('nonfinite JSON constant')


def path_profile(name):
    # Deliberately narrow portable profile, not an NTFS containment attestation.
    if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z0-9_./-]{1,1024}', name):
        return False
    reserved = re.compile(r'^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?$', re.I)
    return all(part not in ('', '.', '..') and not part.endswith('.')
               and len(part) <= 255 and not reserved.fullmatch(part)
               for part in name.split('/')) and not name.lower().endswith('.pdf')


def verify(raw, expected_sha256):
    if not isinstance(raw, bytes) or not 0 < len(raw) <= 10 * 1024 * 1024:
        raise ValueError('capsule must contain between one byte and ten MiB')
    if not isinstance(expected_sha256, str) or not re.fullmatch(r'[0-9a-fA-F]{64}', expected_sha256):
        raise ValueError('consumer-supplied expected SHA-256 is required')
    digest = hashlib.sha256(raw).hexdigest()
    if digest != expected_sha256.lower():
        raise ValueError('outer source expectation mismatch')
    capsule = json.loads(raw.decode('utf-8'), object_pairs_hook=pairs_unique, parse_constant=nonfinite)
    if not isinstance(capsule, dict) or not isinstance(capsule.get('files'), list) or not 1 <= len(capsule['files']) <= 1000:
        raise ValueError('bounded nonempty file inventory required')
    seen, selected = set(), []
    for item in capsule['files']:
        if not isinstance(item, dict):
            raise ValueError('file record must be an object')
        names = [item[k] for k in ('path', 'logical_path') if k in item]
        if len(names) != 1 or not path_profile(names[0]):
            raise ValueError('path outside the declared portable profile')
        name = names[0]
        if name.casefold() in seen:
            raise ValueError('duplicate or case-colliding path')
        seen.add(name.casefold())
        keys = [k for k in ('text', 'content_utf8', 'content_base64') if k in item]
        if len(keys) != 1 or not isinstance(item[keys[0]], str):
            raise ValueError('exactly one supported content representation required')
        if keys[0] == 'content_base64':
            payload = base64.b64decode(item[keys[0]], validate=True)
        else:
            payload = item[keys[0]].encode('utf-8')
        if type(item.get('bytes')) is not int or item['bytes'] < 0 or len(payload) != item['bytes']:
            raise ValueError('file byte count mismatch')
        inner = hashlib.sha256(payload).hexdigest()
        if not isinstance(item.get('sha256'), str) or inner != item['sha256'].lower():
            raise ValueError('file digest mismatch')
        selected.append({'path': name, 'bytes': len(payload), 'sha256': inner})
    return {'schema': 'ghc.selected-capsule-verification.v1', 'bytes': len(raw),
            'sha256': digest, 'verified_files': len(selected), 'files': selected,
            'extracted': False, 'executed': False,
            'scope': 'byte agreement with supplied expectation and narrow logical path profile; provenance, authority and OS containment not attested'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('capsule', type=Path)
    parser.add_argument('--expected-sha256', required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.capsule.stat().st_size > 10 * 1024 * 1024:
        parser.error('capsule exceeds ten MiB')
    result = verify(args.capsule.read_bytes(), args.expected_sha256)
    if args.output:
        with args.output.open('x', encoding='utf-8', newline='\n') as output:
            json.dump(result, output, indent=2)
            output.write('\n')
    print(json.dumps({'verified_files': result['verified_files'], 'sha256': result['sha256'],
                      'extracted': False, 'executed': False}))


if __name__ == '__main__':
    main()
