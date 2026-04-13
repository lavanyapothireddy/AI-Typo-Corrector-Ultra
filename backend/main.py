from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input model
class TextIn(BaseModel):
    text: str


# -----------------------------
# SMART CORRECTION ENGINE
# -----------------------------

SLANG_DICT = {
    "englih": "english",
    "touh": "tough",
    "anguage": "language",
    "pyhton": "python",
    "poplr": "popular",
    "schl": "school",
    "u": "you",
    "r": "are",
    "hv": "have",
}


def normalize_word(word: str) -> str:
    return SLANG_DICT.get(word.lower(), word)


def correct_text(text: str):
    words = text.split()

    corrected_words = []
    wrong_count = 0

    for w in words:
        fixed = normalize_word(w)

        if fixed != w:
            wrong_count += 1

        corrected_words.append(fixed)

    corrected_sentence = " ".join(corrected_words)

    total_words = len(words)
    correct_words = total_words - wrong_count

    # Grammarly-like score (simple but stable)
    score = int((correct_words / total_words) * 100) if total_words > 0 else 0

    return corrected_sentence, wrong_count, correct_words, total_words, score


# -----------------------------
# API
# -----------------------------

@app.post("/correct")
def correct(data: TextIn):

    corrected, wrong, correct_w, total, score = correct_text(data.text)

    return {
        "original": data.text,
        "corrected": corrected,
        "wrong_words": wrong,
        "correct_words": correct_w,
        "total_words": total,
        "score": score
    }
