# VibeGuard

O'zbekcha (lotin) · [Ўзбекча (кирилл)](README.uz-cyrl.md) · [Русский](README.ru.md) · [English](README.en.md)

Vibecoding bilan yozilgan loyihalarni (Telegram bot, Mini App, sayt, APK) xavfsizlik va xatolarga tekshiradigan Claude Code plagini. **Red Team** rejimida 13 xil hujumchi ko'zi bilan kodni o'qiydi, zaif joylarni topadi, tuzatish yo'lini ko'rsatadi va tasdiq bilan tuzatadi.

> Faqat o'zingizga tegishli yoki yozma ruxsat olingan loyihalarda ishlating. Kafolat yo'q. MIT litsenziya.

## O'rnatish (Claude Code)

```
/plugin marketplace add RakhimovUK/vibeguard
/plugin install vibeguard@vibeguard
```

## Buyruqlar

| Buyruq | Nima qiladi |
|---|---|
| `/vibeguard:redteam [qism]` | To'liq hujum: skriptlar, hujumchilar, skeptik, zanjirlar, hisobot |
| `/vibeguard:quick` | Tezkor: sirlar va kritik xatolar |
| `/vibeguard:ship` | Chiqarishdan oldin: faqat oxirgi o'zgarishlar, "tayyor / tayyor emas" |
| `/vibeguard:fix VG-001` | Tasdiq bilan tuzatish: test, alohida branch, qayta hujum |
| `/vibeguard:guard on` | Qo'riqchi: kodga sir yozilsa to'xtatadi |
| `/vibeguard:rules` | Topilgan xatolardan `CLAUDE.md` ga loyiha qoidalari |
| `/vibeguard:incident` | Sizish yoki buzilishda qadamma-qadam yo'riqnoma |
| `/vibeguard:lang ru` | Til: `uz`, `uz-cyrl`, `ru`, `en` |

Birinchi ishga tushishda ruxsat tasdig'i va til so'raladi.

## Hisobotda nima bor

- Xavf bali (0-100) va hukm: chiqarishga tayyor / tayyor emas.
- **Bugun 3 ta ish:** eng muhim uchta tuzatish.
- **Vaqt byudjeti:** hujumchi 10 daqiqada, 1 kunda, 1 haftada nimaga yetadi.
- **Hujum zanjirlari:** mayda xatolar birga qanday katta zarar beradi va qaysi bitta tuzatish zanjirni uzadi.
- Har bir topilma (`VG-001`): qayerda, dalil, hujumchi darajasi, hujum yo'li, tuzatish, tuzatilmasa nima bo'ladi, Claude Code uchun tayyor prompt.
- "O'zingiz qilasiz" ro'yxati (masalan, sizgan tokenni almashtirish).
- Qizil va ko'k hisob, qayta hujum natijasi. HTML ko'rinishi ham yasaladi.

## Hujumchilar

| Agent | Kim |
|---|---|
| attacker-outsider | anonim tashqi hujumchi |
| attacker-user | yomon niyatli foydalanuvchi |
| attacker-token | tokeni qo'lga tushgan hujumchi |
| attacker-fraudster | to'lov va mantiq firibgari |
| attacker-cost | xarajat hujumchisi |
| attacker-supply | bog'liqliklar va CI orqali hujum |
| attacker-deploy | infratuzilma hujumchisi |
| attacker-takeover | akkaunt o'g'risi |
| attacker-insider | sobiq admin yoki xodim |
| attacker-scraper | ma'lumot yig'uvchi |
| attacker-phisher | soxtalashtiruvchi |
| attacker-apk | APKni ochib o'qiydigan hujumchi |
| attacker-ai | AI funksiyasini aldovchi |

Skeptik agent har bir topilmani qayta tekshiradi. Isbotsiz topilma hisobotga kirmaydi.

## Xavfsizlik chegaralari

- Sukut bo'yicha faqat kod o'qiladi. Jonli sinov faqat localhost yoki siz ko'rsatgan test muhitida.
- Tayyor exploit yozilmaydi.
- Kod faqat tasdiqdan keyin, alohida branch'da o'zgaradi. Push, merge va deploy sizda qoladi.
- Toza hisobot xavfsizlik kafolati emas.

## Boshqa vositalar va CI

- Cursor, Codex va shunga o'xshashlar: `adapters/AGENTS.md`.
- GitHub'da har PR'ni tekshirish: `adapters/github-action/vibeguard.yml` (faqat skriptlar qatlami, AI'siz).
- Qo'riqchi rejimi `python3` talab qiladi.

## Holat

v0.6. Skriptlar va qo'riqchi sinov loyihalarida sinalgan (`python3 skills/vibeguard/scripts/selftest.py`). Hujumchi agentlar aniqligi hali o'lchanmagan: natijalaringizni issue orqali yuboring. Hissa qo'shish: `CONTRIBUTING.md`. Zaiflik haqida xabar: `SECURITY.md`.
