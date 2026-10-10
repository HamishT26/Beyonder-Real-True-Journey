import {loadAdminPolicy,createAdminCommander,CommanderError} from './admin-commander.mjs';

const [action,policyFile,id,sha256,...extra]=process.argv.slice(2);
try{
 if(extra.length||!policyFile||!['status','approve'].includes(action))throw new CommanderError('usage: status POLICY | approve POLICY ID SHA256');
 const api=createAdminCommander(await loadAdminPolicy(policyFile));
 const result=action==='status'?await api.dispatch('nexus.admin.status',{}):await api.approve(id,sha256);
 process.stdout.write(JSON.stringify(result)+'\n');
}catch(error){
 process.stderr.write(JSON.stringify({ok:false,code:error instanceof CommanderError?error.code:'operation_failed'})+'\n');process.exitCode=1;
}
