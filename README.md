# Pro Multi-Tab Notepad

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Pro Multi-Tab Notepad は、Python と CustomTkinter を使用して構築された、モダンで高機能なマルチタブ型テキストエディタです。
シンプルなテキスト編集から、プログラミング（Python, HTML, CSS, JavaScript）や Markdown の作成・プレビューまで幅広く対応しています。

---

## 🌟 主な特徴

- **モダンな UI**: ダークモード/ライトモードを完全サポートした洗練されたデザイン。
- **マルチタブ管理**: 複数のファイルを同時に開き、快適に切り替えて作業できます。
- **強力な Markdown 支援**:
  - **プレビュー機能**: 編集モードとプレビューモードをワンクリックで切り替え可能。
  - 見出し、太字、コードブロックなどの視覚的なレンダリングに対応。
- **コーディング支援**:
  - **シンタックスハイライト**: Python, HTML, CSS, JS, Markdown に対応。
  - **行番号表示**: リアルタイムで更新される行番号エリア。
  - **グリッド表示**: 水平・垂直のガイド線（罫線）を表示可能。
  - **現在行強調**: カーソル行をハイライトし、視認性を向上。
- **検索機能**: リアルタイムハイライトと前後へのナビゲーション。
- **多言語対応 (i18n)**: 日本語と英語の UI 切り替えに対応。
- **自動ディレクトリ作成**: ユーザーのホームディレクトリに専用の保存フォルダを自動作成。

## 🚀 はじめかた

### 1. 動作環境
- Python 3.8 以上

### 2. ライブラリのインストール
ターミナルまたはコマンドプロンプトで以下のコマンドを実行してください。

```bash
pip install customtkinter
```

### 3. アプリの起動

メインスクリプトを実行します。

```bash
python my_notepad_app.py
```

## ⌨️ ショートカットキー

|キー組合せ|機能|
|Ctrl + N|新規タブの作成|
|Ctrl + O|ファイルを開く|
|Ctrl + S|ファイルを保存|
|Ctrl + F|検索パネルの表示/非表示|
|"Ctrl + ,"|設定画面の表示/非表示|
|Ctrl + L|行番号の表示/非表示を切り替え|
|Ctrl + G|罫線（グリッド）の表示/非表示を切り替え|
|Ctrl + H|現在行ハイライトの有効/無効を切り替え|

## ⚙️ 設定オプション
設定画面（Ctrl + ,）から以下の項目を自由にカスタマイズし、即座に反映させることができます。

- 外観: ライトモード / ダークモード。

- エディタ: フォントサイズ変更、各種視覚ガイド（行番号・罫線・強調）の ON/OFF。

- ファイル: デフォルトの保存先ディレクトリ。

- 言語: 日本語 / 英語。

## 📁 専用フォルダについて
初回起動時に、利便性のために以下のディレクトリが自動的に作成され、デフォルトの保存先として設定されます。

パス: ~/ProMultiTabNotepad (ユーザーホームディレクトリ内)

## 🛠 開発者向け情報
このアプリは Mixin パターン を採用しており、機能ごとに独立したクラスで構成されています。

- TabOperationsMixin: タブ操作（追加・削除・切替）。

- FileOperationsMixin: ファイル I/O。

- SearchOperationsMixin: 検索 UI およびロジック。

- SettingsOperationsMixin: 設定値の管理と UI 制御。

## 📄 ライセンス
このプロジェクトは MIT License のもとで公開されています。

Produced with passion for clean coding.