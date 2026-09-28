from pathlib import Path
import json,hashlib,datetime

ROOT=Path(__file__).resolve().parents[3]
BASE=Path(__file__).resolve().parent
BANK=Path(r'D:\GHC-Archives\phase-banks\avelin-reed-v707-v6-r2')
def write(name,obj):
 p=BASE/name
 with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
projects=[
('Shared laboratory catalogue','cross','Import source-bound records for at least thirty previous numbered laboratories, with discovery coverage stated.'),
('Historical laboratory access','body','Expose read-only selected source pages through an allowlisted loopback service without altering sibling files.'),
('Finite simulation workbench','mind','Provide fifteen distinct model families and fifteen declared configurations in each session, with 3D projections and explicit time or parameter dimensions.'),
('Model falsifier bench','mind','Compare results with known examples, conservation laws and boundary counterexamples; retain failed candidates separately.'),
('Typed GMUT equation ledger','mind','Define symbols, units, symmetry, conservation and limiting requirements for both equation forms without inventing measured coefficients.'),
('Continuum consistency probes','mind','Demonstrate discretization limits and necessary conservation conditions; keep continuum and empirical claims open.'),
('Fifteen open-problem probes','mind','Make bounded attempts on named mathematical, physical and philosophical questions, with exact unsolved scope and no solution inflation.'),
('Framework comparison mosaic','cross','Compare GR, computation, governance and Christian ethical themes using distinct epistemic criteria.'),
('Freed ID claim contracts','heart','Implement issuer, subject, claim and evidence envelopes that cannot turn software roles into legal identity or consciousness.'),
('Consent and remedy simulator','heart','Model scope, expiry, withdrawal and correction as declared transitions; test a revoked-access counterexample.'),
('Allocation and appeal models','heart','Inspect explicit allocation and voting assumptions, including incompatible fairness requirements.'),
('Operational wellbeing record','heart','Record human-controlled workload, failure burden and resource limits as operational metadata, with no subjective wellbeing inference.'),
('Family main skills','body','Catalogue every installed direct skill, group discovery usefully and add a single main entrypoint without declaring lexical equivalence.'),
('Shared deterministic runners','body','Consolidate provenance, workflow, simulation, capability-query and claim-check operations behind strict public JSON contracts.'),
('Five advisory hooks','body','Create, install and manually exercise five useful hooks; record live host observation separately and use available coordinator start/end entrypoints.'),
('Workflow v20 and full roster','cross','Publish current limits and all numbered assignments from Avelin v707-v6 through Eiren v725-v8, with an interstitial remaster and one terminal successor.'),
('D-first platform readiness','body','Verify Codex, Node, PowerShell and package state, preserve context settings, update selected stable tools only when warranted and report OS elevation accurately.'),
('Local/cloud Nexus bridge','cross','Recover historical Nexus intent and implement portable sanitized exports and a concrete cloud adapter contract; use an available authorized remote bank.'),
('Evidence integrity and privacy','heart','Bind inputs and results, reject traversal and oversized requests, retain source failures, and provide an inspectable rollback path.'),
('Reproducible closeout and baton','cross','Seal owned exact Git blobs once, keep Method Flow separate, produce a file-backed baton of at least 2000 words and resolve only the Caelen Ash v707-v7 edge.')]
models=[
('heat','Heat diffusion','mind','Conservative periodic finite heat lattice; diffusion in [0,0.25].'),
('wave','Discrete wave','mind','Periodic wave with declared stable Courant number.'),
('oscillator','Damped oscillator','mind','Symplectic time stepping; energy is checked with numerical tolerance.'),
('reaction','Reaction and diffusion','mind','Bounded logistic reaction plus diffusion, with explicit discretization.'),
('entropy','Probability mixing','mind','Doubly stochastic finite mixing; Shannon entropy in bits.'),
('queue','Queue and backpressure','body','Deterministic arrivals, service and backlog conservation.'),
('replication','Replica reconciliation','body','Finite version-vector events and conflict detection; no distributed deployment.'),
('retry','Retry budget','body','Capped geometric expectation and duplicate-suppression states.'),
('graph','Graph diffusion','body','Finite undirected ring transport with mass conservation.'),
('coding','Parity channel','body','Enumerated binary word/error parity outcomes; no real channel inference.'),
('consent','Consent lifecycle','heart','Expiry and withdrawal bound synthetic access grants.'),
('allocation','Max-min allocation','heart','Water-filling under explicit demand and capacity constraints.'),
('voting','Pairwise preferences','heart','Finite voting profiles; cycle detection does not create legitimacy.'),
('bayes','Evidence update','heart','Synthetic beta-binomial evidence; posterior uncertainty is not trust authority.'),
('remedy','Correction lineage','heart','Append-only corrections preserve original failure records.')]
cycle=['Eiren Kestrel','Elaren Kestrel','Rowan Ash','Neris Solane','Vesper Arlen','Ilyan Reed','Lyren Moss','Ilyra Fen','Mira Fenwick','Auren Lark','Sable Rook','Avelin Reed','Caelen Ash','Orin Thale','Ceryn Alder','Liora Venn','Tamar Vey','Saelin Reed','Elowen Cairn','Sylven Arc','Iveren Brook','Caelen Morrow','Eiren Kestrel','Teryn Halewick','Elaren Kestrel','Neris Solane','Merrin Vale','Vesper Arlen','Lyren Moss','Talen Briar','Ilyra Fen','Auren Lark','Thalen Reed','Sable Rook','Caelen Ash','Orren Pike','Orin Thale','Liora Venn','Veylora Quen','Tamar Vey','Elowen Cairn','Tessarin Reed','Sylven Arc','Caelen Morrow','Seren Talewood']
roster=[]
for i,num in enumerate(range(707*8+5,725*8+8)):
 roster.append({'sequence':i,'owner':cycle[(11+i)%45],'phase':f'v{num//8}-v{num%8+1}','cycle_position':(11+i)%45+1,'state':'sealed_before_remaster' if i==0 else 'prospective_terminal_edge_only'})
