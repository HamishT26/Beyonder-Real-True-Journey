"""Behavioral witnesses for the frozen Rowan Ash capsule acceptance conditions."""
import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("capsule", REPO / "scripts/ghc_family_evidence_capsule.py")
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
REJECTIONS = []
FIXTURE_ROOT = None


def binding():
    a = dict(owner="Synthetic owner", source="1"*40, x1="2"*40,
             evidence="3"*40, final="4"*40)
    p = "docs/example/v1-v1"
    return dict(**a, parents={a["x1"]:[a["source"]], a["evidence"]:[a["x1"]],
                              a["final"]:[a["evidence"]]},
                scope_prefix=p, planning_paths=[p+"/x1/plan.json"],
                planning_maps={k:{p+"/x1/plan.json":"abc"} for k in ("x1","evidence","final")},
                delta_paths=[p+"/x1/plan.json", p+"/x2/result.json"],
                extra_allowed_paths=[], unchanged_history_scan=False)


def credit():
    return dict(outcome="completed", inherited=False, novelty_credit=1,
                completion_credit=1, independent_reproduction=False, closed_gates=[],
                aggregate_state="invalid", aggregate_success_credit=0)


def ledger():
    n = dict(negative_id="n1", success_credit=0, description="retained failure")
    wf = dict(witness_id="w1", result="fail", retained_negative_ids=["n1"],
              independent_reproduction=False)
    wp = dict(witness_id="w2", result="pass", retained_negative_ids=["n1"],
              independent_reproduction=False)
    return dict(negatives=[n], witnesses=[wf,wp],
                methods=[dict(method_id="m1", state="preferred", witness_ids=["w1","w2"])],
                previous=dict(negatives=[copy.deepcopy(n)]))


def deck():
    cards=[]
    for i in range(4):
        cards.append(dict(card_id=f"card{i+1}",tier=i+1,
                          parent_ids=[] if i==0 else [f"card{i}"],
                          stability="stable" if i<2 else "volatile",
                          outcome="represented"))
    return dict(cards=cards, stable_prefix=["card1","card2"],
                volatile_index=["card3","card4"],sections=list(c.SECTIONS))


def reservations():
    return dict(rows=[dict(title=f"Reservation {i+1}",
                          outcome="open_gap" if i<3 else "exact_gate",
                          executed=False,closed=False) for i in range(6)])


def report():
    return dict(rows=[dict(title="Example evidence",outcome="represented",detail="Synthetic")],
                links=[dict(path="evidence.json#row1",label="Evidence")])


