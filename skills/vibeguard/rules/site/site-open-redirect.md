---
id: site-open-redirect
soha: site
xavf: o'rta
lesson: "Only redirect to internal relative paths or an allowlist of domains."
agent: attacker-phisher
---

# Ochiq yo'naltirish (open redirect)

## Nima qidiriladi
- `redirect(req.query.next)`, `location.href = params.get('url')` kabi, manzil tekshirilmasdan yo'naltirish.
- Parametr nomlari: `next`, `url`, `redirect`, `return`, `continue`, `callback`.

## Nega xavfli
Havola sizning domeningizdan boshlanadi, lekin begona saytga olib boradi. Foydalanuvchi domenga ishonib, soxta sahifaga ma'lumot kiritadi.

## Yomon misol
```js
app.get('/go', (req, res) => res.redirect(req.query.url))
```

## Yaxshi misol
```js
app.get('/go', (req, res) => {
  const next = String(req.query.url || '/')
  const safe = next.startsWith('/') && !next.startsWith('//')
  res.redirect(safe ? next : '/')
})
```

## Tuzatish
Faqat ichki yo'llarga yoki ruxsat etilgan domenlar ro'yxatiga yo'naltir.

Claude Code uchun prompt: "Foydalanuvchi parametri bo'yicha yo'naltiradigan joylarni top, faqat ichki nisbiy yo'llarga ruxsat ber va tashqi manzil bosh sahifaga tushishini test bilan isbotla."
