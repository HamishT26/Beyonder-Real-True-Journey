"""Final artifact gates; behavior is included only in the exact-final aggregate."""
import argparse,hashlib,json,re,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(ROOT/'tests'))
import ghc_family_ilyan_reed_v685_v8_validation as v
from pypdf import PdfReader
class FinalArtifacts(unittest.TestCase):
    def test_source_x1_evidence_direct_edges(self):
        p=v.read('final/validation-policy.json')
        self.assertEqual(v.git('rev-parse',p['x1']+'^').decode().strip(),p['source'])
        self.assertEqual(v.git('rev-parse',p['evidence']+'^').decode().strip(),p['x1'])
        self.assertEqual(p['expected_history_commits'],3)
    def test_immutable_x1_exact_files(self):
        paths=v.read('validation/x1-allowlist.json')['paths'];blobs=v.blob_batch([v.X1+':'+p for p in paths]);self.assertTrue(all((ROOT/p).read_bytes()==b for p,b in zip(paths,blobs)))
    def test_immutable_evidence_exact_files(self):
        paths=v.read('validation/evidence-allowlist.json')['paths'];e=v.read('final/validation-policy.json')['evidence'];blobs=v.blob_batch([e+':'+p for p in paths]);self.assertTrue(all((ROOT/p).read_bytes()==b for p,b in zip(paths,blobs)))
    def test_baton_word_count_and_content_digest(self):
        b=(v.BASE/'final/neris-v686-v1-baton.md').read_bytes();t=b.decode();r=v.read('final/baton-integrity.json');self.assertEqual(len(t.split()),r['words']);self.assertTrue(10000<=r['words']<=100000);self.assertEqual(len(re.findall(r'^# \d{2} ',t,re.M)),13);self.assertEqual(v.digest(b),r['sha256'])
    def test_overview_is_at_least_three_actual_pages(self):
        p=v.BASE/'final/integrated-overview.pdf';r=PdfReader(p);receipt=v.read('final/overview-pdf-validation.json');self.assertGreaterEqual(len(r.pages),3);self.assertEqual(len(r.pages),receipt['pages']);self.assertTrue(all(len(page.extract_text())>1500 for page in r.pages));self.assertEqual(v.digest(p.read_bytes()),receipt['sha256'])
    def test_distinct_source_truth_layers(self):
        p=v.read('final/phase-truth.json');self.assertEqual(p['source_repository_seal']['effective_negatives'],64405);self.assertEqual(p['source_initial_activation_baseline']['effective_negatives'],64410);self.assertEqual(p['source_later_external_baseline']['effective_negatives'],64412)
    def test_claim_and_task_count_domains(self):
        p=v.read('final/phase-truth.json');self.assertEqual(p['outcomes'],{'completed':170,'represented':10,'open_gap':10,'exact_gate':10});self.assertEqual(p['declared_proposal_chain'],12230);self.assertEqual(p['real_entities'],0)
    def test_package_transaction_has_three_direct_additions(self):
        p=v.read('x1/package-plan.json');self.assertEqual(sum(x['category']=='direct' for x in p['packages']),3);self.assertEqual(v.read('x2/toolchain/package-smokes.json')['positive_passes'],3);self.assertEqual(v.read('x2/toolchain/package-smokes.json')['adverse_passes'],3);self.assertEqual(v.read('x2/toolchain/advisory-audit.json')['finding_rows'],0)
    def test_global_promotion_counts_have_no_copy_inflation(self):
        p=v.read('x2/global-promotion-installation.json');self.assertEqual(p['installed_count'],10);self.assertEqual(p['unique_shared_runners'],5);self.assertTrue(all(x['byte_parity'] and x['post_copy_validation']['valid'] for x in p['skills']))
    def test_deck_has_four_lenses_in_six_contexts(self):
        p=v.read('x2/flashcards/deck-index.json');self.assertEqual(p['card_count'],210);self.assertEqual(p['unique_practice_lenses'],4);self.assertEqual(p['practice_placements'],6);self.assertTrue(v.deck_check()['valid'])
    def test_method_flow_and_totals_are_explicit(self):
        self.assertTrue(v.method_check()['valid']);self.assertEqual(v.read('final/phase-truth.json')['totals'],{'bounded_passing_witnesses':63909,'effective_methods':82064,'effective_negatives':65519,'exact_gates':579,'failed_witnesses':36367,'open_gaps':592})
    def test_route_is_prepared_and_projection_is_planning(self):
        d=v.read('final/delivery-state.json');self.assertEqual((d['state'],d['recipient'],d['phase'],d['send_count']),('PREPARED_NOT_SENT','Neris Solane','v686-v1',0));schedule=v.read('x2/route-projection.json')['assignments'];self.assertEqual(len(schedule),321);self.assertEqual(schedule[-1]['phase'],'v725-v8');self.assertTrue(all(x['planning_only'] and not x['executed_by_projection'] for x in schedule))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--include-behavior',action='store_true');a=ap.parse_args();loader=unittest.TestLoader();suite=loader.loadTestsFromTestCase(FinalArtifacts)
    if a.include_behavior:
        from test_ghc_family_ilyan_reed_v685_v8_x2 import ProtocolBehavior
        suite.addTests(loader.loadTestsFromTestCase(ProtocolBehavior))
    r=unittest.TextTestRunner(stream=sys.stderr,verbosity=1).run(suite);print(json.dumps({'tests_run':r.testsRun,'failures':len(r.failures),'errors':len(r.errors),'passed':r.wasSuccessful()}));raise SystemExit(0 if r.wasSuccessful() else 1)
if __name__=='__main__':main()
