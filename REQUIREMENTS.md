# LUMI AI Assistant — Full Requirements & Architecture

> **Project Name:** LUMI (formerly JARVIS)  
> **Platform:** Windows 10/11  
> **Language:** Python 3.11  
> **Author:** Joel M  

---

## 📁 Project Structure

```
Project_JARVIS-main/
├── main.py                  # Entry point — starts LUMI
├── .env                     # API keys & configuration
├── requirements.txt         # Python dependencies
├── video_system.py          # Standalone YOLO vision system
├── gemini_client.py         # Gemini Live multimodal client
├── contacts.json            # WhatsApp contacts (optional)
│
├── core/                    # 🧠 BACKEND — Core engine
│   ├── engine.py            # LLM brain (Groq API + tool calling)
│   ├── registry.py          # Dynamic skill loader
│   ├── skill.py             # Abstract base class for skills
│   └── voice.py             # Speech-to-Text & Text-to-Speech
│
├── gui/                     # 🖥️ FRONTEND — HUD Interface
│   ├── __init__.py
│   └── app.py               # PyQt6 Arc Reactor GUI
│
├── skills/                  # ⚡ BACKEND — Modular skill plugins
│   ├── camera_skill.py      # Webcam photo capture
│   ├── datetime_ops.py      # Date & time queries
│   ├── detection_skill.py   # YOLOv8 object detection
│   ├── email_ops.py         # Email checking (IMAP)
│   ├── file_ops.py          # File read/write/list (full system)
│   ├── gemini_live_skill.py # Gemini Live multimodal launcher
│   ├── memory_ops.py        # Persistent memory (JSON storage)
│   ├── screenshot_ops.py    # Screen capture
│   ├── system_ops.py        # System control (volume, apps, commands, power)
│   ├── text_ops.py          # File reading & summarization
│   ├── vision_skill.py      # Live YOLO vision launcher
│   ├── weather_ops.py       # Weather via OpenWeatherMap API
│   ├── web_ops.py           # Google search
│   ├── whatsapp_skill.py    # WhatsApp messaging
│   └── whatsapp/
│       ├── driver.py        # Chrome WebDriver (Selenium)
│       └── whatsapp_client.py # WhatsApp Web automation
│
└── assets/                  # Stored photos, detections, etc.
```

---

## 🖥️ FRONTEND (GUI)

### Technology: **PyQt6**

The frontend is a single-window **HUD (Heads-Up Display)** inspired by Iron Man's Arc Reactor interface.

| Component | File | Description |
|-----------|------|-------------|
| **HexagonPanel** | `gui/app.py` | Left panel — animated hexagonal grid background |
| **CentralReactor** | `gui/app.py` | Center — animated Arc Reactor core that pulses. Turns **orange** when paused, **cyan** when active |
| **TelemetryPanel** | `gui/app.py` | Right panel — animated vertical bar visualizer |
| **Window** | `gui/app.py` | Frameless, translucent black window, always on top |

### Frontend Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `PyQt6` | ≥ 6.6.0 | GUI framework — widgets, painting, animations |

### Frontend Interactions

| Action | What Happens |
|--------|-------------|
| **Click anywhere** | Toggles PAUSE/RESUME (reactor turns orange/cyan) |
| **Press ESC** | Closes the HUD and shuts down LUMI |
| **Visual feedback** | Reactor pulses when listening, static when paused |

---

## 🧠 BACKEND (Core Engine)

### Technology: **Python + Groq API (LLaMA 3.1-8B)**

The backend handles all intelligence — voice I/O, LLM reasoning, tool execution, and skill management.

### Core Components

| Component | File | Description |
|-----------|------|-------------|
| **LumiEngine** | `core/engine.py` | The brain — sends user queries to Groq LLM, handles tool-calling responses, executes skills |
| **SkillRegistry** | `core/registry.py` | Dynamically discovers and loads all skills from `skills/` directory at startup |
| **Skill (ABC)** | `core/skill.py` | Abstract base class — all skills must implement `get_tools()` and `get_functions()` |
| **Voice I/O** | `core/voice.py` | `speak()` = Text-to-Speech (pyttsx3), `listen()` = Speech-to-Text (Google Speech Recognition) |
| **Main Loop** | `main.py` | Orchestrates everything — loads skills, starts voice loop in background thread, launches GUI |

