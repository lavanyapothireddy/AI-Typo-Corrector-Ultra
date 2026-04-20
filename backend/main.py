from fastapi import FastAPI
from pydantic import BaseModel
import difflib

app = FastAPI()

# -----------------------------
# Input Schema
# -----------------------------
class TextIn(BaseModel):
    text: str

# -----------------------------
# Vocabulary
# -----------------------------
WORD_LIST = set([
    "i","am","is","are","he","she","it","we","they",
    "go","goes","going","went","like","likes","love",
    "school","apple","apples","eat","eating",
    "play","playing","run","running",
    "to","from","in","on","at","with",
    "this","that","these","those",
    "good","bad","fast","slow",
    "you","your","my","our",
    "do","does","did","don't","doesn't"
])

# -----------------------------
# Spell correction
# -----------------------------
def correct_word(word):
    matches = difflib.get_close_matches(word, WORD_LIST, n=1, cutoff=0.7)
    return matches[0] if matches else word

# -----------------------------
# Grammar rules (FIXED)
# -----------------------------
def grammar_fix(words):
    result = []

    for i, w in enumerate(words):

        prev = words[i-1] if i > 0 else ""

        # FIX 1: he/she/it + don't → doesn't
        if w in ["dont", "don't"]:
            if prev in ["he", "she", "it"]:
                result.append("doesn't")
            else:
                result.append("don't")
            continue

        # FIX 2: he/she/it + go → goes
        if w == "go" and prev in ["he", "she", "it"]:
            result.append("goes")
            continue

        # FIX 3: i am go → i am going
        if w == "go" and i > 1 and words[i-2] == "i" and words[i-1] == "am":
            result.append("going")
            continue

        # FIX 4: like apple → apples
        if w == "apple" and prev == "like":
            result.append("apples")
            continue

        result.append(w)

    return result

# -----------------------------
# Main processing
# -----------------------------
def process_text(text):
    words = text.lower().split()

    corrected_words = []
    wrong = 0

    for w in words:
        new_w = correct_word(w)
        if new_w != w:
            wrong += 1
        corrected_words.append(new_w)

    # Apply grammar rules
    corrected_words = grammar_fix(corrected_words)

    corrected_sentence = " ".join(corrected_words)

    total = len(words)
    correct = total - wrong
    score = int((correct / total) * 100) if total > 0 else 100

    return {
        "original": text,
        "corrected": corrected_sentence.capitalize(),
        "wrong_words": wrong,
        "correct_words": correct,
        "total_words": total,
        "score": score
    }

# -----------------------------
# API
# -----------------------------
@app.post("/correct")
def correct_text(data: TextIn):
    return process_text(data.text)
