# Ssenariy: havoladan kontent yuklaydigan bot

Misol: foydalanuvchi video yoki musiqa havolasini yuboradi, bot faylni yuklab qaytaradi.

## Nima himoyalanadi
- Server resurslari: trafik, disk, protsessor, hosting hisobi.
- Serverning ichki tarmog'i va muhit o'zgaruvchilari.
- Tashqi platformalar uchun hisob ma'lumotlari (cookie, API kalitlar).
- Bot tokeni va foydalanuvchilar ro'yxati.

## Hujumchi nima istaydi
Xizmatni to'xtatish yoki hisobni oshirish, server ichidagi narsalarni o'qish, serverda buyruq bajarish, botdan boshqalarga zararli kontent tarqatish.

## Tekshiruv rejalari (ustuvorlik tartibida)

1. **Havola serverni ichkariga yo'naltiradi** (`attacker-outsider`; `cost-unbounded-input`)
   - Foydalanuvchi bergan URL tekshiriladimi: faqat http/https, ichki va mahalliy manzillar taqiqlanganmi, yo'naltirishlardan keyin ham?
   - Ruxsat etilgan platformalar ro'yxati bormi yoki istalgan manzil qabul qilinadimi?
2. **Havola buyruqqa aylanadi** (`attacker-user`)
   - Yuklash vositasi (yt-dlp, ffmpeg va boshqalar) qanday chaqiriladi: argumentlar ro'yxati bilanmi yoki shell satri bilanmi?
   - Foydalanuvchi matni argument yoki fayl nomi ichiga tushadimi? Fayl nomi tozalanadimi (`../`, maxsus belgilar)?
3. **Resursni yeb qo'yish** (`attacker-cost`; `cost-no-rate-limit`, `cost-unbounded-input`)
   - Foydalanuvchi bo'yicha limit, bir vaqtdagi vazifalar soni, navbat uzunligi cheklanganmi?
   - Fayl hajmi va davomiyligi yuklashdan **oldin** tekshiriladimi? Timeout bormi?
   - Vaqtinchalik fayllar xato holatida ham tozalanadimi?
4. **Platforma hisob ma'lumotlari** (`attacker-token`; `secrets-in-repo`, `privacy-logs-pii`)
   - Cookie va kalitlar qayerda saqlanadi, logga yoki xato xabariga chiqmaydimi?
5. **Vositalar va paketlar** (`attacker-supply`)
   - Yuklash vositalari versiyasi qotirilganmi, qayerdan o'rnatiladi?
6. **Bot orqali tarqatish** (`attacker-phisher`; `site-xss`)
   - Kontent sarlavhasi yoki tavsifi foydalanuvchiga `parse_mode` bilan tozalanmasdan yuboriladimi?
   - Kesh: bir foydalanuvchi yuklagan fayl boshqasiga noto'g'ri berilishi mumkinmi?
7. **Konteyner** (`attacker-deploy`; `deploy-docker-secrets`)
   - Jarayon root bilan ishlaydimi, fayl tizimiga yozish cheklanganmi?

## Hisobotda alohida ko'rsat
- Bitta foydalanuvchi bir soatda qancha trafik va disk sarflatishi mumkin.
- Eng yomon holat: serverda buyruq bajarish yo'li bormi yoki yo'qmi (aniq javob).
