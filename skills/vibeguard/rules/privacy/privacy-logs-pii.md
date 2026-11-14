---
id: privacy-logs-pii
soha: privacy
xavf: o'rta
lesson: "Log only ids and event types; never log whole request/update objects, phones, emails, tokens or passwords."
agent: attacker-scraper
---

# Loglarda shaxsiy ma'lumot va sirlar

## Nima qidiriladi
- `print`, `console.log`, `logger.info` ga butun so'rov, `update`, `message`, `user` obyekti yoki sarlavhalar beriladi.
- Logda telefon, email, parol, token, to'lov ma'lumoti, `initData`.
- Xato kuzatuv xizmatiga (Sentry va shunga o'xshash) so'rov tanasi to'liq yuboriladi.

## Nega xavfli
Loglar kodga qaraganda kamroq himoyalanadi: hosting paneli, uchinchi tomon xizmatlari, jamoa a'zolari ko'radi. Bitta log sizishi butun foydalanuvchilar ma'lumotini ochadi.

## Yomon misol
```python
logging.info(f"Yangi xabar: {message}")   # butun obyekt, telefon bilan
```

## Yaxshi misol
```python
logging.info("Yangi xabar: user=%s turi=%s", message.from_user.id, message.content_type)
```

## Tuzatish
Logga faqat identifikator va hodisa turini yoz. Nozik maydonlarni yashiruvchi yagona funksiya ishlat. Log saqlash muddatini belgila.

Claude Code uchun prompt: "Loglarga butun obyekt yoki nozik maydon (telefon, email, token, parol) yoziladigan joylarni top, ularni identifikator va hodisa turi bilan almashtir va nozik maydonlarni yashiruvchi yordamchi funksiya qo'sh."
