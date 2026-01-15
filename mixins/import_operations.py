from tkinter import filedialog, messagebox
from config import AppConfig
import pypandoc
import shutil
import os

class ImportOperationsMixin:
    def convert_to_markdown(self, path):
        """[新規追加] テキストのみを変換して読み込むヘルパー"""
        try:
            ext = os.path.splitext(path)[1].lstrip('.').lower()
            return pypandoc.convert_file(path, 'gfm', format=ext)
        except Exception as e:
            messagebox.showerror("Conversion Error", f"変換失敗: {e}")
            return None

    def import_as_bundle(self, existing_path=None):
        """existing_path 引数を受け取れるように修正"""
        path = existing_path or filedialog.askopenfilename(
            filetypes=[("Importable files", "*.docx *.html *.htm")]
        )
        if not path: return

        base_dir = os.path.dirname(path)
        file_name = os.path.splitext(os.path.basename(path))[0]
        bundle_dir = os.path.join(base_dir, f"{file_name}_bundle")
        assets_dir = os.path.join(bundle_dir, "assets")

        try:
            os.makedirs(assets_dir, exist_ok=True)
            ext = os.path.splitext(path)[1].lstrip('.').lower()
            output = pypandoc.convert_file(
                path, 'gfm', format=ext,
                extra_args=['--extract-media', bundle_dir] 
            )
            # mediaフォルダをassetsへ整理
            media_path = os.path.join(bundle_dir, "media")
            if os.path.exists(media_path):
                for f in os.listdir(media_path):
                    shutil.move(os.path.join(media_path, f), os.path.join(assets_dir, f))
                shutil.rmtree(media_path)
                output = output.replace("media/", "assets/")

            index_path = os.path.join(bundle_dir, "index.md")
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(output)
            self.add_new_tab(file_path=index_path, content=output)
        except Exception as e:
            messagebox.showerror("Error", str(e))
