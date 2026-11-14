# Contributing to VibeGuard / Hissa qo'shish

Takliflar, yangi qoidalar va tuzatishlar uchun rahmat. Quyidagi tartib ishni tez ko'rib chiqishga yordam beradi. (English summary at the end.)

## Eng foydali hissalar

1. **Yangi qoida** (`skills/vibeguard/rules/<soha>/<id>.md`). Format: `rules/README.md`. Majburiy: `id`, `soha`, `xavf`, `lesson` (ingliz tilida bir jumla), `agent`; yomon va yaxshi misol; tuzatish va tayyor prompt.
2. **Sinov xatosi** (`fixtures/`): yangi qoida uchun ataylab qo'yilgan xato va `fixtures/expected.json` ga yozuv.
3. **Yolg'on topilma haqida xabar:** skript yoki agent xavfsiz kodni xato deb belgilasa, kod parchasi bilan issue oching.
4. **Tarjima:** `i18n/glossary.md`, `templates/report.<lang>.md`, README.
5. **Ssenariy** (`skills/vibeguard/scenarios/`): yangi loyiha turi uchun tekshiruv rejalari.

## Qat'iy talablar

- **Exploit yo'q.** Qoida va agentlar zaiflik qanday ishlatilishini tushuntiradi, lekin ishlaydigan payload, brute-force yoki DoS kodi qabul qilinmaydi.
- **Haqiqiy sir yo'q.** Sinov uchun faqat `FAKE` so'zi bor soxta qiymatlar.
- **Faqat o'qish.** Hujumchi agentlar `Read, Grep, Glob` bilan cheklanadi. Kod o'zgartiradigan yagona agent: `fixer`, faqat tasdiqdan keyin.
- **Skriptlar:** faqat Python standart kutubxonasi, tarmoq so'rovi yo'q, sirlar yashirib chiqariladi.

## PR'dan oldin

```
python3 skills/vibeguard/scripts/selftest.py
python3 skills/vibeguard/scripts/ci_check.py . --exclude "fixtures/*"
claude plugin validate .
```

Uchalasi ham xatosiz o'tishi kerak. Yangi qoida qo'shgan bo'lsangiz, uni kamida bitta sinov loyihasida `/vibeguard:redteam` bilan sinab, natijani PR'da yozing: topildi / topilmadi / yolg'on topilma.

## Commit va PR

- Bitta PR: bitta mavzu. Sarlavha: `rule: webapp-csrf`, `fix: guard .env tekshiruvi`, `docs: ...`.
- Xulq-atvor o'zgarsa, README va `SKILL.md` ni ham yangilang.

## English summary

Most useful contributions: new rule files, planted bugs in `fixtures/` with an entry in `expected.json`, false-positive reports, translations, and scenario packs. No working exploits, no real secrets, attacker agents stay read-only, scripts use only the Python standard library and make no network requests. Before opening a PR run the three commands above; all must pass.
