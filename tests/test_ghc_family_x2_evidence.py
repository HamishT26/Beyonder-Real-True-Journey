"""Verify the exact x2 evidence, package target, promoted tools and deck."""
import hashlib
import json
import os
import unittest
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PHASE=ROOT/'docs/seren-talewood/v689-v2-r2'
GLOBAL=Path(os.environ['GHC_GLOBAL_TOOLS']) if 'GHC_GLOBAL_TOOLS' in os.environ else ROOT.parents[1]/'global-tools'
SITE=Path(os.environ['GHC_PACKAGE_SITE']) if 'GHC_PACKAGE_SITE' in os.environ else GLOBAL/'seren-workflow-models/python-site'
SKILLS=Path.home()/'.codex/skills'

def load(path):return json.loads(path.read_text(encoding='utf-8'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

class X2Evidence(unittest.TestCase):
    def test_all_frozen_x2_contracts_match_their_actual_observations(self):
        rows=load(PHASE/'x2/contract-results.json')['rows']
        self.assertEqual(len(rows),100)
        self.assertTrue(all(r['matched'] and r['input_unchanged'] and r['expected']==r['observed'] for r in rows))
        self.assertEqual(load(PHASE/'x2/contract-results.json')['core_sha256'],sha(ROOT/'scripts/ghc_family_model_core.py'))

    def test_candidate_repetitions_do_not_create_extra_logical_witnesses(self):
        data=load(PHASE/'x2/candidate-results.json');rows=data['rows']
        self.assertEqual((len(rows),data['fresh_logical_subjects'],data['repeated_x1_subjects']),(100,80,20))
        self.assertTrue(all(r['matched'] and r['original_success_credit']==0 and r['proposal_novelty_credit']==0 for r in rows))
        old={r['negative_id'] for r in load(PHASE/'x1/retained-negative-index.json')['rows']}
        self.assertTrue(all(r['reuses_negative_id'] in old for r in rows if r['reuses_negative_id']))

    def test_safe_and_cleanup_inventories_are_complete(self):
        summary=load(PHASE/'x2/execution-summary.json')
        self.assertEqual(len({r['task_id'] for r in summary['safe_tasks']}),120)
        self.assertTrue(all(r['outcome']=='completed' for r in summary['safe_tasks']))
        clean=load(PHASE/'x2/clean-fix-refine-results.json')['rows']
        self.assertEqual(len(clean),100)
        self.assertTrue(all(r['source_unchanged'] and r['outcome']=='completed' for r in clean))

    def test_installed_target_matches_its_full_manifest(self):
        receipt=load(PHASE/'x2/package-installation.json')
        self.assertEqual((receipt['direct_count'],receipt['closure_count'],receipt['installed_file_count']),(13,16,1321))
        actual={p.relative_to(SITE).as_posix() for p in SITE.rglob('*') if p.is_file()}
        self.assertEqual(actual,{r['path'] for r in receipt['installed_files']})
        for row in receipt['installed_files']:self.assertEqual(sha(SITE/row['path']),row['sha256'])
        self.assertFalse(receipt['host_interpreter_changed'] or receipt['executable_launchers_executed'])

    def test_package_composite_preserves_initial_success_and_scoped_api_recovery(self):
        initial=load(PHASE/'x2/package-smokes.json');current=load(PHASE/'x2/package-smokes-composite.json')
        self.assertEqual(len(initial['rows']),34);self.assertTrue(initial['all_matched'])
        self.assertEqual(len(current['rows']),34);self.assertTrue(current['composite'])
        self.assertEqual(current['current_definition_sha256'],sha(PHASE/'x2/ghc_family_package_smokes.py'))
        self.assertTrue(load(PHASE/'x2/package-api-recovery.json')['passed'])
        self.assertEqual(load(PHASE/'x2/package-api-recovery.json')['deprecated_api_warnings'],0)

    def test_promoted_x2_tools_are_exact(self):
        data=load(PHASE/'x2/tool-build-and-promotion.json')
        self.assertEqual((data['skills_built'],data['runners_built'],len(data['parity'])),(10,5,77))
        self.assertTrue(all(r['exit_code']==0 for r in data['validations']))
        for row in data['parity']:
            target=SKILLS/row['name']/row['relative_path'] if row['kind']=='skill' else GLOBAL/row['name']
            self.assertEqual(sha(ROOT/row['source_path']),row['sha256'])
            self.assertEqual(sha(target),row['sha256'])

    def test_combined_catalogue_selects_current_operations(self):
        self.assertEqual(load(PHASE/'x2/tooling/catalogue-validation.json')['card_count'],31)
        self.assertTrue(load(PHASE/'x2/tooling/catalogue-validation.json')['valid'])
        self.assertTrue(all(r['matched'] for r in load(PHASE/'x2/tooling/catalogue-queries.json')['queries']))
        for row in load(PHASE/'x2/tooling/shared-publication.json')['records']:
            if 'expected_json' in row:continue
            self.assertEqual(sha(SKILLS/row['skill']/row['relative_path']),row['sha256'])

    def test_deck_hashes_parents_and_logical_coverage_are_exact(self):
        deck=PHASE/'x2/deck';index=load(deck/'deck-index.json')
        self.assertEqual((index['card_count'],index['tier_counts']),(697,[1,3,4,689]))
        mapping={}
        for cid in index['card_order']:
            card=load(deck/'cards'/(cid+'.json'));payload={k:v for k,v in card.items() if k!='card_id'}
            expected='ghc-card-'+hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()
            self.assertEqual(cid,expected);mapping[cid]=card
        for card in mapping.values():
            if card['tier']==1:self.assertEqual(card['parent_ids'],[])
            else:
                self.assertEqual(len(card['parent_ids']),1)
                self.assertEqual(mapping[card['parent_ids'][0]]['tier'],card['tier']-1)
        self.assertEqual(len(index['logical_index']),689)
        self.assertEqual(sum(k.startswith('ST6892R2-N') for k in index['logical_index']),200)

    def test_deck_manifest_binds_every_card_and_index(self):
        deck=PHASE/'x2/deck';manifest=load(deck/'card-manifest.json')
        actual={p.relative_to(ROOT).as_posix() for p in deck.rglob('*') if p.is_file()}
        self.assertEqual(actual,{r['path'] for r in manifest['files']}|set(manifest['self_exclusions']))
        for row in manifest['files']:self.assertEqual(sha(ROOT/row['path']),row['sha256'])

    def test_integer_witnesses_have_zero_exact_residual_without_a_universal_claim(self):
        data=load(PHASE/'x2/mathematical-experiments.json')
        self.assertEqual([r['n'] for r in data['egyptian_witnesses']],list(range(2,102)))
        for row in data['egyptian_witnesses']:
            self.assertEqual(sum(Fraction(1,d) for d in row['denominators']),Fraction(4,row['n']))
        self.assertFalse(data['universal_conjecture_proved'] or data['new_fundamental_law_established'])
        self.assertTrue(data['coarse_graining_counterexample']['disagree'])
        self.assertLess(float(data['entropy_counterexample']['entropy_after']),float(data['entropy_counterexample']['entropy_before']))

    def test_method_counts_and_retained_subjects_match(self):
        ledger=load(PHASE/'x2/method-flow.json')
        self.assertEqual((len(ledger['methods']),len(ledger['witnesses'])),(34,396))
        self.assertEqual(sum(w['result']=='fail' for w in ledger['witnesses']),153)
        self.assertEqual(sum(w['result']=='pass' for w in ledger['witnesses']),243)
        self.assertTrue(load(PHASE/'x2/method-validation.json')['valid'])

    def test_successor_and_terminal_work_remain_separate(self):
        ideas=load(PHASE/'x2/successor-ideas.json')
        self.assertEqual((len(ideas['skill_ideas']),len(ideas['runner_ideas'])),(5,5))
        summary=load(PHASE/'x2/execution-summary.json')
        self.assertEqual(summary['total_exact_packet_completions_in_x2'],28)
        self.assertEqual(summary['canonical_invocations'],0);self.assertEqual(summary['successor_messages'],0)

if __name__=='__main__':unittest.main()
