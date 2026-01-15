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
            "preview_interval": "自動更新の間隔 (秒)","import_file": "ファイルをインポート (docx/html)",
            "conversion_error": "変換エラーが発生しました: {error}",
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
