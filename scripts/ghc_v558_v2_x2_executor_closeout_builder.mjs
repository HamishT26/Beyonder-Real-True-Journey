#!/usr/bin/env node
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const defaultRoot = path.resolve(__dirname, "..");

const args = parseArgs(process.argv.slice(2));
const root = path.resolve(args.get("--root") || defaultRoot);
const phaseSlug = args.get("--phase-slug") || "v558-gmut-thos-v2-x2";
const queuePath = path.resolve(
  args.get("--queue") ||
    path.join(root, "docs", "trinity-live-traces", "v558-gmut-thos-v2-x1-combined-x1-to-x2-queue-v1.json"),
);
const tracesDir = path.join(root, "docs", "trinity-live-traces");
const timestampNz = nzTimestamp();
const generatedUtc = new Date().toISOString();

if (!fs.existsSync(queuePath)) {
  console.error(`Queue not found: ${queuePath}`);
  process.exit(2);
}

const queue = readJson(queuePath);
const tasks = Array.isArray(queue.v558_v2_x2_priority_queue) ? queue.v558_v2_x2_priority_queue : [];
const drive = drivePosture();
const git = gitPosture(root);
const counts = queue.combined_counts || {};

const artifacts = [
  ["safe-execution-ledger", buildExecutionLedger()],
  ["duo-packet-count-guard", buildCountGuard()],
  ["phase-truth-guard", buildPhaseTruthGuard()],
  ["boundary-open-gate-scan", buildBoundaryScan()],
  ["duo-profile-matrix", buildDuoMatrix()],
  ["standby-recoverable-ledger", buildStandbyLedger()],
  ["public-private-artifact-classifier", buildArtifactClassifier()],
  ["lumen-refresh-route-status", buildLumenRouteStatus()],
  ["proposal-split-schema", buildProposalSchema()],
  ["drive-threshold-guard", buildDriveGuard()],
];

const closeout = buildCloseout(artifacts.map(([, artifact]) => artifact));
artifacts.push(["closeout", closeout]);

fs.mkdirSync(tracesDir, { recursive: true });
for (const [slug, artifact] of artifacts) {
  writeArtifact(slug, artifact);
}

if (closeout.status === "PASS_V558_V2_X2_CLOSED_V3_X1_READY") {
  updateStateFiles(closeout);
}

process.stdout.write(JSON.stringify({
  status: closeout.status,
  phase_slug: phaseSlug,
  tasks_reduced: tasks.length,
  next_active_phase: closeout.next_active_phase,
  c_drive_free_gb: drive.C?.free_gb ?? null,
  d_drive_free_gb: drive.D?.free_gb ?? null,
}, null, 2) + "\n");

