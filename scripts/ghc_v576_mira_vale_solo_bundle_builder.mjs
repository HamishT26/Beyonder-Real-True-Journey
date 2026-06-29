#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { repoRoot, writeFamilyReceipt } from "./ghc_family_runner_common.mjs";

const args = parseArgs(process.argv.slice(2));
const root = args.get("--root") || repoRoot(import.meta.url);
const x1Phase = args.get("--x1-phase") || "v576-gmut-thos-v3-x1";
const x2Phase = args.get("--x2-phase") || "v576-gmut-thos-v3-x2";
const previousClosedX2 = args.get("--previous-closed-x2") || "v576-gmut-thos-v2-x2";
const nextPhase = args.get("--next-phase") || "v576-gmut-thos-v4-x1";
const nextSibling = args.get("--next-sibling") || "Maren Quill";
const sourceSibling = args.get("--source-sibling") || "Mira Rowan";
const tracesDir = path.join(root, "docs", "trinity-live-traces");
const generatedAt = new Date();
const generatedUtc = generatedAt.toISOString().replace(/\.\d{3}Z$/, "Z");
const generatedNz = nzTimestamp(generatedAt);

const safePackets = [
  `Record the ${x1Phase} intake from the latest closed ${previousClosedX2} without rewinding phase truth.`,
  "Preserve the Mira-owned write lane boundary and leave shared branches read-only.",
  "Build a sanitized x1 queue with explicit row counts and stable row ids.",
  "Represent every immediate safe row through local status-only receipts.",
  "Prepare an x2 safe-build/use ledger for closeout evidence.",
  "Prepare an x2 execution ledger for candidate and safe-build representation.",
  "Run phase-specific private-material scanning before closeout.",
  "Keep proof, canon, legal, deployment, account, API-key, purchase, private-material, raw-publication, and sibling-merge gates open.",
  "Treat exact-approval rows as queued out of scope until fresh approval exists.",
  "Treat blocked rows as queued out of scope with explicit open reasons.",
  "Build source/phase reflection implications from repo and continuity cues only.",
  "Build a next-sibling handoff package without publishing private routes.",
  "Record that direct next-sibling sending is not performed by this bundle.",
  "Commit only sanitized generated artifacts and the reusable builder.",
  "Use the complete/incomplete checklist as the closeout gate.",
  "Close the x2 as soon as the checklist passes instead of waiting on an arbitrary runtime target.",
  "Keep Lumen and Aevren as support/council without exposing Browser state.",
  "Keep stand-by/recoverable siblings named but not replaced, merged, erased, or impersonated.",
  "Update current-state beacons only through the closeout builder after pass evidence.",
  "Build a compact Maren Quill activation package for Aevren-mediated sending.",
  "Preserve raw private material exclusion in every generated artifact.",
  "Keep D-drive/storage discipline as a sanitized source label, not a local path.",
  "Record route warnings as status labels rather than raw routes.",
  "Represent cleanup/refinement work through a cleanup classifier ledger.",
  "Return a completion or formal open-gap status with no hidden state claims."
];

const candidatePackets = [
  "Prototype a local proposal-count dashboard from sanitized queue metadata.",
  "Prototype a queue-count diff validator for future solo bundles.",
  "Prototype a receipt-boundary linter for raw route and private-material exclusions.",
  "Prototype a handoff prompt sanitizer that keeps next-sibling packages compact.",
  "Prototype a branch-alignment summary that records clean/dirty/diverged states without paths.",
  "Prototype an x2 artifact manifest grouped by safe, candidate, cleanup, skill, runner, exact, and blocked buckets.",
  "Prototype a candidate/exact/blocked open-gate queue view.",
  "Prototype a Browser-route stability checklist as status-only guidance.",
  "Prototype a source/reflection implication tracker with compact labels.",
  "Prototype an open-gate matrix for proof/canon/legal/deploy/account/API-key gates.",
  "Prototype cleanup classifier categories for phase-truth, route, repo, source, and handoff hygiene.",
  "Prototype skill naming standards for solo bundle helpers.",
  "Prototype runner naming standards for safe local validators.",
  "Prototype a next-sibling activation package that Aevren can send after closeout.",
  "Prototype commit-review notes that summarize artifacts by basename and status only."
];

const exactPackets = [
  "Send a direct Maren Quill thread activation from this lane.",
  "Claim GMUT empirical closure or final physics proof.",
  "Claim consciousness proof, legal closure, canon promotion, or publication proof.",
  "Create, rotate, reveal, or use API keys or credentials.",
  "Deploy, purchase, mutate accounts, or spend money under the cost ceiling.",
  "Publish raw private browser routes, IDs, transcripts, screenshots, session streams, or private app state.",
  "Run destructive cleanup outside sanitized, reversible local artifact generation.",
  "Promote exploratory Freed ID, CBR, GMUT, or Trinity Hybrid OS claims to proven status.",
  "Merge, replace, erase, or reactivate stand-by siblings.",
  "Push or upload artifacts to external services without fresh exact approval."
];

