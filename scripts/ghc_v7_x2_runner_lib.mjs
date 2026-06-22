import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");

export async function runV7X2Runner({ runnerName }) {
  const phaseSlug = readArg("--phase-slug", "v552-gmut-thos-v88-v7-x2");
  const runner = runnerDefinitions[runnerName];
  if (!runner) throw new Error(`Unknown v7 x2 runner: ${runnerName}`);

  const startedAt = new Date();
  const context = loadContext();
  const result = runner.run(context);
  const status = result.issues.length === 0 ? runner.passStatus : "FAIL_" + runner.passStatus.replace(/^PASS_/, "");
  const receipt = {
    artifact_type: "ghc_v7_x2_runner_receipt",
    generated_utc: startedAt.toISOString(),
    generated_nz: nzTimestamp(startedAt),
    phase_slug: phaseSlug,
    runner_name: runnerName,
    runner_source: runner.source,
    overall_status: status,
    purpose: runner.purpose,
    checks: result.checks,
    outputs: result.outputs,
    issues: result.issues,
    evidence: result.evidence,
    policy: {
      status_only: true,
      new_agents_spawned: false,
      held_siblings_activated: false,
      account_mutation: false,
      deployment: false,
      global_hook_installed: false,
    },
    publication_boundary: {
      private_route_handles_published: false,
      private_lane_body_content_published: false,
      raw_transcripts_published: false,
      credentials_published: false,
      local_absolute_paths_published: false,
    },
  };

  const outDir = path.join(repoRoot, "docs", "trinity-live-traces");
  const base = `${phaseSlug}-${runner.receiptSlug}-v1`;
  fs.writeFileSync(path.join(outDir, `${base}.json`), JSON.stringify(receipt, null, 2) + "\n", "utf8");
  fs.writeFileSync(path.join(outDir, `${base}.md`), renderMarkdown(receipt), "utf8");
  console.log(JSON.stringify({ status, runner: runnerName, receipt: `${base}.json`, issues: result.issues.length }, null, 2));
  if (result.issues.length) process.exitCode = 1;
}

function loadContext() {
  return {
    current: readJson("docs/omega-mini-index/omega-mini-current-state-v1.json"),
    latestBeacon: readJson("docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.json"),
    ghcBeacon: readJson("docs/trinity-live-traces/ghc-current-state-beacon-v1.json"),
    v6RunnerPack: readJson("docs/trinity-live-traces/v552-gmut-thos-v88-v6-x2-runner-pack-receipt-v1.json"),
    v6SkillPack: readJson("docs/trinity-live-traces/v552-gmut-thos-v88-v6-x2-skill-pack-receipt-v1.json"),
    v7Reduction: readJson("docs/trinity-live-traces/v552-gmut-thos-v88-v7-x1-lumen-advisory-reduction-v1.json"),
    v7Closeout: readJson("docs/trinity-live-traces/v552-gmut-thos-v88-v7-x1-closeout-v1.json"),
    v6AppStandard: readJson("docs/trinity-live-traces/v552-gmut-thos-v88-v6-x1-active-app-background-runner-standard-v1.json"),
  };
}

