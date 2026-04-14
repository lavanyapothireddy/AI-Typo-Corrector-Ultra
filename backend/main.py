from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Public AI Model Endpoint
API_URL = "https://api-inference.huggingface.co/models/pszemraj/flan-t5-base-grammar-synthesis"

class TextIn(BaseModel):
    text: str

@app.get("/")
def home():
    return {"status": "AI Typo Corrector Ultra Running Online"}

@app.post("/correct")
def correct(data: TextIn):
    try:
        # Add a prefix so the AI knows to FIX the text
        payload = {"inputs": f"gec: {data.text}"} 
        
        response = requests.post(API_URL, json=payload)
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            corrected = result[0].get('generated_text', data.text)
        else:
            corrected = data.text

        # If the AI returns the exact same thing, let's try a fallback
        # (Sometimes the AI is too conservative)
        return {
            "original": data.text,
            "corrected": corrected.strip(),
            "error_count": 1 if corrected.strip().lower() != data.text.lower() else 0
        }
    except Exception as e:
        return {"original": data.text, "corrected": data.text, "error": str(e)}
