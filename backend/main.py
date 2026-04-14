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


@app.post("/correct")
def correct(data: TextIn):

    payload = {
        "inputs": "grammar: " + data.text
    }

    response = requests.post(API_URL, json=payload)
    result = response.json()

    try:
        corrected = result[0]["generated_text"]
    except:
        corrected = data.text

    return {
        "original": data.text,
        "corrected": corrected
    }
