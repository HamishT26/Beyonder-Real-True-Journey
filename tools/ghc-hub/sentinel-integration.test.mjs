import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {nexusCommand} from './nexus.mjs';
import {validateCommandOptions} from './hub.mjs';

function fixture(t){const base=path.resolve(process.env.GHC_HUB_TEST_TMP||os.tmpdir());fs.mkdirSync(base,{recursive:true});const root=fs.mkdtempSync(path.join(base,'sentinel-hub-'));t.after(()=>{const rel=path.relative(base,path.resolve(root));if(!rel||rel.startsWith('..')||path.isAbsolute(rel))throw new Error('Cleanup scope');fs.rmSync(root,{recursive:true,force:true});});const file=path.join(root,'request.json');const request={schema:'ghc.sentinel.runtime.request.v1',sentinelId:'fixture',provider:'openai',model:'fixture-model',input:'PRIVATE_INPUT_CANARY',maxOutputTokens:32};fs.writeFileSync(file,JSON.stringify(request));return {c:{nexusHome:path.join(root,'private'),platform:process.platform},file,request};}
test('Hub Sentinel provider listing is explicit and offline',async()=>{const r=await nexusCommand('sentinel','api-providers',{},{});assert.equal(r.networkCalls,0);assert.equal(r.liveModelStarted,false);assert.equal(r.providers[0].endpoint,'https://api.openai.com/v1/responses');});
test('Hub Sentinel validation and plan omit prompt and deny unknown prices/budget',async t=>{const {c,file}=fixture(t);const v=await nexusCommand('sentinel','api-validate',{file},c);assert.equal(v.valid,true);const p=await nexusCommand('sentinel','api-plan',{file},c);assert.equal(p.networkCalls,0);assert.equal(p.eligibleForExplicitExecution,false);assert.ok(p.blockers.includes('pricing_and_token_evidence_required'));assert.ok(p.blockers.includes('known_available_budget_required'));assert.ok(!JSON.stringify({v,p}).includes('PRIVATE_INPUT_CANARY'));assert.equal(fs.existsSync(c.nexusHome),false);});
test('Hub planning does not accept an execution or credential flag',()=>{for(const values of [{execute:true},{apiKey:'fixture'},{'ledger-root':'other'}])assert.throws(()=>validateCommandOptions('sentinel','api-plan',values),/Unsupported/);});
