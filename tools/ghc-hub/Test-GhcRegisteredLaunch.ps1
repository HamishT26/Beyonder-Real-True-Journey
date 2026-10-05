[CmdletBinding()]
param([string]$Source=(Join-Path $PSScriptRoot 'Start-GhcAdmin.ps1'))
$ErrorActionPreference='Stop'
$ghcBytes=[IO.File]::ReadAllBytes($Source)
$ghcHash=[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($ghcBytes)).ToLowerInvariant()
$ghcTokens=$null;$ghcErrors=$null
$ghcAst=[Management.Automation.Language.Parser]::ParseInput([Text.Encoding]::UTF8.GetString($ghcBytes),$Source,[ref]$ghcTokens,[ref]$ghcErrors)
if($ghcErrors.Count){throw 'Candidate syntax error'}
foreach($ghcFn in $ghcAst.FindAll({param($n)$n -is [Management.Automation.Language.FunctionDefinitionAst]},$true)){. ([scriptblock]::Create($ghcFn.Extent.Text))}
$ghcResults=[Collections.Generic.List[object]]::new()
function Check([string]$Name,[scriptblock]$Body){try{&$Body;$ghcResults.Add(@{name=$Name;passed=$true})}catch{$ghcResults.Add(@{name=$Name;passed=$false;error=$_.Exception.Message})}}
function Expect([bool]$Value){if(-not $Value){throw 'Expectation failed'}}
function Reject([scriptblock]$Body){$rejected=$false;try{&$Body|Out-Null}catch{$rejected=$true};Expect $rejected}
function Write-GhcTraceStage {}
$script:ghcFixtureMode='absent';$script:ghcShellCalls=0;$script:ghcElevationCalls=0
function Get-Process {[CmdletBinding()]param([string]$Name) if($script:ghcFixtureMode -eq 'present'){[pscustomobject]@{Path='D:\App\ChatGPT.exe'}}elseif($script:ghcFixtureMode -eq 'unknown'){[pscustomobject]@{Path=$null}}}
function Start-Process {[CmdletBinding()]param([string]$FilePath) if($FilePath -ne 'shell:AppsFolder\OpenAI.Codex_2p2nqsd0c76g0!App'){throw 'Unexpected launch target'};$script:ghcShellCalls++}
function New-GhcFixtureItem([string[]]$Names){
 $item=[pscustomobject]@{SelectedNames=$Names}
 Add-Member -InputObject $item -MemberType ScriptMethod -Name Verbs -Value {
  foreach($n in $this.SelectedNames){$v=[pscustomobject]@{Name=$n};Add-Member -InputObject $v -MemberType ScriptMethod -Name DoIt -Value {$script:ghcElevationCalls++};$v}
 }
 return $item
}
function Get-GhcRegisteredAppItem {param([string]$AppUserModelId) if($AppUserModelId -ne 'OpenAI.Codex_2p2nqsd0c76g0!App'){throw 'Unexpected registration'};return (New-GhcFixtureItem $script:ghcFixtureVerbs)}
$script:ghcFixtureVerbs=@('Open','Run as administrator','Uninstall')
Check 'normal route invokes only registered Open' {$r=Invoke-GhcGuardedAppStart -ExpectedPath 'D:\App\ChatGPT.exe' -RegisteredAppUserModelId 'OpenAI.Codex_2p2nqsd0c76g0!App';Expect ($ghcShellCalls -eq 1 -and $ghcElevationCalls -eq 0 -and -not $r.elevationRequested -and -not $r.packageIdentityVerified)}
Check 'Administrator route invokes only the registered elevation verb' {$r=Invoke-GhcGuardedAppStart -ExpectedPath 'D:\App\ChatGPT.exe' -RegisteredAppUserModelId 'OpenAI.Codex_2p2nqsd0c76g0!App' -RegisteredAdministrator;Expect ($ghcShellCalls -eq 1 -and $ghcElevationCalls -eq 1 -and $r.elevationRequested -and $null -eq $r.effectiveAdministrator -and -not $r.appReady)}
foreach($mode in @('present','unknown')){Check ('existing app guard blocks registered elevation: '+$mode){$script:ghcFixtureMode=$mode;Reject {Invoke-GhcGuardedAppStart -ExpectedPath 'D:\App\ChatGPT.exe' -RegisteredAppUserModelId 'OpenAI.Codex_2p2nqsd0c76g0!App' -RegisteredAdministrator};Expect ($ghcElevationCalls -eq 1)}}
$script:ghcFixtureMode='absent'
Check 'missing elevation verb has no direct fallback' {$script:ghcFixtureVerbs=@('Open','Uninstall');Reject {Invoke-GhcGuardedAppStart -ExpectedPath 'D:\App\ChatGPT.exe' -RegisteredAppUserModelId 'OpenAI.Codex_2p2nqsd0c76g0!App' -RegisteredAdministrator};Expect ($ghcShellCalls -eq 1 -and $ghcElevationCalls -eq 1)}
Check 'ambiguous elevation verb fails closed' {Reject {Get-GhcRegisteredElevationVerb (New-GhcFixtureItem @('Run as administrator','Run as administrator'))}}
Check 'unknown localized label fails closed' {Reject {Get-GhcRegisteredElevationVerb (New-GhcFixtureItem @('Unknown localized verb'))}}
Check 'unexpected package identifier is rejected' {Reject {Invoke-GhcGuardedAppStart -ExpectedPath 'D:\App\ChatGPT.exe' -RegisteredAppUserModelId 'Other.App_2p2nqsd0c76g0!App' -RegisteredAdministrator}}
$ghcFailed=@($ghcResults|Where-Object {-not $_.passed})
[ordered]@{schema='ghc.registered-launch-tests.v1';sourceSha256=$ghcHash;checks=$ghcResults.Count;passed=$ghcResults.Count-$ghcFailed.Count;failed=$ghcFailed.Count;actualAppLaunches=0;mode='candidate function tests with inert shell and process fixtures';results=$ghcResults}|ConvertTo-Json -Depth 6
if($ghcFailed.Count){exit 1}
