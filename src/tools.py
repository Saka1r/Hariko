#hariko
#author: Saka1r
#MIT License

import json

def get_config():
    with open("config/config.json", "r", encoding="utf-8") as f:
        CONFIG = json.load(f)

    return CONFIG

def write_to_file(file):
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(file)

    
