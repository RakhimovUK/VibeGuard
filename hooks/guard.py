#!/usr/bin/env python3
"""VibeGuard qo'riqchi rejimi (PreToolUse hook).

Fayl yozilishidan oldin yangi matnda token yoki kalit bor-yo'qligini tekshiradi.
- Aniq sir naqshi (bot tokeni, API kalit, DB paroli...) -> yozish to'xtatiladi (exit 2).
- Umumiy shubha (password = "...") -> foydalanuvchidan so'raladi.
- Faqat `.vibeguard/config.json` da "guard": true bo'lsa ishlaydi.
- AI chaqiruvi yo'q, tarmoq yo'q. Har qanday ichki xatoda yozishga xalaqit bermaydi.
"""
import fnmatch
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "skills", "vibeguard", "scripts"))

SKIP_KEYS = {"file_path", "notebook_path", "path", "old_string", "old_str"}

MESSAGES = {
    "uz": {
        "blocked": "VibeGuard qo'riqchi: yozish to'xtatildi. Yangi matnda sir bor",
        "how": "Sirni kodga yozma: muhit o'zgaruvchisidan o'qi (masalan os.environ / process.env) va qiymatni .env ga foydalanuvchi o'zi qo'ysin.",
        "env": "VibeGuard qo'riqchi: .env fayli .gitignore'da yo'q. Avval .gitignore'ga `.env` qo'sh, keyin yoz.",
        "ask": "VibeGuard qo'riqchi: bu matnda parol yoki kalitga o'xshash qiymat bor",
    },
    "uz-cyrl": {
        "blocked": "VibeGuard қўриқчи: ёзиш тўхтатилди. Янги матнда сир бор",
        "how": "Сирни кодга ёзма: муҳит ўзгарувчисидан ўқи ва қийматни .env га фойдаланувчи ўзи қўйсин.",
        "env": "VibeGuard қўриқчи: .env файли .gitignore'да йўқ. Аввал .gitignore'га `.env` қўш, кейин ёз.",
        "ask": "VibeGuard қўриқчи: бу матнда парол ёки калитга ўхшаш қиймат бор",
    },
    "ru": {
        "blocked": "VibeGuard страж: запись остановлена. В новом тексте есть секрет",
        "how": "Не пиши секрет в код: читай его из переменной окружения, а значение пусть пользователь сам положит в .env.",
        "env": "VibeGuard страж: файл .env не указан в .gitignore. Сначала добавь `.env` в .gitignore, потом пиши.",
        "ask": "VibeGuard страж: в тексте есть значение, похожее на пароль или ключ",
    },
    "en": {
        "blocked": "VibeGuard guard: write blocked. The new text contains a secret",
        "how": "Do not put the secret in code: read it from an environment variable and let the user place the value in .env themselves.",
        "env": "VibeGuard guard: .env is not listed in .gitignore. Add `.env` to .gitignore first, then write.",
        "ask": "VibeGuard guard: this text has a value that looks like a password or key",
    },
}


def strings(value, key=None):
    if key in SKIP_KEYS:
        return
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for k, v in value.items():
            yield from strings(v, k)
    elif isinstance(value, list):
        for v in value:
            yield from strings(v)


def env_ignored(project):
    try:
        with open(os.path.join(project, ".gitignore"), encoding="utf-8", errors="ignore") as fh:
            return bool(re.search(r"(?m)^\s*\*?\.env", fh.read()))
    except OSError:
        return False


def main():
    data = json.load(sys.stdin)
    project = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or "."
    try:
        with open(os.path.join(project, ".vibeguard", "config.json"), encoding="utf-8") as fh:
            config = json.load(fh)
    except (OSError, ValueError):
        return 0
    if not config.get("guard"):
        return 0

    from scan_secrets import COMPILED, PLACEHOLDER, mask

    msg = MESSAGES.get(config.get("lang"), MESSAGES["uz"])
    tool_input = data.get("tool_input") or {}
    path = str(tool_input.get("file_path") or tool_input.get("notebook_path") or "")
    try:
        rel = os.path.relpath(path, project).replace(os.sep, "/") if path else ""
    except ValueError:
        rel = path
    for pattern in config.get("guard_allow") or []:
        if fnmatch.fnmatch(rel, pattern):
            return 0

    base = os.path.basename(path)
    if base == ".env" or (base.startswith(".env.") and not base.endswith((".example", ".sample", ".template"))):
        if env_ignored(project):
            return 0  # sirlarning to'g'ri joyi
        print(msg["env"], file=sys.stderr)
        return 2

    strong, weak = [], []
    for text in strings(tool_input):
        for line in text.splitlines():
            spans = []
            for name, rx in COMPILED:
                for match in rx.finditer(line):
                    value = match.group(1) if match.groups() else match.group(0)
                    if name == "generic_secret" and PLACEHOLDER.match(value):
                        continue
                    span = match.span()
                    if any(s[0] < span[1] and span[0] < s[1] for s in spans):
                        continue
                    spans.append(span)
                    shown = "***" if name == "db_url_with_password" else mask(value)
                    (weak if name == "generic_secret" else strong).append(f"{name} ({shown})")

    where = f" [{rel}]" if rel else ""
    if strong:
        try:  # qizil va ko'k hisob uchun: nechta sir to'xtatildi
            stats_path = os.path.join(project, ".vibeguard", "guard-stats.json")
            try:
                with open(stats_path, encoding="utf-8") as fh:
                    stats = json.load(fh)
            except (OSError, ValueError):
                stats = {}
            stats["blocked"] = int(stats.get("blocked", 0)) + 1
            with open(stats_path, "w", encoding="utf-8") as fh:
                json.dump(stats, fh)
        except Exception:
            pass
        print(f"{msg['blocked']}{where}: {', '.join(sorted(set(strong))[:5])}. {msg['how']}", file=sys.stderr)
        return 2
    if weak:
        json.dump({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": f"{msg['ask']}{where}: {', '.join(sorted(set(weak))[:5])}",
        }}, sys.stdout, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    try:
        code = main()
    except Exception:  # qo'riqchi hech qachon ishni buzmasligi kerak
        code = 0
    sys.exit(code)
