#!/usr/bin/env python3
import re, sys

def detect_email_attack(email_text: str) -> str:
    patterns = [
        r"verify your account",
        r"reset your password",
        r"bank account",
        r"urgent",
        r"congratulations",
        r"click here",
        r"account suspended",
    ]
    # short-message safety rule
    if len(email_text.split()) <= 3 and "http" not in email_text.lower():
        return "✅ Email looks safe (short message)"
    for pat in patterns:
        if re.search(pat, email_text, re.IGNORECASE):
            return "⚠️ Suspicious Email Detected!"
    return "✅ Email looks safe."

if __name__ == "__main__":
    try:
        print("TENANET Email Detection (demo)\n")
        email = input("Enter email text to scan: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n[SCAN-RESULT] No input provided (interrupted).")
        sys.exit(0)

    result = detect_email_attack(email)
    print(f"\n[Result] {result}")
    # single parseable line for logs
    print(f"[SCAN-RESULT] EMAIL | {result}")
