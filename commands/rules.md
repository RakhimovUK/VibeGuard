---
description: Auditda topilgan xatolar asosida loyiha qoidalarini CLAUDE.md ga yozadi, Claude Code o'sha xatoni takrorlamasligi uchun.
argument-hint: "[fayl, sukut: CLAUDE.md]"
---

`vibeguard` skillini yukla va loyiha qoidalarini yangila. Fayl: $ARGUMENTS (bo'sh bo'lsa `CLAUDE.md`).

1. `.vibeguard/findings.json` yo'q bo'lsa: "avval `/vibeguard:redteam` ni ishga tushiring" deb to'xta.
2. Avval ko'rsat, yozma: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/vibeguard/scripts/rules_block.py" --dry-run`. Natijadagi `block` ni foydalanuvchiga ko'rsat va har bir qoida nimani anglatishini uning tilida bir jumla bilan tushuntir (qoidalar ingliz tilida yoziladi, chunki ularni Claude Code o'qiydi).
3. **Tasdiq so'ra.** "Ha" bo'lsa, `--dry-run` siz ishga tushir.
4. Skript faqat `<!-- vibeguard:start -->` va `<!-- vibeguard:end -->` orasidagi blokni yozadi yoki yangilaydi. Fayldagi boshqa matnga tegilmaydi. Blok ichini qo'lda tahrirlama.
5. `unknown_rules` bo'sh bo'lmasa: bu topilmalar uchun tayyor qoida yo'q. Foydalanuvchi xohlasa, ularni blokdan **tashqariga** alohida qo'lda yozishni taklif qil.

Boshqa vositalar (Cursor, Codex): xuddi shu blokni `AGENTS.md` ga yozish uchun `--file AGENTS.md` bilan chaqir.
