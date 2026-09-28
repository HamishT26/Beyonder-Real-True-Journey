"""Apply the bounded review refinements, preserving prior Git snapshots."""
from pathlib import Path
import json, hashlib, shutil, subprocess, sys

ROOT = Path(__file__).resolve().parents[3]
DOC = Path(__file__).resolve().parent
BANK = Path("D:/GHC-Archives/phase-banks/avelin-reed-v707-v6-r2")
def read(p): return json.loads(p.read_text(encoding="utf-8"))
def put(p, x):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def replace(p, old, new):
    s=p.read_text(encoding="utf-8")
    if old not in s: raise ValueError("Expected source not found: "+str(p))
    p.write_text(s.replace(old,new),encoding="utf-8")

inventory=read(ROOT/"laboratory/data/skills.json")
assert isinstance(inventory,list) and len(inventory)==2219
parts=[]
for index,start in enumerate(range(0,len(inventory),800),1):
    name=f"skills-{index}.json"; target=ROOT/"laboratory/data"/name
    put(target,inventory[start:start+800])
    parts.append({"file":name,"rows":len(inventory[start:start+800]),"sha256":digest(target)})
put(ROOT/"laboratory/data/skills.json",{"schema":"ghc.capability-index.v2","total":len(inventory),"chunks":parts,"semantics":"Lossless sharding; metadata discovery does not validate inherited code."})
replace(ROOT/"laboratory/operations.js",
 "if(operation==='catalogue')return queryCatalogue(q,JSON.parse(fs.readFileSync(path.join(dataDir,'skills.json'),'utf8')));",
 "if(operation==='catalogue'){const index=JSON.parse(fs.readFileSync(path.join(dataDir,'skills.json'),'utf8'));const rows=Array.isArray(index)?index:index.chunks.flatMap(c=>{if(!/^skills-[1-9][0-9]*\\.json$/.test(c.file))throw Error('Invalid catalogue chunk');const b=fs.readFileSync(path.join(dataDir,c.file));if(hash(b)!==c.sha256)throw Error('Catalogue digest mismatch');return JSON.parse(b);});return queryCatalogue(q,rows);}")
replace(ROOT/"laboratory/server.js",
 "'model-contracts','intake-card'",
 "'model-contracts','intake-card','integration','skills-1','skills-2','skills-3'")
replace(ROOT/"laboratory/app.js",
 "'model-contracts','intake-card'])",
 "'model-contracts','intake-card','integration'])")
replace(ROOT/"laboratory/app.js",
 "db[name]=await res.json();}",
 "db[name]=await res.json();} const skillIndex=db.skills;db.skills=[];for(const chunk of skillIndex.chunks){const r=await fetch('data/'+chunk.file);if(!r.ok)throw Error('Capability chunk unavailable');const rows=await r.json();if(rows.length!==chunk.rows)throw Error('Capability count mismatch');db.skills.push(...rows);}if(db.skills.length!==skillIndex.total)throw Error('Capability total mismatch');")
replace(ROOT/"laboratory/app.js",
 "library();skills();$('#project-list')",
 "const integrated=db.integration;$('#integration-card').append(record('Consent-safe correction under backpressure',integrated.summary),text('p',integrated.boundary));$('#sibling-list').replaceChildren(...db.roster.sibling_records.map(r=>record(r.identity||r.owner||r.name,JSON.stringify(r))));library();skills();$('#project-list')")
replace(ROOT/"laboratory/index.html",
 '<div id="research-list"></div>',
 '<div id="integration-card"></div><div id="research-list"></div>')
replace(ROOT/"laboratory/index.html",
 '<div class="table-scroll"><table><thead><tr><th>Owner</th>',
 '<details><summary>Thirty identities and observed activity</summary><div id="sibling-list"></div></details><div class="table-scroll"><table><thead><tr><th>Owner</th>')
replace(DOC/"phase.txt",
 "'"+(Path.home()/"AppData/Local/Programs/Python/Python312/python.exe").as_posix()+"'",
 "require('path').join(require('os').homedir(),'AppData/Local/Programs/Python/Python312/python.exe')")
integration=read(DOC/"cross-pillar-integration.json")
put(ROOT/"laboratory/data/integration.json",{
 "schema":"ghc.integration-card.v1","title":"Consent-safe correction under backpressure",
 "summary":f"{integration['passed']}/{integration['total']} recorded checks passed across 12 frozen schedules. The independent matrix calculation agrees within 1e-10; expired publication is denied, the valid control publishes, and the cached-permission mutant is detected.",
 "receipt":"docs/avelin-reed/v707-v6-r2/cross-pillar-integration.json",
 "receipt_sha256":digest(DOC/"cross-pillar-integration.json"),
 "boundary":"Synthetic local software evidence at recorded code versions. No empirical physics, real-world consent, consciousness, identity or public authority is established."})
