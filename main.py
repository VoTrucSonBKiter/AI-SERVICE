from fastapi import FastAPI
from pydantic import BaseModel
import json

from llm import call_llm
from biobert import extract_entities
from schema import PROMPT
from rule_engine import decide_action
from doctor_service import get_available_doctors
from request_builder import build_request  # 👈 nhớ import

app = FastAPI()

class ChatRequest(BaseModel):
    message: str


def normalize(ai_output):
    return {
        "intent": ai_output.get("intent", "unknown"),
        "entities": {
            "symptoms": ai_output.get("entities", {}).get("symptoms", []),
            "drugs": ai_output.get("entities", {}).get("drugs", [])
        },
        "urgency": ai_output.get("urgency", "LOW"),
        "actions": ai_output.get("actions", []),
        "response_text": ai_output.get("response_text", "")
    }


@app.post("/analyze")
def analyze(req: ChatRequest):
    # 🔹 Step 1: extract entities
    entities = extract_entities(req.message)

    # 🔹 Step 2: build prompt
    prompt = f"""
    {PROMPT}

    User message: {req.message}

    Extracted:
    symptoms: {entities['symptoms']}
    drugs: {entities['drugs']}
    """

    # 🔹 Step 3: call LLM
    raw = call_llm(prompt)

    try:
        ai_output = json.loads(raw)
    except:
        return {
            "intent": "unknown",
            "response_text": "Xin lỗi bạn, tôi không hiểu"
        }

    # 🔹 Step 4: normalize
    ai_output = normalize(ai_output)

    # 🔹 Step 5: safety for drug
    if ai_output["intent"] == "drug_usage":
        ai_output["response_text"] += "\n\nPlease consult a doctor before use."

    # 🔹 Step 6: override action
    action = decide_action(ai_output)
    ai_output["actions"] = [{"type": action}]

    # 🔹 Step 7: handle SHOW_DOCTORS
    if action == "SHOW_DOCTORS":
        doctors = get_available_doctors()
        return {
            **ai_output,
            "doctors": doctors
        }

    # 🔹 Step 8: handle CREATE_REQUEST
    if action == "CREATE_REQUEST":
        request_data = build_request("user_123", ai_output)
        return {
            "message": "Doctor will contact you soon",
            "request": request_data
        }

    # 🔹 default
    return ai_output