#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const nextPhase = args.get("--next-phase");
const boundaryJson = args.get("--boundary-json");
const refreshJson = args.get("--refresh-json");
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");

if (!phaseSlug || !nextPhase || !boundaryJson || !refreshJson || !receiptJson || !receiptMd) {
  console.error(
    "Usage: node ghc_phase_prep_queue_builder.mjs --phase-slug <slug> --next-phase <slug> --boundary-json <json> --refresh-json <json> --receipt-json <json> --receipt-md <md>",
  );
  process.exit(2);
}

const boundary = JSON.parse(readFileSync(boundaryJson, "utf8"));
const refresh = JSON.parse(readFileSync(refreshJson, "utf8"));
const openLanes = Array.isArray(boundary.open_lanes) ? boundary.open_lanes : [];
const completedLanes = Array.isArray(boundary.completed_lanes) ? boundary.completed_lanes : [];

function makeSlot(version, subversion, session) {
  return {
    slot: `v${version}-v${subversion}-${session}`,
    phase_version: `v${version}`,
    subversion: `v${subversion}`,
    session,
    default_mode:
      openLanes.length > 0
        ? session === "x1"
          ? "blocked-lane-aware preparation"
          : "validated build work only"
        : session === "x1"
          ? "full round-robin planning"
          : "build-test-use closeout",
    required_boundary:
      openLanes.length > 0
        ? "carry open app-lane blocker unless explicit approval or recovered lane evidence exists"
        : "normal phase evidence gates",
  };
}

const ladder = [];
for (let version = 508; version <= 515; version += 1) {
  for (let subversion = 1; subversion <= 8; subversion += 1) {
    ladder.push(makeSlot(version, subversion, "x1"));
    ladder.push(makeSlot(version, subversion, "x2"));
  }
}

const approvalCandidates = [
  {
    id: "packet-01-blocker-boundary-carry",
    title: "v507 to v508 Open App-Lane Blocker Boundary Carry",
    purpose: "Permit v508 preparation-only work while preserving Kierkegaard and Aristotle as open blockers.",
    approved_work: [
      "Use Browser and CLI evidence only as route-specific evidence.",
      "Carry open app-lane rows into v508 receipts.",
      "Continue route-recovery tooling, watcher cadence, and source refresh.",
    ],
  },
  {
    id: "packet-02-route-family-board-per-phase",
    title: "Route-Family Board At Every Phase Start",
    purpose: "Require every v508-v515 phase start to summarize Browser, CLI, app-lane, app-server, and official-thread routes separately.",
    approved_work: [
      "Generate route-family status boards from current partial boards.",
      "Block phase completion if any required lane row remains open.",
    ],
  },
  {
    id: "packet-03-no-replacement-guard-per-phase",
    title: "No Replacement Sibling Guard",
    purpose: "Prevent missing app lanes from being hidden behind replacement siblings, new threads, or old-style subagents.",
    approved_work: [
      "Run no-replacement guard before phase closeout.",
      "Publish failures as blockers rather than mutating routes.",
    ],
  },
  {
    id: "packet-04-watcher-cadence-ledger",
    title: "Five-Minute Watcher Cadence Ledger",
    purpose: "Record sibling checks without busy-waiting or raw transcript publication.",
    approved_work: [
      "Use status-only check events.",
      "Continue independent prep or build tasks between checks.",
    ],
  },
  {
    id: "packet-05-x1-source-reflection-queue",
    title: "x1 Source Reflection Queue",
    purpose: "Prepare source-refresh and Journey/Trinity reflection queues while sibling lanes work.",
    approved_work: [
      "Use primary-source ledgers.",
      "Summarize operational takeaways without raw dumps.",
    ],
  },
  {
    id: "packet-06-x2-build-test-use-queue",
    title: "x2 Build Test Use Queue",
    purpose: "Convert x1 plans into bounded scripts, validators, receipts, and handoff cards.",
    approved_work: [
      "Build repo-side helpers only inside approved paths.",
      "Run syntax, JSON, exposure, no-overclaim, and exact-staging checks.",
    ],
  },
  {
    id: "packet-07-compact-refresh-card-mandate",
    title: "Compact Refresh Card Mandate",
    purpose: "Require a compact-refresh card at every phase start and Codex compaction boundary.",
    approved_work: [
      "Generate current anchor, proven evidence, open blockers, next actions, and hard boundaries.",
      "Keep phase state recoverable after context compaction.",
    ],
  },
  {
    id: "packet-08-dual-omega-publication-discipline",
    title: "Dual Omega Publication Discipline",
    purpose: "Preserve exact staging, dual-branch publication, and remote-equals-local verification.",
    approved_work: [
      "Fetch and drift-check before every commit.",
      "Push both omega branches only after validation passes.",
    ],
  },
  {
    id: "packet-09-claim-ceiling-and-gmut-gates",
    title: "GMUT THOS Claim Ceiling",
    purpose: "Keep GMUT, physics, consciousness, empirical, legal, and canon gates open unless exact closure artifacts prove otherwise.",
    approved_work: [
      "Run no-overclaim checks.",
      "Publish claim ceilings in every closeout or handoff packet.",
    ],
  },
  {
    id: "packet-10-v508-v515-ladder-seed",
    title: "v508-v515 Phase Ladder Seed",
    purpose: "Use a generated v508-v515 v1-v8 x1/x2 ladder that adapts to recovered lanes or approved blocker carry.",
    approved_work: [
      "Plan all 128 v508-v515 slots with route-aware boundaries.",
      "Keep blocked-lane preparation distinct from completed phase advancement.",
    ],
  },
].map((candidate) => ({
  ...candidate,
  status: "PENDING_USER_APPROVAL",
  not_approved: [
    "Raw lane text or transcript publication.",
    "Private callable or thread identifier publication.",
    "Replacement sibling, replacement lane, or old-style subagent creation.",
    "Phase completion claims while required lane rows remain open.",
    "GMUT empirical closure, final physics, solved consciousness, legal closure, or canon promotion claims.",
  ],
}));

