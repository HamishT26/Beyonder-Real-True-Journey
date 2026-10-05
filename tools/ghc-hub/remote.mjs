import {findExecutable,clean} from './core.mjs';
import {nexusHome,readPrivate,slug,writePrivate} from './private-store.mjs';

export function remoteConfig(raw){
 if(!raw||!slug(raw.id)||!['ssh','gcp-iap'].includes(raw.kind))throw new Error('Invalid remote target');
 if(raw.kind==='ssh'&&!/^[A-Za-z][A-Za-z0-9._-]{0,79}$/.test(raw.alias||''))throw new Error('Invalid SSH alias');
 if(raw.kind==='gcp-iap'&&(!/^[a-z][a-z0-9-]{4,61}[a-z0-9]$/.test(raw.project||'')||!/^[a-z][a-z0-9-]{0,61}[a-z0-9]$/.test(raw.instance||'')||!/^[a-z]+-[a-z]+\d-[a-z]$/.test(raw.zone||'')))throw new Error('Invalid Google Cloud target');
 return {schema:'ghc.nexus.remote.v1',id:raw.id,kind:raw.kind,alias:raw.kind==='ssh'?raw.alias:null,project:raw.kind==='gcp-iap'?raw.project:null,instance:raw.kind==='gcp-iap'?raw.instance:null,zone:raw.kind==='gcp-iap'?raw.zone:null,verified:false,note:clean(raw.note||''),persistentSession:'tmux on the remote host; reconnect after host start',credentialTransfer:false};
}
export function saveRemote(c,raw){return writePrivate(nexusHome(c),'remote/target.json',remoteConfig(raw));}
export function remotePlan(c,target=null){
 const r=target?remoteConfig(target):readPrivate(nexusHome(c),'remote/target.json');
 if(!r)return {schema:'ghc.nexus.remote-plan.v1',status:'setup_required',existingHostVerified:false,reason:'Configure a verified SSH alias or Google Cloud IAP target',desktopCommander:'Use the connected Remote Desktop Commander plugin; offline status cannot be repaired by granting broader shell permissions',provisioningPerformed:false};
 const t=remoteConfig(r);
 if(t.kind==='ssh'){
   const command=findExecutable('ssh',c.platform);return {schema:'ghc.nexus.remote-plan.v1',status:command?'ready':'tool_missing',action:'remote-terminal',command,args:['-t','-o','ForwardAgent=no','-o','StrictHostKeyChecking=yes','-o','ConnectTimeout=20',t.alias,'tmux new-session -A -s ghc-nexus'],cwd:c.cwd,interactive:true,shell:false,note:'Uses the verified SSH configuration and known host key. The remote host must already have tmux. No agent forwarding or public admin listener is added.'};
 }
 return {schema:'ghc.nexus.remote-plan.v1',status:'supported_command_prepared',action:'remote-terminal',executableName:'gcloud',args:['compute','ssh',t.instance,'--project',t.project,'--zone',t.zone,'--tunnel-through-iap','--','-t','-o','ForwardAgent=no','tmux new-session -A -s ghc-nexus'],interactive:true,shell:false,note:'Official Google Cloud IAP route. It requires a configured CLI, authorized project, OS Login/IAP permissions and an existing running VM. A Windows .cmd shim must be invoked through a reviewed wrapper.'};
}
