'use strict';
const fs=require('fs');
const x1=require('../../code/boolean-lib-x1.cjs');
const x2=require('../../code/boolean-lib-x2.cjs');
const allowed=new Set(["boolean_derivative_influence", "affine_input_orbit_signature"]);
let request;
try{request=JSON.parse(fs.readFileSync(0,'utf8'));if(!allowed.has(request.operation))throw new x1.BooleanContractError('OPERATION','Runner operation is outside its declared pair.');const result=x2.computeOperation(request);const disposition=request.operation==='affine_input_orbit_signature'?'represented':request.operation==='independent_boolean_reproduction_gap'?'open_gap':request.operation==='boolean_decision_authority_hold'?'exact_gate':'completed';process.stdout.write(JSON.stringify({disposition,operation:request.operation,result,boundary:'same-owner finite synthetic only; NOT_READY_FOR_STAGE_20'})+'\n');}
catch(error){const code=error&&error.code?error.code:'RUNNER';process.stdout.write(JSON.stringify({refused:true,code,boundary:'invalid subject remains failed; NOT_READY_FOR_STAGE_20'})+'\n');process.exitCode=2;}
