$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'GhcTunnelState.ps1')
$cases=@(
 @{name='ready after a nonzero connect result';action='Connect';code=1;running=$true;ready=$true;healthy=$true;want='vendor_error_but_runtime_ready';exit=0},
 @{name='running but pending is not a failed reconnect instruction';action='Connect';code=1;running=$true;ready=$false;healthy=$false;want='connect_pending_do_not_repeat';exit=2},
 @{name='zero connect result without a running daemon is not success';action='Connect';code=0;running=$false;ready=$false;healthy=$false;want='stopped';exit=1},
 @{name='normal ready result';action='Connect';code=0;running=$true;ready=$true;healthy=$true;want='ready';exit=0},
 @{name='status can successfully report stopped';action='Status';code=$null;running=$false;ready=$false;healthy=$false;want='stopped';exit=0},
 @{name='ready flag alone is insufficient';action='Connect';code=0;running=$false;ready=$true;healthy=$true;want='stopped';exit=1},
 @{name='stop is pending while process still runs';action='Stop';code=$null;running=$true;ready=$true;healthy=$true;want='stop_pending';exit=2},
 @{name='stop confirms a stopped process';action='Stop';code=$null;running=$false;ready=$false;healthy=$false;want='stopped';exit=0}
)
$results=foreach($c in $cases){
 $s=[pscustomobject]@{process_running=$c.running;ready=$c.ready;healthy=$c.healthy;runtime_state='fixture';profile_exists=$true}
 $r=Get-GhcTunnelOutcome -Snapshot $s -Action $c.action -ConnectExitCode $c.code
 if($r.result -ne $c.want -or $r.exitCode -ne $c.exit){throw ('Failed: '+$c.name)}
 [ordered]@{name=$c.name;passed=$true}
}
$unknownCases=@($null,[pscustomobject]@{},[pscustomobject]@{process_running='false'},[pscustomobject]@{process_running=0})
foreach($s in $unknownCases){
 $denied=$false
 try{Test-GhcTunnelMayConnect -Snapshot $s | Out-Null}catch{$denied=$true}
 if(-not $denied){throw 'Unknown process state admitted a connection'}
 $r=Get-GhcTunnelOutcome -Snapshot $s -Action Connect
 if($r.state -ne 'unknown' -or $r.exitCode -ne 3){throw 'Unknown process state was misreported'}
 $results+=@{name='unknown or nonboolean process state refuses connect';passed=$true}
}
foreach($running in @($true,$false)){
 $s=[pscustomobject]@{process_running=$running}
 if((Test-GhcTunnelMayConnect -Snapshot $s) -ne (-not $running)){throw 'Known process state admission mismatch'}
 $results+=@{name=('connect admission for known running='+$running);passed=$true}
}
[ordered]@{passed=$results.Count;failed=0;checks=@($results);realConnections=0} | ConvertTo-Json -Depth 4
