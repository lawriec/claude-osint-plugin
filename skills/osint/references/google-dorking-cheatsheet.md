# Google Advanced Search Operators (Dorking) Cheatsheet

Complete reference for Google search operators used in OSINT investigations. These operators refine searches to find specific content types, domains, and patterns that standard searches miss.

---

## Core Operators

### Domain and URL Operators

| Operator | Function | Example |
|----------|----------|---------|
| `site:` | Restrict results to a specific domain or subdomain | `site:example.com "admin panel"` |
| `inurl:` | Require a term to appear in the page URL | `inurl:login site:example.com` |
| `allinurl:` | Require ALL terms to appear in the URL | `allinurl:admin login panel` |
| `related:` | Find sites similar to the specified URL | `related:example.com` |
| `info:` | Show Google's information about a URL | `info:example.com` |
| `cache:` | Show Google's cached version of a page | `cache:example.com/page` |
| `link:` | Find pages linking to a URL (deprecated, may still partially work) | `link:example.com` |

### Content Operators

| Operator | Function | Example |
|----------|----------|---------|
| `intitle:` | Require a term in the page title | `intitle:"index of" site:example.com` |
| `allintitle:` | Require ALL terms in the page title | `allintitle:admin login portal` |
| `intext:` | Require a term in the page body text | `intext:"password" site:example.com` |
| `allintext:` | Require ALL terms in the page body | `allintext:username password login` |
| `inanchor:` | Term appears in link anchor text pointing to the result | `inanchor:"click here" site:example.com` |

### File Type Operators

| Operator | Function | Example |
|----------|----------|---------|
| `filetype:` | Restrict to a specific file extension | `filetype:pdf site:example.com "confidential"` |
| `ext:` | Same as filetype (alias) | `ext:xlsx "budget" site:example.com` |

Common file types for OSINT:

| Extension | Document Type | OSINT Value |
|-----------|--------------|-------------|
| `pdf` | PDF documents | Reports, filings, manuals, presentations |
| `doc` / `docx` | Word documents | Internal documents, letters, proposals |
| `xls` / `xlsx` | Excel spreadsheets | Financial data, lists, databases |
| `ppt` / `pptx` | PowerPoint presentations | Strategy decks, internal presentations |
| `csv` | Comma-separated values | Data exports, databases |
| `txt` | Plain text | Logs, notes, configuration files |
| `xml` | XML files | Sitemaps, configurations, data feeds |
| `json` | JSON files | API responses, configuration data |
| `sql` | SQL files | Database dumps, schema definitions |
| `log` | Log files | Application logs, access logs |
| `env` | Environment files | Configuration with credentials (sensitive) |
| `conf` / `cfg` | Configuration files | Server and application configurations |
| `bak` | Backup files | Database backups, file backups |
| `key` / `pem` | Key files | Private keys, certificates (sensitive) |
| `kml` / `kmz` | Google Earth files | Geographic data, location markers |
| `gpx` | GPS exchange format | GPS tracks and waypoints |

### Boolean and Text Operators

| Operator | Function | Example |
|----------|----------|---------|
| `"..."` | Exact phrase match | `"John Doe" "Acme Corporation"` |
| `-` | Exclude a term or operator | `"John Doe" -site:facebook.com -site:linkedin.com` |
| `OR` or `\|` | Match either term | `"John Doe" (linkedin OR facebook)` |
| `*` | Wildcard (matches any word) | `"John * Doe"` (matches "John Michael Doe", "John A. Doe", etc.) |
| `AROUND(N)` | Terms must appear within N words of each other | `"CEO" AROUND(3) "resigned"` |
| `()` | Group operators | `site:example.com (filetype:pdf OR filetype:docx)` |

### Date and Number Operators

| Operator | Function | Example |
|----------|----------|---------|
| `before:` | Results from before a date (YYYY-MM-DD) | `site:example.com "announcement" before:2020-01-01` |
| `after:` | Results from after a date (YYYY-MM-DD) | `site:example.com "announcement" after:2024-01-01` |
| `..` (numrange) | Number range | `"employee ID" 1000..2000` |

