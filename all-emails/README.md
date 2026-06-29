# All Verified Emails — Consolidated (third-party + all Cloudflare removed)

**Generated:** 2026-06-29 10:37:14 UTC

## Counts

- **Unique verified emails:** 5064
- **Unique domains represented:** 1781

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
| `tier1-2-dns:dmarc_rua` | 1047 |
| `tier1-2-dns:dmarc_ruf` | 456 |
| `tier1-2-dns:soa_rname` | 130 |
| `tier1-2-smtp` | 1362 |

## Files

- `unique_emails.txt` — unique emails, one per line, sorted
- `all_emails.csv` — long form: (email, domain, phase, source_url)
- `all_emails_dedup.csv` — one row per email, phases joined
- `removed_third_party.csv` — full removal log

## Filtered out

1. DMARC SaaS processors: postmarkapp, agari, dmarcian, valimail, redsift, easydmarc, uriports, fraudmarc, powerdmarc, returnpath, report-uri, dmarc.com, dmarcanalyzer, mailhardener, etc.
2. DNS / registrar / CDN ops mailboxes: godaddy, namecheap, gandi, ovh, ionos, awsdns-hostmaster, fastly, akamai, wixdns, squarespacedns, shopify, automattic, hetzner, digitalocean, linode, etc.
3. Privacy proxies: whoisguard, domainsbyproxy, contactprivacy, etc.
4. **All Cloudflare hosts** — any email host containing `cloudflare` (cloudflare.com, cloudflare.net, dmarc-reports.cloudflare.net, etc.) unconditionally removed.
