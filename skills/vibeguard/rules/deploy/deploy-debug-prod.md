---
id: deploy-debug-prod
soha: deploy
xavf: yuqori
lesson: "Debug mode off by default; no debug/test/env endpoints in production; no stack traces in responses; restrict CORS to known origins."
agent: attacker-outsider
---

# Production'da debug rejimi va ochiq xizmat endpoint'lari

## Nima qidiriladi
- `DEBUG=True`, `app.run(debug=True)`, `NODE_ENV` o'rnatilmagan, batafsil xato sahifalari.
- Himoyasiz `/debug`, `/test`, `/admin`, `/env`, `/metrics`, `/docs`, `/swagger`, `/graphql` (introspection ochiq).
- Xato javobida stack trace, SQL matni yoki fayl yo'llari.
- CORS `*` va `credentials: true` birga.

## Nega xavfli
Debug sahifasi muhit o'zgaruvchilarini, kod parchalarini va ichki tuzilmani ko'rsatadi. Ayrim framework'larda debug konsoli serverda kod bajarish imkonini beradi.

## Yomon misol
```python
@app.get("/debug/env")
def env():
    return dict(os.environ)

app.run(debug=True)
```

## Yaxshi misol
```python
DEBUG = os.environ.get("APP_ENV") == "development"
app.run(debug=DEBUG)
# debug route'lar faqat DEBUG bo'lganda ro'yxatga olinadi
```

## Tuzatish
Debug rejimini muhit o'zgaruvchisiga bog'la, sukut bo'yicha o'chiq. Xizmat endpoint'larini o'chir yoki admin autentifikatsiyasi ortiga qo'y. Foydalanuvchiga umumiy xato xabari, tafsilot faqat logga.

Claude Code uchun prompt: "Debug rejimi sukut bo'yicha o'chiq bo'lsin, debug va test route'larni production'da ro'yxatdan chiqar, xato javoblaridan stack trace'ni olib tashla va CORS'ni aniq domenlar bilan chekla."
