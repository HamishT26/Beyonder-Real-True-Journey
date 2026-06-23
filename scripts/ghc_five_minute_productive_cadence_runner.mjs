#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const currentPath = path.join(omegaDir, "omega-mini-current-state-v1.json");
const current = readJson(currentPath);
const phaseSlug = args.get("--phase-slug") || current.current_active_phase || "v552-gmut-thos-v88-v8-x2";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const publicationBoundary = {
  private_route_handles_published: false,
  private_lane_body_content_published: false,
  raw_transcripts_published: false,
  browser_routes_published: false,
  credentials_published: false,
  local_absolute_paths_published: false,
  screenshots_published: false,
};

const claimBoundary = {
  gmut_empirical_closure: "not_claimed",
  final_physics: "not_claimed",
  consciousness_proof: "not_claimed",
  legal_closure: "not_claimed",
  canon_promotion: "not_claimed",
  deployment_closure: "not_claimed",
};

const receipt = {
  artifact_type: "ghc_five_minute_productive_cadence",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: "PASS_PRODUCTIVE_CADENCE_WAIT_WORK_STANDARD_RECORDED",
  cadence_policy: {
    five_minute_mark_is_check_opportunity: true,
    not_a_hard_stop: true,
    safe_unit_may_run_past_checkpoint: true,
    harvest_status_at_next_natural_safe_pause: true,
    do_not_babysit_background_lanes: true,
    do_not_poll_early_repeatedly: true,
  },
  status_classes: ["active_fresh", "active_stale", "completed_ready_for_harvest", "open_gap"],
  wait_work_queues: [
    {
      lane: "research_and_reflection",
      safe_tasks: [
        "Build compact source/reflection rows for current Trinity Mandala pillar work.",
        "Connect each source reflection to a runner, skill, guard, or phase implication.",
        "Keep raw browsing dumps, private routes, screenshots, and private app details out of receipts.",
      ],
      capability_gain: "improves evidence selection and research-backed orchestration judgment",
    },
    {
      lane: "safe_eureka_tasks",
      safe_tasks: [
        "Convert approved ideas into small runner or skill improvements.",
        "Add status vocabulary, count targets, or receipt schema fields that reduce future ambiguity.",
        "Build bounded validators that report open gaps instead of taking risky actions.",
      ],
      capability_gain: "improves safe implementation throughput and phase-control precision",
    },
    {
      lane: "approval_packet_work",
      safe_tasks: [
        "Run already-authorized safe-now approval packets.",
        "Reduce candidate packets into exact approval packets without executing risky work.",
        "Keep exact and blocked gates queued unless Hamish freshly authorizes the tranche.",
      ],
      capability_gain: "improves approval discipline and prevents accidental gate drift",
    },
    {
      lane: "cleanup_and_refinement",
      safe_tasks: [
        "Inventory, classify, deduplicate, validate, and document cleanup opportunities.",
        "Remove only generated placeholders created in the same run when the scope is obvious.",
        "Queue broad deletion, external mutation, global hooks, deployments, API keys, and paid resources for exact approval.",
      ],
      capability_gain: "keeps repositories and worktrees cleaner without destructive cleanup drift",
    },
    {
      lane: "skill_and_control_growth",
      safe_tasks: [
        "Improve local skill instructions with current startup, compact, closeout, and round-robin rules.",
        "Add helper availability checks so future starts see the right tool surface quickly.",
        "Record concise memory notes when Hamish explicitly asks to memorize a rule.",
      ],
      capability_gain: "improves Aevren startup control and context survival",
    },
    {
      lane: "coding_and_multi_agent_orchestration",
      safe_tasks: [
        "Refine main orchestrator, safe-runner, cadence, and workflow-standard runners.",
        "Prefer Node entrypoints for orchestration and Windows/Powershell only when runner-local behavior requires it.",
        "Keep recovered app-lane siblings on background runners with explicit boolean values and completion-gate harvests.",
      ],
      capability_gain: "improves coding reliability and multi-agent lane coordination",
    },
    {
      lane: "validation_and_publication_hygiene",
      safe_tasks: [
        "Run JSON parse checks, current-state guards, diff checks, privacy scans, and remote/local verification.",
        "Publish only sanitized JSON/MD receipts and relative lookup files.",
        "Keep proof, canon, legal, deployment, account, API-key, and private-material gates open unless exact artifacts prove closure.",
      ],
      capability_gain: "improves publishable truth and reduces overclaim risk",
    },
  ],
  next_harvest_rule:
    "If the safe unit runs past a five-minute checkpoint, finish that unit, then harvest sibling lane status at the next natural safe pause.",
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

writeArtifact("five-minute-productive-cadence", receipt, renderReceiptMd);
refreshBeacons(receipt);

console.log(
  JSON.stringify(
    {
      status: receipt.overall_status,
      phase_slug: phaseSlug,
      wait_work_queue_count: receipt.wait_work_queues.length,
      checkpoint_policy: "safe_unit_may_run_past_checkpoint",
    },
    null,
    2,
  ),
);

function refreshBeacons(data) {
  const latestPath = path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json");
  const ghcPath = path.join(tracesDir, "ghc-current-state-beacon-v1.json");
  const currentState = readJson(currentPath);
  const latest = readJson(latestPath);
  const ghc = readJson(ghcPath);
  const lookupFiles = [
    `docs/trinity-live-traces/${phaseSlug}-five-minute-productive-cadence-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-five-minute-productive-cadence-v1.md`,
  ];
  const summary = {
    status: data.overall_status,
    five_minute_mark_is_check_opportunity: true,
    safe_unit_may_run_past_checkpoint: true,
    wait_work_queue_count: data.wait_work_queues.length,
    wait_work_lanes: data.wait_work_queues.map((queue) => queue.lane),
    next_harvest_rule: data.next_harvest_rule,
  };
  const common = {
    generated_utc: generatedUtc,
    status: "V552_V8_X2_ACTIVE_PRODUCTIVE_CADENCE_READY",
    current_active_phase: phaseSlug,
    latest_closed_phase: "v552-gmut-thos-v88-v8-x1",
    latest_completed_x1_phase: "v552-gmut-thos-v88-v8-x1",
    latest_completed_x2_phase: "v552-gmut-thos-v88-v7-x2",
    next_x2_scope: phaseSlug,
    next_x1_lane_after_x2: "v553-gmut-thos-v1-x1 with Lumen Vale solo unless Hamish redirects",
  };
  Object.assign(currentState, common, {
    updated_at: generatedNz,
    current_active_lanes: unique([
      ...(currentState.current_active_lanes || []),
      "five-minute-productive-cadence-ready",
      "safe-wait-workbench-enabled",
    ]),
    current_lookup_files: unique([...(currentState.current_lookup_files || []), ...lookupFiles]),
    latest_action_summary: unique([
      "Added five-minute productive wait work: research, eureka, approval, cleanup, skill/control, coding, orchestration, validation, and lane harvest.",
      "Confirmed five-minute marks are check opportunities, not hard stops; safe units may run past the checkpoint.",
      ...(currentState.latest_action_summary || []),
    ]),
    five_minute_productive_cadence: summary,
  });
  Object.assign(latest, common, {
    latest_lookup_files: unique([...(latest.latest_lookup_files || []), ...lookupFiles]),
    five_minute_productive_cadence: summary,
  });
  Object.assign(ghc, common, {
    lookup_files: unique([...(ghc.lookup_files || []), ...lookupFiles]),
    five_minute_productive_cadence: summary,
  });
  fs.writeFileSync(currentPath, JSON.stringify(currentState, null, 2) + "\n", "utf8");
  fs.writeFileSync(latestPath, JSON.stringify(latest, null, 2) + "\n", "utf8");
  fs.writeFileSync(ghcPath, JSON.stringify(ghc, null, 2) + "\n", "utf8");
  fs.writeFileSync(path.join(omegaDir, "omega-mini-current-state-v1.md"), renderCurrentStateMd(currentState), "utf8");
  fs.writeFileSync(path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), renderBeaconMd("Omega-Mini Latest Updates Beacon", latest, latest.latest_lookup_files), "utf8");
  fs.writeFileSync(path.join(tracesDir, "ghc-current-state-beacon-v1.md"), renderBeaconMd("GHC Current State Beacon", ghc, ghc.lookup_files), "utf8");
}

