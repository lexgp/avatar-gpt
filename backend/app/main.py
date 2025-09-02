import os
from fastapi import FastAPI, APIRouter
from fastapi import File, UploadFile, Form
from pydantic import BaseModel
from app.services.speech import YandexSpeechService
from app.services.processed import process_text_with_tts
from app.config import YCloudML_FOLDER_ID, YCloudML_AUTH_TOKEN
from typing import List

app = FastAPI()
api_router = APIRouter(prefix="/api")
speech_service = YandexSpeechService(YCloudML_AUTH_TOKEN, YCloudML_FOLDER_ID)

class LLMRequest(BaseModel):
    text: str
    history: list[str]

@api_router.post("/llm")
async def llm_endpoint(request: LLMRequest):
    # print(request.history)
    return process_text_with_tts(request.text, request.history)


@api_router.post("/upload_audio")
async def upload_audio(
        file: UploadFile = File(...),
        history: List[str] = Form(...)
    ):
    # print(history)
    audio_bytes = await file.read()
    input_text = speech_service.recognize_speech(audio_bytes)
    return process_text_with_tts(input_text, history)

app.include_router(api_router)