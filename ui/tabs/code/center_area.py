import customtkinter as ctk

class CodeArea(ctk.CTkFrame):
    def __init__(self, app, master, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        #label
        self.label = ctk.CTkLabel(self, text="Code Area", font=("Arial", 24))
        self.label.pack(pady=20)