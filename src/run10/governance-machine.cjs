'use strict';
// Pure bounded model: no I/O, clocks, credentials, service calls or execution grants.
const { createHash } = require('node:crypto');
const API_VERSION = 'orenna.governance-model.v1';
const ID = /^[A-Za-z0-9_-]{1,64}$/;
const HASH = /^[a-f0-9]{64}$/;
const isId = x => typeof x === 'string' && ID.test(x);
const isHash = x => typeof x === 'string' && HASH.test(x);
const integer = x => Number.isSafeInteger(x) && x >= 0;
const object = x => x !== null && typeof x === 'object' && !Array.isArray(x);
const digest = (domain, text) => createHash('sha256').update(domain + '\0' + text, 'utf8').digest('hex');

function cloneFrozen(value, depth = 0, budget = { nodes: 0 }) {
  if (++budget.nodes > 8192 || depth > 16) throw new TypeError('CONTEXT_BOUND');
  if (value === null || typeof value === 'boolean') return value;
  if (typeof value === 'string') {
    if (value.length > 32768) throw new TypeError('CONTEXT_STRING_BOUND');
    return value;
  }
  if (typeof value === 'number' && Number.isFinite(value)) return value;
  if (Array.isArray(value)) {
    if (value.length > 128) throw new TypeError('CONTEXT_ARRAY_BOUND');
    return Object.freeze(value.map(x => cloneFrozen(x, depth + 1, budget)));
  }
  if (object(value) && (Object.getPrototypeOf(value) === Object.prototype || Object.getPrototypeOf(value) === null)) {
    const names = Object.keys(value);
    if (names.length > 64) throw new TypeError('CONTEXT_FIELD_BOUND');
    const copy = Object.create(null);
    for (const name of names) {
      const descriptor = Object.getOwnPropertyDescriptor(value, name);
      if (!descriptor || !Object.hasOwn(descriptor, 'value')) throw new TypeError('CONTEXT_ACCESSOR');
      copy[name] = cloneFrozen(descriptor.value, depth + 1, budget);
    }
    return Object.freeze(copy);
  }
  throw new TypeError('CONTEXT_NOT_PLAIN_DATA');
}

