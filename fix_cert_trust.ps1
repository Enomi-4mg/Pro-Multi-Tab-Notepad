# fix_cert_trust.ps1
# 証明書を信頼されたルート証明機関ストアに追加

Write-Host "=== Certificate Trust Fix ===" -ForegroundColor Cyan
Write-Host ""

# PFXファイルから証明書を読み込む
$certPath = Join-Path $PSScriptRoot "CodeSigningCert.pfx"

if (-not (Test-Path $certPath)) {
    Write-Host "✗ Certificate not found: $certPath" -ForegroundColor Red
    exit 1
}

Write-Host "Enter certificate password:" -ForegroundColor Yellow
$securePassword = Read-Host -AsSecureString

try {
    # PFXから証明書を読み込み
    $cert = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2($certPath, $securePassword)
    
    Write-Host ""
    Write-Host "Certificate Info:" -ForegroundColor Gray
    Write-Host "  Subject: $($cert.Subject)" -ForegroundColor Gray
    Write-Host "  Thumbprint: $($cert.Thumbprint)" -ForegroundColor Gray
    Write-Host ""
    
    # ルート証明機関ストアに追加
    Write-Host "Adding certificate to Trusted Root Certification Authorities..." -ForegroundColor Yellow
    $store = New-Object System.Security.Cryptography.X509Certificates.X509Store "Root", "CurrentUser"
    $store.Open([System.Security.Cryptography.X509Certificates.OpenFlags]::ReadWrite)
    $store.Add($cert)
    $store.Close()
    
    Write-Host "✓ Certificate added to Root store!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Now run: .\build_and_sign.ps1" -ForegroundColor Cyan
    Write-Host ""
    
} catch {
    Write-Host "✗ Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
