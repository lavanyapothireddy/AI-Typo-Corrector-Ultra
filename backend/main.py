from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from difflib import get_close_matches

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextIn(BaseModel):
    text: str


# 🔤 SIMPLE DICTIONARY (expand this)
WORDS = [
    "english", "language", "school", "python",
    "string", "popular", "going", "hello", "world"
]


# 🧠 SPELL CORRECTOR
def correct_word(word):
    matches = get_close_matches(word.lower(), WORDS, n=1, cutoff=0.7)
    return matches[0] if matches else word


def spell_correct(text):
    return " ".join([correct_word(w) for w in text.split()])


# 🤖 AI GRAMMAR
API_URL = "https://api-inference.huggingface.co/models/vennify/t5-base-grammar-correction"

def grammar_correct(text):
    try:
        res = requests.post(API_URL, json={"inputs": "grammar: " + text})
        data = res.json()
        return data[0]["generated_text"]
    except:
        return text


# 📊 ANALYSIS
def analyze(original, corrected):
    o = original.split()
    c = corrected.split()

    wrong = sum(1 for i in range(min(len(o), len(c))) if o[i] != c[i])
    total = len(o)
    correct = total - wrong

    score = int((correct / total) * 100) if total else 0

    return wrong, correct, total, score


@app.post("/correct")
def correct(data: TextIn):

    # STEP 1: spelling
    spell_fixed = spell_correct(data.text)

    # STEP 2: grammar
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
