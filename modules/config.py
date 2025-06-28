import json
import os

SETTINGS_FILE = "settings.json"
DEFAULT_SETTINGS = {"language": "en", "theme": "light"}
class Settings:
    def __init__(self):
        self.data = {}
        self.load()

    def get(self, key, default=None):
        return self.data.get(key, default)
    
    def set(self, key, value, auto_save=True):
        self.data[key] = value
        if auto_save:
            self.save()

    def load(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        else:
            self.data = DEFAULT_SETTINGS.copy()

    def save(self):
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
