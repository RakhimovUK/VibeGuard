---
id: deploy-supabase-rls
soha: deploy
xavf: kritik
lesson: "Enable RLS with ownership policies on every table; service_role keys stay on the server only."
agent: attacker-deploy
---

# Supabase/Firebase qoidalari ochiq

## Nima qidiriladi
- Supabase migratsiyalarida jadval yaratilgan, lekin `enable row level security` yo'q, yoki siyosat `using (true)`.
- Klient kodida `service_role` kaliti.
- Firebase qoidalarida `allow read, write: if true;` yoki faqat `request.auth != null` (har qanday ro'yxatdan o'tgan odam hammasini o'qiydi).
- Ochiq (public) storage bucket ichida shaxsiy fayllar.

## Nega xavfli
Bu xizmatlarda baza to'g'ridan-to'g'ri internetga ochiq, yagona himoya shu qoidalar. Qoida ochiq bo'lsa, ilovadagi anon kalit bilan butun jadvalni o'qish va o'zgartirish mumkin.

## Yomon misol
```sql
create table orders (id bigint, user_id uuid, total int);
-- RLS yoqilmagan
```

## Yaxshi misol
```sql
alter table orders enable row level security;
create policy "o'z buyurtmalari" on orders
  for select using (auth.uid() = user_id);
```

## Tuzatish
Har bir jadvalda RLS yoq va har amal (select, insert, update, delete) uchun egalik sharti yoz. `service_role` faqat serverda bo'lsin. Paneldagi haqiqiy holatni foydalanuvchi o'zi tekshiradi ("O'zingiz tekshirasiz" ro'yxatiga yoz).

Claude Code uchun prompt: "Barcha jadvallar uchun RLS yoqadigan va egalikka asoslangan siyosatlar yozadigan migratsiya tayyorla, service_role kaliti klient kodida ishlatilmasligini tekshir."
