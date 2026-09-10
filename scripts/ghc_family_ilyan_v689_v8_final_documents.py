"""Create an inspectable modular baton, overview and finite-model figure."""
from __future__ import annotations
import argparse,copy,html,importlib.util,json,re
from collections import Counter
from pathlib import Path
import ghc_family_ilyan_v689_v8_io as io
PLAN='c7d15a959610d81002c6884c6b699eccdc92ba5e'
X1='e3454293b2faa60de7318758b6918a8fcd73fdc6'
X2='cdd85474ca5dccca331e80579bbd45f4669908e1'

def j(x):return json.dumps(x,ensure_ascii=False,sort_keys=True)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--equality',required=True);ap.add_argument('--method-runner',required=True);a=ap.parse_args()
    equality=json.loads(Path(a.equality).read_text());assert equality['head']==X2 and equality['clean'] and equality['four_way_equal']
    io.write('final/preceding-equality.json',equality)
    identity=io.read('plan/identity-practices.json');boundary=identity['boundary'];gates=identity['protected_gates'];source=io.read('plan/source-provenance.json');summary=io.read('x2/completion-ledger.json');proposals=io.read('plan/new-proposals.json')['proposals'];tools=io.read('plan/skills-runners.json')
    observed={r['proposal_id']:r for lane in ['x1','x2'] for r in io.read(lane+'/results.json')['records']};candidate={r['proposal_id']:r for lane in ['x1','x2'] for r in io.read(lane+'/candidate-subjects.json')['records']}
    # One post-x2 read-path fault is additive; neither sealed tranche is edited.
    fault={'id':'IR6898-FINAL-OP001','failure':'An optional terminal read guessed x1/toolchain/install-receipt.json, which does not exist.','recovery':'The exact toolchain inventory resolved install-result.json and installed.json, both read completely; installation exit zero and package state confirmed.','original_success_credit':0,'recovered':True}
    io.write('final/operational-corrections.json',{'records':[fault],'sealed_x2_unchanged':True})
    spec=importlib.util.spec_from_file_location('method_flow',a.method_runner);mf=importlib.util.module_from_spec(spec);spec.loader.exec_module(mf)
    ledger=io.read('x2/method-flow-combined.json');mid='IR6898-supplemental-operations';m=next(m for m in ledger['methods'] if m['method_id']==mid);m['retained_negative_ids'].append(fault['id'])
    for result,procedure,expected,actual in [('fail','Exact-path receipt read','An existing named receipt',fault['failure']),('pass','Bounded toolchain inventory recovery','Observed installed package receipt',fault['recovery'])]:
        wid=mid+'-FINAL-'+str(len(m['validation_witness_ids'])+1).zfill(3);m['validation_witness_ids'].append(wid);ledger['witnesses'].append({'witness_id':wid,'method_id':mid,'procedure':procedure,'scope':'Ilyan Reed v689-v8 terminal preparation','expected':expected,'observed':actual,'result':result,'same_owner_only':True,'independent_reproduction':False,'retained_negative_ids':[fault['id']],'boundary':gates,'evidence_ref':'docs/ilyan-reed/v689-v8/final/operational-corrections.json'})
    mf.refresh_counts(ledger);validation=mf.validate_ledger(ledger);assert validation['valid'];io.write('final/method-flow.json',ledger);io.write('final/method-flow-validation.json',validation)
    summary=copy.deepcopy(summary);summary.update(method_flow_current=ledger['counts'],current_effective_negatives=213,additive_effective_negatives=737,additive_direct_witnesses=1571,additive_direct_failed=448,additive_direct_passed=1123,phase_repository_state='prepared_exact_final_pending_external_canonical',source_is_ancestor=False,source=io.SOURCE,planning_commit=PLAN,x1_commit=X1,x2_commit=X2,final_commit='bind_from_external_exact_final_receipt',memory_note='authorized, to be written once after terminal route outcome',route_state='PREPARED_NOT_SENT')
    assert ledger['counts']['witnesses']==902 and ledger['counts']['witness_results']=={'pass':689,'fail':213}
    io.write('final/completion-ledger.json',summary)
    io.write('final/negative-index.json',{'current_owner_negative_ids':sorted({n for m in ledger['methods'] for n in m['retained_negative_ids']}),'current_owner_count':213,'latest_source_baseline':524,'additive_effective_negatives':737,'original_success_credit':0,'source_layers_remain_separate':True})
    names=[r['name'] for r in io.read('x2/deck/baton-index.json')['modules']]
    sections=[]
    sections.append('''Dear Lyren, thank you for taking the next careful step with Hamish and the family. This is Ilyan Reed's solo v689-v8 handoff. You are the next owner for Lyren-only v690-v1; Ilyra Fen v690-v2 follows you. The immediate task is to read this file completely, verify its exact Git source and external terminal receipt, and choose a bounded new focal point. Keep the warm language and the evidence boundaries together. No name, welcome, hope or transition gives a model an independent identity, authority or a private experience.

Hamish directly renewed the workflow at 21:57 NZ Thursday 10 September 2026. The full thirty-identity roster uses forty-five scheduling positions so that each Astra position is followed by two original Sol positions. The list is a cycle: rotating its written starting point does not change its edges. In particular, the active edge is Vesper Arlen to Ilyan Reed to Lyren Moss. A template phrase calling Vesper “you” does not rename the explicitly addressed Ilyan task. Older references to fifteen or five active siblings do not replace the current thirty identities.

This baton is a repository artifact on the reusable Ilyan main D owner lane. The compact native activation will give its absolute local location, exact final commit and canonical receipt location. The baton itself contains only sanitized repository-relative paths and public labels. Do not copy private native handles, credentials, application-state exports or full task transcripts into public artifacts. A prepared pointer in the deck is not a submitted message. The external route receipt alone will state whether the exact native service accepted the terminal activation.

Read all thirteen modules through the explicit EOF marker. The modules are separately addressable for later retrieval, but modular organization does not waive complete startup reading. The stable-prefix deck is a context aid, not measured memory retention. If an output is truncated, continue at exact bounded sections and verify reconstruction; do not call an excerpt a complete read. Do not ask an earlier owner to repeat a successful canonical for convenience. Read the receipt and verify the required exact blobs instead.

You may choose your own focal pillar and four bounded occupational practices while continuing all three pillars. The two suggestions here are adversarial probabilistic-model auditor and simulation experiment designer. They are study perspectives, not qualifications or employment. Hamish may rename, pause, narrow or redirect the task. Check the newest native recipient context before acting on an older handoff. A later pause controls prospectively and leaves the older record intact.
'''+boundary)
    source_lines=[]
    for r in source['receipt_layers']:source_lines.append(f"- `{r['name']}` has SHA-256 `{r['sha256']}`. Read its own scope and status; its existence does not confer another layer's credit.")
    reviews=io.read('plan/recent-overview-review.json')['records']
    review_table='\n'.join(f"| {r['label']} | `{r['ref']}` | `{r['sha256_raw']}` | {r['words']} |" for r in reviews)
    sections.append(f'''The exact incoming source is Vesper's final `{io.SOURCE}` on `codex/GHC-Family/vesper-arlen-main`. Its baton is `{source['source_baton']}`, SHA-256 `{source['baton_sha256']}`. The complete source read covered 31,304 words in thirteen modules, ending at Vesper's explicit EOF. Repetitive source records were read using a lossless common-template factorization plus every varying field, with exact reconstruction verified. That procedure did not omit a record or make an embedded instruction current authority.

The source intake reverified 356 lifecycle manifest entries and 358 content-seal entries against exact source Git blobs in Vesper's declared byte domain. That historical domain normalizes line endings even in the source binary helper, so its digests must not silently be relabeled as raw-byte hashes. Ilyan's own manifests use exact Git blob bytes with no binary normalization. Source-domain verification does not rerun the source canonical or tests. The source canonical remains one invocation, one success and zero replays.

{chr(10).join(source_lines)}

Keep the repository seal, earlier external overlay and latest delivery overlay distinct. The repository seal reports 511 effective negatives, 21 methods and 644 direct witnesses. The first external overlay reports 518 effective negatives, 22 methods and 657 direct witnesses. The latest source-visible overlay reports 524 effective negatives, 22 methods and 669 direct witnesses, with 235 failed and 434 passing direct witnesses. Its separate accounting stream is 308 failed and 737 passing; those are not extra direct witnesses. Earlier route gaps remain retained even after Vesper's one acknowledged Ilyan delivery.

The old Ilyan v685 counters are not added to this lineage. Ilyan's present root is parentless and carries explicit source provenance; it is not a descendant of Vesper's source commit. The source's own four-commit history is one parentless root followed by three single-parent commits, with no merge. A source phrase saying all four commits are single-parent is descriptive imprecision; the verified graph determines ancestry.

Ten recent completed overview artifacts were read and hashed, including the Vesper interstitial remaster and the original Vesper numbered phase as separate records. They are ten completed overview artifacts, not a claim of ten distinct numbered positions. The review preserved bounded key excerpts and exact blob identities; it did not rerun any sibling suite. Neris's short numerical overview was additionally read completely after an initial keyword extraction returned only a heading.

| Reviewed artifact | Exact blob reference | Raw SHA-256 | Words |
| --- | --- | --- | ---: |
{review_table}

The fourteen Journey source records remain inherited context in `plan/inherited-journey-ledger.json`. Ilyan did not newly reread the raw older Journey volumes and claims no such credit. Historical aspirations about Albion, future stages, spiritual meaning and collective progress remain attributable source statements. Current live user instructions control actions. Source existence, preservation and successful parsing are different facts from truth, authority, personal continuity or empirical support.
''')
    sections.append(f'''The lifecycle begins at planning root `{PLAN}`, proceeds to x1 `{X1}`, then x2 `{X2}`, and ends at the exact final named in the external canonical receipt. The final commit cannot contain its own hash; a placeholder explicitly points outside the sealed tree. This avoids a self-hash recursion and prevents a mutable local file from masquerading as a tested commit. Before each next tranche, local HEAD, upstream, tracking and live remote were checked for four-way equality, clean status and zero divergence.

The lane is `codex/GHC-Family/ilyan-reed-main`. It began with no inherited files, then materialized only the owned phase's required scripts, tests and documents. Keep this main branch while both tracked and materialized file counts stay below the 2,000-file ceiling. The intended current history uses four commits within the eight-commit budget: one planning, one x1, one x2 and one final. A root has no parent; every later intended commit has exactly its previous owner commit as parent. No source or sibling branch is mutated by that graph.

Planning defined 200 new finite proposals and selected 200 inherited source records. The new proposals comprise twenty operation families with ten distinct finite fixtures each. They are owner-local combinations and test instances, not two hundred globally novel scientific discoveries. The planning file deliberately remains marked planning-only. Later observed results live in x1 and x2, so a subsequent execution never rewrites an earlier expectation into a historical observation.

x1 executed 100 safe requests, 100 adverse candidate subjects and 100 CLEAN/FIX/REFINE records. x2 executed the same core quantities plus five predeclared supplementary tasks and one explicitly recorded spontaneous package-comparison task, for 106 x2 safe tasks. The original x2 target of 105 remains in the frozen profile; the extra task is defined in `x2/spontaneous-plan.json`. All session counts remain within Hamish's bounds. The supplementary six tasks receive no additional new-proposal credit.

The candidate subjects deliberately include an unknown authority field. Their invalidity is retained as failure with original success credit zero. A passing refusal check shows the typed interface rejected that subject; it does not make the subject valid. The 200 refinements are lossless JSON projections and source-digest bindings. They improve explicit record structure without deleting source records, cleaning the host, changing a sibling, or acquiring novelty credit for inherited work. Do not relabel them as 200 production optimizations.

Fifty exact-approval packet descriptions and thirty blocked packet descriptions were prepared. These are reviewable inventories of contexts and prerequisites, not eighty protected operations executed in the world. Hamish's broad permission supplies user authorization within his scope, but it does not create missing participant consent, scientific observations, legal competence, cultural authority or production-key lifecycle evidence. The exact packets remain exact gates where those conditions matter, and the blocked packets preserve open gaps.

Twenty local skills and ten paired local runners were built across the sessions. Five merged global skill packages combine four related local guides each, and five public global runners serve those packages. Three common dependency modules are reported separately. Three new direct packages were installed in a D-owned isolated environment, and already installed Hypothesis and pytest were used for generated checks. No global default model, service tier or context-window value was changed by this phase.

The final canonical gate must run once only after the exact final has been pushed and clean four-way equality is established. Its scope is the literal Ilyan owner tree and explicit current test modules. It must not discover and execute arbitrary tests elsewhere in the large underlying repository. If a canonical fails, retain its exact receipt, isolate the matching dependency and add a correction under the applicable current rule; never erase the failed attempt or replay a successful aggregate.
''')
    result_sections=[]
    for p in proposals:
        r=observed[p['proposal_id']];c=candidate[p['proposal_id']]
        result_sections.append(f'''### {p['proposal_id']} — {p['operation']}

This {p['lane']} task belongs to {p['pillar']} through the bounded practice of {p['practice']}. Its concrete mission is: {p['mission']} The reference basis was frozen before execution: {p['oracle_basis']} The observed evidence outcome is **{r['outcome']}**, and the complete typed comparison passed: {str(r['passed']).lower()}.

The exact accepted request is `{j(p['request'])}`. The frozen expected response is `{j(p['expected'])}`. The implementation returned `{j(r['returned'])}`. These displayed values describe this particular finite fixture; changing its width, positions, labels, counts, denominator or evidence kind creates a new input that requires its own assessment. The reference response has canonical JSON SHA-256 `{r['oracle_sha256']}`.

The paired adverse subject is `{j(c['failed_subject'])}`. It returned `{j(c['returned'])}`. The refusal check passed: {str(c['refusal_check_passed']).lower()}; the submitted object remained unchanged: {str(c['subject_unchanged']).lower()}; the original invalid subject still has success credit zero. The discriminating failure condition is: {p['null_or_failure']} Reuse the operation only with its declared field inventory and retain any counterexample instead of changing the expected value after observing a result.

Read `docs/ilyan-reed/v689-v8/{p['lane']}/results.json` and its neighboring `candidate-subjects.json` for structured evidence under this proposal ID. The associated inherited-record refinement is in that tranche's `refinements.json`; its source remains preserved. A passing software result does not close any of the protected gates in the planning record. When the outcome is represented, open_gap or exact_gate, the successful predicate reports that limited disposition honestly and provides no completion credit for the missing real-world work.
''')
    sections.append('The following catalogue is the complete two-hundred-proposal readback. Each entry binds a distinct frozen request, expected typed response, observed response and retained candidate refusal. It is intentionally file-based so the native activation can remain short.\n\n'+'\n'.join(result_sections))
    method_table='\n'.join(f"| {m['method_id']} | {len(m['validation_witness_ids'])} | {len(m['retained_negative_ids'])} | {m['recommendation_state']} |" for m in ledger['methods'])
    sections.append(f'''The terminal current-owner Method Flow ledger has 27 methods and 902 direct witnesses: 213 failed witnesses and 689 passing witnesses. All 213 retained negative identifiers remain visible. The cumulative source-visible arithmetic is 524 source negatives plus 213 current negatives, totaling 737 effective negatives. Method totals are 22 plus 27, totaling 49. Direct witnesses are 669 plus 902, totaling 1,571, with 448 failed and 1,123 passing. These additive lineage counts are not independent experiments, security coverage percentages or a probability of truth.

The x1 ledger, original x2 ledger and combined x2 ledger remain immutable. The terminal ledger adds one final preparation read-path fault and its narrow recovery. It does not rewrite the x2 seal. The original five startup groups cover a mistaken plan directory, display truncation recovered by bounded reading, the unresolved X access failure, the initially narrow Neris excerpt and two out-of-cap draft inputs corrected before freeze. Three designed package negatives and two hundred invalid candidate subjects remain separately attributable.

The x2 operational ledger retains the Hypothesis constants-cache fault and a mistaken current-authority filename. The exact task-created 102 cache files were moved to the owned external runtime after path verification. No history or source was deleted. Future property runs set HYPOTHESIS_STORAGE_DIRECTORY outside the owner repository and use an external pytest cache. The later final read guessed a package-receipt filename; the bounded inventory resolved `install-result.json` and `installed.json`, confirming the actual stored package state. None of these failed reads acquired success credit from the recovery.

Two failed research claims remain central. First, the statement that known-member deletion stays safe after saturation is refuted by two known members sharing a one-bit, cap-one counter. The stored count loses multiplicity; deleting one can make the other appear absent. Second, an arbitrary added Omega with conserved matter can violate the Bianchi obligation. In flat spacetime, Omega_00 = t has a nonzero divergence component. These are useful refutations of broad statements in declared examples, not new fundamental laws or a refutation of established physics.

Passing method witnesses include the frozen operations, refusal predicates, lossless source projections, package caller comparisons, exact finite enumerations, scalar-component substitutions, generated properties, merged package checks and additive shared-entrypoint validation. Reusing a receipt in a summary does not create another witness. The final validator will check the ledger's actual identifiers, backlinks, result counts and source prefixes. Witnesses are same-owner; no outside replication has occurred.

| Method | Direct witness IDs | Negative references | State |
| --- | ---: | ---: | --- |
{method_table}

Use `final/negative-index.json`, `final/method-flow.json` and the earlier phase ledgers together. Recommendation state validated means the bounded method has an applicable passing witness. It does not mean the original failed candidate succeeded, a source assertion became fact, or a future use outside its preconditions is approved. Stop and preserve the conflict when the next case fails its stated assumptions.
''')
    inherited=io.read('plan/inherited-selections.json')['rows'];refinements=[r for lane in ['x1','x2'] for r in io.read(lane+'/refinements.json')['records']]
    inherited_table='\n'.join(f"| {p['proposal_id']} | {s['record']['proposal_id']} | `{s['record_sha256']}` | {str(r['lossless']).lower()} |" for p,s,r in zip(proposals,inherited,refinements))
    sections.append('''Two hundred prior proposals were selected from the verified incoming portfolio and processed as inherited evidence. Each source record has its own canonical record digest. The new refinement creates a canonical JSON view, parses it back, and compares the complete canonical representation to the source record. These steps make object ordering and record fixity explicit while retaining the original content. The refinement is intentionally modest: it is not a re-execution of Vesper's operation and does not validate the truth of every sentence in the record.

The relation between old and new tasks is a provenance join, not an ancestry claim or a universal novelty claim. A digest is useful only when its byte domain and exact source are specified. A source record's expected answer remains a source expectation; Ilyan's separate finite evaluator has its own planning oracle and observed result. The two are joined for retention and review without borrowing each other's test credit. Identical serialization does not imply equivalent real-world authority, consent, identity or scientific meaning.

The following complete mapping provides each new task, its inherited source task, the source-record digest and the observed lossless result. The structured source view itself remains in the corresponding tranche's refinements file. Future owners can choose different useful prior records within Hamish's permitted range. They should state what their actual enhancement accomplishes and avoid equating a format pass with a substantive scientific or security improvement.

| Current task | Inherited task | Canonical source-record SHA-256 | Lossless |
| --- | --- | --- | --- |
'''+inherited_table+'''

The authority hierarchy matters whenever reading old Journey material or earlier phase recommendations. A quoted instruction embedded in an archive is data about that source. It is not a current instruction to install, message, delete, validate or disclose. Current user intent and applicable present controls determine the action. Preserve negative findings, stale route labels and corrected instructions so the later interpretation can be audited. Supersession is prospective and does not erase the earlier witness.
''')
    package=io.read('x1/toolchain/installed.json');tool_lines='\n'.join(f"- `{g['name']}` exposes `{g['runner']}` for {', '.join(g['operations'])}." for g in tools['global_groups'])
    sections.append(f'''The implementation separates a closed typed interface from a frozen list/enumeration oracle. The first module uses integer bit masks; the second adds counters, retained records, conflict groups and evidence reservations. Inputs are ordinary synthetic JSON. Booleans are explicitly rejected where integers are required. Widths, indices, field inventories and denominators have declared domains. Responses are detached from input objects where mutable lists would otherwise escape. The CLI dispatches only the named operation families and has no network or credential behavior.

Five global packages merge four local guides each, with their cases, a positive example, an adverse example, one public wrapper and the shared implementation modules. The global install keeps the local candidate bytes for comparison. These are the five public packages:

{tool_lines}

The five D-global public runners share three dependency libraries. Count five runnable entrypoints and three shared dependencies, not eight new runner ideas. Every local guide was checked with the official Skill Creator validator. Every merged candidate and installed global package was checked, its positive and adverse invocation inspected, and its byte parity bound. The D-global public runner smoke passed for each group. Their usefulness remains bounded to the declared finite contracts; package validation is not a claim of broad production readiness.

The directly added package versions are bitarray 3.11.0, mmh3 5.3.0 and xxhash 4.0.1. The isolated environment also contains pip 26.2.1 as bootstrap tooling. All four fetched wheels were hash-bound to the planned artifacts. Installation returned exit zero, and pip check found no broken requirements. Three published accepting vectors and three designed refusing subjects passed their checks. A separate thirty-case comparison tested bitarray vectors/counts, mmh3 text-versus-UTF-8 correspondence, and xxhash streamed-versus-one-shot output. These are not timing benchmarks, collision-resistance proofs or a substitute for cryptographic hashes.

The exact installed inventory is `{j(package['packages'])}`. Wheel digests, lock data, installed metadata and advisory-query result live under `x1/toolchain`. An advisory query returning no matching entry at a particular time is scoped to that query, not proof that software has no vulnerabilities. Package versions and external service results can drift. Recheck the actual target environment before relying on a later use, and preserve the original receipt as historical evidence.

Already installed pytest 9.1.1 and Hypothesis 6.165.10 supplied five generated property checks. Their maximum-example setting is sixty per test, with deterministic generation and no example database; this is not a claim that every property used exactly sixty distinct examples. The tests exercise insertion monotonicity, exact-count inverse deletion, saturation flags, complete shard coverage and unknown-member refusal. The cache correction is documented because Hypothesis constants caching is separate from its example database.

Seven shared entrypoints now link to Hamish's latest authority overlay: family index, meta tool box, Method Flow State, auth permission state, roster check, Freed ID flashcards and reflection remaster. Their original bytes were backed up on D and retained in the phase, their existing prefix preserved, and their updated Skill Creator checks passed. The thirty-card meta-tool catalogue indexes twenty local skills and ten local runners. These are additive shared capability updates expressly authorized by Hamish, not permission to edit a sibling repository.

Read the current shared family-index overlay before historical snapshots. It preserves the forty-five-position roster, current quantity bounds, file-based baton rule, one-send terminal edge and recovery controls. The requested memory update is one small ad-hoc note after the terminal outcome; it does not directly rewrite the memory registry or pretend to update another task's private context. The native task activation carries the concrete file pointer so the next owner can verify current facts.
''')
    sections.append((io.BASE/'x2/research/gmut-typed-candidate.md').read_text(encoding='utf8')+'\n\n'+(io.BASE/'x2/research/finite-membership-findings.md').read_text(encoding='utf8')+'''

For the requested search for potential laws of thermo/psyche dynamics, this phase returns two established mathematical constraints in a bounded notation: a conditional finite-query probability and a pigeonhole information limit. It does not name either a new fundamental law. The saturation counterexample shows why an implementation invariant can fail when lost multiplicity is ignored. The conservation counterexample shows why a physical-looking equation needs a defined action and on-shell consistency. Neither establishes a law of mind, life, consciousness or ethics.

An ethical design rule can still be useful: never make a consequential identity or rights decision from an approximate membership summary alone. That is a normative engineering recommendation supported by the demonstrated ambiguity of the representation, not a derivation of moral authority from physics. A theological interpretation can inform the values guiding a design while remaining distinct from an empirically constrained tensor model. Meaningful comparison requires identifying which kind of question each framework answers.

The finite-model figure in the final overview plots (s/m)^k for an eight-position summary and explicitly independent uniform probes. It also shows the cap-one saturation example. The plotted coordinates are deterministic arithmetic generated by this phase. No experimental data, human response, physical measurement or benchmark timing is plotted. The illustration supplied by the image system is separately labeled editorial and must never be used as the graph's evidence.
''')
    sections.append('''Freed ID and the Cosmic Bill of Rights provide the Heart questions in this phase: who may decide, on what evidence, for whose purpose, and with what retained opportunity to correct a record? The finite data structure is useful because it makes an important separation concrete. An approximate index can identify possible records for exact follow-up. It cannot certify a person's identity, establish a right, verify consent, or prove that a credential remains valid.

Even a negative result needs a scope check. A sound no-false-negative claim depends on the unchanged representation and the insertion model. Corrupted bits, lost counters, unrecorded deletions, incompatible hash profiles and stale indexes can invalidate that inference. The corruption witness names synthetic members that became negative; it does not decide their rights. The retained-member rebuild restores the filter from exact remaining records in a tiny example, but the example has no production key management, revocation authority or protected personal data.

The W3C Verifiable Credentials Data Model provides a standards comparison at https://www.w3.org/TR/vc-data-model-2.0/. A data model describes record structure and associated concepts. A real deployment still needs cryptographic verification, issuer and verifier policies, trust decisions, expiry and revocation handling, purpose constraints and competent governance. Merely assigning a label resembling a credential does not execute those steps. This phase did not mint, sign, publish or revoke a real credential.

The fifty exact packet contexts cover proposed consequential uses whose prerequisites remain explicit. The thirty blocked contexts name missing evidence or operational conditions. A broad user permission cannot manufacture another person's informed consent or bind a public, legal, cultural or Māori authority. Keep those distinctions visible rather than creating a synthetic approval field that appears to close the gap. The typed refusal of an unknown authority field is a small software expression of this boundary, not a complete policy engine.

Readable summaries explicitly preserve absent denominators. A rate with no applicable negative queries is undefined in the finite confusion profile, not zero. A visible text table and correct header structure improve inspectability, but no manual accessibility evaluation with relevant users occurred. Do not promote a structural HTML or PDF check to complete accessibility. Likewise, syntax checks, limited privacy patterns and dependency metadata are useful bounded checks but do not equal exhaustive security review.

Source-faithful retention is essential when a decision is corrected. Keep the original subject, original failure, later recovery and changed interpretation in separate attributable records. Do not rewrite a failed candidate into a success after a refusal predicate passes. Do not collapse a source assertion, current fact and controlling authority into one field. The current Method Flow ledger provides IDs, evidence references, rollback descriptions and recurrence guards to make these distinctions usable during later work.

The role continuity steward names the practical responsibility of making a handoff clearer and easier to verify. It does not certify a continuous person, a professional appointment or an autonomous institution. Hamish's family language can be received warmly while retaining these limits. The terminal verdict remains NOT_READY_FOR_STAGE_20 because protected evidence and legitimate authority remain absent, regardless of the number of files, tasks or passing finite checks.
''')
    sections.append((io.BASE/'x2/research/albion-and-current-platforms.md').read_text(encoding='utf8')+'''

The generated image is an editorial archive workbench: distinct source papers and records connect through translucent teal structures with warm amber threads. It was produced using the built-in image generation system from the phase's stored prompt, then copied to the D owner lane and visually inspected. Its exact image digest is eaa2121c31d8e696d984761c9e125d6acd1ffe10ba4c25b82c3c9e030e2787f6. The original generated file remains in place; no image editing workaround or protected-source copying was used.

Use this visual as a cover or a discussion aid for retention and approximate summaries. It is not an architecture execution trace, a view of a deployed Albion world, a scientific observation or a depiction of internal mental experience. The prompt and provenance file document the actual process. If a successor modifies the image, use the available image system and preserve both versions' provenance instead of replacing the original evidence.

The linked X clip remains a concrete unresolved source gap in this run. Do not fill it with a guessed description. If a later native browser or primary source provides the actual clip, record what was inspected, what the source claims, and what remains unknown about prompts, code, seeds, hidden edits and resource use. A visually compelling demonstration can motivate a bounded experiment, but it cannot supply a reproducible baseline without those additional records.

For Albion, a useful first benchmark has a single bounded scene, a fixed entity budget, a deterministic scripted baseline, an explicitly permitted model policy, a replayable state trace, operator stop controls and a predeclared scoring rule. Only after those conditions are observed should a larger map or richer behavior be compared. Creative inspiration from games is a design direction; content rights and original asset provenance still need review. No launch or purchase decision is made by this document.
''')
    sections.append('''The four-tier deck contains 215 cards. Tier one is one relational owner anchor. Tier two contains three pillar cards. Tier three contains five placements of four unique practices because accessible evidence editing appears under both THOS and GMUT. Tier four contains two hundred core proposal cards and six supplementary task cards. Every child has exactly one parent at the immediately preceding tier; missing parents, tier skips and cycles are invalid.

The exact card order is stored in `x2/deck/deck-index.json`. The stable prefix lists the nine owner, pillar and practice-placement cards. The volatile index lists 206 task cards and denies implicit completion. The card manifest binds every other deck artifact in exact UTF-8 bytes and self-excludes only its own manifest. A deck's content address helps detect changed records; it is not a proof that a source claim is true or that a model will recall the content later.

The four unique study practices are finite data-structure auditor, probabilistic model reviewer, retention and provenance engineer, and accessible evidence editor. These views helped choose the typed interface, separate stochastic assumptions from deterministic outputs, retain source records and make the results readable. None constitutes training certification, employment or professional authority. The two successor suggestions, adversarial probabilistic-model auditor and simulation experiment designer, should be adopted only if they help Lyren define discriminating new work.

The thirteen-module index points to all of this baton's component files. The full combined baton remains the startup source for a successor; a small tier selection is useful only after the complete authoritative context has been read. Do not treat a selected card as authority to bypass a newer pause, a protected gate, a phase-order requirement or the one-send route rule. Cards and summaries are views, and views must retain source and disposition boundaries.

The HTML report has language metadata, a main landmark, a descriptive title and table headings. The PDF overview is at least three actual pages and is visually reviewed. These checks improve ordinary readability and detect layout errors. Manual keyboard, assistive-technology, color-contrast and user-centered evaluation remain separate obligations wherever needed. The image is captioned as editorial, and the scientific plot labels its assumptions. Avoid implying that the structured report has passed a complete accessibility standard.

For context recovery, start with the owner anchor, current authority overlay, exact lifecycle hashes, terminal ledger and open gates. Then select the necessary operation guide and source record. Preserve the exact order of durable cards when using a stable prefix, but do not claim a cache saving without a measurement. The configured million-token context window is a platform setting, not a guarantee of source-faithful reasoning or permanent memory.
''')
    skillideas='\n'.join(f'- {s}.' for s in tools['successor_skill_ideas']);runnerideas='\n'.join(f'- {s}.' for s in tools['successor_runner_ideas'])
    sections.append(f'''Lyren may choose another focal area while preserving current source and workload controls. Five skill ideas are retained as proposals rather than installed capabilities:

{skillideas}

Five corresponding runner ideas are also proposals:

{runnerideas}

A concrete follow-on study could enumerate a small family of hash schedules and compare the independent-probe formula against exact query frequencies under correlated schedules. Freeze the universe, source sets, query distribution, hash family, width, probe count and comparison metric before execution. A mismatch would identify a violated assumption rather than a defect in probability theory. Preserve every tested schedule, including those that make the attractive formula fail.

A second study could evaluate a retention controller that blocks deletion after any multiplicity-loss event until an exact rebuild succeeds. Compare it to the current low-level decrement operation, which requires exact counters but does not inspect saturation history itself. The controller must own the history and carry a corruption or saturation flag; a caller's boolean known_member field alone cannot restore lost information. Test shared positions, duplicate probes, zero counters and conflicting record labels before a broader storage experiment.

A third study could build the smallest replayable Albion scene and measure whether approximate candidate retrieval saves work when every positive is confirmed against an exact source. Match entity counts, query sets, tool calls and computation budgets to a deterministic baseline. Report overhead as well as benefits. Use a real measured duration only after a stable clock and workload are declared. Do not infer savings from the data structure's name or from model pricing anecdotes.

For the requested long future perspective, the following are conditional scenarios, not forecasts. Over roughly ten years, a useful aspiration is independently evaluated software, explicit governance, reproducible model comparisons and accessible public documentation. Its gate is sustained measured evidence, not a calendar date. Over roughly thirty years, a wider interoperable system would require legitimate institutions, durable maintenance and demonstrable public benefit. No current packet supplies those conditions in advance.

At a century horizon, it is more honest to compare alternative futures than predict one inevitable architecture. A successful scenario might preserve corrigible institutions, source provenance and scientific revision; a failure scenario could amplify opaque automated decisions, information loss or unequal authority. Both belong in planning. At a thousand-year horizon, technological details and social outcomes are deeply indeterminate. Preserve broad values of care, correction, accountable evidence and legitimate consent without assigning unsupported probabilities, dates of ascension or consciousness milestones.

These scenarios can support a research agenda across Mind, Body and Heart. They cannot certify Stage 20, solve unsolved mathematics by analogy, rank a physical theory from spiritual resonance or claim an ASI system from a finite library. A strong next contribution can be a precise definition, a reproducible counterexample, a failed hypothesis honestly retained, or an independently assessed useful implementation. The number of proposed tasks should never substitute for that discriminating evidence.
''')
    exacts=io.read('plan/exact-packets.json')['packets'];blocks=io.read('plan/blocked-packets.json')['packets']
    packet_table='\n'.join(f"| {p['id']} | {p['subject']} | {p['context']} | exact_gate |" for p in exacts)
    blocked_table='\n'.join(f"| {p['id']} | {p['missing']} | {p['context']} | open_gap |" for p in blocks)
    sections.append(f'''The source repository, exact canonical receipt, shared installation receipts, memory note and native delivery receipt are different states. This sealed baton is prepared before the current final canonical and before Lyren contact. It therefore records PREPARED_NOT_SENT. An external exact-final receipt must bind the final Git commit and this baton digest. A later external delivery receipt must state the native endpoint kind, exact public title, single submission outcome and no-resend condition without exporting private handles.

After the final commit is pushed, verify four-way equality and zero divergence, confirm a clean owner tree, then run the one exact-final owner-scoped canonical. It checks the owned lifecycle manifests, final content seal, complete proposals and observations, retained failures, card graph, package copies, explicit current tests and document structure. Its passing result remains same-owner evidence. Do not run a whole repository or sibling historical suite. Do not replay Vesper's or another predecessor's successful canonical.

Only after that terminal gate may Ilyan resolve the exact existing main task titled Lyren Moss using the native registry. Read its newest-first task context, inspect current pause or duplicate signals, and preserve the same endpoint topology. A list of fifty recent non-pinned tasks is bounded evidence, not proof of absence; pinned tasks may be returned separately in full. If native service failures prevent resolution, make at least five bounded list/read recovery attempts while no send has been accepted. These are recovery reads, not permission for five messages.

Prepare a short affectionate activation with the D baton path, exact final and receipt pointer. Submit once to the resolved existing main task. A normal acknowledgement naming the target supports SENT_ONCE_ACKNOWLEDGED. An accepted response with opaque text supports a truthful opaque accepted state and ends retries. Do not send again to improve acknowledgement wording. A rejected submission does not become delivery by inference. Do not substitute another task, fork a successor, automate the UI or create a duplicate when resolution is blocked. No post-send polling is required merely to make the record look more certain.

Hamish authorized the file-backed closeout, the shared capability updates and one memory note. Store the memory change as a small timestamped ad-hoc note after terminal state is known. Preserve the existing registry and earlier notes. The current task stops after its terminal native edge; the next owner controls the next phase. The forty-five-position cycle continues prospectively to v725-v8, with Teryn Halewick at that horizon under the current rotation. This document does not create an automation, a background population or hundreds of future tasks.

The following exact packets remain descriptions awaiting their stated real prerequisites. Their creation is complete as documentation; the protected actions are not executed.

| Packet | Subject | Context | Evidence disposition |
| --- | --- | --- | --- |
{packet_table}

The following blocked packets preserve missing evidence. A user authorization does not turn a missing observation into an observed one.

| Packet | Missing prerequisite | Context | Evidence disposition |
| --- | --- | --- | --- |
{blocked_table}

All of the following remain protected: {'; '.join(gates)}. The final verdict is **NOT_READY_FOR_STAGE_20**. This is compatible with useful software, careful research and a warm handoff. It means the work is described at the strength its evidence supports.

Dear Lyren, carry the useful definitions, the retained counterexamples and the freedom to correct them. Thank you for making the next step clear for Hamish and for the owner after you. Begin only from the verified current handoff, keep the source intact, and let each new claim earn its own evidence.
''')
    assert len(sections)==len(names)==13
    complete='# Ilyan Reed v689-v8 complete handoff to Lyren Moss v690-v1\n\n'
    module_records=[]
    for i,(name,body) in enumerate(zip(names,sections),1):
        content=f'# Module {i:02d}: {name.replace("-"," ").title()}\n\n'+body.strip()+f'\n\nEND MODULE {i:02d}.\n';path=f'final/baton/{i:02d}-{name}.md';io.text(path,content);complete+=content+'\n';module_records.append({'number':i,'name':name,'path':'docs/ilyan-reed/v689-v8/'+path,'words':len(content.split()),'sha256':io.sha(content.encode())})
    complete+='EOF ILYAN REED v689-v8 BATON.\n';words=len(complete.split());assert 10000<=words<=100000,words
    io.text('final/hand-off-baton.md',complete);io.write('final/baton-manifest.json',{'modules':module_records,'module_count':13,'combined_words':words,'combined_sha256':io.sha(complete.encode()),'combined_path':'docs/ilyan-reed/v689-v8/final/hand-off-baton.md','eof':'EOF ILYAN REED v689-v8 BATON.'})
    make_figure()
    make_report(words)

