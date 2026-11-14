# VibeGuard Red Team report

Project: {{loyiha}} | Date: {{sana}} | Language: English

## Verdict

**Risk score: {{ball}}/100** → {{hukm}}  (ready to ship / not ready)

Summary: 2-3 sentences in plain language.

## Three things to do today

Output of `findings.py top3`. One sentence each: what to do and why it comes first.

1. VG-00A: ...
2. VG-00B: ...
3. VG-00C: ...

## Time budget

Output of `findings.py budget`: what an attacker reaches in that time.

| Time | Who | What they reach |
|---|---|---|
| 10 minutes | amateur (havaskor) | ... |
| 1 day | skilled (tajribali) | ... |
| 1 week | targeted (maqsadli) | ... |

## Red vs blue

Output of `findings.py board`. Red (open findings): N | Blue (fixed + blocked by the guard): N

## Attack chains

Show how small issues combine into serious damage.

### Chain 1: {{nomi}}
1. The attacker ... (finding VG-00A)
2. Then ... (finding VG-00B)
3. Result: ...
- **Link that breaks the chain:** VG-00A

## Findings

### VG-001 · {{sarlavha}} · {{critical|high|medium|low}}

- **Status:** confirmed / unconfirmed
- **Attacker level:** amateur / skilled / targeted
- **Where:** `file:line`
- **Evidence:**
  ```
  code snippet (secrets masked)
  ```
- **Who attacks and what they want:**
- **Attack path (steps):**
- **What happens if it is not fixed:**
- **How to fix:**
- **Prompt for Claude Code:**
  > ...

## You do this

Things I cannot do (for example, rotating a leaked token):
- [ ] ...

## Accuracy

Found: N | Confirmed by skeptic: N | Unconfirmed: N | Dropped: N

## Re-attack (after fixes)

| ID | Result |
|---|---|
| VG-001 | fixed / remaining / new / reopened |
