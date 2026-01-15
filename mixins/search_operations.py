import customtkinter as ctk
from config import AppConfig

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
