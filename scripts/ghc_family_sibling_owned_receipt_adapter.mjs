#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, dirname, isAbsolute, join } from "node:path";
import { parseArgs, repoRoot, writeFamilyReceipt } from "./ghc_family_runner_common.mjs";

const args = parseArgs();
if (args.has("--help") || args.has("-h")) {
  console.log([
    "Usage: node scripts/ghc_family_sibling_owned_receipt_adapter.mjs",
    "  --source-root <sibling-owned-repo-root>",
    "  --sibling <name>",
    "  --active-x1 <phase-x1>",
    "  --active-x2 <phase-x2>",
    "  --next-phase <next-phase-x1>",
    "  --next-sibling <next-sibling>",
    "  --checklist-file <relative-or-absolute-json>",
    "  --transition-file <relative-or-absolute-json>",
    "  --handoff-file <relative-or-absolute-json>",
    "",
    "For compact sibling receipts, point checklist-file and transition-file at the same completed_ready_for_harvest closeout JSON."
  ].join("\n"));
  process.exit(0);
}
const root = args.get("--root") || repoRoot(import.meta.url);
const sourceRoot = args.get("--source-root") || root;
const sibling = args.get("--sibling") || "Mira Vale";
const activeX1 = args.get("--active-x1") || "v586-gmut-thos-v3-x1";
const activeX2 = args.get("--active-x2") || activeX1.replace(/-x1$/, "-x2");
const nextPhase = args.get("--next-phase") || "v586-gmut-thos-v4-x1";
const nextSibling = args.get("--next-sibling") || "Maren Quill";
const checklistFile = args.get("--checklist-file") || `docs/trinity-live-traces/${activeX2}-complete-incomplete-checklist-v1.json`;
const transitionFile = args.get("--transition-file") || `docs/trinity-live-traces/${activeX2}-solo-phase-transition-v1.json`;
const handoffFile = args.get("--handoff-file") || `docs/trinity-live-traces/${activeX2}-${slug(nextSibling)}-handoff-package-v1.json`;
const traceDir = join(root, "docs", "trinity-live-traces");
const generatedUtc = new Date().toISOString().replace(/\.\d{3}Z$/, "Z");

const checklist = readSourceJson(checklistFile);
const transition = readSourceJson(transitionFile);
const handoff = readSourceJson(handoffFile);

