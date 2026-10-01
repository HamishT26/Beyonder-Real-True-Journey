'use strict';
const fs=require('node:fs'),path=require('node:path');
const base=path.join(__dirname,'..');
const names=['core-test-results.json','timeout-tests.json','advisory-results.json'];
for(const name of names){const r=JSON.parse(fs.readFileSync(path.join(base,name),'utf8'));if(r.failed)throw Error('Saved failed evidence: '+name);console.log(JSON.stringify({file:name,tests:r.tests,passed:r.passed,failed:r.failed,domain_replayed:false}));}
