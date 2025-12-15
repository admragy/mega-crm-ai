import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# قراءة التوكنات من environment (أمان للـ deploy)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    raise ValueError("حط TELEGRAM_TOKEN و GEMINI_API_KEY في environment variables!")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    'gemini-1.5-flash',  # مجاني وقوي جدًا
    system_instruction="""
أنت AI Senior Full-Stack Architect وProject Manager لمشروع CRM ضخم مفتوح المصدر.
المشروع يشمل:
- CRM كامل (Leads, Contacts, Deals, Tasks, Reports)
- أتمتة إعلانات ممولة (Facebook, Google, TikTok Ads APIs)
- شات بوت AI داخل الداشبورد
- لوحة أدمن متقدمة
- تحكم كامل عبر بوت تليجرام (أنت)

Stack: FastAPI + SQLAlchemy backend, Next.js + Tailwind frontend, PostgreSQL DB, Redis.

فكر خطوة بخطوة، رد بالعربية، استخدم Markdown، ولّد كود نظيف مع مسار الملف الكامل.
ابدأ كل رد بملخص الخطوة الحالية.
    """
)

user_histories = {}
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 **البوت الضخم جاهز دلوقتي!**\n\n"
        "أنا الـ AI Manager بتاع المشروع mega-crm-ai.\n"
        "هنبني كل حاجة خطوة بخطوة.\n\n"
        "أوامر سريعة:\n"
        "- خطة architecture كاملة\n"
        "- ولّد models الـ CRM في backend/models.py\n"
        "- اقترح roadmap للمشروع\n"
        "ابدأ دلوقتي!"
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
        await update.message.reply_text(f"خطأ: {str(e)}.\nجرب تاني أو تأكد من الـ API Key.")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 بوت الـ CRM الضخم شغال!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
