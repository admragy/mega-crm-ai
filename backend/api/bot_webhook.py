from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import google.generativeai as genai

app = FastAPI()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# نفس الكود بتاع البوت (start + handle_message) هنا...

application = Application.builder().token(TELEGRAM_TOKEN).build()
# أضف الهاندلرز...

@app.post(f"/webhook/{TELEGRAM_TOKEN}")
async def webhook(request: Request):
    update = Update.de_json(await request.json(), application.bot)
    await application.process_update(update)
    return {"ok": True}

@app.on_event("startup")
async def set_webhook():
    await application.bot.set_webhook(url=f"https://your-vercel-domain.vercel.app/webhook/{TELEGRAM_TOKEN}")
