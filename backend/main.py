from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextIn(BaseModel):
    text: str


# SAFE MODE (works on Render)
corrector = pipeline(
    "text-generation",
    model="gpt2"   # fallback model that ALWAYS works
)


def correct_text(text: str):
    prompt = f"Correct grammar: {text}"
    result = corrector(prompt, max_length=50, num_return_sequences=1)

    return result[0]["generated_text"]


@app.post("/correct")
def correct(data: TextIn):
    return {
        "original": data.text,
        "corrected": correct_text(data.text)
    }
