#!/usr/bin/env python3
"""VibeGuard: skriptlarni sinov loyihalarida tekshiradi (aniqlik ko'rsatkichi).

Ishlatish: python3 selftest.py
fixtures/expected.json dagi "detector": "script" bandlari topilganini tekshiradi.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
FIXTURES = os.path.join(ROOT, "fixtures")


def run(script, target):
    out = subprocess.run([sys.executable, os.path.join(HERE, script), target],
                         capture_output=True, text=True, timeout=60)
    return json.loads(out.stdout)["findings"]


def main():
    with open(os.path.join(FIXTURES, "expected.json"), encoding="utf-8") as fh:
        expected = json.load(fh)["planted"]
    found = run("scan_secrets.py", FIXTURES) + run("check_hygiene.py", FIXTURES)
    # Git repo ichida .env "tracked" bo'lib chiqadi: sinov uchun ikkalasi bir xil.
    alias = {"env_file_tracked": "env_file_present"}
    index = {(alias.get(f["type"], f["type"]), f["file"].replace(os.sep, "/")) for f in found}

    script_items = [e for e in expected if e["detector"] == "script"]
    missed = [e for e in script_items if (e["type"], e["file"]) not in index]
    expected_keys = {(e["type"], e["file"]) for e in script_items}
    extra = sorted(k for k in index if k not in expected_keys)

    print(f"Skript topishi kerak: {len(script_items)}")
    print(f"Topildi: {len(script_items) - len(missed)}")
    print(f"O'tkazib yuborildi: {len(missed)}")
    for e in missed:
        print(f"  - {e['id']}: {e['type']} @ {e['file']}")
    print(f"Kutilmagan (ortiqcha) topilma: {len(extra)}")
    for kind, file in extra:
        print(f"  + {kind} @ {file}")
    agent_items = [e for e in expected if e["detector"] == "agent"]
    print(f"Faqat agentlar topadigan (bu yerda tekshirilmaydi): {len(agent_items)}")
    sys.exit(1 if missed else 0)


if __name__ == "__main__":
    main()
