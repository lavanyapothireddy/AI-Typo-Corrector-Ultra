from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from textblob import TextBlob
import nltk

# ✅ force download (important for Render)
nltk.download('punkt')

app = FastAPI()

# CORS fix
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextIn(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "Backend running 🚀"}


# 🔥 fallback grammar fixes (rule-based boost)
def basic_fix(text):
    fixes = {
        "dont": "don't",
        "cant": "can't",
        "wont": "won't",
        "im": "I'm",
        "i ": "I ",
        "apple": "apples"  # simple plural fix
    }
    words = text.split()
    new_words = []

    for w in words:
        lw = w.lower()
        if lw in fixes:
            new_words.append(fixes[lw])
        else:
            new_words.append(w)

    return " ".join(new_words)


@app.post("/correct")
def correct_text(data: TextIn):
    text = data.text

    # Step 1: TextBlob correction
    blob = TextBlob(text)
    corrected = str(blob.correct())

    # Step 2: fallback improvement
    corrected = basic_fix(corrected)

    # Step 3: Capitalize first letter
    corrected = corrected[:1].upper() + corrected[1:]

    # scoring
    words = text.split()
    corrected_words = corrected.split()

    correct_count = sum(1 for a, b in zip(words, corrected_words) if a == b)
    total = len(words)
    wrong = total - correct_count
    score = int((correct_count / total) * 100) if total > 0 else 0

    return {
        "original": text,
        "corrected": corrected,
        "wrong_words": wrong,
        "correct_words": correct_count,
        "total_words": total,
        "score": score
    }
