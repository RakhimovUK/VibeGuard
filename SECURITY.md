# Security policy

## Reporting a vulnerability in VibeGuard

If you find a security problem in VibeGuard itself (for example, the guard hook can be bypassed in a way that leaks a secret, a script prints an unmasked secret, or a command could damage a user's project), please report it privately:

- Open the repository's **Security** tab and choose **Report a vulnerability** (GitHub private vulnerability reporting).
- Do not open a public issue for it, and do not include real secrets in the report.

Please include the VibeGuard version (`.claude-plugin/plugin.json`), your OS, the steps to reproduce, and what you expected to happen.

## What VibeGuard is and is not

- VibeGuard reads code and reports weaknesses. It does not attack running systems. Live checks are limited to localhost or a test environment the user names.
- It does not ship exploits. Rules and agents explain how a weakness could be abused and how to fix it.
- A clean report is not a guarantee of security. The risk score measures only what was found.
- Use it only on projects you own or have written permission to test.

## Deliberately vulnerable fixtures

`fixtures/` contains intentionally broken sample code and **fake** secrets (they contain the word `FAKE`). They exist to measure detection accuracy. Do not deploy them. Secret scanners may flag them; that is expected.

## Where your data stays

VibeGuard writes its state to `.vibeguard/` inside your project (config, findings, reports, incident notes) and adds that folder to `.gitignore`. Secret values are masked in reports and are not stored in the findings file. The scripts make no network requests.
