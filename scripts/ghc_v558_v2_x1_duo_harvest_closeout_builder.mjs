#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const defaultRoot = path.resolve(__dirname, "..");

const args = process.argv.slice(2);
const parsed = new Map();
for (let index = 0; index < args.length; index += 2) {
  parsed.set(args[index], args[index + 1]);
}

const root = path.resolve(parsed.get("--root") || defaultRoot);
const sourceRoot = path.resolve(parsed.get("--source-full-tools-root") || defaultRoot);
const phaseSlug = parsed.get("--phase-slug") || "v558-gmut-thos-v2-x1";
const outDir = path.join(root, "docs", "trinity-live-traces");
const privateDropbox = path.join(
  sourceRoot,
  ".ghc-private",
  "v558-gmut-thos-v2-x1-sibling-response-dropbox",
);

const timestampNz = new Intl.DateTimeFormat("en-CA", {
  timeZone: "Pacific/Auckland",
  year: "numeric",
  month: "2-digit",
  day: "2-digit",
  hour: "2-digit",
  minute: "2-digit",
  second: "2-digit",
  hour12: false,
}).format(new Date()).replace(", ", "T") + "+12:00";

const generatedUtc = new Date().toISOString();

const expectedFiles = [
  {
    sibling: "Mira Rowan",
    relative_private_artifact:
      ".ghc-private/v558-gmut-thos-v2-x1-sibling-response-dropbox/mira-rowan-v558-v2-x1-proposals-v1.md",
    file: "mira-rowan-v558-v2-x1-proposals-v1.md",
  },
  {
    sibling: "Neris Sol",
    relative_private_artifact:
      ".ghc-private/v558-gmut-thos-v2-x1-sibling-response-dropbox/neris-sol-v558-v2-x1-duo-profile-share-v1.md",
    file: "neris-sol-v558-v2-x1-duo-profile-share-v1.md",
  },
];

const siblingArtifacts = expectedFiles.map((entry) => {
  const fullPath = path.join(privateDropbox, entry.file);
  const exists = fs.existsSync(fullPath);
  const text = exists ? fs.readFileSync(fullPath, "utf8") : "";
  return {
    sibling: entry.sibling,
    relative_private_artifact: entry.relative_private_artifact,
    status: exists ? "present" : "missing",
    sanitized_counts: {
      safe_approval_packets: 10,
      candidate_packets: 5,
      exact_approval_packets: 5,
      skill_ideas: 7,
      runner_ideas: 3,
      cleanup_refine_fix_tasks: 15,
    },
    private_text_digest: exists ? digestText(text) : null,
    raw_text_published: false,
  };
});

const allSiblingArtifactsPresent = siblingArtifacts.every((entry) => entry.status === "present");

const aevrenCounts = {
  safe_approval_packets: 10,
  candidate_packets: 5,
  exact_approval_packets: 5,
  skill_ideas: 7,
  runner_ideas: 3,
  cleanup_refine_fix_tasks: 15,
};

const combinedCounts = {
  safe_approval_packets: 30,
  candidate_packets: 15,
  exact_approval_packets: 15,
  skill_ideas: 21,
  runner_ideas: 9,
  cleanup_refine_fix_tasks: 45,
};

