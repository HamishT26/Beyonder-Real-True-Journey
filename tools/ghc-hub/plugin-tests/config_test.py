import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('config_menu',ROOT/'plugins/ghc-nexus-config-menu/scripts/config_menu.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)

class ConfigTests(unittest.TestCase):
    def setUp(self):
        directory=Path(os.environ.get('GHC_HUB_TEST_TMP', str(ROOT/'plugin-tests/fixtures')));directory.mkdir(parents=True,exist_ok=True)
        self.root=Path(tempfile.mkdtemp(prefix='config-',dir=directory))
        self.user=self.root/'user.toml';self.project=self.root/'project.toml'
        self.user.write_text('[tui]\nanimations=true\nalternate_screen="auto"\n',encoding='utf-8')
        self.project.write_text('[tui]\nanimations=false\n',encoding='utf-8')
        self.input={'schemaVersion':1,'layers':[{'name':'user','path':str(self.user),'active':True},{'name':'project','path':str(self.project),'active':False}]}
        self.sha=hashlib.sha256(self.user.read_bytes()).hexdigest()
    def test_selected_precedence_and_inactive_layers(self):
        self.assertEqual(c.inspect(self.input)['selectedWinners']['tui.animations']['layer'],'user')
        self.input['layers'][1]['active']=True
        self.assertEqual(c.inspect(self.input)['selectedWinners']['tui.animations']['value'],False)
    def test_secret_fields_and_invalid_values_are_not_emitted(self):
        secret='synthetic-private-marker-not-a-credential'
        self.user.write_text('api_key="'+secret+'"\nhide_agent_reasoning="'+secret+'"\n',encoding='utf-8')
        result=c.inspect(self.input)
        self.assertNotIn(secret,json.dumps(result));self.assertFalse(result['layers'][0]['values']['hide_agent_reasoning']['valid'])
    def test_proposal_preserves_sources_and_requires_private_backup(self):
        before=self.user.read_bytes()
        result=c.propose(self.input,'user',self.sha,['tui.animations=false'])
        self.assertEqual(result['status'],'ready-for-review');self.assertFalse(result['applied'])
        self.assertTrue(result['backup']['requiredBeforeWrite']);self.assertEqual(self.user.read_bytes(),before)
    def test_higher_layer_conflict(self):
        self.input['layers'][1]['active']=True
        self.assertEqual(c.propose(self.input,'user',self.sha,['tui.animations=true'])['status'],'conflict')
    def test_stale_source_hash(self):
        self.user.write_text('[tui]\nanimations=false\n',encoding='utf-8')
        self.assertEqual(c.propose(self.input,'user',self.sha,['tui.animations=true'])['reason'],'source-hash-conflict')
    def test_protected_keys_and_invalid_types_refused(self):
        for setting in ['model="x"','model_context_window=5','sandbox_mode="x"','tui.animations=1','tui.alternate_screen="other"']:
            with self.subTest(setting=setting),self.assertRaises(c.Issue):c.propose(self.input,'user',self.sha,[setting])
    def test_duplicate_keys_and_layer_paths_refused(self):
        with self.assertRaises(c.Issue):c.propose(self.input,'user',self.sha,['tui.animations=true','tui.animations=false'])
        self.input['layers'][1]['path']=str(self.user)
        with self.assertRaises(c.Issue):c.inspect(self.input)
    def test_malformed_toml_does_not_echo_source(self):
        self.user.write_text('secret="synthetic-marker\n',encoding='utf-8')
        result=c.inspect(self.input)
        self.assertEqual(result['layers'][0]['reason'],'malformed-toml');self.assertNotIn('synthetic-marker',json.dumps(result))
    def test_missing_layer_and_inactive_target_hold(self):
        self.assertEqual(c.propose(self.input,'project',hashlib.sha256(self.project.read_bytes()).hexdigest(),['tui.animations=true'])['reason'],'target-not-declared-active')
        self.input['layers'][1]['path']=str(self.root/'missing.toml')
        self.assertEqual(c.propose(self.input,'user',self.sha,['tui.animations=false'])['reason'],'selected-layer-unavailable')
    def test_hardlink_and_oversized_file_refused(self):
        os.link(self.user,self.root/'linked.toml')
        self.assertEqual(c.inspect(self.input)['layers'][0]['reason'],'unsupported-file')
        big=self.root/'large.toml';big.write_bytes(b'#'*(c.LIMIT+1))
        with self.assertRaises(c.Issue):c.read_local(str(big),'.toml')
    def test_invalid_schema_and_json_duplicate_refused(self):
        with self.assertRaises(c.Issue):c.inspect({'schemaVersion':True,'layers':self.input['layers']})
        with self.assertRaises(c.Issue):json.loads('{"a":1,"a":2}',object_pairs_hook=c.unique)

if __name__=='__main__':unittest.main(verbosity=2)
