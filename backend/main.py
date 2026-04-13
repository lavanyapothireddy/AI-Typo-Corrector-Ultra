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

class TextRequest(BaseModel):
    text: str


FIXES = {
    "dont": "don't",
    "wont": "won't",
    "cant": "can't",
    "im": "I'm",
    "teh": "the",
    "adn": "and",
    "recieve": "receive",
    "definately": "definitely",
}


def correct(text: str):
    text = re.sub(r"\s+", " ", text).strip()

    words = text.split()
    result = []

    for w in words:
        result.append(FIXES.get(w.lower(), w))

    return " ".join(result)


@app.get("/")
def home():
    return {"status": "AI Typo Corrector Running"}


@app.post("/correct")
def correct_text(req: TextRequest):
    if not req.text:
        return {"error": "Empty text"}

    return {
        "original": req.text,
        "corrected": correct(req.text)
    }
