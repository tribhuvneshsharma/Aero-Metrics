# Source Governance & Legal Compliance

## 1. Governance Principles
Aero-Metrics operates as a governed, ethical public-interest platform:
- **No Access Circumvention**: Does not bypass CAPTCHA, evade IP blocks, rotate residential proxies, or violate platform terms.
- **Permitted Access Only**: Uses approved public data feeds, developer APIs, or partner agreements.
- **Strict Rate Limiting**: Enforces strict request budgets, jittered intervals, and concurrency limits per domain.
- **Fail-Safe Operation**: If an adapter encounters access denial (`403 Forbidden` / `429 Too Many Requests`), it halts requests immediately, logs the incident, and gracefully switches to replay/fixture data.
- **Zero PII**: No personal user details, credentials, or accounts are requested or stored.
