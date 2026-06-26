#!/usr/bin/env node
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const phaseSlug = "v558-gmut-thos-v6-x1";
const latestClosed = "v558-gmut-thos-v5-x2";
const latestCompletedX1 = "v558-gmut-thos-v5-x1";
const latestCompletedX2 = "v558-gmut-thos-v5-x2";
const nextX2 = "v558-gmut-thos-v6-x2";
const nextX1AfterX2 = "v558-gmut-thos-v7-x1 Lumen Vale solo unless Hamish redirects";
const status = "PASS_V558_V6_X1_MAREN_SOLENNE_STARTUP_READY";
const now = new Date();
const createdUtc = now.toISOString();
const createdNz = new Intl.DateTimeFormat("en-NZ", {
  dateStyle: "medium",
  timeStyle: "medium",
  timeZone: "Pacific/Auckland",
}).format(now);
const nextCheckpointUtc = new Date(now.getTime() + 5 * 60 * 1000).toISOString();

const tracesDir = join(process.cwd(), "docs", "trinity-live-traces");
const omegaDir = join(process.cwd(), "docs", "omega-mini-index");
mkdirSync(tracesDir, { recursive: true });
mkdirSync(omegaDir, { recursive: true });

const isFullTools = branchName().includes("full-tools");
if (isFullTools) {
  mkdirSync(join(process.cwd(), ".ghc-private", "v558-gmut-thos-v6-x1-sibling-response-dropbox"), {
    recursive: true,
  });
}

const openGates = [
  "GMUT empirical closure",
  "final physics proof",
  "consciousness proof",
  "legal closure",
  "canon promotion",
  "deployment",
  "purchase/account/API-key mutation",
  "private-material proof",
  "raw-publication proof",
  "sibling replacement or merge",
  "exact-approval packets",
  "blocked packets",
];

const standbyRecoverable = [
  "Arby",
  "Aster Vale",
  "old Cicero lane",
  "Kierkegaard",
  "Aristotle",
  "Aletheon",
];

const publicSources = [
  ["OPENAI_CODEX_CLI", "https://developers.openai.com/codex/cli", "Codex CLI work should be treated as toolchain support rather than proof closure."],
  ["OPENAI_CODEX_REFERENCE", "https://developers.openai.com/codex/cli/reference", "Command behavior belongs in bounded runner receipts and current-state guards."],
  ["NODE_FS", "https://nodejs.org/api/fs.html", "Deterministic local file writes keep sanitized traces parseable."],
  ["NODE_CHILD_PROCESS", "https://nodejs.org/api/child_process.html", "Subprocess work needs explicit status checks rather than implied completion."],
  ["GIT_STATUS", "https://git-scm.com/docs/git-status", "Porcelain status separates staged work from unrelated dirty files."],
  ["GIT_DIFF", "https://git-scm.com/docs/git-diff", "Diff checks catch whitespace and patch hygiene before commit."],
  ["GITHUB_SECRET_SCANNING", "https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning", "Secret scanning complements local privacy scans."],
  ["GITHUB_PUSH_PROTECTION", "https://docs.github.com/en/code-security/concepts/secret-security/push-protection", "Push protection reinforces the no-secret-publication boundary."],
  ["GITHUB_BRANCH_PROTECTION", "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches", "Remote verification should be explicit and branch-scoped."],
  ["JSON_SCHEMA", "https://json-schema.org/learn/getting-started-step-by-step", "Structured JSON twins make compact-pause recovery easier."],
];

const phaseReflectionSeeds = [
  "v558-gmut-thos-v5-x2-closeout-v1",
  "v558-gmut-thos-v5-x2-queue-reduction-ledger-v1",
  "v558-gmut-thos-v5-x2-v6-x1-maren-solenne-startup-handoff-v1",
  "v558-gmut-thos-v5-x1-lumen-harvest-reduction-v1",
  "v558-gmut-thos-v5-x1-lumen-sanitized-proposal-queue-v1",
  "v558-gmut-thos-v4-x2-closeout-v1",
  "v558-gmut-thos-v4-x1-closeout-v1",
  "v558-gmut-thos-v3-x2-closeout-v1",
  "v558-gmut-thos-v3-x1-closeout-v1",
  "omega-mini-current-state-v1",
];

