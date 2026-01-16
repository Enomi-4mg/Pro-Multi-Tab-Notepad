# Pro Multi-Tab Notepad

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-orange.svg)

Pro Multi-Tab Notepad は、Python と CustomTkinter を使用して構築された、理系学生・エンジニア向けのマルチタブ型テキストエディタです。
通常のテキスト編集に加え、LaTeX 数式、化学構造式（mhchem）のリアルタイムプレビューに対応しています。

---

## 🌟 主な特徴

### 📝 理系特化 Markdown 支援
- **LaTeX 数式**: 高度な数学記号・積分のレンダリングに対応
- **化学式 (mhchem)**: 分子式 $\ce{H2O}$ や反応式 $\ce{2H2 + O2 -> 2H2O}$ を美しく表示
- **ブラウザプレビュー**: ワンクリック（`Ctrl+Shift+P`）でスタイリッシュな HTML プレビューを表示

### 🔄 ライブ・プレビュー機能
- **自動更新プレビュー**: 編集内容を自動的にブラウザプレビューに反映（設定可能な間隔）
- **更新間隔のカスタマイズ**: 設定画面から1秒〜60秒の範囲で自由に調整可能
- **相対パスプレビュー**: `<base>` タグの動的挿入により、ローカル画像を正しく表示
- **再読み込み不要**: 保存操作なしで最新の LaTeX や Markdown を確認可能

### ✏️ Markdown 編集ツールバー **NEW**
- **コンテキスト対応**: .md ファイル編集時のみ、専用の補助ツールバーが出現
- **直感操作**: 見出し（H1/H2）、太字、斜体、箇条書き、テーブル雛形をワンクリック挿入
- **選択範囲対応**: テキストを選択してボタンを押すと、選択範囲を囲むようにタグを挿入
- **動的レイアウト**: タブバーや行番号と干渉しない独立したグリッド配置

### 📥 万能インポート機能（Bundle形式） **NEW**
- **スマート変換**: .docx や .html をワンクリックで Markdown へ変換
- **アセット管理**: 変換時に `[ファイル名]_bundle` フォルダを自動生成し、画像を `assets/` へ自動抽出
- **リンク自動解決**: Markdown 内の画像パスを相対パス（`assets/image.png`）に自動書き換え
- **選択的インポート**: HTML/CSS を開く際、Markdown変換か直接編集かを選択可能

### 💻 コーディング支援
- **シンタックスハイライト**: Python, HTML, CSS, JavaScript, Markdown に対応
- **視覚ガイド**: 行番号表示、グリッド線表示、現在行ハイライト機能
- **検索機能**: リアルタイムハイライトと前後へのナビゲーション

### ⚙️ 設定管理 & UI/UX **NEW**
- **設定のエクスポート/インポート**: 設定を JSON ファイルとして保存・読み込み可能
- **設定の永続化**: アプリ終了時に自動保存、次回起動時に復元
- **バックアップ機能**: 設定ファイルの自動バックアップ（`settings.json.bak`）
- **最近使ったファイル**: 最大10件のファイル履歴を保持
- **ショートカット・ツールチップ**: ボタンホバーで対応するショートカットキーを表示
- **ダークモード/ライトモード**: 完全な外観切り替え対応

### 🌐 その他の機能
- **多言語対応 (i18n)**: 日本語と英語の UI 切り替え
- **自動ディレクトリ作成**: ユーザーのホームディレクトリに専用の保存フォルダを自動作成
- **自動アップデート確認**: GitHub API を利用し、最新版がある場合に通知を表示

## 📁 Bundle形式のディレクトリ構造

インポート機能を利用すると、アセットを含めたプロジェクト管理が容易になります。

```text
[ファイル名]_bundle/
├── index.md        # 変換されたMarkdown本体
└── assets/         # 抽出された画像ファイル群
```

## ⌨️ ショートカットキー

| キー組合せ | 機能 |
| :---: | :---: |
| Ctrl + N | 新規タブの作成 |
| Ctrl + O | ファイルを開く |
| Ctrl + S | ファイルを保存 |
| Ctrl + Shift + S | 名前を付けて保存 |
| Ctrl + Shift + P | Markdown プレビュー表示 |
| Ctrl + Z | Undo |
| Ctrl + Shift + Z | Redo |
| Ctrl + F | 検索パネルの表示/非表示 |
| Ctrl + , | 設定画面の表示/非表示 |
| Ctrl + L | 行番号の表示/非表示 |
| Ctrl + G | 罫線（グリッド）の表示/非表示 |
| Ctrl + H | 現在行強調の ON/OFF |

## ⚙️ 設定オプション

設定ボタン（⚙️）、または設定画面（`Ctrl + ,`）から以下の項目を自由にカスタマイズし、即座に反映させることができます。

### 外観
- **テーマモード**: ライトモード / ダークモードの切り替え

### エディタ設定
- **フォントサイズ**: 8px〜40px の範囲で調整可能（スライダー）
- **行番号を表示**: エディタ左側に行番号を表示
- **罫線を表示**: テキストエリアにグリッド線を表示
- **カレント行を強調**: 現在カーソルがある行をハイライト表示

### プレビュー設定 **NEW**
- **自動更新の間隔**: Markdownプレビューの自動更新間隔を1秒〜60秒の範囲で設定可能

### ファイル設定
- **デフォルトの保存先**: 新規ファイルの保存先ディレクトリを指定

### 言語設定開発者向けコマンド実行手順

## 🚀 はじめかた

### 1. 動作環境
- Python 3.8 以上

