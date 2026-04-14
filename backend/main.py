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


@app.post("/correct")
def run(data: TextIn):
    corrected, wrong, total, score = correct(data.text)

    return {
        "original": data.text,
        "corrected": corrected,
        "wrong_words": wrong,
        "total_words": total,
        "score": score
    }
