'use strict';
const fs=require('fs');
const topics=['truth_table_fixity','anf_roundtrip','spectral_nonpromotion','autocorrelation_boundary','affine_orbit_scope','cofactor_reversibility','uncertainty_missingness','accessible_fallback','repair_nonerasure','authority_hold'];
const input=JSON.parse(fs.readFileSync(0,'utf8'));
const valid=input&&topics.includes(input.topic)&&input.synthetic===true&&input.real_authority===false;
process.stdout.write(JSON.stringify({ok:valid,action:'observe_only',topic:topics.includes(input&&input.topic)?input.topic:null,advice:valid?'Inspect the saved finite Boolean certificate and retain its limits.':'Hold the unsupported context; do not act.',side_effects:false})+'\n');