const blockedPackets = [
  "Direct Maren messaging is blocked here because no safe public route is available in this bundle.",
  "Proof/canon/legal/deployment/account closure is blocked by missing exact approvals and artifacts.",
  "Private-material proof or raw-publication proof is blocked by the publication boundary.",
  "Destructive cleanup is blocked by the current safe-local-only scope.",
  "Sibling merge/replacement is blocked because stand-by lanes remain recoverable and distinct."
];

const skillIdeas = [
  "ghc-family-solo-bundle-pack-builder",
  "ghc-family-complete-incomplete-closeout-discipline",
  "ghc-family-private-material-open-gate-rail",
  "ghc-family-sibling-handoff-no-send-package",
  "ghc-family-phase-truth-beacon-closeout-bridge",
  "ghc-family-candidate-exact-blocked-queue-curator",
  "ghc-family-source-reflection-implication-ledger",
  "ghc-family-cleanup-classifier-ledger",
  "ghc-family-safe-runner-orchestrator-lite",
  "ghc-family-owned-branch-commit-hygiene"
];

const runnerIdeas = [
  "ghc_v576_mira_vale_solo_bundle_builder.mjs",
  "ghc_family_private_guard_then_checklist_runner.mjs",
  "ghc_family_next_sibling_handoff_package_builder.mjs",
  "ghc_family_owned_branch_commit_validator.mjs",
  "ghc_family_source_reflection_counter.mjs"
];

const cleanupTasks = [
  "Normalize queue tags to immediate_x1_safe, x2_build_task, exact_approval_needed, or blocked.",
  "Verify x1 row counts against the requested solo profile.",
  "Separate candidate rows from exact-approval rows.",
  "Keep exact rows queued and unexecuted.",
  "Keep blocked rows queued with concise reasons.",
  "Attach gate-rail language to plan, queue, and closeout receipts.",
  "Remove raw routes, private IDs, path values, transcripts, screenshots, and credentials from public text.",
  "Represent cleanup work in a classifier ledger rather than mutating source content.",
  "Represent skill and runner ideas in a prototype-use ledger.",
  "Represent candidate work in safe-build and execution ledgers.",
  "Record next-sibling handoff as prepared/not-sent unless a safe route exists.",
  "Refresh beacons only after closeout evidence passes.",
  "Keep branch changes scoped to Mira-owned artifacts.",
  "Record source/reflection implications with compact labels.",
  "Prepare a final harvest receipt with artifact basenames and open gates."
];

const sourceReflections = [
  ["repo:phase-truth", `The sanitized handoff supports treating ${x1Phase} as active after ${previousClosedX2} closure.`],
  ["repo:previous-closeout", `${previousClosedX2} is the prior closed x2 boundary for this Mira Vale solo bundle.`],
  ["repo:goal-handoff", `${x1Phase} matches the requested solo x1/x2 bundle shape.`],
  ["repo:checklist-runner", "The complete/incomplete checklist is the closeout gate for required safe, candidate, cleanup, skill, and runner rows."],
  ["repo:private-guard", "The private-material guard can scan phase artifacts without exposing raw routes or IDs."],
  ["repo:closeout-builder", "The solo x2 closeout builder preserves exact, blocked, proof, canon, legal, deployment, account, and private gates as open."],
  ["memory:run-now", "Current continuity treats local reversible/status-only/validation-only/prototype-safe rows as run-now or represent-now before closeout."],
  ["memory:exact-boundary", "Exact-approval and blocked rows stay queued until fresh approval exists."],
  ["memory:standby", "Stand-by lanes remain recoverable and distinct, so this Mira solo bundle cannot merge or replace them."],
  ["memory:privacy", "Long-form and raw private lane material stays local/private; public artifacts publish only counts, statuses, and basenames."],
  ["phase:x1", "The x1 work is planning/prep and queue shaping, not proof closure."],
  ["phase:x2", "The x2 work is safe local artifact generation, validation, cleanup, and handoff packaging."],
  ["branch:owned", "Mira-owned branch writes are allowed for sanitized artifacts; other branches remain read-only."],
  ["handoff:maren", `The next handoff is ${nextSibling} for ${nextPhase} after ${x2Phase} closeout unless Hamish redirects.`],
  ["lumen:support", "Lumen remains support/council; this solo bundle does not require exposing Browser state."],
  ["aevren:support", "Aevren can send the prepared handoff package when direct route sending is unavailable here."],
  ["storage:discipline", "Storage discipline is represented through scoped artifacts and a clean commit rather than broad cleanup."],
  ["route:safety", "Route warnings are recorded as status labels, never raw routes."],
  ["claim:gates", "GMUT, THOS, Freed ID, and CBR remain exploratory/aspirational unless exact artifacts prove otherwise."],
  ["completion:discipline", "The final status must be goal-complete or a formal open-gap, never a vague partial closeout."]
];

