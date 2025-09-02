from app.services.speech import YandexSpeechService
from app.llm import get_llm_reply
from app.config import YCloudML_FOLDER_ID, YCloudML_AUTH_TOKEN

speech_service = YandexSpeechService(YCloudML_AUTH_TOKEN, YCloudML_FOLDER_ID)

def process_text_with_tts(input_text: str):
    """Запрос к LLM и озвучивание ответа."""
    reply_text = get_llm_reply(input_text)
    audio_base64 = speech_service.synthesize(
        text=reply_text,
        voice="oksana",
        emotion="good",
        speed=1.0,
    )
    return {"text": reply_text, "audio": audio_base64}