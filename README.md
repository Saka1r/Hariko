🌐 [English](README.md) | [Русский](README_RU.md)

# 🎧 Hariko

> Local media pipeline: **Audio/Video → Whisper → Text Summary → Jarvis**  
> 100% offline, zero network latency, fully configurable.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![KivyMD](https://img.shields.io/badge/KivyMD-2.0.1.dev0-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Beta-red)

---

## ✨ Features

- 🎤 **Speech-to-Text** via `openai/whisper` (models: `tiny` → `large-v3`)
- 🌍 **Language Detection** (`auto`, `ru`, `en`, etc.)
- 💻 **Hardware Acceleration** (CPU / CUDA auto-fallback)
- 📁 **Multi-format Support** (`.mp3`, `.wav`, `.mp4`, `.mkv`, `.webm`)
- ⚙️ **GUI Configuration** (theme, model size, compute device, paths)
- 🔌 **Jarvis-Ready** (exports clean text for downstream LLM processing)

---

## Quick Start

### Prerequisites
- Python 3.10–3.12
- `ffmpeg` (installed system-wide)
- NVIDIA GPU with CUDA drivers (optional, for faster inference)

### Installation
```bash
git clone https://github.com/Saka1r/hariko.git
cd hariko
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Run

```bash
python src/hariko.py
```
💡 First run requires config/config.json. See the Configuration section below.

## ⚙️ Configuration

```json
{
  "theme": "Dark",
  "gguf_path": "./models/model.Q4_K_M.gguf",
  "whisper_lang": "auto",
  "whisper_model": "base",
  "whisper_computing_device": "cpu"
}
```

| Parameter | Description | Default |
|---|---:|---|
| theme | UI theme | "Dark", "Light" |
| gguf_path | Path to GGUF LLM model (future use) | "" |
| whisper_lang | Transcription language | "auto", "ru", "en" |
| whisper_model | Whisper model size | "tiny", "base", "small", "medium", "large-v3" |
| whisper_computing_device | Compute backend | "cpu", "cuda" |

## 📁 Project Structure

``` bash
hariko/
├── src/
│   ├── hariko.py      # Main UI & app logic (KivyMD 2.0)
│   ├── stt.py         # Whisper transcription pipeline
│   └── tools.py       # Config I/O & file utilities
├── config/
│   ├── config.json    # User settings
│   └── anime.png      # App icon
├── output.txt         # Generated transcript
├── requirements.txt   # Python dependencies
└── README.md          # Documentation
```

## 🔌 Jarvis Integration

Hariko outputs clean text to `output.txt`. Jarvis can:
1. Read the file directly (`tools.get_output()`)
2. Consume via REST/WebSocket (planned)

## 📜 License
MIT License. Free to use, modify, and distribute.

## 🤝 Support

    🐞 Report bugs → Issues
    💡 Feature requests → Discussions
    🛠️ Contribute → Fork & PR

Built for local, private AI workflows.