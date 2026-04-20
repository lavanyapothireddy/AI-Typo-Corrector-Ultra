from fastapi import FastAPI
from pydantic import BaseModel
import language_tool_python

app = FastAPI()

# ✅ OFFLINE TOOL (NO RATE LIMIT)
tool = language_tool_python.LanguageTool('en-US')


class TextIn(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "Grammarly Ultra Backend Running 🚀"}


@app.post("/correct")
def correct_text(data: TextIn):
    text = data.text

    matches = tool.check(text)
    corrected_text = language_tool_python.utils.correct(text, matches)

    words = text.split()
    total_words = len(words)
    wrong_words = len(matches)
    correct_words = max(total_words - wrong_words, 0)

    score = int((correct_words / total_words) * 100) if total_words > 0 else 0

    return {
        "original": text,
        "corrected": corrected_text,
        "wrong_words": wrong_words,
        "correct_words": correct_words,
        "total_words": total_words,
        "score": score
    }
