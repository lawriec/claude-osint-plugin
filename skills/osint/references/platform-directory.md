# Platform Directory Reference

Comprehensive directory of OSINT platforms organized by domain. For each platform: what it does, URL, authentication requirements, and when to use it.

---

## Search Engines

| Platform | URL | Auth | What It Does | When to Use |
|----------|-----|------|-------------|-------------|
| **Google** | google.com | None | Web search with advanced operators (dorking) | Primary search; use operators for precision |
| **Bing** | bing.com | None | Web search; sometimes indexes pages Google misses | Secondary search; different index |
| **Yandex** | yandex.com | None | Russian search engine; excellent image search | Targets in Russia/CIS; reverse image search |
| **Baidu** | baidu.com | None | Chinese search engine | Targets in China; Chinese-language content |
| **DuckDuckGo** | duckduckgo.com | None | Privacy-focused search; bangs for other engines | Quick searches; when you want to avoid personalization |

### Google Dorking Quick Reference

| Operator | Function | Example |
|----------|----------|---------|
| `site:` | Search within a domain | `site:linkedin.com "John Doe"` |
| `filetype:` | Find specific file types | `filetype:pdf "company name"` |
| `intitle:` | Search in page titles | `intitle:"index of" site:example.com` |
| `inurl:` | Search in URLs | `inurl:admin site:example.com` |
| `intext:` | Search in page body | `intext:"@example.com"` |
| `cache:` | Google's cached version | `cache:example.com` |
| `"exact phrase"` | Exact match | `"john.doe@example.com"` |
| `before:` / `after:` | Date range | `"John Doe" after:2023-01-01 before:2024-01-01` |
| `-` | Exclude term | `"John Doe" -facebook -linkedin` |
| `OR` | Either term | `"John Doe" OR "J. Doe"` |
| `*` | Wildcard | `"John * Doe"` |

---

## People Search

| Platform | URL | Auth | What It Does | When to Use |
|----------|-----|------|-------------|-------------|
| **Pipl** | pipl.com | Paid API | Cross-reference people data from multiple sources | Comprehensive identity resolution (commercial) |
| **Spokeo** | spokeo.com | Paid | Aggregates public records, social profiles, contact info | US people search; phone/email/name lookup |
| **WhitePages** | whitepages.com | Freemium | Phone, address, and people lookup | US phone number and address lookup |
| **ThatsThem** | thatsthem.com | Free (limited) | People search by name, email, phone, address | Quick free lookup for US individuals |
| **TruePeopleSearch** | truepeoplesearch.com | Free | Name, address, phone lookup from public records | Free alternative to paid people search (US only) |
| **FamilyTreeNow** | familytreenow.com | Free | Public records and genealogy data | Finding relatives and historical addresses |
| **Social Searcher** | social-searcher.com | Freemium | Real-time social media search | Monitoring mentions across social platforms |

**Note:** People search engines are primarily US-focused. For other countries, search for country-specific public records databases.

---

## Username Enumeration

| Platform | URL | Auth | What It Does | When to Use |
|----------|-----|------|-------------|-------------|
| **Sherlock** | github.com/sherlock-project/sherlock | None (CLI) | Check username across 400+ sites | Starting point for username enumeration |
| **Maigret** | github.com/soxoj/maigret | None (CLI) | Username search across 2500+ sites; richer than Sherlock | Deep username search with profile parsing |
| **WhatsMyName** | whatsmyname.app | None | Web-based username search | Quick browser-based username check |
| **Namechk** | namechk.com | None | Check username/domain availability | Quick availability check across platforms |
| **InstantUsername** | instantusername.com | None | Real-time username availability | Fast browser-based check |

**Strategy:** Start with the `check_username.py` script, then use Sherlock/Maigret for deeper coverage. Verify hits manually since false positives are common.

---

## Social Media

### Major Platforms

