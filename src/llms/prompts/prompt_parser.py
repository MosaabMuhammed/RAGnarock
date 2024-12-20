import os

class PromptParser:
    def __init__(self, lang: str=None, default_lang: str="en"):
        self.default_lang = default_lang
        self.lang = lang or self.default_lang
        self.current_path = os.path.direname(os.path.abspath(__file__))

    def set_lang(self, lang: str):
        if not lang:
            return None
        
        lang_path = os.path.join(self.current_path, "locales", lang)
        if os.path.exists(lang_path):
            self.lang = lang
        else:
            self.lang = self.default_lang

    def get(self, group: str, key: str, vars: dict={}):
        if not group or not key:
            return None

        group_path = os.path.join(self.current_path, "locales", self.lang, f"{group}.json")
        if not os.path.exists(group_path):
            group_path = os.path.join(self.current_path, "locales", self.default_lang, f"{group}.json")
            self.lang = self.default_lang

        if not os.path.exists(group_path):
            return None
        
        module = __import__(f"llms.prompts.locales.{self.lang}.{group}", fromlist=[group])

        if not module:
            return None
        
        key_attr = getattr(module, key, None)
        return key_attr.substitute(vars) if key_attr else None
