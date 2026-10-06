[CmdletBinding()]
param([switch]$CurrentUser,[switch]$Check)
$ErrorActionPreference='Stop'
$ghcCmd=Join-Path ([Environment]::SystemDirectory) 'cmd.exe'
$ghcEntry=Join-Path $PSScriptRoot 'Start-GhcCmdHub.cmd'
$ghcNode='D:\GHC-Archives\global-tools\node\26.10.0\node-v26.10.0-win-x64\node.exe'
$ghcHub=Join-Path $PSScriptRoot 'hub.mjs'
$ghcWork='D:\GHC-Family-Laboratory'
$ghcAdmin=([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
foreach($ghcPath in @($ghcCmd,$ghcEntry,$ghcNode,$ghcHub)){
 if(-not (Test-Path -LiteralPath $ghcPath -PathType Leaf)){throw "Required CMD launcher file is unavailable: $ghcPath"}
}
if(-not (Test-Path -LiteralPath $ghcWork -PathType Container)){throw 'Laboratory directory is unavailable'}
if($ghcEntry -match '["%\r\n]'){throw 'Unsupported characters in CMD launcher path'}
$ghcSignature=Get-AuthenticodeSignature -LiteralPath $ghcCmd
if($ghcSignature.Status -ne 'Valid' -or $ghcSignature.SignerCertificate.Subject -notmatch 'Microsoft Windows'){throw 'Windows Command Prompt signature is not valid'}
$ghcArgs='/d /q /k ""'+$ghcEntry+'""'
if($Check){
 [ordered]@{schema='ghc.nexus.cmd-launch.v1';command=$ghcCmd;arguments=$ghcArgs;node=$ghcNode;hub=$ghcHub;dependenciesPresent=$true;currentProcessAdministrator=$ghcAdmin;elevationRequested=(-not $CurrentUser);uacRequired=(-not $CurrentUser -and -not $ghcAdmin);workingDirectory=$ghcWork;launchPerformed=$false;cloudPrivilegesChanged=$false}|ConvertTo-Json
 return
}
# This is the interactive terminal explicitly selected by the user.
if(-not $CurrentUser -and -not $ghcAdmin){
 Start-Process -FilePath $ghcCmd -ArgumentList $ghcArgs -Verb RunAs -WorkingDirectory $ghcWork -WindowStyle Normal | Out-Null
}else{
 Start-Process -FilePath $ghcCmd -ArgumentList $ghcArgs -WorkingDirectory $ghcWork -WindowStyle Normal | Out-Null
}
