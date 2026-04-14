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
API_URL = "https://api-inference.huggingface.co/models/venmous/grammar-correction-t5"

class TextIn(BaseModel):
    text: str

@app.get("/")
def home():
    return {"status": "Online"}

@app.post("/correct")
def correct(data: TextIn):
    try:
        # 1. Send text to the AI
        response = requests.post(API_URL, json={"inputs": data.text})
        result = response.json()
        
        # 2. Safely extract the corrected text
        # The T5 model usually returns a list like: [{"generated_text": "..."}]
        if isinstance(result, list) and len(result) > 0:
            corrected = result[0].get('generated_text', data.text)
        elif isinstance(result, dict) and 'generated_text' in result:
            corrected = result['generated_text']
        else:
            corrected = data.text # Fallback to original if API fails

        return {
            "original": data.text,
            "corrected": corrected,
            "error_count": 1 if corrected.lower() != data.text.lower() else 0
        }
    except Exception as e:
        return {"original": data.text, "corrected": data.text, "error": str(e)}