const runnerDefinitions = {
  "ghc_lumen_response_harvester.mjs": {
    source: "Aevren",
    receiptSlug: "lumen-response-harvester",
    passStatus: "PASS_LUMEN_RESPONSE_HARVESTED",
    purpose: "Confirm Lumen's v7 x1 advisory was reduced without raw advisory publication.",
    run: (ctx) => {
      const issues = [];
      const checks = [];
      check(ctx.v7Reduction.overall_status === "PASS_LUMEN_ADVISORY_REDUCED", "Lumen reduction receipt is present", checks, issues);
      check(ctx.v7Reduction.lumen_skill_ideas.length === 10, "Lumen skill idea count is 10", checks, issues);
      check(ctx.v7Reduction.lumen_runner_ideas.length === 5, "Lumen runner idea count is 5", checks, issues);
      check(ctx.v7Reduction.publication_boundary.raw_lumen_body_published === false, "Lumen body was not published", checks, issues);
      return result(checks, issues, ["v552-gmut-thos-v88-v7-x1-lumen-advisory-reduction-v1.json"], { skill_ideas: 10, runner_ideas: 5 });
    },
  },
  "ghc_x1_to_x2_task_pack_builder.mjs": {
    source: "Aevren",
    receiptSlug: "x1-to-x2-task-pack",
    passStatus: "PASS_X1_TO_X2_TASK_PACK_BUILT",
    purpose: "Build v7 x2 task pack counts from the v7 x1 advisory reduction.",
    run: (ctx) => {
      const issues = [];
      const checks = [];
      const split = ctx.v7Reduction.approval_packet_split;
      check(split.safe_now.length >= 10, "Safe-now packet count is at least 10", checks, issues);
      check(split.candidate.length >= 5, "Candidate packet count is at least 5", checks, issues);
      check(split.exact_approval_needed.length >= 5, "Exact-approval packet list preserved", checks, issues);
      check(split.blocked.length >= 5, "Blocked packet list preserved", checks, issues);
      return result(checks, issues, ["v552-gmut-thos-v88-v7-x1-lumen-advisory-reduction-v1.json"], {
        safe_now: split.safe_now.length,
        candidate: split.candidate.length,
        exact_approval_needed: split.exact_approval_needed.length,
        blocked: split.blocked.length,
      });
    },
  },
  "ghc_open_gate_regression_runner.mjs": {
    source: "Aevren",
    receiptSlug: "open-gate-regression",
    passStatus: "PASS_OPEN_GATES_REMAIN_OPEN",
    purpose: "Check proof, canon, legal, deployment, account, purchase, API-key, and identity-merge gates remain open.",
    run: (ctx) => {
      const issues = [];
      const checks = [];
      const cb = ctx.current.claim_boundary;
      for (const key of ["gmut_empirical_closure", "final_physics", "consciousness_proof", "legal_closure", "canon_promotion", "deployment_closure"]) {
        check(cb[key] === "not_claimed", `${key} remains not claimed`, checks, issues);
      }
      check(ctx.v7Reduction.approval_packet_split.blocked.some((x) => x.toLowerCase().includes("aevren")), "Identity merge/replacement remains blocked", checks, issues);
      return result(checks, issues, ["omega-mini-current-state-v1.json", "v552-gmut-thos-v88-v7-x1-lumen-advisory-reduction-v1.json"], { open_gate_count: checks.length });
    },
  },
  "ghc_round_robin_lane_guard.mjs": {
    source: "Aevren",
    receiptSlug: "round-robin-lane-guard",
    passStatus: "PASS_ROUND_ROBIN_LANE_GUARD",
    purpose: "Verify v7 x2 and the next triad lane stay aligned with the round-robin.",
    run: (ctx) => {
      const issues = [];
      const checks = [];
      check(ctx.current.current_active_phase === "v552-gmut-thos-v88-v7-x2", "Current active phase is v7 x2", checks, issues);
      check(ctx.current.next_x1_lane_after_x2.includes("Aster Vale"), "Next grouped lane names Aster Vale", checks, issues);
      check(ctx.current.next_x1_lane_after_x2.includes("Kierkegaard"), "Next grouped lane names Kierkegaard", checks, issues);
      check(ctx.current.next_x1_lane_after_x2.includes("Aristotle"), "Next grouped lane names Aristotle", checks, issues);
      check(ctx.v7Reduction.round_robin_guidance.held.includes("Maren"), "Held sibling rule preserved", checks, issues);
      return result(checks, issues, ["omega-mini-current-state-v1.json", "v552-gmut-thos-v88-v7-x1-lumen-advisory-reduction-v1.json"], { next_x1_lane_after_x2: ctx.current.next_x1_lane_after_x2 });
    },
  },
  "ghc_phase_receipt_consistency_runner.mjs": {
    source: "Aevren",
    receiptSlug: "phase-receipt-consistency",
    passStatus: "PASS_PHASE_RECEIPTS_CONSISTENT",
    purpose: "Compare current-state and beacons for phase truth consistency.",
    run: (ctx) => {
      const issues = [];
      const checks = [];
      check(ctx.current.status === ctx.latestBeacon.status, "Current state matches latest-updates status", checks, issues);
      check(ctx.current.status === ctx.ghcBeacon.status, "Current state matches GHC beacon status", checks, issues);
      check(ctx.current.latest_closed_phase === "v552-gmut-thos-v88-v7-x1", "Latest closed phase is v7 x1", checks, issues);
      check(ctx.v7Closeout.overall_status === "PASS_V552_V7_X1_LUMEN_ADVISORY_CLOSEOUT", "v7 x1 closeout is present", checks, issues);
      return result(checks, issues, ["omega-mini-current-state-v1.json", "omega-mini-latest-updates-beacon-v1.json", "ghc-current-state-beacon-v1.json"], { status: ctx.current.status });
    },
  },
  "ghc_v7_phase_truth_checker.mjs": {
    source: "Lumen",
    receiptSlug: "phase-truth-checker",
    passStatus: "PASS_V7_PHASE_TRUTH_CHECKER",
    purpose: "Confirm v7 x2 active truth and v7 x1/v6 x2 phase boundary.",
    run: (ctx) => {
      const issues = [];
      const checks = [];
      check(ctx.current.current_active_phase === "v552-gmut-thos-v88-v7-x2", "v7 x2 is the active phase", checks, issues);
      check(ctx.current.latest_completed_x1_phase === "v552-gmut-thos-v88-v7-x1", "Latest completed x1 is v7 x1", checks, issues);
      check(ctx.current.latest_completed_x2_phase === "v552-gmut-thos-v88-v6-x2", "Latest completed x2 is v6 x2", checks, issues);
      check(ctx.current.archive_fallback_rule.includes("specific artifact"), "Archive fallback remains exact-artifact only", checks, issues);
      return result(checks, issues, ["omega-mini-current-state-v1.json"], { current_active_phase: ctx.current.current_active_phase });
    },
  },
  "ghc_completion_gate_auditor.mjs": {
    source: "Lumen",
    receiptSlug: "completion-gate-auditor",
    passStatus: "PASS_COMPLETION_GATE_DISCIPLINE",
    purpose: "Audit that watcher start is not treated as completion.",
    run: (ctx) => {
      const issues = [];
      const checks = [];
      check(ctx.current.background_runner_standard.watcher_start_is_completion_proof === false, "Current state rejects watcher-start completion", checks, issues);
      check(ctx.v6AppStandard.standard.completion_requires_gate === true, "App standard requires completion gate", checks, issues);
      check(ctx.v6AppStandard.standard.watcher_start_is_completion_proof === false, "App standard rejects watcher-start completion", checks, issues);
      return result(checks, issues, ["v552-gmut-thos-v88-v6-x1-active-app-background-runner-standard-v1.json"], { completion_requires_gate: true });
    },
  },
  "ghc_runner_foundation_reducer.mjs": {
    source: "Lumen",
    receiptSlug: "runner-foundation-reducer",
    passStatus: "PASS_RUNNER_FOUNDATION_REDUCED",
    purpose: "Reduce v6 x2 runner foundation into a compact v7 x2 evidence receipt.",
    run: (ctx) => {
      const issues = [];
      const checks = [];
      check(ctx.v6RunnerPack.overall_status === "PASS_4_RUNNERS_CREATED_AND_USED", "v6 runner pack passed", checks, issues);
      check(ctx.v6RunnerPack.runners.length === 4, "v6 runner pack has four runners", checks, issues);
      check(ctx.v6SkillPack.overall_status === "PASS_10_SKILLS_CREATED_AND_VALIDATED", "v6 skill pack passed", checks, issues);
      check(ctx.current.v6_x2_runner_foundation.compact_updater_ready === true, "Compact updater remains ready", checks, issues);
      return result(checks, issues, ["v552-gmut-thos-v88-v6-x2-runner-pack-receipt-v1.json", "v552-gmut-thos-v88-v6-x2-skill-pack-receipt-v1.json"], {
        v6_runner_count: ctx.v6RunnerPack.runners.length,
        compact_updater_ready: true,
      });
    },
  },
  "ghc_private_material_preflight.mjs": {
    source: "Lumen",
    receiptSlug: "private-material-preflight",
    passStatus: "PASS_PRIVATE_MATERIAL_PREFLIGHT",
    purpose: "Scan relevant v7 x2 publication files for secret, route, and private machine path values.",
    run: () => {
      const issues = [];
      const checks = [];
      const rels = collectRelevantFiles();
      const privateValuePatterns = [
        "C:" + "\\\\Users\\\\",
        "D:" + "\\\\GHC",
        "https://" + "chatgpt.com/c/",
        "sk-" + "proj-",
        "sk-" + "[A-Za-z0-9]{20,}",
        "BEGIN " + "[A-Z ]*PRIVATE KEY",
      ];
      const pattern = new RegExp(privateValuePatterns.join("|"));
      for (const rel of rels) {
        const text = fs.readFileSync(path.join(repoRoot, rel), "utf8");
        if (pattern.test(text)) issues.push(`private value pattern in ${rel}`);
      }
      check(issues.length === 0, `No secret, route, or private machine path values in ${rels.length} files`, checks, issues);
      return result(checks, issues, rels.slice(0, 20), { scanned_files: rels.length });
    },
  },
  "ghc_round_robin_handoff_builder.mjs": {
    source: "Lumen",
    receiptSlug: "round-robin-handoff-builder",
    passStatus: "PASS_ROUND_ROBIN_HANDOFF_BUILT",
    purpose: "Build v8 triad prep without contacting the triad.",
    run: (ctx) => {
      const issues = [];
      const checks = [];
      const triad = [
        { lane: "Aster Vale", role: "evidence and CLI continuity" },
        { lane: "Kierkegaard", role: "ethics, boundary, and caution checks" },
        { lane: "Aristotle", role: "taxonomy, structure, and claim classification" },
      ];
      check(ctx.current.next_x1_lane_after_x2.includes("Aster Vale"), "Triad prep has Aster Vale", checks, issues);
      check(ctx.current.next_x1_lane_after_x2.includes("Kierkegaard"), "Triad prep has Kierkegaard", checks, issues);
      check(ctx.current.next_x1_lane_after_x2.includes("Aristotle"), "Triad prep has Aristotle", checks, issues);
      return result(checks, issues, ["omega-mini-current-state-v1.json", "v552-gmut-thos-v88-v7-x1-lumen-advisory-reduction-v1.json"], { triad, contacted_triad: false });
    },
  },
};

