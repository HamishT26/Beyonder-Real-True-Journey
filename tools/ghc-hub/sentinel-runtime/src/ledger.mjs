import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {LIMITS, SentinelError, requireThat, shape, integerMicros, uuid, sha256, containsCredentialMaterial} from './contract.mjs';

function checkedPath(base, relative, createParents = false) {
  requireThat(path.isAbsolute(base) && typeof relative === 'string' && !path.isAbsolute(relative), 'invalid_state_path');
  requireThat(relative.split(/[\\/]/).every(part => /^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(part) && !['.', '..'].includes(part) && !/[. ]$/.test(part) && !/^(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\.|$)/i.test(part)), 'invalid_state_path');
  const target = path.resolve(base, relative), parsed = path.parse(target);
  let current = parsed.root;
  const parts = target.slice(parsed.root.length).split(path.sep);
  for (let index = 0; index < parts.length; index++) {
    current = path.join(current, parts[index]);
    if (!fs.existsSync(current)) {
      if (createParents && index < parts.length - 1) fs.mkdirSync(current, {mode: 0o700});
      continue;
    }
    const stat = fs.lstatSync(current);
    requireThat(!stat.isSymbolicLink() && (index === parts.length - 1 ? stat.nlink <= 1 || stat.isDirectory() : stat.isDirectory()), 'redirected_or_linked_state_path');
  }
  return target;
}
export function readLocalJson(file, maxBytes = LIMITS.recordBytes) {
  const absolute = path.resolve(file), parent = path.dirname(absolute);
  checkedPath(parent, path.basename(absolute));
  const fd = fs.openSync(absolute, fs.constants.O_RDONLY | (fs.constants.O_NOFOLLOW || 0));
  try {
    const before = fs.fstatSync(fd, {bigint: true});
    requireThat(before.isFile() && before.nlink === 1n && before.size <= BigInt(maxBytes), 'invalid_state_file');
    const buffer = Buffer.alloc(maxBytes + 1); let count = 0;
    while (count < buffer.length) { const read = fs.readSync(fd, buffer, count, buffer.length - count, null); if (read === 0) break; count += read; }
    requireThat(count <= maxBytes, 'invalid_state_file');
    const bytes = buffer.subarray(0, count);
    const after = fs.fstatSync(fd, {bigint: true}), named = fs.statSync(absolute, {bigint: true});
    requireThat(before.dev === named.dev && before.ino === named.ino && before.size === after.size && before.mtimeNs === after.mtimeNs && after.nlink === 1n, 'state_changed_during_read');
    return JSON.parse(new TextDecoder('utf-8', {fatal: true}).decode(bytes));
  } finally { fs.closeSync(fd); }
}

