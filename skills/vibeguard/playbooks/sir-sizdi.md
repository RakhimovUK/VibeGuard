# Yo'riqnoma: token yoki kalit sizdi

Belgilar: sir GitHub'ga tushdi, skrinshot yoki chatda ko'rindi, bot o'zidan-o'zi xabar yubormoqda, AI yoki hosting hisobi keskin o'sdi, provayder "kalitingiz ochiq" deb xat yubordi.

## Birinchi 15 daqiqa: sirni o'ldirish

Sirni koddan o'chirish **yetarli emas**: uni ko'rgan odamda nusxasi bor. Yagona yechim eskisini bekor qilib, yangisini chiqarish.

1. **Qaysi sir(lar) sizganini aniqla.** Shubha bo'lsa, o'sha fayldagi hammasini sizgan deb hisobla.
2. **Eskisini bekor qil, yangisini ol** (foydalanuvchi o'zi, tegishli panelda):
   - Telegram bot tokeni: BotFather'da botni tanlab, tokenni bekor qilish (revoke). Yangi token beriladi, eskisi darhol ishlamay qoladi.
   - AI va boshqa API kalitlari: provayder panelidagi kalitlar bo'limida eskisini o'chirib, yangisini yaratish.
   - Baza paroli yoki ulanish manzili: baza xizmati panelida parolni almashtirish.
   - Supabase/Firebase xizmat kalitlari: loyiha sozlamalaridagi API kalitlari bo'limi.
   - GitHub tokeni, deploy kalitlari: hisob sozlamalarida bekor qilish.
   - Panel tugmalari o'zgarib turadi: aniq yo'l topilmasa, provayderning rasmiy hujjatidan "rotate" yoki "revoke" bo'limini qidir.
3. **Yangi sirni faqat hosting muhit o'zgaruvchilariga qo'y** (masalan Railway'da Variables). Kodga va chatga yozma.
4. **Xizmatni qayta ishga tushir** va ishlayotganini tekshir.
5. Telegram bot uchun: webhook manzili o'zgartirilmaganini tekshir va kerak bo'lsa qayta o'rnat (maxfiy token bilan).

## Keyingi 1 soat: nima zarar bo'ldi

- Provayder panelidagi foydalanish tarixi: g'alati vaqt, hajm, manzillar.
- Bot: tanilmagan xabarlar, o'zgargan webhook, o'zgargan bot nomi yoki tavsifi.
- Baza: yangi yoki o'zgargan yozuvlar, ayniqsa admin, balans va to'lov jadvallarida.
- Hosting: tanilmagan deploy'lar, yangi muhit o'zgaruvchilari, yangi jamoa a'zolari.
- Sir qachondan beri ochiq edi: `git log` bilan birinchi paydo bo'lgan commit sanasini top.

## Kodni tozalash

1. `scan_secrets.py` bilan sir qolgan barcha joylarni top.
2. Koddagi qiymatlarni muhit o'zgaruvchisidan o'qishga o'tkaz, `.env` ni `.gitignore`ga qo'sh.
3. Git tarixini tozalash ixtiyoriy va faqat sir almashtirilgandan keyin: almashtirilgan sir tarixda qolsa ham foydasiz. Repo ommaviy bo'lsa va tarixda boshqa nozik narsa bo'lsa, tozalashni alohida rejalashtir (hamkorlarning nusxalari buziladi).

## Keyin

- `/vibeguard:guard on`: sir kodga qayta yozilishini to'xtatadi.
- Provayder panellarida xarajat chegarasi va ogohlantirish o'rnat.
- Har bir muhit (test, production) uchun alohida kalit, minimal huquq bilan.
- Hisoblarda ikki bosqichli tasdiqlashni yoq.