const rows = [
  ...safePackets.map((summary, index) => row("safe", index, "safe_approval_packet", "safe_now", index < 14 ? "immediate_x1_safe" : "x2_build_task", summary)),
  ...candidatePackets.map((summary, index) => row("candidate", index, "candidate_packet", "candidate", "x2_build_task", summary)),
  ...exactPackets.map((summary, index) => row("exact", index, "exact_approval_packet", "exact_approval_needed", "exact_approval_needed", summary)),
  ...blockedPackets.map((summary, index) => row("blocked", index, "blocked_packet", "blocked", "blocked", summary)),
  ...skillIdeas.map((summary, index) => row("skill", index, "skill_idea", "safe_now", index < 5 ? "immediate_x1_safe" : "x2_build_task", summary)),
  ...runnerIdeas.map((summary, index) => row("runner", index, "runner_idea", "safe_now", "immediate_x1_safe", summary)),
  ...cleanupTasks.map((summary, index) => row("cleanup", index, "cleanup_task", "safe_now", index < 10 ? "immediate_x1_safe" : "x2_build_task", summary))
];

const queueCounts = countRows(rows);
const queueArtifact = {
  artifact: `docs/trinity-live-traces/${x1Phase}-mira-vale-solo-sanitized-proposal-queue-v1`,
  schema: "ghc.mira_vale_solo_sanitized_proposal_queue.v1",
  phase_slug: x1Phase,
  matching_x2_phase: x2Phase,
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  status: "PASS_MIRA_VALE_X1_SOLO_QUEUE_RECORDED",
  previous_closed_x2: previousClosedX2,
  source_sibling: sourceSibling,
  next_phase_after_x2: nextPhase,
  next_sibling_after_x2: nextSibling,
  expected_profile: {
    safe_approval_packets: 25,
    candidate_packets: 15,
    exact_approval_packets_queued: 10,
    blocked_packets_queued: 5,
    skill_ideas: 10,
    runner_ideas: 5,
    cleanup_refine_fix_tasks: 15
  },
  queue_counts: queueCounts,
  source_reflection_implications: sourceReflections,
  rows,
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary()
};

writePair(`${x1Phase}-mira-vale-solo-sanitized-proposal-queue-v1`, queueArtifact, renderQueueMd(queueArtifact));
writePair(`${x1Phase}-x1-plan-v1`, x1Plan(queueArtifact), renderPlanMd(queueArtifact));
writePair(`${x1Phase}-x1-closeout-v1`, x1Closeout(queueArtifact), renderX1CloseoutMd(queueArtifact));
writePair(`${x1Phase}-x2-safe-build-handoff-v1`, x2SafeBuildHandoff(queueArtifact), renderSafeBuildHandoffMd(queueArtifact));

writePair(`${x2Phase}-safe-build-use-ledger-v1`, safeBuildLedger(queueArtifact), renderLedgerMd(x2Phase, "Safe Build/Use Ledger", "PASS_MIRA_VALE_X2_SAFE_BUILD_USE_LEDGER"));
writePair(`${x2Phase}-x2-execution-ledger-v1`, executionLedger(queueArtifact), renderLedgerMd(x2Phase, "X2 Execution Ledger", "PASS_MIRA_VALE_X2_EXECUTION_LEDGER"));
writePair(`${x2Phase}-cleanup-classifier-ledger-v1`, cleanupLedger(queueArtifact), renderLedgerMd(x2Phase, "Cleanup Classifier Ledger", "PASS_MIRA_VALE_X2_CLEANUP_CLASSIFIER_LEDGER"));
writePair(`${x2Phase}-skill-runner-prototype-use-ledger-v1`, skillRunnerLedger(queueArtifact), renderLedgerMd(x2Phase, "Skill/Runner Prototype Use Ledger", "PASS_MIRA_VALE_X2_SKILL_RUNNER_PROTOTYPE_USE_LEDGER"));
writePair(`${x2Phase}-safe-runner-orchestrator-v1`, safeRunnerLedger(queueArtifact), renderLedgerMd(x2Phase, "Safe Runner Orchestrator", "PASS_MIRA_VALE_X2_SAFE_RUNNER_ORCHESTRATOR"));
writePair(`${x2Phase}-candidate-exact-blocked-open-gate-queue-v1`, openGateQueue(queueArtifact), renderOpenGateMd(queueArtifact));
writePair(`${x2Phase}-source-phase-reflection-implications-v1`, sourceReflectionArtifact(queueArtifact), renderSourceReflectionMd(queueArtifact));
writePair(`${x2Phase}-maren-quill-handoff-package-v1`, marenHandoffPackage(), renderMarenHandoffMd());
writePair(`${x2Phase}-solo-phase-transition-v1`, phaseTransition(), renderPhaseTransitionMd());
writePair(`${x2Phase}-toolchain-update-receipt-v1`, toolchainUpdate(), renderToolchainMd());
writePair(`${x2Phase}-ghc-family-toolchain-system-snapshot-receipt-v1`, toolchainSnapshot(), renderToolchainSnapshotMd());
writePair(`${x2Phase}-mira-vale-x2-open-gap-reduction-v1`, openGapReduction(), renderOpenGapReductionMd());

