import random

malicious_names = ["Jakub", "Customer", "User", "Student", "Member"]
brands = ["PayPal", "Microsoft", "Amazon", "Bank of Ireland", "DHL", "University Portal"]
urgent_phrases = [
    "urgent action is required",
    "your access will be suspended",
    "immediate verification is needed",
    "your account is at risk",
    "this issue must be resolved today"
]
fake_links = [
    "http://secure-login-check.com",
    "http://delivery-update-now.com",
    "http://account-reset-alert.com",
    "http://billing-fix-now.com",
    "http://verify-session-now.com"
]

benign_subjects = [
    "project meeting",
    "library notice",
    "assignment reminder",
    "lecture update",
    "student society event",
    "attendance check",
    "portal update",
    "feedback review"
]

benign_messages = [
    "Hi {name}, just a reminder that our {subject} is scheduled for tomorrow afternoon.",
    "Please note that the {subject} has been updated on the student portal.",
    "This is a reminder that your {subject} is due next week.",
    "The {subject} has been moved to another room due to scheduling changes.",
    "Thanks, {name}. Please review the latest details about the {subject} when you have time.",
    "Please verify your attendance for the {subject} on the student portal.",
    "Your university account has been updated with information related to the {subject}.",
    "Please log in to Moodle to review details about the {subject}."
]

def generate_malicious():
    name = random.choice(malicious_names)
    brand = random.choice(brands)
    urgency = random.choice(urgent_phrases)
    link = random.choice(fake_links)

    templates = [
        f"Dear {name}, your {brand} account requires verification. Please click here immediately: {link}",
        f"{brand}: We detected unusual login activity. {urgency}. Reset your password now at {link}",
        f"Hello {name}, your recent transaction could not be processed. {urgency}. Confirm your details here: {link}",
        f"{brand} security alert: suspicious activity detected. Verify your identity now at {link}",
        f"Your parcel could not be delivered. {urgency}. Confirm your address here: {link}",
        f"Please review the attached account notice and confirm your details here: {link}",
        f"A new login attempt was blocked. Continue using your service by signing in here: {link}"
    ]

    return {
        "attack_type": "Dynamic Phishing",
        "text": random.choice(templates),
        "difficulty": random.choice(["easy", "medium", "hard"]),
        "label": "malicious"
    }

def generate_benign():
    name = random.choice(["Jakub", "student", "team", "everyone"])
    subject = random.choice(benign_subjects)

    text = random.choice(benign_messages).format(name=name, subject=subject)

    return {
        "attack_type": "Benign Communication",
        "text": text,
        "difficulty": random.choice(["easy", "medium"]),
        "label": "benign"
    }

def generate_attack():
    if random.random() < 0.5:
        return generate_malicious()
    return generate_benign()