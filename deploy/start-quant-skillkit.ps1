param(
    [string]$HostName = "127.0.0.1",
    [int]$Port = 8010
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$Python = "C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

if (-not (Test-Path -LiteralPath $Python)) {
    throw "Python runtime not found: $Python"
}

Set-Location -LiteralPath $Root
& $Python -m quant_skillkit.cli serve --host $HostName --port $Port
