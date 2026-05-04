FROM node:20-bookworm

# System dependencies:
# - ffmpeg: video-reader MCP server + yt-dlp post-processing
# - python3 + venv: uvx (Reddit/fetch MCP servers) + uv run (osint scripts)
# - chromium + chromedriver: selenium MCP server (browser automation, reverse image search)
# - whois: query_whois.py
# - dnsutils: query_dns.py fallbacks
# - git: investigations template + general use
# - libnss3 et al.: chromium runtime deps (apt usually pulls them, listed for safety)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    python3 \
    python3-pip \
    python3-venv \
    chromium \
    chromium-driver \
    whois \
    dnsutils \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Python tools (system-wide, fine for containers)
# - uv: provides uvx for Reddit/fetch MCP servers, and uv run for osint scripts
# - yt-dlp: binary required by yt-dl MCP server
RUN pip install --break-system-packages uv yt-dlp

# Claude Code CLI
RUN npm install -g @anthropic-ai/claude-code

# Chromium flags for headless container use (consumed by selenium MCP)
ENV CHROME_FLAGS="--headless --no-sandbox --disable-gpu --disable-dev-shm-usage"
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV CHROMIUM_PATH=/usr/bin/chromium

# Create volume mount points with correct ownership BEFORE switching user.
# Docker named volumes inherit permissions from the image directory on first mount.
RUN mkdir -p /home/node/.claude /home/node/investigations /home/node/.npm \
    && chown -R node:node /home/node/.claude /home/node/investigations /home/node/.npm

USER node
WORKDIR /home/node

# Seed the investigations directory with a git repo so investigation templates
# (which expect git tracking) work out of the box.
RUN git -C /home/node/investigations init

# Copy entrypoint (sed strips Windows CRLF line endings if the host is Windows)
COPY --chown=node:node entrypoint.sh /home/node/entrypoint.sh
RUN sed -i 's/\r$//' /home/node/entrypoint.sh && chmod +x /home/node/entrypoint.sh

WORKDIR /home/node/investigations
ENTRYPOINT ["/home/node/entrypoint.sh"]
