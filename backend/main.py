from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Using the BASE model - smaller, faster, more stable
print("Checking for AI Model... the first run may take a few minutes to download.")
fixer = pipeline("text2text-generation", model="pszemraj/flan-t5-base-grammar-synthesis")

class TextIn(BaseModel):
    text: str

@app.get("/")
def home():
    return {"status": "AI Model is running!", "message": "Visit /docs for API testing"}

@app.post("/correct")
def correct(data: TextIn):
    # This model likes the "grammar: " prefix to know its job
    result = fixer(f"grammar: {data.text}", max_length=512)
    corrected_text = result[0]['generated_text']

    return {
        "original": data.text,
        "corrected": corrected_text
    }
