from pathlib import Path
import json,re,hashlib
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[2]
BANK=Path(r'D:\GHC-Archives\phase-banks\avelin-reed-v707-v6-r2')
OUT=ROOT/'laboratory/data';OUT.mkdir(parents=True,exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
rows=read(BANK/'laboratory-audit.json');catalogue=[];mounts=[]
for i,r in enumerate(rows):
 selected=next((x for x in r['selected'] if x['path'].endswith('.html')),None)
 overview=next((x for x in r['selected'] if 'overview' in x['path']),r['selected'][0])
 s=(BANK/'source-windows'/overview['local_readback_file']).read_text(encoding='utf-8')
 pars=[re.sub(r'\s+',' ',p).strip() for p in s.split('\n\n') if p.strip() and not p.startswith('#')]
 topic=next((p for p in pars if any(t in p.lower() for t in ['laboratory','finite','phase adds'])),pars[0] if pars else 'Bounded source evidence')[:1000]
 item={'id':f'L{i+1:02}','owner':r['owner'].replace('-',' ').title(),'phase':r['phase'],'topic':topic,'source_head':r['source_head'],'coverage':r['coverage'],'artifacts':[{'path':x['path'],'sha256':x['sha256'],'bytes':x['bytes']} for x in r['selected']],'html_count':len(r['html_paths']),'github_url':'https://github.com/HamishT26/Beyonder-Real-True-Journey/blob/'+r['source_head']+'/'+(selected or overview)['path'],'inherited_execution_credit':0}
 catalogue.append(item)
 if selected:mounts.append({'id':item['id'],'checkout':str(Path(r'D:\GHC-Archives\worktrees')/r['source_checkout']),'commit':r['source_head'],'path':selected['path'],'sha256':selected['sha256']})
write(OUT/'labs.json',catalogue);write(BANK/'legacy-mounts-private.json',mounts)
write(OUT/'skills.json',read(BANK/'skill-inventory.json'))
write(OUT/'projects.json',read(BASE/'projects.json'));write(OUT/'roster.json',read(BASE/'roster-v20.json'))
research=[
 {'title':'GMUT: a typed research programme','finding':'The four-dimensional GR expression requires a symmetric covariant rank-two correction with curvature units. An unspecified Ω_AB does not identify a field, action, observation model or measured coefficient. Conservation, stability and the GR limit are explicit open requirements.','url':'https://arxiv.org/abs/1907.03150'},
 {'title':'THOS: inspectable local/cloud contracts','finding':'The practical integration is a local reproducible model bank, source-bound artefacts, portable exports and a separate authorized cloud archive. Simulation and agent evaluation remain different forms of evidence.','url':'https://developers.openai.com/api/docs/guides/agent-evals'},
 {'title':'Freed ID: claims, issuers and evidence','finding':'A credential expresses an issuer claim. Our local envelope records a claim and its source, without claiming cryptographic verification, legal identity or consciousness.','url':'https://www.w3.org/TR/vc-data-model/'},
 {'title':'Nexus recovered from Journey v42','finding':'Lines 352–364 describe local compute, cloud compute and a provider bridge. Those are historical architectural proposals. The remaster adopts explicit local/cloud boundaries and budgeted transport; assertions of unlimited capability remain unverified.','url':None},
 {'title':'Recent simulation and evaluation research','finding':'OpenAI deployment simulation research (June 2026) motivates realistic contextual tests. NVIDIA Omniverse DSX (March 2026) motivates explicit digital-twin inputs. Neither result supplies evidence for this project’s physics or identity claims.','url':'https://openai.com/index/deployment-simulation/'},
 {'title':'MCP security boundaries','finding':'Treat remote content as data, preserve token audience boundaries and avoid arbitrary URL forwarding. This laboratory exposes an allowlisted read-only loopback service.','url':'https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices'},
 {'title':'Open mathematical problems','finding':'Finite numerical examples cannot settle universal existence, complexity or spectral claims. The problem dossier records bounded attempts and exact reasons that broader problems remain open.','url':'https://www.claymath.org/millennium-problems/'},
 {'title':'Faith, ethics and physical explanation','finding':'Theological commitments and ethical reasons deserve interpretation in their own terms. They do not become measured tensor terms through a shared vocabulary. CBR comparisons use explicit values and affected-party processes.','url':'https://www.vatican.va/archive/ENG0015/__P6C.HTM'},
 {'title':'Simulation inspiration not retrieved','finding':'The specific mattshumer X post returned HTTP 403. No visual, code or capability claim is attributed to an unread post.','url':'https://x.com/mattshumer_/status/2095596175705399482?s=20'}]
write(OUT/'research.json',research)
write(BASE/'journey-source-index.json',[{k:v for k,v in r.items() if k not in ['windows','opening']} for r in read(BANK/'journey-audit.json')])
write(BASE/'last-ten-phase-review.json',[{'owner':r['owner'],'phase':r['phase'],'source_head':r['source_head'],'overview':next((x['path'] for x in r['selected'] if 'overview' in x['path']),r['selected'][0]['path']),'transfer_to_remaster':'Preserve finite domain limits, exact source bindings, malformed-subject history, separate canonical/delivery states, and browser evidence coverage.','inherited_execution_credit':0} for r in rows[-11:-1]])
write(BASE/'design-spec.json',{'concept':'external phase bank laboratory-concept.png','concept_sha256':hashlib.sha256((BANK/'laboratory-concept.png').read_bytes()).hexdigest(),'layout':'White background, 280px navigation, editorial serif heading, teal control, plot with narrow parameter inspector and exact value table','tokens':{'ink':'#103b48','muted':'#58707c','line':'#dce3e9','teal':'#146669','selected':'#fff2dd'},'intentional_deviations':['Browser chrome is not rendered inside the page.','Numerical table displays actual lattice values rather than illustrative concept values.','Additional nav views are required by the user portfolio and share the same typography and row layout.','Static native HTML/CSS/JS supplies an offline portable workbench without a framework runtime.'],'fidelity_review_pending':True})
print(json.dumps({'labs':len(catalogue),'private_source_mounts':len(mounts),'skills':len(read(OUT/'skills.json')),'last_ten':10,'research_cards':len(research)}))
