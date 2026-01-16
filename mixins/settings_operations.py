import customtkinter as ctk
from tkinter import filedialog, messagebox
from config import AppConfig
import os

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
                                     text=AppConfig.t("version_label", version=AppConfig.APP_VERSION),
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
            self.ver_label.configure(text=AppConfig.t("version_label", version=AppConfig.APP_VERSION))

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
        
        # 設定を保存
        AppConfig.save_settings()
        
        self.update_ui_texts()
        self.update_settings_ui_texts()
        messagebox.showinfo(AppConfig.t("settings_title"), AppConfig.t("settings_applied"))
