# TODO — OSINT Plugin Backlog

## Ready to Build

Items fully specified and ready to implement. Pick from here when working on features.

### References

_No references currently in backlog._

### Scripts

| Priority | Item | Type | Description |
|----------|------|------|-------------|
| HIGH | analyze_image_forensics.py | script | Pillow-based ELA + image enhancement (contrast/saturation/histogram equalization) for Gemini interpretation. See [#1](https://github.com/lawriec/claude-osint-plugin/issues/1) |
| HIGH | detect_steganography.py | script | LSB detection (stego-lsb), embedded file scanning (binwalk3), strings extraction, EOF analysis. See [#1](https://github.com/lawriec/claude-osint-plugin/issues/1) |
| MEDIUM | analyze_enf.py | script | Electrical Network Frequency extraction (scipy + adaptive Goertzel), match against power-grid-frequency.org / UK NESO. See [#1](https://github.com/lawriec/claude-osint-plugin/issues/1) |
| MEDIUM | analyze_pdf_forensics.py | script | PDF keyword scanning (pdfid-style): JavaScript, /OpenAction, embedded files, redaction failures. See [#1](https://github.com/lawriec/claude-osint-plugin/issues/1) |
| MEDIUM | analyze_office_forensics.py | script | MS Office/OLE2 analysis via oletools: VBA macros (olevba), threat detection (oleid), embedded objects (oleobj). See [#1](https://github.com/lawriec/claude-osint-plugin/issues/1) |

### Challenges

_No challenges currently in backlog._

### MCP Server
| Priority | Item | Type | Description |
|----------|------|------|-------------|
| HIGH | mcp-osint-recon | MCP | Consolidate scripts into TypeScript MCP with caching and rate limiting |

## Needs Research

Items that need investigation before implementation.

| Item | Question | Status |
|------|----------|--------|
| Shodan full API MCP | InternetDB covers most needs (free, no key). Full Shodan API needs paid key ($59/mo). Community MCP exists but untested. | Resolved — InternetDB sufficient; move full API to Blocked |
| Censys MCP | Free tier: 250 queries/month, limited to search. Worth a script similar to query_shodan_internetdb.py. | Promotable — write query_censys.py |
| Image ELA tool | Pillow can do ELA (compare JPEG recompression). FotoForensics.com is the reference. Script feasible ~100 lines. | Promotable — write image_ela.py |
| Maltego-style transforms | Our memory-graph MCP + query_wikidata_sparql.py now cover entity expansion. Full Maltego architecture is overkill. | Resolved — covered by existing tools |
| Face recognition ethics | PimEyes is legal in most jurisdictions but ethically fraught. Add guidance note to opsec-ethics.md, don't build tools. | Resolved — add ethics note only |
| SearXNG | Already configured as MCP server in .mcp.json (Docker instance at localhost:8888). Works. | Resolved — already operational |

## Blocked

Items waiting on external dependencies.

| Item | Blocker |
|------|---------|
| TMDB MCP | Needs free API key (1 week approval process) |
| Shodan full API | Needs paid API key ($59/mo) for full search; InternetDB covers most use cases |
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
| osint-landscape.md reference | 2026-04-09 | OSINT landscape guide |
| crypto-financial.md reference | 2026-04-09 | Feature batch 2 |
| radio-signals.md reference | 2026-04-09 | Feature batch 2 |
| dark-web-research.md reference | 2026-04-09 | Feature batch 2 |
| query_virustotal.py | 2026-04-09 | Feature batch 2 |
| query_wikidata_sparql.py | 2026-04-09 | Feature batch 2 |
| query_archive_today.py | 2026-04-09 | Feature batch 2 |
| multi-domain/05-github-forensics | 2026-04-09 | Feature batch 2 |
| geolocation/08-ip-camera-discovery | 2026-04-09 | Feature batch 2 |
| corporate/02-executive-verification | 2026-04-09 | Feature batch 2 |
| verification/05-deepfake-detection | 2026-04-09 | Feature batch 2 |
| query_censys.py | 2026-04-09 | Integration batch |
| image_ela.py | 2026-04-09 | Integration batch |
| Face recognition ethics note | 2026-04-09 | Integration batch |
| SKILL.md tool reference (all 19 scripts) | 2026-04-09 | Integration batch |
| tool-guide.md (7 missing scripts added) | 2026-04-09 | Integration batch |
| Cross-references in domain-infrastructure, platform-directory, people-social-media | 2026-04-09 | Integration batch |
| Resolved 6/7 "Needs Research" items | 2026-04-09 | Integration batch |
| infrastructure/07-censys-host-recon | 2026-04-09 | Coverage batch |
| image-forensics/05-ela-manipulation-detection | 2026-04-09 | Coverage batch |
| infrastructure/08-virustotal-threat-assessment | 2026-04-09 | Coverage batch |
| people/06-wikidata-entity-resolution | 2026-04-09 | Coverage batch |
| verification/06-archive-today-recovery | 2026-04-09 | Coverage batch |
| CI: added pytest to lint.yml workflow | 2026-04-09 | Coverage batch |
