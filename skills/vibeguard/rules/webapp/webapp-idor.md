---
id: webapp-idor
soha: webapp
xavf: yuqori
lesson: "Every query by id must also filter by the current user's ownership; return 404 otherwise."
agent: attacker-user
---

# Egasi tekshirilmaydigan obyektlar (IDOR)

## Nima qidiriladi
- Route parametri yoki so'rov tanasidagi `id` bilan bazadan yozuv olinadi (`/orders/:id`, `?user_id=`), lekin yozuv joriy foydalanuvchiga tegishliligi tekshirilmaydi.
- `findById(req.params.id)` dan keyin `owner`/`user_id` solishtiruvi yo'q.

## Nega xavfli
Foydalanuvchi manzildagi raqamni o'zgartirib, boshqa odamning buyurtmasi, cheki yoki profilini o'qishi yoki o'zgartirishi mumkin.

## Yomon misol
```js
app.get('/orders/:id', auth, async (req, res) => {
  res.json(await Order.findById(req.params.id))
})
```

## Yaxshi misol
```js
app.get('/orders/:id', auth, async (req, res) => {
  const order = await Order.findOne({ _id: req.params.id, userId: req.user.id })
  if (!order) return res.sendStatus(404)
  res.json(order)
})
```

## Tuzatish
Har bir so'rovda egalikni bazaning o'zida filtrlab ol (`id` + `userId`). Topilmasa 404 qaytar.

Claude Code uchun prompt: "ID bo'yicha yozuv qaytaradigan yoki o'zgartiradigan barcha route'larda joriy foydalanuvchi egaligini so'rov filtrida tekshir va boshqa foydalanuvchi yozuviga kirish 404 qaytarishini test bilan isbotla."
