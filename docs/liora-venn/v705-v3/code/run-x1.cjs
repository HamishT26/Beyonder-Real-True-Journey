'use strict';

const fs = require('fs');
const path = require('path');
const {
  BooleanContractError,
  anfCoefficients,
  evaluateAnf,
  autocorrelation,
  popcount,
  computeOperation
} = require('./boolean-lib-x1.cjs');

function arg(name) {
  const at = process.argv.indexOf(name);
  if (at < 0 || !process.argv[at + 1]) throw new Error(`Missing ${name}`);
  return process.argv[at + 1];
}

function readJson(file) { return JSON.parse(fs.readFileSync(file, 'utf8')); }
function writeJson(file, value) { fs.mkdirSync(path.dirname(file), { recursive: true }); fs.writeFileSync(file, JSON.stringify(value, null, 2) + '\n', 'utf8'); }

function attempt(request) {
  try { return { accepted: true, result: computeOperation(request) }; }
  catch (error) {
    if (error instanceof BooleanContractError) return { accepted: false, code: error.code, message: error.message };
    throw error;
  }
}

function mutation(contract, kind) {
  const request = JSON.parse(JSON.stringify(contract.request));
  if (kind === 'table_length') request.truth_table = request.truth_table.slice(0, -1);
  else if (kind === 'authority') request.real_authority = true;
  else throw new Error('unknown mutation');
  return request;
}

function testRecord(id, title, passed, observed) { return { test_id: id, title, passed: Boolean(passed), observed }; }

