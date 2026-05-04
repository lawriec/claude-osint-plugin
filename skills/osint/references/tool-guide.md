# Tool Guide Reference

Complete reference for all tools available during OSINT investigations. Organized by function.

---

## Web Search and Discovery

### tavily_search

| Field | Details |
|-------|---------|
| **What** | AI-powered web search with filtering by date, domain, and topic |
| **When** | Focused queries where you need recent, relevant results with content extraction |
| **MCP** | `tavily` server |

**Example usage:**
```
tavily_search(query="John Doe site:linkedin.com", search_depth="advanced", include_domains=["linkedin.com"], max_results=10)
```

**Key parameters:**
- `search_depth`: "basic" (fast) or "advanced" (thorough, slower)
- `include_domains` / `exclude_domains`: filter by domain
- `days`: limit to results from last N days
- `topic`: "general" or "news"

**Gotchas:**
- Advanced search is slower but significantly better for OSINT
- Domain filtering is powerful — use it to target specific platforms
- Results include extracted content, reducing need for separate fetch

### tavily_extract

| Field | Details |
|-------|---------|
| **What** | Extract clean content from one or more URLs |
| **When** | You have specific URLs and need their text content |
| **MCP** | `tavily` server |

**Example usage:**
```
tavily_extract(urls=["https://example.com/page1", "https://example.com/page2"])
```

**Gotchas:**
- Works on most standard web pages
- May fail on heavily JS-rendered pages (use selenium instead)
- Can extract from multiple URLs in one call

### tavily_crawl

| Field | Details |
|-------|---------|
| **What** | Crawl a website starting from a URL, following links |
| **When** | Mapping out a website's structure or finding all pages on a domain |
| **MCP** | `tavily` server |

**Example usage:**
```
tavily_crawl(url="https://example.com", max_depth=2, limit=50)
```

**Gotchas:**
- Set reasonable limits to avoid crawling too broadly
- Useful for discovering hidden pages or site structure

### searxng_search

| Field | Details |
|-------|---------|
| **What** | Meta-search across multiple engines (Google, Bing, Brave, DuckDuckGo, Yahoo, 250+ others) via self-hosted SearXNG |
| **When** | Broad exploration; when tavily misses results; when you want diverse sources or operator-based filters |
| **MCP** | `searxng` server (set `SEARXNG_URL`, defaults to `http://localhost:8080`) |

**Example usage:**
```
searxng_search(query="\"john.doe\" email", categories=["general"])
searxng_search(query="quarterly report", site="example.com", filetype="pdf", after="2025-01-01")
searxng_search(query="leak", inurl="paste", intitle="dump")
```

**Key parameters:**
- `categories`: array — `general`, `images`, `videos`, `news`, `music`, `files`, `social_media`, `science`, `it`, `map`
- `language`: language code (e.g., `en`, `de`) or `all`
- `time_range`: `day`, `month`, `year`
- `pageno`: page number (default 1)
- `max_results`: 1–100 (default 20)
- **Operator parameters** (passed through to engines): `site`, `filetype`, `after`, `before`, `inurl`, `intitle`
- `region`: VPN exit region (only when VPN is configured — use `searxng_vpn_regions` to list)

**Gotchas:**
- Engine selection is now automatic — no `engines` parameter; SearXNG uses all enabled engines and self-heals
- Reverse image search has been removed from this MCP — use `google-reverse-image` instead, or pass an image URL as the query to text-match where it appears
- Categories are an array, not a string
- Results may be less curated than Tavily; aggregated with engine attribution

### fetch

| Field | Details |
|-------|---------|
| **What** | Simple HTTP fetch of a URL, returns content |
| **When** | Direct URL retrieval; API calls; checking if a page exists |
| **MCP** | `fetch` server |

**Example usage:**
```
fetch(url="https://api.github.com/users/johndoe")
```

**Gotchas:**
- No JavaScript rendering — static content only
- Good for APIs and simple pages
- Use selenium for JS-heavy sites

---

## Image and Video Analysis

