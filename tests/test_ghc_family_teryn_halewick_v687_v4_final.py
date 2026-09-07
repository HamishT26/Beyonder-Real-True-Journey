"""Selected exact-final owner tests. The canonical runner invokes this module once."""
import collections,hashlib,importlib.metadata,json,pathlib,sys,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE=ROOT/'docs/teryn-halewick/v687-v4'
sys.path.insert(0,str(ROOT/'scripts'))
import ghc_family_teryn_halewick_v687_v4_core as core
def load(rel):return core.strict_load(BASE/rel)

class ExactFinalPacket(unittest.TestCase):
    def test_immutable_anchor_declarations(self):
        p=load('final/phase-truth.json')
        self.assertEqual(p['source'],'b3a61e3749e4302dea3bc9711eea79848f3a546b')
        self.assertEqual(p['x1'],'ebb7e751140388b81f0f9c28ff0337854a536ec5')
        self.assertEqual(p['evidence'],'238a48968af1ff0913b97f7230ec36013e939c9e')
    def test_baton_complete_binding(self):
        idx=load('handoffs/baton-index.json');data=(ROOT/idx['path']).read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(),idx['sha256'])
        self.assertEqual(len(data),idx['bytes']);self.assertEqual(len(data.decode().split()),idx['words'])
        self.assertTrue(10000<=idx['words']<=100000);self.assertEqual(len(idx['modules']),13)
        self.assertTrue(data.decode().rstrip().endswith(idx['eof']))
    def test_content_seal(self):
        for entry in load('closeout/content-seal.json')['targets']:
            data=(ROOT/entry['path']).read_bytes().replace(b'\r\n',b'\n').replace(b'\r',b'\n')
            self.assertEqual(hashlib.sha256(data).hexdigest(),entry['sha256_normalized_lf'])
    def test_observed_outcomes(self):
        p=load('final/phase-truth.json')
        self.assertEqual(p['outcomes'],dict(collections.Counter(r['outcome'] for r in load('x2/outcome-ledger.json'))))
        self.assertEqual(sum(p['outcomes'].values()),200)
    def test_failure_accounting_and_nonerasure(self):
        r=load('closeout/retained-negative-register.json')
        self.assertEqual(r['erased_negative_count'],0);self.assertEqual(r['original_failed_success_credit'],0)
        self.assertEqual(sum(x['negatives'] for x in r['groups']),1016)
        self.assertEqual(sum(x['failed'] for x in r['groups']),1016)
        self.assertEqual(sum(x['passing'] for x in r['groups'])+r['positive_contract_witnesses'],1219)
    def test_external_gates_remain_reserved(self):
        r=load('closeout/gate-register.json');self.assertEqual(r['closed_external_gates'],0)
        self.assertEqual(r['effective_open_gaps'],674+len(r['new_open_gaps']))
        self.assertEqual(r['effective_exact_gates'],659+len(r['new_exact_gates']))
    def test_no_preclaimed_route_or_canonical(self):
        p=load('final/phase-truth.json');r=load('closeout/route-readiness.json');c=load('closeout/canonical-contract.json')
        self.assertEqual((r['recipient'],r['phase']),('Caelen Ash','v687-v5'))
        self.assertEqual(r['state'],'PREPARED_NOT_SENT');self.assertEqual(r['message_count'],0)
        self.assertFalse(r['resend_allowed'] or r['create_recipient_allowed'])
        self.assertEqual(p['canonical_successes'],0);self.assertEqual(c['success_budget'],1)
        self.assertFalse(c['replay_after_success'] or c['full_repository_suite'])
    def test_current_runtime_matches_all_frozen_samples(self):
        for row in load('x1/new-proposals.json')['proposals']:
            with self.subTest(proposal=row['id']):
                self.assertTrue(core.strict_equal(core.run(row['operation'],row['input']),row['expected_output']))
    def test_changed_results_are_rejected(self):
        for row in load('x1/new-proposals.json')['proposals']:
            for changed in core.mutated_results(row['expected_output']):
                self.assertFalse(core.strict_equal(changed,row['expected_output']))
    def test_runtime_package_versions(self):
        for p in load('x1/package-plan.json')['packages']:
            self.assertEqual(importlib.metadata.version(p['name']),p['version'])
    def test_tools_and_advisory_scope(self):
        p=load('x2/promotion-receipt.json');self.assertEqual((p['skills'],p['skill_files'],p['shared_runners']),(10,60,5))
        self.assertTrue(p['source_global_byte_parity'])
        self.assertFalse(load('x2/package-advisories.json')['exhaustive_security'])
    def test_successor_ideas_and_overview(self):
        ideas=load('final/successor-ideas.json');self.assertEqual(len(ideas['skills']),10);self.assertEqual(len(ideas['runners']),10)
        self.assertTrue(all(x['credit']==0 for x in ideas['skills']+ideas['runners']))
        self.assertGreaterEqual(len((BASE/'final/integrated-overview.md').read_text(encoding='utf8').split()),1500)

if __name__=='__main__':unittest.main()
