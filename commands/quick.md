---
description: Tezkor tekshiruv. Skriptlar va eng xavfli qoidalar, bir necha daqiqada.
argument-hint: "[yo'l]"
---

`vibeguard` skillini yukla va tezkor tekshiruvni ishga tushir. Maqsad: $ARGUMENTS (bo'sh bo'lsa butun loyiha).

1. `.vibeguard/config.json` yo'q bo'lsa: ruxsat tasdig'i va til (bir marta).
2. Skriptlarni ishga tushir: `scan_secrets.py` va `check_hygiene.py`.
3. Faqat ikkita agentni ishga tushir: `attacker-token` va `attacker-outsider`. Ularga faqat `xavf: kritik` bo'lgan qoidalarni o'qishni ayt.
4. Skeptik va zanjir bosqichlari yo'q. Har bir topilmada `fayl:qator` dalili bo'lsin, bo'lmasa "taxmin" deb belgila.
5. Qisqa natija (to'liq hisobot emas): topilmalar ro'yxati, har biriga bir jumla va tuzatish yo'li. Sirlarni yashir.
6. Topilmalarni xotiraga yoz: `findings.py merge --partial` (tezkor tekshiruv to'liq emas, shuning uchun topilmagan eski topilmalar "tuzatildi" deb belgilanmaydi).
7. Oxirida ayt: "Bu tezkor tekshiruv. To'liq hujum uchun: `/vibeguard:redteam`."

Faqat kod o'qiladi. Hech narsa o'zgartirilmaydi.

Skriptlar joyi: `${CLAUDE_PLUGIN_ROOT}/skills/vibeguard/scripts/`. Chaqirish namunasi: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/vibeguard/scripts/findings.py" score`. Qoidalar: `${CLAUDE_PLUGIN_ROOT}/skills/vibeguard/rules/`.