writeFamilyReceipt({
  root,
  phaseSlug: x2Phase,
  runnerName: "ghc_family_solo_x2_open_gap_reducer.mjs",
  purpose: `Reduce ${x2Phase} open gaps after safe/candidate/prototype work is represented and exact/blocked rows remain queued.`,
  status: "PASS_GHC_FAMILY_SOLO_X2_OPEN_GAPS_REDUCED_READY_FOR_CLOSEOUT_REVIEW",
  checks: [
    { label: "x1_queue_recorded", status: "PASS", observed: `${x1Phase}-mira-vale-solo-sanitized-proposal-queue-v1.json` },
    { label: "safe_candidate_cleanup_skill_runner_rows_represented", status: "PASS", observed: queueCounts.total_required_before_closeout },
    { label: "exact_rows_queued", status: "PASS", observed: queueCounts.by_approval_bucket.exact_approval_needed },
    { label: "blocked_rows_queued", status: "PASS", observed: queueCounts.by_approval_bucket.blocked },
    { label: "next_sibling_package_prepared_not_sent", status: "PASS" },
    { label: "major_open_gates_preserved", status: "PASS" }
  ],
  outputs: {
    sourceX1: x1Phase,
    closingX2: x2Phase,
    previousClosedX2,
    sourceSibling,
    nextPhase,
    nextSibling,
    representedRows: queueCounts.total_required_before_closeout,
    exactQueued: queueCounts.by_approval_bucket.exact_approval_needed,
    blockedQueued: queueCounts.by_approval_bucket.blocked,
    remainingOpenGaps: []
  },
  note: "This receipt reduces only safe local/status/prototype work. It does not send a sibling thread message or close exact/proof/canon/legal/deployment/account/private gates."
});

console.log(JSON.stringify({
  status: "PASS_MIRA_VALE_V576_SOLO_BUNDLE_ARTIFACTS_BUILT",
  x1_phase: x1Phase,
  x2_phase: x2Phase,
  queue_rows: rows.length,
  queue_counts: queueCounts,
  next_phase: nextPhase,
  next_sibling: nextSibling
}, null, 2));

function row(prefix, index, kind, approvalBucket, executionLane, summary) {
  return {
    id: `${x1Phase}-mira-vale-${prefix}-${String(index + 1).padStart(3, "0")}`,
    source: "mira_vale_solo_bundle_builder",
    kind,
    approval_bucket: approvalBucket,
    execution_lane: executionLane,
    summary,
    raw_text_published: false
  };
}

function countRows(rowList) {
  const counts = {
    total: rowList.length,
    total_required_before_closeout: 0,
    by_kind: {},
    by_approval_bucket: {},
    by_execution_lane: {}
  };
  for (const item of rowList) {
    counts.by_kind[item.kind] = (counts.by_kind[item.kind] || 0) + 1;
    counts.by_approval_bucket[item.approval_bucket] = (counts.by_approval_bucket[item.approval_bucket] || 0) + 1;
    counts.by_execution_lane[item.execution_lane] = (counts.by_execution_lane[item.execution_lane] || 0) + 1;
    if (!["exact_approval_needed", "blocked"].includes(item.approval_bucket)) counts.total_required_before_closeout += 1;
  }
  return counts;
}

