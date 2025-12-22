VERSION = "1.3.1"

import customtkinter as ctk
from tkinter import filedialog, messagebox, Canvas
import os
import re

import markdown2
import tempfile

import threading
import requests
import webbrowser
from packaging import version

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

# ==========================================
# 3. シンタックスハイライター
# ==========================================
class SyntaxHighlighter:
    def __init__(self, textbox):
        self.textbox = textbox
        self._setup_tags()

    def _setup_tags(self):
        for name, color in AppConfig.SYNTAX.items():
            self.textbox.tag_config(name, foreground=color)
        self.textbox.tag_config("search_match", background=AppConfig.COLORS["search_highlight"][1], foreground="black")
        self.textbox.tag_config("current_line", background=AppConfig.COLORS["current_line"][1])
        self.textbox.tag_lower("current_line")

    def apply(self, mode):
        self.clear_syntax()
        if mode == "Plain Text": return
        
        content = self.textbox.get("1.0", "end-1c")
        
        rules = []
        if mode == "Python":
            rules = [
                ("keyword", r"\b(def|class|if|else|elif|for|while|return|import|from|as|try|except|with|None|True|False|self|in|is|not|pass|lambda)\b"),
                ("string", r"(\".*?\"|'.*?')"),
                ("comment", r"#.*"),
                ("number", r"\b\d+\b")
            ]
        elif mode == "JavaScript":
            rules = [
                ("keyword", r"\b(function|var|let|const|if|else|for|while|return|import|export|class|async|await|new|this|true|false|null)\b"),
                ("string", r"(\".*?\"|'.*?`|`.*?`)"),
                ("comment", r"//.*|/\*[\s\S]*?\*/"),
                ("number", r"\b\d+\b")
            ]
        elif mode == "HTML":
            rules = [
                ("tag", r"<[^>]+>"),
                ("attr", r"\b[a-zA-Z0-9-]+(?==)"),
                ("string", r"\".*?\"|'.*?'"),
                ("comment", r"<!--[\s\S]*?-->")
            ]
        elif mode == "CSS":
            rules = [
                ("keyword", r"\b(active|hover|focus|visited|link|root|media|import|font-face)\b"),
                ("attr", r"\b[a-zA-Z-]+(?=:)"),
                ("string", r"\".*?\"|'.*?'"),
                ("comment", r"/\*[\s\S]*?\*/")
            ]
        elif mode == "Markdown":
            rules = [
                ("keyword", r"^(#+.*)$"), # 見出し
                ("string", r"(\*\*.*?\*\*|__.*?__)"), # 太字
                ("comment", r"(\[.*?\]\(.*?\))"), # リンク
                ("tag", r"(`.*?`)"), # インラインコード
    ]
            

        for tag, pattern in rules:
            for match in re.finditer(pattern, content):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.textbox.tag_add(tag, start, end)

    def clear_syntax(self):
        for tag in AppConfig.SYNTAX.keys():
            self.textbox.tag_remove(tag, "1.0", "end")

