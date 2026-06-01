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

class Hariko(MDApp):

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

    

    def build(self):

        self.theme_cls.theme_style_switch_animation = True

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_file("hariko.kv")

if __name__ == '__main__':
    Hariko().run()
