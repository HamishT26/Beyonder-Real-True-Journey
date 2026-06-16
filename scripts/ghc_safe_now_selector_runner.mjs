#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, dirname } from "node:path";

const args = parseArgs(process.argv.slice(2));
const phaseSlug = requireArg("--phase-slug");
const stackJson = requireArg("--stack-json");
const receiptJson = requireArg("--receipt-json");
const receiptMd = requireArg("--receipt-md");
const limit = Number(args.get("--limit")?.[0] || "20");

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 1) {
    const key = argv[index];
    if (!key.startsWith("--")) continue;
    const value = argv[index + 1];
    if (!value || value.startsWith("--")) {
      if (!parsed.has(key)) parsed.set(key, []);
      parsed.get(key).push("true");
      continue;
    }
    if (!parsed.has(key)) parsed.set(key, []);
    parsed.get(key).push(value);
    index += 1;
  }
  return parsed;
}

function requireArg(key) {
  const values = args.get(key);
  if (!values || !values[0]) {
    console.error(`Missing required argument: ${key}`);
    process.exit(2);
  }
  return values[0];
}

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function publicSourceRef(path) {
  const normalized = path.replace(/\\/g, "/");
  const docsIndex = normalized.lastIndexOf("docs/");
  if (docsIndex >= 0) return normalized.slice(docsIndex);
  return basename(normalized);
}

function isRunnable(row) {
  return row?.scope_bucket === "safe_now" && row?.completion_bucket === "uncompleted";
}

function rowKey(row) {
  return `${row.kind || "row"}:${row.id || "unknown"}:${row.source_phase || "unknown"}`;
}

function selectRows(rows, rowLimit) {
  const seen = new Set();
  const selected = [];
  for (const row of rows || []) {
    if (!isRunnable(row)) continue;
    const key = rowKey(row);
    if (seen.has(key)) continue;
    seen.add(key);
    selected.push({
      selector_order: selected.length + 1,
      id: row.id,
      title: row.title,
      source_phase: row.source_phase,
      source_ref: row.source_ref,
      source_order: row.source_order,
      action: row.purpose_or_action || row.action || row.purpose || "",
      scope_bucket: row.scope_bucket,
      completion_bucket: row.completion_bucket,
      execution_status: "queued_for_x2",
    });
    if (selected.length >= rowLimit) break;
  }
  return selected;
}

const stack = JSON.parse(readFileSync(stackJson, "utf8"));
const approvalRows = Array.isArray(stack.approval_packets) ? stack.approval_packets : [];
const eurekaRows = Array.isArray(stack.eureka_tasks) ? stack.eureka_tasks : [];
const selectedApprovals = selectRows(approvalRows, Math.min(limit, 10));
const selectedEureka = selectRows(eurekaRows, limit);
const selectedRows = [...selectedApprovals.map((row) => ({ ...row, kind: "approval_packet" })), ...selectedEureka.map((row) => ({ ...row, kind: "eureka_task" }))];

const receipt = {
  schema: "ghc.safe_now_selector.v1",
  generated_utc: utcNow(),
  phase_slug: phaseSlug,
  status: selectedRows.length > 0 ? "PASS_SAFE_NOW_SELECTOR_READY" : "OPEN_GAP_SAFE_NOW_SELECTOR_EMPTY",
  source_stack_ref: publicSourceRef(stackJson),
  selection_policy: {
    scope_bucket_required: "safe_now",
    completion_bucket_required: "uncompleted",
    approval_limit: Math.min(limit, 10),
    eureka_limit: limit,
    raw_lane_content_used: false,
  },
  selected_approval_count: selectedApprovals.length,
  selected_eureka_count: selectedEureka.length,
  selected_total_count: selectedRows.length,
  selected_rows: selectedRows,
  next_actions: [
    "Use selected Eureka rows as v5 x2 build/use candidates inside existing repo-scoped guard rails.",
    "Use selected approval rows as operating permissions only where their source receipt supports the scope.",
    "Do not execute candidate, defer, blocked, or needs_exact_packet rows through this selector.",
    "Refresh this selector after new Lumen, sibling, or Aletheon x2 rows are added to the stack.",
  ],
  publication_boundary: {
    raw_lane_content_published: false,
    raw_chatgpt_transcript_published: false,
    raw_browser_routes_published: false,
    raw_route_handles_published: false,
    screen_capture_files_published: false,
    session_trace_files_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
  },
  claim_boundary: {
    selected_rows_are_completion_proof: false,
    phase_completion: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
  },
};

mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");

const table = selectedRows.map(
  (row) => `| ${row.selector_order} | ${row.kind} | ${row.id} | ${row.title} | ${row.source_phase} | ${row.execution_status} |`,
);
const md = [
  `# ${phaseSlug} Safe-Now Selector`,
  "",
  `Generated UTC: \`${receipt.generated_utc}\``,
  `Status: \`${receipt.status}\``,
  `Source stack: \`${receipt.source_stack_ref}\``,
  "",
  "## Counts",
  "",
  `- Selected approval packets: \`${receipt.selected_approval_count}\``,
  `- Selected Eureka tasks: \`${receipt.selected_eureka_count}\``,
  `- Selected total rows: \`${receipt.selected_total_count}\``,
  "",
  "## Selected Rows",
  "",
  "| # | Kind | ID | Title | Source Phase | Execution Status |",
  "|---:|---|---|---|---|---|",
  ...(table.length ? table : ["| 0 | none | none | No safe-now rows selected | none | none |"]),
  "",
  "## Boundary",
  "",
  "- This selector publishes status-only row metadata and never raw sibling text, raw ChatGPT transcript, browser routes, screenshots, credentials, or local absolute paths.",
  "- Selected rows are not completion proof. They are x2 execution candidates under existing guard rails.",
  "",
].join("\n");
writeFileSync(receiptMd, md, "utf8");

console.log(
  JSON.stringify(
    {
      status: receipt.status,
      selected_approval_count: receipt.selected_approval_count,
      selected_eureka_count: receipt.selected_eureka_count,
      selected_total_count: receipt.selected_total_count,
    },
    null,
    2,
  ),
);

if (receipt.status !== "PASS_SAFE_NOW_SELECTOR_READY") {
  process.exit(1);
}