# ==========================================
# 4. エディタコンポーネント (EditorView)
# ==========================================
class EditorView(ctk.CTkFrame):
    def __init__(self, master, content="", file_path=None, on_change_callback=None, on_cursor_callback=None, **kwargs):
        super().__init__(master, fg_color=AppConfig.COLORS["editor_bg"], corner_radius=0)
        
        self.file_path = file_path
        self.is_modified = False
        self.on_change_callback = on_change_callback
        self.on_cursor_callback = on_cursor_callback
        self.mode = self._detect_mode(file_path)

        # 行番号キャンバス
        self.line_num_canvas = Canvas(self, width=55, 
                                           bg=AppConfig.COLORS["editor_bg"][1] if ctk.get_appearance_mode()=="Dark" else AppConfig.COLORS["editor_bg"][0], 
                                           highlightthickness=0, bd=0)
        
        # テキストエリア
        self.textbox = ctk.CTkTextbox(self, font=AppConfig.get_editor_font(), undo=True, corner_radius=0, border_width=0, **kwargs)
        self.textbox.pack(side="right", fill="both", expand=True)
        
        # パディング設定
        self.textbox._textbox.configure(padx=5, pady=5)

        # スクロール同期の安全な処理
        self.original_yscroll = self.textbox._textbox.cget("yscrollcommand")
        self.textbox._textbox.configure(yscrollcommand=self._on_scroll_sync)

        if AppConfig.settings["show_line_numbers"] or AppConfig.settings["show_grid"]:
            self.line_num_canvas.pack(side="left", fill="y", padx=(0, 0), before=self.textbox)

        self.highlighter = SyntaxHighlighter(self.textbox)
        self.textbox.insert("0.0", content)

        # イベント
        self.textbox.bind("<KeyRelease>", self._handle_event)
        self.textbox.bind("<ButtonRelease-1>", self._handle_event)
        # 画面リサイズ等のタイミングでも行番号を更新
        self.textbox._textbox.bind("<Configure>", lambda e: self.after(10, self.update_line_numbers))
        
        self.line_num_canvas.bind("<MouseWheel>", self._on_canvas_wheel)

        self.update_line_numbers()
        self.apply_highlight()
        self.highlight_current_line()

    def _on_scroll_sync(self, *args):
        if self.original_yscroll:
            if callable(self.original_yscroll):
                self.original_yscroll(*args)
            else:
                try:
                    self.textbox._textbox.tk.call(self.original_yscroll, *args)
                except:
                    pass
        self.update_line_numbers()

    def _on_canvas_wheel(self, event):
        self.textbox._textbox.yview_scroll(int(-1*(event.delta/120)), "units")
        self.update_line_numbers()

    def _detect_mode(self, path):
        if not path: return "Plain Text"
        ext = os.path.splitext(path)[1].lower()
        mapping = {".py": "Python", ".html": "HTML", ".css": "CSS", ".js": "JavaScript", ".md": "Markdown"}
        return mapping.get(ext, "Plain Text")

    def toggle_line_numbers(self, show):
        if show or AppConfig.settings["show_grid"]:
            self.line_num_canvas.pack(side="left", fill="y", before=self.textbox)
            self.update_line_numbers()
        else:
            self.line_num_canvas.pack_forget()

    def update_appearance(self):
        self.textbox.configure(font=AppConfig.get_editor_font())
        mode = ctk.get_appearance_mode()
        self.highlighter.textbox.tag_config("current_line", background=AppConfig.COLORS["current_line"][1] if mode=="Dark" else AppConfig.COLORS["current_line"][0])
        bg_color = AppConfig.COLORS["editor_bg"][1] if mode=="Dark" else AppConfig.COLORS["editor_bg"][0]
        self.line_num_canvas.configure(bg=bg_color)
        self.update_line_numbers()
        self.highlight_current_line()

    def apply_highlight(self):
        self.highlighter.apply(self.mode)

    def highlight_current_line(self):
        """現在行のハイライト"""
        self.textbox.tag_remove("current_line", "1.0", "end")
        if AppConfig.settings["show_current_line"]:
            line_start = self.textbox.index("insert linestart")
            line_end = self.textbox.index("insert lineend + 1c")
            self.textbox.tag_add("current_line", line_start, line_end)

    def update_line_numbers(self):
        self.line_num_canvas.delete("all")
        if not AppConfig.settings["show_line_numbers"] and not AppConfig.settings["show_grid"]:
            return

        i = self.textbox.index("@0,0")
        mode = ctk.get_appearance_mode()
        grid_color = AppConfig.COLORS["grid_line"][1] if mode=="Dark" else AppConfig.COLORS["grid_line"][0]
        
        # 垂直境界線
        if AppConfig.settings["show_grid"]:
            self.line_num_canvas.create_line(54, 0, 54, self.winfo_height(), fill=grid_color)

        while True:
            dline = self.textbox._textbox.dlineinfo(i)
            if dline is None: break
            
            # y=座標, h=行の高さ
            y = dline[1]
            h = dline[3]
            
            # 行番号の描画
            if AppConfig.settings["show_line_numbers"]:
                line_num = str(i).split(".")[0]
                # x=27.5 (幅55の中央), anchor="center" で中央寄せ
                self.line_num_canvas.create_text(27, y + (h/2) + 5, anchor="center", text=line_num, 
                                                 fill=AppConfig.COLORS["line_num_fg"], font=AppConfig.get_editor_font())
            
            # 水平罫線の描画
            if AppConfig.settings["show_grid"]:
                self.line_num_canvas.create_line(0, y + h + 5, 55, y + h + 5, fill=grid_color)

            i = self.textbox.index(f"{i}+1line")

    def _handle_event(self, event=None):
        if event and event.keysym in ("Up", "Down", "Left", "Right", "Page_Up", "Page_Down", "Return", "BackSpace"):
            self.update_line_numbers()
            self.highlight_current_line()
            if self.on_cursor_callback: self.on_cursor_callback()
            return

        if not self.is_modified and event and event.char:
            self.is_modified = True
            if self.on_change_callback: self.on_change_callback()
        
        self.update_line_numbers()
        self.apply_highlight()
        self.highlight_current_line()
        if self.on_cursor_callback: self.on_cursor_callback()

    def get(self, *args, **kwargs): return self.textbox.get(*args, **kwargs)
    def insert(self, *args, **kwargs): return self.textbox.insert(*args, **kwargs)
    def index(self, *args, **kwargs): return self.textbox.index(*args, **kwargs)
    def see(self, *args, **kwargs): return self.textbox.see(*args, **kwargs)
    def focus_set(self): self.textbox.focus_set()
    def reset_modified(self): self.is_modified = False

# ==========================================
# 5. Mixins
# ==========================================