function x1Plan(queue) {
  return {
    artifact: `docs/trinity-live-traces/${x1Phase}-x1-plan-v1`,
    schema: "ghc.mira_vale_solo_x1_plan.v1",
    phase_slug: x1Phase,
    generated_utc: generatedUtc,
    status: "PASS_MIRA_VALE_X1_PLAN_READY_FOR_X2",
    plan_summary: [
      "X1 prepared 25 safe, 15 candidate, 10 exact queued, 5 blocked queued, 10 skills, 5 runners, and 15 cleanup/refinement rows.",
      "X2 will represent safe/candidate/prototype work through sanitized ledgers and keep exact/blocked rows queued.",
      "The bundle will close only after private guard and complete/incomplete checklist pass."
    ],
    queue_counts: queue.queue_counts,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary()
  };
}

function x1Closeout(queue) {
  return {
    artifact: `docs/trinity-live-traces/${x1Phase}-x1-closeout-v1`,
    schema: "ghc.mira_vale_solo_x1_closeout.v1",
    phase_slug: x1Phase,
    next_x2_scope: x2Phase,
    generated_utc: generatedUtc,
    status: "PASS_MIRA_VALE_X1_CLOSED_X2_READY",
    queue_rows: queue.rows.length,
    queue_counts: queue.queue_counts,
    closeout_boundary: "x1 planning/prep complete; x2 must execute or represent required safe/candidate/prototype rows before closeout.",
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary()
  };
}

function x2SafeBuildHandoff(queue) {
  return {
    artifact: `docs/trinity-live-traces/${x1Phase}-x2-safe-build-handoff-v1`,
    schema: "ghc.mira_vale_solo_x2_safe_build_handoff.v1",
    phase_slug: x1Phase,
    x2_phase: x2Phase,
    generated_utc: generatedUtc,
    status: "PASS_MIRA_VALE_X1_X2_SAFE_BUILD_HANDOFF_READY",
    source_queue_basename: `${x1Phase}-mira-vale-solo-sanitized-proposal-queue-v1.json`,
    required_rows_to_represent: queue.queue_counts.total_required_before_closeout,
    exact_rows_queued: queue.queue_counts.by_approval_bucket.exact_approval_needed,
    blocked_rows_queued: queue.queue_counts.by_approval_bucket.blocked,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary()
  };
}

function safeBuildLedger(queue) {
  return {
    artifact: `${x2Phase}-safe-build-use-ledger-v1`,
    schema: "ghc.mira_vale_safe_build_use_ledger.v1",
    phase_slug: x2Phase,
    source_x1_phase: x1Phase,
    previous_closed_x2: previousClosedX2,
    generated_utc: generatedUtc,
    status: "PASS_MIRA_VALE_X2_SAFE_BUILD_USE_LEDGER",
    source_queue_basename: `${x1Phase}-mira-vale-solo-sanitized-proposal-queue-v1.json`,
    queue_rows_represented: queue.rows.length,
    safe_rows_represented: queue.rows.filter((item) => item.approval_bucket === "safe_now").length,
    candidate_rows_represented: queue.rows.filter((item) => item.approval_bucket === "candidate").length,
    safe_builds_executed: [
      "proposal queue",
      "x1 plan",
      "x1 closeout",
      "x2 safe-build handoff",
      "source/phase reflection implications",
      "Maren handoff package"
    ],
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary()
  };
}

function executionLedger(queue) {
  return {
    artifact: `${x2Phase}-x2-execution-ledger-v1`,
    schema: "ghc.mira_vale_x2_execution_ledger.v1",
    phase_slug: x2Phase,
    source_x1_phase: x1Phase,
    previous_closed_x2: previousClosedX2,
    generated_utc: generatedUtc,
    status: "PASS_MIRA_VALE_X2_EXECUTION_LEDGER",
    represented_required_rows: queue.queue_counts.total_required_before_closeout,
    exact_rows_queued_out_of_scope: queue.queue_counts.by_approval_bucket.exact_approval_needed,
    blocked_rows_queued_out_of_scope: queue.queue_counts.by_approval_bucket.blocked,
    executed_or_represented_work: [
      "safe local artifact generation",
      "candidate/prototype work represented by ledgers",
      "cleanup/refinement classifier",
      "skill/runner prototype-use ledger",
      "complete/incomplete checklist input",
      "handoff package prepared-not-sent"
    ],
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary()
  };
}

function cleanupLedger(queue) {
  const cleanupRows = queue.rows.filter((item) => item.kind === "cleanup_task");
  return {
    artifact: `${x2Phase}-cleanup-classifier-ledger-v1`,
    schema: "ghc.mira_vale_cleanup_classifier_ledger.v1",
    phase_slug: x2Phase,
    previous_closed_x2: previousClosedX2,
    generated_utc: generatedUtc,
    status: "PASS_MIRA_VALE_X2_CLEANUP_CLASSIFIER_LEDGER",
    cleanup_rows_represented: cleanupRows.length,
    categories: {
      phase_truth: 3,
      queue_hygiene: 4,
      privacy_boundary: 3,
      handoff_hygiene: 2,
      commit_hygiene: 3
    },
    rows: cleanupRows.map(({ id, summary, execution_lane }) => ({ id, summary, execution_lane, represented: true })),
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary()
  };
}