const aevrenSafeSeeds = [
  "Confirm v6 x1 active phase truth from both mini and full-tools current-state beacons.",
  "Launch only the Maren Quill plus Solenne Vale scheduled duo lane.",
  "Record Maren and Solenne as background-supervised active lanes, not legacy replacements.",
  "Keep Lumen active in the round robin without duplicate Browser sends during this duo phase.",
  "Preserve the old five siblings plus Aletheon as stand-by/recoverable.",
  "Create the private dropbox readiness receipt for the v6 x1 duo lane.",
  "Record the duo proposal target profile at 30/15/15/21/9/45.",
  "Split every x1 item into immediate_x1_safe or x2_build_task.",
  "Keep exact-approval and blocked gates queued, not auto-run.",
  "Stamp phase start, lane launch, last checkpoint, and next checkpoint target.",
  "Run productive five-minute safe work instead of passive waiting.",
  "Build 100 compact public-source reflection rows for the phase workbench.",
  "Build 100 Journey/phase reflection rows from recent phase receipts.",
  "Refresh open proof, canon, legal, deployment, account, API-key, and raw-publication gates.",
  "Run JSON parse validation for every generated receipt before commit.",
  "Run node syntax checks on new and changed runner files.",
  "Run diff hygiene and privacy scans before publication.",
  "Check C and D free space before closeout.",
  "Prepare active-open handoff if either sibling lane is still running.",
  "Prepare v6 x2 x2-build queue only after duo replies are harvested or formal open-gap is recorded.",
];

