---
name: osint
description: >
  Use when the user wants to conduct open source intelligence research — investigating
  people, locations, domains, images, infrastructure, vehicles, or digital artifacts using
  publicly available information. Triggers on: "OSINT", "investigate", "who is this person",
  "where was this photo taken", "find information about", "trace this", "identify this location",
  "lookup this domain", "reverse image search", "find this username", "social media footprint",
  "geolocate", "WHOIS", "DNS lookup", "EXIF data", "metadata analysis", "digital forensics",
  "blockchain trace", "IP lookup", "certificate transparency". Also triggers when the user
  provides an image and asks where it was taken, or provides a username and asks what accounts
  exist, or provides a domain and asks about its infrastructure.
---

# OSINT Investigation Skill

## Philosophy

OSINT is the discipline of collecting, processing, and analyzing publicly available information to produce actionable intelligence. The power of OSINT lies not in any single data source but in cross-referencing — a username leads to an email, which leads to a domain, which leads to an IP, which leads to a physical location. Each connection strengthens the picture.

Every investigation follows the intelligence cycle: define requirements, plan collection, collect data, analyze findings, report results. This is not bureaucracy — it is how you avoid wasting time, missing evidence, and falling into confirmation bias.

Three non-negotiable principles:
1. **Document everything.** Every search query, every result, every dead end. If it is not logged, it did not happen.
2. **Follow the evidence.** Do not chase a theory. Collect data, then see where it points.
3. **Respect boundaries.** Legal and ethical limits are hard constraints, not suggestions. When in doubt, stop and assess.


## Quick Reference: When to Load Reference Files

All reference files live in `references/`. Load them on demand — do not read them all upfront.

| Situation | Read |
|---|---|
| **Starting any new investigation** | **`quick-start.md`** |
| Setting up or resuming an investigation | `investigation-setup.md` |
| Understanding the OSINT intelligence cycle | `osint-cycle.md` |
| Knowledge graph operations | `knowledge-graph.md` |
| Choosing tools, handling tool failures | `tool-guide.md` |
| Legal/ethical questions, OPSEC concerns | `opsec-ethics.md` |
| Free API endpoints and rate limits | `open-apis.md` |
| Finding the right platform/tool for a domain | `platform-directory.md` |
| Geolocation from images/video | `geolocation.md` |
| Investigating a person or social media | `people-social-media.md` |
| Domain, IP, DNS, infrastructure recon | `domain-infrastructure.md` |
| Image/video metadata and forensics | `image-video-forensics.md` |
| Writing investigation reports | `reporting.md` |
| Document metadata, email headers | `document-analysis.md` |
| Vehicle, aircraft, ship identification | `vehicle-object-id.md` |
| Cryptocurrency and blockchain analysis | `crypto-financial.md` |
| Radio signals and broadcast identification | `radio-signals.md` |
| Dark web research methodology and OPSEC | `dark-web-research.md` |
| Google dorking operators and patterns | `google-dorking-cheatsheet.md` |
| OSINT communities, training, and resources | `osint-landscape.md` |


## Before You Start: Ethics and OPSEC

This section is not optional. Read it before every investigation.

**Hard rules — never break these:**
- NEVER log into accounts you do not own or control.
- NEVER impersonate someone or use social engineering against a target.
- NEVER access systems without authorization, even if credentials are found in public data.
- NEVER collect data on minors beyond what is strictly necessary and legally permitted.
- NEVER share raw personal data (SSNs, financial details, medical records) in reports unless the user has a legitimate need and legal authority.

**Awareness requirements:**
- Privacy laws vary by jurisdiction. GDPR (EU), CCPA (California), PIPEDA (Canada), and others impose different obligations. Consider where the target and the investigator are located.
- Some OSINT activities may constitute surveillance under local law. Sustained monitoring of an individual's online activity can cross legal lines even if each individual lookup is legal.
- Accessing data that was obtained through a breach is legally grey at best in many jurisdictions, even if it is publicly available.
- Your investigation may leave traces. DNS lookups, website visits, social media profile views — all can alert a target. Consider whether passive-only collection is required.
- Document your ethical reasoning. If you decide a particular collection method is acceptable, write down why. If it is borderline, err on the side of caution.

**When in doubt:** Read `opsec-ethics.md` for detailed guidance, case studies, and decision frameworks.


## The Intelligence Cycle

Every investigation follows these five steps. Do not skip any of them.

### Step 1: Define the Intelligence Requirement

Before collecting a single piece of data, answer these questions:

