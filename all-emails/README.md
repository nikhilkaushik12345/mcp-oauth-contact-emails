# All Verified Emails — Consolidated (third-party noise removed)

Single rolled-up file of every verified email across all scan phases, with third-party DMARC processors and DNS/hosting-provider ops mailboxes filtered out.

**Generated:** 2026-06-29 10:27:13 UTC

## Counts

- **Unique verified emails:** 5256
- **Unique domains represented:** 1806
- **Unique emails removed as third-party noise:** 300 (across 1847 source rows)

## Per-phase contribution (after filtering)

| Phase | Emails |
|---|---|
| `C-gen` | 109 |
| `C-other` | 76 |
| `C-sec` | 10 |
| `consensus-tier-A` | 188 |
| `consensus-tier-B` | 1973 |
| `security.txt` | 148 |
| `tier1-2-dns:caa_iodef` | 69 |
| `tier1-2-dns:dmarc_rua` | 1234 |
| `tier1-2-dns:dmarc_ruf` | 457 |
| `tier1-2-dns:soa_rname` | 130 |
| `tier1-2-smtp` | 1362 |

## Files

- [`unique_emails.txt`](./unique_emails.txt) — 5256 unique emails, one per line, sorted.
- [`all_emails.csv`](./all_emails.csv) — long form: one row per (email, phase, source_url).
- [`all_emails_dedup.csv`](./all_emails_dedup.csv) — one row per unique email, with all phases joined.
- [`removed_third_party.csv`](./removed_third_party.csv) — the rows we filtered out, for transparency.

## What was filtered out and why

DMARC `rua` / `ruf` reports often go to SaaS processors (Postmark, Agari, dmarcian, valimail, EasyDMARC, redsift, uriports, etc.), and SOA `rname` often points at the DNS/registrar/hosting provider (Cloudflare, GoDaddy, AWS, Squarespace, etc.). Those addresses are real and working but they are NOT the domain owner — they belong to the service provider. They were removed.

An email is kept if the email host's registered root equals the domain's registered root (e.g. an email at `cloudflare.com` is kept when the record's domain IS `cloudflare.com`).

Blocklist (third-party hosts) includes: DMARC SaaS (postmarkapp, agari, dmarcian, dmarc.com, dmarcanalyzer, valimail, redsift, easydmarc, uriports, fraudmarc, powerdmarc, returnpath, report-uri, etc.); DNS/registrar/CDN (cloudflare, godaddy, namecheap, name.com, gandi, ovh, ionos, hover, porkbun, dynadot, enom, namesilo, tucows, fastly, akamai, wixdns, squarespacedns, shopify, automattic, hetzner, digitalocean, linode, vultr, rackspace, ns1, dyn, easydns, registrar-servers, domaincontrol, amazonaws, awsdns-hostmaster, azure, microsoft, google domains); privacy proxies (whoisguard, domainsbyproxy, contactprivacy, etc.).