### gemini ask_question_about_video / ask_question_about_audio

| Field | Details |
|-------|---------|
| **What** | AI analysis of video, image, or audio files |
| **When** | Analyzing visual evidence, identifying objects/text in images, transcribing audio |
| **MCP** | `gemini` server |

**Example usage:**
```
ask_question_about_video(file_path="/path/to/image.jpg", question="What text is visible in this image? Describe all identifying features.")
```

**Gotchas:**
- Despite the name, works on images too
- Good for reading text in screenshots, identifying landmarks, describing scenes
- Provide specific questions for better results
- Use for EXIF-stripped images where metadata is unavailable

### google-reverse-image reverse_image_search

| Field | Details |
|-------|---------|
| **What** | Reverse image search via Google Cloud Vision Web Detection — the same backend that powers Google Images' reverse search UI |
| **When** | Finding pages where an image appears, exact/partial matches, visually similar images, web entities, best-guess label |
| **MCP** | `google-reverse-image` server (set `GOOGLE_VISION_API_KEY`) |

**Example usage:**
```
reverse_image_search(file_path="/path/to/photo.jpg")
reverse_image_search(image_url="https://example.com/photo.jpg", max_results=30)
```

**Key parameters:**
- `file_path` OR `image_url` (exactly one) — local image (max 7 MB) or public HTTPS URL
- `max_results`: 1–50 per result section (default 20)

**What it returns:** Pages with the image, full/partial matching images, visually similar images, web entities, best-guess label.

**Gotchas:**
- Requires a Google Cloud project with billing enabled and the Cloud Vision API enabled (free tier: 1000 calls/month)
- API key must be unrestricted by referrer (stdio MCPs send no referrer); restrict by API instead
- For UI-driven workflows (Google Lens, Yandex), use `selenium` to drive a browser instead

### video-reader (extract_frames / extract_frame_at_timestamp / generate_thumbnail_grid)

| Field | Details |
|-------|---------|
| **What** | Extract individual frames or thumbnail grids from video files |
| **When** | Analyzing video evidence frame-by-frame; creating visual summaries |
| **MCP** | `video-reader` server |

**Example usage:**
```
extract_frame_at_timestamp(input_file="/path/to/video.mp4", timestamp="00:01:30", output_file="/path/to/frame.jpg")
generate_thumbnail_grid(input_file="/path/to/video.mp4", columns=4, rows=4, output_file="/path/to/grid.jpg")
```

**Gotchas:**
- Thumbnail grids are excellent for quick video overview
- Extract specific frames when you spot something in the grid
- Combine with gemini for AI analysis of extracted frames

### selenium take_screenshot

| Field | Details |
|-------|---------|
| **What** | Capture screenshot of a web page in a real browser |
| **When** | Documenting visual evidence; capturing dynamic/JS-rendered content |
| **MCP** | `selenium` server |

**Example usage:**
```
start_browser(browser="chrome", headless=true)
navigate(url="https://example.com/profile")
take_screenshot(filename="evidence-001.png")
```

**Gotchas:**
- Must start_browser first
- Headless mode recommended for automation
- Screenshots are saved to the working directory by default
- Always document what the screenshot shows in the search log

---

## Historical Data

### internet-archive (ia_search / ia_metadata / ia_download)

| Field | Details |
|-------|---------|
| **What** | Search and access the Wayback Machine and Internet Archive collections |
| **When** | Finding deleted/changed web pages; researching historical content; verifying past claims |
| **MCP** | `internet-archive` server |

**Example usage:**
```
ia_search(query="example.com", fields="identifier,title,date", rows=20)
ia_metadata(identifier="some-archive-item-id")
ia_download(identifier="some-item", file="specific-file.html", dest_path="/path/to/save/")
```

**Gotchas:**
- `ia_search` searches Archive.org collections, not the Wayback Machine
- For Wayback Machine snapshots, use the CDX API via fetch: `https://web.archive.org/cdx/search/cdx?url=example.com&output=json`
- Metadata can reveal upload dates, original filenames, and uploader info
- Large downloads may be slow

