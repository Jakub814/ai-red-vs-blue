from src.red_team import generate_attack
from src.blue_team import detect_attack

def run_simulation_round(selected_difficulty=None, defense_mode="ml_based"):
    attack = generate_attack(selected_difficulty)
    detection = detect_attack(attack["text"], defense_mode)

    return {
        "attack_type": attack["attack_type"],
        "difficulty": attack["difficulty"],
        "message": attack["text"],
        "true_label": attack["label"],
        "predicted_label": detection["predicted_label"],
        "confidence": detection["confidence"],
        "explanation": detection["explanation"],
        "defense_mode": defense_mode
    }