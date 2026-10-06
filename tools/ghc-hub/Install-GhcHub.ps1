[CmdletBinding()]
param([switch]$Check)
$ErrorActionPreference='Stop'
$ghcDestination='D:\GHC-Archives\global-tools\ghc-nexus-hub'
$ghcBank='D:\GHC-Archives\phase-banks\saelin-nexus-v3-20261007'
$ghcBin='D:\GHC-Archives\global-tools\bin'
$ghcPwsh='D:\GHC-Archives\global-tools\powershell\7.6.6\pwsh.exe'
$ghcNode='D:\GHC-Archives\global-tools\node\26.10.0\node-v26.10.0-win-x64\node.exe'
$ghcNpm='D:\GHC-Archives\global-tools\node\26.10.0\node-v26.10.0-win-x64\node_modules\npm\bin\npm-cli.js'
$ghcAdminTarget='D:\GHC-Archives\global-tools\ghc-config-launchers\Start-GhcAdmin.ps1'
function Test-GhcCloudPlaceholder([string]$Path) {
 if(-not ('GhcInstallerNativeTags' -as [type])){
 Add-Type -TypeDefinition @'
using System; using System.Runtime.InteropServices; using Microsoft.Win32.SafeHandles;
public static class GhcInstallerNativeTags {
 [StructLayout(LayoutKind.Sequential)] struct TagInfo {public uint Attributes;public uint ReparseTag;}
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)] static extern SafeFileHandle CreateFile(string path,uint access,uint share,IntPtr security,uint creation,uint flags,IntPtr template);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool GetFileInformationByHandleEx(SafeFileHandle h,int cls,out TagInfo data,uint size);
 public static uint Tag(string path){using(var h=CreateFile(path,0,7,IntPtr.Zero,3,0x02200000,IntPtr.Zero)){if(h.IsInvalid)throw new System.ComponentModel.Win32Exception(Marshal.GetLastWin32Error());TagInfo t;if(!GetFileInformationByHandleEx(h,9,out t,8))throw new System.ComponentModel.Win32Exception(Marshal.GetLastWin32Error());return t.ReparseTag;}}
}
'@
 }
 $ghcTag=[GhcInstallerNativeTags]::Tag($Path)
 # CLOUD through CLOUD_F tags are placeholders, not name-surrogate redirects.
 return (($ghcTag -band [uint32]4294905855) -eq [uint32]2415919130)
}
function Assert-GhcPlainPath([string]$Path,[switch]$AllowKnownDesktopPlaceholder) {
 if(-not [IO.Path]::IsPathFullyQualified($Path)){throw 'Absolute installation path required'}
 $ghcPart=[IO.Path]::GetFullPath($Path)
 while($ghcPart){
  if(Test-Path -LiteralPath $ghcPart){if((Get-Item -LiteralPath $ghcPart -Force).Attributes -band [IO.FileAttributes]::ReparsePoint){
   $ghcDesktopPath=[Environment]::GetFolderPath('Desktop')
   $ghcWithinDesktop=[IO.Path]::GetFullPath($Path).StartsWith($ghcDesktopPath+'\',[StringComparison]::OrdinalIgnoreCase)
   if(-not($AllowKnownDesktopPlaceholder -and $ghcWithinDesktop -and (Test-GhcCloudPlaceholder $ghcPart))){throw 'Redirected installation path refused'}
  }}
  $ghcPart=[IO.Path]::GetDirectoryName($ghcPart)
 }
}
Assert-GhcPlainPath $PSScriptRoot
foreach($ghcPath in @($ghcDestination,$ghcBank,$ghcBin,$ghcAdminTarget)){Assert-GhcPlainPath $ghcPath}
$ghcManifest=Get-Content -Raw -LiteralPath (Join-Path $PSScriptRoot 'installation-files.json') | ConvertFrom-Json
if($ghcManifest.schema -ne 'ghc.nexus.install-files.v2' -or $ghcManifest.files.Count -lt 20){throw 'Invalid release manifest'}
$ghcSeen=[Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
$ghcFiles=@(foreach($ghcRow in $ghcManifest.files){
 if($ghcRow.path -notmatch '^[a-zA-Z0-9._/-]+$' -or $ghcRow.path.StartsWith('/') -or @($ghcRow.path.Split('/') | Where-Object {$_ -eq '..' -or $_ -eq '.' -or $_ -eq ''}).Count -or -not $ghcSeen.Add($ghcRow.path)){throw 'Invalid or duplicate release path'}
 $ghcSource=Join-Path $PSScriptRoot $ghcRow.path
 $ghcTarget=Join-Path $ghcDestination $ghcRow.path
 Assert-GhcPlainPath $ghcSource; Assert-GhcPlainPath $ghcTarget
 if(-not(Test-Path -LiteralPath $ghcSource -PathType Leaf)){throw 'Missing release source'}
 if((Get-Item -LiteralPath $ghcSource).Length -ne $ghcRow.bytes -or (Get-FileHash -LiteralPath $ghcSource -Algorithm SHA256).Hash.ToLowerInvariant() -ne $ghcRow.sha256){throw 'Release source digest mismatch'}
 [pscustomobject]@{relative=$ghcRow.path;source=$ghcSource;target=$ghcTarget;sha256=$ghcRow.sha256;bytes=$ghcRow.bytes}
})
if(-not $ghcSeen.Contains('hub.mjs') -or -not $ghcSeen.Contains('mcp/sdk/package-lock.json')){throw 'Required release entrypoint or pinned dependency lock absent'}
foreach($ghcTool in @($ghcNode,$ghcPwsh,$ghcNpm)){if(-not(Test-Path -LiteralPath $ghcTool -PathType Leaf)){throw 'Pinned installation tool missing'}}
$ghcDesktop=[Environment]::GetFolderPath('Desktop')
$ghcPrograms=[Environment]::GetFolderPath('Programs')
$ghcShortcutSpecs=@()
foreach($ghcFolder in @($ghcDesktop,$ghcPrograms)){
 $ghcShortcutSpecs += [pscustomobject]@{path=(Join-Path $ghcFolder 'GHC Nexus Hub - Administrator.lnk');arguments=('-NoLogo -NoProfile -File "'+(Join-Path $ghcDestination 'Start-GhcHub.ps1')+'"');description='GHC terminal hub with normal Windows Administrator consent'}
 $ghcShortcutSpecs += [pscustomobject]@{path=(Join-Path $ghcFolder 'GHC Nexus Hub - Current User.lnk');arguments=('-NoLogo -NoProfile -File "'+(Join-Path $ghcDestination 'Start-GhcHub.ps1')+'" -CurrentUser');description='GHC terminal hub with the current Windows token'}
 $ghcShortcutSpecs += [pscustomobject]@{path=(Join-Path $ghcFolder 'GHC Nexus Hub CMD - Administrator.lnk');arguments=('-NoLogo -NoProfile -File "'+(Join-Path $ghcDestination 'Start-GhcCmdHub.ps1')+'"');description='GHC Hub in Command Prompt with normal Windows Administrator consent'}
 $ghcShortcutSpecs += [pscustomobject]@{path=(Join-Path $ghcFolder 'GHC Nexus Hub CMD - Current User.lnk');arguments=('-NoLogo -NoProfile -File "'+(Join-Path $ghcDestination 'Start-GhcCmdHub.ps1')+'" -CurrentUser');description='GHC Hub in Command Prompt using the current Windows token'}
 $ghcShortcutSpecs += [pscustomobject]@{path=(Join-Path $ghcFolder 'GHC Codex - Registered App.lnk');arguments=('-NoLogo -NoProfile -File "'+$ghcAdminTarget+'" -Target Codex -AppActivation Registered');description='Registered ChatGPT/Codex app activation; preserves Windows package identity when supported'}
 $ghcShortcutSpecs += [pscustomobject]@{path=(Join-Path $ghcFolder 'GHC Codex - Administrator.lnk');arguments=('-NoLogo -NoProfile -File "'+$ghcAdminTarget+'" -Target Codex -AppActivation DirectAdministrator');allowedPreviousArguments=('-NoLogo -NoProfile -File "'+$ghcAdminTarget+'" -Target Codex -AppActivation RegisteredAdministrator');description='Direct Administrator launch; use the separate registered App entry for updates'}
}
$ghcShell=New-Object -ComObject WScript.Shell
foreach($ghcShortcut in $ghcShortcutSpecs){
 Assert-GhcPlainPath $ghcShortcut.path -AllowKnownDesktopPlaceholder
 if(Test-Path -LiteralPath $ghcShortcut.path){$ghcOld=$ghcShell.CreateShortcut($ghcShortcut.path);if($ghcOld.TargetPath -ne $ghcPwsh -or ($ghcOld.Arguments -ne $ghcShortcut.arguments -and $ghcOld.Arguments -ne $ghcShortcut.allowedPreviousArguments)){throw 'An unrelated same-named shortcut exists'}}
}
foreach($ghcWrapper in @('ghc-nexus.cmd','ghc-nexus.ps1')){
 $ghcExisting=Join-Path $ghcBin $ghcWrapper
 Assert-GhcPlainPath $ghcExisting
 if(Test-Path -LiteralPath $ghcExisting){if((Get-Content -Raw -LiteralPath $ghcExisting) -notmatch 'GHC Nexus managed command'){throw 'An unrelated command wrapper exists'}}
}
$ghcOldAdminHash=if(Test-Path -LiteralPath $ghcAdminTarget){(Get-FileHash -LiteralPath $ghcAdminTarget).Hash.ToLowerInvariant()}else{$null}
$ghcNewAdminHash=($ghcFiles | Where-Object relative -eq 'Start-GhcAdmin.ps1').sha256
if($ghcOldAdminHash -and $ghcOldAdminHash -notin @('c8688e45833324fbfc44e3fec16ceba7526db78f4dd62160a69b3215d7184844',$ghcNewAdminHash)){throw 'Shared launcher changed since its reviewed baseline'}
$ghcPlan=[ordered]@{schema='ghc.nexus.install-plan.v2';destination=$ghcDestination;files=$ghcFiles.Count;shortcuts=$ghcShortcutSpecs;wrappers=$ghcBin;dependencies='npm ci --omit=dev --ignore-scripts, pinned MCP SDK2 lock';appRestarted=$false;privateStateIncluded=$false;changesPerformed=$false}
if($Check){$ghcPlan | ConvertTo-Json -Depth 5;return}
$ghcBackup=Join-Path $ghcBank ('install-backup-'+[datetime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ'))
New-Item -ItemType Directory -Path $ghcBackup | Out-Null
$ghcBackups=[Collections.Generic.List[object]]::new()
function Copy-GhcReviewed([string]$Source,[string]$Target,[string]$Relative){
 Assert-GhcPlainPath $Target
 $ghcBackupFile=Join-Path $ghcBackup $Relative
 if(Test-Path -LiteralPath $Target){
  [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($ghcBackupFile)) | Out-Null
  Copy-Item -LiteralPath $Target -Destination $ghcBackupFile
  if((Get-FileHash -LiteralPath $Target).Hash -ne (Get-FileHash -LiteralPath $ghcBackupFile).Hash){throw 'Recovery backup readback mismatch'}
  $ghcBackups.Add([pscustomobject]@{target=$Target;backup=$ghcBackupFile;sha256=(Get-FileHash -LiteralPath $ghcBackupFile).Hash.ToLowerInvariant()})
 }
 [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($Target)) | Out-Null
 Copy-Item -LiteralPath $Source -Destination $Target
 if((Get-FileHash -LiteralPath $Source).Hash -ne (Get-FileHash -LiteralPath $Target).Hash){throw 'Installed readback mismatch'}
}
$ghcUserPathBefore=[Environment]::GetEnvironmentVariable('Path','User')
$ghcReceipt=[ordered]@{schema='ghc.nexus.install.v2';version=$ghcManifest.version;startedAt=[datetime]::UtcNow.ToString('o');status='in_progress';backup=$ghcBackup;destination=$ghcDestination;files=$ghcFiles;backups=$ghcBackups;userPathBefore=$ghcUserPathBefore;shortcuts=$ghcShortcutSpecs;appRestarted=$false;credentialStoresChanged=$false;privateStateIncluded=$false}
try {
 foreach($ghcFile in $ghcFiles){Copy-GhcReviewed $ghcFile.source $ghcFile.target ('runtime/'+$ghcFile.relative)}
 Copy-GhcReviewed (Join-Path $PSScriptRoot 'installation-files.json') (Join-Path $ghcDestination 'installation-files.json') 'runtime/installation-files.json'
 Push-Location -LiteralPath (Join-Path $ghcDestination 'mcp/sdk')
 try {& $ghcNode $ghcNpm ci --omit=dev --ignore-scripts --no-audit --no-fund --prefer-offline --fetch-timeout=20000 --fetch-retries=1 --cache 'D:\GHC-Archives\tool-caches\npm-cache';if($LASTEXITCODE -ne 0){throw 'Pinned MCP dependency installation failed'}} finally {Pop-Location}
 Copy-GhcReviewed (Join-Path $PSScriptRoot 'Start-GhcAdmin.ps1') $ghcAdminTarget 'shared-launcher/Start-GhcAdmin.ps1'
 foreach($ghcWrapper in @('ghc-nexus.cmd','ghc-nexus.ps1')){Copy-GhcReviewed (Join-Path $PSScriptRoot $ghcWrapper) (Join-Path $ghcBin $ghcWrapper) ('bin/'+$ghcWrapper)}
 foreach($ghcShortcut in $ghcShortcutSpecs){
  if(Test-Path -LiteralPath $ghcShortcut.path){$ghcShortcutBackup=Join-Path $ghcBackup ('shortcut-'+[guid]::NewGuid().ToString()+'.lnk');Copy-Item -LiteralPath $ghcShortcut.path -Destination $ghcShortcutBackup;$ghcBackups.Add([pscustomobject]@{target=$ghcShortcut.path;backup=$ghcShortcutBackup;sha256=(Get-FileHash -LiteralPath $ghcShortcutBackup).Hash.ToLowerInvariant()})}
  $ghcLink=$ghcShell.CreateShortcut($ghcShortcut.path);$ghcLink.TargetPath=$ghcPwsh;$ghcLink.Arguments=$ghcShortcut.arguments;$ghcLink.WorkingDirectory='D:\GHC-Family-Laboratory';$ghcLink.Description=$ghcShortcut.description;$ghcLink.IconLocation=$ghcPwsh+',0';$ghcLink.Save()
  $ghcVerified=$ghcShell.CreateShortcut($ghcShortcut.path);if($ghcVerified.TargetPath -ne $ghcPwsh -or $ghcVerified.Arguments -ne $ghcShortcut.arguments){throw 'Shortcut readback mismatch'}
 }
 $ghcPathParts=@($ghcUserPathBefore -split ';' | Where-Object {$_})
 if($ghcBin -notin $ghcPathParts){[Environment]::SetEnvironmentVariable('Path',(($ghcPathParts+$ghcBin) -join ';'),'User')}
 foreach($ghcFile in $ghcFiles){if((Get-Item -LiteralPath $ghcFile.target).Length -ne $ghcFile.bytes -or (Get-FileHash -LiteralPath $ghcFile.target).Hash.ToLowerInvariant() -ne $ghcFile.sha256){throw 'Installed release differs from the frozen manifest'}}
 if((Get-FileHash -LiteralPath $ghcAdminTarget).Hash.ToLowerInvariant() -ne $ghcNewAdminHash){throw 'Shared launcher final readback mismatch'}
 $ghcReceipt.status='installed';$ghcReceipt.completedAt=[datetime]::UtcNow.ToString('o');$ghcReceipt.userPathAfter=[Environment]::GetEnvironmentVariable('Path','User')
} catch {
 $ghcReceipt.status='failed';$ghcReceipt.failureType=$_.Exception.GetType().FullName
 throw
} finally {
 $ghcReceipt | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $ghcBackup 'receipt.json') -Encoding utf8
}
$ghcReceipt | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $ghcBank 'hub-installation.json') -Encoding utf8
[ordered]@{status=$ghcReceipt.status;version=$ghcManifest.version;destination=$ghcDestination;files=$ghcFiles.Count;backup=$ghcBackup;appRestarted=$false;newTerminalForPath=$true}|ConvertTo-Json