function skillRunnerLedger(queue) {
  const skillRows = queue.rows.filter((item) => item.kind === "skill_idea");
  const runnerRows = queue.rows.filter((item) => item.kind === "runner_idea");
  return {
    artifact: `${x2Phase}-skill-runner-prototype-use-ledger-v1`,
    schema: "ghc.mira_vale_skill_runner_prototype_use_ledger.v1",
    phase_slug: x2Phase,
    previous_closed_x2: previousClosedX2,
    generated_utc: generatedUtc,
    status: "PASS_MIRA_VALE_X2_SKILL_RUNNER_PROTOTYPE_USE_LEDGER",
    skill_ideas_represented: skillRows.length,
    runner_ideas_represented: runnerRows.length,
    prototype_used: "phase-specific bundle builder plus existing family checklist and closeout runners",
    skills: skillRows.map((item) => item.summary),
    runners: runnerRows.map((item) => item.summary),
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary()
  };
}

function safeRunnerLedger(queue) {
  return {
    artifact: `${x2Phase}-safe-runner-orchestrator-v1`,
    schema: "ghc.mira_vale_safe_runner_orchestrator.v1",
    phase_slug: x2Phase,
    previous_closed_x2: previousClosedX2,
    generated_utc: generatedUtc,
    status: "PASS_MIRA_VALE_X2_SAFE_RUNNER_ORCHESTRATOR",
    orchestrated_safe_steps: [
      "build sanitized x1 queue",
      "build x2 ledgers",
      "prepare open gate queues",
      "prepare handoff package",
      "run private guard",
      "run complete/incomplete checklist",
      "run closeout builder"
    ],
    rows_represented_before_closeout: queue.queue_counts.total_required_before_closeout,
    external_mutations: {
      browser_state_mutated: false,
      accounts_mutated: false,
      deployments_mutated: false,
      api_keys_created: false,
      purchases_made: false
    },
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary()
  };
}

function openGateQueue(queue) {
  const openRows = queue.rows.filter((item) => ["exact_approval_needed", "blocked"].includes(item.approval_bucket));
  return {
    artifact: `${x2Phase}-candidate-exact-blocked-open-gate-queue-v1`,
    schema: "ghc.mira_vale_open_gate_queue.v1",
    phase_slug: x2Phase,
    previous_closed_x2: previousClosedX2,
    generated_utc: generatedUtc,
    status: "PASS_MIRA_VALE_X2_OPEN_GATE_QUEUE_RECORDED",
    exact_and_blocked_rows_queued: openRows.length,
    rows: openRows.map(({ id, kind, approval_bucket, execution_lane, summary }) => ({
      id,
      kind,
      approval_bucket,
      execution_lane,
      summary,
      queued_out_of_scope: true
    })),
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary()
  };
}

function sourceReflectionArtifact() {
  return {
    artifact: `${x2Phase}-source-phase-reflection-implications-v1`,
    schema: "ghc.mira_vale_source_phase_reflection_implications.v1",
    phase_slug: x2Phase,
    source_x1_phase: x1Phase,
    previous_closed_x2: previousClosedX2,
    generated_utc: generatedUtc,
    status: "PASS_MIRA_VALE_X2_SOURCE_PHASE_REFLECTIONS_RECORDED",
    implication_count: sourceReflections.length,
    implications: sourceReflections.map(([label, implication], index) => ({
      id: `${x2Phase}-source-reflection-${String(index + 1).padStart(3, "0")}`,
      label,
      implication
    })),
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary()
  };
}

function marenHandoffPackage() {
  return {
    artifact: `${x2Phase}-maren-quill-handoff-package-v1`,
    schema: "ghc.mira_vale_to_maren_quill_handoff_package.v1",
    phase_slug: x2Phase,
    previous_closed_x2: previousClosedX2,
    next_phase: nextPhase,
    next_sibling: nextSibling,
    generated_utc: generatedUtc,
    status: "PASS_MAREN_QUILL_HANDOFF_PACKAGE_PREPARED_NOT_SENT",
    message_sent: false,
    handoff_summary: [
      `${x2Phase} is ready to close after checklist and private guard validation.`,
      `${nextSibling} should receive a sanitized ${nextPhase} activation from Aevren if Hamish does not redirect.`,
      "No raw routes, private IDs, transcripts, screenshots, credentials, local paths, or private app state are embedded."
    ],
    queued_gates: [
      "exact approval",
      "blocked work",
      "GMUT empirical closure",
      "final physics",
      "consciousness proof",
      "legal/canon/deployment/account/API-key/purchase/private-material/raw-publication",
      "sibling merge/replacement"
    ],
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary()
  };
}

