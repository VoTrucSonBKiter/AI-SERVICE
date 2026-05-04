from fastapi import FastAPI
from pydantic import BaseModel
import json

from llm import call_llm
from biobert import extract_entities
from schema import PROMPT

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/analyze")
def analyze(req: ChatRequest):
    entities = extract_entities(req.message)

    prompt = f"""
    {PROMPT}

    User message: {req.message}

    Extracted:
    symptoms: {entities['symptoms']}
    drugs: {entities['drugs']}
    """

    raw = call_llm(prompt)

    try:
        return json.loads(raw)
    except:
        return {
            "intent": "unknown",
            "response_text": "Xin lỗi bạn, tôi không hiểu"
        }