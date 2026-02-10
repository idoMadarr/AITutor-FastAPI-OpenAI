from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from typing import List
import logging
import os
import uuid

logger = logging.getLogger("uvicorn")
app = FastAPI()
load_dotenv()

client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))
MODEL = os.getenv("LLM")
TTS_MODEL = os.getenv("TTS_MODEL")
BASE_URL = os.getenv("SERVER")
AUDIO_DIR = "audio"

os.makedirs(AUDIO_DIR, exist_ok=True)
app.mount("/audio", StaticFiles(directory="audio"), name="audio")

system_message = """
    You are a friendly, patient, and encouraging English teacher.
    
    Help the student practice English in a natural, relaxed, and supportive way.
    Use simple explanations, real-life examples, and everyday conversations.
    
    Gently correct mistakes by:
        - Rewriting the sentence correctly
        - Briefly explaining the correction in simple terms
        
    Adapt your language to the student's level.
    Encourage the student to continue speaking and ask follow-up questions when appropriate.
    Avoid long grammar lectures unless the student asks for them.
    """

class ChatRequest(BaseModel):
    message: str
    history: List[dict] = []

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat")
async def chat(payload: ChatRequest):
    message = payload.message
    history = payload.history

    messages = (
        [{"role": "system", "content": system_message}]
        + history
        + [{"role": "user", "content": message}]
    )

    # LLM
    text_response = client.responses.create(model=MODEL, input=messages, temperature=0.8)
    raw_text = text_response.output_text

    # TTS Model
    audio_response = client.audio.speech.create(model=TTS_MODEL, voice="marin", response_format="mp3", input=raw_text)

    # Save audio to file
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(AUDIO_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(audio_response.read())

    return {
        "agent_text_message": raw_text,
        "agent_audio_message": f"/{AUDIO_DIR}/{filename}",
        "format": "mp3"
    }

@app.get("/awake_server")
async def awaken_server():
    return True

@app.delete("/clear_audio")
async def clear_audio():
    delete_files = 0

    for filename in os.listdir(AUDIO_DIR):
        file_path = os.path.join(AUDIO_DIR, filename)

        if os.path.isfile(file_path):
            os.remove(file_path)
            delete_files += 1

    return {
        "status": "ok",
        "delete_files": delete_files,
    }