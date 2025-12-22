# Pro Multi-Tab Notepad

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Pro Multi-Tab Notepad は、Python と CustomTkinter を使用して構築された、理系学生・エンジニア向けのマルチタブ型テキストエディタです。
通常のテキスト編集に加え、LaTeX 数式、化学構造式（mhchem）のリアルタイムプレビューに対応しています。

---

## 🌟 主な特徴

- **理系特化 Markdown 支援**:
  - **LaTeX 数式**: 高度な数学記号・積分のレンダリングに対応。
  - **化学式 (mhchem)**: 分子式 $\ce{H2O}$ や反応式　$\ce{2H2 + O2 -> 2H2O}$　を美しく表示。
  - **ブラウザプレビュー**: ワンクリック（または `Ctrl+Shift+P`）でスタイリッシュな HTML プレビューを表示。
- **ライブ・プレビュー**:
  - **自動更新**: 10秒ごとに編集内容がブラウザに自動反映。設定から更新間隔を **1秒〜60秒** の間で変更可能。
  - **再読み込み不要**: 一度ブラウザを開けば、保存操作なしで最新の LaTeX や Markdown を確認可能。
- **モダンな UI/UX**:
  - **ショートカット・ツールチップ**: ツールバーのボタンにホバーすると、対応するショートカットキーを表示。
  - ダークモード/ライトモードの完全切り替え。
- **コーディング支援**:
  - **シンタックスハイライト**: Python, HTML, CSS, JS, Markdown に対応。
  - **視覚ガイド**: 行番号表示、グリッド線表示、現在行ハイライト機能。
- **検索機能**: リアルタイムハイライトと前後へのナビゲーション。
- **多言語対応 (i18n)**: 日本語と英語の UI 切り替えに対応。
- **自動ディレクトリ作成**: ユーザーのホームディレクトリに専用の保存フォルダを自動作成。
- **自動アップデート確認**: GitHub API を利用し、最新版がある場合に通知を表示。

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

## ⌨️ ショートカットキー

| キー組合せ | 機能 |
| :---: | :---: |
| Ctrl + N | 新規タブの作成 |
| Ctrl + O | ファイルを開く |
| Ctrl + S | ファイルを保存 |
| Ctrl + Shift + P | Markdown プレビュー表示 |
| Ctrl + F | 検索パネルの表示/非表示 |
| Ctrl + , | 設定画面の表示/非表示 |
| Ctrl + L | 行番号の表示/非表示 |
| Ctrl + G | 罫線（グリッド）の表示/非表示 |
| Ctrl + H | 現在行ハイライトの有効/無効 |

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

## 🛠 技術スタック
- GUI: CustomTkinter

- Markdown: markdown2 (with extras)

- Math/Chemistry: MathJax 3.0 (mhchem extension)

- Automation: GitHub Actions (PyInstaller build)

### バージョン番号
バージョン番号は X.Y.Z （例：1.1.2）の形式で表し、それぞれの数字に明確な意味を持たせます。

|項目|呼び方|更新するタイミング|例|
|:---:|:---:|:---:|:---:|
|X|メジャー (Major)|互換性のない 大幅な変更。使い方がガラッと変わる時。|1.1.2 → 2.0.0
|Y|マイナー (Minor)|互換性を保ちつつ、新機能を追加した時。|1.1.2 → 1.2.0
|Z|パッチ (Patch)|互換性を保ちつつ、バグ修正や細かな調整をした時。|1.1.2 → 1.1.3

## 📄 ライセンス
このプロジェクトは MIT License のもとで公開されています。

Produced with passion for clean coding.