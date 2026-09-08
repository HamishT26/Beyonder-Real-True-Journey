"""Final artifact and canonical-fixture checks; never invoke the canonical here."""
import hashlib
import importlib.util
import json
import os
import tempfile
import unittest
import uuid
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PHASE=ROOT/'docs/seren-talewood/v689-v2-r2'
spec=importlib.util.spec_from_file_location('canonical_fixture_functions',PHASE/'final/ghc_family_canonical.py')
canonical=importlib.util.module_from_spec(spec);spec.loader.exec_module(canonical)

def load(path):return canonical.strict_json(path.read_bytes())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

class FinalContract(unittest.TestCase):
    def test_manifest_lifecycle_json_and_exclusive_write_fixtures(self):
        base=Path(os.environ['GHC_FIXTURE_ROOT']);base.mkdir(exist_ok=True,parents=True)
        directory=Path(tempfile.mkdtemp(prefix='final-fixture-',dir=base))
        self.assertTrue(directory.resolve().is_relative_to(base.resolve()))
        result=canonical.fixture_observations(directory)
        self.assertTrue(result['valid_manifest'])
        self.assertEqual(len(result['negative_fixtures']),8)
        self.assertTrue(all(r['rejected'] and r['original_success_credit']==0 for r in result['negative_fixtures']))
        self.assertEqual(result['canonical_invocations'],0)

    def test_typed_equality_does_not_collapse_booleans_or_numeric_types(self):
        self.assertFalse(canonical.typed_equal(True,1))
        self.assertFalse(canonical.typed_equal(1,1.0))
        self.assertTrue(canonical.typed_equal({'b':[1],'a':False},{'a':False,'b':[1]}))

    def test_final_count_reconciliation_preserves_source_and_owner(self):
        counts=load(PHASE/'final/count-reconciliation.json')
        self.assertEqual(counts['owner_delta']['proposals'],200)
        self.assertEqual(counts['owner_delta']['methods'],70)
        self.assertEqual(counts['owner_delta']['negatives'],239)
        self.assertEqual(counts['owner_delta']['failed_witnesses'],239)
        self.assertEqual(counts['owner_delta']['passing_witnesses'],393)
        self.assertEqual(counts['source_repository_seal']['proposals'],17430)
        self.assertEqual(counts['represented_chain_after']['proposals'],17630)
        for key in ['proposals','methods','negatives','failed_witnesses','passing_witnesses']:
            self.assertEqual(counts['source_repository_seal'][key]+counts['owner_delta'][key],counts['represented_chain_after'][key])
        self.assertFalse(counts['aggregate_mapping_complete'])

    def test_final_checklist_resolves_all_owner_execution_tranches(self):
        checklist=load(PHASE/'final/checklist.json')
        completed={r['item']:r['count'] for r in checklist['items'] if r['outcome']=='completed'}
        self.assertEqual(completed['new bounded contracts'],200)
        self.assertEqual(completed['x1 safe tasks'],121)
        self.assertEqual(completed['x2 safe tasks'],120)
        self.assertEqual(completed['candidate field-closure reviews'],100)
        self.assertEqual(completed['source record refinements'],200)
        self.assertEqual(completed['authorized exact packet actions'],49)
        self.assertEqual(checklist['unexecuted_blocked_packets'],30)

    def test_baton_has_thirteen_modules_and_the_required_word_budget(self):
        baton=(PHASE/'final/hand-off-baton.md').read_text(encoding='utf-8')
        self.assertGreaterEqual(len(baton.split()),10000)
        self.assertLessEqual(len(baton.split()),100000)
        self.assertEqual(sum(line.startswith('## Module ') for line in baton.splitlines()),13)
        self.assertTrue(baton.rstrip().endswith('EOF SEREN TALEWOOD v689-v2-r2 BATON.'))
        self.assertIn('Eiren Kestrel v689-v3',baton)
        self.assertIn('Rowan Ash v689-v4',baton)

    def test_current_release_preserves_the_old_hold_as_history(self):
        truth=load(PHASE/'final/phase-truth.json')
        self.assertTrue(truth['successor_activation_authorized'])
        self.assertEqual(truth['successor'],'Eiren Kestrel')
        self.assertEqual(truth['successor_phase'],'v689-v3')
        self.assertTrue(truth['old_seren_hold_preserved'])
        self.assertEqual(truth['source'],'7034e1721b29bd46e10e2a467e79a114f31b5885')
        self.assertEqual(truth['canonical_at_repository_seal'],'prepared_not_invoked')
        self.assertEqual(truth['successor_messages_at_repository_seal'],0)

    def test_canonical_policy_binds_each_lifecycle_definition(self):
        policy=load(PHASE/'final/canonical-policy.json')
        self.assertEqual([r['name'] for r in policy['stages']],['plan','x1','x2','final'])
        self.assertEqual([sum(m['test_count'] for m in r['test_modules']) for r in policy['stages']],[12,31,35,12])
        self.assertEqual(policy['canonical_code_sha256'],sha(PHASE/'final/ghc_family_canonical.py'))
        self.assertEqual(policy['canonical_invocations'],1)
        self.assertFalse(policy['replay_authorized'] or policy['source_execution'])

    def test_combined_deck_includes_new_final_cards_without_rewriting_x2(self):
        index=load(PHASE/'final/deck-extension.json')
        self.assertEqual((index['base_cards'],index['new_cards'],index['total_cards']),(698,2,700))
        for entry in index['cards']:
            card=load(ROOT/entry['path']);payload={k:v for k,v in card.items() if k!='card_id'}
            expected='ghc-card-'+hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()
            self.assertEqual(card['card_id'],expected)
            self.assertEqual(card['tier'],4)
        self.assertTrue(index['prior_deck_unchanged'])

    def test_final_content_seal_covers_all_owner_files(self):
        seal=load(PHASE/'final/content-seal.json')
        objects={p.relative_to(ROOT).as_posix():{'raw':p.read_bytes(),'oid':None} for p in ROOT.rglob('*') if p.is_file() and p.name!='.git' and '__pycache__' not in p.parts}
        pending={str((PHASE/'final'/name).relative_to(ROOT)).replace('\\','/') for name in ['manifest.json','staged-review.json']}-set(objects)
        self.assertLessEqual(pending,set(seal['self_exclusions']))
        canonical.verify_manifest(seal,objects,set(objects)|pending)

    def test_overview_has_three_explicit_print_sections_and_real_figure(self):
        text=(PHASE/'final/overview.html').read_text(encoding='utf-8')
        self.assertEqual(text.count('class="page"'),3)
        self.assertIn('break-after:page',text)
        self.assertIn('probability-and-entropy.png',text)
        self.assertTrue((PHASE/'x2/figures/probability-and-entropy.png').is_file())

    def test_privacy_definitions_detect_each_constructed_fixture(self):
        fixtures={
          'credential':'sk'+'-'+'a'*32,
          'private_absolute_path':chr(67)+':'+chr(92)+'Users'+chr(92)+'example',
          'private_key':'-----BEGIN '+'PRIVATE KEY-----',
          'private_route':'app'+':/'+'/example',
          'raw_uuid':str(uuid.UUID(int=1))}
        self.assertTrue(all(canonical.PATTERNS[k].search(v) for k,v in fixtures.items()))
        self.assertFalse(canonical.PATTERNS['credential'].search('native-task-management-tools-not-exposed'))

    def test_final_fixture_results_preserve_all_failed_subjects(self):
        data=load(PHASE/'final/canonical-fixture-results.json')
        self.assertEqual(len(data['negative_fixtures']),8)
        self.assertTrue(all(r['subject_result']=='fail' and r['original_success_credit']==0 for r in data['negative_fixtures']))
        self.assertEqual(data['canonical_invocations'],0)
        self.assertEqual(load(PHASE/'final/phase-truth.json')['terminal_verdict'],'NOT_READY_FOR_STAGE_20')

if __name__=='__main__':unittest.main()