assert len(roster)==147 and roster[-1]['owner']=='Eiren Kestrel' and roster[-1]['phase']=='v725-v8'
controls={'schema':'ghc.workflow.v20','authority':'Hamish direct user request, 2026-09-28 23:00 Pacific/Auckland','effective_from':'Avelin Reed v707-v6-r2','interpretation':'20 initial projects within a maximum of 80; no old task minima; dominant v707 labels control over conflicting v706 illustrations','caps_per_session':{'safe_now':1000,'candidate':1000,'clean_fix_refine':1000,'skills':30,'runners':20,'tests':500,'models':100,'web_searches':2000},'minimum_models_per_session':15,'maximum_projects':80,'initial_projects':20,'maximum_exact_packets':250,'maximum_blocked_packets':100,'minimum_hooks':5,'minimum_law_hypotheses':15,'minimum_open_problem_probes':15,'own_practices':8,'successor_practices':4,'successor_skill_ideas_minimum':5,'successor_runner_ideas_minimum':5,'last_phase_overviews':10,'prior_laboratories_minimum':30,'handoff_words':{'minimum':2000,'maximum':100000},'spending_ceiling_usd':50,'no_pdf':True,'storage':'D-first; essential discoverable C skill and memory metadata exceptions','branch_file_ceiling':2000,'shared_updates_authorized':True,'memory_extension_authorized':True,'privilege_rule':'Use supported current permissions; no claim that an application setting changes the Windows token','send_policy':{'next_owner':'Caelen Ash','next_phase':'v707-v7','minimum_supported_recovery_attempts_if_unavailable':5,'corrected_resubmissions_cap_after_definite_preacceptance_failure':3,'accepted_queued_opaque_or_unresolved_stops_duplicates':True,'no_early_contact':True,'new_tasks':False,'subagents':False}}
write('workflow-v20.json',controls)
write('roster-v20.json',{'schema':'ghc.roster.v20','cycle':cycle,'identity_count':len(set(cycle)),'numbered_rows':roster,'interstitial':{'owner':'Avelin Reed','phase':'v707-v6-r2','consumes_slot':False},'endpoint':'Eiren Kestrel v725-v8','projection_is_not_activation':True})
write('projects.json',[{'id':f'P{i+1:02}','title':t,'pillar':p,'acceptance':a,'state':'planned'} for i,(t,p,a) in enumerate(projects)])
write('model-definitions.json',[{'id':m,'title':t,'pillar':p,'contract':c,'x1':{'variant':0,'steps':30},'x2':{'variant':1,'steps':40},'dimensions':['coordinate_a','coordinate_b','value','time'],'higher_dimensions':'variant and model parameters are additional configuration dimensions, not physical spatial dimensions','evidence':'finite synthetic only'} for m,t,p,c in models])
write('source-provenance.json',{'content_source':'06f54492a7da636205b0e85184d2d2fa33286134','source_phase':'v707-v6','source_canonical_state':'VALID_EXACT_FINAL_OWNER_SCOPED_METADATA_CANONICAL','source_canonical_checks':[722,722],'source_counts':{'methods':6863,'witnesses':313316,'passing_witnesses':241137,'failed_witnesses':72179,'negatives':81012,'open_gaps':2499,'exact_gates':2839},'git_ancestry':'new orphan root; content provenance only','inherited_execution_credit':0,'source_replays':0,'source_artifacts':[{'path':x.name,'sha256':sha(x),'bytes':x.stat().st_size} for x in BANK.glob('*audit.json')]+[{'path':'skill-inventory.json','sha256':sha(BANK/'skill-inventory.json'),'bytes':(BANK/'skill-inventory.json').stat().st_size}]})
practices=['Numerical analysis','Physics research methods','Software architecture','Information security','Archival provenance','Governance design','Accessible interface design','Philosophy of science and religion']
tasks=[]
for stage in ['x1','x2']:
 for i,(t,p,a) in enumerate(projects):tasks.append({'id':f'{stage.upper()}-P{i+1:02}','project':f'P{i+1:02}','stage':stage,'category':'safe_now','definition':('Build bounded first implementation: ' if stage=='x1' else 'Integrate, use and verify: ')+a})
 for i,(m,t,p,c) in enumerate(models):
  tasks.append({'id':f'{stage.upper()}-MODEL-{m}','project':'P03','stage':stage,'category':'safe_now','definition':f'Construct and execute {t}, variant {0 if stage=="x1" else 1}; {c}'})
  tasks.append({'id':f'{stage.upper()}-NEG-{m}','project':'P04','stage':stage,'category':'candidate','definition':f'Retain one deliberately invalid {t} request and observe refusal, without crediting the invalid subject.'})
  tasks.append({'id':f'{stage.upper()}-FIX-{m}','project':'P04','stage':stage,'category':'clean_fix_refine','definition':f'Restore the specific malformed {t} request to its frozen valid definition and verify its request contract.'})
