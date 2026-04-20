import language_tool_python
import re

tool = language_tool_python.LanguageTool('en-US')


# ----------------------------
# 1. Grammar Engine
# ----------------------------
def grammar_engine(text: str):
    matches = tool.check(text)
    corrected = language_tool_python.utils.correct(text, matches)
    return corrected


# ----------------------------
# 2. Context Intelligence Engine
# ----------------------------
def context_engine(text: str):

    text = text.strip()

    lower = text.lower()

    # verb structure fixes
    lower = re.sub(r"\bi am go to\b", "i am going to", lower)
    lower = re.sub(r"\bhe am\b", "he is", lower)
    lower = re.sub(r"\bshe am\b", "she is", lower)

    # negation fixes
    lower = re.sub(r"\bdont\b", "don't", lower)

    # spelling corrections (safe only common errors)
    fixes = {
        "schl": "school",
        "impotrant": "important",
        "rotatin": "rotating",
        "spedd": "speed",
        "fat": "fast"
    }

    for k, v in fixes.items():
        lower = lower.replace(k, v)

    # capitalize first letter
    return lower.capitalize()


# ----------------------------
# 3. AI-style Rewrite Engine
# ----------------------------
def rewrite_engine(text: str):

    base = context_engine(text)
    final = grammar_engine(base)

    return final


# ----------------------------
# 4. Grammarly-style Scoring
# ----------------------------
def score_engine(original: str, corrected: str):

    o_words = original.lower().split()
    c_words = corrected.lower().split()

    # semantic overlap
    overlap = len(set(o_words) & set(c_words))
    total = len(set(o_words))

    grammar_gain = 100 if original != corrected else 80

    fluency_bonus = min(len(corrected.split()) * 2, 100)

    final_score = int((overlap / total) * 60 + grammar_gain * 0.25 + fluency_bonus * 0.15)

    final_score = min(final_score, 100)

    wrong = len(o_words) - overlap

    return wrong, overlap, len(o_words), final_score