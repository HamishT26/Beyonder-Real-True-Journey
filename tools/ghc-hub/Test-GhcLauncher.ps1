[CmdletBinding()]
param([string]$Source = (Join-Path $PSScriptRoot 'Start-GhcAdmin.ps1'),[string]$Bank = 'D:\GHC-Archives\phase-banks\saelin-v708-v4-remasters-20261004\hub-20261005')
$ErrorActionPreference='Stop'
$tokens=$null; $parseErrors=$null
$capturedSource=[IO.File]::ReadAllBytes($Source)
$capturedHash=[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($capturedSource)).ToLowerInvariant()
$ast=[Management.Automation.Language.Parser]::ParseInput([Text.Encoding]::UTF8.GetString($capturedSource),$Source,[ref]$tokens,[ref]$parseErrors)
if($parseErrors.Count){throw 'Launcher syntax error'}
$functions=$ast.FindAll({param($n) $n -is [Management.Automation.Language.FunctionDefinitionAst]},$true)
foreach($fn in $functions){. ([scriptblock]::Create($fn.Extent.Text))}
$results=[Collections.Generic.List[object]]::new()
function Check([string]$Name,[scriptblock]$Body){try{& $Body; $results.Add(@{name=$Name;passed=$true})}catch{$results.Add(@{name=$Name;passed=$false;error=$_.Exception.GetType().FullName})}}
function Expect([bool]$Condition){if(-not $Condition){throw 'Expectation failed'}}
function Reject([scriptblock]$Body){$rejected=$false;try{& $Body | Out-Null}catch{$rejected=$true};Expect $rejected}
$fixture=Join-Path $Bank ('launcher-test-'+[guid]::NewGuid().ToString())
New-Item -ItemType Directory -Path $fixture | Out-Null
Check 'known duplicate blocks' {Expect ((Get-GhcAppDuplicateState @([pscustomobject]@{Path='D:\App\ChatGPT.exe'}) 'd:\app\chatgpt.exe') -eq 'present')}
Check 'no candidates is absent' {Expect ((Get-GhcAppDuplicateState @() 'D:\App\ChatGPT.exe') -eq 'absent')}
Check 'different executable is absent' {Expect ((Get-GhcAppDuplicateState @([pscustomobject]@{Path='D:\Other\ChatGPT.exe'}) 'D:\App\ChatGPT.exe') -eq 'absent')}
Check 'null candidate path is unknown' {Expect ((Get-GhcAppDuplicateState @([pscustomobject]@{Path=$null}) 'D:\App\ChatGPT.exe') -eq 'unknown')}
Check 'throwing candidate path is unknown' {$bad=[pscustomobject]@{};Add-Member -InputObject $bad -MemberType ScriptProperty -Name Path -Value {throw 'fixture'};Expect ((Get-GhcAppDuplicateState @($bad) 'D:\App\ChatGPT.exe') -eq 'unknown')}
Check 'positive duplicate beats another unknown' {Expect ((Get-GhcAppDuplicateState @([pscustomobject]@{Path=$null},[pscustomobject]@{Path='D:\App\ChatGPT.exe'}) 'D:\App\ChatGPT.exe') -eq 'present')}
Check 'ordinary owned JSONL path accepted' {$f=Join-Path $fixture 'ordinary.jsonl';Expect ((Get-GhcTraceDestination $f) -eq $f)}
foreach($leaf in @('existing.jsonl:trace','CON.jsonl','COM1.jsonl','LPT9.jsonl','log.jsonl.','log.jsonl ','log.txt','bad?.jsonl')){Check ('reject leaf '+$leaf) {Reject {Get-GhcTraceDestination (Join-Path $fixture $leaf)}}}
Check 'outside phase bank rejected' {Reject {Get-GhcTraceDestination 'D:\outside.jsonl'}}
Check 'relative filename rejected' {Reject {Get-GhcTraceDestination 'relative.jsonl'}}
Check 'candidate trace open creates an ordinary new file' {$f=Join-Path $fixture 'new.jsonl';$s=Open-GhcTraceStream $f;$s.Dispose();Expect (Test-Path -LiteralPath $f)}
Check 'candidate exclusive creation preserves existing bytes' {$f=Join-Path $fixture 'existing.jsonl';[IO.File]::WriteAllText($f,'fixture');Reject {$s=Open-GhcTraceStream $f;$s.Dispose()};Expect ([IO.File]::ReadAllText($f) -eq 'fixture')}
$script:ghcTraceDegraded=$false;$script:ghcTraceSource='fixture';$script:ghcTraceOperation='fixture';$script:ghcTraceBegins=@{};$script:ghcTraceWorkBegins=@{}
$script:ghcTraceClock=[pscustomobject]@{Elapsed=[pscustomobject]@{TotalMilliseconds=0.0}}
$script:ghcTraceWriter=[pscustomobject]@{Rows=[Collections.Generic.List[string]]::new()}
Add-Member -InputObject $script:ghcTraceWriter -MemberType ScriptMethod -Name WriteLine -Value {param($line) $this.Rows.Add($line);$script:ghcTraceClock.Elapsed.TotalMilliseconds+=7}
Check 'logging delay separated from operation time' {
 Write-GhcTraceStage 'fixture' 'begin';$script:ghcTraceClock.Elapsed.TotalMilliseconds+=3;Write-GhcTraceStage 'fixture' 'end'
 $last=$script:ghcTraceWriter.Rows[1]|ConvertFrom-Json
 Expect ($last.stageDurationMs -eq 10 -and $last.workDurationMs -eq 3 -and $last.beginRecordMs -eq 7)
}
Check 'partially initialized raw stream is closed' {$script:ghcTraceWriter=$null;$script:ghcTraceStream=[IO.MemoryStream]::new();Close-GhcTrace;Expect (-not $script:ghcTraceStream.CanWrite)}
$script:ghcTraceWriter=$null;$script:mockMode='absent';$script:mockStarts=0;$script:mockTotalStarts=0
function Get-Process {
 [CmdletBinding()]param([string]$Name)
 switch($script:mockMode){
  'no-process-error' {Write-Error -Message fixture -ErrorId NoProcessFoundForGivenName}
  'unexpected-error' {Write-Error -Message fixture -ErrorId AccessDeniedFixture}
  'unknown' {[pscustomobject]@{Path=$null}}
  'present' {[pscustomobject]@{Path='D:\App\ChatGPT.exe'}}
 }
}
function Start-Process {
 [CmdletBinding()]param([string]$FilePath)
 if($FilePath -ne 'INERT-FIXTURE'){throw 'Test must never start an actual executable'}
 $script:mockStarts++;$script:mockTotalStarts++
 [pscustomobject]@{Id=999;ProcessName='inert-fixture'}
}
foreach($mode in @('absent','no-process-error','unexpected-error','unknown','present')){
 Check ('candidate guarded start: '+$mode) {
  $script:mockMode=$mode;$script:mockStarts=0
  if($mode -in @('absent','no-process-error')){Invoke-GhcGuardedAppStart -ExpectedPath 'D:\App\ChatGPT.exe' -LaunchParameters @{FilePath='INERT-FIXTURE'} | Out-Null;Expect ($script:mockStarts -eq 1)}
  else{Reject {Invoke-GhcGuardedAppStart -ExpectedPath 'D:\App\ChatGPT.exe' -LaunchParameters @{FilePath='INERT-FIXTURE'}};Expect ($script:mockStarts -eq 0)}
 }
}
$failed=@($results|Where-Object {-not $_.passed})
[ordered]@{schema='ghc.launcher.guard-tests.v2';sourceSha256=$capturedHash;sourceBinding='one captured byte buffer parsed and hashed before tests';checks=$results.Count;passed=($results.Count-$failed.Count);failed=$failed.Count;observedMockStartCalls=$script:mockTotalStarts;executionMode='captured candidate functions with an inert Start-Process mock';syntheticClock=$true;results=$results} | ConvertTo-Json -Depth 6
if($failed.Count){exit 1}
