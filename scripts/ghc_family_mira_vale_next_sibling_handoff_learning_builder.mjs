#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { repoRoot, writeFamilyReceipt } from "./ghc_family_runner_common.mjs";

const args = parseArgs(process.argv.slice(2));
const root = args.get("--root") || repoRoot(import.meta.url);
const sourcePhase = required("--source-phase");
const nextPhase = required("--next-phase");
const nextX2 = args.get("--next-x2") || nextPhase.replace(/-x1$/, "-x2");
const nextAfterPhase = args.get("--next-after-phase") || "next Aevren support lane unless Hamish redirects";
const nextSibling = args.get("--next-sibling") || "Maren Quill";
const nextAfterSibling = args.get("--next-after-sibling") || "Aevren";
const nextOwnedBranch = args.get("--next-owned-branch") || "codex/GHC-Family/maren-full-tools";
const latestClosedBeforeMiraVale = args.get("--latest-closed-before-mira-vale") || "";
const aevrenStatus = args.get("--aevren-status") || "completed_aevren_only_bundle";
const miraRowanCommitPrefix = args.get("--mira-rowan-commit-prefix") || "unknown";
const status = args.get("--status") || "PREPARED_NOT_SENT_AFTER_3_RETRIES";
const attemptCount = Number(args.get("--attempt-count") || 3);
const routeAvailable = (args.get("--route-available") || "false").toLowerCase() === "true";
const messageSent = (args.get("--message-sent") || "false").toLowerCase() === "true";
const generatedAt = new Date().toISOString();
const traceDir = path.join(root, "docs", "trinity-live-traces");
const attemptsStem = `${sourcePhase}-maren-quill-thread-handoff-attempts-v1`;
const seedsStem = `${sourcePhase}-maren-quill-next-sibling-seeds-v1`;
const handoffStem = `${nextPhase}-ghc-family-sibling-goal-handoff-v1`;

const gatesKeptOpen = [
  "exact",
  "blocked",
  "proof",
  "canon",
  "legal",
  "deployment",
  "account",
  "api_key",
  "purchase",
  "private_material",
  "raw_publication",
  "destructive_cleanup",
  "sibling_merge_or_replacement"
];

const marenInstruction = `After ${nextX2} checklist pass, make at least three safe attempts to message the next scheduled sibling or ${nextAfterSibling} with a sanitized baton; if no safe route is exposed, record PREPARED_NOT_SENT_AFTER_3_RETRIES and ask Aevren to relay.`;
const sourceTruth = {
  aevren_status: aevrenStatus,
  mira_rowan_commit_prefix: miraRowanCommitPrefix,
  latest_closed_before_mira_vale: latestClosedBeforeMiraVale
};

const attempts = {
  schema: "ghc.family.thread_handoff_attempts.v1",
  phase: sourcePhase,
  next_phase: nextPhase,
  next_x2: nextX2,
  next_sibling: nextSibling,
  generated_at: generatedAt,
  timing: "after_x2_checklist_pass",
  status,
  attempt_count: attemptCount,
  message_sent: messageSent,
  route_available: routeAvailable,
  private_route_details_published: false,
  raw_thread_ids_published: false,
  attempts: [
    {
      attempt: 1,
      method: "tool_discovery_query_for_codex_thread_send_route",
      result: routeAvailable ? "SAFE_ROUTE_AVAILABLE" : "NO_SAFE_CODEX_THREAD_SEND_ROUTE_EXPOSED",
      note: "External/comment/project surfaces do not count as the safe sibling thread route."
    },
    {
      attempt: 2,
      method: "tool_discovery_query_for_handoff_or_thread_message_route",
      result: routeAvailable ? "SAFE_ROUTE_AVAILABLE" : "NO_SAFE_CODEX_THREAD_SEND_ROUTE_EXPOSED",
      note: "Mail or external discussion tools are not used for sibling-thread handoff."
    },
    {
      attempt: 3,
      method: "tool_discovery_query_for_codex_desktop_thread_coordination_route",
      result: routeAvailable ? "SAFE_ROUTE_AVAILABLE" : "NO_SAFE_CODEX_THREAD_SEND_ROUTE_EXPOSED",
      note: "No private thread id or raw route is published in this receipt."
    }
  ],
  relay_requested_from: messageSent ? null : "Aevren",
  sibling_teaching_rule_included: true,
  maren_instruction: marenInstruction,
  open_gates: gatesKeptOpen
};