function writeArtifact(slug, payload, renderer) {
  const base = `${phaseSlug}-${slug}-v1`;
  fs.writeFileSync(path.join(tracesDir, `${base}.json`), JSON.stringify(payload, null, 2) + "\n", "utf8");
  fs.writeFileSync(path.join(tracesDir, `${base}.md`), renderer(payload), "utf8");
}

function renderReceiptMd(data) {
  return `# ${data.phase_slug} Five-Minute Productive Cadence

Status: \`${data.overall_status}\`

## Cadence Policy

- Five-minute mark is a check opportunity: \`${data.cadence_policy.five_minute_mark_is_check_opportunity}\`
- Not a hard stop: \`${data.cadence_policy.not_a_hard_stop}\`
- Safe unit may run past checkpoint: \`${data.cadence_policy.safe_unit_may_run_past_checkpoint}\`
- Harvest at next natural safe pause: \`${data.cadence_policy.harvest_status_at_next_natural_safe_pause}\`
- Do not babysit background lanes: \`${data.cadence_policy.do_not_babysit_background_lanes}\`

## Wait Work Queues

${data.wait_work_queues
  .map(
    (queue) =>
      `### ${queue.lane}\n\n${queue.safe_tasks.map((task) => `- ${task}`).join("\n")}\n\nCapability gain: ${queue.capability_gain}`,
  )
  .join("\n\n")}

