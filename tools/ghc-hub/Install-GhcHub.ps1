[CmdletBinding()]
param([switch]$Check)
$ErrorActionPreference='Stop'
$destination='D:\GHC-Archives\global-tools\ghc-nexus-hub'
$bank='D:\GHC-Archives\phase-banks\saelin-v708-v4-remasters-20261004\hub-20261005'
$pwsh='D:\GHC-Archives\global-tools\powershell\7.6.6\pwsh.exe'
$names=@('core.mjs','hub.mjs','hub.test.mjs','privacy-regression.test.mjs','Start-GhcHub.ps1','start-ghc-hub.sh','README.md','HYBRID-WORKFLOW.md','RESEARCH-BASELINE.md','OPERATOR-GUIDE.md','Start-GhcAdmin.ps1','Test-GhcLauncher.ps1')
$files=@($names|ForEach-Object {
 $p=Join-Path $PSScriptRoot $_
 if(-not(Test-Path -LiteralPath $p -PathType Leaf)){throw "Missing source: $_"}
 [pscustomobject]@{name=$_;source=$p;sha256=(Get-FileHash -LiteralPath $p).Hash.ToLowerInvariant()}
})
$desktop=[Environment]::GetFolderPath('Desktop')
$start=[Environment]::GetFolderPath('Programs')
$shortcuts=@((Join-Path $desktop 'GHC Nexus Hub - Administrator.lnk'),(Join-Path $start 'GHC Nexus Hub - Administrator.lnk'))
$shell=New-Object -ComObject WScript.Shell
$expectedArguments='-NoLogo -NoProfile -File "'+(Join-Path $destination 'Start-GhcHub.ps1')+'"'
foreach($shortcut in $shortcuts){
 if(Test-Path -LiteralPath $shortcut){
  $oldLink=$shell.CreateShortcut($shortcut)
  if($oldLink.TargetPath -ne $pwsh -or $oldLink.Arguments -ne $expectedArguments){throw 'A same-named unrelated shortcut exists; no changes performed'}
 }
}
foreach($f in $files){
 $target=Join-Path $destination $f.name
 if((Test-Path -LiteralPath $target) -and ((Get-Item -LiteralPath $target -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)){throw 'An installation leaf is redirected; no changes performed'}
}
if($Check){[ordered]@{destination=$destination;files=$files;shortcuts=$shortcuts;oldShortcutsChanged=$false;changesPerformed=$false}|ConvertTo-Json -Depth 5;return}
$stamp=[datetime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ')
$backup=Join-Path $bank ('hub-install-backup-'+$stamp)
New-Item -ItemType Directory -Path $backup | Out-Null
if(Test-Path -LiteralPath $destination){
 $existing=Get-Item -LiteralPath $destination -Force
 if($existing.Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Installation target is a reparse point'}
}else{New-Item -ItemType Directory -Path $destination | Out-Null}
foreach($f in $files){
 $target=Join-Path $destination $f.name
 if(Test-Path -LiteralPath $target){Copy-Item -LiteralPath $target -Destination (Join-Path $backup $f.name)}
 Copy-Item -LiteralPath $f.source -Destination $target
 if((Get-FileHash -LiteralPath $target).Hash.ToLowerInvariant() -ne $f.sha256){throw "Installed readback mismatch: $($f.name)"}
}
foreach($shortcut in $shortcuts){
 $link=$shell.CreateShortcut($shortcut)
 $link.TargetPath=$pwsh
 $link.Arguments=$expectedArguments
 $link.WorkingDirectory='D:\GHC-Family-Laboratory'
 $link.Description='GHC terminal menu and machine commands; normal UAC requests Administrator access'
 $link.IconLocation=$pwsh+',0'
 $link.Save()
 $checkLink=$shell.CreateShortcut($shortcut)
 if($checkLink.TargetPath -ne $pwsh -or $checkLink.Arguments -ne $link.Arguments){throw 'Shortcut readback mismatch'}
}
$receipt=[ordered]@{schema='ghc.hub.install.v1';utc=[datetime]::UtcNow.ToString('o');destination=$destination;sourceFiles=$files;shortcuts=$shortcuts;backup=$backup;oldShortcutsChanged=$false;appRestarted=$false;credentialStoresChanged=$false}
$receipt|ConvertTo-Json -Depth 6|Set-Content -LiteralPath (Join-Path $bank 'hub-installation.json') -Encoding utf8
$receipt|ConvertTo-Json -Depth 6