### Backend Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `groq` | ≥ 0.4.2 | Groq API client — sends prompts to LLaMA 3.1-8B-instant LLM |
| `python-dotenv` | ≥ 1.0.0 | Loads `.env` file for API keys |
| `pyttsx3` | ≥ 2.90 | Text-to-Speech engine (Windows SAPI5) |
| `SpeechRecognition` | ≥ 3.8.1 | Speech-to-Text (Google Speech Recognition API) |
| `PyAudio` | ≥ 0.2.11 | Microphone access for voice input |
| `requests` | ≥ 2.31.0 | HTTP requests (weather API, web services) |
| `opencv-python` | latest | Camera access, image capture, video processing |
| `Pillow` | ≥ 10.0.0 | Screenshot capture (ImageGrab), image processing |
| `pycaw` | ≥ 20240210 | Windows audio/volume control |
| `comtypes` | ≥ 1.2.0 | Windows COM interface (required by pycaw) |
| `selenium` | latest | Browser automation (WhatsApp Web) |
| `webdriver-manager` | latest | Auto-downloads Chrome WebDriver |

### Optional Heavy Dependencies (not installed by default)

| Package | Purpose |
|---------|---------|
| `ultralytics` | YOLOv8 object detection model |
| `torch` + `torchvision` | PyTorch ML framework (GPU acceleration) |

---

## ⚡ SKILLS (Modular Plugins)

Each skill is a self-contained Python file that registers tools with the LLM.

### Skill Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  User Voice  │────▶│  LumiEngine  │────▶│  Groq LLM   │
│  "take photo"│     │  (engine.py) │     │  (Cloud AI)  │
└─────────────┘     └──────┬───────┘     └──────┬──────┘
                           │                     │
                           │  ◀── tool_call ─────┘
                           │  "take_photo()"
                           ▼
                    ┌──────────────┐
                    │ SkillRegistry│
                    │ (registry.py)│
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ CameraSkill  │──▶ Opens webcam, captures photo
                    │ (camera.py)  │──▶ Saves to Desktop folder
                    └──────────────┘
```

### All Available Skills

| # | Skill | File | Tools Provided | What It Does |
|---|-------|------|----------------|-------------|
| 1 | **Camera** | `camera_skill.py` | `take_photo` | Captures photo via webcam with voice countdown "1, 2, 3, Cheese!" Saves to `Desktop/camera photo by lumi/` |
| 2 | **Date/Time** | `datetime_ops.py` | `get_current_datetime`, `get_current_time`, `get_current_date` | Returns current date and time |
| 3 | **Object Detection** | `detection_skill.py` | `detect_objects` | Uses YOLOv8 to detect objects via camera (requires ultralytics) |
| 4 | **Email** | `email_ops.py` | `check_unread_emails`, `get_recent_emails` | Checks email inbox via IMAP |
| 5 | **File Manager** | `file_ops.py` | `manage_file`, `list_directory` | Read/write/create/append any file, list any folder on the system |
| 6 | **Gemini Live** | `gemini_live_skill.py` | `start_live_vision` | Launches real-time multimodal Gemini conversation (audio + video) |
| 7 | **Memory** | `memory_ops.py` | `remember_fact`, `retrieve_memory`, `list_all_memories`, `forget_fact` | Persistent memory across sessions (JSON file) |
| 8 | **Screenshot** | `screenshot_ops.py` | `take_screenshot` | Captures full screen, saves to `Desktop/screenshot by lumi/` |
| 9 | **System Control** | `system_ops.py` | `set_volume`, `open_app`, `run_system_command`, `get_system_info`, `control_power` | Full Windows system access — volume, apps, PowerShell commands, shutdown/restart/sleep/lock |
| 10 | **Text/Summary** | `text_ops.py` | `read_file_content`, `summarize_file` | Reads files and generates AI summaries |
| 11 | **Live Vision** | `vision_skill.py` | `start_live_vision` | Launches real-time YOLO object detection window |
| 12 | **Weather** | `weather_ops.py` | `get_weather`, `get_current_location_weather` | Weather info via OpenWeatherMap API |
| 13 | **Web Search** | `web_ops.py` | `google_search` | Opens Google search in browser |
| 14 | **WhatsApp** | `whatsapp_skill.py` | `send_whatsapp_message` | Sends WhatsApp messages via browser automation |

---

## 🔑 API Keys & Configuration (.env)

| Variable | Required | Source | Purpose |
|----------|----------|--------|---------|
| `GROQ_API_KEY` | ✅ **Yes** | [console.groq.com](https://console.groq.com/) | LLM brain — powers all AI responses |
| `OPENWEATHERMAP_API_KEY` | ❌ Optional | [openweathermap.org](https://openweathermap.org/api) | Weather skill |
| `DEFAULT_CITY` | ❌ Optional | User config | Default city for weather |
| `EMAIL_ADDRESS` | ❌ Optional | User's email | Email checking skill |
| `EMAIL_PASSWORD` | ❌ Optional | App password | Email authentication |
| `EMAIL_IMAP_SERVER` | ❌ Optional | e.g. `imap.gmail.com` | Email server |

---

## 🚀 How to Run

### Prerequisites
- **Python 3.11** (required — Python 3.14 doesn't support PyAudio)
- **Windows 10/11**
- **Microphone** (for voice input)
- **Speakers** (for voice output)
- **Webcam** (for camera/detection skills)

### Installation & Setup

```bash
# 1. Create virtual environment with Python 3.11
py -3.11 -m venv venv

