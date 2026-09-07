"""Checks for the observed x2 packet and its independently frozen planning data."""
import collections,hashlib,json,pathlib,sys,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from ghc_family_teryn_halewick_v687_v4_core import strict_equal,strict_load
BASE=ROOT/'docs/teryn-halewick/v687-v4'
def load(rel):return strict_load(BASE/rel)

class EvidencePacket(unittest.TestCase):
    def test_complete_frozen_results(self):
        expected={x['id']:x for x in load('x1/new-proposals.json')['proposals']}
        rows=load('x2/contract-results.json');self.assertEqual(len(rows),200)
        for row in rows:
            self.assertTrue(strict_equal(row['actual'],expected[row['proposal_id']]['expected_output']))
            self.assertTrue(row['passed'] and row['input_preserved']);self.assertIsNone(row['error'])
    def test_all_changed_result_candidates_retained(self):
        expected={x['id']:x['expected_output'] for x in load('x1/new-proposals.json')['proposals']}
        rows=load('x2/mutation-results.json');self.assertEqual(len(rows),1000)
        self.assertEqual(len({x['mutation_id'] for x in rows}),1000)
        for row in rows:
            self.assertEqual(row['original_success_credit'],0)
            self.assertTrue(row['rejected'])
            self.assertFalse(strict_equal(row['invalid_candidate'],expected[row['proposal_id']]))
    def test_ledger_accounting_is_derived(self):
        index=load('x2/method-flow/index.json');ledgers=[strict_load(ROOT/r['path']) for r in index['ledgers']]
        self.assertEqual(sum(len(x['methods']) for x in ledgers),index['methods'])
        counts=collections.Counter(w['result'] for x in ledgers for w in x['witnesses'])
        self.assertEqual(counts['fail'],index['failed_witnesses']);self.assertEqual(counts['pass'],index['passing_witnesses'])
        total=load('x2/evidence-counts.json')
        for key in total['effective']:
            self.assertEqual(total['effective'][key],total['inherited_overlay'][key]+total['owner_delta'][key])
        for ledger in ledgers:
            self.assertEqual(len({w['witness_id'] for w in ledger['witnesses']}),len(ledger['witnesses']))
            self.assertTrue(all(w['same_owner_only'] and not w['independent_reproduction'] for w in ledger['witnesses']))
    def test_four_tier_graph_resolves(self):
        folder=BASE/'x2/deck/cards';cards=[strict_load(p) for p in folder.glob('*.json')];by={c['card_id']:c for c in cards}
        self.assertEqual(len(cards),210);self.assertEqual(len(by),210)
        self.assertEqual(collections.Counter(c['tier'] for c in cards),{1:1,2:3,3:6,4:200})
        for c in cards:
            if c['tier']==1:self.assertEqual(c['parent_ids'],[])
            else:
                self.assertEqual(len(c['parent_ids']),1)
                self.assertEqual(by[c['parent_ids'][0]]['tier'],c['tier']-1)
    def test_card_manifest_exact_bytes(self):
        for entry in load('x2/deck/card-manifest.json')['entries']:
            b=(ROOT/entry['path']).read_bytes()
            self.assertEqual(len(b),entry['bytes']);self.assertEqual(hashlib.sha256(b).hexdigest(),entry['sha256'])
    def test_portfolio_execution_and_reservations(self):
        r=load('x2/portfolio-execution.json')
        for key,count in [('safe',300),('candidates',250),('clean_fix_refine',300)]:
            self.assertEqual(len(r[key]),count)
            self.assertTrue(all(x['outcome']=='completed' and x['additional_independent_witness_credit']==0 for x in r[key]))
        self.assertEqual(len(r['exact_packets']),50);self.assertEqual(len(r['blocked_packets']),30)
        self.assertTrue(all(not x['executed'] for x in r['exact_packets']+r['blocked_packets']))
    def test_skills_and_interfaces_observed(self):
        rows=load('x2/skill-runner-validation.json');self.assertEqual(len(rows),10)
        self.assertTrue(all(r['frontmatter_validated'] and r['cli_result_matches'] for r in rows))
        for skill in (BASE/'skills').iterdir():
            manifest=strict_load(skill/'manifest.json')
            for e in manifest['entries']:
                b=(skill/e['path']).read_bytes();self.assertEqual(hashlib.sha256(b).hexdigest(),e['sha256'])
    def test_package_closure_and_smokes(self):
        install=load('x2/package-install.json');self.assertEqual(install['wheels_verified'],8);self.assertEqual(install['exit_code'],0)
        self.assertEqual(load('x2/package-dependency-check.json')['exit_code'],0)
        self.assertTrue(all(r['positive'] and r['adverse_rejected'] for r in load('x2/package-smokes.json')))
    def test_frozen_outcome_domain(self):
        rows=load('x2/outcome-ledger.json')
        self.assertEqual(collections.Counter(r['outcome'] for r in rows),{'completed':161,'represented':20,'open_gap':9,'exact_gate':10})
        self.assertTrue(all(r['sample_passed'] for r in rows))
    def test_document_and_file_caps(self):
        files=[p for p in BASE.rglob('*') if p.is_file()]
        self.assertLessEqual(len(files),2000)
        for p in files:
            if p.suffix in {'.json','.md','.html','.txt','.py','.lock'}:
                self.assertLessEqual(len(p.read_text(encoding='utf8').split()),100000,p.relative_to(BASE).as_posix())

if __name__=='__main__':unittest.main()
