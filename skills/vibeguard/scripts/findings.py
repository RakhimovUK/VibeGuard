#!/usr/bin/env python3
"""VibeGuard: topilmalar xotirasi va xavf bali.

Ishlatish:
  python3 findings.py merge <yangi.json> [--store .vibeguard/findings.json] [--partial]
  python3 findings.py score [--store .vibeguard/findings.json]
  python3 findings.py resolve VG-001 [VG-002 ...]   (qayta hujumda yopilgani tasdiqlansa)
  python3 findings.py top3      (bugun 3 ta ish)
  python3 findings.py budget    (hujumchi 10 daqiqada / 1 kunda / 1 haftada nimaga yetadi)
  python3 findings.py board     (qizil va ko'k hisob)

Qo'shimcha maydonlar: "level": "havaskor|tajribali|maqsadli", "breaks_chain": true|false

<yangi.json>: topilmalar ro'yxati. Har biri:
  {"rule": "webapp-idor", "file": "src/api.js", "line": 42,
   "severity": "kritik|yuqori|o'rta|past", "status": "tasdiqlandi|taxmin",
   "title": "...", "snippet": "kod parchasi (sirsiz)", "agent": "attacker-user"}

Doimiy ID: qoida + fayl + kod parchasi (bo'shliqlarsiz) bo'yicha barmoq izi.
Qator raqami o'zgarsa ham ID saqlanadi.

--partial: tekshiruv to'liq emas (quick, ship, fix). Bu safar topilmagan eski
topilmalar "tuzatildi" deb belgilanmaydi.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import sys

WEIGHTS = {"kritik": 40, "yuqori": 15, "o'rta": 5, "past": 1}
ALIASES = {"critical": "kritik", "high": "yuqori", "medium": "o'rta", "low": "past",
           "orta": "o'rta", "o`rta": "o'rta", "oʻrta": "o'rta"}
CHAIN_BONUS = 10
CHAIN_BONUS_MAX = 20
NOT_READY_SCORE = 30

# Hujumchi darajasi: kim uddalay oladi va taxminan qancha vaqtda.
LEVELS = ["havaskor", "tajribali", "maqsadli"]
LEVEL_ALIASES = {"beginner": "havaskor", "amateur": "havaskor", "script-kiddie": "havaskor", "easy": "havaskor",
                 "skilled": "tajribali", "experienced": "tajribali", "medium": "tajribali",
                 "targeted": "maqsadli", "expert": "maqsadli", "hard": "maqsadli"}
BUDGET = {"havaskor": "10 daqiqa", "tajribali": "1 kun", "maqsadli": "1 hafta"}


def level(value):
    value = str(value or "").strip().lower()
    value = LEVEL_ALIASES.get(value, value)
    return value if value in LEVELS else "tajribali"


def _brief(f):
    return {"id": f["id"], "severity": f["severity"], "level": f.get("level", "tajribali"),
            "title": f.get("title", ""), "file": f.get("file", ""), "line": f.get("line"),
            "rule": f.get("rule", ""), "breaks_chain": bool(f.get("breaks_chain"))}


def _open_confirmed(store):
    return [f for f in store["findings"] if f["state"] == "open" and f.get("status") != "taxmin"]


def top3(store):
    """Bugun 3 ta ish: eng og'ir, zanjirni uzadigan, eng oson ishlatiladigan birinchi."""
    items = sorted(_open_confirmed(store), key=lambda f: (
        -WEIGHTS[f["severity"]], not f.get("breaks_chain"),
        LEVELS.index(f.get("level", "tajribali")), f["id"]))
    return {"top3": [_brief(f) for f in items[:3]]}


def budget(store):
    """Vaqt byudjeti: hujumchi 10 daqiqada, 1 kunda, 1 haftada nimaga yetadi (jamlanib boradi)."""
    out, reachable = [], []
    for name in LEVELS:
        reachable += [f for f in _open_confirmed(store) if f.get("level", "tajribali") == name]
        ordered = sorted(reachable, key=lambda f: (-WEIGHTS[f["severity"]], f["id"]))
        out.append({"time": BUDGET[name], "level": name, "count": len(ordered),
                    "worst": ordered[0]["severity"] if ordered else None,
                    "findings": [f["id"] for f in ordered]})
    return {"budget": out}


def board(store, store_path):
    """Qizil va ko'k hisob: qizil = ochiq topilmalar, ko'k = tuzatilganlar + qo'riqchi to'xtatganlari."""
    blocked = 0
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(store_path)), "guard-stats.json"),
                  encoding="utf-8") as fh:
            blocked = int(json.load(fh).get("blocked", 0))
    except (OSError, ValueError):
        pass
    fixed = sum(1 for f in store["findings"] if f["state"] == "fixed")
    red = sum(1 for f in store["findings"] if f["state"] == "open")
    history = [{"at": r["at"], "score": r["score"]} for r in store.get("runs", [])[-10:]]
    return {"red": red, "blue": fixed + blocked, "blue_fixed": fixed, "blue_guard_blocked": blocked,
            "score_history": history}


def severity(value):
    value = str(value or "").strip().lower()
    value = ALIASES.get(value, value)
    return value if value in WEIGHTS else "o'rta"