### common-crawl (cc_search / cc_fetch)

| Field | Details |
|-------|---------|
| **What** | Search through Common Crawl's web archive (petabytes of historical web data) |
| **When** | Finding historical snapshots of pages; discovering subdomains; checking what content existed at a URL |
| **MCP** | `common-crawl` server |

**Example usage:**
```
cc_search(url="example.com/*", crawl="CC-MAIN-2024-10")
cc_fetch(url="https://example.com/page", crawl="CC-MAIN-2024-10")
```

**Gotchas:**
- Wildcard searches (`*`) find all pages under a domain
- Different crawl indexes cover different time periods
- Use `cc_list_crawls` to see available crawl indexes
- `cc_domain_summary` gives overview of a domain's presence across crawls

---

## Browser Automation

### selenium (full suite)

| Field | Details |
|-------|---------|
| **What** | Full browser automation — navigate, interact, screenshot, execute JS |
| **When** | JS-heavy sites; login-required public pages; reverse image search; complex interactions |
| **MCP** | `selenium` server |

**Core workflow:**
```
1. start_browser(browser="chrome", headless=true)
2. navigate(url="https://target-site.com")
3. take_screenshot(filename="step1.png")
4. interact(selector="#search-input", action="fill", value="search term")
5. interact(selector="#search-button", action="click")
6. take_screenshot(filename="step2-results.png")
7. close_session()
```

**Key operations:**

| Function | Purpose |
|----------|---------|
| `start_browser` | Initialize browser session |
| `navigate` | Go to URL |
| `take_screenshot` | Capture page state |
| `interact` | Click, fill, select elements |
| `execute_script` | Run JavaScript on page |
| `get_element_text` | Extract text from element |
| `get_element_attribute` | Get element attributes (href, src, etc.) |
| `send_keys` | Type text |
| `press_key` | Press keyboard keys |
| `get_cookies` / `add_cookie` | Cookie management |
| `close_session` | Clean up browser |

**OSINT-specific uses:**
- Reverse image search on Google Images or Yandex
- Capturing social media profiles before they're deleted
- Navigating paginated search results
- Interacting with maps and geolocation tools

**Gotchas:**
- Always close sessions when done
- Some sites detect headless browsers — may need non-headless mode
- Use waits/retries for slow-loading pages
- Screenshots are your evidence — take them liberally

---

## Knowledge Graph

### memory-graph (full suite)

| Field | Details |
|-------|---------|
| **What** | Create and query a knowledge graph of entities and relationships |
| **When** | Tracking people, organizations, domains, and their connections throughout an investigation |
| **MCP** | `memory-graph` server |

**Core operations:**
```
create_entities(entities=[{name: "John Doe", entityType: "Person", observations: ["Located in NYC", "Works at Acme Corp"]}])
create_relations(relations=[{from: "John Doe", to: "Acme Corp", relationType: "employed_by"}])
add_observations(observations=[{entityName: "John Doe", contents: ["Email: john@example.com"]}])
search_nodes(query="John Doe")
```

See **knowledge-graph.md** for the full entity schema and relationship types.

**Gotchas:**
- Entity names must be exact when creating relations
- Use `search_nodes` to find entities before creating duplicates
- Add observations incrementally as you discover new information
- The graph persists across the session — build it as you go

---

## Social Media

### reddit (fetch_reddit_hot_threads / fetch_reddit_post_content)

| Field | Details |
|-------|---------|
| **What** | Fetch Reddit threads and post content |
| **When** | Investigating Reddit presence; finding discussions about a subject; OSINT community research |
| **MCP** | `reddit` server |

**Example usage:**
```
fetch_reddit_hot_threads(subreddit="OSINT", limit=10)
fetch_reddit_post_content(url="https://reddit.com/r/OSINT/comments/abc123/title/")
```

**Gotchas:**
- Use for reading public Reddit content
- For user profile investigation, combine with the Reddit JSON API: `https://www.reddit.com/user/{username}/about.json`
- Check r/OSINT, r/RBI, r/TraceLabs for methodology discussions

