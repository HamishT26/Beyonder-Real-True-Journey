import fs from 'node:fs';
const payload = JSON.parse(fs.readFileSync(new URL('../../../docs/trinity-live-traces/v56-live-control-plane-proof-v1.json', import.meta.url)));
console.log(JSON.stringify({ phase: payload.phase, state: payload.control_plane_state }, null, 2));
