---
description: Qo'riqchi rejimi. Kodga token yoki kalit yozilsa darhol to'xtatadi. Yoqish, o'chirish, holat.
argument-hint: "on | off | status"
---

Qo'riqchi rejimini boshqar. Buyruq: $ARGUMENTS (bo'sh bo'lsa `status`).

Qo'riqchi plagin bilan birga keladigan hook (`hooks/guard.py`): Claude Code fayl yozishidan oldin yangi matnni sirlar naqshiga tekshiradi. U faqat `.vibeguard/config.json` da `"guard": true` bo'lsa ishlaydi. AI chaqiruvi yo'q, shuning uchun tez.

- **on:** `.vibeguard/config.json` ni o'qi (yo'q bo'lsa ruxsat tasdig'i va til bilan yarat), `"guard": true` qil. `.vibeguard/` `.gitignore`da ekanini tekshir. Foydalanuvchiga nima bo'lishini bir-ikki jumlada tushuntir:
  - Aniq sir (bot tokeni, API kalit, baza paroli) kodga yozilsa, yozish to'xtatiladi.
  - Parolga o'xshash umumiy qiymat bo'lsa, tasdiq so'raladi.
  - `.env` ga yozish mumkin, lekin `.env` `.gitignore`da bo'lishi shart.
- **off:** `"guard": false` qil.
- **status:** yoqilgan yoki o'chirilganini va `guard_allow` ro'yxatini ko'rsat.

Qo'shimcha: sinov fayllari kabi istisno kerak bo'lsa, foydalanuvchi so'raganda `"guard_allow": ["tests/fixtures/*"]` kabi naqsh qo'sh. O'zing istisno qo'shma.

Eslatma: qo'riqchi faqat Claude Code yozayotgan matnni ko'radi. Qo'lda yozilgan yoki oldindan bor sirlarni `/vibeguard:quick` topadi. `python3` o'rnatilmagan bo'lsa qo'riqchi ishlamaydi: buni tekshir va ayt.
