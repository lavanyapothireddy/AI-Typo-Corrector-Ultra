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
        # We add a specific instruction prefix so the AI knows its job
        payload = {
            "inputs": f"render corrected text: {data.text}",
            "parameters": {"top_p": 0.9, "temperature": 0.1} # Makes the AI more focused
        }
        
        response = requests.post(API_URL, json=payload)
        result = response.json()
        
        # Log the result to Render logs so you can see it
        print(f"AI Result: {result}")

        if isinstance(result, list) and len(result) > 0:
            corrected = result[0].get('generated_text', data.text)
        elif isinstance(result, dict) and 'generated_text' in result:
            corrected = result['generated_text']
        else:
            corrected = data.text

        # Return the response
        return {
            "original": data.text,
            "corrected": corrected.strip(),
            "error_count": 1 if corrected.strip().lower() != data.text.lower() else 0
        }
    except Exception as e:
        return {"original": data.text, "corrected": data.text, "error": str(e)}
