import os
from dotenv import load_dotenv
from telegram import Bot
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DEFAULT_USER_ID = int(os.getenv("DEFAULT_TELEGRAM_USER_ID"))
API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=BOT_TOKEN)
app = FastAPI(title="Telegram Alert Service")

class AlertRequest(BaseModel):
    message: str

@app.post("/send-alert")
async def send_alert(
    alert: AlertRequest,
    x_api_token: str = Header(..., alias="X-API-Token")
):
    if x_api_token != API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid API token")

    chat_id = DEFAULT_USER_ID

    try:
        await bot.send_message(chat_id=chat_id, text=alert.message)
        return {"status": "sent", "chat_id": chat_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}