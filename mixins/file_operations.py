from tkinter import filedialog, messagebox
from config import AppConfig
import pypandoc
import shutil
import os

class FileOperationsMixin:
    def open_file(self):
        # 選択できるファイル形式を拡張
        file_types = [
            ("Supported files", "*.txt *.md *.docx *.html *.htm"),
            ("Markdown/Text", "*.txt *.md"),
            ("Word Document", "*.docx"),
            ("HTML document", "*.html *.htm"),
            ("All files", "*.*")
        ]
        
        path = filedialog.askopenfilename(
            initialdir=AppConfig.settings["default_dir"],
            filetypes=file_types
        )
        
        if not path: return
        
        ext = os.path.splitext(path)[1].lower()
        # HTML/CSSの場合の選択肢
        if ext in [".html", ".htm", ".css"]:
            msg = f"「{os.path.basename(path)}」をどう開きますか？\n\n[はい]: Markdownに変換 (Bundle)\n[いいえ]: ソースコードとして開く"
            choice = messagebox.askyesno("開くオプション", msg)
            if choice: # Markdown変換
                self.import_as_bundle(existing_path=path)
                return
            # 「いいえ」の場合はそのまま下のテキスト読み込みへ流す
        # docxの場合はBundleインポートへ誘導
        if ext == ".docx":
            self.import_as_bundle(existing_path=path)
            return

        # 通常のファイル読み込み処理
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.add_new_tab(file_path=path, content=content)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read: {e}")

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