# 2. Activate it
.\venv\Scripts\activate

# 3. Install dependencies
pip install groq python-dotenv requests pyttsx3 SpeechRecognition PyAudio PyQt6 Pillow opencv-python pycaw comtypes selenium webdriver-manager

# 4. Add your API key to .env file
# Edit .env and set GROQ_API_KEY=gsk_your_key_here

# 5. Run LUMI with GUI + Voice
python main.py

# 6. Or run in text-only mode (no mic needed)
python main.py --text
```

### Run Modes

| Mode | Command | Description |
|------|---------|-------------|
| **Full Mode** | `python main.py` | GUI HUD + Voice input/output |
| **Text Mode** | `python main.py --text` | Terminal only, type commands |

---

## 🔄 Data Flow (How LUMI Works)

```
┌──────────┐    ┌───────────┐    ┌───────────┐    ┌──────────┐
│ 🎤 Mic   │───▶│ listen()  │───▶│ Google    │───▶│ Text     │
│ (PyAudio)│    │ (voice.py)│    │ Speech API│    │ Query    │
└──────────┘    └───────────┘    └───────────┘    └────┬─────┘
                                                       │
                                                       ▼
┌──────────┐    ┌───────────┐    ┌───────────┐    ┌──────────┐
│ 🔊 Speak │◀───│ speak()   │◀───│ LumiEngine│◀───│ Groq API │
│ (pyttsx3)│    │ (voice.py)│    │(engine.py)│    │ LLaMA 8B │
└──────────┘    └───────────┘    └─────┬─────┘    └──────────┘
                                       │
                                       ▼ (if tool_call)
                                ┌──────────────┐
                                │ SkillRegistry│───▶ Execute skill function
                                │              │◀─── Return result
                                └──────────────┘───▶ Send result back to LLM
                                                     for final spoken response
```

---

## 📊 Frontend vs Backend Summary

| Aspect | Frontend (GUI) | Backend (Core + Skills) |
|--------|---------------|------------------------|
| **Technology** | PyQt6 | Python + Groq API |
| **Files** | `gui/app.py` | `core/`, `skills/`, `main.py` |
| **Purpose** | Visual HUD display | Voice I/O, AI reasoning, task execution |
| **Runs on** | Main thread | Background thread |
| **User interaction** | Click to pause/resume, ESC to quit | Voice commands or text input |
| **Dependencies** | PyQt6 (1 package) | 12+ packages |
| **Can run without** | Yes (use `--text` mode) | No — this IS the core logic |

---

## 📝 Save Locations

| Type | Path |
|------|------|
| Camera photos | `C:\Users\joelm\OneDrive\Desktop\camera photo by lumi\` |
| Screenshots | `C:\Users\joelm\OneDrive\Desktop\screenshot by lumi\` |
| Memory file | `~/.jarvic_memory.json` |
| Detection images | `assets/` folder in project directory |

---

*Last updated: February 23, 2026*
