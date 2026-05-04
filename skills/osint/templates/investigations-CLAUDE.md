# CLAUDE.md — OSINT Investigations Workspace

This directory contains OSINT investigations. Each subdirectory is a separate investigation.

## Structure

```
investigations-workspace/
├── CLAUDE.md               # This file
├── .gitignore              # Ignores sensitive data
├── knowledge-graph/        # Shared knowledge graph (memory-graph MCP)
└── <investigation-name>/   # One folder per investigation
    ├── search-log.md       # Every query and result (audit trail)
    ├── leads.md            # Active leads with priority
    ├── dead-ends.md        # Failed approaches
    ├── evidence-chain.md   # Source → finding → conclusion
    ├── report.md           # Structured findings
    └── downloads/          # Saved artifacts (screenshots, files)
```

## Working in This Workspace

1. **Always log queries** in search-log.md — every tool call, every search, every result
2. **Update leads.md** when you find something promising
3. **Record dead ends** so you don't repeat them
4. **Maintain evidence chains** — every finding must trace to a source
5. **Use the knowledge graph** (`memory-graph` MCP) to track entities and relationships across investigations

## Available Tools

### Scripts (run via `uv run skills/osint/scripts/<name>`)

| Category | Scripts |
|----------|---------|
| **Domain/Infra** | `query_dns.py`, `query_whois.py`, `query_crtsh.py`, `query_shodan_internetdb.py`, `query_censys.py` |
| **IP Intelligence** | `query_ipinfo.py` |
| **Threat Intel** | `query_virustotal.py`, `query_urlscan.py` |
| **People** | `check_username.py`, `discover_reddit_threads.py`, `query_wikidata_sparql.py` |
| **Image/Media** | `extract_exif.py`, `image_ela.py` |
| **Transportation** | `query_flightradar.py`, `query_ais.py` |
| **Crypto** | `query_blockchain.py` |
| **Documents** | `analyze_email_headers.py` |
| **Archival** | `query_archive_today.py` |
| **Geolocation** | `sun_position.py` |

### MCP Servers

| Server | Use for |
|--------|---------|
| `tavily` | Web search, content extraction, site crawling |
| `searxng` | Broad meta-search across 250+ engines with operator params (site, filetype, after, before, inurl, intitle) |
| `google-reverse-image` | Reverse image search via Google Cloud Vision Web Detection |
| `gemini` | AI visual analysis of images, video, audio |
| `selenium` | Browser automation, screenshots, reverse image search |
| `internet-archive` | Wayback Machine snapshots |
| `common-crawl` | Historical web crawl data |
| `yt-dl` | Video/audio download and metadata |
| `video-reader` | Frame extraction, video info |
| `reddit` | Reddit thread and post content |
| `memory-graph` | Entity/relationship knowledge graph |
| `fetch` | Raw URL content retrieval |

## Ethics

- Only use publicly available information
- Never access accounts you don't own
- Document ethical reasoning when in doubt
- Be aware of legal boundaries in the relevant jurisdiction
- Read `opsec-ethics.md` for detailed guidance
