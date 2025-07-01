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

############### TEST ###############
from engine.GameObject import GameObject
from engine.Sound import Sound
from engine.Sprite import Sprite

test_Project = Project()
test_Project.add_game_object(GameObject("Sprite1", 100, 150))
test_Project.add_game_object(GameObject("Sprite2", 200, 250))


import random
import string
from PIL import Image, ImageDraw

def random_sprite():
    w, h = random.randint(200, 400), random.randint(200, 400)
    color = tuple(random.randint(0, 255) for _ in range(3)) + (255,)
    name = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    image = Image.new("RGBA", (w, h), color)
    draw = ImageDraw.Draw(image)
    draw.text((w//4, h//4), "🐱", fill=(255, 255, 255, 255))

    sprite = Sprite(name, image)
    return sprite

test_Project.game_objects[0].sprites.append(random_sprite())
test_Project.game_objects[0].sprites.append(random_sprite())
test_Project.game_objects[1].sprites.append(random_sprite())
test_Project.game_objects[1].sprites.append(random_sprite())

test_Project.game_objects[1].sounds.append(Sound("Sound1", "tests/test.wav"))
test_Project.game_objects[2].sounds.append(Sound("Sound2", "tests/test2.wav"))
test_Project.game_objects[2].sounds.append(Sound("Sound1", "tests/test.wav"))
####################################

class ScratchApp(ctk.CTk):
    def __init__(self, settings : Settings, language_manager: LanguageManager):
        super().__init__()
        self.settings = settings
        self.project = test_Project#Project()
        self.language_manager = language_manager
        self.refresh_callbacks = []
        self.on_game_object_selected_callbacks = []

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
        self.set_current_object(self.project.game_objects[0])
        return

    def refresh(self):
        for callback in self.refresh_callbacks:
            callback()

    def add_refresh(self, callback):
        self.refresh_callbacks.append(callback)

    def on_game_object_selected(self, callback):
        self.on_game_object_selected_callbacks.append(callback)

    def set_current_object(self, obj: GameObject):
        self.project.current_object = obj
        for callback in self.on_game_object_selected_callbacks:
            callback(obj)
