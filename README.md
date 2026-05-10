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

## MCP Servers

This plugin configures 9 MCP servers:

| Server | Package | Purpose | API Key Required |
|--------|---------|---------|-----------------|
| **searxng** | `github:lawriec/mcp-searxng` | **Primary search tool.** Multi-engine web search via self-hosted SearXNG — queries Google, Bing, Brave, Yahoo, DuckDuckGo, and 250+ engines simultaneously. Full operator pass-through, category-based search, language filtering, and engine attribution. | No API key — requires Docker (see [SearXNG Setup](#searxng-setup)) |
| tavily | `tavily-mcp@latest` | Targeted web search with date filtering, content extraction, site crawling | Yes — `TAVILY_API_KEY` |
| gemini | `github:lawriec/mcp-gemini-media` | AI analysis of images, video, and audio files | Yes — `GEMINI_API_KEY` |
| google-reverse-image | `github:lawriec/mcp-google-reverse-image` | Reverse image search via Google Cloud Vision Web Detection — finds pages containing an image, exact/partial/visually-similar matches, and detected web entities. Accepts local paths or public URLs. | Yes — `GOOGLE_VISION_API_KEY` |
| yt-dl | `@kevinwatt/yt-dlp-mcp@latest` | YouTube search, metadata, downloads | No (but cookies strongly recommended — see below) |
| internet-archive | `github:lawriec/mcp-internet-archive` | Wayback Machine and Internet Archive access | No |
| video-reader | `github:lawriec/mcp-video-reader` | Video/image frame extraction, thumbnails, ffmpeg operations | No |
| common-crawl | `github:lawriec/mcp-common-crawl` | Search and extract content from Common Crawl web archives | No |
| reddit | `adhikasp/mcp-reddit` | Reddit thread discovery and post scraping | No (optional OAuth for higher rate limits) |

### SearXNG Setup

SearXNG is the plugin's primary search tool. It requires a local Docker instance — without
it, searches fall back to the less capable `WebSearch` tool.

**1. Install Docker** if you don't have it: <https://docs.docker.com/get-docker/>

**2. Start SearXNG** using the pre-configured Docker Compose setup in the
[mcp-searxng](https://github.com/lawriec/mcp-searxng) repo:

```bash
git clone https://github.com/lawriec/mcp-searxng.git
cd mcp-searxng/docker
docker compose up -d
```

**3. Verify** it's running:

```bash
curl "http://localhost:8080/search?q=test&format=json" | head -c 200
```

**4. Note the URL** — you'll be asked for it when you install the plugin.
   The default is `http://localhost:8080`.

SearXNG runs as a lightweight Docker container. Start it before launching Claude Code and
leave it running — it uses minimal resources when idle.

**Optional: VPN protection** — SearXNG queries upstream engines (Google, Bing, etc.) directly
from your IP. During intensive OSINT sessions this can lead to rate-limiting or blocking.
The mcp-searxng Docker setup includes an optional OpenVPN sidecar that routes all search
traffic through a VPN tunnel:

1. Place `.ovpn` files from your VPN provider (NordVPN, ExpressVPN, Surfshark, ProtonVPN,
   Mullvad, etc.) into a folder
2. If your provider requires auth, add a `default.auth` file (username line 1, password line 2)
3. Set environment variables and start with the VPN override:

```bash
export OPENVPN_CONFIG_DIR="$HOME/vpn-profiles"
export OPENVPN_PROFILE="us-east"  # .ovpn filename without extension
cd mcp-searxng/docker
docker compose -f docker-compose.yml -f docker-compose.vpn.yml up -d
```

The VPN container automatically rotates to a random profile every 30 minutes (configurable
via `ROTATE_INTERVAL_MINS`). Set to `0` to stay on one profile.

**Without VPN, everything works normally** — just use `docker compose up -d` as shown above.

See the [mcp-searxng README](https://github.com/lawriec/mcp-searxng#readme) for engine
customization, troubleshooting, and VPN setup details.

### Configuring the Plugin

Each MCP server needs credentials or config before it can connect. The plugin declares
its configurable values in `plugin.json`'s `userConfig` block, and `.mcp.json` references
them as plain `${KEY}` substitutions — meaning **you can set them either way**:

- **Path A — `/plugin` configure UI** (recommended for most users). Values are stored in
  `settings.json` (non-sensitive) or your system keychain (sensitive), and exported to
  each MCP server's subprocess as environment variables.
- **Path B — shell environment variables.** Export them in your shell profile before
  launching `claude`. Claude Code picks them up automatically at startup.

You only need **one** of these paths for any given key. Leaving a key blank disables that
specific MCP server's features but keeps the rest of the plugin working.

> If a value is set in both places, the `/plugin` config takes precedence.

> **`SEARXNG_URL` note**: defaults to `http://localhost:8080`. If you run SearXNG on
> that port, you do not need to set it. Only set it if your instance lives elsewhere.

**Config keys:**

| Key | Required? | Where to get it |
|-----|-----------|-----------------|
| `TAVILY_API_KEY` | Recommended | <https://tavily.com> |
| `GEMINI_API_KEY` | Recommended | <https://aistudio.google.com/apikey> |
| `GOOGLE_VISION_API_KEY` | Optional | <https://console.cloud.google.com/apis/credentials> (enable the Cloud Vision API first) — free tier: 1,000 requests/month |
| `SEARXNG_URL` | Recommended | Your local SearXNG instance, usually `http://localhost:8080` (see [SearXNG Setup](#searxng-setup) above) |
| `YTDLP_COOKIES_FROM_BROWSER` | **Strongly recommended** | Browser name: `chrome`, `firefox`, `edge`, `safari`, `opera`, `brave`, or `chromium`. yt-dlp reads cookies directly from that browser's cookie store. |
| `YTDLP_COOKIES_FILE` | Alternative to above | Absolute path to a Netscape-format `cookies.txt`. Takes priority over the browser option if both are set. |
| `REDDIT_CLIENT_ID` / `REDDIT_CLIENT_SECRET` / `REDDIT_REFRESH_TOKEN` | Optional | <https://www.reddit.com/prefs/apps> — only needed for higher Reddit API rate limits; leave blank to use anonymous mode |

**Why YouTube cookies matter:** without them, YouTube aggressively blocks `yt-dlp` —
even basic metadata lookups fail. Setting `YTDLP_COOKIES_FROM_BROWSER` to your browser
name is the single biggest reliability win you can make. See the
[yt-dlp-mcp cookies docs](https://github.com/kevinwatt/yt-dlp-mcp/blob/main/docs/cookies.md)
for the full list of supported browsers and file format details.

#### Setting values via shell environment variables

```bash
# Linux / macOS — add to ~/.bashrc, ~/.zshrc, etc.
export TAVILY_API_KEY="tvly-..."
export GEMINI_API_KEY="..."
export GOOGLE_VISION_API_KEY="..."
export SEARXNG_URL="http://localhost:8080"
export YTDLP_COOKIES_FROM_BROWSER="chrome"
```

```powershell
# Windows PowerShell — add to $PROFILE
$env:TAVILY_API_KEY = "tvly-..."
$env:GEMINI_API_KEY = "..."
$env:GOOGLE_VISION_API_KEY = "..."
$env:SEARXNG_URL = "http://localhost:8080"
$env:YTDLP_COOKIES_FROM_BROWSER = "chrome"
```

Then start `claude` in that shell. `.mcp.json` references `${TAVILY_API_KEY}` etc.
directly, so Claude Code expands them from the process environment at startup.

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
