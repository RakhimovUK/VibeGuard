# Sinov loyihalari (fixtures)

**OGOHLANTIRISH: bu kodlar ataylab xato bilan yozilgan. Hech qachon ishga tushirmang va deploy qilmang.**

Bu yerdagi barcha token, kalit va parollar soxta (`FAKE` so'zi bilan). Ular faqat skriptlar naqshni taniy olishini sinash uchun.

- `vuln-bot/`: Python Telegram bot, ataylab qo'yilgan xatolar bilan.
- `vuln-webapp/`: Node.js Mini App backend, ataylab qo'yilgan xatolar bilan.
- `expected.json`: qo'yilgan xatolar ro'yxati. `detector: script` bo'lganlarini skriptlar topishi kerak, `detector: agent` bo'lganlarini hujumchi agentlar.

## Sinash

```
python3 skills/vibeguard/scripts/selftest.py
```

Agentlar aniqligini o'lchash: `/vibeguard:redteam fixtures/vuln-bot` ni ishga tushiring va hisobotni `expected.json` bilan solishtiring (topilgan / o'tkazib yuborilgan / yolg'on topilma).
