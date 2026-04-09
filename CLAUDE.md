# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A Claude Code plugin that provides an open source intelligence (OSINT) research skill. It is **not** a traditional software project — there is no build step, no compiled code. The repository is a plugin definition consisting of:

- **`.claude-plugin/plugin.json`** — Plugin metadata (name, description, author)
- **`.mcp.json`** — MCP server configuration (11 servers for research tools)
- **`skills/osint/SKILL.md`** — The core skill definition (OSINT methodology, investigation workflow)
- **`skills/osint/references/`** — Domain-specific reference guides loaded on-demand
- **`skills/osint/scripts/`** — Python scripts runnable via `uv run` (no pre-installation needed)
- **`skills/osint/templates/`** — Investigation workspace templates
- **`challenges/`** — Verifiable OSINT challenges for testing and self-evaluation
- **`tests/`** — Skill integrity tests, script validation, challenge validation

## Architecture

The plugin works through Claude Code's plugin system. When installed, it:

1. Registers MCP servers (defined in `.mcp.json`) that provide tools for web search, archive access, image/video analysis, browser automation, and knowledge graph persistence
2. Exposes the `osint` skill (defined in `SKILL.md`) that triggers automatically when users describe OSINT tasks

**SKILL.md** is the most important file. It defines the complete OSINT methodology following the intelligence cycle: Define (Step 1), Plan (Step 2), Collect (Step 3), Analyze (Step 4), Report (Step 5). Reference files in `references/` are loaded on-demand when specific domains or scenarios arise.

## OSINT Domains Covered

- **Geolocation** — Identifying locations from images/video (GeoGuessr-style)
- **People / Social Media** — Username enumeration, profile correlation, SOCMINT
- **Domain / Infrastructure** — WHOIS, DNS, subdomains, certificate transparency, IP enrichment
- **Image / Video Forensics** — EXIF extraction, reverse image search, manipulation detection
- **Document Analysis** — PDF metadata, email headers, file forensics
- **Vehicle / Object ID** — License plates, aircraft (ADS-B), ships (AIS)
- **Cryptocurrency / Financial** — Blockchain explorers, wallet tracing
- **Radio / Signals** — SDR, broadcast identification

## Scripts

Scripts live in `skills/osint/scripts/` and use `# /// script` blocks for `uv` dependency management. Run them with `uv run <script> <args>`. They output JSON to stdout and log to stderr.

Key scripts:
- `query_dns.py` — DNS enumeration (A, AAAA, MX, TXT, NS, SOA, CNAME, PTR)
- `query_whois.py` — Domain WHOIS lookup with parsed fields
- `query_crtsh.py` — Certificate transparency search via crt.sh
- `query_shodan_internetdb.py` — Shodan InternetDB (free, no API key)
- `extract_exif.py` — Image EXIF/metadata extraction with GPS support
- `check_username.py` — Username existence check across platforms
- `sun_position.py` — Solar angle calculator for shadow-based geolocation
- `analyze_email_headers.py` — Email header parsing and hop analysis
- `query_blockchain.py` — Bitcoin/Ethereum address lookup
- `discover_reddit_threads.py` — Reddit thread discovery for OSINT communities
- `query_flightradar.py` — Aircraft tracking via OpenSky Network API (free, no key)
- `query_ais.py` — Vessel/ship tracking via Fintraffic AIS API
- `query_urlscan.py` — URLScan.io search for threat intelligence
- `query_ipinfo.py` — IP geolocation and ASN lookup via ip-api.com

## MCP Servers

Eleven MCP servers are configured. Two require API keys via environment variables (`TAVILY_API_KEY`, `GEMINI_API_KEY`). The `yt-dl` server accepts `YTDLP_COOKIES_FROM_BROWSER` or `YTDLP_COOKIES_FILE` for YouTube authentication. The `reddit` server optionally accepts `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, and `REDDIT_REFRESH_TOKEN`. The `fetch` and `reddit` servers use `uvx` (Python); all others use `npx`.

## Plugin Installation

```
/plugin install osint@github:lawriec/claude-osint-plugin
```

## Testing

```bash
uv run pytest tests/                              # All tests
uv run pytest tests/test_skill_integrity.py        # Skill/reference link validation
uv run pytest tests/ -m "not integration"          # Skip network-dependent tests
ruff check skills/osint/scripts/                   # Lint scripts
```

## Editing Guidelines

- **SKILL.md changes** affect the core OSINT behavior. Preserve the intelligence cycle structure (Define → Plan → Collect → Analyze → Report).
- **Reference files** are self-contained guides. Each is read only when relevant. They should remain independently useful.
- **Scripts** must have `# /// script` blocks with dependencies, accept `--help`, output JSON to stdout, and log to stderr.
- **Challenges** must have Scenario, Expected Approach, Verification, and Ground Truth sections.
- **`.mcp.json`** uses `${VARIABLE}` placeholders for API keys that expand from shell environment variables at startup.

## Self-Improvement

The `community-analysis.yml` GitHub workflow runs weekly, scraping OSINT communities (Reddit, Bellingcat, Sector035) and creating PRs with skill improvements. The workflow instructions are in `skills/osint/scripts/loop-analyze-community.md`.

## Feature Development

`TODO.md` contains a structured backlog with "Ready to build", "Needs research", and "Blocked" categories. `IDEAS.md` is an unstructured brainstorming space. The community analysis workflow can append ideas to IDEAS.md.