### yt-dl (ytdlp_search_videos / ytdlp_get_video_metadata)

| Field | Details |
|-------|---------|
| **What** | Search YouTube and extract video metadata |
| **When** | Finding videos by/about a subject; extracting upload dates, descriptions, channel info |
| **MCP** | `yt-dl` server |

**Example usage:**
```
ytdlp_search_videos(query="John Doe interview", max_results=10)
ytdlp_get_video_metadata(url="https://youtube.com/watch?v=xxxxx")
```

**Additional tools:**
- `ytdlp_download_video` — download video files
- `ytdlp_download_audio` — extract audio only
- `ytdlp_download_transcript` — get video transcripts
- `ytdlp_get_video_comments` — read comments
- `ytdlp_list_subtitle_languages` — check available subtitle languages

**Gotchas:**
- Metadata includes upload date, channel ID, description, tags, view count
- Comments can contain leads (mentioned names, locations, etc.)
- Transcripts are searchable text — useful for finding mentions
- Works on many platforms beyond YouTube (Vimeo, Twitter, etc.)

---

## OSINT Scripts

Run via `uv run skills/osint/scripts/<name>`. These are purpose-built Python scripts for common OSINT tasks.

### query_dns.py

| Field | Details |
|-------|---------|
| **What** | DNS enumeration — resolve A, AAAA, MX, NS, TXT, CNAME, SOA records |
| **When** | Investigating a domain's infrastructure |
| **Usage** | `uv run skills/osint/scripts/query_dns.py example.com` |

**What it reveals:** IP addresses, mail servers, nameservers, SPF/DKIM/DMARC records, hosting provider clues.

### query_whois.py

| Field | Details |
|-------|---------|
| **What** | WHOIS lookup for domain registration details |
| **When** | Finding who registered a domain, when, and with which registrar |
| **Usage** | `uv run skills/osint/scripts/query_whois.py example.com` |

**What it reveals:** Registrant info (if not privacy-protected), registration/expiry dates, registrar, nameservers.

### query_crtsh.py

| Field | Details |
|-------|---------|
| **What** | Certificate transparency log search via crt.sh |
| **When** | Discovering subdomains; finding related domains on the same certificate |
| **Usage** | `uv run skills/osint/scripts/query_crtsh.py example.com` |

**What it reveals:** All SSL certificates ever issued for a domain, including subdomains (wildcard certs, specific subdomain certs).

### query_shodan_internetdb.py

| Field | Details |
|-------|---------|
| **What** | IP enrichment via Shodan's free InternetDB API |
| **When** | Checking what services/ports are open on an IP; finding hostnames associated with an IP |
| **Usage** | `uv run skills/osint/scripts/query_shodan_internetdb.py 1.2.3.4` |

**What it reveals:** Open ports, hostnames, tags, vulnerabilities (CVEs), CPEs. No API key required.

### extract_exif.py

| Field | Details |
|-------|---------|
| **What** | Extract EXIF/metadata from image files |
| **When** | Checking for GPS coordinates, camera info, timestamps, software used |
| **Usage** | `uv run skills/osint/scripts/extract_exif.py /path/to/image.jpg` |

**What it reveals:** GPS coordinates, camera make/model, date taken, software used to edit, thumbnail data.

**Gotchas:** Most social media platforms strip EXIF on upload. Original files (from email, direct download) are more likely to have metadata.

### check_username.py

| Field | Details |
|-------|---------|
| **What** | Check if a username exists across multiple platforms |
| **When** | Mapping someone's online presence from a known username |
| **Usage** | `uv run skills/osint/scripts/check_username.py johndoe123` |

**What it reveals:** Which platforms have accounts with that username, profile URLs.

### sun_position.py

| Field | Details |
|-------|---------|
| **What** | Calculate solar angle/position for a given location and time |
| **When** | Geolocation verification — matching shadows in photos to expected sun position |
| **Usage** | `uv run skills/osint/scripts/sun_position.py --lat 40.7128 --lon -74.0060 --date 2024-06-15 --time 14:30` |

