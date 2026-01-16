# sign_executable.ps1
# EXEファイルに署名するスクリプト

param(
    [Parameter(Mandatory=$false)]
    [string]$ExePath = "dist\my_notepad_app.exe",
    
    [Parameter(Mandatory=$false)]
    [string]$CertPath = "CodeSigningCert.pfx",
    
    [Parameter(Mandatory=$false)]
    [string]$CertPassword = "",
    
    [Parameter(Mandatory=$false)]
    [string]$TimestampServer = "http://timestamp.comodoca.com/authenticode"
)

Write-Host "=== Code Signing Tool ===" -ForegroundColor Cyan
Write-Host ""

# パスを絶対パスに変換
$ExePath = Join-Path $PSScriptRoot $ExePath
$CertPath = Join-Path $PSScriptRoot $CertPath

# ファイルの存在確認
if (-not (Test-Path $ExePath)) {
    Write-Host "✗ Error: Executable not found: $ExePath" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $CertPath)) {
    Write-Host "✗ Error: Certificate not found: $CertPath" -ForegroundColor Red
    Write-Host "Run create_certificate.ps1 first!" -ForegroundColor Yellow
    exit 1
}

# signtoolの検索
$possiblePaths = @(
    "C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe",
    "C:\Program Files (x86)\Windows Kits\10\bin\10.0.22000.0\x64\signtool.exe",
    "C:\Program Files (x86)\Windows Kits\10\bin\10.0.19041.0\x64\signtool.exe"
)

$signtool = $null
foreach ($path in $possiblePaths) {
    if (Test-Path $path) {
        $signtool = $path
        break
    }
}

if (-not $signtool) {
    # 検索してみる
    Write-Host "Searching for signtool.exe..." -ForegroundColor Yellow
    $found = Get-ChildItem "C:\Program Files (x86)\Windows Kits" -Recurse -Filter "signtool.exe" -ErrorAction SilentlyContinue | 
             Where-Object { $_.FullName -match "x64" } | 
             Select-Object -First 1
    
    if ($found) {
        $signtool = $found.FullName
    }
}

if (-not $signtool) {
    Write-Host "✗ Error: signtool.exe not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Windows SDK from:" -ForegroundColor Yellow
    Write-Host "https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/" -ForegroundColor White
    Write-Host ""
    Write-Host "Or install via Chocolatey:" -ForegroundColor Yellow
    Write-Host "choco install windows-sdk-10 -y" -ForegroundColor White
    exit 1
}

Write-Host "Using signtool: $signtool" -ForegroundColor Gray
Write-Host ""

# パスワードの入力（指定されていない場合）
if ([string]::IsNullOrEmpty($CertPassword)) {
    $securePassword = Read-Host -Prompt "Enter certificate password" -AsSecureString
    $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword)
    $CertPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
}

Write-Host "Signing executable: $(Split-Path $ExePath -Leaf)" -ForegroundColor Yellow
Write-Host "Certificate: $(Split-Path $CertPath -Leaf)" -ForegroundColor Gray
Write-Host ""

# 署名を実行
$arguments = @(
    "sign",
    "/f", "`"$CertPath`"",
    "/p", $CertPassword,
    "/t", $TimestampServer,
    "/fd", "SHA256",
    "/v",
    "`"$ExePath`""
)

try {
    $process = Start-Process -FilePath $signtool -ArgumentList $arguments -Wait -NoNewWindow -PassThru
    
    if ($process.ExitCode -eq 0) {
        Write-Host ""
        Write-Host "✓ Successfully signed: $ExePath" -ForegroundColor Green
        Write-Host ""
        
        # 署名を確認
        Write-Host "Verifying signature..." -ForegroundColor Yellow
        $verifyArgs = @("verify", "/pa", "/v", "`"$ExePath`"")
        Start-Process -FilePath $signtool -ArgumentList $verifyArgs -Wait -NoNewWindow
        
    } else {
        Write-Host ""
        Write-Host "✗ Signing failed with exit code: $($process.ExitCode)" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "✗ Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