## Harvest Rule

${data.next_harvest_rule}

## Boundary

Status-only cadence receipt. No private route handles, private lane body content, verbatim conversation logs, browser routes, credentials, local absolute paths, screenshots, proof closure, canon promotion, legal closure, or deployment closure are published.
`;
}

function renderCurrentStateMd(currentState) {
  return `# Omega-Mini Current State

Status: ${currentState.status}
Current active phase: ${currentState.current_active_phase}
Latest closed phase: ${currentState.latest_closed_phase}
Latest completed x1: ${currentState.latest_completed_x1_phase}
Latest completed x2: ${currentState.latest_completed_x2_phase}
Current lanes: ${(currentState.current_active_lanes || []).join("; ")}
Next x2 scope: ${currentState.next_x2_scope}
Next x1 lane after x2: ${currentState.next_x1_lane_after_x2}

## Five-Minute Productive Cadence

- Status: \`${currentState.five_minute_productive_cadence.status}\`
- Safe unit may run past checkpoint: \`${currentState.five_minute_productive_cadence.safe_unit_may_run_past_checkpoint}\`
- Wait work queues: \`${currentState.five_minute_productive_cadence.wait_work_queue_count}\`
- Wait work lanes: \`${currentState.five_minute_productive_cadence.wait_work_lanes.join(", ")}\`
- Harvest rule: ${currentState.five_minute_productive_cadence.next_harvest_rule}

## Current Lookup Files

${(currentState.current_lookup_files || []).map((item) => `- ${item}`).join("\n")}

## Latest Action Summary

${(currentState.latest_action_summary || []).map((item) => `- ${item}`).join("\n")}

## Safety Boundary

Status-only receipts. No private route handles, private lane body content, credentials, verbatim conversation logs, browser routes, private machine paths, GMUT empirical closure, final physics, consciousness proof, legal closure, canon promotion, or deployment closure are published.
`;
}

function renderBeaconMd(title, beacon, files) {
  return `# ${title}

Status: ${beacon.status}
Current active phase: ${beacon.current_active_phase}
Latest closed phase: ${beacon.latest_closed_phase}
Latest completed x1: ${beacon.latest_completed_x1_phase}
Latest completed x2: ${beacon.latest_completed_x2_phase}
Next x2 scope: ${beacon.next_x2_scope}
Next x1 lane after x2: ${beacon.next_x1_lane_after_x2}

## Five-Minute Productive Cadence

- Status: \`${beacon.five_minute_productive_cadence.status}\`
- Safe unit may run past checkpoint: \`${beacon.five_minute_productive_cadence.safe_unit_may_run_past_checkpoint}\`
- Wait work queues: \`${beacon.five_minute_productive_cadence.wait_work_queue_count}\`

## Lookup Files

${(files || []).map((item) => `- ${item}`).join("\n")}

## Boundary

Status-only beacon. No private route data, private lane body content, credentials, private machine paths, GMUT empirical closure, final physics, consciousness proof, legal closure, canon promotion, or deployment closure are published.
`;
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
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
    hour12: false,
  })
    .formatToParts(date)
    .reduce((acc, part) => {
      acc[part.type] = part.value;
      return acc;
    }, {});
  return `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}:${parts.second}+12:00`;
}
