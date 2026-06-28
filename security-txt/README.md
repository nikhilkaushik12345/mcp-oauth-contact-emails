# security.txt scan

RFC 9116 [`security.txt`](https://www.rfc-editor.org/rfc/rfc9116) scan over 1,915 confirmed MCP + OAuth domains.

## Method

For each domain, fetched these URLs in order until one returned a valid `security.txt`:

1. `https://<domain>/.well-known/security.txt`
2. `https://<domain>/security.txt`
3. `https://www.<domain>/.well-known/security.txt`
4. `https://www.<domain>/security.txt`

A response was accepted only when:

- HTTP 200
- `Content-Type` not HTML
- Body did not start with `<!doctype` / `<html>` (rules out soft-404 HTML)
- Body contained at least one `Contact:` line (RFC 9116 mandatory field)

Emails were extracted only from `Contact:` lines, taking the `mailto:` value or a bare email on that line. No guessing, no scraping, no enrichment.

## Files

| File | Rows | Description |
|---|---:|---|
| `security_emails_found.csv` | 144 | Domains with valid `security.txt` + at least one email contact |
| `security_txt_no_email.csv` | 18 | Domains with valid `security.txt` but no `mailto:` contact |
| `unique_emails.txt` | 148 | Deduplicated unique contact emails |
| `no_security_txt.txt` | 1,753 | Domains where no valid `security.txt` was found |
| `results.json` | 1,915 | Full per-domain raw output, including per-URL error codes |

## Summary

- Total scanned: 1,915
- With valid security.txt + email: **144 (7.5%)**
- With valid security.txt, no email: 18 (0.9%)
- Without security.txt: 1,753 (91.5%)
- Wall-clock: ~50s @ 80 concurrent workers

The 1,753 without `security.txt` are handled by the [`tier1-2/`](../tier1-2/) DNS + SMTP scan.
