# セキュリティ ガイド

## 🔒 重要な注意事項

このプロジェクトはコード署名機能を含んでいます。以下のセキュリティ対策が実施されています。

## 📋 機密ファイル

次のファイルは **絶対に Git にコミットしてはいけません**：

| ファイル | 内容 | 状態 |
|---------|------|------|
| `CodeSigningCert.pfx` | コード署名証明書（秘密鍵を含む） | ✅ `.gitignore` で除外 |
| `.env` | パスワード・API キー | ✅ `.gitignore` で除外 |
| `passwords.txt` | 認証情報 | ✅ `.gitignore` で除外 |

## 🛡️ 安全な運用方法

### ローカル開発環境での使用

```powershell
# 1. 証明書を生成
.\create_certificate.ps1

# 2. 信頼ストアに追加
.\fix_cert_trust.ps1

# 3. ビルド & 署名
.\build_and_sign.ps1
```

### GitHub での自動署名リリース

GitHub Actions ワークフロー（`.github/workflows/release.yml`）が以下を自動実行します：

1. 証明書を GitHub Secrets から Base64 デコード
2. PyInstaller でビルド
3. `signtool.exe` で署名
4. 署名を検証
5. GitHub Releases に署名済み EXE をアップロード

#### GitHub Secrets の設定方法

1. **証明書を Base64 エンコード**:
   ```powershell
   [Convert]::ToBase64String([IO.File]::ReadAllBytes("CodeSigningCert.pfx")) | Set-Clipboard
   ```

2. **GitHub リポジトリで Secrets を登録**:
   - Settings → Secrets and variables → Actions
   - `CODE_SIGNING_CERT`: 上記でコピーした Base64 文字列
   - `CODE_SIGNING_PASSWORD`: 証明書のパスワード

3. **テスト用タグをプッシュ**:
   ```powershell
   git tag v1.5.0
   git push origin v1.5.0
   ```

## ✅ チェックリスト

新しい開発者がこのプロジェクトを使う場合：

- [ ] `.gitignore` が機密ファイルを除外していることを確認
- [ ] `CodeSigningCert.pfx` は **本人のローカル環境でのみ** 保管
- [ ] GitHub Secrets に証明書とパスワードを登録（Base64 エンコード済み）
- [ ] `git log` で機密ファイルが履歴に残っていないことを確認
- [ ] 個人の証明書は個人のみで使用（チーム内で共有しない）

## 🔍 確認コマンド

```powershell
# Git が追跡しているファイルを確認
git ls-files

# 機密ファイルが除外されているか確認
git check-ignore -v CodeSigningCert.pfx
git check-ignore -v .env

# 最近のコミットに機密ファイルがないか確認
git log --all --full-history -p -- CodeSigningCert.pfx
```

## ⚠️ 緊急対応

**万が一秘密鍵を誤ってコミットした場合:**

```powershell
# Git 履歴から完全に削除（全開発者の.gitをクリーン）
git filter-branch --tree-filter 'rm -f CodeSigningCert.pfx' -- --all
git push origin --force --all

# 古い証明書は使用不可にする
# 新しい証明書を生成し直す
.\create_certificate.ps1
```

---

**Last Updated**: 2026-01-16
**Status**: ✅ Secure Configuration
