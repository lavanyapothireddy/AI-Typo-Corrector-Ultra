from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextIn(BaseModel):
    text: str


API_URL = "https://api-inference.huggingface.co/models/vennify/t5-base-grammar-correction"


def ai_correct(text):
    try:
        response = requests.post(API_URL, json={"inputs": "grammar: " + text})
        result = response.json()
        return result[0]["generated_text"]
    except:
        return text


def analyze(original, corrected):
    orig_words = original.split()
    corr_words = corrected.split()

    wrong = sum(1 for o, c in zip(orig_words, corr_words) if o != c)
    total = len(orig_words)
    correct = total - wrong

    score = int((correct / total) * 100) if total else 0

    return wrong, correct, total, score


@app.post("/correct")
def correct(data: TextIn):
    corrected = ai_correct(data.text)
    wrong, correct_w, total, score = analyze(data.text, corrected)

    return {
        "original": data.text,
        "corrected": corrected,
        "wrong_words": wrong,
        "correct_words": correct_w,
        "total_words": total,
        "score": score
    }
