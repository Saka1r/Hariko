# hariko/stt.py
# author: Saka1r
# MIT License

import os
import logging
import whisper
import tools

logger = logging.getLogger(__name__)

# Кэш загруженных моделей: key = "model_device", value = модель
_model_cache = {}


def stt_run(target: str) -> str:
    """Транскрибация аудио/видео через Whisper с учётом настроек из config.json.
    
    Args:
        target: Путь к медиафайлу
        
    Returns:
        Распознанный текст
        
    Raises:
        FileNotFoundError: Если файл не найден
        RuntimeError: При ошибке загрузки модели или транскрипции
    """
    if not target or not os.path.exists(target):
        raise FileNotFoundError(f"Файл не найден: {target}")

    config = tools.get_config()
    model_name = config.get("whisper_model", "base")
    language = config.get("whisper_lang", "auto")
    device = config.get("whisper_computing_device", "cpu")

    # 1. Кэш модели (загрузка занимает время и RAM)
    cache_key = f"{model_name}_{device}"
    if cache_key not in _model_cache:
        logger.info(f"📥 Загрузка модели: {model_name} ({device})")
        _model_cache[cache_key] = whisper.load_model(model_name, device=device)

    model = _model_cache[cache_key]

    # 2. Транскрибация
    logger.info(f"🎤 Обработка: {os.path.basename(target)}")
    result = model.transcribe(
        target,
        language=language if language != "auto" else None,
        fp16=(device == "cuda")  # float16 только для CUDA
    )

    text = result["text"].strip()
    tools.write_to_file(text)
    logger.info("✅ Готово. Текст сохранён в output.txt")
    return text