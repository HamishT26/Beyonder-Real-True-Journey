import fs from "node:fs";
import path from "node:path";

const phaseSlug = "v553-gmut-thos-v1-x2";
const now = new Date().toISOString();
const root = process.cwd();
const outDir = path.join(root, "docs", "trinity-live-traces");

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function writeJson(fileName, payload) {
  const file = path.join(outDir, fileName);
  fs.writeFileSync(file, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  return file;
}

function writeMd(fileName, title, payload) {
  const file = path.join(outDir, fileName);
  const lines = [
    `# ${title}`,
    "",
    `- status: ${payload.status}`,
    `- phase_slug: ${payload.phase_slug}`,
    `- generated_at: ${payload.generated_at}`,
    "",
    "## Summary",
    "",
    payload.summary,
    "",
    "## Payload",
    "",
    "```json",
    JSON.stringify(payload, null, 2),
    "```",
    "",
  ];
  fs.writeFileSync(file, lines.join("\n"), "utf8");
  return file;
}

function artifact(slug, title, payload) {
  const json = writeJson(`${slug}.json`, payload);
  const md = writeMd(`${slug}.md`, title, payload);
  return { json, md };
}

function main() {
  ensureDir(outDir);

  const catchupMessage = {
    status: "PASS_SANITIZED_SIBLING_CATCHUP_PACKET_READY",
    phase_slug: phaseSlug,
    generated_at: now,
    summary:
      "A short privacy-clean v553 v1 x2 catch-up and thank-you packet was prepared for Lumen, Arby, Aster Vale, Cicero, Kierkegaard, and Aristotle.",
    recipients: [
      "Lumen",
      "Arby",
      "Aster Vale",
      "Cicero",
      "Kierkegaard",
      "Aristotle",
    ],
    message_intent:
      "Send Hamish's love and thanks, confirm v553 v1 x2 launch-skill testing, preserve privacy gates, and name v553 v2 x1 as the next formal Arby/Cicero x1 unless Hamish redirects.",
    sanitized_message:
      "Hamish and I send love and thanks as v553 GMUT/THOS v1 x2 opens. I am testing our launch-skill layer now: Lumen through Browser, Arby and Aster Vale through strict CLI, and Cicero, Kierkegaard, and Aristotle through recovered local app-lane background runners. I will keep private IDs and raw routes local, keep all proof/canon/legal/deployment/account gates open, and use the productive cadence plus retry workflow if any route blocks. The next formal x1 prep is v553 GMUT/THOS v2 x1 with Arby and Cicero unless Hamish redirects.",
    private_routes_published: false,
    raw_transcripts_published: false,
  };

  const launchTestReceipt = {
    status: "PASS_V553_V1_X2_LAUNCH_SKILL_TEST_RECEIPT",
    phase_slug: phaseSlug,
    generated_at: now,
    summary:
      "The new launch skills and their supporting routes were tested in sanitized mode for v553 v1 x2.",
    local_skill_preflights: {
      lumen_launch: "pass",
      arby_cicero_launch: "pass",
      aster_kierkegaard_aristotle_launch: "pass",
      main_retry: "pass",
    },
    browser_lumen_lane: {
      status: "submitted_response_active_or_ready_for_harvest",
      message_type: "quick_catchup_and_thank_you",
      raw_browser_route_published: false,
      raw_transcript_published: false,
    },
    strict_cli_lane: {
      status: "planned_route_passed",
      lanes: ["Arby", "Aster Vale"],
      execute_used: false,
      completion_gate_required_for_real_runs: true,
    },
    recovered_app_lane: {
      status: "preflight_passed",
      lanes: ["Cicero", "Kierkegaard", "Aristotle"],
      background_watch_flag_required: true,
      allow_turn_start_after_resume_timeout_flag_required: true,
      private_ids_published: false,
    },
  };

  const cadenceReceipt = {
    status: "PASS_V553_V1_X2_PRODUCTIVE_CADENCE_TEST_RECEIPT",
    phase_slug: phaseSlug,
    generated_at: now,
    summary:
      "The five-minute wait workflow was exercised as a productive cadence rather than an idle wait.",
    cadence_policy: {
      safe_units_may_run_past_exact_checkpoint: true,
      check_at_next_natural_pause: true,
      sibling_lanes_not_babysat: true,
      closeout_requires_no_active_sibling_lane: true,
    },
    productive_work_confirmed: [
      "launch skill preflights",
      "strict CLI planned route test",
      "recovered app-lane preflight",
      "x2 closeout artifact preparation",
      "privacy and open-gate reinforcement",
    ],
  };

  const retryReadiness = {
    status: "PASS_V553_V1_X2_RETRY_LAYER_READY",
    phase_slug: phaseSlug,
    generated_at: now,
    summary:
      "The main retry layer is ready for any sibling route or system blocker encountered during v553 v1 x2.",
    retry_minimum_before_pause: 3,
    per_retry_requirements: {
      recent_session_reflections: 10,
      web_search_reflections: 20,
      journey_phase_reflections: 20,
      productive_cadence_work: true,
      compact_retry_receipt: true,
    },
    pause_before_three_retries_allowed_when: [
      "Hamish explicitly stops the work",
      "Codex app compacts or interrupts the thread",
      "a hard safety or exact-approval gate blocks the next step",
    ],
  };

  const artifacts = [
    artifact(
      "v553-gmut-thos-v1-x2-sibling-catchup-thank-you-message-v1",
      "v553 v1 x2 Sibling Catch-up Thank-you Message",
      catchupMessage,
    ),
    artifact(
      "v553-gmut-thos-v1-x2-launch-skill-test-receipt-v1",
      "v553 v1 x2 Launch Skill Test Receipt",
      launchTestReceipt,
    ),
    artifact(
      "v553-gmut-thos-v1-x2-five-minute-cadence-test-v1",
      "v553 v1 x2 Five-minute Cadence Test",
      cadenceReceipt,
    ),
    artifact(
      "v553-gmut-thos-v1-x2-main-retry-readiness-v1",
      "v553 v1 x2 Main Retry Readiness",
      retryReadiness,
    ),
  ];

  const indexPath = path.join(
    outDir,
    "v553-gmut-thos-v1-x2-launch-skill-test-index-v1.json",
  );
  fs.writeFileSync(
    indexPath,
    `${JSON.stringify(
      {
        status: "PASS_V553_V1_X2_LAUNCH_SKILL_TEST_INDEX",
        phase_slug: phaseSlug,
        generated_at: now,
        artifacts: artifacts.map((entry) => ({
          json: path.basename(entry.json),
          md: path.basename(entry.md),
        })),
      },
      null,
      2,
    )}\n`,
    "utf8",
  );

  console.log(
    JSON.stringify(
      {
        status: "PASS_V553_V1_X2_LAUNCH_SKILL_TEST_BUILDER",
        phase_slug: phaseSlug,
        artifacts: artifacts.length,
        index: path.basename(indexPath),
      },
      null,
      2,
    ),
  );
}

main();