### 2. ライブラリのインストール
ターミナルまたはコマンドプロンプトで以下のコマンドを実行してください。

```bash
pip install -r requirements.txt
```

### 3. アプリの起動

メインスクリプトを実行します。

```bash
python Pro-Multi-Tab-Notepad.py
```

### 4. ローカルでのビルド（開発者向け）

署名付き実行ファイルとインストーラーを作成するには：

**前提条件**：
- NSIS がインストールされていること（[公式サイト](https://nsis.sourceforge.io/)からダウンロード）
- コード署名証明書（自己署名証明書は `.\create_certificate.ps1` で生成可能）

**ビルド手順**：

```powershell
# 1. 証明書の生成（初回のみ）
.\create_certificate.ps1

# 2. 証明書の信頼ストアへの追加（初回のみ）
.\fix_cert_trust.ps1

# 3. ビルドと署名の実行
.\build_and_sign.ps1
```

このスクリプトは以下を自動実行します：
1. config.py からバージョン番号を抽出
2. PyInstaller で `Pro-Multi-Tab-Notepad.exe` をビルド
3. EXE ファイルに署名
4. NSIS でインストーラーを生成
5. インストーラーに署名

**成果物**：
- `dist\Pro-Multi-Tab-Notepad.exe`（署名済み実行ファイル）
- `Pro-Multi-Tab-Notepad-Installer-v*.exe`（署名済みインストーラー）

### 5. GitHub Actions での自動ビルド（開発者向け）

タグをプッシュすると、GitHub Actions が自動的にビルドとリリースを実行します：

```powershell
# バージョンタグを作成してプッシュ
git tag v1.6.3
git push origin v1.6.3
```

ビルドされた成果物は自動的に GitHub Releases に公開されます。

**必要な GitHub Secrets**：
- `CERT_BASE64`: 証明書の Base64 エンコード文字列
- `CERT_PASSWORD`: 証明書のパスワード

詳細は [SECURITY.md](SECURITY.md) を参照してください。📦 インストール方法

### インストーラー版（推奨）

1. [GitHub Releases](https://github.com/EnoMi-4mg/Pro-Multi-Tab-Notepad/releases) から最新の `Pro-Multi-Tab-Notepad-Installer-v*.exe` をダウンロード
2. インストーラーを実行（管理者権限が必要です）
3. インストール先を選択（デフォルト: `C:\Program Files\Pro-Multi-Tab-Notepad`）
4. ファイル関連付けが自動的に設定されます（`.txt`, `.md`, `.html`, `.css`, `.py`）
5. スタートメニューとデスクトップにショートカットが作成されます

**インストーラーの特徴**：
- ✅ ファイルのダブルクリックで Pro Multi-Tab Notepad が起動
- ✅ スタートメニューから簡単に起動
- ✅ デスクトップショートカット
- ✅ アンインストーラー付属（設定の保持/削除を選択可能）
- ✅ デジタル署名済み（発行者: EnoMi-4mg, Personal）

##**TabOperationsMixin**: タブ操作（追加・削除・切替）
- **FileOperationsMixin**: ファイル I/O
- **SearchOperationsMixin**: 検索 UI およびロジック
- **SettingsOperationsMixin**: 設定値の管理と UI 制御
- **MarkdownEditMixin**: Markdown 編集ツールバー
- **ImportOperationsMixin**: ファイルインポート（Bundle形式）
**スタンドアロン版の特徴**：
- ✅ USB メモリなどで持ち運び可能
- ✅ インストール不要
- ⚠️ ファイル関連付けは手動設定が必要

### アンインストール方法

**インストーラー版の場合**：

1. Windows の「設定」→「アプリ」→「インストールされているアプリ」から「Pro Multi-Tab Notepad」を選択
2. 「アンインストール」をクリック
3. ユーザーデータの削除を選択：
   - チェックあり：設定ファイルも完全に削除
   - チェックなし：設定ファイルを保持（再インストール時に設定が復元されます）
初回起動時に、利便性のために以下のディレクトリが自動的に作成され、デフォルトの保存先として設定されます。

パス: ~/ProMultiTabNotepad (ユーザーホームディレクトリ内)

## Releaseにて.exeファイルを公開中・以下の手順はコマンドで実行するもの

## 🚀 はじめかた

### 1. 動作環境
- Python 3.8 以上

### 2. ライブラリのインストール
ターミナルまたはコマンドプロンプトで以下のコマンドを実行してください。

```bash
pip install -r requirements.txt
```

### 3. アプリの起動

メインスクリプトを実行します。

```bash
python my_notepad_app.py
```

## 🛠 開発者向け情報
このアプリは Mixin パターン を採用しており、機能ごとに独立したクラスで構成されています。

- TabOperationsMixin: タブ操作（追加・削除・切替）。

- FileOperationsMixin: ファイル I/O。

- SearchOperationsMixin: 検索 UI およびロジック。

- SettingsOperationsMixin: 設定値の管理と UI 制御。

## 🛠 技術スタック
- GUI: CustomTkinter
**GUI**: CustomTkinter
- **Markdown**: markdown2 (with extras)
- **Math/Chemistry**: MathJax 3.0 (mhchem extension)
- **Document Conversion**: pypandoc
- **Automation**: GitHub Actions (PyInstaller build)

## 📄 ライセンス

このプロジェクトは MIT License のもとで公開されています。
詳細は [LICENSE.txt](LICENSE.txt) をご覧ください。

Copyright (c) 2026 EnoMi-4mg

---
Produced with passion for clean coding.
