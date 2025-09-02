import os
from yandex_cloud_ml_sdk import YCloudML
from app.config import YCloudML_FOLDER_ID, YCloudML_AUTH_TOKEN

sdk = YCloudML(folder_id=YCloudML_FOLDER_ID, auth=YCloudML_AUTH_TOKEN)
model = sdk.models.completions("yandexgpt-lite", model_version="rc")
model = model.configure(temperature=0.3)

def generate_llm_request(message: str, history: list[str]):
    
    history_str = '\n'.join(history)
    history_message = f'''Вот история нашего разговора до этого момента: {history_str}''' if len(history) else ''

    request_message = f'''
    Представь что ты голосовой ассистент системы знаний (RAG).
    Что за система: внутренний документооборот в банке.
    Можешь придумывать ответы, если я спрашиваю что-то конкретное.
    Ты пока только тестовая система.
    Типа Красной королевы из resident evil.
    Мы с тобой разговариваем в диалоге.
    {history_message}
    Сейчас ответь на моё последнее сообщение: {message}
    '''
    return {"role": "user", "text": request_message}

def get_llm_reply(message: str, history: list[str]):
    """
    Отправляет запрос в Yandex GPT и возвращает текст ответа.
    message: входной текст пользователя.
    return: текст ответа от LLM.
    """
    llm_request = generate_llm_request(message, history)
    result = model.run(llm_request)

    return "\n".join([r.text for r in result])