| Platform | URL | OSINT Approach | Key Data Points |
|----------|-----|---------------|-----------------|
| **Facebook** | facebook.com | Graph search is deprecated; use Google dorking: `site:facebook.com "name"` | Friends, check-ins, likes, groups, photos, life events |
| **Twitter/X** | x.com | Advanced search: `x.com/search-advanced` | Tweets, followers, following, lists, tweet timestamps (timezone clues) |
| **Instagram** | instagram.com | Limited without login; use Google cache or third-party viewers | Photos, stories (ephemeral), followers, tagged locations, hashtags |
| **LinkedIn** | linkedin.com | Google dorking: `site:linkedin.com/in/ "name"` | Employment history, education, skills, connections, recommendations |
| **TikTok** | tiktok.com | Public profiles viewable without login | Videos, sounds used, liked videos (if public), bio links |
| **Reddit** | reddit.com | `/user/{name}/about.json`; comment history reveals interests/location | Comment history, subreddit activity, posting patterns, writing style |

### Twitter/X Advanced Search Operators

| Operator | Example |
|----------|---------|
| `from:username` | Tweets from a specific user |
| `to:username` | Replies to a specific user |
| `since:YYYY-MM-DD until:YYYY-MM-DD` | Date range |
| `geocode:lat,lon,radius` | Tweets from a location |
| `filter:images` / `filter:videos` | Media type |
| `min_retweets:N` / `min_faves:N` | Engagement threshold |
| `-filter:retweets` | Exclude retweets |

---

## Image Analysis

| Platform | URL | Auth | What It Does | When to Use |
|----------|-----|------|-------------|-------------|
| **Google Lens** | lens.google.com | None | Reverse image search, object/text recognition | General reverse image search; identifying objects and locations |
| **Yandex Images** | yandex.com/images | None | Reverse image search (often finds results Google misses) | Best for finding faces and matching people photos |
| **TinEye** | tineye.com | None (limited) | Reverse image search focused on finding exact/modified copies | Finding where an image has been published; tracking modifications |
| **SauceNAO** | saucenao.com | None | Reverse image search focused on anime/illustration sources | Finding original source of illustrations and artwork |
| **PimEyes** | pimeyes.com | Paid | Face recognition search engine | Finding where a person's face appears online (use ethically) |
| **FotoForensics** | fotoforensics.com | None | Error Level Analysis (ELA) for detecting image manipulation | Checking if a photo has been edited or manipulated |
| **InVID/WeVerify** | weverify.eu | None | Video/image verification toolkit (browser extension) | Verifying authenticity of images and videos |

**Reverse image search strategy:**
1. Try Google Lens first (broadest index)
2. Try Yandex Images (often finds different results, especially faces)
3. Use TinEye to find exact copies and track image spread
4. Use selenium to automate reverse image search if needed

---

## Domain and IP Intelligence

| Platform | URL | Auth | What It Does | When to Use |
|----------|-----|------|-------------|-------------|
| **Shodan** | shodan.io | Free account + paid for full | Internet-wide scanner; shows open ports, services, banners | Investigating exposed services, IoT devices, infrastructure mapping |
| **Censys** | search.censys.io | Free account | Internet-wide scanner; certificate and host data | Certificate analysis, host discovery, TLS configuration |
| **ZoomEye** | zoomeye.org | Free account | Chinese internet scanner (like Shodan) | Alternative to Shodan; may have different scan results |
| **GreyNoise** | greynoise.io | Free tier | Identifies IPs scanning the internet (noise vs. targeted) | Determining if an IP is a scanner, bot, or benign |
| **Netcraft** | netcraft.com | Free (limited) | Website technology profiling, risk ratings | Identifying web technologies, hosting history, site reputation |
| **DomainTools** | domaintools.com | Paid (some free) | Historical WHOIS, domain profiles, reverse WHOIS | Deep domain investigation, ownership history (commercial) |
| **SecurityTrails** | securitytrails.com | Free tier | Historical DNS, WHOIS, subdomains | DNS history, subdomain enumeration, IP history |
| **DNSDumpster** | dnsdumpster.com | None | DNS reconnaissance and subdomain discovery | Quick visual DNS map of a domain |
| **ViewDNS.info** | viewdns.info | None | Multiple DNS tools (reverse IP, WHOIS history, etc.) | Quick DNS lookups, reverse IP (find other sites on same IP) |
| **BGPView** | bgpview.io | None | BGP/ASN lookups, IP prefix information | Understanding network ownership and routing |

---

## Email Intelligence

