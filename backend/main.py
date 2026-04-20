from fastapi import FastAPI
from pydantic import BaseModel
from textblob import TextBlob

app = FastAPI()

class TextIn(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Backend running 🚀"}

@app.post("/correct")
def correct_text(data: TextIn):
    original = data.text

    # 🔹 Correct using TextBlob
    corrected_text = str(TextBlob(original).correct())

    # 🔹 Word comparison
    original_words = original.split()
    corrected_words = corrected_text.split()

    wrong = sum(1 for o, c in zip(original_words, corrected_words) if o != c)
    total = len(original_words)
    correct = total - wrong
    score = int((correct / total) * 100) if total > 0 else 0

    return {
        "original": original,
        "corrected": corrected_text,
        "wrong_words": wrong,
        "correct_words": correct,
        "total_words": total,
        "score": score
    }
