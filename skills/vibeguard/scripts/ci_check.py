#!/usr/bin/env python3
"""VibeGuard: CI uchun tezkor tekshiruv (AI'siz). Sir topilsa xato kodi bilan tugaydi.

Ishlatish:
  python3 ci_check.py <papka> [--exclude "fixtures/*"] [--exclude "tests/data/*"]

Markdown xulosa chiqaradi (GitHub'da $GITHUB_STEP_SUMMARY ga ham yozadi).
Chiqish kodi: 1 = sir topildi; 0 = sir yo'q (gigiyena ogohlantirishlari to'xtatmaydi).
Hujumchi agentlar CI'da ishlamaydi: bu faqat skriptlar qatlami.
"""
import argparse
import fnmatch
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def run(script, target):
    out = subprocess.run([sys.executable, os.path.join(HERE, script), target],
                         capture_output=True, text=True, timeout=300)
    return json.loads(out.stdout)["findings"]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("target", nargs="?", default=".")
    p.add_argument("--exclude", action="append", default=[])
    a = p.parse_args()

    def keep(f):
        path = f["file"].replace(os.sep, "/")
        return not any(fnmatch.fnmatch(path, pat) for pat in a.exclude)

    secrets = [f for f in run("scan_secrets.py", a.target) if keep(f)]
    hygiene = [f for f in run("check_hygiene.py", a.target) if keep(f)]

    lines = ["## VibeGuard", ""]
    if secrets:
        lines += [f"**Sirlar topildi: {len(secrets)}** (qiymatlar yashirilgan)", "",
                  "| Tur | Fayl | Qator | Qiymat |", "|---|---|---|---|"]
        lines += [f"| {f['type']} | `{f['file']}` | {f['line']} | `{f['masked']}` |" for f in secrets[:50]]
        lines += ["", "Sirni koddan o'chirish yetarli emas: uni provayder panelida almashtiring."]
    else:
        lines.append("Sirlar topilmadi.")
    lines.append("")
    if hygiene:
        lines += [f"Ogohlantirishlar: {len(hygiene)}", "", "| Tur | Fayl | Izoh |", "|---|---|---|"]
        lines += [f"| {f['type']} | `{f['file']}` | {f['note']} |" for f in hygiene[:50]]
    else:
        lines.append("Gigiyena ogohlantirishlari yo'q.")
    lines += ["", "_Bu faqat skriptlar qatlami. To'liq tekshiruv: Claude Code'da `/vibeguard:redteam`._"]
    text = "\n".join(lines) + "\n"
    print(text)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as fh:
            fh.write(text)
    sys.exit(1 if secrets else 0)


if __name__ == "__main__":
    main()
