# OSINT Plugin for Claude Code

An open source intelligence (OSINT) research skill for [Claude Code](https://claude.ai/code). Investigate people, locations, domains, images, infrastructure, and digital artifacts using publicly available information.

## Installation

```
/plugin install osint@github:lawriec/claude-osint-plugin
```

## What It Does

When you ask Claude Code to investigate something — a person, a location in a photo, a suspicious domain, an image's metadata — this plugin activates a structured OSINT methodology based on the intelligence cycle:

1. **Define** the intelligence requirement
2. **Plan** the collection strategy
3. **Collect** data across multiple sources
4. **Analyze** and cross-reference findings
5. **Report** with evidence provenance and confidence ratings

## OSINT Domains

| Domain | Capabilities |
|--------|-------------|
| **Geolocation** | Identify locations from photos/video using signs, vegetation, road markings, sun position, architecture |
| **People / Social Media** | Username enumeration, profile correlation across platforms, SOCMINT |
| **Domain / Infrastructure** | WHOIS, DNS enumeration, subdomain discovery, certificate transparency, IP enrichment |
| **Image / Video Forensics** | EXIF extraction, reverse image search, manipulation detection, metadata analysis |
| **Document Analysis** | PDF metadata, email header analysis, file forensics |
| **Vehicle / Object ID** | License plates, aircraft tracking (ADS-B), ship tracking (AIS) |
| **Cryptocurrency** | Blockchain address lookup, wallet tracing, transaction analysis |
| **Radio / Signals** | Broadcast identification, amateur radio callsign lookup |

## Required API Keys

Set these environment variables before using the plugin:

| Variable | Required | Source |
|----------|----------|--------|
| `TAVILY_API_KEY` | Yes | [tavily.com](https://tavily.com) (free tier available) |
| `GEMINI_API_KEY` | Yes | [Google AI Studio](https://aistudio.google.com) |
| `YTDLP_COOKIES_FROM_BROWSER` | Recommended | Browser name (e.g., `chrome`) for YouTube access |
| `REDDIT_CLIENT_ID` | Optional | [Reddit apps](https://www.reddit.com/prefs/apps) for higher rate limits |
| `REDDIT_CLIENT_SECRET` | Optional | Same as above |

## MCP Servers

This plugin configures 11 MCP servers:

| Server | Purpose |
|--------|---------|
| **tavily** | Web search with date/domain filtering |
| **gemini** | AI analysis of images and video |
| **searxng** | Multi-engine meta-search (250+ engines) |
| **selenium** | Browser automation for JS-heavy sites |
| **fetch** | Simple URL fetching |
| **memory-graph** | Knowledge graph for entity relationships |
| **reddit** | Reddit API access |
| **video-reader** | Video/image frame extraction and analysis |
| **yt-dl** | YouTube metadata and downloads |
| **internet-archive** | Wayback Machine access |
| **common-crawl** | Historical web crawl data |

### SearXNG Setup

SearXNG requires a local Docker instance:

```bash
docker run -d --name searxng -p 8080:8080 \
  -v "${PWD}/searxng:/etc/searxng" \
  -e "BASE_URL=http://localhost:8080" \
  searxng/searxng
```

## OSINT Scripts

Standalone Python scripts runnable via `uv run` (no pre-installation needed):

```bash
uv run skills/osint/scripts/query_dns.py all example.com
uv run skills/osint/scripts/query_whois.py lookup example.com
uv run skills/osint/scripts/query_crtsh.py subdomains example.com
uv run skills/osint/scripts/query_shodan_internetdb.py 8.8.8.8
uv run skills/osint/scripts/extract_exif.py gps photo.jpg
uv run skills/osint/scripts/check_username.py johndoe
uv run skills/osint/scripts/sun_position.py calculate --lat 51.5 --lon -0.1 --date 2024-06-15 --time 14:30
```

## OSINT Resources

### Learning & Methodology
- [The OSINT Handbook](https://www.osinthandbook.com/) — Comprehensive OSINT reference
- [Bellingcat](https://www.bellingcat.com/) — Investigative journalism using OSINT methodology
- [OSINT Framework](https://osintframework.com/) — Categorized directory of OSINT tools
- [IntelTechniques](https://inteltechniques.com/) — Michael Bazzell's OSINT resources and tools
- [Trace Labs](https://www.tracelabs.org/) — Missing persons OSINT CTF events
- [OSINT Curious](https://osintcurio.us/) — Community, podcast, and 10-minute tips
- [Sector035 — Week in OSINT](https://sector035.nl/) — Weekly OSINT newsletter

### Geolocation
- [GeoRainbolt](https://www.youtube.com/@georainbolt) — GeoGuessr techniques and analysis
- [GeoTips](https://geotips.net/) — Country-specific geolocation clues
- [Plonkit](https://www.plonkit.net/) — Google Street View coverage and meta-clues
- [Bellingcat Geolocation Toolkit](https://docs.google.com/document/d/1BfLPJpRtyq4RFtHJoNpvWQjmGnyVkfE2HYoICKOGguA/) — Shadow analysis, landmark matching

### Infrastructure & Domain
- [Shodan](https://www.shodan.io/) — Internet-connected device search (InternetDB is free)
- [Censys](https://search.censys.io/) — Internet-wide scanning data
- [crt.sh](https://crt.sh/) — Certificate transparency log search (free, no auth)
- [SecurityTrails](https://securitytrails.com/) — Historical DNS and WHOIS data
- [VirusTotal](https://www.virustotal.com/) — URL/file/domain analysis

### People & Social Media
- [Sherlock](https://github.com/sherlock-project/sherlock) — Username enumeration across 400+ sites
- [Maigret](https://github.com/soxoj/maigret) — Advanced username enumeration
- [WhatsMyName](https://whatsmyname.app/) — Username search across platforms
- [Have I Been Pwned](https://haveibeenpwned.com/) — Breach data search

### Communities
- [r/OSINT](https://www.reddit.com/r/OSINT/) — OSINT discussion and tools
- [r/geoguessr](https://www.reddit.com/r/geoguessr/) — Geolocation community
- [r/RBI](https://www.reddit.com/r/RBI/) — Reddit Bureau of Investigation
- [r/traceanobject](https://www.reddit.com/r/traceanobject/) — Europol image analysis
- [SANS OSINT Summit](https://www.sans.org/cyber-security-summit/) — Annual training event

## Development

```bash
# Run tests
uv run pytest tests/

# Lint
ruff check skills/osint/scripts/
ruff format skills/osint/scripts/
```

## License

MIT
