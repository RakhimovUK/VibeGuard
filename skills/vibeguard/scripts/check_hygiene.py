#!/usr/bin/env python3
"""VibeGuard: repo gigiyenasi (.gitignore, .env, bog'liqliklar, Docker). Faqat o'qiydi.

Ishlatish: python3 check_hygiene.py <papka>
Natija: JSON.
"""
import json
import os
import re
import subprocess
import sys

SKIP_DIRS = {".git", "node_modules", "venv", ".venv", "__pycache__", "dist",
             "build", ".next", ".vibeguard", "vendor"}
SECRET_NAME = re.compile(r"(?i)(token|secret|password|passwd|api_?key|private)")


def read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            return fh.read()
    except OSError:
        return ""


def tracked_files(root):
    """Git kuzatayotgan fayllar. Git repo bo'lmasa None."""
    try:
        out = subprocess.run(["git", "-C", root, "ls-files"], capture_output=True,
                             text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    return set(out.stdout.splitlines())


def check_dir(path, root, tracked, add):
    rel = lambda name: os.path.relpath(os.path.join(path, name), root)
    names = set(os.listdir(path))

    for name in sorted(names):
        if name == ".env" or (name.startswith(".env.") and not name.endswith((".example", ".sample", ".template"))):
            if tracked is None:
                add("env_file_present", rel(name), "Sirlar fayli bor. Git'ga tushmasligini tekshiring.")
            elif rel(name) in tracked:
                add("env_file_tracked", rel(name), "Sirlar fayli git'da kuzatilmoqda.")

    if "package.json" in names:
        try:
            pkg = json.loads(read(os.path.join(path, "package.json")) or "{}")
        except ValueError:
            pkg = {}
        if not names & {"package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lockb"}:
            add("no_lockfile", rel("package.json"), "Lock fayl yo'q: har o'rnatishda boshqa versiya kelishi mumkin.")
        for section in ("dependencies", "devDependencies"):
            for dep, version in (pkg.get(section) or {}).items():
                if str(version).strip() in ("*", "latest", ""):
                    add("unpinned_dependency", rel("package.json"), f"{dep}: versiya qotirilmagan ({version}).")

    if "requirements.txt" in names:
        for number, line in enumerate(read(os.path.join(path, "requirements.txt")).splitlines(), 1):
            line = line.split("#")[0].strip()
            if line and not line.startswith("-") and "==" not in line and "@" not in line:
                add("unpinned_dependency", rel("requirements.txt"), f"{line}: versiya qotirilmagan.", number)

    for name in sorted(n for n in names if n == "Dockerfile" or n.startswith("Dockerfile.")):
        text = read(os.path.join(path, name))
        lines = text.splitlines()
        if not re.search(r"(?im)^\s*USER\s+(?!root\b)\S+", text):
            add("docker_root_user", rel(name), "USER yo'q: konteyner root bilan ishlaydi.")
        for number, line in enumerate(lines, 1):
            m = re.match(r"(?i)\s*(ENV|ARG)\s+([A-Za-z_][A-Za-z0-9_]*)\s*[= ]\s*(\S+)", line)
            if m and SECRET_NAME.search(m.group(2)) and not m.group(3).startswith("$"):
                add("docker_secret_in_image", rel(name), f"{m.group(2)}: sir tasvir ichiga yozilgan.", number)
            if re.match(r"(?i)\s*COPY\s+.*\.env\b", line):
                add("docker_copies_env", rel(name), ".env tasvirga ko'chirilmoqda.", number)
            f = re.match(r"(?i)\s*FROM\s+(\S+)", line)
            if f and (f.group(1).endswith(":latest") or (":" not in f.group(1) and "@" not in f.group(1) and f.group(1).lower() != "scratch")):
                add("docker_unpinned_base", rel(name), f"{f.group(1)}: asos tasvir versiyasi qotirilmagan.", number)
        if ".dockerignore" not in names:
            add("no_dockerignore", rel(name), ".dockerignore yo'q: .env va .git tasvirga tushishi mumkin.")


def main():
    root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    findings = []

    def add(kind, file, note, line=None):
        item = {"type": kind, "file": file, "note": note}
        if line:
            item["line"] = line
        findings.append(item)

    tracked = tracked_files(root)
    gitignore = read(os.path.join(root, ".gitignore"))
    if not gitignore:
        add("no_gitignore", ".gitignore", ".gitignore yo'q.")
    elif not re.search(r"(?m)^\s*\*?\.env", gitignore):
        add("env_not_ignored", ".gitignore", ".env .gitignore'da ko'rsatilmagan.")

    for current, dirs, _files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        check_dir(current, root, tracked, add)

    json.dump({"tool": "check_hygiene", "git_repo": tracked is not None,
               "count": len(findings), "findings": findings},
              sys.stdout, indent=2, ensure_ascii=False)
    print()


if __name__ == "__main__":
    main()
