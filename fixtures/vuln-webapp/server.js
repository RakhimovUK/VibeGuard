// ATAYLAB XATO BILAN YOZILGAN SINOV KODI. ISHGA TUSHIRMANG.
// Barcha sirlar soxta.
const express = require('express')
const cors = require('cors')
const db = require('./db')

const app = express()
app.use(cors({ origin: '*', credentials: true }))   // VG: deploy-debug-prod (keng CORS)
app.use(express.json({ limit: '500mb' }))           // VG: cost-unbounded-input

// VG: bot-initdata (user id klientdan olinadi, initData tekshirilmaydi)
app.post('/api/balance', async (req, res) => {
  const user = await db.get('SELECT * FROM users WHERE id = ?', [req.body.userId])
  res.json(user)                                    // VG: privacy-overexposed-fields
})

// VG: webapp-idor (egalik tekshirilmaydi)
app.get('/api/orders/:id', async (req, res) => {
  res.json(await db.get('SELECT * FROM orders WHERE id = ?', [req.params.id]))
})

// VG: webapp-sql-injection
app.get('/api/search', async (req, res) => {
  res.json(await db.all("SELECT id, name FROM products WHERE name LIKE '%" + req.query.q + "%'"))
})

// VG: webapp-client-trust (narx klientdan)
app.post('/api/buy', async (req, res) => {
  await db.run('UPDATE users SET balance = balance - ? WHERE id = ?', [req.body.price, req.body.userId])
  res.json({ ok: true })
})

// VG: site-open-redirect
app.get('/go', (req, res) => res.redirect(req.query.url))

// VG: deploy-debug-prod (muhit o'zgaruvchilari ochiq)
app.get('/debug/env', (req, res) => res.json(process.env))

// VG: bot-webhook-secret (maxfiy token tekshirilmaydi)
app.post('/webhook', async (req, res) => {
  await handleUpdate(req.body)
  res.sendStatus(200)
})

async function handleUpdate(update) {}

app.listen(3000)
