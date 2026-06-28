# Consensus Email Discovery

Multi-source consensus pipeline to find verified contact/security emails for 1915 MCP+OAuth domains.

## Method

For each domain, queried **4 independent public sources in parallel**:
1. **Direct page fetch** — `/security`, `/.well-known/security.txt`, `/contact`, `/legal`, `/responsible-disclosure`, `/trust`, `/bug-bounty`, `/abuse`, `/policies`, `/help/security`, `/privacy`, `/terms`, root
2. **DuckDuckGo HTML scrape** — top results for `"<domain> security vulnerability report email"`
3. **Bing HTML scrape** — same query
4. **Google HTML scrape** — same query

**Strict filter:** all extracted emails MUST end in `@<domain>` or `@<registrable_parent>` — no third-party emails, no `gmail.com`, no `wordpress.com`, no `wixpress`, no `noreply`/`donotreply`, no image-asset false matches.

## Results

| Tier | Count | Definition |
|---|---|---|
| 🥇 **A** | **177** | Security-flavored local part (`security@`, `vuln@`, `psirt@`, `cert@`, `infosec@`, `abuse@`, `disclosure@`, `bugbounty@`) found on the official domain |
| 🥈 **B** | **879** | Generic verified email (`info@`, `contact@`, `support@`, `legal@`, etc.) found on official contact page |
| ❌ none | 859 | No verifiable email found via any source |
| **Total** | **1915** | |

**Hit rate: 55.1%**

## Files

| File | Description |
|---|---|
| `consensus_master.csv` | Master table — one row per domain, top email with tier, score, sources, URLs, snippet |
| `consensus_master.json` | Full audit trail — every candidate email per domain with all sources, URLs, snippets |
| `consensus_tier_a_security.csv` | Tier-A only — 177 highest-confidence security contacts |
| `consensus_all_verified.csv` | Flat list of all Tier A+B emails (one row per email, multi-row per domain) |
| `consensus_no_email.txt` | 859 domains where no email was found (manual-review queue) |

## Scoring

```
score = source_count                # 1-4
      + 2 if local-part is security-flavored
      + 2 if any URL is on the official domain
```

Email with highest score is selected as `top_email`. Ties broken by tier > source_count > alphabetical.

## Pipeline parameters

- Workers: 60 (per-domain), 4 (per-source within each domain)
- Per-fetch timeout: 3-5 seconds
- Phase 1 throughput: ~0.1 domains/sec (legacy, 20 workers sequential sources)
- Phase 2 throughput: ~5 domains/sec (60 workers, parallel sources per domain)

## Notes & honest limitations

- **Search engines (DDG/Bing/Google) blocked most of my scrape requests.** Real value came from the direct-fetch source. Tier C ("only found via search engine") = 0 because of this. A future run with Playwright + real-browser sessions would unlock that layer.
- **Tier B is "verified company email," not "verified security contact."** If a domain has only `info@` or `support@`, that's the best available — but it may not be the right contact for security disclosures.
- **859 domains have zero discoverable email.** Many are minimal landing pages, JS-rendered apps with no contact info in HTML, or sites that block direct HTTP fetches.