function createTrustedBoundary() {
  const contexts = new WeakMap();

  // TRUSTED-HOST-ONLY BOOTSTRAP. Never expose this method as an agent JSON endpoint.
  // It does not authenticate humans: the caller must supply independently verified facts.
  function bindTrustedContext(hostVerifiedSnapshot) {
    const copy = cloneFrozen(hostVerifiedSnapshot);
    const handle = Object.freeze(Object.create(null));
    contexts.set(handle, copy);
    return handle;
  }

  // Deterministic over one immutable caller snapshot and a bounded parsed-JSON event trace.
  // There is no caller-supplied prior machine state and no effect/permission API.
  function evaluate(contextHandle, events) {
    let state = 'COLLECTING', approvals = 0, humanApproved = false, started = false;
    const output = (code = 'NONE', selectedState = state) => Object.freeze({
      state: selectedState, code, approvals, requiredApprovals: 6,
      humanApproved, started, retryAllowed: false, executionAuthorized: false, synthetic: true
    });
    const hold = code => output(code, 'HELD');
    if (!contexts.has(contextHandle)) return hold('UNTRUSTED_CONTEXT');
    const c = contexts.get(contextHandle);
    if (!object(c) || typeof c.actionBytes !== 'string' || typeof c.rosterBytes !== 'string' ||
        Buffer.byteLength(c.actionBytes, 'utf8') > 32768 || Buffer.byteLength(c.rosterBytes, 'utf8') > 32768 ||
        !isHash(c.expectedActionDigest) || !isHash(c.expectedRosterDigest) ||
        !integer(c.rosterEpoch) || !integer(c.revocationEpoch) ||
        typeof c.actionRevoked !== 'boolean') return hold('CONTEXT_SHAPE');
    if (digest('ghc.freed-id.action-design.v1', c.actionBytes) !== c.expectedActionDigest) return hold('ACTION_DIGEST');
    if (digest('ghc.freed-id.roster.v1', c.rosterBytes) !== c.expectedRosterDigest) return hold('ROSTER_DIGEST');
    let action, roster;
    try { action = JSON.parse(c.actionBytes); roster = JSON.parse(c.rosterBytes); }
    catch { return hold('CONTEXT_ENCODING'); }
    // Array encodings deliberately avoid ambiguous duplicate JSON object keys.
    if (!Array.isArray(action) || action.length !== 6 ||
        !isId(action[0]) || !isId(action[1]) || !isId(action[2]) ||
        !integer(action[3]) || !integer(action[4]) || !integer(action[5]) || action[4] >= action[5]) return hold('ACTION_SHAPE');
    if (action[2] !== 'pilot-six') return hold('TIER_DISABLED');
    if (!Array.isArray(roster) || roster.length !== 6) return hold('ROSTER_SIZE');
    const members = new Map(), keys = new Set();
    for (const pair of roster) {
      if (!Array.isArray(pair) || pair.length !== 2 || !pair.every(isId)) return hold('ROSTER_SHAPE');
      if (members.has(pair[0])) return hold('ROSTER_DUPLICATE_ID');
      if (keys.has(pair[1])) return hold('ROSTER_DUPLICATE_KEY');
      members.set(pair[0], pair[1]); keys.add(pair[1]);
    }
    if (c.clockVerified !== true || !integer(c.nowMs)) return hold('CLOCK_UNVERIFIED');
    if (c.nowMs < action[4]) return hold('ACTION_NOT_YET_VALID');
    if (c.nowMs >= action[5]) return hold('ACTION_EXPIRED');
    if (c.actionRevoked || c.revocationEpoch !== action[3]) return hold('ACTION_REVOKED');
    for (const list of [c.revokedKeys, c.revokedHumanProofs]) {
      if (!Array.isArray(list) || list.length > 64 || !list.every(isId) || new Set(list).size !== list.length) return hold('CONTEXT_REVOCATION');
    }
    const mapProofs = list => {
      if (!Array.isArray(list) || list.length > 64) return null;
      const map = new Map();
      for (const p of list) {
        if (!object(p) || !isId(p.id) || map.has(p.id)) return null;
        map.set(p.id, p);
      }
      return map;
    };
    const votes = mapProofs(c.voteProofs), humans = mapProofs(c.humanProofs), receipts = mapProofs(c.receiptProofs);
    if (!votes || !humans || !receipts) return hold('CONTEXT_PROOFS');
    if (!Array.isArray(events) || events.length > 32) return hold('EVENTS_SHAPE');
    const binding = p => p.actionDigest === c.expectedActionDigest && p.rosterDigest === c.expectedRosterDigest &&
      p.rosterEpoch === c.rosterEpoch && p.revocationEpoch === c.revocationEpoch;
    const timeShape = p => integer(p.issuedAt) && integer(p.expiresAt) &&
      p.issuedAt >= action[4] && p.issuedAt <= c.nowMs && p.issuedAt < p.expiresAt && p.expiresAt <= action[5];
    const reviewersSeen = new Set(), proofsSeen = new Set();

    for (const event of events) {
      if (!object(event) || typeof event.type !== 'string') return hold('EVENT_SHAPE');
      const takesProof = ['vote', 'human', 'result', 'reconcile'].includes(event.type);
      if (!takesProof && !['start', 'retry'].includes(event.type)) return hold('EVENT_TYPE');
      const expectedNames = takesProof ? ['type', 'actionDigest', 'rosterDigest', 'proofRef'] : ['type', 'actionDigest', 'rosterDigest'];
      if (Object.keys(event).length !== expectedNames.length || expectedNames.some(k => !Object.hasOwn(event, k)) ||
          (takesProof && !isId(event.proofRef))) return hold('EVENT_SHAPE');
      if (event.actionDigest !== c.expectedActionDigest || event.rosterDigest !== c.expectedRosterDigest) return hold('EVENT_BINDING');
      if (state === 'OUTCOME_UNKNOWN' && event.type !== 'reconcile') return output('UNKNOWN_RESULT_NO_RETRY', 'OUTCOME_UNKNOWN');

      if (event.type === 'vote') {
        if (!['COLLECTING', 'PENDING_HUMAN'].includes(state)) return hold('STATE_ORDER');
        const p = votes.get(event.proofRef);
        if (!p || p.verified !== true || p.originKind !== 'reviewer-session') return hold('VOTE_PROOF_REQUIRED');
        if (!binding(p)) return hold('VOTE_BINDING');
        if (!members.has(p.reviewerId)) return hold('VOTE_IDENTITY');
        if (members.get(p.reviewerId) !== p.keyId) return hold('VOTE_KEY');
        if (c.revokedKeys.includes(p.keyId)) return hold('KEY_REVOKED');
        if (!timeShape(p)) return hold('VOTE_TIME');
        if (c.nowMs >= p.expiresAt) return hold('VOTE_EXPIRED');
        if (proofsSeen.has(p.id)) return hold('DUPLICATE_PROOF');
        if (reviewersSeen.has(p.reviewerId)) return hold('DUPLICATE_REVIEWER');
        if (!['approve', 'reject', 'abstain'].includes(p.decision)) return hold('VOTE_DECISION');
        proofsSeen.add(p.id); reviewersSeen.add(p.reviewerId);
        if (p.decision === 'reject') return hold('DISSENT_UNRESOLVED');
        if (p.decision === 'approve') approvals++;
        state = approvals === 6 ? 'PENDING_HUMAN' : 'COLLECTING';
      } else if (event.type === 'human') {
        if (state !== 'PENDING_HUMAN' || approvals !== 6) return hold('REVIEW_NOT_COMPLETE');
        const p = humans.get(event.proofRef);
        if (!p) return hold('HUMAN_PROOF_REQUIRED');
        if (p.humanOriginVerified !== true || p.sourceKind !== 'direct-human' || !isId(p.humanActorId)) return hold('HUMAN_PROVENANCE');
        if (!binding(p) || p.operationId !== action[0] || p.scope !== action[1] || p.tier !== action[2]) return hold('HUMAN_BINDING');
        if (c.revokedHumanProofs.includes(p.id)) return hold('HUMAN_REVOKED');
        if (!timeShape(p)) return hold('HUMAN_TIME');
        if (c.nowMs >= p.expiresAt) return hold('HUMAN_EXPIRED');
        humanApproved = true; state = 'HUMAN_APPROVED';
      } else if (event.type === 'start') {
        if (started) return hold('DUPLICATE_START');
        if (approvals !== 6) return hold('THRESHOLD_UNMET');
        if (!humanApproved || state !== 'HUMAN_APPROVED') return hold('HUMAN_APPROVAL_REQUIRED');
        started = true; state = 'STARTED';
      } else if (event.type === 'retry') {
        return hold('RETRY_FORBIDDEN');
      } else {
        if (!started) return hold('RESULT_BEFORE_START');
        if (event.type === 'reconcile' && state !== 'OUTCOME_UNKNOWN') return hold('STATE_ORDER');
        if (event.type === 'result' && !['STARTED', 'ACCEPTED'].includes(state)) return hold('STATE_ORDER');
        const p = receipts.get(event.proofRef);
        if (!p || p.verified !== true) return output('RECEIPT_PROOF_REQUIRED', 'OUTCOME_UNKNOWN');
        if (!binding(p) || p.operationId !== action[0]) return output('RECEIPT_BINDING', 'OUTCOME_UNKNOWN');
        if (!['accepted', 'complete', 'unknown', 'rejected'].includes(p.state)) return output('RECEIPT_STATE', 'OUTCOME_UNKNOWN');
        if (event.type === 'reconcile' && !['complete', 'rejected'].includes(p.state)) return output('RECONCILIATION_NOT_FINAL', 'OUTCOME_UNKNOWN');
        if (p.state === 'rejected') return hold('RESULT_REJECTED');
        state = p.state === 'complete' ? 'COMPLETED' : p.state === 'accepted' ? 'ACCEPTED' : 'OUTCOME_UNKNOWN';
      }
    }
    return output();
  }
  return Object.freeze({ bindTrustedContext, evaluate });
}
module.exports = Object.freeze({ API_VERSION, createTrustedBoundary });
