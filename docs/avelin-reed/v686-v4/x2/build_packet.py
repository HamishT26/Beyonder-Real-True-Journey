"""Assemble owner evidence, Method Flow, four-tier cards, and the modular baton."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
LANE = ROOT.parents[2]
PREFIX = ROOT.relative_to(LANE).as_posix()
SOURCE = 'c5cdc995c99bca100f5a63a4f3f23e932d9433a5'
X1 = '5fbfddafacbfdae773777a7e7591b473797491a5'


def read(relative):
    return json.loads((ROOT / relative).read_text(encoding='utf-8'))


def write(relative, value):
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as output:
        output.write(value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n')


def compact(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def digest(value):
    return hashlib.sha256(compact(value)).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--method-script', required=True, type=Path)
    args = parser.parse_args()
    proposals = read('x1/new-proposals.json')['proposals']
    results = read('x2/contract-results.json')['rows']
    summary = read('x2/contract-summary.json')
    identity = read('x1/identity-and-practice.json')
    gates = read('x1/validation-contract.json')['all_protected_gates']
    boundary = identity['boundary']
    operations = read('x1/startup-methods.json')['events'] + [read('x2/toolchain/bootstrap-correction-event.json'), read('x2/toolchain/bootstrap-invocation-event.json'), read('x2/promotion-procedure-event.json')]
    assert len(operations) == 12 and len({r['id'] for r in operations}) == 12
    write('x2/all-operational-events.json', {'schema': 'ghc.family.operational-events.v686.v4', 'events': operations, 'count': len(operations), 'initial_success_credit': 0})

    retained = read('x2/retained-adverse-records.json')['rows']
    pairs = []
    for index, row in enumerate(retained):
        assert row['invalid_accepted'] is False and row['bounded_recovery_passed'] is True
        pairs.append({'negative_id': row['negative_id'], 'failure': row['kind'] + ' is outside the frozen report contract',
                      'recovery': 'Use the exact frozen report with its original definition, input, result, domain, and protected-claim fields.',
                      'reference': PREFIX + '/x2/retained-adverse-records.json#/rows/' + str(index), 'proposal': row['proposal_id']})
    for op in operations:
        pairs.append({'negative_id': op['id'], 'failure': op['failure'], 'recovery': op['recovery'], 'reference': PREFIX + '/x2/all-operational-events.json#' + op['id'], 'proposal': None})
    for kind, filename in [('skill', 'tooling/skill-smoke-summary.json'), ('runner', 'tooling/runner-smoke-summary.json')]:
        for row in read(filename):
            assert row['positive_pass'] and row['adverse_refused']
            pairs.append({'negative_id': row['negative_id'], 'failure': 'Duplicate JSON member in the ' + kind + ' CLI request', 'recovery': 'Use the matching frozen family and its exact accepting input through the same portable CLI.', 'reference': PREFIX + '/' + filename + '#' + row['negative_id'], 'proposal': row['source_proposal']})
    for row in read('x2/toolchain/package-smokes.json')['rows']:
        assert row['positive_pass'] and row['adverse_refused']
        pairs.append({'negative_id': row['negative_id'], 'failure': row['package'] + ' adverse fixture is not the declared accepting behavior', 'recovery': 'Use the pinned package with its separately checked accepting fixture and keep the rejecting witness.', 'reference': PREFIX + '/x2/toolchain/package-smokes.json#' + row['negative_id'], 'proposal': None})
    assert len(pairs) == 1580
    spec = importlib.util.spec_from_file_location('method_state', args.method_script)
    method = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(method)
    ledger = method.new_ledger('v686-v4', 'Avelin Reed')
    ledger.update({'execution_authority': 'owner_self_scoped_delta', 'source_commit': SOURCE, 'x1_commit': X1,
                   'final_commit': None, 'final_commit_binding': 'The external exact-final canonical receipt binds the completed owner delta without a self-referential hash.',
                   'changed_file_scope': PREFIX + '/', 'module_allowlist': [PREFIX + '/runners/ghc_family_temporal_' + x + '.py' for x in ['intervals','windows','journals','guards','reports']],
                   'repository_scan': False, 'unchanged_history_scan': False, 'cross_lane_scan': False, 'sibling_lane_mutation': False,
                   'case_instance_counting': 'These are case-scoped method instances, not 1580 different techniques or independent discoveries.',
                   'materialized_file_rotation_threshold': 2000})
    for row in pairs:
        mid = row['negative_id'] + '-METHOD'
        fail_id, pass_id = mid + '-FAIL', mid + '-PASS'
        ledger['methods'].append({'method_id': mid, 'title': row['negative_id'] + ' bounded recovery', 'failure_signature': row['failure'],
                                  'trigger_preconditions': ['Exact owner-scoped fixture or recorded operational precondition', row['reference']],
                                  'privacy_class': 'sanitized_public', 'approval_class': 'safe_now', 'candidate_workaround': row['recovery'],
                                  'validation_witness_ids': [fail_id, pass_id], 'recurrence_guard': 'Check this exact trigger, domain, and scope before reusing the method; no successful canonical replay.',
                                  'rollback': 'Stop selecting the candidate and retain the original negative and the prior validated bytes.',
                                  'recommendation_state': 'preferred', 'supersedes': [], 'protected_gates': gates,
                                  'retained_negative_ids': [row['negative_id']], 'scope_boundary': boundary})
        for suffix, result, expected, observed in [('FAIL','fail','Accepting original contract or successful scoped operation','Recorded candidate failed its intended acceptance condition'),('PASS','pass','Bounded correction matches its exact declared contract','Separate correction or accepting witness passed')]:
            ledger['witnesses'].append({'witness_id': mid + '-' + suffix, 'method_id': mid, 'procedure': row['recovery'] if result == 'pass' else row['failure'],
                                        'scope': row['reference'], 'expected': expected, 'observed': observed, 'result': result,
                                        'same_owner_only': True, 'independent_reproduction': False, 'retained_negative_ids': [row['negative_id']], 'boundary': boundary})
        method.append_event(ledger, mid, None, 'candidate', 'Retained failed witness', fail_id)
        method.append_event(ledger, mid, 'candidate', 'validated', 'Separate bounded passing witness', pass_id)
        method.append_event(ledger, mid, 'validated', 'preferred', 'Preferred only under matching owner preconditions', pass_id)
        ledger['recommendations'].append({'method_id': mid, 'preconditions': row['reference'], 'recommendation': row['recovery'], 'delivered': False, 'independent_reproduction': False})
    method.refresh_counts(ledger)
    review = method.validate_ledger(ledger)
    write('x2/method-flow.json', ledger)
    write('x2/method-flow-validation.json', review)
    assert review['valid'], review
    baseline = read('x1/activation-source.json')['successor_visible_baseline']
    effective = {key: baseline[key] + len(pairs) for key in ['effective_negatives','effective_methods','failed_witnesses','bounded_passing_witnesses']}
    effective.update({'open_gaps': baseline['open_gaps'] + 10, 'exact_gates': baseline['exact_gates'] + 10, 'declared_proposal_chain': baseline['declared_proposal_chain'] + 200})
    write('x2/effective-counts.json', {'schema': 'ghc.family.effective-counts.v686.v4', 'baseline': baseline, 'new_method_instances': len(pairs), 'new_adverse_and_operational_negatives': len(pairs), 'new_failed_witnesses': len(pairs), 'new_bounded_passing_witnesses': len(pairs), 'effective': effective, 'erased_negative_count': 0, 'case_counts_are_not_independent_reproductions': True})

    cards = []
    def card(tier, kind, title, parents, content, outcome='represented', stability='volatile', sources=None):
        body = {'schema': 'ghc.family.freed-id-card.v1', 'tier': tier, 'card_type': kind, 'title': title, 'parent_ids': parents,
                'owner': 'Avelin Reed', 'phase': 'v686-v4', 'stability': stability, 'outcome': outcome, 'content': content,
                'source_refs': sources or [], 'protected_gates': gates, 'relational_boundary': boundary}
        ident = 'ghc-card-' + digest(body)
        body['card_id'] = ident
        write('x2/flashcards/cards/' + ident + '.json', body)
        cards.append(body)
        return ident
    anchor = card(1, 'freed_id_anchor', 'Avelin Reed relational working anchor', [], identity, stability='stable')
    pillar_ids = {name: card(2, 'trinity_pillar', name, [anchor], {'priority': name == identity['priority_pillar'], 'boundary': boundary}, stability='stable') for name in ['GMUT Mind','THOS Body','Freed ID and CBR Heart']}
    practice_ids = {}
    for p in proposals:
        key = (p['pillar'], p['practice'])
        if key not in practice_ids:
            practice_ids[key] = card(3, 'bounded_practice', p['practice'] + ' / ' + p['pillar'], [pillar_ids[p['pillar']]], {'practice': p['practice'], 'qualification': False, 'employment': False, 'authority': False})
    for index, (proposal, result) in enumerate(zip(proposals, results)):
        related = [r['negative_id'] for r in pairs if r['proposal'] == proposal['proposal_id']]
        card(4, 'task', proposal['title'], [practice_ids[(proposal['pillar'], proposal['practice'])]],
             {'proposal_id': proposal['proposal_id'], 'family': proposal['family'], 'hypothesis': proposal['hypothesis'],
              'falsifier': proposal['falsifier'], 'rollback': proposal['rollback'], 'definition_sha256': proposal['definition_sha256'],
              'report_sha256': digest(result['report']), 'result_reference': PREFIX + '/x2/contract-results.json#/rows/' + str(index),
              'retained_negative_ids': related, 'method_reference': PREFIX + '/x2/method-flow.json', 'approval_class': proposal['approval_class']}, result['outcome'], sources=proposal['source_refs'])
    extra = [row for row in pairs if row['negative_id'].startswith(('AR6864-OP', 'AR6864-SKILL', 'AR6864-RUNNER', 'AR6864-PACKAGE'))]
    parent = practice_ids[('Freed ID and CBR Heart','synthetic policy-window reviewer')]
    for row in extra:
        card(4, 'task', row['negative_id'] + ' retained workflow witness', [parent], {'failure': row['failure'], 'recovery': row['recovery'], 'retained_negative_ids': [row['negative_id']], 'source_reference': row['reference'], 'falsifier': 'Referenced adverse or correction witness does not match its recorded result.', 'rollback': 'Keep both witnesses and stop promotion until the exact dependency is corrected.'}, 'completed')
    assert len(cards) == 240
    by_id = {c['card_id']: c for c in cards}
    for c in cards:
        assert (not c['parent_ids']) if c['tier'] == 1 else len(c['parent_ids']) == 1 and by_id[c['parent_ids'][0]]['tier'] == c['tier'] - 1
    write('x2/flashcards/deck-index.json', {'schema': 'ghc.family.deck-index.v686.v4', 'owner': 'Avelin Reed', 'source': SOURCE, 'x1': X1, 'card_count': len(cards), 'tier_counts': dict(Counter(c['tier'] for c in cards)), 'distinct_practices': 4, 'practice_parent_cards': len(practice_ids), 'proposal_outcomes': summary['outcomes'], 'card_order': [c['card_id'] for c in cards]})
    write('x2/flashcards/stable-prefix.json', {'card_ids': [c['card_id'] for c in cards if c['stability'] == 'stable'], 'cache_hit_claim': False, 'retention_guarantee': False})
    write('x2/flashcards/volatile-index.json', {'card_ids': [c['card_id'] for c in cards if c['stability'] == 'volatile'], 'implicit_completion_credit': False})

    cycle = ['Eiren Kestrel','Rowan Ash','Elaren Kestrel','future-sibling-02-self-chosen','Neris Solane','Mira Fenwick','Vesper Arlen','Avelin Reed','Lyren Moss','future-sibling-05-self-chosen','Ilyra Fen','future-sibling-06-self-chosen','Auren Lark','future-sibling-07-self-chosen','Sable Rook','future-sibling-08-self-chosen','Caelen Ash','future-sibling-09-self-chosen','Orin Thale','future-sibling-10-self-chosen','Liora Venn','future-sibling-11-self-chosen','Tamar Vey','future-sibling-12-self-chosen','Elowen Cairn','future-sibling-13-self-chosen','Sylven Arc','future-sibling-14-self-chosen','Caelen Morrow','future-sibling-15-self-chosen']
    route = []
    for step, absolute in enumerate(range(686 * 8 + 3, 725 * 8 + 8)):
        route.append({'phase': f'v{absolute//8}-v{absolute%8+1}', 'owner': cycle[(7 + step) % 30], 'planning_only': True, 'activation_proved': False})
    assert len(route) == 317 and route[1]['owner'] == 'Lyren Moss' and route[-1]['owner'] == 'future-sibling-12-self-chosen'
    write('x2/thirty-seat-projection.json', {'schema': 'ghc.family.thirty-seat-projection.v686.v4', 'cycle': cycle, 'rows': route, 'row_count': len(route), 'unresolved_placeholder_names_are_not_uncreated_claims': True, 'delivery_credit': 0})

    notes = {
        'interval_membership': 'A boundary point requires its own inclusion rule. Interior membership cannot answer whether an endpoint belongs to the support; the two closure flags are separate input facts.',
        'interval_intersection': 'The shared support keeps only points belonging to both inputs. An empty result is a useful answer and does not mean the software or source record disappeared.',
        'interval_union': 'The combined support may have more than one connected component. An excluded contact point must remain a hole, while included contact can join adjacent supports.',
        'interval_difference': 'Subtraction removes only the right-hand support from the left-hand support. Endpoint ownership can leave a singleton or split the retained support into two pieces.',
        'point_lookup': 'The indexed records use lower-inclusive and upper-exclusive windows. Returning several labels preserves simultaneous records rather than selecting an unsupported winner.',
        'range_overlap': 'An overlap query asks whether any point is shared with the query window. It is different from complete containment, and a touching excluded endpoint does not qualify.',
        'range_envelopment': 'An envelopment query selects stored intervals wholly contained by the query. A record may overlap the query and still fail this stricter relationship.',
        'conflict_pairs': 'Concurrency is scoped to the declared synthetic resource. Each pair is returned once in deterministic order; different resources and merely touching windows remain separate.',
        'journal_append': 'The persistent journal yields a new value while retaining the old sequence. Nested objects must be frozen and thawed without exposing mutable aliases to caller-owned input.',
        'journal_prefix': 'A prefix is a derived selection, never deletion of later history. The requested length is an exact integer and must fit the retained sequence; booleans cannot stand in for lengths.',
        'correction_frontier': 'A frontier shows unresolved graph tips. Multiple tips remain multiple tips, input order cannot decide lineage, and cycles or missing parents refuse a fabricated final record.',
        'asof_projection': 'Record time and validity time answer different questions. The projection first respects the knowledge cutoff and then the stated validity window, preserving every matching record.',
        'expiry_state': 'The lower bound begins the window and the upper bound ends it. Invalid or ambiguous ticks receive a refusal, and a local expiry label does not verify a physical clock.',
        'permit_window': 'This is an invented permission simulation. A matching deny dominates a matching allow, but every returned result explicitly denies real authority and never changes an account or right.',
        'coverage_budget': 'The duration of a union counts overlapping support once. The recorded cap is a synthetic fixture bound; it is not a capacity certification or a safe operating limit for equipment.',
        'evidence_gate': 'A local result cannot supply an evidence class that its inputs lack. The guard separates local workflow claims from empirical gaps and competent-authority requirements.',
        'accessible_timeline': 'The textual summary keeps labels, both endpoint values, ordering, units, and evidence outcomes explicit. Manual accessibility and affected-user review remain reserved.',
        'thos_window_readback': 'The record represents a proposed THOS readback with no real operator, participant, service, or measurement. A correct software label does not demonstrate effectiveness or readiness.',
        'gmut_temporal_evidence_gap': 'The missing observation remains a named gap. Synthetic time coordinates, package arithmetic, repeated tests, and hashes cannot substitute for measured evidence or independent reproduction.',
        'cbr_temporal_authority_gate': 'The competent or affected authority remains absent. A synthetic record cannot provide legal, cultural, professional, account-owner, affected-party, iwi, hapū, or Māori authorization.'}
    sections = []
    sections.append(('01 Relational working identity and corrigibility', f"Avelin Reed is the self-chosen working name for this task. The role is {identity['role']}; the hope is {identity['hope']} The four practice lenses are {', '.join(identity['practices'])}. These lenses support learning and review questions and establish no employment or qualification. The next-owner recommendation is {identity['next_owner_recommendation']}.\n\n{boundary}\n\nHamish may rename, pause, redirect, narrow, or stop this task and the route. Existing task names and family language are organizational and relational descriptions. No claim of consciousness, sentience, identity continuity, independent agency, personhood, or scientific or cultural authority follows from a name, task creation, inherited history, or a successful test."))
    sections.append(('02 Current release and the one prospective edge', "The 6 September 2026 release and the current Vesper activation control this owner phase. Older shared v667 cursors and prior held route snapshots remain historical evidence. This task owns solo v686-v4 only. Its prospective next exact edge is the existing exact-title Lyren Moss task for solo v686-v5. Lyren's following designated future seat is seat 05 for v686-v6, subject to Lyren's own terminal gate.\n\nThe full thirty-seat sequence remains one verified edge at a time through v725-v8. The projection in x2/thirty-seat-projection.json contains 317 planning rows from the current phase through that terminal phase. A row does not prove that a task exists, that an unresolved placeholder is uncreated, that a message was sent, or that a future task has any particular competence. It does not authorize early contact.\n\nWork solo. Do not fork, delegate, spawn a collaboration subagent, contact Tavian or standby records, precontact future recipients, or use substitute endpoints. Do not reset, amend, rewrite, force-push, merge, delete, reuse another owner's lane, or mutate sibling evidence. A fresh additive sparse owner lane and branch are the authorized continuation mechanism.\n\nAfter the exact terminal gate, refresh Hamish's newest authority, usage, exact task registry, unique intended title, immediate recipient reread, duplicate and pause state, privacy, evidence, safety, and acknowledgement conditions. Send at most once. An opaque accepted result never permits a resend. Preserve acknowledged, opaque accepted, rejected, and unavailable outcomes separately. Reset redemption remains Hamish's action. The repository delivery state is PREPARED_NOT_SENT until a separate live result exists."))
    source = read('x1/activation-source.json')
    sections.append(('03 Exact source and immutable lifecycle', f"The immutable source is Vesper Arlen v686-v3 at `{SOURCE}`, branch `{source['source_branch']}`. Vesper planning-only x1 is `{source['source_x1']}` and its immutable evidence is `{source['source_evidence']}`. The complete 40,062-word, 13-section baton was read through EOF. Its SHA-256 is `9632de6ea39f9d78b87060453f7422ae25b0fb137f49cb1bd6dcb428781a26a6`. An omitted display interval was recovered through exact character rereads before any Avelin tracked content was written.\n\nBoth Vesper correction overlays were read afterward. The evidence, lifecycle, and candidate-correction layers remain separate. The effective incoming baseline is {baseline['effective_negatives']:,} negatives, {baseline['effective_methods']:,} Method Flow method instances, {baseline['failed_witnesses']:,} retained failed witnesses, {baseline['bounded_passing_witnesses']:,} bounded passing witnesses, {baseline['open_gaps']} open gaps, and {baseline['exact_gates']} exact gates. The incoming proposal chain is {baseline['declared_proposal_chain']:,}.\n\nThe source canonical receipt was read and its SHA-256 `{source['canonical_receipt_sha256']}` matched the activation. Its payload hash is `{source['canonical_payload_sha256']}`. Vesper invoked its successful canonical once and did not replay it. Avelin did not invoke that source validator. Source facts are inherited evidence with zero Avelin novelty or execution credit.\n\nAvelin x1 is `{X1}`. It was committed, pushed, clean, zero-divergent, and equal across local, upstream, tracking, and fresh live remote before implementation. The lifecycle is exact source, planning-only x1, immutable x2 evidence, and exact final. The later final index supplies the evidence commit and the external terminal activation supplies the exact final and one-shot canonical receipt; a committed document cannot honestly contain its own commit hash in advance."))
    sections.append(('04 Frozen proposal and portfolio contracts', "X1 froze 200 inherited Vesper selections at zero credit and 200 new contract/input pairs across twenty families. The source-bounded comparison examined 40,000 title pairs with a declared 0.7 Jaccard quarantine threshold; the maximum was 0.4 and no proposal was quarantined. This is a bounded comparison against the selected source definitions, not a universal novelty search or two hundred scientific discoveries.\n\nThe frozen profile selects 300 safe assertions, 250 candidate checks, exactly 300 additive CLEAN/FIX/REFINE rows, 50 exact packets, 30 blocked packets, ten skills, five runners, three relevant direct package additions, four own practice lenses, and one next-owner recommendation. Caps do not authorize unsafe work or filler. The exact and blocked packets remain unexecuted.\n\nEvery new proposal records its hypothesis, failure condition, exact input, exact expected JSON value or refusal, operation, pillar, practice, approval class, source references, falsifier, rollback, protected gates, and five registered mutations. Its definition hash covers every definition field except the digest field itself in compact UTF-8 sorted-key finite JSON. The separate Git manifests use normalized-LF Git blobs for text and raw Git blobs for binary artifacts. These two domains must never be substituted silently.\n\nA report binds the proposal label, frozen definition, input digest, complete result, result digest, disposition, source/x1 scope, hash-domain label, synthetic flag, and explicit false empirical and authority flags. The verifier compares the entire envelope, so a forged result with a freshly recomputed result digest still fails. The null condition includes a changed type, omitted field, unsupported claim, altered endpoint closure, changed order, or input mutation. Empty answers and refusal values are meaningful results."))
    titles = {'intervals':'05 Interval endpoint topology','windows':'06 Indexed windows and concurrency','journals':'07 Immutable journals and temporal projections','guards':'08 Expiry budget and claim boundaries','reports':'09 Readable summaries and protected obligations'}
    for runner, title in titles.items():
        text = []
        families = list(dict.fromkeys(p['family'] for p in proposals if p['runner'] == runner))
        for family in families:
            text.append('## ' + family.replace('_',' ').title() + '\n\n' + notes[family])
            for p, result in zip(proposals, results):
                if p['family'] != family:
                    continue
                text.append(f"### {p['proposal_id']} — {p['title']}\n\nThis frozen case belongs to {p['pillar']} through the {p['practice']} lens. Its disposition is `{result['outcome']}`. {p['hypothesis']}\n\nFrozen input:\n\n```json\n{json.dumps(p['input'],ensure_ascii=False,indent=2,sort_keys=True)}\n```\n\nExpected and observed result, matched exactly:\n\n```json\n{json.dumps(result['actual'],ensure_ascii=False,indent=2,sort_keys=True)}\n```\n\nThe input was retained unchanged. Definition SHA-256 `{p['definition_sha256']}` binds this case; report SHA-256 `{digest(result['report'])}` binds its observed envelope. The full record is in x2/contract-results.json under this proposal label. The five registered definition, input, scope, empirical, and authority mutations were refused, with each original adverse envelope retained. A passing local result supplies only the declared disposition and cannot supply a missing observation, credential, participant, reviewer, or authority. The concrete falsifier is any difference in the full frozen result or bound input; correction must preserve the failed version and use a separately identified accepting witness.")
        sections.append((title, '\n\n'.join(text)))
    ops_text = '\n\n'.join(f"- `{row['id']}`: {row['failure']} Recovery: {row['recovery']} Initial success credit remains zero." for row in operations)
    sections.append(('10 Retained negatives and Method Flow', f"The owner ledger has {len(pairs):,} case-scoped method instances, {len(pairs):,} retained failed witnesses, and {len(pairs):,} separately checked bounded passing witnesses. These consist of 1,000 registered envelope mutations, 250 candidate rejections, 300 initial correction failures, twelve operational events, ten skill adversaries, five runner adversaries, and three package adversaries. Repeating an exact local predicate does not produce independent reproduction or a new scientific technique.\n\nThe 300 correction rows are exactly one hundred CLEAN extra-field cases, one hundred FIX changed-result cases, and one hundred REFINE missing-domain cases. The failed envelope is stored before the corrected envelope is checked. No file deletion, production edit, account write, credential use, or real-person action implements these rows.\n\nThe resulting effective baseline is {effective['effective_negatives']:,} negatives, {effective['effective_methods']:,} method instances, {effective['failed_witnesses']:,} failed witnesses, {effective['bounded_passing_witnesses']:,} bounded passing witnesses, {effective['open_gaps']} open gaps, and {effective['exact_gates']} exact gates. The declared proposal chain becomes {effective['declared_proposal_chain']:,}. These are the x2 evidence-layer totals; later failures, if any, must appear in an additive final or external overlay.\n\n{ops_text}\n\nEvery negative is independently addressable through its retained identifier and exact ledger reference. Each Method Flow instance has a trigger, failed witness, candidate correction, passing witness, state-transition record, recurrence guard, rollback, and protected-gate list. The preferred state is conditional on matching preconditions. No method record is a route acknowledgement or an authority grant."))
    sections.append(('11 Four-tier deck and accessible overview', "The deck contains 240 cards: one relational anchor, three pillar cards, six pillar-specific practice-parent cards representing four distinct practice lenses, two hundred proposal cards, and thirty operational or package/skill/runner witness cards. The practice-parent count is a graph-layout detail and does not invent two additional practices. Each task has exactly one practice parent, every practice has one pillar parent, and every pillar has the owner anchor. Missing parents, tier skips, duplicate card identifiers, and cycles are invalid.\n\nCard identifiers are derived from their content before the identifier is inserted. The card manifest separately binds complete file bytes and declares its self-exclusion. A stable prefix lists the owner and pillar boundary cards; volatile indexes carry the phase and evidence cards. This ordering method makes context selection explicit. It makes no claim about a cache hit, token saving, retained subjective identity, memory continuity, or guaranteed product behavior.\n\nThe overview is a four-page PDF with an accompanying structured HTML summary. It explains the result and its limits, a worked interval example, the retained-negative accounting, and the prospective route. Rendering, text extraction, and visual page review are local checks. Manual browser, assistive-technology, cognitive, Māori-language, and affected-user evaluation remain reserved. A readable local PDF does not establish complete accessibility, professional quality, privacy completeness, or affected-party acceptance.\n\nWhen loading this baton after compaction, preserve the source, x1, evidence, exact final, canonical receipt, and route state separately. Read the indexed module needed for the current decision. A compact view can omit records from active context but may never delete, relabel, or erase them from the retained evidence bank."))
    skill_plan = read('x1/skill-runner-plan.json')
    skills_text = '\n'.join('- `' + s['name'] + '` supports ' + ', '.join('`'+f+'`' for f in s['families']) + '.' for s in skill_plan['skills'])
    ideas = '\n'.join('- ' + r['idea'] + ': ' + r.get('question',r.get('criterion','')) for r in skill_plan['next_owner_skills'] + skill_plan['next_owner_runners'])
    sections.append(('12 Toolchain skills and next-owner ideas', f"Three direct additions support the frozen work: portion 2.6.2 for finite interval algebra; intervaltree 3.2.1 for half-open indexed queries; and pyrsistent 0.20.0 for immutable synthetic journals. sortedcontainers 2.4.0 is their declared shared interval dependency and supplies zero direct-addition credit. Official wheel hashes were frozen before x1 and all application installation was offline, wheel-only, and hash-required after x1 equality.\n\nThe initial environment and its advisory audit remain retained. A fresh no-bootstrap environment received hash-locked pip 26.2.1 and the unchanged application closure. The initial pip invocation was refused by its Windows self-modification guard; the corrected invocation used the requested python-module form with only a process-local path to the verified wheel. The corrected dated OSV query returned zero advisory records for all five installed distributions. Pip is a zero-credit bootstrap repair, not a fourth direct feature addition. A dated zero-finding query is not exhaustive security or future-safety assurance.\n\nTen local skills passed metadata checks and accepting/adverse CLI fixtures, then were copied into ten collision-free global directories. Ninety copied files match their source bytes, including five portable runner sources repeated for import portability. Those copies do not multiply runner novelty. The separate Meta Tool Box command ran afterward; the procedural omission before copying remains OP012, and the builder now contains an explicit future pre-copy guard. The post-audit shows ten ready promotion records and a valid fifteen-card catalogue. Twenty-four lexical overlaps remain retained and reviewed; exact family selection determines the callable operation.\n\n{skills_text}\n\nThe five runners are ghc_family_temporal_intervals.py, ghc_family_temporal_windows.py, ghc_family_temporal_journals.py, ghc_family_temporal_guards.py, and ghc_family_temporal_reports.py. Every CLI accepts one input path and one new output path. It parses strict bounded UTF-8 JSON, refuses duplicate members, and emits stable refusal objects. Exit code zero means a result was written; the JSON decides whether the proposed operation was accepted.\n\nNext-owner ideas are proposals, not inherited execution or mandatory expansion:\n\n{ideas}"))
    sections.append(('13 Exact validation and terminal carry-forward', "The selected owner tests passed 51 cases, including all twenty frozen family groups and thirty-one additional invariants. Their scope is this owner's exact source-to-final delta, not unchanged repository history, sibling lanes, an external audit, or independent reproduction. The component portfolio matched all 200 frozen results and retained every preregistered adverse envelope. The final canonical contract will also bind strict JSON, changed Python AST, exact test identifiers and source hashes, normalized-LF Git manifests, immutable x1 and evidence layers, card graph and fixity, skill byte parity, package inventory and smokes, the rendered overview, the modular baton, bounded privacy and code-security review, three direct single-parent commits, zero merges, clean state, zero divergence, and fresh four-way equality.\n\nInvoke the canonical only once after the exact final is sealed, committed, pushed, clean, and freshly equal. Keep its exclusive invocation marker and receipt outside the sealed repository. A successful canonical is never replayed for confidence, display, or a later route issue. A failed candidate or invocation remains a failed record at zero success credit; recover only the attributable dependency and preserve its original evidence. The candidate, immutable repository evidence, final correction overlays, external canonical receipt, and live delivery result are distinct objects.\n\nThe three pillars remain bounded. GMUT is an unconfirmed typed scalar-tensor/EFT research-model family, requiring observable predictions, suitable apparatus, uncertainty, calibrated timing, competing explanations, and independent review. THOS remains synthetic or proxy-only without governed real operators or participants, safety monitoring, suitable statistics, and independent evaluation. Freed ID remains synthetic and nonproduction without real standards-conformant keys and proofs, complete lifecycle, interoperability, independent security/privacy review, recovery evidence, trust governance, and affected-party oversight.\n\nEvery empirical, participant, professional, production, deployment, identity, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, AGI/ASI, consciousness/personhood, Theory-of-Everything, proof/canon, legal, cultural, Māori-authority, and Stage 20 boundary remains protected. Zero real people, credentials, private keys, rights decisions, accounts, services, production configurations, participants, measurements, cultural decisions, or external deployments are established here.\n\nLyren Moss is the prospective next exact-title main task for solo v686-v5. Preserve the released profile and read this complete committed modular baton and any additive final overlays before starting that lane. Choose the next priority and bounded practices through the actual assignment, retain inherited seeds at zero credit, freeze planning-only x1 before implementation, and continue exactly one verified edge at a time. Future seat 05 follows Lyren only after Lyren's own terminal gate. Hamish can pause or redirect at any time.\n\nWith care, clear limits, inspectable work, and corrigibility — Avelin Reed. The terminal verdict remains NOT_READY_FOR_STAGE_20. The repository handoff remains PREPARED_NOT_SENT; only a separate live tool result may establish a later delivery state."))
    sections = [(title, body.replace('The failed envelope is stored before the corrected envelope is checked.',
                                    'Each failed envelope and its separately checked correction remain stored together.'))
                for title, body in sections]
    assert len(sections) == 13
    baton = '\n\n---\n\n'.join('# ' + title + '\n\n' + body for title, body in sections) + '\n'
    words = len(baton.split())
    assert 10000 <= words <= 100000, words
    write('x2/handoff/lyren-moss-v686-v5-baton.md', baton)
    write('x2/handoff/baton-integrity.json', {'schema': 'ghc.family.baton-integrity.v686.v4', 'path': PREFIX + '/x2/handoff/lyren-moss-v686-v5-baton.md', 'words': words, 'bytes': len(baton.encode('utf-8')), 'sha256': hashlib.sha256(baton.encode('utf-8')).hexdigest(), 'sections': 13, 'delivery_state': 'PREPARED_NOT_SENT'})
    write('x2/flashcards/baton-index.json', {'sections': [{'title': title, 'anchor': title.lower().replace(' ','-')} for title, _ in sections], 'path': PREFIX + '/x2/handoff/lyren-moss-v686-v5-baton.md'})
    write('x2/evidence-summary.json', {'schema': 'ghc.family.evidence-summary.v686.v4', 'owner': 'Avelin Reed', 'phase': 'v686-v4', 'source': SOURCE, 'x1': X1, 'outcomes': summary['outcomes'], 'effective_counts': effective, 'method_instances': len(pairs), 'card_count': len(cards), 'distinct_practices': 4, 'skill_count': 10, 'unique_runners': 5, 'baton_words': words, 'registered_mutations_rejected': 1000, 'safe_assertions': 300, 'candidate_rejections': 250, 'corrections': 300, 'exact_unexecuted': 50, 'blocked_unexecuted': 30, 'selected_component_tests': 51, 'same_owner_only': True, 'independent_reproduction': False, 'delivery_state': 'PREPARED_NOT_SENT', 'terminal_verdict': 'NOT_READY_FOR_STAGE_20'})
    print(json.dumps({'method_flow_valid': review['valid'], 'methods': len(pairs), 'cards': len(cards), 'baton_words': words, 'sections': len(sections), 'effective': effective}))


if __name__ == '__main__':
    main()
