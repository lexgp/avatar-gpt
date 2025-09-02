import requests
import base64
import requests
from datetime import datetime


class YandexSpeechService:
    """Сервис работы с Yandex SpeechKit: синтез речи и распознавание аудио."""

    TTS_URL = "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize"
    STT_URL = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize"

    def __init__(self, api_key: str, folder_id: str):
        self.api_key = api_key
        self.folder_id = folder_id
        self.headers = {
            "Authorization": f"Api-Key {api_key}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def recognize_speech(self, audio_bytes: bytes) -> str:
        """
        Преобразует аудио в текст с помощью Yandex STT.
        audio_bytes: содержимое файла в памяти.
        return: распознанный текст.
        """
        params = {"folderId": self.folder_id, "lang": "ru-RU"}

        response = requests.post(
            self.STT_URL,
            headers=self.headers,
            params=params,
            data=audio_bytes,
        )

        if response.status_code != 200:
            raise Exception(f"STT failed: {response.text}")

        result = response.json()
        return result.get("result", "")

    def synthesize(
        self,
        text: str,
        voice: str = "oksana",
        emotion: str = "good",
        speed: float = 1.0,
        format: str = "oggopus",
        return_type: str = "base64",
    ) -> str:
        """
        Синтезирует речь из текста.
        return_type:
          - "base64": возвращает строку base64.
          - "file": сохраняет файл на диск и возвращает путь.
        """
        data = {
            "text": text,
            "voice": voice,
            "emotion": emotion,
            "speed": str(speed),
            "format": format,
            "folderId": self.folder_id,
            "lang": "ru-RU",
        }

        response = requests.post(self.TTS_URL, headers=self.headers, data=data)

        if response.status_code != 200:
            print(f"Ошибка синтеза: {response.status_code} - {response.text}")
            return None

        if return_type == "base64":
            return base64.b64encode(response.content).decode("utf-8")
        else:
            from datetime import datetime
            filename = f"speech_{datetime.now():%Y%m%d_%H%M%S}.ogg"
            with open(filename, "wb") as f:
                f.write(response.content)
            return filename