class TabOperationsMixin:
    def init_tab_system(self):
        self.tabs = {}
        self.tab_order = []
        self.current_tab_id = None
        self.tab_count = 0

    def add_new_tab(self, file_path=None, content=""):
        self.tab_count += 1
        tab_id = f"tab_{self.tab_count}"
        name = os.path.basename(file_path) if file_path else f"{AppConfig.t('untitled')} {self.tab_count}"

        editor = EditorView(
            self.editor_container, content, file_path, 
            on_change_callback=lambda: self._mark_as_modified(tab_id),
            on_cursor_callback=self.update_status_bar
        )
        
        tab_unit = ctk.CTkFrame(self.tab_bar, fg_color="transparent")
        tab_unit.pack(side="left", padx=(0, 1))
        
        btn = ctk.CTkButton(tab_unit, text=name, width=140, height=30, corner_radius=0, anchor="w",
                            fg_color="transparent", text_color=AppConfig.COLORS["text_inactive"],
                            command=lambda: self.switch_tab(tab_id))
        btn.pack(side="left")

        close_btn = ctk.CTkButton(tab_unit, text="×", width=25, height=30, corner_radius=0,
                                  fg_color="transparent", hover_color="#AA3333",
                                  command=lambda: self.close_tab(tab_id))
        close_btn.pack(side="left")

        self.tabs[tab_id] = {"editor": editor, "tab_unit": tab_unit, "btn": btn, "name": name}
        self.tab_order.append(tab_id)
        
        self.show_editor_view()
        self.switch_tab(tab_id)

    def switch_tab(self, tab_id):
        if self.current_tab_id and self.current_tab_id in self.tabs:
            old = self.tabs[self.current_tab_id]
            old["editor"].pack_forget()
            old["btn"].configure(text_color=AppConfig.COLORS["text_inactive"], font=AppConfig.get_ui_font(False))
            old["tab_unit"].configure(fg_color="transparent")

        new = self.tabs[tab_id]
        new["editor"].pack(fill="both", expand=True)
        new["btn"].configure(text_color=AppConfig.COLORS["text_active"], font=AppConfig.get_ui_font(True))
        new["tab_unit"].configure(fg_color=AppConfig.COLORS["editor_bg"])
        
        self.current_tab_id = tab_id
        new["editor"].focus_set()
        new["editor"].update_line_numbers()
        new["editor"].highlight_current_line()
        self.update_status_bar()

    def close_tab(self, tab_id):
        tab = self.tabs[tab_id]
        if tab["editor"].is_modified:
            if not messagebox.askyesno("Confirm", f"{tab['name']}{AppConfig.t('confirm_close')}"):
                return
        
        if tab_id == self.current_tab_id: self.current_tab_id = None
        tab["tab_unit"].destroy()
        tab["editor"].destroy()
        del self.tabs[tab_id]
        self.tab_order.remove(tab_id)

        if self.tab_order: self.switch_tab(self.tab_order[-1])
        self._check_empty_state()
        self.update_status_bar()

    def _mark_as_modified(self, tab_id):
        info = self.tabs[tab_id]
        if not info["btn"].cget("text").endswith("*"):
            info["btn"].configure(text=f"{info['name']} *")

class FileOperationsMixin:
    def open_file(self):
        path = filedialog.askopenfilename(initialdir=AppConfig.settings["default_dir"])
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.add_new_tab(file_path=path, content=content)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def save_file(self):
        if not self.current_tab_id: return
        tab = self.tabs[self.current_tab_id]
        editor = tab["editor"]
        path = editor.file_path or filedialog.asksaveasfilename(
            defaultextension=".txt", 
            initialdir=AppConfig.settings["default_dir"]
        )
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(editor.get("1.0", "end-1c"))
                editor.file_path = path
                editor.mode = editor._detect_mode(path)
                editor.apply_highlight()
                tab["name"] = os.path.basename(path)
                tab["btn"].configure(text=tab["name"])
                editor.reset_modified()
                self.update_status_bar()
            except Exception as e:
                messagebox.showerror("Error", str(e))

