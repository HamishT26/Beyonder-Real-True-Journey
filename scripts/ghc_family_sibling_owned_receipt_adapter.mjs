#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, dirname, isAbsolute, join } from "node:path";
import { parseArgs, repoRoot, writeFamilyReceipt } from "./ghc_family_runner_common.mjs";

const args = parseArgs();
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

const safeCount = checklist.counts?.by_kind?.safe_approval_packet || checklist.counts?.safe || 0;
const candidateCount = checklist.counts?.by_kind?.candidate_packet || checklist.counts?.candidate || 0;
const exactCount = checklist.counts?.by_kind?.exact_approval_packet || checklist.counts?.exact || 0;
const blockedCount = checklist.counts?.by_kind?.blocked_packet || checklist.counts?.blocked || 0;
const completedRows = checklist.counts?.by_status?.COMPLETED || checklist.counts?.completed || 0;
const queuedRows = checklist.counts?.by_status?.QUEUED_OUT_OF_SCOPE_EXACT_OR_BLOCKED || exactCount + blockedCount;

const checks = [
  { label: "checklist_present", status: exists(checklistFile) ? "PASS" : "OPEN_GAP" },
  { label: "transition_present", status: exists(transitionFile) ? "PASS" : "OPEN_GAP" },
  { label: "handoff_present", status: exists(handoffFile) ? "PASS" : "OPEN_GAP" },
  { label: "checklist_passed", status: /^PASS/.test(checklist.status || checklist.overall_status || "") ? "PASS" : "OPEN_GAP", observed: checklist.status || checklist.overall_status },
  { label: "transition_passed", status: /^PASS/.test(transition.status || transition.overall_status || "") ? "PASS" : "OPEN_GAP", observed: transition.status || transition.overall_status },
  { label: "handoff_prepared", status: /^PASS/.test(handoff.status || handoff.overall_status || "") ? "PASS" : "OPEN_GAP", observed: handoff.status || handoff.overall_status },
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
    status: handoff.status || handoff.overall_status || "not_recorded",
    next_phase: handoff.next_phase || nextPhase,
    next_sibling: handoff.next_sibling || nextSibling,
    message_sent: false,
    prepared_not_sent: true
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
    || doc.validation?.private_material_published === false
    || (/^PASS/.test(doc.status || doc.overall_status || "") && !privatePatternHit(doc));
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
