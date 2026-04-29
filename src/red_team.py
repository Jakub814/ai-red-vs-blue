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
soft_phrases = [
    "please review the details",
    "please confirm your information",
    "review your account notice",
    "check your latest account message",
    "continue using your service by signing in"
]
fake_links = [
    "http://secure-login-check.com",
    "http://delivery-update-now.com",
    "http://account-reset-alert.com",
    "http://billing-fix-now.com",
    "http://verify-session-now.com",
    "http://portal-check-secure.com",
    "http://review-login-now.com"
]

benign_names = ["Jakub", "student", "team", "everyone", "member"]
benign_subjects = [
    "project meeting",
    "library notice",
    "assignment reminder",
    "lecture update",
    "student society event",
    "attendance check",
    "portal update",
    "feedback review",
    "timetable change",
    "presentation slot"
]

easy_benign_templates = [
    "Hi {name}, just a reminder that our {subject} is scheduled for tomorrow afternoon.",
    "Please note that the {subject} has been updated on the student portal.",
    "This is a reminder that your {subject} is due next week.",
    "The {subject} has been moved to another room due to scheduling changes.",
    "Thanks, {name}. Please review the latest details about the {subject} when you have time."
]

medium_benign_templates = [
    "Please verify your attendance for the {subject} on the student portal.",
    "Your university account has been updated with information related to the {subject}.",
    "Please log in to Moodle to review details about the {subject}.",
    "Confirm your details for the {subject} using the university portal.",
    "Your secure portal message about the {subject} is now available."
]

hard_benign_templates = [
    "A login to the student portal was recorded successfully. Please review the {subject} details when convenient.",
    "Your account message about the {subject} is available on the university system.",
    "Please confirm your presentation details for the {subject} on the student scheduling portal.",
    "Your account information related to the {subject} was updated successfully this morning.",
    "Review your secure university portal message for details about the {subject}."
]

easy_malicious_templates = [
    "Dear {name}, your {brand} account requires verification. Please click here immediately: {link}",
    "{brand}: We detected unusual login activity. {urgent}. Reset your password now at {link}",
    "{brand} security alert: suspicious activity detected. Verify your identity now at {link}",
    "Your parcel could not be delivered. {urgent}. Confirm your address here: {link}"
]

medium_malicious_templates = [
    "Hello {name}, your recent transaction could not be processed. {urgent}. Confirm your details here: {link}",
    "Please review the attached account notice and confirm your details here: {link}",
    "A new login attempt was blocked. Continue using your service by signing in here: {link}",
    "Please review your secure account message here: {link}",
    "Confirm your account details to prevent interruption of service: {link}"
]

hard_malicious_templates = [
    "Please review your latest account notice and confirm your information here: {link}",
    "A login attempt was detected on your account. Review the activity here: {link}",
    "Your service notification requires confirmation. Continue here: {link}",
    "Review your secure portal message here: {link}",
    "Your recent account message is ready to review here: {link}"
]

def generate_malicious():
    name = random.choice(malicious_names)
    brand = random.choice(brands)
    urgent = random.choice(urgent_phrases)
    link = random.choice(fake_links)

    difficulty = random.choice(["easy", "medium", "hard"])

    if difficulty == "easy":
        text = random.choice(easy_malicious_templates).format(
            name=name, brand=brand, urgent=urgent, link=link
        )
    elif difficulty == "medium":
        text = random.choice(medium_malicious_templates).format(
            name=name, brand=brand, urgent=urgent, link=link
        )
    else:
        text = random.choice(hard_malicious_templates).format(
            name=name, brand=brand, urgent=urgent, link=link
        )

    return {
        "attack_type": "Dynamic Phishing",
        "text": text,
        "difficulty": difficulty,
        "label": "malicious"
    }

def generate_benign():
    name = random.choice(benign_names)
    subject = random.choice(benign_subjects)

    difficulty = random.choice(["easy", "medium", "hard"])

    if difficulty == "easy":
        text = random.choice(easy_benign_templates).format(name=name, subject=subject)
    elif difficulty == "medium":
        text = random.choice(medium_benign_templates).format(name=name, subject=subject)
    else:
        text = random.choice(hard_benign_templates).format(name=name, subject=subject)

    return {
        "attack_type": "Benign Communication",
        "text": text,
        "difficulty": difficulty,
        "label": "benign"
    }

def generate_attack(selected_difficulty=None):
    while True:
        attack = generate_malicious() if random.random() < 0.5 else generate_benign()
        if selected_difficulty is None or attack["difficulty"] == selected_difficulty:
            return attack