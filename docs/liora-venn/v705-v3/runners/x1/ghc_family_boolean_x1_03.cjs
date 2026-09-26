'use strict';
const fs=require('fs');
const lib=require('../../code/boolean-lib-x1.cjs');
const allowed=new Set(["algebraic_degree", "walsh_hadamard_spectrum"]);
let request;
try{request=JSON.parse(fs.readFileSync(0,'utf8'));if(!allowed.has(request.operation))throw new lib.BooleanContractError('OPERATION','Runner operation is outside its declared pair.');const result=lib.computeOperation(request);process.stdout.write(JSON.stringify({disposition:'completed',operation:request.operation,result,boundary:'same-owner finite synthetic only; NOT_READY_FOR_STAGE_20'})+'\n');}
catch(error){const code=error&&error.code?error.code:'RUNNER';process.stdout.write(JSON.stringify({refused:true,code,boundary:'invalid subject remains failed; NOT_READY_FOR_STAGE_20'})+'\n');process.exitCode=2;}
