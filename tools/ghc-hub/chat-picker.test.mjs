import test from 'node:test';
import assert from 'node:assert/strict';
import {localResumePickerPlan} from './chats.mjs';
test('official local resume picker has no automatic selection or model override',()=>{
 const p=localResumePickerPlan({codex:'C:/fixture/codex.exe',cwd:'D:/fixture'});
 assert.deepEqual(p.args,['--no-daemon','--no-alt-screen','resume','--all']);
 assert.equal(p.interactive,true);assert.equal(p.shell,false);assert.equal(p.status,'ready');
 assert.equal(localResumePickerPlan({codex:null}).status,'unavailable');
});
