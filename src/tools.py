# hariko/tools.py
# author: Saka1r
# MIT License

import os
import json
import logging

logger = logging.getLogger(__name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "config.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "output.txt")


def get_config() -> dict:
    """Загружает настройки из config/config.json"""
    if not os.path.exists(CONFIG_PATH):
        logger.warning("⚠️ config.json не найден. Возвращаю пустой конфиг.")
        return {}
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        logger.error("❌ Ошибка в config.json: нарушен синтаксис JSON")
        return {}


def get_output() -> str:
    """Возвращает содержимое output.txt"""
    if not os.path.exists(OUTPUT_PATH):
        logger.warning("⚠️ output.txt не найден")
        return ""
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        return f.read()


def write_to_file(text: str) -> None:
    """Записывает текст в output.txt"""
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(text)

    
