[CmdletBinding()]
param([switch]$CurrentUser,[switch]$Check)
$ErrorActionPreference = 'Stop'
$node = 'D:\GHC-Archives\global-tools\node\26.10.0\node-v26.10.0-win-x64\node.exe'
$pwsh = 'D:\GHC-Archives\global-tools\powershell\7.6.6\pwsh.exe'
$entry = Join-Path $PSScriptRoot 'hub.mjs'
$work = 'D:\GHC-Family-Laboratory'
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
foreach ($file in @($node,$pwsh,$entry)) { if (-not (Test-Path -LiteralPath $file -PathType Leaf)) { throw "Required launcher file is unavailable: $file" } }
if ($Check) {
    [ordered]@{schema='ghc.hub.launcher-check.v1';administrator=$isAdmin;uacRequired=(-not $CurrentUser -and -not $isAdmin);node=$node;entry=$entry;workingDirectory=$work;launchPerformed=$false} | ConvertTo-Json
    return
}
if (-not $CurrentUser -and -not $isAdmin) {
    $signature = Get-AuthenticodeSignature -LiteralPath $pwsh
    if ($signature.Status -ne 'Valid' -or $signature.SignerCertificate.Subject -notmatch 'Microsoft Corporation') { throw 'Pinned PowerShell signature is not valid.' }
    $argsString = '-NoLogo -NoProfile -NoExit -File "' + $PSCommandPath + '" -CurrentUser'
    # This is the interactive terminal explicitly selected by the user.
    Start-Process -FilePath $pwsh -Verb RunAs -ArgumentList $argsString -WorkingDirectory $work -WindowStyle Normal | Out-Null
    return
}
$env:GHC_HUB_HOME = 'D:\GHC-Archives\phase-banks\ghc-hub'
$env:GHC_HUB_WORKSPACE = $work
Set-Location -LiteralPath $work
& $node $entry menu
exit $LASTEXITCODE
