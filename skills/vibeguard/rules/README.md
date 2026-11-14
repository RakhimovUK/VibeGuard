# Qoida fayllari formati

Har bir qoida alohida fayl: `rules/<soha>/<id>.md`. Soha: `bot`, `webapp`, `site`, `apk`, `secrets`, `bugs`, `payments`, `deploy`, `privacy`, `ai`, `cost`.

Hujumchi agent faqat o'z sohasidagi qoidalarni o'qiydi.

## Qolip

```markdown
---
id: payments-idempotency
soha: payments
xavf: yuqori
agent: attacker-fraudster
---

# Nomi

## Nima qidiriladi
Qanday kod belgilari bu xatoga ishora qiladi (qidiruv iboralari, naqshlar).

## Nega xavfli
Hujumchi buni qanday ishlatadi (tushuntirish darajasida, payloadsiz).

## Yomon misol
kod

## Yaxshi misol
kod

## Tuzatish
Qadamlar. Claude Code uchun tayyor prompt.
```

## Qoidalar

- Bitta fayl: bitta xato turi.
- Misollar qisqa va stackdan mustaqil bo'lsin (kerak bo'lsa bir nechta tilda).
- Ishlaydigan exploit yoki payload yozilmaydi.
