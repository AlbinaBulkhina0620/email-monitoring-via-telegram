import os
import requests

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")


def send_telegram_alert(message):

    url = "http://127.0.0.1:8000/send-alert"

    headers = {
        "X-API-Token": API_TOKEN
    }

    data = {
        "message": message
    }

    response = requests.post(
        url,
        json=data,
        headers=headers
    )

    print("Telegram response:", response.status_code)
    print(response.text)