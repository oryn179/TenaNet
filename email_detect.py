##EMAIL_Detect.py ##Made By Oryn𓃵
import re

def detect_email_attack(email_text: str) -> str:
    # Simple suspicious keyword patterns
    patterns = [
        r"verify your account",
        r"reset your password",
        r"bank account",
        r"urgent",
        r"congratulations",
        r"click here",
    ]
    for pat in patterns:
        if re.search(pat, email_text, re.IGNORECASE):
            return "⚠️ Suspicious Email Detected!"
    return "✅ Email looks safe."

if __name__ == "__main__":
    print("TENANET Email Detection is running...\n")
    email = input("Enter email text to scan: ")
    print("\n[Result] " + detect_email_attack(email))


##Made By Oryn 