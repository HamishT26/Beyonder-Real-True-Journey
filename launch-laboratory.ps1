$ErrorActionPreference = 'Stop'
$ghcLabRoot = 'D:\GHC-Family-Laboratory'
$ghcCurrent = Get-Content -LiteralPath (Join-Path $ghcLabRoot 'current.json') -Raw | ConvertFrom-Json
$ghcRelease = [IO.Path]::GetFullPath($ghcCurrent.release)
$ghcReleasePrefix = [IO.Path]::GetFullPath((Join-Path $ghcLabRoot 'releases')) + [IO.Path]::DirectorySeparatorChar
if (-not $ghcRelease.StartsWith($ghcReleasePrefix, [StringComparison]::OrdinalIgnoreCase)) { throw 'Release outside the laboratory bank' }
$ghcManifest = Join-Path $ghcRelease 'release-manifest.json'
if ((Get-FileHash -LiteralPath $ghcManifest -Algorithm SHA256).Hash.ToLowerInvariant() -ne $ghcCurrent.manifest_sha256) { throw 'Release manifest changed' }
$env:GHC_LAB_MOUNTS = Join-Path $ghcLabRoot 'private\legacy-mounts.json'
$env:GHC_LAB_DB = Join-Path $ghcLabRoot 'private\evidence.sqlite'
$env:GHC_LAB_PIN = Join-Path $ghcLabRoot 'private\source-expectation.json'
$ghcExisting = Get-NetTCPConnection -LocalAddress '127.0.0.1' -LocalPort 43177 -State Listen -ErrorAction SilentlyContinue
if ($ghcExisting) { Write-Output 'A loopback service already owns port 43177; it was not replaced.'; return }
$ghcNode = 'D:\GHC-Archives\global-tools\node\26.10.0\node-v26.10.0-win-x64\node.exe'
$ghcServer = Join-Path $ghcRelease 'laboratory\server.js'
$ghcProcess = Start-Process -FilePath $ghcNode -ArgumentList $ghcServer -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $ghcLabRoot 'private\server.stdout.txt') -RedirectStandardError (Join-Path $ghcLabRoot 'private\server.stderr.txt')
@{pid=$ghcProcess.Id;release=$ghcRelease;port=43177} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $ghcLabRoot 'private\server-process.json') -Encoding utf8
Write-Output 'GHC Family Laboratory: http://127.0.0.1:43177/'
