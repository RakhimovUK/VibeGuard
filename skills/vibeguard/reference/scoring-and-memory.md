# Xavf bali va topilmalar xotirasi

Ikkalasi ham `scripts/findings.py` orqali hisoblanadi. Balni o'zing taxmin qilma: skript natijasini ishlat.

## Xotira: `.vibeguard/findings.json`

- Har bir topilma doimiy ID oladi: `VG-001`, `VG-002`...
- ID barmoq iziga bog'langan: qoida + fayl + kod parchasi (bo'shliqlarsiz). Qator raqami o'zgarsa ID saqlanadi. Fayl ko'chirilsa yoki kod qayta yozilsa yangi ID beriladi.
- Holatlar: `open` (ochiq), `fixed` (tuzatildi). Tuzatilgan topilma qayta topilsa "qayta ochildi" deb chiqadi.
- To'liq tekshiruvda (`redteam`) bu safar topilmagan ochiq topilmalar `fixed` bo'ladi.
- Qisman tekshiruvda (`quick`, `ship`, `fix`) `--partial` ishlatiladi: topilmaganlar o'zgarmaydi.
- `.vibeguard/` `.gitignore`da bo'lishi kerak. Xotiraga sir qiymati yozilmaydi (`snippet` saqlanmaydi, faqat barmoq izi).

Agentlar topilmani shu shaklda qaytaradi:

```json
{"rule": "webapp-idor", "file": "src/api.js", "line": 42,
 "severity": "yuqori", "status": "tasdiqlandi",
 "title": "Buyurtma egasi tekshirilmaydi",
 "snippet": "res.json(await Order.findById(req.params.id))",
 "agent": "attacker-user",
 "level": "havaskor", "breaks_chain": false}
```

## Hujumchi darajasi (`level`)

| Daraja | Kim | Vaqt byudjeti |
|---|---|---|
| `havaskor` | oddiy brauzer yoki tayyor vosita bilan, kod yozmaydi | 10 daqiqa |
| `tajribali` | kod yozishni va so'rovlarni o'zgartirishni biladi | 1 kun |
| `maqsadli` | aynan shu loyihani o'rgangan, sabr bilan ishlaydi | 1 hafta |

Daraja xavf darajasidan mustaqil: past darajali hujumchi uddalaydigan kritik xato eng shoshilinchi.

## Qo'shimcha buyruqlar

- `findings.py top3`: **bugun 3 ta ish**. Tartib: xavf darajasi, keyin zanjirni uzadigan (`breaks_chain`), keyin eng oson ishlatiladigan. Faqat tasdiqlangan ochiq topilmalar.
- `findings.py budget`: **vaqt byudjeti**. 10 daqiqa / 1 kun / 1 hafta ichida hujumchi yeta oladigan topilmalar (jamlanib boradi).
- `findings.py board`: **qizil va ko'k hisob**. Qizil: ochiq topilmalar. Ko'k: tuzatilganlar va qo'riqchi to'xtatgan sirlar soni (`.vibeguard/guard-stats.json`).

## Xavf bali (0-100)

| Xavf darajasi | Og'irlik |
|---|---|
| kritik | 40 |
| yuqori | 15 |
| o'rta | 5 |
| past | 1 |

- "Taxmin" holatidagi topilma yarim og'irlik oladi.
- Har bir tasdiqlangan hujum zanjiri +10, ko'pi bilan +20.
- Yig'indi 100 dan oshmaydi. Faqat ochiq topilmalar hisoblanadi.

## Hukm

- **Tayyor emas:** kamida bitta tasdiqlangan kritik topilma bor, yoki bal 30 va undan yuqori.
- **Tayyor:** aks holda. Bal 0 bo'lmasa, qolgan topilmalarni eslat.

Bal xavfsizlik kafolati emas: u faqat topilgan xatolarni o'lchaydi. Hisobotda buni bir jumla bilan ayt.
