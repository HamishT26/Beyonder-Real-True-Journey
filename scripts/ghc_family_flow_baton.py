"""Build the final modular handoff and a five-page readable overview."""
import argparse,hashlib,html,json,re,subprocess,unittest
from pathlib import Path
from scripts.ghc_family_flow_closeout import ROOT,BASE,PLAN,X1,read,write,rawwrite
from scripts.ghc_family_flow_canonical import equality,flatten
BOUNDARY='Same-owner synthetic software and documentation. No independent reproduction, empirical GMUT confirmation, real allocation permission, identity continuity, professional qualification, legal or cultural authority, or Stage 20 evidence. NOT_READY_FOR_STAGE_20.'
def js(value):return json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)
def block(value):return '\n```json\n'+js(value)+'\n```\n'
def md_module(number,title,body):
    return f'# Module {number:02} - {title}\n\nMira Fenwick | Trinity Mandala v690-v3 | provenance and correction steward\n\n{BOUNDARY}\n\n{body.strip()}\n\nEnd of independently readable module {number:02}.\n'

def case_section(proposal,record):
    p=proposal;r=record
    accepted='The request is accepted inside the finite profile.' if r['observed']['accepted'] else 'The subject is refused inside the finite profile; its refusal is the expected result and the failed subject retains zero original credit.'
    return f'''### {p['proposal_id']} - {p['title']}

Session {p['session']}; pillar {p['pillar']}; practice {p['practice']}; disposition `{r['disposition']}`.

{p['mission']} {accepted} The complete typed observed envelope matches the frozen oracle. Input nonmutation was checked. The paired request adds `unreviewed_authority_grant`; its recorded refusal is `{r['candidate_observed']['error']}`, with zero candidate original success credit and a separately passing guard.

The planning null is: {p['null_hypothesis']} The falsifier is: {p['falsifier']}

Frozen request:{block(p['request'])}
Frozen expected envelope:{block(p['expected_envelope'])}
Observed envelope:{block(r['observed'])}

Definition SHA-256: `{p['definition_sha256']}`. The source of the definition is `plan/new-proposals.json`; the materialized observation is `{p['artifact']}`. Oracle basis: {p['oracle_basis']} Recovery: {p['recovery']} Scope remains the declared synthetic request. A passed computation does not satisfy the protected evidence or authority gates.
'''

