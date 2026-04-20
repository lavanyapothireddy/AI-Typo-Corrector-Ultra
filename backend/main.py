from fastapi import FastAPI
from pydantic import BaseModel
import language_tool_python

app = FastAPI()

# Use PUBLIC API (important for Render)
tool = language_tool_python.LanguageToolPublicAPI('en-US')


class TextIn(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "Grammarly Ultra AI is running 🚀"}


@app.post("/correct")
def correct_text(data: TextIn):
    text = data.text

    matches = tool.check(text)

    corrected = text
    wrong_words = len(matches)

    # Apply corrections
    for match in reversed(matches):
        if match.replacements:
            corrected = (
                corrected[:match.offset] +
                match.replacements[0] +
                corrected[match.offset + match.errorLength:]
            )

    total_words = len(text.split())
    correct_words = total_words - wrong_words
    score = int((correct_words / total_words) * 100) if total_words > 0 else 100

    return {
        "original": text,
        "corrected": corrected,
        "wrong_words": wrong_words,
        "correct_words": correct_words,
        "total_words": total_words,
        "score": score
    }
