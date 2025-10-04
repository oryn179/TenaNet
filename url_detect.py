##url_detect.py ##Made By Oryn𓃵
import re

def detect_url_attack(url: str) -> str:
    suspicious_domains = [
        "bit.ly", "tinyurl", "freegift", "prize", "login", "verify"
    ]
    if not url.startswith("http"):
        return "⚠️ Invalid URL format."
    for domain in suspicious_domains:
        if domain.lower() in url.lower():
            return f"⚠️ Suspicious URL Detected: {url}"
    return f"✅ URL looks safe: {url}"

if __name__ == "__main__":
    print("TENANET URL Scam Detection is running...\n")
    url = input("Enter a URL to scan: ")
    print("\n[Result] " + detect_url_attack(url))
