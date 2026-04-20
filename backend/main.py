from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextIn(BaseModel):
    text: str


def simple_correct(text: str):
    corrections = {
        "dont": "don't",
        "doesnt": "doesn't",
        "cant": "can't",
        "wont": "won't",
        "im": "I'm",
        "i": "I",
        "schol": "school",
        "spedd": "speed",
        "rotatin": "rotating"
    }

    words = text.split()
    corrected_words = []
    wrong = 0

    for w in words:
        lw = w.lower()
        if lw in corrections:
            corrected_words.append(corrections[lw])
            wrong += 1
        else:
            corrected_words.append(w)

    # basic grammar fix
    if len(corrected_words) > 1:
        if corrected_words[0].lower() == "he" and corrected_words[1] == "don't":
            corrected_words[1] = "doesn't"

    corrected_sentence = " ".join(corrected_words)
    corrected_sentence = corrected_sentence.capitalize()

    total = len(words)
    correct = total - wrong
    score = int((correct / total) * 100) if total > 0 else 0

    return corrected_sentence, wrong, correct, total, score


@app.get("/")
def home():
    return {"message": "Backend running 🚀"}


@app.post("/correct")
def correct_text(data: TextIn):
    corrected, wrong, correct, total, score = simple_correct(data.text)

    return {
        "original": data.text,
        "corrected": corrected,
        "wrong_words": wrong,
        "correct_words": correct,
        "total_words": total,
        "score": score
    }