def fingerprint(item):
    body = re.sub(r"\s+", "", item.get("snippet") or item.get("title") or "")
    raw = "|".join([item.get("rule", ""), item.get("file", "").replace("\\", "/"), body])
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]


def load(path):
    if not os.path.exists(path):
        return {"next_id": 1, "findings": [], "chains": 0, "runs": []}
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def save(path, store):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(store, fh, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def score(store):
    total = 0.0
    counts = {k: 0 for k in WEIGHTS}
    confirmed_critical = 0
    open_items = [f for f in store["findings"] if f["state"] == "open"]
    for f in open_items:
        confirmed = f.get("status") != "taxmin"
        total += WEIGHTS[f["severity"]] * (1.0 if confirmed else 0.5)
        counts[f["severity"]] += 1
        if confirmed and f["severity"] == "kritik":
            confirmed_critical += 1
    total += min(int(store.get("chains", 0)) * CHAIN_BONUS, CHAIN_BONUS_MAX) if open_items else 0
    value = min(100, int(round(total)))
    ready = confirmed_critical == 0 and value < NOT_READY_SCORE
    return {"score": value, "verdict": "tayyor" if ready else "tayyor emas",
            "open": len(open_items), "by_severity": counts,
            "fixed_total": sum(1 for f in store["findings"] if f["state"] == "fixed")}


def merge(store, incoming, partial, chains):
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    by_fp = {f["fingerprint"]: f for f in store["findings"]}
    seen, new_ids, reopened = set(), [], []
    for item in incoming:
        fp = fingerprint(item)
        if fp in seen:
            continue
        seen.add(fp)
        fields = {
            "rule": item.get("rule", ""), "file": item.get("file", "").replace("\\", "/"),
            "line": item.get("line"), "severity": severity(item.get("severity")),
            "status": "taxmin" if item.get("status") == "taxmin" else "tasdiqlandi",
            "title": item.get("title", ""), "agent": item.get("agent", ""),
            "level": level(item.get("level")), "breaks_chain": bool(item.get("breaks_chain")),
        }
        if fp in by_fp:
            old = by_fp[fp]
            if old["state"] == "fixed":
                reopened.append(old["id"])
            old.update(fields, state="open", last_seen=now)
        else:
            entry = {"id": "VG-%03d" % store["next_id"], "fingerprint": fp,
                     "state": "open", "first_seen": now, "last_seen": now, **fields}
            store["next_id"] += 1
            store["findings"].append(entry)
            new_ids.append(entry["id"])
    fixed_ids = []
    if not partial:
        for f in store["findings"]:
            if f["state"] == "open" and f["fingerprint"] not in seen:
                f["state"] = "fixed"
                f["fixed_at"] = now
                fixed_ids.append(f["id"])
        store["chains"] = chains
    elif chains is not None and chains > 0:
        store["chains"] = chains
    remaining = [f["id"] for f in store["findings"]
                 if f["state"] == "open" and f["id"] not in new_ids and f["id"] not in reopened]
    result = {"new": new_ids, "reopened": reopened, "fixed": fixed_ids,
              "remaining": remaining, **score(store)}
    store["runs"].append({"at": now, "partial": partial, "score": result["score"],
                          "new": len(new_ids), "fixed": len(fixed_ids)})
    store["runs"] = store["runs"][-50:]
    return result


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("merge")
    m.add_argument("incoming")
    m.add_argument("--store", default=".vibeguard/findings.json")
    m.add_argument("--partial", action="store_true")
    m.add_argument("--chains", type=int, default=None, help="tasdiqlangan hujum zanjirlari soni")
    s = sub.add_parser("score")
    s.add_argument("--store", default=".vibeguard/findings.json")
    r = sub.add_parser("resolve", help="qayta hujumda yopilgani tasdiqlangan topilmalar")
    r.add_argument("ids", nargs="+")
    r.add_argument("--store", default=".vibeguard/findings.json")
    for name in ("top3", "budget", "board"):
        sub.add_parser(name).add_argument("--store", default=".vibeguard/findings.json")
    args = parser.parse_args()

    store = load(args.store)
    if args.cmd == "score":
        result = score(store)
    elif args.cmd == "top3":
        result = top3(store)
    elif args.cmd == "budget":
        result = budget(store)
    elif args.cmd == "board":
        result = board(store, args.store)
    elif args.cmd == "resolve":
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        wanted = {i.upper() for i in args.ids}
        done = []
        for f in store["findings"]:
            if f["id"] in wanted and f["state"] == "open":
                f["state"], f["fixed_at"] = "fixed", now
                done.append(f["id"])
        save(args.store, store)
        result = {"fixed": done, "not_found_or_already_fixed": sorted(wanted - set(done)), **score(store)}
    else:
        with open(args.incoming, encoding="utf-8") as fh:
            incoming = json.load(fh)
        if isinstance(incoming, dict):
            incoming = incoming.get("findings", [])
        chains = args.chains if args.chains is not None else (None if args.partial else 0)
        result = merge(store, incoming, args.partial, chains)
        save(args.store, store)
    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    print()


if __name__ == "__main__":
    main()
