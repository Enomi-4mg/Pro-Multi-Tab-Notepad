import customtkinter as ctk
from config import AppConfig
from ui_components import EditorView

class TabOperationsMixin:
    def init_tab_system(self):
        self.tabs = {}
        self.tab_order = []
        self.current_tab_id = None
        self.tab_count = 0

    def add_new_tab(self, file_path=None, content=""):
        self.tab_count += 1
        tab_id = f"tab_{self.tab_count}"
        name = __import__("os").path.basename(file_path) if file_path else f"{AppConfig.t('untitled')} {self.tab_count}"

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
        self.update_toolbar_visibility()
    
    def close_tab(self, tab_id):
        from tkinter import messagebox
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