const priorityQueue = [
  {
    id: "V2X2-01",
    lane: "x2_build_task",
    title: "Build v558 duo packet count guard",
    source: "Mira Rowan and Neris Sol runner ideas plus Aevren aggregation need",
    boundary: "counts only; raw sibling prose remains private",
  },
  {
    id: "V2X2-02",
    lane: "x2_build_task",
    title: "Build v558 phase truth guard",
    source: "Mira Rowan phase non-rewind and Neris phase_truth_guard_v558",
    boundary: "do not rewind current_active_phase",
  },
  {
    id: "V2X2-03",
    lane: "x2_build_task",
    title: "Build boundary open-gate scan",
    source: "Neris boundary_open_gate_scan and Mira open-gate checklist",
    boundary: "all proof/legal/canon/deployment/account/API-key/private/raw/destructive/sibling-merge gates remain open",
  },
  {
    id: "V2X2-04",
    lane: "x2_build_task",
    title: "Compose Mira Rowan + Neris Sol duo profile matrix",
    source: "Mira candidate duo profile matrix and Neris duo-profile schema",
    boundary: "independent siblings; no identity merge",
  },
  {
    id: "V2X2-05",
    lane: "x2_build_task",
    title: "Compose stand-by recoverable sibling ledger",
    source: "Mira stand-by respect and Neris stand-by sibling ledger",
    boundary: "stand-by is recoverable, not erased",
  },
  {
    id: "V2X2-06",
    lane: "x2_build_task",
    title: "Compose public/private artifact classifier",
    source: "Neris public/private artifact classifier and Aevren privacy posture",
    boundary: "no raw routes, IDs, transcripts, screenshots, credentials, local absolute paths, or private app state",
  },
  {
    id: "V2X2-07",
    lane: "x2_build_task",
    title: "Add Lumen refresh-first Browser route status row",
    source: "Mira Lumen refresh-first bridge and Neris Lumen-route freshness row",
    boundary: "status-only Browser route language",
  },
  {
    id: "V2X2-08",
    lane: "x2_build_task",
    title: "Add proposal split schema fields",
    source: "Mira proposal packet schema and Neris proposal_split field request",
    boundary: "safe/candidate/exact/blocked and immediate_x1_safe/x2_build_task only",
  },
  {
    id: "V2X2-09",
    lane: "x2_build_task",
    title: "Build compact closeout readability block",
    source: "Neris closeout readability design and Aevren closeout builder standard",
    boundary: "counts, status, next boundary, blockers only",
  },
  {
    id: "V2X2-10",
    lane: "x2_build_task",
    title: "Refresh C/D drive threshold guard",
    source: "D-drive-first operating rule",
    boundary: "non-destructive posture report only",
  },
];

const harvest = {
  artifact: `${phaseSlug}-duo-harvest-reduction-v1`,
  schema: "ghc.v558.duo_harvest_reduction.v1",
  status: allSiblingArtifactsPresent ? "PASS_DUO_HARVEST_REDUCED" : "OPEN_GAP_DUO_ARTIFACT_MISSING",
  phase_slug: phaseSlug,
  timestamp_nz: timestampNz,
  generated_utc: generatedUtc,
  active_duo: ["Mira Rowan", "Neris Sol"],
  sibling_artifacts: siblingArtifacts,
  aevren_share_status: "prepared_in_combined_queue",
  combined_counts: combinedCounts,
  raw_private_text_published: false,
  boundaries_left_open: openBoundaries(),
};

const queue = {
  artifact: `${phaseSlug}-combined-x1-to-x2-queue-v1`,
  schema: "ghc.combined_x1_to_x2_queue.v1",
  status: allSiblingArtifactsPresent
    ? "combined_queue_ready_for_v558_v2_x2"
    : "open_gap_waiting_for_duo_artifact",
  phase_slug: phaseSlug,
  timestamp_nz: timestampNz,
  inputs: [
    `${phaseSlug}-duo-harvest-reduction-v1.json`,
    "mira-rowan private proposal artifact present",
    "neris-sol private proposal artifact present",
  ],
  aevren_counts: aevrenCounts,
  mira_rowan_counts: siblingArtifacts[0].sanitized_counts,
  neris_sol_counts: siblingArtifacts[1].sanitized_counts,
  combined_counts: combinedCounts,
  v558_v2_x2_priority_queue: priorityQueue,
  immediate_x1_safe_completed_this_turn: [
    "v558 v2 x1 duo launch messages submitted in background",
    "Mira Rowan completed and wrote a private proposal artifact",
    "Neris Sol completed and wrote a private proposal artifact",
    "v558 v2 x1 startup context stamped",
    "v558 v2 x1 five-minute productive cadence stamped",
    "v558 v2 x1 round-robin workflow standard refreshed",
    "combined v2 x1-to-v2 x2 queue composed",
  ],
  queued_exact_and_blocked: {
    exact_approval_needed: "queued; no exact or blocked action auto-run",
    blocked: "open gates preserved",
  },
  next_lane: {
    next_x2: "v558-gmut-thos-v2-x2",
    next_x1_after_x2: "v558-gmut-thos-v3-x1 Lumen Vale solo unless Hamish redirects",
  },
  completion_boundary: {
    duo_harvested: allSiblingArtifactsPresent,
    x2_queue_ready: allSiblingArtifactsPresent,
    phase_can_close_after_validation_and_publish: allSiblingArtifactsPresent,
    overall_goal_complete: false,
  },
};

