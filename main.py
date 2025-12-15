import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# ================== قراءة من environment (أمان) ==================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    raise ValueError("حط TELEGRAM_TOKEN و GEMINI_API_KEY في الـ environment variables!")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction="""
أنت AI Senior Project Manager لبناء مشروع CRM ضخم مفتوح المصدر على GitHub.
المشروع: CRM كامل + أتمتة إعلانات ممولة + شات بوت AI داخل الداشبورد + لوحة أدمن.
Stack: FastAPI backend, Next.js frontend, PostgreSQL.
فكر خطوة بخطوة، رد بالعربية، Markdown، كود نظيف مع مسارات.
    """
)

user_histories = {}
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 البوت جاهز على أي منصة دلوقتي!\n"
        "هنبني الـ CRM الضخم مع Gemini مجاني.\n"
        "ابدأ: خطة architecture، أو ولّد models..."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_text = update.message.text

    if user_id not in user_histories:
        user_histories[user_id] = []

    user_histories[user_id].append({"role": "user", "parts": [user_text]})

    try:
        chat = model.start_chat(history=user_histories[user_id])
        response = chat.send_message(user_text)
        ai_reply = response.text

        user_histories[user_id].append({"role": "model", "parts": [ai_reply]})

        await update.message.reply_text(ai_reply, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"خطأ: {str(e)}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 البوت شغال على المنصة!")
    app.run_polling()  # polling لـ Render/Fly، أو غيّره لـ webhook لـ Vercel

if __name__ == "__main__":
    main()
