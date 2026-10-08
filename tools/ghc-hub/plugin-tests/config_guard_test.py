import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'plugins/ghc-nexus-config-menu/scripts'))
import config_guard as g


class GuardianConfigTests(unittest.TestCase):
    def setUp(self):
        base = Path(os.environ.get('GHC_HUB_TEST_TMP', str(ROOT/'plugin-tests/fixtures')))
        base.mkdir(parents=True, exist_ok=True)
        self.root = Path(tempfile.mkdtemp(prefix='guardian-', dir=base))
        self.file = self.root/'config.toml'
        self.backup = self.root/'private'
        self.backup.mkdir()

    def put(self, text):
        raw = text.encode('utf-8')
        self.file.write_bytes(raw)
        return raw, g.digest(raw)

    def test_root_and_profile_only_removal(self):
        raw, sha = self.put(
            'approval_policy="never"\n[features.guardianv2]\nthread_context=true\n'
            '[profiles."work mode".features.guardianv2]\nthread_context=false\n'
            '[other]\nthread_context="preserved"\n')
        revised, paths = g.remove_deprecated(raw)
        self.assertEqual(len(paths), 2)
        self.assertEqual(g.parse(revised)['other']['thread_context'], 'preserved')
        self.assertEqual(g.parse(revised)['approval_policy'], 'never')

    def test_dotted_assignment_with_implicit_tables(self):
        raw = b'features.guardianv2.thread_context=true\nmodel="keep"\n'
        after, paths = g.remove_deprecated(raw)
        self.assertEqual(after, b'model="keep"\n')
        self.assertEqual(len(paths), 1)

    def test_quoted_key_and_profile_dotted_assignment(self):
        raw = b'[profiles."a.b"]\nfeatures."guardianv2"."thread_context"=false\nmodel="keep"\n'
        after, paths = g.remove_deprecated(raw)
        self.assertEqual(len(paths), 1)
        self.assertEqual(g.parse(after)['profiles']['a.b']['model'], 'keep')

    def test_no_op_preserves_every_byte(self):
        raw = b'# thread_context=true\r\n[other]\r\nthread_context=true\r\n'
        self.assertEqual(g.remove_deprecated(raw), (raw, []))

    def test_bom_crlf_comments_and_unrelated_values(self):
        raw = b'\xef\xbb\xbf# heading\r\n[features.guardianv2]\r\nthread_context=true # obsolete\r\n# keep\r\n'
        after, _ = g.remove_deprecated(raw)
        self.assertEqual(after, b'\xef\xbb\xbf# heading\r\n[features.guardianv2]\r\n# keep\r\n')

    def test_inline_table_is_held_without_rewrite(self):
        with self.assertRaisesRegex(g.Issue, 'unsupported-assignment-syntax'):
            g.remove_deprecated(b'features={guardianv2={thread_context=true}}\n')

    def test_assignment_like_multiline_string_is_not_changed(self):
        raw = b'notes="""\n[features.guardianv2]\nthread_context=true\n"""\n[features.guardianv2]\nthread_context=true\n'
        with self.assertRaisesRegex(g.Issue, 'unsupported-assignment-syntax'):
            g.remove_deprecated(raw)

    def test_malformed_config_is_not_echoed(self):
        self.put('secret="private-synthetic-marker\n')
        with self.assertRaisesRegex(g.Issue, '^malformed-toml$'):
            g.audit(str(self.file))

    def test_audit_is_read_only_and_redacts_values(self):
        raw, _ = self.put('secret="private-synthetic-marker"\n[features.guardianv2]\nthread_context=true\n')
        report = g.audit(str(self.file))
        self.assertEqual(report['status'], 'deprecated-found')
        self.assertNotIn('private-synthetic-marker', json.dumps(report))
        self.assertEqual(self.file.read_bytes(), raw)

    def test_preview_never_writes(self):
        raw, sha = self.put('[features.guardianv2]\nthread_context=true\n')
        result = g.repair(str(self.file), sha, None)
        self.assertEqual(result['status'], 'ready')
        self.assertEqual(self.file.read_bytes(), raw)
        self.assertEqual(list(self.backup.iterdir()), [])

    def test_repair_backup_readback_and_second_no_op(self):
        raw, sha = self.put('model="keep"\n[features.guardianv2]\nthread_context=true\n')
        result = g.repair(str(self.file), sha, str(self.backup), True)
        self.assertTrue(result['configurationWritten'])
        self.assertEqual(Path(result['backupPath']).read_bytes(), raw)
        current = self.file.read_bytes()
        result2 = g.repair(str(self.file), g.digest(current), str(self.backup), True)
        self.assertEqual(result2['status'], 'clean')
        self.assertFalse(result2['configurationWritten'])
        self.assertEqual(len(list(self.backup.iterdir())), 1)

    def test_stale_hash_is_held(self):
        raw, _ = self.put('[features.guardianv2]\nthread_context=true\n')
        with self.assertRaisesRegex(g.Issue, 'source-hash-conflict'):
            g.repair(str(self.file), '0'*64, str(self.backup), True)
        self.assertEqual(self.file.read_bytes(), raw)

    def test_linked_file_is_held(self):
        _, sha = self.put('[features.guardianv2]\nthread_context=true\n')
        os.link(self.file, self.root/'linked.toml')
        with self.assertRaisesRegex(g.Issue, 'unsupported-file'):
            g.repair(str(self.file), sha, str(self.backup), True)

    def test_concurrent_edit_is_preserved(self):
        raw, sha = self.put('[features.guardianv2]\nthread_context=true\n')
        original = g.read_local
        count = 0
        def changed(filename, suffix):
            nonlocal count
            if Path(filename) == self.file:
                count += 1
                if count == 2:
                    self.file.write_bytes(raw + b'# later edit\n')
            return original(filename, suffix)
        with mock.patch.object(g, 'read_local', changed):
            with self.assertRaisesRegex(g.Issue, 'source-changed-before-write'):
                g.repair(str(self.file), sha, str(self.backup), True)
        self.assertEqual(self.file.read_bytes(), raw + b'# later edit\n')

    def test_backup_conflict_is_preserved(self):
        raw, sha = self.put('[features.guardianv2]\nthread_context=true\n')
        (self.backup/('guardian-config-'+sha+'.toml')).write_text('# other\n')
        with self.assertRaisesRegex(g.Issue, 'backup-conflict'):
            g.repair(str(self.file), sha, str(self.backup), True)
        self.assertEqual(self.file.read_bytes(), raw)

    def test_nonfinite_values_survive_semantic_comparison(self):
        raw = b'value=nan\n[features.guardianv2]\nthread_context=true\n'
        after, _ = g.remove_deprecated(raw)
        self.assertIn(b'value=nan', after)

    def test_config_inspector_reports_key_without_value(self):
        self.put('[profiles.admin.features.guardianv2]\nthread_context="private-synthetic-marker"\n')
        result = g.deprecated_paths(g.parse(self.file.read_bytes()))
        self.assertEqual(result, [['profiles','admin','features','guardianv2','thread_context']])
        self.assertNotIn('private-synthetic-marker', json.dumps(result))


if __name__ == '__main__':
    unittest.main(verbosity=2)