**What it reveals:** Sun azimuth and elevation, useful for verifying when/where a photo was taken based on shadow analysis.

### analyze_email_headers.py

| Field | Details |
|-------|---------|
| **What** | Parse and analyze email headers |
| **When** | Tracing the origin of an email; identifying spoofing; verifying sender |
| **Usage** | `uv run skills/osint/scripts/analyze_email_headers.py /path/to/headers.txt` |

**What it reveals:** Sending server IPs, relay path, SPF/DKIM verification results, timestamps, originating client.

### query_blockchain.py

| Field | Details |
|-------|---------|
| **What** | Look up cryptocurrency address information |
| **When** | Investigating crypto wallets; tracking transactions |
| **Usage** | `uv run skills/osint/scripts/query_blockchain.py <address>` |

**What it reveals:** Balance, transaction count, first/last seen dates.

### discover_reddit_threads.py

| Field | Details |
|-------|---------|
| **What** | Discover relevant Reddit threads across OSINT-related subreddits |
| **When** | Finding community discussions, techniques, or prior investigations related to your case |
| **Usage** | `uv run skills/osint/scripts/discover_reddit_threads.py "search term"` |

**What it reveals:** Relevant threads from OSINT-focused subreddits.

### query_flightradar.py

| Field | Details |
|-------|---------|
| **What** | Aircraft tracking via the OpenSky Network API |
| **When** | Identifying aircraft by registration/callsign, tracking flights, analyzing airport traffic |
| **Usage** | `uv run skills/osint/scripts/query_flightradar.py aircraft N12345` or `flights --bbox 45,5,55,15` or `airport EGLL departures` |

**What it reveals:** Live aircraft positions, flight paths, airport arrivals/departures, aircraft metadata. Free, no API key required.

### query_ais.py

| Field | Details |
|-------|---------|
| **What** | Vessel/ship tracking via Fintraffic AIS API |
| **When** | Identifying vessels in the Baltic Sea, tracking ship movements |
| **Usage** | `uv run skills/osint/scripts/query_ais.py vessels --mmsi 123456789` or `vessels --name "SHIP NAME"` |

**What it reveals:** Vessel position, speed, heading, destination, ship type, MMSI/IMO identifiers. Coverage limited to Baltic Sea region.

### query_urlscan.py

| Field | Details |
|-------|---------|
| **What** | URLScan.io domain and IP intelligence |
| **When** | Threat assessment of suspicious URLs/domains; checking if a site has been flagged |
| **Usage** | `uv run skills/osint/scripts/query_urlscan.py search "domain:example.com"` or `result <uuid>` |

**What it reveals:** Prior scan results, verdicts, page content, redirects, screenshots, hosting infrastructure. Free for searches (no API key needed).

### query_ipinfo.py

| Field | Details |
|-------|---------|
| **What** | IP geolocation and ASN lookup via ip-api.com |
| **When** | Geolocating IPs, identifying hosting providers, detecting proxies/VPNs |
| **Usage** | `uv run skills/osint/scripts/query_ipinfo.py geo 8.8.8.8` or `asn 8.8.8.8` or `batch 1.1.1.1 8.8.8.8` |

**What it reveals:** Country, city, ISP, organization, ASN, reverse DNS, hosting/proxy/mobile flags. Supports batch lookups (up to 100 IPs).

### query_virustotal.py

| Field | Details |
|-------|---------|
| **What** | VirusTotal v3 API for threat intelligence |
| **When** | Checking domain/IP/URL/file reputation; malware analysis |
| **Usage** | `uv run skills/osint/scripts/query_virustotal.py domain example.com` or `ip 1.2.3.4` or `url https://...` or `hash <sha256>` |
| **Auth** | Requires `VT_API_KEY` environment variable (free tier: 4 requests/min) |

**What it reveals:** Detection stats (malicious/suspicious/clean), WHOIS data, DNS records, community reputation, file analysis results.

### query_wikidata_sparql.py

