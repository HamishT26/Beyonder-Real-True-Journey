#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, join } from "node:path";

const args = parseArgs(process.argv.slice(2));
const phaseSlug = required("--phase-slug");
const tracesDir = join(process.cwd(), "docs", "trinity-live-traces");
const sourceX1 = args.get("--source-x1") || inferSourceX1(phaseSlug);
const queuePath = args.get("--queue") || findQueue(sourceX1);
const mode = args.get("--mode") || (phaseSlug.endsWith("-x2") ? "x2" : "x1");
const now = new Date();
const generatedUtc = now.toISOString().replace(/\.\d{3}Z$/, "Z");
const generatedNz = nzTimestamp(now);
mkdirSync(tracesDir, { recursive: true });

if (!queuePath || !existsSync(queuePath)) {
  console.error(JSON.stringify({
    status: "OPEN_GAP_COMPLETE_INCOMPLETE_QUEUE_MISSING",
    phase_slug: phaseSlug,
    source_x1: sourceX1,
    queue_path_published: false,
  }, null, 2));
  process.exit(2);
}

const queue = readJson(queuePath);
const rows = Array.isArray(queue.rows) ? queue.rows : [];
const evidence = collectEvidence(phaseSlug, mode);
const checklistRows = rows.map((row, index) => classifyRow(row, index, evidence, mode));
const counts = checklistRows.reduce((acc, row) => {
  acc.total += 1;
  acc.by_status[row.completion_status] = (acc.by_status[row.completion_status] || 0) + 1;
  acc.by_kind[row.kind] = (acc.by_kind[row.kind] || 0) + 1;
  acc.by_approval_bucket[row.approval_bucket] = (acc.by_approval_bucket[row.approval_bucket] || 0) + 1;
  return acc;
}, { total: 0, by_status: {}, by_kind: {}, by_approval_bucket: {} });
const incompleteRequired = checklistRows.filter((row) => row.required_before_closeout && row.completion_status !== "COMPLETED").length;
const queuedOutOfScope = checklistRows.filter((row) => row.completion_status === "QUEUED_OUT_OF_SCOPE_EXACT_OR_BLOCKED").length;
const overallStatus = incompleteRequired === 0
  ? "PASS_COMPLETE_INCOMPLETE_CHECKLIST_REQUIRED_WORK_COMPLETED"
  : "OPEN_GAP_COMPLETE_INCOMPLETE_CHECKLIST_REQUIRED_WORK_INCOMPLETE";

const artifact = {
  artifact: `docs/trinity-live-traces/${phaseSlug}-complete-incomplete-checklist-v1`,
  schema: "ghc.complete_incomplete_checklist.v1",
  phase_slug: phaseSlug,
  source_x1_phase: sourceX1,
  mode,
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  status: overallStatus,
  closeout_allowed_by_checklist: incompleteRequired === 0,
  mandatory_rule: "immediate_x1_safe, candidate, cleanup/refine/fix, skill, and runner proposal rows must be completed or represented by matching safe ledgers before closeout; exact-approval and blocked rows remain queued out of scope",
  source_queue_basename: basename(queuePath),
  raw_private_material_published: false,
  counts,
  incomplete_required_rows: incompleteRequired,
  queued_out_of_scope_rows: queuedOutOfScope,
  evidence,
  rows: checklistRows,
  open_gates: [
    "exact approval packets remain queued",
    "blocked packets remain queued",
    "GMUT empirical closure remains open",
    "final physics and consciousness proof remain open",
    "legal/canon/deployment/account/API-key/private-material/raw-publication gates remain open",
    "sibling replacement/merge/erasure gates remain open",
  ],
};

writePair(artifact);

console.log(JSON.stringify({
  status: overallStatus,
  phase_slug: phaseSlug,
  source_x1: sourceX1,
  queue_rows: rows.length,
  completed_rows: counts.by_status.COMPLETED || 0,
  incomplete_required_rows: incompleteRequired,
  queued_out_of_scope_rows: queuedOutOfScope,
  closeout_allowed_by_checklist: artifact.closeout_allowed_by_checklist,
  receipt: `${phaseSlug}-complete-incomplete-checklist-v1.json`,
}, null, 2));

