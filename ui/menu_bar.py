import customtkinter as ctk
from tkinter import filedialog

class MenuBar(ctk.CTkFrame):
    def __init__(self, app, master):
        super().__init__(master, height=40)
        self.app = app
        get_text = lambda p: self.app.language_manager.get(p)

        self.file_menu = ctk.CTkOptionMenu(self, values=["New", "Load", "Save"], command=self.file_action)
        self.file_menu.set(get_text("menu.file.label"))
        self.file_menu.pack(side="left", padx=5)

        self.edit_menu = ctk.CTkOptionMenu(self, values=["Coming soon"])
        self.edit_menu.set(get_text("menu.edit.label"))
        self.edit_menu.pack(side="left", padx=5)

        self.lang_menu = ctk.CTkOptionMenu(self, values=list(self.app.language_manager.languages.values()), command=self.set_language)
        self.lang_menu.set(get_text("menu.language.label"))
        self.lang_menu.pack(side="left", padx=5)

        self.theme_menu = ctk.CTkOptionMenu(self, values=["Light", "Dark"], command=self.set_theme)
        self.theme_menu.set(get_text("menu.theme.label"))
        self.theme_menu.pack(side="left", padx=5)


        # === Contrôles à droite du menu ===
        # Fullscreen toggle state
        fullscreen_state = [False]

        def start_action():
            print("▶️ Start clicked")

        def stop_action():
            print("⏹️ Stop clicked")

        def toggle_fullscreen():
            fullscreen_state[0] = not fullscreen_state[0]
            self.app.attributes("-fullscreen", fullscreen_state[0])
            self.fullscreen_btn.configure(text="🗕" if fullscreen_state[0] else "⛶")

        self.fullscreen_btn = ctk.CTkButton(self, text="⛶", width=20, command=toggle_fullscreen)
        self.fullscreen_btn.pack(side="right", padx=5)

        self.stop_btn = ctk.CTkButton(self, text="⏹", width=40, command=stop_action)
        self.stop_btn.pack(side="right", padx=5)

        self.start_btn = ctk.CTkButton(self, text="▶", width=40, command=start_action)
        self.start_btn.pack(side="right", padx=5)

        self.app.add_refresh(self.refresh)

    def refresh(self):
        get_text = lambda p: self.app.language_manager.get(p)
        self.file_menu.set(get_text("menu.file.label"))
        self.edit_menu.set(get_text("menu.edit.label"))
        self.lang_menu.set(get_text("menu.language.label"))
        self.theme_menu.set(get_text("menu.theme.label"))
        self.file_menu.configure(values=[
            get_text("menu.file.new"),
            get_text("menu.file.load"),
            get_text("menu.file.save")
        ])
        self.edit_menu.configure(values=[get_text("menu.edit.coming_soon")])
        self.theme_menu.configure(values=[
            get_text("menu.theme.light"),
            get_text("menu.theme.dark")
        ])

    def file_action(self, choice):
        get_text = lambda p: self.app.language_manager.get(p)
        self.file_menu.set(self.app.language_manager.get("menu.file.label"))
        if choice == get_text("menu.file.load"):
            filedialog.askopenfilename()
        elif choice == get_text("menu.file.save"):
            filedialog.asksaveasfilename()
        elif choice == get_text("menu.file.new"):
            print("New Project triggered")

    def set_language(self, lang_label):
        lang = "en"
        for code, name in self.app.language_manager.languages.items():
            if name == lang_label:
                lang = code
                break
        else:
            print(f"Language '{lang_label}' not found, defaulting to 'en'.")
        self.app.language_manager.load(lang)
        self.app.settings.set("language", lang, auto_save=True)
        self.app.refresh()

    def set_theme(self, theme):
        get_text = lambda p: self.app.language_manager.get(p)
        self.theme_menu.set(get_text("menu.theme.label"))
        theme = "light" if theme == get_text("menu.theme.light") else "dark"
        ctk.set_appearance_mode(theme)
        self.app.settings.set("theme", theme, auto_save=True)
        self.app.refresh()