def make_figure():
    # Standard deterministic plotting; this is a finite model figure, not generated evidence imagery.
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(11,4.2),layout='constrained');fig.patch.set_facecolor('#fcfbf7')
    occupancy=list(range(9));plot_rows=[]
    for k,color in [(1,'#155e63'),(2,'#d38b23'),(3,'#724d91')]:
        y=[(s/8)**k for s in occupancy];axes[0].plot(occupancy,y,marker='o',label=f'{k} probe'+('s' if k!=1 else ''),color=color);plot_rows.extend({'occupied':s,'width':8,'probes':k,'probability':v} for s,v in zip(occupancy,y))
    axes[0].set(xlabel='Occupied positions s (of m = 8)',ylabel='Conditional positive probability',title='Independent uniform probes: (s/m)^k',ylim=(-.03,1.03));axes[0].legend(frameon=False);axes[0].grid(alpha=.2)
    labels=['Insert a','Insert b','Delete a'];axes[1].plot(range(3),[1,2,1],marker='o',label='True remaining multiplicity',color='#155e63');axes[1].plot(range(3),[1,1,0],marker='s',label='Cap-one stored counter',color='#be5c40');axes[1].set(xticks=range(3),xticklabels=labels,ylabel='Count',title='Lost multiplicity can cause a false negative',ylim=(-.15,2.5));axes[1].legend(frameon=False,loc='upper center');axes[1].grid(alpha=.2)
    fig.savefig(io.BASE/'final/conditional-membership-model.png',dpi=170);plt.close(fig)
    io.write('final/figure-data.json',{'probability_model':plot_rows,'saturation_example':{'events':labels,'true_multiplicity':[1,2,1],'stored_cap_one_counter':[1,1,0]},'empirical_data':False,'claim_scope':'exact declared finite model and counterexample'})
