---
description: Tasdiqlangan topilmalarni tuzatadi. Har biri uchun test, alohida branch va commit, so'ng qayta hujum.
argument-hint: "[topilma ID'lari, masalan VG-001 VG-003; bo'sh bo'lsa ro'yxat ko'rsatiladi]"
---

`vibeguard` skillini yukla va tuzatish rejimini ishga tushir. Topilmalar: $ARGUMENTS

1. `.vibeguard/findings.json` ni o'qi. Yo'q bo'lsa: "avval `/vibeguard:redteam` ni ishga tushiring" deb to'xta.
2. ID berilmagan bo'lsa: ochiq topilmalarni xavf darajasi bo'yicha ko'rsat va qaysilarini tuzatishni so'ra. "Taxmin" holatidagilarni tuzatishga taklif qilma: avval tasdiqlash kerak.
3. **Tasdiq:** tuzatiladigan ro'yxatni ko'rsat va aniq "ha" ol. Tasdiqsiz hech narsa o'zgartirma.
4. `git status` toza ekanini tekshir. Toza bo'lmasa, foydalanuvchidan avval o'zgarishlarini saqlashni so'ra.
5. Har bir topilma uchun **ketma-ket** (parallel emas) `fixer` agentini chaqir. Unga ber: ID, fayl:qator, qoida fayli, tuzatish yo'li.
6. Fixer tugagach, **qayta hujum:** topilmani dastlab topgan hujumchi agentni faqat shu fayllarga qayta ishga tushir. Hujum yo'li yopilganmi?
   - Yopilgan: `findings.py resolve <ID>` bilan xotirada `fixed` deb belgila.
   - Yopilmagan: fixer'ga bir marta qayta urinish, yana bo'lmasa to'xta va foydalanuvchiga tushuntir.
   - Qayta hujum yangi xato topsa: `findings.py merge --partial` bilan qo'sh.
7. `findings.py score` ni ko'rsat: bal oldin va keyin.
8. Yakuniy xulosa:
   - Tuzatildi / qoldi jadvali.
   - Yaratilgan branch'lar ro'yxati va ularni qanday ko'rib chiqib birlashtirish.
   - **O'zingiz qilasiz:** sirlarni almashtirish, paneldagi sozlamalar, deploy.

Push, merge va deploy qilinmaydi: bularni foydalanuvchi o'zi bajaradi.

Skriptlar joyi: `${CLAUDE_PLUGIN_ROOT}/skills/vibeguard/scripts/`. Chaqirish namunasi: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/vibeguard/scripts/findings.py" score`. Qoidalar: `${CLAUDE_PLUGIN_ROOT}/skills/vibeguard/rules/`.
