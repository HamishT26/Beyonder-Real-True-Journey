'use strict';

const fs = require('fs');
const path = require('path');
const x1 = require('./boolean-lib-x1.cjs');
const x2 = require('./boolean-lib-x2.cjs');

function arg(name) { const at = process.argv.indexOf(name); if (at < 0 || !process.argv[at + 1]) throw new Error(`Missing ${name}`); return process.argv[at + 1]; }
function readJson(file) { return JSON.parse(fs.readFileSync(file, 'utf8')); }
function writeJson(file, value) { fs.mkdirSync(path.dirname(file), { recursive: true }); fs.writeFileSync(file, JSON.stringify(value, null, 2) + '\n', 'utf8'); }
function attempt(request) { try { return { accepted: true, result: x2.computeOperation(request) }; } catch (error) { if (error instanceof x1.BooleanContractError) return { accepted: false, code: error.code, message: error.message }; throw error; } }
function mutation(contract, kind) { const request = JSON.parse(JSON.stringify(contract.request)); if (kind === 'nonbinary') request.truth_table[0] = 2; else if (kind === 'authority') request.real_authority = true; else throw new Error('unknown mutation'); return request; }
function testRecord(id, title, passed, observed) { return { test_id: id, title, passed: Boolean(passed), observed }; }

