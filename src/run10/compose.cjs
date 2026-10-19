'use strict';
// Source-only composition candidate. No real human authority or execution grant is produced.
const { createHash } = require('node:crypto');
const hash = (domain, bytes) => createHash('sha256').update(domain + '\0' + bytes, 'utf8').digest('hex');
const copy = value => JSON.parse(JSON.stringify(value));

function compose(identity, governance, fixture, materialized) {
  const counts = { identityAssess: 0, identityVerify: 0, governanceEvaluate: 0 };
  const evidence = [];
  const envelope = (review, bridgeState, governanceResult) => ({
    review, bridgeState, governance: governanceResult,
    executionAuthorized: false, permissionsGranted: false, actualHumanApproval: false
  });
  if (identity.contractVersion !== 2 || governance.API_VERSION !== 'orenna.governance-model.v1') throw Error('MODEL_API');
  if (!fixture || !Array.isArray(fixture.identity.registry) || fixture.identity.registry.length !== 6 ||
      !Array.isArray(fixture.identity.messages) || fixture.identity.messages.length > 6 ||
      materialized.proofs.length !== fixture.identity.messages.length) throw Error('COMPOSITION_FIXTURE_SHAPE');

  const gate = identity.createReviewGate(materialized.registry, fixture.identity.policy, fixture.identity.context);
  counts.identityAssess++;
  const review = gate.assess(materialized.proofs, fixture.identity.now);
  if (!review.ok) return { result: envelope(review, 'HELD_IDENTITY', null), counts, projectedEvidence: evidence, materializedGovernanceContext: null };
  if (review.state !== 'eligible_for_human_review' || review.executionAuthorized !== false ||
      review.permissionsGranted !== false || review.independentOrganizationsEstablished !== false) throw Error('IDENTITY_REVIEW_CLAIM_CHANGED');

  const snapshot = copy(fixture.governance.callerSnapshot);
  const actionDigest = hash('ghc.freed-id.action-design.v1', snapshot.actionBytes);
  const rosterDigest = hash('ghc.freed-id.roster.v1', snapshot.rosterBytes);
  const joinedDigest = hash('ghc.x2.identity-governance-join.v1', actionDigest + '\0' + rosterDigest);
  const action = JSON.parse(snapshot.actionBytes), roster = JSON.parse(snapshot.rosterBytes);
  // This narrow profile explicitly couples the two frozen epochs and time windows.
  if (actionDigest !== snapshot.expectedActionDigest || rosterDigest !== snapshot.expectedRosterDigest ||
      fixture.identity.context.action !== joinedDigest ||
      fixture.identity.context.epoch !== snapshot.rosterEpoch ||
      fixture.identity.context.epoch !== snapshot.revocationEpoch ||
      fixture.identity.context.notBefore !== action[4] ||
      fixture.identity.context.expiresAt !== action[5] ||
      fixture.identity.now !== snapshot.nowMs) {
    return { result: envelope(review, 'HELD_BINDING', null), counts, projectedEvidence: evidence, materializedGovernanceContext: null };
  }
  if (!Array.isArray(roster) || roster.length !== 6 || !Array.isArray(snapshot.voteProofs) || snapshot.voteProofs.length !== 0) throw Error('PROJECTION_NOT_EMPTY');
  const mapping = new Map();
  const keySlots = new Set(), logicalKeys = new Set();
  for (const r of fixture.identity.registry) {
    if (mapping.has(r.actor) || keySlots.has(r.keySlot) || logicalKeys.has(r.logicalKeyId)) throw Error('PROJECTION_DUPLICATE_MAPPING');
    if (!roster.some(pair => pair[0] === r.actor && pair[1] === r.logicalKeyId)) throw Error('PROJECTION_ROSTER_MISMATCH');
    mapping.set(r.actor, r); keySlots.add(r.keySlot); logicalKeys.add(r.logicalKeyId);
  }
  for (let i = 0; i < materialized.proofs.length; i++) {
    counts.identityVerify++;
    const verified = gate.verify(materialized.proofs[i], fixture.identity.now);
    if (!verified.ok || verified.decision !== 'approve' || !mapping.has(verified.actor)) throw Error('VERIFIED_PROJECTION_INCONSISTENT');
    const enrolled = mapping.get(verified.actor);
    if (fixture.identity.messages[i].actor !== verified.actor) throw Error('PROJECTION_ACTOR_MISMATCH');
    evidence.push({ actor: verified.actor, keyFingerprint: verified.keyFingerprint, role: verified.role, decision: verified.decision });
    // Only verified REVIEWER evidence is projected. No identity result creates a human proof.
    snapshot.voteProofs.push({
      id: 'bridge-v' + (i + 1), reviewerId: verified.actor, keyId: enrolled.logicalKeyId,
      decision: verified.decision, verified: true, originKind: 'reviewer-session',
      issuedAt: fixture.governance.voteIssuedAt, expiresAt: fixture.identity.messages[i].expires,
      actionDigest, rosterDigest, rosterEpoch: snapshot.rosterEpoch, revocationEpoch: snapshot.revocationEpoch
    });
  }
  // The harness simulates a separately trusted caller. These fixtures authenticate no actual human.
  const boundary = governance.createTrustedBoundary();
  const handle = boundary.bindTrustedContext(snapshot);
  counts.governanceEvaluate++;
  const result = boundary.evaluate(handle, fixture.governance.events);
  return { result: envelope(review, 'GOVERNANCE_EVALUATED', result), counts,
    projectedEvidence: evidence, materializedGovernanceContext: snapshot };
}
module.exports = Object.freeze({ compose, contractVersion: 1 });
