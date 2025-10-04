#!/usr/bin/env python3
import re, sys
from urllib.parse import urlparse

def detect_url_attack(url: str) -> str:
    if not url:
        return "No URL provided."
    if not url.startswith("http"):
        url = "http://" + url
    try:
        parsed = urlparse(url)
    except Exception:
        return "⚠️ Invalid URL format."
    suspicious_tokens = ["bit.ly", "tinyurl", "freegift", "prize", "login", "verify", "ngrok.io"]
    host = parsed.netloc.lower()
    for tok in suspicious_tokens:
        if tok in host or tok in url.lower():
            return f"⚠️ Suspicious URL Detected: {url}"
    return f"✅ URL looks safe: {url}"

if __name__ == "__main__":
    try:
        print("TENANET URL Scam Detection (demo)\n")
        url = input("Enter a URL to scan: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n[SCAN-RESULT] No input provided (interrupted).")
        sys.exit(0)

    result = detect_url_attack(url)
    print(f"\n[Result] {result}")
    print(f"[SCAN-RESULT] URL | {result}")