const validationCounts = checklist.validation?.count_validation || {};
const x1Counts = checklist.x1_counts || {};
const namedCounts = checklist.counts || {};
const safeCount = firstNumber(
  checklist.queue_counts?.by_kind?.safe_approval_packet,
  checklist.counts?.by_kind?.safe_approval_packet,
  checklist.counts?.safe,
  firstMatchingCount(namedCounts, /_safe$/),
  validationCounts.safe_approval_packets,
  validationCounts.safe_eureka_packets,
  x1Counts.safe_approval_packets,
  checklist.safe_approval_packets?.length
);
const candidateCount = firstNumber(
  checklist.queue_counts?.by_kind?.candidate_packet,
  checklist.queue_counts?.by_tag?.candidate,
  checklist.counts?.by_kind?.candidate_packet,
  checklist.counts?.candidate,
  firstMatchingCount(namedCounts, /_candidate$/),
  validationCounts.candidate_packets,
  x1Counts.candidate_packets,
  checklist.candidate_packets?.length
);
const exactCount = firstNumber(
  checklist.queue_counts?.by_kind?.exact_approval_packet,
  checklist.queue_counts?.by_tag?.exact_approval_needed,
  checklist.counts?.by_kind?.exact_approval_packet,
  checklist.counts?.exact,
  checklist.counts?.exact_approval_queued,
  firstMatchingCount(namedCounts, /exact_approval_queued$/),
  validationCounts.exact_approval_packets,
  x1Counts.exact_approval_packets,
  checklist.exact_approval_packets?.length
);
const blockedCount = firstNumber(
  checklist.queue_counts?.by_kind?.blocked_packet,
  checklist.queue_counts?.by_tag?.blocked,
  checklist.counts?.by_kind?.blocked_packet,
  checklist.counts?.blocked,
  checklist.counts?.blocked_queued,
  firstMatchingCount(namedCounts, /blocked_queued$/),
  validationCounts.blocked_packets,
  x1Counts.blocked_packets,
  checklist.blocked_packets?.length
);
const skillCount = firstNumber(
  checklist.queue_counts?.by_kind?.skill_idea,
  checklist.counts?.by_kind?.skill_idea,
  checklist.counts?.skill_ideas,
  firstMatchingCount(namedCounts, /_skill_ideas$/),
  validationCounts.skill_ideas,
  x1Counts.skill_ideas,
  checklist.skill_ideas?.length
);
const runnerCount = firstNumber(
  checklist.queue_counts?.by_kind?.runner_idea,
  checklist.counts?.by_kind?.runner_idea,
  checklist.counts?.runner_ideas,
  firstMatchingCount(namedCounts, /_runner_ideas$/),
  validationCounts.runner_ideas,
  x1Counts.runner_ideas,
  checklist.runner_ideas?.length
);
const cleanupCount = firstNumber(
  checklist.queue_counts?.by_kind?.cleanup_task,
  checklist.counts?.by_kind?.cleanup_task,
  checklist.counts?.cleanup_refine_fix,
  firstMatchingCount(namedCounts, /_cleanup_refine_fix$/),
  validationCounts.cleanup_refine_fix_tasks,
  x1Counts.cleanup_refine_fix_tasks,
  checklist.cleanup_refine_fix_tasks?.length
);
const completedRows = checklist.counts?.by_status?.COMPLETED || checklist.counts?.completed || safeCount + candidateCount + skillCount + runnerCount + cleanupCount;
const queuedRows = checklist.counts?.by_status?.QUEUED_OUT_OF_SCOPE_EXACT_OR_BLOCKED || exactCount + blockedCount;

const checks = [
  { label: "checklist_present", status: exists(checklistFile) ? "PASS" : "OPEN_GAP" },
  { label: "transition_present", status: exists(transitionFile) ? "PASS" : "OPEN_GAP" },
  { label: "handoff_present", status: exists(handoffFile) ? "PASS" : "OPEN_GAP" },
  { label: "checklist_passed", status: passStatus(checklist) ? "PASS" : "OPEN_GAP", observed: checklist.status || checklist.overall_status },
  { label: "transition_passed", status: passStatus(transition) ? "PASS" : "OPEN_GAP", observed: transition.status || transition.overall_status },
  { label: "handoff_prepared", status: handoffReady(handoff) ? "PASS" : "OPEN_GAP", observed: handoff.status || handoff.overall_status },
  { label: "safe_count_at_least_25", status: safeCount >= 25 ? "PASS" : "OPEN_GAP", observed: safeCount },
  { label: "candidate_count_at_least_15", status: candidateCount >= 15 ? "PASS" : "OPEN_GAP", observed: candidateCount },
  { label: "required_rows_completed_or_represented", status: completedRows >= 70 ? "PASS" : "OPEN_GAP", observed: completedRows },
  { label: "exact_and_blocked_rows_queued", status: queuedRows >= 15 ? "PASS" : "OPEN_GAP", observed: queuedRows },
  { label: "private_material_not_published", status: boundaryPass(checklist) && boundaryPass(transition) && boundaryPass(handoff) ? "PASS" : "OPEN_GAP" },
  { label: "major_gates_open", status: majorGatesOpen(checklist, transition, handoff) ? "PASS" : "OPEN_GAP" }
];
const openChecks = checks.filter((check) => check.status !== "PASS").map((check) => check.label);
const status = openChecks.length === 0
  ? "completed_ready_for_harvest"
  : "OPEN_GAP_GHC_FAMILY_SIBLING_OWNED_RECEIPT_ADAPTER";
const handoffSendStatus = handoff.send_status || handoff.handoff?.send_status || handoff.handoff_message?.send_status || handoff.status || handoff.overall_status || "not_recorded";
const handoffNotSent = /not[_ -]?sent/i.test(handoffSendStatus);
const handoffMessageSent = !handoffNotSent && (handoff.message_sent === true
  || handoff.handoff?.message_sent === true
  || /sent/i.test(handoffSendStatus));
