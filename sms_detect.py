##Sms_Detect.py ##Made By Oryn𓃵
import re

def detect_sms_attack(sms_text: str) -> str:
    patterns = [
        r"you won",
        r"lottery",
        r"urgent",
        r"click here",
        r"http://",
        r"https://",
    ]
    for pat in patterns:
        if re.search(pat, sms_text, re.IGNORECASE):
            return "⚠️ Suspicious SMS Detected!"
    return "✅ SMS looks safe."

if __name__ == "__main__":
    print("TENANET SMS Detection is running...\n")
    sms = input("Enter SMS text to scan: ")
    print("\n[Result] " + detect_sms_attack(sms))
#!/usr/bin/env python3

print("TENANET SMS Detection (demo)")

try:
    text = input("Enter SMS text to scan: ")
except EOFError:
    print("[SCAN-RESULT] No input provided (stdin closed).")
    exit(0)

if not text.strip():
    print("[SCAN-RESULT] Empty input.")
else:
    print(f"[SCAN-RESULT] Scanned text: {text}")
