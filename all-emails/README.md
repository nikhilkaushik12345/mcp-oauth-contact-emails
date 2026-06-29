# All Verified Emails — Consolidated (third-party + Cloudflare removed)

Single rolled-up file of every verified email across all scan phases, with third-party DMARC processors, DNS/hosting-provider ops mailboxes, and all Cloudflare-hosted addresses filtered out.

**Generated:** 2026-06-29 10:34:18 UTC

## Counts

- **Unique verified emails:** 5251
- **Unique domains represented:** 1805

## Per-phase contribution

| Phase | Emails |
|---|---|
| `C-gen` | 109 |
| `C-other` | 76 |
| `C-sec` | 10 |
| `consensus-tier-A` | 188 |
| `consensus-tier-B` | 1968 |
| `security.txt` | 148 |
| `tier1-2-dns:caa_iodef` | 69 |
| `tier1-2-dns:dmarc_rua` | 1234 |
| `tier1-2-dns:dmarc_ruf` | 457 |
| `tier1-2-dns:soa_rname` | 130 |
| `tier1-2-smtp` | 1362 |

## Files

- `unique_emails.txt` — unique emails, one per line, sorted.
- `all_emails.csv` — long form: one row per (email, phase, source_url).
- `all_emails_dedup.csv` — one row per unique email with all phases joined.
- `removed_third_party.csv` — every row that was filtered out (third-party processors, DNS providers, and Cloudflare), for transparency.

## What was filtered out

1. **DMARC SaaS processors** — postmarkapp, agari, dmarcian, valimail, redsift, easydmarc, uriports, fraudmarc, powerdmarc, returnpath, report-uri, dmarc.com, dmarcanalyzer, mailhardener, and similar.
2. **DNS / registrar / CDN ops mailboxes** — godaddy, namecheap, name.com, gandi, ovh, ionos, awsdns-hostmaster, fastly, akamai, wixdns, squarespacedns, shopify, automattic, hetzner, digitalocean, linode, etc.
3. **Privacy proxies** — whoisguard, domainsbyproxy, contactprivacy, etc.
4. **Cloudflare** — every `@cloudflare.com` and `*.cloudflare.com` address removed unconditionally, including cases where the source domain was cloudflare itself.
