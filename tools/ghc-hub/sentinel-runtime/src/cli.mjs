import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequest, offlinePlan, providers, LIMITS} from './contract.mjs';
import {FileLedger, readLocalJson} from './ledger.mjs';

/** The standalone CLI is offline; a trusted Hub caller must inject a runtime to use `run`. */
export async function cliMain(argv, {runtime = null, stdout = text => process.stdout.write(text)} = {}) {
  try {
    const [command, ...rest] = argv;
    if (command === 'providers' && rest.length === 0) { stdout(JSON.stringify({providers: providers(), networkCalls: 0}) + '\n'); return 0; }
    if (!['validate', 'plan', 'run'].includes(command) || rest.length % 2) throw new Error('invalid_cli');
    const flags = {};
    for (let index = 0; index < rest.length; index += 2) {
      if (!['--request', '--quote', '--ledger-root', '--run-id', '--reviewed-hash', '--execution'].includes(rest[index]) || Object.hasOwn(flags, rest[index])) throw new Error('invalid_cli');
      flags[rest[index]] = rest[index + 1];
    }
    if (!flags['--request'] || !path.isAbsolute(flags['--request'])) throw new Error('request_file_required');
    const request = readLocalJson(flags['--request'], LIMITS.inputBytes * 6 + 4096);
    if (command === 'validate') {
      const validated = createRequest(request);
      stdout(JSON.stringify({valid: true, provider: validated.provider, model: validated.model, networkCalls: 0}) + '\n'); return 0;
    }
    const quote = flags['--quote'] ? readLocalJson(flags['--quote']) : null;
    if (command === 'plan') {
      const budget = flags['--ledger-root'] ? new FileLedger(flags['--ledger-root']).snapshot() : null;
      stdout(JSON.stringify(offlinePlan(request, {quote, budget})) + '\n'); return 0;
    }
    if (!runtime) { stdout(JSON.stringify({status: 'denied', reason: 'trusted_runtime_and_credential_provider_required', httpAttempts: 0}) + '\n'); return 2; }
    const result = await runtime.runOnce({request, quote, runId: flags['--run-id'], execute: true,
      execution: flags['--execution'] ?? 'live', reviewedRequestSha256: flags['--reviewed-hash']});
    stdout(JSON.stringify(result).replace(/[\x7f-\x9f\u061c\u200e\u200f\u202a-\u202e\u2066-\u206f]/g, char => '\\u' + char.charCodeAt(0).toString(16).padStart(4, '0')) + '\n');
    return ['completed', 'incomplete', 'refused'].includes(result.status) ? 0 : 2;
  } catch (error) {
    const code = typeof error.code === 'string' && /^[a-z_]+$/.test(error.code) ? error.code : 'invalid_input_or_file';
    stdout(JSON.stringify({status: 'denied', reason: code, httpAttempts: 0}) + '\n'); return 2;
  }
}
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  process.exitCode = await cliMain(process.argv.slice(2));
}
