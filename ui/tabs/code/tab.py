import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
from ui.widgets.VerticalTabview import VerticalTabview
from ui.block.blocks import blocks_available


class DragPopup:
    def __init__(self, master, img: Image.Image):
        self.master = master
        self.img = img

        # Convertir en PhotoImage RGBA
        self.tk_img = ImageTk.PhotoImage(self.img)

        # Créer la fenêtre popup
        self.popup = tk.Toplevel(master)
        self.popup.overrideredirect(True)
        self.popup.attributes('-topmost', True)

        # Définir la couleur transparente pour Windows
        transparent_color = '#FF00FF'
        self.popup.config(bg=transparent_color)
        self.popup.wm_attributes('-transparentcolor', transparent_color)

        # Créer le Label avec fond transparent
        self.label = tk.Label(self.popup, image=self.tk_img, bg=transparent_color, bd=0)
        self.label.pack(padx=5, pady=5)

    def move(self, x, y):
        """Déplace le popup"""
        self.popup.geometry(f"+{x}+{y}")

    def destroy(self):
        """Ferme le popup"""
        self.popup.destroy()


class CodeTab(ctk.CTkFrame):
    def __init__(self, app, master, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app

        # ---- Drag state ----
        self.drag_popup = None

        # ---- TabView à gauche ----
        self.tabview = VerticalTabview(self)
        self.tabview.pack(fill="both", expand=True)

        # ---- Onglets ----
        self.tabs = list(blocks_available.keys())
        self.scroll_frames = {}

        for tab_name in self.tabs:
            tab = self.tabview.add(tab_name)

            scroll = ctk.CTkScrollableFrame(tab, width=800, height=600)
            scroll.pack(fill="both", expand=True, padx=1, pady=1)
            self.scroll_frames[tab_name] = scroll

            section_label = ctk.CTkLabel(
                scroll,
                text=f"{tab_name} Blocks",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            section_label.pack(pady=(10, 5), anchor="w")

            for block in blocks_available[tab_name]:
                svg = block.build_svg()
                img = svg.draw(background_color=(255, 255, 255, 0))

                block_img = ctk.CTkImage(dark_image=img, light_image=img, size=(int(img.size[0] / 2.75), int(img.size[1] / 2.75)))

                btn = ctk.CTkButton(
                    scroll,
                    text="",
                    image=block_img,
                    compound="left",
                    fg_color="transparent",
                    hover=False,
                    cursor="hand2",
                )
                btn.pack(pady=5, anchor="w")

                btn.bind("<ButtonPress-1>", lambda e, img=img: self.start_drag(e, img))
                btn.bind("<B1-Motion>", self.do_drag)
                btn.bind("<ButtonRelease-1>", self.stop_drag)

    def start_drag(self, event, img):
        """Démarre le drag avec un vrai popup transparent"""
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        self.drag_popup = DragPopup(self.app, img)
        self.do_drag(event)

    def do_drag(self, event):
        """Déplace le popup"""
        if self.drag_popup:
            x = self.app.winfo_pointerx()
            y = self.app.winfo_pointery()
            self.drag_popup.move(x, y)

    def stop_drag(self, event):
        """Stoppe le drag"""
        if self.drag_popup:
            self.drag_popup.destroy()
            self.drag_popup = None
