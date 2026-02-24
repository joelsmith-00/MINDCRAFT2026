# 🏗️ LUMI Professional Architecture: Layered Blueprint

This directory represents the **Ultra-Clean Professional Structure** for Project LUMI. Every file has been moved and linked to its new home to ensure modularity and high performance.

---

## 🎨 1. Presentation Layer (`app/`)
*The "Skin" and "Voice" of LUMI.*

- **`gui/`**:
  - `app.py`: The primary HUD and Central Reactor interface.
  - `wave_ui.py`: Real-time audio ripple visualizer.
- **`voice_mode/`**:
  - `Activate_Voice_Mode.bat`: Shortcut for hands-free assistant mode.
  - `Start_Lumi_Listener.bat`: Background wake-word detection script.

---

## 🧠 2. Brain Layer (`core/`)
*The "Central Nervous System".*

- `engine.py`: Logic orchestrator that processes prompts via Groq AI.
- `voice.py`: Speech-to-Text (STT) and Text-to-Speech (TTS) drivers.
- `registry.py`: Dynamic skill loader that finds tools across all folders.
- `skill.py`: Base DNA for all assistant tools.
- `memory.py`: Persistent JSON-based user memory storage.

---

## 💪 3. Capability Layer (`features/`)
*The "Muscles" — categorized skills.*

- **`automation/`**: `whatsapp.py`, `email.py`, `n8n.py`.
- **`system/`**: `system_ops.py`, `file_ops.py`, `screenshot.py`, `camera.py`.
- **`ai/`**: `vision.py`, `detection.py`, `gemini_live.py`, `text_summary.py` + `yolov8n.pt`.
- **`utilities/`**: `datetime.py`, `weather.py`.

---

## 🌐 4. Integration Layer (`integrations/`)
*The Bridge to External Worlds.*

- **`llm/`**: `groq_client.py`, `gemini_client.py`, `openrouter_client.py`.
- **`n8n/`**: All tools for testing the Cloud Workflow bridge.
- **`diagnostics/`**: `verify_engine.py`, `verify_skills.py`, `verify_voice.py`.

---

## 🗂 5. Resource Layer (`assets/`)
*Static Assets and User Data.*

- **`images/`**: Logos and UI assets (e.g., `arc_reactor.png`).
- **`storage/`**:
  - `screenshots/` & `camera_photos/`: User-generated media.
  - `contacts.json`: WhatsApp data.
  - `memory.json`: AI learned facts.
  - `learn.txt` & `incomplete.txt`: System logs.

---

*LUMI Workflow Structure: Verified February 24, 2026*
