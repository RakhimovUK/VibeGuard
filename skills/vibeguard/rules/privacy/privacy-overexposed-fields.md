---
id: privacy-overexposed-fields
soha: privacy
xavf: yuqori
lesson: "Return an explicit list of fields from every endpoint, cap list limits, and avoid sequential ids in public URLs."
agent: attacker-scraper
---

# API keragidan ortiq ma'lumot qaytaradi

## Nima qidiriladi
- `res.json(user)`, `return user.__dict__`, `SELECT *` natijasi to'g'ridan-to'g'ri javobga ketadi.
- Ro'yxat endpoint'larida `limit` yo'q yoki klient istalgan qiymat bera oladi.
- Ommaviy profil javobida telefon, email, balans, parol xeshi, ichki belgilar.
- Ketma-ket sonli ID ochiq manzillarda.

## Nega xavfli
Frontend ko'rsatmasa ham, javobdagi hamma maydon foydalanuvchiga yetib boradi. Limitsiz ro'yxat va ketma-ket ID bilan butun bazani bir necha so'rovda yig'ib olish mumkin.

## Yomon misol
```js
app.get('/users', async (req, res) => res.json(await User.find()))
```

## Yaxshi misol
```js
app.get('/users', auth, async (req, res) => {
  const limit = Math.min(Number(req.query.limit) || 20, 50)
  const users = await User.find().select('id name avatar').limit(limit)
  res.json(users)
})
```

## Tuzatish
Har bir javob uchun ruxsat etilgan maydonlar ro'yxatini aniq yoz, ro'yxatlarda maksimal limit qo'y, ochiq manzillarda tasodifiy identifikator (UUID) ishlat.

Claude Code uchun prompt: "Model obyektini to'liq qaytaradigan endpoint'larni top, har biri uchun ruxsat etilgan maydonlar ro'yxatini kirit, ro'yxatlarga maksimal limit qo'y va nozik maydon javobda yo'qligini test bilan isbotla."