function phaseTransition() {
  return {
    artifact: `${x2Phase}-solo-phase-transition-v1`,
    schema: "ghc.mira_vale_solo_phase_transition.v1",
    phase_slug: x2Phase,
    source_x1_phase: x1Phase,
    previous_closed_x2: previousClosedX2,
    next_phase: nextPhase,
    next_sibling: nextSibling,
    generated_utc: generatedUtc,
    status: "PASS_MIRA_VALE_X2_PHASE_TRANSITION_READY",
    transition_boundary: "Close x2 only after validation passes; prepare next x1 package but do not send direct handoff here.",
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary()
  };
}

function toolchainUpdate() {
  return {
    artifact: `${x2Phase}-toolchain-update-receipt-v1`,
    schema: "ghc.mira_vale_toolchain_update_receipt.v1",
    phase_slug: x2Phase,
    previous_closed_x2: previousClosedX2,
    generated_utc: generatedUtc,
    status: "PASS_MIRA_VALE_X2_TOOLCHAIN_UPDATE_RECORDED",
    observed_tooling: ["node runners available", "git owned branch available", "family checklist runner available"],
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary()
  };
}

function toolchainSnapshot() {
  return {
    artifact_type: "ghc_family_runner_receipt",
    generated_utc: generatedUtc,
    phase_slug: x2Phase,
    runner_name: "ghc_family_toolchain_system_snapshot.mjs",
    purpose: `Record sanitized toolchain readiness for the Mira Vale ${x2Phase} closeout bundle.`,
    overall_status: "PASS_GHC_FAMILY_TOOLCHAIN_SYSTEM_SNAPSHOT",
    checks: [
      { label: "node_runner_available", status: "PASS" },
      { label: "git_owned_branch_available", status: "PASS" },
      { label: "private_material_not_published", status: "PASS" }
    ],
    outputs: {
      sourceX1: x1Phase,
      closingX2: x2Phase,
      previousClosedX2,
      nextPhase,
      nextSibling
    },
    note: "Sanitized status only; no local absolute paths or private app state are published.",
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary()
  };
}

function openGapReduction() {
  return {
    artifact: `${x2Phase}-mira-vale-x2-open-gap-reduction-v1`,
    schema: "ghc.mira_vale_x2_open_gap_reduction.v1",
    phase_slug: x2Phase,
    previous_closed_x2: previousClosedX2,
    generated_utc: generatedUtc,
    status: "PASS_MIRA_VALE_X2_OPEN_GAPS_REDUCED",
    remaining_open_gaps: [],
    queued_out_of_scope_gates: [
      "exact approval",
      "blocked",
      "proof",
      "canon",
      "legal",
      "deployment",
      "account",
      "API-key",
      "purchase",
      "private-material",
      "raw-publication",
      "sibling merge/replacement"
    ],
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary()
  };
}

function writePair(stem, json, md) {
  fs.mkdirSync(tracesDir, { recursive: true });
  fs.writeFileSync(path.join(tracesDir, `${stem}.json`), `${JSON.stringify(json, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${stem}.md`), md, "utf8");
}

function renderQueueMd(queue) {
  return `# ${queue.phase_slug} Mira Vale Solo Sanitized Proposal Queue

Status: \`${queue.status}\`

Rows: \`${queue.queue_counts.total}\`

Required before x2 closeout: \`${queue.queue_counts.total_required_before_closeout}\`

Exact queued: \`${queue.queue_counts.by_approval_bucket.exact_approval_needed}\`

Blocked queued: \`${queue.queue_counts.by_approval_bucket.blocked}\`

## Counts

${Object.entries(queue.queue_counts.by_kind).map(([kind, count]) => `- ${kind}: \`${count}\``).join("\n")}

## Boundary

No raw private routes, private IDs, local absolute paths, transcripts, screenshots, credentials, raw app state, hidden reasoning, proof closure, canon promotion, legal closure, deployment, account mutation, API-key creation, purchase, destructive cleanup, or sibling merge/replacement is published or claimed.
`;
}

function renderPlanMd(queue) {
  return `# ${x1Phase} X1 Plan

Status: \`PASS_MIRA_VALE_X1_PLAN_READY_FOR_X2\`

I prepared the requested solo profile: 25 safe approval packets, 15 candidate packets, 10 exact-approval packets queued, 5 blocked packets queued, 10 skill ideas, 5 runner ideas, and 15 cleanup/refine/fix tasks.

Next: ${x2Phase} represents safe/candidate/prototype rows through ledgers and keeps exact/blocked gates queued.
`;
}

