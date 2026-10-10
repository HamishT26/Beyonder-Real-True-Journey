[CmdletBinding()]
param([ValidateSet('Status','Connect','Stop')][string]$Action='Status')
$ErrorActionPreference='Stop'
$ghcClient='D:\GHC-Archives\global-tools\tunnel-client\0.0.16\tunnel-client.exe'
$ghcNode='D:/GHC-Archives/global-tools/node/26.11.1/node-v26.11.1-win-x64/node.exe'
$ghcServer='D:/GHC-Archives/global-tools/ghc-nexus-hub/mcp-admin-server.mjs'
$ghcPolicy='D:/GHC-Archives/private/ghc-nexus/admin/policy.json'
$ghcAlias='ghc-nexus'
. (Join-Path $PSScriptRoot 'GhcTunnelState.ps1')
$ghcConfig='D:/GHC-Archives/private/ghc-nexus/admin/hub28.json'
if(Test-Path -LiteralPath $ghcConfig -PathType Leaf){$ghcServer='D:/GHC-Archives/global-tools/ghc-nexus-hub/mcp-hub28-server.mjs';$ghcArgument=$ghcConfig}else{$ghcArgument=$ghcPolicy}
$ghcConnectExit=$null
foreach($ghcFile in @($ghcClient,$ghcNode,$ghcServer,$ghcPolicy)){if(-not(Test-Path -LiteralPath $ghcFile -PathType Leaf)){throw 'Reviewed Nexus runtime input missing'}}
if($Action -eq 'Connect'){
 $ghcIdentity=[Security.Principal.WindowsIdentity]::GetCurrent()
 $ghcPrincipal=[Security.Principal.WindowsPrincipal]::new($ghcIdentity)
 if(-not $ghcPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)){throw 'Start this operator script from the existing elevated Hub terminal'}
 $ghcBeforeRaw=& $ghcClient runtimes status $ghcAlias --json
 if($LASTEXITCODE -ne 0){throw 'Inspect the named runtime before another connection attempt'}
 $ghcBefore=$ghcBeforeRaw | ConvertFrom-Json
 if(-not $ghcBefore.process_running){
  # The credential is a reference only; this script never reads its contents.
  $ghcRaw=& $ghcClient runtimes connect --alias $ghcAlias --profile $ghcAlias --profile-dir 'D:/GHC-Archives/private/ghc-nexus/tunnel-profiles' --tunnel-id 'tunnel_6ac76521898c8191a0ef32cefeb6b7e2' --mcp-command "$ghcNode --max-old-space-size=128 $ghcServer $ghcArgument" --runtime-api-key 'file:D:/GHC-Archives/private/ghc-nexus/credentials/openai-api-key.txt' --json
  $ghcConnectExit=$LASTEXITCODE
 }
}elseif($Action -eq 'Stop'){
 $ghcRaw=& $ghcClient runtimes stop $ghcAlias --json
 if($LASTEXITCODE -ne 0){throw 'Named tunnel stop failed'}
}
$ghcStatusRaw=& $ghcClient runtimes status $ghcAlias --json
if($LASTEXITCODE -ne 0){throw 'Named tunnel status unavailable'}
$ghcStatus=$ghcStatusRaw | ConvertFrom-Json
# Intentionally omit raw log tails and credential/profile details.
$ghcOutcome=Get-GhcTunnelOutcome -Snapshot $ghcStatus -Action $Action -ConnectExitCode $ghcConnectExit
$ghcOutcome | ConvertTo-Json -Depth 3
exit $ghcOutcome.exitCode
