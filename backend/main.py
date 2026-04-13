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


# LOAD AI MODEL (this is real intelligence)
corrector = pipeline(
    "text2text-generation",
    model="vennify/t5-base-grammar-correction"
)


def correct_text(text):
    result = corrector(text, max_length=256)
    return result[0]['generated_text']


@app.post("/correct")
def correct(data: TextIn):
    return {
        "original": data.text,
        "corrected": correct_text(data.text)
    }