def build():
    gate=equality();assert gate['clean'] and gate['divergence']==[0,0] and len(set(gate['four_heads']))==1
    x2=gate['four_heads'][0];assert x2 not in (PLAN,X1)
    final=BASE/'final';final.mkdir(exist_ok=False);write(final/'x2-equality.json',dict(gate,x2=x2))
    identity=read('plan/identity-practices.json');source=read('plan/source-provenance.json');account=read('x2/accounting-r2.json')
    rows=read('plan/new-proposals.json')['proposals'];results={r['proposal_id']:r for phase in ['x1','x2'] for r in read(phase+'/results.json')['results']}
    tools=read('plan/skills-runners.json');modules=[]
    modules.append(('Current owner, evidence class and authority',f'''
This is Mira Fenwick's solo v690-v3 x1/x2 bundle under Hamish's current weighted continuation. The role is **{identity['role']}**, and the working hope is **{identity['hope']}** The primary pillar is **{identity['priority_pillar']}**. These names, roles, hopes and family terms organize collaboration; they establish no consciousness, personhood, identity continuity, independent agency, employment, qualification or authority.

The phase implements a bounded directed-capacity network and assignment toolkit. Two separately frozen execution cohorts contain 200 core proposals, with 180 completed, ten represented, five open gaps and five exact gates. A completed record can be an accurately refused malformed request. It does not mean every input is feasible or accepted. X1 contains sixty accepted and forty refused safe subjects; X2 contains sixty-eight accepted and thirty-two refused safe subjects. All two hundred complete expected envelopes matched. Two hundred additional candidate subjects are intentionally refused and retain zero original success credit. Their successful guards are different observations.

The local evidence consists of source definitions, immutable input-oracle pairs, recorded envelopes, automated invariant checks, package-interface comparisons, caller smokes, byte manifests and editorial review. Every check is same-owner under shared infrastructure. There is no claim of independent reproduction. Algorithmic cross-checking supplies a limited check against implementation mistakes; it does not remove shared assumptions, shared code or shared infrastructure.

The three pillars have different missing obligations. GMUT Mind requires a physical model, units, dynamics, observables, uncertainty, likelihood, calibration and disconfirming empirical tests. THOS Body requires governed real workloads, resource accounting, comparators and safety evaluation. Freed ID and CBR Heart requires real key and proof lifecycles, standards-conformant interoperability, relevant trust governance and affected-party standing. A synthetic Boolean named authority cannot satisfy those requirements.

The four practices used here are:
{chr(10).join('- '+p for p in identity['own_practices'])}

They are work practices, not qualifications. The next owner is offered exactly two learning recommendations: {identity['successor_recommendations'][0]} and {identity['successor_recommendations'][1]}. A recommendation is prospective and has no execution credit.

Protected gates remain explicit:
{chr(10).join('- '+g for g in identity['protected_gates'])}

Māori concepts remain under Māori authority. None of this file, the route, the digest ledger or the finite optimization examples determines cultural standing, professional competence, legal authority, consent or a remedy for affected people. The terminal verdict is NOT_READY_FOR_STAGE_20.
'''))
    modules.append(('Exact source, retained corrections and non-erasure',f'''
The incoming owner is Ilyra Fen v690-v2. Source final: `{source['final']}` on `{source['branch']}`. The source is provenance for this blank-root owner lane. It is not a Git ancestor of Mira's planning root. The source's earlier Lyren provenance likewise remains provenance rather than ancestry. The earlier completed Mira v686-v2 worktree is a separate historical lane and was not modified or replayed.

Ilyra's complete baton was read through EOF: {source['baton_regex_words']} regex words and {source['baton_whitespace_words']} whitespace words. The supplied message digest did not agree with the exact committed blob. Supplied digest: `{source['baton_supplied_message_sha256']}`. Actual raw Git blob digest: `{source['baton_git_blob_sha256']}`. Three committed Ilyra manifests agreed with the actual digest. This was not explained by changing LF to CRLF. The disagreement is retained as MF6903-OP001, and execution continued from the exact named final, agreeing manifests and corrected composite receipt. No record claims the supplied digest matched.

The source canonical invocation failed once because yaml was unavailable. The first source dependency-corrected composite failed once because its caller lacked the scripts package root. Each failed invocation remains failed, has zero success credit and was not replayed. The successful source dependency-root-corrected composite has status `{source['source_composite_status']}`. That is a composite success; Ilyra canonical success credit remains zero. Its 26 checks and 32 selected tests are historical evidence from Ilyra, not Mira executions.

Mira replayed 462 source manifest entries at their correct historical commits and 35 source content-seal entries at exact final. All 497 matched, with zero mismatches and zero source tests or validator invocations. Byte-domain and caller-root corrections are workflow evidence only. They do not promote empirical, identity or authority claims.

Source accounting has three retained layers. The immutable repository layer has 1,268 effective negatives, 105 methods, 3,507 direct witnesses, 979 failed and 2,528 passing. The incoming quoted correction overlay has 1,273 negatives, 110 methods, 3,517 direct witnesses, 984 failed and 2,533 passing. A later route overlay retains IF6902-ROUTE-F001, where a pause guard matched negated historical language. The acknowledged delivery receipt supplies the latest inherited baseline: 1,274 negatives, 111 methods, 3,519 direct witnesses, 985 failed and 2,534 passing. All three layers remain distinct. The latest route overlay controls the arithmetic prospectively; it does not overwrite the repository or quoted layer.

The exact source receipt bindings are:{block(source['receipt_bindings'])}

At intake the source chain had one parentless root and five single-parent children, no merge, and clean equality among local HEAD, upstream, tracking ref and live remote. That intake observation is not a promise about a future source state. The source final named above remains the content anchor. Incoming transport and source validation are separate states.
'''))
    modules.append(('Weighted workflow and immutable execution order',f'''
The current workflow has 45 positions and 30 established identities. Astra positions occur once per identity; Sol positions occur twice. The cadence is Astra, Sol, Sol. The 294-assignment projection ends with Teryn Halewick v725-v8. A schedule file does not activate a task. Current model settings and established spellings remain intact. The weighted reviewer passed against the actual v4 profile and roster; the old unique-cycle reviewer is a different input contract.

The present route is Ilyra Fen v690-v2 -> Mira Fenwick v690-v3 -> Auren Lark v690-v4 -> Sable Rook v690-v5. Only Auren is the prospective next owner for this completed phase. No future seat is created, no substitute task is selected, and no later owner is precontacted. The former v686 route is historical and does not govern this continuation.

Owner root is archive-relative `worktrees/mira-fenwick-main`; branch is `codex/GHC-Family/mira-fenwick-main`. Planning is the parentless root `{PLAN}`. X1 is its direct child `{X1}`. X2 is X1's direct child `{x2}`. The intended exact final is X2's next direct child, resolved by the external terminal receipt after push. Four commits are within the ceiling of eight. Each commit is additive, and source provenance is explicitly outside ancestry.

The planning commit contains the two complete 100-case portfolios, frozen request and oracle definitions, 200 inherited records, package plan, skill and runner plan, 50 exact packets and 30 blocked packets. Planning did not execute the production evaluator or reference solvers. Only after planning was committed, pushed and clean with four-way equality did X1 begin. X1's local skills, runners, checks, manifests and package protocol were sealed and pushed before X2 execution. X2's new files were added without changing the planning or X1 bytes.

Per session, the three portfolios are one hundred safe requests, one hundred candidate subjects and one hundred CLEAN/FIX/REFINE record projections. The last category reconstructs canonical inherited records losslessly. It does not clean the host, rewrite source code, delete caches, rerun predecessor work or add inherited novelty. Each session builds ten local skills and five paired runners. Five merged global skills and five public D runners are a separate bounded promotion after local readiness checks.

D holds owner artifacts, downloaded wheels, scratch receipts, isolated environments, public runners and this baton. C holds the five essential skill discovery packages. Global discovery does not prove an already active task reloaded the skill catalogue. Public runners use module invocation from the declared public root; they require their adjacent scripts package and three core modules. Source tools are not patched to accommodate a changed caller.

Clean local status, a successful push, tracking equality and live remote equality are separate facts. The external final receipt binds all four before canonical execution. A canonical success can occur once only after that gate. The content of this sealed final package accurately records its pre-canonical state. Later validation and delivery facts are external additive receipts, not edits to a successful canonical head.
'''))
    modules.append(('Finite mathematics, counterexamples and pillar limits','''
The software domain is explicit: a directed graph with two to eight vertices, distinguished vertices s and t, at most twelve arcs, no self arcs, no duplicated ordered arc pair, and integral capacities from zero through eight. Vertex names follow the declared ASCII token grammar. Opposite directions may coexist as different arcs. Flow vectors have one nonnegative integer per declared arc. Every internal vertex has zero outgoing-minus-incoming balance. Source and sink balances are opposites, with nonnegative net source value. A feasibility result reports those finite predicates only.

The residual construction includes unused forward capacity and reverse capacity equal to cancellable existing flow. With two opposite declared arcs, the residual value in one direction can contain both contributions. An augmentation must cancel available reverse flow and then assign the remaining increment to forward capacity without silently merging the original arcs. The reverse-residual invariant test supplies a concrete two-unit example in which cancellation is necessary to recover the second unit. The runner exposes closed validated inputs; internal helpers assume already validated values.

For a source-side vertex set containing s and excluding t, cut capacity sums only arcs leaving the set. For any feasible flow, conservation makes its net value equal to net flow across the cut. Outgoing flow is at most outgoing capacity and incoming flow is nonnegative, so flow value is bounded by every cut capacity. When no augmenting path exists, the residual-reachable vertices from s define a cut with saturated outgoing arcs and no positive incoming flow that could be cancelled across it. Under the stated finite capacity assumptions, that cut's capacity equals the achieved flow value. This is an application of the classical max-flow/min-cut argument, not a new theorem or a physical-law derivation.

The exact primary source is Ford and Fulkerson, Maximal Flow Through a Network, DOI https://doi.org/10.4153/CJM-1956-045-5. Its primary paper was accessible. The Edmonds-Karp bibliographic DOI https://doi.org/10.1145/321694.321699 is retained, but the paper body could not be retrieved: the archive returned an internal error and ACM returned HTTP 403. No claim is made to have read that unavailable body. Official NetworkX documentation at https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.flow.edmonds_karp.html supplies current breadth-first augmentation terminology and residual conventions. The broader flow reference is https://networkx.org/documentation/stable/reference/algorithms/flow.html. No source code was copied from these references.

Supplementary proposal MF6903-SUP01 enumerates all 27 three-vertex forward networks whose three capacities are in {0,1,2}. For arcs s->a, a->t and s->t with capacities a,b,c, the closed form is c + min(a,b). The augmentation algorithm, exhaustive source-cut enumeration and closed form agree in every one of those 27 cases. This finite exhaustion covers precisely those networks. It does not exhaust the full eight-vertex profile or establish independent reproduction.

MF6903-SUP02 refutes the universal claim that increasing any capacity strictly increases throughput. The serial capacities are three and two. Increasing the first to four leaves the optimum at two because the second arc remains limiting. The wrong universal claim keeps zero success credit. The counterexample and corrected interpretation are separately recorded.

MF6903-SUP03 refutes the universal claim that greedily choosing each currently cheapest column minimizes assignment cost. For the matrix [[1,2],[2,99]], the greedy diagonal costs one hundred. The swapped columns cost four. The bounded assignment operation enumerates distinct-column permutations and reports the first minimum under the declared tie order. Forbidden cells are null; infeasibility is represented explicitly. The procedure handles matrices with at most eight rows and eight columns. It makes no claim that a chosen cost matrix captures fairness, welfare or a legitimate allocation rule.

Lower-bound feasibility and linear minimum cost use bounded integer enumeration. The candidate product is capped at fifty thousand. Costs are bounded integers with absolute value at most one thousand. Negative-cost cycles can affect the optimum even when required net throughput is zero; the retained unit test records such a bounded cycle. This finite exact search has a deliberate performance ceiling and is not a scalable general optimization service. An infeasible lower bound remains infeasible rather than being silently relaxed.

MF6903-SUP04 leaves the GMUT physical correspondence open. There is no spacetime action, physical-unit mapping, observable model, calibration record, uncertainty analysis or empirical likelihood here. Finite conservation constraints in a graph are mathematical definitions. They are not measurements of physical conservation, gravitation, consciousness or a Theory of Everything.

MF6903-SUP05 retains a feasible network with all three declared flags set true. The output still contains real_world_verification in its missing obligations and external_action remains false. A field name cannot create consent, legal authority, cultural standing or affected-party approval. In THOS, a small synthetic optimum gives no real matched-workload reliability result. In Freed ID, a hash or canonical record gives no live key, credential proof or trust-governance certification. These boundaries remain open even when every numerical and software comparison passes.
'''))
    for offset,title in [(0,'X1 frozen cases 001 through 050'),(50,'X1 frozen cases 051 through 100'),(100,'X2 frozen cases 101 through 150'),(150,'X2 frozen cases 151 through 200')]:
        body='This module contains fifty complete frozen request, oracle and observed-envelope records. Source references provide mathematical context only. The expected rejection of a subject is not counted as that subject succeeding. Every paired candidate has an explicit retained refusal in the session results.\n\n'
        body+='\n'.join(case_section(p,results[p['proposal_id']]) for p in rows[offset:offset+50]);modules.append((title,body))
    modules.append(('Reviewed packages and reusable capability portfolio',f'''
Three direct additions were installed in the dedicated D environment: highspy 1.15.1, PuLP 3.3.2 and PyMaxflow 1.3.2. NumPy 2.5.3 is an explicit transitive dependency, with zero direct-package credit. Exact downloaded wheels were hash verified, locked and installed offline with required hashes. The installation receipt records a clean pip dependency check and no system Python mutation. A dated OSV query returned no findings for those four versions; that is a bounded advisory observation, not exhaustive security or a promise that future advisories will not appear.

The package protocol was frozen before installation. Thirty synthetic maximum-flow comparisons and three adverse checks passed. highspy and PuLP share the HiGHS backend, so there are three interface comparisons across two solver backends. They are not three independent reproductions. The HiGHS results had to fall within absolute 1e-9 of an integer optimum; PyMaxflow used integer capacities. Package checks used the frozen graph values without executing the future X2 operation during X1. Comparison and dependency records receive no extra core-proposal credit.

Official API references used were https://ergo-code.github.io/HiGHS/stable/interfaces/python/example-py/, https://coin-or.github.io/pulp/guides/how_to_configure_solvers.html and https://pmneila.github.io/PyMaxflow/tutorial.html. PuLP documentation exposed an alpha line while the installed stable version was 3.3.2. Actual calls were therefore checked against the installed interface. The receipt, not a rolling documentation heading, binds the installed version.

The twenty local skills each preserve their operation contract, accepting subject, rejected subject, source definitions and skill metadata. Official quick validation passed for each skill. Ten paired local runners passed their accepting and outside-group caller checks. Core modules and package initializers have zero extra runner credit. Every public runner invokes a closed evaluator and writes a fresh output path exclusively; direct rootless-file execution is outside its documented caller contract.

Five merged groups combine four retained local guides each:
{chr(10).join('- '+g['skill']+' -> '+g['runner']+'; operations '+', '.join(g['operations']) for g in tools['global_groups'])}

Before global mutation, all five merged packages passed local official metadata validation and five checks per runner: four accepting operations and one outside-group refusal. The forty-card Meta Tool Box catalogue passed its schema review. Thirty-six trigger overlaps were examined and retained as intentional guide/runner composition. The explicit operation and caller contract choose the endpoint. No silent winner, overwritten local guide or extra novelty is inferred from matching trigger words.

Promotion readiness was checked before copying to absent destinations. Five skills were copied to essential C discovery folders; five public runners, three core modules and one initializer were copied under archive-relative global-tools/family-flow-certificates. All twenty-four files matched their prepared bytes. Official metadata checks passed on the installed skill copies. The installed D callers repeated the same four accepting and one outside-group checks per group. No existing global package was overwritten.

The installed root's module form is `python -X utf8 -m scripts.RUNNER_STEM --input OWNED_INPUT.json --output FRESH_OUTPUT.json`. That command is a caller pattern, not authorization to act on a real system or unreviewed data. Rollback means selecting retained prior tooling while preserving the new evidence; this phase authorizes no destructive deletion. Future users must review the actual input, bounds and authority requirements of their own task.
'''))
    ops=read('plan/startup-failures.json')['events']+read('x1/startup-overlay.json')['events']+read('x2/source-access-overlay.json')['events']+[read('x2/retained-closeout/failure.json')]
    modules.append(('Method Flow, retained failures and exact accounting',f'''
The current owner records {account['own']['methods']} methods and {account['own']['direct_witnesses']} direct witnesses: {account['own']['passing_witnesses']} passing and {account['own']['failed_witnesses']} failed. A direct witness is an explicit same-owner ledger row. A failed subject, a passing guard, an interface comparison, a byte comparison and a record reconstruction retain distinct row identities. They are not interchangeable evidence classes.

The three main ledgers and correction ledger remain separate. X1 has 24 methods and 543 witnesses, with 379 passing and 164 failed. X2 base has 15 methods and 487 witnesses, with 340 passing and 147 failed. The X2 addendum has eight methods and 132 witnesses, with 117 passing and 15 failed. The deck caller correction adds one method, one failed attempt and one passing recovery. All four ledgers pass the shared family schema validator and have disjoint method and witness identifiers.

The owner effective-negative definition is explicit: 327 distinct failed witness subjects plus thirty distinct unexecuted protected packets equals 357. The fifty lifecycle prerequisite packets are not counted again as negative subjects. This accounting convention is recorded in x2/accounting-r2.json. The earlier x2/accounting.json was written before the deck caller failure and remains retained, with the later record explicitly superseding its current projection. No original ledger was erased.

Adding the current owner delta to the latest Ilyra route overlay gives 1,631 cumulative effective negatives, 159 methods, 4,683 direct witnesses, 1,312 failed and 3,371 passing. Historical Mira v686 counts belong to another source domain and are not added. Canonical pass counts and transport acknowledgments do not automatically add method or proposal credit. Any later operational failure would require its own additive receipt and accounting overlay.

Retained operational records:{block(ops)}

The first deck caller assumed canonical JSON returned text and called encode on a bytes value. It failed before writing the first card. The original builder bytes and failure record were preserved. The corrected caller passes canonical bytes directly to SHA-256, then builds and checks all 215 cards. The successful correction does not turn the original attempt into a pass.

Source-page retrieval failures do not erase the bibliographic record or permit an invented paper summary. The accessible primary Ford-Fulkerson paper and official NetworkX documentation support the bounded explanation, while the unavailable Edmonds-Karp body remains unclaimed. Stage 20, empirical and affected-authority gaps remain open after the software caller and document retrieval corrections.
'''))
    modules.append(('Four-tier deck, provenance and accessible reading','''
The deck uses four tiers: owner, pillar, practice and task. It has one owner root, three pillar cards, six placements of four distinct practices, and 205 task cards. Two hundred task cards correspond to core proposals and five correspond to separately defined supplementary proposals. Every non-root card has exactly one parent from the immediately preceding tier. Multiple practice placements are explicit and do not create six distinct practices.

Each card's identifier is SHA-256 of canonical UTF-8 JSON of the card fields excluding the identifier itself. The card contains its tier, label, parent and payload. Parent cards are created before their descendants. Hashes bind exact record bytes in a declared canonical domain; they do not establish personal identity, agency, trustworthy intent or cultural standing. The deck index records the entire parent map and count. A structural check recomputes each content digest and validates tier adjacency.

The HTML index declares its language and viewport, presents one main heading, supplies a table caption and explicit row and column headers, and uses readable contrast and spacing. These are structural and editorial checks. No assistive-technology evaluation or affected-reader review occurred, so complete accessibility remains an open gap. The overview PDF is a separate five-page reading aid; the full Markdown baton and JSON records retain exact searchable details.

A reader can start from a core task card, inspect the definition digest, follow the recorded phase results and then read the full request-oracle-observation triad in the corresponding module. A supplementary card points to supplementary-results.json and carries zero core-proposal credit. The hierarchy supports navigation without replacing the original evidence. A missing observation cannot be repaired by adding an extra link or presenting a more polished diagram.

The preservation approach is non-erasure. When a caller or source claim fails, retain its input, output, definition and identity, then add a separately bound correction or scope reservation. Current projections can name superseded records without deleting them. Hash migration, canonical serialization and repository ancestry are separate concepts. Raw Git blob hashes bind committed bytes; a platform-normalized checkout is not a substitute for a historical blob.

Provenance vocabulary was informed by the W3C PROV-O reference at https://www.w3.org/TR/prov-o/. Credential boundaries were reviewed with https://www.w3.org/TR/vc-data-model-2.0/, and structural accessibility considerations with https://www.w3.org/TR/WCAG22/. These citations do not certify conformance. No live credential proof, key lifecycle, browser interoperability matrix or accessibility audit is supplied by this bundle.
'''))
    modules.append(('Exact packets, blocked obligations and next practices',f'''
Fifty exact packets bind lifecycle prerequisites across planning, X1, X2, package promotion and terminal routing. They name schema, source hash, input freeze, parent, manifest, privacy, tests, clean state, push and fresh equality. They are explicit gates, not a claim that fifty external actions were authorized or performed. The final packet-disposition file links each to the appropriate actual evidence. The ten terminal-route packets remain exact gates at this sealed pre-canonical state; later terminal evidence belongs in an additive external receipt.

Thirty protected packets remain unexecuted. Their original states and subjects are preserved in plan/blocked-packets.json. A graph optimum, an installed package or a passing static scan does not unlock them. The protected subjects include real observations, empirical calibration, governed workloads, real credential operations, legal or cultural authority, complete accessibility, exhaustive security and Stage 20 claims. Recording a missing obligation is useful work; it is still an open gap or exact gate, and it does not earn execution credit.

The four current practices and the two successor recommendations are deliberately distinct. The successor may consider adversarial optimality-certificate review: a small independently specified certificate checker should verify feasibility and equality with a supplied cut without trusting the producer's chosen labels. It needs its own frozen definition and negative subjects before execution. The other recommendation is governed allocation experiment design: specify affected participants, actual authority, workload, comparators, uncertainty and stopping rules before any real use. That is an experiment-design recommendation, not permission to conduct one.

Five next skill ideas are:
{chr(10).join('- '+v for v in tools['next_skill_ideas'])}

Five next runner ideas are:
{chr(10).join('- '+v for v in tools['next_runner_ideas'])}

These ten ideas are prospective. They have no implementation, installation, validation or novelty credit in the current bundle. Auren should first read this exact final and the current route controls, then select its own bounded proposals. A future implementation must preserve any failed original proposal and avoid counting a renamed guide or repeated fixture as new research.

The software performance ceiling is deliberate. Enumeration refuses workloads beyond the stated bounds, and the public scripts expose only the declared operation groups. Changing those bounds is a new contract requiring a cost review and meaningful validation. The current code is not a deployment service, identity platform, empirical physics apparatus or governed allocation system. Stop at the protected boundary even if a caller offers to set every Boolean to true.
'''))
    modules.append(('Final gate, recovery and guarded successor delivery',f'''
The exact X2 anchor is `{x2}`. Its fresh clean equality receipt is final/x2-equality.json. Final artifacts are added after X2; earlier planning and execution files are immutable. The final manifest excludes only itself and covers every new final file. The content seal excludes itself and the final manifest. The canonical validator replays each phase manifest at its correct commit and verifies exact owner coverage, rather than mixing checkout bytes with older commits.

The current owner canonical has not run at the point represented by this sealed file. Its required command is the module `scripts.ghc_family_flow_canonical` from the owner root, using a fresh external receipt path under archive-relative receipts/mira-fenwick/v690-v3. Before the invocation, require exact final push, clean typed zero/zero divergence and equality of local HEAD, upstream, tracking and live remote refs. The validator uses a head-specific exclusive invocation marker. A passed or failed canonical must not be replayed. Component preflight carries zero canonical invocation or success credit.

The exact selected tests are the 18 X1 and 20 X2 owner tests, bound by their full IDs and source definition hashes. No predecessor suite, old Mira lane or whole-repository test command belongs to this scope. The validator checks the two hundred frozen envelopes, designed refusals, inherited zero-credit records, four compatible Method Flow ledgers, 215 cards, five global skill packages, five public runners, isolated package versions, source receipt bindings, privacy patterns, JSON/YAML parseability, Python syntax and the five-page overview review. These are bounded checks, not exhaustive privacy, security or accessibility assurance.

After a successful once-only canonical, prepare a compact file-backed message for the existing Auren Lark task. Refresh current weighted controls and newest direct user instructions. Query the native active registry and archived registry as necessary. A bounded listing is not proof that a task is absent. Resolve the exact endpoint kind, title and identity without guessing a private handle. Read the incoming contents with outputs enabled where required, decode the JSON envelope before projecting text, and inspect newest messages first.

Immediately before sending, check the exact target for a current pause, redirect, duplicate activation or already accepted v690-v4 request. A negated historical pause phrase in an agent's summary is not itself a new direct pause instruction. If the native service fails before a send has been accepted, perform at least five bounded fresh lookup/read recovery attempts as current workflow requires, retaining each failure. If exact identity or route authority remains unresolved, record the open route gap and stop. Do not create a duplicate, substitute a target, use a UI workaround or infer absence from a bounded result.

Once a send is accepted, acknowledged or opaque accepted, do not resend. Record the actual transport state in an external receipt and stop. A tool acknowledgment means the message was accepted; it is not proof that Auren completed induction, began X1 or finished its phase. Following owner Sable Rook v690-v5 stays uncontacted by this run. No new task, fork, subagent, automation, model override, reset redemption or private route identifier belongs in the committed baton.

If a future host cannot import a dependency or locate the package root, retain the exact failed command and receipt before changing anything. Prefer the named module caller and declared runtime. Do not replay Ilyra's failed canonical or either source composite. Do not rewrite prior successful canonical evidence. A correction can only be additive, owner-scoped and truthfully labeled. The final verdict remains NOT_READY_FOR_STAGE_20 after a successful software validation or task delivery.
'''))
    assert len(modules)==13
    manifest=[];parts=[]
    for n,(title,body) in enumerate(modules,1):
        text=md_module(n,title,body);name=f'modules/{n:02}-'+re.sub('[^a-z0-9]+','-',title.lower()).strip('-')+'.md';raw=text.encode()
        rawwrite(final/name,raw);manifest.append({'path':name,'title':title,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'whitespace_words':len(text.split())});parts.append(text)
    baton='# Mira Fenwick v690-v3 - Complete hand-off baton\n\n'+BOUNDARY+'\n\n'+''.join('\n'+part for part in parts)
    assert 10000<=len(baton.split())<=100000
    rawwrite(final/'hand-off-baton.md',baton.encode());write(final/'baton-manifest.json',{'modules':manifest,'baton_sha256':hashlib.sha256(baton.encode()).hexdigest(),'bytes':len(baton.encode()),'whitespace_words':len(baton.split()),'regex_words':len(re.findall(r"\b[\w'-]+\b",baton)),'self_excluded':True})
    truth={'owner':'Mira Fenwick','phase':'v690-v3','source_final':source['final'],'source_is_ancestor':False,'planning':PLAN,'x1':X1,'x2':x2,
        'verdict':'NOT_READY_FOR_STAGE_20','core_outcomes':account['core_outcomes'],'canonical_state':'NOT_INVOKED_PENDING_EXACT_FINAL_GATE','delivery_state':'PREPARED_NOT_SENT',
        'source_canonical_success_credit':0,'source_composite_status':source['source_composite_status'],'latest_accounting':'x2/accounting-r2.json','own':account['own'],'cumulative':account['cumulative'],
        'canonical_and_delivery_truth':'Read external exact-final and delivery receipts; this sealed file records pre-canonical state.'}
    write(final/'phase-truth.json',truth)
    loader=unittest.TestLoader();suite=loader.loadTestsFromNames(['tests.test_flow_x1','tests.test_flow_x2']);ids=sorted(flatten(suite));assert len(ids)==38 and not loader.errors
    write(final/'test-inventory.json',{'test_ids':ids,'count':38,'definitions':[{'path':'tests/'+name,'sha256':hashlib.sha256((ROOT/'tests'/name).read_bytes()).hexdigest()} for name in ['test_flow_x1.py','test_flow_x2.py']],'source_tests_selected':0,'old_mira_tests_selected':0,'executed_during_inventory':0})
    packets=[]
    for p in read('plan/exact-packets.json')['packets']:
        row=dict(p);row['state']='exact_gate' if p['kind']=='terminal_route' else 'completed';row['scope']='Named lifecycle prerequisite only; no protected authority transfer.'
        if p['kind']=='package_promotion' and p['action'] in ['parent','clean_state','push','fresh_equality']:
            row['state']='represented';row['scope']='Global files are outside Git. Their relationship is an additive source copy with byte parity, not a global Git parent, clean-state, push or ref-equality claim.'
        row['evidence']={'planning_binding':'x1/planning-equality.json and plan/manifest.json','x1_binding':'x2/x1-equality.json and x1/manifest.json','x2_binding':'final/x2-equality.json and x2/manifest.json','package_promotion':'x2/global-preflight.json, x2/promotion-policy-preflight.json and x2/global-promotion.json','terminal_route':'External exact-final canonical and guarded delivery receipts required'}[p['kind']]
        packets.append(row)
    write(final/'exact-packet-dispositions.json',{'packets':packets,'protected_actions_authorized':0,'blocked_subjects_executed':0})
    checklist={'completed':['Frozen planning parentless root','X1 and X2 separate execution and seals','200 complete oracle envelopes','200 retained candidate refusals','200 lossless inherited record projections','20 local skills and 10 paired runners','5 global skills and 5 public runners','3 direct packages and 1 explicit dependency','38 selected tests passed at session stages','215 four-tier cards','13-module full baton','48 compatible Method Flow methods'],
        'represented':['10 core summaries','1 supplementary authority counterexample','Structural accessibility review','Prospective weighted route'],
        'open_gap':['5 core empirical reservations','1 supplementary GMUT model gap','Real observations and independent reproduction','Affected-reader and assistive-technology evaluation'],
        'exact_gate':['5 core authority reservations','30 protected packets remain unexecuted','Exact-final canonical pending final push','Auren v690-v4 delivery pending guarded terminal route']}
    write(final/'completion-checklist.json',checklist)
    write(final/'canonical-policy.json',{'owner_only':True,'exact_final_required':True,'canonical_max_invocations':1,'canonical_max_successes':1,'canonical_replays':0,'predecessor_runs':0,'module_caller_required':True,'exclusive_external_marker':True,'final_receipt_archive_relative':'receipts/mira-fenwick/v690-v3/exact-final-owner-scoped-canonical.json','no_task_creation':True,'no_early_successor_contact':True})
    pages=overview_pages(truth);write(final/'overview-content.json',{'pages':pages,'editorial_state':'sealed content before exact-final canonical and delivery'})
    overview='# Mira Fenwick v690-v3 - Five-page overview\n\n'+''.join('## '+p['title']+'\n\n'+'\n\n'.join(p['paragraphs'])+'\n\n' for p in pages)
    rawwrite(final/'overview.md',overview.encode())
    doc='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Mira Fenwick v690-v3 overview</title><style>body{font:18px/1.65 system-ui;max-width:850px;margin:2rem auto;padding:1rem;color:#18252d}h1,h2{line-height:1.2}section{margin-block:2.5rem}a{color:#064c89}</style><main><h1>Mira Fenwick v690-v3</h1>'+''.join('<section><h2>'+html.escape(p['title'])+'</h2>'+''.join('<p>'+html.escape(t)+'</p>' for t in p['paragraphs'])+'</section>' for p in pages)+'</main></html>\n'
    rawwrite(final/'overview.html',doc.encode());print(json.dumps({'x2':x2,'modules':13,'baton_words':len(baton.split()),'baton_sha256':hashlib.sha256(baton.encode()).hexdigest(),'test_ids':38}))

