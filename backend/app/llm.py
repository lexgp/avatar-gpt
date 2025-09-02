import os
from yandex_cloud_ml_sdk import YCloudML
from app.config import YCloudML_FOLDER_ID, YCloudML_AUTH_TOKEN

sdk = YCloudML(folder_id=YCloudML_FOLDER_ID, auth=YCloudML_AUTH_TOKEN)
model = sdk.models.completions("yandexgpt-lite", model_version="rc")
model = model.configure(temperature=0.3)

def generate_llm_request(message: str):
    return {"role": "user", "text": message}

def get_llm_reply(message: str):
    """
    Отправляет запрос в Yandex GPT и возвращает текст ответа.
    message: входной текст пользователя.
    return: текст ответа от LLM.
    """
    llm_request = generate_llm_request(message)
    result = model.run(llm_request)

    return "\n".join([r.text for r in result])

