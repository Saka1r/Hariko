#hariko
#author: Saka1r
#MIT License

import json

def get_config():
    with open("config/config.json", "r") as f:
        CONFIG = json.load(f)

    return CONFIG

def write_to_file(file):
    with open("output.txt", "w") as f:
        f.write(file)

    