**What does the user need to know?**
Restate the question in your own words. Vague requests like "find out about this person" need to be narrowed: Are they looking for contact information? Professional background? Online presence? Criminal history? Location history?

**What domains does this investigation span?**
Classify the work into one or more of these categories:
- Geolocation (where is this place / where was this photo taken?)
- People / Social Media (who is this person / what is their online presence?)
- Infrastructure (what is behind this domain / IP / email?)
- Image / Video Forensics (is this image authentic / what can we extract?)
- Document Analysis (what does the metadata reveal?)
- Vehicle / Object Identification (what is this vehicle / aircraft / ship?)
- Financial / Cryptocurrency (where did this money go?)
- Signals / Broadcast (what is this radio signal / broadcast?)

**What does success look like?**
Define concrete deliverables. "A list of all social media accounts associated with this username" is testable. "Everything about this person" is not.

**What are the constraints?**
- Time: Is this urgent?
- Scope: What is out of bounds?
- Ethics: Are there any special considerations?
- Legal: What jurisdiction applies?

**Load reference files** for each identified domain.

### Step 2: Plan Collection Strategy

With the requirement defined, plan how to collect the data.

**Order of operations matters:**
1. Start with passive collection (querying public databases, cached data, archives). This leaves minimal traces.
2. Move to semi-passive (visiting websites, loading profiles). This may leave traces in logs.
3. Only perform active collection (port scanning, direct interaction) if explicitly authorized.

**Identify pivot opportunities:**
Think ahead about how findings might chain together. If you are investigating a username, plan for the possibility that you will find an email, which might lead to domains. Have the tools ready.

**Choose your tools:**
Based on the domains identified in Step 1, determine which MCP servers, scripts, and APIs you will need. Read `tool-guide.md` if uncertain about capabilities or availability.

**Set up the workspace:**
Read `investigation-setup.md` and scaffold the investigation directory:
```
investigation-name/
├── search-log.md       # Every query and result
├── leads.md            # Active leads (HIGH/MEDIUM/LOW)
├── dead-ends.md        # What failed and why
├── evidence-chain.md   # Source → finding → conclusion
└── report.md           # Structured findings
```

Initialize the knowledge graph with the seed entities (the starting data points the user has provided).

### Step 3: Collection

This is where the work happens. The approach depends entirely on the investigation domain(s).

#### Geolocation

Systematic narrowing from broad to specific:
1. **Language and script** — What language is visible in signs, text, documents? This narrows to a country or region.
2. **Environmental clues** — Vegetation, terrain, climate, sun position, architecture, road markings, vehicles.
3. **Infrastructure clues** — Power line styles, utility poles, road signs, bollards, license plates.
4. **Specific identifiers** — Business names, phone numbers, addresses, landmarks.
5. **Verification** — Cross-reference with satellite imagery, street view, local maps.

Use Gemini for image analysis (it handles visual question-answering well). Use `sun_position.py` for shadow-based time/location estimation. Use `google-reverse-image` (Cloud Vision Web Detection) for reverse image search to find matching locations, or `selenium` to drive Google Lens / Yandex when you need a UI-driven workflow.

Read `geolocation.md` for the full methodology, including worked examples.

#### People and Social Media

Start with whatever identifiers you have and expand outward:
1. **Username enumeration** — Use `check_username.py` to test a username across platforms.
2. **Email discovery** — Check for email-to-username patterns, use breach databases (where legally permitted), check PGP key servers.
3. **Profile analysis** — Extract all available information from each discovered profile: bio, connections, posts, timestamps, locations.
4. **Cross-referencing** — Match profile photos, writing style, posted times, shared content across platforms.
5. **Network mapping** — Who do they interact with? Frequent commenters, shared group memberships, tagged photos.

Read `people-social-media.md` for platform-specific techniques and common pivot patterns.

#### Domain and Infrastructure

Passive reconnaissance first, active only with authorization:
1. **WHOIS** — Registration data, registrant info, nameservers, registration/expiration dates. Use `query_whois.py`.
2. **DNS enumeration** — A, AAAA, MX, TXT, NS, SOA, CNAME records. Use `query_dns.py`. Look for SPF, DKIM, DMARC in TXT records.
3. **Certificate transparency** — Discover subdomains via crt.sh. Use `query_crtsh.py`.
4. **IP enrichment** — Reverse DNS, geolocation, open ports, known services. Use `query_shodan_internetdb.py` for free enrichment.
5. **Historical data** — Wayback Machine for historical snapshots. Common Crawl for historical page content.
6. **Relationship mapping** — Shared IPs, shared nameservers, shared registrant data, shared analytics IDs, shared ad network IDs.

