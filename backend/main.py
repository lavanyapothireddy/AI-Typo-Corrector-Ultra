from fastapi import FastAPI
from pydantic import BaseModel
from textblob import TextBlob
import re

app = FastAPI()

class TextIn(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "Backend running 🚀"}


# 🔹 simple grammar fixes (smart rules)
def grammar_fix(text):
    text = text.lower()

    # subject-verb agreement
    text = re.sub(r"\bhe dont\b", "he doesn't", text)
    text = re.sub(r"\bshe dont\b", "she doesn't", text)
    text = re.sub(r"\bit dont\b", "it doesn't", text)

    # plural correction
    text = re.sub(r"\bapple\b", "apples", text)

    return text


@app.post("/correct")
def correct_text(data: TextIn):
    try:
        original = data.text

        # Step 1: spelling correction
        corrected = str(TextBlob(original).correct())

        # Step 2: grammar correction
        corrected = grammar_fix(corrected)

        # Step 3: formatting
        corrected = corrected.capitalize()

        # scoring
        original_words = original.split()
        corrected_words = corrected.split()

        wrong = sum(1 for o, c in zip(original_words, corrected_words) if o != c)
        total = len(original_words)
        correct = total - wrong
        score = int((correct / total) * 100) if total > 0 else 0

        return {
            "original": original,
            "corrected": corrected,
            "wrong_words": wrong,
            "correct_words": correct,
            "total_words": total,
            "score": score
        }

    except Exception as e:
        return {"error": str(e)}