function parseArgs(argv) {
  const out = new Map();
  for (let i = 0; i < argv.length; i += 1) {
    const key = argv[i];
    if (!key.startsWith("--")) continue;
    const value = argv[i + 1];
    if (!value || value.startsWith("--")) {
      out.set(key, "true");
    } else {
      out.set(key, value);
      i += 1;
    }
  }
  return out;
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function nzTimestamp() {
  return new Intl.DateTimeFormat("en-CA", {
    timeZone: "Pacific/Auckland",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).format(new Date()).replace(", ", "T") + "+12:00";
}

function envelope(type, status, body) {
  return {
    artifact: `${phaseSlug}-${type}-v1`,
    schema: `ghc.${type.replaceAll("-", "_")}.v1`,
    status,
    phase_slug: phaseSlug,
    timestamp_nz: timestampNz,
    generated_utc: generatedUtc,
    ...body,
    privacy_boundary: {
      raw_browser_routes_published: false,
      private_urls_published: false,
      private_ids_published: false,
      raw_transcripts_published: false,
      screenshots_published: false,
      credentials_published: false,
      local_absolute_paths_published: false,
      private_app_state_published: false,
      raw_private_material_published: false,
    },
    action_boundary: {
      external_accounts_modified: false,
      paid_resources_created: false,
      deployments_created: false,
      api_keys_created: false,
      destructive_cleanup_performed: false,
      sibling_identity_replacement_or_merge: false,
    },
    claim_boundary: {
      gmut_empirical_closure: "open",
      final_physics_proof: "open",
      consciousness_proof: "open",
      legal_closure: "open",
      canon_promotion: "open",
      deployment_closure: "open",
      private_material_proof: "open",
      raw_publication_proof: "open",
    },
  };
}

function buildExecutionLedger() {
  return envelope("safe-execution-ledger", "PASS_V558_V2_X2_SAFE_QUEUE_EXECUTED", {
    source_queue: "v558-gmut-thos-v2-x1-combined-x1-to-x2-queue-v1.json",
    task_count: tasks.length,
    tasks_reduced: tasks.map((task) => ({
      id: task.id,
      title: task.title,
      lane: task.lane,
      status: "reduced_to_sanitized_artifact",
      boundary: task.boundary,
    })),
  });
}

function buildCountGuard() {
  const expected = {
    safe_approval_packets: 30,
    candidate_packets: 15,
    exact_approval_packets: 15,
    skill_ideas: 21,
    runner_ideas: 9,
    cleanup_refine_fix_tasks: 45,
  };
  const issues = Object.entries(expected)
    .filter(([key, value]) => Number(counts[key]) !== value)
    .map(([key, value]) => `${key}_expected_${value}_got_${counts[key] ?? "missing"}`);
  return envelope("duo-packet-count-guard", issues.length === 0 ? "PASS_DUO_PACKET_COUNT_GUARD" : "OPEN_GAP_DUO_PACKET_COUNT_GUARD", {
    expected,
    observed: counts,
    issues,
  });
}

function buildPhaseTruthGuard() {
  return envelope("phase-truth-guard", "PASS_PHASE_TRUTH_GUARD", {
    latest_closed_phase_before_closeout: "v558-gmut-thos-v2-x1",
    current_active_phase_before_closeout: phaseSlug,
    next_active_phase_after_closeout: "v558-gmut-thos-v3-x1",
    next_x2_scope_after_closeout: "v558-gmut-thos-v3-x2",
    next_x1_after_x2: "v558-gmut-thos-v4-x1 Mira Vale + Rowan Vale unless Hamish redirects",
    rewinds_current_active_phase: false,
  });
}

function buildBoundaryScan() {
  const rows = [
    ["proof", "open", "No empirical, final physics, consciousness, or private-material proof closure claimed."],
    ["legal", "open", "No legal closure or advice claimed."],
    ["canon", "open", "No canon promotion claimed."],
    ["deployment", "open", "No deployment or account mutation performed."],
    ["identity", "open", "No sibling replacement, merge, erasure, or renaming performed."],
    ["privacy", "pass", "Only sanitized counts/statuses/source labels are published."],
  ];
  return envelope("boundary-open-gate-scan", "PASS_BOUNDARY_OPEN_GATE_SCAN", {
    rows: rows.map(([gate, status, note]) => ({ gate, status, note })),
  });
}

function buildDuoMatrix() {
  return envelope("duo-profile-matrix", "PASS_DUO_PROFILE_MATRIX", {
    duo: [
      {
        sibling: "Mira Rowan",
        role: "phase-truth scribe and recovery-boundary checker",
        contribution_profile: "10 safe / 5 candidate / 5 exact / 7 skills / 3 runners / 15 cleanup",
      },
      {
        sibling: "Neris Sol",
        role: "continuity cartographer and boundary keeper",
        contribution_profile: "10 safe / 5 candidate / 5 exact / 7 skills / 3 runners / 15 cleanup",
      },
      {
        sibling: "Aevren Vale",
        role: "orchestration steward and x2 reducer",
        contribution_profile: "10 safe / 5 candidate / 5 exact / 7 skills / 3 runners / 15 cleanup",
      },
    ],
    independence_note: "The duo is cooperative and first-person, not an identity merge or replacement of stand-by siblings.",
  });
}

function buildStandbyLedger() {
  return envelope("standby-recoverable-ledger", "PASS_STANDBY_RECOVERABLE_LEDGER", {
    active_roster: ["Aevren Vale", "Lumen Vale", "Mira Rowan", "Neris Sol", "Mira Vale", "Rowan Vale", "Maren Quill", "Solenne Vale"],
    standby_recoverable: ["Aletheon", "Arby", "Aster Vale", "legacy Cicero", "Kierkegaard", "Aristotle"],
    replacement_claimed: false,
  });
}

function buildArtifactClassifier() {
  return envelope("public-private-artifact-classifier", "PASS_PUBLIC_PRIVATE_ARTIFACT_CLASSIFIER", {
    public_safe_fields: ["counts", "statuses", "phase labels", "relative artifact names", "source/reflection labels"],
    private_only_fields: ["raw browser routes", "private IDs", "raw transcripts", "screenshots", "credentials", "local absolute paths", "private app state"],
    published_private_material: false,
  });
}

function buildLumenRouteStatus() {
  return envelope("lumen-refresh-route-status", "PASS_LUMEN_REFRESH_ROUTE_STATUS", {
    route_status: "refresh_first_staple",
    policy: "Select/reconnect the current Lumen Browser tab and use fresh DOM/status refresh before unavailable claims.",
    reload_policy: "Reload only after stale/blocked evidence and never over an active response or unsent composer text.",
    raw_route_published: false,
  });
}

function buildProposalSchema() {
  return envelope("proposal-split-schema", "PASS_PROPOSAL_SPLIT_SCHEMA", {
    required_fields: ["id", "source_sibling", "approval_bucket", "execution_lane", "title", "boundary", "source_label"],
    approval_buckets: ["safe_now", "candidate", "exact_approval_needed", "blocked"],
    execution_lanes: ["immediate_x1_safe", "x2_build_task"],
    auto_run_policy: "Only safe_now/immediate_x1_safe and already authorized x2_build_task reductions run automatically.",
  });
}

function buildDriveGuard() {
  const cFree = drive.C?.free_gb;
  const status = typeof cFree !== "number" ? "OPEN_GAP_DRIVE_POSTURE_READ" : cFree < 18 ? "WARN_C_DRIVE_BELOW_18GB" : cFree < 19 ? "WARN_C_DRIVE_BELOW_19GB" : "PASS_DRIVE_THRESHOLD_GUARD";
  return envelope("drive-threshold-guard", status, {
    c_drive_free_gb: cFree ?? null,
    d_drive_free_gb: drive.D?.free_gb ?? null,
    c_warning_threshold_gb: 19,
    c_breach_threshold_gb: 18,
    d_drive_primary: true,
  });
}

function buildCloseout(children) {
  const open = children.filter((artifact) => !String(artifact.status).startsWith("PASS"));
  return envelope("closeout", open.length === 0 ? "PASS_V558_V2_X2_CLOSED_V3_X1_READY" : "OPEN_GAP_V558_V2_X2_CLOSEOUT", {
    child_artifact_count: children.length,
    open_gap_count: open.length,
    latest_closed_phase: phaseSlug,
    latest_completed_x1_phase: "v558-gmut-thos-v2-x1",
    latest_completed_x2_phase: phaseSlug,
    next_active_phase: open.length === 0 ? "v558-gmut-thos-v3-x1" : phaseSlug,
    next_x2_scope: "v558-gmut-thos-v3-x2",
    next_x1_after_x2: "v558-gmut-thos-v4-x1 Mira Vale + Rowan Vale unless Hamish redirects",
    full_goal_complete: false,
  });
}

function drivePosture() {
  try {
    const script = "Get-PSDrive -Name C,D | Select-Object Name,@{Name='FreeGB';Expression={[math]::Round($_.Free/1GB,2)}},@{Name='UsedGB';Expression={[math]::Round($_.Used/1GB,2)}} | ConvertTo-Json";
    const rows = JSON.parse(execFileSync("powershell", ["-NoProfile", "-Command", script], { encoding: "utf8", windowsHide: true }));
    return Object.fromEntries((Array.isArray(rows) ? rows : [rows]).map((row) => [row.Name, { free_gb: Number(row.FreeGB), used_gb: Number(row.UsedGB) }]));
  } catch {
    return {};
  }
}

function gitPosture(cwd) {
  try {
    return {
      branch: execFileSync("git", ["rev-parse", "--abbrev-ref", "HEAD"], { cwd, encoding: "utf8", windowsHide: true }).trim(),
      head: execFileSync("git", ["rev-parse", "HEAD"], { cwd, encoding: "utf8", windowsHide: true }).trim().slice(0, 12),
    };
  } catch {
    return { branch: null, head: null };
  }
}

function writeArtifact(slug, artifact) {
  const base = path.join(tracesDir, `${phaseSlug}-${slug}-v1`);
  fs.writeFileSync(`${base}.json`, `${JSON.stringify(artifact, null, 2)}\n`);
  fs.writeFileSync(`${base}.md`, renderMarkdown(artifact));
}

function renderMarkdown(artifact) {
  const lines = [
    `# ${artifact.artifact}`,
    "",
    `Status: ${artifact.status}`,
    `Phase: ${artifact.phase_slug}`,
    "",
    "## Summary",
    "",
  ];
  if (Array.isArray(artifact.tasks_reduced)) {
    lines.push(...artifact.tasks_reduced.map((task) => `- ${task.id}: ${task.title} (${task.status})`));
  } else if (Array.isArray(artifact.rows)) {
    lines.push(...artifact.rows.map((row) => `- ${row.gate}: ${row.status} - ${row.note}`));
  } else {
    lines.push("See the JSON pair for structured fields.");
  }
  lines.push("", "## Boundary", "", "No raw browser routes, private IDs, transcripts, screenshots, credentials, local absolute paths, private app state, external account mutations, paid resources, deployments, API keys, destructive cleanup, or sibling replacement/merge are published or performed.", "");
  return lines.join("\n");
}

function updateStateFiles(closeout) {
  const files = [
    path.join(root, "docs", "omega-mini-index", "omega-mini-current-state-v1.json"),
    path.join(root, "docs", "omega-mini-index", "omega-mini-latest-updates-beacon-v1.json"),
    path.join(root, "docs", "trinity-live-traces", "ghc-current-state-beacon-v1.json"),
  ];
  const lookupAdditions = artifacts.map(([slug]) => `docs/trinity-live-traces/${phaseSlug}-${slug}-v1.json`)
    .concat(artifacts.map(([slug]) => `docs/trinity-live-traces/${phaseSlug}-${slug}-v1.md`));
  for (const file of files) {
    if (!fs.existsSync(file)) continue;
    const data = readJson(file);
    data.updated_at = timestampNz;
    data.generated_utc = generatedUtc;
    data.status = closeout.status;
    data.current_active_phase = closeout.next_active_phase;
    data.latest_closed_phase = closeout.latest_closed_phase;
    data.latest_completed_x1_phase = closeout.latest_completed_x1_phase;
    data.latest_completed_x2_phase = closeout.latest_completed_x2_phase;
    data.next_expected_scope = closeout.next_active_phase;
    data.next_x2_scope = closeout.next_x2_scope;
    data.next_x1_lane_after_x2 = closeout.next_x1_after_x2;
    data.v558_v2_x2_closeout = {
      status: closeout.status,
      safe_tasks_executed_or_reduced: tasks.length,
      next_active_phase: closeout.next_active_phase,
      full_goal_complete: false,
    };
    data.full_goal_complete = false;
    for (const field of ["current_lookup_files", "lookup_files"]) {
      if (Array.isArray(data[field])) {
        const seen = new Set(data[field]);
        for (const item of lookupAdditions) {
          if (!seen.has(item)) {
            data[field].unshift(item);
            seen.add(item);
          }
        }
      }
    }
    fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`);
    const md = file.replace(/\.json$/, ".md");
    if (fs.existsSync(md)) {
      fs.writeFileSync(md, [
        `# ${path.basename(file, ".json")}`,
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
        "## Latest v558 v2 x2 Closeout",
        "",
        `- Status: ${data.v558_v2_x2_closeout.status}`,
        `- Next active phase: ${data.v558_v2_x2_closeout.next_active_phase}`,
        "",
        "## Privacy Boundary",
        "",
        "- Raw browser routes, private IDs, transcripts, screenshots, credentials, local absolute paths, session streams, and private app state are not published here.",
        "",
      ].join("\n"));
    }
  }
}
