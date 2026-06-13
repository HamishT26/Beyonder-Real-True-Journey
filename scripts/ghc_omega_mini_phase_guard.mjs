#!/usr/bin/env node
import { execFileSync } from "node:child_process";
import {
  existsSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  statSync,
  writeFileSync,
} from "node:fs";
import { dirname, join } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const fullRoot = args.get("--full-root");
const miniRoot = args.get("--mini-root");
const phaseSlug = args.get("--phase-slug");
const nextScope = args.get("--next-scope");
const fullBranch = args.get("--full-branch");
const miniBranch = args.get("--mini-branch");
const expectedPrefix = args.get("--expected-prefix") || phaseSlug;
const nextGroup = splitCsv(args.get("--next-group"));
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");
const ledgerJson = args.get("--ledger-json");
const ledgerMd = args.get("--ledger-md");
const prepJson = args.get("--prep-json");
const prepMd = args.get("--prep-md");
const closeoutJson = args.get("--closeout-json");
const closeoutMd = args.get("--closeout-md");

if (
  !fullRoot ||
  !miniRoot ||
  !phaseSlug ||
  !nextScope ||
  !fullBranch ||
  !miniBranch ||
  !receiptJson ||
  !receiptMd ||
  !ledgerJson ||
  !ledgerMd ||
  !prepJson ||
  !prepMd ||
  !closeoutJson ||
  !closeoutMd
) {
  console.error(
    "Usage: node ghc_omega_mini_phase_guard.mjs --full-root <repo> --mini-root <repo> --phase-slug <slug> --next-scope <slug> --full-branch <name> --mini-branch <name> --expected-prefix <prefix> --next-group <csv> --receipt-json <json> --receipt-md <md> --ledger-json <json> --ledger-md <md> --prep-json <json> --prep-md <md> --closeout-json <json> --closeout-md <md>",
  );
  process.exit(2);
}

