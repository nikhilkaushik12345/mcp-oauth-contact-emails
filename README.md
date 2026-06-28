# mcp-oauth-contact-emails

Official security and abuse contact emails for the **1,915 confirmed MCP + OAuth domains** from the broader MCP/OAuth scan effort.

Every contact in this repo is sourced from a public, machine-verifiable record published by the domain owner. **No guessing. No scraping. No enrichment.**

## Coverage

| Source | Domains | Notes |
|---|---:|---|
| RFC 9116 `security.txt` with `Contact:` mailto | **144** | gold standard — explicit security contact published by the domain |
| `security.txt` present but no mailto contact | 18 | web form, PGP key, or policy URL only |
| **No `security.txt`** — fell through to DNS + SMTP | **1,753** | covered by Tier 1 (DNS) and Tier 2 (SMTP RCPT-TO) below |

For the 1,753 domains without `security.txt`:

| Mechanism | Domains | RFC |
|---|---:|---|
| DNS **SOA RNAME** (zone admin email) | 1,752 | RFC 1035 |
| DNS **CAA `iodef`** (incident reporting endpoint) | 67 | RFC 8659 |
| DNS **DMARC `rua` / `ruf`** (report addresses) | 1,312 | RFC 7489 |
| SMTP **`security@<domain>`** verified live (RCPT TO 250, non-catch-all MX) | 450 | RFC 5321 + RFC 2142 |
| SMTP **`abuse@<domain>`** verified live (RCPT TO 250, non-catch-all MX) | 912 | RFC 5321 + RFC 2142 |
| Catch-all MX detected (SMTP signal demoted) | 522 | — |

Every one of the 1,753 has at least one source returning a contact. Combined with the 144 from `security.txt`, you have actionable contacts for **all 1,915 domains**.

## Layout

```
security-txt/
  README.md                      method + summary
  security_emails_found.csv      144 domains w/ valid security.txt + email
  security_txt_no_email.csv      18 domains w/ valid security.txt, no email
  unique_emails.txt              148 deduplicated unique contact emails
  no_security_txt.txt            1753 domains with no security.txt (input to tier1-2)
  results.json                   per-domain raw scan output

tier1-2/
  README.md                      method + summary
  tier12_contacts.csv            flat per-domain CSV across all sources
  tier12_results.json            per-domain raw output

inputs/
  confirmed_oauth.txt            input list of 1915 domains
```

## How to use

- **Maximum-confidence outreach:** use `security-txt/security_emails_found.csv` (144 domains, explicit security contacts) plus `tier1-2/tier12_contacts.csv` rows where `security_at_status = accepted` or `abuse_at_status = accepted` AND `catch_all = False` (an additional ~1,362 verified live mailboxes).
- **Reporting / vulnerability disclosure:** prefer `caa_iodef` and `dmarc_ruf` columns where present — these are explicitly published incident endpoints.
- **Best-effort fallback:** `soa_rname` is published by virtually every domain but is often a hosting provider's admin contact rather than a security team.

## Method

### security.txt scan
For each domain, fetched in order: `https://<domain>/.well-known/security.txt`, `/security.txt`, then the same paths under `www.`. A response was accepted only if HTTP 200, non-HTML content, body did not start with `<html>`/`<!doctype`, and body contained at least one `Contact:` line. Emails were extracted only from `Contact: mailto:` values.

### Tier 1 (DNS)
- `SOA` lookup → parse `RNAME` (with `\.`-escape handling) into an email address
- `CAA` lookup → keep records with `tag = iodef`
- `_dmarc.<domain>` TXT lookup → parse `rua=` and `ruf=` mailto values
- Used public resolvers (1.1.1.1, 8.8.8.8, 9.9.9.9) with 5s timeout

### Tier 2 (SMTP RCPT-TO live verification)
For each domain:
1. Resolve MX records (fallback to implicit MX via A)
2. Connect to the highest-priority MX on port 25, EHLO/HELO with the target domain
3. `MAIL FROM:<probe-<random>@example.com>`
4. `RCPT TO:<<random-local-part>@<domain>>` — used to detect catch-all MX
5. `RCPT TO:<security@<domain>>` and `RCPT TO:<abuse@<domain>>`
6. `QUIT` — **no DATA command is ever sent, no mail is delivered**

If the random local-part is accepted (250), the MX is a catch-all and the `security@` / `abuse@` accept status is demoted to "unverifiable" (still reported in JSON but flagged in CSV).

## Scale

- 1,915 domains scanned for `security.txt` in ~50s at 80 concurrent workers
- 1,753 domains scanned for DNS + SMTP Tier 1+2 in ~112s at 25 concurrent workers

## Inputs

The 1,915-domain input list comes from `confirmed_oauth.txt` (also vendored in `inputs/`), which was produced by an earlier MCP + OAuth metadata scan across multiple source lists (results published separately in [`mcp-oauth-verification-results`](https://github.com/nikhilkaushik12345/mcp-oauth-verification-results) and related repos).

## License

MIT — see `LICENSE`.
