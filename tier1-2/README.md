# Tier 1 + Tier 2 contact discovery

For the 1,753 domains that do **not** publish a `security.txt`, this scan extracts official contacts from two layers of public, machine-verifiable signals.

## Tier 1 — DNS (publisher: domain owner)

| Signal | RFC | Field meaning |
|---|---|---|
| **SOA `RNAME`** | [RFC 1035](https://www.rfc-editor.org/rfc/rfc1035) | Zone admin email, e.g. `hostmaster.example.com` → `hostmaster@example.com` |
| **CAA `iodef`** | [RFC 8659](https://www.rfc-editor.org/rfc/rfc8659) | Security incident reporting endpoint (mailto or URL) |
| **DMARC `rua` / `ruf`** | [RFC 7489](https://www.rfc-editor.org/rfc/rfc7489) | Aggregate / forensic email-security report addresses |

Public resolvers used: `1.1.1.1`, `8.8.8.8`, `9.9.9.9`. Timeout 5s.

## Tier 2 — SMTP RCPT-TO live verification

For each domain we resolve MX records and probe the highest-priority MX:

1. `EHLO <domain>` (fallback to `HELO`)
2. `MAIL FROM:<probe-<random>@example.com>`
3. `RCPT TO:<<random-local-part>@<domain>>` — catch-all detection probe
4. `RSET`, then `RCPT TO:<security@<domain>>`
5. `RSET`, then `RCPT TO:<abuse@<domain>>`
6. `QUIT`

**No `DATA` command is ever sent.** No mail is delivered. The probe is strictly an envelope-level recipient validation.

If the random local-part is accepted (`250`), the MX is a catch-all and the `security@` / `abuse@` accept status is **demoted** — the JSON keeps the raw code but the CSV marks `catch_all = True` so downstream consumers can filter.

## Files

| File | Rows | Description |
|---|---:|---|
| `tier12_contacts.csv` | 1,753 | Flat per-domain CSV with one column per source |
| `tier12_results.json` | 1,753 | Per-domain raw output (Tier 1 + Tier 2) |

### `tier12_contacts.csv` columns

| Column | Source |
|---|---|
| `domain` | input domain |
| `soa_rname` | RFC 1035 SOA RNAME → email |
| `caa_iodef` | RFC 8659 CAA `iodef` entries (`; `-separated) |
| `dmarc_rua` | RFC 7489 DMARC `rua` addresses (`; `-separated) |
| `dmarc_ruf` | RFC 7489 DMARC `ruf` addresses (`; `-separated) |
| `security_at_status` | `accepted` / `rejected` / `temp-fail` / `accepted(catch-all)` / `no-mx` / `mx-unreachable` |
| `abuse_at_status` | same vocabulary |
| `catch_all` | `True` / `False` / `None` |
| `mx_count` | MX record count |

## Summary

| Signal | Domains hit |
|---|---:|
| SOA RNAME | **1,752** |
| CAA iodef | 67 |
| DMARC rua/ruf | **1,312** |
| `security@` SMTP-verified live (non-catch-all) | 450 |
| `abuse@`   SMTP-verified live (non-catch-all) | 912 |
| Catch-all MX (SMTP demoted) | 522 |

Wall-clock: ~112s @ 25 concurrent workers.
