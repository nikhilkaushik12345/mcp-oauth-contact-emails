#!/usr/bin/env python3
"""Faster consensus runner — higher concurrency + tight timeouts. Same source set."""
import os, sys, re, json, time, csv, ssl
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError as FTimeout
from urllib.parse import quote_plus, urlparse, unquote, parse_qs
import urllib.request

TIMEOUT = 4
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
EMAIL_RE = re.compile(r'(?<![A-Za-z0-9._%+-])([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})')
SEC_LOCALS = ('security','vuln','psirt','cert','infosec','abuse','disclosure','bugbounty','bounty','report','soc')
JUNK = ('example.com','yourdomain','domain.com','test@','@test.','noreply','no-reply','donotreply','do-not-reply','wixpress','sentry.io','wordpress.com','wix.com','squarespace','godaddy','@2x.png','@3x.png')
TWO_LEVEL = {'co.uk','co.jp','com.au','co.in','com.br','co.kr','com.mx','co.za','com.sg','co.nz','com.tr','com.tw','com.hk','co.il','ac.uk','gov.uk','org.uk','net.au','org.au'}

def parent(d):
    p = d.lower().split('.')
    if len(p) <= 2: return d.lower()
    last2 = '.'.join(p[-2:])
    if last2 in TWO_LEVEL: return '.'.join(p[-3:])
    return last2