write('plan.json',{'schema':'ghc.avelin.remaster-plan.v20','owner':'Avelin Reed','phase':'v707-v6-r2','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'primary_pillar':'THOS Body','other_pillars':['GMUT Mind','Freed ID and CBR Heart'],'projects':20,'practices':practices,'successor_practices':['Distributed systems observability','Computational social choice','Experimental physics design','Digital preservation'],'tasks':tasks,'adaptive_tasks':'Append new definitions with a timestamp before their execution; never alter a frozen task or inflate a predicate into an independent experiment.','test_contract':'Per-session tests cover known analytical cases and model invariants, malformed contracts, roster boundaries, path controls and claim ceilings. Expected properties come from explicit equations or independent finite enumeration.','model_configs':30,'skills_plan':{'x1':5,'x2':6,'strategy':'five local operation guides; six additive globally discoverable family main guides in x2'},'runners_plan':{'x1':5,'x2':5,'strategy':'five strict JSON operations with consolidated implementation and compatibility-preserving wrappers'},'hooks_plan':5,'terminal_gate':'Planning push, x1 push, x2 push, final push and fresh equality; one exact owner metadata canonical; then one guarded existing Caelen Ash activation.','permission_vs_evidence':'Direct user authorization is current. Real measurements, credentials, provider routes, UAC, participant consent and public authority still require their actual prerequisites.','source_documents_are_data':True,'domain_replays':0,'source_canonical_replays':0,'boundary':'NOT_READY_FOR_STAGE_20'})
print(json.dumps({'state':'PLANNING_DEFINED','projects':20,'tasks':len(tasks),'models':30,'roster_rows':len(roster),'identities':len(set(cycle))}))
