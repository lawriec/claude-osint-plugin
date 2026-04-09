# Challenge: Company Background Investigation

## Domain
Corporate OSINT

## Difficulty
Hard

## Scenario
"A due diligence firm has been hired to investigate a potential business partner: 'Cloudflare, Inc.' Before entering a contract, the client needs a comprehensive background report covering:

1. Corporate structure and key leadership
2. Technical infrastructure footprint
3. Online presence and reputation
4. Any red flags or concerns

Conduct the investigation using only public sources. Produce a structured due diligence report with confidence levels for each finding."

## Expected Approach
1. **Company background research** -- Use Tavily (`mcp__tavily__tavily_search`) to search for Cloudflare corporate information, SEC filings, news articles, and press releases. Identify founding date, IPO status, stock ticker, headquarters location, and business model.
2. **Domain registration analysis** -- `query_whois.py lookup cloudflare.com`:
   - Check registration date and registrar
   - Check registrant organization details
   - Evaluate domain age as an indicator of legitimacy
   - Note any WHOIS privacy settings
3. **DNS infrastructure enumeration** -- `query_dns.py all cloudflare.com`:
   - Map A, AAAA, MX, NS, TXT, SOA records
   - Assess infrastructure complexity (enterprise-grade DNS indicates established company)
   - Check for SPF, DKIM, DMARC as indicators of email security maturity
4. **Certificate transparency analysis** -- `query_crtsh.py subdomains cloudflare.com`:
   - Enumerate subdomains to assess scale of certificate infrastructure
   - Identify operational domains (api, dash, developers, etc.)
   - Volume of certificates indicates organizational scale
5. **IP and service reconnaissance** -- `query_shodan_internetdb.py` on discovered IPs:
   - Identify open services and ports
   - Assess hosting infrastructure
   - Note AS number and network ownership
6. **Social media presence** -- `check_username.py cloudflare`:
   - Verify presence across major platforms
   - Consistent branding across platforms indicates legitimacy
7. **Historical web presence** -- Use Common Crawl MCP (`mcp__common-crawl__cc_search` or `mcp__common-crawl__cc_domain_summary`):
   - Analyze how long the domain has appeared in web crawls
   - Check historical content consistency
   - Look for changes in business description over time
8. **Knowledge graph construction** -- Use memory-graph MCP (`mcp__memory-graph__create_entities`, `mcp__memory-graph__create_relations`):
   - Create entities: Cloudflare Inc, Matthew Prince (CEO), Michelle Zatlyn (COO/President), key investors, subsidiaries
   - Map relationships: leadership, ownership, partnerships
   - Build a queryable graph of the corporate structure
9. **Report compilation** -- Synthesize all findings into a structured due diligence report with confidence levels (High/Medium/Low) for each section.

## Verification
- [ ] Company founding date, IPO year, and stock ticker identified
- [ ] Key leadership (CEO, COO at minimum) identified by name
- [ ] WHOIS registration details retrieved and analyzed
- [ ] DNS records enumerated showing infrastructure complexity
- [ ] Certificate transparency search returned subdomains at scale
- [ ] At least one IP investigated via Shodan InternetDB
- [ ] Social media presence checked across multiple platforms
- [ ] Common Crawl used to assess historical web presence
- [ ] Knowledge graph built with entities and relationships
- [ ] Final report includes confidence levels per section
- [ ] Overall assessment of legitimacy provided

## Ground Truth

<details>
<summary>Click to reveal</summary>

**Cloudflare, Inc. -- Key Facts:**

1. **Corporate basics:**
   - Founded: 2009 by Matthew Prince, Lee Holloway, and Michelle Zatlyn
   - Incorporated in Delaware, headquartered in San Francisco, CA
   - NYSE: NET (IPO September 2019)
   - Major internet infrastructure and security company

2. **Key leadership:**
   - Matthew Prince -- Co-founder and CEO
   - Michelle Zatlyn -- Co-founder, President and COO
   - Thomas Seifert -- CFO
   - Board includes well-known tech investors and executives

3. **Infrastructure findings:**
   - AS13335 is one of the largest autonomous systems on the internet
   - Operates a global anycast network spanning 300+ cities
   - `cloudflare.com` has enterprise-grade DNS with extensive records
   - Thousands of subdomains reflecting a large-scale SaaS operation
   - WHOIS shows long-standing registration with corporate registrant

4. **Web and social presence:**
   - Active on all major social platforms (Twitter/X, LinkedIn, GitHub, etc.)
   - Consistent branding and high follower counts
   - Regular blog posts, developer documentation, transparency reports

5. **Assessment:**
   - Cloudflare is a legitimate, well-established, publicly traded technology company
   - No significant red flags for a due diligence investigation
   - Strong infrastructure, transparent leadership, active public communications

**Scoring:**
- **Score 5 if:** Agent investigates 8+ dimensions (WHOIS, DNS, crt.sh, Shodan, social media, Common Crawl, web search, knowledge graph), produces a structured report with confidence levels, uses memory-graph for entity mapping, and correctly concludes Cloudflare is a legitimate major tech company
- **Score 4 if:** Agent covers 6-7 investigation dimensions, produces a structured report, and uses at least one of Common Crawl or memory-graph
- **Score 3 if:** Agent covers 4-5 dimensions with reasonable analysis but misses Common Crawl, knowledge graph, or confidence levels
- **Score 2 if:** Agent runs some tools but produces only a surface-level summary without structured assessment
- **Score 1 if:** Agent relies primarily on web search without leveraging infrastructure investigation tools

</details>