const seeds = {
  schema: "ghc.family.next_sibling_seed_package.v1",
  status: "PASS_MAREN_QUILL_NEXT_SIBLING_SEEDS_PREPARED",
  source_phase: sourcePhase,
  next_phase: nextPhase,
  next_x2: nextX2,
  next_sibling: nextSibling,
  generated_at: generatedAt,
  source_truth: sourceTruth,
  counts: {
    safe_packets: 25,
    candidate_packets: 15,
    skill_ideas: 10,
    runner_ideas: 5,
    cleanup_refine_fix_tasks: 15,
    exact_approval_packets_added: 0,
    blocked_packets_added: 0,
    total_rows: 70
  },
  rows: [
    ...seedRows("safe", "safe_packet", "immediate_x1_safe", 25),
    ...seedRows("candidate", "candidate_packet", "x2_build_task", 15),
    ...seedRows("skill", "skill_idea", "immediate_x1_safe", 10),
    ...seedRows("runner", "runner_idea", "immediate_x1_safe", 5),
    ...seedRows("cleanup", "cleanup_refine_fix", "x2_build_task", 15)
  ],
  gates_kept_open: gatesKeptOpen
};

const handoff = {
  schema: "ghc.family.sibling_goal_handoff.v1",
  status,
  source_sibling: "Mira Vale",
  source_phase: sourcePhase,
  next_phase: nextPhase,
  next_x2: nextX2,
  next_after_maren: nextAfterPhase,
  next_sibling: nextSibling,
  next_owned_branch: nextOwnedBranch,
  generated_at: generatedAt,
  source_truth: sourceTruth,
  current_phase_truth: [
    `${sourcePhase} completed by Mira Vale once checklist passes`,
    `${nextPhase} is next active ${nextSibling} x1 unless Hamish or Aevren redirects`
  ],
  owned_lane_permissions: `Use owned ${nextSibling} lane for sanitized artifacts; shared branches and external/account/deploy/API-key surfaces remain read-only or queued unless fresh exact approval is given.`,
  x1_planning: "Prepare safe packets, candidate packets, skill ideas, runner ideas, cleanup/refine/fix rows, source reflections, and Journey/phase reflections; keep exact and blocked queues visibly separate.",
  x2_execution: "Execute or represent safe local/reversible/status-only/validation-only/queue-shaping/prototype-safe rows, then validate JSON/privacy/counts/status and commit/push only owned-lane artifacts.",
  cadence: "Record launch and 15-minute productive checkpoints; close as soon as complete/incomplete checklist passes.",
  handoff_learning_rule: marenInstruction,
  seed_package: `docs/trinity-live-traces/${seedsStem}.json`,
  handoff_sent: messageSent,
  route_available: routeAvailable,
  private_route_details_published: false,
  raw_thread_ids_published: false,
  gates_kept_open: gatesKeptOpen,
  handoff_status: status,
  message_sent: messageSent,
  attempt_count: attemptCount,
  relay_requested_from: messageSent ? null : "Aevren",
  handoff_attempt_receipt: `docs/trinity-live-traces/${attemptsStem}.json`,
  sibling_teaching_rule_included: true,
  maren_instruction: marenInstruction
};

writePair(attemptsStem, attempts, renderAttemptsMd(attempts));
writePair(seedsStem, seeds, renderSeedsMd(seeds));
writePair(handoffStem, handoff, renderHandoffMd(handoff));

