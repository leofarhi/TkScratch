import customtkinter as ctk
import tkinter as tk

class StageArea(tk.Frame):
    def __init__(self, app, master, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        #self.pack_propagate(False)
        self.scene_canvas = tk.Canvas(self, bg="white", highlightthickness=1, relief="solid")
        self.scene_canvas.pack()

        self.resize_job = None
        self.bind("<Configure>", self.maintain_aspect_ratio)

    def maintain_aspect_ratio(self, event):
        if self.resize_job:
            self.after_cancel(self.resize_job)

        def do_resize():
            container_width = self.winfo_width()
            new_height = int(container_width * 3 / 4)
            self.scene_canvas.config(width=container_width, height=new_height)

        self.resize_job = self.after_idle(do_resize)