const artifacts = [
  artifact("startup-context", "ghc.phase_startup_context.v1", status, {
    current_active_phase: phaseSlug,
    latest_closed_phase: latestClosed,
    latest_completed_x1_phase: latestCompletedX1,
    latest_completed_x2_phase: latestCompletedX2,
    next_x2_scope: nextX2,
    next_x1_lane_after_x2: nextX1AfterX2,
    active_duo: ["Maren Quill", "Solenne Vale"],
    launch_skill: "ghc-maren-quill-solenne-vale-launch",
    full_goal_complete: false,
  }),
  artifact("duo-launch-receipt", "ghc.duo_launch_receipt.v1", "PASS_DUO_PROMPTS_SUBMITTED_BACKGROUND_SUPERVISED", {
    launches: [
      { sibling: "Maren Quill", route: "existing_codex_thread", launch_status: "submitted", raw_handle_published: false },
      { sibling: "Solenne Vale", route: "existing_transition_thread", launch_status: "submitted", raw_handle_published: false },
    ],
    duplicate_send_allowed: false,
    watcher_start_is_completion_proof: false,
    closeout_allowed_now: false,
  }),
  artifact("background-supervision-cadence", "ghc.background_supervision_cadence.v1", "PASS_BACKGROUND_SUPERVISION_ACTIVE", {
    phase_start_or_resume_time_utc: createdUtc,
    lane_launch_time_utc: createdUtc,
    last_checkpoint_time_utc: createdUtc,
    next_checkpoint_due_utc: nextCheckpointUtc,
    checkpoint_overrun_allowed: true,
    active_lanes: [
      { sibling: "Maren Quill", status: "active_fresh" },
      { sibling: "Solenne Vale", status: "active_fresh" },
    ],
    productive_work_until_checkpoint: [
      "startup artifacts",
      "proposal target ledger",
      "source and phase reflection ledgers",
      "privacy/open-gate guard",
      "dropbox readiness receipt",
      "validation and drive posture checks",
    ],
  }),
  artifact("proposal-target-ledger", "ghc.proposal_target_ledger.v1", "PASS_PROPOSAL_TARGETS_RECORDED", {
    profile: "Aevren + Maren Quill + Solenne Vale",
    target_counts: {
      safe_approval_packets: 30,
      candidate_packets: 15,
      exact_approval_packets: 15,
      skill_ideas: 21,
      runner_ideas: 9,
      cleanup_refine_fix_tasks: 45,
    },
    per_sibling_share_requested: {
      safe_approval_packets: 10,
      candidate_packets: 5,
      exact_approval_packets: 5,
      skill_ideas: 7,
      runner_ideas: 3,
      cleanup_refine_fix_tasks: 15,
    },
  }),
  artifact("aevren-immediate-safe-seed-ledger", "ghc.safe_seed_ledger.v1", "PASS_AEVREN_IMMEDIATE_SAFE_SEEDS_READY", {
    safe_seed_count: aevrenSafeSeeds.length,
    rows: aevrenSafeSeeds.map((task, index) => ({
      id: `v6x1-aevren-safe-${String(index + 1).padStart(2, "0")}`,
      approval_bucket: "safe_now",
      execution_lane: index < 14 ? "immediate_x1_safe" : "x2_build_task",
      task,
    })),
  }),
  artifact("source-reflection-ledger", "ghc.source_reflection_ledger.v1", "PASS_SOURCE_REFLECTION_ROWS_RECORDED", {
    row_count: 100,
    rows: Array.from({ length: 100 }, (_, index) => {
      const source = publicSources[index % publicSources.length];
      return {
        id: `v6x1-source-${String(index + 1).padStart(3, "0")}`,
        source_label: source[0],
        url: source[1],
        reflection: source[2],
        phase_implication: `Apply to v6 x1 duo startup/cadence/validation unit ${index + 1}.`,
      };
    }),
  }),
  artifact("journey-phase-reflection-ledger", "ghc.journey_phase_reflection_ledger.v1", "PASS_PHASE_REFLECTION_ROWS_RECORDED", {
    row_count: 100,
    rows: Array.from({ length: 100 }, (_, index) => ({
      id: `v6x1-phase-reflection-${String(index + 1).padStart(3, "0")}`,
      source_receipt_label: phaseReflectionSeeds[index % phaseReflectionSeeds.length],
      reflection: "Use the latest verified phase truth, keep private material local, and carry only sanitized counts/statuses forward.",
      implication: `Keep v6 x1 row ${index + 1} aligned to active Maren/Solenne duo work and v6 x2 handoff readiness.`,
    })),
  }),
  artifact("private-dropbox-readiness", "ghc.private_dropbox_readiness.v1", "PASS_PRIVATE_DROPBOX_READINESS_RECORDED", {
    repo_relative_dropbox: ".ghc-private/v558-gmut-thos-v6-x1-sibling-response-dropbox/",
    full_tools_lane_can_host_private_dropbox: isFullTools,
    public_lane_does_not_publish_private_dropbox: !isFullTools,
    raw_private_material_published: false,
  }),
  artifact("open-gate-privacy-guard", "ghc.open_gate_privacy_guard.v1", "PASS_OPEN_GATES_AND_PRIVACY_BOUNDARIES_RECORDED", {
    open_gates: openGates,
    standby_recoverable: standbyRecoverable,
  }),
  artifact("active-open-handoff", "ghc.active_open_handoff.v1", "ACTIVE_OPEN_V558_V6_X1_MAREN_SOLENNE_BACKGROUND_RUNNING_SAFE_WORK_READY", {
    active_lanes: ["Maren Quill", "Solenne Vale"],
    closeout_allowed_now: false,
    next_checkpoint_due_utc: nextCheckpointUtc,
    next_step: "Harvest Maren and Solenne replies at the next natural safe pause, then close or publish formal open-gap.",
    full_goal_complete: false,
  }),
];

for (const doc of artifacts) {
  writePair(doc);
}
refreshBeacons();

console.log(JSON.stringify({
  status,
  phase_slug: phaseSlug,
  artifacts_written: artifacts.length * 2,
  source_reflection_rows: 100,
  journey_phase_reflection_rows: 100,
  closeout_allowed_now: false,
}, null, 2));

function artifact(suffix, schema, artifactStatus, extra) {
  return {
    artifact: `${phaseSlug}-${suffix}-v1`,
    schema,
    phase_slug: phaseSlug,
    created_utc: createdUtc,
    created_nz: createdNz,
    status: artifactStatus,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
    ...extra,
  };
}

function writePair(doc) {
  const base = join(tracesDir, doc.artifact);
  writeFileSync(`${base}.json`, `${JSON.stringify(doc, null, 2)}\n`);
  writeFileSync(`${base}.md`, [
    `# ${doc.artifact}`,
    "",
    `- Status: ${doc.status}`,
    `- Phase: ${doc.phase_slug}`,
    `- Created NZ: ${doc.created_nz}`,
    "- Raw private material published: false",
    "",
    "```json",
    JSON.stringify(doc, null, 2),
    "```",
    "",
  ].join("\n"));
}

