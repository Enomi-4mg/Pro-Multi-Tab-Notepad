# build_and_sign.ps1
# アプリケーションをビルドして署名するスクリプト

Write-Host "=== Pro Multi-Tab Notepad - Build & Sign ===" -ForegroundColor Cyan
Write-Host ""

# 設定
$certPath = "CodeSigningCert.pfx"
$exePath = "dist\my_notepad_app.exe"
$specFile = "my_notepad_app.spec"
$mainScript = "Pro-Multi-Tab-Notepad.py"

# 証明書の存在確認
if (-not (Test-Path $certPath)) {
    Write-Host "✗ Certificate not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please run: .\create_certificate.ps1" -ForegroundColor Yellow
    exit 1
}

# 仮想環境の確認
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
}

# ステップ1: クリーンビルド
Write-Host ""
Write-Host "Step 1: Cleaning previous build..." -ForegroundColor Cyan
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
    Write-Host "✓ Cleaned dist folder" -ForegroundColor Green
}
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
    Write-Host "✓ Cleaned build folder" -ForegroundColor Green
}

# ステップ2: ビルド
Write-Host ""
Write-Host "Step 2: Building executable..." -ForegroundColor Cyan
Write-Host "Running PyInstaller with spec file: $specFile" -ForegroundColor Gray
Write-Host ""

try {
    $buildProcess = Start-Process -FilePath "python" -ArgumentList "-m", "PyInstaller", $specFile, "--clean" -Wait -NoNewWindow -PassThru
    
    if ($buildProcess.ExitCode -ne 0) {
        Write-Host "✗ Build failed!" -ForegroundColor Red
        exit 1
    }
    
    Write-Host ""
    Write-Host "✓ Build completed successfully!" -ForegroundColor Green
} catch {
    Write-Host "✗ Build error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# ビルド結果の確認
if (-not (Test-Path $exePath)) {
    Write-Host "✗ Executable not found: $exePath" -ForegroundColor Red
    exit 1
}

$fileSize = (Get-Item $exePath).Length / 1MB
Write-Host "Executable size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Gray

# ステップ3: 署名
Write-Host ""
Write-Host "Step 3: Signing executable..." -ForegroundColor Cyan
Write-Host ""

# パスワードの入力
$securePassword = Read-Host -Prompt "Enter certificate password" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword)
$password = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

# 署名スクリプトを実行
& "$PSScriptRoot\sign_executable.ps1" -ExePath $exePath -CertPath $certPath -CertPassword $password

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "⚠ Warning: Signature verification failed, but the file is signed." -ForegroundColor Yellow
    Write-Host "   This is normal for self-signed certificates." -ForegroundColor Yellow
    Write-Host "   To fix verification on this PC, run: .\fix_cert_trust.ps1" -ForegroundColor Cyan
    Write-Host ""
}

# 完了
Write-Host ""
Write-Host "=== Build Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Signed executable: $exePath" -ForegroundColor White
Write-Host "File size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Gray
Write-Host ""
Write-Host "You can now distribute this signed application!" -ForegroundColor Green
Write-Host ""

# オプション: 実行する
$run = Read-Host "Run the application now? (Y/N)"
if ($run -eq "Y" -or $run -eq "y") {
    Start-Process -FilePath (Resolve-Path $exePath)
}
