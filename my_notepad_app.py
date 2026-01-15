VERSION = "1.5.0"

import customtkinter as ctk
from tkinter import messagebox
import os
import re
import markdown2
import tempfile
import threading
import requests
import webbrowser
from packaging import version

# Import from new modules
from config import AppConfig, I18n, CTkToolTip
from ui_components import EditorView, SyntaxHighlighter
from mixins import (
    TabOperationsMixin,
    FileOperationsMixin,
    SearchOperationsMixin,
    SettingsOperationsMixin,
    MarkdownEditMixin,
    ImportOperationsMixin,
)

# ==========================================
# 7. メインアプリケーション (MultiTabApp)
# ==========================================
class MultiTabApp(ctk.CTk, TabOperationsMixin, FileOperationsMixin, SearchOperationsMixin, SettingsOperationsMixin, ImportOperationsMixin, MarkdownEditMixin):
    def __init__(self):
        super().__init__()
        # --- 変数の初期化 ---
        self.preview_file = None 
        
        self._ensure_app_directory()
        self.init_tab_system()
        self._setup_window()
        self._create_widgets()
        self.init_markdown_toolbar()
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
        # レイアウトを1行分増やす調整
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1) # ここがエディタ。ここを weight=1 にする
        self.grid_rowconfigure(4, weight=0)
        self.grid_columnconfigure(0, weight=1)
        
        # --- row 0: メインツールバー ---
        self.toolbar = ctk.CTkFrame(self, height=40, corner_radius=0, fg_color=AppConfig.COLORS["toolbar_bg"])
        self.toolbar.grid(row=0, column=0, sticky="ew")
        # ボタン追加処理
        self.btn_new = self._add_toolbar_button("new_file", self.add_new_tab, "Ctrl+N")
        self.btn_open = self._add_toolbar_button("open_file", self.open_file, "Ctrl+O")
        self.btn_save = self._add_toolbar_button("save_file", self.save_file, "Ctrl+S")
        self.btn_find = self._add_toolbar_button("find", self.toggle_search, "Ctrl+F")
        self.btn_preview = self._add_toolbar_button("preview", self.preview_markdown, "Ctrl+Shift+P")
        
        self.btn_settings = ctk.CTkButton(self.toolbar, text="", width=80, height=30, fg_color="transparent", 
                                          text_color=AppConfig.COLORS["text_active"], command=self.toggle_settings)
        self.btn_settings.pack(side="right", padx=10, pady=5)
        CTkToolTip(self.btn_settings, "Ctrl+,")
        
        # --- row 1: タブバー ---
        self.tab_bar = ctk.CTkScrollableFrame(self, height=35, orientation="horizontal", 
                                             fg_color=AppConfig.COLORS["tabbar_bg"], corner_radius=0)
        self.tab_bar.grid(row=1, column=0, sticky="ew")
        
        # --- row 3: エディタコンテナ ---
        self.editor_container = ctk.CTkFrame(self, corner_radius=0, fg_color=AppConfig.COLORS["editor_bg"])
        self.editor_container.grid(row=3, column=0, sticky="nsew")
        # (Welcomeフレーム)
        self.welcome_frame = ctk.CTkFrame(self.editor_container, fg_color="transparent")
        self.welcome_title = ctk.CTkLabel(self.welcome_frame, text="", font=(None, 28, "bold"))
        self.welcome_title.pack(pady=(0, 10))
        self.welcome_subtitle = ctk.CTkLabel(self.welcome_frame, text="", text_color=AppConfig.COLORS["text_secondary"])
        self.welcome_subtitle.pack(pady=(0, 30))
        
        btn_container = ctk.CTkFrame(self.welcome_frame, fg_color="transparent")
        btn_container.pack()
        self.welcome_new_btn = ctk.CTkButton(btn_container, text="", width=140, height=40, command=self.add_new_tab)
        self.welcome_new_btn.pack(side="left", padx=10)
        CTkToolTip(self.welcome_new_btn, "Ctrl+N")
        self.welcome_open_btn = ctk.CTkButton(btn_container, text="", width=140, height=40, command=self.open_file, fg_color="transparent", border_width=1)
        self.welcome_open_btn.pack(side="left", padx=10)
        CTkToolTip(self.welcome_open_btn, "Ctrl+O")
        
        # --- row 4: ステータスバー ---
        self.status_bar = ctk.CTkFrame(self, height=25, corner_radius=0, fg_color=AppConfig.COLORS["status_bg"])
        self.status_bar.grid(row=4, column=0, sticky="ew")
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
        self.bind_all("<Control-Shift-Z>", lambda e: self.redo_action() or "break")
        self.bind_all("<Control-Shift-z>", lambda e: self.redo_action() or "break")

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
    
    def redo_action(self):
        """現在アクティブなタブのエディタでやり直し(Redo)を実行する"""
        if not self.current_tab_id or self.current_tab_id not in self.tabs:
            return
        
        # 現在のタブのエディタ(CTkTextbox)の内部テキストウィジェットでredoを実行
        editor_view = self.tabs[self.current_tab_id]["editor"]
        try:
            # CTkTextboxの内部のtkinter.Textウィジェットに対してedit_redoを呼び出す
            editor_view.textbox._textbox.edit_redo()
            # 変更があったことを検知するためにイベントハンドラを呼ぶ
            editor_view._handle_event()
        except Exception:
            # やり直す履歴がない場合は何もしない
            pass

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
        editor = tab["editor"]
        content = editor.get("1.0", "end-1c")
        
        base_tag = ""
        if editor.file_path:
            # ファイルが存在するディレクトリをBaseにすることで assets/image.png が読み込める
            file_dir = os.path.abspath(os.path.dirname(editor.file_path)).replace("\\", "/")
            base_tag = f'<base href="file:///{file_dir}/">'
        
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
        border_color = "#444" if is_dark else "#ccc"
        header_bg = "#333" if is_dark else "#f5f5f5"
        
        interval_sec = AppConfig.settings.get("preview_interval", 5)

        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            {base_tag}
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
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; border: 1px solid {border_color}; }}
                th, td {{ border: 1px solid {border_color}; padding: 12px; text-align: left; }}
                th {{ background-color: {header_bg}; font-weight: bold; }}
                tr:nth-child(even) {{ background-color: rgba(128,128,128,0.05); }}
                img {{ max-width: 100%; height: auto; border-radius: 4px; }}
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