| Platform | URL | Auth | What It Does | When to Use |
|----------|-----|------|-------------|-------------|
| **Hunter.io** | hunter.io | Free tier (25/month) | Find email addresses associated with a domain | Discovering corporate email patterns |
| **Holehe** | github.com/megadose/holehe | None (CLI) | Check which services an email is registered on | Mapping accounts linked to an email |
| **theHarvester** | github.com/laramies/theHarvester | None (CLI) | Gather emails, subdomains, IPs from public sources | Broad reconnaissance on a domain |
| **EmailRep** | emailrep.io | Free tier | Email reputation and activity scoring | Quick check on whether an email is suspicious |
| **Epieos** | epieos.com | Free | Find Google account info, linked services from email | Discovering accounts linked to a Gmail address |

**Email investigation workflow:**
1. Verify the email exists (Hunter.io or SMTP check)
2. Check Gravatar for linked profile
3. Use Holehe to find registered services
4. Search breach databases (HIBP) for associated accounts
5. Google dork: `"email@example.com"` for public mentions

---

## Geolocation Tools

| Platform | URL | Auth | What It Does | When to Use |
|----------|-----|------|-------------|-------------|
| **Google Earth Pro** | earth.google.com | Free | 3D satellite imagery, historical imagery, measurement tools | Verifying locations in photos; historical satellite comparison |
| **SunCalc** | suncalc.org | None | Calculate sun position for any place/time | Verifying photo timestamps via shadow analysis |
| **GeoTips** | geotips.net | None | Country-specific clues for geolocation (language, infrastructure) | Identifying countries from environmental clues in photos |
| **Plonkit** | plonkit.net | None | GeoGuessr-style clue reference for geolocation | Quick reference for road markings, signs, vegetation by country |
| **Overpass Turbo** | overpass-turbo.eu | None | Query OpenStreetMap data visually | Finding specific features near a location (bridges, towers, etc.) |
| **Google Street View** | maps.google.com | None | Ground-level imagery | Verifying locations; comparing photo angles |
| **Sentinel Hub** | sentinel-hub.com | Free tier | Satellite imagery from Sentinel missions | Recent satellite imagery; environmental monitoring |
| **Mapillary** | mapillary.com | None | Crowdsourced street-level imagery | Street view alternatives, especially outside Google coverage |
| **F4map** | f4map.com | None | 3D OpenStreetMap rendering | Understanding building heights and urban layout |

---

## Archives and Historical Data

| Platform | URL | Auth | What It Does | When to Use |
|----------|-----|------|-------------|-------------|
| **Wayback Machine** | web.archive.org | None | Historical snapshots of web pages since 1996 | Finding deleted content, tracking website changes over time |
| **archive.today** | archive.today (also archive.ph, archive.is) | None | On-demand web page archiving; `uv run query_archive_today.py search <url>` | Preserving current page state; accessing cached copies |
| **Google Cache** | `cache:URL` in Google | None | Google's most recent cached copy of a page | Quick check of recent page state; recently deleted content |
| **Common Crawl** | commoncrawl.org | None | Massive web crawl archive (petabytes) | Large-scale historical analysis; finding pages not in Wayback |
| **CachedView** | cachedview.nl | None | Aggregator for multiple cache sources | One-stop shop for finding cached versions |

---

## Document and Metadata Analysis

| Platform | URL | Auth | What It Does | When to Use |
|----------|-----|------|-------------|-------------|
| **ExifTool** | exiftool.org | None (CLI) | Extract metadata from images, documents, videos | Checking GPS, camera info, author, timestamps in files |
| **FOCA** | github.com/ElevenPaths/FOCA | None (Windows) | Extract metadata from documents found on a domain | Bulk document metadata extraction for a target organization |
| **Metagoofil** | github.com/laramies/metagoofil | None (CLI) | Find and download public documents from a domain, extract metadata | Discovering employee names, software, paths from public docs |
| **PDF Examiner** | pdfexaminer.com | None | Analyze PDF files for hidden data and malware | Examining suspicious PDFs |
| **Jeffrey's Exif Viewer** | exif.regex.info | None | Online EXIF viewer for images | Quick online EXIF check without installing tools |

---

## Cryptocurrency