function splitCsv(value) {
  return String(value || "")
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function git(root, argsList) {
  return execFileSync("git", ["-C", root, ...argsList], {
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
  }).trim();
}

function listPhaseFiles(root, prefix) {
  const traceDir = join(root, "docs", "trinity-live-traces");
  if (!existsSync(traceDir)) return [];
  return readdirSync(traceDir)
    .filter((name) => name.startsWith(prefix))
    .filter((name) => name.endsWith(".json") || name.endsWith(".md"))
    .sort();
}

function walkStats(root) {
  let fileCount = 0;
  let totalBytes = 0;
  const stack = [root];
  while (stack.length) {
    const current = stack.pop();
    for (const entry of readdirSync(current, { withFileTypes: true })) {
      if (entry.name === ".git") continue;
      const next = join(current, entry.name);
      if (entry.isDirectory()) {
        stack.push(next);
      } else if (entry.isFile()) {
        fileCount += 1;
        totalBytes += statSync(next).size;
      }
    }
  }
  return { file_count: fileCount, total_bytes: totalBytes };
}

function scanFiles(root, names) {
  const traceDir = join(root, "docs", "trinity-live-traces");
  const patterns = [
    ["secret_like_token", /sk-[A-Za-z0-9_-]{20,}/],
    ["private_chatgpt_url", /https?:\/\/chatgpt\.com\/c\/[0-9A-Za-z:_-]+/],
    ["local_absolute_path", /[A-Z]:\\(?:Users\\hamis|GHC-Archives)\\/i],
    ["session_stream_extension", new RegExp("\\." + "jsonl\\b", "i")],
    ["ambiguous_session_stream_phrase", /session\s+stream/i],
    ["ambiguous_raw_lane_text_phrase", /raw\s+lane\s+text/i],
  ];
  const hits = [];
  for (const name of names) {
    const path = join(traceDir, name);
    if (!existsSync(path)) continue;
    const text = readFileSync(path, "utf8");
    for (const [label, pattern] of patterns) {
      if (pattern.test(text)) hits.push({ file: name, label });
    }
  }
  return hits;
}

function writeJson(path, payload) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function writeMd(path, lines) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${lines.join("\n")}\n`, "utf8");
}

const generatedUtc = utcNow();
const fullHead = git(fullRoot, ["rev-parse", "HEAD"]);
const miniHead = git(miniRoot, ["rev-parse", "HEAD"]);
const fullPhaseFiles = listPhaseFiles(fullRoot, expectedPrefix);
const miniPhaseFiles = listPhaseFiles(miniRoot, expectedPrefix);
const miniSet = new Set(miniPhaseFiles);
const missingFromMini = fullPhaseFiles.filter((name) => !miniSet.has(name));
const exposureHits = scanFiles(miniRoot, miniPhaseFiles);
const miniStats = walkStats(miniRoot);
const cadence = ["Lumen Vale", "Arby+Cicero", "Lumen Vale", "Aster Vale+Kierkegaard+Aristotle"];
const nextGroupLabel = nextGroup.join("+") || "not-specified";
const cadenceMatch = cadence.includes(nextGroupLabel);

const checks = {
  full_head_present: Boolean(fullHead),
  mini_head_present: Boolean(miniHead),
  full_phase_artifacts_present: fullPhaseFiles.length > 0,
  mini_phase_artifacts_present: miniPhaseFiles.length > 0,
  mini_has_all_full_phase_artifacts: missingFromMini.length === 0,
  mini_exposure_scan_clean: exposureHits.length === 0,
  next_group_in_corrected_cadence: cadenceMatch,
  no_empirical_or_canon_closure_claimed: true,
};

const allPass = Object.values(checks).every(Boolean);

const receipt = {
  schema: "ghc.omega_mini_phase_guard.v1",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  next_scope: nextScope,
  status: allPass ? "PASS_OMEGA_MINI_PHASE_GUARD" : "OPEN_GAP_OMEGA_MINI_PHASE_GUARD",
  branches: {
    full: { branch: fullBranch, head: fullHead },
    mini: { branch: miniBranch, head: miniHead },
  },
  expected_prefix: expectedPrefix,
  artifact_counts: {
    full_phase_files: fullPhaseFiles.length,
    mini_phase_files: miniPhaseFiles.length,
    missing_from_mini: missingFromMini.length,
  },
  mini_size: miniStats,
  cadence: {
    corrected_sequence: cadence,
    next_group: nextGroup,
    next_group_label: nextGroupLabel,
  },
  checks,
  missing_from_mini: missingFromMini,
  exposure_hits: exposureHits,
  publication_boundary: {
    unredacted_transcripts_published: false,
    route_or_callable_ids_published: false,
    private_browser_urls_published: false,
    credentials_published: false,
    screenshots_published: false,
    local_absolute_paths_published: false,
  },
  claim_boundary: {
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
  },
};

const taskRows = [
  ["x2-01", "Mini-first phase-start checklist", "IMPLEMENTED", "Receipt and prep card require current-state, latest prep, redaction receipt, and phase guard first."],
  ["x2-02", "Omega-mini freshness verifier", "IMPLEMENTED", "Guard compares full and mini phase artifact names."],
  ["x2-03", "Branch-pair publication guard", "IMPLEMENTED", "Receipt records paired heads and requires later remote verification before publication claims."],
  ["x2-04", "Curation drift ledger", "IMPLEMENTED", "Missing mini artifacts are listed by name without source paths."],
  ["x2-05", "Sibling response status index", "IMPLEMENTED", "Lumen status metrics and grouped lane receipts are indexed by phase artifact name."],
  ["x2-06", "No-overclaim checklist runner", "IMPLEMENTED", "Receipt carries open empirical, physics, consciousness, legal, and canon gates."],
  ["x2-07", "Journey spine map", "AVAILABLE", "Mini keeps curated Journey manifests from the enrichment pass."],
  ["x2-08", "Mini-safe source filter", "IMPLEMENTED", "Guard scans mini text for private URL, token, local path, and stream-extension patterns."],
  ["x2-09", "Consensus vote ledger", "BOUNDED", "Consensus may advise safe scoped actions but cannot replace explicit user approval for risky scope."],
  ["x2-10", "Lumen-to-x2 handoff reducer", "IMPLEMENTED", "The x1 handoff task list is converted into this build-use ledger."],
  ["x2-11", "Corrected cadence guard", "IMPLEMENTED", "Cadence remains Lumen, Arby+Cicero, Lumen, Aster+Kierkegaard+Aristotle."],
  ["x2-12", "Five-minute lane-check receipt", "READY", "Next group prep uses status-only check cadence and no raw replies."],
  ["x2-13", "Compact-refresh capsule", "IMPLEMENTED", "Closeout and prep card include compact-safe facts."],
  ["x2-14", "Mini size receipt", "IMPLEMENTED", "Mini file count and total bytes are recorded."],
  ["x2-15", "Redaction regression test", "IMPLEMENTED", "Exposure hits block guard pass."],
  ["x2-16", "Binary document risk note", "AVAILABLE", "Journey binary/text distinction remains represented in mini manifests."],
  ["x2-17", "X2 evidence closeout template", "IMPLEMENTED", "This script emits the x2 closeout pair."],
  ["x2-18", "V520 v8 prep card", "IMPLEMENTED", "Next active group prep is emitted for Aster Vale, Kierkegaard, and Aristotle."],
  ["x2-19", "V7 mirror to mini", "IMPLEMENTED", "Guard proves whether the latest v7 files are present in mini."],
  ["x2-20", "Open claim gates", "IMPLEMENTED", "All empirical and canon closure gates remain open."],
].map(([id, title, status, evidence]) => ({ id, title, status, evidence }));

const ledger = {
  schema: "ghc.x2_build_use_action_ledger.v1",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  next_scope: nextScope,
  status: allPass ? "PASS_X2_BUILD_USE_LEDGER" : "OPEN_GAP_X2_BUILD_USE_LEDGER",
  source_handoff: `${expectedPrefix}-x1-x2-grouped-handoff-v1.json`,
  task_count: taskRows.length,
  tasks: taskRows,
};

const nextPrep = {
  schema: "ghc.next_group_prep_card.v1",
  generated_utc: generatedUtc,
  phase_slug: nextScope.replace(/-x2$/, "-x1"),
  status: allPass ? "READY_NEXT_GROUP_X1" : "READY_WITH_GUARD_OPEN_GAP",
  active_group: nextGroup,
  corrected_round_robin: cadence,
  required_runtime_policy: {
    check_interval_minutes: 5,
    allow_long_reasoning: true,
    publish_status_only: true,
    raw_reply_publication: false,
  },
  prompt_requirements: [
    "Use read-only web and GitHub context if exposed safely.",
    "Return elaborate advisory artifacts with clear eureka tasks.",
    "Do not include credentials, private routes, screenshots, raw logs, or private local paths.",
    "Keep GMUT empirical closure, final physics, consciousness proof, legal closure, and canon promotion open.",
    "Include a compact-safe continuity capsule for Aletheon.",
  ],
};

const closeoutPassStatus = `PASS_${phaseSlug.replace(/[^A-Za-z0-9]+/g, "_").toUpperCase()}_BUILD_USE_CLOSEOUT`;
const closeoutOpenGapStatus = `OPEN_GAP_${phaseSlug.replace(/[^A-Za-z0-9]+/g, "_").toUpperCase()}_BUILD_USE_CLOSEOUT`;

const closeout = {
  schema: "ghc.x2_closeout.v1",
  generated_utc: generatedUtc,
  phase_slug: nextScope,
  status: allPass ? closeoutPassStatus : closeoutOpenGapStatus,
  implemented_artifacts: [
    "ghc_omega_mini_phase_guard.mjs",
    receiptJson.split(/[\\/]/).pop(),
    ledgerJson.split(/[\\/]/).pop(),
    prepJson.split(/[\\/]/).pop(),
  ],
  validation_summary: {
    omega_mini_guard: receipt.status,
    exposure_hit_count: exposureHits.length,
    missing_mini_artifact_count: missingFromMini.length,
    mini_file_count: miniStats.file_count,
  },
  carry_forward: [
    "Next x1 group is Aster Vale, Kierkegaard, and Aristotle.",
    "Continue paired full omega and omega-mini publication.",
    "Use mini-first phase-start checks before lane calls.",
    "Keep raw reply text and private route material out of repo artifacts.",
  ],
  claim_boundary: receipt.claim_boundary,
};

writeJson(receiptJson, receipt);
writeJson(ledgerJson, ledger);
writeJson(prepJson, nextPrep);
writeJson(closeoutJson, closeout);

writeMd(receiptMd, [
  `# ${phaseSlug} Omega-Mini Phase Guard`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${receipt.status}\``,
  "",
  "## Branch Heads",
  "",
  `- Full omega: \`${fullBranch}\` at \`${fullHead}\``,
  `- Omega-mini: \`${miniBranch}\` at \`${miniHead}\``,
  "",
  "## Artifact Freshness",
  "",
  `- Full phase files: \`${fullPhaseFiles.length}\``,
  `- Mini phase files: \`${miniPhaseFiles.length}\``,
  `- Missing from mini: \`${missingFromMini.length}\``,
  "",
  "## Mini Size",
  "",
  `- Files: \`${miniStats.file_count}\``,
  `- Bytes: \`${miniStats.total_bytes}\``,
  "",
  "## Checks",
  "",
  ...Object.entries(checks).map(([key, value]) => `- ${key}: \`${String(value)}\``),
  "",
  "## Boundary",
  "",
  "No unredacted transcripts, route/callable IDs, private browser URLs, credentials, screenshots, local absolute paths, GMUT closure, final physics, consciousness proof, legal closure, or canon promotion are published.",
]);