Read `domain-infrastructure.md` for the full methodology.

#### Image and Video Forensics

Extract and analyze all available metadata:
1. **EXIF data** — Use `extract_exif.py` for camera model, GPS coordinates, timestamps, software used.
2. **Reverse image search** — Find other instances of the image online. Identify the original source.
3. **Manipulation detection** — Look for signs of editing: inconsistent lighting, clone stamp artifacts, metadata inconsistencies, Error Level Analysis.
4. **Content analysis** — Use Gemini to identify objects, text, locations, people in images.
5. **Video-specific** — Extract frames at key moments, analyze audio, check for subtitle tracks, examine video metadata with `yt-dl`.

Read `image-video-forensics.md` for detailed techniques.

#### Multi-Domain Investigations

Most real investigations cross domain boundaries. A person investigation might reveal a domain they own, which leads to infrastructure analysis, which reveals other domains, which connect to other people.

Follow the evidence wherever it leads. When you pivot from one domain to another, load the relevant reference file and apply that domain's methodology.

#### Collection Discipline

For EVERY collection action, without exception:

1. **Log the query** in `search-log.md` — what you searched, where, when, and any parameters.
2. **Record the result** — what came back, including null results. Negative results are data.
3. **Triage the result:**
   - If it is a promising lead, add it to `leads.md` with a priority (HIGH/MEDIUM/LOW) and a note on what to do next.
   - If it is a dead end, add it to `dead-ends.md` with a note on why it failed.
   - If it is a confirmed finding, add it to `evidence-chain.md`.
4. **Update the knowledge graph** — add new entities, relationships, and observations using `memory-graph` tools.

### Step 4: Processing and Analysis

Raw data is not intelligence. Analysis transforms data into answers.

**Cross-reference findings across sources.**
A username found on two platforms is interesting. The same username linked to the same email on both platforms is more significant. That email also appearing in WHOIS records for a domain is a strong connection.

**Build timelines.**
When you have temporal data (post timestamps, domain registration dates, WHOIS changes, commit history), arrange it chronologically. Timelines reveal patterns: when was a person active? When did infrastructure change? Do events correlate?

**Assess confidence levels for every finding:**

| Level | Definition | Criteria |
|---|---|---|
| **Confirmed** | Established beyond reasonable doubt | Multiple independent sources agree; direct evidence |
| **Probable** | More likely true than not | Strong evidence from at least one reliable source |
| **Possible** | Plausible but not yet corroborated | Some supporting evidence; needs additional sources |
| **Speculative** | Inference or hypothesis | Based on patterns or a single weak source; flag clearly |

**Look for contradictions.**
When sources disagree, that is often more informative than when they agree. A profile claiming to be in New York but posting at times consistent with Pacific timezone tells you something. A domain WHOIS showing registration in 2020 but Wayback Machine snapshots from 2018 tells you something.

**Document the evidence chain.**
For every conclusion, trace it back to its sources:
```
Source: crt.sh query for example.com
Finding: Subdomain admin.example.com exists
Source: Shodan InternetDB for admin.example.com IP
Finding: Port 22 (SSH) and 443 (HTTPS) open
Conclusion: example.com has an administrative interface (PROBABLE)
```

**Update the knowledge graph** with relationships between entities and confidence assessments.

### Step 5: Reporting

Present findings in a structured format that the user can act on.

**Organize by confidence level.** Lead with confirmed findings, then probable, then possible. Clearly label anything speculative.

**Provide evidence provenance.** Every claim must cite its source. "The domain was registered on 2023-01-15" needs to say "(source: WHOIS query, 2024-03-20)".

**Document negative results.** What you searched for and did not find is important context. It tells the reader (and future investigators) what has already been ruled out.

**Provide next steps.** If the investigation is incomplete, list concrete actions that would advance it. Prioritize by expected value.

**Use structured report templates.** Read `reporting.md` for templates appropriate to different investigation types.


## Tool Quick Reference

The most commonly used tools. For full details, fallback options, and troubleshooting, read `tool-guide.md`.

