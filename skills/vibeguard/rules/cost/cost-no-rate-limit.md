---
id: cost-no-rate-limit
soha: cost
xavf: yuqori
lesson: "Add per-user rate limits and daily quotas (persistent store) to paid or heavy operations and to login/OTP endpoints."
agent: attacker-cost
---

# Pullik yoki og'ir amallarda limit yo'q

## Nima qidiriladi
- AI, SMS, email, yuklab olish, video qayta ishlash kabi chaqiruvlar foydalanuvchi bo'yicha hisoblanmaydi.
- Login, OTP, ro'yxatdan o'tish, qidiruv endpoint'larida rate limit yo'q.
- Bot buyruqlarida "bir foydalanuvchi, bir vaqtda bitta vazifa" cheklovi yo'q.
- Limit faqat xotirada (qayta ishga tushganda yo'qoladi, bir nechta nusxada ishlamaydi).

## Nega xavfli
Bitta odam yoki skript minglab so'rov yuborib, pullik xizmat hisobini oshiradi yoki serverni band qilib, boshqalarga xizmatni to'xtatadi.

## Yomon misol
```python
@dp.message(Command("download"))
async def download(msg):
    await heavy_download(msg.text)      # cheklovsiz
```

## Yaxshi misol
```python
@dp.message(Command("download"))
async def download(msg):
    if not await limiter.allow(msg.from_user.id, per_minute=3, per_day=50):
        return await msg.answer("Biroz kuting.")
    await heavy_download(msg.text)
```

## Tuzatish
Foydalanuvchi va IP bo'yicha limit (Redis yoki baza orqali), kunlik kvota, bir vaqtdagi vazifalar soni cheklovi. Provayder va hosting panelida byudjet ogohlantirishi ("O'zingiz qilasiz").

Claude Code uchun prompt: "Pullik va og'ir amallarni chaqiradigan handler'larni top, foydalanuvchi bo'yicha daqiqalik va kunlik limit qo'sh (doimiy saqlagich bilan) va limitdan oshgan so'rov rad etilishini test bilan isbotla."
