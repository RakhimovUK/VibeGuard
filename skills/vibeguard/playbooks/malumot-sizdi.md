# Yo'riqnoma: foydalanuvchilar ma'lumoti sizdi yoki baza ochiq qoldi

Belgilar: baza yoki storage internetdan parolsiz ochilmoqda, kimdir foydalanuvchilar ro'yxatini ko'rsatdi, API boshqa odam ma'lumotini qaytarmoqda, loglar ochiq joyda.

## Birinchi 15 daqiqa: eshikni yopish

1. **Ochiq joyni yop** (foydalanuvchi o'zi, panelda): baza va storage'ni ommaviy kirishdan ol, ochiq qoidalarni (Supabase RLS, Firebase rules) vaqtincha "hech kim" ga o'tkaz. Xizmat qisman to'xtasa ham, bu ma'lumot oqib turishidan yaxshi.
2. Teshik kodda bo'lsa (masalan, egalik tekshirilmaydigan endpoint): o'sha endpoint'ni vaqtincha o'chir yoki xizmatni texnik ishlar rejimiga o'tkaz.
3. **Bazaga kirish kalitlarini almashtir** (`sir-sizdi.md` bo'yicha): hujumchi kalitni ko'chirib olgan bo'lishi mumkin.
4. **Hech narsani o'chirma:** loglar va baza holati dalil. Imkon bo'lsa bazaning zaxira nusxasini ol.

## Keyingi 1 soat: nima sizdi

- Qaysi jadval va fayllar ochiq edi va ularda nima bor: ism, telefon, email, to'lov ma'lumoti, parol xeshlari, xabarlar.
- Qachondan beri ochiq: deploy va sozlama o'zgarishlari tarixi.
- Kim kirgan: baza va hosting loglari, g'alati katta hajmli so'rovlar, tanilmagan manzillar.
- Taxminan nechta foydalanuvchi ta'sirlangan.

Aniq bilmasang, "bilmaymiz" deb yoz. Zararni kichraytirib ko'rsatma.

## Teshikni topish va yopish

1. `/vibeguard:redteam` yoki tegishli hujumchilar (`attacker-deploy`, `attacker-scraper`, `attacker-user`).
2. `/vibeguard:fix` bilan tuzatish va qayta hujum.
3. Tuzatilgandan keyingina xizmatni to'liq yoq.

## Foydalanuvchilarga xabar

Parol xeshlari, to'lov ma'lumoti yoki shaxsiy yozishmalar sizgan bo'lsa, foydalanuvchilar o'zini himoya qilishi uchun bilishi kerak. Xabar loyihasi:

- Nima bo'ldi va qachon (sodda, aybni yumshatmasdan).
- Qaysi ma'lumot ta'sirlangan va qaysi biri ta'sirlanmagan.
- Biz nima qildik.
- Foydalanuvchi nima qilishi kerak (parolni almashtirish, shubhali xabarlarga ishonmaslik).
- Savollar uchun rasmiy aloqa kanali.

Huquqiy majburiyatlar (muddatlar, kimga xabar berish) mamlakatga bog'liq: mahalliy shaxsiy ma'lumotlar qonunchiligini tekshir yoki yuristga murojaat qil. VibeGuard huquqiy maslahat bermaydi.

## Keyin

- Faqat kerakli ma'lumotni yig'ish va saqlash muddatini belgilash.
- Loglardan shaxsiy ma'lumotni olib tashlash.
- Zaxira nusxa va uni tiklashni sinab ko'rish.
