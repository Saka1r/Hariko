#    _   _            _ _         
#   | | | |          (_) |        
#   | |_| | __ _ _ __ _| | _____  
#   |  _  |/ _` | '__| | |/ / _ \ 
#   | | | | (_| | |  | |   < (_) |
#   \_| |_/\__,_|_|  |_|_|\_\___/ 

# Author / Saka1r
# MIT License 

from kivymd.app import MDApp
from kivy.lang.builder import Builder

from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivy.core.window import Window

import json 

Window.size = (500, 700)

class Hariko(MDApp):

    def config_to_settings(self):
        if self.theme_cls.theme_style == "Light":
            self.root.ids.theme_checkbox_widget.active = True
        else:
            self.root.ids.theme_checkbox_widget.active = False
        self.root.ids.gguf_path_widget.text = self.gguf_path
        self.root.ids.wp_lang_widget.text = self.wp_lang
        self.root.ids.wp_model_widget.text = self.wp_model
        self.root.ids.wp_cd_widget.text = self.wp_cd

    def upload_config(self):
        with open("config/config.json", "r") as f:
            CONFIG = json.load(f)

        self.theme_cls.theme_style = CONFIG["theme"]
        self.gguf_path = CONFIG["gguf_path"]
        self.wp_lang = CONFIG["whisper_lang"]
        self.wp_model = CONFIG["whisper_model"]
        self.wp_cd = CONFIG["whisper_computing_device"]

        self.config_to_settings()

    def update_config(self):

        self.gguf_path = self.root.ids.gguf_path_widget.text
        self.wp_lang = self.root.ids.wp_lang_widget.text
        self.wp_model = self.root.ids.wp_model_widget.text
        self.wp_cd = self.root.ids.wp_cd_widget.text

        CONFIG = {"theme": self.theme_cls.theme_style, "gguf_path": self.gguf_path, 
                  "whisper_lang": self.wp_lang, "whisper_model": self.wp_model,
                  "whisper_computing_device": self.wp_cd}

        with open("config/config.json", "w") as f:
            json.dump(CONFIG, f, indent=4, ensure_ascii=False)    

    def on_switch_tabs(
        self,
        bar: MDNavigationBar,
        item: MDNavigationItem,
        item_icon: str,
        item_text: str,
    ):
        self.root.ids.screen_manager.current = item_text

    def switch_theme(self, active):
        if active:
            self.theme_cls.theme_style = "Light"
        else:
            self.theme_cls.theme_style = "Dark"

    def on_start(self):
        self.upload_config()

    def build(self):
        self.icon = "config/anime.png"
        self.theme_cls.theme_style_switch_animation = True

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_file("hariko.kv")

if __name__ == '__main__':
    Hariko().run()