class SearchOperationsMixin:
    def init_search_ui(self):
        self.search_active = False
        self.search_frame = ctk.CTkFrame(self.editor_container, height=45, fg_color=AppConfig.COLORS["toolbar_bg"], border_width=1, border_color="gray50")
        
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Find...", width=200)
        self.search_entry.pack(side="left", padx=10, pady=5)
        self.search_entry.bind("<KeyRelease>", self._on_search_change)
        self.search_entry.bind("<Return>", lambda e: self._on_search_next())

        ctk.CTkButton(self.search_frame, text="<", width=30, command=self._on_search_prev).pack(side="left", padx=2)
        ctk.CTkButton(self.search_frame, text=">", width=30, command=self._on_search_next).pack(side="left", padx=2)

        ctk.CTkButton(self.search_frame, text="×", width=30, fg_color="transparent", hover_color="#AA3333", command=self.toggle_search).pack(side="left", padx=10)

    def toggle_search(self, event=None):
        if not self.current_tab_id: return
        if not self.search_active:
            self.search_frame.place(relx=1.0, x=-20, y=20, anchor="ne")
            self.search_frame.lift()
            self.search_entry.focus_set()
            self.search_active = True
            self._on_search_change()
        else:
            self.search_frame.place_forget()
            self.search_active = False
            if self.current_tab_id in self.tabs:
                self.tabs[self.current_tab_id]["editor"].textbox.tag_remove("search_match", "1.0", "end")

    def _on_search_change(self, event=None):
        if not self.current_tab_id: return
        query = self.search_entry.get()
        editor = self.tabs[self.current_tab_id]["editor"]
        editor.textbox.tag_remove("search_match", "1.0", "end")
        if not query: return

        start_pos = "1.0"
        while True:
            start_pos = editor.textbox.search(query, start_pos, stopindex="end", nocase=True)
            if not start_pos: break
            end_pos = f"{start_pos}+{len(query)}c"
            editor.textbox.tag_add("search_match", start_pos, end_pos)
            start_pos = end_pos

    def _on_search_next(self):
        if not self.current_tab_id: return
        query = self.search_entry.get()
        if not query: return
        editor = self.tabs[self.current_tab_id]["editor"]
        current_pos = editor.textbox.index("insert+1c")
        idx = editor.textbox.search(query, current_pos, stopindex="end", nocase=True)
        if not idx: idx = editor.textbox.search(query, "1.0", stopindex="end", nocase=True)
        if idx:
            editor.textbox.mark_set("insert", idx)
            editor.textbox.see(idx)

    def _on_search_prev(self):
        if not self.current_tab_id: return
        query = self.search_entry.get()
        if not query: return
        editor = self.tabs[self.current_tab_id]["editor"]
        current_pos = editor.textbox.index("insert")
        idx = editor.textbox.search(query, current_pos, stopindex="1.0", backwards=True, nocase=True)
        if not idx: idx = editor.textbox.search(query, "end", stopindex="1.0", backwards=True, nocase=True)
        if idx:
            editor.textbox.mark_set("insert", idx)
            editor.textbox.see(idx)

