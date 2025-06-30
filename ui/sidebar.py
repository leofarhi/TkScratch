import customtkinter as ctk
from ui.tabs.code.tab import CodeTab
from ui.tabs.costumes.tab import CostumesTab
from ui.tabs.sounds.tab import SoundsTab

class SideBar(ctk.CTkFrame):
    def __init__(self, app, master, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        get_text = lambda p: self.app.language_manager.get(p)
        self.pack_propagate(False)
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=5, pady=5)
        self.tabs.add("code")
        self.tabs.add("costumes")
        self.tabs.add("sounds")
        self.tabs.current_names = {
            "code":"code",
            "costumes":"costumes",
            "sounds":"sounds"
        }
        self.tabs._segmented_button.configure(command=self._segmented_button_callback)
        # Add frames to the tabs
        self.tab_code = CodeTab(self.app, self.tabs.tab("code"))
        self.tab_code.pack(fill="both", expand=True)
        self.tab_costumes = CostumesTab(self.app, self.tabs.tab("costumes"))
        self.tab_costumes.pack(fill="both", expand=True)
        self.tab_sounds = SoundsTab(self.app, self.tabs.tab("sounds"))
        self.tab_sounds.pack(fill="both", expand=True)

        self.app.add_refresh(self.refresh)

    def refresh(self):
        get_text = lambda p: self.app.language_manager.get(p)
        for key,button in self.tabs._segmented_button._buttons_dict.items():
            button.configure(text=get_text(f"tabs.{key}"))
        self.tabs.update()

    def _segmented_button_callback(self, selected_name):
         self.tabs._segmented_button_callback(selected_name)
         self.on_tab_changed(selected_name)

    def on_tab_changed(self, current_tab):
        tab_id = list(self.tabs.current_names.keys())[list(self.tabs.current_names.values()).index(current_tab)]
        self.app.center_area.show_frame(tab_id)