| Platform | URL | Auth | What It Does | When to Use |
|----------|-----|------|-------------|-------------|
| **Blockchain.com** | blockchain.com/explorer | None | Bitcoin blockchain explorer | Investigating Bitcoin transactions and addresses |
| **Etherscan** | etherscan.io | Free account | Ethereum blockchain explorer | Investigating Ethereum transactions, tokens, contracts |
| **OXT.me** | oxt.me | None | Advanced Bitcoin analysis with transaction graphs | Tracing Bitcoin transaction flows and clustering |
| **Blockchair** | blockchair.com | None | Multi-chain explorer (BTC, ETH, and many others) | Investigating addresses across multiple blockchains |
| **Chainalysis** | chainalysis.com | Commercial | Enterprise blockchain analysis with entity attribution | Professional investigations (law enforcement, compliance) |
| **Ethplorer** | ethplorer.io | Free API | Ethereum token transfers and holdings | Tracking ERC-20 token movements |

---

## Aviation

| Platform | URL | Auth | What It Does | When to Use |
|----------|-----|------|-------------|-------------|
| **FlightRadar24** | flightradar24.com | Freemium | Real-time flight tracking worldwide | Tracking aircraft movements; identifying flights |
| **ADS-B Exchange** | adsbexchange.com | None | Unfiltered ADS-B flight tracking (no military/VIP censorship) | Tracking flights that are hidden on other platforms |
| **FlightAware** | flightaware.com | Freemium | Flight tracking with detailed route and delay info | US-focused flight tracking; historical flight data |
| **OpenSky Network** | opensky-network.org | Free account | Open ADS-B data with research API | Bulk historical flight data; academic research |
| **Planespotters.net** | planespotters.net | None | Aircraft registration and photo database | Identifying aircraft by registration number |

---

## Maritime

| Platform | URL | Auth | What It Does | When to Use |
|----------|-----|------|-------------|-------------|
| **MarineTraffic** | marinetraffic.com | Freemium | Real-time ship tracking via AIS data | Tracking vessel movements worldwide |
| **VesselFinder** | vesselfinder.com | Freemium | Ship tracking with port and route information | Alternative to MarineTraffic |
| **MyShipTracking** | myshiptracking.com | Free | Basic ship tracking | Quick vessel lookup |
| **Equasis** | equasis.org | Free account | Ship safety and inspection records | Vessel ownership, flag state, inspection history |

---

## Maps and Satellite Imagery

| Platform | URL | Auth | What It Does | When to Use |
|----------|-----|------|-------------|-------------|
| **Google Earth** | earth.google.com | None | Satellite imagery with historical timeline | Location verification; historical comparison |
| **Sentinel Hub** | sentinel-hub.com | Free tier | Copernicus satellite data (Sentinel-1/2/3) | Environmental monitoring; recent satellite imagery |
| **Maxar** | maxar.com | Commercial | High-resolution commercial satellite imagery | Detailed analysis when Google Earth isn't enough |
| **Planet Labs** | planet.com | Commercial | Daily satellite imagery of the entire earth | Monitoring changes over time at high frequency |
| **Zoom Earth** | zoom.earth | None | Near-real-time satellite imagery and weather | Quick satellite view with recent imagery |
| **Wikimapia** | wikimapia.org | None | User-annotated satellite imagery | Identifying unmarked buildings and features |

---

## Dark Web

| Platform | URL | Auth | What It Does | When to Use |
|----------|-----|------|-------------|-------------|
| **Ahmia** | ahmia.fi | None | Search engine for .onion sites (clearnet accessible) | Searching for mentions on Tor hidden services without needing Tor |
| **OnionScan** | github.com/s-rah/onionscan | None (CLI) | Analyze .onion sites for security misconfigurations | Investigating hidden service infrastructure (requires Tor) |
| **Dark.fail** | dark.fail | None | Verified .onion links directory | Finding current addresses for known hidden services |
| **IntelX** | intelx.io | Freemium | Search engine indexing Tor, I2P, paste sites, and data leaks | Searching across dark web, paste sites, and public data leaks |

**Important:** Do not link to or visit .onion sites directly without Tor. Dark web research requires additional OPSEC measures (see opsec-ethics.md). Exercise extreme caution and ensure legal compliance.

---

## Breach Data and Credential Exposure

