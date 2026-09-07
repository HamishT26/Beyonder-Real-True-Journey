"""Freeze Thalen's planning inputs only. No PCM runtime or x2 outcomes exist here."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = Path('docs/thalen-reed/v687-v8')
SOURCE = '7e72086683731c40b4884ee7254c864891e354a9'
BRANCH = 'codex/GHC-Family/thalen-reed-v687-v8-full-tools'
GATES = ['empirical','real_participant','professional','production','deployment','identity',
         'legal','cultural','affected_party','maori_authority','privacy_complete',
         'accessibility_complete','exhaustive_security','independent_reproduction',
         'agi_asi','consciousness_personhood','theory_of_everything','proof_canon','stage20']
BOUNDARY = ('Relational working language only; no consciousness, personhood, identity continuity, '
            'employment, qualification, independent agency, scientific, operational, legal, cultural, '
            'affected-party, or Maori authority is established. Same-owner software evidence is not '
            'independent reproduction. NOT_READY_FOR_STAGE_20.')
OPS = [
    ('riff_chunks','ghc-family-riff-chunk-walk','THOS Body',0),
    ('pcm_format','ghc-family-pcm-format-arithmetic','THOS Body',0),
    ('pcm_frames','ghc-family-pcm-frame-boundary','THOS Body',0),
    ('sample_time','ghc-family-sample-time-rational','GMUT Mind',1),
    ('pcm_range','ghc-family-pcm-integer-range','GMUT Mind',1),
    ('channel_permutation','ghc-family-audio-channel-permutation','THOS Body',2),
    ('edit_intervals','ghc-family-audio-edit-intervals','THOS Body',2),
    ('segment_binding','ghc-family-audio-segment-binding','Freed ID and CBR Heart',3),
    ('restoration_claim','ghc-family-restoration-claim-evidence','Freed ID and CBR Heart',3),
    ('disclosure_gate','ghc-family-audio-disclosure-reservations','Freed ID and CBR Heart',3),
]
PRACTICES = ['synthetic PCM container integrity reviewer','rational sample-timeline registrar',
             'audio edit provenance reviewer','accessible audio evidence documentation reviewer']
RUNNERS = [
    ('ghc_family_pcm_container_runner.py',['riff_chunks','pcm_format']),
    ('ghc_family_pcm_timeline_runner.py',['pcm_frames','sample_time']),
    ('ghc_family_pcm_edit_runner.py',['pcm_range','channel_permutation']),
    ('ghc_family_pcm_byte_binding_runner.py',['edit_intervals','segment_binding']),
    ('ghc_family_pcm_claim_runner.py',['restoration_claim','disclosure_gate']),
]
SOURCES = [
    {'source_id':'microsoft-riff','status':'stable','url':'https://learn.microsoft.com/en-us/windows/win32/xaudio2/resource-interchange-file-format--riff-','use':'RIFF envelope size, FOURCC, chunk size, and WORD padding; no audio content interpretation.'},
    {'source_id':'microsoft-waveformatex','status':'stable','url':'https://learn.microsoft.com/en-us/windows/win32/api/mmeapi/ns-mmeapi-waveformatex','use':'Classic PCM block alignment and byte-rate arithmetic; extended and compressed formats remain outside this profile.'},
    {'source_id':'python-wave','status':'current','url':'https://docs.python.org/3.12/library/wave.html','use':'A separate local parser for synthetic uncompressed PCM fixtures; not independent reproduction.'},
    {'source_id':'soundfile','status':'current','url':'https://pypi.org/project/soundfile/0.14.0/','use':'Pinned package metadata and bounded in-memory PCM readback.'},
    {'source_id':'construct','status':'current','url':'https://pypi.org/project/construct/2.10.70/','use':'A declarative binary header parser with a truncated-input witness.'},
    {'source_id':'bitstruct','status':'current','url':'https://pypi.org/project/bitstruct/8.23.0/','use':'Signed integer packing and explicit range rejection.'},
    {'source_id':'construct-docs','status':'stable','url':'https://construct.readthedocs.io/en/latest/intro.html','use':'Parser/build interfaces, checked against the installed pinned implementation in x2.'},
    {'source_id':'bitstruct-docs','status':'watch','url':'https://bitstruct.readthedocs.io/en/latest/','use':'Interface reference displays version 8.17.0; pinned 8.23.0 behavior must be witnessed.'},
    {'source_id':'soundfile-docs','status':'watch','url':'https://python-soundfile.readthedocs.io/en/0.13.1/','use':'Documentation redirect is older than pinned 0.14.0; no silent version-equivalence claim.'},
]

def dump(path, value):
    target=ROOT/path
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(value,indent=2,ensure_ascii=False,sort_keys=True)+'\n',encoding='utf-8',newline='\n')

def git(*args):
    return subprocess.check_output(['git','-C',str(ROOT),*args],text=True).strip()

def blob(path):
    return subprocess.check_output(['git','-C',str(ROOT),'show',SOURCE+':'+path])

def method_ledger():
    faults=[
        ('001','The combined baton window and reference listing exceeded the model output budget.','Read the complete catalogue with byte-reconstructable repeated templates and every substitution; check the committed digest.'),
        ('002','The first hundred-entry lossless catalogue display exceeded the wrapper output limit.','Retain the complete result and display the missing rows in a bounded follow-up without executing predecessor validation.'),
        ('003','Combined release, authorization, and roster output was truncated.','Read the release separately and display complete compact JSON in retained bounded slices.'),
        ('004','The release profile was requested from a nonexistent index-reference filename.','Use the observed workflow-profile-20260906.json in the owned-bundle-rotation package.'),
        ('005','An unfiltered parent-task read mixed current and older phase material and exceeded the output bound.','Decode the retained native envelope and select only current v687-v7 messages; preserve phase partitions.'),
        ('006','A compact-JSON payload digest did not match the canonical receipt hash domain.','Read the sealed serializer and hash sorted indented UTF-8 JSON with its final LF; the expected payload digest then matches.'),
        ('008','Sparse setup after no-checkout left the new worktree index empty and exposed staged deletions.','Verify the empty owner worktree, populate its index from immutable HEAD with read-tree, and check index-tree equality plus clean sparse state.'),
    ]
    methods=[];witnesses=[];events=[]
    for suffix,failure,recovery in faults:
        mid='TR6878-START-M'+suffix;nid='TR6878-START-N'+suffix
        methods.append({'method_id':mid,'title':failure,'failure_signature':failure,
            'trigger_preconditions':['Thalen v687-v8 startup','bounded source or owner setup'],
            'privacy_class':'sanitized_public','approval_class':'safe_now','candidate_workaround':recovery,
            'validation_witness_ids':[mid+'-FAIL',mid+'-PASS'],'recurrence_guard':recovery,
            'rollback':'Stop the affected operation and retain all prior evidence. No source or sibling mutation.',
            'recommendation_state':'preferred','supersedes':[],'protected_gates':GATES,
            'retained_negative_ids':[nid],'scope_boundary':'Startup dependency only; zero proposal or external credit.'})
        for result,observed in [('fail',failure),('pass',recovery)]:
            witnesses.append({'witness_id':mid+'-'+result.upper(),'method_id':mid,'procedure':'Bounded startup read or index setup',
                'scope':'Thalen startup dependency','expected':'Complete attributable result within exact source and owner scope',
                'observed':observed,'result':result,'same_owner_only':True,'independent_reproduction':False,
                'retained_negative_ids':[nid],'boundary':'A corrected pass never erases the failed witness.'})
        for a,b in [('observed','candidate'),('candidate','validated'),('validated','preferred')]:events.append({'method_id':mid,'from':a,'to':b})
    return {'schema':'ghc.family.method-flow-state.v1','phase':'v687-v8','owner':'Thalen Reed',
            'identity_boundary':BOUNDARY,'execution_authority':'owner_self_scoped_delta','source_commit':SOURCE,
            'final_commit':None,'methods':methods,'witnesses':witnesses,'state_events':events,'recommendations':[],
            'counts':{'methods':len(methods),'failed_witnesses':len(methods),'passing_witnesses':len(methods),'witnesses':len(witnesses)},
            'boundary':'Startup-only evidence; x2 has not begun. All original failures retain zero success credit.'}

def overview():
    pages=[
        ('Planning authority and source',
         'Thalen Reed owns solo Trinity Mandala v687-v8. The relational role is keeper of clear handoffs. '
         'The hope is that each successor receives evidence they can inspect and limits they can trust. '
         'Optional they/them pronouns and every family term remain working language only. This phase begins '
         'from Orin Thale exact final '+SOURCE+'. The committed 38,819-word baton was read through its EOF '
         'using full prose and a byte-reconstructable rendering of its repetitive catalogue. All 200 catalogue '
         'entries were examined. The baton hash, external canonical receipt hash, exact payload serializer, '
         'four direct source-to-final parents, clean source state, typed divergence, and fresh four-way equality '
         'were checked. All 689 manifest bindings plus fifteen declared lifecycle exclusions were read and '
         'reconciled at their named commits. This is source-integrity checking, with no inherited canonical replay. '
         'The inherited proposal total is 15,230. The 200 selected source reviews carry zero Thalen novelty '
         'and completion credit. Their titles sometimes name spectral behavior absent from their actual input '
         'fields; their original dispositions and evidence remain preserved. A source description mentions two '
         'final failures, whereas its authoritative retained register contains three. The register is retained '
         'without silently changing sealed totals. The 6 September release and current explicit activation '
         'control the thirty-seat route. Older installed roster files are historical snapshots, even when their '
         'structure validates. No current name or phase is inferred from those old cursors. Only Thalen is '
         'activated by this assignment; the future Liora Venn v688-v1 edge remains behind Thalen terminal gates.'),
        ('Concrete prospective work and its limits',
         'The priority pillar is THOS Body through synthetic PCM container and evidence work. GMUT Mind '
         'retains exact sample-time and integer-range representations; neither representation is a physical '
         'observation or a theory test. Freed ID and CBR Heart retain byte provenance, disclosure reservations, '
         'affected-party review needs, and the separation of synthetic claims from real authority. Four bounded '
         'practice lenses organize the fixtures. The first examines RIFF envelopes and classic PCM metadata. '
         'The second records sample indices and exact rational times without float coercion or rounding. '
         'The third examines channel permutations and half-open edit maps while retaining the source. '
         'The fourth records digest claims, restoration comparison limitations, and authority reservations. '
         'Each of the 200 proposals freezes its own concrete input and entire expected output. These are '
         'definitions for later tests, not observed passes. Examples include a missing odd-chunk padding byte, '
         'a contradictory PCM byte rate, a fractional inverse sample index, Boolean values presented as '
         'integers, overlapping edit spans, and a claimed digest over the wrong byte interval. Restoration '
         'metrics can describe a finite synthetic difference but cannot establish listening quality. A '
         'self-declared rights or review field cannot authorize publication or establish independent review. '
         'The portfolio plans 300 safe procedures, 250 candidate challenges, and exactly 300 additive '
         'CLEAN/FIX/REFINE procedures. These are traceable workflow tasks tied to a bounded fixture set; '
         'reuse of a fixture does not multiply scientific evidence or independent witnesses. Fifty exact '
         'packets and thirty blocked packets remain unexecuted. Three packages are planned with exact '
         'versions and verified wheel hashes. Downloading those wheels is preparation only. No isolated '
         'environment or package execution is claimed in x1. Documentation version drift is explicitly '
         'marked watch and must be checked against the pinned packages during x2.'),
        ('Lifecycle, recovery, and terminal contract',
         'This x1 freeze contains planning records, input fixtures, acceptance definitions, source checks, '
         'and startup failures. It contains no PCM runtime implementation, x2 execution results, global '
         'promotions, package-installation claim, or successor-delivery claim. It must be committed and '
         'pushed as a direct child of the immutable source. X2 may begin only after clean local, upstream, '
         'tracking, and fresh live-remote equality, with integer zero ahead and zero behind. The owner '
         'lane is a fresh additive D-drive sparse worktree. Its first empty-index setup failure remains '
         'recorded with the later exact index reconstruction as a separate witness. No deletion was '
         'committed and no sibling worktree was changed. The scope stays below 2,000 owner files and each '
         'document stays below 100,000 words. The intended ordinary history is source, x1, evidence, and '
         'final, with at most two additive correction commits if a real dependency failure justifies them. '
         'No merge, amendment, reset, force push, or historical rewrite is part of the plan. The final '
         'aggregate must include every changed path rather than filtering out unexpected paths. It must '
         'verify exact lifecycle manifests, strict JSON with duplicate-key rejection, five-class privacy '
         'adjudication, bounded changed-code security, byte parity for curated promotions, source preservation, '
         'staged allowlists, and the exact pushed head. Its exclusive external latch is created at most once. '
         'A success is never replayed; a failure keeps zero canonical success credit. All safe and candidate '
         'tasks must be executed or truthfully kept at an evidence or authority boundary. Real participants, '
         'production identity keys, legal interpretation, professional competence, cultural decisions, Maori '
         'wording and data governance, tikanga, taonga, matauranga, and Maori authority remain exact-gated. '
         'Maori concepts remain under Maori authority. The terminal verdict remains NOT_READY_FOR_STAGE_20. '
         'Only after the full owner terminal gate may the exact existing Liora task be resolved, immediately '
         'reread, and sent one compact file-backed activation if every live guard permits it. No precontact, '
         'replacement, duplicate, fork, collaboration subagent, or resend is authorized.'),
    ]
    esc=lambda s:s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    return '<!doctype html>\n<html lang="en"><meta charset="utf-8"><title>Thalen v687-v8 planning overview</title><style>@page{size:A4;margin:18mm}body{font:14px/1.6 system-ui;max-width:850px;margin:auto}section{break-after:page;min-height:250mm}section:last-child{break-after:auto}</style><main>'+''.join('<section class="page"><h1>'+esc(h)+'</h1><p>'+esc(t)+'</p><p>'+esc(BOUNDARY)+'</p></section>' for h,t in pages)+'</main></html>\n'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--wheel-plan',type=Path,required=True);ap.add_argument('--skill-root',type=Path,required=True);a=ap.parse_args()
    assert git('rev-parse','HEAD')==SOURCE and git('branch','--show-current')==BRANCH
    assert not (ROOT/BASE/'x2').exists()
    from ghc_family_thalen_reed_v687_v8_fixtures import build_cases
    cases=build_cases(); opmeta={o:(s,p,practice) for o,s,p,practice in OPS}
    for c in cases:
        skill,pillar,practice=opmeta[c['operation']]
        c.update({'schema':'ghc.family.frozen-pcm-contract.v1','source_status':'current','source_kind':'synthetic',
            'pillar':pillar,'practice':PRACTICES[practice],'approval_class':'safe_now','execution_lane':'x2_only',
            'hypothesis':'The declared bounded operation preserves the stated input and returns the complete frozen output for this concrete case.',
            'null_or_failure_condition':'Any wrong field, type, omitted value, unexpected authority promotion, or input mutation fails this contract.',
            'falsifier_or_acceptance_gate':'Type-sensitive equality of the complete output plus unchanged input, with all declared altered-output candidates rejected.',
            'concrete_artifact':str(BASE/'x2/contract-results.json').replace('\\','/'),
            'rollback_or_recovery':'Retain the original fixture and failure; correct only the owner implementation or leave the evidence or authority gate open.',
            'protected_gates':GATES,'skill':skill,'external_credit':False})
    dump(BASE/'x1/identity.json',{'schema':'ghc.family.relational-induction.v1','name':'Thalen Reed','role':'keeper of clear handoffs','hope':'that each successor receives evidence they can inspect and limits they can trust','pronouns':'they/them','active_title_collision_count':0,'archived_title_collision_count':0,'task_renamed':True,'seat':10,'boundary':BOUNDARY})
    dump(BASE/'x1/new-proposals.json',{'schema':'ghc.family.proposal-freeze.v1','chain_before':15230,'chain_after':15430,'count':200,'planning_only':True,'proposals':cases})
    inherited=json.loads(blob('docs/orin-thale/v687-v7/x1/new-proposals.json'))['proposals']
    reviews=[]
    for p in inherited:
        reviews.append({'proposal_id':p['proposal_id'],'source':SOURCE,'source_definition_sha256':hashlib.sha256(json.dumps(p,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest(),
            'title':p['title'],'operation':p['operation'],'inherited_expected_disposition':p['expected_disposition'],
            'review':'Retain the finite record contract. Its ordinal-derived output does not exercise the spectral behavior named by the descriptive title. No scientific or current-owner completion is inferred.',
            'new_owner_novelty_credit':0,'new_owner_completion_credit':0})
    dump(BASE/'x1/inherited-review.json',{'schema':'ghc.family.inherited-review.v1','source':SOURCE,'count':200,'reviews':reviews,'source_outcomes_preserved':{'completed':125,'represented':39,'open_gap':20,'exact_gate':16}})
    dump(BASE/'x1/novelty-review.json',{'schema':'ghc.family.bounded-novelty-screen.v1','scope':'Exact inherited Orin proposal inputs and chosen owner tool names; not a global novelty claim.',
         'inherited_review_count':200,'new_count':200,'exact_input_collisions':0,'global_skill_name_collisions':[s for _,s,_,_ in OPS if (a.skill_root/s).exists()],
         'distinction':'New contracts inspect actual RIFF bytes, PCM fields, frame indices, integer samples, edit spans, digests, metric comparability, and explicit disclosure actions. No contract decides from an ordinal or proposal identifier.',
         'inherited_seed':'Audio restoration uncertainty registrar accepted as a bounded synthetic documentation practice; independent proposal development remains required.'})
    tasks={k:[] for k in ['safe_now','candidates','clean_fix_refine','exact_packets','blocked_packets']}
    def task(category,ident,pid,procedure,expected='completed',**extra):tasks[category].append({'packet_id':ident,'proposal_ref':pid,'procedure':procedure,'expected_execution_disposition':expected,'executed':False,**extra})
    for c in cases:task('safe_now','TR6878-S-'+c['proposal_id'],c['proposal_id'],'complete_frozen_output')
    for c in cases[:100]:task('safe_now','TR6878-S-PRESERVE-'+c['proposal_id'],c['proposal_id'],'input_unchanged')
    mutation_names=['missing_accepted','accepted_type','extra_authority','value_replaced','external_credit_promoted']
    for c in cases[::4]:
        for mutation in mutation_names:task('candidates','TR6878-C-'+c['proposal_id']+'-'+mutation,c['proposal_id'],'altered_output_rejection',mutation=mutation,original_candidate_success_credit=0)
    for c in cases[:100]:
        for action in ['canonical_json_roundtrip','definition_digest_binding','stable_identifier_uniqueness']:
            task('clean_fix_refine','TR6878-CFR-'+c['proposal_id']+'-'+action,c['proposal_id'],action,additive_only=True)
    gates=['real_audio_custody','speaker_consent','rights_release','production_identity','maori_authority']
    for i in range(50):task('exact_packets',f'TR6878-E{i+1:03d}',cases[150+i]['proposal_id'],'reserved_external_action','exact_gate',missing_prerequisite=gates[i//10],protected_gates=GATES)
    gaps=['real_recording','calibration_record','registered_listening_protocol']
    for i in range(30):task('blocked_packets',f'TR6878-B{i+1:03d}',cases[170+i]['proposal_id'],'absent_external_evidence','open_gap',missing_prerequisite=gaps[i//10],protected_gates=GATES)
    tasks.update({'schema':'ghc.family.portfolio-plan.v1','destructive_cleanup_planned':False,'execution_started':False,'witness_reuse_rule':'Tasks are distinct declared procedures, not independent scientific witnesses. A referenced result is not counted twice as a new empirical observation.'})
    dump(BASE/'x1/portfolio-plan.json',tasks)
    dump(BASE/'x1/skill-runner-plan.json',{'schema':'ghc.family.skill-runner-plan.v1','skills':[{'name':s,'operation':o,'build_in_x2':True} for o,s,_,_ in OPS],
        'runners':[{'name':n,'operations':ops,'build_in_x2':True} for n,ops in RUNNERS],
        'core':'ghc_family_pcm_evidence_core.py','global_promotions':{'skills':10,'runners':5,'overwrite':False,'byte_parity_required':True},'source_compatibility':'All prior entrypoints remain untouched.'})
    wheel_plan=json.loads(a.wheel_plan.read_text(encoding='utf-8'));assert len(wheel_plan['wheels'])==7 and sum(w['direct'] for w in wheel_plan['wheels'])==3
    dump(BASE/'x1/wheel-plan.json',wheel_plan)
    (ROOT/BASE/'x1/requirements.lock').write_text(''.join(w['name']+'=='+w['version']+' --hash=sha256:'+w['sha256']+'\n' for w in wheel_plan['wheels']),encoding='utf-8',newline='\n')
    dump(BASE/'x1/package-plan.json',{'schema':'ghc.family.package-plan.v1','direct_packages':{'soundfile':'0.14.0','construct':'2.10.70','bitstruct':'8.23.0'},'new_environment_in_x2':True,'installed':False,
        'platform':'CPython 3.12 Windows AMD64','hash_lock':'x1/requirements.lock','wheel_count':7,'network_install':False,'wheel_only':True,'host_python_mutation':False,
        'smokes':[{'name':'soundfile','positive':'In-memory PCM16 WAVE readback matches independently declared samples and metadata.','adverse':'A truncated non-WAVE byte fixture is rejected.'},
                  {'name':'construct','positive':'Declarative RIFF header parse matches the frozen twelve-byte header.','adverse':'A short header raises the package stream error.'},
                  {'name':'bitstruct','positive':'Signed sixteen-bit endpoint values pack and unpack exactly.','adverse':'A positive value above the signed limit is rejected.'}],
        'rollback':'Stop selecting this isolated owner environment and retain its lock, wheels, and failed witnesses. No host changes or deletion.'})
    profile=json.loads((a.skill_root/'ghc-family-owned-bundle-rotation/references/workflow-profile-20260906.json').read_text())
    dump(BASE/'x1/release-profile.json',profile)
    dump(BASE/'x1/route-plan.json',{'schema':'ghc.family.owner-route-plan.v1','owner':'Thalen Reed','phase':'v687-v8','endpoint_kind':'main_task','seat_placeholder':'future-sibling-10-self-chosen','source_owner':'Orin Thale','source':SOURCE,
        'authority':'Hamish current seat-10 activation and 6 September thirty-seat release','next_owner':'Liora Venn','next_phase':'v688-v1','state':'PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED','message_count':0,'precontacted':False,'create_task':False,'fork':False,'subagent':False,
        'terminal_guards':['exact_final_canonical_success','clean_pushed_four_way_equal','current_authority','unique_exact_existing_title','immediate_recipient_reread','no_duplicate_pause_redirect','usage_available','privacy_evidence_safety_authority','one_acknowledged_send_no_resend']})
    dump(BASE/'x1/deck-plan.json',{'schema':'ghc.family.four-tier-deck-plan.v1','tiers':['owner','pillar','practice','task'],'owner_cards':1,'pillar_cards':3,'practice_cards':4,'task_cards':200,'practices':PRACTICES,
        'primary_pillar':'THOS Body','hierarchy_note':'Each practice has exactly one pillar parent; a cross-pillar relationship is a content reference, never a second parent.',
        'practice_parents':['THOS Body','GMUT Mind','THOS Body','Freed ID and CBR Heart'],'modular_sections':13,'cache_effect_claimed':False,'build_only_after_x1_equality':True})
    ideas=['RIFF nested-list depth budgets','RF64 ds64 size precedence','WAVE extensible valid-bit boundaries','Broadcast Wave time-reference arithmetic','Audio cue-point relocation maps','Loudness metadata missingness','Dither provenance without quality claims','Restoration parameter lineage','Consent expiry with retained source views','Accessible transcript timing reservations']
    dump(BASE/'x1/successor-ideas.json',{'schema':'ghc.family.successor-ideas.v1','owner':'Liora Venn','phase':'v688-v1','skill_ideas':[{'title':x,'credit':0,'independent_review_required':True} for x in ideas],
        'runner_ideas':[{'title':x+' bounded runner','credit':0,'not_built':True} for x in ideas],
        'practice_recommendation':'synthetic audiovisual timing and access registrar','recommendation_count':1,'precontacted':False})
    dump(BASE/'x1/source-ledger.json',{'schema':'ghc.family.primary-source-ledger.v1','entries':SOURCES,'citations_are_observations':False,'real_rows':0,'web_queries_used':2,'web_query_ceiling':1000})
    dump(BASE/'x1/method-flow/ledger.json',method_ledger())
    dump(BASE/'x1/source-verification.json',{'schema':'ghc.family.source-verification.v1','source':SOURCE,'source_branch':'codex/GHC-Family/orin-thale-v687-v7-full-tools','baton_sha256':'66c083032ec373ba12b1afe6d44a9dc5b6ad07d4bd2d7103977e7053ff2c2cd4','baton_words':38819,'baton_bytes':356642,'baton_eof_read':True,
        'baton_read_method':'Full prose plus a lossless two-template rendering with every one of 200 input/output substitutions, reconstructed byte-for-byte through EOF.',
        'source_receipt_sha256':'ddfbf1dab87b609dffe360f50236145685c91c61e344e10f1646c0d43c3295ae','source_payload_sha256':'7ffd314417061583aeca715385e0b5fbcf1c45bafad0884891a70f74f12808ab','payload_domain':'sorted indent-two ensure_ascii-false JSON plus one LF','source_canonical_replayed':False,
        'source_clean':True,'source_divergence':[0,0],'source_four_way_equal':True,'direct_single_parent_commits':4,'source_merges':0,'manifest_bindings':689,'manifest_exclusions':15,'manifest_mismatches':0,
        'inherited_descriptor_correction':'The final register has three final failures; the baton mentions two. Retain the three explicit records without changing sealed totals.',
        'later_orin_external_display_faults':'Retained in source task summary as external zero-credit evidence; no unverified arithmetic folded into repository counts.'})
    required=['ghc-family-index','ghc-family-main-task-induction','ghc-family-d-first-structured-evidence-toolchain','ghc-family-lifecycle-test-isolator','ghc-family-privacy-candidate-classifier','ghc-family-staged-surface-allowlist','ghc-family-owner-scope-canonical','ghc-family-canonical-success-latch','freed-id-four-tier-deck','ghc-family-workflow-plan-refinement','ghc-family-reflection-remaster','ghc-family-method-flow-state','ghc-drive-bank-guardian','ghc-family-meta-tool-box','ghc-family-roster-check','ghc-freed-id-flashcards','ghc-family-owned-bundle-rotation','.system/skill-creator']
    dump(BASE/'x1/reading-receipt.json',{'schema':'ghc.family.required-reading.v1','source':SOURCE,'skill_entrypoints':[{'name':n,'sha256':hashlib.sha256((a.skill_root/n/'SKILL.md').read_bytes()).hexdigest(),'eof_read':True} for n in required],
        'references_read':['hamish-release-20260906.md','workflow-profile-20260906.json','routing-precedence.md','current-state.json','current-roster.json','roster-state-schema.md','method-flow schema.md','workflow-plan-schema.md','decision-schema.md','deck-schema.md','flashcard-reflection.md','freed-id-flashcards.md','workflow.md','failure-shields.md','catalogue-schema.md','rowan-v685-v6-r2-authorized-workflow.md'],
        'source_phase_local_skills_read':10,'source_lifecycle_manifests_read':5,'historical_roster_structurally_valid':True,'historical_cursor_used_for_current_ownership':False})
    dump(BASE/'x1/scope-budget.json',{'schema':'ghc.family.owner-scope-budget.v1','primary_drive':'D','essential_global_skill_drive':'C','c_free_gb':18.77,'d_free_gb':465.48,'sparse_before_materialization':True,'materialized_source_files':0,'owner_file_ceiling':1999,
        'document_word_ceiling':100000,'baton_word_range':[10000,100000],'commit_cap':{'x1':1,'x2_and_final':4,'total':5},'ordinary_lifecycle':['source','x1','evidence','final'],'correction_commits':'Only additive corrections justified by actual retained failures within the total ceiling.',
        'canonical_invocation_budget':1,'canonical_replay':False,'validation_scope':'owner_self_scoped_delta','sibling_lane_mutation':False,'source_lanes_read_only':True})
    dump(BASE/'x1/validation-contract.json',{'schema':'ghc.family.owner-validation-plan.v1','phase':'v687-v8','planning_checks':['source_anchors','200_distinct_inputs','200_zero_credit_reviews','release_portfolio_counts','no_x2','no_observed_outcomes','package_hash_plan','authority_boundaries','exact_owner_paths','strict_json','privacy','manifest','diff_hygiene'],
        'x2_checks':['200_full_output_matches','input_preservation','250_preregistered_altered_outputs','300_CFR_procedures','3_package_positive_and_adverse_smokes','10_skills_quick_validate_and_use','5_runners_use','four_tier_deck','promotion_parity'],
        'canonical_checks':['all_delta_paths_owner_allowed','exact_direct_ancestry','zero_merges','one_final_parent','immutable_x1','immutable_evidence','manifest_arithmetic','strict_JSON_duplicate_and_constant_refusal','five_class_privacy_adjudication','bounded_changed_code_security','selected_owner_tests','document_caps','baton_EOF_and_digest','global_parity','clean','typed_zero_divergence','fresh_four_way_equality'],
        'no_predecessor_execution':True,'external_exclusive_latch':True,'terminal_verdict':'NOT_READY_FOR_STAGE_20','protected_gates':GATES})
    dump(BASE/'x1/phase-truth.json',{'schema':'ghc.family.phase-truth.v687.v8.x1','owner':'Thalen Reed','phase':'v687-v8','state':'PLANNING_ONLY_FREEZE','source':SOURCE,'proposal_count':200,'frozen_chain_total':15430,'x2_started':False,'x2_completion_credit':0,'canonical_invocations':0,'successor_contacted':False,'terminal_verdict':'NOT_READY_FOR_STAGE_20'})
    (ROOT/BASE/'x1/integrated-overview.html').write_text(overview(),encoding='utf-8',newline='\n')
    print(json.dumps({'state':'PLANNING_ONLY_MATERIALIZED','proposal_count':200,'portfolio':{k:len(tasks[k]) for k in ['safe_now','candidates','clean_fix_refine','exact_packets','blocked_packets']},'no_x2':True}))

if __name__=='__main__':main()
