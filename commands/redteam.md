---
description: Red Team rejimi. Hujumchi ko'zi bilan loyihani tekshiradi, zaif joylarni va tuzatish yo'lini ko'rsatadi.
argument-hint: "[yo'l yoki qism: bot | webapp | site | apk | payments] [--hammasi]"
---

`vibeguard` skillini yukla va Red Team rejimini ishga tushir. Maqsad: $ARGUMENTS (bo'sh bo'lsa butun loyiha).

Qadamlar:

1. `.vibeguard/config.json` bor-yo'qligini tekshir. Yo'q bo'lsa: ruxsat tasdig'ini so'ra ("loyiha meniki yoki yozma ruxsatim bor") va tilni tanlat (uz-lotin, uz-kirill, ru, en). Tasdiqsiz davom etma.
2. `redteam-recon` agentini ishga tushir. U stack va qismlarni (bot, webapp, sayt, apk, to'lov, deploy) aniqlaydi. Keyin `${CLAUDE_PLUGIN_ROOT}/skills/vibeguard/scenarios/README.md` ni o'qi: loyiha turiga mos ssenariy bo'lsa, uni o'qib, tegishli hujumchi agentlarga "avval shu rejalarni tekshir" deb ber (ssenariy qidiruvni cheklamaydi).
3. Skriptlarni ishga tushir (tez, AI'siz) va natijasini agentlarga dalil sifatida ber:
   - `python3 "${CLAUDE_PLUGIN_ROOT}/skills/vibeguard/scripts/scan_secrets.py" <papka>`
   - `python3 "${CLAUDE_PLUGIN_ROOT}/skills/vibeguard/scripts/check_hygiene.py" <papka>`
   Python yo'q bo'lsa bu qadamni o'tkazib yubor va hisobotda ayt. gitleaks, semgrep, npm audit, pip-audit o'rnatilgan bo'lsa ularni ham ishlat (faqat o'qish rejimida).
4. **Hujumchilarni tanla va navbat bilan ishlat** (hammasini bir vaqtda EMAS: ulanish uzilishi va limitga urilish xavfi bor).
   a. Recon natijasiga qarab mos hujumchilarni tanla. Argumentda `--hammasi` bo'lsa, hammasini tanla. Mos kelmaganlarini "o'tkazib yuborildi: sababi" deb hisobotga yoz:
      - `attacker-outsider` (har doim)
      - `attacker-supply` (har doim: bog'liqliklar va CI)
      - `attacker-user` (login yoki foydalanuvchi ma'lumoti bor bo'lsa)
      - `attacker-token` (token, kalit, `.env`, bot tokeni bor bo'lsa)
      - `attacker-takeover` (kalit, sessiya, initData, oila/ulashish kodi yoki hisobga kirish bo'lsa)
      - `attacker-fraudster` (to'lov, Stars, balans, promo, referal bor bo'lsa)
      - `attacker-cost` (pullik API, hosting, AI chaqiruvlari bor bo'lsa)
      - `attacker-deploy` (Docker, Railway, Supabase/Firebase, baza sozlamalari bor bo'lsa)
      - `attacker-insider` (admin panel yoki admin buyruqlari bor bo'lsa)
      - `attacker-scraper` (foydalanuvchi ma'lumoti saqlansa)
      - `attacker-phisher` (bot, redirect, deep link yoki webhook bor bo'lsa)
      - `attacker-apk` (Android ilova bor bo'lsa)
      - `attacker-ai` (AI funksiyasi bor bo'lsa)
   b. Tanlanganlarni shu ustuvorlik tartibida to'p-to'p qil, **har to'pda 3 tadan ko'p emas**:
      1-to'p: `takeover`, `token`, `outsider` (hisobga kirish va kalit o'g'irlash)
      2-to'p: `user`, `fraudster`, `deploy` (boshqa odam ma'lumoti, pul, server)
      3-to'p: `cost`, `supply`, `ai`
      4-to'p: `apk`, `insider`, `scraper`, `phisher`
      Bo'sh qolgan joylarni keyingi to'p bilan to'ldirma, shunchaki ketma-ket davom et.
   c. To'pni ishga tushirishdan oldin vazifalar ro'yxatiga (TaskCreate) har agentni yoz. To'p tugagach darhol natijani `.vibeguard/progress.json` ga yoz (agent nomi, holati `tugadi|yiqildi|o'tkazildi`, topilmalar soni). To'plar orasida foydalanuvchiga bir qator xabar ber ("2/4 to'p tugadi, 7 topilma").
   d. Har agentga **qisqa va aniq** topshiriq ber: loyiha yo'li, recon xulosasidan faqat shu agentga tegishli qism (fayllar, endpointlar), `rules/` ichidan `agent:` maydoni uning nomiga teng qoidalarni o'qish, natija shakli (JSON massiv, fayl:qator dalili majburiy), "faqat o'qi". Uzun umumiy topshiriq berma, aniqlik pasayadi.
   e. Agent yiqilsa (ulanish xatosi, to'xtatilgan, bo'sh javob): **bir marta** qayta urin, bu safar yakka o'zi. Yana yiqilsa `progress.json` da `yiqildi` deb belgila, hisobotda "TEKSHIRILMADI" bo'limiga yoz (bu "xavfsiz" degani emas). Qolgan to'plarni to'xtatma.
   f. `.vibeguard/progress.json` allaqachon bor va to'liq bo'lmasa, foydalanuvchidan so'ra: "Davom ettiramizmi yoki boshidan boshlaymizmi?". Davom ettirsang, faqat `tugadi` bo'lmaganlarini ishlat.
5. Barcha topilmalarni `redteam-skeptic` agentiga ber. U isbotsizini tashlaydi.
6. Xotirani yangila: topilmalarni JSON faylga yoz (`.vibeguard/last-run.json`, shakli `${CLAUDE_PLUGIN_ROOT}/skills/vibeguard/reference/scoring-and-memory.md` da) va `python3 "${CLAUDE_PLUGIN_ROOT}/skills/vibeguard/scripts/findings.py" merge .vibeguard/last-run.json` ni ishga tushir. Natijadagi doimiy ID'larni (VG-001...) va "yangi / qolgan / tuzatildi / qayta ochildi" ro'yxatini ishlat. Maqsad butun loyiha bo'lmasa (faqat bir qism), `--partial` qo'sh.
7. Tasdiqlangan topilmalarni ID'lari bilan `redteam-chain` agentiga ber. Zanjirlar sonini `findings.py merge ... --chains N` bilan qayta yoz yoki birinchi chaqiruvda ber.
   Zanjir agenti ko'rsatgan "uzadigan halqa" topilmalariga `"breaks_chain": true` qo'yib qayta `merge` qil.
8. Xavf bali va hukmni `findings.py score` dan ol. O'zing hisoblama. Shuningdek `findings.py top3` (bugun 3 ta ish), `findings.py budget` (vaqt byudjeti) va `findings.py board` (qizil va ko'k hisob) natijalarini hisobotning mos bo'limlariga qo'y.
9. `${CLAUDE_PLUGIN_ROOT}/skills/vibeguard/templates/report.<lang>.md` qolipi bo'yicha hisobotni foydalanuvchi tilida yoz va `.vibeguard/reports/` ga saqla. `<lang>` config'dagi til (`uz`, `uz-cyrl`, `ru`, `en`). Sirlarni yashir. `.vibeguard/` ni `.gitignore`ga qo'sh. Keyin HTML ko'rinishini ham yasa: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/vibeguard/scripts/report_html.py" --lang <lang> --title "<loyiha>"` va fayl yo'lini ayt (ulashishdan oldin ko'zdan kechirishni eslat).
10. Hisobot oxirida so'ra: "Tuzatishni boshlaymizmi?". Tasdiqsiz kodni o'zgartirma. Tasdiq bo'lsa `/vibeguard:fix` tartibi bo'yicha davom et.

Eslatma: faqat kod o'qiladi. Jonli sinov faqat localhost yoki foydalanuvchi aniq ko'rsatgan test muhitida. Production va uchinchi shaxs xizmatlariga so'rov yuborma. Tayyor exploit yozma.
