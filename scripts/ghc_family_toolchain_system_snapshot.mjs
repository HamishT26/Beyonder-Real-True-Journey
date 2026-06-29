#!/usr/bin/env node
import { execFileSync } from "node:child_process";
import { parseArgs, repoRoot, writeFamilyReceipt } from "./ghc_family_runner_common.mjs";

const args = parseArgs();
const root = args.get("--root") || repoRoot(import.meta.url);
const phaseSlug = args.get("--phase-slug") || "v576-gmut-thos-v2-x2";

const probes = [
  ["codex_cli", windowsCommand("codex"), windowsArgs("codex", ["--version"])],
  ["node", "node", ["--version"]],
  ["npm", npmCommand(), npmArgs(["--version"])],
  ["git", "git", ["--version"]],
  ["python", "python", ["--version"]],
  ["powershell", "powershell", ["-NoProfile", "-Command", "$PSVersionTable.PSVersion.ToString()"]]
].map(([name, command, commandArgs]) => runProbe(name, command, commandArgs));

const driveProbe = runDriveProbe();
const codexProbe = probes.find((probe) => probe.name === "codex_cli");
const codexLatestNpm = safeExec(npmCommand(), npmArgs(["view", "@openai/codex", "version"]));
const codexVersionMatchesNpm = codexProbe?.stdout.includes(codexLatestNpm);
const cFreeGb = driveProbe.drives.find((drive) => drive.name === "C")?.freeGb || 0;
const dFreeGb = driveProbe.drives.find((drive) => drive.name === "D")?.freeGb || 0;

const checks = [
  { label: "toolchain_probes_completed", status: probes.every((probe) => probe.status === "PASS") ? "PASS" : "OPEN_GAP" },
  { label: "codex_cli_matches_npm_latest", status: codexVersionMatchesNpm ? "PASS" : "OPEN_GAP", observed: { local: codexProbe?.stdout, npmLatest: codexLatestNpm } },
  { label: "c_drive_above_warning_floor", status: cFreeGb >= 19 ? "PASS" : "OPEN_GAP", observed: cFreeGb },
  { label: "d_drive_available_for_work", status: dFreeGb > 100 ? "PASS" : "OPEN_GAP", observed: dFreeGb },
  { label: "codex_desktop_app_not_mutated", status: "PASS" }
];

writeFamilyReceipt({
  root,
  phaseSlug,
  runnerName: "ghc_family_toolchain_system_snapshot.mjs",
  purpose: "Capture a sanitized phase-start/resume toolchain and drive snapshot without mutating the Codex desktop app package.",
  status: checks.every((check) => check.status === "PASS")
    ? "PASS_GHC_FAMILY_TOOLCHAIN_SYSTEM_SNAPSHOT"
    : "OPEN_GAP_GHC_FAMILY_TOOLCHAIN_SYSTEM_SNAPSHOT",
  checks,
  outputs: {
    probes,
    codexLatestNpm,
    drives: driveProbe.drives,
    updatePolicy: "Codex CLI may be updated from npm when newer; Codex desktop app remains status-only from this workflow."
  }
});

function runProbe(name, command, commandArgs) {
  try {
    return { name, status: "PASS", stdout: safeExec(command, commandArgs) };
  } catch (error) {
    return { name, status: "OPEN_GAP", stdout: "", error: "probe_failed" };
  }
}

function runDriveProbe() {
  try {
    const raw = execFileSync("powershell", [
      "-NoProfile",
      "-Command",
      "Get-PSDrive -Name C,D | Select-Object Name,Free,Used | ConvertTo-Json"
    ], { encoding: "utf8" });
    const parsed = JSON.parse(raw);
    const rows = Array.isArray(parsed) ? parsed : [parsed];
    return {
      status: "PASS",
      drives: rows.map((row) => ({
        name: row.Name,
        freeGb: roundGb(row.Free),
        usedGb: roundGb(row.Used)
      }))
    };
  } catch {
    return { status: "OPEN_GAP", drives: [] };
  }
}

function safeExec(command, commandArgs) {
  return execFileSync(command, commandArgs, { encoding: "utf8" }).trim();
}

function roundGb(bytes) {
  return Math.round((Number(bytes || 0) / 1024 / 1024 / 1024) * 100) / 100;
}

function npmCommand() {
  return windowsCommand("npm");
}

function npmArgs(args) {
  return windowsArgs("npm", args);
}

function windowsCommand(command) {
  return process.platform === "win32" ? "cmd.exe" : command;
}

function windowsArgs(command, args) {
  if (process.platform !== "win32") return args;
  return ["/d", "/s", "/c", [command, ...args].map(quoteCmd).join(" ")];
}

function quoteCmd(value) {
  return /[\s&()[\]{}^=;!'+,`~]/.test(value) ? `"${value.replace(/"/g, '\\"')}"` : value;
}
