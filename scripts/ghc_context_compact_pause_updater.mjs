#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import { mkdirSync, writeFileSync } from "node:fs";
import { basename, dirname, join } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const ROOT = new URL("..", import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1");
const root = args.get("--root") || ROOT;
const phaseSlug = args.get("--phase-slug");
const receiptPrefix = args.get("--receipt-prefix") || `${phaseSlug}-compact-pause-updater`;
const agent = args.get("--agent") || "Aevren Vale";

if (!phaseSlug) {
  console.error("Usage: node ghc_context_compact_pause_updater.mjs --phase-slug <slug> [--receipt-prefix <prefix>]");
  process.exit(2);
}

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function runUpdater() {
  return spawnSync(
    process.execPath,
    [
      join(root, "scripts", "ghc_phase_startup_context_updater.mjs"),
      "--root",
      root,
      "--phase-slug",
      phaseSlug,
      "--event",
      "compact-pause",
      "--agent",
      agent,
      "--receipt-prefix",
      `${receiptPrefix}-startup-snapshot`,
    ],
    {
      cwd: root,
      encoding: "utf8",
      windowsHide: true,
      maxBuffer: 1024 * 1024,
    },
  );
}

const generatedUtc = utcNow();
const proc = runUpdater();
let childStatus = "unparsed";
try {
  childStatus = JSON.parse(proc.stdout || "{}").status || "json_status_missing";
} catch {
  childStatus = "unparsed";
}

const receipt = {
  artifact_type: "ghc_context_compact_pause_updater",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  overall_status: proc.status === 0 ? "PASS_COMPACT_PAUSE_CONTEXT_UPDATED" : "OPEN_GAP_COMPACT_PAUSE_CONTEXT_UPDATE",
  policy: {
    run_on_precompact_or_postcompact: true,
    manual_invocation_supported: true,
    auto_hook_installed: false,
    reason_auto_hook_not_installed: "Global Codex hook installation is a broader local app-state mutation and needs a fresh exact approval packet.",
    preserve_active_sibling_as_open_not_closed: true,
    preserve_blocker_retry_progress: true,
    blocker_retry_minimum_sessions_before_pause: 3,
    blocker_retry_web_search_reflections_per_retry: 20,
    blocker_retry_journey_phase_reflections_per_retry: 20,
  },
  child_updater: {
    status: proc.status,
    stdout_status: childStatus,
    stdout_bytes: Buffer.byteLength(proc.stdout || "", "utf8"),
    stderr_bytes: Buffer.byteLength(proc.stderr || "", "utf8"),
  },
  publication_boundary: {
    private_route_handles_published: false,
    private_lane_body_content_published: false,
    verbatim_conversation_logs_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
  },
  claim_boundary: {
    phase_completion: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    canon_promotion: "not_claimed",
  },
};

const traceDir = join(root, "docs", "trinity-live-traces");
const receiptJson = join(traceDir, `${receiptPrefix}-v1.json`);
const receiptMd = join(traceDir, `${receiptPrefix}-v1.md`);
mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");
writeFileSync(
  receiptMd,
  [
    `# ${phaseSlug} Compact Pause Updater`,
    "",
    `Generated UTC: \`${generatedUtc}\``,
    "",
    `Status: \`${receipt.overall_status}\``,
    "",
    "## Policy",
    "",
    "- Run on pre-compact or post-compact events when an exact hook/automation approval exists.",
    "- Manual invocation is supported now.",
    "- No global hook was installed in this safe-now packet.",
    "- Active sibling lanes are preserved as active/open, not closed.",
    "- Blocker retry progress preserves retry number, 10-session reflection, 20 web-search reflections, and 20 Journey/phase-document reflections.",
    "",
    "## Boundary",
    "",
    "Status-only compact updater. No private routes, private lane body content, verbatim conversation logs, credentials, or local absolute paths are published.",
    "",
  ].join("\n"),
  "utf8",
);

console.log(
  JSON.stringify(
    {
      status: receipt.overall_status,
      child_status: childStatus,
      receipt: basename(receiptJson),
    },
    null,
    2,
  ),
);
process.exit(proc.status === 0 ? 0 : 1);