| Field | Details |
|-------|---------|
| **What** | Wikidata entity search and SPARQL queries |
| **When** | Entity resolution — identifying people, organizations, places; enriching knowledge graphs |
| **Usage** | `uv run skills/osint/scripts/query_wikidata_sparql.py entity "Angela Merkel"` or `properties Q567` or `related Q567` |

**What it reveals:** Wikidata QIDs, descriptions, aliases, structured properties (birth date, nationality, employer, education), related entities.

### query_archive_today.py

| Field | Details |
|-------|---------|
| **What** | archive.today snapshot search and retrieval |
| **When** | Finding preserved copies of web pages; complementing Wayback Machine with archive.today |
| **Usage** | `uv run skills/osint/scripts/query_archive_today.py search https://example.com` or `newest https://...` or `oldest https://...` |

**What it reveals:** Snapshot URLs, timestamps, and original URLs from archive.today/archive.ph.

### query_censys.py

| Field | Details |
|-------|---------|
| **What** | Censys Search API for host intelligence |
| **When** | Enriching IP data beyond Shodan InternetDB; searching for hosts by services, location, or software |
| **Usage** | `uv run skills/osint/scripts/query_censys.py host 8.8.8.8` or `search "services.service_name: HTTP"` |
| **Auth** | Requires `CENSYS_API_ID` and `CENSYS_API_SECRET` environment variables (free: 250 queries/month at censys.io) |

**What it reveals:** Services (port, protocol, software), location (country, city, coordinates), autonomous system (ASN, organization), operating system, DNS records.

### image_ela.py

| Field | Details |
|-------|---------|
| **What** | Error Level Analysis for detecting image manipulation |
| **When** | Checking if an image has been edited; forensic analysis of photos |
| **Usage** | `uv run skills/osint/scripts/image_ela.py analyze photo.jpg` or `compare img1.jpg img2.jpg` or `metadata photo.jpg` |

**What it reveals:** ELA visualization (saved as PNG), error statistics (mean, max, std dev per channel), manipulation assessment. High-error patches indicate areas that were edited at a different compression level than the surrounding image.

**Gotchas:** ELA works best on JPEG images. PNGs and other lossless formats will show uniform error levels. Multiple re-saves degrade ELA accuracy.

---

## Tool Selection Quick Reference

| I need to... | Use this |
|--------------|----------|
| Search the web broadly | `searxng_search` |
| Search the web with filters | `tavily_search` |
| Get content from a URL | `tavily_extract` or `fetch` |
| Map a website's pages | `tavily_crawl` |
| Find deleted web pages | `internet-archive` or `common-crawl` |
| Look up DNS records | `query_dns.py` |
| Find subdomains | `query_crtsh.py` |
| Check domain registration | `query_whois.py` |
| Scan an IP address | `query_shodan_internetdb.py` |
| Check a username across platforms | `check_username.py` |
| Extract image metadata | `extract_exif.py` |
| Analyze email headers | `analyze_email_headers.py` |
| Look up a crypto wallet | `query_blockchain.py` |
| Analyze an image with AI | `gemini ask_question_about_video` |
| Reverse image search | `google-reverse-image reverse_image_search` |
| Extract video frames | `video-reader extract_frames` |
| Screenshot a web page | `selenium take_screenshot` |
| Interact with JS-heavy sites | `selenium` (full workflow) |
| Track entities and connections | `memory-graph` |
| Search YouTube | `ytdlp_search_videos` |
| Read Reddit threads | `reddit fetch_reddit_post_content` |
| Verify sun position in photo | `sun_position.py` |
| Track aircraft/flights | `query_flightradar.py` |
| Track ships/vessels | `query_ais.py` |
| Scan a URL for threats | `query_urlscan.py` |
| Geolocate an IP address | `query_ipinfo.py` |
| Check domain/file reputation | `query_virustotal.py` |
| Resolve entities (people/orgs) | `query_wikidata_sparql.py` |
| Find archived web pages | `query_archive_today.py` |
| Scan host with Censys | `query_censys.py` |
| Detect image manipulation | `image_ela.py` |
