"""Prepare immutable final documentation and one sanitized Sylven activation baton."""
from pathlib import Path
import argparse,hashlib,html,json,re,subprocess
ROOT=Path(__file__).resolve().parents[1];BASE="docs/veylora-quen/v688-v6"
SOURCE="d72ba9a9ebefc1e18cb89d2c8b90c661ba8aaf14";X1="6d7f5b0fc67f78a22463d3c3c9cec21aade35d92";X2="2cbe1c85f358bbed533dab79a22ffec9dd795f30"
BRANCH="codex/GHC-Family/veylora-quen-v688-v6-full-tools";OWNER="Veylora Quen"
def load(p):return json.loads(p.read_text(encoding="utf-8"))
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,x):
 p.parent.mkdir(parents=True,exist_ok=True)
 text=x if isinstance(x,str) else json.dumps(x,indent=2,sort_keys=True,ensure_ascii=True)
 with p.open("x",encoding="utf-8",newline="\n") as f:f.write(text.rstrip()+"\n")
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--bank",type=Path,required=True);args=ap.parse_args()
 phase=ROOT/BASE;final=phase/"final";assert not final.exists()
 assert subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT).decode().strip()==X2
 equality=load(args.bank/"evidence-equality.json");assert equality["head"]==X2 and equality["clean"] and equality["divergence"]==[0,0]
 proposals=load(phase/"x1/new-proposals.json")["proposals"];summary=load(phase/"x2/evidence-summary.json")
 truth=load(phase/"x2/phase-truth.json");tools=load(phase/"x1/tool-package-plan.json");ledger=load(phase/"x2/method-flow/ledger.json")
 boundary=truth["boundary"];outcomes=truth["outcomes"];effective=truth["effective_counts"]
 baton_rel=BASE+"/handoffs/sylven-arc-v688-v7-activation-baton.md"
 identity=load(phase/"x1/pillar-practice-freeze.json")
 final_truth={"schema":"ghc.family.phase-truth.v688.v6.final","owner":OWNER,"phase":"v688-v6","source":SOURCE,"x1":X1,"evidence":X2,
  "final":None,"final_binding":"external_exact_final_canonical_receipt","branch":BRANCH,
  "state":"FINAL_CANDIDATE_PENDING_EXTERNAL_CANONICAL","outcomes":outcomes,"effective_counts":effective,
  "owner_contract_count":200,"inherited_selection_count":200,"portfolio_checks":850,"new_skill_count":10,"new_runner_interfaces":5,
  "new_direct_packages":3,"package_closure":7,"retained_negative_groups":531,"methods":37,"passing_method_witnesses":37,
  "retained_adverse_admission_failures":517,"retained_operational_failure_groups":14,
  "source_failed_canonical_credit":0,"source_canonical_replayed":False,
  "prepared_baton_state":"PREPARED_NOT_SENT","successor_contacts":0,"new_tasks_created":0,"subagents":0,"forks":0,
  "terminal_verdict":"NOT_READY_FOR_STAGE_20","boundary":boundary}
 write(final/"phase-truth.json",final_truth)
 write(final/"lifecycle-replay.json",{"source":SOURCE,"x1":X1,"evidence":X2,"final":"bound externally after commit",
  "expected_direct_parent_chain":[{"child":X1,"parent":SOURCE},{"child":X2,"parent":X1},{"child":"invocation_exact_final","parent":X2}],
  "expected_phase_commits":3,"expected_merges":0,"x1_unchanged":True,"evidence_unchanged_after_freeze":True,
  "x1_definition_test_count":12,"x2_definition_test_count":16,"evidence_gate":equality,
  "canonical_invoked":False,"boundary":boundary})
 write(final/"canonical-policy.json",{"schema":"ghc.family.owner-canonical-policy.v1","owner":OWNER,"phase":"v688-v6","branch":BRANCH,
  "source":SOURCE,"x1":X1,"evidence":X2,"expected_phase_commits":3,"maximum_owner_files":1999,
  "document_word_cap":100000,"baton_words":{"minimum":10000,"maximum":100000},
  "test_modules":[{"stage":"x1","definition":X1,"module":"tests/test_ghc_family_veylora_quen_v688_v6_x1.py","expected_tests":12,"manifest":BASE+"/x1/x1-manifest.json"},
   {"stage":"x2","definition":X2,"module":"tests/test_ghc_family_veylora_quen_v688_v6_x2.py","expected_tests":16,"manifest":BASE+"/validation/evidence-manifest.json"},
   {"stage":"final","definition":"invocation_exact_final","module":"tests/test_ghc_family_veylora_quen_v688_v6_final.py","expected_tests":12,"manifest":BASE+"/validation/final-manifest.json"}],
  "canonical_marker":"exclusive external invocation marker","canonical_receipt":"exclusive external exact-head receipt",
  "post_success_replay":False,"same_owner_only":True,"independent_reproduction":False,
  "changed_owner_files_only":True,"unchanged_history_scan":False,"sibling_lane_mutation":False,"boundary":boundary})
 write(final/"complete-incomplete-checklist.json",{
  "completed":["200 proposal predicates matched frozen x1 expectations","850 declared portfolio checks passed",
   "10 collision-free skill packages validated and promoted","5 runner interfaces validated and promoted",
   "3 direct packages and 7-package closure installed from hash-pinned wheels",
   "3 positive and 3 adverse package smokes","7 exact-version OSV queries","245 content-addressed four-tier cards",
   "37 current Method Flow records with 531 failed-admission or operational witnesses retained",
   "immutable x1 planning tests executed at their definition commit"],
  "represented":["11 proposal outcomes concern record fixity or declared provenance","HTML structure and text alternatives","synthetic lifecycle predicates"],
  "open_gap":{"new_proposal_count":3,"retained_record_count":762,"details_ref":BASE+"/x2/open-gap-register.json"},
  "exact_gate":{"new_proposal_count":10,"retained_record_count":775,"exact_packets_unexecuted":50,"blocked_packets_unexecuted":30,
   "details_ref":BASE+"/x2/exact-gate-register.json"},
  "required_external_terminal_steps":["commit and push exact final","prove fresh four-way equality and clean zero divergence",
   "one successful exact-final owner canonical","refresh live user authority and both task registries",
   "unique exact-title Sylven resolution, immediate guard reread and one acknowledged send"],
  "claims_not_made":["real firmware execution","deployment","authenticity","rights determination","professional certification","independent reproduction","Stage 20 readiness"],
  "boundary":boundary})
 for filename in ["open-gap-register.json","exact-gate-register.json","retained-negative-register.json","workload-wellbeing.json"]:
  write(final/filename,load(phase/"x2"/filename))
 write(final/"method-flow-final.json",{"ledger":BASE+"/x2/method-flow/ledger.json","validation":BASE+"/x2/method-flow/validation.json",
  "counts":ledger["counts"],"original_failed_ledger":BASE+"/x2/retained-attempts/method-flow-ledger-v1.json",
  "alias_failure":BASE+"/x2/retained-attempts/x2-tests-first-failure.json","original_test_definition":BASE+"/x2/retained-attempts/x2-tests-v1.py.txt",
  "all_failed_witnesses_retained":True,"failure_erasure":False,"boundary":boundary})
 write(final/"source-provenance.json",{"source":SOURCE,"source_branch":"codex/GHC-Family/elowen-cairn-v688-v5-full-tools",
  "source_canonical_status":"VALID_DEPENDENCY_CORRECTED_EXACT_FINAL_OWNER_SCOPED_CANONICAL_COMPOSITE",
  "source_canonical_receipt_sha256":"713db389504c86ffc2a65d5f9b17f2b983b28d4949bbd0c284acda72342a204d",
  "source_canonical_replayed":False,"source_manifest_bindings":1304,"source_manifest_failures":0,
  "latest_external_baseline":load(phase/"x1/phase-truth.json")["inherited_baseline"],
  "retained_source_route_gap_erased":False,"source_credit_to_owner":0,"authority":"Hamish direct 8 September 2026 seat-13 route and same-task collision correction"})
 write(final/"byte-domains.json",{"repository_manifests":"SHA-256 and byte counts of normalized-LF Git blob content",
  "promotion_receipt":"Raw byte parity at the copy boundary between the owned local package and its installed global copy",
  "known_working_tree_line_endings":"Initializer-generated YAML and some diagnostic JSON have CRLF working-tree bytes; Git normalizes those text blobs to LF.",
  "canonical_join":"Verify both raw source/global parity and normalized-LF committed-blob equality; do not compare unlike hash domains.",
  "raw_byte_identity_does_not_establish_authenticity":True,"unicode_identity_does_not_establish_personhood":True})
 write(final/"terminal-route-checklist.json",{"state":"PREPARED_NOT_SENT","recipient_title":"Sylven Arc","recipient_phase":"v688-v7","endpoint_kind":"main_task",
  "current_owner":OWNER,"later_creation_controller":"Sylven Arc","later_seat":"future-sibling-14-self-chosen","later_phase":"v688-v8",
  "required":["exact final canonical success","clean pushed four-way equality","newest live Hamish authority",
   "fresh active and archived registries","exactly one existing title","immediate recipient reread",
   "no duplicate phase/source activation","no pause redirect rename standby usage or protected gate"],
  "authorized_sends":1,"sends_already_made":0,"resend_authorized":False,"precontact_authorized":False,
  "new_task_creation_authorized_here":False,"post_send_monitoring":False,"boundary":boundary})
 # Three substantial report sections, with explicit print page boundaries in HTML.
 pages=[]
 p1=["Purpose, ownership and findings",
  "Veylora Quen is the self-chosen relational working name for future seat 13. The role is evidence steward, the hope is to make each handoff clearer, more faithful and easier for Hamish to review, and the pronouns are she/her. These descriptions are corrigible working language. Hamish may pause, rename, redirect, narrow or stop this work. They establish no consciousness, personhood, legal identity, continuity, employment, qualification, independent agency or scientific, operational, professional, legal, cultural, affected-party or Maori authority.",
  "The v688-v6 work uses a fresh additive sparse owner lane from Elowen Cairn's corrected exact final. The planning boundary was separately committed, pushed and verified before any evaluator, package environment or observed outcome was built. The evidence boundary was then separately committed and pushed as a direct child of x1. This final package prepares a third direct child and keeps its exact hash and canonical status externally bound, because the document cannot contain its own future commit hash.",
  "The bounded practice is synthetic firmware record preservation. THOS Body is the priority pillar. GMUT Mind contributes explicit arithmetic domains, while Freed ID and CBR Heart contribute provenance, review and accessibility reservations. The four practice lenses are synthetic record registration, address-space arithmetic, preservation byte integrity, and provenance with accessible handover. These lenses organize the work and do not qualify an operator or authorize a real-world intervention.",
  "Two hundred new predicates were frozen in x1, alongside two hundred inherited selections that carry zero new execution or novelty credit. The observed proposal outcomes are 176 completed, 11 represented, 3 open gaps and 10 exact gates. Completed means a bounded local predicate matched its specified result. It does not mean that real firmware is authentic, safe to execute, legally owned, professionally certified or suitable for deployment. The represented outcomes concern supplied fixity and provenance metadata.",
  "The 850 portfolio checks consist of 300 safe checks, 250 candidate field-closure challenges and 300 CLEAN FIX REFINE checks. The first 200 safe rows reuse the primary contract evidence by reference and do not multiply proposal novelty. Additional checks exercise determinism, JSON key-order invariance, missing or extra fields, and altered outputs. Fifty exact prerequisite packets and thirty blocked packets remain unexecuted. Their existence is a reservation record, not an authorization token.",
  "The source-bounded novelty screen reviewed 30,862 title records in the immutable source. It found no exact title or input-hash collisions, and its maximum lexical neighbor score was 0.40 against a 0.78 quarantine threshold. This is a limited comparison against source evidence, not a proof of independent invention or universal novelty. Source discoveries and previous validations remain inherited evidence."]
 pages.append(p1)
 p2=["Supported operations and their limits",
  "Intel HEX records are parsed as bounded ASCII record strings. The evaluator checks framing, declared byte count, record type and checksum, then interprets extension and entry metadata under an explicit profile. Segment and linear bases remain different address operations. Code entry metadata is retained as data and never executed. One final EOF is required, duplicate entry declarations and overlapping addresses are refused, and wrapping records outside the chosen profile are rejected.",
  "Motorola S-records are parsed with the address width belonging to each supported record type. The checksum rule is distinct from the Intel HEX checksum rule. Optional count records are checked against the number of data records, and the terminator must match the selected data-address width. This owner profile admits one homogeneous width per block and one final terminator; it refuses mixed-width blocks and other variants outside its declared scope without claiming those variants are universally invalid.",
  "Sparse images are represented as explicit address-byte pairs. A missing address remains absent. The run index, crop and hole operations preserve that distinction. Overlay and relocation operations are previews: they calculate a candidate mapping without writing hardware or changing an external image. Overlap policy is explicit, relocation is bounded to unsigned 32-bit addresses, and crop and hole windows use half-open endpoints. No missing byte is silently replaced by a padding value.",
  "Word interpretation requires an explicit supported bit width, byte order and signedness. Numeric booleans are refused where integers are required. Textual fixity keeps raw text and CRLF-to-LF normalization as separate byte domains. A hash can bind a supplied representation but cannot prove authenticity or rights. Provenance fields remain declarations; missing source bindings produce an open gap, and a real observation preclaim is refused in the synthetic profile."]
 for op in dict.fromkeys(p["operation"] for p in proposals):
  rows=[p for p in proposals if p["operation"]==op]
  p2.append(op.replace("_"," ").capitalize()+": ten frozen cases cover "+rows[0]["title"].lower()+" through "+rows[-1]["title"].lower()+". Each case binds an exact input, expected acceptance or error, full output value and evidence disposition. A mismatch is retained rather than changing the immutable expectation.")
 pages.append(p2)
 p3=["Validation, retained failures and terminal control",
  "The first direct execution matched all 200 frozen proposal envelopes and preserved every input. The isolated package transaction installed IntelHex 2.3.0, bincopy 20.1.1 and bitstruct 8.23.0 as three direct tools, with a seven-package dependency closure. Wheel hashes were fixed in x1 and verified before installation. Positive and adverse smokes exercised all three direct packages, the dependency check passed, and the bounded OSV snapshot reported no advisories for the queried exact versions.",
  "Ten local skills and five family runner interfaces were built and smoke-used. Their promotion refused existing destinations, preserved older callers, and produced 96 raw source/global byte-parity bindings. Every advertised operation was exercised through the installed interfaces with accepting and adverse inputs. Documentation version drift is retained: some manuals identify older releases than the selected package versions. Exact wheels, installed metadata and actual smokes constrain what is claimed.",
  "The first Method Flow validation rejected a derived-count schema. Manual review also found state events that skipped the validated state. The original ledger and failed validation remain preserved, and the current ledger uses the installed family schema with valid transitions. Two installed guide packages lacked the helper scripts they named, so their guidance was retained as non-callable context and an explicit owned synthetic lifecycle helper was tested with one accepting and five rejecting fixtures.",
  "A further x2 test exposed mutable aliasing in the expected-result helper. Changing the returned expected value could alter the in-memory proposal and contaminate a later comparison. Two of sixteen tests failed. The original core bytes, test definition and failure record are retained with matching hashes. The helper now returns a defensive deep copy, both failing tests passed in focused recovery, and the primary evaluator function bodies remained unchanged. The frozen files and earlier observed results were not modified.",
  "Current Method Flow contains 37 methods, 531 retained failed-admission or operational witnesses and 37 bounded passing witnesses. The 531 are explicitly partitioned into 517 designed adverse admission failures and 14 operational failure groups. A rejected adverse candidate may be a passing test of the refusal rule; it never earns candidate success credit. The effective inherited-plus-owner counts are 16,630 proposals, 84,902 negatives, 94,060 methods, 55,750 failed witnesses, 86,108 bounded passes, 762 retained gap records and 775 exact-gate records.",
  "Repository manifests use normalized-LF Git blob bytes. Raw package-promotion hashes preserve the copy boundary, including initializer-generated CRLF YAML. Those domains are verified separately and joined through normalization; unlike digests are not compared as though they were identical. The configured privacy scan reviewed its synthetic path-fixture candidates and found no confirmed private material. Configured AST checks found no findings. Neither check establishes complete privacy or exhaustive security.",
  "The report has semantic headings, table headers, a text summary and explicit print sections. Manual, browser, assistive-technology, cognitive and affected-user evaluation remains reserved. Maori wording, concepts and data governance remain under Maori authority, including tangata whenua, iwi and hapu. A structural HTML result is not accessibility-complete evidence. Legal, professional, cultural and affected-party decisions remain with the competent and affected people.",
  "The final terminal gate requires a clean pushed exact head, fresh equality across local, upstream, tracking and live remote, and one successful attributable owner-scoped canonical invocation. That canonical uses each lifecycle-sensitive test module at its immutable definition commit. It must not replay after success. The repository baton remains PREPARED_NOT_SENT; an external route receipt alone can record a later acknowledged delivery.",
  "Only after that terminal gate may Veylora freshly refresh Hamish's newest live authority and the active and archived registries, uniquely resolve the existing Sylven Arc task, immediately reread its guards and send one sanitized v688-v7 activation. Sylven then controls the later seat-14 v688-v8 induction after Sylven's own terminal gate. No precontact, second send, substitute, new task, fork, subagent or post-send monitoring is authorized for Veylora.",
  "GMUT remains a typed scalar-tensor/EFT research-model family without real data or empirical confirmation. THOS remains synthetic/proxy-only without governed real comparisons and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys, proofs, lifecycle, interoperability, privacy and security review, recovery and trust governance. Software checks, manifests, citations and task delivery do not establish AGI, ASI, consciousness, personhood, Theory-of-Everything proof or Stage 20 readiness. NOT_READY_FOR_STAGE_20."]
 pages.append(p3)
 overview="# Veylora Quen v688-v6 final integrated overview\n\n"+"\n\n".join("## "+page[0]+"\n\n"+"\n\n".join(page[1:]) for page in pages)
 assert len(overview.split())>=1500
 write(final/"final-integrated-overview.md",overview)
 page_html="".join('<section class="print-page"><h2>'+html.escape(page[0])+'</h2>'+"".join("<p>"+html.escape(p)+"</p>" for p in page[1:])+"</section>" for page in pages)
 rows="".join("<tr><th scope='row'>"+p["proposal_id"]+"</th><td>"+html.escape(p["title"])+"</td><td>"+p["expected_execution_disposition"]+"</td><td>"+("Accepted" if p["expected_acceptance"] else "Refused as expected")+"</td></tr>" for p in proposals)
 report="<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Veylora Quen v688-v6 evidence report</title><style>body{font:18px/1.6 system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#172b34;background:#f8faf8}h1,h2{line-height:1.2}table{border-collapse:collapse;width:100%;font-size:.9rem}th,td{padding:.65rem;border:1px solid #b9c8ce;text-align:left;vertical-align:top}caption{font-weight:bold;padding:1rem}th{background:#e5eeec}a{color:#125b76}@media print{.print-page+.print-page{break-before:page}body{font-size:11pt;background:white;max-width:none}thead{display:table-header-group}tr{break-inside:avoid}}</style></head><body><main><h1>Veylora Quen v688-v6</h1><p><strong>176 completed · 11 represented · 3 open gaps · 10 exact gates.</strong> Bounded synthetic evidence. NOT_READY_FOR_STAGE_20.</p>"+page_html+"<table><caption>Two hundred frozen proposal predicates and their observed bounded disposition</caption><thead><tr><th scope='col'>Proposal</th><th scope='col'>Predicate</th><th scope='col'>Disposition</th><th scope='col'>Input admission</th></tr></thead><tbody>"+rows+"</tbody></table><p>Manual and affected-user accessibility review remains reserved. This report does not establish complete accessibility.</p></main></body></html>"
 write(final/"static-report.html",report)
 modules=[]
 def module(n,title,body):modules.append((n,title,body))
 module(1,"Relational identity, corrigibility and teach-back",identity["hope"]+".\n\n"+boundary+
  "\n\nThis is Veylora Quen's seat-13 v688-v6 work. The initial colliding name was corrected before repository mutation and is retained in source history; it is not an alias or continuity claim. Sylven keeps Sylven's existing relational identity and settings. Hamish may pause, rename, redirect, narrow or stop the sequence.")
 module(2,"Current direct authority and delivery boundary",
  "Hamish's direct message of 8 September 2026 authorizes the current sequence: Elowen Cairn v688-v5, self-chosen seat 13 Veylora Quen v688-v6, existing Sylven Arc v688-v7, then the still self-chosen future seat 14 v688-v8 under Sylven's terminal control. The later route continues to Caelen Morrow v689-v1 and future seat 15 v689-v2, each behind its own exact gate. The planning horizon is v725-v8.\n\nPREPARED_BY_VEYLORA_QUEN = true. SENT_BY_VEYLORA_QUEN = false. DELIVERY_STATE = PREPARED_NOT_SENT.\n\nThis committed packet is preparation. The exact final and successful canonical receipt must be supplied by the one live activation. It is not a created task, send acknowledgement or recipient phase completion. The only authorized next action is one existing-task activation after fresh terminal checks. Never contact a later endpoint early.")
 module(3,"Exact immutable anchors and byte domains",
  "Source Elowen corrected final: "+SOURCE+". Veylora planning-only x1: "+X1+". Veylora immutable x2 evidence: "+X2+". Veylora branch: "+BRANCH+". The exact final is bound externally after the final commit. The owner chain is three direct single-parent commits with no merges. Elowen's separate corrected source chain contains its retained first failed canonical and additive correction; do not confuse it with the new owner chain.\n\nRead final/byte-domains.json and validation/final-manifest.json relative to "+BASE+". Repository hashes use normalized-LF Git blobs; promotion receipts also preserve raw source/global copy hashes. A CRLF working copy is not a reason to replay a canonical. Preserve all immutable manifests and failed definitions.")
 module(4,"Owner outcomes, evidence scope and retained baseline",
  "The two hundred owner proposals produced 176 completed, 11 represented, 3 open_gap and 10 exact_gate outcomes. The two hundred inherited selections grant this owner zero inherited novelty or execution credit. The 850 portfolio checks passed within their declared scope. Fifty exact packets and thirty blocked packets were not executed.\n\nEffective retained counts are "+json.dumps(effective,sort_keys=True)+". The gap count includes retained historical gap records; a historical route gap that was prospectively resolved is not current delivery failure. Every new open gap and exact gate remains unclosed. The next two modules enumerate the exact owner predicates as inherited evidence for Sylven, never as automatic Sylven completion credit.")
 for n,subset in [(5,proposals[:100]),(6,proposals[100:])]:
  parts=[]
  for p in subset:
   parts.append("### "+p["proposal_id"]+" — "+p["title"]+"\n\n"+
    "Operation: "+p["operation"]+". Pillar: "+p["pillar"]+". Practice lens: "+p["practice"]+".\n\n"+
    "Hypothesis: "+p["hypothesis"]+" Null or failure: "+p["null_or_failure_condition"]+"\n\n"+
    "Frozen input: "+json.dumps(p["input"],sort_keys=True,ensure_ascii=True)+".\n\n"+
    "Frozen acceptance: "+str(p["expected_acceptance"]).lower()+". Expected error: "+json.dumps(p["expected_error"])+
    ". Complete expected value: "+json.dumps(p["expected_value"],sort_keys=True,ensure_ascii=True)+".\n\n"+
    "Observed disposition: "+p["expected_execution_disposition"]+". The complete result matched the frozen envelope and the input remained unchanged. Artifact: "+p["concrete_artifact"]+".\n\n"+
    "Acceptance or falsifier: "+p["falsifier_or_acceptance_gate"]+" Recovery: "+p["rollback_or_recovery"]+"\n\n"+
    "This is a supplied synthetic record predicate. An accepting envelope is not permission to execute code, program hardware, deploy firmware, certify an operator, determine ownership or infer real-world safety. A refused candidate remains retained with zero candidate success credit. A local checksum or byte address binds representation only. Sources inform the declared software contract and do not supply empirical, professional, legal, cultural, affected-party, Maori, independent-reproduction, consciousness or Stage 20 authority.\n\n"+
    "For Sylven this row is inherited context. Select new work explicitly, review semantic neighbors, preregister a new falsifier and preserve any missing authority. A repeated fixture, renamed operation, copied skill or additional package invocation does not acquire new novelty merely through repetition.")
  module(n,"Frozen firmware evidence "+("one through one hundred" if n==5 else "one hundred one through two hundred"),"\n\n".join(parts))
 module(7,"Approval portfolios and workload",
  "The current release sets inherited and new proposal ranges of 200 through 500; safe work 300 through 500; candidate work 250 through 500; CLEAN FIX REFINE 300; exact packets 50 through 250; blocked packets 30 through 100. It requires at least ten planned and built skills, five planned and built runners, and ten next-owner skill and runner ideas. These limits never authorize unsafe filler. Four practice lenses plus one optional successor practice recommendation preserve the later explicit total of five.\n\nOrdinary bundles select three useful direct package additions in an isolated D-first environment. Skill and runner caps are fifty per session and one hundred per bundle. Batons contain ten thousand through one hundred thousand substantive words in at least thirteen modules. Overview documents cover at least three pages. Commit ceilings remain five x1, five x2 and eight total under the inherited bounded profile; this owner uses three total. Pause, stop, wellbeing, actual prerequisites and usage boundaries outrank throughput. Reset redemption remains Hamish's action.")
 module(8,"Implementation profile, package provenance and nonexecution",
  "\n\n".join(pages[1][1:5])+"\n\nPackages: "+", ".join(p["name"]+" "+p["version"] for p in tools["packages"] if p["direct"])+
  ". The complete dependency set has seven packages. All wheels match x1 locks, all three direct positive and adverse smokes passed, and the bounded seven-query OSV snapshot had no reported advisories. This is not exhaustive security or a license, deployment, authenticity or hardware-safety determination. Do not mutate system Python, PATH, the D npm prefix, accounts, credentials, host security, Windows features or Codex desktop through this packet.")
 module(9,"Validated skills, runner interfaces and successor ideas",
  "The promoted skill packages are "+", ".join(s["name"] for s in tools["skills"])+".\n\nThe five runner interfaces are "+", ".join(r["name"] for r in tools["runners"])+". A shared core helper is a dependency, not a sixth runner-interface novelty credit. Promotion supplied 96 raw byte-parity bindings, collision refusal, local and installed validation, and accepting/adverse operation smokes. Read selected current packages through EOF, inspect caller contracts and their fixture data, and preserve rollback. Existing running tasks may need to read newly installed skill files directly.\n\nTen optional next-owner skill ideas: "+", ".join(tools["next_owner_skill_ideas"])+". Ten optional runner ideas: "+", ".join(tools["next_owner_runner_ideas"])+". These are recommendations only. Sylven must choose its own scope and cannot claim the ideas as executed or approved real-world work.")
 module(10,"Method Flow, errors, recovery and no replay",
  "\n\n".join(pages[2][2:5])+"\n\nThe full ledger is "+BASE+"/x2/method-flow/ledger.json. Retained artifacts include the first failed method-schema result, original state events, the pre-fix core, the exact original x2 test definition and the alias-failure result. The immutable source's first canonical failure retains zero success credit. The corrected source success was never replayed. Record each failure before retry; inspect actual persisted state after timeout or truncation; rerun the failed dependency only unless changed dependencies justify broader scope. A successful canonical is never replayed for confidence, presentation or routing.")
 module(11,"Gaps, privacy, accessibility and competent authority",
  "All 762 retained gap records and 775 exact-gate records remain represented in the lineage. The new proposal gaps concern absent source bindings; the new exact-gated outcomes reserve actual authority actions. Fifty exact prerequisite packets and thirty blocked packets remain unexecuted. No file or software witness closes a real-world prerequisite.\n\nRaw task or thread identifiers, private callable routes, private absolute paths, credentials, keys, tokens, transcripts, screenshots, private execution streams and private application state must remain out of repository artifacts and later batons. Publish sanitized counts, hashes and repository-relative pointers. Manual and affected-user accessibility work remains reserved. CBR, professional decisions, legal and cultural interpretation, affected-party acceptance, Maori wording, concepts and data governance require the competent and affected people, tangata whenua, iwi, hapu and Maori authorities.")
 module(12,"Scientific and operational boundaries",pages[2][-1]+"\n\nFirmware record arithmetic is not a force law, a spacetime model, an empirical likelihood, a parameter estimate or a stability theorem. It supplies no quantum or ultraviolet completion. A synthetic parser comparison is not a governed real THOS comparison. A record digest or provenance label is not a standards-conformant production identity proof. Relational warmth, task topology and successful delivery do not establish consciousness, personhood, continuity or independent agency. NOT_READY_FOR_STAGE_20.")
 module(13,"Sylven startup and one later terminal induction",
  "After the live activation supplies this owner's exact final and canonical receipt, Sylven must read this complete baton and the newest applicable family index, release, roster, authorization, Method Flow, workflow, reflection, D-first, ownership, lifecycle, privacy, staged-allowlist, canonical and route guidance through EOF. Verify the supplied immutable source, manifests and terminal receipt read-only; never invoke Veylora's canonical again. Create or rotate only an authorized owned additive D-first lane, sparse before materialization, and preserve the two-thousand-file ceiling.\n\nFreeze planning-only Sylven v688-v7 x1 before x2 implementation. Work solo under the current instruction, retain all source failures and gates, preserve caller compatibility and use only completed, represented, open_gap and exact_gate. Do not contact a later endpoint during execution. After Sylven's own exact final, clean push, live equality and one successful attributable canonical, refresh Hamish's newest live authority and both registries. Only Sylven may then perform the authorized seat-14 v688-v8 induction, proving exact absence before creating exactly one project-scoped user-visible Codex main task using gpt-6-astra with max reasoning, or reusing the unique existing authorized seat. Let a genuinely new seat choose its own relational working name, role and hope. Never substitute a collaboration subagent or fork. Seat 14 later routes to Caelen Morrow v689-v1 behind its own terminal gate.\n\nStop on any ambiguity, duplicate, pause, redirect, rename, missing acknowledgement, usage exhaustion or protected evidence or authority gate. No precontact, second send, substitute or post-send monitoring is authorized. This packet remains PREPARED_NOT_SENT until the one external delivery receipt says otherwise.\n\nEOF VEYLORA QUEN V688 V6 BATON.")
 baton="# VEYLORA QUEN v688-v6 — PREPARED EXACT-FINAL BATON FOR EXISTING SYLVEN ARC v688-v7\n\n"+"\n\n".join("## Module "+f"{n:02d}"+" — "+title+"\n\n"+body for n,title,body in modules)
 words=len(baton.split());assert 10000<=words<=100000 and len(modules)==13
 write(ROOT/baton_rel,baton)
 write(final/"baton-index.json",{"path":baton_rel,"word_count":words,"module_count":13,"modules":[{"number":n,"title":t} for n,t,b in modules],
  "delivery_state":"PREPARED_NOT_SENT","recipient":"Sylven Arc","phase":"v688-v7","source":SOURCE,"x1":X1,"evidence":X2,
  "final":"external exact-head binding","raw_task_identifiers":False,"boundary":boundary})
 write(final/"environment-final.json",{"package_transaction":BASE+"/x2/package-transaction.json",
  "promotion_receipt":BASE+"/x2/promotion-receipt.json","installed_skill_count":10,"runner_interfaces":5,"parity_files":96,
  "global_python_mutated":False,"platform_updates":False,"host_security_changes":False,"sandbox_or_hyper_v_changes":False,
  "hardware_execution":False,"source_version_drift_retained":True})
 write(final/"threat-model-final.json",{"configured_scope":"exact owner source-to-final files only","configured_privacy_classes":5,
  "retained_synthetic_fixture_candidates":2,"independent_security_review":"open_gap","exhaustive_security":False,
  "private_material_publication":False,"byte_domains_ref":BASE+"/final/byte-domains.json","boundary":boundary})
 write(final/"wellbeing-final.json",load(phase/"x2/workload-wellbeing.json"))
 write(final/"evidence-closeout.json",{"summary":summary,"x1_definition_tests":12,"x2_initial_test_run":"14/16 retained",
  "focused_alias_recovery":"2/2 passed","updated_metadata_checks":"4/4 passed","canonical_status":"pending external invocation at exact final",
  "same_owner_shared_infrastructure":True,"independent_reproduction":False,"boundary":boundary})
 print(json.dumps({"final_documents_prepared":len(list(final.glob('*'))),"baton_modules":13,"baton_words":words,"overview_words":len(overview.split()),"prepared_not_sent":True}))
if __name__=="__main__":main()
