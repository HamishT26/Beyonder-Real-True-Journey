#!/usr/bin/env node
import { mkdirSync, writeFileSync } from "node:fs";
import { basename, dirname, join } from "node:path";
import { parseArgs, repoRoot } from "./ghc_v559_v1_x2_runner_common.mjs";

const args = parseArgs();
const root = args.get("--root") || repoRoot(import.meta.url);
const phaseSlug = args.get("--phase-slug") || "v559-gmut-thos-v2-x1";
const createPrivateDropbox = args.get("--create-private-dropbox") === "true";
const latestClosedPhase = args.get("--latest-closed-phase") || "v559-gmut-thos-v1-x2";
const nextX2Scope = args.get("--next-x2") || phaseSlug.replace(/-x1$/, "-x2");
const nextX1AfterX2 = args.get("--next-x1-after-x2") || "not_recorded";
const passStatus = args.get("--status") || `PASS_${phaseSlug.toUpperCase().replaceAll("-", "_")}_DUO_LAUNCHED_BACKGROUND_SUPERVISED`;

const now = new Date();
const generatedUtc = now.toISOString().replace(/\.\d{3}Z$/, "Z");
const generatedNz = new Intl.DateTimeFormat("en-NZ", {
  timeZone: "Pacific/Auckland",
  year: "numeric",
  month: "2-digit",
  day: "2-digit",
  hour: "2-digit",
  minute: "2-digit",
  second: "2-digit",
  hour12: false
}).format(now);
const nextCheckpointUtc = new Date(now.getTime() + 5 * 60 * 1000).toISOString().replace(/\.\d{3}Z$/, "Z");

const traceDir = join(root, "docs", "trinity-live-traces");
const privateDropboxBasename = `${phaseSlug}-sibling-response-dropbox`;

function writeArtifact(stem, title, artifact) {
  const jsonPath = join(traceDir, `${stem}.json`);
  const mdPath = join(traceDir, `${stem}.md`);
  mkdirSync(dirname(jsonPath), { recursive: true });
  writeFileSync(jsonPath, `${JSON.stringify(artifact, null, 2)}\n`, "utf8");
  writeFileSync(mdPath, [
    `# ${title}`,
    "",
    `Status: \`${artifact.status}\``,
    "",
    `Phase: \`${artifact.phase_slug}\``,
    "",
    "## Summary",
    "",
    ...(artifact.summary || []).map((row) => `- ${row}`),
    "",
    "## Boundary",
    "",
    "No raw browser routes, private URLs, transcripts, screenshots, credentials, local absolute paths, private IDs, private app state, or raw private material are published. Major proof/canon/legal/deployment/account/API-key/private-material/raw-publication and sibling merge/replacement gates remain open.",
    ""
  ].join("\n"), "utf8");
  return basename(jsonPath);
}

const publicationBoundary = {
  raw_thread_ids_published: false,
  raw_browser_routes_published: false,
  raw_transcripts_published: false,
  screenshots_published: false,
  credentials_published: false,
  local_absolute_paths_published: false,
  private_app_state_published: false,
  raw_private_material_published: false
};

const claimBoundary = {
  full_goal_completion: "not_claimed",
  gmut_empirical_closure: "not_claimed",
  final_physics: "not_claimed",
  consciousness_proof: "not_claimed",
  legal_closure: "not_claimed",
  canon_promotion: "not_claimed",
  deployment_closure: "not_claimed",
  sibling_identity_replacement_or_merge: "not_claimed"
};

