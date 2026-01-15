import customtkinter as ctk
from config import AppConfig

class MarkdownEditMixin:
    def init_markdown_toolbar(self):
        """Markdown専用の補助ボタンバーを作成 (初期は隠しておく)"""
        # toolbarの下に配置するためのフレーム
        self.md_toolbar = ctk.CTkFrame(self, height=35, fg_color=AppConfig.COLORS["toolbar_bg"])
        
        # 挿入ボタンの定義
        buttons = [
            ("H1", "# "), ("H2", "## "), ("B", "**", "**"), 
            ("I", "*", "*"), ("List", "- "), ("Table", "\n| col | col |\n|---|---|\n| val | val |\n")
        ]

        for b in buttons:
            label = b[0]
            prefix = b[1]
            suffix = b[2] if len(b) > 2 else ""
            btn = ctk.CTkButton(self.md_toolbar, text=label, width=40, height=25, 
                                font=("Segoe UI", 11), fg_color="transparent", border_width=1,
                                command=lambda p=prefix, s=suffix: self.insert_md_tag(p, s))
            btn.pack(side="left", padx=2, pady=5)

    def insert_md_tag(self, prefix, suffix=""):
        if not self.current_tab_id: return
        editor = self.tabs[self.current_tab_id]["editor"].textbox
        try:
            # 選択範囲があれば囲む、なければカーソル位置に挿入
            sel_text = editor.get("sel.first", "sel.last")
            editor.delete("sel.first", "sel.last")
            editor.insert("insert", f"{prefix}{sel_text}{suffix}")
        except:
            editor.insert("insert", f"{prefix}{suffix}")
            if suffix: editor.mark_set("insert", f"insert-{len(suffix)}c")

    def update_toolbar_visibility(self):
        """現在のファイルのモードに応じてツールバーの表示/非表示を切り替える"""
        if not self.current_tab_id or self.current_tab_id not in self.tabs:
            self.md_toolbar.grid_remove()
            return

        editor = self.tabs[self.current_tab_id]["editor"]
        if editor.mode == "Markdown":
            # gridでtoolbarの下(row=2)に表示
            self.md_toolbar.grid(row=2, column=0, sticky="ew")
        else:
            self.md_toolbar.grid_remove()
