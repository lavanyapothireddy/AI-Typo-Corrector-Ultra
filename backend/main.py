from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import language_tool_python
import os

app = FastAPI()

# Allow your website to talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the tool
tool = language_tool_python.LanguageTool('en-US')

class TextIn(BaseModel):
    text: str

@app.get("/")
def home():
    return {"status": "Backend is running!"}

@app.post("/correct")
def correct(data: TextIn):
    matches = tool.check(data.text)
    corrected_text = language_tool_python.utils.correct(data.text, matches)
    
    return {
        "original": data.text,
        "corrected": corrected_text,
        "error_count": len(matches)
    }
