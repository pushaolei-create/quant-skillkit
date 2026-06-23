param(
    [string]$BaseUrl = "http://127.0.0.1:8010",
    [string]$OutputPath = ""
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$Python = "C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

if (-not (Test-Path -LiteralPath $Python)) {
    throw "Python runtime not found: $Python"
}

if (-not $OutputPath) {
    $OutputPath = Join-Path $PSScriptRoot "hermes-tool-manifest.generated.json"
}

Set-Location -LiteralPath $Root
$json = & $Python -m quant_skillkit.cli manifest --base-url $BaseUrl
[System.IO.File]::WriteAllText($OutputPath, $json, [System.Text.UTF8Encoding]::new($false))
Write-Output $OutputPath