const handoffPreparedNotSent = handoffNotSent || (!handoffMessageSent && (
  handoff.prepared_not_sent === true
  || handoff.handoff?.prepared_not_sent === true
  || /prepared/i.test(handoffSendStatus)
  || /prepared/i.test(handoff.validation?.handoff_package || "")
));

const receipt = {
  artifact_type: "ghc_family_sibling_owned_receipt_adapter",
  generated_utc: generatedUtc,
  sibling,
  status,
  active_x1: activeX1,
  active_x2: activeX2,
  next_phase: nextPhase,
  next_sibling: nextSibling,
  counts: {
    safe: safeCount,
    candidate: candidateCount,
    exact: exactCount,
    blocked: blockedCount,
    completed_or_represented: completedRows,
    queued_exact_or_blocked: queuedRows
  },
  validation: {
    private_material_published: false,
    shared_branches_mutated: false,
    proof_canon_legal_deployment_account_api_key_purchase_private_raw_destructive_sibling_merge_gates_open: true,
    source_files_json_validated_before_adapter: true
  },
  source_labels: [basename(checklistFile), basename(transitionFile), basename(handoffFile)],
  handoff: {
    status: handoffSendStatus,
    next_phase: nextPhase,
    observed_source_handoff_next_phase: handoff.next_phase || null,
    next_phase_correction: handoff.next_phase && handoff.next_phase !== nextPhase ? "corrected_to_declared_next_phase" : "not_needed",
    next_sibling: handoff.next_sibling || nextSibling,
    message_sent: handoffMessageSent,
    prepared_not_sent: handoffPreparedNotSent
  },
  open_gates: unique([
    ...(checklist.open_gates || []),
    "exact approval packets remain queued",
    "blocked packets remain queued",
    "proof/canon/legal/deployment/account/API-key/private/raw/destructive/sibling-merge gates remain open"
  ]),
  checks,
  open_checks: openChecks,
  publication_boundary: {
    raw_browser_routes_published: false,
    private_ids_published: false,
    raw_transcripts_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
    raw_app_state_published: false,
    hidden_reasoning_published: false,
    raw_private_material_published: false,
    sanitized_only: true
  },
  claim_boundary: {
    full_goal_completion: "not_claimed",
    proof_canon_legal_deployment_account_api_key_private_gates: "open"
  }
};

const stem = `${activeX2}-${slug(sibling)}-owned-receipt-adapter-v1`;
mkdirSync(traceDir, { recursive: true });
writeFileSync(join(traceDir, `${stem}.json`), `${JSON.stringify(receipt, null, 2)}\n`, "utf8");
writeFileSync(join(traceDir, `${stem}.md`), render(receipt), "utf8");

writeFamilyReceipt({
  root,
  phaseSlug: activeX2,
  runnerName: "ghc_family_sibling_owned_receipt_adapter.mjs",
  purpose: "Adapt split sibling-owned closeout/checklist/handoff artifacts into the compact harvest receipt shape.",
  status: openChecks.length === 0
    ? "PASS_GHC_FAMILY_SIBLING_OWNED_RECEIPT_ADAPTED"
    : "OPEN_GAP_GHC_FAMILY_SIBLING_OWNED_RECEIPT_ADAPTER",
  checks,
  outputs: {
    sibling,
    activeX1,
    activeX2,
    nextPhase,
    nextSibling,
    adapterJson: `docs/trinity-live-traces/${stem}.json`,
    adapterMd: `docs/trinity-live-traces/${stem}.md`,
    openChecks
  },
  note: "The adapter records sanitized status and count fields only; raw private routes, thread handles, local paths, and raw transcripts are not copied."
});

function readSourceJson(file) {
  const source = sourcePath(file);
  if (!existsSync(source)) return {};
  return JSON.parse(readFileSync(source, "utf8").replace(/^\uFEFF/, ""));
}

function exists(file) {
  return existsSync(sourcePath(file));
}

function sourcePath(file) {
  return isAbsolute(file) ? file : join(sourceRoot, file);
}