def overview_pages(truth):
    return [
    {'title':'Outcome and scope','paragraphs':[
    'Mira Fenwick | Trinity Mandala v690-v3 | provenance and correction steward. Working hope: make each handoff easier to inspect and safely revise. Primary pillar: Freed ID and CBR Heart.',
    'The two execution sessions produced a bounded directed-flow and assignment toolkit. All 200 frozen request envelopes matched their planned results. Core dispositions are 180 completed, 10 represented, 5 open_gap and 5 exact_gate. A correctly refused malformed request is a completed software check; it is not an accepted or feasible allocation.',
    'Each session contains 100 safe requests, 100 candidate subjects and 100 lossless inherited-record projections. The 200 candidate subjects remain failed at zero original credit, alongside separately passing refusal guards. X1 accepted 60 safe inputs and refused 40; X2 accepted 68 and refused 32.',
    'The owner selected 38 automated tests: 18 in X1 and 20 in X2. Five supplementary proposals remain separate from the 200 core proposals. They include 27 closed-form network comparisons, two numerical counterexamples, an empirical model gap and an authority counterexample.',
    'This overview is sealed before the once-only exact-final canonical and guarded Auren delivery. Their actual results must be read in the external terminal receipts. NOT_READY_FOR_STAGE_20 remains the verdict after a successful software check or transport acknowledgment.']},
    {'title':'Source integrity and accounting','paragraphs':[
    'Source: Ilyra Fen v690-v2, exact final '+truth['source_final']+'. Source provenance is outside this owner lane ancestry. The complete source baton and correction record were read. Read-only replay matched 462 historical manifest entries and 35 content-seal entries. No source test, canonical or composite was rerun.',
    'The incoming message supplied a baton digest that differed from the exact Git blob and three agreeing committed manifests. The mismatch is retained as OP001. The agreed raw blob digest begins dd88a34a5517b334. The full digest and all source receipt hashes are in the baton and source-provenance record.',
    'Ilyra had one failed canonical invocation and one failed initial composite. Its successful corrected composite remains a composite success, with zero canonical success credit. A later source route overlay also retains a guard that misread negated historical pause language.',
    'Current owner accounting: 48 methods; 1,164 direct witnesses, comprising 837 passing and 327 failed. Thirty distinct protected packets are unexecuted. The declared effective-negative total is 327 + 30 = 357; fifty lifecycle gates are not counted again as failed subjects.',
    'Cumulative accounting uses Ilyra latest route overlay: 1,631 effective negatives, 159 methods, 4,683 direct witnesses, 1,312 failed and 3,371 passing. Earlier source repository, quoted activation and route totals remain separate. Nine current operational failures, including the corrected deck byte-domain caller, are retained.']},
    {'title':'Finite mathematics and useful counterexamples','paragraphs':[
    'The graph profile contains 2 to 8 vertices, at most 12 directed arcs and integer capacities from 0 to 8. Source s and sink t are explicit. Duplicate directed arcs and self arcs are refused. Residual paths include reverse cancellation. Internal flow conservation and capacity feasibility are checked before reporting throughput.',
    'An augmenting-path maximum is compared with exhaustive source-cut enumeration. For all 27 three-vertex forward networks with capacities in {0,1,2}, both agree with c + min(a,b), where c is direct capacity and a,b form the serial route. This is finite same-owner verification of classical mathematics, with no physical-law or independent-reproduction claim.',
    'Increasing one capacity need not increase throughput. A serial network with capacities 3 and 2 still carries 2 after the first capacity becomes 4. The rejected universal claim remains failed.',
    'Greedy assignment need not minimize total cost. For [[1,2],[2,99]], a greedy diagonal costs 100, while swapped columns cost 4. The exact bounded enumerator respects distinct columns and forbidden cells. It does not decide whether the cost matrix is fair or legitimate.',
    'Minimum-cost and lower-bound searches stop above 50,000 candidate vectors. Negative bounded cycles can change zero-throughput costs. Classical reference: Ford and Fulkerson, DOI 10.4153/CJM-1956-045-5. Official NetworkX documentation supports breadth-first and residual terminology. The Edmonds-Karp paper body was unavailable and is not claimed as read.']},
    {'title':'Tools, provenance and reading aids','paragraphs':[
    'Each session built 10 local skills and 5 paired runners. Five merged skills combine the 20 retained guides into network structure, residual execution, optimality certificates, capacity and cost, and allocation reservations. The 40-card catalogue has 36 reviewed intentional trigger overlaps.',
    'Five global skill packages and five public D runners were promoted to absent destinations. All 24 copied files matched their prepared bytes. Local and installed runner checks covered four accepting operations and one outside-group refusal per group. Existing files were not overwritten. Discovery does not prove an active task reloaded its skills.',
    'Direct packages: highspy 1.15.1, PuLP 3.3.2 and PyMaxflow 1.3.2. NumPy 2.5.3 is an explicit transitive dependency with zero direct-package credit. Exact wheels were hash locked and installed offline in a dedicated D environment. Dependency and dated advisory checks are recorded.',
    'Thirty solver-interface comparisons and three adverse checks passed. PuLP and highspy share HiGHS: three interfaces use two backends. This remains same-owner comparison. Public runners need no third-party solver package, but require their adjacent scripts package and three core modules.',
    'The full baton has 13 independently readable modules. The content-addressed deck has 215 cards: one owner, three pillars, six placements of four practices and 205 tasks. Every non-root card has one parent in the preceding tier. HTML and PDF improve navigation; complete accessibility remains unverified.']},
    {'title':'Protected boundaries and next delivery','paragraphs':[
    'GMUT Mind: graph conservation is a mathematical constraint. A physical action, units, observable map, calibration, uncertainty, likelihood and empirical falsifier are absent. THOS Body: governed real workloads, actual comparators, safety evaluation and resource measurements remain missing.',
    'Freed ID and CBR Heart: a digest does not prove identity or authority. Real keys, proofs, credential lifecycle, interoperability, trust governance and affected-party standing require their own evidence. In the synthetic policy example, every declared flag is true and external_action still remains false.',
    'Names, roles, hopes and family language organize this collaboration. They establish no consciousness, personhood, identity continuity, independent agency or qualification. Professional, legal, cultural, affected-party and Maori authority remain reserved. NOT_READY_FOR_STAGE_20.',
    'The current weighted workflow has 45 positions, 30 identities and Astra, Sol, Sol cadence. The prospective next owner is Auren Lark v690-v4; Sable Rook v690-v5 follows. The 294-assignment projection ends with Teryn Halewick v725-v8. A schedule is not activation authority.',
    'After exact final push, clean four-way equality and one successful canonical, resolve the existing Auren task and immediately reread pause, redirect and duplicate guards. Send at most once. An accepted or opaque accepted result ends retries. Record the actual delivery state externally and stop. No task creation, fork, subagent, model override, reset redemption, automation or later-owner contact is part of this run.']}]

