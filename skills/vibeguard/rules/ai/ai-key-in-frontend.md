---
id: ai-key-in-frontend
soha: ai
xavf: kritik
lesson: "AI API keys stay on the server; add per-user quotas and max_tokens limits to AI endpoints."
agent: attacker-ai
---

# AI API kaliti frontend'da va limitsiz

## Nima qidiriladi
- Brauzer, Mini App yoki APK kodi AI provayderiga to'g'ridan-to'g'ri murojaat qiladi.
- Kalit `NEXT_PUBLIC_`, `VITE_`, `REACT_APP_`, `EXPO_PUBLIC_` kabi ommaviy o'zgaruvchida.
- Backend'dagi AI endpoint'ida foydalanuvchi bo'yicha limit va maksimal token cheklovi yo'q.

## Nega xavfli
Frontend'dagi kalitni har kim ko'chirib olib, sizning hisobingizdan foydalanadi. Limitsiz backend endpoint ham xuddi shunday: bitta odam bir kechada katta hisob chiqarishi mumkin.

## Yomon misol
```js
fetch('https://api.provider.com/v1/chat', {
  headers: { Authorization: `Bearer ${import.meta.env.VITE_AI_KEY}` }
})
```

## Yaxshi misol
```js
// frontend
fetch('/api/chat', { method: 'POST', body: JSON.stringify({ text }) })

// backend: kalit serverda, foydalanuvchi bo'yicha kunlik limit, max_tokens cheklangan
```

## Tuzatish
Kalitni serverga ko'chir va eski kalitni almashtir. Backend'da autentifikatsiya, foydalanuvchi bo'yicha kvota, `max_tokens` va kirish uzunligi cheklovini qo'y. Provayder panelida oylik xarajat chegarasini o'rnat ("O'zingiz qilasiz").

Claude Code uchun prompt: "AI chaqiruvlarini backend orqali o'tkaz, kalitni server muhit o'zgaruvchisiga ko'chir, foydalanuvchi bo'yicha kunlik limit va max_tokens cheklovini qo'sh."
