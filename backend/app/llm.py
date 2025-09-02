import os
from dotenv import load_dotenv
from yandex_cloud_ml_sdk import YCloudML
from app.speech_synthesizer import YandexSpeechSynthesizer

load_dotenv()

YCloudML_FOLDER_ID = os.getenv("YCloudML_FOLDER_ID")
YCloudML_AUTH_TOKEN = os.getenv("YCloudML_AUTH_TOKEN")

sdk = YCloudML(folder_id=YCloudML_FOLDER_ID, auth=YCloudML_AUTH_TOKEN)
model = sdk.models.completions("yandexgpt-lite", model_version="rc")
model = model.configure(temperature=0.3)

def generate_llm_request(message: str):
    return {"role": "user", "text": message}

def get_llm_reply(message: str):
    llm_request = generate_llm_request(message)
    result = model.run(llm_request)

    text = "\n".join([r.text for r in result])
    
    synthesizer = YandexSpeechSynthesizer(YCloudML_AUTH_TOKEN, YCloudML_FOLDER_ID)
    audio_base64 = synthesizer.synthesize(
        text=text,
        voice="oksana",
        emotion="good",
        speed=1.0,
        # format="lpcm"
    )

    return {"text": text, "audio": audio_base64}
