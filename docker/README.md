# OSINT Agent — Docker

Run the OSINT plugin in a sandboxed container with `--dangerously-skip-permissions`.

## Prerequisites

- Docker
- API keys (all optional but each unlocks a tool):
  - [Tavily](https://tavily.com) — focused web search
  - [Google AI Studio](https://aistudio.google.com) — Gemini for image/video analysis
  - [Google Cloud Vision](https://cloud.google.com/vision) — reverse image search (free tier 1000/mo)
  - Optional: Reddit OAuth, SearXNG URL, yt-dlp cookies
- A Claude Max (or Pro/Team/Enterprise) subscription

## Build

```bash
docker build -t osint-agent docker/
```

## First Run (One-Time Setup)

The first run is interactive — you'll authenticate with Claude, install the plugin,
and answer its configuration prompts.

```bash
docker run -it \
  --name osint-agent \
  --shm-size=1g \
  -v osint-claude-config:/home/node/.claude \
  -v osint-investigations:/home/node/investigations \
  -v osint-npm-cache:/home/node/.npm \
  osint-agent
```

`--shm-size=1g` is required for Chromium (selenium MCP).

Follow the on-screen instructions:

1. Claude Code prints an OAuth URL — open it in your browser, sign in, paste the code back
2. Install the plugin:

   ```
   /plugin install osint@github:lawriec/claude-osint-plugin
   ```

3. When prompted, enter your API keys. Leave blank anything you don't have — the
   corresponding MCP server's tools will be unavailable but the rest of the plugin
   keeps working.
4. Exit (`/exit` or Ctrl+C)

Credentials, plugin config, and plugins are saved in the `osint-claude-config` volume.

## Subsequent Runs

After first-run setup, the agent launches autonomously with `--dangerously-skip-permissions`:

```bash
docker run -it --rm \
  --shm-size=1g \
  -v osint-claude-config:/home/node/.claude \
  -v osint-investigations:/home/node/investigations \
  -v osint-npm-cache:/home/node/.npm \
  osint-agent
```

No env-var flags are needed — the plugin reads keys from the persisted `.claude` volume.

## YouTube Cookies (Recommended)

`ytdlp_cookies_from_browser` doesn't work inside a container (no host browser), so
pass cookies as a file path. Without cookies, YouTube aggressively blocks `yt-dlp`.

1. Export cookies in Netscape format on the host (browser extension like
   "Get cookies.txt LOCALLY")
2. Pass via `YTDLP_COOKIES_BASE64` — the entrypoint decodes to
   `/home/node/.ytdlp-cookies.txt` and exports `YTDLP_COOKIES_FILE`:

   ```bash
   docker run -it --rm \
     --shm-size=1g \
     -e YTDLP_COOKIES_BASE64="$(base64 < cookies.txt)" \
     -v osint-claude-config:/home/node/.claude \
     -v osint-investigations:/home/node/investigations \
     -v osint-npm-cache:/home/node/.npm \
     osint-agent
   ```

## Self-Hosted SearXNG

The `searxng` MCP defaults to `http://localhost:8080`, which won't reach a SearXNG
container running on the host network. Either:

- Run SearXNG on a Docker network and pass `-e SEARXNG_URL=http://searxng:8080`
  with `--network` joining both containers, or
- Pass `-e SEARXNG_URL=http://host.docker.internal:8080` (Docker Desktop) to reach
  a SearXNG running on the host

## Volumes

| Volume | Container Path | Purpose |
|--------|---------------|---------|
| `osint-claude-config` | `/home/node/.claude` | OAuth credentials, plugins, settings |
| `osint-investigations` | `/home/node/investigations` | Investigation data, knowledge graph, templates (git-initialized) |
| `osint-npm-cache` | `/home/node/.npm` | npm package cache (MCP servers) |

All data persists across container restarts. No host filesystem is mounted.

## Notes

- Container runs as non-root user `node`
- Bundled tools: ffmpeg, chromium + chromedriver, whois, dnsutils, git, uv, yt-dlp
- MCP servers start on demand via Claude Code's plugin system; first start downloads them via npm/uvx
- The 12 MCP servers configured by the plugin: tavily, gemini, yt-dl, internet-archive, video-reader, selenium, fetch, memory-graph, common-crawl, reddit, searxng, google-reverse-image

## Resetting

```bash
# Remove all volumes (credentials, investigations, npm cache)
docker volume rm osint-claude-config osint-investigations osint-npm-cache

# Remove the image
docker rmi osint-agent
```
