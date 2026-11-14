---
id: deploy-docker-secrets
soha: deploy
xavf: yuqori
lesson: "No secrets in Dockerfile or image layers; add .dockerignore (.env, .git); run as a non-root USER; pin the base image."
agent: attacker-deploy
---

# Docker tasvirida sirlar va root

## Nima qidiriladi
- `Dockerfile` ichida `ENV TOKEN=...`, `ARG PASSWORD=...` yoki `COPY .env`.
- `.dockerignore` yo'q yoki unda `.env`, `.git` ko'rsatilmagan (`COPY . .` hammasini oladi).
- `USER` ko'rsatmasi yo'q (konteyner root bilan ishlaydi).
- `FROM image:latest` yoki tegsiz asos tasvir.

## Nega xavfli
Tasvir qatlamlarida qolgan sir tasvirni olgan har kimga ko'rinadi. Root bilan ishlaydigan konteynerda ilovadagi bitta xato butun konteynerni egallashga olib keladi.

## Yomon misol
```dockerfile
FROM node:latest
ENV BOT_TOKEN=123...xyz
COPY . .
CMD ["node", "server.js"]
```

## Yaxshi misol
```dockerfile
FROM node:22-slim
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY src ./src
USER node
CMD ["node", "src/server.js"]
```

## Tuzatish
Sirlarni faqat ishga tushirish paytida hosting muhit o'zgaruvchilari orqali ber. `.dockerignore` ga `.env`, `.git`, `node_modules` qo'sh. `USER` bilan oddiy foydalanuvchiga o't. Tasvirga tushgan sirni almashtir.

Claude Code uchun prompt: "Dockerfile'dan sirlarni olib tashla, .dockerignore yarat (.env, .git), root bo'lmagan USER qo'sh va asos tasvirni aniq versiyaga qotir."
