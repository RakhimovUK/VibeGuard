# VibeGuard

[O'zbekcha (lotin)](README.md) · [Ўзбекча (кирилл)](README.uz-cyrl.md) · [Русский](README.ru.md) · English

A Claude Code plugin that audits vibe-coded projects (Telegram bots, Mini Apps, websites, APKs) for security holes and bugs. In **Red Team** mode it reads your code through the eyes of 13 different attackers, finds the weak spots, explains how to fix them, and fixes them with your approval.

> Use only on projects you own or have written permission to test. No warranty. MIT license.

## Install (Claude Code)

```
/plugin marketplace add <github-user>/vibeguard
/plugin install vibeguard@vibeguard
```

## Commands

| Command | What it does |
|---|---|
| `/vibeguard:redteam [part]` | Full attack: scripts, attackers, skeptic, chains, report |
| `/vibeguard:quick` | Fast: secrets and critical issues |
| `/vibeguard:ship` | Before release: recent changes only, "ready / not ready" |
| `/vibeguard:fix VG-001` | Fix with approval: test, separate branch, re-attack |
| `/vibeguard:guard on` | Guard: blocks secrets from being written into code |
| `/vibeguard:rules` | Project rules in `CLAUDE.md` from the issues found |
| `/vibeguard:incident` | Step-by-step playbook for a leak or breach |
| `/vibeguard:lang en` | Language: `uz`, `uz-cyrl`, `ru`, `en` |

The first run asks for a permission confirmation and a language.

## What the report contains

- Risk score (0-100) and a verdict: ready to ship / not ready.
- **Three things to do today:** the most important fixes.
- **Time budget:** what an attacker reaches in 10 minutes, 1 day, 1 week.
- **Attack chains:** how small issues combine, and which single fix breaks the chain.
- Each finding (`VG-001`): location, evidence, attacker level, attack path, fix, what happens if it stays, and a ready prompt for Claude Code.
- A "you do this" list (for example, rotating a leaked token).
- Red vs blue score and re-attack results. An HTML view is generated too.

## Attackers

outsider (anonymous), user (malicious account holder), token (holds a leaked secret), fraudster (payment and logic abuse), cost (runs up your bill), supply (dependencies and CI), deploy (infrastructure), takeover (account theft), insider (former admin), scraper (bulk data collection), phisher (impersonation), apk (reverse engineering), ai (prompt injection).

A skeptic agent re-checks every finding. Findings without evidence are dropped.

## Safety limits

- Read-only by default. Live checks only against localhost or a test environment you name.
- No working exploits are written.
- Code changes only after approval, on a separate branch. Push, merge and deploy stay with you.
- A clean report is not a guarantee of security.

## Other tools and CI

- Cursor, Codex and similar: `adapters/AGENTS.md`.
- Check every PR on GitHub: `adapters/github-action/vibeguard.yml` (scripts only, no AI).
- Guard mode needs `python3`.

## Status

v0.6. Scripts and the guard hook are tested on the fixtures (`python3 skills/vibeguard/scripts/selftest.py`). Attacker-agent accuracy has not been measured yet: please share your results in an issue. Contributing: `CONTRIBUTING.md`. Reporting a vulnerability: `SECURITY.md`.
