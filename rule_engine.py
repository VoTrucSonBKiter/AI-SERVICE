def decide_action(ai_output):
    intent = ai_output.get("intent", "unknown")
    urgency = ai_output.get("urgency", "LOW")

    # 🚨 PRIORITY CAO NHẤT: emergency
    if urgency == "HIGH":
        return "CREATE_REQUEST"

    # 🏥 yêu cầu bác sĩ
    if intent in ["doctor_request", "find_doctor"]:
        return "SHOW_DOCTORS"

    # 🩺 có triệu chứng
    symptoms = ai_output.get("entities", {}).get("symptoms", [])
    if len(symptoms) > 0:
        return "SHOW_DOCTORS"

    return "NONE"