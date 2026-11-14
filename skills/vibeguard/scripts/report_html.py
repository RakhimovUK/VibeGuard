#!/usr/bin/env python3
"""VibeGuard: topilmalar xotirasidan bitta faylli HTML hisobot yasaydi.

Ishlatish:
  python3 report_html.py [--store .vibeguard/findings.json]
                         [--out .vibeguard/reports/report.html]
                         [--lang uz|uz-cyrl|ru|en] [--title "Loyiha nomi"]

Fayl tashqi resurs yuklamaydi. Sir qiymatlari xotirada saqlanmaydi, shuning uchun
hisobotda ham yo'q. Baribir ulashishdan oldin ko'zdan kechiring: fayl yo'llari va
topilma sarlavhalari loyiha tuzilishini ochib beradi.
"""
import argparse
import datetime
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from findings import load, score, top3  # noqa: E402

L = {
    "uz": {"title": "VibeGuard hisoboti", "score": "Xavf bali", "ready": "Chiqarishga tayyor",
           "notready": "Tayyor emas", "open": "Ochiq", "fixed": "Tuzatildi", "all": "Hammasi",
           "id": "ID", "sev": "Xavf", "what": "Topilma", "where": "Qayerda", "rule": "Qoida",
           "state": "Holat", "guess": "taxmin", "none": "Topilma yo'q.",
           "note": "Bal faqat topilgan xatolarni o'lchaydi, xavfsizlik kafolati emas.",
           "sevs": {"kritik": "kritik", "yuqori": "yuqori", "o'rta": "o'rta", "past": "past"}},
    "uz-cyrl": {"title": "VibeGuard ҳисоботи", "score": "Хавф бали", "ready": "Чиқаришга тайёр",
                "notready": "Тайёр эмас", "open": "Очиқ", "fixed": "Тузатилди", "all": "Ҳаммаси",
                "id": "ID", "sev": "Хавф", "what": "Топилма", "where": "Қаерда", "rule": "Қоида",
                "state": "Ҳолат", "guess": "тахмин", "none": "Топилма йўқ.",
                "note": "Бал фақат топилган хатоларни ўлчайди, хавфсизлик кафолати эмас.",
                "sevs": {"kritik": "критик", "yuqori": "юқори", "o'rta": "ўрта", "past": "паст"}},
    "ru": {"title": "Отчёт VibeGuard", "score": "Балл риска", "ready": "Готов к выпуску",
           "notready": "Не готов", "open": "Открыто", "fixed": "Исправлено", "all": "Все",
           "id": "ID", "sev": "Серьёзность", "what": "Находка", "where": "Где", "rule": "Правило",
           "state": "Статус", "guess": "предположение", "none": "Находок нет.",
           "note": "Балл измеряет только найденные ошибки и не является гарантией безопасности.",
           "sevs": {"kritik": "критическая", "yuqori": "высокая", "o'rta": "средняя", "past": "низкая"}},
    "en": {"title": "VibeGuard report", "score": "Risk score", "ready": "Ready to ship",
           "notready": "Not ready", "open": "Open", "fixed": "Fixed", "all": "All",
           "id": "ID", "sev": "Severity", "what": "Finding", "where": "Where", "rule": "Rule",
           "state": "State", "guess": "unconfirmed", "none": "No findings.",
           "note": "The score only measures the issues found; it is not a guarantee of security.",
           "sevs": {"kritik": "critical", "yuqori": "high", "o'rta": "medium", "past": "low"}},
}
L["uz"].update(top3="Bugun 3 ta ish", levels={"havaskor": "havaskor", "tajribali": "tajribali", "maqsadli": "maqsadli"})
L["uz-cyrl"].update(top3="Бугун 3 та иш", levels={"havaskor": "ҳаваскор", "tajribali": "тажрибали", "maqsadli": "мақсадли"})
L["ru"].update(top3="Три дела на сегодня", levels={"havaskor": "любитель", "tajribali": "опытный", "maqsadli": "целевой"})
L["en"].update(top3="Three things to do today", levels={"havaskor": "amateur", "tajribali": "skilled", "maqsadli": "targeted"})
ORDER = {"kritik": 0, "yuqori": 1, "o'rta": 2, "past": 3}
SEV_CLASS = {"kritik": "s0", "yuqori": "s1", "o'rta": "s2", "past": "s3"}

CSS = """
:root{color-scheme:light dark;--bg:#fff;--fg:#1a1a1a;--mut:#666;--line:#e3e3e3;--card:#f6f6f6}
@media(prefers-color-scheme:dark){:root{--bg:#141414;--fg:#eee;--mut:#9a9a9a;--line:#2e2e2e;--card:#1e1e1e}}
*{box-sizing:border-box}body{margin:0;padding:20px;background:var(--bg);color:var(--fg);
font:15px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
main{max-width:900px;margin:0 auto}h1{font-size:22px;margin:0 0 4px}.mut{color:var(--mut);font-size:13px}
.top{display:flex;gap:12px;flex-wrap:wrap;margin:16px 0}
.box{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 16px;min-width:120px}
.box b{display:block;font-size:26px;line-height:1.2}.bad b{color:#c62828}.ok b{color:#2e7d32}
.filters{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}
button{font:inherit;padding:6px 12px;border-radius:999px;border:1px solid var(--line);
background:var(--card);color:var(--fg);cursor:pointer}button[aria-pressed=true]{background:var(--fg);color:var(--bg)}
.item{border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin:8px 0}
.item h2{font-size:16px;margin:4px 0}.row{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.tag{font-size:12px;padding:2px 8px;border-radius:999px;border:1px solid var(--line)}
.s0{background:#c62828;color:#fff;border-color:#c62828}.s1{background:#e65100;color:#fff;border-color:#e65100}
.s2{background:#f9a825;color:#1a1a1a;border-color:#f9a825}.s3{background:#757575;color:#fff;border-color:#757575}
code{font:13px ui-monospace,Menlo,Consolas,monospace;word-break:break-all}.fixed{opacity:.6}
[hidden]{display:none}
"""

