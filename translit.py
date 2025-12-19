# Userni yozgan alifboga moslashtirish uchun transliteratsiya funksiyalari
import re
from transliterate import translit

CYR_TO_LAT = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d",
    "е": "e", "ё": "yo", "ж": "j", "з": "z", "и": "i",
    "й": "y", "к": "k", "л": "l", "м": "m", "н": "n",
    "о": "o", "п": "p", "р": "r", "с": "s", "т": "t",
    "у": "u", "ф": "f", "х": "x", "ц": "ts", "ч": "ch",
    "ш": "sh", "щ": "sh", "ъ": "", "ы": "i", "ь": "",
    "э": "e", "ю": "yu", "я": "ya",
    "қ": "q", "ғ": "g‘", "ҳ": "h", "ў": "o‘",
}

LAT_TO_CYR = {
    "yo": "ё", "yu": "ю", "ya": "я", "ch": "ч", "sh": "ш",
    "o‘": "ў", "g‘": "ғ", "q": "қ", "h": "ҳ",
}

def is_cyrillic(text: str) -> bool:
    return bool(re.search(r"[А-Яа-я]", text))

def is_latin(text: str) -> bool:
    return bool(re.search(r"[A-Za-z]", text))

def cyr_to_latin(text: str) -> str:
    result = ""
    for ch in text.lower():
        result += CYR_TO_LAT.get(ch, ch)
    return result

def latin_to_cyr(text: str) -> str:
    t = text.lower()
    for k, v in LAT_TO_CYR.items():
        t = t.replace(k, v)
    return t
