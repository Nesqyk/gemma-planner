## Gemma Planner: Local Voice-Driven AI Calendar Assistant

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![pyttsx3](https://img.shields.io/pypi/v/pyttsx3)
![Whisper](https://img.shields.io/pypi/v/openai-whisper)
![Transformers](https://img.shields.io/pypi/v/transformers)

---

### What is this project?
Gemma Planner is a local, privacy-focused AI assistant that lets you schedule calendar events using your voice. It leverages:
- **Google's FunctionGemma LLM** (runs locally via HuggingFace Transformers)
- **OpenAI Whisper** for speech-to-text
- **pyttsx3** for speech synthesis
- **ics** for calendar event creation

No cloud APIs required—everything runs on your machine.

---

### Setup Instructions
1. **Clone the repository:**
	```bash
	git clone https://github.com/Nesqyk/gemma-planner.git
	cd gemma-planner
	```
2. **Install dependencies:**
	```bash
	pip install -r requirements.txt
	```
3. **Install ffmpeg** (required for Whisper):
	- On Ubuntu: `sudo apt install ffmpeg`
	- On Windows: [Download from ffmpeg.org](https://ffmpeg.org/download.html)
4. **Run the assistant:**
	```bash
	python main.py
	```

---

### How it works
1. The assistant greets you and waits for your voice input.
2. Your speech is transcribed to text using Whisper.
3. The LLM interprets your intent and, if needed, triggers a function call (e.g., to schedule an event).
4. If scheduling, the assistant creates a `.ics` calendar file and opens it for you.
5. The assistant responds to you via speech (pyttsx3).

Say "exit" or "quit" to stop the assistant.

---

### Architecture

```
User (voice)
	↓
[voice_engine.py]  ←→  [main.py]  ←→  [calendar_tool.py]
	↓                  |   |             |
pyttsx3 (TTS)         |   |             |-- ics (calendar)
Whisper (STT)         |   |-- HuggingFace Transformers (Gemma LLM)
```

- **main.py**: Orchestrates the agent, LLM, and function calls.
- **voice_engine.py**: Handles speech input (Whisper) and output (pyttsx3).
- **calendar_tool.py**: Creates and opens calendar events as `.ics` files.

---

**Local-first, private, and extensible.**