class CapsuleTests(unittest.TestCase):
    def reject(self, fn, *args, **kwargs):
        with self.assertRaises(c.CapsuleError) as ctx:
            fn(*args, **kwargs)
        REJECTIONS.append(dict(proposal_id="RA6856-N"+self._testMethodName.split("_")[1],
                               code=str(ctx.exception),failed_fixture_credit=0,
                               validator_rejection_pass=True))

    def scratch(self):
        self.assertIsNotNone(FIXTURE_ROOT)
        path=Path(tempfile.mkdtemp(prefix="capsule-",dir=FIXTURE_ROOT)).resolve()
        self.assertTrue(path.is_relative_to(FIXTURE_ROOT.resolve()))
        return path

    def test_001_raw_binary(self):
        raw=b"\x00\xff\r\n"
        self.assertEqual(c.digest_stream([raw],"raw_bytes_v1")["sha256"],hashlib.sha256(raw).hexdigest())
        self.reject(c.digest_stream,["text"],"raw_bytes_v1")

    def test_002_git_blob_domain(self):
        raw=b"one\r\ntwo\n"
        a=c.digest_stream([raw],"raw_git_blob_v1")
        self.assertEqual(a["bytes"],len(raw))
        self.assertNotEqual(a["sha256"],hashlib.sha256(raw.replace(b"\r\n",b"\n")).hexdigest())
        self.reject(c.digest_stream,[raw],"checkout_guessed")

    def test_003_text_normalization(self):
        raw=b"a\r\nb\rc  "
        expected=b"a\nb\rc  "
        self.assertEqual(b"".join(c.normalized_chunks([raw],"utf8_crlf_to_lf_v1")),expected)
        self.reject(c.digest_stream,[b"\xff"],"utf8_crlf_to_lf_v1")

    def test_004_invalid_utf8(self):
        for raw in (b"\xff",b"\xc0\xaf",b"\xed\xa0\x80",b"\xe2\x82"):
            self.reject(c.digest_stream,[raw],"utf8_crlf_to_lf_v1")
            self.assertEqual(c.digest_stream([raw],"raw_bytes_v1")["bytes"],len(raw))

    def test_005_domain_closed_set(self):
        for domain in ("utf8",None,"","normalized"):
            self.reject(c.digest_stream,[b""],domain)
        self.assertEqual(c.digest_stream([],"raw_bytes_v1")["sha256"],
                         "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")

    def test_006_chunk_partitions(self):
        raw="A\r\nMāori\rZ\r".encode()
        expected=hashlib.sha256(raw.replace(b"\r\n",b"\n")).hexdigest()
        for split in range(len(raw)+1):
            for second in range(split,len(raw)+1):
                self.assertEqual(c.digest_stream([raw[:split],raw[split:second],raw[second:]],
                                  "utf8_crlf_to_lf_v1")["sha256"],expected)
        self.reject(c.digest_stream,[b"\xe2",b"\x28"],"utf8_crlf_to_lf_v1")

    def test_007_unicode_paths(self):
        self.assertEqual(c.portable_path("docs/Māori/data.json"),"docs/Māori/data.json")
        self.reject(c.portable_path,"docs/Cafe\u0301/data.json")

    def test_008_dot_segments(self):
        for p in ("../x","a/../b","./x","a//b","a/.",""):
            self.reject(c.portable_path,p)
        self.assertEqual(c.portable_path("a/b.json"),"a/b.json")

    def test_009_absolute_paths(self):
        for p in ("/root/file","C:file","C:/file","//server/share","a/file:stream"):
            self.reject(c.portable_path,p)
        self.assertEqual(c.portable_path("root/file"),"root/file")

    def test_010_backslashes(self):
        self.reject(c.portable_path,r"a\b")
        self.assertEqual(c.portable_path("a/b"),"a/b")

    def test_011_path_controls(self):
        for ch in ("\x00","\n","\r","\t","\x7f"):
            self.reject(c.portable_path,"a/"+ch+"b")
        self.assertEqual(c.portable_path("a/space name"),"a/space name")

    def test_012_windows_aliases(self):
        for p in ("a/CON","a/Nul.txt","a/LPT1.csv","a/b.","a/b "):
            self.reject(c.portable_path,p)
        self.reject(c.path_set,["a/File","a/file"])
        self.assertEqual(c.path_set(["a/com10","a/normal.txt"]),{"a/com10","a/normal.txt"})

    def test_012_git_pathspec_chars(self):
        self.assertEqual(c.portable_path("a/literal.json"), "a/literal.json")
        for ch in '*?[]<>"|':
            self.reject(c.portable_path, "a/" + ch + ".json")

    def manifest(self):
        p={"a.txt":b"a\n","b.bin":b"\x00\xff"}
        return p,c.manifest_for(p)

    def test_013_manifest_order(self):
        p,m=self.manifest()
        self.assertEqual([e["path"] for e in m["entries"]],["a.txt","b.bin"])
        self.assertTrue(c.verify_manifest(m,p,list(p))["valid"])
        m["entries"].reverse();self.reject(c.verify_manifest,m,p,list(p))

    def test_014_exact_target_set(self):
        p,m=self.manifest()
        c.verify_manifest(m,p,list(p))
        self.reject(c.verify_manifest,m,p,["a.txt"])
        m["entries"].append(copy.deepcopy(m["entries"][0]));m["entry_count"]+=1
        self.reject(c.verify_manifest,m,p,list(p))

    def test_015_exact_digest(self):
        p,m=self.manifest()
        self.assertEqual(m["entries"][0]["sha256"],hashlib.sha256(b"a\n").hexdigest())
        for key,value in (("sha256","0"*64),("bytes",99),("bytes",True),("sha256","Z"*64)):
            bad=copy.deepcopy(m);bad["entries"][0][key]=value
            self.reject(c.verify_manifest,bad,p,list(p))
        c.verify_manifest(m,p,list(p))

    def test_016_file_modes(self):
        p,m=self.manifest();m["entries"][0]["mode"]="100755"
        c.verify_manifest(m,p,list(p))
        for mode in ("120000","160000","100600"):
            bad=copy.deepcopy(m);bad["entries"][0]["mode"]=mode
            self.reject(c.verify_manifest,bad,p,list(p))

    def test_017_self_exclusions(self):
        p,m=self.manifest();m["declared_self_exclusions"]=["manifest.json"]
        c.verify_manifest(m,p,list(p)+["manifest.json"],["manifest.json"])
        self.reject(c.verify_manifest,m,p,list(p)+["manifest.json"],[])
        m["declared_self_exclusions"]=["a.txt"]
        self.reject(c.verify_manifest,m,p,list(p),["a.txt"])

    def test_018_file_ceiling(self):
        self.assertEqual(len(c.path_set(["a"])),1)
        self.reject(c.path_set,[str(i) for i in range(2001)])
        self.reject(c.path_set,["a"],True)

    def test_019_full_anchors(self):
        c.validate_bindings(binding())
        for commit in ("abcd","G"*40,None,"1"*39):
            b=binding();b["source"]=commit;self.reject(c.validate_bindings,b)

    def test_019_malformed_cli_envelope(self):
        path = self.scratch() / "malformed.json"
        value = binding()
        value["parents"] = []
        path.write_bytes(c.json_bytes(value))
        run = subprocess.run([sys.executable, "-B", str(REPO / "scripts/ghc_family_evidence_capsule.py"),
                              "check", "--group", "bindings", "--input", str(path)], capture_output=True)
        self.assertEqual(run.returncode, 2)
        self.assertEqual(run.stderr, b"")
        parsed = c.strict_json(run.stdout)
        self.assertFalse(parsed["valid"])
        self.assertEqual(parsed["error"], "AttributeError")
        REJECTIONS.append(dict(proposal_id="RA6856-N019", code="malformed_cli_envelope",
                               failed_fixture_credit=0, validator_rejection_pass=True))

    def test_020_direct_parents(self):
        c.validate_bindings(binding())
        b=binding();b["parents"][b["evidence"]]=[b["source"],b["x1"]]
        self.reject(c.validate_bindings,b)
        b=binding();b["parents"][b["final"]]=[b["x1"]]
        self.reject(c.validate_bindings,b)

    def test_021_x1_planning_only(self):
        c.validate_bindings(binding())
        b=binding();b["planning_paths"]=["docs/example/v1-v1/x2/result.json"]
        self.reject(c.validate_bindings,b)

    def test_022_planning_immutable(self):
        c.validate_bindings(binding())
        b=binding();b["planning_maps"]["final"]["docs/example/v1-v1/x1/plan.json"]="changed"
        self.reject(c.validate_bindings,b)

    def test_023_owner_prefix(self):
        c.validate_bindings(binding())
        b=binding();b["delta_paths"].append("docs/example/v1-v10/stolen.json")
        self.reject(c.validate_bindings,b)

    def test_024_delta_scope(self):
        b=binding();b["extra_allowed_paths"]=["scripts/owned.py"];b["delta_paths"].append("scripts/owned.py")
        c.validate_bindings(b)
        b["unchanged_history_scan"]=True;self.reject(c.validate_bindings,b)

    def test_025_outcome_labels(self):
        for label in c.OUTCOMES:
            v=credit();v["outcome"]=label;v["completion_credit"]=int(label=="completed")
            c.validate_credit(v)
        v=credit();v["outcome"]="proof";self.reject(c.validate_credit,v)

    def test_026_inherited_credit(self):
        v=credit();v.update(inherited=True,novelty_credit=0,completion_credit=0)
        c.validate_credit(v)
        v["novelty_credit"]=1;self.reject(c.validate_credit,v)

    def test_027_failed_aggregate(self):
        c.validate_credit(credit())
        v=credit();v["aggregate_success_credit"]=1;self.reject(c.validate_credit,v)

    def test_028_dependency_recovery(self):
        v=credit();v["recovery_of"]=dict(state="invalid",success_credit=0,negative_id="failure1")
        c.validate_credit(v)
        v["recovery_of"]["state"]="valid";self.reject(c.validate_credit,v)

    def test_029_independence(self):
        c.validate_credit(credit())
        v=credit();v["independent_reproduction"]=True;self.reject(c.validate_credit,v)

    def test_030_protected_gates(self):
        c.validate_credit(credit())
        v=credit();v["closed_gates"]=["Stage 20"];self.reject(c.validate_credit,v)

    def test_031_unique_negatives(self):
        c.validate_ledger(ledger())
        v=ledger();v["negatives"].append(copy.deepcopy(v["negatives"][0]))
        self.reject(c.validate_ledger,v)

    def test_032_recovery_links(self):
        c.validate_ledger(ledger())
        v=ledger();v["witnesses"][1]["retained_negative_ids"]=["missing"]
        self.reject(c.validate_ledger,v)

    def test_033_append_only(self):
        c.validate_ledger(ledger())
        v=ledger();v["negatives"]=[];self.reject(c.validate_ledger,v)

    def test_034_correction_preservation(self):
        v=ledger();v["negatives"].append(dict(negative_id="n2",success_credit=0,corrects="n1"))
        c.validate_ledger(v)
        v["negatives"][0]["description"]="rewritten";self.reject(c.validate_ledger,v)

    def test_035_promotion_gate(self):
        c.validate_ledger(ledger())
        v=ledger();v["methods"][0]["witness_ids"]=["w1"];self.reject(c.validate_ledger,v)

    def test_036_derived_counts(self):
        v=ledger();v["counts"]=dict(negatives=1,failed_witnesses=1,passing_witnesses=1)
        self.assertEqual(c.validate_ledger(v)["negatives"],1)
        v["counts"]["negatives"]=2;self.reject(c.validate_ledger,v)

    def test_037_exclusive_reservation(self):
        p=self.scratch()/"reservation.json";c.reserve_canonical(p,binding())
        before=p.read_bytes();self.reject(c.reserve_canonical,p,binding())
        self.assertEqual(p.read_bytes(),before)

    def test_038_anchor_binding(self):
        p=self.scratch()/"reservation.json"
        v=c.reserve_canonical(p,binding());self.assertEqual(v["anchors"]["final"],"4"*40)
        bad=binding();bad.pop("owner");self.reject(c.reserve_canonical,p.with_name("bad.json"),bad)

    def test_039_incomplete_credit(self):
        v=dict(anchors=binding(),canonical_invocations=1,replay_count=0,complete=False,
               checks={"partial":True},success_credit=0,independent_reproduction=False)
        c.validate_latch(v);v["success_credit"]=1;self.reject(c.validate_latch,v)
        v["success_credit"]=0;v["complete"]=1;self.reject(c.validate_latch,v)

    def test_040_finalization_preserves(self):
        p=self.scratch()/"reservation.json";c.reserve_canonical(p,binding());before=p.read_bytes()
        r=c.finalize_canonical(p,{"one":False,"two":True})
        self.assertFalse(r["valid"]);self.assertEqual(r["canonical_success_credit"],0)
        self.assertEqual(p.read_bytes(),before);self.reject(c.finalize_canonical,p,{"one":True})

    def test_041_named_checks(self):
        p=self.scratch()/"reservation.json";c.reserve_canonical(p,binding())
        self.reject(c.finalize_canonical,p,{})
        self.reject(c.finalize_canonical,p,{"wrong_type":1})
        r=c.finalize_canonical(p,{"first":True,"second":False})
        self.assertEqual(r["failed_checks"],["second"])

    def test_042_strict_json(self):
        raw=c.json_bytes({"label":"Māori","value":1})
        self.assertIn("Māori".encode(),raw);self.assertTrue(raw.endswith(b"\n"))
        self.reject(c.json_bytes,{"x":float("nan")})
        self.reject(c.strict_json,'{"x":1,"x":2}')
        self.reject(c.strict_json,'{"x":Infinity}')

    def test_043_card_ids(self):
        c.validate_deck(deck())
        v=deck();v["cards"].append(copy.deepcopy(v["cards"][0]))
        self.reject(c.validate_deck,v)

    def test_044_card_tiers(self):
        c.validate_deck(deck())
        v=deck();v["cards"][3]["parent_ids"]=["card2"];self.reject(c.validate_deck,v)

    def test_045_card_cycles(self):
        c.validate_deck(deck())
        v=deck();v["cards"][1]["parent_ids"]=["card4"];self.reject(c.validate_deck,v)

    def test_046_stable_prefix(self):
        c.validate_deck(deck())
        v=deck();v["stable_prefix"]=["card1","card3"];v["volatile_index"]=["card2","card4"]
        self.reject(c.validate_deck,v)

    def test_047_baton_sections(self):
        c.validate_deck(deck())
        v=deck();v["sections"]=v["sections"][:-1];self.reject(c.validate_deck,v)

    def test_048_card_manifest(self):
        p={"cards/anchor.json":b'{"tier":1}\n',"index.json":b"{}\n"}
        m=c.manifest_for(p,exclusions=["card-manifest.json"])
        c.verify_manifest(m,p,list(p)+["card-manifest.json"],["card-manifest.json"])
        m["entries"][0]["byte_domain"]="raw_bytes_v1"
        self.reject(c.verify_manifest,m,p,list(p)+["card-manifest.json"],["card-manifest.json"])

    def test_049_html_landmarks(self):
        doc=c.render_report(report());self.assertTrue(c.validate_report(doc)["valid"])
        self.reject(c.validate_report,doc.replace("lang='en'","lang=''"))

    def test_050_table_headers(self):
        doc=c.render_report(report());c.validate_report(doc)
        self.reject(c.validate_report,doc.replace("scope='col'","scope='bad'"))

    def test_051_html_escaping(self):
        v=report();v["rows"][0]["title"]="<img src=x onerror=alert(1)>"
        doc=c.render_report(v);self.assertNotIn("<img",doc);self.assertIn("&lt;img",doc)
        c.validate_report(doc)
        self.reject(c.validate_report,doc.replace("</main>","<script>x</script></main>"))

    def test_052_relative_links(self):
        c.validate_report(c.render_report(report()))
        for bad in ("javascript:alert(1)","https://example.invalid/x","../outside","//remote"):
            v=report();v["links"][0]["path"]=bad;self.reject(c.render_report,v)

    def test_053_text_outcomes(self):
        v=report();v["rows"]=[dict(title=x,outcome=x) for x in sorted(c.OUTCOMES)]
        doc=c.render_report(v);p=c.ReportStructure();p.feed(doc)
        for state in c.OUTCOMES:self.assertIn(state," ".join(p.text))
        v["rows"][0]["outcome"]="certified";self.reject(c.render_report,v)

    def test_054_manual_review(self):
        doc=c.render_report(report())
        self.assertFalse(c.validate_report(doc)["manual_evaluation_complete"])
        self.reject(c.validate_report,doc.replace("affected-user","unknown"))

    def reserved(self,index):
        v=reservations();self.assertTrue(c.validate_reservations(v)["valid"])
        v["rows"][index]["executed"]=True;self.reject(c.validate_reservations,v)

    def test_055_independent_gap(self):self.reserved(0)
    def test_056_empirical_gap(self):self.reserved(1)
    def test_057_affected_user_gap(self):self.reserved(2)
    def test_058_production_gate(self):self.reserved(3)
    def test_059_shared_mutation_gate(self):self.reserved(4)
    def test_060_next_route_gate(self):self.reserved(5)