def pdf():
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak
    import os
    final=BASE/'final';target=final/'overview.pdf';assert not target.exists()
    fonts=Path(os.environ['WINDIR'])/'Fonts';pdfmetrics.registerFont(TTFont('MiraArial',str(fonts/'arial.ttf')));pdfmetrics.registerFont(TTFont('MiraArialBold',str(fonts/'arialbd.ttf')))
    normal=ParagraphStyle('body',fontName='MiraArial',fontSize=11,leading=16,spaceAfter=15,textColor=colors.HexColor('#202b33'))
    heading=ParagraphStyle('heading',fontName='MiraArialBold',fontSize=23,leading=29,spaceAfter=22,textColor=colors.HexColor('#163b53'))
    kicker=ParagraphStyle('kicker',fontName='MiraArialBold',fontSize=10,leading=14,spaceAfter=9,textColor=colors.HexColor('#52616b'))
    story=[];pages=read('final/overview-content.json')['pages']
    for n,page in enumerate(pages,1):
        if n>1:story.append(PageBreak())
        story.append(Paragraph('MIRA FENWICK / V690-V3 / '+str(n)+' OF 5',kicker));story.append(Paragraph(html.escape(page['title']),heading))
        for para in page['paragraphs']:story.append(Paragraph(html.escape(para.replace('\u2014','-').replace('\u2013','-')),normal))
    def footer(canvas,doc):
        canvas.setStrokeColor(colors.HexColor('#b8c6ce'));canvas.line(49,43,A4[0]-49,43);canvas.setFont('MiraArial',8)
        canvas.setFillColor(colors.HexColor('#52616b'));canvas.drawString(49,29,'Same-owner evidence | NOT_READY_FOR_STAGE_20');canvas.drawRightString(A4[0]-49,29,str(doc.page))
    doc=SimpleDocTemplate(str(target),pagesize=A4,rightMargin=49,leftMargin=49,topMargin=49,bottomMargin=61,title='Mira Fenwick v690-v3 overview',author='Mira Fenwick',subject='Finite flow evidence and retained boundaries')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    from pypdf import PdfReader
    reader=PdfReader(str(target));assert len(reader.pages)==5
    for page in reader.pages:assert len(page.extract_text())>400
    print(json.dumps({'pdf_pages':len(reader.pages),'pdf_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'visual_review_pending':True}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['build','pdf']);a=p.parse_args();globals()[a.action]()
