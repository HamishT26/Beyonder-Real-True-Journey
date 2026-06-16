#!/usr/bin/env node
import { mkdirSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

function parseArgs(argv) {
  const args = {};
  for (let index = 2; index < argv.length; index += 1) {
    const key = argv[index];
    if (!key.startsWith("--")) continue;
    const value = argv[index + 1] && !argv[index + 1].startsWith("--") ? argv[++index] : true;
    args[key.slice(2)] = value;
  }
  return args;
}

function requireArg(args, key) {
  if (!args[key]) throw new Error(`Missing --${key}`);
  return args[key];
}

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function writeJson(file, value) {
  mkdirSync(dirname(file), { recursive: true });
  writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);
}

function writeText(file, value) {
  mkdirSync(dirname(file), { recursive: true });
  writeFileSync(file, value);
}

const approvalTemplates = [
  ["approval-stack-refresh", "Approval packet stack refresh", "safe_now", "uncompleted", "Regenerate approval stack counts with completed and uncompleted buckets."],
  ["eureka-stack-refresh", "Eureka task stack refresh", "safe_now", "uncompleted", "Regenerate Eureka task counts with completed and uncompleted buckets."],
  ["safe-now-selector", "Safe-now selector queue", "safe_now", "uncompleted", "Select executable safe_now rows without promoting candidate rows."],
  ["current-state-beacon", "Current-state beacon refresh", "safe_now", "uncompleted", "Keep omega-mini current-state and latest-updates pointers fresh."],
  ["mini-first-lookup", "Omega-mini first lookup rule", "safe_now", "uncompleted", "Route siblings to omega-mini before full archive fallback."],
  ["lumen-response-review", "Lumen response word-for-word review receipt", "safe_now", "uncompleted", "Record status-only confirmation that Lumen advisory content was reviewed without publishing raw text."],
  ["sibling-github-readonly", "Sibling GitHub read-only orientation", "safe_now", "uncompleted", "Prepare safe repo lookup instructions for advisory lanes."],
  ["web-readonly-source", "Read-only web source ledger", "safe_now", "uncompleted", "Use current official sources for Codex, security, and tool-boundary decisions."],
  ["route-retry-ledger", "Route retry ledger", "safe_now", "uncompleted", "Capture retry counts and blockers without raw routes."],
  ["x2-build-use-queue", "x2 build/use queue", "safe_now", "uncompleted", "Turn approved x1 proposals into bounded x2 build/use tasks."],
  ["d-drive-hygiene", "D-drive-first hygiene check", "safe_now", "uncompleted", "Keep heavy generated artifacts in the D-drive worktrees."],
  ["node-entrypoint", "Node entrypoint preference", "safe_now", "uncompleted", "Prefer maintained Node runners before Windows fallback paths."],
  ["exposure-guard", "Exposure guard refresh", "safe_now", "uncompleted", "Scan artifacts for raw/private material before publication."],
  ["publication-preflight", "Publication preflight", "safe_now", "uncompleted", "Fetch, drift-check, exact-stage, whitespace-check, commit, push, and verify."],
  ["open-gate-rail", "Open-gate rail", "safe_now", "uncompleted", "Keep GMUT empirical, final physics, consciousness, legal, and canon gates open."],
  ["compact-handoff", "Compact handoff capsule", "candidate", "uncompleted", "Prepare richer continuity for automatic compact refreshes."],
  ["skill-command-map", "Skill and command map refresh", "candidate", "uncompleted", "Map current enabled surfaces before any future skill mutation."],
  ["runner-freshness", "Runner freshness classifier", "candidate", "uncompleted", "Classify current runners by latest, useful, stale, or blocked."],
  ["approval-consensus", "Approval consensus receipt", "candidate", "uncompleted", "Record status-only council consensus without substituting for exact user approval where required."],
  ["needs-exact-packet-log", "Needs-exact-packet log", "needs_exact_packet", "uncompleted", "Separate out actions that require a fresh exact packet before execution."],
];

