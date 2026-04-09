# Docker Container for OSINT Agent

Run the OSINT plugin in a sandboxed container with full tool access.

## Build

```bash
docker build -t osint-agent docker/
```

## Run

```bash
docker run -it \
  --shm-size=1g \
  -e TAVILY_API_KEY="$TAVILY_API_KEY" \
  -e GEMINI_API_KEY="$GEMINI_API_KEY" \
  -v osint-claude-config:/root/.claude \
  -v osint-investigations:/home/node/investigations \
  osint-agent
```

## Volumes

| Volume | Purpose |
|--------|---------|
| `osint-claude-config` | OAuth tokens, plugin config, settings |
| `osint-investigations` | Investigation data, knowledge graph |

## Notes

- `--shm-size=1g` is required for Chromium (Selenium MCP)
- First start is slow — npm downloads MCP server packages on demand
- Subsequent starts are faster — packages are cached in the config volume
- The container has full internet access for OSINT research
