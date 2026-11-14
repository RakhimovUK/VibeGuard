# Yo'riqnoma: pul yoki balans yo'qoldi

Belgilar: balanslar hisobga to'g'ri kelmaydi, mahsulot to'lovsiz berilgan, bitta foydalanuvchida g'alati katta balans, bir xil to'lov ikki marta qayd etilgan, promo yoki referal cheksiz ishlatilgan.

## Birinchi 15 daqiqa: oqimni to'xtatish

1. **Pul chiqadigan yo'llarni vaqtincha to'xtat:** yechib olish, mahsulot yetkazish (masalan Stars yuborish), promo va referal bonuslari. Kirim (to'lov qabul qilish) ishlab tursa bo'ladi, lekin yetkazish navbatga tushsin.
2. Shubhali hisoblarni **muzlat**, o'chirma: yozuvlar dalil.
3. Admin huquqi orqali bo'lgan deb gumon qilsang: admin ro'yxatini tekshir, admin tokenlari va parollarini almashtir (`sir-sizdi.md`).
4. To'lov provayderi va yetkazuvchi xizmat balansini panelda tekshir: u yerdagi raqam haqiqat manbai.

## Keyingi 1 soat: qancha va qanday

- Solishtir: provayderdagi to'lovlar ro'yxati va bazadagi to'lovlar. Farqlar: bazada bor, provayderda yo'q (soxta tasdiq); bir provayder to'loviga bir nechta yetkazish (takror).
- Vaqt bo'yicha qara: bir soniyada bir foydalanuvchidan ko'p so'rov (poyga holati), bir xil hodisa identifikatori takrori (webhook takrori), manfiy yoki juda kichik summalar (klientdan kelgan narx).
- Balansi o'zgargan, lekin mos to'lov yozuvi yo'q hisoblar (admin yo'li yoki to'g'ridan-to'g'ri bazaga kirish).
- Umumiy zarar va ta'sirlangan hisoblar soni.

## Teshikni topish va yopish

1. `attacker-fraudster` ni to'lov va balans kodiga ishga tushir. Qoidalar: `payments-idempotency`, `bugs-race-condition`, `webapp-client-trust`, `bot-webhook-secret`.
2. `/vibeguard:fix`: har biri uchun test (takror hodisa balansni ikki marta oshirmaydi, bir vaqtdagi ikki so'rovdan bittasi o'tadi).
3. Qayta hujumdan keyingina to'xtatilgan yo'llarni och.

## Tiklash

- Noqonuniy berilgan balanslarni tuzatish: har bir o'zgarishni jurnalga yoz (kim, qachon, nega).
- Halol foydalanuvchilarga yetkazilmagan buyurtmalarni navbatdan chiqarib bajar.
- To'lov provayderi bilan bog'lanish kerak bo'lsa (qaytarish, nizo), buni foydalanuvchi o'zi qiladi.

## Keyin

- Har bir balans o'zgarishi uchun jurnal jadvali (audit log).
- Kunlik avtomatik solishtiruv: provayder va baza yig'indilari.
- Yirik summalar va admin amallari uchun limit va ikkinchi tasdiq.
- G'alati faollik uchun ogohlantirish (bir hisobdan qisqa vaqtda ko'p operatsiya).
