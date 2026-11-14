# Ssenariy: pul yoki raqamli tovar sotadigan bot

Misol: Telegram Stars sotish, obuna, ichki balans, raqamli mahsulot yetkazish.

## Nima himoyalanadi
- Pul oqimi: to'lov qabul qilish, balans, yetkazish (masalan Stars yuborish).
- Yetkazuvchi xizmat hisobi va kalitlari (to'lov provayderi, Fragment yoki shunga o'xshash).
- Foydalanuvchilar balansi va buyurtmalar tarixi.

## Hujumchi nima istaydi
To'lamasdan olish, bir marta to'lab ikki marta olish, boshqaning balansini sarflash, admin bo'lib balans yozish, yetkazuvchi hisobni bo'shatish.

## Tekshiruv rejalari (ustuvorlik tartibida)

1. **To'lamasdan olish** (`attacker-fraudster`; `webapp-client-trust`, `bot-webhook-secret`)
   - "To'landi" holati qayerda o'rnatiladi? Provayder tasdig'i serverda tekshiriladimi yoki klient/webhook so'ziga ishoniladimi?
   - Narx va miqdor qayerdan olinadi: serverdagi katalogdanmi yoki so'rovdanmi?
   - Webhook maxfiy tokeni va provayder imzosi tekshiriladimi?
2. **Bir to'lovga ikki yetkazish** (`attacker-fraudster`; `payments-idempotency`, `bugs-race-condition`)
   - Hodisa identifikatori unique saqlanadimi?
   - Balans yechish va yetkazish bitta tranzaksiyadami? Bir vaqtdagi ikki so'rov nima qiladi?
   - Yetkazish yiqilsa: pul qaytadimi, qayta urinishda ikki marta yetkazilmaydimi? (`bugs-unhandled-errors`)
3. **Boshqaning balansi** (`attacker-user`; `bot-initdata`, `webapp-idor`)
   - Foydalanuvchi kimligi faqat tasdiqlangan manbadan olinadimi?
   - Buyurtma va balans so'rovlarida egalik tekshiriladimi?
4. **Admin yo'li** (`attacker-insider`)
   - Balans qo'shish, qaytarish, narx o'zgartirish buyruqlarida rol serverda tekshiriladimi?
   - Admin amallari jurnalga yoziladimi, limit bormi?
5. **Yetkazuvchi hisob kalitlari** (`attacker-token`; `secrets-in-repo`)
   - Kalitlar qayerda, huquqi qanchalik keng, sizsa nima yo'qotiladi?
   - Yetkazuvchi hisobda kunlik limit yoki ogohlantirish bormi?
6. **Promo va referal** (`attacker-fraudster`)
   - Bir martalik cheklov unique bilan ta'minlanganmi, o'zini o'zi taklif qilish mumkinmi?
7. **Xarajat** (`attacker-cost`; `cost-no-rate-limit`)
   - Buyurtma yaratish va to'lov havolasi olishda limit bormi?

## Hisobotda alohida ko'rsat
- Provayder va baza yig'indilarini solishtirish yo'li bormi (kunlik tekshiruv).
- Eng yomon holatda bir kechada qancha yo'qotish mumkin (raqamsiz bo'lsa tavsif).
