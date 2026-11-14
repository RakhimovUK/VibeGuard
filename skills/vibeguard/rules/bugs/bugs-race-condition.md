---
id: bugs-race-condition
soha: bugs
xavf: yuqori
lesson: "Change balances, stock and one-time bonuses with atomic updates or row locks; add unique constraints for one-time actions."
agent: attacker-fraudster
---

# Poyga holati: "tekshir, keyin o'zgartir"

## Nima qidiriladi
- Balans, zaxira, limit yoki promo-kod avval o'qiladi, keyin alohida so'rov bilan yoziladi.
- `if user.balance >= price: user.balance -= price` tranzaksiya va qulfsiz.
- "Bir marta" bajarilishi kerak amallar (bonus olish, promo ishlatish) unique cheklovsiz.

## Nega xavfli
Ikki so'rov bir vaqtda kelsa, ikkalasi ham eski qiymatni ko'radi va ikkalasi ham o'tadi: balansdan bir marta yechilib, mahsulot ikki marta beriladi yoki bonus ikki marta olinadi.

## Yomon misol
```python
if user.balance >= price:
    user.balance -= price
    user.save()
    give_product(user)
```

## Yaxshi misol
```python
updated = db.execute(
    "UPDATE users SET balance = balance - %s WHERE id = %s AND balance >= %s",
    (price, user.id, price),
)
if updated.rowcount == 1:
    give_product(user)
```

## Tuzatish
Tekshirish va o'zgartirishni bitta atomar so'rovga birlashtir yoki tranzaksiya ichida satrni qulfla. Bir martalik amallarga unique indeks qo'y.

Claude Code uchun prompt: "Balans, zaxira va bir martalik bonuslarni o'zgartiradigan kodni atomar yangilash yoki tranzaksiyaga o'tkaz va bir vaqtdagi ikki so'rovdan faqat bittasi o'tishini test bilan isbotla."
