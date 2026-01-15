import customtkinter as ctk
from tkinter import Canvas
import os
import re
from config import AppConfig

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