| Platform | URL | Auth | What It Does | When to Use |
|----------|-----|------|-------------|-------------|
| **HaveIBeenPwned** | haveibeenpwned.com | API key (paid) | Check if email/phone appears in known breaches | First check for any email investigation |
| **DeHashed** | dehashed.com | Paid | Search breach databases by email, username, IP, name, etc. | Deep credential exposure research |
| **LeakCheck** | leakcheck.io | Paid | Search leaked credentials databases | Alternative to DeHashed |
| **IntelX** | intelx.io | Freemium | Searches paste sites, breach compilations, dark web | Broad exposure check |
| **Snusbase** | snusbase.com | Paid | Breach database search | Alternative breach search |

**Legal awareness:** The legality of accessing, possessing, or using breach data varies significantly by jurisdiction. In many places, merely accessing breach databases (beyond HIBP) may be legally questionable. Always:
- Use HIBP as your primary breach check (legal and ethical)
- Do not download or possess raw breach databases
- Never use breached credentials for any purpose
- Document your methodology in case it is questioned
- Consult legal guidance if your investigation requires deeper breach analysis

---

## Miscellaneous OSINT Platforms

| Platform | URL | Auth | What It Does | When to Use |
|----------|-----|------|-------------|-------------|
| **Maltego** | maltego.com | Free CE edition | Visual link analysis and OSINT data fusion | Complex investigations with many entity relationships |
| **SpiderFoot** | spiderfoot.net | Free (self-hosted) | Automated OSINT reconnaissance | Automated broad reconnaissance on a target |
| **Recon-ng** | github.com/lanmaster53/recon-ng | None (CLI) | Modular web reconnaissance framework | Scripted, repeatable reconnaissance workflows |
| **OSINT Framework** | osintframework.com | None | Directory of OSINT tools organized by data type | Finding the right tool for a specific data type |
| **IntelTechniques** | inteltechniques.com | None | OSINT tools, techniques, and training by Michael Bazzell | Learning OSINT methodology; custom search tools |
| **Bellingcat Toolkit** | bellingcat.gitbook.io/toolkit | None | Curated OSINT tool collection from Bellingcat | Finding verified, tested OSINT tools |
| **Hunchly** | hunchly.com | Paid | Automatic web page capture during investigations | Preserving evidence while browsing (browser extension) |
| **Wayback Machine Downloader** | github.com/hartator/wayback-machine-downloader | None (CLI) | Bulk download all Wayback Machine snapshots of a site | Downloading entire archived websites |
| **Wikidata** | wikidata.org | None | Structured knowledge base for entity resolution; `uv run query_wikidata_sparql.py entity <name>` | Identifying people, orgs, places; enriching knowledge graphs |
| **VirusTotal** | virustotal.com | Free API key | Domain/IP/URL/file reputation; `uv run query_virustotal.py domain <domain>` | Threat intelligence; checking if domains/files are flagged |

---

## Platform Selection Guide

| I need to investigate... | Start with these platforms |
|--------------------------|---------------------------|
| A person (name only) | Google dorking, TruePeopleSearch, social media search |
| A person (email known) | HIBP, Gravatar, Holehe, Epieos, Google `"email"` |
| A person (username known) | check_username.py, Sherlock/Maigret, WhatsMyName |
| A person (phone known) | TruePeopleSearch, Spokeo, reverse phone lookup |
| A domain | WHOIS, DNS, crt.sh, SecurityTrails, Shodan, Wayback |
| An IP address | Shodan InternetDB, ip-api, AbuseIPDB, VirusTotal |
| An image | Google Lens, Yandex Images, TinEye, ExifTool |
| A location | Google Earth, Overpass Turbo, SunCalc, GeoTips |
| A company | OpenCorporates, LinkedIn, Google dorking, FOCA |
| A crypto wallet | Blockchain.com, Etherscan, OXT.me, Blockchair |
| An aircraft | FlightRadar24, ADS-B Exchange, Planespotters |
| A vessel | MarineTraffic, VesselFinder, Equasis |
| Deleted web content | Wayback Machine, archive.today, Google Cache, Common Crawl |
| Breach exposure | HIBP, then DeHashed/LeakCheck if needed (legal awareness) |
