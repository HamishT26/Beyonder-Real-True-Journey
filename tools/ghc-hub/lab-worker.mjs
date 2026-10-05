import {fileURLToPath} from 'node:url';
import path from 'node:path';
export function simulate(model,size){
 if(!Number.isInteger(size)||size<1||size>200000)throw new Error('Invalid size');
 let observation,passed;
 if(model==='diffusion'){
   let x=Array(32).fill(0);x[0]=1;const initialMass=1,initialEnergy=1;
   for(let t=0;t<size;t++){const y=x.map((v,i)=>v+0.2*(x[(i+31)%32]-2*v+x[(i+1)%32]));x=y;}
   const mass=x.reduce((a,b)=>a+b,0),energy=x.reduce((a,b)=>a+b*b,0);
   observation={cells:32,steps:size,coefficient:0.2,initialMass,mass,initialEnergy,energy,minimum:Math.min(...x),maximum:Math.max(...x)};
   passed=Math.abs(mass-1)<1e-9&&energy<=1+1e-12&&x.every(v=>Number.isFinite(v)&&v>=-1e-12);
 }else if(model==='queue'){
   let finish=0,totalWait=0,maxWait=0;
   for(let i=0;i<size;i++){const arrival=i*3,service=1+i%5,start=Math.max(arrival,finish);totalWait+=start-arrival;maxWait=Math.max(maxWait,start-arrival);finish=start+service;}
   observation={jobs:size,arrivalSpacing:3,lastCompletion:finish,totalWait,maxWait,meanWait:totalWait/size};passed=Number.isSafeInteger(finish)&&totalWait>=0&&maxWait<=3;
 }else if(model==='consent'){
   let allowed=0,denied=0,violations=0;
   for(let i=0;i<size;i++){const issued=i%7,expires=issued+3,now=i%11,revoked=i%5===0;const permit=!revoked&&now>=issued&&now<expires;if(permit){allowed++;if(revoked||now<issued||now>=expires)violations++;}else denied++;}
   observation={decisions:size,allowed,denied,violations,boundary:'issued <= now < expires; explicit revocation denies'};passed=allowed+denied===size&&violations===0;
 }else throw new Error('Unknown model');
 return {schema:'ghc.nexus.lab-result.v1',model,passed,observation,empiricalEvidence:false,professionalOrLegalCertification:false};
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){try{const result=simulate(process.argv[2],Number(process.argv[3]));console.log(JSON.stringify(result));process.exitCode=result.passed?0:1;}catch{console.error(JSON.stringify({status:'invalid_model_or_size'}));process.exitCode=2;}}
