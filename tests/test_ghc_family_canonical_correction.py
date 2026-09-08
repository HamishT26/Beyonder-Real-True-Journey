"""Verify the exact byte-domain repair without invoking either canonical."""
import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REL='docs/seren-talewood/v689-v2-r2/final/correction'
FOLDER=ROOT/REL
spec=importlib.util.spec_from_file_location('corrected_definition',FOLDER/'ghc_family_corrected_canonical.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def load(path):return json.loads(path.read_text(encoding='utf-8'))

class CorrectionContract(unittest.TestCase):
    def test_twenty_two_exact_byte_domains_are_reversible(self):
        rows=load(FOLDER/'byte-domain-bindings.json')['mismatches'];self.assertEqual(len(rows),22)
        self.assertEqual(sum(r['path'].endswith('openai.yaml') for r in rows),20)
        for row in rows:
            git_raw=(ROOT/row['path']).read_bytes().replace(b'\r\n',b'\n')
            restored=m.restore_checkout(git_raw,row)
            self.assertEqual(hashlib.sha256(restored).hexdigest(),row['declared_sha256'])
            self.assertEqual(restored.replace(b'\r\n',b'\n'),git_raw)

    def test_an_unbound_byte_change_is_rejected(self):
        row=load(FOLDER/'byte-domain-bindings.json')['mismatches'][0]
        raw=(ROOT/row['path']).read_bytes().replace(b'\r\n',b'\n')
        with self.assertRaises(AssertionError):m.restore_checkout(raw+b' ',row)

    def test_prior_failure_and_one_success_limit_are_explicit(self):
        policy=load(FOLDER/'policy.json');failed=load(FOLDER/'retained-first-failure.json')
        self.assertEqual((failed['invocations'],failed['successes']),(1,0))
        self.assertEqual(policy['total_attempt_limit'],2)
        self.assertEqual(policy['corrected_invocation_limit'],1)
        self.assertFalse(policy['successful_replay_authorized'])
        self.assertEqual(policy['retained_definition_sha256'],hashlib.sha256((FOLDER.parent/'ghc_family_canonical.py').read_bytes()).hexdigest())
        self.assertEqual(policy['corrected_definition_sha256'],hashlib.sha256((FOLDER/'ghc_family_corrected_canonical.py').read_bytes()).hexdigest())

    def test_corrected_git_seal_covers_all_current_files(self):
        seal=load(FOLDER/'git-content-seal.json');bindings={r['path'] for r in load(FOLDER/'byte-domain-bindings.json')['mismatches']}
        objects={}
        for path in ROOT.rglob('*'):
            if not path.is_file() or path.name=='.git' or '__pycache__' in path.parts:continue
            relative=path.relative_to(ROOT).as_posix();raw=path.read_bytes()
            if relative in bindings:raw=raw.replace(b'\r\n',b'\n')
            objects[relative]={'raw':raw,'oid':None}
        pending={REL+'/'+n for n in ['manifest.json','staged-review.json']}-set(objects)
        m.c.verify_manifest(seal,objects,set(objects)|pending)

    def test_current_totals_add_only_the_operational_correction(self):
        data=load(FOLDER/'count-overlay.json')
        self.assertEqual(data['additional_owner_delta'],dict(proposals=0,methods=1,negatives=1,failed_witnesses=1,passing_witnesses=1))
        self.assertEqual(data['current_owner_delta'],dict(proposals=200,methods=71,negatives=240,failed_witnesses=240,passing_witnesses=394))
        self.assertEqual(data['prior_failure_success_credit'],0)

if __name__=='__main__':unittest.main()
