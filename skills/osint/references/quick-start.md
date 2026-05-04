# Quick Start — First Steps for Any Investigation

When a user describes an OSINT task, use this guide to pick the right starting point fast. Don't read 100 pages of methodology — start here, then load domain-specific references as needed.

---

## What Kind of Investigation?

| The user wants to... | Start with | First tool | Load reference |
|----------------------|-----------|------------|----------------|
| Find where a photo was taken | **Geolocation** | `gemini` (visual analysis) + `extract_exif.py` | geolocation.md |
| Investigate a person | **People/SOCMINT** | `check_username.py` + `tavily_search` | people-social-media.md |
| Map a domain's infrastructure | **Domain/Infra** | `query_dns.py` + `query_whois.py` | domain-infrastructure.md |
| Check if a site/file is malicious | **Threat Intel** | `query_virustotal.py` + `query_urlscan.py` | domain-infrastructure.md |
| Analyze an image for manipulation | **Image Forensics** | `image_ela.py` + `extract_exif.py` | image-video-forensics.md |
| Track an aircraft or vessel | **Transportation** | `query_flightradar.py` or `query_ais.py` | vehicle-object-id.md |
| Trace a crypto wallet | **Cryptocurrency** | `query_blockchain.py` | crypto-financial.md |
| Find deleted web content | **Archival** | `internet-archive` MCP + `query_archive_today.py` | (no dedicated ref — use tool-guide.md) |
| Verify a claim or fact-check | **Verification** | `tavily_search` + `searxng_search` | osint-cycle.md |
| Investigate a company | **Corporate** | `query_whois.py` + `common-crawl` MCP + `tavily_search` | (no dedicated ref — use platform-directory.md) |
| Resolve an entity (who is this?) | **Entity Resolution** | `query_wikidata_sparql.py` + `tavily_search` | people-social-media.md |

---

## First 5 Minutes of Any Investigation

### 1. Create a workspace (30 seconds)

```bash
mkdir -p investigations/<case-name>/{downloads}
cd investigations/<case-name>
```

Create these files immediately:
- `search-log.md` — Log every query, tool, result, and timestamp
- `leads.md` — Track promising findings (HIGH / MEDIUM / LOW priority)

### 2. Define the question (1 minute)

Write a single sentence: "I need to find out ___."

This prevents rabbit holes. Everything you do should move toward answering this question.

### 3. Run the first tool (1 minute)

Don't think too hard. Pick the first tool from the table above and run it. The first result tells you where to pivot.

### 4. Log and pivot (ongoing)

After each tool result:
1. Log the query and key findings in `search-log.md`
2. Ask: "What new question does this answer raise?"
3. Pick the next tool to answer that question
4. Update `leads.md` if you found something promising

---

## Common First Moves by Domain

### Person Investigation
```
1. check_username.py <username>           → which platforms?
2. tavily_search "<name>" site:linkedin   → professional profile
3. query_wikidata_sparql.py entity "<name>" → structured data (public figures)
4. searxng_search "<name>" "<email>"      → broader web presence
5. check_username.py on any new usernames found
```

### Domain Investigation
```
1. query_whois.py <domain>                → who registered it, when?
2. query_dns.py all <domain>              → what infrastructure?
3. query_crtsh.py <domain>                → what subdomains (via certs)?
4. query_shodan_internetdb.py <ip>        → what's running on the server?
5. query_ipinfo.py geo <ip>               → where is it hosted?
6. query_virustotal.py domain <domain>    → is it flagged as malicious?
```

### Geolocation from Image
```
1. extract_exif.py <image>                → GPS coordinates? Camera info?
2. gemini ask_question_about_video        → what's visible? Language? Signs?
3. selenium → Google Lens reverse search  → where else does this image appear?
4. sun_position.py (if shadows visible)   → verify time/location from sun angle
5. tavily_search with visible clues       → narrow the location
```

### Threat Assessment
```
1. query_whois.py <domain>                → domain age, registrar, privacy?
2. query_dns.py all <domain>              → MX, SPF, DKIM present?
3. query_urlscan.py search "domain:<d>"   → has it been scanned before?
4. query_virustotal.py domain <domain>    → detection stats
5. query_ipinfo.py geo <ip>               → hosting provider, proxy flags
6. query_shodan_internetdb.py <ip>        → open ports, vulns, hostnames
7. query_crtsh.py <domain>               → cert history (Let's Encrypt only = red flag)
```

### Image Forensics
```
1. extract_exif.py <image>                → metadata intact or stripped?
2. image_ela.py analyze <image>           → ELA for manipulation detection
3. gemini ask_question_about_video        → visual artifact detection
4. selenium → Google Lens/Yandex/TinEye  → find original version
5. image_ela.py compare <original> <suspect> → pixel-level comparison
```

### Crypto Wallet Tracing
```
1. query_blockchain.py btc <address>      → balance, transaction count
2. tavily_search "<address>"              → has it been tagged/identified?
3. searxng_search "<address>" blockchain  → any forum/exchange mentions?
4. query_blockchain.py eth <address>      → if Ethereum, check there too
```

---

## When You're Stuck

| Problem | Try this |
|---------|----------|
| No results from main tool | Try a different search engine (Tavily vs SearXNG) |
| Can't find a person | Try email permutations, old usernames, family connections |
| Domain has privacy WHOIS | Check cert transparency, DNS records, historical WHOIS |
| Image has no EXIF | Use reverse image search, visual clue analysis with Gemini |
| Dead end on one platform | Pivot to a different platform (Reddit, archived pages, Common Crawl) |
| Too many results | Use Google dorking operators to narrow (`site:`, `filetype:`, date ranges) |
| Need historical data | Wayback Machine (`internet-archive` MCP), `query_archive_today.py`, `common-crawl` MCP |
| Entity is ambiguous | Use `query_wikidata_sparql.py entity` to disambiguate with structured data |

---

## Investigation Quality Checklist

Before finishing, verify:

- [ ] Every finding has a source logged in `search-log.md`
- [ ] Multiple independent sources confirm key findings (not just one)
- [ ] Dead ends are documented (so you don't repeat them)
- [ ] The evidence chain is traceable: source → finding → conclusion
- [ ] No assumptions are stated as facts — note confidence levels
- [ ] OPSEC was maintained (passive collection only unless authorized)