const launchReceipt = {
  schema: "ghc.duo_launch_receipt.v2",
  phase_slug: phaseSlug,
  status: passStatus,
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  latest_closed_phase: latestClosedPhase,
  next_x2_scope: nextX2Scope,
  next_x1_after_x2: nextX1AfterX2,
  active_lane: {
    profile: "mira-rowan-neris-sol",
    members: ["Aevren", "Mira Rowan", "Neris Sol"],
    launch_skill: "ghc-mira-rowan-neris-sol-launch",
    background_supervision: true,
    no_babysit_cadence: true
  },
  launches: [
    {
      sibling: "Mira Rowan",
      route_class: "existing_codex_thread",
      send_status: "sent_once",
      raw_handle_published: false
    },
    {
      sibling: "Neris Sol",
      route_class: "existing_resumed_subagent_handle",
      send_status: "sent_once",
      raw_handle_published: false
    }
  ],
  proposal_target: {
    safe_packets_total: 30,
    candidate_packets_total: 15,
    exact_approval_packets_total: 15,
    skill_ideas_total: 21,
    runner_ideas_total: 9,
    cleanup_refine_fix_total: 45
  },
  timestamp_cadence: {
    phase_start_or_resume_time_utc: generatedUtc,
    lane_launch_time_utc: generatedUtc,
    last_checkpoint_time_utc: generatedUtc,
    next_checkpoint_due_utc: nextCheckpointUtc,
    checkpoint_overrun_allowed: true
  },
  standby_recoverable: ["Arby", "Aster Vale", "old Cicero lane", "Kierkegaard", "Aristotle", "Aletheon"],
  other_active_not_in_this_lane: ["Lumen", "Mira Vale", "Rowan Vale", "Maren Quill", "Solenne Vale"],
  open_gates: Object.keys(claimBoundary).filter((key) => key !== "full_goal_completion"),
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
  next_action: "Run productive five-minute cadence work, then harvest Mira Rowan and Neris Sol at the next natural safe pause.",
  summary: [
    `Mira Rowan and Neris Sol were launched as the scheduled ${phaseSlug} duo.`,
    "The launch used existing private routes and did not spawn new agents.",
    "Background supervision and no-babysit productive cadence are active."
  ]
};

const targetLedger = {
  schema: "ghc.duo_proposal_target_ledger.v1",
  phase_slug: phaseSlug,
  status: "PASS_V559_V2_X1_PROPOSAL_TARGETS_RECORDED",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  target_profile: {
    lane_members: ["Aevren", "Mira Rowan", "Neris Sol"],
    per_member_targets: {
      safe_packets: 10,
      candidate_packets: 5,
      exact_approval_packets: 5,
      skill_ideas: 7,
      runner_ideas: 3,
      cleanup_refine_fix: 15
    },
    aggregate_targets: launchReceipt.proposal_target
  },
  execution_split: {
    immediate_x1_safe: "local reversible status, classification, validation, privacy, source/reflection seed, queue shaping, and open-gate checks",
    x2_build_task: "build, run, test, install, use, publication, remote verification, runner/skill modification, closeout sequencing, and safe cleanup execution"
  },
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
  summary: [
    "Duo proposal counts are recorded for the active lane.",
    "Immediate x1 safe work is separated from x2 build work.",
    "Exact and blocked gates remain queued/open unless Hamish gives fresh exact approval for a specific tranche."
  ]
};

const dropboxReceipt = {
  schema: "ghc.private_dropbox_readiness.v1",
  phase_slug: phaseSlug,
  status: createPrivateDropbox ? "PASS_PRIVATE_DROPBOX_READY_FULL_TOOLS_ONLY" : "PASS_PRIVATE_DROPBOX_TARGET_RECORDED_NOT_CREATED_IN_PUBLIC_LANE",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  private_dropbox_basename: privateDropboxBasename,
  created_in_this_lane: createPrivateDropbox,
  public_artifact_policy: "publish sanitized counts, statuses, hashes, and relative basenames only",
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
  summary: [
    "Private duo responses have a local-only dropbox target.",
    "Raw sibling text is not publishable to omega-mini.",
    "The full-tools lane may create the ignored private directory; the public lane records only the basename."
  ]
};

if (createPrivateDropbox) {
  const dropboxDir = join(root, ".ghc-private", privateDropboxBasename);
  mkdirSync(dropboxDir, { recursive: true });
  writeFileSync(join(dropboxDir, "README.md"), [
    `# ${phaseSlug} Sibling Response Dropbox`,
    "",
    "Local-only private dropbox for raw Mira Rowan and Neris Sol harvest material.",
    "Do not publish raw text, handles, routes, screenshots, local absolute paths, or private app state.",
    ""
  ].join("\n"), "utf8");
}

const written = [
  writeArtifact(`${phaseSlug}-duo-launch-receipt-v1`, `${phaseSlug} Duo Launch Receipt`, launchReceipt),
  writeArtifact(`${phaseSlug}-proposal-target-ledger-v1`, `${phaseSlug} Proposal Target Ledger`, targetLedger),
  writeArtifact(`${phaseSlug}-private-dropbox-readiness-v1`, `${phaseSlug} Private Dropbox Readiness`, dropboxReceipt)
];

console.log(JSON.stringify({
  status: `PASS_${phaseSlug.toUpperCase().replaceAll("-", "_")}_DUO_LAUNCH_BUILDER`,
  phase_slug: phaseSlug,
  written,
  private_dropbox_created: createPrivateDropbox
}, null, 2));