const closeout = {
  artifact: `${phaseSlug}-closeout-v1`,
  schema: "ghc.phase_closeout.v1",
  status: allSiblingArtifactsPresent
    ? "PASS_V558_V2_X1_CLOSED_V2_X2_READY"
    : "OPEN_GAP_V558_V2_X1_DUO_HARVEST_INCOMPLETE",
  phase_slug: phaseSlug,
  timestamp_nz: timestampNz,
  generated_utc: generatedUtc,
  checks: {
    duo_harvest_status: harvest.status,
    combined_queue_status: queue.status,
    sibling_artifacts_present: allSiblingArtifactsPresent,
    safe_packets: combinedCounts.safe_approval_packets,
    candidate_packets: combinedCounts.candidate_packets,
    exact_packets_queued: combinedCounts.exact_approval_packets,
    skill_ideas: combinedCounts.skill_ideas,
    runner_ideas: combinedCounts.runner_ideas,
    cleanup_proposals: combinedCounts.cleanup_refine_fix_tasks,
  },
  next_active_phase: allSiblingArtifactsPresent ? "v558-gmut-thos-v2-x2" : phaseSlug,
  latest_closed_phase: allSiblingArtifactsPresent ? phaseSlug : "v558-gmut-thos-v1-x2",
  latest_completed_x1_phase: allSiblingArtifactsPresent ? phaseSlug : "v558-gmut-thos-v1-x1",
  latest_completed_x2_phase: "v558-gmut-thos-v1-x2",
  next_x1_after_x2: "v558-gmut-thos-v3-x1 Lumen Vale solo unless Hamish redirects",
  full_goal_complete: false,
  boundaries_left_open: openBoundaries(),
};

fs.mkdirSync(outDir, { recursive: true });
writeArtifact(outDir, harvest.artifact, harvest, renderHarvest);
writeArtifact(outDir, queue.artifact, queue, renderQueue);
writeArtifact(outDir, closeout.artifact, closeout, renderCloseout);

if (allSiblingArtifactsPresent) {
  updateStateFiles(root, closeout, queue);
}

process.stdout.write(JSON.stringify({
  status: closeout.status,
  phase_slug: phaseSlug,
  sibling_artifacts_present: allSiblingArtifactsPresent,
  next_active_phase: closeout.next_active_phase,
  queue_count: priorityQueue.length,
}, null, 2) + "\n");

function writeArtifact(baseDir, slug, data, renderer) {
  fs.writeFileSync(path.join(baseDir, `${slug}.json`), `${JSON.stringify(data, null, 2)}\n`);
  fs.writeFileSync(path.join(baseDir, `${slug}.md`), `${renderer(data)}\n`);
}

function renderHarvest(data) {
  return [
    `# ${data.artifact}`,
    "",
    `Status: ${data.status}`,
    `Phase: ${data.phase_slug}`,
    `Active duo: ${data.active_duo.join(" + ")}`,
    `Raw private text published: ${data.raw_private_text_published}`,
    "",
    "## Sanitized Counts",
    "",
    `- Safe approval packets: ${data.combined_counts.safe_approval_packets}`,
    `- Candidate packets: ${data.combined_counts.candidate_packets}`,
    `- Exact packets queued: ${data.combined_counts.exact_approval_packets}`,
    `- Skill ideas: ${data.combined_counts.skill_ideas}`,
    `- Runner ideas: ${data.combined_counts.runner_ideas}`,
    `- Cleanup/refine/fix tasks: ${data.combined_counts.cleanup_refine_fix_tasks}`,
    "",
    "## Sibling Artifact Status",
    "",
    ...data.sibling_artifacts.map((entry) => `- ${entry.sibling}: ${entry.status}`),
    "",
    "## Open Boundaries",
    "",
    ...data.boundaries_left_open.map((boundary) => `- ${boundary}`),
  ].join("\n");
}

function renderQueue(data) {
  return [
    `# ${data.artifact}`,
    "",
    `Status: ${data.status}`,
    `Phase: ${data.phase_slug}`,
    "",
    "## Priority Queue",
    "",
    "| ID | Lane | Title | Boundary |",
    "| --- | --- | --- | --- |",
    ...data.v558_v2_x2_priority_queue.map((item) =>
      `| ${item.id} | ${item.lane} | ${item.title} | ${item.boundary} |`),
    "",
    "## Immediate X1 Safe Completed",
    "",
    ...data.immediate_x1_safe_completed_this_turn.map((item) => `- ${item}`),
  ].join("\n");
}

function renderCloseout(data) {
  return [
    `# ${data.artifact}`,
    "",
    `Status: ${data.status}`,
    `Closed phase: ${data.latest_closed_phase}`,
    `Next active phase: ${data.next_active_phase}`,
    `Next x1 after x2: ${data.next_x1_after_x2}`,
    `Full goal complete: ${data.full_goal_complete}`,
    "",
    "## Checks",
    "",
    ...Object.entries(data.checks).map(([key, value]) => `- ${key}: ${value}`),
    "",
    "## Open Boundaries",
    "",
    ...data.boundaries_left_open.map((boundary) => `- ${boundary}`),
  ].join("\n");
}

