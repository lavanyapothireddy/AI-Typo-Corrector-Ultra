from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json
import os
from difflib import get_close_matches
from wordfreq import zipf_frequency

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextIn(BaseModel):
    text: str

class LearnIn(BaseModel):
    wrong: str
    correct: str


# =========================
# 📂 SLANG DATABASE
# =========================
DB_FILE = "slang_db.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)


# =========================
# 🧠 SMART WORD CHECK
# =========================
COMMON_WORDS = [
    "english", "language", "school", "python",
    "string", "popular", "going", "hello",
    "world", "because", "you", "are"
]

def correct_word(word, db):
    word_lower = word.lower()

    # 1️⃣ Check learned slang
    if word_lower in db:
        return db[word_lower]

    # 2️⃣ If valid English word → keep
    if zipf_frequency(word_lower, "en") > 3:
        return word

    # 3️⃣ Try to find closest match
    match = get_close_matches(word_lower, COMMON_WORDS, n=1, cutoff=0.6)

    return match[0] if match else word


def spell_correct(text, db):
    return " ".join([correct_word(w, db) for w in text.split()])


# =========================
# 🤖 AI GRAMMAR
# =========================
API_URL = "https://api-inference.huggingface.co/models/vennify/t5-base-grammar-correction"

def grammar_correct(text):
    try:
        res = requests.post(API_URL, json={"inputs": "grammar: " + text})
        data = res.json()
        return data[0]["generated_text"]
    except:
        return text


# =========================
# 📊 ANALYSIS
# =========================
def analyze(original, corrected):
    o = original.split()
    c = corrected.split()

    wrong = sum(1 for i in range(min(len(o), len(c))) if o[i] != c[i])
    total = len(o)
    correct = total - wrong

    score = int((correct / total) * 100) if total else 0

    return wrong, correct, total, score


# =========================
# 🚀 MAIN API
# =========================
@app.get("/")
def home():
    return {"status": "AI Typo Corrector Running"}


@app.post("/correct")
def correct(data: TextIn):
    db = load_db()

    # Step 1: smart spelling
    spell_fixed = spell_correct(data.text, db)

    # Step 2: grammar AI
    corrected = grammar_correct(spell_fixed)

    wrong, correct_w, total, score = analyze(data.text, corrected)

    return {
        "original": data.text,
        "corrected": corrected,
        "wrong_words": wrong,
        "correct_words": correct_w,
        "total_words": total,
        "score": score
    }


# =========================
# 🧠 LEARNING API
# =========================
@app.post("/learn")
def learn(data: LearnIn):
    db = load_db()

    db[data.wrong.lower()] = data.correct.lower()

    save_db(db)

    return {"message": "Learned successfully", "data": db}
