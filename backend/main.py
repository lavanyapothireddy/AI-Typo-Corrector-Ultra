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
API_URL = "https://api-inference.huggingface.co/models/vennify/t5-base-grammar-correction"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

class TextRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"status": "AI Typo Corrector is Online!"}

@app.post("/correct")
async def correct(data: TextRequest):
    # 'gec:' helps the T5 model understand it needs to fix grammar
    payload = {
        "inputs": f"gec: {data.text}",
        "parameters": {"wait_for_model": True}
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()
        
        # Safely extract the corrected text
        if isinstance(result, list) and len(result) > 0:
            final_text = result[0].get("generated_text", data.text)
        else:
            final_text = data.text
            
    except Exception as e:
        final_text = data.text
        print(f"Error: {e}")

    # 2. FIX: We use the key "corrected" here
    return {
        "original": data.text,
        "corrected": final_text
    }