| Need | Tool/Script | Notes |
|---|---|---|
| Web search | `tavily_search`, `searxng_search` | Tavily for focused queries; SearXNG for broad multi-engine with operator params (site, filetype, after, before, inurl, intitle) |
| Image analysis | `gemini` (`ask_question_about_video`) | Works for both still images and video; strong at visual QA |
| Reverse image search | `google-reverse-image` (`reverse_image_search`) | Cloud Vision Web Detection — pages with the image, exact/partial matches, visually similar |
| Reverse image (browser) | `selenium` (navigate to Google Lens/Yandex) | Fallback when Vision misses or you need a UI-driven workflow |
| Website screenshots | `selenium` (`take_screenshot`) | Document visual evidence of web pages |
| Historical pages | `internet-archive`, `common-crawl` | Wayback Machine snapshots, historical crawl data |
| Video metadata | `yt-dl` (`ytdlp_get_video_metadata`) | YouTube and many other video platforms |
| DNS lookup | `uv run query_dns.py` | Full DNS record enumeration (A, AAAA, MX, TXT, NS, SOA, CNAME) |
| WHOIS | `uv run query_whois.py` | Domain registration data, registrant info |
| Cert transparency | `uv run query_crtsh.py` | Subdomain discovery via certificate logs |
| IP enrichment | `uv run query_shodan_internetdb.py` | Open ports, hostnames, known vulns (free, no API key) |
| EXIF extraction | `uv run extract_exif.py` | GPS coordinates, camera info, timestamps, software |
| Username check | `uv run check_username.py` | Test username existence across many platforms |
| Sun position | `uv run sun_position.py` | Calculate sun angle for shadow-based geolocation |
| Email headers | `uv run analyze_email_headers.py` | Parse email hops, extract originating IPs, detect spoofing |
| IP geolocation | `uv run query_ipinfo.py` | Geo, ASN, hosting/proxy flags via ip-api.com (batch support) |
| URL scanning | `uv run query_urlscan.py` | URLScan.io domain/IP intelligence (free, no key for search) |
| Blockchain | `uv run query_blockchain.py` | Bitcoin/Ethereum address balance and transaction lookup |
| Aircraft tracking | `uv run query_flightradar.py` | OpenSky Network — live flights, aircraft lookup, airport traffic |
| Vessel tracking | `uv run query_ais.py` | Fintraffic AIS — Baltic Sea vessel positions and metadata |
| Reddit discovery | `uv run discover_reddit_threads.py` | Find OSINT-relevant threads across subreddits |
| VirusTotal | `uv run query_virustotal.py` | Domain/IP/URL/hash threat reports (needs VT_API_KEY) |
| Wikidata | `uv run query_wikidata_sparql.py` | Entity resolution, SPARQL queries for people/orgs/places |
| archive.today | `uv run query_archive_today.py` | Search/retrieve archive.today snapshots |
| Censys | `uv run query_censys.py` | Host search and IP detail lookup (needs CENSYS_API_ID/SECRET) |
| Image ELA | `uv run image_ela.py` | Error Level Analysis for detecting image manipulation |
| Knowledge graph | `memory-graph` tools | Track entities, relationships, and observations |
| Reddit research | `reddit` tools | Fetch threads, post content from subreddits |
| Fetch web page | `fetch` | Retrieve raw page content for analysis |
| Video frames | `video-reader` (`extract_frames`) | Pull frames from video for image analysis |

**Tool selection principles:**
- Use Tavily for precise factual queries. Use SearXNG for broad multi-engine exploration with structured operators. Use `google-reverse-image` for reverse image search.
- Always try the purpose-built script first (e.g., `query_dns.py` for DNS). Fall back to web-based tools if the script fails.
- Use Selenium for anything requiring a real browser (JavaScript-heavy sites, CAPTCHAs, interactive tools).
- Use the knowledge graph (`memory-graph`) throughout — it is how you track what you have found and how it connects.


## Investigation Workspace

Every investigation gets its own directory. This is not optional — it is how you maintain the discipline that separates useful OSINT from random Googling.

### Workspace Structure

```
investigation-name/
├── search-log.md       # Every query, tool, timestamp, and result
├── leads.md            # Active leads ranked HIGH / MEDIUM / LOW
├── dead-ends.md        # What was tried and why it failed
├── evidence-chain.md   # Source → finding → conclusion chains
└── report.md           # Structured findings for the user
```

### Search Log Format

```markdown
## [Timestamp or sequence number]
- **Tool:** query_whois.py
- **Query:** example.com
- **Result:** Registered 2023-01-15, registrant: REDACTED, nameservers: ns1.cloudflare.com, ns2.cloudflare.com
- **Action:** Added to evidence-chain. Pivot to DNS enumeration.
```

### Leads Format

```markdown
## HIGH
- [ ] Check DNS records for example.com — WHOIS shows Cloudflare, may reveal origin IP via historical DNS
- [ ] Reverse image search the profile photo — unique enough to potentially find other accounts

## MEDIUM
- [ ] Check Wayback Machine for example.com — may reveal content before current owner

## LOW
- [ ] Search for registrant email on other WHOIS records — likely redacted but worth trying
```

