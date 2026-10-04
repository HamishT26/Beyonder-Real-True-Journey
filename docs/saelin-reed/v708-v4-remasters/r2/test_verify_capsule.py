import base64
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('capsule_guard', Path(__file__).with_name('verify_capsule.py'))
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


def raw_files(files):
    return json.dumps({'files': files}).encode('utf-8')


def fixture(key='text'):
    content = b'bounded fixture\n'
    return {'path': 'source/fixture.txt', 'bytes': len(content),
            'sha256': hashlib.sha256(content).hexdigest(),
            key: base64.b64encode(content).decode() if key == 'content_base64' else content.decode()}


class CapsuleTests(unittest.TestCase):
    def accepted(self, data):
        return guard.verify(data, hashlib.sha256(data).hexdigest())

    def test_three_exact_transport_forms(self):
        for key in ('text', 'content_utf8', 'content_base64'):
            with self.subTest(key=key):
                result = self.accepted(raw_files([fixture(key)]))
                self.assertEqual(result['verified_files'], 1)
                self.assertFalse(result['executed'])

    def test_mismatched_outer_expectation(self):
        with self.assertRaises(ValueError):
            guard.verify(raw_files([fixture()]), '0' * 64)

    def test_duplicate_decoded_json_key(self):
        raw = b'{"files":[],"fi\\u006ces":[]}'
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            self.accepted(raw)

    def test_parent_path_rejected(self):
        item = fixture(); item['path'] = 'source/../outside'
        with self.assertRaises(ValueError): self.accepted(raw_files([item]))

    def test_case_collision_rejected(self):
        item = fixture(); other = fixture(); other['path'] = item['path'].upper()
        with self.assertRaises(ValueError): self.accepted(raw_files([item, other]))

    def test_ambiguous_content_rejected(self):
        item = fixture(); item['content_utf8'] = item['text']
        with self.assertRaises(ValueError): self.accepted(raw_files([item]))

    def test_changed_payload_rejected(self):
        item = fixture(); item['text'] = 'changed fixture\n'
        with self.assertRaises(ValueError): self.accepted(raw_files([item]))

    def test_invalid_base64_rejected(self):
        item = fixture('content_base64'); item['content_base64'] += '!'
        with self.assertRaises(ValueError): self.accepted(raw_files([item]))

    def test_reserved_and_pdf_names_rejected(self):
        for path in ('source/CON.txt', 'source/a.pdf'):
            with self.subTest(path=path):
                item = fixture(); item['path'] = path
                with self.assertRaises(ValueError): self.accepted(raw_files([item]))


if __name__ == '__main__':
    unittest.main(verbosity=2)
