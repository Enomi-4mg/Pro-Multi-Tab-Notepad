# sign_executable.ps1
# EXEファイルに署名するスクリプト

param(
    [Parameter(Mandatory=$true)]
    [string]$ExePath,
    
    [Parameter(Mandatory=$true)]
    [string]$CertPath,
    
    [Parameter(Mandatory=$true)]
    [string]$CertPassword,
    
    [Parameter(Mandatory=$false)]
    [string]$TimestampServer = "http://timestamp.digicert.com"
)

Write-Host "=== Code Signing Tool ===" -ForegroundColor Cyan
Write-Host ""

# パラメータ表示
Write-Host "Parameters received:" -ForegroundColor Gray
Write-Host "  ExePath: $ExePath" -ForegroundColor Gray
Write-Host "  CertPath: $CertPath" -ForegroundColor Gray
Write-Host ""

# ファイルの存在確認
if (-not (Test-Path $ExePath)) {
    Write-Host "✗ Error: File not found: $ExePath" -ForegroundColor Red
    Write-Host "Current directory: $(Get-Location)" -ForegroundColor Gray
    if (Test-Path "dist") {
        Write-Host "Files in dist:" -ForegroundColor Gray
        Get-ChildItem "dist" -Filter "*.exe" | ForEach-Object { 
            Write-Host "  - $($_.Name)" -ForegroundColor Yellow
        }
    }
    Write-Error "Executable not found: $ExePath"
    exit 1
}

if (-not (Test-Path $CertPath)) {
    Write-Host "✗ Error: Certificate not found: $CertPath" -ForegroundColor Red
    Write-Error "Certificate not found: $CertPath"
    exit 1
}

Write-Host "✓ Files verified" -ForegroundColor Green
Write-Host ""

# signtool の検索
Write-Host "Searching for signtool.exe..." -ForegroundColor Gray
$signtool = $null

$possiblePaths = @(
    "C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64\signtool.exe",
    "C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe",
    "C:\Program Files (x86)\Windows Kits\10\bin\10.0.22000.0\x64\signtool.exe",
    "C:\Program Files (x86)\Windows Kits\10\bin\10.0.19041.0\x64\signtool.exe"
)

foreach ($path in $possiblePaths) {
    if (Test-Path $path) {
        $signtool = $path
        Write-Host "✓ Found: $signtool" -ForegroundColor Green
        break
    }
}

if (-not $signtool) {
    Write-Host "Searching recursively..." -ForegroundColor Yellow
    $found = Get-ChildItem "C:\Program Files (x86)\Windows Kits" -Recurse -Filter "signtool.exe" -ErrorAction SilentlyContinue | 
             Where-Object { $_.FullName -match "x64" } | 
             Select-Object -First 1
    
    if ($found) {
        $signtool = $found.FullName
        Write-Host "✓ Found: $signtool" -ForegroundColor Green
    } else {
        Write-Host "✗ signtool.exe not found" -ForegroundColor Red
        Write-Error "signtool.exe not found"
        exit 1
    }
}

Write-Host ""

# 絶対パスに変換
$ExePath = (Resolve-Path $ExePath).Path
$CertPath = (Resolve-Path $CertPath).Path

Write-Host "Resolved absolute paths:" -ForegroundColor Gray
Write-Host "  ExePath: $ExePath" -ForegroundColor Gray
Write-Host "  CertPath: $CertPath" -ForegroundColor Gray
Write-Host ""

Write-Host "Signing with:" -ForegroundColor Cyan
Write-Host "  Tool: $signtool" -ForegroundColor Gray
Write-Host "  Timestamp: $TimestampServer" -ForegroundColor Gray
Write-Host ""

# 署名を実行
& $signtool sign /f "$CertPath" /p "$CertPassword" /tr "$TimestampServer" /td SHA256 /fd SHA256 /v "$ExePath"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✓ Successfully signed: $(Split-Path $ExePath -Leaf)" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "✗ Signing failed with exit code: $LASTEXITCODE" -ForegroundColor Red
    Write-Error "Code signing failed"
    exit $LASTEXITCODE
}