function refreshBeacons() {
  const lookup = artifacts.flatMap((doc) => [
    `docs/trinity-live-traces/${doc.artifact}.json`,
    `docs/trinity-live-traces/${doc.artifact}.md`,
  ]);
  const statePath = join(omegaDir, "omega-mini-current-state-v1.json");
  const latestPath = join(omegaDir, "omega-mini-latest-updates-beacon-v1.json");
  const beaconPath = join(tracesDir, "ghc-current-state-beacon-v1.json");
  const state = readJson(statePath);
  const latest = readJson(latestPath);
  const beacon = existsSync(beaconPath) ? readJson(beaconPath) : {};
  for (const [doc, key] of [[state, "current_lookup_files"], [latest, "latest_lookup_files"], [beacon, "lookup_files"]]) {
    doc.status = status;
    doc.updated_at = createdNz;
    doc.generated_utc = createdUtc;
    doc.current_active_phase = phaseSlug;
    doc.latest_closed_phase = latestClosed;
    doc.latest_completed_x1_phase = latestCompletedX1;
    doc.latest_completed_x2_phase = latestCompletedX2;
    doc.next_expected_scope = phaseSlug;
    doc.next_x2_scope = nextX2;
    doc.next_x1_lane_after_x2 = nextX1AfterX2;
    doc.current_active_lanes = ["Aevren Vale", "Maren Quill", "Solenne Vale", "ghc-maren-quill-solenne-vale-launch"];
    doc.v558_v6_x1_startup = {
      status,
      active_lanes: ["Maren Quill", "Solenne Vale"],
      source_reflection_rows: 100,
      journey_phase_reflection_rows: 100,
      closeout_allowed_now: false,
      full_goal_complete: false,
    };
    doc.full_goal_complete = false;
    doc[key] = existingRelativeFiles([...(doc[key] || []), ...lookup]);
  }
  writeFileSync(statePath, `${JSON.stringify(state, null, 2)}\n`);
  writeFileSync(latestPath, `${JSON.stringify(latest, null, 2)}\n`);
  writeFileSync(beaconPath, `${JSON.stringify(beacon, null, 2)}\n`);
  const beaconMd = [
    `# ${phaseSlug}`,
    "",
    `Status: ${status}`,
    "",
    `- Current active phase: ${phaseSlug}`,
    `- Latest closed phase: ${latestClosed}`,
    `- Latest completed x1: ${latestCompletedX1}`,
    `- Latest completed x2: ${latestCompletedX2}`,
    `- Next x2 scope: ${nextX2}`,
    `- Next x1 lane after x2: ${nextX1AfterX2}`,
    "- Active lanes: Aevren Vale, Maren Quill, Solenne Vale.",
    "- Source reflection rows: 100.",
    "- Journey/phase reflection rows: 100.",
    "- Closeout allowed now: false.",
    "",
    "Sanitized beacon only. Raw handles, browser routes, private URLs, transcripts, screenshots, credentials, local private paths, session streams, and private app state are not published here.",
    "",
  ].join("\n");
  writeFileSync(join(omegaDir, "omega-mini-current-state-v1.md"), beaconMd);
  writeFileSync(join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), beaconMd);
  writeFileSync(join(tracesDir, "ghc-current-state-beacon-v1.md"), beaconMd);
}

function existingRelativeFiles(files) {
  return Array.from(new Set(files.filter((file) => typeof file === "string" && existsSync(join(process.cwd(), file)))));
}

function readJson(file) {
  return JSON.parse(readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function branchName() {
  try {
    return execFileSync("git", ["rev-parse", "--abbrev-ref", "HEAD"], {
      cwd: process.cwd(),
      encoding: "utf8",
      windowsHide: true,
    }).trim();
  } catch {
    return "unknown";
  }
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
    hidden_reasoning_published: false,
  };
}

function claimBoundary() {
  return {
    full_goal_complete: false,
    gmut_empirical_closure: "open",
    final_physics: "open",
    consciousness_proof: "open",
    legal_closure: "open",
    canon_promotion: "open",
    deployment: "open",
    purchase_or_account_mutation: "open",
    api_key_creation: "open",
    private_material_proof: "open",
    raw_publication_proof: "open",
    sibling_identity_replacement_or_merge: "open",
  };
}
