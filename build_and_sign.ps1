# build_and_sign.ps1
# アプリケーションをビルドして署名するスクリプト（インストーラー対応版）

Write-Host "=== Pro Multi-Tab Notepad - Build & Sign ===" -ForegroundColor Cyan
Write-Host ""

# config.py から APP_VERSION を抽出
Write-Host "Extracting version from config.py..." -ForegroundColor Gray
$versionMatch = Select-String -Path "config.py" -Pattern 'APP_VERSION\s*=\s*"([^"]+)"'
if ($versionMatch) {
    $appVersion = $versionMatch.Matches.Groups[1].Value
    Write-Host "✓ App Version: $appVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Could not extract version from config.py" -ForegroundColor Red
    exit 1
}

# 設定
$certPath = "CodeSigningCert.pfx"
$exeName = "Pro-Multi-Tab-Notepad.exe"
$exePath = "dist\$exeName"
$specFile = "my_notepad_app.spec"
$mainScript = "Pro-Multi-Tab-Notepad.py"
$nsiScript = "installer.nsi"
$installerExe = "Pro-Multi-Tab-Notepad-Installer-v$appVersion.exe"

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

# ステップ3: 署名（EXE）
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

# ステップ4: NSIS インストーラーの生成
Write-Host ""
Write-Host "Step 4: Building NSIS installer..." -ForegroundColor Cyan
Write-Host ""

# NSIS の存在確認
$nsisPath = "C:\Program Files (x86)\NSIS\makensis.exe"
if (-not (Test-Path $nsisPath)) {
    Write-Host "⚠ NSIS not found at default location" -ForegroundColor Yellow
    Write-Host "Searching for makensis.exe in PATH..." -ForegroundColor Gray
    $nsisPath = (Get-Command makensis.exe -ErrorAction SilentlyContinue).Source
    if (-not $nsisPath) {
        Write-Host "✗ NSIS not found!" -ForegroundColor Red
        Write-Host "Please install NSIS from: https://nsis.sourceforge.io/" -ForegroundColor Yellow
        Write-Host "Skipping installer creation..." -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Signed executable is available at: $exePath" -ForegroundColor Green
        exit 0
    }
}

Write-Host "✓ Found NSIS: $nsisPath" -ForegroundColor Green

# NSIS でインストーラーをビルド
Write-Host "Compiling installer with version $appVersion..." -ForegroundColor Gray
try {
    $nsisArgs = @("/DAPP_VERSION=$appVersion", $nsiScript)
    $nsisProcess = Start-Process -FilePath $nsisPath -ArgumentList $nsisArgs -Wait -NoNewWindow -PassThru
    
    if ($nsisProcess.ExitCode -ne 0) {
        Write-Host "✗ NSIS compilation failed!" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✓ Installer created successfully!" -ForegroundColor Green
} catch {
    Write-Host "✗ NSIS error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# インストーラーの存在確認
if (-not (Test-Path $installerExe)) {
    Write-Host "✗ Installer not found: $installerExe" -ForegroundColor Red
    exit 1
}

# ステップ5: インストーラーに署名
Write-Host ""
Write-Host "Step 5: Signing installer..." -ForegroundColor Cyan
Write-Host ""

& "$PSScriptRoot\sign_executable.ps1" -ExePath $installerExe -CertPath $certPath -CertPassword $password

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "⚠ Warning: Installer signature verification failed, but the file is signed." -ForegroundColor Yellow
    Write-Host ""
}

# 完了
Write-Host ""
Write-Host "=== Build Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "✓ Signed executable: $exePath" -ForegroundColor White
Write-Host "✓ Signed installer: $installerExe" -ForegroundColor White
Write-Host ""
$exeSize = (Get-Item $exePath).Length / 1MB
$installerSize = (Get-Item $installerExe).Length / 1MB
Write-Host "Executable size: $([math]::Round($exeSize, 2)) MB" -ForegroundColor Gray
Write-Host "Installer size: $([math]::Round($installerSize, 2)) MB" -ForegroundColor Gray
Write-Host ""
Write-Host "You can now distribute these signed files!" -ForegroundColor Green
Write-Host ""

# オプション: 実行する
$run = Read-Host "Run the installer now? (Y/N)"
if ($run -eq "Y" -or $run -eq "y") {
    Start-Process -FilePath (Resolve-Path $installerExe)
}
