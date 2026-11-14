---
id: payments-idempotency
soha: payments
xavf: yuqori
lesson: "Make payment and webhook handlers idempotent: store the event id under a unique index and change balances inside one transaction."
agent: attacker-fraudster
---

# To'lov va webhook idempotentligi yo'q

## Nima qidiriladi
- To'lov tasdig'i webhook yoki callback orqali keladi va mahsulot/balans darhol beriladi.
- Hodisa identifikatori (`payment_id`, `charge_id`, `update_id`) bazada saqlanib, qayta kelganda tekshirilmaydi.
- Balansni "o'qi, hisobla, yoz" ketma-ketligida o'zgartirish, tranzaksiyasiz.

## Nega xavfli
Bir xil to'lov hodisasi ikki marta kelsa (provayder qayta yuborishi yoki hujumchi takrorlashi), mahsulot yoki balans ikki marta beriladi. Bir vaqtdagi ikki so'rov ham balansni ikki marta ishlatishi mumkin.

## Yomon misol
```python
def on_payment(event):
    user.balance += event.amount   # takror kelsa yana qo'shiladi
    user.save()
```

## Yaxshi misol
```python
def on_payment(event):
    with db.transaction():
        if Payment.exists(event.id):   # unique indeks bilan
            return
        Payment.create(id=event.id)
        user.balance += event.amount
        user.save()
```

## Tuzatish
`payment_id` ustiga unique indeks qo'y, tekshirish va yozishni bitta tranzaksiyada qil, webhook imzosini tekshir.

Claude Code uchun prompt: "To'lov qayta ishlash funksiyasini idempotent qil: hodisa id'si unique saqlansin, balans o'zgarishi tranzaksiyada bo'lsin, takror hodisa e'tiborsiz qoldirilsin va buning uchun test yoz."