---

## OSINT-Specific Search Recipes

### People Search

**Find a person across platforms:**
```
"John Doe" site:linkedin.com/in/
"John Doe" site:facebook.com
"John Doe" site:twitter.com OR site:x.com
"John Doe" (site:facebook.com | site:instagram.com | site:twitter.com | site:linkedin.com)
```

**Find mentions outside major social media (often more revealing):**
```
"John Doe" -site:facebook.com -site:twitter.com -site:linkedin.com -site:instagram.com
"@johndoe" -site:twitter.com -site:x.com
```

**Find email addresses:**
```
"john.doe@" site:github.com
"john.doe@example.com"
"johndoe" "@gmail.com" OR "@yahoo.com" OR "@outlook.com"
```

**Find resumes and CVs:**
```
"John Doe" filetype:pdf (resume OR CV OR "curriculum vitae")
"John Doe" filetype:docx (resume OR CV)
"John Doe" site:slideshare.net
```

**Find forum/community activity:**
```
"johndoe" site:reddit.com
"johndoe" site:stackoverflow.com
"johndoe" site:medium.com
"johndoe" site:quora.com
"johndoe" (site:discourse.org OR inurl:forum OR inurl:community)
```

**Find publications and academic work:**
```
"John Doe" site:scholar.google.com
"John Doe" site:researchgate.net
"John Doe" filetype:pdf (site:arxiv.org OR site:ssrn.com)
"John Doe" site:orcid.org
```

### Infrastructure and Domain Discovery

**Find subdomains (indexed by Google):**
```
site:*.example.com -www
site:example.com -www -site:www.example.com
```

**Find directory listings:**
```
intitle:"index of" site:example.com
intitle:"index of /" site:example.com
```

**Find exposed configuration and environment files:**
```
site:example.com filetype:env
site:example.com filetype:yml "password"
site:example.com filetype:conf
site:example.com filetype:ini
site:example.com filetype:xml "configuration"
site:example.com filetype:json "apikey" OR "api_key" OR "secret"
```

**Find exposed log files:**
```
site:example.com filetype:log
site:example.com filetype:log "error" OR "warning"
intitle:"index of" "access.log" site:example.com
```

**Find admin panels and login pages:**
```
site:example.com inurl:admin
site:example.com inurl:login
site:example.com intitle:"admin" OR intitle:"login" OR intitle:"dashboard"
site:example.com inurl:wp-admin OR inurl:wp-login
site:example.com inurl:administrator
```

**Find sitemaps and robots.txt:**
```
site:example.com filetype:xml "sitemap"
site:example.com inurl:robots.txt
```

**Find error pages revealing technology stack:**
```
site:example.com "Fatal error" OR "Warning:" OR "Notice:"
site:example.com "stack trace" OR "traceback"
site:example.com "SQL syntax" OR "mysql_fetch"
```

### Exposed Credentials and Sensitive Data

**Leaked data on paste sites:**
```
site:pastebin.com "example.com"
site:paste.ee "example.com"
site:ghostbin.co "example.com"
site:justpaste.it "example.com"
"example.com" (site:pastebin.com | site:paste.ee | site:justpaste.it)
```

**Code repository leaks:**
```
site:github.com "example.com" password
site:github.com "example.com" "api_key" OR "apikey" OR "secret"
site:gitlab.com "example.com" password
site:bitbucket.org "example.com" password
site:github.com "example.com" filetype:env
```

**Database dumps:**
```
filetype:sql "example.com"
filetype:sql "INSERT INTO" "example.com"
filetype:csv "example.com" "email" "password"
filetype:bak "example.com"
```

**Exposed files with credentials:**
```
intitle:"index of" "credentials"
intitle:"index of" ".env"
intitle:"index of" "id_rsa"
intitle:"index of" "wp-config.php"
filetype:pem "PRIVATE KEY"
filetype:key "PRIVATE KEY"
```

### Document Discovery

