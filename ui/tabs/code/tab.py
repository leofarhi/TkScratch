import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageDraw
import random
from ui.widgets.VerticalTabview import VerticalTabview

class CodeTab(ctk.CTkFrame):
    def __init__(self, app, master, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        # Conteneur principal
        #self.grid_columnconfigure(1, weight=1)
        #self.grid_rowconfigure(0, weight=1)

        # TabView à gauche
        self.tabview = VerticalTabview(self)
        self.tabview.pack(fill="both", expand=True)


        # Onglets à créer
        self.tabs = ["Motion", "Looks", "Sound", "Events", "Control", "Sensing", "Operators", "Variables", "My Blocks"]

        # Stocker les frames scrollables par onglet
        self.scroll_frames = {}

        for tab_name in self.tabs:
            tab = self.tabview.add(tab_name)

            # Scrollable Frame dans chaque tab
            scroll = ctk.CTkScrollableFrame(tab, width=800, height=600)
            scroll.pack(fill="both", expand=True, padx=1, pady=1)

            self.scroll_frames[tab_name] = scroll

            # Exemple de contenu
            section_label = ctk.CTkLabel(scroll, text=f"{tab_name} Blocks", font=ctk.CTkFont(size=18, weight="bold"))
            section_label.pack(pady=(10, 5), anchor="w")

            for i in range(18):
                img = self.generate_block_image()
                block_img = ctk.CTkImage(dark_image=img, light_image=img, size=(200, 40))
                btn = ctk.CTkButton(scroll, text=f"{tab_name} Block {i+1}", image=block_img, compound="left")
                btn.pack(pady=5, anchor="w")

    def generate_block_image(self):
        """Crée une image PIL de couleur aléatoire."""
        img = Image.new("RGB", (200, 40), self.random_color())
        draw = ImageDraw.Draw(img)
        draw.text((10, 10), "Block", fill="white")
        return img

    def random_color(self):
        """Couleur RGB aléatoire (plutôt claire)."""
        return tuple(random.randint(100, 255) for _ in range(3))