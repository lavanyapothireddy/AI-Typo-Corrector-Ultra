from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextIn(BaseModel):
    text: str


SLANG = {
    "englih": "english",
    "touh": "tough",
    "pyhton": "python",
    "schl": "school",
}


def correct(text: str):
    words = text.split()
    corrected = []
    wrong = 0

    for w in words:
        fixed = SLANG.get(w.lower(), w)
        if fixed != w:
            wrong += 1
        corrected.append(fixed)

    final_text = " ".join(corrected)
    total = len(words)
    score = int(((total - wrong) / total) * 100) if total else 0

    return final_text, wrong, total, score

@app.get("/")
def home():
    return {"status": "AI Typo Corrector is Online!"}
@app.post("/correct")
async def correct(data: TextRequest):
    payload = {
        "inputs": f"grammar: {data.text}",
        "parameters": {"wait_for_model": True} # This forces Render to wait for the AI
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()

    # Debug: Print this in your Render logs to see what the AI is actually saying
    print(f"AI Response: {result}")

    # Logic to extract the text safely
    if isinstance(result, list) and len(result) > 0:
        final_text = result[0].get("generated_text", data.text)
    else:
        final_text = data.text # Fallback to original text if AI fails

    error_count = 1 if final_text.lower() != data.text.lower() else 0
    
    return {
        "original": data.text,
        "corrected": final_text,
        "error_count": error_count
    }
