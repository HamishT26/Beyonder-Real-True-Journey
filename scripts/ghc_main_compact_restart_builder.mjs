#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");

const args = process.argv.slice(2);
const parsed = new Map();
for (let index = 0; index < args.length; index += 2) {
  parsed.set(args[index], args[index + 1]);
}

const phaseSlug = parsed.get("--phase-slug") || readCurrentPhase() || "unknown";
const explicitBuilder = parsed.get("--builder");
const builder = explicitBuilder || "ghc_context_compact_pause_updater.mjs";
const receiptPrefix = parsed.get("--receipt-prefix") || `${phaseSlug}-main-compact-restart`;

const childArgs = explicitBuilder
  ? args.includes("--phase-slug")
    ? args
    : ["--phase-slug", phaseSlug, ...args]
  : [
      "--root",
      repoRoot,
      "--phase-slug",
      phaseSlug,
      "--agent",
      parsed.get("--agent") || "Aevren Vale",
      "--receipt-prefix",
      receiptPrefix,
    ];

const child = spawnSync(process.execPath, [path.join(__dirname, builder), ...childArgs], {
  cwd: repoRoot,
  encoding: "utf8",
  stdio: ["ignore", "pipe", "pipe"],
  windowsHide: true,
  maxBuffer: 1024 * 1024,
});

const result = {
  status: child.status === 0 ? "PASS_MAIN_COMPACT_RESTART_BUILDER_DELEGATED" : "FAIL_MAIN_COMPACT_RESTART_BUILDER_DELEGATED",
  phase_slug: phaseSlug,
  delegated_builder: builder,
  exit_status: child.status,
  stdout: parseMaybeJson(child.stdout),
  stderr_excerpt: (child.stderr || "").slice(0, 4000),
  restart_policy: {
    compact_pause_preserves_active_lanes_as_open: true,
    child_startup_snapshot_required: true,
    no_global_hook_installed_by_default: true,
  },
};

process.stdout.write(JSON.stringify(result, null, 2) + "\n");
process.exit(child.status ?? 1);

function readCurrentPhase() {
  const file = path.join(repoRoot, "docs", "omega-mini-index", "omega-mini-current-state-v1.json");
  if (!fs.existsSync(file)) {
    return null;
  }
  try {
    return JSON.parse(fs.readFileSync(file, "utf8")).current_active_phase || null;
  } catch {
    return null;
  }
}

function parseMaybeJson(text) {
  const trimmed = (text || "").trim();
  if (!trimmed) {
    return null;
  }
  try {
    return JSON.parse(trimmed);
  } catch {
    return { text_excerpt: trimmed.slice(0, 4000) };
  }
}