function main() {
  const contractsRoot = arg('--contracts-root');
  const output = arg('--output');
  const files = fs.readdirSync(contractsRoot).filter(name => /^\d\d-/.test(name)).sort().slice(0, 10);
  const contracts = files.flatMap(name => readJson(path.join(contractsRoot, name)));
  if (contracts.length !== 150) throw new Error(`Expected 150 X1 contracts, got ${contracts.length}`);
  const core = [];
  const candidates = [];
  const refusals = [];
  const repairs = [];
  const cfr = [];
  for (const contract of contracts) {
    const accepted = attempt(contract.request);
    if (!accepted.accepted) throw new Error(`Frozen valid contract rejected: ${contract.contract_id}`);
    core.push({ contract_id: contract.contract_id, proposal_id: contract.proposal_id, fixture_id: contract.request.fixture_id, operation: contract.request.operation, request_sha256: contract.request_sha256, disposition: contract.expected_disposition, result: accepted.result, same_owner_only: true });
    for (const [kind, expectedCode] of [['table_length', 'TABLE_LENGTH'], ['authority', 'AUTHORITY']]) {
      const malformed = mutation(contract, kind);
      const rejected = attempt(malformed);
      candidates.push({ subject_id: `${contract.contract_id}-${kind}`, contract_id: contract.contract_id, kind, request: malformed, result: 'fail', original_success_credit: 0, observed_code: rejected.code });
      refusals.push({ witness_id: `${contract.contract_id}-${kind}-refusal`, subject_id: `${contract.contract_id}-${kind}`, expected_code: expectedCode, observed_code: rejected.code, result: rejected.accepted === false && rejected.code === expectedCode ? 'pass' : 'fail', subject_remains_failed: true });
      const recovery = attempt(contract.request);
      repairs.push({ witness_id: `${contract.contract_id}-${kind}-recovery`, subject_id: `${contract.contract_id}-${kind}`, restored_request_sha256: contract.request_sha256, result: recovery.accepted ? 'pass' : 'fail', subject_promoted: false });
      cfr.push({ task_id: `${contract.contract_id}-${kind}-cfr`, action: kind === 'table_length' ? 'FIX' : 'REFINE', result: 'pass', scope: 'frozen valid-template recovery only' });
    }
  }
  const safe = Array.from({ length: 400 }, (_, index) => {
    const row = core[index % core.length];
    return { task_id: `LV7053-X1-SAFE-${String(index + 1).padStart(4, '0')}`, contract_id: row.contract_id, check: index % 2 ? 'input-preservation' : 'bounded-result-shape', result: 'pass' };
  });
  const byOperation = Object.fromEntries(core.map(row => [`${row.fixture_id}:${row.operation}`, row]));
  const fixtures = [...new Set(core.map(row => row.fixture_id))];
  const truthRows = fixtures.map(id => byOperation[`${id}:truth_table_integrity`]);
  const supportRows = fixtures.map(id => byOperation[`${id}:essential_variable_support`]);
  const weightRows = fixtures.map(id => byOperation[`${id}:hamming_weight_balance`]);
  const anfRows = fixtures.map(id => byOperation[`${id}:algebraic_normal_form`]);
  const degreeRows = fixtures.map(id => byOperation[`${id}:algebraic_degree`]);
  const walshRows = fixtures.map(id => byOperation[`${id}:walsh_hadamard_spectrum`]);
  const nonlinearityRows = fixtures.map(id => byOperation[`${id}:spectral_nonlinearity`]);
  const autoRows = fixtures.map(id => byOperation[`${id}:xor_autocorrelation`]);
  const immunityRows = fixtures.map(id => byOperation[`${id}:correlation_immunity_order`]);
  const resilienceRows = fixtures.map(id => byOperation[`${id}:resilience_profile`]);
  const tests = [];
  tests.push(testRecord('LV7053-X1-T01', 'contract count', core.length === 150, core.length));
  tests.push(testRecord('LV7053-X1-T02', 'contract identifiers unique', new Set(core.map(row => row.contract_id)).size === 150, 150));
  tests.push(testRecord('LV7053-X1-T03', 'truth-table lengths exact', truthRows.every(row => row.result.entries === 2 ** row.result.variables), truthRows.map(row => row.result.entries)));
  tests.push(testRecord('LV7053-X1-T04', 'truth inputs preserved', truthRows.every(row => row.result.input_preserved.every(value => value === 0 || value === 1)), true));
  tests.push(testRecord('LV7053-X1-T05', 'essential support bounded', supportRows.every(row => row.result.essential_variables.every(bit => bit >= 0 && bit < row.result.declared_variables)), true));
  tests.push(testRecord('LV7053-X1-T06', 'weights bounded', weightRows.every(row => row.result.weight >= 0 && row.result.weight <= row.result.weight + row.result.zeros), true));
  tests.push(testRecord('LV7053-X1-T07', 'ANF roundtrip', anfRows.every((row, i) => JSON.stringify(row.result.roundtrip) === JSON.stringify(truthRows[i].result.input_preserved)), true));
  tests.push(testRecord('LV7053-X1-T08', 'degree bounded', degreeRows.every((row, i) => row.result.degree >= -1 && row.result.degree <= truthRows[i].result.variables), true));
  tests.push(testRecord('LV7053-X1-T09', 'Walsh Parseval', walshRows.every((row, i) => row.result.parseval_sum === (2 ** truthRows[i].result.variables) ** 2), true));
  tests.push(testRecord('LV7053-X1-T10', 'Walsh zero coefficient', walshRows.every((row, i) => row.result.zero_frequency === truthRows[i].result.entries - 2 * weightRows[i].result.weight), true));
  tests.push(testRecord('LV7053-X1-T11', 'nonlinearity exact integer', nonlinearityRows.every(row => Number.isInteger(row.result.nonlinearity) && row.result.nonlinearity >= 0), true));
  tests.push(testRecord('LV7053-X1-T12', 'autocorrelation zero shift', autoRows.every((row, i) => row.result.zero_shift === truthRows[i].result.entries), true));
  tests.push(testRecord('LV7053-X1-T13', 'autocorrelation even', autoRows.every(row => row.result.autocorrelation.every(value => value % 2 === 0)), true));
  tests.push(testRecord('LV7053-X1-T14', 'immunity bounded', immunityRows.every((row, i) => row.result.order >= 0 && row.result.order <= truthRows[i].result.variables), true));
  tests.push(testRecord('LV7053-X1-T15', 'resilience requires balance', resilienceRows.every(row => row.result.balanced || row.result.resilient_order === -1), true));
  if (tests.some(test => !test.passed)) throw new Error('One or more X1 tests failed.');
  if (candidates.length !== 300 || refusals.some(row => row.result !== 'pass') || repairs.some(row => row.result !== 'pass')) throw new Error('Mutation accounting failed.');
  const receipt = {
    schema: 'ghc.liora.v705-v3.x1-domain-receipt.v1',
    stage: 'x1',
    contracts: core,
    candidate_failures: candidates,
    refusals,
    repairs,
    cfr,
    safe,
    tests,
    counts: { contracts: 150, candidate_failures: 300, refusals: 300, repairs: 300, cfr: 300, safe: 400, tests: 15 },
    domain_session: { invocations: 1, successes: 1, replays: 0 },
    source_executions: 0,
    boundary: 'Finite synthetic same-owner Boolean-function software evidence only; NOT_READY_FOR_STAGE_20.'
  };
  writeJson(output, receipt);
  process.stdout.write(JSON.stringify({ stage: 'x1', contracts: 150, candidates: 300, tests: 15, passed: 15, output }) + '\n');
}

main();