function classifyRow(row, index, evidence, mode) {
  const kind = row.kind || "unknown";
  const approvalBucket = row.approval_bucket || "unknown";
  const executionLane = row.execution_lane || "unknown";
  const exactOrBlocked = approvalBucket === "exact_approval_needed" || approvalBucket === "blocked" || /exact|blocked/.test(kind);
  const required = !exactOrBlocked && (
    approvalBucket === "safe_now" ||
    approvalBucket === "candidate" ||
    executionLane === "immediate_x1_safe" ||
    ["cleanup_task", "skill_idea", "runner_idea", "candidate_packet", "safe_approval_packet"].includes(kind)
  );
  const category = categoryFor(kind, approvalBucket, executionLane);
  let completionStatus = "NOT_REQUIRED";
  let completionEvidence = "not_required";
  if (exactOrBlocked) {
    completionStatus = "QUEUED_OUT_OF_SCOPE_EXACT_OR_BLOCKED";
    completionEvidence = "exact_or_blocked_boundary";
  } else if (required) {
    const hasEvidence = hasCategoryEvidence(category, evidence, mode);
    completionStatus = hasEvidence ? "COMPLETED" : "INCOMPLETE";
    completionEvidence = hasEvidence ? evidenceForCategory(category, evidence, mode) : `missing_${category}_completion_evidence`;
  }
  return {
    row_index: index + 1,
    id: row.id || `${sourceX1}-row-${String(index + 1).padStart(3, "0")}`,
    kind,
    approval_bucket: approvalBucket,
    execution_lane: executionLane,
    required_before_closeout: required,
    completion_status: completionStatus,
    completion_evidence: completionEvidence,
    summary: sanitize(row.summary || ""),
    raw_text_published: false,
  };
}

function categoryFor(kind, approvalBucket, executionLane) {
  if (kind === "cleanup_task") return "cleanup";
  if (kind === "skill_idea" || kind === "runner_idea") return "skill_runner";
  if (approvalBucket === "candidate" || kind === "candidate_packet") return "candidate";
  if (executionLane === "immediate_x1_safe" || approvalBucket === "safe_now") return "safe";
  return "general";
}

function hasCategoryEvidence(category, evidence, mode) {
  if (mode === "x1") {
    return evidence.x1_harvest_or_closeout_ready;
  }
  if (category === "cleanup") return evidence.cleanup_ledger;
  if (category === "skill_runner") return evidence.skill_runner_ledger;
  if (category === "candidate") return evidence.safe_build_ledger || evidence.x2_execution_ledger;
  return evidence.safe_build_ledger || evidence.x2_execution_ledger || evidence.safe_runner_orchestrator;
}

function evidenceForCategory(category, evidence, mode) {
  if (mode === "x1") return evidence.x1_harvest_or_closeout_ready_name;
  if (category === "cleanup") return evidence.cleanup_ledger_name;
  if (category === "skill_runner") return evidence.skill_runner_ledger_name;
  if (category === "candidate") return evidence.safe_build_ledger_name || evidence.x2_execution_ledger_name;
  return evidence.safe_build_ledger_name || evidence.x2_execution_ledger_name || evidence.safe_runner_orchestrator_name;
}

function collectEvidence(slug, mode) {
  const names = [
    `${slug}-safe-build-use-ledger-v1.json`,
    `${slug}-x2-execution-ledger-v1.json`,
    `${slug}-cleanup-classifier-ledger-v1.json`,
    `${slug}-skill-runner-prototype-use-ledger-v1.json`,
    `${slug}-skill-runner-prototype-ledger-v1.json`,
    `${slug}-safe-runner-orchestrator-v1.json`,
    `${sourceX1}-lumen-browser-send-receipt-v1.json`,
    `${sourceX1}-lumen-harvest-reduction-v1.json`,
    `${sourceX1}-duo-harvest-reduction-v1.json`,
    `${sourceX1}-lumen-closeout-v1.json`,
    `${sourceX1}-duo-closeout-v1.json`,
  ];
  const byName = Object.fromEntries(names.map((name) => [name, readStatus(name)]));
  const statusPass = (name) => byName[name]?.startsWith("PASS");
  return {
    mode,
    safe_build_ledger: statusPass(`${slug}-safe-build-use-ledger-v1.json`),
    safe_build_ledger_name: statusPass(`${slug}-safe-build-use-ledger-v1.json`) ? `${slug}-safe-build-use-ledger-v1.json` : null,
    x2_execution_ledger: statusPass(`${slug}-x2-execution-ledger-v1.json`),
    x2_execution_ledger_name: statusPass(`${slug}-x2-execution-ledger-v1.json`) ? `${slug}-x2-execution-ledger-v1.json` : null,
    cleanup_ledger: statusPass(`${slug}-cleanup-classifier-ledger-v1.json`),
    cleanup_ledger_name: statusPass(`${slug}-cleanup-classifier-ledger-v1.json`) ? `${slug}-cleanup-classifier-ledger-v1.json` : null,
    skill_runner_ledger: statusPass(`${slug}-skill-runner-prototype-use-ledger-v1.json`) || statusPass(`${slug}-skill-runner-prototype-ledger-v1.json`),
    skill_runner_ledger_name: statusPass(`${slug}-skill-runner-prototype-use-ledger-v1.json`) ? `${slug}-skill-runner-prototype-use-ledger-v1.json` : statusPass(`${slug}-skill-runner-prototype-ledger-v1.json`) ? `${slug}-skill-runner-prototype-ledger-v1.json` : null,
    safe_runner_orchestrator: statusPass(`${slug}-safe-runner-orchestrator-v1.json`),
    safe_runner_orchestrator_name: statusPass(`${slug}-safe-runner-orchestrator-v1.json`) ? `${slug}-safe-runner-orchestrator-v1.json` : null,
    x1_harvest_or_closeout_ready: mode === "x1" && (
      statusPass(`${sourceX1}-lumen-harvest-reduction-v1.json`) ||
      statusPass(`${sourceX1}-duo-harvest-reduction-v1.json`) ||
      statusPass(`${sourceX1}-lumen-closeout-v1.json`) ||
      statusPass(`${sourceX1}-duo-closeout-v1.json`)
    ),
    x1_harvest_or_closeout_ready_name: mode === "x1"
      ? [`${sourceX1}-lumen-harvest-reduction-v1.json`, `${sourceX1}-duo-harvest-reduction-v1.json`, `${sourceX1}-lumen-closeout-v1.json`, `${sourceX1}-duo-closeout-v1.json`].find(statusPass) || null
      : null,
    checked_artifacts: byName,
  };
}

