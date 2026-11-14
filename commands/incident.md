---
description: Hodisa rejimi. Buzilish yoki sizish yuz berganda qadamma-qadam yo'riqnoma.
argument-hint: "[nima bo'ldi: token sizdi | ma'lumot sizdi | pul yo'qoldi | bilmayman]"
---

`vibeguard` skillini yukla va hodisa rejimini ishga tushir. Foydalanuvchi aytgani: $ARGUMENTS

Foydalanuvchi hozir xavotirda. Qisqa, xotirjam va tartib bilan gapir. Bir vaqtda bitta qadam.

1. **Nima bo'lganini aniqla** (aytilmagan bo'lsa bitta savol bilan): token yoki kalit sizdi / foydalanuvchilar ma'lumoti sizdi yoki baza ochiq qoldi / pul yoki balans yo'qoldi / g'alati xatti-harakat, sababi noma'lum.
2. Mos yo'riqnomani o'qi (`${CLAUDE_PLUGIN_ROOT}/skills/vibeguard/playbooks/`):
   - `sir-sizdi.md`
   - `malumot-sizdi.md`
   - `pul-yoqoldi.md`
   - Noma'lum bo'lsa: `sir-sizdi.md` dan boshla (eng ko'p uchraydigan va eng tez zarar beradigan holat).
3. **Avval to'xtatish, keyin tekshirish.** Yo'riqnomadagi "Birinchi 15 daqiqa" qadamlarini foydalanuvchi bilan birga bajar. Panellardagi ishlarni (BotFather, hosting, baza, to'lov provayderi) foydalanuvchi o'zi qiladi: sen qayerga kirish va nimani bosishni aytasan.
4. Kodda sen qila oladigan ishlar: sir qayerlarda ishlatilganini topish (`scan_secrets.py`), git tarixini o'qish, loglarni tahlil qilish (foydalanuvchi bersa), teshikni topish uchun tegishli hujumchi agentni ishga tushirish.
5. **Dalillarni saqla:** loglarni o'chirma, tarixni qayta yozma (`git filter-repo`, `push --force`) to hodisa tugamaguncha. Foydalanuvchi so'rasa ham avval oqibatini tushuntir.
6. Vaqt jadvalini yurit: `.vibeguard/incidents/<sana>.md` ga nima, qachon aniqlangani va qanday chora ko'rilganini yoz (sirlarsiz).
7. Yakunda: teshik yopilganini `/vibeguard:redteam` bilan tekshirishni taklif qil va "keyingi safar bo'lmasligi uchun" 3 ta aniq chora yoz.

Chegaralar: hech kimga "javob hujumi" qilinmaydi, begona tizimlar tekshirilmaydi. Huquqiy majburiyatlar (foydalanuvchilarni yoki davlat organini xabardor qilish) mamlakatga bog'liq: aniq maslahat berma, foydalanuvchiga mahalliy qonun talablarini tekshirishni yoki yuristga murojaat qilishni ayt.

Skriptlar joyi: `${CLAUDE_PLUGIN_ROOT}/skills/vibeguard/scripts/`. Chaqirish namunasi: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/vibeguard/scripts/findings.py" score`. Qoidalar: `${CLAUDE_PLUGIN_ROOT}/skills/vibeguard/rules/`.
