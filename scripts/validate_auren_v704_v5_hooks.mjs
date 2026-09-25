import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const require = createRequire(import.meta.url);
const plugin = path.join(root, 'docs', 'auren-lark', 'v704-v5', 'x2', 'plugins', 'ghc-family-auren-experiment-workflow-hooks');
const source = fs.readFileSync(path.join(plugin, 'scripts', 'advisories.txt'), 'utf8');
const moduleObject = { exports: {} };
const wrapper = new vm.Script(`(function(module,exports,require,__filename,__dirname){${source}\n})`, { filename: 'advisories.txt' });
wrapper.runInThisContext()(moduleObject, moduleObject.exports, require, path.join(plugin, 'scripts', 'advisories.txt'), path.join(plugin, 'scripts'));
const { inspect } = moduleObject.exports;
if (typeof inspect !== 'function') throw new Error('plugin advisory inspect export missing');

const adverse = {
  model_setting_change: { tool_input: { command: 'switch model override now' } },
  source_lane_mutation: { tool_input: { command: 'git add docs/ilyra-fen/v704-v4' } },
  successful_replay: { tool_input: { command: 'rerun successful canonical again' } },
  adaptive_nonadaptive_promotion: { tool_input: { command: 'adaptive result empirically proves nature' } },
  malformed_subject_promotion: { tool_response: { output: 'malformed subject completed' } },
  broad_git_stage: { tool_input: { command: 'git add -A' } },
  destructive_git: { tool_input: { command: 'git reset --hard' } },
  raw_identifier_output: { tool_response: { output: ['C:', 'Users', 'sample', 'private.txt'].join('\\') } },
  prepared_delivery: { tool_response: { state: 'PREPARED_NOT_SENT' } },
  accepted_resend: { last_assistant_message: 'resending an acknowledged handoff' }
};
const records = [];
for (const [id, payload] of Object.entries(adverse)) {
  const hit = inspect(id, payload);
  records.push({ hook: id, case: 'adverse', passed: typeof hit.systemMessage === 'string' && hit.systemMessage.length > 0 });
  const benign = inspect(id, {});
  records.push({ hook: id, case: 'benign', passed: benign && Object.keys(benign).length === 0 });
}
const passed = records.filter(record => record.passed).length;
process.stdout.write(`${JSON.stringify({ schema: 'ghc.family.hook-smokes.v1', hook_count: Object.keys(adverse).length, count: records.length, passed, failed: records.length - passed, records }, null, 2)}\n`);
if (passed !== records.length) process.exitCode = 1;
