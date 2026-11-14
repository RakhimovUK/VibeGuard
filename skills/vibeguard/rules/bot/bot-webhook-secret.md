---
id: bot-webhook-secret
soha: bot
xavf: yuqori
lesson: "Set a webhook secret_token and verify it on every webhook request; verify payment provider signatures."
agent: attacker-phisher
---

# Webhook maxfiy tokeni tekshirilmaydi

## Nima qidiriladi
- Telegram webhook endpoint'i `X-Telegram-Bot-Api-Secret-Token` sarlavhasini tekshirmaydi.
- `setWebhook` chaqiruvida `secret_token` berilmagan.
- To'lov provayderi webhook'ida imzo tekshiruvi yo'q.
- Webhook manzili taxmin qilinadigan (`/webhook`, `/bot`).

## Nega xavfli
Manzilni bilgan har kim serverga soxta "Telegram" yoki "to'lov" hodisasini yubora oladi: istalgan foydalanuvchi nomidan buyruq, soxta to'lov tasdig'i.

## Yomon misol
```python
@app.post("/webhook")
async def webhook(request):
    await dp.feed_update(bot, await request.json())
```

## Yaxshi misol
```python
@app.post("/webhook")
async def webhook(request):
    got = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
    if not hmac.compare_digest(got, WEBHOOK_SECRET):
        return Response(status_code=403)
    await dp.feed_update(bot, await request.json())
```

## Tuzatish
`setWebhook` da `secret_token` o'rnat va har so'rovda doimiy vaqtli solishtirish bilan tekshir. To'lov webhook'larida provayder hujjatidagi imzo tekshiruvini qo'lla.

Claude Code uchun prompt: "Telegram webhook'iga secret_token qo'sh va sarlavhani tekshir, to'lov webhook'larida imzoni tekshir va noto'g'ri tokenli so'rov 403 olishini test bilan isbotla."
