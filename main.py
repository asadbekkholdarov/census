import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from translit import is_cyrillic, is_latin, latin_to_cyr, cyr_to_latin


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")  # o'zingizning API kalitingizni shu yerga yozing


if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY .env faylida yo‘q")


genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# Dataset yuklaymiz
with open("./data.json", "r", encoding="utf-8") as f:
    DATA = json.load(f)

CONTEXT = "\n".join([
    f"{i+1}. SAVOL: {x['question']} | JAVOB: {x['answer']}"
    for i, x in enumerate(DATA)
])
def find_answer(user_question: str) -> str:
    prompt = f"""
    Sen professional AI assistantsan.

    VAZIFA:
    - Foydalanuvchi savolining MAZMUNINI tahlil qil
    - Quyidagi savol-javoblardan ENG MOSINI tanla
    - Faqat o‘sha savolning JAVOBINI qaytar
    - Agar mos savol topilmasa: "Mazur tutasiz, call-markazga bog'langaningiz yaxshiroq! +998 (71) 202-8175" deb yoz

    Foydalanuvchi savoli:
    {user_question}

    SAVOL-JAVOBLAR:
    {CONTEXT}

    Faqat JAVOBNI yoz. Izoh yo‘q.
    """

    res = model.generate_content(prompt)
    return res.text.strip()



print("\n Chatbot tayyor Savolingizni yozing --- . Chiqish uchun: exit\n")

while True:
    user_q = input("Savol --> : ").strip()
    if user_q.lower() == "exit":
        break

    answer = find_answer(user_q)

# user yozgan alifboga moslashtirish
    if is_latin(user_q):
     answer = cyr_to_latin(answer)
    elif is_cyrillic(user_q):
     answer = latin_to_cyr(answer)


    print(f"Javob --> : {answer}\n")
