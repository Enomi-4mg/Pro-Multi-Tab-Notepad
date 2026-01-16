import customtkinter as ctk
import os

# ==========================================
# 1. 多言語管理 (I18n)
# ==========================================
class I18n:
    translations = {
        "ja": {
            "new_file": "新規作成",
            "open_file": "開く",
            "save_file": "保存",
            "find": "検索",
            "settings": "設定",
            "untitled": "無題",
            "welcome_title": "Pro Multi-Tab Notepad",
            "welcome_subtitle": "こんにちは！\nファイルを作成するか、既存のファイルを開いて開始してください！",
            "ready": "準備完了",
            "no_file": "ファイルなし",
            "modified": " (変更あり)",
            "line_col": "行 {line}, 列 {col} | 文字数: {chars} | モード: {mode}",
            "settings_title": "設定",
            "appearance": "外観",
            "theme_mode": "テーマモード (Light/Dark)",
            "editor_settings": "エディタ設定",
            "font_size": "フォントサイズ",
            "show_line_num": "行番号を表示",
            "show_grid": "罫線を表示",
            "show_current_line": "カレント行を強調",
            "file_settings": "ファイル設定",
            "default_dir": "デフォルトの保存先",
            "language_settings": "言語設定",
            "lang_label": "表示言語",
            "apply_btn": "設定を適用",
            "back_btn": "エディタに戻る",
            "confirm_close": " は変更されています。保存せずに閉じますか？",
            "settings_applied": "設定を適用しました。",
            "update_available": "新バージョン ({version}) が利用可能です！\nGitHubからダウンロードしますか？",
            "update_title": "アップデート通知",
            "version_label": "バージョン: {version}",
            "preview": "プレビュー",
            "markdown_preview": "Markdownプレビュー (ブラウザ)",
            "preview_settings": "プレビュー設定",
            "preview_interval": "自動更新の間隔 (秒)",
            "import_file": "ファイルをインポート (docx/html)",
            "conversion_error": "変換エラーが発生しました: {error}",
            "export_settings": "設定をエクスポート",
            "import_settings": "設定をインポート",
            "export_success": "設定をエクスポートしました",
            "import_success": "設定をインポートしました",
            "import_error": "インポートエラー",
            "save_as": "名前を付けて保存",
            "recent_files": "最近のファイル",
            "no_recent_files": "履歴なし",
            "file_not_found": "ファイル '{path}' が見つかりません",
        },
        "en": {
            "new_file": "New",
            "open_file": "Open",
            "save_file": "Save",
            "find": "Find",
            "settings": "Settings",
            "untitled": "Untitled",
            "welcome_title": "Pro Multi-Tab Notepad",
            "welcome_subtitle": "Start by creating a new file or opening an existing one.",
            "ready": "Ready",
            "no_file": "No file open",
            "modified": " (Modified)",
            "line_col": "Line {line}, Col {col} | Chars: {chars} | Mode: {mode}",
            "settings_title": "Settings",
            "appearance": "Appearance",
            "theme_mode": "Theme Mode (Light/Dark)",
            "editor_settings": "Editor",
            "font_size": "Font Size",
            "show_line_num": "Show Line Numbers",
            "show_grid": "Show Grid Lines",
            "show_current_line": "Highlight Current Line",
            "file_settings": "Files",
            "default_dir": "Default Save Directory",
            "language_settings": "Language",
            "lang_label": "Language",
            "apply_btn": "Apply Changes",
            "back_btn": "Back to Editor",
            "confirm_close": " has unsaved changes. Close anyway?",
            "settings_applied": "Settings applied successfully!",
            "update_available": "New version ({version}) is available!\nDo you want to download it from GitHub?",
            "update_title": "Update Available",
            "version_label": "Version: {version}",
            "preview": "Preview",
            "markdown_preview": "Markdown Preview (Browser)",
            "preview_settings": "Preview Settings",
            "preview_interval": "Update Interval (sec)",
            "import_file": "Import File (docx/html)",
            "conversion_error": "Conversion error: {error}",
            "export_settings": "Export Settings",
            "import_settings": "Import Settings",
            "export_success": "Settings exported",
            "import_success": "Settings imported",
            "import_error": "Import error",
            "save_as": "Save As",
            "recent_files": "Recent Files",
            "no_recent_files": "No recent files",
            "file_not_found": "File '{path}' not found",
        }
    }

    @classmethod
    def get(cls, key, lang="ja", **kwargs):
        text = cls.translations.get(lang, cls.translations["en"]).get(key, key)
        return text.format(**kwargs)