**All documents on a domain:**
```
site:example.com filetype:pdf
site:example.com filetype:docx OR filetype:doc
site:example.com filetype:xlsx OR filetype:xls
site:example.com filetype:pptx OR filetype:ppt
site:example.com (filetype:pdf | filetype:docx | filetype:xlsx | filetype:pptx)
```

**Sensitive documents:**
```
site:example.com filetype:pdf "confidential"
site:example.com filetype:pdf "internal use only"
site:example.com filetype:pdf "not for distribution"
site:example.com filetype:pdf "draft" OR "privileged"
```

**Documents mentioning a specific person or topic:**
```
filetype:pdf "John Doe" "Acme Corporation"
filetype:pdf "Project Phoenix" site:example.com
filetype:xlsx "salary" OR "compensation" site:example.com
```

**Financial documents:**
```
site:example.com filetype:pdf "annual report"
site:example.com filetype:pdf "financial statement"
site:example.com filetype:xlsx "budget"
filetype:pdf "example.com" "10-K" OR "10-Q"
```

### Historical and Cached Content

**Google's cached version of a page:**
```
cache:example.com/removed-page
```

**Temporal narrowing (combine with other operators):**
```
site:example.com "announcement" after:2024-01-01 before:2024-06-30
"John Doe" "Acme Corp" after:2020-01-01 before:2022-01-01
site:example.com "breach" OR "incident" after:2023-01-01
```

### Geolocation Searches

**Coordinates in web pages:**
```
"51.5074" "-0.1278" site:example.com
"latitude" "longitude" site:example.com
```

**Geotagged photos:**
```
"EXIF" "GPS" site:flickr.com "example location"
"coordinates" filetype:kml site:example.com
filetype:gpx "trail name"
```

**Location-specific results:**
```
site:example.com "123 Main Street"
"example.com" "New York" OR "London" OR "Tokyo"
```

### Social Media Deep Search

**Reddit:**
```
site:reddit.com/r/OSINT "technique"
site:reddit.com "johndoe"
site:reddit.com/user/johndoe
"example.com" site:reddit.com
```

**YouTube:**
```
site:youtube.com "OSINT" "tutorial"
site:youtube.com "John Doe" "interview"
site:youtube.com/channel/ "example topic"
```

**Medium and blogs:**
```
site:medium.com "@johndoe"
site:medium.com "example.com"
site:substack.com "John Doe"
inurl:blog "example topic" "John Doe"
```

**GitHub user activity:**
```
site:github.com "johndoe"
site:github.com author:johndoe
"johndoe" site:github.com/*/issues
```

---

## Operator Combinations

The real power of Google dorking is combining operators. Here are patterns for common OSINT scenarios:

### Investigate an Organization

```
# Find all indexed subdomains
site:*.example.com -www

# Find all documents
site:example.com (filetype:pdf | filetype:docx | filetype:xlsx)

# Find exposed admin/internal pages
site:example.com (inurl:admin | inurl:internal | inurl:portal | inurl:intranet)

# Find employee names
site:example.com filetype:pdf "team" OR "staff" OR "directory"

# Find technology stack clues
site:example.com "powered by" OR "built with"

# Find connected organizations
"example.com" -site:example.com (site:linkedin.com | site:crunchbase.com | site:bloomberg.com)
```

### Investigate a Person

```
# Comprehensive social media search
"John Doe" (site:linkedin.com | site:facebook.com | site:twitter.com | site:instagram.com)

# Find content they created
"John Doe" (site:medium.com | site:github.com | site:stackoverflow.com | site:slideshare.net)

# Find mentions by others
"John Doe" -site:linkedin.com -site:facebook.com -site:twitter.com "CEO" OR "founder" OR "director"

# Find associated email addresses
"John Doe" ("@gmail.com" | "@yahoo.com" | "@example.com")

# Find in legal or government records
"John Doe" (site:courtlistener.com | site:sec.gov | filetype:pdf "plaintiff" OR "defendant")
```

---

## Google Dorking Ethics

**Finding exposed data is NOT authorization to access it.**

