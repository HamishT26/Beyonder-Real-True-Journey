param([Parameter(Mandatory=$true)][string]$FixtureRoot)
$ErrorActionPreference='Stop'
$before=$env:PATH
. (Join-Path $PSScriptRoot 'GhcToolEnvironment.ps1')
$results=[Collections.Generic.List[object]]::new()
function Check([string]$Name,[bool]$Passed){if(-not $Passed){throw ('Failed: '+$Name)};$results.Add([pscustomobject]@{name=$Name;passed=$true})}
Check 'dot-source does not change process PATH' ($env:PATH -ceq $before)
if(-not [IO.Path]::IsPathRooted($FixtureRoot)){throw 'Absolute fixture root required'}
if(Test-Path -LiteralPath $FixtureRoot){throw 'Fresh fixture root required'}
[IO.Directory]::CreateDirectory($FixtureRoot) | Out-Null
$choices=@()
foreach($name in @('pwsh','node','git','gh')){
 $directory=Join-Path $FixtureRoot $name
 [IO.Directory]::CreateDirectory($directory) | Out-Null
 [IO.File]::WriteAllText((Join-Path $directory ($name+'.exe')),'Fixture only: never executed')
 $choices+=@{name=$name;directory=$directory;executable=($name+'.exe');match=('^C:/legacy/'+$name+'$')}
}
$prefix=($choices.directory -join ';')
$actual=Get-GhcPreferredToolPath -CurrentPath 'C:\shadow;C:\legacy\node;C:\other' -Choices $choices
Check 'preferred directories precede existing shims' ($actual -ceq ($prefix+';C:\shadow;C:\other'))
$quoted='"C:\LEGACY\NODE\";c:/legacy/git/;C:\keep'
Check 'quoted case and trailing separators normalize' ((Get-GhcPreferredToolPath -CurrentPath $quoted -Choices $choices) -ceq ($prefix+';C:\keep'))
Check 'unrelated directories preserve order' ((Get-GhcPreferredToolPath -CurrentPath 'C:\b;C:\a;C:\b' -Choices $choices) -ceq ($prefix+';C:\b;C:\a;C:\b'))
Check 'reapplying is idempotent' ((Get-GhcPreferredToolPath -CurrentPath $actual -Choices $choices) -ceq $actual)
Check 'empty PATH receives available reviewed prefix' ((Get-GhcPreferredToolPath -CurrentPath '' -Choices $choices) -ceq $prefix)
$missing=@{name='gh';directory=(Join-Path $FixtureRoot 'absent-gh');executable='gh.exe';match='^C:/legacy/gh$'}
$limited=@($choices | Where-Object name -ne 'gh')+@($missing)
Check 'missing optional tool preserves working fallback' ((Get-GhcPreferredToolPath -CurrentPath 'C:\legacy\gh;C:\other' -Choices $limited) -ceq (($choices[0..2].directory -join ';')+';C:\legacy\gh;C:\other'))
$refused=$false
try{Get-GhcPreferredToolPath -CurrentPath '' -Choices $limited -RequiredTools gh | Out-Null}catch{$refused=$_.Exception.Message -like '*Required tool missing: gh*'}
Check 'missing required tool is refused' $refused
$refused=$false
try{Get-GhcPreferredToolPath -CurrentPath '' -Choices $choices -RequiredTools imaginary | Out-Null}catch{$refused=$true}
Check 'unknown required tool is refused' $refused
Check 'available required Node passes' ((Get-GhcPreferredToolPath -CurrentPath '' -Choices $choices -RequiredTools node) -ceq $prefix)
Check 'no preference exists leaves original usable entries' ((Get-GhcPreferredToolPath -CurrentPath 'C:\legacy\gh;C:\other' -Choices @($missing)) -ceq 'C:\legacy\gh;C:\other')
Check 'function leaves parent PATH untouched' ($env:PATH -ceq $before)
[ordered]@{scope='PowerShell pure helper fixtures; no live launch or tunnel call';passed=$results.Count;checks=$results} | ConvertTo-Json -Depth 4 -Compress
