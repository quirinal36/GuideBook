# Makefile 과 같은 기능 (make 가 없는 Windows 용)
# 사용법: .\build.ps1 html | epub | pdf | all | qr | check | todo | placeholders | serve | clean
param([string]$Target = "all")
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

function Invoke-Step([string]$exe, [string[]]$argv) {
    & $exe @argv
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
function Qr    { Invoke-Step python @("scripts/gen_qr.py") }
function Check { Invoke-Step python @("scripts/check_figures.py") }

switch ($Target) {
    "all"          { Qr; Check; Invoke-Step quarto @("render") }
    "html"         { Qr; Invoke-Step quarto @("render", "--to", "html") }
    "epub"         { Qr; Invoke-Step quarto @("render", "--to", "epub") }
    "pdf"          { Qr; Invoke-Step quarto @("render", "--to", "typst") }
    "qr"           { Qr }
    "check"        { Check }
    "todo"         { Invoke-Step python @("scripts/check_figures.py", "--todo") }
    "placeholders" { Invoke-Step python @("scripts/make_placeholders.py") }
    "serve"        { Qr; Invoke-Step quarto @("preview") }
    "clean"        { Remove-Item -Recurse -Force -ErrorAction SilentlyContinue _book, .quarto }
    default        { Write-Error "알 수 없는 대상: $Target" }
}