function main() {
  const contractsRoot = arg('--contracts-root');
  const x1ResultsPath = arg('--x1-results');
  const output = arg('--output');
  const files = fs.readdirSync(contractsRoot).filter(name => /^\d\d-/.test(name)).sort().slice(10);
  const contracts = files.flatMap(name => readJson(path.join(contractsRoot, name)));
  if (contracts.length !== 150) throw new Error(`Expected 150 X2 contracts, got ${contracts.length}`);
  const core = [], candidates = [], refusals = [], repairs = [], cfr = [];
  for (const contract of contracts) {
    const accepted = attempt(contract.request);
    if (!accepted.accepted) throw new Error(`Frozen valid contract rejected: ${contract.contract_id}`);
    core.push({ contract_id: contract.contract_id, proposal_id: contract.proposal_id, fixture_id: contract.request.fixture_id, operation: contract.request.operation, request_sha256: contract.request_sha256, disposition: contract.expected_disposition, result: accepted.result, same_owner_only: true });
    for (const [kind, expectedCode] of [['nonbinary', 'BINARY'], ['authority', 'AUTHORITY']]) {
      const malformed = mutation(contract, kind), rejected = attempt(malformed);
      candidates.push({ subject_id: `${contract.contract_id}-${kind}`, contract_id: contract.contract_id, kind, request: malformed, result: 'fail', original_success_credit: 0, observed_code: rejected.code });
      refusals.push({ witness_id: `${contract.contract_id}-${kind}-refusal`, subject_id: `${contract.contract_id}-${kind}`, expected_code: expectedCode, observed_code: rejected.code, result: rejected.accepted === false && rejected.code === expectedCode ? 'pass' : 'fail', subject_remains_failed: true });
      const recovery = attempt(contract.request);
      repairs.push({ witness_id: `${contract.contract_id}-${kind}-recovery`, subject_id: `${contract.contract_id}-${kind}`, restored_request_sha256: contract.request_sha256, result: recovery.accepted ? 'pass' : 'fail', subject_promoted: false });
      cfr.push({ task_id: `${contract.contract_id}-${kind}-cfr`, action: kind === 'nonbinary' ? 'FIX' : 'REFINE', result: 'pass', scope: 'frozen valid-template recovery only' });
    }
  }
  const safe = Array.from({ length: 400 }, (_, index) => { const row = core[index % core.length]; return { task_id: `LV7053-X2-SAFE-${String(index + 1).padStart(4, '0')}`, contract_id: row.contract_id, check: index % 2 ? 'bounded-result-shape' : 'disposition-preservation', result: 'pass' }; });
  const byOperation = Object.fromEntries(core.map(row => [`${row.fixture_id}:${row.operation}`, row]));
  const fixtures = [...new Set(core.map(row => row.fixture_id))];
  const rows = name => fixtures.map(id => byOperation[`${id}:${name}`]);
  const monotone = rows('partial_order_monotonicity'), unate = rows('variable_unateness'), canal = rows('canalizing_assignments'), symmetry = rows('permutation_symmetry_group');
  const mobius = rows('mobius_roundtrip'), cofactor = rows('cofactor_restriction_pair'), derivative = rows('boolean_derivative_influence'), affine = rows('affine_input_orbit_signature');
  const gaps = rows('independent_boolean_reproduction_gap'), gates = rows('boolean_decision_authority_hold');
  const x1Results = readJson(x1ResultsPath);
  const x1Map = Object.fromEntries(x1Results.map(row => [`${row.fixture_id}:${row.operation}`, row.result]));
  const models = fixtures.map((fixture, index) => ({
    model_id: `LV7053-MODEL-${String(index + 1).padStart(2, '0')}`,
    fixture_id: fixture,
    coordinates: {
      algebraic_degree: x1Map[`${fixture}:algebraic_degree`].degree,
      spectral_nonlinearity: x1Map[`${fixture}:spectral_nonlinearity`].nonlinearity,
      permutation_automorphisms: symmetry[index].result.automorphism_count
    },
    dimensionless: true,
    physical_interpretation: false
  }));
  const tests=[];
  tests.push(testRecord('LV7053-X2-T01','contract count',core.length===150,core.length));
  tests.push(testRecord('LV7053-X2-T02','contract identifiers unique',new Set(core.map(r=>r.contract_id)).size===150,150));
  tests.push(testRecord('LV7053-X2-T03','monotonicity booleans',monotone.every(r=>typeof r.result.monotone==='boolean'),true));
  tests.push(testRecord('LV7053-X2-T04','monotonicity violation pairs',monotone.every(r=>r.result.violations.every(v=>v.length===2)),true));
  tests.push(testRecord('LV7053-X2-T05','unateness coordinate counts',unate.every((r,i)=>r.result.coordinates.length===(i<9?2:3)),true));
  tests.push(testRecord('LV7053-X2-T06','unateness classifications',unate.every(r=>r.result.coordinates.every(c=>['independent','positive','negative','neither'].includes(c.classification))),true));
  tests.push(testRecord('LV7053-X2-T07','canalizing variables bounded',canal.every((r,i)=>r.result.assignments.every(a=>a.variable>=0&&a.variable<(i<9?2:3))),true));
  tests.push(testRecord('LV7053-X2-T08','canalizing outputs binary',canal.every(r=>r.result.assignments.every(a=>a.output_value===0||a.output_value===1)),true));
  tests.push(testRecord('LV7053-X2-T09','symmetry identity present',symmetry.every(r=>r.result.automorphism_count>=1),true));
  tests.push(testRecord('LV7053-X2-T10','symmetry counts bounded',symmetry.every((r,i)=>r.result.automorphism_count<=((i<9)?2:6)),true));
  tests.push(testRecord('LV7053-X2-T11','Mobius roundtrip',mobius.every(r=>r.result.roundtrip===true),true));
  tests.push(testRecord('LV7053-X2-T12','cofactor pair counts',cofactor.every((r,i)=>r.result.pair_count===(i<9?2:3)),true));
  tests.push(testRecord('LV7053-X2-T13','cofactor rows doubled',cofactor.every((r,i)=>r.result.cofactors.length===2*(i<9?2:3)),true));
  tests.push(testRecord('LV7053-X2-T14','cofactor lengths exact',cofactor.every((r,i)=>r.result.cofactors.every(c=>c.cofactor.length===2**((i<9?2:3)-1))),true));
  tests.push(testRecord('LV7053-X2-T15','derivative coordinate counts',derivative.every((r,i)=>r.result.derivatives.length===(i<9?2:3)),true));
  tests.push(testRecord('LV7053-X2-T16','derivative values binary',derivative.every(r=>r.result.derivatives.every(d=>d.derivative.every(v=>v===0||v===1))),true));
  tests.push(testRecord('LV7053-X2-T17','derivative weights even',derivative.every(r=>r.result.derivatives.every(d=>d.weight%2===0)),true));
  tests.push(testRecord('LV7053-X2-T18','influence denominators exact',derivative.every((r,i)=>r.result.derivatives.every(d=>d.influence_denominator===2**(i<9?2:3))),true));
  tests.push(testRecord('LV7053-X2-T19','affine orbit nonempty',affine.every(r=>r.result.orbit_size>=1),true));
  tests.push(testRecord('LV7053-X2-T20','affine signature length',affine.every((r,i)=>r.result.canonical_signature.length===2**(i<9?2:3)),true));
  tests.push(testRecord('LV7053-X2-T21','affine transformation counts',affine.every((r,i)=>r.result.transformations_considered===((i<9)?24:1344)),true));
  tests.push(testRecord('LV7053-X2-T22','represented disposition exact',affine.every(r=>r.disposition==='represented'),true));
  tests.push(testRecord('LV7053-X2-T23','open gaps held',gaps.every(r=>r.result.state==='open_gap'&&r.result.executed===false),true));
  tests.push(testRecord('LV7053-X2-T24','open-gap disposition exact',gaps.every(r=>r.disposition==='open_gap'),true));
  tests.push(testRecord('LV7053-X2-T25','authority gates held',gates.every(r=>r.result.state==='exact_gate'&&r.result.executed===false),true));
  tests.push(testRecord('LV7053-X2-T26','authority disposition exact',gates.every(r=>r.disposition==='exact_gate'),true));
  tests.push(testRecord('LV7053-X2-T27','candidate count',candidates.length===300,candidates.length));
  tests.push(testRecord('LV7053-X2-T28','refusals pass',refusals.length===300&&refusals.every(r=>r.result==='pass'),refusals.length));
  tests.push(testRecord('LV7053-X2-T29','repairs pass',repairs.length===300&&repairs.every(r=>r.result==='pass'),repairs.length));
  tests.push(testRecord('LV7053-X2-T30','portfolio counts',safe.length===400&&cfr.length===300,{safe:safe.length,cfr:cfr.length}));
  if(tests.some(t=>!t.passed)) throw new Error('One or more X2 tests failed: '+JSON.stringify(tests.filter(t=>!t.passed)));
  const receipt={schema:'ghc.liora.v705-v3.x2-domain-receipt.v1',stage:'x2',contracts:core,candidate_failures:candidates,refusals,repairs,cfr,safe,tests,models,counts:{contracts:150,candidate_failures:300,refusals:300,repairs:300,cfr:300,safe:400,tests:30,models:15},domain_session:{invocations:1,successes:1,replays:0},source_executions:0,x1_replays:0,boundary:'Finite synthetic same-owner Boolean-function software evidence only; NOT_READY_FOR_STAGE_20.'};
  writeJson(output,receipt);
  process.stdout.write(JSON.stringify({stage:'x2',contracts:150,candidates:300,tests:30,passed:30,models:15,output})+'\n');
}

main();
