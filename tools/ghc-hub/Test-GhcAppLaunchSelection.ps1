$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'GhcAppLaunchSelection.ps1')
$results=[Collections.Generic.List[object]]::new()
function Assert-That { param([bool]$Condition,[string]$Message) if(-not $Condition){throw $Message} }
function Case { param([string]$Name,[scriptblock]$Body) try { & $Body; $results.Add([pscustomobject]@{name=$Name;passed=$true}) } catch { $results.Add([pscustomobject]@{name=$Name;passed=$false;error=$_.Exception.Message}) } }
function New-Package {
 param([string]$Version,[string]$Executable='app\ChatGPT.exe')
 $full='OpenAI.Codex_{0}_x64__abcdefghjkmnp' -f $Version
 return [pscustomobject]@{Name='OpenAI.Codex';Version=$Version;PackageFamilyName='OpenAI.Codex_abcdefghjkmnp';PackageFullName=$full;InstallLocation=('C:\FixturePackages\'+$full);Publisher='CN=OpenAI';Status='Ok';IsFramework=$false;IsResourcePackage=$false;IsBundle=$false;FixtureExecutable=$Executable}
}
function Select-Fixture {
 param([object[]]$Packages,[string]$Signature='Valid',[switch]$MismatchManifest,[switch]$MissingExecutable)
 $script:fixtures=@($Packages);$script:fixtureSignature=$Signature;$script:mismatch=[bool]$MismatchManifest;$script:leafExists=-not [bool]$MissingExecutable
 Resolve-GhcAppLaunchSelection -Packages $Packages -ReadManifest {
  param($manifestPath)
  $p=@($script:fixtures | Where-Object { (Join-Path $_.InstallLocation 'AppxManifest.xml') -eq $manifestPath })[0]
  $v=if($script:mismatch){'0.0.0.0'}else{$p.Version}
  '<Package><Identity Name="OpenAI.Codex" Version="'+$v+'" Publisher="CN=OpenAI"/><Applications><Application Id="App" Executable="'+$p.FixtureExecutable+'"/></Applications></Package>'
 } -TestExecutable {param($p) $script:leafExists} -ReadSignature {param($p) [pscustomobject]@{Status=$script:fixtureSignature;SignerCertificate=[pscustomobject]@{Subject='CN=OpenAI'}}}
}
Case 'numeric newest version, independent of enumeration order' {
 foreach($versions in @(@('2.9.0.0','2.10.0.0'),@('2.10.0.0','2.9.0.0'))) {
  $p=@($versions | ForEach-Object {New-Package $_});$r=Select-Fixture $p
  Assert-That ($r.Status -eq 'ready' -and $r.Selected.Version -eq '2.10.0.0') 'Newest numeric version not selected.'
 }
}
Case 'invalid newest signature holds without older fallback' {
 $r=Select-Fixture @((New-Package '2.9.0.0'),(New-Package '2.10.0.0')) -Signature 'NotTrusted'
 Assert-That ($r.Status -eq 'held' -and -not $r.DowngradePerformed) 'Invalid newest was not held.'
}
Case 'manifest version mismatch holds' { Assert-That ((Select-Fixture @((New-Package '2.10.0.0')) -MismatchManifest).Status -eq 'held') 'Manifest mismatch accepted.' }
Case 'manifest path traversal holds' { Assert-That ((Select-Fixture @((New-Package '2.10.0.0' '..\..\outside.exe'))).Status -eq 'held') 'Escaping executable accepted.' }
Case 'missing newest executable holds' { Assert-That ((Select-Fixture @((New-Package '2.10.0.0')) -MissingExecutable).Status -eq 'held') 'Missing executable accepted.' }
Case 'equal highest version at different paths is ambiguous' {
 $a=New-Package '2.10.0.0';$b=New-Package '2.10.0.0';$b.InstallLocation='D:\OtherFixturePackages\'+$b.PackageFullName
 Assert-That ((Select-Fixture @($a,$b)).Status -eq 'held') 'Ambiguous path accepted.'
}
Case 'multiple registered families hold' {
 $a=New-Package '2.9.0.0';$b=New-Package '2.10.0.0'
 $b.PackageFamilyName='OpenAI.Codex_0000000000000';$b.PackageFullName='OpenAI.Codex_2.10.0.0_x64__0000000000000'
 Assert-That ((Select-Fixture @($a,$b)).Status -eq 'held') 'Family ambiguity accepted.'
}
Case 'empty current-user snapshot holds' { Assert-That ((Select-Fixture @()).Status -eq 'held') 'Empty snapshot accepted.' }
Case 'framework rows cannot displace main App' {
 $a=New-Package '9.0.0.0';$a.IsFramework=$true
 $r=Select-Fixture @($a,(New-Package '2.10.0.0'))
 Assert-That ($r.Status -eq 'ready' -and $r.Selected.Version -eq '2.10.0.0') 'Framework displaced main.'
}
$older=New-Package '2.9.0.0';$newer=New-Package '2.10.0.0'
$selection=Select-Fixture @($older,$newer)
Case 'current executable process blocks duplicate launch' {
 $r=Get-GhcAppRunningObservation -Selection $selection -Processes @([pscustomobject]@{Id=101;Path=$selection.Selected.ExecutablePath})
 Assert-That ($r.State -eq 'current-running' -and -not $r.CanLaunch) 'Current duplicate not held.'
}
Case 'known older registered package process is detected' {
 $r=Get-GhcAppRunningObservation -Selection $selection -Processes @([pscustomobject]@{Id=102;Path=(Join-Path $older.InstallLocation 'app\ChatGPT.exe')})
 Assert-That ($r.State -eq 'older-package-running' -and -not $r.CanLaunch -and $r.Entries[0].Evidence -eq 'current-user-registration-path') 'Older registered path not detected.'
}
Case 'older removed registration is held with path-only version evidence' {
 $single=Select-Fixture @($newer)
 $r=Get-GhcAppRunningObservation -Selection $single -Processes @([pscustomobject]@{Id=103;Path=(Join-Path $older.InstallLocation 'app\ChatGPT.exe')})
 Assert-That ($r.State -eq 'older-package-running' -and -not $r.CanLaunch -and $r.Entries[0].Evidence -eq 'package-directory-name-only' -and -not $r.LoadedPackageIdentityVerified) 'Old path was missed or overclaimed.'
}
Case 'unreadable candidate path holds' {
 $r=Get-GhcAppRunningObservation -Selection $selection -Processes @([pscustomobject]@{Id=104})
 Assert-That ($r.State -eq 'unknown' -and -not $r.CanLaunch) 'Unreadable candidate assumed absent.'
}
Case 'different readable candidate path holds without inventing its version' {
 $r=Get-GhcAppRunningObservation -Selection $selection -Processes @([pscustomobject]@{Id=105;Path='C:\OtherApp\ChatGPT.exe'})
 Assert-That ($r.State -eq 'different-path' -and -not $r.CanLaunch -and $null -eq $r.Entries[0].VersionFromEvidence) 'Different path was ignored or assigned a version.'
}
Case 'empty successful process discovery is the only launchable state' {
 $r=Get-GhcAppRunningObservation -Selection $selection -Processes @()
 Assert-That ($r.State -eq 'absent' -and $r.CanLaunch) 'Empty successful discovery not accepted.'
 $r=Get-GhcAppRunningObservation -Selection $selection -Processes @() -DiscoveryFailed
 Assert-That ($r.State -eq 'unknown' -and -not $r.CanLaunch) 'Discovery error assumed absent.'
}
Case 'current manifest image name supplements the legacy App name' {
 $r=Select-Fixture @((New-Package '2.10.0.0' 'app\Codex.exe'))
 Assert-That ($r.Status -eq 'ready' -and $r.Selected.ProcessNames -contains 'Codex' -and $r.Selected.ProcessNames -contains 'ChatGPT') 'Current image name was not retained.'
}
$receipt=[ordered]@{schema='ghc.launcher-selection-tests.v1';tests=$results.Count;passed=@($results|Where-Object passed).Count;failed=@($results|Where-Object {-not $_.passed}).Count;results=$results.ToArray();appLaunches=0}
$receipt|ConvertTo-Json -Depth 8
if($receipt.failed -gt 0){exit 1}
