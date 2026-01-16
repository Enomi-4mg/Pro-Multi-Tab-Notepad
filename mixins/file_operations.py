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
            # 最近のファイルリストに追加
            self._add_to_recent(path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read: {e}")
    
    def open_file_by_path(self, path):
        """指定したパスのファイルを開く（起動時引数や履歴からの呼び出し用）"""
        if not os.path.exists(path):
            messagebox.showerror(
                AppConfig.t("file_not_found"),
                AppConfig.t("file_not_found", path=path)
            )
            # 存在しないファイルを履歴から削除
            if path in AppConfig.settings["recent_files"]:
                AppConfig.settings["recent_files"].remove(path)
            return
        
        ext = os.path.splitext(path)[1].lower()
        
        # docxの場合はBundleインポート
        if ext == ".docx":
            self.import_as_bundle(existing_path=path)
            self._add_to_recent(path)
            return
        
        # 通常のテキストファイル
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.add_new_tab(file_path=path, content=content)
            self._add_to_recent(path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read: {e}")

    def save_file(self):
        if not self.current_tab_id: return
        tab = self.tabs[self.current_tab_id]
        editor = tab["editor"]
        
        # 既存ファイルの場合はそのまま保存、新規ファイルの場合はinitialdirを設定
        if editor.file_path:
            path = editor.file_path
        else:
            # 新規ファイル: last_save_dir または default_dir を使用
            initial_dir = AppConfig.settings.get("last_save_dir") or AppConfig.settings["default_dir"]
            path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                initialdir=initial_dir
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
                
                # 保存先ディレクトリを記憶
                AppConfig.settings["last_save_dir"] = os.path.dirname(path)
                
                # 最近のファイルリストに追加
                self._add_to_recent(path)
                
                self.update_status_bar()
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def save_file_as(self):
        """別名で保存機能"""
        if not self.current_tab_id: return
        tab = self.tabs[self.current_tab_id]
        editor = tab["editor"]
        
        # initialdirを現在のファイルのディレクトリまたはlast_save_dirに設定
        if editor.file_path:
            initial_dir = os.path.dirname(editor.file_path)
        else:
            initial_dir = AppConfig.settings.get("last_save_dir") or AppConfig.settings["default_dir"]
        
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialdir=initial_dir,
            initialfile=os.path.basename(editor.file_path) if editor.file_path else "untitled.txt"
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
                
                # 保存先ディレクトリを記憶
                AppConfig.settings["last_save_dir"] = os.path.dirname(path)
                
                # 最近のファイルリストに追加
                self._add_to_recent(path)
                
                self.update_status_bar()
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def _add_to_recent(self, path):
        """最近のファイルリストに追加（最大10件まで）"""
        abs_path = os.path.abspath(path)
        recent = AppConfig.settings["recent_files"]
        
        # 重複を削除
        if abs_path in recent:
            recent.remove(abs_path)
        
        # 先頭に追加
        recent.insert(0, abs_path)
        
        # 最大10件に制限
        AppConfig.settings["recent_files"] = recent[:10]
