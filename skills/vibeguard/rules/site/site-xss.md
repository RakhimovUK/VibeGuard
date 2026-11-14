---
id: site-xss
soha: site
xavf: yuqori
lesson: "Render user text as text (textContent, auto-escaping); sanitize if HTML is required; escape user text in bot messages with parse_mode."
agent: attacker-user
---

# Foydalanuvchi matnini HTML sifatida chiqarish (XSS)

## Nima qidiriladi
- `innerHTML`, `outerHTML`, `document.write`, `insertAdjacentHTML` ga foydalanuvchi ma'lumoti beriladi.
- React `dangerouslySetInnerHTML`, Vue `v-html`, shablonlarda `| safe`, `{{{ }}}`, `<%- %>`.
- Bot: foydalanuvchi matni `parse_mode=HTML/Markdown` bilan tozalanmasdan boshqalarga yuboriladi.

## Nega xavfli
Bir foydalanuvchi kiritgan matn boshqasining brauzerida kod bo'lib ishlaydi: sessiyani o'g'irlash, uning nomidan amal bajarish, soxta forma ko'rsatish mumkin.

## Yomon misol
```js
el.innerHTML = comment.text
```

## Yaxshi misol
```js
el.textContent = comment.text
```

## Tuzatish
Matnni matn sifatida chiqar. HTML kerak bo'lsa, ishonchli tozalovchi kutubxonadan o'tkaz. Sessiya cookie'siga `HttpOnly` qo'y va Content-Security-Policy sarlavhasini yoq.

Claude Code uchun prompt: "Foydalanuvchi ma'lumoti HTML sifatida chiqariladigan joylarni top, matn sifatida chiqarishga o'tkaz yoki tozalovchidan o'tkaz, va teg ichidagi kiritma matn bo'lib ko'rinishini test bilan isbotla."
