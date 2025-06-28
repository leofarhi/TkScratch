import customtkinter as ctk
from ui.tabs.costumes.center_area import CostumesArea
from ui.tabs.code.center_area import CodeArea
from ui.tabs.sounds.center_area import SoundsArea

class CenterArea(ctk.CTkFrame):
    def __init__(self, app, master, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.center_area ={
            "code": CodeArea(app, self),
            "costumes": CostumesArea(app, self),
            "sounds": SoundsArea(app, self)
        }
        self.current_frame = None
        self.show_frame("code")

    def show_frame(self, frame_name):
        if self.current_frame is not None:
            self.current_frame.pack_forget()
        self.current_frame = self.center_area[frame_name]
        self.current_frame.pack(fill="both", expand=True, padx=5, pady=5)