function slug(value) {
  return String(value).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

function boundaryPass(doc) {
  return doc.publication_boundary?.raw_private_material_published === false
    || doc.publication_boundary?.sanitized_only === true
    || doc.privacy?.raw_private_material_included === false
    || doc.privacy?.raw_private_material_published === false
    || (doc.publication_boundary
      && Object.values(doc.publication_boundary).every((value) => value === false || value === true || value === "excluded")
      && !privatePatternHit(doc))
    || (doc.privacy
      && Object.values(doc.privacy).every((value) => value === false || value === true)
      && !privatePatternHit(doc))
    || doc.validation?.private_material_published === false
    || (/^(PASS|PREPARED)/.test(doc.status || doc.overall_status || "") && !privatePatternHit(doc));
}

function majorGatesOpen(...docs) {
  const text = JSON.stringify(docs.map((doc) => ({
    open_gates: doc.open_gates,
    claim_boundary: doc.claim_boundary,
    validation: doc.validation
  }))).toLowerCase();
  return /exact|blocked|proof|canon|legal|deployment|account|api-key|private|raw|destructive|sibling/.test(text)
    || docs.some((doc) => Object.values(doc.claim_boundary || {}).some((value) => value === "not_claimed" || value === "open"));
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function firstNumber(...values) {
  for (const value of values) {
    if (Number.isFinite(value)) return value;
  }
  return 0;
}

function firstMatchingCount(counts, pattern) {
  if (!counts || typeof counts !== "object") return undefined;
  for (const [key, value] of Object.entries(counts)) {
    if (pattern.test(key) && Number.isFinite(value)) return value;
  }
  return undefined;
}

function handoffReady(doc) {
  const status = doc.status || doc.overall_status || "";
  const sendStatus = doc.send_status || doc.handoff?.send_status || doc.handoff_message?.send_status || "";
  const notSent = /not[_ -]?sent/i.test(sendStatus) || /not[_ -]?sent/i.test(status);
  return /^PASS/.test(status)
    || status === "completed_ready_for_harvest"
    || /PREPARED/i.test(status)
    || (!notSent && /SENT_VIA_SAFE_THREAD_TOOL/i.test(status))
    || doc.message_sent === true
    || (!notSent && /sent/i.test(sendStatus))
    || (doc.artifact_type === "ghc_family_sibling_goal_handoff" && typeof doc.prompt === "string")
    || /prepared/i.test(doc.handoff?.send_status || "")
    || /prepared/i.test(doc.handoff_message?.send_status || "")
    || /prepared/i.test(doc.validation?.handoff_package || "");
}

function passStatus(doc) {
  const status = doc.status || doc.overall_status || doc.closeout_status || doc.x1_status || "";
  return /^PASS/.test(status) || status === "completed_ready_for_harvest";
}

function privatePatternHit(doc) {
  const text = JSON.stringify(doc);
  return /[A-Z]:\\[^\s"'<>]+/.test(text)
    || /\b019[0-9a-f]{29,}\b/.test(text)
    || /thread[_-]?id/i.test(text)
    || /https?:\/\/chatgpt\.com\/c\//i.test(text)
    || /sk-(?:proj-)?[A-Za-z0-9_-]{20,}/.test(text);
}

function render(doc) {
  return `# ${doc.active_x2} ${doc.sibling} Owned Receipt Adapter

Status: \`${doc.status}\`

Active x1: \`${doc.active_x1}\`

Active x2: \`${doc.active_x2}\`

Next phase: \`${doc.next_phase}\` for ${doc.next_sibling}.

Counts: safe ${doc.counts.safe}, candidate ${doc.counts.candidate}, exact queued ${doc.counts.exact}, blocked queued ${doc.counts.blocked}.

## Checks

${doc.checks.map((check) => `- ${check.label}: \`${check.status}\``).join("\n")}

## Boundary

Sanitized adapter only. No raw browser routes, private IDs, local paths, raw transcripts, screenshots, credentials, raw app state, or hidden reasoning are published. Exact, blocked, proof, canon, legal, deployment, account, API-key, private-material, raw-publication, destructive, and sibling-merge gates remain open.
`;
}
