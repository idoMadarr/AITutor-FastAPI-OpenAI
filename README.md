uv run uvicorn main:app --host 0.0.0.0 --port 8000

# English Tutor API (FastAPI + OpenAI)

A lightweight **FastAPI backend** that powers an AI English tutor.
It accepts chat messages, keeps short conversation history, generates a text response using an LLM, converts that response to **speech (TTS)**, and serves the generated audio files via a static endpoint.

---

## Features

* 🧠 LLM-powered English tutor (friendly, patient, corrective)
* 🔊 Text-to-Speech (MP3 output)
* 💬 Conversation history support
* 📁 Static audio file hosting
* 🧹 Endpoint to clean up generated audio files

---

## Tech Stack

* **FastAPI** – API framework
* **OpenAI API** – LLM + TTS
* **Pydantic** – request validation
* **Python 3.10+**

---

## Project Structure

```
.
├── main.py            # FastAPI app
├── audio/             # Generated MP3 files (auto-created)
├── .env               # Environment variables
└── README.md
```

---

## Environment Variables

Create a `.env` file in the root directory:

```env
OPEN_AI_KEY=your_openai_api_key
LLM=gpt-4o-mini
TTS_MODEL=gpt-4o-mini-tts
SERVER=http://127.0.0.1:8000
```

### Notes

* `LLM` – model used for text generation
* `TTS_MODEL` – model used for text-to-speech

---

## Installation

```bash
uv sync --frozen && uv cache prune --ci
```

---

## Running the Server

```bash
uv run uvicorn main:app --host 0.0.0.0 --port $PORT
```

Server will be available at:

```
http://127.0.0.1:8000
```