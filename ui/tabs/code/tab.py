import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
from ui.widgets.VerticalTabview import VerticalTabview
from ui.tabs.code.center_area import CodeArea
from ui.block.blocks import blocks_available
from functools import partial


class DragPopup:
    def __init__(self, master, img: Image.Image):
        self.master = master
        self.img = img

        self.tk_img = ImageTk.PhotoImage(self.img)

        self.popup = tk.Toplevel(master)
        self.popup.overrideredirect(True)
        self.popup.attributes('-topmost', True)

        transparent_color = '#FF00FF'
        self.popup.config(bg=transparent_color)
        self.popup.wm_attributes('-transparentcolor', transparent_color)

        self.label = tk.Label(self.popup, image=self.tk_img, bg=transparent_color, bd=0)
        self.label.pack()

        self.width = self.tk_img.width()+2  # Adding 2 for padding
        self.height = self.tk_img.height()+ 2  # Adding 2 for padding

    def move(self, x, y, offset_x=0, offset_y=0):
        """Déplace le popup en conservant l'offset"""
        new_x = x - offset_x
        new_y = y - offset_y
        self.popup.geometry(f"{self.width}x{self.height}+{new_x}+{new_y}")

    def destroy(self):
        self.popup.destroy()


class CodeTab(ctk.CTkFrame):
    def __init__(self, app, master, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app

        # ---- Drag state ----
        self.drag_popup = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        # ---- TabView à gauche ----
        self.tabview = VerticalTabview(self)
        self.tabview.pack(fill="both", expand=True)

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
                    fg_color="transparent",
                    hover=False,
                    cursor="hand2",
                    border_spacing=0,
                    border_width=0,
                    corner_radius=0,
                )
                btn.pack(pady=5, anchor="w")

                btn.bind("<ButtonPress-1>", partial(self.start_drag, img=img, block=block))
                btn.bind("<B1-Motion>", self.do_drag)
                btn.bind("<ButtonRelease-1>", self.stop_drag)

    def start_drag(self, event, img, block):
        """Démarre le drag en calculant l'offset"""
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        self.drag_popup = DragPopup(self.app, img)
        self.drag_block = block

        # Calcul de l'offset clic → image
        self.drag_offset_x = event.x
        self.drag_offset_y = event.y

        self.do_drag(event)

    def do_drag(self, event):
        """Déplace le popup en tenant compte de l'offset"""
        if self.drag_popup:
            x = self.app.winfo_pointerx()
            y = self.app.winfo_pointery()
            self.drag_popup.move(x, y, self.drag_offset_x, self.drag_offset_y)

    def stop_drag(self, event):
        """Stoppe le drag et fait le drop sur le canvas"""
        if self.drag_popup:
            # Coords absolues
            abs_x = self.app.winfo_pointerx()
            abs_y = self.app.winfo_pointery()

            # Récupère le canvas
            canvas = CodeArea.Instance.canvas

            # Convertit en coords locales au canvas
            canvas_x = abs_x - canvas.winfo_rootx() - self.drag_offset_x
            canvas_y = abs_y - canvas.winfo_rooty() - self.drag_offset_y

            # Drop réel
            CodeArea.Instance.drop_block(self.drag_block.clone(), canvas_x, canvas_y)

            # Nettoie le popup
            self.drag_popup.destroy()
            self.drag_popup = None