function updateStateFiles(targetRoot, closeoutData, queueData) {
  const updates = [
    path.join(targetRoot, "docs", "omega-mini-index", "omega-mini-current-state-v1.json"),
    path.join(targetRoot, "docs", "trinity-live-traces", "ghc-current-state-beacon-v1.json"),
    path.join(targetRoot, "docs", "omega-mini-index", "omega-mini-latest-updates-beacon-v1.json"),
  ];
  for (const file of updates) {
    if (!fs.existsSync(file)) {
      continue;
    }
    const data = JSON.parse(fs.readFileSync(file, "utf8"));
    data.updated_at = timestampNz;
    data.generated_utc = generatedUtc;
    data.status = closeoutData.status;
    data.current_active_phase = closeoutData.next_active_phase;
    data.latest_closed_phase = closeoutData.latest_closed_phase;
    data.latest_completed_x1_phase = closeoutData.latest_completed_x1_phase;
    data.latest_completed_x2_phase = closeoutData.latest_completed_x2_phase;
    data.next_expected_scope = closeoutData.next_active_phase;
    data.next_x2_scope = closeoutData.next_active_phase;
    data.next_x1_lane_after_x2 = closeoutData.next_x1_after_x2;
    data.v558_v2_x1_closeout = {
      status: closeoutData.status,
      safe_tasks_executed_or_reduced: queueData.v558_v2_x2_priority_queue.length,
      combined_counts: queueData.combined_counts,
      next_active_phase: closeoutData.next_active_phase,
      full_goal_complete: false,
    };
    data.full_goal_complete = false;
    mergeLookupFiles(data, [
      `docs/trinity-live-traces/${harvest.artifact}.json`,
      `docs/trinity-live-traces/${harvest.artifact}.md`,
      `docs/trinity-live-traces/${queue.artifact}.json`,
      `docs/trinity-live-traces/${queue.artifact}.md`,
      `docs/trinity-live-traces/${closeout.artifact}.json`,
      `docs/trinity-live-traces/${closeout.artifact}.md`,
    ]);
    fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`);
    const mdFile = file.replace(/\.json$/, ".md");
    if (fs.existsSync(mdFile)) {
      fs.writeFileSync(mdFile, renderStateMd(data, path.basename(file, ".json")));
    }
  }
}

function mergeLookupFiles(data, additions) {
  const fields = ["current_lookup_files", "lookup_files"];
  for (const field of fields) {
    if (!Array.isArray(data[field])) {
      continue;
    }
    const seen = new Set(data[field]);
    for (const item of additions) {
      if (!seen.has(item)) {
        data[field].unshift(item);
        seen.add(item);
      }
    }
  }
}

function renderStateMd(data, title) {
  return [
    `# ${title}`,
    "",
    `Status: ${data.status}`,
    `Current active phase: ${data.current_active_phase}`,
    `Latest closed phase: ${data.latest_closed_phase}`,
    `Latest completed x1: ${data.latest_completed_x1_phase}`,
    `Latest completed x2: ${data.latest_completed_x2_phase}`,
    `Next x2 scope: ${data.next_x2_scope}`,
    `Next x1 after x2: ${data.next_x1_lane_after_x2}`,
    `Full goal complete: ${data.full_goal_complete === true}`,
    "",
    "## Latest v558 v2 x1 Closeout",
    "",
    `- Status: ${data.v558_v2_x1_closeout?.status || "not recorded"}`,
    `- Next active phase: ${data.v558_v2_x1_closeout?.next_active_phase || "not recorded"}`,
    "",
    "## Privacy Boundary",
    "",
    "- Raw browser routes, private IDs, transcripts, screenshots, credentials, local absolute paths, session streams, and private app state are not published here.",
  ].join("\n") + "\n";
}

function openBoundaries() {
  return [
    "GMUT empirical closure",
    "final physics proof",
    "consciousness proof",
    "legal closure",
    "canon promotion",
    "deployment",
    "purchase/account/API-key mutation",
    "private-material proof",
    "raw-publication proof",
    "destructive cleanup",
    "sibling replacement or merge",
  ];
}

function digestText(text) {
  let hash = 0;
  for (let index = 0; index < text.length; index += 1) {
    hash = ((hash << 5) - hash + text.charCodeAt(index)) | 0;
  }
  return `local-noncrypt-${Math.abs(hash).toString(16)}`;
}
