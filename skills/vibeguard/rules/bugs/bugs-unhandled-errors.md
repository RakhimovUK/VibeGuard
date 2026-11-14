---
id: bugs-unhandled-errors
soha: bugs
xavf: o'rta
lesson: "Never swallow exceptions; log them, roll back or refund half-finished operations, and validate input before use."
agent: attacker-outsider
---

# Ushlanmagan xatolar va yutib yuborilgan istisnolar

## Nima qidiriladi
- Tashqi chaqiruvlar (API, baza, fayl) atrofida xato ushlash yo'q, bitta xato butun jarayonni to'xtatadi.
- `except: pass`, bo'sh `catch {}`: xato yutiladi va amal "muvaffaqiyatli" deb davom etadi.
- `await` unutilgan, promise ushlanmagan.
- Pul yechilgandan keyingi qadam yiqilsa, pulni qaytarish yoki qayta urinish yo'q.
- Kiritma turi tekshirilmaydi (`int(text)`, `JSON.parse` himoyasiz).

## Nega xavfli
Kutilmagan kiritma botni yoki serverni yiqitadi. Yutilgan xato esa ma'lumotni buzadi: foydalanuvchidan pul yechiladi, mahsulot berilmaydi va hech kim bilmaydi.

## Yomon misol
```python
try:
    charge(user, price)
    deliver(user, product)
except:
    pass
```

## Yaxshi misol
```python
charge_id = charge(user, price)
try:
    deliver(user, product)
except Exception:
    logger.exception("Yetkazish yiqildi, charge=%s", charge_id)
    refund(charge_id)
    raise
```

## Tuzatish
Xatoni yutma: logga yoz, foydalanuvchiga tushunarli xabar ber, yarim bajarilgan amalni orqaga qaytar. Umumiy xato ushlagich qo'y, kiritmani ishlatishdan oldin tekshir.

Claude Code uchun prompt: "Bo'sh except/catch bloklarini va himoyasiz tashqi chaqiruvlarni top, xatolarni logga yozadigan va yarim bajarilgan to'lov amallarini qaytaradigan qil, noto'g'ri kiritma jarayonni yiqitmasligini test bilan isbotla."
