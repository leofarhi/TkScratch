import customtkinter as ctk
import tkinter as tk

class CodeTab(ctk.CTkFrame):
    def __init__(self, app, master, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app