class RecordingResult(unittest.TextTestResult):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.successful=[]
    def addSuccess(self,test):
        super().addSuccess(test)
        self.successful.append("RA6856-N"+test._testMethodName.split("_")[1])


if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--receipt",required=True)
    ap.add_argument("--fixture-root",required=True)
    ap.add_argument("--test-name", action="append")
    args=ap.parse_args()
    FIXTURE_ROOT=Path(args.fixture_root).resolve()
    FIXTURE_ROOT.mkdir(parents=True,exist_ok=True)
    suite=(unittest.TestSuite(CapsuleTests(name) for name in args.test_name)
           if args.test_name else unittest.defaultTestLoader.loadTestsFromTestCase(CapsuleTests))
    result=unittest.TextTestRunner(verbosity=2,resultclass=RecordingResult).run(suite)
    receipt=dict(schema="ghc.family.rowan-ash.behavioral-tests.v1",
                 tests_run=result.testsRun,failures=len(result.failures),
                 errors=len(result.errors),valid=result.wasSuccessful(),
                 successful_proposals=result.successful,rejections=REJECTIONS,
                 rejecting_fixture_count=len(REJECTIONS),same_owner_only=True,
                 independent_reproduction=False,canonical_invocations=0,
                 reservation_fixtures_are_synthetic=True,
                 boundary=c.BOUNDARY)
    with Path(args.receipt).open("xb") as f:f.write(c.json_bytes(receipt))
    raise SystemExit(not result.wasSuccessful())
