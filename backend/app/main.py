import os
from fastapi import FastAPI, APIRouter
from fastapi import File, UploadFile
from pydantic import BaseModel
from app.llm import get_llm_reply
from app.services.speech import YandexSpeechService
from app.services.processed import process_text_with_tts
from app.config import YCloudML_FOLDER_ID, YCloudML_AUTH_TOKEN

app = FastAPI()
api_router = APIRouter(prefix="/api")
speech_service = YandexSpeechService(YCloudML_AUTH_TOKEN, YCloudML_FOLDER_ID)

class LLMRequest(BaseModel):
    text: str

@api_router.post("/llm")
async def llm_endpoint(request: LLMRequest):
    return process_text_with_tts(request.text)


@api_router.post("/upload_audio")
async def upload_audio(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    input_text = speech_service.recognize_speech(audio_bytes)
    result = process_text_with_tts(input_text)
    return {**result, "input": input_text}

app.include_router(api_router)