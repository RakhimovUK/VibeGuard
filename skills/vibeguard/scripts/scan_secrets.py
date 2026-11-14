#!/usr/bin/env python3
"""VibeGuard: sirlarni qidiradi (token, kalit, parol). Faqat o'qiydi.

Ishlatish: python3 scan_secrets.py <papka>
Natija: JSON. Sirlar yashirib chiqariladi (birinchi va oxirgi 4 belgi).
"""
import json
import os
import re
import sys

SKIP_DIRS = {".git", "node_modules", "venv", ".venv", "__pycache__", "dist",
             "build", ".next", ".vibeguard", "vendor", ".gradle", "Pods"}
SKIP_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip",
            ".gz", ".jar", ".apk", ".so", ".dll", ".exe", ".woff", ".woff2",
            ".ttf", ".mp3", ".mp4", ".lock"}
MAX_BYTES = 1_000_000

PATTERNS = [
    ("telegram_bot_token", r"\b\d{8,10}:[A-Za-z0-9_-]{35}\b"),
    ("ai_api_key", r"\bsk-[A-Za-z0-9_-]{20,}"),
    ("aws_access_key", r"\bAKIA[0-9A-Z]{16}\b"),
    ("github_token", r"\bgh[pousr]_[A-Za-z0-9]{36,}"),
    ("jwt_or_supabase_key", r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"),
    ("private_key", r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    ("db_url_with_password", r"\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis)://[^:\s/'\"]+:[^@\s'\"]+@"),
    ("generic_secret", r"(?i)(?:password|passwd|secret|api_?key|token)\w*\s*[:=]\s*['\"]([^'\"\s]{8,})['\"]"),
]
COMPILED = [(name, re.compile(rx)) for name, rx in PATTERNS]
PLACEHOLDER = re.compile(r"(?i)^(?:your|change|example|xxx|todo|<|\$\{|process\.env|os\.environ)|^.*\.\.\.")


def mask(value):
    value = value.strip()
    if len(value) <= 10:
        return value[:2] + "..."
    return value[:4] + "..." + value[-4:]


def scan_file(path, root):
    try:
        if os.path.getsize(path) > MAX_BYTES:
            return []
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            lines = fh.readlines()
    except OSError:
        return []
    found = []
    for number, line in enumerate(lines, 1):
        seen_spans = []
        for name, rx in COMPILED:
            for match in rx.finditer(line):
                value = match.group(1) if match.groups() else match.group(0)
                if name == "generic_secret" and PLACEHOLDER.match(value):
                    continue
                span = match.span()
                if any(s[0] < span[1] and span[0] < s[1] for s in seen_spans):
                    continue  # aniqroq naqsh allaqachon topgan
                seen_spans.append(span)
                found.append({
                    "type": name,
                    "file": os.path.relpath(path, root),
                    "line": number,
                    # DB manzilida parolning hech bir belgisi chiqmasin
                    "masked": (value.split("://")[0] + "://***:***@"
                               if name == "db_url_with_password" else mask(value)),
                })
    return found


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    findings = []
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if os.path.splitext(name)[1].lower() in SKIP_EXT:
                continue
            findings.extend(scan_file(os.path.join(current, name), root))
    json.dump({"tool": "scan_secrets", "count": len(findings), "findings": findings},
              sys.stdout, indent=2, ensure_ascii=False)
    print()


if __name__ == "__main__":
    main()
