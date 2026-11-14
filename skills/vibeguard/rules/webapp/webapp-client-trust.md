---
id: webapp-client-trust
soha: webapp
xavf: yuqori
lesson: "Never trust price, amount, discount or role from the client; compute them on the server and whitelist updatable fields."
agent: attacker-fraudster
---

# Klientdan kelgan narx, miqdor yoki rolga ishonish

## Nima qidiriladi
- Server `price`, `amount`, `total`, `discount`, `is_admin`, `role` kabi qiymatlarni so'rov tanasidan oladi va qayta hisoblamaydi.
- Tekshiruv faqat frontend'da (forma validatsiyasi, yashirilgan tugma).
- `Object.assign(user, req.body)` yoki `User.update(req.body)` (mass assignment).

## Nega xavfli
Klient so'rovni istalgancha o'zgartira oladi. Narx 1 so'mga, miqdor manfiyga, rol adminga aylanishi mumkin.

## Yomon misol
```js
app.post('/buy', auth, async (req, res) => {
  await charge(req.user, req.body.price)
  await give(req.user, req.body.productId)
})
```

## Yaxshi misol
```js
app.post('/buy', auth, async (req, res) => {
  const product = await Product.findById(req.body.productId)
  if (!product) return res.sendStatus(404)
  await charge(req.user, product.price)   // narx serverdan
  await give(req.user, product.id)
})
```

## Tuzatish
Klientdan faqat "nima" keladi (mahsulot id, soni), "qancha" va "kim" serverda aniqlanadi. Yangilanadigan maydonlar ro'yxatini aniq yoz.

Claude Code uchun prompt: "Narx, summa, chegirma va rol qiymatlari klientdan olinadigan joylarni top, ularni serverda hisoblaydigan qil, miqdorni musbat butun son sifatida tekshir va o'zgartirilgan narx rad etilishini test bilan isbotla."
