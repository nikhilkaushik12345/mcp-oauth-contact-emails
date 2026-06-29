# Tier C Email Harvest — Summary

**Source list:** `consensus/consensus_no_email.txt` (859 domains with no email found in prior consensus phases).

**Scan completed:** 2026-06-29 09:15:31 UTC
**Method:** Pure HTTP (Python `requests` + `ThreadPoolExecutor`, 30 workers, `(connect=5s, read=8s)` per-request timeout, ~16s soft cap per worker). No Playwright, no browser automation. Executed in three 30-worker batches (300+300+259) to fit the sandbox's per-execution budget; per-batch wall-clock ≈ 33–53s; total scan wall-clock ≈ 125s.

## Counts

- **Total domains scanned:** 859
- **Domains with at least one verified email:** 99
- **Unique emails (verified, same-domain):** 195
- **By tier:**
  - C-sec (security/abuse/psirt/...): **10**
  - C-gen (info/contact/support/...): **109**
  - C-other: **76**

## Methodology

For each domain:
1. GET `https://{domain}{path}` for paths `/contact`, `/contact-us`, `/security`, `/about`. Falls back to `http://` on SSL errors. HTTP 4xx/5xx responses for a path are skipped.
2. Response body capped at 512KB. Emails extracted via regex `[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}`.
3. Kept only emails whose host equals the domain's TLD-aware registered root or a subdomain of it (multi-part TLDs like `.co.uk`, `.com.au`, `.co.jp`, etc. handled via a registered-suffix table).
4. Rejected: `noreply`, `no-reply`, `donotreply`, `do-not-reply`, `mailer-daemon`, `postmaster`; locals ending in image/file extensions (png, jpg, jpeg, gif, svg, webp, ico, css, js, json, xml, pdf, zip, mp4, webm); locals containing `wordpress` or `example`; hosts whose suffix is an image/file extension.
5. Classification (token-based, with substring fallback):
   - **C-sec:** security, abuse, psirt, soc, cert, disclosure, vuln, vulnerability, incident, infosec, responsibledisclosure, security-team, bugbounty, bounty
   - **C-gen:** info, contact, support, hello, help, admin, sales, press, media, legal, privacy, dpo, compliance, team, office
   - **C-other:** anything else

## Sample emails

### C-sec
- abuse@brevo.com  (brevo.com)
- security@convex.dev  (convex.dev)
- security@mux.com  (mux.com)
- security@octolane.com  (octolane.com)
- securityeng@optimizely.com  (optimizely.com)
- u003esecurityeng@optimizely.com  (optimizely.com)
- security@rudderstack.com  (rudderstack.com)
- security@vantage.sh  (vantage.sh)
- social@warmlyyours.com  (warmlyyours.com)
- security@waterplan.com  (waterplan.com)

### C-gen
- sales@abacum.ai  (abacum.ai)
- support@abacum.ai  (abacum.ai)
- support@accessowl.com  (accessowl.com)
- info@aneon.at  (aneon.at)
- help@are.na  (are.na)
- contact@aurelian.com  (aurelian.com)
- support@beachbossinfluencers.com  (beachbossinfluencers.com)
- sales@bellwetherit.com  (bellwetherit.com)
- support@bluegamma.io  (bluegamma.io)
- info@callpercy.com  (callpercy.com)

### C-other
- pierre-lous@alpic.ai  (alpic.ai)
- fred@alpic.ai  (alpic.ai)
- nikolay@alpic.ai  (alpic.ai)
- erica@alpic.ai  (alpic.ai)
- charles@alpic.ai  (alpic.ai)
- rike@antler.co  (antler.co)
- everyone@are.na  (are.na)
- tech@beachbossinfluencers.com  (beachbossinfluencers.com)
- johndoe@bluegamma.io  (bluegamma.io)
- zendesk-box@brevo.com  (brevo.com)