# ==========================================
# 2. 定数・スタイルの管理 (AppConfig)
# ==========================================
class AppConfig:
    APP_TITLE = "Pro Multi-Tab Notepad"
    APP_VERSION = "1.6.1"  # バージョン情報
    GEOMETRY = "1200x800"
    
    # 専用ディレクトリの定義
    APP_DIR_NAME = "ProMultiTabNotepad"
    APP_DIR_PATH = os.path.join(os.path.expanduser("~"), APP_DIR_NAME)
    
    settings = {
        "appearance": "dark",
        "font_size": 14,
        "font_family": "Consolas",
        "show_line_numbers": True,
        "show_grid": False,
        "show_current_line": True,
        "default_dir": APP_DIR_PATH, # 専用ディレクトリを初期値に設定
        "preview_interval": 5,
        "lang": "ja",
        "last_save_dir": None,  # 最後に保存したディレクトリ
        "recent_files": [],  # 最近開いたファイルのリスト（最大10件）
    }
    
    COLORS = {
        "toolbar_bg": ("gray90", "#2b2b2b"),
        "tabbar_bg": ("gray85", "#242424"),
        "editor_bg": ("white", "#1a1a1a"),
        "text_active": ("black", "white"),
        "text_inactive": "gray50",
        "status_bg": ("gray80", "#1e1e1e"),
        "text_secondary": ("gray40", "gray60"),
        "search_highlight": ("#FFFF00", "#D4A017"),
        "line_num_fg": "gray50",
        "grid_line": ("gray85", "#333333"),
        "current_line": ("#F5F5F5", "#282828"),
    }

    SYNTAX = {
        "keyword": "#569CD6",
        "string": "#CE9178",
        "comment": "#6A9955",
        "number": "#B5CEA8",
        "tag": "#569CD6",
        "attr": "#9CDCFE",
    }
    
    @classmethod
    def get_editor_font(cls):
        return (cls.settings["font_family"], cls.settings["font_size"])

    @classmethod
    def get_ui_font(cls, bold=False):
        return ("Segoe UI", 12, "bold" if bold else "normal")

    @classmethod
    def t(cls, key, **kwargs):
        return I18n.get(key, cls.settings["lang"], **kwargs)
    
    @classmethod
    def save_settings(cls):
        """設定をJSONファイルに保存する（既存ファイルは.bakにバックアップ）"""
        import json
        settings_path = os.path.join(cls.APP_DIR_PATH, "settings.json")
        backup_path = os.path.join(cls.APP_DIR_PATH, "settings.json.bak")
        
        try:
            # 既存のsettings.jsonがあればバックアップ
            if os.path.exists(settings_path):
                if os.path.exists(backup_path):
                    os.remove(backup_path)
                os.rename(settings_path, backup_path)
            
            # 新しい設定を保存
            with open(settings_path, "w", encoding="utf-8") as f:
                json.dump(cls.settings, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"設定保存エラー: {e}")
            return False
    
    @classmethod
    def load_settings(cls):
        """設定をJSONファイルから読み込む（失敗時は.bakから復元を試行）"""
        import json
        settings_path = os.path.join(cls.APP_DIR_PATH, "settings.json")
        backup_path = os.path.join(cls.APP_DIR_PATH, "settings.json.bak")
        
        # デフォルト設定のコピーを保持
        default_settings = cls.settings.copy()
        
        # まず通常のsettings.jsonを試行
        if os.path.exists(settings_path):
            try:
                with open(settings_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    # デフォルト値とマージ（新しい設定項目との互換性確保）
                    cls.settings.update(loaded)
                print("設定を読み込みました")
                return True
            except Exception as e:
                print(f"設定読み込みエラー: {e}。バックアップから復元を試みます...")
        
        # settings.jsonが失敗した場合、バックアップから復元
        if os.path.exists(backup_path):
            try:
                with open(backup_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    cls.settings = default_settings
                    cls.settings.update(loaded)
                print("バックアップから設定を復元しました")
                return True
            except Exception as e:
                print(f"バックアップ復元エラー: {e}。デフォルト設定を使用します")
        
        # 両方失敗した場合はデフォルト設定を使用
        cls.settings = default_settings
        print("デフォルト設定を使用します")
        return False
    
    @classmethod
    def export_settings(cls, path):
        """設定を指定したパスにエクスポートする"""
        import json
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(cls.settings, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"設定エクスポートエラー: {e}")
            return False
    
    @classmethod
    def import_settings(cls, path):
        """設定を指定したパスからインポートする"""
        import json
        try:
            with open(path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                # デフォルト値を保持しつつ更新
                default_settings = {
                    "appearance": "dark",
                    "font_size": 14,
                    "font_family": "Consolas",
                    "show_line_numbers": True,
                    "show_grid": False,
                    "show_current_line": True,
                    "default_dir": cls.APP_DIR_PATH,
                    "preview_interval": 5,
                    "lang": "ja",
                    "last_save_dir": None,
                    "recent_files": [],
                }
                default_settings.update(loaded)
                cls.settings = default_settings
            return True
        except Exception as e:
            print(f"設定インポートエラー: {e}")
            return False
    
    GITHUB_USER = "EnoMi-4mg" # 書き換えてください
    REPO_NAME = "Pro-Multi-Tab-Notepad"
    GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/releases/latest"

class CTkToolTip:
    """ボタンホバー時にショートカットキーを表示する簡易ツールチップ"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self._after_id = None
        self.widget.bind("<Enter>", self.show_delayed)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_delayed(self, event=None):
        if self._after_id: self.widget.after_cancel(self._after_id)
        self._after_id = self.widget.after(300, self.show_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip_window or not self.text: return
        try:
            x = self.widget.winfo_rootx() + (self.widget.winfo_width() // 2)
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
            
            self.tooltip_window = tw = ctk.CTkToplevel(self.widget)
            tw.wm_overrideredirect(True)
            tw.wm_geometry(f"+{x}+{y}")
            tw.attributes("-topmost", True)
            tw.attributes("-alpha", 0.9)
            
            label = ctk.CTkLabel(tw, text=self.text, fg_color=("#333333", "#444444"), 
                                 text_color="white", corner_radius=4, padx=8, pady=4, 
                                 font=("Segoe UI", 10, "bold"))
            label.pack()
        except:
            self.hide_tooltip()

    def hide_tooltip(self, event=None):
        if self._after_id:
            self.widget.after_cancel(self._after_id)
            self._after_id = None
        if self.tooltip_window:
            try:
                self.tooltip_window.destroy()
            except:
                pass
            self.tooltip_window = None
