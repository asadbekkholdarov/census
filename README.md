# Gemini AI Chatbot API

Bu loyiha **Gemini 2.5 Flash modeli** asosida ishlovchi AI chatbot API hisoblanadi. Chatbot berilgan **savol–javoblar (dataset)** asosida foydalanuvchi savollariga **mazmunan mos** javob qaytaradi.

API xususiyatlari:

* Lotin va Kirill alifbosini avtomatik aniqlaydi
* Savol boshqacha yozilsa ham mazmunini tushunadi
* REST API orqali web sahifaga oson ulanadi

---

##  Loyihaning tarkibi

```
chatbot_Gemini/
│
├── api.py            # Asosiy API (FastAPI)
├── main.py           # Terminalda test qilish uchun
├── translit.py       # Lotin ↔ Kirill o‘girish
├── data.json         # Savol-javoblar bazasi
├── requirements.txt  # Kerakli kutubxonalar
├── .env              # API key (foydalanuvchi qo‘shadi)
└── venv/             # Virtual muhit
```

---

## Talablar

* Python **3.10+**
* Internet (Gemini API uchun)

---

## O‘rnatish va ishga tushirish

###  Loyihani yuklab olish

```bash
git clone <repository_url>
cd chatbot_Gemini
```

---

### Virtual muhit yaratish

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### Kerakli kutubxonalarni o‘rnatish

```bash
pip install -r requirements.txt
```

---

### `.env` fayl yaratish (MUHIM)

Loyiha papkasida `.env` nomli fayl yarating va ichiga **Gemini API key** ni yozing:

```env
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXX
```

> Eslatma:
> `.env` faylni GitHub’ga yuklamang. API key maxfiy bo‘lishi kerak.

---

### API’ni ishga tushirish

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

Agar hammasi to‘g‘ri bo‘lsa:

```
Uvicorn running on http://0.0.0.0:8000
```

---

##  API’ni tekshirish

###  Brauzerda tekshirish

```
http://localhost:8000
```

Natija:

```json
{
  "status": "OK",
  "message": "Gemini Chatbot API ishlayapti",
  "docs": "/docs"
}
```

---

###  API hujjatlari (Swagger)

```
http://localhost:8000/docs
```

Bu yerda API’ni brauzer orqali test qilish mumkin.

---

## Asosiy API endpoint

### POST `/ask`

**So‘rov (JSON):**

```json
{
  "question": "royxatga olish uchun necha marta keladi"
}
```

**Javob (JSON):**

```json
{
  "answer": "odatda bir marta kelishi kifoya..."
}
```

### Xususiyatlar:

* Savol **lotincha** bo‘lsa → javob **lotincha**
* Savol **kirillcha** bo‘lsa → javob **kirillcha**
* Savol mazmuni tushunilmasa:

```json
{
  "answer": "Savol aniqlanmadi"
}
```

---

##  Web sahifaga ulash

Frontend (HTML / React / Vue va boshqalar) quyidagi manzilga POST so‘rov yuboradi:

```
http://SERVER_IP:8000/ask
```

Body:

```json
{
  "question": "Savol matni"
}
```

---

##  Xavfsizlik

* `.env` faylni hech qachon ochiq joylashtirmang
* API key faqat serverda saqlansin
* Zarurat bo‘lsa IP cheklov yoki token qo‘shish mumkin

---

##  Eslatma

Bu loyiha:

* tayyor ishlaydigan holatda topshiriladi
* kengaytirish (yangi savollar qo‘shish) oson
* serverga joylashga tayyor

---

