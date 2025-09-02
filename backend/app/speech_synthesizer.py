import requests
import json
import os
import base64
import requests
from datetime import datetime


class YandexSpeechSynthesizer:
    def __init__(self, api_key, folder_id):
        self.api_key = api_key
        self.folder_id = folder_id
        self.url = "https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize"
        self.headers = {
            "Authorization": f"Api-Key {api_key}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
    
    def synthesize(self, text, voice="oksana", emotion="good", speed=1.0, format="oggopus", return_type="base64"):
        """
        Синтезирует речь из текста
        Возвращает путь к созданному аудиофайлу
        return_type: "base64" - возвращает base64 строку, "file" - сохраняет файл и возвращает путь
        """
        data = {
            "text": text,
            "voice": voice,
            "emotion": emotion,
            "speed": str(speed),
            "format": format,
            "folderId": self.folder_id,
            "lang": "ru-RU"
        }
        
        try:
            response = requests.post(self.url, headers=self.headers, data=data)
            
            if response.status_code == 200:
                if return_type == "base64":
                    # Конвертируем в base64
                    audio_base64 = base64.b64encode(response.content).decode('utf-8')
                    print("Аудио успешно преобразовано в base64")
                    return audio_base64
                else:
                    # Сохраняем в файл
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"speech_{timestamp}.ogg"
                    
                    with open(filename, "wb") as f:
                        f.write(response.content)
                    
                    print(f"Аудио сохранено как: {filename}")
                    return filename
            else:
                print(f"Ошибка синтеза: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Ошибка при синтезе речи: {e}")
            return None