JS = """
const state={sev:'all',st:'open'};
function apply(){document.querySelectorAll('.item').forEach(e=>{
e.hidden=!((state.sev==='all'||e.dataset.sev===state.sev)&&(state.st==='all'||e.dataset.st===state.st));});
document.querySelectorAll('button[data-k]').forEach(b=>b.setAttribute('aria-pressed',state[b.dataset.k]===b.dataset.v));}
document.querySelectorAll('button[data-k]').forEach(b=>b.addEventListener('click',()=>{state[b.dataset.k]=b.dataset.v;apply();}));
apply();
"""


def build(store, lang, title):
    t = L.get(lang, L["uz"])
    e = html.escape
    result = score(store)
    ready = result["verdict"] == "tayyor"
    items = sorted(store["findings"], key=lambda f: (f["state"] != "open", ORDER.get(f["severity"], 9), f["id"]))
    out = ["<!DOCTYPE html>", f'<html lang="{e(lang)}"><head><meta charset="utf-8">',
           '<meta name="viewport" content="width=device-width,initial-scale=1">',
           f"<title>{e(t['title'])}</title><style>{CSS}</style></head><body><main>",
           f"<h1>{e(t['title'])}{': ' + e(title) if title else ''}</h1>",
           f'<div class="mut">{e(datetime.date.today().isoformat())}</div>',
           '<div class="top">',
           f'<div class="box {"ok" if ready else "bad"}"><span class="mut">{e(t["score"])}</span><b>{result["score"]}/100</b>'
           f'{e(t["ready"] if ready else t["notready"])}</div>',
           f'<div class="box"><span class="mut">{e(t["open"])}</span><b>{result["open"]}</b></div>',
           f'<div class="box"><span class="mut">{e(t["fixed"])}</span><b>{result["fixed_total"]}</b></div>',
           "</div>", f'<p class="mut">{e(t["note"])}</p>']
    picks = top3(store)["top3"]
    if picks:
        out.append(f'<div class="box"><span class="mut">{e(t["top3"])}</span><ol>')
        for f in picks:
            out.append(f'<li><b>{e(f["id"])}</b> {e(f["title"] or f["rule"])} '
                       f'<span class="tag {SEV_CLASS.get(f["severity"], "s2")}">{e(t["sevs"].get(f["severity"], f["severity"]))}</span></li>')
        out.append("</ol></div>")
    out.append('<div class="filters">')
    out.append(f'<button data-k="st" data-v="open">{e(t["open"])}</button>'
               f'<button data-k="st" data-v="fixed">{e(t["fixed"])}</button>'
               f'<button data-k="st" data-v="all">{e(t["all"])}</button>')
    out.append('</div><div class="filters">')
    out.append(f'<button data-k="sev" data-v="all">{e(t["all"])}</button>')
    for sev in ORDER:
        out.append(f'<button data-k="sev" data-v="{SEV_CLASS[sev]}">{e(t["sevs"][sev])} ({result["by_severity"][sev]})</button>')
    out.append("</div>")
    if not items:
        out.append(f"<p>{e(t['none'])}</p>")
    for f in items:
        sev = f["severity"]
        where = e(str(f.get("file", ""))) + (":" + e(str(f["line"])) if f.get("line") else "")
        guess = f' <span class="tag">{e(t["guess"])}</span>' if f.get("status") == "taxmin" else ""
        out.append(
            f'<div class="item {"fixed" if f["state"] == "fixed" else ""}" data-sev="{SEV_CLASS.get(sev, "s2")}" data-st="{e(f["state"])}">'
            f'<div class="row"><b>{e(f["id"])}</b><span class="tag {SEV_CLASS.get(sev, "s2")}">{e(t["sevs"].get(sev, sev))}</span>'
            f'<span class="tag">{e(t["open"] if f["state"] == "open" else t["fixed"])}</span>'
            f'<span class="tag">{e(t["levels"].get(f.get("level", "tajribali"), "tajribali"))}</span>{guess}</div>'
            f'<h2>{e(f.get("title") or f.get("rule") or "")}</h2>'
            f'<div class="mut">{e(t["where"])}: <code>{where}</code> · {e(t["rule"])}: <code>{e(f.get("rule", ""))}</code></div></div>')
    out.append(f"</main><script>{JS}</script></body></html>")
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--store", default=".vibeguard/findings.json")
    p.add_argument("--out", default=".vibeguard/reports/report.html")
    p.add_argument("--lang", default="uz", choices=sorted(L))
    p.add_argument("--title", default="")
    a = p.parse_args()
    page = build(load(a.store), a.lang, a.title)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write(page)
    print(a.out)


if __name__ == "__main__":
    main()