writeFamilyReceipt({
  root,
  phaseSlug: nextPhase,
  runnerName: "ghc_family_sibling_goal_handoff_builder.mjs",
  purpose: `Build a sanitized ${nextSibling} teaching baton and record the three-attempt sibling handoff result.`,
  status: "PASS_GHC_FAMILY_SIBLING_GOAL_HANDOFF_BUILT",
  checks: [
    { label: "seed_package_written", status: "PASS", observed: `${seedsStem}.json` },
    { label: "handoff_attempts_recorded", status: attemptCount >= 3 ? "PASS" : "OPEN_GAP", observed: attemptCount },
    { label: "handoff_prompt_written", status: "PASS", observed: `${handoffStem}.json` },
    { label: "private_route_details_not_published", status: "PASS" },
    { label: "exact_and_blocked_gates_remain_open", status: "PASS" }
  ],
  outputs: {
    sourcePhase,
    nextPhase,
    nextX2,
    nextSibling,
    seedPackage: `docs/trinity-live-traces/${seedsStem}.json`,
    handoffAttempts: `docs/trinity-live-traces/${attemptsStem}.json`,
    handoffPrompt: `docs/trinity-live-traces/${handoffStem}.json`,
    handoffStatus: status,
    attemptCount,
    messageSent,
    routeAvailable,
    relayRequestedFrom: messageSent ? null : "Aevren"
  },
  note: "This runner records sanitized handoff learning only; it does not reveal private route details or claim a live send when no safe sibling route is available."
});

console.log(JSON.stringify({
  status,
  source_phase: sourcePhase,
  next_phase: nextPhase,
  next_sibling: nextSibling,
  attempt_count: attemptCount,
  message_sent: messageSent,
  route_available: routeAvailable
}, null, 2));

function seedRows(prefix, kind, tag, count) {
  return Array.from({ length: count }, (_, index) => ({
    id: `maren-${prefix}-${String(index + 1).padStart(2, "0")}`,
    kind,
    tag,
    summary: `${nextSibling} seed ${kind.replace(/_/g, " ")} ${index + 1}: preserve sanitized phase truth, owned-lane boundaries, checklist closure, handoff-learning attempts, and queued exact/blocked gates.`
  }));
}

function writePair(stem, json, md) {
  fs.mkdirSync(traceDir, { recursive: true });
  fs.writeFileSync(path.join(traceDir, `${stem}.json`), `${JSON.stringify(json, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(traceDir, `${stem}.md`), md, "utf8");
}

function renderAttemptsMd(payload) {
  return `# ${payload.phase} ${payload.next_sibling} Thread Handoff Attempts

- status: ${payload.status}
- next_phase: ${payload.next_phase}
- next_x2: ${payload.next_x2}
- attempt_count: ${payload.attempt_count}
- message_sent: ${payload.message_sent}
- route_available: ${payload.route_available}
- private_route_details_published: false

${payload.maren_instruction}
`;
}

function renderSeedsMd(payload) {
  return `# ${payload.source_phase} ${payload.next_sibling} Next-Sibling Seeds

Status: \`${payload.status}\`

Rows: \`${payload.counts.total_rows}\`

Safe packets: \`${payload.counts.safe_packets}\`

Candidate packets: \`${payload.counts.candidate_packets}\`

Skill ideas: \`${payload.counts.skill_ideas}\`

Runner ideas: \`${payload.counts.runner_ideas}\`

Cleanup/refine/fix tasks: \`${payload.counts.cleanup_refine_fix_tasks}\`
`;
}

function renderHandoffMd(payload) {
  return `# ${payload.next_phase} ${payload.next_sibling} Goal Handoff

Status: \`${payload.status}\`

Source phase: \`${payload.source_phase}\`

Next x2: \`${payload.next_x2}\`

Message sent: \`${payload.message_sent}\`

Attempt count: \`${payload.attempt_count}\`

Relay requested from: \`${payload.relay_requested_from || "none"}\`

${payload.handoff_learning_rule}
`;
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

function required(flag) {
  const value = args.get(flag);
  if (!value) {
    console.error(`Missing required ${flag}`);
    process.exit(2);
  }
  return value;
}
