from fastapi import FastAPI
from pydantic import BaseModel
from core import rewrite_engine, score_engine

app = FastAPI()


class TextIn(BaseModel):
    text: str


@app.post("/correct")
def correct(data: TextIn):

    original = data.text

    corrected = rewrite_engine(original)

    wrong, correct_w, total, score = score_engine(original, corrected)

    return {
        "original": original,
        "corrected": corrected,
        "wrong_words": wrong,
        "correct_words": correct_w,
        "total_words": total,
        "score": score
    }
