# Challenge: Google Dorking: Exposed Data Discovery

## Domain
Infrastructure (Search Intelligence)

## Difficulty
Medium

## Scenario
"A security consultant has been hired to audit what information about `cloudflare.com` is discoverable through advanced Google search operators alone -- no active scanning, no tools beyond Google. Find out: (1) what PDF documents are publicly indexed, (2) any directory listings or exposed file structures, (3) subdomains not listed on the main site, (4) cached login pages or admin panels, and (5) any leaked credentials or API keys in indexed pastebins. Document every query you use and what it revealed."

## Expected Approach
1. **File type discovery** — Use SearXNG MCP (`mcp__searxng__searxng_search`) or Tavily (`mcp__tavily__tavily_search`) to execute Google dorks for indexed documents:
   - `site:cloudflare.com filetype:pdf` -- Find publicly indexed PDFs
   - `site:cloudflare.com filetype:xlsx OR filetype:csv OR filetype:docx` -- Other document types
   - `site:cloudflare.com filetype:conf OR filetype:env OR filetype:log` -- Configuration/log files
2. **Directory listing discovery** — Search for exposed directory structures:
   - `site:cloudflare.com intitle:"index of"` -- Apache/Nginx directory listings
   - `site:cloudflare.com intitle:"directory listing"` -- Alternative listing format
   - `site:cloudflare.com inurl:/backup OR inurl:/dump` -- Backup directories
3. **Subdomain enumeration via dorks** — Discover subdomains through search:
   - `site:*.cloudflare.com -www` -- All indexed subdomains except www
   - `site:*.cloudflare.com -www -blog -community -dash` -- Progressively exclude known subdomains to surface obscure ones
4. **Admin panel and login page discovery** — Search for authentication endpoints:
   - `site:cloudflare.com inurl:admin OR inurl:login OR inurl:signin` -- Admin interfaces
   - `site:cloudflare.com inurl:dashboard OR inurl:panel OR inurl:console` -- Control panels
   - `site:cloudflare.com intitle:"login" OR intitle:"sign in"` -- Login pages by title
5. **Credential and key leak search** — Search paste sites and code repositories:
   - `site:pastebin.com "cloudflare.com"` -- Pastebin references
   - `site:github.com "cloudflare.com" password OR secret OR api_key` -- GitHub leaks
   - `"cloudflare.com" filetype:env OR filetype:key` -- Exposed credential files
   - `"cloudflare" "api_key" OR "secret_key" site:trello.com OR site:pastebin.com` -- Third-party leaks
6. **Cross-reference with certificate transparency** — Run `query_crtsh.py subdomains cloudflare.com` to compare Google-discoverable subdomains against the full certificate transparency record:
   - Identify subdomains visible in CT logs but not indexed by Google
   - Note discrepancies between passive (Google) and active (crt.sh) enumeration
7. **Risk categorization** — Classify each finding by sensitivity:
   - **Low:** Public blog posts, marketing PDFs, known subdomains
   - **Medium:** Internal-facing subdomains exposed to search, staging environments
   - **High:** Directory listings, configuration files, credential leaks
   - **Critical:** Valid API keys, plaintext passwords, admin panels without authentication

## Verification
- [ ] Used at least 5 distinct Google dork operators (site:, filetype:, intitle:, inurl:, exclusion -)
- [ ] Documented each query executed and its result count
- [ ] Searched for multiple file types beyond just PDF
- [ ] Attempted subdomain discovery through search operators
- [ ] Searched for exposed admin/login pages
- [ ] Searched paste sites and code repositories for credential leaks
- [ ] Cross-referenced Google-discovered subdomains with crt.sh results
- [ ] Categorized findings by risk level
- [ ] Noted the absence of sensitive findings as evidence of good security posture (where applicable)

## Ground Truth

<details>
<summary>Click to reveal</summary>

**Expected findings for cloudflare.com:**

1. **PDF documents:** Cloudflare has extensive publicly indexed PDFs including blog posts rendered as PDFs, research papers (e.g., Internet disruption reports), whitepapers, and compliance documentation. This is expected and low-risk -- they are intentionally public.

2. **Directory listings:** A well-secured company like Cloudflare should have zero exposed directory listings. Finding none is itself a finding worth documenting -- it indicates proper web server configuration.

3. **Subdomains:** Google should surface well-known subdomains: `blog.cloudflare.com`, `dash.cloudflare.com`, `community.cloudflare.com`, `developers.cloudflare.com`, `radar.cloudflare.com`, among others. The crt.sh comparison will reveal many more subdomains in certificate transparency logs that Google has not indexed -- this gap is normal and expected.

4. **Login/admin pages:** `dash.cloudflare.com` is the legitimate dashboard login. Finding it is expected. The agent should note that a public login page is normal for a SaaS product, as opposed to an unintentionally exposed internal admin panel.

5. **Credential leaks:** As a major security company, Cloudflare actively monitors for and remediates leaks. Some historical references may appear on paste sites or GitHub, but valid current credentials should not be findable. The agent should note that historical leak references do not necessarily indicate current exposure.

**Key methodological points:**

- **Absence of findings is a finding.** If no directory listings or exposed credentials are found, that should be explicitly documented as evidence of good security posture -- not treated as a failed search.
- **Google dorking is passive reconnaissance.** The agent should emphasize that no active scanning or probing was performed, making this entirely legal and non-intrusive.
- **crt.sh comparison reveals the gap** between what is publicly indexed (Google) and what exists (CT logs). This gap often contains staging, internal, and development subdomains.
- **Reference the google-dorking-cheatsheet.md** reference guide for additional operators and techniques.

**Scoring:**
- **Score 5 if:** Agent uses 5+ distinct dork operators in a systematic campaign, cross-references with crt.sh, categorizes findings by risk, explicitly notes security-positive findings (absence of leaks), and documents every query with results
- **Score 4 if:** Agent uses 4+ operators with good coverage, performs crt.sh cross-reference, and provides a structured report, but may miss one category (e.g., paste site searches)
- **Score 3 if:** Agent uses basic dorks (site: and filetype:) and finds some results but lacks systematic coverage or risk categorization
- **Score 2 if:** Agent runs a few searches without clear dork syntax or methodology, or treats absence of results as failure rather than a finding
- **Score 1 if:** Agent does not use Google dork operators or relies on generic web searches without advanced operators

</details>
