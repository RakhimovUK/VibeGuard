# ATAYLAB XATO BILAN YOZILGAN SINOV KODI. ISHGA TUSHIRMANG.
# Barcha sirlar soxta.
import logging
import sqlite3

BOT_TOKEN = "1234567890:AAFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKE0"  # VG: secrets-in-repo
AI_KEY = "sk-FAKEFAKEFAKEFAKEFAKEFAKE1234"                     # VG: secrets-in-repo
ADMIN_IDS = [111111111]

db = sqlite3.connect("bot.db")


def on_message(message):
    # VG: privacy-logs-pii (butun xabar, telefon bilan logga ketadi)
    logging.info(f"Yangi xabar: {message}")


def cmd_addbalance(message):
    # VG: attacker-insider/user (admin tekshiruvi yo'q)
    _, user_id, amount = message["text"].split()
    db.execute(f"UPDATE users SET balance = balance + {amount} WHERE id = {user_id}")  # VG: webapp-sql-injection
    db.commit()


def on_payment(event):
    # VG: payments-idempotency (hodisa id saqlanmaydi, takror kelsa yana qo'shiladi)
    user_id = event["user_id"]
    db.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (event["amount"], user_id))
    db.commit()


def buy(user, price):
    # VG: bugs-race-condition (tekshir, keyin o'zgartir)
    row = db.execute("SELECT balance FROM users WHERE id = ?", (user,)).fetchone()
    if row[0] >= price:
        db.execute("UPDATE users SET balance = ? WHERE id = ?", (row[0] - price, user))
        db.commit()
        try:
            deliver(user)
        except:  # VG: bugs-unhandled-errors (xato yutiladi, pul qaytmaydi)
            pass


def cmd_ask(message):
    # VG: cost-no-rate-limit (pullik AI chaqiruvi limitsiz)
    # VG: ai-prompt-injection (tizim ko'rsatmasi va foydalanuvchi matni bitta satrda)
    prompt = "Sen yordamchisan. Maxfiy kod: 4242. Foydalanuvchi: " + message["text"]
    return call_ai(AI_KEY, prompt)


def deliver(user):
    raise NotImplementedError


def call_ai(key, prompt):
    raise NotImplementedError
