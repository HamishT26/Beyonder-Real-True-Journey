#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { spawnSync } from "node:child_process";
import { setTimeout as sleep } from "node:timers/promises";
import { tmpdir } from "node:os";

const ROOT = new URL("..", import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1");
const TRACE_DIR = join(ROOT, "docs", "trinity-live-traces");

const options = {
  lanes: [],
  execute: false,
  backgroundWatch: false,
  waitSeconds: 0,
  minimumWords: 2000,
  itemsPerCategory: 10,
};

for (let index = 2; index < process.argv.length; index += 1) {
  const arg = process.argv[index];
  const next = process.argv[index + 1];
  if (arg === "--lane") {
    options.lanes.push(next);
    index += 1;
  } else if (arg === "--execute") {
    options.execute = true;
  } else if (arg === "--background-watch") {
    options.backgroundWatch = true;
  } else if (arg === "--phase-slug") {
    options.phaseSlug = next;
    index += 1;
  } else if (arg === "--output-dir") {
    options.outputDir = next;
    index += 1;
  } else if (arg === "--receipt-prefix") {
    options.receiptPrefix = next;
    index += 1;
  } else if (arg === "--wait-seconds") {
    options.waitSeconds = Number(next);
    index += 1;
  } else if (arg === "--minimum-words") {
    options.minimumWords = Number(next);
    index += 1;
  } else if (arg === "--items-per-category") {
    options.itemsPerCategory = Number(next);
    index += 1;
  }
}

if (!options.phaseSlug) {
  console.error("Usage: node ghc_strict_cli_lane_cycle.mjs --phase-slug <slug> --lane <name> [--execute] [--background-watch] [--wait-seconds <n>]");
  process.exit(2);
}

if (options.lanes.length === 0) {
  options.lanes.push("Arby");
}

options.receiptPrefix = options.receiptPrefix || `${options.phaseSlug}-strict-cli-lane-cycle`;
options.outputDir = options.outputDir || join(tmpdir(), `${options.receiptPrefix}-strict-cli-lane-cycle`);

function relTrace(name) {
  return join(TRACE_DIR, `${options.receiptPrefix}-${name}-v1`);
}

function run(label, args, allowFailure = false) {
  const proc = spawnSync(args[0], args.slice(1), {
    cwd: ROOT,
    encoding: "utf8",
    windowsHide: true,
    maxBuffer: 1024 * 1024,
  });
  const result = {
    label,
    command: args[0],
    status: proc.status,
    signal: proc.signal,
    stdout_bytes: Buffer.byteLength(proc.stdout || "", "utf8"),
    stderr_bytes: Buffer.byteLength(proc.stderr || "", "utf8"),
  };
  if (!allowFailure && proc.status !== 0) {
    result.failed = true;
  }
  return result;
}

function readJson(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

function writeJson(path, payload) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function writeMd(path, payload) {
  const lines = [
    `# ${payload.phase_slug} Strict CLI Lane Cycle`,
    "",
    `- generated_utc: \`${payload.generated_utc}\``,
    `- overall_status: \`${payload.overall_status}\``,
    `- execute: \`${payload.execute}\``,
    `- lanes: \`${payload.lanes.join(", ")}\``,
    "- raw boundary: temp-only; no prompt body, unredacted lane content, stdout, stderr, local paths, screen-capture files, or credentials are published.",
    "",
    "## Receipts",
  ];
  for (const [key, value] of Object.entries(payload.receipts)) {
    lines.push(`- ${key}: \`${value || "not_written"}\``);
  }
  lines.push("", "## Steps");
  for (const step of payload.steps) {
    lines.push(`- ${step.label}: status \`${step.status}\`, stdout bytes \`${step.stdout_bytes}\`, stderr bytes \`${step.stderr_bytes}\``);
  }
  lines.push("", "## Boundary", "");
  lines.push("This cycle runner publishes status-only receipts. GMUT, final physics, consciousness, and canon gates remain open.");
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${lines.join("\n")}\n`, "utf8");
}

async function main() {
  mkdirSync(options.outputDir, { recursive: true });
  const launcherJson = `${relTrace("launcher")}.json`;
  const launcherMd = `${relTrace("launcher")}.md`;
  const completionJson = `${relTrace("completion")}.json`;
  const completionMd = `${relTrace("completion")}.md`;
  const qualityJson = `${relTrace("quality")}.json`;
  const qualityMd = `${relTrace("quality")}.md`;
  const markerJson = `${relTrace("marker-review")}.json`;
  const markerMd = `${relTrace("marker-review")}.md`;
  const cycleJson = `${relTrace("receipt")}.json`;
  const cycleMd = `${relTrace("receipt")}.md`;

  const steps = [];
  const launcherArgs = [
    "python",
    "scripts/thos_cli_strict_stdin_lane_launcher.py",
    "--phase-slug",
    options.phaseSlug,
    "--output-dir",
    options.outputDir,
    "--minimum-words",
    String(options.minimumWords),
    "--items-per-category",
    String(options.itemsPerCategory),
    "--receipt-json",
    launcherJson,
    "--receipt-md",
    launcherMd,
  ];
  for (const lane of options.lanes) {
    launcherArgs.push("--lane", lane);
  }
  if (options.execute) {
    launcherArgs.push("--execute");
  }
  steps.push(run("strict_launcher", launcherArgs));

  if (options.execute && !options.backgroundWatch && options.waitSeconds > 0) {
    await sleep(options.waitSeconds * 1000);
  }

  let completion = null;
  let quality = null;
  let marker = null;
  if (options.execute && !options.backgroundWatch) {
    const completionArgs = [
      "python",
      "scripts/thos_cli_lane_completion_notifier.py",
      "--output-dir",
      options.outputDir,
      "--phase-slug",
      options.phaseSlug,
      "--poll-seconds",
      "30",
      "--timeout-seconds",
      "1",
      "--receipt-json",
      completionJson,
      "--receipt-md",
      completionMd,
      "--once",
    ];
    for (const lane of options.lanes) {
      completionArgs.push("--lane", lane);
    }
    steps.push(run("completion_notifier_once", completionArgs, true));
    if (existsSync(completionJson)) {
      completion = readJson(completionJson);
    }
    if (completion && ["FINAL_MESSAGES_READY", "OPEN_GAP_FINAL_MESSAGE_MARKER_REVIEW"].includes(completion.aggregate_status)) {
      const qualityArgs = [
        "python",
        "scripts/thos_cli_elaboration_quality_gate.py",
        "--output-dir",
        options.outputDir,
        "--phase-slug",
        options.phaseSlug,
        "--minimum-words",
        String(options.minimumWords),
        "--minimum-items-per-category",
        String(options.itemsPerCategory),
        "--receipt-json",
        qualityJson,
        "--receipt-md",
        qualityMd,
      ];
      for (const lane of options.lanes) {
        qualityArgs.push("--lane", lane);
      }
      steps.push(run("quality_gate", qualityArgs, true));
      if (existsSync(qualityJson)) {
        quality = readJson(qualityJson);
      }
      const markerArgs = [
        "python",
        "scripts/thos_cli_marker_review_ledger.py",
        "--phase-slug",
        options.phaseSlug,
        "--notifier-json",
        completionJson,
        "--quality-json",
        qualityJson,
        "--receipt-json",
        markerJson,
        "--receipt-md",
        markerMd,
      ];
      steps.push(run("marker_review", markerArgs, true));
      if (existsSync(markerJson)) {
        marker = readJson(markerJson);
      }
    }
  }

  let overallStatus = "PASS_STRICT_CLI_CYCLE_PLANNED";
  if (options.execute) {
    if (options.backgroundWatch) {
      const launcherStep = steps.find((step) => step.label === "strict_launcher");
      overallStatus = launcherStep?.status === 0 ? "PASS_STRICT_CLI_BACKGROUND_WATCH_STARTED" : "OPEN_GAP_STRICT_CLI_BACKGROUND_WATCH";
    } else if (quality?.aggregate_status === "PASS_ALL_CLI_LANES_ELABORATE" && marker?.overall_status === "PASS_MARKER_REVIEW_LEDGER") {
      overallStatus = "PASS_STRICT_CLI_CYCLE_READY";
    } else if (completion?.aggregate_status === "OPEN_GAP_FINAL_MESSAGE_PENDING") {
      overallStatus = "OPEN_GAP_STRICT_CLI_CYCLE_PENDING";
    } else {
      overallStatus = "OPEN_GAP_STRICT_CLI_CYCLE_REVIEW";
    }
  }

  const generatedAt = new Date();
  const payload = {
    artifact_type: "strict_cli_lane_cycle",
    generated_utc: generatedAt.toISOString(),
    phase_slug: options.phaseSlug,
    overall_status: overallStatus,
    timestamp_workflow: {
      lane_launch_or_harvest_time_utc: generatedAt.toISOString(),
      last_checkpoint_time_utc: generatedAt.toISOString(),
      next_checkpoint_due_utc: new Date(generatedAt.getTime() + 5 * 60 * 1000).toISOString(),
      checkpoint_interval_minutes: 5,
      checkpoint_overrun_allowed: true,
      background_watch_is_completion_proof: false,
      continue_retry_refresh_repair_until_gate_or_formal_open_gap: true,
    },
    execute: options.execute,
    background_watch_requested: options.backgroundWatch,
    lanes: options.lanes,
    wait_seconds: options.waitSeconds,
    output_dir: "<local_temp_redacted>",
    receipts: {
      launcher: existsSync(launcherJson) ? launcherJson.split(/[\\/]/).pop() : null,
      completion: existsSync(completionJson) ? completionJson.split(/[\\/]/).pop() : null,
      quality: existsSync(qualityJson) ? qualityJson.split(/[\\/]/).pop() : null,
      marker_review: existsSync(markerJson) ? markerJson.split(/[\\/]/).pop() : null,
    },
    steps,
    completion_status: completion?.aggregate_status || null,
    quality_status: quality?.aggregate_status || null,
    marker_status: marker?.overall_status || null,
    publication_boundary: {
      prompt_body_published: false,
      raw_lane_content_published: false,
      raw_transport_published: false,
      local_absolute_paths_published: false,
      screen_capture_files_published: false,
      credentials_published: false,
    },
    cadence_boundary: {
      background_watch_is_completion_proof: false,
      passive_wait_required: false,
      harvest_at_next_natural_safe_pause: true,
      timestamp_workflow_required: true,
    },
    claim_boundary: {
      gmut_gate_state: "open",
      canon_promotion: "not_claimed",
    },
  };
  writeJson(cycleJson, payload);
  writeMd(cycleMd, payload);
  console.log(JSON.stringify({ status: payload.overall_status, phase_slug: payload.phase_slug }, null, 2));
  process.exit(overallStatus.startsWith("PASS") ? 0 : 1);
}

main().catch((error) => {
  console.error(error?.message || String(error));
  process.exit(1);
});