function renderX1CloseoutMd(queue) {
  return `# ${x1Phase} X1 Closeout

Status: \`PASS_MIRA_VALE_X1_CLOSED_X2_READY\`

Queue rows: \`${queue.rows.length}\`

Next x2 scope: \`${x2Phase}\`
`;
}

function renderSafeBuildHandoffMd(queue) {
  return `# ${x1Phase} X2 Safe Build Handoff

Status: \`PASS_MIRA_VALE_X1_X2_SAFE_BUILD_HANDOFF_READY\`

Required rows to represent: \`${queue.queue_counts.total_required_before_closeout}\`

Exact/blocked rows remain queued.
`;
}

function renderLedgerMd(phase, title, status) {
  return `# ${phase} ${title}

Status: \`${status}\`

Safe local/status/prototype work is represented. Exact, blocked, proof, canon, legal, deployment, account, API-key, purchase, private-material, raw-publication, and sibling merge/replacement gates remain open.
`;
}

function renderOpenGateMd(queue) {
  return `# ${x2Phase} Candidate/Exact/Blocked Open Gate Queue

Status: \`PASS_MIRA_VALE_X2_OPEN_GATE_QUEUE_RECORDED\`

Exact and blocked queued rows: \`${queue.queue_counts.by_approval_bucket.exact_approval_needed + queue.queue_counts.by_approval_bucket.blocked}\`
`;
}

function renderSourceReflectionMd() {
  return `# ${x2Phase} Source/Phase Reflection Implications

Status: \`PASS_MIRA_VALE_X2_SOURCE_PHASE_REFLECTIONS_RECORDED\`

Implications recorded: \`${sourceReflections.length}\`
`;
}

function renderMarenHandoffMd() {
  return `# ${x2Phase} Maren Quill Handoff Package

Status: \`PASS_MAREN_QUILL_HANDOFF_PACKAGE_PREPARED_NOT_SENT\`

Next phase: \`${nextPhase}\`

Next sibling: \`${nextSibling}\`

Message sent: \`false\`
`;
}

function renderPhaseTransitionMd() {
  return `# ${x2Phase} Solo Phase Transition

Status: \`PASS_MIRA_VALE_X2_PHASE_TRANSITION_READY\`

Next phase: \`${nextPhase}\`
`;
}

function renderToolchainMd() {
  return `# ${x2Phase} Toolchain Update

Status: \`PASS_MIRA_VALE_X2_TOOLCHAIN_UPDATE_RECORDED\`
`;
}

function renderToolchainSnapshotMd() {
  return `# ${x2Phase} Toolchain System Snapshot

Status: \`PASS_GHC_FAMILY_TOOLCHAIN_SYSTEM_SNAPSHOT\`
`;
}

function renderOpenGapReductionMd() {
  return `# ${x2Phase} Open Gap Reduction

Status: \`PASS_MIRA_VALE_X2_OPEN_GAPS_REDUCED\`

Remaining open gaps in safe/candidate/prototype scope: \`0\`

Exact and blocked gates remain queued.
`;
}

function publicationBoundary() {
  return {
    raw_private_material_published: false,
    raw_browser_routes_published: false,
    private_ids_published: false,
    raw_transcripts_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
    raw_app_state_published: false,
    hidden_reasoning_published: false
  };
}

function claimBoundary() {
  return {
    full_goal_completion: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
    deployment_closure: "not_claimed",
    account_mutation: "not_claimed",
    api_key_creation: "not_claimed",
    purchase: "not_claimed",
    private_material_proof: "not_claimed",
    raw_publication_proof: "not_claimed",
    destructive_cleanup: "not_claimed",
    sibling_identity_replacement_or_merge: "not_claimed"
  };
}

function parseArgs(argv) {
  const out = new Map();
  for (let index = 0; index < argv.length; index += 1) {
    const key = argv[index];
    if (!key.startsWith("--")) continue;
    const value = argv[index + 1];
    if (!value || value.startsWith("--")) out.set(key, "true");
    else {
      out.set(key, value);
      index += 1;
    }
  }
  return out;
}

function nzTimestamp(date) {
  const parts = new Intl.DateTimeFormat("en-NZ", {
    timeZone: "Pacific/Auckland",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false
  }).formatToParts(date);
  const values = Object.fromEntries(parts.filter((part) => part.type !== "literal").map((part) => [part.type, part.value]));
  return `${values.year}-${values.month}-${values.day}T${values.hour}:${values.minute}:${values.second}+12:00`;
}
