# TODO — OSINT Plugin Backlog

## Ready to Build

Items fully specified and ready to implement. Pick from here when working on features.

### References
| Priority | Item | Type | Domain | Description |
|----------|------|------|--------|-------------|
| MEDIUM | crypto-financial.md | reference | Crypto | Blockchain explorers, wallet clustering, DeFi tracing, mixer detection |
| MEDIUM | radio-signals.md | reference | Radio | SDR basics, amateur radio callsign lookup, broadcast identification |
| LOW | dark-web-research.md | reference | Dark web | Ahmia, onion scanning, .onion research ethics and legal boundaries |

### Scripts
| Priority | Item | Type | Description |
|----------|------|------|-------------|
| MEDIUM | query_virustotal.py | script | VirusTotal free API (needs free key, 4 req/min) |
| LOW | query_wikidata_sparql.py | script | Wikidata SPARQL queries for entity resolution |
| LOW | query_archive_today.py | script | archive.today snapshot search and retrieval |

### Challenges
| Priority | Item | Type | Description |
|----------|------|------|-------------|
| MEDIUM | challenges/multi-domain/05-github-forensics.md | challenge | Investigate a GitHub user via commits, emails, linked repos |
| MEDIUM | challenges/geolocation/08-ip-camera-discovery.md | challenge | Identify location from IP camera stream clues (Shodan + geolocation) |
| MEDIUM | challenges/corporate/02-executive-verification.md | challenge | Verify executive claims via LinkedIn, registries, filings |
| LOW | challenges/verification/05-deepfake-detection.md | challenge | Identify manipulated/AI-generated media via forensic analysis |

### MCP Server
| Priority | Item | Type | Description |
|----------|------|------|-------------|
| HIGH | mcp-osint-recon | MCP | Consolidate scripts into TypeScript MCP with caching and rate limiting |

## Needs Research

Items that need investigation before implementation.

| Item | Question |
|------|----------|
| Shodan full API MCP | Is there an existing MCP? What's the free tier? Worth building vs. using InternetDB? |
| VirusTotal MCP | Multiple endpoints (URL scan, file scan, domain). Is the free tier useful enough? |
| Censys MCP | Internet-wide scanning data. Free tier research needed. |
| Image ELA tool | Best approach for Error Level Analysis? Python library or external tool? |
| Maltego-style transforms | Can we build entity expansion as an MCP? What's the architecture? |
| Face recognition ethics | PimEyes and similar tools — should we include guidance? Legal issues? |
| SearXNG alternatives | Self-hosted vs. public instances. Docker setup documentation needed? |

## Blocked

Items waiting on external dependencies.

| Item | Blocker |
|------|---------|
| TMDB MCP | Needs free API key (1 week approval process) |
| Shodan full API | Needs paid API key for full search |
| Discord server reading | Needs bot token or user cookie — ethical and TOS concerns |
| Twitter/X API | No free read API. Workarounds exist but are fragile. |

## Completed

Items that have been implemented.

| Item | Date | PR |
|------|------|----|
| Core skill (SKILL.md) | 2026-04-09 | Initial commit |
| 7 core reference guides | 2026-04-09 | Initial commit |
| 5 domain reference guides | 2026-04-09 | Initial commit |
| 10 Python scripts | 2026-04-09 | Initial commit |
| 10 OSINT challenges | 2026-04-09 | Initial commit |
| Investigation templates | 2026-04-09 | Initial commit |
| GitHub workflows (5) | 2026-04-09 | Initial commit |
| Docker setup | 2026-04-09 | Initial commit |
| Test suite | 2026-04-09 | Initial commit |
| query_flightradar.py (OpenSky) | 2026-04-09 | Feature batch |
| query_ais.py (Fintraffic AIS) | 2026-04-09 | Feature batch |
| query_urlscan.py (URLScan.io) | 2026-04-09 | Feature batch |
| query_ipinfo.py (ip-api.com) | 2026-04-09 | Feature batch |
| document-analysis.md reference | 2026-04-09 | Feature batch |
| vehicle-object-id.md reference | 2026-04-09 | Feature batch |
| google-dorking-cheatsheet.md | 2026-04-09 | Feature batch |
| geolocation/04-vegetation-clues | 2026-04-09 | Feature batch |
| infrastructure/03-phishing-detection | 2026-04-09 | Feature batch |
| multi-domain/03-ctf-style | 2026-04-09 | Feature batch |
| infrastructure/04-email-header-forensics | 2026-04-09 | Challenge expansion |
| infrastructure/05-ip-attribution | 2026-04-09 | Challenge expansion |
| image-forensics/03-social-media-metadata | 2026-04-09 | Challenge expansion |
| people/03-reddit-community-analysis | 2026-04-09 | Challenge expansion |
| geolocation/05-flight-path-identification | 2026-04-09 | Challenge expansion |
| transportation/01-vessel-identification | 2026-04-09 | Challenge expansion |
| transportation/02-airport-traffic-analysis | 2026-04-09 | Challenge expansion |
| crypto/01-wallet-tracing | 2026-04-09 | Challenge expansion |
| verification/01-historical-website-analysis | 2026-04-09 | Challenge expansion |
| verification/02-threat-intel-domain-scan | 2026-04-09 | Challenge expansion |
| image-forensics/04-reverse-image-search | 2026-04-09 | Challenge expansion v2 |
| infrastructure/06-google-dorking-practical | 2026-04-09 | Challenge expansion v2 |
| verification/03-wayback-timeline | 2026-04-09 | Challenge expansion v2 |
| verification/04-fact-check-viral-claim | 2026-04-09 | Challenge expansion v2 |
| corporate/01-company-investigation | 2026-04-09 | Challenge expansion v2 |
| multi-domain/04-video-intelligence | 2026-04-09 | Challenge expansion v2 |
| geolocation/06-common-crawl-historical | 2026-04-09 | Challenge expansion v2 |
| geolocation/07-basic-whois-geolocation | 2026-04-09 | Challenge expansion v2 |
| people/04-basic-social-footprint | 2026-04-09 | Challenge expansion v2 |
| people/05-behavioral-pattern-analysis | 2026-04-09 | Challenge expansion v2 |
