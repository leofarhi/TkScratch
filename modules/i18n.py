import json
import os

LANG_DIR = "languages"


class LanguageManager:
    languages = {"en": "English", "fr": "Français"}
    def __init__(self):
        self.current_language = "en"
        self.translations = {}
        self.load(self.current_language)

    def load(self, lang):
        if lang not in LanguageManager.languages.keys():
            raise ValueError(f"Language '{lang}' is not supported.")
        self.current_language = lang
        lang_file = os.path.join(LANG_DIR, f"{lang}.json")
        if os.path.exists(lang_file):
            with open(lang_file, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
        else:
            self.translations = {}

    def get(self, path):
        keys = path.split(".")
        data = self.translations
        for k in keys:
            if k in data:
                data = data[k]
            else:
                return path
        return data

