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

class Hariko(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        return Builder.load_file("hariko.kv")

if __name__ == '__main__':
    Hariko().run()
