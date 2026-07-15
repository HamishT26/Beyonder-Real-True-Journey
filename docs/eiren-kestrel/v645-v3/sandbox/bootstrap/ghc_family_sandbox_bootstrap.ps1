param(
  [Parameter(Mandatory=$true)][ValidateSet('eiren','ilyra','sable','orin','tamar','sylven')][string]$Owner
)

$ErrorActionPreference = 'Stop'
$principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
  throw 'Sandbox bootstrap requires administrative context inside the isolated sandbox.'
}

$outputRoot = "C:\GHC\Output\$Owner"
$workspace = "C:\GHC\Workspace\$Owner"
New-Item -ItemType Directory -Force -Path $outputRoot,$workspace | Out-Null

$receipt = [ordered]@{
  schema = 'ghc.family.sandbox-bootstrap.v1'
  owner_label = $Owner
  administrative_context_inside_sandbox = $true
  network_install_attempted = $false
  mapped_input_read_only_expected = $true
  package_results = @()
  boundary = 'This runtime receipt applies only to one ephemeral sandbox session and is not host-security certification.'
}

$manifestPath = 'C:\GHC\Bootstrap\offline-packages.json'
if (Test-Path -LiteralPath $manifestPath) {
  $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
  foreach ($package in $manifest.packages) {
    $candidate = Join-Path 'C:\GHC\Input' $package.file
    if (-not (Test-Path -LiteralPath $candidate)) { throw "Offline package missing: $($package.name)" }
    $digest = (Get-FileHash -LiteralPath $candidate -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($digest -ne $package.sha256.ToLowerInvariant()) { throw "Hash mismatch: $($package.name)" }
    $extension = [IO.Path]::GetExtension($candidate).ToLowerInvariant()
    if ($extension -notin @('.msi','.exe')) { throw "Unsupported offline installer type: $extension" }
    $process = Start-Process -FilePath $candidate -ArgumentList @($package.arguments) -Wait -PassThru -WindowStyle Hidden
    $receipt.package_results += [ordered]@{name=$package.name; sha256=$digest; exit_code=$process.ExitCode}
    if ($process.ExitCode -ne 0) { throw "Offline installer failed: $($package.name)" }
  }
}

$receipt | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $outputRoot 'bootstrap-receipt.json') -Encoding UTF8
