from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

# 1. FIX: Added CORS Middleware so the browser allows the connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Replace with your actual Hugging Face Token (or use Environment Variables)
HF_TOKEN = "your_hugging_face_token_here"
API_URL = "https://api-inference.huggingface.co/models/Psudo-Code/grammar-error-correction"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

class TextRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"status": "AI Typo Corrector is Online!"}

@app.post("/correct")
async def correct(data: TextRequest):
    # We add "Fix grammar: " to the start to tell the AI what its job is
    payload = {
        "inputs": f"Fix grammar: {data.text}",
        "parameters": {
            "wait_for_model": True,
            "max_length": 100
        }
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()
    
    # Hugging Face models sometimes return a list of dicts or just a list
    if isinstance(result, list) and len(result) > 0:
        # Try to get 'generated_text', if not, just take the first string
        final_text = result[0].get("generated_text", result[0])
    else:
        final_text = data.text

    # Final cleanup: Remove the "Fix grammar: " prefix if the AI kept it
    final_text = final_text.replace("Fix grammar: ", "").strip()

    return {
        "original": data.text,
        "corrected": final_text
    }
