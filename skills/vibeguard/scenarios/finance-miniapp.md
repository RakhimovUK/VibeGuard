# Ssenariy: shaxsiy ma'lumot saqlaydigan Mini App

Misol: xarajatlar hisobi, kundalik, vazifalar, shaxsiy statistika.

## Nima himoyalanadi
- Har bir foydalanuvchining shaxsiy yozuvlari (moliyaviy odatlar, summalar, izohlar).
- Hisobga kirish: boshqa odam nomidan kirib bo'lmasligi.
- Baza va uning kalitlari.

## Hujumchi nima istaydi
Boshqaning yozuvlarini o'qish, butun bazani yig'ib olish, boshqaning yozuvlarini o'zgartirish yoki o'chirish, ilova nomidan foydalanuvchini aldash.

## Tekshiruv rejalari (ustuvorlik tartibida)

1. **Kimligini soxtalashtirish** (`attacker-user`; `bot-initdata`)
   - Har bir API so'rovida `initData` imzosi va muddati serverda tekshiriladimi?
   - Foydalanuvchi identifikatori faqat tasdiqlangan ma'lumotdan olinadimi?
2. **Boshqaning yozuvlari** (`attacker-user`; `webapp-idor`)
   - O'qish, o'zgartirish, o'chirish va eksport so'rovlarining har birida egalik tekshiriladimi? (Ko'pincha o'qish himoyalangan, o'chirish unutilgan.)
   - Umumiy hisob yoki oila rejimi bo'lsa: a'zolik serverda tekshiriladimi?
3. **Bazani to'g'ridan-to'g'ri o'qish** (`attacker-deploy`; `deploy-supabase-rls`)
   - Klient bazaga to'g'ridan-to'g'ri ulanadimi? RLS yoki qoidalar har jadvalda egalikka bog'langanmi?
   - Klient kodida keng huquqli kalit yo'qmi? (`secrets-in-repo`, `ai-key-in-frontend`)
4. **Ommaviy yig'ish** (`attacker-scraper`; `privacy-overexposed-fields`)
   - Ro'yxat va statistika endpoint'lari faqat o'z ma'lumotini qaytaradimi, limit bormi?
   - Javoblarda keragidan ortiq maydon yo'qmi? Identifikatorlar ketma-ketmi?
5. **Loglar va tahlil** (`attacker-scraper`; `privacy-logs-pii`)
   - Summalar, izohlar, `initData` logga yoki xato kuzatuv xizmatiga tushadimi?
6. **Foydalanuvchi matni ekranda** (`attacker-user`; `site-xss`)
   - Kategoriya nomi, izoh kabi matnlar HTML sifatida chiqariladimi?
7. **Kiritma va xatolar** (`attacker-outsider`; `bugs-unhandled-errors`, `webapp-sql-injection`)
   - Manfiy, juda katta yoki noto'g'ri turdagi qiymatlar nima qiladi?
8. **AI funksiyasi bo'lsa** (`attacker-ai`; `ai-prompt-injection`)
   - Bir foydalanuvchi ma'lumoti boshqasining so'roviga tushmaydimi?

## Hisobotda alohida ko'rsat
- Nima yig'iladi va qancha saqlanadi; foydalanuvchi o'z ma'lumotini o'chira oladimi.
- Eng yomon holat: bitta hujumchi nechta foydalanuvchi ma'lumotiga yetadi.
