---
id: ai-prompt-injection
soha: ai
xavf: yuqori
lesson: "Keep system and user roles separate; treat model output as untrusted input; require confirmation for irreversible tool actions; no secrets in system prompts."
agent: attacker-ai
---

# AI ko'rsatmasiga foydalanuvchi matnini aralashtirish

## Nima qidiriladi
- Tizim ko'rsatmasi va foydalanuvchi matni bitta satrga birlashtiriladi.
- AI o'qiydigan tashqi kontent (sayt, fayl, boshqa foydalanuvchi xabari) ko'rsatmadan ajratilmagan.
- AI javobi tekshirilmasdan SQL, shell, HTML yoki boshqa API chaqiruviga beriladi.
- AI'ga keng vositalar berilgan (bazaga yozish, pul, xabar yuborish) va amal tasdiqsiz bajariladi.
- Tizim ko'rsatmasida sir yoki ichki ma'lumot.

## Nega xavfli
Model ko'rsatma bilan ma'lumotni ishonchli ajrata olmaydi. Foydalanuvchi yoki tashqi kontent modelga boshqa topshiriq berishi, ichki ko'rsatmani chiqarib olishi yoki model vositalari orqali zararli amal bajartirishi mumkin.

## Yomon misol
```python
prompt = SYSTEM + "\nFoydalanuvchi: " + user_text
answer = llm(prompt)
db.execute(answer)
```

## Yaxshi misol
```python
answer = llm(system=SYSTEM, messages=[{"role": "user", "content": user_text}])
action = parse_allowed_action(answer)      # faqat ruxsat etilgan amallar ro'yxati
if action.needs_confirmation:
    ask_user_to_confirm(action)
```

## Tuzatish
Rollarni ajrat, model javobini ishonchsiz kiritma deb qabul qil, vositalarni minimal huquq bilan ber, qaytarib bo'lmaydigan amallarda inson tasdig'ini so'ra, tizim ko'rsatmasiga sir yozma.

Claude Code uchun prompt: "AI chaqiruvlarida tizim va foydalanuvchi rollarini ajrat, model javobini ruxsat etilgan amallar ro'yxati bilan tekshir, xavfli amallarga tasdiq qo'sh va tizim ko'rsatmasidan sirlarni olib tashla."
