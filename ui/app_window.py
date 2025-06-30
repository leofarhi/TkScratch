import customtkinter as ctk
import tkinter as tk
from ui.menu_bar import MenuBar
from ui.sidebar import SideBar
from ui.stage_area import StageArea
from ui.info_area import InfoArea
from ui.center_area import CenterArea
from modules.i18n import LanguageManager
from modules.config import Settings
from engine.Project import Project

from engine.GameObject import GameObject
from engine.Sound import Sound
from engine.Sprite import Sprite
test_Project = Project()
test_Project.add_game_object(GameObject("Sprite1", 100, 150))
test_Project.add_game_object(GameObject("Sprite2", 200, 250))

class ScratchApp(ctk.CTk):
    def __init__(self, settings : Settings, language_manager: LanguageManager):
        super().__init__()
        self.settings = settings
        self.project = Project()
        self.language_manager = language_manager
        self.refresh_callbacks = []

        ctk.set_appearance_mode(settings.get("theme"))
        ctk.set_default_color_theme("blue")

        self.title("Scratch Clone")
        self.geometry("1600x900")

        # === CUSTOM MENU ===
        self.menu_area = MenuBar(self, self)
        self.menu_area.pack(fill="x", side="top")

        # === MAIN FRAME ===
        # === Main Paned Window ===
        def themed_color():
            return ctk.ThemeManager.theme["CTkFrame"]["border_color"][self.settings.get("theme") == "dark"]

        self.main_paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashwidth=6, sashrelief=tk.RIDGE, bg=themed_color())
        self.main_paned.pack(fill="both", expand=True)
        self.add_refresh(lambda: self.main_paned.config(bg=themed_color()))

        # === Bloc gauche (Tabview) ===
        self.sidebar = SideBar(self, self.main_paned, bg_color=ctk.ThemeManager.theme["CTkFrame"]["border_color"])
        self.main_paned.add(self.sidebar, minsize=200)

        self.center_area = CenterArea(self, self.main_paned, bg_color=ctk.ThemeManager.theme["CTkFrame"]["border_color"])
        self.main_paned.add(self.center_area, minsize=300, width=2200)
        
        # === Zone droite (scène + infos) ===
        self.rightside = ctk.CTkFrame(self.main_paned, bg_color=ctk.ThemeManager.theme["CTkFrame"]["border_color"])
        self.main_paned.add(self.rightside, minsize=100, width=200)
        self.rightside.pack_propagate(False)

        # === Scène ===
        self.stage_area = StageArea(self, self.rightside)
        self.stage_area.pack(side="top", fill="both", anchor="n")

        # === Info Area ===
        self.info_area = InfoArea(self, self.rightside, bg_color="transparent", fg_color="transparent")
        self.info_area.pack(side="bottom", fill="both", expand=True)

        self.refresh()
        return

    def refresh(self):
        for callback in self.refresh_callbacks:
            callback()

    def add_refresh(self, callback):
        self.refresh_callbacks.append(callback)