- Directory listings, login pages, and configuration files found via dorking are publicly indexed but may not be intended for public access
- Do not use dorking to access systems, download databases, or exploit vulnerabilities
- If you find exposed credentials or sensitive data, consider responsible disclosure
- Automated dorking at scale may violate Google's Terms of Service
- See `opsec-ethics.md` for complete ethical guidelines
- Your purpose is intelligence gathering from public information, not penetration testing

**Legal considerations:**
- Viewing publicly indexed pages is generally legal in most jurisdictions
- Accessing systems using discovered credentials is unauthorized access (illegal)
- Downloading exposed databases may be illegal depending on the contents and jurisdiction
- Laws vary significantly by country — when in doubt, consult legal counsel

---

## Limitations and Workarounds

### Google Rate Limiting

Google rate-limits automated and rapid sequential queries:
- **Manual searches:** Generally 50-100 queries before CAPTCHA
- **Automated scraping:** Will be blocked quickly
- **Workaround:** Use SearXNG (`searxng_search` MCP tool) to distribute queries across multiple search engines simultaneously
- **Workaround:** Space queries manually and vary search patterns
- **Workaround:** Use Google Custom Search API (100 free queries/day, paid beyond that)

### Deprecated or Inconsistent Operators

| Operator | Status |
|----------|--------|
| `link:` | Officially deprecated; may return partial results |
| `info:` | Reduced functionality; mostly redirects to a normal search |
| `inanchor:` | Inconsistent results; works sometimes |
| `cache:` | Being phased out by Google (2024+); may not work for all pages |
| `~` (synonym) | Deprecated; Google now does synonym expansion automatically |
| `+` (force include) | Deprecated; use `"exact phrase"` instead |

### Indexing Gaps

Google does not index everything:
- **Deep web:** Content behind login walls, paywalls, or forms
- **Dynamically generated pages:** Some JavaScript-rendered content is not indexed
- **Deliberately excluded:** Pages blocked by robots.txt or noindex meta tags
- **Freshness:** Recently published pages may take days or weeks to be indexed
- **Removed content:** Deindexed pages (DMCA takedowns, right to be forgotten requests)

### Alternative Search Engines for Additional Coverage

| Engine | Strength |
|--------|----------|
| **Bing** | Sometimes indexes pages Google misses; better for some site: queries |
| **Yandex** | Better coverage of Russian/CIS websites; powerful image search |
| **DuckDuckGo** | Uses Bing index; useful for non-personalized results |
| **Baidu** | Chinese internet coverage |
| **Shodan** | Indexes internet-connected devices (not web pages) |
| **Censys** | Indexes certificates and hosts |
| **SearXNG** | Meta-search across all of the above (use `searxng_search` tool) |

**Strategy:** Run important queries on at least Google and one alternative engine. Use SearXNG to efficiently query multiple engines in a single request.

---

## Quick Reference Card

**Find all PDFs on a domain:**
`site:example.com filetype:pdf`

**Find subdomains:**
`site:*.example.com -www`

**Find a person on LinkedIn:**
`"John Doe" site:linkedin.com/in/`

**Find exposed directory listings:**
`intitle:"index of" site:example.com`

**Find leaked credentials:**
`site:pastebin.com "example.com"`

**Find documents mentioning two things:**
`filetype:pdf "Project Alpha" "example.com"`

**Exclude noise from results:**
`"search term" -site:pinterest.com -site:facebook.com`

**Find pages from a specific time period:**
`site:example.com "announcement" after:2024-01-01 before:2024-12-31`

**Find terms near each other:**
`"CEO" AROUND(5) "arrested"`

**Search for a code/ID pattern:**
`"employee ID" 5000..6000 site:example.com`

---

## Cross-References

- `domain-infrastructure.md` — Deep infrastructure investigation techniques (DNS, WHOIS, certificates)
- `people-social-media.md` — Social media investigation methodology
- `opsec-ethics.md` — Ethical guidelines for search and data collection
- `tool-guide.md` — SearXNG, Tavily, and other search tools available in the plugin
- `document-analysis.md` — Analyzing documents found via dorking
