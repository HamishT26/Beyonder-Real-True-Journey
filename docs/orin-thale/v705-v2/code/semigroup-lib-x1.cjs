"use strict";

function sortObject(value) {
  if (Array.isArray(value)) return value.map(sortObject);
  if (value && typeof value === "object") {
    const out = {};
    for (const key of Object.keys(value).sort()) out[key] = sortObject(value[key]);
    return out;
  }
  return value;
}

function canonical(value) { return JSON.stringify(sortObject(value)); }
function uniqueSorted(values) { return [...new Set(values)].sort((a, b) => a - b); }
function range(n) { return Array.from({length:n}, (_, i) => i); }
function cartesian4(n, fn) { for (let a=0;a<n;a++) for(let b=0;b<n;b++) for(let c=0;c<n;c++) for(let d=0;d<n;d++) fn(a,b,c,d); }

function validateRequest(request) {
  if (request.real_authority === true) throw new Error("AUTHORITY");
  const table = request.table;
  if (!Array.isArray(table) || table.length < 2 || table.length > 5) throw new Error("ORDER");
  const n = table.length;
  if (!table.every(row => Array.isArray(row) && row.length === n)) throw new Error("SQUARE");
  if (!table.every(row => row.every(x => Number.isInteger(x) && x >= 0 && x < n))) throw new Error("CLOSURE");
  return table;
}

function associativity(table) {
  const n = table.length, failures = [];
  for (let a=0;a<n;a++) for(let b=0;b<n;b++) for(let c=0;c<n;c++) {
    const left=table[table[a][b]][c], right=table[a][table[b][c]];
    if (left !== right) failures.push([a,b,c,left,right]);
  }
  return {associative: failures.length === 0, failures};
}

function identitiesAndZeros(table) {
  const n=table.length, xs=range(n);
  const left_ids=xs.filter(e => xs.every(x => table[e][x] === x));
  const right_ids=xs.filter(e => xs.every(x => table[x][e] === x));
  const left_zeros=xs.filter(z => xs.every(x => table[z][x] === z));
  const right_zeros=xs.filter(z => xs.every(x => table[x][z] === z));
  return {
    left_identities:left_ids,
    right_identities:right_ids,
    two_sided_identities:left_ids.filter(x => right_ids.includes(x)),
    left_zeros,
    right_zeros,
    two_sided_zeros:left_zeros.filter(x => right_zeros.includes(x)),
  };
}

function principalIdeals(table) {
  const n=table.length, rows=[];
  for (let a=0;a<n;a++) {
    const left=[a], right=[a], two=[a];
    for (let s=0;s<n;s++) { left.push(table[s][a]); right.push(table[a][s]); two.push(table[s][a], table[a][s]); }
    for (let s=0;s<n;s++) for(let t=0;t<n;t++) two.push(table[table[s][a]][t]);
    rows.push({element:a,left:uniqueSorted(left),right:uniqueSorted(right),two_sided:uniqueSorted(two)});
  }
  return {rows};
}

function equivalenceClasses(signatures) {
  const groups=new Map();
  signatures.forEach((value,index)=>{const key=canonical(value); if(!groups.has(key)) groups.set(key,[]); groups.get(key).push(index);});
  return [...groups.values()].sort((a,b)=>a[0]-b[0]);
}

function joinClasses(n,left,right) {
  const parent=range(n);
  function find(x){while(parent[x]!==x){parent[x]=parent[parent[x]];x=parent[x];}return x;}
  function union(a,b){let ra=find(a),rb=find(b);if(ra!==rb){parent[Math.max(ra,rb)]=Math.min(ra,rb);}}
  for(const block of [...left,...right]) for(const value of block.slice(1)) union(block[0],value);
  const groups=new Map(); for(let i=0;i<n;i++){const r=find(i);if(!groups.has(r))groups.set(r,[]);groups.get(r).push(i);}
  return [...groups.values()].sort((a,b)=>a[0]-b[0]);
}

