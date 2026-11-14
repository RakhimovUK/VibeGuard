---
id: cost-unbounded-input
soha: cost
xavf: o'rta
lesson: "Limit upload size, request body size and timeouts; validate user-supplied URLs and block internal addresses."
agent: attacker-cost
---

# Cheklanmagan kiritma: fayl hajmi, so'rov tanasi, kutish vaqti

## Nima qidiriladi
- Fayl yuklashda hajm va tur cheklovi yo'q.
- So'rov tanasi limiti o'chirilgan yoki juda katta (`limit: '500mb'`).
- Tashqi so'rovlarda `timeout` yo'q.
- Foydalanuvchi bergan URL'dan yuklab olishda hajm, davomiylik va manzil tekshirilmaydi.
- Navbat va vaqtinchalik fayllar tozalanmaydi.

## Nega xavfli
Juda katta fayl yoki cheksiz kutadigan so'rov xotira, disk va tarmoq trafigini yeb qo'yadi. Xizmat to'xtaydi yoki hosting hisobi o'sadi. URL bo'yicha yuklash ichki manzillarga murojaat qilishga ham ishlatilishi mumkin.

## Yomon misol
```js
app.use(express.json({ limit: '500mb' }))
const r = await fetch(req.body.url)          // timeout va hajm cheklovi yo'q
```

## Yaxshi misol
```js
app.use(express.json({ limit: '100kb' }))
const r = await fetch(url, { signal: AbortSignal.timeout(15000) })
// hajmni oqim davomida sanab, chegaradan oshsa to'xtatish
```

## Tuzatish
Har bir kirish uchun maksimal hajm, tur ro'yxati va timeout belgila. URL'larni tekshir (faqat http/https, ichki va mahalliy manzillar taqiqlangan). Vaqtinchalik fayllarni tozala.

Claude Code uchun prompt: "Fayl yuklash, so'rov tanasi va tashqi so'rovlar uchun hajm chegarasi va timeout qo'sh, foydalanuvchi bergan URL'larda ichki manzillarni taqiqla va chegaradan katta kiritma rad etilishini test bilan isbotla."
