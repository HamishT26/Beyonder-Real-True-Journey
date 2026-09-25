'use strict';
const fs=require('fs');
const OPS=['table_record','left_division','right_division','identities','associativity','commutativity','idempotents','left_translation_cycles','right_translation_cycles','subquasigroups','nuclei','automorphisms','transversals','parastrophes','principal_loop_isotope','relabel_covariance','accessible_summary','uncertainty_annotation','external_evidence_gap','authority_gate'];
function fail(code){const e=new Error(code);e.code=code;throw e;}
function validate(r){
 if(!r||typeof r!=='object'||Array.isArray(r))fail('ENVELOPE');
 if(r.real_authority===true)fail('AUTHORITY');
 if(Object.keys(r).sort().join('|')!==['schema','operation','profile_id','table','purpose'].sort().join('|'))fail('FIELDS');
 if(r.schema!=='ghc.family.quasigroup.request.v1'||r.purpose!=='synthetic'||typeof r.profile_id!=='string')fail('SCHEMA');
 if(!OPS.includes(r.operation))fail('OPERATION');
 const t=r.table;if(!Array.isArray(t)||t.length<2||t.length>5)fail('TABLE'); const n=t.length;
 for(const row of t){if(!Array.isArray(row)||row.length!==n)fail('TABLE');for(const v of row)if(!Number.isInteger(v)||v<0||v>=n)fail('SYMBOL');if(new Set(row).size!==n)fail('LATIN');}
 for(let j=0;j<n;j++){let seen=0;for(let i=0;i<n;i++)seen|=1<<t[i][j];if(seen!==(1<<n)-1)fail('LATIN');}return t;
}
function perms(n){const out=[];function visit(a,used){if(a.length===n){out.push(a.slice());return;}for(let i=0;i<n;i++)if(!(used&(1<<i))){a.push(i);visit(a,used|(1<<i));a.pop();}}visit([],0);return out;}
function cycleRecord(p){let used=0,out=[];for(let i=0;i<p.length;i++)if(!(used&(1<<i))){let c=[],j=i;do{c.push(j);used|=1<<j;j=p[j];}while(j!==i);out.push(c);}return out;}
function table(n,fn){return Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>fn(i,j)));}
function compute(r){
 const t=validate(r),n=t.length,u=Array.from({length:n},(_,i)=>i),op=r.operation;
 if(op==='table_record')return {order:n,entries:n*n,latin:true};
 if(op==='left_division'){let z=table(n,()=>-1);for(let x=0;x<n;x++)for(let y=0;y<n;y++)z[x][t[x][y]]=y;return z;}
 if(op==='right_division'){let z=table(n,()=>-1);for(let x=0;x<n;x++)for(let y=0;y<n;y++)z[t[x][y]][y]=x;return z;}
 if(op==='identities'){let left=[],right=[];for(let e=0;e<n;e++){let l=true,rr=true;for(let x=0;x<n;x++){l&&=t[e][x]===x;rr&&=t[x][e]===x;}if(l)left.push(e);if(rr)right.push(e);}return {left,right,two_sided:left.filter(x=>right.includes(x))};}
 if(op==='associativity'){let count=0,first=null;for(let a=0;a<n;a++)for(let b=0;b<n;b++)for(let c=0;c<n;c++){let l=t[t[a][b]][c],rr=t[a][t[b][c]];if(l!==rr){count++;if(first===null)first=[a,b,c,l,rr];}}return {holds:count===0,failure_count:count,first_failure:first};}
 if(op==='commutativity'){let count=0,first=null;for(let a=0;a<n;a++)for(let b=0;b<n;b++)if(t[a][b]!==t[b][a]){count++;if(first===null)first=[a,b,t[a][b],t[b][a]];}return {holds:count===0,failure_count:count,first_failure:first};}
 if(op==='idempotents'){let out=[];for(let a=0;a<n;a++)if(t[a][a]===a)out.push(a);return out;}
 if(op==='left_translation_cycles')return t.map(cycleRecord);
 if(op==='right_translation_cycles')return u.map(j=>cycleRecord(u.map(i=>t[i][j])));
 if(op==='subquasigroups'){let out=[];for(let mask=1;mask<(1<<n);mask++){let ok=true;for(let a=0;a<n;a++)if(mask&(1<<a))for(let b=0;b<n;b++)if((mask&(1<<b))&&!(mask&(1<<t[a][b])))ok=false;if(ok)out.push(u.filter(i=>mask&(1<<i)));}return out;}
 if(op==='nuclei'){let left=u.slice(),middle=u.slice(),right=u.slice();for(let a=0;a<n;a++)for(let b=0;b<n;b++)for(let c=0;c<n;c++)if(t[a][t[b][c]]!==t[t[a][b]][c]){left=left.filter(x=>x!==a);middle=middle.filter(x=>x!==b);right=right.filter(x=>x!==c);}return {left,middle,right,intersection:left.filter(x=>middle.includes(x)&&right.includes(x))};}
 if(op==='automorphisms'){let out=[];for(const p of perms(n)){let ok=true;for(let a=0;a<n;a++)for(let b=0;b<n;b++)if(t[p[a]][p[b]]!==p[t[a][b]])ok=false;if(ok)out.push(p);}return out;}
 if(op==='transversals'){let out=[];function walk(row,cols,symbols,chosen){if(row===n){out.push(chosen.slice());return;}for(let c=0;c<n;c++){let s=t[row][c];if(!(cols&(1<<c))&&!(symbols&(1<<s))){chosen.push(c);walk(row+1,cols|(1<<c),symbols|(1<<s),chosen);chosen.pop();}}}walk(0,0,0,[]);return out;}
 if(op==='parastrophes'){let out={};for(const p of perms(3)){let z=table(n,()=>-1);for(let a=0;a<n;a++)for(let b=0;b<n;b++){let v=[a,b,t[a][b]];z[v[p[0]]][v[p[1]]]=v[p[2]];}out[p.join('')]=z;}return out;}
 if(op==='principal_loop_isotope'){let f=0,g=1,left_map=[],right_map=[];for(let i=0;i<n;i++){left_map[t[i][g]]=i;right_map[t[f][i]]=i;}return {f,g,left_map,right_map,table:table(n,(x,y)=>t[left_map[x]][right_map[y]]),identity:t[f][g]};}
 if(op==='relabel_covariance'){let mapping=u.map(i=>(i+1)%n),inverse=[];for(let i=0;i<n;i++)inverse[mapping[i]]=i;let z=table(n,(a,b)=>mapping[t[inverse[a]][inverse[b]]]);let ok=true;for(let a=0;a<n;a++)for(let b=0;b<n;b++)if(inverse[z[mapping[a]][mapping[b]]]!==t[a][b])ok=false;return {mapping,inverse,table:z,roundtrip_verified:ok};}
 if(op==='accessible_summary')return {order:n,row_symbols_unique:true,column_symbols_unique:true,real_layout_authorized:false,table:t};
 if(op==='uncertainty_annotation')return {measurement_uncertainty:null,reason:'No observations; exact finite synthetic table only.'};
 if(op==='external_evidence_gap')return {missing:['independent implementation','real use study','affected-user review'],empirical_credit:0};
 if(op==='authority_gate')return {action:'held',required:['competent review','affected-party authorization'],executed:false};
 fail('OPERATION');
}
function evaluate(r){try{return {ok:true,value:compute(r)};}catch(e){if(!e.code)throw e;return {ok:false,error:e.code};}}
module.exports={OPS,evaluate,validate};
if(require.main===module){const r=JSON.parse(fs.readFileSync(0,'utf8'));process.stdout.write(JSON.stringify(Array.isArray(r)?r.map(evaluate):evaluate(r))+'\n');}
