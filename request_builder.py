def build_request(user_id, ai_output):
    return {
        "patient_id": user_id,
        "symptoms": ai_output.get("entities", {}).get("symptoms", []),
        "drugs": ai_output.get("entities", {}).get("drugs", []),
        "urgency": ai_output.get("urgency", "LOW"),
        "status": "PENDING"
    }