# src/utils.py

import json
import os

class I18nManager:
    def __init__(self, lang="en"):
        self.lang = lang
        self.strings = {}
        self.load_lang(self.lang)

    def load_lang(self, lang):
        self.lang = lang
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, "conf", f"lang.{lang}.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.strings = json.load(f)
        except Exception as e:
            print(f"Failed to load lang {lang}: {e}")

    def get(self, key):
        return self.strings.get(key, key)

global_i18n = I18nManager("en")