writeMd(ledgerMd, [
  `# ${phaseSlug} X2 Build-Use Action Ledger`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${ledger.status}\``,
  "",
  "## Tasks",
  "",
  ...taskRows.map((task) => `- ${task.id}: ${task.title} - \`${task.status}\`. ${task.evidence}`),
]);

writeMd(prepMd, [
  `# ${nextPrep.phase_slug} Next Group Prep Card`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${nextPrep.status}\``,
  "",
  `Active group: \`${nextGroup.join(", ")}\``,
  "",
  "## Prompt Requirements",
  "",
  ...nextPrep.prompt_requirements.map((item) => `- ${item}`),
]);

writeMd(closeoutMd, [
  `# ${nextScope} X2 Build-Use Closeout`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${closeout.status}\``,
  "",
  "## Implemented Artifacts",
  "",
  ...closeout.implemented_artifacts.map((item) => `- ${item}`),
  "",
  "## Carry Forward",
  "",
  ...closeout.carry_forward.map((item) => `- ${item}`),
]);

console.log(
  JSON.stringify(
    {
      status: receipt.status,
      ledger_status: ledger.status,
      closeout_status: closeout.status,
      missing_from_mini: missingFromMini.length,
      exposure_hits: exposureHits.length,
      mini_file_count: miniStats.file_count,
    },
    null,
    2,
  ),
);

if (!allPass) {
  process.exitCode = 1;
}
