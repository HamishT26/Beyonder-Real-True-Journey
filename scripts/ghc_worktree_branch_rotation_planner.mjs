#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const args = parseArgs(process.argv.slice(2));
const phaseSlug = args.get("--phase-slug") || "v557-gmut-thos-v4-x1";
const miniRoot = args.get("--mini-root") || repoRoot;
const fullToolsRoot = args.get("--full-tools-root");
const nextMini = args.get("--next-mini") || "omega-mini-3";
const nextFullTools = args.get("--next-full-tools") || "full-tools-2";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const mini = inspectWorktree(miniRoot, "omega-mini-publication");
const fullTools = fullToolsRoot ? inspectWorktree(fullToolsRoot, "full-tools-private-support") : null;
const rotationWarnings = [
  ...rotationSignals(mini),
  ...(fullTools ? rotationSignals(fullTools) : []),
];
const recommendRotation = rotationWarnings.length > 0;

const payload = {
  artifact_type: "ghc_worktree_branch_rotation_planner",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: recommendRotation ? "WARN_ROTATION_RECOMMENDED_AT_SAFE_BOUNDARY" : "PASS_ROTATION_NOT_REQUIRED_NOW",
  current_lanes: {
    mini,
    full_tools: fullTools,
  },
  next_lane_names: {
    next_omega_mini_lane: nextMini,
    next_full_tools_lane: nextFullTools,
    example_mini_branch: miniBranchName(nextMini),
    example_full_tools_branch: `codex/GHC-Family/aevren-${nextFullTools}`,
  },
  rotation_warnings: rotationWarnings,
  safe_rotation_policy: [
    "Commit and push only sanitized omega-mini artifacts before creating the next mini branch.",
    "Create new mini lanes from a verified clean sanitized head.",
    "Create new full-tools lanes from a safe base, not from dirty private support files.",
    "Keep raw Lumen responses and private app-lane maps local-only; carry only digests/counts.",
    "Do not delete old worktrees or rewrite history as part of rotation.",
  ],
  activation_state: "planned_not_rotated_by_this_runner",
  publication_boundary: publicationBoundary(),
  safety_boundary: safetyBoundary(),
};

writePair("worktree-branch-rotation-planner", payload);

process.stdout.write(JSON.stringify({
  status: payload.overall_status,
  phase_slug: phaseSlug,
  recommend_rotation: recommendRotation,
  rotation_warnings: rotationWarnings.length,
  next_omega_mini_lane: nextMini,
  next_full_tools_lane: nextFullTools,
  raw_private_material_moved: false,
}, null, 2) + "\n");

function inspectWorktree(root, laneKind) {
  const out = {
    lane_kind: laneKind,
    root_published: false,
    exists: Boolean(root && fs.existsSync(root)),
    git_head: null,
    branch: null,
    porcelain_line_count: null,
    untracked_line_count: null,
    modified_line_count: null,
    trace_artifact_count: null,
    status_error: null,
  };
  if (!out.exists) return out;
  try {
    out.git_head = execGit(root, ["rev-parse", "HEAD"]).trim();
  } catch (error) {
    out.status_error = compactError(error);
  }
  try {
    out.branch = execGit(root, ["branch", "--show-current"]).trim() || "detached";
  } catch {}
  try {
    const status = execGit(root, ["status", "--short"]).split(/\r?\n/).filter(Boolean);
    out.porcelain_line_count = status.length;
    out.untracked_line_count = status.filter((line) => line.startsWith("??")).length;
    out.modified_line_count = status.length - out.untracked_line_count;
  } catch (error) {
    out.status_error = compactError(error);
  }
  try {
    const traceDir = path.join(root, "docs", "trinity-live-traces");
    out.trace_artifact_count = fs.existsSync(traceDir)
      ? fs.readdirSync(traceDir).filter((name) => name.endsWith(".json") || name.endsWith(".md")).length
      : 0;
  } catch {}
  return out;
}