function readStatus(name) {
  const file = join(tracesDir, name);
  if (!existsSync(file)) return null;
  try {
    const data = readJson(file);
    return data.status || data.overall_status || null;
  } catch {
    return "OPEN_GAP_JSON_PARSE_FAILED";
  }
}

function findQueue(source) {
  const candidates = [
    `${source}-lumen-sanitized-proposal-queue-v1.json`,
    `${source}-duo-sanitized-proposal-queue-v1.json`,
  ].map((name) => join(tracesDir, name));
  return candidates.find((file) => existsSync(file));
}

function inferSourceX1(slug) {
  return slug.endsWith("-x2") ? slug.replace(/-x2$/, "-x1") : slug;
}

function writePair(data) {
  const base = join(tracesDir, `${phaseSlug}-complete-incomplete-checklist-v1`);
  writeFileSync(`${base}.json`, `${JSON.stringify(data, null, 2)}\n`, "utf8");
  writeFileSync(`${base}.md`, renderMd(data), "utf8");
}

function renderMd(data) {
  return `# ${phaseSlug} Complete/Incomplete Checklist

Status: \`${data.status}\`
Closeout allowed by checklist: \`${data.closeout_allowed_by_checklist}\`
Source x1: \`${data.source_x1_phase}\`
Source queue: \`${data.source_queue_basename}\`

## Counts

- Total rows: \`${data.counts.total}\`
- Completed rows: \`${data.counts.by_status.COMPLETED || 0}\`
- Incomplete required rows: \`${data.incomplete_required_rows}\`
- Queued exact/blocked rows: \`${data.queued_out_of_scope_rows}\`

## Mandatory Rule

${data.mandatory_rule}

## Open Gates

${data.open_gates.map((gate) => `- ${gate}`).join("\n")}
`;
}

function parseArgs(argv) {
  const out = new Map();
  for (let i = 0; i < argv.length; i += 1) {
    const key = argv[i];
    if (!key.startsWith("--")) continue;
    const value = argv[i + 1];
    if (!value || value.startsWith("--")) out.set(key, "true");
    else {
      out.set(key, value);
      i += 1;
    }
  }
  return out;
}

function required(flag) {
  const value = args.get(flag);
  if (!value) {
    console.error(`Usage: node scripts/ghc_complete_incomplete_checklist_runner.mjs ${flag} <value>`);
    process.exit(2);
  }
  return value;
}

function readJson(file) {
  return JSON.parse(readFileSync(file, "utf8"));
}

function sanitize(value) {
  return String(value)
    .replace(/[A-Z]:[\\/][^\s`'"<>]+/g, "[local-path-redacted]")
    .replace(/https:\/\/chatgpt\.com\/c\/[A-Za-z0-9?=_-]+/g, "[browser-route-redacted]")
    .slice(0, 260);
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
  }).formatToParts(date);
  const value = Object.fromEntries(parts.filter((part) => part.type !== "literal").map((part) => [part.type, part.value]));
  return `${value.year}-${value.month}-${value.day}T${value.hour}:${value.minute}:${value.second}+12:00`;
}
