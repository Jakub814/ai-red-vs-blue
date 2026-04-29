import joblib
from pathlib import Path

MODEL_PATH = Path("models/phishing_detector.joblib")
model = joblib.load(MODEL_PATH) if MODEL_PATH.exists() else None

suspicious_keywords = [
    "urgent",
    "verify",
    "suspension",
    "click",
    "reset your password",
    "unusual login",
    "confirm your address",
    "account requires",
    "detected unusual login",
    "billing",
    "payment failed",
    "security alert"
]

def generate_explanation(message: str) -> str:
    lower_msg = message.lower()
    reasons = []

    for keyword in suspicious_keywords:
        if keyword in lower_msg:
            reasons.append(f"Contains suspicious phrase: '{keyword}'")

    if "http://" in lower_msg or "https://" in lower_msg:
        reasons.append("Contains a link")

    return "; ".join(reasons) if reasons else "No high-risk phishing indicators detected; classified as benign by the trained model."

def rule_based_detect(message: str):
    lower_msg = message.lower()
    score = 0
    reasons = []

    for keyword in suspicious_keywords:
        if keyword in lower_msg:
            score += 1
            reasons.append(f"Contains suspicious phrase: '{keyword}'")

    if "http://" in lower_msg or "https://" in lower_msg:
        score += 1
        reasons.append("Contains a link")

    predicted_label = "malicious" if score >= 2 else "benign"
    confidence = min(0.5 + score * 0.1, 0.99)

    return {
        "predicted_label": predicted_label,
        "confidence": round(float(confidence), 2),
        "explanation": "; ".join(reasons) if reasons else "No strong indicators detected"
    }

def ml_detect(message: str):
    if model is None:
        raise FileNotFoundError("Model file not found. Train the model first.")

    predicted_label = model.predict([message])[0]
    probabilities = model.predict_proba([message])[0]
    class_labels = model.classes_
    confidence_map = dict(zip(class_labels, probabilities))
    confidence = confidence_map[predicted_label]

    return {
        "predicted_label": predicted_label,
        "confidence": round(float(confidence), 2),
        "explanation": generate_explanation(message)
    }

def hybrid_detect(message: str):
    rule_result = rule_based_detect(message)
    ml_result = ml_detect(message)

    if rule_result["predicted_label"] == "malicious" or ml_result["predicted_label"] == "malicious":
        predicted_label = "malicious"
    else:
        predicted_label = "benign"

    confidence = max(rule_result["confidence"], ml_result["confidence"])
    explanation = f"Rule-Based: {rule_result['predicted_label']}; ML-Based: {ml_result['predicted_label']}"

    return {
        "predicted_label": predicted_label,
        "confidence": round(float(confidence), 2),
        "explanation": explanation
    }

def detect_attack(message: str, mode="ml_based"):
    if mode == "rule_based":
        return rule_based_detect(message)
    elif mode == "hybrid":
        return hybrid_detect(message)
    return ml_detect(message)