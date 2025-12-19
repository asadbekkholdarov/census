import os
import json
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
from telegram.constants import ChatAction

from translit import (
    is_latin,
    is_cyrillic,
    latin_to_cyr,
    cyr_to_latin,
)

# =======================
# ENV
# =======================
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY .env faylida yo‘q")

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN .env faylida yo‘q")

# =======================
# GEMINI
# =======================
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# =======================
# DATA
# =======================
with open("data.json", "r", encoding="utf-8") as f:
    DATA = json.load(f)

CONTEXT = "\n".join(
    [
        f"{i+1}. SAVOL: {x['question']} | JAVOB: {x['answer']}"
        for i, x in enumerate(DATA)
    ]
)

# =======================
# AI ANSWER
# =======================
def find_answer(user_question: str) -> str:
    prompt = f"""
Sen professional AI assistantsan.

VAZIFA:
- Foydalanuvchi savolining MAZMUNINI tahlil qil
- Quyidagi savol-javoblardan ENG MOSINI tanla
- FAQAT o‘sha savolning JAVOBINI qaytar
- Agar mos savol topilmasa:
  "☹️ Afsuski, bu savolingizga menda javob topilmadi.
   📞 Call-markazga murojaat qiling. +998 (71) 202-8175"

Foydalanuvchi savoli:
{user_question}

SAVOL-JAVOBLAR:
{CONTEXT}

Faqat JAVOBNI yoz. Izoh yo‘q.
"""
    response = model.generate_content(prompt)
    return response.text.strip()

# =======================
# TYPING LOOP
# =======================
async def typing_action(bot, chat_id, stop_event: asyncio.Event):
    while not stop_event.is_set():
        await bot.send_chat_action(
            chat_id=chat_id,
            action=ChatAction.TYPING
        )
        await asyncio.sleep(4)  # typing ~5s ko‘rinadi

# =======================
# HANDLERS
# =======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Assalomu alaykum!\n\n"
        "🤖 Men aholini ro‘yxatga olish bo‘yicha savollarga javob beruvchi "
        "sun'iy intellekt yordamchingizman.\n"
        "🧠 Ismim *CensusGPT*\n\n"
        "✍️ Savolingizni yozing.",
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_q = update.message.text.strip()

    if not user_q:
        await update.message.reply_text("✍️ Savolingizni yozing.")
        return

    stop_event = asyncio.Event()

    try:
        # 🔄 typing boshlanadi
        typing_task = asyncio.create_task(
            typing_action(
                context.bot,
                update.effective_chat.id,
                stop_event
            )
        )

        # 🧠 AI javobi (THREAD ichida → typing ishlaydi)
        answer = await asyncio.to_thread(find_answer, user_q)

        # 🛑 typing to‘xtaydi
        stop_event.set()
        await typing_task

        # 🔤 Alifbo moslash
        if is_latin(user_q):
            answer = cyr_to_latin(answer)
        elif is_cyrillic(user_q):
            answer = latin_to_cyr(answer)

        await update.message.reply_text(
            f"✅ *Javob:*\n\n{answer}",
            parse_mode="Markdown"
        )

    except Exception as e:
        stop_event.set()
        print(e)
        await update.message.reply_text(
            "❌ Texnik xatolik yuz berdi. Keyinroq urinib ko‘ring."
        )
# =======================
# MAIN
# =======================
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Telegram chatbot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
