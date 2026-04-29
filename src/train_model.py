import os
import joblib
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

TRAINING_DATA = [
    # ---------------- MALICIOUS ----------------
    {
        "text": "Dear user, your account requires urgent verification. Please click the link below to avoid suspension: http://secure-login-check.com",
        "label": "malicious"
    },
    {
        "text": "Your parcel could not be delivered today. Please confirm your address immediately here: http://delivery-update-now.com",
        "label": "malicious"
    },
    {
        "text": "We detected unusual login activity on your account. Reset your password now at http://account-reset-alert.com",
        "label": "malicious"
    },
    {
        "text": "Your mailbox is almost full. Upgrade now to avoid losing emails: http://mail-upgrade-now.com",
        "label": "malicious"
    },
    {
        "text": "Security alert: suspicious sign-in detected. Verify your identity immediately here: http://verify-session-now.com",
        "label": "malicious"
    },
    {
        "text": "Payment failed for your subscription. Update billing details now: http://billing-fix-now.com",
        "label": "malicious"
    },
    {
        "text": "Bank of Ireland: suspicious transaction detected. Verify your account immediately at http://verify-bank-now.com",
        "label": "malicious"
    },
    {
        "text": "Amazon notice: your account has been locked. Confirm your login now at http://amazon-security-alert.com",
        "label": "malicious"
    },
    {
        "text": "DHL delivery failed. Your parcel is on hold. Update your address now at http://delivery-resolve-now.com",
        "label": "malicious"
    },
    {
        "text": "Please review the attached account notice and confirm your details here: http://portal-check-secure.com",
        "label": "malicious"
    },
    {
        "text": "A new login attempt was blocked. Continue using your service by signing in here: http://session-review-now.com",
        "label": "malicious"
    },
    {
        "text": "Please review your secure account message here: http://secure-message-check.com",
        "label": "malicious"
    },
    {
        "text": "Your recent transaction could not be processed. Review your details here: http://billing-review-now.com",
        "label": "malicious"
    },
    {
        "text": "Confirm your account details to prevent interruption of service: http://confirm-service-now.com",
        "label": "malicious"
    },
    {
        "text": "A login attempt was detected on your account. Review the activity here: http://review-login-now.com",
        "label": "malicious"
    },

    # ---------------- BENIGN ----------------
    {
        "text": "Hi team, just a reminder that our project meeting is scheduled for 2 PM tomorrow in Room 3.",
        "label": "benign"
    },
    {
        "text": "The library will close at 6 PM today due to scheduled maintenance. Please plan accordingly.",
        "label": "benign"
    },
    {
        "text": "Reminder: your software development assignment is due next Monday at 5 PM via Moodle.",
        "label": "benign"
    },
    {
        "text": "Your lecture has been moved to Lab 2 this afternoon.",
        "label": "benign"
    },
    {
        "text": "Please find attached the updated timetable for next semester.",
        "label": "benign"
    },
    {
        "text": "The society meeting has been postponed until Friday evening.",
        "label": "benign"
    },
    {
        "text": "The project presentation schedule has now been published on Moodle.",
        "label": "benign"
    },
    {
        "text": "Please review the latest class notice when you have time.",
        "label": "benign"
    },
    {
        "text": "The student portal has been updated with this week’s room changes.",
        "label": "benign"
    },
    {
        "text": "Please verify your attendance for tomorrow’s lab session on the student portal.",
        "label": "benign"
    },
    {
        "text": "Your university account has been updated with the latest timetable.",
        "label": "benign"
    },
    {
        "text": "Please log in to Moodle to review your assignment feedback.",
        "label": "benign"
    },
    {
        "text": "A new update is available on the library account page for registered students.",
        "label": "benign"
    },
    {
        "text": "Confirm your attendance for the student workshop on the university portal.",
        "label": "benign"
    },
    {
        "text": "Your account details for the library system were updated successfully this morning.",
        "label": "benign"
    },
    {
        "text": "Please review your portal message about the upcoming timetable changes.",
        "label": "benign"
    },
    {
        "text": "A login to the student portal was recorded successfully from your usual device.",
        "label": "benign"
    },
    {
        "text": "Please confirm your presentation slot using the department scheduling system.",
        "label": "benign"
    },
    {
        "text": "Your secure university portal message is now available to review.",
        "label": "benign"
    }
]

def train_and_save_model():
    df = pd.DataFrame(TRAINING_DATA)

    model = Pipeline([
        ("vectorizer", CountVectorizer(ngram_range=(1, 2), lowercase=True)),
        ("classifier", LogisticRegression(max_iter=2000))
    ])

    model.fit(df["text"], df["label"])

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/phishing_detector.joblib")

    print("Model trained and saved to models/phishing_detector.joblib")


if __name__ == "__main__":
    train_and_save_model()