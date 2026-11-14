---
id: webapp-sql-injection
soha: webapp
xavf: kritik
lesson: "Always use parameterized queries or the ORM; never build SQL with string concatenation or f-strings."
agent: attacker-user
---

# So'rov matniga foydalanuvchi kiritmasini qo'shish (SQL in'ektsiya)

## Nima qidiriladi
- SQL satri `+`, f-string, shablon (`${}`) yoki `%` bilan yig'iladi va ichida foydalanuvchi qiymati bor.
- `db.query("... " + x)`, `cursor.execute(f"...")`, `raw()` chaqiruvlari.
- NoSQL: so'rov obyektiga `req.body` to'g'ridan-to'g'ri beriladi.

## Nega xavfli
Kiritma so'rovning bir qismiga aylanadi. Hujumchi boshqa jadvallarni o'qishi, yozuvlarni o'zgartirishi yoki o'chirishi mumkin.

## Yomon misol
```python
cur.execute(f"SELECT * FROM users WHERE name = '{name}'")
```

## Yaxshi misol
```python
cur.execute("SELECT * FROM users WHERE name = %s", (name,))
```

## Tuzatish
Har doim parametrli so'rov yoki ORM ishlat. Jadval va ustun nomlari kiritmadan kelsa, ruxsat etilgan ro'yxat bilan solishtir.

Claude Code uchun prompt: "Satr birlashtirish bilan yig'ilgan barcha SQL so'rovlarni parametrli so'rovga o'tkaz va maxsus belgili kiritma so'rovni buzmasligini test bilan isbotla."