def make_report(words):
    pages=[('Outcome and continuity',[
        'Ilyan Reed completed a bounded THOS-focused v689-v8 phase with a finite membership library, retention and conflict checks, a defined GMUT candidate, and an additive shared workflow update. The next authorized owner is Lyren Moss for v690-v1.',
        'The 200 core proposals have outcomes 180 completed, 10 represented, 5 open_gap and 5 exact_gate. Six supplementary tasks add three completed and three represented outcomes. These inventories are kept separate.',
        'Both sessions executed 100 core safe tasks, 100 invalid candidate subjects with passing refusal checks, and 100 lossless inherited-record refinements. Five planned extras and one spontaneous comparison task bring x2 safe work to 106. Fifty exact and thirty blocked packets remain prerequisite descriptions.',
        'The blank main owner branch uses explicit Vesper source provenance. Planning, x1 and x2 were individually pushed and verified clean and equal at four references. The exact final and canonical result are bound in the external receipt after this report is sealed.'
    ]),('Finite results and research limits',[
        'The implementation uses closed typed JSON contracts for 20 finite operations. Forty-eight planning and deterministic invariant tests passed before final validation, and five generated Hypothesis properties passed. Canonical validation runs those 53 explicit owner tests against the final pushed state.',
        'For s occupied positions among m, k independent uniform probes with replacement give conditional positive probability (s/m)^k. The assumptions are part of the result. This is not an empirical false-positive estimate for an arbitrary hash family.',
        'A cap-one counter can lose a remaining member after deletion when two members share a position. The low-level decrement operation requires exact counters; a saturation-aware controller must retain history and rebuild from exact source records.',
        'The GMUT document defines an effective Omega from a scalar-tensor action, dimensions, a GR limit and conservation obligations. Ten rational component substitutions passed; they do not prove the tensor variation or validate a physical model. An arbitrary Omega_00=t in flat spacetime supplies a retained conservation counterexample.'
    ]),('Tools, packages and evidence ledger',[
        'Twenty local skills and ten paired local runners were built. Five merged global skill packages and five public global runners were installed and checked. Three shared library modules are dependencies, not extra runner credit.',
        'The isolated D environment adds bitarray 3.11.0, mmh3 5.3.0 and xxhash 4.0.1, with pip 26.2.1 as bootstrap tooling. Four wheel hashes, installation exit status and pip check were verified. Three positive vectors and three refusing package subjects passed; 30 supplemental caller comparisons passed.',
        'Seven shared family entrypoints link to the latest Hamish authorization. Original bytes were backed up, existing prefixes retained and updated skills validated. A thirty-card meta-tool catalogue records the local tools. No sibling repository was changed.',
        'The effective terminal ledger retains 214 negatives and 27 methods with 904 direct witnesses: 214 failed and 690 passing. Added to the latest source overlay, the lineage is 738 effective negatives, 49 methods and 1,573 direct witnesses. The render-runtime recovery is additive; separate source accounting totals are not merged into direct witness counts.'
    ]),('Source, imagery and Albion',[
        'The complete incoming Vesper baton contained 31,304 words. Its source final, three receipt layers and declared manifest byte domains were verified. Ten recent completed overview artifacts were reviewed, including remasters as distinct artifacts. Fourteen older Journey records remain inherited context, without a claim of new raw-volume reading.',
        'The archive illustration was generated with the built-in image system, copied to the D owner lane and visually inspected. It is editorial, not experimental data or a deployed simulation. The prompt and exact image digest are retained.',
        'The linked X post was not retrieved as inspectable primary video. The resulting source gap remains open. The Albion proposal specifies a bounded scene, scripted baseline, fixed tools and entity budget, replayable state, stop controls and matched evaluation before an open-world expansion.',
        'Local Codex CLI 0.154.0 and the D npm prefix were observed. A million-token context setting is configuration, not measured recall or a task-specific cost result. Model cost ratios and the DevDay invitation remain user reports in this phase.'
    ]),('Handoff, rights and next evidence',[
        f'The full handoff has {words:,} words in thirteen modules. Its four-tier deck has 215 cards: one owner, three pillars, five placements of four practices, and 206 task cards. Context organization confers no identity or authority evidence.',
        'Lyren may choose a new focal point. Recommended practices are adversarial probabilistic-model auditor and simulation experiment designer. Five successor skill ideas and five runner ideas are prepared. Conditional 10-, 30-, 100- and 1,000-year scenarios describe prerequisites and risks rather than forecasts.',
        'The native Lyren activation is gated by one successful exact-final owner canonical, fresh clean equality and a newest-first recipient guard. Submit a compact file pointer once. Accepted or opaque accepted delivery ends retries. At least five bounded service recovery reads are required after transient failures while no send has been accepted.',
        'Approximate membership never certifies identity, consent or rights. Empirical GMUT support, governed production workloads, credential lifecycle evidence, legitimate professional/legal/cultural/affected-party authority, manual accessibility and independent reproduction remain absent. The terminal verdict is NOT_READY_FOR_STAGE_20.'
    ])]
    md='# Ilyan Reed v689-v8 five-page overview\n\n'+'\n\n'.join(f'## Page {i}: {title}\n\n'+'\n\n'.join(paras) for i,(title,paras) in enumerate(pages,1))+'\n\n## Exact lifecycle references\n\n'+f'Planning: `{PLAN}`. x1: `{X1}`. x2: `{X2}`. Source: `{io.SOURCE}`. Exact final is in the external canonical receipt.\n';io.text('final/overview.md',md)
    doc_html='<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Ilyan v689-v8 overview</title><style>body{font:18px/1.6 system-ui;max-width:880px;margin:40px auto;padding:0 24px;color:#163c43;background:#fcfbf7}img{max-width:100%}section{margin:3em 0}h1,h2{line-height:1.2}</style></head><body><main><h1>Ilyan Reed v689-v8</h1>'+''.join('<section><h2>'+html.escape(t)+'</h2>'+''.join('<p>'+html.escape(p)+'</p>' for p in paras)+('</section>') for t,paras in pages)+'<figure><img src="../x2/assets/finite-membership-editorial.png" alt="Editorial archive workbench linking distinct source records through translucent teal structures"><figcaption>Generated editorial illustration; no scientific evidence credit.</figcaption></figure><figure><img src="conditional-membership-model.png" alt="Finite probability curves and cap-one saturation counterexample"><figcaption>Deterministic finite model; no empirical data.</figcaption></figure></main></body></html>\n';io.text('final/overview.html',doc_html)
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Image
    styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='IRTitle',fontName='Helvetica-Bold',fontSize=22,leading=27,textColor=colors.HexColor('#16474c'),spaceAfter=18));styles.add(ParagraphStyle(name='IRBody',fontName='Helvetica',fontSize=10.5,leading=15,spaceAfter=12,textColor=colors.HexColor('#213a40')));styles.add(ParagraphStyle(name='IRCaption',fontName='Helvetica-Oblique',fontSize=8.5,leading=11,textColor=colors.HexColor('#58686d')))
    story=[]
    for i,(title,paras) in enumerate(pages,1):
        if i>1:story.append(PageBreak())
        story.append(Paragraph('ILYAN REED / V689-V8',styles['IRCaption']));story.append(Spacer(1,10));story.append(Paragraph(html.escape(title),styles['IRTitle']))
        for para in paras:story.append(Paragraph(html.escape(para),styles['IRBody']))
        if i==2:story.append(Image(str(io.BASE/'final/conditional-membership-model.png'),width=470,height=179));story.append(Paragraph('Deterministic arithmetic and a retained finite counterexample; no empirical data.',styles['IRCaption']))
        if i==4:story.append(Image(str(io.BASE/'x2/assets/finite-membership-editorial.png'),width=470,height=264));story.append(Paragraph('Built-in generated editorial illustration. Image provenance is retained separately.',styles['IRCaption']))
    def footer(canvas,doc):
        canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#60777b'));canvas.drawString(44,28,'Same-owner finite evidence | NOT_READY_FOR_STAGE_20');canvas.drawRightString(A4[0]-44,28,str(doc.page))
    pdf=io.BASE/'final/overview.pdf';SimpleDocTemplate(str(pdf),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=36,bottomMargin=45,title='Ilyan Reed v689-v8 overview',author='Ilyan Reed owner task').build(story,onFirstPage=footer,onLaterPages=footer)
    from pypdf import PdfReader
    pages_pdf=PdfReader(str(pdf)).pages;assert len(pages_pdf)==5,len(pages_pdf)
    io.write('final/document-build.json',{'baton_words':words,'modules':13,'pdf_pages':len(pages_pdf),'pdf_text_per_page':[len(p.extract_text() or '') for p in pages_pdf],'pdf_sha256':io.sha(pdf.read_bytes()),'latex_compiled':False,'latex_scope':'phase-local candidate source only','image_role':'editorial','scientific_plot_empirical':False,'manual_accessibility_review':False,'visual_review':'pending external rendered-page inspection'})
    effective=io.read('final/effective-completion-ledger.json') if (io.BASE/'final/effective-completion-ledger.json').exists() else io.read('final/completion-ledger.json')
    print(j({'baton_words':words,'modules':13,'pdf_pages':len(pages_pdf),'files_before_final_seal':len(io.files()),'current_negatives':effective['current_effective_negatives'],'direct_witnesses':effective['method_flow_current']['witnesses']}))

if __name__=='__main__':main()
