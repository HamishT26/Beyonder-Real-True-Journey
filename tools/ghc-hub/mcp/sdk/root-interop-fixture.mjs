import fs from 'node:fs';
import {main} from '../../mcp-server.mjs';
if (!process.env.GHC_NEXUS_TEST_PID_FILE) throw new Error('Isolated test PID path required');
fs.appendFileSync(process.env.GHC_NEXUS_TEST_PID_FILE,JSON.stringify({pid:process.pid,at:new Date().toISOString()})+'\n');
await main();
