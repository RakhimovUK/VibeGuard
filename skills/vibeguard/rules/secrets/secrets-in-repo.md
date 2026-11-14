---
id: secrets-in-repo
soha: secrets
xavf: kritik
lesson: "Never hardcode tokens, keys or passwords; read them from environment variables and keep .env in .gitignore."
agent: attacker-token
---

# Sirlar repoda yoki frontend'da

## Nima qidiriladi
- `.env` fayli git'da kuzatilmoqda yoki `.gitignore`da yo'q.
- Kodda qattiq yozilgan token, API kalit, DB URL (`sk-`, `AKIA`, `ghp_`, bot tokeni naqshi `\d{8,10}:[A-Za-z0-9_-]{35}`).
- Frontend bundle yoki APK ichida `service_role`, maxfiy kalit, ichki URL.
- Git tarixida o'chirilgan, lekin hali ko'rinadigan sirlar.

## Nega xavfli
Repoga yoki frontend'ga tushgan sir hammaga ochiq. Hujumchi u bilan bot nomidan yozishi, bazaga kirishi yoki hisobingizga pul sarflashi mumkin. Faylni o'chirish yetarli emas: git tarixida qoladi.

## Yomon misol
```js
const BOT_TOKEN = "123456789:AAH..."   // kodga yozilgan
```

## Yaxshi misol
```js
const BOT_TOKEN = process.env.BOT_TOKEN
if (!BOT_TOKEN) throw new Error("BOT_TOKEN kerak")
```

## Tuzatish
1. **Avval sirni almashtir** (BotFather, Railway, Supabase panelidan). Bu "O'zingiz qilasiz" ro'yxatiga kiradi.
2. Sirni env o'zgaruvchisiga ko'chir, `.env` ni `.gitignore`ga qo'sh.
3. Tarixni tozalash (`git filter-repo`) faqat almashtirishdan keyin, ixtiyoriy.

Claude Code uchun prompt: "Koddagi barcha qattiq yozilgan sirlarni env o'zgaruvchilariga ko'chir, .env.example yarat, .env ni .gitignore'ga qo'sh. Sirlarning o'zini chiqarma."
