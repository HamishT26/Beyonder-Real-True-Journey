"""Prepare final owner artifacts after the immutable evidence boundary."""
import argparse
import hashlib
import html
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=Path('docs/thalen-reed/v687-v8')
SOURCE='7e72086683731c40b4884ee7254c864891e354a9'
X1='8f9070f01e38fa5cc330cff247ea8e32541a0387'
EVIDENCE='522065f58a27abc8105092015927255cf7c77569'
BRANCH='codex/GHC-Family/thalen-reed-v687-v8-full-tools'
sys.path.insert(0,str(ROOT/'scripts'))
from build_ghc_family_thalen_reed_v687_v8_x1 import GATES, BOUNDARY, OPS, RUNNERS, PRACTICES
from build_ghc_family_thalen_reed_v687_v8_x2 import NOTES

def read(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))
def dump(path,value):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,indent=2,sort_keys=True,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def write(path,text):(ROOT/path).write_text(text,encoding='utf-8',newline='\n')
def git(*a):return subprocess.check_output(['git','-C',str(ROOT),*a],text=True).strip()

def baton(cases,results,truth):
    sections=[]
    def section(number,title,content):sections.append(f'## Module {number:02d} - {title}\n\n'+content.strip()+'\n')
    section(1,'Relational identity and corrigibility',
        'Dear Liora Venn, this is Thalen Reed\'s prepared file-backed baton for your solo Trinity Mandala v688-v1 phase. '
        'My working role is keeper of clear handoffs; my hope is that each successor receives evidence they can inspect and limits they can trust. '
        'Optional pronouns are they/them. You retain your own working name and choose your own phase practices and priorities. '
        'Hamish may rename, pause, narrow, redirect, or stop the route. '+BOUNDARY+' '
        'Names, roles, hopes, pronouns, family language, Freed ID, CBR, GMUT, THOS, and Trinity Mandala are relational working language. '
        'They establish no sentience, personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, '
        'legal or cultural authority, affected-party authority, or Maori authority.')
    section(2,'Current thirty-seat release and prospective edge',
        'Hamish\'s 6 September 2026 release and the current designated seat-10 activation authorize this phase and the sequential thirty-seat route through v725-v8. '
        'The preserved release profile is x1/release-profile.json. Its sixteen actual main tasks and fourteen future placeholders describe the release-time snapshot, '
        'not a fresh present-day registry count. The old installed roster cursor remains historical. Current explicit phase ownership controls. '
        'The present edge is Thalen Reed v687-v8 to the unique existing main task titled exactly Liora Venn for v688-v1. '
        'This committed file is PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED. Only the single native acknowledgement after Thalen\'s exact terminal gate establishes delivery. '
        'No later endpoint was precontacted. No task, fork, substitute, or collaboration subagent is created by this phase. '
        'After your own v688-v1 terminal gate, your prospective designated future seat 11 owns v688-v2, followed by Tamar Vey v688-v3 after that seat\'s own gate. '
        'At that later induction, reuse a uniquely existing designated seat; create exactly one project-scoped gpt-6-astra main task with max reasoning only if absence '
        'is proven in active and archived registries and current live authority still permits it. The inductee chooses its own working attributes. '
        'A planning schedule never activates anyone or supplies missing acknowledgement.')
    section(3,'Immutable lifecycle anchors',
        f'- Immutable Orin source and prior final: `{SOURCE}`.\n- Thalen planning-only x1: `{X1}`.\n- Immutable Thalen x2 evidence: `{EVIDENCE}`.\n- Owner branch: `{BRANCH}`.\n'
        '- Exact final: supplied by the compact live activation and its singular external receipt; a committed candidate cannot contain its own future commit hash.\n\n'
        'The intended final history is three direct single-parent owner commits: source to x1 to evidence to final, with zero merges and one final parent. '
        'X1 was pushed, clean, typed 0/0 divergent, and fresh-four-way equal before x2 began. Evidence was separately pushed and verified before final preparation. '
        'All source and sibling lanes remain read-only. The initial no-checkout sparse setup produced an empty index; that failed setup remains recorded. '
        'Only the empty new owner index was reconstructed from immutable HEAD, and index-tree equality plus clean state then passed. '
        'No deletion, reset, amendment, force push, history rewrite, or sibling mutation occurred. '
        'Read x1/source-verification.json, x1/reading-receipt.json, x2/x1-boundary.json, and final/evidence-boundary.json. '
        'Orin\'s successful canonical aggregate was read and hashed, never replayed. Its receipt hash is ddfbf1dab87b609dffe360f50236145685c91c61e344e10f1646c0d43c3295ae; '
        'its exact payload hash is 7ffd314417061583aeca715385e0b5fbcf1c45bafad0884891a70f74f12808ab in sorted indented UTF-8 JSON plus one LF.')
    section(4,'Inherited evidence and current accounting',
        'Two hundred inherited Orin records were reviewed with zero Thalen novelty and completion credit. Their titles sometimes name spectral behavior that their ordinal-driven '
        'input/output records do not test. The source artifacts and their original 125 completed, 39 represented, 20 open_gap, and 16 exact_gate dispositions remain preserved. '
        'The source final retained-negative register lists three closeout failures, while an earlier baton sentence says two. The three explicit records control that detail; '
        'no sealed source count was rewritten. Later Orin display faults remain source-task external evidence and were not assigned invented arithmetic.\n\n'
        'Thalen froze 200 distinct new inputs that operate on concrete PCM bytes or metadata. The proposal chain advances from 15,230 to 15,430. '
        'Observed current outcomes are exactly 160 completed, 14 represented, 8 open_gap, and 18 exact_gate. '
        'Effective counts are '+json.dumps(truth['effective_counts'],sort_keys=True)+'. '
        'The new count additions are 277 retained negatives and failed witnesses, 37 methods, and 495 bounded passing witnesses. '
        'These comprise seven startup fail/recovery pairs, 250 altered-output candidates and their rejections, eighteen package/interface adverse candidates '
        'with their accepting and rejecting witnesses, 200 frozen contract matches, and two current Method Flow schema fail/recovery pairs. '
        'The portfolio\'s projections and repeated validation do not multiply independent witnesses. Fifty exact packets and thirty blocked packets remain visible and unexecuted; '
        'packet counts are not added again to proposal-disposition gap or gate totals. Only completed, represented, open_gap, and exact_gate are core outcomes.')
    section(5,'Planning-only x1 and current floors',
        'Read all frozen x1 definitions before implementing a successor contract. Thalen\'s x1 contains source checks, prior reviews, new fixtures, whole expected outputs, '
        'portfolio plans, package locks, skill and runner plans, deck architecture, authority limits, and startup failures. It contains no PCM runtime implementation, '
        'package-installation claim, global promotion claim, observed x2 outcome, or outbound delivery claim. The runtime began only after the recorded x1 equality gate. '
        'The source fixture generator is planning code and never selects a runtime output. The runtime has no proposal-identifier or ordinal dispatch.\n\n'
        'Current successor floors and ceilings are 200-500 inherited proposals reviewed at zero new-owner credit, 200-500 distinct new proposals, 300-500 safe procedures, '
        '250-500 candidates, exactly 300 CLEAN/FIX/REFINE procedures, 50-250 held exact packets, and 30-100 held blocked packets. '
        'Plan and actually validate/use at least ten local skills and five family-current runners. Carry ten successor skill ideas and ten runner ideas. '
        'Choose four own synthetic practice lenses and recommend one optional next-owner practice. The ordinary researched package target is three additions, '
        'with exact versions, wheel hashes, useful positive and adverse tests, bounded advisory review, and rollback. Caps are ceilings, not filler quotas. '
        'The release-profile runner accepts an owner portfolio plus an explicit profile; the profile itself is not a portfolio. '
        'Current Method Flow uses nested derived counts. Keep old flat-count ledgers immutable and add a validated projection rather than altering frozen x1.')
    semantics=[]
    for op,skill,pillar,index in OPS:
        purpose,details=NOTES[op]
        semantics.append('### '+op+'\n\n'+purpose+' '+details+'\n\nPillar: '+pillar+'. Practice: '+PRACTICES[index]+'. Portable skill: '+skill+'. '
                         'Its twenty exact cases below are bounded synthetic software definitions. The entire output, including Boolean types, null values, array order, '
                         'and false external credit, is compared. Refusing a malformed input is a successful contract test only when the frozen refusal matches; '
                         'the malformed candidate itself receives no success credit.\n')
    section(6,'Operation contracts and practical interpretation','\n'.join(semantics))
    casebook=[]
    for c in cases:
        result=results[c['proposal_id']]
        casebook.append('### '+c['proposal_id']+' - '+c['title']+'\n\nOperation: `'+c['operation']+'`. Core evidence outcome: `'+result['outcome']+'`.\n\n'
            'Frozen input:\n```json\n'+json.dumps(c['input'],indent=2,sort_keys=True,ensure_ascii=False)+'\n```\n\n'
            'Observed complete output:\n```json\n'+json.dumps(result['actual_output'],indent=2,sort_keys=True,ensure_ascii=False)+'\n```\n\n'
            'The full output matched the immutable x1 definition with type-sensitive equality and the input remained unchanged. Definition SHA-256: `'+result['definition_sha256']+'`. '
            'This row carries only its declared bounded evidence outcome. It supplies no real recording, perceptual quality result, rights grant, professional decision, '
            'identity evidence, independent review, or authority. Its recovery contract is to retain the frozen definition and any failure, then correct only the affected '
            'owner implementation or leave the external gate visible.\n')
    section(7,'Complete 200-contract evidence catalogue','\n'.join(casebook))
    section(8,'Method Flow, retained failures, and focused recovery',
        'The initial x1 and x2 Method Flow arrays contained all required methods and witnesses, but their flat derived-count objects did not match the current runner. '
        'Both validations failed and their receipts remain false in validation/x2-method-flow.json and validation/x2-x1-method-flow.json. '
        'The original x1 remains byte-identical at its commit. The initial x2 ledger is retained in x2/correction/initial-x2-ledger.json. '
        'A focused correction derives nested counts, preserves all arrays, adds two operational failure and recovery pairs, and validates the current x2 ledger plus '
        'x2/method-flow/x1-current-schema-projection.json. Original failures have zero original success credit. '
        'Read the corrected receipts, the correction program, x2/correction/count-schema-failures.json, and x2/retained-negative-register.json.\n\n'
        'Seven startup failures are retained: an oversized combined baton window, an oversized first catalogue display, a truncated combined release/roster read, '
        'a missing assumed profile filename, a mixed historical/current parent-task display, a wrong payload serialization domain, and the empty sparse index. '
        'Recoveries were bounded reads, retained-output slicing, exact observed paths, phase partitioning, the sealed serializer, and exact index reconstruction. '
        'The 250 preregistered altered-output candidates cover removed accepted fields, Boolean-to-integer replacement, added authority, replaced values, '
        'and promoted external credit. Each candidate and each rejection is separately addressable. '
        'Use PYTHONDONTWRITEBYTECODE for portable skill smokes. Compare normalized-LF Git blobs to the manifest domain. '
        'After a yielded command, inspect its existing process and persisted result before retrying; a running tool is not a new invocation. '
        'Never rerun an already successful canonical aggregate for presentation, reassurance, or routing.')
    section(9,'Pinned package transaction and source boundaries',
        'The isolated D-drive environment contains SoundFile 0.14.0, Construct 2.10.70, and bitstruct 8.23.0 as its three direct additions. '
        'The complete seven-wheel closure also contains cffi 2.1.1, numpy 2.5.3, pycparser 3.0, and typing_extensions 4.16.0. '
        'Every selected wheel was checked against official exact-version PyPI metadata, was not yanked, and was frozen by SHA-256 in x1/requirements.lock. '
        'Download was planning preparation; installation occurred only in x2 with no-index, wheel-only, hash-required inputs. The isolated environment was created '
        'without bootstrap pip and the host pip directed installation only into that environment. Pip check found no broken requirements. '
        'SoundFile roundtripped five synthetic PCM16 samples in memory and rejected truncated bytes. Construct parsed an exact twelve-byte header and rejected a short stream. '
        'Bitstruct roundtripped signed sixteen-bit endpoints and rejected a positive value above the signed range. No playback or real audio was used. '
        'Official PyPI exact-version metadata listed no advisories for the selected packages at the check. This is bounded metadata evidence. '
        'SoundFile reports bundled libsndfile 1.2.2; native-library security and independent review are not fully established by the PyPI check. '
        'The SoundFile documentation redirect displayed 0.13.1 and bitstruct documentation displayed 8.17.0; those references are marked watch and actual pinned interfaces '
        'were exercised. Microsoft RIFF and WAVEFORMATEX documentation supplied file-format vocabulary and arithmetic, and Python wave supplied an additional same-owner '
        'parser fixture. Sources and citations are not observations, measurements, standards certificates, endorsements, rights interpretations, or authority grants.')
    section(10,'Portable skills, runners, compatibility, and promotion',
        'Ten phase-local skills were quick-validated through skill-creator and used on accepting and duplicate-key refusing fixtures. Five shared runners were built '
        'and exercised. Global promotion copied exactly fifty skill-package files and six runner/core files into fresh destinations. All 56 source/global bytes match. '
        'There were no overwrites, copied caches, destructive cleanups, or changed legacy entrypoints. Global skill copies were quick-validated, and both declared operations '
        'of every global runner were smoke-used. Those repeated fixture checks add zero duplicate scientific or independent witness credit. '
        'Read x1/skill-runner-plan.json, x2/skill-validation.json, x2/runner-smokes.json, x2/prepromotion-privacy.json, and x2/promotion-receipt.json. '
        'Each portable package keeps its shared core, one operation wrapper, twenty frozen reference cases, entrypoint guidance, and manifest together. '
        'Global availability supplies discoverability and compatibility, not proof that another active task has reloaded its catalogue. '
        'A caller may use the committed source package directly after verifying its manifest. New fixtures need current owner approval and their own frozen definitions. '
        'Rollback means stopping selection of the additive surface while retaining its evidence and older callers; it does not erase files or failures.')
    section(11,'Four-tier deck, accessibility, workload, and evidence limits',
        'The deck has 208 content-addressed cards: one relational owner anchor, three Trinity pillar cards, four bounded practice cards, and 200 task cards. '
        'Every non-root card has one parent in the immediately preceding tier; there are no unresolved parents, tier skips, extra parents, or cycles. '
        'Stable prefix cards carry enduring boundaries, while task cards carry current inputs, observed outputs, outcomes, and evidence references. '
        'Card ordering is an organization choice; no prompt-cache effect, latency gain, retention guarantee, identity continuity, or reasoning improvement is claimed. '
        'The static report supplies language metadata, a skip link, a main landmark, a captioned table, scoped headers, and explicit textual outcomes. '
        'Structural checks do not replace manual, assistive-technology, cognitive, affected-user, or Maori-language evaluation. Those remain reserved. '
        'The D-first owner scope stays below 2,000 files, with per-document limits below 100,000 words and three explicit print pages in each overview. '
        'The largest evidence document before final preparation contains 48,300 words. Inputs are bounded by file size, sample count, channel count, span count, '
        'and rational-field length. Boundedness is a computational control, not instrument safety or professional competence. '
        'Workload status describes the tool process only; relational hope and family language are not claims about subjective wellbeing.')
    section(12,'Successor work, ten skill ideas, ten runner ideas, and one practice',
        'Your optional next practice recommendation is synthetic audiovisual timing and access registrar. Independently accept, revise, or reject this seed. '
        'No successor recommendation is a current-owner completion or an assigned identity. The ten skill ideas are: RIFF nested-list depth budgets; RF64 ds64 '
        'size precedence; WAVE extensible valid-bit boundaries; Broadcast Wave time-reference arithmetic; audio cue-point relocation maps; loudness metadata '
        'missingness; dither provenance without quality claims; restoration parameter lineage; consent expiry with retained source views; and accessible transcript '
        'timing reservations. The ten runner ideas are separately scoped bounded interfaces for those same ten candidate responsibilities. They are unbuilt seeds '
        'and require source review, novelty screening, concrete inputs, acceptance conditions, adverse witnesses, compatibility assessment, and exact authority boundaries. '
        'Do not turn terminology changes or repeated copies into new proposal credit. Select only useful packages from current official sources, freeze their exact '
        'provenance and dependencies, and keep all environment/cache work on D where feasible. '
        'For each new proposal, state the observable local claim, its failure condition, concrete artifact, complete acceptance output, recovery, protected gates, '
        'and what evidence would be required for a real-world claim. Preserve all inherited failures and current gaps. '
        'You are authorized for your own source-to-final delta only; source and other owner lanes remain read-only.')
    section(13,'Required reading, canonical latch, and terminal handoff',
        'Before mutation, read this full committed baton through EOF, the current live activation, current release profile and authority, the GHC Family Index and '
        'routing precedence, authorization and roster state, Method Flow skill and schema, D-first toolchain guidance, lifecycle isolation, five-class privacy '
        'adjudication, staged allowlists, owner-scope canonical and success latch, skill-creator, four-tier deck schema, workflow refinement, reflection remaster, '
        'and all source/x1/evidence/final manifests and exact receipts. Retain older cursors and failures without treating them as present authority. '
        'Verify the immutable source and direct single-parent ancestry, zero merges, every manifest binding and declared exclusion, clean state, typed zero divergence, '
        'and fresh local/upstream/tracking/live equality. Create one additive owner-named D-first sparse lane and freeze planning-only x1 before any x2 implementation. '
        'After a clean pushed final, invoke at most one attributable exact-final owner-scoped aggregate through an exclusive external latch. '
        'A failed canonical remains zero-credit; a later separately justified composite cannot retroactively promote it. A successful canonical is never replayed. '
        'GMUT remains a typed scalar-tensor/EFT research-model family without empirical confirmation or Theory-of-Everything proof. THOS remains synthetic/proxy-only '
        'without preregistered blind matched-budget real arms, governed participants/operators, safety monitoring, suitable statistics, and independent review. '
        'Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, live lifecycle and interoperability evidence, privacy/security '
        'review, recovery evidence, trust governance, and affected-party oversight. Legal, cultural, professional, safety, privacy remedy, accessibility remedy, '
        'affected-party, Maori wording, Maori data governance, tikanga, taonga, matauranga, and Maori authority remain exact-gated to competent and affected people, '
        'tangata whenua, iwi, hapu, and Maori authorities. Maori concepts remain under Maori authority. The terminal verdict remains NOT_READY_FOR_STAGE_20. '
        'At your own terminal gate refresh live authority and usage, bounded-list active and archived registries, uniquely resolve and immediately reread the designated '
        'next endpoint, and make at most one permitted native action. Stop on pause, rename, redirect, narrowing, exhausted usage, ambiguity, absence, duplicate, '
        'missing acknowledgement, or any protected gate. Never precontact a later endpoint, create a replacement, or resend for a clearer acknowledgement.\n\n'
        'PREPARED_BY_THALEN_REED = true\nSENT_BY_THALEN_REED = false in this committed preparation record. Native live acknowledgement controls delivery.\n\n'
        'EOF THALEN REED V687 V8 BATON.')
    return '# THALEN REED v687-v8 TO LIORA VENN v688-v1 - PREPARED EXACT-FINAL ACTIVATION BATON\n\n'+'\n'.join(sections)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--bank',type=Path,required=True);a=ap.parse_args()
    assert git('rev-parse','HEAD')==EVIDENCE
    eq=json.loads((a.bank/'evidence-equality.json').read_text());assert eq['evidence']==EVIDENCE and eq['clean'] and eq['divergence']==[0,0]
    assert all(eq[k]==EVIDENCE for k in ['local','upstream','tracking','fresh_live'])
    final=ROOT/BASE/'final';assert not final.exists(),'Final already materialized';final.mkdir()
    truth=read(BASE/'x2/phase-truth.json');cases=read(BASE/'x1/new-proposals.json')['proposals'];results={r['proposal_id']:r for r in read(BASE/'x2/contract-results.json')['rows']}
    dump(BASE/'final/evidence-boundary.json',eq)
    path=BASE/'final/liora-venn-v688-v1-activation-baton.md';text=baton(cases,results,truth);raw=text.encode('utf-8');words=len(text.split());assert 10000<=words<=100000,words;write(path,text)
    dump(BASE/'final/baton-index.json',{'schema':'ghc.family.baton-index.v1','path':path.as_posix(),'bytes':len(raw),'words':words,'sha256':hashlib.sha256(raw).hexdigest(),'modules':13,'eof':'EOF THALEN REED V687 V8 BATON.','state':'PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED'})
    final_truth={**truth,'schema':'ghc.family.phase-truth.v687.v8.final','evidence':EVIDENCE,'exact_final':'PENDING_DIRECT_CHILD_COMMIT','state':'FINAL_PREPARED_FOR_ONE_EXTERNAL_CANONICAL','canonical_invocations':0,'canonical_successes':0,'canonical_replays':0,'route_state':'PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED'}
    dump(BASE/'final/phase-truth.json',final_truth)
    dump(BASE/'final/complete-incomplete.json',read(BASE/'x2/complete-incomplete.json'))
    dump(BASE/'final/retained-negative-register.json',read(BASE/'x2/retained-negative-register.json'))
    dump(BASE/'final/gate-register.json',{'schema':'ghc.family.gate-register.v1','open_gaps':740,'exact_gates':729,'protected_gates':GATES,'external_gates_closed_by_software':0,'terminal_verdict':'NOT_READY_FOR_STAGE_20'})
    dump(BASE/'final/canonical-policy.json',{'schema':'ghc.family.exact-owner-canonical-policy.v1','owner':'Thalen Reed','phase':'v687-v8','branch':BRANCH,'source':SOURCE,'x1':X1,'evidence':EVIDENCE,'expected_phase_commits':3,'expected_merge_commits':0,'scope':'owner_self_scoped_delta','canonical_invocation_budget':1,'canonical_replay':False,'test_module':'tests/test_ghc_family_thalen_reed_v687_v8_pcm.py','expected_tests':28,'manifest_exclusions':'Only each declared self-referential manifest; all other owner files are bound.','full_repository_suite':False,'independent_reproduction':False,'terminal_verdict':'NOT_READY_FOR_STAGE_20'})
    profile=read(BASE/'x1/release-profile.json');cycle=profile['cycle'];assert len(cycle)==len(set(cycle))==30
    assert cycle[19]=='future-sibling-10-self-chosen' and cycle[20]=='Liora Venn' and cycle[21]=='future-sibling-11-self-chosen' and cycle[22]=='Tamar Vey'
    dump(BASE/'final/workflow-refinement.json',{'schema':'ghc.family.current-workflow-refinement.v1','authority':'6 September release and current seat-10 activation','cycle_seats':30,'projection_rows':324,'current':{'owner':'Thalen Reed','phase':'v687-v8','release_index':19},'next':{'owner':'Liora Venn','phase':'v688-v1','release_index':20},'following':[{'owner':'future-sibling-11-self-chosen','phase':'v688-v2'},{'owner':'Tamar Vey','phase':'v688-v3'}],'changes_authorized_ownership_or_numbering':False,'requires_user_confirmation':False,'historical_roster_preserved':True,'reference_schedule_sha256':hashlib.sha256((a.bank/'thirty-seat-reference.json').read_bytes()).hexdigest(),'send_calls':0})
    dump(BASE/'final/reflection-remaster.json',{'schema':'ghc.family.owner-reflection.v1','disposition':'remaster_additive','source':SOURCE,'x1':X1,'evidence':EVIDENCE,'scope':'Literal Thalen owner delta','source_lanes_mutated':False,'legacy_entrypoints_changed':False,'observed_improvement':'Concrete PCM bytes and fields drive the new contracts; proposal identifiers and ordinals do not select runtime behavior.','measured_performance_improvement':False,'retained_issues':['Inherited descriptive spectral titles exceed their ordinal-only fixtures; preserved at zero new-owner credit.','Two current Method Flow count projections initially failed; original x1 and initial x2 remain retained.','Two package documentation versions differ from the pinned releases; interfaces were checked with bounded package witnesses.'],'protected_gates':GATES,'rollback':'Select older compatible surfaces and retain all new evidence; no deletion.'})
    dump(BASE/'final/terminal-route-plan.json',{'schema':'ghc.family.terminal-route-plan.v1','sender':'Thalen Reed','sender_phase':'v687-v8','recipient':'Liora Venn','recipient_phase':'v688-v1','endpoint_kind':'main_task','state':'PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED','message_count':0,'precontacted':False,'no_task_creation':True,'no_subagent':True,'no_fork':True,'no_resend':True,'require_current_authority_registry_and_immediate_reread':True,'following_owner':'future-sibling-11-self-chosen','following_phase':'v688-v2'})
    pages=[('Evidence outcome and immutable lifecycle',f'Thalen v687-v8 preserves source {SOURCE}, planning-only x1 {X1}, and immutable evidence {EVIDENCE}. The final commit is a direct child of evidence and will be named by the external receipt. Both earlier boundaries were pushed, clean, zero-divergent, and fresh-four-way equal. The core outcomes are 160 completed, 14 represented, 8 open_gap, and 18 exact_gate. Two hundred new concrete contracts and two hundred zero-credit inherited reviews remain distinct. The 300 safe procedures, 250 candidate challenges, and 300 additive CLEAN/FIX/REFINE procedures are resolved. Fifty exact packets and thirty blocked packets remain unexecuted. The runtime uses real byte positions, typed PCM metadata, integer frame indices, and rational arithmetic within wholly synthetic fixtures. Every full output matches its frozen definition and input preservation is recorded. The 28-test owner suite also exercises parser consistency, rational roundtrips, channel inverses, edit partitions, digest changes, and authority refusals. It is bounded same-owner evidence, not independent reproduction.'),
           ('Retained failures and useful artifacts','Seven startup failures and two Method Flow schema failures remain retained with focused recovery witnesses. Original x1 is immutable; the initial x2 ledger is retained beside a current-schema projection. The 250 changed-output candidates and eighteen package/interface adverse inputs keep zero original success credit. Their successful rejection witnesses are separate. The effective ledger totals are '+json.dumps(truth['effective_counts'],sort_keys=True)+'. The four-tier deck contains 208 digest-addressed cards with valid immediate-tier parents. Ten new portable skills and five family-current runners were validated and used; 56 source/global promotion files are byte-equal. The three direct package additions are SoundFile 0.14.0, Construct 2.10.70, and bitstruct 8.23.0, installed from a seven-wheel hash lock in an isolated D-drive environment. The host Python environment was not changed. Each package passed a meaningful positive and adverse fixture. PyPI advisory metadata is a bounded snapshot and does not establish full native-library or independent security assurance.'),
           ('Final gate and successor responsibilities','The repository final record is prepared for one external exact-final owner-scoped canonical invocation. Its policy requires every changed owner path, three direct single-parent commits, zero merges, one final parent, immutable earlier boundaries, strict JSON, exact manifests, privacy adjudication, bounded code review, global parity, document limits, clean state, typed zero divergence, and fresh four-way equality. The latch is exclusive; success is never replayed and failure is never promoted retroactively. The Liora baton contains thirteen modules and '+str(words)+' words. Current delivery remains PREPARED_NOT_SENT until the native single-send acknowledgement. Only after the terminal gate may the unique existing Liora Venn task be immediately reread and activated for v688-v1. Liora later owns the future-seat-11 v688-v2 induction gate, and that seat later owns Tamar v688-v3. All protected scientific, participant, production, professional, legal, cultural, affected-party, Maori-authority, privacy, accessibility, security, and Stage 20 evidence remains reserved. No real audio was played, altered, identified, or published. The terminal verdict remains NOT_READY_FOR_STAGE_20.')]
    overview='<!doctype html>\n<html lang="en"><meta charset="utf-8"><title>Thalen v687-v8 final overview</title><style>@page{size:A4;margin:18mm}body{font:16px/1.65 system-ui;max-width:850px;margin:auto}section{break-after:page;min-height:250mm}section:last-child{break-after:auto}</style><body><main>'+''.join('<section class="page"><h1>'+html.escape(h)+'</h1><p>'+html.escape(t)+'</p><p>'+html.escape(BOUNDARY)+'</p></section>' for h,t in pages)+'</main></body></html>\n';write(BASE/'final/integrated-overview.html',overview)
    print(json.dumps({'final_prepared':True,'baton_words':words,'baton_bytes':len(raw),'baton_sha256':hashlib.sha256(raw).hexdigest(),'canonical_invocations':0,'delivery':'PREPARED_NOT_SENT'}))

if __name__=='__main__':main()