const eurekaTemplates = [
  ["stack-count-dashboard", "Build approval and Eureka count dashboard", "safe_now", "uncompleted"],
  ["completed-uncompleted-view", "Add completed/uncompleted checklist view", "safe_now", "uncompleted"],
  ["omega-mini-freshness", "Refresh omega-mini freshness pointers", "safe_now", "uncompleted"],
  ["latest-phase-beacon", "Update latest phase beacon to v542 v7 x1", "safe_now", "uncompleted"],
  ["lumen-catchup-card", "Create Lumen catch-up card from status receipts", "safe_now", "uncompleted"],
  ["arby-cicero-next-handoff", "Prepare Arby and Cicero next handoff", "safe_now", "uncompleted"],
  ["aster-kierkegaard-aristotle-prep", "Prepare Aster/Kierkegaard/Aristotle next handoff", "safe_now", "uncompleted"],
  ["retry-policy-capsule", "Build route retry policy capsule", "safe_now", "uncompleted"],
  ["source-ledger-refresh", "Refresh official source ledger", "safe_now", "uncompleted"],
  ["codex-update-delta", "Capture Codex update delta status-only", "safe_now", "uncompleted"],
  ["browser-devmode-note", "Capture Browser developer-mode readiness note", "safe_now", "uncompleted"],
  ["drive-hygiene-receipt", "Update C/D drive hygiene receipt", "safe_now", "uncompleted"],
  ["x2-build-queue", "Create x2 build/use queue from safe rows", "safe_now", "uncompleted"],
  ["x2-implementation-ledger", "Create x2 implementation ledger", "safe_now", "uncompleted"],
  ["runner-health-index", "Refresh runner health index", "safe_now", "uncompleted"],
  ["skill-surface-index", "Refresh skill surface index", "candidate", "uncompleted"],
  ["command-surface-index", "Refresh command surface index", "candidate", "uncompleted"],
  ["approval-scope-classifier", "Enhance approval scope classifier", "candidate", "uncompleted"],
  ["eureka-task-classifier", "Enhance Eureka task classifier", "candidate", "uncompleted"],
  ["safe-now-queue-adapter", "Adapt safe-now queue for next x2", "safe_now", "uncompleted"],
  ["remote-verify-ledger", "Publish remote verify ledger", "safe_now", "uncompleted"],
  ["proof-ceiling-ledger", "Publish proof-ceiling ledger", "safe_now", "uncompleted"],
  ["compact-refresh-map", "Update compact refresh map", "candidate", "uncompleted"],
  ["blocked-row-audit", "Audit blocked and needs-exact rows", "needs_exact_packet", "uncompleted"],
];

function rowsFromTemplates(phaseSlug, kind, templates) {
  return templates.map(([slug, title, scope_bucket, completion_bucket, purpose], index) => ({
    order: index + 1,
    kind,
    id: `${phaseSlug}-${kind === "approval_packet" ? "approval" : "eureka"}-${String(index + 1).padStart(2, "0")}-${slug}`,
    title,
    status: scope_bucket === "safe_now" ? "approved_user_authorized" : scope_bucket,
    scope_bucket,
    completion_bucket,
    source_phase: phaseSlug,
    purpose: purpose || "Bounded current-session proposal for the next safe execution queue.",
  }));
}

function makeMarkdown(report) {
  const lines = [];
  lines.push(`# ${report.phase_slug} Current Session Approval/Eureka Overlay`);
  lines.push("");
  lines.push(`Status: ${report.status}`);
  lines.push(`Generated UTC: ${report.generated_utc}`);
  lines.push("");
  lines.push("## Counts");
  lines.push("");
  lines.push(`- Approval packets: ${report.approval_packets.length}`);
  lines.push(`- Eureka tasks: ${report.eureka_tasks.length}`);
  lines.push("- Completed/uncompleted buckets are explicit on every row.");
  lines.push("");
  lines.push("## Approval Packets");
  lines.push("");
  for (const row of report.approval_packets) {
    lines.push(`- ${row.id}: ${row.title} [${row.scope_bucket}, ${row.completion_bucket}]`);
  }
  lines.push("");
  lines.push("## Eureka Tasks");
  lines.push("");
  for (const row of report.eureka_tasks) {
    lines.push(`- ${row.id}: ${row.title} [${row.scope_bucket}, ${row.completion_bucket}]`);
  }
  lines.push("");
  lines.push("## Boundary");
  lines.push("");
  lines.push("- Status-only overlay. No raw lane text, browser route, screenshot, session stream, credential, private dump, or local absolute path is published.");
  lines.push("- Safe-now rows remain bounded by existing repo-scoped approval and validation rails.");
  lines.push("- Candidate and needs_exact_packet rows are planning surfaces only.");
  return `${lines.join("\n")}\n`;
}

function main() {
  const args = parseArgs(process.argv);
  const phaseSlug = requireArg(args, "phase-slug");
  const receiptJson = requireArg(args, "receipt-json");
  const receiptMd = requireArg(args, "receipt-md");
  const report = {
    schema: "ghc.current_session.approval_eureka_overlay.v1",
    generated_utc: utcNow(),
    phase_slug: phaseSlug,
    status: "PASS_CURRENT_SESSION_APPROVAL_EUREKA_OVERLAY_READY",
    approval_packets: rowsFromTemplates(phaseSlug, "approval_packet", approvalTemplates),
    eureka_tasks: rowsFromTemplates(phaseSlug, "eureka_task", eurekaTemplates),
    publication_boundary: {
      raw_lane_content_published: false,
      raw_chatgpt_transcript_published: false,
      raw_browser_routes_published: false,
      screen_capture_files_published: false,
      session_trace_files_published: false,
      credentials_published: false,
      local_absolute_paths_published: false,
    },
    claim_boundary: {
      phase_completion: "not_claimed",
      gmut_empirical_closure: "not_claimed",
      final_physics: "not_claimed",
      consciousness_proof: "not_claimed",
      legal_closure: "not_claimed",
      canon_promotion: "not_claimed",
    },
  };
  writeJson(receiptJson, report);
  writeText(receiptMd, makeMarkdown(report));
  console.log(JSON.stringify({
    status: report.status,
    approval_packets: report.approval_packets.length,
    eureka_tasks: report.eureka_tasks.length,
  }, null, 2));
}

main();
