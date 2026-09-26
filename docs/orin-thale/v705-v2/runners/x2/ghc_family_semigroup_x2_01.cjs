"use strict";
const fs=require("fs"),path=require("path");
const lib=require(path.join(__dirname,"..","..","code","semigroup-lib-x2.cjs"));
const root=path.resolve(__dirname,"..","..","..","..","..");
const contractDir=path.join(root,"docs","orin-thale","v705-v2","planning","contracts");
const allowed=["automorphism_census", "endomorphism_census"];const negative=process.argv.includes("--negative");let chosen=null;
for(const file of fs.readdirSync(contractDir).sort()){const rows=JSON.parse(fs.readFileSync(path.join(contractDir,file),"utf8"));for(const row of rows){if(allowed.includes(row.request.operation)){chosen=row;break;}}if(chosen)break;}
if(!chosen){console.error("NO_CONTRACT");process.exit(2);}if(negative)chosen.request={...chosen.request,real_authority:true};
try{const actual=lib.analyze(chosen.request);if(negative){console.error("NEGATIVE_ACCEPTED");process.exit(3);}console.log(JSON.stringify({status:"PASS",operation:chosen.request.operation,digest:lib.canonical(actual)}));}
catch(error){if(negative&&String(error.message)==="AUTHORITY"){console.log(JSON.stringify({status:"REJECTED",error:"AUTHORITY"}));process.exit(0);}console.error(String(error.stack||error));process.exit(4);}
