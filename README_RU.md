🌐 [English](README.md) | [Русский](README_RU.md)

# 🎧 Hariko

> Локальный пайплайн: **Аудио/Видео → Whisper → Текстовый конспект → Jarvis**  
> Полная приватность, нулевая задержка сети, гибкая настройка.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![KivyMD](https://img.shields.io/badge/KivyMD-2.0.1.dev0-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Beta-red)

---

## ✨ Возможности

- 🎤 **Распознавание речи** через `openai/whisper` (модели: `tiny` → `large-v3`)
- 🌍 **Автоопределение языка** (`auto`, `ru`, `en` и др.)
- 💻 **Аппаратное ускорение** (CPU / CUDA с автоматическим фоллбэком)
- 📁 **Поддержка форматов** (`.mp3`, `.wav`, `.mp4`, `.mkv`, `.webm`)
- ⚙️ **GUI-настройки** (тема, размер модели, устройство вычислений, пути)
- 🔌 **Готовность к Jarvis** (экспорт чистого текста для дальнейшей LLM-обработки)

---

## 🚀 Быстрый старт

### Требования
- Python 3.10–3.12
- `ffmpeg` (установлен в системе)
- Видеокарта NVIDIA с драйверами CUDA (опционально, для ускорения)

### Установка
```bash
git clone https://github.com/Saka1r/hariko.git
cd hariko
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate для Windows
pip install -r requirements.txt
```
### Запуск

```bash
python src/hariko.py
```
💡 При первом запуске необходим файл config/config.json. См. раздел Конфигурация.

## ⚙️ Конфигурация

Файл: config/config.json

```json
{
  "theme": "Dark",
  "gguf_path": "./models/model.Q4_K_M.gguf",
  "whisper_lang": "auto",
  "whisper_model": "base",
  "whisper_computing_device": "cpu"
}
```

| Параметр | Описание | По умолчанию |
|---|---:|---|
| theme | Тема интерфейса | "Dark", "Light" |
| gguf_path | Путь к GGUF-модели LLM (на будущее) | "" |
| whisper_lang | Язык транскрипции | "auto", "ru", "en" |
| whisper_model | Размер модели Whisper | "tiny", "base", "small", "medium", "large-v3" |
| whisper_computing_device | Устройство вычислений | "cpu", "cuda" |

## 📁 Структура проекта

```bash
hariko/
├── src/
│   ├── hariko.py      # Основной UI и логика приложения (KivyMD 2.0)
│   ├── stt.py         # Пайплайн транскрипции (Whisper)
│   └── tools.py       # Утилиты: конфиг, чтение/запись файлов
├── config/
│   ├── config.json    # Пользовательские настройки
│   └── anime.png      # Иконка приложения
├── output.txt         # Результат транскрипции
├── requirements.txt   # Зависимости Python
└── README_RU.md       # Документация (RU)
```

## 🔌 Интеграция с Jarvis
Hariko сохраняет результат в output.txt. Jarvis может:
1. Читать файл напрямую (tools.get_output())
2. Получать данные по REST/WebSocket (в планах)

## 📜 Лицензия
MIT License. Свободное использование, модификация и распространение.

## 🤝 Поддержка

    🐞 Баги → Issues
    💡 Идеи → Discussions
    🛠️ Участие → Fork & Pull Request

Создано для локальных и приватных ИИ-пайплайнов.