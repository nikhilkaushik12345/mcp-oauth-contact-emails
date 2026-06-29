# All Verified Emails — Strict Same-Domain Only

Every email here is on the **same registered root domain** as the record it was associated with. All third-party processors, DMARC SaaS, DNS providers, Mailgun, Cloudflare, registrars, hosting providers, and anything with `dmarc` or `mailgun` in the address have been removed.

**Generated:** 2026-06-29 10:40:55 UTC

## Counts

- **Unique verified emails:** 4088
- **Unique domains represented:** 1614

## Filter rule

Keep `email@host.tld` for record-domain `D` only if:
1. The registered root of `host.tld` equals the registered root of `D` (TLD-aware — `.co.uk`, `.com.au`, etc. handled).
2. The email does NOT contain `dmarc` or `mailgun` anywhere in the address.

This deletes every third-party-routed contact (DMARC reporters, Mailgun, SendGrid, Postmark, Agari, dmarcian, Cloudflare reporting, AWS/GoDaddy/Namecheap/etc.) and keeps only addresses on the company's own domain.

## Per-phase contribution

| Phase | Emails |
|---|---|
| `C-gen` | 109 |
| `C-other` | 76 |
| `C-sec` | 10 |
| `consensus-tier-A` | 188 |
| `consensus-tier-B` | 1968 |
| `security.txt` | 128 |
| `tier1-2-dns:caa_iodef` | 61 |
| `tier1-2-dns:dmarc_rua` | 343 |
| `tier1-2-dns:dmarc_ruf` | 145 |
| `tier1-2-dns:soa_rname` | 48 |
| `tier1-2-smtp` | 1362 |

## Files

- `unique_emails.txt` — one per line, sorted
- `all_emails.csv` — long form (email, domain, phase, source_url)
- `all_emails_dedup.csv` — wide form, phases joined per email
- `removed_third_party.csv` — full log of every removed row with reason