### Dead Ends Format

```markdown
## username_search — Twitter
- **Query:** Searched for @exampleuser on Twitter
- **Result:** Account exists but is private, no useful public data
- **Why dead end:** Cannot extract further information without authentication
- **Logged:** 2024-03-20
```

Read `investigation-setup.md` for full templates and workspace initialization procedures.


## Cross-Domain Pivoting

Cross-domain pivoting is what makes OSINT powerful. A single piece of data in one domain unlocks findings in another. Always be alert for pivot opportunities.

### Common Pivot Chains

**Username to Location:**
```
Username → check_username.py → profiles on multiple platforms
  → Profile analysis → email address in bio
    → Email → WHOIS search → domain ownership
      → Domain → DNS records → IP address
        → IP → geolocation → approximate physical location
```

**Image to Identity:**
```
Image → EXIF extraction → GPS coordinates → specific location
  → Reverse image search → original posting → author's profile
    → Profile → username → cross-platform enumeration → network
```

**Domain to Network:**
```
Domain → WHOIS → registrant email/org
  → Reverse WHOIS → other domains by same registrant
    → Shared hosting analysis → related infrastructure
      → Certificate transparency → subdomains → services
```

**Social Post to Verification:**
```
Social media post → claimed location + timestamp
  → Image in post → EXIF check → actual GPS (if present)
    → Shadow analysis → sun_position.py → consistent with claimed time?
      → Background details → reverse image search → matches claimed location?
```

**Photo to Business:**
```
Photo → reverse image search → matching location in Street View
  → Street View → business names visible → business registry lookup
    → Business registry → owner information → connected entities
```

### Pivot Discipline

Every time you pivot from one domain to another:
1. Log the pivot in `search-log.md` — what prompted it, what you expect to find.
2. Load the relevant domain reference file if you have not already.
3. Add new entities and relationships to the knowledge graph.
4. Update `evidence-chain.md` with the connection between domains.
5. Check whether the pivot is still within scope of the original intelligence requirement. If not, note it as a potential future lead but do not pursue it unless the user expands the scope.


## Common Pitfalls

These are the mistakes that derail investigations. Review this list when you feel stuck or uncertain.

**Not logging searches.**
If you do not log what you searched and what you found, you will repeat work, miss patterns, and be unable to explain your findings. Log everything, including searches that return nothing.

**Confirmation bias.**
The most dangerous failure mode in OSINT. Once you form a hypothesis, you will naturally look for evidence that confirms it and discount evidence that contradicts it. Counteract this by:
- Explicitly seeking disconfirming evidence
- Asking "what would prove this wrong?"
- Assigning confidence levels honestly
- Treating contradictions as valuable signals, not inconveniences

**Over-reliance on a single source.**
No single source is authoritative. WHOIS data can be faked. Social media profiles can be impersonated. Timestamps can be manipulated. Always seek corroboration from independent sources.

**Ignoring cached and archived data.**
The current version of a website, profile, or document may not be the most informative version. Always check:
- Wayback Machine for website history
- Google cache for recent snapshots
- Common Crawl for historical page content
- Social media archives and cached profiles

**Not considering deliberate deception.**
Information found online may be intentionally false. Disinformation, sockpuppet accounts, planted evidence — all are possibilities. Assess the reliability of each source independently.

**Scope creep.**
OSINT investigations can expand infinitely. Every finding opens new avenues. Constantly return to the intelligence requirement defined in Step 1. If a lead is interesting but out of scope, note it in `leads.md` as LOW priority and move on.

**Violating ethical boundaries under pressure.**
When an investigation is time-sensitive or the user is impatient, the temptation to cut ethical corners grows. Do not. The boundaries defined in the Ethics and OPSEC section are not flexible. If a collection method is questionable, document why you chose not to use it and propose alternatives.

**Failing to record negative results.**
"I searched for X and found nothing" is a finding. It tells future investigators not to repeat that search. It constrains the space of possibilities. It may even be the answer — sometimes the absence of a digital footprint is itself significant.

**Not using the knowledge graph.**
The knowledge graph is your external memory. If you are not adding entities and relationships as you discover them, you are relying on context window alone, which means you will lose connections in long investigations. Use `memory-graph` tools consistently.

**Treating tools as infallible.**
Every tool has limitations. Username checkers produce false positives and false negatives. WHOIS data may be outdated. Geolocation databases have error margins. Always note the tool and method used, and treat its output as one data point, not ground truth.