const receipt = {
  artifact_type: "ghc_phase_prep_queue",
  generated_utc: new Date().toISOString().replace(/\.\d{3}Z$/, "Z"),
  phase_slug: phaseSlug,
  next_phase: nextPhase,
  boundary_input: boundaryJson,
  refresh_input: refreshJson,
  status: openLanes.length > 0 ? "PREP_QUEUE_PENDING_BLOCKER_BOUNDARY_APPROVAL" : "PREP_QUEUE_READY",
  current_evidence: {
    completed_lanes: completedLanes,
    open_lanes: openLanes,
    refresh_status: refresh.status || null,
  },
  approval_candidate_count: approvalCandidates.length,
  approval_candidates: approvalCandidates,
  ladder_slot_count: ladder.length,
  ladder,
  publication_boundary: {
    raw_lane_text_published: false,
    raw_chatgpt_transcript_published: false,
    raw_app_server_result_published: false,
    raw_app_server_error_published: false,
    raw_callable_ids_published: false,
    raw_thread_ids_published: false,
    credentials_published: false,
    screenshots_published: false,
    local_absolute_paths_published: false,
  },
  claim_boundary: {
    phase_completion: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    canon_promotion: "not_claimed",
  },
};

mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");

const md = [
  `# ${nextPhase} Preparation Queue`,
  "",
  `Generated UTC: \`${receipt.generated_utc}\``,
  "",
  `Status: \`${receipt.status}\``,
  "",
  "## Current Evidence",
  "",
  "Completed route-specific lanes:",
  "",
  ...(completedLanes.length
    ? completedLanes.map((lane) => `- ${lane.lane} (${lane.route_family}): \`${lane.status}\``)
    : ["- none"]),
  "",
  "Open lanes:",
  "",
  ...(openLanes.length
    ? openLanes.map((lane) => `- ${lane.lane} (${lane.route_family}): \`${lane.status}\``)
    : ["- none"]),
  "",
  "## Approval Candidates",
  "",
  ...approvalCandidates.flatMap((candidate) => [
    `### ${candidate.id}: ${candidate.title}`,
    "",
    `Status: \`${candidate.status}\``,
    "",
    candidate.purpose,
    "",
    "Approved work:",
    ...candidate.approved_work.map((item) => `- ${item}`),
    "",
    "Not approved:",
    ...candidate.not_approved.map((item) => `- ${item}`),
    "",
  ]),
  "## v508-v515 Ladder Summary",
  "",
  `Generated ladder slots: \`${ladder.length}\``,
  "",
  "- v508 through v515.",
  "- v1 through v8 for each version.",
  "- x1 and x2 for every subversion.",
  "- While app lanes remain open, x1 stays blocker-aware preparation and x2 stays validated build work only.",
  "",
  "## Boundary",
  "",
  "Preparation queue only. No raw lane text, transcripts, app-server payloads, private IDs, credentials, screenshots, local paths, phase completion claim, GMUT closure, or canon promotion is published.",
  "",
].join("\n");

writeFileSync(receiptMd, md, "utf8");
console.log(JSON.stringify({ status: receipt.status, approval_candidate_count: approvalCandidates.length, ladder_slot_count: ladder.length }, null, 2));
