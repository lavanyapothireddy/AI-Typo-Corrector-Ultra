from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from textblob import TextBlob

app = FastAPI()

# Enable CORS
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


@app.post("/correct")
def correct_text(data: TextIn):
    text = data.text

    # ✅ REAL correction using TextBlob
    blob = TextBlob(text)
    corrected = str(blob.correct())

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
