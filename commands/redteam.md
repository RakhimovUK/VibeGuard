---
description: Red Team rejimi. Hujumchi ko'zi bilan loyihani tekshiradi, zaif joylarni va tuzatish yo'lini ko'rsatadi.
argument-hint: "[yo'l yoki qism: bot | webapp | site | apk | payments]"
---

`vibeguard` skillini yukla va Red Team rejimini ishga tushir. Maqsad: $ARGUMENTS (bo'sh bo'lsa butun loyiha).

Qadamlar:

1. `.vibeguard/config.json` bor-yo'qligini tekshir. Yo'q bo'lsa: ruxsat tasdig'ini so'ra ("loyiha meniki yoki yozma ruxsatim bor") va tilni tanlat (uz-lotin, uz-kirill, ru, en). Tasdiqsiz davom etma.
2. `redteam-recon` agentini ishga tushir. U stack va qismlarni (bot, webapp, sayt, apk, to'lov, deploy) aniqlaydi. Keyin `${CLAUDE_PLUGIN_ROOT}/skills/vibeguard/scenarios/README.md` ni o'qi: loyiha turiga mos ssenariy bo'lsa, uni o'qib, tegishli hujumchi agentlarga "avval shu rejalarni tekshir" deb ber (ssenariy qidiruvni cheklamaydi).
3. Skriptlarni ishga tushir (tez, AI'siz) va natijasini agentlarga dalil sifatida ber:
   - `python3 "${CLAUDE_PLUGIN_ROOT}/skills/vibeguard/scripts/scan_secrets.py" <papka>`
   - `python3 "${CLAUDE_PLUGIN_ROOT}/skills/vibeguard/scripts/check_hygiene.py" <papka>`
   Python yo'q bo'lsa bu qadamni o'tkazib yubor va hisobotda ayt. gitleaks, semgrep, npm audit, pip-audit o'rnatilgan bo'lsa ularni ham ishlat (faqat o'qish rejimida).
4. Recon natijasiga qarab tegishli hujumchi agentlarni **bir vaqtda** ishga tushir. Har bir agentga `${CLAUDE_PLUGIN_ROOT}/skills/vibeguard/rules/` ichidan `agent:` maydoni uning nomiga teng bo'lgan qoida fayllarini o'qishni ayt:
   - `attacker-outsider` (har doim)
   - `attacker-user` (login yoki foydalanuvchi ma'lumoti bor bo'lsa)
   - `attacker-token` (token, kalit, `.env`, bot tokeni bor bo'lsa)
   - `attacker-fraudster` (to'lov, Stars, balans, promo, referal bor bo'lsa)
   - `attacker-cost` (pullik API, hosting, AI chaqiruvlari bor bo'lsa)
   - `attacker-supply` (har doim: bog'liqliklar va CI)
   - `attacker-deploy` (Docker, Railway, Supabase/Firebase, baza sozlamalari bor bo'lsa)
   - `attacker-takeover` (login, parol, OTP yoki sessiya bor bo'lsa)
   - `attacker-insider` (admin panel yoki admin buyruqlari bor bo'lsa)
   - `attacker-scraper` (foydalanuvchi ma'lumoti saqlansa)
   - `attacker-phisher` (bot, redirect, deep link yoki webhook bor bo'lsa)
   - `attacker-apk` (Android ilova bor bo'lsa)
   - `attacker-ai` (AI funksiyasi bor bo'lsa)
5. Barcha topilmalarni `redteam-skeptic` agentiga ber. U isbotsizini tashlaydi.
6. Xotirani yangila: topilmalarni JSON faylga yoz (`.vibeguard/last-run.json`, shakli `${CLAUDE_PLUGIN_ROOT}/skills/vibeguard/reference/scoring-and-memory.md` da) va `python3 "${CLAUDE_PLUGIN_ROOT}/skills/vibeguard/scripts/findings.py" merge .vibeguard/last-run.json` ni ishga tushir. Natijadagi doimiy ID'larni (VG-001...) va "yangi / qolgan / tuzatildi / qayta ochildi" ro'yxatini ishlat. Maqsad butun loyiha bo'lmasa (faqat bir qism), `--partial` qo'sh.
7. Tasdiqlangan topilmalarni ID'lari bilan `redteam-chain` agentiga ber. Zanjirlar sonini `findings.py merge ... --chains N` bilan qayta yoz yoki birinchi chaqiruvda ber.
   Zanjir agenti ko'rsatgan "uzadigan halqa" topilmalariga `"breaks_chain": true` qo'yib qayta `merge` qil.
8. Xavf bali va hukmni `findings.py score` dan ol. O'zing hisoblama. Shuningdek `findings.py top3` (bugun 3 ta ish), `findings.py budget` (vaqt byudjeti) va `findings.py board` (qizil va ko'k hisob) natijalarini hisobotning mos bo'limlariga qo'y.
9. `${CLAUDE_PLUGIN_ROOT}/skills/vibeguard/templates/report.<lang>.md` qolipi bo'yicha hisobotni foydalanuvchi tilida yoz va `.vibeguard/reports/` ga saqla. `<lang>` config'dagi til (`uz`, `uz-cyrl`, `ru`, `en`). Sirlarni yashir. `.vibeguard/` ni `.gitignore`ga qo'sh. Keyin HTML ko'rinishini ham yasa: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/vibeguard/scripts/report_html.py" --lang <lang> --title "<loyiha>"` va fayl yo'lini ayt (ulashishdan oldin ko'zdan kechirishni eslat).
10. Hisobot oxirida so'ra: "Tuzatishni boshlaymizmi?". Tasdiqsiz kodni o'zgartirma. Tasdiq bo'lsa `/vibeguard:fix` tartibi bo'yicha davom et.

Eslatma: faqat kod o'qiladi. Jonli sinov faqat localhost yoki foydalanuvchi aniq ko'rsatgan test muhitida. Production va uchinchi shaxs xizmatlariga so'rov yuborma. Tayyor exploit yozma.
