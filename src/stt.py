#hariko
#author: Saka1r
# MIT License

import whisper

import tools

def stt_run(target=None):
    CONFIG = tools.get_config()
    
    model = whisper.load_model(CONFIG["whisper_model"])

    result = model.transcribe(target)

    print(result["text"])
    tools.write_to_file(result["text"])
