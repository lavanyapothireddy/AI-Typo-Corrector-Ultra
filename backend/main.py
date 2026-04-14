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
# Use this model instead - it's much better at catching 'i am go'
API_URL = "https://api-inference.huggingface.co/models/pszemraj/flan-t5-large-grammar-synthesis"

# ... inside your correct function ...
payload = {
    "inputs": f"grammar: {data.text}", # Changed 'fix:' to 'grammar:'
}

class TextIn(BaseModel):
    text: str

@app.get("/")
def home():
    return {"status": "AI Typo Corrector Ultra Running Online"}

@app.post("/correct")
def correct(data: TextIn):
    try:
        # We add 'fix: ' to the start of the sentence. 
        # This is the "magic word" for this AI model to start correcting.
        payload = { "inputs": f"grammar: {data.text}", # Changed 'fix:' to 'grammar:'
                  }
        
        response = requests.post(API_URL, json=payload)
        result = response.json()
        
        # Log the AI's raw thoughts to your Render terminal
        print(f"AI response: {result}")

        if isinstance(result, list) and len(result) > 0:
            corrected = result[0].get('generated_text', data.text)
        else:
            corrected = data.text

        # Clean up the output (remove the AI's prefix if it adds one)
        final_text = corrected.replace("fix: ", "").strip()

        return {
            "original": data.text,
            "corrected": final_text,
            "error_count": 1 if final_text.lower() != data.text.lower() else 0
        }
    except Exception as e:
        return {"original": data.text, "corrected": data.text, "error": str(e)}