# ==========================================
# 6. 設定管理
# ==========================================
class SettingsOperationsMixin:
    def init_settings_ui(self):
        self.settings_visible = False
        self.settings_view = ctk.CTkScrollableFrame(self.editor_container, fg_color=AppConfig.COLORS["editor_bg"])
        
        self.settings_title_label = ctk.CTkLabel(self.settings_view, text="", font=(None, 24, "bold"))
        self.settings_title_label.pack(pady=20, padx=40, anchor="w")

        # 外観
        self.app_section = self._create_section_label("appearance")
        self.mode_var = ctk.StringVar(value=AppConfig.settings["appearance"])
        self.mode_row = self._create_setting_row("theme_mode")
        self.mode_btn = ctk.CTkSegmentedButton(self.mode_row, values=["light", "dark"], variable=self.mode_var)
        self.mode_btn.pack(side="right")

        # エディタ設定
        self.edit_section = self._create_section_label("editor_settings")
        self.size_row = self._create_setting_row("font_size")
        self.size_slider = ctk.CTkSlider(self.size_row, from_=8, to=40, number_of_steps=32)
        self.size_slider.set(AppConfig.settings["font_size"])
        self.size_slider.pack(side="right", padx=10)
        self.size_label = ctk.CTkLabel(self.size_row, text=str(AppConfig.settings["font_size"]))
        self.size_label.pack(side="right")
        self.size_slider.configure(command=lambda v: self.size_label.configure(text=str(int(v))))

        self.line_num_var = ctk.BooleanVar(value=AppConfig.settings["show_line_numbers"])
        self.line_num_row = self._create_setting_row("show_line_num")
        self.line_num_switch = ctk.CTkSwitch(self.line_num_row, text="", variable=self.line_num_var)
        self.line_num_switch.pack(side="right")

        self.grid_var = ctk.BooleanVar(value=AppConfig.settings["show_grid"])
        self.grid_row = self._create_setting_row("show_grid")
        self.grid_switch = ctk.CTkSwitch(self.grid_row, text="", variable=self.grid_var)
        self.grid_switch.pack(side="right")

        self.cur_line_var = ctk.BooleanVar(value=AppConfig.settings["show_current_line"])
        self.cur_line_row = self._create_setting_row("show_current_line")
        self.cur_line_switch = ctk.CTkSwitch(self.cur_line_row, text="", variable=self.cur_line_var)
        self.cur_line_switch.pack(side="right")
        
        # プレビュー設定セクション
        self.preview_section = self._create_section_label("preview_settings")
        self.interval_row = self._create_setting_row("preview_interval")
        
        # スライダー (1秒〜60秒)
        self.interval_slider = ctk.CTkSlider(self.interval_row, from_=1, to=60, number_of_steps=59)
        self.interval_slider.set(AppConfig.settings["preview_interval"])
        self.interval_slider.pack(side="right", padx=10)
        
        self.interval_label = ctk.CTkLabel(self.interval_row, text=f"{AppConfig.settings['preview_interval']}s")
        self.interval_label.pack(side="right")
        self.interval_slider.configure(command=lambda v: self.interval_label.configure(text=f"{int(v)}s"))

        # ファイル設定
        self.file_section = self._create_section_label("file_settings")
        self.dir_row = self._create_setting_row("default_dir")
        self.dir_path_var = ctk.StringVar(value=AppConfig.settings["default_dir"])
        ctk.CTkEntry(self.dir_row, textvariable=self.dir_path_var, width=300).pack(side="left", padx=(0, 10))
        ctk.CTkButton(self.dir_row, text="...", width=40, command=self._browse_default_dir).pack(side="left")

        # 言語設定
        self.lang_section = self._create_section_label("language_settings")
        self.lang_var = ctk.StringVar(value=AppConfig.settings["lang"])
        self.lang_row = self._create_setting_row("lang_label")
        self.lang_menu = ctk.CTkOptionMenu(self.lang_row, values=["ja", "en"], variable=self.lang_var)
        self.lang_menu.pack(side="right")

        # 下部ボタン
        self.btn_frame = ctk.CTkFrame(self.settings_view, fg_color="transparent")
        self.btn_frame.pack(pady=40, padx=40, fill="x")
        self.apply_btn = ctk.CTkButton(self.btn_frame, text="", command=self.apply_settings, fg_color="#28a745", hover_color="#218838")
        self.apply_btn.pack(side="right", padx=10)
        self.back_btn = ctk.CTkButton(self.btn_frame, text="", command=self.show_editor_view, fg_color="transparent", border_width=1)
        self.back_btn.pack(side="right")
        
        self.ver_label = ctk.CTkLabel(self.settings_view, 
                                     text=AppConfig.t("version_label", version=VERSION),
                                     text_color=AppConfig.COLORS["text_secondary"])
        self.ver_label.pack(pady=10)

    def _create_section_label(self, key):
        lbl = ctk.CTkLabel(self.settings_view, text=AppConfig.t(key), font=(None, 16, "bold"), text_color=AppConfig.COLORS["text_secondary"])
        lbl.pack(pady=(20, 10), padx=40, anchor="w")
        lbl.key = key
        return lbl

    def _create_setting_row(self, key):
        row = ctk.CTkFrame(self.settings_view, fg_color="transparent")
        row.pack(fill="x", padx=60, pady=5)
        lbl = ctk.CTkLabel(row, text=AppConfig.t(key))
        lbl.pack(side="left")
        row.label = lbl
        row.key = key
        return row

    def _browse_default_dir(self):
        path = filedialog.askdirectory()
        if path: self.dir_path_var.set(path)

    def toggle_settings(self):
        if self.settings_visible: self.show_editor_view()
        else: self.show_settings_view()

    def show_settings_view(self):
        self._hide_all_views()
        self.update_settings_ui_texts()
        self.settings_view.pack(fill="both", expand=True)
        self.settings_visible = True
        self.tab_bar.grid_remove()

    def show_editor_view(self):
        self._hide_all_views()
        self.settings_visible = False
        self._check_empty_state()
        if self.tabs:
            self.tab_bar.grid()
            if self.current_tab_id:
                self.tabs[self.current_tab_id]["editor"].pack(fill="both", expand=True)

    def _hide_all_views(self):
        self.settings_view.pack_forget()
        self.welcome_frame.place_forget()
        if self.current_tab_id and self.current_tab_id in self.tabs:
            self.tabs[self.current_tab_id]["editor"].pack_forget()

    def update_settings_ui_texts(self):
        self.settings_title_label.configure(text=AppConfig.t("settings_title"))
        self.app_section.configure(text=AppConfig.t(self.app_section.key))
        self.edit_section.configure(text=AppConfig.t(self.edit_section.key))
        self.line_num_row.label.configure(text=AppConfig.t(self.line_num_row.key))
        self.grid_row.label.configure(text=AppConfig.t(self.grid_row.key))
        self.cur_line_row.label.configure(text=AppConfig.t(self.cur_line_row.key))
        self.file_section.configure(text=AppConfig.t(self.file_section.key))
        self.lang_section.configure(text=AppConfig.t(self.lang_section.key))
        self.mode_row.label.configure(text=AppConfig.t(self.mode_row.key))
        self.size_row.label.configure(text=AppConfig.t(self.size_row.key))
        self.dir_row.label.configure(text=AppConfig.t(self.dir_row.key))
        self.lang_row.label.configure(text=AppConfig.t(self.lang_row.key))
        self.apply_btn.configure(text=AppConfig.t("apply_btn"))
        self.back_btn.configure(text=AppConfig.t("back_btn"))
        if hasattr(self, "ver_label"):
            self.ver_label.configure(text=AppConfig.t("version_label", version=VERSION))

    def apply_settings(self):
        AppConfig.settings["appearance"] = self.mode_var.get()
        AppConfig.settings["font_size"] = int(self.size_slider.get())
        AppConfig.settings["show_line_numbers"] = self.line_num_var.get()
        AppConfig.settings["show_grid"] = self.grid_var.get()
        AppConfig.settings["show_current_line"] = self.cur_line_var.get()
        AppConfig.settings["default_dir"] = self.dir_path_var.get()
        AppConfig.settings["lang"] = self.lang_var.get()
        AppConfig.settings["preview_interval"] = int(self.interval_slider.get())

        ctk.set_appearance_mode(AppConfig.settings["appearance"])
        for tab in self.tabs.values():
            tab["editor"].toggle_line_numbers(AppConfig.settings["show_line_numbers"])
            tab["editor"].update_appearance()
            tab["editor"].highlight_current_line()
        
        self.update_ui_texts()
        self.update_settings_ui_texts()
        messagebox.showinfo(AppConfig.t("settings_title"), AppConfig.t("settings_applied"))

