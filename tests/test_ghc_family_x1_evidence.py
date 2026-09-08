"""Close the x1 evidence boundary against actual retained records and installations."""
import hashlib
import json
import os
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REL=ROOT/'docs/seren-talewood/v689-v2-r2'
SKILLS=Path.home()/'.codex/skills'
GLOBAL=Path(os.environ['GHC_GLOBAL_TOOLS']) if 'GHC_GLOBAL_TOOLS' in os.environ else ROOT.parents[1]/'global-tools'

def load(path):return json.loads(path.read_text(encoding='utf-8'))
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

class X1Evidence(unittest.TestCase):
    def test_every_defined_safe_task_has_attributable_evidence(self):
        core=load(REL/'x1/contract-results.json')['rows']
        reused=load(REL/'x1/reuse-existing-tools-results.json')['observations']
        controls=load(REL/'x1/spontaneous-safety-plan.json')['tasks']
        extra=load(REL/'x1/profile-review-plan.json')
        ids={f'ST6892R2-X1-SAFE-{i:03}' for i in range(1,101)}
        ids|={r['task_id'] for r in reused}|{r['task_id'] for r in controls}|{extra['task_id']}
        self.assertEqual(len(ids),121)
        self.assertEqual(len(core),100)
        self.assertTrue(all(r['matched'] and r['input_unchanged'] for r in core+reused))
        self.assertTrue(load(REL/'x1/profile-review-results.json')['valid_profile']['valid'])

    def test_cleanup_targets_preserve_every_selected_source(self):
        planned={r['task_id']:r for r in load(REL/'plan/approval-portfolio.json')['clean_fix_refine'] if r['stage']=='x1'}
        rows=load(REL/'x1/clean-fix-refine-results.json')['rows']
        selected={r['selection_id']:r for r in load(REL/'plan/inherited-selections.json')['selections']}
        self.assertEqual({r['task_id'] for r in rows},set(planned))
        for row in rows:
            original=selected[row['selection_id']]
            self.assertEqual(row['artifact']['original_input'],original['original_input'])
            self.assertEqual(row['artifact']['original_expected'],original['original_expected'])
            self.assertEqual(row['artifact']['retained_gates'],original['original_protected_gates'])
            self.assertTrue(row['source_unchanged'])

    def test_new_global_capabilities_match_the_reviewed_owner_files(self):
        receipt=load(REL/'x1/tool-build-and-promotion.json')
        self.assertEqual((receipt['skills_built'],receipt['runners_built']),(10,5))
        self.assertEqual(len(receipt['parity']),66)
        self.assertTrue(all(r['exit_code']==0 for r in receipt['validations']))
        for row in receipt['parity']:
            source=ROOT/row['source_path']
            target=SKILLS/row['name']/row['relative_path'] if row['kind']=='skill' else GLOBAL/row['name']
            self.assertEqual(digest(source),row['sha256'])
            self.assertEqual(digest(target),row['sha256'])

    def test_shared_entrypoints_preserve_their_archives(self):
        receipt=load(REL/'x1/shared-integration-receipt.json')
        self.assertEqual(receipt['entrypoints_updated'],27)
        for row in receipt['records']:
            if row['kind']=='global_runner':
                self.assertEqual(digest(GLOBAL/row['name']),row['after_sha256'])
                continue
            base=SKILLS/row['skill']
            self.assertEqual(digest(base/row['relative_path']),row['after_sha256'])
            self.assertEqual(digest(ROOT/row['source_path']),row['after_sha256'])
            if row['kind']=='entrypoint':self.assertEqual(digest(base/row['preserved_archive']),row['before_sha256'])
        self.assertLess(receipt['entrypoint_words_after'],receipt['entrypoint_words_before'])
        self.assertFalse(receipt['cache_or_retention_improvement_claimed'])

    def test_current_catalogue_query_correction_is_preserved_and_published(self):
        correction=load(REL/'tooling/shared-catalogue-token-correction.json')
        self.assertTrue(correction['original_preserved'])
        self.assertTrue(all(q['matched'] for q in correction['queries']))
        for row in correction['records']:
            if 'expected_json' in row:
                continue
            target=SKILLS/row['skill']/row['relative_path']
            self.assertEqual(digest(target),row['sha256'])
        for row in load(REL/'x1/shared-pointer-snapshot.json')['rows']:
            self.assertEqual(digest(SKILLS/row['skill']/row['relative_path']),row['sha256'])
        self.assertEqual(load(REL/'tooling/catalogue-v2-validation.json')['card_count'],16)
        self.assertEqual(load(REL/'tooling/catalogue-v2-collision-review.json')['unresolved'],0)

    def test_all_method_witnesses_and_failures_remain_distinct(self):
        ledgers=[load(REL/'x1/method-flow.json'),load(REL/'x1/catalogue-method-addendum.json')]
        methods=[r for ledger in ledgers for r in ledger['methods']]
        witnesses=[r for ledger in ledgers for r in ledger['witnesses']]
        self.assertEqual(len({r['method_id'] for r in methods}),34)
        self.assertEqual(len({r['witness_id'] for r in witnesses}),217)
        self.assertEqual(sum(r['result']=='fail' for r in witnesses),77)
        self.assertEqual(sum(r['result']=='pass' for r in witnesses),140)
        self.assertTrue(all(r['independent_reproduction'] is False for r in witnesses))
        self.assertTrue(load(REL/'x1/method-validation.json')['valid'])
        self.assertTrue(load(REL/'x1/catalogue-method-validation.json')['valid'])

    def test_x2_and_external_actions_are_not_preclaimed(self):
        summary=load(REL/'x1/execution-summary.json')
        self.assertEqual(summary['packages_installed'],0)
        self.assertEqual(summary['candidate_tasks_remaining_for_x2'],100)
        self.assertEqual(summary['canonical_invocations'],0)
        self.assertEqual(summary['successor_messages'],0)
        self.assertFalse((REL/'x2/contract-results.json').exists())

if __name__=='__main__':unittest.main()
