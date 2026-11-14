---
id: bot-initdata
soha: bot
xavf: kritik
lesson: "Verify Telegram initData signature and auth_date on the server; never take the user id from the request body or initDataUnsafe."
agent: attacker-user
---

# Telegram initData serverda tekshirilmaydi

## Nima qidiriladi
- Mini App backend'i `user_id` ni so'rov tanasi, URL yoki `initDataUnsafe` dan to'g'ridan-to'g'ri oladi.
- `initData` imzosi (bot tokeni asosidagi HMAC) va `auth_date` muddati tekshirilmaydi.

## Nega xavfli
Klientdan kelgan `user_id` ga ishonilsa, istalgan odam boshqa foydalanuvchi nomidan amal bajarishi, uning ma'lumotini o'qishi yoki balansini sarflashi mumkin.

## Yomon misol
```js
app.post('/api/balance', (req, res) => {
  const user = db.get(req.body.userId)   // klient aytgan id
  res.json(user)
})
```

## Yaxshi misol
```js
app.post('/api/balance', (req, res) => {
  const data = verifyInitData(req.headers['x-init-data'], BOT_TOKEN, { maxAgeSec: 3600 })
  if (!data) return res.sendStatus(401)
  res.json(db.get(data.user.id))          // serverda tasdiqlangan id
})
```

## Tuzatish
Telegram hujjatidagi `initData` tekshiruv algoritmini serverda qo'lla, `auth_date` ni cheklab, foydalanuvchini faqat tasdiqlangan ma'lumotdan ol.

Claude Code uchun prompt: "Barcha Mini App API route'larida Telegram initData imzosini va auth_date muddatini serverda tekshir, user_id ni faqat tasdiqlangan initData'dan ol va buning uchun test yoz."
