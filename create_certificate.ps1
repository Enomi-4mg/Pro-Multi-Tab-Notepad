# create_certificate.ps1
# 自己署名証明書を作成するスクリプト
# WARNING: このスクリプトで生成された CodeSigningCert.pfx を Git にコミットしないでください！
# 秘密鍵を含むため、.gitignore で除外されています。

Write-Host "=== Code Signing Certificate Creator ===" -ForegroundColor Cyan
Write-Host "" -ForegroundColor Red
Write-Host "⚠️  WARNING: Generated certificate file will be in .gitignore" -ForegroundColor Red
Write-Host "Do NOT commit CodeSigningCert.pfx to version control!" -ForegroundColor Red
Write-Host ""

# 証明書の設定
$subject = "CN=EnoMi-4mg,O=Personal,C=JP"
$friendlyName = "Pro Multi-Tab Notepad Code Signing Certificate"
$years = 5
$certPath = Join-Path $PSScriptRoot "CodeSigningCert.pfx"

Write-Host "Creating self-signed certificate..." -ForegroundColor Yellow
Write-Host "Subject: $subject"
Write-Host "Valid for: $years years"
Write-Host ""

try {
    # 自己署名証明書を作成
    $cert = New-SelfSignedCertificate `
        -CertStoreLocation "Cert:\CurrentUser\My" `
        -Subject $subject `
        -FriendlyName $friendlyName `
        -KeyAlgorithm RSA `
        -KeyLength 2048 `
        -NotAfter (Get-Date).AddYears($years) `
        -Type CodeSigningCert `
        -KeyUsage DigitalSignature `
        -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.3")

    Write-Host "✓ Certificate created successfully!" -ForegroundColor Green
    Write-Host "  Thumbprint: $($cert.Thumbprint)"
    Write-Host ""

    # パスワードの入力
    Write-Host "Enter a password to protect the certificate file:" -ForegroundColor Yellow
    $password = Read-Host -AsSecureString

    # 証明書をPFXファイルにエクスポート
    Write-Host "Exporting certificate to PFX file..." -ForegroundColor Yellow
    Export-PfxCertificate -Cert $cert -FilePath $certPath -Password $password | Out-Null

    Write-Host "✓ Certificate exported to: $certPath" -ForegroundColor Green
    Write-Host ""

    # 信頼されたストアに追加
    Write-Host "Adding certificate to Trusted Publishers store..." -ForegroundColor Yellow
    $store = New-Object System.Security.Cryptography.X509Certificates.X509Store "TrustedPublisher", "CurrentUser"
    $store.Open([System.Security.Cryptography.X509Certificates.OpenFlags]::ReadWrite)
    $store.Add($cert)
    $store.Close()

    Write-Host "✓ Certificate added to Trusted Publishers!" -ForegroundColor Green
    Write-Host ""

    # 証明書情報を保存
    $certInfo = @{
        Thumbprint = $cert.Thumbprint
        Subject = $cert.Subject
        NotAfter = $cert.NotAfter.ToString("yyyy-MM-dd")
        Created = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    }

    $certInfo | ConvertTo-Json | Out-File (Join-Path $PSScriptRoot "cert_info.json")

    Write-Host "=== Setup Complete ===" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Certificate file: $certPath" -ForegroundColor White
    Write-Host "Save your password securely - you'll need it for signing!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Update build_and_sign.ps1 with your certificate password"
    Write-Host "2. Run: .\build_and_sign.ps1"
    Write-Host ""

} catch {
    Write-Host "✗ Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
