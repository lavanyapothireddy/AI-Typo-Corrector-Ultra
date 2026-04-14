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

# This uses a public API so you don't need to install Java or heavy models
API_URL = "https://api-inference.huggingface.co/models/venmous/grammar-correction-t5"

class TextIn(BaseModel):
    text: str

@app.get("/")
def home():
    return {"status": " AI Typo Corrector ULtra Running"}

@app.post("/correct")
def correct(data: TextIn):
    # Call the remote AI
    response = requests.post(API_URL, json={"inputs": data.text})
    result = response.json()
    
    # Extract corrected text
    corrected = result[0]['generated_text'] if isinstance(result, list) else data.text
    
    return {
        "original": data.text,
        "corrected": corrected,
        "error_count": 1 if corrected != data.text else 0
    }
