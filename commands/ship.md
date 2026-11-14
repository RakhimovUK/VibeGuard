---
description: Chiqarishdan oldingi tekshiruv. Faqat oxirgi o'zgarishlarni tekshiradi va "tayyor / tayyor emas" hukmini beradi.
argument-hint: "[taqqoslash uchun branch yoki commit, sukut: main]"
---

`vibeguard` skillini yukla va chiqarishdan oldingi tekshiruvni ishga tushir.

1. `.vibeguard/config.json` yo'q bo'lsa: ruxsat tasdig'i va til.
2. O'zgargan fayllarni aniqla: `git diff --name-only <asos>...HEAD` va saqlanmagan o'zgarishlar. Asos: $ARGUMENTS, bo'sh bo'lsa `main` (yo'q bo'lsa `master`). Git repo bo'lmasa, foydalanuvchiga `/vibeguard:redteam` ni tavsiya qil va to'xta.
3. O'zgarish yo'q bo'lsa: "tekshiradigan o'zgarish yo'q" deb to'xta.
4. Skriptlarni butun loyihada ishga tushir (tez): `scan_secrets.py`, `check_hygiene.py`.
5. O'zgargan fayllar qaysi sohaga tegishini aniqla (bot, webapp, payments, deploy va h.k.) va faqat tegishli hujumchi agentlarni ishga tushir. Ularga o'zgargan fayllar ro'yxatini va diff'ni ber; ular shu fayllarni va ular chaqiradigan kodni o'qiydi.
6. Topilmalarni `redteam-skeptic` ga ber.
7. Xotirani yangila: `findings.py merge --partial`. Keyin `findings.py score`.
8. Hukm:
   - **Tayyor emas:** bu o'zgarishlarda tasdiqlangan kritik yoki yuqori topilma bor, yoki yangi sir topildi.
   - **Tayyor:** aks holda. Xotirada ochiq qolgan eski topilmalar bo'lsa, ularni alohida eslat.
9. Qisqa natija: hukm, yangi topilmalar (ID, fayl:qator, tuzatish), eski ochiq topilmalar soni.

Faqat kod o'qiladi. Deploy'ni to'xtatmaydi va o'zi deploy qilmaydi: qaror foydalanuvchida.

Skriptlar joyi: `${CLAUDE_PLUGIN_ROOT}/skills/vibeguard/scripts/`. Chaqirish namunasi: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/vibeguard/scripts/findings.py" score`. Qoidalar: `${CLAUDE_PLUGIN_ROOT}/skills/vibeguard/rules/`.