function rotationSignals(lane) {
  const signals = [];
  if (!lane.exists) {
    signals.push({ lane_kind: lane.lane_kind, signal: "missing_lane", severity: "warning" });
    return signals;
  }
  if ((lane.porcelain_line_count || 0) > 200) {
    signals.push({ lane_kind: lane.lane_kind, signal: "very_large_dirty_or_untracked_surface", count: lane.porcelain_line_count, severity: "warning" });
  }
  if ((lane.untracked_line_count || 0) > 100) {
    signals.push({ lane_kind: lane.lane_kind, signal: "large_untracked_surface", count: lane.untracked_line_count, severity: "warning" });
  }
  if ((lane.trace_artifact_count || 0) > 1200) {
    signals.push({ lane_kind: lane.lane_kind, signal: "large_trace_artifact_surface", count: lane.trace_artifact_count, severity: "advisory" });
  }
  if (lane.branch === "detached" && lane.lane_kind.includes("full-tools")) {
    signals.push({ lane_kind: lane.lane_kind, signal: "detached_private_support_lane", severity: "advisory" });
  }
  if (lane.status_error) {
    signals.push({ lane_kind: lane.lane_kind, signal: "git_status_error", severity: "warning" });
  }
  return signals;
}

function execGit(cwd, gitArgs) {
  return execFileSync("git", gitArgs, { cwd, encoding: "utf8", timeout: 60000 });
}

function compactError(error) {
  return String(error?.message || error).slice(0, 180);
}

function writePair(suffix, doc) {
  fs.mkdirSync(tracesDir, { recursive: true });
  const base = path.join(tracesDir, `${phaseSlug}-${suffix}-v1`);
  fs.writeFileSync(`${base}.json`, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
  fs.writeFileSync(`${base}.md`, renderMd(doc), "utf8");
}

function renderMd(doc) {
  return [
    `# ${doc.phase_slug} worktree branch rotation planner`,
    "",
    `Status: \`${doc.overall_status}\``,
    "",
    `Recommended next mini lane: \`${doc.next_lane_names.next_omega_mini_lane}\``,
    `Recommended next full-tools lane: \`${doc.next_lane_names.next_full_tools_lane}\``,
    "",
    "## Rotation Warnings",
    "",
    ...(doc.rotation_warnings.length
      ? doc.rotation_warnings.map((warning) => `- \`${warning.lane_kind}\`: ${warning.signal}`)
      : ["- none"]),
    "",
    "## Safe Rotation Policy",
    "",
    ...doc.safe_rotation_policy.map((line) => `- ${line}`),
    "",
    "## Boundary",
    "",
    "No raw Lumen text, private callable IDs, private Browser routes, local private paths, screenshots, credentials, destructive cleanup, history rewrite, deployment, purchase, account mutation, API key creation, or sibling identity changes were performed.",
    "",
  ].join("\n");
}

function publicationBoundary() {
  return {
    local_absolute_paths_published: false,
    raw_private_material_published: false,
    private_callable_ids_published: false,
    private_browser_routes_published: false,
    screenshots_published: false,
    credentials_published: false,
  };
}

function safetyBoundary() {
  return {
    destructive_cleanup_performed: false,
    history_rewritten: false,
    branches_created_by_runner: false,
    worktrees_created_by_runner: false,
    external_accounts_modified: false,
    paid_resources_created: false,
    deployments_created: false,
    api_keys_created: false,
    sibling_activation_performed: false,
  };
}

function parseArgs(argv) {
  const out = new Map();
  for (let index = 0; index < argv.length; index += 1) {
    const key = argv[index];
    if (!key.startsWith("--")) continue;
    const value = argv[index + 1];
    if (!value || value.startsWith("--")) {
      out.set(key, "true");
    } else {
      out.set(key, value);
      index += 1;
    }
  }
  return out;
}

function miniBranchName(laneName) {
  const normalized = String(laneName || "").replace(/^omega-/, "");
  return `codex/GHC-Family/beyonder-shared-omega-line-${normalized}`;
}

function nzTimestamp(date) {
  return new Intl.DateTimeFormat("en-NZ", {
    timeZone: "Pacific/Auckland",
    dateStyle: "medium",
    timeStyle: "medium",
    hourCycle: "h23",
  }).format(date);
}
