# All Verified Emails — Consolidated

Single rolled-up file of every verified email across all scan phases.

**Generated:** 2026-06-29 09:53:31 UTC

## Counts

- **Unique verified emails:** 5556
- **Unique domains represented:** 1909

## Per-phase contribution (emails that appeared in each phase; an email can appear in multiple)

| Phase | Count |
|---|---|
| `C-gen` | 109 |
| `C-other` | 76 |
| `C-sec` | 10 |
| `consensus-tier-A` | 188 |
| `consensus-tier-B` | 1973 |
| `security.txt` | 148 |
| `tier1-2-dns:caa_iodef` | 69 |
| `tier1-2-dns:dmarc_rua` | 1457 |
| `tier1-2-dns:dmarc_ruf` | 565 |
| `tier1-2-dns:soa_rname` | 146 |
| `tier1-2-smtp` | 1362 |

## Files

- [`unique_emails.txt`](./unique_emails.txt) — 5556 unique emails, one per line, sorted.
- [`all_emails.csv`](./all_emails.csv) — long form: one row per (email, source). Lets you see every phase that confirmed a given email.
- [`all_emails_dedup.csv`](./all_emails_dedup.csv) — wide form: one row per unique email, with all phases joined into a `phases` column.

## Source phases included

- `security.txt` — emails from `/.well-known/security.txt` (initial 1,915-domain scan)
- `tier1-2-smtp` — SMTP-verified `security@` / `abuse@` (RCPT TO check accepted)
- `tier1-2-dns:{soa_rname|caa_iodef|dmarc_rua|dmarc_ruf}` — emails exposed in DNS records
- `consensus-tier-A` — security-focused consensus (direct fetch + search engines)
- `consensus-tier-B` — general consensus (direct fetch + search engines)
- `C-sec`, `C-gen`, `C-other` — Tier C HTTP scrape of the 859 remaining domains

## Notes

- Email host is validated against domain (TLD-aware registered root) at each ingest step, so all entries are same-domain or subdomain of the listed domain.
- Standard rejects applied at source: `noreply`, `no-reply`, `donotreply`, `mailer-daemon`, `postmaster`, image/file extensions, `wordpress`, `example`.
