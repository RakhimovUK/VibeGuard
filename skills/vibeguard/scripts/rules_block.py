#!/usr/bin/env python3
"""VibeGuard: audit topilmalari asosida loyiha qoidalarini CLAUDE.md ga yozadi.

Ishlatish:
  python3 rules_block.py [--store .vibeguard/findings.json] [--file CLAUDE.md] [--dry-run]

Faqat belgilangan blokni yozadi yoki yangilaydi:
  <!-- vibeguard:start --> ... <!-- vibeguard:end -->
Blokdan tashqaridagi matnga tegmaydi. Ochiq va tuzatilgan topilmalarning qoidalari
kiradi (xato takrorlanmasligi uchun). Qoida matni rules/ fayllaridagi `lesson:` dan olinadi.
"""
import argparse
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
START, END = "<!-- vibeguard:start -->", "<!-- vibeguard:end -->"


def lessons(rules_dir):
    out = {}
    for path in glob.glob(os.path.join(rules_dir, "*", "*.md")):
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        rid = re.search(r"^id:\s*(.+)$", text, re.M)
        lesson = re.search(r'^lesson:\s*"?(.*?)"?\s*$', text, re.M)
        if rid and lesson:
            out[rid.group(1).strip()] = lesson.group(1).strip()
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--store", default=".vibeguard/findings.json")
    p.add_argument("--file", default="CLAUDE.md")
    p.add_argument("--rules-dir", default=os.path.join(HERE, "..", "rules"))
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()

    try:
        with open(a.store, encoding="utf-8") as fh:
            store = json.load(fh)
    except (OSError, ValueError):
        print(json.dumps({"error": "findings store not found", "store": a.store}))
        sys.exit(1)

    known = lessons(a.rules_dir)
    used, unknown = [], []
    for f in store.get("findings", []):
        rid = f.get("rule", "")
        if f.get("status") == "taxmin":
            continue
        if rid in known and rid not in used:
            used.append(rid)
        elif rid and rid not in known and rid not in unknown:
            unknown.append(rid)
    used.sort()

    if not used:
        print(json.dumps({"written": False, "reason": "no confirmed findings with a known rule",
                          "unknown_rules": unknown}, ensure_ascii=False))
        return

    lines = [START, "## Security rules (VibeGuard)", "",
             "Generated from this project's audit findings by `/vibeguard:rules`. "
             "Do not edit inside this block; it is rewritten on the next run.", ""]
    lines += [f"- {known[rid]} (`{rid}`)" for rid in used]
    lines.append(END)
    block = "\n".join(lines)

    try:
        with open(a.file, encoding="utf-8") as fh:
            current = fh.read()
    except OSError:
        current = ""
    if START in current and END in current:
        head, rest = current.split(START, 1)
        tail = rest.split(END, 1)[1]
        updated = head + block + tail
    else:
        updated = (current.rstrip("\n") + "\n\n" if current.strip() else "") + block + "\n"

    changed = updated != current
    if changed and not a.dry_run:
        with open(a.file, "w", encoding="utf-8") as fh:
            fh.write(updated)
    print(json.dumps({"written": changed and not a.dry_run, "would_change": changed, "file": a.file,
                      "rules": used, "unknown_rules": unknown, "block": block}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