review={
 "schema":"ghc.consultation-receipt.v20","title":"Review and refine GHC Lab",
 "route":"authenticated existing ChatGPT UI","messages_sent":2,"replies_read":2,
 "new_conversations":0,"new_agents":0,"current_x1_messages":0,"current_x2_messages":2,
 "timing_exception":"The standing instruction arrived after x1 sealed. Both actual messages occurred in x2; no retroactive x1 credit.",
 "standing_rule":{"x1":1,"x2":1,"typo_interpretation":"x21 means x1","wait":"Permit a slow response; continue independent work; do not resend an accepted or unresolved message."},
 "target":"Private D-drive review-conversation.json resolves the exact user-selected conversation; no private identifier in public export.",
 "replies":[{"topic":"Durable uniqueness and provenance/readback","adopted_receipts":["shared-intake-acceptance.json","shared-intake-barrier-acceptance.json"]},
 {"topic":"Consent-safe correction under backpressure","adopted_receipts":["integration-plan.json","cross-pillar-integration.json"]}],
 "independent_reproduction":False,"successor_gate_unchanged":"Caelen Ash v707-v7 only after terminal canonical and exact native routing."}
put(DOC/"consultation-receipt.json",review)
with (DOC/"review-adoption.md").open("a",encoding="utf-8") as f:
    f.write("\n## The two completed consultations\n\nBoth explicitly requested messages were sent through the authenticated existing ChatGPT conversation and both substantive replies were read. This establishes that UI route for this conversation. It does not establish a separate agent messaging API. The first reply led to a persistent SQLite transaction, a required non-null source tuple, independent pinned expectations, same-buffer validation and consumer readback. Thirteen acceptance checks and a separate two-check all-ready barrier continuation passed. The continuation strengthens synchronization without replaying the successful aggregate. A total of 122 ordinary test processes were used, with no agent or chat creation.\n\nThe second reply led to the frozen consent-safe correction integration: twelve schedules and fifteen checks, an independent discrete update-matrix oracle, explicit four-slot waiting and two-slot service bounds, expiry checked at publication, retained failed original R0, separate correction R1 and zero inherited credit. The deliberate cached-permission mutant was detected. These are same-owner synthetic software results. The reviewer's suggestions are advisory; their reply is not independent reproduction of the implementation.\n\nHamish's new standing rule is one advisory message during x1 and one during x2 for future bundles. Both current messages happened in x2 because x1 had already sealed. Preserve that exception. A slow Pro response is not a failed send. Never resend accepted or unresolved messages merely because a response takes time. The advisory conversation is separate from the thirty-seat roster and the Caelen successor gate.\n")
plugin=Path("D:/GHC-Archives/plugins/ghc-family-laboratory-v20")
plugin_dest=ROOT/"plugins/ghc-family-laboratory-v20"
copied=[]
for p in sorted(plugin.rglob("*")):
    if p.is_file() and "__pycache__" not in p.parts and p.suffix!=".pyc":
        rel=p.relative_to(plugin); dest=plugin_dest/rel
        dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
        copied.append({"path":dest.relative_to(ROOT).as_posix(),"sha256":digest(dest)})
put(DOC/"plugin-installation.json",{**read(BANK/"plugin-installation.json"),"source_files":copied})
put(DOC/"compatibility-mapping.json",{
 "schema":"ghc.caller-map.v20","deletions":0,"legacy_names_retained":True,
 "earlier_router":"v18 remains an independent legacy entrypoint; no claim of semantic equivalence",
 "main_guides":[{"guide":"ghc-family-main-"+name+"-v20","operation":op,"existing_adapter":"runners/"+op+".txt"} for name,op in [("laboratory","catalogue"),("models","model"),("evidence","integrity"),("governance","claim"),("workflow","route"),("capabilities","catalogue")]],
 "change":"The skill inventory uses three lossless chunks. CLI verifies each digest; the UI checks row counts. The persistent intake API independently verifies its stored evidence."})
put(DOC/"review-finish-receipt.json",{"skills":2219,"chunks":parts,"plugin_source_files":len(copied),"consultations":2,"replies":2,"current_x1":0,"current_x2":2,"source_replay":False})
print(json.dumps({"skills":2219,"chunks":len(parts),"plugin_files":len(copied),"review_replies":2}))
