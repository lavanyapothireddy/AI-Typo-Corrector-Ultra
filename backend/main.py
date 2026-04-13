from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import language_tool_python

# -----------------------
# APP INITIALIZATION
# -----------------------
app = FastAPI()

# -----------------------
# CORS FIX (IMPORTANT)
# -----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow frontend (5500, 3000, etc.)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# NLP ENGINE
# -----------------------
tool = language_tool_python.LanguageTool("en-US")

# -----------------------
# REQUEST MODEL (clean structure)
# -----------------------
class TextRequest(BaseModel):
    text: str

# -----------------------
# ROUTES
# -----------------------

@app.get("/")
def home():
    return {
        "message": "AI Typo Corrector Ultra API is running"
    }


@app.post("/correct")
def correct_text(req: TextRequest):
    text = req.text

    if not text.strip():
        return {
            "error": "Empty text provided"
        }

    # -----------------------
    # ERROR DETECTION
    # -----------------------
    matches = tool.check(text)

    # -----------------------
    # CORRECTION
    # -----------------------
    corrected_text = language_tool_python.utils.correct(text, matches)

    # -----------------------
    # OPTIONAL: ERROR DETAILS
    # -----------------------
    issues = []
    for m in matches:
        issues.append({
            "message": m.message,
            "offset": m.offset,
            "length": m.errorLength,
            "suggestions": m.replacements[:3]
        })

    # -----------------------
    # RESPONSE
    # -----------------------
    return {
        "original": text,
        "corrected": corrected_text,
        "issues_count": len(matches),
        "issues": issues
    }