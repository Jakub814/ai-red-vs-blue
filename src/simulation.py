from src.red_team import generate_attack
from src.blue_team import detect_attack

def run_simulation_round():
    attack = generate_attack()
    detection = detect_attack(attack["text"])

    return {
        "attack_type": attack["attack_type"],
        "difficulty": attack["difficulty"],
        "message": attack["text"],
        "true_label": attack["label"],
        "predicted_label": detection["predicted_label"],
        "confidence": detection["confidence"],
        "explanation": detection["explanation"]
    }