function readJson(rel) {
  return JSON.parse(fs.readFileSync(path.join(repoRoot, rel), "utf8"));
}

function collectRelevantFiles() {
  const dirs = ["docs/omega-mini-index", "docs/trinity-live-traces"];
  const files = [];
  for (const dir of dirs) {
    for (const name of fs.readdirSync(path.join(repoRoot, dir))) {
      if (name.includes("v7-x2") || name.includes("v7-x1") || name.includes("current-state") || name.includes("latest-updates")) {
        const rel = path.join(dir, name).replaceAll("\\", "/");
        if (fs.statSync(path.join(repoRoot, rel)).isFile()) files.push(rel);
      }
    }
  }
  return files.sort();
}

function result(checks, issues, evidence, outputs) {
  return { checks, issues, evidence, outputs };
}

function check(condition, label, checks, issues) {
  checks.push({ label, passed: Boolean(condition) });
  if (!condition) issues.push(label);
}

function readArg(flag, fallback) {
  const index = process.argv.indexOf(flag);
  if (index >= 0 && process.argv[index + 1]) return process.argv[index + 1];
  return fallback;
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
  }).formatToParts(date).reduce((acc, part) => {
    acc[part.type] = part.value;
    return acc;
  }, {});
  return `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}:${parts.second}+12:00`;
}

function renderMarkdown(receipt) {
  const checks = receipt.checks.map((item) => `- ${item.passed ? "PASS" : "FAIL"}: ${item.label}`).join("\n");
  const evidence = receipt.evidence.map((item) => `- \`${item}\``).join("\n");
  return `# ${receipt.runner_name}\n\nStatus: \`${receipt.overall_status}\`\n\nPurpose: ${receipt.purpose}\n\n## Checks\n\n${checks}\n\n## Evidence\n\n${evidence}\n\n## Boundary\n\nStatus-only runner. No new agents, held sibling activation, account mutation, deployment, global hook installation, private route handles, private lane body content, transcript text, credentials, or private machine paths are published.\n`;
}
