import os
from dotenv import load_dotenv

load_dotenv()

YCloudML_FOLDER_ID = os.getenv("YCloudML_FOLDER_ID")
YCloudML_AUTH_TOKEN = os.getenv("YCloudML_AUTH_TOKEN")