# ==========================================
# 7. メインアプリケーション (MultiTabApp)
# ==========================================
class MultiTabApp(ctk.CTk, TabOperationsMixin, FileOperationsMixin, SearchOperationsMixin, SettingsOperationsMixin):
    def __init__(self):
        super().__init__()
        # --- 変数の初期化 ---
        self.preview_file = None 
        
        self._ensure_app_directory()
        self.init_tab_system()
        self._setup_window()
        self._create_widgets()
        self.init_search_ui()
        self.init_settings_ui()
        self._setup_bindings()
        self._check_empty_state()
        self.update_ui_texts()
        
        # 10秒ごとの自動プレビュー更新ループ開始
        self._setup_auto_preview()
        
        self.after(2000, self.check_for_updates)

    def _ensure_app_directory(self):
        """ホームディレクトリに専用のフォルダを自動作成する"""
        if not os.path.exists(AppConfig.APP_DIR_PATH):
            try:
                os.makedirs(AppConfig.APP_DIR_PATH)
            except Exception as e:
                print(f"ディレクトリ作成エラー: {e}")

    def _setup_window(self):
        self.title(AppConfig.APP_TITLE)
        self.geometry(AppConfig.GEOMETRY)
        ctk.set_appearance_mode(AppConfig.settings["appearance"])

    def _create_widgets(self):
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.toolbar = ctk.CTkFrame(self, height=40, corner_radius=0, fg_color=AppConfig.COLORS["toolbar_bg"])
        self.toolbar.grid(row=0, column=0, sticky="ew")
        
        self.btn_new = self._add_toolbar_button("new_file", self.add_new_tab, "Ctrl+N")
        self.btn_open = self._add_toolbar_button("open_file", self.open_file, "Ctrl+O")
        self.btn_save = self._add_toolbar_button("save_file", self.save_file, "Ctrl+S")
        self.btn_find = self._add_toolbar_button("find", self.toggle_search, "Ctrl+F")
        self.btn_preview = self._add_toolbar_button("preview", self.preview_markdown, "Ctrl+Shift+P")
        
        self.btn_settings = ctk.CTkButton(self.toolbar, text="", width=80, height=30, fg_color="transparent", 
                                          text_color=AppConfig.COLORS["text_active"], command=self.toggle_settings)
        self.btn_settings.pack(side="right", padx=10, pady=5)
        CTkToolTip(self.btn_settings, "Ctrl+,")

        self.tab_bar = ctk.CTkScrollableFrame(self, height=35, orientation="horizontal", 
                                             fg_color=AppConfig.COLORS["tabbar_bg"], corner_radius=0)
        self.tab_bar.grid(row=1, column=0, sticky="new")
        
        self.editor_container = ctk.CTkFrame(self, corner_radius=0, fg_color=AppConfig.COLORS["editor_bg"])
        self.editor_container.grid(row=1, column=0, sticky="nsew", pady=(35, 0))

        self.welcome_frame = ctk.CTkFrame(self.editor_container, fg_color="transparent")
        self.welcome_title = ctk.CTkLabel(self.welcome_frame, text="", font=(None, 28, "bold"))
        self.welcome_title.pack(pady=(0, 10))
        self.welcome_subtitle = ctk.CTkLabel(self.welcome_frame, text="", text_color=AppConfig.COLORS["text_secondary"])
        self.welcome_subtitle.pack(pady=(0, 30))
        
        btn_container = ctk.CTkFrame(self.welcome_frame, fg_color="transparent")
        btn_container.pack()
        self.welcome_new_btn = ctk.CTkButton(btn_container, text="", width=140, height=40, command=self.add_new_tab)
        self.welcome_new_btn.pack(side="left", padx=10)
        self.welcome_open_btn = ctk.CTkButton(btn_container, text="", width=140, height=40, command=self.open_file, fg_color="transparent", border_width=1)
        self.welcome_open_btn.pack(side="left", padx=10)
        
        self.status_bar = ctk.CTkFrame(self, height=25, corner_radius=0, fg_color=AppConfig.COLORS["status_bg"])
        self.status_bar.grid(row=2, column=0, sticky="ew")
        self.status_label_left = ctk.CTkLabel(self.status_bar, text="", font=("Segoe UI", 11))
        self.status_label_left.pack(side="left", padx=15)
        self.status_label_right = ctk.CTkLabel(self.status_bar, text="", font=("Segoe UI", 11))
        self.status_label_right.pack(side="right", padx=15)

    def _add_toolbar_button(self, key, command, shortcut_text=""):
        btn = ctk.CTkButton(self.toolbar, text=AppConfig.t(key), width=70, height=30, fg_color="transparent", 
                            text_color=AppConfig.COLORS["text_active"], command=command)
        btn.pack(side="left", padx=5, pady=5)
        btn.key = key
        if shortcut_text:
            CTkToolTip(btn, shortcut_text)
        return btn

    def update_ui_texts(self):
        self.btn_new.configure(text=AppConfig.t("new_file"))
        self.btn_open.configure(text=AppConfig.t("open_file"))
        self.btn_save.configure(text=AppConfig.t("save_file"))
        self.btn_find.configure(text=AppConfig.t("find"))
        self.btn_settings.configure(text=AppConfig.t("settings"))
        self.welcome_title.configure(text=AppConfig.t("welcome_title"))
        self.welcome_subtitle.configure(text=AppConfig.t("welcome_subtitle"))
        self.welcome_new_btn.configure(text=AppConfig.t("new_file"))
        self.welcome_open_btn.configure(text=AppConfig.t("open_file"))
        self.update_status_bar()

    def _setup_bindings(self):
        self.bind_all("<Control-n>", lambda e: self.add_new_tab() or "break")
        self.bind_all("<Control-o>", lambda e: self.open_file() or "break")
        self.bind_all("<Control-s>", lambda e: self.save_file() or "break")
        self.bind_all("<Control-f>", self.toggle_search)
        self.bind_all("<Control-comma>", lambda e: self.toggle_settings())
        # ショートカットキーを修正
        self.bind_all("<Control-Shift-P>", lambda e: self.preview_markdown() or "break")
        self.bind_all("<Control-Shift-p>", lambda e: self.preview_markdown() or "break")
        
        self.bind_all("<Control-l>", lambda e: self.toggle_line_numbers_global())
        self.bind_all("<Control-g>", lambda e: self.toggle_grid_global())
        self.bind_all("<Control-h>", lambda e: self.toggle_current_line_global())

    def toggle_line_numbers_global(self):
        new_state = not AppConfig.settings["show_line_numbers"]
        AppConfig.settings["show_line_numbers"] = new_state
        self.line_num_var.set(new_state)
        for tab in self.tabs.values():
            tab["editor"].toggle_line_numbers(new_state)

    def toggle_grid_global(self):
        new_state = not AppConfig.settings["show_grid"]
        AppConfig.settings["show_grid"] = new_state
        self.grid_var.set(new_state)
        for tab in self.tabs.values():
            tab["editor"].update_line_numbers()
            tab["editor"].highlight_current_line()

    def toggle_current_line_global(self):
        new_state = not AppConfig.settings["show_current_line"]
        AppConfig.settings["show_current_line"] = new_state
        self.cur_line_var.set(new_state)
        for tab in self.tabs.values():
            tab["editor"].highlight_current_line()

    def update_status_bar(self):
        if self.settings_visible:
            self.status_label_left.configure(text=AppConfig.t("settings_title"))
            self.status_label_right.configure(text="")
            return

        if not self.current_tab_id or self.current_tab_id not in self.tabs:
            self.status_label_left.configure(text=AppConfig.t("no_file"))
            self.status_label_right.configure(text="")
            return
            
        editor = self.tabs[self.current_tab_id]["editor"]
        mod = AppConfig.t("modified") if editor.is_modified else ""
        self.status_label_left.configure(text=f"{editor.file_path or AppConfig.t('untitled')}{mod}")
        line, col = editor.textbox.index("insert").split(".")
        self.status_label_right.configure(text=AppConfig.t("line_col", line=line, col=col, chars=len(editor.get("1.0", "end-1c")), mode=editor.mode))

    def _check_empty_state(self):
        if self.settings_visible: return
        if not self.tabs:
            self.welcome_frame.place(relx=0.5, rely=0.5, anchor="center")
            self.tab_bar.grid_remove()
        else:
            self.welcome_frame.place_forget()
            self.tab_bar.grid()
    
    def _setup_auto_preview(self):
        """バックグラウンドでHTMLファイルを更新し続ける"""
        self.save_preview_html()
        interval_ms = AppConfig.settings.get("preview_interval", 5) * 1000
        self.after(interval_ms, self._setup_auto_preview)
    
    def save_preview_html(self):
        """現在の内容を一時ファイルに上書き保存する（ブラウザは開かない）"""
        if not self.current_tab_id or self.current_tab_id not in self.tabs:
            return None
        
        tab = self.tabs[self.current_tab_id]
        content = tab["editor"].get("1.0", "end-1c")

        # --- 数式・化学式保護ロジック ---
        math_blocks = []
        def save_math(match):
            placeholder = f"@@MATH{len(math_blocks)}@@"
            math_blocks.append(match.group(0))
            return placeholder

        # 正規表現：$$, $, \begin{}, \ce{} を保護
        pattern = r'(\$\$.*?\$\$|\\begin\{.*?\}.*?\\end\{.*?\}|\\ce\{.*?\}|\$.*?\$)'
        content_protected = re.sub(pattern, save_math, content, flags=re.DOTALL)
        
        # 変数名を html_body に統一
        html_body = markdown2.markdown(content_protected, extras=["fenced-code-blocks", "tables", "task_lists"])

        # 保護していた数式を復元
        for i, block in enumerate(math_blocks):
            html_body = html_body.replace(f"@@MATH{i}@@", block)

        # UI設定に基づいた配色
        is_dark = ctk.get_appearance_mode() == "Dark"
        bg_color = "#1a1a1a" if is_dark else "white"
        text_color = "#e0e0e0" if is_dark else "black"
        
        interval_sec = AppConfig.settings.get("preview_interval", 5)

        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <script>
                // ブラウザ側のリロード間隔も設定値に同期
                setInterval(() => {{ location.reload(); }}, {interval_sec * 1000});
                
                // スクロール位置の維持ロジック (UX向上)
                window.onbeforeunload = function() {{ localStorage.setItem('scrollPos', window.scrollY); }};
                window.onload = function() {{
                    if (localStorage.getItem('scrollPos')) 
                        window.scrollTo(0, parseInt(localStorage.getItem('scrollPos')));
                }};
                
                window.MathJax = {{
                  tex: {{
                    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
                    processEscapes: true
                  }},
                  loader: {{ load: ['[tex]/mhchem'] }}
                }};
            </script>
            <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
            <style>
                body {{ background-color: {bg_color}; color: {text_color}; font-family: sans-serif; line-height: 1.7; max-width: 850px; margin: 0 auto; padding: 40px; }}
                h1 {{ border-bottom: 2px solid #569CD6; padding-bottom: 10px; }}
                pre {{ background: #2b2b2b; color: #f8f8f2; padding: 15px; border-radius: 8px; overflow-x: auto; }}
                .MathJax {{ font-size: 1.1em !important; }}
            </style>
        </head>
        <body>{html_body}</body>
        </html>
        """
        
        if self.preview_file is None:
            temp = tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8")
            self.preview_file = temp
            temp.close()
        
        try:
            with open(self.preview_file.name, "w", encoding="utf-8") as f:
                f.write(full_html)
            return self.preview_file.name
        except:
            return None
    
    def preview_markdown(self):
        """手動でプレビューをブラウザに表示する"""
        path = self.save_preview_html()
        if path:
            webbrowser.open(f"file://{path}")

    def _setup_window(self):
        # タイトルにバージョンを表示
        self.title(f"{AppConfig.APP_TITLE} - v{VERSION}")
        self.geometry(AppConfig.GEOMETRY)
        ctk.set_appearance_mode(AppConfig.settings["appearance"])

    def check_for_updates(self):
        """GitHub APIを使用して最新バージョンを確認する"""
        def _check():
            try:
                response = requests.get(AppConfig.GITHUB_API_URL, timeout=(5, 15))
                print(f"Update check: status code {response.status_code}") # デバッグ用
                
                if response.status_code == 200:
                    data = response.json()
                    latest_version_str = data["tag_name"].lstrip('v')
                    
                    # デバッグ用にコンソール出力
                    print(f"Current version: {VERSION}")
                    print(f"Latest version on GitHub: {latest_version_str}")
                    
                    if version.parse(latest_version_str) > version.parse(VERSION):
                        self.after(0, lambda: self._show_update_dialog(latest_version_str, data["html_url"]))
                    else:
                        print("No update available.")
            except Exception as e:
                print(f"Update check failed: {e}")

        # バックグラウンドスレッドで実行
        thread = threading.Thread(target=_check, daemon=True)
        thread.start()

    def _show_update_dialog(self, latest_ver, download_url):
        """アップデート通知ダイアログを表示"""
        msg = AppConfig.t("update_available", version=latest_ver)
        if messagebox.askyesno(AppConfig.t("update_title"), msg):
            webbrowser.open(download_url)

if __name__ == "__main__":
    app = MultiTabApp()
    try:
        app.mainloop()
    except KeyboardInterrupt:
        pass