def http_get(url, timeout=TIMEOUT):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept":"text/html,*/*;q=0.8"})
        ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return r.geturl(), r.read(1_500_000).decode(r.headers.get_content_charset() or 'utf-8', errors='replace')
    except Exception: return None, None

def extract(text, domain):
    if not text: return []
    par = parent(domain); dlow = domain.lower(); out = []
    for m in EMAIL_RE.finditer(text):
        em = m.group(1).lower().strip().strip('.')
        if '@' not in em: continue
        host = em.split('@')[1]
        if not (host == dlow or host == par or host.endswith('.'+par)): continue
        if any(j in em for j in JUNK): continue
        if em.endswith(('.png','.jpg','.svg','.gif','.webp')): continue
        s,e = max(0,m.start()-100), min(len(text), m.end()+100)
        snip = re.sub(r'\s+',' ',text[s:e]).strip()[:200]
        out.append((em, snip))
    return out

PATHS = ["/.well-known/security.txt","/security.txt","/security","/security/","/security.html",
         "/contact","/contact-us","/legal","/responsible-disclosure","/vulnerability-disclosure",
         "/bug-bounty","/about/security","/trust","/trust-center","/abuse","/policies","/help/security",
         "/privacy","/terms","/"]

def src_direct(domain):
    results = []
    for p in PATHS:
        url = f"https://{domain}{p}"
        final, body = http_get(url, timeout=3)
        if not body: continue
        for em, snip in extract(body, domain):
            results.append({"email":em,"url":final or url,"snippet":snip,"via":"direct","on_official":True})
    return results

def _scrape(url, domain, via):
    final, body = http_get(url, timeout=5)
    if not body: return []
    if via == "ddg":
        link_re = re.compile(r'<a[^>]+class="result__a"[^>]+href="([^"]+)"', re.I)
        urls = []
        for href in link_re.findall(body)[:4]:
            if 'uddg=' in href:
                try:
                    qs = parse_qs(urlparse(href).query)
                    real = qs.get('uddg',[None])[0]
                    if real: urls.append(unquote(real))
                except: pass
            elif href.startswith('http'): urls.append(href)
    elif via == "bing":
        urls = re.findall(r'<li class="b_algo"[^>]*>\s*<h2><a[^>]+href="([^"]+)"', body, re.I)[:4]
    elif via == "google":
        urls = []
        for u in re.findall(r'<a href="/url\?q=(https?://[^&]+)&', body, re.I):
            if any(s in u for s in ('google.com','webcache','youtube.com','facebook.com','linkedin.com')): continue
            urls.append(u)
            if len(urls)>=4: break
    else: urls = []
    par = parent(domain); results = []
    for u in urls:
        host = urlparse(u).hostname or ''
        on_off = host.endswith(par)
        _, ptext = http_get(u, timeout=4)
        if not ptext: continue
        for em, snip in extract(ptext, domain):
            results.append({"email":em,"url":u,"snippet":snip,"via":via,"on_official":on_off})
    return results

def src_ddg(d):    return _scrape(f"https://html.duckduckgo.com/html/?q={quote_plus(f'{d} security vulnerability report email')}", d, "ddg")
def src_bing(d):   return _scrape(f"https://www.bing.com/search?q={quote_plus(f'{d} security vulnerability report email')}", d, "bing")
def src_google(d): return _scrape(f"https://www.google.com/search?q={quote_plus(f'{d} security vulnerability report email')}&hl=en", d, "google")

def process(domain):
    domain = domain.strip().lower()
    if not domain: return None
    findings = []
    # Run 4 sources in PARALLEL per-domain (was sequential before)
    with ThreadPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(fn, domain): n for fn,n in [(src_direct,'direct'),(src_ddg,'ddg'),(src_bing,'bing'),(src_google,'google')]}
        for fu in as_completed(futs, timeout=30):
            try: findings.extend(fu.result() or [])
            except Exception: pass
    by = {}
    for f in findings:
        em = f["email"]
        if em not in by:
            by[em] = {"email":em,"sources":set(),"urls":set(),"snippets":[],"on_official":False}
        by[em]["sources"].add(f["via"]); by[em]["urls"].add(f["url"])
        by[em]["on_official"] = by[em]["on_official"] or f["on_official"]
        if len(by[em]["snippets"]) < 3: by[em]["snippets"].append(f["snippet"])
    ranked = []
    for em, d in by.items():
        local = em.split('@')[0]
        score = len(d["sources"])
        if any(k in local for k in SEC_LOCALS): score += 2
        if d["on_official"]: score += 2
        is_sec = any(k in local for k in SEC_LOCALS)
        tier = "A" if (is_sec and d["on_official"]) else ("B" if d["on_official"] else "C")
        ranked.append({"email":em,"tier":tier,"score":score,"source_count":len(d["sources"]),
                       "sources":sorted(d["sources"]),"urls":sorted(d["urls"])[:5],
                       "snippets":d["snippets"],"on_official":d["on_official"]})
    ranked.sort(key=lambda x:(-x["score"], x["tier"], -x["source_count"], x["email"]))
    return {"domain":domain,"candidates":ranked,"n_findings":len(findings)}

def main():
    in_file = sys.argv[1]; out_json = sys.argv[2]; out_csv = sys.argv[3]
    workers = int(sys.argv[4]) if len(sys.argv)>4 else 60
    with open(in_file) as f: doms = [l.strip() for l in f if l.strip()]
    results = []
    print(f"Scanning {len(doms)} domains with {workers} workers (4-src parallel per domain)...")
    t0 = time.time(); save_every = 50
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(process, d): d for d in doms}
        for i, fu in enumerate(as_completed(futs)):
            try:
                r = fu.result(timeout=45)
                if r: results.append(r)
            except Exception as e:
                d = futs[fu]
                results.append({"domain":d,"candidates":[],"n_findings":0,"error":str(e)[:80]})
            if (i+1) % 25 == 0 or (i+1)==len(doms):
                el = time.time()-t0
                rate = (i+1)/el if el>0 else 0
                eta = (len(doms)-(i+1))/rate if rate>0 else 0
                hits = sum(1 for r in results if r.get('candidates'))
                print(f"  [{i+1}/{len(doms)}] {el:.0f}s, {rate:.2f}/s, ETA {eta:.0f}s, hits {hits}/{len(results)}", flush=True)
            if (i+1) % save_every == 0:
                with open(out_json + '.partial','w') as f: json.dump(results, f)
    with open(out_json, 'w') as f: json.dump(results, f, indent=2)
    if os.path.exists(out_json + '.partial'): os.remove(out_json + '.partial')
    with open(out_csv, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(["domain","top_email","tier","score","source_count","sources","source_urls","top_snippet","all_candidates"])
        for r in results:
            if r.get("candidates"):
                t = r["candidates"][0]
                allc = "; ".join(f"{c['email']}({c['tier']},{c['score']},{','.join(c['sources'])})" for c in r["candidates"][:6])
                w.writerow([r["domain"],t["email"],t["tier"],t["score"],t["source_count"],
                            ",".join(t["sources"])," | ".join(t["urls"][:3]),
                            (t["snippets"][0] if t["snippets"] else ""), allc])
            else:
                w.writerow([r["domain"],"","",0,0,"","","",""])
    print(f"DONE. {sum(1 for r in results if r.get('candidates'))}/{len(results)} hits. Time: {time.time()-t0:.0f}s")

if __name__ == "__main__":
    main()