/** Cooperating writers share this ledger. This is not an account-wide billing enforcement service. */
export class FileLedger {
  constructor(root, {maxRuns = LIMITS.ledgerRuns} = {}) {
    requireThat(typeof root === 'string' && path.isAbsolute(root), 'absolute_state_root_required');
    requireThat(Number.isInteger(maxRuns) && maxRuns >= 1 && maxRuns <= LIMITS.ledgerRuns, 'invalid_run_capacity');
    this.root = path.resolve(root); this.maxRuns = maxRuns;
  }
  create(relative, value) {
    const target = checkedPath(this.root, relative, true);
    const bytes = Buffer.from(JSON.stringify(value) + '\n');
    requireThat(bytes.length <= LIMITS.recordBytes, 'record_size_limit');
    const fd = fs.openSync(target, 'wx', 0o600);
    try { fs.writeFileSync(fd, bytes); fs.fsyncSync(fd); } finally { fs.closeSync(fd); }
    return {relative, sha256: sha256(bytes)};
  }
  read(relative) { return readLocalJson(checkedPath(this.root, relative)); }
  initialize(grant) {
    shape(grant, ['schema', 'currency', 'ceilingMicros', 'priorSpendMicros', 'priorCommittedMicros', 'availableBudgetVerified', 'scope', 'approvalReference'], 'invalid_budget_fields');
    requireThat(grant.schema === 'ghc.sentinel.budget.v1' && grant.currency === 'USD' && grant.scope === 'local-allocation', 'invalid_budget_schema');
    requireThat(grant.availableBudgetVerified === true && typeof grant.approvalReference === 'string' && /^[a-z0-9][a-z0-9-]{0,79}$/.test(grant.approvalReference), 'known_available_budget_required');
    requireThat(!containsCredentialMaterial(grant.approvalReference), 'credential_material_in_budget_reference');
    const ceiling = integerMicros(grant.ceilingMicros), spent = integerMicros(grant.priorSpendMicros), committed = integerMicros(grant.priorCommittedMicros);
    requireThat(ceiling <= 50000000n && spent + committed <= ceiling, 'invalid_budget_amount');
    return this.create('ledger/budget.json', {...grant, aggregateUsd50Enforced: false});
  }
  withLock(operation) {
    const lockPath = checkedPath(this.root, 'ledger/reservation.lock', true);
    const nonce = crypto.randomUUID(); let fd;
    try { fd = fs.openSync(lockPath, 'wx', 0o600); }
    catch (error) { if (error.code === 'EEXIST') throw new SentinelError('ledger_busy_or_stale_lock'); throw error; }
    const identity = fs.fstatSync(fd, {bigint: true});
    try { fs.writeFileSync(fd, nonce); fs.fsyncSync(fd); return operation(); }
    finally {
      fs.closeSync(fd);
      const stat = fs.lstatSync(lockPath, {bigint: true});
      if (!stat.isSymbolicLink() && stat.ino === identity.ino && stat.dev === identity.dev && stat.nlink === 1n && fs.readFileSync(lockPath, 'utf8') === nonce) {
        fs.unlinkSync(lockPath); // Only this short-lived owned lock is removed; records are never deleted.
      }
    }
  }
  snapshot() {
    const budgetPath = checkedPath(this.root, 'ledger/budget.json');
    if (!fs.existsSync(budgetPath)) return {known: false, reason: 'known_available_budget_required', aggregateUsd50Enforced: false};
    const budget = this.read('ledger/budget.json');
    requireThat(budget.schema === 'ghc.sentinel.budget.v1' && budget.availableBudgetVerified === true && budget.currency === 'USD' && budget.scope === 'local-allocation', 'invalid_budget_state');
    const ceiling = integerMicros(budget.ceilingMicros);
    requireThat(ceiling <= 50000000n, 'invalid_budget_state');
    let spent = integerMicros(budget.priorSpendMicros), held = integerMicros(budget.priorCommittedMicros), overrun = false;
    const directory = path.dirname(checkedPath(this.root, 'ledger/entries/placeholder.json'));
    const names = fs.existsSync(directory) ? fs.readdirSync(directory) : [];
    requireThat(names.length <= LIMITS.ledgerRuns * 2, 'ledger_capacity');
    requireThat(names.every(name => /^[0-9a-f-]{36}\.(reserve|settle)\.json$/.test(name)), 'unrecognized_ledger_record');
    const reserves = new Map(), settlements = new Map();
    for (const name of names.sort()) {
      const entry = this.read('ledger/entries/' + name);
      requireThat(uuid(entry.runId) && name.startsWith(entry.runId + '.'), 'invalid_ledger_record');
      (name.endsWith('.reserve.json') ? reserves : settlements).set(entry.runId, entry);
    }
    requireThat(reserves.size <= LIMITS.ledgerRuns && [...settlements.keys()].every(id => reserves.has(id)), 'invalid_ledger_history');
    for (const [id, reserve] of reserves) {
      requireThat(reserve.schema === 'ghc.sentinel.reserve.v1' && /^[a-f0-9]{64}$/.test(reserve.requestSha256), 'invalid_reservation');
      const amount = integerMicros(reserve.reservedMicros);
      const settlement = settlements.get(id);
      if (!settlement) { held += amount; continue; }
      requireThat(settlement.schema === 'ghc.sentinel.settle.v1' && settlement.requestSha256 === reserve.requestSha256 && ['reported_usage_upper_bound', 'known_not_sent'].includes(settlement.basis), 'invalid_settlement');
      const cost = integerMicros(settlement.accountedUpperMicros);
      if (settlement.basis === 'known_not_sent') requireThat(cost === 0n, 'invalid_not_sent_settlement');
      spent += cost; overrun ||= cost > amount || settlement.boundBreach === true;
    }
    overrun ||= spent + held > ceiling;
    return {known: true, scope: budget.scope, ceilingMicros: ceiling.toString(), accountedUpperMicros: spent.toString(),
      heldMicros: held.toString(), availableMicros: (ceiling > spent + held ? ceiling - spent - held : 0n).toString(),
      reservations: reserves.size, unsettled: reserves.size - settlements.size, overrun, aggregateUsd50Enforced: false};
  }
  reserve(runId, requestSha256, reservedMicros, quoteSha256) {
    requireThat(uuid(runId) && /^[a-f0-9]{64}$/.test(requestSha256) && /^[a-f0-9]{64}$/.test(quoteSha256), 'invalid_reservation');
    const amount = integerMicros(reservedMicros);
    return this.withLock(() => {
      const state = this.snapshot();
      requireThat(state.known, 'known_available_budget_required');
      requireThat(!state.overrun, 'ledger_overrun_requires_review');
      requireThat(state.reservations < LIMITS.ledgerRuns, 'ledger_capacity');
      requireThat(amount <= BigInt(state.availableMicros), 'insufficient_local_budget');
      return this.create(`ledger/entries/${runId}.reserve.json`, {schema: 'ghc.sentinel.reserve.v1', runId, requestSha256, reservedMicros, quoteSha256});
    });
  }
  settle(runId, accountedUpperMicros, basis, {boundBreach = false} = {}) {
    return this.withLock(() => {
      const reservation = this.read(`ledger/entries/${runId}.reserve.json`);
      integerMicros(accountedUpperMicros);
      requireThat(['reported_usage_upper_bound', 'known_not_sent'].includes(basis), 'invalid_settlement_basis');
      return this.create(`ledger/entries/${runId}.settle.json`, {schema: 'ghc.sentinel.settle.v1', runId,
        requestSha256: reservation.requestSha256, accountedUpperMicros, basis, boundBreach: boundBreach === true});
    });
  }
  beginRun(runId, intent) {
    requireThat(uuid(runId), 'invalid_run_id');
    return this.withLock(() => {
      const directory = path.dirname(checkedPath(this.root, 'runs/placeholder.json'));
      if (fs.existsSync(directory)) {
        const iterator = fs.opendirSync(directory); let count = 0;
        try {
          for (let entry; (entry = iterator.readSync()) !== null;) {
            requireThat(entry.isDirectory() && !entry.isSymbolicLink() && uuid(entry.name), 'invalid_run_directory');
            requireThat(++count < this.maxRuns, 'run_receipt_capacity');
          }
        } finally { iterator.closeSync(); }
      }
      const target = checkedPath(this.root, `runs/${runId}/intent.json`, true);
      return this.create(path.relative(this.root, target), intent);
    });
  }
  markDispatch(runId) { return this.create(`runs/${runId}/dispatch.json`, {schema: 'ghc.sentinel.dispatch-intent.v1', runId, meaning: 'Request may have been sent; not a delivery or billing acknowledgement'}); }
  receipt(runId, record) { return this.create(`runs/${runId}/receipt.json`, record); }
}
