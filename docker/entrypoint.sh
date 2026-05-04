#!/bin/bash
set -e

# --- YouTube cookie handling ---
# yt-dlp inside a container can't read host browser cookies. Pass cookies as
# base64 via YTDLP_COOKIES_BASE64; we materialize them at a fixed path and
# export YTDLP_COOKIES_FILE so the yt-dl MCP picks them up.
COOKIES_PATH=/home/node/.ytdlp-cookies.txt
if [ -n "$YTDLP_COOKIES_BASE64" ]; then
  echo "$YTDLP_COOKIES_BASE64" | base64 -d > "$COOKIES_PATH"
  export YTDLP_COOKIES_FILE="$COOKIES_PATH"
  echo "[entrypoint] YouTube cookies decoded to $COOKIES_PATH"
fi

# --- First-run detection ---
# On first run, we leave permission prompts ON so Claude Code's OAuth flow
# works. After credentials are persisted, switch to autonomous mode.
if [ ! -f "$HOME/.claude/.credentials.json" ]; then
  echo "============================================"
  echo "  First-run setup required"
  echo "============================================"
  echo ""
  echo "Claude Code will prompt you to authenticate."
  echo "It prints an OAuth URL — open it in your host"
  echo "browser, sign in, and paste the code back."
  echo ""
  echo "After authenticating, install the plugin:"
  echo ""
  echo "  /plugin install osint@github:lawriec/claude-osint-plugin"
  echo ""
  echo "The plugin will prompt for API keys (Tavily,"
  echo "Gemini, Google Vision, optional Reddit, SearXNG"
  echo "URL, etc.). Leave anything you don't have blank."
  echo ""
  echo "Credentials, plugin config, and installed plugins"
  echo "persist in the osint-claude-config Docker volume."
  echo "============================================"
  echo ""
  exec claude "$@"
else
  # Normal run — autonomous mode
  exec claude --dangerously-skip-permissions "$@"
fi
