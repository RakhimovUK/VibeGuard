# VibeGuard for other coding agents (Cursor, Codex, and similar)

Copy this file into your project as `AGENTS.md` (or append it to an existing one), and clone the VibeGuard repository next to it or into `.vibeguard-tool/`. Paths below assume `.vibeguard-tool/`.

Subagents, slash commands and the guard hook exist only in Claude Code. Here the same audit runs as one sequential procedure. The rules, scripts and report format are shared.

## Hard limits

1. Ask once: "This project is mine or I have written permission to test it." Stop without a yes.
2. Read code only. Live requests are allowed only to localhost or a test environment the user names. Never touch production or third-party services.
3. Explain how a weakness could be abused; do not write working exploits, payload lists, brute-force or DoS scripts. To prove a bug, write a test that checks the safe behaviour.
4. Never change code without approval. Report first, then fix on a separate branch, one commit per finding.
5. Mask secrets in all output (`sk-...a4f2`). Keep `.vibeguard/` in `.gitignore`.
6. Every finding needs `file:line` and a code snippet. Mark anything unproven as unconfirmed.

## Audit procedure

1. Read `.vibeguard/config.json` for `lang` (`uz`, `uz-cyrl`, `ru`, `en`); ask and create it if missing.
2. Map the project: stack, parts (bot, web app, site, APK, payments, deploy), entry points, where secrets live.
3. Run the scripts and keep their output as evidence:
   - `python3 .vibeguard-tool/skills/vibeguard/scripts/scan_secrets.py .`
   - `python3 .vibeguard-tool/skills/vibeguard/scripts/check_hygiene.py .`
4. Read `.vibeguard-tool/skills/vibeguard/scenarios/README.md`; if a scenario matches the project type, check its plans first.
5. Take the attacker roles one at a time. For each, read its file in `.vibeguard-tool/agents/attacker-*.md` and the rule files in `.vibeguard-tool/skills/vibeguard/rules/` whose `agent:` field names that role. Skip roles that do not apply (no APK, no AI feature, and so on).
6. Review your own findings as a skeptic (`agents/redteam-skeptic.md`): reopen each file, look for a protection elsewhere, drop or downgrade what you cannot prove.
7. Save findings as JSON in the shape described in `skills/vibeguard/reference/scoring-and-memory.md`, then run `findings.py merge`, `score`, `top3`, `budget` and `board` from the same scripts folder. Do not compute the score yourself.
8. Link confirmed findings into attack chains (`agents/redteam-chain.md`).
9. Write the report from `skills/vibeguard/templates/report.<lang>.md` into `.vibeguard/reports/`.
10. Ask before fixing. Follow `agents/fixer.md`: failing test, minimal fix, passing test, one commit, no push or merge.

## Project rules

To write the lessons from the audit into this file so the same mistakes are not repeated:

`python3 .vibeguard-tool/skills/vibeguard/scripts/rules_block.py --file AGENTS.md --dry-run`

Show the block to the user, and run it again without `--dry-run` after they agree. Only the text between the `vibeguard:start` and `vibeguard:end` markers is rewritten.
