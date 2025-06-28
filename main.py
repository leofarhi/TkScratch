import customtkinter as ctk
from modules.config import Settings
from modules.i18n import LanguageManager
from ui.app_window import ScratchApp

if __name__ == "__main__":
    settings = Settings()
    language_manager = LanguageManager()
    language_manager.load(settings.get("language"))

    app = ScratchApp(settings, language_manager)
    app.mainloop()
