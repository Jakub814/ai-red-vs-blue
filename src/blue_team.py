import joblib
from pathlib import Path

MODEL_PATH = Path("models/phishing_detector.joblib")

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

model = None
if MODEL_PATH.exists():
    model = joblib.load(MODEL_PATH)

def generate_explanation(message: str) -> str:
    lower_msg = message.lower()
    reasons = []

    for keyword in suspicious_keywords:
        if keyword in lower_msg:
            reasons.append(f"Contains suspicious phrase: '{keyword}'")

    if "http://" in lower_msg or "https://" in lower_msg:
        reasons.append("Contains a link")

    return "; ".join(reasons) if reasons else "No high-risk phishing indicators detected; classified as benign by the trained model."

def detect_attack(message: str) -> dict:
    if model is None:
        raise FileNotFoundError("Model file not found. Train the model first.")

    predicted_label = model.predict([message])[0]

    probabilities = model.predict_proba([message])[0]
    class_labels = model.classes_
    confidence_map = dict(zip(class_labels, probabilities))
    confidence = confidence_map[predicted_label]

    explanation = generate_explanation(message)

    return {
        "predicted_label": predicted_label,
        "confidence": round(float(confidence), 2),
        "explanation": explanation
    }