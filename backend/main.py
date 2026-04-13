from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from textblob import TextBlob

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextIn(BaseModel):
    text: str


# ------------------ SMART CORRECTION ------------------
def correct_text(text: str):

    # slang dictionary (YOU CAN EXPAND THIS)
    slang = {
        "schl": "school",
        "englih": "english",
        "touh": "tough",
        "anguage": "language",
        "pyhton": "python",
        "poplr": "popular"
    }

    words = text.split()
    fixed_words = []

    for w in words:
        fixed_words.append(slang.get(w.lower(), w))

    cleaned = " ".join(fixed_words)

    # grammar correction layer
    blob = TextBlob(cleaned)
    return str(blob.correct())


# ------------------ API ------------------
@app.post("/correct")
def correct(data: TextIn):

    corrected = correct_text(data.text)

    return {
        "original": data.text,
        "corrected": corrected
    }


@app.get("/")
def home():
    return {"status": "running"}