function greens(table) {
  const ideals=principalIdeals(table).rows;
  const L=equivalenceClasses(ideals.map(x=>x.left));
  const R=equivalenceClasses(ideals.map(x=>x.right));
  const J=equivalenceClasses(ideals.map(x=>x.two_sided));
  const H=[]; for(const lb of L) for(const rb of R){const x=lb.filter(v=>rb.includes(v));if(x.length)H.push(x);}
  H.sort((a,b)=>a[0]-b[0]); const D=joinClasses(table.length,L,R);
  return {L,R,H,D,J,finite_D_equals_J:canonical(D)===canonical(J)};
}

function minimalIdeal(table) {
  const candidates=[...new Map(principalIdeals(table).rows.map(x=>[canonical(x.two_sided),x.two_sided])).values()];
  candidates.sort((a,b)=>a.length-b.length || canonical(a).localeCompare(canonical(b)));
  const minimal=candidates.filter(c=>!candidates.some(o=>o.length<c.length && o.every(x=>c.includes(x))));
  return {minimal_principal_ideals:minimal,unique:minimal.length===1,kernel:minimal.length===1?minimal[0]:[]};
}

function combinations(n,size,start=0,prefix=[],out=[]) {
  if(prefix.length===size){out.push([...prefix]);return out;}
  for(let i=start;i<n;i++){prefix.push(i);combinations(n,size,i+1,prefix,out);prefix.pop();} return out;
}

function subsemigroups(table) {
  const n=table.length, subsets=[];
  for(let size=1;size<=n;size++) for(const subset of combinations(n,size)) {
    const set=new Set(subset); if(subset.every(a=>subset.every(b=>set.has(table[a][b])))) subsets.push(subset);
  }
  return {count:subsets.length,subsets};
}

function setPartitions(items) {
  if(items.length===0) return [[]];
  const [first,...rest]=items, out=[];
  for(const partition of setPartitions(rest)) {
    out.push([[first],...partition.map(b=>[...b])]);
    for(let i=0;i<partition.length;i++){const copy=partition.map(b=>[...b]);copy[i]=[first,...copy[i]];out.push(copy);}
  }
  const map=new Map(); for(const p of out){const blocks=p.map(b=>[...b].sort((a,b)=>a-b)).sort((a,b)=>a[0]-b[0]);map.set(canonical(blocks),blocks);}
  return [...map.entries()].sort((a,b)=>a[0].localeCompare(b[0])).map(x=>x[1]);
}

function congruences(table) {
  const n=table.length, accepted=[];
  for(const partition of setPartitions(range(n))) {
    const blockOf={}; partition.forEach((block,i)=>block.forEach(v=>blockOf[v]=i)); let good=true;
    cartesian4(n,(a,b,c,d)=>{if(good && blockOf[a]===blockOf[b] && blockOf[c]===blockOf[d] && blockOf[table[a][c]]!==blockOf[table[b][d]]) good=false;});
    if(good) accepted.push(partition);
  }
  accepted.sort((a,b)=>a.length-b.length || canonical(a).localeCompare(canonical(b)));
  return {count:accepted.length,partitions:accepted};
}

function analyze(request) {
  const table=validateRequest(request), n=table.length, assoc=associativity(table);
  if(!assoc.associative) throw new Error("NOT_ASSOCIATIVE");
  switch(request.operation) {
    case "table_record": return {order:n,entries:n*n,closed:true,associative:true};
    case "associativity_certificate": return {associative:true,failure_count:0,counterexample:null};
    case "identity_and_zero": return identitiesAndZeros(table);
    case "idempotent_census": {const elements=range(n).filter(x=>table[x][x]===x);return {count:elements.length,elements};}
    case "unit_group": {const ids=identitiesAndZeros(table).two_sided_identities,pairs=[];if(ids.length){const e=ids[0];for(let a=0;a<n;a++)for(let b=0;b<n;b++)if(table[a][b]===e&&table[b][a]===e)pairs.push([a,b]);}return {identity:ids.length?ids[0]:null,units:uniqueSorted(pairs.map(x=>x[0])),inverse_pairs:pairs};}
    case "principal_ideals": return principalIdeals(table);
    case "greens_relations": return greens(table);
    case "minimal_ideal": return minimalIdeal(table);
    case "subsemigroup_census": return subsemigroups(table);
    case "congruence_census": return congruences(table);
    default: throw new Error("OPERATION");
  }
}

module.exports={canonical,analyze,greens,minimalIdeal,identitiesAndZeros};
