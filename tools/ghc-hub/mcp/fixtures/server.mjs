// Explicit synthetic stdio fixture; never connects to the real hub.
import {serveStdio} from '../adapter.mjs';
import {fixtureBindings} from './bindings.mjs';
try {
  const result=await serveStdio({input:process.stdin,output:process.stdout,...fixtureBindings()}).done;
  process.exitCode=result.reason==='eof'?0:1;
} catch {
  process.stderr.write('Fixture initialization failed.\n');
  process.exitCode=1;
}
