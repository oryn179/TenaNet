#!/usr/bin/env python3
"""
Parse a folder of raw emails (RFC822 / .eml style files) and save CSV with columns:
"text","label"

Usage:
  python3 parse_emails_to_csv.py --input-dir easy_ham --output data/easy_ham.csv --label real
"""
import os, sys, argparse, csv, email
from email import policy
from email.parser import BytesParser
import html
import re

def extract_text_from_message(msg):
    # prefer text/plain parts; fallback to extracting text from html
    if msg.is_multipart():
        parts = msg.walk()
    else:
        parts = [msg]

    text_parts = []
    html_parts = []

    for part in parts:
        ctype = part.get_content_type()
        try:
            payload = part.get_payload(decode=True)
        except Exception:
            payload = None
        if payload:
            try:
                text = payload.decode(part.get_content_charset() or 'utf-8', errors='replace')
            except Exception:
                # fallback
                text = payload.decode('utf-8', errors='replace') if isinstance(payload, (bytes, bytearray)) else str(payload)
            if ctype == 'text/plain':
                text_parts.append(text)
            elif ctype == 'text/html':
                html_parts.append(text)

    if text_parts:
        return "\n".join(text_parts).strip()
    if html_parts:
        # strip tags roughly
        html_text = "\n".join(html_parts)
        # naive html->text: remove tags
        text = re.sub(r'<script.*?>.*?</script>', '', html_text, flags=re.S|re.I)
        text = re.sub(r'<style.*?>.*?</style>', '', text, flags=re.S|re.I)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = html.unescape(text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    # no body found, try subject
    subj = msg.get('subject') or ''
    return (subj or '').strip()

def parse_file(path):
    try:
        with open(path, 'rb') as f:
            msg = BytesParser(policy=policy.default).parse(f)
        subject = msg.get('subject') or ''
        body = extract_text_from_message(msg)
        # combine subject + body
        text = (subject.strip() + "\n\n" + body.strip()).strip()
        # reduce whitespace
        text = re.sub(r'\s+', ' ', text)
        return text
    except Exception as e:
        # print(f"Warning: failed to parse {path}: {e}", file=sys.stderr)
        return None

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input-dir', required=True, help='Folder with raw email files')
    p.add_argument('--output', required=True, help='Output CSV path')
    p.add_argument('--label', default='real', help='Label to write for each row (real/fake)')
    args = p.parse_args()

    files = []
    for root, _, filenames in os.walk(args.input_dir):
        for name in filenames:
            files.append(os.path.join(root, name))
    files.sort()
    if not files:
        print("No files found in", args.input_dir, file=sys.stderr)
        sys.exit(2)

    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)

    with open(args.output, 'w', newline='', encoding='utf-8') as csvf:
        writer = csv.writer(csvf)
        writer.writerow(['text','label'])
        for i, fpath in enumerate(files, 1):
            text = parse_file(fpath)
            if text and len(text.strip())>0:
                # truncate to a reasonable length (optional)
                writer.writerow([text[:10000], args.label])
            if i % 500 == 0:
                print(f"Processed {i} files...", flush=True)

    print("Saved", args.output)

if __name__ == '__main__':
    main()
