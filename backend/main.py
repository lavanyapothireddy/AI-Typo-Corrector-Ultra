from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
import difflib

app = FastAPI()

# CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ FIXED PIPELINE (IMPORTANT CHANGE)
corrector = pipeline(
    "text-generation",
    model="pszemraj/flan-t5-large-grammar-synthesis"
)

class TextIn(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "AI Grammar Backend Running 🚀"}


@app.post("/correct")
def correct_text(data: TextIn):
    text = data.text

    # 🔥 Generate output
    result = corrector(
        text,
        max_length=128,
        do_sample=False
    )

    generated = result[0]["generated_text"]

    # 🔥 CLEAN OUTPUT (VERY IMPORTANT)
    corrected = generated.replace(text, "").strip()

    if not corrected:
        corrected = text

    # Capitalize first letter
    corrected = corrected[:1].upper() + corrected[1:]

    # 🔥 Better scoring
    similarity = difflib.SequenceMatcher(None, text, corrected).ratio()
    score = int(similarity * 100)

    return {
        "original": text,
        "corrected": corrected,
        "score": score
    }
