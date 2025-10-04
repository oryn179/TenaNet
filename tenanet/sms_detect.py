#!/usr/bin/env python3
import re, sys

def detect_sms_attack(sms_text: str) -> str:
    patterns = [
        r"you won",
        r"lottery",
        r"urgent",
        r"click here",
        r"http://",
        r"https://",
        r"transfer",
        r"verify code",
    ]
    if len(sms_text.split()) <= 3 and "http" not in sms_text.lower():
        return "✅ SMS looks safe (short message)"
    for pat in patterns:
        if re.search(pat, sms_text, re.IGNORECASE):
            return "⚠️ Suspicious SMS Detected!"
    return "✅ SMS looks safe."

if __name__ == "__main__":
    try:
        print("TENANET SMS Detection (demo)\n")
        sms = input("Enter SMS text to scan: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n[SCAN-RESULT] No input provided (interrupted).")
        sys.exit(0)

    result = detect_sms_attack(sms)
    print(f"\n[Result] {result}")
    print(f"[SCAN-RESULT] SMS | {result}")
